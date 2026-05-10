# BLK-SYSTEM-066 — CEB_009 Fresh-Target Patch Execution Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, `test-driven-development`, and `repo-mcp-closeout-via-stdio` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, `docs/BLK-059_blk-system-post-058-roadmap.md` for current sequencing, BLK-001 through BLK-006 for V-model authority boundaries, and BLK-070 for exact-target drift handling.

**Goal:** Capture the user's fresh approval for the current Kuronode `origin/main` target and perform one exact BLK-pipe-mediated CEB_009 patch execution against that target.
**BLK-024 track:** Track C — BLK-pipe blast shield and forge; Track A — doctrine/review gates; maturity level L4 bounded real-repo source mutation attempt.
**Architecture:** BLK-System remains the planner/auditor. Go `blk-pipe` remains the only patch commit enforcement layer. A local synchronization step may align the Kuronode checkout to the approved current target SHA before BLK-pipe, but the only authorized source change is still constrained to `scripts/smoke_test.ts` through BLK-pipe allowlists.
**Tech Stack:** Markdown doctrine/outcomes, Python approval-capture fixture/tests, Go `blk-pipe`, Kuronode TypeScript target file `scripts/smoke_test.ts`.
**Authority boundary:** One exact BLK-pipe-mediated patch attempt against Kuronode `70b6062b92cf61c12bf190f92dc6b45ea4dcd438`; no live Codex, no BLK-test MCP, no Electron/smoke runtime, no TypeScript/package-manager tooling, no BEO/CEO publication, no RTM generation, no protected BLK-req reads, and no Kuronode remote push unless separately approved after review.

---

## 1. Current Known State

Captured before writing this plan:

```text
Date: 2026-05-11T08:39:29+10:00
BLK-System HEAD: 38f30df feat: capture ceb009 patch approval with drift gate
BLK-System origin/main: 38f30df4d1564a1d4137af5bc9bec9e58b913f20
Kuronode local HEAD: cb09d965c0407612c9ce8fc9cc58c5e62c82e1b2
Kuronode observed origin/main: 70b6062b92cf61c12bf190f92dc6b45ea4dcd438
```

The user then replied `I approve` immediately after the closeout stated that a fresh approval must explicitly target:

```text
70b6062b92cf61c12bf190f92dc6b45ea4dcd438
```

BLK-SYSTEM-066 treats that reply as approval for exactly this displayed current target SHA and nothing broader.

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

Kuronode local checkout may be reset to this exact approved SHA before BLK-pipe because local state is stale. This synchronization is not patch authority and must not create a source diff. If synchronization fails or lands on any other SHA, stop.

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

### Task 000 — Publish this plan

Write this plan and `docs/outcomes/BLK-SYSTEM-066_task-000-outcome.md`, verify exact paths, commit, and push.

### Task 001 — TDD fresh-target approval/payload gate

Add RED/GREEN tests and a fresh-target approval fixture that binds the current target SHA, rejects any other SHA, and emits one BLK-pipe payload for `scripts/smoke_test.ts` only.

### Task 002 — Boundary and doctrine gate

Create `docs/BLK-071_ceb009-fresh-target-patch-execution-boundary.md` and add a persistent active-doctrine gate denying adjacent authorities.

### Task 003 — Execute one exact BLK-pipe attempt

1. Verify Kuronode local workspace is clean.
2. Fetch `origin` and reset local `main` to `70b6062b92cf61c12bf190f92dc6b45ea4dcd438`.
3. Verify local HEAD and observed `origin/main` both equal the approved SHA.
4. Invoke `go run ./cmd/blk-pipe --payload <absolute payload path>` exactly once.
5. Capture the raw BLK-pipe JSON report.
6. Do not push Kuronode.

### Task 004 — Closeout and publication

1. Run Kuronode MCP closeout review if a patch commit exists.
2. Run BLK-System focused/full tests and Go verification.
3. Hostile-review the patch report and boundary.
4. Commit/push BLK-System outcome documents.
5. Leave Kuronode remote push for a separate explicit decision.

---

## 5. Stop Conditions

Stop before BLK-pipe if:

1. observed `origin/main` is not `70b6062b92cf61c12bf190f92dc6b45ea4dcd438`;
2. local reset does not land exactly on `70b6062b92cf61c12bf190f92dc6b45ea4dcd438`;
3. workspace is dirty before patch execution;
4. payload expands beyond `scripts/smoke_test.ts`;
5. payload attempts Codex, BLK-test MCP, Electron/smoke runtime, TypeScript/package-manager tooling, network/model/browser/cyber tooling, BEO/CEO publication, RTM, protected body reads, or remote push.

---

## 6. Expected Success State

```text
KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_BLK_PIPE_COMMITTED_NOT_PUSHED
```

This state means local Kuronode commit evidence exists. It does not mean remote push, CEO/BEO publication, BLK-test PASS, RTM generation, or production validation authority.
