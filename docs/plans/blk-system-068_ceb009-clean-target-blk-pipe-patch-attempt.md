# BLK-SYSTEM-068 — CEB_009 Clean-Target BLK-pipe Patch Attempt Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. This plan follows BLK-004, BLK-071, BLK-SYSTEM-066/067 closeouts, and the exact-target BLK-pipe worktree-sterility pattern.

**Goal:** Execute the user's fresh approval for one exact BLK-pipe-mediated CEB_009 patch attempt after ignored-artifact cleanup.
**BLK-024 track:** Track C — BLK-pipe blast shield and forge; Track A — doctrine/review gates; maturity level L4 bounded real-repo source mutation attempt.
**Architecture:** BLK-System records approval, builds an exact payload, and audits the result. Go `blk-pipe` is the only authorized source-mutation mechanism. Kuronode remains the target repo and no remote push is authorized.
**Tech Stack:** Markdown outcomes, JSON payload/report, Go `blk-pipe`, Python engine payload that edits only `scripts/smoke_test.ts`.
**Authority boundary:** One exact BLK-pipe-mediated patch attempt against Kuronode SHA `70b6062b92cf61c12bf190f92dc6b45ea4dcd438`; allowed mutation path `scripts/smoke_test.ts` only; no Codex, no BLK-test MCP, no Electron/smoke runtime, no TypeScript/package-manager tooling, no BEO/CEO publication, no RTM, no protected reads, and no Kuronode remote push.

---

## 1. Current Known State

Captured before this plan:

```text
Date: 2026-05-11T09:12:51+10:00
BLK-System HEAD: 40b9bad docs: close out blk-system 067 ignored cleanup
BLK-System origin/main: 40b9bad65392a5367d059898d7ae6590db177657
Kuronode local HEAD: 70b6062b92cf61c12bf190f92dc6b45ea4dcd438
Kuronode origin/main: 70b6062b92cf61c12bf190f92dc6b45ea4dcd438
Kuronode worktree status rows with ignored/untracked included: 0
scripts/smoke_test.ts unstaged diff: empty
scripts/smoke_test.ts staged diff: empty
```

User approval text:

```text
I approve BLK-SYSTEM-068: one exact BLK-pipe-mediated CEB_009 patch attempt against Kuronode SHA

70b6062b92cf61c12bf190f92dc6b45ea4dcd438, modifying only scripts/smoke_test.ts, with no Codex, no BLK-test MCP, no Electron/smoke runtime, no TypeScript/package-manager tooling, no BEO/CEO publication, no RTM, and no Kuronode remote push.
```

---

## 2. Exact Target and Allowlist

```text
repo: github:camcamcami/Kuronode-v1
workspace: /home/dad/code/Kuronode-v1
branch: main
approved target head: 70b6062b92cf61c12bf190f92dc6b45ea4dcd438
allowed_modified_files: [scripts/smoke_test.ts]
allowed_new_files: []
```

---

## 3. Patch Intent

Only `scripts/smoke_test.ts` may be modified, to:

1. remove `@ts-ignore` and unsafe `any` projection-result access;
2. add typed preload API and projection-result guards;
3. fail on timeout sentinel before PASS logging;
4. fail on missing AST payload before PASS logging;
5. preserve listener unsubscribe and Electron close cleanup.

---

## 4. Tasks

### Task 000 — Publish plan

Write this plan and task-000 outcome, verify Markdown, commit, and push.

### Task 001 — Build fresh approval record and payload

Create BLK-SYSTEM-068 approval record and BLK-pipe payload with a fresh run ID and exact allowlist.

### Task 002 — Execute one BLK-pipe attempt

1. Verify local and remote target SHA match the approved SHA.
2. Verify worktree sterility using `git status --porcelain=v1 --untracked-files=all --ignored`.
3. Invoke `go run ./cmd/blk-pipe --payload <payload>` exactly once.
4. Capture the raw report.

### Task 003 — Verify and close out

Verify Kuronode commit/diff state, write hostile review/closeout, run BLK-System verification, commit, and push BLK-System artifacts.

---

## 5. Stop Conditions

Stop before BLK-pipe if:

1. local or remote Kuronode SHA differs from the approved target;
2. worktree sterility check returns any row;
3. payload allowlist expands beyond `scripts/smoke_test.ts`;
4. any step requires Codex, BLK-test MCP, Electron/smoke runtime, TypeScript/package-manager tooling, protected reads, BEO/CEO publication, RTM, or Kuronode push.

---

## 6. Expected Success State

```text
KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_BLK_PIPE_COMMITTED_NOT_PUSHED
```

This means only a local Kuronode commit exists. It is not remote publication, not runtime validation, not BEO/CEO publication, and not RTM closure.
