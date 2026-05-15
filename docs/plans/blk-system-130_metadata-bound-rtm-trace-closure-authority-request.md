# BLK-SYSTEM-130 — Metadata-Bound RTM / blk-link Trace-Closure Authority Request Plan

**Status:** Planned for immediate execution
**Date:** 2026-05-15T11:08:45+10:00
**Documentation model:** Lean — one plan because the user explicitly asked to plan first; one sprint closeout at finish; no new BLK-### document.

## 1. Objective

Implement a deterministic, review-only authority-request fixture that consumes the exact BLK-SYSTEM-129 external BEO publication execution record and packages the next RTM / `blk-link` trace-closure step for human review.

## 2. Scope

Create `RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-001` as a hash-bound request package that:

- binds to `BEO-PUBLICATION-EXECUTION-129-001` and its canonical package hash;
- binds to the BLK-129 publication record hash, metadata-bound BEO/BEB IDs, and exact trace metadata identities;
- selects the next rung as one future local/non-authoritative RTM trace-closure approval decision, not execution;
- preserves false side-effect flags for RTM generation, drift rejection, active-vault hash comparison, coverage truth, protected-body reads/copying/hashing/scanning, signer/storage/ledger/rollback, target/source/Git mutation, BLK-pipe/BLK-test/Codex runtime, tooling, and production-isolation claims.

## 3. Non-Scope / Authority Boundary

This sprint does not authorize or perform:

- runtime RTM generation;
- production or reusable `blk-link` execution;
- RTM drift rejection or authoritative drift decision;
- active-vault hash comparison or coverage truth;
- protected BLK-req / use-case body reads, copying, parsing, hashing, scanning, or mutation;
- signer key material, cryptographic signing, immutable storage, public ledger append, rollback, revocation, or supersession;
- BEB dispatch or BEO closeout execution;
- target/source/Git mutation outside the BLK-System sprint commit;
- BLK-pipe, BLK-test, Codex, package-manager, network, model-service, browser, cyber, or production-isolation behavior.

## 4. Tasks

1. Add RED tests for the BLK-130 request package, exact BLK-129 hash binding, denied-authority exact sets, hostile string/protected-path probes, and no live tooling imports.
2. Implement the smallest fixture that passes those tests.
3. Update BLK-077, BLK-079, executable current-state index, and doctrine gates to show BLK-SYSTEM-130 request complete and next frontier approval capture only.
4. Run focused tests, hostile audit, full Python suite, and diff checks.
5. Write exactly one sprint closeout in `docs/outcomes/BLK-SYSTEM-130_sprint-closeout.md`, commit exact paths, push.

## 5. Stop Conditions

Stop and do not continue if implementation requires actual RTM/blk-link execution, protected-body access, runtime/tooling, production authority, signer/storage/ledger behavior, or more than one outcome document.
