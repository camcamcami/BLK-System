# BLK-033 — Offline RTM generation boundary

**Status:** Active implementation boundary — Narrow approved offline RTM generation from supplied fixture inputs
**Sprint:** BLK-SYSTEM-030
**BLK-024 track:** Track H — BLK-link offline RTM ledger
**Maturity:** Narrow approved local RTM generation from already-supplied fixture inputs

---

## 1. Purpose

BLK-033 records the Offline RTM generation boundary created by BLK-SYSTEM-030. It implements narrow approved offline RTM generation from supplied fixture inputs without granting adjacent authorities.

The active vocabulary is:

- `OFFLINE_RTM_GENERATION_APPROVAL_FIXTURE_ONLY`
- `OFFLINE_RTM_LEDGER_GENERATED_FIXTURE_ONLY`
- `OFFLINE_RTM_COVERAGE_MATRIX_FIXTURE_ONLY`
- `OFFLINE_RTM_GENERATION_APPROVED_NARROW`
- `DRIFT_REVIEW_REQUIRED_NOT_REJECTED`
- `PROTECTED_BODY_NOT_READ`
- `ACTIVE_VAULT_NOT_SCANNED`
- `BEO_PUBLICATION_NOT_PERFORMED`
- `NO_SIGNER_STORAGE_OR_PUBLIC_LEDGER_SIDE_EFFECTS`

Persistent doctrine gate marker: BLK-SYSTEM-030 pins narrow offline RTM generation only.

---

## 2. Authorized Input Boundary

BLK-033 authorizes deterministic local RTM ledger fixture generation only from already-supplied dictionaries with these statuses:

```text
input_status: "PUBLISHED_BEO_INPUT_FIXTURE_ONLY"
backend_status: "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY"
approval_scope: "OFFLINE_RTM_GENERATION_APPROVAL_FIXTURE_ONLY"
```

The published-BEO input must provide BEO identity, canonical BEO hash, source BEB identity, publication receipt hash, and trace artifact identities. The active-vault metadata backend must provide backend manifest identity/hash, backend approval hash, and hash-only metadata records. Hash-only metadata records must include only kind, id, version_hash, metadata source, and explicit no-body flags.

Publication receipts, backend approvals, trace artifacts, metadata records, generation approvals, and top-level input dictionaries are strict allowlist containers. Ignored top-level live-state fields, unbound publication event hashes, and backend `manifest_records` containers are not accepted. Accepted status/hash/scope fields are validated as supplied and are not whitespace-normalized. Identity fields use compact numeric fixture-ID positive-format allowlists and separator/compaction-normalized authority/protected-reference checks; they reject prose/body-like values, encoded paths, whitespace, path-like values, protected-vault references, and inherited-authority strings. Operator identity is limited to a compact lower-case fixture identity grammar plus normalized protected-reference/body-marker rejection. Approval timestamps must match a strict RFC3339 fixture timestamp shape before canonical hash binding.

This boundary does not treat BEO publication candidates, RTM readiness proposals, backend metadata approvals, BLK-test PASS, BLK-pipe execution success, or BEO publication approval as RTM generation approval. It does not inherit approval. The RTM-specific approval fixture must bind canonical `authorization_request_hash` and `approval_record_hash` values to the supplied input identity, BEO hash, publication receipt hash, backend manifest hash, backend approval hash, output ID, sorted trace/hash metadata identities, operator identity, timestamp, and no-drift-rejection policy.

---

## 3. Generated Output Boundary

The offline RTM ledger output may include:

- `rtm_id`;
- `rtm_status: "OFFLINE_RTM_LEDGER_GENERATED_FIXTURE_ONLY"`;
- `rtm_authority: "OFFLINE_RTM_GENERATION_APPROVED_NARROW"`;
- `coverage_matrix_status: "OFFLINE_RTM_COVERAGE_MATRIX_FIXTURE_ONLY"`;
- deterministic `rtm_ledger_hash` from canonical JSON;
- source BEO/input/backend/approval identities and hashes;
- copied trace artifact identities and hash-only metadata identities;
- coverage records with `TRACE_HASH_MATCHED` only when supplied trace artifact and supplied metadata records match by kind, id, and version_hash.

