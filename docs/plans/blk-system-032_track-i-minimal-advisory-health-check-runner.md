# BLK-SYSTEM-032 — Track I Minimal Advisory Health-Check Runner Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and hostile review discipline when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable.

**Goal:** Add a minimal fixed-profile Track I health-check runner that can execute narrow local advisory checks while preserving no-authority semantics.
**BLK-024 track:** Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening / maturity level L4 pilot runtime for local fixed health-check profiles only, not L5 production authority.
**Architecture:** BLK-SYSTEM-032 follows the BLK-032 fixture boundary and creates a new BLK-034 advisory-runner boundary. The runner may execute only fixed repository-owned argv profiles under `shell=False`, with bounded output, scrubbed environment, no source/Git mutation, no package-manager/network/model/cyber tooling, and no protected-vault or active-vault scan authority. Health-check PASS is advisory only and never grants BLK-pipe, BLK-test, BEO, RTM, drift, publication, signer/storage/ledger, rollback, or approval authority.
**Tech Stack:** Markdown doctrine/review/outcome docs, Python `unittest`, Python standard library subprocess with fixed argv only, Git CLI for exact-path commits.
**Authority boundary:** Narrow local advisory health-check runner pilot. No arbitrary shell, no caller-supplied commands, no production BLK-test MCP, no protected BLK-req body reads/copying/parsing/hashing/summarizing, no active-vault path scan or runtime comparison, no BEO publication, no signer/storage/public-ledger mutation, no runtime RTM generation beyond existing BLK-033 fixture evidence, no drift rejection/final drift decision, no package-manager/network/model/cyber tooling, no Git/source mutation by the runner, and no production health-check authority.

---

## 0. Current Known State

- **Date:** 2026-05-08T17:20:20+10:00
- **Branch state:** `## main...origin/main`
- **HEAD:** `e3e1209 docs: close blk-system sprint 031 doctrine hygiene`
- **Remote main:** `e3e1209ec424647124be4d97287205320a6f489e refs/heads/main`
- **Baseline verification:**
  - Recent discovery subagent ran `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'` — Ran 432 tests, OK.
  - Recent discovery subagent ran `go test ./...` — PASS.
  - Recent discovery subagent ran `go vet ./...` — PASS.
  - `git diff --check` — PASS.
- **ID discovery:** Existing system sprint plans/outcomes run through `BLK-SYSTEM-031`; root BLK docs run through `BLK-033`. `BLK-SYSTEM-032`, `blk-system-032`, and `BLK-034` have no current file collisions.
- **Selection rationale:** BLK-032 explicitly says a later sprint may request live Track I health-check execution if it preserves fixed argv arrays, bounded output, denial of network/package-manager/protected-vault access, read-only Git checks, and advisory-only PASS. After BLK-SYSTEM-030/031, Track I local operator diagnostics are lower-risk than expanding BLK-test, BEO publication, RTM generation, or drift authority.

---

## 1. Sprint-Dispatch Approval Provenance

Per BLK-024 operating guidance added by BLK-SYSTEM-031, this authority-bearing sprint records dispatch approval separately from runtime/profile evidence.

| Field | Value |
| --- | --- |
| Source system | Discord DM to Hermes |
| Operator identity | Camcamcam / Discord user ID `684235178083745819` |
| Message/event ID | Not available to Hermes in this runtime context |
| Timestamp | 2026-05-08T17:11:00+10:00 session context; preflight at 2026-05-08T17:20:20+10:00 |
| Approved scope | “scope out next blk-system plan, write it and then execute all tasks” interpreted as the next safe BLK-System sprint after BLK-SYSTEM-031: a minimal Track I advisory health-check runner pilot with fixed local profiles only |
| Explicit excluded authorities | Arbitrary shell, caller-supplied commands, network/API/model/cyber tooling, package-manager execution, protected-vault body reads, active-vault scanning, Git/source mutation by the runner, production BLK-test MCP, new BLK-test smoke, BEO publication, signer/storage/public-ledger writes, runtime RTM generation outside BLK-033 fixture evidence, RTM drift rejection/final drift decisions, and L5 production health-check authority |
| Separation statement | Sprint-dispatch approval does not substitute for runtime/profile approval fixtures and does not grant adjacent BLK-pipe, BLK-test, BEO, RTM, drift, publication, signer/storage/ledger, rollback, or approval authority. |

