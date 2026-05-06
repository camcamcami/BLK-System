# BLK-021 — BEO Draft Publication Gate Review

**Status:** Active draft-only BEO gate review contract
**Scope:** BLK-SYSTEM-015 Draft BEO publication gate review for source-bound BLK-020 first-smoke evidence, with no authoritative BEO publication or RTM authority.

---

## 1. Purpose

BLK-021 records the BLK-SYSTEM-015 draft BEO publication gate review. It defines how source-bound and replayable BLK-020 first-smoke evidence may project into draft BEO fixtures while preserving `beo_publication: "DRAFT_ONLY"` and `rtm_status: "NOT_GENERATED"`.

BLK-021 does not authorize authoritative BEO publication, public outcome ledger mutation, signer/storage/rollback authority, RTM generation, RTM coverage, protected BLK-req vault body reads, or rerunning BLK-SYSTEM-014 first live smoke.

---

## 2. Draft-only BEO gate boundary

PASS/FAIL evidence may project only to draft BEO fixtures. Every projected object must remain a deterministic local fixture and must retain:

```text
beo_publication: "DRAFT_ONLY"
rtm_status: "NOT_GENERATED"
```

The projection is not publication. It does not create a BEO signer, published timestamp, storage location, public ledger row, rollback authority, release authority, or operator approval for publication.

---

## 3. Accepted source evidence

The accepted source for this gate is BLK-020 first-smoke evidence only, carried as local dictionaries with:

- `sprint: "BLK-SYSTEM-014"`;
- `source: "blk-test-mcp-first-live-smoke"`;
- `run_id`;
- `tool_name`;
- `beb_id`;
- `commit_hash`;
- `pre_engine_hash`;
- non-empty canonical `trace_artifacts`;
- non-empty PASS/FAIL checks;
- `approval_record_hash`;
- `authorization_request_hash`;
- `source_evidence_hash`;
- `transcript_hash`;
- `cleanup_status`.

Source-bound and replayable evidence is required. Missing, malformed, or authority-bearing evidence fails closed.

---

## 4. Projection status matrix

| First-smoke evidence status | Draft BEO result |
| --- | --- |
| `PASS` | draft PASS BEO fixture only |
| `FAIL` | draft FAIL BEO fixture only |
| `BLOCKED` | no BEO success projection |
| `FATAL_TIMEOUT` | no BEO success projection |
| `FATAL_OUTPUT_FLOOD` | no BEO success projection |
| `TRANSPORT_ERROR` | no BEO success projection |
| `OPERATOR_INTERRUPTED` | no BEO success projection |
| unknown/missing | no BEO success projection |

BLOCKED evidence must not project to success. Fatal, transport, interrupted, unknown, and missing evidence must not become BEO success evidence.

---

## 5. Required replay/source fields and canonical hashes

The projector requires canonical `sha256:<64-lowercase-hex>` values for replay/source hashes and canonical `sha256:<64-lowercase-hex>` trace artifact `version_hash` values. The cryptographic baton remains opaque; BLK-021 does not verify protected requirement bodies.

---

## 6. Publication non-authority checklist

BLK-021 preserves these markers:

- does not authorize authoritative BEO publication;
- does not mutate public outcome ledgers;
- does not grant signer/storage/rollback authority;
- does not add published timestamps, signatures, storage locations, public ledger identifiers, rollback authority, or publication authority;
- does not authorize live BLK-test MCP;
- does not rerun BLK-SYSTEM-014 first live smoke;
- does not use arbitrary shell;
- does not run against real target repositories;
- does not mutate primary repo as BLK-test behavior.

---

## 7. RTM non-generation and active-vault exclusion

BLK-021 does not authorize RTM generation and does not claim RTM coverage. It rejects RTM, RTM ID, requirements, coverage matrix, coverage status, drift, or drift-decision fields in draft BEO projection.

BLK-021 does not read protected BLK-req vault bodies from `docs/active/`, `docs/requirements/`, or `docs/use_cases/`.

---

## 8. Implementation and tests

Implementation and test files:

- `python/beo_fixture_projection.py`
- `python/test_beo_fixture_projection.py`
- `python/test_active_doctrine_review_gates.py`

Related doctrine:

- `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`
- `docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md`

---

## 9. Stop conditions

Stop and treat any future change as outside BLK-021 authority if it attempts to publish BEOs, mutate public outcome ledgers, add signer/storage/rollback authority, generate RTM, claim RTM coverage, read protected BLK-req vault bodies, rerun BLK-SYSTEM-014 first live smoke, broaden BLK-test MCP tools, start live transport, or project BLOCKED/FATAL/transport/operator-interrupted/unknown evidence to success.

---

## 10. Handoff

A later explicit authoritative BEO publication sprint may be proposed only with separate human approval, signer/storage/rollback design, public ledger mutation rules, and rollback evidence.

A Later RTM sprint remains separate from BLK-test MCP and draft BEO projection. It must define any offline RTM generation, drift rejection, active-vault hash policy, and rollback behavior separately.
