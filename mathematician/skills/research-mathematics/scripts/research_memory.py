#!/usr/bin/env python3
"""Manage a canonical document's curated SQLite research memory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Sequence


SCHEMA_VERSION = 3
DISPOSITIONS = ("open", "active", "parked", "rejected", "integrated")
CLAIM_STATUSES = ("conjectural", "supported", "refuted", "proved", "unresolved")
CARD_SUMMARY_FIELDS = (
    "slug",
    "kind",
    "title",
    "summary_md",
    "disposition",
    "claim_status",
    "reason",
    "next_test",
    "revival_condition",
)
CARD_FIELDS = (*CARD_SUMMARY_FIELDS[:4], "detail_md", *CARD_SUMMARY_FIELDS[4:])
REQUIRED_CARD_FIELDS = ("slug", "kind", "title", "summary_md", "disposition")
MUTABLE_CARD_FIELDS = tuple(name for name in CARD_FIELDS if name != "slug")
OPTIONAL_CARD_FIELDS = frozenset(
    {
        "detail_md",
        "claim_status",
        "reason",
        "next_test",
        "revival_condition",
    }
)
CARD_STATE_REQUIREMENTS = {
    "open": ("next_test",),
    "active": ("next_test",),
    "parked": ("revival_condition",),
    "rejected": ("reason",),
    "integrated": (),
}
CANONICAL_RELATIONS = (
    "same-subject",
    "addresses",
    "supports",
    "constrains",
    "tests",
    "implements",
    "integrated-at",
)
CANONICAL_ITEM_FIELDS = ("canonical_key", "kind", "title")
CANONICAL_ITEM_MUTABLE_FIELDS = ("kind", "title")
ORIGIN_FIELDS = (
    "card_slug",
    "source_locator",
    "source_slug",
    "source_digest",
    "applicability_md",
)
APPLY_BATCH_FIELDS = (
    "round_id",
    "batch_digest",
    "expected_database_revision",
    "expected_canonical_digest",
    "canonical_digest",
    "card_operations",
    "origin_operations",
    "edge_operations",
    "canonical_item_operations",
    "canonical_alias_operations",
    "card_canonical_link_operations",
)
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
SEMANTIC_KEY_RE = re.compile(
    r"[a-z0-9]+(?:-[a-z0-9]+)*(?:/[a-z0-9]+(?:-[a-z0-9]+)*)?\Z"
)
REQUIRED_COLUMNS = {
    "meta": {
        "singleton",
        "schema_version",
        "theory_slug",
        "canonical_path",
        "canonical_sha256",
        "database_revision",
        "last_round_id",
        "last_batch_digest",
        "created_at",
        "updated_at",
    },
    "card": set(CARD_SUMMARY_FIELDS)
    | {"revision", "content_sha256", "created_at", "updated_at"},
    "card_body": {"card_slug", "detail_md"},
    "card_origin": set(ORIGIN_FIELDS),
    "edge": {"source_slug", "relation", "target_slug", "note_md"},
    "canonical_item": {
        "canonical_key",
        "kind",
        "title",
        "anchor",
        "indexed_section_sha256",
        "fingerprint_version",
        "revision",
        "content_sha256",
        "created_at",
        "updated_at",
    },
    "canonical_alias": {"alias", "canonical_key", "source_locator"},
    "card_canonical_link": {
        "card_slug",
        "canonical_key",
        "relation",
        "note_md",
        "reviewed_canonical_sha256",
        "reviewed_section_sha256",
        "reviewed_card_revision",
        "revision",
        "created_at",
        "updated_at",
    },
}


class ResearchMemoryError(Exception):
    """A user-facing validation or conflict error."""


class JSONArgumentParser(argparse.ArgumentParser):
    """Report command-line validation failures through the JSON error path."""

    def error(self, message: str) -> None:
        raise ResearchMemoryError(message)


SCHEMA_SQL = """
CREATE TABLE meta (
    singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
    schema_version INTEGER NOT NULL CHECK (schema_version = 3),
    theory_slug TEXT NOT NULL CHECK (length(trim(theory_slug)) > 0),
    canonical_path TEXT NOT NULL CHECK (length(trim(canonical_path)) > 0),
    canonical_sha256 TEXT NOT NULL
        CHECK (length(canonical_sha256) = 64
               AND canonical_sha256 NOT GLOB '*[^0-9a-f]*'),
    database_revision INTEGER NOT NULL CHECK (database_revision >= 0),
    last_round_id TEXT,
    last_batch_digest TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK ((last_round_id IS NULL AND last_batch_digest IS NULL)
           OR (last_round_id IS NOT NULL AND last_batch_digest IS NOT NULL
               AND length(trim(last_round_id)) > 0
               AND length(last_batch_digest) = 64
               AND last_batch_digest NOT GLOB '*[^0-9a-f]*'))
);

CREATE TABLE card (
    slug TEXT PRIMARY KEY NOT NULL CHECK (length(trim(slug)) > 0),
    kind TEXT NOT NULL CHECK (length(trim(kind)) > 0),
    title TEXT NOT NULL CHECK (length(trim(title)) > 0),
    summary_md TEXT NOT NULL CHECK (length(trim(summary_md)) > 0),
    disposition TEXT NOT NULL
        CHECK (disposition IN ('open', 'active', 'parked', 'rejected', 'integrated')),
    claim_status TEXT
        CHECK (claim_status IS NULL OR claim_status IN
               ('conjectural', 'supported', 'refuted', 'proved', 'unresolved')),
    reason TEXT,
    next_test TEXT,
    revival_condition TEXT,
    revision INTEGER NOT NULL CHECK (revision >= 1),
    content_sha256 TEXT NOT NULL
        CHECK (length(content_sha256) = 64
               AND content_sha256 NOT GLOB '*[^0-9a-f]*'),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (disposition NOT IN ('open', 'active')
           OR length(trim(coalesce(next_test, ''))) > 0),
    CHECK (disposition <> 'parked'
           OR length(trim(coalesce(revival_condition, ''))) > 0),
    CHECK (disposition <> 'rejected'
           OR length(trim(coalesce(reason, ''))) > 0)
);

CREATE TABLE card_body (
    card_slug TEXT PRIMARY KEY NOT NULL REFERENCES card(slug) ON DELETE CASCADE,
    detail_md TEXT NOT NULL CHECK (length(trim(detail_md)) > 0)
);

CREATE TABLE card_origin (
    card_slug TEXT NOT NULL REFERENCES card(slug) ON DELETE CASCADE,
    source_locator TEXT NOT NULL CHECK (length(trim(source_locator)) > 0),
    source_slug TEXT NOT NULL CHECK (length(trim(source_slug)) > 0),
    source_digest TEXT NOT NULL
        CHECK (length(source_digest) = 64
               AND source_digest NOT GLOB '*[^0-9a-f]*'),
    applicability_md TEXT NOT NULL CHECK (length(trim(applicability_md)) > 0),
    PRIMARY KEY (card_slug, source_locator, source_slug, source_digest)
);

CREATE TABLE edge (
    source_slug TEXT NOT NULL REFERENCES card(slug) ON DELETE CASCADE,
    relation TEXT NOT NULL CHECK (length(trim(relation)) > 0),
    target_slug TEXT NOT NULL REFERENCES card(slug) ON DELETE CASCADE,
    note_md TEXT,
    PRIMARY KEY (source_slug, relation, target_slug)
);

