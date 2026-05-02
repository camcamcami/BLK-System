# BLK-pipe Sprint 001 — Deterministic Execution Kernel Implementation Plan

> **For Hermes:** Use `subagent-driven-development` skill to implement this plan task-by-task. Use TDD for every code-producing task. Do not integrate Codex or any live LLM engine in this sprint.

**Status:** Planned
**Date:** 2026-05-02
**Target Component:** `blk-pipe`
**Primary Doctrine:** BLK-001, BLK-003, BLK-004, BLK-006

**Goal:** Build the first deterministic Go CLI kernel for `blk-pipe`: a local binary that accepts a JSON payload, executes a fake tactical engine inside a Git working tree, stages only allowlisted files, destroys unauthorized edits, and emits a deterministic JSON report with BLK-defined exit behavior.

**Architecture:** `blk-pipe` is a compiled transport and safety layer, not an LLM client and not an architectural decision-maker. The first sprint isolates the safety kernel from all future orchestration complexity by using fake engine scripts and temporary Git repositories. Later sprints can add Codex-specific invocation only after file-boundary enforcement is proven.

**Tech Stack:** Go 1.22+, standard library only for Sprint 001, POSIX shell fixtures for fake engines, Git CLI, Go `testing` package.

---

## 0. Strategic Decision

BLK-pipe is the correct first implementation target because it is the deterministic safety kernel for the rest of BLK-System. It can be built and tested without Discord, without LLM APIs, without BLK-req storage, and without the BLK-test MCP server.

The first sprint must therefore avoid expanding into the full autonomous loop. The sprint is successful only when the following statement is true:

> Given a Git repository and a bounded payload, `blk-pipe` can run a local fake engine, preserve only explicitly allowlisted file changes, destroy all unauthorized mutations, and report the outcome deterministically.

---

## 1. Explicit Non-Goals

Do **not** implement any of the following in Sprint 001:

- Codex CLI integration.
- Discord integration.
- BLK-req artifact authoring or promotion.
- BLK-test MCP server.
- RTM generation.
- BEB/BEO full document lifecycle.
- Network access.
- Cross-platform Windows behavior.
- Long-running daemon/service mode.

This sprint produces a local command-line binary only.

---

## 2. Proposed Repository Layout

Create the initial implementation under these paths:

```text
go.mod
cmd/blk-pipe/main.go
internal/contracts/payload.go
internal/contracts/report.go
internal/gitguard/status.go
internal/gitguard/stage.go
internal/gitguard/cleanup.go
internal/engine/runner.go
internal/pipe/run.go
internal/pipe/exitcodes.go
internal/testutil/gitrepo.go
internal/testutil/fakeengine.go
testdata/engines/success.sh
testdata/engines/unauthorized.sh
testdata/engines/noop.sh
testdata/engines/flood.sh
testdata/engines/fail.sh
```

Future sprint candidates, not part of Sprint 001:

```text
internal/revert/
internal/orchestrator/
python/blk_pipe_adapter.py
schemas/blk-pipe-payload.schema.json
schemas/blk-pipe-report.schema.json
```

---

## 3. Sprint 001 Payload Contract

Sprint 001 uses a deliberately small payload that is compatible with the broader BLK-004 direction but does not attempt the full V47 schema.

```json
{
  "action": "execute",
  "workdir": "/absolute/path/to/git/repo",
  "engine_command": ["/absolute/path/to/fake-engine.sh"],
  "allowed_modified_files": ["src/allowed.txt"],
  "allowed_new_files": ["src/new.txt"],
  "timeout_seconds": 60,
  "max_output_bytes": 52428800
}
```

### Required validation rules

- `action` must equal `execute` for Sprint 001.
- `workdir` must be absolute.
- `engine_command` must contain at least one element.
- allowlist paths must be relative, clean paths.
- allowlist paths must not contain `..`.
- `timeout_seconds` must be greater than 0.
- `max_output_bytes` must be greater than 0.
- Any allowlist entry matching `^docs/(requirements|use_cases)/.*` must be rejected before engine execution.

