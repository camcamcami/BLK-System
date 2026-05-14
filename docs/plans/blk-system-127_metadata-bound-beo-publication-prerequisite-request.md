# BLK-SYSTEM-127 — Metadata-Bound BEO Publication Prerequisite Request Plan

**Status:** Planned for execution
**Date:** 2026-05-15T07:30:10+10:00
**Documentation model:** Lean — no new BLK document by default; one sprint closeout only.

## 1. Goal

Package the BLK-SYSTEM-126 review-only decision gate and BLK-SYSTEM-125 metadata interface into a deterministic metadata-bound BEO publication prerequisite request.

The request must be ready for future human review while preserving the boundary that no publication approval, publication execution, signer/storage/ledger operation, RTM generation, BLK-pipe/BLK-test/Codex runtime, target/source/Git mutation, or protected-body access is granted.

## 2. Scope

Implement the smallest local fixture surface:

- `python/metadata_bound_beo_publication_prerequisite_request.py`
- `python/test_metadata_bound_beo_publication_prerequisite_request.py`
- targeted updates to current-state/roadmap gate tests and docs only where needed:
  - `python/blk_current_state_authority_index.py`
  - `python/test_blk_current_state_authority_index.py`
  - active doctrine/lean-doc tests if they pin current frontier wording
  - `docs/BLK-077_blk-system-post-078-roadmap.md`
  - `docs/BLK-079_post-078-current-state-authority-index.md`

## 3. TDD / Validation Plan

1. RED: add tests proving the request cannot be built yet and must reject:
   - forged or rehashed upstream decision gates;
   - mismatched interface/gate/request IDs and canonical hashes;
   - Unicode-digit exact IDs and Discord identity spoofing;
   - nested authority/protected-body/secret laundering;
   - positive side-effect flags and incomplete/duplicate excluded-authority sets;
   - caller mutation after hash-bound package creation.
2. GREEN: implement the minimal fixture to pass the tests.
3. Update active current-state markers from BLK-SYSTEM-126 frontier to BLK-SYSTEM-127 request complete.
4. Verify focused tests, hostile audit probes, full Python suite, and `git diff --check`.

## 4. Authority Boundary

BLK-SYSTEM-127 may create request-readiness evidence only. It does **not** authorize:

- BEB dispatch or BEO closeout execution;
- publication approval capture;
- authoritative BEO publication or runtime `PUBLISHED` output;
- signer key material, cryptographic signing, immutable storage, public ledger append/mutation, rollback, revocation, or supersession;
- RTM generation, RTM drift rejection, active-vault hash comparison, coverage-truth promotion, or production `blk-link`;
- protected BLK-req body reads/copying/parsing/hashing/scanning/mutation;
- BLK-pipe runtime dispatch, BLK-test runtime/production MCP, live Codex, package/network/model/browser/cyber tooling, target/source/Git mutation, or production-isolation claims.

## 5. Closeout Checklist

- One outcome only: `docs/outcomes/BLK-SYSTEM-127_sprint-closeout.md`.
- No new `docs/BLK-###` unless implementation reveals a durable reusable contract that cannot live in code/tests/outcome.
- No BLK-001 through BLK-006 current-state edits.
- Exact-path Git staging only.
