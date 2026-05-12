# BLK-085 — BEO Publication Pilot Execution Request Gate

**Status:** Active L0/L1 request-gate boundary — explicit human-approval request only; not publication approval and not publication execution
**Scope:** BLK-SYSTEM-085 selects the post-BLK-SYSTEM-084 `beo_publication_pilot_execution_request` frontier as a deterministic request-gate fixture. It converts BLK-083 decision-package evidence into a future human-approval request package without approving or executing a publication pilot.

---

## 1. Purpose

BLK-085 records the BLK-SYSTEM-085 boundary for a BEO Publication Pilot Execution Request Gate. The purpose is to make the next BEO publication pilot decision exact, hash-bound, reviewable, and hostile-auditable without turning a request into approval or publication.

Canonical markers:

```text
BEO_PUBLICATION_PILOT_EXECUTION_REQUEST_GATE
BEO_PUBLICATION_PILOT_EXECUTION_REQUEST_READY_FOR_EXPLICIT_HUMAN_APPROVAL_NOT_EXECUTED
beo_publication_pilot_execution_request
EXPLICIT_HUMAN_PUBLICATION_PILOT_APPROVAL_REQUIRED_NOT_GRANTED
BEO_PUBLICATION_PILOT_EXECUTION_REQUEST_GATE_ONLY_NOT_APPROVAL_NOT_EXECUTION
```

BLK-085 consumes the current review-only readiness chain:

```text
docs/BLK-083_beo-publication-decision-package-pilot-request.md
python/beo_publication_decision_package.py
python/beo_publication_pilot_execution_request.py
```

It does not consume approval. It does not run a pilot. It does not create published BEO output.

---

## 2. Current Runtime Boundary

The current BEO publication path remains request-only and fixture-only:

```text
request_status: "BEO_PUBLICATION_PILOT_EXECUTION_REQUEST_READY_FOR_EXPLICIT_HUMAN_APPROVAL_NOT_EXECUTED"
beo_publication: "PILOT_EXECUTION_REQUEST_ONLY_NOT_APPROVED_NOT_PUBLISHED"
rtm_status: "NOT_GENERATED"
approval_granted: false
publication_approved: false
pilot_execution_authorized: false
publication_performed: false
```

The deterministic fixture in `python/beo_publication_pilot_execution_request.py` accepts caller-supplied BLK-083 decision-package and execution-request dictionaries, validates them, and returns a local request package. It does not read files, scan a target repository, invoke a subprocess, invoke BLK-test, invoke Codex, invoke BLK-pipe, access network/tooling services, or mutate any external state.

---

## 3. Required Upstream Binding

A valid BLK-085 request package must bind all of the following from the submitted BLK-083 decision package:

- upstream decision package ID and canonical decision package hash;
- envelope ID and canonical envelope hash;
- BEO ID and BEO hash;
- publication target ID and target reference;
- source evidence hash;
- trace artifacts with canonical version hashes;
- signer, storage, ledger, rollback, audit, and pilot-control policy hashes;
- upstream pilot request ID and upstream future approval/run ID candidates;
- exact denied-authority set inherited from the decision package plus BLK-085 request-gate denial surface.

The submitted decision-package hash must be recomputed from the submitted decision-package body. A caller-supplied hash is not trusted if the body does not match.

---

## 4. Request Gate Contract

BLK-085 packages a future human decision request. A conforming package must:

1. select exactly `beo_publication_pilot_execution_request`;
2. return `BEO_PUBLICATION_PILOT_EXECUTION_REQUEST_READY_FOR_EXPLICIT_HUMAN_APPROVAL_NOT_EXECUTED`;
3. record `EXPLICIT_HUMAN_PUBLICATION_PILOT_APPROVAL_REQUIRED_NOT_GRANTED` as the next required authority;
4. keep `approval_granted`, `publication_approved`, `pilot_execution_authorized`, and `publication_performed` false;
5. keep every publication, signer, storage, ledger, rollback, RTM, protected-body, BLK-test, Codex, BLK-pipe, target-repo, source/Git, tooling, and production-isolation side-effect flag false;
6. require fresh future approval/run IDs that do not reuse upstream BLK-083 decision-package IDs;
7. require exact proof obligations and exact denied authorities with duplicate rejection;
8. fail closed on stale, expired, replayed, forged, mismatched, malformed, or schema-expanded packages;
9. recursively reject authority-smuggling keys or strings in allowed request structures.

---

## 5. Proof Obligations for Any Later Publication Pilot Approval

BLK-085 does not satisfy these obligations as approval; it records that any later sprint granting actual pilot authority must satisfy them separately:

```text
UPSTREAM_DECISION_PACKAGE_IDENTITY_AND_HASH_BOUND
BEO_IDENTITY_AND_HASH_BOUND
PUBLICATION_TARGET_IDENTITY_BOUND_WITHOUT_WRITE
FRESH_APPROVAL_ID_AND_RUN_ID_RESERVED_FOR_FUTURE_APPROVAL
EXPLICIT_HUMAN_APPROVAL_REQUIRED_BEFORE_ANY_PILOT_EXECUTION
SIGNER_STORAGE_LEDGER_ROLLBACK_POLICIES_BOUND_WITHOUT_EXECUTION
REPLAY_EXPIRY_AND_OPERATOR_STOP_CONTROLS_BOUND
RTM_AND_DRIFT_AUTHORITIES_EXCLUDED
PROTECTED_BODY_NO_READ_GUARANTEE_BOUND
HOSTILE_REVIEW_REQUIRED_BEFORE_ANY_PUBLICATION_PILOT_EXECUTION
```

A package that omits or duplicates any obligation is not review-ready.

---

## 6. Explicit Denied Authority Markers

BLK-085 pins the following denial surface:

```text
NO_PUBLICATION_APPROVAL_GRANTED
NO_PUBLICATION_PILOT_EXECUTION_PERFORMED
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

BLK-085 selects the BEO publication pilot execution request frontier only. It does not select:

- bounded BLK-test evidence refresh;
- Codex L3 synthetic smoke;
- RTM authority request;
- target-repo mutation governance;
- BEB dispatch;
- BEO closeout execution;
- actual publication pilot execution.

Those remain separate explicit operator decisions. A green BLK-085 fixture or doctrine gate cannot be reused as approval for any adjacent frontier.

---

## 8. Implementation and Tests

BLK-SYSTEM-085 implementation is limited to:

```text
docs/BLK-085_beo-publication-pilot-execution-request-gate.md
python/beo_publication_pilot_execution_request.py
python/test_beo_publication_pilot_execution_request.py
python/test_active_doctrine_review_gates.py
```

The fixture is deterministic and local. It evaluates submitted dictionaries only and never performs runtime publication or external operations.

Persistent doctrine gate marker: BLK-SYSTEM-085 pins BEO publication pilot execution request as request-only and non-runtime

---

## 9. Stop Conditions

Stop and require a new explicit human decision if any future change attempts to treat BLK-085, a BLK-085 PASSing fixture, BLK-083, BLK-060, BLK-057, BLK-077, BLK-079, BLK-084, an approval envelope, a decision package, or a request package as sufficient authority for publication approval, live approval capture, publication pilot execution, signing, immutable storage, public ledger mutation, rollback, revocation, supersession, RTM generation, drift rejection, protected-body reads, BLK-test runtime, Codex execution, BLK-pipe execution, BEB dispatch, BEO closeout execution, target-repo scanning, target-repo mutation, source/Git mutation, package/network/model/browser/cyber tooling, or production isolation claims.
