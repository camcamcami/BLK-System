# BLK-SYSTEM-110 Task 001 Outcome — Exit-Code Taxonomy Split

**Status:** COMPLETE
**Date:** 2026-05-14
**Plan:** `docs/plans/blk-system-110_exit-code-taxonomy-split.md`
**Record:** `docs/BLK-110_exit-code-taxonomy-split.md`

## Summary

Implemented HR-009 exit-code taxonomy hardening. Invalid payload now uses Exit 8, validation/syntax failure remains Exit 2, and protected allowlist/unauthorized mutation remains Exit 3.

## Markers

```text
BLK_SYSTEM_110_EXIT_CODE_TAXONOMY_SPLIT
INVALID_PAYLOAD_EXIT_CODE_8
SYNTAX_VALIDATION_FAILURE_REMAINS_EXIT_CODE_2
PROTECTED_ALLOWLIST_VIOLATIONS_REMAIN_EXIT_CODE_3
```

## RED Evidence

Observed before implementation:

```text
go test ./internal/pipe ./internal/contracts -run 'TestExitCodes|TestReportJSONIncludesStableV47FieldsWhenEmpty|TestRunRejectsExecuteWithoutValidationBeforeEngine' -count=1 -v
FAIL: ExitInvalidPayload = 2, want 8; invalid payload and validation failure share code 2.

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_pipe_adapter.BlkPipeAdapterTest.test_return_code_routes_strict_v47 python.test_blk_pipe_adapter.BlkPipeAdapterTest.test_return_code_rejects_cross_taxonomy_status_laundering -v
FAILED: code 8 mapped to INTERNAL_ERROR; code 2 accepted INVALID_PAYLOAD status.
```

## GREEN Evidence

```text
go test ./internal/pipe ./internal/contracts -run 'TestExitCodes|TestReportJSONIncludesStableV47FieldsWhenEmpty|TestRunRejectsExecuteWithoutValidationBeforeEngine' -count=1 -v
PASS

go test ./internal/pipe ./internal/contracts -count=1
ok github.com/camcamcami/BLK-System/internal/pipe
ok github.com/camcamcami/BLK-System/internal/contracts

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_pipe_adapter -v
OK (36 tests)
```

## Authority Boundary

Task 001 does not authorize target-repo BLK-pipe dispatch, BLK-test runtime execution, BEO publication, RTM generation/drift rejection, protected-body reads, production `blk-link`, signer/storage/ledger/rollback behavior, package/network/model/browser/cyber tooling, or source/Git mutation outside the BLK-System sprint commit.
