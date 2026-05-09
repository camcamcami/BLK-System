# BLK-SYSTEM-043 — Current-State Authority Index Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `code-review` when executing. This plan is guided by `docs/BLK-045_blk-system-post-042-roadmap.md` as the current post-BLK-SYSTEM-042 roadmap, with `docs/BLK-024_blk-system-development-roadmap.md` retained for maturity-model lineage, then BLK-001 through BLK-006 as applicable.

**Goal:** Evaluate BLK-045 and create a concise current-state authority index so the operator can see which BLK-System surfaces are enabled, fixture-only, disabled, or future-authority before any activation sprint.

**BLK-045 fork:** Fork A — Consolidation / Current-State Index.

**BLK-024 maturity lineage:** L0 doctrine plus L1 document/fixture gates. This is not L2 live transport, not L3 smoke, not L4 pilot runtime, and not L5 production authority.

**Architecture:** BLK-045 supersedes BLK-024 for post-BLK-SYSTEM-042 roadmap selection and says the next major choice should be either a short consolidation sprint or one explicitly approved runtime frontier. No explicit live Codex or BLK-test activation approval was granted in the operator request. Therefore the next logical sprint is the low-risk consolidation fork: BLK-046 plus a deterministic local index fixture that records current authority cutlines without enabling runtime behavior.

**Tech Stack:** Markdown doctrine, Python fixture/tests, active doctrine gates.

**Authority boundary:** Consolidation/index only. No live Codex execution, reusable live tactical LLM dispatch, BLK-pipe execution run, BLK-test MCP transport, arbitrary shell as BLK-test behavior, source mutation outside exact sprint files, protected BLK-req vault body reads/copying/parsing/hashing/summarizing/scanning/mutation, authoritative BEO publication, runtime RTM generation, RTM drift rejection, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, network/model/cyber/browser/package-manager tooling, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claim.

---

## 0. Current Repository State at Planning

```text
Date: 2026-05-09T18:45:13+10:00
Branch: main...origin/main
HEAD: c2abb34 docs: add blk045 post-042 roadmap
Existing highest system plan: docs/plans/blk-system-042_codex-live-dispatch-execution-authority-design-gate.md
Existing highest BLK boundary/roadmap doc: docs/BLK-045_blk-system-post-042-roadmap.md
```

Discovery found no existing `BLK-SYSTEM-043`, `blk-system-043`, or `BLK-046` owner in `docs/` or `python/`.

---

## 1. BLK-045 Evaluation

BLK-045 is internally usable as the current roadmap selector:

1. It clearly supersedes BLK-024 for current sequencing after BLK-SYSTEM-042 while retaining BLK-024's maturity vocabulary.
2. It preserves BLK-001 through BLK-006 authority boundaries and does not weaken active BLK-025 through BLK-044 cutlines.
3. It correctly identifies that Codex pre-dispatch evidence, validation profiles, operator health fixtures, and BEO/RTM packaging have enough scaffolding for a human decision.
4. It offers three valid forks: consolidation, Codex live-dispatch activation, or V-model completion.
5. It requires explicit activation approval before any L3/L4 runtime frontier.

The operator requested evaluation, planning, and execution but did not explicitly grant live Codex execution, BLK-test pilot authority, BEO publication, RTM generation, or drift authority. Under BLK-045 Sections 4, 5, 8, and 10, this makes Fork A the next logical sprint. It reduces cognitive load and stale-roadmap ambiguity before the later human decision about Fork B or Fork C.

---

## 2. Governing Documents and Obligations

