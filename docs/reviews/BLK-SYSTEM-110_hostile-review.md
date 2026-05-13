# BLK-SYSTEM-110 Hostile Review — Exit-Code Taxonomy Split

**Status:** PASS
**Date:** 2026-05-14
**Reviewed scope:** `internal/pipe/exitcodes.go`, `internal/pipe/exitcodes_test.go`, `internal/pipe/run_test.go`, `python/blk_pipe_adapter.py`, `python/test_blk_pipe_adapter.py`, BLK-003/004/031 routing docs, and `docs/BLK-110_exit-code-taxonomy-split.md`.

## Required Markers

```text
BLK_SYSTEM_110_EXIT_CODE_TAXONOMY_SPLIT
INVALID_PAYLOAD_EXIT_CODE_8
SYNTAX_VALIDATION_FAILURE_REMAINS_EXIT_CODE_2
PROTECTED_ALLOWLIST_VIOLATIONS_REMAIN_EXIT_CODE_3
```

## Finding Disposition

- **HR-009:** CLOSED. `INVALID_PAYLOAD` now has its own Exit 8 route; validation/syntax failure remains Exit 2.

## Hostile Checks

| Probe | Result |
| --- | --- |
| `ExitInvalidPayload == ExitValidationFailed` | BLOCKED by Go regression; values are 8 and 2. |
| Invalid payload with report status `INVALID_PAYLOAD` | Routes as Exit 8. |
| Validation failure with report status `SYNTAX_GATE_FAILED` | Routes as Exit 2. |
| Exit 2 report attempts `INVALID_PAYLOAD` | Python adapter overrides to `SYNTAX_GATE_FAILED`. |
| Exit 8 report attempts `SYNTAX_GATE_FAILED` | Python adapter overrides to `INVALID_PAYLOAD`. |
| Protected allowlist violations accidentally moved off Exit 3 | NOT PRESENT; protected and unauthorized mutation routing remains Exit 3. |
| Authority laundering from taxonomy hardening into runtime/publication/RTM authority | NOT PRESENT; docs preserve explicit denials. |

## Review Result

PASS for BLK-SYSTEM-110 scope. HR-009 is closed without granting new runtime authority.
