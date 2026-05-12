# BLK-SYSTEM-091 Plan — RTM Drift-Rejection Authority Request

## Sprint Intent

Package the BLK-SYSTEM-090 local RTM generation pilot evidence into a deterministic request for future human review of RTM drift-rejection authority. This sprint is request-only: it does not approve, execute, or simulate drift rejection.

## Authority Surface

Authorized in this sprint:

- deterministic request package for future exact RTM drift-rejection authority review;
- hash binding to the BLK-SYSTEM-090 local RTM generation pilot package and its local RTM ledger hash;
- explicit denial of drift decision/execution until a later approval and execution sequence.

Not authorized in this sprint:

- drift rejection approval;
- drift rejection execution or drift decision;
- active-vault hash comparison, protected body reads, or protected body hashing;
- external ledger mutation, signer/storage/rollback side effects, or authoritative publication;
- target-repo scan or mutation;
- source/Git mutation by the fixture;
- BEB dispatch or BEO closeout execution;
- BLK-pipe, BLK-test, Codex, package/network/model/browser/cyber tooling;
- production sandbox or host-secret-isolation claims.

## Task Sequence

1. **Task 000 — Plan and scope**
   - Publish this plan and pin local RTM evidence vs drift authority request vs drift execution.

2. **Task 001 — Drift-rejection authority request RED/GREEN**
   - Add RED tests for exact BLK-SYSTEM-090 package binding, RTM ledger hash recomputation, request-only status, false side-effect flags, exact proof/denial sets, and hostile authority-laundering probes.
   - Implement `python/rtm_drift_rejection_authority_request.py` minimally to pass.

3. **Task 002 — Doctrine and gates**
   - Publish `docs/BLK-091_rtm-drift-rejection-authority-request.md`.
   - Update current-state executable/doc gates so BLK-SYSTEM-091 is visible as request-only evidence.

4. **Task 003 — Roadmap/current-state alignment**
   - Update BLK-077/BLK-079 to record BLK-SYSTEM-091 completion and preserve that drift approval/execution require future exact decisions.

5. **Task 004 — Hostile review and remediation**
   - Review for request-as-approval laundering, drift execution wording, protected-body read claims, external ledger claims, and stale next-frontier wording.

6. **Task 005 — Verification and closeout**
   - Run focused tests, full Python suite, Go checks where applicable, and `git diff --check`.
   - Publish task outcomes and sprint closeout.

## Expected Status Markers

```text
RTM_DRIFT_REJECTION_AUTHORITY_REQUEST_READY_AFTER_LOCAL_RTM_GENERATION_NOT_GRANTED
DRIFT_REJECTION_REQUEST_ONLY_NOT_GRANTED
EXPLICIT_HUMAN_RTM_DRIFT_REJECTION_APPROVAL_REQUIRED_NOT_GRANTED
```
