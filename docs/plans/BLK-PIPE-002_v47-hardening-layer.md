# BLK-pipe Sprint 002 — V47 Hardening Layer Implementation Plan

> **For Hermes:** Use `blk-system-sprint-execution`, `test-driven-development`, `subagent-driven-development`, and two-stage review for every implementation task. Use strict TDD for all code-producing tasks. Do not let implementation subagents push. Do not integrate Codex or any live tactical LLM engine in this sprint.

**Status:** Planned
**Date:** 2026-05-03
**Repository:** `/home/dad/BLK-System`
**Target Component:** `blk-pipe`
**Primary Doctrine:** `docs/BLK-004_blk-pipe-v47-architecture-suite.md`
**Sprint 001 Base:** `docs/outcomes/BLK-PIPE-001_sprint-001-closeout.md`

**Goal:** Harden the Sprint 001 deterministic BLK-pipe kernel toward the BLK-004/V47 interface by reconciling exit codes, adding V47-compatible contracts/reporting, centralizing bounded command execution, adding validation/revert/branch handling, and introducing a Python adapter shell without invoking Codex.

**Architecture:** Sprint 002 keeps `blk-pipe` as a compiled deterministic transport and safety layer. It layers V47 contract compatibility and stronger execution physics on top of the Sprint 001 file-boundary kernel, while preserving existing allowlist, cleanup, `.git` hardening, and hook-disabled commit guarantees. The sprint remains locally testable with fake/shell engines and hermetic Git repositories.

**Tech Stack:** Go 1.22 module semantics with local Go toolchain, Go standard library only for production code, Git CLI, POSIX shell fixtures for tests, Python standard library for adapter tests/docs if Task 10 is reached.

---

## 0. Current Known State

Before drafting this plan:

```text
Branch: main
Remote: origin/main
HEAD: a3165f5 docs: patch blk-pipe sprint 001 closeout
Go toolchain: /home/dad/.local/bin/go, go1.26.2 linux/amd64
Full suite: go test ./... PASS
Working tree: clean and aligned with origin/main before creating this plan file
```

While this document is being authored, `docs/plans/BLK-PIPE-002_v47-hardening-layer.md` may appear as an untracked/modified planning file. Commit and push the plan before executing Task 1.

Always run Go commands with:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Current Sprint 001 capabilities:

- `go run ./cmd/blk-pipe --health`
- `go run ./cmd/blk-pipe --payload /absolute/path/to/payload.json`
- `go run ./cmd/blk-pipe --payload-stdin`
- minimal Sprint 001 payload using `workdir`, `engine_command`, `timeout_seconds`, and `max_output_bytes`
- allowlist-only staging via `git add -- <file>`
- unauthorized mutation cleanup and `.git` metadata hardening
- process-group kill behavior for engine timeout/flood/inherited pipe writers
- protected BLK-req artifact denial for `docs/requirements/` and `docs/use_cases/`

Current known V47 gaps to close or prepare in this sprint:

- Sprint 001 exit code `4 ENGINE_FAILED` conflicts with BLK-004/V47 exit code `4 INVALID_REVERT_ANCHOR`.
- Sprint 001 report lacks V47 fields: `exit_code`, `pre_engine_hash`, `git_diff`, `engine_logs`, `validation_logs`, `diff_summary`, and `untracked_files`.
- Engine output is counted but not yet retained as bounded `engine_logs`.
- Git commands are not yet all routed through a generalized bounded command helper.
- Engine/Git environments scrub `GIT_*` in some paths, but do not yet explicitly scrub `SSH_AUTH_SOCK`, `SSH_AGENT_PID`, or `SSH_ASKPASS`, nor enforce deterministic `PWD` everywhere.
- Main-level signal trapping/panic recovery/active process-group reaping is not implemented.
- Validation commands are not yet supported.
- Revert action is not yet supported.
- Branch/fetch/orphan handling is not yet supported.
- Python adapter is not yet implemented.

---

## 1. Sprint 002 Non-Goals

Do **not** implement any of the following in Sprint 002 unless the user explicitly revises the plan:

- live Codex invocation,
- OpenAI/local LLM API calls,
- Discord or messaging-platform integration,
- BLK-req authoring/promotion,
- BLK-test MCP server integration,
- RTM generation,
- BEB/BEO lifecycle automation,
- Windows support,
- daemon/service mode,
- broad autonomous orchestration beyond the local binary and adapter contract.

Sprint 002 may create the interface that a future Codex caller will use, but tests must use fake/local commands only. **Sprint 002 does not run Codex.**

---

## 2. Non-Negotiable Safety Invariants To Preserve

These Sprint 001 invariants must not regress:

1. No production `git add .` or `git add -u`.
2. Stage only explicit allowlisted files with `git add -- <file>`.
3. Reject allowlist entries that are absolute, dirty/unclean, `.`, contain `..`, contain Git pathspec/glob metacharacters, or target protected BLK-req artifact paths.
4. Reject directory allowlist entries and deleted/missing allowlisted files before Git sees them.
5. Clean workspace preflight must reject tracked, untracked, and ignored pre-existing files before destructive execute/revert behavior.
6. Engine output must remain bounded and must not accumulate unbounded output in memory.
7. Timeout/flood process control must kill process groups, including child pipe-writer regressions.
8. `.git` mutations are unauthorized and restored where possible.
9. Commit hooks must remain disabled for BLK-pipe-created commits, including orphan initialization commits.
10. Unauthorized cleanup must remove ignored files and nested Git repositories created by the engine.
11. `--payload-stdin` remains available for internal/test usage unless explicitly removed later.
12. `--health` remains deterministic and must continue passing.
13. Validation commands must never run after a detected `.git` mutation.
14. Revert must not delete dirty pre-existing user work.
15. Orphan branch initialization must not accidentally commit the inherited tree.

