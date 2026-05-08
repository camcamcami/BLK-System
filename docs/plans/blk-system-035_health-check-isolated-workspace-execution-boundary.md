# BLK-SYSTEM-035 — Health-Check Isolated Workspace Execution Boundary Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and hostile review discipline when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable.

**Goal:** Add an optional isolated-workspace execution mode for the advisory health-check runner so fixed verification profiles can run from a runner-owned copy outside the source repository while preserving advisory-only, non-production authority.
**BLK-024 track:** Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening / maturity level L4 pilot runtime for local fixed profiles only, not L5 production authority.
**Architecture:** BLK-SYSTEM-035 follows BLK-SYSTEM-034's side-effect observation hardening with the next logical rung: execute non-Git fixed profiles from a runner-owned isolated workspace copy outside `REPO_ROOT`. The sprint creates BLK-037 as the isolated-workspace boundary, preserves the existing five BLK-035 profile IDs, keeps source-repository status/cache observations, excludes `.git` and protected BLK-req paths from the isolated copy, and reports explicit non-claims for production sandbox, network firewall, host-secret isolation, BLK-test, BEO, RTM, and drift authority.
**Tech Stack:** Markdown doctrine/review/outcome docs, Python `unittest`, Python standard library filesystem/subprocess/process control, Git CLI for exact-path commits.
**Authority boundary:** Optional local isolated-workspace health-check execution only. No new profile IDs, no arbitrary shell, no caller-supplied commands, no network/API/model/cyber tooling, no package-manager execution, no protected BLK-req body reads/copying/parsing/hashing/summarizing, no active-vault path scan or runtime comparison, no BEO publication, no signer/storage/public-ledger mutation, no runtime RTM generation, no drift rejection/final drift decision, no Git/source repair by the runner, and no L5 production health-check authority.

---

## 0. Current Known State

- **Date:** 2026-05-08T20:48:04+10:00
- **Branch state:** `## main...origin/main`
- **HEAD:** `14a7dbd docs: close blk-system sprint 034 health-check boundary`
- **Remote main:** `14a7dbdbc3d7f2f960c3161eb5a21243ea5a7b68 refs/heads/main`
- **Baseline verification:**
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner` — Ran 19 tests, OK
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates` — Ran 54 tests, OK
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'` — Ran 455 tests, OK
  - `go test ./...` — PASS across all packages
  - `go vet ./...` — PASS
  - `git diff --check` — PASS
- **ID discovery:** `BLK-SYSTEM-035`, `blk-system-035`, and `BLK-037` have no existing plan/outcome/root-doc collisions.
- **Source analysis:** BLK-SYSTEM-034 closeout names isolated-workspace health-check execution as the first future-work candidate if stronger no-source-mutation claims are required. BLK-036 explicitly says future sprints may request isolated-workspace execution only through a fresh plan, RED/GREEN tests, hostile review, and a new or amended boundary.

---

## 1. Sprint-Dispatch Approval Provenance

| Field | Value |
| --- | --- |
| Source system | Discord DM to Hermes |
| Operator identity | Camcamcam / Discord user ID `684235178083745819` |
| Message/event ID | Not available to Hermes in this runtime context |
| Timestamp | 2026-05-08 session context; preflight at 2026-05-08T20:48:04+10:00 |
| Approved scope | “now that BLK-SYSTEM-034 is complete can you write the plan for the next logical sprint and then execute all of the tasks” interpreted as BLK-SYSTEM-035 isolated-workspace advisory health-check hardening only. |
| Explicit excluded authorities | New profile IDs, arbitrary shell, caller-supplied commands, production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux or host-secret isolation claims, network firewall claims, package-manager execution, protected-vault body reads/copying/parsing/hashing/summarizing, active-vault scanning/comparison, Git/source repair, BLK-pipe dispatch, production BLK-test MCP, new BLK-test smoke, BEO publication, signer/storage/public-ledger writes, runtime RTM generation, RTM drift rejection/final drift decisions, and L5 production health-check authority. |
| Separation statement | Sprint-dispatch approval does not substitute for runtime/profile approval fixtures and does not grant adjacent BLK-pipe, BLK-test, BEO, RTM, drift, publication, signer/storage/ledger, rollback, or approval authority. |

---

## 2. Authority Boundary

This sprint authorizes edits only to:

- `docs/plans/blk-system-035_health-check-isolated-workspace-execution-boundary.md`
- `docs/BLK-037_track-i-health-check-isolated-workspace-execution-boundary.md`
- `docs/reviews/BLK-SYSTEM-035_health-check-isolated-workspace-inventory.md`
- `docs/reviews/BLK-SYSTEM-035_health-check-isolated-workspace-hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-035_*`
- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `python/test_active_doctrine_review_gates.py`

