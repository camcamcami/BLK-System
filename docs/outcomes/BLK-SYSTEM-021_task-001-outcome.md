# BLK-SYSTEM-021 — Task 001 Outcome

**Status:** Complete — RED gates added
**Date:** 2026-05-07T21:08:07+10:00
**Plan:** `docs/plans/blk-system-021_python-adapter-policy-layer-hardening.md`

---

## 1. Summary

Task 001 added failing Python adapter policy preflight gates to `python/test_blk_pipe_adapter.py`.

The RED tests prove the adapter does not yet consistently reject malformed execute payload shapes before invoking the fake `blk-pipe` binary. Existing behavior already rejects mixed `validation_profiles` plus `validation_commands` and invalid `validation_commands`, but the new policy layer is still missing for trace metadata, critical fields, non-absolute work directories, validation profile hygiene, and protected BLK-req allowlist paths.

---

## 2. Files Changed

```text
python/test_blk_pipe_adapter.py
docs/outcomes/BLK-SYSTEM-021_task-001-outcome.md
```

---

## 3. RED Evidence

Command:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_pipe_adapter -v
```

Observed result:

```text
Ran 30 tests in 0.879s
FAILED (failures=23)
```

Representative failing behaviors:

```text
AssertionError: ValueError not raised
- test_execute_sprint_rejects_missing_or_empty_trace_artifacts_before_invocation
- test_execute_sprint_rejects_malformed_trace_artifacts_before_invocation
- test_execute_sprint_rejects_non_absolute_work_dir_before_invocation
- test_execute_sprint_rejects_empty_execute_fields_before_invocation
- test_execute_sprint_rejects_invalid_validation_profiles_before_invocation
- test_execute_sprint_rejects_protected_blk_req_allowlist_paths_before_invocation
```

Passing control checks included:

```text
test_execute_sprint_rejects_mixed_validation_profiles_and_commands ... ok
test_execute_sprint_rejects_invalid_validation_commands_before_invocation ... ok
test_execute_sprint_preserves_non_empty_trusted_local_validation_commands ... ok
```

---

## 4. Non-Execution Statement

Task 001 did not invoke Hindsight, Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads/copying/parsing/hashing/mutation, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, or source mutation outside exact approved allowlists.

---

## 5. No-Authority-Expansion Statement

The task adds RED tests only. It does not grant runtime authority and does not make Python the final enforcement authority. Task 002 owns the minimal adapter preflight implementation while preserving Go `blk-pipe` as the final authority.
