from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Optional
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    REPO_ROOT
    / "mathematician"
    / "skills"
    / "consolidate-math-documents"
    / "scripts"
    / "retire_sources.py"
)
MEMORY_SCRIPT = (
    REPO_ROOT
    / "mathematician"
    / "skills"
    / "research-mathematics"
    / "scripts"
    / "research_memory.py"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module():
    specification = importlib.util.spec_from_file_location("retire_sources", SCRIPT)
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load retirement helper")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class RetireSourcesCLITest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        self.git("init", "-q")
        self.git("config", "user.email", "tests@example.invalid")
        self.git("config", "user.name", "Research Memory Tests")

        self.target = self.root / "combined.md"
        self.target_db = self.root / "combined.research.sqlite"
        self.source = self.root / "old.md"
        self.source_db = self.root / "old.research.sqlite"
        self.target.write_text("# Combined\n", encoding="utf-8")
        self.source.write_text("# Old theory\n", encoding="utf-8")
        for canonical, theory in ((self.target, "combined"), (self.source, "old")):
            completed = subprocess.run(
                [
                    sys.executable,
                    str(MEMORY_SCRIPT),
                    "init",
                    "--canonical",
                    str(canonical),
                    "--theory",
                    theory,
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
        self.git("add", "combined.md", "combined.research.sqlite", "old.md", "old.research.sqlite")
        self.git("commit", "-q", "-m", "fixture")
        self.manifest = self.root / "retirement.json"
        self.write_manifest()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def git(self, *arguments: str, success: bool = True) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(
            ["git", "-C", str(self.root), *arguments],
            capture_output=True,
            text=True,
            check=False,
        )
        if success:
            self.assertEqual(completed.returncode, 0, completed.stderr)
        return completed

    def file_record(
        self, path: Path, claimed_digest: Optional[str] = None
    ) -> dict[str, str]:
        return {
            "path": str(path.relative_to(self.root)),
            "sha256": claimed_digest or digest(path),
        }

    def write_manifest(
        self,
        *,
        sources: Optional[list[dict]] = None,
        target: Optional[dict] = None,
        root: Optional[Path] = None,
    ) -> None:
        value = {
            "repository_root": str(root or self.root),
            "target": target
            or {
                "canonical": self.file_record(self.target),
                "database": {"path": "combined.research.sqlite"},
            },
            "sources": sources
            if sources is not None
            else [
                {
                    "canonical": self.file_record(self.source),
                    "database": self.file_record(self.source_db),
                }
            ],
        }
        self.manifest.write_text(json.dumps(value), encoding="utf-8")

    def run_cli(self, command: str, *, success: bool = True) -> dict:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), command, "--manifest", str(self.manifest)],
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
            output = completed.stderr
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            self.fail(
                f"retirement helper did not emit JSON: "
                f"stdout={completed.stdout!r}, stderr={completed.stderr!r}"
            )

    def test_check_then_apply_deletes_only_sources_and_leaves_unstaged_deletions(self) -> None:
        before_target = self.target.read_bytes()
        before_target_db = self.target_db.read_bytes()

        checked = self.run_cli("check")
        self.assertTrue(checked["eligible"])
        self.assertTrue(self.source.exists())
        self.assertTrue(self.source_db.exists())

        applied = self.run_cli("apply")
        self.assertEqual(applied["remaining"], [])
        self.assertEqual(
            applied["deleted"], [str(self.source_db.resolve()), str(self.source.resolve())]
        )
        self.assertFalse(self.source.exists())
        self.assertFalse(self.source_db.exists())
        self.assertEqual(self.target.read_bytes(), before_target)
        self.assertEqual(self.target_db.read_bytes(), before_target_db)
        self.assertEqual(self.git("diff", "--cached", "--name-only").stdout, "")
        status = self.git("status", "--short", "--", "old.md", "old.research.sqlite").stdout
        self.assertIn("old.md", status)
        self.assertIn("old.research.sqlite", status)

    def test_digest_change_blocks_entire_set(self) -> None:
        self.write_manifest(
            sources=[
                {
                    "canonical": self.file_record(self.source, "0" * 64),
                    "database": self.file_record(self.source_db),
                }
            ]
        )
        result = self.run_cli("apply", success=False)
        self.assertIn("digest changed", result["error"])
        self.assertTrue(self.source.exists())
        self.assertTrue(self.source_db.exists())

    def test_target_manifest_supports_prepublication_check_then_validates_close(self) -> None:
        expected_canonical = self.target.read_bytes()
        self.target.unlink()
        self.target_db.unlink()

        checked = self.run_cli("check")
        self.assertFalse(checked["target_ready"])
        self.assertEqual(checked["target_state"], "absent")
        result = self.run_cli("apply", success=False)
        self.assertIn("target.canonical does not exist", result["error"])
        self.assertTrue(self.source.exists())

        self.target.write_bytes(expected_canonical)
        completed = subprocess.run(
            [
                sys.executable,
                str(MEMORY_SCRIPT),
                "init",
                "--canonical",
                str(self.target),
                "--theory",
                "combined",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        applied = self.run_cli("apply")
        self.assertTrue(applied["ok"])

    def test_existing_target_digest_and_database_status_are_revalidated(self) -> None:
        before = self.target_db.read_bytes()
        checked = self.run_cli("check")
        self.assertTrue(checked["target_ready"])
        self.assertEqual(self.target_db.read_bytes(), before)

        self.write_manifest(
            target={
                "canonical": self.file_record(self.target, "0" * 64),
                "database": {"path": "combined.research.sqlite"},
            }
        )
        result = self.run_cli("check")
        self.assertFalse(result["target_ready"])
        self.assertEqual(result["target_state"], "candidate_pending")
        result = self.run_cli("apply", success=False)
        self.assertIn("target.canonical digest changed", result["error"])

        self.target.write_text("# Changed target\n", encoding="utf-8")
        self.write_manifest()
        result = self.run_cli("check", success=False)
        self.assertIn("canonical status is not current", result["error"])

    def test_target_database_must_belong_to_named_canonical(self) -> None:
        other = self.root / "other.md"
        other.write_text("# Other\n", encoding="utf-8")
        other_db = self.root / "other.research.sqlite"
        completed = subprocess.run(
            [
                sys.executable,
                str(MEMORY_SCRIPT),
                "init",
                "--canonical",
                str(other),
                "--theory",
                "other",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.write_manifest(
            target={
                "canonical": self.file_record(self.target),
                "database": {"path": str(other_db.relative_to(self.root))},
            }
        )
        result = self.run_cli("check", success=False)
        self.assertIn("does not belong to its paired canonical", result["error"])

    def test_unstaged_staged_untracked_and_ignored_sources_are_blocked(self) -> None:
        with self.subTest("unstaged"):
            self.source.write_text("# Changed\n", encoding="utf-8")
            self.write_manifest()
            result = self.run_cli("check", success=False)
            self.assertIn("unstaged changes", result["error"])
        self.git("restore", "--", "old.md")

        with self.subTest("staged"):
            self.source.write_text("# Staged\n", encoding="utf-8")
            self.git("add", "old.md")
            self.write_manifest()
            result = self.run_cli("check", success=False)
            self.assertIn("staged changes", result["error"])
        self.git("restore", "--staged", "--worktree", "old.md")

        with self.subTest("untracked"):
            untracked = self.root / "draft.md"
            untracked.write_text("# Draft\n", encoding="utf-8")
            self.write_manifest(sources=[{"canonical": self.file_record(untracked)}])
            result = self.run_cli("check", success=False)
            self.assertIn("untracked", result["error"])

        with self.subTest("ignored"):
            (self.root / ".gitignore").write_text("old.md\n", encoding="utf-8")
            self.git("add", ".gitignore")
            self.git("commit", "-q", "-m", "ignore old source")
            self.write_manifest()
            result = self.run_cli("check", success=False)
            self.assertIn("ignored by Git", result["error"])

    def test_sidecars_symlinks_directories_and_outside_paths_are_blocked(self) -> None:
        with self.subTest("sidecar"):
            sidecar = Path(str(self.source_db) + "-wal")
            sidecar.write_bytes(b"live")
            result = self.run_cli("check", success=False)
            self.assertIn("sidecar", result["error"])
            sidecar.unlink()

        with self.subTest("symlink"):
            link = self.root / "linked.md"
            link.symlink_to(self.source.name)
            self.write_manifest(
                sources=[
                    {
                        "canonical": {
                            "path": "linked.md",
                            "sha256": digest(self.source),
                        }
                    }
                ]
            )
            result = self.run_cli("check", success=False)
            self.assertIn("symlink", result["error"])

        with self.subTest("directory"):
            directory = self.root / "not-a-file"
            directory.mkdir()
            self.write_manifest(
                sources=[{"canonical": {"path": "not-a-file", "sha256": "0" * 64}}]
            )
            result = self.run_cli("check", success=False)
            self.assertIn("not a regular file", result["error"])

        with self.subTest("outside"):
            outside = self.base / "outside.md"
            outside.write_text("outside\n", encoding="utf-8")
            self.write_manifest(
                sources=[
                    {
                        "canonical": {
                            "path": str(outside),
                            "sha256": digest(outside),
                        }
                    }
                ]
            )
            result = self.run_cli("check", success=False)
            self.assertIn("outside repository_root", result["error"])

    def test_duplicate_target_overlap_and_incomplete_pair_are_blocked(self) -> None:
        with self.subTest("duplicate"):
            pair = {
                "canonical": self.file_record(self.source),
                "database": self.file_record(self.source_db),
            }
            self.write_manifest(sources=[pair, pair])
            result = self.run_cli("check", success=False)
            self.assertIn("duplicate", result["error"])

        with self.subTest("target overlap"):
            self.write_manifest(
                sources=[
                    {
                        "canonical": self.file_record(self.target),
                        "database": self.file_record(self.target_db),
                    }
                ]
            )
            result = self.run_cli("check", success=False)
            self.assertIn("target-overlapping", result["error"])

        with self.subTest("incomplete pair"):
            self.write_manifest(
                sources=[
                    {
                        "canonical": self.file_record(self.source),
                        "database": {"path": "old.research.sqlite"},
                    }
                ]
            )
            result = self.run_cli("check", success=False)
            self.assertIn("invalid fields", result["error"])

    def test_role_extensions_prevent_arbitrary_file_retirement(self) -> None:
        text = self.root / "notes.txt"
        text.write_text("not canonical\n", encoding="utf-8")
        database = self.root / "memory.db"
        database.write_bytes(b"not sqlite-named")
        self.git("add", "notes.txt", "memory.db")
        self.git("commit", "-q", "-m", "non-mathematical files")

        with self.subTest("canonical"):
            self.write_manifest(sources=[{"canonical": self.file_record(text)}])
            result = self.run_cli("check", success=False)
            self.assertIn(".markdown, .md", result["error"])

        with self.subTest("database"):
            self.write_manifest(
                sources=[
                    {
                        "canonical": self.file_record(self.source),
                        "database": self.file_record(database),
                    }
                ]
            )
            result = self.run_cli("check", success=False)
            self.assertIn(".sqlite", result["error"])

    def test_omitted_adjacent_default_database_is_never_orphaned(self) -> None:
        self.write_manifest(sources=[{"canonical": self.file_record(self.source)}])
        result = self.run_cli("apply", success=False)
        self.assertIn("adjacent default companion exists", result["error"])
        self.assertTrue(self.source.exists())
        self.assertTrue(self.source_db.exists())

    def test_canonical_only_source_without_adjacent_database_can_be_retired(self) -> None:
        canonical_only = self.root / "notes.markdown"
        canonical_only.write_text("# Canonical-only notes\n", encoding="utf-8")
        self.git("add", "notes.markdown")
        self.git("commit", "-q", "-m", "canonical-only source")
        self.write_manifest(
            sources=[{"canonical": self.file_record(canonical_only)}]
        )
        result = self.run_cli("apply")
        self.assertEqual(result["deleted"], [str(canonical_only.resolve())])
        self.assertFalse(canonical_only.exists())
        self.assertTrue(self.source.exists())
        self.assertTrue(self.source_db.exists())

    def test_pathspec_magic_filename_is_treated_literally_and_rejected_untracked(self) -> None:
        magic = self.root / ":(glob)*.md"
        magic.write_text("# Untracked magic path\n", encoding="utf-8")
        self.write_manifest(sources=[{"canonical": self.file_record(magic)}])
        result = self.run_cli("apply", success=False)
        self.assertIn("untracked", result["error"])
        self.assertTrue(magic.exists())

    def test_hidden_git_index_states_cannot_mask_unrecoverable_edits(self) -> None:
        with self.subTest("assume-unchanged"):
            self.git("update-index", "--assume-unchanged", "old.md")
            self.source.write_text("# Hidden local edit\n", encoding="utf-8")
            self.write_manifest()
            result = self.run_cli("apply", success=False)
            self.assertIn("unsafe Git index state", result["error"])
            self.assertTrue(self.source.exists())
            self.assertTrue(self.source_db.exists())
            self.git("update-index", "--no-assume-unchanged", "old.md")
            self.git("restore", "--", "old.md")

        with self.subTest("skip-worktree"):
            self.git("update-index", "--skip-worktree", "old.md")
            self.source.write_text("# Hidden sparse-checkout edit\n", encoding="utf-8")
            self.write_manifest()
            result = self.run_cli("apply", success=False)
            self.assertIn("unsafe Git index state", result["error"])
            self.assertTrue(self.source.exists())
            self.assertTrue(self.source_db.exists())
            self.git("update-index", "--no-skip-worktree", "old.md")
            self.git("restore", "--", "old.md")

    def test_source_database_must_be_schema2_and_owned_by_paired_canonical(self) -> None:
        other = self.root / "other-source.md"
        other.write_text("# Other source\n", encoding="utf-8")
        other_db = self.root / "other-source.research.sqlite"
        completed = subprocess.run(
            [
                sys.executable,
                str(MEMORY_SCRIPT),
                "init",
                "--canonical",
                str(other),
                "--theory",
                "other-source",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        invalid_db = self.root / "invalid.research.sqlite"
        invalid_db.write_bytes(b"not a SQLite database")
        self.git("add", "other-source.md", "other-source.research.sqlite", "invalid.research.sqlite")
        self.git("commit", "-q", "-m", "other companions")

        with self.subTest("wrong owner"):
            before = other_db.read_bytes()
            self.write_manifest(
                sources=[
                    {
                        "canonical": self.file_record(self.source),
                        "database": self.file_record(other_db),
                    }
                ]
            )
            result = self.run_cli("check", success=False)
            self.assertIn("does not belong to its paired canonical", result["error"])
            self.assertEqual(other_db.read_bytes(), before)
            self.assertTrue(self.source.exists())

        with self.subTest("invalid schema"):
            before = invalid_db.read_bytes()
            self.write_manifest(
                sources=[
                    {
                        "canonical": self.file_record(self.source),
                        "database": self.file_record(invalid_db),
                    }
                ]
            )
            result = self.run_cli("check", success=False)
            self.assertIn("failed research-memory check", result["error"])
            self.assertEqual(invalid_db.read_bytes(), before)

    def test_stale_but_owned_source_database_can_be_reviewed_and_retired(self) -> None:
        self.source.write_text("# Old theory, revised after memory consolidation\n", encoding="utf-8")
        self.git("add", "old.md")
        self.git("commit", "-q", "-m", "revise canonical without memory batch")
        self.write_manifest()

        checked = self.run_cli("check")
        self.assertTrue(checked["eligible"])
        applied = self.run_cli("apply")
        self.assertEqual(applied["remaining"], [])
        self.assertFalse(self.source.exists())
        self.assertFalse(self.source_db.exists())

    def test_non_git_root_is_blocked_before_any_deletion(self) -> None:
        plain = self.base / "plain"
        plain.mkdir()
        (plain / "target.md").write_text("target\n", encoding="utf-8")
        (plain / "target.sqlite").write_bytes(b"target")
        (plain / "source.md").write_text("source\n", encoding="utf-8")
        self.manifest.write_text(
            json.dumps(
                {
                    "repository_root": str(plain),
                    "target": {
                        "canonical": {
                            "path": "target.md",
                            "sha256": digest(plain / "target.md"),
                        },
                        "database": {"path": "target.sqlite"},
                    },
                    "sources": [
                        {
                            "canonical": {
                                "path": "source.md",
                                "sha256": digest(plain / "source.md"),
                            }
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        result = self.run_cli("apply", success=False)
        self.assertIn("not a Git working tree", result["error"])
        self.assertTrue((plain / "source.md").exists())

    def test_partial_unlink_failure_reports_exact_deleted_and_remaining_paths(self) -> None:
        module = load_module()
        real_unlink = Path.unlink

        def fail_on_canonical(path: Path, *args, **kwargs):
            if path == self.source.resolve():
                raise PermissionError("simulated refusal")
            return real_unlink(path, *args, **kwargs)

        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(Path, "unlink", new=fail_on_canonical):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                return_code = module.main(
                    ["apply", "--manifest", str(self.manifest)]
                )

        self.assertEqual(return_code, 1)
        self.assertEqual(stdout.getvalue(), "")
        result = json.loads(stderr.getvalue())
        self.assertFalse(result["ok"])
        self.assertEqual(result["deleted"], [str(self.source_db.resolve())])
        self.assertEqual(result["remaining"], [str(self.source.resolve())])
        self.assertTrue(self.source.exists())
        self.assertFalse(self.source_db.exists())
        self.assertTrue(self.target.exists())
        self.assertTrue(self.target_db.exists())

    def test_source_replacement_after_plan_stops_remaining_deletions(self) -> None:
        module = load_module()
        real_build_plan = module.build_plan

        def build_then_replace(*args, **kwargs):
            plan = real_build_plan(*args, **kwargs)
            replacement = self.root / "replacement.md"
            replacement.write_bytes(self.source.read_bytes())
            replacement.replace(self.source)
            return plan

        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(module, "build_plan", new=build_then_replace):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                return_code = module.main(
                    ["apply", "--manifest", str(self.manifest)]
                )

        self.assertEqual(return_code, 1)
        result = json.loads(stderr.getvalue())
        self.assertIn("identity changed", result["error"])
        self.assertEqual(result["deleted"], [])
        self.assertEqual(
            result["remaining"],
            [str(self.source_db.resolve()), str(self.source.resolve())],
        )
        self.assertTrue(self.source_db.exists())
        self.assertTrue(self.source.exists())

    def test_target_replacement_after_source_preflight_blocks_first_deletion(self) -> None:
        module = load_module()
        real_build_plan = module.build_plan

        def build_then_replace(*args, **kwargs):
            plan = real_build_plan(*args, **kwargs)
            replacement = self.root / "replacement-target.md"
            replacement.write_bytes(self.target.read_bytes())
            replacement.replace(self.target)
            return plan

        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(module, "build_plan", new=build_then_replace):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                return_code = module.main(
                    ["apply", "--manifest", str(self.manifest)]
                )

        self.assertEqual(return_code, 1)
        result = json.loads(stderr.getvalue())
        self.assertIn("identity changed", result["error"])
        self.assertEqual(result["deleted"], [])
        self.assertEqual(
            result["remaining"],
            [str(self.source_db.resolve()), str(self.source.resolve())],
        )
        self.assertTrue(self.source_db.exists())
        self.assertTrue(self.source.exists())


if __name__ == "__main__":
    unittest.main()
