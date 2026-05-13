# BLK-SYSTEM-099 Hostile Review — External BEO Publication Approval Decision Capture

**Date:** 2026-05-13
**Reviewer:** Hermes local hostile audit after delegated review timeout
**Scope:** Local BLK-SYSTEM-099 uncommitted changes for approval-decision capture only.
**Verdict:** PASS after remediation

---

## 0. Review Note

A delegated hostile-review subagent timed out after 600 seconds and is not treated as PASS evidence. Hermes performed this local hostile audit with concrete probes and remediated stale-roadmap findings before closeout.

---

## 1. Reviewed Surfaces

```text
python/beo_external_publication_approval_decision.py
python/test_beo_external_publication_approval_decision.py
docs/BLK-099_external-beo-publication-approval-decision.md
docs/BLK-077_blk-system-post-078-roadmap.md
docs/BLK-079_post-078-current-state-authority-index.md
python/blk_current_state_authority_index.py
python/test_blk_current_state_authority_index.py
python/test_active_doctrine_review_gates.py
docs/plans/blk-system-099_external-beo-publication-approval-decision-capture.md
docs/outcomes/BLK-SYSTEM-099_task-000-outcome.md
docs/outcomes/BLK-SYSTEM-099_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-099_task-002-outcome.md
docs/outcomes/BLK-SYSTEM-099_task-003-outcome.md
```

---

## 2. Authority-Boundary Findings

### Finding 1 — Approval vs execution separation

**Result:** PASS

BLK-SYSTEM-099 records:

```text
EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK098_REQUEST_NOT_PUBLISHED
BEO-PUBLICATION-APPROVAL-DECISION-099-001
approval_decision_package_hash: sha256:c83ea7982632b587a8596550cfa0f1c36b546a70b8f2fa8cbefb4aedfeda383b
BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001
sha256:a782b223c88ae155a37519b87313dd2085450515c78ba60e93277c636ba6e041
```

The package captures approval for one future separately scoped external BEO publication execution sprint only. It sets publication/execution/run-consumption side-effect flags false and records `beo_publication_status: APPROVAL_DECISION_CAPTURED_NOT_PUBLISHED`.

### Finding 2 — Future run ID consumption

**Result:** PASS

`RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001` is reserved but not consumed. The fixture requires `future_publication_execution_run_id_consumed: False`, rejects side-effect flag mutation, and current-state docs state run ID reserved but not consumed.

### Finding 3 — Upstream BLK-SYSTEM-098 package forgery

**Result:** PASS

The fixture recomputes `request_package_hash`, checks exact BLK-098 status/id/scope/frontier, validates exact proof/denial sets and all BLK-098 false side-effect flags, then requires canonical hash `sha256:a782b223c88ae155a37519b87313dd2085450515c78ba60e93277c636ba6e041`. Self-consistently rehashed target-head drift and approval-granted drift are rejected by tests.

### Finding 4 — Scanner hardening for authority laundering

**Result:** PASS

Focused tests and custom probes block compact/camel/percent variants for `PublicationAuthorized`, `SigningGranted`, `BEOisPublished`, `rtm_generation_authorized`, and `docs%252Factive` protected-path references outside the narrow 099 decision record.

Custom hostile probe output:

```text
operator_identity_publication_authorized: BLOCKED: authority-laundering text at operator_identity: publicationauthorized
operator_text_signing_granted: BLOCKED: authority-laundering text at operator_approval_text_raw: signinggranted
operator_text_double_encoded_protected_path: BLOCKED: protected BLK-req body reference at operator_approval_text_raw: docsactive
package_id_beo_is_published: BLOCKED: authority-laundering text at approval_decision_package_id: beoispublished
decision_result_rtm_generation_authorized: BLOCKED: authority-laundering text at decision_result: rtm generation
side_effect_publication_execution: BLOCKED: publication_execution_performed must remain false
CUSTOM_HOSTILE_PROBES_OK
```

### Finding 5 — Stale BLK-SYSTEM-098 frontier wording

**Initial result:** BLOCKER

Initial local review found stale current-state/roadmap wording that still presented BLK-SYSTEM-098 as the current open frontier and still used `After BLK-SYSTEM-098` language.

**Remediation:** COMPLETE

Patched:

```text
docs/BLK-077_blk-system-post-078-roadmap.md
docs/BLK-079_post-078-current-state-authority-index.md
python/test_active_doctrine_review_gates.py
```

Post-remediation stale scan:

```text
STALE_FRONTIER_SCAN_OK
```

### Finding 6 — Adjacent denied authorities

**Result:** PASS

The fixture, docs, and current-state index continue to deny:

- external publication execution in this sprint;
- runtime `PUBLISHED` BEO output;
- signer key material and cryptographic signing;
- immutable storage writes and public ledger mutation;
- rollback, revocation, and supersession;
- runtime RTM generation and RTM drift rejection;
- authoritative drift decision, active-vault comparison, coverage truth, and coverage promotion;
- protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation;
- target-repo scan/mutation and source/Git mutation;
- BLK-pipe, BLK-test runtime, Codex, package/network/model/browser/cyber tooling;
- production isolation claims.

---

## 3. Verification Evidence

Focused suite after remediation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_beo_external_publication_approval_decision python.test_active_doctrine_review_gates python.test_blk_current_state_authority_index
.....................................................................................................................................................
----------------------------------------------------------------------
Ran 149 tests in 17.386s

OK
```

Custom hostile probes and stale scan:

```text
CUSTOM_HOSTILE_PROBES_OK
STALE_FRONTIER_SCAN_OK
```

---

## 4. Final Verdict

PASS. BLK-SYSTEM-099 captures approval-decision evidence for the exact BLK-SYSTEM-098 package without publication execution or adjacent authority laundering. A future external BEO publication execution sprint remains separately required before any publication side effect.
