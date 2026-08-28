#!/usr/bin/env python3
"""Store large mathematical working memory behind a small, bounded JSON API."""

from __future__ import annotations

import argparse
import ast
import functools
import hashlib
import json
import math
import re
import sqlite3
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Sequence

from canonical_sections import CanonicalDocument, CanonicalSectionsError, scan_canonical


SCHEMA_VERSION = 4
APPLICATION_ID = 0x4D415434  # MAT4
ARTIFACT_SCHEMA = 1
DEFAULT_LIMIT = 8
MAX_LIMIT = 25
MAX_OFFSET = 10_000
BODY_CHUNK = 16_000
MAX_SOURCE_BYTES = 2 * 1024 * 1024
MAX_METADATA_BYTES = 64 * 1024
MAX_METADATA_NODES = 50_000
MAX_METADATA_DEPTH = 12
MAX_JSON_OUTPUT_BYTES = 1024 * 1024
MAX_CHECK_ISSUES = 100
HASH_CHUNK_BYTES = 1024 * 1024

SLUG_RE = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")
DIGEST_RE = re.compile(r"[0-9a-f]{64}\Z")
FACET_TYPES = ("field", "subfield", "term", "identifier", "symbol")
DISPOSITIONS = ("open", "active", "parked", "rejected", "integrated")
CLAIM_STATUSES = ("proved", "refuted", "conjectural", "incomplete", "unresolved")
ARTIFACT_MODES = ("discover", "falsify", "certify", "replay")

SCHEMA_SQL = f"""
CREATE TABLE meta (
    singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
    canonical_sha256 TEXT NOT NULL CHECK (length(canonical_sha256) = 64),
    revision INTEGER NOT NULL CHECK (revision >= 0),
    last_round_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE card (
    slug TEXT PRIMARY KEY,
    kind TEXT NOT NULL,
    title TEXT NOT NULL,
    summary_md TEXT NOT NULL,
    disposition TEXT NOT NULL CHECK (disposition IN {DISPOSITIONS}),
    claim_status TEXT CHECK (claim_status IS NULL OR claim_status IN {CLAIM_STATUSES}),
    reason TEXT,
    next_test TEXT,
    revival_condition TEXT,
    revision INTEGER NOT NULL CHECK (revision >= 1),
    content_sha256 TEXT NOT NULL CHECK (length(content_sha256) = 64),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE card_body (
    card_slug TEXT PRIMARY KEY REFERENCES card(slug) ON DELETE CASCADE,
    detail_md TEXT NOT NULL
);

CREATE TABLE card_facet (
    card_slug TEXT NOT NULL REFERENCES card(slug) ON DELETE CASCADE,
    type TEXT NOT NULL CHECK (type IN {FACET_TYPES}),
    value TEXT NOT NULL,
    normalized_value TEXT NOT NULL,
    PRIMARY KEY (card_slug, type, normalized_value)
);

CREATE TABLE card_origin (
    card_slug TEXT NOT NULL REFERENCES card(slug) ON DELETE CASCADE,
    source_locator TEXT NOT NULL,
    source_slug TEXT NOT NULL,
    source_digest TEXT NOT NULL CHECK (length(source_digest) = 64),
    applicability_md TEXT NOT NULL,
    PRIMARY KEY (card_slug, source_locator, source_slug, source_digest)
);

CREATE TABLE card_edge (
    source_slug TEXT NOT NULL REFERENCES card(slug) ON DELETE CASCADE,
    relation TEXT NOT NULL,
    target_slug TEXT NOT NULL REFERENCES card(slug) ON DELETE CASCADE,
    note_md TEXT,
    PRIMARY KEY (source_slug, relation, target_slug)
);

CREATE TABLE card_key (
    card_slug TEXT NOT NULL REFERENCES card(slug) ON DELETE CASCADE,
    canonical_key TEXT NOT NULL,
    relation TEXT NOT NULL,
    note_md TEXT,
    reviewed_section_sha256 TEXT NOT NULL CHECK (length(reviewed_section_sha256) = 64),
    reviewed_card_revision INTEGER NOT NULL CHECK (reviewed_card_revision >= 1),
    revision INTEGER NOT NULL CHECK (revision >= 1),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (card_slug, canonical_key, relation)
);

CREATE TABLE artifact (
    slug TEXT PRIMARY KEY,
    kind TEXT NOT NULL,
    title TEXT NOT NULL,
    summary_md TEXT NOT NULL,
    source_path TEXT NOT NULL UNIQUE,
    source_sha256 TEXT NOT NULL CHECK (length(source_sha256) = 64),
    metadata_json TEXT NOT NULL,
    metadata_sha256 TEXT NOT NULL CHECK (length(metadata_sha256) = 64),
    revision INTEGER NOT NULL CHECK (revision >= 1),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE artifact_ref (
    artifact_slug TEXT NOT NULL REFERENCES artifact(slug) ON DELETE CASCADE,
    role TEXT NOT NULL,
    path TEXT NOT NULL,
    sha256 TEXT NOT NULL CHECK (length(sha256) = 64),
    size_bytes INTEGER NOT NULL CHECK (size_bytes >= 0),
    PRIMARY KEY (artifact_slug, role, path)
);

CREATE TABLE artifact_link (
    artifact_slug TEXT NOT NULL REFERENCES artifact(slug) ON DELETE CASCADE,
    target_type TEXT NOT NULL CHECK (target_type IN ('card', 'key')),
    target_key TEXT NOT NULL,
    relation TEXT NOT NULL,
    applicability_md TEXT,
    source TEXT NOT NULL CHECK (source IN ('metadata', 'curated')),
    PRIMARY KEY (artifact_slug, target_type, target_key, relation, source)
);

CREATE INDEX card_state_idx ON card(disposition, updated_at DESC);
CREATE INDEX card_facet_lookup_idx ON card_facet(type, normalized_value, card_slug);
CREATE INDEX card_origin_source_idx ON card_origin(source_locator, source_slug, source_digest);
CREATE INDEX card_edge_target_idx ON card_edge(target_slug, relation);
CREATE INDEX card_key_lookup_idx ON card_key(canonical_key, relation);
CREATE INDEX artifact_link_target_idx ON artifact_link(target_type, target_key, relation);

CREATE VIRTUAL TABLE summary_fts USING fts5(
    entity_type UNINDEXED,
    slug UNINDEXED,
    title,
    summary_md,
    terms,
    tokenize = 'unicode61'
);
"""


class ResearchMemoryError(Exception):
    """A deterministic validation, integrity, or optimistic-lock error."""


class JSONArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ResearchMemoryError(message)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_file(path: Path) -> tuple[str, int]:
    """Hash an arbitrary referenced file without loading it into memory."""
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while chunk := stream.read(HASH_CHUNK_BYTES):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def digest_json(value: Any) -> str:
    return digest_bytes(canonical_json(value).encode("utf-8"))


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise ResearchMemoryError(f"{label} must be an object with string keys")
    return value


def require_keys(value: Mapping[str, Any], allowed: Iterable[str], label: str) -> None:
    unknown = sorted(set(value) - set(allowed))
    if unknown:
        raise ResearchMemoryError(f"{label} has unknown field(s): {', '.join(unknown)}")


def require_text(value: Any, label: str, *, maximum: int = 200_000) -> str:
    if not isinstance(value, str):
        raise ResearchMemoryError(f"{label} must be a string")
    text = value.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        raise ResearchMemoryError(f"{label} must not be empty")
    if len(text) > maximum:
        raise ResearchMemoryError(f"{label} exceeds {maximum} characters")
    return text


def optional_text(value: Any, label: str, *, maximum: int = 200_000) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ResearchMemoryError(f"{label} must be a string or null")
    text = value.replace("\r\n", "\n").replace("\r", "\n").strip()
    if len(text) > maximum:
        raise ResearchMemoryError(f"{label} exceeds {maximum} characters")
    return text or None


def require_slug(value: Any, label: str = "slug") -> str:
    slug = require_text(value, label, maximum=120)
    if SLUG_RE.fullmatch(slug) is None:
        raise ResearchMemoryError(f"{label} must be lowercase kebab-case")
    return slug


def require_digest(value: Any, label: str) -> str:
    if not isinstance(value, str) or DIGEST_RE.fullmatch(value) is None:
        raise ResearchMemoryError(f"{label} must be a lowercase SHA-256 digest")
    return value


