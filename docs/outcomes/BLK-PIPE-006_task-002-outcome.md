# BLK-pipe Sprint 006 — Task 2 Outcome

**Status:** Complete
**Date:** 2026-05-05
**Task:** Require Canonical Trace Artifact Hashes
**Commit:** `890fa29 fix: require canonical blk trace artifact hashes`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Align BLK-pipe and Python fixture contracts with BLK-001’s cryptographic baton intent by requiring canonical `sha256:<64-lowercase-hex>` `version_hash` values at deterministic contract boundaries.

Task 2 validates syntax only. It does not read, parse, or verify active BLK-req vault files, does not generate an RTM, and does not publish an authoritative BEO.

No live Codex, live tactical LLMs, network model services, cyber tooling, live BLK-test MCP, Hindsight, RTM generation, or authoritative BEO publication were used.

---

## 2. Files Added/Changed

Modified:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/contracts/report_test.go`
- `internal/pipe/run_test.go`
- `python/blk_orchestrator_gate.py`
- `python/test_blk_orchestrator_gate.py`
- `python/blk_pipe_dry_run_orchestrator.py`
- `python/test_blk_pipe_dry_run_orchestrator.py`
- `python/test_blk_pipe_adapter.py`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`

Added:

- `docs/outcomes/BLK-PIPE-006_task-002-outcome.md`

---

## 3. Behavior Implemented

### 3.1 Go contract validation

`contracts.ValidateTraceArtifacts(...)` now rejects noncanonical trace artifact hashes.

A supplied `trace_artifacts[*].version_hash` must match:

```text
sha256:<64-lowercase-hex>
```

The Go validator now rejects:

- missing `version_hash`,
- missing `sha256:` prefix,
- short hashes such as `sha256:0123456789abcdef`,
- uppercase hex,
- non-hex characters,
- oversized values without echoing the rejected hash body.

Existing bounds remain intact:

- at most 64 trace artifacts,
- bounded `kind` and `id` lengths,
- no requirement/use-case body parsing,
- no comparison against live BLK-req vault files.

### 3.2 Python approval/MCP stub validation

`python/blk_orchestrator_gate.py` now uses the same canonical hash regex for trace metadata accepted by disabled BLK-test MCP request/response stubs:

```text
^sha256:[0-9a-f]{64}$
```

The Python stub boundary now rejects malformed `trace_artifacts[*].version_hash` values instead of silently preserving malformed or PASS-shaped trace data.

`trace_hash` validation for the approval-token path was also reworded to the same canonical syntax language.

### 3.3 Python dry-run fixture validation

`python/blk_pipe_dry_run_orchestrator.py` now validates synthetic fixture trace hashes during BEB fixture loading and when serializing `TraceArtifact` payload objects.

The synthetic ID remains unchanged:

```text
REQ-DRY-001
```

The synthetic fixture hash must still be canonical syntax. The parser validates syntax only; it does not verify the hash against requirement files.

### 3.4 Test fixture updates

Existing Go and Python test fixtures that were intentionally preserving trace artifact values were updated from short historical hashes to canonical 64-lowercase-hex hashes.

Short, uppercase, and non-hex values remain present only in negative tests.

### 3.5 Documentation updates

Active contract docs now state the canonical syntax consistently:

```text
sha256:<64-lowercase-hex>
```

Updated docs preserve the authority boundary: BLK-pipe and Python fixtures validate syntax but do not parse protected BLK-req content or verify hashes against files under:

- `docs/active/`
- `docs/requirements/`
- `docs/use_cases/`

---

## 4. TDD Evidence

### 4.1 RED

Before implementation, the new Go tests failed because the existing validator only checked the `sha256:` prefix:

```text
=== RUN   TestPayloadDecodeRejectsTraceArtifactShortSHA256Hash
    payload_test.go:255: DecodePayload() error = nil, want non-nil
--- FAIL: TestPayloadDecodeRejectsTraceArtifactShortSHA256Hash (0.00s)
=== RUN   TestPayloadDecodeRejectsTraceArtifactUppercaseSHA256Hash
    payload_test.go:267: DecodePayload() error = nil, want non-nil
--- FAIL: TestPayloadDecodeRejectsTraceArtifactUppercaseSHA256Hash (0.00s)
=== RUN   TestPayloadDecodeRejectsTraceArtifactNonHexSHA256Hash
    payload_test.go:279: DecodePayload() error = nil, want non-nil
--- FAIL: TestPayloadDecodeRejectsTraceArtifactNonHexSHA256Hash (0.00s)
```

