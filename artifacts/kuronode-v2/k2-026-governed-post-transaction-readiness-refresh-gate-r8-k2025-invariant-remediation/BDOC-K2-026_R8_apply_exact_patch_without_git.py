#!/usr/bin/env python3
"""Apply the R8 K2-026 exact patch without invoking git."""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

PATCH = pathlib.Path('/home/dad/BLK-System/artifacts/kuronode-v2/k2-026-governed-post-transaction-readiness-refresh-gate-r8-k2025-invariant-remediation/BDOC-K2-026_R8_k2025_invariant_remediation_exact_patch.diff')
EXPECTED = 'sha256:bf890b0a920ecf28c8dd3162614d4538cc60f5ed7d7b67ee4c9cf4ccb6824d6b'


def main() -> int:
    data = PATCH.read_bytes()
    actual = "sha256:" + hashlib.sha256(data).hexdigest()
    if actual != EXPECTED:
        print(f"patch hash mismatch: {actual} != {EXPECTED}", file=sys.stderr)
        return 2
    return subprocess.run([
        "patch",
        "-p1",
        "--batch",
        "--forward",
        "--reject-file=-",
        "--no-backup-if-mismatch",
        "-i",
        str(PATCH),
    ], text=True).returncode


if __name__ == "__main__":
    raise SystemExit(main())
