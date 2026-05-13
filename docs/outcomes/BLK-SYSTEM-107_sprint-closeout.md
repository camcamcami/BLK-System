# BLK-SYSTEM-107 Sprint Closeout — Mandatory Validation Required

**Status:** COMPLETE
**Date:** 2026-05-14
**Sprint:** BLK-SYSTEM-107
**Plan:** `docs/plans/blk-system-107_mandatory-validation-required.md`
**Record:** `docs/BLK-107_mandatory-validation-required.md`
**Hostile review:** `docs/reviews/BLK-SYSTEM-107_hostile-review.md`

## Summary

BLK-SYSTEM-107 implements the HR-003 mandatory-validation gate. Execute payloads now fail closed before engine side effects unless they provide either non-empty repository-owned `validation_profiles` or non-empty trusted-local `validation_commands`.

## Required Markers

```text
BLK_SYSTEM_107_MANDATORY_VALIDATION_REQUIRED
EXECUTE_PAYLOAD_REQUIRES_VALIDATION_PROFILE_OR_COMMAND
VALIDATION_REQUIRED_BEFORE_ENGINE_SIDE_EFFECTS
PYTHON_ADAPTER_VALIDATION_REQUIRED_FAIL_FAST_ONLY_GO_REMAINS_AUTHORITY
```

## Implementation

- Added Go contract validation requiring a validation source for execute payloads.
- Added Go pipe regressions proving missing or explicitly empty validation is rejected before the engine creates `SHOULD_NOT_EXIST.txt`.
- Updated Go payload tests and helpers so valid execute fixtures carry validation.
- Updated Python adapter preflight so missing/empty validation raises before `blk-pipe` invocation.
- Updated Python adapter tests to prove fail-fast behavior and preserve non-empty trusted-local compatibility.
- Updated BLK-004 current-state overlay to state the mandatory execute validation requirement.

## RED/GREEN Evidence

RED failures were observed before implementation:

- Go `TestRunRejectsExecuteWithoutValidationBeforeEngine` returned `SUCCESS` and created `SHOULD_NOT_EXIST.txt` before the fix.
- Go `TestRunRejectsExecuteWithEmptyValidationBeforeEngine` returned `SUCCESS` for empty `validation_commands` and empty `validation_profiles` before the fix.
- Python `test_execute_sprint_requires_validation_before_invocation` failed because `ValueError` was not raised and `blk-pipe` was invoked before the fix.

Focused GREEN checks after implementation:

```text
go test ./internal/contracts ./internal/pipe -run 'TestPayloadValidateRejectsExecuteWithoutValidation|TestRunRejectsExecuteWithoutValidationBeforeEngine|TestRunRejectsExecuteWithEmptyValidationBeforeEngine' -count=1 -v
PASS

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_pipe_adapter.BlkPipeAdapterTest.test_execute_sprint_requires_validation_before_invocation python.test_blk_pipe_adapter.BlkPipeAdapterTest.test_execute_sprint_preserves_non_empty_trusted_local_validation_commands -v
OK
```

## Authority Boundary

BLK-SYSTEM-107 is local BLK-pipe validation hardening only. It grants no BLK-pipe runtime dispatch against target repositories, no BLK-test runtime, no BEO publication, no RTM generation or drift rejection, no protected-body reads, no production `blk-link`, no signer/storage/ledger/rollback authority, and no source/Git mutation outside the BLK-System sprint commit.

## Residual Work

- HR-006 remains open: validation profiles and legacy validation commands still use the existing shell-command validation runner.
- Future less-trusted/autonomous execution work must prefer repository-owned `validation_profiles` and add separate profile/command-model hardening before authority expansion.
