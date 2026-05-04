# BLK-pipe Sprint 006 — Task 3 Outcome

**Status:** Complete
**Date:** 2026-05-05
**Task:** Bind BLK-test MCP Stubs to Source Trace Evidence
**Commit:** `ec34932 fix: bind blk-test mcp stubs to source evidence`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Prevent PASS/FAIL-shaped BLK-test MCP mapping from existing without exact source evidence and trace-baton preservation.

Task 3 remains deterministic local remediation only. It does not call live BLK-test MCP, run Codex, call live tactical LLMs, open network sockets, spawn subprocesses, run cyber tooling, read protected BLK-req vault paths, generate RTM artifacts, or publish authoritative BEOs.

---

## 2. Files Added/Changed

Modified:

- `python/blk_orchestrator_gate.py`
- `python/test_blk_orchestrator_gate.py`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
- `README.md`

Added:

- `docs/outcomes/BLK-PIPE-006_task-003-outcome.md`

---

## 3. Behavior Implemented

### 3.1 Request-source validation

`build_blk_test_mcp_request(source_report, enabled=False)` now fails closed unless the source report includes:

- known BLK-pipe `status`,
- non-empty `beb_id`,
- non-empty `pre_engine_hash`,
- non-empty canonical `trace_artifacts`, with each `version_hash` matching `sha256:<64-lowercase-hex>`.

For evaluation-shaped disabled requests, `source_report.status` must be `SUCCESS`. SUCCESS reports must also include:

- non-empty `commit_hash`,
- non-empty `staged_files`.

Non-success source reports now raise `ValueError` instead of being shaped as `blk_test.evaluate_execution` requests. This sprint chose the plan’s preferred fail-closed behavior: raise clearly rather than returning an evaluation-shaped request for non-success input.

`enabled=True` still raises. The send stub still returns `BLOCKED` and records:

```text
network_called = False
subprocess_called = False
rtm_status = NOT_GENERATED
beo_publication = DRAFT_ONLY
```

### 3.2 Response-source binding

`map_blk_test_mcp_response(...)` now requires explicit source context:

```python
map_blk_test_mcp_response(response, *, source_request=source_request)
```

A missing `source_request` is rejected by the Python call contract before mapping can occur.

`PASS` and `FAIL` mapping now require:

- `source_request.source_status == "SUCCESS"`,
- exact response/source `beb_id` match,
- exact response/source `commit_hash` match,
- exact response/source `pre_engine_hash` match,
- exact response/source `trace_artifacts` match,
- non-empty response `checks`.

Mapped PASS/FAIL outputs preserve source-request evidence rather than trusting response-only evidence.

### 3.3 BLOCKED preservation

`BLOCKED` response mapping preserves source-request `trace_artifacts` and may omit `commit_hash` when the source context never succeeded. It does not claim BLK-test evaluation success or failure.

All mapped outputs remain fixture/draft-only:

```text
rtm_status = NOT_GENERATED
beo_publication = DRAFT_ONLY
```

### 3.4 Documentation updates

Updated BLK-013/014/015 and README so current doctrine states:

- disabled MCP request builders require source evidence,
- non-success reports are not evaluation requests,
- PASS/FAIL mapping is source-bound,
- BLOCKED mapping preserves source trace artifacts,
- live BLK-test MCP remains disabled,
- RTM generation and authoritative BEO publication remain blocked.

---

## 4. TDD Evidence

### 4.1 RED

New tests were added before implementation. The focused suite failed against the previous implementation because request validation and source-bound response mapping did not exist yet.

Representative RED failures:

```text
FAIL: test_blk_test_mcp_request_rejects_non_success_as_evaluation_request
AssertionError: ValueError not raised

FAIL: test_blk_test_mcp_response_mapping_requires_source_request
AssertionError: TypeError not raised

FAIL: test_build_blk_test_mcp_request_rejects_missing_source_evidence (... field='trace_artifacts')
AssertionError: ValueError not raised

ERROR: test_blk_test_mcp_response_mapping_accepts_future_fixture_statuses (... status='PASS')
TypeError: map_blk_test_mcp_response() got an unexpected keyword argument 'source_request'
```

Focused RED summary:

```text
Ran 24 tests in 0.003s
FAILED (failures=9, errors=13)
```

### 4.2 GREEN

After implementation, the focused Task 3 suite passed:

```text
python3 -m unittest discover -s python -p 'test_blk_orchestrator_gate.py' -v
Ran 24 tests in 0.001s
OK
```

The required source-context probe passed:

```text
source-required probe PASS
```

Full Python suite passed:

```text
python3 -m unittest discover -s python -p 'test_*.py'
Ran 84 tests in 0.952s
OK
```

---

## 5. Review Results

Sprint 006 Task 3 used deterministic local review gates only. No live tactical reviewer, live Codex, live BLK-test MCP, cyber tooling, RTM generation, Hindsight, or authoritative BEO publication was used.

### 5.1 Spec / traceability gate

Passed. The gate verified:

- PASS cannot map without `source_request`,
- PASS rejects `beb_id`, `commit_hash`, and `pre_engine_hash` mismatches,
- PASS rejects missing or mismatched `trace_artifacts`,
- PASS rejects empty `checks`,
- non-success source reports cannot become evaluation requests,
- BLOCKED mapping preserves source trace artifacts and may omit commit evidence,
- BLK-013/014/015 describe current disabled/source-bound behavior.

Result:

```text
SPEC_TRACEABILITY_GATE_PASS
DOC_SOURCE_BINDING_GATE_PASS
```

### 5.2 Safety / docs-quality gate

Passed. The gate verified:

- runtime code did not import or call socket/subprocess/network helpers,
- runtime code did not introduce protected active-vault path access tokens,
- touched Markdown fences are balanced,
- touched files have final newlines,
- touched files have no trailing whitespace.

Result:

```text
SAFETY_DOCS_GATE_PASS
```

---

## 6. Full Verification

Final verification before the implementation commit passed:

```text
python3 -m unittest discover -s python -p 'test_*.py'
Ran 84 tests in 0.952s
OK

go test ./...
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	7.939s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)

go vet ./...
PASS

go run ./cmd/blk-pipe --health
{"status":"OK","component":"blk-pipe"}

production broad-staging grep
PASS

production direct-Git grep
PASS

triple-dot diff grep over BLK-pipe active docs
PASS

git diff --check
PASS
```

---

## 7. Residual Scope

Task 3 does not authorize live integration. Still blocked after this task:

- live Codex invocation,
- live tactical LLM/API calls,
- cyber tooling or cyber execution,
- live BLK-test MCP calls,
- RTM generation,
- authoritative BEO publication,
- protected BLK-req vault reads from `docs/active/`, `docs/requirements/`, or `docs/use_cases/`.

Remaining Sprint 006 work:

1. Task 4 — repair active doctrine drift against BLK-001.
2. Task 5 — fix outcome remote metadata and extend metadata gates.
3. Task 6 — sprint closeout and next-sprint seed.
