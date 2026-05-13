# BLK-110 — Exit-Code Taxonomy Split

**Status:** Active L1 local taxonomy hardening boundary — not sprint/runtime authority
**Purpose:** Record BLK-SYSTEM-110 remediation of HR-009 by separating invalid-payload routing from syntax/validation failure routing.
**Scope:** Go `blk-pipe` exit codes, Python adapter status routing, and operator-facing routing doctrine only.

## Required Markers

```text
BLK_SYSTEM_110_EXIT_CODE_TAXONOMY_SPLIT
INVALID_PAYLOAD_EXIT_CODE_8
SYNTAX_VALIDATION_FAILURE_REMAINS_EXIT_CODE_2
PROTECTED_ALLOWLIST_VIOLATIONS_REMAIN_EXIT_CODE_3
```

Persistent doctrine gate marker: BLK-SYSTEM-110 pins invalid payload to Exit 8, validation/syntax failure to Exit 2, and protected allowlist/unauthorized mutation to Exit 3.

## Authority Boundary

BLK-110 does not authorize target-repo BLK-pipe dispatch, BLK-test runtime execution, BEO publication, RTM generation, RTM drift rejection, protected BLK-req body reads, active-vault hash comparison, production `blk-link`, signer/storage/ledger/rollback behavior, package/network/model/browser/cyber tooling, production isolation claims, or source/Git mutation outside exact BLK-System sprint files.

## Remediation Summary

- `ExitInvalidPayload` is now POSIX Exit 8.
- `ExitValidationFailed` remains POSIX Exit 2 and maps to `SYNTAX_GATE_FAILED`.
- `ExitUnauthorizedMutation` remains POSIX Exit 3 for protected allowlist violations and unauthorized mutation.
- Python adapter routing now defaults Exit 8 to `INVALID_PAYLOAD`, defaults Exit 2 to `SYNTAX_GATE_FAILED`, and rejects cross-taxonomy status laundering.
- BLK-003, BLK-004, and BLK-031 operator/doctrine wording now distinguish invalid payload from syntax/validation failure.

## Finding Disposition

- HR-009: CLOSED. Invalid payload and validation failure no longer share POSIX Exit 2.
