# BLK-SYSTEM-023 — BEO Publication Candidate Fixture Bridge Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `requesting-code-review` when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable. Execute task-by-task with deterministic evidence, exact-path staging, per-task outcome docs, hostile review, and push after each task. Do not use Hindsight unless explicitly requested. Do not run Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke, authoritative BEO publication, RTM generation, signer key material, storage writers, public ledger writers, rollback executors, or active-vault body reads unless a separate execution approval explicitly grants it.

**Goal:** Move BEO publication from prose-only design toward deterministic publication-candidate fixtures while preserving draft-only runtime and denying actual publication authority.
**BLK-024 track:** Track G — BEO publication path / maturity level L1 fixture-only, with L0 doctrine-boundary updates and persistent doctrine-gate tests.
**Architecture:** Current BEO projection remains `DRAFT_ONLY`; this sprint may create local candidate fixtures that prove the publication envelope shape, approval binding, hash binding, signer/storage/ledger/rollback metadata, and rejection rules without publishing anything. BLK-pipe execution success, BLK-test evidence, draft BEO projection, codex-live approval, BLK-test approval, and RTM approval are all separate from BEO publication approval. RTM generation remains separate and disabled.
**Tech Stack:** Markdown doctrine/review docs, Python fixture helpers, Python `unittest` gates, Git CLI.
**Authority boundary:** Fixture-only and doctrine-only. This plan does not authorize authoritative BEO publication, runtime `PUBLISHED` BEO output, signer key use, immutable storage writes, public ledger mutation, rollback/revocation execution, RTM generation, RTM drift rejection authority, production BLK-test MCP, new live BLK-test smoke, protected BLK-req vault body reads/copying/parsing/hashing/mutation, or source mutation outside exact approved allowlists.

---

## 0. Current Known State

Planning preflight captured before drafting this plan:

```text
date -Iseconds              -> 2026-05-08T06:51:09+10:00
git status --short --branch -> ## main...origin/main
HEAD                        -> c10f25f docs: close blk-system sprint 022 blk-test readiness
```

Relevant existing sprint/document state:

```text
docs/BLK-024_blk-system-development-roadmap.md
docs/plans/blk-system-022_blk-test-pilot-readiness-design-review.md
docs/outcomes/BLK-SYSTEM-022_sprint-closeout.md
docs/reviews/BLK-SYSTEM-022_blk-test-pilot-readiness-design-review.md
docs/BLK-014_blk-execution-outcome-fixture-shape.md
docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md
docs/BLK-021_beo-draft-publication-gate-review.md
docs/BLK-022_authoritative-beo-publication-design-boundary.md
docs/BLK-023_offline-rtm-ledger-design-boundary.md
docs/BLK-025_blk-test-pilot-readiness-boundary.md
python/beo_fixture_projection.py
python/test_beo_fixture_projection.py
python/test_beo_publication_design_gates.py
python/test_active_doctrine_review_gates.py
```

Next-ID discovery:

```text
No existing docs/plans/blk-system-023* file was found.
No existing BLK-SYSTEM-023 outcome file was found.
BLK-SYSTEM-022 closeout lists BEO publication implementation design-to-fixture bridge as the first recommended follow-up.
BLK-024 near-term direction item 4 is BEO publication implementation design-to-fixture bridge.
Selected sprint ID: BLK-SYSTEM-023
Selected plan path: docs/plans/blk-system-023_beo-publication-candidate-fixture-bridge.md
```

BLK-024 Track G source:

- Track G says current BEO outputs must preserve `beo_publication: "DRAFT_ONLY"` and `rtm_status: "NOT_GENERATED"`.
- Track G asks for a publication candidate schema with canonical BEO hash, source evidence identity, BLK-pipe report identity, BLK-test evidence identity, and trace artifacts.
- Track G requires publication-specific human approval that cannot be inherited from execution, BLK-test, draft BEO projection, or RTM approval.
- Track G requires signer identity, key-handling, immutable storage, public ledger append rules, rollback, revocation, and supersession rules.
- Track G rejects publishing success from BLOCKED, fatal, transport-error, interrupted, missing, malformed, stale, or unknown evidence.
- Track G keeps RTM generation separate from publication.

