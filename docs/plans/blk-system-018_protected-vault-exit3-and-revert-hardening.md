# BLK-SYSTEM-018 — Protected-Vault Exit 3 and Revert Emergency-Path Hardening Plan

> **For Hermes:** Use `blk-system-sprint-execution`, `test-driven-development`, and two-stage hostile review for every implementation task. Implement task-by-task with strict RED/GREEN evidence. Commit and push after each task outcome. Do not use Hindsight. Do not run live Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, RTM generation, RTM authority, or authoritative BEO publication.

**Goal:** Remediate the two immediate blocking implementation findings from the current BLK-001 through BLK-006 hostile alignment review: protected BLK-req vault allowlist hits must route as POSIX Exit 3, and BLK-pipe revert must remain reachable from dirty/broken workspaces.

**Architecture:** This sprint is a surgical BLK-pipe blast-shield hardening sprint. It preserves current authority boundaries while correcting POSIX routing and emergency-revert sequencing in the compiled Go path. It does not expand BLK-test, BEO, RTM, approval, or live execution authority.

**Tech Stack:** Go 1.26.x via `$HOME/.local/bin`, Go standard library, existing BLK-System Python unittest gates, Markdown review/outcome docs, Git CLI.

---

## 0. Current Known State

Planning preflight captured before writing this plan:

```text
date -Iseconds             -> 2026-05-07T17:28:02+10:00
git status --short --branch -> ## main...origin/main
HEAD                       -> 023c309 docs: review blk-system alignment with blk-001 through blk-006
```

Source review artifact:

```text
docs/reviews/BLK-SYSTEM_current-implementation_BLK-001-through-BLK-006_hostile-alignment-review.md
```

Review findings owned by this sprint:

- `BLOCKING-1` — protected BLK-req vault allowlist violations route as Exit 2 instead of BLK-006 Exit 3.
- `BLOCKING-2` — `revert` recovery is blocked by normal clean-preflight checks.

Review findings explicitly **not** owned by this sprint:

- `BLOCKING-3` doctrine contradiction around BLK-020 first-smoke authority. That belongs in a follow-up doctrine cleanup sprint, currently seeded as `BLK-SYSTEM-019`.
- Validation command profile tightening.
- Python adapter policy-layer clarification.
- BEO terminology normalization.

---

## 1. Scope and Non-Goals

### In scope

1. Add Go regression tests proving protected `docs/active/`, `docs/requirements/`, and `docs/use_cases/` allowlist entries return:
   - POSIX Exit 3 (`ExitUnauthorizedMutation`),
   - report status `UNAUTHORIZED_FILE_MUTATION`,
   - no engine execution,
   - no protected body reads,
   - no workspace residue.
2. Patch BLK-pipe payload/run routing so protected vault allowlist validation maps to Exit 3 while ordinary malformed payloads remain Exit 2.
3. Add Go regression tests proving valid revert can execute even when the workspace contains dirty tracked changes, untracked files, ignored files, and nested `.git` residue.
4. Patch BLK-pipe run ordering so `Action == "revert"` reaches `runRevert(...)` before execute-mode clean-preflight while still preserving target branch/hash/ancestry validation.
5. Document every task outcome under `docs/outcomes/BLK-SYSTEM-018_*`.
6. Close the sprint with a hostile self-review against BLK-001 through BLK-006 and the source review report.

### Non-goals

This sprint must not implement or authorize:

- live Codex or live tactical LLM execution;
- production BLK-test MCP;
- new live BLK-test MCP smoke runs;
- network model service calls;
- cyber tooling;
- BLK-req vault body reads, copying, parsing, or mutation;
- RTM generation, `generate_rtm.py`, runtime `rtm_id`, RTM drift authority, or coverage matrices;
- authoritative BEO publication;
- validation command profile redesign;
- Python adapter policy hardening;
- BLK-003/BLK-017/BLK-020 doctrine cleanup beyond outcome references.

---

## 2. BLK-001 through BLK-006 Alignment Matrix

