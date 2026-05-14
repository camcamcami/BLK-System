# BLK-SYSTEM-122..124 — BLK-req Revision Lifecycle Plan

**Status:** Execution plan
**Date:** 2026-05-14T19:11:27+10:00
**Documentation model:** Lean — no BLK-### sprint docs, one closeout outcome per sprint.

## Objective

Close the BLK-req frontier selected after BLK-SYSTEM-120: exact-ID active artifact retrieval, staged revision drafts, and HITL revision promotion with parent-hash concurrency checks.

## Sprint slices

### BLK-SYSTEM-122 — Exact-ID retrieval

- Add deterministic retrieval for one active `REQ-###` or `UC-###` by exact ID.
- Map IDs directly to `docs/requirements/active/<id>.md` or `docs/use_cases/active/<id>.md`.
- Reject malformed IDs, missing files, symlinked active paths, metadata/path ID mismatch, and any need for broad active-vault scanning.

### BLK-SYSTEM-123 — Staged revision drafts

- Add a revision draft writer that starts from exact-ID retrieval.
- Write only to staging with existing artifact ID, `parent_hash` bound to the active artifact version hash, `version_hash: PENDING`, and `status: DRAFT`.
- Preserve no active-vault writes and no adjacent authority.

### BLK-SYSTEM-124 — HITL revision promotion

- Add approval-bound revision promotion for staged drafts.
- Re-read exact active artifact, require current `version_hash == parent_hash`, then atomically replace the exact active artifact.
- Consume approval IDs only after successful active write; roll back active write if replay-ledger persistence fails.

## Validation

- RED/GREEN focused tests in `python/test_blk_req_legislative_gateway.py`.
- Current-state gates in `python/test_blk_current_state_authority_index.py`.
- Lean documentation policy regression.
- Full Python discovery and `git diff --check` before commit.

## Authority boundary

This plan authorizes local deterministic BLK-req backend helpers only. It does not authorize BEB dispatch, BEO closeout/publication, BLK-pipe runtime dispatch, BLK-test runtime/MCP, RTM generation, drift rejection, coverage truth, non-BLK-req target/source/Git mutation, package/network/model/browser/cyber tooling, signer/storage/public-ledger/rollback behavior, or production-isolation claims.