---

## 4. Sprint 001 Report Contract

Every run writes exactly one JSON report to stdout.

```json
{
  "status": "SUCCESS",
  "action": "execute",
  "workdir": "/absolute/path/to/git/repo",
  "commit_hash": "abc123...",
  "staged_files": ["src/allowed.txt"],
  "destroyed_files": ["src/unauthorized.txt"],
  "engine_exit_code": 0,
  "engine_output_bytes": 1234,
  "error": ""
}
```

### Initial statuses

| Status | Meaning | Exit code |
|---|---|---:|
| `SUCCESS` | allowlisted changes were committed or no valid changes were needed | 0 |
| `INVALID_PAYLOAD` | payload parse/validation failed | 2 |
| `UNAUTHORIZED_FILE_MUTATION` | engine changed files outside allowlist or attempted protected docs mutation | 3 |
| `ENGINE_FAILED` | engine exited non-zero without a more specific BLK-pipe failure | 4 |
| `FATAL_OUTPUT_FLOOD` | combined stdout/stderr exceeded `max_output_bytes` | 5 |
| `ENGINE_TIMEOUT` | engine exceeded `timeout_seconds` | 6 |
| `GIT_DIRTY` | repository was dirty before execution | 7 |
| `INTERNAL_ERROR` | unexpected infrastructure failure | 9 |

Note: BLK-004 also reserves exit code 4 for revert ancestry failures. Sprint 001 does not implement `revert`; Sprint 002 must reconcile the final shared exit-code registry before adding revert behavior.

---

## 5. Acceptance Criteria

Sprint 001 is complete when all are true:

1. `go test ./...` passes.
2. `go run ./cmd/blk-pipe --health` prints a deterministic health JSON and exits 0.
3. A fake engine that modifies only allowlisted files succeeds.
4. A fake engine that modifies any unallowlisted file returns `UNAUTHORIZED_FILE_MUTATION` and exit 3.
5. A fake engine that touches `docs/requirements/...` or `docs/use_cases/...` is denied before execution when those paths appear in allowlists.
6. Unauthorized files are physically removed or reverted from the worktree.
7. No code uses `git add .` or `git add -u`.
8. Tests prove only explicit allowlist entries are staged.
9. Hangs and floods are bounded.
10. The repository remains clean after the test suite.

---

## 6. Implementation Tasks

### Task 1: Initialize Go module and CLI skeleton

**Objective:** Create the minimal Go module and `blk-pipe` command entrypoint.

**Files:**

- Create: `go.mod`
- Create: `cmd/blk-pipe/main.go`
- Create: `internal/pipe/exitcodes.go`

**Step 1: Create `go.mod`**

```go
module github.com/camcamcami/BLK-System

go 1.22
```

**Step 2: Add exit constants**

```go
package pipe

const (
    ExitSuccess              = 0
    ExitInvalidPayload       = 2
    ExitUnauthorizedMutation = 3
    ExitEngineFailed         = 4
    ExitOutputFlood          = 5
    ExitEngineTimeout        = 6
    ExitGitDirty             = 7
    ExitInternalError        = 9
)
```

**Step 3: Add `--health` path**

`cmd/blk-pipe/main.go` should initially support only:

```bash
go run ./cmd/blk-pipe --health
```

Expected stdout:

```json
{"status":"OK","component":"blk-pipe"}
```

**Step 4: Verify**

Run:

```bash
go test ./...
go run ./cmd/blk-pipe --health
```

Expected: tests pass, health JSON printed, exit 0.

**Step 5: Commit**

```bash
git add go.mod cmd/blk-pipe/main.go internal/pipe/exitcodes.go
git commit -m "feat: initialize blk-pipe Go CLI"
```

---

### Task 2: Define payload and report contracts

**Objective:** Add typed Go structs for the Sprint 001 payload/report contracts.

**Files:**

- Create: `internal/contracts/payload.go`
- Create: `internal/contracts/report.go`
- Create: `internal/contracts/payload_test.go`

**Step 1: Write failing validation tests**

