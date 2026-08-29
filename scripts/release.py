#!/usr/bin/env python3
"""Cut a tested, tagged GitHub release from the default branch."""

from __future__ import annotations

import argparse
import re
import shlex
import shutil
import subprocess
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CITATION = ROOT / "CITATION.cff"
README = ROOT / "README.md"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class ReleaseError(RuntimeError):
    """A release precondition or command failed."""


def capture(*command: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if check and result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ReleaseError(f"{shlex.join(command)} failed: {detail}")
    return result


def run(*command: str) -> None:
    print(f"+ {shlex.join(command)}", flush=True)
    try:
        subprocess.run(command, cwd=ROOT, check=True)
    except subprocess.CalledProcessError as error:
        raise ReleaseError(f"{shlex.join(command)} failed") from error


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise ReleaseError(f"expected exactly one {label}")
    return updated


def read_current_version(citation: str, readme: str) -> str:
    versions = re.findall(r'^version: "(\d+\.\d+\.\d+)"$', citation, re.MULTILINE)
    if len(versions) != 1:
        raise ReleaseError("CITATION.cff must contain one quoted semantic version")
    version = versions[0]
    expected = (f"Version {version})", f"version = {{{version}}},")
    if any(readme.count(token) != 1 for token in expected):
        raise ReleaseError("README.md citation versions do not match CITATION.cff")
    return version


def bump_version(version: str, part: str) -> str:
    match = SEMVER.fullmatch(version)
    if not match:
        raise ReleaseError(f"unsupported version: {version!r}")
    major, minor, patch = map(int, match.groups())
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def update_metadata(
    citation: str, readme: str, current: str, target: str, released: date
) -> tuple[str, str]:
    citation = replace_once(
        citation,
        rf'^version: "{re.escape(current)}"$',
        f'version: "{target}"',
        "CITATION.cff version",
    )
    citation = replace_once(
        citation,
        r'^date-released: "\d{4}-\d{2}-\d{2}"$',
        f'date-released: "{released.isoformat()}"',
        "CITATION.cff release date",
    )
    readme = replace_once(
        readme,
        rf"Version {re.escape(current)}\)",
        f"Version {target})",
        "README prose version",
    )
    readme = replace_once(
        readme,
        rf"^  version = \{{{re.escape(current)}\}},$",
        f"  version = {{{target}}},",
        "README BibTeX version",
    )
    return citation, readme


def ensure_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise ReleaseError(f"required command not found: {name}")


def git(*arguments: str) -> str:
    return capture("git", *arguments).stdout.strip()


def remote_tag_exists(tag: str) -> bool:
    result = capture(
        "git", "ls-remote", "--exit-code", "--tags", "origin", f"refs/tags/{tag}", check=False
    )
    if result.returncode not in (0, 2):
        raise ReleaseError(result.stderr.strip() or f"could not inspect remote tag {tag}")
    return result.returncode == 0


def github_release_exists(tag: str) -> bool:
    return capture("gh", "release", "view", tag, "--json", "tagName", check=False).returncode == 0


def publish(branch: str, tag: str, head: str) -> None:
    tag_commit = capture("git", "rev-list", "-n", "1", tag, check=False)
    if tag_commit.returncode:
        run("git", "tag", "-a", tag, "-m", tag)
    elif tag_commit.stdout.strip() != head:
        raise ReleaseError(f"local tag {tag} does not point at HEAD")

    remote_head = git("rev-parse", f"origin/{branch}")
    if remote_head != head or not remote_tag_exists(tag):
        run(
            "git",
            "push",
            "--atomic",
            "origin",
            f"HEAD:refs/heads/{branch}",
            f"refs/tags/{tag}",
        )
    if github_release_exists(tag):
        raise ReleaseError(f"GitHub release {tag} already exists; add changes before releasing again")
    run(
        "gh",
        "release",
        "create",
        tag,
        "--verify-tag",
        "--generate-notes",
        "--fail-on-no-commits",
        "--title",
        tag,
    )
    print(f"Released {tag} on GitHub.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--bump", choices=("major", "minor", "patch"))
    choice.add_argument("--version", help="exact X.Y.Z version to release")
    args = parser.parse_args()

    for tool in ("git", "gh"):
        ensure_tool(tool)

    citation = CITATION.read_text()
    readme = README.read_text()
    current = read_current_version(citation, readme)
    target = args.version or bump_version(current, args.bump)
    if not SEMVER.fullmatch(target):
        raise ReleaseError("--version must be an unprefixed X.Y.Z semantic version")

    dirty = git("status", "--porcelain")
    if dirty:
        raise ReleaseError(f"working tree must be clean:\n{dirty}")
    capture("gh", "auth", "status")
    branch = capture(
        "gh", "repo", "view", "--json", "defaultBranchRef", "--jq", ".defaultBranchRef.name"
    ).stdout.strip()
    if git("branch", "--show-current") != branch:
        raise ReleaseError(f"release from the GitHub default branch ({branch})")
    run("git", "fetch", "--quiet", "origin", branch)

    head = git("rev-parse", "HEAD")
    remote_head = git("rev-parse", f"origin/{branch}")
    current_tag = f"v{current}"
    release_commit = git("log", "-1", "--pretty=%s") == f"release: {current_tag}"
    tagged_here = current_tag in git("tag", "--points-at", "HEAD").splitlines()
    if release_commit or tagged_here:
        if head != remote_head:
            ahead = git("rev-list", "--count", f"origin/{branch}..HEAD")
            ancestor = capture(
                "git", "merge-base", "--is-ancestor", f"origin/{branch}", "HEAD", check=False
            )
            if ahead != "1" or ancestor.returncode != 0:
                raise ReleaseError("local release commit has diverged from the remote branch")
        publish(branch, current_tag, head)
        return

    if tuple(map(int, target.split("."))) <= tuple(map(int, current.split("."))):
        raise ReleaseError(f"target version {target} must be newer than {current}")
    if head != remote_head:
        raise ReleaseError(f"local {branch} is not at origin/{branch}; pull or push before releasing")
    tag = f"v{target}"
    if capture("git", "rev-parse", "--verify", "--quiet", f"refs/tags/{tag}", check=False).returncode == 0:
        raise ReleaseError(f"local tag already exists: {tag}")
    if remote_tag_exists(tag) or github_release_exists(tag):
        raise ReleaseError(f"remote release or tag already exists: {tag}")

    updated_citation, updated_readme = update_metadata(
        citation, readme, current, target, date.today()
    )
    try:
        CITATION.write_text(updated_citation)
        README.write_text(updated_readme)
        run("git", "diff", "--check")
        run("python3", "-m", "unittest", "discover", "-s", "mathematician/tests", "-p", "test_*.py")
    except BaseException:
        CITATION.write_text(citation)
        README.write_text(readme)
        raise

    run("git", "add", "CITATION.cff", "README.md")
    run("git", "commit", "-m", f"release: {tag}")
    head = git("rev-parse", "HEAD")
    publish(branch, tag, head)


if __name__ == "__main__":
    try:
        main()
    except ReleaseError as error:
        raise SystemExit(f"release failed: {error}") from error
