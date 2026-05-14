# BLK-077 — BLK-System Lean Production Roadmap

**Status:** Active lean roadmap guidance — not sprint authority and not runtime authority
**Date:** 2026-05-15T07:30:10+10:00
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
BLK_SYSTEM_127_METADATA_BOUND_BEO_PUBLICATION_PREREQUISITE_REQUEST_COMPLETE
METADATA_BOUND_BEO_PUBLICATION_PREREQUISITE_REQUEST_READY_NOT_GRANTED
BEO-PUBLICATION-PREREQUISITE-REQUEST-127-001
BLK_SYSTEM_126_BEO_PUBLICATION_PATH_DECISION_GATE_COMPLETE
BEO_PUBLICATION_PATH_DECISION_GATE_REVIEW_ONLY_BY_126
BLK_SYSTEM_125_BEB_BEO_METADATA_HANDOFF_COMPLETE
EXACT_BLK_REQ_TRACE_METADATA_HANDOFF_COMPLETE_BY_125
BEB_BEO_METADATA_HANDOFF_NO_PROTECTED_BODY_COPY_BY_125
NEXT_FRONTIER_EXTERNAL_BEO_PUBLICATION_APPROVAL_CAPTURE_PLANNING_NOT_EXECUTION_AUTHORITY
BLK_TEST_FUNCTIONAL_MODULE_NOT_BLK_SYSTEM_TEST_SUITE_PINNED
```

BLK-SYSTEM-125 closed the metadata handoff frontier by requiring BEB/BEO-facing trace metadata to carry exact `REQ-###` / `UC-###` IDs and canonical `version_hash` values only.

BLK-SYSTEM-126 closed the BEO publication path decision gate by binding the BLK-SYSTEM-125 metadata interface through exact IDs and canonical hash.

BLK-SYSTEM-127 closed the metadata-bound prerequisite request by packaging the metadata interface and decision gate into `BEO-PUBLICATION-PREREQUISITE-REQUEST-127-001` for future approval-capture review only.

BLK-test remains a BLK-System functional module, not the BLK-System test suite. BLK-test evidence is evidence only; it does not grant source mutation, BEO publication, RTM, coverage, drift, or production MCP authority.

---

## 3. Active Next Frontier

**Next production-driving frontier:** external BEO publication approval capture.

Required scope:

- consume `BEO-PUBLICATION-PREREQUISITE-REQUEST-127-001` by exact ID and canonical hash only;
- capture or reject a human decision for the exact request package;
- preserve `NOT_PUBLISHED` / record-only boundaries unless the user explicitly approves a separate execution rung;
- never copy protected requirement/use-case body text into publication-path metadata;
- close with one sprint outcome and no new BLK document unless a durable interface/contract is created.

Stop conditions:

- any BEO publication execution, signer/storage/ledger behavior, rollback/revocation/supersession, RTM generation, drift rejection, BLK-pipe runtime, BLK-test runtime, live Codex, target-repo mutation, or protected-body copy request;
- any proposal to infer publication execution authority from the request package, prior record-only outputs, or operator shorthand;
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

1. **External BEO publication approval capture** — current frontier; exact request-bound human decision capture, not publication execution.
2. **External BEO publication execution record** — only after a separate explicit human decision, exact IDs, replay controls, and signer/storage/ledger false-side-effect policy.
3. **Production `blk-link` / RTM trace closure** — only after publication prerequisites are real, not inferred from local evidence.

Operational hardening may interrupt the queue only when it removes a current production blocker or fixes an authority leak.

---

## 6. Documentation Stop / Split Rules

Split or stop a proposed sprint when it tries to combine unrelated authority rungs, create a BLK document without durable future value, create per-task outcome docs, or update BLK-001 through BLK-006 with current-state text.

A sprint is sufficiently documented when code/tests/docs are verified and the single sprint closeout explains what changed, what was tested, and what remains unauthorized.
