# BLK-077 — BLK-System Lean Production Roadmap

**Status:** Active lean roadmap guidance — not sprint authority and not runtime authority
**Date:** 2026-05-14T18:38:26+10:00
**Purpose:** Drive BLK-System production forward with the minimum durable documentation needed for safe execution.
**Scope:** Current production sequencing, documentation-burden control, and authority cutlines. This is not a sprint plan, BEB, BEO, or runtime approval.

---

## 1. Lean Documentation Contract

```text
LEAN_DOCUMENTATION_MODEL_ACTIVE
NO_BLK_DOC_PER_SPRINT
ONE_OUTCOME_PER_SPRINT_NO_TASK_OUTCOME_DOCS
BLK_001_TO_006_FIXED_OVERVIEW_NOT_SPRINT_STATE
ROADMAP_OCCAM_PRODUCTION_ONLY
```

BLK-System now uses a lean documentation model:

1. **No BLK-### per sprint.** A new BLK document is justified only for a durable architecture contract, authority boundary, schema, component specification, or reusable doctrine.
2. **One sprint outcome.** The default closeout artifact is `docs/outcomes/BLK-SYSTEM-###_sprint-closeout.md`. Per-task outcome documents are retired for new work unless the user explicitly requests them.
3. **Root overview stability.** BLK-001 through BLK-006 are fixed overview docs. They should not receive sprint-current-state updates, completion markers, or roadmap status patches.
4. **Roadmap minimalism.** This roadmap keeps only current state, active next frontier, authority boundaries, and a short production queue. Historical ladders live in existing outcome/review docs and Git history.

---

## 2. Current Production State

```text
BLK_SYSTEM_120_HITL_BASELINE_PROMOTION_COMPLETE
DISCORD_HITL_APPROVAL_CAPTURED_FOR_NEW_BASELINES
NEW_BASELINE_PROMOTION_WRITES_ACTIVE_VAULT_BY_BACKEND_ONLY
NEXT_FRONTIER_BLK_REQ_STAGED_REVISION_AND_EXACT_ID_RETRIEVAL_PLANNING_NOT_EXECUTION_AUTHORITY
NO_REVISION_OVERWRITE_OR_EXACT_ID_RETRIEVAL_BY_120
BLK_TEST_FUNCTIONAL_MODULE_NOT_BLK_SYSTEM_TEST_SUITE_PINNED
```

BLK-SYSTEM-120 completed HITL approval capture and backend-only new-baseline promotion for BLK-req. The active gap is the next BLK-req production step: staged revision plus exact-ID retrieval. That gap is planning/implementation scope only until separately executed and closed.

BLK-test remains a BLK-System functional module, not the BLK-System test suite. BLK-test evidence is evidence only; it does not grant source mutation, BEO publication, RTM, coverage, drift, or production MCP authority.

---

## 3. Active Next Frontier

**Next production-driving frontier:** BLK-req staged revision and exact-ID retrieval.

Required scope:

- retrieve one active requirement/use-case by exact ID without broad protected-vault scanning;
- support staged revisions with parent-hash concurrency checks;
- preserve backend-only active-vault writes after explicit HITL approval;
- keep protected bodies isolated from trace closure, BEO/RTM, BLK-test, and tactical execution;
- close with one sprint outcome and no new BLK document unless a durable interface/contract is created.

Stop conditions:

- any need for broad active-vault scanning;
- any protected-body use outside BLK-req's own approved backend workflow;
- any BEO publication, RTM generation, drift rejection, BLK-pipe runtime, BLK-test runtime, live Codex, or target-repo mutation request;
- any proposal to create paperwork not needed for production movement.

---

## 4. Authority Boundaries

This roadmap does not authorize:

- BEB writing, BEB dispatch, BEO writing, or BEO closeout execution;
- live Codex or reusable tactical LLM dispatch;
- BLK-pipe runtime execution outside separately approved exact payloads;
- production/generic BLK-test MCP;
- source/Git mutation outside exact allowlists;
- protected BLK-req body reads/copying/parsing/hashing/scanning/mutation outside the approved BLK-req backend path;
- authoritative BEO publication, signer/storage/ledger/rollback behavior, or runtime `PUBLISHED` output;
- RTM generation, production `blk-link`, RTM drift rejection, active-vault hash comparison, coverage truth, or public ledger mutation;
- package-manager, network, model-service, browser, cyber tooling, or production-isolation claims.

---

## 5. Minimal Roadmap Queue

1. **BLK-req staged revision + exact-ID retrieval** — current frontier.
2. **BEB/BEO metadata handoff hardening** — only after BLK-req retrieval/revision is closed and only as metadata/trace plumbing, not publication authority.
3. **BEO publication path** — explicit separate authority decision; no signer/storage/ledger side effects without approval.
4. **Production `blk-link` / RTM trace closure** — only after publication prerequisites are real, not inferred from local evidence.

Operational hardening may interrupt the queue only when it removes a current production blocker or fixes an authority leak.

---

## 6. Documentation Stop / Split Rules

Split or stop a proposed sprint when it tries to combine unrelated authority rungs, create a BLK document without durable future value, create per-task outcome docs, or update BLK-001 through BLK-006 with current-state text.

A sprint is sufficiently documented when code/tests/docs are verified and the single sprint closeout explains what changed, what was tested, and what remains unauthorized.
