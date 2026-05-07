# BLK-SYSTEM-022 — BLK-test Pilot Readiness Design Review Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `requesting-code-review` when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable. Execute task-by-task with deterministic evidence, exact-path staging, per-task outcome docs, hostile review, and push after each task. Do not use Hindsight unless explicitly requested. Do not run Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke, authoritative BEO publication, RTM generation, or RTM authority unless a separate execution approval explicitly grants it.

**Goal:** Define the BLK-test pilot-readiness boundary and proof checklist before any broader live BLK-test authority is requested.
**BLK-024 track:** Track F — BLK-test production-readiness ladder / maturity level L0 doctrine-only design review, with L1 persistent doctrine-gate tests.
**Architecture:** BLK-test remains an evidence-only physics oracle boundary. BLK-017, BLK-018, BLK-019, and BLK-020 remain the current active contracts: disabled generic transport, inert workspace/process probes, one-run approval/source-evidence validation, and one accepted first live fixed-tool smoke exception. This sprint must not start a live BLK-test MCP server or repeat the smoke; it only writes the pilot readiness contract and adds gates that prevent future documents from silently promoting BLK-test to mutation, publication, RTM, arbitrary-shell, protected-vault, or production authority.
**Tech Stack:** Markdown doctrine/review docs, Python `unittest` doctrine gates, Git CLI.
**Authority boundary:** Doctrine/review and local gate tests only. This plan does not authorize production BLK-test MCP, new live BLK-test smoke runs, arbitrary shell as BLK-test behavior, source mutation by BLK-test, protected BLK-req vault body reads, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, or source mutation outside exact approved allowlists.

---

## 0. Current Known State

Planning preflight captured before drafting this plan:

```text
date -Iseconds              -> 2026-05-07T21:40:26+10:00
git status --short --branch -> ## main...origin/main
HEAD                        -> 6b3fea4 docs: close blk-system sprint 021 python adapter policy
```

Relevant existing sprint/document state:

```text
docs/BLK-024_blk-system-development-roadmap.md
docs/plans/blk-system-021_python-adapter-policy-layer-hardening.md
docs/outcomes/BLK-SYSTEM-021_sprint-closeout.md
docs/reviews/BLK-SYSTEM-021_post-remediation-hostile-review.md
docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md
docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md
docs/BLK-019_blk-test-mcp-approval-source-evidence-authorization.md
docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md
```

Next-ID discovery:

```text
No existing docs/plans/blk-system-022* file was found.
No existing BLK-SYSTEM-022 outcome file was found.
BLK-SYSTEM-021 closeout lists BLK-test pilot design review as the next safe follow-up after validation-profile and adapter hardening.
Selected sprint ID: BLK-SYSTEM-022
Selected plan path: docs/plans/blk-system-022_blk-test-pilot-readiness-design-review.md
```

BLK-024 Track F source:

- Track F says BLK-test must move toward production-readiness without gaining planning, mutation, publication, or RTM authority.
- Track F preserves fixed-tool registry semantics: no arbitrary shell, caller-supplied command execution, or dynamic tool expansion.
- Track F requires workspace isolation proof against target-repo escape, `.git` ancestry/descendant escape, symlink escape, secret exposure, timeout failure, output flood, and cleanup failure.
- Track F separates pilot real-repo verification authority from synthetic smoke authority.
- Track F requires every BLK-test output to remain evidence only: PASS/FAIL/BLOCKED/FATAL evidence must not publish BEOs, mutate source, or generate RTM.

Current BLK-test boundary observed during planning:

- BLK-017: generic live BLK-test MCP remains disabled; transport work is stdio-only metadata/probe evidence.
- BLK-018: workspace/process-control probes are inert local fixtures only; they do not execute fixed-tool tests or target the primary repository.
- BLK-019: approval/source-evidence records are BLK-test-specific, one-run/scoped, expiry/replay checked, and cannot reuse Codex-live approval.
- BLK-020: one accepted first live fixed-tool smoke exists for a synthetic isolated workspace and one fixed tool, `run_ast_validation`; it is historical and does not authorize production BLK-test MCP.
- BLK-SYSTEM-021 closed the prerequisite Track E adapter hardening and explicitly left BLK-test pilot design review as a later candidate.

---

## 1. Scope and Non-Goals

### In scope

