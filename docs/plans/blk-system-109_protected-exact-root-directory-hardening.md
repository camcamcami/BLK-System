# BLK-SYSTEM-109 — Protected Exact Root/Directory Hardening Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md`, BLK-003, BLK-004, BLK-006, BLK-077, BLK-079, and the post-103 hostile review.

**Goal:** Close HR-007 and HR-008 by rejecting protected BLK-req exact roots, descendants, and directory allowlist/source-scope entries before engine/runtime side effects.
**BLK-024 track:** Track C — BLK-pipe blast shield and forge; Track E — Python adapter/policy layer; Track F — BLK-test production-readiness ladder; Track J — Security, sandbox, and capability hardening / maturity L1 deterministic local hardening.
**Architecture:** BLK-006 requires protected BLK-req vault access violations to abort before tactical spawn. Go `blk-pipe` remains final mutation enforcement authority, and Python BLK-test runtime helpers remain bounded evidence-only guards. This sprint closes exact-root/directory classification gaps without authorizing new runtime work.
**Tech Stack:** Go contracts/pipe tests, Python protected-path helper/tests, Markdown plan/review/outcome docs.
**Authority boundary:** Local BLK-System hardening only; no target-repo BLK-pipe dispatch, no BLK-test runtime execution, no BEO publication, no RTM generation or drift rejection, no protected-body reads, no production `blk-link`, no signer/storage/ledger/rollback authority, no package/network/model/browser/cyber tooling, and no source/Git mutation outside exact BLK-System sprint files.

## Preflight State

```text
date: 2026-05-14T09:18:56+10:00
git: main at e524558 fix: require validation for execute payloads
working tree: clean before BLK-SYSTEM-109/110/111 plan edits
```

## Source Findings

From `docs/reviews/BLK-SYSTEM_post-103_all-codebase-hostile-review-and-completion-roadmap.md`:

- HR-007: Protected exact directory roots can slip through Go allowlist classification, and tracked directories can be accepted before engine execution.
- HR-008: Python BLK-test runtime source-scope guards accept exact protected roots for `docs/active`, `docs/requirements`, and `docs/use_cases`.

## Tasks

0. Publish this plan and task-000 outcome lineage.
1. Add RED Go tests proving `docs/active`, `docs/requirements`, and `docs/use_cases` exact allowlist entries are rejected as protected and tracked directory allowlist entries are rejected before engine side effects.
2. Add RED Python tests proving exact protected source roots and descendants are rejected for all four affected BLK-test runtime helpers.
3. Patch Go protected path predicates and tracked-file classification so exact roots and directories fail before engine execution.
4. Add a shared Python protected-source-scope predicate and wire affected runtime helpers through it.
5. Run focused Go/Python tests, full Go/Python verification, doctrine gates, `gofmt`, and `git diff --check`.
6. Publish hostile review and sprint closeout with explicit no-authority language.

## Required Markers

```text
BLK_SYSTEM_109_PROTECTED_EXACT_ROOT_DIRECTORY_HARDENED
PROTECTED_DOCS_EXACT_ROOTS_REJECTED
GO_ALLOWLIST_REQUIRES_EXACT_FILES_BEFORE_ENGINE
PYTHON_BLK_TEST_SOURCE_SCOPE_REJECTS_PROTECTED_ROOTS
```