- **BLK-045:** Current roadmap selector after BLK-SYSTEM-042. This sprint implements the recommended short consolidation/current-state index fork only.
- **BLK-024:** Historical roadmap and maturity-model lineage. This sprint remains L0/L1 and does not claim L2/L3/L4/L5.
- **BLK-001:** Preserve V-model separation between BLK-req, planning, tactical execution, BLK-pipe mutation enforcement, BLK-test evidence, BEO publication, and blk-link trace closure.
- **BLK-002 / BLK-005 / BLK-006:** Preserve staged artifact lifecycle, active-vault immutability, canonical hash binding, and protected-vault hard-deny semantics. This sprint must not read protected BLK-req bodies.
- **BLK-003:** Preserve human dispatch gates, bounded context, and no implicit inheritance between execution, testing, publication, and RTM.
- **BLK-004:** Preserve Go `blk-pipe` as final enforcement authority; Python index fixtures are advisory/documentary only.
- **BLK-040 through BLK-044:** Preserve Codex live-dispatch ladder as review-ready/design-ready/disabled-adapter evidence only, with no live execution authority.

---

## 3. Proposed Implementation Surface

### New Boundary/Index Document

```text
docs/BLK-046_blk-system-current-state-authority-index.md
```

Required vocabulary:

```text
BLK_SYSTEM_CURRENT_STATE_AUTHORITY_INDEX
BLK_045_CURRENT_ROADMAP_CONTROLS_POST_042_SELECTION
CONSOLIDATION_INDEX_ONLY_NO_RUNTIME_AUTHORITY
CURRENT_STATE_INDEX_L0_L1_ONLY
CODEX_LIVE_DISPATCH_REVIEW_READY_NOT_EXECUTION_AUTHORIZED
BLK_TEST_EVIDENCE_ONLY_PRODUCTION_MCP_DISABLED
BEO_PUBLICATION_DISABLED_DRAFT_AND_FIXTURE_ONLY
RTM_RUNTIME_GENERATION_AND_DRIFT_REJECTION_DISABLED
PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN
BLK_PIPE_REMAINS_FINAL_MUTATION_ENFORCEMENT_AUTHORITY
CURRENT_STATE_INDEX_GRANTS_NO_LIVE_AUTHORITY
```

### New Python Fixture

```text
python/blk_current_state_authority_index.py
```

Proposed functions:

```text
build_current_state_authority_index()
validate_current_state_authority_index(record)
evaluate_current_state_authority_index(record)
```

The fixture must return a deterministic local current-state record. It must not read protected BLK-req bodies, start subprocesses, call Codex, call BLK-pipe, use Git, call network/model services, install packages, mutate files, publish BEOs, generate RTMs, or claim production isolation.

### New Tests

```text
python/test_blk_current_state_authority_index.py
```

Test scope:

1. the default index evaluates to `CURRENT_STATE_INDEX_READY_FOR_OPERATOR_REVIEW_NOT_AUTHORITY`;
2. every expected authority surface is present exactly once;
3. live Codex, production BLK-test, authoritative BEO publication, runtime RTM generation, drift rejection, protected-body access, network/package/model/cyber/browser tooling, and production sandbox claims are all denied;
4. unsupported state/maturity values fail closed;
5. recursive authority-laundering keys/strings fail closed;
6. source AST contains no live imports/calls for subprocess, shell, Git, network clients, package managers, `exec`, or `eval`.

### Doctrine Gate Update

```text
python/test_active_doctrine_review_gates.py
```

Add persistent gates requiring BLK-045 to remain the current roadmap selector and BLK-046 to preserve the current-state index non-execution boundary.

---

## 4. Exact Allowed Implementation Paths

```text
docs/plans/blk-system-043_current-state-authority-index.md
docs/outcomes/BLK-SYSTEM-043_task-000-outcome.md
docs/BLK-046_blk-system-current-state-authority-index.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-043_task-001-outcome.md
python/blk_current_state_authority_index.py
python/test_blk_current_state_authority_index.py
docs/outcomes/BLK-SYSTEM-043_task-002-outcome.md
docs/reviews/BLK-SYSTEM-043_current-state-authority-index-hostile-review.md
docs/outcomes/BLK-SYSTEM-043_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-043_sprint-closeout.md
```

No `docs/active/`, `docs/requirements/`, or `docs/use_cases/` path may be modified or read for protected body content.

---

## 5. Task Breakdown

