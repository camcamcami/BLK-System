# BLK-SYSTEM-094 — Post-093 Roadmap / RTM-Ladder Alignment Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `blk-system-authority-gated-sprints` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable.

**Goal:** Clean up and align the active post-BLK-SYSTEM-093 roadmap/current-state surfaces so the local non-authoritative BEO/RTM pilot ladder cannot be confused with runtime `blk-link` trace closure or the next execution frontier.

**BLK-024 track:** Track A — Doctrine, alignment, and review gates; Track H — BLK-link offline RTM ledger. Maturity level L0/L1 doctrine/current-state gate only.

**Architecture:** BLK-001 keeps `blk-req`, planning, `blk-pipe`, `blk-test`, BEO publication, and `blk-link` trace closure separate. BLK-SYSTEM-087 through BLK-SYSTEM-093 built a local-only pilot/request/approval ladder, but hostile review found stale roadmap wording that could blur local pilot evidence with real runtime RTM/blk-link authority. This sprint resolves that ambiguity before any next execution frontier.

**Tech Stack:** Markdown doctrine/roadmap docs plus Python current-state/doctrine tests only.

**Authority boundary:** Consolidation/remediation only. This sprint grants no runtime RTM generation, no RTM drift-rejection execution, no drift decision, no protected-body reads/hashing, no active-vault comparison, no external BEO publication, no signer/storage/ledger/rollback effects, no target/source/Git mutation by fixtures, no BEB dispatch, no BEO closeout execution, no BLK-pipe/BLK-test/Codex runtime, no package/network/model/browser/cyber tooling, and no production-isolation claim.

## Current Known State

Captured during preflight:

```text
git status: ## main...origin/main
HEAD: ba6c4af feat: capture blk 093 drift rejection approval
Date: 2026-05-13T08:39:40+10:00
```

BLK-SYSTEM-093 is complete and pushed. The next candidate RTM-ladder movement is not automatic; hostile review recommended cleanup/alignment before any exact local drift-rejection execution sprint.

## Governing Documents

- `docs/BLK-024_blk-system-development-roadmap.md` — historical maturity vocabulary; Track A and H principles.
- `docs/BLK-001_blk-system-master-architecture.md` — V-model component separation and hashes as trace baton, not authority.
- `docs/BLK-077_blk-system-post-078-roadmap.md` — active roadmap selector.
- `docs/BLK-079_post-078-current-state-authority-index.md` — active current-state index.
- `docs/BLK-087_exact-beo-publication-pilot-execution.md` through `docs/BLK-093_rtm-drift-rejection-approval-decision-capture.md` — local pilot/request/approval ladder artifacts to clarify, not execute.

## Hostile-Review Findings Being Remediated

1. Local non-authoritative RTM pilot ladder needs explicit vocabulary distinct from real runtime `blk-link` closure.
2. Do not execute the next RTM drift-rejection rung until stale Workstream E / current-state wording is reconciled.
3. Future authority rungs should remain independently auditable; BLK-SYSTEM-089/090/091 were separately documented but landed in one combined commit.
4. Approval captured is not execution selected. Post-093 docs must not say approval has not occurred for the BLK-091 package.
5. Fixture complexity is mostly justified, but roadmap/index docs should avoid adding another generic preparatory rung unless a specific stale-doc/test/review failure exists.

## Tasks

### Task 000 — Plan and scope

- Publish this plan.
- Record `docs/outcomes/BLK-SYSTEM-094_task-000-outcome.md`.
- No implementation or runtime authority.

### Task 001 — RED tests for post-093 cleanup requirements

- Add/patch focused tests that initially fail because BLK-094 docs/surfaces are absent.
- Gate markers for:
  - local non-authoritative BEO/RTM pilot ladder not runtime `blk-link` closure;
  - actual authoritative BEO publication remains prerequisite for real runtime trace closure;
  - BLK-SYSTEM-093 approval-decision capture is not execution selection;
  - future authority rungs must be independently auditable;
  - stale post-092/post-093 wording is removed or explicitly historical;
  - BLK-094 current-state surface denies adjacent authorities.

### Task 002 — GREEN doctrine/current-state alignment

- Add `docs/BLK-094_post-093-roadmap-rtm-ladder-alignment.md`.
- Patch `docs/BLK-077_blk-system-post-078-roadmap.md` and `docs/BLK-079_post-078-current-state-authority-index.md`.
- Patch `python/blk_current_state_authority_index.py` and tests with a BLK-094 surface.
- Preserve historical markers where required but make current frontier wording unambiguous.

### Task 003 — Hostile review and remediation

- Hostile-review the BLK-094 changes against BLK-001, BLK-077, BLK-079, and the post-093 findings.
- Record `docs/reviews/BLK-SYSTEM-094_hostile-review.md`.
- Remediate blockers with tests and docs before closeout.

### Task 004 — Verification and closeout

- Run focused tests.
- Run full Python unittest suite.
- Run Go tests/vet and `git diff --check`.
- Record task outcomes and `docs/outcomes/BLK-SYSTEM-094_sprint-closeout.md`.
- Exact-path stage, commit, push, and verify remote alignment.

## Acceptance Criteria

- BLK-077 and BLK-079 clearly distinguish local non-authoritative pilot ladders from real runtime `blk-link` trace closure.
- BLK-077 and BLK-079 no longer present BLK-SYSTEM-093 approval capture as missing or as execution authority.
- BLK-094 is present in docs, current-state index, and active doctrine gates.
- Current candidate frontiers after BLK-094 are explicit: one exact local RTM drift-rejection execution sprint if separately selected, bounded BLK-test evidence refresh, Codex L3 smoke, or bounded remediation/consolidation.
- Future authority rungs are required to be independently auditable when practical.
- No adjacent authority is granted.
