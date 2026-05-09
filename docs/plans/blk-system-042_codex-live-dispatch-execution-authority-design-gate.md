# BLK-SYSTEM-042 — Codex Live-Dispatch Execution Authority Design Gate Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `code-review` when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable.

**Goal:** Define and fixture-test a fail-closed Codex live-dispatch execution-authority design gate that packages the prerequisites for a future live-dispatch authority request while granting no execution authority in this sprint.

**BLK-024 track:** Track A — Doctrine, alignment, and review gates; Track C — BLK-pipe blast shield and forge; Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening.

**Maturity level:** BLK-024 L0 doctrine boundary plus L1 fixture/local implementation. This is not L2 live transport, not L3 smoke, not L4 pilot runtime, and not L5 production authority.

**Architecture:** BLK-SYSTEM-038 created deterministic Codex invocation profiles. BLK-SYSTEM-039 wrapped them in dispatch-envelope evidence. BLK-SYSTEM-040 added a live-dispatch readiness gate. BLK-SYSTEM-041 created an authority-request package and disabled adapter. BLK-SYSTEM-042 now defines the next design gate for the future execution-authority envelope without enabling the disabled adapter or dispatching anything.

**Tech Stack:** Markdown doctrine, Python fixtures/tests, active doctrine gates.

**Authority boundary:** Design gate and local fixture only. No live Codex execution, no runtime dispatch, no subprocess start, no BLK-pipe invocation, no Git/source mutation, no worktree creation, no package-manager/network/model/cyber/browser tooling, no protected BLK-req vault body reads, no production BLK-test MCP, no BEO publication, no RTM generation, no drift rejection, and no production sandbox/cgroup/VM/firewall/host-secret-isolation claims.

---

## 0. Current Repository State at Planning

```text
Date: 2026-05-09T16:03:22+10:00
Branch: main...origin/main
HEAD: 0ac3139 docs: close blk-system sprint 041 codex live dispatch disabled adapter
Existing highest system plan: docs/plans/blk-system-041_codex-live-dispatch-authority-request-disabled-adapter.md
Existing highest BLK boundary doc: docs/BLK-043_codex-live-dispatch-authority-request-disabled-adapter-boundary.md
```

Discovery found no existing `BLK-SYSTEM-042`, `blk-system-042`, or `BLK-044` owner in `docs/` or `python/`.

---

## 1. Why This Sprint Exists

BLK-SYSTEM-041 deliberately stopped at `AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_EXECUTION` plus `DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED`. That request package proves review readiness and disabled-adapter refusal, but it does not define the specific design evidence a later sprint would need before asking for any live execution-authority pilot.

BLK-SYSTEM-042 creates that design gate safely. It records the required future authority surfaces as review-only contracts: approval envelope, BLK-pipe integration contract, containment contract, telemetry contract, rollback contract, monitoring/operator controls, failure ceiling, replay protection, and hostile audit. A complete record can return `EXECUTION_AUTHORITY_DESIGN_READY_FOR_REVIEW_NOT_EXECUTION`; all dispatch/execution flags remain false.

This sprint is not permission to run Codex. It is a fail-closed design gate before any separate future L3/L4 authority request.

---

## 2. Governing Documents and Obligations

- **BLK-024:** Preserve visible maturity rungs. This sprint is L0/L1 design/fixture only, not smoke, pilot, or production authority.
- **BLK-001:** Preserve separation between Hermes planning/audit, Codex tactical work, BLK-pipe mutation enforcement, BLK-test evidence, BEO publication, and RTM closure.
- **BLK-002 / BLK-005 / BLK-006:** Do not read, copy, parse, hash, summarize, scan, or mutate protected BLK-req vault bodies.
- **BLK-003:** Target Codex/BLK-pipe orchestration does not become current authority without a later explicit approval envelope.
- **BLK-004:** Go `blk-pipe` remains the mutation enforcement authority. Python design-gate fixtures are review artifacts only.
- **BLK-040:** Invocation profile remains fixture-only and starts no Codex process.
- **BLK-041:** Dispatch envelope remains fixture-only and starts no subprocess.
- **BLK-042:** Readiness gate remains review-only; `READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION` is not execution approval.
- **BLK-043:** Authority request remains review-only and disabled adapter remains blocked.

