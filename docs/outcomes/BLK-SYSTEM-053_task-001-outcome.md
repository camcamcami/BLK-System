# BLK-SYSTEM-053 — Task 001 Outcome

**Status:** Complete — parameterized approval envelope implemented with TDD
**Date:** 2026-05-10T12:10:00+10:00
**Task:** Parameterized non-disposable L4 wrapper approvals without new runtime authority

---

## 1. Summary

Task 001 cleaned up the non-disposable L4 runtime wrapper by adding a typed `L4RuntimeApprovalEnvelope` that carries sprint, approval/run IDs, exact target/source/workspace paths, replay ledger path, nonce binding, and workspace marker filename.

The historical BLK-SYSTEM-051 default path remains supported for legacy callers and tests. Fresh synthetic envelopes can now use their own sprint nonce binding, marker name, workspace, and durable replay ledger without monkey-patching module globals or embedding BLK-SYSTEM-051 text.

No real non-disposable runtime pilot was executed.

---

## 2. Code Changes

Changed files:

```text
python/blk_test_non_disposable_l4_runtime_pilot.py
python/test_blk_test_non_disposable_l4_runtime_pilot.py
```

Implemented:

1. `L4RuntimeApprovalEnvelope` dataclass with fixed-tool and marker-name validation.
2. Optional `approval_envelope` parameter on `run_blk_test_non_disposable_l4_runtime_pilot`.
3. Envelope-bound exact path spelling checks.
4. Envelope-bound resolved path, expected HEAD, replay ledger, sprint, nonce, and workspace marker handling.
5. Legacy `_default_approval_envelope()` preserving BLK-SYSTEM-051 behavior.

---

## 3. RED/GREEN Evidence

RED was observed before implementation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  python.test_blk_test_non_disposable_l4_runtime_pilot.BlkTestNonDisposableL4RuntimePilotTest.test_parameterized_envelope_uses_its_own_sprint_nonce_marker_workspace_and_ledger \
  python.test_blk_test_non_disposable_l4_runtime_pilot.BlkTestNonDisposableL4RuntimePilotTest.test_parameterized_envelope_rejects_historical_nonce_laundering -q

FAILED (errors=2)
AttributeError: module 'blk_test_non_disposable_l4_runtime_pilot' has no attribute 'L4RuntimeApprovalEnvelope'
```

Additional hostile RED was observed before envelope validation hardening:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  python.test_blk_test_non_disposable_l4_runtime_pilot.BlkTestNonDisposableL4RuntimePilotTest.test_parameterized_envelope_rejects_tool_expansion_and_marker_path_escape -q

FAILED (failures=1)
AssertionError: ValueError not raised
```

GREEN after implementation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  python.test_blk_test_non_disposable_l4_runtime_pilot.BlkTestNonDisposableL4RuntimePilotTest.test_parameterized_envelope_rejects_tool_expansion_and_marker_path_escape -q
Ran 1 test in 0.014s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_test_non_disposable_l4_runtime_pilot -q
Ran 19 tests in 0.233s — OK
```

---

## 4. Authority Boundary

Task 001 is wrapper hardening only. It does not authorize production BLK-test MCP, generic BLK-test MCP, reusable BLK-test service startup, any new real non-disposable runtime run, arbitrary repositories, arbitrary shell, caller-supplied commands, dynamic tool expansion, source/Git mutation by BLK-test, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime RTM generation, RTM drift rejection, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, package-manager/network/model/browser/cyber tooling, live Codex execution, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.
