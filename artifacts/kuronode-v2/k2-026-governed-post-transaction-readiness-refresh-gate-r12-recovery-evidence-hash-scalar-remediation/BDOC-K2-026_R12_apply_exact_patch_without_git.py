#!/usr/bin/env python3
"""Apply the R12 K2-026 exact patch without invoking git."""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

PATCH = pathlib.Path('/home/dad/BLK-System/artifacts/kuronode-v2/k2-026-governed-post-transaction-readiness-refresh-gate-r12-recovery-evidence-hash-scalar-remediation/BDOC-K2-026_R12_recovery_evidence_hash_scalar_exact_patch.diff')
EXPECTED = 'sha256:b767b0559d637f71f49b71d782c25a6e8a5ad326f71de274161ebc3e4c91e322'


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
