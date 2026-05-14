# BLK-077 — BLK-System Lean Production Roadmap

**Status:** Active lean roadmap guidance — not sprint authority and not runtime authority
**Date:** 2026-05-14T19:11:27+10:00
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

BLK-System uses a lean documentation model:

1. **No BLK-### per sprint.** Create a new BLK document only for a durable architecture contract, authority boundary, schema, component specification, or reusable doctrine.
2. **One sprint outcome.** The default closeout artifact is `docs/outcomes/BLK-SYSTEM-###_sprint-closeout.md`. Per-task outcome documents are retired for new work unless explicitly requested.
3. **Root overview stability.** BLK-001 through BLK-006 are fixed overview docs. They should not receive sprint-current-state updates, completion markers, or roadmap status patches.
4. **Roadmap minimalism.** This roadmap keeps only current state, active next frontier, authority boundaries, and a short production queue. Historical ladders live in outcome/review docs and Git history.

---

## 2. Current Production State

```text
BLK_SYSTEM_124_STAGED_REVISION_PROMOTION_COMPLETE
EXACT_ID_RETRIEVAL_BACKEND_COMPLETE_BY_122
STAGED_REVISION_DRAFTS_WITH_PARENT_HASH_COMPLETE_BY_123
HITL_STAGED_REVISION_PROMOTION_CONCURRENCY_COMPLETE_BY_124
NEXT_FRONTIER_BEB_BEO_METADATA_HANDOFF_HARDENING_PLANNING_NOT_EXECUTION_AUTHORITY
BLK_TEST_FUNCTIONAL_MODULE_NOT_BLK_SYSTEM_TEST_SUITE_PINNED
```

BLK-SYSTEM-122 through BLK-SYSTEM-124 closed the BLK-req revision lifecycle frontier: exact active artifact retrieval, staged revision drafts with parent-hash binding, and HITL approval-bound revision promotion with concurrency checks.

The active gap is now **BEB/BEO metadata handoff hardening**: carry exact BLK-req IDs and version hashes forward as metadata/trace references without copying protected bodies or granting execution/publication authority.

BLK-test remains a BLK-System functional module, not the BLK-System test suite. BLK-test evidence is evidence only; it does not grant source mutation, BEO publication, RTM, coverage, drift, or production MCP authority.

---

## 3. Active Next Frontier

**Next production-driving frontier:** BEB/BEO metadata handoff hardening.

Required scope:

- represent exact BLK-req `REQ-###` / `UC-###` references and version hashes in BEB/BEO metadata fixtures or validators;
- validate that metadata cites exact versions rather than protected body text;
- preserve metadata/trace plumbing only, not BEB dispatch, BEO closeout, publication, signer/storage/ledger, or RTM authority;
- close with one sprint outcome and no new BLK document unless a durable interface/contract is created.

Stop conditions:

- any protected BLK-req body copying outside the BLK-req backend workflow;
- any BEB dispatch, BEO closeout/publication, signer/storage/ledger behavior, RTM generation, drift rejection, BLK-pipe runtime, BLK-test runtime, live Codex, or target-repo mutation request;
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

1. **BEB/BEO metadata handoff hardening** — current frontier; metadata/trace plumbing only.
2. **BEO publication path decision gate** — explicit separate authority decision; no signer/storage/ledger side effects without approval.
3. **Production `blk-link` / RTM trace closure** — only after publication prerequisites are real, not inferred from local evidence.

Operational hardening may interrupt the queue only when it removes a current production blocker or fixes an authority leak.

---

## 6. Documentation Stop / Split Rules

Split or stop a proposed sprint when it tries to combine unrelated authority rungs, create a BLK document without durable future value, create per-task outcome docs, or update BLK-001 through BLK-006 with current-state text.

A sprint is sufficiently documented when code/tests/docs are verified and the single sprint closeout explains what changed, what was tested, and what remains unauthorized.
