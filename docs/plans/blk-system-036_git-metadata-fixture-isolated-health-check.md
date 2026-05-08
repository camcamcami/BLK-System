# BLK-SYSTEM-036 — Health-Check Git Metadata Fixture Boundary Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and hostile review discipline when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable. This sprint forbids live Codex/tactical-engine/model execution and uses deterministic local review gates instead of live reviewer agents.

**Goal:** Enable safe isolated-mode evidence for `git_status_short_branch` through a source-bound Git metadata fixture that does not copy `.git`, does not mutate Git/source state, and keeps health-check PASS advisory only.
**BLK-024 track:** Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening / maturity level L4 pilot runtime for local fixed profiles only, not L5 production authority.
**Architecture:** BLK-SYSTEM-036 follows BLK-SYSTEM-035, which intentionally kept `git_status_short_branch` source-repository mode only because isolated copies exclude `.git`. This sprint creates BLK-038 as the safe Git metadata fixture boundary, adds a deterministic inventory, and changes only the existing `git_status_short_branch` profile behavior in `workspace_mode="isolated_copy"`: it may execute a trusted fixed Git status metadata reader from the runner-owned isolated workspace while pointing Git at the source repo through explicit `--git-dir`/`--work-tree` arguments and `GIT_OPTIONAL_LOCKS=0`. It must not copy `.git`, synthesize history, clone/worktree, stage, commit, repair, read protected bodies, expand profile IDs, or claim production health-check authority.
**Tech Stack:** Markdown doctrine/review/outcome docs, Python `unittest`, Python standard library subprocess/process control, Git CLI for non-mutating metadata evidence, Git exact-path commits.
**Authority boundary:** Optional local advisory Git metadata fixture for the existing `git_status_short_branch` profile in isolated mode only. No new profile IDs, no arbitrary shell, no caller-supplied commands, no network/API/model/cyber tooling, no package-manager execution, no `.git` copying, no synthetic Git history, no clone/worktree/staging/commit/revert/repair, no protected BLK-req body reads/copying/parsing/hashing/summarizing, no active-vault path scan beyond existing Git status metadata, no BEO publication, no signer/storage/public-ledger mutation, no runtime RTM generation, no drift rejection/final drift decision, and no L5 production health-check authority.

---

## 0. Current Known State

- **Date:** 2026-05-08T21:49:27+10:00
- **Branch state:** `## main...origin/main`
- **HEAD:** `184dfd5 docs: close blk-system sprint 035 isolated health-check`
- **Remote main:** `184dfd539d01660538cb4a603598f2e395ef8fe3 refs/heads/main`
- **Baseline verification:**
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates` — Ran 55 tests, OK
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner` — Ran 28 tests, OK
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'` — Ran 465 tests, OK
  - `go test ./...` — PASS across all packages
  - `go vet ./...` — PASS
  - `git diff --check` — PASS
- **ID discovery:** `BLK-SYSTEM-036`, `blk-system-036`, and `BLK-038` have no existing plan/outcome/root-doc collisions.
- **Source analysis:** BLK-SYSTEM-035 closeout names safe Git-metadata fixture design for isolated `git_status_short_branch` as the first future-work candidate. BLK-037 authorizes future safe Git-metadata fixture work only through a fresh plan, RED/GREEN tests, hostile review, and a new or amended boundary.

---

## 1. Sprint-Dispatch Approval Provenance

| Field | Value |
| --- | --- |
| Source system | Discord DM to Hermes |
| Operator identity | Camcamcam / Discord user ID `684235178083745819` |
| Message/event ID | Not available to Hermes in this runtime context |
| Timestamp | 2026-05-08 session context; preflight at 2026-05-08T21:49:27+10:00 |
| Approved scope | “plan and execute all tasks for blk-system-036” interpreted as BLK-SYSTEM-036 safe Git metadata fixture support for isolated-mode advisory `git_status_short_branch`, following the first future-work candidate from BLK-SYSTEM-035 closeout. |
| Explicit excluded authorities | New health-check profile IDs, arbitrary shell, caller-supplied commands or argv, live Codex/tactical LLM/model execution, production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux or host-secret isolation claims, network firewall claims, package-manager execution, `.git` copying, synthetic Git history, clone/worktree/staging/commit/revert/repair authority, protected-vault body reads/copying/parsing/hashing/summarizing, active-vault body/path scanning beyond existing Git status metadata, Git/source mutation, BLK-pipe dispatch, production BLK-test MCP, new BLK-test smoke, BEO publication, signer/storage/public-ledger writes, runtime RTM generation, RTM drift rejection/final drift decisions, and L5 production health-check authority. |
| Separation statement | Sprint-dispatch approval does not substitute for runtime/profile approval fixtures and does not grant adjacent BLK-pipe, BLK-test, BEO, RTM, drift, publication, signer/storage/ledger, rollback, or approval authority. |

