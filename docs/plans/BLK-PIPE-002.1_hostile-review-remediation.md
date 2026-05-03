# BLK-pipe Sprint 002.1 — Hostile Review Remediation Plan

> **For Hermes:** Use `blk-system-sprint-execution`, `test-driven-development`, `subagent-driven-development`, and two-stage review for every implementation task. This is a remediation sprint generated from the post-Sprint 002 hostile review. Use strict TDD. Do not let implementation subagents push. Do not integrate Codex or any live tactical LLM engine in this sprint.

**Status:** Planned
**Date:** 2026-05-03
**Repository:** `/home/dad/BLK-System`
**Target Component:** `blk-pipe`
**Primary Doctrine:** `docs/BLK-001_blk-system-master-architecture.md`, `docs/BLK-004_blk-pipe-v47-architecture-suite.md`
**Sprint 002 Base:** `docs/outcomes/BLK-PIPE-002_sprint-002-closeout.md`
**Preparation Source:** post-Sprint 002 hostile review of Phase 1 and Phase 2 implementation

**Goal:** Close the safety gaps found after Sprint 002 before any Sprint 003 live tactical/Codex integration work begins.

**Architecture:** Sprint 002.1 keeps `blk-pipe` as a deterministic POSIX transport and safety layer. It does not expand orchestration scope. It adds targeted hostile-regression tests and minimal implementation changes for physical residue cleanup, escaped-descendant timeout/flood containment, read-only validation semantics, validation safety precedence, and V47 `l2_packet` delivery.

**Tech Stack:** Go 1.22 module semantics with local Go toolchain (`/home/dad/.local/bin/go`, currently `go1.26.2 linux/amd64`), Go standard library only for production code, Git CLI through bounded helpers, POSIX shell fixtures for tests, Python standard library adapter tests.

---

## 0. Current Known State

Preflight observed while drafting this plan:

```text
Date: 2026-05-03
Branch: main
Remote: origin/main
HEAD: 76f3cea docs: record blk-pipe sprint 002 closeout hash
Working tree: clean and aligned with origin/main
Go toolchain: go version go1.26.2 linux/amd64
```

Always run Go commands with:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Current Sprint 002 documented capabilities include:

- `go run ./cmd/blk-pipe --health`
- `go run ./cmd/blk-pipe --payload /absolute/path/to/payload.json`
- `go run ./cmd/blk-pipe --payload-stdin`
- Sprint 001 legacy and V47-compatible payload decoding
- V47-compatible report fields
- bounded engine execution through `internal/execguard`
- bounded Git calls through `internal/gitguard.RunGit`
- signal/panic fatal guard
- validation commands
- revert route
- branch/fetch/orphan preparation
- local Python adapter

The hostile review found that those capabilities are still not sufficient for live tactical/Codex integration.

---

## 1. Sprint 002.1 Non-Goals

Do **not** implement any of the following in Sprint 002.1 unless the user explicitly revises this plan:

- live Codex invocation,
- OpenAI/local LLM API calls,
- Discord or messaging-platform integration,
- BLK-req authoring or promotion,
- BLK-test MCP integration,
- RTM generation,
- BEB/BEO lifecycle automation,
- Windows support,
- daemon/service mode,
- broader orchestration beyond local `blk-pipe` and the existing Python adapter contract,
- separate tracked-vs-new allowlist semantics unless explicitly required by a task below.

Sprint 002.1 exists to make Sprint 002 truthful and harder to break. **Sprint 002.1 does not run Codex.**

---

## 2. Hostile Review Findings To Remediate

### Finding A — Success path can leave unauthorized physical residue

The current success path can return `SUCCESS` when the engine creates an allowlisted file change plus an unauthorized empty directory. Git reports a clean worktree because Git does not track empty directories, but physical residue remains on disk.

Observed hostile probe result:

```json
{
  "report_status": "SUCCESS",
  "report_exit_code": 0,
  "report_untracked_files": ["ghostdir/"],
  "ghostdir_exists_after_return": true
}
```

Relevant current code:

- `internal/pipe/run.go` stages allowlisted paths.
- `internal/pipe/run.go` audits unauthorized files with Git-only visibility.
- `internal/pipe/run.go` commits without success-path erasure.
- `internal/pipe/run.go` helper `emptyUntrackedDirs` exists but is not part of the success-path unauthorized audit.

Doctrine pressure:

- BLK-001 says `blk-pipe` must physically enforce allowed mutations and abort unauthorized edits.
- BLK-004 says staging must be followed by unauthorized erasure before commit.

