# BLK-SYSTEM-142 — Metadata-Bound RTM-Generation Authority Request Plan

**Status:** Planned
**Date:** 2026-05-15T18:26:10+10:00
**Sprint:** BLK-SYSTEM-142

## 1. Objective

Package the clean BLK-SYSTEM-141 active-vault hash-comparison reconciliation into one metadata-bound RTM-generation authority request for future operator review.

This sprint is request-only. It must not approve, reserve, consume, or execute any RTM-generation run.

## 2. Scope

- Consume `ACTIVE-VAULT-HASH-COMPARISON-POST-EXECUTION-RECONCILIATION-141-001` by exact ID and canonical package hash.
- Emit `RTM-GENERATION-AUTHORITY-REQUEST-142-001` as a deterministic local fixture package.
- Bind exact upstream reconciliation hash, context hash, BEO/BEB IDs, exact trace identities, request window, proof obligations, denied authorities, and false side-effect flags.
- Update only the active roadmap/current-state surfaces needed to reflect the new request-only frontier.
- Produce exactly one sprint closeout outcome.

## 3. Non-Authority Boundary

BLK-SYSTEM-142 does not grant or perform:

- RTM generation approval, execution, run reservation, or run consumption;
- drift rejection, authoritative drift decisions, coverage truth, or reusable production `blk-link`;
- protected BLK-req body reads/copying/parsing/hashing/scanning/mutation;
- active-vault filesystem reads/scans beyond consuming submitted BLK-141 evidence;
- signer/storage/ledger/rollback/revocation/supersession behavior;
- BEB dispatch, BEO closeout execution, or BEO publication/signing;
- target/source/Git mutation by the fixture;
- BLK-pipe, BLK-test, Codex, arbitrary shell, package-manager, network, model, browser, cyber tooling, or production-isolation claims.

## 4. TDD / Verification Plan

1. RED: add focused tests for successful request packaging and rejection of forged BLK-141 evidence, stale/replayed/expired requests, malformed exact IDs/hashes, authority laundering, protected paths/body snippets, bad exact sets, side-effect flags, and live-tool/protected-file access.
2. GREEN: implement the smallest deterministic fixture to pass.
3. Update `python/blk_current_state_authority_index.py`, BLK-077, BLK-079, and active doctrine tests with request-only BLK-142 markers.
4. Run hostile audit, focused tests, full Python suite, `git diff --check`, and exact-path commit/push.

## 5. Documentation Burden Check

No new BLK-### doctrine document is planned. This plan exists because the user explicitly asked to plan and execute. Closeout will be one file: `docs/outcomes/BLK-SYSTEM-142_sprint-closeout.md`.
