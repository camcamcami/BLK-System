# BLK-093 — RTM Drift-Rejection Approval Decision Capture

## Active Boundary

Active RTM drift-rejection approval-decision boundary — exact approval capture only; not drift-rejection execution and not a drift decision.

## Status Markers

```text
RTM_DRIFT_REJECTION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK091_REQUEST_NOT_EXECUTED
APPROVED_FOR_ONE_FUTURE_LOCAL_RTM_DRIFT_REJECTION_EXECUTION_NOT_EXECUTED
EXACT_LOCAL_RTM_DRIFT_REJECTION_EXECUTION_REQUIRED_NOT_RUN
BLK_SYSTEM_093_GRANTS_NO_RTM_DRIFT_REJECTION_EXECUTION
```

## Fixture Binding

```text
approval_decision_package_id: RTM-DRIFT-REJECTION-APPROVAL-DECISION-093-001
approval_id: APPROVAL-BLK-SYSTEM-091-RTM-DRIFT-REJECTION-001
future_run_id: RUN-BLK-SYSTEM-091-RTM-DRIFT-REJECTION-001
upstream_authority_request_package_id: RTM-DRIFT-REJECTION-AUTHORITY-REQUEST-091-001
selected_frontier: rtm_drift_rejection_approval_decision_capture
decision_scope: RTM_DRIFT_REJECTION_APPROVAL_DECISION_ONLY_NOT_EXECUTION
python/rtm_drift_rejection_approval_decision.py
```

## Proof Obligations

- BLK091_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND
- HUMAN_RTM_DRIFT_REJECTION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_REQUEST
- APPROVAL_ID_RESERVED_FOR_BLK091_RTM_DRIFT_REJECTION
- FUTURE_RUN_ID_RESERVED_NOT_CONSUMED
- LOCAL_RTM_LEDGER_EVIDENCE_INHERITED_BY_HASH_ONLY
- DRIFT_REJECTION_NOT_EXECUTED_BY_APPROVAL_DECISION
- DRIFT_DECISION_NOT_MADE_BY_APPROVAL_DECISION
- ACTIVE_VAULT_AND_PROTECTED_BODY_ACCESS_EXCLUDED
- SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED
- TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED
- HOSTILE_REVIEW_REQUIRED_BEFORE_RTM_DRIFT_REJECTION_EXECUTION

## Authority Cutline

BLK-SYSTEM-093 records a scoped human decision for one future local RTM drift-rejection execution sprint. It does not execute RTM drift rejection, does not make a drift decision, does not perform active-vault hash comparison, performs no protected-body reads or hashing, does not publish externally, accesses no signer key material, performs no signing, writes no immutable storage, mutates no public ledger, performs no rollback/revocation/supersession, scans or mutates no target repository, mutates no source or Git state by fixture, dispatches no BEB, executes no BEO closeout, runs no BLK-pipe/BLK-test/Codex runtime, uses no package/network/model/browser/cyber tooling, and claims no production isolation.

Persistent doctrine gate marker: BLK-SYSTEM-093 pins RTM drift-rejection approval capture as decision-only and not execution authority.
