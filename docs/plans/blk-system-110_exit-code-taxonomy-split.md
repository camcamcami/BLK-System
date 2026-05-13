# BLK-SYSTEM-110 — Exit-Code Taxonomy Split Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md`, BLK-003, BLK-004, BLK-006, BLK-077, BLK-079, and the post-103 hostile review.

**Goal:** Close HR-009 by giving invalid payload failures a distinct POSIX route from syntax/validation gate failures while preserving Exit 3 for protected BLK-req and unauthorized mutation violations.
**BLK-024 track:** Track C — BLK-pipe blast shield and forge; Track I — Operator UX, observability, and escalation / maturity L1 deterministic local hardening.
**Architecture:** BLK-003 routes validation failures to Exit 2 and protected/unauthorized mutation failures to Exit 3. Invalid payload is a different failure class and must not share the syntax/validation route in code, adapter defaults, or operator-facing doctrine.
**Tech Stack:** Go exit-code constants/tests, Python adapter routing/tests, BLK-003/BLK-031 vocabulary docs as needed, Markdown plan/review/outcome docs.
**Authority boundary:** Local taxonomy and diagnostics hardening only; no target-repo BLK-pipe dispatch, no BLK-test runtime execution, no BEO publication, no RTM generation or drift rejection, no protected-body reads, no production `blk-link`, no signer/storage/ledger/rollback authority, no package/network/model/browser/cyber tooling, and no source/Git mutation outside exact BLK-System sprint files.

## Preflight State

```text
date: 2026-05-14T09:18:56+10:00
git: main at e524558 fix: require validation for execute payloads
working tree: clean before BLK-SYSTEM-109/110/111 plan edits
```

## Source Finding

From `docs/reviews/BLK-SYSTEM_post-103_all-codebase-hostile-review-and-completion-roadmap.md`:

- HR-009: `ExitInvalidPayload` shares POSIX Exit 2 with `ExitValidationFailed`, and Python adapter routing permits both `INVALID_PAYLOAD` and `SYNTAX_GATE_FAILED` for code 2.

## Tasks

0. Publish this plan and task-000 outcome lineage.
1. Add RED Go tests proving `ExitInvalidPayload` and `ExitValidationFailed` are distinct and that invalid payload reports route to the invalid-payload code.
2. Add RED Python adapter tests proving code 8 defaults to `INVALID_PAYLOAD`, code 2 defaults to `SYNTAX_GATE_FAILED`, and cross-status laundering is rejected.
3. Patch Go exit constants/routing and report tests.
4. Patch Python adapter status maps and tests.
5. Patch BLK-003/BLK-031 operator-facing wording where invalid payload/syntax validation routing appears.
6. Run focused Go/Python tests, full Go/Python verification, doctrine gates, `gofmt`, and `git diff --check`.
7. Publish hostile review and sprint closeout with explicit no-authority language.

## Required Markers

```text
BLK_SYSTEM_110_EXIT_CODE_TAXONOMY_SPLIT
INVALID_PAYLOAD_EXIT_CODE_8
SYNTAX_VALIDATION_FAILURE_REMAINS_EXIT_CODE_2
PROTECTED_ALLOWLIST_VIOLATIONS_REMAIN_EXIT_CODE_3
```
