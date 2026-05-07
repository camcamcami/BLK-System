# BLK-SYSTEM-027 — RTM Generation Readiness Proposal Fixture Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and local hostile review gates when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable. Execute task-by-task with deterministic evidence, exact-path staging, per-task outcome docs, hostile review, and push after each task. Do not use Hindsight unless explicitly requested. Do not run Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke, authoritative BEO publication, runtime RTM generation, RTM drift rejection, active-vault filesystem scanning, protected BLK-req vault body reads, or source mutation outside exact approved allowlists.

**Goal:** Create a deterministic proposal-only fixture boundary for a future RTM generation sprint, proving that published-BEO input fixtures and active-vault hash metadata backend fixtures can be packaged for later human RTM approval without generating RTM now.
**BLK-024 track:** Track H — BLK-link offline RTM ledger, with Track B hash-only metadata and Track G published-BEO input prerequisites / maturity level L1 fixture-only with L0 doctrine-boundary update and persistent doctrine gates.
**Architecture:** This sprint does not generate an RTM ledger, does not create coverage matrices, does not compare active-vault hashes as runtime authority, and does not make drift decisions. It creates a local proposal fixture that consumes already-supplied `PUBLISHED_BEO_INPUT_FIXTURE_ONLY` and `ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY` records, validates no-body/no-side-effect boundaries, and emits `RTM_GENERATION_READINESS_PROPOSAL_FIXTURE_ONLY` evidence for a later human decision.
**Tech Stack:** Markdown doctrine/review docs, Python fixture helper, Python `unittest` gates, Git CLI.
**Authority boundary:** Proposal-only fixture and doctrine-only. This plan does not authorize protected BLK-req vault body reads/copying/parsing/hashing/mutation, active-vault filesystem scanning, runtime active-vault hash comparison, runtime RTM generation, RTM IDs, RTM ledgers, coverage matrices, drift decisions, RTM drift rejection authority, authoritative BEO publication, runtime `PUBLISHED` BEO output, signer/storage/ledger/rollback side effects, live BLK-test MCP, new live smoke runs, or source mutation outside exact approved allowlists.

---

## 0. Current Known State

Planning preflight captured before drafting this plan:

```text
date -Iseconds              -> 2026-05-08T09:14:35+10:00
git status --short --branch -> ## main...origin/main
HEAD                        -> 1a0ef64 docs: close blk-system sprint 026 active vault hash backend
```

Next-ID discovery:

```text
Latest sprint plan/outcome: BLK-SYSTEM-026
No existing docs/plans/blk-system-027* file was found during discovery.
No existing BLK-SYSTEM-027 outcome file was found during discovery.
Latest active BLK doc: docs/BLK-029_active-vault-hash-metadata-backend-boundary.md
Selected sprint ID: BLK-SYSTEM-027
Selected new boundary doc: docs/BLK-030_rtm-generation-readiness-proposal-boundary.md
```

Selection rationale:

- BLK-SYSTEM-026 closeout recommends an RTM generation proposal only after explicit human approval and after published-BEO input plus hash-only metadata backend prerequisites are considered sufficient.
- The operator requested the next BLK-System plan and execution; this sprint treats that as approval to create and execute a proposal-only fixture sprint, not approval to generate RTM.
- BLK-027, BLK-028, and BLK-029 provide the prerequisite fixture boundaries. This sprint packages those prerequisites into a readiness proposal while keeping RTM generation and drift rejection disabled.

---

## 1. Scope and Non-Goals

### In scope

1. Inventory RTM generation prerequisites across BLK-023, BLK-024, BLK-027, BLK-028, BLK-029, and recent sprint closeouts.
2. Add RED tests for a missing RTM generation readiness proposal fixture helper and BLK-030 boundary document.
3. Implement deterministic proposal-only fixture construction from already-supplied published-BEO input fixtures and active-vault backend hash metadata fixtures.
4. Create `docs/BLK-030_rtm-generation-readiness-proposal-boundary.md` as the active proposal-fixture boundary contract.
5. Add persistent doctrine gates preventing future edits from converting the proposal fixture into runtime RTM generation, coverage matrices, active-vault scanning, protected-body access, drift decisions, or publication authority.
6. Create hostile review, task outcomes, and sprint closeout.

### Non-goals

This sprint must not implement or authorize:

- protected BLK-req vault body reads, copying, parsing, hashing, summarizing, comparing, mutation, or exposure under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`;
- active-vault filesystem scanning, active-vault path export, backend promotion, staged revision, or live metadata export from protected paths;
- runtime active-vault hash comparison authority;
- runtime RTM generation, runtime RTM IDs, RTM ledgers, coverage matrices, coverage claims, drift events, drift decisions, or RTM drift rejection authority;
- authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material, cryptographic signing, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution;
- production BLK-test MCP, new live BLK-test smoke, arbitrary shell as BLK-test behavior, or BLK-test source mutation.

---

## 2. BLK-001 through BLK-006 Alignment Matrix

| Governing doc | Required boundary | Sprint 027 treatment |
| --- | --- | --- |
| BLK-001 — Master Architecture | Preserve separation between `blk-req`, Hermes planning/audit, BLK-pipe mutation, BLK-test evidence, BEO handling, and `blk-link` trace closure. | Adds only a local `blk-link` proposal fixture; no RTM ledger, protected-body access, publication, verification, or source mutation authority is added. |
| BLK-002 — Artifact Lifecycle | Active requirements/use cases remain protected by staging, linting, HITL approval, canonical hashing, and immutable baselines. | Consumes supplied hash metadata backend fixture records only; does not read, hash, compare, expose, or mutate active-vault bodies. |
| BLK-003 — Orchestration Protocol | RTM approval must remain separate from execution, BLK-test, and BEO publication. | Proposal records `generation_approval_required: true` and `rtm_generation_authorized: false`; it cannot inherit execution, BLK-test, BEO, Codex, or backend metadata approval. |
| BLK-004 — BLK-pipe V47 Suite | BLK-pipe remains deterministic authority for bounded mutation, validation, cleanup, reports, and exact-path staging. | Sprint changes are exact docs/Python allowlists only. No BLK-pipe execution authority or validation-profile changes are in scope. |
| BLK-005 — BLK-Req Specification | Future RTM work binds to canonical artifact hashes; drift rejection is separate authority. | Proposal fixture preserves canonical hash identities but emits readiness records only, not coverage claims or drift decisions. |
| BLK-006 — BLK-Req Implementation Brief | Protected-vault hard-deny, staged revisions, and HITL authorization remain BLK-req/backend authority. | Proposal fixture rejects protected path/body fields and promotion/revision authority fields. It does not implement a live backend reader. |

---

## 3. Controller Workflow for Each Task

For each task:

1. Preflight:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   git status --short --branch
   git log -1 --oneline
   ```
2. Use strict TDD for code/test changes: write or patch the focused test first, observe RED, implement minimally, observe GREEN, then run shared verification.
3. Shared verification:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   go test ./...
   go vet ./...
   PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
   git diff --check
   ```
4. Remove Python caches before staging.
5. Write `docs/outcomes/BLK-SYSTEM-027_task-00N-outcome.md` recording objective, files, RED/GREEN evidence, verification, exact staged paths, and non-execution statement.
6. Stage exact paths only. Do not use `git add .`, `git add -u`, broad globs, stash, reset, checkout, or broad pathspecs to manage sprint files.
7. Commit and push to `origin/main` after each task commit.

---

## 4. Task 0 — Commit Sprint Plan

**Objective:** Preserve this sprint plan as an in-repo executable contract before implementation begins.

**Files:**

- Create: `docs/plans/blk-system-027_rtm-generation-readiness-proposal-fixture.md`
- Create: `docs/outcomes/BLK-SYSTEM-027_task-000-outcome.md`

**Verification:**

```bash
git diff --check -- docs/plans/blk-system-027_rtm-generation-readiness-proposal-fixture.md docs/outcomes/BLK-SYSTEM-027_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
fence = chr(96) * 3
for path in [Path('docs/plans/blk-system-027_rtm-generation-readiness-proposal-fixture.md'), Path('docs/outcomes/BLK-SYSTEM-027_task-000-outcome.md')]:
    text = path.read_text()
    assert text.count(fence) % 2 == 0, path
PY
```

**Commit message:** `docs: plan blk-system sprint 027 rtm readiness proposal`

---

## 5. Task 1 — Inventory RTM Generation Proposal Prerequisites

**Objective:** Produce a bounded inventory of current RTM design, published-BEO input, hash metadata backend prerequisites, and no-authority exclusions.

**Files:**

- Create: `docs/outcomes/BLK-SYSTEM-027_task-001-outcome.md`

**Required source inventory:**

- `docs/BLK-001_blk-system-master-architecture.md`
- `docs/BLK-002_blk-req-artifact-lifecycle.md`
- `docs/BLK-003_blk-pipe-blk-test-orchestration.md`
- `docs/BLK-005_blk-req-specification.md`
- `docs/BLK-006_blk-req-implementation-brief.md`
- `docs/BLK-023_offline-rtm-ledger-design-boundary.md`
- `docs/BLK-024_blk-system-development-roadmap.md`
- `docs/BLK-027_rtm-hash-only-metadata-path-boundary.md`
- `docs/BLK-028_published-beo-input-boundary.md`
- `docs/BLK-029_active-vault-hash-metadata-backend-boundary.md`
- `docs/outcomes/BLK-SYSTEM-024_sprint-closeout.md`
- `docs/outcomes/BLK-SYSTEM-025_sprint-closeout.md`
- `docs/outcomes/BLK-SYSTEM-026_sprint-closeout.md`
- `python/rtm_hash_only_metadata_path_fixtures.py`
- `python/published_beo_input_boundary_fixtures.py`
- `python/active_vault_hash_metadata_backend_fixtures.py`
- `python/test_active_doctrine_review_gates.py`

**Acceptance criteria:**

- Inventory distinguishes proposal-only readiness from runtime RTM generation.
- Inventory names exact published-BEO input and backend hash metadata fixture fields required for `RTM_GENERATION_READINESS_PROPOSAL_FIXTURE_ONLY`.
- Inventory records forbidden active-vault path fields, body-bearing fields, RTM runtime fields, coverage matrix fields, drift fields, publication fields, and side-effect flags.
- No implementation files are changed in this task.

**Verification commands:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest   python.test_rtm_hash_only_metadata_path_fixtures   python.test_published_beo_input_boundary_fixtures   python.test_active_vault_hash_metadata_backend_fixtures   python.test_active_doctrine_review_gates -v
git diff --check -- docs/outcomes/BLK-SYSTEM-027_task-001-outcome.md
```

