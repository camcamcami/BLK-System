# BLK-084 — Post-083 Frontier Selection Gate Refresh

**Status:** Active L0/L1 post-083 frontier-selection gate — review-only; not runtime authority  
**Scope:** BLK-SYSTEM-084 refreshes the historical frontier-selection pattern for the post-BLK-SYSTEM-083 state. It records exact candidate names for future human decisions while preserving every adjacent authority denial.

---

## 1. Purpose

BLK-077, BLK-079, BLK-083, and the BLK-SYSTEM-083 closeout agree that there is no automatic next sprint authority after the BEO Publication Decision Package / Pilot Request. BLK-084 turns that stop condition into a current deterministic selection-gate boundary.

Canonical markers:

```text
BLK_SYSTEM_POST_083_FRONTIER_SELECTION_GATE
POST_083_FRONTIER_SELECTION_READY_FOR_HUMAN_DECISION_NOT_AUTHORITY
POST_083_FRONTIER_SELECTION_BLOCKED_NOT_AUTHORIZED
POST_083_FRONTIER_SELECTION_BLOCKED_PENDING_PUBLICATION_PREREQUISITES
NEXT_LOGICAL_SPRINT_IS_NOT_APPROVAL
NEXT_SPRINT_IS_NOT_APPROVAL
BLK_083_DECISION_PACKAGE_IS_NOT_PUBLICATION_APPROVAL
POST_083_FRONTIER_SELECTION_L0_L1_FIXTURE_ONLY
```

Persistent doctrine gate marker: BLK-SYSTEM-084 pins post-083 frontier selection as review-only and non-runtime.

---

## 2. Current Runtime Boundary

The post-083 selection gate is deterministic local fixture logic only:

```text
selection_status: "BLK_SYSTEM_POST_083_FRONTIER_SELECTION_GATE"
review_status: "POST_083_FRONTIER_SELECTION_READY_FOR_HUMAN_DECISION_NOT_AUTHORITY"
runtime_authority_granted: false
publication_approval_granted: false
publication_pilot_execution_authorized: false
blk_test_runtime_authorized: false
codex_live_dispatch_authorized: false
blk_pipe_dispatch_authorized: false
runtime_rtm_generation_authorized: false
```

The fixture in `python/blk_post083_frontier_selection_gate.py` accepts caller-supplied dictionaries/arguments and returns a local review decision. It does not read files, inspect target repositories, launch subprocesses, start BLK-test, start Codex, dispatch BLK-pipe, call network/model/browser/cyber/package tooling, access signer/storage/ledger/rollback facilities, generate RTM, publish BEOs, or mutate external state.

---

## 3. Exact Candidate Frontiers

A valid post-083 record must name exactly one of these current candidate frontiers:

```text
bounded_blk_test_evidence_refresh
beo_publication_pilot_execution_request
codex_live_dispatch_l3_smoke
rtm_authority_request_after_publication_prerequisites
bounded_consolidation_or_remediation_sprint
```

Any generic string such as `next logical`, `next sprint`, `beo_publication`, `publication_pilot`, `rtm_generation`, or `blk_test_refresh` is blocked. Multiple frontier selections, nested frontier selections, and secondary frontier fields are blocked.

### 3.1 Candidate boundaries

| Candidate | Selection meaning | Still unauthorized |
| --- | --- | --- |
| `bounded_blk_test_evidence_refresh` | A future human may consider exactly one bounded BLK-test evidence refresh. | No BLK-test runtime, production MCP, source/Git mutation, BEO publication, RTM, protected-body reads, or coverage/drift truth. |
| `beo_publication_pilot_execution_request` | A future human may consider actual BEO publication pilot execution under a separate exact approval. | No publication approval capture, no publication pilot execution, no signer/storage/ledger/rollback side effects, no runtime `PUBLISHED` BEO output. |
| `codex_live_dispatch_l3_smoke` | A future human may consider exactly one Codex L3 smoke. | No Codex subprocess, BLK-pipe dispatch, source mutation, package/network/model/browser/cyber tooling, or production isolation claim. |
| `rtm_authority_request_after_publication_prerequisites` | A future human may consider RTM authority only after actual publication prerequisites exist. | No runtime RTM generation, drift rejection, active-vault hash comparison, protected-body reads, or public ledger mutation. |
| `bounded_consolidation_or_remediation_sprint` | A future human may choose another bounded L0/L1 consolidation/remediation task. | No authority jump unless the sprint names an exact approval envelope and authority boundary. |

---

## 4. RTM Publication-Prerequisite Block

`rtm_authority_request_after_publication_prerequisites` is a candidate name, not an available runtime capability. The BLK-084 selection fixture cannot itself prove publication prerequisites and must return `POST_083_FRONTIER_SELECTION_BLOCKED_PENDING_PUBLICATION_PREREQUISITES` for RTM selection. A later authority-specific sprint must provide actual published-BEO/publication evidence, approval identity, and hash-bound prerequisite proof before any RTM authority request can become review-ready.

BLK-083 decision-package readiness is not a published BEO, not publication approval, not signer/storage/ledger/rollback authority, and not RTM input authority.

