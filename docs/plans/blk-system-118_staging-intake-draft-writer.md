# BLK-SYSTEM-118 — Staging Intake Draft Writer Plan

**Status:** Planned / executing
**Date:** 2026-05-14
**Track:** Milestone 1 — BLK-req legislative gateway implementation
**Predecessor:** BLK-SYSTEM-117 version-aware staging linter

## Purpose

Implement the second local backend operation named by the BLK-SYSTEM-116 contract: a safe staging intake writer for new requirement and use-case drafts.

## Scope

- Add `write_staging_draft()` to `python/lint_artifacts.py`.
- Write new draft artifacts only under `docs/requirements/staging/` or `docs/use_cases/staging/`.
- Generate strict draft frontmatter with `id: "TBD"`, `schema_version: "1.0"`, `parent_hash: ""`, `version_hash: "PENDING"`, `status: "DRAFT"`, required rationale, and linked node list.
- Run the BLK-SYSTEM-117 linter before write; invalid drafts must return diagnostics without creating a file.
- Document bounded self-remediation loop policy: maximum 3 attempts; this sprint does not implement autonomous LLM rewriting.

## RED Tests First

1. Tests must fail before implementation because `write_staging_draft` does not exist.
2. Requirement and use-case writer tests must prove output path and metadata shape.
3. Invalid drafts must not be written.
4. Path traversal and pre-existing draft overwrite attempts must fail closed.
5. Active-vault path writes must be absent.

## Explicit Non-Authority

This sprint does not authorize active-vault writes, active-vault body reads, HITL approval capture, baseline promotion, exact-ID retrieval, revision checkout, concurrency lock, BLK-pipe dispatch, BLK-test runtime, BEO publication, RTM generation, RTM drift rejection, target/source/Git mutation beyond this repository commit, package/network/model/browser/cyber tooling, signer/storage/ledger behavior, or production isolation claims.

## Exit Criteria

- Focused RED/GREEN tests pass.
- BLK-118 record, hostile review, and closeout docs exist.
- BLK-SYSTEM-116 contract and BLK-SYSTEM-117 linter tests remain green.
- `git diff --check` passes.
