# BLK-SYSTEM-020 — Validation Command Profile Tightening Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `requesting-code-review` when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable. Execute task-by-task with strict RED/GREEN evidence, deterministic local tests, exact-path staging, per-task outcome docs, and push after each task. Do not use Hindsight unless explicitly requested. Do not run Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, RTM generation, RTM authority, or authoritative BEO publication unless a separate execution approval explicitly grants it.

**Goal:** Replace shell-shaped validation authority for future BLK-native payloads with repository-owned named validation profiles while preserving current guarded-local compatibility boundaries.
**BLK-024 track:** Track D — Validation command profile tightening / maturity level L1 fixture-only implementation with L2-style fail-closed payload refusal for invalid profiles.
**Architecture:** BLK-pipe remains the deterministic Go blast shield. This sprint introduces a small repository-owned validation profile registry, payload/report fields that make the selected profile and exact resolved commands auditable, and doctrine gates that mark free-form validation strings as trusted-local transitional authority rather than a future autonomous boundary. Python adapter changes are limited to payload compatibility for profile fields; they do not upgrade Python into the enforcement authority.
**Tech Stack:** Go (`internal/contracts`, `internal/validation`, `internal/pipe`), Python adapter/unit tests, Markdown doctrine gates, Git CLI.
**Authority boundary:** Fixture/local implementation hardening only. This plan does not authorize production BLK-test MCP, live tactical execution, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, or source mutation outside exact approved allowlists.

---

## 0. Current Known State

Planning preflight captured before drafting this plan:

```text
date -Iseconds              -> 2026-05-07T19:59:22+10:00
git status --short --branch -> ## main...origin/main
HEAD                        -> ba8a710 docs: add blk-system development roadmap
```

Relevant existing sprint/document state:

```text
docs/BLK-024_blk-system-development-roadmap.md
docs/plans/blk-system-019_active-doctrine-authority-overlay-cleanup.md
docs/outcomes/BLK-SYSTEM-019_sprint-closeout.md
docs/reviews/BLK-SYSTEM-019_post-remediation-hostile-review.md
```

Next-ID discovery:

```text
Latest existing system plan: docs/plans/blk-system-019_active-doctrine-authority-overlay-cleanup.md
Latest existing closeout:    docs/outcomes/BLK-SYSTEM-019_sprint-closeout.md
Selected sprint ID:          BLK-SYSTEM-020
Selected plan path:          docs/plans/blk-system-020_validation-command-profile-tightening.md
```

BLK-024 near-term source:

- Recommended near-term item 1 is **Validation command profile tightening**.
- Track D says validation commands are currently bounded, timed, and output-limited, but still payload-provided shell strings.
- Track D exit marker says a BEB should request validation by profile name and BLK-pipe should prove which exact commands ran without treating arbitrary shell text as trusted authority.

Current implementation surface observed during planning:

- `internal/contracts/payload.go` accepts `validation_commands []string` with count/size/empty checks only.
- `internal/validation/validation.go` executes each payload-provided command via `sh -c <command>` under bounded `execguard` execution.
- `internal/pipe/run.go` records deterministic `validation_NNN` logs and returns `SYNTAX_GATE_FAILED` on failed validation.
- `python/blk_pipe_adapter.py` forwards `validation_commands` into payload JSON.

---

## 1. Scope and Non-Goals

### In scope

1. Add repository-owned named validation profiles and unit tests for deterministic resolution.
2. Extend payload decoding/validation to support `validation_profiles` and reject invalid profile requests fail-closed before engine execution.
3. Preserve current validation execution guarantees: sequential execution, bounded output, per-command timeout behavior, deterministic `validation_NNN` log keys, validation-failure cleanup/revert, and exact-path staging.
4. Add report evidence showing profile source, requested profile names, and exact resolved commands so Hermes hostile audit can verify what ran.
5. Add minimal Python adapter support for profile payload fields without making Python the final authority.
6. Patch BLK-004/current doctrine gates to state that payload-provided `validation_commands` are transitional trusted-local compatibility, not future less-trusted/autonomous validation authority.
7. Close with a hostile self-review against BLK-001 through BLK-006 and BLK-024 Track D.

### Non-goals

This sprint must not implement or authorize:

