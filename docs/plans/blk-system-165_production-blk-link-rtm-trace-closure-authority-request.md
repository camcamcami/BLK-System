# BLK-SYSTEM-165 — Production `blk-link` / RTM Trace-Closure Authority Request Plan

**Status:** Planned for immediate execution
**Date:** 2026-05-16T13:33:10+10:00

## Goal

Emit one deterministic, request-only authority package for a future narrowly bounded production `blk-link` / RTM trace-closure approval-capture step.

## Scope

- Consume the exact BLK-SYSTEM-162 post trace-closure review package and BLK-SYSTEM-163/164 hardening state.
- Produce review-ready request evidence only.
- Update the active roadmap/current-state index to the next frontier: exact approval capture, not execution.

## Files Expected

- `python/production_blk_link_rtm_trace_closure_authority_request_165.py`
- `python/test_production_blk_link_rtm_trace_closure_authority_request_165.py`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_metadata_rtm_post_generation_ladder_159_162.py`
- `python/test_lean_documentation_policy.py`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `docs/outcomes/BLK-SYSTEM-165_sprint-closeout.md`

## Authority Boundary

This sprint does not approve, reserve a run ID for, or execute production `blk-link`; does not generate RTM; does not reject drift; does not establish coverage truth; does not compare/read/scan/hash protected BLK-req bodies; does not dispatch BEB/BEO/BLK-pipe/BLK-test/Codex; does not mutate target/source/Git state; and does not grant signer/storage/ledger reuse or production-isolation claims.

## Validation

1. RED focused test for missing request fixture.
2. GREEN focused request/current-state/lean-doc tests.
3. Hostile audit for hash binding, false flags, authority laundering, active-doc stale frontier removal, and live-tool imports.
4. Full Python unittest discovery and `git diff --check`.

## Documentation Burden

No new `docs/BLK-###` document. One plan because the sprint is authority-sensitive, and one closeout outcome at completion.