The sprint must preserve the existing five fixed profile IDs from BLK-035:

1. `git_status_short_branch`
2. `active_doctrine_gate`
3. `python_unittest_discovery`
4. `go_test_all`
5. `go_vet_all`

No new health-check profiles are authorized. The isolated-workspace mode is optional and must not change default source-repository behavior. Because the isolated copy deliberately excludes `.git`, `git_status_short_branch` remains source-repository mode only unless a later sprint creates a separate safe Git-metadata fixture boundary.

---

## 3. BLK-024 Selection Rationale

BLK-024 Track I calls for operator health checks that clarify local system status. Track J calls for explicit filesystem, process, timeout, output, environment, and capability boundaries. BLK-SYSTEM-032 created the minimal runner, BLK-SYSTEM-033 expanded fixed profiles, and BLK-SYSTEM-034 hardened side-effect observation. The next safest logical step is not production authority but optional isolated-workspace execution for heavier non-Git profiles so the source repository is no longer the process working directory.

This sprint remains L4 local pilot runtime because it runs real local fixed profiles, but it does not grant L5 production health-check authority and does not claim OS-level sandboxing. It only strengthens source-repository non-mutation posture by copying a filtered snapshot into a runner-owned temporary workspace outside the repository.

---

## 4. BLK-001 Through BLK-006 Alignment

| Governing doc | Relevance | Preserved boundary |
| --- | --- | --- |
| BLK-001 — Master Architecture | Health-check evidence is operator context near multiple subsystems. | Health checks remain advisory and do not collapse BLK-req, Hermes planning, BLK-pipe mutation, BLK-test verification, BEO publication, or blk-link RTM/drift roles. |
| BLK-002 — Artifact Lifecycle | Isolated workspaces must not copy or inspect protected artifact bodies. | No staging, linting, promotion, active-vault body access, revision, approval capture, or canonical hashing changes. |
| BLK-003 — Orchestration Protocol | Isolated workspace language overlaps BLK-test target-state clone semantics. | This runner is not production BLK-test MCP, not BEB/L2 dispatch, not tactical LLM invocation, not BEO handoff, and not BLK-test source evidence authority. |
| BLK-004 — BLK-pipe V47 Suite | Health-check process isolation resembles BLK-pipe/validation safeguards. | Runner does not run BLK-pipe, stage, commit, push, reset, checkout, stash, clean, revert, or replace Go-side validation enforcement. |
| BLK-005 — BLK-Req Specification | Filtered copies must preserve protected-body isolation and trace authority separation. | No protected body reads, RTM drift decisions, active-vault comparison, or trace authority changes. |
| BLK-006 — BLK-Req Implementation Brief | Protected-vault hard-deny remains central. | Isolated copy setup must exclude `docs/active/`, `docs/requirements/`, and `docs/use_cases/` and must not read protected bodies to decide health status. |

---

## 5. Planned Tasks

### Task 0 — Publish plan and task-000 outcome

**Goal:** Commit this plan and a task-000 outcome using exact-path staging.

**Files:**

- `docs/plans/blk-system-035_health-check-isolated-workspace-execution-boundary.md`
- `docs/outcomes/BLK-SYSTEM-035_task-000-outcome.md`

**Verification:**

- `git diff --check -- docs/plans/blk-system-035_health-check-isolated-workspace-execution-boundary.md docs/outcomes/BLK-SYSTEM-035_task-000-outcome.md`
- Markdown fence balance check.

**Commit:** `docs: plan blk-system sprint 035 isolated health-check`

---

### Task 1 — Inventory and BLK-037 boundary doctrine

**Goal:** Record the exact isolated-workspace design inventory and create BLK-037 active boundary with persistent doctrine-gate coverage.

**Files:**

- `docs/reviews/BLK-SYSTEM-035_health-check-isolated-workspace-inventory.md`
- `docs/BLK-037_track-i-health-check-isolated-workspace-execution-boundary.md`
- `python/test_active_doctrine_review_gates.py`
- `docs/outcomes/BLK-SYSTEM-035_task-001-outcome.md`

**TDD gate:** Add a RED doctrine test that fails until BLK-037 pins:

