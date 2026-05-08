# BLK-SYSTEM-028 — Operator UX / Observability Runbooks Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `systematic-debugging` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable.

**Goal:** Make current guarded BLK-System failures understandable to the human operator through deterministic local status fixtures, bounded escalation packages, and doctrine-pinned runbook language without granting new runtime authority.
**BLK-024 track:** Track I — Operator UX, observability, and escalation / maturity level L1 fixture-only with L0 runbook doctrine.
**Architecture:** BLK-System remains separated by BLK-001 domains. The new operator observability helper may normalize already-supplied report dictionaries into concise local status and escalation fixtures, but it must not execute commands, inspect files, call live services, mutate repositories, publish BEOs, generate RTM, or make policy decisions beyond deterministic classification of provided evidence.
**Tech Stack:** Python `unittest` fixtures plus Markdown doctrine/runbook artifacts.
**Authority boundary:** L1 deterministic local fixtures and L0 doctrine only. No live health checks, production BLK-test MCP, authoritative BEO publication, RTM generation, RTM drift rejection, active-vault scanning, protected-body reads, signer/storage/ledger/rollback authority, source mutation outside exact approved allowlists, or runtime approval capture.

---

## 0. Current Known State

- **Date:** 2026-05-08T10:49:10+10:00
- **Branch state:** `## main...origin/main`
- **HEAD:** `7b6efd8 docs: close blk-system sprint 027 rtm readiness proposal`
- **Baseline verification:** `go test ./...`, `go vet ./...`, and `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover python 'test_*.py'` passed before plan drafting.
- **Latest completed sprint:** BLK-SYSTEM-027 created proposal-only RTM generation readiness fixtures and explicitly recommended Track I operator UX/observability runbooks before runtime RTM authority unless a separate explicit RTM-generation authority request is approved.

---

## 1. Non-Execution and Non-Authority Boundary

This sprint does not authorize Hindsight use, Codex use, live tactical LLM execution, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, BLK-test source mutation, arbitrary shell as BLK-test behavior, active-vault filesystem scanning, protected BLK-req vault body reads/copying/parsing/hashing/mutation, runtime active-vault hash comparison, backend promotion, staged revision execution, authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, runtime RTM generation, runtime RTM IDs, RTM ledgers, runtime coverage matrices, RTM drift rejection authority, production sandbox/cgroup/VM/network/host-secret isolation claims, or source mutation outside exact approved allowlists.

Escalation fixtures created here are advisory operator packages only. They preserve evidence identity, bounded excerpts, and raw-evidence references supplied by the caller; they do not fetch raw logs, upload artifacts, post to Discord, open GitHub issues, or decide whether a human approval is valid.

---

## 2. BLK-024 Selection Rationale

BLK-024 Track I says BLK-System needs concise status reports, token-bounded escalation packages, obvious failure ceilings, health-check/runbook clarity, and common-failure runbooks. After BLK-SYSTEM-027, runtime RTM generation remains unapproved; therefore the safest next sprint is Track I observability/runbooks, not Track H runtime ledger generation.

This sprint remains L1/L0 because Track I can improve operator clarity without climbing any runtime authority ladder.

---

## 3. BLK-001 Through BLK-006 Alignment Matrix

| Governing doc | Relevance to BLK-SYSTEM-028 | Preserved boundary |
| --- | --- | --- |
| BLK-001 — Master Architecture | Operator reports summarize which BLK-System domain is blocked: BLK-req, Hermes planning, BLK-pipe mutation, BLK-test evidence, BEO, RTM, or human approval. | Summary fixtures do not merge domain authorities or let observability mutate/verify/publish/generate. |
| BLK-002 — Artifact Lifecycle | Runbook language must distinguish stale/lint/schema/approval problems in BLK-req artifacts from runtime authority. | No active-vault scanning, protected-body reads, promotion, or staged revision execution. |
| BLK-003 — Orchestration Protocol | Escalation packages should make failure ceiling, reverted state, dirty state, POSIX route, and needed human decision obvious. | Escalation packages are evidence summaries only; they do not dispatch tactical work or approve retries. |
| BLK-004 — BLK-pipe V47 Suite | Common runbooks cover invalid payload, unauthorized mutation, validation failure, output flood, invalid revert anchor, and dirty workspace status. | Go BLK-pipe remains the deterministic enforcement authority; Python observability is not an executor. |
| BLK-005 — BLK-Req Specification | Status fixtures may refer to trace artifact IDs and `version_hash` values supplied by the caller. | No requirement/use-case body parsing, hashing, or drift decision. |
| BLK-006 — BLK-Req Implementation Brief | Protected-vault hard-deny and HITL authorization remain central operator explanations. | No protected-vault body reads and no Discord/HITL approval capture by this helper. |

---

## 4. Planned Tasks

### Task 0 — Publish plan and task-000 outcome

**Deliverables:**

