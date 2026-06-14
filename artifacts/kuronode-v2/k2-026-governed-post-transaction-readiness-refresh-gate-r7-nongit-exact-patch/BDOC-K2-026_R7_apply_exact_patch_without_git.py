#!/usr/bin/env python3
"""Apply the R7 K2-026 exact patch without invoking git.

BLK-pipe owns target-hash preflight, staging, validation, and commit. This helper
only hash-checks the package-owned patch bytes and invokes GNU patch against the
current working directory.
"""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

PATCH = pathlib.Path('/home/dad/BLK-System/artifacts/kuronode-v2/k2-026-governed-post-transaction-readiness-refresh-gate-r7-nongit-exact-patch/BDOC-K2-026_R7_hostile_review_remediation_exact_patch.diff')
EXPECTED = 'sha256:e068c0c71d135374cc1840eccc27ff9eeabc11dcfe9c5de7da35819ef2f97adf'


def main() -> int:
    data = PATCH.read_bytes()
    actual = "sha256:" + hashlib.sha256(data).hexdigest()
    if actual != EXPECTED:
        print(f"patch hash mismatch: {actual} != {EXPECTED}", file=sys.stderr)
        return 2
    cmd = [
        "patch",
        "-p1",
        "--batch",
        "--forward",
        "--reject-file=-",
        "--no-backup-if-mismatch",
        "-i",
        str(PATCH),
    ]
    completed = subprocess.run(cmd, text=True)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