def require_revision(value: Any, label: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ResearchMemoryError(f"{label} must be an integer >= {minimum}")
    return value


def require_sequence(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ResearchMemoryError(f"{label} must be an array")
    return value


def normalize_relation(value: Any, label: str = "relation") -> str:
    return require_slug(value, label)


def normalize_facet_value(kind: str, value: Any, label: str) -> tuple[str, str]:
    text = " ".join(unicodedata.normalize("NFKC", require_text(value, label, maximum=240)).split())
    if kind == "identifier":
        if ":" not in text:
            raise ResearchMemoryError(
                f"{label} must be namespaced, for example 'msc2020:05C31'"
            )
        namespace, local = text.split(":", 1)
        normalized = f"{namespace.casefold()}:{local}"
        if re.fullmatch(r"[a-z][a-z0-9.-]*:[^\s:][^\s]*", normalized) is None:
            raise ResearchMemoryError(
                f"{label} must be namespaced, for example 'msc2020:05C31'"
            )
    elif kind == "symbol":
        normalized = text
    else:
        normalized = text.casefold()
    return text, normalized


def normalize_facets(value: Any, label: str = "card.facets") -> list[dict[str, str]]:
    raw = require_sequence(value, label)
    if len(raw) > 32:
        raise ResearchMemoryError(f"{label} may contain at most 32 facets")
    facets: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for index, item in enumerate(raw):
        facet = require_mapping(item, f"{label}[{index}]")
        require_keys(facet, ("type", "value"), f"{label}[{index}]")
        kind = require_text(facet.get("type"), f"{label}[{index}].type", maximum=20)
        if kind not in FACET_TYPES:
            raise ResearchMemoryError(
                f"{label}[{index}].type must be one of: {', '.join(FACET_TYPES)}"
            )
        text, normalized = normalize_facet_value(
            kind, facet.get("value"), f"{label}[{index}].value"
        )
        identity = (kind, normalized)
        if identity in seen:
            raise ResearchMemoryError(f"{label} contains duplicate {kind}={text!r}")
        seen.add(identity)
        facets.append({"type": kind, "value": text, "normalized_value": normalized})
    facets.sort(key=lambda facet: (facet["type"], facet["normalized_value"]))
    return facets


CARD_BASE_FIELDS = (
    "slug",
    "kind",
    "title",
    "summary_md",
    "detail_md",
    "disposition",
    "claim_status",
    "reason",
    "next_test",
    "revival_condition",
    "facets",
)
CARD_MUTABLE_FIELDS = tuple(field for field in CARD_BASE_FIELDS if field != "slug")


def normalize_card(value: Any, *, require_all: bool = True) -> dict[str, Any]:
    raw = require_mapping(value, "card")
    require_keys(raw, CARD_BASE_FIELDS, "card")
    required = ("slug", "kind", "title", "summary_md", "disposition")
    if require_all:
        missing = [field for field in required if field not in raw]
        if missing:
            raise ResearchMemoryError(f"card is missing field(s): {', '.join(missing)}")

    result: dict[str, Any] = {}
    if "slug" in raw:
        result["slug"] = require_slug(raw["slug"], "card.slug")
    if "kind" in raw:
        result["kind"] = require_slug(raw["kind"], "card.kind")
    if "title" in raw:
        result["title"] = require_text(raw["title"], "card.title", maximum=240)
    if "summary_md" in raw:
        result["summary_md"] = require_text(
            raw["summary_md"], "card.summary_md", maximum=2_000
        )
    if "detail_md" in raw:
        result["detail_md"] = optional_text(raw["detail_md"], "card.detail_md")
    if "disposition" in raw:
        disposition = require_text(raw["disposition"], "card.disposition", maximum=20)
        if disposition not in DISPOSITIONS:
            raise ResearchMemoryError(
                "card.disposition must be one of: " + ", ".join(DISPOSITIONS)
            )
        result["disposition"] = disposition
    if "claim_status" in raw:
        claim = optional_text(raw["claim_status"], "card.claim_status", maximum=20)
        if claim is not None and claim not in CLAIM_STATUSES:
            raise ResearchMemoryError(
                "card.claim_status must be null or one of: " + ", ".join(CLAIM_STATUSES)
            )
        result["claim_status"] = claim
    for field in ("reason", "next_test", "revival_condition"):
        if field in raw:
            result[field] = optional_text(raw[field], f"card.{field}", maximum=4_000)
    if "facets" in raw:
        result["facets"] = normalize_facets(raw["facets"])

    if require_all:
        for field in ("detail_md", "claim_status", "reason", "next_test", "revival_condition"):
            result.setdefault(field, None)
        result.setdefault("facets", [])
        _validate_card_state(result)
    return result


def _validate_card_state(card: Mapping[str, Any]) -> None:
    disposition = card["disposition"]
    needed = {
        "open": "next_test",
        "active": "next_test",
        "parked": "revival_condition",
        "rejected": "reason",
    }.get(disposition)
    if needed and not card.get(needed):
        raise ResearchMemoryError(f"{disposition} cards require card.{needed}")


def card_content(card: Mapping[str, Any]) -> dict[str, Any]:
    return {field: card.get(field) for field in CARD_BASE_FIELDS}


def repository_root(canonical: Path) -> Path:
    for candidate in (canonical.parent, *canonical.parents):
        if (candidate / ".git").exists():
            return candidate.resolve()
    return canonical.parent.resolve()


def safe_repository_file(root: Path, value: Any, label: str, *, python: bool = False) -> tuple[str, Path]:
    text = require_text(value, label, maximum=500)
    if "\\" in text:
        raise ResearchMemoryError(f"{label} must use repository-relative POSIX separators")
    relative = PurePosixPath(text)
    if relative.is_absolute() or not relative.parts or any(part in ("", ".", "..") for part in relative.parts):
        raise ResearchMemoryError(f"{label} must be a normalized repository-relative path")
    if python and relative.suffix != ".py":
        raise ResearchMemoryError(f"{label} must identify a .py file")
    candidate = root.joinpath(*relative.parts)
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ResearchMemoryError(f"{label} must not traverse a symlink: {text}")
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (FileNotFoundError, ValueError) as error:
        raise ResearchMemoryError(f"{label} is not a repository file: {text}") from error
    if not resolved.is_file():
        raise ResearchMemoryError(f"{label} must be a regular file: {text}")
    return relative.as_posix(), resolved


def _reject_duplicate_dict_keys(node: ast.AST) -> None:
    for child in ast.walk(node):
        if not isinstance(child, ast.Dict):
            continue
        seen: set[Any] = set()
        for key_node in child.keys:
            if key_node is None:
                raise ResearchMemoryError("RESEARCH_ARTIFACT must not use dictionary unpacking")
            try:
                key = ast.literal_eval(key_node)
                hash(key)
            except (ValueError, TypeError) as error:
                raise ResearchMemoryError("RESEARCH_ARTIFACT dictionary keys must be literals") from error
            if key in seen:
                raise ResearchMemoryError(f"RESEARCH_ARTIFACT has duplicate dictionary key {key!r}")
            seen.add(key)


def _validate_native(value: Any, label: str, *, depth: int = 0) -> None:
    if depth > MAX_METADATA_DEPTH:
        raise ResearchMemoryError(f"{label} exceeds maximum nesting depth")
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ResearchMemoryError(f"{label} must not contain NaN or infinity")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_native(item, f"{label}[{index}]", depth=depth + 1)
        return
    if isinstance(value, dict) and all(isinstance(key, str) for key in value):
        for key, item in value.items():
            _validate_native(item, f"{label}.{key}", depth=depth + 1)
        return
    raise ResearchMemoryError(
        f"{label} must contain only dict, list, string, number, bool, and None literals"
    )


ARTIFACT_FIELDS = {
    "schema",
    "slug",
    "kind",
    "mode",
    "title",
    "summary",
    "canonical_keys",
    "target_digest",
    "purpose",
    "scope",
    "encoded_target",
    "evidence_ceiling",
    "reproduce",
    "limitations",
    "references",
    "result",
}
REPRODUCE_FIELDS = {"argv", "runtime", "parameters", "seeds", "budget", "stopping_rule"}


def extract_artifact(root: Path, source_path: Any, document: CanonicalDocument) -> dict[str, Any]:
    relative, source = safe_repository_file(root, source_path, "artifact.source_path", python=True)
    size = source.stat().st_size
    if size > MAX_SOURCE_BYTES:
        raise ResearchMemoryError(
            f"artifact source exceeds {MAX_SOURCE_BYTES} bytes: {relative}"
        )
    source_bytes = source.read_bytes()
    try:
        tree = ast.parse(source_bytes.decode("utf-8"), filename=relative)
    except (SyntaxError, UnicodeDecodeError) as error:
        raise ResearchMemoryError(f"artifact source is not valid UTF-8 Python: {error}") from error
    if sum(1 for _ in ast.walk(tree)) > MAX_METADATA_NODES:
        raise ResearchMemoryError("artifact source AST is too large")
    assignments = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "RESEARCH_ARTIFACT" for target in node.targets)
    ]
    if len(assignments) != 1:
        raise ResearchMemoryError(
            "artifact source must contain exactly one top-level RESEARCH_ARTIFACT assignment"
        )
    assignment = assignments[0]
    if len(assignment.targets) != 1 or not isinstance(assignment.targets[0], ast.Name):
        raise ResearchMemoryError("RESEARCH_ARTIFACT must use a simple top-level assignment")
    if not isinstance(assignment.value, ast.Dict):
        raise ResearchMemoryError("RESEARCH_ARTIFACT must be a literal dict")
    _reject_duplicate_dict_keys(assignment.value)
    try:
        metadata = ast.literal_eval(assignment.value)
    except (ValueError, TypeError, MemoryError, RecursionError) as error:
        raise ResearchMemoryError("RESEARCH_ARTIFACT must be entirely literal") from error
    _validate_native(metadata, "RESEARCH_ARTIFACT")
    metadata = require_mapping(metadata, "RESEARCH_ARTIFACT")
    require_keys(metadata, ARTIFACT_FIELDS, "RESEARCH_ARTIFACT")
    required = {
        "schema",
        "slug",
        "kind",
        "mode",
        "title",
        "summary",
        "canonical_keys",
        "target_digest",
        "purpose",
        "scope",
        "encoded_target",
        "evidence_ceiling",
        "reproduce",
    }
    missing = sorted(required - set(metadata))
    if missing:
        raise ResearchMemoryError(
            "RESEARCH_ARTIFACT is missing field(s): " + ", ".join(missing)
        )
    if (
        isinstance(metadata["schema"], bool)
        or not isinstance(metadata["schema"], int)
        or metadata["schema"] != ARTIFACT_SCHEMA
    ):
        raise ResearchMemoryError(f"RESEARCH_ARTIFACT.schema must equal {ARTIFACT_SCHEMA}")

    mode = require_text(metadata["mode"], "RESEARCH_ARTIFACT.mode", maximum=20)
    if mode not in ARTIFACT_MODES:
        raise ResearchMemoryError(
            "RESEARCH_ARTIFACT.mode must be one of: " + ", ".join(ARTIFACT_MODES)
        )

    normalized: dict[str, Any] = {
        "schema": ARTIFACT_SCHEMA,
        "slug": require_slug(metadata["slug"], "RESEARCH_ARTIFACT.slug"),
        "kind": require_slug(metadata["kind"], "RESEARCH_ARTIFACT.kind"),
        "mode": mode,
        "title": require_text(metadata["title"], "RESEARCH_ARTIFACT.title", maximum=240),
        "summary": require_text(metadata["summary"], "RESEARCH_ARTIFACT.summary", maximum=2_000),
        "purpose": require_text(metadata["purpose"], "RESEARCH_ARTIFACT.purpose", maximum=4_000),
        "scope": require_text(metadata["scope"], "RESEARCH_ARTIFACT.scope", maximum=4_000),
        "target_digest": require_digest(
            metadata["target_digest"], "RESEARCH_ARTIFACT.target_digest"
        ),
        "encoded_target": require_text(
            metadata["encoded_target"], "RESEARCH_ARTIFACT.encoded_target", maximum=4_000
        ),
        "evidence_ceiling": require_text(
            metadata["evidence_ceiling"], "RESEARCH_ARTIFACT.evidence_ceiling", maximum=4_000
        ),
    }
    keys = [
        require_slug(key, f"RESEARCH_ARTIFACT.canonical_keys[{index}]")
        for index, key in enumerate(require_sequence(metadata["canonical_keys"], "RESEARCH_ARTIFACT.canonical_keys"))
    ]
    if len(keys) > 32 or len(keys) != len(set(keys)):
        raise ResearchMemoryError("RESEARCH_ARTIFACT.canonical_keys must be unique and contain at most 32 keys")
    unknown_keys = sorted(set(keys) - set(document.by_key))
    if unknown_keys:
        raise ResearchMemoryError(
            "RESEARCH_ARTIFACT references unknown canonical key(s): " + ", ".join(unknown_keys)
        )
    normalized["canonical_keys"] = keys

    reproduce = require_mapping(metadata["reproduce"], "RESEARCH_ARTIFACT.reproduce")
    require_keys(reproduce, REPRODUCE_FIELDS, "RESEARCH_ARTIFACT.reproduce")
    missing_reproduce = sorted(
        {"argv", "runtime", "budget", "stopping_rule"} - set(reproduce)
    )
    if missing_reproduce:
        raise ResearchMemoryError(
            "RESEARCH_ARTIFACT.reproduce is missing field(s): "
            + ", ".join(missing_reproduce)
        )
    argv = require_sequence(reproduce["argv"], "RESEARCH_ARTIFACT.reproduce.argv")
    if not argv or len(argv) > 64:
        raise ResearchMemoryError("RESEARCH_ARTIFACT.reproduce.argv must contain 1 to 64 arguments")
    normalized_reproduce: dict[str, Any] = {
        "argv": [
            require_text(item, f"RESEARCH_ARTIFACT.reproduce.argv[{index}]", maximum=1_000)
            for index, item in enumerate(argv)
        ],
        "runtime": require_text(reproduce["runtime"], "RESEARCH_ARTIFACT.reproduce.runtime", maximum=240),
    }
    if "parameters" in reproduce:
        normalized_reproduce["parameters"] = require_mapping(
            reproduce["parameters"], "RESEARCH_ARTIFACT.reproduce.parameters"
        )
    if "seeds" in reproduce:
        normalized_reproduce["seeds"] = require_sequence(
            reproduce["seeds"], "RESEARCH_ARTIFACT.reproduce.seeds"
        )
    budget = require_mapping(
        reproduce["budget"], "RESEARCH_ARTIFACT.reproduce.budget"
    )
    if not budget:
        raise ResearchMemoryError("RESEARCH_ARTIFACT.reproduce.budget must not be empty")
    normalized_reproduce["budget"] = budget
    normalized_reproduce["stopping_rule"] = require_text(
        reproduce["stopping_rule"],
        "RESEARCH_ARTIFACT.reproduce.stopping_rule",
        maximum=2_000,
    )
    normalized["reproduce"] = normalized_reproduce

    limitations = metadata.get("limitations", [])
    normalized["limitations"] = [
        require_text(item, f"RESEARCH_ARTIFACT.limitations[{index}]", maximum=2_000)
        for index, item in enumerate(require_sequence(limitations, "RESEARCH_ARTIFACT.limitations"))
    ]
    if len(normalized["limitations"]) > 32:
        raise ResearchMemoryError("RESEARCH_ARTIFACT.limitations may contain at most 32 items")
    if "result" in metadata:
        normalized["result"] = require_mapping(metadata["result"], "RESEARCH_ARTIFACT.result")

    references: list[dict[str, Any]] = []
    for index, item in enumerate(require_sequence(metadata.get("references", []), "RESEARCH_ARTIFACT.references")):
        reference = require_mapping(item, f"RESEARCH_ARTIFACT.references[{index}]")
        require_keys(reference, ("role", "path", "sha256"), f"RESEARCH_ARTIFACT.references[{index}]")
        role = require_slug(reference.get("role"), f"RESEARCH_ARTIFACT.references[{index}].role")
        ref_relative, ref_path = safe_repository_file(
            root, reference.get("path"), f"RESEARCH_ARTIFACT.references[{index}].path"
        )
        expected = require_digest(
            reference.get("sha256"), f"RESEARCH_ARTIFACT.references[{index}].sha256"
        )
        observed, size_bytes = digest_file(ref_path)
        if observed != expected:
            raise ResearchMemoryError(
                f"artifact reference digest mismatch for {ref_relative}: expected {expected}, observed {observed}"
            )
        references.append(
            {"role": role, "path": ref_relative, "sha256": observed, "size_bytes": size_bytes}
        )
    if len(references) > 128 or len({(ref["role"], ref["path"]) for ref in references}) != len(references):
        raise ResearchMemoryError("RESEARCH_ARTIFACT.references must be unique and contain at most 128 items")
    normalized["references"] = [
        {key: ref[key] for key in ("role", "path", "sha256")} for ref in references
    ]

    metadata_json = canonical_json(normalized)
    if len(metadata_json.encode("utf-8")) > MAX_METADATA_BYTES:
        raise ResearchMemoryError(f"RESEARCH_ARTIFACT metadata exceeds {MAX_METADATA_BYTES} bytes")
    return {
        "slug": normalized["slug"],
        "kind": normalized["kind"],
        "title": normalized["title"],
        "summary_md": normalized["summary"],
        "source_path": relative,
        "source_sha256": digest_bytes(source_bytes),
        "metadata": normalized,
        "metadata_json": metadata_json,
        "metadata_sha256": digest_bytes(metadata_json.encode("utf-8")),
        "references": references,
    }