Current BEO/RTM boundary observed during planning:

- BLK-014 defines deterministic draft BEO fixture shape only. It preserves opaque `trace_artifacts` and forces `beo_publication: "DRAFT_ONLY"` plus `rtm_status: "NOT_GENERATED"`.
- BLK-016 defines disabled BLK-test MCP adapter smoke and BEO/RTM interface fixtures only. It does not authorize authoritative BEO publication, RTM generation, live BLK-test MCP, or protected-vault reads.
- BLK-021 records draft-only BEO publication gate review for BLK-020 first-smoke evidence. It rejects publication authority fields and RTM authority fields.
- BLK-022 records authoritative BEO publication as design-only. It requires publication-specific approval and a later implementation sprint before any publisher, signer, storage writer, ledger writer, or rollback executor exists.
- BLK-023 keeps RTM design separate and disabled.
- BLK-025 explicitly separates BEO publication implementation from BLK-test pilot, synthetic-smoke expansion, RTM hash-only metadata path, and production BLK-test MCP.

---

## 1. Scope and Non-Goals

### In scope

1. Inventory current BEO doctrine, code, tests, and review handoffs before writing new fixture logic.
2. Add RED tests for a missing BEO publication candidate fixture helper and boundary document.
3. Implement deterministic fixture-only candidate construction, validation, and rejection rules.
4. Create `docs/BLK-026_beo-publication-candidate-fixture-boundary.md` as the new active fixture-boundary contract for publication candidates.
5. Add persistent doctrine gates so future edits cannot silently convert candidate fixtures into real publication authority.
6. Create a hostile review and closeout with explicit finding IDs, remediation, and residual next-sprint split.

### Non-goals

This sprint must not implement or authorize:

- authoritative BEO publication;
- runtime `beo_publication: "PUBLISHED"` output;
- live publication approval capture through Discord or any other IdP;
- real signer key material access, cryptographic signing, KMS integration, secret reads, or host-key reads;
- immutable storage writes, public ledger mutation, rollback execution, revocation execution, or supersession execution;
- RTM generation, RTM IDs, coverage matrices, active-vault hash comparison, RTM drift rejection, or drift decisions;
- production BLK-test MCP, new live BLK-test smoke runs, replay of BLK-SYSTEM-014/BLK-020 smoke, or BLK-test authority expansion;
- protected BLK-req vault body reads, copying, parsing, hashing, mutation, or drift comparison;
- treating BLK-pipe execution success, BLK-test PASS, draft BEO projection, codex-live approval, BLK-test approval, or RTM approval as BEO publication approval;
- projecting BLOCKED, fatal, transport-error, interrupted, missing, malformed, stale, unknown, replayed, expired, or mismatched evidence into published success.

---

## 2. BLK-001 through BLK-006 Alignment Matrix

