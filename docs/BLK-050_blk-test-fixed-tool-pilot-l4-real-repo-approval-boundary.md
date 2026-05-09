# BLK-050 — BLK-test Fixed-Tool Pilot L4 Real-Repo Approval Boundary

**Status:** Active L4 approval-boundary contract — exact-target real-repo preflight only; no runtime execution this sprint
**Date:** 2026-05-09T21:30:17+10:00
**Purpose:** Define the approval envelope and denial boundary required before any future BLK-test fixed-tool L4 real-repo pilot may execute, while keeping BLK-SYSTEM-047 itself non-runtime because no exact target approval was supplied.
**Scope:** BLK-045 Fork C / BLK-049 follow-up. This document converts the previous `L4_REAL_REPO_PILOT_BLOCKED_PENDING_EXACT_TARGET_APPROVAL` stop condition into a machine-checkable approval-boundary contract. It is not production BLK-test MCP authority, not generic BLK-test MCP authority, not real-repo runtime authority for this sprint, and not BEO/RTM/publication authority.

---

## 0. Boundary Markers

```text
BLK_TEST_FIXED_TOOL_PILOT_L4_REAL_REPO_APPROVAL_BOUNDARY
L4_REAL_REPO_APPROVAL_BOUNDARY_ONLY_NO_RUNTIME_THIS_SPRINT
EXACT_TARGET_REPO_PATH_BRANCH_WORKSPACE_REQUIRED
READ_ONLY_FIXED_TOOL_RUN_AST_VALIDATION_ONLY
REAL_REPO_SOURCE_MUTATION_FORBIDDEN
PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN
BEO_PUBLICATION_AND_RTM_REMAIN_SEPARATE_AUTHORITIES
EXACT_TARGET_APPROVAL_DOES_NOT_AUTHORIZE_PRODUCTION_MCP
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_047
```

Persistent doctrine gate marker: BLK-SYSTEM-047 pins L4 real-repo pilot as approval-boundary-only until exact target approval exists.

---

## 1. Relationship to BLK-049

BLK-049 authorized only:

```text
L3_SYNTHETIC_FIXED_TOOL_PILOT_ONLY_THIS_SPRINT
```

and explicitly blocked:

```text
L4_REAL_REPO_PILOT_BLOCKED_PENDING_EXACT_TARGET_APPROVAL
```

BLK-050 does not erase that block. It defines what a later exact-target approval envelope must contain before a future sprint may start L4 runtime. BLK-SYSTEM-047 may build and test the envelope/preflight fixture, but it must not run `run_ast_validation` against any real repository.

---

## 2. Required Exact Target Approval Envelope

A future L4 real-repo pilot approval must name all of the following fields exactly:

1. approved repository root path;
2. approved source subtree path within that repository;
3. approved branch or detached worktree identity;
4. approved workspace clone path;
5. workspace marker nonce;
6. read-only fixed tool name `run_ast_validation`;
7. test profile `blk-test-l4-real-repo-readonly-fixed-tool`;
8. timeout class, timeout seconds, output byte limit, and output compression/redaction behavior;
9. one-run replay identifiers for approval ID and run ID;
10. approval issue/expiry timestamps;
11. operator identity and source-system provenance;
12. cleanup and rollback obligations;
13. operator stop control;
14. hostile-review criteria;
15. explicit excluded authorities.

Missing, empty, inherited, wildcard, ambiguous, stale, expired, replayed, or authority-laundered approval evidence must block preflight before any runtime starts.

---

## 3. Non-Authority Boundary

BLK-050 does not authorize:

- production BLK-test MCP;
- generic BLK-test MCP;
- reusable BLK-test service startup;
- arbitrary shell or caller-supplied commands;
- wildcard fixed tools or dynamic tool expansion;
- package-manager, network, model-service, browser, or cyber tooling;
- real-repo BLK-test runtime in BLK-SYSTEM-047 without a complete exact target approval envelope;
- execution against `/home/dad/BLK-System` as a BLK-test target;
- execution against root paths, home paths, protected-vault paths, host-secret-bearing paths, symlink escapes, traversal aliases, or unowned workspaces;
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
- No real-repo BLK-test runtime in BLK-SYSTEM-047 without a complete exact target approval envelope.
- No source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test.
- No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison.
- No authoritative BEO publication.
- No runtime RTM generation or RTM drift rejection.
- No package-manager, network, model-service, browser, or cyber tooling authority.
- No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim.

