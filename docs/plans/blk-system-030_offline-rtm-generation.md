# BLK-SYSTEM-030 — Offline RTM Generation Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, `systematic-debugging`, and hostile review skills when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable.

**Goal:** Implement narrow offline RTM generation from already-supplied `PUBLISHED_BEO_INPUT_FIXTURE_ONLY` and `ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY` inputs.
**BLK-024 track:** Track H — BLK-link offline RTM ledger, with Track G published-BEO input and Track B hash-only metadata prerequisites / maturity level L2-style approved local generation from fixture inputs.
**Architecture:** BLK-SYSTEM-030 consumes caller-supplied published-BEO input fixture metadata and caller-supplied active-vault hash metadata backend fixture records to build a deterministic offline RTM ledger object. It does not read protected BLK-req bodies, scan active-vault files, publish BEOs, mutate signer/storage/public ledgers, reject drift, inherit approvals, or contact external services. Drift and stale/missing/rejected evidence states become review records only.
**Tech Stack:** Markdown doctrine/review docs, Python deterministic local helper, Python `unittest` gates, Git CLI.
**Authority boundary:** Narrow RTM-generation approval only. No protected BLK-req body reads, no active-vault filesystem scanning, no BEO publication, no signer/storage/public-ledger side effects, no RTM drift rejection, and no inherited approval from execution/BLK-test/BEO publication/proposal fixtures.

---

## 0. Current Known State

- **Date:** 2026-05-08T14:22:54+10:00
- **Branch state:** `## main...origin/main`
- **HEAD:** `e294169 docs: close blk-system sprint 029 health-check boundary`
- **Baseline verification:**
  - `go test ./...` — PASS
  - `go vet ./...` — PASS
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover python 'test_*.py'` — Ran 409 tests in 6.450s, OK
  - `git diff --check` — PASS
- **ID discovery:** `BLK-SYSTEM-030` has no existing plan/outcome/review collision. `BLK-033` is the next available root BLK boundary document ID after BLK-032.
- **Explicit approval source:** Current operator message approves a narrow BLK-System sprint to implement offline RTM generation from already-supplied `PUBLISHED_BEO_INPUT_FIXTURE_ONLY` and `ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY` inputs, while excluding protected-body reads, active-vault scanning, BEO publication, signer/storage/public-ledger side effects, RTM drift rejection, and inherited approvals.

---

## 1. Authority Boundary

This sprint authorizes only deterministic local offline RTM generation from already-supplied fixture dictionaries. It may emit an offline RTM ledger fixture and coverage/review records derived from supplied trace artifact identities and supplied hash metadata identities.

This sprint does not authorize Hindsight use, Codex use, live tactical LLM execution, network model services, cyber tooling, protected BLK-req vault body reads/copying/parsing/hashing/mutation, active-vault filesystem scanning, runtime active-vault file comparison, authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, RTM drift rejection authority, production BLK-test MCP, new live BLK-test smoke runs, production sandbox/cgroup/VM/network/host-secret isolation claims, package-manager execution, arbitrary shell, or source mutation outside exact approved allowlists.

RTM generation approval in this sprint is not inherited from BLK-pipe execution, BLK-test PASS, BEO publication candidate fixtures, published-BEO input receipt fixtures, backend metadata approval fixtures, or BLK-SYSTEM-027 proposal fixtures. It must be represented by a new `OFFLINE_RTM_GENERATION_APPROVAL_FIXTURE_ONLY` approval record bound to exact input IDs/hashes, backend manifest hash, operator identity, timestamp, output identity, and explicit no-drift-rejection policy.

---

## 2. BLK-024 Selection Rationale

BLK-024 Track H says `blk-link` should create an offline RTM ledger from published BEO metadata and approved hash-only vault metadata while preserving protected-body isolation and human-review boundaries for drift decisions.

BLK-SYSTEM-025 created `PUBLISHED_BEO_INPUT_FIXTURE_ONLY` input fixtures. BLK-SYSTEM-026 created `ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY` backend fixtures. BLK-SYSTEM-027 created only `RTM_GENERATION_READINESS_PROPOSAL_FIXTURE_ONLY` evidence and explicitly required later human approval for generation. The current operator message supplies that narrow approval.

---

## 3. BLK-001 Through BLK-006 Alignment

| Governing doc | Relevance | Preserved boundary |
| --- | --- | --- |
| BLK-001 — Master Architecture | Offline RTM closes trace between BEO metadata and BLK-req hash metadata. | Does not merge BLK-req, BLK-pipe, BLK-test, BEO publication, or drift authorities. |
| BLK-002 — Artifact Lifecycle | RTM consumes immutable IDs and canonical hashes. | No staging, promotion, revision, active-vault scanning, or protected-body access. |
| BLK-003 — Orchestration Protocol | RTM generation approval remains separate from execution/BLK-test/BEO gates. | No BEB dispatch, BLK-pipe invocation, BLK-test startup, retry approval, or failure-ceiling reset. |
| BLK-004 — BLK-pipe V47 Suite | Source mutation remains owned by BLK-pipe. | RTM helper is pure local data normalization/generation and does not touch Git/source. |
| BLK-005 — BLK-Req Specification | Trace artifacts use kind/id/version_hash only. | No requirement/use-case body parsing; hash-only identity matching only. |
| BLK-006 — BLK-Req Implementation Brief | Protected vault remains hard-deny. | No protected-vault body reads, copies, parsing, hashing, summaries, or path scans. |

---

## 4. Planned Artifacts

Task execution should create or modify exactly these primary artifacts unless hostile review requires exact-scope remediation:

- `docs/BLK-033_offline-rtm-generation-boundary.md`
- `python/offline_rtm_generation_fixtures.py`
- `python/test_offline_rtm_generation_fixtures.py`
- `python/test_active_doctrine_review_gates.py`
- `docs/reviews/BLK-SYSTEM-030_offline-rtm-generation-input-inventory.md`
- `docs/reviews/BLK-SYSTEM-030_offline-rtm-generation-hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-030_task-000-outcome.md`
- `docs/outcomes/BLK-SYSTEM-030_task-001-outcome.md`
- `docs/outcomes/BLK-SYSTEM-030_task-002-outcome.md`
- `docs/outcomes/BLK-SYSTEM-030_task-003-outcome.md`
- `docs/outcomes/BLK-SYSTEM-030_sprint-closeout.md`

---

## 5. Planned Tasks

### Task 0 — Publish plan and task-000 outcome

**Deliverables:**

- `docs/plans/blk-system-030_offline-rtm-generation.md`
- `docs/outcomes/BLK-SYSTEM-030_task-000-outcome.md`

**Acceptance criteria:**

- Plan records live preflight facts and explicit approval scope.
- Plan states BLK-024 Track H and narrow RTM generation boundary.
- Plan excludes protected-body reads, active-vault scanning, BEO publication, signer/storage/public-ledger side effects, drift rejection, and inherited approvals.
- Plan is committed and pushed with exact-path staging.

**Verification:**

```bash
git diff --check -- docs/plans/blk-system-030_offline-rtm-generation.md docs/outcomes/BLK-SYSTEM-030_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
for p in [
    Path('docs/plans/blk-system-030_offline-rtm-generation.md'),
    Path('docs/outcomes/BLK-SYSTEM-030_task-000-outcome.md'),
]:
    text = p.read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, p
