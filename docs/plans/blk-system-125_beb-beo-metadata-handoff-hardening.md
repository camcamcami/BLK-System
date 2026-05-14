# BLK-SYSTEM-125 — BEB/BEO Metadata Handoff Hardening Plan

**Status:** Execution plan
**Date:** 2026-05-14T20:11:52+10:00
**Documentation model:** Lean — no BLK-125 doctrine doc unless a durable interface contract emerges; one sprint closeout only.

## Goal

Close the BEB/BEO metadata handoff frontier by ensuring draft BEO/RTM interface metadata carries exact BLK-req IDs and version hashes only, without copying protected bodies or implying BEB/BEO/RTM authority.

## Scope

- Harden `python/beo_rtm_interface_fixtures.py` trace artifact validation.
- Add regression tests in `python/test_beo_rtm_interface_fixtures.py` and related existing gate tests as needed.
- Update BLK-077 / BLK-079 / executable current-state surfaces after the frontier is complete.
- Create exactly one outcome: `docs/outcomes/BLK-SYSTEM-125_sprint-closeout.md`.

## Required Behavior

- Accept only trace artifacts with:
  - `kind` in `{REQ, UC}`;
  - exact matching `id` format `REQ-###` or `UC-###`;
  - canonical `version_hash` format `sha256:<64 lowercase hex>`;
  - no extra keys.
- Reject trace artifacts that contain protected body/path fields, protected path text, active-vault path strings, body excerpts, authority wording, or mismatched kind/id pairs.
- Preserve metadata-only handoff flags:
  - no active-vault read;
  - no requirements resolution;
  - no BEB dispatch;
  - no BEO closeout/publication;
  - no RTM generation/drift decision;
  - no signer/storage/ledger/rollback behavior.

## Verification

- RED/GREEN focused tests for BEO/RTM interface fixture metadata hardening.
- Current-state / lean-doc gate tests after roadmap/index updates.
- Full unittest discovery before commit.
- Local hostile audit for protected-body leakage, authority laundering, stale roadmap wording, and lean-doc invariants.

## Authority Boundary

BLK-SYSTEM-125 is metadata validation only. It does not authorize BEB writing/dispatch, BEO closeout/publication, RTM generation, drift rejection, active-vault body reads outside the BLK-req backend path, BLK-pipe runtime, BLK-test runtime/MCP, source/Git mutation, package/network/model/browser/cyber tooling, signer/storage/public-ledger/rollback behavior, or production-isolation claims.
