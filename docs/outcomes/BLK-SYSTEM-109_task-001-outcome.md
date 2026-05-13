# BLK-SYSTEM-109 Task 001 Outcome — Protected Exact Root/Directory Hardening

**Status:** COMPLETE
**Date:** 2026-05-14
**Plan:** `docs/plans/blk-system-109_protected-exact-root-directory-hardening.md`
**Record:** `docs/BLK-109_protected-exact-root-directory-hardening.md`

## Summary

Implemented HR-007 and HR-008 hardening:

- Go protected-path classification now covers exact `docs/active`, `docs/requirements`, and `docs/use_cases` roots plus descendants.
- Go wrong-class preflight rejects existing directories before engine execution and checks exact tracked-file equality rather than treating any `git ls-files` output as a tracked file.
- Python BLK-test runtime helpers now use a shared no-read path classifier to reject protected exact roots and descendants.

## Markers

```text
BLK_SYSTEM_109_PROTECTED_EXACT_ROOT_DIRECTORY_HARDENED
PROTECTED_DOCS_EXACT_ROOTS_REJECTED
GO_ALLOWLIST_REQUIRES_EXACT_FILES_BEFORE_ENGINE
PYTHON_BLK_TEST_SOURCE_SCOPE_REJECTS_PROTECTED_ROOTS
```

## RED Evidence

Observed before implementation:

```text
go test ./internal/contracts ./internal/pipe -run 'TestPayloadDecodeProtectedPathsStillFailForLegacyAndV47Allowlists|TestRunRejectsTrackedDirectoryAllowlistBeforeEngine' -count=1 -v
FAIL: exact protected roots decoded without error; tracked directory allowlist reached engine/no-candidate-diff path.

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest <four exact-root source-scope tests> -v
FAILED (failures=12): exact docs/active, docs/requirements, and docs/use_cases roots did not raise ValueError.
```

## GREEN Evidence

```text
go test ./internal/contracts ./internal/pipe -run 'TestPayloadDecodeProtectedPathsStillFailForLegacyAndV47Allowlists|TestRunRejectsTrackedDirectoryAllowlistBeforeEngine' -count=1 -v
PASS

go test ./internal/contracts ./internal/pipe -count=1
ok github.com/camcamcami/BLK-System/internal/contracts
ok github.com/camcamcami/BLK-System/internal/pipe

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_test_kuronode_workspace_read_only_pilot_runtime python.test_blk_test_kuronode_workspace_bounded_evidence_refresh python.test_blk_test_non_disposable_l4_runtime_pilot python.test_blk_test_fixed_tool_l4_disposable_repo_runtime -v
OK (50 tests)
```

## Authority Boundary

Task 001 does not authorize target-repo BLK-pipe dispatch, BLK-test runtime execution, BEO publication, RTM generation/drift rejection, protected-body reads, production `blk-link`, signer/storage/ledger/rollback behavior, package/network/model/browser/cyber tooling, or source/Git mutation outside the BLK-System sprint commit.
