# BLK-SYSTEM-107 — Mandatory Validation Required Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md`, BLK-003, BLK-004, and BLK-006.

**Goal:** Make validation mandatory for every execute payload by rejecting payloads that provide neither non-empty `validation_profiles` nor non-empty `validation_commands` at both the Go authority layer and Python adapter preflight layer.
**BLK-024 track:** Track D — Validation command profile tightening; Track C — BLK-pipe blast shield and forge / maturity L1 deterministic local enforcement.
**Architecture:** BLK-003 already requires global workspace syntax validation in payloads. BLK-004 makes Go `blk-pipe` the enforcement authority while Python adapter checks remain fail-fast convenience only. BLK-SYSTEM-107 closes the bypass where an execute payload could omit validation and still reach engine/commit flow.
**Tech Stack:** Go contracts/pipe tests, Python adapter tests, Markdown plan/review/outcome docs.
**Authority boundary:** Local BLK-System validation hardening only; no BLK-pipe runtime dispatch against Kuronode/target repositories, no BLK-test runtime, no BEO publication, no RTM generation/drift rejection, no protected-body reads, no target/source/Git mutation outside this BLK-System commit, no production `blk-link`, and no signer/storage/ledger/rollback authority.

## Preflight State

```text
date: 2026-05-14T08:46:19+10:00
git: main at 9def74a fix: avoid protected body reads in worktree snapshots
working tree: clean before BLK-SYSTEM-107 plan edits
```

## Source Finding

From `docs/reviews/BLK-SYSTEM_post-103_all-codebase-hostile-review-and-completion-roadmap.md`:

- HR-003: Mandatory validation gate is still incomplete if execute payloads can omit validation and continue to engine/commit flow.

## Tasks

0. Publish this plan and task-000 outcome lineage.
1. Add RED Go tests proving missing and explicitly empty validation are rejected before engine side effects.
2. Add RED Python adapter tests proving missing and explicitly empty validation are rejected before invoking `blk-pipe`.
3. Patch Go contracts and Python adapter validation minimally.
4. Run focused Go/Python tests, full Go/Python verification, Go vet, doctrine gates, and diff checks.
5. Publish hostile review and closeout, commit exact paths, and push.

## Required Markers

```text
BLK_SYSTEM_107_MANDATORY_VALIDATION_REQUIRED
EXECUTE_PAYLOAD_REQUIRES_VALIDATION_PROFILE_OR_COMMAND
VALIDATION_REQUIRED_BEFORE_ENGINE_SIDE_EFFECTS
PYTHON_ADAPTER_VALIDATION_REQUIRED_FAIL_FAST_ONLY_GO_REMAINS_AUTHORITY
```
