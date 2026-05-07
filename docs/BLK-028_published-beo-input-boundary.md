# BLK-028 — Published BEO Input Boundary

**Status:** Active fixture boundary contract — not BEO publication authority
**Scope:** BLK-SYSTEM-025 published-BEO input boundary fixture; deterministic local input fixtures only, with no authoritative BEO publication, no runtime `PUBLISHED` BEO output, no live publication approval capture, no signer/storage/ledger/rollback side effects, no RTM generation, no RTM drift rejection authority, and no protected-vault body reads.

---

## 1. Purpose

BLK-028 records the Published BEO input boundary created by BLK-SYSTEM-025.

The purpose is to bridge BLK-024 Track G — BEO publication path and Track H — BLK-link offline RTM ledger by defining a fixture-only published-BEO input shape that future RTM design can distinguish from BEO publication candidates.

Current runtime boundary:

```text
input_status: "PUBLISHED_BEO_INPUT_FIXTURE_ONLY"
publication_receipt_scope: "PUBLISHED_BEO_INPUT_FIXTURE_ONLY"
beo_publication: "PUBLISHED_INPUT_FIXTURE_ONLY"
rtm_status: "NOT_GENERATED"
publication_performed: false
signature_generated: false
key_material_accessed: false
immutable_storage_written: false
public_ledger_mutated: false
rollback_executed: false
active_vault_read: false
protected_body_read: false
rtm_created: false
matrix_created: false
drift_decision_made: false
```

This is maturity level L1 fixture-only. Published-BEO input fixtures are not BEO publication execution, not runtime `PUBLISHED` BEO output, not RTM ledgers, not coverage matrices, not drift decisions, and not protected-vault readers.

---

## 2. Current Runtime Boundary

BLK-028 does not authorize authoritative BEO publication, does not emit runtime `PUBLISHED` BEO output, does not capture live publication approval, does not create a live publisher, does not create a signer, does not use signer key material, does not write immutable storage, does not mutate a public ledger, and does not execute rollback, revocation, or supersession.

BLK-028 does not authorize RTM generation, runtime RTM IDs, coverage matrices, coverage claims, runtime active-vault hash comparison, drift decisions, or RTM drift rejection authority.

BLK-028 also asserts no protected BLK-req vault body reads.

---

## 3. Fixture Shape

A published-BEO input fixture may include:

- `input_id`;
- `input_status: "PUBLISHED_BEO_INPUT_FIXTURE_ONLY"`;
- source BEO publication candidate identity;
- source `beo_id`, `beo_hash`, `beb_id`, `beo_status`, `commit_hash`, and `pre_engine_hash`;
- exact source `trace_artifacts`;
- a supplied publication receipt fixture;
- `publication_receipt_scope: "PUBLISHED_BEO_INPUT_FIXTURE_ONLY"`;
- `beo_publication: "PUBLISHED_INPUT_FIXTURE_ONLY"` as fixture vocabulary only, not runtime `PUBLISHED` BEO output;
- `rtm_status: "NOT_GENERATED"`;
- no-side-effect booleans proving no publication execution, no protected-body access, no RTM generation, no matrix creation, and no drift decision.

publication candidates are not published-BEO inputs. A future RTM implementation must not treat `PUBLICATION_CANDIDATE_FIXTURE_ONLY` as a published-BEO input unless a separate `PUBLISHED_BEO_INPUT_FIXTURE_ONLY` receipt fixture is present and valid.

---

## 4. Publication Receipt Fixture Boundary

A publication receipt fixture is supplied metadata only. It may bind:

- `receipt_id`;
- `publication_receipt_hash`;
- `publication_event_hash`;
- `published_input_identity`;
- `publication_receipt_scope: "PUBLISHED_BEO_INPUT_FIXTURE_ONLY"`;
- approved candidate identity;
- approved BEO hash;
- operator identity;
- signer identity;
- storage receipt hash;
- ledger receipt hash;
- fixture publication timestamp;
- expired/replayed/stale flags that must be false;
- side-effect flags proving no signature generation, no signer key material access, no immutable storage writes, no public ledger mutation, no rollback, revocation, or supersession execution.

Missing or malformed publication receipt fails closed. The receipt fixture is not live publication approval capture and does not authorize authoritative BEO publication.

---

## 5. Candidate and Receipt Rejection Boundary

Published-BEO input fixtures reject:

- source candidates whose `candidate_status` is not `PUBLICATION_CANDIDATE_FIXTURE_ONLY`;
- source candidates with runtime `beo_publication: "PUBLISHED"`;
- `published: true` on the source candidate;
- malformed candidate IDs, BEO IDs, BEO hashes, `pre_engine_hash`, or trace artifact hashes;
- receipt fixtures with missing, mismatched, malformed, stale, replayed, or expired receipt identity;
- receipt fixtures with `publication_receipt_scope` other than `PUBLISHED_BEO_INPUT_FIXTURE_ONLY`;
- publication authority fields;
- signature material or signer key material;
- signer/storage/ledger/rollback flags that claim side effects;
- RTM fields such as RTM IDs, coverage matrices, coverage claims, drift status, or drift decisions;
- active-vault read flags;
- protected-body read flags;
- body-bearing fields.

BLOCKED/fatal/transport/interrupted/unknown/missing/malformed/stale/replayed evidence cannot become successful published-BEO input. FAIL candidate evidence remains failed input metadata and must not be converted to success.

---

## 6. RTM and Protected-Vault Exclusion

RTM remains separate and disabled. BLK-028 does not authorize RTM generation, RTM drift rejection authority, active-vault hash comparison, coverage matrices, coverage claims, or drift decisions.

Protected BLK-req vault bodies remain unread. BLK-028 does not read, copy, parse, hash, summarize, quote, compare, mutate, or expose protected requirement or use-case bodies under:

```text
docs/active/
docs/requirements/
docs/use_cases/
```

BLK-027 remains the RTM hash-only metadata path boundary. A future RTM generation sprint may consume published-BEO input fixture metadata only after a later explicit sprint and human approval.

---

## 7. Future Authority Split

future RTM generation requires a later explicit sprint and human approval.

That later sprint must separately request and prove:

1. RTM-specific generation approval;
2. published-BEO input fixture or authoritative BEO publication input validation;
3. approved backend hash-only active-vault metadata path;
4. protected-body exclusion;
5. coverage matrix generation rules;
6. stale/missing/malformed/superseded/unknown/rejected evidence states;
7. drift-review handoff;
8. rollback/supersession policy;
9. hostile review and closeout.

Future authoritative BEO publication requires a separate explicit sprint and human approval. That later sprint must separately request and prove live publication approval capture, signer identity and key-handling authority, immutable storage write authority, public ledger append authority, rollback/revocation/supersession authority, replay-resistant audit bundle handling, and hostile review.

RTM drift rejection authority requires a still-later explicit authority boundary beyond basic ledger generation.

---

## 8. Implementation and Tests

Sprint 025 implementation is limited to deterministic local fixtures and doctrine gates:

- `python/published_beo_input_boundary_fixtures.py`
- `python/test_published_beo_input_boundary_fixtures.py`
- `python/test_active_doctrine_review_gates.py`
- `docs/BLK-028_published-beo-input-boundary.md`
- `docs/reviews/BLK-SYSTEM-025_published-beo-input-boundary-review.md`

No BEO publisher module is authorized by this document. No RTM generator module is authorized by this document. No ledger writer, active-vault body reader, coverage matrix generator, drift-decision runtime, signer, storage writer, public ledger writer, rollback executor, revocation executor, supersession executor, production BLK-test MCP server, or live-smoke rerun is authorized by this document.

---

## 9. Stop Conditions

Stop and treat any future change as outside BLK-028 authority if it attempts to publish authoritative BEOs, emit runtime `PUBLISHED` BEO output, capture live approval, access signer key material, sign, write immutable storage, mutate a public ledger, execute rollback/revocation/supersession, generate RTM, emit runtime RTM IDs, create coverage matrices, claim coverage, compare active-vault hashes as runtime authority, make drift decisions, authorize RTM drift rejection, read protected BLK-req vault bodies, treat BEO publication candidates as published-BEO inputs without receipt fixtures, start production BLK-test MCP, rerun BLK-SYSTEM-014/BLK-SYSTEM-020 smoke, broaden BLK-test authority, or treat execution/BLK-test/draft-BEO/codex-live/candidate/RTM approval as publication approval.

---

## 10. Non-Authority Thesis

BLK-028 makes the published-BEO input boundary mechanically reviewable without making BEO publication real and without making RTM generation real. The fixture proves shape, receipt binding, candidate-vs-input separation, approval separation, and side-effect denial; it does not close the V-model trace.