1. Inventory the current BLK-test doctrine and implementation surfaces without starting live transport.
2. Add RED doctrine gates for a missing BLK-test pilot-readiness boundary document and required non-authority markers.
3. Create `docs/BLK-025_blk-test-pilot-readiness-boundary.md` as a design-only boundary contract that defines what must be proven before any later L4 pilot request.
4. Create a hostile readiness design review under `docs/reviews/` with finding IDs, stop conditions, pilot prerequisites, and explicit rejected authority paths.
5. Preserve BLK-017 through BLK-020 as current active contracts unless the review finds a narrow wording contradiction that must be patched.
6. Record per-task outcome docs and a sprint closeout.

### Non-goals

This sprint must not implement or authorize:

- production BLK-test MCP;
- new live BLK-test smoke runs or replay of BLK-SYSTEM-014/BLK-020 smoke;
- arbitrary shell, dynamic command execution, package-manager execution, cyber tooling, or model/network calls as BLK-test behavior;
- source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test;
- BLK-test execution against `/home/dad/BLK-System`, a real target repository, a `.git` root/ancestor/descendant, protected BLK-req vault paths, root paths, home paths, or host-secret-bearing paths;
- protected BLK-req vault body reads, copying, parsing, hashing, mutation, or drift comparison;
- authoritative BEO publication, public ledger mutation, signer/storage/rollback authority;
- RTM generation, RTM drift rejection, or active requirement coverage decisions;
- production sandbox, VM, cgroup, network, or host-secret isolation claims;
- treating PASS evidence as publication, RTM, or source-mutation authority.

---

## 2. BLK-001 through BLK-006 Alignment Matrix

| Governing doc | Required boundary | Sprint 022 treatment |
| --- | --- | --- |
| BLK-001 — Master Architecture | Preserve strict separation between BLK-req laws, Hermes planning/audit, BLK-pipe source mutation, BLK-test evidence, and blk-link trace closure. | BLK-test pilot readiness is documented as evidence-only. No source mutation, publication, or RTM authority is added. |
| BLK-002 — Artifact Lifecycle | Requirements/use-case staging, HITL approval, canonical hashing, and active-vault isolation remain separate from tactical and verification layers. | BLK-test readiness may reference opaque `version_hash`/`trace_artifacts` metadata but must not read, hash, parse, or compare protected bodies. |
| BLK-003 — Orchestration Protocol | BLK-test Phase 4.2 target architecture must remain separate from current disabled/smoke/pilot authority. | The design review defines the proof ladder before pilot authority and preserves human approval, POSIX routing, hostile audit, and escalation boundaries. |
| BLK-004 — BLK-pipe V47 Suite | BLK-pipe remains deterministic compiled authority for source mutation, allowlists, validation, cleanup, Git, and report evidence. | BLK-test remains post-mutation evidence only and cannot broaden BLK-pipe allowlists or mutate source. |
| BLK-005 — BLK-Req Specification | Requirements/use-cases remain atomic, hash-bound, and traceable through canonical metadata. | BLK-test pilot readiness uses canonical metadata only and does not make coverage, drift, or active-vault truth claims. |
| BLK-006 — BLK-Req Implementation Brief | Protected vault hard-deny, staged revisions, and Discord/HITL authorization remain BLK-req/backend authority. | The pilot readiness boundary must explicitly reject active-vault body reads and protected path execution by BLK-test. |

---

## 3. Controller Workflow for Each Task

For each task:

1. Preflight:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   git status --short --branch
   git log -1 --oneline
   ```
2. Read this task section and the governing docs named in it.
3. For code/test changes, use strict TDD:
   - add or patch the failing focused test first;
   - run the focused test and capture RED;
   - implement only the scoped file changes;
   - rerun focused test and capture GREEN;
   - run shared verification.
4. Shared verification:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   go test ./...
   go vet ./...
   PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
   git diff --check
   ```
5. Remove generated Python cache before status/staging:
   ```bash
   python3 - <<'PY'
   from pathlib import Path
   import shutil
   for p in [Path('python/__pycache__'), Path('python/.pytest_cache'), Path('.pytest_cache')]:
       if p.exists():
           shutil.rmtree(p)
   PY
   ```
6. Write a task outcome doc under `docs/outcomes/` recording RED/GREEN evidence, exact changed paths, verification commands, and the non-execution statement.
7. Stage exact paths only. Do not use `git add .`, `git add -u`, broad globs, stash, reset, checkout, or broad pathspecs to manage task files.
8. Verify staged paths:
   ```bash
   git diff --cached --name-only
   ```
9. Commit with the task-specific message.
10. Push to `origin/main` after each task commit.

---

## 4. Task 0 — Commit Sprint Plan

**Objective:** Preserve this sprint plan as an in-repo executable contract before implementation begins.

**Files:**

