# BLK-SYSTEM-084 — Post-083 Frontier Selection Gate Refresh Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, `test-driven-development`, and hostile review while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity lineage, but current selection authority is `docs/BLK-077_blk-system-post-078-roadmap.md` plus `docs/BLK-079_post-078-current-state-authority-index.md`.

**Goal:** Refresh BLK-System's frontier-selection machinery for the post-BLK-SYSTEM-083 state so “next logical sprint” language cannot become implicit authority for publication, BLK-test, Codex, RTM, target-repo, or protected-body work.  
**BLK-024 track:** Track A — doctrine/alignment/review gates, Track G — BEO publication path, Track I — operator UX/observability and escalation; maturity level L0/L1 fixture-only.  
**Architecture:** BLK-077 and BLK-079 say no automatic post-083 sprint authority exists. BLK-SYSTEM-084 selects the lowest-authority bounded consolidation/remediation movement: a deterministic post-083 frontier-selection gate that can classify exactly one future frontier for human decision while denying all activation side effects.  
**Tech Stack:** Markdown doctrine/plans/outcomes plus deterministic Python fixture/tests.  
**Authority boundary:** L0/L1 selection fixture and doctrine-gate refresh only. This sprint does not grant publication approval, execute a publication pilot, run BLK-test, start Codex, invoke BLK-pipe, generate RTM, inspect/mutate a target repository, read protected BLK-req bodies, use package/network/model/browser/cyber tooling, or claim production isolation.

---

## 0. Preflight Current State

Preflight captured on 2026-05-12T08:12:10+10:00:

```text
## main...origin/main
5e306b6 docs: close blk-system 083 beo publication decision package
origin/main: 5e306b6db11e0556feb9298c2ddd187afe020655
```

ID discovery:

- No `docs/BLK-084_*.md` exists.
- No `docs/plans/blk-system-084_*.md` exists before this plan.
- `python/test_beo_publication_decision_package.py` already reserves future candidate ID strings containing `BLK-SYSTEM-084`, but there is no BLK-SYSTEM-084 sprint artifact.
- BLK-077 line 325 and BLK-079 line 221 require explicit operator decision before any higher-authority post-083 frontier.
- BLK-SYSTEM-083 closeout line 209 states no automatic next sprint authority exists and any BLK-SYSTEM-084 selection must name exactly one frontier.

Selection rationale:

The user asked for the “next logical BLK-System sprint” but did not name a specific higher-authority frontier such as actual BEO publication pilot execution, BLK-test evidence refresh, Codex L3 smoke, or RTM authority. Under BLK-077/079/083, that is not enough authority to run a higher frontier. The next logical non-laundering sprint is therefore a bounded consolidation/remediation sprint: refresh the frontier-selection gate to the post-083 candidate set and keep all future activation separate.

---

## 1. Governing Documents

| Governing doc | BLK-SYSTEM-084 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Preserve separation between planning, tactical execution, BLK-pipe mutation, BLK-test evidence, BEO publication, and RTM trace closure. |
| BLK-002 — Artifact Lifecycle | Preserve HITL approval and active-vault isolation; selection evidence cannot promote protected artifacts or read protected bodies. |
| BLK-003 — Orchestration Protocol | Preserve human dispatch gates and no inherited authority across BEB/BEO/BLK-test/BEO publication/RTM phases. |
| BLK-004 — BLK-pipe V47 Suite | Preserve Go BLK-pipe as final mutation enforcement; this selector cannot dispatch BLK-pipe or mutate source. |
| BLK-005 — BLK-Req Specification | Preserve trace binding without creating coverage, drift, publication, or RTM truth from selection records. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny and no body reads/copying/parsing/hashing/summarizing/scanning/mutation. |
| BLK-077 — Post-078 Roadmap | Current roadmap selector. After BLK-SYSTEM-083, require exact frontier choice before higher authority. |
| BLK-079 — Current-State Authority Index | Current operator authority map. BLK-SYSTEM-084 must keep the index non-runtime. |
| BLK-083 — BEO Publication Decision Package | Publication decision-package readiness is not approval and not execution. |
| BLK-048 — Historical Authority Frontier Selection Gate | Historical selection-gate pattern to avoid `next sprint` authority laundering; must not remain the only post-083 selector because it is BLK-045-era and omits current candidates. |

---

## 2. Non-Authority Contract

This plan does not authorize production BLK-test MCP, live tactical LLM/Codex execution, arbitrary shell as BLK-test behavior, BLK-pipe dispatch, protected BLK-req vault body reads, BEO closeout execution, authoritative BEO publication, publication pilot execution, live publication approval capture, signer/storage/ledger/rollback side effects, runtime RTM generation, RTM drift rejection, public ledger mutation, target-repo scan/mutation, package-manager/network/model/browser/cyber tooling, or production sandbox/host-secret-isolation claims.

---

## 3. Task List

### Task 000 — Publish this plan and task-000 outcome

**Objective:** Commit this sprint plan plus a task-000 outcome documenting that no implementation changed yet.

**Allowed paths:**

```text
docs/plans/blk-system-084_post-083-frontier-selection-gate-refresh.md
docs/outcomes/BLK-SYSTEM-084_task-000-outcome.md
```

**Verification:**

