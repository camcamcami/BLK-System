# BLK-053 — Non-Disposable L4 Exact-Target Approval Envelope Boundary

**Status:** Active approval-envelope boundary — human-review package only; no non-disposable runtime this sprint
**Date:** 2026-05-10T08:47:47+10:00
**Purpose:** Define the exact-target approval-envelope gate required before BLK-System may ask a human to approve one future non-disposable L4 BLK-test fixed-tool pilot.
**Scope:** BLK-045 Fork C / BLK-052 follow-up. This boundary validates envelope completeness, single-frontier selection, replay/expiry/source binding, target/workspace separation, and denied adjacent authorities. It is not runtime authority and does not execute the future pilot.

---

## 0. Boundary Markers

```text
BLK_TEST_NON_DISPOSABLE_L4_EXACT_TARGET_APPROVAL_ENVELOPE
NON_DISPOSABLE_L4_EXACT_TARGET_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
EXACTLY_ONE_NON_DISPOSABLE_TARGET_REQUIRED
APPROVAL_ENVELOPE_DOES_NOT_AUTHORIZE_RUNTIME
READ_ONLY_RUN_AST_VALIDATION_ONLY_FUTURE_RUNTIME
NO_NON_DISPOSABLE_RUNTIME_THIS_SPRINT
BEO_PUBLICATION_AND_RTM_REMAIN_SEPARATE_AUTHORITIES
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_050
```

Persistent doctrine gate marker: BLK-SYSTEM-050 pins non-disposable L4 advancement to exact-target approval-envelope review only.

---

## 1. Relationship to BLK-052

BLK-052 allowed only:

```text
NON_DISPOSABLE_L4_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
```

BLK-053 does not convert that request-ready state into runtime approval. BLK-053 only validates whether a future exact-target non-disposable L4 approval envelope is complete enough for a human to review.

---

## 2. Review-Ready Semantics

The only positive state is:

```text
NON_DISPOSABLE_L4_EXACT_TARGET_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
```

This means:

- BLK-SYSTEM-049 request-ready evidence is bound by artifact path and SHA256;
- exactly one frontier is selected: `blk_test_non_disposable_l4_run_ast_validation`;
- target repo/source/workspace/branch/replay/output/cleanup/operator-stop fields are complete;
- all adjacent BEO, RTM, publication, drift, production MCP, source mutation, and protected-body authorities remain denied;
- no runtime approval exists and no non-disposable runtime execution occurred.

This does not authorize execution.

---

## 3. Required Approval Envelope Fields

A future runtime approval envelope must separately name and bind:

1. selected frontier;
2. repository root path;
3. source subtree path;
4. branch or detached worktree identity;
5. workspace clone path;
6. workspace marker nonce;
7. exact fixed tool `run_ast_validation`;
8. timeout seconds and output byte limit;
9. approval ID;
10. run ID;
11. issued-at timestamp;
12. expires-at timestamp;
13. operator identity;
14. source-system provenance;
15. cleanup and rollback obligations;
16. operator stop control;
17. hostile-review criteria;
18. explicit excluded authorities;
19. no-side-effect flags;
20. BLK-SYSTEM-049 evidence artifact descriptors.

BLK-SYSTEM-050 may validate these fields. It must not consume them as runtime approval.

---

## 4. Non-Authority Boundary

BLK-053 does not authorize:

- production BLK-test MCP;
- generic BLK-test MCP;
- reusable BLK-test service startup;
- non-disposable runtime execution authority;
- live Codex execution authority;
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
- No live Codex execution authority.
- No source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test.
- No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison.
- No authoritative BEO publication.
- No runtime RTM generation or RTM drift rejection.
- No package-manager, network, model-service, browser, or cyber tooling authority.
- No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim.

---

## 5. Stop Conditions

Pause and require hostile review plus a new human decision if any future sprint attempts to:

1. treat `NON_DISPOSABLE_L4_EXACT_TARGET_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME` as runtime approval;
2. execute against a non-disposable repository without a new exact-target runtime sprint;
3. select more than one frontier;
4. start live Codex execution;
5. convert PASS evidence into BEO publication, RTM generation, active coverage, drift rejection, protected-vault truth, or production isolation claims;
6. mutate source or Git state as BLK-test behavior;
7. read, copy, parse, hash, summarize, scan, mutate, or compare protected BLK-req vault bodies;
8. rely on caller-supplied commands, package managers, network access, model services, browser tools, or cyber tooling.

---

## 6. Future Runtime Preconditions

A later non-disposable runtime sprint must still provide a new explicit human runtime approval naming the exact envelope and may run only one read-only `run_ast_validation` pilot.

The later sprint must prove:

- approval ID and run ID are consumed before process start;
- target and workspace paths are resolved before cleanup;
- source repo remains read-only;
- workspace marker nonce binds cleanup to the wrapper-owned workspace;
- traversal, symlink, protected, and secret descendant paths are rejected;
- timeout and output caps produce non-success evidence and cleanup;
- operator stop controls are available before runtime begins;
- hostile review passes before closeout.

BLK-053 is only the approval-envelope review gate before that later runtime sprint.
