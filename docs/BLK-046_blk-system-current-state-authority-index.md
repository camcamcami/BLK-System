# BLK-046 — BLK-System Current-State Authority Index

> **Superseded by BLK-079:** `docs/BLK-079_post-078-current-state-authority-index.md` supersedes this document for current-state authority indexing after BLK-SYSTEM-078. BLK-077 controls current roadmap selection after BLK-SYSTEM-078; BLK-078 is the current tactical-standard/profile architecture anchor.

**Status:** Superseded current-state authority index — retained as historical post-042/post-045 lineage; not current roadmap authority, not sprint authority, and not runtime authority
**Date:** 2026-05-09T18:45:13+10:00
**Superseded by:** `docs/BLK-079_post-078-current-state-authority-index.md`
**Purpose:** Provide a historical current-state authority map after BLK-SYSTEM-042 and BLK-045 so the operator can distinguish the older post-042 activation-fork context from the post-078 map.
**Scope:** Historical current authority classification, governing-document links, and operator decision support. This document is not a sprint plan, not an execution brief, not a current roadmap selector, and not a grant of runtime authority.

BLK-046 is retained as historical current-state authority index lineage.

---

## 0. Index Markers

```text
BLK_SYSTEM_CURRENT_STATE_AUTHORITY_INDEX
BLK_045_CURRENT_ROADMAP_CONTROLS_POST_042_SELECTION
CONSOLIDATION_INDEX_ONLY_NO_RUNTIME_AUTHORITY
CURRENT_STATE_INDEX_L0_L1_ONLY
CODEX_LIVE_DISPATCH_REVIEW_READY_NOT_EXECUTION_AUTHORIZED
BLK_TEST_EVIDENCE_ONLY_PRODUCTION_MCP_DISABLED
BEO_PUBLICATION_DISABLED_DRAFT_AND_FIXTURE_ONLY
RTM_RUNTIME_GENERATION_AND_DRIFT_REJECTION_DISABLED
PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN
BLK_PIPE_REMAINS_FINAL_MUTATION_ENFORCEMENT_AUTHORITY
CURRENT_STATE_INDEX_GRANTS_NO_LIVE_AUTHORITY
```

Persistent doctrine gate marker: BLK-SYSTEM-043 pins current-state authority index non-execution scope.

---

## 1. Non-Execution and Non-Authority Boundary

BLK-046 is a consolidation/index document only. It does not authorize:

- live Codex execution;
- reusable live tactical LLM dispatch;
- new BLK-pipe execution runs outside separately approved sprint payloads;
- production BLK-test MCP;
- arbitrary shell as BLK-test behavior;
- source mutation outside exact approved allowlists;
- protected BLK-req vault body reads, copying, parsing, hashing, summarizing, scanning, or mutation;
- authoritative BEO publication;
- runtime RTM generation;
- RTM drift rejection authority;
- public ledger mutation;
- signer, storage, rollback, revocation, supersession, or release authority;
- package-manager, network, model-service, browser, or cyber tooling authority;
- production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, network-firewall, or host-secret-isolation claims.

Operator shorthand:

- No live Codex execution authority.
- No production BLK-test MCP authority.
- No authoritative BEO publication authority.
- No runtime RTM generation authority.
- No RTM drift rejection authority.
- No protected BLK-req body reads.
- No network, model-service, cyber, browser, or package-manager tooling authority.
- No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim.

---

## 2. Roadmap Selection Result

BLK-045 controls current roadmap selection after BLK-SYSTEM-042. BLK-024 remains historical roadmap context and maturity vocabulary lineage.

BLK-045 recommends three acceptable forks:

1. Fork A — Consolidation / Current-State Index.
2. Fork B — Codex Live-Dispatch Activation.
3. Fork C — Complete the Right Side of the V-Model.

The operator request that produced BLK-SYSTEM-043 asked Hermes to evaluate BLK-045, write the next logical sprint plan, and execute all tasks. It did not explicitly grant any live runtime authority. Therefore BLK-SYSTEM-043 follows Fork A.

A later Fork B or Fork C sprint requires separate explicit human approval naming the exact activation frontier, maturity rung, allowed paths, excluded authorities, replay/expiry behavior, rollback behavior, and hostile review criteria.

---

## 3. Current Authority Surface Table

