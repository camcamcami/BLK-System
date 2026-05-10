# BLK-SYSTEM-067 — Kuronode Ignored-Artifact Cleanup Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `systematic-debugging` while executing. This plan follows BLK-024/BLK-059 maturity vocabulary and BLK-004/BLK-071 exact BLK-pipe worktree-sterility constraints.

**Goal:** Execute the user's explicit `Cleanup ignored artifacts` instruction by removing ignored Kuronode worktree artifacts that blocked BLK-pipe in BLK-SYSTEM-066.
**BLK-024 track:** Track C — BLK-pipe blast shield and forge; Track A — doctrine/review gates; maturity level L4 target-worktree sanitation operation, no source patch.
**Architecture:** Kuronode remains the target repository. BLK-System records the cleanup authority and evidence. Cleanup is limited to `git clean -fdX` ignored artifacts reported by Git; it does not authorize untracked non-ignored deletion, source mutation, BLK-pipe retry, package-manager restoration, or remote push.
**Tech Stack:** Markdown outcomes, Git status/clean dry-run and execution, no package manager, no Electron/smoke runtime.
**Authority boundary:** Cleanup of ignored Kuronode artifacts only. No BLK-pipe retry, no source patch, no Codex, no BLK-test MCP, no TypeScript/package-manager execution, no BEO/CEO publication, no RTM, no protected reads, no Kuronode push.

---

## 1. Current Known State

Captured before this plan:

```text
Date: 2026-05-11T09:02:42+10:00
BLK-System HEAD: ee6d93d feat: gate ceb009 fresh target patch attempt
Kuronode HEAD: 70b6062b92cf61c12bf190f92dc6b45ea4dcd438
Kuronode origin/main: 70b6062b92cf61c12bf190f92dc6b45ea4dcd438
Kuronode tracked dirty count: 0
Kuronode untracked non-ignored count: 0
Kuronode ignored count: 62767
```

Git dry-run for ignored cleanup (`git clean -ndX`) reported exactly these top-level removals:

```text
Would remove .kuronode-packets/
Would remove executionpipe/node_modules/
Would remove executionpipe/package-lock.json
Would remove mcp-server/dist/
Would remove mcp-server/node_modules/
Would remove node_modules/
Would remove packages/core/dist/
Would remove packages/core/node_modules/
Would remove packages/electron/dist/
Would remove packages/electron/node_modules/
Would remove packages/kuronode-graph/dist/
Would remove packages/kuronode-graph/node_modules/
```

---

## 2. Tasks

### Task 000 — Publish plan

Record the plan and task-000 outcome in BLK-System.

### Task 001 — Execute ignored-artifact cleanup

Run exactly:

```text
git clean -fdX
```

from `/home/dad/code/Kuronode-v1`, after verifying the dry-run shape above and target SHA. Capture the raw cleanup output and post-clean status summary.

### Task 002 — Verify no source mutation

Verify:

```text
git status --short --branch
git status --porcelain=v1 --untracked-files=all --ignored
git rev-parse HEAD
git ls-remote origin refs/heads/main
git diff -- scripts/smoke_test.ts
git diff --cached -- scripts/smoke_test.ts
```

### Task 003 — Closeout

Write outcome and hostile-review docs, run BLK-System markdown/diff checks, commit, and push BLK-System docs. Do not retry BLK-pipe in this sprint.

---

## 3. Stop Conditions

Stop before cleanup if:

1. Kuronode local HEAD or origin/main differs from `70b6062b92cf61c12bf190f92dc6b45ea4dcd438`;
2. tracked source files are dirty;
3. non-ignored untracked files appear;
4. the cleanup candidate set expands beyond ignored Git artifacts;
5. cleanup would require package-manager commands, source edits, BLK-pipe invocation, protected-path reads, or remote push.

---

## 4. Expected Success State

```text
KURONODE_IGNORED_ARTIFACT_CLEANUP_COMPLETE_PATCH_NOT_EXECUTED
```

This state means the Kuronode worktree has been sanitized for ignored artifacts. It does not authorize a BLK-pipe retry or source patch without a fresh explicit run authority.
