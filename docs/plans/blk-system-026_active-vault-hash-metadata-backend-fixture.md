# BLK-SYSTEM-026 — Active-Vault Hash Metadata Backend Fixture Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and local hostile review gates when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable. Execute task-by-task with deterministic evidence, exact-path staging, per-task outcome docs, hostile review, and push after each task. Do not use Hindsight unless explicitly requested. Do not run Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke, authoritative BEO publication, RTM generation, runtime active-vault comparison, protected BLK-req vault body reads, or source mutation outside exact approved allowlists unless a later separate execution approval explicitly grants it.

**Goal:** Define and fixture-test a hash-only active-vault metadata backend boundary so future RTM work can consume approved hash metadata without reading protected requirement/use-case bodies or generating RTM now.
**BLK-024 track:** Track B — BLK-req legislative gateway and Track H — BLK-link offline RTM ledger / maturity level L1 fixture-only with L0 doctrine-boundary update and persistent doctrine gates.
**Architecture:** This sprint does not scan `docs/active/`, does not parse protected artifacts, does not generate RTM, and does not compare hashes as runtime authority. It creates a deterministic local fixture contract that consumes already-supplied backend manifest records, validates canonical identity, version hash, approval, and no-body/no-side-effect flags, and emits `ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY` records suitable for the BLK-027 hash-metadata path.
**Tech Stack:** Markdown doctrine/review docs, Python fixture helper, Python `unittest` gates, Git CLI.
**Authority boundary:** Fixture-only and doctrine-only. This plan does not authorize protected BLK-req vault body reads/copying/parsing/hashing/mutation, active-vault filesystem scanning, runtime active-vault hash comparison, RTM generation, RTM IDs, coverage matrices, drift decisions, RTM drift rejection authority, authoritative BEO publication, runtime `PUBLISHED` BEO output, signer/storage/ledger/rollback side effects, live BLK-test MCP, new live smoke runs, or source mutation outside exact approved allowlists.

---

## 0. Current Known State

Planning preflight captured before drafting this plan:

```text
date -Iseconds              -> 2026-05-08T08:38:31+10:00
git status --short --branch -> ## main...origin/main
HEAD                        -> 62def84 docs: close blk-system sprint 025 published beo input
```

Next-ID discovery:

```text
Latest sprint plan/outcome: BLK-SYSTEM-025
No existing docs/plans/blk-system-026* file was found during discovery.
No existing BLK-SYSTEM-026 outcome file was found during discovery.
Latest active BLK doc: docs/BLK-028_published-beo-input-boundary.md
Selected sprint ID: BLK-SYSTEM-026
Selected new boundary doc: docs/BLK-029_active-vault-hash-metadata-backend-boundary.md
```

Selection rationale:

- BLK-SYSTEM-025 closeout recommends hash-only active-vault backend design as the safe follow-up before any RTM generation proposal.
- BLK-027 and BLK-028 both state that future RTM generation requires an approved backend hash-only active-vault metadata path.
- This sprint chooses the safest fixture/backend-boundary rung and keeps RTM generation, coverage, drift rejection, and protected-body access disabled.

---

## 1. Scope and Non-Goals

### In scope

1. Inventory current BLK-req canonical hash doctrine, BLK-027 hash metadata fixtures, BLK-028 published-BEO input boundary, and protected-vault exclusions.
2. Add RED tests for a missing active-vault hash metadata backend fixture helper and BLK-029 boundary document.
3. Implement deterministic fixture-only backend metadata construction from already-supplied manifest entries.
4. Create `docs/BLK-029_active-vault-hash-metadata-backend-boundary.md` as the active fixture-boundary contract.
5. Add persistent doctrine gates to prevent future edits from converting the backend fixture into protected-body access, active-vault scanning, RTM generation, coverage, drift rejection, or publication authority.
6. Create hostile review, task outcomes, and sprint closeout.

### Non-goals

This sprint must not implement or authorize:

- protected BLK-req vault body reads, copying, parsing, hashing, summarizing, comparing, mutation, or exposure under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`;
- active-vault filesystem scanning, backend promotion, staged revision, or live metadata export from protected paths;
- runtime active-vault hash comparison authority;
- RTM generation, RTM IDs, RTM ledgers, coverage matrices, coverage claims, drift events, drift decisions, or RTM drift rejection authority;
- authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material, cryptographic signing, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution;
- production BLK-test MCP, new live BLK-test smoke, arbitrary shell as BLK-test behavior, or BLK-test source mutation.

---

## 2. BLK-001 through BLK-006 Alignment Matrix

| Governing doc | Required boundary | Sprint 026 treatment |
| --- | --- | --- |
| BLK-001 — Master Architecture | Preserve strict separation between `blk-req`, Hermes planning/audit, BLK-pipe mutation, BLK-test evidence, BEO handling, and `blk-link` trace closure. | Adds only a local hash metadata backend fixture for future `blk-link`; no RTM ledger, protected-body access, publication, or source-mutation authority is added. |
| BLK-002 — Artifact Lifecycle | Active requirements/use cases remain protected by staging, linting, HITL approval, canonical hashing, and immutable baselines. | Fixture code consumes supplied manifest metadata only. It does not read, hash, parse, compare, expose, or mutate active-vault bodies. |
| BLK-003 — Orchestration Protocol | Target RTM and traceability language must not override current disabled/draft-only boundaries. | Backend metadata approval stays fixture-only. RTM approval remains separate. The fixture cannot inherit execution, BLK-test, BEO-publication, Codex, or RTM approval. |
| BLK-004 — BLK-pipe V47 Suite | BLK-pipe remains deterministic authority for bounded mutation, validation, cleanup, reports, and exact-path staging. | Sprint changes are limited to exact docs/Python allowlists. No BLK-pipe execution or validation-profile authority changes are in scope. |
| BLK-005 — BLK-Req Specification | BEOs and future RTMs bind to canonical artifact hashes; drift rejection is target-state until explicitly authorized. | Fixture preserves canonical `version_hash` metadata and explicitly refuses coverage/drift decisions. |
| BLK-006 — BLK-Req Implementation Brief | Protected-vault hard-deny, staged revisions, and HITL authorization remain BLK-req/backend authority. | Fixture code rejects active-vault path inputs, body-bearing fields, and promotion/revision authority fields. It does not implement a backend active-vault reader. |

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
5. Write `docs/outcomes/BLK-SYSTEM-026_task-00N-outcome.md` recording objective, files, RED/GREEN evidence, verification, exact staged paths, and non-execution statement.
6. Stage exact paths only. Do not use `git add .`, `git add -u`, broad globs, stash, reset, checkout, or broad pathspecs to manage sprint files.
7. Commit and push to `origin/main` after each task commit.

---

## 4. Task 0 — Commit Sprint Plan

**Objective:** Preserve this sprint plan as an in-repo executable contract before implementation begins.

**Files:**

- Create: `docs/plans/blk-system-026_active-vault-hash-metadata-backend-fixture.md`
- Create: `docs/outcomes/BLK-SYSTEM-026_task-000-outcome.md`

**Verification:**

```bash
git diff --check -- docs/plans/blk-system-026_active-vault-hash-metadata-backend-fixture.md docs/outcomes/BLK-SYSTEM-026_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
fence = chr(96) * 3
for path in [Path('docs/plans/blk-system-026_active-vault-hash-metadata-backend-fixture.md'), Path('docs/outcomes/BLK-SYSTEM-026_task-000-outcome.md')]:
    text = path.read_text()
    assert text.count(fence) % 2 == 0, path
PY
```

**Commit message:** `docs: plan blk-system sprint 026 active vault hash backend`

---

## 5. Task 1 — Inventory Hash Metadata Backend Prerequisites

**Objective:** Produce a bounded inventory of current BLK-req hash doctrine, fixture metadata records, published-BEO input prerequisites, and protected-vault exclusions.

**Files:**

- Create: `docs/outcomes/BLK-SYSTEM-026_task-001-outcome.md`

**Required source inventory:**

- `docs/BLK-002_blk-req-artifact-lifecycle.md`
- `docs/BLK-005_blk-req-specification.md`
- `docs/BLK-006_blk-req-implementation-brief.md`
- `docs/BLK-024_blk-system-development-roadmap.md`
- `docs/BLK-027_rtm-hash-only-metadata-path-boundary.md`
- `docs/BLK-028_published-beo-input-boundary.md`
- `docs/outcomes/BLK-SYSTEM-024_sprint-closeout.md`
- `docs/outcomes/BLK-SYSTEM-025_sprint-closeout.md`
- `python/rtm_hash_only_metadata_path_fixtures.py`
- `python/test_rtm_hash_only_metadata_path_fixtures.py`
- `python/test_active_doctrine_review_gates.py`

**Acceptance criteria:**

- Inventory distinguishes supplied hash metadata records from live active-vault readers/scanners.
- Inventory names exact manifest fields required for `ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY`.
- Inventory records forbidden active-vault path fields, body-bearing fields, promotion/revision fields, RTM authority fields, publication fields, and side-effect flags.
- No implementation files are changed in this task.

**Verification commands:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest   python.test_rtm_hash_only_metadata_path_fixtures   python.test_active_doctrine_review_gates -v
git diff --check -- docs/outcomes/BLK-SYSTEM-026_task-001-outcome.md
```