| Governing doc | Required boundary | Sprint 023 treatment |
| --- | --- | --- |
| BLK-001 — Master Architecture | Preserve strict separation between BLK-req laws, Hermes planning/audit, BLK-pipe source mutation, BLK-test evidence, BEO handling, and blk-link trace closure. | Adds only fixture candidate packaging after draft BEO evidence. No publication, RTM, protected-vault, or source-mutation authority is added. |
| BLK-002 — Artifact Lifecycle | Requirements/use-case baselines stay protected behind staging, linting, HITL approval, canonical hashing, and active-vault immutability. | Candidate fixtures may carry opaque `trace_artifacts[*].version_hash` metadata only. They must not read, hash, parse, compare, or expose protected bodies. |
| BLK-003 — Orchestration Protocol | Target BEO/RTM language must not override current disabled/draft-only boundaries. Human dispatch, hostile audit, failure ceiling, and current BLK-test/BEO/RTM disabled boundaries remain separate. | Publication candidate construction is local fixture work only. It cannot inherit execution or BLK-test approval and cannot produce RTM. |
| BLK-004 — BLK-pipe V47 Suite | BLK-pipe remains deterministic authority for bounded source mutation, validation, cleanup, Git staging, reports, and revert. | This sprint may add Python fixture code/tests/docs by exact allowlist only. It must not modify BLK-pipe execution authority or validation profile semantics unless a blocker is found and explicitly justified. |
| BLK-005 — BLK-Req Specification | BEOs bind to canonical artifact hashes; drift rejection is target-state until authorized RTM/blk-link implementation exists. | Candidate fixtures preserve canonical hashes as opaque metadata and must not claim drift rejection, coverage, or active-vault truth. |
| BLK-006 — BLK-Req Implementation Brief | Protected vault hard-deny, staged revisions, and Discord/HITL authorization remain BLK-req/backend authority. | Candidate fixture code must deny protected-vault body access and must not implement live publication approval capture. |

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

- Create: `docs/plans/blk-system-023_beo-publication-candidate-fixture-bridge.md`
- Create: `docs/outcomes/BLK-SYSTEM-023_task-000-outcome.md`

**Steps:**

1. Verify the plan exists and contains required authority markers:
   ```bash
   test -f docs/plans/blk-system-023_beo-publication-candidate-fixture-bridge.md
   grep -F "Track G — BEO publication path" docs/plans/blk-system-023_beo-publication-candidate-fixture-bridge.md
   grep -F "does not authorize authoritative BEO publication" docs/plans/blk-system-023_beo-publication-candidate-fixture-bridge.md
   grep -F "does not authorize RTM generation" docs/plans/blk-system-023_beo-publication-candidate-fixture-bridge.md
   grep -F "protected BLK-req vault body reads" docs/plans/blk-system-023_beo-publication-candidate-fixture-bridge.md
   git diff --check -- docs/plans/blk-system-023_beo-publication-candidate-fixture-bridge.md
   ```
2. Create `docs/outcomes/BLK-SYSTEM-023_task-000-outcome.md` recording:
   - plan path;
   - BLK-024 Track G source;
   - current preflight status;
   - no implementation change;
   - non-execution statement.
3. Run plan-only verification:
   ```bash
   git diff --check -- docs/plans/blk-system-023_beo-publication-candidate-fixture-bridge.md docs/outcomes/BLK-SYSTEM-023_task-000-outcome.md
   python3 - <<'PY'
   from pathlib import Path
   for path in [Path('docs/plans/blk-system-023_beo-publication-candidate-fixture-bridge.md'), Path('docs/outcomes/BLK-SYSTEM-023_task-000-outcome.md')]:
       text = path.read_text()
       fence = chr(96) * 3
       assert text.count(fence) % 2 == 0, path
   PY
   ```
4. Stage exact files:
   ```bash
   git add docs/plans/blk-system-023_beo-publication-candidate-fixture-bridge.md \
           docs/outcomes/BLK-SYSTEM-023_task-000-outcome.md
   git diff --cached --name-only
   ```
5. Commit and push:
   ```bash
   git commit -m "docs: plan blk-system sprint 023 beo candidate fixtures"
   git push origin main
   ```

---

## 5. Task 1 — Inventory BEO Publication Candidate Inputs

**Objective:** Produce a bounded inventory of current draft BEO fixtures, BEO publication design boundaries, RTM exclusions, and candidate-field prerequisites before writing fixture logic.

**Files:**

- Create: `docs/outcomes/BLK-SYSTEM-023_task-001-outcome.md`

**Required source inventory:**