Test cases:

- valid payload passes,
- relative `workdir` fails,
- empty `engine_command` fails,
- `../escape.txt` allowlist path fails,
- `docs/requirements/active/REQ-001.md` allowlist path fails.

**Step 2: Implement payload struct**

```go
package contracts

type Payload struct {
    Action               string   `json:"action"`
    Workdir              string   `json:"workdir"`
    EngineCommand        []string `json:"engine_command"`
    AllowedModifiedFiles []string `json:"allowed_modified_files"`
    AllowedNewFiles      []string `json:"allowed_new_files"`
    TimeoutSeconds       int      `json:"timeout_seconds"`
    MaxOutputBytes       int64    `json:"max_output_bytes"`
}
```

**Step 3: Implement report struct**

```go
package contracts

type Report struct {
    Status            string   `json:"status"`
    Action            string   `json:"action"`
    Workdir           string   `json:"workdir"`
    CommitHash        string   `json:"commit_hash"`
    StagedFiles       []string `json:"staged_files"`
    DestroyedFiles    []string `json:"destroyed_files"`
    EngineExitCode    int      `json:"engine_exit_code"`
    EngineOutputBytes int64    `json:"engine_output_bytes"`
    Error             string   `json:"error"`
}
```

**Step 4: Implement validation**

Add `func (p Payload) Validate() error`.

**Step 5: Verify**

Run:

```bash
go test ./internal/contracts -v
```

Expected: all validation tests pass.

**Step 6: Commit**

```bash
git add internal/contracts
git commit -m "feat: define blk-pipe payload contracts"
```

---

### Task 3: Add Git test repository utility

**Objective:** Provide a reusable helper for integration tests using real temporary Git repositories.

**Files:**

- Create: `internal/testutil/gitrepo.go`
- Create: `internal/testutil/gitrepo_test.go`

**Step 1: Write failing test**

Test helper must:

- create temp dir,
- run `git init`,
- configure local user name/email,
- create an initial commit,
- return repo path.

**Step 2: Implement helper**

Expose:

```go
func NewGitRepo(t testing.TB) string
func WriteFile(t testing.TB, repo string, rel string, content string)
func RunGit(t testing.TB, repo string, args ...string) string
```

**Step 3: Verify**

Run:

```bash
go test ./internal/testutil -v
```

Expected: helper creates a clean Git repository with one commit.

**Step 4: Commit**

```bash
git add internal/testutil
git commit -m "test: add git repository test utility"
```

---

### Task 4: Implement preflight clean-repo check

**Objective:** Abort execution if the worktree is dirty before the fake engine starts.

**Files:**

- Create: `internal/gitguard/status.go`
- Create: `internal/gitguard/status_test.go`

**Step 1: Write failing tests**

Cases:

- clean repo returns nil,
- modified tracked file returns dirty error,
- untracked file returns dirty error.

**Step 2: Implement status check**

Use:

```bash
git status --porcelain
```

No output means clean.

**Step 3: Verify**

Run:

```bash
go test ./internal/gitguard -run TestCleanRepo -v
```

Expected: clean/dirty status tests pass.

**Step 4: Commit**

```bash
git add internal/gitguard/status.go internal/gitguard/status_test.go
git commit -m "feat: enforce clean git preflight"
```

---

### Task 5: Implement bounded fake engine runner

**Objective:** Run a local command with timeout and output byte cap.

**Files:**

- Create: `internal/engine/runner.go`
- Create: `internal/engine/runner_test.go`
- Create: `testdata/engines/success.sh`
- Create: `testdata/engines/fail.sh`
- Create: `testdata/engines/flood.sh`

**Step 1: Write failing tests**

Cases:

- success script exits 0,
- fail script returns non-zero exit code,
- timeout kills sleeping process,
- output flood kills flood script.

**Step 2: Implement runner**

Expose:

```go
type Result struct {
    ExitCode int
    OutputBytes int64
    TimedOut bool
    Flooded bool
}

func Run(ctx context.Context, workdir string, command []string, maxOutputBytes int64) (Result, error)
```

