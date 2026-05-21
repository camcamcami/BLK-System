# BLK-128 — Verified-Loop BEO Publication Approval Request Contract

**Status:** Active component/authority contract
**Purpose:** Define the request-only package and refreshed challenge boundary for one verified-loop BEO publication path after BLK-SYSTEM-302..305 review evidence.
**Scope:** BLK-SYSTEM-306..309 request/contract/challenge/reconciliation plus BLK-SYSTEM-310..312 expired-attempt/refresh/reconciliation artifacts. This is not approval capture, run-ID authority, BEO closeout execution, BEO publication, RTM generation, production `blk-link`, protected-body access, runtime/tooling, or target/source/Git mutation.

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
NEXT_FRONTIER_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESHED_BOUND_APPROVE_REQUIRED_NOT_GRANTED
```

## 2. Required upstream evidence

The package must bind canonical BLK-SYSTEM-305 review evidence and reject self-consistent rehashes:

- `BLK_SYSTEM_305_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECONCILED`
- `BLK_SYSTEM_301_EXACT_BLK_TEST_ORACLE_VERIFICATION_RECONCILED`
- `BLK_SYSTEM_251_REUSABLE_BEO_PUBLICATION_RECONCILED_PER_RUN_EXACT_APPROVAL_READY`

The request may prepare a short `Approve` challenge artifact only when the request hash, nonce, operator identity, and request window are exact and hash-bound. That short reply is not approval in this package; a future capture/execution package must verify it.

## 3. Canonical package hashes

```text
blk306_approval_request_hash=sha256:becd296289dc4ba965a04e4e498202a9b6e708b0f697fcd3431049125985c939
blk307_approval_request_contract_hash=sha256:1a12d788d0032a44200b557d6cfa525e8d8e180ddda900d243f9faf9395f2ce0
blk308_approval_challenge_record_hash=sha256:931728d4fbb34f4310cae79ccd7c64462cc61b630d0c8409918c94955c5b0434
blk309_approval_request_reconciliation_hash=sha256:0f9c754a31db778ed2cf377d389da75459a81a4bd55626cfe8b82a2542ab1e83
blk310_expired_attempt_hash=sha256:40279079760ad5513de916b53bd306abd2ecf3cd7bae97d2b2e79e53c25ecc92
blk311_refresh_challenge_hash=sha256:778d72563994ca8e32ae23f947abbe29c60457f374e953195adc1a9fe5707af4
blk312_reconciliation_hash=sha256:ea1b859b7f13ea1ea55c254478e121d8f7969069e632134e6a2ddaff1ffd1a96
```

These hashes are part of the exact request boundary. BLK-SYSTEM-306..309 now represent the original request/challenge only, and BLK-SYSTEM-310..312 represent the refreshed challenge after expiry. Any later capture package must bind the refreshed `blk311_refresh_challenge_hash`, `blk310_expired_attempt_hash`, refresh nonce `BEO-APPROVAL-REFRESH-NONCE-BLK-SYSTEM-311-001`, operator identity, short `Approve` hash, and `2026-05-21T14:45:00+10:00`..`2026-05-21T20:45:00+10:00` window; it must not accept self-consistent alternate request IDs, alternate windows, alternate nonces, or regenerated hashes.

## 4. What this package may do

- Build an exact approval-request artifact over verified-loop BEO publication review evidence.
- Bind the exact Discord operator identity for a future decision.
- Bind a short `Approve` challenge hash and nonce for future capture.
- Record that the challenge artifact exists and is pending.
- Reconcile to the refreshed-bound-`Approve`-required frontier after expiry.
- If the original challenge expires, record the expired/unbound attempt and issue a refreshed short `Approve` challenge with exact hash and time-window binding.

## 5. Authority boundary

This package grants:

- no approval capture;
- no approval reuse;
- no generic `Approve` authority outside the exact challenge hash/nonce/window/operator binding;
- no run-ID reservation or consumption;
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
NEXT_FRONTIER_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESHED_BOUND_APPROVE_REQUIRED_NOT_GRANTED
```

That frontier may only proceed if the operator replies with short `Approve` bound to `blk311_refresh_challenge_hash=sha256:778d72563994ca8e32ae23f947abbe29c60457f374e953195adc1a9fe5707af4` during `2026-05-21T14:45:00+10:00`..`2026-05-21T20:45:00+10:00`. A later package must capture the exact decision and prove the bounded BEO publication execution path without granting reusable publication/signing/storage/ledger authority or RTM / production `blk-link` authority.
