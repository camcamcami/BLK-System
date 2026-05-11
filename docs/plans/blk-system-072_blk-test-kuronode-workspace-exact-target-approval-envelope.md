# BLK-SYSTEM-072 — BLK-test Kuronode Workspace Exact-Target Approval Envelope Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, `test-driven-development`, and `code-review` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, `docs/BLK-059_blk-system-post-058-roadmap.md` for current roadmap selection, and BLK-001 through BLK-006 plus BLK-072 for authority boundaries.

**Goal:** Create a fresh exact-target approval-envelope review package for a future read-only BLK-test functional-module pilot over the Kuronode workspace, without executing the pilot.
**BLK-024 track:** Track F — BLK-test production-readiness ladder; Track J — capability hardening / maturity level L0/L1 approval-envelope fixture only.
**Architecture:** BLK-SYSTEM-071 produced request readiness for a future Kuronode workspace BLK-test module pilot. This sprint creates the next safe rung: a review-only exact-target approval envelope that binds the BLK-SYSTEM-071 request package, target identity, future approval/run IDs, proof obligations, replay policy, output bounds, and denied authorities. It remains non-runtime and does not approve or execute BLK-test runtime.
**Tech Stack:** Markdown doctrine/outcomes; Python `unittest` fixture validators; no package-manager, Electron, TypeScript, smoke-test, Codex, BLK-pipe, or live BLK-test MCP execution.
**Authority boundary:** L0/L1 exact-target approval-envelope fixture only. No runtime, no live BLK-test MCP, no Kuronode source/Git mutation, no CEB_009 artifact reuse, no remote push, no BEO publication, no RTM generation.

---

## 0. Current Known State

Captured at planning time:

```text
date: 2026-05-11T11:37:37+10:00
BLK-System status: ## main...origin/main
BLK-System HEAD: 1210a9c docs: close out blk-system 071 kuronode workspace request
BLK-System remote main: 1210a9c980dff29109ea1b0ddc3f027cc6a84ca7 refs/heads/main
Kuronode status: ## main...origin/main [ahead 1]
Kuronode HEAD: 38e332b188e45edcb484765694112c9041ad1a3b
```

The Kuronode workspace is local-ahead-one from the prior CEB_009 patch. This sprint does not push, patch, reset, clean, fetch, checkout, or otherwise mutate Kuronode.

---

## 1. Governing Documents

- **BLK-024:** Supplies maturity ladder vocabulary; this sprint remains L0/L1 fixture-only/review-only.
- **BLK-059:** Current roadmap; keeps production/generic BLK-test MCP, reusable service startup, arbitrary shell, source/Git mutation by BLK-test, protected body reads, BEO publication, RTM generation, package-manager/network/model/browser/cyber tooling, and production isolation claims unauthorized.
- **BLK-001:** Separates BLK-test evidence from mutation, publication, and trace closure authority.
- **BLK-002 / BLK-005 / BLK-006:** Protect BLK-req bodies; this sprint does not read, copy, scan, hash, summarize, mutate, or compare protected BLK-req bodies.
- **BLK-003:** Requires human dispatch gates and prevents BLK-test/BEO/RTM authority inheritance.
- **BLK-004:** Preserves deterministic enforcement and exact allowlists; this sprint does not invoke BLK-pipe.
- **BLK-047 through BLK-056:** Prior BLK-test ladder boundaries. This sprint follows the exact-target approval-envelope pattern but targets Kuronode and remains non-runtime.
- **BLK-072 / BLK-SYSTEM-071:** Immediate upstream request readiness. BLK-SYSTEM-072 must bind and verify the BLK-SYSTEM-071 request package and preserve the BLK-test module naming correction.

---

## 2. Explicit Non-Authority Boundary

This plan does not authorize:

- production BLK-test MCP;
- generic BLK-test MCP;
- reusable BLK-test service startup;
- BLK-test runtime execution against Kuronode;
- runtime approval;
- arbitrary shell or caller-supplied commands as BLK-test behavior;
- dynamic tool expansion;
- Electron launch, smoke-test execution, TypeScript tooling, formatter, linter, typechecker, package-manager invocation, network, model-service, browser, or cyber tooling;
- Kuronode source mutation;
- Kuronode Git mutation, staging, commit, push, reset, checkout, revert, stash, cleanup, or autofix;
- reuse of CEB_009 approval IDs, run IDs, BLK-pipe payloads/reports, patch authority, or static-pilot artifacts as executable BLK-test fixture inputs;
- BLK-test as BLK-System test-suite semantics;
- protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison;
- authoritative BEO publication;
- runtime `PUBLISHED` BEO output;
- RTM generation;
- RTM drift rejection;
- coverage matrix/coverage-claim promotion;
- active-vault hash comparison;
- signer/storage/ledger/rollback/revocation/supersession/release authority;
- production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claims.

