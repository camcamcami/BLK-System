# BLK-SYSTEM-163 — Current-State Denied Surface Hardening Plan

**Status:** Execution plan
**Date:** 2026-05-16T10:33:45+10:00

## Objective

Harden the executable current-state authority index so the post-BLK-162 hardening-only frontier explicitly denies every adjacent authority named by BLK-077/BLK-079, not only the older representative subset.

## Scope

- Expand executable denied flags for source/Git mutation, signer/storage/ledger reuse, rollback/revocation/supersession, BEO closeout execution, protected-body copy/parse/hash/scan, reusable RTM generation, production `blk-link`, drift rejection, coverage truth, and active-vault comparison.
- Add regression tests proving default records include these flags as `False`, positive values fail closed, missing flags fail closed, and the human roadmap/index carry matching denial markers without becoming a sprint ledger.
- Update BLK-077/BLK-079 only where the compact current-state map needs to reflect the hardening result.
- Produce exactly one sprint closeout.

## Non-Scope / Authority Boundary

This sprint does not authorize protected-body reads, RTM generation, production `blk-link`, drift rejection, coverage truth, active-vault comparison, source/Git mutation, BEO closeout execution, BEO publication/signing/storage/ledger reuse, rollback/revocation/supersession, BLK-pipe runtime, BLK-test runtime, live Codex, package/network/model/browser/cyber tooling, or production-isolation claims.

## TDD Plan

1. RED: extend `python/test_blk_current_state_authority_index.py` to require the complete denied flag set and compact documentation markers.
2. GREEN: update `python/blk_current_state_authority_index.py`, BLK-077, and BLK-079 minimally.
3. Verify focused tests, hostile audit, full Python suite, Go checks where applicable, `git diff --check`, one closeout, exact-path commit, push.

## Documentation Burden Check

No new `docs/BLK-###` document. This plan exists because the user explicitly requested planning before execution. The sprint will create one outcome closeout only.
