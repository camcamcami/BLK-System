# BLK-SYSTEM-134 — Production blk-link / RTM Trace-Closure Approval Capture Plan

**Status:** Planned for immediate execution
**Date:** 2026-05-15T14:28:54+10:00
**Documentation model:** Lean — plan because user explicitly requested plan first; one closeout only.

## 1. Objective

Capture an exact approval decision for the BLK-SYSTEM-133 production `blk-link` / RTM trace-closure authority request.

The sprint may produce a deterministic approval-capture fixture for:

- `PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-133-001`
- expected request package hash `sha256:8fa1f60ed592b4fda4b1b3cd2e2132a19fd74a24f80b559e8c1b57aa5221e271`

The sprint must not execute production `blk-link`, generate RTM, reject drift, compare active-vault hashes, create coverage truth, read protected bodies, mutate target/source/Git state outside this repo change, run BLK-pipe/BLK-test/Codex/tooling, or claim production isolation.

## 2. Tasks

1. Add RED tests for a BLK-SYSTEM-134 approval-capture package.
2. Implement a strict, deterministic approval-capture fixture.
3. Bind the decision to exact BLK-SYSTEM-133 request identity and canonical hash.
4. Reserve one future production trace-closure run ID without consuming it.
5. Update executable current-state, BLK-077, BLK-079, active doctrine gates, and lean-doc gates.
6. Run hostile audit, focused verification, full suite, and `git diff --check`.
7. Write exactly one sprint closeout and commit/push exact paths.

## 3. Expected Output

- `PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-134-001`
- `APPROVAL-BLK-SYSTEM-133-PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-001`
- `RUN-BLK-SYSTEM-135-PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-001` reserved but not consumed
- next frontier: production `blk-link` / RTM trace-closure execution planning only

## 4. Authority Boundary

This sprint can capture approval for one future production trace-closure execution sprint only. It cannot execute that future run.

Still unauthorized:

- production/reusable `blk-link` execution now;
- RTM generation;
- RTM drift rejection or authoritative drift decision;
- active-vault hash comparison;
- coverage truth / coverage matrix generation;
- protected BLK-req or use-case body reads/copying/parsing/hashing/scanning/mutation;
- signer key access, signing, immutable storage, ledger append, rollback, revocation, or supersession;
- BEB dispatch or BEO closeout execution;
- BLK-pipe, BLK-test, Codex, package-manager, network, model-service, browser, cyber tooling, target/source/Git mutation, or production-isolation claims.

## 5. Verification Plan

- RED: `python.test_production_blk_link_rtm_trace_closure_approval_capture` fails before implementation.
- GREEN: focused BLK-SYSTEM-134 fixture tests pass.
- Focused current-state/doctrine/lean-doc verification passes after docs closeout exists.
- Hostile audit checks exact hash binding, no side effects, no stale request-frontier active marker, no live imports/calls, and laundering probes.
- Full `python -m unittest discover python 'test_*.py'` passes.