Sprint 002.1 policy decision: no `SUCCESS` may leave unauthorized physical residue. The stricter BLK-001 abort behavior wins: if any unauthorized physical residue is observed, return `UNAUTHORIZED_FILE_MUTATION` / exit `3`, clean it, and do not create a success commit.

### Finding B — Timeout can return before escaped child mutates the repo

A session-escaped child process can survive a timeout and mutate the repo after BLK-pipe reports `ENGINE_TIMEOUT` and returns.

Observed hostile probe result:

```json
{
  "report_status": "ENGINE_TIMEOUT",
  "report_exit_code": 6,
  "git_status_immediate": "",
  "git_status_after_delay": "?? late.txt"
}
```

Relevant current code:

- `internal/execguard/command.go` has active command and Linux pipe-holder discovery machinery.
- Timeout/flood/cancel paths can close the output reader and return without invoking active pipe-holder cleanup before unregistering.
- The current comment explicitly notes timeout/cancel can force return before escaped descendants exit.

Sprint 002.1 policy decision: on timeout, output flood, or context cancel, BLK-pipe must make a best-effort active cleanup pass before returning and before unregistering the active command. Linux pipe-holder cleanup must be used when available.

### Finding C — Validation can author the committed diff

A no-op engine followed by a validation command that writes an allowlisted file can currently become a successful commit.

Observed hostile probe result:

```json
{
  "report_status": "SUCCESS",
  "report_exit_code": 0,
  "committed_README": "validation"
}
```

Sprint 002.1 policy decision: validation commands are gates, not mutation engines. Validation must be read-only relative to the post-engine worktree state. A validation command must not create the first commit-worthy diff or alter any engine-produced diff.

### Finding D — Validation safety violations are misrouted as syntax failure

A validation command that writes `.git/hooks/post-commit` and exits non-zero currently returns `SYNTAX_GATE_FAILED` / exit `2`, not `UNAUTHORIZED_FILE_MUTATION` / exit `3`.

Observed hostile probe result:

```json
{
  "report_status": "SYNTAX_GATE_FAILED",
  "report_exit_code": 2,
  "report_destroyed_files": []
}
```

Sprint 002.1 policy decision: safety violations outrank syntax failures. After validation, always run `.git` and worktree mutation audits regardless of validation success/failure. If validation mutates `.git` or unauthorized worktree paths, route to `UNAUTHORIZED_FILE_MUTATION` / exit `3`.

### Finding E — V47 `l2_packet` is accepted but dropped

The V47 payload carries `l2_packet`, and BLK-004 examples use engine args with `-`, implying stdin-driven packet delivery. Current decoding accepts `l2_packet` at the wire level but drops it before engine execution.

Observed hostile probe result:

```json
{
  "report_status": "SUCCESS",
  "committed_packet_txt_repr": "''",
  "expected_packet_delivered": false
}
```

Sprint 002.1 policy decision: `l2_packet` must be normalized into the internal payload and delivered to the engine process via stdin for execute actions. Empty `l2_packet` should mean empty stdin, not an error.

---

## 3. Non-Negotiable Invariants To Preserve

1. No production `git add .` or `git add -u`.
2. Stage only explicit allowlisted files with `git add -- <file>`.
3. Reject allowlist pathspec/glob/traversal/protected BLK-req hazards.
4. Clean preflight must reject pre-existing tracked, untracked, ignored, and empty untracked directory state before destructive execute/revert behavior.
5. Output remains bounded and retained logs remain bounded.
6. Timeout/flood/cancel process control must not allow late worktree mutation after return.
7. `.git` mutations are unauthorized and restored where possible.
8. Commit hooks remain disabled for BLK-pipe-created commits, including orphan initialization commits.
9. Unauthorized cleanup must remove ignored files and nested Git repositories created by the engine.
10. `--payload-stdin` and `--health` remain supported.
11. Revert remains a fast path and must not run engine, validation, staging, branch creation, or commit.
12. Branch/orphan behavior must remain deterministic and hook-disabled.
13. V47 strict router code meanings remain separated from local extension codes.
14. No Codex/live tactical engine integration is introduced.

Copy-pasteable production broad-staging check:

```bash
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
```

Copy-pasteable production direct-Git-call check:

```bash
! git grep -n -E 'exec\.Command(Context)?\("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
```

---

## 4. Standard Controller Workflow For Each Task

For each implementation task:

Code snippets in this plan are illustrative pseudocode. Implementation subagents must translate them into the existing helper style already present in the target test files and must not introduce a parallel test framework just because a snippet uses shorthand helper names.

