# BLK-097 — Bounded BLK-test Evidence Refresh Request / Exact-Target Frontier

**Status:** Completed consumed one-run BLK-test evidence-refresh boundary — exact-target evidence only; no production BLK-test MCP
**Boundary marker:** `BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_BOUNDARY`
**Sprint:** BLK-SYSTEM-097
**Persistent doctrine gate:** `PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_097_KURONODE_BOUNDED_EVIDENCE_REFRESH`

---

## Purpose

BLK-SYSTEM-097 permits exactly one bounded BLK-test functional-module evidence refresh over the real Kuronode workspace target after BLK-SYSTEM-096 reconciled the local BEO/RTM ladder and the operator selected the BLK-test evidence-refresh frontier.

BLK-test is a BLK-System functional module, not BLK-System's test suite.

The refresh is evidence-only. Its result vocabulary is:

```text
BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_PASS_EVIDENCE_ONLY
BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_FAIL_EVIDENCE_ONLY
BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_BLOCKED_EVIDENCE_ONLY
```

A PASS is only BLK-test evidence for the bounded source-descriptor profile. A FAIL is legitimate BLK-test evidence. A BLOCKED result consumes the replay IDs and does not permit automatic retargeting or rerun.

---

## Exact Runtime Identity

```text
approval_id: APPROVAL-BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-001
run_id: RUN-BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-001
target_repo_path: /home/dad/code/Kuronode-v1
source_subtree_path: /home/dad/code/Kuronode-v1/scripts
workspace_clone_path: /tmp/blk-system-097-kuronode-evidence-refresh-workspace
replay_ledger_path: /tmp/blk-system-097-kuronode-evidence-refresh-replay-ledger.json
target_branch: main
target_head_sha: aebea51bed911c781a537d84d38b2dcb838b1368
fixed_tool: run_ast_validation
```

The runtime must re-check that local Kuronode HEAD and observed `origin/main` remain `aebea51bed911c781a537d84d38b2dcb838b1368` before executing the fixed tool. If either identity differs, the run closes as BLOCKED evidence-only.

---

## Required Proof Markers

```text
USER_REQUESTED_EXECUTE_ALL_TASKS_FOR_BLK_SYSTEM_097
OPERATOR_AUTHORIZED_BLK_SYSTEM_097_EXACT_EVIDENCE_REFRESH
KURONODE_ORIGIN_MAIN_HEAD_RECHECKED
READ_ONLY_RUN_AST_VALIDATION_ONLY
REPLAY_CONSUMED_BEFORE_RUNTIME
NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST
NO_PROTECTED_BODY_READ
NO_BEO_RTM_COVERAGE_DRIFT_AUTHORITY
```

Replay IDs are consumed before runtime and cannot be reused even if the refresh BLOCKS.

---

## Runtime Behavior Allowed

Only these behaviors are allowed:

1. verify exact target path, source-subtree path, workspace path, branch, local HEAD, and observed remote HEAD;
2. validate the BLK-SYSTEM-097 authorization record and proof/denial sets;
3. consume caller-owned, process-local, and durable replay ledgers before runtime;
4. snapshot the approved source subtree and `.git` metadata for mutation detection;
5. copy the approved `/home/dad/code/Kuronode-v1/scripts` subtree into the wrapper-owned `/tmp/blk-system-097-kuronode-evidence-refresh-workspace` workspace;
6. build TypeScript/TSX source descriptors from the copied files;
7. run fixed `run_ast_validation` evidence logic over the copied descriptors;
8. remove the wrapper-owned workspace;
9. emit bounded JSON evidence with actual serialized byte count.

---

## Explicit Non-Authority Boundary

- No production BLK-test MCP authority
- No generic BLK-test MCP authority
- No reusable BLK-test service startup
- No arbitrary shell or caller-supplied commands
- No dynamic tool expansion
- No Electron launch, no Playwright launch, no smoke-test execution, no TypeScript compiler, no linter, no formatter, no package-manager invocation
- No network/model/browser/cyber tooling
- No BLK-pipe execution
- No Codex execution
- No live tactical LLM dispatch
- No Kuronode source mutation
- No Kuronode Git mutation, staging, commit, push, reset, checkout, revert, stash, cleanup, autofix, or remote writes by BLK-test
- No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison
- No authoritative BEO publication
- No runtime PUBLISHED BEO output
- No RTM generation or RTM drift rejection
- No coverage matrix, coverage claim, active-vault hash comparison, or drift decision
- No public ledger mutation
- No signer, storage, rollback, revocation, supersession, or release authority
- No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation proof

---

## Stop Conditions

The refresh must stop as BLOCKED evidence-only, without rerun under the same IDs, if:

- local HEAD differs from `aebea51bed911c781a537d84d38b2dcb838b1368`;
- observed `origin/main` differs from `aebea51bed911c781a537d84d38b2dcb838b1368`;
- either runtime ID is already present in caller-owned, process-local, durable replay state, or committed BLK-SYSTEM-097 evidence;
- any raw path spelling differs from the exact approved spelling even if it resolves to the same path;
- the wrapper-owned workspace already exists before runtime;
- the source subtree contains a secret-like descendant, `.git` metadata, protected BLK-req descendant, or symlink escape;
- source or Git metadata changes during the refresh;
- the wrapper-owned workspace is not cleaned up;
- bounded evidence cannot honestly fit the output limit.

---

## Doctrine Persistence

This boundary is pinned by `python/test_active_doctrine_review_gates.py` so later sprints cannot silently convert the BLK-SYSTEM-097 evidence refresh into production BLK-test MCP, a generic service, a source/Git mutation path, a protected-body read path, BEO/RTM/coverage/drift authority, or proof of host isolation.