PY
```

**Commit:** `docs: plan blk-system sprint 030 offline rtm generation`

### Task 1 — Inventory approved inputs and generation constraints

**Deliverables:**

- `docs/reviews/BLK-SYSTEM-030_offline-rtm-generation-input-inventory.md`
- `docs/outcomes/BLK-SYSTEM-030_task-001-outcome.md`

**Acceptance criteria:**

- Inventory names exact required published-BEO input fields.
- Inventory names exact required active-vault hash metadata backend fields.
- Inventory defines `OFFLINE_RTM_GENERATION_APPROVAL_FIXTURE_ONLY` approval binding.
- Inventory defines RTM ledger output fields and review-only coverage states.
- Inventory records forbidden fields/actions: protected paths/bodies, active-vault scans, publication/signing/storage/ledger side effects, drift rejection, source mutation, inherited approvals, runtime API/network/tool execution.

**Verification:**

```bash
git diff --check -- docs/reviews/BLK-SYSTEM-030_offline-rtm-generation-input-inventory.md docs/outcomes/BLK-SYSTEM-030_task-001-outcome.md
```

**Commit:** `docs: inventory offline rtm generation inputs`

### Task 2 — Implement offline RTM generation helper and BLK-033 doctrine

**Deliverables:**

- `python/offline_rtm_generation_fixtures.py`
- `python/test_offline_rtm_generation_fixtures.py`
- `docs/BLK-033_offline-rtm-generation-boundary.md`
- update `python/test_active_doctrine_review_gates.py`
- `docs/outcomes/BLK-SYSTEM-030_task-002-outcome.md`

**Required vocabulary:**

- `OFFLINE_RTM_GENERATION_APPROVAL_FIXTURE_ONLY`
- `OFFLINE_RTM_LEDGER_GENERATED_FIXTURE_ONLY`
- `OFFLINE_RTM_COVERAGE_MATRIX_FIXTURE_ONLY`
- `DRIFT_REVIEW_REQUIRED_NOT_REJECTED`
- `PROTECTED_BODY_NOT_READ`
- `ACTIVE_VAULT_NOT_SCANNED`
- `BEO_PUBLICATION_NOT_PERFORMED`
- `NO_SIGNER_STORAGE_OR_PUBLIC_LEDGER_SIDE_EFFECTS`

**Acceptance criteria:**

- Strict TDD: write failing tests first, observe RED, then implement minimal fixture code.
- Helper consumes only caller-supplied dictionaries: published-BEO input fixture, backend metadata fixture, and RTM-generation approval fixture.
- Happy path emits deterministic offline RTM ledger fixture with:
  - ledger ID and ledger hash derived from canonical JSON of supplied metadata;
  - source input ID, BEO ID/hash, BEO status, publication receipt hash;
  - backend manifest ID/hash and backend approval hash;
  - trace artifacts copied from input metadata only;
  - coverage records with `TRACE_HASH_MATCHED` for exact kind/id/version_hash matches;
  - review-only states for missing, extra, or mismatched metadata that fail closed unless the test explicitly models a review package;
  - explicit no-side-effect booleans.
- Input validation rejects:
  - non-`PUBLISHED_BEO_INPUT_FIXTURE_ONLY` inputs;
  - non-`ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY` backend fixtures;
  - missing/malformed hashes or IDs;
  - duplicate trace or metadata identities;
  - trace/metadata mismatches;
  - extra metadata identities;
  - protected path/body fields and nested body/path/secret fields;
  - active-vault read/scan flags;
  - publication/signer/storage/public-ledger/rollback fields or flags;
  - drift rejection fields/flags;
  - inherited approval scopes such as proposal, execution, BLK-test, BEO publication, or backend approval.
- Implementation must not import or call live execution/network/file-scan APIs (`subprocess`, `socket`, `requests`, `urllib`, `http.client`, `os.system`, `eval`, `exec`, `__import__`, `open`, `Path`, `read_text`, `glob`, `rglob`, Discord/GitHub APIs).
- BLK-033 must state that this sprint authorizes only offline RTM generation from already-supplied fixture inputs and does not authorize drift rejection or protected-body access.

**Focused verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_offline_rtm_generation_fixtures -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
```

