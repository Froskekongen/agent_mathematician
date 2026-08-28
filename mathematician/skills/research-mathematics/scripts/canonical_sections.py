#!/usr/bin/env python3
"""Index and safely assign semantic research keys to Markdown sections."""

from __future__ import annotations

import argparse
import errno
import fcntl
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple, Union


FINGERPRINT_VERSION = 1
ANCHOR_PREFIX = "research-key--"
KEY_PATTERN = r"[a-z0-9]+(?:-[a-z0-9]+)*(?:/[a-z0-9]+(?:-[a-z0-9]+)*)?"
KEY_RE = re.compile(KEY_PATTERN + r"\Z")
ANCHOR_RE = re.compile(
    r'^<a id="' + re.escape(ANCHOR_PREFIX) + r"(?P<key>" + KEY_PATTERN + r')"></a>[ \t]*$'
)
LABEL_RE = re.compile(r"^\*\*Research (?P<plural>keys?):\*\*[ \t]+(?P<body>.*?)[ \t]*$")
LABEL_KEY_RE = re.compile(r"`(?P<key>" + KEY_PATTERN + r")`")
ATX_RE = re.compile(r"^(?P<marks>#{1,6})(?:[ \t]+(?P<title>.*?)[ \t]*|[ \t]*)$")
FENCE_RE = re.compile(r"^ {0,3}(?P<run>`{3,}|~{3,})(?P<info>.*)$")
MALFORMED_ATX_RE = re.compile(r"^#{1,6}\S")
INDENTED_ATX_RE = re.compile(r"^[ \t]+#{1,6}(?:[ \t]|$)")
COMMONMARK_BLOCK_TAGS = (
    "address|article|aside|base|basefont|blockquote|body|caption|center|col|"
    "colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|"
    "footer|form|frame|frameset|h[1-6]|head|header|hr|html|iframe|legend|li|"
    "link|main|menu|menuitem|nav|noframes|ol|optgroup|option|p|param|search|"
    "section|summary|table|tbody|td|tfoot|th|thead|title|tr|track|ul"
)
RAW_HTML_BLOCK_RE = re.compile(
    r"^ {0,3}(?:"
    r"<(?:script|pre|style|textarea)(?=[\t\f\r />]|$)|"
    r"<!--|<\?|<![A-Z]|<!\[CDATA\[|"
    r"</?(?:" + COMMONMARK_BLOCK_TAGS + r")(?=[\t\f\r />]|$)|"
    r"</?[A-Z][^<>]*>[ \t]*$"
    r")",
    re.IGNORECASE,
)


class CanonicalSectionsError(Exception):
    """A deterministic canonical-Markdown validation or conflict error."""

    def __init__(self, errors: Union[str, Sequence[str]]) -> None:
        if isinstance(errors, str):
            self.errors = (errors,)
        else:
            self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


class CanonicalMutationCommittedError(CanonicalSectionsError):
    """The replacement committed, but directory durability was not confirmed."""

    def __init__(self, path: Path, installed_sha256: str, cause: OSError) -> None:
        self.path = path
        self.installed_sha256 = installed_sha256
        self.durability_error = str(cause)
        super().__init__(
            "canonical replacement committed, but directory durability was not "
            f"confirmed: {cause}"
        )


class JSONArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise CanonicalSectionsError(message)


@dataclass(frozen=True)
class CanonicalSection:
    keys: Tuple[str, ...]
    title: str
    level: int
    heading_line: int
    start_line: int
    end_line: int
    start_byte: int
    end_byte: int
    anchor_ids: Tuple[str, ...]
    ancestry: Tuple[str, ...]
    section_sha256: str
    fingerprint_version: int = FINGERPRINT_VERSION
    _heading_index: int = field(default=-1, repr=False, compare=False)
    _anchor_indices: Tuple[int, ...] = field(default=(), repr=False, compare=False)
    _anchor_separator_indices: Tuple[int, ...] = field(
        default=(), repr=False, compare=False
    )
    _label_index: Optional[int] = field(default=None, repr=False, compare=False)

    def metadata(self) -> Dict[str, Any]:
        return {
            "keys": list(self.keys),
            "anchor_ids": list(self.anchor_ids),
            "title": self.title,
            "heading_level": self.level,
            "heading_line": self.heading_line,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "start_byte": self.start_byte,
            "end_byte": self.end_byte,
            "ancestry": list(self.ancestry),
            "section_sha256": self.section_sha256,
            "fingerprint_version": self.fingerprint_version,
        }