1. Read and summarize:
   - `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
   - `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`
   - `docs/BLK-021_beo-draft-publication-gate-review.md`
   - `docs/BLK-022_authoritative-beo-publication-design-boundary.md`
   - `docs/BLK-023_offline-rtm-ledger-design-boundary.md`
   - `docs/BLK-024_blk-system-development-roadmap.md`
   - `docs/BLK-025_blk-test-pilot-readiness-boundary.md`
2. Inspect implementation/test surfaces:
   - `python/beo_fixture_projection.py`
   - `python/test_beo_fixture_projection.py`
   - `python/beo_rtm_interface_fixtures.py`
   - `python/test_beo_rtm_interface_fixtures.py`
   - `python/test_beo_publication_design_gates.py`
   - `python/test_active_doctrine_review_gates.py`
3. Record an inventory table with at least these rows:
   - draft BEO source shape;
   - accepted PASS/FAIL statuses;
   - BLOCKED/fatal/transport/interrupted/unknown rejection;
   - canonical BEO hash gap;
   - publication-specific approval fixture gap;
   - signer identity/key-handling fixture gap;
   - immutable storage fixture gap;
   - public ledger fixture gap;
   - rollback/revocation/supersession fixture gap;
   - RTM/protected-vault exclusion.
4. Identify exact paths that the later tasks may modify. Do not implement candidate fixtures in Task 1.

**Verification commands:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  python.test_beo_fixture_projection \
  python.test_beo_rtm_interface_fixtures \
  python.test_beo_publication_design_gates \
  python.test_active_doctrine_review_gates -v
git diff --check -- docs/outcomes/BLK-SYSTEM-023_task-001-outcome.md
```

**Acceptance criteria:**

- The outcome doc identifies the current boundary as draft-only/design-only.
- The outcome doc names the missing candidate-fixture surfaces without granting authority.
- The outcome doc lists exact future files and explicitly excludes protected-vault reads, signer key use, ledger writes, RTM generation, and BLK-test authority expansion.

**Commit:** `docs: inventory beo publication candidate inputs`

---

## 6. Task 2 — Add RED Candidate Fixture Tests

**Objective:** Add deterministic failing tests for the BEO publication candidate fixture boundary before implementation exists.

**Files:**

- Create: `python/test_beo_publication_candidate_fixtures.py`
- Create: `docs/outcomes/BLK-SYSTEM-023_task-002-outcome.md`

**RED test requirements:**

Create tests that expect a not-yet-implemented fixture helper, provisionally named:

```python
build_beo_publication_candidate_fixture(
    draft_beo: dict[str, object],
    *,
    candidate_id: str,
    publication_approval: dict[str, object],
    signer_fixture: dict[str, object],
    storage_fixture: dict[str, object],
    ledger_fixture: dict[str, object],
    rollback_fixture: dict[str, object],
) -> dict[str, object]
```

The RED tests must assert the future helper will:

1. Accept only draft BEO fixtures whose `beo_publication` is `DRAFT_ONLY` and `rtm_status` is `NOT_GENERATED`.
2. Preserve `beo_id`, `beb_id`, `status`, `commit_hash`, `pre_engine_hash`, and exact `trace_artifacts` without reading active-vault bodies.
3. Compute or require a canonical `beo_hash` with `sha256:<64-lowercase-hex>` syntax over the supplied draft fixture only.
4. Bind publication-specific fixture approval fields:
   - `approval_record_hash`;
   - `operator_identity`;
   - `approval_scope` equal to a publication-candidate-only value;
   - `approval_timestamp` or deterministic fixture timestamp.
5. Preserve signer/storage/ledger/rollback metadata as fixture descriptors only, with explicit booleans proving no key material, storage write, ledger mutation, or rollback execution occurred.
6. Reject or fail closed on:
   - `beo_publication: "PUBLISHED"`;
   - any RTM authority field (`rtm`, `rtm_id`, `coverage_matrix`, `drift_decision`, etc.);
   - missing, malformed, stale, expired, replayed, or mismatched approval fixture hashes;
   - missing/malformed canonical hashes;
   - `active_vault_read: true`;
   - key material fields or secret-bearing signer fields;
   - storage write / ledger mutation / rollback execution booleans set true;
   - BLOCKED, fatal, transport-error, interrupted, unknown, or missing status projected as success.
