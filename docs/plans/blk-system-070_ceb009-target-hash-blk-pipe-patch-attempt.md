# BLK-SYSTEM-070 — CEB_009 Target-Hash BLK-pipe Patch Attempt Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `blk-system-authority-gated-sprints` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, with active selection controlled by `docs/BLK-059_blk-system-post-058-roadmap.md`, then BLK-001 through BLK-006 as applicable.

**Goal:** Execute exactly one fresh, exact-target, BLK-pipe-mediated CEB_009 patch attempt against Kuronode SHA `70b6062b92cf61c12bf190f92dc6b45ea4dcd438` using `target_hash` equal to that SHA.
**BLK-024 track:** Track C — BLK-pipe blast shield and forge / L3 exact approved real-repo source-mutation attempt.
**Architecture:** Hermes records the operator approval, constructs a target-hash-pinned BLK-pipe payload, and invokes the Go BLK-pipe utility exactly once. BLK-pipe is the only mutation authority for Kuronode. Hermes then audits the raw report, side effects, allowlist, and authority boundaries before closeout.
**Tech Stack:** Markdown, JSON, Python artifact generation, Go `blk-pipe`, Git.
**Authority boundary:** Authorized only for one BLK-pipe-mediated patch attempt modifying `scripts/smoke_test.ts` in Kuronode at the exact approved SHA. No Codex, no BLK-test MCP, no Electron/smoke runtime, no TypeScript/package-manager tooling, no BEO/CEO publication, no RTM, and no Kuronode remote push.

---

## 1. Operator Approval Captured

The operator explicitly approved:

```text
I approve BLK-SYSTEM-070: one exact BLK-pipe-mediated CEB_009 patch attempt against Kuronode SHA 70b6062b92cf61c12bf190f92dc6b45ea4dcd438, with target_hash equal to that SHA, modifying only scripts/smoke_test.ts, with no Codex, no BLK-test MCP, no Electron/ smoke runtime, no TypeScript/ package-manager tooling, no BEO/CEO publication, no RTM, and no Kuronode remote push.
```

Approval is bound to:

```text
approved_sha=70b6062b92cf61c12bf190f92dc6b45ea4dcd438
target_hash=70b6062b92cf61c12bf190f92dc6b45ea4dcd438
allowed_modified_files=[scripts/smoke_test.ts]
allowed_new_files=[]
run_id=BLK-SYSTEM-070-CEB009-TARGET-HASH-PATCH-RUN-001
```

---

## 2. Current Known State

Captured 2026-05-11T10:03:33+10:00:

```text
BLK-System HEAD: 2c9cf9d docs: correct blk-system 069 closeout commit chain
BLK-System status: ## main...origin/main
BLK-System remote main: 2c9cf9d618d9cfa778d4c02b5c65e5cc623266d5
Kuronode HEAD: 70b6062b92cf61c12bf190f92dc6b45ea4dcd438
Kuronode origin/main: 70b6062b92cf61c12bf190f92dc6b45ea4dcd438
Kuronode status rows including ignored: 0
Kuronode branch status: ## main...origin/main
scripts/smoke_test.ts unstaged diff bytes: 0
scripts/smoke_test.ts staged diff bytes: 0
```

---

## 3. Governing Doctrine Alignment

- **BLK-001:** Preserves component separation: Hermes plans/audits, BLK-pipe enforces source mutation, and downstream verification/publication/trace closure remain separate.
- **BLK-002 / BLK-005:** No BLK-req baseline, staging, active-vault body read, or requirement mutation is in scope.
- **BLK-003:** Uses a bounded handoff packet and exact allowlist; honors human dispatch and failure closeout boundaries.
- **BLK-004:** Uses BLK-pipe as the deterministic mutation authority with exact allowlists, output caps, validation abort, report evidence, and Sprint 069 exact-target local `target_hash` gate.
- **BLK-006:** Preserves protected-vault hard-deny and no protected BLK-req body reads.
- **BLK-059:** Advances Kuronode tactical quality intent by attempting a tightly bounded patch under BLK-pipe, without expanding validation/runtime/publication authorities.

---

## 4. Execution Tasks

### Task 000 — Plan publication

