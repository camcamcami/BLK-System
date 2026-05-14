# BLK-SYSTEM-122 — Exact-ID Retrieval Sprint Closeout

**Status:** Complete
**Date:** 2026-05-14T19:11:27+10:00
**Commit:** See Git commit containing this closeout

## 1. Objective

Implement deterministic BLK-req active artifact retrieval by exact `REQ-###` / `UC-###` ID without broad active-vault scanning.

## 2. Files Changed

- `python/lint_artifacts.py`
- `python/test_blk_req_legislative_gateway.py`
- `docs/plans/blk-system-122-124_blk-req-revision-lifecycle.md`
- `docs/outcomes/BLK-SYSTEM-122_sprint-closeout.md`

## 3. Implementation Summary

- Added `retrieve_active_artifact_by_exact_id()`.
- Maps `REQ-###` directly to `docs/requirements/active/<id>.md` and `UC-###` directly to `docs/use_cases/active/<id>.md`.
- Rejects malformed IDs, missing active files, symlinked active paths, ID/path metadata mismatches, invalid active metadata, and version-hash mismatch.
- Returns explicit false side-effect flags for broad active-vault scan, active-vault write, RTM, drift, BEO publication, and trace-closure protected-body use.

## 4. Verification

RED evidence:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_req_legislative_gateway.BlkReqRevisionLifecycle122To124Test -v
ImportError: cannot import name 'promote_staged_revision_to_active' from 'lint_artifacts'
```

Focused GREEN evidence:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_req_legislative_gateway.BlkReqRevisionLifecycle122To124Test -v
Ran 9 tests
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_req_legislative_gateway -v
Ran 43 tests
OK
```

Aggregate verification is recorded in the BLK-SYSTEM-124 closeout for the combined 122-124 batch.

## 5. Hostile Review / Risk Check

- Exact-ID retrieval uses direct path derivation from strict ID regexes; no `iterdir`/glob scan is needed.
- Active path guard rejects symlink traversal and workspace escape before read.
- The function reads only the exact active artifact requested by ID and does not grant downstream trace closure, RTM, BEO, BLK-test, or BLK-pipe authority.

## 6. Authority Boundary

BLK-SYSTEM-122 authorizes local deterministic exact-ID retrieval inside the BLK-req backend only. It does not authorize broad active-vault scanning, protected-body use outside the BLK-req backend path, staged revision promotion, BEB dispatch, BEO closeout/publication, BLK-pipe runtime, BLK-test runtime/MCP, RTM generation, drift rejection, non-BLK-req target/source/Git mutation, package/network/model/browser/cyber tooling, signer/storage/public-ledger/rollback behavior, or production-isolation claims.

## 7. Documentation Burden Check

- No `docs/BLK-122_*.md` was created.
- No per-task outcome documents were created.
- This single file is the BLK-SYSTEM-122 sprint outcome.