**Step 3: Verify**

Run:

```bash
go test ./internal/engine -v
```

Expected: all runner tests pass.

**Step 4: Commit**

```bash
git add internal/engine testdata/engines
git commit -m "feat: add bounded engine runner"
```

---

### Task 6: Implement allowlist-only staging

**Objective:** Stage only explicitly allowlisted modified/new files; never stage everything.

**Files:**

- Create: `internal/gitguard/stage.go`
- Create: `internal/gitguard/stage_test.go`

**Step 1: Write failing tests**

Cases:

- modified allowlisted file is staged,
- new allowlisted file is staged,
- unallowlisted changed file is not staged,
- no use of broad staging commands.

**Step 2: Implement staging**

Use only explicit paths:

```bash
git add -- <path>
```

Never use:

```bash
git add .
git add -u
```

**Step 3: Verify**

Run:

```bash
go test ./internal/gitguard -run TestStageAllowlist -v
```

Expected: only allowlisted paths appear in `git diff --cached --name-only`.

**Step 4: Commit**

```bash
git add internal/gitguard/stage.go internal/gitguard/stage_test.go
git commit -m "feat: stage only allowlisted files"
```

---

### Task 7: Implement unauthorized mutation cleanup

**Objective:** Physically remove/revert unallowlisted changes after allowed files are staged.

**Files:**

- Create: `internal/gitguard/cleanup.go`
- Create: `internal/gitguard/cleanup_test.go`

**Step 1: Write failing tests**

Cases:

- unallowlisted tracked modifications are reverted,
- unallowlisted untracked files are deleted,
- staged allowlisted changes remain staged.

**Step 2: Implement cleanup**

Use carefully bounded Git commands:

```bash
git checkout -- .
git clean -fd
```

This is allowed only after explicit allowlisted files have already been staged.

**Step 3: Verify**

Run:

```bash
go test ./internal/gitguard -run TestCleanup -v
```

Expected: unauthorized mutations are gone and allowlisted staged diff remains.

**Step 4: Commit**

```bash
git add internal/gitguard/cleanup.go internal/gitguard/cleanup_test.go
git commit -m "feat: destroy unauthorized mutations"
```

---

### Task 8: Implement pipe execution orchestration

**Objective:** Wire validation, clean preflight, engine run, staging, cleanup, commit, and report generation.

**Files:**

- Create: `internal/pipe/run.go`
- Create: `internal/pipe/run_test.go`
- Modify: `cmd/blk-pipe/main.go`

**Step 1: Write failing integration tests**

Cases:

- success engine modifies `src/allowed.txt`, run exits 0, report status `SUCCESS`, commit exists,
- unauthorized engine modifies `src/unauthorized.txt`, run exits 3, unauthorized file absent after run,
- dirty repo before run exits 7,
- failing engine exits 4.

**Step 2: Implement runner orchestration**

Execution sequence:

1. parse payload,
2. validate payload,
3. assert clean repo,
4. run fake engine,
5. map timeout/flood/engine failure,
6. stage allowed paths,
7. cleanup unauthorized mutations,
8. if staged diff exists, commit with deterministic message,
9. emit report.

Suggested deterministic commit message:

```text
blk-pipe: apply bounded engine changes
```

**Step 3: Verify**

Run:

```bash
go test ./internal/pipe -v
go test ./...
```

Expected: all package and integration tests pass.

**Step 4: Commit**

```bash
git add internal/pipe cmd/blk-pipe/main.go
git commit -m "feat: orchestrate bounded blk-pipe execution"
```

---

### Task 9: Add protected BLK-req path deny tests

**Objective:** Enforce BLK-006 hard-deny for `docs/requirements/*` and `docs/use_cases/*` allowlist entries.

**Files:**

- Modify: `internal/contracts/payload_test.go`
- Modify: `internal/pipe/run_test.go`

**Step 1: Write failing tests**

Cases:

- payload with `allowed_modified_files: ["docs/requirements/active/REQ-001.md"]` fails validation,
- payload with `allowed_new_files: ["docs/use_cases/staging/UC-001.md"]` fails validation,
- engine is not invoked when protected path validation fails.

**Step 2: Implement or adjust validation**

Ensure the regex is exactly:

```regexp
^docs/(requirements|use_cases)/.*
```

**Step 3: Verify**

Run:

```bash
go test ./internal/contracts ./internal/pipe -v
```

Expected: protected BLK-req paths are rejected pre-execution.

**Step 4: Commit**

```bash
git add internal/contracts internal/pipe
git commit -m "feat: hard-deny blk-req artifact mutations"
```

---

### Task 10: Add CLI payload file support

**Objective:** Make the CLI accept a payload JSON file.

**Files:**

- Modify: `cmd/blk-pipe/main.go`
- Create: `cmd/blk-pipe/main_test.go` if testable without shelling out, otherwise cover via `internal/pipe` and smoke command.

**Step 1: Add CLI contract**

Supported invocations:

```bash
blk-pipe --health
blk-pipe --payload /absolute/path/to/payload.json
```

**Step 2: Verify manually**

Run:

```bash
go run ./cmd/blk-pipe --health
go test ./...
```

Expected: health and tests pass.

**Step 3: Commit**

```bash
git add cmd/blk-pipe
git commit -m "feat: add blk-pipe payload CLI"
```

---

### Task 11: Add documentation for Sprint 001 CLI

**Objective:** Document the first usable command contract for local developers.

**Files:**

- Create: `docs/BLK-009_blk-pipe-sprint-001-cli.md`
- Modify: `README.md`

**Step 1: Document commands**

Include:

```bash
go test ./...
go run ./cmd/blk-pipe --health
go run ./cmd/blk-pipe --payload /tmp/payload.json
```

**Step 2: Document non-goals**

Explicitly say Sprint 001 does not run Codex.

**Step 3: Verify**

Run:

```bash
git diff --check
go test ./...
```

**Step 4: Commit**

```bash
git add README.md docs/BLK-009_blk-pipe-sprint-001-cli.md
git commit -m "docs: describe blk-pipe sprint 001 CLI"
```

---

## 7. Verification Matrix

| Case | Fixture | Expected status | Exit |
|---|---|---:|---:|
| Health check | none | `OK` | 0 |
| Valid allowlisted edit | `success.sh` | `SUCCESS` | 0 |
| Engine failure | `fail.sh` | `ENGINE_FAILED` | 4 |
| Output flood | `flood.sh` | `FATAL_OUTPUT_FLOOD` | 5 |
| Timeout | sleep fixture | `ENGINE_TIMEOUT` | 6 |
| Dirty repo preflight | pre-modified repo | `GIT_DIRTY` | 7 |
| Unauthorized mutation | `unauthorized.sh` | `UNAUTHORIZED_FILE_MUTATION` | 3 |
| Protected requirements path | payload validation | `INVALID_PAYLOAD` | 2 |
| Protected use-case path | payload validation | `INVALID_PAYLOAD` | 2 |

---

## 8. Final Sprint Closeout Requirements

Before declaring Sprint 001 complete:

```bash
git status --short
go test ./...
git grep -n "git add \.\|git add -u" -- . ':!docs/plans/BLK-PIPE-001_deterministic-execution-kernel.md'
```

Expected:

- no uncommitted changes,
- all tests pass,
- no production code contains broad Git staging commands.

The closeout note must include:

- final commit hash,
- list of implemented exit codes,
- test output summary,
- any deviation from BLK-004/BLK-006,
- explicit statement that Codex integration remains deferred.

---

## 9. Recommended Next Sprint After This

If Sprint 001 succeeds, Sprint 002 should implement the V47 hardening layer:

- final V47 payload schema,
- revert ancestry gate,
- environment scrubbing,
- `GIT_SSH_COMMAND` hardening,
- 15-minute default execution timebox,
- Python adapter contract,
- final exit-code registry reconciliation.

Only after Sprint 002 should BLK-pipe invoke Codex or any live tactical LLM engine.