**Commit message:** `docs: inventory rtm readiness proposal prerequisites`

---

## 6. Task 2 — Add RTM Generation Readiness Proposal Fixture

**Objective:** Add a deterministic local proposal fixture helper and boundary document proving RTM-generation readiness packaging without runtime RTM generation, coverage matrices, active-vault scanning, protected-body reads, drift decisions, or publication.

**Files:**

- Create: `python/test_rtm_generation_readiness_proposal_fixtures.py`
- Create: `python/rtm_generation_readiness_proposal_fixtures.py`
- Create: `docs/BLK-030_rtm-generation-readiness-proposal-boundary.md`
- Create: `docs/outcomes/BLK-SYSTEM-027_task-002-outcome.md`

**Required RED tests before implementation:**

- happy-path fixture preserves published-BEO input identity, BEO hash, trace artifacts, backend manifest hash, hash metadata identities, and explicit later-approval requirement;
- output uses `proposal_status: "RTM_GENERATION_READINESS_PROPOSAL_FIXTURE_ONLY"`, `rtm_status: "NOT_GENERATED"`, and `rtm_generation_authorized: false`;
- malformed hashes, missing IDs, mismatched trace/hash metadata identities, active-vault/protected path fields, body-bearing fields, RTM runtime fields, coverage matrix fields, drift fields, publication authority fields, side-effect flags, stale/replayed/expired proposal request, and non-string identities fail closed;
- implementation performs no protected-vault file reads and imports no live transport/storage/network/process modules.

**Acceptance criteria:**

- The helper exports `build_rtm_generation_readiness_proposal_fixture(...)`.
- Output records `generation_approval_required: true`, `rtm_generation_authorized: false`, `rtm_created: false`, `matrix_created: false`, and `drift_decision_made: false`.
- Output carries only supplied published-BEO input fixture and backend hash metadata fixture identities.
- BLK-030 clearly states proposal-only L1 fixture authority and future RTM approval stop conditions.

**Verification commands:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_rtm_generation_readiness_proposal_fixtures -v
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
```

**Commit message:** `feat: add rtm readiness proposal fixtures`

---

## 7. Task 3 — Add Persistent Doctrine Gate and Close Sprint

**Objective:** Add an active doctrine gate for BLK-030, run hostile review, remediate any blockers, and close the sprint.

**Files:**

- Modify: `python/test_active_doctrine_review_gates.py`
- Create: `docs/reviews/BLK-SYSTEM-027_rtm-generation-readiness-proposal-review.md`
- Create: `docs/outcomes/BLK-SYSTEM-027_task-003-outcome.md`
- Create: `docs/outcomes/BLK-SYSTEM-027_sprint-closeout.md`

**Acceptance criteria:**

- Active doctrine gate requires BLK-030 proposal-only/no-runtime-RTM/no-active-vault-scan/no-protected-body/no-coverage-matrix/no-drift/no-publication markers.
- Active doctrine gate scans `python/rtm_generation_readiness_proposal_fixtures.py` for forbidden live dependency and authority markers.
- Hostile review returns PASS or records finding IDs and remediations before closeout.
- Final verification passes.
- Every sprint task has an outcome document.

**Final verification commands:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_rtm_generation_readiness_proposal_fixtures -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
git status --short --branch
```

**Commit message:** `docs: close blk-system sprint 027 rtm readiness proposal`

---

## 8. Final Acceptance Criteria

The sprint is complete when:

- `docs/plans/blk-system-027_rtm-generation-readiness-proposal-fixture.md` is committed and pushed.
- Every task has an outcome doc under `docs/outcomes/`.
- `python/rtm_generation_readiness_proposal_fixtures.py` and tests exist and pass.
- `docs/BLK-030_rtm-generation-readiness-proposal-boundary.md` exists and states proposal-only, no-runtime-RTM, no-active-vault-scan, no-protected-body, no-coverage-matrix, no-drift, and no-publication authority.
- `python/test_active_doctrine_review_gates.py` pins the BLK-030 boundary.
- Hostile review exists and any blockers are remediated.
- Full Go/Python verification passes.
- Final closeout is committed and pushed to `origin/main`.
