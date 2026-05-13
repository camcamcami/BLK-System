# BLK-SYSTEM-109 Sprint Closeout — Protected Exact Root/Directory Hardening

**Status:** COMPLETE
**Date:** 2026-05-14
**Sprint:** BLK-SYSTEM-109
**Plan:** `docs/plans/blk-system-109_protected-exact-root-directory-hardening.md`
**Record:** `docs/BLK-109_protected-exact-root-directory-hardening.md`
**Hostile review:** `docs/reviews/BLK-SYSTEM-109_hostile-review.md`

## Summary

BLK-SYSTEM-109 closes HR-007 and HR-008. Go allowlist validation/preflight now treats protected exact roots and existing directories as denied before engine side effects, and Python BLK-test runtime helpers reject exact protected source roots through a shared no-read guard.

## Required Markers

```text
BLK_SYSTEM_109_PROTECTED_EXACT_ROOT_DIRECTORY_HARDENED
PROTECTED_DOCS_EXACT_ROOTS_REJECTED
GO_ALLOWLIST_REQUIRES_EXACT_FILES_BEFORE_ENGINE
PYTHON_BLK_TEST_SOURCE_SCOPE_REJECTS_PROTECTED_ROOTS
```

## Verification

```text
go test ./internal/contracts ./internal/pipe -count=1
ok github.com/camcamcami/BLK-System/internal/contracts
ok github.com/camcamcami/BLK-System/internal/pipe

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_test_kuronode_workspace_read_only_pilot_runtime python.test_blk_test_kuronode_workspace_bounded_evidence_refresh python.test_blk_test_non_disposable_l4_runtime_pilot python.test_blk_test_fixed_tool_l4_disposable_repo_runtime -v
OK (50 tests)
```

## Authority Boundary

BLK-SYSTEM-109 is local hardening only. It grants no target-repo BLK-pipe dispatch, no BLK-test runtime execution, no BEO publication, no RTM generation or drift rejection, no protected-body reads, no production `blk-link`, no signer/storage/ledger/rollback authority, no package/network/model/browser/cyber tooling, and no source/Git mutation outside exact BLK-System sprint files.

## Next Sprint

Proceed to BLK-SYSTEM-110 — Exit-Code Taxonomy Split for HR-009.
