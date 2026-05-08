# BLK-SYSTEM-031 — Doctrine Hygiene After BLK-033 Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-doctrine-gate-remediation`, `test-driven-development`, and hostile review skills when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable.

**Goal:** Close the small doctrine-hygiene gaps found after the BLK-033 offline RTM generation review without expanding runtime authority.
**BLK-024 track:** Track A — Doctrine, alignment, and review gates; Track H — BLK-link offline RTM ledger; Track I — Operator UX, observability, and escalation / maturity level L0 doctrine-only with persistent L1 local doctrine gates.
**Architecture:** BLK-SYSTEM-031 patches active doctrine and persistent review gates only. It normalizes BLK-033/BLK-SYSTEM-030 maturity vocabulary to BLK-024's L0-L5 ladder, updates operator runbook vocabulary for the new fixture-generated RTM state, and adds durable sprint-dispatch approval provenance guidance for future authority-bearing sprints. It does not alter runtime helpers, generate new RTM ledgers, read protected bodies, publish BEOs, or authorize drift rejection.
**Tech Stack:** Markdown doctrine/review/outcome docs, Python `unittest` doctrine gates, Git CLI.
**Authority boundary:** Doctrine-only / persistent local gate update. No live tactical LLM execution, no production BLK-test MCP, no protected BLK-req body reads, no active-vault scanning, no authoritative BEO publication, no runtime `PUBLISHED` BEO output, no signer/storage/public-ledger side effects, no RTM generation beyond existing BLK-033 fixture boundary, no RTM drift rejection, no source mutation outside exact approved doctrine/test/outcome allowlists.

---

## 0. Current Known State

- **Date:** 2026-05-08T16:45:36+10:00
- **Branch state:** `## main...origin/main`
- **HEAD:** `4e2f76d fix: harden offline rtm generation fixtures`
- **Remote main:** `4e2f76d54333c6a19d4edb71619be9814ca90afc refs/heads/main`
- **Baseline verification:**
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'` — Ran 431 tests in 6.462s, OK
  - `go test ./...` — PASS
  - `go vet ./...` — PASS
  - `git diff --check` — PASS
- **ID discovery:** `BLK-SYSTEM-031` and `blk-system-031` have no existing plan/outcome collisions. No new root BLK document is needed; this sprint patches existing active doctrine docs.
- **Source review:** Discord hostile review on 2026-05-08 found no Critical/High blockers, but recommended a small doctrine hygiene sprint with three findings: maturity-vocabulary normalization, BLK-031 operator RTM vocabulary update, and future sprint-dispatch approval provenance guidance.

---

## 1. Authority Boundary

This sprint authorizes only doctrine and persistent gate hygiene. It may edit:

- `docs/BLK-024_blk-system-development-roadmap.md`
- `docs/BLK-031_operator-ux-observability-runbook-boundary.md`
- `docs/BLK-033_offline-rtm-generation-boundary.md`
- `docs/plans/blk-system-030_offline-rtm-generation.md`
- `docs/outcomes/BLK-SYSTEM-030_sprint-closeout.md`
- `python/test_active_doctrine_review_gates.py`
- `docs/outcomes/BLK-SYSTEM-031_*`
- `docs/reviews/BLK-SYSTEM-031_*`

This sprint does not authorize Hindsight use, Codex use, live tactical LLM execution, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads/copying/parsing/hashing/mutation, active-vault filesystem scanning, runtime active-vault file comparison, authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, new RTM generation authority beyond existing BLK-033 fixture-only local generation, RTM drift rejection authority, production sandbox/cgroup/VM/network/host-secret isolation claims, package-manager execution, or source mutation outside exact approved allowlists.

---

## 2. BLK-024 Selection Rationale

BLK-024 Track A requires the doctrine set to let a new reader distinguish current runtime authority, design-only doctrine, fixture-only behavior, and future target architecture without tribal knowledge. BLK-024 also says sprint plans must clearly state whether the sprint is doctrine-only, fixture-only, disabled transport, synthetic smoke, pilot, or production authority.

