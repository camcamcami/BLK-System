# BLK-test Kuronode Workspace Read-Only Pilot Runtime Boundary

**Status:** Active one-run runtime boundary — read-only evidence pilot only; no production BLK-test MCP
**Boundary marker:** `BLK_TEST_KURONODE_WORKSPACE_READ_ONLY_PILOT_RUNTIME_BOUNDARY`
**Sprint:** BLK-SYSTEM-073
**Persistent doctrine gate:** `PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_073_KURONODE_WORKSPACE_READ_ONLY_PILOT_RUNTIME`

---

## Purpose

BLK-SYSTEM-073 permits exactly one bounded BLK-test functional-module runtime pilot over the real Kuronode workspace target after BLK-SYSTEM-071 request-readiness, BLK-SYSTEM-072 exact-target envelope review, and the subsequent Kuronode push authorization.

BLK-test is a BLK-System functional module, not BLK-System's test suite.

The pilot is evidence-only. Its result vocabulary is:

```text
BLK_TEST_KURONODE_WORKSPACE_READ_ONLY_PILOT_PASS_EVIDENCE_ONLY
BLK_TEST_KURONODE_WORKSPACE_READ_ONLY_PILOT_FAIL_EVIDENCE_ONLY
BLK_TEST_KURONODE_WORKSPACE_READ_ONLY_PILOT_BLOCKED_EVIDENCE_ONLY
```

A PASS is only BLK-test evidence for the bounded source-descriptor profile. A FAIL is a legitimate BLK-test finding. A BLOCKED result consumes the replay IDs and does not permit automatic retargeting or rerun.

---

## Exact Runtime Identity

```text
approval_id: APPROVAL-BLK-SYSTEM-073-KURONODE-WORKSPACE-001
run_id: RUN-BLK-SYSTEM-073-KURONODE-WORKSPACE-001
target_repo_path: /home/dad/code/Kuronode-v1
source_subtree_path: /home/dad/code/Kuronode-v1/scripts
workspace_clone_path: /tmp/blk-system-073-kuronode-workspace-read-only-pilot-workspace
replay_ledger_path: /tmp/blk-system-073-kuronode-workspace-read-only-pilot-replay-ledger.json
target_branch: main
target_head_sha: 38e332b188e45edcb484765694112c9041ad1a3b
fixed_tool: run_ast_validation
```

The runtime must re-check that local Kuronode HEAD and observed `origin/main` remain `38e332b188e45edcb484765694112c9041ad1a3b` before executing the fixed tool. If either identity differs, the run closes as BLOCKED evidence-only.

---

## Required Proof Markers

```text
USER_REQUESTED_EXECUTE_ALL_TASKS_FOR_BLK_SYSTEM_073
UPSTREAM_BLK_SYSTEM_072_ENVELOPE_BOUND_NOT_RUNTIME_APPROVAL
KURONODE_ORIGIN_MAIN_HEAD_RECHECKED
READ_ONLY_RUN_AST_VALIDATION_ONLY
REPLAY_CONSUMED_BEFORE_RUNTIME
NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST
NO_PROTECTED_BODY_READ
NO_BEO_RTM_COVERAGE_DRIFT_AUTHORITY
```

The upstream BLK-SYSTEM-072 envelope is bound as review evidence only. It is not runtime approval by itself; BLK-SYSTEM-073 supplies the fresh exact runtime IDs above.

Replay IDs are consumed before runtime and cannot be reused even if the pilot BLOCKS.

---

## Runtime Behavior Allowed

Only these behaviors are allowed:

1. verify exact target path, source-subtree path, workspace path, branch, local HEAD, and observed remote HEAD;
2. validate the upstream BLK-SYSTEM-072 envelope hash and no-authority fields;
3. validate the BLK-SYSTEM-073 authorization record and proof/denial sets;
4. consume caller-owned, process-local, and durable replay ledgers before runtime;
5. snapshot the approved source subtree and `.git` metadata for mutation detection;
6. copy the approved `/home/dad/code/Kuronode-v1/scripts` subtree into the wrapper-owned `/tmp/blk-system-073-kuronode-workspace-read-only-pilot-workspace` workspace;
7. build TypeScript/TSX source descriptors from the copied files;
8. run fixed `run_ast_validation` evidence logic over the copied descriptors;
9. remove the wrapper-owned workspace;
10. emit bounded JSON evidence with actual serialized byte count.

---

## Explicit Non-Authority Boundary

- No production BLK-test MCP authority
- No generic BLK-test MCP authority
- No reusable BLK-test service startup
- No arbitrary shell or caller-supplied commands
- No dynamic tool expansion
- No Electron launch, no Playwright launch, no smoke-test execution, no TypeScript compiler, no linter, no formatter, no package-manager invocation
- No network/model/browser/cyber tooling
- No Kuronode source mutation
- No Kuronode Git mutation, staging, commit, push, reset, checkout, revert, stash, cleanup, autofix, or remote writes by BLK-test
- No CEB_009, BLK-SYSTEM-070, BLK-SYSTEM-071, or BLK-SYSTEM-072 artifact reuse as executable runtime authority
- No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison
- No authoritative BEO publication
- No runtime PUBLISHED BEO output
- No RTM generation or RTM drift rejection
- No coverage matrix, coverage claim, active-vault hash comparison, or drift decision
- No public ledger mutation
- No signer, storage, rollback, revocation, supersession, or release authority
- No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation proof
- No live Codex execution authority
- No live tactical LLM dispatch

---

## Stop Conditions

The pilot must stop as BLOCKED evidence-only, without rerun under the same IDs, if:

- local HEAD differs from `38e332b188e45edcb484765694112c9041ad1a3b`;
- observed `origin/main` differs from `38e332b188e45edcb484765694112c9041ad1a3b`;
- either runtime ID is already present in caller-owned, process-local, or durable replay state;
- any raw path spelling differs from the exact approved spelling even if it resolves to the same path;
- the wrapper-owned workspace already exists before runtime;
- the source subtree contains a secret-like descendant, `.git` metadata, protected BLK-req descendant, or symlink escape;
- source or Git metadata changes during the pilot;
- the wrapper-owned workspace is not cleaned up;
- bounded evidence cannot honestly fit the output limit.

---

## Doctrine Persistence

This boundary is pinned by `python/test_active_doctrine_review_gates.py` so later sprints cannot silently convert the BLK-SYSTEM-073 read-only pilot into production BLK-test MCP, a generic service, a source/Git mutation path, a protected-body read path, BEO/RTM/coverage/drift authority, or proof of host isolation.