- Create: `docs/plans/blk-system-022_blk-test-pilot-readiness-design-review.md`
- Create: `docs/outcomes/BLK-SYSTEM-022_task-000-outcome.md`

**Steps:**

1. Verify the plan exists and contains required authority markers:
   ```bash
   test -f docs/plans/blk-system-022_blk-test-pilot-readiness-design-review.md
   grep -F "Track F — BLK-test production-readiness ladder" docs/plans/blk-system-022_blk-test-pilot-readiness-design-review.md
   grep -F "does not authorize production BLK-test MCP" docs/plans/blk-system-022_blk-test-pilot-readiness-design-review.md
   grep -F "does not authorize RTM generation" docs/plans/blk-system-022_blk-test-pilot-readiness-design-review.md
   grep -F "source mutation by BLK-test" docs/plans/blk-system-022_blk-test-pilot-readiness-design-review.md
   git diff --check -- docs/plans/blk-system-022_blk-test-pilot-readiness-design-review.md
   ```
2. Create `docs/outcomes/BLK-SYSTEM-022_task-000-outcome.md` recording:
   - plan path;
   - BLK-024 Track F source;
   - current preflight status;
   - no implementation change;
   - non-execution statement.
3. Run plan-only verification:
   ```bash
   git diff --check -- docs/plans/blk-system-022_blk-test-pilot-readiness-design-review.md docs/outcomes/BLK-SYSTEM-022_task-000-outcome.md
   python3 - <<'PY'
   from pathlib import Path
   for path in [Path('docs/plans/blk-system-022_blk-test-pilot-readiness-design-review.md'), Path('docs/outcomes/BLK-SYSTEM-022_task-000-outcome.md')]:
       text = path.read_text()
       fence = chr(96) * 3
       assert text.count(fence) % 2 == 0, path
   PY
   ```
4. Stage exact files:
   ```bash
   git add docs/plans/blk-system-022_blk-test-pilot-readiness-design-review.md \
           docs/outcomes/BLK-SYSTEM-022_task-000-outcome.md
   git diff --cached --name-only
   ```
5. Commit and push:
   ```bash
   git commit -m "docs: plan blk-system sprint 022 blk-test readiness"
   git push origin main
   ```

---

## 5. Task 1 — Inventory BLK-test Current-State Contracts

**Objective:** Produce a bounded inventory of current BLK-test doctrine, code, tests, evidence vocabulary, and hard stop conditions before writing any new boundary document.

**Files:**

- Create: `docs/outcomes/BLK-SYSTEM-022_task-001-outcome.md`

**Required source inventory:**

1. Read and summarize:
   - `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md`
   - `docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md`
   - `docs/BLK-019_blk-test-mcp-approval-source-evidence-authorization.md`
   - `docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md`
   - `docs/BLK-024_blk-system-development-roadmap.md`
2. Inspect implementation/test surfaces without running live transport:
   - `python/blk_test_mcp_disabled_transport.py`
   - `python/test_blk_test_mcp_disabled_transport.py`
   - `python/blk_test_mcp_workspace_process_probes.py`
   - `python/test_blk_test_mcp_workspace_process_probes.py`
   - `python/blk_test_mcp_approval_authorization.py`
   - `python/test_blk_test_mcp_approval_authorization.py`
   - `python/blk_test_mcp_fixed_tool_live_smoke.py`
   - `python/test_blk_test_mcp_fixed_tool_live_smoke.py`
   - `python/test_active_doctrine_review_gates.py`
3. Record a readiness table with at least these rows:
   - disabled generic startup;
   - fixed-tool registry descriptor and one-smoke exception;
   - workspace ancestry/descendant `.git` escape rejection;
   - protected BLK-req path/body exclusion;
   - source-evidence binding;
   - approval replay/expiry rejection;
   - process timeout/output flood/cleanup behavior;
   - evidence statuses and non-projection to BEO/RTM;
   - production sandbox/host-secret claims.
4. Identify candidate pilot prerequisites, but do not grant pilot authority.

**Verification commands:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  python.test_blk_test_mcp_disabled_transport \
  python.test_blk_test_mcp_workspace_process_probes \
  python.test_blk_test_mcp_approval_authorization \
  python.test_blk_test_mcp_fixed_tool_live_smoke \
  python.test_active_doctrine_review_gates -v
git diff --check -- docs/outcomes/BLK-SYSTEM-022_task-001-outcome.md
```

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-022_task-001-outcome.md` must record inventory findings, verification output, exact paths inspected, and the non-execution statement.

**Commit message:**

```text
docs: inventory blk-test pilot readiness contracts
```

