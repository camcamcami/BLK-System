# BLK-SYSTEM-040 — Codex Live-Dispatch Readiness Gate Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, `systematic-debugging`, and `code-review` when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable.

**Goal:** Define and implement a fail-closed Codex live-dispatch readiness gate fixture that evaluates whether a BLK-039 dispatch envelope has all prerequisite evidence for a future live-dispatch authority request, while still refusing to start Codex, BLK-pipe, Git, subprocesses, or source mutation.

**BLK-024 track:** Track A — Doctrine, alignment, and review gates; Track C — BLK-pipe blast shield and forge; Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening.

**Maturity level:** BLK-024 L1 fixture/local implementation plus L2 disabled/fail-closed transport semantics. This sprint creates deterministic local readiness records and BLOCKED/NOT_AUTHORIZED decisions only. It is not L3 synthetic smoke, not L4 pilot runtime, and not L5 production authority.

**Architecture:** BLK-SYSTEM-038 created a deterministic Codex invocation profile fixture. BLK-SYSTEM-039 wrapped that profile in a deterministic dispatch-envelope fixture. BLK-SYSTEM-040 adds the next safe rung: a readiness gate that checks whether all future live-dispatch prerequisites are explicitly present, but it must always return non-executing readiness evidence rather than dispatching.

**Tech Stack:** Markdown doctrine, Python fixtures/tests, active doctrine gates.

**Authority boundary:** Fail-closed readiness gate fixture only. No live Codex execution, no runtime dispatch, no subprocess start, no BLK-pipe invocation, no Git/source mutation, no worktree creation, no package-manager/network/model/cyber/browser tooling, no protected BLK-req vault body reads, no production BLK-test MCP, no authoritative BEO publication, no RTM generation, and no drift rejection.

---

## 0. Current Repository State at Planning

Captured before writing this plan:

```text
Date: 2026-05-09T14:16:40+10:00
Branch: main...origin/main
HEAD: ced587e docs: close blk-system sprint 039 codex dispatch envelope
Existing highest system plan: docs/plans/blk-system-039_codex-deterministic-dispatch-envelope.md
Existing highest BLK boundary doc: docs/BLK-041_codex-deterministic-dispatch-envelope-boundary.md
```

Discovery found no existing `BLK-SYSTEM-040`, `blk-system-040`, or `BLK-042` owner in `docs/` or `python/`. BLK-041 explicitly identifies a future live-dispatch request as requiring runtime approval, BLK-pipe wiring, containment evidence, validation execution, telemetry persistence, rollback, monitoring, failure ceiling handling, operator controls, and hostile review.

---

## 1. Why This Sprint Exists

BLK-SYSTEM-039 deliberately stopped before live Codex execution. Its closeout states that a later sprint may request explicit live Codex dispatch authority only after a separate sprint defines and proves runtime approval, BLK-pipe wiring, containment evidence, validation execution, telemetry persistence, rollback behavior, monitoring, failure ceiling handling, operator controls, and hostile review.

BLK-SYSTEM-040 is that prerequisite definition and proof fixture. It is not the live-dispatch sprint. It creates a fail-closed gate that reports `BLOCKED_NOT_AUTHORIZED` unless the future request carries every required prerequisite as bounded local evidence. Even when all prerequisites are present, the gate may report readiness evidence only; it still must not launch Codex, call BLK-pipe, create worktrees, or mutate source.

---

## 2. Governing Documents and Obligations

### BLK-024 Roadmap Alignment

- Track A requires persistent doctrine gates for any new authority boundary and clear current-state vs target-state language.
- Track C requires Go `blk-pipe` to remain the enforcement authority and requires negative tests before any new authority path.
- Track I requires operator-visible blocked/ready/escalation records that make missing approvals and policy blocks obvious.
- Track J requires honest capability boundaries, no production sandbox claims, and default denial of network/model/cyber/package-manager surfaces.
- Maturity stays at L1/L2: local fixtures plus fail-closed non-executing readiness semantics.

### BLK-001 Alignment

BLK-001 separates requirements, planning, source mutation, verification, publication, and trace closure. This sprint preserves that separation by producing readiness evidence only. It does not collapse Hermes planning, Codex implementation, BLK-pipe mutation, BLK-test evidence, BEO publication, or RTM closure into one helper.

### BLK-002 / BLK-005 / BLK-006 Alignment

