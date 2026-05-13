# BLK-SYSTEM-096 — Post-095 Local RTM Ladder Reconciliation Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first for maturity vocabulary, then by current selectors `docs/BLK-077_blk-system-post-078-roadmap.md` and `docs/BLK-079_post-078-current-state-authority-index.md`, and by BLK-001 through BLK-006 as applicable.

**Goal:** Reconcile BLK-System current-state surfaces after BLK-SYSTEM-095 consumed the exact local RTM drift-rejection run ID, close the post-local-execution reconciliation marker, and reset the next-frontier decision boundary without granting runtime `blk-link` trace closure or any adjacent authority.
**BLK-024 track:** Track A — Doctrine, alignment, and review gates; Track H — BLK-link offline RTM ledger / maturity level L0/L1 reconciliation and doctrine-gate evidence.
**Architecture:** This is a BLK-System-only reconciliation sprint. It updates active doctrine/current-state documents, the executable current-state index, and persistent tests so future sprint selection sees BLK-SYSTEM-095 as consumed local evidence rather than a pending local execution frontier. It does not execute BLK-pipe, BLK-test, Codex, BEB/BEO, publication, RTM generation, drift rejection, or protected-vault access.
**Tech Stack:** Markdown doctrine docs, Python unittest gates, existing `python/blk_current_state_authority_index.py`.
**Authority boundary:** L0/L1 reconciliation-only. No external authoritative BEO publication, signer/storage/ledger/rollback authority, runtime `PUBLISHED` BEO output, runtime RTM generation, authoritative drift decision, reusable/runtime RTM drift-rejection authority, runtime `blk-link` trace closure, active-vault hash comparison, protected BLK-req body reads/hashing, public ledger mutation, target/source/Git mutation by fixtures, BEB dispatch, BEO closeout execution, BLK-pipe/BLK-test/Codex runtime, package/network/model/browser/cyber tooling, or production-isolation claim.

---

## Current Known State

Captured before plan writing:

```text
2026-05-13T12:58:39+10:00
## main...origin/main
500f7b1 feat: execute exact local rtm drift rejection
```

Live roadmap/current-state evidence:

- `docs/BLK-077_blk-system-post-078-roadmap.md` records BLK-SYSTEM-095 complete and states that candidate frontiers after BLK-SYSTEM-095 include a bounded post-local-execution reconciliation/current-state cleanup sprint if concrete drift is identified.
- `docs/BLK-079_post-078-current-state-authority-index.md` records BLK-SYSTEM-095 as local non-authoritative evidence only.
- `docs/BLK-095_exact-local-rtm-drift-rejection-execution.md` intentionally emitted `POST_LOCAL_RTM_DRIFT_REJECTION_RECONCILIATION_REQUIRED_NOT_RUNTIME_BLK_LINK` as its next required non-runtime step.
- `python/blk_current_state_authority_index.py` contains a BLK-095 surface but no BLK-096 reconciliation surface yet.

Concrete reconciliation trigger:

```text
POST_LOCAL_RTM_DRIFT_REJECTION_RECONCILIATION_REQUIRED_NOT_RUNTIME_BLK_LINK
```

This marker is correct inside BLK-095's local execution artifact, but it should not remain as an unclosed current-state selection marker in BLK-077/BLK-079 once BLK-SYSTEM-096 completes.

---

## BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-SYSTEM-096 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Preserve the separation between BLK-req, Hermes planning, BLK-pipe mutation, BLK-test evidence, BEO publication, and blk-link trace closure. BLK-SYSTEM-095 local evidence is not runtime `blk-link`. |
| BLK-002 — Artifact Lifecycle | Do not read, hash, compare, summarize, or mutate protected BLK-req bodies. Use only existing public doctrine/current-state docs and exact local fixture markers. |
| BLK-003 — Orchestration Protocol | No BEB generation/dispatch, no BLK-pipe invocation, no BLK-test run, and no BEO handoff. This sprint only updates doctrine/index surfaces and tests. |
| BLK-004 — BLK-pipe V47 Suite | Go `blk-pipe` remains final mutation enforcement for any future source mutation. BLK-SYSTEM-096 does not run BLK-pipe or create a source-mutation payload. |
| BLK-005 — BLK-Req Specification | Keep drift semantics separate from authority. Local drift-rejection evidence does not become active-vault comparison, coverage truth, authoritative drift decision, or reusable runtime drift authority. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny behavior and no protected-body reads. The current-state index may cite BLK IDs and fixture IDs but must not inspect active-vault content. |

---

## Tasks

### Task 0 — Publish the plan and plan outcome locally

**Deliverables:**

- `docs/plans/blk-system-096_post-095-local-rtm-ladder-reconciliation.md`
- `docs/outcomes/BLK-SYSTEM-096_task-000-outcome.md`

**Verification:**

- `git diff --check -- docs/plans/blk-system-096_post-095-local-rtm-ladder-reconciliation.md docs/outcomes/BLK-SYSTEM-096_task-000-outcome.md`
- Markdown fence balance check for both files.

