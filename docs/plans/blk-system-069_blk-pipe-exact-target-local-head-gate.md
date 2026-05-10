# BLK-SYSTEM-069 — BLK-pipe Exact-Target Local Head Gate Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `blk-system-authority-gated-sprints` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, with active selection controlled by `docs/BLK-059_blk-system-post-058-roadmap.md`, then BLK-001 through BLK-006 as applicable.

**Goal:** Remove the BLK-pipe private-HTTPS internal-fetch blocker for exact-target, already-local source-mutation attempts by adding a deterministic local `target_hash` gate that fails closed before engine execution if the local branch is absent or not exactly approved.
**BLK-024 track:** Track C — BLK-pipe blast shield and forge / L1-L2 local guard hardening.
**Architecture:** Go `blk-pipe` remains the mutation authority. Python may construct safer payloads, but Go enforces exact-target local state before tactical engine start. Remote alignment remains an external approval/preflight obligation for this CEB_009 chain and is not silently replaced by this sprint.
**Tech Stack:** Go, Python unittest, Markdown doctrine/outcome docs.
**Authority boundary:** BLK-System implementation hardening only. This plan does not authorize a Kuronode patch attempt, Codex, BLK-test MCP, Electron/smoke runtime, TypeScript/package-manager tooling, BEO/CEO publication, RTM generation, Kuronode remote push, credential injection, or private-repo network fetch bypass for unpinned payloads.

---

## 1. Current Known State

Captured 2026-05-11T09:25:58+10:00:

```text
BLK-System HEAD: f6dc577 docs: close out blk-system 068 patch attempt
BLK-System status: ## main...origin/main
BLK-System remote main: f6dc577fec1d845d3ef52b074481710b9d0caaf5
Kuronode HEAD: 70b6062b92cf61c12bf190f92dc6b45ea4dcd438
Kuronode origin/main: 70b6062b92cf61c12bf190f92dc6b45ea4dcd438
Kuronode status rows including ignored: 0
Kuronode remote URL: https://github.com/camcamcami/Kuronode-v1.git
```

BLK-SYSTEM-068 proved the target worktree was sterile, but the single authorized BLK-pipe attempt blocked before mutation because `gitguard.PrepareTargetBranch` unconditionally ran `git fetch origin` in a scrubbed environment that could not authenticate to the private HTTPS GitHub remote.

---

## 2. Governing Doctrine Alignment

- **BLK-001:** Preserves separation between Hermes planning/audit, BLK-pipe source mutation enforcement, and later verification/publication layers.
- **BLK-002 / BLK-005:** No protected BLK-req staging, active-vault body read, baseline promotion, or requirement mutation is in scope.
- **BLK-003:** Keeps human dispatch gates and failure closeout boundaries; this sprint is not a new CEB_009 patch dispatch.
- **BLK-004:** Modifies BLK-pipe Git-fortress behavior only for an explicitly pinned execute payload. Exact-path staging, output caps, cleanup, validation aborts, and verified revert remain unchanged.
- **BLK-006:** Preserves protected-vault hard-deny and no protected body reads.
- **BLK-059:** Advances Workstream B / Track C dependency work needed for Kuronode tactical quality activation without granting package-manager, network, model, browser, cyber, publication, RTM, or production sandbox authority.

---

## 3. Design Decision

Add an **exact-target local mode** for execute payloads with a non-empty `target_hash`:

1. `target_hash` for execute payloads must validate as a full 40- or 64-character hexadecimal commit object ID.
2. When `target_branch` and `target_hash` are present, BLK-pipe must:
   - validate the branch name;
   - require the current worktree to be clean;
   - checkout only an existing local branch;
   - avoid `git fetch origin`, `ls-remote`, remote-tracking checkout, and orphan branch creation;
   - verify `HEAD == target_hash` after checkout;
   - fail closed before engine execution on missing local branch or head mismatch.
3. When `target_hash` is absent, legacy branch preparation remains unchanged and may still fetch for unpinned branch discovery.
4. When `target_hash` is present without `target_branch`, BLK-pipe must verify the current `HEAD` equals `target_hash` before engine execution.
5. The CEB_009 fresh-target payload builder must include `target_hash` so a future fresh approval can use the local exact-target gate.

