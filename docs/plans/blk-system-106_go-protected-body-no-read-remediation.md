# BLK-SYSTEM-106 — Go Protected-Body No-Read Remediation Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md`, BLK-001, BLK-004, BLK-005, BLK-006, and the post-103 reconciliation docs.

**Goal:** Remediate the Go `blk-pipe` physical worktree snapshot so it does not directly read protected BLK-req body files while preserving allowlist enforcement and cleanup evidence.
**BLK-024 track:** Track C — BLK-pipe blast shield and forge; Track J — Security, sandbox, and capability hardening / maturity L1 local deterministic implementation hardening.
**Architecture:** BLK-pipe may observe metadata and Git state to enforce mutation boundaries, but must not read/copy/parse/hash protected BLK-req body bytes under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`. BLK-006 protected-vault hard-deny and BLK-105 `NO_PROTECTED_BODY_READS_FOR_TRACE_CLOSURE` control this sprint.
**Tech Stack:** Go (`internal/pipe/run.go`, `internal/pipe/run_test.go`), Markdown plan/review/outcome docs.
**Authority boundary:** Local BLK-System implementation/test hardening only; no BLK-pipe runtime dispatch against Kuronode/target repositories, no BLK-test runtime, no BEO publication, no RTM generation or drift rejection, no protected-body reads, no target/source/Git mutation outside this BLK-System commit, no production `blk-link`, and no signer/storage/ledger/rollback authority.

## Preflight State

```text
date: 2026-05-14T08:38:30+10:00
git: main at acc7551 docs: reconcile root doctrine post-103 state
working tree: clean before BLK-SYSTEM-106 plan edits
```

## Source Finding

From `docs/reviews/BLK-SYSTEM_post-103_all-codebase-hostile-review-and-completion-roadmap.md`:

- HR-001: Go `blk-pipe` physical snapshots could read protected BLK-req body files as part of worktree snapshots. This violates the no-protected-body-read doctrine and must be remediated before the next implementation frontier.

## Tasks

0. Publish this plan and task-000 outcome lineage.
1. Add a RED Go regression proving unreadable protected BLK-req body files do not block safe allowed work; under current code this fails because the snapshot directly reads protected bodies.
2. Patch `internal/pipe/run.go` so physical worktree snapshots use metadata-only opaque entries for protected BLK-req body paths.
3. Run focused Go tests, full Go tests, Go vet, Python doctrine gates, and diff checks.
4. Publish hostile review and closeout, commit exact paths, and push.

## Required Markers

```text
BLK_SYSTEM_106_GO_PROTECTED_BODY_NO_READ_REMEDIATED
GO_PHYSICAL_WORKTREE_PROTECTED_BODY_METADATA_ONLY
NO_PROTECTED_BODY_READS_FOR_TRACE_CLOSURE
```
