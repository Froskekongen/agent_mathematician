from __future__ import annotations

import fcntl
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    REPO_ROOT
    / "mathematician"
    / "skills"
    / "research-mathematics"
    / "scripts"
    / "canonical_sections.py"
)
sys.path.insert(0, str(SCRIPT.parent))
import canonical_sections as sections  # noqa: E402


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class CanonicalSectionsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.canonical = self.root / "theory.md"

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
        self.assertEqual(completed.returncode == 0, success, completed.stderr)
        output = completed.stdout if completed.stdout else completed.stderr
        return json.loads(output)

    def test_scan_front_matter_fences_hierarchy_and_multiple_keys(self) -> None:
        content = """---
title: Théorie
fake: '# not a heading'
---
# Root

Root body.

<a id="research-key--implicit-young-evaluation"></a>
<a id="research-key--operator/repeated-centre"></a>

## Candidate α

**Research keys:** `implicit-young-evaluation`, `operator/repeated-centre`

```markdown
# ignored-heading
<a id="research-key--ignored"></a>
**Research key:** `ignored`
```

Candidate body.

### Child

Child body.

## Sibling

Sibling body.
"""
        self.canonical.write_text(content, encoding="utf-8")
        document = sections.scan_canonical(self.canonical)

        self.assertEqual(len(document.sections), 4)
        candidate = document.by_key["implicit-young-evaluation"]
        self.assertIs(candidate, document.by_key["operator/repeated-centre"])
        self.assertEqual(candidate.title, "Candidate α")
        self.assertEqual(candidate.ancestry, ("Root",))
        self.assertEqual(candidate.anchor_ids[0], "research-key--implicit-young-evaluation")
        self.assertIn("### Child", document.section_markdown(candidate))
        self.assertNotIn("## Sibling", document.section_markdown(candidate))

        scan = self.run_cli("scan", "--canonical", str(self.canonical))
        self.assertEqual(scan["research_key_count"], 2)
        self.assertNotIn("Candidate body.", json.dumps(scan))
        shown = self.run_cli(
            "show",
            "--canonical",
            str(self.canonical),
            "--key",
            "operator/repeated-centre",
        )
        self.assertIn("Candidate body.", shown["section"]["section_md"])
        self.assertNotIn("Sibling body.", shown["section"]["section_md"])

    def test_fingerprint_normalizes_line_endings_and_excludes_generated_lines(self) -> None:
        plain = b"# Root\n\n## Child\n\nBody.\n"
        keyed = (
            b"# Root\n\n"
            b'<a id="research-key--child-subject"></a>\n'
            b"\n"
            b"## Child\n"
            b"**Research key:** `child-subject`\n\n"
            b"Body.\n"
        )
        plain_document = sections.scan_bytes(plain)
        keyed_document = sections.scan_bytes(keyed)
        self.assertEqual(
            plain_document.sections[1].section_sha256,
            keyed_document.sections[1].section_sha256,
        )
        crlf_document = sections.scan_bytes(keyed.replace(b"\n", b"\r\n"))
        self.assertEqual(
            keyed_document.sections[1].section_sha256,
            crlf_document.sections[1].section_sha256,
        )

        changed_ancestor = sections.scan_bytes(keyed.replace(b"# Root", b"# Renamed root"))
        self.assertNotEqual(
            keyed_document.sections[1].section_sha256,
            changed_ancestor.sections[1].section_sha256,
        )
        changed_body = sections.scan_bytes(keyed.replace(b"Body.", b"Changed."))
        self.assertNotEqual(
            keyed_document.sections[0].section_sha256,
            changed_body.sections[0].section_sha256,
        )

    def test_check_reports_structural_errors_outside_but_not_inside_fences(self) -> None:
        self.canonical.write_text(
            """# Root

```markdown
  ## ignored
<a id="research-key--ignored"></a>
```

<a id="research-key--duplicate"></a>
## One
**Research key:** `different`

  ## Indented

<a id="research-key--duplicate"></a>
## Two
**Research key:** `duplicate`
""",
            encoding="utf-8",
        )
        result = self.run_cli(
            "check", "--canonical", str(self.canonical), success=False
        )
        errors = "\n".join(result["errors"])
        self.assertIn("anchor keys and visible Research keys differ", errors)
        self.assertIn("must start in column zero", errors)
        self.assertNotIn("ignored", errors)

    def test_raw_html_blocks_are_rejected_instead_of_indexing_phantom_sections(self) -> None:
        blocks = {
            "comment": ("<!--", "-->"),
            "script": ("<script>", "</script>"),
            "pre": ("<pre>", "</pre>"),
        }
        for name, (opener, closer) in blocks.items():
            with self.subTest(name=name):
                data = (
                    "# Visible\n\n"
                    f"{opener}\n"
                    '<a id="research-key--phantom"></a>\n\n'
                    "## Phantom\n"
                    "**Research key:** `phantom`\n"
                    f"{closer}\n"
                ).encode("utf-8")
                with self.assertRaisesRegex(
                    sections.CanonicalSectionsError,
                    "unsupported CommonMark raw-HTML block opener",
                ):
                    sections.scan_bytes(data)

        fenced = b"# Visible\n\n```html\n<!--\n# ignored\n-->\n```\n"
        self.assertEqual(len(sections.scan_bytes(fenced).sections), 1)

    def test_key_set_is_locked_digest_checked_source_preserving_and_idempotent(self) -> None:
        original = b"# Root\n\nIntro.\n\n## Target\n\nTarget body.\n\n## Other\n\nOther body.\n"
        self.canonical.write_bytes(original)
        before = sections.scan_canonical(self.canonical)
        target = before.sections[1]

        result = self.run_cli(
            "key-set",
            "--canonical",
            str(self.canonical),
            "--heading-line",
            str(target.heading_line),
            "--key",
            "implicit-young-evaluation",
            "--key",
            "operator/repeated-centre",
            "--expected-canonical-sha256",
            before.canonical_sha256,
        )
        self.assertTrue(result["changed"])
        updated = sections.scan_canonical(self.canonical)
        updated_target = updated.by_key["implicit-young-evaluation"]
        self.assertEqual(updated_target.section_sha256, target.section_sha256)
        expected = original.replace(
            b"## Target\n",
            b'<a id="research-key--implicit-young-evaluation"></a>\n'
            b'<a id="research-key--operator/repeated-centre"></a>\n'
            b"\n"
            b"## Target\n"
            b"**Research keys:** `implicit-young-evaluation`, `operator/repeated-centre`\n",
        )
        self.assertEqual(self.canonical.read_bytes(), expected)

        unchanged = self.run_cli(
            "key-set",
            "--canonical",
            str(self.canonical),
            "--heading-line",
            str(updated_target.heading_line),
            "--key",
            "implicit-young-evaluation",
            "--key",
            "operator/repeated-centre",
            "--expected-canonical-sha256",
            updated.canonical_sha256,
        )
        self.assertFalse(unchanged["changed"])
        self.assertEqual(self.canonical.read_bytes(), expected)

        conflict = self.run_cli(
            "key-set",
            "--canonical",
            str(self.canonical),
            "--heading-line",
            str(updated_target.heading_line),
            "--key",
            "replacement",
            "--expected-canonical-sha256",
            digest(original),
            success=False,
        )
        self.assertIn("conflict", conflict["error"])
        self.assertEqual(self.canonical.read_bytes(), expected)

    def test_key_set_rejects_lock_contention_and_a_pre_replace_edit(self) -> None:
        original = b"# Subject\n\nOriginal.\n"
        self.canonical.write_bytes(original)
        expected = digest(original)

        descriptor = os.open(self.canonical, os.O_RDONLY)
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = self.run_cli(
                "key-set",
                "--canonical",
                str(self.canonical),
                "--heading-line",
                "1",
                "--key",
                "subject",
                "--expected-canonical-sha256",
                expected,
                success=False,
            )
            self.assertIn("locked by another cooperating writer", result["error"])
            self.assertEqual(self.canonical.read_bytes(), original)
        finally:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)

        concurrent = b"# Subject\n\nConcurrent edit.\n"
        real_open_regular_file = sections._open_regular_file
        open_calls = 0

        def edit_before_recheck(path: Path) -> tuple[int, os.stat_result]:
            nonlocal open_calls
            open_calls += 1
            if open_calls == 3:
                self.canonical.write_bytes(concurrent)
            return real_open_regular_file(path)

        with mock.patch.object(
            sections, "_open_regular_file", side_effect=edit_before_recheck
        ):
            with self.assertRaisesRegex(
                sections.CanonicalSectionsError, "changed while preparing replacement"
            ):
                sections.set_section_keys(
                    self.canonical, 1, ["subject"], expected
                )
        self.assertEqual(self.canonical.read_bytes(), concurrent)

    def test_post_replace_fsync_failure_reports_committed_digest(self) -> None:
        original = b"# Subject\n\nOriginal.\n"
        self.canonical.write_bytes(original)
        expected = digest(original)
        fsync_calls = 0

        def fail_directory_fsync(_descriptor: int) -> None:
            nonlocal fsync_calls
            fsync_calls += 1
            if fsync_calls == 2:
                raise OSError("injected directory fsync failure")

        error_stream = io.StringIO()
        with mock.patch.object(sections.os, "fsync", side_effect=fail_directory_fsync):
            with redirect_stderr(error_stream):
                return_code = sections.main(
                    [
                        "key-set",
                        "--canonical",
                        str(self.canonical),
                        "--heading-line",
                        "1",
                        "--key",
                        "subject",
                        "--expected-canonical-sha256",
                        expected,
                    ]
                )
        self.assertEqual(return_code, 1)
        result = json.loads(error_stream.getvalue())
        self.assertTrue(result["committed"])
        self.assertFalse(result["durability_confirmed"])
        self.assertEqual(result["canonical_sha256"], digest(self.canonical.read_bytes()))
        self.assertEqual(result["installed_sha256"], result["canonical_sha256"])
        self.assertIn("injected directory fsync failure", result["durability_error"])

    def test_key_qualification_has_at_most_one_slash(self) -> None:
        self.canonical.write_bytes(b"# Subject\n")
        document = sections.scan_canonical(self.canonical)
        result = self.run_cli(
            "key-set",
            "--canonical",
            str(self.canonical),
            "--heading-line",
            "1",
            "--key",
            "theory/subtheory/subject",
            "--expected-canonical-sha256",
            document.canonical_sha256,
            success=False,
        )
        self.assertIn("invalid research key", result["error"])

    def test_utf8_bom_has_targeted_rejection(self) -> None:
        with self.assertRaisesRegex(
            sections.CanonicalSectionsError, "BOM-free UTF-8"
        ):
            sections.scan_bytes(b"\xef\xbb\xbf# Subject\n")

    def test_key_set_rejects_key_owned_by_another_section(self) -> None:
        self.canonical.write_text(
            """<a id="research-key--owned"></a>

# One
**Research key:** `owned`

# Two
""",
            encoding="utf-8",
        )
        document = sections.scan_canonical(self.canonical)
        result = self.run_cli(
            "key-set",
            "--canonical",
            str(self.canonical),
            "--heading-line",
            str(document.sections[1].heading_line),
            "--key",
            "owned",
            "--expected-canonical-sha256",
            document.canonical_sha256,
            success=False,
        )
        self.assertIn("already belongs", result["error"])

    def test_key_set_refuses_heading_without_line_ending(self) -> None:
        self.canonical.write_bytes(b"# Final heading")
        document = sections.scan_canonical(self.canonical)
        result = self.run_cli(
            "key-set",
            "--canonical",
            str(self.canonical),
            "--heading-line",
            "1",
            "--key",
            "final-heading",
            "--expected-canonical-sha256",
            document.canonical_sha256,
            success=False,
        )
        self.assertIn("end with a newline", result["error"])
        self.assertEqual(self.canonical.read_bytes(), b"# Final heading")

    def test_anchor_separator_is_required_and_fingerprint_neutral(self) -> None:
        invalid = (
            b'<a id="research-key--subject"></a>\n'
            b"# Subject\n"
            b"**Research key:** `subject`\n"
        )
        with self.assertRaisesRegex(sections.CanonicalSectionsError, "exactly one blank"):
            sections.scan_bytes(invalid)

        original = b"# Root\n\n## Subject\n\nBody.\n"
        self.canonical.write_bytes(original)
        before = sections.scan_canonical(self.canonical)
        parent_hash = before.sections[0].section_sha256
        result = self.run_cli(
            "key-set",
            "--canonical",
            str(self.canonical),
            "--heading-line",
            "3",
            "--key",
            "subject",
            "--expected-canonical-sha256",
            before.canonical_sha256,
        )
        self.assertTrue(result["changed"])
        expected_fragment = (
            b'<a id="research-key--subject"></a>\n\n'
            b"## Subject\n"
            b"**Research key:** `subject`\n"
        )
        self.assertIn(expected_fragment, self.canonical.read_bytes())
        after = sections.scan_canonical(self.canonical)
        self.assertEqual(after.sections[0].section_sha256, parent_hash)

    def test_key_set_rejects_symlink_and_non_regular_file(self) -> None:
        target = self.root / "target.md"
        target.write_bytes(b"# Target\n")
        link = self.root / "link.md"
        try:
            link.symlink_to(target)
        except (NotImplementedError, OSError):
            self.skipTest("symlinks unavailable")
        result = self.run_cli(
            "key-set",
            "--canonical",
            str(link),
            "--heading-line",
            "1",
            "--key",
            "target",
            "--expected-canonical-sha256",
            digest(target.read_bytes()),
            success=False,
        )
        self.assertIn("must not be a symlink", result["error"])
        self.assertEqual(target.read_bytes(), b"# Target\n")
        self.assertTrue(link.is_symlink())

        directory_result = self.run_cli(
            "scan", "--canonical", str(self.root), success=False
        )
        self.assertIn("regular file", directory_result["error"])


if __name__ == "__main__":
    unittest.main()
