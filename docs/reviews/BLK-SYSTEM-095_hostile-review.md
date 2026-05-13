# BLK-SYSTEM-095 Hostile Review — Exact Local RTM Drift-Rejection Execution

**Status:** PASS after remediation
**Review timestamp:** 2026-05-13T12:15:22+10:00
**Sprint:** BLK-SYSTEM-095 — Exact Local RTM Drift-Rejection Execution

## Scope

Reviewed the BLK-SYSTEM-095 exact local RTM drift-rejection execution sprint against BLK-001, BLK-077, BLK-079, BLK-093, BLK-094, and the BLK-System authority-gated sprint rules.

Reviewed artifacts:

- `python/exact_local_rtm_drift_rejection_execution.py`
- `python/test_exact_local_rtm_drift_rejection_execution.py`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_active_doctrine_review_gates.py`
- `docs/plans/blk-system-095_exact-local-rtm-drift-rejection-execution.md`
- `docs/BLK-095_exact-local-rtm-drift-rejection-execution.md`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- task outcomes `000` through `003`

## Boundary Reviewed

BLK-SYSTEM-095 may only consume the exact BLK-SYSTEM-093 approval-decision package and exact future run ID inside a local non-authoritative fixture:

```text
RTM-DRIFT-REJECTION-APPROVAL-DECISION-093-001
RUN-BLK-SYSTEM-091-RTM-DRIFT-REJECTION-001
RTM-DRIFT-REJECTION-EXECUTION-095-001
PILOT_LOCAL_RTM_DRIFT_REJECTION_RECORDED_NOT_AUTHORITATIVE
```

It must not grant reusable/runtime RTM drift-rejection authority, authoritative drift decision, runtime `blk-link` trace closure, active-vault comparison, protected-body reads/hashing, external ledger mutation, target/source/Git mutation by fixtures, BEB dispatch, BEO closeout execution, BLK-pipe/BLK-test/Codex runtime, package/network/model/browser/cyber tooling, or production-isolation claims.

## Initial Hostile Findings

### Finding 1 — Self-hashed lookalike BLK-093 approvals could pass

Initial review found that the BLK-095 fixture recomputed the submitted approval package hash but did not pin the canonical BLK-093 package identity/hash and upstream BLK-091/BLK-090 identity fields. A self-consistent forged approval package could be re-hashed and mirrored into the execution request.

**Remediation:** Added canonical BLK-093 package hash pinning plus exact canonical upstream/operator/RTM/BEO/target field validation. Added regression tests for self-hashed lookalikes.

### Finding 2 — Nested `local_rtm_ledger` trace pollution could pass

Initial review found that nested `trace_artifacts` and `pilot_publication_artifact_hash` were copied into output evidence without strict shape/hash/laundering validation.

**Remediation:** Added exact trace-artifact schema, allowed trace-kind checking, required `version_hash`, required `pilot_publication_artifact_hash`, and nested string scanning. Added regression tests for malformed trace shape, invalid hashes, and protected-body laundering text.

### Finding 3 — BLK-093 approval attestation was not validated

Initial review found the upstream approval package `operator_attestation` was schema-required but not exact-key/all-true validated.

**Remediation:** Added exact BLK-093 attestation validation and regressions for corrupted attestation booleans.

### Finding 4 — BLK-095-specific laundering variants were missed

Initial review found the scanner missed runtime `blk-link` trace-closure and authoritative-drift-decision variants.

**Remediation:** Added BLK-095-local normalized marker scanning for runtime `blk-link` trace closure, authoritative drift decision, reusable/runtime RTM drift rejection, protected-body reads/hashing, active-vault comparison, ledger mutation, target/source/Git mutation, BEB/BEO execution, runtime/tooling, and production isolation. Added request and trace-artifact laundering regressions.

### Finding 5 — Calendar-expired approvals could pass

Initial review found that a self-consistent, already-expired approval interval could be accepted if request timestamps fit inside that old interval.

**Remediation:** Added deterministic fixture evaluation-time expiry validation and regression coverage.

### Finding 6 — Active docs/index still contained stale post-095 wording

Initial docs/current-state review found stale “execution remains unrun” and “candidate exact local execution sprint” wording in active BLK-077/079/current-state surfaces after BLK-SYSTEM-095 had executed locally.

**Remediation:** Rephrased stale active wording as historical BLK-093/094 state and recorded BLK-SYSTEM-095 local consumption of the exact run ID. Added active-doc stale-phrase gates.

### Finding 7 — Superseded approval-required markers were unqualified

Initial review found `EXPLICIT_HUMAN_RTM_DRIFT_REJECTION_APPROVAL_REQUIRED_NOT_GRANTED` still appeared as a current unqualified marker after BLK-SYSTEM-093 approval capture and BLK-SYSTEM-095 local consumption.

**Remediation:** Qualified remaining occurrences as historical/as-of-BLK-091 markers and paired them with later BLK-SYSTEM-093 approval capture / BLK-SYSTEM-095 local run consumption in BLK-077, BLK-079, and the executable current-state index.

### Finding 8 — Current-state scanner missed positive BLK-095 effect phrasing

Initial review found the scanner missed variants such as `authoritative drift decision made`, `runtime blk-link trace closure occurred`, `active-vault comparison performed`, `protected-body reads are enabled`, and `external ledger mutation performed`.

**Remediation:** Added spaced, hyphenated, hash/non-hash, and compact/camel variants to the scanner and regression tests. Added negation handling so canonical denial wording such as “no source mutation authorized” and “no runtime blk-link trace closure occurred” does not false-positive while positive claims still fail closed.

## Re-Review Result

Focused re-reviews after remediation passed:

- Python fixture re-review: PASS — self-hashed approvals, nested ledger pollution, corrupt attestation, calendar-expired approval, and BLK-095-specific laundering probes were rejected.
- Docs/current-state/gates re-review: PASS — stale active wording was qualified or removed, superseded approval-required markers were historical/as-of markers, and current-state scanner probes for active-vault comparison variants now fail closed.

Focused verification during re-review:

```text
python/test_exact_local_rtm_drift_rejection_execution.py: 8 tests passed, 53 subtests passed
python/test_blk_current_state_authority_index.py + python/test_active_doctrine_review_gates.py: Ran 135 tests ... OK
```

## Final Review Decision

PASS after remediation.

BLK-SYSTEM-095 is safe to proceed to closeout verification as local non-authoritative evidence only. This review grants no reusable/runtime RTM drift-rejection authority, no authoritative drift decision, no runtime `blk-link` trace closure, no active-vault comparison, no protected-body reads/hashing, no external ledger mutation, no target/source/Git mutation, no BEB/BEO execution, no runtime/tooling, and no production-isolation claim.