@dataclass(frozen=True)
class CanonicalDocument:
    path: Path
    canonical_sha256: str
    sections: Tuple[CanonicalSection, ...]
    by_key: Mapping[str, CanonicalSection]
    raw: bytes = field(repr=False, compare=False)

    def metadata(self) -> Dict[str, Any]:
        addressable = sum(bool(section.keys) for section in self.sections)
        return {
            "canonical": str(self.path),
            "canonical_sha256": self.canonical_sha256,
            "fingerprint_version": FINGERPRINT_VERSION,
            "section_count": len(self.sections),
            "addressable_section_count": addressable,
            "research_key_count": len(self.by_key),
            "sections": [section.metadata() for section in self.sections],
        }

    def section_markdown(self, section: CanonicalSection) -> str:
        return self.raw[section.start_byte : section.end_byte].decode("utf-8")


@dataclass
class _Heading:
    index: int
    level: int
    title: str
    ancestry_indices: Tuple[int, ...] = ()
    anchor_indices: Tuple[int, ...] = ()
    anchor_separator_indices: Tuple[int, ...] = ()
    label_index: Optional[int] = None
    keys: Tuple[str, ...] = ()


def _strip_eol(line: bytes) -> bytes:
    if line.endswith(b"\r\n"):
        return line[:-2]
    if line.endswith((b"\n", b"\r")):
        return line[:-1]
    return line


def _line_ending(line: bytes) -> bytes:
    if line.endswith(b"\r\n"):
        return b"\r\n"
    if line.endswith(b"\n"):
        return b"\n"
    if line.endswith(b"\r"):
        return b"\r"
    return b""


def _line_text(line: bytes) -> str:
    return _strip_eol(line).decode("utf-8")


def _normalized_text(lines: Sequence[bytes]) -> str:
    return b"".join(lines).replace(b"\r\n", b"\n").decode("utf-8")


def _heading_title(match: re.Match[str]) -> str:
    title = (match.group("title") or "").strip()
    return re.sub(r"[ \t]+#+[ \t]*$", "", title).strip()


def _parse_label(line: str, line_number: int, errors: list[str]) -> Optional[Tuple[str, ...]]:
    match = LABEL_RE.fullmatch(line)
    if not match:
        if line.lstrip().startswith("**Research key"):
            errors.append(f"line {line_number}: malformed Research key label")
        return None
    body = match.group("body")
    parts = body.split(", ") if body else []
    keys: list[str] = []
    for part in parts:
        key_match = LABEL_KEY_RE.fullmatch(part)
        if not key_match:
            errors.append(f"line {line_number}: malformed Research key list")
            return ()
        keys.append(key_match.group("key"))
    if not keys:
        errors.append(f"line {line_number}: Research key label has no keys")
        return ()
    expected_plural = "key" if len(keys) == 1 else "keys"
    if match.group("plural") != expected_plural:
        errors.append(
            f"line {line_number}: use 'Research {expected_plural}' for {len(keys)} key(s)"
        )
    if len(set(keys)) != len(keys):
        errors.append(f"line {line_number}: duplicate key in Research key label")
    return tuple(keys)


