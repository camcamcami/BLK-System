# BLK-SYSTEM-131 — Metadata-Bound RTM Trace-Closure Approval Capture Plan

**Status:** Planned for immediate execution
**Date:** 2026-05-15T12:03:39+10:00
**Documentation model:** Lean — one plan because the user explicitly asked to plan first; one sprint closeout at finish; no new BLK-### document.

## 1. Objective

Implement a deterministic approval-capture fixture for the exact BLK-SYSTEM-130 RTM trace-closure authority request.

The sprint captures a human/operator decision for `RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-001` only. It reserves a future local, non-authoritative trace-closure run ID but does not execute trace closure.

## 2. Scope

Create `RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-131-001` as a hash-bound approval capture package that:

- recomputes and requires the exact BLK-130 request package hash `sha256:cf59f9360d79226ff89e9743ea49b7824b0852908422c6de005ca7f9580a68b2`;
- binds the exact upstream BLK-129 publication execution ID and hash carried by BLK-130;
- captures approval for one future local/non-authoritative RTM trace-closure execution run ID;
- preserves `future_run_id_consumed=False`;
- preserves false side-effect flags for production `blk-link`, RTM generation, drift rejection, active-vault hash comparison, coverage truth, protected-body reads/copying/hashing/scanning, signer/storage/ledger/rollback, target/source/Git mutation, BLK-pipe/BLK-test/Codex runtime, tooling, and production-isolation claims.

## 3. Non-Scope / Authority Boundary

This sprint does not authorize or perform:

- local/non-authoritative trace-closure execution;
- production or reusable `blk-link` execution;
- RTM generation;
- RTM drift rejection or authoritative drift decision;
- active-vault hash comparison or coverage truth;
- protected BLK-req / use-case body reads, copying, parsing, hashing, scanning, or mutation;
- signer key material, cryptographic signing, immutable storage, public ledger append, rollback, revocation, or supersession;
- BEB dispatch or BEO closeout execution;
- target/source/Git mutation outside the BLK-System sprint commit;
- BLK-pipe, BLK-test, Codex, package-manager, network, model-service, browser, cyber, or production-isolation behavior.

## 4. Tasks

1. Add RED tests for exact BLK-130 request binding, approval capture package shape, future run reservation, denied-authority exact sets, hostile string/protected-path probes, timestamp windows, and no live tooling imports.
2. Implement the smallest fixture that passes those tests.
3. Update BLK-077, BLK-079, executable current-state index, and doctrine gates to show BLK-SYSTEM-131 approval capture complete and next frontier local/non-authoritative execution record only.
4. Run focused tests, hostile audit, full Python suite, and diff checks.
5. Write exactly one sprint closeout in `docs/outcomes/BLK-SYSTEM-131_sprint-closeout.md`, commit exact paths, push.

## 5. Stop Conditions

Stop and do not continue if implementation requires actual RTM/blk-link execution, protected-body access, runtime/tooling, production authority, signer/storage/ledger behavior, or more than one outcome document.
