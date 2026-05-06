# BLK-SYSTEM-014 — Task 3 Outcome

**Status:** Complete
**Date:** 2026-05-07T06:50:56+10:00
**Task:** Dependency-free stdio fixed-tool smoke harness
**Commit:** `181c2eb feat: add bounded stdio fixed-tool smoke harness`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Implement the bounded local stdio process path and one fixed `run_ast_validation` tool against synthetic isolated workspaces, without running the official first live smoke.

## 2. Files Added/Changed

- Modified `python/blk_test_mcp_fixed_tool_live_smoke.py`.
- Modified `python/test_blk_test_mcp_fixed_tool_live_smoke.py`.
- Added this outcome document.

## 3. Behavior Implemented

Task 3 added:

- `fixed_sprint014_live_tool_registry_descriptor()` exposing only `run_ast_validation`.
- `validate_sprint014_smoke_workspace(...)` rejecting primary repo, root/home paths, `.git` metadata, protected BLK-req prefixes, and symlink escapes.
- `resolve_sprint014_fixed_tool_command(...)` returning a static Python file-entrypoint command and rejecting caller-supplied command paths.
- `run_sprint014_fixed_tool_stdio_smoke(...)` running a dependency-free line-delimited JSON-RPC/MCP-subset stdio child process.

The child supports `initialize`, `tools/list`, and `tools/call` for `run_ast_validation`. It returns:

- `PASS` when `src/smoke_fixture.py` parses and contains `SMOKE_FIXTURE = True`;
- `FAIL` for syntax errors or missing smoke marker;
- `BLOCKED` when the fixture is absent;
- `FATAL_TIMEOUT` for bounded timeout;
- `FATAL_OUTPUT_FLOOD` for bounded output overflow.

All returned evidence keeps no source-write, no BEO publication, no RTM generation, and no active-vault-read authority.

## 4. TDD Evidence

### 4.1 RED

Focused Task 3 tests failed before harness helpers existed:

```text
ImportError: cannot import name 'fixed_sprint014_live_tool_registry_descriptor'
```

### 4.2 GREEN

Focused Sprint 014 suite after implementation:

```text
Ran 17 tests in 1.127s

OK
```

Source-scan gate:

```text
Sprint 014 live-smoke source scan: PASS
```

## 5. Review Results

Self-review confirmed the command is static, uses stdio pipes, rejects caller-supplied commands, preserves a single fixed tool, returns bounded/sanitized output excerpts, and preserves non-authority fields. Workspace tests cover real-repo/home/root rejection, `.git` rejection, protected prefix rejection, symlink escape rejection, and synthetic workspace acceptance.

## 6. Final Verification

```text
python -m py_compile python/blk_test_mcp_fixed_tool_live_smoke.py: PASS
git diff --check: PASS
Staged paths:
python/blk_test_mcp_fixed_tool_live_smoke.py
python/test_blk_test_mcp_fixed_tool_live_smoke.py
```

Implementation commit:

```text
181c2eb feat: add bounded stdio fixed-tool smoke harness
```

## 7. Deviations / Notes

The static child command uses the Python script file directly rather than `-c` or caller-supplied arguments. The command avoids isolated `-I` because the child script imports the adjacent Sprint 013 approval helper from the repository `python/` directory; the command remains static, stdio-only, dependency-free, and non-networked.

## 8. Next Task

Task 4 — commit-before-approval checkpoint and first live smoke.