---

## 2. Authority Boundary

This sprint authorizes edits only to:

- `docs/plans/blk-system-036_git-metadata-fixture-isolated-health-check.md`
- `docs/BLK-038_track-i-health-check-git-metadata-fixture-boundary.md`
- `docs/reviews/BLK-SYSTEM-036_health-check-git-metadata-fixture-inventory.md`
- `docs/reviews/BLK-SYSTEM-036_health-check-git-metadata-fixture-hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-036_*`
- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `python/test_active_doctrine_review_gates.py`

The sprint must preserve exactly the existing five fixed profile IDs from BLK-035:

1. `git_status_short_branch`
2. `active_doctrine_gate`
3. `python_unittest_discovery`
4. `go_test_all`
5. `go_vet_all`

No new health-check profiles are authorized. Default source-repository mode must remain compatible with existing callers. Isolated-mode `git_status_short_branch` may use a metadata-fixture command shape only; it must not copy `.git`, create a synthetic repository, run clone/worktree setup, stage, commit, clean, reset, checkout, revert, or repair source state.

---

## 3. BLK-024 Selection Rationale

BLK-024 Track I calls for health checks that clarify local system state. Track J calls for explicit filesystem, process, timeout, output, environment, and capability boundaries. BLK-SYSTEM-032 created the minimal runner, BLK-SYSTEM-033 expanded fixed profiles, BLK-SYSTEM-034 hardened side-effect observation, and BLK-SYSTEM-035 added optional isolated workspaces for non-Git profiles while deliberately keeping Git status source-only.

The safest next step is the first BLK-SYSTEM-035 future-work candidate: safe Git metadata fixture design for isolated `git_status_short_branch`. The sprint remains L4 local pilot runtime because it runs a real local fixed Git status command shape, but it does not grant L5 production authority and does not claim OS sandboxing. It only lets isolated-mode health-check evidence include source Git status without copying `.git` or mutating the repository.

---

## 4. BLK-001 Through BLK-006 Alignment

| Governing doc | Relevance | Preserved boundary |
| --- | --- | --- |
| BLK-001 — Master Architecture | Health-check evidence is operator context near multiple subsystems. | Health checks remain advisory and do not collapse BLK-req, Hermes planning, BLK-pipe mutation, BLK-test verification, BEO publication, or blk-link RTM/drift roles. |
| BLK-002 — Artifact Lifecycle | Git status may observe filenames but must not read or promote protected artifacts. | No staging, linting, promotion, active-vault body access, revision, approval capture, canonical hashing, or artifact mutation changes. |
| BLK-003 — Orchestration Protocol | Health-check status could be mistaken for execution/test approval. | This runner is not BEB/L2 dispatch, not tactical LLM invocation, not BLK-test MCP, not BEO handoff, and not source-evidence approval. |
| BLK-004 — BLK-pipe V47 Suite | Git command surfaces overlap BLK-pipe mutation authority. | The runner uses only non-mutating status metadata and does not run BLK-pipe, stage, commit, push, reset, checkout, stash, clean, revert, or replace Go-side enforcement. |
| BLK-005 — BLK-Req Specification | Protected body and trace authority remain separate. | No protected body reads, RTM drift decisions, active-vault comparison, or trace authority changes. |
| BLK-006 — BLK-Req Implementation Brief | Protected-vault hard-deny remains central. | The isolated copy still excludes `docs/active/`, `docs/requirements/`, and `docs/use_cases/`; Git metadata evidence must not copy or parse protected bodies. |

---

## 5. Planned Tasks

### Task 0 — Publish plan and task-000 outcome

**Goal:** Commit this plan and a task-000 outcome using exact-path staging.

**Files:**

- `docs/plans/blk-system-036_git-metadata-fixture-isolated-health-check.md`
- `docs/outcomes/BLK-SYSTEM-036_task-000-outcome.md`

**Verification:**

- `git diff --check -- docs/plans/blk-system-036_git-metadata-fixture-isolated-health-check.md docs/outcomes/BLK-SYSTEM-036_task-000-outcome.md`
- Markdown fence balance check.

**Commit:** `docs: plan blk-system sprint 036 git metadata fixture`

---

### Task 1 — Inventory and BLK-038 boundary doctrine

**Goal:** Record the safe Git metadata fixture inventory and create BLK-038 active boundary with persistent doctrine-gate coverage.

**Files:**

- `docs/reviews/BLK-SYSTEM-036_health-check-git-metadata-fixture-inventory.md`
- `docs/BLK-038_track-i-health-check-git-metadata-fixture-boundary.md`
- `python/test_active_doctrine_review_gates.py`
- `docs/outcomes/BLK-SYSTEM-036_task-001-outcome.md`