---

## 3. Deliverables

1. `python/blk_test_kuronode_workspace_exact_target_approval_envelope.py`
2. `python/test_blk_test_kuronode_workspace_exact_target_approval_envelope.py`
3. `docs/BLK-073_blk-test-kuronode-workspace-exact-target-approval-envelope-boundary.md`
4. Active doctrine gate updates in `python/test_active_doctrine_review_gates.py`
5. Per-task outcomes under `docs/outcomes/`
6. Hostile review under `docs/reviews/`
7. Sprint closeout under `docs/outcomes/BLK-SYSTEM-072_sprint-closeout.md`

---

## 4. Task Plan

### Task 000 — Plan publication

Create this plan and Task 000 outcome. Verify Markdown fences and `git diff --check`, then exact-path commit and push.

### Task 001 — Exact-target approval-envelope fixture, RED/GREEN

Add RED tests first for a validator that consumes a BLK-SYSTEM-071 request package and exact-target approval-envelope proposal.

Required behaviors:

- complete package returns `BLK_TEST_KURONODE_WORKSPACE_EXACT_TARGET_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME`;
- runtime approval/execution flags remain false;
- upstream request hash is recomputed and bound;
- exact target path, branch, HEAD, workspace status, fixed tool, output caps, replay policy, operator stop, and approval/run IDs are bound;
- approval/run IDs must be fresh BLK-SYSTEM-072 IDs and cannot reuse CEB_009, BLK-SYSTEM-070, BLK-SYSTEM-071, BLK-SYSTEM-051, or BLK-SYSTEM-052 IDs;
- exact denied-authority set, exact no-side-effect false flags, and exact proof markers are required;
- all valid string fields reject runtime approval, BLK-test-as-BLK-System-test-suite wording, CEB_009 executable reuse, protected paths/secrets, BEO/RTM/coverage/drift, tooling, source/Git mutation, and production-isolation laundering.

### Task 002 — BLK-073 boundary and active doctrine gate

Create BLK-073 and a persistent active doctrine gate that asserts:

- BLK-SYSTEM-072 is review-only approval-envelope readiness;
- BLK-test remains a functional module, not a BLK-System test suite;
- exact Kuronode target is bound;
- upstream BLK-SYSTEM-071 request package is bound by recomputed hash;
- future approval/run IDs are fresh and one-use;
- no runtime, no MCP startup, no mutation, no CEB_009 executable reuse, no BEO/RTM/coverage/drift/protected-body/tooling/production-isolation authority.

### Task 003 — Hostile review and remediation

Perform hostile review focused on:

1. approval-envelope-as-runtime-approval laundering;
2. BLK-test module naming confusion;
3. upstream request hash forgery;
4. replay ID and consumed-ID reuse;
5. exact target path/head drift;
6. valid-field natural language authority smuggling;
7. CEB_009 / BLK-SYSTEM-070 / BLK-SYSTEM-071 executable artifact reuse;
8. BEO/RTM/coverage/drift inheritance;
9. protected path/secrets and tooling/source/Git mutation laundering;
10. active doctrine gate absence checks.

Remediate blockers with tests/docs before closeout.

### Task 004 — Final verification and closeout

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_kuronode_workspace_exact_target_approval_envelope -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint072_blk_test_kuronode_workspace_exact_target_approval_envelope_is_review_only -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest discover python 'test_*.py'
go test ./...
git diff --check
```

Write final outcomes and closeout, exact-path commit, push, and verify remote.

---

## 5. Stop Conditions

Stop and report instead of broadening scope if:

- any step needs to execute BLK-test runtime against Kuronode;
- any step needs to start BLK-test MCP;
- any step needs to run Electron, smoke tests, npm, TypeScript tooling, package-manager commands, network tools, model/browser/cyber tools, or Codex;
- any step needs to mutate Kuronode source/Git state or push Kuronode;
- any step needs protected BLK-req body reads or active-vault scanning;
- any fixture requires CEB_009 artifacts as executable input;
- any wording treats BLK-test as a BLK-System test suite;
- exact target HEAD differs from `38e332b188e45edcb484765694112c9041ad1a3b` and the envelope would need retargeting.