---

## 4. L4 Preflight Semantics

The BLK-SYSTEM-047 fixture may return only these preflight-level states:

```text
L4_REAL_REPO_PILOT_BLOCKED_PENDING_EXACT_TARGET_APPROVAL
BLK_TEST_L4_REAL_REPO_PREFLIGHT_READY_NOT_EXECUTED
```

`BLK_TEST_L4_REAL_REPO_PREFLIGHT_READY_NOT_EXECUTED` means the approval envelope is internally complete and exact enough for a later sprint to decide whether to execute. It does not mean this sprint executed a real-repo pilot.

The preflight record must preserve:

```text
fixed_tool_executed: false
subprocess_called: false
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

## 5. Real-Repo and Workspace Boundary

The target repository and workspace checks must reject:

1. `/home/dad/BLK-System` as the BLK-test target;
2. root and home paths;
3. protected BLK-req paths or names including `docs/active`, `docs/requirements`, and `docs/use_cases`;
4. source subtree paths containing `.git`;
5. symlink escapes from the approved workspace clone;
6. traversal aliases;
7. unowned workspace paths or nonce mismatches;
8. host-secret-bearing paths such as `.ssh`, `.env`, credential stores, token paths, or cloud key paths.

BLK-test L4 approval is read-only evidence approval. It cannot mutate the target repository, the source subtree, Git state, or BLK-req protected vault bodies.

---

## 6. Fixed-Tool Registry

The only candidate fixed tool for this approval boundary is:

```text
run_ast_validation
```

The registry must reject arbitrary shell, caller-supplied command arrays, wildcard tools, unknown tools, dynamic tool expansion, package managers, network calls, model-service calls, browser tooling, and cyber tooling.

---

## 7. BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-050 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Preserve BLK-test as a verification evidence oracle only; planning, mutation, publication, and RTM remain separate. |
| BLK-002 — Artifact Lifecycle | Preserve HITL authority, staging isolation, active-vault immutability, and no verifier access to protected bodies. |
| BLK-003 — Orchestration Protocol | Preserve human gates, bounded context, hostile review, failure ceilings, and no approval inheritance. |
| BLK-004 — BLK-pipe V47 Suite | Preserve BLK-pipe as source mutation/Git enforcement; BLK-test cannot mutate source or broaden allowlists. |
| BLK-005 — BLK-Req Specification | Preserve canonical trace binding without protected-body leakage or coverage/drift claims. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny and no tactical/verifier body reads. |

---

## 8. Stop Conditions

Pause and require hostile review plus new human approval if any future sprint attempts to:

1. treat BLK-050 as production BLK-test MCP authority;
2. treat BLK-SYSTEM-047 as real-repo runtime approval;
3. inherit approval from BLK-047 request readiness, BLK-048 frontier selection, BLK-049 L3 synthetic PASS, BLK-pipe approval, Codex approval, BEO fixture readiness, RTM fixture readiness, or BLK-020 first-smoke evidence;
4. run a real-repo pilot without exact target repo/path/branch/workspace approval;
5. run any tool other than `run_ast_validation` without a later fixed-registry approval;
6. use arbitrary shell, package managers, network, model-service, browser, or cyber tooling;
7. mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source;
8. read, copy, parse, hash, summarize, scan, mutate, or compare protected BLK-req bodies;
9. convert PASS evidence into BEO publication, RTM generation, active coverage, drift rejection, protected-vault truth, or production isolation claims.

---

## 9. Final Boundary Thesis

BLK-050 turns L4 real-repo pilot activation into an exact-target approval problem. It does not itself start runtime. The safe next future step, only after a complete exact target approval envelope exists, is a separate sprint that runs one read-only `run_ast_validation` L4 pilot and then pauses for hostile review before any broader BLK-test authority is considered.