def _fingerprint(
    lines: Sequence[bytes],
    heading: _Heading,
    headings: Sequence[_Heading],
    end_index: int,
    generated_indices: set[int],
) -> str:
    ancestry = [
        _strip_eol(lines[headings[index].index]).decode("utf-8")
        for index in heading.ancestry_indices
    ]
    section_lines = [
        lines[index]
        for index in range(heading.index, end_index)
        if index not in generated_indices
    ]
    payload = {
        "version": FINGERPRINT_VERSION,
        "ancestry": ancestry,
        "section": _normalized_text(section_lines),
    }
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def scan_bytes(
    data: bytes, path: Union[str, Path] = Path("<memory>")
) -> CanonicalDocument:
    """Parse and validate one canonical Markdown snapshot."""
    if data.startswith(b"\xef\xbb\xbf"):
        raise CanonicalSectionsError(
            "canonical Markdown must use BOM-free UTF-8; remove the UTF-8 BOM"
        )
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CanonicalSectionsError(
            f"canonical Markdown is not valid UTF-8 at byte {error.start}"
        ) from error

    path = Path(path)
    lines = data.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))

    errors: list[str] = []
    headings: list[_Heading] = []
    anchors: Dict[int, str] = {}
    labels: Dict[int, Tuple[str, ...]] = {}

    content_start = 0
    if lines and _line_text(lines[0]) == "---":
        for index in range(1, len(lines)):
            if _line_text(lines[index]) in ("---", "..."):
                content_start = index + 1
                break
        else:
            errors.append("line 1: unclosed top-of-file front matter")
            content_start = len(lines)

    fence_character: Optional[str] = None
    fence_length = 0
    fence_line = 0
    previous_plain_nonblank = False
    for index in range(content_start, len(lines)):
        text = _line_text(lines[index])
        line_number = index + 1
        fence_match = FENCE_RE.match(text)
        if fence_character is not None:
            if fence_match:
                run = fence_match.group("run")
                if (
                    run[0] == fence_character
                    and len(run) >= fence_length
                    and not fence_match.group("info").strip()
                ):
                    fence_character = None
            continue
        if fence_match:
            run = fence_match.group("run")
            if run[0] == "`" and "`" in fence_match.group("info"):
                pass
            else:
                fence_character = run[0]
                fence_length = len(run)
                fence_line = line_number
                previous_plain_nonblank = False
                continue

        anchor_match = ANCHOR_RE.fullmatch(text)
        if anchor_match:
            anchors[index] = anchor_match.group("key")
            previous_plain_nonblank = True
            continue
        if text.lstrip().startswith("<a id") and ANCHOR_PREFIX in text:
            errors.append(f"line {line_number}: malformed research-key anchor")
            previous_plain_nonblank = True
            continue
        if RAW_HTML_BLOCK_RE.match(text):
            errors.append(
                f"line {line_number}: unsupported CommonMark raw-HTML block "
                "opener; only generated research-key anchors are allowed"
            )
            previous_plain_nonblank = True
            continue

        label = _parse_label(text, line_number, errors)
        if label is not None:
            labels[index] = label
            previous_plain_nonblank = True
            continue

        heading_match = ATX_RE.fullmatch(text)
        if heading_match:
            title = _heading_title(heading_match)
            if not title:
                errors.append(f"line {line_number}: ATX heading needs a title")
            headings.append(
                _Heading(index, len(heading_match.group("marks")), title)
            )
            previous_plain_nonblank = True
            continue
        if MALFORMED_ATX_RE.match(text):
            errors.append(
                f"line {line_number}: ATX heading must have whitespace after '#'")
        elif INDENTED_ATX_RE.match(text):
            errors.append(f"line {line_number}: indexed ATX headings must start in column zero")
        elif previous_plain_nonblank and re.fullmatch(r"[=-]{3,}[ \t]*", text):
            errors.append(f"line {line_number}: Setext headings are not supported")
        previous_plain_nonblank = bool(text.strip())

    if fence_character is not None:
        errors.append(f"line {fence_line}: unclosed {fence_character * fence_length} fence")
    if not headings:
        errors.append("canonical Markdown has no column-zero ATX headings")

    used_anchors: set[int] = set()
    used_labels: set[int] = set()
    generated_separators: set[int] = set()
    stack: list[int] = []
    for position, heading in enumerate(headings):
        while stack and headings[stack[-1]].level >= heading.level:
            stack.pop()
        heading.ancestry_indices = tuple(stack)
        stack.append(position)

        cursor = heading.index - 1
        reverse_separator_indices: list[int] = []
        while cursor >= content_start and not _line_text(lines[cursor]).strip():
            reverse_separator_indices.append(cursor)
            cursor -= 1
        reverse_anchor_indices: list[int] = []
        while cursor in anchors:
            reverse_anchor_indices.append(cursor)
            cursor -= 1
        heading.anchor_indices = tuple(reversed(reverse_anchor_indices))
        used_anchors.update(heading.anchor_indices)
        if heading.anchor_indices:
            heading.anchor_separator_indices = tuple(
                reversed(reverse_separator_indices)
            )
            generated_separators.update(heading.anchor_separator_indices)
            if len(heading.anchor_separator_indices) != 1:
                errors.append(
                    f"line {heading.index + 1}: research-key anchors require exactly one blank line before the heading"
                )

        cursor = heading.index + 1
        while cursor < len(lines) and not _line_text(lines[cursor]).strip():
            cursor += 1
        if cursor in labels:
            heading.label_index = cursor
            used_labels.add(cursor)

        anchor_keys = tuple(anchors[index] for index in heading.anchor_indices)
        label_keys = labels.get(heading.label_index, ())
        if bool(anchor_keys) != bool(label_keys):
            errors.append(
                f"line {heading.index + 1}: research keys require both anchors and a visible label"
            )
        elif anchor_keys and anchor_keys != label_keys:
            errors.append(
                f"line {heading.index + 1}: anchor keys and visible Research keys differ"
            )
        heading.keys = anchor_keys if anchor_keys == label_keys else ()

    for index in sorted(set(anchors) - used_anchors):
        errors.append(f"line {index + 1}: research-key anchor is not attached to a heading")
    for index in sorted(set(labels) - used_labels):
        errors.append(f"line {index + 1}: Research key label is not attached to a heading")

    key_lines: Dict[str, int] = {}
    for heading in headings:
        for key in heading.keys:
            if key in key_lines:
                errors.append(
                    f"line {heading.index + 1}: duplicate research key '{key}' "
                    f"(first used at line {key_lines[key]})"
                )
            else:
                key_lines[key] = heading.index + 1

    if errors:
        raise CanonicalSectionsError(errors)

    generated_indices = set(anchors) | set(labels) | generated_separators
    sections: list[CanonicalSection] = []
    for position, heading in enumerate(headings):
        end_index = len(lines)
        for following in headings[position + 1 :]:
            if following.level <= heading.level:
                end_index = (
                    following.anchor_indices[0]
                    if following.anchor_indices
                    else following.index
                )
                break
        ancestry = tuple(headings[index].title for index in heading.ancestry_indices)
        section = CanonicalSection(
            keys=heading.keys,
            title=heading.title,
            level=heading.level,
            heading_line=heading.index + 1,
            start_line=heading.index + 1,
            end_line=max(heading.index + 1, end_index),
            start_byte=offsets[heading.index],
            end_byte=offsets[end_index],
            anchor_ids=tuple(ANCHOR_PREFIX + key for key in heading.keys),
            ancestry=ancestry,
            section_sha256=_fingerprint(
                lines, heading, headings, end_index, generated_indices
            ),
            _heading_index=heading.index,
            _anchor_indices=heading.anchor_indices,
            _anchor_separator_indices=heading.anchor_separator_indices,
            _label_index=heading.label_index,
        )
        sections.append(section)

    by_key = {key: section for section in sections for key in section.keys}
    return CanonicalDocument(
        path=path,
        canonical_sha256=hashlib.sha256(data).hexdigest(),
        sections=tuple(sections),
        by_key=by_key,
        raw=data,
    )


