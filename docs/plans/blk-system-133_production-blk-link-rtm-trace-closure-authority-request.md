# BLK-SYSTEM-133 — Production blk-link / RTM Trace-Closure Authority Request Plan

**Status:** Planned for immediate execution
**Date:** 2026-05-15T13:05:32+10:00
**Documentation model:** Lean — plan created because the user explicitly asked to plan first; one sprint closeout at finish; no new BLK-### document.

## 1. Objective

Implement a deterministic request-only authority package for production `blk-link` / RTM trace closure, bound to the exact BLK-SYSTEM-132 local/non-authoritative trace-closure execution record.

The sprint creates review evidence only. It does not capture approval, execute production `blk-link`, generate RTM, reject drift, compare active-vault hashes, establish coverage truth, read protected bodies, mutate source/target/Git state, run BLK-pipe/BLK-test/Codex/tooling, or claim production isolation.

## 2. Scope

Create `PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-133-001` as a hash-bound request package that:

- recomputes and requires upstream execution package `RTM-TRACE-CLOSURE-EXECUTION-132-001` at hash `sha256:548934403cd71a4eebc27c4e164a43f9e2d7f71b8cfab7765b1f51e65f44fed5`;
- requires upstream trace record `RTM-TRACE-CLOSURE-RECORD-132-001` at hash `sha256:2b78924d8d839dff65c2137cabf09362a23feec24fa21010238ef8c48703c3ca`;
- emits a review-ready request for future exact production `blk-link` / RTM trace-closure approval capture, not approval or execution;
- binds `authority_request_hash`, `requested_at`, `expires_at`, `expired`, `replayed`, `stale`, exact proof obligations, exact denied authorities, and false side-effect flags into the final package hash;
- updates BLK-077, BLK-079, executable current-state index, and doctrine gates to make the next frontier production `blk-link` / RTM trace-closure approval capture planning only.

## 3. Non-Scope / Authority Boundary

This sprint does not authorize or perform:

- approval capture;
- production or reusable `blk-link` execution;
- RTM generation;
- RTM drift rejection or authoritative drift decision;
- active-vault hash comparison or coverage truth;
- protected BLK-req / use-case body reads, copying, parsing, hashing, scanning, or mutation;
- signer key material, cryptographic signing, immutable storage, public ledger append, rollback, revocation, or supersession;
- BEB dispatch or BEO closeout execution;
- target/source/Git mutation;
- BLK-pipe, BLK-test, Codex, package-manager, network, model-service, browser, cyber, or production-isolation behavior.

## 4. Tasks

1. Add RED tests for exact BLK-132 execution package binding, request-only package shape, request-window hash binding, denied-authority/proof-obligation exact sets, hostile string/protected-path probes, timestamp windows, and no live tooling imports.
2. Implement the smallest deterministic fixture that passes those tests.
3. Update current-state/roadmap gates for BLK-SYSTEM-133 and the next frontier.
4. Run focused tests, hostile audit, full Python suite, diff checks, and repo bytecode scan.
5. Write exactly one sprint closeout in `docs/outcomes/BLK-SYSTEM-133_sprint-closeout.md`, commit exact paths, push.

## 5. Stop Conditions

Stop and do not continue if implementation requires approval capture, production `blk-link` execution, RTM generation, protected-body access, signer/storage/ledger behavior, runtime/tooling, production authority, or more than one outcome document.
