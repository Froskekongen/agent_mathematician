from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = (
    REPO_ROOT / "mathematician" / "skills" / "research-mathematics" / "scripts"
)
import sys

sys.path.insert(0, str(SCRIPT_DIR))
import canonical_sections as sections  # noqa: E402


FRONT = "---\nresearch_memory: ./theory.research.sqlite\n---\n"


class CanonicalSectionsTest(unittest.TestCase):
    def test_scalar_keys_hierarchy_subtrees_and_fences(self) -> None:
        content = FRONT + """# Root

**Research key:** `root-result`

Root body.

## Child

**Research key:** `child-result`

```markdown
# Ignored
**Research key:** `ignored`
```

Child body.

## Sibling
Sibling body.
"""
        document = sections.scan_bytes(content.encode(), "/tmp/theory.md")
        self.assertEqual(set(document.by_key), {"root-result", "child-result"})
        child = document.by_key["child-result"]
        self.assertEqual(child.ancestry, ("Root",))
        self.assertIn("Child body.", document.section_markdown(child))
        self.assertNotIn("Sibling body.", document.section_markdown(child))
        self.assertIn("## Child", document.section_markdown(document.by_key["root-result"]))
        self.assertEqual(document.memory_relative_path, "./theory.research.sqlite")
        self.assertTrue(document.memory_declared)

    def test_key_is_first_nonblank_not_necessarily_adjacent(self) -> None:
        good = FRONT + "# Result\n\n\n**Research key:** `main-result`\nBody.\n"
        self.assertIn("main-result", sections.scan_bytes(good.encode()).by_key)

        late = FRONT + "# Result\n\nIntervening prose.\n**Research key:** `main-result`\n"
        with self.assertRaisesRegex(
            sections.CanonicalSectionsError, "first nonblank line"
        ):
            sections.scan_bytes(late.encode())

    def test_exact_singular_kebab_label_and_unique_keys(self) -> None:
        invalid = (
            FRONT
            + "# One\n**Research keys:** `one`, `two`\n"
            + "# Two\n**Research key:** `Bad_Key`\n"
        )
        with self.assertRaises(sections.CanonicalSectionsError) as caught:
            sections.scan_bytes(invalid.encode())
        errors = "\n".join(caught.exception.errors)
        self.assertIn("malformed Research key label", errors)

        duplicate = FRONT + "# One\n**Research key:** `same-key`\n# Two\n**Research key:** `same-key`\n"
        with self.assertRaisesRegex(sections.CanonicalSectionsError, "duplicate Research key"):
            sections.scan_bytes(duplicate.encode())

    def test_marker_lines_are_excluded_but_ancestry_and_body_are_hashed(self) -> None:
        original = FRONT + "# Root\n**Research key:** `first-key`\n## Child\n**Research key:** `child-key`\nBody.\n"
        renamed_key = original.replace("`child-key`", "`second-key`")
        first = sections.scan_bytes(original.encode()).sections[1]
        second = sections.scan_bytes(renamed_key.encode()).sections[1]
        self.assertEqual(first.section_sha256, second.section_sha256)

        renamed_ancestor = original.replace("# Root", "# Other root")
        changed_body = original.replace("Body.", "Changed body.")
        self.assertNotEqual(
            first.section_sha256,
            sections.scan_bytes(renamed_ancestor.encode()).sections[1].section_sha256,
        )
        self.assertNotEqual(
            first.section_sha256,
            sections.scan_bytes(changed_body.encode()).sections[1].section_sha256,
        )
        crlf = sections.scan_bytes(original.replace("\n", "\r\n").encode()).sections[1]
        self.assertEqual(first.section_sha256, crlf.section_sha256)

    def test_html_is_ordinary_content_and_never_a_generated_address(self) -> None:
        content = FRONT + "# Result\n**Research key:** `result`\n<a id=\"anything\"></a>\nBody.\n"
        document = sections.scan_bytes(content.encode())
        self.assertEqual(document.by_key["result"].key, "result")
        metadata = document.by_key["result"].metadata()
        self.assertNotIn("anchor", metadata)
        self.assertNotIn("deep_link", metadata)

    def test_front_matter_is_narrow_and_missing_locator_is_ensure_only(self) -> None:
        with self.assertRaisesRegex(sections.CanonicalSectionsError, "expected"):
            sections.scan_bytes(
                b"---\nresearch_memory:\n  path: ./old.research.sqlite\n---\n# T\n"
            )
        with self.assertRaisesRegex(sections.CanonicalSectionsError, "front matter"):
            sections.scan_bytes(b"# Theory\n")
        document = sections.scan_bytes(
            b"# Theory\n", "/tmp/clean-name.md", allow_missing_memory=True
        )
        self.assertFalse(document.memory_declared)
        self.assertEqual(document.memory_relative_path, "./clean-name.research.sqlite")

        with self.assertRaisesRegex(sections.CanonicalSectionsError, "must not contain '..'"):
            sections.scan_bytes(
                b"---\nresearch_memory: ./nested/../escape.research.sqlite\n---\n"
            )

    def test_memory_locator_stays_lexical_and_rejects_symlink_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            nested = root / "nested"
            nested.mkdir()
            canonical = root / "theory.md"
            canonical.write_text(
                "---\nresearch_memory: ./nested/theory.research.sqlite\n---\n# T\n",
                encoding="utf-8",
            )
            document = sections.scan_canonical(canonical)
            self.assertEqual(
                document.memory_path,
                canonical.resolve().parent / "nested" / "theory.research.sqlite",
            )

            outside = root / "outside"
            outside.mkdir()
            (root / "nested-link").symlink_to(outside, target_is_directory=True)
            canonical.write_text(
                "---\nresearch_memory: ./nested-link/theory.research.sqlite\n---\n# T\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(sections.CanonicalSectionsError, "traverse a symlink"):
                sections.scan_canonical(canonical)

            target = root / "actual.research.sqlite"
            target.touch()
            (root / "direct.research.sqlite").symlink_to(target)
            canonical.write_text(
                "---\nresearch_memory: ./direct.research.sqlite\n---\n# T\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(sections.CanonicalSectionsError, "traverse a symlink"):
                sections.scan_canonical(canonical)

    def test_scan_canonical_rejects_symlinks_and_invalid_utf8(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            canonical = root / "theory.md"
            canonical.write_text(FRONT + "# Theory\n", encoding="utf-8")
            link = root / "link.md"
            link.symlink_to(canonical)
            with self.assertRaisesRegex(sections.CanonicalSectionsError, "non-symlink"):
                sections.scan_canonical(link)
        with self.assertRaisesRegex(sections.CanonicalSectionsError, "valid UTF-8"):
            sections.scan_bytes(b"---\nresearch_memory: ./x.research.sqlite\n---\n\xff")

    def test_unterminated_fence_is_rejected(self) -> None:
        with self.assertRaisesRegex(sections.CanonicalSectionsError, "unterminated"):
            sections.scan_bytes((FRONT + "# T\n```python\n# ignored\n").encode())


if __name__ == "__main__":
    unittest.main()
