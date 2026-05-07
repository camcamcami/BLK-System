# BLK-SYSTEM-025 — Published BEO Input Boundary Fixture Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and local hostile review gates when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable. Execute task-by-task with deterministic evidence, exact-path staging, per-task outcome docs, hostile review, and push after each task. Do not use Hindsight unless explicitly requested. Do not run Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke, authoritative BEO publication, RTM generation, RTM drift rejection, protected BLK-req vault body reads, or source mutation outside exact approved allowlists unless a later separate execution approval explicitly grants it.

**Goal:** Define and fixture-test a published-BEO input boundary for future RTM work so `blk-link` can later distinguish publication candidates from already-published BEO input metadata without granting publication or RTM authority now.
**BLK-024 track:** Track G — BEO publication path and Track H — BLK-link offline RTM ledger / maturity level L1 fixture-only with L0 doctrine-boundary update and persistent doctrine gates.
**Architecture:** This sprint does not publish BEOs and does not generate RTM. It creates a deterministic local fixture contract that consumes an already-supplied BEO publication candidate fixture plus an already-supplied publication-receipt fixture, validates canonical identity and no-side-effect flags, and emits `PUBLISHED_BEO_INPUT_FIXTURE_ONLY` metadata suitable for later RTM design without calling a signer, writer, ledger, rollback path, active-vault reader, or RTM generator.
**Tech Stack:** Markdown doctrine/review docs, Python fixture helper, Python `unittest` gates, Git CLI.
**Authority boundary:** Fixture-only and doctrine-only. This plan does not authorize authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, RTM generation, RTM IDs, coverage matrices, active-vault hash comparison as runtime authority, RTM drift rejection authority, protected BLK-req vault body reads/copying/parsing/hashing/mutation, live BLK-test MCP, new live smoke runs, public ledger mutation, signer/storage/rollback authority, or source mutation outside exact approved allowlists.

---

## 0. Current Known State

Planning preflight captured before drafting this plan:

```text
date -Iseconds              -> 2026-05-08T08:07:40+10:00
git status --short --branch -> ## main...origin/main
HEAD                        -> e548378 docs: close blk-system sprint 024 rtm hash metadata
```

Next-ID discovery:

```text
Latest sprint plan/outcome: BLK-SYSTEM-024
No existing docs/plans/blk-system-025* file was found during discovery.
No existing BLK-SYSTEM-025 outcome file was found during discovery.
Latest active BLK doc: docs/BLK-027_rtm-hash-only-metadata-path-boundary.md
Selected sprint ID: BLK-SYSTEM-025
Selected new boundary doc: docs/BLK-028_published-beo-input-boundary.md
```

Selection rationale:

- BLK-SYSTEM-024 closeout recommends a published-BEO input boundary before RTM generation because Track H must not treat publication candidates as published BEOs.
- BLK-027 states future RTM generation requires authoritative BEO publication or a separately approved published-BEO fixture input path.
- This sprint chooses the safer fixture-input path and keeps publication and RTM generation disabled.

---

## 1. Scope and Non-Goals

### In scope

1. Inventory current BEO candidate, publication design, and RTM hash metadata surfaces.
2. Add RED tests for a missing published-BEO input fixture helper and boundary document.
3. Implement deterministic fixture-only published-BEO input construction and rejection rules.
4. Create `docs/BLK-028_published-beo-input-boundary.md` as the active fixture-boundary contract.
5. Add persistent doctrine gates to prevent future edits from converting the fixture into publication, RTM generation, active-vault body reads, or drift rejection authority.
6. Create hostile review, task outcomes, and sprint closeout.

### Non-goals

This sprint must not implement or authorize:

- authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material, cryptographic signing, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution;
- RTM generation, RTM IDs, RTM ledgers, coverage matrices, coverage claims, drift events, drift decisions, or RTM drift rejection authority;
- runtime active-vault hash comparison authority;
- protected BLK-req vault body reads, copying, parsing, hashing, summarizing, comparing, mutation, or exposure under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`;
- production BLK-test MCP, new live BLK-test smoke, arbitrary shell as BLK-test behavior, or BLK-test source mutation;
- treating BEO publication candidate fixtures as already-published BEOs without an explicit `PUBLISHED_BEO_INPUT_FIXTURE_ONLY` receipt fixture.

---

## 2. BLK-001 through BLK-006 Alignment Matrix

| Governing doc | Required boundary | Sprint 025 treatment |
| --- | --- | --- |
| BLK-001 — Master Architecture | Preserve strict separation between `blk-req`, Hermes planning/audit, BLK-pipe mutation, BLK-test evidence, BEO handling, and `blk-link` trace closure. | Adds only a local published-BEO input fixture for future `blk-link`; no BEO publication, RTM ledger, protected-body access, or source-mutation authority is added. |
| BLK-002 — Artifact Lifecycle | Active requirements/use cases remain protected by staging, linting, HITL approval, canonical hashing, and immutable baselines. | Fixture code consumes supplied trace hashes only. It does not read, hash, parse, compare, expose, or mutate active-vault bodies. |
| BLK-003 — Orchestration Protocol | Target BLK-test/BEO/RTM language must not override current disabled/draft-only boundaries. | Publication receipt approval stays fixture-only. RTM approval remains separate. The fixture cannot inherit execution, BLK-test, draft-BEO, candidate, Codex, or RTM approval as publication authority. |
| BLK-004 — BLK-pipe V47 Suite | BLK-pipe remains deterministic authority for bounded mutation, validation, cleanup, reports, and exact-path staging. | Sprint changes are limited to exact docs/Python allowlists. No BLK-pipe execution or validation-profile authority changes are in scope. |
| BLK-005 — BLK-Req Specification | BEOs and future RTMs bind to canonical artifact hashes; drift rejection is target-state until explicitly authorized. | Fixture preserves canonical trace artifacts and BEO hash identity without making coverage or drift decisions. |
| BLK-006 — BLK-Req Implementation Brief | Protected-vault hard-deny, staged revisions, and HITL authorization remain BLK-req/backend authority. | Fixture code rejects active-vault read flags and body-bearing evidence. It does not implement a backend active-vault reader. |

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
4. Remove Python caches before staging:
   ```bash
   python3 - <<'PY'
   from pathlib import Path
   import shutil
   for p in [Path('python/__pycache__'), Path('python/.pytest_cache'), Path('.pytest_cache')]:
       if p.exists():
           shutil.rmtree(p)
   PY
   ```
5. Write `docs/outcomes/BLK-SYSTEM-025_task-00N-outcome.md` recording objective, files, RED/GREEN evidence, verification, exact staged paths, and non-execution statement.
6. Stage exact paths only. Do not use `git add .`, `git add -u`, broad globs, stash, reset, checkout, or broad pathspecs to manage sprint files.
7. Commit and push to `origin/main` after each task commit.

---

## 4. Task 0 — Commit Sprint Plan

**Objective:** Preserve this sprint plan as an in-repo executable contract before implementation begins.

**Files:**

- Create: `docs/plans/blk-system-025_published-beo-input-boundary-fixture.md`
- Create: `docs/outcomes/BLK-SYSTEM-025_task-000-outcome.md`

**Verification:**

```bash
git diff --check -- docs/plans/blk-system-025_published-beo-input-boundary-fixture.md docs/outcomes/BLK-SYSTEM-025_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
fence = chr(96) * 3
for path in [Path('docs/plans/blk-system-025_published-beo-input-boundary-fixture.md'), Path('docs/outcomes/BLK-SYSTEM-025_task-000-outcome.md')]:
    text = path.read_text()
    assert text.count(fence) % 2 == 0, path
PY
```

**Commit message:** `docs: plan blk-system sprint 025 published beo input`

---

## 5. Task 1 — Inventory Published-BEO Input Prerequisites

**Objective:** Produce a bounded inventory of current BEO publication candidate fixtures, authoritative publication design boundaries, RTM hash-only metadata prerequisites, and protected-vault exclusions.

**Files:**

- Create: `docs/outcomes/BLK-SYSTEM-025_task-001-outcome.md`

**Required source inventory:**

- `docs/BLK-022_authoritative-beo-publication-design-boundary.md`
- `docs/BLK-023_offline-rtm-ledger-design-boundary.md`
- `docs/BLK-024_blk-system-development-roadmap.md`
- `docs/BLK-026_beo-publication-candidate-fixture-boundary.md`
- `docs/BLK-027_rtm-hash-only-metadata-path-boundary.md`
- `docs/outcomes/BLK-SYSTEM-024_sprint-closeout.md`
- `python/beo_publication_candidate_fixtures.py`
- `python/test_beo_publication_candidate_fixtures.py`
- `python/rtm_hash_only_metadata_path_fixtures.py`
- `python/test_rtm_hash_only_metadata_path_fixtures.py`
- `python/test_active_doctrine_review_gates.py`

**Acceptance criteria:**

- Inventory distinguishes BEO publication candidates from published-BEO input fixtures.
- Inventory names exact receipt fixture fields required for `PUBLISHED_BEO_INPUT_FIXTURE_ONLY`.
- Inventory records forbidden publication side-effect fields, forbidden protected-body fields, and forbidden RTM authority fields.
- No implementation files are changed in this task.

**Verification commands:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  python.test_beo_publication_candidate_fixtures \
  python.test_rtm_hash_only_metadata_path_fixtures \
  python.test_active_doctrine_review_gates -v
git diff --check -- docs/outcomes/BLK-SYSTEM-025_task-001-outcome.md
```