The current BLK-033/BLK-SYSTEM-030 language is safe in substance but uses non-standard maturity wording (`L2-style approved local generation`, `Narrow approved local RTM generation`) that is not a BLK-024 rung. BLK-031 also predates BLK-033 and does not describe the new fixture-generated RTM status. Finally, authority-bearing future sprints need durable sprint-dispatch approval provenance rather than prose-only `current operator message` wording.

---

## 3. BLK-001 Through BLK-006 Alignment

| Governing doc | Relevance | Preserved boundary |
| --- | --- | --- |
| BLK-001 — Master Architecture | Doctrine hygiene touches BLK-link/RTM and operator observability vocabulary. | Keeps BLK-req, BLK-pipe, BLK-test, BEO publication, and blk-link authority separate. |
| BLK-002 — Artifact Lifecycle | Approval provenance guidance intersects HITL audit semantics. | Does not alter staging, linting, promotion, revision, active vault, or canonical hashing mechanics. |
| BLK-003 — Orchestration Protocol | Future sprint approval provenance must not imply dispatch, BLK-pipe invocation, BLK-test startup, or BEO generation. | No BEB/L2 dispatch, retry approval, BLK-test production authority, or failure-ceiling behavior changes. |
| BLK-004 — BLK-pipe V47 Suite | Sprint remains docs/tests only and must avoid broad Git staging. | No BLK-pipe source changes, no validation command authority expansion, no runtime helper changes. |
| BLK-005 — BLK-Req Specification | Trace/RTM vocabulary uses artifact IDs and hashes. | No requirement/use-case body reads, no drift rejection, no active-vault comparison changes. |
| BLK-006 — BLK-Req Implementation Brief | Protected vault hard-deny must remain intact. | No protected-vault body reads, copies, parsing, hashing, summaries, or path scans. |

---

## 4. Planned Tasks

### Task 0 — Publish plan and task-000 outcome

**Goal:** Commit this plan and a task-000 outcome using exact-path staging.

**Files:**

- `docs/plans/blk-system-031_doctrine-hygiene-after-blk033.md`
- `docs/outcomes/BLK-SYSTEM-031_task-000-outcome.md`

**Verification:**

- `git diff --check -- docs/plans/blk-system-031_doctrine-hygiene-after-blk033.md docs/outcomes/BLK-SYSTEM-031_task-000-outcome.md`
- Markdown fence balance check.

**Commit:** `docs: plan blk-system sprint 031 doctrine hygiene`

---

### Task 1 — Normalize BLK-033 / BLK-SYSTEM-030 maturity vocabulary

**Finding:** BLK-033/BLK-SYSTEM-030 use non-standard maturity vocabulary that does not map cleanly to BLK-024.

**Goal:** Patch active docs so BLK-033 and the BLK-SYSTEM-030 plan/closeout clearly say the work is BLK-024 **L1 fixture-only deterministic local RTM ledger fixture generation** from already-supplied dictionaries; it is not L2 disabled transport, L4 pilot runtime, or L5 production authority.

**Files:**

- `python/test_active_doctrine_review_gates.py`
- `docs/BLK-033_offline-rtm-generation-boundary.md`
- `docs/plans/blk-system-030_offline-rtm-generation.md`
- `docs/outcomes/BLK-SYSTEM-030_sprint-closeout.md`
- `docs/outcomes/BLK-SYSTEM-031_task-001-outcome.md`

**TDD gate:** Add a RED doctrine test that fails until the exact L1/no-L2/no-L4/no-L5 markers exist and stale `L2-style approved local generation` / ambiguous `Narrow approved local RTM generation` wording is removed.

**Verification:** focused doctrine gate, full Python suite, Go tests, Go vet, `git diff --check`.

