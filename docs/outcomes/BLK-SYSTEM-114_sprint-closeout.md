# BLK-SYSTEM-114 Sprint Closeout — BLK-pipe Report/Evidence Hardening

**Status:** COMPLETE
**Date:** 2026-05-14
**Sprint:** BLK-SYSTEM-114
**Plan:** `docs/plans/blk-system-114_blk-pipe-report-evidence-hardening.md`
**Record:** `docs/BLK-114_blk-pipe-report-evidence-hardening.md`
**Hostile review:** `docs/reviews/BLK-SYSTEM-114_hostile-review.md`

## Summary

BLK-SYSTEM-114 hardens local `blk-pipe` reports so operator diagnostics and hostile review can inspect selected caps, exact file allowlists, target identity, validation trust/profile evidence, failure class, denial route, and cleanup status without relying on prose inference.

## Required Markers

```text
BLK_SYSTEM_114_REPORT_EVIDENCE_HARDENING
REPORT_PRESERVES_SELECTED_TIMEOUT_AND_OUTPUT_CAPS
REPORT_PRESERVES_EXACT_FILE_ALLOWLIST_EVIDENCE
REPORT_PRESERVES_VALIDATION_TRUST_AND_PROFILE_EVIDENCE
REPORT_EXPOSES_FAILURE_CLASS_DENIAL_ROUTE_AND_CLEANUP_STATUS
REPORT_EVIDENCE_IS_DIAGNOSTIC_NOT_AUTHORITY
```

## RED/GREEN Evidence

RED failures observed before implementation:

```text
go test ./internal/contracts ./internal/pipe -run 'TestReportMarshalIncludesExecutionBoundaryEvidence|TestRunV47SuccessNormalizesPayloadAndReportsStableFields|TestRunRejectsExecuteWithoutValidationBeforeEngine' -count=1 -v
FAIL: Report lacked TimeoutSeconds, MaxOutputBytes, AllowedModifiedFiles, AllowedNewFiles, FailureClass, DenialRoute, and CleanupStatus fields; invalid-payload report route fields were absent.
```

Focused GREEN checks after implementation:

```text
go test ./internal/contracts ./internal/pipe -run 'TestReportMarshalIncludesExecutionBoundaryEvidence|TestRunV47SuccessNormalizesPayloadAndReportsStableFields|TestRunRejectsExecuteWithoutValidationBeforeEngine|TestRunValidationProfileExecutesResolvedCommandsAndReportsEvidence' -count=1
ok  	github.com/camcamcami/BLK-System/internal/contracts	0.003s
ok  	github.com/camcamcami/BLK-System/internal/pipe	0.207s
```

```text
rm -rf /tmp/blk-system-pycache && PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_pipe_adapter.BlkPipeAdapterTest.test_execution_result_dataclass_defaults python.test_blk_pipe_adapter.BlkPipeAdapterTest.test_execution_result_preserves_non_success_report_evidence -v
Ran 2 tests in 0.002s
OK
```

## Files Changed

- `internal/contracts/report.go`
- `internal/contracts/report_test.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- `python/blk_pipe_adapter.py`
- `python/test_blk_pipe_adapter.py`
- `docs/BLK-004_blk-pipe-v47-architecture-suite.md`
- `docs/BLK-114_blk-pipe-report-evidence-hardening.md`
- `docs/reviews/BLK-SYSTEM-114_hostile-review.md`

## Authority Boundary

BLK-SYSTEM-114 is local report/evidence hardening only. It grants no BLK-pipe runtime dispatch against target repositories, no BLK-test runtime, no BEO publication, no RTM generation or drift rejection, no protected-body reads, no production `blk-link`, no signer/storage/ledger/rollback authority, no package/network/model/browser/cyber tooling, and no source/Git mutation outside this BLK-System sprint commit.

## Next Work

BLK-SYSTEM-115 should reconcile the production-hardening bridge, pin 112-114 completion in doctrine/current-state surfaces, add persistent doctrine gates for the bridge markers, and set the next frontier to BLK-req legislative gateway planning without granting runtime authority.