**Commit message:** `docs: inventory published beo input prerequisites`

---

## 6. Task 2 — Add Published-BEO Input Fixture

**Objective:** Add a deterministic local fixture helper and boundary document proving the published-BEO input shape without publishing BEOs, generating RTM, computing coverage, deciding drift, or reading protected bodies.

**Files:**

- Create: `python/test_published_beo_input_boundary_fixtures.py`
- Create: `python/published_beo_input_boundary_fixtures.py`
- Create: `docs/BLK-028_published-beo-input-boundary.md`
- Create: `docs/outcomes/BLK-SYSTEM-025_task-002-outcome.md`

**Required RED tests before implementation:**

- happy-path fixture preserves candidate identity, canonical BEO hash, canonical trace artifacts, receipt identity, and no-side-effect booleans;
- FAIL candidate evidence remains failed input metadata and cannot become success;
- malformed candidate hashes, malformed trace hashes, missing IDs, active-vault read flags, body-bearing fields, publication side-effect flags, signer/storage/ledger/rollback execution flags, RTM authority fields, non-candidate BEO states, and bad receipt fixtures fail closed;
- implementation performs no protected-vault file reads and imports no live transport/storage/network/process modules.

**Acceptance criteria:**

- The helper exports `build_published_beo_input_boundary_fixture(...)`.
- Output uses `input_status: "PUBLISHED_BEO_INPUT_FIXTURE_ONLY"` and `rtm_status: "NOT_GENERATED"`.
- Output sets `publication_performed`, `signature_generated`, `immutable_storage_written`, `public_ledger_mutated`, `rollback_executed`, `active_vault_read`, `protected_body_read`, `rtm_created`, `matrix_created`, and `drift_decision_made` to `False`.
- Output carries only supplied candidate and receipt metadata and records `publication_receipt_scope: "PUBLISHED_BEO_INPUT_FIXTURE_ONLY"`.
- BLK-028 clearly states L1 fixture-only authority and future-approval stop conditions.

**Verification commands:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_published_beo_input_boundary_fixtures -v
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
```

**Commit message:** `feat: add published beo input fixtures`

---

## 7. Task 3 — Add Persistent Doctrine Gate and Close Sprint

**Objective:** Add an active doctrine gate for BLK-028, run hostile review, remediate any blockers, and close the sprint.

**Files:**

- Modify: `python/test_active_doctrine_review_gates.py`
- Create: `docs/reviews/BLK-SYSTEM-025_published-beo-input-boundary-review.md`
- Create: `docs/outcomes/BLK-SYSTEM-025_task-003-outcome.md`
- Create: `docs/outcomes/BLK-SYSTEM-025_sprint-closeout.md`

**Acceptance criteria:**

- Active doctrine gate requires BLK-028 fixture-only/no-publication/no-RTM/no-drift/no-protected-body markers.
- Active doctrine gate scans `python/published_beo_input_boundary_fixtures.py` for forbidden live dependency and authority markers.
- Hostile review returns PASS or records finding IDs and remediations before closeout.
- Final verification passes.
- Every sprint task has an outcome document.

**Final verification commands:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_published_beo_input_boundary_fixtures -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
git status --short --branch
```

**Commit message:** `docs: close blk-system sprint 025 published beo input`

---

## 8. Final Acceptance Criteria

The sprint is complete when:

- `docs/plans/blk-system-025_published-beo-input-boundary-fixture.md` is committed and pushed.
- Every task has an outcome doc under `docs/outcomes/`.
- `python/published_beo_input_boundary_fixtures.py` and tests exist and pass.
- `docs/BLK-028_published-beo-input-boundary.md` exists and states the fixture-only, no-publication, no-RTM, no-protected-body boundary.
- `python/test_active_doctrine_review_gates.py` pins the BLK-028 boundary.
- Hostile review exists and any blockers are remediated.
- Full Go/Python verification passes.
- Final closeout is committed and pushed to `origin/main`.
