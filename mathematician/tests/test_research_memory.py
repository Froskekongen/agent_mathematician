from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    REPO_ROOT
    / "mathematician"
    / "skills"
    / "research-mathematics"
    / "scripts"
    / "research_memory.py"
)
sys.path.insert(0, str(SCRIPT.parent))
import research_memory as memory  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ResearchMemoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / ".git").mkdir()
        self.canonical = self.root / "theory.md"
        self.database = self.root / "theory.research.sqlite"
        self.body = """# Main theorem

**Research key:** `main-theorem`

The initial statement.

## Boundary case

**Research key:** `boundary-case`

The boundary statement.
"""

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_cli(
        self, *arguments: str, input_value: object | None = None, success: bool = True
    ) -> dict:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            cwd=REPO_ROOT,
            input=(json.dumps(input_value) if input_value is not None else None),
            capture_output=True,
            text=True,
            check=False,
        )
        output = completed.stdout or completed.stderr
        self.assertEqual(completed.returncode == 0, success, output)
        self.assertTrue(output, completed)
        return json.loads(output)

    def bootstrap(self) -> None:
        self.canonical.write_text(self.body, encoding="utf-8")
        created = self.run_cli("ensure", str(self.canonical))
        self.assertTrue(created["created"])
        self.assertEqual(
            created["locator_to_add"], "research_memory: ./theory.research.sqlite"
        )
        self.canonical.write_text(
            "---\nresearch_memory: ./theory.research.sqlite\n---\n" + self.body,
            encoding="utf-8",
        )

    def changeset(self, round_id: str, revision: int, **operations: object) -> dict:
        return {
            "round_id": round_id,
            "expected_revision": revision,
            "expected_canonical_sha256": sha256(self.canonical),
            **operations,
        }

    @staticmethod
    def card(slug: str, **overrides: object) -> dict:
        card = {
            "slug": slug,
            "kind": "proof-route",
            "title": slug.replace("-", " ").title(),
            "summary_md": f"Summary for {slug}.",
            "detail_md": f"Detailed argument for {slug}.",
            "disposition": "open",
            "claim_status": "incomplete",
            "next_test": "Check the smallest unresolved case.",
            "facets": [],
        }
        card.update(overrides)
        return card

    @staticmethod
    def artifact_metadata(slug: str = "retained-check") -> dict:
        return {
            "schema": 1,
            "slug": slug,
            "kind": "exact-checker",
            "mode": "certify",
            "title": "Retained exact checker",
            "summary": "Checks the declared finite target exactly.",
            "canonical_keys": ["main-theorem"],
            "target_digest": "c" * 64,
            "purpose": "Certify the encoded finite proposition.",
            "scope": "The declared finite encoded family.",
            "encoded_target": "Every encoded candidate passes the exact predicate.",
            "evidence_ceiling": "Proof only of the encoded finite proposition.",
            "reproduce": {
                "argv": ["python3", "artifacts/check.py"],
                "runtime": "CPython 3",
                "budget": {"candidates": 20},
                "stopping_rule": "Exhaust all twenty candidates.",
            },
        }

    def apply(self, value: dict, *, success: bool = True) -> dict:
        return self.run_cli(
            "apply", str(self.canonical), input_value=value, success=success
        )

    @staticmethod
    def issue_messages(payload: dict) -> str:
        return "\n".join(issue["message"] for issue in payload.get("errors", []))

    def test_exactly_four_public_commands(self) -> None:
        parser = memory.build_parser()
        subparsers = next(
            action for action in parser._actions if isinstance(action, argparse._SubParsersAction)
        )
        self.assertEqual(set(subparsers.choices), {"ensure", "read", "apply", "check"})

        help_result = subprocess.run(
            [sys.executable, str(SCRIPT), "apply", "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        self.assertIn("Normative stdin grammar", help_result.stdout)
        self.assertIn("expected_canonical_sha256", help_result.stdout)
        self.assertIn('op:"update"', help_result.stdout)

    def test_ensure_bootstrap_only_and_exact_identity(self) -> None:
        self.canonical.write_text(self.body, encoding="utf-8")
        first = self.run_cli("ensure", str(self.canonical))
        self.assertEqual(first["database_path"], str(self.database.resolve()))
        self.assertTrue(first["current"])
        second = self.run_cli("ensure", str(self.canonical))
        self.assertFalse(second["created"])

        self.canonical.write_text(
            "---\nresearch_memory: ./theory.research.sqlite\n---\n" + self.body,
            encoding="utf-8",
        )
        linked = self.run_cli("ensure", str(self.canonical))
        self.assertFalse(linked["current"])
        self.assertEqual(linked["status"], "stale")

        self.database.unlink()
        missing = self.run_cli("ensure", str(self.canonical), success=False)
        self.assertIn("refusing to recreate", missing["error"])

    def test_old_or_modified_schema_is_rejected_without_migration(self) -> None:
        self.canonical.write_text(self.body, encoding="utf-8")
        self.run_cli("ensure", str(self.canonical))
        connection = sqlite3.connect(self.database)
        connection.execute("PRAGMA user_version=3")
        connection.commit()
        connection.close()
        failed = self.run_cli("ensure", str(self.canonical), success=False)
        self.assertIn("unsupported schema version 3", failed["error"])

        self.database.unlink()
        self.run_cli("ensure", str(self.canonical))
        connection = sqlite3.connect(self.database)
        connection.execute("CREATE TABLE surprise(value TEXT)")
        connection.commit()
        connection.close()
        failed = self.run_cli("ensure", str(self.canonical), success=False)
        self.assertIn("unexpected schema object", failed["error"])

    def test_card_lifecycle_has_explicit_ops_and_optimistic_revisions(self) -> None:
        self.bootstrap()
        added = self.apply(
            self.changeset(
                "add-card",
                0,
                cards=[{"op": "add", "card": self.card("route-one")}],
            )
        )
        self.assertEqual(added["database_revision"], 1)
        summary = self.run_cli("read", str(self.canonical), "card", "route-one")["card"]
        self.assertNotIn("detail_md", summary)
        self.assertEqual(summary["next_test"], "Check the smallest unresolved case.")
        self.assertEqual(summary["revision"], 1)
        self.assertRegex(summary["content_sha256"], r"^[0-9a-f]{64}$")

        full = self.run_cli(
            "read", str(self.canonical), "card", "route-one", "--full"
        )["card"]
        self.assertIn("Detailed argument", full["detail_md"]["text"])

        conflict = self.apply(
            self.changeset(
                "bad-update",
                1,
                cards=[
                    {
                        "op": "update",
                        "slug": "route-one",
                        "expected_revision": 9,
                        "set": {"title": "Changed"},
                    }
                ],
            ),
            success=False,
        )
        self.assertIn("revision conflict", conflict["error"])
        meta = self.run_cli("read", str(self.canonical), "meta")["meta"]
        self.assertEqual(meta["database_revision"], 1)

        updated = self.apply(
            self.changeset(
                "good-update",
                1,
                cards=[
                    {
                        "op": "update",
                        "slug": "route-one",
                        "expected_revision": 1,
                        "set": {
                            "disposition": "integrated",
                            "claim_status": "proved",
                            "next_test": None,
                        },
                    }
                ],
            )
        )
        self.assertEqual(updated["database_revision"], 2)
        self.assertEqual(
            self.run_cli("read", str(self.canonical), "card", "route-one")["card"]["claim_status"],
            "proved",
        )

        duplicate = self.apply(
            self.changeset(
                "duplicate-add",
                2,
                cards=[{"op": "add", "card": self.card("route-one")}],
            ),
            success=False,
        )
        self.assertIn("violates database constraints", duplicate["error"])

    def test_claim_status_and_workflow_disposition_are_separate(self) -> None:
        self.bootstrap()
        unsupported = self.apply(
            self.changeset(
                "legacy-status",
                0,
                cards=[
                    {
                        "op": "add",
                        "card": self.card("bad-status", claim_status="supported"),
                    }
                ],
            ),
            success=False,
        )
        self.assertIn("proved, refuted, conjectural, incomplete, unresolved", unsupported["error"])
        missing_state_reason = self.apply(
            self.changeset(
                "bad-state",
                0,
                cards=[
                    {
                        "op": "add",
                        "card": self.card(
                            "parked-route",
                            disposition="parked",
                            next_test=None,
                            revival_condition=None,
                        ),
                    }
                ],
            ),
            success=False,
        )
        self.assertIn("revival_condition", missing_state_reason["error"])

    def test_faceted_search_has_or_within_type_and_and_across_types(self) -> None:
        self.bootstrap()
        cards = [
            self.card(
                "algebra-group",
                facets=[
                    {"type": "field", "value": "Álgebra"},
                    {"type": "term", "value": "Finite Groups"},
                    {"type": "identifier", "value": "MSC2020:20D10"},
                    {"type": "symbol", "value": "GL_n(F)"},
                ],
            ),
            self.card(
                "combinatorial-group",
                facets=[
                    {"type": "field", "value": "Combinatorics"},
                    {"type": "term", "value": "finite groups"},
                ],
            ),
            self.card(
                "number-prime",
                facets=[
                    {"type": "field", "value": "Number theory"},
                    {"type": "term", "value": "Prime numbers"},
                ],
            ),
        ]
        self.apply(
            self.changeset(
                "facets", 0, cards=[{"op": "add", "card": card} for card in cards]
            )
        )
        self.assertTrue(self.run_cli("check", str(self.canonical))["ok"])
        stored = self.run_cli(
            "read", str(self.canonical), "card", "algebra-group", "--full"
        )["card"]["facets"]
        self.assertEqual(
            [(facet["type"], facet["normalized_value"]) for facet in stored],
            [
                ("field", "álgebra"),
                ("identifier", "msc2020:20D10"),
                ("symbol", "GL_n(F)"),
                ("term", "finite groups"),
            ],
        )
        result = self.run_cli(
            "read",
            str(self.canonical),
            "search",
            "--facet",
            "field=álgebra",
            "--facet",
            "field=COMBINATORICS",
            "--facet",
            "term=FINITE GROUPS",
        )
        self.assertEqual(
            {item["slug"] for item in result["results"]},
            {"algebra-group", "combinatorial-group"},
        )
        identifier = self.run_cli(
            "read",
            str(self.canonical),
            "search",
            "--facet",
            "identifier=msc2020:20D10",
        )
        self.assertEqual([item["slug"] for item in identifier["results"]], ["algebra-group"])
        wrong_case = self.run_cli(
            "read",
            str(self.canonical),
            "search",
            "--facet",
            "identifier=MSC2020:20d10",
        )
        self.assertEqual(wrong_case["results"], [])

    def test_text_search_and_all_are_bounded_and_summary_only(self) -> None:
        self.bootstrap()
        cards = [
            self.card(f"route-{index}", summary_md=f"Spectral obstruction number {index}.")
            for index in range(10)
        ]
        self.apply(
            self.changeset(
                "many-cards", 0, cards=[{"op": "add", "card": card} for card in cards]
            )
        )
        result = self.run_cli("read", str(self.canonical), "search", "spectral")
        self.assertEqual(len(result["results"]), memory.DEFAULT_LIMIT)
        self.assertNotIn("detail_md", json.dumps(result))
        too_many = self.run_cli(
            "read", str(self.canonical), "all", "--limit", "26", success=False
        )
        self.assertIn("may not exceed 25", too_many["error"])
        self.assertLessEqual(
            len(json.dumps(result).encode("utf-8")), memory.MAX_JSON_OUTPUT_BYTES
        )
        fallback, encoded = memory.bounded_json_output(
            {"ok": True, "blob": "x" * (memory.MAX_JSON_OUTPUT_BYTES + 1)},
            "read",
        )
        self.assertFalse(fallback["ok"])
        self.assertLessEqual(len(encoded.encode("utf-8")), memory.MAX_JSON_OUTPUT_BYTES)

    def test_reads_report_digests_current_state_and_key_pagination(self) -> None:
        self.bootstrap()
        cards = [self.card(f"linked-{index}") for index in range(3)]
        self.apply(
            self.changeset(
                "paged-links",
                0,
                cards=[{"op": "add", "card": card} for card in cards],
                key_links=[
                    {
                        "op": "add",
                        "card_slug": card["slug"],
                        "canonical_key": "main-theorem",
                        "relation": "supports",
                    }
                    for card in cards
                ],
            )
        )
        page = self.run_cli(
            "read",
            str(self.canonical),
            "key",
            "main-theorem",
            "--limit",
            "1",
            "--offset",
            "1",
        )
        self.assertTrue(page["canonical_digest_current"])
        self.assertEqual(page["canonical_sha256"], sha256(self.canonical))
        self.assertEqual(page["canonical_sha256"], page["indexed_canonical_sha256"])
        self.assertEqual(page["pagination"]["cards"]["total"], 3)
        self.assertEqual(page["pagination"]["cards"]["offset"], 1)
        self.assertEqual(len(page["cards"]), 1)
        self.assertEqual(page["cards"][0]["slug"], "linked-1")
        self.assertTrue(page["cards"][0]["link_current"])
        self.assertNotIn("next_test", page["cards"][0])

    def test_full_card_body_is_chunked(self) -> None:
        self.bootstrap()
        detail = "x" * (memory.BODY_CHUNK + 100)
        self.apply(
            self.changeset(
                "long-body",
                0,
                cards=[{"op": "add", "card": self.card("long-card", detail_md=detail)}],
            )
        )
        first = self.run_cli(
            "read", str(self.canonical), "card", "long-card", "--full"
        )["card"]["detail_md"]
        self.assertEqual(len(first["text"]), memory.BODY_CHUNK)
        second = self.run_cli(
            "read",
            str(self.canonical),
            "card",
            "long-card",
            "--full",
            "--body-offset",
            str(first["next_offset"]),
        )["card"]["detail_md"]
        self.assertEqual(len(second["text"]), 100)

    def test_key_links_return_selected_section_and_detect_staleness(self) -> None:
        self.bootstrap()
        self.apply(
            self.changeset(
                "link",
                0,
                cards=[{"op": "add", "card": self.card("linked-card")}],
                key_links=[
                    {
                        "op": "add",
                        "card_slug": "linked-card",
                        "canonical_key": "main-theorem",
                        "relation": "supports",
                        "note_md": "This route supports the main claim.",
                    }
                ],
            )
        )
        result = self.run_cli(
            "read", str(self.canonical), "key", "main-theorem"
        )
        self.assertIn("The initial statement", result["section"]["markdown"]["text"])
        self.assertEqual([card["slug"] for card in result["cards"]], ["linked-card"])
        self.assertNotIn("detail_md", result["cards"][0])

        self.canonical.write_text(
            self.canonical.read_text(encoding="utf-8").replace(
                "The initial statement.", "The materially revised statement."
            ),
            encoding="utf-8",
        )
        stale_read = self.run_cli(
            "read", str(self.canonical), "key", "main-theorem"
        )
        self.assertFalse(stale_read["canonical_digest_current"])
        self.assertFalse(stale_read["cards"][0]["link_current"])
        stale = self.run_cli("check", str(self.canonical), success=False)
        self.assertTrue(stale["integrity_ok"])
        self.assertFalse(stale["current"])
        self.assertEqual(stale["status"], "stale")
        self.assertIn("stale section digest", self.issue_messages(stale))
        self.assertEqual(stale["errors"][0]["category"], "stale")

        self.apply(
            self.changeset(
                "refresh-link",
                1,
                key_links=[
                    {
                        "op": "update",
                        "card_slug": "linked-card",
                        "canonical_key": "main-theorem",
                        "relation": "supports",
                        "expected_revision": 1,
                        "set": {},
                    }
                ],
            )
        )
        current = self.run_cli("check", str(self.canonical))
        self.assertEqual(current["status"], "current")

    def test_native_artifact_metadata_is_static_hashed_and_never_executed(self) -> None:
        self.bootstrap()
        data = self.root / "artifacts" / "input.txt"
        data.parent.mkdir()
        data.write_text("1 2 3\n", encoding="utf-8")
        marker = self.root / "executed.txt"
        source = self.root / "artifacts" / "search.py"
        metadata = {
            "schema": 1,
            "slug": "degree-six-search",
            "kind": "bounded-experiment",
            "mode": "falsify",
            "title": "Degree-six search",
            "summary": "Enumerates the declared finite family.",
            "canonical_keys": ["main-theorem"],
            "purpose": "Attempt to falsify the candidate in a bounded family.",
            "scope": "All declared inputs through degree six.",
            "target_digest": "a" * 64,
            "reproduce": {
                "argv": ["python3", "artifacts/search.py"],
                "runtime": "CPython 3",
                "parameters": {"max_degree": 6},
                "seeds": [],
                "budget": {"candidates": 100},
                "stopping_rule": "Exhaust the finite family.",
            },
            "encoded_target": "Find a counterexample in the declared finite family.",
            "evidence_ceiling": "A witness refutes the encoded target; absence is scoped only.",
            "limitations": ["No claim beyond degree six."],
            "references": [
                {
                    "role": "input",
                    "path": "artifacts/input.txt",
                    "sha256": sha256(data),
                }
            ],
            "result": {"status": "no-counterexample", "denominator": 100},
        }
        source.write_text(
            "RESEARCH_ARTIFACT = "
            + repr(metadata)
            + "\n"
            + f"open({str(marker)!r}, 'w').write('executed')\n"
            + "raise RuntimeError('must never execute')\n",
            encoding="utf-8",
        )
        self.apply(
            self.changeset(
                "artifact", 0, artifacts=[{"op": "add", "source_path": "artifacts/search.py"}]
            )
        )
        self.assertFalse(marker.exists())
        artifact = self.run_cli(
            "read", str(self.canonical), "artifact", "degree-six-search", "--full"
        )["artifact"]
        self.assertEqual(artifact["metadata"]["reproduce"]["parameters"], {"max_degree": 6})
        self.assertEqual(artifact["references"][0]["sha256"], sha256(data))
        linked = self.run_cli("read", str(self.canonical), "key", "main-theorem")
        self.assertEqual([item["slug"] for item in linked["artifacts"]], ["degree-six-search"])
        self.run_cli("check", str(self.canonical))
        self.assertFalse(marker.exists())

        data.write_text("changed\n", encoding="utf-8")
        stale = self.run_cli("check", str(self.canonical), success=False)
        self.assertTrue(stale["integrity_ok"])
        self.assertEqual(stale["status"], "stale")
        self.assertIn("digest mismatch", self.issue_messages(stale))

    def test_artifact_metadata_rejects_computation_and_non_native_tuples(self) -> None:
        self.bootstrap()
        artifacts = self.root / "artifacts"
        artifacts.mkdir()
        dynamic = artifacts / "dynamic.py"
        dynamic.write_text("RESEARCH_ARTIFACT = build_metadata()\n", encoding="utf-8")
        failed = self.apply(
            self.changeset(
                "dynamic", 0, artifacts=[{"op": "add", "source_path": "artifacts/dynamic.py"}]
            ),
            success=False,
        )
        self.assertIn("literal dict", failed["error"])

        duplicate = artifacts / "duplicate.py"
        duplicate.write_text(
            "RESEARCH_ARTIFACT = {'schema': 1, 'schema': 1}\n", encoding="utf-8"
        )
        failed = self.apply(
            self.changeset(
                "duplicate", 0, artifacts=[{"op": "add", "source_path": "artifacts/duplicate.py"}]
            ),
            success=False,
        )
        self.assertIn("duplicate dictionary key", failed["error"])

        link = artifacts / "link.py"
        link.symlink_to(dynamic)
        failed = self.apply(
            self.changeset(
                "symlink", 0, artifacts=[{"op": "add", "source_path": "artifacts/link.py"}]
            ),
            success=False,
        )
        self.assertIn("must not traverse a symlink", failed["error"])

    def test_retained_artifact_contract_is_exact_and_mode_controlled(self) -> None:
        self.bootstrap()
        artifacts = self.root / "artifacts"
        artifacts.mkdir()

        for name, mutate, expected in (
            (
                "bool-schema",
                lambda value: value.update(schema=True),
                "schema must equal 1",
            ),
            (
                "bad-mode",
                lambda value: value.update(mode="benchmark"),
                "mode must be one of",
            ),
            (
                "missing-budget",
                lambda value: value["reproduce"].pop("budget"),
                "reproduce is missing field(s): budget",
            ),
            (
                "missing-target",
                lambda value: value.pop("encoded_target"),
                "missing field(s): encoded_target",
            ),
        ):
            metadata = self.artifact_metadata(name)
            mutate(metadata)
            source = artifacts / f"{name}.py"
            source.write_text(f"RESEARCH_ARTIFACT = {metadata!r}\n", encoding="utf-8")
            failed = self.apply(
                self.changeset(
                    name,
                    0,
                    artifacts=[{"op": "add", "source_path": f"artifacts/{name}.py"}],
                ),
                success=False,
            )
            self.assertIn(expected, failed["error"])

    def test_check_recomputes_card_hash_state_and_returns_structured_issues(self) -> None:
        self.bootstrap()
        self.apply(
            self.changeset(
                "card-for-audit",
                0,
                cards=[{"op": "add", "card": self.card("audited-card")}],
            )
        )
        connection = sqlite3.connect(self.database)
        connection.execute(
            "UPDATE card SET disposition='parked',content_sha256=? WHERE slug='audited-card'",
            ("0" * 64,),
        )
        connection.commit()
        connection.close()

        checked = self.run_cli("check", str(self.canonical), success=False)
        codes = {issue["code"] for issue in checked["errors"]}
        self.assertIn("card-content-digest", codes)
        self.assertIn("card-state", codes)
        self.assertTrue(all("category" in issue for issue in checked["errors"]))
        self.assertEqual(checked["status"], "invalid")

    def test_check_rederives_every_artifact_cache_field_and_metadata_link(self) -> None:
        self.bootstrap()
        artifacts = self.root / "artifacts"
        artifacts.mkdir()
        source = artifacts / "check.py"
        metadata = self.artifact_metadata()
        source.write_text(f"RESEARCH_ARTIFACT = {metadata!r}\n", encoding="utf-8")
        self.apply(
            self.changeset(
                "retain-artifact",
                0,
                artifacts=[{"op": "add", "source_path": "artifacts/check.py"}],
            )
        )

        metadata["title"] = "Revised checker title"
        metadata["canonical_keys"] = ["boundary-case"]
        source.write_text(f"RESEARCH_ARTIFACT = {metadata!r}\n", encoding="utf-8")
        checked = self.run_cli("check", str(self.canonical), success=False)
        codes = {issue["code"] for issue in checked["errors"]}
        self.assertIn("artifact-cache", codes)
        self.assertIn("artifact-metadata-links", codes)
        self.assertTrue(checked["integrity_ok"])
        self.assertEqual(checked["status"], "stale")

    def test_origins_edges_and_transaction_rollback(self) -> None:
        self.bootstrap()
        source_digest = "b" * 64
        failed = self.apply(
            self.changeset(
                "rollback",
                0,
                cards=[{"op": "add", "card": self.card("new-card")}],
                origins=[
                    {
                        "op": "add",
                        "card_slug": "missing-card",
                        "source_locator": "source.research.sqlite",
                        "source_slug": "source-card",
                        "source_digest": source_digest,
                        "applicability_md": "Applies to the finite case.",
                    }
                ],
            ),
            success=False,
        )
        self.assertIn("violates database constraints", failed["error"])
        missing = self.run_cli(
            "read", str(self.canonical), "card", "new-card", success=False
        )
        self.assertIn("does not exist", missing["error"])

        self.apply(
            self.changeset(
                "relations",
                0,
                cards=[
                    {"op": "add", "card": self.card("source-card")},
                    {"op": "add", "card": self.card("target-card")},
                ],
                origins=[
                    {
                        "op": "add",
                        "card_slug": "target-card",
                        "source_locator": "source.research.sqlite",
                        "source_slug": "source-card",
                        "source_digest": source_digest,
                        "applicability_md": "Applies to the finite case.",
                    }
                ],
                edges=[
                    {
                        "op": "add",
                        "source_slug": "source-card",
                        "relation": "supports",
                        "target_slug": "target-card",
                        "note_md": "Supplies the missing estimate.",
                    }
                ],
            )
        )
        full = self.run_cli(
            "read", str(self.canonical), "card", "target-card", "--full"
        )["card"]
        self.assertEqual(full["origins"][0]["source_slug"], "source-card")
        self.assertEqual(full["incoming_edges"][0]["source_slug"], "source-card")

    def test_database_pair_can_move_without_relink_command(self) -> None:
        self.bootstrap()
        self.apply(
            self.changeset(
                "one-card", 0, cards=[{"op": "add", "card": self.card("portable-card")}]
            )
        )
        destination = self.root / "moved"
        destination.mkdir()
        moved_canonical = destination / self.canonical.name
        moved_database = destination / self.database.name
        shutil.move(self.canonical, moved_canonical)
        shutil.move(self.database, moved_database)
        result = self.run_cli("read", str(moved_canonical), "card", "portable-card")
        self.assertEqual(result["card"]["slug"], "portable-card")
        self.assertEqual(self.run_cli("check", str(moved_canonical))["status"], "current")


if __name__ == "__main__":
    unittest.main()