**Commit:** `docs: normalize blk033 maturity vocabulary`

---

### Task 2 — Update BLK-031 operator RTM runbook vocabulary

**Finding:** BLK-031 predates BLK-033 and only describes `RTM_NOT_GENERATED`, so operator vocabulary does not distinguish fixture-generated RTM ledgers from forbidden runtime generation.

**Goal:** Patch BLK-031 with operator-facing vocabulary and runbook guidance for:

1. `RTM_NOT_GENERATED` outside BLK-033;
2. `OFFLINE_RTM_LEDGER_GENERATED_FIXTURE_ONLY` under BLK-033;
3. forbidden live/runtime RTM generation;
4. `DRIFT_REVIEW_REQUIRED_NOT_REJECTED` as human-review-required, not drift rejection.

**Files:**

- `python/test_active_doctrine_review_gates.py`
- `docs/BLK-031_operator-ux-observability-runbook-boundary.md`
- `docs/outcomes/BLK-SYSTEM-031_task-002-outcome.md`

**TDD gate:** Add a RED doctrine test that fails until BLK-031 pins the four operator states and their non-authority boundaries.

**Verification:** focused doctrine gate, full Python suite, Go tests, Go vet, `git diff --check`.

**Commit:** `docs: update operator rtm fixture vocabulary`

---

### Task 3 — Add future sprint-dispatch approval provenance guidance

**Finding:** BLK-SYSTEM-030 plan used prose-only `Current operator message approves...` wording. Runtime fixture approval hashes are strong, but future sprint-dispatch approval provenance should be durable.

**Goal:** Patch BLK-024 operating guidance to require future authority-bearing sprint plans to record sprint-dispatch approval provenance separately from runtime/fixture approvals: source system, operator identity, message/event ID when available, timestamp, exact approved scope, explicit excluded authorities, and a statement that sprint-dispatch approval does not substitute for runtime approval fixtures.

**Files:**

- `python/test_active_doctrine_review_gates.py`
- `docs/BLK-024_blk-system-development-roadmap.md`
- `docs/outcomes/BLK-SYSTEM-031_task-003-outcome.md`

**TDD gate:** Add a RED doctrine test that fails until BLK-024 contains the approval-provenance markers and separates sprint-dispatch approval from runtime/fixture approval.

**Verification:** focused doctrine gate, full Python suite, Go tests, Go vet, `git diff --check`.

**Commit:** `docs: require sprint approval provenance markers`

---

### Task 4 — Hostile review and closeout

**Goal:** Hostile-review the completed doctrine hygiene sprint, prove it introduced no runtime authority expansion, and close out.

**Files:**

- `docs/reviews/BLK-SYSTEM-031_doctrine-hygiene-hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-031_sprint-closeout.md`

**Review checklist:**

- BLK-033 maturity vocabulary is now BLK-024 L1 fixture-only and not L2/L4/L5.
- BLK-031 distinguishes no RTM, fixture RTM, forbidden runtime RTM, and drift-review-not-rejection states.
- BLK-024 requires future sprint approval provenance without granting runtime authority.
- No protected body reads, active-vault scans, BEO publication, new RTM generation authority, drift rejection, BLK-test production authority, Codex/live tactical LLM use, network/model/cyber tooling, or runtime source mutation are introduced.

**Verification:** full Python suite, Go tests, Go vet, markdown fence check, `git diff --check`, clean git status, push verification.

**Commit:** `docs: close blk-system sprint 031 doctrine hygiene`

---

## 5. Final Acceptance Criteria

BLK-SYSTEM-031 is complete only when:

1. all planned docs and gates are patched by RED/GREEN evidence;
2. task outcome docs exist for Tasks 000-003;
3. hostile review and sprint closeout exist;
4. `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'` passes;
5. `go test ./...` passes;
6. `go vet ./...` passes;
7. `git diff --check` passes;
8. commits are exact-path staged and pushed to `origin/main` after each task.
