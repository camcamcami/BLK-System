# BLK-118 — Staging Intake Draft Writer

**Status:** Active BLK-req staging writer record — not approval or active-vault promotion authority
**Date:** 2026-05-14
**Sprint:** BLK-SYSTEM-118
**Track:** Milestone 1 — BLK-req legislative gateway implementation
**Predecessor:** BLK-SYSTEM-117

## Purpose

BLK-SYSTEM-118 implements the second local backend operation named by the BLK-SYSTEM-116 contract: a safe staging intake writer for new BLK-req requirement and use-case drafts.

## Required Markers

```text
BLK_SYSTEM_118_STAGING_DRAFT_WRITER
DRAFT_WRITER_OUTPUTS_ONLY_TO_STAGING_DIRECTORIES
NEW_DRAFT_METADATA_ID_TBD_VERSION_HASH_PENDING
INVALID_DRAFTS_RETURN_DIAGNOSTICS_WITHOUT_WRITING
MAX_SELF_REMEDIATION_ATTEMPTS_THREE_DOCUMENTED
NO_HITL_APPROVAL_CAPTURE_OR_ACTIVE_PROMOTION_BY_118
```

## Enforced Behavior

1. `python/lint_artifacts.py::write_staging_draft()` accepts a new requirement or use-case draft request and builds strict frontmatter.
2. Requirement drafts write only below `docs/requirements/staging/`.
3. Use-case drafts write only below `docs/use_cases/staging/`.
4. New drafts always use `id: "TBD"`, `schema_version: "1.0"`, `parent_hash: ""`, `version_hash: "PENDING"`, and `status: "DRAFT"`.
5. The BLK-SYSTEM-117 linter runs before any file write. Invalid drafts return structured diagnostics and `written: false` without creating a file.
6. Filename slugs are lowercase alphanumeric/hyphen only; traversal and path separators are rejected.
7. Existing draft filenames fail closed unless an explicit caller-owned overwrite flag is passed.
8. The returned package records `max_self_remediation_attempts: 3`; BLK-SYSTEM-118 documents the cap but does not implement autonomous LLM rewriting.

## Explicit Non-Authority

BLK-SYSTEM-118 grants no active-vault writes, no active-vault body reads, no HITL approval capture, no baseline promotion, no exact-ID retrieval, no revision checkout, no concurrency lock, no BLK-pipe dispatch, no BLK-test runtime, no BEO publication, no RTM generation or drift rejection, no target/source/Git mutation outside this BLK-System sprint, no package/network/model/browser/cyber tooling, no signer/storage/ledger/rollback behavior, and no production isolation claim.

## BLK-test Vocabulary

BLK-test is a BLK-System functional module, not BLK-System's test suite. The draft writer does not consume BLK-test evidence and does not treat any BLK-test result as BLK-req approval or promotion authority.
