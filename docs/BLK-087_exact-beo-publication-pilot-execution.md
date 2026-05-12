# BLK-087 — Exact BEO Publication Pilot Execution

**Status:** Active exact local publication-pilot execution boundary — one BLK-086-bound pilot executed locally; not external authoritative publication and not RTM authority
**Scope:** BLK-SYSTEM-087 consumes the canonical BLK-086 approval-decision package and records one deterministic local BEO publication pilot execution for `BEO-054-001`. It emits a hash-bound local pilot publication artifact. It does not perform external authoritative publication, signer key access, cryptographic signing, immutable storage writes, public ledger mutation, rollback, revocation, supersession, RTM generation, protected-body reads, target-repo scan/mutation, BLK-test/Codex/BLK-pipe runtime, package/network/model/browser/cyber tooling, or production isolation.

---

## 1. Purpose

BLK-087 records the BLK-SYSTEM-087 boundary for exact BEO publication pilot execution. The purpose is to consume the reserved BLK-086 run ID in a deterministic local fixture and prove one bounded publication-pilot output shape while preserving all adjacent authority boundaries.

Canonical markers:

```text
EXACT_BEO_PUBLICATION_PILOT_EXECUTION
BEO_PUBLICATION_PILOT_EXECUTED_FOR_EXACT_BLK086_APPROVAL_LOCAL_ONLY
exact_beo_publication_pilot_execution
EXACT_BEO_PUBLICATION_PILOT_EXECUTION_LOCAL_ONLY_NO_SIGNER_STORAGE_LEDGER_RTM
PILOT_LOCAL_PUBLISHED_BEO_OUTPUT_NOT_AUTHORITATIVE
RTM_AUTHORITY_REQUEST_AFTER_PUBLISHED_BEO_PREREQUISITES_NOT_GRANTED
```

BLK-087 consumes:

```text
docs/BLK-086_beo-publication-pilot-approval-decision.md
python/beo_publication_pilot_approval_decision.py
python/beo_publication_pilot_execution.py
```

It executes one local pilot fixture. It does not publish to an external authoritative target, sign artifacts, write immutable storage, append ledgers, execute rollback/revocation/supersession, generate RTM, or read protected bodies.

---

## 2. Exact BLK-086 Binding

The BLK-087 execution package is bound to the canonical BLK-086 approval-decision package:

```text
execution_package_id: BEO-PUBLICATION-PILOT-EXECUTION-087-001
approval_decision_package_id: BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-001
approval_decision_package_hash: sha256:2ade9eee61d5688c32f12cf9bec1a2668d03f091d1a14fb6eeef1c7f2f1a54b9
approval_decision_status: BEO_PUBLICATION_PILOT_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK085_REQUEST_NOT_EXECUTED
request_package_id: BEO-PUBLICATION-PILOT-EXECUTION-REQUEST-085-001
request_package_hash: sha256:6dc1b6eac1d85b3a2d3b7c01eb8efa2f3f5ed0f91e04227a3a7b43554271db10
upstream_decision_package_id: BEO-PUBLICATION-DECISION-PACKAGE-083-001
upstream_decision_package_hash: sha256:2abdc185164bfef129f9011f53192e70c8f01af76d00ab0039c6072c4358ff5b
beo_id: BEO-054-001
beo_hash: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
target_id: BEO-PUBLICATION-TARGET-055-001
target_ref: fixture://beo-publication-targets/055/001
approval_id: APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001
run_id_consumed: RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001
```

A submitted approval-decision package must recompute to its own `approval_decision_package_hash` and match the canonical BLK-086 fixture fields. A self-consistent forged approval-decision package is invalid even when its hash recomputes.

---

## 3. Execution Contract

A conforming BLK-087 execution package must:

1. select exactly `exact_beo_publication_pilot_execution`;
2. return `BEO_PUBLICATION_PILOT_EXECUTED_FOR_EXACT_BLK086_APPROVAL_LOCAL_ONLY`;
3. use exactly `BEO-PUBLICATION-PILOT-EXECUTION-087-001` as the execution package ID;
4. consume exactly `RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001` for this deterministic local fixture package;
5. bind exactly `APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001`, `BEO-054-001`, the BEO hash, target ID/ref, source evidence hash, trace artifacts, and signer/storage/ledger/rollback/audit policy hashes;
6. emit `PILOT_LOCAL_PUBLISHED_BEO_OUTPUT_NOT_AUTHORITATIVE` as the local pilot BEO publication state;
7. emit `RTM_AUTHORITY_REQUEST_AFTER_PUBLISHED_BEO_PREREQUISITES_NOT_GRANTED` as the next authority boundary;
8. keep external authoritative publication, live approval capture, signer/storage/ledger/rollback/RTM/protected-body/target-repo/source-Git/BEB/BEO-closeout/BLK-test/Codex/BLK-pipe/tooling/isolation side-effect flags false;
9. require exact proof obligations and exact denied authorities with duplicate rejection;
10. fail closed on stale, expired, replayed, forged, mismatched, malformed, retargeted, or schema-expanded packages;
11. reject authority-smuggling strings in caller-controlled identity fields.

Execution proof obligations pinned by the fixture:

