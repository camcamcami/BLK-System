# BLK-SYSTEM-024 — RTM Hash-Only Metadata Path Fixture Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and local hostile review gates when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable. Execute task-by-task with deterministic evidence, exact-path staging, per-task outcome docs, hostile review, and push after each task. Do not use Hindsight unless explicitly requested. Do not run Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke, authoritative BEO publication, RTM generation, RTM drift rejection, active-vault body reads, or source mutation outside exact approved allowlists unless a later separate execution approval explicitly grants it.

**Goal:** Define and fixture-test the future `blk-link` hash-only metadata path so RTM work can reason about canonical hashes without reading protected BLK-req bodies or generating RTM ledgers.
**BLK-024 track:** Track H — BLK-link offline RTM ledger / maturity level L1 fixture-only with L0 doctrine-boundary update and persistent doctrine gates.
**Architecture:** This sprint does not implement RTM generation. It creates a deterministic local fixture contract that accepts already-supplied BEO publication-candidate metadata and already-supplied hash-only active-vault metadata, validates canonical hash shape and authority flags, preserves non-generation, and records future comparison inputs without computing coverage, making drift decisions, reading protected bodies, or publishing BEOs.
**Tech Stack:** Markdown doctrine/review docs, Python fixture helper, Python `unittest` gates, Git CLI.
**Authority boundary:** Fixture-only and doctrine-only. This plan does not authorize authoritative BEO publication, runtime `PUBLISHED` BEO output, RTM generation, RTM IDs, coverage matrices, active-vault hash comparison as runtime authority, RTM drift rejection authority, protected BLK-req vault body reads/copying/parsing/hashing/mutation, live BLK-test MCP, new live smoke runs, public ledger mutation, signer/storage/rollback authority, or source mutation outside exact approved allowlists.

---

## 0. Current Known State

Planning preflight captured before drafting this plan:

```text
date -Iseconds              -> 2026-05-08T07:35:13+10:00
git status --short --branch -> ## main...origin/main
HEAD                        -> 0691d4e docs: close blk-system sprint 023 beo candidate fixtures
```

Next-ID discovery:

```text
Latest sprint plan/outcome: BLK-SYSTEM-023
No existing docs/plans/blk-system-024* file was found during discovery.
No existing BLK-SYSTEM-024 outcome file was found during discovery.
Latest active BLK doc: docs/BLK-026_beo-publication-candidate-fixture-boundary.md
Selected sprint ID: BLK-SYSTEM-024
Selected new boundary doc: docs/BLK-027_rtm-hash-only-metadata-path-boundary.md
```

BLK-024 Track H source:

- RTM generation approval remains separate from execution, BLK-test, and BEO publication approval.
- Hash-only active-vault metadata must be defined through an approved backend path.
- Future coverage matrices may use published BEO metadata and canonical active-vault hashes only, not protected requirement bodies.
- Coverage states such as traced, missing, stale, malformed, superseded, unknown, and rejected remain future RTM semantics.
- RTM drift rejection is a later authority beyond basic ledger generation.

Sprint 023 closeout recommends this Track H work as the first follow-up candidate and preserves BEO publication candidate fixtures as non-published inputs only.

---

## 1. Scope and Non-Goals

### In scope

1. Create a bounded inventory of current RTM/BEO candidate doctrine and code surfaces before implementation.
2. Add RED tests for a missing RTM hash-only metadata path fixture helper and boundary document.
3. Implement deterministic fixture-only metadata path construction and rejection rules.
4. Create `docs/BLK-027_rtm-hash-only-metadata-path-boundary.md` as the active fixture-boundary contract.
5. Add persistent doctrine gates to prevent future edits from converting the fixture into RTM generation, drift rejection, protected-body reads, or publication authority.
6. Create hostile review, task outcomes, and sprint closeout.

### Non-goals

This sprint must not implement or authorize:

- RTM generation, RTM IDs, RTM ledgers, coverage matrices, coverage claims, drift events, drift decisions, or drift rejection authority;
- runtime active-vault hash comparison authority;
- protected BLK-req vault body reads, copying, parsing, hashing, summarizing, comparing, mutation, or exposure under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`;
- authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material, storage writers, public ledger mutation, rollback/revocation/supersession execution;
- production BLK-test MCP, new live BLK-test smoke, arbitrary shell as BLK-test behavior, or BLK-test source mutation;
- treating BEO publication-candidate fixtures as published BEOs or treating execution/BLK-test/BEO publication approval as RTM approval.

---

## 2. BLK-001 through BLK-006 Alignment Matrix

| Governing doc | Required boundary | Sprint 024 treatment |
| --- | --- | --- |
| BLK-001 — Master Architecture | Preserve strict separation between `blk-req`, Hermes planning/audit, BLK-pipe mutation, BLK-test evidence, BEO handling, and `blk-link` trace closure. | Adds only a local hash-metadata path fixture for future `blk-link`; no RTM ledger, publication, protected-body access, or source-mutation authority is added. |
| BLK-002 — Artifact Lifecycle | Active requirements/use cases remain protected by staging, linting, HITL approval, canonical hashing, and immutable baselines. | Fixture code consumes supplied hash-only metadata records only. It does not read, hash, parse, compare, expose, or mutate active-vault bodies. |
| BLK-003 — Orchestration Protocol | Target BLK-test/BEO/RTM language must not override current disabled/draft-only boundaries. | RTM approval stays separate. Fixture outputs remain `rtm_status: "NOT_GENERATED"` and cannot inherit execution, BLK-test, or BEO approval. |
| BLK-004 — BLK-pipe V47 Suite | BLK-pipe remains deterministic authority for bounded mutation, validation, cleanup, reports, and exact-path staging. | Sprint changes are limited to exact docs/Python allowlists. No BLK-pipe execution or validation-profile authority changes are in scope. |
| BLK-005 — BLK-Req Specification | BEOs and future RTMs bind to canonical artifact hashes; drift rejection is target-state until explicitly authorized. | Fixture records canonical hash metadata and future-state vocabulary without making coverage or drift decisions. |
| BLK-006 — BLK-Req Implementation Brief | Protected-vault hard-deny, staged revisions, and HITL authorization remain BLK-req/backend authority. | Fixture code rejects body-bearing records and active-vault read flags; it does not implement a backend active-vault reader. |

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
5. Write `docs/outcomes/BLK-SYSTEM-024_task-00N-outcome.md` recording objective, files, RED/GREEN evidence, verification, exact staged paths, and non-execution statement.
6. Stage exact paths only. Do not use `git add .`, `git add -u`, broad globs, stash, reset, checkout, or broad pathspecs to manage sprint files.
7. Commit and push to `origin/main` after each task commit.

---

## 4. Task 0 — Commit Sprint Plan

**Objective:** Preserve this sprint plan as an in-repo executable contract before implementation begins.

**Files:**

- Create: `docs/plans/blk-system-024_rtm-hash-only-metadata-path-fixture.md`
- Create: `docs/outcomes/BLK-SYSTEM-024_task-000-outcome.md`

**Verification:**

```bash
git diff --check -- docs/plans/blk-system-024_rtm-hash-only-metadata-path-fixture.md docs/outcomes/BLK-SYSTEM-024_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
fence = chr(96) * 3
for path in [Path('docs/plans/blk-system-024_rtm-hash-only-metadata-path-fixture.md'), Path('docs/outcomes/BLK-SYSTEM-024_task-000-outcome.md')]:
    text = path.read_text()
    assert text.count(fence) % 2 == 0, path
PY
```

**Commit message:** `docs: plan blk-system sprint 024 rtm hash metadata`

---

## 5. Task 1 — Inventory RTM Hash-Only Metadata Inputs

**Objective:** Produce a bounded inventory of current RTM design, BEO publication candidate fixtures, protected-vault exclusions, and future hash-only metadata prerequisites.

**Files:**

- Create: `docs/outcomes/BLK-SYSTEM-024_task-001-outcome.md`

**Required source inventory:**

- `docs/BLK-023_offline-rtm-ledger-design-boundary.md`
- `docs/BLK-024_blk-system-development-roadmap.md`
- `docs/BLK-026_beo-publication-candidate-fixture-boundary.md`
- `docs/outcomes/BLK-SYSTEM-023_sprint-closeout.md`
- `python/beo_publication_candidate_fixtures.py`
- `python/test_beo_publication_candidate_fixtures.py`
- `python/beo_rtm_interface_fixtures.py`
- `python/test_rtm_ledger_design_gates.py`
- `python/test_active_doctrine_review_gates.py`

**Acceptance criteria:**

- Inventory distinguishes BEO publication candidate fixtures from published BEOs.
- Inventory names the exact fields allowed in supplied hash-only metadata records: `kind`, `id`, `version_hash`, `metadata_source`, `body_included`, `body_read`.
- Inventory records forbidden body-bearing fields and forbidden RTM authority fields.
- No implementation files are changed in this task.

**Verification commands:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  python.test_beo_publication_candidate_fixtures \
  python.test_beo_rtm_interface_fixtures \
  python.test_rtm_ledger_design_gates \
  python.test_active_doctrine_review_gates -v
git diff --check -- docs/outcomes/BLK-SYSTEM-024_task-001-outcome.md
```