**Commit message:** `docs: inventory active vault hash backend prerequisites`

---

## 6. Task 2 — Add Active-Vault Hash Metadata Backend Fixture

**Objective:** Add a deterministic local fixture helper and boundary document proving backend hash metadata export shape without active-vault scanning, protected-body reads, RTM generation, coverage, drift decisions, or publication.

**Files:**

- Create: `python/test_active_vault_hash_metadata_backend_fixtures.py`
- Create: `python/active_vault_hash_metadata_backend_fixtures.py`
- Create: `docs/BLK-029_active-vault-hash-metadata-backend-boundary.md`
- Create: `docs/outcomes/BLK-SYSTEM-026_task-002-outcome.md`

**Required RED tests before implementation:**

- happy-path fixture preserves manifest identity, artifact kind/id/version_hash, backend approval identity, and no-side-effect booleans;
- output records use `metadata_source: "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY"` and `downstream_metadata_source: "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY"`;
- malformed hashes, missing IDs, active-vault/protected path fields, body-bearing fields, promotion/revision authority fields, RTM authority fields, publication authority fields, side-effect flags, stale/replayed/expired approval, and non-string identity values fail closed;
- implementation performs no protected-vault file reads and imports no live transport/storage/network/process modules.

**Acceptance criteria:**

- The helper exports `build_active_vault_hash_metadata_backend_fixture(...)`.
- Output uses `backend_status: "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY"` and `rtm_status: "NOT_GENERATED"`.
- Output sets `active_vault_scanned`, `active_vault_read`, `protected_body_read`, `body_copied`, `body_hashed`, `rtm_created`, `matrix_created`, `drift_decision_made`, `publication_performed`, and `source_mutated` to `False`.
- Output carries only supplied manifest metadata and records fixture-only backend approval.
- BLK-029 clearly states L1 fixture-only authority and future-approval stop conditions.

**Verification commands:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_vault_hash_metadata_backend_fixtures -v
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
```

**Commit message:** `feat: add active vault hash metadata backend fixtures`

---

## 7. Task 3 — Add Persistent Doctrine Gate and Close Sprint

**Objective:** Add an active doctrine gate for BLK-029, run hostile review, remediate any blockers, and close the sprint.

**Files:**

- Modify: `python/test_active_doctrine_review_gates.py`
- Create: `docs/reviews/BLK-SYSTEM-026_active-vault-hash-metadata-backend-review.md`
- Create: `docs/outcomes/BLK-SYSTEM-026_task-003-outcome.md`
- Create: `docs/outcomes/BLK-SYSTEM-026_sprint-closeout.md`

**Acceptance criteria:**

- Active doctrine gate requires BLK-029 fixture-only/no-active-vault-scan/no-protected-body/no-RTM/no-drift/no-publication markers.
- Active doctrine gate scans `python/active_vault_hash_metadata_backend_fixtures.py` for forbidden live dependency and authority markers.
- Hostile review returns PASS or records finding IDs and remediations before closeout.
- Final verification passes.
- Every sprint task has an outcome document.

**Final verification commands:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_vault_hash_metadata_backend_fixtures -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
git status --short --branch
```

**Commit message:** `docs: close blk-system sprint 026 active vault hash backend`

---

## 8. Final Acceptance Criteria

The sprint is complete when:

- `docs/plans/blk-system-026_active-vault-hash-metadata-backend-fixture.md` is committed and pushed.
- Every task has an outcome doc under `docs/outcomes/`.
- `python/active_vault_hash_metadata_backend_fixtures.py` and tests exist and pass.
- `docs/BLK-029_active-vault-hash-metadata-backend-boundary.md` exists and states the fixture-only, no-active-vault-scan, no-RTM, no-protected-body boundary.
- `python/test_active_doctrine_review_gates.py` pins the BLK-029 boundary.
- Hostile review exists and any blockers are remediated.
- Full Go/Python verification passes.
- Final closeout is committed and pushed to `origin/main`.