def _open_regular_file(path: Path) -> Tuple[int, os.stat_result]:
    path_info = path.lstat()
    if stat.S_ISLNK(path_info.st_mode):
        raise CanonicalSectionsError(f"canonical Markdown must not be a symlink: {path}")
    if not stat.S_ISREG(path_info.st_mode):
        raise CanonicalSectionsError(f"canonical Markdown must be a regular file: {path}")
    descriptor = os.open(
        str(path), os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    )
    opened_info = os.fstat(descriptor)
    if not stat.S_ISREG(opened_info.st_mode):
        os.close(descriptor)
        raise CanonicalSectionsError(
            f"canonical Markdown must be a regular file: {path}"
        )
    return descriptor, opened_info


def _read_descriptor(descriptor: int) -> bytes:
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        chunk = os.read(descriptor, 1024 * 1024)
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)


def _read_regular_file(path: Path) -> Tuple[bytes, int]:
    descriptor, opened_info = _open_regular_file(path)
    try:
        return _read_descriptor(descriptor), stat.S_IMODE(opened_info.st_mode)
    finally:
        os.close(descriptor)


def scan_canonical(path: Union[str, Path]) -> CanonicalDocument:
    canonical = Path(os.path.abspath(os.fspath(path)))
    data, _mode = _read_regular_file(canonical)
    return scan_bytes(data, canonical)


