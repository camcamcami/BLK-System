# BLK-SYSTEM-045 — Authority Frontier Selection Gate Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `code-review` when executing. This plan is guided by `docs/BLK-045_blk-system-post-042-roadmap.md` as the current post-BLK-SYSTEM-042 roadmap, with `docs/BLK-024_blk-system-development-roadmap.md` retained for maturity-model lineage, then BLK-001 through BLK-006 as applicable.

**Goal:** Add a deterministic authority-frontier selection gate so future activation cannot be inferred from “next sprint” language, review-ready fixtures, or adjacent approvals.

**BLK-045 fork:** Cross-fork selection control for BLK-045 Fork B / Fork C activation decisions.

**BLK-024 maturity lineage:** L0 doctrine plus L1 fixture/gate only. This is not L2 transport enablement, not L3 smoke, not L4 pilot runtime, and not L5 production authority.

**Architecture:** BLK-045 says the next real progress step is a controlled decision about exactly one frontier: Codex live-dispatch activation or BLK-test fixed-tool pilot authority, followed later by BEO/RTM only after verification evidence is trustworthy. BLK-SYSTEM-044 produced a BLK-test request package but explicitly did not grant runtime authority. This sprint converts that stop condition into an active selection gate: it can classify a proposed frontier decision as review-ready or blocked, but it cannot start Codex, BLK-test, BLK-pipe, BEO, RTM, or any runtime capability.

**Tech Stack:** Markdown doctrine, Python deterministic fixture/tests, active doctrine gates.

**Authority boundary:** Selection gate only. No live Codex execution, no Codex subprocess, no BLK-pipe dispatch, no production BLK-test MCP, no live BLK-test server/client startup, no fixed-tool execution, no source/Git mutation by BLK-test or Codex, no protected BLK-req body reads/copying/scanning, no authoritative BEO publication, no runtime RTM generation, no RTM drift rejection, no package-manager/network/model/browser/cyber tooling, and no production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claim.

---

## 0. Current Repository State at Planning

```text
Date: 2026-05-09T20:02:26+10:00
Branch: main...origin/main
HEAD: 7386323 docs: close blk-system sprint 044 blk-test pilot request
Existing highest system plan: docs/plans/blk-system-044_blk-test-fixed-tool-pilot-authority-request.md
Existing highest BLK boundary doc: docs/BLK-047_blk-test-fixed-tool-pilot-authority-request-boundary.md
```

Discovery found no existing `BLK-SYSTEM-045`, `blk-system-045`, or `BLK-048` owner in `docs/plans/`, `docs/outcomes/`, or active `docs/BLK-*.md`.

---

## 1. Scope Decision

The operator requested the next BLK-System sprint and execution of all tasks, but did not explicitly name a runtime authority frontier or grant live Codex/BLK-test runtime approval. Under BLK-045 and BLK-047, this means the sprint must not activate runtime.

The concrete blocker is now decision ambiguity: `BLK_TEST_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME` and Codex review-ready/design-ready artifacts are easy to mistake for an activation grant. BLK-SYSTEM-045 therefore adds a frontier selection gate that requires exactly one named frontier and exact future approval fields before any later activation sprint may proceed.

---

## 2. Governing Documents and Obligations

- **BLK-045:** Current roadmap selector. It asks which single authority frontier should be activated or completed next, and under what explicit approval envelope.
- **BLK-046:** Current-state index. It preserves Codex and BLK-test as non-runtime without explicit approval.
- **BLK-047:** BLK-test fixed-tool pilot request boundary. It states BLK-SYSTEM-044 request readiness is not runtime approval.
- **BLK-040 through BLK-044:** Codex live-dispatch ladder remains review-ready/design-ready/disabled evidence only.
- **BLK-017 through BLK-020 / BLK-025:** BLK-test remains disabled/gated evidence with one historical first-smoke exception only.
- **BLK-001:** Preserve separation between planning, execution, BLK-pipe mutation, BLK-test evidence, BEO publication, and RTM trace closure.
- **BLK-002 / BLK-005 / BLK-006:** Preserve protected-vault hard-deny and no protected body reads.
- **BLK-003:** Preserve human gates, hostile review, bounded context, failure ceilings, and no implicit inheritance between execution, verification, publication, and RTM.
- **BLK-004:** Preserve BLK-pipe as source mutation/Git enforcement; selection gates cannot mutate source.

