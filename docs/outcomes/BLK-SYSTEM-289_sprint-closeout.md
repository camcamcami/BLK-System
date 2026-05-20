# BLK-SYSTEM-289 — Promotion/Purge/Stale Gate Sprint Closeout

**Status:** Complete
**Date:** 2026-05-20
**Commit:** this commit (`feat: add speculative quarantine HITL gate package`)

## 1. Objective

Implement the local gate evidence that either opens promotion for one exact quarantined result hash after target-hash recheck, purges rejected/expired/dry-run-only results, or blocks stale target hashes.

## 2. Files Changed

- `python/blk_speculative_quarantine_approval_286_289.py`
- `python/test_blk_speculative_quarantine_approval_286_289.py`
- `docs/BLK-123_speculative-quarantine-approval-contract.md`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_lean_documentation_policy.py`

## 3. Implementation Summary

BLK-SYSTEM-289 added `build_promotion_or_purge_gate_289(...)` and `validate_promotion_or_purge_gate_289(...)`. The gate requires the selected result hash to match quarantine evidence, target hash at decision to match the pre-quarantine target hash, a live decision window, the original HITL interaction package for revalidation, and typed policy evidence for `CONFIG_POLICY_BYPASS`. `APPROVE_DRY_RUN_ONLY` is handled as `DRY_RUN_ONLY_PURGED`, not durable promotion.

## 4. Verification

Focused verification completed:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_speculative_quarantine_approval_286_289 -v
Ran 13 tests in 0.250s
OK
```

Full verification completed with `TMPDIR=/var/tmp/blk-system-tests`: `Ran 1485 tests in 19.029s — OK (skipped=35)`. Whitespace verification is recorded in the commit verification output.

## 5. Hostile Review / Risk Check

- Exact result hash mismatch raises before any promotion evidence can be produced.
- Target hash drift produces `STALE_TARGET_HASH_BLOCKED` and purge evidence.
- Rejection, expiry, and dry-run-only decisions do not open promotion and require purge evidence.
- The gate evidence records `durable_target_mutation_performed=false`; it is a local proof object, not a live mutator.

## 6. Authority Boundary

This sprint creates promotion/purge gate evidence only. It does not apply patches, write to target repos, consume real run IDs outside local evidence, start runtimes/transports, publish BEOs, generate RTM, operate production `blk-link`, use BLK-test MCP, read protected bodies, or claim production isolation.

## 7. Documentation Burden Check

No new BLK doc was created for this sprint. The durable contract remains BLK-123; this sprint has exactly one outcome closeout and no per-task outcome docs.
