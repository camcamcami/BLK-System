# BLK-023 — Offline RTM Ledger Design Boundary

**Status:** Active design-only boundary contract
**Scope:** BLK-SYSTEM-017 offline RTM ledger design boundary; non-executing, non-generating, non-drift-rejecting, and non-publication.

---

## 1. Purpose

BLK-023 records the BLK-SYSTEM-017 offline RTM ledger design boundary for a future `blk-link` traceability mechanism. It exists because BLK-016/021 preserve disabled RTM interface fields, BLK-022 separates BEO publication from RTM, and Sprint 010 GAP-010 requires RTM non-generation to remain mandatory until a later explicit Traceability Aggregator sprint.

BLK-023 is design-only doctrine. It does not authorize RTM generation, does not authorize RTM drift rejection authority, does not implement generate_rtm.py, does not create coverage matrices, and does not make drift decisions.

---

## 2. Current runtime boundary

Current runtime RTM interfaces remain disabled-only:

```text
beo_publication: "DRAFT_ONLY" remains mandatory
rtm_status: "NOT_GENERATED" remains mandatory
rtm_authority: "DISABLED_INTERFACE_ONLY" remains mandatory
```

BLK-023 does not emit runtime rtm_id, does not emit runtime `rtm`, does not emit runtime `requirements`, does not emit runtime `coverage_matrix`, does not emit runtime `coverage_status`, does not emit runtime `drift`, does not emit runtime `drift_decision`, and does not emit runtime `drift_status`.

Existing projectors in `python/beo_fixture_projection.py` and disabled interface fixtures in `python/beo_rtm_interface_fixtures.py` remain constrained by BLK-014, BLK-016, BLK-021, and BLK-022.

---

## 3. RTM approval separation

A future offline RTM implementation must require RTM-specific human approval. It cannot inherit approval from execution, BLK-test smoke, or BEO publication authorization.

Required separation:

- RTM generation approval is separate from BEO publication approval;
- RTM generation approval is separate from BLK-test MCP approval;
- RTM generation approval is separate from codex-live approval;
- RTM generation approval is separate from BLK-pipe execution success;
- RTM generation approval is separate from draft BEO projection;
- BEO publication approval does not authorize RTM generation;
- BLK-test PASS does not authorize RTM generation;
- RTM drift rejection authority requires a separate future review boundary.

A future RTM approval must bind exact RTM identity, source BEO identity, source BEO hash, source outcome identity, source evidence hash, BLK-test evidence identity, active-vault hash policy, operator identity, ledger target, drift policy, rollback/supersession policy, and timestamp.

---

## 4. Hash-only active-vault policy

hash-only active-vault comparison remains future authority. BLK-023 may design future use of opaque `trace_artifacts[*].version_hash` values and active-vault hashes, but it does not perform active-vault hash comparison at runtime.

protected BLK-req vault bodies remain unread. BLK-023 does not parse, compare, quote, summarize, or expose protected requirement or use-case bodies under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`.

A future implementation must prove hash-only access, bounded replay evidence, secret exclusion, and protected-body exclusion before any RTM generation authority can be requested.

---

## 5. Future RTM ledger candidate schema — prose only

A future implementation sprint may propose an RTM ledger candidate schema only after separate human approval. The schema must include:

- RTM ID and canonical RTM ledger hash;
- source BEO ID and canonical BEO hash;
- source outcome identity and source BLK-pipe evidence identity;
- BLK-test evidence source, run ID, status, and transcript hash;
- non-empty canonical `trace_artifacts[*].version_hash` values;
- active-vault hash identity and hash-only comparison policy;
- coverage status vocabulary for traced, missing, stale, unknown, superseded, and rejected evidence;
- drift event identity and review state;
- rollback, supersession, and recovery plan;
- audit bundle and protected-body exclusion record.

This section is prose only. It is not a runtime schema, not a ledger writer, not an active-vault scanner, and not a drift-decision executor.

---

## 6. Coverage and drift vocabulary

| Candidate state | Sprint 017 design boundary |
| --- | --- |
| traced hash match | May be a future design state only; Sprint 017 does not claim coverage. |
| missing BEO trace hash | Must remain a future rejection/review state; Sprint 017 does not emit RTM. |
| stale active-vault hash | Must remain a future rejection/review state; Sprint 017 does not make drift decisions. |
| malformed trace hash | Must remain a future rejection state and must not become coverage. |
| replayed or mismatched evidence | Must remain a future rejection state and must not become coverage. |
| protected body access required | Must stop; protected BLK-req vault bodies remain unread. |

No future RTM design may convert missing, stale, malformed, replayed, mismatched, unknown, or protected-body-dependent evidence into verified coverage without explicit future authority and review.

---

## 7. BEO publication, BLK-test, and source mutation exclusions

BLK-023 does not authorize authoritative BEO publication, does not mutate public outcome ledgers, does not grant signer/storage/rollback authority, and does not treat BEO publication approval as RTM generation approval.

BLK-023 does not start live BLK-test MCP, does not rerun BLK-SYSTEM-014 first live smoke, does not broaden fixed tools, does not run against real target repositories, does not use arbitrary shell, and does not emit RTM coverage or drift decisions from BLK-test evidence.

BLK-023 does not mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source as RTM behavior.

---

## 8. Implementation and tests

Sprint 017 implementation is limited to docs and gates:

- `docs/reviews/BLK-SYSTEM-017_offline-rtm-ledger-design-review.md`
- `docs/BLK-023_offline-rtm-ledger-design-boundary.md`
- `python/test_active_doctrine_review_gates.py`
- `python/test_rtm_ledger_design_gates.py`

No RTM generator module is authorized by this document. No `generate_rtm.py`, ledger writer, active-vault scanner, coverage matrix generator, or drift-decision runtime is authorized by this document.

---

## 9. Stop conditions

Stop and treat any future change as outside BLK-023 authority if it attempts to generate RTM, authorize RTM drift rejection authority, implement `generate_rtm.py`, emit runtime `rtm_id`, emit runtime `rtm`, create coverage matrices, claim coverage, make drift decisions, compare active-vault hashes at runtime, read protected BLK-req vault bodies, publish authoritative BEOs, mutate public outcome ledgers, add signer/storage/rollback authority, start live BLK-test MCP, rerun BLK-SYSTEM-014 first live smoke, broaden tools, run against real target repositories, mutate source, or claim production sandbox or host-secret isolation.
