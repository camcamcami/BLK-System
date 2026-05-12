# BLK-088 — RTM Authority Request After Local BEO Pilot Prerequisites

**Status:** Active RTM authority request boundary — review package only; not RTM generation authority
**Scope:** BLK-SYSTEM-088 packages the BLK-SYSTEM-087 local BEO publication-pilot execution evidence into a deterministic RTM authority request for human review. It does not grant human RTM approval, generate RTM, reject drift, compare active-vault hashes, create coverage matrices, read protected BLK-req bodies, perform external authoritative BEO publication, access signer key material, sign, write storage, append ledgers, execute rollback/revocation/supersession, scan or mutate target repositories, mutate source/Git, dispatch BEB/BEO closeout, run BLK-pipe/BLK-test/Codex, use package/network/model/browser/cyber tooling, or claim production isolation.

---

## 1. Purpose

BLK-088 records the BLK-SYSTEM-088 boundary for requesting, but not granting, future exact RTM generation authority after the local BLK-SYSTEM-087 BEO publication-pilot prerequisites were packaged.

Canonical markers:

```text
RTM_AUTHORITY_REQUEST_AFTER_LOCAL_BEO_PILOT_PREREQUISITES
RTM_AUTHORITY_REQUEST_READY_AFTER_LOCAL_BEO_PILOT_PREREQUISITES_NOT_GRANTED
rtm_authority_request_after_local_beo_pilot_prerequisites
RTM_AUTHORITY_REQUEST_AFTER_LOCAL_BEO_PILOT_PREREQUISITES_REVIEW_ONLY
EXPLICIT_HUMAN_RTM_GENERATION_APPROVAL_REQUIRED_NOT_GRANTED
REQUEST_ONLY_NOT_GRANTED
```

BLK-088 consumes:

```text
docs/BLK-087_exact-beo-publication-pilot-execution.md
python/beo_publication_pilot_execution.py
python/rtm_authority_request_after_beo_pilot.py
```

It emits a request package only. It does not generate RTM, decide drift, compare active-vault hashes, create coverage matrices, or read protected bodies.

---

## 2. Exact BLK-087 Binding

The BLK-088 authority request package is bound to the canonical BLK-087 local pilot execution package:

```text
authority_request_package_id: RTM-AUTHORITY-REQUEST-AFTER-BEO-PILOT-088-001
upstream_execution_package_id: BEO-PUBLICATION-PILOT-EXECUTION-087-001
upstream_execution_status: BEO_PUBLICATION_PILOT_EXECUTED_FOR_EXACT_BLK086_APPROVAL_LOCAL_ONLY
approval_decision_package_id: BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-001
approval_decision_package_hash: sha256:2ade9eee61d5688c32f12cf9bec1a2668d03f091d1a14fb6eeef1c7f2f1a54b9
approval_id: APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001
run_id_consumed: RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001
beo_id: BEO-054-001
beo_hash: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
target_id: BEO-PUBLICATION-TARGET-055-001
target_ref: fixture://beo-publication-targets/055/001
local_pilot_beo_publication: PILOT_LOCAL_PUBLISHED_BEO_OUTPUT_NOT_AUTHORITATIVE
rtm_authority: REQUEST_ONLY_NOT_GRANTED
```

A submitted BLK-087 execution package must recompute to its own `execution_package_hash` and must match the canonical local pilot fixture fields. A self-consistent forged execution package is invalid even when its hash recomputes.

---

## 3. Request Contract

A conforming BLK-088 request package must:

1. select exactly `rtm_authority_request_after_local_beo_pilot_prerequisites`;
2. return `RTM_AUTHORITY_REQUEST_READY_AFTER_LOCAL_BEO_PILOT_PREREQUISITES_NOT_GRANTED`;
3. use exactly `RTM-AUTHORITY-REQUEST-AFTER-BEO-PILOT-088-001` as the authority request package ID;
4. bind exactly the BLK-087 execution package ID/hash and the local pilot publication artifact hash;
5. disclose that the BLK-087 local artifact is `PILOT_LOCAL_PUBLISHED_BEO_OUTPUT_NOT_AUTHORITATIVE` and not external authoritative publication;
6. set `REQUEST_ONLY_NOT_GRANTED` and `EXPLICIT_HUMAN_RTM_GENERATION_APPROVAL_REQUIRED_NOT_GRANTED`;
7. keep RTM generation, drift rejection, drift decision, active-vault hash comparison, coverage matrix, coverage claim, protected-body read, publication, signer, storage, ledger, rollback, target-repo, source/Git, BEB/BEO closeout, BLK-pipe, BLK-test, Codex, tooling, and isolation side-effect flags false;
8. require exact proof obligations and exact denied authorities with duplicate rejection;
9. fail closed on stale, expired, replayed, forged, mismatched, malformed, retargeted, or schema-expanded packages;
10. reject authority-smuggling strings in caller-controlled identity fields.