The new Python approval/MCP tests failed because malformed trace hashes were not rejected:

```text
FAIL: test_blk_test_mcp_request_rejects_short_trace_hash
AssertionError: ValueError not raised

FAIL: test_blk_test_mcp_response_mapping_rejects_uppercase_trace_hash
AssertionError: ValueError not raised
```

The new dry-run fixture parser test failed because noncanonical synthetic trace hashes were accepted:

```text
FAIL: test_load_dry_run_fixture_rejects_noncanonical_trace_hash
AssertionError: ValueError not raised
```

### 4.2 GREEN

Focused Go trace tests passed after implementation:

```text
go test ./internal/contracts -run 'TestPayloadDecode.*Trace|TestReportMarshal.*Trace' -v
PASS
ok  	github.com/camcamcami/BLK-System/internal/contracts	0.003s
```

Focused Python approval/MCP tests passed:

```text
python3 -m unittest discover -s python -p 'test_blk_orchestrator_gate.py' -v
Ran 13 tests in 0.001s
OK
```

Focused Python dry-run fixture tests passed:

```text
python3 -m unittest discover -s python -p 'test_blk_pipe_dry_run_orchestrator.py' -v
Ran 19 tests in 0.193s
OK
```

Full suites also passed before commit:

```text
python3 -m unittest discover -s python -p 'test_*.py'
Ran 73 tests in 0.655s
OK
```

---

## 5. Review Results

Sprint 006 Task 2 used deterministic local review gates only. No live tactical reviewer, live Codex, live BLK-test MCP, cyber tooling, RTM generation, or authoritative BEO publication was used.

### 5.1 Spec / traceability gate

Passed. The gate verified:

- Go rejects short, uppercase, and non-hex trace artifact hashes,
- Python request/response helpers reject short, uppercase, and non-hex trace artifact hashes,
- the dry-run BEB fixture parser rejects noncanonical synthetic trace hashes,
- active contract docs use `sha256:<64-lowercase-hex>` language consistently,
- no active BLK-req vault reads were introduced.

Result:

```text
spec gate: Python short/uppercase/nonhex rejection PASS
spec gate: Go short/uppercase/nonhex rejection PASS
spec gate: active docs canonical language PASS
spec gate: no active BLK-req vault reads introduced PASS
```

### 5.2 Safety / docs-quality gate

Passed. The gate verified:

- Python error messages do not echo rejected hash bodies,
- added runtime lines did not introduce live network/model/MCP/Codex execution surfaces,
- touched Markdown fences are balanced,
- touched files have final newlines,
- touched lines have no trailing whitespace.

Result:

```text
safety gate: Python hash-body leak check PASS
safety gate: no new live-execution runtime tokens PASS
safety gate: Markdown/file hygiene PASS
```

---

## 6. Final Verification

Final verification before the implementation commit passed:

```text
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
go run ./cmd/blk-pipe --health
git diff --check
```

Observed key results:

```text
Ran 73 tests in 0.655s
OK
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	0.123s
ok  	github.com/camcamcami/BLK-System/internal/execguard	8.967s
ok  	github.com/camcamcami/BLK-System/internal/gitguard	0.955s
ok  	github.com/camcamcami/BLK-System/internal/pipe	6.927s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	0.160s
{"status":"OK","component":"blk-pipe"}
```

Implementation commit was created and pushed:

```text
890fa29 (HEAD -> main) fix: require canonical blk trace artifact hashes
To https://github.com/camcamcami/BLK-System.git
   5d6a823..890fa29  main -> main
```

Repository status after push:

```text
## main...origin/main
```

---

## 7. Deviations / Notes

- `internal/pipe/run_test.go` and `python/test_blk_pipe_adapter.py` were updated in addition to the plan’s primary file list because they contained positive-preservation fixtures with now-invalid short hash examples.
- Historical plans/outcomes that mention the older short-hash examples were not rewritten; Task 2 updated active contract docs and current tests.
- Validation is syntax-only. No code reads active BLK-req vault files or compares hashes against requirement/use-case documents.
- The disabled BLK-test MCP path remains disabled; this task only hardens request/response shape validation.
- No Hindsight was used.

---

## 8. Next Task

BLK-PIPE-006 Task 3 should bind disabled BLK-test MCP stubs to source trace evidence so PASS/FAIL-shaped mapping cannot exist without exact source evidence and trace-baton preservation.
