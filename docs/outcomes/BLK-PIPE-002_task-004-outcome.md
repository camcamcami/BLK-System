# BLK-PIPE-002 Task 004 Outcome — Main-Level Signal Trap, Panic Recovery, and Active Reaping

Status: COMPLETE
Date: 2026-05-03
Sprint plan: `docs/plans/BLK-PIPE-002_v47-hardening-layer.md`
Task: Sprint 002 Task 4 — main-level signal trap, panic recovery, and active process reaping
Implementation commit: `4a2ce0f feat: add blk-pipe fatal signal guard`
Remote: pushed to `origin/main`

## Summary

Task 004 implemented the BLK-004 fatal-system guard around the `blk-pipe` CLI entrypoint.

The implementation adds a POSIX main-level runtime guard that traps `SIGINT` and `SIGTERM`, recovers panics into a sterile JSON fatal report, reaps active command process groups and discoverable descendants, prevents duplicate normal/fatal report emission, and exits with code `1` for fatal-system paths.

The implementation was pushed to `origin/main` as:

```text
4a2ce0f feat: add blk-pipe fatal signal guard
```

## Files Changed

```text
cmd/blk-pipe/main.go
cmd/blk-pipe/main_test.go
internal/execguard/command.go
internal/execguard/command_test.go
internal/runtimeguard/signal.go
internal/runtimeguard/signal_test.go
```

Commit stat:

```text
cmd/blk-pipe/main.go                 |  38 ++-
cmd/blk-pipe/main_test.go            | 104 +++++++++
internal/execguard/command.go        | 347 ++++++++++++++++++++++++++-
internal/execguard/command_test.go   | 438 +++++++++++++++++++++++++++++++++++
internal/runtimeguard/signal.go      | 267 +++++++++++++++++++++
internal/runtimeguard/signal_test.go | 198 ++++++++++++++++
6 files changed, 1388 insertions(+), 4 deletions(-)
```

## Implemented Behavior

### Main-level runtime guard

`cmd/blk-pipe/main.go` now routes normal CLI execution through `runtimeguard.Run` via a testable guarded-main seam.

The guard preserves existing CLI behavior for:

- `--health`,
- `--payload-stdin`,
- `--payload /absolute/path/to/payload.json`,
- unsupported or invalid invocations.

The POSIX CLI entrypoint wires fatal cleanup to:

```text
execguard.KillActiveProcessGroups()
```

### Signal handling

`internal/runtimeguard` traps POSIX fatal signals:

```text
SIGINT
SIGTERM
```

On signal, the guard:

1. begins the fatal report gate,
2. cancels the runner context,
3. invokes active process reaping,
4. waits boundedly for the runner to settle,
5. emits a single sterile fatal JSON report,
6. exits with code `1`.

The signal goroutine does not call `os.Exit` before cleanup completes. This was a deliberate review-driven hardening point because exiting directly from the signal goroutine could skip child cleanup and leave orphaned command descendants.

### Panic recovery

Panics inside guarded CLI execution are recovered into a sterile fatal JSON report.

The report uses fatal-system status and exit code `1`, while intentionally not leaking:

- panic values,
- stack traces,
- filesystem paths,
- secrets or token-like values.

### Report gate

`runtimeguard.ReportGate` serializes normal and fatal report writes so fatal-system paths cannot produce duplicate or interleaved JSON reports.

Covered behavior includes:

- fatal signal suppresses a concurrently queued normal report,
- late signal handling is checked before normal flush completes,
- fatal panic emits exactly one report,
- fatal signal emits exactly one report.

### Active process registry and reaping

`internal/execguard` now maintains an active command registry so the main-level guard can reap currently running command trees.

Key properties:

- active registry entries are keyed by unique monotonic IDs, not by PID;
- the registry remains active through output-drain time;
- direct command liveness is tracked separately with `directLive`;
- after `cmd.Wait()` reaps the direct command, stale root PID/PGID targeting is disabled;
- inherited-output pipe holders can still be discovered and reaped while output drain is in progress;
- visible descendants and process groups of live active command roots are targeted;
- visible descendants and process groups of external inherited-output pipe holders are targeted;
- the current `blk-pipe` process PID is skipped and not traversed as a pipe holder.

This preserves Task 3 command-guard behavior while adding the main-level fatal cleanup required by Task 4.

## TDD Evidence

### Initial RED evidence

