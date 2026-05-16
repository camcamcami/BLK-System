# BLK-SYSTEM-174 — Protected-Body Verification Decision Request Plan

**Status:** Planned because BLK-SYSTEM-173 reconciled clean
**Scope:** Request-only next authority package after clean BLK-SYSTEM-173 reconciliation

## Goal
Emit a request-only package for future exact protected-body verification decision approval. This is needed after the clean metadata-only decision reconciliation because metadata evidence cannot establish protected-body verification or coverage truth.

## Files
- `python/metadata_bound_drift_coverage_decision_ladder_172_174.py`
- `python/test_metadata_bound_drift_coverage_decision_ladder_172_174.py`
- `docs/outcomes/BLK-SYSTEM-174_sprint-closeout.md`

## Authority Boundary
Request-only. No approval capture, run-ID reservation/consumption, protected-body reads/copying/parsing/hashing/scanning, drift rejection, coverage truth, RTM generation, reusable production `blk-link`, tooling/runtime, signer/storage/ledger reuse, target/source/Git mutation, or production-isolation claim.

## Verification
Focused request-only unittest, current-state/lean-doc gates, hostile review, full Python discovery, Go tests, and `git diff --check`.
