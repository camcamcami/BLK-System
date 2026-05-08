# BLK-SYSTEM-034 — Health-Check Sandbox and Side-Effect Observation Boundary Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and hostile review discipline when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable.

**Goal:** Harden the advisory health-check runner's local execution boundary by adding honest sandbox vocabulary, stronger side-effect observation, runner-owned temporary containment, and process-group timeout cleanup without granting production health-check authority.
**BLK-024 track:** Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening / maturity level L4 pilot runtime for local fixed profiles only, not L5 production authority.
**Architecture:** BLK-SYSTEM-034 extends BLK-034/BLK-035 by creating BLK-036 as the health-check sandbox and side-effect observation boundary. The sprint keeps the runner fixed-profile and advisory-only while improving observable execution hygiene: runner-owned temporary directories outside the repository, per-run Python bytecode cache routing, explicit non-claims for unobserved surfaces, repo-local cache artifact observation, process-group timeout cleanup, and bounded evidence. It does not claim a production sandbox, cgroup, VM, namespace, seccomp, AppArmor/SELinux, host-secret isolation, network-denial firewall, or production monitoring authority.
**Tech Stack:** Markdown doctrine/review/outcome docs, Python `unittest`, Python standard library subprocess/process control, Git CLI for exact-path commits.
**Authority boundary:** Narrow local advisory health-check boundary hardening only. No arbitrary shell, no caller-supplied commands, no new profile IDs, no network/API/model/cyber tooling, no package-manager execution, no protected BLK-req body reads/copying/parsing/hashing/summarizing, no active-vault path scan or runtime comparison, no BEO publication, no signer/storage/public-ledger mutation, no runtime RTM generation, no drift rejection/final drift decision, no Git/source repair by the runner, and no production health-check authority.

---

## 0. Current Known State

- **Date:** 2026-05-08T19:21:29+10:00
- **Branch state:** `## main...origin/main`
- **HEAD:** `f0cf12c docs: close blk-system sprint 033 health-check profiles`
- **Remote main:** `f0cf12c634e3fa4729d555537fea3e18161e3d19 refs/heads/main`
- **Baseline verification:**
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner` — Ran 13 tests, OK
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates` — Ran 53 tests, OK
  - `go test ./...` — PASS across all packages
  - `go vet ./...` — PASS
  - `git diff --check` — PASS
- **ID discovery:** `BLK-SYSTEM-034`, `blk-system-034`, and `BLK-036` have no existing plan/outcome/root-doc collisions.
- **Source analysis:** BLK-SYSTEM-033 closeout names stronger sandbox/side-effect observation as the next safe future work. BLK-035 already requires `WORKSPACE_STATUS_CHANGE_OBSERVED_NOT_SOURCE_MUTATION_PROOF`; BLK-SYSTEM-034 must preserve that honest non-claim while adding mechanical observations instead of broadening authority.

---

## 1. Sprint-Dispatch Approval Provenance

| Field | Value |
| --- | --- |
| Source system | Discord DM to Hermes |
| Operator identity | Camcamcam / Discord user ID `684235178083745819` |
| Message/event ID | Not available to Hermes in this runtime context |
| Timestamp | 2026-05-08 session context; preflight at 2026-05-08T19:21:29+10:00 |
| Approved scope | “can you plan BLK-SYSTEM-034: Health-Check Sandbox and Side-Effect Observation Boundary. When the plan is written execute all tasks” interpreted as a fixed-profile advisory health-check boundary hardening sprint only. |
| Explicit excluded authorities | Arbitrary shell, caller-supplied commands, new profile IDs, production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux or host-secret isolation claims, network firewall claims, protected-vault body reads, active-vault scanning, Git/source repair, BLK-pipe dispatch, production BLK-test MCP, new BLK-test smoke, BEO publication, signer/storage/public-ledger writes, runtime RTM generation, RTM drift rejection/final drift decisions, and L5 production health-check authority. |
| Separation statement | Sprint-dispatch approval does not substitute for runtime/profile approval fixtures and does not grant adjacent BLK-pipe, BLK-test, BEO, RTM, drift, publication, signer/storage/ledger, rollback, or approval authority. |

---

## 2. Authority Boundary

