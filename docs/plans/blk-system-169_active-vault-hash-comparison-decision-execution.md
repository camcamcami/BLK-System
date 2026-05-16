# BLK-SYSTEM-169 — Active-Vault Hash Comparison Decision Execution Plan

**Status:** Planned for execution in this batch
**Scope:** Exact approval capture + one-run metadata/hash comparison record

## Goal
Consume the exact BLK-SYSTEM-168 request using the operator directive, record exact approval, consume one run ID, and emit record-only metadata/hash comparison evidence.

## Files
- `python/active_vault_hash_comparison_ladder_168_171.py`
- `python/test_active_vault_hash_comparison_ladder_168_171.py`
- `docs/outcomes/BLK-SYSTEM-169_sprint-closeout.md`

## Authority Boundary
Only the exact caller-supplied metadata/hash comparison record is produced. No active-vault filesystem reads/scans, protected-body access, RTM generation, drift rejection, coverage truth, reusable production `blk-link`, tooling/runtime, signer/storage/ledger reuse, target/source/Git mutation, or production-isolation claim.

## Verification
Focused unittest for the 168..171 ladder, hash-binding/defensive-copy tests, current-state/lean-doc gates, hostile review, full Python discovery, Go tests, and `git diff --check`.
