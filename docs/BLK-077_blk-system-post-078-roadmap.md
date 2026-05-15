# BLK-077 — BLK-System Lean Production Roadmap

**Status:** Active lean roadmap guidance — not sprint authority and not runtime authority
**Date:** 2026-05-16T09:00:00+10:00
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
4. **Roadmap minimalism.** Keep only current state, active frontier, authority boundary, and stop/split conditions.

---

## 2. Current Production State

```text
BLK_SYSTEM_157_METADATA_BOUND_RTM_GENERATION_DECISION_REQUEST_COMPLETE
METADATA-BOUND-RTM-GENERATION-DECISION-REQUEST-157-001
sha256:ed32e6e86952e0b67fe209115e7dba8fcf2334c218a6efbaeb69a5460cc8d556
upstream_review_hash=sha256:9dcbe35946b9320fc4aaf46cfb31273e38ccf56a49249f7eac91be37278f537e
upstream_reconciliation_record_hash=sha256:1a2e06f4cb0c539f44d55c49b798cc5251d2e9a821f47e8794ccc0719747d026
BLK_SYSTEM_152_AUTHORITATIVE_BEO_PUBLICATION_FINALITY_COMPLETE
sha256:fa661ce760a5df8d8c1d893a8b71b4ccbfa5b882e683e594511aa30984ba09a3
NEXT_FRONTIER_METADATA_BOUND_RTM_GENERATION_APPROVAL_NOT_GRANTED
BLK_TEST_FUNCTIONAL_MODULE_NOT_BLK_SYSTEM_TEST_SUITE_PINNED
```

BLK-SYSTEM-157 produced a request-only package for a future exact operator approval decision on metadata-bound RTM generation. It binds to the clean BLK-SYSTEM-156 post-reconciliation review and BLK-SYSTEM-155 reconciliation record. It grants no approval capture, no run ID, no RTM generation, no production `blk-link`, no drift rejection, no coverage truth, no protected-body access, no runtime tooling, no source/Git mutation, and no signer/storage/ledger reuse.

BLK-test remains a BLK-System functional module, not the BLK-System test suite. BLK-test evidence is evidence only; it does not grant source mutation, RTM, coverage, drift, or production MCP authority.

---

## 3. Active Next Frontier

**Next production-driving frontier:** exact operator approval for metadata-bound RTM generation remains required and not granted.

Permitted scope:

- capture a future exact approval only if the operator explicitly approves the BLK-SYSTEM-157 request;
- use metadata-only IDs and hashes; do not use protected requirement body text;
- preserve denial of drift rejection, coverage truth, reusable production `blk-link`, signer/storage/ledger reuse, runtime tooling, and source/Git mutation unless separately named;
- close future work with one sprint outcome and no new BLK document unless a durable interface/contract is created.

Stop conditions:

- any attempt to treat BLK-SYSTEM-157 request as approval, run-ID reservation, RTM generation, production `blk-link`, drift rejection, coverage truth, or reusable authority;
- any attempt to reuse BLK-SYSTEM-152 signer/storage/ledger authority for another publication or reconciliation run;
- any request to read, copy, parse, hash, scan, summarize, or mutate protected requirement body text;
- any BLK-pipe runtime, BLK-test runtime, live Codex, target-repo mutation, or tooling expansion without a separate exact approval.

---

## 4. Authority Boundaries

This roadmap does not authorize:

- RTM generation, production `blk-link` execution, drift rejection, coverage truth, or active-vault comparison;
- protected BLK-req body reads/copying/parsing/hashing/scanning/mutation;
- reusable BEO publication/signing/storage/ledger authority or future publication runs;
- rollback, revocation, or supersession execution;
- BEB dispatch or BEO closeout execution;
- live Codex or reusable tactical LLM dispatch;
- BLK-pipe runtime execution outside separately approved exact payloads;
- production/generic BLK-test MCP;
- source/Git mutation outside exact allowlists;
- package-manager, network, model-service, browser, cyber tooling, or production-isolation claims.

---

## 5. Minimal Roadmap Queue

1. **Metadata-bound RTM generation approval** — exact operator approval required before any run ID or generation package.
2. **Hardening-only** — available if no production authority path is selected.

---

## 6. Documentation Stop / Split Rules

Split or stop a proposed sprint when it combines unrelated authority rungs, creates a BLK document without durable future value, creates per-task outcome docs, updates BLK-001 through BLK-006 with current-state text, or creates paperwork-only micro-sprints for approval/run-ID bookkeeping that can safely be preflight inside the useful execution package.

A sprint is sufficiently documented when code/tests/docs are verified and the single sprint closeout explains what changed, what was tested, and what remains unauthorized.
