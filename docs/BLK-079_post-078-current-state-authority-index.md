# BLK-079 — BLK-System Current-State Authority Index

**Status:** Active lean current-state authority index — not sprint authority and not runtime authority
**Date:** 2026-05-16
**Purpose:** Give the operator the current authority map without replaying sprint history.
**Scope:** Current surfaces, current cutlines, and governing pointers. This document is not a sprint plan, not a BEB, not a BEO, and not a runtime approval. Historical evidence lives in `docs/outcomes/` and Git history.

---

## 1. Lean Index Contract

```text
LEAN_DOCUMENTATION_MODEL_ACTIVE
NO_BLK_DOC_PER_SPRINT
ONE_OUTCOME_PER_SPRINT_NO_TASK_OUTCOME_DOCS
BLK_001_TO_006_FIXED_OVERVIEW_NOT_SPRINT_STATE
LEAN_CURRENT_STATE_INDEX_ACTIVE
NO_SPRINT_BY_SPRINT_LEDGER_IN_ACTIVE_INDEX
CURRENT_STATE_INDEX_GRANTS_NO_LIVE_AUTHORITY
NO_KURONODE_MUTATION_AUTHORITY
BLK_TEST_FUNCTIONAL_MODULE_NOT_BLK_SYSTEM_TEST_SUITE_PINNED
PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN
BLK_SYSTEM_157_METADATA_BOUND_RTM_GENERATION_DECISION_REQUEST_COMPLETE
NEXT_FRONTIER_METADATA_BOUND_RTM_GENERATION_APPROVAL_NOT_GRANTED
```

BLK-079 is a compact current-state map. It intentionally does not carry cumulative sprint-marker chains. If a future sprint needs historical detail, use the single sprint closeouts under `docs/outcomes/`.

---

## 2. Current State

```text
METADATA-BOUND-RTM-GENERATION-DECISION-REQUEST-157-001
sha256:ed32e6e86952e0b67fe209115e7dba8fcf2334c218a6efbaeb69a5460cc8d556
upstream_review_hash=sha256:9dcbe35946b9320fc4aaf46cfb31273e38ccf56a49249f7eac91be37278f537e
upstream_reconciliation_record_hash=sha256:1a2e06f4cb0c539f44d55c49b798cc5251d2e9a821f47e8794ccc0719747d026
NEXT_FRONTIER_METADATA_BOUND_RTM_GENERATION_APPROVAL_NOT_GRANTED
```

Active state: **metadata-bound RTM generation decision request complete**. Exact operator approval for metadata-bound RTM generation remains required and ungranted.

---

## 3. Current Authority Surfaces

| Surface | Current state | Authority cutline |
| --- | --- | --- |
| BLK-req legislative gateway | Metadata-bound prerequisite/request path complete | Protected bodies remain isolated; no protected-body reads, BEO closeout execution, drift rejection, or target/source/Git mutation. |
| BLK-pipe blast shield | Local guarded enforcement | Explicit validation-profile evidence only; no broad dispatch, target/source/Git mutation, tooling expansion, or production isolation. |
| Python adapter layer | Fail-fast convenience layer | Deterministic local packaging only; no BLK-pipe dispatch, Codex execution, source mutation, RTM generation, or protected-body reads. |
| Validation profiles | Repository-owned local profiles | Structured local evidence only; PASS is diagnostic evidence, not runtime, mutation, publication, RTM, tooling, or isolation authority. |
| BLK-test | Disabled/gated evidence only | BLK-test is a BLK-System functional module, not the BLK-System test suite; production MCP remains disabled and evidence grants no adjacent authority. |
| Operator health / observability | Advisory local pilot | Health output is advisory only; PASS is not execution approval, sandbox evidence, BEO/RTM truth, or protected-body authority. |
| Codex live-dispatch ladder | Review-ready, not execution-authorized | No live Codex subprocess, BLK-pipe dispatch, source mutation, package/network/model/browser/cyber tooling, or production-isolation claim. |
| BEO publication path | Authoritative finality complete | BLK-SYSTEM-152 completed one exact signer/storage/ledger finality package. This is not reusable publication authority and does not grant rollback/revocation/supersession, BEO closeout execution, RTM generation, drift rejection, coverage truth, protected-body access, runtime tooling, or target/source/Git mutation. |
| RTM / blk-link | Request-only RTM generation decision package complete | BLK-SYSTEM-157 requested a future exact metadata-bound RTM generation approval decision. No approval capture, no run ID, no RTM generation, no protected-body access, no production `blk-link`, no drift rejection, no coverage truth, no signer/storage/ledger reuse, no runtime tooling, and no target/source/Git mutation is granted. |

---

## 4. Governing Pointers

- Active roadmap: `docs/BLK-077_blk-system-post-078-roadmap.md`
- Executable current-state gate: `python/blk_current_state_authority_index.py`
- RTM generation decision request fixture: `python/metadata_bound_rtm_generation_decision_request.py`
- Post-reconciliation review fixture: `python/post_metadata_rtm_blk_link_reconciliation_review.py`
- Historical sprint evidence: `docs/outcomes/`

---

## 5. Authority Boundary

This index grants no RTM generation, no production `blk-link` execution, no drift rejection, no coverage truth, no active-vault comparison, no protected BLK-req body reads/copying/parsing/hashing/scanning/mutation, no reusable BEO publication/signing/storage/ledger authority, no future publication run, no rollback/revocation/supersession execution, no BEB dispatch, no BEO closeout execution, no live Codex/tactical LLM dispatch, no BLK-pipe runtime beyond an exact approved payload, no production BLK-test MCP, no target/source/Git mutation, no package/network/model/browser/cyber tooling, and no production-isolation claim.

---

## 6. Documentation Burden Guard

BLK-079 should remain short enough to read in one pass. Do not append sprint-by-sprint status chains here. Add current-state deltas only when they affect operator selection; otherwise record evidence in the single sprint closeout.
