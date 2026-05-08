# BLK-SYSTEM-030 — Offline RTM Generation Input Inventory

**Status:** Complete inventory — approved narrow offline RTM generation inputs
**Date:** 2026-05-08T14:22:54+10:00
**Plan:** `docs/plans/blk-system-030_offline-rtm-generation.md`
**BLK-024 track:** Track H — BLK-link offline RTM ledger
**Maturity:** Approved local RTM generation from already-supplied fixture inputs; no drift rejection or live vault access

---

## 1. Inventory Boundary

This inventory defines the exact already-supplied inputs and output constraints for BLK-SYSTEM-030 offline RTM generation. It does not authorize active-vault filesystem scanning, protected BLK-req body reads, BEO publication, signer/storage/public-ledger side effects, RTM drift rejection, or inherited approval from earlier fixtures.

The implementation may generate a deterministic local RTM ledger fixture from dictionaries supplied by the caller. It must not fetch, read, scan, execute, publish, sign, store, mutate, or decide drift.

---

## 2. Required Published-BEO Input Fields

A valid published-BEO input must be a caller-supplied `PUBLISHED_BEO_INPUT_FIXTURE_ONLY` dictionary with at minimum:

| Field | Required constraint |
| --- | --- |
| `input_id` | Non-empty string identity bound by RTM approval. |
| `input_status` | Must equal `PUBLISHED_BEO_INPUT_FIXTURE_ONLY`. |
| `beo_id` | Non-empty BEO identity. |
| `beo_hash` | Canonical `sha256:<64 lowercase hex>`. |
| `beb_id` | Non-empty source BEB identity. |
| `beo_status` | Accepted source status such as `PASS` or `FAIL`; status is recorded, not converted into publication authority. |
| `trace_artifacts` | Non-empty exact artifact identities with `kind`, `id`, and canonical `version_hash`. |
| `publication_receipt.publication_receipt_hash` | Canonical receipt hash supplied by the fixture. |
| `publication_receipt_scope` | Must equal `PUBLISHED_BEO_INPUT_FIXTURE_ONLY`. |
| `beo_publication` | Must equal `PUBLISHED_INPUT_FIXTURE_ONLY`, not runtime `PUBLISHED`. |
| `rtm_status` | Must equal `NOT_GENERATED` on input. |

Required false input flags:

- `publication_performed: false`
- `signature_generated: false`
- `key_material_accessed: false`
- `immutable_storage_written: false`
- `public_ledger_mutated: false`
- `rollback_executed: false`
- `active_vault_read: false`
- `protected_body_read: false`
- `rtm_created: false`
- `matrix_created: false`
- `drift_decision_made: false`

---

## 3. Required Active-Vault Hash Metadata Backend Fields

A valid backend input must be a caller-supplied `ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY` dictionary with at minimum:

| Field | Required constraint |
| --- | --- |
| `manifest_id` | Non-empty backend manifest identity. |
| `backend_status` | Must equal `ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY`. |
| `backend_manifest_hash` | Canonical `sha256:<64 lowercase hex>`. |
| `backend_approval.approval_record_hash` | Canonical approval hash supplied by backend fixture. |
| `downstream_hash_metadata_records` | Non-empty list of hash-only metadata records. |
| `rtm_status` | Must equal `NOT_GENERATED` on input. |

Each downstream metadata record must include:

| Field | Required constraint |
| --- | --- |
| `kind` | Non-empty artifact class matching trace artifact kind. |
| `id` | Non-empty artifact identity matching trace artifact ID. |
| `version_hash` | Canonical `sha256:<64 lowercase hex>`. |
| `metadata_source` | Must equal `ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY`. |
| `body_included` | Must be `false`. |
| `body_read` | Must be `false`. |

Required false backend flags:

- `active_vault_scanned: false`
- `active_vault_read: false`
- `protected_body_read: false`
- `body_copied: false`
- `body_hashed: false`
- `rtm_created: false`
- `matrix_created: false`
- `drift_decision_made: false`
- `publication_performed: false`
- `source_mutated: false`

---

## 4. Required RTM Generation Approval Fixture

BLK-SYSTEM-030 must introduce a new RTM-specific approval dictionary:

```text
approval_scope: "OFFLINE_RTM_GENERATION_APPROVAL_FIXTURE_ONLY"
generation_authorized: true
drift_rejection_authorized: false
```

Required binding fields:

| Field | Required constraint |
| --- | --- |
| `approval_id` | Non-empty approval identity. |
| `approval_record_hash` | Canonical hash of the operator approval record. |
| `authorization_request_hash` | Canonical hash of the request being approved. |
| `operator_identity` | Non-empty operator identity. |
| `approval_scope` | Must equal `OFFLINE_RTM_GENERATION_APPROVAL_FIXTURE_ONLY`. |
| `approval_timestamp` | Non-empty timestamp string. |
| `approved_input_id` | Must match published-BEO input `input_id`. |
| `approved_beo_hash` | Must match published-BEO input `beo_hash`. |
| `approved_backend_manifest_hash` | Must match backend fixture `backend_manifest_hash`. |
| `approved_output_id` | Must match requested RTM output identity. |
| `generation_authorized` | Must be `true`. |
| `drift_rejection_authorized` | Must be `false`. |
| `expired`, `replayed`, `stale` | Must all be `false`. |