- `HEALTH_CHECK_ISOLATED_WORKSPACE_EXECUTION_BOUNDARY`
- `ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO`
- `SOURCE_REPO_NOT_EXECUTION_CWD`
- `PROTECTED_BLK_REQ_PATHS_EXCLUDED_FROM_COPY`
- `DOT_GIT_EXCLUDED_FROM_COPY`
- `SOURCE_REPO_STATUS_BEFORE_AFTER_OBSERVATION_REQUIRED`
- `SOURCE_REPO_CACHE_OBSERVATION_REQUIRED`
- `ISOLATED_WORKSPACE_REMOVAL_REQUIRED`
- `GIT_STATUS_PROFILE_SOURCE_REPO_ONLY`
- `NO_NEW_PROFILE_IDS`
- `NO_PRODUCTION_SANDBOX_CGROUP_VM_CLAIM`
- `NO_NETWORK_FIREWALL_CLAIM`
- `NO_HOST_SECRET_ISOLATION_CLAIM`
- `NOT_PRODUCTION_HEALTH_CHECK_AUTHORITY`

**Verification:** focused doctrine gate, focused runner tests, full Python suite, Go tests, Go vet, `git diff --check`.

**Commit:** `docs: define blk037 isolated health-check boundary`

---

### Task 2 — Implement optional isolated-workspace runner mode with TDD

**Goal:** Add optional isolated-workspace execution for non-Git fixed profiles while preserving default source-repository behavior.

**Files:**

- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `docs/outcomes/BLK-SYSTEM-035_task-002-outcome.md`

**TDD gates:** Add RED tests before implementation proving:

1. `workspace_mode="isolated_copy"` executes eligible non-Git fixed profiles with `cwd` under a runner-owned temp directory outside `REPO_ROOT`, not the source repo;
2. isolated-copy `PYTHONPATH`, `TMPDIR`, `TMP`, `TEMP`, and `PYTHONPYCACHEPREFIX` point outside `REPO_ROOT`;
3. the isolated copy excludes `.git`, `docs/active/`, `docs/requirements/`, `docs/use_cases/`, `__pycache__`, and `.pyc` artifacts;
4. source-repository Git status/cache snapshots are still observed before and after isolated execution, and any source-repository change blocks advisory PASS;
5. the isolated workspace is removed after completion and failed removal blocks advisory PASS;
6. `git_status_short_branch` fails closed for isolated mode before subprocess startup because `.git` is deliberately excluded;
7. default source-repository mode remains byte-for-byte compatible for existing callers.

**Verification:** focused runner tests, focused doctrine gate, full Python suite, Go tests, Go vet, live isolated-mode smoke of `active_doctrine_gate`, `python_unittest_discovery`, `go_test_all`, and `go_vet_all`, source-mode smoke of all five profiles, `git diff --check`.

**Commit:** `feat: add isolated health-check workspace mode`

---

### Task 3 — Hostile review and closeout

**Goal:** Hostile-review the completed sprint, remediate any blockers, and close out.

**Files:**

- `docs/reviews/BLK-SYSTEM-035_health-check-isolated-workspace-hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-035_task-003-outcome.md`
- `docs/outcomes/BLK-SYSTEM-035_sprint-closeout.md`

**Review checklist:**

- no new profile IDs or caller-supplied commands;
- isolated workspace is outside the source repository and removed after completion;
- `.git` and protected BLK-req paths are excluded from isolated copies;
- source-repository status/cache changes block PASS;
- `git_status_short_branch` does not pretend to run in a `.git`-less isolated copy;
- output byte gate, redaction, temp/cache containment, startup failure handling, and process-group timeout cleanup remain bounded;
- evidence does not claim production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux enforcement, network firewall enforcement, or host-secret isolation;
- no protected-vault body reads/copying/parsing/hashing/summarizing, active-vault scans, Git/source repair, BLK-pipe dispatch, production BLK-test MCP, BEO publication, runtime RTM generation, or drift rejection;
- health-check PASS remains advisory and cannot become approval or production health-check authority.

**Verification:** full Python suite, Go tests, Go vet, markdown fence check, `git diff --check`, clean git status, push verification.

**Commit:** `docs: close blk-system sprint 035 isolated health-check`

---

## 6. Final Acceptance Criteria

BLK-SYSTEM-035 is complete only when:

1. the plan and Task 0 outcome are committed and pushed;
2. BLK-037 and the inventory review exist and are covered by RED/GREEN doctrine gates;
3. optional isolated-workspace mode is implemented by RED/GREEN tests;
4. hostile review and sprint closeout exist;
5. source-mode smoke of all five profiles returns advisory evidence;
6. isolated-mode smoke of `active_doctrine_gate`, `python_unittest_discovery`, `go_test_all`, and `go_vet_all` returns advisory evidence;
7. `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'` passes;
8. `go test ./...` passes;
9. `go vet ./...` passes;
10. `git diff --check` passes;
11. commits are exact-path staged and pushed to `origin/main` after each task.