The first strict-TDD implementation added tests before production code. RED failures included missing runtime guard and active reaper symbols:

```text
# github.com/camcamcami/BLK-System/internal/runtimeguard
internal/runtimeguard/signal_test.go:24:10: undefined: Run
internal/runtimeguard/signal_test.go:24:36: undefined: Options
internal/runtimeguard/signal_test.go:66:11: undefined: Run
internal/runtimeguard/signal_test.go:66:37: undefined: Options
github.com/camcamcami/BLK-System/internal/runtimeguard: no non-test Go files

# github.com/camcamcami/BLK-System/internal/execguard
internal/execguard/command_test.go:306:17: undefined: KillActiveProcessGroups
```

### Review-fix RED evidence

Later review cycles added regression tests before each safety fix.

Third-round active-registry RED evidence:

```text
TestActiveRegistryAllowsRepeatedRootPIDUntilEachRunUnregisters
captured first=false second=true ... want both runs registered independently
```

Fourth-round pipe-holder descendant RED evidence:

```text
=== RUN   TestActiveCleanupTargetsIncludePipeHolderDescendantsAfterDirectReaped
    command_test.go:487: cleanup targets omitted pipe-holder descendant PID 666 in map[int]struct {}{444:struct{}{}}
--- FAIL: TestActiveCleanupTargetsIncludePipeHolderDescendantsAfterDirectReaped (0.00s)
FAIL
FAIL github.com/camcamcami/BLK-System/internal/execguard 0.003s
```

Fifth-round own-PID pipe-holder RED evidence:

```text
go test ./internal/execguard -run TestActiveCleanupTargetsDoNotTraverseOwnPipeHolderDescendantsAfterDirectReaped -count=1 -v
cleanup targets included excluded PID 565
```

### GREEN evidence

The final implementation passes the focused fatal guard, active cleanup, race, full test, vet, broad-staging grep, and diff-check verification listed below.

## Review Results

Task 004 went through repeated two-stage review: spec compliance first, then code-quality/safety review. No implementation was pushed until both final reviews passed.

### Initial review rounds

Initial and intermediate reviews found issues in signal cleanup ordering, report gating, active registry lifetime, and PID/PGID safety. These were fixed in amended local commits before the final implementation push.

Confirmed fixed behaviors include:

- signal path cancels, reaps, waits, then emits fatal report;
- no direct `os.Exit` from the signal goroutine before cleanup;
- normal/fatal report output is gated;
- signal notification is stopped before normal flush with a final queued-signal check;
- active registry remains present through output drain;
- active registry uses unique IDs rather than process IDs;
- direct process state is marked reaped after `cmd.Wait()`;
- stale root PID/PGID targeting is disabled after direct process reap.

### Fourth-round spec review finding

A spec reviewer reproduced a critical containment gap:

```text
root command launches setsid pipe-holder A,
A launches setsid child B,
root exits 0,
A keeps blk-pipe stdout/stderr pipe open,
B redirects stdio to /dev/null and sleeps,
SIGTERM is sent while execguard.Run is blocked draining A's pipe.
```

Observed before fix:

```text
blk-pipe exits 1 and writes one FATAL_SYSTEM_PANIC JSON report;
A is killed;
B and B's sleep child remain alive.
```

Fix:

- `activeCleanupTargets` now traverses visible descendants of external inherited-output pipe-holder PIDs.
- Target PGIDs for those descendants are included when discoverable.
- Stale direct root PID/PGID targeting remains disabled after `directLive=false`.

Final spec re-review passed and included a black-box repro confirming the holder, child, and grandchild were non-live after fatal SIGTERM.

### Fifth-round quality review finding

A quality reviewer found a safety overreach risk: Linux pipe inode discovery can include the current `blk-pipe` process because reader and writer ends show the same `pipe:[inode]`. The previous fourth-round fix skipped adding `ownPID`, but still traversed descendants of `ownPID` when `ownPID` appeared in the pipe-holder set.

Fix:

- the pipe-holder cleanup loop now skips `pid == ownPID` before adding or traversing descendants;
- regression coverage proves arbitrary `blk-pipe` own children/grandchildren are not included;
- external pipe-holder descendants remain included;
- stale root PID/PGID behavior remains excluded after direct reap.

### Final review verdicts

Final post-fifth-fix spec review verdict:

```text
PASS
```

Final post-fifth-fix code-quality/safety review verdict:

```text
APPROVED
```

Final reviewers verified:

