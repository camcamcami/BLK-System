# BLK-051 — BLK-test Fixed-Tool L4 Disposable Real-Repo Runtime Boundary

**Status:** Active bounded L4 runtime boundary — disposable exact-target real-repo only; not production BLK-test MCP
**Date:** 2026-05-10T07:10:22+10:00
**Purpose:** Authorize the smallest useful BLK-test L4 runtime pilot: one read-only `run_ast_validation` fixed-tool run against a disposable exact-target real Git repository created by the BLK-SYSTEM-048 harness.
**Scope:** BLK-045 Fork C / BLK-050 follow-up. This boundary permits only a harness-owned disposable real-repo runtime slice. It is not production BLK-test MCP authority, not generic BLK-test MCP authority, not authority to run against `/home/dad/BLK-System` or arbitrary operator repositories, and not BEO/RTM/publication/drift authority.

---

## 0. Boundary Markers

```text
BLK_TEST_FIXED_TOOL_L4_DISPOSABLE_REAL_REPO_RUNTIME_BOUNDARY
L4_DISPOSABLE_REAL_REPO_RUN_AST_VALIDATION_ONLY_THIS_SPRINT
EXACT_TARGET_DISPOSABLE_GIT_REPO_REQUIRED
READ_ONLY_FIXED_TOOL_RUN_AST_VALIDATION_ONLY
REPLAY_CONSUMED_BEFORE_RUNTIME
NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST
PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN
BEO_PUBLICATION_AND_RTM_REMAIN_SEPARATE_AUTHORITIES
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_048
```

Persistent doctrine gate marker: BLK-SYSTEM-048 pins L4 runtime to one disposable exact-target real-repo run_ast_validation pilot.

---

## 1. Relationship to BLK-050

BLK-050 defined exact-target L4 preflight readiness:

```text
BLK_TEST_L4_REAL_REPO_PREFLIGHT_READY_NOT_EXECUTED
```

BLK-051 narrows the first runtime use of that readiness to a disposable real Git repository created by the sprint harness. It does not authorize runtime against existing operator repositories. It does not authorize production/generic BLK-test MCP.

---

## 2. Approved Runtime Slice

The only approved runtime slice is:

```text
approved_runtime_slice: L4_DISPOSABLE_REAL_REPO_RUN_AST_VALIDATION_ONLY_THIS_SPRINT
approved_target_class: disposable real Git repository created by BLK-SYSTEM-048 harness
approved_tool: run_ast_validation
approved_execution_model: in-process Python ast.parse over approved .py files only
approval_consumption: replay approval_id and run_id consumed before runtime
source_mutation_allowed: false
git_mutation_allowed: false
beo_publication: DRAFT_ONLY
rtm_status: NOT_GENERATED
```

The fixed tool AST validation phase may read only approved `.py` files under the approved source subtree of the disposable target repository. Before that AST phase, the runtime may perform bounded disposable Git identity verification by reading only the harness-owned repo marker plus `.git/HEAD`, the referenced HEAD ref, the loose HEAD commit object, and the loose HEAD tree object; broad Git metadata byte reads remain forbidden. It must not read protected BLK-req bodies or host-secret-bearing paths.

---

## 3. Non-Authority Boundary

BLK-051 does not authorize:

- production BLK-test MCP;
- generic BLK-test MCP;
- reusable BLK-test service startup;
- arbitrary shell or caller-supplied commands;
- wildcard fixed tools or dynamic tool expansion;
- package-manager, network, model-service, browser, or cyber tooling;
- execution against /home/dad/BLK-System or arbitrary operator repositories;
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
- No arbitrary shell or caller-supplied commands.
- No execution against /home/dad/BLK-System or arbitrary operator repositories.
- No source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test.
- No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison.
- No authoritative BEO publication.
- No runtime RTM generation or RTM drift rejection.
- No package-manager, network, model-service, browser, or cyber tooling authority.
- No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim.

---

## 4. Evidence Semantics

BLK-SYSTEM-048 runtime evidence may return only evidence states:

```text
BLK_TEST_L4_DISPOSABLE_REPO_PASS_EVIDENCE_ONLY
BLK_TEST_L4_DISPOSABLE_REPO_FAIL_EVIDENCE_ONLY
BLK_TEST_L4_DISPOSABLE_REPO_BLOCKED_EVIDENCE_ONLY
```

PASS means only that the approved disposable source subtree's Python files parsed successfully. FAIL means syntax errors or validation errors were found. BLOCKED means policy/preflight/path/replay/authority checks prevented runtime. None of these states authorize BEO publication, RTM generation, coverage truth, drift rejection, source mutation, or production isolation claims.

Runtime evidence must include:

```text
fixed_tool_executed: true only after preflight and replay consumption
source_write_allowed: false
staging_allowed: false
commit_allowed: false
push_allowed: false
active_vault_read: false
beo_publication: DRAFT_ONLY
rtm_status: NOT_GENERATED
production_isolation_claimed: false
```

---

## 5. Stop Conditions

Pause and require hostile review plus new human approval if any future sprint attempts to:

1. treat BLK-051 as production BLK-test MCP authority;
2. run against `/home/dad/BLK-System` or arbitrary operator repositories;
3. run tools other than `run_ast_validation`;
4. use arbitrary shell, package managers, network, model-service, browser, or cyber tooling;
5. mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source;
6. read, copy, parse, hash, summarize, scan, mutate, or compare protected BLK-req bodies;
7. convert PASS evidence into BEO publication, RTM generation, active coverage, drift rejection, protected-vault truth, or production isolation claims.

---

## 6. BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-051 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Preserve BLK-test as verification evidence only; planning, mutation, publication, and RTM remain separate. |
| BLK-002 — Artifact Lifecycle | Preserve HITL authority, staging isolation, active-vault immutability, and no verifier access to protected bodies. |
| BLK-003 — Orchestration Protocol | Preserve human gates, bounded context, hostile review, failure ceilings, and no approval inheritance. |
| BLK-004 — BLK-pipe V47 Suite | Preserve BLK-pipe as source mutation/Git enforcement; BLK-test cannot mutate source or broaden allowlists. |
| BLK-005 — BLK-Req Specification | Preserve canonical trace binding without protected-body leakage or coverage/drift claims. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny and no tactical/verifier body reads. |

---

## 7. Final Boundary Thesis

BLK-051 permits exactly one kind of L4 BLK-test runtime evidence: read-only AST validation against a disposable exact-target real Git repository owned by the sprint harness. This is sufficient to prove the L4 runtime loop can work without turning BLK-test into production MCP, mutation authority, publication authority, or trace-closure authority.