### Task 1 — RED doctrine/current-state gates for BLK-SYSTEM-096

Add failing tests before implementation to require:

- `docs/BLK-096_post-095-local-rtm-ladder-reconciliation.md` exists and contains:
  - `BLK_SYSTEM_096_POST_095_LOCAL_RTM_LADDER_RECONCILED`
  - `LOCAL_RTM_DRIFT_REJECTION_EVIDENCE_CONSUMED_NOT_AUTHORITY`
  - `POST_LOCAL_RTM_RECONCILIATION_COMPLETE_NOT_RUNTIME_BLK_LINK`
  - `NEXT_FRONTIER_REQUIRES_EXPLICIT_OPERATOR_DECISION_AFTER_LOCAL_LADDER`
  - `NO_RUNTIME_BLK_LINK_TRACE_CLOSURE_BY_BLK_SYSTEM_096`
- BLK-077 and BLK-079 record BLK-SYSTEM-096 as reconciliation-only and no longer carry the unqualified BLK-095 next-required marker as current selection state.
- `python/blk_current_state_authority_index.py` exposes an exact BLK-096 surface with denied runtime/publication/RTM/protected-body/tooling authorities.
- The current-state scanner blocks runtime trace-closure laundering variants beyond BLK-095's blocker set.

**Expected RED:** focused tests fail because BLK-096 docs/index surfaces do not exist yet.

### Task 2 — GREEN BLK-096 doctrine and executable index implementation

Implement the smallest change that satisfies Task 1:

- Write `docs/BLK-096_post-095-local-rtm-ladder-reconciliation.md` as the authoritative sprint doctrine artifact.
- Update `docs/BLK-077_blk-system-post-078-roadmap.md` with a post-BLK-SYSTEM-096 boundary update and current candidate frontier reset.
- Update `docs/BLK-079_post-078-current-state-authority-index.md` with a post-BLK-SYSTEM-096 current-state update.
- Update `python/blk_current_state_authority_index.py` so the executable index includes the BLK-096 reconciliation surface and stronger trace-closure laundering denial tokens.
- Keep BLK-095's own artifact history intact; do not rewrite BLK-095 evidence to pretend it was born reconciled.

### Task 3 — Hostile review and remediation

Run an adversarial review against the diff for:

- unclosed or ambiguous `required` / `pending` / `candidate` wording after BLK-096;
- local evidence accidentally promoted to runtime `blk-link` trace closure;
- authoritative BEO publication, active-vault comparison, protected-body access, or external ledger side effects being implied by reconciliation prose;
- scanner false negatives for compact/camel/percent-encoded trace-closure and active-vault wording;
- over-broad scanner false positives that reject safe explicit denial language.

Remediate with tests first when blockers are found.

### Task 4 — Outcomes, closeout, and verification

Write:

- `docs/reviews/BLK-SYSTEM-096_hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-096_task-001-outcome.md`
- `docs/outcomes/BLK-SYSTEM-096_task-002-outcome.md`
- `docs/outcomes/BLK-SYSTEM-096_task-003-outcome.md`
- `docs/outcomes/BLK-SYSTEM-096_task-004-outcome.md`
- `docs/outcomes/BLK-SYSTEM-096_sprint-closeout.md`

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_active_doctrine_review_gates python.test_blk_current_state_authority_index
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

Check no repository-local `__pycache__` / `.pyc` artifacts remain.

### Task 5 — Commit, push, and remote verification

Use exact-path staging only. Commit after all verification and closeout artifacts exist. Push to `origin main`, then verify local and remote heads match.

---

## Explicit Non-Authority Statement

BLK-SYSTEM-096 reconciles current-state language after local non-authoritative evidence. It does not authorize production BLK-test MCP, live tactical LLM/Codex execution, BLK-pipe dispatch, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads/copying/parsing/hashing/scanning/mutation, authoritative BEO publication, runtime `PUBLISHED` BEO output, signer/storage/ledger/rollback/release authority, runtime RTM generation, RTM drift rejection authority, authoritative drift decisions, runtime `blk-link` trace closure, active-vault hash comparison, public ledger mutation, target-repo scans or mutation, package-manager/network/model/browser/cyber tooling, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.

---

## Stop Conditions

Pause and split the sprint if any task attempts to:

1. turn BLK-SYSTEM-095 local evidence into authoritative publication, active-vault comparison, authoritative drift truth, runtime `blk-link`, or reusable RTM authority;
2. execute any BEB/BEO, BLK-pipe, BLK-test, Codex, package manager, network, browser, model-service, or cyber tooling path;
3. inspect protected BLK-req vault bodies or active-vault contents;
4. mutate target repositories, source outside the exact BLK-System doc/test/index files listed by this plan, or Git state before final exact-path commit;
5. bundle a BLK-test refresh, Codex smoke, BEO publication runtime, or RTM runtime activation into this reconciliation sprint.