- main-level guard installation;
- POSIX build tags on OS-dependent files;
- sterile panic recovery;
- signal trap behavior;
- exactly-one fatal JSON report behavior;
- active process registry and active cleanup behavior;
- external pipe-holder descendant cleanup;
- own-PID pipe-holder traversal suppression;
- full test/race/vet/diff-check success;
- no Codex/live LLM integration.

## Final Controller Verification

Final controller verification before the implementation push used:

```bash
export PATH="$HOME/.local/bin:$PATH"
git config user.name "camcamcami"
git config user.email "cam.elvey@gmail.com"
git status --short --branch
git log --oneline --decorate -5
gofmt -l cmd/blk-pipe/main.go cmd/blk-pipe/main_test.go internal/execguard/command.go internal/execguard/command_test.go internal/runtimeguard/signal.go internal/runtimeguard/signal_test.go
go test ./cmd/blk-pipe -v
go test ./internal/runtimeguard -v
go test ./internal/execguard -v
go test ./internal/engine -v
go test ./internal/pipe -v
go test -race ./internal/runtimeguard ./internal/execguard ./cmd/blk-pipe
go test ./...
go vet ./...
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
git diff --check
git push origin main
git status --short --branch
git log --oneline --decorate -5
```

Focused test results included:

```text
ok github.com/camcamcami/BLK-System/cmd/blk-pipe        (cached)
ok github.com/camcamcami/BLK-System/internal/runtimeguard (cached)
ok github.com/camcamcami/BLK-System/internal/execguard  (cached)
ok github.com/camcamcami/BLK-System/internal/engine     0.060s
ok github.com/camcamcami/BLK-System/internal/pipe       0.422s
```

Race and full-suite results included:

```text
ok github.com/camcamcami/BLK-System/internal/runtimeguard (cached)
ok github.com/camcamcami/BLK-System/internal/execguard  2.982s
ok github.com/camcamcami/BLK-System/cmd/blk-pipe        (cached)
ok github.com/camcamcami/BLK-System/cmd/blk-pipe        (cached)
ok github.com/camcamcami/BLK-System/internal/contracts  (cached)
ok github.com/camcamcami/BLK-System/internal/engine     0.067s
ok github.com/camcamcami/BLK-System/internal/execguard  0.952s
ok github.com/camcamcami/BLK-System/internal/gitguard   (cached)
ok github.com/camcamcami/BLK-System/internal/pipe       0.403s
ok github.com/camcamcami/BLK-System/internal/runtimeguard (cached)
ok github.com/camcamcami/BLK-System/internal/testutil   (cached)
```

`gofmt -l`, `go vet ./...`, the broad staging grep, and `git diff --check` passed with no output.

Implementation push result:

```text
To https://github.com/camcamcami/BLK-System.git
   032a58c..4a2ce0f  main -> main
```

Final implementation state:

```text
4a2ce0f (HEAD -> main, origin/main) feat: add blk-pipe fatal signal guard
032a58c docs: record BLK-pipe sprint 002 task 3 outcome
871f3a9 feat: add bounded command guard
```

## Out of Scope / Not Implemented

Per Sprint 002 Task 4 boundaries, this task did not add:

- validation command execution,
- validation report semantics,
- branch/fetch/orphan handling,
- revert behavior,
- Python adapter behavior,
- Codex/live LLM integration,
- Windows fallback implementation.

The runtime guard and process cleanup remain POSIX-scoped under the Sprint 002 task constraint.

## Notes and Limitations

Linux has the strongest containment behavior because the implementation can inspect `/proc` for inherited-output pipe holders. Darwin build tags are present, but Darwin lacks the same Linux `/proc` pipe-holder discovery path; this remains a reduced-containment portability note rather than a hidden guarantee.

The implemented guard is not a full OS sandbox. It hardens the deterministic execution kernel's fatal cleanup path using process groups, visible process-tree traversal, active registry state, and inherited-output pipe-holder discovery. Descendants outside those observable/containable surfaces still require future stronger sandboxing or supervision if the doctrine later demands full host-level containment.

## Result

BLK-pipe Sprint 002 Task 004 is complete and pushed.

The repository now has main-level fatal signal and panic handling with sterile fatal JSON reports, exit code `1`, exactly-one-report gating, and active command reaping that covers live command groups plus discoverable inherited-output pipe-holder descendants without reintroducing stale root PID/PGID or own-process descendant overreach.