### Task 0 — Plan Publication

Create and publish this plan plus `docs/outcomes/BLK-SYSTEM-043_task-000-outcome.md`.

Verification:

```bash
git diff --check -- docs/plans/blk-system-043_current-state-authority-index.md docs/outcomes/BLK-SYSTEM-043_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
for path in [
    Path('docs/plans/blk-system-043_current-state-authority-index.md'),
    Path('docs/outcomes/BLK-SYSTEM-043_task-000-outcome.md'),
]:
    text = path.read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, path
print('markdown sanity PASS')
PY
```

Commit: `docs: plan blk-system sprint 043 current state authority index`

### Task 1 — BLK-046 Current-State Index and Doctrine Gates

Add BLK-046 and persistent active doctrine gates. RED first: add the focused gates and verify failure before writing the doc.

Allowed files:

```text
docs/BLK-046_blk-system-current-state-authority-index.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-043_task-001-outcome.md
```

Verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- docs/BLK-046_blk-system-current-state-authority-index.md python/test_active_doctrine_review_gates.py docs/outcomes/BLK-SYSTEM-043_task-001-outcome.md
```

Commit: `docs: define blk046 current state authority index`

### Task 2 — Deterministic Authority Index Fixture

Implement the pure fixture/helper and tests. RED first: create the tests and verify failure before implementing the helper.

Required record shape:

```text
index_id: blk_system_current_state_authority_index
index_status: BLK_SYSTEM_CURRENT_STATE_AUTHORITY_INDEX
roadmap_source: BLK-045
maturity: CURRENT_STATE_INDEX_L0_L1_ONLY
evaluation: CURRENT_STATE_INDEX_READY_FOR_OPERATOR_REVIEW_NOT_AUTHORITY or CURRENT_STATE_INDEX_BLOCKED
runtime_authority_granted: false
live_codex_execution_authorized: false
production_blk_test_mcp_authorized: false
authoritative_beo_publication_authorized: false
runtime_rtm_generation_authorized: false
rtm_drift_rejection_authorized: false
protected_blk_req_body_reads_authorized: false
```

Allowed files:

```text
python/blk_current_state_authority_index.py
python/test_blk_current_state_authority_index.py
docs/outcomes/BLK-SYSTEM-043_task-002-outcome.md
```

Verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_current_state_authority_index -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- python/blk_current_state_authority_index.py python/test_blk_current_state_authority_index.py docs/outcomes/BLK-SYSTEM-043_task-002-outcome.md
```

Commit: `feat: add current state authority index fixture`

### Task 3 — Hostile Review and Closeout

Perform hostile review, remediate blockers, write review and closeout docs, run final verification, commit, and push.

Hostile review questions:

1. Does BLK-046 or the fixture accidentally grant live Codex, BLK-pipe dispatch, BLK-test MCP, BEO publication, RTM generation, drift rejection, protected-body access, network/model/cyber/browser/package-manager tooling, or production isolation authority?
2. Does the index distinguish review-ready/fixture-ready from runtime authority?
3. Does BLK-045's supersession of BLK-024 remain clear without weakening BLK-001 through BLK-006?
4. Are all authority surfaces represented exactly once, or can a missing surface hide an unsafe default?
5. Can recursive authority-laundering keys/strings bypass fixture validation?
6. Is the next-step recommendation honest: consolidation now, explicit human approval required before any activation sprint?

Final verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_current_state_authority_index -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
export PATH="$HOME/.local/bin:$PATH"; go test ./... && go vet ./...
git diff --check
```

Commit: `docs: close blk-system sprint 043 current state authority index`

---

## 6. Expected Final State

BLK-SYSTEM-043 should leave the repository with a BLK-046 current-state authority index, persistent doctrine gates, and a deterministic Python fixture summarizing current authority surfaces. The sprint may report operator-review readiness only. It must not report runtime approval, dispatch success, verification success, source mutation, production sandbox enforcement, BEO publication, RTM generation, or drift decisions.
