# BLK-pipe Sprint 003 — Task 2 Outcome

**Status:** Complete
**Date:** 2026-05-04
**Task:** Add Opaque Trace Artifact Hash Baton Fields
**Commit:** `52bdb2e feat: carry blk-pipe trace artifact hashes`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Add a bounded, opaque trace-artifact contract so BLK-pipe can carry BLK-001 canonical hash baton metadata from CEB/L2 input through execution reports without interpreting architecture semantics.

This implements the BLK-001 context appropriately by treating `version_hash` values as transport metadata only:

- BLK-pipe does not parse requirement or use-case bodies.
- BLK-pipe does not verify trace hashes against files.
- BLK-pipe does not generate CEOs or RTMs.
- BLK-pipe does not invoke Codex, live LLM APIs, Discord HITL flows, or cyber execution.
- BLK-pipe remains the deterministic transport and repository blast shield in the BLK-001 separation-of-concerns model.

## 2. Files Added/Changed

Implementation commit `52bdb2e` changed:

```text
docs/BLK-010_blk-pipe-v47-hardening-cli.md
internal/contracts/payload.go
internal/contracts/payload_test.go
internal/contracts/report.go
internal/contracts/report_test.go
internal/pipe/run.go
internal/pipe/run_test.go
python/blk_pipe_adapter.py
python/test_blk_pipe_adapter.py
```

No production Git-staging, process-supervision, validation-authority, or sandbox behavior was broadened.

## 3. Behavior Implemented

### 3.1 Go payload contract

Added `contracts.TraceArtifact`:

```go
type TraceArtifact struct {
    Kind        string `json:"kind"`
    ID          string `json:"id"`
    VersionHash string `json:"version_hash"`
}
```

Added `TraceArtifacts []TraceArtifact` to both the normalized payload and wire payload structures so legacy/V47 payload decoding preserves `trace_artifacts` when supplied.

Validation is bounded and transport-focused:

- `trace_artifacts` may be empty.
- Maximum artifact count is `64`.
- `kind`, `id`, and `version_hash` must be non-empty.
- Each string is capped at `256` bytes.
- `version_hash` must start with `sha256:`.
- Oversized invalid values are not echoed in validation errors.

### 3.2 Go report contract

Added `TraceArtifacts []TraceArtifact` to `contracts.Report` as a stable JSON field:

- `NewReport()` initializes it to `[]TraceArtifact{}`.
- `Report.MarshalJSON()` normalizes nil values back to `[]`, not `null`.
- Valid trace artifacts are emitted unchanged as opaque metadata.

### 3.3 Pipe propagation

`internal/pipe/run.go` now copies safely validated `trace_artifacts` into reports during payload parsing.

Important safety behavior:

- Successful execution reports preserve trace artifacts.
- Invalid payload reports preserve trace artifacts when the artifacts themselves were safely decoded/validated and another payload field caused the failure.
- Invalid trace artifacts are not copied back into reports, preventing oversized invalid values from being echoed through report fields.

### 3.4 Python adapter integration surface

`python/blk_pipe_adapter.py` now:

- adds `trace_artifacts` to `ExecutionResult`,
- accepts optional `trace_artifacts` in `BlkPipeAdapter.execute_sprint(...)`,
- includes `trace_artifacts` in the JSON payload only when provided,
- maps parsed report `trace_artifacts` back onto `ExecutionResult`,
- defaults missing or null report `trace_artifacts` values to `[]`,
- preserves existing callers that omit `trace_artifacts`.

The adapter still invokes BLK-pipe with argv only and introduces no shell or live tactical-engine integration.

### 3.5 CLI contract documentation

`docs/BLK-010_blk-pipe-v47-hardening-cli.md` now documents Sprint 003 trace-artifact transport as a bounded, opaque BLK-001 `version_hash` baton field. The document explicitly states BLK-pipe does not parse requirement/use-case bodies, generate RTMs, verify hashes against files, or run Codex/LLMs.

## 4. TDD Evidence

### 4.1 RED

The implementation subagent timed out before returning its own RED transcript, so the controller reconstructed RED evidence in a detached temporary worktree from the pre-task baseline by applying only the new tests and running the focused suites. This demonstrated the tests failed for the expected missing-contract reasons before production code was present.

Command shape:

```text
git worktree add --detach /tmp/blk-pipe-003-task2-red HEAD
git apply /tmp/blk-pipe-003-task2-tests.patch
go test ./internal/contracts -run 'TestPayload.*Trace|TestReport.*Trace' -v
go test ./internal/pipe -run 'TestRun.*Trace' -v
python3 -m unittest discover -s python -p 'test_*.py'
```

Observed RED excerpts:

```text
contracts exit=1
internal/contracts/payload_test.go:103:16: undefined: TraceArtifact
internal/contracts/payload_test.go:113:34: payload.TraceArtifacts undefined
internal/contracts/payload_test.go:621:49: undefined: TraceArtifact
FAIL github.com/camcamcami/BLK-System/internal/contracts [build failed]
```

```text
pipe exit=1
internal/pipe/run_test.go:261:26: undefined: contracts.TraceArtifact
internal/pipe/run_test.go:292:36: report.TraceArtifacts undefined
FAIL github.com/camcamcami/BLK-System/internal/pipe [build failed]
```