7. Not import, call, or reference live signer/KMS, network, storage SDK, public ledger writer, Discord API, live BLK-test MCP, subprocess runner, or RTM generator modules.

**RED command:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_beo_publication_candidate_fixtures -v
```

Expected RED failure: import/name failure or explicit missing-helper failure only. If the focused test passes before implementation, stop and investigate stale implementation or underspecified tests.

**Shared verification after RED capture:**

```bash
git diff --check -- python/test_beo_publication_candidate_fixtures.py docs/outcomes/BLK-SYSTEM-023_task-002-outcome.md
```

**Acceptance criteria:**

- RED failure is captured in the outcome doc.
- Tests pin candidate-only, no-publication, no-RTM, no-protected-vault, and no-side-effect boundaries.
- Tests do not require real publication approval, real signing, storage, ledger mutation, rollback execution, network, or live BLK-test.

**Commit:** `test: add beo publication candidate fixture red tests`

---

## 7. Task 3 — Implement Candidate Fixture Helper and BLK-026 Boundary

**Objective:** Turn the Task 2 RED tests GREEN with minimal fixture-only implementation and document the boundary in a new active BLK doc.

**Files:**

- Create: `python/beo_publication_candidate_fixtures.py`
- Modify: `python/test_beo_publication_candidate_fixtures.py`
- Create: `docs/BLK-026_beo-publication-candidate-fixture-boundary.md`
- Create: `docs/outcomes/BLK-SYSTEM-023_task-003-outcome.md`

**Implementation requirements:**

1. Implement only deterministic local fixture helpers. Do not add live signer, storage, ledger, Discord, BLK-test, subprocess, network, or RTM dependencies.
2. Candidate output must be clearly non-published, for example:
   ```text
   candidate_status: "PUBLICATION_CANDIDATE_FIXTURE_ONLY"
   beo_publication: "DRAFT_ONLY"
   rtm_status: "NOT_GENERATED"
   published: false
   key_material_accessed: false
   immutable_storage_written: false
   public_ledger_mutated: false
   rollback_executed: false
   active_vault_read: false
   ```
3. Candidate output must include a canonical BEO hash derived from deterministic serialization of the supplied draft BEO fixture only. It must not hash protected BLK-req bodies.
4. Candidate output must bind source identities and hashes:
   - `candidate_id`;
   - `beo_id`;
   - `beo_hash`;
   - `beb_id`;
   - `commit_hash`;
   - `pre_engine_hash`;
   - exact `trace_artifacts`;
   - BLK-test/source evidence identity when present;
   - publication approval fixture hash;
   - signer/storage/ledger/rollback fixture identities.
5. Candidate output must reject prohibited statuses and authority fields without converting them to success.
6. `docs/BLK-026_beo-publication-candidate-fixture-boundary.md` must state:
   - status: `Active fixture boundary contract — not publication authority`;
   - BLK-024 Track G / L1 fixture-only maturity;
   - current runtime remains `DRAFT_ONLY` and `NOT_GENERATED`;
   - candidate fixtures are not published BEOs;
   - publication-specific approval is fixture-only and cannot be inherited;
   - signer/storage/ledger/rollback descriptors are fixture-only;
   - RTM remains separate and disabled;
   - protected-vault bodies remain unread;
   - future authoritative publication requires a separate sprint, explicit human approval, hostile review, signer/storage/ledger/rollback side-effect authority, rollback/revocation/supersession policy, and closeout.

**Focused GREEN command:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_beo_publication_candidate_fixtures -v
```

**Required broader verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  python.test_beo_fixture_projection \
  python.test_beo_rtm_interface_fixtures \
  python.test_beo_publication_design_gates \
  python.test_beo_publication_candidate_fixtures \
  python.test_active_doctrine_review_gates -v
