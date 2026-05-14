# BLK-SYSTEM-112 Hostile Review — Structured Validation Profile argv Hardening

**Status:** PASS
**Date:** 2026-05-14
**Reviewed scope:** `internal/validationprofiles`, `internal/validation`, `internal/contracts`, `internal/pipe`, `python/blk_pipe_adapter.py`, `docs/BLK-004_blk-pipe-v47-architecture-suite.md`, `docs/BLK-112_structured-validation-profile-argv-hardening.md`

## Required Markers

```text
BLK_SYSTEM_112_STRUCTURED_VALIDATION_PROFILE_ARGV_HARDENING
VALIDATION_PROFILES_RESOLVE_TO_STRUCTURED_ARGV_ENV_SPECS
REPOSITORY_OWNED_PROFILES_DO_NOT_EXECUTE_THROUGH_SH_C
RESOLVED_VALIDATION_ARGV_REPORTED_FOR_HOSTILE_AUDIT
LEGACY_VALIDATION_COMMANDS_REMAIN_TRUSTED_LOCAL_COMPATIBILITY_ONLY
```

## Finding Disposition

- **HR-006 profile shell path:** CLOSED. Repository-owned profiles resolve to structured argv/env specs and execute through `validation.RunSpecs()` without `sh -c`.
- **HR-006 legacy `validation_commands`:** NOT CLOSED by this sprint. The shell runner remains for trusted-local compatibility and must stay visibly separate from structured profile execution.

## Hostile Checks

| Probe | Result |
| --- | --- |
| Repository profile still resolves to `sh -c` | BLOCKED by `TestResolveSpecsReturnsStructuredArgvWithoutShell`. |
| Returned profile specs can mutate registry | BLOCKED by `TestResolveSpecEvidenceReturnsDefensiveCopies`. |
| Structured validation expands `$HOME`, `&&`, or `touch` through a shell | BLOCKED by `TestRunSpecsDoesNotUseShellExpansionOrMetacharacters`. |
| `blk-pipe` profile path silently falls back to legacy shell strings | BLOCKED by report evidence asserting `resolved_validation_argv`. |
| Legacy trusted-local compatibility accidentally removed | NOT BROKEN; `validation.Run()` remains the shell-string path and existing legacy command tests remain in place. |
| Authority laundering into runtime/publication/RTM/protected-read authority | NOT PRESENT; BLK-004 and BLK-112 preserve explicit denials. |

## Review Result

PASS for BLK-SYSTEM-112 scope. Repository-owned validation profiles now execute as structured argv/env specs, not shell command strings. Residual trusted-local shell command compatibility is explicitly not production/autonomous authority and is carried forward to BLK-SYSTEM-113.