```text
BLK086_APPROVAL_DECISION_IDENTITY_AND_HASH_BOUND
APPROVAL_ID_MATCHES_BLK086_CAPTURED_APPROVAL
RUN_ID_MATCHES_BLK086_RESERVED_RUN_ID_AND_CONSUMED_ONCE
BEO_IDENTITY_AND_HASH_BOUND
PUBLICATION_TARGET_IDENTITY_BOUND_WITHOUT_EXTERNAL_WRITE
LOCAL_PILOT_PUBLICATION_ARTIFACT_HASH_BOUND
SIGNER_STORAGE_LEDGER_ROLLBACK_POLICIES_BOUND_WITHOUT_SIDE_EFFECTS
RTM_AND_DRIFT_AUTHORITIES_EXCLUDED
PROTECTED_BODY_NO_READ_GUARANTEE_BOUND
TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED
HOSTILE_REVIEW_REQUIRED_AFTER_PUBLICATION_PILOT_EXECUTION
```

---

## 4. Local Pilot Publication Artifact

The deterministic local artifact is a receipt-like fixture only:

```text
publication_mode: LOCAL_DETERMINISTIC_PILOT_ONLY
published_beo_id: BEO-054-001
signature_status: NOT_SIGNED_NO_KEY_MATERIAL
storage_status: NOT_WRITTEN_LOCAL_RECEIPT_ONLY
ledger_status: NOT_APPENDED_LOCAL_RECEIPT_ONLY
rollback_status: NOT_EXECUTED_POLICY_BOUND_ONLY
rtm_status: NOT_GENERATED
```

The artifact is hash-bound by `pilot_publication_artifact_hash`, and the enclosing package is hash-bound by `execution_package_hash`.

---

## 5. Proof Obligations for Any Later RTM Authority Request

BLK-087 records a local publication-pilot artifact only. A later RTM authority request must still satisfy:

```text
PUBLISHED_BEO_PILOT_ARTIFACT_IDENTITY_AND_HASH_BOUND
BEO_IDENTITY_AND_HASH_BOUND
PUBLICATION_TARGET_IDENTITY_BOUND_WITHOUT_EXTERNAL_WRITE
SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED
RTM_AUTHORITY_SEPARATELY_REQUESTED_NOT_GRANTED_BY_PILOT
PROTECTED_BODY_NO_READ_GUARANTEE_BOUND
TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED
HOSTILE_REVIEW_REQUIRED_BEFORE_RTM_AUTHORITY_REQUEST
```

A local pilot output does not grant RTM generation, RTM drift rejection, active-vault hash comparison, coverage matrices, coverage claims, or protected-body reads.

---

## 6. Denied Authority Markers

BLK-087 pins this denial surface for this sprint:

```text
NO_AUTHORITATIVE_EXTERNAL_BEO_PUBLICATION_BY_BLK_SYSTEM_087
NO_LIVE_EXTERNAL_PUBLICATION_APPROVAL_CAPTURE
NO_APPROVAL_RETARGETING_OR_SCOPE_EXPANSION
NO_SIGNER_KEY_MATERIAL_ACCESS
NO_CRYPTOGRAPHIC_SIGNING_AUTHORITY
NO_IMMUTABLE_STORAGE_WRITE_AUTHORITY
NO_PUBLIC_LEDGER_APPEND_OR_MUTATION_AUTHORITY
NO_ROLLBACK_REVOCATION_OR_SUPERSESSION_EXECUTION_AUTHORITY
NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY
NO_ACTIVE_VAULT_HASH_COMPARISON_OR_COVERAGE_CLAIM_AUTHORITY
NO_PROTECTED_BLK_REQ_BODY_READS
NO_TARGET_REPO_SCAN_OR_MUTATION_AUTHORITY
NO_SOURCE_OR_GIT_MUTATION_BY_FIXTURE
NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_EXECUTION_AUTHORITY
NO_BLK_PIPE_BLK_TEST_OR_CODEX_RUNTIME_AUTHORITY
NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY
NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM
```

These denial markers do not cancel the exact local pilot execution. They prevent the local pilot from laundering itself into external publication, RTM, trace closure, target-repo work, or production authority.

---

## 7. Separation from Adjacent Frontiers

BLK-087 selects the exact local BEO publication pilot execution frontier only. It does not select:

- external authoritative publication;
- live external approval capture;
- signer, storage, ledger, rollback, revocation, or supersession execution;
- RTM generation or drift rejection;
- bounded BLK-test evidence refresh;
- Codex L3 smoke;
- target-repo scan or mutation;
- BEB dispatch;
- BEO closeout execution.

Those remain separate explicit operator decisions and sprint scopes.

---

## 8. Implementation and Tests

BLK-SYSTEM-087 implementation is limited to:

```text
docs/BLK-087_exact-beo-publication-pilot-execution.md
python/beo_publication_pilot_execution.py
python/test_beo_publication_pilot_execution.py
python/test_active_doctrine_review_gates.py
```

The fixture is deterministic and local. It evaluates submitted dictionaries only and never performs external publication or runtime operations.

Persistent doctrine gate marker: BLK-SYSTEM-087 pins exact BEO publication pilot execution as local-only and no-adjacent-authority

---

## 9. Stop Conditions

Stop and require a new explicit human decision if any future change attempts to treat BLK-087, a BLK-087 PASSing fixture, the local pilot artifact, BLK-086, BLK-085, BLK-083, BLK-060, BLK-057, BLK-077, BLK-079, an execution package, an approval-decision package, an approval envelope, a decision package, or a request package as sufficient authority for external authoritative publication, live approval capture, signer key access, cryptographic signing, immutable storage writes, public ledger mutation, rollback, revocation, supersession, RTM generation, drift rejection, protected-body reads, BLK-test runtime, Codex execution, BLK-pipe execution, BEB dispatch, BEO closeout execution, target-repo scanning, target-repo mutation, source/Git mutation, package/network/model/browser/cyber tooling, or production isolation claims.
