# BLK-SYSTEM-033 — Health-Check Fixed-Profile Expansion Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and hostile review discipline when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable.

**Goal:** Expand the BLK-034 advisory health-check runner with three additional fixed local profiles while preserving advisory-only, no-production-authority semantics.
**BLK-024 track:** Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening / maturity level L4 pilot runtime for local fixed profiles only, not L5 production authority.
**Architecture:** BLK-SYSTEM-033 extends the existing BLK-034 runner surface by creating BLK-035 as an expansion boundary for exactly three additional profiles: full Python unittest discovery, `go test ./...`, and `go vet ./...`. The sprint keeps the runner as local advisory tooling using trusted absolute executables, canonical repo-root validation, fixed argv arrays, `shell=False`, scrubbed environment, bounded output, deterministic evidence hashes, and no adjacent BLK-System authority. The sprint does not turn health checks into BLK-pipe validation authority or production monitoring.
**Tech Stack:** Markdown doctrine/review/outcome docs, Python `unittest`, Python standard library subprocess runner, Go test/vet as fixed local profiles, Git CLI for exact-path commits.
**Authority boundary:** Narrow local advisory health-check profile expansion. No arbitrary shell, no caller-supplied commands, no network/API/model/cyber tooling, no package-manager execution, no protected BLK-req body reads/copying/parsing/hashing/summarizing, no active-vault path scan or runtime comparison, no BEO publication, no signer/storage/public-ledger mutation, no runtime RTM generation beyond existing BLK-033 fixture evidence, no drift rejection/final drift decision, no Git/source mutation by the runner, and no production health-check authority.

---

## 0. Current Known State

- **Date:** 2026-05-08T18:01:28+10:00
- **Branch state:** `## main...origin/main`
- **HEAD:** `559b029 docs: close blk-system sprint 032 health-check runner`
- **Remote main:** `559b0290206dfbcacb95208f7d3248984440c110 refs/heads/main`
- **Baseline verification:**
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'` — Ran 441 tests in 6.500s, OK
  - `go test ./...` — PASS across all packages
  - `go vet ./...` — PASS
  - `git diff --check` — PASS
- **ID discovery:** `BLK-SYSTEM-033`, `blk-system-033`, and `BLK-035` have no existing plan/outcome/root-doc collisions.
- **Source analysis:** BLK-SYSTEM-032 closeout lists future health-check profile expansion as the natural next Track I candidate, but states BLK-034 does not authorize deferred full Python discovery, `go test ./...`, or `go vet ./...` profiles without a fresh sprint. BLK-024 Track I calls for health checks for local binaries, Python tools, schemas, test fixtures, and disabled transport stubs; Track J requires bounded process/output/env capability claims.

---

## 1. Sprint-Dispatch Approval Provenance

Per BLK-024 operating guidance, this authority-bearing sprint records dispatch approval separately from runtime/profile evidence.

| Field | Value |
| --- | --- |
| Source system | Discord DM to Hermes |
| Operator identity | Camcamcam / Discord user ID `684235178083745819` |
| Message/event ID | Not available to Hermes in this runtime context |
| Timestamp | 2026-05-08 session context; preflight at 2026-05-08T18:01:28+10:00 |
| Approved scope | “based on the recent analysis can you plan the next blk-system spring and execute all tasks from that plan. Ensure alignment with blk-024” interpreted as the next safe BLK-024-aligned BLK-System sprint after BLK-SYSTEM-032: fixed health-check profile expansion for full Python discovery, `go test ./...`, and `go vet ./...` only |
| Explicit excluded authorities | Arbitrary shell, caller-supplied commands, network/API/model/cyber tooling, package-manager execution, protected-vault body reads, active-vault scanning, Git/source mutation by the runner, BLK-pipe dispatch, production BLK-test MCP, new BLK-test smoke, BEO publication, signer/storage/public-ledger writes, runtime RTM generation outside BLK-033 fixture evidence, RTM drift rejection/final drift decisions, and L5 production health-check authority |
| Separation statement | Sprint-dispatch approval does not substitute for runtime/profile approval fixtures and does not grant adjacent BLK-pipe, BLK-test, BEO, RTM, drift, publication, signer/storage/ledger, rollback, or approval authority. |

---

## 2. Authority Boundary

This sprint authorizes edits only to:

- `docs/plans/blk-system-033_health-check-fixed-profile-expansion.md`
- `docs/BLK-035_track-i-health-check-profile-expansion-boundary.md`
- `docs/reviews/BLK-SYSTEM-033_health-check-profile-expansion-inventory.md`
- `docs/reviews/BLK-SYSTEM-033_health-check-profile-expansion-hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-033_*`
- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `python/test_active_doctrine_review_gates.py`
- `python/blk_test_mcp_fixed_tool_live_smoke.py` when needed only to preserve bytecode-cache controls for fixed-profile child interpreters exercised by Python discovery
- `python/test_blk_test_mcp_fixed_tool_live_smoke.py` when needed only to prove that child-interpreter bytecode controls survive that harness's scrubbed environment

The sprint may add only these new fixed profile IDs:

1. `python_unittest_discovery` → `[trusted_python3, '-m', 'unittest', 'discover', '-s', 'python', '-p', 'test_*.py']`
2. `go_test_all` → `[trusted_go, 'test', './...']`
3. `go_vet_all` → `[trusted_go, 'vet', './...']`

The sprint must preserve the existing profiles:

1. `git_status_short_branch`
2. `active_doctrine_gate`

The runner must still reject unknown profiles and must never accept raw command strings or caller-supplied argv.

---

## 3. BLK-024 Selection Rationale

BLK-024 Track I explicitly calls for health checks for local binaries, Python tools, schemas, test fixtures, and disabled transport stubs. BLK-024 Track J requires honest sandbox/capability claims, environment scrubbing, process/output bounds, fixed tools over shell, and default denial of network/model/cyber tooling.

BLK-SYSTEM-032 established the minimal advisory runner. The safest follow-up is not production health-check authority, BLK-test expansion, BEO publication, RTM generation, or drift rejection. It is a bounded expansion of the same local advisory runner to include the already-used project verification commands as fixed profiles.

---

## 4. BLK-001 Through BLK-006 Alignment

| Governing doc | Relevance | Preserved boundary |
| --- | --- | --- |
| BLK-001 — Master Architecture | Health-check status is cross-component operator evidence. | Health checks remain advisory and do not collapse BLK-req, Hermes planning, BLK-pipe mutation, BLK-test verification, BEO publication, or blk-link RTM/drift roles. |
| BLK-002 — Artifact Lifecycle | Full Python discovery may exercise doctrine gates that read active docs, but runner profiles must not touch requirements lifecycle authority. | No staging, linting, promotion, active-vault reads, revision, approval capture, or canonical hashing changes. |
| BLK-003 — Orchestration Protocol | Operator diagnostics can inform escalation but cannot dispatch execution or retry loops. | No BEB/L2 dispatch, tactical LLM invocation, BLK-test startup, BEO handoff, or failure-ceiling authority changes. |
| BLK-004 — BLK-pipe V47 Suite | `go test`/`go vet` look like verification but are not BLK-pipe validation authority. | Runner does not run BLK-pipe, stage, commit, push, reset, checkout, stash, clean, revert, or replace Go-side validation enforcement. |
| BLK-005 — BLK-Req Specification | Doctrine/test checks preserve trace vocabulary but must not inspect requirement bodies. | No protected requirement/use-case body reads, RTM drift decisions, or active-vault comparison. |
| BLK-006 — BLK-Req Implementation Brief | Protected-vault hard-deny remains central. | Runner rejects protected-vault/body/path-scan language and does not scan active-vault paths. |

---

## 5. Planned Tasks

### Task 0 — Publish plan and task-000 outcome

**Goal:** Commit this plan and a task-000 outcome using exact-path staging.

**Files:**

- `docs/plans/blk-system-033_health-check-fixed-profile-expansion.md`
- `docs/outcomes/BLK-SYSTEM-033_task-000-outcome.md`

**Verification:**

- `git diff --check -- docs/plans/blk-system-033_health-check-fixed-profile-expansion.md docs/outcomes/BLK-SYSTEM-033_task-000-outcome.md`
- Markdown fence balance check.

**Commit:** `docs: plan blk-system sprint 033 health-check profiles`

---

### Task 1 — Inventory and BLK-035 boundary doctrine

**Goal:** Record the exact profile-expansion inventory and create BLK-035 active boundary with persistent doctrine-gate coverage.

**Files:**

