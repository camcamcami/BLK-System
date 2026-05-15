# BLK-077 — BLK-System Lean Production Roadmap

**Status:** Active lean roadmap guidance — not sprint authority and not runtime authority
**Date:** 2026-05-15T16:44:00+10:00
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

1. **No BLK-### per sprint.** Create a new BLK document only for durable architecture, authority, schema, component, or reusable doctrine.
2. **One sprint outcome.** The default closeout artifact is `docs/outcomes/BLK-SYSTEM-###_sprint-closeout.md`.
3. **Root overview stability.** BLK-001 through BLK-006 are fixed overview docs, not sprint-current-state dashboards.
4. **Roadmap minimalism.** Keep only current state, active next frontier, authority boundary, and stop/split conditions.

---

## 2. Current Production State

```text
BLK_SYSTEM_139_ACTIVE_VAULT_HASH_COMPARISON_APPROVAL_CAPTURE_COMPLETE
ACTIVE_VAULT_HASH_COMPARISON_APPROVAL_CAPTURED_FOR_EXACT_BLK138_REQUEST_NOT_EXECUTED
ACTIVE-VAULT-HASH-COMPARISON-APPROVAL-CAPTURE-139-001
sha256:695ed2b919982566d97b10244dd0b352154afe5b4fe5ea97b84173757fda4bec
APPROVAL-BLK-SYSTEM-138-ACTIVE-VAULT-HASH-COMPARISON-001
RUN-BLK-SYSTEM-140-ACTIVE-VAULT-HASH-COMPARISON-001
BLK_SYSTEM_138_ACTIVE_VAULT_HASH_COMPARISON_AUTHORITY_REQUEST_COMPLETE
ACTIVE-VAULT-HASH-COMPARISON-AUTHORITY-REQUEST-138-001
sha256:8b9e0b1ad6c5cf702ba7537d080f32073929495117f4ba4547f41c40e384d68b
sha256:dfebaad5e0846024044fed87153fbfdb67b7f3222a7fccdda5cfdf9c4db10949
BLK_SYSTEM_137_ACTIVE_VAULT_HASH_COMPARISON_DECISION_PACKAGE_COMPLETE
ACTIVE-VAULT-HASH-COMPARISON-DECISION-137-001
sha256:f9f3b1d596a490ea45172595df760496de8fea87f54be533631c4d4f3e78ff16
BLK_SYSTEM_136_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_POST_EXECUTION_RECONCILIATION_COMPLETE
PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-POST-EXECUTION-RECONCILIATION-136-001
sha256:aff988888bbd0bb630f63a9463e166264cf6ddfa99c0ebbc958a098b4b30c9c4
NEXT_FRONTIER_EXACT_ACTIVE_VAULT_HASH_COMPARISON_EXECUTION_NOT_RUN
BLK_TEST_FUNCTIONAL_MODULE_NOT_BLK_SYSTEM_TEST_SUITE_PINNED
```

BLK-SYSTEM-137 chose metadata/hash-only active-vault comparison as the next narrow capability. BLK-SYSTEM-138 packaged the exact request. BLK-SYSTEM-139 captured exact approval and reserved `RUN-BLK-SYSTEM-140-ACTIVE-VAULT-HASH-COMPARISON-001` without consuming it.

BLK-SYSTEM-139 does not perform active-vault comparison, read/copy/parse/hash/scan protected requirement bodies, generate RTM, reject drift, establish coverage truth, run reusable production `blk-link`, mutate target/source/Git state, run BLK-pipe/BLK-test/Codex/tooling, perform signer/storage/ledger behavior, or claim production isolation.

BLK-test remains a BLK-System functional module, not the BLK-System test suite. BLK-test evidence is evidence only; it does not grant source mutation, BEO publication, RTM, coverage, drift, or production MCP authority.

---

## 3. Active Next Frontier

**Next production-driving frontier:** one exact metadata/hash-only active-vault comparison execution record.

Required scope:

- consume `ACTIVE-VAULT-HASH-COMPARISON-APPROVAL-CAPTURE-139-001` by exact ID and canonical hash only;
- consume only `RUN-BLK-SYSTEM-140-ACTIVE-VAULT-HASH-COMPARISON-001`;
- compare metadata/canonical hashes only, with no protected requirement body reads, body copying, body parsing, body hashing, or body scanning;
- preserve RTM generation, drift rejection, coverage truth, reusable production `blk-link`, signer/storage/ledger behavior, runtime/tooling, and production-isolation false-side-effect policy unless separately authorized;
- close with one sprint outcome and no new BLK document unless a durable interface/contract is created.

Stop conditions:

- any request to read, copy, parse, hash, scan, summarize, or mutate protected requirement body text;
- any attempt to treat metadata/hash comparison approval as RTM generation, drift rejection, coverage truth, reusable production `blk-link`, BEO publication, or protected-body authority;
- any signer/storage/ledger behavior, rollback/revocation/supersession, BLK-pipe runtime, BLK-test runtime, live Codex, target-repo mutation, or tooling expansion;
- any proposal to create paperwork not needed for production movement.

---

## 4. Authority Boundaries

This roadmap does not authorize:

- BEB writing, BEB dispatch, BEO writing, or BEO closeout execution;
- live Codex or reusable tactical LLM dispatch;
- BLK-pipe runtime execution outside separately approved exact payloads;
- production/generic BLK-test MCP;
- source/Git mutation outside exact allowlists;
- protected BLK-req body reads/copying/parsing/hashing/scanning/mutation;
- signer/storage/ledger/rollback behavior or reusable BEO publication authority;
- reusable production `blk-link`, RTM generation, RTM drift rejection, coverage truth, or public ledger mutation;
- package-manager, network, model-service, browser, cyber tooling, or production-isolation claims.

---

## 5. Minimal Roadmap Queue

1. **Exact active-vault hash comparison execution** — current frontier; consume the BLK-139 approval/run ID once and emit record-only evidence.
2. **Post-comparison reconciliation** — decide whether clean comparison evidence unlocks RTM generation, drift handling, or reusable production `blk-link` as the next single frontier.

Operational hardening may interrupt the queue only when it removes a current production blocker or fixes an authority leak.

---

## 6. Documentation Stop / Split Rules

Split or stop a proposed sprint when it tries to combine unrelated authority rungs, create a BLK document without durable future value, create per-task outcome docs, or update BLK-001 through BLK-006 with current-state text.

A sprint is sufficiently documented when code/tests/docs are verified and the single sprint closeout explains what changed, what was tested, and what remains unauthorized.