**Commit:** `feat: add offline rtm generation fixtures`

### Task 3 — Hostile review, remediation, full verification, and closeout

**Deliverables:**

- `docs/reviews/BLK-SYSTEM-030_offline-rtm-generation-hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-030_task-003-outcome.md`
- `docs/outcomes/BLK-SYSTEM-030_sprint-closeout.md`
- exact remediation changes required by hostile review, if any

**Hostile review must probe:**

- protected-body reads or active-vault scans sneaking through evidence refs, metadata, strings, or side-effect flags;
- BEO publication or signer/storage/public-ledger side effects disguised as receipt handling;
- RTM drift rejection disguised as coverage, stale, mismatch, or review state;
- inherited approval from proposal, execution, BLK-test, BEO publication, or backend metadata approvals;
- trace/metadata bijection errors and extra metadata emitted as coverage;
- ledger hash instability from non-canonical ordering;
- accepting malformed/replayed/stale/expired approval;
- unsupported top-level fields ignored instead of rejected;
- marker-only doctrine gates that do not assert the actual boundary.

**Full verification:**

```bash
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover python 'test_*.py'
git diff --check
git status --short --branch
```

**Commit:** `docs: close blk-system sprint 030 offline rtm generation`

---

## 6. Exact-Path Git Discipline

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

Remove Python bytecode/cache artifacts before staging using a short Python cleanup or exact cache paths only.

---

## 7. Stop Conditions

Stop and escalate rather than broadening scope if any task appears to require:

- reading, copying, parsing, hashing, summarizing, quoting, or exposing protected BLK-req vault bodies;
- scanning `docs/active/`, `docs/requirements/`, `docs/use_cases/`, or any active/protected-vault path;
- treating BEO publication candidates as published-BEO inputs without `PUBLISHED_BEO_INPUT_FIXTURE_ONLY`;
- publishing BEOs or accessing signer/storage/public-ledger authority;
- mutating source, Git, active-vault files, immutable storage, or public ledgers;
- rejecting drift or making a final drift decision;
- inheriting approval from execution, BLK-test, BEO publication, backend metadata, or RTM proposal fixtures;
- contacting network/model/API services, running package managers, or executing shell commands as product behavior;
- claiming production sandbox, cgroup, VM, network, or host-secret isolation.

---

## 8. Future Authority Handoff

After BLK-SYSTEM-030 closes, a later sprint may request RTM drift review or rejection authority only if:

1. BLK-033 exists and passes doctrine gates;
2. offline RTM ledger generation has hostile-reviewed trace/metadata bijection and canonical hashing;
3. drift-like states are emitted as review-required records only;
4. protected-body exclusion remains mechanically tested;
5. signer/storage/public-ledger/BEO publication side effects remain absent;
6. the human explicitly approves drift-review/rejection authority as a separate sprint.