1. Preflight:

   ```bash
   cd /home/dad/BLK-System
   git status --short --branch
   git fetch origin main
   git status --short --branch
   export PATH="$HOME/.local/bin:$PATH"
   go version
   go test ./...
   python3 -m unittest discover -s python -p 'test_*.py'
   ```

2. Read the relevant task section in this plan plus:
   - `docs/BLK-001_blk-system-master-architecture.md`, especially `blk-pipe` blast-shield scope.
   - `docs/BLK-004_blk-pipe-v47-architecture-suite.md`, especially hard bans and execution sequence.
   - `docs/outcomes/BLK-PIPE-002_sprint-002-closeout.md`, especially current deferrals.
3. Dispatch a fresh implementation subagent with strict TDD instructions.
4. Require RED evidence before implementation.
5. Inspect the diff manually.
6. Run focused tests, full tests, `go vet ./...`, Python adapter tests when relevant, safety greps, and `git diff --check`.
7. Run two fresh reviewers:
   - spec compliance review against this plan, BLK-001, and BLK-004,
   - code-quality/safety review focused on late mutations, cleanup ordering, process leaks, and overclaims.
8. If either reviewer requests changes, amend the local unpushed task commit and rerun both reviews.
9. Only the controller pushes:

   ```bash
   git push origin main
   ```

10. Create and push a matching outcome doc after each task:

    ```text
    docs/outcomes/BLK-PIPE-002.1_task-00N-outcome.md
    ```

Outcome docs must include hostile RED evidence, GREEN evidence, review results, final verification, deviations, and next task.

---

## 5. Task 1 — Enforce No-Success-With-Physical-Residue

### Objective

Make it impossible for execute success to leave unauthorized physical residue, including empty untracked directories that Git does not report in normal status/diff output.

### Files

Modify:

- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- optionally `internal/gitguard/cleanup.go` if cleanup helper API needs a context-aware variant

Expected implementation commit:

```bash
git commit -m "fix: block blk-pipe success with physical residue"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002.1_task-001-outcome.md
```

### Target Behavior

- Engine creates only allowlisted changes: `SUCCESS`, commit created, repo clean, no untracked or empty directories remain.
- Engine creates allowlisted changes plus unauthorized empty directory: `UNAUTHORIZED_FILE_MUTATION`, exit `3`, no success commit, repo physically clean after return.
- Engine creates allowlisted changes plus unauthorized untracked file, ignored file, nested Git repo, or non-empty directory: `UNAUTHORIZED_FILE_MUTATION`, exit `3`, no success commit, repo physically clean after return.
- `destroyed_files` should include the unauthorized paths when detectable. Empty directories should appear with a trailing slash, for example `ghostdir/`.

### TDD Steps

#### Step 1: Add failing empty-directory residue test

In `internal/pipe/run_test.go`, add a test like:

```go
func TestRunUnauthorizedEmptyDirectoryFailsAndCleans(t *testing.T) {
    repo := testutil.NewGitRepo(t)
    payload := payloadForEngine(t, repo,
        []string{"sh", "-c", "printf changed > README.md; mkdir ghostdir"},
        []string{"README.md"},
        nil,
    )

    code, report := runPayload(t, payload)

    if code != ExitUnauthorizedMutation {
        t.Fatalf("exit code = %d, want %d; report=%+v", code, ExitUnauthorizedMutation, report)
    }
    if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
        t.Fatalf("status = %q", report.Status)
    }
    if _, err := os.Stat(filepath.Join(repo, "ghostdir")); !errors.Is(err, os.ErrNotExist) {
        t.Fatalf("ghostdir survived cleanup: %v", err)
    }
    assertGitStatusClean(t, repo)
    assertHeadUnchanged(t, repo)
}
```

Use the existing test helper style from `internal/pipe/run_test.go`; do not invent a parallel helper framework unless necessary.

Focused RED command:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run TestRunUnauthorizedEmptyDirectoryFailsAndCleans -v
```

Expected RED before implementation: current code returns `SUCCESS` or leaves `ghostdir/` physically present.

#### Step 2: Add non-empty directory and ignored-residue regressions

Add tests proving unauthorized residue paths are caught and cleaned:

- `TestRunUnauthorizedNonEmptyDirectoryFailsAndCleans`
- `TestRunUnauthorizedIgnoredFileFailsAndCleans`
- preserve any existing nested Git repo cleanup tests.

Focused command:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestRunUnauthorized.*(Directory|Ignored)' -v
```

Expected RED where current audit misses empty directories.

#### Step 3: Implement physical residue audit

Update `internal/pipe/run.go` so post-engine/pre-commit unauthorized auditing includes:

