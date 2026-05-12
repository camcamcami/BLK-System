# BLK-SYSTEM-085 — BEO Publication Pilot Execution Request Gate Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, `test-driven-development`, and hostile review while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, but current sequencing authority is `docs/BLK-077_blk-system-post-078-roadmap.md`, `docs/BLK-079_post-078-current-state-authority-index.md`, and `docs/BLK-084_post-083-frontier-selection-gate-refresh.md`.

**Goal:** Convert the post-BLK-SYSTEM-084 `beo_publication_pilot_execution_request` frontier into a deterministic, explicit human-approval request gate without approving or executing publication.
**BLK-024 track:** Track G — BEO publication path, Track A — doctrine/alignment/review gates, Track I — operator UX/observability and escalation; maturity level L0/L1 request fixture with L2-style fail-closed validation, not runtime.
**Architecture:** BLK-077/079/084 require a fresh operator decision naming exactly one frontier before any higher-authority work. The user asked for the next logical BLK-System sprint after BLK-SYSTEM-084; BLK-077 records the BLK-001-aligned current priority as `beo_publication_pilot_execution_request`. BLK-SYSTEM-085 therefore selects exactly that frontier as a request-gate sprint only. It consumes the BLK-083 decision-package fixture as upstream evidence and emits a local request package that a future human may approve separately.
**Tech Stack:** Markdown doctrine/plans/outcomes plus deterministic Python fixture/tests.
**Authority boundary:** This sprint is not publication approval and not publication pilot execution. It does not write or publish a BEO, capture live approval, sign artifacts, write immutable storage, append ledgers, execute rollback/revocation/supersession, generate RTM, compare protected active-vault hashes, read protected BLK-req bodies, run BLK-test/Codex/BLK-pipe, dispatch BEBs, close out BEOs, scan or mutate a target repo, use package/network/model/browser/cyber tooling, or claim production isolation.

---

## 0. Preflight Current State

Preflight captured on 2026-05-12T12:27:37+10:00:

```text
## main...origin/main
HEAD: 5842890b3344f1836c94f84c43fb75a7adba7bcc
origin/main: 5842890b3344f1836c94f84c43fb75a7adba7bcc
latest commit: 5842890 docs: close blk-system 084 post-083 frontier selection gate
```

ID discovery:

- No `BLK-SYSTEM-085`, `BLK-085`, or `blk-system-085` artifact exists.
- `docs/BLK-084_post-083-frontier-selection-gate-refresh.md` lists `beo_publication_pilot_execution_request` as one exact candidate frontier.
- `docs/BLK-077_blk-system-post-078-roadmap.md` says the current BLK-001-aligned priority is `beo_publication_pilot_execution_request`, but that guidance is not authority and grants no publication, BEO, BLK-test, Codex, BLK-pipe, RTM, protected-body, target-repo, tooling, signer/storage/ledger/rollback, or isolation authority.
- `docs/BLK-083_beo-publication-decision-package-pilot-request.md` provides the upstream decision-package fixture and explicitly requires a later separate publication pilot approval before any pilot execution.

Selection rationale:

The request to execute the next logical BLK-System sprint is treated as selecting exactly one roadmap candidate frontier: `beo_publication_pilot_execution_request`. BLK-SYSTEM-085 does not execute the pilot. It creates the deterministic request gate that makes any later approval explicit, exact, hash-bound, bounded, and hostile-reviewable.

---

## 1. Governing Documents

| Governing doc | BLK-SYSTEM-085 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Advance the end-to-end V-model closure path while preserving separation between planning, tactical execution, BLK-pipe mutation, BLK-test evidence, BEO publication, and blk-link RTM trace closure. |
| BLK-002 — Artifact Lifecycle | Preserve HITL approval boundaries and active-vault immutability; this request gate must not promote artifacts or read protected bodies. |
| BLK-003 — Orchestration Protocol | Preserve human dispatch gates and no inherited authority across BEB, BEO, BLK-test, BEO publication, and RTM phases. |
| BLK-004 — BLK-pipe V47 Suite | Preserve Go BLK-pipe as final mutation enforcement; this request gate cannot dispatch BLK-pipe or mutate source. |
| BLK-005 — BLK-Req Specification | Preserve canonical `version_hash` trace binding without claiming coverage, drift truth, or RTM closure. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny and no protected body reads/copying/parsing/hashing/summarizing/scanning/mutation. |
| BLK-022, BLK-026, BLK-057, BLK-060 | Preserve historical BEO publication design/request/envelope boundaries as review-only unless a later sprint grants exact publication-pilot authority. |
| BLK-077, BLK-079, BLK-084 | Current post-084 selection authority: exactly one frontier may be selected, but roadmap guidance is not execution authority. |
| BLK-083 | Upstream BEO Publication Decision Package / Pilot Request fixture; its output is evidence for this request gate, not approval. |

