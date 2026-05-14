# BLK-SYSTEM-112 Sprint Closeout — Structured Validation Profile argv Hardening

**Status:** COMPLETE
**Date:** 2026-05-14
**Sprint:** BLK-SYSTEM-112
**Plan:** `docs/plans/blk-system-112_structured-validation-profile-argv-hardening.md`
**Record:** `docs/BLK-112_structured-validation-profile-argv-hardening.md`
**Hostile review:** `docs/reviews/BLK-SYSTEM-112_hostile-review.md`

## Summary

BLK-SYSTEM-112 closes the repository-owned profile half of HR-006. Validation profiles now resolve to structured argv/env specs and `blk-pipe` executes those specs without shell interpretation. Reports include exact `resolved_validation_argv` evidence while preserving human-readable `resolved_validation_commands`.

## Required Markers

```text
BLK_SYSTEM_112_STRUCTURED_VALIDATION_PROFILE_ARGV_HARDENING
VALIDATION_PROFILES_RESOLVE_TO_STRUCTURED_ARGV_ENV_SPECS
REPOSITORY_OWNED_PROFILES_DO_NOT_EXECUTE_THROUGH_SH_C
RESOLVED_VALIDATION_ARGV_REPORTED_FOR_HOSTILE_AUDIT
LEGACY_VALIDATION_COMMANDS_REMAIN_TRUSTED_LOCAL_COMPATIBILITY_ONLY
```

## RED/GREEN Evidence

RED failures observed before implementation:

```text
go test ./internal/validationprofiles ./internal/validation -run 'TestResolveSpecsReturnsStructuredArgvWithoutShell|TestResolveSpecEvidenceReturnsDefensiveCopies|TestRunSpecsDoesNotUseShellExpansionOrMetacharacters' -count=1 -v
FAIL: undefined ResolveSpecs / validationprofiles.CommandSpec / RunSpecs
```

Focused GREEN checks after implementation:

```text
go test ./internal/validationprofiles ./internal/validation ./internal/contracts ./internal/pipe -run 'TestResolveSpecsReturnsStructuredArgvWithoutShell|TestResolveSpecEvidenceReturnsDefensiveCopies|TestRunSpecsDoesNotUseShellExpansionOrMetacharacters|TestRunValidationProfileExecutesResolvedCommandsAndReportsEvidence|TestRunValidationProfileFailureRoutesToSyntaxGateAndCleans|TestDecodePayloadAcceptsValidationProfiles|TestReportMarshalIncludesValidationProfileEvidence' -count=1 -v
PASS
```

## Authority Boundary

BLK-SYSTEM-112 is local BLK-pipe validation-profile hardening only. It grants no BLK-pipe runtime dispatch against target repositories, no BLK-test runtime, no BEO publication, no RTM generation or drift rejection, no protected-body reads, no production `blk-link`, no signer/storage/ledger/rollback authority, no package/network/model/browser/cyber tooling, and no source/Git mutation outside the BLK-System sprint commit.

## Residual Work

BLK-SYSTEM-113 must harden the validation trust boundary and capability policy. Legacy `validation_commands` remain shell-based trusted-local compatibility and must not be accepted as autonomous/less-trusted validation authority.
