# BLK-054 — BLK-test Non-Disposable L4 Runtime Pilot Boundary

**Status:** Active one-run L4 pilot runtime boundary — exact target only; evidence only; not production BLK-test MCP
**Date:** 2026-05-10T09:42:18+10:00
**Purpose:** Define the only authorized non-disposable BLK-test L4 runtime pilot for BLK-SYSTEM-051: one read-only `run_ast_validation` run against `/home/dad/BLK-System/python`, with bounded evidence and no adjacent authority inheritance.
**Scope:** BLK-045 Fork C / BLK-053 follow-up. This boundary consumes the operator-confirmed exact target envelope and permits only one wrapper-mediated read-only AST validation pilot. It is not reusable BLK-test service authority and does not authorize production/generic BLK-test MCP.

---

## 0. Boundary Markers

```text
BLK_TEST_NON_DISPOSABLE_L4_RUNTIME_PILOT
BLK_TEST_NON_DISPOSABLE_L4_RUNTIME_PILOT_PASS_EVIDENCE_ONLY
APPROVED_ONE_RUN_ONLY_APPROVAL_BLK_SYSTEM_051_001
RUN_ID_RUN_BLK_SYSTEM_051_001_CONSUMED_BEFORE_RUNTIME
TARGET_REPO_PATH_HOME_DAD_BLK_SYSTEM
SOURCE_SUBTREE_PATH_HOME_DAD_BLK_SYSTEM_PYTHON
TARGET_HEAD_75E44C4066F7CBAD38ED15AFDC93A8EAFD703340_REQUIRED
WORKSPACE_CLONE_PATH_TMP_BLK_SYSTEM_051_NON_DISPOSABLE_L4_RUNTIME_WORKSPACE
READ_ONLY_RUN_AST_VALIDATION_ONLY
WRAPPER_OWNED_WORKSPACE_MARKER_NONCE_REQUIRED
SOURCE_AND_GIT_SNAPSHOTS_MUST_MATCH_AFTER_RUNTIME
WORKSPACE_CLEANUP_REQUIRED_ON_PASS_FAIL_BLOCKED_TIMEOUT_OUTPUT_OVERFLOW
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_051
```

Persistent doctrine gate marker: BLK-SYSTEM-051 pins non-disposable L4 runtime to exactly one approved read-only AST-validation run and evidence-only semantics.

---

## 1. Relationship to BLK-053

BLK-053 allowed only:

```text
NON_DISPOSABLE_L4_EXACT_TARGET_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
```

BLK-054 consumes the separately confirmed exact target envelope and activates only one L4 pilot runtime slice. BLK-054 does not widen BLK-053 into generic runtime authority and does not authorize any future run beyond the named approval/run IDs.

---

## 2. Approved Exact Target

The only approved target envelope is:

```text
target_repo_path: /home/dad/BLK-System
source_subtree_path: /home/dad/BLK-System/python
branch_or_worktree: main at 75e44c4066f7cbad38ed15afdc93a8eafd703340
workspace_clone_path: /tmp/blk-system-051-non-disposable-l4-runtime-workspace
approval_id: APPROVAL-BLK-SYSTEM-051-001
run_id: RUN-BLK-SYSTEM-051-001
expires_at: 1 hour from operator confirmation
fixed_tool: run_ast_validation
```

Any spelling, path, branch, HEAD, approval ID, run ID, workspace, expiry, or tool mismatch is a stop condition.

---

## 3. Runtime Semantics

The only permitted positive state is:

```text
BLK_TEST_NON_DISPOSABLE_L4_RUNTIME_PILOT_PASS_EVIDENCE_ONLY
```

This means:

- approval ID and run ID were consumed before clone/process/runtime work began;
- target HEAD matched `75e44c4066f7cbad38ed15afdc93a8eafd703340` before runtime;
- the source subtree resolved inside `/home/dad/BLK-System`;
- the source subtree did not contain protected BLK-req, Git metadata, secret, or symlink-escape descendants;
- the wrapper-owned workspace marker nonce existed before validation and was verified before cleanup;
- only Python AST parsing of `.py` files occurred;
- source tree and target Git metadata snapshots matched after runtime;
- the wrapper-owned workspace was cleaned after runtime;
- the output was bounded and evidence-only.

This positive state does not authorize publication, trace closure, mutation, or production reuse.

---

## 4. Non-Authority Boundary

BLK-054 does not authorize:

- production BLK-test MCP;
- generic BLK-test MCP;
- reusable BLK-test service startup;
- No production BLK-test MCP authority;
- No generic BLK-test MCP authority;
- No reusable BLK-test service startup;
- No second or reusable non-disposable runtime run;
- No live Codex execution authority;
- No arbitrary shell or caller-supplied commands;
- wildcard fixed tools or dynamic tool expansion;
- No source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test;
- No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison;
- No authoritative BEO publication;
- No runtime RTM generation or RTM drift rejection;
- public ledger mutation;
- signer, storage, rollback, revocation, supersession, or release authority;
- No package-manager, network, model-service, browser, or cyber tooling authority;
- No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim.

Operator shorthand:

- The pilot may read `.py` files in the approved source subtree only for AST parsing.
- The pilot must not mutate source or Git state.
- The pilot must not read protected BLK-req bodies or infer drift/coverage truth.
- The pilot must not publish BEOs or generate RTMs.
- The pilot must not become a reusable runtime service.

---

## 5. Stop Conditions

Pause and require hostile review plus a new human decision if any future action attempts to:

1. rerun `APPROVAL-BLK-SYSTEM-051-001` or `RUN-BLK-SYSTEM-051-001`;
2. run against any target other than `/home/dad/BLK-System/python` at HEAD `75e44c4066f7cbad38ed15afdc93a8eafd703340`;
3. use any tool other than `run_ast_validation`;
4. skip replay consumption before workspace/process start;
5. validate the source tree directly after workspace creation fails;
6. leave wrapper-owned workspace files behind after PASS, FAIL, BLOCKED, timeout, or output overflow;
7. treat PASS as BEO publication, RTM generation, active coverage, drift rejection, protected-vault truth, production BLK-test MCP, or production isolation;
8. mutate source or Git state as BLK-test behavior;
9. read, copy, parse, hash, summarize, scan, mutate, or compare protected BLK-req vault bodies;
10. rely on caller-supplied commands, package managers, network access, model services, browser tools, or cyber tooling.

---

## 6. Future Work Boundary

After BLK-SYSTEM-051, BLK-test may have one non-disposable L4 evidence artifact. That evidence is not enough to advance BEO publication or RTM runtime/drift authority by inheritance.

A later sprint must separately request any BEO publication, RTM generation, drift rejection, production BLK-test MCP, reusable BLK-test service, or additional non-disposable runtime authority.