---

## 6. Task 2 — Add RED Doctrine Gates for Pilot Readiness Boundary

**Objective:** Add persistent doctrine gates proving the repository lacks a dedicated BLK-test pilot-readiness boundary and required non-authority markers before the new document is written.

**Files:**

- Modify: `python/test_active_doctrine_review_gates.py`
- Create: `docs/outcomes/BLK-SYSTEM-022_task-002-outcome.md`

**Required RED gate:**

Add a focused test, recommended name:

```text
test_sprint022_blk_test_pilot_readiness_boundary_preserves_evidence_only_authority
```

The gate should fail until `docs/BLK-025_blk-test-pilot-readiness-boundary.md` exists and includes markers such as:

```text
BLK-test pilot readiness boundary
Design-only boundary contract
Track F — BLK-test production-readiness ladder
evidence only
fixed-tool registry
no arbitrary shell
no source mutation
no protected BLK-req vault body reads
no authoritative BEO publication
no RTM generation
no production BLK-test MCP
separate human approval
L4 pilot authority requires a later explicit sprint
```

The same gate may also verify that BLK-017 through BLK-020 remain discoverable and still include their current non-authority language.

**Focused RED command:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
```

**Expected RED:** the new gate fails because `docs/BLK-025_blk-test-pilot-readiness-boundary.md` does not yet exist or lacks required markers.

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-022_task-002-outcome.md` must record the RED output, exact changed paths, and confirm no BLK-test live authority was granted.

**Commit message:**

```text
test: add blk-test pilot readiness doctrine gate
```

---

## 7. Task 3 — Draft BLK-025 Pilot Readiness Boundary and Turn Gates GREEN

**Objective:** Create the design-only boundary document that defines what must be proven before any later BLK-test pilot authority request.

**Files:**

- Create: `docs/BLK-025_blk-test-pilot-readiness-boundary.md`
- Modify: `python/test_active_doctrine_review_gates.py` only if the Task 2 gate needs a narrow marker correction
- Create: `docs/outcomes/BLK-SYSTEM-022_task-003-outcome.md`

**BLK-025 requirements:**

1. Header status must be explicit: `Design-only boundary contract — not runtime authority`.
2. Include a `Non-Execution and Non-Authority Boundary` section near the top.
3. Anchor to BLK-024 Track F and classify the current document as L0 doctrine-only.
4. Preserve the current-state ladder:
   - BLK-017: disabled generic transport.
   - BLK-018: inert workspace/process-control probes.
   - BLK-019: one-run/scoped approval/source-evidence validation.
   - BLK-020: one historical synthetic fixed-tool smoke exception.
5. Define the later L4 pilot authority prerequisites without granting them:
   - separate human pilot approval distinct from execution, BLK-test smoke, BEO publication, and RTM approval;
   - fixed-tool registry with no caller-supplied commands or dynamic tool expansion;
   - source-bound evidence envelope tied to BLK-pipe report identity, commit hash, `pre_engine_hash`, `post_engine_hash`, `beb_id`, and canonical `trace_artifacts`;
   - workspace isolation proof against real target-repo escape, `.git` ancestry/descendant escape, symlink escape, protected paths, root/home paths, and host-secret paths;
   - process timeout, output-flood, descendant-kill, pipe-holder, and cleanup-failure behavior;
   - PASS/FAIL/BLOCKED/FATAL/transport status semantics that do not project to BEO publication, RTM generation, BLK-req promotion, or source mutation;
   - replay hashes and expiry/reuse rejection.
6. Include stop conditions matching BLK-024 Section 7 where relevant.
7. Include a future-sprint split table that separates synthetic-smoke expansion, L4 pilot, BEO publication, and RTM ledger work.

**Focused GREEN command:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
```

**Shared GREEN commands:**

```bash
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
```

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-022_task-003-outcome.md` must record Task 2 RED, Task 3 GREEN, exact changed paths, and the no-authority-expansion statement.

**Commit message:**

```text
docs: define blk-test pilot readiness boundary
```

---

## 8. Task 4 — Hostile Design Review and Sprint Closeout

**Objective:** Hostile-review BLK-SYSTEM-022 against BLK-024 Track F, BLK-001 through BLK-006, BLK-017 through BLK-020, and the non-authority boundaries in this plan.

**Files:**

- Create: `docs/reviews/BLK-SYSTEM-022_blk-test-pilot-readiness-design-review.md`
- Create: `docs/outcomes/BLK-SYSTEM-022_task-004-outcome.md`
- Create: `docs/outcomes/BLK-SYSTEM-022_sprint-closeout.md`
- Modify, only if the review finds a narrow contradiction: `docs/BLK-025_blk-test-pilot-readiness-boundary.md` or `python/test_active_doctrine_review_gates.py`

