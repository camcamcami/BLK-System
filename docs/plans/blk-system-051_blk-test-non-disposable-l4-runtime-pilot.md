# BLK-SYSTEM-051 — BLK-test Non-Disposable L4 Runtime Pilot Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, `systematic-debugging`, and hostile review while executing. This plan is guided by `docs/BLK-045_blk-system-post-042-roadmap.md` as the current post-042 roadmap, with BLK-024 retained for maturity vocabulary, then BLK-001 through BLK-006 and BLK-053 as applicable.

**Goal:** Execute exactly one approved non-disposable L4 BLK-test fixed-tool runtime pilot using only read-only `run_ast_validation` against the approved `/home/dad/BLK-System/python` target, returning evidence only.
**BLK-024 track:** Track F — BLK-test production-readiness ladder / maturity level L4 Pilot Runtime.
**Architecture:** BLK-001 keeps BLK-test as the right-side Physics Oracle. BLK-SYSTEM-051 activates only one bounded BLK-test runtime slice after BLK-SYSTEM-050 approval-envelope readiness. The runtime wrapper consumes the exact approval/run IDs before process start, verifies the non-disposable target and workspace clone boundary, runs AST validation on a wrapper-owned workspace clone, compares target source/Git snapshots before and after, cleans up the wrapper-owned workspace, and emits bounded evidence only.
**Tech Stack:** Markdown doctrine/outcomes, Python deterministic wrapper/tests, local Git metadata reads and local clone/copy mechanics, Python `ast.parse` fixed tool.
**Authority boundary:** L4 pilot runtime for one exact target only. Not production BLK-test MCP. Not generic BLK-test. Not reusable service startup. Not source/Git mutation. Not BEO publication. Not RTM generation. Not drift rejection.

---

## 0. Preflight State

```text
preflight_date: 2026-05-10T09:42:18+10:00
repo: /home/dad/BLK-System
branch: main...origin/main
head: 75e44c4 docs: close blk-system sprint 050 approval envelope
remote_main: 75e44c4066f7cbad38ed15afdc93a8eafd703340
```

## 1. Explicit Approved Runtime Envelope

The operator confirmed this exact normalized envelope:

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

Operator approval text:

```text
I approve one BLK-test non-disposable L4 runtime pilot using only read-only run_ast_validation against the exact target above.

This approval does not authorize source/Git mutation, production/generic BLK-test MCP, reusable BLK-test service startup, live Codex execution, arbitrary shell, caller-supplied commands, package-manager/network/model/browser/cyber tooling, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, BEO publication, RTM generation, drift rejection, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, or production isolation claims.
```

## 2. Scope

### In scope

1. Add BLK-054 as the active non-disposable L4 runtime boundary.
2. Add deterministic Python tests first for the runtime wrapper.
3. Add a deterministic wrapper that:
   - validates exact approval ID and run ID;
   - validates expiry and replay state before clone/process start;
   - validates target repo HEAD equals `75e44c4066f7cbad38ed15afdc93a8eafd703340` before runtime;
   - validates source subtree resolves inside the approved target and is not protected/secret/Git metadata;
   - rejects symlink escapes and descendant `.git` directories inside the source scope;
   - creates only the wrapper-owned workspace path under `/tmp/blk-system-051-non-disposable-l4-runtime-workspace`;
   - writes a structured workspace marker nonce before validation and verifies it before cleanup;
   - runs only `run_ast_validation` using Python `ast.parse` on `.py` files from the workspace copy;
   - snapshots source files and target `.git` metadata before and after runtime;
   - returns `PASS`, `FAIL`, or `BLOCKED` evidence only;
   - cleans the wrapper-owned workspace on success, failure, timeout, output overflow, or blocked evidence.
4. Execute the approved one-run pilot exactly once.
5. Store the returned evidence in BLK-SYSTEM-051 outcome documentation.
6. Run hostile authority review and remediate blockers.
7. Run focused and full verification, then commit and push exact paths.

### Out of scope / denied

BLK-SYSTEM-051 does not authorize:

- production BLK-test MCP;
- generic BLK-test MCP;
- reusable BLK-test service startup;
- any second or reusable non-disposable runtime run;
- live Codex execution;
- arbitrary shell or caller-supplied commands;
- wildcard fixed tools or dynamic tool expansion;
- package-manager, network, model-service, browser, or cyber tooling;
- source or Git mutation by BLK-test;
- protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison;
- authoritative BEO publication;
- runtime RTM generation or RTM drift rejection;
- public ledger mutation;
- signer, storage, rollback, revocation, supersession, or release authority;
- production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claims.

