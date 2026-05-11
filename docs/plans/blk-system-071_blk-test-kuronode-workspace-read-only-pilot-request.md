# BLK-SYSTEM-071 — BLK-test Kuronode Workspace Read-Only Pilot Request Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, `docs/BLK-059_blk-system-post-058-roadmap.md` for current roadmap selection, then BLK-001 through BLK-006 and active BLK-test/Kuronode boundary documents as applicable.

**Goal:** Create a fresh, non-runtime human-review request package for a future read-only BLK-test module pilot over the real Kuronode workspace, without reusing CEB_009 authority or implying BLK-System test-suite semantics.
**BLK-024 track:** Track F — BLK-test production-readiness ladder; Track J — capability hardening / maturity level L0/L1 request/doctrine/fixture only.
**Architecture:** BLK-test is a BLK-System functional evidence module, not a test suite for BLK-System. This sprint creates a deterministic request/fixture boundary for a future BLK-test module run against `/home/dad/code/Kuronode-v1`, pinned to the current local Kuronode workspace identity, while preserving all runtime and mutation authority as pending human decision. The sprint uses Python validators and active doctrine gates only; it does not execute BLK-test runtime against Kuronode.
**Tech Stack:** Markdown doctrine/outcomes; Python `unittest` fixture validators; no package-manager, Electron, TypeScript, smoke-test, Codex, or live BLK-test MCP execution.
**Authority boundary:** L0/L1 request/doctrine/fixture only. No runtime, no live BLK-test MCP, no Kuronode source/Git mutation, no CEB_009 artifact reuse, no remote push, no BEO publication, no RTM generation.

---

## 0. Current Known State

Captured at planning time:

```text
date: 2026-05-11T10:51:35+10:00
BLK-System status: ## main...origin/main
BLK-System HEAD: 13e787a docs: close out blk-system 070 patch attempt
BLK-System remote main: 13e787a171c4a93be3a9d0f320889678b0688812 refs/heads/main
Kuronode status: ## main...origin/main [ahead 1]
Kuronode HEAD: 38e332b blk-pipe: apply bounded engine changes
Kuronode root: /home/dad/code/Kuronode-v1
```

The Kuronode local workspace is intentionally ahead by one local CEB_009 patch commit. This sprint does not push, patch, reset, fetch, or otherwise mutate that workspace.

---

## 1. Naming Discipline

This sprint must preserve the user's naming correction:

```text
BLK-test is a BLK-System functional module, not BLK-System's test suite.
```

Allowed phrasing:

- BLK-test module pilot
- BLK-test evidence module
- BLK-test read-only oracle/request
- Kuronode workspace validation via BLK-test module

Forbidden phrasing:

- BLK-System test
- test of BLK-System
- testing BLK-System with Kuronode
- BLK-test as proof that BLK-System itself was tested

---

## 2. Governing Documents

- **BLK-024:** supplies maturity vocabulary and ladder discipline; this sprint remains L0/L1.
- **BLK-059:** current roadmap; keeps production/generic BLK-test MCP, reusable service startup, arbitrary shell, source/Git mutation by BLK-test, protected body reads, BEO publication, RTM generation, package-manager/network/model/browser/cyber tooling, and production isolation claims unauthorized.
- **BLK-001:** separates BLK-pipe mutation, BLK-test evidence, BEO publication, and blk-link/RTM trace closure. BLK-test evidence is not authority.
- **BLK-002 / BLK-005 / BLK-006:** protect BLK-req active/staging bodies; this sprint does not read, copy, scan, hash, summarize, mutate, or compare protected BLK-req bodies.
- **BLK-003:** requires human dispatch gates and prevents BLK-test/BEO/RTM authority inheritance.
- **BLK-004:** preserves deterministic enforcement and exact allowlists; this sprint does not invoke BLK-pipe or perform source mutation.
- **BLK-047 through BLK-056:** define BLK-test fixed-tool, real-repo, non-disposable, replay, and evidence-only boundaries; this sprint creates a fresh Kuronode-target request package, not runtime.
- **BLK-058 / BLK-061 / BLK-062 / BLK-063 / BLK-064:** provide Kuronode TypeScript Power-of-Ten/static-profile lineage; this sprint may reference that lineage but must not reuse CEB_009 artifacts as executable inputs.
- **BLK-071 and BLK-SYSTEM-070 closeout:** record consumed CEB_009 patch authority and local Kuronode commit; this sprint may cite historical evidence but must not reuse approvals, run IDs, payloads, reports, or source-mutation authority.

---

## 3. Explicit Non-Authority Boundary

This plan does not authorize:

