from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parents[2]
MATHEMATICIAN_ROOT = REPO_ROOT / "mathematician"
SCRIPT = (
    MATHEMATICIAN_ROOT
    / "skills"
    / "research-mathematics"
    / "scripts"
    / "research_memory.py"
)


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def batch_content_digest(batch: dict) -> str:
    content = {key: value for key, value in batch.items() if key != "batch_digest"}
    encoded = json.dumps(
        content, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class ResearchMemoryCLITest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.canonical = self.root / "theory.md"
        self.canonical.write_text("# Théorie\n\nCanonical α.\n", encoding="utf-8")
        self.db = self.root / "theory.research.sqlite"
        self.run_cli(
            "init",
            "--canonical",
            str(self.canonical),
            "--theory",
            "sample-theory",
        )
        self.batch_number = 0

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_cli(self, *arguments: str, success: bool = True) -> dict:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if success:
            self.assertEqual(completed.returncode, 0, completed.stderr)
            output = completed.stdout
        else:
            self.assertNotEqual(completed.returncode, 0, completed.stdout)
            output = completed.stderr or completed.stdout
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            self.fail(f"CLI did not emit JSON: stdout={completed.stdout!r}, stderr={completed.stderr!r}")

    def card(self, slug: str, **changes: object) -> dict:
        value = {
            "slug": slug,
            "kind": "direction",
            "title": slug.replace("-", " ").title(),
            "summary_md": f"Self-contained summary for **{slug}**.",
            "detail_md": None,
            "disposition": "open",
            "claim_status": "unresolved",
            "reason": None,
            "next_test": "Run the next discriminating calculation.",
            "revival_condition": None,
            "canonical_anchor": None,
            "origin_uri": None,
            "origin_digest": None,
        }
        value.update(changes)
        return value

    def apply(
        self,
        card_operations: list[dict] | None = None,
        edge_operations: list[dict] | None = None,
        *,
        expected_revision: int | None = None,
        round_id: str | None = None,
        batch_digest: str | None = None,
        canonical_digest: str | None = None,
        success: bool = True,
    ) -> tuple[dict, dict]:
        self.batch_number += 1
        expected = self.batch_number - 1 if expected_revision is None else expected_revision
        batch = {
            "round_id": round_id or f"round-{self.batch_number}",
            "expected_database_revision": expected,
            "canonical_digest": canonical_digest
            or hashlib.sha256(self.canonical.read_bytes()).hexdigest(),
            "card_operations": card_operations or [],
            "edge_operations": edge_operations or [],
        }
        batch["batch_digest"] = batch_digest or batch_content_digest(batch)
        batch_path = self.root / f"batch-{self.batch_number}.json"
        batch_path.write_text(json.dumps(batch, ensure_ascii=False), encoding="utf-8")
        result = self.run_cli(
            "apply", "--db", str(self.db), "--input", str(batch_path), success=success
        )
        return result, batch

    def test_init_default_metadata_and_overwrite_refusal(self) -> None:
        with closing(sqlite3.connect(self.db)) as connection:
            meta = connection.execute("SELECT * FROM meta").fetchone()
            self.assertEqual(connection.execute("PRAGMA user_version").fetchone()[0], 1)
            self.assertEqual(connection.execute("PRAGMA journal_mode").fetchone()[0], "delete")
            self.assertEqual(meta[1], 1)
            self.assertEqual(meta[2], "sample-theory")
            self.assertEqual(meta[3], "theory.md")
            self.assertEqual(meta[5], 0)
        result = self.run_cli(
            "init",
            "--canonical",
            str(self.canonical),
            "--theory",
            "again",
            success=False,
        )
        self.assertIn("refusing to overwrite", result["error"])

        dangling = self.root / "dangling.sqlite"
        dangling.symlink_to(self.root / "missing-target.sqlite")
        result = self.run_cli(
            "init",
            "--canonical",
            str(self.canonical),
            "--theory",
            "dangling",
            "--db",
            str(dangling),
            success=False,
        )
        self.assertIn("refusing to overwrite", result["error"])
        self.assertFalse((self.root / "missing-target.sqlite").exists())

    def test_argument_errors_are_json(self) -> None:
        result = self.run_cli("init", "--canonical", str(self.canonical), success=False)
        self.assertFalse(result["ok"])
        self.assertIn("required", result["error"])

    def test_add_show_unicode_multiline_and_edges(self) -> None:
        first = self.card(
            "unicode-route",
            title="Route λ",
            summary_md="First line.\r\n\r\nSecond line with ∀ε.",
        )
        second = self.card(
            "known-obstruction",
            kind="obstruction",
            disposition="rejected",
            claim_status="supported",
            next_test=None,
            reason="The boundary case contradicts the proposed estimate.",
        )
        result, _ = self.apply(
            [
                {"op": "add", "card": first},
                {"op": "add", "card": second},
            ],
            [
                {
                    "op": "add",
                    "source_slug": "unicode-route",
                    "relation": "blocked_by",
                    "target_slug": "known-obstruction",
                    "note_md": "Use at β = 0.",
                }
            ],
        )
        self.assertEqual(result["database_revision"], 1)
        shown = self.run_cli("show", "--db", str(self.db), "--slug", "unicode-route")
        self.assertEqual(shown["card"]["title"], "Route λ")
        self.assertEqual(shown["card"]["summary_md"], "First line.\n\nSecond line with ∀ε.")
        self.assertEqual(shown["outgoing_edges"][0]["target_slug"], "known-obstruction")
        self.assertNotEqual(shown["card"]["content_sha256"], digest(""))

    def test_state_constraints_and_status_axes_are_independent(self) -> None:
        invalid_cards = [
            self.card("open-no-test", next_test=None),
            self.card(
                "parked-no-revival", disposition="parked", next_test=None
            ),
            self.card(
                "rejected-no-reason", disposition="rejected", next_test=None
            ),
            self.card(
                "integrated-no-anchor", disposition="integrated", next_test=None
            ),
        ]
        for index, card in enumerate(invalid_cards):
            with self.subTest(card=card["slug"]):
                result, _ = self.apply(
                    [{"op": "add", "card": card}],
                    expected_revision=0,
                    round_id=f"invalid-{index}",
                    success=False,
                )
                self.assertIn("require", result["error"])
        result, _ = self.apply(
            [
                {
                    "op": "add",
                    "card": self.card(
                        "refuted-open",
                        disposition="open",
                        claim_status="refuted",
                    ),
                },
                {
                    "op": "add",
                    "card": self.card(
                        "supported-rejected",
                        disposition="rejected",
                        claim_status="supported",
                        next_test=None,
                        reason="This route is too costly, though the lemma remains supported.",
                    ),
                },
            ],
            expected_revision=0,
            round_id="valid-independent-axes",
        )
        self.assertEqual(result["database_revision"], 1)

    def test_database_constraints_reject_partial_origin_and_retry_metadata(self) -> None:
        card = self.card("origin-must-be-paired")
        with closing(sqlite3.connect(self.db)) as connection:
            columns = list(card)
            values = [card[column] for column in columns]
            card_hash = digest("irrelevant-but-valid")
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    f"""
                    INSERT INTO card ({', '.join(columns)}, revision, content_sha256,
                                      created_at, updated_at)
                    VALUES ({', '.join('?' for _ in columns)}, 1, ?, ?, ?)
                    """,
                    (
                        *values[:-2],
                        "file:///foreign.sqlite#card",
                        None,
                        card_hash,
                        "2026-01-01T00:00:00Z",
                        "2026-01-01T00:00:00Z",
                    ),
                )
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    "UPDATE meta SET last_round_id = 'partial', last_batch_digest = NULL"
                )

    def test_update_delete_revision_checks_and_edge_cascade(self) -> None:
        self.apply(
            [
                {"op": "add", "card": self.card("source")},
                {"op": "add", "card": self.card("target")},
            ],
            [
                {
                    "op": "add",
                    "source_slug": "source",
                    "relation": "depends_on",
                    "target_slug": "target",
                }
            ],
        )
        result, _ = self.apply(
            [
                {
                    "op": "update",
                    "slug": "source",
                    "expected_revision": 1,
                    "changes": {"title": "Updated source"},
                }
            ]
        )
        self.assertEqual(result["database_revision"], 2)
        stale, _ = self.apply(
            [
                {
                    "op": "delete",
                    "slug": "source",
                    "expected_revision": 1,
                }
            ],
            expected_revision=2,
            success=False,
        )
        self.assertIn("revision conflict", stale["error"])
        self.apply(
            [
                {
                    "op": "delete",
                    "slug": "source",
                    "expected_revision": 2,
                }
            ],
            expected_revision=2,
        )
        with closing(sqlite3.connect(self.db)) as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM edge").fetchone()[0], 0)

    def test_mixed_batch_rolls_back_completely(self) -> None:
        result, _ = self.apply(
            [
                {"op": "add", "card": self.card("would-have-worked")},
                {"op": "add", "card": self.card("bad", next_test=None)},
            ],
            expected_revision=0,
            success=False,
        )
        self.assertIn("require", result["error"])
        with closing(sqlite3.connect(self.db)) as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM card").fetchone()[0], 0)
            self.assertEqual(connection.execute("SELECT database_revision FROM meta").fetchone()[0], 0)

    def test_database_and_canonical_revision_conflicts(self) -> None:
        self.apply([{"op": "add", "card": self.card("first")}])
        database_conflict, _ = self.apply(
            expected_revision=0, success=False
        )
        self.assertIn("database revision conflict", database_conflict["error"])

        self.canonical.write_text("# Changed\n", encoding="utf-8")
        canonical_conflict, _ = self.apply(
            expected_revision=1,
            canonical_digest=digest("not the document"),
            success=False,
        )
        self.assertIn("canonical digest conflict", canonical_conflict["error"])

    def test_immediate_retry_is_idempotent_and_changed_reuse_fails(self) -> None:
        first, batch = self.apply([{"op": "add", "card": self.card("once")}])
        batch_path = self.root / "retry.json"
        batch_path.write_text(json.dumps(batch), encoding="utf-8")
        retry = self.run_cli(
            "apply", "--db", str(self.db), "--input", str(batch_path)
        )
        self.assertTrue(retry["idempotent_retry"])
        self.assertEqual(retry["database_revision"], first["database_revision"])

        changed_with_reused_digest = dict(batch)
        changed_with_reused_digest["card_operations"] = []
        batch_path.write_text(json.dumps(changed_with_reused_digest), encoding="utf-8")
        invalid_digest = self.run_cli(
            "apply", "--db", str(self.db), "--input", str(batch_path), success=False
        )
        self.assertIn("does not match", invalid_digest["error"])

        batch["card_operations"] = []
        batch["batch_digest"] = batch_content_digest(batch)
        batch_path.write_text(json.dumps(batch), encoding="utf-8")
        changed = self.run_cli(
            "apply", "--db", str(self.db), "--input", str(batch_path), success=False
        )
        self.assertIn("different content", changed["error"])
        with closing(sqlite3.connect(self.db)) as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM card").fetchone()[0], 1)

    def test_search_defaults_explicit_rejected_kind_and_literal_text(self) -> None:
        self.apply(
            [
                {"op": "add", "card": self.card("active", disposition="active")},
                {
                    "op": "add",
                    "card": self.card(
                        "parked",
                        disposition="parked",
                        next_test=None,
                        revival_condition="A sharper bound becomes available.",
                    ),
                },
                {
                    "op": "add",
                    "card": self.card(
                        "rejected-percent",
                        kind="obstruction",
                        summary_md="The 100% endpoint breaks the estimate.",
                        disposition="rejected",
                        next_test=None,
                        reason="Explicit counterexample.",
                    ),
                },
                {"op": "add", "card": self.card("older-open")},
                {"op": "add", "card": self.card("newer-open")},
            ]
        )
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute(
                "UPDATE card SET updated_at = '2025-01-01T00:00:00Z' WHERE slug = 'older-open'"
            )
            connection.execute(
                "UPDATE card SET updated_at = '2026-01-01T00:00:00Z' WHERE slug = 'newer-open'"
            )
            connection.commit()
        default = self.run_cli("search", "--db", str(self.db))
        self.assertEqual(
            [card["slug"] for card in default["cards"]],
            ["active", "newer-open", "older-open", "parked"],
        )
        rejected = self.run_cli(
            "search",
            "--db",
            str(self.db),
            "--state",
            "rejected",
            "--kind",
            "obstruction",
            "--text",
            "100%",
        )
        self.assertEqual(rejected["count"], 1)
        self.assertNotIn("detail_md", rejected["cards"][0])
        self.assertEqual(rejected["cards"][0]["theory"], "sample-theory")

    def test_multi_database_search_is_read_only_and_missing_db_is_not_created(self) -> None:
        self.apply([{"op": "add", "card": self.card("home-card")}])
        foreign_dir = self.root / "foreign"
        foreign_dir.mkdir()
        foreign_canonical = foreign_dir / "foreign.md"
        foreign_canonical.write_text("# Foreign\n", encoding="utf-8")
        foreign_db = foreign_dir / "foreign.research.sqlite"
        self.run_cli(
            "init",
            "--canonical",
            str(foreign_canonical),
            "--theory",
            "foreign-theory",
            "--db",
            str(foreign_db),
        )
        foreign_batch = {
            "round_id": "foreign-round",
            "expected_database_revision": 0,
            "canonical_digest": hashlib.sha256(foreign_canonical.read_bytes()).hexdigest(),
            "card_operations": [{"op": "add", "card": self.card("foreign-card")}],
            "edge_operations": [],
        }
        foreign_batch["batch_digest"] = batch_content_digest(foreign_batch)
        foreign_batch_path = foreign_dir / "batch.json"
        foreign_batch_path.write_text(json.dumps(foreign_batch), encoding="utf-8")
        self.run_cli(
            "apply", "--db", str(foreign_db), "--input", str(foreign_batch_path)
        )
        before = foreign_db.read_bytes()
        result = self.run_cli(
            "search", "--db", str(self.db), "--db", str(foreign_db)
        )
        self.assertEqual({card["slug"] for card in result["cards"]}, {"home-card", "foreign-card"})
        self.assertEqual(foreign_db.read_bytes(), before)

        missing = self.root / "missing.sqlite"
        error = self.run_cli("search", "--db", str(missing), success=False)
        self.assertIn("does not exist", error["error"])
        self.assertFalse(missing.exists())

    def test_cross_theory_snapshot_provenance(self) -> None:
        origin = (self.root / "foreign.research.sqlite").resolve().as_uri() + "#foreign-card"
        origin_digest = digest("foreign-card-content")
        self.apply(
            [
                {
                    "op": "add",
                    "card": self.card(
                        "local-snapshot",
                        kind="source-applicability",
                        detail_md=(
                            "Map foreign object X to local Y; hypothesis H remains unmatched."
                        ),
                        origin_uri=origin,
                        origin_digest=origin_digest,
                    ),
                }
            ]
        )
        shown = self.run_cli("show", "--db", str(self.db), "--slug", "local-snapshot")
        self.assertEqual(shown["card"]["origin_uri"], origin)
        self.assertEqual(shown["card"]["origin_digest"], origin_digest)

    def test_check_reports_staleness_without_invalidating_database(self) -> None:
        current = self.run_cli("check", "--db", str(self.db))
        self.assertTrue(current["ok"])
        self.assertEqual(current["canonical_status"], "current")
        self.canonical.write_text("# Later canonical edit\n", encoding="utf-8")
        stale = self.run_cli("check", "--db", str(self.db))
        self.assertTrue(stale["ok"])
        self.assertEqual(stale["canonical_status"], "requires_review")
        self.assertTrue(stale["warnings"])

    def test_check_detects_integrity_failures_and_wal_sidecars(self) -> None:
        self.apply([{"op": "add", "card": self.card("tampered")}])
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute(
                "UPDATE card SET content_sha256 = ? WHERE slug = 'tampered'", (digest("wrong"),)
            )
            connection.commit()
        result = self.run_cli("check", "--db", str(self.db), success=False)
        self.assertTrue(any("stale content digest" in error for error in result["errors"]))

        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute(
                "INSERT INTO edge (source_slug, relation, target_slug) VALUES (?, ?, ?)",
                ("tampered", "points_to", "missing-card"),
            )
            connection.commit()
        foreign_key_result = self.run_cli("check", "--db", str(self.db), success=False)
        self.assertTrue(
            any("foreign_key_check" in error for error in foreign_key_result["errors"])
        )
        sidecars = [Path(str(self.db) + suffix) for suffix in ("-journal", "-wal", "-shm")]
        for sidecar in sidecars:
            sidecar.touch()
        result = self.run_cli("check", "--db", str(self.db), success=False)
        self.assertTrue(any("sidecar" in error for error in result["errors"]))
        for sidecar in sidecars:
            self.assertTrue(sidecar.exists())

    def test_check_validates_required_schema_shape(self) -> None:
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute("CREATE TABLE hidden_ledger (entry TEXT)")
            connection.commit()
        result = self.run_cli("check", "--db", str(self.db), success=False)
        self.assertTrue(any("unexpected schema-v1 table" in error for error in result["errors"]))
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute("DROP TABLE hidden_ledger")
            connection.execute("ALTER TABLE card ADD COLUMN legacy_marker TEXT")
            connection.commit()
        result = self.run_cli("check", "--db", str(self.db), success=False)
        self.assertTrue(
            any("unexpected schema-v1 column" in error for error in result["errors"])
        )
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute("DROP TABLE edge")
            connection.commit()
        result = self.run_cli("check", "--db", str(self.db), success=False)
        self.assertTrue(any("missing required table" in error for error in result["errors"]))
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute(
                """
                CREATE TABLE edge (
                    source_slug TEXT NOT NULL,
                    relation TEXT NOT NULL,
                    target_slug TEXT NOT NULL,
                    note_md TEXT,
                    PRIMARY KEY (source_slug, relation, target_slug)
                )
                """
            )
            connection.commit()
        result = self.run_cli("check", "--db", str(self.db), success=False)
        self.assertTrue(
            any("cascading foreign key" in error for error in result["errors"])
        )

    def test_check_emits_json_for_missing_card_column_with_rows(self) -> None:
        self.apply([{"op": "add", "card": self.card("surviving-row")}])
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute(
                """
                CREATE TABLE card_without_title AS
                SELECT slug, kind, summary_md, detail_md, disposition,
                       claim_status, reason, next_test, revival_condition,
                       canonical_anchor, origin_uri, origin_digest, revision,
                       content_sha256, created_at, updated_at
                FROM card
                """
            )
            connection.execute("DROP TABLE card")
            connection.execute("ALTER TABLE card_without_title RENAME TO card")
            connection.commit()

        result = self.run_cli("check", "--db", str(self.db), success=False)
        self.assertTrue(any("missing column(s): title" in error for error in result["errors"]))
        self.assertTrue(any("database validation failed" in error for error in result["errors"]))

    def test_successful_operations_leave_no_wal_or_shm(self) -> None:
        self.apply([{"op": "add", "card": self.card("clean-journal")}])
        self.run_cli("search", "--db", str(self.db))
        self.run_cli("show", "--db", str(self.db), "--slug", "clean-journal")
        self.run_cli("check", "--db", str(self.db))
        self.assertFalse(Path(str(self.db) + "-journal").exists())
        self.assertFalse(Path(str(self.db) + "-wal").exists())
        self.assertFalse(Path(str(self.db) + "-shm").exists())