def _normalized_sql(value: str) -> str:
    return " ".join(value.rstrip(";").split())


@functools.lru_cache(maxsize=1)
def expected_schema_objects() -> dict[tuple[str, str], str]:
    connection = sqlite3.connect(":memory:")
    try:
        connection.executescript(SCHEMA_SQL)
        return {
            (row[0], row[1]): _normalized_sql(row[2])
            for row in connection.execute(
                "SELECT type, name, sql FROM sqlite_master "
                "WHERE name NOT LIKE 'sqlite_%' AND sql IS NOT NULL"
            )
        }
    finally:
        connection.close()


def schema_errors(connection: sqlite3.Connection) -> list[str]:
    expected = expected_schema_objects()
    actual = {
        (row[0], row[1]): _normalized_sql(row[2])
        for row in connection.execute(
            "SELECT type, name, sql FROM sqlite_master "
            "WHERE name NOT LIKE 'sqlite_%' AND sql IS NOT NULL"
        )
    }
    errors: list[str] = []
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    changed = sorted(key for key in set(expected) & set(actual) if expected[key] != actual[key])
    if missing:
        errors.append("missing schema object(s): " + ", ".join(f"{kind} {name}" for kind, name in missing))
    if extra:
        errors.append("unexpected schema object(s): " + ", ".join(f"{kind} {name}" for kind, name in extra))
    if changed:
        errors.append("changed schema object(s): " + ", ".join(f"{kind} {name}" for kind, name in changed))
    return errors


def database_uri(path: Path, mode: str) -> str:
    return path.absolute().as_uri() + "?mode=" + mode


def _identity_errors(connection: sqlite3.Connection) -> list[str]:
    application_id = int(connection.execute("PRAGMA application_id").fetchone()[0])
    version = int(connection.execute("PRAGMA user_version").fetchone()[0])
    errors: list[str] = []
    if application_id != APPLICATION_ID:
        errors.append(
            f"unsupported SQLite application_id {application_id}; expected {APPLICATION_ID}"
        )
    if version != SCHEMA_VERSION:
        errors.append(f"unsupported schema version {version}; expected {SCHEMA_VERSION}")
    return errors


def connect_database(document: CanonicalDocument, *, writable: bool = False) -> sqlite3.Connection:
    path = document.memory_path
    if path.is_symlink() or not path.is_file():
        raise ResearchMemoryError(f"database must be a regular non-symlink file: {path}")
    mode = "rw" if writable else "ro"
    connection = sqlite3.connect(
        database_uri(path, mode), uri=True, isolation_level=None, timeout=5.0
    )
    try:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        if not writable:
            connection.execute("PRAGMA query_only=ON")
        errors = _identity_errors(connection)
        if not errors:
            errors.extend(schema_errors(connection))
        if errors:
            raise ResearchMemoryError("; ".join(errors))
        meta = connection.execute("SELECT * FROM meta WHERE singleton=1").fetchone()
        if meta is None:
            raise ResearchMemoryError("database meta row is missing")
        return connection
    except Exception:
        connection.close()
        raise


def create_database(document: CanonicalDocument) -> None:
    path = document.memory_path
    if path.exists() or path.is_symlink():
        raise ResearchMemoryError(f"refusing to replace existing database path: {path}")
    if not path.parent.is_dir():
        raise ResearchMemoryError(f"database parent directory does not exist: {path.parent}")
    connection: sqlite3.Connection | None = None
    created = False
    try:
        path.open("xb").close()
        created = True
        connection = sqlite3.connect(path)
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA journal_mode=DELETE")
        connection.executescript(SCHEMA_SQL)
        connection.execute(f"PRAGMA application_id={APPLICATION_ID}")
        connection.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
        now = utc_now()
        connection.execute(
            "INSERT INTO meta VALUES (1, ?, 0, NULL, ?, ?)",
            (document.canonical_sha256, now, now),
        )
        connection.commit()
    except Exception:
        if connection is not None:
            connection.close()
            connection = None
        if created and path.exists() and not path.is_symlink():
            path.unlink()
        raise
    finally:
        if connection is not None:
            connection.close()


def meta_row(connection: sqlite3.Connection) -> sqlite3.Row:
    row = connection.execute("SELECT * FROM meta WHERE singleton=1").fetchone()
    if row is None:
        raise ResearchMemoryError("database meta row is missing")
    return row


def card_summary(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: row[key]
        for key in (
            "slug",
            "kind",
            "title",
            "summary_md",
            "disposition",
            "claim_status",
            "revision",
            "content_sha256",
            "updated_at",
        )
    }


def artifact_summary(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: row[key]
        for key in (
            "slug",
            "kind",
            "title",
            "summary_md",
            "source_path",
            "source_sha256",
            "metadata_sha256",
            "revision",
            "updated_at",
        )
    }


def selected_card(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        **card_summary(row),
        "reason": row["reason"],
        "next_test": row["next_test"],
        "revival_condition": row["revival_condition"],
    }


def load_card(connection: sqlite3.Connection, slug: str) -> dict[str, Any]:
    row = connection.execute("SELECT * FROM card WHERE slug=?", (slug,)).fetchone()
    if row is None:
        raise ResearchMemoryError(f"card does not exist: {slug}")
    body = connection.execute(
        "SELECT detail_md FROM card_body WHERE card_slug=?", (slug,)
    ).fetchone()
    facets = [
        {"type": item["type"], "value": item["value"], "normalized_value": item["normalized_value"]}
        for item in connection.execute(
            "SELECT type, value, normalized_value FROM card_facet "
            "WHERE card_slug=? ORDER BY type, normalized_value",
            (slug,),
        )
    ]
    return {
        **{key: row[key] for key in CARD_BASE_FIELDS if key not in ("detail_md", "facets")},
        "detail_md": body["detail_md"] if body else None,
        "facets": facets,
    }


def refresh_card_search(connection: sqlite3.Connection, slug: str) -> None:
    connection.execute(
        "DELETE FROM summary_fts WHERE entity_type='card' AND slug=?", (slug,)
    )
    row = connection.execute(
        "SELECT slug, title, summary_md, kind FROM card WHERE slug=?", (slug,)
    ).fetchone()
    if row is None:
        return
    terms = " ".join(
        [row["kind"]]
        + [
            facet[0]
            for facet in connection.execute(
                "SELECT value FROM card_facet WHERE card_slug=? ORDER BY type, normalized_value",
                (slug,),
            )
        ]
    )
    connection.execute(
        "INSERT INTO summary_fts(entity_type,slug,title,summary_md,terms) VALUES ('card',?,?,?,?)",
        (slug, row["title"], row["summary_md"], terms),
    )


