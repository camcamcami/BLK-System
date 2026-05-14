# BLK-SYSTEM-119 — Canonical Serialization and Version Hash Engine Plan

**Status:** Planned / executing
**Date:** 2026-05-14
**Track:** Milestone 1 — BLK-req legislative gateway implementation
**Predecessor:** BLK-SYSTEM-118 staging draft writer

## Purpose

Implement the third local backend operation named by the BLK-SYSTEM-116 contract: deterministic canonical serialization and `version_hash` computation for BLK-req artifacts.

## Scope

- Add canonical serialization for the exact BLK-005/006 field scope: `id`, `schema_version`, `status`, `rationale`, `linked_nodes`, and exact Markdown body.
- Add SHA-256 `version_hash` computation with `sha256:<64-lowercase-hex>` output.
- Exclude `parent_hash` and any pre-existing `version_hash` field from canonical input.
- Add staging-only hash preview for drafts without active-vault reads or promotion.
- Reconcile roadmap/current-state surfaces to record the 116-119 foundation as complete and point the next frontier to BLK-SYSTEM-120 planning, not execution authority.

## RED Tests First

1. Tests must fail before implementation because canonical hash functions do not exist.
2. Hash tests must prove body/rationale/status/link changes alter the hash while `parent_hash` and pre-existing `version_hash` do not.
3. Staging preview tests must reject active paths before reads.
4. Doctrine/current-state tests must fail until BLK-119 and roadmap/index markers are patched.

## Explicit Non-Authority

This sprint does not authorize active-vault promotion, active-vault overwrite, HITL approval capture, revision checkout, exact-ID retrieval, RTM drift decisions, active-vault hash comparison for trace closure, BLK-pipe dispatch, BLK-test runtime, BEO publication, RTM generation, target/source/Git mutation outside this BLK-System sprint, package/network/model/browser/cyber tooling, signer/storage/ledger behavior, or production isolation claims.

## Exit Criteria

- Focused RED/GREEN tests pass.
- BLK-119 record, hostile review, and closeout docs exist.
- BLK-077, BLK-079, and `python/blk_current_state_authority_index.py` acknowledge the 116-119 foundation and next frontier.
- Aggregate Python and Go verification passes before final push.
