# BLK-SYSTEM-047 — BLK-test Fixed-Tool Pilot L4 Real-Repo Approval Boundary Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, `systematic-debugging`, and `code-review` when executing. This plan is guided by `docs/BLK-045_blk-system-post-042-roadmap.md` as the current roadmap, with `docs/BLK-024_blk-system-development-roadmap.md` retained for maturity lineage, then BLK-001 through BLK-006 and BLK-047/BLK-048/BLK-049 as applicable.

**Goal:** Create the BLK-test L4 real-repo approval boundary and fail-closed preflight fixture that can accept only a future exact-target approval envelope, without executing against any real repository in this sprint.

**BLK-045 fork:** Fork C — Complete the Right Side of the V-Model, verification frontier maturation.

**BLK-024 maturity lineage:** L4 pilot authority request / approval-boundary fixture only. Because the operator named the sprint but did not provide exact target repo/path/branch/workspace/runtime details, this sprint must remain L0/L1 approval-boundary plus fail-closed L4 preflight. It does not execute a real-repo pilot and does not grant L5 production BLK-test MCP authority.

**Architecture:** BLK-SYSTEM-046 proved one approval-bound L3 synthetic `run_ast_validation` evidence path and BLK-049 left L4 blocked pending exact target approval. BLK-SYSTEM-047 turns that block into a machine-checkable L4 approval-boundary contract: exact target identity, branch/worktree, source subtree, workspace clone identity, marker nonce, read-only profile, timeout/output limits, replay/expiry policy, operator stop controls, rollback/cleanup obligations, and hostile-review criteria must all be present before any future L4 runtime can start. With no exact target supplied in this request, the fixture must return a review/ready-or-blocked preflight record only and prove that no BLK-test fixed tool is executed.

**Tech Stack:** Markdown doctrine, Python deterministic approval-envelope/preflight fixture, unittest doctrine gates, hostile review, Go/Python verification.

**Authority boundary:** This sprint does not authorize production BLK-test MCP, generic BLK-test MCP, arbitrary shell, caller-supplied commands, dynamic tool expansion, package-manager/network/model/browser/cyber tooling, source/Git mutation by BLK-test, staging/commit/push/reset/stash/checkout/revert/autofix, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime RTM generation, RTM drift rejection, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.

---

## 0. Current Repository State at Planning

```text
Date: 2026-05-09T21:30:17+10:00
Branch: main...origin/main
HEAD: 97f49bd docs: close blk-system sprint 046 blk-test pilot
Remote HEAD: 97f49bdf562d068cb9d3efaa4d6ee06d5f199e07 refs/heads/main
Existing highest system plan: docs/plans/blk-system-046_blk-test-fixed-tool-pilot-l3-l4.md
Existing highest BLK boundary doc: docs/BLK-049_blk-test-fixed-tool-pilot-l3-l4-boundary.md
```

Discovery found no existing `BLK-SYSTEM-047`, `blk-system-047`, or `BLK-050` owner in the repository.

---

## 1. Operator Request and Approval Provenance

The current operator message explicitly requested:

```text
write the plan for the BLK-SYSTEM-047 - BLK-test Fixed-Tool Pilot L4 Real-Repo Approval Boundary and then execute all tasks
```

This is sprint-dispatch approval to plan and execute the approval-boundary work. It is not treated as real-repo runtime approval because it does not name the exact target repo/path/branch/workspace, rollback/cleanup obligations, timeout/output profile, replay/expiry policy, and operator stop details required by BLK-049.

Approved sprint scope:

```text
source_system: Discord DM with Camcamcam
operator_identity: camcamcami / Discord user 684235178083745819
sprint: BLK-SYSTEM-047
boundary_doc: BLK-050
approved_work: L4 real-repo approval-boundary doctrine plus deterministic fail-closed preflight fixture
runtime_execution: NOT_AUTHORIZED_THIS_SPRINT_WITHOUT_EXACT_TARGET_APPROVAL
fixed_tool: run_ast_validation only as a future approved L4 fixed-tool candidate
```

---

## 2. Governing Documents and Obligations

| Governing doc | Obligation for BLK-SYSTEM-047 |
| --- | --- |
| BLK-045 | Continue Fork C; mature BLK-test evidence before BEO publication or RTM. Do not add preparatory rungs unless they remove a concrete blocker. |
| BLK-049 | L4 remains blocked until exact target approval exists. Define the exact-target envelope before runtime starts. |
| BLK-048 | Preserve the selected BLK-test frontier and do not inherit Codex/BEO/RTM authority. |
| BLK-047 | Preserve BLK-test-specific approval, fixed-tool registry proof, source/evidence binding, replay protection, output bounds, cleanup, and operator stop controls. |
| BLK-017 / BLK-018 / BLK-019 / BLK-020 / BLK-025 | Preserve generic/production BLK-test disabled boundaries and historical first-smoke separation. |
| BLK-001 | BLK-test remains a verification evidence oracle only. |
| BLK-002 / BLK-005 / BLK-006 | Preserve protected-vault isolation and no protected body reads. |
| BLK-003 | Preserve human gates, hostile review, bounded context, and no implicit inheritance between execution, verification, publication, and RTM. |
| BLK-004 | Preserve BLK-pipe as source mutation/Git enforcement; BLK-test cannot mutate source or broaden allowlists. |