No protected BLK-req body reads, copying, parsing, hashing, mutation, or active-vault scans are allowed. The readiness gate may carry opaque `trace_artifacts` metadata and supplied hash-like strings but must not compare them against live protected vault content.

### BLK-003 Alignment

BLK-003 target-state orchestration describes Codex receiving a bounded packet through BLK-pipe. Current doctrine still requires separate authority before that path can be live. This sprint checks future live-dispatch prerequisites but does not perform the dispatch.

### BLK-004 Alignment

Go `blk-pipe` remains the deterministic mutation enforcement authority. Python readiness checks are pre-dispatch and non-authorizing only. They must not claim to replace BLK-pipe payload validation, process control, Git isolation, validation execution, cleanup, report evidence, or revert behavior.

### BLK-040 / BLK-041 Alignment

BLK-040 owns the deterministic invocation profile fixture. BLK-041 owns the deterministic dispatch-envelope fixture. BLK-SYSTEM-040 must validate that a readiness request preserves those fixtures and must not weaken their no-execution, advisory telemetry, exact boundary, failure ceiling, or authority-laundering protections.

---

## 3. Non-Authority Statement

This plan does not authorize live Codex execution, reusable runtime dispatch, BLK-pipe execution, production BLK-test MCP, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads/copying/parsing/hashing/summarizing/scanning/mutation, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, source mutation outside exact approved sprint files, package-manager/network/model/cyber/browser tooling, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.

A `READY_FOR_AUTHORITY_REVIEW` result from this sprint is not permission to execute Codex. It means only that a later human-approved authority sprint has enough prerequisite evidence to review.

---

## 4. Proposed Implementation Surface

### New Boundary Document

```text
docs/BLK-042_codex-live-dispatch-readiness-gate-boundary.md
```

Required vocabulary:

```text
CODEX_LIVE_DISPATCH_READINESS_GATE_FIXTURE_ONLY
CODEX_LIVE_DISPATCH_GATE_FAILS_CLOSED
CODEX_LIVE_DISPATCH_GATE_STARTS_NO_SUBPROCESS
CODEX_LIVE_DISPATCH_GATE_REQUIRES_RUNTIME_APPROVAL
CODEX_LIVE_DISPATCH_GATE_REQUIRES_BLK_PIPE_WIRING_PLAN
CODEX_LIVE_DISPATCH_GATE_REQUIRES_CONTAINMENT_EVIDENCE
CODEX_LIVE_DISPATCH_GATE_REQUIRES_VALIDATION_EXECUTION_PLAN
CODEX_LIVE_DISPATCH_GATE_REQUIRES_TELEMETRY_PERSISTENCE_PLAN
CODEX_LIVE_DISPATCH_GATE_REQUIRES_ROLLBACK_PLAN
CODEX_LIVE_DISPATCH_GATE_REQUIRES_MONITORING_PLAN
CODEX_LIVE_DISPATCH_GATE_REQUIRES_OPERATOR_CONTROLS
CODEX_LIVE_DISPATCH_GATE_GRANTS_NO_EXECUTION_AUTHORITY
READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION
BLOCKED_NOT_AUTHORIZED
```

### New Python Module

```text
python/blk_codex_live_dispatch_readiness_gate.py
```

Proposed functions:

```text
build_codex_live_dispatch_readiness_gate(...)
validate_codex_live_dispatch_readiness_gate(record)
evaluate_codex_live_dispatch_readiness(record)
```

The helper must build and validate structured dictionaries only. It may validate BLK-040 and BLK-041 fixture records. It must not run subprocesses, call Codex, create worktrees, call Git, call BLK-pipe, read Codex configuration, inspect network state, mutate files, stage/commit/push, call package managers, or inspect protected BLK-req bodies.

### New Tests

```text
python/test_blk_codex_live_dispatch_readiness_gate.py
```

Test scope:

1. valid request with complete prerequisite evidence returns `READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION`, not execution permission;
2. missing runtime approval returns `BLOCKED_NOT_AUTHORIZED` with operator escalation;
3. missing BLK-pipe wiring, containment, validation execution, telemetry persistence, rollback, monitoring, operator controls, failure ceiling, or hostile audit evidence blocks;
4. stale/expired/replayed runtime approval blocks;
5. invalid BLK-040 profile or BLK-041 dispatch envelope blocks;
6. attempts to set live execution, subprocess started, BLK-pipe dispatched, source/Git mutation, BEO/RTM/drift, protected-vault, package-manager/network/model/cyber/browser, or production sandbox authority fail closed;
7. recursive authority-laundering fields and strings fail closed;
8. source AST contains no live imports/calls for subprocess, shell, Git, network clients, package managers, `exec`, or `eval`.

