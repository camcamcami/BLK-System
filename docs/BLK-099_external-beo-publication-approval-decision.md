# BLK-099 — External BEO Publication Approval Decision Capture

**Status:** Active BLK-System approval-decision capture boundary — not publication execution
**Date:** 2026-05-13
**Purpose:** Record the deterministic boundary for capturing the operator's explicit approval decision for the exact BLK-SYSTEM-098 prerequisite request package.
**Scope:** BLK-System-local fixture, doctrine markers, current-state indexing, and outcome evidence. This document is not a sprint plan, not a BEB, not a BEO, not publication execution, not signing, not storage/ledger/rollback authority, and not RTM authority.

---

## 0. Boundary Markers

```text
EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION_CAPTURE_BOUNDARY
EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK098_REQUEST_NOT_PUBLISHED
BEO-PUBLICATION-APPROVAL-DECISION-099-001
BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001
APPROVAL-BLK-SYSTEM-099-EXTERNAL-BEO-PUBLICATION-001
RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_099_EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION
```

Persistent doctrine gate marker: BLK-SYSTEM-099 captures approval for one future separately scoped external BEO publication execution sprint. It records approval-decision evidence only. External publication not executed. Future publication execution run ID is reserved but not consumed.

---

## 1. Exact Upstream Request Bound

BLK-SYSTEM-099 consumes the review-only BLK-SYSTEM-098 prerequisite request package and does not perform a target-repo operation.