```text
git diff --check -- docs/plans/blk-system-084_post-083-frontier-selection-gate-refresh.md docs/outcomes/BLK-SYSTEM-084_task-000-outcome.md
python - <<'PY'
from pathlib import Path
for path in [Path('docs/plans/blk-system-084_post-083-frontier-selection-gate-refresh.md'), Path('docs/outcomes/BLK-SYSTEM-084_task-000-outcome.md')]:
    text = path.read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, path
PY
```

**Commit:** `docs: plan blk-system 084 post-083 frontier selection gate`

### Task 001 — RED/GREEN post-083 frontier-selection fixture

**Objective:** Add a deterministic Python fixture for current post-083 frontier selection.

**Allowed paths:**

```text
python/test_blk_post083_frontier_selection_gate.py
python/blk_post083_frontier_selection_gate.py
docs/outcomes/BLK-SYSTEM-084_task-001-outcome.md
```

**RED:** Write tests first proving the fixture is missing and must enforce:

1. exact candidate frontier names only;
2. “next logical sprint” / “next sprint” / generic strings are not authority;
3. no multiple frontier selections;
4. BEO pilot, BLK-test refresh, Codex L3 smoke, and RTM request candidates are selection records only, not execution;
5. RTM request selection remains blocked without actual publication prerequisites;
6. exact denied-authority set and false side-effect flags;
7. nested key/value/string authority laundering rejection, including percent-encoded publication/RTM/protected-body claims;
8. no source/Git/runtime/network/tooling imports or calls.

**GREEN:** Implement only enough deterministic local validation/building code to satisfy those tests. The fixture must not read files, inspect target repos, spawn subprocesses, use network/tooling services, write side effects, or consume approval/run IDs.

**Focused tests:**

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest -v python.test_blk_post083_frontier_selection_gate
```

**Commit:** `feat: add post-083 frontier selection fixture`

### Task 002 — BLK-084 doctrine and active doctrine gate

**Objective:** Publish `BLK-084` as the current post-083 selection-gate boundary and pin persistent doctrine markers.

**Allowed paths:**

```text
docs/BLK-084_post-083-frontier-selection-gate-refresh.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-084_task-002-outcome.md
```

**RED:** Add an active doctrine gate that fails until BLK-084 contains exact markers for post-083 selection, review-only fixture status, the candidate frontier set, RTM prerequisite blocking, explicit denial of publication/BLK-test/Codex/RTM/BLK-pipe/target/protected/tooling/isolation authority, and no authority inheritance from BLK-077/079/083/048.

**GREEN:** Write the doctrine doc minimally to satisfy the gate.

**Focused tests:**

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest -v python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint084_post083_frontier_selection_gate_refresh_denies_runtime_authority
```

**Commit:** `docs: add blk 084 post-083 frontier selection doctrine`

### Task 003 — Roadmap/current-state alignment

**Objective:** Update BLK-077, BLK-079, and the current-state fixture so BLK-SYSTEM-084 is complete and higher-authority frontiers still require separate exact approval.

**Allowed paths:**

```text
docs/BLK-077_blk-system-post-078-roadmap.md
docs/BLK-079_post-078-current-state-authority-index.md
python/blk_current_state_authority_index.py
python/test_blk_current_state_authority_index.py
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-084_task-003-outcome.md
```

**RED:** Add tests that fail until current-state surfaces include BLK-084 and roadmap/index text says post-084 work still requires exactly one separately approved frontier.

**GREEN:** Update the docs/fixture to reflect BLK-SYSTEM-084 without granting any runtime authority.

**Focused tests:**

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest -v python.test_blk_current_state_authority_index python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint084_completion_preserves_post083_frontier_authority_boundary
```

**Commit:** `docs: align roadmap after blk-system 084`

### Task 004 — Hostile review, remediation, closeout, and push

**Objective:** Perform adversarial review, remediate blockers with tests, run final verification, publish review and closeout docs, and push `main`.

**Allowed paths:**

```text
docs/reviews/BLK-SYSTEM-084_hostile-review.md
docs/outcomes/BLK-SYSTEM-084_sprint-closeout.md
```

Hostile review must probe:

- “next logical sprint” becoming implicit approval;
- multiple-frontier or nested-secondary-frontier selection;
- stale BLK-048 allowed-frontier leakage;
- BEO decision-package readiness laundering into actual publication;
- RTM authority before publication prerequisites;
- percent-encoded / compact / camelCase authority terms;
- hidden target-repo, protected-body, package-manager, network, model, browser, cyber, signer/storage/ledger/rollback, or production-isolation side effects;
- missing false side-effect flags or incomplete denied-authority sets.

Final verification:

```text
rm -rf /tmp/blk-system-pycache && PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
go test ./...
git diff --check
```

**Commit:** `docs: close blk-system 084 post-083 frontier selection gate`

---

## 4. Completion Criteria

BLK-SYSTEM-084 is complete only when:

1. the plan and all outcome docs are committed;
2. the post-083 frontier-selection fixture has RED/GREEN evidence;
3. BLK-084 doctrine exists and is pinned by an active doctrine gate;
4. BLK-077/079/current-state fixture record BLK-SYSTEM-084 completion;
5. hostile review passes after any remediation;
6. full Python suite, Go suite, and `git diff --check` pass;
7. changes are pushed to `origin/main`.
