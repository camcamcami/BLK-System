# BLK-SYSTEM-117 — Version-Aware Staging Linter Backend Plan

**Status:** Planned / executing
**Date:** 2026-05-14
**Track:** Milestone 1 — BLK-req legislative gateway implementation
**Predecessor:** BLK-SYSTEM-116 contract scaffold

## Purpose

Implement the first local backend operation named by the BLK-SYSTEM-116 contract: a version-aware staging linter for BLK-req requirement and use-case drafts.

## Scope

- Add staging-only artifact parsing and linting to `python/lint_artifacts.py`.
- Route artifact rules by path:
  - `docs/requirements/staging/*.md` -> requirement schema plus atomicity/subjective vocabulary gates.
  - `docs/use_cases/staging/*.md` -> use-case schema plus 500-word narrative bound.
- Enforce draft metadata: `schema_version: "1.0"`, `status: "DRAFT"`, `version_hash: "PENDING"`, required `rationale`, required `linked_nodes`, and `[[REQ-###]]` / `[[UC-###]]` link syntax.
- Return deterministic structured diagnostic payloads.

## RED Tests First

1. Tests must fail before implementation because `lint_artifact` does not exist.
2. Requirement tests must prove compound/subjective prose is rejected outside bullets.
3. Use-case tests must prove atomicity is suspended while the 500-word bound remains enforced.
4. Path-boundary tests must prove active/non-staging paths are rejected before file reads.

## Explicit Non-Authority

This sprint does not authorize active-vault body reads, active-vault writes, HITL approval capture, baseline promotion, exact-ID retrieval, BLK-pipe dispatch, BLK-test runtime, BEO publication, RTM generation, RTM drift rejection, target/source/Git mutation, tooling/network/package-manager behavior, signer/storage/ledger behavior, or production isolation claims.

## Exit Criteria

- Focused RED/GREEN tests pass.
- BLK-117 record, hostile review, and closeout docs exist.
- BLK-SYSTEM-116 contract still validates.
- `git diff --check` passes.
