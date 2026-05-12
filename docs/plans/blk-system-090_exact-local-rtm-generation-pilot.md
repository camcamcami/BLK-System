# BLK-SYSTEM-090 Plan — Exact Local RTM Generation Pilot

## Sprint Intent

Consume the BLK-SYSTEM-089 exact RTM generation approval decision and execute one deterministic local RTM generation pilot. The pilot produces local hash-bound RTM evidence only; it does not reject drift, read protected bodies, perform active-vault body/hash comparison, publish externally, mutate ledgers, or grant downstream drift authority.

## Authority Surface

Authorized in this sprint:

- one local deterministic RTM generation pilot bound to `RTM-GENERATION-APPROVAL-DECISION-089-001`;
- consumption of `RUN-BLK-SYSTEM-088-RTM-GENERATION-001` exactly once in the returned fixture;
- hash-only binding to the BLK-SYSTEM-087 local BEO publication-pilot artifact carried through BLK-SYSTEM-088/089.

Not authorized in this sprint:

- RTM drift rejection or any drift decision;
- protected BLK-req body reads or active-vault body scanning;
- authoritative external BEO publication;
- cryptographic signing, signer key-material access, immutable storage write, public ledger append/mutation, rollback, revocation, or supersession execution;
- target-repo scan or mutation;
- source/Git mutation by the fixture;
- BEB dispatch or BEO closeout execution;
- BLK-pipe, BLK-test, Codex, package/network/model/browser/cyber tooling;
- production sandbox or host-secret-isolation claims.

## Task Sequence

1. **Task 000 — Plan and scope**
   - Publish this plan and pin approval-capture vs local-generation vs drift-rejection boundaries.

2. **Task 001 — Local RTM generation fixture RED/GREEN**
   - Add RED tests for exact BLK-SYSTEM-089 approval binding, approval interval/run ID consumption, deterministic RTM hash, deep-copy behavior, and denial of drift/protected/external side effects.
   - Implement `python/exact_local_rtm_generation_pilot.py` minimally to pass.

3. **Task 002 — Doctrine and gates**
   - Publish `docs/BLK-090_exact-local-rtm-generation-pilot.md`.
   - Update current-state executable/doc gates so BLK-SYSTEM-090 is visible as local generation evidence only.

4. **Task 003 — Roadmap/current-state alignment**
   - Update BLK-077/BLK-079 to record BLK-SYSTEM-090 completion and move the next frontier to a drift-rejection authority request only.

5. **Task 004 — Hostile review and remediation**
   - Review for drift-rejection laundering, coverage-claim laundering, protected-body reads, false external ledger claims, and stale next-frontier text.

6. **Task 005 — Verification and closeout**
   - Run focused tests, full Python suite, Go checks where applicable, and `git diff --check`.
   - Publish task outcomes and sprint closeout.

## Expected Status Markers

```text
LOCAL_RTM_GENERATION_PILOT_EXECUTED_FOR_EXACT_BLK089_APPROVAL
PILOT_LOCAL_RTM_LEDGER_GENERATED_NOT_AUTHORITATIVE
RTM_DRIFT_REJECTION_AUTHORITY_REQUEST_REQUIRED_NOT_GRANTED
```