def refresh_artifact_search(connection: sqlite3.Connection, slug: str) -> None:
    connection.execute(
        "DELETE FROM summary_fts WHERE entity_type='artifact' AND slug=?", (slug,)
    )
    row = connection.execute(
        "SELECT slug, title, summary_md, kind, metadata_json FROM artifact WHERE slug=?",
        (slug,),
    ).fetchone()
    if row is None:
        return
    metadata = json.loads(row["metadata_json"])
    terms = " ".join([row["kind"], metadata["purpose"], metadata["scope"], *metadata["canonical_keys"]])
    connection.execute(
        "INSERT INTO summary_fts(entity_type,slug,title,summary_md,terms) VALUES ('artifact',?,?,?,?)",
        (slug, row["title"], row["summary_md"], terms),
    )


def _insert_card(connection: sqlite3.Connection, card: Mapping[str, Any], now: str) -> None:
    content_sha256 = digest_json(card_content(card))
    connection.execute(
        """INSERT INTO card(
            slug,kind,title,summary_md,disposition,claim_status,reason,next_test,
            revival_condition,revision,content_sha256,created_at,updated_at
        ) VALUES (?,?,?,?,?,?,?,?,?,1,?,?,?)""",
        (
            card["slug"], card["kind"], card["title"], card["summary_md"],
            card["disposition"], card["claim_status"], card["reason"], card["next_test"],
            card["revival_condition"], content_sha256, now, now,
        ),
    )
    if card["detail_md"] is not None:
        connection.execute(
            "INSERT INTO card_body(card_slug,detail_md) VALUES (?,?)",
            (card["slug"], card["detail_md"]),
        )
    connection.executemany(
        "INSERT INTO card_facet(card_slug,type,value,normalized_value) VALUES (?,?,?,?)",
        [
            (card["slug"], facet["type"], facet["value"], facet["normalized_value"])
            for facet in card["facets"]
        ],
    )
    refresh_card_search(connection, card["slug"])


def _replace_card(connection: sqlite3.Connection, card: Mapping[str, Any], revision: int, now: str) -> None:
    content_sha256 = digest_json(card_content(card))
    connection.execute(
        """UPDATE card SET kind=?,title=?,summary_md=?,disposition=?,claim_status=?,
           reason=?,next_test=?,revival_condition=?,revision=?,content_sha256=?,updated_at=?
           WHERE slug=?""",
        (
            card["kind"], card["title"], card["summary_md"], card["disposition"],
            card["claim_status"], card["reason"], card["next_test"], card["revival_condition"],
            revision, content_sha256, now, card["slug"],
        ),
    )
    connection.execute("DELETE FROM card_body WHERE card_slug=?", (card["slug"],))
    if card["detail_md"] is not None:
        connection.execute(
            "INSERT INTO card_body(card_slug,detail_md) VALUES (?,?)",
            (card["slug"], card["detail_md"]),
        )
    connection.execute("DELETE FROM card_facet WHERE card_slug=?", (card["slug"],))
    connection.executemany(
        "INSERT INTO card_facet(card_slug,type,value,normalized_value) VALUES (?,?,?,?)",
        [
            (card["slug"], facet["type"], facet["value"], facet["normalized_value"])
            for facet in card["facets"]
        ],
    )
    refresh_card_search(connection, card["slug"])


def _write_artifact(
    connection: sqlite3.Connection,
    artifact: Mapping[str, Any],
    document: CanonicalDocument,
    now: str,
    *,
    revision: int,
) -> None:
    slug = artifact["slug"]
    if revision == 1:
        connection.execute(
            """INSERT INTO artifact(
               slug,kind,title,summary_md,source_path,source_sha256,metadata_json,
               metadata_sha256,revision,created_at,updated_at
               ) VALUES (?,?,?,?,?,?,?,?,1,?,?)""",
            (
                slug, artifact["kind"], artifact["title"], artifact["summary_md"],
                artifact["source_path"], artifact["source_sha256"], artifact["metadata_json"],
                artifact["metadata_sha256"], now, now,
            ),
        )
    else:
        connection.execute(
            """UPDATE artifact SET kind=?,title=?,summary_md=?,source_path=?,source_sha256=?,
               metadata_json=?,metadata_sha256=?,revision=?,updated_at=? WHERE slug=?""",
            (
                artifact["kind"], artifact["title"], artifact["summary_md"], artifact["source_path"],
                artifact["source_sha256"], artifact["metadata_json"], artifact["metadata_sha256"],
                revision, now, slug,
            ),
        )
        connection.execute("DELETE FROM artifact_ref WHERE artifact_slug=?", (slug,))
        connection.execute(
            "DELETE FROM artifact_link WHERE artifact_slug=? AND source='metadata'", (slug,)
        )
    connection.executemany(
        "INSERT INTO artifact_ref(artifact_slug,role,path,sha256,size_bytes) VALUES (?,?,?,?,?)",
        [
            (slug, ref["role"], ref["path"], ref["sha256"], ref["size_bytes"])
            for ref in artifact["references"]
        ],
    )
    connection.executemany(
        """INSERT INTO artifact_link(
           artifact_slug,target_type,target_key,relation,applicability_md,source
           ) VALUES (?,'key',?,'addresses',NULL,'metadata')""",
        [(slug, key) for key in artifact["metadata"]["canonical_keys"]],
    )
    refresh_artifact_search(connection, slug)


def _operation(value: Any, label: str, allowed: Iterable[str]) -> tuple[dict[str, Any], str]:
    item = require_mapping(value, label)
    op = require_text(item.get("op"), f"{label}.op", maximum=20)
    if op not in allowed:
        raise ResearchMemoryError(f"{label}.op must be one of: {', '.join(allowed)}")
    return item, op


def apply_card_operations(
    connection: sqlite3.Connection, operations: Any, now: str
) -> int:
    count = 0
    touched: set[str] = set()
    for index, value in enumerate(require_sequence(operations, "changeset.cards")):
        label = f"changeset.cards[{index}]"
        item, op = _operation(value, label, ("add", "update", "delete"))
        if op == "add":
            require_keys(item, ("op", "card"), label)
            card = normalize_card(item.get("card"))
            slug = card["slug"]
            if slug in touched:
                raise ResearchMemoryError(f"changeset.cards repeats target {slug!r}")
            _insert_card(connection, card, now)
        else:
            allowed = ("op", "slug", "expected_revision", "set") if op == "update" else (
                "op", "slug", "expected_revision"
            )
            require_keys(item, allowed, label)
            slug = require_slug(item.get("slug"), f"{label}.slug")
            if slug in touched:
                raise ResearchMemoryError(f"changeset.cards repeats target {slug!r}")
            expected = require_revision(
                item.get("expected_revision"), f"{label}.expected_revision", minimum=1
            )
            row = connection.execute(
                "SELECT revision, content_sha256 FROM card WHERE slug=?", (slug,)
            ).fetchone()
            if row is None:
                raise ResearchMemoryError(f"card does not exist: {slug}")
            if row["revision"] != expected:
                raise ResearchMemoryError(
                    f"card {slug!r} revision conflict: expected {expected}, observed {row['revision']}"
                )
            if op == "delete":
                connection.execute(
                    "DELETE FROM summary_fts WHERE entity_type='card' AND slug=?", (slug,)
                )
                connection.execute("DELETE FROM card WHERE slug=?", (slug,))
            else:
                patch = require_mapping(item.get("set"), f"{label}.set")
                require_keys(patch, CARD_MUTABLE_FIELDS, f"{label}.set")
                if not patch:
                    raise ResearchMemoryError(f"{label}.set must not be empty")
                current = load_card(connection, slug)
                normalized_patch = normalize_card({**patch}, require_all=False)
                updated = {**current, **normalized_patch}
                _validate_card_state(updated)
                if digest_json(card_content(updated)) == row["content_sha256"]:
                    raise ResearchMemoryError(f"card {slug!r} update makes no change")
                _replace_card(connection, updated, expected + 1, now)
        touched.add(slug)
        count += 1
    return count


def apply_artifact_operations(
    connection: sqlite3.Connection,
    operations: Any,
    document: CanonicalDocument,
    root: Path,
    now: str,
) -> int:
    count = 0
    touched: set[str] = set()
    for index, value in enumerate(require_sequence(operations, "changeset.artifacts")):
        label = f"changeset.artifacts[{index}]"
        item, op = _operation(value, label, ("add", "update", "delete"))
        if op == "add":
            require_keys(item, ("op", "source_path"), label)
            artifact = extract_artifact(root, item.get("source_path"), document)
            slug = artifact["slug"]
            if slug in touched:
                raise ResearchMemoryError(f"changeset.artifacts repeats target {slug!r}")
            _write_artifact(connection, artifact, document, now, revision=1)
        else:
            allowed = ("op", "slug", "expected_revision", "source_path") if op == "update" else (
                "op", "slug", "expected_revision"
            )
            require_keys(item, allowed, label)
            slug = require_slug(item.get("slug"), f"{label}.slug")
            if slug in touched:
                raise ResearchMemoryError(f"changeset.artifacts repeats target {slug!r}")
            expected = require_revision(
                item.get("expected_revision"), f"{label}.expected_revision", minimum=1
            )
            row = connection.execute(
                "SELECT revision,source_path,source_sha256,metadata_sha256 FROM artifact WHERE slug=?",
                (slug,),
            ).fetchone()
            if row is None:
                raise ResearchMemoryError(f"artifact does not exist: {slug}")
            if row["revision"] != expected:
                raise ResearchMemoryError(
                    f"artifact {slug!r} revision conflict: expected {expected}, observed {row['revision']}"
                )
            if op == "delete":
                connection.execute(
                    "DELETE FROM summary_fts WHERE entity_type='artifact' AND slug=?", (slug,)
                )
                connection.execute("DELETE FROM artifact WHERE slug=?", (slug,))
            else:
                artifact = extract_artifact(root, item.get("source_path"), document)
                if artifact["slug"] != slug:
                    raise ResearchMemoryError(
                        f"artifact source declares slug {artifact['slug']!r}, expected {slug!r}"
                    )
                if (
                    artifact["source_path"] == row["source_path"]
                    and artifact["source_sha256"] == row["source_sha256"]
                    and artifact["metadata_sha256"] == row["metadata_sha256"]
                ):
                    raise ResearchMemoryError(f"artifact {slug!r} update makes no change")
                _write_artifact(connection, artifact, document, now, revision=expected + 1)
        touched.add(slug)
        count += 1
    return count


def apply_origin_operations(connection: sqlite3.Connection, operations: Any) -> int:
    count = 0
    for index, value in enumerate(require_sequence(operations, "changeset.origins")):
        label = f"changeset.origins[{index}]"
        item, op = _operation(value, label, ("add", "delete"))
        allowed = (
            "op", "card_slug", "source_locator", "source_slug", "source_digest", "applicability_md"
        )
        require_keys(item, allowed if op == "add" else allowed[:-1], label)
        slug = require_slug(item.get("card_slug"), f"{label}.card_slug")
        locator = require_text(item.get("source_locator"), f"{label}.source_locator", maximum=1_000)
        source_slug = require_slug(item.get("source_slug"), f"{label}.source_slug")
        digest = require_digest(item.get("source_digest"), f"{label}.source_digest")
        if op == "add":
            applicability = require_text(
                item.get("applicability_md"), f"{label}.applicability_md", maximum=4_000
            )
            connection.execute(
                "INSERT INTO card_origin VALUES (?,?,?,?,?)",
                (slug, locator, source_slug, digest, applicability),
            )
        else:
            cursor = connection.execute(
                """DELETE FROM card_origin WHERE card_slug=? AND source_locator=?
                   AND source_slug=? AND source_digest=?""",
                (slug, locator, source_slug, digest),
            )
            if cursor.rowcount != 1:
                raise ResearchMemoryError(
                    f"origin does not exist: {slug}, {locator}, {source_slug}, {digest}"
                )
        count += 1
    return count


