# BLK-pipe Sprint 004 — Task 2 Outcome

**Status:** Complete
**Date:** 2026-05-04
**Task:** Enforce Payload Byte Cap at Direct Decode/Run Boundary
**Commit:** `5b23649 fix: enforce blk-pipe payload cap for direct callers`
**Remote:** pushed to `origin/main` after final verification

---

## 1. Objective

Task 2 resolved the Phase 3 payload-size review note by enforcing the existing 2 MiB BLK-pipe payload JSON cap at direct in-process boundaries, not only at CLI file/stdin ingress.

The completed behavior is:

- `contracts.DecodePayload(data)` rejects `len(data) > contracts.DefaultMaxPayloadJSONBytes` before JSON unmarshal.
- `pipe.Run(ctx, payloadJSON, writer)` returns `ExitInvalidPayload` and emits report status `INVALID_PAYLOAD` for oversized direct payload bytes.
- Oversized payload errors do not echo the payload body.
- Existing CLI bounded-read behavior remains intact.

## 2. Files Added/Changed

Changed in implementation commit `5b23649`:

- `internal/contracts/payload.go`
  - Added `ValidatePayloadJSONSize(data []byte) error`.
  - Called the helper at the start of `DecodePayload` before JSON unmarshal.
- `internal/contracts/payload_test.go`
  - Added direct decode oversized-payload regression coverage.
- `internal/pipe/run_test.go`
  - Added direct `pipe.Run` oversized-payload regression coverage and non-leak assertion.
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
  - Documented that direct `contracts.DecodePayload` and `pipe.Run` callers are bounded.
- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md`
  - Updated the payload/validation bounds readiness bullet to include direct decode/run boundaries.

This outcome document is created separately at:

- `docs/outcomes/BLK-PIPE-004_task-002-outcome.md`

## 3. Behavior Implemented

`DecodePayload` now fails closed before attempting to unmarshal an oversized byte slice:

```go
func ValidatePayloadJSONSize(data []byte) error {
    if len(data) > DefaultMaxPayloadJSONBytes {
        return fmt.Errorf("payload JSON exceeds maximum size of %d bytes", DefaultMaxPayloadJSONBytes)
    }
    return nil
}
```

Because `pipe.Run` already routes through `parseAndValidatePayload` -> `contracts.DecodePayload`, direct `pipe.Run` callers now receive the standard invalid-payload path for oversized payload JSON:

- exit code: `2` / `ExitInvalidPayload`
- report status: `INVALID_PAYLOAD`
- stable empty report fields retained
- no payload body echo in report error/output

## 4. TDD Evidence

### 4.1 RED

Added failing tests first:

```text
TestDecodePayloadRejectsOversizedPayloadBytes
TestRunRejectsOversizedPayloadBytesBeforeDecode
```

RED command evidence:

```text
$ go test ./internal/contracts -run 'TestDecodePayloadRejectsOversized' -v
=== RUN   TestDecodePayloadRejectsOversizedPayloadBytes
    payload_test.go:96: DecodePayload() error = "invalid character '{' looking for beginning of object key string", want payload byte cap
--- FAIL: TestDecodePayloadRejectsOversizedPayloadBytes (0.00s)
FAIL

$ go test ./internal/pipe -run 'TestRunRejectsOversized|TestRun.*InvalidPayload' -v
=== RUN   TestRunRejectsOversizedPayloadBytesBeforeDecode
    run_test.go:319: report error = "invalid character '{' looking for beginning of object key string", want payload byte cap
--- FAIL: TestRunRejectsOversizedPayloadBytesBeforeDecode (0.00s)
FAIL
```

The failures showed direct oversized input still reached JSON unmarshal instead of the payload byte-cap guard.

### 4.2 GREEN

After implementing `ValidatePayloadJSONSize` and calling it before unmarshal:

```text
$ go test ./internal/contracts -run 'TestDecodePayloadRejectsOversized' -v
=== RUN   TestDecodePayloadRejectsOversizedPayloadBytes
--- PASS: TestDecodePayloadRejectsOversizedPayloadBytes (0.00s)
PASS
ok  	github.com/camcamcami/BLK-System/internal/contracts	0.003s

