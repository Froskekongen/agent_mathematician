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
SECTIONS_SCRIPT = SCRIPT.with_name("canonical_sections.py")


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
        }
        value.update(changes)
        return value

    def set_keys(self, *keys: str, heading_line: int = 1) -> dict:
        expected = hashlib.sha256(self.canonical.read_bytes()).hexdigest()
        completed = subprocess.run(
            [
                sys.executable,
                str(SECTIONS_SCRIPT),
                "key-set",
                "--canonical",
                str(self.canonical),
                "--heading-line",
                str(heading_line),
                "--expected-canonical-sha256",
                expected,
                *[part for key in keys for part in ("--key", key)],
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return json.loads(completed.stdout)

    def apply(
        self,
        card_operations: list[dict] | None = None,
        edge_operations: list[dict] | None = None,
        origin_operations: list[dict] | None = None,
        canonical_item_operations: list[dict] | None = None,
        canonical_alias_operations: list[dict] | None = None,
        card_canonical_link_operations: list[dict] | None = None,
        *,
        expected_revision: int | None = None,
        expected_canonical_digest: str | None = None,
        round_id: str | None = None,
        batch_digest: str | None = None,
        canonical_digest: str | None = None,
        success: bool = True,
    ) -> tuple[dict, dict]:
        self.batch_number += 1
        expected = self.batch_number - 1 if expected_revision is None else expected_revision
        if expected_canonical_digest is None:
            with closing(sqlite3.connect(self.db)) as connection:
                expected_canonical_digest = connection.execute(
                    "SELECT canonical_sha256 FROM meta WHERE singleton = 1"
                ).fetchone()[0]
        batch = {
            "round_id": round_id or f"round-{self.batch_number}",
            "expected_database_revision": expected,
            "expected_canonical_digest": expected_canonical_digest,
            "canonical_digest": canonical_digest
            or hashlib.sha256(self.canonical.read_bytes()).hexdigest(),
            "card_operations": card_operations or [],
            "origin_operations": origin_operations or [],
            "edge_operations": edge_operations or [],
            "canonical_item_operations": canonical_item_operations or [],
            "canonical_alias_operations": canonical_alias_operations or [],
            "card_canonical_link_operations": card_canonical_link_operations or [],
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
            self.assertEqual(connection.execute("PRAGMA user_version").fetchone()[0], 3)
            self.assertEqual(connection.execute("PRAGMA journal_mode").fetchone()[0], "delete")
            self.assertEqual(meta[1], 3)
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

    def test_contract_is_deterministic_self_contained_and_needs_no_database(self) -> None:
        self.db.unlink()
        self.canonical.unlink()
        before = set(self.root.iterdir())
        runs = [
            subprocess.run(
                [sys.executable, str(SCRIPT), "contract"],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=False,
            )
            for _ in range(2)
        ]
        for completed in runs:
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(completed.stderr, "")
        self.assertEqual(runs[0].stdout, runs[1].stdout)
        self.assertEqual(set(self.root.iterdir()), before)

        contract = json.loads(runs[0].stdout)
        self.assertEqual(contract["schema_version"], 3)
        self.assertEqual(
            contract["locator"]["default_value"],
            {
                "path": "./<stem>.research.sqlite",
                "schema": 3,
                "optional_for_understanding": True,
            },
        )
        self.assertEqual(contract["locator"]["default_theory_slug"], "<stem>")
        self.assertEqual(
            contract["statuses"]["disposition"],
            ["open", "active", "parked", "rejected", "integrated"],
        )
        self.assertTrue(contract["statuses"]["claim_status"]["nullable"])
        self.assertEqual(
            contract["card"]["required_fields"],
            ["slug", "kind", "title", "summary_md", "disposition"],
        )
        self.assertEqual(
            contract["card"]["state_requirements"]["rejected"], ["reason"]
        )

        batch = contract["apply_batch"]
        self.assertEqual(
            batch["fields"],
            [
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
            ],
        )
        self.assertEqual(
            batch["digest_rule"],
            {
                "algorithm": "sha256",
                "encoding": "utf-8",
                "exclude_top_level_fields": ["batch_digest"],
                "json": {
                    "ensure_ascii": False,
                    "sort_keys": True,
                    "separators": [",", ":"],
                },
            },
        )
        operations = batch["operations"]
        self.assertEqual(
            operations["card"]["update"]["required_fields"],
            ["op", "slug", "expected_revision", "changes"],
        )
        self.assertEqual(
            operations["origin"]["delete"]["required_fields"],
            ["op", "card_slug", "source_locator", "source_slug", "source_digest"],
        )
        self.assertEqual(
            operations["edge"]["add"]["optional_fields"], ["note_md"]
        )

        help_result = subprocess.run(
            [sys.executable, str(SCRIPT), "--help"],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        self.assertIn("contract", help_result.stdout)

    def test_ensure_creates_reuses_and_requires_existing(self) -> None:
        canonical = self.root / "topic.v2.markdown"
        canonical.write_text("# Topic v2\n", encoding="utf-8")
        created = self.run_cli("ensure", "--canonical", str(canonical))
        database = self.root / "topic.v2.research.sqlite"
        self.assertTrue(created["created"])
        self.assertEqual(Path(created["database"]), database.resolve())
        self.assertEqual(created["theory"], "topic.v2")
        self.assertEqual(created["schema_version"], 3)

        before = database.read_bytes()
        reused = self.run_cli("ensure", "--canonical", str(canonical))
        self.assertFalse(reused["created"])
        self.assertEqual(reused["canonical_status"], "current")
        self.assertEqual(database.read_bytes(), before)

        canonical.write_text("# Topic v2\n\nEdited after consolidation.\n", encoding="utf-8")
        stale = self.run_cli("ensure", "--canonical", str(canonical))
        self.assertEqual(stale["canonical_status"], "requires_review")
        self.assertEqual(database.read_bytes(), before)

        missing = self.root / "located-but-missing.sqlite"
        refused = self.run_cli(
            "ensure",
            "--canonical",
            str(canonical),
            "--db",
            str(missing),
            "--require-existing",
            success=False,
        )
        self.assertIn("does not exist", refused["error"])
        self.assertFalse(missing.exists())

        mismatch = self.run_cli(
            "ensure",
            "--canonical",
            str(canonical),
            "--theory",
            "different-theory",
            success=False,
        )
        self.assertIn("theory", mismatch["error"])

        other_canonical = self.root / "other-owner.md"
        other_canonical.write_text("# Other owner\n", encoding="utf-8")
        home_before = self.db.read_bytes()
        owner_collision = self.run_cli(
            "ensure",
            "--canonical",
            str(other_canonical),
            "--db",
            str(self.db),
            "--require-existing",
            success=False,
        )
        self.assertIn("canonical identity conflict", owner_collision["error"])
        self.assertEqual(self.db.read_bytes(), home_before)

        collision_canonical = self.root / "collision.md"
        collision_canonical.write_text("# Collision\n", encoding="utf-8")
        collision_db = self.root / "collision.research.sqlite"
        collision_db.write_bytes(b"not a SQLite database")
        collision_before = collision_db.read_bytes()
        collision = self.run_cli(
            "ensure", "--canonical", str(collision_canonical), success=False
        )
        self.assertFalse(collision["ok"])
        self.assertEqual(collision_db.read_bytes(), collision_before)

        symlink_target = self.root / "symlink-target.md"
        symlink_target.write_text("# Symlink target\n", encoding="utf-8")
        symlink_canonical = self.root / "symlink.md"
        symlink_canonical.symlink_to(symlink_target)
        symlink_result = self.run_cli(
            "ensure", "--canonical", str(symlink_canonical), success=False
        )
        self.assertIn("symbolic link", symlink_result["error"])
        self.assertFalse((self.root / "symlink.research.sqlite").exists())
        self.assertFalse((self.root / "symlink-target.research.sqlite").exists())

        db_symlink_canonical = self.root / "db-symlink.md"
        db_symlink_canonical.write_text("# DB symlink\n", encoding="utf-8")
        db_symlink = self.root / "db-symlink.research.sqlite"
        db_symlink.symlink_to(self.db)
        db_symlink_result = self.run_cli(
            "ensure", "--canonical", str(db_symlink_canonical), success=False
        )
        self.assertIn("symbolic link", db_symlink_result["error"])

        sidecar_canonical = self.root / "sidecar.md"
        sidecar_canonical.write_text("# Sidecar collision\n", encoding="utf-8")
        sidecar_db = self.root / "sidecar.research.sqlite"
        Path(str(sidecar_db) + "-wal").touch()
        sidecar_result = self.run_cli(
            "ensure", "--canonical", str(sidecar_canonical), success=False
        )
        self.assertIn("sidecar", sidecar_result["error"])
        self.assertFalse(sidecar_db.exists())

    def test_relink_is_revision_checked_and_idempotent(self) -> None:
        old_canonical = self.canonical
        new_canonical = self.root / "renamed-theory.md"
        old_canonical.rename(new_canonical)
        before_cards = self.db.read_bytes()
        result = self.run_cli(
            "relink",
            "--db",
            str(self.db),
            "--canonical",
            str(new_canonical),
            "--expected-canonical",
            str(old_canonical),
            "--expected-database-revision",
            "0",
        )
        self.assertTrue(result["changed"])
        self.assertEqual(result["database_revision"], 1)
        self.assertEqual(result["canonical_status"], "current")

        retry = self.run_cli(
            "relink",
            "--db",
            str(self.db),
            "--canonical",
            str(new_canonical),
            "--expected-canonical",
            str(old_canonical),
            "--expected-database-revision",
            "0",
        )
        self.assertTrue(retry["idempotent_retry"])
        self.assertFalse(retry["changed"])
        self.assertEqual(retry["database_revision"], 1)

        ensured = self.run_cli(
            "ensure",
            "--canonical",
            str(new_canonical),
            "--db",
            str(self.db),
            "--theory",
            "sample-theory",
            "--require-existing",
        )
        self.assertFalse(ensured["created"])
        self.assertEqual(ensured["database_revision"], 1)
        self.assertNotEqual(self.db.read_bytes(), before_cards)

        another_canonical = self.root / "another.md"
        another_canonical.write_text("# Another\n", encoding="utf-8")
        wrong_revision = self.run_cli(
            "relink",
            "--db",
            str(self.db),
            "--canonical",
            str(another_canonical),
            "--expected-canonical",
            str(new_canonical),
            "--expected-database-revision",
            "0",
            success=False,
        )
        self.assertIn("revision conflict", wrong_revision["error"])

    def test_relink_preserves_digest_and_allows_old_document_to_remain(self) -> None:
        old_canonical = self.canonical
        new_canonical = self.root / "copied-and-edited.md"
        new_canonical.write_text("# Edited copy\n", encoding="utf-8")
        with closing(sqlite3.connect(self.db)) as connection:
            stored_digest = connection.execute(
                "SELECT canonical_sha256 FROM meta"
            ).fetchone()[0]

        result = self.run_cli(
            "relink",
            "--db",
            str(self.db),
            "--canonical",
            str(new_canonical),
            "--expected-canonical",
            str(old_canonical),
            "--expected-database-revision",
            "0",
        )
        self.assertTrue(old_canonical.is_file())
        self.assertTrue(result["changed"])
        self.assertEqual(result["canonical_status"], "requires_review")
        with closing(sqlite3.connect(self.db)) as connection:
            meta = connection.execute(
                "SELECT canonical_path, canonical_sha256, database_revision FROM meta"
            ).fetchone()
        self.assertEqual(meta[0], "copied-and-edited.md")
        self.assertEqual(meta[1], stored_digest)
        self.assertEqual(meta[2], 1)

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

    def test_semantic_crosswalk_exact_lookup_refresh_review_and_body_isolation(self) -> None:
        self.set_keys("implicit-young-evaluation", "endpoint-obstruction")
        first, _ = self.apply(
            [
                {
                    "op": "add",
                    "card": self.card(
                        "implicit-young-evaluation",
                        detail_md="only-in-private-detail: full symbolic derivation",
                    ),
                },
                {"op": "add", "card": self.card("endpoint-counterexample")},
            ],
            canonical_item_operations=[
                {
                    "op": "add",
                    "canonical_key": "implicit-young-evaluation",
                    "kind": "mechanism",
                    "title": "Implicit Young evaluation",
                },
                {
                    "op": "add",
                    "canonical_key": "endpoint-obstruction",
                    "kind": "obstruction",
                    "title": "Endpoint obstruction",
                },
            ],
            canonical_alias_operations=[
                {
                    "op": "add",
                    "alias": "IR-COMP-1",
                    "canonical_key": "implicit-young-evaluation",
                    "source_locator": "legacy-round-1",
                }
            ],
            card_canonical_link_operations=[
                {
                    "op": "add",
                    "card_slug": "implicit-young-evaluation",
                    "canonical_key": "implicit-young-evaluation",
                    "relation": "same-subject",
                },
                {
                    "op": "add",
                    "card_slug": "implicit-young-evaluation",
                    "canonical_key": "endpoint-obstruction",
                    "relation": "tests",
                },
                {
                    "op": "add",
                    "card_slug": "endpoint-counterexample",
                    "canonical_key": "implicit-young-evaluation",
                    "relation": "constrains",
                },
            ],
        )
        self.assertEqual(first["database_revision"], 1)

        lookup = self.run_cli(
            "lookup", "--db", str(self.db), "--canonical", "IR-COMP-1"
        )
        self.assertEqual(lookup["query"]["matched_as"], "alias")
        self.assertEqual(
            {card["slug"] for card in lookup["cards"]},
            {"implicit-young-evaluation", "endpoint-counterexample"},
        )
        self.assertTrue(all(all(link["status"].values()) for link in lookup["links"]))
        self.assertNotIn("detail_md", json.dumps(lookup))
        self.assertNotIn("only-in-private-detail", json.dumps(lookup))
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute(
                """
                UPDATE canonical_item SET fingerprint_version = 99
                WHERE canonical_key = 'implicit-young-evaluation'
                """
            )
            connection.commit()
        wrong_version = self.run_cli(
            "lookup",
            "--db",
            str(self.db),
            "--canonical",
            "implicit-young-evaluation",
        )
        self.assertFalse(wrong_version["canonical_items"][0]["section_match"])
        self.assertTrue(
            all(
                not link["status"]["canonical_item_section_match"]
                for link in wrong_version["links"]
            )
        )
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute(
                """
                UPDATE canonical_item SET fingerprint_version = 1
                WHERE canonical_key = 'implicit-young-evaluation'
                """
            )
            connection.commit()
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute("PRAGMA ignore_check_constraints=ON")
            connection.execute(
                """
                INSERT INTO card_canonical_link
                SELECT card_slug, canonical_key, 'same-subject', note_md,
                       reviewed_canonical_sha256, reviewed_section_sha256,
                       reviewed_card_revision, revision, created_at, updated_at
                FROM card_canonical_link
                WHERE card_slug = 'endpoint-counterexample'
                  AND canonical_key = 'implicit-young-evaluation'
                  AND relation = 'constrains'
                """
            )
            connection.commit()
        invalid_same_subject = self.run_cli(
            "check", "--db", str(self.db), success=False
        )
        self.assertTrue(
            any(
                "same-subject card canonical link has unequal" in error
                for error in invalid_same_subject["errors"]
            )
        )
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute(
                """
                DELETE FROM card_canonical_link
                WHERE card_slug = 'endpoint-counterexample'
                  AND canonical_key = 'implicit-young-evaluation'
                  AND relation = 'same-subject'
                """
            )
            connection.commit()
        private_search = self.run_cli(
            "search", "--db", str(self.db), "--text", "only-in-private-detail"
        )
        self.assertEqual(private_search["count"], 0)
        shown = self.run_cli(
            "show", "--db", str(self.db), "--slug", "implicit-young-evaluation"
        )
        self.assertIn("only-in-private-detail", shown["card"]["detail_md"])
        with closing(sqlite3.connect(self.db)) as connection:
            fingerprints = connection.execute(
                "SELECT DISTINCT indexed_section_sha256 FROM canonical_item"
            ).fetchall()
        self.assertEqual(len(fingerprints), 1)

        self.apply(
            [
                {
                    "op": "update",
                    "slug": "implicit-young-evaluation",
                    "expected_revision": 1,
                    "changes": {"title": "Refined Young evaluation route"},
                }
            ]
        )
        card_lookup = self.run_cli(
            "lookup", "--db", str(self.db), "--card", "implicit-young-evaluation"
        )
        self.assertTrue(
            all(
                not link["status"]["reviewed_card_revision_match"]
                for link in card_lookup["links"]
            )
        )

        self.canonical.write_text(
            self.canonical.read_text(encoding="utf-8")
            + "\nA strengthened endpoint calculation.\n",
            encoding="utf-8",
        )
        stale = self.run_cli(
            "lookup", "--db", str(self.db), "--canonical", "implicit-young-evaluation"
        )
        self.assertEqual(stale["canonical_status"], "requires_review")
        self.assertTrue(stale["cards"])
        self.assertTrue(
            all(not link["status"]["reviewed_document_match"] for link in stale["links"])
        )
        self.assertTrue(
            all(not link["status"]["reviewed_section_match"] for link in stale["links"])
        )

        self.apply(
            canonical_item_operations=[
                {
                    "op": "refresh",
                    "canonical_key": key,
                    "expected_revision": 1,
                }
                for key in ("implicit-young-evaluation", "endpoint-obstruction")
            ],
            card_canonical_link_operations=[
                {
                    "op": "review",
                    "card_slug": card_slug,
                    "canonical_key": canonical_key,
                    "relation": relation,
                    "expected_revision": 1,
                }
                for card_slug, canonical_key, relation in (
                    (
                        "implicit-young-evaluation",
                        "implicit-young-evaluation",
                        "same-subject",
                    ),
                    ("implicit-young-evaluation", "endpoint-obstruction", "tests"),
                    (
                        "endpoint-counterexample",
                        "implicit-young-evaluation",
                        "constrains",
                    ),
                )
            ],
        )
        reviewed = self.run_cli(
            "lookup", "--db", str(self.db), "--card", "implicit-young-evaluation"
        )
        self.assertEqual(reviewed["canonical_status"], "current")
        self.assertTrue(
            all(all(link["status"].values()) for link in reviewed["links"])
        )
        checked = self.run_cli("check", "--db", str(self.db))
        self.assertEqual(checked["crosswalk_status"]["stale_items"], [])
        self.assertEqual(checked["crosswalk_status"]["stale_links"], [])

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

    def test_canonical_key_allows_at_most_one_theory_qualification(self) -> None:
        rejected, _ = self.apply(
            canonical_item_operations=[
                {
                    "op": "add",
                    "canonical_key": "theory/subtheory/result",
                    "kind": "result",
                    "title": "Over-qualified result",
                }
            ],
            success=False,
        )
        self.assertIn("lowercase semantic kebab-case key", rejected["error"])

    def test_local_card_slugs_are_semantic_identifiers(self) -> None:
        rejected, _ = self.apply(
            [{"op": "add", "card": self.card("IR-COMP-1")}],
            success=False,
        )
        self.assertIn("card.slug must be a lowercase semantic", rejected["error"])

    def test_database_constraints_reject_invalid_origin_and_retry_metadata(self) -> None:
        self.apply([{"op": "add", "card": self.card("origin-target")}])
        with closing(sqlite3.connect(self.db)) as connection:
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    """
                    INSERT INTO card_origin (
                        card_slug, source_locator, source_slug,
                        source_digest, applicability_md
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        "origin-target",
                        "../foreign.research.sqlite",
                        "foreign-card",
                        "not-a-digest",
                        "The objects agree on the stated subcategory.",
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

        baseline_conflict, _ = self.apply(
            expected_revision=1,
            expected_canonical_digest=digest("not-the-stored-baseline"),
            success=False,
        )
        self.assertIn("canonical baseline conflict", baseline_conflict["error"])

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

        self.canonical.write_text("# Drift after committed batch\n", encoding="utf-8")
        drift_retry = self.run_cli(
            "apply", "--db", str(self.db), "--input", str(batch_path)
        )
        self.assertTrue(drift_retry["idempotent_retry"])
        self.canonical.unlink()
        missing_retry = self.run_cli(
            "apply", "--db", str(self.db), "--input", str(batch_path)
        )
        self.assertTrue(missing_retry["idempotent_retry"])

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
            "expected_canonical_digest": hashlib.sha256(
                foreign_canonical.read_bytes()
            ).hexdigest(),
            "canonical_digest": hashlib.sha256(foreign_canonical.read_bytes()).hexdigest(),
            "card_operations": [{"op": "add", "card": self.card("foreign-card")}],
            "origin_operations": [],
            "edge_operations": [],
            "canonical_item_operations": [],
            "canonical_alias_operations": [],
            "card_canonical_link_operations": [],
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
        export_error = self.run_cli("export", "--db", str(missing), success=False)
        self.assertIn("does not exist", export_error["error"])
        self.assertFalse(missing.exists())

    def test_cross_theory_snapshot_provenance(self) -> None:
        first_digest = digest("foreign-card-content")
        second_digest = digest("second-foreign-card-content")
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
                    ),
                }
            ],
            origin_operations=[
                {
                    "op": "add",
                    "card_slug": "local-snapshot",
                    "source_locator": "foreign.research.sqlite",
                    "source_slug": "foreign-card",
                    "source_digest": first_digest,
                    "applicability_md": "Map X to Y; hypothesis H remains unmatched.",
                },
                {
                    "op": "add",
                    "card_slug": "local-snapshot",
                    "source_locator": "other/foreign.research.sqlite",
                    "source_slug": "second-card",
                    "source_digest": second_digest,
                    "applicability_md": "Use only the compact case.",
                },
            ],
        )
        shown = self.run_cli("show", "--db", str(self.db), "--slug", "local-snapshot")
        self.assertEqual(len(shown["origins"]), 2)
        self.assertEqual(shown["origins"][0]["source_digest"], first_digest)
        self.assertEqual(shown["origins"][1]["source_digest"], second_digest)

    def test_origin_replacement_cascade_and_mixed_rollback(self) -> None:
        source_digest = digest("source-card")
        key = {
            "card_slug": "local-card",
            "source_locator": "../source.research.sqlite",
            "source_slug": "source-card",
            "source_digest": source_digest,
        }
        self.apply(
            [{"op": "add", "card": self.card("local-card")}],
            origin_operations=[
                {
                    "op": "add",
                    **key,
                    "applicability_md": "The hypotheses agree exactly.",
                }
            ],
        )
        self.apply(
            origin_operations=[
                {"op": "delete", **key},
                {
                    "op": "add",
                    **key,
                    "applicability_md": "Only the finite-dimensional case applies.",
                },
            ]
        )
        shown = self.run_cli("show", "--db", str(self.db), "--slug", "local-card")
        self.assertEqual(
            shown["origins"][0]["applicability_md"],
            "Only the finite-dimensional case applies.",
        )
        self.assertEqual(shown["card"]["revision"], 1)

        failed_replacement, _ = self.apply(
            origin_operations=[
                {"op": "delete", **key},
                {
                    "op": "add",
                    **key,
                    "applicability_md": "   ",
                },
            ],
            expected_revision=2,
            success=False,
        )
        self.assertIn("must not be empty", failed_replacement["error"])
        restored = self.run_cli(
            "show", "--db", str(self.db), "--slug", "local-card"
        )
        self.assertEqual(
            restored["origins"][0]["applicability_md"],
            "Only the finite-dimensional case applies.",
        )

        failed, _ = self.apply(
            [{"op": "add", "card": self.card("rolled-back-card")}],
            origin_operations=[
                {
                    "op": "add",
                    "card_slug": "rolled-back-card",
                    "source_locator": "source.research.sqlite",
                    "source_slug": "bad-source",
                    "source_digest": "invalid",
                    "applicability_md": "Would otherwise be useful.",
                }
            ],
            expected_revision=2,
            success=False,
        )
        self.assertIn("digest", failed["error"])
        with closing(sqlite3.connect(self.db)) as connection:
            self.assertEqual(
                connection.execute(
                    "SELECT count(*) FROM card WHERE slug = 'rolled-back-card'"
                ).fetchone()[0],
                0,
            )
            self.assertEqual(
                connection.execute("SELECT database_revision FROM meta").fetchone()[0],
                2,
            )

        self.apply(
            [{"op": "delete", "slug": "local-card", "expected_revision": 1}],
            expected_revision=2,
        )
        with closing(sqlite3.connect(self.db)) as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM card_origin").fetchone()[0], 0)

    def test_export_is_complete_deterministic_and_read_only(self) -> None:
        source_digest = digest("export-source")
        self.canonical.write_text(
            '<a id="research-key--omega-result"></a>\n\n'
            '# Théorie\n'
            '**Research key:** `omega-result`\n\n'
            'Canonical α.\n',
            encoding="utf-8",
        )
        self.apply(
            [
                {"op": "add", "card": self.card("zeta")},
                {
                    "op": "add",
                    "card": self.card(
                        "alpha",
                        disposition="rejected",
                        next_test=None,
                        reason="Rejected after an exact obstruction.",
                    ),
                },
                {
                    "op": "add",
                    "card": self.card("beta", disposition="active"),
                },
                {
                    "op": "add",
                    "card": self.card(
                        "gamma",
                        disposition="parked",
                        next_test=None,
                        revival_condition="A uniform estimate becomes available.",
                    ),
                },
                {
                    "op": "add",
                    "card": self.card(
                        "omega",
                        disposition="integrated",
                        next_test=None,
                    ),
                },
            ],
            [
                {
                    "op": "add",
                    "source_slug": "zeta",
                    "relation": "depends_on",
                    "target_slug": "alpha",
                    "note_md": "Unicode edge λ.",
                }
            ],
            origin_operations=[
                {
                    "op": "add",
                    "card_slug": "zeta",
                    "source_locator": "source.research.sqlite",
                    "source_slug": "source-zeta",
                    "source_digest": source_digest,
                    "applicability_md": "First line.\n\nSecond line with ∀ε.",
                }
            ],
            canonical_item_operations=[
                {
                    "op": "add",
                    "canonical_key": "omega-result",
                    "kind": "result",
                    "title": "Omega result",
                }
            ],
            card_canonical_link_operations=[
                {
                    "op": "add",
                    "card_slug": "omega",
                    "canonical_key": "omega-result",
                    "relation": "integrated-at",
                }
            ],
        )
        before = self.db.read_bytes()
        first = self.run_cli("export", "--db", str(self.db))
        second = self.run_cli("export", "--db", str(self.db))
        self.assertEqual(first, second)
        self.assertEqual(self.db.read_bytes(), before)
        self.assertEqual(
            [card["slug"] for card in first["cards"]],
            ["alpha", "beta", "gamma", "omega", "zeta"],
        )
        self.assertEqual(
            {card["disposition"] for card in first["cards"]},
            {"open", "active", "parked", "rejected", "integrated"},
        )
        self.assertEqual(first["origins"][0]["source_digest"], source_digest)
        self.assertEqual(first["edges"][0]["note_md"], "Unicode edge λ.")
        semantic_export = {
            key: first[key]
            for key in (
                "meta",
                "cards",
                "card_bodies",
                "origins",
                "edges",
                "canonical_items",
                "canonical_aliases",
                "card_canonical_links",
            )
        }
        self.assertEqual(first["export_digest"], batch_content_digest(semantic_export))

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
        self.assertTrue(any("unexpected schema-v3 table" in error for error in result["errors"]))
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute("DROP TABLE hidden_ledger")
            connection.execute("ALTER TABLE card ADD COLUMN legacy_marker TEXT")
            connection.commit()
        result = self.run_cli("check", "--db", str(self.db), success=False)
        self.assertTrue(
            any("unexpected schema-v3 column" in error for error in result["errors"])
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

    def test_schema_definition_and_null_slug_are_enforced(self) -> None:
        with closing(sqlite3.connect(self.db)) as connection:
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    """
                    INSERT INTO card (
                        slug, kind, title, summary_md, disposition, next_test,
                        revision, content_sha256, created_at, updated_at
                    ) VALUES (NULL, 'direction', 'Null slug', 'Summary', 'open',
                              'Next test', 1, ?, '2026-08-28T00:00:00Z',
                              '2026-08-28T00:00:00Z')
                    """,
                    (digest("null slug"),),
                )

            definition = connection.execute(
                "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'card'"
            ).fetchone()[0]
            weakened = definition.replace(
                "slug TEXT PRIMARY KEY NOT NULL CHECK",
                "slug TEXT PRIMARY KEY CHECK",
            )
            self.assertNotEqual(weakened, definition)
            schema_version = connection.execute("PRAGMA schema_version").fetchone()[0]
            connection.execute("PRAGMA writable_schema=ON")
            connection.execute(
                "UPDATE sqlite_master SET sql = ? WHERE type = 'table' AND name = 'card'",
                (weakened,),
            )
            connection.execute("PRAGMA writable_schema=OFF")
            connection.execute(f"PRAGMA schema_version={schema_version + 1}")
            connection.commit()

        result = self.run_cli("check", "--db", str(self.db), success=False)
        self.assertTrue(any("definition mismatch" in error for error in result["errors"]))
        ensured = self.run_cli(
            "ensure",
            "--canonical",
            str(self.canonical),
            "--db",
            str(self.db),
            "--require-existing",
            success=False,
        )
        self.assertIn("definition mismatch", ensured["error"])

        replacement = self.root / "replacement.md"
        replacement.write_text("# Replacement\n", encoding="utf-8")
        with closing(sqlite3.connect(self.db)) as connection:
            before_meta = connection.execute(
                "SELECT canonical_path, database_revision FROM meta"
            ).fetchone()
        relinked = self.run_cli(
            "relink",
            "--db",
            str(self.db),
            "--canonical",
            str(replacement),
            "--expected-canonical",
            str(self.canonical),
            "--expected-database-revision",
            "0",
            success=False,
        )
        self.assertIn("definition mismatch", relinked["error"])
        with closing(sqlite3.connect(self.db)) as connection:
            after_meta = connection.execute(
                "SELECT canonical_path, database_revision FROM meta"
            ).fetchone()
        self.assertEqual(after_meta, before_meta)

    def test_unsupported_schema_version_is_rejected(self) -> None:
        for unsupported in (0, 1, 2, 99):
            with closing(sqlite3.connect(self.db)) as connection:
                connection.execute(f"PRAGMA user_version={unsupported}")
                connection.commit()
            result = self.run_cli("check", "--db", str(self.db), success=False)
            self.assertTrue(
                any("expected 3" in error for error in result["errors"]),
                unsupported,
            )
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute("PRAGMA user_version=3")
            connection.commit()

    def test_check_emits_json_for_missing_card_column_with_rows(self) -> None:
        self.apply([{"op": "add", "card": self.card("surviving-row")}])
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute(
                """
                CREATE TABLE card_without_title AS
                SELECT slug, kind, summary_md, disposition,
                       claim_status, reason, next_test, revival_condition,
                       revision, content_sha256, created_at, updated_at
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
            "consolidate-math-documents",
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

        consolidate = (
            skills_root / "consolidate-math-documents" / "SKILL.md"
        ).read_text(encoding="utf-8")
        consolidate_flat = " ".join(consolidate.split())
        self.assertIn("disable-model-invocation: true", consolidate)
        for required in (
            "read-only",
            "new target",
            "Preview",
            "same-theory unification",
            "cross-theory synthesis",
            "retirement manifest",
            "discard-with-source",
            "unresolved-conflict",
            "card_origin",
            "source-retirement",
        ):
            self.assertIn(required, consolidate_flat)
        self.assertNotIn("`source-only`", consolidate)

        protocol = (
            skills_root
            / "research-mathematics"
            / "references"
            / "research-memory.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Schema 3 is the only supported", protocol)
        self.assertIn("`contract`", protocol)
        self.assertIn("canonical_sections.py", protocol)
        self.assertIn("semantic research key", protocol)
        self.assertIn("exact `lookup`", protocol)
        self.assertIn("card_origin", protocol)
        self.assertNotIn("origin_uri", protocol)
        self.assertNotIn("origin_digest", protocol)

        retirement = (
            skills_root
            / "consolidate-math-documents"
            / "references"
            / "source-retirement.md"
        ).read_text(encoding="utf-8")
        for required in (
            "tracked",
            "clean",
            "unstaged",
            "partial",
            "retire_sources.py",
        ):
            self.assertIn(required, retirement)

        # Guard the two shared hot paths against instruction sediment.
        self.assertLessEqual(len(protocol.split()), 2100)
        self.assertLessEqual(len(consolidate.split()), 1200)
        database_aware_words = len(protocol.split()) + sum(
            len((skills_root / name / "SKILL.md").read_text(encoding="utf-8").split())
            for name in participating
        )
        self.assertLessEqual(database_aware_words, 9000)

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
        self.assertEqual(len(module.SKILL_NAMES), 8)
        self.assertIn("consolidate-math-documents", module.SKILL_NAMES)

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
            self.assertTrue(
                (destination / "consolidate-math-documents" / "SKILL.md").is_file()
            )
            self.assertTrue(
                (
                    destination
                    / "consolidate-math-documents"
                    / "references"
                    / "source-retirement.md"
                ).is_file()
            )
            self.assertTrue(
                (
                    destination
                    / "consolidate-math-documents"
                    / "scripts"
                    / "retire_sources.py"
                ).is_file()
            )
            self.assertFalse(obsolete.exists())
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "preserve")


if __name__ == "__main__":
    unittest.main()