def apply_edge_operations(connection: sqlite3.Connection, operations: Any) -> int:
    count = 0
    for index, value in enumerate(require_sequence(operations, "changeset.edges")):
        label = f"changeset.edges[{index}]"
        item, op = _operation(value, label, ("add", "delete"))
        allowed = ("op", "source_slug", "relation", "target_slug", "note_md")
        require_keys(item, allowed if op == "add" else allowed[:-1], label)
        source = require_slug(item.get("source_slug"), f"{label}.source_slug")
        relation = normalize_relation(item.get("relation"), f"{label}.relation")
        target = require_slug(item.get("target_slug"), f"{label}.target_slug")
        if source == target:
            raise ResearchMemoryError(f"{label} must not create a self-edge")
        if op == "add":
            note = optional_text(item.get("note_md"), f"{label}.note_md", maximum=4_000)
            connection.execute(
                "INSERT INTO card_edge VALUES (?,?,?,?)", (source, relation, target, note)
            )
        else:
            cursor = connection.execute(
                "DELETE FROM card_edge WHERE source_slug=? AND relation=? AND target_slug=?",
                (source, relation, target),
            )
            if cursor.rowcount != 1:
                raise ResearchMemoryError(f"edge does not exist: {source}, {relation}, {target}")
        count += 1
    return count


def apply_key_link_operations(
    connection: sqlite3.Connection,
    operations: Any,
    document: CanonicalDocument,
    now: str,
) -> int:
    count = 0
    for index, value in enumerate(require_sequence(operations, "changeset.key_links")):
        label = f"changeset.key_links[{index}]"
        item, op = _operation(value, label, ("add", "update", "delete"))
        base = ("op", "card_slug", "canonical_key", "relation")
        if op == "add":
            allowed = (*base, "note_md")
        elif op == "update":
            allowed = (*base, "expected_revision", "set")
        else:
            allowed = (*base, "expected_revision")
        require_keys(item, allowed, label)
        slug = require_slug(item.get("card_slug"), f"{label}.card_slug")
        key = require_slug(item.get("canonical_key"), f"{label}.canonical_key")
        relation = normalize_relation(item.get("relation"), f"{label}.relation")
        section = document.by_key.get(key)
        if section is None:
            raise ResearchMemoryError(f"canonical key does not exist: {key}")
        card = connection.execute("SELECT revision FROM card WHERE slug=?", (slug,)).fetchone()
        if card is None:
            raise ResearchMemoryError(f"card does not exist: {slug}")
        identity = (slug, key, relation)
        if op == "add":
            note = optional_text(item.get("note_md"), f"{label}.note_md", maximum=4_000)
            connection.execute(
                """INSERT INTO card_key(
                   card_slug,canonical_key,relation,note_md,reviewed_section_sha256,
                   reviewed_card_revision,revision,created_at,updated_at
                   ) VALUES (?,?,?,?,?,?,1,?,?)""",
                (*identity, note, section.section_sha256, card["revision"], now, now),
            )
        else:
            expected = require_revision(
                item.get("expected_revision"), f"{label}.expected_revision", minimum=1
            )
            row = connection.execute(
                "SELECT revision,note_md,reviewed_section_sha256,reviewed_card_revision "
                "FROM card_key WHERE card_slug=? AND canonical_key=? AND relation=?",
                identity,
            ).fetchone()
            if row is None:
                raise ResearchMemoryError(f"key link does not exist: {slug}, {key}, {relation}")
            if row["revision"] != expected:
                raise ResearchMemoryError(
                    f"key link revision conflict: expected {expected}, observed {row['revision']}"
                )
            if op == "delete":
                connection.execute(
                    "DELETE FROM card_key WHERE card_slug=? AND canonical_key=? AND relation=?",
                    identity,
                )
            else:
                patch = require_mapping(item.get("set"), f"{label}.set")
                require_keys(patch, ("note_md",), f"{label}.set")
                note = (
                    optional_text(patch["note_md"], f"{label}.set.note_md", maximum=4_000)
                    if "note_md" in patch
                    else row["note_md"]
                )
                changed = (
                    note != row["note_md"]
                    or section.section_sha256 != row["reviewed_section_sha256"]
                    or card["revision"] != row["reviewed_card_revision"]
                )
                if not changed:
                    raise ResearchMemoryError(f"{label} makes no change")
                connection.execute(
                    """UPDATE card_key SET note_md=?,reviewed_section_sha256=?,
                       reviewed_card_revision=?,revision=?,updated_at=?
                       WHERE card_slug=? AND canonical_key=? AND relation=?""",
                    (
                        note, section.section_sha256, card["revision"], expected + 1, now,
                        *identity,
                    ),
                )
        count += 1
    return count


def _require_artifact_target(
    connection: sqlite3.Connection, document: CanonicalDocument, target_type: str, target_key: str
) -> None:
    if target_type == "key":
        if target_key not in document.by_key:
            raise ResearchMemoryError(f"canonical key does not exist: {target_key}")
    elif connection.execute("SELECT 1 FROM card WHERE slug=?", (target_key,)).fetchone() is None:
        raise ResearchMemoryError(f"card does not exist: {target_key}")


def apply_artifact_link_operations(
    connection: sqlite3.Connection, operations: Any, document: CanonicalDocument
) -> int:
    count = 0
    for index, value in enumerate(require_sequence(operations, "changeset.artifact_links")):
        label = f"changeset.artifact_links[{index}]"
        item, op = _operation(value, label, ("add", "delete"))
        allowed = (
            "op", "artifact_slug", "target_type", "target_key", "relation", "applicability_md"
        )
        require_keys(item, allowed if op == "add" else allowed[:-1], label)
        artifact = require_slug(item.get("artifact_slug"), f"{label}.artifact_slug")
        target_type = require_text(item.get("target_type"), f"{label}.target_type", maximum=10)
        if target_type not in ("card", "key"):
            raise ResearchMemoryError(f"{label}.target_type must be 'card' or 'key'")
        target_key = require_slug(item.get("target_key"), f"{label}.target_key")
        relation = normalize_relation(item.get("relation"), f"{label}.relation")
        _require_artifact_target(connection, document, target_type, target_key)
        identity = (artifact, target_type, target_key, relation, "curated")
        if op == "add":
            applicability = optional_text(
                item.get("applicability_md"), f"{label}.applicability_md", maximum=4_000
            )
            connection.execute(
                "INSERT INTO artifact_link VALUES (?,?,?,?,?,?)",
                (artifact, target_type, target_key, relation, applicability, "curated"),
            )
        else:
            cursor = connection.execute(
                """DELETE FROM artifact_link WHERE artifact_slug=? AND target_type=?
                   AND target_key=? AND relation=? AND source=?""",
                identity,
            )
            if cursor.rowcount != 1:
                raise ResearchMemoryError(
                    f"curated artifact link does not exist: {artifact}, {target_type}, {target_key}, {relation}"
                )
        count += 1
    return count


def semantic_errors(connection: sqlite3.Connection, document: CanonicalDocument) -> list[str]:
    errors: list[str] = []
    for row in connection.execute(
        "SELECT card_slug,canonical_key FROM card_key ORDER BY card_slug,canonical_key"
    ):
        if row["canonical_key"] not in document.by_key:
            errors.append(
                f"card {row['card_slug']!r} links missing canonical key {row['canonical_key']!r}"
            )
    for row in connection.execute(
        "SELECT artifact_slug,target_type,target_key FROM artifact_link ORDER BY artifact_slug,target_type,target_key"
    ):
        if row["target_type"] == "key" and row["target_key"] not in document.by_key:
            errors.append(
                f"artifact {row['artifact_slug']!r} links missing canonical key {row['target_key']!r}"
            )
        if row["target_type"] == "card" and connection.execute(
            "SELECT 1 FROM card WHERE slug=?", (row["target_key"],)
        ).fetchone() is None:
            errors.append(
                f"artifact {row['artifact_slug']!r} links missing card {row['target_key']!r}"
            )
    return errors


CHANGESET_FIELDS = {
    "round_id",
    "expected_revision",
    "expected_canonical_sha256",
    "cards",
    "artifacts",
    "origins",
    "edges",
    "key_links",
    "artifact_links",
}


def apply_changeset(document: CanonicalDocument, value: Any) -> dict[str, Any]:
    changeset = require_mapping(value, "changeset")
    require_keys(changeset, CHANGESET_FIELDS, "changeset")
    for required in ("round_id", "expected_revision", "expected_canonical_sha256"):
        if required not in changeset:
            raise ResearchMemoryError(f"changeset is missing field: {required}")
    round_id = require_text(changeset["round_id"], "changeset.round_id", maximum=200)
    expected_revision = require_revision(changeset["expected_revision"], "changeset.expected_revision")
    expected_canonical = require_digest(
        changeset["expected_canonical_sha256"], "changeset.expected_canonical_sha256"
    )
    if expected_canonical != document.canonical_sha256:
        raise ResearchMemoryError(
            "canonical digest conflict: "
            f"expected {expected_canonical}, observed {document.canonical_sha256}"
        )

    connection = connect_database(document, writable=True)
    root = repository_root(document.path)
    now = utc_now()
    try:
        connection.execute("BEGIN IMMEDIATE")
        meta = meta_row(connection)
        if meta["revision"] != expected_revision:
            raise ResearchMemoryError(
                f"database revision conflict: expected {expected_revision}, observed {meta['revision']}"
            )
        if meta["last_round_id"] == round_id:
            raise ResearchMemoryError(f"round_id was already committed: {round_id}")

        counts = {
            "cards": apply_card_operations(connection, changeset.get("cards", []), now),
            "artifacts": apply_artifact_operations(
                connection, changeset.get("artifacts", []), document, root, now
            ),
            "origins": apply_origin_operations(connection, changeset.get("origins", [])),
            "edges": apply_edge_operations(connection, changeset.get("edges", [])),
            "key_links": apply_key_link_operations(
                connection, changeset.get("key_links", []), document, now
            ),
            "artifact_links": apply_artifact_link_operations(
                connection, changeset.get("artifact_links", []), document
            ),
        }
        relationship_errors = semantic_errors(connection, document)
        if relationship_errors:
            raise ResearchMemoryError("; ".join(relationship_errors))
        if not any(counts.values()) and meta["canonical_sha256"] == document.canonical_sha256:
            raise ResearchMemoryError("changeset makes no change")
        new_revision = expected_revision + 1
        connection.execute(
            """UPDATE meta SET canonical_sha256=?,revision=?,last_round_id=?,updated_at=?
               WHERE singleton=1""",
            (document.canonical_sha256, new_revision, round_id, now),
        )
        foreign = list(connection.execute("PRAGMA foreign_key_check"))
        if foreign:
            raise ResearchMemoryError(f"foreign-key check failed for {len(foreign)} row(s)")
        connection.commit()
        return {
            "ok": True,
            "command": "apply",
            "round_id": round_id,
            "canonical_path": str(document.path.resolve()),
            "database_path": str(document.memory_path),
            "canonical_sha256": document.canonical_sha256,
            "database_revision": new_revision,
            "operation_counts": counts,
        }
    except sqlite3.IntegrityError as error:
        connection.rollback()
        raise ResearchMemoryError(f"changeset violates database constraints: {error}") from error
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def _search_row(entity_type: str, row: sqlite3.Row) -> dict[str, Any]:
    summary = card_summary(row) if entity_type == "card" else artifact_summary(row)
    return {"entity_type": entity_type, **summary}


