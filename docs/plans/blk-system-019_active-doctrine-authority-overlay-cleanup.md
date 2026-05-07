# BLK-SYSTEM-019 — Active Doctrine Authority Overlay Cleanup Plan

> **For Hermes:** Use `blk-system-sprint-execution`, `blk-doctrine-gate-remediation`, and `test-driven-development`. Execute task-by-task with strict RED/GREEN evidence, deterministic local review gates, exact-path staging, per-task outcome docs, and push after each task. Do not use Hindsight. Do not run Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, RTM generation, RTM authority, or authoritative BEO publication.

**Goal:** Remediate `BLOCKING-3` from the BLK-001 through BLK-006 hostile alignment review by clarifying active doctrine around the accepted BLK-020 first live fixed-tool smoke evidence contract without broadening runtime authority.

**Architecture:** This is a doctrine-only BLK-System authority-overlay cleanup sprint. It patches active documentation and persistent Python gates so generic/production BLK-test MCP remains disabled while BLK-020's one accepted synthetic first-smoke evidence contract is explicitly acknowledged. It also normalizes stale BEO wording and stale Sprint 014 future-tense references that could confuse future authority routing.

**Tech Stack:** Markdown active doctrine under `docs/BLK-*.md`, Python `unittest` doctrine gates, Go/Python full-suite verification, Git CLI.

---

## 0. Current Known State

Planning preflight captured before drafting this plan:

```text
date -Iseconds              -> 2026-05-07T18:33:37+10:00
git status --short --branch -> ## main...origin/main
HEAD                        -> 1396255 docs: record blk-system sprint 018 closeout hash
```

Source artifacts:

```text
docs/reviews/BLK-SYSTEM_current-implementation_BLK-001-through-BLK-006_hostile-alignment-review.md
docs/outcomes/BLK-SYSTEM-018_sprint-closeout.md
docs/reviews/BLK-SYSTEM-018_post-remediation-hostile-review.md
```

Source finding owned by this sprint:

```text
BLOCKING-3 — Active doctrine contradicts accepted first live fixed-tool BLK-test smoke authority
```

From the source hostile review, the contradiction is narrow:

- `docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md` records one accepted first live fixed-tool BLK-test MCP smoke under explicit human approval, with no production BLK-test MCP authority.
- Older active doctrine still says live BLK-test MCP remains disabled/non-executing without qualifying the one accepted BLK-020 exception.

Findings explicitly not owned by this sprint:

- validation command profile tightening;
- Python adapter policy-layer hardening;
- runtime BLK-test MCP implementation beyond the already accepted BLK-020 evidence contract;
- any new live smoke run;
- authoritative BEO publication;
- RTM generation or RTM drift authority;
- BLK-pipe protected-vault/revert implementation hardening, already closed by BLK-SYSTEM-018.

---

## 1. Scope and Non-Goals

### In scope

1. Add persistent active doctrine gates proving current doctrine acknowledges BLK-020's accepted first-smoke evidence contract while preserving that generic/production BLK-test MCP remains disabled.
2. Patch `docs/BLK-003_blk-pipe-blk-test-orchestration.md` overlays to distinguish:
   - broad live BLK-test MCP authority, still disabled;
   - the one accepted BLK-020 first fixed-tool synthetic smoke evidence contract, already recorded and bounded.
3. Patch `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md` and `docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md` stale future-tense references so they acknowledge BLK-020 without implying production authority.
4. Normalize active BEO wording where current docs could imply BLK-test owns or publishes authoritative BEO generation. The current boundary must remain draft-only/design-only unless a later sprint grants publication authority.
5. Close the sprint with a hostile self-review against BLK-001 through BLK-006, BLK-017 through BLK-023, and the source hostile review.

### Non-goals

This sprint must not implement or authorize:

- new live BLK-test MCP runs;
- production BLK-test MCP;
- live MCP client/server startup beyond the historical BLK-020 evidence record;
- arbitrary shell or new fixed-tool execution;
- source mutation authority for BLK-test;
- BLK-req vault body reads, copying, parsing, hashing, or mutation;
- authoritative BEO publication, public ledger mutation, signer/storage/rollback authority;
- RTM generation, `generate_rtm.py`, runtime `rtm_id`, RTM coverage matrices, or RTM drift rejection;
- validation command profile redesign;
- Python adapter policy hardening;
- Codex, live tactical LLMs, network model services, or cyber tooling.

---

## 2. BLK-001 through BLK-006 Alignment Matrix