- `docs/reviews/BLK-SYSTEM-033_health-check-profile-expansion-inventory.md`
- `docs/BLK-035_track-i-health-check-profile-expansion-boundary.md`
- `python/test_active_doctrine_review_gates.py`
- `docs/outcomes/BLK-SYSTEM-033_task-001-outcome.md`

**TDD gate:** Add a RED doctrine test that fails until BLK-035 pins:

- `HEALTH_CHECK_PROFILE_EXPANSION_ADVISORY_ONLY`
- `PYTHON_UNITTEST_DISCOVERY_PROFILE_ADVISORY_ONLY`
- `GO_TEST_ALL_PROFILE_ADVISORY_ONLY`
- `GO_VET_ALL_PROFILE_ADVISORY_ONLY`
- `TRUSTED_ABSOLUTE_EXECUTABLES_ONLY`
- `CANONICAL_REPO_ROOT_REQUIRED`
- `PROCESS_OUTPUT_BYTE_GATE_REQUIRED`
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

**Commit:** `docs: define blk035 health-check profile expansion boundary`

---

### Task 2 — Implement fixed-profile expansion with TDD

**Goal:** Add exactly three fixed profiles to the existing runner while preserving the BLK-034/BLK-035 safety model.

**Files:**

- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `docs/outcomes/BLK-SYSTEM-033_task-002-outcome.md`

**TDD gates:** Add RED tests before implementation proving:

1. new profile IDs exist and resolve to trusted absolute executables with exact fixed argv tails;
2. `go` is resolved through a trusted local/system path, not inherited `PATH`;
3. all five profiles run through `shell=False`, canonical repo-root validation, scrubbed env, output byte gate, and advisory-only status;
4. unknown profiles, caller-supplied argv, shell/inline interpreter, network/package/cyber/model, Git mutation, protected-vault/body, active-vault scan, BEO/RTM/drift authority, and PASS-as-approval laundering attempts fail closed;
5. local smoke runs of all five profiles return advisory evidence without mutating source/Git state.

**Verification:** focused runner tests, focused doctrine gate, full Python suite, Go tests, Go vet, `git diff --check`.

**Commit:** `feat: expand advisory health-check profiles`

---

### Task 3 — Hostile review and closeout

**Goal:** Hostile-review the completed sprint, remediate any blockers, and close out.

**Files:**

- `docs/reviews/BLK-SYSTEM-033_health-check-profile-expansion-hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-033_task-003-outcome.md`
- `docs/outcomes/BLK-SYSTEM-033_sprint-closeout.md`

**Review checklist:**

- exact fixed argv only for all five profiles;
- no raw command string or caller-supplied argv execution;
- trusted executable resolution cannot be hijacked by inherited `PATH`;
- canonical repo-root validation prevents module/workspace shadowing;
- no shell or inline interpreter escape beyond approved module/test invocations;
- no network/API/model/cyber/package-manager tooling;
- no Git/source mutation by the runner;
- no protected-vault body reads or active-vault scans by the runner;
- no BEO publication, signer/storage/public-ledger, runtime RTM generation, or drift rejection;
- output byte gate and redaction are mechanical;
- Python discovery cannot dirty the repository through repo-local `__pycache__` creation, including child interpreters in existing fixed-profile smoke harnesses;
- before/after workspace status observation uses non-mutating Git optional-lock safeguards and does not over-claim unobserved source-mutation surfaces;
- health-check PASS cannot become approval, BLK-pipe validation authority, or production health-check authority;
- sprint-dispatch approval provenance is preserved separately from runtime/profile evidence.

**Verification:** full Python suite, Go tests, Go vet, markdown fence check, `git diff --check`, clean git status, push verification.

**Commit:** `docs: close blk-system sprint 033 health-check profiles`

---

## 6. Final Acceptance Criteria

BLK-SYSTEM-033 is complete only when:

1. the plan and Task 0 outcome are committed and pushed;
2. BLK-035 and the inventory review exist and are covered by RED/GREEN doctrine gates;
3. the three fixed profile additions are implemented by RED/GREEN tests;
4. hostile review and sprint closeout exist;
5. all five profiles smoke-run locally through the runner and return advisory evidence;
6. `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'` passes;
7. `go test ./...` passes;
8. `go vet ./...` passes;
9. `git diff --check` passes;
10. commits are exact-path staged and pushed to `origin/main` after each task.