---

## 3. Proposed Implementation Surface

### New Boundary Document

```text
docs/BLK-048_authority-frontier-selection-gate-boundary.md
```

Required markers:

```text
BLK_SYSTEM_AUTHORITY_FRONTIER_SELECTION_GATE
FRONTIER_SELECTION_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY
EXACTLY_ONE_FRONTIER_REQUIRED
RUNTIME_APPROVAL_NOT_INFERRED_FROM_NEXT_SPRINT
BLK_TEST_REQUEST_READY_IS_NOT_PILOT_APPROVAL
CODEX_REVIEW_READY_IS_NOT_LIVE_EXECUTION_APPROVAL
BEO_AND_RTM_BLOCKED_UNTIL_VERIFICATION_FRONTIER_APPROVED
PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN
ADJACENT_AUTHORITY_INHERITANCE_FORBIDDEN
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_045
```

### New Python Fixture

```text
python/blk_authority_frontier_selection_gate.py
```

Proposed functions:

```text
build_authority_frontier_selection_gate(...)
validate_authority_frontier_selection_gate(record)
simulate_disabled_frontier_activation_adapter(record)
```

The fixture must be pure and deterministic. It must not import or invoke subprocess, live MCP, socket/network clients, package managers, model services, browser/cyber tools, Git, BLK-pipe, BEO publication, RTM generation, protected-vault readers, or filesystem mutation helpers.

### New Tests

```text
python/test_blk_authority_frontier_selection_gate.py
```

Required test scope:

1. a valid single-frontier selection evaluates to `FRONTIER_SELECTION_READY_FOR_HUMAN_DECISION_NOT_RUNTIME`;
2. no frontier, multiple frontiers, or unknown frontiers fail closed;
3. BLK-test request readiness, Codex review readiness, BEO fixture readiness, RTM fixture readiness, sprint-dispatch approval, and “next sprint” wording cannot substitute for runtime approval;
4. adjacent authority inheritance fails closed;
5. recursive generic authority/approval/claim laundering fails closed;
6. disabled activation adapter reports all runtime side-effect flags false;
7. AST checks prove no live execution/network/filesystem mutation imports/calls.

### Doctrine Gate Update

```text
python/test_active_doctrine_review_gates.py
```

Add a persistent gate requiring BLK-048 to preserve the selection-only non-runtime boundary and exact markers above.

---

## 4. Exact Allowed Implementation Paths

```text
docs/plans/blk-system-045_authority-frontier-selection-gate.md
docs/outcomes/BLK-SYSTEM-045_task-000-outcome.md
docs/BLK-048_authority-frontier-selection-gate-boundary.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-045_task-001-outcome.md
python/blk_authority_frontier_selection_gate.py
python/test_blk_authority_frontier_selection_gate.py
docs/outcomes/BLK-SYSTEM-045_task-002-outcome.md
docs/reviews/BLK-SYSTEM-045_authority-frontier-selection-gate-hostile-review.md
docs/outcomes/BLK-SYSTEM-045_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-045_sprint-closeout.md
```

No runtime, protected-vault, active-vault body, real target repo, `.git`, network, package-manager, model, browser, cyber, BLK-pipe dispatch, BEO publication, or RTM generation path may be used.

---

## 5. Task Breakdown

### Task 0 — Plan Publication

Create and publish this plan plus `docs/outcomes/BLK-SYSTEM-045_task-000-outcome.md`.

