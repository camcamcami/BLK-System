# BLK-SYSTEM-101 — RTM Trace-Closure Authority Request After External BEO Publication Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` when executing.

**Goal:** Package the BLK-SYSTEM-100 external BEO publication record into an exact request for future local `blk-link` / RTM trace-closure execution authority without granting or executing that authority.
**BLK-024 track:** Track H — BLK-link offline RTM ledger; Track A — doctrine/review gates; maturity L0/L1 request fixture.
**Architecture:** BLK-001 keeps BEO publication and blk-link trace closure separate. BLK-100 provides a hash-bound publication record; BLK-101 may request the next exact trace-closure frontier but must not generate RTM, reject drift, compare active-vault hashes, or read protected bodies.
**Tech Stack:** Python deterministic fixture, Markdown doctrine/outcome/review artifacts, unittest gates.
**Authority boundary:** Request package only; no approval capture and no execution.

## Preflight State

```text
date: 2026-05-13T20:51:07+10:00
git: main at 4f48368 feat: execute blk-system 100 external beo publication
working tree: clean before sprint planning
```

## Exact Inputs

- `docs/BLK-100_external-beo-publication-execution.md`
- `docs/outcomes/BLK-SYSTEM-100_external-beo-publication-execution.json`
- `execution_package_id: BEO-PUBLICATION-EXECUTION-100-001`
- `execution_package_hash: sha256:5269146b6b46e27e38878a327b1ac6180068d5c9e427067604b611512a72289d`
- `publication_record_hash: sha256:1efbfd9b6b9d828b7b793c1c9c2b0f8115c36db69ef850e5a2f2ff94195923b4`

## Non-Authority Boundary

This sprint does not authorize or perform RTM generation, RTM drift rejection, active-vault hash comparison, protected BLK-req body reads/copying/parsing/hashing/scanning, signer/storage/ledger/rollback side effects, public ledger mutation, target/source/Git mutation, BEB dispatch, BEO closeout execution, BLK-pipe/BLK-test/Codex runtime, package/network/model/browser/cyber tooling, or production-isolation claims.

## Tasks

0. Publish this plan and `docs/outcomes/BLK-SYSTEM-101_task-000-outcome.md`.
1. Add RED tests for a BLK-101 request fixture that rejects forged BLK-100 hashes, run-ID reuse, nested authority laundering, missing/extra denied authorities, and premature RTM/trace execution.
2. Implement `python/rtm_trace_closure_authority_request_after_external_beo.py` minimally to pass the tests.
3. Generate `docs/BLK-101_rtm-trace-closure-authority-request-after-external-beo.md` and a hash-bound package artifact.
4. Update active roadmap/current-state surfaces and persistent doctrine gates.
5. Run hostile review, focused tests, full verification, closeout, commit, and push exact paths.

## Expected Output Marker

```text
RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_READY_AFTER_EXTERNAL_BEO_PUBLICATION_NOT_GRANTED
RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-101-001
EXACT_RTM_TRACE_CLOSURE_APPROVAL_DECISION_REQUIRED_NOT_CAPTURED
```