---

## 2. Authority Boundary

This sprint authorizes edits only to:

- `docs/plans/blk-system-032_track-i-minimal-advisory-health-check-runner.md`
- `docs/BLK-034_track-i-advisory-health-check-runner-boundary.md`
- `docs/reviews/BLK-SYSTEM-032_health-check-runner-inventory.md`
- `docs/reviews/BLK-SYSTEM-032_health-check-runner-hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-032_*`
- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `python/test_active_doctrine_review_gates.py`

The runner may execute only these initial fixed profiles:

1. `git_status_short_branch` → `['git', 'status', '--short', '--branch']`
2. `active_doctrine_gate` → `['python3', '-m', 'unittest', 'python.test_active_doctrine_review_gates']`

The runner must reject unknown profiles and must never accept raw command strings or caller-supplied argv. Wider profiles such as full Python discovery, `go test ./...`, and `go vet ./...` remain future expansion candidates unless a later sprint explicitly adds them.

---

## 3. BLK-024 Selection Rationale

BLK-024 Track I asks for local health checks for binaries, Python tools, schemas, test fixtures, disabled transport stubs, and clearer escalation packages. BLK-SYSTEM-029 built the non-executing health-check boundary and fixtures; BLK-SYSTEM-032 climbs one rung to a minimal L4 pilot runtime because it runs bounded checks against the real local repo, but only under fixed profiles and advisory semantics.

This is safer than the other obvious post-BLK-SYSTEM-031 candidates:

- It does not expand BLK-test from disabled/smoke to production.
- It does not publish BEOs or capture publication approvals.
- It does not broaden offline RTM generation beyond BLK-033 fixture-only evidence.
- It does not make drift rejection decisions.
- It improves operator diagnostics needed before future authority-bearing work.

---

## 4. BLK-001 Through BLK-006 Alignment

| Governing doc | Relevance | Preserved boundary |
| --- | --- | --- |
| BLK-001 — Master Architecture | Track I diagnostics touch cross-component status visibility. | Health checks provide advisory evidence only and do not collapse BLK-req, Hermes planning, BLK-pipe mutation, BLK-test verification, BEO publication, or blk-link RTM/drift roles. |
| BLK-002 — Artifact Lifecycle | Health-check output may mention doctrine-gate status but must not inspect or mutate requirement artifacts. | No staging, linting, promotion, active-vault reads, revision, approval capture, or canonical hashing changes. |
| BLK-003 — Orchestration Protocol | Operator diagnostics may inform escalation but cannot dispatch execution. | No BEB/L2 dispatch, no tactical LLM invocation, no BLK-test startup, no BEO handoff, no retry/failure-ceiling authority changes. |
| BLK-004 — BLK-pipe V47 Suite | Git and validation status must not become mutation authority. | Runner does not stage, commit, push, reset, checkout, stash, clean, revert, or run BLK-pipe; validation profiles remain BLK-pipe-owned. |
| BLK-005 — BLK-Req Specification | Doctrine-gate checks preserve trace terminology without artifact body access. | No protected requirement/use-case body reads or drift decisions. |
| BLK-006 — BLK-Req Implementation Brief | Protected-vault hard-deny remains central. | Runner rejects protected-vault/body/path-scan language and does not scan active vault paths. |

---

## 5. Planned Tasks

### Task 0 — Publish plan and task-000 outcome

**Goal:** Commit this plan and a task-000 outcome using exact-path staging.

**Files:**

- `docs/plans/blk-system-032_track-i-minimal-advisory-health-check-runner.md`
- `docs/outcomes/BLK-SYSTEM-032_task-000-outcome.md`

**Verification:**

- `git diff --check -- docs/plans/blk-system-032_track-i-minimal-advisory-health-check-runner.md docs/outcomes/BLK-SYSTEM-032_task-000-outcome.md`
- Markdown fence balance check.

**Commit:** `docs: plan blk-system sprint 032 health-check runner`

---

### Task 1 — Inventory and BLK-034 boundary doctrine