The following approval scopes are explicitly rejected as inherited authority:

- `RTM_GENERATION_READINESS_PROPOSAL_FIXTURE_ONLY`
- `PUBLISHED_BEO_INPUT_FIXTURE_ONLY`
- `ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY`
- `BLK_TEST_PASS`
- `BEO_PUBLICATION_APPROVAL`
- `BLK_PIPE_EXECUTION_APPROVAL`
- `CODEX_LIVE_APPROVAL`

---

## 5. RTM Ledger Output Fields

The generated offline RTM ledger fixture should include:

- `rtm_id`
- `rtm_status: "OFFLINE_RTM_LEDGER_GENERATED_FIXTURE_ONLY"`
- `rtm_authority: "OFFLINE_RTM_GENERATION_APPROVED_NARROW"`
- `coverage_matrix_status: "OFFLINE_RTM_COVERAGE_MATRIX_FIXTURE_ONLY"`
- canonical `rtm_ledger_hash`
- source `input_id`, `beo_id`, `beo_hash`, `beb_id`, `beo_status`, and `publication_receipt_hash`
- source `manifest_id`, `backend_manifest_hash`, and `backend_approval_hash`
- exact trace artifact identities from the published-BEO input
- exact hash metadata identities from the backend fixture
- coverage records generated only by hash identity matching
- approval binding evidence copied from the RTM generation approval fixture
- explicit no-side-effect booleans

---

## 6. Coverage and Review States

Allowed coverage state vocabulary:

| State | Meaning | Authority |
| --- | --- | --- |
| `TRACE_HASH_MATCHED` | Trace artifact and supplied metadata identity share `kind`, `id`, and `version_hash`. | Valid offline RTM coverage record. |
| `MISSING_HASH_METADATA_REVIEW_REQUIRED` | Trace artifact has no supplied metadata identity. | Fail-closed or review package only; not drift rejection. |
| `EXTRA_HASH_METADATA_REVIEW_REQUIRED` | Metadata exists for no trace artifact identity. | Fail-closed or review package only; not drift rejection. |
| `HASH_MISMATCH_REVIEW_REQUIRED` | Trace and metadata identities match but hash differs. | Fail-closed or review package only; not drift rejection. |
| `DRIFT_REVIEW_REQUIRED_NOT_REJECTED` | A drift-like condition exists but no rejection is authorized. | Human-review handoff only. |

Task 2 should fail closed on missing, extra, duplicate, or mismatched identities for the generated ledger helper unless a future separate review-package helper is explicitly planned. BLK-SYSTEM-030 does not authorize RTM drift rejection.

---

## 7. Forbidden Fields and Side Effects

Reject top-level and nested fields that attempt to smuggle:

- protected path/body content: `path`, `active_vault_path`, `protected_path`, `body`, `text`, `content`, `markdown`, `requirement_body`, `use_case_body`, `body_excerpt`, `body_hash_input`, `raw_artifact`, `artifact_text`;
- active-vault scanning/reading: `active_vault_scanned`, `active_vault_read`, path scan commands, body copy/parse/hash flags;
- BEO publication/signing/storage/ledger authority: `publication_authority`, `beo_publication_authority`, `published_at`, `signature`, `key_material`, `private_key`, `storage_writer`, `ledger_writer`, `public_ledger_mutated`, rollback/revocation/supersession fields;
- RTM drift rejection: `drift_rejection`, `drift_rejected`, `reject_drift`, `drift_decision: "REJECTED"`;
- inherited approval scopes from execution, BLK-test, BEO publication, published input, backend metadata, or proposal fixtures;
- network/API/package-manager/shell behavior.

---

## 8. Acceptance Mapping for Task 2

Task 2 should prove via RED/GREEN tests that the offline RTM generation helper:

- builds deterministic `OFFLINE_RTM_LEDGER_GENERATED_FIXTURE_ONLY` output from valid supplied inputs and RTM-specific approval;
- produces stable ledger hashes regardless of input dictionary insertion order;
- requires exact trace/metadata bijection by `(kind, id)` and `version_hash`;
- rejects duplicate trace identities, duplicate metadata identities, extra metadata, missing metadata, hash mismatches, malformed hashes, unsupported fields, nested protected-body/path/secret/publication/drift fields, true side-effect flags, stale/replayed/expired approval, and inherited approval scopes;
- emits all explicit no-side-effect markers including `PROTECTED_BODY_NOT_READ`, `ACTIVE_VAULT_NOT_SCANNED`, `BEO_PUBLICATION_NOT_PERFORMED`, and `NO_SIGNER_STORAGE_OR_PUBLIC_LEDGER_SIDE_EFFECTS`;
- contains no live execution/network/file-scan/API surface.