def _fts_query(text: str) -> str:
    tokens = re.findall(r"[^\W_]+", text, flags=re.UNICODE)
    if not tokens:
        raise ResearchMemoryError("search text must contain a word or number")
    return " AND ".join('"' + token.replace('"', '""') + '"' for token in tokens)


def normalize_search_facets(values: Sequence[str]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for index, value in enumerate(values):
        if "=" not in value:
            raise ResearchMemoryError(
                f"facet {index + 1} must use TYPE=VALUE, for example field=combinatorics"
            )
        kind, raw = value.split("=", 1)
        if kind not in FACET_TYPES:
            raise ResearchMemoryError(
                f"facet type must be one of: {', '.join(FACET_TYPES)}"
            )
        _, normalized = normalize_facet_value(kind, raw, f"facet {index + 1}")
        grouped.setdefault(kind, [])
        if normalized not in grouped[kind]:
            grouped[kind].append(normalized)
    return grouped


def search_summaries(
    connection: sqlite3.Connection,
    text: str | None,
    facets: Mapping[str, Sequence[str]],
    *,
    limit: int,
    offset: int,
) -> tuple[list[dict[str, Any]], int]:
    params: list[Any] = []
    joins = ""
    where: list[str] = []
    if text:
        joins = (
            "JOIN summary_fts ON summary_fts.entity_type='card' "
            "AND summary_fts.slug=c.slug"
        )
        where.append("summary_fts MATCH ?")
        params.append(_fts_query(text))
    for kind, values in facets.items():
        placeholders = ",".join("?" for _ in values)
        where.append(
            "EXISTS (SELECT 1 FROM card_facet f WHERE f.card_slug=c.slug "
            f"AND f.type=? AND f.normalized_value IN ({placeholders}))"
        )
        params.extend([kind, *values])
    predicate = " WHERE " + " AND ".join(where) if where else ""
    rank = "bm25(summary_fts)" if text else "0.0"
    card_total = int(
        connection.execute(
            f"SELECT count(*) FROM card c {joins}{predicate}", params
        ).fetchone()[0]
    )
    fetch = offset + limit
    card_order = "rank,c.slug" if text else "c.updated_at DESC,c.slug"
    cards = [
        ("card", row, float(row["rank"]))
        for row in connection.execute(
            f"SELECT c.*, {rank} AS rank FROM card c {joins}{predicate} "
            f"ORDER BY {card_order} LIMIT ?",
            [*params, fetch],
        )
    ]

    artifacts: list[tuple[str, sqlite3.Row, float]] = []
    artifact_total = 0
    if not facets:
        artifact_total = int(
            connection.execute(
                """SELECT count(*) FROM artifact a JOIN summary_fts
                   ON summary_fts.entity_type='artifact' AND summary_fts.slug=a.slug
                   WHERE summary_fts MATCH ?"""
                if text
                else "SELECT count(*) FROM artifact",
                (_fts_query(text),) if text else (),
            ).fetchone()[0]
        )
        if text:
            artifacts = [
                ("artifact", row, float(row["rank"]))
                for row in connection.execute(
                    """SELECT a.*, bm25(summary_fts) AS rank FROM artifact a
                       JOIN summary_fts ON summary_fts.entity_type='artifact'
                         AND summary_fts.slug=a.slug
                       WHERE summary_fts MATCH ? ORDER BY rank,a.slug LIMIT ?""",
                    (_fts_query(text), fetch),
                )
            ]
        else:
            artifacts = [
                ("artifact", row, 0.0)
                for row in connection.execute(
                    "SELECT a.*, 0.0 AS rank FROM artifact a "
                    "ORDER BY a.updated_at DESC,a.slug LIMIT ?",
                    (fetch,),
                )
            ]
    combined = cards + artifacts
    if text:
        combined.sort(key=lambda item: (item[2], item[0], item[1]["slug"]))
    else:
        combined.sort(key=lambda item: (item[1]["updated_at"], item[0], item[1]["slug"]), reverse=True)
    total = card_total + artifact_total
    return [
        _search_row(entity_type, row)
        for entity_type, row, _ in combined[offset : offset + limit]
    ], total


def text_chunk(text: str | None, offset: int) -> dict[str, Any] | None:
    if text is None:
        return None
    if offset > len(text):
        raise ResearchMemoryError(
            f"body offset {offset} exceeds body length {len(text)}"
        )
    end = min(offset + BODY_CHUNK, len(text))
    return {
        "text": text[offset:end],
        "offset": offset,
        "end": end,
        "total_characters": len(text),
        "next_offset": end if end < len(text) else None,
    }


def page_metadata(total: int, offset: int, limit: int) -> dict[str, int | None]:
    end = min(total, offset + limit)
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "next_offset": end if end < total else None,
    }


def read_meta(connection: sqlite3.Connection, document: CanonicalDocument) -> dict[str, Any]:
    meta = meta_row(connection)
    counts = {
        table: connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        for table in ("card", "artifact", "card_key", "artifact_link")
    }
    return {
        "canonical_path": str(document.path.resolve()),
        "database_path": str(document.memory_path),
        "canonical_sha256": document.canonical_sha256,
        "indexed_canonical_sha256": meta["canonical_sha256"],
        "database_revision": meta["revision"],
        "last_round_id": meta["last_round_id"],
        "canonical_digest_current": (
            meta["canonical_sha256"] == document.canonical_sha256
        ),
        "counts": counts,
    }