$ go test ./internal/pipe -run 'TestRunRejectsOversized|TestRun.*InvalidPayload' -v
=== RUN   TestRunRejectsOversizedPayloadBytesBeforeDecode
--- PASS: TestRunRejectsOversizedPayloadBytesBeforeDecode (0.00s)
=== RUN   TestRunInvalidPayloadReportsTraceArtifactsWhenDecodedBeforeValidationFailure
--- PASS: TestRunInvalidPayloadReportsTraceArtifactsWhenDecodedBeforeValidationFailure (0.00s)
=== RUN   TestRunReportInvalidPayloadIncludesExitCodeAndStableV47Fields
--- PASS: TestRunReportInvalidPayloadIncludesExitCodeAndStableV47Fields (0.00s)
=== RUN   TestRunInvalidPayloadWorkdirConflictPreservesReportMetadata
--- PASS: TestRunInvalidPayloadWorkdirConflictPreservesReportMetadata (0.00s)
=== RUN   TestRunInvalidPayloadEngineConflictPreservesReportMetadata
--- PASS: TestRunInvalidPayloadEngineConflictPreservesReportMetadata (0.00s)
PASS
ok  	github.com/camcamcami/BLK-System/internal/pipe	0.005s

$ go test ./cmd/blk-pipe -run 'TestPayload.*Oversized' -v
=== RUN   TestPayloadStdinRejectsOversizedPayload
--- PASS: TestPayloadStdinRejectsOversizedPayload (0.00s)
=== RUN   TestPayloadFileRejectsOversizedPayloadBeforePipeRun
--- PASS: TestPayloadFileRejectsOversizedPayloadBeforePipeRun (0.00s)
PASS
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	0.009s
```

## 5. Review Results

No live Codex, live tactical LLM, network model service, cyber tooling, Hindsight, or live BLK-test MCP was used.

### 5.1 Deterministic spec / traceability gate

Result: `PASS`

The deterministic gate verified:

- `ValidatePayloadJSONSize` exists in `internal/contracts/payload.go`.
- `DecodePayload` calls `ValidatePayloadJSONSize(data)` before `json.Unmarshal(data, &wire)`.
- Contract and pipe tests exist for oversized direct payload bytes.
- BLK-010 documents direct `contracts.DecodePayload(data)` and `pipe.Run(ctx, payloadJSON, writer)` enforcement.
- BLK-012 documents the direct boundary as part of payload/validation bounds.

Gate output:

```text
SPEC_TRACEABILITY_GATE PASS
```

### 5.2 Deterministic safety / docs-quality gate

Result: `PASS`

The deterministic gate verified:

- Changed files end with final newlines.
- Markdown fences remain balanced.
- Changed lines have no trailing whitespace.
- Added lines do not introduce live model/network execution tokens, real Codex invocation tokens, or active-vault access tokens.
- Oversized-payload tests assert secret/body non-leakage.

Gate output:

```text
SAFETY_DOCS_QUALITY_GATE PASS
ADDED_LINES_STATIC_SAFETY_GATE PASS
```

## 6. Final Verification

Final implementation verification before committing:

```text
$ go test ./internal/contracts -run 'TestDecodePayloadRejectsOversized' -v
PASS

$ go test ./internal/pipe -run 'TestRunRejectsOversized|TestRun.*InvalidPayload' -v
PASS

$ go test ./cmd/blk-pipe -run 'TestPayload.*Oversized' -v
PASS

$ go test ./...
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	0.052s
ok  	github.com/camcamcami/BLK-System/internal/contracts	0.072s
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	6.854s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	0.134s

$ python3 -m unittest discover -s python -p 'test_*.py'
Ran 17 tests in 0.379s
OK

$ go vet ./...
PASS

$ git diff --check
PASS
```

Additional deterministic safety greps:

```text
$ ! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go'
PASS

$ ! git grep -n -E 'exec\.Command(Context)?\("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
PASS

$ ! git grep -n -E 'git.*diff.*\.\.\.' -- '*.go' ':!*_test.go' docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md docs/plans/BLK-PIPE-004_dry-run-orchestrator-and-blk-test-fixtures.md
PASS
```

Implementation commit:

```text
5b23649 fix: enforce blk-pipe payload cap for direct callers
```

## 7. Deviations / Notes

- The implementation used deterministic local review gates instead of live reviewer agents because the task explicitly forbids live tactical LLMs and the Sprint 004 plan requires deterministic review gates for this sprint.
- No adapter behavior changed; Task 2 was limited to Go direct decode/run enforcement and documentation.
- No live Codex, live LLM, network model service, cyber tooling, Hindsight, or live BLK-test MCP was used.
- The outcome document is committed separately from the implementation commit, matching the BLK-System sprint execution workflow.

## 8. Next Task

Next planned sprint task:

```text
Task 3 — Freeze Adapter Status Fidelity as a Local V47-Compatible Extension
```
