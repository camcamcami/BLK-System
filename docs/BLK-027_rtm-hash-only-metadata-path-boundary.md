# BLK-027 — RTM Hash-Only Metadata Path Boundary

**Status:** Active fixture boundary contract — not RTM generation authority  
**Scope:** BLK-SYSTEM-024 RTM hash-only metadata path fixture; deterministic local path fixtures only, with no RTM generation, no runtime active-vault hash comparison authority, no coverage matrices, no RTM drift rejection authority, no protected-vault body reads, and no authoritative BEO publication.

---

## 1. Purpose

BLK-027 records the RTM hash-only metadata path boundary created by BLK-SYSTEM-024.

The purpose is to move BLK-024 Track H — BLK-link offline RTM ledger from prose-only design toward deterministic local hash-metadata path fixtures while preserving the current runtime boundary:

```text
path_status: "RTM_HASH_METADATA_PATH_FIXTURE_ONLY"
rtm_status: "NOT_GENERATED"
comparison_state: "NOT_EVALUATED_FIXTURE_ONLY"
active_vault_read: false
protected_body_read: false
rtm_created: false
matrix_created: false
drift_decision_made: false
published: false
```

This is maturity level L1 fixture-only. RTM hash metadata path fixtures are not RTM ledgers, not coverage matrices, not drift decisions, not published BEOs, and not protected-vault readers.

---

## 2. Current Runtime Boundary

Current runtime RTM output remains disabled-only:

```text
rtm_status: "NOT_GENERATED"
rtm_authority: "RTM_HASH_METADATA_PATH_FIXTURE_ONLY"
comparison_state: "NOT_EVALUATED_FIXTURE_ONLY"
```

BLK-027 does not authorize RTM generation, does not emit runtime RTM IDs, does not create coverage matrices, does not claim coverage, does not compare active-vault hashes as runtime authority, does not make drift decisions, and does not authorize RTM drift rejection authority.

BLK-027 also does not authorize authoritative BEO publication, runtime `PUBLISHED` BEO output, no protected BLK-req vault body reads, public ledger mutation, signer key material, immutable storage writes, rollback execution, revocation execution, or supersession execution.

---

## 3. Fixture Shape

A RTM hash-only metadata path fixture may include:

- `path_id`;
- `path_status: "RTM_HASH_METADATA_PATH_FIXTURE_ONLY"`;
- source BEO publication candidate identity;
- source `beo_id`, `beo_hash`, `beb_id`, and `beo_status`;
- exact source `trace_artifacts`;
- supplied hash-only active-vault metadata records;
- fixture-only RTM metadata approval;
- path records that pair trace artifact identities with supplied metadata identities;
- `comparison_state: "NOT_EVALUATED_FIXTURE_ONLY"`;
- no-authority booleans proving non-generation, no protected-body access, no matrix creation, no drift decision, and no publication.

BEO publication candidates are not published BEOs. A future RTM implementation must not treat `PUBLICATION_CANDIDATE_FIXTURE_ONLY` as authoritative publication.

---

## 4. Hash-Only Metadata Record Boundary

hash-only metadata records must not contain protected bodies.

Allowed metadata record shape:

| Field | Constraint |
| --- | --- |
| `kind` | Required non-empty artifact class such as `REQ` or `UC`. |
| `id` | Required non-empty artifact ID. |
| `version_hash` | Required canonical `sha256:<64-lowercase-hex>`. |
| `metadata_source` | Must equal `ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY`. |
| `body_included` | Must be `false`. |
| `body_read` | Must be `false`. |

Forbidden protected-body-shaped fields include `body`, `text`, `content`, `markdown`, `requirement_body`, `use_case_body`, `body_excerpt`, and `body_hash_input`.

Protected BLK-req vault bodies remain unread. BLK-027 does not read, copy, parse, hash, summarize, quote, compare, mutate, or expose protected requirement or use-case bodies under:

```text
docs/active/
docs/requirements/
docs/use_cases/
```

---

## 5. Approval Separation

RTM hash metadata path approval is fixture-only metadata and cannot be inherited from execution, BLK-test, draft BEO projection, BEO publication candidate approval, codex-live approval, or BEO publication approval.

A fixture approval may bind:

- `approval_record_hash`;
- `authorization_request_hash`;
- `operator_identity`;
- `approval_scope: "RTM_HASH_METADATA_PATH_FIXTURE_ONLY"`;
- `approval_timestamp`;
- approved candidate identity;
- approved BEO hash;
- expired/replayed/stale flags that must be false.

This fixture approval is not RTM generation approval and does not authorize `blk-link` runtime execution.

---

## 6. Rejection Boundary

RTM hash metadata path fixtures reject:

- non-candidate BEO states;
- `beo_publication: "PUBLISHED"`;
- `published: true`;
- RTM generation fields such as RTM IDs, coverage matrices, coverage status, drift, drift status, or drift decisions;
- active-vault read flags;
- protected-body read flags;
- body-bearing metadata records;
- missing or malformed canonical hashes;
- malformed or stale RTM metadata approval fixtures.

Missing, malformed, stale, replayed, unknown, superseded, rejected, drifted, or protected-body-dependent evidence cannot become verified RTM coverage in this boundary.

Missing or malformed hash-only metadata fails closed. Hash-only metadata records must carry canonical hashes, fixture-only metadata source, no protected body fields, and explicit `body_included: false` / `body_read: false` flags before a fixture path can be built.

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

---

## 8. Implementation and Tests

Sprint 024 implementation is limited to deterministic local fixtures and doctrine gates:

- `python/rtm_hash_only_metadata_path_fixtures.py`
- `python/test_rtm_hash_only_metadata_path_fixtures.py`
- `python/test_active_doctrine_review_gates.py`
- `docs/BLK-027_rtm-hash-only-metadata-path-boundary.md`
- `docs/reviews/BLK-SYSTEM-024_rtm-hash-only-metadata-path-review.md`

No RTM generator module is authorized by this document. No ledger writer, active-vault body reader, coverage matrix generator, drift-decision runtime, BEO publisher, signer, storage writer, public ledger writer, rollback executor, revocation executor, supersession executor, production BLK-test MCP server, or live-smoke rerun is authorized by this document.

---

## 9. Stop Conditions

Stop and treat any future change as outside BLK-027 authority if it attempts to generate RTM, emit runtime RTM IDs, create coverage matrices, claim coverage, compare active-vault hashes as runtime authority, make drift decisions, authorize RTM drift rejection, read protected BLK-req vault bodies, treat BEO publication candidates as published BEOs, publish authoritative BEOs, capture live approval, access signer key material, write immutable storage, mutate a public ledger, execute rollback/revocation/supersession, start production BLK-test MCP, rerun BLK-SYSTEM-014/BLK-SYSTEM-020 smoke, broaden BLK-test authority, or treat execution/BLK-test/draft-BEO/codex-live/BEO-publication approval as RTM approval.

---

## 10. Non-Authority Thesis

BLK-027 makes the hash-only metadata path mechanically reviewable without making RTM generation real. The fixture proves shape, hash-only input constraints, approval separation, and side-effect denial; it does not close the V-model trace.
