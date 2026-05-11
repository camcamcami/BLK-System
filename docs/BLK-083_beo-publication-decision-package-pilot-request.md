# BLK-083 — BEO Publication Decision Package / Pilot Request

**Status:** Active L0/L1 BEO publication decision-package boundary — deterministic human-review fixture and doctrine gate only; not publication approval and not publication authority
**Scope:** BLK-SYSTEM-083 selected the post-BLK-SYSTEM-082 BEO Publication Decision Package / Pilot Request frontier. It packages existing BLK-057 and BLK-060 publication-readiness surfaces into a review-only decision package and preserves every adjacent authority denial.

---

## 1. Purpose

BLK-083 records the BLK-SYSTEM-083 boundary for a BEO Publication Decision Package / Pilot Request. The purpose is to make the next publication-pilot decision explicit, hash-bound, and reviewable without turning a request package into approval or execution.

Canonical marker:

```text
BEO_PUBLICATION_DECISION_PACKAGE_PILOT_REQUEST
BEO_PUBLICATION_DECISION_PACKAGE_READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PUBLISHED
beo_publication_pilot_request
FUTURE_EXPLICIT_HUMAN_PUBLICATION_PILOT_APPROVAL_REQUIRED_NOT_GRANTED
BEO_PUBLICATION_DECISION_PACKAGE_ONLY_NOT_PUBLICATION_APPROVAL
```

BLK-083 consumes the existing readiness chain:

```text
docs/BLK-057_authoritative-beo-publication-authority-request-boundary.md
docs/BLK-060_authoritative-beo-publication-approval-envelope-boundary.md
python/beo_publication_decision_package.py
```

It does not consume approval. It does not run a pilot. It does not create published BEO output.

---

## 2. Current Runtime Boundary

The current BEO publication path remains review-only and fixture-only:

```text
beo_publication: "DECISION_PACKAGE_ONLY_NOT_APPROVED_NOT_PUBLISHED"
rtm_status: "NOT_GENERATED"
publication_performed: false
approval_granted: false
publication_approved: false
pilot_execution_authorized: false
```

The deterministic fixture in `python/beo_publication_decision_package.py` accepts caller-supplied approval-envelope and decision-request dictionaries, validates them, and returns a local review package. It does not read files, scan a target repository, invoke a subprocess, invoke BLK-test, invoke Codex, invoke BLK-pipe, access network/tooling services, or mutate any external state.

---

## 3. Required Upstream Binding

A valid BLK-083 decision package must bind all of the following from the submitted BLK-060 envelope:

- approval envelope ID and canonical envelope hash;
- BEO ID and BEO hash;
- publication target ID;
- candidate ID;
- source evidence hash;
- trace artifacts with canonical version hashes;
- pilot ID, run ID, and approval ID as review package inputs only;
- signer, storage, ledger, rollback, audit, and pilot-control policies as no-side-effect contracts;
- exact denied-authority set inherited from the envelope plus the BLK-083 decision-package denial surface.

The submitted envelope hash must be recomputed from the submitted envelope body. A caller-supplied hash is not trusted if the body does not match.

---

## 4. Decision Package Contract

BLK-083 packages a future human decision request. A conforming package must:

1. select exactly `beo_publication_pilot_request`;
2. return `BEO_PUBLICATION_DECISION_PACKAGE_READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PUBLISHED`;
3. record `FUTURE_EXPLICIT_HUMAN_PUBLICATION_PILOT_APPROVAL_REQUIRED_NOT_GRANTED` as the next required authority;
4. keep `approval_granted`, `publication_approved`, and `pilot_execution_authorized` false;
5. keep every publication, signer, storage, ledger, rollback, RTM, protected-body, BLK-test, Codex, BLK-pipe, target-repo, tooling, and production-isolation side-effect flag false;
6. require exact proof obligations and exact denied authorities with duplicate rejection;
7. fail closed on stale, expired, replayed, forged, mismatched, malformed, or schema-expanded packages;
8. recursively reject authority-smuggling keys or strings in allowed nested structures.

---

## 5. Proof Obligations for Any Later Publication Pilot

BLK-083 does not satisfy these obligations; it records that any later sprint requesting actual pilot execution must satisfy them separately:

- `APPROVAL_ENVELOPE_IDENTITY_AND_HASH_BOUND`
- `BEO_IDENTITY_AND_HASH_BOUND`
- `PUBLICATION_TARGET_IDENTITY_BOUND_WITHOUT_WRITE`
- `SIGNER_POLICY_WITHOUT_KEY_MATERIAL_BOUND`
- `STORAGE_POLICY_WITHOUT_IMMUTABLE_WRITE_BOUND`
- `LEDGER_POLICY_WITHOUT_APPEND_BOUND`
- `ROLLBACK_REVOCATION_SUPERSESSION_POLICY_WITHOUT_EXECUTION_BOUND`
- `AUDIT_BUNDLE_HASH_BOUND`
- `FRESH_APPROVAL_ID_AND_RUN_ID_REQUIRED_FOR_FUTURE_PILOT`
- `REPLAY_EXPIRY_AND_OPERATOR_STOP_CONTROLS_REQUIRED`
- `RTM_AND_DRIFT_AUTHORITIES_EXCLUDED`
- `PROTECTED_BODY_NO_READ_GUARANTEE_REQUIRED`
- `HOSTILE_REVIEW_REQUIRED_BEFORE_PUBLICATION_PILOT`

A package that omits or duplicates any obligation is not review-ready.

---

## 6. Explicit Denied Authority Markers

BLK-083 pins the following denial surface:

```text
NO_ACTUAL_AUTHORITATIVE_BEO_PUBLICATION_AUTHORITY
NO_PUBLICATION_APPROVAL_GRANTED
NO_PUBLICATION_PILOT_EXECUTION_AUTHORITY
NO_RUNTIME_PUBLISHED_BEO_OUTPUT
NO_LIVE_PUBLICATION_APPROVAL_CAPTURE
NO_SIGNER_KEY_MATERIAL_ACCESS
NO_CRYPTOGRAPHIC_SIGNING_AUTHORITY
NO_IMMUTABLE_STORAGE_WRITE_AUTHORITY
NO_PUBLIC_LEDGER_APPEND_OR_MUTATION_AUTHORITY
NO_ROLLBACK_REVOCATION_OR_SUPERSESSION_EXECUTION_AUTHORITY
NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY
NO_ACTIVE_VAULT_HASH_COMPARISON_OR_COVERAGE_CLAIM_AUTHORITY
NO_PROTECTED_BLK_REQ_BODY_READS
NO_TARGET_REPO_SCAN_OR_MUTATION_AUTHORITY
NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_EXECUTION_AUTHORITY
NO_BLK_PIPE_BLK_TEST_OR_CODEX_RUNTIME_AUTHORITY
NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY
NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM
```

These are negative boundaries, not escalation steps.

---

## 7. Separation from Adjacent Frontiers

BLK-083 selects the BEO publication decision-package frontier only. It does not select:

- bounded BLK-test evidence refresh;
- Codex L3 synthetic smoke;
- RTM authority request;
- target-repo mutation governance;
- BEO closeout execution;
- actual publication pilot execution.

Those remain separate explicit operator decisions. A green BLK-083 fixture or doctrine gate cannot be reused as approval for any adjacent frontier.

---

## 8. Implementation and Tests

BLK-SYSTEM-083 implementation is limited to:

```text
docs/BLK-083_beo-publication-decision-package-pilot-request.md
python/beo_publication_decision_package.py
python/test_beo_publication_decision_package.py
python/test_active_doctrine_review_gates.py
```

The fixture is deterministic and local. It evaluates submitted dictionaries only and never performs runtime publication or external operations.

Persistent doctrine gate marker: BLK-SYSTEM-083 pins BEO publication decision package as L0/L1 human-review request scope

---

## 9. Stop Conditions

Stop and require a new explicit human decision if any future change attempts to treat BLK-083, a BLK-083 PASSing fixture, BLK-057, BLK-060, BLK-077, BLK-079, BLK-081, BLK-082, an approval envelope, or a decision package as sufficient authority for publication, live approval capture, publication pilot execution, signing, immutable storage, public ledger mutation, rollback, revocation, supersession, RTM generation, drift rejection, protected-body reads, BLK-test runtime, Codex execution, BLK-pipe execution, BEB dispatch, BEO closeout execution, target-repo scanning, target-repo mutation, package/network/model/browser/cyber tooling, or production isolation claims.
