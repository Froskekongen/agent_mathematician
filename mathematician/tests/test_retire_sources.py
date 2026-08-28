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


def canonical_text(database: str | None, title: str) -> str:
    locator = f"research_memory: ./{database}\n" if database else ""
    return f"---\n{locator}---\n# {title}\n"


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
        self.bootstrap(self.target, "Combined")
        self.bootstrap(self.source, "Old theory")
        self.git(
            "add",
            self.target.name,
            self.target_db.name,
            self.source.name,
            self.source_db.name,
        )
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

    def ensure(self, canonical: Path) -> dict:
        completed = subprocess.run(
            [sys.executable, str(MEMORY_SCRIPT), "ensure", str(canonical)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return json.loads(completed.stdout)

    def bootstrap(self, canonical: Path, title: str) -> None:
        canonical.write_text(canonical_text(None, title), encoding="utf-8")
        ensured = self.ensure(canonical)
        locator = ensured["locator_to_add"]
        self.assertIsInstance(locator, str)
        canonical.write_text(
            canonical.read_text(encoding="utf-8").replace(
                "---\n", f"---\n{locator}\n", 1
            ),
            encoding="utf-8",
        )
        changeset = {
            "round_id": "bootstrap-locator",
            "expected_revision": 0,
            "expected_canonical_sha256": digest(canonical),
        }
        completed = subprocess.run(
            [sys.executable, str(MEMORY_SCRIPT), "apply", str(canonical)],
            input=json.dumps(changeset),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)

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
    ) -> None:
        value = {
            "repository_root": str(self.root),
            "target": target
            or {
                "canonical": self.file_record(self.target),
                "database": {"path": self.target_db.name},
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
                "retirement helper did not emit JSON: "
                f"stdout={completed.stdout!r}, stderr={completed.stderr!r}"
            )

    def test_check_then_apply_deletes_only_clean_git_sources(self) -> None:
        before_target = self.target.read_bytes()
        before_target_db = self.target_db.read_bytes()

        checked = self.run_cli("check")
        self.assertTrue(checked["eligible"])
        self.assertEqual(checked["target_state"], "ready")

        applied = self.run_cli("apply")
        self.assertEqual(applied["remaining"], [])
        self.assertEqual(
            applied["deleted"],
            [str(self.source_db.resolve()), str(self.source.resolve())],
        )
        self.assertFalse(self.source.exists())
        self.assertFalse(self.source_db.exists())
        self.assertEqual(self.target.read_bytes(), before_target)
        self.assertEqual(self.target_db.read_bytes(), before_target_db)
        self.assertEqual(self.git("diff", "--cached", "--name-only").stdout, "")
        status = self.git(
            "status", "--short", "--", self.source.name, self.source_db.name
        ).stdout
        self.assertIn(self.source.name, status)
        self.assertIn(self.source_db.name, status)

    def test_source_digest_change_blocks_the_entire_set(self) -> None:
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

    def test_duplicate_json_keys_are_rejected_at_every_depth(self) -> None:
        root = json.dumps(str(self.root))
        target_digest = json.dumps(digest(self.target))
        source_digest = json.dumps(digest(self.source))
        source_db_digest = json.dumps(digest(self.source_db))
        cases = (
            (
                "top-level",
                '{"repository_root":' + root + ',"repository_root":' + root
                + ',"target":{},"sources":[]}',
            ),
            (
                "nested",
                '{"repository_root":' + root
                + ',"target":{"canonical":{"path":"combined.md",'
                + '"path":"old.md","sha256":' + target_digest
                + '},"database":{"path":"combined.research.sqlite"}},'
                + '"sources":[{"canonical":{"path":"old.md","sha256":'
                + source_digest + '},"database":{"path":"old.research.sqlite",'
                + '"sha256":' + source_db_digest + '}}]}',
            ),
        )
        for label, raw in cases:
            with self.subTest(label=label):
                self.manifest.write_text(raw, encoding="utf-8")
                result = self.run_cli("check", success=False)
                self.assertIn("duplicate JSON key", result["error"])

    def test_absent_target_can_be_preflighted_but_not_applied(self) -> None:
        expected_canonical = self.target.read_bytes()
        self.target.unlink()
        self.target_db.unlink()

        checked = self.run_cli("check")
        self.assertFalse(checked["target_ready"])
        self.assertEqual(checked["target_state"], "absent")
        result = self.run_cli("apply", success=False)
        self.assertIn("target.canonical does not exist", result["error"])
        self.assertTrue(self.source.exists())

        self.bootstrap(self.target, "Combined")
        self.assertEqual(self.target.read_bytes(), expected_canonical)
        applied = self.run_cli("apply")
        self.assertTrue(applied["ok"])

    def test_target_must_be_exact_current_and_paired(self) -> None:
        self.target.write_text(
            canonical_text(self.target_db.name, "Changed target"), encoding="utf-8"
        )
        self.write_manifest()
        stale = self.run_cli("check", success=False)
        self.assertIn("not current", stale["error"])
        self.assertTrue(self.source.exists())
        self.git("restore", "--", self.target.name)

        other = self.root / "other.md"
        other_db = self.root / "other.research.sqlite"
        self.bootstrap(other, "Other")
        self.write_manifest(
            target={
                "canonical": self.file_record(self.target),
                "database": {"path": other_db.name},
            }
        )
        wrong_pair = self.run_cli("check", success=False)
        self.assertIn("does not belong", wrong_pair["error"])

    def test_dirty_untracked_and_hidden_sources_are_blocked(self) -> None:
        with self.subTest("unstaged"):
            self.source.write_text(
                canonical_text(self.source_db.name, "Changed"), encoding="utf-8"
            )
            self.write_manifest()
            result = self.run_cli("check", success=False)
            self.assertIn("unstaged changes", result["error"])
        self.git("restore", "--", self.source.name)

        with self.subTest("untracked"):
            draft = self.root / "draft.md"
            draft.write_text("# Draft\n", encoding="utf-8")
            self.write_manifest(sources=[{"canonical": self.file_record(draft)}])
            result = self.run_cli("check", success=False)
            self.assertIn("untracked", result["error"])

        with self.subTest("assume-unchanged"):
            self.git("update-index", "--assume-unchanged", self.source.name)
            self.source.write_text(
                canonical_text(self.source_db.name, "Hidden edit"), encoding="utf-8"
            )
            self.write_manifest()
            result = self.run_cli("apply", success=False)
            self.assertIn("unsafe Git index state", result["error"])
            self.git("update-index", "--no-assume-unchanged", self.source.name)
            self.git("restore", "--", self.source.name)

    def test_sidecars_symlinks_and_outside_paths_are_blocked(self) -> None:
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
                            "path": link.name,
                            "sha256": digest(self.source),
                        }
                    }
                ]
            )
            result = self.run_cli("check", success=False)
            self.assertIn("symlink", result["error"])

        with self.subTest("outside repository"):
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

    def test_source_database_must_be_valid_and_owned_but_may_be_stale(self) -> None:
        other = self.root / "other-source.md"
        other_db = self.root / "other-source.research.sqlite"
        self.bootstrap(other, "Other source")
        self.git("add", other.name, other_db.name)
        self.git("commit", "-q", "-m", "other source pair")

        self.write_manifest(
            sources=[
                {
                    "canonical": self.file_record(self.source),
                    "database": self.file_record(other_db),
                }
            ]
        )
        wrong_owner = self.run_cli("check", success=False)
        self.assertIn("does not belong", wrong_owner["error"])

        broken = self.root / "broken.md"
        broken_db = self.root / "broken.research.sqlite"
        broken.write_text(canonical_text(broken_db.name, "Broken"), encoding="utf-8")
        broken_db.write_bytes(b"not sqlite")
        self.git("add", broken.name, broken_db.name)
        self.git("commit", "-q", "-m", "broken source pair")
        self.write_manifest(
            sources=[
                {
                    "canonical": self.file_record(broken),
                    "database": self.file_record(broken_db),
                }
            ]
        )
        invalid = self.run_cli("check", success=False)
        self.assertIn("failed research-memory check", invalid["error"])
        self.assertIn("[database-validation] database validation failed", invalid["error"])
        self.assertNotIn("unknown error", invalid["error"])

        self.source.write_text(
            canonical_text(self.source_db.name, "Old theory revised"), encoding="utf-8"
        )
        self.git("add", self.source.name)
        self.git("commit", "-q", "-m", "revise source canonical")
        self.write_manifest()
        self.assertTrue(self.run_cli("check")["eligible"])
        self.assertTrue(self.run_cli("apply")["ok"])

    def test_omitted_database_is_allowed_only_when_no_companion_exists(self) -> None:
        self.write_manifest(sources=[{"canonical": self.file_record(self.source)}])
        result = self.run_cli("apply", success=False)
        self.assertIn("adjacent default companion exists", result["error"])

        notes = self.root / "notes.markdown"
        notes.write_text("# Canonical-only notes\n", encoding="utf-8")
        self.git("add", notes.name)
        self.git("commit", "-q", "-m", "canonical-only notes")
        self.write_manifest(sources=[{"canonical": self.file_record(notes)}])
        retired = self.run_cli("apply")
        self.assertEqual(retired["deleted"], [str(notes.resolve())])
        self.assertFalse(notes.exists())

    def test_partial_unlink_failure_reports_deleted_and_remaining_paths(self) -> None:
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
                return_code = module.main(["apply", "--manifest", str(self.manifest)])

        self.assertEqual(return_code, 1)
        self.assertEqual(stdout.getvalue(), "")
        result = json.loads(stderr.getvalue())
        self.assertEqual(result["deleted"], [str(self.source_db.resolve())])
        self.assertEqual(result["remaining"], [str(self.source.resolve())])
        self.assertTrue(self.source.exists())
        self.assertFalse(self.source_db.exists())

    def test_file_replacement_after_preflight_stops_before_deletion(self) -> None:
        module = load_module()
        real_build_plan = module.build_plan

        for name, replaced in (("source", self.source), ("target", self.target)):
            with self.subTest(name):

                def build_then_replace(*args, **kwargs):
                    plan = real_build_plan(*args, **kwargs)
                    replacement = self.root / f"replacement-{name}.md"
                    replacement.write_bytes(replaced.read_bytes())
                    replacement.replace(replaced)
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
                self.assertTrue(self.source.exists())
                self.assertTrue(self.source_db.exists())
                if name == "source":
                    self.git("restore", "--", self.source.name)


if __name__ == "__main__":
    unittest.main()