**Hostile review checklist:**

1. Does BLK-025 remain design-only and avoid any live runtime authority?
2. Does it preserve BLK-017 disabled generic transport?
3. Does it preserve BLK-018 inert workspace/process-control probe scope?
4. Does it preserve BLK-019 one-run/scoped BLK-test-specific approval/source-evidence validation?
5. Does it preserve BLK-020 as a historical single synthetic fixed-tool smoke exception only?
6. Does it reject production BLK-test MCP, new live smoke, arbitrary shell, caller-supplied commands, dynamic tool expansion, source mutation, protected-vault body reads, BEO publication, RTM generation, drift rejection, public ledger mutation, signer/storage/rollback authority, and production sandbox claims?
7. Are later synthetic-smoke, pilot, BEO, and RTM authorities split into separate future approvals?
8. Does the pilot prerequisite list include workspace `.git` ancestry/descendant escape, symlink escape, protected path, root/home, host-secret, timeout, output flood, descendant process, cleanup, replay, and approval reuse failures?
9. Do persistent doctrine gates fail closed on missing pilot-readiness authority markers?
10. Are follow-up candidates stated as prerequisites, not authority grants?

**Verification commands:**

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
git status --short --branch
```

**Closeout requirements:**

`docs/outcomes/BLK-SYSTEM-022_sprint-closeout.md` must include:

- final commit table for task commits;
- summary of the BLK-test pilot-readiness boundary;
- final verification output;
- non-execution statement;
- no-authority-expansion statement;
- residual/next-sprint seeds.

Likely next-sprint seeds after closeout:

- BEO publication implementation design-to-fixture bridge, if the BLK-test pilot readiness boundary passes hostile review and the operator chooses Track G next;
- a separate synthetic-smoke expansion plan only if explicit human approval selects a new source-bound one-run envelope;
- RTM hash-only metadata path design only after publication prerequisites remain separated and protected-vault body reads remain denied.

**Staging and commit:**

```bash
git add docs/reviews/BLK-SYSTEM-022_blk-test-pilot-readiness-design-review.md \
        docs/outcomes/BLK-SYSTEM-022_task-004-outcome.md \
        docs/outcomes/BLK-SYSTEM-022_sprint-closeout.md
# Include docs/BLK-025... or test gate path here only if Task 4 remediation changed them.
git diff --cached --name-only
git commit -m "docs: close blk-system sprint 022 blk-test readiness"
git push origin main
```

---

## 9. Acceptance Criteria

BLK-SYSTEM-022 is complete only if all criteria below pass:

1. `docs/BLK-025_blk-test-pilot-readiness-boundary.md` exists and is explicitly design-only / not runtime authority.
2. BLK-025 anchors to BLK-024 Track F and defines the current BLK-test ladder across BLK-017, BLK-018, BLK-019, and BLK-020.
3. BLK-025 defines later L4 pilot prerequisites without granting pilot authority.
4. BLK-025 explicitly denies production BLK-test MCP, new live smoke, arbitrary shell, caller-supplied commands, dynamic tool expansion, source mutation, protected-vault body reads, BEO publication, RTM generation, RTM drift rejection, public ledger mutation, signer/storage/rollback authority, and production sandbox claims.
5. Persistent doctrine gates cover the pilot-readiness boundary and required non-authority markers.
6. A hostile design review exists at `docs/reviews/BLK-SYSTEM-022_blk-test-pilot-readiness-design-review.md`.
7. Every task has an outcome doc under `docs/outcomes/`.
8. Full verification passes:
   ```bash
   go test ./...
   go vet ./...
   PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
   git diff --check
   ```
9. Sprint closeout is committed and pushed.

---

## 10. Non-Execution and No-Authority-Expansion Statement

This plan does not authorize Hindsight use, Codex use, live tactical LLM execution, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, arbitrary shell as BLK-test behavior, source mutation by BLK-test, protected BLK-req vault body reads, copying, parsing, hashing, or mutation, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, production sandbox/cgroup/VM/network/host-secret isolation claims, or source mutation outside exact approved allowlists.

The intended authority movement is only documentation clarity and persistent doctrine gating: BLK-test pilot-readiness prerequisites become explicit, but any actual synthetic smoke expansion, L4 pilot runtime, BEO publication, or RTM generation still requires a later separate sprint plan, explicit human approval, deterministic tests, hostile review, and closeout.
