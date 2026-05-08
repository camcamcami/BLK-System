# BLK-SYSTEM-030 — Offline RTM Generation Hostile Review

**Status:** PASS after remediation
**Date:** 2026-05-08T15:56:20+10:00
**Plan:** `docs/plans/blk-system-030_offline-rtm-generation.md`
**Boundary:** `docs/BLK-033_offline-rtm-generation-boundary.md`
**Implementation:** `python/offline_rtm_generation_fixtures.py`

---

## 1. Review Scope

This hostile review audited BLK-SYSTEM-030 for narrow offline RTM generation from already-supplied fixture inputs only:

- `PUBLISHED_BEO_INPUT_FIXTURE_ONLY`
- `ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY`
- `OFFLINE_RTM_GENERATION_APPROVAL_FIXTURE_ONLY`

The review specifically tested whether the implementation accidentally authorized protected BLK-req body reads, active-vault filesystem scanning, BEO publication, signer/storage/public-ledger side effects, RTM drift rejection, inherited approval, live execution, network/API/package-manager calls, or source mutation through runtime paths.

Reviewed artifacts:

- `docs/plans/blk-system-030_offline-rtm-generation.md`
- `docs/reviews/BLK-SYSTEM-030_offline-rtm-generation-input-inventory.md`
- `docs/BLK-033_offline-rtm-generation-boundary.md`
- `python/offline_rtm_generation_fixtures.py`
- `python/test_offline_rtm_generation_fixtures.py`
- `python/test_active_doctrine_review_gates.py`
- `docs/outcomes/BLK-SYSTEM-030_task-002-outcome.md`

---

## 2. Hostile Review Loop

Multiple hostile reviews initially returned `BLOCKED` even after focused tests passed. The blockers were valid guidance-alignment gaps for offline fixture work: accepted-but-ignored fields, nested authority smuggling, body/prose identity laundering, separator variants of inherited-authority markers, insufficient canonical approval binding, and strip-before-validate schema normalization.

Each blocker was converted into RED regression coverage before implementation remediation, then rerun to GREEN.

---

## 3. Blockers and Remediation

| # | Blocker | Remediation |
| --- | --- | --- |
| 1 | Nested `publication_receipt`, `backend_approval`, `trace_artifacts`, and metadata containers could carry unsupported protected body/path/publication/secret/drift fields. | Added strict allowlists for accepted containers and RED tests for nested smuggling. |
| 2 | Canonical approval hashes could be stale or replayed unless bound to exact supplied input, backend, trace, metadata, operator, timestamp, output, and no-drift policy. | Added canonical `authorization_request_hash` and `approval_record_hash` recomputation and mismatch rejection. |
| 3 | Body/prose and protected paths could be laundered through identity fields such as `REQ-THE_SYSTEM_SHALL_NOT_READ_BODY_TEXT` or encoded path text. | Added compact numeric fixture-ID positive grammars plus forbidden identity fragment checks. |
| 4 | Separator variants such as `BEO-PUBLICATION-APPROVAL` and `BLK.TEST.PASS` bypassed underscore-only inherited-authority checks. | Added separator-normalized authority checks and regression probes for hyphen/dot variants. |
| 5 | Backend `manifest_records` and unbound `publication_event_hash` fields were accepted despite not being semantically needed for generated output. | Removed these fields from allowed schemas and added fail-closed tests. |
| 6 | Operator identity could carry protected-reference/body markers or compacted inherited authority such as `beopublicationapproval`, `blktestpass`, `codexliveapproval`, `publishedbeoinputfixtureonly`, or `rejectdrift`. | Limited operator identity grammar and checked both normalized and compacted authority/protected markers. |
| 7 | Accepted status/hash/scope/timestamp fields were stripped before validation, allowing whitespace-normalized supplied values. | Changed raw schema validation to reject leading/trailing whitespace and added regression coverage. |
| 8 | Approval timestamps could carry smuggled/malformed values before canonical hash comparison. | Added strict RFC3339 fixture timestamp validation before canonical approval binding. |

---

## 4. Post-Remediation Hostile Probes

Final hostile review returned `PASS` and verified rejection of the concrete guidance probes:

```text
REQ-THE_SYSTEM_SHALL_NOT_READ_BODY_TEXT                 rejected
docs%2Factive%2FREQ-001.md                             rejected
RTM-GEN-APPROVAL-BEO-PUBLICATION-APPROVAL              rejected
BEO-PUBLICATION-APPROVAL                                rejected
BEO_PUBLICATION_APPROVAL                                rejected
BLK.TEST.PASS                                           rejected
beopublicationapproval                                  rejected
blktestpass                                             rejected
codexliveapproval                                       rejected
publishedbeoinputfixtureonly                           rejected
rejectdrift                                             rejected
```

The final review also verified strict rejection of nested smuggling, ignored top-level live-state fields, backend `manifest_records`, unbound `publication_event_hash`, stale/mismatched approval hashes, malformed timestamps, and whitespace-normalized accepted schema values.

---

## 5. Boundary Assertions After Remediation

The remediated implementation preserves BLK-SYSTEM-030 guidance alignment:

- only already-supplied fixture dictionaries are consumed;
- no protected BLK-req body read surface exists;
- no active-vault filesystem scanning or file-read/hash-comparison surface exists;
- no BEO publication, signer, storage, public-ledger, or source mutation surface exists;
- no network/API/model/package-manager/shell execution surface exists;
- no RTM drift rejection authority is granted;
- no BLK-test, BEO publication, proposal, execution, Codex/live, or backend approval is inherited as RTM generation approval;
- every accepted field is schema-validated and either semantically used in output/canonical hashes or explicitly rejected;
- trace artifacts and hash metadata must match exactly by `(kind, id, version_hash)` before coverage records are generated.

---

## 6. Verification

Focused verification after remediation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_offline_rtm_generation_fixtures -v
Ran 21 tests in 0.016s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
Ran 50 tests in 0.005s
OK
```

Full verification before closeout docs:

```text
go test ./...                              PASS
go vet ./...                               PASS
python unittest discover                   Ran 431 tests in 6.470s — OK
markdown fence check                       PASS
git diff --check                           PASS
```

---

## 7. Final Verdict

PASS after remediation. BLK-SYSTEM-030 remains aligned with guidance documentation and is limited to deterministic offline RTM generation from supplied fixtures only. It does not grant adjacent live, publication, storage, approval, drift, protected-read, active-vault-scan, or execution authority.
