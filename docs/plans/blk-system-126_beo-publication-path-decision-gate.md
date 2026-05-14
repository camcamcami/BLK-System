# BLK-SYSTEM-126 — BEO Publication Path Decision Gate Plan

**Status:** Planned for immediate execution
**Date:** 2026-05-15T06:31:24+10:00
**Documentation model:** lean — no `docs/BLK-126_*.md`; one sprint closeout only

## Goal

Build the smallest review-only decision gate that connects the BLK-SYSTEM-125 metadata-only BEB/BEO handoff to the BEO publication path without granting publication, signer/storage/ledger, RTM, BLK-pipe, BLK-test, Codex, target mutation, or protected-body authority.

## Scope

Touch only:

- `python/beo_publication_path_decision_gate.py` — new local review-only gate fixture.
- `python/test_beo_publication_path_decision_gate.py` — RED/GREEN tests.
- `python/blk_current_state_authority_index.py` and tests — mark BLK-SYSTEM-126 complete and next frontier planning-only.
- `docs/BLK-077_blk-system-post-078-roadmap.md` and `docs/BLK-079_post-078-current-state-authority-index.md` — Occam current-state update.
- `docs/outcomes/BLK-SYSTEM-126_sprint-closeout.md` — one closeout.

## Required Behavior

The gate must:

1. Accept only exact BLK-SYSTEM-125-style BEO/RTM interface metadata: `BEO_RTM_IFACE_###`, `BEO_###`, `BEB_###`, exact `REQ-###` / `UC-###`, and canonical `sha256:<64 lowercase hex>` trace hashes.
2. Bind the submitted interface by canonical hash and exact IDs.
3. Select exactly one next planning rung: `metadata_bound_beo_publication_prerequisite_request`.
4. Emit `READY_FOR_OPERATOR_REVIEW_NOT_AUTHORITY` evidence only.
5. Reject body text, protected paths, publication approval/execution, signer/storage/ledger, RTM/coverage/drift, BLK-pipe/BLK-test/Codex/runtime, source/Git mutation, tooling, and production-isolation laundering across top-level, nested, camelCase, compact, and percent-encoded variants.
6. Keep every side-effect flag false.

## Verification

- Focused RED then GREEN:
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_beo_publication_path_decision_gate -v`
- Related focused suite:
  - `python.test_beo_rtm_interface_fixtures`
  - `python.test_beo_publication_decision_package`
  - `python.test_beo_publication_prerequisite_request_after_evidence_refresh`
  - `python.test_blk_current_state_authority_index`
  - selected active doctrine gate
- Aggregate discovery after closeout.
- `git diff --check -- <exact changed paths>`.

## Authority Boundary

BLK-SYSTEM-126 is a decision gate only. It does not authorize or perform BEB dispatch, BEO closeout/publication, approval capture, signer/storage/ledger/rollback/revocation/supersession behavior, RTM generation, drift rejection, active-vault hash comparison, protected body reads/copying/scanning, BLK-pipe/BLK-test/Codex runtime, target/source/Git mutation, package/network/model/browser/cyber tooling, or production-isolation claims.

## Closeout

Write exactly one sprint closeout at `docs/outcomes/BLK-SYSTEM-126_sprint-closeout.md`. Do not create `docs/BLK-126_*.md` or per-task outcomes.