---

## 2. Non-Authority Contract

BLK-SYSTEM-085 may build, validate, document, and close out a deterministic local request package. It may not perform any real publication side effect.

Explicit denials:

```text
NO_PUBLICATION_APPROVAL_GRANTED
NO_PUBLICATION_PILOT_EXECUTION_PERFORMED
NO_RUNTIME_PUBLISHED_BEO_OUTPUT
NO_LIVE_PUBLICATION_APPROVAL_CAPTURE
NO_SIGNER_KEY_MATERIAL_ACCESS
NO_CRYPTOGRAPHIC_SIGNING_AUTHORITY
NO_IMMUTABLE_STORAGE_WRITE_AUTHORITY
NO_PUBLIC_LEDGER_APPEND_OR_MUTATION_AUTHORITY
NO_ROLLBACK_REVOCATION_OR_SUPERSESSION_EXECUTION_AUTHORITY
NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY
NO_ACTIVE_VAULT_HASH_COMPARISON_OR_COVERAGE_CLAIM_AUTHORITY
NO_PROTECTED_BLK_REQ_BODY_READS
NO_TARGET_REPO_SCAN_OR_MUTATION_AUTHORITY
NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_EXECUTION_AUTHORITY
NO_BLK_PIPE_BLK_TEST_OR_CODEX_RUNTIME_AUTHORITY
NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY
NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM
```

---

## 3. Task List

### Task 000 — Publish this plan and task-000 outcome

**Objective:** Commit this sprint plan plus a task-000 outcome documenting that no implementation changed yet.

**Allowed paths:**

```text
docs/plans/blk-system-085_beo-publication-pilot-execution-request-gate.md
docs/outcomes/BLK-SYSTEM-085_task-000-outcome.md
```

**Verification:**

```text
git diff --check -- docs/plans/blk-system-085_beo-publication-pilot-execution-request-gate.md docs/outcomes/BLK-SYSTEM-085_task-000-outcome.md
python - <<'PY'
from pathlib import Path
for path in [Path('docs/plans/blk-system-085_beo-publication-pilot-execution-request-gate.md'), Path('docs/outcomes/BLK-SYSTEM-085_task-000-outcome.md')]:
    text = path.read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, path
PY
```

**Commit:** `docs: plan blk-system 085 beo publication pilot request gate`

### Task 001 — RED/GREEN BEO publication pilot execution request fixture

**Objective:** Add a deterministic local fixture that consumes a BLK-083 decision package and a submitted execution-request envelope, then emits a review-ready request package that remains not approved and not executed.

**Allowed paths:**

```text
python/test_beo_publication_pilot_execution_request.py
python/beo_publication_pilot_execution_request.py
docs/outcomes/BLK-SYSTEM-085_task-001-outcome.md
```

**RED:** Write tests first proving the fixture is missing and must enforce:

1. exact frontier `beo_publication_pilot_execution_request`;
2. exact upstream BLK-083 decision package schema/status/hash/body binding;
3. no `approval_granted`, `publication_approved`, `pilot_execution_authorized`, `publication_performed`, runtime `PUBLISHED` output, signing, storage, ledger, rollback, RTM, protected-body, target-repo, BLK-test/Codex/BLK-pipe, tooling, or production-isolation side effects;
4. fresh future approval/run IDs that do not reuse upstream envelope or BLK-083 future IDs;
5. exact proof-obligation and denied-authority sets with duplicate/extra/missing rejection;
6. recursive caller-controlled key/value scanning with percent-decoding for publication approval, execution, signing/storage/ledger/rollback, RTM, protected-body, target-repo, tooling, source/Git, and production-isolation laundering;
7. no live-surface imports/calls.