- BLK-test production MCP or new live BLK-test smoke runs;
- arbitrary shell as BLK-test behavior;
- source mutation by BLK-test;
- protected BLK-req vault body reads, copying, parsing, hashing, or mutation;
- authoritative BEO publication, public ledger mutation, signer/storage/rollback authority;
- RTM generation, runtime `rtm_id`, RTM coverage matrices, or RTM drift rejection;
- Python adapter policy-layer hardening beyond profile-field compatibility;
- a complete BEB generator migration;
- package-manager, network, secret-reading, or broad host-inspection validation profiles;
- silent removal of existing trusted-local compatibility unless tests and doctrine explicitly account for the migration boundary.

---

## 2. BLK-001 through BLK-006 Alignment Matrix

| Governing doc | Required boundary | Sprint 020 treatment |
| --- | --- | --- |
| BLK-001 — Master Architecture | Preserve separation between BLK-req, Hermes planning, BLK-pipe mutation, BLK-test evidence, and blk-link trace closure. | Only BLK-pipe validation hardening changes. No BLK-test, BEO, or RTM authority is added. |
| BLK-002 — Artifact Lifecycle | Requirements/use-case staging, HITL approval, canonical hashes, and protected active vault isolation remain separate from tactical validation. | Profiles must not read protected BLK-req vault bodies or imply active-vault access. |
| BLK-003 — Orchestration Protocol | BEB/L2 packets, exact trace artifacts, bounded validation, POSIX routing, hostile audit, and failure ceilings remain explicit. | Profile names become the preferred BLK-native validation request shape; reports expose exact resolved commands for hostile audit. |
| BLK-004 — BLK-pipe V47 Suite | BLK-pipe is deterministic compiled authority; validation aborts must cleanly revert and report evidence. | Adds Go-owned profile registry and fail-closed payload validation while preserving sequential validation and cleanup semantics. |
| BLK-005 — BLK-Req Specification | Traceability remains atomic, hash-bound, and body-isolated. | No change to requirement/use-case schemas; validation profiles operate on source/build tests only. |
| BLK-006 — BLK-Req Implementation Brief | Protected vault hard-deny and staged revisions remain BLK-req/backend concerns, not tactical/validation authority. | Tests must prove profile work does not weaken protected path allowlist rejection or protected-vault body isolation. |

---

## 3. Controller Workflow for Each Task

For each task:

1. Preflight:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   git status --short --branch
   git log -1 --oneline
   ```
2. Read this task section and the governing docs named in it.
3. Use strict TDD where code changes are involved:
   - add/patch the failing focused test first;
   - run the focused test and capture RED;
   - implement only the scoped files;
   - rerun focused test and capture GREEN;
   - run shared verification.
4. Shared verification:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   go test ./...
   go vet ./...
   PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
   git diff --check
   ```
5. Remove generated Python cache before status/staging:
   ```bash
   python3 - <<'PY'
   from pathlib import Path
   import shutil
   for p in [Path('python/__pycache__'), Path('python/.pytest_cache'), Path('.pytest_cache')]:
       if p.exists():
           shutil.rmtree(p)
   PY
   ```
6. Write a task outcome doc under `docs/outcomes/` recording RED/GREEN evidence, exact changed paths, verification commands, and the non-execution statement.
7. Stage exact paths only. Do not use `git add .`, `git add -u`, broad globs, stash, reset, checkout, or broad pathspecs to manage task files.
8. Verify staged paths:
   ```bash
   git diff --cached --name-only
   ```
9. Commit with the task-specific message.
10. Push to `origin/main` after each task commit.

---

## 4. Task 0 — Commit Sprint Plan

**Objective:** Preserve this sprint plan as an in-repo executable contract before implementation begins.

**Files:**

- Create: `docs/plans/blk-system-020_validation-command-profile-tightening.md`
- Create: `docs/outcomes/BLK-SYSTEM-020_task-000-outcome.md`

**Steps:**

1. Verify the plan exists and contains required authority markers:
   ```bash
   test -f docs/plans/blk-system-020_validation-command-profile-tightening.md
   grep -F "Track D — Validation command profile tightening" docs/plans/blk-system-020_validation-command-profile-tightening.md
   grep -F "validation_profiles" docs/plans/blk-system-020_validation-command-profile-tightening.md
   grep -F "payload-provided `validation_commands` are transitional trusted-local compatibility" docs/plans/blk-system-020_validation-command-profile-tightening.md
   grep -F "does not authorize production BLK-test MCP" docs/plans/blk-system-020_validation-command-profile-tightening.md
   grep -F "does not authorize RTM generation" docs/plans/blk-system-020_validation-command-profile-tightening.md
   git diff --check -- docs/plans/blk-system-020_validation-command-profile-tightening.md
   ```