```text
python exit=1
TypeError: BlkPipeAdapter.execute_sprint() got an unexpected keyword argument 'trace_artifacts'
AttributeError: 'ExecutionResult' object has no attribute 'trace_artifacts'
FAILED (errors=4)
```

### 4.2 GREEN

Focused trace tests passed after implementation:

```text
go test ./internal/contracts -run 'TestPayload.*Trace|TestReport.*Trace' -v
PASS
ok github.com/camcamcami/BLK-System/internal/contracts
```

```text
go test ./internal/pipe -run 'TestRun.*Trace' -v
=== RUN   TestRunSuccessReportsTraceArtifacts
--- PASS: TestRunSuccessReportsTraceArtifacts
=== RUN   TestRunInvalidPayloadReportsTraceArtifactsWhenDecodedBeforeValidationFailure
--- PASS: TestRunInvalidPayloadReportsTraceArtifactsWhenDecodedBeforeValidationFailure
=== RUN   TestRunInvalidTraceArtifactDoesNotEchoLongHash
--- PASS: TestRunInvalidTraceArtifactDoesNotEchoLongHash
PASS
ok github.com/camcamcami/BLK-System/internal/pipe
```

Python adapter tests passed:

```text
python3 -m unittest discover -s python -p 'test_*.py'
..............
Ran 14 tests
OK
```

Full Go suite and vet passed:

```text
go test ./...
ok github.com/camcamcami/BLK-System/cmd/blk-pipe
ok github.com/camcamcami/BLK-System/internal/contracts
ok github.com/camcamcami/BLK-System/internal/engine
ok github.com/camcamcami/BLK-System/internal/execguard
ok github.com/camcamcami/BLK-System/internal/gitguard
ok github.com/camcamcami/BLK-System/internal/pipe
ok github.com/camcamcami/BLK-System/internal/runtimeguard
ok github.com/camcamcami/BLK-System/internal/testutil
ok github.com/camcamcami/BLK-System/internal/validation

go vet ./... PASS
```

## 5. Review Results

Two fresh review gates were run before the implementation commit was pushed.

### 5.1 Spec compliance review

Result: `PASS`

Reviewer findings:

- `TraceArtifact` and `trace_artifacts` are added to payload/report contracts.
- Validation remains bounded and transport-focused.
- Reports emit stable `[]` and preserve valid trace artifacts.
- Invalid payload reports preserve trace context when safely decoded.
- Python adapter preserves the integration boundary and remains backward-compatible.
- BLK-010 documents the bounded opaque contract and the BLK-001 deterministic transport scope.

Focused verification rerun by reviewer:

```text
go test ./internal/contracts -run 'TestPayload.*Trace|TestReport.*Trace' -v PASS
go test ./internal/pipe -run 'TestRun.*Trace' -v PASS
python3 -m unittest discover -s python -p 'test_blk_pipe_adapter.py' -v PASS
```

### 5.2 Code-quality/security review

Result: `APPROVED`

Reviewer findings:

- Stable JSON shape is preserved.
- Oversized invalid trace values are not leaked in errors or report fields.
- No requirement/use-case parsing, hash verification, RTM/CEO generation, Codex/LLM integration, or broad Git staging was introduced.
- Python adapter remains backward-compatible and defaults missing/null report `trace_artifacts` to `[]`.
- Existing BLK-pipe safety invariants remain intact.

## 6. Final Verification

Final verification before pushing `52bdb2e`:

```text
gofmt -l internal/contracts/payload.go internal/contracts/payload_test.go internal/contracts/report.go internal/contracts/report_test.go internal/pipe/run.go internal/pipe/run_test.go
# no output

go test ./internal/contracts -run 'TestPayload.*Trace|TestReport.*Trace' -v PASS
go test ./internal/pipe -run 'TestRun.*Trace' -v PASS
python3 -m unittest discover -s python -p 'test_*.py' PASS
go test ./... PASS
go vet ./... PASS
```

Safety greps:

```text
! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go' PASS
! git grep -n -E 'exec\.Command(Context)?\("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**' PASS
! git grep -n -E 'git[^\n]*diff[^\n]*\.\.\.' -- '*.go' ':!*_test.go' docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/plans/BLK-PIPE-003_integration-readiness-and-capability-profiles.md docs/outcomes/BLK-PIPE-003_task-001-outcome.md PASS
```

Diff/status/push:

```text
git diff --check HEAD^ HEAD PASS
git status --short --branch
## main...origin/main [ahead 1]

git push origin main
9aee1bc..52bdb2e main -> main

git status --short --branch
## main...origin/main
```

## 7. Deviations / Notes

- The implementation subagent timed out before committing or returning its summary. The controller inspected the resulting diff, hardened report behavior so invalid oversized trace artifacts are not echoed through report fields, ran RED reconstruction in a detached worktree, ran all focused/full verification, then committed and pushed the implementation.
- The task intentionally does not validate trace hashes against the BLK-req vault. That is deferred to BLK-001 ledger/RTM components, preserving BLK-pipe's deterministic transport boundary.
- The Python test suite creates `python/__pycache__/`; it was removed before committing and pushing.

## 8. Next Task

Task 3 in `docs/plans/BLK-PIPE-003_integration-readiness-and-capability-profiles.md`: **Make Revert Branch-Safe**.