This is not credential injection. It does not make BLK-pipe trust a stale local checkout blindly: the local `HEAD` must exactly equal the approval-bound hash, while remote alignment remains a separately recorded preflight and approval obligation.

---

## 4. Tasks

### Task 000 — Plan publication

- Create this plan and `docs/outcomes/BLK-SYSTEM-069_task-000-outcome.md`.
- Verify Markdown fences and exact-path diff checks.
- Commit and push as `docs: plan blk-system 069 exact target gate`.

### Task 001 — Go BLK-pipe exact-target local gate

**Files expected:**

```text
internal/contracts/payload.go
internal/contracts/payload_test.go
internal/gitguard/branch.go
internal/gitguard/branch_test.go
internal/pipe/run.go
internal/pipe/run_test.go
```

**RED gates first:**

- Execute payload with unsafe `target_hash` is rejected.
- Exact-target local branch preparation does not invoke `git fetch`, `git ls-remote`, remote checkout, or orphan creation.
- Missing local branch in exact-target mode fails before engine execution.
- Local branch at a different HEAD fails before engine execution and leaves no source mutation.
- Current-branch exact-target mode with no `target_branch` fails before engine execution if `HEAD` mismatches.

**GREEN implementation:**

- Add minimal Go helpers to enforce exact-target local branch/current-head checks.
- Preserve legacy fetch behavior for unpinned payloads.
- Use existing bounded Git helper paths only.

**Verification:**

```text
go test ./internal/contracts ./internal/gitguard ./internal/pipe
go test ./...
git diff --check
```

### Task 002 — CEB_009 payload builder exact-target binding

**Files expected:**

```text
python/kuronode_power_of_ten_ceb009_fresh_target_patch_execution.py
python/test_kuronode_power_of_ten_ceb009_fresh_target_patch_execution.py
```

**RED gates first:**

- Builder output must include `target_hash == CURRENT_TARGET_HEAD_SHA` in the BLK-pipe payload.
- Mutating or omitting exact target SHA remains rejected by request validation.
- The payload remains limited to `scripts/smoke_test.ts`, no new files, no Codex, no BLK-test MCP, no Electron/smoke runtime, no TypeScript/package-manager tooling, no BEO/CEO publication, no RTM, and no Kuronode remote push.

**GREEN implementation:**

- Add `target_hash` to the generated payload.
- Keep all prior side-effect flags false until a future sprint invokes BLK-pipe.

**Verification:**

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_kuronode_power_of_ten_ceb009_fresh_target_patch_execution
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover python 'test_*.py'
git diff --check
```

### Task 003 — Hostile review and closeout

- Hostile-review authority laundering and safety regressions:
  - `target_hash` must not become retargeting authority;
  - exact-target local mode must not fetch or use remote state;
  - unpinned payloads must not inherit local-only behavior;
  - future CEB_009 patch authority remains fresh and separate;
  - no Kuronode patch, commit, push, runtime smoke, package-manager command, BEO/CEO publication, or RTM generation occurs in this sprint.
- Write:

```text
docs/reviews/BLK-SYSTEM-069_blk-pipe-exact-target-local-head-gate-hostile-review.md
docs/outcomes/BLK-SYSTEM-069_sprint-closeout.md
```

- Commit and push as `docs: close out blk-system 069 exact target gate`.

---

## 5. Stop Conditions

Stop and close as BLOCKED if:

- BLK-System worktree is dirty with unowned changes;
- tests show exact-target mode still fetches or can start the engine after a head mismatch;
- a fix requires credential helper injection, broad environment restoration, or live private-repo network fetch authority;
- a future CEB_009 patch attempt is needed to prove the code change. That requires a fresh explicit approval and a separate sprint.

---

## 6. Non-Goals

This sprint does not authorize production BLK-test MCP, live tactical LLM execution, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads, authoritative BEO/CEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, Kuronode source mutation, Kuronode remote push, Electron/smoke runtime, TypeScript tooling, package-manager invocation, browser/cyber tooling, or credential injection.