- unstaged tracked modifications,
- untracked files,
- ignored files created after preflight,
- empty untracked directories,
- nested Git repositories/directories created by the engine.

Recommended implementation shape:

- Reuse existing helpers where possible:
  - `untrackedFiles`
  - `ignoredFileSet`
  - `emptyUntrackedDirs`
  - `mergePathSets`
  - `uniqueSorted`
- Introduce a single helper such as:

```go
func unauthorizedPhysicalResidue(repo string, allowedModified []string, allowedNew []string, baselineUntracked map[string]struct{}) ([]string, error)
```

This helper should return all unauthorized physical paths, including empty directories with trailing slash.

Policy: if the helper returns any path after engine/validation and before commit, set:

```go
report.Status = "UNAUTHORIZED_FILE_MUTATION"
report.DestroyedFiles = residue
report.Error = "engine modified files outside the allowlist"
```

Then run cleanup, preserve `HEAD`, and return `ExitUnauthorizedMutation`.

#### Step 4: Add success cleanup assertion

Add a success test proving a normal allowlisted run leaves no untracked, ignored, or empty directory residue:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestRunSuccess.*Clean' -v
```

#### Step 5: Verify

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/pipe/run.go internal/pipe/run_test.go internal/gitguard/cleanup.go
go test ./internal/pipe -run 'TestRunUnauthorized.*|TestRunSuccess.*Clean' -v
go test ./internal/pipe -v
go test ./...
go vet ./...
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
git diff --check
```

### Review Gate

Spec reviewer must confirm no `SUCCESS` path can leave unauthorized physical residue.

Code-quality reviewer must confirm cleanup ordering cannot delete pre-existing user work because clean preflight still runs before engine execution.

---

## 6. Task 2 — Reap Escaped Descendants On Timeout, Flood, and Cancel

### Objective

Prevent escaped descendants from mutating the worktree after BLK-pipe returns from engine timeout, output flood, or context cancellation.

### Files

Modify:

- `internal/execguard/command.go`
- `internal/execguard/command_test.go`
- `internal/engine/runner.go` only if its API needs to expose additional cleanup state
- `internal/engine/runner_test.go` if engine-level regression coverage is needed
- `internal/pipe/run_test.go` for integration coverage

Expected implementation commit:

```bash
git commit -m "fix: reap escaped engine descendants on bounded exits"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002.1_task-002-outcome.md
```

### Target Behavior

When `execguard.Run` exits due to timeout, output flood, or context cancellation:

- the direct process group is killed,
- active cleanup / pipe-holder discovery runs before unregistering the command,
- Linux escaped descendants holding inherited output FDs are targeted,
- BLK-pipe does not return while a discovered escaped descendant can still mutate the worktree,
- if cleanup cannot fully contain an OS-level escape, the limitation is documented in the outcome and tests prove the known inherited-pipe case is covered.

### TDD Steps

#### Step 1: Add execguard RED test for escaped timeout child

In `internal/execguard/command_test.go`, add a Linux/POSIX test with a bounded watchdog:

```go
func TestRunTimeoutReapsEscapedDescendantHoldingOutputPipeBeforeReturn(t *testing.T) {
    if runtime.GOOS != "linux" {
        t.Skip("Linux /proc pipe-holder discovery is required for this regression")
    }
    workdir := t.TempDir()
    ctx := context.Background()
    result, err := Run(ctx, Options{
        Workdir: workdir,
        Command: []string{"sh", "-c", "setsid sh -c 'sleep 1; printf late > late.txt; echo late' & sleep 10"},
        Timeout: 100 * time.Millisecond,
        MaxOutputBytes: 4096,
        Env: ScrubbedEnv(workdir),
    })
    if err != nil {
        t.Fatalf("Run returned infrastructure error: %v", err)
    }
    if !result.TimedOut {
        t.Fatalf("TimedOut=false")
    }
    time.Sleep(1500 * time.Millisecond)
    if _, err := os.Stat(filepath.Join(workdir, "late.txt")); !errors.Is(err, os.ErrNotExist) {
        t.Fatalf("escaped descendant mutated after return: %v", err)
    }
}
```

