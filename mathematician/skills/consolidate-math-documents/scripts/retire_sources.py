#!/usr/bin/env python3
"""Safely retire Git-recoverable source pairs after consolidation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence


SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
SIDECAR_SUFFIXES = ("-journal", "-wal", "-shm")


class RetirementError(Exception):
    """A user-facing manifest or safety error."""


class JSONArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise RetirementError(message)


@dataclass(frozen=True)
class FileIdentity:
    device: int
    inode: int
    size: int
    mtime_ns: int


@dataclass(frozen=True)
class FileRecord:
    path: Path
    sha256: Optional[str]
    present: bool
    digest_matches: Optional[bool]
    observed_sha256: Optional[str]
    identity: Optional[FileIdentity]


@dataclass(frozen=True)
class RetirementPlan:
    repository_root: Path
    target_canonical: FileRecord
    target_database: FileRecord
    source_pairs: tuple[tuple[FileRecord, Optional[FileRecord]], ...]

    @property
    def target_ready(self) -> bool:
        return (
            self.target_canonical.present
            and self.target_database.present
            and self.target_canonical.digest_matches is True
        )

    @property
    def retirement_order(self) -> tuple[FileRecord, ...]:
        # Delete the companion first so a partial failure leaves readable Markdown.
        records = []
        for canonical, database in self.source_pairs:
            if database is not None:
                records.append(database)
            records.append(canonical)
        return tuple(records)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(
    root: Path,
    *arguments: str,
    input_text: Optional[str] = None,
    literal_paths: bool = True,
) -> subprocess.CompletedProcess[str]:
    command = ["git"]
    if literal_paths:
        command.append("--literal-pathspecs")
    return subprocess.run(
        [*command, "-C", str(root), *arguments],
        capture_output=True,
        text=True,
        input=input_text,
        check=False,
    )


def require_git_success(result: subprocess.CompletedProcess[str], action: str) -> str:
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "Git command failed"
        raise RetirementError(f"{action}: {detail}")
    return result.stdout.strip()


def load_json(path: Path) -> Mapping[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise RetirementError(f"manifest is not a regular file: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise RetirementError(f"invalid JSON manifest: {error}") from error
    if not isinstance(value, dict):
        raise RetirementError("manifest must be a JSON object")
    return value


def exact_keys(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        details = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if extra:
            details.append("unexpected " + ", ".join(extra))
        raise RetirementError(f"{label} has invalid fields ({'; '.join(details)})")


def repository_root(value: Any) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise RetirementError("repository_root must be a nonempty absolute path")
    raw = Path(value)
    if not raw.is_absolute() or raw.is_symlink() or not raw.is_dir():
        raise RetirementError("repository_root must be an existing non-symlink directory")
    root = raw.resolve()
    top = git(root, "rev-parse", "--show-toplevel")
    if top.returncode != 0:
        raise RetirementError("repository_root is not a Git working tree")
    if Path(top.stdout.strip()).resolve() != root:
        raise RetirementError("repository_root must be the Git top-level directory")
    require_git_success(git(root, "rev-parse", "--verify", "HEAD"), "Git HEAD required")
    return root


def repo_path(
    root: Path, value: Any, label: str, *, allow_missing: bool = False
) -> tuple[Path, bool]:
    if not isinstance(value, str) or not value.strip():
        raise RetirementError(f"{label} path must be nonempty")
    supplied = Path(value)
    candidate = supplied if supplied.is_absolute() else root / supplied
    candidate = Path(os.path.abspath(candidate))
    try:
        relative = candidate.relative_to(root)
    except ValueError as error:
        raise RetirementError(f"{label} is outside repository_root: {candidate}") from error

    current = root
    for component in relative.parts:
        current /= component
        if current.is_symlink():
            raise RetirementError(f"{label} may not use a symlink: {current}")
        if not current.exists() and current != candidate:
            raise RetirementError(f"{label} has a missing parent directory: {current}")
    if not candidate.exists():
        if allow_missing:
            return candidate, False
        raise RetirementError(f"{label} does not exist: {candidate}")
    if not candidate.is_file():
        raise RetirementError(f"{label} is not a regular file: {candidate}")
    return candidate, True


def require_no_sidecars(database: Path, label: str) -> None:
    sidecars = [Path(str(database) + suffix) for suffix in SIDECAR_SUFFIXES]
    present = [str(path) for path in sidecars if path.exists() or path.is_symlink()]
    if present:
        raise RetirementError(f"{label} has live SQLite sidecar(s): {', '.join(present)}")


def file_identity(path: Path, label: str) -> FileIdentity:
    try:
        metadata = path.lstat()
    except OSError as error:
        raise RetirementError(f"{label} is no longer accessible: {path}: {error}") from error
    if stat.S_ISLNK(metadata.st_mode):
        raise RetirementError(f"{label} became a symlink: {path}")
    if not stat.S_ISREG(metadata.st_mode):
        raise RetirementError(f"{label} is no longer a regular file: {path}")
    return FileIdentity(
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_size,
        metadata.st_mtime_ns,
    )


def file_record(
    root: Path,
    value: Any,
    label: str,
    kind: str,
    *,
    allow_missing: bool = False,
    digest_required: bool = True,
    allow_digest_mismatch: bool = False,
) -> FileRecord:
    if not isinstance(value, dict):
        raise RetirementError(f"{label} must be an object")
    expected_fields = {"path", "sha256"} if digest_required else {"path"}
    exact_keys(value, expected_fields, label)
    digest = value.get("sha256")
    if digest_required and (
        not isinstance(digest, str) or SHA256_RE.fullmatch(digest) is None
    ):
        raise RetirementError(f"{label}.sha256 must be 64 lowercase hexadecimal characters")
    path, present = repo_path(root, value["path"], label, allow_missing=allow_missing)
    allowed_suffixes = {"canonical": {".md", ".markdown"}, "database": {".sqlite"}}
    if path.suffix.lower() not in allowed_suffixes[kind]:
        expected = ", ".join(sorted(allowed_suffixes[kind]))
        raise RetirementError(f"{label} must use one of these extensions: {expected}")
    digest_matches = None
    observed_digest = None
    identity = None
    if present:
        identity = file_identity(path, label)
        observed_digest = sha256_file(path)
        if file_identity(path, label) != identity:
            raise RetirementError(f"{label} changed while its digest was read: {path}")
    if observed_digest is not None and digest is not None:
        digest_matches = observed_digest == digest
        if not digest_matches and not allow_digest_mismatch:
            raise RetirementError(
                f"{label} digest changed: expected {digest}, found {observed_digest} ({path})"
            )
    elif digest is not None:
        digest_matches = False
    return FileRecord(
        path, digest, present, digest_matches, observed_digest, identity
    )


def validate_database_pair(
    database: FileRecord,
    canonical: FileRecord,
    label: str,
    *,
    require_current: bool,
) -> None:
    helper = (
        Path(__file__).resolve().parents[2]
        / "research-mathematics"
        / "scripts"
        / "research_memory.py"
    )
    completed = subprocess.run(
        [sys.executable, str(helper), "check", "--db", str(database.path)],
        capture_output=True,
        text=True,
        check=False,
    )
    output = completed.stdout.strip() or completed.stderr
    try:
        result = json.loads(output)
    except json.JSONDecodeError as error:
        raise RetirementError(f"{label} validator did not emit JSON") from error
    if completed.returncode != 0 or not result.get("ok"):
        raise RetirementError(
            f"{label} failed research-memory check: {result.get('error', 'unknown error')}"
        )
    if require_current and result.get("canonical_status") != "current":
        raise RetirementError(
            f"{label} canonical status is not current; consolidate it before retirement"
        )

    identity = subprocess.run(
        [
            sys.executable,
            str(helper),
            "ensure",
            "--canonical",
            str(canonical.path),
            "--db",
            str(database.path),
            "--require-existing",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    identity_output = identity.stdout.strip() or identity.stderr
    try:
        identity_result = json.loads(identity_output)
    except json.JSONDecodeError as error:
        raise RetirementError(f"{label} identity validator did not emit JSON") from error
    if identity.returncode != 0 or not identity_result.get("ok"):
        raise RetirementError(
            f"{label} does not belong to its paired canonical: "
            + identity_result.get("error", "unknown error")
        )
    revalidate_record(database)
    revalidate_record(canonical)


def revalidate_record(record: FileRecord, *, require_expected: bool = False) -> None:
    if not record.present or record.identity is None or record.observed_sha256 is None:
        raise RetirementError(f"file was absent during preflight: {record.path}")
    identity = file_identity(record.path, "file")
    if identity != record.identity:
        raise RetirementError(f"file identity changed after preflight: {record.path}")
    current_digest = sha256_file(record.path)
    if file_identity(record.path, "file") != identity:
        raise RetirementError(f"file changed while being revalidated: {record.path}")
    if current_digest != record.observed_sha256:
        raise RetirementError(f"file content changed after preflight: {record.path}")
    if require_expected and (
        record.sha256 is None or current_digest != record.sha256
    ):
        raise RetirementError(f"file no longer matches its expected digest: {record.path}")


def relative_posix(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def require_tracked_clean(root: Path, record: FileRecord) -> None:
    relative = relative_posix(root, record.path)
    tracked = git(root, "ls-files", "--error-unmatch", "--", relative)
    if tracked.returncode != 0:
        raise RetirementError(f"source is untracked and cannot be recovered from Git: {record.path}")

    # Both flags tell Git to omit worktree changes from ordinary diff checks.
    # Only the normal `H` tag provides the recovery guarantee used below.
    index_state = git(root, "ls-files", "-v", "-z", "--", relative)
    state_output = require_git_success(
        index_state, f"could not inspect Git index flags for {record.path}"
    )
    if not state_output or state_output[0] != "H":
        raise RetirementError(
            "source has assume-unchanged, skip-worktree, or another unsafe "
            f"Git index state: {record.path}"
        )

    unmerged = require_git_success(
        git(root, "ls-files", "--unmerged", "--", relative),
        f"could not inspect {record.path}",
    )
    if unmerged:
        raise RetirementError(f"source has an unresolved Git merge: {record.path}")

    staged = git(root, "diff", "--cached", "--quiet", "HEAD", "--", relative)
    if staged.returncode not in (0, 1):
        require_git_success(staged, f"could not inspect staged state for {record.path}")
    if staged.returncode == 1:
        raise RetirementError(f"source has staged changes: {record.path}")

    unstaged = git(root, "diff", "--quiet", "--", relative)
    if unstaged.returncode not in (0, 1):
        require_git_success(unstaged, f"could not inspect working-tree state for {record.path}")
    if unstaged.returncode == 1:
        raise RetirementError(f"source has unstaged changes: {record.path}")

    # check-ignore does not accept literal pathspec magic, but --stdin consumes
    # pathnames rather than pathspecs. NUL framing also handles newlines safely.
    ignored = git(
        root,
        "check-ignore",
        "--no-index",
        "--quiet",
        "-z",
        "--stdin",
        input_text=relative + "\0",
        literal_paths=False,
    )
    if ignored.returncode not in (0, 1):
        require_git_success(ignored, f"could not inspect ignore state for {record.path}")
    if ignored.returncode == 0:
        raise RetirementError(f"source is ignored by Git rules: {record.path}")


def build_plan(manifest_path: Path, *, require_targets: bool) -> RetirementPlan:
    manifest = load_json(manifest_path)
    exact_keys(manifest, {"repository_root", "target", "sources"}, "manifest")
    root = repository_root(manifest["repository_root"])

    target = manifest["target"]
    if not isinstance(target, dict):
        raise RetirementError("target must be an object")
    exact_keys(target, {"canonical", "database"}, "target")
    target_canonical = file_record(
        root,
        target["canonical"],
        "target.canonical",
        "canonical",
        allow_missing=not require_targets,
        allow_digest_mismatch=not require_targets,
    )
    target_database = file_record(
        root,
        target["database"],
        "target.database",
        "database",
        allow_missing=not require_targets,
        digest_required=False,
    )
    require_no_sidecars(target_database.path, "target.database")
    if target_canonical.present != target_database.present:
        raise RetirementError("target pair is incomplete; both paths must exist or both be absent")
    if target_database.present:
        validate_database_pair(
            target_database,
            target_canonical,
            "target.database",
            require_current=True,
        )

    sources = manifest["sources"]
    if not isinstance(sources, list) or not sources:
        raise RetirementError("sources must be a nonempty array")

    pairs = []
    seen_paths: set[Path] = set()
    if target_canonical.path == target_database.path:
        raise RetirementError("target canonical and database resolve to the same file")
    seen_identities = {
        (record.path.stat().st_dev, record.path.stat().st_ino)
        for record in (target_canonical, target_database)
        if record.present
    }
    if target_canonical.present and target_database.present and len(seen_identities) != 2:
        raise RetirementError("target canonical and database resolve to the same file")

    for index, value in enumerate(sources):
        label = f"sources[{index}]"
        if not isinstance(value, dict):
            raise RetirementError(f"{label} must be an object")
        if set(value) not in ({"canonical"}, {"canonical", "database"}):
            raise RetirementError(
                f"{label} must contain canonical and may contain one located database"
            )
        canonical = file_record(
            root, value["canonical"], f"{label}.canonical", "canonical"
        )
        database = None
        if "database" in value:
            if value["database"] is None:
                raise RetirementError(f"{label}.database must be omitted when no companion is located")
            database = file_record(
                root, value["database"], f"{label}.database", "database"
            )
            require_no_sidecars(database.path, f"{label}.database")
        else:
            default_database = canonical.path.with_name(
                canonical.path.stem + ".research.sqlite"
            )
            if default_database.exists() or default_database.is_symlink():
                raise RetirementError(
                    f"{label}.database was omitted but the adjacent default companion exists: "
                    f"{default_database}"
                )

        for record in (canonical, database):
            if record is None:
                continue
            identity = (record.path.stat().st_dev, record.path.stat().st_ino)
            if record.path in seen_paths or identity in seen_identities:
                raise RetirementError(f"duplicate or target-overlapping source: {record.path}")
            seen_paths.add(record.path)
            seen_identities.add(identity)
            require_tracked_clean(root, record)
        if database is not None:
            validate_database_pair(
                database,
                canonical,
                f"{label}.database",
                require_current=False,
            )
        pairs.append((canonical, database))

    return RetirementPlan(root, target_canonical, target_database, tuple(pairs))


def plan_payload(plan: RetirementPlan) -> dict[str, Any]:
    return {
        "repository_root": str(plan.repository_root),
        "target": {
            "canonical": {
                "path": str(plan.target_canonical.path),
                "sha256": plan.target_canonical.sha256,
            },
            "database": {
                "path": str(plan.target_database.path),
            },
        },
        "target_ready": plan.target_ready,
        "target_state": (
            "ready"
            if plan.target_ready
            else "candidate_pending"
            if plan.target_canonical.present
            else "absent"
        ),
        "sources": [
            {
                "canonical": {"path": str(canonical.path), "sha256": canonical.sha256},
                **(
                    {"database": {"path": str(database.path), "sha256": database.sha256}}
                    if database is not None
                    else {}
                ),
            }
            for canonical, database in plan.source_pairs
        ],
        "retirement_order": [str(record.path) for record in plan.retirement_order],
    }


def command_check(args: argparse.Namespace) -> dict[str, Any]:
    plan = build_plan(Path(args.manifest), require_targets=False)
    return {"ok": True, "command": "check", "eligible": True, **plan_payload(plan)}


def remaining_paths(records: Sequence[FileRecord]) -> list[str]:
    return [
        str(record.path)
        for record in records
        if record.path.exists() or record.path.is_symlink()
    ]


def retirement_failure(
    error: Exception, records: Sequence[FileRecord], deleted: Sequence[str]
) -> dict[str, Any]:
    return {
        "ok": False,
        "command": "apply",
        "error": f"source retirement stopped: {error}",
        "deleted": list(deleted),
        "remaining": remaining_paths(records),
    }


def revalidate_target(plan: RetirementPlan) -> None:
    revalidate_record(plan.target_canonical, require_expected=True)
    revalidate_record(plan.target_database)
    require_no_sidecars(plan.target_database.path, "target.database")
    validate_database_pair(
        plan.target_database,
        plan.target_canonical,
        "target.database",
        require_current=True,
    )


def command_apply(args: argparse.Namespace) -> dict[str, Any]:
    plan = build_plan(Path(args.manifest), require_targets=True)
    records = plan.retirement_order
    deleted: list[str] = []
    try:
        # Source preflight may be slow; prove the closed target is still exact.
        revalidate_target(plan)
    except (OSError, RetirementError) as error:
        return retirement_failure(error, records, deleted)

    paired_canonicals = {
        database.path: canonical
        for canonical, database in plan.source_pairs
        if database is not None
    }
    for record in records:
        try:
            if record.path in paired_canonicals:
                require_no_sidecars(record.path, "source database")
                validate_database_pair(
                    record,
                    paired_canonicals[record.path],
                    "source database",
                    require_current=False,
                )
            require_tracked_clean(plan.repository_root, record)
            revalidate_record(record, require_expected=True)
            record.path.unlink()
            deleted.append(str(record.path))
        except (OSError, RetirementError) as error:
            return retirement_failure(error, records, deleted)

    remaining = remaining_paths(records)
    if remaining:
        return {
            "ok": False,
            "command": "apply",
            "error": "source path reappeared during retirement",
            "deleted": deleted,
            "remaining": remaining,
        }
    return {
        "ok": True,
        "command": "apply",
        "deleted": deleted,
        "remaining": [],
        "target": {
            "canonical": str(plan.target_canonical.path),
            "database": str(plan.target_database.path),
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = JSONArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name, handler in (("check", command_check), ("apply", command_apply)):
        command = commands.add_parser(name)
        command.add_argument("--manifest", required=True)
        command.set_defaults(handler=handler)
    return parser


def emit(value: Mapping[str, Any], stream: Any = sys.stdout) -> None:
    json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
    stream.write("\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        result = args.handler(args)
        emit(result, sys.stdout if result.get("ok") else sys.stderr)
        return 0 if result.get("ok") else 1
    except (RetirementError, OSError, subprocess.SubprocessError) as error:
        emit({"ok": False, "error": str(error)}, sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
