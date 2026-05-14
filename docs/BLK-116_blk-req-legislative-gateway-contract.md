# BLK-116 — BLK-req Legislative Gateway Contract

**Status:** Active BLK-req gateway contract record — not execution or promotion authority
**Date:** 2026-05-14
**Sprint:** BLK-SYSTEM-116
**Track:** Milestone 1 — BLK-req legislative gateway implementation

## Purpose

BLK-SYSTEM-116 creates the first executable contract scaffold for the BLK-req legislative gateway. It pins the allowed local backend slices for BLK-SYSTEM-117 through BLK-SYSTEM-119 while preserving the post-103 cutline that protected active-vault bodies are not available to BLK-pipe, BLK-test, BEO, RTM, Codex, health-check, profile, or generic helper surfaces.

## Required Markers

```text
BLK_SYSTEM_116_BLK_REQ_LEGISLATIVE_GATEWAY_CONTRACT
CONTRACT_READY_NOT_EXECUTION_AUTHORITY
ALLOWED_LOCAL_BACKEND_OPERATIONS_117_118_119_ONLY
DENIED_ADJACENT_AUTHORITIES_EXACT_SET_PINNED
NO_HITL_APPROVAL_CAPTURE_OR_ACTIVE_PROMOTION_BY_116
BLK_REQ_LEGISLATIVE_GATEWAY_MILESTONE_1_STARTED
```

## Contract Surface

The contract in `python/lint_artifacts.py` exposes exactly these local backend operation names for the next slices:

1. `BLK_SYSTEM_117_STAGING_LINTER`
2. `BLK_SYSTEM_118_STAGING_DRAFT_WRITER`
3. `BLK_SYSTEM_119_CANONICAL_VERSION_HASH_ENGINE`

This is a planning and local deterministic backend scaffold only. BLK-SYSTEM-120 and later work must separately scope HITL approval capture, baseline promotion, revision concurrency locks, active-vault overwrite, or exact-ID retrieval.

## Denied Adjacent Authorities

BLK-SYSTEM-116 pins exact denied authorities in code and tests:

- `BLK_PIPE_RUNTIME_DISPATCH`
- `TARGET_SOURCE_GIT_MUTATION`
- `BLK_TEST_RUNTIME`
- `BEO_PUBLICATION`
- `RTM_GENERATION`
- `RTM_DRIFT_REJECTION`
- `PROTECTED_ACTIVE_BODY_READS`
- `ACTIVE_VAULT_WRITE`
- `LIVE_CODEX_DISPATCH`
- `NETWORK_MODEL_BROWSER_CYBER_TOOLING`
- `PACKAGE_MANAGER_TOOLING`
- `SIGNER_STORAGE_LEDGER_ROLLBACK`
- `PRODUCTION_ISOLATION_CLAIM`
- `HITL_APPROVAL_CAPTURE`
- `ACTIVE_VAULT_PROMOTION`
- `EXACT_ID_RETRIEVAL`

Every matching side-effect flag remains false in the contract record.

## BLK-test Vocabulary

BLK-test is a BLK-System functional module, not BLK-System's test suite. BLK-test evidence or future BLK-test module behavior cannot be inherited by the BLK-req gateway contract as approval, promotion, BEO, RTM, protected-read, or runtime authority.

## Explicit Non-Authority

This record grants no BLK-pipe runtime dispatch, no target/source/Git mutation, no BLK-test runtime, no BEO publication, no RTM generation, no RTM drift rejection, no protected active-vault body reads, no production `blk-link`, no live Codex dispatch, no package/network/model/browser/cyber tooling, no signer/storage/ledger/rollback behavior, no production isolation claim, no HITL approval capture, no active-vault promotion, and no exact-ID retrieval.