Copy-pasteable production broad-staging check:

```bash
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
```

Copy-pasteable production direct-Git-call check after Task 5:

```bash
! git grep -n 'exec.Command("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
```

`internal/testutil/**` is deliberately excluded because it is test support code even when helper files are not named `*_test.go`.

---

## 3. Exit-Code Registry Policy

BLK-004/V47 strict Python router codes:

```text
0 SUCCESS
1 FATAL_SYSTEM_PANIC / INTERNAL_ERROR / FATAL_ENGINE_FAILED
2 SYNTAX_GATE_FAILED / VALIDATION_FAILED / INVALID_PAYLOAD
3 UNAUTHORIZED_FILE_MUTATION
4 INVALID_REVERT_ANCHOR
5 FATAL_OUTPUT_FLOOD
```

Legacy/local extension codes retained temporarily for compatibility until doctrine explicitly removes or remaps them:

```text
6 ENGINE_TIMEOUT
7 GIT_DIRTY
9 INTERNAL_ERROR_LEGACY
```

Rules:

- Code `4` must stop meaning `ENGINE_FAILED` before the revert route is introduced.
- Non-zero engine process exit should route to code `1` with status `FATAL_ENGINE_FAILED` unless a later doctrine update assigns a more specific code.
- Payload parse/validation errors can remain code `2`, with status `INVALID_PAYLOAD`.
- Validation command failures route to code `2`, with status `SYNTAX_GATE_FAILED` or `VALIDATION_FAILED` as finalized in implementation.
- Do not call the local extension codes “strict V47 router codes.”

---

## 4. Standard Controller Workflow For Each Task

For each implementation task:

1. Preflight:

   ```bash
   cd /home/dad/BLK-System
   git status --short --branch
   git fetch origin main
   git status --short --branch
   export PATH="$HOME/.local/bin:$PATH"
   go version
   go test ./...
   ```

2. Read the task section in this plan and the relevant section of `docs/BLK-004_blk-pipe-v47-architecture-suite.md`.
3. Dispatch a fresh implementation subagent with strict TDD instructions.
4. Require the subagent to show RED evidence before implementation.
5. Inspect the diff manually.
6. Run focused tests, full tests, and `git diff --check`.
7. Run two fresh reviewers:
   - spec compliance review against this plan and BLK-004,
   - code-quality/safety review against Sprint 001 invariants.
8. If either reviewer requests changes, amend the local unpushed task commit and rerun both reviews.
9. Only the controller pushes:

   ```bash
   git push origin main
   ```

10. Create and push a matching outcome doc after each task:

    ```text
    docs/outcomes/BLK-PIPE-002_task-00N-outcome.md
    ```

Outcome docs should include RED/GREEN evidence, review results, final verification, deviations, and next task.

---

## 5. Task 1 — Reconcile Exit-Code Registry

### Objective

Move BLK-pipe away from the Sprint 001 `4 ENGINE_FAILED` conflict and establish named constants/statuses for the V47 router before revert support exists.

### Files

Modify:

- `internal/pipe/exitcodes.go`
- `internal/pipe/exitcodes_test.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- `docs/BLK-009_blk-pipe-sprint-001-cli.md` if user-facing docs must mention the compatibility transition

Expected implementation commit:

```bash
git commit -m "feat: reconcile blk-pipe v47 exit codes"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002_task-001-outcome.md
```

### TDD Steps

#### Step 1: Add failing registry tests

In `internal/pipe/exitcodes_test.go`, add/update tests proving:

- `ExitInvalidRevertAnchor == 4`,
- `ExitFatalSystemPanic == 1`,
- no engine-failure path uses code `4`,
- `ExitOutputFlood == 5`,
- `ExitUnauthorizedMutation == 3`,
- legacy local extensions are explicitly named separately: `ExitEngineTimeout == 6`, `ExitGitDirty == 7`, `ExitInternalError == 9` if retained.

Focused command:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run TestExitCodes -v
```

Expected RED before implementation if the current constants still map engine failure to `4`.

#### Step 2: Add failing engine-failure routing test

In `internal/pipe/run_test.go`, add/update a test proving a non-zero engine exit returns `ExitFatalSystemPanic` and not `ExitInvalidRevertAnchor`.

Required properties:

- fake engine exits non-zero,
- report status is `FATAL_ENGINE_FAILED` or an explicitly chosen fatal status,
- exit code is `1`,
- HEAD is unchanged,
- repo is clean,
- code `4` is not used.

#### Step 3: Implement constants and status names

Recommended constants:

```go
const (
    ExitSuccess              = 0
    ExitFatalSystemPanic     = 1
    ExitInvalidPayload       = 2
    ExitValidationFailed     = 2
    ExitUnauthorizedMutation = 3
    ExitInvalidRevertAnchor  = 4
    ExitOutputFlood          = 5
    ExitEngineTimeout        = 6
    ExitGitDirty             = 7
    ExitInternalError        = 9
)
```

Update `run.go` so non-zero engine exits no longer return code `4`.