### Doctrine Gate Update

```text
python/test_active_doctrine_review_gates.py
```

Add a persistent gate requiring BLK-042 to preserve the fail-closed non-executing readiness boundary and deny live Codex, BLK-pipe dispatch, protected-vault reads, production sandbox claims, BEO publication, RTM generation, and drift rejection.

---

## 5. Exact Allowed Implementation Paths

Implementation may modify or create only these paths unless hostile review finds a required exact-path correction:

```text
docs/plans/blk-system-040_codex-live-dispatch-readiness-gate.md
docs/outcomes/BLK-SYSTEM-040_task-000-outcome.md
docs/BLK-042_codex-live-dispatch-readiness-gate-boundary.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-040_task-001-outcome.md
python/blk_codex_live_dispatch_readiness_gate.py
python/test_blk_codex_live_dispatch_readiness_gate.py
docs/outcomes/BLK-SYSTEM-040_task-002-outcome.md
docs/reviews/BLK-SYSTEM-040_codex-live-dispatch-readiness-gate-hostile-review.md
docs/outcomes/BLK-SYSTEM-040_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-040_sprint-closeout.md
```

No `docs/active/`, `docs/requirements/`, or `docs/use_cases/` path may be modified or read for protected body content.

---

## 6. Task Breakdown

### Task 0 — Plan Publication

**Objective:** Commit and push this plan plus a task-000 outcome document.

**Allowed files:**

```text
docs/plans/blk-system-040_codex-live-dispatch-readiness-gate.md
docs/outcomes/BLK-SYSTEM-040_task-000-outcome.md
```

**Verification:**

```bash
git diff --check -- docs/plans/blk-system-040_codex-live-dispatch-readiness-gate.md docs/outcomes/BLK-SYSTEM-040_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
for path in [
    Path('docs/plans/blk-system-040_codex-live-dispatch-readiness-gate.md'),
    Path('docs/outcomes/BLK-SYSTEM-040_task-000-outcome.md'),
]:
    text = path.read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, path
print('markdown sanity PASS')
PY
```

**Commit:** `docs: plan blk-system sprint 040 codex live dispatch readiness gate`

### Task 1 — BLK-042 Boundary and Active Doctrine Gate

**Objective:** Add BLK-042 and a persistent active doctrine gate.

**RED tests first:** add the gate before the BLK-042 document exists and verify the focused gate fails.

**Allowed files:**

```text
docs/BLK-042_codex-live-dispatch-readiness-gate-boundary.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-040_task-001-outcome.md
```

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- docs/BLK-042_codex-live-dispatch-readiness-gate-boundary.md python/test_active_doctrine_review_gates.py docs/outcomes/BLK-SYSTEM-040_task-001-outcome.md
```

**Commit:** `docs: define blk042 codex live dispatch readiness gate`

### Task 2 — Readiness Gate Fixture

**Objective:** Implement the fail-closed readiness gate builder/evaluator and tests.

**RED tests first:** create `python/test_blk_codex_live_dispatch_readiness_gate.py` and verify it fails because the helper module is absent or incomplete.

**Required behavior:**

```text
readiness_gate_id: codex_live_dispatch_readiness_gate
readiness_status: CODEX_LIVE_DISPATCH_READINESS_GATE_FIXTURE_ONLY
evaluation: READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION or BLOCKED_NOT_AUTHORIZED
execution_authorized: false
codex_subprocess_started: false
blk_pipe_dispatched: false
source_mutation_authorized: false
runtime_approval.required: true
runtime_approval.validated_for_review_only: true
```

**Allowed files:**

```text
python/blk_codex_live_dispatch_readiness_gate.py
python/test_blk_codex_live_dispatch_readiness_gate.py
docs/outcomes/BLK-SYSTEM-040_task-002-outcome.md
```

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_live_dispatch_readiness_gate -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_dispatch_envelope -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- python/blk_codex_live_dispatch_readiness_gate.py python/test_blk_codex_live_dispatch_readiness_gate.py docs/outcomes/BLK-SYSTEM-040_task-002-outcome.md
```