Proof obligations pinned by the fixture:

```text
BLK087_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND
BLK087_LOCAL_PILOT_STATUS_BOUND
PILOT_PUBLICATION_ARTIFACT_IDENTITY_AND_HASH_BOUND
BEO_IDENTITY_AND_HASH_BOUND
PUBLICATION_TARGET_IDENTITY_BOUND_WITHOUT_EXTERNAL_WRITE
LOCAL_PILOT_ONLY_NOT_EXTERNAL_AUTHORITATIVE_PUBLICATION_DISCLOSED
RTM_AUTHORITY_REQUESTED_FOR_REVIEW_NOT_GRANTED
RTM_GENERATION_AND_DRIFT_AUTHORITIES_EXCLUDED_UNTIL_FUTURE_APPROVAL
ACTIVE_VAULT_HASH_COMPARISON_AND_COVERAGE_CLAIMS_EXCLUDED
PROTECTED_BODY_NO_READ_GUARANTEE_BOUND
SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED
TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED
HOSTILE_REVIEW_REQUIRED_BEFORE_ANY_RTM_GENERATION
```

---

## 4. Denied Authority Markers

BLK-088 pins this denial surface:

```text
NO_RUNTIME_RTM_GENERATION_BY_BLK_SYSTEM_088
NO_RTM_DRIFT_REJECTION_OR_DRIFT_DECISION_AUTHORITY
NO_ACTIVE_VAULT_HASH_COMPARISON_OR_COVERAGE_CLAIM_AUTHORITY
NO_PROTECTED_BLK_REQ_BODY_READS
NO_AUTHORITATIVE_EXTERNAL_BEO_PUBLICATION_BY_BLK_SYSTEM_088
NO_LIVE_EXTERNAL_PUBLICATION_APPROVAL_CAPTURE
NO_SIGNER_KEY_MATERIAL_ACCESS
NO_CRYPTOGRAPHIC_SIGNING_AUTHORITY
NO_IMMUTABLE_STORAGE_WRITE_AUTHORITY
NO_PUBLIC_LEDGER_APPEND_OR_MUTATION_AUTHORITY
NO_ROLLBACK_REVOCATION_OR_SUPERSESSION_EXECUTION_AUTHORITY
NO_TARGET_REPO_SCAN_OR_MUTATION_AUTHORITY
NO_SOURCE_OR_GIT_MUTATION_BY_FIXTURE
NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_EXECUTION_AUTHORITY
NO_BLK_PIPE_BLK_TEST_OR_CODEX_RUNTIME_AUTHORITY
NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY
NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM
```

These denial markers prevent a request package from laundering itself into runtime RTM generation, trace closure, drift decisions, protected-vault access, external publication, target-repo work, or production authority.

---

## 5. Separation from Adjacent Frontiers

BLK-088 selects the RTM authority request frontier only. It does not select:

- RTM generation;
- RTM drift rejection;
- active-vault hash comparison;
- coverage matrix creation or coverage-claim promotion;
- protected BLK-req body reads;
- external authoritative BEO publication;
- bounded BLK-test evidence refresh;
- Codex L3 smoke;
- target-repo scan or mutation;
- BEB dispatch;
- BEO closeout execution.

Those remain separate explicit operator decisions and sprint scopes.

---

## 6. Implementation and Tests

BLK-SYSTEM-088 implementation is limited to:

```text
docs/BLK-088_rtm-authority-request-after-local-beo-pilot-prerequisites.md
python/rtm_authority_request_after_beo_pilot.py
python/test_rtm_authority_request_after_beo_pilot.py
python/test_active_doctrine_review_gates.py
python/blk_current_state_authority_index.py
python/test_blk_current_state_authority_index.py
```

The fixture is deterministic and local. It evaluates submitted dictionaries only and never performs runtime generation or external operations.

Persistent doctrine gate marker: BLK-SYSTEM-088 pins RTM authority request as review-only and not generation authority

---

## 7. Stop Conditions

Stop and require a new explicit human decision if any future change attempts to treat BLK-088, a BLK-088 PASSing fixture, the request package, BLK-087 local pilot evidence, BLK-086, BLK-085, BLK-083, BLK-077, BLK-079, or any local artifact as sufficient authority for RTM generation, drift rejection, active-vault hash comparison, coverage matrix creation, coverage claims, protected-body reads, external authoritative publication, live approval capture, signer key access, cryptographic signing, immutable storage writes, public ledger mutation, rollback, revocation, supersession, BLK-test runtime, Codex execution, BLK-pipe execution, BEB dispatch, BEO closeout execution, target-repo scanning, target-repo mutation, source/Git mutation, package/network/model/browser/cyber tooling, or production isolation claims.
