# BLK-SYSTEM-147 — Hardening-Only Regression Sweep Plan

**Status:** Planned for immediate execution
**Date:** 2026-05-15T21:26:39+10:00

## Goal

Prove the BLK-SYSTEM-146 lean current-state/index model is stable across repo tests and authority gates, without reopening any production authority rung.

## Scope

- Add regression gates that keep BLK-077 and BLK-079 lean.
- Add a source-level gate that finds unguarded active-doc historical marker requirements before they force ledger bloat back into BLK-077/079.
- Add stricter current-state authority-smuggling probes for compact/camel/percent-encoded positive authority wording.
- Extend lean one-closeout policy to BLK-SYSTEM-147.
- Produce exactly one closeout: `docs/outcomes/BLK-SYSTEM-147_sprint-closeout.md`.

## Non-Scope / Authority Boundary

BLK-SYSTEM-147 is hardening-only. It grants no BEO publication, BEB dispatch, RTM generation, drift rejection, protected body reads, production `blk-link`, BLK-pipe/BLK-test/Codex runtime, target/source/Git mutation beyond this repo patch, signer/storage/ledger/rollback, package/network/model/browser/cyber tooling, or production-isolation authority.

## Validation

1. Write RED tests for the missing guard/probe.
2. Patch implementation/tests minimally.
3. Run focused tests.
4. Run hostile audit for lean-doc and authority regression.
5. Run full Python suite and Go checks.
6. Commit exact changed paths and push `main`.

## Documentation Burden Rule

No `docs/BLK-147_*.md`. No per-task outcome docs. BLK-001 through BLK-006 remain untouched.