**GREEN:** Implement only enough deterministic local validation/building code to satisfy those tests. The fixture must not read files, inspect target repos, spawn subprocesses, use network/tooling services, write side effects, or consume approval/run IDs.

**Focused tests:**

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest -v python.test_beo_publication_pilot_execution_request
```

**Commit:** `feat: add beo publication pilot request gate`

### Task 002 — BLK-085 doctrine and active doctrine gate

**Objective:** Publish `BLK-085` as the BEO publication pilot execution request gate boundary and pin persistent doctrine markers.

**Allowed paths:**

```text
docs/BLK-085_beo-publication-pilot-execution-request-gate.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-085_task-002-outcome.md
```

**RED:** Add an active doctrine gate that fails until BLK-085 contains exact markers for request-gate status, upstream BLK-083 binding, future explicit approval requirement, exact denied-authority markers, and separation from RTM/BLK-test/Codex/BLK-pipe/target/protected/tooling/isolation authority.

**GREEN:** Write the doctrine doc minimally to satisfy the gate.

**Focused tests:**

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest -v python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint085_beo_publication_pilot_execution_request_gate_denies_publication_authority
```

**Commit:** `docs: add blk 085 beo publication pilot request gate`

### Task 003 — Roadmap/current-state alignment

**Objective:** Update BLK-077, BLK-079, and the current-state fixture so BLK-SYSTEM-085 is recorded as a completed request gate and any later actual publication pilot still requires a separate explicit human approval.

**Allowed paths:**

```text
docs/BLK-077_blk-system-post-078-roadmap.md
docs/BLK-079_post-078-current-state-authority-index.md
python/blk_current_state_authority_index.py
python/test_blk_current_state_authority_index.py
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-085_task-003-outcome.md
```

**RED:** Add tests that fail until current-state surfaces include BLK-085 and roadmap/index text says BLK-SYSTEM-085 is a request gate only, not approval or publication.

**GREEN:** Update docs/fixture to reflect BLK-SYSTEM-085 without granting any runtime authority.

**Focused tests:**

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest -v python.test_blk_current_state_authority_index python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint085_completion_preserves_publication_pilot_authority_boundary
```

**Commit:** `docs: align roadmap after blk-system 085`

### Task 004 — Hostile review, remediation, closeout, and push

**Objective:** Perform adversarial review, remediate blockers with tests, run final verification, publish review and closeout docs, and push `main`.

**Allowed paths:**

```text
docs/reviews/BLK-SYSTEM-085_hostile-review.md
docs/outcomes/BLK-SYSTEM-085_sprint-closeout.md
```

Hostile review must probe:

- request package becoming publication approval;
- request package becoming publication pilot execution;
- self-consistent forged BLK-083 decision packages;
- reused approval/run IDs;
- stale, expired, or replayed request envelopes;
- multiple-frontier or secondary-frontier selection;
- BEO decision-package readiness laundering into actual publication;
- RTM authority before publication prerequisites;
- percent-encoded / compact / camelCase authority terms;
- hidden target-repo, source/Git, protected-body, package-manager, network, model, browser, cyber, signer/storage/ledger/rollback, or production-isolation side effects;
- missing false side-effect flags or incomplete denied-authority sets.

Final verification:

```text
rm -rf /tmp/blk-system-pycache python/__pycache__ && PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

**Commit:** `docs: close blk-system 085 beo publication pilot request gate`

---

## 4. Completion Criteria

BLK-SYSTEM-085 is complete only when:

1. the plan and all outcome docs are committed;
2. the BEO publication pilot execution request fixture has RED/GREEN evidence;
3. BLK-085 doctrine exists and is pinned by an active doctrine gate;
4. BLK-077/079/current-state fixture record BLK-SYSTEM-085 completion;
5. hostile review passes after any remediation;
6. full Python suite, Go suite, Go vet, and `git diff --check` pass;
7. changes are pushed to `origin/main`.
