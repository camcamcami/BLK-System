# BLK-SYSTEM-048 — BLK-test Fixed-Tool L4 Disposable Real-Repo Runtime Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, `systematic-debugging`, and `code-review` when executing. This plan is guided by `docs/BLK-045_blk-system-post-042-roadmap.md` as current roadmap, with `docs/BLK-024_blk-system-development-roadmap.md` retained for maturity lineage, then BLK-001 through BLK-006 and BLK-047/BLK-048/BLK-049/BLK-050 as applicable.

**Goal:** Execute the smallest safe L4 BLK-test fixed-tool pilot by running read-only `run_ast_validation` against an exact-target disposable real Git repository created by the sprint harness, then stop before production/generic BLK-test authority.

**BLK-045 fork:** Fork C — Complete the Right Side of the V-Model, verification frontier maturation.

**BLK-024 maturity lineage:** L4 pilot runtime, limited to one disposable exact-target real-repo fixture created by the sprint harness. This is not L5 production BLK-test MCP authority and not authority to run against `/home/dad/BLK-System` or arbitrary real repositories.

**Architecture:** BLK-SYSTEM-047 created BLK-050 and a strict exact-target L4 preflight fixture. BLK-SYSTEM-048 uses that preflight boundary to generate a disposable real Git repository target, bind it to a structured workspace marker and approval envelope, consume replay IDs before execution, run only in-process Python AST validation over approved `.py` files, verify no source/Git mutation, return evidence only, and keep BEO/RTM/publication/drift authorities disabled.

**Tech Stack:** Markdown doctrine, Python deterministic approval/runtime fixture, unittest, Go verification.

**Authority boundary:** This sprint authorizes one harness-owned disposable real-repo L4 fixed-tool runtime path only. It does not authorize production BLK-test MCP, generic BLK-test MCP, arbitrary shell, caller-supplied commands, dynamic tool expansion, package-manager/network/model/browser/cyber tooling, execution against `/home/dad/BLK-System` as a target, execution against arbitrary operator repos, source/Git mutation by BLK-test, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime RTM generation, RTM drift rejection, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.

---

## 0. Current Repository State at Planning

```text
Date: 2026-05-10T07:10:22+10:00
Branch: main...origin/main
HEAD: 4960dbc docs: close blk-system sprint 047 l4 approval boundary
Remote HEAD: 4960dbcdd111d4152fc927578041d7a1936d4b48 refs/heads/main
Existing highest system plan: docs/plans/blk-system-047_blk-test-fixed-tool-pilot-l4-real-repo-approval-boundary.md
Existing highest BLK boundary doc: docs/BLK-050_blk-test-fixed-tool-pilot-l4-real-repo-approval-boundary.md
```

Discovery found no existing `BLK-SYSTEM-048`, `blk-system-048`, or `BLK-051` owner in the repository.

---

## 1. Operator Request and Runtime Approval Provenance

The current operator message requested:

```text
write the plan for the next logical blk-system sprint and then execute all tasks
```

After BLK-SYSTEM-047, the next logical BLK-test step is the first L4 runtime sprint, but only if it supplies an exact target. This plan narrows the exact target to a disposable real Git repository created inside the sprint harness. The operator message is therefore treated as sprint-dispatch approval for this specific disposable-target L4 pilot only, not for arbitrary real repositories.

Approved runtime envelope for this sprint:

```text
source_system: Discord DM with Camcamcam
operator_identity: camcamcami / Discord user 684235178083745819
sprint: BLK-SYSTEM-048
boundary_doc: BLK-051
approved_runtime_slice: L4_DISPOSABLE_REAL_REPO_RUN_AST_VALIDATION_ONLY_THIS_SPRINT
approved_target_class: disposable real Git repository created by the BLK-SYSTEM-048 test/runtime harness
approved_tool: run_ast_validation
approval_consumption: approval_id and run_id consumed before fixed-tool execution
```

---

## 2. Governing Documents and Obligations