## 3. BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-SYSTEM-051 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Preserve BLK-test as evidence-only Physics Oracle. Do not let PASS become BEO publication, RTM generation, mutation, or approval authority. |
| BLK-002 — Artifact Lifecycle | Do not read or mutate protected BLK-req bodies or staging/active requirement artifacts. |
| BLK-003 — Orchestration Protocol | Preserve human approval gate, exact trace artifacts, hostile audit, and separate BEO/RTM approvals. |
| BLK-004 — BLK-pipe V47 Suite | Do not grant broad mutation/execution authority or arbitrary command expansion. BLK-pipe remains separate final source-mutation authority. |
| BLK-005 — BLK-Req Specification | Preserve canonical hash trace boundaries without reading protected requirement bodies. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny semantics and no tactical/BLK-test body-read access. |
| BLK-053 — Exact-Target Approval Envelope | Consume only the approved exact target envelope and maintain all denied adjacent authorities. |

## 4. Task Plan

### Task 000 — Publish plan

- Write this plan.
- Write `docs/outcomes/BLK-SYSTEM-051_task-000-outcome.md`.
- Verify Markdown fences and `git diff --check`.
- Commit and push exact plan/outcome paths.

### Task 001 — Boundary doctrine and persistent gate

- Add `docs/BLK-054_blk-test-non-disposable-l4-runtime-pilot-boundary.md`.
- Patch `python/test_active_doctrine_review_gates.py` to require BLK-054 and BLK-SYSTEM-051 markers.
- RED: focused gate fails before BLK-054 exists.
- GREEN: focused gate passes after BLK-054.
- Write `docs/outcomes/BLK-SYSTEM-051_task-001-outcome.md`.

### Task 002 — Runtime wrapper TDD

- Add failing tests in `python/test_blk_test_non_disposable_l4_runtime_pilot.py` before production code.
- Implement `python/blk_test_non_disposable_l4_runtime_pilot.py` minimally.
- Required tests include:
  - exact approval/run replay is consumed before workspace/process start;
  - wrong/expired approval blocks before workspace creation;
  - target HEAD mismatch blocks;
  - source path outside target, protected descendants, `.git` descendants, secrets, and symlink escapes block;
  - wrong tool blocks;
  - output cap/timeout produce non-success evidence and cleanup;
  - source tree and target Git metadata are unchanged after PASS/FAIL;
  - PASS evidence remains evidence-only and does not publish BEO/RTM or claim production isolation.
- Write `docs/outcomes/BLK-SYSTEM-051_task-002-outcome.md`.

### Task 003 — Execute approved one-run pilot

- Execute exactly one approved runtime run using:

```text
target_repo_path: /home/dad/BLK-System
source_subtree_path: /home/dad/BLK-System/python
branch_or_worktree: main at 75e44c4066f7cbad38ed15afdc93a8eafd703340
workspace_clone_path: /tmp/blk-system-051-non-disposable-l4-runtime-workspace
approval_id: APPROVAL-BLK-SYSTEM-051-001
run_id: RUN-BLK-SYSTEM-051-001
fixed_tool: run_ast_validation
```

- Record evidence in `docs/outcomes/BLK-SYSTEM-051_task-003-outcome.md`.
- Do not rerun the approved runtime after success; use synthetic tests for later remediation.

### Task 004 — Hostile review and remediation

- Run hostile authority review over BLK-054, wrapper, tests, plan, and runtime evidence.
- Remediate blockers using synthetic tests only unless a new explicit runtime approval is provided.
- Write `docs/reviews/BLK-SYSTEM-051_blk-test-non-disposable-l4-runtime-hostile-review.md`.
- Write `docs/outcomes/BLK-SYSTEM-051_task-004-outcome.md`.

### Task 005 — Final verification and closeout

- Run focused tests, doctrine gates, full Python suite, Go tests/vet, and `git diff --check`.
- Write `docs/outcomes/BLK-SYSTEM-051_sprint-closeout.md`.
- Commit and push exact changed paths.

## 5. Stop Conditions

Stop and require a new human decision if:

1. the approved target path, source subtree, branch/head, workspace, approval ID, run ID, tool, or expiry differs;
2. target HEAD differs from `75e44c4066f7cbad38ed15afdc93a8eafd703340` before runtime;
3. the source subtree contains protected BLK-req, Git metadata, secret, or symlink-escape descendants;
4. the wrapper cannot prove source tree and target Git metadata are unchanged;
5. evidence output exceeds the cap or validation times out;
6. hostile review finds a blocker that would require rerunning the approved runtime;
7. any code path attempts BEO publication, RTM generation, drift rejection, source/Git mutation, live Codex, arbitrary shell, package/network/model/browser/cyber tooling, or protected-body reads.

## 6. Expected Positive State

```text
BLK_TEST_NON_DISPOSABLE_L4_RUNTIME_PILOT_PASS_EVIDENCE_ONLY
```

This means only that the approved one-run `run_ast_validation` pilot returned bounded evidence and did not mutate the target source/Git state. It is not production BLK-test MCP, BEO publication, RTM generation, drift truth, protected-vault truth, live Codex approval, or production isolation evidence.
