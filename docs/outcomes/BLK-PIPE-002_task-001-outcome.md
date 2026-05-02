# BLK-pipe Sprint 002 — Task 1 Outcome

**Status:** Complete
**Date:** 2026-05-03
**Task:** Reconcile Exit-Code Registry
**Commit:** `f30ead8 feat: reconcile blk-pipe v47 exit codes`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Task 1 reconciled the Sprint 001 `ENGINE_FAILED` / code `4` conflict with BLK-004/V47 before any revert route is implemented.

The required safety property is now explicit:

- code `4` is reserved for `INVALID_REVERT_ANCHOR`,
- non-zero engine process exits no longer consume code `4`,
- non-zero engine process exits route to a fatal status/code path,
- Sprint 001 local extension codes remain explicit and separate from strict V47 router codes.

No revert behavior, validation gate, branch handling, Python adapter, Codex integration, or live tactical LLM invocation was added in this task.

---

## 2. Files Added/Changed

Changed:

- `internal/pipe/exitcodes.go`
- `internal/pipe/exitcodes_test.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- `docs/BLK-009_blk-pipe-sprint-001-cli.md`

No new production package was added.

---

## 3. Behavior Implemented

### 3.1 Exit-code constants

`internal/pipe/exitcodes.go` now defines:

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

### 3.2 Engine failure routing

Non-zero engine exits now produce:

```text
status: FATAL_ENGINE_FAILED
exit:   1
```

instead of the Sprint 001 behavior:

```text
status: ENGINE_FAILED
exit:   4
```

The engine's own process exit code is still preserved in the report's `engine_exit_code` field.

### 3.3 Code `4` reservation

Code `4` is now represented by:

```go
ExitInvalidRevertAnchor = 4
```

The revert route itself is still not implemented. This task only reserves the code so later revert work can be added without colliding with engine-failure behavior.

### 3.4 Preserved Sprint 001 behavior

The task intentionally preserved existing behavior for:

- invalid payloads,
- unauthorized mutations,
- output flood,
- engine timeout,
- dirty Git preflight,
- internal errors,
- allowlist staging,
- cleanup paths,
- `.git` mutation hardening,
- hook-disabled commits.

### 3.5 Documentation update

`docs/BLK-009_blk-pipe-sprint-001-cli.md` now records the compatibility transition:

- non-zero engine exits use `FATAL_ENGINE_FAILED` / code `1`,
- code `4` is reserved for `INVALID_REVERT_ANCHOR`,
- revert is not implemented as of Sprint 002 Task 1,
- most V47 hardening work remains future Sprint 002 work.

---

## 4. TDD Evidence

### 4.1 RED

The implementation subagent wrote tests first, then ran:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestExitCodes|TestRunEngineFailure' -v
```

Expected RED occurred because the new constants did not exist yet:

```text
internal/pipe/exitcodes_test.go:8:31: undefined: ExitFatalSystemPanic
internal/pipe/exitcodes_test.go:10:31: undefined: ExitValidationFailed
internal/pipe/exitcodes_test.go:12:31: undefined: ExitInvalidRevertAnchor
FAIL github.com/camcamcami/BLK-System/internal/pipe [build failed]
```

This proved the new tests were exercising missing Task 1 behavior before implementation.

### 4.2 GREEN

