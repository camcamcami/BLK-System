# BLK-pipe Sprint 001 — Task 5 Outcome

**Status:** Complete
**Date:** 2026-05-02
**Task:** Implement bounded fake engine runner
**Commit:** `a86af82 feat: add bounded engine runner`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Run a local fake engine command from BLK-pipe with deterministic process bounds before later sprint tasks wire staging, cleanup, commits, and final report generation.

Task 5 introduces `internal/engine`, the first execution component in the BLK-pipe safety kernel. The runner is responsible for starting a local command in a target working directory, collecting bounded combined stdout/stderr byte counts, honoring caller-driven timeouts through `context.Context`, detecting output floods, and reporting engine exit state without confusing ordinary engine failure with BLK-pipe infrastructure failure.

This task intentionally does **not** implement CLI payload support, pipe orchestration, allowlist staging, unauthorized mutation cleanup, commit creation, report emission, Codex integration, Discord integration, or network behavior.

---

## 2. Files Added

```text
internal/engine/runner.go
internal/engine/runner_test.go
testdata/engines/success.sh
testdata/engines/fail.sh
testdata/engines/flood.sh
```

The engine fixtures are executable shell scripts committed under `testdata/engines`.

---

## 3. Behavior Implemented

### 3.1 Public API

```go
type Result struct {
    ExitCode int
    OutputBytes int64
    TimedOut bool
    Flooded bool
}

func Run(ctx context.Context, workdir string, command []string, maxOutputBytes int64) (Result, error)
```

### 3.2 Successful engine execution

`Run` executes the supplied local command in the supplied working directory.

For a successful command:

- `Result.ExitCode` is `0`,
- `Result.OutputBytes` counts combined stdout/stderr bytes read from the process,
- `Result.TimedOut` is `false`,
- `Result.Flooded` is `false`,
- returned error is `nil`.

Covered by:

```text
TestRunSuccessScriptExitsZero
```

### 3.3 Non-zero engine exit

A fake engine exiting non-zero is treated as an engine result, not a BLK-pipe infrastructure error.

For a failing command:

- `Result.ExitCode` contains the non-zero engine exit code,
- output bytes are still counted,
- returned error is `nil`.

This keeps later `pipe` orchestration able to map ordinary engine failure to the correct BLK-pipe report/exit behavior rather than treating it as an internal runner crash.

Covered by:

```text
TestRunFailScriptReportsNonZeroExitWithoutInfrastructureError
```

### 3.4 Timeout handling

Timeout is driven by the caller's `context.Context`.

The implementation uses `exec.CommandContext` and assigns the command to its own process group on Linux. On cancellation, the runner kills the process group, which handles shell child processes in the Sprint 001 Linux/POSIX scope better than killing only the immediate shell process.

Covered by:

```text
TestRunTimeoutKillsSleepingProcess
```

### 3.5 Output flood handling

The runner reads combined stdout/stderr through an OS pipe and counts bytes as they are read. It does not accumulate unbounded output in memory.

When read bytes exceed `maxOutputBytes`:

- `Result.Flooded` becomes `true`,
- the command process group is killed,
- `Result.OutputBytes` records the bytes observed,
- returned error remains `nil` for the expected flood outcome.

Covered by:

```text
TestRunOutputFloodKillsFloodScript
```

### 3.6 Inherited pipe writer hang prevention

Code quality review identified an important process-race hazard: a direct shell process can exit while a background child keeps inherited stdout/stderr pipe file descriptors open. If the runner only waits for pipe EOF after the direct process exits, BLK-pipe can hang forever waiting on a child that outlived the shell.

A regression test now covers this case:

```text
TestRunDoesNotHangWhenChildInheritsOutputPipeAfterParentExit
```

The fix kills the command process group after the direct process exits, before the runner waits for output draining to finish. This closes inherited pipe writers from child processes and prevents output-drain hangs.

### 3.7 Start failure handling

If the command cannot start, `Run` returns an infrastructure error rather than a fake engine result.

Covered by:

```text
TestRunStartFailureIsInfrastructureError
```

---

## 4. TDD Evidence

### 4.1 Initial RED

Tests were written before the initial production implementation.

Initial focused test command:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/engine -v
```

Initial failure evidence:

```text
# github.com/camcamcami/BLK-System/internal/engine [github.com/camcamcami/BLK-System/internal/engine.test]
internal/engine/runner_test.go:19:17: undefined: Run
internal/engine/runner_test.go:41:17: undefined: Run
internal/engine/runner_test.go:65:17: undefined: Run
internal/engine/runner_test.go:86:17: undefined: Run
internal/engine/runner_test.go:105:12: undefined: Run
FAIL
```

This confirmed the tests were exercising a missing API, not merely passing against existing behavior.

### 4.2 Initial GREEN

After implementing the first runner version:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/engine -v
go test ./...
git diff --check
```

Initial focused and full test suites passed.

### 4.3 Review-Driven RED

The first code quality review found a blocking inherited-pipe hang risk.

Regression test added:

```text
TestRunDoesNotHangWhenChildInheritsOutputPipeAfterParentExit
```

Focused regression command:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/engine -run TestRunDoesNotHangWhenChildInheritsOutputPipeAfterParentExit -count=1 -v
```

RED evidence before the fix:

```text
Run did not return after direct process exited while child held output pipe open
```

### 4.4 Final GREEN

Final focused verification:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/engine -v
```

Result:

```text
=== RUN   TestRunSuccessScriptExitsZero
--- PASS: TestRunSuccessScriptExitsZero
=== RUN   TestRunFailScriptReportsNonZeroExitWithoutInfrastructureError
--- PASS: TestRunFailScriptReportsNonZeroExitWithoutInfrastructureError
=== RUN   TestRunTimeoutKillsSleepingProcess
--- PASS: TestRunTimeoutKillsSleepingProcess
=== RUN   TestRunOutputFloodKillsFloodScript
--- PASS: TestRunOutputFloodKillsFloodScript
=== RUN   TestRunDoesNotHangWhenChildInheritsOutputPipeAfterParentExit
--- PASS: TestRunDoesNotHangWhenChildInheritsOutputPipeAfterParentExit
=== RUN   TestRunStartFailureIsInfrastructureError
--- PASS: TestRunStartFailureIsInfrastructureError
PASS
ok github.com/camcamcami/BLK-System/internal/engine
```

Full repository verification also passed:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./...
git diff --check
```

---

## 5. Review Results

### 5.1 Initial Spec Compliance Review

Verdict: **PASS**

Gaps: none.

Spec review confirmed:

- required files were added,
- required public API exists,
- required tests exist,
- success, failure, timeout, and flood behavior are covered,
- scope stayed limited to the bounded engine runner.

### 5.2 Initial Code Quality Review

Verdict: **REQUEST_CHANGES**

Blocking issue found:

- `Run` could hang when the direct process exited while a child process kept inherited stdout/stderr pipe file descriptors open.

Root cause:

- The flood-kill goroutine stopped as soon as `cmd.Wait()` returned.
- `Run` then waited on output draining.
- A background child could keep the pipe open after the direct shell process exited.
- Context cancellation no longer killed that child once the direct process had already exited.

Reviewer repro pattern:

```go
engine.Run(ctx, ".", []string{"sh", "-c", "yes flood & exit 0"}, 4096)
```

### 5.3 Review Fix

Fix implemented with TDD:

- added inherited-pipe regression coverage,
- killed the command process group after direct process exit before waiting for output draining to complete,
- amended the unpushed implementation commit.

### 5.4 Final Spec Compliance Review

Verdict: **PASS**

Gaps: none.

### 5.5 Final Code Quality Review

Verdict: **APPROVED**

Critical issues: none.

Important issues: none.

Minor issues: none blocking.

The final review explicitly re-checked:

- process timeout behavior,
- shell-child process handling,
- output flood behavior,
- inherited pipe hang prevention,
- non-zero exit mapping,
- start failure handling,
- deterministic tests,
- absence of scope creep.

---

## 6. Final Verification

Final verification before pushing the implementation commit:

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -l internal/engine/runner.go internal/engine/runner_test.go internal/gitguard/status.go internal/gitguard/status_test.go internal/testutil/gitrepo.go internal/testutil/gitrepo_test.go internal/contracts/payload.go internal/contracts/payload_test.go internal/contracts/report.go internal/pipe/exitcodes.go internal/pipe/exitcodes_test.go cmd/blk-pipe/main.go cmd/blk-pipe/main_test.go
go test ./internal/engine -v
go test -race ./internal/engine
go test ./internal/engine -count=20
go test ./...
git diff --check
git status --short --branch
git log --oneline --decorate -4
git push origin main
git status --short --branch
```

Result:

```text
gofmt check                    PASS
go test ./internal/engine -v   PASS
go test -race ./internal/engine PASS
go test ./internal/engine -count=20 PASS
go test ./...                  PASS
git diff --check               PASS
implementation push            PASS
repo state after push          clean, aligned with origin/main
```

Implementation commit pushed:

```text
a86af82 feat: add bounded engine runner
```

Outcome-document verification before the documentation commit:

```bash
python3 - <<'PY'
from pathlib import Path
p = Path('docs/outcomes/BLK-PIPE-001_task-005-outcome.md')
text = p.read_text()
assert text.startswith('# BLK-pipe Sprint 001')
assert text.count(chr(96) * 3) % 2 == 0
assert '**Status:** Complete' in text
assert 'a86af82 feat: add bounded engine runner' in text
PY
git diff --check
```

---

## 7. Deviations / Notes

- The plan required timeout and output cap behavior; the implementation additionally hardens process cleanup using Linux process groups to handle shell child processes within the Sprint 001 POSIX/Linux scope.
- `Run` treats non-zero engine exit as a normal engine result, not an infrastructure error. Later orchestration can map this into `ENGINE_FAILED` report/exit behavior.
- Output is counted, not retained, preventing unbounded memory growth from fake engine output.
- The runner currently reports `OutputBytes` as bytes read and observed; it does not expose captured output content.
- `maxOutputBytes < 0` is rejected as an invalid runner call. Payload-level validation already rejects non-positive values before orchestration.
- No external Go dependencies were added.
- No live LLM, network, Discord, Codex, staging, cleanup, or pipe orchestration behavior was added.

---

## 8. Next Task

Proceed to Sprint 001 Task 6: implement allowlist-only staging.

Task 6 will add:

```text
internal/gitguard/stage.go
internal/gitguard/stage_test.go
```

Required behavior:

- stage modified allowlisted files,
- stage new allowlisted files,
- do not stage unallowlisted changed files,
- never use broad staging commands such as `git add .` or `git add -u`,
- only use explicit path staging:

```bash
git add -- <path>
```