**TDD gate:** Add a RED doctrine test that fails until BLK-038 pins:

- `HEALTH_CHECK_GIT_METADATA_FIXTURE_BOUNDARY`
- `GIT_STATUS_ISOLATED_METADATA_FIXTURE`
- `SOURCE_GIT_METADATA_READ_ONLY`
- `GIT_OPTIONAL_LOCKS_DISABLED`
- `GIT_STATUS_CWD_IS_ISOLATED_WORKSPACE`
- `GIT_DIR_AND_WORK_TREE_EXPLICIT`
- `DOT_GIT_NOT_COPIED`
- `SYNTHETIC_GIT_HISTORY_FORBIDDEN`
- `NO_CLONE_OR_WORKTREE_SETUP`
- `NO_GIT_MUTATION`
- `NO_SOURCE_MUTATION`
- `NO_PROTECTED_BODY_READ`
- `NO_PROTECTED_BODY_COPY`
- `NO_NEW_PROFILE_IDS`
- `NOT_PRODUCTION_HEALTH_CHECK_AUTHORITY`

**Verification:** focused doctrine gate, focused runner tests, full Python suite, Go tests, Go vet, `git diff --check`.

**Commit:** `docs: define blk038 git metadata fixture boundary`

---

### Task 2 — Implement isolated-mode `git_status_short_branch` metadata fixture with TDD

**Goal:** Replace the BLK-SYSTEM-035 isolated-mode rejection for `git_status_short_branch` with a safe source-bound Git metadata fixture command shape.

**Files:**

- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `docs/outcomes/BLK-SYSTEM-036_task-002-outcome.md`

**TDD gates:** Add RED tests before implementation proving:

1. `workspace_mode="isolated_copy"` for `git_status_short_branch` no longer raises before subprocess startup;
2. the metadata command uses the trusted absolute Git executable, `--git-dir <source>/.git`, `--work-tree <source>`, `status`, `--short`, `--branch`, `shell=False`, and `GIT_OPTIONAL_LOCKS=0`;
3. the metadata command executes with `cwd` set to the runner-owned isolated workspace, not the source repository;
4. `.git` is not copied into the isolated workspace and no synthetic history/clone/worktree setup is attempted;
5. result evidence exposes explicit metadata-fixture markers and remains advisory only;
6. source repository status/cache changes still block advisory PASS;
7. default source-repository mode remains byte-for-byte compatible for existing callers.

**Verification:** focused runner tests, focused doctrine gate, full Python suite, Go tests, Go vet, live source-mode smoke of all five profiles, live isolated-mode smoke of all five profiles, `git diff --check`.

**Commit:** `feat: add isolated git status metadata fixture`

---

### Task 3 — Hostile review and closeout

**Goal:** Hostile-review the completed sprint, remediate any blockers, and close out.

**Files:**

- `docs/reviews/BLK-SYSTEM-036_health-check-git-metadata-fixture-hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-036_task-003-outcome.md`
- `docs/outcomes/BLK-SYSTEM-036_sprint-closeout.md`

**Review checklist:**

- no new profile IDs or caller-supplied commands;
- `git_status_short_branch` isolated mode does not copy `.git`;
- Git metadata command is trusted, fixed, shell-free, optional-lock-safe, and cwd-isolated;
- no clone/worktree/synthetic history/staging/commit/repair path appears;
- source status/cache changes still block advisory PASS;
- output byte gate, redaction, temp/cache containment, startup failure handling, and process-group timeout cleanup remain bounded;
- evidence does not claim production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux enforcement, network firewall enforcement, or host-secret isolation;
- no protected-vault body reads/copying/parsing/hashing/summarizing, Git/source repair, BLK-pipe dispatch, production BLK-test MCP, BEO publication, runtime RTM generation, or drift rejection;
- health-check PASS remains advisory and cannot become approval or production health-check authority.

**Verification:** full Python suite, Go tests, Go vet, markdown fence check, deterministic spec/safety gates, `git diff --check`, clean git status, push verification.

**Commit:** `docs: close blk-system sprint 036 git metadata fixture`

---

## 6. Final Acceptance Criteria

BLK-SYSTEM-036 is complete only when:

1. the plan and Task 0 outcome are committed and pushed;
2. BLK-038 and the inventory review exist and are covered by RED/GREEN doctrine gates;
3. isolated-mode `git_status_short_branch` metadata fixture behavior is implemented by RED/GREEN tests;
4. hostile review and sprint closeout exist;
5. source-mode smoke of all five profiles returns advisory evidence;
6. isolated-mode smoke of all five profiles returns advisory evidence, including `git_status_short_branch` through the metadata fixture path;
7. `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'` passes;
8. `go test ./...` passes;
9. `go vet ./...` passes;
10. `git diff --check` passes;
11. commits are exact-path staged and pushed to `origin/main` after each task.
