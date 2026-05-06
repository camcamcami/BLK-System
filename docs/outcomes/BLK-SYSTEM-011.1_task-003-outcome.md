# BLK-SYSTEM-011.1 — Task 3 Outcome

**Status:** Complete
**Date:** 2026-05-06
**Task:** Replace brittle live-surface source scan with AST-aware gate
**Implementation Commit:** pending before commit
**Remote:** pending push

---

## 1. Objective

Prove the disabled transport module has no live execution imports/calls while preserving required public evidence vocabulary such as `subprocess_called`.

## 2. Files Added/Changed

- `python/test_blk_test_mcp_disabled_transport.py`
- `docs/outcomes/BLK-SYSTEM-011.1_task-003-outcome.md`

## 3. Behavior Implemented

- Added `_assert_disabled_transport_source_has_no_live_surfaces(...)` as an AST-aware test helper.
- The helper rejects live imports such as `subprocess`, `socket`, `requests`, `http.server`, `urllib`, and `asyncio`.
- The helper rejects live calls such as `os.system(...)`, `eval(...)`, `exec(...)`, `__import__(...)`, `subprocess.Popen(...)`, and `*.run_command(...)`.
- The helper rejects forbidden literal capability markers such as `shell=True`, `publish_beo`, `generate_rtm`, and `read_active_vault`.
- The helper allows required public evidence vocabulary such as `subprocess_called`.
- The actual module source gate now uses the AST-aware helper instead of a brittle broad `subprocess` substring ban.

## 4. TDD Evidence

### 4.1 RED

```text
PYTHONPATH=python python3 -m unittest \
  python.test_blk_test_mcp_disabled_transport.DisabledTransportStartupTest.test_live_surface_source_scan_rejects_ast_imports_and_calls_but_allows_public_evidence_keys -v

FAILED (errors=1)
NameError: name '_assert_disabled_transport_source_has_no_live_surfaces' is not defined
```

### 4.2 GREEN

```text
PYTHONPATH=python python3 -m unittest python.test_blk_test_mcp_disabled_transport.DisabledTransportStartupTest -v
Ran 18 tests in 0.002s
OK
```

## 5. Review Results

Deterministic local review:

- Synthetic positive and negative cases prove the source scanner itself rejects live surfaces and preserves `subprocess_called` evidence vocabulary.
- The actual disabled transport module remains dependency-free and does not import or call live execution surfaces.
- No production behavior changed in this task.

## 6. Final Verification

```text
python3 -m unittest discover -s python -p 'test_*.py'
Ran 224 tests in 5.194s
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

BLK-SYSTEM-011.1 Task 3 hardens test review gates only. It does not authorize live BLK-test MCP, live MCP client/server startup, JSON-RPC/MCP handshake, fixed-tool execution, subprocess spawning as BLK-test behavior, network transport, source mutation, staging, commit, push, authoritative BEO publication, RTM generation, active BLK-req vault reads, approval-channel mechanics, or production sandbox/cgroup/VM/host-secret isolation.

## 8. Next Task

Task 4 — Patch BLK-017 active doctrine with 011.1 hardening markers.