| Domain | Required boundary | Sprint 018 treatment |
| --- | --- | --- |
| `blk-req` Legislative Gateway | Protected vault paths under `docs/active/`, `docs/requirements/`, and `docs/use_cases/` must not be mutated or read by tactical/probe code. | Strengthens blast-shield routing for allowlist hits. No protected body reads are introduced. |
| Architecture & Feature Planning | Hermes owns scoped planning and review; BLK-pipe must not become planner/router. | No planning authority moves into BLK-pipe. Code changes only classify existing payload boundary violations. |
| `blk-pipe` Blast Shield & Forge | Owns source mutation, staging, Git allowlists, POSIX statuses, and emergency recovery. | Corrects Exit 3 routing and ensures emergency revert remains reachable. |
| `blk-test` Physics Oracle | Must not stage, commit, mutate source, read protected vault bodies, publish BEOs, or generate RTM. | No BLK-test runtime or doctrine authority changes. |
| `blk-link` Ledger / RTM | Offline RTM authority remains separate; no hidden RTM generation or drift rejection. | No RTM code or runtime fields are introduced. |
| Cryptographic baton | `version_hash` / canonical `trace_artifacts` must not be weakened. | Existing trace-artifact tests remain in force; this sprint does not alter baton semantics. |

---

## 3. Controller Workflow for Each Task

For each task:

1. Preflight:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   git status --short --branch
   git log -1 --oneline
   ```
2. Read this plan task section and the source review section it references.
3. Use strict TDD:
   - write/patch the failing test first;
   - run the focused test and capture RED;
   - patch minimal implementation/docs;
   - rerun the focused test and capture GREEN;
   - run shared verification.
4. Shared verification for implementation tasks:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
   go test ./...
   go vet ./...
   git diff --check
   ```
5. Remove generated cache before status/staging. If shell cleanup hangs, use Python cleanup:
   ```bash
   python3 - <<'PY'
   from pathlib import Path
   import shutil
   for p in [Path('python/__pycache__'), Path('python/.pytest_cache'), Path('.pytest_cache')]:
       if p.exists():
           shutil.rmtree(p)
   PY
   ```
6. Write a task outcome doc under `docs/outcomes/` with RED/GREEN evidence, shared verification, exact changed paths, and non-execution statement.
7. Stage exact paths only. Do not use `git add .` or `git add -u`.
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

- Create: `docs/plans/blk-system-018_protected-vault-exit3-and-revert-hardening.md`
- Create: `docs/outcomes/BLK-SYSTEM-018_task-000-outcome.md`

**Steps:**

1. Verify the plan exists and contains required scope markers:
   ```bash
   test -f docs/plans/blk-system-018_protected-vault-exit3-and-revert-hardening.md
   grep -F "BLOCKING-1" docs/plans/blk-system-018_protected-vault-exit3-and-revert-hardening.md
   grep -F "BLOCKING-2" docs/plans/blk-system-018_protected-vault-exit3-and-revert-hardening.md
   grep -F "BLK-SYSTEM-019" docs/plans/blk-system-018_protected-vault-exit3-and-revert-hardening.md
   git diff --check
   ```
2. Create `docs/outcomes/BLK-SYSTEM-018_task-000-outcome.md` recording:
   - plan path;
   - review source path;
   - preflight status;
   - no implementation change;
   - non-execution statement.
3. Run shared verification. For this docs-only task, `go test ./...`, `go vet ./...`, Python unittest discovery, and `git diff --check` are sufficient.
4. Stage exact files:
   ```bash
   git add docs/plans/blk-system-018_protected-vault-exit3-and-revert-hardening.md \
           docs/outcomes/BLK-SYSTEM-018_task-000-outcome.md
   git diff --cached --name-only
   ```
5. Commit and push:
   ```bash
   git commit -m "docs: plan blk-system sprint 018 hardening"
   git push
   ```

---

## 5. Task 1 — Add RED Tests for Protected Vault Allowlist Exit 3 Routing

**Objective:** Prove protected BLK-req vault allowlist entries currently fail the BLK-006 POSIX route by returning Exit 2 instead of Exit 3.

**Source finding:** `BLOCKING-1` in `docs/reviews/BLK-SYSTEM_current-implementation_BLK-001-through-BLK-006_hostile-alignment-review.md`.

**Files:**

- Modify: `internal/pipe/run_test.go`
- Create: `docs/outcomes/BLK-SYSTEM-018_task-001-outcome.md`

**Test design:**

Add table-driven tests near existing allowlist/preflight tests in `internal/pipe/run_test.go`.

