# BLK-SYSTEM-172 — Metadata-Bound Drift/Coverage Decision Execution Plan

**Status:** Planned for execution in this batch
**Scope:** Exact BLK-SYSTEM-171 approval capture plus one bounded metadata-only decision record

## Goal
Consume the exact BLK-SYSTEM-171 request under the operator's current directive and emit one record-only metadata-bound drift/coverage decision package.

## Files
- `python/metadata_bound_drift_coverage_decision_ladder_172_174.py`
- `python/test_metadata_bound_drift_coverage_decision_ladder_172_174.py`
- `docs/outcomes/BLK-SYSTEM-172_sprint-closeout.md`

## Authority Boundary
Approval is limited to the exact BLK-171 request and one run ID. No protected-body reads/copying/parsing/hashing/scanning, RTM generation, RTM drift rejection, coverage truth, reusable `blk-link`, tooling/runtime, signer/storage/ledger reuse, target/source/Git mutation, or production-isolation claim.

## Verification
Focused unittest for BLK-SYSTEM-172 decision execution, hostile probes for rehashed upstream packages and adjacent-authority flags, current-state/lean-doc gates, full Python discovery, Go tests, and `git diff --check`.
