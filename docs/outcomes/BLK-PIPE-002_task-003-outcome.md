# BLK-PIPE-002 Task 003 Outcome — Reusable Bounded Command Guard

Status: COMPLETE
Date: 2026-05-03
Sprint plan: `docs/plans/BLK-PIPE-002_v47-hardening-layer.md`
Task: Sprint 002 Task 3 — reusable bounded command guard
Implementation commit: `871f3a9 feat: add bounded command guard`

## Summary

Task 003 implemented the reusable POSIX bounded command guard required before Sprint 002 can safely reuse command execution semantics for engine runs, later validation commands, and later Git command handling.

The work added `internal/execguard` and refactored the existing engine runner to consume it. `pipe.Run` now carries bounded engine output into V47 reports through `EngineLogs`, including success, engine failure, and output-flood paths.

The implementation was pushed to `origin/main` as:

```text
871f3a9 feat: add bounded command guard
```

## Files Changed

```text
docs/BLK-003_blk-pipe-blk-test-orchestration.md
internal/engine/runner.go
internal/engine/runner_test.go
internal/execguard/command.go
internal/execguard/command_test.go
internal/pipe/run.go
internal/pipe/run_test.go
```

## Implemented Behavior

### `internal/execguard`

Added a reusable bounded command execution package with:

- `Options`
  - `Workdir string`
  - `Command []string`
  - `Timeout time.Duration`
  - `MaxOutputBytes int64`
  - `Env []string`
- `CommandResult`
  - `ExitCode int`
  - `Output []byte`
  - `OutputBytes int64`
  - `TimedOut bool`
  - `Flooded bool`
- `Run(ctx context.Context, opts Options) (CommandResult, error)`
- `ScrubbedEnv(workdir string, extra ...string) []string`

The guard provides:

- POSIX process-group isolation and process-group kill behavior.
- Bounded retained combined stdout/stderr output.
- Total output byte counting separate from retained output length.
- Output flood detection and kill behavior.
- Timeout/context cancellation detection and kill behavior.
- Non-zero child exit handling without treating normal command failure as infrastructure failure.
- Infrastructure error return for command start failures.
- Environment scrubbing for inherited Git and SSH-agent risk.

### Environment Scrub

`ScrubbedEnv` removes inherited unsafe or nondeterministic entries, including:

```text
GIT_*
PWD
SSH_AUTH_SOCK
SSH_AGENT_PID
SSH_ASKPASS
```

It then appends deterministic execution defaults:

```text
GIT_CONFIG_GLOBAL=/dev/null
GIT_CONFIG_NOSYSTEM=1
PWD=<workdir>
```

Extra caller-provided env entries are preserved and appended after the scrubbed base environment.

### Engine Integration

`internal/engine.Run` now delegates bounded command execution to `internal/execguard`, preserving existing caller-facing engine behavior while using the reusable guard for:

- success output capture,
- non-zero exit reporting,
- timeouts,
- output flood handling,
- command start failures,
- inherited pipe writer handling.

### Pipe Report Integration

`internal/pipe.Run` now populates `report.EngineLogs` from bounded engine output on relevant report paths.

Covered report paths include:

- successful engine run,
- engine failure,
- output flood failure.

The flood path remains bounded and returns the expected fatal output flood status/exit behavior.

## Review Findings and Fixes

### Initial escaped-child hang finding

The first code-quality review found that a descendant process could escape the original process group while keeping stdout/stderr open. The original implementation could wait indefinitely for output reader completion after the direct child exited.

Fix:

- Added regression coverage for escaped descendants that keep inherited stdout/stderr open.
- Added bounded output-drain handling for timeout/cancel/flood paths.
- Ensured `Run` does not hang indefinitely when an escaped descendant holds inherited output pipes open.

### Post-return worktree race finding

A follow-up code-quality review found a subtler safety issue: bounding the output drain prevented a hang, but it also allowed `Run` to return while an escaped descendant was still alive and still holding inherited stdout/stderr. That could let a hostile descendant mutate the worktree after `pipe.Run` started cleanup/staging/commit work.

Fix:

- Added strict-TDD regression test:
  - `TestRunWaitsForEscapedDescendantToCloseInheritedOutputPipeBeforeReturning`