Suggested test names:

- `TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation`
- `TestRunProtectedVaultAllowlistDoesNotStartEngine`

Minimum cases:

| Case | Payload field | Path |
| --- | --- | --- |
| active modified | `AllowedModifiedFiles` | `docs/active/REQ-001.md` |
| requirements modified | `AllowedModifiedFiles` | `docs/requirements/REQ-001.md` |
| use-cases new | `AllowedNewFiles` | `docs/use_cases/UC-001.md` |
| active new | `AllowedNewFiles` | `docs/active/UC-001.md` |

Each case must use a sentinel engine command that would create a file if executed, for example:

```go
EngineCommand: []string{"sh", "-c", "printf ran > engine-ran.txt"},
```

Required assertions:

```go
if exitCode != ExitUnauthorizedMutation {
    t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitUnauthorizedMutation, report)
}
if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
    t.Fatalf("status = %q, want UNAUTHORIZED_FILE_MUTATION", report.Status)
}
if !strings.Contains(report.Error, "protected") {
    t.Fatalf("error = %q, want protected vault marker", report.Error)
}
if _, err := os.Stat(filepath.Join(repo, "engine-ran.txt")); !os.IsNotExist(err) {
    t.Fatalf("engine appears to have run; stat err=%v", err)
}
assertClean(t, repo)
```

**RED command:**

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestRunProtectedVaultAllowlist' -count=1 -v
```

**Expected RED:**

The focused test must fail because the current code returns Exit 2 / `INVALID_PAYLOAD`, not Exit 3 / `UNAUTHORIZED_FILE_MUTATION`.

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-018_task-001-outcome.md` must record:

- test names added;
- RED command and failure excerpt;
- exact finding source;
- no implementation changed yet;
- non-execution statement.

**Commit:**

```bash
git add internal/pipe/run_test.go docs/outcomes/BLK-SYSTEM-018_task-001-outcome.md
git commit -m "test: expose protected vault exit routing gap"
git push
```

---

## 6. Task 2 — Route Protected Vault Allowlist Hits to Exit 3

**Objective:** Patch BLK-pipe so protected BLK-req vault allowlist hits return Exit 3 while ordinary malformed payloads still return Exit 2.

**Files:**

- Modify: `internal/contracts/payload.go`
- Modify: `internal/pipe/run.go`
- Modify: `internal/pipe/run_test.go` only if Task 1 tests need minor expected-message adjustment; do not weaken assertions.
- Create: `docs/outcomes/BLK-SYSTEM-018_task-002-outcome.md`

**Implementation guidance:**

Use the smallest design that preserves existing validation semantics and gives `internal/pipe` a reliable classifier.

Acceptable pattern:

1. Add an exported predicate/helper in `internal/contracts/payload.go`, for example:
   ```go
   func IsProtectedDocsPath(entry string) bool { ... }
   func ProtectedDocsPrefix(entry string) string { ... }
   func HasProtectedDocsAllowlistEntry(p Payload) (field string, entry string, prefix string, ok bool) { ... }
   ```
   Keep the existing unexported helpers as wrappers if needed, or update internal callers to the exported helpers.
2. In `parseAndValidatePayload(...)`, when `DecodePayload(...)` returns an error, inspect any partially decoded payload allowlists already populated in `payload`. If a protected docs allowlist entry is present, return:
   - `report.Status = "UNAUTHORIZED_FILE_MUTATION"`
   - `report.Error` containing field name and protected prefix, without reading file bodies
   - `ExitUnauthorizedMutation`
3. Ordinary payload errors must remain:
   - `report.Status = "INVALID_PAYLOAD"`
   - `ExitInvalidPayload`

**Important guardrails:**

- Do not remove protected-path validation from `contracts.Payload.Validate()` unless all existing contract tests are deliberately updated and still prove protected paths are rejected.
- Do not read protected files to classify the error. Classification must use path strings only.
- Do not spawn the engine for protected allowlist payloads.
- Do not broaden allowlist semantics.

**GREEN command:**

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestRunProtectedVaultAllowlist' -count=1 -v
```

**Regression command:**

```bash
go test ./internal/contracts ./internal/pipe -count=1
```

**Shared verification:**

Run the full shared verification from §3.

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-018_task-002-outcome.md` must record:

- Task 1 RED evidence reference;
- GREEN focused test output;
- full shared verification;
- exact files changed;
- statement that protected body reads were not introduced;
- statement that ordinary malformed payloads still route as Exit 2.

**Commit:**

```bash
git add internal/contracts/payload.go \
        internal/pipe/run.go \
        internal/pipe/run_test.go \
        docs/outcomes/BLK-SYSTEM-018_task-002-outcome.md
git commit -m "fix: route protected vault allowlists as unauthorized mutations"
git push
```

---

## 7. Task 3 — Add RED Tests for Revert Reachability from Dirty Workspaces

**Objective:** Prove valid revert currently fails before reset/clean when ordinary execute-mode clean-preflight sees workspace residue.

**Source finding:** `BLOCKING-2` in `docs/reviews/BLK-SYSTEM_current-implementation_BLK-001-through-BLK-006_hostile-alignment-review.md`.

**Files:**

- Modify: `internal/pipe/run_test.go`
- Create: `docs/outcomes/BLK-SYSTEM-018_task-003-outcome.md`

**Test design:**

Add tests near existing revert tests around `TestRunRevertSuccessResetsToVerifiedAncestorAndCleans`.

Suggested test names:

- `TestRunRevertBypassesCleanPreflightForDirtyTrackedWorkspace`
- `TestRunRevertBypassesCleanPreflightForUntrackedAndIgnoredResidue`
- Replace or invert the existing `TestRunRevertPreExistingNestedGitRepositoryExitsSevenBeforeReset` expectation with `TestRunRevertCleansPreExistingNestedGitRepositoryAfterValidAnchor` if hostile review scope chooses nested `.git` residue as emergency-cleanable residue.

Required dirty tracked case:

1. Use `twoCommitRepo(t)`.
2. Modify a tracked file without committing.
3. Invoke revert to the first commit.
4. Assert `ExitSuccess`, `report.Status == "SUCCESS"`, `HEAD == targetHash`, and workspace clean.

Required untracked/ignored case:

1. Use `twoCommitRepo(t)`.
2. Create an untracked file, an ignored file, and a `.gitignore` rule as needed.
3. Invoke revert to the first commit.
4. Assert both residues are removed and workspace is clean.

Nested `.git` case decision:

- If keeping nested `.git` rejection is judged safer than emergency cleanup, document that deviation explicitly in the Task 3 outcome and keep the existing Exit 7 test.
- If following the hostile review strictly, update the test to prove a valid revert removes nested `.git` residue through `git clean -ffdx` after hash/branch/ancestry validation.
- Do not silently preserve the old Exit 7 behavior without rationale.

**RED command:**

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestRunRevert(BypassesCleanPreflight|CleansPreExistingNestedGitRepository)' -count=1 -v
```

**Expected RED:**

The focused tests should fail because `run(...)` calls `cleanPreflight(...)` before `runRevert(...)`, producing `ExitGitDirty` or equivalent preflight rejection before reset/clean.

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-018_task-003-outcome.md` must record:

- RED failure excerpts;
- whether nested `.git` is intentionally remediated or explicitly deferred with rationale;
- no implementation changed yet;
- non-execution statement.

**Commit:**

```bash
git add internal/pipe/run_test.go docs/outcomes/BLK-SYSTEM-018_task-003-outcome.md
git commit -m "test: expose revert preflight reachability gap"
git push
```

---

## 8. Task 4 — Make Revert Reachable Before Execute-Mode Clean Preflight

**Objective:** Patch BLK-pipe so valid `Action == "revert"` payloads reach verified reset/clean even when the workspace has dirty/untracked/ignored residue.

**Files:**

- Modify: `internal/pipe/run.go`
- Modify: `internal/pipe/run_test.go` only if Task 3 tests need minor expected-message adjustment; do not weaken assertions.
- Create: `docs/outcomes/BLK-SYSTEM-018_task-004-outcome.md`

**Implementation guidance:**

Current flow:

```go
payload, exitCode := parseAndValidatePayload(payloadJSON, report)
...
baselineUntracked, exitCode := cleanPreflight(payload.Workdir, report)
...
if payload.Action == "revert" {
    return runRevert(payload, report)
}
```

Required flow:

```go
payload, exitCode := parseAndValidatePayload(payloadJSON, report)
if exitCode != ExitSuccess {
    return exitCode
}
if payload.Action == "revert" {
    return runRevert(payload, report)
}
baselineUntracked, exitCode := cleanPreflight(payload.Workdir, report)
...
```

Keep these protections intact:

- `parseAndValidatePayload(...)` still validates payload shape.
- `runRevert(...)` still verifies target branch when supplied.
- `runRevert(...)` still verifies target commit is a full object ID for the repository.
- `runRevert(...)` still verifies target hash is an ancestor of `HEAD`.
- Invalid revert anchors still return `ExitInvalidRevertAnchor` and must not reset.
- Execute-mode preflight behavior remains unchanged.

**GREEN command:**

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestRunRevert(BypassesCleanPreflight|CleansPreExistingNestedGitRepository|InvalidAnchor|WithTargetBranch|SHA256)' -count=1 -v
```

**Regression command:**

```bash
go test ./internal/pipe -count=1
```

**Shared verification:**

Run the full shared verification from §3.

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-018_task-004-outcome.md` must record:

- Task 3 RED evidence reference;
- GREEN focused test output;
- full shared verification;
- exact changed files;
- statement that invalid anchors remain protected;
- statement that execute-mode clean preflight remains unchanged.

**Commit:**

```bash
git add internal/pipe/run.go \
        internal/pipe/run_test.go \
        docs/outcomes/BLK-SYSTEM-018_task-004-outcome.md
git commit -m "fix: allow verified revert before execute preflight"
git push
```

---

## 9. Task 5 — Add Persistent Review Gates and Active Doctrine Cross-References

**Objective:** Add documentation gates proving the sprint report and active doctrine preserve the hardened BLK-001 through BLK-006 boundary without broadening authority.

**Files:**

- Modify: `python/test_active_doctrine_review_gates.py`
- Modify: `docs/BLK-006_blk-req-implementation-brief.md`
- Modify: `docs/BLK-004_blk-pipe-v47-architecture-suite.md` only if needed to cross-reference emergency revert ordering.
- Create: `docs/outcomes/BLK-SYSTEM-018_task-005-outcome.md`

**Gate design:**

Add one or more focused gates asserting that active doctrine contains markers for:

- `protected BLK-req vault allowlist violations return POSIX Exit 3`
- `UNAUTHORIZED_FILE_MUTATION`
- `revert bypasses execute-mode clean preflight only after target hash validation`
- `target_hash` / `sprint_base_hash`
- `does not authorize BLK-req vault body reads`
- `does not authorize live BLK-test MCP`
- `does not authorize authoritative BEO publication`
- `does not authorize RTM generation`

**RED command:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
```

Expected RED: missing new Sprint 018 boundary markers in active doctrine.

**Patch guidance:**

Patch only current active doctrine sections needed to record the corrected boundary. Do not rewrite historical reviews/outcomes.

Recommended docs patches:

1. `docs/BLK-006_blk-req-implementation-brief.md`
   - Clarify that protected vault allowlist hits are authority violations and must surface as `UNAUTHORIZED_FILE_MUTATION` / POSIX Exit 3, not generic invalid payload.
2. `docs/BLK-004_blk-pipe-v47-architecture-suite.md`
   - Clarify that verified emergency revert is a recovery path and must not be blocked by execute-mode clean preflight, but must retain target hash/branch/ancestry validation.

**GREEN command:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
```

**Shared verification:**

Run the full shared verification from §3.

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-018_task-005-outcome.md` must record:

- RED/GREEN doctrine gate evidence;
- exact doctrine sections patched;
- explicit no-authority-expansion statement;
- full shared verification.

**Commit:**

```bash
git add python/test_active_doctrine_review_gates.py \
        docs/BLK-006_blk-req-implementation-brief.md \
        docs/BLK-004_blk-pipe-v47-architecture-suite.md \
        docs/outcomes/BLK-SYSTEM-018_task-005-outcome.md