#### Step 4: Verify

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/pipe/exitcodes.go internal/pipe/exitcodes_test.go internal/pipe/run.go internal/pipe/run_test.go
go test ./internal/pipe -run 'TestExitCodes|TestRunEngineFailure' -v
go test ./...
git diff --check
```

### Review Gate

Spec reviewer must confirm code `4` is reserved for invalid revert anchor only.

Code-quality reviewer must confirm no timeout/flood/unauthorized cleanup behavior regressed.

---

## 6. Task 2 — Add V47 Payload and Stable Report Contracts With Legacy Normalization

### Objective

Support decoding V47 payload/report fields while preserving Sprint 001 payload compatibility during migration.

### Files

Modify/create:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/contracts/report.go`
- optionally create `internal/contracts/v47.go`
- optionally create `internal/contracts/report_test.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`

Expected implementation commit:

```bash
git commit -m "feat: add blk-pipe v47 contracts"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002_task-002-outcome.md
```

### Target Payload Behavior

Accept both Sprint 001 legacy payloads and V47-compatible payloads.

Normalization rules:

- `work_dir` maps to internal `Workdir`.
- `workdir` remains accepted for legacy tests.
- `engine` plus `engine_args` maps to internal `EngineCommand = append([]string{engine}, engine_args...)` for execute actions.
- `engine_command` remains accepted for legacy tests.
- If V47 payload omits legacy timeout/output fields, use deterministic defaults:
  - `timeout_seconds = 900`,
  - `max_output_bytes = 52428800`.
- Protected BLK-req allowlist validation remains unchanged.

### Target Report Behavior

Add stable V47 fields. Core V47 fields must be present in JSON even when empty; do **not** use `omitempty` on `git_diff`, `engine_logs`, `validation_logs`, or `untracked_files`.

Required report fields:

```go
type DiffSummary struct {
    FilesChanged int      `json:"files_changed"`
    Insertions   int      `json:"insertions"`
    Deletions    int      `json:"deletions"`
    Files        []string `json:"files"`
}

type Report struct {
    Status            string            `json:"status"`
    ExitCode          int               `json:"exit_code"`
    Action            string            `json:"action"`
    Workdir           string            `json:"workdir"`
    WorkDir           string            `json:"work_dir,omitempty"`
    TargetBranch      string            `json:"target_branch,omitempty"`
    CebID             string            `json:"ceb_id,omitempty"`
    CommitHash        string            `json:"commit_hash,omitempty"`
    PreEngineHash     string            `json:"pre_engine_hash,omitempty"`
    GitDiff           string            `json:"git_diff"`
    EngineLogs        string            `json:"engine_logs"`
    ValidationLogs    map[string]string `json:"validation_logs"`
    DiffSummary       *DiffSummary      `json:"diff_summary,omitempty"`
    UntrackedFiles    []string          `json:"untracked_files"`
    StagedFiles       []string          `json:"staged_files"`
    DestroyedFiles    []string          `json:"destroyed_files"`
    EngineExitCode    int               `json:"engine_exit_code"`
    EngineOutputBytes int64             `json:"engine_output_bytes"`
    Error             string            `json:"error,omitempty"`
}
```

Initialize `ValidationLogs` to an empty map and `UntrackedFiles` to an empty slice for every report path.

### TDD Steps

#### Step 1: Add payload decode tests

Test:

- legacy payload still validates,
- V47 `work_dir` decodes into internal workdir,
- V47 `engine` + `engine_args` normalizes into command argv,
- missing V47 timeout/output values receive defaults,
- invalid relative `work_dir` fails,
- protected paths still fail in both allowlist fields.

#### Step 2: Add report JSON tests

Test that JSON includes stable fields even when empty:

- `exit_code`,
- `git_diff`,
- `engine_logs`,
- `validation_logs`,
- `untracked_files`,
- legacy `staged_files` and `destroyed_files`.

#### Step 3: Wire `pipe.Run` to the decoder

Replace direct `json.Unmarshal` in `parseAndValidatePayload` with the new contract decoder. Set `report.ExitCode` before encoding for all routes.