**Commit:** `feat: add codex live dispatch readiness gate fixture`

### Task 3 — Hostile Review and Sprint Closeout

**Objective:** Perform hostile review, remediate blockers, write review and closeout docs, and push final state.

**Hostile review focus:**

1. Does the helper start subprocesses, call Codex, call Git, create worktrees, call BLK-pipe, invoke package managers, or inspect protected vaults?
2. Can `READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION` be interpreted as execution approval?
3. Can missing/stale/replayed runtime approval pass?
4. Can missing BLK-pipe wiring, containment, validation, telemetry persistence, rollback, monitoring, operator controls, failure ceiling, or hostile audit evidence pass?
5. Can telemetry become canonical mutation, validation, approval, BEO, RTM, or drift evidence?
6. Can generic authority-laundering keys/strings bypass recursive scanning?
7. Does the sprint imply live Codex, BLK-pipe dispatch, BLK-test authority, BEO publication, RTM generation, protected-vault access, source mutation, or production sandbox authority?

**Allowed files:**

```text
docs/reviews/BLK-SYSTEM-040_codex-live-dispatch-readiness-gate-hostile-review.md
docs/outcomes/BLK-SYSTEM-040_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-040_sprint-closeout.md
```

If hostile review finds code or doctrine blockers, remediation may touch only the exact files already authorized by Tasks 1 and 2, and the outcome must record the reason.

**Final verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_live_dispatch_readiness_gate -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_dispatch_envelope -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
export PATH="$HOME/.local/bin:$PATH"; go test ./... && go vet ./...
git diff --check
```

**Commit:** `docs: close blk-system sprint 040 codex live dispatch readiness gate`

---

## 7. Required Implementation Invariants

1. The readiness gate must be pure and side-effect free.
2. The readiness gate must not call `codex`, subprocess, shell, Git, BLK-pipe, BLK-test, network APIs, package managers, browsers, model services, BEO tooling, RTM tooling, protected-vault readers, or filesystem mutation helpers.
3. It must validate BLK-040 and BLK-041 fixture inputs without weakening their no-execution and advisory telemetry guarantees.
4. It must require runtime approval provenance for review only and must fail closed on missing, expired, replayed, stale, or malformed approval IDs.
5. It must require explicit evidence sections for BLK-pipe wiring, containment, validation execution, telemetry persistence, rollback, monitoring, operator controls, failure ceiling, and hostile audit.
6. It must produce operator-facing blocked reasons for missing prerequisites.
7. It must recursively reject authority-laundering keys and strings.
8. It must always set live execution, subprocess, BLK-pipe dispatch, Git/source mutation, BEO publication, RTM generation, drift rejection, protected-vault, package-manager/network/model/cyber/browser, and production sandbox authority fields to false.
9. `READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION` must never be shortened to `READY_FOR_EXECUTION` or equivalent.
10. No future executor may treat this readiness record as permission to run Codex without a separate explicitly approved live-dispatch authority sprint.

---

## 8. Outcome Document Requirements

Each task outcome must include:

- task ID and status;
- exact files changed;
- RED/GREEN evidence where applicable;
- verification commands and results;
- authority boundary statement;
- planned commit message and final hash reported by controller/closeout where self-referential hashing would be impossible;
- note that no protected BLK-req body reads occurred.

Task 3 closeout must additionally include:

- final hostile review verdict;
- final verification suite results;
- final commits;
- final repo status;
- statement that BLK-SYSTEM-040 did not authorize live Codex execution, BLK-pipe dispatch, source mutation, or production sandbox claims.

---

## 9. Expected Final State

After successful closeout, BLK-System will have:

1. BLK-042 documenting the fail-closed Codex live-dispatch readiness boundary;
2. a pure Python readiness-gate fixture/helper that validates all prerequisite evidence and always refuses execution authority;
3. tests proving missing prerequisites, stale/replayed runtime approval, invalid BLK-040/BLK-041 inputs, live-surface imports/calls, and authority laundering fail closed;
4. outcome/review/closeout docs recording the sprint.

This creates a safer future path for a later explicit Codex live-dispatch authority request without granting live tactical authority now.
