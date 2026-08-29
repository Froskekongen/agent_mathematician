from __future__ import annotations

import importlib.util
import unittest
from datetime import date
from pathlib import Path


SCRIPT = Path(__file__).parents[2] / "scripts" / "release.py"
SPEC = importlib.util.spec_from_file_location("release", SCRIPT)
assert SPEC and SPEC.loader
release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)


class ReleaseMetadataTests(unittest.TestCase):
    def test_bumps_each_semver_part(self) -> None:
        self.assertEqual(release.bump_version("1.2.3", "patch"), "1.2.4")
        self.assertEqual(release.bump_version("1.2.3", "minor"), "1.3.0")
        self.assertEqual(release.bump_version("1.2.3", "major"), "2.0.0")

    def test_updates_every_release_field(self) -> None:
        citation = 'version: "1.2.3"\ndate-released: "2025-01-01"\n'
        readme = "Version 1.2.3)\n  version = {1.2.3},\n"

        citation, readme = release.update_metadata(
            citation, readme, "1.2.3", "1.3.0", date(2026, 8, 29)
        )

        self.assertEqual(citation, 'version: "1.3.0"\ndate-released: "2026-08-29"\n')
        self.assertEqual(readme, "Version 1.3.0)\n  version = {1.3.0},\n")


if __name__ == "__main__":
    unittest.main()
