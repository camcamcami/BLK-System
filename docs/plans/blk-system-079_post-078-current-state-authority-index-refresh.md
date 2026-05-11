# BLK-SYSTEM-079 — Post-078 Current-State Authority Index Refresh Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `blk-doctrine-gate-remediation` while executing. This plan is guided by historical maturity vocabulary in `docs/BLK-024_blk-system-development-roadmap.md`, current roadmap selection in `docs/BLK-077_blk-system-post-078-roadmap.md`, tactical-standard profile architecture in `docs/BLK-078_tactical-standard-profile-architecture.md`, and BLK-001 through BLK-006 as applicable.

**Goal:** Refresh BLK-System's operator-facing current-state authority map after BLK-SYSTEM-078 by superseding the stale BLK-046 index, making BLK-077 the current roadmap selector, recording BLK-078 as the tactical-standard/profile architecture anchor, and preserving all denied runtime authorities.
**BLK-024 track:** Track A — Doctrine, alignment, and review gates; Track I — Operator UX, observability, and escalation / maturity L0 doctrine-only plus L1 deterministic local fixture/gate tests.
**Architecture:** BLK-077 controls post-078 roadmap selection. BLK-078 separates Layer A universal BLK-System core, Layer B universal tactical-output safety, and Layer C target tactical profiles. This sprint refreshes current-state documentation and deterministic advisory fixtures so future sprint selection does not rely on stale BLK-045/046/059 authority maps.
**Tech Stack:** Markdown doctrine, Python unittest gates, Go test/vet verification.
**Authority boundary:** BLK-System documentation and deterministic local gate work only. No BEB dispatch or BEO closeout execution, no Kuronode source or Git mutation, no live Codex dispatch, no BLK-pipe execution, no production BLK-test MCP, no BEO publication, no RTM generation, no protected BLK-req body access, no package-manager/network/model/browser/cyber tooling, and no production sandbox or host-isolation claim.

---

## 0. Current Known State

Captured: `2026-05-11T19:06:54+10:00`

```text
repo: /home/dad/BLK-System
branch: main
local HEAD: 6741cd7afca499be25903b862f7e891bd63558f7
remote main: 6741cd7afca499be25903b862f7e891bd63558f7
status: ## main...origin/main
last commit: 6741cd7 docs: align roadmap with tactical profile architecture
```

Discovery:

```text
existing BLK-079 doc: none
existing BLK-SYSTEM-079 plan/outcomes: none
stale current-state index: docs/BLK-046_blk-system-current-state-authority-index.md still names BLK-045 as current roadmap selector
current roadmap selector: docs/BLK-077_blk-system-post-078-roadmap.md
profile architecture anchor: docs/BLK-078_tactical-standard-profile-architecture.md
```