After implementation, focused tests passed:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestExitCodes|TestRunEngineFailure' -v
```

Observed:

```text
=== RUN   TestExitCodes
--- PASS: TestExitCodes (0.00s)
=== RUN   TestExitCodesEngineFailuresDoNotUseInvalidRevertAnchor
--- PASS: TestExitCodesEngineFailuresDoNotUseInvalidRevertAnchor (0.00s)
=== RUN   TestRunEngineFailureRoutesToFatalSystemPanic
--- PASS: TestRunEngineFailureRoutesToFatalSystemPanic (0.03s)
PASS
ok github.com/camcamcami/BLK-System/internal/pipe
```

The full `internal/pipe` suite also passed, including existing safety tests for:

- successful allowlisted mutation,
- hook-disabled commits,
- unauthorized mutation cleanup,
- nested Git repository cleanup,
- `.git/info/exclude` mutation hardening,
- `.git` root deletion recovery,
- Git hook mutation denial,
- dirty repo preflight,
- ignored-file preflight,
- protected BLK-req path denial.

---

## 5. Review Results

### 5.1 Spec Compliance Review

Result: **PASS**

The spec reviewer verified:

- `ExitInvalidRevertAnchor == 4`,
- `ExitFatalSystemPanic == 1`,
- `ExitOutputFlood == 5`,
- `ExitUnauthorizedMutation == 3`,
- retained local extensions `6`, `7`, and `9`,
- non-zero engine exits now return code `1` with `FATAL_ENGINE_FAILED`,
- code `4` is no longer used for engine failures,
- docs reflect code `4` reservation,
- no revert or live LLM/Codex integration was added.

Spec-review verification included:

```bash
go test ./internal/pipe -run 'TestExitCodes|TestRunEngineFailure' -v
go test ./...
git diff --check HEAD^..HEAD
```

All passed.

### 5.2 Code Quality / Safety Review

Result: **APPROVED**

The code-quality reviewer found no critical or important issues.

Reviewer checks included:

- non-zero engine exits route to code `1` and status `FATAL_ENGINE_FAILED`,
- timeout/flood/unauthorized/git-dirty behavior was not altered,
- cleanup ordering remained intact,
- allowlist staging and `.git` safety paths were not broadened,
- no broad staging was introduced,
- no Codex/live LLM integration was added,
- no revert behavior was accidentally implemented.

A minor documentation wording nit was addressed before the final amend: the docs now say revert is not implemented “as of Sprint 002 Task 1” rather than “in Sprint 001.”

---

## 6. Final Verification

Controller verification before pushing the implementation commit:

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -l internal/pipe/exitcodes.go internal/pipe/exitcodes_test.go internal/pipe/run.go internal/pipe/run_test.go
go test ./internal/pipe -run 'TestExitCodes|TestRunEngineFailure' -v
go test ./internal/pipe -v
go test ./...
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
git diff --check HEAD^ HEAD
git status --short --branch
git push origin main
git status --short --branch
```

Observed summary:

```text
TestExitCodes PASS
TestExitCodesEngineFailuresDoNotUseInvalidRevertAnchor PASS
TestRunEngineFailureRoutesToFatalSystemPanic PASS
ok github.com/camcamcami/BLK-System/internal/pipe
ok github.com/camcamcami/BLK-System/cmd/blk-pipe
ok github.com/camcamcami/BLK-System/internal/contracts
ok github.com/camcamcami/BLK-System/internal/engine
ok github.com/camcamcami/BLK-System/internal/gitguard
ok github.com/camcamcami/BLK-System/internal/testutil
```

The production broad-staging grep printed no matches. `git diff --check HEAD^ HEAD` passed. The implementation commit was pushed to `origin/main`.

Final implementation state:

```text
f30ead8 (HEAD -> main, origin/main) feat: reconcile blk-pipe v47 exit codes
3ee6ded docs: plan blk-pipe sprint 002
```

---

## 7. Deviations / Notes

- The implementation commit was first created as `ae60945`, then amended to `f30ead8` after addressing a minor documentation wording improvement from code-quality review.
- `docs/BLK-009_blk-pipe-sprint-001-cli.md` was updated because it contained stale user-facing `4 ENGINE_FAILED` documentation.
- Revert remains unimplemented until a later Sprint 002 task.
- Strict V47 report schema, validation commands, branch/orphan handling, bounded Git helper, signal handling, and Python adapter remain future Sprint 002 tasks.
- Codex/live tactical engine integration remains deferred.

---

## 8. Next Task

Next planned work:

```text
BLK-pipe Sprint 002 — Task 2: Add V47 Payload and Stable Report Contracts With Legacy Normalization
```

Task 2 should preserve Sprint 001 payload compatibility while adding V47-compatible payload decoding and stable report JSON fields.
