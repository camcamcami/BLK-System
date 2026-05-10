# BLK-SYSTEM-053 — Repeatable Non-Disposable L4 Wrapper Approvals Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, `test-driven-development`, and hostile review while executing. This plan is guided by `docs/BLK-045_blk-system-post-042-roadmap.md` as current roadmap, with `docs/BLK-024_blk-system-development-roadmap.md` retained for maturity vocabulary, then BLK-001 through BLK-006 as applicable.

**Goal:** Clean up the non-disposable L4 runtime wrapper so future fresh approvals can bind their own sprint/nonce/workspace/ledger envelope without mixed historical nonce text, while adding no new runtime authority.
**BLK-024 / BLK-045 track:** Track F / Fork C — BLK-test production-readiness ladder; maturity level L1/L2 wrapper hardening and approval-envelope fixture support, not an L4 runtime run.
**Architecture:** BLK-SYSTEM-052 proved one fresh L4 `run_ast_validation` PASS but exposed a maintainability wart: the committed wrapper still had BLK-SYSTEM-051-specific nonce and marker strings. BLK-SYSTEM-053 must parameterize those sprint-specific bindings behind a typed exact approval envelope, preserve all hardened replay/path/mutation/evidence controls, and keep legacy BLK-SYSTEM-051 behavior tested. It must not execute another non-disposable runtime pilot.
**Tech Stack:** Python runtime wrapper/tests, Markdown boundary/outcomes, active doctrine gate.
**Authority boundary:** Local wrapper hardening only. No production/generic BLK-test MCP, no reusable BLK-test service, no new non-disposable runtime run, no BEO publication, no RTM generation, and no source/Git mutation authority.

---

## 1. Current Known State

Preflight:

```text
date: 2026-05-10T11:47:54+10:00
git status --short --branch: ## main...origin/main
git log -1 --oneline: c4d6733 docs: close blk-system sprint 052 runtime pass
git rev-parse HEAD: c4d6733d4e1bbafa80d9dd6135f43d972ac55711
```

BLK-SYSTEM-052 result:

```text
BLK_TEST_NON_DISPOSABLE_L4_RUNTIME_PILOT_PASS_EVIDENCE_ONLY
```

BLK-SYSTEM-052 hostile review accepted the mixed `BLK-SYSTEM-051`/`BLK-SYSTEM-052` nonce compatibility detail as non-blocking because all authority-bearing fields were bound to BLK-SYSTEM-052. It recommended future wrapper cleanup so fresh approvals no longer require mixed historical nonce text.

---

## 2. Governing Doctrine Alignment

- **BLK-045 / BLK-024:** This is controlled support work for Fork C / Track F after a successful fixed-tool L4 pilot. It removes a concrete activation wart rather than adding another authority rung.
- **BLK-001:** Preserves BLK-test as a physics/evidence oracle. The wrapper must not become planner, publisher, mutator, or trace-closure authority.
- **BLK-002 / BLK-005 / BLK-006:** No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, active-vault comparison, or drift decision are authorized.
- **BLK-003:** Generic/live BLK-test MCP remains disabled. Fixed-tool execution remains available only under separately approved exact one-run envelopes.
- **BLK-004:** BLK-pipe mutation authority remains separate. The wrapper must not stage, commit, push, reset, stash, checkout, revert, or autofix as BLK-test behavior.
- **BLK-054 / BLK-055:** Prior one-run runtime boundaries remain consumed historical evidence. BLK-SYSTEM-053 must not reopen or rerun BLK-SYSTEM-051 or BLK-SYSTEM-052 IDs.

---

## 3. Non-Authority Boundary

This plan does not authorize production BLK-test MCP, generic BLK-test MCP, reusable BLK-test service startup, arbitrary repositories, arbitrary shell, caller-supplied commands, dynamic tool expansion, source/Git mutation by BLK-test, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime RTM generation, RTM drift rejection, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, package-manager/network/model/browser/cyber tooling, live Codex execution, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.

---

## 4. Implementation Intent

The wrapper should gain a typed approval-envelope configuration, expected to include at least:

