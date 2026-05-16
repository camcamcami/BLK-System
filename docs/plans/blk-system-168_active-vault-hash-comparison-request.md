# BLK-SYSTEM-168 — Active-Vault Hash Comparison Request Plan

**Status:** Planned for execution in this batch
**Scope:** Request-only package after clean BLK-SYSTEM-167 reconciliation

## Goal
Emit a metadata/hash-only active-vault comparison authority request bound to BLK-SYSTEM-167 clean reconciliation.

## Files
- `python/active_vault_hash_comparison_ladder_168_171.py`
- `python/test_active_vault_hash_comparison_ladder_168_171.py`
- `docs/outcomes/BLK-SYSTEM-168_sprint-closeout.md`

## Authority Boundary
No approval capture, run-ID reservation/consumption, comparison execution, protected-body reads/copying/parsing/hashing/scanning, RTM generation, drift rejection, coverage truth, reusable production `blk-link`, tooling/runtime, signer/storage/ledger reuse, target/source/Git mutation, or production-isolation claim.

## Verification
Focused unittest for the 168..171 ladder, current-state/lean-doc gates, hostile review, full Python discovery, Go tests, and `git diff --check`.
