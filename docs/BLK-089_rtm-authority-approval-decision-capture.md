# BLK-089 — RTM Authority Approval Decision Capture

## Active Boundary

Active RTM generation approval-decision boundary — exact approval capture only; not RTM generation execution.

## Status Markers

```text
RTM_GENERATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK088_REQUEST_NOT_GENERATED
APPROVED_FOR_ONE_FUTURE_LOCAL_RTM_GENERATION_PILOT_NOT_GENERATED
EXACT_LOCAL_RTM_GENERATION_PILOT_REQUIRED_NOT_RUN
```

## Fixture Binding

```text
approval_decision_package_id: RTM-GENERATION-APPROVAL-DECISION-089-001
approval_id: APPROVAL-BLK-SYSTEM-088-RTM-GENERATION-001
future_run_id: RUN-BLK-SYSTEM-088-RTM-GENERATION-001
upstream_authority_request_package_id: RTM-AUTHORITY-REQUEST-AFTER-BEO-PILOT-088-001
selected_frontier: rtm_generation_approval_decision_capture
decision_scope: RTM_GENERATION_APPROVAL_DECISION_ONLY_NOT_GENERATION
python/rtm_generation_approval_decision.py
```

## Proof Obligations

- BLK088_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND
- HUMAN_RTM_GENERATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_REQUEST
- APPROVAL_ID_RESERVED_FOR_BLK088_RTM_GENERATION
- FUTURE_RUN_ID_RESERVED_NOT_CONSUMED
- LOCAL_BEO_PILOT_EVIDENCE_INHERITED_BY_HASH_ONLY
- RTM_NOT_GENERATED_BY_APPROVAL_DECISION
- DRIFT_REJECTION_AND_DRIFT_DECISION_EXCLUDED
- ACTIVE_VAULT_AND_PROTECTED_BODY_ACCESS_EXCLUDED
- SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED
- TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED
- HOSTILE_REVIEW_REQUIRED_BEFORE_RTM_GENERATION_PILOT

## Authority Cutline

BLK-SYSTEM-089 records a scoped human decision for a future local RTM generation pilot. It does not run the pilot, does not emit an RTM ledger, does not reject drift, does not read protected bodies, does not perform active-vault hash comparison, does not publish externally, does not access signer key material, does not sign, does not write storage, does not append or mutate public ledgers, does not execute rollback/revocation/supersession, does not scan or mutate target repositories, does not authorize BEB dispatch or BEO closeout execution, does not run BLK-pipe/BLK-test/Codex, does not use package/network/model/browser/cyber tooling, and does not claim production isolation.

Persistent doctrine gate marker: BLK-SYSTEM-089 pins RTM approval capture as decision-only and not generation authority.