---

## 5. Explicit Denied Authority Surface

BLK-084 denies all adjacent authority surfaces:

```text
NO_ACTUAL_AUTHORITATIVE_BEO_PUBLICATION_AUTHORITY
NO_PUBLICATION_APPROVAL_CAPTURE
NO_PUBLICATION_PILOT_EXECUTION
NO_RUNTIME_PUBLISHED_BEO_OUTPUT
NO_SIGNER_KEY_MATERIAL_ACCESS
NO_CRYPTOGRAPHIC_SIGNING_AUTHORITY
NO_IMMUTABLE_STORAGE_WRITE_AUTHORITY
NO_PUBLIC_LEDGER_APPEND_OR_MUTATION_AUTHORITY
NO_ROLLBACK_REVOCATION_OR_SUPERSESSION_EXECUTION_AUTHORITY
NO_RUNTIME_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY
NO_ACTIVE_VAULT_HASH_COMPARISON_OR_COVERAGE_CLAIM_AUTHORITY
NO_PROTECTED_BLK_REQ_BODY_READS
NO_TARGET_REPO_SCAN_OR_MUTATION_AUTHORITY
NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_EXECUTION_AUTHORITY
NO_BLK_PIPE_DISPATCH_OR_RUNTIME_AUTHORITY
NO_BLK_TEST_RUNTIME_OR_PRODUCTION_MCP_AUTHORITY
NO_CODEX_LIVE_EXECUTION_AUTHORITY
NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY
NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM
```

Operator shorthand:

- No actual authoritative BEO publication authority.
- No publication approval capture.
- No publication pilot execution.
- No signer key material access or cryptographic signing.
- No immutable storage writes or public ledger mutation.
- No runtime RTM generation or RTM drift rejection.
- No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison.
- No target-repo scan or mutation.
- No BLK-pipe dispatch, BLK-test runtime, production BLK-test MCP, or live Codex execution.
- No package-manager, network, model-service, browser, or cyber tooling authority.
- No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim.

---

## 6. Required Selection-Gate Semantics

The deterministic gate must require:

1. exactly one current post-083 frontier;
2. a fresh selection ID and replay protection inputs;
3. governing documents for the selected frontier;
4. explicit future approval fields;
5. exact excluded adjacent authorities with duplicate rejection;
6. hostile-review checklist markers;
7. disabled activation adapter side-effect flags;
8. recursive key/value/string authority-laundering scans;
9. percent-decoded scan variants for encoded authority terms.

The deterministic gate must reject:

- “next logical sprint” as approval;
- “next sprint” as approval;
- BLK-083 decision package readiness as publication approval;
- BLK-077 or BLK-079 roadmap/index text as runtime approval;
- BLK-048 historical selection readiness as current post-083 approval;
- review-ready, request-ready, fixture-ready, static-profile-ready, disabled-adapter-ready, or hostile-review-ready evidence as activation authority;
- hidden signer/storage/ledger/rollback, target-repo, protected-body, package-manager, network, model-service, browser, cyber, BLK-test, Codex, BLK-pipe, BEO publication, RTM, coverage, drift, sandbox, or host-isolation claims.

---

## 7. Relationship to Existing Boundary Documents

| Surface | Relationship |
| --- | --- |
| BLK-048 | Historical BLK-045-era authority frontier selection gate. BLK-084 refreshes the pattern for post-BLK-SYSTEM-083 and does not inherit BLK-048 activation authority. |
| BLK-077 | Current roadmap selector. BLK-084 implements its post-083 “explicit operator decision” stop condition as a local fixture. |
| BLK-079 | Current-state authority index. BLK-084 remains index/selection evidence only and does not grant runtime authority. |
| BLK-083 | BEO publication decision package / pilot request. BLK-084 can name `beo_publication_pilot_execution_request` for a future decision, but cannot approve or execute it. |
| BLK-001 through BLK-006 | Preserve separation of concerns, BLK-req protected-body isolation, BLK-pipe final mutation authority, trace binding, HITL approval, and no inherited authority across execution/verification/publication/RTM layers. |

---

## 8. Stop Conditions

Pause and require hostile review plus a fresh human decision if any future sprint attempts to:

1. treat BLK-084, BLK-077, BLK-079, BLK-083, BLK-048, or a selection fixture as publication approval or runtime authority;
2. execute or approve more than one frontier in one sprint;
3. execute actual publication pilot behavior without separate publication approval and signer/storage/ledger/rollback boundary proof;
4. generate RTM from request-only or fixture-only publication evidence;
5. run BLK-test, Codex, BLK-pipe, package-manager, network, model-service, browser, or cyber tooling from selection-gate code;
6. read, copy, parse, hash, summarize, scan, mutate, or compare protected BLK-req bodies;
7. scan or mutate target repositories from selection-gate code;
8. claim production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret isolation from selection evidence.

---

## 9. Final Boundary Thesis

BLK-084 makes the post-BLK-SYSTEM-083 next step explicit without taking it. It can route one future frontier to human decision; it cannot approve, execute, publish, verify, trace-close, mutate, or isolate anything by itself.