- `docs/plans/blk-system-028_operator-ux-observability-runbooks.md`
- `docs/outcomes/BLK-SYSTEM-028_task-000-outcome.md`

**Verification:**

```bash
git diff --check -- docs/plans/blk-system-028_operator-ux-observability-runbooks.md docs/outcomes/BLK-SYSTEM-028_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
for p in [
    Path('docs/plans/blk-system-028_operator-ux-observability-runbooks.md'),
    Path('docs/outcomes/BLK-SYSTEM-028_task-000-outcome.md'),
]:
    text = p.read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, p
PY
```

**Commit:** `docs: plan blk-system sprint 028 operator observability`

### Task 1 — Inventory current operator failure surfaces and runbook vocabulary

**Deliverables:**

- `docs/reviews/BLK-SYSTEM-028_operator-observability-runbook-inventory.md`
- `docs/outcomes/BLK-SYSTEM-028_task-001-outcome.md`

**Acceptance criteria:**

- Inventory maps common operator-facing failure classes to owning BLK-System domain, likely evidence inputs, concise status phrase, needed human decision, and forbidden authority inheritance.
- Must cover at minimum: invalid payload, unauthorized mutation, syntax/validation gate failure, output flood, invalid revert anchor, disabled BLK-test, draft-only BEO, RTM non-generation, missing approval, stale/replayed approval, protected-vault request, dirty workspace, and unknown/malformed report.
- Must explicitly say this sprint does not run live health checks; future health checks require a separate authority decision.

**Commit:** `docs: inventory blk operator observability surfaces`

### Task 2 — Implement deterministic local observability fixtures and BLK-031 boundary

**Deliverables:**

- `python/blk_operator_observability_fixtures.py`
- `python/test_blk_operator_observability_fixtures.py`
- `docs/BLK-031_operator-ux-observability-runbook-boundary.md`
- `docs/outcomes/BLK-SYSTEM-028_task-002-outcome.md`
- update `python/test_active_doctrine_review_gates.py` with a persistent BLK-031 boundary gate

**Acceptance criteria:**

- Strict TDD: write RED tests first, watch failure, then implement.
- Helper accepts already-supplied report dictionaries and returns deterministic local status fixtures.
- Each fixture includes `status_fixture: "OPERATOR_OBSERVABILITY_FIXTURE_ONLY"`, `authority: "OBSERVABILITY_ONLY_NOT_EXECUTION"`, owning domain, concise status, failure class, retry/revert/dirty indicators, human decision required, bounded evidence excerpt, raw evidence identity/hash/reference, and no-side-effect booleans.
- Escalation package builder preserves a bounded summary plus evidence hashes/references without embedding unbounded raw logs.
- Rejects unsupported top-level fields, forbidden live authority fields, nested secret/body/path/runtime RTM/publication fields, malformed hashes, non-bool side-effect flags, and unbounded excerpt settings.
- Source must not import or call live execution/network/process/file-scanning APIs (`subprocess`, `socket`, `requests`, `urllib`, `os.system`, `eval`, `exec`, `__import__`, `open`, `Path.read_text`, package managers, Git commands, Discord/GitHub APIs).
- BLK-031 pins current Track I L1/L0 no-authority semantics and runbook vocabulary.

**Focused verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_observability_fixtures -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
```

**Commit:** `feat: add operator observability fixtures`

### Task 3 — Hostile review, remediation, full verification, and closeout

**Deliverables:**

- `docs/reviews/BLK-SYSTEM-028_operator-observability-hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-028_task-003-outcome.md`
- `docs/outcomes/BLK-SYSTEM-028_sprint-closeout.md`
- any exact remediation changes required by the hostile review

**Acceptance criteria:**

- Hostile review explicitly probes: authority laundering, status-action confusion, raw-log token flooding, protected-body leakage, path/body/secret recursion, runtime RTM/publication drift fields, misleading retry approval, dirty workspace ambiguity, and insufficient doctrine gates.
- Any blocker is remediated before closeout.
- Full verification passes:

```bash
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover python 'test_*.py'
git diff --check
git status --short --branch
```

**Commit:** `docs: close blk-system sprint 028 operator observability`

---

## 5. Exact-Path Git Discipline

Every task must stage exact paths only. Do not use `git add .`, broad globs, stash, reset, or checkout to manage task files. After each task:

```bash
git add <exact task paths>
git diff --cached --name-only
git commit -m "<task message>"
git push origin main
git status --short --branch
git log -1 --oneline
git ls-remote origin refs/heads/main
```

---

## 6. Stop Conditions

Stop and escalate rather than broadening scope if any task appears to require:

- live command execution as part of operator health checks;
- reading raw files/logs from paths rather than normalizing caller-supplied evidence;
- storing or uploading escalation artifacts outside the repo docs committed by this sprint;
- approving retries, publication, RTM generation, or drift decisions;
- inspecting protected BLK-req body content;
- mutating source through the observability helper;
- claiming production sandbox or host-secret isolation.