def command_read(args: argparse.Namespace, document: CanonicalDocument) -> dict[str, Any]:
    if not document.memory_declared:
        raise ResearchMemoryError("canonical front matter does not declare research_memory")
    limit = require_revision(args.limit, "--limit", minimum=1)
    if limit > MAX_LIMIT:
        raise ResearchMemoryError(f"--limit may not exceed {MAX_LIMIT}")
    offset = require_revision(args.offset, "--offset")
    if offset > MAX_OFFSET:
        raise ResearchMemoryError(f"--offset may not exceed {MAX_OFFSET}")
    body_offset = require_revision(args.body_offset, "--body-offset")
    selector = args.selector
    value = args.value
    needs_value = selector in ("key", "card", "artifact")
    if needs_value and value is None:
        raise ResearchMemoryError(f"read {selector} requires VALUE")
    if selector not in ("search",) and args.facet:
        raise ResearchMemoryError("--facet is valid only with read search")
    if selector not in ("card", "artifact") and args.full:
        raise ResearchMemoryError("--full is valid only with read card or read artifact")
    if selector not in ("key", "card") and body_offset:
        raise ResearchMemoryError("--body-offset is valid only with read key or read card")
    if selector not in ("search",) and not needs_value and value is not None:
        raise ResearchMemoryError(f"read {selector} does not accept VALUE")

    connection = connect_database(document)
    try:
        meta = meta_row(connection)
        base = {
            "ok": True,
            "command": "read",
            "selector": selector,
            "database_path": str(document.memory_path),
            "database_revision": meta["revision"],
            "canonical_sha256": document.canonical_sha256,
            "indexed_canonical_sha256": meta["canonical_sha256"],
            # This is intentionally narrower than `check`'s full `current`.
            # A bounded read does not replay artifacts or rederive every cache.
            "canonical_digest_current": (
                meta["canonical_sha256"] == document.canonical_sha256
            ),
        }
        if selector == "meta":
            return {**base, "meta": read_meta(connection, document)}
        if selector == "keys":
            keys = [section.metadata() for section in document.sections if section.key]
            return {
                **base,
                **page_metadata(len(keys), offset, limit),
                "keys": keys[offset : offset + limit],
            }
        if selector == "key":
            key = require_slug(value, "key")
            section = document.by_key.get(key)
            if section is None:
                raise ResearchMemoryError(f"canonical key does not exist: {key}")
            card_total = int(connection.execute(
                "SELECT count(DISTINCT card_slug) FROM card_key WHERE canonical_key=?",
                (key,),
            ).fetchone()[0])
            artifact_total = int(connection.execute(
                "SELECT count(DISTINCT artifact_slug) FROM artifact_link "
                "WHERE target_type='key' AND target_key=?",
                (key,),
            ).fetchone()[0])
            card_rows = list(
                connection.execute(
                    """SELECT c.*,
                       MIN(CASE WHEN k.reviewed_section_sha256=?
                                 AND k.reviewed_card_revision=c.revision
                                THEN 1 ELSE 0 END) AS link_current
                       FROM card c JOIN card_key k ON k.card_slug=c.slug
                       WHERE k.canonical_key=? GROUP BY c.slug
                       ORDER BY c.updated_at DESC,c.slug
                       LIMIT ? OFFSET ?""",
                    (section.section_sha256, key, limit, offset),
                )
            )
            artifact_rows = list(
                connection.execute(
                    """SELECT DISTINCT a.* FROM artifact a JOIN artifact_link l
                       ON l.artifact_slug=a.slug WHERE l.target_type='key' AND l.target_key=?
                       ORDER BY a.updated_at DESC,a.slug LIMIT ? OFFSET ?""",
                    (key, limit, offset),
                )
            )
            return {
                **base,
                "key": key,
                "section": {
                    **section.metadata(),
                    "markdown": text_chunk(document.section_markdown(section), body_offset),
                },
                "pagination": {
                    "cards": page_metadata(card_total, offset, limit),
                    "artifacts": page_metadata(artifact_total, offset, limit),
                },
                "cards": [
                    {**card_summary(row), "link_current": bool(row["link_current"])}
                    for row in card_rows
                ],
                "artifacts": [artifact_summary(row) for row in artifact_rows],
            }
        if selector == "card":
            slug = require_slug(value, "card slug")
            row = connection.execute("SELECT * FROM card WHERE slug=?", (slug,)).fetchone()
            if row is None:
                raise ResearchMemoryError(f"card does not exist: {slug}")
            result: dict[str, Any] = selected_card(row)
            if args.full:
                body = connection.execute(
                    "SELECT detail_md FROM card_body WHERE card_slug=?", (slug,)
                ).fetchone()
                related_totals = {
                    "origins": connection.execute(
                        "SELECT count(*) FROM card_origin WHERE card_slug=?", (slug,)
                    ).fetchone()[0],
                    "outgoing_edges": connection.execute(
                        "SELECT count(*) FROM card_edge WHERE source_slug=?", (slug,)
                    ).fetchone()[0],
                    "incoming_edges": connection.execute(
                        "SELECT count(*) FROM card_edge WHERE target_slug=?", (slug,)
                    ).fetchone()[0],
                    "key_links": connection.execute(
                        "SELECT count(*) FROM card_key WHERE card_slug=?", (slug,)
                    ).fetchone()[0],
                    "artifact_links": connection.execute(
                        "SELECT count(*) FROM artifact_link WHERE target_type='card' AND target_key=?",
                        (slug,),
                    ).fetchone()[0],
                }
                result.update(
                    {
                        "detail_md": text_chunk(body["detail_md"] if body else None, body_offset),
                        "facets": [dict(item) for item in connection.execute(
                            "SELECT type,value,normalized_value FROM card_facet WHERE card_slug=? ORDER BY type,normalized_value",
                            (slug,),
                        )],
                        "origins": [dict(item) for item in connection.execute(
                            "SELECT source_locator,source_slug,source_digest,applicability_md "
                            "FROM card_origin WHERE card_slug=? ORDER BY source_locator,source_slug "
                            "LIMIT ? OFFSET ?",
                            (slug, limit, offset),
                        )],
                        "outgoing_edges": [dict(item) for item in connection.execute(
                            "SELECT relation,target_slug,note_md FROM card_edge WHERE source_slug=? "
                            "ORDER BY relation,target_slug LIMIT ? OFFSET ?",
                            (slug, limit, offset),
                        )],
                        "incoming_edges": [dict(item) for item in connection.execute(
                            "SELECT source_slug,relation,note_md FROM card_edge WHERE target_slug=? "
                            "ORDER BY relation,source_slug LIMIT ? OFFSET ?",
                            (slug, limit, offset),
                        )],
                        "key_links": [dict(item) for item in connection.execute(
                            "SELECT canonical_key,relation,note_md,reviewed_section_sha256,"
                            "reviewed_card_revision,revision FROM card_key WHERE card_slug=? "
                            "ORDER BY canonical_key,relation LIMIT ? OFFSET ?",
                            (slug, limit, offset),
                        )],
                        "artifact_links": [dict(item) for item in connection.execute(
                            "SELECT artifact_slug,relation,applicability_md,source FROM artifact_link "
                            "WHERE target_type='card' AND target_key=? ORDER BY artifact_slug,relation "
                            "LIMIT ? OFFSET ?",
                            (slug, limit, offset),
                        )],
                        "related_pagination": {
                            name: page_metadata(int(total), offset, limit)
                            for name, total in related_totals.items()
                        },
                    }
                )
            return {**base, "card": result}
        if selector == "artifact":
            slug = require_slug(value, "artifact slug")
            row = connection.execute("SELECT * FROM artifact WHERE slug=?", (slug,)).fetchone()
            if row is None:
                raise ResearchMemoryError(f"artifact does not exist: {slug}")
            result = artifact_summary(row)
            if args.full:
                reference_total = int(connection.execute(
                    "SELECT count(*) FROM artifact_ref WHERE artifact_slug=?", (slug,)
                ).fetchone()[0])
                link_total = int(connection.execute(
                    "SELECT count(*) FROM artifact_link WHERE artifact_slug=?", (slug,)
                ).fetchone()[0])
                result.update(
                    {
                        "metadata": json.loads(row["metadata_json"]),
                        "references": [dict(item) for item in connection.execute(
                            "SELECT role,path,sha256,size_bytes FROM artifact_ref WHERE artifact_slug=? "
                            "ORDER BY role,path LIMIT ? OFFSET ?",
                            (slug, limit, offset),
                        )],
                        "links": [dict(item) for item in connection.execute(
                            "SELECT target_type,target_key,relation,applicability_md,source "
                            "FROM artifact_link WHERE artifact_slug=? "
                            "ORDER BY target_type,target_key,relation,source LIMIT ? OFFSET ?",
                            (slug, limit, offset),
                        )],
                        "related_pagination": {
                            "references": page_metadata(reference_total, offset, limit),
                            "links": page_metadata(link_total, offset, limit),
                        },
                    }
                )
            return {**base, "artifact": result}
        facets = normalize_search_facets(args.facet)
        search_text = optional_text(value, "search text", maximum=1_000) if value is not None else None
        if selector == "search" and search_text is None and not facets:
            raise ResearchMemoryError("read search requires text VALUE or at least one --facet")
        if selector == "all":
            search_text = None
            facets = {}
        results, total = search_summaries(
            connection, search_text, facets, limit=limit, offset=offset
        )
        return {
            **base,
            "query": search_text,
            "facets": [f"{kind}={value}" for kind, values in facets.items() for value in values],
            **page_metadata(total, offset, limit),
            "results": results,
        }
    finally:
        connection.close()


def _expected_search_rows(connection: sqlite3.Connection) -> list[tuple[str, str, str, str, str]]:
    rows: list[tuple[str, str, str, str, str]] = []
    for card in connection.execute("SELECT slug,title,summary_md,kind FROM card ORDER BY slug"):
        terms = " ".join(
            [card["kind"]]
            + [
                facet[0]
                for facet in connection.execute(
                    "SELECT value FROM card_facet WHERE card_slug=? ORDER BY type,normalized_value",
                    (card["slug"],),
                )
            ]
        )
        rows.append(("card", card["slug"], card["title"], card["summary_md"], terms))
    for artifact in connection.execute(
        "SELECT slug,title,summary_md,kind,metadata_json FROM artifact ORDER BY slug"
    ):
        metadata = json.loads(artifact["metadata_json"])
        terms = " ".join(
            [artifact["kind"], metadata["purpose"], metadata["scope"], *metadata["canonical_keys"]]
        )
        rows.append(("artifact", artifact["slug"], artifact["title"], artifact["summary_md"], terms))
    return sorted(rows)


def inspect_database(document: CanonicalDocument) -> dict[str, Any]:
    path = document.memory_path
    base: dict[str, Any] = {
        "canonical_path": str(document.path.resolve()),
        "database_path": str(path),
        "canonical_sha256": document.canonical_sha256,
        "indexed_canonical_sha256": None,
        "database_revision": None,
        "integrity_ok": False,
        "current": False,
        "status": "invalid",
        "errors": [],
        "omitted_error_count": 0,
    }
    integrity_errors: list[dict[str, Any]] = []
    stale_errors: list[dict[str, Any]] = []
    omitted = 0
    integrity_count = 0
    stale_count = 0

    def record(
        category: str,
        code: str,
        message: str,
        *,
        entity_type: str | None = None,
        entity_key: str | None = None,
    ) -> None:
        nonlocal omitted, integrity_count, stale_count
        issue: dict[str, Any] = {
            "category": category,
            "code": code,
            "message": message,
        }
        if entity_type is not None:
            issue["entity_type"] = entity_type
        if entity_key is not None:
            issue["entity_key"] = entity_key
        target = integrity_errors if category == "integrity" else stale_errors
        if category == "integrity":
            integrity_count += 1
        else:
            stale_count += 1
        if len(integrity_errors) + len(stale_errors) < MAX_CHECK_ISSUES:
            target.append(issue)
        else:
            omitted += 1

    def finish() -> dict[str, Any]:
        base["integrity_ok"] = integrity_count == 0
        base["current"] = integrity_count == 0 and stale_count == 0
        base["status"] = (
            "current"
            if base["current"]
            else "stale"
            if base["integrity_ok"]
            else "invalid"
        )
        base["errors"] = integrity_errors + stale_errors
        base["omitted_error_count"] = omitted
        base["error_count"] = integrity_count + stale_count
        return base

    if path.is_symlink() or not path.is_file():
        record(
            "integrity",
            "database-path",
            f"database must be a regular non-symlink file: {path}",
        )
        return finish()
    try:
        connection = sqlite3.connect(database_uri(path, "ro"), uri=True)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA query_only=ON")
        connection.execute("PRAGMA foreign_keys=ON")
    except sqlite3.DatabaseError as error:
        record("integrity", "database-open", f"cannot open research database: {error}")
        return finish()
    try:
        identity = _identity_errors(connection)
        for message in identity:
            record("integrity", "database-identity", message)
        if not identity:
            for message in schema_errors(connection):
                record("integrity", "database-schema", message)
        if integrity_errors:
            base["status"] = "invalid"
            return finish()
        quick = [row[0] for row in connection.execute("PRAGMA integrity_check")]
        if quick != ["ok"]:
            for message in quick:
                record(
                    "integrity", "sqlite-integrity", f"SQLite integrity check: {message}"
                )
        foreign = list(connection.execute("PRAGMA foreign_key_check"))
        if foreign:
            record(
                "integrity",
                "foreign-key",
                f"foreign-key check failed for {len(foreign)} row(s)",
            )
        meta = connection.execute("SELECT * FROM meta WHERE singleton=1").fetchone()
        if meta is None:
            record("integrity", "meta-missing", "database meta row is missing")
        else:
            base["indexed_canonical_sha256"] = meta["canonical_sha256"]
            base["database_revision"] = meta["revision"]
            if meta["canonical_sha256"] != document.canonical_sha256:
                record(
                    "stale",
                    "canonical-digest",
                    "canonical digest is stale: "
                    f"indexed {meta['canonical_sha256']}, observed {document.canonical_sha256}",
                )

        for row in connection.execute("SELECT * FROM card ORDER BY slug"):
            slug = str(row["slug"])
            facets = [
                dict(facet)
                for facet in connection.execute(
                    "SELECT type,value,normalized_value FROM card_facet "
                    "WHERE card_slug=? ORDER BY type,normalized_value",
                    (slug,),
                )
            ]
            body = connection.execute(
                "SELECT detail_md FROM card_body WHERE card_slug=?", (slug,)
            ).fetchone()
            candidate = {
                key: row[key]
                for key in CARD_BASE_FIELDS
                if key not in ("detail_md", "facets")
            }
            candidate["detail_md"] = body["detail_md"] if body else None
            candidate["facets"] = [
                {"type": facet["type"], "value": facet["value"]} for facet in facets
            ]
            try:
                normalized = normalize_card(candidate, require_all=False)
                require_revision(row["revision"], f"card {slug}.revision", minimum=1)
                normalized_facets = normalized["facets"]
                if facets != normalized_facets:
                    record(
                        "integrity",
                        "card-facet-cache",
                        "stored facet normalization does not match the controlled normalization",
                        entity_type="card",
                        entity_key=slug,
                    )
                observed_hash = digest_json(card_content(normalized))
                if observed_hash != row["content_sha256"]:
                    record(
                        "integrity",
                        "card-content-digest",
                        f"content digest mismatch: stored {row['content_sha256']}, observed {observed_hash}",
                        entity_type="card",
                        entity_key=slug,
                    )
            except ResearchMemoryError as error:
                record(
                    "integrity",
                    "card-content",
                    str(error),
                    entity_type="card",
                    entity_key=slug,
                )
            else:
                try:
                    _validate_card_state(normalized)
                except ResearchMemoryError as error:
                    record(
                        "integrity",
                        "card-state",
                        str(error),
                        entity_type="card",
                        entity_key=slug,
                    )

        try:
            actual_search = sorted(
                tuple(row)
                for row in connection.execute(
                    "SELECT entity_type,slug,title,summary_md,terms FROM summary_fts"
                )
            )
            if actual_search != _expected_search_rows(connection):
                record(
                    "integrity",
                    "summary-index",
                    "summary search index does not match stored summaries",
                )
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            record(
                "integrity",
                "summary-index-source",
                f"cannot derive summary search index: {error}",
            )

        for row in connection.execute(
            """SELECT k.card_slug,k.canonical_key,k.reviewed_section_sha256,
               k.reviewed_card_revision,c.revision AS card_revision
               FROM card_key k JOIN card c ON c.slug=k.card_slug
               ORDER BY k.card_slug,k.canonical_key"""
        ):
            section = document.by_key.get(row["canonical_key"])
            if section is None:
                record(
                    "stale",
                    "card-key-missing",
                    f"links missing canonical key {row['canonical_key']!r}",
                    entity_type="card",
                    entity_key=row["card_slug"],
                )
            elif section.section_sha256 != row["reviewed_section_sha256"]:
                record(
                    "stale",
                    "card-key-section-digest",
                    f"link to {row['canonical_key']!r} has a stale section digest",
                    entity_type="card",
                    entity_key=row["card_slug"],
                )
            if row["card_revision"] != row["reviewed_card_revision"]:
                record(
                    "stale",
                    "card-key-card-revision",
                    f"link to {row['canonical_key']!r} has a stale card revision",
                    entity_type="card",
                    entity_key=row["card_slug"],
                )

        root = repository_root(document.path)
        for row in connection.execute("SELECT * FROM artifact ORDER BY slug"):
            slug = str(row["slug"])
            try:
                observed = extract_artifact(root, row["source_path"], document)
                cache_fields = {
                    "slug": observed["slug"],
                    "kind": observed["kind"],
                    "title": observed["title"],
                    "summary_md": observed["summary_md"],
                    "source_path": observed["source_path"],
                    "source_sha256": observed["source_sha256"],
                    "metadata_json": observed["metadata_json"],
                    "metadata_sha256": observed["metadata_sha256"],
                }
                changed_fields = sorted(
                    field for field, expected in cache_fields.items() if row[field] != expected
                )
                if changed_fields:
                    record(
                        "stale",
                        "artifact-cache",
                        "cached field(s) differ from source: " + ", ".join(changed_fields),
                        entity_type="artifact",
                        entity_key=slug,
                    )
                expected_refs = sorted(
                    (ref["role"], ref["path"], ref["sha256"], ref["size_bytes"])
                    for ref in observed["references"]
                )
                cached_refs = sorted(
                    tuple(ref)
                    for ref in connection.execute(
                        "SELECT role,path,sha256,size_bytes FROM artifact_ref WHERE artifact_slug=?",
                        (row["slug"],),
                    )
                )
                if expected_refs != cached_refs:
                    record(
                        "stale",
                        "artifact-reference-cache",
                        "cached reference hashes or sizes differ from source metadata",
                        entity_type="artifact",
                        entity_key=slug,
                    )
                expected_links = sorted(
                    ("key", key, "addresses", None, "metadata")
                    for key in observed["metadata"]["canonical_keys"]
                )
                cached_links = sorted(
                    tuple(link)
                    for link in connection.execute(
                        "SELECT target_type,target_key,relation,applicability_md,source "
                        "FROM artifact_link WHERE artifact_slug=? AND source='metadata'",
                        (slug,),
                    )
                )
                if expected_links != cached_links:
                    record(
                        "stale",
                        "artifact-metadata-links",
                        "metadata-derived canonical links differ from source metadata",
                        entity_type="artifact",
                        entity_key=slug,
                    )
            except ResearchMemoryError as error:
                record(
                    "stale",
                    "artifact-source",
                    str(error),
                    entity_type="artifact",
                    entity_key=slug,
                )

        for error in semantic_errors(connection, document):
            if "missing canonical key" in error:
                record("stale", "relationship-target", error)
            else:
                record("integrity", "relationship-target", error)

        counts = {
            table: connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
            for table in ("card", "artifact", "card_key", "artifact_link")
        }
        base["counts"] = counts
    except (sqlite3.DatabaseError, json.JSONDecodeError, KeyError, TypeError) as error:
        record(
            "integrity",
            "database-validation",
            f"database validation failed: {error}",
        )
    finally:
        connection.close()

    return finish()


