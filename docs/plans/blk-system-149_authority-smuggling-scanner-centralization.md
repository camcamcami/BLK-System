# BLK-SYSTEM-149 — Authority-Smuggling Scanner Centralization Plan

## Goal

Centralize current-state authority-smuggling normalization and scanning so future hardening does not duplicate fragile denylist/percent-decoding logic.

## Scope

- Add a small reusable Python scanner module for compact/camel/percent-decoded authority and protected-path probes.
- Route the current-state authority index through the shared scanner.
- Add focused regression tests for encoded authority claims, compact authority tokens, protected active paths, and no false positive on denial prose.

## Authority Boundary

This sprint is hardening-only. It selects no authority rung and grants no runtime, BEB/BEO, RTM, drift, publication, protected-body, signer/storage/ledger, tooling, BLK-pipe/BLK-test/Codex, target/source/Git mutation outside this repo patch, or production-isolation authority.

## Verification

- RED/GREEN focused scanner and current-state tests.
- Broad Python discovery after closeouts.
- One closeout only: `docs/outcomes/BLK-SYSTEM-149_sprint-closeout.md`.
- No new `docs/BLK-149_*.md`.
