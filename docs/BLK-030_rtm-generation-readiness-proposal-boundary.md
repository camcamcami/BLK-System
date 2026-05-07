# BLK-030 — RTM Generation Readiness Proposal Boundary

**Status:** Active proposal fixture boundary contract — not runtime RTM generation authority
**Scope:** BLK-SYSTEM-027 RTM generation readiness proposal boundary; deterministic local proposal fixtures only, with no runtime RTM generation, no RTM IDs, no RTM ledgers, no coverage matrices, no RTM drift rejection authority, no active-vault filesystem scanning, no protected BLK-req vault body reads, no runtime active-vault hash comparison, and no authoritative BEO publication.

---

## 1. Purpose

BLK-030 records the RTM generation readiness proposal boundary created by BLK-SYSTEM-027.

The purpose is to bridge BLK-024 Track H — BLK-link offline RTM ledger with Track G published-BEO input fixtures and Track B hash-only metadata backend fixtures. It defines a proposal-only fixture shape that can package already-supplied `PUBLISHED_BEO_INPUT_FIXTURE_ONLY` and `ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY` evidence for later human RTM approval review without generating RTM now.

Current runtime boundary:

```text
proposal_status: "RTM_GENERATION_READINESS_PROPOSAL_FIXTURE_ONLY"
rtm_status: "NOT_GENERATED"
rtm_authority: "PROPOSAL_ONLY_NOT_AUTHORIZED"
generation_approval_required: true
rtm_generation_authorized: false
active_vault_scanned: false
active_vault_read: false
protected_body_read: false
body_copied: false
body_hashed: false
rtm_created: false
matrix_created: false
drift_decision_made: false
publication_performed: false
source_mutated: false
```

This is maturity level L1 fixture-only with L0 doctrine-boundary update. The proposal fixture is not a runtime RTM generator, not an RTM ledger, not a coverage matrix, not a drift decision, not RTM drift rejection authority, not active-vault read authority, not BEO publication authority, and not BLK-test authority.

---

## 2. Current Runtime Boundary

BLK-030 does not authorize runtime RTM generation, runtime RTM IDs, RTM ledgers, coverage matrices, coverage claims, active-vault hash comparison as runtime authority, drift events, drift decisions, or RTM drift rejection authority.

BLK-030 does not authorize active-vault filesystem scanning, active-vault file reads, protected BLK-req vault body reads, body copying, body parsing, body hashing, active-vault mutation, staging promotion, revision application, or backend promotion authority.

BLK-030 also does not authorize authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, public ledger mutation, signer key material, immutable storage writes, rollback execution, revocation execution, supersession execution, production BLK-test MCP, or new live BLK-test smoke runs.

---

## 3. Proposal Fixture Shape

An RTM generation readiness proposal fixture may include:

- `proposal_id`;
- `proposal_status: "RTM_GENERATION_READINESS_PROPOSAL_FIXTURE_ONLY"`;
- source published-BEO input identity from a `PUBLISHED_BEO_INPUT_FIXTURE_ONLY` fixture;
- BEO identity and canonical BEO hash;
- trace artifact identities and canonical `version_hash` values;
- active-vault hash metadata backend manifest identity from an `ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY` fixture;
- metadata record identities from `ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY` downstream records;
- readiness records with `readiness_state: "READY_FOR_LATER_RTM_APPROVAL"` only;
- proposal request metadata proving separate later RTM approval remains required;
- no-side-effect booleans proving no active-vault scanning, no active-vault reads, no protected-body access, no body copying/hashing, no RTM generation, no matrix creation, no drift decision, no publication, and no source mutation.

A proposal fixture is not a live RTM generation request execution. It is a deterministic local review packet for a later human decision.

---

## 4. Input Boundary

### 4.1 Published-BEO input fixture

A valid proposal input must use already-supplied published-BEO input fixture metadata only:

```text
input_status: "PUBLISHED_BEO_INPUT_FIXTURE_ONLY"
publication_receipt_scope: "PUBLISHED_BEO_INPUT_FIXTURE_ONLY"
beo_publication: "PUBLISHED_INPUT_FIXTURE_ONLY"
rtm_status: "NOT_GENERATED"
```

The published-BEO input fixture must not perform publication, access signer key material, write immutable storage, mutate a public ledger, execute rollback, read active-vault files, read protected bodies, create RTM, create matrices, or make drift decisions.

Published-BEO input fixtures are still fixture inputs. They are not runtime authoritative BEO publication and do not grant RTM generation authority.

### 4.2 Active-vault hash metadata backend fixture

A valid proposal input must use already-supplied backend hash metadata fixture metadata only:

```text
backend_status: "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY"
metadata_source: "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY"
rtm_status: "NOT_GENERATED"
```

The backend fixture must not scan active-vault files, read active-vault files, read/copy/parse/hash protected bodies, generate RTM, create matrices, make drift decisions, publish BEOs, or mutate source.

Hash metadata records must not contain protected bodies. Missing or malformed metadata fails closed. Mismatched trace artifact and metadata `version_hash` identities fail closed.