| Governing doc | Obligation for BLK-SYSTEM-048 |
| --- | --- |
| BLK-045 | Continue Fork C; mature BLK-test evidence before BEO publication or RTM. |
| BLK-050 | Use exact target repo/path/branch/workspace approval, structured workspace marker, replay/expiry, cleanup/rollback, and hostile-review criteria before runtime. |
| BLK-049 | Preserve fixed-tool registry and no production/generic BLK-test MCP. |
| BLK-047 | Preserve BLK-test-specific approval and no adjacent authority inheritance. |
| BLK-048 | Preserve selected BLK-test frontier and no Codex/BEO/RTM authority inheritance. |
| BLK-017 / BLK-018 / BLK-019 / BLK-020 / BLK-025 | Preserve generic/production BLK-test disabled boundaries and historical first-smoke separation. |
| BLK-001 | BLK-test remains verification evidence only. |
| BLK-002 / BLK-005 / BLK-006 | Preserve protected-vault isolation and no protected body reads. |
| BLK-003 | Preserve human gates, hostile review, bounded context, and no implicit inheritance between execution, verification, publication, and RTM. |
| BLK-004 | Preserve BLK-pipe as source mutation/Git enforcement; BLK-test cannot mutate source or broaden allowlists. |

---

## 3. Implementation Surface

### New boundary document

```text
docs/BLK-051_blk-test-fixed-tool-l4-disposable-real-repo-runtime-boundary.md
```

Required markers include:

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

### New runtime fixture

```text
python/blk_test_fixed_tool_l4_disposable_repo_runtime.py
python/test_blk_test_fixed_tool_l4_disposable_repo_runtime.py
```

The fixture must:

1. create or consume an exact approval envelope compatible with BLK-050;
2. validate target repo, source subtree, workspace marker, timeout/output profile, replay/expiry, and denied authorities;
3. consume replay IDs before runtime;
4. run only `run_ast_validation` in-process, without subprocess or shell;
5. parse approved `.py` files with `ast.parse`;
6. return PASS for valid syntax, FAIL for syntax errors, and BLOCKED for policy/preflight failures;
7. snapshot the approved source tree before/after and prove no source/Git mutation;
8. preserve `beo_publication: DRAFT_ONLY`, `rtm_status: NOT_GENERATED`, `active_vault_read: false`, and `production_isolation_claimed: false`.

---

## 4. Tasks

### Task 0 — Plan publication

1. Write this plan.
2. Write `docs/outcomes/BLK-SYSTEM-048_task-000-outcome.md`.
3. Verify exact paths with `git diff --check` and Markdown fence balance.
4. Commit and push exact paths only.

### Task 1 — BLK-051 boundary and doctrine gate

1. Add failing active-doctrine test for BLK-051 markers.
2. Verify RED against missing BLK-051.
3. Write BLK-051 boundary.
4. Verify GREEN focused doctrine gate.
5. Write `docs/outcomes/BLK-SYSTEM-048_task-001-outcome.md`.
6. Commit and push exact paths only.

### Task 2 — L4 disposable real-repo runtime fixture

1. Add failing tests first for PASS, FAIL, replay, no-mutation, target rejection, and PASS-as-publication/RTM laundering.
2. Verify RED because the module/API is missing.
3. Implement minimal deterministic runtime fixture.
4. Verify GREEN focused tests and related BLK-test tests.
5. Write `docs/outcomes/BLK-SYSTEM-048_task-002-outcome.md`.
6. Commit and push exact paths only.

### Task 3 — Hostile review, remediation, and closeout

1. Run hostile review focused on runtime authority laundering, path escape, replay consumption, source/Git mutation, protected body leakage, and PASS-as-publication/RTM/coverage/drift laundering.
2. Remediate all blockers with tests first.
3. Run focused tests, full Python unittest discovery, `go test ./...`, `go vet ./...`, and `git diff --check`.
4. Write hostile review, Task 003 outcome, and sprint closeout.
5. Commit and push exact paths only.

---

## 5. Stop Conditions

Pause and require a new human approval if any task attempts to:

1. run against `/home/dad/BLK-System` or an arbitrary external repository;
2. treat BLK-SYSTEM-048 as production/generic BLK-test MCP authority;
3. run arbitrary shell, caller-supplied commands, package managers, network, model-service, browser, or cyber tooling;
4. mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source as BLK-test;
5. read, copy, parse, hash, summarize, scan, mutate, or compare protected BLK-req bodies;
6. publish authoritative BEOs;
7. generate RTM or reject drift;
8. claim production isolation.

---

## 6. Definition of Done

BLK-SYSTEM-048 is complete when:

- BLK-051 exists and is pinned by a persistent doctrine gate;
- the runtime fixture executes only against a harness-owned disposable exact-target real Git repository;
- PASS/FAIL evidence is generated by read-only AST validation;
- replay IDs are consumed before runtime;
- before/after source snapshots prove no source/Git mutation;
- hostile review passes after any remediation;
- full verification passes;
- all outcome docs and closeout are committed and pushed to `origin/main`.