def _validate_key(key: str) -> None:
    if not KEY_RE.fullmatch(key):
        raise CanonicalSectionsError(
            f"invalid research key '{key}'; use a lowercase ASCII kebab key "
            "or one theory/key qualification"
        )


def _preferred_newline(lines: Sequence[bytes], heading_index: int) -> bytes:
    ending = _line_ending(lines[heading_index])
    if ending:
        return ending
    for line in lines:
        ending = _line_ending(line)
        if ending:
            return ending
    return b"\n"


def _replace_spans(data: bytes, replacements: Sequence[Tuple[int, int, bytes]]) -> bytes:
    result = data
    for start, end, replacement in sorted(replacements, reverse=True):
        result = result[:start] + replacement + result[end:]
    return result


def _atomic_replace(path: Path, data: bytes, expected_sha256: str) -> None:
    target_descriptor, locked_info = _open_regular_file(path)
    temporary_name: Optional[str] = None
    replaced = False
    try:
        try:
            fcntl.flock(
                target_descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB
            )
        except OSError as error:
            if error.errno in (errno.EACCES, errno.EAGAIN):
                raise CanonicalSectionsError(
                    "canonical Markdown is locked by another cooperating writer"
                ) from error
            raise

        current = _read_descriptor(target_descriptor)
        if hashlib.sha256(current).hexdigest() != expected_sha256:
            raise CanonicalSectionsError(
                "canonical Markdown changed after parsing; refusing to replace it"
            )

        temporary_descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
        )
        with os.fdopen(temporary_descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fchmod(stream.fileno(), stat.S_IMODE(locked_info.st_mode))
            os.fsync(stream.fileno())

        current_descriptor, current_info = _open_regular_file(path)
        try:
            same_inode = (current_info.st_dev, current_info.st_ino) == (
                locked_info.st_dev,
                locked_info.st_ino,
            )
            same_mode = stat.S_IMODE(current_info.st_mode) == stat.S_IMODE(
                locked_info.st_mode
            )
            current_digest = hashlib.sha256(
                _read_descriptor(current_descriptor)
            ).hexdigest()
        finally:
            os.close(current_descriptor)
        final_info = path.lstat()
        if (
            not same_inode
            or not same_mode
            or not stat.S_ISREG(final_info.st_mode)
            or (final_info.st_dev, final_info.st_ino)
            != (locked_info.st_dev, locked_info.st_ino)
            or stat.S_IMODE(final_info.st_mode)
            != stat.S_IMODE(locked_info.st_mode)
            or current_digest != expected_sha256
        ):
            raise CanonicalSectionsError(
                "canonical Markdown changed while preparing replacement; refusing to replace it"
            )

        os.replace(temporary_name, path)
        replaced = True
        try:
            directory_descriptor = os.open(
                str(path.parent), os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
            )
            try:
                os.fsync(directory_descriptor)
            finally:
                os.close(directory_descriptor)
        except OSError as error:
            raise CanonicalMutationCommittedError(
                path, hashlib.sha256(data).hexdigest(), error
            ) from error
    finally:
        try:
            fcntl.flock(target_descriptor, fcntl.LOCK_UN)
        except OSError:
            pass
        os.close(target_descriptor)
        if temporary_name is not None and not replaced and os.path.exists(temporary_name):
            os.unlink(temporary_name)


def set_section_keys(
    path: Union[str, Path],
    heading_line: int,
    keys: Sequence[str],
    expected_canonical_sha256: str,
) -> Tuple[CanonicalDocument, CanonicalSection, bool, str]:
    """Set all primary keys on one heading under a whole-file SHA precondition."""
    if not re.fullmatch(r"[0-9a-f]{64}", expected_canonical_sha256):
        raise CanonicalSectionsError("expected canonical SHA-256 must be 64 lowercase hex characters")
    desired = tuple(keys)
    if not desired:
        raise CanonicalSectionsError("key-set requires at least one --key")
    for key in desired:
        _validate_key(key)
    if len(set(desired)) != len(desired):
        raise CanonicalSectionsError("key-set keys must be unique")

    document = scan_canonical(path)
    if document.canonical_sha256 != expected_canonical_sha256:
        raise CanonicalSectionsError(
            "canonical SHA-256 conflict: "
            f"expected {expected_canonical_sha256}, found {document.canonical_sha256}"
        )
    matches = [section for section in document.sections if section.heading_line == heading_line]
    if not matches:
        raise CanonicalSectionsError(f"line {heading_line} is not an indexed ATX heading")
    section = matches[0]
    for key in desired:
        owner = document.by_key.get(key)
        if owner is not None and owner.heading_line != heading_line:
            raise CanonicalSectionsError(
                f"research key '{key}' already belongs to heading line {owner.heading_line}"
            )
    if section.keys == desired:
        return document, section, False, document.canonical_sha256

    lines = document.raw.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    newline = _preferred_newline(lines, section._heading_index)
    anchors = b"".join(
        f'<a id="{ANCHOR_PREFIX}{key}"></a>'.encode("utf-8") + newline
        for key in desired
    )
    label_word = "key" if len(desired) == 1 else "keys"
    label = (
        f"**Research {label_word}:** " + ", ".join(f"`{key}`" for key in desired)
    ).encode("utf-8")

    replacements: list[Tuple[int, int, bytes]] = []
    if section._anchor_indices:
        replacements.append(
            (
                offsets[section._anchor_indices[0]],
                offsets[section._anchor_indices[-1] + 1],
                anchors,
            )
        )
        assert section._label_index is not None
        label_ending = _line_ending(lines[section._label_index]) or newline
        replacements.append(
            (
                offsets[section._label_index],
                offsets[section._label_index + 1],
                label + label_ending,
            )
        )
    else:
        if not _line_ending(lines[section._heading_index]):
            raise CanonicalSectionsError(
                "key-set requires the target heading line to end with a newline"
            )
        replacements.append(
            (
                offsets[section._heading_index],
                offsets[section._heading_index],
                anchors + newline,
            )
        )
        heading_end = offsets[section._heading_index + 1]
        after_heading = label + newline
        replacements.append((heading_end, heading_end, after_heading))

    updated_raw = _replace_spans(document.raw, replacements)
    updated = scan_bytes(updated_raw, document.path)
    updated_section = updated.by_key[desired[0]]
    if updated_section.keys != desired:
        raise CanonicalSectionsError("internal key-set validation failed")
    if updated_section.section_sha256 != section.section_sha256:
        raise CanonicalSectionsError("key-set unexpectedly changed section content")

    _atomic_replace(document.path, updated_raw, expected_canonical_sha256)
    return updated, updated_section, True, document.canonical_sha256


def command_scan(args: argparse.Namespace) -> Dict[str, Any]:
    document = scan_canonical(args.canonical)
    return {"ok": True, "command": "scan", **document.metadata()}


def command_check(args: argparse.Namespace) -> Dict[str, Any]:
    path = Path(os.path.abspath(args.canonical))
    try:
        document = scan_canonical(path)
    except CanonicalSectionsError as error:
        return {
            "ok": False,
            "command": "check",
            "canonical": str(path),
            "errors": list(error.errors),
        }
    return {
        "ok": True,
        "command": "check",
        "canonical": str(path),
        "canonical_sha256": document.canonical_sha256,
        "fingerprint_version": FINGERPRINT_VERSION,
        "section_count": len(document.sections),
        "research_key_count": len(document.by_key),
        "errors": [],
    }


def command_show(args: argparse.Namespace) -> Dict[str, Any]:
    document = scan_canonical(args.canonical)
    section = document.by_key.get(args.key)
    if section is None:
        raise CanonicalSectionsError(f"unknown research key '{args.key}'")
    return {
        "ok": True,
        "command": "show",
        "canonical": str(document.path),
        "canonical_sha256": document.canonical_sha256,
        "matched_key": args.key,
        "section": {
            **section.metadata(),
            "section_md": document.section_markdown(section),
        },
    }


def command_key_set(args: argparse.Namespace) -> Dict[str, Any]:
    document, section, changed, previous_sha256 = set_section_keys(
        args.canonical,
        args.heading_line,
        args.key,
        args.expected_canonical_sha256,
    )
    return {
        "ok": True,
        "command": "key-set",
        "canonical": str(document.path),
        "changed": changed,
        "previous_canonical_sha256": previous_sha256,
        "canonical_sha256": document.canonical_sha256,
        "section": section.metadata(),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = JSONArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="emit section metadata only")
    scan_parser.add_argument("--canonical", required=True)
    scan_parser.set_defaults(handler=command_scan)

    check_parser = subparsers.add_parser("check", help="validate canonical section structure")
    check_parser.add_argument("--canonical", required=True)
    check_parser.set_defaults(handler=command_check)

    show_parser = subparsers.add_parser("show", help="emit exactly one keyed section")
    show_parser.add_argument("--canonical", required=True)
    show_parser.add_argument("--key", required=True)
    show_parser.set_defaults(handler=command_show)

    key_set_parser = subparsers.add_parser(
        "key-set", help="set all keys on one heading under a SHA-256 precondition"
    )
    key_set_parser.add_argument("--canonical", required=True)
    key_set_parser.add_argument("--heading-line", required=True, type=int)
    key_set_parser.add_argument("--key", required=True, action="append")
    key_set_parser.add_argument("--expected-canonical-sha256", required=True)
    key_set_parser.set_defaults(handler=command_key_set)
    return parser


def emit(payload: Mapping[str, Any], stream: Any = sys.stdout) -> None:
    json.dump(payload, stream, ensure_ascii=False, sort_keys=True, indent=2)
    stream.write("\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        result = args.handler(args)
        emit(result, sys.stdout if result.get("ok", True) else sys.stderr)
        return 0 if result.get("ok", True) else 1
    except CanonicalMutationCommittedError as error:
        emit(
            {
                "ok": False,
                "error": str(error),
                "committed": True,
                "durability_confirmed": False,
                "canonical": str(error.path),
                "canonical_sha256": error.installed_sha256,
                "installed_sha256": error.installed_sha256,
                "durability_error": error.durability_error,
            },
            sys.stderr,
        )
        return 1
    except (CanonicalSectionsError, OSError, KeyError, IndexError) as error:
        emit({"ok": False, "error": str(error)}, sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
