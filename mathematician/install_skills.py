#!/usr/bin/env python3
"""Install the mathematical research skill suite for supported agents."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SKILL_NAMES = (
    "research-mathematics",
    "explore-mathematical-structure",
    "explore-proof-strategies",
    "formalize-concepts",
    "destroy-theory",
    "explain-mathematics",
    "audit-assumptions",
)

OBSOLETE_SKILL_PATHS = (
    Path("explore-mathematical-structure/references/exploration-ledger.md"),
)


def target_roots(home: Path) -> dict[str, Path]:
    """Return current user-level skill roots for each supported host."""
    return {
        "codex": home / ".agents" / "skills",
        "cursor": home / ".agents" / "skills",
        "claude": home / ".claude" / "skills",
    }


def install(source_root: Path, destination_root: Path, *, dry_run: bool) -> None:
    """Copy every suite skill into one user-level skill root."""
    for name in SKILL_NAMES:
        source = source_root / name
        destination = destination_root / name
        if not (source / "SKILL.md").is_file():
            raise SystemExit(f"missing source skill: {source}")
        if destination.is_symlink() or (destination.exists() and not destination.is_dir()):
            raise SystemExit(f"refusing to overwrite non-directory target: {destination}")
        print(f"{'would install' if dry_run else 'installing'} {name} -> {destination}")
        if not dry_run:
            destination_root.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, destination, dirs_exist_ok=True)

    for relative in OBSOLETE_SKILL_PATHS:
        obsolete = destination_root / relative
        if obsolete.is_file() or obsolete.is_symlink():
            print(f"{'would remove' if dry_run else 'removing'} obsolete suite file {obsolete}")
            if not dry_run:
                obsolete.unlink()


def main() -> None:
    """Parse targets and install the complete suite."""
    parser = argparse.ArgumentParser(
        description=(
            "Install all seven skills globally. Codex and Cursor share the open-standard "
            "~/.agents/skills root; Claude Code uses ~/.claude/skills."
        )
    )
    parser.add_argument(
        "targets",
        nargs="*",
        choices=("codex", "cursor", "claude", "all"),
        default=("all",),
        help="hosts to install for (default: all)",
    )
    parser.add_argument("--dry-run", action="store_true", help="show destinations only")
    args = parser.parse_args()

    requested = {"codex", "cursor", "claude"} if "all" in args.targets else set(args.targets)
    roots = target_roots(Path.home())
    source_root = Path(__file__).resolve().parent / "skills"

    # Deduplicate Codex and Cursor's shared open-standard root.
    destinations = {roots[target] for target in requested}
    for destination in sorted(destinations, key=str):
        install(source_root, destination, dry_run=args.dry_run)

    if not args.dry_run:
        print("installed; restart an agent if its current session does not discover the new root")


if __name__ == "__main__":
    main()