Focused RED command:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/execguard -run TestRunTimeoutReapsEscapedDescendantHoldingOutputPipeBeforeReturn -v
```

Expected RED before implementation: `late.txt` appears after return.

#### Step 2: Add flood/cancel sibling tests

Add at least one additional test for output flood or explicit context cancellation:

- `TestRunFloodReapsEscapedDescendantHoldingOutputPipeBeforeReturn`
- or `TestRunContextCancelReapsEscapedDescendantHoldingOutputPipeBeforeReturn`

Keep commands bounded and include test-level `time.After` / watchdog patterns so regressions fail promptly.

#### Step 3: Implement active cleanup before unregister

In `internal/execguard/command.go`, ensure timeout/flood/cancel paths call active cleanup while the command is still registered.

Suggested approach:

- add a helper that calls `killActiveProcessGroups(false)` for the currently active registry,
- invoke it after `cmd.Wait()`/timeout state is known and before `waitForOutputDrain` closes the reader and before deferred unregister runs,
- preserve current normal-exit behavior that waits for pipe EOF for escaped descendants,
- avoid killing `ownPID` or the process's own process group.

Do not remove existing `activeCleanupTargets` regressions.

#### Step 4: Add pipe-level integration regression

In `internal/pipe/run_test.go`, add a test like:

```go
func TestRunEngineTimeoutDoesNotAllowLateMutation(t *testing.T) { ... }
```

Expected:

- report status `ENGINE_TIMEOUT`,
- exit `ExitEngineTimeout`,
- immediate repo clean,
- after a delay, repo still clean,
- `late.txt` absent.

#### Step 5: Verify

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/execguard/command.go internal/execguard/command_test.go internal/engine/runner.go internal/engine/runner_test.go internal/pipe/run_test.go
go test ./internal/execguard -run 'TestRun.*(Timeout|Flood|Cancel).*Escaped' -v
go test -race ./internal/execguard
go test ./internal/engine -v
go test ./internal/pipe -run 'TestRunEngineTimeoutDoesNotAllowLateMutation' -v
go test ./...
go vet ./...
git diff --check
```

### Review Gate

Spec reviewer must confirm BLK-004 timeout/flood orphan behavior is materially improved and the accepted containment limits are explicit.

Code-quality reviewer must focus on process leaks, deadlocks, PID/PGID reuse hazards, Linux `/proc` assumptions, and Darwin behavior notes.

---

## 7. Task 3 — Make Validation Read-Only And Prioritize Safety Violations

### Objective

Prevent validation commands from authoring or altering the committed diff, and ensure validation-created safety violations route to `UNAUTHORIZED_FILE_MUTATION` even when validation also fails syntactically.

### Files

Modify:

- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- optionally `internal/validation/validation.go` only if result shape needs additional metadata
- optionally `internal/contracts/report.go` if additional report detail is required

Expected implementation commit:

```bash
git commit -m "fix: enforce read-only blk-pipe validation"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002.1_task-003-outcome.md
```

### Target Behavior

- Engine creates allowed diff, validation reads only and passes: `SUCCESS`, commit created.
- Engine creates allowed diff, validation reads only and fails: `SYNTAX_GATE_FAILED`, exit `2`, no commit, repo restored to `PreEngineHash`.
- Engine does nothing, validation writes an allowlisted file and passes: `UNAUTHORIZED_FILE_MUTATION`, exit `3`, no commit, repo clean.
- Engine creates allowed diff, validation modifies an allowlisted file and passes: `UNAUTHORIZED_FILE_MUTATION`, exit `3`, no commit, repo clean.
- Validation writes `.git` and fails: `UNAUTHORIZED_FILE_MUTATION`, exit `3`, no commit, repo clean.
- Validation writes unauthorized worktree path and fails: `UNAUTHORIZED_FILE_MUTATION`, exit `3`, no commit, repo clean.

### TDD Steps

#### Step 1: Add RED test proving validation cannot author first diff

In `internal/pipe/run_test.go`:

```go
func TestRunValidationCannotAuthorAllowedDiff(t *testing.T) {
    repo := testutil.NewGitRepo(t)
    payload := payloadWithValidation(t, repo,
        []string{"sh", "-c", "printf noop"},
        []string{"sh -c 'printf validation > README.md'"},
        []string{"README.md"},
        nil,
    )

    code, report := runPayload(t, payload)

    if code != ExitUnauthorizedMutation {
        t.Fatalf("exit code = %d, want %d; report=%+v", code, ExitUnauthorizedMutation, report)
    }
    assertHeadUnchanged(t, repo)
    assertGitStatusClean(t, repo)
}
```