| Domain | Required boundary | Sprint 019 treatment |
| --- | --- | --- |
| `blk-req` Legislative Gateway | Protected vault bodies remain isolated; BLK-test must not read or interpret active requirement bodies. | Adds doctrine/gate language preserving no protected-vault body reads in the BLK-020 exception. |
| Architecture & Feature Planning | Hermes owns scoped planning/review and authority interpretation. | Clarifies active doctrine so future planning can distinguish accepted evidence from production authority. |
| `blk-pipe` Blast Shield & Forge | Owns source mutation, Git allowlists, and POSIX routing. | No BLK-pipe code changes. Sprint 018 hardening remains the current implementation boundary. |
| `blk-test` Physics Oracle | May provide bounded verification evidence only within approved authority; must not become source mutator, planner, RTM generator, or BEO publisher. | Clarifies that BLK-020 is a one-run synthetic evidence contract, not production MCP authority. |
| `blk-link` Ledger / RTM | Offline RTM authority remains separate; no hidden RTM generation or drift rejection in BLK-test/BEO docs. | Adds/retains no-RTM-generation and no-RTM-drift-authority markers. |
| Cryptographic baton | `version_hash` / canonical `trace_artifacts` must remain source-bound and opaque. | No trace semantics changes; doctrine gates preserve source-bound BLK-020 evidence language. |

---

## 3. Controller Workflow for Each Task

For each task:

1. Preflight:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   git status --short --branch
   git log -1 --oneline
   ```
2. Read this plan task section and the source review finding it references.
3. Use strict docs-TDD:
   - write or patch the failing gate first;
   - run the focused test and capture RED;
   - patch only named active doctrine/docs;
   - rerun the focused gate and capture GREEN;
   - run shared verification.
4. Shared verification:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
   go test ./...
   go vet ./...
   git diff --check
   ```
5. Remove generated cache before status/staging:
   ```bash
   python3 - <<'PY'
   from pathlib import Path
   import shutil
   for p in [Path('python/__pycache__'), Path('python/.pytest_cache'), Path('.pytest_cache')]:
       if p.exists():
           shutil.rmtree(p)
   PY
   ```
6. Write a task outcome doc under `docs/outcomes/` with RED/GREEN evidence, exact changed paths, full verification, and non-execution statement.
7. Stage exact paths only. Do not use `git add .`, `git add -u`, broad globs, stash, reset, or checkout to manage task files.
8. Verify staged paths:
   ```bash
   git diff --cached --name-only
   ```
9. Commit with the task-specific message.
10. Push to `origin/main` after each task commit.

---

## 4. Task 0 — Commit Sprint Plan

**Objective:** Preserve this sprint plan as an in-repo executable contract before remediation begins.

**Files:**

- Create: `docs/plans/blk-system-019_active-doctrine-authority-overlay-cleanup.md`
- Create: `docs/outcomes/BLK-SYSTEM-019_task-000-outcome.md`

**Steps:**

1. Verify the plan exists and contains required scope markers:
   ```bash
   test -f docs/plans/blk-system-019_active-doctrine-authority-overlay-cleanup.md
   grep -F "BLOCKING-3" docs/plans/blk-system-019_active-doctrine-authority-overlay-cleanup.md
   grep -F "BLK-020" docs/plans/blk-system-019_active-doctrine-authority-overlay-cleanup.md
   grep -F "does not authorize production BLK-test MCP" docs/plans/blk-system-019_active-doctrine-authority-overlay-cleanup.md
   grep -F "does not authorize RTM generation" docs/plans/blk-system-019_active-doctrine-authority-overlay-cleanup.md
   git diff --check
   ```
2. Create `docs/outcomes/BLK-SYSTEM-019_task-000-outcome.md` recording:
   - plan path;
   - source review path;
   - BLK-SYSTEM-018 closeout dependency;
   - preflight status;
   - no implementation change;
   - non-execution statement.
3. Run shared verification.
4. Stage exact files:
   ```bash
   git add docs/plans/blk-system-019_active-doctrine-authority-overlay-cleanup.md \
           docs/outcomes/BLK-SYSTEM-019_task-000-outcome.md
   git diff --cached --name-only
   ```
5. Commit and push:
   ```bash
   git commit -m "docs: plan blk-system sprint 019 authority cleanup"
   git push origin main
   ```

---

## 5. Task 1 — Add RED Gates for BLK-020 Exception Overlay

**Objective:** Prove active doctrine currently lacks an unambiguous BLK-020 exception overlay that distinguishes accepted first-smoke evidence from production BLK-test MCP authority.

**Source finding:** `BLOCKING-3` in `docs/reviews/BLK-SYSTEM_current-implementation_BLK-001-through-BLK-006_hostile-alignment-review.md`.

