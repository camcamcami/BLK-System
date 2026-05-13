# BLK-095 — Exact Local RTM Drift-Rejection Execution

## Active Boundary

Active exact local RTM drift-rejection execution boundary — one local fixture execution bound to the BLK-SYSTEM-093 approval-decision package. It is not reusable/runtime RTM drift-rejection authority, not authoritative drift truth, and not runtime `blk-link` trace closure.

## Status Markers

```text
LOCAL_RTM_DRIFT_REJECTION_EXECUTED_FOR_EXACT_BLK093_APPROVAL
PILOT_LOCAL_RTM_DRIFT_REJECTION_RECORDED_NOT_AUTHORITATIVE
AUTHORITATIVE_DRIFT_DECISION_NOT_MADE
NO_RUNTIME_BLK_LINK_TRACE_CLOSURE_BY_BLK_SYSTEM_095
POST_LOCAL_RTM_DRIFT_REJECTION_RECONCILIATION_REQUIRED_NOT_RUNTIME_BLK_LINK
```

## Fixture Binding

```text
execution_package_id: RTM-DRIFT-REJECTION-EXECUTION-095-001
approval_decision_package_id: RTM-DRIFT-REJECTION-APPROVAL-DECISION-093-001
approval_id: APPROVAL-BLK-SYSTEM-091-RTM-DRIFT-REJECTION-001
run_id_consumed: RUN-BLK-SYSTEM-091-RTM-DRIFT-REJECTION-001
drift_rejection_id: LOCAL-RTM-DRIFT-REJECTION-095-001
selected_frontier: exact_local_rtm_drift_rejection_execution
execution_scope: EXACT_LOCAL_RTM_DRIFT_REJECTION_EXECUTION_LOCAL_ONLY
python/exact_local_rtm_drift_rejection_execution.py
```

## Proof Obligations

- BLK093_APPROVAL_DECISION_IDENTITY_AND_HASH_BOUND
- APPROVAL_INTERVAL_BOUND_TO_EXECUTION_WINDOW
- RUN_ID_CONSUMED_EXACTLY_ONCE_IN_LOCAL_FIXTURE
- LOCAL_RTM_LEDGER_INPUT_HASH_BOUND
- LOCAL_RTM_DRIFT_REJECTION_RECORDED_NOT_AUTHORITATIVE
- AUTHORITATIVE_DRIFT_DECISION_NOT_MADE
- RUNTIME_BLK_LINK_TRACE_CLOSURE_EXCLUDED
- ACTIVE_VAULT_AND_PROTECTED_BODY_ACCESS_EXCLUDED
- SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED
- TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED
- POST_LOCAL_EXECUTION_RECONCILIATION_REQUIRED

## Output Meaning

BLK-SYSTEM-095 records a local drift-rejection execution artifact for the non-authoritative local pilot ladder. The emitted result is:

```text
PILOT_LOCAL_RTM_DRIFT_REJECTION_RECORDED_NOT_AUTHORITATIVE
```

That result means the BLK-SYSTEM-093 future run ID was consumed in a deterministic local fixture and a hash-bound local drift-rejection record was emitted. It does not mean that active-vault hashes were compared, protected bodies were read, an external ledger was mutated, a runtime `blk-link` trace closure occurred, or an authoritative drift decision was made.

## Authority Cutline

BLK-SYSTEM-095 may only consume `RUN-BLK-SYSTEM-091-RTM-DRIFT-REJECTION-001` against `RTM-DRIFT-REJECTION-APPROVAL-DECISION-093-001` and emit local evidence. It grants no reusable/runtime RTM drift-rejection grant, no authoritative drift decision, no runtime `blk-link` trace closure, no active-vault hash comparison, no protected-body reads or hashing, no external ledger mutation, no external authoritative publication, no signer/storage/rollback side effects, no target-repo scan or mutation, no source/Git mutation by fixture, no BEB dispatch, no BEO closeout execution, no BLK-pipe/BLK-test/Codex runtime, no package/network/model/browser/cyber tooling, and no production isolation claim.

Persistent doctrine gate marker: BLK-SYSTEM-095 pins exact local RTM drift-rejection execution as local non-authoritative evidence and not runtime `blk-link` authority.
