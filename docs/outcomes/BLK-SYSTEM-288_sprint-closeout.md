# BLK-SYSTEM-288 — Speculative Quarantine Evidence Sprint Closeout

**Status:** Complete
**Date:** 2026-05-20
**Commit:** this commit (`feat: add speculative quarantine HITL gate package`)

## 1. Objective

Represent pre-approval compute as disposable quarantine evidence while proving durable target/source/Git state remains unchanged before promotion.

## 2. Files Changed

- `python/blk_speculative_quarantine_approval_286_289.py`
- `python/test_blk_speculative_quarantine_approval_286_289.py`
- `docs/BLK-123_speculative-quarantine-approval-contract.md`
- Active roadmap/current-state gates updated in BLK-077, BLK-079, and current-state tests.

## 3. Implementation Summary

BLK-SYSTEM-288 added `build_speculative_quarantine_evidence_288(...)` and `validate_speculative_quarantine_evidence_288(...)`. Quarantine evidence binds request/interaction hashes, exact run ID, timing mode, target hash before quarantine, manifest/result/report hashes, quarantine workspace ID, time window, default-false external side-effect flags, and false target mutation flags.

## 4. Verification

Focused verification completed:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_speculative_quarantine_approval_286_289 -v
Ran 13 tests in 0.250s
OK
```

Full verification completed with `TMPDIR=/var/tmp/blk-system-tests`: `Ran 1485 tests in 19.029s — OK (skipped=35)`. Whitespace verification is recorded in the commit verification output.

## 5. Hostile Review / Risk Check

- Quarantine workspace identity must be an exact `QUARANTINE-` ID, not a source path.
- External side effects are fail-closed by default (`codex_model_api_called`, `network_called`, and `package_manager_called` remain false).
- Pre-approval compute is represented as hash-bound local evidence only, with `promotion_performed=false` and `target_repo_mutated=false`.

## 6. Authority Boundary

This sprint does not run BLK-pipe or Codex. It does not create real quarantine workspaces, mutate target/source/Git state, call networks/model APIs/package managers, read protected bodies, publish BEOs, generate RTM, or operate `blk-link`.

## 7. Documentation Burden Check

No new BLK doc was created for this sprint. BLK-123 carries the durable contract; this sprint has exactly one outcome closeout and no per-task outcome docs.
