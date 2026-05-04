# BLK-pipe Sprint 003 — Task 4 Outcome

**Status:** Complete
**Date:** 2026-05-04
**Task:** Bound Payload Ingestion and Validation Work
**Commit:** `e13d56f fix: bound blk-pipe payload and validation work`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Bound payload JSON ingestion and validation work so BLK-pipe remains a deterministic BLK-001 transport and repository blast shield. Task 4 closes unbounded input/work multiplication gaps without enabling live Codex, live LLM execution, cyber execution, tactical interpretation, or sandbox claims.

---

## 2. Files Added/Changed

Implementation commit changed:

- `cmd/blk-pipe/main.go`
- `cmd/blk-pipe/main_test.go`
- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/validation/validation.go`
- `internal/validation/validation_test.go`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md`

Outcome commit adds:

- `docs/outcomes/BLK-PIPE-003_task-004-outcome.md`

---

## 3. Behavior Implemented

### 3.1 Payload ingestion bounds

- Added `DefaultMaxPayloadJSONBytes = 2 * 1024 * 1024`.
- `blk-pipe --payload /absolute/path` now rejects regular payload files larger than 2 MiB via `os.Stat` before reading all bytes where possible.
- File payload mode still performs a bounded read after open, so file races or special-file surprises cannot force an unbounded read.
- `blk-pipe --payload-stdin` reads at most `DefaultMaxPayloadJSONBytes + 1` bytes and rejects oversized input.
- Oversized payloads return `ExitInvalidPayload` (`2`).
- Oversized-payload errors are short size errors and do not echo payload body bytes.

### 3.2 Payload validation work bounds

- Added `DefaultMaxValidationCommands = 16`.
- Added `DefaultMaxValidationCommandBytes = 4096`.
- Payload validation rejects more than 16 validation commands.
- Payload validation rejects any validation command string over 4096 bytes.
- Long validation command errors avoid echoing the full command body.

### 3.3 Overall validation runtime bound

- Validation execution now receives one overall deadline equal to `payload.TimeoutSeconds` after engine success.
- The whole validation phase is bounded by that deadline rather than multiplying timeout by command count.
- Timed-out or flooded validation commands stop later validation commands.
- A code-quality review found that an already-canceled validation context could otherwise return an empty successful validation result. The implementation commit was amended so already-canceled validation before the first command returns an error instead of success, and later overall deadline expiration is represented as validation failure rather than skipped success.

### 3.4 Documentation updates

- Updated `docs/BLK-010_blk-pipe-v47-hardening-cli.md` with the payload and validation bounds.
- Updated `docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md` to keep integration-readiness claims bounded: BLK-pipe remains a deterministic transport/blast shield, not a full sandbox, general host-secret isolation layer, live Codex runner, live LLM runner, or cyber-execution authorization.

---

## 4. TDD Evidence

### 4.1 RED

The implementation subagent added failing tests before production changes. Representative RED failures:

```text
go test ./cmd/blk-pipe -run 'TestPayload.*Oversized|TestRunPayload' -v
undefined: contracts.DefaultMaxPayloadJSONBytes
FAIL github.com/camcamcami/BLK-System/cmd/blk-pipe [build failed]
```

```text
go test ./internal/contracts -run 'TestPayload.*ValidationCommand|TestPayload.*TooMany' -v
undefined: DefaultMaxValidationCommands
undefined: DefaultMaxValidationCommandBytes
FAIL github.com/camcamcami/BLK-System/internal/contracts [build failed]
```

```text
go test ./internal/validation -run TestValidationRunUsesOverallDeadline -v
validation_002 ran after overall deadline
--- FAIL: TestValidationRunUsesOverallDeadline
```

The review-requested cancellation regression was also reproduced before the fix:

```text
validation.Run(ctx already canceled, commands=["printf should-not-run"]) returned nil error with empty outcomes
```

### 4.2 GREEN

After implementation and review-requested amendment, focused validation passed:

```text
go test ./cmd/blk-pipe -run 'TestPayload.*Oversized|TestRunPayload' -v
PASS
ok  github.com/camcamcami/BLK-System/cmd/blk-pipe
```

```text
go test ./internal/contracts -run 'TestPayload.*ValidationCommand|TestPayload.*TooMany' -v
PASS
ok  github.com/camcamcami/BLK-System/internal/contracts
```

```text
go test ./internal/validation -v
PASS
ok  github.com/camcamcami/BLK-System/internal/validation
```

```text
go test ./internal/pipe -run 'Test.*Validation' -v
PASS
ok  github.com/camcamcami/BLK-System/internal/pipe
```

```text
go test ./...
PASS
```

---

## 5. Review Results

Two fresh review gates were run after implementation.

### 5.1 First review pass

- Spec compliance review: `PASS`.
- Code-quality/safety review: `REQUEST_CHANGES`.

Blocking finding: `internal/validation/validation.go` could silently treat an already-canceled validation context as success by breaking out of the command loop and returning an empty non-failing result.

### 5.2 Fix and second review pass

Fix applied:

- Already-canceled context before the first validation command returns an error.
- Overall context expiration after some validation progress records a deterministic timeout failure rather than success.
- Timed-out or flooded validation commands stop later validation commands.
- Added regression tests:
  - `TestRunAlreadyCanceledContextDoesNotReturnValidationSuccess`
  - `TestRunOverallDeadlineBeforeLaterCommandDoesNotReturnSuccess`

Second review results:

- Spec compliance review: `PASS`.
- Code-quality/safety review: `APPROVED`.

---

## 6. Final Verification

Final verification before pushing implementation:

```text
export PATH="$HOME/.local/bin:$PATH"
gofmt -l cmd/blk-pipe/main.go cmd/blk-pipe/main_test.go internal/contracts/payload.go internal/contracts/payload_test.go internal/validation/validation.go internal/validation/validation_test.go
go test ./cmd/blk-pipe -run 'TestPayload.*Oversized|TestRunPayload' -v
go test ./internal/contracts -run 'TestPayload.*ValidationCommand|TestPayload.*TooMany' -v
go test ./internal/validation -v
go test ./internal/pipe -run 'Test.*Validation' -v
go test ./...
go vet ./...
production direct-Git grep
production broad-staging grep
triple-dot diff grep across touched production/docs/plan/outcomes
git diff --check HEAD^ HEAD
git status --short --branch
git log --oneline --decorate -4
```

All final checks passed. Implementation was pushed:

```text
To https://github.com/camcamcami/BLK-System.git
   fe3d198..e13d56f  main -> main
```

---

## 7. Deviations / Notes

- `internal/pipe/run.go` did not require a code change because the existing call site already passed `payload.TimeoutSeconds` into validation after engine success. The task was completed by changing validation semantics so that timeout is treated as an overall phase deadline and no later commands execute after timeout/flood/cancellation.
- No new exit code was added.
- No Python adapter behavior was changed in Task 4.
- The outcome document is committed separately from the implementation commit to preserve task-code vs outcome-doc separation.

---

## 8. Next Task

Next planned Sprint 003 task: Task 5 — Preserve Adapter Status Fidelity.
