from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MEMORY = (
    REPO_ROOT
    / "mathematician"
    / "skills"
    / "research-mathematics"
    / "scripts"
    / "research_memory.py"
)
RETIRE = (
    REPO_ROOT
    / "mathematician"
    / "skills"
    / "consolidate-math-documents"
    / "scripts"
    / "retire_sources.py"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ConsolidationWorkflowTest(unittest.TestCase):
    def run_json(
        self, script: Path, *arguments: str, input_value: dict | None = None
    ) -> dict:
        completed = subprocess.run(
            [sys.executable, str(script), *arguments],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            input=(
                json.dumps(input_value, ensure_ascii=False)
                if input_value is not None
                else None
            ),
            check=False,
        )
        output = completed.stdout or completed.stderr
        self.assertEqual(completed.returncode, 0, output)
        return json.loads(output)

    def add_locator(self, canonical: Path, ensured: dict) -> None:
        locator = ensured["locator_to_add"]
        self.assertIsInstance(locator, str)
        canonical.write_text(
            canonical.read_text(encoding="utf-8").replace(
                "---\n", f"---\n{locator}\n", 1
            ),
            encoding="utf-8",
        )

    def git(self, root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(
            ["git", "-C", str(root), *arguments],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return completed

    def apply(
        self,
        canonical: Path,
        round_id: str,
        *,
        cards: list[dict],
        origins: list[dict] | None = None,
    ) -> None:
        batch = {
            "round_id": round_id,
            "expected_revision": 0,
            "expected_canonical_sha256": sha256(canonical),
            "cards": [{"op": "add", "card": card} for card in cards],
            "origins": origins or [],
        }
        self.run_json(MEMORY, "apply", str(canonical), input_value=batch)

    def test_two_source_pairs_become_one_target_and_recoverable_deletions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "theory-repository"
            workpad = base / "round-workpad"
            root.mkdir()
            workpad.mkdir()
            self.git(root, "init", "-q")
            self.git(root, "config", "user.email", "example@example.invalid")
            self.git(root, "config", "user.name", "Consolidation Example")

            source_a = root / "finite-case.md"
            source_b = root / "boundary-case.md"
            source_a.write_text(
                """---
---
# Finite case

For a finite set `X`, define `w(X)=|X|`. Then `w(X union Y) <= w(X)+w(Y)`.
""",
                encoding="utf-8",
            )
            source_b.write_text(
                """---
---
# Boundary case

The same weight has equality for disjoint finite sets. Infinite sets are outside this model.
""",
                encoding="utf-8",
            )
            source_a_db = root / "finite-case.research.sqlite"
            source_b_db = root / "boundary-case.research.sqlite"
            self.add_locator(
                source_a, self.run_json(MEMORY, "ensure", str(source_a))
            )
            self.add_locator(
                source_b, self.run_json(MEMORY, "ensure", str(source_b))
            )

            self.apply(
                source_a,
                "source-a-card",
                cards=[
                    {
                        "slug": "symmetry-shortcut",
                        "kind": "proof-route",
                        "title": "Symmetry shortcut fails for overlap",
                        "summary_md": "Treating every union as disjoint loses the overlap term.",
                        "disposition": "rejected",
                        "claim_status": "refuted",
                        "reason": "The singleton example X=Y gives strict overcounting.",
                    }
                ],
            )
            self.apply(
                source_b,
                "source-b-card",
                cards=[
                    {
                        "slug": "infinite-extension",
                        "kind": "proof-obligation",
                        "title": "Choose an infinite-set replacement",
                        "summary_md": "Cardinality does not retain the intended finite weight behavior without a new codomain.",
                        "disposition": "open",
                        "claim_status": "unresolved",
                        "next_test": "Test counting measure on sigma-finite examples.",
                    }
                ],
            )
            source_a_card = self.run_json(
                MEMORY, "read", str(source_a), "card", "symmetry-shortcut"
            )["card"]
            source_b_card = self.run_json(
                MEMORY, "read", str(source_b), "card", "infinite-extension"
            )["card"]

            self.git(root, "add", source_a.name, source_b.name, source_a_db.name, source_b_db.name)
            self.git(root, "commit", "-q", "-m", "source theory pairs")
            source_hashes = {path.name: sha256(path) for path in (source_a, source_b, source_a_db, source_b_db)}

            target = root / "weight-theory.md"
            target_db = root / "weight-theory.research.sqlite"
            target_text = """---
research_memory: ./weight-theory.research.sqlite
---
# Finite weight theory

For a finite set `X`, define `w(X)=|X|`. For finite `X,Y`,
`w(X union Y) <= w(X)+w(Y)`, with equality when they are disjoint.
The infinite extension remains unresolved.

## Consolidation provenance

Consolidated from `finite-case.md` and `boundary-case.md`; their exact Git-tracked
versions supplied the inequality, equality boundary, rejected shortcut, and open extension.
"""
            manifest = {
                "repository_root": str(root),
                "target": {
                    "canonical": {
                        "path": target.name,
                        "sha256": hashlib.sha256(target_text.encode("utf-8")).hexdigest(),
                    },
                    "database": {"path": target_db.name},
                },
                "sources": [
                    {
                        "canonical": {"path": source_a.name, "sha256": source_hashes[source_a.name]},
                        "database": {"path": source_a_db.name, "sha256": source_hashes[source_a_db.name]},
                    },
                    {
                        "canonical": {"path": source_b.name, "sha256": source_hashes[source_b.name]},
                        "database": {"path": source_b_db.name, "sha256": source_hashes[source_b_db.name]},
                    },
                ],
            }
            manifest_path = workpad / "retirement.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            preflight = self.run_json(RETIRE, "check", "--manifest", str(manifest_path))
            self.assertEqual(preflight["target_state"], "absent")

            target.write_text(
                target_text.replace(
                    "research_memory: ./weight-theory.research.sqlite\n", ""
                ),
                encoding="utf-8",
            )
            ensured = self.run_json(MEMORY, "ensure", str(target))
            self.assertEqual(
                ensured["locator_to_add"],
                "research_memory: ./weight-theory.research.sqlite",
            )
            target.write_text(target_text, encoding="utf-8")
            self.apply(
                target,
                "target-curation",
                cards=[
                    {
                        "slug": "next-extension-test",
                        "kind": "proof-obligation",
                        "title": "Test an infinite-set weight",
                        "summary_md": "The finite inequality and disjoint equality are settled; an infinite analogue needs a new weight codomain.",
                        "disposition": "open",
                        "claim_status": "unresolved",
                        "next_test": "Test counting measure on sigma-finite examples.",
                    }
                ],
                origins=[
                    {
                        "op": "add",
                        "card_slug": "next-extension-test",
                        "source_locator": source_a_db.name,
                        "source_slug": source_a_card["slug"],
                        "source_digest": source_a_card["content_sha256"],
                        "applicability_md": "The overlap obstruction limits equality in the target finite-set theory.",
                    },
                    {
                        "op": "add",
                        "card_slug": "next-extension-test",
                        "source_locator": source_b_db.name,
                        "source_slug": source_b_card["slug"],
                        "source_digest": source_b_card["content_sha256"],
                        "applicability_md": "The source obligation becomes the target's explicit infinite-extension test.",
                    },
                ],
            )

            checked = self.run_json(MEMORY, "check", str(target))
            self.assertTrue(checked["current"])
            shown = self.run_json(
                MEMORY, "read", str(target), "card", "next-extension-test", "--full"
            )
            self.assertEqual(len(shown["card"]["origins"]), 2)

            ready = self.run_json(RETIRE, "check", "--manifest", str(manifest_path))
            self.assertEqual(ready["target_state"], "ready")
            retired = self.run_json(RETIRE, "apply", "--manifest", str(manifest_path))
            self.assertEqual(retired["remaining"], [])
            for path in (source_a, source_b, source_a_db, source_b_db):
                self.assertFalse(path.exists())
            self.assertTrue(target.exists())
            self.assertTrue(target_db.exists())

            post_retirement = self.run_json(MEMORY, "check", str(target))
            self.assertTrue(post_retirement["current"])
            shown_after = self.run_json(
                MEMORY, "read", str(target), "card", "next-extension-test", "--full"
            )
            self.assertEqual(len(shown_after["card"]["origins"]), 2)
            self.assertEqual(self.git(root, "diff", "--cached", "--name-only").stdout, "")
            status = self.git(root, "status", "--short").stdout
            for name in source_hashes:
                self.assertIn(name, status)

            self.git(root, "restore", "--source=HEAD", "--worktree", "--", *source_hashes)
            for name, expected in source_hashes.items():
                self.assertEqual(sha256(root / name), expected)

            shutil.rmtree(workpad)
            self.assertFalse(workpad.exists())


if __name__ == "__main__":
    unittest.main()
