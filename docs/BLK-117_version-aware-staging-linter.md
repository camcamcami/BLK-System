# BLK-117 — Version-Aware Staging Linter

**Status:** Active BLK-req staging linter record — not approval, promotion, or hash-assignment authority
**Date:** 2026-05-14
**Sprint:** BLK-SYSTEM-117
**Track:** Milestone 1 — BLK-req legislative gateway implementation
**Predecessor:** BLK-SYSTEM-116

## Purpose

BLK-SYSTEM-117 implements the first local backend operation named by the BLK-SYSTEM-116 contract: a deterministic version-aware linter for BLK-req requirement and use-case drafts under staging directories only.

## Required Markers

```text
BLK_SYSTEM_117_VERSION_AWARE_STAGING_LINTER
LINTER_ROUTES_REQUIREMENTS_AND_USE_CASES_BY_STAGING_PATH
DRAFT_METADATA_SCHEMA_VERSION_1_0_ENFORCED
ACTIVE_VAULT_BODY_READS_REJECTED_BY_LINTER
STRUCTURED_JSON_DIAGNOSTICS_RETURNED
NO_ACTIVE_PROMOTION_OR_HASH_ASSIGNMENT_BY_117
```

## Enforced Behavior

1. `python/lint_artifacts.py::lint_artifact()` classifies paths before body reads.
2. Only direct Markdown files under `docs/requirements/staging/` and `docs/use_cases/staging/` are eligible.
3. Requirements route to metadata schema validation plus atomicity/subjective-vocabulary checks.
4. Use cases route to metadata schema validation plus the 500-word narrative bound; strict requirement atomicity is intentionally suspended for use-case narrative prose.
5. Draft metadata enforces `schema_version: "1.0"`, `status: "DRAFT"`, `version_hash: "PENDING"`, required `rationale`, required `linked_nodes`, and bracket link syntax such as `[[REQ-001]]` or `[[UC-001]]`.
6. Diagnostics return deterministic JSON-like dictionaries with stable `code`, `message`, and `field` keys.
7. Active and non-staging paths return `PATH_NOT_STAGING` or related diagnostics before artifact body reads.

## Explicit Non-Authority

BLK-SYSTEM-117 grants no active-vault body reads, no active-vault writes, no HITL approval capture, no baseline promotion, no exact-ID retrieval, no BLK-pipe dispatch, no BLK-test runtime, no BEO publication, no RTM generation or drift rejection, no target/source/Git mutation, no package/network/model/browser/cyber tooling, no signer/storage/ledger/rollback behavior, and no production isolation claim.

## BLK-test Vocabulary

BLK-test is a BLK-System functional module, not BLK-System's test suite. The staging linter is a BLK-req backend component; it does not consume BLK-test evidence as approval or verification authority.
