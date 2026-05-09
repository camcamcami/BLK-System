# BLK-048 — Authority Frontier Selection Gate Boundary

**Status:** Active selection-gate contract — review/decision routing only; not runtime authority
**Date:** 2026-05-09T20:02:26+10:00
**Purpose:** Require an explicit single-frontier human decision before any future BLK-System runtime activation sprint can proceed.
**Scope:** BLK-045 cross-fork selection control for Codex live-dispatch and BLK-test fixed-tool pilot decisions. This boundary is L0/L1 doctrine/fixture evidence only. It is not a sprint plan, not a runtime approval envelope, and not permission to start Codex, BLK-test, BLK-pipe, BEO, RTM, or any adjacent runtime capability.

---

## 0. Boundary Markers

```text
BLK_SYSTEM_AUTHORITY_FRONTIER_SELECTION_GATE
FRONTIER_SELECTION_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY
EXACTLY_ONE_FRONTIER_REQUIRED
RUNTIME_APPROVAL_NOT_INFERRED_FROM_NEXT_SPRINT
BLK_TEST_REQUEST_READY_IS_NOT_PILOT_APPROVAL
CODEX_REVIEW_READY_IS_NOT_LIVE_EXECUTION_APPROVAL
BEO_AND_RTM_BLOCKED_UNTIL_VERIFICATION_FRONTIER_APPROVED
PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN
ADJACENT_AUTHORITY_INHERITANCE_FORBIDDEN
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_045
```

Persistent doctrine gate marker: BLK-SYSTEM-045 pins authority frontier selection as review-only and non-runtime.

---

## 1. Non-Execution and Non-Authority Boundary

BLK-048 is a selection gate only. It does not authorize:

- live Codex execution;
- Codex subprocess startup;
- BLK-pipe dispatch from any Codex or selection adapter;
- production BLK-test MCP;
- live BLK-test server or client startup;
- BLK-test fixed-tool execution;
- new BLK-test smoke runs;
- replay of the BLK-SYSTEM-014 / BLK-020 historical first fixed-tool smoke;
- source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test, Codex, or selection-gate code;
- protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison;
- authoritative BEO publication;
- runtime RTM generation or drift rejection;
- public ledger mutation;
- signer, storage, rollback, revocation, supersession, or release authority;
- package-manager, network, model-service, browser, or cyber tooling;
- production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claims.

Operator shorthand:

- No live Codex execution authority.
- No production BLK-test MCP authority.
- No BLK-test fixed-tool execution authority.
- No authoritative BEO publication authority.
- No runtime RTM generation or drift rejection authority.
- No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison.
- No package-manager, network, model-service, browser, or cyber tooling authority.
- No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim.

---

## 2. Current Roadmap Problem

BLK-045 asks the operator to choose exactly one authority frontier. BLK-046 shows current surfaces are review-ready, fixture-ready, disabled, or future-authority only. BLK-047 created a BLK-test pilot request package but explicitly states request readiness is not runtime approval.

The recurring failure mode is authority inference: a future sprint could treat “next sprint,” sprint-dispatch approval, BLK-test request readiness, Codex review readiness, BEO fixture readiness, or RTM fixture readiness as if it were runtime approval. BLK-048 blocks that inference.

---

## 3. Allowed Frontier Selection Outcomes

A deterministic frontier selection gate may report only:

```text
FRONTIER_SELECTION_READY_FOR_HUMAN_DECISION_NOT_RUNTIME
FRONTIER_SELECTION_BLOCKED_NOT_AUTHORIZED
FRONTIER_ACTIVATION_DISABLED_NOT_AUTHORIZED
```

A selection record may name exactly one candidate frontier for human decision:

```text
codex_live_dispatch_l3_smoke
blk_test_fixed_tool_pilot_l3_l4
```

Any other frontier, no frontier, or multiple frontier selection is blocked. BEO publication and RTM generation are deliberately not selectable until verification evidence is trustworthy and a later governing boundary explicitly opens those frontiers.

---

## 4. Required Selection Gate Semantics

The selection gate must require:

1. exactly one selected frontier;
2. governing docs for the selected frontier;
3. an explicit future approval requirement;
4. exact excluded adjacent authorities;
5. a statement that sprint-dispatch approval does not substitute for runtime approval;
6. a statement that review-ready/request-ready/fixture-ready evidence is not runtime approval;
7. hostile-review checklist for authority inheritance;
8. complete disabled activation adapter side-effect denial.

The gate must reject:

- `next sprint` as approval;
- sprint-dispatch approval as runtime approval;
- BLK-test request readiness as pilot approval;
- Codex review readiness as live execution approval;
- BEO fixture readiness as publication approval;
- RTM fixture readiness as generation/drift approval;
- selected-frontier arrays with more than one value;
- generic authority, approval, authorized, allowed, or claim fields that launder runtime approval;
- strings asserting live/runtime/execution/transport/pilot approval;
- adjacent authority inheritance across Codex, BLK-test, BLK-pipe, BEO, RTM, protected-vault, package/network/model/browser/cyber tooling, or production isolation.

---

## 5. Relationship to Existing Boundary Documents

| Surface | Current relationship |
| --- | --- |
| BLK-040 through BLK-044 | Codex live-dispatch ladder remains enough to request a future L3 smoke decision, not enough to execute. |
| BLK-047 | BLK-test fixed-tool pilot request package remains enough to request a future pilot decision, not enough to execute. |
| BLK-026 / BLK-028 | BEO fixtures remain draft/candidate/input evidence only; publication is blocked until verification evidence is trustworthy and publication authority is separately granted. |
| BLK-027 / BLK-029 / BLK-030 / BLK-033 | RTM/offline-ledger fixtures remain local fixture evidence only; runtime generation and drift rejection are blocked until separate RTM authority exists. |
| BLK-006 | Protected BLK-req body isolation remains absolute for selection-gate code and future activation planning. |

---

## 6. Stop Conditions

Pause and require hostile review plus a new human decision if any future sprint attempts to:

1. treat BLK-048 or a selection fixture as runtime approval;
2. select more than one runtime frontier;
3. select BEO publication or RTM generation before verification frontier evidence is trustworthy and separately authorized;
4. start Codex, BLK-test, BLK-pipe, BEO, RTM, network, model, browser, cyber, or package-manager tooling from a selection adapter;
5. inherit approval from sprint-dispatch, BLK-test request readiness, Codex review readiness, BEO fixture readiness, RTM fixture readiness, BLK-pipe approval, or BLK-020 first-smoke evidence;
6. read, copy, parse, hash, summarize, scan, mutate, or compare protected BLK-req bodies;
7. claim production sandbox or host-secret isolation from a selection decision.

---

## 7. BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-048 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Preserve separation between planning, execution, verification, publication, and trace closure. |
| BLK-002 — Artifact Lifecycle | Preserve HITL authority, active-vault immutability, and no implicit promotion from selection evidence. |
| BLK-003 — Orchestration Protocol | Preserve human dispatch gates, hostile audit, failure ceilings, and no inherited authority across phases. |
| BLK-004 — BLK-pipe V47 Suite | Preserve BLK-pipe as source mutation/Git enforcement; selection code cannot dispatch or mutate. |
| BLK-005 — BLK-Req Specification | Preserve trace binding without converting selection/readiness evidence into coverage or drift truth. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny and no tactical/verifier/selection body reads. |

---

## 8. Final Boundary Thesis

BLK-048 turns the post-BLK-SYSTEM-044 question into an explicit gate: exactly one frontier must be named for human decision, and every adjacent authority remains disabled. The gate can make a future approval request auditable; it cannot approve or execute runtime behavior.