**Files:**

- Modify: `python/test_active_doctrine_review_gates.py`
- Create: `docs/outcomes/BLK-SYSTEM-019_task-001-outcome.md`

**Gate design:**

Add a focused gate, recommended name:

```text
test_sprint019_blk020_exception_overlay_preserves_disabled_authority
```

Recommended required markers:

For `BLK-003`:

```text
BLK-020 first-smoke evidence contract
single accepted first live fixed-tool smoke exception
generic/production BLK-test MCP remains disabled
no new live BLK-test MCP authority
does not authorize production BLK-test MCP
does not authorize source mutation as BLK-test behavior
does not read protected BLK-req vault bodies
does not authorize authoritative BEO publication
does not authorize RTM generation
```

For `BLK-017`:

```text
BLK-020 first-smoke evidence contract
single accepted first live fixed-tool smoke exception
disabled transport contract remains active for generic startup paths
no new live BLK-test MCP authority
does not authorize production BLK-test MCP
does not authorize authoritative BEO publication
does not authorize RTM generation
```

For `BLK-018`:

```text
BLK-020 records the accepted BLK-SYSTEM-014 first-smoke evidence contract
synthetic isolated workspace
not production BLK-test MCP authority
```

**RED command:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
```

**Expected RED:** missing new Sprint 019 exception-overlay markers in `BLK-003` and `BLK-017`; `BLK-018` may already contain some BLK-020 context but should still be checked for stale future-tense gaps.

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-019_task-001-outcome.md` must record:

- gate name added;
- RED failure excerpt;
- exact source finding;
- no doctrine patched yet;
- non-execution statement.

**Commit:**

```bash
git add python/test_active_doctrine_review_gates.py docs/outcomes/BLK-SYSTEM-019_task-001-outcome.md
git commit -m "test: expose blk020 doctrine overlay gap"
git push origin main
```

---

## 6. Task 2 — Patch BLK-003 Current Boundary for BLK-020 Exception

**Objective:** Patch BLK-003 so Phase 4.2 and escalation/current-boundary language acknowledge BLK-020's accepted first-smoke evidence while preserving that generic/production BLK-test MCP remains disabled.

**Files:**

- Modify: `docs/BLK-003_blk-pipe-blk-test-orchestration.md`
- Modify: `python/test_active_doctrine_review_gates.py` only if Task 1 marker wording needs a narrow adjustment; do not weaken the authority boundary.
- Create: `docs/outcomes/BLK-SYSTEM-019_task-002-outcome.md`

**Patch guidance:**

Patch active overlay sections only, especially:

- `## 0B. Current implementation boundary after Sprint 007`
- `### Phase 4.2 — The Physics Oracle (blk-test Evaluation; Target Architecture)`
- `## 10. Human Escalation Protocol (§10)` current implementation boundary paragraph if needed.

Required doctrine shape:

```text
BLK-020 first-smoke evidence contract records the single accepted first live fixed-tool smoke exception.
The exception is historical/evidence-bound and synthetic; it does not grant generic or production BLK-test MCP authority.
Generic/production BLK-test MCP remains disabled unless a later active doctrine sprint grants broader authority.
The BLK-020 exception does not authorize source mutation as BLK-test behavior, protected BLK-req vault body reads, authoritative BEO publication, RTM generation, or RTM drift rejection authority.
```

**GREEN command:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
```

**Shared verification:** Run full shared verification from §3.

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-019_task-002-outcome.md` must record:

- Task 1 RED reference;
- GREEN focused gate output;
- exact BLK-003 sections patched;
- no-authority-expansion statement;
- shared verification.

**Commit:**

```bash
git add docs/BLK-003_blk-pipe-blk-test-orchestration.md \
        python/test_active_doctrine_review_gates.py \
        docs/outcomes/BLK-SYSTEM-019_task-002-outcome.md
git diff --cached --name-only
git commit -m "docs: clarify blk020 exception in blk003 doctrine"
git push origin main
```

If `python/test_active_doctrine_review_gates.py` is not changed in Task 2, omit it from staging and record the omission rationale in the outcome.

---

## 7. Task 3 — Patch BLK-017 and BLK-018 Future-Tense / Disabled-Authority Overlay

**Objective:** Patch disabled transport and workspace/process active doctrine so BLK-020 is acknowledged as accepted evidence, not future impossible work, while preserving disabled generic startup authority.

**Files:**

- Modify: `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md`
- Modify: `docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md`
- Modify: `python/test_active_doctrine_review_gates.py` only if gate wording needs a narrow adjustment; do not weaken the authority boundary.
- Create: `docs/outcomes/BLK-SYSTEM-019_task-003-outcome.md`

