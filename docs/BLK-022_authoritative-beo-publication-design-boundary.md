# BLK-022 — Authoritative BEO Publication Design Boundary

**Status:** Active design-only boundary contract
**Scope:** BLK-SYSTEM-016 authoritative BEO publication design boundary; non-executing, non-publishing, and non-RTM.

---

## 1. Purpose

BLK-022 records the BLK-SYSTEM-016 design boundary for a future authoritative BEO publication mechanism. It exists because BLK-021 permits source-bound BLK-020 first-smoke evidence to project only into draft BEO fixtures; publication authority remains separate.

BLK-022 is design-only doctrine. It does not authorize authoritative BEO publication, does not implement BEO publication, does not mutate public outcome ledgers, and does not grant signer/storage/rollback authority.

---

## 2. Current runtime boundary

Current runtime BEO projection is still draft-only:

```text
beo_publication: "DRAFT_ONLY" remains the only current runtime output
rtm_status: "NOT_GENERATED" remains mandatory
```

BLK-022 does not emit runtime PUBLISHED BEOs, does not add a BEO publisher, does not add a public ledger writer, does not add a signer, does not add storage writes, and does not add a rollback executor.

Existing projectors in `python/beo_fixture_projection.py` and interface fixtures in `python/beo_rtm_interface_fixtures.py` remain constrained by BLK-014, BLK-016, and BLK-021.

---

## 3. Publication approval separation

A future BEO publication implementation must require a publication-specific human approval. It cannot inherit approval from execution or test authorization.

Required separation:

- codex-live approval is not BEO publication approval;
- BLK-test MCP approval is not BEO publication approval;
- BLK-pipe execution success is not BEO publication approval;
- draft BEO projection is not BEO publication approval;
- Hermes/Codex implementation support is not publication approval.

A future publication approval must bind exact BEO identity, BEO content hash, source evidence hash, source BLK-pipe report identity, BLK-test evidence identity, operator identity, signer identity, storage target identity, public ledger target, rollback policy, and timestamp.

---

## 4. Future publication candidate schema — prose only

A future implementation sprint may propose a publication candidate schema only after separate human approval. The schema must include:

- draft BEO ID and canonical BEO hash;
- `beb_id`, source commit hash, `pre_engine_hash`, and source evidence hash;
- BLK-test evidence source, run ID, transcript hash, and cleanup status;
- non-empty canonical `trace_artifacts[*].version_hash` values;
- publication approval record hash and operator identity;
- signer identity policy and signature envelope;
- storage target identity and immutable write policy;
- public ledger mutation rules;
- rollback, revocation, and supersession plan.

This section is prose only. It is not a runtime schema, not a storage adapter, not a signer, and not a ledger writer.

---

## 5. Status matrix

| Candidate status | Publication design boundary |
| --- | --- |
| `PASS` | PASS stays PASS and may become a future publication candidate only after publication-specific approval. |
| `FAIL` | FAIL stays FAIL and may become a future publication candidate only as failed evidence. |
| `BLOCKED` | BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success. |
| `FATAL_TIMEOUT` | BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success. |
| `FATAL_OUTPUT_FLOOD` | BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success. |
| `TRANSPORT_ERROR` | BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success. |
| `OPERATOR_INTERRUPTED` | BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success. |
| unknown/missing | BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success. |

No future publication design may convert failed, blocked, fatal, transport, interrupted, unknown, or missing evidence into success.

---

## 6. Public ledger, signer, storage, and rollback checklist

A later publication implementation sprint must define and test all of the following before it may request authority:

1. Publication-specific human approval validation.
2. Signer identity policy, key handling, and secret non-exposure rules.
3. Immutable storage target and write semantics.
4. Public ledger mutation rules and append-only identity.
5. Rollback, revocation, supersession, and recovery rules.
6. Replay bundle and audit hash rules.
7. Rejection for stale, mismatched, missing, replayed, or expired approvals.
8. Rejection for any attempt to publish `BLOCKED`, fatal, transport, interrupted, unknown, or missing evidence as success.
9. Bounded evidence and secret/protected-body exclusion.
10. Post-publication handoff boundaries for later RTM work.

Sprint 016 defines this checklist only. It does not implement any checklist item as runtime authority.

---

## 7. RTM and protected vault exclusion

BLK-022 does not generate RTM, does not create `rtm_id`, does not create coverage matrices, does not claim coverage, does not compare active-vault hashes, and does not make drift decisions.

protected BLK-req vault bodies remain unread. BLK-022 does not parse, compare, quote, summarize, or expose bodies under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`.

A Later RTM sprint remains separate from BEO publication design. It must define offline traceability, active-vault hash policy, coverage, drift rejection, and rollback interactions independently.

BLK-023 records the BLK-SYSTEM-017 offline RTM ledger design boundary. BLK-023 is design-only: it does not authorize RTM generation, does not authorize RTM drift rejection authority, does not implement `generate_rtm.py`, does not emit runtime `rtm_id`, does not create coverage matrices, does not make drift decisions, keeps rtm_status: "NOT_GENERATED" remains mandatory for current runtime outputs, and keeps protected BLK-req vault bodies unread.

---

## 8. Implementation and tests

Sprint 016 implementation is limited to docs and gates:

- `docs/reviews/BLK-SYSTEM-016_authoritative-beo-publication-design-review.md`
- `docs/BLK-022_authoritative-beo-publication-design-boundary.md`
- `python/test_active_doctrine_review_gates.py`
- `python/test_beo_publication_design_gates.py`

No publisher module is authorized by this document.

---

## 9. Stop conditions

Stop and treat any future change as outside BLK-022 authority if it attempts to publish BEOs, mutate public outcome ledgers, add signer/storage/rollback authority, emit runtime `PUBLISHED` BEOs, accept live publication approvals, generate RTM, claim coverage, compare active-vault hashes, read protected BLK-req vault bodies, rerun BLK-SYSTEM-014 first live smoke, broaden BLK-test MCP tools, start live transport, or project BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown evidence to success.
