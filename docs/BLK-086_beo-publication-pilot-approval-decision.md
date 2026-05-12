# BLK-086 — BEO Publication Pilot Approval Decision

**Status:** Active exact approval-decision boundary — human approval decision captured for the exact BLK-085 request; not publication pilot execution
**Scope:** BLK-SYSTEM-086 consumes the canonical BLK-085 BEO publication pilot execution request package and records a deterministic approval-decision package for one future exact publication-pilot execution sprint. It does not execute that pilot.

---

## 1. Purpose

BLK-086 records the BLK-SYSTEM-086 boundary for a BEO Publication Pilot Approval Decision. The purpose is to convert the exact BLK-085 request package into a hash-bound approval-decision record while preserving the remaining runtime and side-effect boundaries.

Canonical markers:

```text
BEO_PUBLICATION_PILOT_APPROVAL_DECISION
BEO_PUBLICATION_PILOT_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK085_REQUEST_NOT_EXECUTED
beo_publication_pilot_approval_decision
BEO_PUBLICATION_PILOT_APPROVAL_DECISION_ONLY_NOT_EXECUTION
EXACT_BEO_PUBLICATION_PILOT_EXECUTION_SPRINT_REQUIRED_NOT_RUN
```

BLK-086 consumes:

```text
docs/BLK-085_beo-publication-pilot-execution-request-gate.md
python/beo_publication_pilot_execution_request.py
python/beo_publication_pilot_approval_decision.py
```

It captures a decision package. It does not run a pilot. It does not create runtime published BEO output.

---

## 2. Exact BLK-085 Binding

The BLK-086 decision package is bound to the canonical BLK-085 request:

```text
approval_decision_package_id: BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-001
request_package_id: BEO-PUBLICATION-PILOT-EXECUTION-REQUEST-085-001
request_package_hash: sha256:6dc1b6eac1d85b3a2d3b7c01eb8efa2f3f5ed0f91e04227a3a7b43554271db10
upstream_decision_package_id: BEO-PUBLICATION-DECISION-PACKAGE-083-001
upstream_decision_package_hash: sha256:2abdc185164bfef129f9011f53192e70c8f01af76d00ab0039c6072c4358ff5b
beo_id: BEO-054-001
beo_hash: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
target_id: BEO-PUBLICATION-TARGET-055-001
target_ref: fixture://beo-publication-targets/055/001
pilot_request_id: BEO-PUBLICATION-PILOT-EXECUTION-REQUEST-085-PILOT-001
approval_id: APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001
future_run_id: RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001
```

A submitted request package must recompute to the exact `request_package_hash` and match the canonical BLK-085 fixture fields. A self-consistent forged request package is invalid even when its hash recomputes.

---

## 3. Approval-Decision Contract

A conforming BLK-086 approval-decision package must:

1. select exactly `beo_publication_pilot_approval_decision`;
2. return `BEO_PUBLICATION_PILOT_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK085_REQUEST_NOT_EXECUTED`;
3. record `APPROVED_FOR_ONE_FUTURE_BEO_PUBLICATION_PILOT_EXECUTION_NOT_EXECUTED` as the exact decision result;
4. use exactly `BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-001` as the approval decision package ID;
5. capture exactly `APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001` as the approval ID for the canonical BLK-085 request;
6. reserve, but not consume, `RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001` for a later exact execution sprint;
7. record `EXACT_BEO_PUBLICATION_PILOT_EXECUTION_SPRINT_REQUIRED_NOT_RUN` as the next required authority boundary;
8. keep publication pilot execution and every signer/storage/ledger/rollback/RTM/protected-body/target-repo/source-Git/BEB/BEO-closeout/BLK-test/Codex/BLK-pipe/tooling/isolation side-effect flag false;
9. require exact proof obligations and exact denied authorities with duplicate rejection;
10. fail closed on stale, expired, replayed, forged, mismatched, malformed, retargeted, or schema-expanded packages;
11. recursively reject authority-smuggling strings in caller-controlled identity fields.

---

## 4. Proof Obligations for Any Later Execution Sprint

BLK-086 records approval-decision capture only. A later execution sprint must still satisfy:

```text
BLK085_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND
HUMAN_APPROVAL_DECISION_CAPTURED_FOR_EXACT_REQUEST
APPROVAL_ID_MATCHES_BLK085_FUTURE_APPROVAL_ID
FUTURE_RUN_ID_RESERVED_NOT_CONSUMED
BEO_IDENTITY_AND_HASH_BOUND
PUBLICATION_TARGET_IDENTITY_BOUND_WITHOUT_WRITE
SIGNER_STORAGE_LEDGER_ROLLBACK_POLICIES_BOUND_WITHOUT_SIDE_EFFECTS
RTM_AND_DRIFT_AUTHORITIES_EXCLUDED
PROTECTED_BODY_NO_READ_GUARANTEE_BOUND
NEXT_EXECUTION_SPRINT_REQUIRED_BEFORE_ANY_PUBLICATION_PILOT_RUN
HOSTILE_REVIEW_REQUIRED_BEFORE_PUBLICATION_PILOT_EXECUTION
```

A package that omits or duplicates any obligation is not decision-ready.

---

## 5. Denied Authority Markers

BLK-086 pins this denial surface for this sprint:

```text
NO_PUBLICATION_PILOT_EXECUTION_PERFORMED_BY_BLK_SYSTEM_086
NO_RUNTIME_PUBLISHED_BEO_OUTPUT
NO_LIVE_EXTERNAL_PUBLICATION_APPROVAL_CAPTURE
NO_APPROVAL_RETARGETING_OR_SCOPE_EXPANSION
NO_FUTURE_RUN_ID_CONSUMPTION
NO_SIGNER_KEY_MATERIAL_ACCESS
NO_CRYPTOGRAPHIC_SIGNING_AUTHORITY
NO_IMMUTABLE_STORAGE_WRITE_AUTHORITY
NO_PUBLIC_LEDGER_APPEND_OR_MUTATION_AUTHORITY
NO_ROLLBACK_REVOCATION_OR_SUPERSESSION_EXECUTION_AUTHORITY
NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY
NO_ACTIVE_VAULT_HASH_COMPARISON_OR_COVERAGE_CLAIM_AUTHORITY
NO_PROTECTED_BLK_REQ_BODY_READS
NO_TARGET_REPO_SCAN_OR_MUTATION_AUTHORITY
NO_SOURCE_OR_GIT_MUTATION_AUTHORITY
NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_EXECUTION_AUTHORITY
NO_BLK_PIPE_BLK_TEST_OR_CODEX_RUNTIME_AUTHORITY
NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY
NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM
```

These are boundaries for BLK-SYSTEM-086. They do not cancel the captured approval decision; they prevent this sprint from laundering the decision into runtime side effects.

---

## 6. Separation from Adjacent Frontiers

BLK-086 selects the BEO publication pilot approval-decision frontier only. It does not select:

- publication pilot execution;
- signer, storage, ledger, rollback, revocation, or supersession execution;
- RTM generation or drift rejection;
- bounded BLK-test evidence refresh;
- Codex L3 smoke;
- target-repo scan or mutation;
- BEB dispatch;
- BEO closeout execution.

Those remain separate explicit operator decisions and sprint scopes.

---

## 7. Implementation and Tests

BLK-SYSTEM-086 implementation is limited to:

```text
docs/BLK-086_beo-publication-pilot-approval-decision.md
python/beo_publication_pilot_approval_decision.py
python/test_beo_publication_pilot_approval_decision.py
python/test_active_doctrine_review_gates.py
```

The fixture is deterministic and local. It evaluates submitted dictionaries only and never performs runtime publication or external operations.

Persistent doctrine gate marker: BLK-SYSTEM-086 pins BEO publication pilot approval decision as exact request-bound approval capture, not execution

---

## 8. Stop Conditions

Stop and require a new explicit human decision if any future change attempts to treat BLK-086, a BLK-086 PASSing fixture, BLK-085, BLK-083, BLK-060, BLK-057, BLK-077, BLK-079, BLK-084, an approval-decision package, an approval envelope, a decision package, or a request package as sufficient authority for publication pilot execution, runtime `PUBLISHED` BEO output, live external approval-system integration, signer key access, cryptographic signing, immutable storage writes, public ledger mutation, rollback, revocation, supersession, RTM generation, drift rejection, protected-body reads, BLK-test runtime, Codex execution, BLK-pipe execution, BEB dispatch, BEO closeout execution, target-repo scanning, target-repo mutation, source/Git mutation, package/network/model/browser/cyber tooling, or production isolation claims.