Focused RED command:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run TestRunValidationCannotAuthorAllowedDiff -v
```

Expected RED before implementation: current code returns `SUCCESS` and commits validation output.

#### Step 2: Add RED test for validation modifying engine-produced allowed diff

Add:

```go
func TestRunValidationCannotModifyEngineProducedDiff(t *testing.T) { ... }
```

Engine writes `engine` to `README.md`; validation writes `validation` to `README.md`; expected `UNAUTHORIZED_FILE_MUTATION`, no commit, clean repo.

#### Step 3: Add RED test for safety precedence over syntax failure

Add:

```go
func TestRunValidationGitMutationOutranksSyntaxFailure(t *testing.T) { ... }
```

Validation command writes `.git/hooks/post-commit` and exits `1`. Expected:

- exit `ExitUnauthorizedMutation`,
- status `UNAUTHORIZED_FILE_MUTATION`,
- no success commit,
- `.git` restored,
- repo clean.

Also add a worktree sibling:

```go
func TestRunValidationUnauthorizedWorktreeMutationOutranksSyntaxFailure(t *testing.T) { ... }
```

#### Step 4: Add preservation test for normal validation failure

Preserve intended syntax behavior:

```go
func TestRunValidationFailureWithoutMutationStaysSyntaxGateFailed(t *testing.T) { ... }
```

Expected `SYNTAX_GATE_FAILED` / exit `2` when validation only reads or prints and exits non-zero.

#### Step 5: Implement post-engine and post-validation snapshots

Recommended implementation shape:

1. After engine success and `.git` audit, capture a worktree snapshot before validation.
2. Run all validation commands sequentially and collect logs as today.
3. After validation, always run `.git` mutation audit and worktree snapshot comparison before evaluating syntax result.
4. If validation changed `.git` or worktree state, route unauthorized and clean/restore.
5. If validation did not mutate but validation failed, route syntax failure.
6. If validation did not mutate and passed, continue staging/commit using engine-produced worktree state.

Snapshot requirements:

- detect tracked content changes,
- detect new untracked files,
- detect ignored files,
- detect empty untracked directories,
- remain bounded for repo-local test fixtures,
- do not read `.git` through the worktree snapshot; `.git` is handled by `gitSnapshot`.

Possible helper names:

```go
type worktreeSnapshot struct { ... }
func snapshotWorktree(repo string) (worktreeSnapshot, error)
func (s worktreeSnapshot) ChangedPaths(repo string) ([]string, error)
```

#### Step 6: Verify

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/pipe/run.go internal/pipe/run_test.go internal/validation/validation.go internal/contracts/report.go
go test ./internal/pipe -run 'TestRunValidation.*' -v
go test ./internal/validation -v
go test ./internal/pipe -v
go test ./...
go vet ./...
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
git diff --check
```

### Review Gate

Spec reviewer must confirm validation is now a gate and cannot author or alter the committed diff.

Code-quality reviewer must confirm mutation precedence is correct and cleanup cannot hide a validation-created safety violation behind syntax failure.

---

## 8. Task 4 — Deliver V47 `l2_packet` To Engine Stdin

### Objective

Normalize V47 `l2_packet` into the internal payload and deliver it to the engine process via stdin for execute actions.

### Files

Modify:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/execguard/command.go`
- `internal/execguard/command_test.go`
- `internal/engine/runner.go`
- `internal/engine/runner_test.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `python/test_blk_pipe_adapter.py` only if adapter payload-shape tests should assert `l2_packet` delivery intent

Expected implementation commit:

```bash
git commit -m "feat: deliver blk-pipe l2 packet to engine stdin"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002.1_task-004-outcome.md
```

### Target Behavior

- V47 payload `l2_packet` is preserved in `contracts.Payload`.
- Execute action passes `payload.L2Packet` to the engine process stdin.
- Engine args using `-` can read the packet from stdin.
- Empty `l2_packet` results in empty stdin and remains valid.
- Revert action ignores `l2_packet` as before because revert must not run engine.
- Existing legacy `engine_command` payloads without `l2_packet` continue to work.

### TDD Steps

#### Step 1: Add contract decode test

In `internal/contracts/payload_test.go`, add:

```go
func TestDecodePayloadPreservesV47L2Packet(t *testing.T) { ... }
```

Expected decoded payload field:

```go
if payload.L2Packet != "expected packet" { t.Fatalf(...) }
```