---

## 3. Proposed Implementation Surface

### New Boundary Document

```text
docs/BLK-044_codex-live-dispatch-execution-authority-design-gate.md
```

Required vocabulary:

```text
CODEX_LIVE_DISPATCH_EXECUTION_AUTHORITY_DESIGN_GATE_FIXTURE_ONLY
CODEX_EXECUTION_AUTHORITY_DESIGN_GATE_FAILS_CLOSED
CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_AUTHORITY_REQUEST_PACKAGE
CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_APPROVAL_ENVELOPE_CONTRACT
CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_BLK_PIPE_INTEGRATION_CONTRACT
CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_CONTAINMENT_CONTRACT
CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_TELEMETRY_CONTRACT
CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_ROLLBACK_CONTRACT
CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_MONITORING_OPERATOR_CONTROL_CONTRACT
CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_FAILURE_CEILING_CONTRACT
CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_REPLAY_PROTECTION_CONTRACT
CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_HOSTILE_AUDIT_CONTRACT
CODEX_EXECUTION_AUTHORITY_DESIGN_GRANTS_NO_EXECUTION_AUTHORITY
EXECUTION_AUTHORITY_DESIGN_READY_FOR_REVIEW_NOT_EXECUTION
EXECUTION_AUTHORITY_DESIGN_BLOCKED
```

### New Python Module

```text
python/blk_codex_live_dispatch_execution_authority_design_gate.py
```

Proposed functions:

```text
build_codex_live_dispatch_execution_authority_design_gate(...)
validate_codex_live_dispatch_execution_authority_design_gate(record, ...)
```

The module must validate a BLK-043 authority-request record, evaluate review-only design contracts, and return blocked reasons without starting subprocesses, calling Codex, calling BLK-pipe, calling Git, creating worktrees, mutating files, reading artifact bodies, reading Codex configuration, inspecting protected BLK-req bodies, using network clients, or installing packages.

### New Tests

```text
python/test_blk_codex_live_dispatch_execution_authority_design_gate.py
```

Test scope:

1. complete design gate packages BLK-043 request evidence and returns `EXECUTION_AUTHORITY_DESIGN_READY_FOR_REVIEW_NOT_EXECUTION`;
2. any missing design contract returns `EXECUTION_AUTHORITY_DESIGN_BLOCKED`;
3. blocked or malformed BLK-043 request evidence blocks readiness;
4. side-effect flags for execution, subprocess, BLK-pipe, source/Git mutation, protected-vault access, BEO/RTM/drift, network/package tooling, and production sandbox claims fail closed;
5. recursive authority-laundering keys/strings fail closed in both builder and validator paths;
6. source AST contains no live imports/calls for subprocess, shell, Git, network clients, package managers, `exec`, or `eval`.

### Doctrine Gate Update

```text
python/test_active_doctrine_review_gates.py
```

Add a persistent gate requiring BLK-044 to preserve the design-only execution-authority boundary.

---

## 4. Exact Allowed Implementation Paths

```text
docs/plans/blk-system-042_codex-live-dispatch-execution-authority-design-gate.md
docs/outcomes/BLK-SYSTEM-042_task-000-outcome.md
docs/BLK-044_codex-live-dispatch-execution-authority-design-gate.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-042_task-001-outcome.md
python/blk_codex_live_dispatch_execution_authority_design_gate.py
python/test_blk_codex_live_dispatch_execution_authority_design_gate.py
docs/outcomes/BLK-SYSTEM-042_task-002-outcome.md
docs/reviews/BLK-SYSTEM-042_codex-live-dispatch-execution-authority-design-gate-hostile-review.md
docs/outcomes/BLK-SYSTEM-042_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-042_sprint-closeout.md
```

No `docs/active/`, `docs/requirements/`, or `docs/use_cases/` path may be modified or read for protected body content.

---

## 5. Task Breakdown

### Task 0 — Plan Publication

Create and publish this plan plus `docs/outcomes/BLK-SYSTEM-042_task-000-outcome.md`.

Verification:

```bash
git diff --check -- docs/plans/blk-system-042_codex-live-dispatch-execution-authority-design-gate.md docs/outcomes/BLK-SYSTEM-042_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
for path in [
    Path('docs/plans/blk-system-042_codex-live-dispatch-execution-authority-design-gate.md'),
    Path('docs/outcomes/BLK-SYSTEM-042_task-000-outcome.md'),
]:
    text = path.read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, path
print('markdown sanity PASS')
PY
```

Commit: `docs: plan blk-system sprint 042 codex execution authority design gate`

### Task 1 — BLK-044 Boundary and Doctrine Gate

Add BLK-044 and a persistent active doctrine gate. RED first: add the focused gate and verify failure before writing the doc.

Allowed files:

```text
docs/BLK-044_codex-live-dispatch-execution-authority-design-gate.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-042_task-001-outcome.md
```

Verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- docs/BLK-044_codex-live-dispatch-execution-authority-design-gate.md python/test_active_doctrine_review_gates.py docs/outcomes/BLK-SYSTEM-042_task-001-outcome.md
```

Commit: `docs: define blk044 codex execution authority design gate`

### Task 2 — Execution Authority Design Gate Fixture

Implement the pure fixture/helper and tests. RED first: create the tests and verify failure before implementing the helper.

Required record shape:

```text
design_gate_id: codex_live_dispatch_execution_authority_design_gate
design_gate_status: CODEX_LIVE_DISPATCH_EXECUTION_AUTHORITY_DESIGN_GATE_FIXTURE_ONLY
evaluation: EXECUTION_AUTHORITY_DESIGN_READY_FOR_REVIEW_NOT_EXECUTION or EXECUTION_AUTHORITY_DESIGN_BLOCKED
execution_authorized: false
codex_subprocess_started: false
blk_pipe_dispatched: false
source_mutation_authorized: false
production_sandbox_claimed: false
```

Allowed files:

```text
python/blk_codex_live_dispatch_execution_authority_design_gate.py
python/test_blk_codex_live_dispatch_execution_authority_design_gate.py
docs/outcomes/BLK-SYSTEM-042_task-002-outcome.md
```

Verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_live_dispatch_execution_authority_design_gate -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_live_dispatch_authority_request -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_live_dispatch_readiness_gate -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- python/blk_codex_live_dispatch_execution_authority_design_gate.py python/test_blk_codex_live_dispatch_execution_authority_design_gate.py docs/outcomes/BLK-SYSTEM-042_task-002-outcome.md
```

Commit: `feat: add codex execution authority design gate fixture`

### Task 3 — Hostile Review and Closeout

Perform hostile review, remediate blockers, write review and closeout docs, run final verification, commit, and push.

Hostile review questions:

1. Does any helper start subprocesses, call Codex, call Git, call BLK-pipe, install packages, use network/model/cyber/browser tooling, or inspect protected vaults?
2. Can `EXECUTION_AUTHORITY_DESIGN_READY_FOR_REVIEW_NOT_EXECUTION` become execution approval?
3. Can a blocked BLK-043 authority-request package pass?
4. Can missing approval-envelope, BLK-pipe, containment, telemetry, rollback, monitoring/operator, failure-ceiling, replay-protection, or hostile-audit contracts pass?
5. Can side-effect flags be laundered through nested contract dictionaries?
6. Can design contracts imply production sandbox, network firewall, or host-secret isolation enforcement?
7. Can recursive authority-laundering keys/strings bypass builder/evaluator validation?

Final verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_live_dispatch_execution_authority_design_gate -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_live_dispatch_authority_request -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_live_dispatch_readiness_gate -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_dispatch_envelope -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
export PATH="$HOME/.local/bin:$PATH"; go test ./... && go vet ./...
git diff --check
```

Commit: `docs: close blk-system sprint 042 codex execution authority design gate`

---

## 6. Expected Final State

BLK-SYSTEM-042 should leave the repository with a BLK-044 doctrine boundary, persistent doctrine gate, and deterministic Python design-gate fixture. The fixture may report design review readiness only; it must never report execution approval, dispatch success, source mutation, production sandbox enforcement, BEO publication, RTM generation, or drift decisions.
