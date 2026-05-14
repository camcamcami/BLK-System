# BLK-SYSTEM-120 — HITL Approval Capture and New Baseline Promotion Plan

**Status:** Planned / executing
**Date:** 2026-05-14
**Track:** Milestone 1 — BLK-req legislative gateway implementation
**Predecessors:** BLK-SYSTEM-116, BLK-SYSTEM-117, BLK-SYSTEM-118, BLK-SYSTEM-119

## Purpose

Implement the next BLK-req legislative gateway slice: deterministic capture of a Discord HITL approval record and approval-bound promotion of a lint-clean staging draft into the active BLK-req vault as a **new baseline**.

## Scope

1. Add a backend API that captures a Discord approval payload containing user ID, message ID, interaction timestamp, approval ID, exact staging relative path, and exact pre-promotion staging hash.
2. Add a backend API that promotes a staging draft only when:
   - the path is under `docs/requirements/staging/` or `docs/use_cases/staging/`;
   - staging lint passes;
   - the approval is explicit and Discord-bound;
   - the approval path and preview hash match the current staging draft;
   - the target active path is the next sequential `REQ-###.md` or `UC-###.md`;
   - no symlink component can redirect the active-vault write.
3. Convert new drafts from `id: "TBD"`, `status: "DRAFT"`, and `version_hash: "PENDING"` to a baselined active artifact with permanent ID, `status: "BASELINED"`, final canonical `version_hash`, and `baseline_authorization` audit metadata.
4. Remove the promoted staging draft only after the active file has been written via a temporary file + atomic replacement.
5. Update BLK-077, BLK-079, and executable doctrine gates to mark BLK-SYSTEM-120 complete and select the next frontier.

## Explicit Non-Scope

BLK-SYSTEM-120 does **not** implement staged revision checkout, active-vault overwrite of existing baselines, concurrency-lock revision overwrite, exact-ID retrieval for BEB planning, BEB dispatch, BLK-pipe runtime, BLK-test runtime, BEO publication, RTM generation, RTM drift rejection, protected active body reads for trace closure, Kuronode mutation, signer/storage/ledger behavior, network/model/browser/cyber tooling, or production isolation.

The sprint authorizes only deterministic local backend code for **new-baseline promotion** under explicit HITL approval input. It does not promote any real BLK-req artifact in this sprint; tests use temporary workspaces.

## RED Tests

Add failing tests for:

- approval capture requiring exact Discord identity, timezone-aware timestamp, staging path, and staging hash;
- new requirement baseline promotion assigning the next sequential `REQ-###`, injecting `baseline_authorization`, assigning final hash, deleting staging only after active write, and returning side-effect evidence;
- rejection of unapproved, mismatched-path, mismatched-hash, reused approval ID, active-target collision, and symlinked active-target cases before active writes;
- BLK-120 doctrine markers and next-frontier markers.

## Success Criteria

- Focused BLK-req tests pass.
- Doctrine gate for BLK-SYSTEM-120 passes.
- Full Python suite and Go suite pass.
- Hostile review records no blocking authority laundering or path bypass.
- Commit and push to `origin/main`.
