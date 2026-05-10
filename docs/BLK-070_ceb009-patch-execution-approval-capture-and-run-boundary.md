# BLK-070 — CEB_009 Patch Execution Approval Capture and Run Boundary

**Status:** Active exact-target approval-capture boundary — one BLK-pipe-mediated patch attempt is approved only for the named target head; current remote-target drift blocks execution until fresh approval
**Date:** 2026-05-11T08:31:00+10:00
**Purpose:** Define the BLK-SYSTEM-065 boundary for capturing the operator's explicit CEB_009 patch-execution approval and either preparing one exact BLK-pipe payload or blocking before invocation when exact-target drift is observed.
**Scope:** BLK-System-owned approval-capture fixture plus one exact BLK-pipe-mediated Kuronode source mutation attempt if and only if local and observed remote target heads match the approved target SHA. This boundary does not authorize retargeting to a different HEAD, live Codex, Electron/smoke runtime, TypeScript/package-manager tooling, BLK-test MCP, BEO/CEO publication, RTM, protected reads, production isolation claims, or Kuronode remote push.

---

## 0. Boundary Markers

```text
KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_APPROVAL_CAPTURE_AND_RUN_BOUNDARY
KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_READY_FOR_ONE_EXACT_BLK_PIPE_PATCH_ATTEMPT
KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_BLOCKED_TARGET_DRIFT_NOT_EXECUTED
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_065_CEB009_PATCH_EXECUTION_APPROVAL_CAPTURE_AND_RUN
```

Operator approval captured in BLK-SYSTEM-065 is exact-target approval only.

Approval capture is not retargeting authority.

A local HEAD match is insufficient if the observed remote target branch differs from the approved target SHA.

BLK-pipe success would be patch-commit evidence only, not BEO/CEO publication, not BLK-test PASS evidence, not RTM trace closure, and not remote-push authority.

---

## 1. Authorized Scope

BLK-SYSTEM-065 may:

1. capture the explicit Discord operator grant for one exact CEB_009 patch execution;
2. consume and recompute the BLK-SYSTEM-064 authority-request hash;
3. require exact target identity:
   - `github:camcamcami/Kuronode-v1`;
   - branch `main`;
   - head `cb09d965c0407612c9ce8fc9cc58c5e62c82e1b2`;
   - path `scripts/smoke_test.ts`;
   - `allowed_modified_files=[scripts/smoke_test.ts]`;
   - `allowed_new_files=[]`;
4. require exact approval ID, run ID, expiry, operator identity, output bound, operator stop, rollback expectation, cleanup expectation, and replay ledger identity;
5. build a BLK-pipe payload only when local and observed remote target heads both equal the approved target SHA;
6. invoke Go `blk-pipe` at most once only after the exact-target gate returns ready;
7. allow BLK-pipe to commit only the allowlisted file if the engine and validation succeed;
8. write BLK-System plan, outcome, review, and closeout documents and commit/push those BLK-System repository maintenance artifacts.

---

## 2. Required Stop Condition

If any target-head drift is observed, BLK-SYSTEM-065 must return:

```text
KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_BLOCKED_TARGET_DRIFT_NOT_EXECUTED
TARGET_HEAD_DRIFT_REQUIRES_FRESH_APPROVAL
```

This stop condition applies when:

1. local Kuronode HEAD is not `cb09d965c0407612c9ce8fc9cc58c5e62c82e1b2`; or
2. observed Kuronode `origin/main` is not `cb09d965c0407612c9ce8fc9cc58c5e62c82e1b2`.

When blocked, BLK-pipe must not be invoked, the patch must not be applied, and Kuronode source/Git must remain unmodified by this sprint.

---

## 3. Exact Patch Intent

The only authorized source mutation, if exact-target checks pass, is the CEB_009 remediation of `scripts/smoke_test.ts`:

1. replace `@ts-ignore` / unsafe `any` result access with typed API declarations and result guards;
2. validate that the projection result has a string `streamId`;
3. reject timeout sentinel before PASS logging;
4. reject missing AST payload before PASS logging;
5. preserve listener `unsub()` cleanup;
6. preserve `finally` close cleanup for Electron.

---

## 4. Required Side-Effect Semantics

A ready approval-capture record may set:

```text
approval_captured=True
execution_authorized=True
blk_pipe_invoked=False
patch_executed=False
patch_committed=False
kuronode_remote_pushed=False
```

Only the actual BLK-pipe report may prove invocation or commit. The approval-capture fixture cannot self-report a completed patch.

A blocked approval-capture record must set:

```text
approval_captured=True
execution_authorized=False
blk_pipe_invoked=False
patch_executed=False
patch_committed=False
kuronode_remote_pushed=False
```

---

## 5. Explicit Non-Authority

No retargeting to `70b6062b92cf61c12bf190f92dc6b45ea4dcd438` or any other SHA without fresh approval.

No Kuronode remote push.

No source or Git mutation outside exact BLK-pipe allowlists.

No live Codex execution.

No production BLK-test MCP authority.

No generic BLK-test MCP authority.

No reusable BLK-test service startup.

No arbitrary shell as BLK-test behavior.

No Electron launch, no headless smoke-test execution, and no wall-clock timeout wait.

No TypeScript tooling, typechecker, linter, formatter, or package-manager execution.

No package-manager, network, model-service, browser, or cyber tooling authority.

No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison.

No authoritative BEO publication.

No CEO_009 publication.

No runtime `PUBLISHED` BEO output.

No live publication approval capture.

No signer key material access.

No cryptographic signing.

No immutable storage writes.

No public ledger append or mutation.

No rollback, revocation, or supersession execution except BLK-pipe revert/reset cleanup bounded to the exact patch attempt.

No runtime RTM generation or RTM drift rejection.

No active-vault hash comparison, coverage matrix, coverage claim, or drift decision.

No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim.

---

## 6. Relationship to BLK-069

BLK-069 required a separate future sprint to capture human patch execution approval before BLK-pipe invocation. BLK-070 is that approval-capture boundary, but it remains exact-target bound. BLK-070 does not weaken BLK-069's adjacent non-authorities and does not permit using the BLK-SYSTEM-064 request-ready package to patch a different HEAD.

---

## 7. Current Observed State

At BLK-SYSTEM-065 preflight, the local Kuronode checkout was at the approved target head:

```text
cb09d965c0407612c9ce8fc9cc58c5e62c82e1b2
```

The observed GitHub `origin/main` target head was:

```text
70b6062b92cf61c12bf190f92dc6b45ea4dcd438
```

Therefore this boundary expects the actual BLK-pipe execution task to block unless a fresh approval retargets the sprint or the target branch is reconciled under explicit authority.
