# BLK-System Sprint 012 — Task 5 Outcome

**Status:** Complete
**Date:** 2026-05-06
**Task:** Prove Fixed Inert Process Timeout, Output Flood, and Process-Tree Kill Path
**Sprint:** BLK-SYSTEM-012 — Workspace Isolation and Process-Control Implementation Probes
**Implementation Commit:** `c59de8f test: prove inert process timeout flood kill probes`
**Remote:** implementation pushed to `origin/main`

---

## 1. Objective

Task 5 extends the BLK-SYSTEM-012 dependency-free Python probe module with a fixed inert child-process runner and deterministic unittest probes for timeout, output flood, process-tree termination, bounded output capture, and non-authority evidence.

This remains a local probe-only implementation. It does not authorize live BLK-test MCP, live MCP client/server startup, fixed-tool test execution, network access, BEO publication, RTM generation, RTM drift authority, primary-repo mutation from probe code, staging from probe code, commits from probe code, production sandbox enforcement, or production host-secret isolation.

---

## 2. Files Added/Changed

Modified:

- `python/blk_test_mcp_workspace_process_probes.py`
- `python/test_blk_test_mcp_workspace_process_probes.py`

Outcome document:

- `docs/outcomes/BLK-SYSTEM-012_task-005-outcome.md`

---

## 3. Behavior Implemented

Added the public Task 5 API:

```python
def run_fixed_inert_process_probe(
    probe_name: str,
    *,
    cwd,
    timeout_seconds: float,
    max_output_bytes: int,
    env=None,
) -> dict[str, object]:
    """Run only fixed inert local probes and return bounded process-control evidence."""
```

Allowed probe names are fixed to:

- `exit_zero`
- `exit_nonzero`
- `timeout`
- `output_flood`
- `descendant_timeout`

Unknown probe names return `PROBE_BLOCKED_UNKNOWN_NAME` without spawning.

Process-control behavior:

- child snippets are fixed inert Python snippets only;
- child and descendant Python interpreters use `sys.executable` with `-I -S` startup isolation;
- child processes are launched with `start_new_session=True` for process-group isolation;
- no shell execution is used;
- timeout and output flood use one shared process-tree kill helper returning `SHARED_TIMEOUT_FLOOD_KILL`;
- output is read through bounded nonblocking pipe handling, not unbounded accumulation;
- direct-child exit triggers process-group cleanup before pipe drain so descendants inheriting stdout/stderr cannot hang the runner;
- result evidence remains `PROBE_ONLY` and records no BEO/RTM authority fields.

Required result evidence includes:

```text
authority = PROBE_ONLY
probe_status = PASS | FAIL | FATAL_TIMEOUT | FATAL_OUTPUT_FLOOD | PROBE_BLOCKED_UNKNOWN_NAME
inert_subprocess_called = True/False
live_mcp_subprocess_called = False
fixed_tool_tests_executed = []
network_called = False
process_tree_dead = True/False
kill_path = SHARED_TIMEOUT_FLOOD_KILL | None
stdout_bytes_captured = bounded integer
stderr_bytes_captured = bounded integer
output_truncated = True/False
```

---

## 4. TDD Evidence

### 4.1 Initial RED — missing Task 5 API

The Task 5 tests were added before the public API existed. The focused suite failed as expected:

```text
FAILED (failures=1, errors=6)
AttributeError: module 'blk_test_mcp_workspace_process_probes' has no attribute 'run_fixed_inert_process_probe'
AttributeError: module 'blk_test_mcp_workspace_process_probes' has no attribute 'subprocess'
AssertionError: 'run_fixed_inert_process_probe' not found in source
```

### 4.2 Review-driven RED gates

The first hostile code-quality review found two real issues:

- `descendant_timeout` marker evidence was checked after `TemporaryDirectory` cleanup;
- caller-supplied `PYTHONPATH` could pre-execute `sitecustomize.py` before fixed snippets.

I added regression tests before fixing startup isolation. The focused suite failed as expected:

```text
FAILED (failures=2)
test_python_startup_environment_cannot_preexecute_unfixed_code ... FAIL
test_source_uses_fixed_subprocess_without_shell_or_dynamic_dispatch ... FAIL
```

A second hostile review found the same startup risk in the nested descendant Python process and requested an explicit no-hang regression for parent-exits-before-pipe-holding-descendant. I added those regressions and fixed descendant startup isolation with `-I -S` as well.

### 4.3 GREEN — focused Task 5 gate

Command:

```bash
python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
```

Final result:

```text
Ran 46 tests in 2.558s

OK
```

Focused Task 5 coverage includes:

- `exit_zero` returns `PASS`;
- `exit_nonzero` returns `FAIL` and preserves exit code `7`;
- `timeout` returns `FATAL_TIMEOUT`, kills the process group, and reports `process_tree_dead`;
- `output_flood` returns `FATAL_OUTPUT_FLOOD`, caps captured output, and uses `SHARED_TIMEOUT_FLOOD_KILL`;
- `descendant_timeout` kills descendants before cleanup release;
- unknown probe names reject without spawning;
- module source contains no shell execution or dynamic-dispatch markers;
- process results contain no BEO publication or RTM authority fields;
- top-level and nested Python startup cannot pre-execute `PYTHONPATH`/`sitecustomize.py` code;
- direct-child exit before a pipe-holding descendant does not hang.

---

## 5. Review Evidence

Final hostile reviews:

```text
Spec compliance review: PASS
Code quality/safety review: APPROVED
```

Notable review-driven fixes:

- moved descendant escape-marker assertion before temporary-directory cleanup;
- added Python startup isolation with `-I -S` for the top-level child interpreter;
- added Python startup isolation with `-I -S` for the nested descendant interpreter;
- added regression coverage for `PYTHONPATH`/`sitecustomize.py` pre-execution attempts;
- added regression coverage for the child-exits-first, descendant-holds-pipe no-hang case.

---

## 6. Verification

Commands run from `/home/dad/BLK-System`:

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

Results:

```text
Focused Task 5 suite: Ran 46 tests in 2.558s — OK
Full Python unittest suite: Ran 200 tests in 3.238s — OK
go test ./...: OK
go vet ./...: OK
git diff --check: OK
```

Additional stress/regression gates:

```bash
python3 - <<'PY'
import subprocess, sys
cmd=[sys.executable, '-m', 'unittest', 'discover', '-s', 'python', '-p', 'test_blk_test_mcp_workspace_process_probes.py']
for i in range(5):
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode:
        print(result.stdout, end='')
        print(result.stderr, end='')
        raise SystemExit(result.returncode)
    print(f'focused repeat {i + 1}/5 passed')
PY
go test -race ./...
```

Results:

```text
focused repeat 1/5 passed
focused repeat 2/5 passed
focused repeat 3/5 passed
focused repeat 4/5 passed
focused repeat 5/5 passed
go test -race ./...: OK
```

---

## 7. Scope and Non-Goals Preserved

Task 5 does not add or authorize:

- live BLK-test MCP execution;
- live MCP server/client startup;
- arbitrary command execution;
- shell execution;
- network clients or servers;
- package-manager calls;
- Git write commands from probe code;
- fixed BLK-test tool descriptor execution;
- BEO publication;
- RTM generation;
- RTM drift rejection authority;
- protected BLK-req vault reads;
- production sandbox/cgroup/VM enforcement claims;
- production host-secret isolation claims.

---

## 8. Result

BLK-SYSTEM-012 Task 5 is complete. The implementation and this outcome document were pushed to GitHub after the task, matching the updated outcome-doc policy.