- production BLK-test MCP;
- generic BLK-test MCP;
- reusable BLK-test service startup;
- BLK-test runtime execution against Kuronode;
- arbitrary shell as BLK-test behavior;
- caller-supplied commands or dynamic tool expansion;
- Electron launch, smoke-test execution, TypeScript tooling, ESLint, formatter, typechecker, package-manager, network, model-service, browser, or cyber tooling;
- Kuronode source mutation;
- Kuronode Git mutation, staging, commit, push, reset, checkout, revert, stash, or cleanup;
- reuse of CEB_009 approval IDs, run IDs, BLK-pipe payloads/reports, patch authority, or static-pilot artifacts as executable test fixtures;
- BLK-System test-suite semantics for BLK-test module work;
- protected BLK-req vault body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison;
- authoritative BEO publication;
- runtime `PUBLISHED` BEO output;
- RTM generation;
- RTM drift rejection;
- coverage matrix/coverage-claim promotion;
- active-vault hash comparison;
- signer/storage/ledger/rollback/revocation/supersession/release authority;
- production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claims.

---

## 4. Deliverables

1. `python/blk_test_kuronode_workspace_pilot_request.py`
2. `python/test_blk_test_kuronode_workspace_pilot_request.py`
3. `docs/BLK-072_blk-test-kuronode-workspace-read-only-pilot-request-boundary.md`
4. Active doctrine gate updates in `python/test_active_doctrine_review_gates.py`
5. Per-task outcomes under `docs/outcomes/`
6. Hostile review under `docs/reviews/`
7. Sprint closeout under `docs/outcomes/BLK-SYSTEM-071_sprint-closeout.md`

---

## 5. Task Plan

### Task 000 — Plan publication

Create this plan and a Task 000 outcome. Verify:

```bash
git diff --check -- docs/plans/blk-system-071_blk-test-kuronode-workspace-read-only-pilot-request.md docs/outcomes/BLK-SYSTEM-071_task-000-outcome.md
python - <<'PY'
from pathlib import Path
for p in [
    Path('docs/plans/blk-system-071_blk-test-kuronode-workspace-read-only-pilot-request.md'),
    Path('docs/outcomes/BLK-SYSTEM-071_task-000-outcome.md'),
]:
    text = p.read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, p
PY
```

Stage exact paths only, commit, and push.

### Task 001 — Request fixture validator, RED/GREEN

Add RED tests first for a BLK-test module Kuronode workspace pilot request validator:

- complete request returns `BLK_TEST_KURONODE_WORKSPACE_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME`;
- result remains `runtime_approved=False`, `blk_test_runtime_executed=False`, `source_mutation_allowed=False`, `git_mutation_allowed=False`;
- exact target binds `/home/dad/code/Kuronode-v1`, branch `main`, and current local HEAD `38e332b188e45edcb484765694112c9041ad1a3b`;
- CEB_009 historical artifacts cannot be reused as executable fixture inputs, approvals, run IDs, or payloads;
- phrase laundering that frames BLK-test as a BLK-System test suite is rejected;
- runtime approval, production/generic MCP, BEO/RTM, coverage/drift, protected-body, package-manager/tooling/network/source/Git mutation, and production-isolation laundering are rejected;
- exact denied-authority set equality and no-side-effect false-flag equality are required;
- required proof markers are exact and meaningful.

Then implement the smallest validator and rerun focused tests.

### Task 002 — BLK-072 boundary and active doctrine gate

Write BLK-072 as the authority boundary for this request package. Add a persistent active doctrine gate asserting:

- BLK-test module naming distinction;
- Kuronode workspace exact-target request readiness only;
- no runtime execution;
- no CEB_009 reuse;
- no production/generic BLK-test MCP;
- no Kuronode source/Git mutation;
- no protected-body, BEO, RTM, coverage/drift, tooling, or production-isolation authority.

Run focused gate tests and the request fixture tests.

### Task 003 — Hostile review and remediation

Perform a hostile review focused on:

1. BLK-test module naming hallucination risk;
2. PASS-as-runtime or request-as-approval laundering;
3. CEB_009 consumed-authority reuse;
4. exact target drift or unstated remote-push assumptions;
5. source/Git mutation and cleanup laundering;
6. protected path and secret-path smuggling;
7. BEO/RTM/publication/coverage/drift authority inheritance;
8. exact denied-authority set weakening;
9. proof-marker placeholders and no-side-effect omissions.

Remediate blockers with tests/docs before closeout.

### Task 004 — Final verification, closeout, commit, push

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_kuronode_workspace_pilot_request -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint071_blk_test_kuronode_workspace_pilot_request_is_module_request_not_blk_system_test -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest discover python 'test_*.py'
go test ./...
git diff --check
```

Write per-task outcomes and closeout. Stage exact paths only, commit, push, and verify `origin/main`.

---

## 6. Stop Conditions

Stop and report instead of broadening scope if:

- Kuronode workspace is dirty in a way that would require cleanup or mutation;
- any task would need to run Electron, npm, TypeScript tooling, smoke tests, or package-manager commands;
- a fixture requires CEB_009 artifacts as executable input;
- approval/run ID reuse appears necessary;
- any step requires protected BLK-req body reads or active-vault scanning;
- any test implies BLK-test is the BLK-System test suite rather than a functional evidence module;
- any runtime execution against Kuronode is needed to complete the sprint.
