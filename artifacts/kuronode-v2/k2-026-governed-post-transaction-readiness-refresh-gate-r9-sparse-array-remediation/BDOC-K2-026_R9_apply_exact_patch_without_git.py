#!/usr/bin/env python3
"""Apply the R9 K2-026 exact patch without invoking git."""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

PATCH = pathlib.Path('/home/dad/BLK-System/artifacts/kuronode-v2/k2-026-governed-post-transaction-readiness-refresh-gate-r9-sparse-array-remediation/BDOC-K2-026_R9_sparse_array_remediation_exact_patch.diff')
EXPECTED = 'sha256:cd797537082f6016417bf9c2a46f74cae61223488c0adc43e7b429f4cf4c460a'


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
