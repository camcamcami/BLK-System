# BLK-SYSTEM-013 Task 004 Outcome — Replay and Audit Gates

**Sprint:** `BLK-SYSTEM-013` — Approval-channel and Source-Evidence Authorization Mechanics
**Task:** Task 4 — Expiry, replay, and deterministic audit hashes
**Status:** COMPLETE

---

## Summary

Added expiry/replay gates and deterministic audit hashes for Sprint 013 BLK-test approval validation evidence.

Implementation commit pushed to `origin/main`:

```text
67a8479 feat: add blk-test approval replay and audit gates
```

Touched implementation paths:

```text
python/blk_test_mcp_approval_authorization.py
python/test_blk_test_mcp_approval_authorization.py
```

---

## RED/GREEN Evidence

RED was observed after adding replay/audit tests and before implementation:

```text
FAILED (failures=3, errors=2)
KeyError: 'approval_record_hash'
AssertionError: ValueError not raised
```

GREEN verification after implementation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_mcp_approval_authorization
.........................
----------------------------------------------------------------------
Ran 25 tests in 0.003s

OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s python -p 'test_blk_test_mcp_approval_authorization.py'
.........................
----------------------------------------------------------------------
Ran 25 tests in 0.004s

OK

git diff --check: PASS
```

---

## Implemented Behavior

- Expired approvals reject.
- Replayed `approval_id` values reject via caller-supplied used-ID state.
- Malformed UTC timestamps reject.
- Missing `expires_at` rejects.
- `approval_record_hash`, `source_evidence_hash`, and `authorization_request_hash` are stable `sha256:<64-lowercase-hex>` values using canonical JSON.
- Source evidence hash changes when source evidence changes.
- Returned audit evidence omits raw secret/protected-vault body text.

---

## Authority Boundary

This task implemented local replay/audit evidence only. It does not authorize live BLK-test MCP, does not authorize live MCP client/server startup, does not execute fixed-tool tests, does not mutate primary repo as BLK-test behavior, does not authorize authoritative BEO publication, does not authorize RTM generation, and does not read protected BLK-req vault bodies.

Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke.