go test ./...
go vet ./...
git diff --check
```

**Acceptance criteria:**

- Focused RED turns GREEN.
- Candidate helper is deterministic and side-effect-free.
- BLK-026 exists and preserves candidate-only/no-authority markers.
- Current draft BEO projectors still output `DRAFT_ONLY` and `NOT_GENERATED`.
- No protected BLK-req body access, RTM generation, signing, storage write, ledger mutation, rollback execution, live BLK-test, or network/model/cyber tooling is introduced.

**Commit:** `feat: add beo publication candidate fixtures`

---

## 8. Task 4 — Add Persistent Doctrine Gates for BLK-026

**Objective:** Make the candidate-only boundary persistent so future edits cannot silently promote fixture candidates into publication authority.

**Files:**

- Modify: `python/test_active_doctrine_review_gates.py`
- Modify if needed for wording only: `docs/BLK-022_authoritative-beo-publication-design-boundary.md`
- Create: `docs/outcomes/BLK-SYSTEM-023_task-004-outcome.md`

**Doctrine-gate requirements:**

Add a focused gate such as:

```text
test_sprint023_beo_publication_candidate_fixture_boundary_preserves_no_publication_authority
```

The gate must require `docs/BLK-026_beo-publication-candidate-fixture-boundary.md` to contain markers for:

- `BEO publication candidate fixture boundary`;
- `Active fixture boundary contract — not publication authority`;
- `Track G — BEO publication path`;
- `PUBLICATION_CANDIDATE_FIXTURE_ONLY`;
- `beo_publication: "DRAFT_ONLY"`;
- `rtm_status: "NOT_GENERATED"`;
- no authoritative BEO publication;
- no runtime `PUBLISHED` BEO output;
- no signer key material;
- no immutable storage writes;
- no public ledger mutation;
- no rollback, revocation, or supersession execution;
- no RTM generation;
- no RTM drift rejection authority;
- no protected BLK-req vault body reads;
- publication-specific approval cannot be inherited from execution, BLK-test, draft BEO projection, codex-live approval, or RTM approval;
- BLOCKED/fatal/transport/interrupted/unknown/missing/malformed/stale/replayed evidence cannot publish success;
- future authoritative publication requires a later explicit sprint and human approval.

If BLK-022 wording is patched, it must be a narrow forward reference to BLK-026 only. Do not weaken BLK-022's design-only boundary or imply publication authority now exists.

**Verification commands:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_beo_publication_candidate_fixtures -v
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
```

**Acceptance criteria:**

- Doctrine gate fails if BLK-026 loses candidate-only or forbidden-authority markers.
- BLK-022 remains design-only and no-authority.
- Full Python/Go verification passes.

**Commit:** `test: gate beo publication candidate boundary`

---

## 9. Task 5 — Hostile Review, Remediation, and Closeout

**Objective:** Hostile-audit the sprint, remediate any blocker, and close the sprint with exact evidence.

**Files:**

- Create: `docs/reviews/BLK-SYSTEM-023_beo-publication-candidate-fixture-review.md`
- Create: `docs/outcomes/BLK-SYSTEM-023_task-005-outcome.md`
- Create: `docs/outcomes/BLK-SYSTEM-023_sprint-closeout.md`
- Modify only if remediation demands it: files changed in Tasks 2-4

**Hostile review checklist:**

