# BLK-pipe Sprint 002 — Task 7 Outcome

**Status:** Complete
**Date:** 2026-05-03
**Task:** Task 7 — Add Sequential Validation Command Gate
**Commit:** `2168a4f feat: add blk-pipe validation gate`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Task 7 added BLK-004/V47 sequential validation command support to the deterministic BLK-pipe kernel.

The objective was to run payload-provided `validation_commands` after successful engine execution and after `.git` mutation audit, but before allowlist staging and commit. Validation logs must be captured deterministically, validation failure must restore the repository to `PreEngineHash`, and validation must never run after detected `.git` metadata mutation.

---

## 2. Files Added/Changed

Implementation commit `2168a4f` changed:

- `internal/validation/validation.go`
  - New bounded sequential validation runner.
  - Uses `execguard.Run` with `execguard.ScrubbedEnv`.
  - Produces deterministic log keys such as `validation_001`.
  - Runs every validation command before evaluating failure.
  - Caps aggregate retained validation logs to `max_output_bytes`.
- `internal/validation/validation_test.go`
  - Sequential execution, deterministic log, failure aggregation, aggregate log cap, and environment scrub tests.
- `internal/contracts/payload.go`
  - Added `validation_commands` to payload decoding/normalization.
  - Rejects blank validation commands.
- `internal/contracts/payload_test.go`
  - Added payload coverage for validation commands.
- `internal/pipe/run.go`
  - Integrated validation between engine execution / `.git` audit and staging / commit.
  - Added pre-validation and post-validation `.git` mutation denial paths.
  - Added rollback/cleanup behavior for validation failure.
  - Hardened `.git` snapshot restoration for unsupported entries and path-kind replacements.
- `internal/pipe/run_test.go`
  - Added pipe-level validation success/failure tests.
  - Added `.git` mutation-before-validation and validation-induced `.git` mutation regressions.
  - Added unsupported `.git` entry and existing directory replacement regressions.

Commit stat:

```text
internal/contracts/payload.go          |  17 ++
internal/contracts/payload_test.go     |  14 ++
internal/pipe/run.go                   | 132 ++++++++++--
internal/pipe/run_test.go              | 366 ++++++++++++++++++++++++++++++++-
internal/validation/validation.go      |  88 ++++++++
internal/validation/validation_test.go | 158 ++++++++++++++
6 files changed, 753 insertions(+), 22 deletions(-)
```

---

## 3. Behavior Implemented

### 3.1 Payload contract

`validation_commands` are now decoded from both V47-compatible payloads and legacy-normalized payload execution paths. Blank entries are invalid payload data.

### 3.2 Sequential validation runner

The new `internal/validation` package runs validation commands sequentially in the payload workdir. Each command is executed through the bounded `execguard.Run` helper with the same scrubbed environment baseline used for bounded subprocess execution.

Validation logs are keyed deterministically:

```text
validation_001
validation_002
validation_003
```

The runner intentionally does not short-circuit after the first failure. All commands run, logs are aggregated, and failure is evaluated after completion, matching BLK-004's sequential aggregation rule.

### 3.3 Aggregate log cap

Review caught that per-command output caps could still retain `N * max_output_bytes` across `N` validation commands. The final implementation applies an aggregate retained-log budget across all validation logs while still running all commands and detecting failures.

### 3.4 Pipe orchestration integration

The pipe execution order now includes:

1. clean preflight,
2. capture `PreEngineHash`,
3. engine execution,
4. `.git` mutation audit before validation,
5. validation command execution,
6. `.git` mutation audit after validation,
7. strict allowlist staging,
8. unauthorized cleanup,
9. commit gate and commit.

### 3.5 Validation failure behavior

If any validation command fails, BLK-pipe now:

- preserves validation logs in the report,
- restores the repository to `PreEngineHash`,
- cleans unauthorized files,
- returns status `SYNTAX_GATE_FAILED`,
- exits with `ExitValidationFailed` / code `2`,
- does not stage or commit.

### 3.6 `.git` mutation hardening

Validation must not run after engine-created `.git` metadata mutation, and validation-created `.git` mutation must not reach staging/commit. Task 7 now denies both.

Review also found a deeper restore hole: unsupported `.git` entries such as FIFOs, or existing `.git` directories replaced by unsupported entries, could break restoration and leave dirty worktrees. The final implementation hardens `.git` snapshot restoration to remove current paths that are new or have a changed kind before recreating snapshot entries.

Regression coverage includes:

- engine mutates `.git/hooks/post-commit` before validation,
- validation mutates `.git/hooks/post-commit`,
- engine creates unsupported `.git` FIFO,
- validation creates unsupported `.git` FIFO,
- engine replaces existing `.git/hooks` directory with FIFO,
- validation replaces existing `.git/refs` directory with FIFO.

---

## 4. TDD Evidence

### 4.1 RED

Implementation and fix subagents added tests before production changes and observed expected failures.

Initial Task 7 RED evidence:

```text
go test ./internal/validation -v
FAIL: undefined validation Run implementation

go test ./internal/contracts ...
FAIL: unknown field ValidationCommands

go test ./internal/pipe -run 'TestRun.*Validation|TestRun.*Git.*Validation' -v
FAIL: unknown field ValidationCommands
```

First review-fix RED evidence:

```text
TestRunRetainsAggregateLogsWithinMaxOutputBytesAndStillRunsAllCommands
FAIL: retained validation logs exceeded aggregate cap

TestRunValidationGitHookMutationIsUnauthorizedRestoredAndDoesNotCommit
FAIL: blk-pipe returned SUCCESS/0 and committed after validation created .git/hooks/post-commit
```

Second review-fix RED evidence:

```text
go test ./internal/pipe -run 'TestRun(GitUnsupportedEntryMutation|ValidationUnsupportedGitEntryMutation)' -v
FAIL: exit code = 9, want 3
FAIL: INTERNAL_ERROR from restore git metadata: unsupported git entry ".git/evilfifo"
```

Third review-fix RED evidence:

```text
TestRunGitDirectoryReplacedByUnsupportedEntryIsUnauthorizedRestoredAndDoesNotCommit
FAIL: exit code = 9, want 3
FAIL: restore git directory ".git/hooks": not a directory

TestRunValidationGitDirectoryReplacedByUnsupportedEntryIsUnauthorizedRestoredAndDoesNotCommit
FAIL: exit code = 9, want 3
FAIL: restore git directory ".git/refs": not a directory
```

### 4.2 GREEN

Final focused verification passed:

```text
== focused validation tests ==
PASS
ok  github.com/camcamcami/BLK-System/internal/validation  0.013s

== focused pipe tests ==
PASS
ok  github.com/camcamcami/BLK-System/internal/pipe  0.300s
```

Final full-suite verification passed:

```text
== full suite ==
ok  github.com/camcamcami/BLK-System/cmd/blk-pipe       (cached)
ok  github.com/camcamcami/BLK-System/internal/contracts (cached)
ok  github.com/camcamcami/BLK-System/internal/engine    (cached)
ok  github.com/camcamcami/BLK-System/internal/execguard (cached)
ok  github.com/camcamcami/BLK-System/internal/gitguard  (cached)
ok  github.com/camcamcami/BLK-System/internal/pipe      0.717s
ok  github.com/camcamcami/BLK-System/internal/runtimeguard (cached)
ok  github.com/camcamcami/BLK-System/internal/testutil  (cached)
ok  github.com/camcamcami/BLK-System/internal/validation 0.014s
```

---

## 5. Review Results

### 5.1 Spec compliance review

Final verdict: `PASS`.

Evidence from the final spec reviewer:

- Payload supports `validation_commands` and validates blank commands.
- Validation runs after engine success and pre-validation `.git` audit, before staging.
- Pre-validation `.git` mutation blocks validation.
- Post-validation `.git` mutation blocks staging/commit.
- Sequential validation produces deterministic log keys and aggregate-bounded logs.
- Validation failure restores to `PreEngineHash`, cleans, exits `2`, and does not commit.
- Unsupported `.git` entries, including existing dirs replaced by FIFOs, restore clean with `UNAUTHORIZED_FILE_MUTATION` / exit `3`.

### 5.2 Code-quality and safety review

Final verdict: `APPROVED`.

Evidence from the final safety reviewer:

- No critical, important, or minor issues remained.
- Post-validation `.git` mutations are checked and rolled back before staging/commit.
- `gitSnapshot.Restore` handles deleted `.git`, root replacement, and file/dir/symlink/unsupported kind transitions.
- Aggregate validation logs are bounded across commands.
- Validation and engine execution route through `execguard`.
- Production Git operations route through `gitguard.RunGit`.
- No production broad staging commands were found.
- Failure cleanup paths reset to the pre-engine hash and tests confirm no dirty repos or success commits remain.

### 5.3 Review-driven hardening added

The review loop materially improved Task 7 by adding regressions for:

- validation-induced `.git` hook persistence,
- aggregate validation log growth beyond configured cap,
- malformed env scrub assertions,
- unsupported `.git` FIFO entries,
- replacement of existing `.git` directories by unsupported entries.

---

## 6. Final Verification

Controller final verification command sequence:

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -l internal/validation/*.go internal/contracts/*.go internal/pipe/run.go internal/pipe/run_test.go
go test ./internal/validation -v
go test ./internal/pipe -run 'TestRun.*Unsupported|TestRun.*Validation|TestRun.*Git.*Mutation' -v
go test ./...
go vet ./...
! git grep -n 'exec.Command("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go'
git diff --check HEAD^ HEAD
git status --short --branch
git log --oneline --decorate -4
git push origin main
git status --short --branch
```

Final verification results:

```text
gofmt check: PASS (no files listed)
go test ./internal/validation -v: PASS
go test ./internal/pipe -run 'TestRun.*Unsupported|TestRun.*Validation|TestRun.*Git.*Mutation' -v: PASS
go test ./...: PASS
go vet ./...: PASS
production direct Git grep: PASS
production broad staging grep: PASS
git diff --check HEAD^ HEAD: PASS
git push origin main: 10a4b9b..2168a4f main -> main
final status: ## main...origin/main
```

Remote after implementation push:

```text
2168a4f (HEAD -> main, origin/main) feat: add blk-pipe validation gate
10a4b9b docs: record BLK-pipe sprint 002 task 6 outcome
9819f01 feat: report blk-pipe v47 execution details
fd269d6 docs: record BLK-pipe sprint 002 task 5 outcome
```

---

## 7. Deviations / Notes

- `internal/contracts/report.go` was not modified because `Report.ValidationLogs` and stable JSON report support already existed from earlier Sprint 002 work.
- The validation runner executes payload command strings through `execguard.Run`. This preserves the plan's explicit payload-command-string model without adding live Codex, shell expansion beyond the provided command string, or unbounded execution.
- The review loop exposed `.git` snapshot restoration hazards beyond the narrow Task 7 validation gate. These were fixed because validation cannot be considered safe if `.git` mutation rollback can leave the repo broken or dirty.
- Sprint 002 still does not run Codex or any live LLM engine.

---

## 8. Next Task

Next incomplete task after Task 7 is:

```text
Task 8 — Add Revert Escape Hatch
```

Expected implementation commit from the plan:

```bash
git commit -m "feat: add blk-pipe revert action"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002_task-008-outcome.md
```