**Patch guidance:**

For `BLK-017` Section 7, replace stale future-only statements such as:

```text
Sprint 014 may only consider first live fixed-tool BLK-test MCP smoke...
Until those later sprints complete...
```

with current-boundary language:

```text
BLK-020 records the single accepted BLK-SYSTEM-014 first-smoke evidence contract. BLK-017 remains the active disabled transport contract for generic startup paths and disabled-by-default behavior. The BLK-020 exception does not authorize production BLK-test MCP, arbitrary tools, source mutation, protected-vault body reads, authoritative BEO publication, RTM generation, or RTM drift authority.
```

For `BLK-018`, patch any remaining future-tense lines around Sprint 014 so they say BLK-020 records the accepted first-smoke evidence contract and future extensions require fresh approval/source evidence.

**GREEN command:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
```

**Shared verification:** Run full shared verification from §3.

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-019_task-003-outcome.md` must record:

- GREEN gate evidence;
- exact BLK-017/BLK-018 sections patched;
- statement that generic/production BLK-test MCP remains disabled;
- shared verification;
- non-execution statement.

**Commit:**

```bash
git add docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md \
        docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md \
        python/test_active_doctrine_review_gates.py \
        docs/outcomes/BLK-SYSTEM-019_task-003-outcome.md
git diff --cached --name-only
git commit -m "docs: align disabled transport doctrine with blk020 evidence"
git push origin main
```

If `python/test_active_doctrine_review_gates.py` is not changed in Task 3, omit it from staging and record the omission rationale in the outcome.

---

## 8. Task 4 — Normalize Active BEO Authority Wording

**Objective:** Remove active doctrine ambiguity that could imply BLK-test publishes or owns authoritative BEO generation today.

**Source risk:** `RISK-3 — BEO generation responsibility remains terminologically muddy in older doctrine` from the source hostile review.

**Files:**

- Modify: `python/test_active_doctrine_review_gates.py`
- Modify: `docs/BLK-001_blk-system-master-architecture.md`
- Modify: `docs/BLK-003_blk-pipe-blk-test-orchestration.md` if needed after Task 2 patches.
- Create: `docs/outcomes/BLK-SYSTEM-019_task-004-outcome.md`

**Gate design:**

Add a focused gate, recommended name:

```text
test_sprint019_beo_authority_wording_is_draft_or_future_only
```

Required markers should prove:

```text
BLK-test returns verification evidence, not authoritative BEO publication authority
draft-only BEO fixture
authoritative BEO publication remains disabled
RTM generation remains disabled
future/offline publication requires later explicit authority
```

**Patch guidance:**

In `BLK-001`, update wording that says `blk-link` cross-references BEOs generated by `blk-test` so the current doctrine says one of:

```text
BEOs are generated only by the authorized execution-outcome/publication path after BLK-test evidence; current BEO handling remains draft-only/design-only until a later publication authority is granted.
```

Do not rewrite historical outcomes or review docs. Patch only active doctrine.

**RED command:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
```

**Expected RED:** missing BEO authority wording in `BLK-001` and/or `BLK-003`.

**GREEN command:** same as RED after doc patches.

**Shared verification:** Run full shared verification from §3.

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-019_task-004-outcome.md` must record:

- RED/GREEN gate evidence;
- exact active doctrine lines/sections patched;
- statement that no BEO publication authority was introduced;
- shared verification.

**Commit:**

```bash
git add python/test_active_doctrine_review_gates.py \
        docs/BLK-001_blk-system-master-architecture.md \
        docs/BLK-003_blk-pipe-blk-test-orchestration.md \
        docs/outcomes/BLK-SYSTEM-019_task-004-outcome.md
git diff --cached --name-only
git commit -m "docs: normalize beo authority wording"
git push origin main
```

If `docs/BLK-003_blk-pipe-blk-test-orchestration.md` needs no additional patch after Task 2, omit it from staging and record the omission rationale.

---

## 9. Task 5 — Sprint Closeout and Hostile Self-Review

**Objective:** Close BLK-SYSTEM-019 with an evidence-backed hostile self-review proving `BLOCKING-3` is remediated without broadening authority.

**Files:**

- Create: `docs/reviews/BLK-SYSTEM-019_post-remediation-hostile-review.md`
- Create: `docs/outcomes/BLK-SYSTEM-019_sprint-closeout.md`

**Hostile self-review requirements:**

`docs/reviews/BLK-SYSTEM-019_post-remediation-hostile-review.md` must verify:

1. BLK-003 acknowledges BLK-020's single accepted first-smoke evidence contract.
2. BLK-017 acknowledges BLK-020 while preserving disabled generic startup authority.
3. BLK-018 contains no stale future-tense contradiction around the already accepted BLK-020 evidence.
4. Generic/production BLK-test MCP remains disabled.
5. No new live smoke run, MCP startup, arbitrary shell, network model service, or cyber tooling was introduced.
6. BLK-test still has no source mutation, staging, commit, push, checkout, reset, stash, or revert authority.
7. Protected BLK-req vault body reads remain forbidden.
8. Authoritative BEO publication remains disabled.
9. RTM generation and RTM drift rejection authority remain disabled.
10. BEO wording in active doctrine is draft-only/future-authority only and does not assign current authoritative BEO publication to BLK-test.

**Closeout requirements:**

`docs/outcomes/BLK-SYSTEM-019_sprint-closeout.md` must include:

- final commit table for Tasks 0-5;
- source review path;
- before/after summary for `BLOCKING-3`;
- note that `RISK-3` BEO wording was normalized if Task 4 lands;
- final verification evidence;
- explicit non-execution statement;
- next-sprint seed for a later hardening candidate, likely validation command profile tightening, unless a higher-priority review supersedes it.

**Final verification commands:**

```bash
export PATH="$HOME/.local/bin:$PATH"
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

**Cleanup/status:**

```bash
python3 - <<'PY'
from pathlib import Path
import shutil
for p in [Path('python/__pycache__'), Path('python/.pytest_cache'), Path('.pytest_cache')]:
    if p.exists():
        shutil.rmtree(p)
PY
git status --short --branch
git diff --cached --name-only
```

**Commit:**

```bash
git add docs/reviews/BLK-SYSTEM-019_post-remediation-hostile-review.md \
        docs/outcomes/BLK-SYSTEM-019_sprint-closeout.md
git diff --cached --name-only
git commit -m "docs: close out blk-system sprint 019"
git push origin main
```

If the closeout needs to record its own landed closeout commit hash, use the Sprint 018 two-commit metadata pattern:

1. commit and push the closeout;
2. patch the closeout to record that landed commit hash;
3. commit and push a metadata update.

---

## 10. Final Sprint Acceptance Criteria

BLK-SYSTEM-019 is complete only when all criteria are true:

1. `BLK-003` acknowledges the BLK-020 single accepted first-smoke evidence contract.
2. `BLK-003` still says generic/production BLK-test MCP remains disabled absent later explicit authority.
3. `BLK-017` acknowledges BLK-020 while preserving disabled transport as the active generic-startup contract.
4. `BLK-018` no longer frames Sprint 014 first-smoke as only future work without acknowledging BLK-020.
5. Persistent Python gates enforce the BLK-020 exception overlay markers.
6. Active doctrine preserves no production BLK-test MCP authority.
7. Active doctrine preserves no source mutation authority for BLK-test.
8. Active doctrine preserves no protected BLK-req vault body reads.
9. Active doctrine preserves no authoritative BEO publication.
10. Active doctrine preserves no RTM generation or RTM drift authority.
11. Active BEO wording no longer implies BLK-test currently owns or publishes authoritative BEO generation.
12. Python unittest discovery passes.
13. `go test ./...` passes.
14. `go vet ./...` passes.
15. `git diff --check` passes.
16. Task outcomes exist for every task.
17. Sprint closeout and hostile self-review exist.
18. All task commits are pushed to `origin/main`.
19. No Codex, live tactical LLMs, network model services, cyber tooling, new live BLK-test MCP run, RTM generation, RTM authority, or authoritative BEO publication was introduced.
20. Follow-up hardening candidates remain separately scoped rather than silently absorbed into this doctrine cleanup sprint.

---

## 11. Quick Resume Prompt for Future Hermes

Open `/home/dad/BLK-System/docs/plans/blk-system-019_active-doctrine-authority-overlay-cleanup.md`. Execute the next incomplete task using `blk-system-sprint-execution`, `blk-doctrine-gate-remediation`, strict docs-TDD, exact-path staging, per-task outcome docs, and push after each task. Source review is `docs/reviews/BLK-SYSTEM_current-implementation_BLK-001-through-BLK-006_hostile-alignment-review.md`; source closeout is `docs/outcomes/BLK-SYSTEM-018_sprint-closeout.md`. Sprint owns only `BLOCKING-3` doctrine contradiction cleanup and BEO wording normalization risk; do not broaden into validation command profile hardening, Python adapter policy hardening, new live BLK-test MCP runs, RTM generation, RTM authority, or authoritative BEO publication.