This sprint authorizes edits only to:

- `docs/plans/blk-system-034_health-check-sandbox-side-effect-observation-boundary.md`
- `docs/BLK-036_track-i-health-check-sandbox-side-effect-observation-boundary.md`
- `docs/reviews/BLK-SYSTEM-034_health-check-side-effect-inventory.md`
- `docs/reviews/BLK-SYSTEM-034_health-check-sandbox-side-effect-hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-034_*`
- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `python/test_active_doctrine_review_gates.py`

The sprint must preserve the existing five fixed profile IDs from BLK-035:

1. `git_status_short_branch`
2. `active_doctrine_gate`
3. `python_unittest_discovery`
4. `go_test_all`
5. `go_vet_all`

No new health-check profiles are authorized by this sprint.

---

## 3. BLK-024 Selection Rationale

BLK-024 Track I calls for operator health checks and escalation clarity. Track J requires security, sandbox, and capability hardening. BLK-SYSTEM-032/033 created and expanded the local advisory fixed-profile runner; the safest next step is not L5 production authority but honest boundary hardening that makes observed side effects explicit and avoids false sandbox claims.

This sprint therefore improves the runner's local execution hygiene while keeping the maturity rung at L4 pilot runtime. It is not a production sandbox sprint and not an authority expansion into BLK-pipe validation, BLK-test, BEO, RTM, or drift decisions.

---

## 4. BLK-001 Through BLK-006 Alignment

| Governing doc | Relevance | Preserved boundary |
| --- | --- | --- |
| BLK-001 — Master Architecture | Health-check evidence is operator context near multiple subsystems. | Health checks remain advisory and do not collapse BLK-req, Hermes planning, BLK-pipe mutation, BLK-test verification, BEO publication, or blk-link RTM/drift roles. |
| BLK-002 — Artifact Lifecycle | Runner observations must not become artifact lifecycle authority. | No staging, linting, promotion, active-vault body access, revision, approval capture, or canonical hashing changes. |
| BLK-003 — Orchestration Protocol | Process/sandbox vocabulary overlaps execution and BLK-test target architecture. | No BEB/L2 dispatch, tactical LLM invocation, production BLK-test startup, BEO handoff, or failure-ceiling authority changes. |
| BLK-004 — BLK-pipe V47 Suite | Health-check process cleanup resembles BLK-pipe process safeguards. | Runner does not run BLK-pipe, stage, commit, push, reset, checkout, stash, clean, revert, or replace Go-side validation enforcement. |
| BLK-005 — BLK-Req Specification | Side-effect observations must not inspect protected requirement/use-case bodies. | No protected body reads, RTM drift decisions, active-vault comparison, or trace authority changes. |
| BLK-006 — BLK-Req Implementation Brief | Protected-vault hard-deny remains central. | Runner continues to reject protected-vault/body/path-scan language and does not scan active-vault paths. |

---

## 5. Planned Tasks

### Task 0 — Publish plan and task-000 outcome

**Goal:** Commit this plan and a task-000 outcome using exact-path staging.

**Files:**

- `docs/plans/blk-system-034_health-check-sandbox-side-effect-observation-boundary.md`
- `docs/outcomes/BLK-SYSTEM-034_task-000-outcome.md`

**Verification:**

- `git diff --check -- docs/plans/blk-system-034_health-check-sandbox-side-effect-observation-boundary.md docs/outcomes/BLK-SYSTEM-034_task-000-outcome.md`
- Markdown fence balance check.

**Commit:** `docs: plan blk-system sprint 034 health-check boundary`

---

### Task 1 — Inventory and BLK-036 boundary doctrine

**Goal:** Record the exact side-effect observation inventory and create BLK-036 active boundary with persistent doctrine-gate coverage.

**Files:**

- `docs/reviews/BLK-SYSTEM-034_health-check-side-effect-inventory.md`
- `docs/BLK-036_track-i-health-check-sandbox-side-effect-observation-boundary.md`
- `python/test_active_doctrine_review_gates.py`
- `docs/outcomes/BLK-SYSTEM-034_task-001-outcome.md`

**TDD gate:** Add a RED doctrine test that fails until BLK-036 pins:

