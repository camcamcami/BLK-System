# BLK-SYSTEM-116 — BLK-req Legislative Gateway Contract Plan

**Status:** Planned / executing
**Date:** 2026-05-14
**Track:** Milestone 1 — BLK-req legislative gateway implementation
**Source:** BLK-077 next-frontier marker `NEXT_FRONTIER_BLK_REQ_LEGISLATIVE_GATEWAY_PLANNING_NOT_EXECUTION_AUTHORITY`

## Purpose

Create the executable contract scaffold for the BLK-req legislative gateway before implementing linter, draft writer, promotion, or retrieval mechanics. The contract must make the future 117-121 slices explicit while preserving the post-103 authority cutline.

## Scope

- Add a Python contract surface for the BLK-req legislative gateway.
- Pin allowed local backend operations for BLK-SYSTEM-117 through BLK-SYSTEM-119 only: staging linting, staging draft writing, and canonical hash preview/assignment primitives.
- Reject authority laundering through positive runtime/publication/RTM/protected-active-body wording.
- Add a doctrine record for BLK-116.

## RED Tests First

1. Focused unit tests must fail before implementation because the contract module does not exist.
2. The contract test must require exact denied-authority coverage and false side-effect flags.
3. The doctrine test must fail until `docs/BLK-116_blk-req-legislative-gateway-contract.md` pins the BLK-116 markers.

## Explicit Non-Authority

This sprint does not authorize BLK-pipe runtime dispatch, target/source/Git mutation, BLK-test runtime, BEO publication, RTM generation, RTM drift rejection, protected active-vault body reads, production `blk-link`, live Codex dispatch, package/network/model/browser/cyber tooling, signer/storage/ledger/rollback behavior, production isolation claims, HITL approval capture, active-vault promotion, or exact-ID retrieval.

## Exit Criteria

- Focused RED/GREEN tests for the contract pass.
- BLK-116 record, hostile review, and closeout docs exist.
- `git diff --check` passes.
- Commit lands separately from later 117-119 implementation work.
