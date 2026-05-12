# BLK-090 — Exact Local RTM Generation Pilot

## Active Boundary

Active exact local RTM generation pilot boundary — local deterministic RTM ledger evidence only; not drift rejection authority.

## Status Markers

```text
LOCAL_RTM_GENERATION_PILOT_EXECUTED_FOR_EXACT_BLK089_APPROVAL
PILOT_LOCAL_RTM_LEDGER_GENERATED_NOT_AUTHORITATIVE
RTM_DRIFT_REJECTION_AUTHORITY_REQUEST_REQUIRED_NOT_GRANTED
```

## Fixture Binding

```text
execution_package_id: RTM-GENERATION-PILOT-EXECUTION-090-001
approval_decision_package_id: RTM-GENERATION-APPROVAL-DECISION-089-001
approval_id: APPROVAL-BLK-SYSTEM-088-RTM-GENERATION-001
run_id_consumed: RUN-BLK-SYSTEM-088-RTM-GENERATION-001
rtm_id: RTM-090-001
selected_frontier: exact_local_rtm_generation_pilot
execution_scope: EXACT_LOCAL_RTM_GENERATION_PILOT_ONLY
python/exact_local_rtm_generation_pilot.py
```

## Proof Obligations

- BLK089_APPROVAL_DECISION_IDENTITY_AND_HASH_BOUND
- APPROVAL_INTERVAL_BOUND_TO_EXECUTION_WINDOW
- RUN_ID_CONSUMED_EXACTLY_ONCE_IN_LOCAL_FIXTURE
- LOCAL_RTM_LEDGER_HASH_BOUND
- BEO_AND_TRACE_HASH_EVIDENCE_BOUND
- PROTECTED_BODY_NO_READ_GUARANTEE_BOUND
- DRIFT_REJECTION_AND_DRIFT_DECISION_EXCLUDED
- SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED
- TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED
- FUTURE_DRIFT_REJECTION_AUTHORITY_REQUEST_REQUIRED

## Authority Cutline

BLK-SYSTEM-090 consumes the exact BLK-SYSTEM-089 future run ID once and emits `PILOT_LOCAL_RTM_LEDGER_GENERATED_NOT_AUTHORITATIVE` as local deterministic evidence. It grants no RTM drift rejection, no drift decision, no protected-body reads, no active-vault body scan, no external authoritative publication, no signer/storage/ledger/rollback side effects, no target-repo scan or mutation, no source/Git mutation by the fixture, no BEB dispatch or BEO closeout execution, no BLK-pipe/BLK-test/Codex runtime, no package/network/model/browser/cyber tooling, and no production isolation claim.

Persistent doctrine gate marker: BLK-SYSTEM-090 pins local RTM generation as exact local evidence only and not drift rejection authority.