```text
sprint
approval_id
run_id
expected_head
approved_target_repo
approved_source_subtree
approved_workspace
replay_ledger_path
marker_nonce_binding
workspace_marker_name
fixed_tool
```

The legacy global constants must remain supported for BLK-SYSTEM-051 tests and historical callers, but future wrapper calls should be able to pass a fresh envelope without monkey-patching module globals or embedding `BLK-SYSTEM-051` in the nonce.

Required safety preservation:

1. exact path spelling checks before resolution;
2. exact approved resolved path checks;
3. exact approved HEAD checks;
4. fixed tool only;
5. caller replay sets required;
6. durable replay ledger plus process-local replay sets;
7. pre-owned workspace rejection;
8. protected/source/secret/symlink scope rejection;
9. source and `.git` content/metadata snapshots, including root directories and symlink payloads;
10. bounded evidence and accurate byte accounting;
11. evidence-only denial flags for BEO/RTM/MCP/source-mutation authority.

---

## 5. Task Plan

### Task 000 — Plan and publish this sprint plan

Deliverables:

```text
docs/plans/blk-system-053_repeatable-non-disposable-l4-wrapper-approvals.md
docs/outcomes/BLK-SYSTEM-053_task-000-outcome.md
```

Actions:

1. Record preflight state and governing docs.
2. Publish the plan and Task 000 outcome via exact-path commit/push.
3. Do not modify runtime code in Task 000.

### Task 001 — Parameterized approval envelope via TDD

Deliverables:

```text
python/blk_test_non_disposable_l4_runtime_pilot.py
python/test_blk_test_non_disposable_l4_runtime_pilot.py
docs/outcomes/BLK-SYSTEM-053_task-001-outcome.md
```

Actions:

1. Add RED tests proving a fresh envelope can use its own sprint, nonce binding, marker name, workspace, and ledger without BLK-SYSTEM-051 text.
2. Add RED tests proving mismatched envelope fields fail closed and legacy BLK-SYSTEM-051 wrapper behavior remains intact.
3. Implement the smallest GREEN change: a typed envelope object plus helper call path.
4. Verify focused runtime tests.
5. Do not run a real non-disposable target pilot.

### Task 002 — Boundary doc, doctrine gate, and hostile review

Deliverables:

```text
docs/BLK-056_repeatable-non-disposable-l4-wrapper-approval-boundary.md
python/test_active_doctrine_review_gates.py
docs/reviews/BLK-SYSTEM-053_repeatable-non-disposable-l4-wrapper-approvals-hostile-review.md
docs/outcomes/BLK-SYSTEM-053_task-002-outcome.md
```

Actions:

1. Add BLK-056 boundary markers proving this is wrapper hardening only, not fresh runtime authority.
2. Add persistent active doctrine gate coverage for BLK-056.
3. Hostile-review code, tests, and docs for authority laundering, replay bypass, path/HEAD substitution, generic runtime service creep, and BEO/RTM/source-mutation claims.
4. Remediate blockers with synthetic tests only.

### Task 003 — Verification, closeout, commit, and push

Deliverables:

```text
docs/outcomes/BLK-SYSTEM-053_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-053_sprint-closeout.md
```

Actions:

1. Run focused wrapper tests, active doctrine gates, full Python discovery, Go tests, Go vet, and `git diff --check`.
2. Record final verification output.
3. Stage exact paths only.
4. Commit and push to `origin/main`.
5. Report final commit hash.

---

## 6. Stop Conditions

Stop and report before final closeout if any implementation:

1. executes a real non-disposable runtime pilot;
2. reuses BLK-SYSTEM-051 or BLK-SYSTEM-052 approval/run IDs;
3. weakens exact path spelling, exact HEAD, replay, output, source snapshot, or `.git` snapshot checks;
4. permits caller-supplied commands or non-`run_ast_validation` tools without a separate fixed-tool authority boundary;
5. stages, commits, pushes, mutates source, or mutates `.git` as BLK-test behavior;
6. claims production/generic BLK-test MCP, reusable runtime service, BEO publication, RTM generation, drift rejection, protected-body read, live Codex, package/network/model/browser/cyber tooling, or production isolation authority;
7. fails hostile review or full verification.
