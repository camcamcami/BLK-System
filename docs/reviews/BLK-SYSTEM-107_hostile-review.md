# BLK-SYSTEM-107 Hostile Review — Mandatory Validation Required

**Status:** PASS
**Date:** 2026-05-14
**Reviewed scope:** `internal/contracts/payload.go`, `internal/contracts/payload_test.go`, `internal/pipe/run_test.go`, `python/blk_pipe_adapter.py`, `python/test_blk_pipe_adapter.py`, `docs/BLK-004_blk-pipe-v47-architecture-suite.md`, `docs/BLK-107_mandatory-validation-required.md`

## Required Markers

```text
BLK_SYSTEM_107_MANDATORY_VALIDATION_REQUIRED
EXECUTE_PAYLOAD_REQUIRES_VALIDATION_PROFILE_OR_COMMAND
VALIDATION_REQUIRED_BEFORE_ENGINE_SIDE_EFFECTS
PYTHON_ADAPTER_VALIDATION_REQUIRED_FAIL_FAST_ONLY_GO_REMAINS_AUTHORITY
```

## Finding Disposition

- **HR-003:** CLOSED for the no-validation execute bypass. Execute payloads now require non-empty `validation_profiles` or non-empty `validation_commands` before engine side effects.
- **HR-006:** NOT CLOSED by this sprint. Shell/profile model hardening remains a future validation-profile tightening sprint.

## Hostile Checks

| Probe | Result |
| --- | --- |
| Missing validation source reaches engine | BLOCKED by Go `Payload.Validate()` and `Run()` before engine side effects. |
| Explicit `validation_commands: []` reaches engine | BLOCKED as `INVALID_PAYLOAD`; sentinel file remains absent in regression test. |
| Explicit `validation_profiles: []` reaches engine | BLOCKED as `INVALID_PAYLOAD`; sentinel file remains absent in regression test. |
| Python adapter silently defaults missing validation to `[]` and invokes `blk-pipe` | BLOCKED; adapter raises before the fake capture directory is created. |
| Non-empty trusted-local `validation_commands` compatibility accidentally broken | NOT BROKEN; focused Python regression preserves non-empty commands. |
| Non-empty repository-owned `validation_profiles` compatibility accidentally broken | NOT BROKEN; existing adapter/profile tests pass. |
| Revert path accidentally forced through execute validation | NOT BROKEN; revert remains outside execute validation requirement. |
| Authority laundering from validation hardening into runtime/publication/RTM/protected-read authority | NOT PRESENT in changed code or docs; docs preserve explicit denials. |

## Boundary Review

- Go remains the enforcement authority. Python adapter validation is fail-fast convenience only.
- Validation requirement does not authorize broader file allowlists, target repo execution, BLK-test runtime, BEO publication, RTM generation/drift rejection, protected-body reads, signer/storage/ledger behavior, or production `blk-link`.
- Legacy `validation_commands` compatibility is deliberately retained for trusted-local use and remains visibly separate from repository-owned `validation_profiles`.
- BLK-004 overlay now states the execute validation requirement while preserving the less-trusted/autonomous profile-only boundary.

## Review Result

PASS for BLK-SYSTEM-107 scope. The no-validation execute bypass is closed with RED/GREEN Go and Python regressions. Residual profile-command shell tightening remains separate follow-up work and must not be treated as authorized by this closeout.
