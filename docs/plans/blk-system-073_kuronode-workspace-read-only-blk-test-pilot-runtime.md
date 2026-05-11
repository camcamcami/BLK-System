# BLK-SYSTEM-073 — Kuronode Workspace Read-Only BLK-test Pilot Runtime Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, `test-driven-development`, and `code-review` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, `docs/BLK-059_blk-system-post-058-roadmap.md` for current roadmap selection, BLK-001 through BLK-006, and BLK-071 through BLK-073 for the Kuronode exact-target chain.

**Goal:** Execute exactly one read-only BLK-test functional-module pilot over the now-pushed Kuronode workspace target using fixed `run_ast_validation` evidence only.
**BLK-024 track:** Track F — BLK-test production-readiness ladder; maturity level L4 pilot runtime, but single-use/read-only/evidence-only.
**Architecture:** BLK-SYSTEM-071 created the Kuronode request package. BLK-SYSTEM-072 created the review-only exact-target approval envelope. The user then authorized the Kuronode commit push and asked to execute the next logical BLK-System sprint, which is the one-run read-only BLK-test module pilot. BLK-test remains a BLK-System functional module, not BLK-System's test suite.
**Tech Stack:** Python `unittest`; deterministic file/snapshot logic; Kuronode real workspace read-only source reads; no TypeScript tooling, package manager, Electron, browser, network, Codex, BLK-pipe, BEO, RTM, or protected-body access.
**Authority boundary:** One exact L4 read-only pilot run over `/home/dad/code/Kuronode-v1` at HEAD `38e332b188e45edcb484765694112c9041ad1a3b`; source/Git mutation forbidden; replay IDs consumed before runtime; evidence-only result may be PASS/FAIL/BLOCKED.

---

## 0. Current Known State

Captured at planning time:

```text
date: 2026-05-11T12:29:53+10:00
BLK-System status: ## main...origin/main
BLK-System HEAD: bd5c4eb docs: close out blk-system 072 approval envelope
BLK-System remote main: bd5c4eb780dcd32fcb206548744ed4c433f542d2 refs/heads/main
Kuronode status: ## main...origin/main
Kuronode local HEAD: 38e332b188e45edcb484765694112c9041ad1a3b
Kuronode remote main: 38e332b188e45edcb484765694112c9041ad1a3b refs/heads/main
```

The Kuronode CEB_009 patch is now pushed to `origin/main`; this sprint must still re-check exact local and remote target identity immediately before runtime.

---

## 1. Governing Documents

- **BLK-024:** Track F maturity ladder. This sprint is a narrow L4 pilot, not production authority.
- **BLK-059:** Current post-058 roadmap and authority posture.
- **BLK-001:** Preserves separation between BLK-test evidence, source mutation, BEO publication, RTM trace closure, and operator decisions.
- **BLK-002 / BLK-005 / BLK-006:** Protected BLK-req body hard-deny remains active; no protected-body reads, copies, hashes, scans, or drift comparisons.
- **BLK-003:** Requires human dispatch gates and keeps BLK-test/BEO/RTM authority separate.
- **BLK-004:** Informs exact allowlists, output caps, replay, and no broad staging/mutation rules.
- **BLK-072 / BLK-SYSTEM-071:** Upstream request package.
- **BLK-073 / BLK-SYSTEM-072:** Review-only exact-target approval envelope and hostile hardening.

---

## 2. Runtime Authorization Captured by This Plan

This plan treats the current operator request — “write the plan for the next logical blk-system sprint and then execute all tasks” after authorizing the Kuronode commit — as explicit authorization to execute this one BLK-SYSTEM-073 read-only pilot, bounded by the exact parameters below.

Runtime identifiers:

```text
approval_id: APPROVAL-BLK-SYSTEM-073-KURONODE-WORKSPACE-001
run_id: RUN-BLK-SYSTEM-073-KURONODE-WORKSPACE-001
target_repo_path: /home/dad/code/Kuronode-v1
source_subtree_path: /home/dad/code/Kuronode-v1/scripts
workspace_clone_path: /tmp/blk-system-073-kuronode-workspace-read-only-pilot-workspace
replay_ledger_path: /tmp/blk-system-073-kuronode-workspace-read-only-pilot-replay-ledger.json
expected_head: 38e332b188e45edcb484765694112c9041ad1a3b
fixed_tool: run_ast_validation
output_byte_limit: 16384
```

If any target identity or replay precondition fails, the pilot must close as BLOCKED evidence-only, not retarget or rerun.

---

## 3. Explicit Non-Authority Boundary

This sprint does not authorize:

- production BLK-test MCP;
- generic BLK-test MCP;
- reusable BLK-test service startup;
- arbitrary shell or caller-supplied commands as BLK-test behavior;
- dynamic tool expansion;
- Electron launch, Playwright launch, smoke-test execution, TypeScript compiler, linter, formatter, package-manager invocation, network/model/browser/cyber tooling;
- Kuronode source mutation;
- Kuronode Git mutation, staging, commit, push, reset, checkout, revert, stash, cleanup, autofix, or remote writes by BLK-test;
- reuse of CEB_009/BLK-SYSTEM-070/071 artifacts as executable fixture authority;
- BLK-test as BLK-System test-suite semantics;
- protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison;
- authoritative BEO publication;
- runtime `PUBLISHED` BEO output;
- RTM generation;
- RTM drift rejection;
- coverage matrix/coverage-claim promotion;
- active-vault hash comparison;
- public ledger mutation;
- signer/storage/rollback/revocation/supersession/release authority;
- production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claims.

---

## 4. Deliverables

1. `python/blk_test_kuronode_workspace_read_only_pilot_runtime.py`
2. `python/test_blk_test_kuronode_workspace_read_only_pilot_runtime.py`
3. `docs/BLK-074_blk-test-kuronode-workspace-read-only-pilot-runtime-boundary.md`
4. Active doctrine gate updates in `python/test_active_doctrine_review_gates.py`
5. Runtime evidence JSON under `docs/outcomes/BLK-SYSTEM-073_runtime-evidence.json`
6. Per-task outcomes under `docs/outcomes/`
7. Hostile review under `docs/reviews/`
8. Sprint closeout under `docs/outcomes/BLK-SYSTEM-073_sprint-closeout.md`

---

## 5. Task Plan

### Task 000 — Plan publication

Create this plan and Task 000 outcome. Verify balanced Markdown fences and `git diff --check`, then exact-path commit and push.

### Task 001 — Runtime runner, RED/GREEN

Add RED tests first for a BLK-SYSTEM-073 read-only pilot runner that:

- consumes a validated BLK-SYSTEM-072 upstream envelope as review evidence, without treating it as runtime approval;
- validates explicit BLK-SYSTEM-073 runtime authorization;
- requires exact local target path/head/branch context and exact source subtree spelling;
- requires exact remote `origin/main` head evidence before runtime;
- requires caller-owned replay sets, durable ledger, and process-local replay protection;
- consumes replay IDs before runtime after static validation;
- rejects path aliases, pre-owned workspaces, secret/protected descendants, source/Git mutation surfaces, output caps below minimum, and stale/expired approvals;
- copies only the approved source subtree to a wrapper-owned temp workspace;
- executes fixed read-only `run_ast_validation` by parsing/evaluating copied `.ts`/`.tsx` source descriptors only;
- records pre/post source and `.git` metadata hashes;
- verifies workspace cleanup;
- bounds JSON evidence and records actual serialized byte size.

### Task 002 — BLK-074 boundary and active doctrine gate

Create BLK-074 and a persistent active doctrine gate that asserts BLK-SYSTEM-073 is exactly one read-only evidence pilot, not production BLK-test MCP, not a BLK-System test suite, not mutation, not publication, not RTM, not protected-body access, and not production isolation proof.

### Task 003 — Execute one approved pilot

Before runtime:

1. re-check BLK-System clean state;
2. re-check Kuronode local and remote HEAD equal `38e332b188e45edcb484765694112c9041ad1a3b`;
3. check the BLK-SYSTEM-073 replay ledger is not already consumed;
4. run the exact approved runtime once;
5. write `docs/outcomes/BLK-SYSTEM-073_runtime-evidence.json`;
6. verify post-run Kuronode status remains clean and HEAD unchanged.

If the run returns FAIL, document the evidence as a legitimate BLK-test finding. If it returns BLOCKED, do not rerun with the same IDs.

### Task 004 — Hostile review and remediation

Hostile-review focus:

- PASS-as-runtime-production laundering;
- BLK-test as BLK-System test-suite wording;
- replay reuse and ledger deletion;
- stale target HEAD or remote mismatch;
- path alias and pre-owned workspace handling;
- source and `.git` mutation detection;
- secret/protected descendant rejection;
- output cap truthfulness;
- fixed-tool and no-tool-expansion enforcement;
- BEO/RTM/coverage/drift/publication inheritance.

Remediate blockers with tests/docs before closeout.

### Task 005 — Final verification and closeout

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_kuronode_workspace_read_only_pilot_runtime -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint073_blk_test_kuronode_workspace_read_only_pilot_runtime_is_evidence_only -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest discover python 'test_*.py'
go test ./...
git diff --check
```

Write closeout, exact-path commit, push, and verify remote.

---

## 6. Stop Conditions

Stop and report instead of broadening scope if:

- Kuronode local or remote HEAD differs from `38e332b188e45edcb484765694112c9041ad1a3b`;
- the BLK-SYSTEM-073 approval/run IDs were already consumed;
- runtime would require Electron, Playwright, smoke tests, TypeScript tooling, package managers, network, browser/model/cyber tooling, Codex, or BLK-pipe;
- source/Git mutation is needed or detected;
- protected BLK-req body access is needed or detected;
- output bounds cannot honestly contain evidence;
- any wording treats BLK-test as a BLK-System test suite;
- any step needs BEO publication, RTM generation, coverage/drift truth, or production BLK-test MCP.
