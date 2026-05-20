# BLK-SYSTEM-287 — HITL Interaction Identity/Relay Evidence Sprint Closeout

**Status:** Complete
**Date:** 2026-05-20
**Commit:** this commit (`feat: add speculative quarantine HITL gate package`)

## 1. Objective

Bind Discord button/selector HITL decisions into deterministic `blk-id` actor/approval records and typed `blk-relay` HITL signal evidence without introducing relay transport or message dispatch.

## 2. Files Changed

- `python/blk_speculative_quarantine_approval_286_289.py`
- `python/test_blk_speculative_quarantine_approval_286_289.py`
- `docs/BLK-123_speculative-quarantine-approval-contract.md`
- Active roadmap/current-state gates updated in BLK-077, BLK-079, and current-state tests.

## 3. Implementation Summary

BLK-SYSTEM-287 added `build_hitl_interaction_evidence_287(...)` and `validate_hitl_interaction_evidence_287(...)`. The evidence requires ASCII decimal Discord snowflakes, exact `REQUEST-` and `BLK-HITL-` IDs, an allowed decision vocabulary, timezone-aware decision windows, actor identity hash, approval identity hash, and HITL relay hash.

## 4. Verification

Focused verification completed:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_speculative_quarantine_approval_286_289 -v
Ran 13 tests in 0.250s
OK
```

Full verification completed with `TMPDIR=/var/tmp/blk-system-tests`: `Ran 1485 tests in 19.029s — OK (skipped=35)`. Whitespace verification is recorded in the commit verification output.

## 5. Hostile Review / Risk Check

- Unicode/fullwidth Discord snowflakes are rejected.
- `APPROVED` and other non-contract decision spellings are rejected.
- Component IDs attempting to smuggle transport/runtime wording are rejected by exact-prefix and laundering scans.
- Relay evidence remains a local hash-bound envelope; no Discord API interaction or message dispatch is introduced.

## 6. Authority Boundary

This sprint records HITL interaction evidence only. It grants no approval reuse, no relay network runtime, no BLK-pipe runtime, no live Codex dispatch, no target/source/Git mutation, no BEO/RTM/`blk-link`, and no protected-body access.

## 7. Documentation Burden Check

No new BLK doc was created for this sprint. BLK-123 carries the durable cross-sprint contract; this sprint has exactly one outcome closeout and no per-task outcome docs.
