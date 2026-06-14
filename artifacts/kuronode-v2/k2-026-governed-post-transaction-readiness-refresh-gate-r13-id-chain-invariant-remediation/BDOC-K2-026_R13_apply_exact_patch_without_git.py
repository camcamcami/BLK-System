#!/usr/bin/env python3
"""Apply the R13 K2-026 exact patch without invoking git."""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

PATCH = pathlib.Path('/home/dad/BLK-System/artifacts/kuronode-v2/k2-026-governed-post-transaction-readiness-refresh-gate-r13-id-chain-invariant-remediation/BDOC-K2-026_R13_id_chain_invariant_exact_patch.diff')
EXPECTED = 'sha256:a10e93ab6e8939be01021c2152ead372360ffab520ba5da0d2af30bde4393cbc'


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
