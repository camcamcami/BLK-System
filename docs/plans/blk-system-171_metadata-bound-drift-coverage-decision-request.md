# BLK-SYSTEM-171 — Metadata-Bound Drift/Coverage Decision Request Plan

**Status:** Planned for execution in this batch
**Scope:** Request-only next authority package after clean BLK-SYSTEM-170 reconciliation

## Goal
Emit a request-only package for future exact metadata-bound drift/coverage decision approval after BLK-SYSTEM-170 clean reconciliation.

## Files
- `python/active_vault_hash_comparison_ladder_168_171.py`
- `python/test_active_vault_hash_comparison_ladder_168_171.py`
- `docs/outcomes/BLK-SYSTEM-171_sprint-closeout.md`

## Authority Boundary
No approval capture, run-ID reservation/consumption, drift decision, drift rejection, coverage truth, RTM generation, protected-body reads/copying/parsing/hashing/scanning, active-vault filesystem read/scan, reusable production `blk-link`, tooling/runtime, signer/storage/ledger reuse, target/source/Git mutation, or production-isolation claim.

## Verification
Focused unittest for BLK-SYSTEM-171 request-only behavior, current-state/lean-doc gates, hostile review, full Python discovery, Go tests, and `git diff --check`.