class SuiteStructureTest(unittest.TestCase):
    def test_research_memory_role_structure_without_yaml_dependency(self) -> None:
        skills_root = MATHEMATICIAN_ROOT / "skills"
        participating = (
            "research-mathematics",
            "explore-mathematical-structure",
            "explore-proof-strategies",
            "destroy-theory",
            "audit-assumptions",
        )
        for name in participating:
            text = (skills_root / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("research-memory", text, name)

        formalize = (skills_root / "formalize-concepts" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("research-memory", formalize)
        self.assertNotIn("research_memory.py", formalize)
        self.assertNotIn(".research.sqlite", formalize)

        explain = (skills_root / "explain-mathematics" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("queried read-only", explain)
        self.assertIn("never initialize or write", explain)

        obsolete = (
            skills_root
            / "explore-mathematical-structure"
            / "references"
            / "exploration-ledger.md"
        )
        self.assertFalse(obsolete.exists())
        for document in skills_root.rglob("*.md"):
            self.assertNotIn(
                "exploration-ledger.md",
                document.read_text(encoding="utf-8"),
                str(document),
            )

        for metadata in skills_root.glob("*/agents/openai.yaml"):
            self.assertIn(
                "allow_implicit_invocation: false",
                metadata.read_text(encoding="utf-8"),
                str(metadata),
            )

    def test_relative_markdown_links_exist(self) -> None:
        link_pattern = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
        failures: list[str] = []
        for document in sorted((MATHEMATICIAN_ROOT / "skills").rglob("*.md")):
            for raw_link in link_pattern.findall(document.read_text(encoding="utf-8")):
                link = raw_link.strip().split(maxsplit=1)[0].strip("<>")
                if not link or link.startswith(("#", "http://", "https://", "mailto:")):
                    continue
                target = unquote(link.split("#", 1)[0])
                if not (document.parent / target).resolve().is_file():
                    failures.append(f"{document.relative_to(REPO_ROOT)} -> {target}")
        self.assertEqual(failures, [], "missing relative links:\n" + "\n".join(failures))

    def test_installer_copies_shared_resources_and_removes_only_obsolete_file(self) -> None:
        specification = importlib.util.spec_from_file_location(
            "install_skills", MATHEMATICIAN_ROOT / "install_skills.py"
        )
        self.assertIsNotNone(specification)
        self.assertIsNotNone(specification.loader)
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "skills"
            reference_dir = (
                destination / "explore-mathematical-structure" / "references"
            )
            reference_dir.mkdir(parents=True)
            obsolete = reference_dir / "exploration-ledger.md"
            sentinel = reference_dir / "user-notes.md"
            obsolete.write_text("obsolete", encoding="utf-8")
            sentinel.write_text("preserve", encoding="utf-8")

            module.install(MATHEMATICIAN_ROOT / "skills", destination, dry_run=False)

            installed_research = destination / "research-mathematics"
            self.assertTrue((installed_research / "scripts" / "research_memory.py").is_file())
            self.assertTrue((installed_research / "references" / "research-memory.md").is_file())
            self.assertFalse(obsolete.exists())
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "preserve")


if __name__ == "__main__":
    unittest.main()