1. Verify BLK-024 Track G alignment and maturity L1 fixture-only classification.
2. Verify BLK-001 through BLK-006 authority boundaries remain intact.
3. Verify `beo_publication: "DRAFT_ONLY"` and `rtm_status: "NOT_GENERATED"` remain mandatory for runtime/current fixtures.
4. Verify candidate fixtures are not published BEOs and cannot create `PUBLISHED` runtime output.
5. Verify publication approval fixture cannot inherit from codex-live, BLK-pipe execution, BLK-test, draft BEO projection, or RTM approval.
6. Verify signer/storage/ledger/rollback descriptors are fixture-only and no side effects occur.
7. Verify RTM generation, active-vault hash comparison, drift rejection, and coverage claims remain out of scope.
8. Verify protected BLK-req vault bodies remain unread.
9. Verify BLOCKED/fatal/transport/interrupted/unknown/missing/malformed/stale/replayed evidence cannot become published success.
10. Verify no network/model/cyber/live BLK-test/Discord API/signer/KMS/storage/ledger/rollback dependencies were introduced.
11. Verify persistent doctrine gates cover BLK-026 and hostile-review remediation markers.

**Required final verification:**

```bash
export PATH="$HOME/.local/bin:$PATH"
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_beo_publication_candidate_fixtures -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
git status --short --branch
```

**Closeout requirements:**

The closeout must record:

- final commit table;
- task outcome table;
- implemented files;
- verification output summary;
- acceptance criteria status;
- non-execution statement;
- no-authority-expansion statement;
- residual next-sprint seeds.

**Commit:** `docs: close blk-system sprint 023 beo candidate fixtures`

---

## 10. Sprint-Level Acceptance Criteria

- `docs/BLK-026_beo-publication-candidate-fixture-boundary.md` exists and is explicitly fixture-only / not publication authority.
- `python/beo_publication_candidate_fixtures.py` exists and is deterministic, local, side-effect-free, and protected-vault-body-free.
- `python/test_beo_publication_candidate_fixtures.py` covers accepted candidate construction and forbidden authority/rejection cases.
- Candidate fixtures include canonical BEO hash binding, publication-specific approval fixture binding, signer/storage/ledger/rollback fixture descriptors, exact trace-artifact preservation, and explicit no-side-effect booleans.
- Candidate fixtures cannot emit runtime `PUBLISHED` BEO output.
- Existing draft BEO projection remains `DRAFT_ONLY` and `NOT_GENERATED`.
- RTM generation, RTM drift rejection, active-vault hash comparison, and coverage matrices remain disabled/out of scope.
- Protected BLK-req vault bodies remain unread.
- Persistent doctrine gates pin the BLK-026 no-authority boundary.
- Hostile review exists and any blockers are remediated.
- Every task has an outcome doc.
- Full Go/Python verification passes.

---

## 11. Non-Execution Statement

BLK-SYSTEM-023 does not authorize Hindsight use, Codex use, live tactical LLM execution, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, replay of BLK-SYSTEM-014/BLK-020 smoke, arbitrary shell as BLK-test behavior, source mutation by BLK-test, protected BLK-req vault body reads/copying/parsing/hashing/mutation, authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, real signer key material access, cryptographic signing, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, RTM generation, RTM drift rejection authority, active-vault hash comparison, coverage matrices, production sandbox/cgroup/VM/network/host-secret isolation claims, or source mutation outside exact approved allowlists.

---

## 12. Residual / Next-Sprint Seeds

Possible follow-up candidates after BLK-SYSTEM-023 closes:

1. RTM hash-only metadata path design under BLK-024 Track H, only after candidate fixtures keep protected-vault bodies denied.
2. Publication approval fixture hardening under Track G, still not live approval capture, if hostile review finds approval replay/staleness gaps.
3. Authoritative BEO publication implementation proposal only after explicit human approval for signer/storage/ledger/rollback side-effect authority and separate hostile pre-review.
4. Separate synthetic-smoke expansion or BLK-test L4 pilot only if the operator explicitly approves a new source-bound one-run envelope; do not couple it to BEO publication.

---

## 13. Final Planning Thesis

BLK-SYSTEM-023 should make BEO publication mechanically boring before making it real. The output is a replayable candidate fixture, not a published outcome: it proves shape, binding, rejection, and side-effect denial while keeping publication, RTM, protected-vault, and BLK-test authorities separate.
