# BLK-SYSTEM-095 — Exact Local RTM Drift-Rejection Execution Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `blk-system-authority-gated-sprints` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable.

**Goal:** Execute exactly one local, non-authoritative RTM drift-rejection fixture bound to `RTM-DRIFT-REJECTION-APPROVAL-DECISION-093-001`, then align roadmap/current-state docs without promoting runtime `blk-link` closure.

**BLK-024 track:** Track H — BLK-link offline RTM ledger, with Track A doctrine/current-state gates. Maturity level L1 local activation/fixture only.

**Architecture:** BLK-001 keeps BEO publication, RTM generation, drift rejection, protected-body access, external ledger mutation, and source/Git mutation as separate authority surfaces. BLK-SYSTEM-094 clarified that the BLK-SYSTEM-087 through BLK-SYSTEM-093 ladder is local and non-authoritative, but BLK-SYSTEM-093 contains a scoped approval-decision package for one future local drift-rejection execution sprint. BLK-SYSTEM-095 consumes that exact package locally and emits deterministic evidence only.

**Tech Stack:** Markdown doctrine/roadmap/outcome docs plus Python deterministic fixture and unittest gates.

**Authority boundary:** Exact local execution only. This sprint may consume `RUN-BLK-SYSTEM-091-RTM-DRIFT-REJECTION-001` inside a local fixture and produce `PILOT_LOCAL_RTM_DRIFT_REJECTION_RECORDED_NOT_AUTHORITATIVE`. It grants no reusable/runtime RTM drift-rejection authority, no authoritative drift decision, no runtime `blk-link` trace closure, no active-vault hash comparison, no protected-body reads/hashing, no external ledger mutation, no external authoritative publication, no signer/storage/rollback effects, no target/source/Git mutation by fixtures, no BEB dispatch, no BEO closeout execution, no BLK-pipe/BLK-test/Codex runtime, no package/network/model/browser/cyber tooling, and no production-isolation claim.

## Current Known State

Captured during preflight:

```text
git status: ## main...origin/main
HEAD: b45a797 docs: align post-093 rtm ladder state
Date: 2026-05-13T11:15:51+10:00
```

BLK-SYSTEM-094 is complete and pushed. BLK-077/079 name the next RTM-ladder continuation, if selected, as one exact local RTM drift-rejection execution sprint against `RTM-DRIFT-REJECTION-APPROVAL-DECISION-093-001`. The operator has now asked for the next logical sprint plan and execution, so BLK-SYSTEM-095 selects that single frontier.

## Governing Documents

- `docs/BLK-024_blk-system-development-roadmap.md` — Track H maturity vocabulary and separation of approvals.
- `docs/BLK-001_blk-system-master-architecture.md` — V-model separation and hashes as trace baton, not authority.
- `docs/BLK-077_blk-system-post-078-roadmap.md` — active post-078 roadmap selector and candidate frontier list.
- `docs/BLK-079_post-078-current-state-authority-index.md` — active current-state authority map.
- `docs/BLK-091_rtm-drift-rejection-authority-request.md` — request-only upstream package boundary.
- `docs/BLK-093_rtm-drift-rejection-approval-decision-capture.md` — exact approval-decision package to consume.
- `docs/BLK-094_post-093-roadmap-rtm-ladder-alignment.md` — local pilot ladder alignment boundary.

## Tasks

### Task 000 — Plan and scope

- Publish this plan.
- Record `docs/outcomes/BLK-SYSTEM-095_task-000-outcome.md`.
- No fixture execution yet.

### Task 001 — RED tests for exact local execution

- Add focused tests that initially fail because `python/exact_local_rtm_drift_rejection_execution.py` does not exist.
- Gate exact consumption of the BLK-SYSTEM-093 package:
  - `RTM-DRIFT-REJECTION-APPROVAL-DECISION-093-001`;
  - `APPROVAL-BLK-SYSTEM-091-RTM-DRIFT-REJECTION-001`;
  - `RUN-BLK-SYSTEM-091-RTM-DRIFT-REJECTION-001`.
- Add negative tests for forged approval packages, consumed/stale/replayed run IDs, approval-window mismatch, side-effect flags, exact-set drift, nested ledger pollution, and authority-laundering text.

### Task 002 — GREEN exact local execution fixture

- Implement `python/exact_local_rtm_drift_rejection_execution.py` minimally to satisfy Task 001.
- Emit deterministic local evidence:
  - status `LOCAL_RTM_DRIFT_REJECTION_EXECUTED_FOR_EXACT_BLK093_APPROVAL`;
  - output marker `PILOT_LOCAL_RTM_DRIFT_REJECTION_RECORDED_NOT_AUTHORITATIVE`;
  - hash-bound local drift-rejection record;
  - all adjacent side-effect flags false.
- Defensively deep-copy nested hash-bound inputs before hashing/returning packages.

### Task 003 — Doctrine/current-state alignment

- Add `docs/BLK-095_exact-local-rtm-drift-rejection-execution.md`.
- Update `docs/BLK-077_blk-system-post-078-roadmap.md` and `docs/BLK-079_post-078-current-state-authority-index.md` so BLK-SYSTEM-095 is recorded as local evidence only.
- Add a BLK-095 current-state surface in `python/blk_current_state_authority_index.py` and corresponding tests.
- Add active-doctrine gates for BLK-095 markers and stale post-094 wording.

### Task 004 — Hostile review and remediation

- Hostile-review the BLK-095 fixture, docs, current-state index, and tests against BLK-001, BLK-077, BLK-079, and BLK-094.
- Record `docs/reviews/BLK-SYSTEM-095_hostile-review.md`.
- Remediate blockers with tests/docs before closeout.

### Task 005 — Verification and closeout

- Run focused tests.
- Run full Python unittest discovery.
- Run Go tests/vet and `git diff --check`.
- Record task outcomes and `docs/outcomes/BLK-SYSTEM-095_sprint-closeout.md`.
- Exact-path stage, commit, push, and verify remote alignment.

## Acceptance Criteria

- The exact BLK-SYSTEM-093 approval-decision package is consumed by one local fixture only.
- `RUN-BLK-SYSTEM-091-RTM-DRIFT-REJECTION-001` is consumed exactly inside local evidence; no reusable runtime authority follows.
- The output is marked `PILOT_LOCAL_RTM_DRIFT_REJECTION_RECORDED_NOT_AUTHORITATIVE`.
- No authoritative drift decision, runtime `blk-link` trace closure, active-vault hash comparison, protected-body read/hash, external ledger mutation, signer/storage/rollback effect, target/source/Git mutation, BEB/BEO execution, BLK-pipe/BLK-test/Codex runtime, tooling, or production isolation claim is created.
- BLK-077, BLK-079, executable current-state index, and active doctrine gates agree after execution.
- Hostile review passes after any remediation.
