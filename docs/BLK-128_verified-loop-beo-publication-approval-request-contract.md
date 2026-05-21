# BLK-128 — Verified-Loop BEO Publication Approval Request Contract

**Status:** Active component/authority contract
**Purpose:** Define the request-only, historical challenge, live non-approval guard, and BLK-SYSTEM-316 standing-development approval boundary for one verified-loop BEO publication path after BLK-SYSTEM-302..305 review evidence.
**Scope:** BLK-SYSTEM-306..309 request/contract/challenge/reconciliation, BLK-SYSTEM-310..312 expired-attempt/refresh/reconciliation, BLK-SYSTEM-313..315 live generic-directive guard artifacts, and BLK-SYSTEM-316 standing BLK-System development approval. This is not reusable approval, reusable run-ID authority, reusable BEO closeout execution, reusable BEO publication, RTM generation, production `blk-link`, protected-body access, runtime/tooling, Kuronode mutation, or target/source/Git mutation outside exact BLK-System sprint discipline.

---

## 1. Contract markers

```text
BLK_SYSTEM_306_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_READY
BLK_SYSTEM_307_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_CONTRACT_READY
BLK_SYSTEM_308_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CHALLENGE_RECORDED
BLK_SYSTEM_309_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_RECONCILED
historical_frontier=NEXT_FRONTIER_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CAPTURE_AND_BOUNDED_EXECUTION_REQUIRED_NOT_GRANTED
BLK_SYSTEM_310_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CHALLENGE_EXPIRED_ATTEMPT_RECORDED
BLK_SYSTEM_311_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESH_APPROVE_CHALLENGE_READY
BLK_SYSTEM_312_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESH_CHALLENGE_RECONCILED
BLK_SYSTEM_313_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_LIVE_REFRESH_GENERIC_DIRECTIVE_RECORDED
BLK_SYSTEM_314_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_SHORT_APPROVE_GUARD_READY
BLK_SYSTEM_315_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_LIVE_REFRESH_NON_APPROVAL_RECONCILED
BLK_SYSTEM_316_STANDING_BLK_SYSTEM_DEVELOPMENT_APPROVAL_RECORDED
NEXT_FRONTIER_BLK_SYSTEM_STANDING_DEVELOPMENT_APPROVAL_ACTIVE_NO_TIME_CLOCK
```

## 2. Required upstream evidence

The package must bind canonical BLK-SYSTEM-305 review evidence and reject self-consistent rehashes:

- `BLK_SYSTEM_305_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECONCILED`
- `BLK_SYSTEM_301_EXACT_BLK_TEST_ORACLE_VERIFICATION_RECONCILED`
- `BLK_SYSTEM_251_REUSABLE_BEO_PUBLICATION_RECONCILED_PER_RUN_EXACT_APPROVAL_READY`

BLK-SYSTEM-306..315 prepared and guarded the historical short `Approve` challenge path. BLK-SYSTEM-316 supersedes that active UX for BLK-System development: repository development no longer depends on an expiring challenge clock. The standing development approval hash is not itself BEO publication, run-ID, signer/storage/ledger, RTM, or production `blk-link` authority.

## 3. Canonical package hashes

```text
blk306_approval_request_hash=sha256:becd296289dc4ba965a04e4e498202a9b6e708b0f697fcd3431049125985c939
blk307_approval_request_contract_hash=sha256:1a12d788d0032a44200b557d6cfa525e8d8e180ddda900d243f9faf9395f2ce0
blk308_approval_challenge_record_hash=sha256:931728d4fbb34f4310cae79ccd7c64462cc61b630d0c8409918c94955c5b0434
blk309_approval_request_reconciliation_hash=sha256:0f9c754a31db778ed2cf377d389da75459a81a4bd55626cfe8b82a2542ab1e83
blk310_expired_attempt_hash=sha256:40279079760ad5513de916b53bd306abd2ecf3cd7bae97d2b2e79e53c25ecc92
blk311_refresh_challenge_hash=sha256:778d72563994ca8e32ae23f947abbe29c60457f374e953195adc1a9fe5707af4
blk312_reconciliation_hash=sha256:ea1b859b7f13ea1ea55c254478e121d8f7969069e632134e6a2ddaff1ffd1a96
blk313_live_directive_hash=sha256:cbb7e08f7706289f353302d97a13578f9e05ae5628ce74d8242d4eb14bced942
blk314_short_approve_guard_hash=sha256:d4738258e0e9580144f3254f915ff799165169ac781de21eec6e960848b49101
blk315_reconciliation_hash=sha256:a120abbca3e6226d27bc26241234fc811a880c568d51456343183370237a243c
blk316_standing_development_approval_hash=sha256:87e904afb73319fc0c0dd73ea914f428afdc9c3e035642ae0f2af55ed51782f5
```

These hashes are part of the exact request boundary. BLK-SYSTEM-306..315 remain historical clock/challenge evidence. BLK-SYSTEM-316 is now the active no-clock BLK-System development approval record. Any later package that references BLK-SYSTEM-316 must bind `blk316_standing_development_approval_hash`, the exact operator identity, and the verified-loop evidence chain; it must not accept self-consistent alternate request IDs, alternate nonces, generic directives, or regenerated hashes. BEO publication side effects require a separate exact no-clock side-effect decision.

## 4. What this package may do

- Build an exact approval-request artifact over verified-loop BEO publication review evidence.
- Bind the exact Discord operator identity for a future decision.
- Preserve historical short `Approve` challenge evidence as fail-closed context.
- Record standing BLK-System development approval without an expiring clock.
- Reconcile to the no-clock standing BLK-System development frontier.
- Require a separate exact no-clock side-effect decision before any run-ID movement or publication finality attempt.

## 5. Authority boundary

This package grants:

- no approval capture by this contract;
- no reusable approval;
- no generic `Approve` clock/challenge requirement for BLK-System development after BLK-SYSTEM-316;
- no run-ID reservation or consumption in this contract;
- no BEO closeout execution;
- no BEO publication;
- no signer reuse, key-material access, or signature generation;
- no storage reuse or immutable-storage write;
- no ledger reuse or public-ledger append;
- no rollback, revocation, or supersession execution;
- no RTM generation;
- no production `blk-link`;
- no drift rejection;
- no coverage truth;
- no protected-body access;
- no BLK-pipe, BLK-test, Codex, package/network/model/browser/cyber runtime/tooling;
- no production-isolation claim;
- no target/source/Git mutation.

## 6. Next frontier

The next frontier is:

```text
NEXT_FRONTIER_BLK_SYSTEM_STANDING_DEVELOPMENT_APPROVAL_ACTIVE_NO_TIME_CLOCK
```

That frontier means BLK-System repository development may proceed without waiting for an expiring short-reply clock. A later BEO side-effect package must capture a separate exact no-clock decision and prove the bounded BEO publication execution path without granting reusable publication/signing/storage/ledger authority or RTM / production `blk-link` authority.