Baseline checks:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_current_state_authority_index -q
# Ran 11 tests in 0.381s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint043_current_state_authority_index_boundary_denies_runtime_authority -q
# Ran 1 test — OK
```

---

## 1. Selection Rationale

BLK-077 explicitly selects BLK-SYSTEM-079 as the first post-078 sprint because BLK-046 and older roadmap/index documents are stale relative to BLK-SYSTEM-078, BLK-077, and BLK-078.

This sprint executes BLK-077 Workstream A only:

1. supersede or refresh BLK-046 so it no longer says BLK-045 controls current roadmap selection;
2. record BLK-077 as current roadmap authority;
3. record BLK-078 as the tactical-standard/profile architecture authority;
4. preserve BLK-058 as a future approved Kuronode TypeScript Layer C profile input, not as dispatch authority;
5. update persistent deterministic gates for future sprint selection.

The sprint deliberately does not proceed to target-repo execution governance, profile registry implementation, BEO publication, RTM generation, live Codex, or Kuronode mutation. Those are separate future frontiers.

---

## 2. Governing Alignment

| Document | Relevance | Preserved boundary |
| --- | --- | --- |
| BLK-001 | Defines the V-model separation between architecture, tactical execution, deterministic enforcement, verification evidence, publication, and trace closure. | Current-state indexing must make authority cutlines visible without converting target-state architecture into current runtime authority. |
| BLK-002 | Defines staged requirements/use-case intake and HITL promotion. | No current-state fixture, helper, BLK-test path, BEO path, RTM path, Codex path, or target-profile path may read/copy/parse/hash/summarize/scan/mutate protected BLK-req bodies. |
| BLK-003 | Defines orchestration, human dispatch gates, BLK-pipe invocation, hostile audit, BLK-test evidence, and BEO handoff. | Human dispatch gates remain separate from this index; BLK-test, BEO, and RTM authorities remain separately approved frontiers. |
| BLK-004 | Defines BLK-pipe V47 and validation profile boundaries. | Go BLK-pipe remains final mutation enforcement; this sprint does not run BLK-pipe or grant broader validation shell authority. |
| BLK-005 | Defines requirement/use-case trace binding and canonical hashes. | Index records may cite docs and authority surfaces; they do not generate RTM coverage, drift decisions, or protected-body hash comparison. |
| BLK-006 | Defines protected-vault hard-deny and Discord/HITL authorization. | Protected-vault body reads and writes remain denied; no tactical worker receives protected-body access from this sprint. |
| BLK-058 | Defines the Kuronode TypeScript tactical standard. | Under BLK-078 it is a Layer C target-profile source for future approved work only, not current Kuronode dispatch or mutation authority. |
| BLK-077 | Active post-078 roadmap selector. | Controls next-work selection after BLK-SYSTEM-078 and routes future target-standard work through BLK-078. |
| BLK-078 | Tactical-standard/profile architecture. | Adds Layer A/B/C vocabulary; does not authorize target scans, mutation, runtime tooling, or execution. |

---

## 3. Exact Scope and File Allowlist

### Planning and outcome docs

```text
docs/plans/blk-system-079_post-078-current-state-authority-index-refresh.md
docs/outcomes/BLK-SYSTEM-079_task-000-outcome.md
docs/outcomes/BLK-SYSTEM-079_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-079_task-002-outcome.md
docs/reviews/BLK-SYSTEM-079_hostile-review.md
docs/outcomes/BLK-SYSTEM-079_sprint-closeout.md
```

### Current-state doctrine docs

```text
docs/BLK-046_blk-system-current-state-authority-index.md
docs/BLK-077_blk-system-post-078-roadmap.md
docs/BLK-079_post-078-current-state-authority-index.md
```

### Deterministic local gates/fixtures

```text
python/blk_current_state_authority_index.py
python/test_blk_current_state_authority_index.py
python/test_active_doctrine_review_gates.py
```

No other files are in scope without a new human decision.

---

## 4. Explicitly Forbidden

This sprint does not authorize or perform:

- BEB dispatch or BEO closeout execution;
- Kuronode source or Git mutation;
- target-repo scans, package-manager commands, browser automation, network/model-service calls, cyber tooling, or TypeScript tooling;
- live Codex execution, Codex subprocess startup, or live tactical LLM dispatch;
- BLK-pipe execution or source mutation outside exact approved allowlists;
- production/generic BLK-test MCP or reusable BLK-test service startup;
- arbitrary shell as BLK-test behavior;
- source or Git mutation by BLK-test;
- protected BLK-req vault body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison;
- authoritative BEO publication, runtime `PUBLISHED` output, signer/storage/ledger/rollback/revocation/supersession/release authority;
- runtime RTM generation, RTM drift rejection, public ledger mutation, active-vault hash comparison, or coverage-matrix authority;
- production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claims.

---

## 5. Required Current-State Refresh Contract

The refreshed index must:

1. identify `docs/BLK-077_blk-system-post-078-roadmap.md` as the active roadmap selector;
2. identify `docs/BLK-078_tactical-standard-profile-architecture.md` as the tactical-standard/profile architecture anchor;
3. identify `docs/BLK-079_post-078-current-state-authority-index.md` as superseding BLK-046 for post-078 current-state indexing;
4. keep BLK-046 in history with a supersession notice rather than deleting it;
5. include a deterministic current-state fixture with strict schema validation and fail-closed authority-laundering rejection;
6. add explicit surfaces for BLK-078 profile architecture and BLK-058 Kuronode TypeScript profile source;
7. force every denied authority flag to `False` even when evaluating blocked records;
8. reject natural-language authority laundering in allowed strings and governing-doc lists;
9. update BLK-077 only as roadmap/status alignment, not as runtime authority;
10. make BLK-SYSTEM-080 the next default non-runtime architecture-development sprint after BLK-SYSTEM-079 closes.

---

## 6. Task Plan

### Task 000 — Plan publication

- Write this plan.
- Write `docs/outcomes/BLK-SYSTEM-079_task-000-outcome.md`.
- Verify markdown fences and `git diff --check` for exact plan paths.
- Commit and push the plan publication.

### Task 001 — RED/GREEN current-state index fixture refresh

- Add failing tests first in `python/test_blk_current_state_authority_index.py` requiring:
  - `roadmap_source == "BLK-077"`;
  - governing docs include BLK-077 and BLK-078 where relevant;
  - `EXPECTED_SURFACES` includes `BLK-078 tactical standard profile architecture` and `BLK-058 Kuronode TypeScript tactical profile source` exactly once;
  - BLK-058 is constrained as future approved Layer C input, not dispatch authority;
  - natural-language and governing-doc laundering still fail closed.
- Run the focused test and capture RED failure.
- Patch `python/blk_current_state_authority_index.py` minimally to satisfy the post-078 contract.
- Rerun focused tests for GREEN.
- Write `docs/outcomes/BLK-SYSTEM-079_task-001-outcome.md`.
- Commit and push exact paths.

### Task 002 — Doctrine document refresh and persistent active gate

- Add a failing active-doctrine gate in `python/test_active_doctrine_review_gates.py` requiring post-078 markers in BLK-079, BLK-046 supersession text, and BLK-077 post-079 next-sprint alignment.
- Run the focused gate and capture RED failure.
- Create `docs/BLK-079_post-078-current-state-authority-index.md`.
- Patch `docs/BLK-046_blk-system-current-state-authority-index.md` with a top supersession notice to BLK-079 and BLK-077/078.
- Patch `docs/BLK-077_blk-system-post-078-roadmap.md` so current-state documentation references BLK-079 and the default next sprint after this sprint is BLK-SYSTEM-080.
- Rerun focused gates and current-state fixture tests for GREEN.
- Write `docs/outcomes/BLK-SYSTEM-079_task-002-outcome.md`.
- Commit and push exact paths.

### Task 003 — Hostile review and closeout

- Review all changed paths for file-boundary drift, stale BLK-045/046 authority leakage, runtime-authority laundering, and BLK-058/078 scope confusion.
- Run full verification:
  - `git diff --check` for exact changed paths;
  - markdown fence balance for new/changed markdown;
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'`;
  - `go test ./...`;
  - `go vet ./...`.
- Write `docs/reviews/BLK-SYSTEM-079_hostile-review.md`.
- Write `docs/outcomes/BLK-SYSTEM-079_sprint-closeout.md`.
- Commit and push exact paths.

---

## 7. Definition of Done

- Plan, task outcomes, hostile review, and sprint closeout are committed and pushed.
- BLK-079 exists and supersedes BLK-046 for post-078 current-state authority indexing.
- BLK-046 remains retained as historical lineage with a clear supersession notice.
- BLK-077 points future default planning to BLK-SYSTEM-080 after BLK-SYSTEM-079 closes.
- Current-state fixture and active doctrine gates pass with BLK-077/078/079 markers.
- Full Python unittest discovery, Go tests, Go vet, markdown fence checks, and `git diff --check` pass.
- No forbidden runtime, target-repo, publication, RTM, protected-body, tooling, or production-isolation authority is granted or implied.
