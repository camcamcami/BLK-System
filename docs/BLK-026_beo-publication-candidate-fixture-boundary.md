# BLK-026 — BEO Publication Candidate Fixture Boundary

**Status:** Active fixture boundary contract — not publication authority  
**Scope:** BLK-SYSTEM-023 BEO publication candidate fixture bridge; deterministic local candidate fixtures only, with no authoritative BEO publication, no runtime `PUBLISHED` BEO output, no RTM generation, no signer/storage/ledger/rollback side effects, and no protected-vault body reads.

---

## 1. Purpose

BLK-026 records the BEO publication candidate fixture boundary created by BLK-SYSTEM-023.

The purpose is to move BLK-024 Track G — BEO publication path from prose-only design toward deterministic local publication-candidate fixtures while preserving the current runtime boundary:

```text
candidate_status: "PUBLICATION_CANDIDATE_FIXTURE_ONLY"
beo_publication: "DRAFT_ONLY"
rtm_status: "NOT_GENERATED"
published: false
key_material_accessed: false
immutable_storage_written: false
public_ledger_mutated: false
rollback_executed: false
active_vault_read: false
```

This is maturity level L1 fixture-only. Candidate fixtures are not published BEOs.

---

## 2. Current Runtime Boundary

Current runtime BEO output remains draft-only:

```text
beo_publication: "DRAFT_ONLY"
rtm_status: "NOT_GENERATED"
```

BLK-026 does not authorize authoritative BEO publication, does not emit runtime `PUBLISHED` BEO output, does not create a live publisher, does not create a signer, does not use signer key material, does not write immutable storage, does not mutate a public ledger, and does not execute rollback, revocation, or supersession.

BLK-026 also asserts no RTM drift rejection authority and no protected BLK-req vault body reads.

Existing draft BEO projectors in `python/beo_fixture_projection.py` remain governed by BLK-014, BLK-016, and BLK-021. Candidate fixture construction in `python/beo_publication_candidate_fixtures.py` consumes already-supplied draft BEO fixtures only.

---

## 3. Candidate Fixture Shape

A BEO publication candidate fixture may include:

- `candidate_id`;
- `candidate_status: "PUBLICATION_CANDIDATE_FIXTURE_ONLY"`;
- source `beo_id`;
- canonical `beo_hash` computed from the supplied draft BEO fixture only;
- source `beb_id`;
- source `commit_hash`;
- source `pre_engine_hash`;
- exact source `trace_artifacts`;
- optional source-evidence identity copied from draft evidence metadata;
- publication-specific fixture approval metadata;
- signer fixture descriptor;
- storage fixture descriptor;
- ledger fixture descriptor;
- rollback fixture descriptor;
- no-side-effect booleans proving non-publication and no authority expansion.

