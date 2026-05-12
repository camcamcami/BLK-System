# BLK-SYSTEM-089 Plan — RTM Authority Approval Decision Capture

## Sprint Intent

Capture the exact human RTM generation approval decision for the completed BLK-SYSTEM-088 request package without generating an RTM, rejecting drift, reading protected bodies, mutating ledgers, or inheriting adjacent authority.

## Authority Surface

Authorized in this sprint:

- deterministic local fixture capture of one human approval decision for the exact BLK-SYSTEM-088 RTM authority request package;
- reservation of one future local RTM generation pilot run ID;
- hash binding to the BLK-SYSTEM-088 request package and its upstream BLK-SYSTEM-087 local BEO publication-pilot evidence.

Not authorized in this sprint:

- RTM generation;
- RTM drift rejection or drift decision;
- active-vault hash comparison or protected BLK-req body reads;
- authoritative external BEO publication;
- signer key-material access, cryptographic signing, immutable storage writes, public ledger mutation, rollback, revocation, or supersession execution;
- target-repo scan or mutation;
- source/Git mutation by the fixture;
- BEB dispatch or BEO closeout execution;
- BLK-pipe, BLK-test, or Codex runtime;
- package/network/model/browser/cyber tooling;
- production sandbox or host-secret-isolation claims.

## Task Sequence

1. **Task 000 — Plan and scope**
   - Publish this plan.
   - Pin the request-vs-decision-vs-generation cutline.

2. **Task 001 — Approval-decision fixture RED/GREEN**
   - Add RED tests for exact BLK-SYSTEM-088 package binding, package hash recomputation, approval ID/run ID reservation, timestamp windows, replay/stale/expired rejection, exact denied-authority sets, and normalized authority-laundering probes.
   - Implement `python/rtm_generation_approval_decision.py` minimally to pass.

3. **Task 002 — Doctrine and gates**
   - Publish `docs/BLK-089_rtm-authority-approval-decision-capture.md`.
   - Update current-state executable/doc gates so BLK-SYSTEM-089 is visible without implying generation.

4. **Task 003 — Roadmap/current-state alignment**
   - Update BLK-077 and BLK-079 to record BLK-SYSTEM-089 complete and make BLK-SYSTEM-090 the next exact local pilot only.

5. **Task 004 — Hostile review and remediation**
   - Run hostile review focused on approval laundering, generation laundering, drift rejection leakage, protected-body reads, and stale roadmap wording.

6. **Task 005 — Verification and closeout**
   - Run focused tests, full Python suite, Go checks where applicable, and `git diff --check`.
   - Publish task outcomes and sprint closeout.

## Expected Status Markers

```text
RTM_GENERATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK088_REQUEST_NOT_GENERATED
APPROVED_FOR_ONE_FUTURE_LOCAL_RTM_GENERATION_PILOT_NOT_GENERATED
EXACT_LOCAL_RTM_GENERATION_PILOT_REQUIRED_NOT_RUN
```
