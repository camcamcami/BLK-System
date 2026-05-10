# BLK-SYSTEM-065 — CEB_009 Patch Execution Approval Capture and BLK-pipe Run Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, `test-driven-development`, and `repo-mcp-closeout-via-stdio` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, `docs/BLK-059_blk-system-post-058-roadmap.md` for current sequencing, and BLK-001 through BLK-006 for V-model authority boundaries.

**Goal:** Capture the operator's explicit CEB_009 patch-execution approval and perform at most one exact BLK-pipe-mediated patch attempt against the approved Kuronode target if exact-target drift checks pass.
**BLK-024 track:** Track C — BLK-pipe blast shield and forge; Track A — doctrine/review gates; maturity level L4 bounded real-repo source mutation attempt.
**Architecture:** BLK-System remains the planner/auditor. Go `blk-pipe` remains the only mutation-and-commit enforcement layer for the Kuronode source change. Python approval-capture logic may validate evidence and build an execution payload, but it cannot replace BLK-pipe's allowlist, cleanup, validation, and commit gates.
**Tech Stack:** Markdown doctrine/outcomes, Python approval-capture fixture/tests, Go `blk-pipe`, Kuronode TypeScript target file `scripts/smoke_test.ts`.
**Authority boundary:** One exact CEB_009 patch execution attempt is approved by the operator only if target identity remains exact. No production BLK-test MCP, no live Codex, no Electron launch, no smoke-test run, no TypeScript/package-manager/tool-install execution, no authoritative BEO/CEO publication, no RTM generation, no protected BLK-req body reads, and no source mutation outside `scripts/smoke_test.ts`.

---

## 1. Current Known State

Captured before writing this plan:

```text
Date: 2026-05-11T08:18:17+10:00
BLK-System: ## main...origin/main
BLK-System HEAD: 83be315 feat: add ceb009 patch execution authority request
BLK-System origin/main: 83be31503cca8cc1b9ce07d7f7a8933bcd962acf
Kuronode local: ## main...origin/main
Kuronode local HEAD: cb09d965c0407612c9ce8fc9cc58c5e62c82e1b2
Kuronode origin/main observed by ls-remote: 70b6062b92cf61c12bf190f92dc6b45ea4dcd438
```

The operator explicitly granted authority in Discord:

```text
We should capture approval and perform one exact BLK-pipe-mediated patch execution in the same sprint. I explicitly grant that authority up front.
```

The prior BLK-SYSTEM-064 authority request targets Kuronode `main` at:

```text
cb09d965c0407612c9ce8fc9cc58c5e62c82e1b2
```

Because `origin/main` currently reports a different HEAD, this sprint must treat remote exact-target drift as a hard execution preflight condition. The sprint may capture the approval, but it must not execute BLK-pipe against a different target SHA unless a fresh approval names that SHA.

---

## 2. Governing Documents

- `docs/BLK-001_blk-system-master-architecture.md`: preserves separation between Hermes planning/audit, BLK-pipe mutation enforcement, BLK-test evidence, BEO publication, and RTM trace closure.
- `docs/BLK-002_blk-req-artifact-lifecycle.md`: preserves HITL authorization, staging, canonical hashing, and protected active-vault immutability.
- `docs/BLK-003_blk-pipe-blk-test-orchestration.md`: governs BLK-pipe invocation, exact payload boundaries, POSIX routing, hostile audit, and current disabled BLK-test/BEO/RTM boundaries.
- `docs/BLK-004_blk-pipe-v47-architecture-suite.md`: governs Go BLK-pipe as deterministic final authority for source mutation, allowlists, validation, cleanup, Git routing, and report evidence.
- `docs/BLK-005_blk-req-specification.md`: preserves trace-artifact binding and protected execution boundaries without granting drift authority.
- `docs/BLK-006_blk-req-implementation-brief.md`: preserves protected-vault hard-deny behavior and no protected body reads.
- `docs/BLK-069_ceb009-patch-execution-authority-request-boundary.md`: supplies the request-ready input state and future approval obligations.

---

## 3. Exact Target and Allowlist

Approved request target:

```text
repo: github:camcamcami/Kuronode-v1
workspace: /home/dad/code/Kuronode-v1
branch: main
target head: cb09d965c0407612c9ce8fc9cc58c5e62c82e1b2
allowed_modified_files: [scripts/smoke_test.ts]
allowed_new_files: []
```

