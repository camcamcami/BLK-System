# BLK-SYSTEM-011.1 — Task 1 Outcome

**Status:** Complete
**Date:** 2026-05-06
**Task:** Reject tainted non-stdio descriptor metadata across public helpers
**Implementation Commit:** pending before commit
**Remote:** pending push

---

## 1. Objective

Prove every public disabled-transport helper that consumes descriptor metadata rejects tainted non-stdio transport values instead of echoing or normalizing them.

## 2. Files Added/Changed

- `python/test_blk_test_mcp_disabled_transport.py`
- `python/blk_test_mcp_disabled_transport.py`
- `docs/outcomes/BLK-SYSTEM-011.1_task-001-outcome.md`

## 3. Behavior Implemented

- Added focused regressions proving direct descriptor taint is rejected for:
  - `evaluate_disabled_transport_startup(...)`
  - `build_non_executing_handshake_probe(...)`
  - `build_disabled_lifecycle_probe(...)`
- Added `_require_stdio_transport_metadata(...)` to reject non-`stdio` descriptor metadata with `ValueError` containing `stdio-only`.
- Preserved normal disabled/non-executing evidence for descriptors returned by `build_disabled_transport_descriptor()`.

## 4. TDD Evidence

### 4.1 RED

```text
PYTHONPATH=python python3 -m unittest \
  python.test_blk_test_mcp_disabled_transport.DisabledTransportStartupTest.test_startup_decision_rejects_tainted_non_stdio_descriptor_metadata \
  python.test_blk_test_mcp_disabled_transport.DisabledTransportStartupTest.test_handshake_probe_rejects_tainted_non_stdio_descriptor_metadata \
  python.test_blk_test_mcp_disabled_transport.DisabledTransportStartupTest.test_lifecycle_probe_rejects_tainted_non_stdio_descriptor_metadata -v

FAILED (failures=3)
AssertionError: ValueError not raised
```

### 4.2 GREEN

```text
PYTHONPATH=python python3 -m unittest python.test_blk_test_mcp_disabled_transport.DisabledTransportStartupTest -v
Ran 17 tests in 0.001s
OK
```

## 5. Review Results

Deterministic local review:

- Scope matched Task 1 files and required public helpers.
- Tainted metadata is rejected, not normalized.
- No live BLK-test MCP, JSON-RPC/MCP handshake, network, subprocess, fixed-tool execution, active-vault read, BEO publication, RTM generation, approval mechanics, or production sandbox/host-secret claim was introduced.

## 6. Final Verification

```text
python3 -m unittest discover -s python -p 'test_*.py'
Ran 223 tests in 5.179s
OK

go test ./...
ok github.com/camcamcami/BLK-System/cmd/blk-pipe (cached)
ok github.com/camcamcami/BLK-System/internal/contracts (cached)
ok github.com/camcamcami/BLK-System/internal/engine (cached)
ok github.com/camcamcami/BLK-System/internal/execguard (cached)
ok github.com/camcamcami/BLK-System/internal/gitguard (cached)
ok github.com/camcamcami/BLK-System/internal/pipe (cached)
ok github.com/camcamcami/BLK-System/internal/runtimeguard (cached)
ok github.com/camcamcami/BLK-System/internal/testutil (cached)
ok github.com/camcamcami/BLK-System/internal/validation (cached)

go vet ./...
PASS

git diff --check
PASS
```

## 7. Non-Authority Statement

BLK-SYSTEM-011.1 Task 1 hardens disabled transport metadata only. It does not authorize live BLK-test MCP, live MCP client/server startup, JSON-RPC/MCP handshake, fixed-tool execution, subprocess spawning as BLK-test behavior, network transport, source mutation, staging, commit, push, authoritative BEO publication, RTM generation, active BLK-req vault reads, approval-channel mechanics, or production sandbox/cgroup/VM/host-secret isolation.

## 8. Next Task

Task 2 — Add explicit no source-write, staging, commit, and push evidence fields.
