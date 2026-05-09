# BLK-052 — BLK-test L4 Evidence Trust and Non-Disposable Request Gate

**Status:** Active request-gate boundary — evidence trust review only; no non-disposable runtime this sprint
**Date:** 2026-05-10T08:09:46+10:00
**Purpose:** Define the evidence-trust gate required before BLK-System may request a future non-disposable exact-target L4 BLK-test pilot, without granting or executing that pilot in BLK-SYSTEM-049.
**Scope:** BLK-045 Fork C / BLK-051 follow-up. This boundary evaluates disposable L4 evidence and future exact-target request completeness only. It is not production BLK-test MCP authority, not generic BLK-test MCP authority, not non-disposable repository runtime authority, and not BEO/RTM/publication/drift authority.

---

## 0. Boundary Markers

```text
BLK_TEST_L4_EVIDENCE_TRUST_AND_NON_DISPOSABLE_REQUEST_GATE
NON_DISPOSABLE_L4_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
DISPOSABLE_L4_EVIDENCE_TRUST_REVIEW_ONLY
NO_NON_DISPOSABLE_RUNTIME_THIS_SPRINT
EXACT_TARGET_NON_DISPOSABLE_REPO_REQUIRED_FOR_FUTURE_RUNTIME
BEO_PUBLICATION_AND_RTM_REMAIN_SEPARATE_AUTHORITIES
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_049
```

Persistent doctrine gate marker: BLK-SYSTEM-049 pins non-disposable L4 advancement to evidence-trust request readiness only.

---

## 1. Relationship to BLK-051

BLK-051 authorized only:

```text
L4_DISPOSABLE_REAL_REPO_RUN_AST_VALIDATION_ONLY_THIS_SPRINT
```

BLK-052 does not broaden that runtime authority. It reviews the trustworthiness of BLK-SYSTEM-048 disposable evidence and can produce only a human-review request package for a future non-disposable exact-target L4 pilot.

---

## 2. Request-Ready Semantics

The only positive state is:

```text
NON_DISPOSABLE_L4_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
```

This means:

- BLK-SYSTEM-048 disposable L4 evidence is present and internally trustworthy enough to discuss the next pilot;
- hostile review passed after remediation;
- final verification evidence is present;
- future exact-target proposal fields are complete enough for human review;
- no runtime approval exists for the future non-disposable pilot.

This does not authorize execution.

---

## 3. Future Exact Target Fields

A later non-disposable L4 runtime sprint must separately name and approve:

1. repository root path;
2. source subtree path;
3. branch or detached worktree identity;
4. workspace clone path;
5. workspace marker nonce;
6. exact fixed tool `run_ast_validation`;
7. timeout/output cap profile;
8. replay approval ID and run ID;
9. issue and expiry timestamps;
10. operator identity and source-system provenance;
11. cleanup and rollback obligations;
12. operator stop control;
13. hostile-review criteria;
14. explicit excluded authorities.

BLK-SYSTEM-049 may validate that these fields exist in a proposal, but it must not consume them as runtime approval.

---

## 4. Non-Authority Boundary

BLK-052 does not authorize:

- production BLK-test MCP;
- generic BLK-test MCP;
- reusable BLK-test service startup;
- non-disposable runtime execution authority;
- arbitrary shell or caller-supplied commands;
- wildcard fixed tools or dynamic tool expansion;
- package-manager, network, model-service, browser, or cyber tooling;
- source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test;
- protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison;
- authoritative BEO publication;
- runtime RTM generation or RTM drift rejection;
- public ledger mutation;
- signer, storage, rollback, revocation, supersession, or release authority;
- production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claims.

Operator shorthand:

- No production BLK-test MCP authority.
- No generic BLK-test MCP authority.
- No non-disposable runtime execution authority.
- No source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test.
- No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison.
- No authoritative BEO publication.
- No runtime RTM generation or RTM drift rejection.
- No package-manager, network, model-service, browser, or cyber tooling authority.
- No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim.

---

## 5. Stop Conditions

Pause and require hostile review plus new human approval if any future sprint attempts to:

1. treat `NON_DISPOSABLE_L4_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME` as runtime approval;
2. execute against a non-disposable repository without a new exact-target runtime sprint;
3. convert PASS evidence into BEO publication, RTM generation, active coverage, drift rejection, protected-vault truth, or production isolation claims;
4. inherit approval from BLK-SYSTEM-048 disposable runtime, BLK-050 preflight, BLK-047 request readiness, BLK-pipe approval, Codex approval, BEO fixtures, or RTM fixtures;
5. read protected BLK-req bodies or host-secret-bearing paths.

---

## 6. BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-052 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Preserve BLK-test as verification evidence only; publication and RTM remain separate. |
| BLK-002 — Artifact Lifecycle | Preserve HITL approval and active-vault immutability. |
| BLK-003 — Orchestration Protocol | Preserve human gates, hostile review, and no approval inheritance. |
| BLK-004 — BLK-pipe V47 Suite | Preserve BLK-pipe ownership of source mutation/Git authority. |
| BLK-005 — BLK-Req Specification | Preserve trace/hash semantics without coverage/drift claims. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny and no verifier body reads. |

---

## 7. Final Boundary Thesis

BLK-052 turns BLK-SYSTEM-048 evidence into a reviewable question, not runtime authority. It lets the operator decide whether a later non-disposable exact-target L4 pilot is worth requesting while keeping all execution, publication, RTM, drift, protected-body, and production authority disabled.