- Observed the test fail before the implementation change.
- Changed normal/direct-child-exit semantics so `Run` waits for inherited stdout/stderr pipes to close before returning.
- Kept timeout, context cancellation, and output-flood paths bounded so hostile or stuck descendants cannot hang the guard forever when a bound is active.
- Added a test-level watchdog so the regression fails promptly instead of waiting for the package/global test timeout.

Accepted portable-POSIX limitation:

- Descendants that both escape the process group and close/redirect inherited output file descriptors remain outside this guard’s portable POSIX containment scope.
- This limitation is documented in the relevant BLK-pipe orchestration doctrine rather than hidden in implementation assumptions.

## Out of Scope / Not Implemented

Per Sprint 002 Task 3 boundaries, this task did not add:

- validation command execution,
- branch/fetch/orphan handling,
- revert behavior,
- Python adapter behavior,
- Codex/live LLM integration,
- Windows fallback implementation.

The process-control implementation remains POSIX-only under the Sprint 002 constraint.

## Review Evidence

### Spec compliance review

Spec re-review on amended commit `00cfbde` passed before the final test-watchdog amendment.

Key findings:

- `execguard` API and behavior matched Task 3 requirements.
- POSIX-only process-control files used the intended `linux || darwin` build constraint.
- Timeout, flood, retained output, non-zero exit, and process-group kill behavior were covered.
- Environment scrub behavior matched the required Git/SSH-agent hardening.
- Engine integration and `pipe.Run` report integration were aligned.
- No validation execution, branch/fetch/orphan handling, revert behavior, Python adapter, or live LLM/Codex integration was introduced.

### Code-quality/safety review

Final code-quality/safety re-review passed with no blocking findings.

Key findings:

- The amended wait semantics fix the previously identified post-return worktree race for escaped descendants that keep inherited stdout/stderr open.
- Timeout, cancellation, and output flood paths remain bounded.
- Same-process-group background children are killed after the direct process exits.
- Output retention remains bounded by `MaxOutputBytes`.
- Channel/goroutine lifecycle had no obvious close/send races.
- Env scrub behavior correctly removes inherited Git and SSH-agent risk.

Minor review note addressed before final push:

- Added a test-level watchdog around `TestRunWaitsForEscapedDescendantToCloseInheritedOutputPipeBeforeReturning` so a regression fails promptly.

## Final Verification

Final controller verification before push used:

```bash
export PATH="$HOME/.local/bin:$PATH"
git status --short --branch
git show --stat --oneline HEAD
gofmt -l internal/execguard/command.go internal/execguard/command_test.go internal/engine/runner.go internal/engine/runner_test.go internal/pipe/run.go internal/pipe/run_test.go
go test ./internal/execguard -v
go test ./internal/engine -v
go test ./internal/pipe -run 'TestRun.*EngineLogs|TestRun.*OutputFlood' -v
go test ./...
go vet ./...
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
git diff --check
git push origin main
git status --short --branch
git log --oneline --decorate -3
```

Results:

```text
ok  github.com/camcamcami/BLK-System/internal/execguard  0.867s
ok  github.com/camcamcami/BLK-System/internal/engine     0.060s
ok  github.com/camcamcami/BLK-System/internal/pipe       0.078s
ok  github.com/camcamcami/BLK-System/cmd/blk-pipe        (cached)
ok  github.com/camcamcami/BLK-System/internal/contracts  (cached)
ok  github.com/camcamcami/BLK-System/internal/engine     0.069s
ok  github.com/camcamcami/BLK-System/internal/execguard  0.870s
ok  github.com/camcamcami/BLK-System/internal/gitguard   (cached)
ok  github.com/camcamcami/BLK-System/internal/pipe       0.394s
ok  github.com/camcamcami/BLK-System/internal/testutil   (cached)
```

`go vet ./...`, broad staging grep, and `git diff --check` passed with no output.

Push result:

```text
To https://github.com/camcamcami/BLK-System.git
   4c71f8d..871f3a9  main -> main
```

Final implementation state:

```text
871f3a9 (HEAD -> main, origin/main) feat: add bounded command guard
4c71f8d docs: record BLK-pipe sprint 002 task 2 outcome
b123772 feat: add blk-pipe v47 contracts
```

## Result

BLK-pipe Sprint 002 Task 003 is complete and pushed.

The repository now has a reusable POSIX bounded command guard for engine execution and later command execution surfaces, with bounded output retention, timeout/flood handling, environment scrubbing, process-group kill behavior, and explicit handling/documentation for escaped descendant limitations.
