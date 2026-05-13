# BLK-SYSTEM-111 — Doctrine Gate Coverage and Runbook Vocabulary Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md`, BLK-001 through BLK-006, BLK-031, BLK-077, BLK-079, and the post-103 hostile review.

**Goal:** Close HR-010, HR-011, and HR-012 by strengthening active doctrine gates, propagating the BLK-test functional-module warning, and updating operator runbook vocabulary for post-100/post-103 non-authoritative evidence states.
**BLK-024 track:** Track A — Doctrine, alignment, and review gates; Track I — Operator UX, observability, and escalation / maturity L0/L1 doctrine and deterministic gate hardening.
**Architecture:** Documentation is authority-bearing. BLK-077/079 must not leave stale post-103 frontier wording that future agents can quote as current, BLK-test must remain clearly distinct from the repository's normal Go/Python test suites, and BLK-031 should expose post-100/post-103 record-only evidence states without granting publication or `blk-link` authority.
**Tech Stack:** Python doctrine-gate tests, BLK-077/079/031 documentation, Markdown plan/review/outcome docs.
**Authority boundary:** Doctrine/runbook hardening only; no target-repo BLK-pipe dispatch, no BLK-test runtime execution, no BEO publication, no RTM generation or drift rejection, no protected-body reads, no production `blk-link`, no signer/storage/ledger/rollback authority, no package/network/model/browser/cyber tooling, and no source/Git mutation outside exact BLK-System sprint files.

## Preflight State

```text
date: 2026-05-14T09:18:56+10:00
git: main at e524558 fix: require validation for execute payloads
working tree: clean before BLK-SYSTEM-109/110/111 plan edits
```

## Source Findings

From `docs/reviews/BLK-SYSTEM_post-103_all-codebase-hostile-review-and-completion-roadmap.md`:

- HR-010: Doctrine gates pass while stale current-state prose can remain allowed.
- HR-011: The exact warning that BLK-test is a BLK-System functional module, not the BLK-System test suite, is under-propagated.
- HR-012: BLK-031 operator runbook vocabulary lags post-100/post-103 evidence states.

## Tasks

0. Publish this plan and task-000 outcome lineage.
1. Add RED doctrine gates proving BLK-077/079 carry post-103 frontier markers, do not carry stale active next-frontier wording after 109/110 closure, and keep BEO/RTM post-100/103 distinctions.
2. Add RED gates pinning the exact BLK-test functional-module warning on operator-facing current-state surfaces.
3. Add RED gates pinning BLK-031 vocabulary for `PUBLISHED_EXTERNAL_BEO_RECORD` and `PILOT_LOCAL_RTM_TRACE_CLOSURE_RECORDED_NOT_AUTHORITATIVE` while preserving signer/storage/ledger and production `blk-link` denials.
4. Patch BLK-077/079 and BLK-031 minimally to satisfy the gates.
5. Run focused doctrine tests, full Go/Python verification, and `git diff --check`.
6. Publish hostile review and sprint closeout with explicit no-authority language.

## Required Markers

```text
BLK_SYSTEM_111_DOCTRINE_GATE_COVERAGE_RUNBOOK_VOCABULARY
POST_103_FRONTIER_GATES_PINNED
BLK_TEST_FUNCTIONAL_MODULE_NOT_BLK_SYSTEM_TEST_SUITE_PINNED
RUNBOOK_POST_100_103_RECORD_ONLY_STATES_PINNED
```
