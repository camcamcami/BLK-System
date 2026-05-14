# BLK-119 — Canonical Version Hash Engine

**Status:** Active BLK-req canonical hash engine record — not baseline promotion, retrieval, or drift authority
**Date:** 2026-05-14
**Sprint:** BLK-SYSTEM-119
**Track:** Milestone 1 — BLK-req legislative gateway implementation
**Predecessors:** BLK-SYSTEM-116, BLK-SYSTEM-117, BLK-SYSTEM-118

## Purpose

BLK-SYSTEM-119 implements deterministic canonical serialization and `version_hash` computation for BLK-req artifacts. It completes the 116-119 foundation slice: contract, staging linter, staging draft writer, and hash engine.

## Required Markers

```text
BLK_SYSTEM_119_CANONICAL_VERSION_HASH_ENGINE
CANONICAL_SERIALIZATION_FIELDS_ID_SCHEMA_STATUS_RATIONALE_LINKS_BODY
VERSION_HASH_SHA256_LOWERCASE_HEX
VERSION_HASH_IGNORES_PARENT_HASH_AND_PREEXISTING_VERSION_HASH_FIELD
HASH_PREVIEW_STAGING_ONLY_NO_ACTIVE_VAULT_READ
NO_BASELINE_PROMOTION_OR_DRIFT_DECISION_BY_119
BLK_REQ_LEGISLATIVE_GATEWAY_FOUNDATION_116_119_COMPLETE
STAGING_LINTER_DRAFT_WRITER_AND_HASH_ENGINE_COMPLETE
NEXT_FRONTIER_BLK_REQ_HITL_BASELINE_PROMOTION_PLANNING_NOT_EXECUTION_AUTHORITY
NO_ACTIVE_VAULT_PROMOTION_OR_RETRIEVAL_BY_119
```

## Enforced Behavior

1. `canonicalize_artifact_text()` serializes exactly these fields: `id`, `schema_version`, `status`, `rationale`, `linked_nodes`, and exact Markdown body bytes after frontmatter parsing.
2. `compute_version_hash()` returns `sha256:<64-lowercase-hex>` over the deterministic JSON canonical serialization.
3. `parent_hash` and any pre-existing `version_hash` field are excluded from canonical input.
4. Changes to the canonical fields or body change the hash.
5. `preview_staging_version_hash()` computes a staging-only hash preview and rejects active or non-staging paths before body reads.
6. Hash preview packages carry false side-effect fields for active-vault read/write, baseline promotion, RTM generation, and drift decisions.

## 116-119 Foundation Close

BLK_REQ_LEGISLATIVE_GATEWAY_FOUNDATION_116_119_COMPLETE records that the first Milestone 1 foundation group is complete:

- BLK-SYSTEM-116: contract scaffold.
- BLK-SYSTEM-117: version-aware staging linter.
- BLK-SYSTEM-118: staging intake draft writer.
- BLK-SYSTEM-119: canonical serialization and version hash engine.

The next frontier is `NEXT_FRONTIER_BLK_REQ_HITL_BASELINE_PROMOTION_PLANNING_NOT_EXECUTION_AUTHORITY`. It requires a new sprint and does not inherit authority from the hash preview engine.

## Explicit Non-Authority

BLK-SYSTEM-119 grants no active-vault promotion, no active-vault overwrite, no HITL approval capture, no revision checkout, no exact-ID retrieval, no active-vault hash comparison for trace closure, no RTM drift decision, no BLK-pipe dispatch, no BLK-test runtime, no BEO publication, no RTM generation, no target/source/Git mutation outside this BLK-System sprint, no package/network/model/browser/cyber tooling, no signer/storage/ledger/rollback behavior, and no production isolation claim.

## BLK-test Vocabulary

BLK-test is a BLK-System functional module, not BLK-System's test suite. BLK-test evidence does not authorize BLK-req hash previews, active-vault promotion, retrieval, BEO publication, RTM generation, or drift decisions.