**Goal:** Record the exact health-check runner inventory and create the active BLK-034 boundary with persistent doctrine-gate coverage.

**Files:**

- `docs/reviews/BLK-SYSTEM-032_health-check-runner-inventory.md`
- `docs/BLK-034_track-i-advisory-health-check-runner-boundary.md`
- `python/test_active_doctrine_review_gates.py`
- `docs/outcomes/BLK-SYSTEM-032_task-001-outcome.md`

**TDD gate:** Add a RED doctrine test that fails until BLK-034 pins:

- `HEALTH_CHECK_RUNNER_PILOT_ADVISORY_ONLY`
- `HEALTH_CHECK_EXECUTED_LOCAL_FIXED_PROFILE`
- `HEALTH_CHECK_PASS_GRANTS_NO_AUTHORITY`
- `NO_ARBITRARY_SHELL`
- `NO_NETWORK_MODEL_CYBER_TOOLING`
- `NO_PACKAGE_MANAGER`
- `NO_GIT_MUTATION`
- `NO_SOURCE_MUTATION`
- `NO_PROTECTED_BODY_READ`
- `NO_ACTIVE_VAULT_SCAN`
- `NO_BEO_PUBLICATION`
- `NO_RTM_GENERATION`
- `NO_DRIFT_REJECTION`
- `NOT_PRODUCTION_HEALTH_CHECK_AUTHORITY`

**Verification:** focused doctrine gate, full Python suite, Go tests, Go vet, `git diff --check`.

**Commit:** `docs: define blk034 advisory health-check runner boundary`

---

### Task 2 — Implement minimal fixed-profile runner with TDD

**Goal:** Implement a tiny fixed-profile runner that executes only the two initial local profiles and returns bounded advisory evidence.

**Files:**

- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `docs/outcomes/BLK-SYSTEM-032_task-002-outcome.md`

**TDD gates:** Add RED tests before implementation proving:

1. known fixed profiles run with exact argv and `shell=False`;
2. unknown profiles and caller-supplied argv/command strings are rejected;
3. shell, inline interpreter, network/package/cyber/model, Git mutation, protected-vault/body, active-vault scan, BEO/RTM/drift authority, and PASS-as-approval laundering attempts fail closed;
4. environment output is scrubbed, output is bounded, full raw flood output is not embedded, and evidence hashes are deterministic;
5. PASS/FAIL/BLOCKED results are advisory and never grant authority or mutate source/Git state.

**Verification:** focused runner tests, focused doctrine gate, full Python suite, Go tests, Go vet, `git diff --check`.

**Commit:** `feat: add advisory health-check runner pilot`

---

### Task 3 — Hostile review and closeout

**Goal:** Hostile-review the completed sprint, remediate any blockers, and close out.

**Files:**

- `docs/reviews/BLK-SYSTEM-032_health-check-runner-hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-032_sprint-closeout.md`

**Review checklist:**

- fixed argv only; no raw command string or caller-supplied argv execution;
- no shell or inline interpreter escape;
- no network/API/model/cyber/package-manager tooling;
- no Git/source mutation by the runner;
- no protected-vault body reads or active-vault scans;
- no BEO publication, signer/storage/public-ledger, runtime RTM generation, or drift rejection;
- output bounds and redaction are mechanical;
- health-check PASS cannot become approval or production authority;
- sprint-dispatch approval provenance is preserved separately from runtime/profile evidence.

**Verification:** full Python suite, Go tests, Go vet, markdown fence check, `git diff --check`, clean git status, push verification.

**Commit:** `docs: close blk-system sprint 032 health-check runner`

---

## 6. Final Acceptance Criteria

BLK-SYSTEM-032 is complete only when:

1. the plan and Task 0 outcome are committed and pushed;
2. BLK-034 and the inventory review exist and are covered by RED/GREEN doctrine gates;
3. the minimal runner is implemented by RED/GREEN tests;
4. hostile review and sprint closeout exist;
5. `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'` passes;
6. `go test ./...` passes;
7. `go vet ./...` passes;
8. `git diff --check` passes;
9. commits are exact-path staged and pushed to `origin/main` after each task.