Focused RED command:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/contracts -run TestDecodePayloadPreservesV47L2Packet -v
```

Expected RED before implementation: `Payload` has no `L2Packet` field.

#### Step 2: Add execguard stdin test

In `internal/execguard/command_test.go`, add:

```go
func TestRunWritesInputToCommandStdin(t *testing.T) { ... }
```

Suggested API:

```go
type Options struct {
    Workdir        string
    Command        []string
    Timeout        time.Duration
    MaxOutputBytes int64
    Env            []string
    Stdin          io.Reader
}
```

Alternative acceptable API: `Input []byte`, if simpler. Choose one and use it consistently.

Expected command:

```go
Command: []string{"sh", "-c", "cat > packet.txt"}
Stdin: strings.NewReader("expected packet")
```

Assert `packet.txt` contains `expected packet`.

#### Step 3: Add engine runner stdin test

In `internal/engine/runner_test.go`, add a test proving `engine.Run` can pass input through to `execguard.Run`.

Prefer a backwards-compatible API if practical, for example:

```go
func Run(ctx context.Context, workdir string, command []string, maxOutputBytes int64, stdin ...string) (Result, error)
```

or a clearer options struct if the implementation accepts a wider refactor.

Do not break existing tests unless updating call sites is trivial and mechanical.

#### Step 4: Add pipe-level L2 packet test

In `internal/pipe/run_test.go`, add:

```go
func TestRunV47L2PacketDeliveredToEngineStdin(t *testing.T) { ... }
```

Payload shape:

```json
{
  "action": "execute",
  "work_dir": "/tmp/repo",
  "engine": "sh",
  "engine_args": ["-c", "cat > packet.txt"],
  "l2_packet": "EXPECTED_PACKET",
  "allowed_new_files": ["packet.txt"],
  "allowed_modified_files": []
}
```

Expected:

- `SUCCESS`,
- commit created,
- committed `packet.txt` equals `EXPECTED_PACKET`,
- repo clean.

#### Step 5: Update docs truthfully

Update `docs/BLK-010_blk-pipe-v47-hardening-cli.md` to state:

- Sprint 002.1 delivers `l2_packet` to engine stdin for execute actions.
- This still does not invoke Codex or any live LLM.
- Engine stdin is bounded by payload bytes only if/when a future payload-size cap exists. Do not overclaim payload-byte bounding if it is not implemented.

#### Step 6: Verify

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/contracts/payload.go internal/contracts/payload_test.go internal/execguard/command.go internal/execguard/command_test.go internal/engine/runner.go internal/engine/runner_test.go internal/pipe/run.go internal/pipe/run_test.go
go test ./internal/contracts -run TestDecodePayloadPreservesV47L2Packet -v
go test ./internal/execguard -run TestRunWritesInputToCommandStdin -v
go test ./internal/engine -run 'TestRun.*Input|TestRun.*Stdin' -v
go test ./internal/pipe -run TestRunV47L2PacketDeliveredToEngineStdin -v
go test ./...
python3 -m unittest discover -s python -p 'test_*.py'
go vet ./...
git diff --check
```

### Review Gate

Spec reviewer must confirm V47 `l2_packet` is no longer silently dropped and that revert remains engine-free.

Code-quality reviewer must confirm stdin handling cannot deadlock and does not unbound retained output or logs.

---

## 9. Task 5 — Documentation, Regression Matrix, and Sprint 002.1 Closeout

### Objective

Document completed Sprint 002.1 behavior, update prior overclaims, and close the remediation sprint with traceable verification.

### Files

Create:

- `docs/outcomes/BLK-PIPE-002.1_task-005-outcome.md`
- `docs/outcomes/BLK-PIPE-002.1_sprint-002.1-closeout.md`

Modify as needed:

- `README.md`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- this plan file only if execution discovers a necessary correction before closeout

Expected documentation/outcome commits:

```bash
git commit -m "docs: record BLK-pipe sprint 002.1 task 5 outcome"
git commit -m "docs: close out blk-pipe sprint 002.1"
```

The Task 5 outcome document records the documentation/closeout task evidence. The sprint closeout document records final sprint-level evidence and may use the two-commit hash-recording pattern if it must contain its own commit hash.

If the closeout doc must contain its own closeout commit hash, use the two-commit docs pattern from `blk-system-sprint-execution`:

1. create/commit the closeout doc with pending closeout hash,
2. capture that commit hash,
3. patch the doc to record it,
4. commit the metadata update separately.

### Required Closeout Content

The Sprint 002.1 closeout doc must include:

- final implementation commit hash for each task,
- outcome document paths for each task,
- hostile RED evidence for all five findings,
- GREEN evidence proving fixes,
- final full verification summary,
- updated safety guarantee list,
- remaining deferrals,
- explicit statement that Sprint 002.1 does not run Codex,
- explicit statement whether Sprint 003 planning/readiness may proceed; any live Codex or live LLM run remains blocked until separate explicit user approval.

### Required Regression Matrix

Closeout must include this matrix with final observed status:

| Probe | Expected after Sprint 002.1 |
|---|---|
| Engine creates allowlisted change plus `ghostdir/` | `UNAUTHORIZED_FILE_MUTATION`, exit `3`, no commit, `ghostdir/` absent |
| Engine timeout with session-escaped child writing `late.txt` after delay | `ENGINE_TIMEOUT`, exit `6`, no late `late.txt`, repo clean after delay |
| No-op engine, validation writes allowlisted file | `UNAUTHORIZED_FILE_MUTATION`, exit `3`, no commit |
| Validation writes `.git/hooks/post-commit` and exits `1` | `UNAUTHORIZED_FILE_MUTATION`, exit `3`, `.git` restored |
| V47 `l2_packet` with engine reading stdin | `SUCCESS`, committed packet content matches payload |

### Final Verification

Run:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./...
go vet ./...
python3 -m unittest discover -s python -p 'test_*.py'
go run ./cmd/blk-pipe --health
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
! git grep -n -E 'exec\.Command(Context)?\("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
! git grep -n -E 'git[^\n]*diff[^\n]*\.\.\.' -- '*.go' ':!*_test.go' docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/plans/BLK-PIPE-002.1_hostile-review-remediation.md docs/outcomes/BLK-PIPE-002.1_task-*-outcome.md docs/outcomes/BLK-PIPE-002.1_sprint-002.1-closeout.md
git diff --check
git status --short --branch
```

Remove Python `__pycache__` if adapter tests generate it:

```bash
rm -rf python/__pycache__
git status --short --branch
```

### Review Gate

Spec reviewer must compare the closeout against this plan and verify every hostile finding is either fixed or explicitly deferred with user approval.

Code-quality/doc reviewer must check Markdown formatting, no trailing whitespace, balanced fences, truthful commands, no Codex invocation instructions, no broad staging examples, no `git stash`, and no triple-dot diff instruction.

---

## 10. Final Sprint 002.1 Acceptance Criteria

Sprint 002.1 is complete when all are true:

1. `go test ./...` passes.
2. `go vet ./...` passes.
3. Python adapter tests pass.
4. `go run ./cmd/blk-pipe --health` remains deterministic.
5. No production broad staging command exists.
6. No direct production Git command exists outside `internal/gitguard/command.go` and `internal/testutil/**` carveout.
7. No triple-dot Git diff appears in production Go or Sprint 002.1 docs.
8. Unauthorized empty directories cannot survive a `SUCCESS` run.
9. Unauthorized physical residue returns `UNAUTHORIZED_FILE_MUTATION` / exit `3` and is cleaned.
10. Timeout/flood/cancel paths do not allow known inherited-pipe escaped descendants to mutate after return.
11. Validation cannot author or alter committed diffs.
12. Validation-created safety violations route to `UNAUTHORIZED_FILE_MUTATION` / exit `3`, even if validation exits non-zero.
13. V47 `l2_packet` is delivered to engine stdin for execute actions.
14. Revert remains engine-free and validation-free.
15. Branch/orphan behavior remains green.
16. Signal/panic fatal behavior remains green.
17. No Codex/live LLM integration is introduced.
18. Every task has a pushed outcome document.
19. Sprint 002.1 closeout is pushed and documents whether Sprint 003 planning/readiness may proceed; live Codex/live LLM execution remains blocked pending separate explicit user approval.

---

## 11. Recommended Sprint 003 Gate After Sprint 002.1

Sprint 003 should remain blocked until Sprint 002.1 closeout explicitly says the hostile regression matrix is green.

If Sprint 002.1 passes, Sprint 003 may plan controlled tactical-engine integration readiness, but should still start with fake/dry-run parity tests before any live Codex call.

Recommended Sprint 003 seed scope after this sprint:

1. Decide whether tactical execution invokes Codex directly through `engine`/`engine_args` or through a higher-level Hermes/Python orchestrator.
2. Add CEB/L2 packet fixture tests around payload construction and stdin delivery.
3. Add fake-Codex/dry-run parity tests before any live Codex run.
4. Add HITL safety gates before live model execution.
5. Add BLK-test integration only after local validation semantics remain stable.
6. Decide whether local extension exit codes `6`, `7`, and `9` should remain or collapse into strict V47 router families.

---

## 12. Quick Resume Prompt For Future Hermes

If context is lost, resume with:

```text
Open /home/dad/BLK-System/docs/plans/BLK-PIPE-002.1_hostile-review-remediation.md. Execute Task 1 next using blk-system-sprint-execution, strict TDD, two-stage review, controller-only push, and a pushed/attached outcome doc. This sprint remediates post-Sprint 002 hostile review findings: no-success-with-physical-residue, escaped-descendant timeout/flood cleanup, read-only validation with safety precedence, and V47 l2_packet stdin delivery. Do not integrate Codex/live LLMs in Sprint 002.1.
```