- Write this plan and task-000 outcome.
- Verify Markdown fences and `git diff --check` for exact paths.
- Commit and push as `docs: plan blk-system 070 target hash patch attempt`.

### Task 001 — Approval record and payload generation

Create:

```text
docs/outcomes/BLK-SYSTEM-070_task-001-approval-record.json
docs/outcomes/BLK-SYSTEM-070_blk-pipe-payload.json
docs/outcomes/BLK-SYSTEM-070_task-001-outcome.md
```

Payload requirements:

```json
{
  "action": "execute",
  "beb_id": "CEB_009",
  "work_dir": "/home/dad/code/Kuronode-v1",
  "target_branch": "main",
  "target_hash": "70b6062b92cf61c12bf190f92dc6b45ea4dcd438",
  "allowed_modified_files": ["scripts/smoke_test.ts"],
  "allowed_new_files": [],
  "validation_commands": ["git diff --check -- scripts/smoke_test.ts"]
}
```

The engine may be only the deterministic Python source-edit script already captured for CEB_009 remediation. The payload must not start Codex, BLK-test MCP, Electron/smoke runtime, TypeScript tooling, package managers, publication, RTM, or Kuronode remote push.

### Task 002 — One BLK-pipe patch attempt

Before invocation, re-check:

```text
Kuronode HEAD == approved SHA
Kuronode origin/main == approved SHA
Kuronode worktree status rows including ignored == 0
scripts/smoke_test.ts unstaged diff == empty
scripts/smoke_test.ts staged diff == empty
```

Invoke exactly once:

```text
go run ./cmd/blk-pipe --payload /home/dad/BLK-System/docs/outcomes/BLK-SYSTEM-070_blk-pipe-payload.json
```

Capture raw report:

```text
docs/outcomes/BLK-SYSTEM-070_blk-pipe-report.json
```

Post-attempt checks:

```text
Kuronode HEAD
Kuronode status --short --branch
Kuronode diff for scripts/smoke_test.ts
Kuronode staged diff for scripts/smoke_test.ts
Kuronode remote push not performed
```

If BLK-pipe returns `SUCCESS`, record the new local Kuronode commit hash and diff. Do not push Kuronode.

If BLK-pipe returns any blocked/failure status, record the raw report, verify no unapproved side effects, and do not retry this run ID.

### Task 003 — Hostile review and sprint closeout

Create:

```text
docs/outcomes/BLK-SYSTEM-070_task-002-outcome.md
docs/reviews/BLK-SYSTEM-070_ceb009-target-hash-blk-pipe-patch-attempt-hostile-review.md
docs/outcomes/BLK-SYSTEM-070_sprint-closeout.md
```

Hostile review must check:

- exact target SHA and `target_hash` match approval;
- no fetch-auth workaround or credential injection was used;
- BLK-pipe was invoked exactly once;
- only `scripts/smoke_test.ts` was modified/committed if successful;
- no Kuronode remote push;
- no Codex, BLK-test MCP, Electron/smoke runtime, TypeScript/package-manager tooling, BEO/CEO publication, RTM, protected-body read, or authority laundering;
- adapter/report status preserved exact outcome.

Run final BLK-System verification:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover python 'test_*.py'
go test ./...
git diff --check
```

---

## 5. Stop Conditions

Stop without invoking BLK-pipe if:

- Kuronode local or remote head differs from the approved SHA;
- Kuronode worktree is not sterile;
- payload `target_hash` differs from the approved SHA;
- payload allowlists differ from exactly `scripts/smoke_test.ts` modified and no new files;
- any step requires Codex, BLK-test MCP, Electron/smoke runtime, TypeScript/package-manager tooling, credentials, Kuronode remote push, BEO/CEO publication, RTM, or protected body reads.

Stop after one invocation regardless of BLK-pipe status. The run ID is consumed.

---

## 6. Non-Goals

This sprint does not authorize production BLK-test MCP, live tactical LLM execution, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads, authoritative BEO/CEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, source mutation outside `scripts/smoke_test.ts`, Electron/smoke runtime, TypeScript tooling, package-manager invocation, browser/cyber tooling, credential injection, or Kuronode remote push.
