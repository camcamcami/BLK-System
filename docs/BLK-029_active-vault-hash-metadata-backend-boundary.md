# BLK-029 — Active-vault Hash Metadata Backend Boundary

**Status:** Active fixture boundary contract — not active-vault read authority and not RTM generation authority
**Scope:** BLK-SYSTEM-026 active-vault hash metadata backend fixture; deterministic local backend-manifest fixtures only, with no active-vault filesystem scanning, no protected BLK-req vault body reads, no runtime active-vault hash comparison authority, no RTM generation, no coverage matrices, no RTM drift rejection authority, and no authoritative BEO publication.

---

## 1. Purpose

BLK-029 records the Active-vault hash metadata backend boundary created by BLK-SYSTEM-026.

The purpose is to bridge BLK-024 Track B — BLK-req legislative gateway and Track H — BLK-link offline RTM ledger by defining a fixture-only backend metadata shape that future RTM design can consume without direct access to protected requirement or use-case bodies.

Current runtime boundary:

```text
backend_status: "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY"
metadata_source: "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY"
downstream_metadata_source: "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY"
rtm_status: "NOT_GENERATED"
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

This is maturity level L1 fixture-only. Active-vault hash metadata backend fixtures are not active-vault readers, not active-vault scanners, not protected-body parsers, not RTM ledgers, not coverage matrices, not drift decisions, not published BEOs, and not BLK-req promotion or revision scripts.

---

## 2. Current Runtime Boundary

BLK-029 does not authorize active-vault filesystem scanning, active-vault file reads, protected BLK-req vault body reads, body copying, body parsing, body hashing, active-vault mutation, staging promotion, revision application, or backend promotion authority.

BLK-029 does not authorize RTM generation, does not emit runtime RTM IDs, does not create coverage matrices, does not claim coverage, does not compare active-vault hashes as runtime authority, does not make drift decisions, and does not authorize RTM drift rejection authority.

BLK-029 also does not authorize authoritative BEO publication, runtime `PUBLISHED` BEO output, public ledger mutation, signer key material, immutable storage writes, rollback execution, revocation execution, or supersession execution.

---

## 3. Fixture Shape

An active-vault hash metadata backend fixture may include:

- `manifest_id`;
- `backend_status: "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY"`;
- a common `backend_manifest_hash`;
- already-supplied backend manifest records;
- fixture-only backend approval metadata;
- downstream records with `metadata_source: "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY"` for BLK-027 compatibility;
- `rtm_status: "NOT_GENERATED"`;
- no-side-effect booleans proving no active-vault scanning, no active-vault reads, no protected-body access, no body copying/hashing, no RTM generation, no matrix creation, no drift decision, no publication, and no source mutation.

A backend fixture is not a live backend export. It represents already-supplied metadata only.

---

## 4. Backend Manifest Record Boundary

Backend manifest records must not contain protected bodies or protected path inputs.

Allowed backend manifest record shape:

| Field | Constraint |
| --- | --- |
| `kind` | Required non-empty artifact class such as `REQ` or `UC`. |
| `id` | Required non-empty artifact ID. |
| `version_hash` | Required canonical `sha256:<64-lowercase-hex>`. |
| `manifest_record_id` | Required non-empty fixture record identity. |
| `backend_manifest_hash` | Required canonical manifest hash shared by all records in a fixture. |
| `metadata_source` | Must equal `ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY`. |
| `downstream_metadata_source` | Must equal `ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY`. |
| `body_included` | Must be `false`. |
| `body_read` | Must be `false`. |
| `body_copied` | Must be `false`. |
| `body_hashed` | Must be `false`. |
| `active_vault_read` | Must be `false`. |
| `active_vault_scanned` | Must be `false`. |
| `protected_path_accessed` | Must be `false`. |

Forbidden protected-path fields include `active_vault_path`, `protected_path`, `requirements_path`, `use_cases_path`, `source_path`, `file_path`, and `path`.

Forbidden protected-body-shaped fields include `body`, `text`, `content`, `markdown`, `requirement_body`, `use_case_body`, `body_excerpt`, `body_hash_input`, `raw_artifact`, and `artifact_text`.

Protected BLK-req vault bodies remain unread. BLK-029 does not read, copy, parse, hash, summarize, quote, compare, mutate, or expose protected requirement or use-case bodies under:

```text
docs/active/
docs/requirements/
docs/use_cases/
```

Missing or malformed backend manifest metadata fails closed. Backend fixture records must carry canonical hashes, fixture-only metadata source, no protected path fields, no protected body fields, and explicit false body/access flags before any downstream `ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY` record can be built.

---

## 5. Approval Separation

Active-vault hash metadata backend approval is fixture-only metadata and cannot be inherited from execution, BLK-test, draft BEO projection, BEO publication candidate approval, published-BEO input receipt, Codex-live approval, BEO publication approval, or RTM approval.

A fixture approval may bind:

- `approval_record_hash`;
- `authorization_request_hash`;
- `operator_identity`;
- `approval_scope: "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY"`;
- `approval_timestamp`;
- approved backend manifest hash;
- expired/replayed/stale flags that must be false.

This fixture approval is not RTM generation approval and does not authorize `blk-link` runtime execution.

---

## 6. Rejection Boundary

Active-vault hash metadata backend fixtures reject:

- protected path fields;
- protected-body fields;
- non-string artifact, record, manifest, or operator identities;
- malformed canonical hashes;
- backend manifest records whose metadata source is not `ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY`;
- downstream metadata records whose downstream source is not `ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY`;
- active-vault read or scan flags;
- body read, copy, hash, or inclusion flags;
- promotion, revision, baseline authorization, parent-lock, or active-vault write fields;
- RTM generation fields such as RTM IDs, coverage matrices, coverage status, drift status, or drift decisions;
- publication fields such as signatures, ledgers, publication authority, runtime `PUBLISHED` BEO output, or published timestamps;
- stale, replayed, expired, mismatched, missing, malformed, unknown, superseded, rejected, drifted, or protected-body-dependent evidence as verified coverage.

---

## 7. Future Authority Split

future RTM generation requires a later explicit sprint and human approval.

That later sprint must separately request and prove:

1. authoritative BEO publication or a separately approved published-BEO fixture input path;
2. RTM-specific generation approval;
3. an approved backend hash-only active-vault metadata path;
4. protected-body exclusion;
5. coverage matrix generation rules;
6. stale/missing/malformed/superseded/unknown/rejected evidence states;
7. drift-review handoff;
8. rollback/supersession policy;
9. hostile review and closeout.

RTM drift rejection authority requires a still-later explicit authority boundary beyond basic ledger generation.

Future live BLK-req backend export requires a separate explicit sprint and human approval. That later sprint must prove promotion-time manifest creation or another no-body metadata mechanism without exposing protected bodies to BLK-test, BEO, RTM, tactical engines, or Discord context.

---

## 8. Implementation and Tests

Sprint 026 implementation is limited to deterministic local fixtures and doctrine gates:

- `python/active_vault_hash_metadata_backend_fixtures.py`
- `python/test_active_vault_hash_metadata_backend_fixtures.py`
- `python/test_active_doctrine_review_gates.py`
- `docs/BLK-029_active-vault-hash-metadata-backend-boundary.md`
- `docs/reviews/BLK-SYSTEM-026_active-vault-hash-metadata-backend-review.md`

No active-vault scanner module is authorized by this document. No protected-vault body reader, backend promotion runner, staged revision executor, RTM generator module, ledger writer, coverage matrix generator, drift-decision runtime, BEO publisher, signer, storage writer, public ledger writer, rollback executor, revocation executor, supersession executor, production BLK-test MCP server, or live-smoke rerun is authorized by this document.

---

## 9. Stop Conditions

Stop and treat any future change as outside BLK-029 authority if it attempts to scan `docs/active/`, read protected BLK-req vault bodies, copy bodies, parse bodies, hash bodies, expose body excerpts, mutate active-vault files, perform backend promotion, apply staged revisions, compare active-vault hashes as runtime authority, generate RTM, emit runtime RTM IDs, create coverage matrices, claim coverage, make drift decisions, authorize RTM drift rejection, publish authoritative BEOs, emit runtime `PUBLISHED` BEO output, capture live approval, access signer key material, write immutable storage, mutate a public ledger, execute rollback/revocation/supersession, start production BLK-test MCP, rerun BLK-SYSTEM-014/BLK-SYSTEM-020 smoke, broaden BLK-test authority, or treat execution/BLK-test/draft-BEO/candidate/published-input/Codex-live/BEO-publication approval as backend metadata or RTM approval.

---

## 10. Non-Authority Thesis

BLK-029 makes the hash-only active-vault metadata backend boundary mechanically reviewable without making protected-vault reads real and without making RTM generation real. The fixture proves metadata shape, approval separation, downstream compatibility with BLK-027, and side-effect denial; it does not close the V-model trace.