git commit -m "docs: gate blk-system sprint 018 authority boundaries"
git push
```

If `docs/BLK-004_blk-pipe-v47-architecture-suite.md` does not need a patch after inspection, omit it from staging and record the omission rationale in the outcome.

---

## 10. Task 6 — Sprint Closeout and Hostile Self-Review

**Objective:** Close BLK-SYSTEM-018 with an evidence-backed sprint closeout proving the two immediate blockers were remediated and no authority expanded.

**Files:**

- Create: `docs/reviews/BLK-SYSTEM-018_post-remediation-hostile-review.md`
- Create: `docs/outcomes/BLK-SYSTEM-018_sprint-closeout.md`

**Hostile self-review requirements:**

`docs/reviews/BLK-SYSTEM-018_post-remediation-hostile-review.md` must verify:

1. Protected vault allowlist hits now return Exit 3 and `UNAUTHORIZED_FILE_MUTATION`.
2. Ordinary malformed payloads still return Exit 2 / `INVALID_PAYLOAD`.
3. Protected vault body reads are not introduced.
4. Engine execution does not start for protected allowlist hits.
5. Valid revert can run from dirty/untracked/ignored residue after target validation.
6. Invalid revert anchors still fail and do not reset.
7. Execute-mode clean preflight remains in force.
8. No live BLK-test MCP, BEO publication, or RTM authority was introduced.
9. `BLK-SYSTEM-019` remains the follow-up owner for doctrine contradiction cleanup around BLK-020.

**Closeout requirements:**

`docs/outcomes/BLK-SYSTEM-018_sprint-closeout.md` must include:

- final commit table for Tasks 0-6;
- source review path;
- before/after summary for `BLOCKING-1` and `BLOCKING-2`;
- final verification evidence;
- explicit non-execution statement;
- next-sprint seed for `BLK-SYSTEM-019 — Active doctrine authority overlay cleanup`.

**Final verification commands:**

```bash
export PATH="$HOME/.local/bin:$PATH"
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

**Cleanup/status:**

Use Python cache cleanup if needed, then:

```bash
git status --short --branch
git diff --cached --name-only
```

**Commit:**

```bash
git add docs/reviews/BLK-SYSTEM-018_post-remediation-hostile-review.md \
        docs/outcomes/BLK-SYSTEM-018_sprint-closeout.md
git commit -m "docs: close out blk-system sprint 018"
git push
```

---

## 11. Final Sprint Acceptance Criteria

BLK-SYSTEM-018 is complete only when all criteria are true:

1. Protected allowlist entries under `docs/active/`, `docs/requirements/`, and `docs/use_cases/` route to Exit 3.
2. Protected allowlist reports use `UNAUTHORIZED_FILE_MUTATION`.
3. Protected allowlist reports do not require or perform protected body reads.
4. Engine execution is skipped for protected allowlist payloads.
5. Ordinary malformed payloads still route to Exit 2.
6. Valid revert executes from dirty tracked workspaces.
7. Valid revert executes from untracked/ignored residue workspaces.
8. Nested `.git` revert behavior is either remediated or explicitly deferred with rationale and user-visible evidence.
9. Invalid target hash/branch/ancestry still prevents revert reset.
10. Execute-mode clean preflight remains enforced for non-revert execution.
11. Active doctrine records the Exit 3 and emergency-revert boundaries.
12. Python unittest discovery passes.
13. `go test ./...` passes.
14. `go vet ./...` passes.
15. `git diff --check` passes.
16. Task outcomes exist for every task.
17. Sprint closeout and hostile self-review exist.
18. All task commits are pushed to `origin/main`.
19. No live BLK-test MCP, RTM generation, RTM authority, or authoritative BEO publication was introduced.
20. Follow-up `BLK-SYSTEM-019` remains explicitly scoped to doctrine cleanup, not implementation hardening.

---

## 12. Quick Resume Prompt for Future Hermes

Open `/home/dad/BLK-System/docs/plans/blk-system-018_protected-vault-exit3-and-revert-hardening.md`. Execute the next incomplete task using `blk-system-sprint-execution`, strict TDD, exact-path staging, per-task outcome docs, and push after each task. Source review is `docs/reviews/BLK-SYSTEM_current-implementation_BLK-001-through-BLK-006_hostile-alignment-review.md`. Sprint owns only BLOCKING-1 and BLOCKING-2. Do not broaden into BLK-SYSTEM-019 doctrine cleanup, validation command redesign, Python adapter policy hardening, live BLK-test MCP, RTM generation, or authoritative BEO publication.
