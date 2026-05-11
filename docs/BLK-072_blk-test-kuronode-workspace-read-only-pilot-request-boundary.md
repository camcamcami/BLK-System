# BLK-072 — BLK-test Kuronode Workspace Read-Only Pilot Request Boundary

**Status:** Active request/doctrine/fixture boundary — human-review package only; no Kuronode BLK-test runtime this sprint
**Date:** 2026-05-11T10:55:00+10:00
**Sprint:** BLK-SYSTEM-071
**Purpose:** Define the non-runtime boundary for a future read-only BLK-test functional-module pilot over the real Kuronode workspace.
**Scope:** Deterministic request-package validation and active doctrine gates for targeting `/home/dad/code/Kuronode-v1` at local HEAD `38e332b188e45edcb484765694112c9041ad1a3b`; no runtime execution, no workspace mutation, and no reuse of CEB_009 authority as executable fixture input.

---

## 0. Boundary Markers

```text
BLK_TEST_KURONODE_WORKSPACE_PILOT_REQUEST_BOUNDARY
BLK_TEST_KURONODE_WORKSPACE_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
BLK_TEST_MODULE_NOT_BLK_SYSTEM_TEST_SUITE
KURONODE_WORKSPACE_EXACT_TARGET_BOUND
READ_ONLY_FIXED_TOOL_ONLY
NO_CEB009_REUSE
NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST
NO_PROTECTED_BODY_READ
BEO_RTM_AND_COVERAGE_AUTHORITY_SEPARATE
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_071_KURONODE_WORKSPACE_PILOT_REQUEST
```

Persistent doctrine gate marker: BLK-SYSTEM-071 pins BLK-test Kuronode workspace work to module request readiness only, not BLK-System test-suite semantics and not runtime.

---

## 1. Naming Boundary

BLK-test is a BLK-System functional module, not BLK-System's test suite.

This boundary exists to prevent future sessions from misreading a BLK-test module pilot as a test of BLK-System itself. BLK-test work must be described as module/oracle/runtime/evidence work, not as proof that BLK-System itself was tested.

Accepted names:

- BLK-test module pilot
- BLK-test evidence module request
- BLK-test read-only oracle request
- Kuronode workspace validation via BLK-test module

Forbidden names:

- BLK-System test
- test of BLK-System
- testing BLK-System with Kuronode
- BLK-test as proof that BLK-System itself was tested

---

## 2. Request-Ready State

The only positive state produced by BLK-SYSTEM-071 is:

```text
BLK_TEST_KURONODE_WORKSPACE_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
```

This means a deterministic request package exists for future human review. It does not mean runtime approval exists, BLK-test runtime executed, or Kuronode was validated.

The request package binds:

```text
target_repo_path: /home/dad/code/Kuronode-v1
target_branch: main
target_head_sha: 38e332b188e45edcb484765694112c9041ad1a3b
target_workspace_label: kuronode-v1-local-workspace
workspace_status: main...origin/main [ahead 1]
fixed_tool: run_ast_validation
tool_mode: READ_ONLY_STATIC_AST_VALIDATION_REQUEST_ONLY
```

Kuronode's local ahead-one state is target identity context only. This boundary does not authorize remote push, local reset, cleanup, checkout, fetch, or any other Git operation in Kuronode.

---

## 3. Relationship to CEB_009 and BLK-SYSTEM-070

BLK-SYSTEM-070 successfully applied the CEB_009 patch locally through BLK-pipe and produced Kuronode commit `38e332b188e45edcb484765694112c9041ad1a3b`.

BLK-SYSTEM-071 may cite that commit as target identity context. It must not reuse any consumed CEB_009 authority as executable BLK-test input.

No CEB_009 approval IDs, run IDs, BLK-pipe payloads, reports, or patch authority reused as executable BLK-test fixture input.

CEB_009 may remain historical evidence only. A future BLK-test runtime pilot against Kuronode must use a fresh approval envelope, fresh replay IDs, exact current target identity, and explicit operator approval.

---

## 4. Required Request Proofs

A valid BLK-SYSTEM-071 request package must carry exactly these proof markers:

```text
BLK_TEST_MODULE_NOT_BLK_SYSTEM_TEST_SUITE
KURONODE_WORKSPACE_EXACT_TARGET_BOUND
READ_ONLY_FIXED_TOOL_ONLY
NO_CEB009_REUSE
NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST
NO_PROTECTED_BODY_READ
BEO_RTM_AND_COVERAGE_AUTHORITY_SEPARATE
```

Placeholders such as `ok`, `done`, or `pass` are not valid proof markers. Extra markers that imply live execution, runtime approval, BEO publication, RTM generation, coverage truth, drift rejection, protected-body access, source/Git mutation, tooling execution, or production isolation are invalid.

---

## 5. Explicit Non-Authority

No production BLK-test MCP authority.

No generic BLK-test MCP authority.

No reusable BLK-test service startup.

No Kuronode BLK-test runtime execution in BLK-SYSTEM-071.

No arbitrary shell or caller-supplied commands.

No dynamic tool expansion.

No Electron launch, no smoke-test execution, no TypeScript tooling, no package-manager invocation, no network/model/browser/cyber tooling.

No CEB_009 approval IDs, run IDs, BLK-pipe payloads, reports, or patch authority reused as executable BLK-test fixture input.

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

## 6. Future Runtime Requirement

A future runtime sprint, if desired, must create a separate exact-target approval envelope that includes:

1. the current Kuronode repo path, branch, and HEAD at that future time;
2. fresh approval and run IDs;
3. replay ledger policy;
4. read-only fixed-tool definition;
5. timeout and output caps;
6. pre/post source and Git mutation snapshots;
7. operator stop controls;
8. wrapper/workspace isolation and cleanup obligations;
9. hostile review before and after execution;
10. explicit no-BEO/no-RTM/no-coverage-drift/no-protected-body/no-production-MCP denials.

BLK-SYSTEM-071 creates only the request-ready package for such a future decision.
