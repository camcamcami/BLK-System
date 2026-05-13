"""Shared no-read protected BLK-req path guards.

These helpers classify path names only. They do not read, copy, parse, hash,
summarize, scan, or mutate protected BLK-req body bytes.
"""

from __future__ import annotations

from pathlib import Path

PROTECTED_BLK_REQ_RELATIVE_ROOTS = (
    ("docs", "active"),
    ("docs", "requirements"),
    ("docs", "use_cases"),
)


def protected_blk_req_path_marker(path: Path) -> str | None:
    """Return the protected BLK-req root marker if *path* is under one.

    Classification is segment-based so exact roots such as ``docs/active`` and
    descendants such as ``docs/active/REQ-001.md`` are treated identically.
    """

    parts = path.resolve().parts
    for index in range(0, max(len(parts) - 1, 0)):
        pair = (parts[index], parts[index + 1])
        if pair in PROTECTED_BLK_REQ_RELATIVE_ROOTS:
            return "/".join(pair)
    return None


def reject_protected_blk_req_source_path(path: Path) -> None:
    marker = protected_blk_req_path_marker(path)
    if marker is not None:
        raise ValueError(f"source scope contains protected BLK-req root or descendant: {marker}")
