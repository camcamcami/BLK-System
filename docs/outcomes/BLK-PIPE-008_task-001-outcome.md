# BLK-pipe Sprint 008 — Task 1 Outcome

**Status:** Complete
**Date:** 2026-05-05
**Task:** Enforce Non-Empty Canonical Trace Artifacts for Execute Payloads
**Implementation Commit:** included in the Task 1 commit containing this outcome document
**Remote:** pending push at time of writing

---

## 1. Objective

Task 1 closes Sprint 008 finding D-001: successful governed BLK-pipe `execute` payloads must no longer be able to reach the engine and produce `SUCCESS` with `trace_artifacts: []`.

Implemented behavior:

- `action: "execute"` now requires non-empty `trace_artifacts` during `Payload.Validate()`.
- Each supplied trace artifact continues to use the existing canonical validation gate:
  - `kind` non-empty and <= 256 bytes;
  - `id` non-empty and <= 256 bytes;
  - `version_hash` matches `sha256:<64-lowercase-hex>`;
  - at most 64 artifacts.
- `action: "revert"` does not require trace artifacts.
- Invalid-payload failure reports still emit stable empty fields and do not echo malformed/oversized trace bodies.
- Legacy-shaped `execute` payloads remain accepted only when they also carry non-empty canonical `trace_artifacts`.

---

## 2. Files Changed

Updated:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/pipe/run_test.go`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`

Created outcome:

- `docs/outcomes/BLK-PIPE-008_task-001-outcome.md`

---

## 3. RED Evidence

### Contract-level RED

After adding `TestPayloadValidateRejectsExecuteWithoutTraceArtifacts` and the revert exemption test, the expected RED occurred:

```text
=== RUN   TestPayloadValidateRejectsExecuteWithoutTraceArtifacts
    payload_test.go:41: Validate() error = nil, want trace_artifacts rejection
--- FAIL: TestPayloadValidateRejectsExecuteWithoutTraceArtifacts (0.00s)
=== RUN   TestPayloadValidateRevertDoesNotRequireTraceArtifacts
--- PASS: TestPayloadValidateRevertDoesNotRequireTraceArtifacts (0.00s)
FAIL
FAIL	github.com/camcamcami/BLK-System/internal/contracts	0.002s
FAIL
```

### Run-level RED

After adding `TestRunRejectsExecuteWithoutTraceArtifactsBeforeEngine`, BLK-pipe still ran the engine and committed a successful empty-trace result:

```text
=== RUN   TestRunRejectsExecuteWithoutTraceArtifactsBeforeEngine
    run_test.go:321: exit code = 0, want 2; report={Status:SUCCESS ExitCode:0 Action:execute ... GitDiff:diff --git a/SHOULD_NOT_EXIST.txt b/SHOULD_NOT_EXIST.txt ... TraceArtifacts:[] ValidationLogs:map[validation_001:] ... StagedFiles:[SHOULD_NOT_EXIST.txt] ...}
--- FAIL: TestRunRejectsExecuteWithoutTraceArtifactsBeforeEngine (0.05s)
FAIL
FAIL	github.com/camcamcami/BLK-System/internal/pipe	0.048s
FAIL
```

This proved the pre-Task-1 gap: an execute payload with absent `trace_artifacts` could reach engine execution and produce a success report with `trace_artifacts: []`.

---

## 4. GREEN Implementation

Minimal implementation:

- Added an execute-only presence check in `Payload.Validate()` after canonical trace shape validation and after the `revert` exemption:

```text
trace_artifacts must be non-empty for execute payloads
```

- Kept `ValidateTraceArtifacts(...)` reusable for shape validation, including empty slices in non-execute/report-copy contexts.
- Updated success-oriented contract and run fixtures to include deterministic canonical traces.
- Added a run-level regression test that marshals an execute payload without traces directly, bypassing test helper trace injection, and asserts:
  - exit code `ExitInvalidPayload` / `2`;
  - report status `INVALID_PAYLOAD`;
  - error mentions `trace_artifacts` and `non-empty`;
  - `SHOULD_NOT_EXIST.txt` was never created, proving the engine did not run;
  - stable empty report fields remain stable.
- Updated BLK-010 to state that `trace_artifacts` is required/non-empty for `execute`, not required for `revert`, and remains opaque metadata that BLK-pipe does not resolve against requirement/use-case bodies or files.

---

## 5. GREEN Focused Test Evidence

Contract focused gate:

```text
=== RUN   TestPayloadValidateRejectsExecuteWithoutTraceArtifacts
--- PASS: TestPayloadValidateRejectsExecuteWithoutTraceArtifacts (0.00s)
=== RUN   TestPayloadValidateRevertDoesNotRequireTraceArtifacts
--- PASS: TestPayloadValidateRevertDoesNotRequireTraceArtifacts (0.00s)
PASS
```

Expanded contracts gate:

```text
go test ./internal/contracts -run 'Trace|PayloadValidate|DecodePayload' -v
PASS
ok  	github.com/camcamcami/BLK-System/internal/contracts	0.005s
```

Run-level focused gate:

```text
go test ./internal/pipe -run 'Trace|WithoutTrace|V47|Success' -v
PASS
ok  	github.com/camcamcami/BLK-System/internal/pipe	0.762s
```

Whole Go gate:

```text
go test ./...
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	0.020s
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	6.763s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)
```

---

## 6. Shared Verification

Final shared verification before commit:

```text
python3 -m unittest discover -s python -p 'test_*.py'
.................................................................................................................
----------------------------------------------------------------------
Ran 113 tests in 0.691s

OK

go test ./... -> PASS

go vet ./... -> PASS

go run ./cmd/blk-pipe --health -> {"status":"OK","component":"blk-pipe"}

git diff --check -> PASS
```

Post-test cleanup:

```text
python/__pycache__/ removed before committing.
```

---

## 7. Authority / Safety Boundary

Task 1 did not run or enable:

- live Codex;
- live tactical LLM APIs;
- network model services;
- cyber tooling or cyber execution;
- live BLK-test MCP;
- live MCP transport;
- authoritative BLK-test verdict authority;
- authoritative BEO publication;
- RTM generation;
- RTM drift authority;
- sandbox/container/cgroup/VM enforcement;
- production host-secret isolation claims;
- production approval-channel mechanics;
- active BLK-req vault reads or requirement-body parsing.

The change only hardens deterministic local BLK-pipe payload validation and updates local tests/docs for that boundary.

---

## 8. Remaining Sprint 008 Work

Task 1 closes D-001 only. Remaining Sprint 008 tasks still own:

- Task 2 / D-002: canonical trace validation in BLK-test handoff fixtures;
- Task 3 / D-003: strict tracked-vs-new allowlist semantics;
- Task 4 / D-004: no-candidate gate before validation;
- Task 5 / D-005 through D-009: BLK-004/BLK-010 current-state decision overlay;
- Task 6: sprint closeout and hostile self-review.