def command_ensure(canonical: Path) -> dict[str, Any]:
    document = scan_canonical(canonical, allow_missing_memory=True)
    created = False
    if document.memory_declared and not document.memory_path.exists():
        raise ResearchMemoryError(
            f"declared research database is missing; refusing to recreate it: {document.memory_path}"
        )
    if not document.memory_path.exists():
        create_database(document)
        created = True
    state = inspect_database(document)
    if not state["integrity_ok"]:
        raise ResearchMemoryError(
            "; ".join(issue["message"] for issue in state["errors"])
        )
    return {
        "ok": True,
        "command": "ensure",
        "created": created,
        "research_memory": document.memory_relative_path,
        "locator_to_add": (
            None
            if document.memory_declared
            else f"research_memory: {document.memory_relative_path}"
        ),
        **{key: state[key] for key in (
            "canonical_path", "database_path", "canonical_sha256",
            "indexed_canonical_sha256", "database_revision", "integrity_ok", "current", "status"
        )},
        "errors": state["errors"],
    }


def command_check(canonical: Path) -> dict[str, Any]:
    document = scan_canonical(canonical)
    state = inspect_database(document)
    return {"ok": state["integrity_ok"] and state["current"], "command": "check", **state}


def parse_json_input(text: str) -> Any:
    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ResearchMemoryError(f"JSON input has duplicate key {key!r}")
            result[key] = value
        return result

    try:
        return json.loads(text, object_pairs_hook=no_duplicates)
    except json.JSONDecodeError as error:
        raise ResearchMemoryError(f"stdin is not valid JSON: {error}") from error


APPLY_HELP = """Normative stdin grammar (unknown fields are errors):
  changeset = {round_id, expected_revision, expected_canonical_sha256,
               cards?, artifacts?, origins?, edges?, key_links?, artifact_links?}
  cards = [{op:"add", card:{...}} |
           {op:"update", slug, expected_revision, set:{...}} |
           {op:"delete", slug, expected_revision}]
  artifacts = [{op:"add", source_path} |
               {op:"update", slug, expected_revision, source_path} |
               {op:"delete", slug, expected_revision}]
  origins = [{op:"add", card_slug, source_locator, source_slug, source_digest,
              applicability_md} |
             {op:"delete", card_slug, source_locator, source_slug, source_digest}]
  edges = [{op:"add", source_slug, relation, target_slug, note_md?} |
           {op:"delete", source_slug, relation, target_slug}]
  key_links = [{op:"add", card_slug, canonical_key, relation, note_md?} |
               {op:"update", card_slug, canonical_key, relation,
                expected_revision, set:{note_md?}} |
               {op:"delete", card_slug, canonical_key, relation, expected_revision}]
  artifact_links = [{op:"add", artifact_slug, target_type, target_key,
                     relation, applicability_md?} |
                    {op:"delete", artifact_slug, target_type, target_key, relation}]

Minimal example:
  {"round_id":"r1","expected_revision":0,
   "expected_canonical_sha256":"0000000000000000000000000000000000000000000000000000000000000000",
   "cards":[{"op":"add","card":{"slug":"route-one","kind":"proof-route",
   "title":"Route one","summary_md":"Reusable summary.","disposition":"open",
   "next_test":"Check the boundary case.","facets":[]}}]}

Card optional fields: detail_md, claim_status, reason, next_test,
revival_condition, facets. Artifact metadata is read statically from the native
RESEARCH_ARTIFACT dict in source_path. Every array defaults to empty.
"""


def build_parser() -> argparse.ArgumentParser:
    parser = JSONArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    ensure = subparsers.add_parser("ensure", help="create or validate the one companion database")
    ensure.add_argument("canonical", type=Path)

    read = subparsers.add_parser("read", help="perform one bounded memory read")
    read.add_argument("canonical", type=Path)
    read.add_argument(
        "selector", choices=("meta", "keys", "key", "card", "artifact", "search", "all")
    )
    read.add_argument("value", nargs="?")
    read.add_argument("--facet", action="append", default=[])
    read.add_argument("--full", action="store_true")
    read.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    read.add_argument("--offset", type=int, default=0)
    read.add_argument("--body-offset", type=int, default=0)

    apply_parser = subparsers.add_parser(
        "apply",
        help="apply one optimistic JSON changeset from stdin",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=APPLY_HELP,
    )
    apply_parser.add_argument("canonical", type=Path)

    check = subparsers.add_parser("check", help="validate database integrity and freshness")
    check.add_argument("canonical", type=Path)
    return parser


def bounded_json_output(payload: Mapping[str, Any], command: str | None) -> tuple[dict[str, Any], str]:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    size = len(encoded.encode("utf-8"))
    if size <= MAX_JSON_OUTPUT_BYTES:
        return dict(payload), encoded
    fallback = {
        "ok": False,
        "command": command,
        "error": "JSON output exceeds the global budget; narrow the read or repair the database",
        "observed_bytes": size,
        "maximum_bytes": MAX_JSON_OUTPUT_BYTES,
    }
    return fallback, json.dumps(fallback, ensure_ascii=False, sort_keys=True)


def main(argv: Sequence[str] | None = None) -> int:
    command: str | None = None
    try:
        args = build_parser().parse_args(argv)
        command = args.command
        if command == "ensure":
            payload = command_ensure(args.canonical)
        elif command == "read":
            document = scan_canonical(args.canonical)
            payload = command_read(args, document)
        elif command == "apply":
            document = scan_canonical(args.canonical)
            if not document.memory_declared:
                raise ResearchMemoryError("canonical front matter does not declare research_memory")
            payload = apply_changeset(document, parse_json_input(sys.stdin.read()))
        else:
            payload = command_check(args.canonical)
        payload, encoded = bounded_json_output(payload, command)
        stream = sys.stdout if payload.get("ok") else sys.stderr
        print(encoded, file=stream)
        return 0 if payload.get("ok") else 1
    except (ResearchMemoryError, CanonicalSectionsError, OSError, sqlite3.DatabaseError) as error:
        payload = {"ok": False, "command": command, "error": str(error)}
        if isinstance(error, CanonicalSectionsError):
            payload["errors"] = [
                {
                    "category": "integrity",
                    "code": "canonical-contract",
                    "message": message,
                }
                for message in error.errors
            ]
        _, encoded = bounded_json_output(payload, command)
        print(encoded, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