#### Step 4: Verify

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/contracts/*.go internal/pipe/run.go internal/pipe/run_test.go
go test ./internal/contracts -v
go test ./internal/pipe -v
go test ./...
git diff --check
```

### Review Gate

Spec reviewer must confirm Sprint 001 payloads still work and V47 payloads decode without adding live engine integration.

Code-quality reviewer must check that defaults are deterministic and validation remains centralized.

---

## 7. Task 3 — Add Reusable Bounded Command Guard, Engine Log Capture, and Environment Scrub

### Objective

Create a reusable standard-library command helper that bounds process runtime/output, captures bounded logs, kills process groups, and constructs deterministic scrubbed environments for engines, validation commands, and later Git helpers.

### Files

Create:

- `internal/execguard/command.go`
- `internal/execguard/command_test.go`

Modify:

- `internal/engine/runner.go`
- `internal/engine/runner_test.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`

Expected implementation commit:

```bash
git commit -m "feat: add bounded command guard"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002_task-003-outcome.md
```

### Target API

Suggested API:

```go
type CommandResult struct {
    ExitCode    int
    Output      []byte
    OutputBytes int64
    TimedOut    bool
    Flooded     bool
}

type Options struct {
    Workdir        string
    Command        []string
    Timeout        time.Duration
    MaxOutputBytes int64
    Env            []string
}

func Run(ctx context.Context, opts Options) (CommandResult, error)
func ScrubbedEnv(workdir string, extra ...string) []string
```

Environment requirements:

- remove all inherited `GIT_*`,
- remove `SSH_AUTH_SOCK`,
- remove `SSH_AGENT_PID`,
- remove `SSH_ASKPASS`,
- append `GIT_CONFIG_GLOBAL=/dev/null`,
- append `GIT_CONFIG_NOSYSTEM=1`,
- append deterministic `PWD=<workdir>`.

POSIX build-tag requirement:

- Any file using `syscall`, process groups, or platform-specific process control must start with `//go:build linux || darwin`.
- Do not add Windows fallbacks in Sprint 002.

### TDD Steps

#### Step 1: Add env scrub tests

Test that `ScrubbedEnv` removes dangerous inherited keys and sets deterministic replacements.

#### Step 2: Add command bounding tests

Port or mirror existing engine runner tests for:

- success command exits 0 and captures output,
- non-zero command returns exit code and bounded output without infrastructure error,
- timeout kills process group,
- output flood kills process group and does not retain unbounded output,
- inherited pipe-writer regression cannot hang.

#### Step 3: Implement helper minimally

Move logic from `internal/engine/runner.go` only after tests are RED.

#### Step 4: Refactor engine runner and report engine logs

Keep the public `engine.Run` API stable if practical, but extend its `Result` to expose bounded output/log bytes or provide another path for `pipe.Run` to set `report.EngineLogs`.

Required tests:

- successful fake engine output appears in `report.EngineLogs`,
- failing fake engine output appears in `report.EngineLogs`,
- flood path does not store unbounded logs and still exits with output flood status.

#### Step 5: Verify

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/execguard/command.go internal/execguard/command_test.go internal/engine/runner.go internal/engine/runner_test.go internal/pipe/run.go internal/pipe/run_test.go
go test ./internal/execguard -v
go test ./internal/engine -v
go test -race ./internal/engine
go test ./internal/engine -count=20
go test ./internal/pipe -run 'TestRun.*EngineLogs|TestRun.*OutputFlood' -v
go test ./...
git diff --check
```

### Review Gate

Spec reviewer must confirm environment scrub, output/time bounding, and `engine_logs` population match BLK-004.

Code-quality reviewer must focus on goroutine/process leaks, process-group kill behavior, bounded log retention, and POSIX build tags.

---

## 8. Task 4 — Add Main-Level Signal Trap, Panic Recovery, and Active Process Reaping

### Objective

Implement BLK-004's fatal-system behavior: trap `SIGINT`/`SIGTERM`, recover panics into a sterile JSON report, reap active process groups, and exit with code `1`.

### Files

Create/modify:

- `cmd/blk-pipe/main.go`
- `cmd/blk-pipe/main_test.go`
- `internal/execguard/command.go`
- `internal/execguard/command_test.go`
- optionally create `internal/runtimeguard/signal.go`
- optionally create `internal/runtimeguard/signal_test.go`

Expected implementation commit:

```bash
git commit -m "feat: add blk-pipe fatal signal guard"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002_task-004-outcome.md
```

### Target Behavior

- If `main` panics, emit one JSON report with fatal status and exit `1`.
- If process receives `SIGINT` or `SIGTERM` while an engine/validation command is active, kill/reap the active process group and exit `1`.
- Do not emit multiple JSON reports.
- OS-dependent signal/process code must use `//go:build linux || darwin`.

### TDD Steps

#### Step 1: Add testable runtime guard seams

Introduce small seams rather than hard-to-test global behavior. For example:

- a function that formats sterile fatal reports,
- an active process registry in `execguard`,
- test-only command that sleeps and records child PID.

#### Step 2: Add panic recovery tests

Test the report emitted on an injected panic path.

#### Step 3: Add signal process-group cleanup test

Use a bounded subprocess test if practical:

- start `blk-pipe` with fake long-running engine,
- send `SIGTERM`,
- assert exit code `1`,
- assert child process is gone,
- assert output is valid JSON or documented fatal report format.

If full subprocess signal testing is too flaky, unit-test active process registry/reaping and document the remaining manual smoke command in the outcome.

#### Step 4: Verify

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w cmd/blk-pipe/main.go cmd/blk-pipe/main_test.go internal/execguard/*.go internal/runtimeguard/*.go
go test ./cmd/blk-pipe -v
go test ./internal/execguard -v
go test ./...
git diff --check
```

### Review Gate

Spec reviewer must confirm BLK-004 signal/panic behavior is represented and code `1` is used.

Code-quality reviewer must confirm signal tests are deterministic or clearly bounded and no orphan process remains.

---

## 9. Task 5 — Route Git Calls Through a Bounded Git Helper

### Objective

Centralize production Git command execution and remove ad hoc `exec.Command("git", ...)` call sites from BLK-pipe production paths.

### Files

Create/modify:

- `internal/gitguard/command.go`
- `internal/gitguard/command_test.go`
- `internal/gitguard/status.go`
- `internal/gitguard/stage.go`
- `internal/gitguard/cleanup.go`
- `internal/pipe/run.go`
- relevant tests under `internal/gitguard/*_test.go` and `internal/pipe/run_test.go`

Expected implementation commit:

```bash
git commit -m "feat: bound blk-pipe git commands"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002_task-005-outcome.md
```

### Target API

Suggested API:

```go
type GitResult struct {
    Stdout []byte
}

func RunGit(ctx context.Context, repo string, args ...string) (GitResult, error)
func RunGitWithLimit(ctx context.Context, repo string, maxOutputBytes int64, args ...string) (GitResult, error)
func RunGitWithEnv(ctx context.Context, repo string, extraEnv []string, args ...string) (GitResult, error)
```

Default Git timeout should be short and deterministic, for example `30 * time.Second`, unless a specific operation requires more.

`ls-remote` support in later branch prep must be able to inject:

```text
GIT_SSH_COMMAND=ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes
```

### TDD Steps

#### Step 1: Add tests for bounded Git helper

Test:

- `rev-parse HEAD` succeeds in a hermetic repo,
- failing Git command returns stderr context,
- inherited `GIT_*` and SSH env are scrubbed,
- output flood is reported as an infrastructure error,
- command timeout is reported as an infrastructure error,
- `ls-remote` extra env can inject the headless SSH hardening variable.

#### Step 2: Replace production call sites

Replace ad hoc Git execution in:

- `gitguard.EnsureClean`,
- `gitguard.StageAllowlist`,
- `gitguard.CleanupUnauthorized`,
- `pipe.runGit` or remove it entirely.

Production code may still use `exec.Command` for non-Git execution through `execguard`; it should not call Git directly outside the helper after this task.

#### Step 3: Add grep guard

Run:

```bash
! git grep -n 'exec.Command("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
```

#### Step 4: Verify

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/gitguard/*.go internal/pipe/run.go
go test ./internal/gitguard -v
go test ./internal/pipe -v
go test ./...
! git grep -n 'exec.Command("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
git diff --check
```

### Review Gate

Spec reviewer must confirm all production Git calls use the helper.

Code-quality reviewer must confirm broad cleanup remains safe only after staging/preflight prerequisites.

---

## 10. Task 6 — Add Pre-Engine Hash, Mandatory Zero-Diff Abort, Diff Summary, Git Diff, and Untracked Report Fields

### Objective

Populate V47 report fields for execute runs and enforce BLK-004's no-silent-staging-failure rule.

### Files

Modify:

- `internal/contracts/report.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`

Expected implementation commit:

```bash
git commit -m "feat: report blk-pipe v47 execution details"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002_task-006-outcome.md
```

### Target Behavior

For successful execute runs, report must include:

- `pre_engine_hash`: HEAD before engine execution,
- `git_diff`: `git diff <PreEngineHash> HEAD --`,
- `diff_summary`: parsed from `git diff <PreEngineHash> HEAD --numstat --`,
- `untracked_files`: from rogue-file audit after success,
- `exit_code`: process exit code,
- `engine_logs`: already wired by Task 3.

Zero-diff rule is mandatory:

- If engine exits 0 but produces no staged allowlisted diff after strict staging and unauthorized cleanup, return `UNAUTHORIZED_FILE_MUTATION`, exit code `3`, do not commit, preserve `HEAD`, and leave repo clean.

This resolves BLK-004's internal wording tension by using the hard-ban/commit-gate rule: no staged allowed diff is an unauthorized/staging failure with exit `3`.

### TDD Steps

#### Step 1: Add success report tests

In `internal/pipe/run_test.go`, add tests proving a successful allowlisted modification reports:

- non-empty `PreEngineHash`,
- `CommitHash != PreEngineHash`,
- `GitDiff` contains the allowed file change,
- `DiffSummary.FilesChanged == 1`,
- `DiffSummary.Files` includes the changed file,
- `UntrackedFiles` is empty,
- `EngineLogs` contains bounded fake engine output when present.

#### Step 2: Add mandatory zero-diff test

Add test where engine exits 0 but changes nothing. Assert:

- exit `3`,
- status `UNAUTHORIZED_FILE_MUTATION`,
- no commit,
- `HEAD == PreEngineHash`,
- repo clean.

#### Step 3: Implement reporting and commit gate

Capture `preEngineHash` after clean preflight and before engine execution. Extract diffs only through bounded Git helper. Never use triple-dot diff.

#### Step 4: Verify

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/contracts/report.go internal/pipe/run.go internal/pipe/run_test.go
go test ./internal/pipe -run 'TestRunSuccess.*Report|TestRun.*ZeroDiff' -v
go test ./...
git diff --check
```

### Review Gate

Spec reviewer must confirm no triple-dot diff and V47 field names are correct.

Code-quality reviewer must confirm diff extraction is bounded and no zero-diff success remains.

---

## 11. Task 7 — Add Sequential Validation Command Gate

### Objective

Run validation commands sequentially after engine execution and `.git` mutation audit, but before staging/commit; aggregate logs; abort and restore on validation failure.

### Files

Create/modify:

- `internal/validation/validation.go`
- `internal/validation/validation_test.go`
- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/contracts/report.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`

Expected implementation commit:

```bash
git commit -m "feat: add blk-pipe validation gate"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002_task-007-outcome.md
```

### Target Behavior

- `validation_commands` are command strings from payload.
- Run validation after engine success **only after checking `.git` mutations**. If `.git` changed, restore and return `UNAUTHORIZED_FILE_MUTATION` before validation can run.
- Run validation commands sequentially in payload workdir.
- Capture logs in `validation_logs` keyed by deterministic names such as `validation_001`, `validation_002`.
- Run all commands sequentially and aggregate logs; evaluate failure after completion.
- If any validation command fails:
  - restore repo to `PreEngineHash`,
  - clean unauthorized files,
  - report status `SYNTAX_GATE_FAILED`,
  - exit code `2`,
  - do not stage or commit.

### TDD Steps

#### Step 1: Add validation package tests

Test:

- commands run sequentially in order,
- logs are captured under deterministic keys,
- failing command records output and failure,
- inherited dangerous env is scrubbed.

#### Step 2: Add `.git` mutation before validation regression

Pipe-level test:

- engine mutates `.git/hooks/post-commit`,
- validation command would create sentinel file if run,
- run returns `UNAUTHORIZED_FILE_MUTATION`,
- sentinel file does not exist,
- `.git` is restored,
- repo clean.

#### Step 3: Add validation failure test

Pipe-level test:

- engine modifies `README.md`,
- validation command fails,
- exit code is `ExitValidationFailed`,
- report status is `SYNTAX_GATE_FAILED`,
- `validation_logs` contains command output,
- no success commit is created,
- repo restored to pre-engine content and clean.

#### Step 4: Add validation success test

Prove validation success allows staging/cleanup/commit and logs are present.

#### Step 5: Implement validation runner

Use `execguard.Run` with deterministic env. Do not use unbounded `os/exec` directly.

#### Step 6: Verify

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/validation/*.go internal/contracts/*.go internal/pipe/run.go internal/pipe/run_test.go
go test ./internal/validation -v
go test ./internal/pipe -run 'TestRun.*Validation|TestRun.*Git.*Validation' -v
go test ./...
git diff --check
```

### Review Gate

Spec reviewer must confirm validation cannot run after `.git` mutation and validation failure aborts before staging/commit.

Code-quality reviewer must confirm validation logs are bounded and no shell injection is introduced beyond explicit payload command strings.

---

## 12. Task 8 — Add Revert Escape Hatch

### Objective

Implement `action: "revert"` using a verified absolute `target_hash` ancestry gate and no relative anchors, while preserving pre-existing dirty user work.

### Files

Modify:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`

Expected implementation commit:

```bash
git commit -m "feat: add blk-pipe revert action"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002_task-008-outcome.md
```

### Target Behavior

Sprint 002 follows the BLK-004 fast-path ordering: revert routes before execute branch/fetch/engine/validation/staging logic. Revert operates on the currently checked-out workspace. The caller/orchestrator must provide the correct workspace/branch. Do not create branches or run the engine for revert in this task.

Before destructive reset/clean:

1. Validate payload.
2. Run clean preflight and reject dirty tracked, untracked, or ignored pre-existing files without modifying the repo.
3. Validate `target_hash` is present and safe.
4. Resolve only full hex commit object IDs or otherwise reject. Do not accept `HEAD`, `HEAD~1`, `HEAD^`, `@{1}`, branch names, tag names, or pathspec-ish syntax.
5. Run `git merge-base --is-ancestor <target_hash> HEAD`.
6. If ancestry check fails, report `INVALID_REVERT_ANCHOR`, exit code `4`, and do not reset.
7. If ancestry check passes, run `git reset --hard <target_hash>` and cleanup.
8. Emit exactly one JSON report and exit `0`.

### TDD Steps

#### Step 1: Add payload validation tests

Test that revert requires:

- absolute workdir/work_dir,
- target hash present,
- no relative anchors (`HEAD~1`, `HEAD^`, `@{1}`),
- no branch/tag names.

#### Step 2: Add successful revert integration test

Create hermetic repo with two commits. Revert to first commit hash. Assert:

- exit `0`,
- status `SUCCESS`,
- HEAD equals target hash,
- second commit content removed,
- repo clean.

#### Step 3: Add invalid anchor integration test

Use a sibling/unrelated commit or invalid hash. Assert:

- exit `4`,
- status `INVALID_REVERT_ANCHOR`,
- HEAD unchanged,
- repo clean.

#### Step 4: Add dirty-preflight preservation tests

Tests:

- dirty tracked file before revert is preserved and revert does not run,
- pre-existing untracked/ignored file before revert is preserved and revert does not run.

#### Step 5: Add no-engine/no-validation/no-commit test

Payload may contain engine/validation fields, but revert must not run them. Assert no sentinel files are created and no new commit is made.

#### Step 6: Verify

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/contracts/payload.go internal/contracts/payload_test.go internal/pipe/run.go internal/pipe/run_test.go
go test ./internal/contracts -run 'TestPayload.*Revert' -v
go test ./internal/pipe -run 'TestRun.*Revert' -v
go test ./...
git diff --check
```

### Review Gate

Spec reviewer must confirm no relative anchors and code `4` is only invalid revert anchor.

Code-quality reviewer must confirm revert cannot run engine/validation/commit and cannot delete dirty pre-existing work.

---

## 13. Task 9 — Add Branch/Fetch/Orphan Workspace Preparation For Execute

### Objective

Prepare the target branch for execute payloads using deterministic fetch/checkout/orphan handling, including true empty orphan initialization before capturing `PreEngineHash`.

### Files

Create/modify:

- `internal/gitguard/branch.go`
- `internal/gitguard/branch_test.go`
- `internal/contracts/payload.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`

Expected implementation commit:

```bash
git commit -m "feat: add blk-pipe branch preparation"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002_task-009-outcome.md
```

### Target Behavior

For execute payloads with `target_branch`:

1. Validate payload and branch name.
2. Reject dirty current workspace before branch switching.
3. `git fetch origin` if a remote exists.
4. `git checkout <target_branch>` if local branch exists.
5. Else `git checkout -t origin/<target_branch>` if remote branch exists.
6. Else use bounded `git ls-remote --symref` fallback only if needed by implementation; it must inject headless SSH hardening:

   ```text
   GIT_SSH_COMMAND=ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes
   ```

7. Else create orphan branch: `git checkout --orphan <target_branch>`.
8. If orphan branch created, clear the inherited index/tree before the initialization commit:

   ```bash
   git read-tree --empty
   git -c core.hooksPath=/dev/null commit --allow-empty -m "Initialize branch"
   ```

   BLK-004 has an internal message wording conflict (`Initialize` vs `Initialize branch`). Sprint 002 chooses `Initialize branch` to match the execution-sequence source segment and documents that choice.

9. After branch preparation, perform the chosen Sprint 001/V47 workspace sterilization sequence:
   - reject dirty/untracked/ignored post-checkout state if it represents pre-existing user work,
   - run required bounded `git reset --hard HEAD` and cleanup only after the safety decision,
   - then capture `PreEngineHash`.

Safety constraints:

- `target_branch` must reject empty, whitespace, path traversal, shell metacharacters, and Git revision/pathspec tricks.
- Do not use shell; pass branch as argv.
- The empty orphan initialization commit must have hooks disabled.
- Orphan initialization must not commit inherited files from the previous branch.

### TDD Steps

#### Step 1: Add branch validation tests

Validate safe branch names and reject:

- empty,
- `../escape`,
- `feature;rm -rf`,
- `HEAD~1`,
- names starting with `-`,
- names containing whitespace/control characters.

#### Step 2: Add dirty-current-workspace test

Dirty current workspace before branch prep must abort without checkout/reset/cleanup.

#### Step 3: Add local branch checkout test

Hermetic repo creates local branch. Payload targets branch. Assert execution occurs on that branch.

#### Step 4: Add remote tracking test if feasible

Use two temp repos: bare remote and working clone. Assert missing local branch can track `origin/<branch>`.

#### Step 5: Add orphan survival and empty-tree test

Target a brand-new branch. Assert:

- branch exists,
- initialization commit exists,
- initialization commit tree is empty and does not include inherited `README.md`,
- HEAD is valid before engine execution,
- final execution can commit allowed changes.

#### Step 6: Add post-checkout dirty/untracked state test

If target branch contains state that would violate preflight expectations, assert deterministic behavior and no silent deletion of user work.

#### Step 7: Verify

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/gitguard/branch.go internal/gitguard/branch_test.go internal/contracts/payload.go internal/pipe/run.go internal/pipe/run_test.go
go test ./internal/gitguard -run 'Test.*Branch|TestPrepareTargetBranch' -v
go test ./internal/pipe -run 'TestRun.*Branch|TestRun.*Orphan' -v
go test ./...
git diff --check
```

### Review Gate

Spec reviewer must confirm orphan initialization occurs before capturing HEAD and does not inherit the old tree.

Code-quality reviewer must focus on branch-name validation, preflight ordering, `ls-remote` SSH hardening, and no shell/pathspec injection.

---

## 14. Task 10 — Add Python Adapter Skeleton and Tests

### Objective

Introduce a local Python adapter around `blk-pipe --payload <tempfile>` that matches BLK-004 expectations without invoking Codex or any live LLM.

### Files

Create:

- `python/blk_pipe_adapter.py`
- `python/test_blk_pipe_adapter.py`

Modify:

- `README.md` or `docs/BLK-009_blk-pipe-sprint-001-cli.md` only if documentation needs to point at the adapter

Expected implementation commit:

```bash
git commit -m "feat: add blk-pipe python adapter"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002_task-010-outcome.md
```

### Target Behavior

Adapter should expose:

```python
@dataclass
class ExecutionResult:
    status: str
    exit_code: int
    pre_engine_hash: str = ""
    git_diff: str = ""
    engine_logs: str = ""
    validation_logs: dict[str, str] | None = None
    diff_summary: dict | None = None
    error: str | None = None
    untracked_files: list[str] | None = None

class BlkPipeAdapter:
    def __init__(self, binary_path: str = "blk-pipe") -> None: ...
    def run_health_check(self) -> bool: ...
    def execute_sprint(...): ...
    def abort_sprint_and_revert(...): ...
```

Hard constraints:

- Use `tempfile.NamedTemporaryFile(delete=False, suffix='.json')` or equivalent.
- Invoke `[binary_path, "--payload", temp_payload_path]` without shell.
- Parse stdout JSON.
- Route by return code exactly as BLK-004 specifies.
- Clean up temp payload file in `finally`.
- Tests must use a fake `blk-pipe` executable script or the local Go binary with fake commands; do not call Codex.

### TDD Steps

#### Step 1: Add adapter tests with fake binary

Tests must cover all strict V47 return-code routes:

- `0 -> parsed/SUCCESS`,
- `1 -> FATAL_SYSTEM_PANIC`,
- `2 -> SYNTAX_GATE_FAILED`,
- `3 -> UNAUTHORIZED_FILE_MUTATION`,
- `4 -> INVALID_REVERT_ANCHOR`,
- `5 -> FATAL_OUTPUT_FLOOD`,
- invalid/non-JSON stdout maps to fatal crash result,
- health check true on exit 0,
- execute_sprint writes expected payload JSON and invokes `--payload`,
- temp payload file is removed.

Use Python standard-library `unittest` unless the project deliberately adopts pytest later.

#### Step 2: Implement adapter

Keep it small and deterministic.

#### Step 3: Optional integration smoke

Build/run the Go CLI and invoke health via adapter if practical.

#### Step 4: Verify

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
git diff --check
```

### Review Gate

Spec reviewer must confirm the adapter contract matches BLK-004 and does not call Codex.

Code-quality reviewer must confirm no shell invocation, temp file cleanup, and deterministic return-code routing.

---

## 15. Task 11 — Sprint 002 Documentation and Closeout

### Objective

Document the Sprint 002 V47-compatible BLK-pipe contract and close the sprint with traceable verification.

### Files

Create:

- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/outcomes/BLK-PIPE-002_sprint-002-closeout.md`

Modify:

- `README.md`

Expected implementation/docs commit:

```bash
git commit -m "docs: describe blk-pipe v47 hardening layer"
```

Expected closeout commit:

```bash
git commit -m "docs: close out blk-pipe sprint 002"
```

### Required Documentation Content

The Sprint 002 CLI/doc must include:

- supported commands:
  - `go run ./cmd/blk-pipe --health`,
  - `go run ./cmd/blk-pipe --payload /tmp/payload.json`,
  - optional/internal `go run ./cmd/blk-pipe --payload-stdin`,
- V47-compatible payload fields,
- stable V47-compatible report fields,
- strict V47 router exit codes and any legacy/local extensions,
- signal/panic fatal behavior,
- validation gate behavior,
- revert route behavior,
- branch/fetch/orphan behavior,
- Python adapter path if Task 10 completed,
- explicit sentence: `Sprint 002 does not run Codex`,
- remaining deferrals and recommended Sprint 003 scope.

The closeout note must include:

- final implementation commit hash,
- sprint closeout commit hash after it is committed,
- list of implemented tasks,
- test output summary,
- production broad-staging grep result,
- direct Git-call grep result excluding test utilities,
- BLK-004/V47 deviations still remaining,
- explicit statement that Codex/live engine integration remains deferred.

### Verification

Run:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./...
python3 -m unittest discover -s python -p 'test_*.py'
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
! git grep -n 'exec.Command("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
git diff --check
```

If Python adapter tests are not present because Task 10 was deliberately deferred, record that explicitly and do not hide it behind `|| true` in final closeout evidence.

### Review Gate

Spec reviewer must check documentation against completed implementation only; no overclaims.

Code-quality/doc reviewer must check Markdown formatting, balanced fences, no trailing whitespace, and copy-pasteable commands.

---

## 16. Final Sprint 002 Acceptance Criteria

Sprint 002 is complete when all completed tasks pass their review gates and the following are true:

1. `go test ./...` passes.
2. `go run ./cmd/blk-pipe --health` remains deterministic.
3. `--payload /absolute/path` still works.
4. Sprint 001 payloads remain supported unless a deliberate migration note says otherwise.
5. V47-compatible payloads are accepted for local fake-engine execution.
6. Strict V47 router codes `0-5` are documented separately from any legacy/local extension codes.
7. Exit code `4` is reserved for invalid revert anchor only.
8. Engine non-zero exits no longer use code `4`.
9. Signal/panic paths emit fatal behavior and exit `1`.
10. Validation command failures restore the repo and exit `2`.
11. Validation never runs after detected `.git` mutation.
12. Unauthorized mutations still exit `3` and leave the repo clean.
13. Zero-diff/no-staged-allowed-change runs exit `3` and leave the repo clean.
14. Output floods still exit `5` and leave the repo clean.
15. Timeouts remain bounded and leave the repo clean.
16. All production Git calls route through the bounded Git helper.
17. Production code contains no broad staging commands.
18. `git diff <Hash> HEAD --` is used for final diff extraction, not triple-dot diff.
19. Revert uses verified `target_hash`, rejects relative anchors, and refuses dirty pre-existing work.
20. Branch/orphan handling initializes orphan branches before capturing HEAD and does not inherit previous branch files.
21. Python adapter, if implemented, shells out without shell and cleans temp payloads.
22. No Codex/live LLM integration is introduced.

---

## 17. Recommended Sprint 003 Seed Scope

After Sprint 002 succeeds, consider Sprint 003 for controlled tactical-engine integration:

1. Decide whether `engine`/`engine_args` should invoke Codex directly or through a higher-level Hermes/Python orchestrator.
2. Add explicit Codex dry-run/fake-engine parity tests before live runs.
3. Add CEB/L2 packet fixture tests.
4. Add operational timeout defaults and observability around long tactical runs.
5. Integrate BLK-test validation adapters if doctrine is ready.
6. Add human-in-the-loop safety gates before live model execution.

Codex/live engine integration should remain blocked until Sprint 002 closeout proves deterministic V47 file-boundary, validation, revert, branch, signal, and adapter behavior.

---

## 18. Quick Resume Prompt For Future Hermes

If context is lost, resume with:

```text
Open /home/dad/BLK-System/docs/plans/BLK-PIPE-002_v47-hardening-layer.md. Execute Task 1 next using blk-system-sprint-execution, strict TDD, two-stage review, controller-only push, and a pushed/attached outcome doc. Preserve Sprint 001 safety invariants and do not integrate Codex/live LLMs in Sprint 002.
```
