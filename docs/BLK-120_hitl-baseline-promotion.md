# BLK-120 — HITL Baseline Promotion

**Status:** Active BLK-req new-baseline promotion backend record — not staged revision, exact-ID retrieval, BEB dispatch, BEO publication, RTM generation, or drift authority
**Date:** 2026-05-14
**Sprint:** BLK-SYSTEM-120
**Track:** Milestone 1 — BLK-req legislative gateway implementation
**Predecessors:** BLK-SYSTEM-116, BLK-SYSTEM-117, BLK-SYSTEM-118, BLK-SYSTEM-119

## Purpose

BLK-SYSTEM-120 implements deterministic backend support for capturing Discord HITL approval input and promoting a lint-clean staging draft into the active BLK-req vault as a **new baseline**.

## Required Markers

```text
BLK_SYSTEM_120_HITL_BASELINE_PROMOTION
BLK_SYSTEM_120_HITL_BASELINE_PROMOTION_COMPLETE
DISCORD_HITL_APPROVAL_CAPTURED_FOR_NEW_BASELINES
NEW_BASELINE_PROMOTION_WRITES_ACTIVE_VAULT_BY_BACKEND_ONLY
BASELINE_VERSION_HASH_ASSIGNED_ON_PROMOTION
APPROVAL_BINDS_DISCORD_USER_MESSAGE_TIMESTAMP_PATH_AND_HASH
ACTIVE_VAULT_WRITE_PATH_REJECTS_SYMLINKS_AND_COLLISIONS
ACTIVE_VAULT_PUBLISH_IS_NO_OVERWRITE_EXCLUSIVE_CREATE
APPROVAL_REPLAY_LEDGER_CONSUMES_BASELINE_APPROVAL_IDS
APPROVAL_REPLAY_LEDGER_NOT_CONSUMED_ON_PUBLISH_FAILURE
DISCORD_IDENTITY_VALUES_MUST_BE_SNOWFLAKE_STRINGS
NO_REVISION_OVERWRITE_OR_EXACT_ID_RETRIEVAL_BY_120
NEXT_FRONTIER_BLK_REQ_STAGED_REVISION_AND_EXACT_ID_RETRIEVAL_PLANNING_NOT_EXECUTION_AUTHORITY
```

## Implemented Backend Surface

`python/lint_artifacts.py` now exposes:

1. `capture_baseline_approval(...)`
   - accepts an explicit Discord HITL approval payload;
   - requires `idp=discord`, `approved=True`, approval ID, numeric Discord snowflake user ID, numeric Discord snowflake message ID, timezone-aware interaction timestamp, exact staging relative path, and exact staging preview hash;
   - returns an `approval_record_hash`;
   - performs no active-vault write and no promotion.
2. `promote_staging_draft_to_baseline(...)`
   - accepts one staging artifact and one approval payload;
   - re-lints the staging draft;
   - recomputes and compares the staging preview hash;
   - assigns the next sequential `REQ-###` or `UC-###` by active-vault filename scan only;
   - injects `baseline_authorization` metadata;
   - computes the final canonical `version_hash`;
   - writes the active-vault target with a no-overwrite exclusive-create operation so a raced target cannot be replaced;
   - records the consumed approval ID in a workspace-local replay ledger only after active publish succeeds, and rolls back the active publish if replay-ledger persistence fails;
   - deletes the staging draft only after the active write succeeds.

## Authority Boundary

BLK-SYSTEM-120 authorizes deterministic local backend code for new-baseline promotion under explicit HITL approval input. It does not promote any real BLK-req artifact during this sprint; sprint tests use temporary workspaces.

BLK-SYSTEM-120 grants no staged revision checkout, no active-vault overwrite of an existing baseline, no concurrency-lock revision overwrite, no exact-ID retrieval for BEB planning, no BEB dispatch, no BLK-pipe runtime dispatch, no BLK-test runtime, no BEO publication, no RTM generation, no RTM drift rejection, no protected active body reads for trace closure, no non-BLK-req/Kuronode mutation, no package/network/model/browser/cyber tooling, no signer/storage/public-authority-ledger/rollback behavior, and no production isolation claim.

## BLK-test Vocabulary

BLK-test is a BLK-System functional module, not BLK-System's test suite. BLK-test evidence does not authorize BLK-req promotion, retrieval, BEO publication, RTM generation, drift rejection, source mutation, or runtime dispatch.