The canonical `beo_hash` is a hash of the supplied draft BEO fixture object. It is not a hash of protected BLK-req vault bodies and must not require reading, copying, parsing, summarizing, exposing, or comparing bodies under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`.

---

## 4. Publication-Specific Approval Fixture

publication-specific approval cannot be inherited from execution, BLK-test, draft BEO projection, codex-live approval, or RTM approval.

A candidate fixture approval descriptor is fixture-only metadata. It may bind:

- `approval_record_hash`;
- `authorization_request_hash`;
- `operator_identity`;
- `approval_scope: "BEO_PUBLICATION_CANDIDATE_FIXTURE_ONLY"`;
- `approval_timestamp`;
- approved BEO identity;
- approved BEO hash;
- expired/replayed/stale flags that must be false.

This fixture approval is not live approval capture and does not authorize authoritative BEO publication.

---

## 5. Signer, Storage, Ledger, and Rollback Descriptors

Signer/storage/ledger/rollback descriptors are fixture-only.

They must prove:

- no signer key material access;
- no cryptographic signing side effect;
- no immutable storage writes;
- no public ledger mutation;
- no rollback, revocation, or supersession execution.

BLK-026 does not authorize signer key material, storage writer authority, public ledger mutation, rollback execution, revocation execution, or supersession execution.

---

## 6. Status and Evidence Rejection Boundary

Candidate fixtures may carry PASS/FAIL draft evidence as candidate evidence only. They must not convert bad evidence into published success.

BLOCKED/fatal/transport/interrupted/unknown/missing/malformed/stale/replayed evidence cannot publish success. Expired, replayed, stale, mismatched, malformed, or missing publication fixture approval also fails closed.

Candidate fixtures reject:

- runtime `PUBLISHED` BEO output;
- publication authority fields;
- RTM fields such as RTM IDs, coverage matrices, coverage status, drift, or drift decisions;
- active-vault read flags;
- missing or malformed canonical hashes;
- side-effect descriptors that claim signer key material access, storage writes, ledger mutation, rollback execution, revocation execution, or supersession execution.

---

## 7. RTM and Protected-Vault Exclusion

RTM remains separate and disabled. BLK-026 does not authorize RTM generation, RTM drift rejection authority, active-vault hash comparison, coverage matrices, coverage claims, or drift decisions.

Protected BLK-req vault bodies remain unread. BLK-026 does not read, copy, parse, hash, summarize, quote, compare, mutate, or expose protected requirement or use-case bodies under:

```text
docs/active/
docs/requirements/
docs/use_cases/
```

BLK-023 remains the design-only RTM boundary. Any RTM hash-only metadata path requires a later separate Track H sprint, explicit human approval, deterministic tests, hostile review, and closeout.

---

## 8. Implementation and Tests

Sprint 023 implementation is limited to deterministic local fixtures and doctrine gates:

- `python/beo_publication_candidate_fixtures.py`
- `python/test_beo_publication_candidate_fixtures.py`
- `python/test_active_doctrine_review_gates.py`
- `docs/BLK-026_beo-publication-candidate-fixture-boundary.md`
- `docs/reviews/BLK-SYSTEM-023_beo-publication-candidate-fixture-review.md`

No publisher module is authorized by this document. No live signer, storage writer, public ledger writer, rollback executor, revocation executor, supersession executor, RTM generator, active-vault scanner, BLK-test production MCP server, or live-smoke rerun is authorized by this document.

---

## 9. Future Authority Split

future authoritative publication requires a later explicit sprint and human approval.

That later sprint must separately request and prove:

1. publication-specific human approval capture;
2. signer identity and key-handling authority;
3. immutable storage write authority;
4. public ledger append authority;
5. rollback, revocation, and supersession authority;
6. replay-resistant audit bundle handling;
7. rejection of stale, replayed, mismatched, malformed, missing, BLOCKED, fatal, transport, interrupted, or unknown evidence;
8. RTM non-generation unless a separate RTM sprint has been approved;
9. protected-vault body exclusion;
10. hostile review and closeout.

BEO publication implementation remains separate from synthetic-smoke expansion, L4 BLK-test pilot runtime, RTM hash-only metadata path, and production BLK-test MCP.

---

## 10. Stop Conditions

Stop and treat any future change as outside BLK-026 authority if it attempts to publish authoritative BEOs, emit runtime `PUBLISHED` BEO output, capture live publication approval, access signer key material, sign, write immutable storage, mutate a public ledger, execute rollback/revocation/supersession, generate RTM, perform RTM drift rejection, compare active-vault hashes, create coverage matrices, read protected BLK-req vault bodies, start production BLK-test MCP, rerun BLK-SYSTEM-014/BLK-020 smoke, broaden BLK-test authority, or treat execution/BLK-test/draft-BEO/codex-live/RTM approval as publication approval.

---

## 11. Non-Authority Thesis

BLK-026 makes BEO publication candidate fixtures mechanically reviewable without making BEO publication real. The candidate proves shape, binding, rejection, and side-effect denial; it does not publish outcomes.