Coverage records are generated only by trace/hash metadata bijection. This means coverage records are generated only by trace/hash metadata bijection. Extra metadata, missing metadata, duplicate identities, mismatched hashes, malformed hashes, unsupported fields, stale/replayed approval, or protected-body-dependent evidence fails closed.

---

## 4. Explicit Non-Authorities

BLK-033 does not read protected BLK-req vault bodies, does not copy protected bodies, does not parse protected bodies, does not hash protected bodies, does not quote protected bodies, and does not summarize protected bodies.

BLK-033 does not scan active-vault paths, does not read active-vault files, does not compare active-vault files at runtime, does not mutate active-vault files, and does not perform backend promotion.

BLK-033 does not publish BEOs, does not emit runtime `PUBLISHED` BEO output, does not capture live publication approval, does not access signer key material, does not generate cryptographic signatures, does not write immutable storage, does not mutate public ledgers, and does not execute rollback, revocation, or supersession.

BLK-033 does not reject drift, does not authorize RTM drift rejection, and does not make final drift decisions. Drift-like evidence is represented only as `DRIFT_REVIEW_REQUIRED_NOT_REJECTED` for later human review.

BLK-033 does not start production BLK-test MCP, rerun live smoke, invoke BLK-pipe, mutate source, contact network/API/model services, run package managers, or execute arbitrary shell.

---

## 5. Rejection Boundary

Offline RTM generation fixtures reject:

- protected path fields such as `active_vault_path`, `protected_path`, `requirements_path`, `use_cases_path`, `source_path`, `file_path`, and `path`;
- protected-body fields such as `body`, `text`, `content`, `markdown`, `requirement_body`, `use_case_body`, `body_excerpt`, `body_hash_input`, `raw_artifact`, and `artifact_text`;
- publication and side-effect fields such as `publication_authority`, `beo_publication_authority`, `published_at`, `signature`, `key_material`, `private_key`, `ledger_id`, storage authority, signer authority, rollback authority, and runtime public-ledger mutation;
- drift rejection fields such as `drift_rejection`, `drift_rejected`, `reject_drift`, and `drift_decision`;
- inherited approval scopes from proposal fixtures, execution, BLK-test, BEO publication, published-BEO input receipts, backend metadata approvals, or Codex/live tactical approvals;
- unsupported fields in nested publication receipt, backend approval, trace artifact, metadata record, and approval containers;
- path-like identity values or identity values carrying protected-vault references, body-like prose, encoded path text, whitespace, separator-variant authority markers, or inherited-authority strings;
- backend `manifest_records`, unbound publication event hashes, or other unused context holders that could carry protected body text, protected paths, live-state flags, or inherited authority;
- leading/trailing whitespace normalization in accepted status, hash, scope, timestamp, or identity schema fields;
- mismatched canonical `authorization_request_hash` or `approval_record_hash` values for RTM-specific approval;
- true side-effect flags for active-vault reads/scans, protected-body reads, body copy/hash, publication, signing, storage, public ledger mutation, source mutation, or drift decisions.

---

## 6. Stop Conditions

Stop and treat any future change as outside BLK-033 authority if it attempts to read protected bodies, scan active vaults, publish BEOs, access signer/storage/public-ledger authority, reject drift, inherit approval, mutate source or Git, run network/API/package-manager/shell behavior, start BLK-test, or claim production sandbox/host-secret isolation.

---

## 7. Future Authority Handoff

A later sprint may request drift review or drift rejection authority only as a separate human-approved sprint. That later sprint must preserve BLK-033's generated ledger hash stability, trace/hash metadata bijection, protected-body exclusion, no active-vault scanning, and no signer/storage/public-ledger side effects.