---

## 3. Implementation Surface

### New boundary document

```text
docs/BLK-050_blk-test-fixed-tool-pilot-l4-real-repo-approval-boundary.md
```

Required markers include:

```text
BLK_TEST_FIXED_TOOL_PILOT_L4_REAL_REPO_APPROVAL_BOUNDARY
L4_REAL_REPO_APPROVAL_BOUNDARY_ONLY_NO_RUNTIME_THIS_SPRINT
EXACT_TARGET_REPO_PATH_BRANCH_WORKSPACE_REQUIRED
READ_ONLY_FIXED_TOOL_RUN_AST_VALIDATION_ONLY
REAL_REPO_SOURCE_MUTATION_FORBIDDEN
PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN
BEO_PUBLICATION_AND_RTM_REMAIN_SEPARATE_AUTHORITIES
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_047
```

### New Python fixture

```text
python/blk_test_fixed_tool_pilot_l4_real_repo_approval_boundary.py
python/test_blk_test_fixed_tool_pilot_l4_real_repo_approval_boundary.py
```

The fixture must:

1. build deterministic L4 approval requests and approval records;
2. require exact target repo/path/branch/workspace identity;
3. reject primary repo, home/root paths, protected BLK-req prefixes, `.git` target paths, descendants containing `.git`, symlink escapes, and unowned workspace clones;
4. require read-only semantics, no mutation, no package/network/model/browser/cyber/shell authority;
5. reject authority-laundering strings and nested unsupported keys;
6. require caller-supplied replay sets and consume nothing when blocked;
7. return `BLK_TEST_L4_REAL_REPO_PREFLIGHT_READY_NOT_EXECUTED` only for a complete approval envelope;
8. return `L4_REAL_REPO_PILOT_BLOCKED_PENDING_EXACT_TARGET_APPROVAL` when exact approval is missing;
9. never execute `run_ast_validation` or any subprocess in this sprint.

### Persistent doctrine gate

Patch:

```text
python/test_active_doctrine_review_gates.py
```

with a BLK-050 path constant and a BLK-SYSTEM-047 doctrine marker test.

---

## 4. Tasks

### Task 0 — Plan publication

1. Write this plan.
2. Write `docs/outcomes/BLK-SYSTEM-047_task-000-outcome.md`.
3. Verify exact paths with `git diff --check` and Markdown fence balance.
4. Commit and push exact paths only.

### Task 1 — BLK-050 boundary and doctrine gate

1. Add failing active-doctrine test for BLK-050 required markers.
2. Verify RED against missing BLK-050.
3. Write BLK-050 boundary document.
4. Verify GREEN focused doctrine gate.
5. Write `docs/outcomes/BLK-SYSTEM-047_task-001-outcome.md`.
6. Commit and push exact paths only.

### Task 2 — L4 approval-boundary fixture

1. Add failing tests first for the approval envelope and blocked/runtime-denial behavior.
2. Verify RED because module/API is missing.
3. Implement minimal deterministic fixture.
4. Verify GREEN focused tests.
5. Write `docs/outcomes/BLK-SYSTEM-047_task-002-outcome.md`.
6. Commit and push exact paths only.

### Task 3 — Hostile review, remediation, and closeout

1. Run hostile review focused on authority laundering, real-repo path escape, replay/expiry, proof placeholders, and PASS-as-publication/RTM/coverage/drift laundering.
2. Remediate all blockers with tests first.
3. Run focused tests, full Python unittest discovery, `go test ./...`, `go vet ./...`, and `git diff --check`.
4. Write `docs/reviews/BLK-SYSTEM-047_blk-test-fixed-tool-pilot-l4-real-repo-approval-boundary-hostile-review.md`.
5. Write `docs/outcomes/BLK-SYSTEM-047_task-003-outcome.md` and `docs/outcomes/BLK-SYSTEM-047_sprint-closeout.md`.
6. Commit and push exact paths only.

---

## 5. Stop Conditions

Pause and require a new human approval if any task attempts to:

1. execute against a real repository as BLK-test runtime;
2. treat this sprint request as exact L4 target runtime approval;
3. start production or generic BLK-test MCP;
4. run arbitrary shell or caller-supplied commands;
5. mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source as BLK-test;
6. read, copy, parse, hash, summarize, scan, mutate, or compare protected BLK-req bodies;
7. publish authoritative BEOs;
8. generate RTM or reject drift;
9. call network/model/browser/cyber/package-manager tooling;
10. claim production isolation.

---

## 6. Definition of Done

BLK-SYSTEM-047 is complete when:

- BLK-050 exists and is pinned by a persistent doctrine gate;
- the L4 approval-boundary fixture has RED/GREEN tests proving complete-envelope readiness and missing-target blocking;
- no test or fixture starts live BLK-test runtime against a real repo;
- hostile review passes after any remediation;
- full verification passes;
- all outcome docs and closeout are committed and pushed to `origin/main`.
