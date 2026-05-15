# BLK-SYSTEM-148 — Lean Current-State Drift Removal Plan

## Goal

Remove recurring sprint-specific closeout pointers from BLK-079 so the current-state authority index does not require a maintenance edit after every sprint.

## Scope

- Add a regression gate proving BLK-079 does not contain sprint-specific closeout pointers.
- Replace specific closeout links in BLK-079 with a stable pointer to `docs/outcomes/` for historical evidence.
- Preserve hardening-only/no-rung-selected authority state.

## Authority Boundary

This sprint grants no BEB dispatch, BEO closeout/publication execution, RTM generation, drift rejection, production `blk-link`, protected-body access, signer/storage/ledger behavior, BLK-pipe/BLK-test/Codex runtime, target/source/Git mutation outside this repo patch, broad tooling, or production-isolation claim.

## Verification

- Focused lean/current-state tests.
- `git diff --check` on touched files.
- One closeout only: `docs/outcomes/BLK-SYSTEM-148_sprint-closeout.md`.
- No new `docs/BLK-148_*.md`.