### 4.3 Proposal request

A proposal request may bind:

- `proposal_request_hash`;
- `authorization_request_hash`;
- `operator_identity`;
- `request_scope: "RTM_GENERATION_READINESS_PROPOSAL_FIXTURE_ONLY"`;
- `request_timestamp`;
- approved published-BEO input identity;
- approved BEO hash;
- approved backend manifest hash;
- `generation_approval_required: true`;
- `rtm_generation_authorized: false`;
- expired/replayed/stale flags that must be false.

This proposal request is not RTM generation approval and cannot be treated as runtime authority.

---

## 5. Rejection Boundary

RTM generation readiness proposal fixtures reject:

- protected path fields such as `active_vault_path`, `protected_path`, `requirements_path`, `use_cases_path`, `source_path`, `file_path`, and `path`;
- protected-body fields such as `body`, `text`, `content`, `markdown`, `requirement_body`, `use_case_body`, `body_excerpt`, `body_hash_input`, `raw_artifact`, and `artifact_text`;
- runtime RTM fields such as `rtm_id`, `rtm_ledger`, `rtm_output`, `generated_at`, `generation_commit`, `coverage_matrix`, `coverage_status`, and `coverage_claim`;
- drift fields such as `drift`, `drift_status`, `drift_decision`, `drift_rejection`, and `drift_rejected`;
- publication fields such as `signature`, `ledger_id`, `publication_authority`, `published_at`, and `beo_publication_authority`;
- secret-bearing fields such as `key_material`, `private_key`, `secret`, `token`, and `host_key`;
- true side-effect flags for active-vault scanning/read, protected-body read, body copy/hash, RTM creation, matrix creation, drift decision, publication, source mutation, signer, storage, ledger, or rollback behavior;
- stale, replayed, expired, mismatched, missing, malformed, unknown, superseded, rejected, drifted, or protected-body-dependent evidence as RTM-ready evidence.

Nested protected-body, RTM runtime, drift, publication, path, and secret-bearing fields fail closed.

---

## 6. Future Authority Split

future runtime RTM generation requires a later explicit sprint and human approval.

That later sprint must separately request and prove:

1. RTM-specific generation approval, not inherited from this proposal fixture;
2. accepted published-BEO input authority or a stronger live publication authority;
3. an approved hash-only active-vault metadata backend path;
4. protected-body exclusion;
5. coverage matrix generation rules;
6. stale/missing/malformed/superseded/unknown/rejected evidence states;
7. drift-review handoff;
8. rollback/supersession policy;
9. hostile review and closeout.

RTM drift rejection authority requires a still-later explicit authority boundary beyond basic ledger generation.

Future live BLK-req backend export requires a separate explicit sprint and human approval. That later sprint must prove promotion-time manifest creation or another no-body metadata mechanism without exposing protected bodies to BLK-test, BEO, RTM, tactical engines, or Discord context.

---

## 7. Implementation and Tests

Sprint 027 implementation is limited to deterministic local fixtures and doctrine gates:

- `python/rtm_generation_readiness_proposal_fixtures.py`
- `python/test_rtm_generation_readiness_proposal_fixtures.py`
- `python/test_active_doctrine_review_gates.py`
- `docs/BLK-030_rtm-generation-readiness-proposal-boundary.md`
- `docs/reviews/BLK-SYSTEM-027_rtm-generation-readiness-proposal-review.md`

No runtime RTM generator module is authorized by this document. No RTM ledger writer, coverage matrix generator, drift-decision runtime, active-vault scanner module, protected-vault body reader, backend promotion runner, staged revision executor, BEO publisher, signer, storage writer, public ledger writer, rollback executor, revocation executor, supersession executor, production BLK-test MCP server, or live-smoke rerun is authorized by this document.

---

## 8. Stop Conditions

Stop and treat any future change as outside BLK-030 authority if it attempts to scan `docs/active/`, read protected BLK-req vault bodies, copy bodies, parse bodies, hash bodies, expose body excerpts, mutate active-vault files, perform backend promotion, apply staged revisions, compare active-vault hashes as runtime authority, generate RTM at runtime, emit runtime RTM IDs, create RTM ledgers, create coverage matrices, claim coverage, make drift decisions, authorize RTM drift rejection, publish authoritative BEOs, emit runtime `PUBLISHED` BEO output, capture live approval, access signer key material, write immutable storage, mutate a public ledger, execute rollback/revocation/supersession, start production BLK-test MCP, rerun BLK-SYSTEM-014/BLK-SYSTEM-020 smoke, broaden BLK-test authority, or treat execution/BLK-test/draft-BEO/candidate/published-input/backend-metadata/Codex-live/BEO-publication approval as runtime RTM generation approval.

---

## 9. Non-Authority Thesis

BLK-030 makes future RTM-generation readiness mechanically reviewable without making RTM generation real. The fixture proves prerequisite packaging, approval separation, hash identity preservation, and side-effect denial; it does not close the V-model trace and does not grant runtime ledger authority.
