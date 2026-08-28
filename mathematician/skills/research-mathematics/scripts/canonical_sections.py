#!/usr/bin/env python3
"""Read the small canonical-Markdown contract used by research memory."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Mapping


FINGERPRINT_VERSION = 1
KEY_PATTERN = r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*"
KEY_RE = re.compile(KEY_PATTERN + r"\Z")
LABEL_RE = re.compile(r"^\*\*Research key:\*\* `(?P<key>" + KEY_PATTERN + r")`$")
ATX_RE = re.compile(r"^(?P<marks>#{1,6})(?:[ \t]+(?P<title>.*?)[ \t]*|[ \t]*)$")
FENCE_RE = re.compile(r"^ {0,3}(?P<run>`{3,}|~{3,})(?P<rest>.*)$")
MEMORY_RE = re.compile(r"^research_memory: (?P<path>\./[^\s#]+\.research\.sqlite)$")


class CanonicalSectionsError(Exception):
    """The canonical document does not satisfy the narrow indexing contract."""

    def __init__(self, errors: str | list[str]) -> None:
        self.errors = (errors,) if isinstance(errors, str) else tuple(errors)
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True)
class CanonicalSection:
    key: str | None
    title: str
    level: int
    heading_line: int
    start_line: int
    end_line: int
    start_byte: int
    end_byte: int
    ancestry: tuple[str, ...]
    section_sha256: str
    fingerprint_version: int = FINGERPRINT_VERSION

    def metadata(self) -> dict[str, object]:
        return {
            "key": self.key,
            "title": self.title,
            "heading_level": self.level,
            "heading_line": self.heading_line,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "ancestry": list(self.ancestry),
            "section_sha256": self.section_sha256,
            "fingerprint_version": self.fingerprint_version,
        }


@dataclass(frozen=True)
class CanonicalDocument:
    path: Path
    memory_relative_path: str
    memory_path: Path
    memory_declared: bool
    canonical_sha256: str
    sections: tuple[CanonicalSection, ...]
    by_key: Mapping[str, CanonicalSection]
    raw: bytes = field(repr=False, compare=False)

    def metadata(self) -> dict[str, object]:
        return {
            "canonical": str(self.path),
            "research_memory": self.memory_relative_path,
            "research_memory_declared": self.memory_declared,
            "canonical_sha256": self.canonical_sha256,
            "fingerprint_version": FINGERPRINT_VERSION,
            "section_count": len(self.sections),
            "research_key_count": len(self.by_key),
        }

    def section_markdown(self, section: CanonicalSection) -> str:
        return self.raw[section.start_byte : section.end_byte].decode("utf-8")


@dataclass
class _Heading:
    index: int
    level: int
    title: str
    ancestry: tuple[str, ...]
    key: str | None = None
    key_index: int | None = None


def _line_text(line: bytes) -> str:
    if line.endswith(b"\r\n"):
        line = line[:-2]
    elif line.endswith((b"\n", b"\r")):
        line = line[:-1]
    return line.decode("utf-8")


def _title(match: re.Match[str]) -> str:
    title = (match.group("title") or "").strip()
    return re.sub(r"[ \t]+#+[ \t]*$", "", title).strip()


def _front_matter(
    lines: list[bytes], errors: list[str], *, allow_missing_memory: bool
) -> tuple[str | None, int]:
    if not lines or _line_text(lines[0]) != "---":
        if not allow_missing_memory:
            errors.append("line 1: canonical Markdown must start with front matter")
        return None, 0
    end = next(
        (index for index in range(1, len(lines)) if _line_text(lines[index]) == "---"),
        None,
    )
    if end is None:
        errors.append("line 1: front matter is not closed by an exact '---' line")
        return None, len(lines)

    memory: str | None = None
    for index in range(1, end):
        text = _line_text(lines[index])
        match = MEMORY_RE.fullmatch(text)
        if match:
            if memory is not None:
                errors.append(f"line {index + 1}: duplicate research_memory scalar")
            memory = match.group("path")
        elif text.startswith("research_memory"):
            errors.append(
                f"line {index + 1}: expected "
                "'research_memory: ./NAME.research.sqlite'"
            )
    if memory is None:
        if not allow_missing_memory:
            errors.append("front matter requires research_memory: ./NAME.research.sqlite")
    elif any(part == ".." for part in Path(memory[2:]).parts):
        errors.append("research_memory path must not contain '..'")
    return memory, end + 1


def _fingerprint(
    lines: list[bytes],
    heading: _Heading,
    end: int,
    key_lines: set[int],
) -> str:
    subtree = b"".join(
        line
        for index, line in enumerate(lines[heading.index : end], heading.index)
        if index not in key_lines
    ).replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    payload = {
        "version": FINGERPRINT_VERSION,
        "ancestry": list(heading.ancestry),
        "subtree": subtree.decode("utf-8"),
    }
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def scan_bytes(
    data: bytes,
    path: str | Path = "<memory>",
    *,
    allow_missing_memory: bool = False,
) -> CanonicalDocument:
    """Parse one BOM-free UTF-8 snapshot without changing it."""
    if data.startswith(b"\xef\xbb\xbf"):
        raise CanonicalSectionsError("canonical Markdown must be BOM-free UTF-8")
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CanonicalSectionsError(
            f"canonical Markdown is not valid UTF-8 at byte {error.start}"
        ) from error

    lines = data.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))

    errors: list[str] = []
    memory_relative, body_start = _front_matter(
        lines, errors, allow_missing_memory=allow_missing_memory
    )
    headings: list[_Heading] = []
    stack: list[_Heading] = []
    pending: _Heading | None = None
    fence: tuple[str, int] | None = None

    for index in range(body_start, len(lines)):
        text = _line_text(lines[index])
        fence_match = FENCE_RE.match(text)
        if fence is not None:
            if (
                fence_match
                and fence_match.group("run")[0] == fence[0]
                and len(fence_match.group("run")) >= fence[1]
                and not fence_match.group("rest").strip()
            ):
                fence = None
            continue
        if fence_match:
            pending = None
            fence = (fence_match.group("run")[0], len(fence_match.group("run")))
            continue

        match = ATX_RE.fullmatch(text)
        if match:
            level = len(match.group("marks"))
            while stack and stack[-1].level >= level:
                stack.pop()
            heading = _Heading(
                index, level, _title(match), tuple(item.title for item in stack)
            )
            headings.append(heading)
            stack.append(heading)
            pending = heading
            continue

        if text.startswith("**Research key"):
            label = LABEL_RE.fullmatch(text)
            if label is None:
                errors.append(f"line {index + 1}: malformed Research key label")
            elif pending is None:
                errors.append(
                    f"line {index + 1}: Research key must be the first nonblank line after an ATX heading"
                )
            else:
                pending.key = label.group("key")
                pending.key_index = index
            pending = None
        elif text.strip():
            pending = None

    if fence is not None:
        errors.append("unterminated fenced code block")

    seen: dict[str, int] = {}
    for heading in headings:
        if heading.key is not None:
            previous = seen.get(heading.key)
            if previous is not None:
                errors.append(
                    f"line {(heading.key_index or heading.index) + 1}: duplicate Research key {heading.key!r}; "
                    f"first declared on line {previous}"
                )
            else:
                seen[heading.key] = (heading.key_index or heading.index) + 1
    if errors:
        raise CanonicalSectionsError(errors)

    key_lines = {
        heading.key_index for heading in headings if heading.key_index is not None
    }
    sections: list[CanonicalSection] = []
    by_key: dict[str, CanonicalSection] = {}
    for position, heading in enumerate(headings):
        end = next(
            (
                later.index
                for later in headings[position + 1 :]
                if later.level <= heading.level
            ),
            len(lines),
        )
        section = CanonicalSection(
            key=heading.key,
            title=heading.title,
            level=heading.level,
            heading_line=heading.index + 1,
            start_line=heading.index + 1,
            end_line=end,
            start_byte=offsets[heading.index],
            end_byte=offsets[end],
            ancestry=heading.ancestry,
            section_sha256=_fingerprint(lines, heading, end, key_lines),
        )
        sections.append(section)
        if section.key is not None:
            by_key[section.key] = section

    canonical_path = Path(path)
    memory_declared = memory_relative is not None
    if memory_relative is None:
        memory_relative = f"./{canonical_path.stem}.research.sqlite"
    # Keep the declared spelling.  Resolving here would erase the very symlink
    # components that callers must reject before opening or creating SQLite.
    memory_path = canonical_path.parent / memory_relative[2:]
    return CanonicalDocument(
        path=canonical_path,
        memory_relative_path=memory_relative,
        memory_path=memory_path,
        memory_declared=memory_declared,
        canonical_sha256=hashlib.sha256(data).hexdigest(),
        sections=tuple(sections),
        by_key=MappingProxyType(by_key),
        raw=data,
    )


def scan_canonical(
    path: str | Path, *, allow_missing_memory: bool = False
) -> CanonicalDocument:
    """Read and scan one regular, non-symlink canonical Markdown file."""
    canonical = Path(path)
    if canonical.is_symlink() or not canonical.is_file():
        raise CanonicalSectionsError(
            f"canonical must be a regular non-symlink file: {canonical}"
        )
    document = scan_bytes(
        canonical.read_bytes(),
        canonical.resolve(),
        allow_missing_memory=allow_missing_memory,
    )
    root = document.path.parent
    current = root
    for part in Path(document.memory_relative_path[2:]).parts:
        current = current / part
        if current.is_symlink():
            raise CanonicalSectionsError(
                "research_memory path must not traverse a symlink: "
                f"{document.memory_relative_path}"
            )
    try:
        current.resolve(strict=False).relative_to(root.resolve(strict=True))
    except (FileNotFoundError, ValueError) as error:
        raise CanonicalSectionsError(
            "research_memory path must remain within the canonical directory"
        ) from error
    return document
