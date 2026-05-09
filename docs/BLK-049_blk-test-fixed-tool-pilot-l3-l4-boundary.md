# BLK-049 — BLK-test Fixed-Tool Pilot L3/L4 Boundary

**Status:** Active bounded pilot boundary — L3 synthetic fixed-tool execution only; L4 real-repo pilot blocked pending exact target approval
**Date:** 2026-05-09T20:38:30+10:00
**Purpose:** Define the active BLK-test fixed-tool pilot boundary selected by the operator after BLK-048, while limiting this sprint's runtime to one synthetic L3 fixed-tool evidence path and keeping real-repo L4 pilot execution blocked.
**Scope:** BLK-045 Fork C / BLK-048 selected frontier `blk_test_fixed_tool_pilot_l3_l4`. This boundary permits only approval-bound synthetic workspace execution of repository-owned fixed tool `run_ast_validation` through the BLK-SYSTEM-046 fixture. It is not production BLK-test MCP authority, not generic BLK-test MCP authority, not L4 real-repo authority, and not publication/RTM authority.

---

## 0. Boundary Markers

```text
BLK_TEST_FIXED_TOOL_PILOT_L3_L4_BOUNDARY
BLK_TEST_FRONTIER_SELECTED_BY_OPERATOR
L3_SYNTHETIC_FIXED_TOOL_PILOT_ONLY_THIS_SPRINT
L4_REAL_REPO_PILOT_BLOCKED_PENDING_EXACT_TARGET_APPROVAL
FIXED_TOOL_REGISTRY_RUN_AST_VALIDATION_ONLY
SOURCE_BOUND_REPLAY_PROTECTED_APPROVAL_REQUIRED
SYNTHETIC_WORKSPACE_ISOLATION_REQUIRED
BLK_TEST_EVIDENCE_ONLY_NO_SOURCE_MUTATION
PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN
BEO_PUBLICATION_AND_RTM_REMAIN_SEPARATE_AUTHORITIES
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_046
```

Persistent doctrine gate marker: BLK-SYSTEM-046 pins BLK-test fixed-tool pilot as L3 synthetic-only with L4 real-repo runtime blocked.

---

## 1. Operator Selection and Exact Runtime Slice

The operator selected the single frontier:

```text
blk_test_fixed_tool_pilot_l3_l4
```

That selection satisfies BLK-048's exactly-one-frontier rule. It does not grant broad or production authority. BLK-SYSTEM-046 binds the selection to this exact runtime slice:

```text
selected_frontier: blk_test_fixed_tool_pilot_l3_l4
approved_runtime_slice: L3_SYNTHETIC_FIXED_TOOL_PILOT_ONLY_THIS_SPRINT
approved_fixed_tool: run_ast_validation
approved_workspace_class: synthetic isolated workspace created by the BLK-SYSTEM-046 test/fixture harness
approved_transport: stdio fixed-tool harness only
l4_real_repo_pilot: L4_REAL_REPO_PILOT_BLOCKED_PENDING_EXACT_TARGET_APPROVAL
```

A later L4 real-repo pilot must provide an additional approval envelope naming exact target repository, path, branch/worktree, workspace identity, rollback/cleanup obligations, timeout/output profile, operator stop controls, and hostile-review criteria before any real target execution starts.

---

## 2. Non-Authority Boundary

BLK-049 does not authorize:

- production BLK-test MCP;
- generic BLK-test MCP;
- reusable BLK-test service startup;
- arbitrary shell or caller-supplied commands;
- wildcard fixed tools or dynamic tool expansion;
- package-manager, network, model-service, browser, or cyber tooling;
- L4 real-repo runtime without exact target approval;
- execution against `/home/dad/BLK-System` as a BLK-test target;
- execution against real repositories, `.git` roots, `.git` ancestors, `.git` descendants, root paths, home paths, protected-vault paths, host-secret-bearing paths, symlink escapes, traversal aliases, or unowned workspaces;
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
- No L4 real-repo runtime without exact target approval.
- No source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test.
- No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison.
- No authoritative BEO publication.
- No runtime RTM generation or RTM drift rejection.
- No package-manager, network, model-service, browser, or cyber tooling authority.
- No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim.

---

## 3. Required Approval and Replay Semantics

The BLK-SYSTEM-046 fixture must require all of the following before L3 synthetic execution:

1. explicit selected frontier `blk_test_fixed_tool_pilot_l3_l4`;
2. BLK-test-specific approval kind, not Codex, BLK-pipe, BEO, RTM, or BLK-020 approval reuse;
3. source-bound authorization request with source report identity, `beb_id`, source commit hash, `pre_engine_hash`, canonical trace artifacts, requested fixed tool, test profile, workspace identity, timeout/output profile, approval identity, and replay identifiers;
4. caller-supplied `used_approval_ids` and `used_run_ids` sets;
5. one-run replay refusal before process start;
6. exact envelope hash binding approval, run ID, source evidence, workspace identity, timeout/output profile, implementation identity, and driver identity;
7. explicit human approval checkpoint for this sprint's synthetic L3 runtime slice;
8. cleanup verification before success evidence.

The fixture must fail closed for missing, mismatched, expired, stale, replayed, malformed, BLOCKED, unknown, transport-error, interrupted, policy-blocked, or authority-laundered evidence.

---

## 4. Fixed-Tool Registry and Workspace Boundary

Allowed tool registry:

```text
run_ast_validation
```

The tool registry must reject:

- arbitrary shell;
- caller-supplied command arrays;
- wildcard tools;
- unknown tools;
- dynamic tool expansion;
- package managers;
- network/model/browser/cyber capabilities.

Allowed workspace class:

```text
synthetic isolated workspace created by the BLK-SYSTEM-046 fixture/test harness
```

Workspace checks must reject primary repo targets, real repositories, `.git` roots, `.git` ancestors, `.git` descendants, root/home/protected/host-secret paths, symlink escapes, traversal aliases, and unowned workspaces. Protected-vault checks must use path/metadata guards only and must not read protected BLK-req bodies.

---

## 5. Evidence Semantics

BLK-test remains evidence only. PASS, FAIL, BLOCKED, FATAL, transport-error, interrupted, stale, malformed, unknown, replayed, or policy-blocked evidence must not:

- mutate source;
- stage, commit, push, reset, stash, checkout, revert, or autofix;
- publish BEOs;
- generate RTM;
- create active coverage truth;
- make drift decisions;
- promote BLK-req artifacts;
- read protected bodies;
- claim production isolation.

Runtime output fields must preserve:

```text
beo_publication: DRAFT_ONLY
rtm_status: NOT_GENERATED
source_write_allowed: false
active_vault_read: false
production_isolation_claimed: false
```

---

## 6. Relationship to BLK-047 and BLK-048

BLK-047 remains the request package contract. BLK-048 remains the selection gate. BLK-049 is the narrower selected-frontier runtime boundary for BLK-SYSTEM-046.

BLK-049 does not erase or weaken BLK-047/BLK-048 stop conditions. It only converts the selected frontier into one synthetic L3 execution allowance with an L4 preflight block. If future work tries to broaden beyond this, pause for hostile review and a new human approval.

---

## 7. BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-049 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Preserve BLK-test as evidence oracle only; planning, source mutation, publication, and RTM remain separate. |
| BLK-002 — Artifact Lifecycle | Preserve HITL authority, staging isolation, active-vault immutability, and no verifier access to protected bodies. |
| BLK-003 — Orchestration Protocol | Preserve human gates, bounded context, hostile review, failure ceilings, and no approval inheritance. |
| BLK-004 — BLK-pipe V47 Suite | Preserve BLK-pipe as source mutation/Git enforcement; BLK-test cannot mutate source or broaden allowlists. |
| BLK-005 — BLK-Req Specification | Preserve canonical trace binding without protected-body leakage or coverage/drift claims. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny and no tactical/verifier body reads. |

---

## 8. Stop Conditions

Pause and require hostile review plus new human approval if any future sprint attempts to:

1. treat BLK-049 as production BLK-test MCP authority;
2. reuse BLK-047 request readiness, BLK-048 selection readiness, BLK-pipe approval, Codex approval, BEO fixture readiness, RTM fixture readiness, or BLK-020 first-smoke evidence as pilot approval;
3. run against a real target repository without exact L4 target approval;
4. execute any tool other than `run_ast_validation` without a later fixed-registry approval;
5. use arbitrary shell, package managers, network, model-service, browser, or cyber tooling;
6. mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source;
7. read, copy, parse, hash, summarize, scan, mutate, or compare protected BLK-req bodies;
8. convert PASS evidence into BEO publication, RTM generation, active coverage, drift rejection, protected-vault truth, or production isolation claims.

---

## 9. Final Boundary Thesis

BLK-049 activates only the smallest useful BLK-test frontier: an approval-bound, replay-protected, synthetic L3 fixed-tool evidence run. L4 real-repo pilot runtime remains blocked until the operator supplies exact target approval and the system proves rollback, cleanup, replay, output, and stop-control behavior for that target.
