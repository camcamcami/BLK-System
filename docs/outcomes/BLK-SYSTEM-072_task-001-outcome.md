# BLK-SYSTEM-072 Task 001 Outcome — Exact-Target Approval-Envelope Fixture

**Status:** Complete
**Date:** 2026-05-11T11:58:00+10:00
**Task:** Task 001 — Exact-target approval-envelope fixture, RED/GREEN

---

## Summary

Implemented `python/blk_test_kuronode_workspace_exact_target_approval_envelope.py` with tests in `python/test_blk_test_kuronode_workspace_exact_target_approval_envelope.py`.

The fixture validates a review-only exact-target approval envelope for a future BLK-test functional-module pilot over Kuronode. It does not approve runtime and does not execute BLK-test runtime.

---

## RED Evidence

Initial RED was observed before implementation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_kuronode_workspace_exact_target_approval_envelope -q
ModuleNotFoundError: No module named 'blk_test_kuronode_workspace_exact_target_approval_envelope'
FAILED (errors=1)
```

Additional hostile RED cases were added and observed after the first GREEN pass:

```text
FAIL: test_upstream_request_schema_is_closed_even_when_attacker_recomputes_hash
AssertionError: ValueError not raised

FAIL: test_timestamps_are_timezone_aware_ordered_and_within_review_ttl
AssertionError: ValueError not raised

Ran 8 tests in 0.019s
FAILED (failures=2)
```

---

## GREEN Implementation

The fixture now enforces:

- exact upstream BLK-SYSTEM-071 request-ready status;
- closed upstream request schema before accepting a recomputed hash;
- canonical upstream request hash recomputation;
- exact Kuronode target path, branch, HEAD, workspace status, fixed tool, and BLK-test role statement;
- exact review-only approval envelope schema;
- fresh BLK-SYSTEM-072 approval/run IDs;
- timezone-aware ordered timestamps and a bounded four-hour review TTL;
- exact timeout/output profile;
- exact replay policy;
- exact proof marker set;
- exact denied-authority set;
- exact no-side-effect false flag set;
- recursive authority/secret/tooling/mutation/protected-path laundering rejection for valid string surfaces.

---

## Verification

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_kuronode_workspace_exact_target_approval_envelope -q
----------------------------------------------------------------------
Ran 8 tests in 0.021s

OK
```

---

## Non-Execution Statement

Task 001 did not run BLK-test runtime against Kuronode, did not start BLK-test MCP, did not run Electron/smoke/TypeScript/package-manager tooling, did not invoke Codex, did not invoke BLK-pipe, did not mutate Kuronode source or Git state, did not push Kuronode, did not read protected BLK-req bodies, did not publish BEOs, and did not generate RTM.