2. Create `docs/outcomes/BLK-SYSTEM-020_task-000-outcome.md` recording:
   - plan path;
   - BLK-024 Track D source;
   - current preflight status;
   - no implementation change;
   - non-execution statement.
3. Run shared verification.
4. Stage exact files:
   ```bash
   git add docs/plans/blk-system-020_validation-command-profile-tightening.md \
           docs/outcomes/BLK-SYSTEM-020_task-000-outcome.md
   git diff --cached --name-only
   ```
5. Commit and push:
   ```bash
   git commit -m "docs: plan blk-system sprint 020 validation profiles"
   git push origin main
   ```

---

## 5. Task 1 — Add RED Gates for Validation Profile Payload Contract

**Objective:** Prove the current payload contract lacks a profile-name validation path and lacks fail-closed checks for invalid profile requests.

**Files:**

- Modify: `internal/contracts/payload_test.go`
- Modify: `internal/contracts/report_test.go` if report JSON evidence tests already live there; otherwise create a focused report test in the same package.
- Create: `docs/outcomes/BLK-SYSTEM-020_task-001-outcome.md`

**Required RED tests:**

1. Decode accepts a V47 execute payload with:
   ```json
   "validation_profiles": ["go-full"]
   ```
   and preserves `ValidationProfiles` on the normalized payload.
2. Decode rejects unknown profiles, for example:
   ```json
   "validation_profiles": ["curl-production"]
   ```
3. Decode rejects mixed profile and free-form command authority:
   ```json
   "validation_profiles": ["go-full"],
   "validation_commands": ["go test ./..."]
   ```
4. Decode rejects duplicate profiles.
5. Decode preserves legacy `validation_commands` only as the explicit trusted-local compatibility path. The test name and comments must state this is not future less-trusted/autonomous authority.
6. Report JSON can expose enough validation profile evidence for hostile audit, at minimum:
   - requested profile names;
   - profile/legacy source marker;
   - exact resolved command array, when profiles were used.

**Focused RED commands:**

```bash
go test ./internal/contracts -run 'TestDecodePayload.*ValidationProfile|TestReport.*ValidationProfile' -count=1
```

**Expected RED:** missing `ValidationProfiles` field, unknown-profile checks, mixed-source rejection, duplicate rejection, and/or report evidence fields.

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-020_task-001-outcome.md` must record the RED output and confirm no production authority was granted.

**Commit message:**

```text
test: add validation profile payload contract gates
```

---

## 6. Task 2 — Implement Repository-Owned Validation Profile Registry

**Objective:** Add the minimal Go profile registry and payload validation/resolution needed to turn profile names into deterministic repository-owned command arrays.

**Files:**

- Create: `internal/validationprofiles/profiles.go`
- Create: `internal/validationprofiles/profiles_test.go`
- Modify: `internal/contracts/payload.go`
- Modify: `internal/contracts/payload_test.go`
- Modify: `internal/contracts/report.go`
- Modify: `internal/contracts/report_test.go` if present/needed
- Create: `docs/outcomes/BLK-SYSTEM-020_task-002-outcome.md`

**Profile registry requirements:**

Initial allowed profile set must be intentionally small and local-only:

| Profile | Resolved commands | Notes |
| --- | --- | --- |
| `go-test` | `go test ./...` | Local Go tests only. |
| `go-vet` | `go vet ./...` | Local Go vet only. |
| `go-full` | `go test ./...`; `go vet ./...` | Canonical Go full gate. |
| `python-unittest` | `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'` | Local Python unittest discovery only. |
| `docs-doctrine-gates` | `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v` | Active doctrine gate only. |

Registry constraints:

- No network commands.
- No package manager commands.
- No secret-reading, SSH-agent, token, environment dump, broad host-inspection, or destructive commands.
- No caller-provided command text inside profile resolution.
- Unknown names fail payload validation before engine execution.
- Duplicate names fail payload validation.
- Mixed `validation_profiles` and `validation_commands` fail payload validation unless a later sprint explicitly defines a migration field. Do not silently merge both.
- Resolved command arrays must be copied defensively so callers cannot mutate global registry state.

Payload/report requirements:

- `Payload` gains `ValidationProfiles []string` and a helper or resolved field that the pipe can use without reinterpreting unvalidated names.
- `Report` gains fields for requested validation profiles and exact resolved validation commands, or equivalent auditable evidence.
- Revert payloads continue to accept empty validation fields and must not require profiles.
- Legacy `validation_commands` remains accepted only when `validation_profiles` is empty. Tests and docs must identify it as trusted-local compatibility, not a future autonomous boundary.