| Surface | Current state | Maturity | Governing documents | Current authority cutline |
| --- | --- | --- | --- | --- |
| BLK-req legislative gateway | Staging/linting/baseline doctrine and protected-vault hard-deny semantics | L0/L1 | BLK-002, BLK-005, BLK-006, BLK-045 | Protected bodies remain isolated. No tactical, BLK-test, BEO, RTM, Codex, health-check, or fixture helper may read/copy/parse/hash/summarize/scan/mutate protected BLK-req bodies. |
| BLK-pipe blast shield | Local guarded mutation enforcement with validation profiles and report evidence | Local guarded enforcement; not broad autonomy | BLK-004, BLK-045 | BLK-pipe remains final mutation enforcement authority. Less-trusted/autonomous boundaries must not use arbitrary validation shell or broad file authority. |
| Python adapter | Fail-fast convenience policy layer | L1/L2-style preflight only | BLK-004, BLK-045 | Adapter checks do not replace Go enforcement and do not create sandbox, network, or host-secret-isolation claims. |
| Validation profiles | Repository-owned local command profiles | Mature local profile support | BLK-004, BLK-045 | Profiles constrain validation commands but do not grant package-manager, network, secret-reading, BLK-test, BEO, RTM, or arbitrary shell authority. |
| BLK-test | Disabled/gated evidence path plus one historical synthetic fixed-tool smoke | Disabled/design plus historical L3 exception | BLK-017, BLK-018, BLK-019, BLK-020, BLK-045 | BLK-test returns evidence only. Production MCP remains disabled. No source mutation, publication, RTM generation, arbitrary shell, or protected body reads. |
| Operator health / observability | Fixed-profile advisory local checks and escalation packages | Advisory pilot | BLK-031 through BLK-039, BLK-045 | PASS is advisory only. Health checks do not become BLK-test verification, execution approval, or production sandbox evidence. |
| Codex live-dispatch ladder | Review-ready design/request/disabled-adapter fixtures | L0/L1/L2-style disabled evidence; no L3 live smoke yet | BLK-040, BLK-041, BLK-042, BLK-043, BLK-044, BLK-045 | Review-ready is not execution-authorized. No live Codex subprocess, BLK-pipe dispatch from Codex adapter, source mutation, package/network/model/cyber/browser tooling, or production isolation authority. |
| BEO publication path | Draft/candidate/input fixtures only | L0/L1 | BLK-014, BLK-016, BLK-021, BLK-022, BLK-026, BLK-028, BLK-045 | Authoritative publication remains disabled. No signer, immutable storage, public ledger, rollback, revocation, supersession, or runtime PUBLISHED output. |
| RTM / blk-link | Hash-only path fixtures and offline local RTM ledger fixture generation | Fixture/offline local evidence only | BLK-023, BLK-027, BLK-029, BLK-030, BLK-033, BLK-045 | Runtime RTM generation and drift rejection remain separate future authorities. No protected-body reads and no public ledger mutation. |

---

## 4. Decision Guidance

Use this index as the operator map before choosing a runtime frontier:

1. If cognitive load is still high, improve index/runbook clarity only; do not add another abstract fixture without a blocker.
2. If choosing Codex activation, request exactly one L3 synthetic live-dispatch smoke with explicit approval and all BLK-045 Fork B constraints.
3. If choosing V-model completion, start with BLK-test fixed-tool pilot authority before BEO publication and RTM/blk-link authority.
4. Do not combine Codex live dispatch, BLK-test pilot authority, BEO publication, RTM generation, and drift rejection in one sprint.
5. Preserve protected BLK-req body isolation regardless of frontier.

---

## 5. BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-046 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Preserve V-model separation and make current activation gaps visible without turning target-state architecture into current authority. |
| BLK-002 — Artifact Lifecycle | Preserve staging, linting, promotion, active-vault immutability, and HITL authority for BLK-req artifacts. |
| BLK-003 — Orchestration Protocol | Preserve human dispatch gates and separate execution, testing, publication, and RTM approvals. |
| BLK-004 — BLK-pipe V47 Suite | Preserve Go BLK-pipe as final enforcement for source mutation and validation profile resolution. |
| BLK-005 — BLK-Req Specification | Preserve canonical trace binding and avoid protected-body leakage. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny semantics and no tactical write/body-read access. |

---

## 6. Stop Conditions

Pause and require hostile review plus human decision if a future sprint attempts to treat this index as approval for live execution, BLK-test production MCP, BEO publication, RTM generation, drift rejection, public ledger mutation, protected-body access, package/network/model/cyber/browser tooling, or production isolation claims.

BLK-046 is a map. It is not the territory, not a dispatch envelope, not a runtime approval, and not a substitute for frontier-specific evidence.