**Commit message:** `docs: inventory rtm hash metadata path inputs`

---

## 6. Task 2 — Add RTM Hash-Only Metadata Path Fixture

**Objective:** Add a deterministic local fixture helper and boundary document proving the hash-only metadata path shape without generating RTM, computing coverage, deciding drift, publishing BEOs, or reading protected bodies.

**Files:**

- Create: `python/test_rtm_hash_only_metadata_path_fixtures.py`
- Create: `python/rtm_hash_only_metadata_path_fixtures.py`
- Create: `docs/BLK-027_rtm-hash-only-metadata-path-boundary.md`
- Create: `docs/outcomes/BLK-SYSTEM-024_task-002-outcome.md`

**Required RED tests before implementation:**

- happy-path fixture preserves BEO candidate identity, canonical trace artifacts, supplied hash-only metadata, and no-authority booleans;
- FAIL candidate evidence stays non-success and still does not generate RTM;
- malformed trace hashes, malformed metadata hashes, missing IDs, body-bearing metadata, active-vault read flags, publication authority, RTM authority fields, non-candidate BEO states, and bad RTM approval fixtures fail closed;
- implementation performs no protected-vault file reads and imports no live transport/storage/network/process modules.

**Acceptance criteria:**

- The helper exports `build_rtm_hash_only_metadata_path_fixture(...)`.
- Output uses `path_status: "RTM_HASH_METADATA_PATH_FIXTURE_ONLY"` and `rtm_status: "NOT_GENERATED"`.
- Output sets `active_vault_read`, `protected_body_read`, `rtm_created`, `matrix_created`, and `drift_decision_made` to `False`.
- Output carries only supplied hash metadata and records `comparison_state: "NOT_EVALUATED_FIXTURE_ONLY"`.
- BLK-027 clearly states L1 fixture-only authority and future-approval stop conditions.

**Verification commands:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_rtm_hash_only_metadata_path_fixtures -v
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
```

**Commit message:** `feat: add rtm hash metadata path fixtures`

---

## 7. Task 3 — Add Persistent Doctrine Gate and Close Sprint

**Objective:** Add an active doctrine gate for BLK-027, run hostile review, remediate any blockers, and close the sprint.

**Files:**

- Modify: `python/test_active_doctrine_review_gates.py`
- Create: `docs/reviews/BLK-SYSTEM-024_rtm-hash-only-metadata-path-review.md`
- Create: `docs/outcomes/BLK-SYSTEM-024_task-003-outcome.md`
- Create: `docs/outcomes/BLK-SYSTEM-024_sprint-closeout.md`

**Acceptance criteria:**

- Active doctrine gate requires BLK-027 fixture-only/no-RTM/no-drift/no-protected-body/no-publication markers.
- Active doctrine gate scans `python/rtm_hash_only_metadata_path_fixtures.py` for forbidden live dependency and authority markers.
- Hostile review returns PASS or records finding IDs and remediations before closeout.
- Final verification passes.
- Every sprint task has an outcome document.

**Final verification commands:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_rtm_hash_only_metadata_path_fixtures -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
git status --short --branch
```

**Commit message:** `docs: close blk-system sprint 024 rtm hash metadata`

---

## 8. Non-Execution Statement

BLK-SYSTEM-024 does not authorize Hindsight use, Codex use, live tactical LLM execution, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, replay of BLK-SYSTEM-014/BLK-020 smoke, arbitrary shell as BLK-test behavior, source mutation by BLK-test, protected BLK-req vault body reads/copying/parsing/hashing/mutation, authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, RTM generation, RTM drift rejection authority, runtime active-vault hash comparison, coverage matrices, production sandbox/cgroup/VM/network/host-secret isolation claims, or source mutation outside exact approved allowlists.

---

## 9. Completion Thesis

BLK-SYSTEM-024 is complete only when BLK-System has a reviewed, tested, fixture-only path for carrying hash-only metadata toward future `blk-link` work, while RTM generation and protected-vault access remain physically absent and doctrinally denied.