**Focused GREEN commands:**

```bash
go test ./internal/validationprofiles ./internal/contracts -count=1
go test ./internal/contracts -run 'TestDecodePayload.*ValidationProfile|TestReport.*ValidationProfile|TestDecodePayload.*Legacy' -count=1
```

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-020_task-002-outcome.md` must record RED from Task 1, GREEN for the registry/contract tests, exact changed paths, and no-authority-expansion statement.

**Commit message:**

```text
feat: add validation profile registry and payload contract
```

---

## 7. Task 3 — Wire Profiles Through BLK-pipe Execution and Python Adapter Payloads

**Objective:** Ensure BLK-pipe actually runs resolved profile commands, reports the profile evidence, preserves cleanup semantics, and lets the Python adapter construct profile-based payloads.

**Files:**

- Modify: `internal/pipe/run.go`
- Modify: `internal/pipe/run_test.go`
- Modify: `internal/validation/validation.go` only if needed to preserve command-source evidence; do not weaken existing sequential/run bounds.
- Modify: `internal/validation/validation_test.go` only if needed for profile execution edge cases.
- Modify: `python/blk_pipe_adapter.py`
- Modify: `python/test_blk_pipe_adapter.py`
- Create: `docs/outcomes/BLK-SYSTEM-020_task-003-outcome.md`

**Required behavior:**

1. When `validation_profiles` is present, BLK-pipe must run the resolved command list from the Go registry, not payload-provided shell text.
2. Report output must identify profile source and exact resolved commands before returning success or validation failure.
3. Existing validation failure behavior must remain intact:
   - failed validation returns `SYNTAX_GATE_FAILED` / POSIX Exit 2;
   - candidate mutation is cleaned/reverted to the pre-engine hash;
   - validation logs remain deterministic `validation_NNN` keys;
   - validation output limits and timeout behavior still apply;
   - validation-created unauthorized mutations still return unauthorized mutation routing.
4. Python adapter adds a profile-aware invocation path, recommended API shape:
   ```python
   execute_sprint(..., validation_profiles: list[str] | None = None, validation_commands: list[str] | None = None, ...)
   ```
   The adapter must not silently send both fields. If both are supplied, it should fail locally before invoking `blk-pipe`.
5. Python adapter changes are compatibility-only. The Go binary remains final enforcement authority.

**Focused RED/GREEN command examples:**

```bash
go test ./internal/pipe -run 'TestRun.*ValidationProfile|TestRun.*ValidationFailure' -count=1
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_pipe_adapter -v
```

**Shared GREEN commands:**

```bash
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
```

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-020_task-003-outcome.md` must record RED/GREEN evidence, profile-report sample keys, and no production BLK-test/BEO/RTM authority.

**Commit message:**

```text
feat: run validation profiles through blk-pipe
```

---

## 8. Task 4 — Patch Doctrine and Persistent Review Gates

**Objective:** Make active doctrine accurately describe the new profile boundary and prevent future docs from treating free-form validation shell as broader autonomous authority.

**Files:**

- Modify: `docs/BLK-004_blk-pipe-v47-architecture-suite.md`
- Modify: `python/test_active_doctrine_review_gates.py`
- Create: `docs/outcomes/BLK-SYSTEM-020_task-004-outcome.md`

**Doctrine requirements:**

Patch BLK-004 current-state overlay and validation sections to state:

- BLK-pipe supports repository-owned named `validation_profiles`.
- Profile names resolve to deterministic command arrays owned by the repository.
- Reports expose exact resolved commands for hostile audit.
- Free-form `validation_commands` are transitional trusted-local compatibility only.
- Less-trusted/autonomous payload boundaries must use profiles or a later explicit human-reviewed doctrine exception.
- Profiles do not authorize network, package-manager, secret-reading, protected BLK-req body reads, BLK-test production MCP, BEO publication, RTM generation, or arbitrary shell as BLK-test behavior.
- Python adapter profile support is convenience/payload construction only; Go remains the enforcement authority.

**Persistent gate requirements:**

Add a focused Python doctrine gate, recommended name:

```text
test_sprint020_validation_profile_boundary_preserves_go_authority
```

The gate should verify required markers in `docs/BLK-004_blk-pipe-v47-architecture-suite.md`, including:

```text
validation_profiles
repository-owned named validation profiles
exact resolved commands
transitional trusted-local compatibility
less-trusted/autonomous payload boundaries must use profiles
Go remains the enforcement authority
```

**RED command:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
```

**Expected RED:** missing Sprint 020 profile-boundary markers in BLK-004.

**GREEN/shared commands:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-020_task-004-outcome.md` must record RED/GREEN doctrine-gate evidence and confirm no BLK-test/BEO/RTM/protected-vault authority expansion.

**Commit message:**

```text
docs: define validation profile authority boundary
```

---

## 9. Task 5 — Hostile Self-Review and Sprint Closeout

**Objective:** Verify the completed sprint against BLK-024 Track D, BLK-001 through BLK-006, and the authority boundaries in this plan.

**Files:**

- Create: `docs/reviews/BLK-SYSTEM-020_post-remediation-hostile-review.md`
- Create: `docs/outcomes/BLK-SYSTEM-020_sprint-closeout.md`
- Create: `docs/outcomes/BLK-SYSTEM-020_task-005-outcome.md`

**Hostile review checklist:**

1. Does any code path still treat payload-provided arbitrary shell as the preferred future/autonomous validation boundary?
2. Are `validation_profiles` resolved only from repository-owned command arrays?
3. Are unknown, duplicate, or mixed profile/command requests rejected fail-closed before engine execution?
4. Does BLK-pipe report exact resolved commands for profile-based validation?
5. Did validation failure routing remain `SYNTAX_GATE_FAILED` with cleanup/revert semantics intact?
6. Did protected BLK-req vault allowlist rejection remain Exit 3 / unauthorized mutation and body-isolated?
7. Did Python adapter support remain a convenience layer rather than final authority?
8. Did the sprint avoid production BLK-test MCP, new live smoke runs, arbitrary shell as BLK-test, protected-vault body reads, authoritative BEO publication, RTM generation, and drift authority?
9. Are follow-up candidates separated cleanly, especially Python adapter policy hardening and BEB generator migration?

**Verification commands:**

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
git status --short --branch
```

**Closeout requirements:**

`docs/outcomes/BLK-SYSTEM-020_sprint-closeout.md` must include:

- final commit table for task commits;
- summary of profile registry and payload/report evidence;
- final verification output;
- non-execution statement;
- no-authority-expansion statement;
- residual/next-sprint seeds.

Likely next-sprint seeds after closeout:

- BLK-SYSTEM-021 Python adapter policy-layer hardening (BLK-024 Track E);
- BEB generator/profile migration if any trusted-local payload producers still emit `validation_commands`;
- later explicit removal or stricter gating of legacy free-form validation commands after all approved producers migrate.

**Staging and commit:**

```bash
git add docs/reviews/BLK-SYSTEM-020_post-remediation-hostile-review.md \
        docs/outcomes/BLK-SYSTEM-020_task-005-outcome.md \
        docs/outcomes/BLK-SYSTEM-020_sprint-closeout.md
git diff --cached --name-only
git commit -m "docs: close blk-system sprint 020 validation profiles"
git push origin main
```

---

## 10. Acceptance Criteria

BLK-SYSTEM-020 is complete only if all criteria below pass:

1. `validation_profiles` is supported in the Go payload contract.
2. Unknown, duplicate, and mixed profile/free-form validation requests fail closed before engine execution.
3. Repository-owned profile resolution is covered by focused Go tests.
4. Profile-based execution runs exact resolved commands and reports profile evidence.
5. Existing validation failure, output limit, timeout, cleanup, and exact-path staging behavior remains covered by tests.
6. Python adapter can construct profile payloads and refuses to send both profiles and commands in one request.
7. BLK-004 and persistent doctrine gates preserve the profile authority boundary.
8. Full verification passes:
   ```bash
   go test ./...
   go vet ./...
   PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
   git diff --check
   ```
9. Every task has an outcome doc under `docs/outcomes/`.
10. Hostile self-review and sprint closeout are committed and pushed.

---

## 11. Non-Execution and No-Authority-Expansion Statement

This plan does not authorize Hindsight use, Codex use, live tactical LLM execution, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads, copying, parsing, hashing, or mutation, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, or source mutation outside exact approved allowlists.

The intended authority movement is only a reduction of validation-command ambiguity: future BLK-native payloads can request validation by repository-owned profile names, and BLK-pipe can report the exact commands it ran for hostile audit.
