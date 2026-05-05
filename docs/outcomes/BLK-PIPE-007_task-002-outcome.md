# BLK-pipe Sprint 007 — Task 2 Outcome

**Status:** Complete
**Date:** 2026-05-05
**Task:** Add Explicit Disabled Not-Run MCP Request Shape for Non-SUCCESS Source Reports
**Commit:** `118a329 feat: add disabled blk-test mcp not-run request shape`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Add an explicit disabled BLK-test MCP not-run request shape for known non-`SUCCESS` BLK-pipe source reports.

The purpose was to let disabled adapter/BEO/RTM fixture paths represent BLK-test-not-run evidence without weakening the existing rule that non-success BLK-pipe reports must not become `blk_test.evaluate_execution` requests.

---

## 2. Files Added/Changed

Changed implementation/test files:

- `python/blk_orchestrator_gate.py`
- `python/test_blk_orchestrator_gate.py`
- `python/blk_test_mcp_adapter_smoke.py`
- `python/test_blk_test_mcp_adapter_smoke.py`

Created outcome file:

- `docs/outcomes/BLK-PIPE-007_task-002-outcome.md`

No active doctrine files were changed in Task 2; BLK-016/README active-contract updates remain scoped to Task 5.

---

## 3. Behavior Implemented

Implemented public helper:

```python
def build_blk_test_mcp_not_run_request(
    source_report: dict[str, Any],
    *,
    enabled: bool = False,
) -> dict[str, Any]:
    ...
```

The helper now:

1. Raises `RuntimeError` when `enabled=True`; it does not open a live MCP path.
2. Requires a known non-success BLK-pipe status.
3. Rejects `status == "SUCCESS"` and points callers to `build_blk_test_mcp_request(...)` for evaluation-shaped disabled requests.
4. Requires non-empty `beb_id`, non-empty `pre_engine_hash`, and non-empty canonical `trace_artifacts`.
5. Preserves optional `commit_hash`, `staged_files`, and `destroyed_files` without requiring success-only commit/staging evidence.
6. Returns a disabled request with:
   - `enabled: False`
   - `transport: "DISABLED_STUB"`
   - `method: "blk_test.not_run"`
   - `source_status: <non-success BLK-pipe status>`
   - `rtm_status: "NOT_GENERATED"`
   - `beo_publication: "DRAFT_ONLY"`
   - a deterministic reason string that names the source status.

Also updated `run_disabled_blk_test_mcp_adapter_smoke(...)` so it now selects:

- `build_blk_test_mcp_request(...)` for `SUCCESS` source reports,
- `build_blk_test_mcp_not_run_request(...)` for known non-success source reports.

The response mapper behavior remains fail-closed:

- `BLOCKED` can map from a not-run source request.
- `PASS`/`FAIL` still require `source_status == "SUCCESS"` and reject not-run source context.

Existing `build_blk_test_mcp_request(non_success_report)` behavior was preserved: non-success source reports still raise instead of producing `blk_test.evaluate_execution`.

---

## 4. TDD Evidence

### 4.1 RED

Tests were added first in:

- `python/test_blk_orchestrator_gate.py`
- `python/test_blk_test_mcp_adapter_smoke.py`

Initial focused RED for the missing public helper:

```text
test_blk_orchestrator_gate (unittest.loader._FailedTest.test_blk_orchestrator_gate) ... ERROR
ImportError: cannot import name 'build_blk_test_mcp_not_run_request' from 'blk_orchestrator_gate'
Ran 1 test in 0.000s
FAILED (errors=1)
```

Adapter-smoke RED before routing non-success reports to the not-run builder:

```text
test_disabled_adapter_smoke_builds_not_run_request_for_non_success_without_response ... ERROR
test_disabled_adapter_smoke_maps_not_run_source_only_to_blocked_fixture ... ERROR
test_disabled_adapter_smoke_rejects_not_run_pass_fixture ... FAIL
ValueError: BLK-test MCP evaluation request requires source_report status SUCCESS; got SYNTAX_GATE_FAILED
Ran 8 tests in 0.001s
FAILED (failures=1, errors=2)
```

These failures matched the planned Task 2 RED signal: the not-run request helper did not exist, and adapter smoke still tried to treat non-success source reports as evaluation requests.

### 4.2 GREEN

Focused orchestrator gate suite after implementation:

```text
Ran 29 tests in 0.002s
OK
```

Focused adapter-smoke suite after implementation:

```text
Ran 8 tests in 0.001s
OK
```

Full Python suite after implementation:

```text
Ran 97 tests in 0.645s
OK
```

---

## 5. Review Results

Plan-specific deterministic local review gates were used. No live Codex, live tactical LLM, network-model, cyber, or live BLK-test MCP reviewer was dispatched.

Deterministic Task 2 spec gate verified:

- only expected implementation/test files changed before the outcome doc,
- `build_blk_test_mcp_request(non_success_report)` still rejects evaluation-shaped requests,
- `build_blk_test_mcp_not_run_request(non_success_report)` returns `method: "blk_test.not_run"`,
- the not-run request preserves `beb_id`, `pre_engine_hash`, exact `trace_artifacts`, `rtm_status: "NOT_GENERATED"`, and `beo_publication: "DRAFT_ONLY"`,
- `build_blk_test_mcp_not_run_request(success_report)` rejects and points to the evaluation-shaped helper,
- `BLOCKED` can map from not-run source context,
- `PASS` cannot map from not-run source context,
- adapter smoke routes non-success source reports to not-run/BLOCKED without reporting live transport.

Gate output:

```text
TASK2_SPEC_GATE_PASS
TASK2_SAFETY_GATE_PASS
```

Safety gate verified runtime implementation files do not import or call forbidden live-capability modules/patterns, including network, subprocess, active-vault reads, and `shell=True`.

Additional repository safety greps:

```text
DIRECT_GIT_GREP_PASS
BROAD_STAGING_GREP_PASS
TRIPLE_DOT_DIFF_GREP_PASS
```

Review verdict:

```text
PASS — Task 2 implementation matches the sprint plan and preserves disabled/not-run authority boundaries.
```

---

## 6. Final Verification

Final focused/shared verification before implementation commit:

```text
python3 -m unittest discover -s python -p 'test_blk_orchestrator_gate.py' -v -> Ran 29 tests, OK
python3 -m unittest discover -s python -p 'test_blk_test_mcp_adapter_smoke.py' -v -> Ran 8 tests, OK
python3 -m unittest discover -s python -p 'test_*.py' -> Ran 97 tests, OK
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

Task 2 did not run or enable:

- live Codex,
- live tactical LLMs,
- network model services,
- cyber tooling or cyber execution,
- live BLK-test MCP,
- live MCP transport,
- RTM generation,
- RTM authority,
- authoritative BEO publication,
- sandbox/capability enforcement,
- real approval-channel mechanics,
- active BLK-req vault reads or requirement-body parsing.

The new `blk_test.not_run` shape is disabled fixture/interface data only. It records why BLK-test did not run and preserves opaque source trace metadata for later fixture-only BEO/RTM interface coverage.

---

## 8. Deviations / Notes

- The implementation commit excludes this outcome document; the outcome is committed separately to preserve the established BLK-System outcome workflow.
- No active-contract documentation was updated in Task 2 because the Sprint 007 plan assigns consolidated BLK-016/README documentation updates to Task 5.

---

## 9. Next Task

Proceed to Task 3: project source-bound disabled MCP PASS/FAIL fixture output into draft BEO shape without treating it as live BLK-test authority, RTM generation, or authoritative BEO publication.