CREATE TABLE canonical_item (
    canonical_key TEXT PRIMARY KEY NOT NULL CHECK (length(trim(canonical_key)) > 0),
    kind TEXT NOT NULL CHECK (length(trim(kind)) > 0),
    title TEXT NOT NULL CHECK (length(trim(title)) > 0),
    anchor TEXT NOT NULL UNIQUE CHECK (length(trim(anchor)) > 0),
    indexed_section_sha256 TEXT NOT NULL
        CHECK (length(indexed_section_sha256) = 64
               AND indexed_section_sha256 NOT GLOB '*[^0-9a-f]*'),
    fingerprint_version INTEGER NOT NULL CHECK (fingerprint_version >= 1),
    revision INTEGER NOT NULL CHECK (revision >= 1),
    content_sha256 TEXT NOT NULL
        CHECK (length(content_sha256) = 64
               AND content_sha256 NOT GLOB '*[^0-9a-f]*'),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE canonical_alias (
    alias TEXT PRIMARY KEY NOT NULL CHECK (length(trim(alias)) > 0),
    canonical_key TEXT NOT NULL REFERENCES canonical_item(canonical_key)
        ON DELETE CASCADE,
    source_locator TEXT CHECK (
        source_locator IS NULL OR length(trim(source_locator)) > 0
    )
);

CREATE TABLE card_canonical_link (
    card_slug TEXT NOT NULL REFERENCES card(slug) ON DELETE CASCADE,
    canonical_key TEXT NOT NULL REFERENCES canonical_item(canonical_key)
        ON DELETE CASCADE,
    relation TEXT NOT NULL CHECK (relation IN (
        'same-subject', 'addresses', 'supports', 'constrains', 'tests',
        'implements', 'integrated-at'
    )),
    note_md TEXT,
    reviewed_canonical_sha256 TEXT NOT NULL
        CHECK (length(reviewed_canonical_sha256) = 64
               AND reviewed_canonical_sha256 NOT GLOB '*[^0-9a-f]*'),
    reviewed_section_sha256 TEXT NOT NULL
        CHECK (length(reviewed_section_sha256) = 64
               AND reviewed_section_sha256 NOT GLOB '*[^0-9a-f]*'),
    reviewed_card_revision INTEGER NOT NULL CHECK (reviewed_card_revision >= 1),
    revision INTEGER NOT NULL CHECK (revision >= 1),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (relation <> 'same-subject' OR card_slug = canonical_key),
    PRIMARY KEY (card_slug, canonical_key, relation)
);

CREATE INDEX card_disposition_updated_idx ON card(disposition, updated_at DESC);
CREATE INDEX card_kind_idx ON card(kind);
CREATE INDEX card_origin_source_idx ON card_origin(source_locator, source_slug);
CREATE INDEX edge_target_idx ON edge(target_slug);
CREATE INDEX canonical_alias_key_idx ON canonical_alias(canonical_key);
CREATE INDEX card_canonical_link_key_idx
    ON card_canonical_link(canonical_key, relation);
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_digest(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def normalize_schema_sql(value: str) -> str:
    """Normalize harmless formatting while retaining schema semantics."""
    return " ".join(value.rstrip(";").split())


def expected_schema_objects() -> dict[tuple[str, str], str]:
    """Return the exact supported tables and indexes defined by this tool."""
    connection = sqlite3.connect(":memory:")
    try:
        connection.executescript(SCHEMA_SQL)
        return {
            (row[0], row[1]): normalize_schema_sql(row[2])
            for row in connection.execute(
                "SELECT type, name, sql FROM sqlite_master "
                "WHERE name NOT LIKE 'sqlite_%' AND sql IS NOT NULL"
            )
        }
    finally:
        connection.close()


def schema_object_errors(connection: sqlite3.Connection) -> list[str]:
    """Compare a database with the one supported schema, including checks."""
    expected = expected_schema_objects()
    actual = {
        (row[0], row[1]): normalize_schema_sql(row[2])
        for row in connection.execute(
            "SELECT type, name, sql FROM sqlite_master "
            "WHERE name NOT LIKE 'sqlite_%' AND sql IS NOT NULL"
        )
    }
    errors: list[str] = []
    missing = sorted(set(expected) - set(actual))
    unexpected = sorted(set(actual) - set(expected))
    changed = sorted(
        key for key in set(expected) & set(actual) if expected[key] != actual[key]
    )
    if missing:
        errors.append(
            f"missing schema-v{SCHEMA_VERSION} object(s): "
            + ", ".join(f"{kind} {name}" for kind, name in missing)
        )
    if unexpected:
        errors.append(
            f"unexpected schema-v{SCHEMA_VERSION} object(s): "
            + ", ".join(f"{kind} {name}" for kind, name in unexpected)
        )
    if changed:
        errors.append(
            f"schema-v{SCHEMA_VERSION} definition mismatch: "
            + ", ".join(f"{kind} {name}" for kind, name in changed)
        )
    return errors


def sqlite_sidecars(path: Path) -> list[Path]:
    return [
        Path(str(path) + suffix)
        for suffix in ("-journal", "-wal", "-shm")
        if Path(str(path) + suffix).exists()
    ]


def require_no_sidecars(path: Path) -> None:
    sidecars = sqlite_sidecars(path)
    if sidecars:
        raise ResearchMemoryError(
            "unsettled SQLite sidecar(s) present: "
            + ", ".join(str(sidecar) for sidecar in sidecars)
        )


def batch_content_digest(batch: Mapping[str, Any]) -> str:
    """Hash canonical JSON for the batch with its batch_digest field omitted."""
    return json_digest({key: value for key, value in batch.items() if key != "batch_digest"})


def require_mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ResearchMemoryError(f"{label} must be a JSON object")
    return value


def require_keys(value: Mapping[str, Any], allowed: Iterable[str], label: str) -> None:
    unknown = sorted(set(value) - set(allowed))
    if unknown:
        raise ResearchMemoryError(f"{label} has unknown field(s): {', '.join(unknown)}")


def require_text(value: Any, label: str) -> str:
    if not isinstance(value, str):
        raise ResearchMemoryError(f"{label} must be a string")
    normalized = value.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        raise ResearchMemoryError(f"{label} must not be empty")
    return normalized


def optional_text(value: Any, label: str) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ResearchMemoryError(f"{label} must be a string or null")
    normalized = value.replace("\r\n", "\n").replace("\r", "\n").strip()
    return normalized or None


def require_digest(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        raise ResearchMemoryError(f"{label} must be a lowercase SHA-256 hex digest")
    return value


def require_semantic_key(value: Any, label: str = "canonical key") -> str:
    key = require_text(value, label)
    if SEMANTIC_KEY_RE.fullmatch(key) is None:
        raise ResearchMemoryError(
            f"{label} must be a lowercase semantic kebab-case key"
        )
    return key


def scan_canonical_document(path: Path) -> Any:
    """Load the sibling source-preserving section index behind one boundary."""
    try:
        from canonical_sections import CanonicalSectionsError, scan_canonical
    except ImportError as error:
        raise ResearchMemoryError(
            "canonical section tooling is unavailable next to research_memory.py"
        ) from error
    try:
        return scan_canonical(path)
    except CanonicalSectionsError as error:
        raise ResearchMemoryError(f"canonical section validation failed: {error}")


def section_for_key(document: Any, key: str) -> Any:
    section = document.by_key.get(key)
    if section is None:
        raise ResearchMemoryError(
            f"canonical key {key!r} is not declared in the canonical document"
        )
    return section


def anchor_for_key(section: Any, key: str) -> str:
    try:
        return section.anchor_ids[section.keys.index(key)]
    except (AttributeError, IndexError, ValueError) as error:
        raise ResearchMemoryError(
            f"canonical section index has no anchor for key {key!r}"
        ) from error


def require_revision(value: Any, label: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ResearchMemoryError(f"{label} must be an integer >= {minimum}")
    return value


def normalize_card(raw: Mapping[str, Any]) -> dict[str, Any]:
    require_keys(raw, CARD_FIELDS, "card")
    missing = [name for name in REQUIRED_CARD_FIELDS if name not in raw]
    if missing:
        raise ResearchMemoryError(f"card is missing field(s): {', '.join(missing)}")

    card: dict[str, Any] = {}
    for name in CARD_FIELDS:
        value = raw.get(name)
        if name == "slug":
            card[name] = require_semantic_key(value, "card.slug")
        elif name in OPTIONAL_CARD_FIELDS:
            card[name] = optional_text(value, f"card.{name}")
        else:
            card[name] = require_text(value, f"card.{name}")

    if card["disposition"] not in DISPOSITIONS:
        raise ResearchMemoryError(
            "card.disposition must be one of: " + ", ".join(DISPOSITIONS)
        )
    if card["claim_status"] is not None and card["claim_status"] not in CLAIM_STATUSES:
        raise ResearchMemoryError(
            "card.claim_status must be null or one of: " + ", ".join(CLAIM_STATUSES)
        )
    for field in CARD_STATE_REQUIREMENTS[card["disposition"]]:
        if card[field] is None:
            raise ResearchMemoryError(
                f"{card['disposition']} cards require card.{field}"
            )
    return card


def card_digest(card: Mapping[str, Any]) -> str:
    return json_digest({name: card.get(name) for name in CARD_FIELDS})


def database_uri(path: Path, mode: str) -> str:
    return path.resolve().as_uri() + "?mode=" + mode


def connect_read_only(path: Path) -> sqlite3.Connection:
    if not path.is_file():
        raise ResearchMemoryError(f"database does not exist: {path}")
    connection = sqlite3.connect(database_uri(path, "ro"), uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only=ON")
    connection.execute("PRAGMA foreign_keys=ON")
    return connection


def connect_read_write(path: Path) -> sqlite3.Connection:
    if not path.is_file():
        raise ResearchMemoryError(f"database does not exist: {path}")
    connection = sqlite3.connect(
        database_uri(path, "rw"), uri=True, isolation_level=None, timeout=5.0
    )
    try:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA busy_timeout=5000")
        journal_mode = connection.execute("PRAGMA journal_mode").fetchone()[0]
        if str(journal_mode).lower() == "delete":
            return connection
        raise ResearchMemoryError(
            f"database journal mode is {journal_mode!r}, expected 'delete'"
        )
    except Exception:
        connection.close()
        raise


def read_meta(connection: sqlite3.Connection) -> sqlite3.Row:
    row = connection.execute("SELECT * FROM meta WHERE singleton = 1").fetchone()
    if row is None:
        raise ResearchMemoryError(
            f"database has no schema-v{SCHEMA_VERSION} metadata row"
        )
    return row


def require_current_schema(connection: sqlite3.Connection) -> sqlite3.Row:
    user_version = connection.execute("PRAGMA user_version").fetchone()[0]
    if user_version != SCHEMA_VERSION:
        raise ResearchMemoryError(
            f"user_version is {user_version}, expected {SCHEMA_VERSION}"
        )
    meta = read_meta(connection)
    if meta["schema_version"] != SCHEMA_VERSION:
        raise ResearchMemoryError(
            "metadata schema version is "
            f"{meta['schema_version']}, expected {SCHEMA_VERSION}"
        )
    definition_errors = schema_object_errors(connection)
    if definition_errors:
        raise ResearchMemoryError("; ".join(definition_errors))
    return meta


def canonical_from_meta(db_path: Path, meta: Mapping[str, Any]) -> Path:
    stored = Path(str(meta["canonical_path"]))
    if stored.is_absolute():
        raise ResearchMemoryError("metadata canonical_path must be relative to the database")
    return (db_path.resolve().parent / stored).resolve()


def require_markdown_file(raw_path: str, label: str = "canonical document") -> Path:
    requested = Path(raw_path)
    if requested.is_symlink():
        raise ResearchMemoryError(
            f"{label} must not be a symbolic link: {requested.absolute()}"
        )
    path = requested.resolve()
    if not path.is_file():
        raise ResearchMemoryError(f"{label} does not exist: {path}")
    if path.suffix.lower() not in (".md", ".markdown"):
        raise ResearchMemoryError(f"{label} must be a Markdown file")
    return path


def default_database_path(canonical: Path) -> Path:
    return canonical.with_suffix(".research.sqlite")


def create_database(canonical: Path, theory: str, db_path: Path) -> dict[str, Any]:
    if not db_path.parent.is_dir():
        raise ResearchMemoryError(
            f"database parent directory does not exist: {db_path.parent}"
        )
    require_no_sidecars(db_path)
    canonical_document = scan_canonical_document(canonical)

    try:
        descriptor = os.open(str(db_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ResearchMemoryError(f"refusing to overwrite existing path: {db_path}")
    os.close(descriptor)

    try:
        connection = sqlite3.connect(str(db_path), isolation_level=None)
        try:
            connection.execute("PRAGMA foreign_keys=ON")
            journal_mode = connection.execute("PRAGMA journal_mode=DELETE").fetchone()[0]
            if str(journal_mode).lower() != "delete":
                raise ResearchMemoryError("could not enable DELETE journal mode")
            connection.execute("BEGIN IMMEDIATE")
            connection.executescript(SCHEMA_SQL)
            connection.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
            timestamp = utc_now()
            relative = Path(os.path.relpath(canonical, db_path.parent)).as_posix()
            digest = canonical_document.canonical_sha256
            connection.execute(
                """
                INSERT INTO meta (
                    singleton, schema_version, theory_slug, canonical_path,
                    canonical_sha256, database_revision, last_round_id,
                    last_batch_digest, created_at, updated_at
                ) VALUES (1, ?, ?, ?, ?, 0, NULL, NULL, ?, ?)
                """,
                (SCHEMA_VERSION, theory, relative, digest, timestamp, timestamp),
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
    except Exception:
        db_path.unlink(missing_ok=True)
        raise

    return {
        "ok": True,
        "command": "init",
        "database": str(db_path),
        "canonical": str(canonical),
        "theory": theory,
        "schema_version": SCHEMA_VERSION,
        "database_revision": 0,
        "canonical_digest": digest,
    }


def command_init(args: argparse.Namespace) -> dict[str, Any]:
    canonical = require_markdown_file(args.canonical)
    theory = require_text(args.theory, "theory")
    if args.db:
        requested_db = Path(args.db)
        if requested_db.is_symlink() or requested_db.exists():
            raise ResearchMemoryError(
                f"refusing to overwrite existing path: {requested_db.absolute()}"
            )
        db_path = requested_db.resolve()
    else:
        db_path = default_database_path(canonical)
    return create_database(canonical, theory, db_path)


def load_batch(path: Path) -> Mapping[str, Any]:
    if not path.is_file():
        raise ResearchMemoryError(f"batch file does not exist: {path}")
    try:
        with path.open("r", encoding="utf-8") as stream:
            value = json.load(stream)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ResearchMemoryError(f"cannot read batch JSON: {error}")
    return require_mapping(value, "batch")


def validate_batch(raw: Mapping[str, Any]) -> dict[str, Any]:
    fields = set(APPLY_BATCH_FIELDS)
    require_keys(raw, fields, "batch")
    missing = sorted(fields - set(raw))
    if missing:
        raise ResearchMemoryError(f"batch is missing field(s): {', '.join(missing)}")
    operation_fields = (
        "card_operations",
        "origin_operations",
        "edge_operations",
        "canonical_item_operations",
        "canonical_alias_operations",
        "card_canonical_link_operations",
    )
    for field in operation_fields:
        if not isinstance(raw[field], list):
            raise ResearchMemoryError(f"batch.{field} must be a JSON array")
    declared_digest = require_digest(raw["batch_digest"], "batch.batch_digest")
    actual_digest = batch_content_digest(raw)
    if declared_digest != actual_digest:
        raise ResearchMemoryError(
            "batch.batch_digest does not match canonical JSON for the batch content"
        )
    return {
        "round_id": require_text(raw["round_id"], "batch.round_id"),
        "batch_digest": declared_digest,
        "expected_database_revision": require_revision(
            raw["expected_database_revision"], "batch.expected_database_revision"
        ),
        "expected_canonical_digest": require_digest(
            raw["expected_canonical_digest"], "batch.expected_canonical_digest"
        ),
        "canonical_digest": require_digest(
            raw["canonical_digest"], "batch.canonical_digest"
        ),
        **{field: raw[field] for field in operation_fields},
    }


def row_as_card(row: Mapping[str, Any]) -> dict[str, Any]:
    return {name: row[name] for name in CARD_FIELDS}


def select_card(connection: sqlite3.Connection, slug: str) -> Optional[sqlite3.Row]:
    return connection.execute(
        """
        SELECT card.*, card_body.detail_md
        FROM card LEFT JOIN card_body ON card_body.card_slug = card.slug
        WHERE card.slug = ?
        """,
        (slug,),
    ).fetchone()


def apply_card_operation(
    connection: sqlite3.Connection, raw: Any, timestamp: str
) -> str:
    operation = require_mapping(raw, "card operation")
    op = require_text(operation.get("op"), "card operation.op")
    if op == "add":
        require_keys(operation, ("op", "card"), "card add operation")
        if "card" not in operation:
            raise ResearchMemoryError("card add operation requires card")
        card = normalize_card(require_mapping(operation["card"], "card"))
        values = [card[name] for name in CARD_SUMMARY_FIELDS]
        try:
            connection.execute(
                f"""
                INSERT INTO card ({', '.join(CARD_SUMMARY_FIELDS)}, revision,
                                  content_sha256, created_at, updated_at)
                VALUES ({', '.join('?' for _ in CARD_SUMMARY_FIELDS)}, 1, ?, ?, ?)
                """,
                (*values, card_digest(card), timestamp, timestamp),
            )
            if card["detail_md"] is not None:
                connection.execute(
                    "INSERT INTO card_body (card_slug, detail_md) VALUES (?, ?)",
                    (card["slug"], card["detail_md"]),
                )
        except sqlite3.IntegrityError as error:
            raise ResearchMemoryError(f"cannot add card {card['slug']!r}: {error}")
        return card["slug"]

    if op == "update":
        require_keys(
            operation,
            ("op", "slug", "expected_revision", "changes"),
            "card update operation",
        )
        slug = require_text(operation.get("slug"), "card update operation.slug")
        expected = require_revision(
            operation.get("expected_revision"),
            "card update operation.expected_revision",
            1,
        )
        changes = require_mapping(
            operation.get("changes"), "card update operation.changes"
        )
        require_keys(changes, MUTABLE_CARD_FIELDS, "card update operation.changes")
        if not changes:
            raise ResearchMemoryError("card update operation.changes must not be empty")
        row = select_card(connection, slug)
        if row is None:
            raise ResearchMemoryError(f"card does not exist: {slug}")
        if row["revision"] != expected:
            raise ResearchMemoryError(
                f"card {slug!r} revision conflict: expected {expected}, found {row['revision']}"
            )
        card = row_as_card(row)
        card.update(changes)
        card = normalize_card(card)
        mutable_summary_fields = tuple(
            name for name in CARD_SUMMARY_FIELDS if name != "slug"
        )
        assignments = ", ".join(f"{name} = ?" for name in mutable_summary_fields)
        values = [card[name] for name in mutable_summary_fields]
        cursor = connection.execute(
            f"""
            UPDATE card
            SET {assignments}, revision = revision + 1,
                content_sha256 = ?, updated_at = ?
            WHERE slug = ? AND revision = ?
            """,
            (*values, card_digest(card), timestamp, slug, expected),
        )
        if cursor.rowcount != 1:
            raise ResearchMemoryError(f"card {slug!r} changed during update")
        if card["detail_md"] is None:
            connection.execute("DELETE FROM card_body WHERE card_slug = ?", (slug,))
        else:
            connection.execute(
                """
                INSERT INTO card_body (card_slug, detail_md) VALUES (?, ?)
                ON CONFLICT(card_slug) DO UPDATE SET detail_md = excluded.detail_md
                """,
                (slug, card["detail_md"]),
            )
        return slug

    if op == "delete":
        require_keys(
            operation, ("op", "slug", "expected_revision"), "card delete operation"
        )
        slug = require_text(operation.get("slug"), "card delete operation.slug")
        expected = require_revision(
            operation.get("expected_revision"),
            "card delete operation.expected_revision",
            1,
        )
        cursor = connection.execute(
            "DELETE FROM card WHERE slug = ? AND revision = ?", (slug, expected)
        )
        if cursor.rowcount != 1:
            row = connection.execute(
                "SELECT revision FROM card WHERE slug = ?", (slug,)
            ).fetchone()
            if row is None:
                raise ResearchMemoryError(f"card does not exist: {slug}")
            raise ResearchMemoryError(
                f"card {slug!r} revision conflict: expected {expected}, found {row['revision']}"
            )
        return slug

    raise ResearchMemoryError("card operation.op must be add, update, or delete")


def normalize_origin(raw: Mapping[str, Any], include_applicability: bool) -> dict[str, Any]:
    allowed = ("op", "card_slug", "source_locator", "source_slug", "source_digest")
    if include_applicability:
        allowed += ("applicability_md",)
    require_keys(raw, allowed, "origin operation")
    return {
        "card_slug": require_text(raw.get("card_slug"), "origin operation.card_slug"),
        "source_locator": require_text(
            raw.get("source_locator"), "origin operation.source_locator"
        ),
        "source_slug": require_text(
            raw.get("source_slug"), "origin operation.source_slug"
        ),
        "source_digest": require_digest(
            raw.get("source_digest"), "origin operation.source_digest"
        ),
        "applicability_md": (
            require_text(
                raw.get("applicability_md"), "origin operation.applicability_md"
            )
            if include_applicability
            else None
        ),
    }


def apply_origin_operation(connection: sqlite3.Connection, raw: Any) -> dict[str, str]:
    operation = require_mapping(raw, "origin operation")
    op = require_text(operation.get("op"), "origin operation.op")
    if op not in ("add", "delete"):
        raise ResearchMemoryError("origin operation.op must be add or delete")
    origin = normalize_origin(operation, include_applicability=(op == "add"))
    key = tuple(origin[name] for name in ORIGIN_FIELDS[:4])
    if op == "add":
        try:
            connection.execute(
                """
                INSERT INTO card_origin (
                    card_slug, source_locator, source_slug, source_digest,
                    applicability_md
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (*key, origin["applicability_md"]),
            )
        except sqlite3.IntegrityError as error:
            raise ResearchMemoryError(f"cannot add card origin {key!r}: {error}")
    else:
        cursor = connection.execute(
            """
            DELETE FROM card_origin
            WHERE card_slug = ? AND source_locator = ? AND source_slug = ?
                  AND source_digest = ?
            """,
            key,
        )
        if cursor.rowcount != 1:
            raise ResearchMemoryError(f"card origin does not exist: {key!r}")
    return {
        "card_slug": origin["card_slug"],
        "source_locator": origin["source_locator"],
        "source_slug": origin["source_slug"],
        "source_digest": origin["source_digest"],
    }


def normalize_edge(raw: Mapping[str, Any], include_note: bool) -> dict[str, Any]:
    allowed = ("op", "source_slug", "relation", "target_slug")
    if include_note:
        allowed += ("note_md",)
    require_keys(raw, allowed, "edge operation")
    edge = {
        "source_slug": require_text(raw.get("source_slug"), "edge operation.source_slug"),
        "relation": require_text(raw.get("relation"), "edge operation.relation"),
        "target_slug": require_text(raw.get("target_slug"), "edge operation.target_slug"),
        "note_md": (
            optional_text(raw.get("note_md"), "edge operation.note_md")
            if include_note
            else None
        ),
    }
    return edge


def apply_edge_operation(connection: sqlite3.Connection, raw: Any) -> dict[str, str]:
    operation = require_mapping(raw, "edge operation")
    op = require_text(operation.get("op"), "edge operation.op")
    if op not in ("add", "delete"):
        raise ResearchMemoryError("edge operation.op must be add or delete")
    edge = normalize_edge(operation, include_note=(op == "add"))
    key = (edge["source_slug"], edge["relation"], edge["target_slug"])
    if op == "add":
        try:
            connection.execute(
                "INSERT INTO edge (source_slug, relation, target_slug, note_md) VALUES (?, ?, ?, ?)",
                (*key, edge["note_md"]),
            )
        except sqlite3.IntegrityError as error:
            raise ResearchMemoryError(f"cannot add edge {key!r}: {error}")
    else:
        cursor = connection.execute(
            "DELETE FROM edge WHERE source_slug = ? AND relation = ? AND target_slug = ?",
            key,
        )
        if cursor.rowcount != 1:
            raise ResearchMemoryError(f"edge does not exist: {key!r}")
    return {
        "source_slug": edge["source_slug"],
        "relation": edge["relation"],
        "target_slug": edge["target_slug"],
    }


def canonical_item_digest(item: Mapping[str, Any]) -> str:
    return json_digest(
        {
            name: item[name]
            for name in (
                "canonical_key",
                "kind",
                "title",
                "anchor",
                "indexed_section_sha256",
                "fingerprint_version",
            )
        }
    )


def section_snapshot(document: Any, key: str) -> dict[str, Any]:
    section = section_for_key(document, key)
    return {
        "anchor": anchor_for_key(section, key),
        "indexed_section_sha256": require_digest(
            section.section_sha256, f"canonical section {key!r} fingerprint"
        ),
        "fingerprint_version": require_revision(
            section.fingerprint_version,
            f"canonical section {key!r} fingerprint version",
            1,
        ),
    }


def apply_canonical_item_operation(
    connection: sqlite3.Connection, raw: Any, timestamp: str, document: Any
) -> str:
    operation = require_mapping(raw, "canonical item operation")
    op = require_text(operation.get("op"), "canonical item operation.op")
    key = require_semantic_key(
        operation.get("canonical_key"), "canonical item operation.canonical_key"
    )

    if op == "add":
        require_keys(
            operation,
            ("op", "canonical_key", "kind", "title"),
            "canonical item add operation",
        )
        if connection.execute(
            "SELECT 1 FROM canonical_alias WHERE alias = ?", (key,)
        ).fetchone():
            raise ResearchMemoryError(
                f"cannot add canonical item {key!r}: key is already an alias"
            )
        item = {
            "canonical_key": key,
            "kind": require_text(operation.get("kind"), "canonical item operation.kind"),
            "title": require_text(
                operation.get("title"), "canonical item operation.title"
            ),
            **section_snapshot(document, key),
        }
        try:
            connection.execute(
                """
                INSERT INTO canonical_item (
                    canonical_key, kind, title, anchor, indexed_section_sha256,
                    fingerprint_version, revision, content_sha256, created_at,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, ?)
                """,
                (
                    item["canonical_key"],
                    item["kind"],
                    item["title"],
                    item["anchor"],
                    item["indexed_section_sha256"],
                    item["fingerprint_version"],
                    canonical_item_digest(item),
                    timestamp,
                    timestamp,
                ),
            )
        except sqlite3.IntegrityError as error:
            raise ResearchMemoryError(f"cannot add canonical item {key!r}: {error}")
        return key

    if op == "update":
        require_keys(
            operation,
            ("op", "canonical_key", "expected_revision", "changes"),
            "canonical item update operation",
        )
        expected = require_revision(
            operation.get("expected_revision"),
            "canonical item operation.expected_revision",
            1,
        )
        changes = require_mapping(
            operation.get("changes"), "canonical item operation.changes"
        )
        require_keys(
            changes,
            CANONICAL_ITEM_MUTABLE_FIELDS,
            "canonical item operation.changes",
        )
        if not changes:
            raise ResearchMemoryError(
                "canonical item operation.changes must not be empty"
            )
        row = connection.execute(
            "SELECT * FROM canonical_item WHERE canonical_key = ?", (key,)
        ).fetchone()
        if row is None:
            raise ResearchMemoryError(f"canonical item does not exist: {key}")
        if row["revision"] != expected:
            raise ResearchMemoryError(
                f"canonical item {key!r} revision conflict: expected {expected}, "
                f"found {row['revision']}"
            )
        item = dict(row)
        for name, value in changes.items():
            item[name] = require_text(value, f"canonical item changes.{name}")
        cursor = connection.execute(
            """
            UPDATE canonical_item
            SET kind = ?, title = ?, revision = revision + 1,
                content_sha256 = ?, updated_at = ?
            WHERE canonical_key = ? AND revision = ?
            """,
            (
                item["kind"],
                item["title"],
                canonical_item_digest(item),
                timestamp,
                key,
                expected,
            ),
        )
        if cursor.rowcount != 1:
            raise ResearchMemoryError(f"canonical item {key!r} changed during update")
        return key

    if op == "refresh":
        require_keys(
            operation,
            ("op", "canonical_key", "expected_revision"),
            "canonical item refresh operation",
        )
        expected = require_revision(
            operation.get("expected_revision"),
            "canonical item operation.expected_revision",
            1,
        )
        row = connection.execute(
            "SELECT * FROM canonical_item WHERE canonical_key = ?", (key,)
        ).fetchone()
        if row is None:
            raise ResearchMemoryError(f"canonical item does not exist: {key}")
        if row["revision"] != expected:
            raise ResearchMemoryError(
                f"canonical item {key!r} revision conflict: expected {expected}, "
                f"found {row['revision']}"
            )
        item = {**dict(row), **section_snapshot(document, key)}
        cursor = connection.execute(
            """
            UPDATE canonical_item
            SET anchor = ?, indexed_section_sha256 = ?, fingerprint_version = ?,
                revision = revision + 1, content_sha256 = ?, updated_at = ?
            WHERE canonical_key = ? AND revision = ?
            """,
            (
                item["anchor"],
                item["indexed_section_sha256"],
                item["fingerprint_version"],
                canonical_item_digest(item),
                timestamp,
                key,
                expected,
            ),
        )
        if cursor.rowcount != 1:
            raise ResearchMemoryError(f"canonical item {key!r} changed during refresh")
        return key

    if op == "delete":
        require_keys(
            operation,
            ("op", "canonical_key", "expected_revision"),
            "canonical item delete operation",
        )
        expected = require_revision(
            operation.get("expected_revision"),
            "canonical item operation.expected_revision",
            1,
        )
        cursor = connection.execute(
            "DELETE FROM canonical_item WHERE canonical_key = ? AND revision = ?",
            (key, expected),
        )
        if cursor.rowcount != 1:
            row = connection.execute(
                "SELECT revision FROM canonical_item WHERE canonical_key = ?", (key,)
            ).fetchone()
            if row is None:
                raise ResearchMemoryError(f"canonical item does not exist: {key}")
            raise ResearchMemoryError(
                f"canonical item {key!r} revision conflict: expected {expected}, "
                f"found {row['revision']}"
            )
        return key

    raise ResearchMemoryError(
        "canonical item operation.op must be add, update, refresh, or delete"
    )


def apply_canonical_alias_operation(
    connection: sqlite3.Connection, raw: Any
) -> dict[str, str]:
    operation = require_mapping(raw, "canonical alias operation")
    op = require_text(operation.get("op"), "canonical alias operation.op")
    alias = require_text(operation.get("alias"), "canonical alias operation.alias")
    key = require_semantic_key(
        operation.get("canonical_key"), "canonical alias operation.canonical_key"
    )
    if op == "add":
        require_keys(
            operation,
            ("op", "alias", "canonical_key", "source_locator"),
            "canonical alias add operation",
        )
        if alias == key or connection.execute(
            "SELECT 1 FROM canonical_item WHERE canonical_key = ?", (alias,)
        ).fetchone():
            raise ResearchMemoryError(
                f"cannot add canonical alias {alias!r}: it is a primary canonical key"
            )
        source_locator = optional_text(
            operation.get("source_locator"), "canonical alias operation.source_locator"
        )
        try:
            connection.execute(
                """
                INSERT INTO canonical_alias (alias, canonical_key, source_locator)
                VALUES (?, ?, ?)
                """,
                (alias, key, source_locator),
            )
        except sqlite3.IntegrityError as error:
            raise ResearchMemoryError(f"cannot add canonical alias {alias!r}: {error}")
    elif op == "delete":
        require_keys(
            operation,
            ("op", "alias", "canonical_key"),
            "canonical alias delete operation",
        )
        cursor = connection.execute(
            "DELETE FROM canonical_alias WHERE alias = ? AND canonical_key = ?",
            (alias, key),
        )
        if cursor.rowcount != 1:
            raise ResearchMemoryError(
                f"canonical alias does not exist: {(alias, key)!r}"
            )
    else:
        raise ResearchMemoryError("canonical alias operation.op must be add or delete")
    return {"alias": alias, "canonical_key": key}


def normalize_card_canonical_link(
    raw: Mapping[str, Any], *, include_note: bool
) -> dict[str, Any]:
    allowed = (
        "op",
        "card_slug",
        "canonical_key",
        "relation",
        "expected_revision",
    )
    if include_note:
        allowed += ("note_md",)
    require_keys(raw, allowed, "card canonical link operation")
    relation = require_text(
        raw.get("relation"), "card canonical link operation.relation"
    )
    if relation not in CANONICAL_RELATIONS:
        raise ResearchMemoryError(
            "card canonical link relation must be one of: "
            + ", ".join(CANONICAL_RELATIONS)
        )
    card_slug = require_text(
        raw.get("card_slug"), "card canonical link operation.card_slug"
    )
    canonical_key = require_semantic_key(
        raw.get("canonical_key"),
        "card canonical link operation.canonical_key",
    )
    if relation == "same-subject" and card_slug != canonical_key:
        raise ResearchMemoryError(
            "same-subject links require card_slug to equal canonical_key"
        )
    return {
        "card_slug": card_slug,
        "canonical_key": canonical_key,
        "relation": relation,
        "note_md": (
            optional_text(raw.get("note_md"), "card canonical link operation.note_md")
            if include_note
            else None
        ),
    }


def apply_card_canonical_link_operation(
    connection: sqlite3.Connection,
    raw: Any,
    timestamp: str,
    document: Any,
    canonical_digest: str,
) -> dict[str, str]:
    operation = require_mapping(raw, "card canonical link operation")
    op = require_text(operation.get("op"), "card canonical link operation.op")
    if op not in ("add", "review", "delete"):
        raise ResearchMemoryError(
            "card canonical link operation.op must be add, review, or delete"
        )
    include_note = op in ("add", "review") and "note_md" in operation
    allowed = ["op", "card_slug", "canonical_key", "relation"]
    if op in ("review", "delete"):
        allowed.append("expected_revision")
    if include_note:
        allowed.append("note_md")
    require_keys(operation, allowed, "card canonical link operation")
    link = normalize_card_canonical_link(operation, include_note=include_note)
    key = (link["card_slug"], link["canonical_key"], link["relation"])

    if op == "delete":
        expected = require_revision(
            operation.get("expected_revision"),
            "card canonical link operation.expected_revision",
            1,
        )
        cursor = connection.execute(
            """
            DELETE FROM card_canonical_link
            WHERE card_slug = ? AND canonical_key = ? AND relation = ?
                  AND revision = ?
            """,
            (*key, expected),
        )
        if cursor.rowcount != 1:
            raise ResearchMemoryError(
                f"card canonical link does not exist at revision {expected}: {key!r}"
            )
        return {
            "card_slug": link["card_slug"],
            "canonical_key": link["canonical_key"],
            "relation": link["relation"],
        }

    card = connection.execute(
        "SELECT revision FROM card WHERE slug = ?", (link["card_slug"],)
    ).fetchone()
    if card is None:
        raise ResearchMemoryError(f"card does not exist: {link['card_slug']}")
    item = connection.execute(
        """
        SELECT indexed_section_sha256, fingerprint_version
        FROM canonical_item WHERE canonical_key = ?
        """,
        (link["canonical_key"],),
    ).fetchone()
    if item is None:
        raise ResearchMemoryError(
            f"canonical item does not exist: {link['canonical_key']}"
        )
    section = section_for_key(document, link["canonical_key"])
    section_digest = require_digest(
        section.section_sha256,
        f"canonical section {link['canonical_key']!r} fingerprint",
    )
    if (
        item["indexed_section_sha256"] != section_digest
        or item["fingerprint_version"] != section.fingerprint_version
    ):
        raise ResearchMemoryError(
            f"canonical item {link['canonical_key']!r} must be refreshed before linking"
        )

    if op == "add":
        try:
            connection.execute(
                """
                INSERT INTO card_canonical_link (
                    card_slug, canonical_key, relation, note_md,
                    reviewed_canonical_sha256, reviewed_section_sha256,
                    reviewed_card_revision, revision, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
                """,
                (
                    *key,
                    link["note_md"],
                    canonical_digest,
                    section_digest,
                    card["revision"],
                    timestamp,
                    timestamp,
                ),
            )
        except sqlite3.IntegrityError as error:
            raise ResearchMemoryError(
                f"cannot add card canonical link {key!r}: {error}"
            )
    else:
        expected = require_revision(
            operation.get("expected_revision"),
            "card canonical link operation.expected_revision",
            1,
        )
        existing = connection.execute(
            """
            SELECT note_md, revision FROM card_canonical_link
            WHERE card_slug = ? AND canonical_key = ? AND relation = ?
            """,
            key,
        ).fetchone()
        if existing is None:
            raise ResearchMemoryError(f"card canonical link does not exist: {key!r}")
        if existing["revision"] != expected:
            raise ResearchMemoryError(
                f"card canonical link {key!r} revision conflict: expected {expected}, "
                f"found {existing['revision']}"
            )
        note = link["note_md"] if include_note else existing["note_md"]
        cursor = connection.execute(
            """
            UPDATE card_canonical_link
            SET note_md = ?, reviewed_canonical_sha256 = ?,
                reviewed_section_sha256 = ?, reviewed_card_revision = ?,
                revision = revision + 1, updated_at = ?
            WHERE card_slug = ? AND canonical_key = ? AND relation = ?
                  AND revision = ?
            """,
            (
                note,
                canonical_digest,
                section_digest,
                card["revision"],
                timestamp,
                *key,
                expected,
            ),
        )
        if cursor.rowcount != 1:
            raise ResearchMemoryError(f"card canonical link {key!r} changed during review")

    return {
        "card_slug": link["card_slug"],
        "canonical_key": link["canonical_key"],
        "relation": link["relation"],
    }


def require_integrated_links(connection: sqlite3.Connection) -> None:
    missing = [
        row[0]
        for row in connection.execute(
            """
            SELECT card.slug
            FROM card
            WHERE disposition = 'integrated'
              AND NOT EXISTS (
                  SELECT 1 FROM card_canonical_link AS link
                  WHERE link.card_slug = card.slug
                    AND link.relation = 'integrated-at'
              )
            ORDER BY card.slug
            """
        )
    ]
    if missing:
        raise ResearchMemoryError(
            "integrated cards require an integrated-at canonical link: "
            + ", ".join(missing)
        )


def command_apply(args: argparse.Namespace) -> dict[str, Any]:
    db_path = Path(args.db).resolve()
    batch = validate_batch(load_batch(Path(args.input)))
    connection = connect_read_write(db_path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        meta = require_current_schema(connection)
        if meta["last_round_id"] == batch["round_id"]:
            if meta["last_batch_digest"] != batch["batch_digest"]:
                raise ResearchMemoryError(
                    f"round {batch['round_id']!r} was already applied with different content"
                )
            connection.rollback()
            return {
                "ok": True,
                "command": "apply",
                "database": str(db_path),
                "round_id": batch["round_id"],
                "database_revision": meta["database_revision"],
                "idempotent_retry": True,
                "changed_cards": [],
                "changed_origins": [],
                "changed_edges": [],
                "changed_canonical_items": [],
                "changed_canonical_aliases": [],
                "changed_card_canonical_links": [],
            }

        canonical = canonical_from_meta(db_path, meta)
        if not canonical.is_file():
            raise ResearchMemoryError(f"canonical document does not exist: {canonical}")
        actual_canonical_digest = sha256_file(canonical)
        if actual_canonical_digest != batch["canonical_digest"]:
            raise ResearchMemoryError(
                "canonical digest conflict: batch does not match the current canonical document"
            )

        expected_database_revision = batch["expected_database_revision"]
        if meta["database_revision"] != expected_database_revision:
            raise ResearchMemoryError(
                "database revision conflict: expected "
                f"{expected_database_revision}, found {meta['database_revision']}"
            )
        if meta["canonical_sha256"] != batch["expected_canonical_digest"]:
            raise ResearchMemoryError(
                "canonical baseline conflict: expected stored digest "
                f"{batch['expected_canonical_digest']}, found {meta['canonical_sha256']}"
            )

        document = scan_canonical_document(canonical)
        if document.canonical_sha256 != batch["canonical_digest"]:
            raise ResearchMemoryError(
                "canonical section index digest does not match the published document"
            )

        timestamp = utc_now()
        changed_cards = [
            apply_card_operation(connection, operation, timestamp)
            for operation in batch["card_operations"]
        ]
        changed_origins = [
            apply_origin_operation(connection, operation)
            for operation in batch["origin_operations"]
        ]
        changed_edges = [
            apply_edge_operation(connection, operation)
            for operation in batch["edge_operations"]
        ]
        changed_canonical_items = [
            apply_canonical_item_operation(connection, operation, timestamp, document)
            for operation in batch["canonical_item_operations"]
        ]
        changed_canonical_aliases = [
            apply_canonical_alias_operation(connection, operation)
            for operation in batch["canonical_alias_operations"]
        ]
        changed_card_canonical_links = [
            apply_card_canonical_link_operation(
                connection,
                operation,
                timestamp,
                document,
                batch["canonical_digest"],
            )
            for operation in batch["card_canonical_link_operations"]
        ]
        require_integrated_links(connection)
        if sha256_file(canonical) != batch["canonical_digest"]:
            raise ResearchMemoryError(
                "canonical document changed while the batch was being applied"
            )
        new_revision = expected_database_revision + 1
        connection.execute(
            """
            UPDATE meta
            SET canonical_sha256 = ?, database_revision = ?, last_round_id = ?,
                last_batch_digest = ?, updated_at = ?
            WHERE singleton = 1 AND database_revision = ?
            """,
            (
                batch["canonical_digest"],
                new_revision,
                batch["round_id"],
                batch["batch_digest"],
                timestamp,
                expected_database_revision,
            ),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return {
        "ok": True,
        "command": "apply",
        "database": str(db_path),
        "round_id": batch["round_id"],
        "database_revision": new_revision,
        "idempotent_retry": False,
        "changed_cards": changed_cards,
        "changed_origins": changed_origins,
        "changed_edges": changed_edges,
        "changed_canonical_items": changed_canonical_items,
        "changed_canonical_aliases": changed_canonical_aliases,
        "changed_card_canonical_links": changed_card_canonical_links,
    }


def flatten(values: Optional[Sequence[Sequence[str]]]) -> list[str]:
    return [item for group in (values or ()) for item in group]


def command_search(args: argparse.Namespace) -> dict[str, Any]:
    states = flatten(args.state) or ["active", "open", "parked"]
    invalid_states = sorted(set(states) - set(DISPOSITIONS))
    if invalid_states:
        raise ResearchMemoryError("invalid state(s): " + ", ".join(invalid_states))
    kinds = flatten(args.kind)
    for kind in kinds:
        require_text(kind, "kind")
    limit = require_revision(args.limit, "limit", 1)
    text_query = None if args.text is None else require_text(args.text, "text")

    cards: list[dict[str, Any]] = []
    for raw_path in args.db:
        db_path = Path(raw_path).resolve()
        connection = connect_read_only(db_path)
        try:
            meta = require_current_schema(connection)
            where = ["disposition IN (" + ",".join("?" for _ in states) + ")"]
            parameters: list[Any] = list(states)
            if kinds:
                where.append("kind IN (" + ",".join("?" for _ in kinds) + ")")
                parameters.extend(kinds)
            if text_query is not None:
                escaped = (
                    text_query.replace("\\", "\\\\")
                    .replace("%", "\\%")
                    .replace("_", "\\_")
                )
                where.append(
                    "(slug LIKE ? ESCAPE '\\' OR title LIKE ? ESCAPE '\\' "
                    "OR summary_md LIKE ? ESCAPE '\\')"
                )
                parameters.extend([f"%{escaped}%"] * 3)
            rows = connection.execute(
                f"""
                SELECT slug, kind, title, summary_md, disposition, claim_status,
                       reason, next_test, revival_condition, revision,
                       content_sha256, updated_at
                FROM card
                WHERE {' AND '.join(where)}
                ORDER BY CASE disposition
                    WHEN 'active' THEN 0 WHEN 'open' THEN 1 WHEN 'parked' THEN 2
                    WHEN 'rejected' THEN 3 ELSE 4 END,
                    updated_at DESC, slug
                LIMIT ?
                """,
                (*parameters, limit),
            ).fetchall()
            for row in rows:
                item = dict(row)
                item.update(
                    {
                        "theory": meta["theory_slug"],
                        "database": str(db_path),
                    }
                )
                cards.append(item)
        finally:
            connection.close()

    priority = {
        state: position
        for position, state in enumerate(
            ("active", "open", "parked", "rejected", "integrated")
        )
    }
    # Stable passes give disposition priority, then descending recency, then a
    # deterministic theory/slug tie-break without inverting text fields.
    cards.sort(key=lambda card: (card["theory"], card["slug"]))
    cards.sort(key=lambda card: str(card["updated_at"]), reverse=True)
    cards.sort(key=lambda card: priority[card["disposition"]])
    cards = cards[:limit]
    return {"ok": True, "command": "search", "count": len(cards), "cards": cards}


def section_metadata(document: Any, key: str) -> Optional[dict[str, Any]]:
    section = document.by_key.get(key)
    if section is None:
        return None
    return {
        "keys": list(section.keys),
        "title": section.title,
        "heading_level": section.level,
        "heading_line": section.heading_line,
        "start_line": section.start_line,
        "end_line": section.end_line,
        "anchor": anchor_for_key(section, key),
        "section_sha256": section.section_sha256,
        "fingerprint_version": section.fingerprint_version,
    }


def card_summary(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        name: row[name]
        for name in (
            *CARD_SUMMARY_FIELDS,
            "revision",
            "content_sha256",
            "updated_at",
        )
    }


def link_with_status(
    row: Mapping[str, Any], document: Any, current_digest: str, stored_digest: str
) -> dict[str, Any]:
    section = document.by_key.get(row["canonical_key"])
    return {
        name: row[name]
        for name in (
            "card_slug",
            "canonical_key",
            "relation",
            "note_md",
            "reviewed_canonical_sha256",
            "reviewed_section_sha256",
            "reviewed_card_revision",
            "revision",
        )
    } | {
        "status": {
            "canonical_key_present": section is not None,
            "database_document_match": stored_digest == current_digest,
            "canonical_item_section_match": (
                section is not None
                and row["indexed_section_sha256"] == section.section_sha256
                and row["fingerprint_version"] == section.fingerprint_version
            ),
            "reviewed_document_match": (
                row["reviewed_canonical_sha256"] == current_digest
            ),
            "reviewed_section_match": (
                section is not None
                and row["reviewed_section_sha256"] == section.section_sha256
            ),
            "reviewed_card_revision_match": (
                row["reviewed_card_revision"] == row["current_card_revision"]
            ),
        }
    }


def command_lookup(args: argparse.Namespace) -> dict[str, Any]:
    db_path = Path(args.db).resolve()
    require_no_sidecars(db_path)
    connection = connect_read_only(db_path)
    try:
        connection.execute("BEGIN")
        meta = require_current_schema(connection)
        canonical = canonical_from_meta(db_path, meta)
        if not canonical.is_file():
            raise ResearchMemoryError(f"canonical document does not exist: {canonical}")
        document = scan_canonical_document(canonical)
        current_digest = document.canonical_sha256
        canonical_status = (
            "current"
            if current_digest == meta["canonical_sha256"]
            else "requires_review"
        )

        matched_as: Optional[str] = None
        matched_value: str
        if args.canonical is not None:
            matched_value = require_text(args.canonical, "canonical lookup key")
            item = connection.execute(
                "SELECT * FROM canonical_item WHERE canonical_key = ?",
                (matched_value,),
            ).fetchone()
            if item is not None:
                canonical_keys = [item["canonical_key"]]
                matched_as = "canonical-key"
            else:
                alias = connection.execute(
                    "SELECT canonical_key FROM canonical_alias WHERE alias = ?",
                    (matched_value,),
                ).fetchone()
                if alias is None:
                    raise ResearchMemoryError(
                        f"canonical key or alias does not exist: {matched_value}"
                    )
                canonical_keys = [alias["canonical_key"]]
                matched_as = "alias"
            card_slugs: Optional[list[str]] = None
        else:
            matched_value = require_text(args.card, "card lookup slug")
            if connection.execute(
                "SELECT 1 FROM card WHERE slug = ?", (matched_value,)
            ).fetchone() is None:
                raise ResearchMemoryError(f"card does not exist: {matched_value}")
            canonical_keys = [
                row[0]
                for row in connection.execute(
                    """
                    SELECT DISTINCT canonical_key FROM card_canonical_link
                    WHERE card_slug = ? ORDER BY canonical_key
                    """,
                    (matched_value,),
                )
            ]
            card_slugs = [matched_value]
            matched_as = "card"

        items: list[dict[str, Any]] = []
        for key in canonical_keys:
            row = connection.execute(
                "SELECT * FROM canonical_item WHERE canonical_key = ?", (key,)
            ).fetchone()
            if row is None:
                continue
            aliases = [
                dict(alias)
                for alias in connection.execute(
                    """
                    SELECT alias, source_locator FROM canonical_alias
                    WHERE canonical_key = ? ORDER BY alias
                    """,
                    (key,),
                )
            ]
            item = dict(row)
            item["aliases"] = aliases
            item["section"] = section_metadata(document, key)
            item["section_match"] = (
                item["section"] is not None
                and row["indexed_section_sha256"]
                == item["section"]["section_sha256"]
                and row["fingerprint_version"]
                == item["section"]["fingerprint_version"]
            )
            items.append(item)

        placeholders = ",".join("?" for _ in canonical_keys)
        if args.canonical is not None:
            link_rows = (
                []
                if not canonical_keys
                else connection.execute(
                    f"""
                    SELECT link.*, item.indexed_section_sha256,
                           item.fingerprint_version,
                           card.revision AS current_card_revision
                    FROM card_canonical_link AS link
                    JOIN canonical_item AS item
                      ON item.canonical_key = link.canonical_key
                    JOIN card ON card.slug = link.card_slug
                    WHERE link.canonical_key IN ({placeholders})
                    ORDER BY link.card_slug, link.canonical_key, link.relation
                    """,
                    canonical_keys,
                ).fetchall()
            )
            card_slugs = sorted({row["card_slug"] for row in link_rows})
        else:
            link_rows = connection.execute(
                """
                SELECT link.*, item.indexed_section_sha256,
                       item.fingerprint_version,
                       card.revision AS current_card_revision
                FROM card_canonical_link AS link
                JOIN canonical_item AS item
                  ON item.canonical_key = link.canonical_key
                JOIN card ON card.slug = link.card_slug
                WHERE link.card_slug = ?
                ORDER BY link.canonical_key, link.relation
                """,
                (matched_value,),
            ).fetchall()
        links = [
            link_with_status(
                row, document, current_digest, meta["canonical_sha256"]
            )
            for row in link_rows
        ]
        cards = [
            card_summary(row)
            for slug in card_slugs or []
            for row in [
                connection.execute("SELECT * FROM card WHERE slug = ?", (slug,)).fetchone()
            ]
            if row is not None
        ]
    finally:
        connection.rollback()
        connection.close()
    return {
        "ok": True,
        "command": "lookup",
        "database": str(db_path),
        "theory": meta["theory_slug"],
        "query": {"value": matched_value, "matched_as": matched_as},
        "canonical_status": canonical_status,
        "canonical_items": items,
        "cards": cards,
        "links": links,
    }


def command_show(args: argparse.Namespace) -> dict[str, Any]:
    db_path = Path(args.db).resolve()
    slug = require_text(args.slug, "slug")
    connection = connect_read_only(db_path)
    try:
        connection.execute("BEGIN")
        meta = require_current_schema(connection)
        row = select_card(connection, slug)
        if row is None:
            raise ResearchMemoryError(f"card does not exist: {slug}")
        origins = [
            dict(origin)
            for origin in connection.execute(
                """
                SELECT card_slug, source_locator, source_slug, source_digest,
                       applicability_md
                FROM card_origin WHERE card_slug = ?
                ORDER BY source_locator, source_slug, source_digest
                """,
                (slug,),
            )
        ]
        outgoing = [
            dict(edge)
            for edge in connection.execute(
                """
                SELECT source_slug, relation, target_slug, note_md
                FROM edge WHERE source_slug = ?
                ORDER BY relation, target_slug
                """,
                (slug,),
            )
        ]
        incoming = [
            dict(edge)
            for edge in connection.execute(
                """
                SELECT source_slug, relation, target_slug, note_md
                FROM edge WHERE target_slug = ?
                ORDER BY relation, source_slug
                """,
                (slug,),
            )
        ]
        canonical_links = [
            dict(link)
            for link in connection.execute(
                """
                SELECT link.*, item.title AS canonical_title,
                       item.anchor AS canonical_anchor
                FROM card_canonical_link AS link
                JOIN canonical_item AS item
                  ON item.canonical_key = link.canonical_key
                WHERE link.card_slug = ?
                ORDER BY link.canonical_key, link.relation
                """,
                (slug,),
            )
        ]
        card = dict(row)
    finally:
        connection.rollback()
        connection.close()
    return {
        "ok": True,
        "command": "show",
        "database": str(db_path),
        "theory": meta["theory_slug"],
        "card": card,
        "origins": origins,
        "outgoing_edges": outgoing,
        "incoming_edges": incoming,
        "canonical_links": canonical_links,
    }


def check_card_row(row: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        card = normalize_card(row_as_card(row))
        expected_digest = card_digest(card)
        if row["content_sha256"] != expected_digest:
            errors.append(f"card {row['slug']!r} has a stale content digest")
        require_revision(row["revision"], f"card {row['slug']!r} revision", 1)
        require_text(row["created_at"], f"card {row['slug']!r} created_at")
        require_text(row["updated_at"], f"card {row['slug']!r} updated_at")
    except ResearchMemoryError as error:
        errors.append(str(error))
    return errors


def check_canonical_item_row(row: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        require_semantic_key(row["canonical_key"])
        require_text(row["kind"], f"canonical item {row['canonical_key']!r} kind")
        require_text(row["title"], f"canonical item {row['canonical_key']!r} title")
        require_text(row["anchor"], f"canonical item {row['canonical_key']!r} anchor")
        require_digest(
            row["indexed_section_sha256"],
            f"canonical item {row['canonical_key']!r} section fingerprint",
        )
        require_revision(
            row["fingerprint_version"],
            f"canonical item {row['canonical_key']!r} fingerprint version",
            1,
        )
        require_revision(
            row["revision"], f"canonical item {row['canonical_key']!r} revision", 1
        )
        require_text(
            row["created_at"], f"canonical item {row['canonical_key']!r} created_at"
        )
        require_text(
            row["updated_at"], f"canonical item {row['canonical_key']!r} updated_at"
        )
        if row["content_sha256"] != canonical_item_digest(row):
            errors.append(
                f"canonical item {row['canonical_key']!r} has a stale content digest"
            )
    except ResearchMemoryError as error:
        errors.append(str(error))
    return errors


def check_crosswalk_rows(connection: sqlite3.Connection) -> list[str]:
    errors: list[str] = []
    for row in connection.execute("SELECT * FROM canonical_item ORDER BY canonical_key"):
        errors.extend(check_canonical_item_row(row))
    for row in connection.execute(
        "SELECT alias, canonical_key, source_locator FROM canonical_alias ORDER BY alias"
    ):
        try:
            require_text(row["alias"], "canonical alias")
            require_semantic_key(row["canonical_key"])
            optional_text(row["source_locator"], "canonical alias source_locator")
            if connection.execute(
                "SELECT 1 FROM canonical_item WHERE canonical_key = ?", (row["alias"],)
            ).fetchone():
                errors.append(
                    f"canonical alias {row['alias']!r} collides with a primary key"
                )
        except ResearchMemoryError as error:
            errors.append(str(error))
    for row in connection.execute(
        "SELECT * FROM card_canonical_link ORDER BY card_slug, canonical_key, relation"
    ):
        try:
            require_text(row["card_slug"], "card canonical link card_slug")
            require_semantic_key(row["canonical_key"])
            if row["relation"] not in CANONICAL_RELATIONS:
                errors.append(
                    f"invalid card canonical link relation: {row['relation']!r}"
                )
            if (
                row["relation"] == "same-subject"
                and row["card_slug"] != row["canonical_key"]
            ):
                errors.append(
                    "same-subject card canonical link has unequal card slug and key: "
                    f"{row['card_slug']!r}, {row['canonical_key']!r}"
                )
            optional_text(row["note_md"], "card canonical link note_md")
            require_digest(
                row["reviewed_canonical_sha256"],
                "card canonical link reviewed_canonical_sha256",
            )
            require_digest(
                row["reviewed_section_sha256"],
                "card canonical link reviewed_section_sha256",
            )
            require_revision(
                row["reviewed_card_revision"],
                "card canonical link reviewed_card_revision",
                1,
            )
            require_revision(row["revision"], "card canonical link revision", 1)
            require_text(row["created_at"], "card canonical link created_at")
            require_text(row["updated_at"], "card canonical link updated_at")
        except ResearchMemoryError as error:
            errors.append(str(error))
    try:
        require_integrated_links(connection)
    except ResearchMemoryError as error:
        errors.append(str(error))
    return errors


def crosswalk_freshness(
    connection: sqlite3.Connection,
    document: Any,
    current_digest: str,
    stored_digest: str,
) -> dict[str, Any]:
    stale_items: list[dict[str, Any]] = []
    item_count = 0
    for row in connection.execute(
        """
        SELECT canonical_key, indexed_section_sha256, fingerprint_version
        FROM canonical_item ORDER BY canonical_key
        """
    ):
        item_count += 1
        section = document.by_key.get(row["canonical_key"])
        key_present = section is not None
        section_match = (
            key_present
            and row["indexed_section_sha256"] == section.section_sha256
            and row["fingerprint_version"] == section.fingerprint_version
        )
        if not section_match:
            stale_items.append(
                {
                    "canonical_key": row["canonical_key"],
                    "canonical_key_present": key_present,
                    "canonical_item_section_match": section_match,
                }
            )

    stale_links: list[dict[str, Any]] = []
    link_count = 0
    for row in connection.execute(
        """
        SELECT link.*, item.indexed_section_sha256, item.fingerprint_version,
               card.revision AS current_card_revision
        FROM card_canonical_link AS link
        JOIN canonical_item AS item ON item.canonical_key = link.canonical_key
        JOIN card ON card.slug = link.card_slug
        ORDER BY link.card_slug, link.canonical_key, link.relation
        """
    ):
        link_count += 1
        payload = link_with_status(row, document, current_digest, stored_digest)
        if not all(payload["status"].values()):
            stale_links.append(payload)
    return {
        "canonical_item_count": item_count,
        "card_canonical_link_count": link_count,
        "stale_items": stale_items,
        "stale_links": stale_links,
    }


def validate_open_database(
    connection: sqlite3.Connection,
    db_path: Path,
    *,
    require_canonical: bool,
) -> dict[str, Any]:
    """Validate one transaction snapshot for commands that require a sound DB."""
    errors: list[str] = []
    warnings: list[str] = []
    meta = require_current_schema(connection)

    journal_mode = str(connection.execute("PRAGMA journal_mode").fetchone()[0]).lower()
    if journal_mode != "delete":
        errors.append(f"journal mode is {journal_mode!r}, expected 'delete'")
    quick_check = [row[0] for row in connection.execute("PRAGMA quick_check")]
    if quick_check != ["ok"]:
        errors.extend(f"quick_check: {message}" for message in quick_check)
    foreign_keys = [tuple(row) for row in connection.execute("PRAGMA foreign_key_check")]
    if foreign_keys:
        errors.extend(f"foreign_key_check: {row!r}" for row in foreign_keys)

    if connection.execute("SELECT count(*) FROM meta").fetchone()[0] != 1:
        errors.append("metadata table must contain exactly one row")
    try:
        require_text(meta["theory_slug"], "metadata theory_slug")
        require_text(meta["canonical_path"], "metadata canonical_path")
        require_digest(meta["canonical_sha256"], "metadata canonical_sha256")
        require_revision(meta["database_revision"], "metadata database_revision")
        require_text(meta["created_at"], "metadata created_at")
        require_text(meta["updated_at"], "metadata updated_at")
        if (meta["last_round_id"] is None) != (meta["last_batch_digest"] is None):
            errors.append(
                "metadata last_round_id and last_batch_digest must be supplied together"
            )
        elif meta["last_round_id"] is not None:
            require_text(meta["last_round_id"], "metadata last_round_id")
            require_digest(meta["last_batch_digest"], "metadata last_batch_digest")
    except ResearchMemoryError as error:
        errors.append(str(error))

    for row in connection.execute(
        """
        SELECT card.*, card_body.detail_md
        FROM card LEFT JOIN card_body ON card_body.card_slug = card.slug
        ORDER BY card.slug
        """
    ):
        errors.extend(check_card_row(row))
    for row in connection.execute(
        """
        SELECT card_slug, source_locator, source_slug, source_digest,
               applicability_md
        FROM card_origin
        ORDER BY card_slug, source_locator, source_slug, source_digest
        """
    ):
        try:
            require_text(row["card_slug"], "origin card_slug")
            require_text(row["source_locator"], "origin source_locator")
            require_text(row["source_slug"], "origin source_slug")
            require_digest(row["source_digest"], "origin source_digest")
            require_text(row["applicability_md"], "origin applicability_md")
        except ResearchMemoryError as error:
            errors.append(str(error))
    for row in connection.execute(
        "SELECT source_slug, relation, target_slug, note_md FROM edge"
    ):
        try:
            require_text(row["source_slug"], "edge source_slug")
            require_text(row["relation"], "edge relation")
            require_text(row["target_slug"], "edge target_slug")
            optional_text(row["note_md"], "edge note_md")
        except ResearchMemoryError as error:
            errors.append(str(error))
    errors.extend(check_crosswalk_rows(connection))

    canonical = canonical_from_meta(db_path, meta)
    canonical_status = "unchecked"
    canonical_document = None
    if require_canonical:
        if not canonical.is_file():
            errors.append(f"canonical document does not exist: {canonical}")
            canonical_status = "missing"
        else:
            try:
                canonical_document = scan_canonical_document(canonical)
                if canonical_document.canonical_sha256 == meta["canonical_sha256"]:
                    canonical_status = "current"
                else:
                    canonical_status = "requires_review"
                    warnings.append(
                        "canonical document changed since the database was consolidated; "
                        "crosswalk links require review"
                    )
            except ResearchMemoryError as error:
                errors.append(str(error))
                canonical_status = "invalid"

    sidecars = sqlite_sidecars(db_path)
    if sidecars:
        errors.append(
            "unsettled SQLite sidecar(s) present: "
            + ", ".join(str(sidecar) for sidecar in sidecars)
        )
    if errors:
        raise ResearchMemoryError("database validation failed: " + "; ".join(errors))
    return {
        "meta": meta,
        "canonical": canonical,
        "canonical_status": canonical_status,
        "canonical_document": canonical_document,
        "warnings": warnings,
    }


def command_check(args: argparse.Namespace) -> dict[str, Any]:
    db_path = Path(args.db).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    canonical_status = "unknown"
    freshness: Optional[dict[str, Any]] = None
    meta = None
    user_version = None
    connection = connect_read_only(db_path)
    try:
        connection.execute("BEGIN")
        user_version = connection.execute("PRAGMA user_version").fetchone()[0]
        if user_version != SCHEMA_VERSION:
            errors.append(
                f"user_version is {user_version}, expected {SCHEMA_VERSION}"
            )
        journal_mode = str(connection.execute("PRAGMA journal_mode").fetchone()[0]).lower()
        if journal_mode != "delete":
            errors.append(f"journal mode is {journal_mode!r}, expected 'delete'")
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
            )
        }
        missing_tables = sorted(set(REQUIRED_COLUMNS) - tables)
        if missing_tables:
            errors.append("missing required table(s): " + ", ".join(missing_tables))
        unexpected_tables = sorted(tables - set(REQUIRED_COLUMNS))
        if unexpected_tables:
            errors.append(
                f"unexpected schema-v{SCHEMA_VERSION} table(s): "
                + ", ".join(unexpected_tables)
            )
        errors.extend(schema_object_errors(connection))
        for table, required in REQUIRED_COLUMNS.items():
            if table not in tables:
                continue
            actual = {
                row[1] for row in connection.execute(f"PRAGMA table_info({table})")
            }
            missing_columns = sorted(required - actual)
            if missing_columns:
                errors.append(
                    f"table {table!r} is missing column(s): {', '.join(missing_columns)}"
                )
            unexpected_columns = sorted(actual - required)
            if unexpected_columns:
                errors.append(
                    f"table {table!r} has unexpected schema-v{SCHEMA_VERSION} column(s): "
                    + ", ".join(unexpected_columns)
                )
        expected_primary_keys = {
            "meta": [(1, "singleton")],
            "card": [(1, "slug")],
            "card_body": [(1, "card_slug")],
            "card_origin": [
                (1, "card_slug"),
                (2, "source_locator"),
                (3, "source_slug"),
                (4, "source_digest"),
            ],
            "edge": [(1, "source_slug"), (2, "relation"), (3, "target_slug")],
            "canonical_item": [(1, "canonical_key")],
            "canonical_alias": [(1, "alias")],
            "card_canonical_link": [
                (1, "card_slug"),
                (2, "canonical_key"),
                (3, "relation"),
            ],
        }
        for table, expected_primary_key in expected_primary_keys.items():
            if table not in tables:
                continue
            actual_primary_key = sorted(
                (row[5], row[1])
                for row in connection.execute(f"PRAGMA table_info({table})")
                if row[5]
            )
            if actual_primary_key != expected_primary_key:
                errors.append(f"table {table!r} has the wrong primary key")
        if "edge" in tables:
            edge_foreign_keys = {
                (row[3], row[2], row[4], str(row[6]).upper())
                for row in connection.execute("PRAGMA foreign_key_list(edge)")
            }
            expected_foreign_keys = {
                ("source_slug", "card", "slug", "CASCADE"),
                ("target_slug", "card", "slug", "CASCADE"),
            }
            missing_foreign_keys = expected_foreign_keys - edge_foreign_keys
            if missing_foreign_keys:
                errors.append(
                    "edge table is missing required cascading foreign key(s): "
                    + ", ".join(sorted(key[0] for key in missing_foreign_keys))
                )
        if "card_origin" in tables:
            origin_foreign_keys = {
                (row[3], row[2], row[4], str(row[6]).upper())
                for row in connection.execute("PRAGMA foreign_key_list(card_origin)")
            }
            expected_origin_foreign_key = {
                ("card_slug", "card", "slug", "CASCADE")
            }
            if not expected_origin_foreign_key.issubset(origin_foreign_keys):
                errors.append(
                    "card_origin table is missing its required cascading foreign key"
                )
        quick_check = [row[0] for row in connection.execute("PRAGMA quick_check")]
        if quick_check != ["ok"]:
            errors.extend(f"quick_check: {message}" for message in quick_check)
        foreign_keys = [tuple(row) for row in connection.execute("PRAGMA foreign_key_check")]
        if foreign_keys:
            errors.extend(f"foreign_key_check: {row!r}" for row in foreign_keys)

        meta = read_meta(connection)
        meta_count = connection.execute("SELECT count(*) FROM meta").fetchone()[0]
        if meta_count != 1:
            errors.append(f"metadata table has {meta_count} rows, expected exactly one")
        if meta["schema_version"] != SCHEMA_VERSION:
            errors.append(
                f"metadata schema version is {meta['schema_version']}, expected {SCHEMA_VERSION}"
            )
        require_text(meta["theory_slug"], "metadata theory_slug")
        require_text(meta["canonical_path"], "metadata canonical_path")
        require_digest(meta["canonical_sha256"], "metadata canonical_sha256")
        require_revision(meta["database_revision"], "metadata database_revision")
        require_text(meta["created_at"], "metadata created_at")
        require_text(meta["updated_at"], "metadata updated_at")
        if (meta["last_round_id"] is None) != (meta["last_batch_digest"] is None):
            errors.append(
                "metadata last_round_id and last_batch_digest must be supplied together"
            )
        elif meta["last_round_id"] is not None:
            require_text(meta["last_round_id"], "metadata last_round_id")
            require_digest(meta["last_batch_digest"], "metadata last_batch_digest")
        canonical = canonical_from_meta(db_path, meta)
        if not canonical.is_file():
            canonical_status = "missing"
            errors.append(f"canonical document does not exist: {canonical}")
        else:
            try:
                document = scan_canonical_document(canonical)
                current_digest = document.canonical_sha256
                if current_digest == meta["canonical_sha256"]:
                    canonical_status = "current"
                else:
                    canonical_status = "requires_review"
                    warnings.append(
                        "canonical document changed since the database was consolidated; "
                        "crosswalk links require review"
                    )
                freshness = crosswalk_freshness(
                    connection,
                    document,
                    current_digest,
                    meta["canonical_sha256"],
                )
                if freshness["stale_items"]:
                    warnings.append("canonical items require refresh")
                if freshness["stale_links"]:
                    warnings.append("card canonical links require review")
            except ResearchMemoryError as error:
                canonical_status = "invalid"
                errors.append(str(error))

        for row in connection.execute(
            """
            SELECT card.*, card_body.detail_md
            FROM card LEFT JOIN card_body ON card_body.card_slug = card.slug
            ORDER BY card.slug
            """
        ):
            errors.extend(check_card_row(row))
        for row in connection.execute(
            """
            SELECT card_slug, source_locator, source_slug, source_digest,
                   applicability_md
            FROM card_origin
            ORDER BY card_slug, source_locator, source_slug, source_digest
            """
        ):
            try:
                require_text(row["card_slug"], "origin card_slug")
                require_text(row["source_locator"], "origin source_locator")
                require_text(row["source_slug"], "origin source_slug")
                require_digest(row["source_digest"], "origin source_digest")
                require_text(row["applicability_md"], "origin applicability_md")
            except ResearchMemoryError as error:
                errors.append(str(error))
        for row in connection.execute(
            "SELECT source_slug, relation, target_slug, note_md FROM edge"
        ):
            try:
                require_text(row["source_slug"], "edge source_slug")
                require_text(row["relation"], "edge relation")
                require_text(row["target_slug"], "edge target_slug")
                optional_text(row["note_md"], "edge note_md")
            except ResearchMemoryError as error:
                errors.append(str(error))
        errors.extend(check_crosswalk_rows(connection))
    except (sqlite3.DatabaseError, ResearchMemoryError, KeyError, IndexError) as error:
        errors.append(f"database validation failed: {error}")
    finally:
        connection.rollback()
        connection.close()

    sidecars = sqlite_sidecars(db_path)
    if sidecars:
        errors.append(
            "unsettled SQLite sidecar(s) present: "
            + ", ".join(str(sidecar) for sidecar in sidecars)
        )

    return {
        "ok": not errors,
        "command": "check",
        "database": str(db_path),
        "schema_version": user_version,
        "theory": None if meta is None else meta["theory_slug"],
        "database_revision": None if meta is None else meta["database_revision"],
        "canonical_status": canonical_status,
        "crosswalk_status": freshness,
        "errors": errors,
        "warnings": warnings,
    }


def command_ensure(args: argparse.Namespace) -> dict[str, Any]:
    canonical = require_markdown_file(args.canonical)
    requested_db = Path(args.db) if args.db else default_database_path(canonical)
    if requested_db.is_symlink():
        raise ResearchMemoryError(
            f"database path must not be a symbolic link: {requested_db.absolute()}"
        )
    db_path = requested_db.resolve()
    explicit_theory = (
        None if args.theory is None else require_text(args.theory, "theory")
    )

    if not requested_db.exists():
        if args.require_existing:
            raise ResearchMemoryError(f"database does not exist: {db_path}")
        theory = explicit_theory or canonical.stem
        result = create_database(canonical, theory, db_path)
        result.update(
            {
                "command": "ensure",
                "created": True,
                "canonical_status": "current",
                "warnings": [],
            }
        )
        return result

    if not requested_db.is_file():
        raise ResearchMemoryError(f"database path is not a regular file: {db_path}")

    require_no_sidecars(db_path)
    connection = connect_read_only(db_path)
    try:
        connection.execute("BEGIN")
        validation = validate_open_database(
            connection, db_path, require_canonical=True
        )
        meta = validation["meta"]
        stored_canonical = validation["canonical"]
        stored_theory = require_text(meta["theory_slug"], "metadata theory_slug")
        database_revision = require_revision(
            meta["database_revision"], "metadata database_revision"
        )
        canonical_digest = require_digest(
            meta["canonical_sha256"], "metadata canonical_sha256"
        )
    finally:
        connection.rollback()
        connection.close()

    if stored_canonical != canonical:
        raise ResearchMemoryError(
            "database canonical identity conflict: requested "
            f"{canonical}, database names {stored_canonical}"
        )
    if explicit_theory is not None and stored_theory != explicit_theory:
        raise ResearchMemoryError(
            "database theory identity conflict: requested "
            f"{explicit_theory!r}, found {stored_theory!r}"
        )

    return {
        "ok": True,
        "command": "ensure",
        "created": False,
        "database": str(db_path),
        "canonical": str(canonical),
        "theory": stored_theory,
        "schema_version": SCHEMA_VERSION,
        "database_revision": database_revision,
        "canonical_digest": canonical_digest,
        "canonical_status": validation["canonical_status"],
        "warnings": validation["warnings"],
    }


def command_relink(args: argparse.Namespace) -> dict[str, Any]:
    requested_db = Path(args.db)
    if requested_db.is_symlink():
        raise ResearchMemoryError(
            f"database path must not be a symbolic link: {requested_db.absolute()}"
        )
    db_path = requested_db.resolve()
    require_no_sidecars(db_path)
    canonical = require_markdown_file(args.canonical, "new canonical document")
    canonical_document = scan_canonical_document(canonical)
    expected_canonical = Path(args.expected_canonical).resolve()
    if expected_canonical.suffix.lower() not in (".md", ".markdown"):
        raise ResearchMemoryError("expected canonical path must name a Markdown file")
    if expected_canonical == canonical:
        raise ResearchMemoryError("old and new canonical paths must be different")
    expected_revision = require_revision(
        args.expected_database_revision, "expected database revision"
    )

    connection = connect_read_write(db_path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        validation = validate_open_database(
            connection, db_path, require_canonical=False
        )
        meta = validation["meta"]
        current_canonical = validation["canonical"]
        current_revision = require_revision(
            meta["database_revision"], "metadata database_revision"
        )
        stored_digest = require_digest(
            meta["canonical_sha256"], "metadata canonical_sha256"
        )
        theory = require_text(meta["theory_slug"], "metadata theory_slug")
        current_canonical_digest = canonical_document.canonical_sha256

        if current_canonical == canonical:
            if current_revision == expected_revision:
                # Moving a pair together can leave the relative locator already
                # correct. There is nothing to repair and therefore no revision
                # to consume.
                new_revision = current_revision
                idempotent_retry = True
                changed = False
            elif current_revision == expected_revision + 1:
                new_revision = current_revision
                idempotent_retry = True
                changed = False
            else:
                raise ResearchMemoryError(
                    "database revision conflict: expected "
                    f"{expected_revision} (or {expected_revision + 1} for an "
                    f"immediate retry), found {current_revision}"
                )
        else:
            if current_canonical != expected_canonical:
                raise ResearchMemoryError(
                    "database canonical identity conflict: expected "
                    f"{expected_canonical}, found {current_canonical}"
                )
            if current_revision != expected_revision:
                raise ResearchMemoryError(
                    "database revision conflict: expected "
                    f"{expected_revision}, found {current_revision}"
                )
            relative = Path(os.path.relpath(canonical, db_path.parent)).as_posix()
            timestamp = utc_now()
            cursor = connection.execute(
                """
                UPDATE meta
                SET canonical_path = ?, database_revision = database_revision + 1,
                    updated_at = ?
                WHERE singleton = 1 AND database_revision = ?
                """,
                (relative, timestamp, expected_revision),
            )
            if cursor.rowcount != 1:
                raise ResearchMemoryError("database changed during relink")
            new_revision = expected_revision + 1
            idempotent_retry = False
            changed = True
        if sha256_file(canonical) != current_canonical_digest:
            raise ResearchMemoryError("canonical document changed during relink")
        if changed:
            connection.commit()
        else:
            connection.rollback()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    canonical_status = (
        "current" if current_canonical_digest == stored_digest else "requires_review"
    )
    warnings = []
    if canonical_status == "requires_review":
        warnings.append(
            "new canonical content differs from the last consolidated digest; "
            "card-canonical link review snapshots may require review"
        )
    return {
        "ok": True,
        "command": "relink",
        "database": str(db_path),
        "canonical": str(canonical),
        "theory": theory,
        "schema_version": SCHEMA_VERSION,
        "database_revision": new_revision,
        "canonical_status": canonical_status,
        "changed": changed,
        "idempotent_retry": idempotent_retry,
        "warnings": warnings,
    }


def command_export(args: argparse.Namespace) -> dict[str, Any]:
    db_path = Path(args.db).resolve()
    require_no_sidecars(db_path)
    connection = connect_read_only(db_path)
    try:
        connection.execute("BEGIN")
        validation = validate_open_database(
            connection, db_path, require_canonical=True
        )
        meta = dict(validation["meta"])
        cards = [
            dict(row)
            for row in connection.execute("SELECT * FROM card ORDER BY slug")
        ]
        card_bodies = [
            dict(row)
            for row in connection.execute(
                "SELECT card_slug, detail_md FROM card_body ORDER BY card_slug"
            )
        ]
        origins = [
            dict(row)
            for row in connection.execute(
                """
                SELECT card_slug, source_locator, source_slug, source_digest,
                       applicability_md
                FROM card_origin
                ORDER BY card_slug, source_locator, source_slug, source_digest
                """
            )
        ]
        edges = [
            dict(row)
            for row in connection.execute(
                """
                SELECT source_slug, relation, target_slug, note_md
                FROM edge ORDER BY source_slug, relation, target_slug
                """
            )
        ]
        canonical_items = [
            dict(row)
            for row in connection.execute(
                "SELECT * FROM canonical_item ORDER BY canonical_key"
            )
        ]
        canonical_aliases = [
            dict(row)
            for row in connection.execute(
                """
                SELECT alias, canonical_key, source_locator
                FROM canonical_alias ORDER BY alias
                """
            )
        ]
        card_canonical_links = [
            dict(row)
            for row in connection.execute(
                """
                SELECT * FROM card_canonical_link
                ORDER BY card_slug, canonical_key, relation
                """
            )
        ]
    finally:
        connection.rollback()
        connection.close()
    semantic_export = {
        "meta": meta,
        "cards": cards,
        "card_bodies": card_bodies,
        "origins": origins,
        "edges": edges,
        "canonical_items": canonical_items,
        "canonical_aliases": canonical_aliases,
        "card_canonical_links": card_canonical_links,
    }
    return {
        "ok": True,
        "command": "export",
        "database": str(db_path),
        "schema_version": SCHEMA_VERSION,
        "canonical_status": validation["canonical_status"],
        "warnings": validation["warnings"],
        "export_digest": json_digest(semantic_export),
        **semantic_export,
    }


def command_contract(_args: argparse.Namespace) -> dict[str, Any]:
    """Return the machine-readable schema-3 authoring contract without a database."""
    return {
        "ok": True,
        "command": "contract",
        "schema_version": SCHEMA_VERSION,
        "locator": {
            "yaml_key": "research_memory",
            "default_value": {
                "path": "./<stem>.research.sqlite",
                "schema": SCHEMA_VERSION,
                "optional_for_understanding": True,
            },
            "default_database_name": "<stem>.research.sqlite",
            "default_theory_slug": "<stem>",
            "stem_rule": "canonical filename with its final .md or .markdown suffix removed",
        },
        "statuses": {
            "disposition": list(DISPOSITIONS),
            "claim_status": {"values": list(CLAIM_STATUSES), "nullable": True},
        },
        "card": {
            "fields": list(CARD_FIELDS),
            "required_fields": list(REQUIRED_CARD_FIELDS),
            "optional_nullable_fields": sorted(OPTIONAL_CARD_FIELDS),
            "state_requirements": {
                state: list(fields)
                for state, fields in CARD_STATE_REQUIREMENTS.items()
            },
            "kind": "nonempty extensible string",
            "storage": {
                "summary_table": "card",
                "detail_table": "card_body",
                "search_reads_detail": False,
                "show_reads_one_detail": True,
            },
            "integrated_requirement": "at least one integrated-at canonical link",
        },
        "canonical_crosswalk": {
            "primary_key_format": "lowercase semantic kebab-case, optionally theory-qualified",
            "relations": list(CANONICAL_RELATIONS),
            "aliases_resolve_exactly": True,
            "lookup_returns_card_detail": False,
        },
        "apply_batch": {
            "fields": list(APPLY_BATCH_FIELDS),
            "digest_rule": {
                "algorithm": "sha256",
                "encoding": "utf-8",
                "exclude_top_level_fields": ["batch_digest"],
                "json": {
                    "ensure_ascii": False,
                    "sort_keys": True,
                    "separators": [",", ":"],
                },
            },
            "operations": {
                "card": {
                    "add": {
                        "op_value": "add",
                        "required_fields": ["op", "card"],
                        "card_fields": list(CARD_FIELDS),
                    },
                    "update": {
                        "op_value": "update",
                        "required_fields": [
                            "op",
                            "slug",
                            "expected_revision",
                            "changes",
                        ],
                        "allowed_change_fields": list(MUTABLE_CARD_FIELDS),
                        "changes_must_be_nonempty": True,
                    },
                    "delete": {
                        "op_value": "delete",
                        "required_fields": ["op", "slug", "expected_revision"],
                    },
                },
                "origin": {
                    "add": {
                        "op_value": "add",
                        "required_fields": ["op", *ORIGIN_FIELDS],
                    },
                    "delete": {
                        "op_value": "delete",
                        "required_fields": ["op", *ORIGIN_FIELDS[:4]],
                    },
                },
                "edge": {
                    "add": {
                        "op_value": "add",
                        "required_fields": [
                            "op",
                            "source_slug",
                            "relation",
                            "target_slug",
                        ],
                        "optional_fields": ["note_md"],
                    },
                    "delete": {
                        "op_value": "delete",
                        "required_fields": [
                            "op",
                            "source_slug",
                            "relation",
                            "target_slug",
                        ],
                    },
                    "relation": "nonempty extensible string",
                },
                "canonical_item": {
                    "add": {
                        "op_value": "add",
                        "required_fields": ["op", "canonical_key", "kind", "title"],
                    },
                    "update": {
                        "op_value": "update",
                        "required_fields": [
                            "op",
                            "canonical_key",
                            "expected_revision",
                            "changes",
                        ],
                        "allowed_change_fields": list(CANONICAL_ITEM_MUTABLE_FIELDS),
                    },
                    "refresh": {
                        "op_value": "refresh",
                        "required_fields": [
                            "op",
                            "canonical_key",
                            "expected_revision",
                        ],
                    },
                    "delete": {
                        "op_value": "delete",
                        "required_fields": [
                            "op",
                            "canonical_key",
                            "expected_revision",
                        ],
                    },
                    "section_metadata_is_parser_derived": True,
                },
                "canonical_alias": {
                    "add": {
                        "op_value": "add",
                        "required_fields": ["op", "alias", "canonical_key"],
                        "optional_fields": ["source_locator"],
                    },
                    "delete": {
                        "op_value": "delete",
                        "required_fields": ["op", "alias", "canonical_key"],
                    },
                },
                "card_canonical_link": {
                    "add": {
                        "op_value": "add",
                        "required_fields": [
                            "op",
                            "card_slug",
                            "canonical_key",
                            "relation",
                        ],
                        "optional_fields": ["note_md"],
                    },
                    "review": {
                        "op_value": "review",
                        "required_fields": [
                            "op",
                            "card_slug",
                            "canonical_key",
                            "relation",
                            "expected_revision",
                        ],
                        "optional_fields": ["note_md"],
                    },
                    "delete": {
                        "op_value": "delete",
                        "required_fields": [
                            "op",
                            "card_slug",
                            "canonical_key",
                            "relation",
                            "expected_revision",
                        ],
                    },
                    "relations": list(CANONICAL_RELATIONS),
                    "review_snapshots_are_tool_derived": True,
                },
            },
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = JSONArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="create an empty companion database")
    init_parser.add_argument("--canonical", required=True)
    init_parser.add_argument("--theory", required=True)
    init_parser.add_argument("--db")
    init_parser.set_defaults(handler=command_init)

    ensure_parser = subparsers.add_parser(
        "ensure", help="create or validate a canonical companion database"
    )
    ensure_parser.add_argument("--canonical", required=True)
    ensure_parser.add_argument("--theory")
    ensure_parser.add_argument("--db")
    ensure_parser.add_argument("--require-existing", action="store_true")
    ensure_parser.set_defaults(handler=command_ensure)

    relink_parser = subparsers.add_parser(
        "relink", help="repair canonical ownership metadata after a deliberate move"
    )
    relink_parser.add_argument("--db", required=True)
    relink_parser.add_argument("--canonical", required=True)
    relink_parser.add_argument("--expected-canonical", required=True)
    relink_parser.add_argument(
        "--expected-database-revision", required=True, type=int
    )
    relink_parser.set_defaults(handler=command_relink)

    apply_parser = subparsers.add_parser("apply", help="apply one revision-checked batch")
    apply_parser.add_argument("--db", required=True)
    apply_parser.add_argument("--input", required=True)
    apply_parser.set_defaults(handler=command_apply)

    search_parser = subparsers.add_parser("search", help="search card summaries read-only")
    search_parser.add_argument("--db", action="append", required=True)
    search_parser.add_argument("--text")
    search_parser.add_argument("--state", action="append", nargs="+")
    search_parser.add_argument("--kind", action="append", nargs="+")
    search_parser.add_argument("--limit", type=int, default=50)
    search_parser.set_defaults(handler=command_search)

    lookup_parser = subparsers.add_parser(
        "lookup", help="resolve one canonical key, alias, or card without card bodies"
    )
    lookup_parser.add_argument("--db", required=True)
    lookup_group = lookup_parser.add_mutually_exclusive_group(required=True)
    lookup_group.add_argument("--canonical")
    lookup_group.add_argument("--card")
    lookup_parser.set_defaults(handler=command_lookup)

    show_parser = subparsers.add_parser("show", help="show one card and adjacent edges")
    show_parser.add_argument("--db", required=True)
    show_parser.add_argument("--slug", required=True)
    show_parser.set_defaults(handler=command_show)

    export_parser = subparsers.add_parser(
        "export", help="export complete research memory read-only"
    )
    export_parser.add_argument("--db", required=True)
    export_parser.set_defaults(handler=command_export)

    contract_parser = subparsers.add_parser(
        "contract", help="print the schema-3 authoring contract"
    )
    contract_parser.set_defaults(handler=command_contract)

    check_parser = subparsers.add_parser("check", help="validate one companion database")
    check_parser.add_argument("--db", required=True)
    check_parser.set_defaults(handler=command_check)
    return parser


def emit(payload: Mapping[str, Any], stream: Any = sys.stdout) -> None:
    json.dump(payload, stream, ensure_ascii=False, sort_keys=True, indent=2)
    stream.write("\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        result = args.handler(args)
        emit(result)
        return 0 if result.get("ok", True) else 1
    except (
        ResearchMemoryError,
        sqlite3.DatabaseError,
        OSError,
        KeyError,
        IndexError,
    ) as error:
        emit({"ok": False, "error": str(error)}, sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
