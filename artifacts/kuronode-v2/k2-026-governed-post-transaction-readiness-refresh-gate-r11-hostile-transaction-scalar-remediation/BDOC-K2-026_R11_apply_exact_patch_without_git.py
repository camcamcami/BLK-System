#!/usr/bin/env python3
"""Apply the R11 K2-026 exact patch without invoking git."""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

PATCH = pathlib.Path('/home/dad/BLK-System/artifacts/kuronode-v2/k2-026-governed-post-transaction-readiness-refresh-gate-r11-hostile-transaction-scalar-remediation/BDOC-K2-026_R11_hostile_transaction_scalar_exact_patch.diff')
EXPECTED = 'sha256:8cc2cc504d87973ac5a31bec2953164410c4d081d7493ffef3b6c10ac111b7f9'


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
