# BLK-SYSTEM-105 — Root Doctrine Post-103 Reconciliation Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable.

**Goal:** Patch root doctrine docs so BLK-001/003/005/006 distinguish post-BLK-SYSTEM-100 record-only external BEO evidence and post-BLK-SYSTEM-103 local non-authoritative trace-closure evidence from still-denied production authority.
**BLK-024 track:** Track A — Doctrine, alignment, and review gates / maturity L0/L1 documentation and doctrine-gate.
**Architecture:** BLK-SYSTEM-104 reconciled BLK-077/079 and current-state code. BLK-SYSTEM-105 applies the same post-103 boundary to root architecture/orchestration/requirements docs without granting runtime authority.
**Tech Stack:** Markdown doctrine docs and Python unittest doctrine gates.
**Authority boundary:** Doctrine/test cleanup only; no BLK-pipe runtime execution, BLK-test runtime, BEO publication, RTM generation, drift rejection, protected-body reads, target/source/Git mutation outside BLK-System documentation/test commits, Codex execution, tooling authority, signer/storage/ledger side effects, or production-isolation claim.

## Preflight State

```text
date: 2026-05-14T08:24:25+10:00
git: main at 4b4fc11 docs: reconcile post-103 roadmap state
working tree: clean before plan/test edits
```

## Source Findings

From `docs/reviews/BLK-SYSTEM_post-103_all-codebase-hostile-review-and-completion-roadmap.md`:

- HR-004: active root doctrine/current-state docs are stale and contradictory after BLK-SYSTEM-100/103.
- HR-010: doctrine tests pass while stale current-state prose remains allowed.

## Tasks

0. Publish this plan and task-000 outcome lineage.
1. Add RED doctrine gates for root post-103 reconciliation markers and stale root-doctrine wording.
2. Patch `docs/BLK-001_blk-system-master-architecture.md`, `docs/BLK-003_blk-pipe-blk-test-orchestration.md`, `docs/BLK-005_blk-req-specification.md`, and `docs/BLK-006_blk-req-implementation-brief.md`.
3. Run focused/full verification and hostile self-review.
4. Publish closeout and exact-path commit.

## Required Markers

```text
BLK_SYSTEM_105_ROOT_DOCTRINE_POST_103_RECONCILED
POST_103_ROOT_DOCTRINE_RECONCILIATION_BOUNDARY
BEO_PUBLICATION_RECORD_ONLY_SIGNER_STORAGE_LEDGER_DISABLED
RTM_TRACE_CLOSURE_LOCAL_RECORD_ONLY_PRODUCTION_BLK_LINK_DISABLED
NO_PROTECTED_BODY_READS_FOR_TRACE_CLOSURE
```
