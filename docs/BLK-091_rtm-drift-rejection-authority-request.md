# BLK-091 — RTM Drift-Rejection Authority Request

## Active Boundary

Active RTM drift-rejection authority request boundary — review package only; not drift rejection approval or execution.

## Status Markers

```text
RTM_DRIFT_REJECTION_AUTHORITY_REQUEST_READY_AFTER_LOCAL_RTM_GENERATION_NOT_GRANTED
DRIFT_REJECTION_REQUEST_ONLY_NOT_GRANTED
EXPLICIT_HUMAN_RTM_DRIFT_REJECTION_APPROVAL_REQUIRED_NOT_GRANTED
```

## Fixture Binding

```text
authority_request_package_id: RTM-DRIFT-REJECTION-AUTHORITY-REQUEST-091-001
upstream_rtm_generation_package_id: RTM-GENERATION-PILOT-EXECUTION-090-001
rtm_id: RTM-090-001
selected_frontier: rtm_drift_rejection_authority_request
request_scope: RTM_DRIFT_REJECTION_AUTHORITY_REQUEST_REVIEW_ONLY
python/rtm_drift_rejection_authority_request.py
```

## Proof Obligations

- BLK090_LOCAL_RTM_GENERATION_PACKAGE_IDENTITY_AND_HASH_BOUND
- LOCAL_RTM_LEDGER_IDENTITY_AND_HASH_BOUND
- BEO_AND_TARGET_HASH_EVIDENCE_BOUND
- DRIFT_REJECTION_REQUESTED_FOR_REVIEW_NOT_GRANTED
- NO_DRIFT_REJECTION_OR_DRIFT_DECISION_PERFORMED
- PROTECTED_BODY_NO_READ_OR_HASH_GUARANTEE_BOUND
- EXTERNAL_LEDGER_SIGNER_STORAGE_NO_SIDE_EFFECTS_CONFIRMED
- TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED
- HOSTILE_REVIEW_REQUIRED_BEFORE_ANY_DRIFT_APPROVAL

## Authority Cutline

BLK-SYSTEM-091 packages BLK-SYSTEM-090 local RTM generation evidence into a future human-review request. It grants no drift rejection approval, no drift rejection execution, no drift decision, no active-vault hash comparison, no protected-body reads or protected-body hashing, no external ledger mutation, no signer/storage/rollback side effects, no authoritative publication, no target-repo scan or mutation, no source/Git mutation by the fixture, no BEB dispatch or BEO closeout execution, no BLK-pipe/BLK-test/Codex runtime, no package/network/model/browser/cyber tooling, and no production isolation claim.

Persistent doctrine gate marker: BLK-SYSTEM-091 pins RTM drift rejection as request-only and not approval or execution authority.
