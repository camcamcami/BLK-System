# BLK-SYSTEM-146 — Lean Current-State / Index Hardening Plan

**Status:** Planned for immediate execution
**Date:** 2026-05-15T21:05:33+10:00

## Goal

Reduce active BLK-System documentation burden after BLK-SYSTEM-145 by turning BLK-079 and the executable current-state index back into concise current-state surfaces instead of sprint-by-sprint ledgers.

## Scope

- Compress `docs/BLK-079_post-078-current-state-authority-index.md` to the current operator-facing authority map only.
- Keep `docs/BLK-077_blk-system-post-078-roadmap.md` Occam-focused and hardening-only.
- Update `python/blk_current_state_authority_index.py` so executable surfaces are current categories, not a historical sprint catalog.
- Update regression gates to enforce line/count/length limits and hardening-only authority boundaries.
- Produce exactly one closeout: `docs/outcomes/BLK-SYSTEM-146_sprint-closeout.md`.

## Non-Scope / Authority Boundary

BLK-SYSTEM-146 grants no BEO publication, BEB dispatch, RTM generation, drift rejection, protected body reads, production `blk-link`, BLK-pipe/BLK-test/Codex runtime, target/source/Git mutation beyond this repository patch, signer/storage/ledger/rollback, package/network/model/browser/cyber tooling, or production-isolation authority.

## Validation

1. Add RED tests that fail on current active-doc/index bloat.
2. Patch implementation/docs minimally to pass.
3. Run focused unittest modules.
4. Run hostile audit for authority creep and lean-doc regressions.
5. Run full Python suite and Go checks.
6. Commit exact changed paths and push `main`.

## Documentation Burden Rule

No new `docs/BLK-146_*.md` document. No per-task outcome docs. BLK-001 through BLK-006 remain untouched.
