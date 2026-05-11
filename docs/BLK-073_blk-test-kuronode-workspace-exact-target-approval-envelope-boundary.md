# BLK-073 — BLK-test Kuronode Workspace Exact-Target Approval Envelope Boundary

**Status:** Active approval-envelope fixture boundary — human-review package only; no Kuronode BLK-test runtime this sprint
**Date:** 2026-05-11T11:45:00+10:00
**Sprint:** BLK-SYSTEM-072
**Purpose:** Define the review-only exact-target approval-envelope boundary for a future read-only BLK-test functional-module pilot over the real Kuronode workspace.
**Scope:** Deterministic approval-envelope validation that binds the BLK-SYSTEM-071 request package, exact Kuronode target identity, fresh future approval/run IDs, replay policy, output bounds, proof markers, and denied authorities. This boundary does not approve or execute runtime.

---

## 0. Boundary Markers

```text
BLK_TEST_KURONODE_WORKSPACE_EXACT_TARGET_APPROVAL_ENVELOPE_BOUNDARY
BLK_TEST_KURONODE_WORKSPACE_EXACT_TARGET_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
BLK_TEST_MODULE_NOT_BLK_SYSTEM_TEST_SUITE
UPSTREAM_REQUEST_HASH_RECOMPUTED
EXACT_KURONODE_TARGET_BOUND
FRESH_BLK_SYSTEM_072_APPROVAL_ID_REQUIRED
FRESH_BLK_SYSTEM_072_RUN_ID_REQUIRED
REPLAY_POLICY_REVIEW_ONLY
READ_ONLY_FIXED_TOOL_FUTURE_RUNTIME_ONLY
NO_RUNTIME_APPROVAL_GRANTED
NO_CEB009_REUSE
NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST
BEO_RTM_AND_COVERAGE_AUTHORITY_SEPARATE
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_072_KURONODE_WORKSPACE_EXACT_TARGET_APPROVAL_ENVELOPE
```

Persistent doctrine gate marker: BLK-SYSTEM-072 pins the Kuronode workspace approval envelope to human-review readiness only, not runtime approval and not BLK-System test-suite semantics.

---

## 1. Naming Boundary

BLK-test is a BLK-System functional module, not BLK-System's test suite.

This boundary describes a future possible use of the BLK-test module against Kuronode. It does not test BLK-System itself and must not be described as a BLK-System test suite.

---

## 2. Review-Ready State

The only positive state produced by BLK-SYSTEM-072 is:

```text
BLK_TEST_KURONODE_WORKSPACE_EXACT_TARGET_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
```

This means an exact-target approval-envelope fixture is ready for human review. It does not mean runtime approval exists, BLK-test runtime executed, Kuronode was validated, or any source/Git operation occurred.

---

## 3. Upstream Request Binding

The envelope must consume and recompute the BLK-SYSTEM-071 upstream request hash.

Required upstream marker:

```text
BLK_TEST_KURONODE_WORKSPACE_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
```

Required proof:

```text
UPSTREAM_REQUEST_HASH_RECOMPUTED
```

A submitted upstream package with a forged `request_hash`, altered target HEAD, altered target path, altered branch, altered workspace status, altered fixed tool, or altered BLK-test role statement must fail closed.

---

## 4. Exact Target and Future IDs

The exact target identity is:

```text
target_repo_path: /home/dad/code/Kuronode-v1
target_branch: main
target_head_sha: 38e332b188e45edcb484765694112c9041ad1a3b
workspace_status: main...origin/main [ahead 1]
fixed_tool: run_ast_validation
tool_mode: READ_ONLY_STATIC_AST_VALIDATION_FUTURE_RUNTIME_ONLY
```

The review-only envelope IDs are:

```text
approval_envelope_id: BLK-SYSTEM-072-KURONODE-WORKSPACE-APPROVAL-ENVELOPE-001
approval_id: APPROVAL-BLK-SYSTEM-072-KURONODE-WORKSPACE-001
run_id: RUN-BLK-SYSTEM-072-KURONODE-WORKSPACE-001
```

These are not runtime approval or runtime execution. They are exact future IDs that a later human-approved runtime sprint may either consume or supersede under a new plan.

---

## 5. Required Envelope Proofs

A valid BLK-SYSTEM-072 envelope must carry exactly these proof markers:

```text
UPSTREAM_REQUEST_HASH_RECOMPUTED
EXACT_KURONODE_TARGET_BOUND
FRESH_BLK_SYSTEM_072_APPROVAL_ID_REQUIRED
FRESH_BLK_SYSTEM_072_RUN_ID_REQUIRED
REPLAY_POLICY_REVIEW_ONLY
READ_ONLY_FIXED_TOOL_FUTURE_RUNTIME_ONLY
NO_RUNTIME_APPROVAL_GRANTED
NO_CEB009_REUSE
NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST
BEO_RTM_AND_COVERAGE_AUTHORITY_SEPARATE
```

Placeholders such as `ok`, `done`, or `pass` are invalid. Additional markers that imply runtime approval, live execution, BEO publication, RTM generation, coverage truth, drift rejection, protected-body access, source/Git mutation, tooling execution, or production isolation are invalid.

---

## 6. Explicit Non-Authority

No runtime approval.

No Kuronode BLK-test runtime execution in BLK-SYSTEM-072.

No production BLK-test MCP authority.

No generic BLK-test MCP authority.

No reusable BLK-test service startup.

No arbitrary shell or caller-supplied commands.

No dynamic tool expansion.

No Electron launch, no smoke-test execution, no TypeScript tooling, no package-manager invocation, no network/model/browser/cyber tooling.

No CEB_009 approval IDs, run IDs, BLK-pipe payloads, reports, or patch authority reused as executable BLK-test fixture input.

No BLK-SYSTEM-071 request package treated as runtime approval.

No source mutation, staging, commit, push, reset, stash, checkout, revert, cleanup, or autofix by BLK-test.

No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison.

No authoritative BEO publication.

No runtime `PUBLISHED` BEO output.

No runtime RTM generation or RTM drift rejection.

No coverage matrix, coverage claim, active-vault hash comparison, or drift decision.

No public ledger mutation.

No signer, storage, rollback, revocation, supersession, or release authority.

No live Codex execution authority.

No live tactical LLM dispatch.

No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim.

---

## 7. Future Runtime Requirement

A later runtime sprint, if explicitly approved, must:

1. re-check the current Kuronode path, branch, HEAD, and worktree state at that time;
2. consume fresh or still-valid approval/run IDs before runtime starts;
3. enforce replay policy durably;
4. verify wrapper/workspace isolation;
5. run only the fixed read-only `run_ast_validation` BLK-test module behavior;
6. record pre/post source and Git snapshots;
7. bound output and timeout;
8. preserve operator stop controls;
9. perform hostile review after execution;
10. keep BEO, RTM, coverage/drift, protected-body, mutation, and production-MCP authorities separate.

BLK-SYSTEM-072 itself does none of those runtime actions.