- `HEALTH_CHECK_SANDBOX_SIDE_EFFECT_OBSERVATION_BOUNDARY`
- `RUNNER_TEMP_CONTAINMENT_OUTSIDE_REPO`
- `PYTHON_BYTECODE_CACHE_PER_RUN_OUTSIDE_REPO`
- `PROCESS_GROUP_TIMEOUT_CLEANUP_REQUIRED`
- `REPO_CACHE_ARTIFACT_OBSERVATION_REQUIRED`
- `GIT_STATUS_BEFORE_AFTER_OBSERVATION_REQUIRED`
- `OBSERVED_SIDE_EFFECTS_BLOCK_ADVISORY_PASS`
- `NO_PRODUCTION_SANDBOX_CGROUP_VM_CLAIM`
- `NO_NETWORK_FIREWALL_CLAIM`
- `NO_HOST_SECRET_ISOLATION_CLAIM`
- `NOT_PRODUCTION_HEALTH_CHECK_AUTHORITY`

**Verification:** focused doctrine gate, focused runner tests, full Python suite, Go tests, Go vet, `git diff --check`.

**Commit:** `docs: define blk036 health-check side-effect boundary`

---

### Task 2 — Implement runner boundary hardening with TDD

**Goal:** Add local side-effect observation and process cleanup hardening while preserving fixed-profile advisory semantics.

**Files:**

- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `docs/outcomes/BLK-SYSTEM-034_task-002-outcome.md`

**TDD gates:** Add RED tests before implementation proving:

1. every profile receives runner-owned `TMPDIR`/`TMP`/`TEMP` and per-run `PYTHONPYCACHEPREFIX` outside the repository;
2. repo-local `__pycache__` / `.pyc` creation during a profile blocks the result as `BLOCKED_ADVISORY_ONLY`;
3. timeout cleanup targets the process group/session, not only the direct child;
4. results expose honest observation vocabulary: observed workspace/cache/temp cleanup status plus explicit non-claims for network firewall, production sandbox, host-secret isolation, and unobserved protected surfaces;
5. all five existing profile IDs remain unchanged and advisory-only; unknown profiles and caller-supplied commands still fail closed before subprocess startup.

**Verification:** focused runner tests, focused doctrine gate, full Python suite, Go tests, Go vet, live smoke of all five profiles, `git diff --check`.

**Commit:** `feat: harden health-check side-effect observation`

---

### Task 3 — Hostile review and closeout

**Goal:** Hostile-review the completed sprint, remediate any blockers, and close out.

**Files:**

- `docs/reviews/BLK-SYSTEM-034_health-check-sandbox-side-effect-hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-034_task-003-outcome.md`
- `docs/outcomes/BLK-SYSTEM-034_sprint-closeout.md`

**Review checklist:**

- no new profile IDs or caller-supplied commands;
- runner-owned temp/cache paths stay outside the repository and are removed after completion;
- repo-local cache artifacts or Git status changes block PASS;
- process-group timeout cleanup is attempted and recorded by tests;
- output byte gate and redaction remain bounded;
- evidence does not claim production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux enforcement, network firewall enforcement, or host-secret isolation;
- no protected-vault body reads, active-vault scans, Git/source repair, BLK-pipe dispatch, production BLK-test MCP, BEO publication, runtime RTM generation, or drift rejection;
- health-check PASS remains advisory and cannot become approval or production health-check authority.

**Verification:** full Python suite, Go tests, Go vet, markdown fence check, `git diff --check`, clean git status, push verification.

**Commit:** `docs: close blk-system sprint 034 health-check boundary`

---

## 6. Final Acceptance Criteria

BLK-SYSTEM-034 is complete only when:

1. the plan and Task 0 outcome are committed and pushed;
2. BLK-036 and the inventory review exist and are covered by RED/GREEN doctrine gates;
3. runner hardening is implemented by RED/GREEN tests;
4. hostile review and sprint closeout exist;
5. all five profiles smoke-run locally through the runner and return advisory evidence;
6. `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'` passes;
7. `go test ./...` passes;
8. `go vet ./...` passes;
9. `git diff --check` passes;
10. commits are exact-path staged and pushed to `origin/main` after each task.