Patch intent:

1. remove unsafe `@ts-ignore` / `any` result access from `scripts/smoke_test.ts`;
2. add a typed projection-result guard;
3. make timeout sentinel fail before PASS logging;
4. require string `streamId` and an AST payload before PASS;
5. preserve listener unsubscribe and Electron close cleanup.

---

## 4. Tasks

### Task 000 — Publish this plan

1. Write this plan and `docs/outcomes/BLK-SYSTEM-065_task-000-outcome.md`.
2. Verify Markdown fences and `git diff --check` on exact paths.
3. Commit and push exact paths to BLK-System `origin/main`.

### Task 001 — TDD approval-capture and execution-readiness gate

1. Add RED tests for a BLK-SYSTEM-065 approval-capture fixture.
2. Require exact BLK-SYSTEM-064 authority-request hash recomputation.
3. Capture operator approval ID, run ID, approval timestamp, expiry, target repo/path/branch/head, and allowlists.
4. Reject stale/mismatched local or remote target heads, expired approvals, replayed IDs, broadened allowlists, and adjacent-authority laundering.
5. Emit `READY_FOR_ONE_EXACT_BLK_PIPE_PATCH_ATTEMPT` only when exact-target checks pass; emit a blocked state when target drift is detected.

### Task 002 — Boundary and active doctrine gate

1. Create `docs/BLK-070_ceb009-patch-execution-approval-capture-and-run-boundary.md`.
2. Update `python/test_active_doctrine_review_gates.py` with persistent BLK-070 markers.
3. Preserve explicit non-authority for BLK-test MCP, Codex, Electron/smoke runtime, TypeScript/package-manager tooling, BEO/CEO publication, RTM, protected reads, and production isolation.

### Task 003 — One exact BLK-pipe-mediated patch attempt, only if target checks pass

1. Before invoking BLK-pipe, verify Kuronode local HEAD and observed `origin/main` exactly match the approved target head.
2. If target drift exists, write a BLOCKED outcome and do not invoke BLK-pipe.
3. If exact checks pass, build an absolute payload for `go run ./cmd/blk-pipe --payload <payload>` with:
   - `work_dir=/home/dad/code/Kuronode-v1`;
   - `target_branch=main`;
   - `allowed_modified_files=[scripts/smoke_test.ts]`;
   - `allowed_new_files=[]`;
   - no live Codex;
   - no Electron/smoke/TypeScript/package-manager validation;
   - validation limited to non-runtime diff hygiene.
4. Capture the BLK-pipe JSON report verbatim in a BLK-System outcome document.

### Task 004 — Hostile review, closeout, and publication

1. Hostile-review approval laundering, target-drift laundering, stale-head execution, BLK-pipe report interpretation, and adjacent-authority creep.
2. Run focused tests, full Python suite, Go tests/vet, Markdown fence checks, and `git diff --check`.
3. If Kuronode was patched, run Kuronode MCP closeout review via stdio before final closeout.
4. Commit and push BLK-System exact paths.
5. Do not push Kuronode unless separately authorized after reviewing the BLK-pipe commit and remote-head state.

---

## 5. Stop Conditions

Stop and do not invoke BLK-pipe if any of the following is true:

1. local Kuronode HEAD is not `cb09d965c0407612c9ce8fc9cc58c5e62c82e1b2`;
2. observed Kuronode `origin/main` is not `cb09d965c0407612c9ce8fc9cc58c5e62c82e1b2`;
3. workspace is dirty before BLK-pipe;
4. approval is expired, replayed, missing exact approval/run IDs, or missing the operator's explicit grant text;
5. allowlist includes anything except `scripts/smoke_test.ts` as a modified file and no new files;
6. payload attempts Codex, Electron, smoke runtime, TypeScript tooling, package-manager execution, network/model/browser/cyber tooling, BEO/CEO publication, RTM, protected body reads, or production isolation claims.

---

## 6. Expected Statuses

If exact-target checks pass and BLK-pipe succeeds:

```text
KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_APPROVED_AND_BLK_PIPE_COMMITTED
```

If target drift is detected before BLK-pipe:

```text
KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_BLOCKED_TARGET_DRIFT_NOT_EXECUTED
```

The current preflight already indicates the remote-drift branch is likely unless a fresh approval targets `70b6062b92cf61c12bf190f92dc6b45ea4dcd438` or the remote is otherwise reconciled under explicit authority.
