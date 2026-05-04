# BLK-pipe Sprint 005 — Task 4 Outcome

**Status:** Complete
**Date:** 2026-05-05
**Task:** Preserve BLK-pipe Execution Evidence in Python Adapters
**Commit:** `def41ff feat: preserve blk-pipe execution evidence in python adapters`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Preserve BLK-pipe execution evidence through the Python adapter and dry-run fixture invocation path so future orchestration and BLK-test handoff code can inspect success and non-success reports without reparsing stdout or losing context.

Task 4 specifically required preserving:

- `commit_hash`,
- `staged_files`,
- `destroyed_files`,
- `raw_report`,
- `stderr`,
- nonzero return-code family behavior.

The task also required a no-throw dry-run invocation helper that returns parsed non-success reports so `BLOCKED` BLK-test handoffs can be built without misrouting BLK-pipe failures as BLK-test `FAIL`.

---

## 2. Files Added/Changed

Modified:

- `python/blk_pipe_adapter.py`
- `python/test_blk_pipe_adapter.py`
- `python/blk_pipe_dry_run_orchestrator.py`
- `python/test_blk_pipe_dry_run_orchestrator.py`
- `python/test_beo_fixture_projection.py`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`

Created:

- `docs/outcomes/BLK-PIPE-005_task-004-outcome.md`

---

## 3. Behavior Implemented

### 3.1 Adapter evidence fields

`ExecutionResult` now includes:

```python
commit_hash: str = ""
staged_files: list[str] | None = None
destroyed_files: list[str] | None = None
raw_report: dict | None = None
stderr: str = ""
```

Parsed BLK-pipe JSON reports now preserve those fields on both success and non-success paths.

### 3.2 Existing status safety preserved

The adapter still routes by subprocess return-code family first:

- unknown nonzero exits still force `INTERNAL_ERROR`, even if stdout claims `SUCCESS`,
- non-JSON stdout still maps to `FATAL_CRASH`,
- exit-code-compatible parsed statuses are still preserved,
- temp payload files are still removed in `finally`,
- subprocess calls remain shell-free argv calls.

### 3.3 No-throw dry-run fixture invocation

Added:

```python
@dataclass(frozen=True)
class DryRunExecutionResult:
    returncode: int
    status: str
    report: dict
    stderr: str


def invoke_blk_pipe_dry_run_fixture(...) -> DryRunExecutionResult: ...
```

This helper parses and returns non-success BLK-pipe JSON reports without raising. The existing success-focused `run_blk_pipe_dry_run_fixture(...)` wrapper remains available and is implemented on top of the no-throw helper; it still raises on nonzero return codes for existing success-only callers.

### 3.4 BLOCKED handoff path proven

A new end-to-end fixture test proves a non-success dry-run report can be returned, inspected, and converted into a deterministic BLK-test `BLOCKED` handoff without BLK-test MCP, live Codex, live tactical LLMs, network model services, or cyber tooling.

---

## 4. TDD Evidence

### 4.1 RED

After adding the Task 4 tests and before implementation, focused tests failed as expected:

```text
AttributeError: 'ExecutionResult' object has no attribute 'commit_hash'
AttributeError: 'ExecutionResult' object has no attribute 'destroyed_files'
AttributeError: 'ExecutionResult' object has no attribute 'raw_report'
ImportError: cannot import name 'DryRunExecutionResult' from 'blk_pipe_dry_run_orchestrator'
ImportError: cannot import name 'invoke_blk_pipe_dry_run_fixture' from 'blk_pipe_dry_run_orchestrator'
```

Command used:

```bash
python3 -m unittest discover -s python -p 'test_blk_pipe_adapter.py' -v
python3 -m unittest discover -s python -p 'test_blk_pipe_dry_run_orchestrator.py' -v
python3 -m unittest discover -s python -p 'test_beo_fixture_projection.py' -v
```

### 4.2 GREEN

After implementation, the focused Task 4 tests passed:

```text
python3 -m unittest discover -s python -p 'test_blk_pipe_adapter.py' -v
# Ran 20 tests ... OK

python3 -m unittest discover -s python -p 'test_blk_pipe_dry_run_orchestrator.py' -v
# Ran 16 tests ... OK

python3 -m unittest discover -s python -p 'test_beo_fixture_projection.py' -v
# Ran 8 tests ... OK
```

Full Python suite also passed:

```text
python3 -m unittest discover -s python -p 'test_*.py'
# Ran 57 tests ... OK
```

---

## 5. Review Results

Live Codex, live tactical LLM reviewer agents, Hindsight, network model services, cyber tooling, and live BLK-test MCP were not used. The two required review gates were executed as deterministic local scripts.

### 5.1 Spec / Traceability Review

Result:

```text
SPEC/TRACEABILITY REVIEW PASS
```

The gate verified:

- all required `ExecutionResult` fields exist,
- parsed JSON reports preserve `commit_hash`, `staged_files`, `destroyed_files`, `raw_report`, and `stderr`,
- unknown nonzero exits still force `INTERNAL_ERROR`,
- non-JSON stdout still maps to `FATAL_CRASH`,
- required tests exist,
- `DryRunExecutionResult` and `invoke_blk_pipe_dry_run_fixture(...)` exist,
- success wrapper delegates to the no-throw helper,
- docs describe the new evidence-preserving behavior.

### 5.2 Safety / Documentation Review

Result:

```text
SAFETY/DOCS REVIEW PASS
```

The gate verified:

- touched files have final newlines and no trailing whitespace,
- touched Markdown fences are balanced,
- production adapter/orchestrator subprocess usage remains `shell=False` by omission and explicit argv-list based,
- subprocess calls use `check=False`,
- temp payload cleanup remains in `finally`,
- runtime code did not introduce forbidden live-execution tokens.

---

## 6. Final Verification

Implementation commit verification before push:

```bash
python3 -m unittest discover -s python -p 'test_blk_pipe_adapter.py' -v
python3 -m unittest discover -s python -p 'test_blk_pipe_dry_run_orchestrator.py' -v
python3 -m unittest discover -s python -p 'test_blk_test_handoff_fixtures.py' -v
python3 -m unittest discover -s python -p 'test_beo_fixture_projection.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

All passed.

Additional deterministic safety greps passed:

```text
direct git grep PASS
broad staging grep PASS
triple-dot grep PASS
```

Post-commit verification also passed:

```bash
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check HEAD^ HEAD
```

Final implementation state:

```text
## main...origin/main
```

---

## 7. Deviations / Notes

- No Hindsight tools were used.
- No live Codex, live tactical LLMs, network model services, cyber tooling, or live BLK-test MCP were run.
- The no-throw helper still raises on non-JSON stdout because there is no parsed BLK-pipe report to preserve. This keeps the helper focused on the Task 4 requirement: returning parsed non-success report evidence without raising.
- `run_blk_pipe_dry_run_fixture(...)` remains success-focused for existing tests and callers; callers needing BLOCKED evidence should use `invoke_blk_pipe_dry_run_fixture(...)`.

---

## 8. Next Task

Task 5 — Canonicalize Trace Metadata and BLK-Native Vocabulary in Active Doctrine.