| Input | Bound identity |
| --- | --- |
| BLK-SYSTEM-098 prerequisite request package | `BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001` |
| BLK-SYSTEM-098 request package hash | `sha256:a782b223c88ae155a37519b87313dd2085450515c78ba60e93277c636ba6e041` |
| BLK-SYSTEM-098 request status | `BEO_PUBLICATION_PREREQUISITE_REQUEST_READY_AFTER_BLK_TEST_REFRESH_NOT_GRANTED` |
| BLK-SYSTEM-097 evidence canonical hash inherited by hash only | `sha256:ebf3121a3a62dabaea589dc796ad645ef56d71d59574326bf278fbf563b66580` |
| BLK-SYSTEM-087 local pilot execution package hash inherited by hash only | `sha256:78df1c4420bebd3da4e568bff8dd9f424f093e2548248b2825f2781ab8f31a7e` |
| BLK-SYSTEM-087 local pilot artifact hash inherited by hash only | `sha256:6ee76d749bdb809bb39ae2f6f26c22c302370f9bf30da54acfc208a6661e875a` |
| Target repo path carried as evidence metadata only | `/home/dad/code/Kuronode-v1` |
| Target HEAD carried as evidence metadata only | `aebea51bed911c781a537d84d38b2dcb838b1368` |
| BEO identity carried from local pilot fixture only | `BEO-054-001` |
| BEO hash carried from local pilot fixture only | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` |

The operator approval text was received in the current Discord DM session as:

```text
I approve external BEO publication for BEO-PUBLICATION-PREREQUISITE-REQUEST-098- 001 under BLK-SYSTEM-099
```

The whitespace anomaly in `098- 001` is retained as raw provenance while the fixture requires the normalized package ID `BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001` and exact request package hash above.

---

## 2. Implemented Fixture Contract

The deterministic fixture lives at:

```text
python/beo_external_publication_approval_decision.py
```

It builds approval-decision package:

```text
approval_decision_package_id: BEO-PUBLICATION-APPROVAL-DECISION-099-001
approval_decision_status: EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK098_REQUEST_NOT_PUBLISHED
approval_decision_package_hash: sha256:c83ea7982632b587a8596550cfa0f1c36b546a70b8f2fa8cbefb4aedfeda383b
selected_frontier: external_beo_publication_approval_decision_capture
decision_scope: EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION_ONLY_NOT_PUBLICATION_EXECUTION
decision_result: APPROVED_FOR_ONE_FUTURE_EXTERNAL_BEO_PUBLICATION_EXECUTION_NOT_PUBLISHED
approval_id: APPROVAL-BLK-SYSTEM-099-EXTERNAL-BEO-PUBLICATION-001
future_publication_execution_run_id: RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001
next_required_authority: SEPARATELY_SCOPED_EXTERNAL_BEO_PUBLICATION_EXECUTION_REQUIRED_NOT_RUN
```

The fixture must reject:

1. BLK-SYSTEM-098 request packages whose submitted package hash does not recompute.
2. Self-consistently rehashed BLK-SYSTEM-098 request packages that differ from canonical package hash `sha256:a782b223c88ae155a37519b87313dd2085450515c78ba60e93277c636ba6e041`.
3. BLK-SYSTEM-098 request packages that already claim publication approval, publication execution, signer/storage/ledger/rollback, RTM, drift, protected-body, target/source/Git, BLK-pipe/BLK-test/Codex/tooling, or production-isolation side effects.
4. Approval-decision payloads that retarget the package id/hash, BEO id/hash, target path/head, approval ID, or future execution run ID.
5. Approval-decision payloads that expire, replay, become stale, duplicate proof/denial sets, omit exact proof obligations, add extra fields, or set any forbidden side-effect flag.
6. Authority-laundering text in caller-controlled strings, including compact/camel/allcaps/percent-encoded `PublicationAuthorized`, `SigningGranted`, `BEOisPublished`, `rtm_generation_authorized`, and protected path variants.

---

## 3. Approval Capture Boundary

BLK-SYSTEM-099 records human approval for one future separately scoped external BEO publication execution sprint only. It does not execute that sprint. It does not consume `RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001`.

This state is intentionally narrow:

- Approval captured: yes, for the exact BLK-SYSTEM-098 package and hash.
- External publication not executed.
- Runtime `PUBLISHED` BEO output not emitted.
- Future publication execution run ID is reserved but not consumed.
- A separate future sprint must define signer/storage/ledger/rollback policies, execution run window, hostile review, and publication closeout before any external publication execution can occur.

---

## 4. Non-Authority Boundary

BLK-SYSTEM-099 does not authorize or perform:

- No external authoritative BEO publication execution.
- No runtime PUBLISHED BEO output.
- No signer key-material access or cryptographic signing.
- No immutable storage writes or public ledger mutation.
- No rollback, revocation, or supersession execution.
- No runtime RTM generation or RTM drift rejection.
- No authoritative drift decision, active-vault hash comparison, coverage truth, or coverage-claim promotion.
- No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison.
- No target-repo scan or mutation.
- No source/Git mutation by fixtures.
- No BLK-pipe, BLK-test runtime, Codex, package/network/model/browser/cyber tooling, or production-isolation authority.
- No production BLK-test MCP or generic BLK-test MCP authority.
- No BEB dispatch or BEO closeout execution.

Passing prerequisite evidence is evidence. Captured approval is not publication. Publication execution requires a future exact sprint.

---

## 5. Proof Obligations

The fixture pins this exact proof-obligation set:

```text
ACTIVE_VAULT_AND_PROTECTED_BODY_ACCESS_EXCLUDED
APPROVAL_ID_RESERVED_FOR_BLK099_DECISION
BLK098_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND
BLK098_REQUEST_STATUS_NOT_GRANTED_BOUND
BLK_PIPE_BLK_TEST_CODEX_TOOLING_EXCLUDED
EXTERNAL_PUBLICATION_NOT_EXECUTED_BY_APPROVAL_DECISION
FUTURE_PUBLICATION_EXECUTION_RUN_ID_RESERVED_NOT_CONSUMED
HOSTILE_REVIEW_REQUIRED_BEFORE_EXTERNAL_PUBLICATION_EXECUTION
HUMAN_EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_REQUEST
OPERATOR_RAW_TEXT_AND_NORMALIZED_REQUEST_ID_BOUND
PUBLICATION_AUTHORIZED_AND_SIGNING_GRANTED_MARKERS_REJECTED_OUTSIDE_RECORD
RTM_AND_DRIFT_AUTHORITIES_EXCLUDED
SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED
TARGET_REPO_AND_SOURCE_GIT_MUTATION_EXCLUDED
```

The fixture pins denied-authority coverage for external publication execution, runtime published BEO output, future run ID consumption, `PublicationAuthorized` / `SigningGranted` markers outside the BLK-SYSTEM-099 record, signing, storage, ledger mutation, rollback/revocation/supersession, RTM generation, RTM drift rejection, drift decision, active-vault comparison, coverage, protected body reads, target/source/Git mutation, BEB/BEO execution, BLK-pipe, BLK-test runtime, production BLK-test MCP, generic BLK-test MCP, Codex, arbitrary shell, tooling, and production isolation.

---

## 6. Relationship To BLK-001 Through BLK-006

| Governing doc | BLK-099 alignment |
| --- | --- |
| BLK-001 — Master Architecture | Records who approved what and which exact package hash was approved, without converting the record into publication execution or trace closure. |
| BLK-002 — BLK-Req Artifact Lifecycle | Captures human decision provenance without mutating active/protected BLK-req bodies. |
| BLK-003 — BLK-pipe & BLK-test Orchestration Protocol | Does not dispatch a BEB, publish a BEO, run BLK-pipe, run BLK-test, start Codex, or generate RTM. |
| BLK-004 — BLK-pipe V47 Suite | Does not invoke mutation enforcement or any target-repo Git path. |
| BLK-005 — BLK-Req Specification | Preserves hash trace semantics while avoiding coverage, drift, RTM, or active-vault comparison claims. |
| BLK-006 — BLK-Req Implementation Brief | Preserves protected-vault hard-deny and no protected-body reads. |

---

## 7. Stop Conditions

Pause and require a separate exact sprint if any future step attempts to:

1. treat `EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK098_REQUEST_NOT_PUBLISHED` as publication execution;
2. consume `RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001` inside BLK-SYSTEM-099;
3. perform external publication, signing, immutable storage writes, public ledger mutation, rollback, revocation, or supersession;
4. generate RTM, perform RTM drift rejection, compare active-vault hashes, promote coverage truth, or make an authoritative drift decision;
5. read, hash, scan, summarize, compare, or mutate protected BLK-req bodies;
6. run BLK-pipe, BLK-test runtime, Codex, package managers, network/model/browser/cyber tooling, or arbitrary shell as fixture behavior;
7. scan or mutate the target repository;
8. claim production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret isolation.

BLK-SYSTEM-099 only captures the approval decision and reserves future execution identity.