Verification:

```bash
git diff --check -- docs/plans/blk-system-045_authority-frontier-selection-gate.md docs/outcomes/BLK-SYSTEM-045_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
for path in [
    Path('docs/plans/blk-system-045_authority-frontier-selection-gate.md'),
    Path('docs/outcomes/BLK-SYSTEM-045_task-000-outcome.md'),
]:
    text = path.read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, path
print('markdown sanity PASS')
PY
```

Commit: `docs: plan blk-system sprint 045 frontier selection gate`

### Task 1 — BLK-048 Boundary and Doctrine Gate

Add BLK-048 and persistent active doctrine gates. RED first: add the focused gate and verify failure before writing the doc.

Allowed files:

```text
docs/BLK-048_authority-frontier-selection-gate-boundary.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-045_task-001-outcome.md
```

Verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- docs/BLK-048_authority-frontier-selection-gate-boundary.md python/test_active_doctrine_review_gates.py docs/outcomes/BLK-SYSTEM-045_task-001-outcome.md
```

Commit: `docs: define blk048 frontier selection gate`

### Task 2 — Deterministic Frontier Selection Fixture

Implement the pure selection fixture and tests. RED first: create tests and verify failure before implementing the helper.

Required record shape includes:

```text
selection_id: BLK-SYSTEM-045-FRONTIER-SELECTION-001
selection_status: BLK_SYSTEM_AUTHORITY_FRONTIER_SELECTION_GATE
review_status: FRONTIER_SELECTION_READY_FOR_HUMAN_DECISION_NOT_RUNTIME or FRONTIER_SELECTION_BLOCKED_NOT_AUTHORIZED
maturity: L0_L1_SELECTION_FIXTURE_ONLY
selected_frontier: codex_live_dispatch_l3_smoke or blk_test_fixed_tool_pilot_l3_l4
exactly_one_frontier_selected: true
runtime_authority_granted: false
```

Allowed files:

```text
python/blk_authority_frontier_selection_gate.py
python/test_blk_authority_frontier_selection_gate.py
docs/outcomes/BLK-SYSTEM-045_task-002-outcome.md
```

Verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_authority_frontier_selection_gate -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- python/blk_authority_frontier_selection_gate.py python/test_blk_authority_frontier_selection_gate.py docs/outcomes/BLK-SYSTEM-045_task-002-outcome.md
```

Commit: `feat: add authority frontier selection gate fixture`

### Task 3 — Hostile Review and Closeout

Perform hostile review, remediate blockers, write review and closeout docs, run final verification, commit, and push.

Hostile review questions:

1. Can the fixture treat “next sprint,” sprint-dispatch approval, BLK-test request readiness, Codex review readiness, BEO fixture readiness, or RTM fixture readiness as runtime approval?
2. Can multiple frontiers be selected at once?
3. Can adjacent authorities be inherited across Codex, BLK-test, BEO, RTM, BLK-pipe, protected-vault, package/network/model/browser/cyber tooling, or production isolation?
4. Can recursive generic authority/approval/claim keys or positive runtime strings bypass validation?
5. Does the disabled activation adapter prove no side effects across every denied authority surface?
6. Is the next-step recommendation honest: future runtime requires explicit human approval naming one frontier?

Final verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_authority_frontier_selection_gate -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
export PATH="$HOME/.local/bin:$PATH"; go test ./... && go vet ./...
git diff --check
```

Commit: `docs: close blk-system sprint 045 frontier selection gate`

---

## 6. Expected Final State

BLK-SYSTEM-045 should leave the repository with a BLK-048 authority-frontier selection boundary, persistent doctrine gate, deterministic Python selection fixture, hostile review, and closeout evidence. The sprint may report human-decision readiness only. It must not report runtime approval, Codex execution, BLK-test transport, fixed-tool execution, source mutation, BEO publication, RTM generation, drift rejection, protected-body reads, or production isolation.
