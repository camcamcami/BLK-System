# BLK-045 — BLK-System Post-042 Roadmap

**Status:** Active roadmap guidance — supersedes BLK-024 for post-BLK-SYSTEM-042 planning; not sprint authority
**Date:** 2026-05-09T18:34:39+10:00
**Purpose:** Provide the current BLK-System roadmap after BLK-SYSTEM-042, correcting BLK-024's post-Sprint-019 baseline and shifting future work from open-ended safety scaffolding toward selective, explicitly approved runtime activation or V-model completion.
**Scope:** Strategic sequencing, authority cutlines, maturity assessment, and candidate sprint directions. This document is not a sprint plan, not an execution brief, and not a grant of runtime authority.

---

## 0. Supersession Notice

BLK-045 supersedes `docs/BLK-024_blk-system-development-roadmap.md` for current roadmap selection after BLK-SYSTEM-042.

BLK-024 remains retained as historical post-BLK-SYSTEM-019 roadmap context and as lineage for the BLK-024 maturity vocabulary. Where BLK-024 and BLK-045 conflict about current state, near-term sequencing, or recommended next work, BLK-045 is controlling.

BLK-045 does not supersede or weaken the active authority boundaries in BLK-001 through BLK-006 or BLK-025 through BLK-044. Those documents remain active within their scoped authority surfaces unless a later BLK document explicitly changes them.

---

## 1. Non-Execution and Non-Authority Boundary

BLK-045 is roadmap guidance only. It does not authorize:

- live Codex execution;
- reusable live tactical LLM dispatch;
- new BLK-pipe execution runs outside separately approved sprint payloads;
- production BLK-test MCP;
- arbitrary shell as BLK-test behavior;
- source mutation outside exact approved allowlists;
- protected BLK-req vault body reads, copying, parsing, hashing, summarizing, scanning, or mutation;
- authoritative BEO publication;
- runtime RTM generation beyond already-fixtured/offline local evidence boundaries;
- RTM drift rejection authority;
- public ledger mutation;
- signer, storage, rollback, revocation, supersession, or release authority;
- package-manager, network, model-service, browser, or cyber tooling authority;
- production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, network-firewall, or host-secret-isolation claims.

Every candidate below still requires a later explicit sprint plan, deterministic RED/GREEN evidence, hostile review, exact file boundaries, and separate human approval where the maturity rung requires it.

---

## 2. Baseline After BLK-SYSTEM-042

BLK-System is no longer early-stage doctrine only. It is a guarded autonomy platform with strong safety rails and several fixture/pilot ladders, but it is not yet the full production autonomous V-model described by BLK-001.

### 2.1 Completed foundation since BLK-024

BLK-024 was written after BLK-SYSTEM-019. Since then, the system completed major tracks:

1. **Validation and adapter hardening**
   - BLK-SYSTEM-020 introduced repository-owned validation profiles.
   - BLK-SYSTEM-021 hardened Python adapter policy while preserving Go `blk-pipe` as final authority.
2. **BLK-test readiness and observability**
   - BLK-SYSTEM-022 defined BLK-test pilot-readiness boundaries.
   - BLK-SYSTEM-028 through BLK-SYSTEM-037 built operator observability, advisory health checks, isolated workspace handling, Git metadata fixtures, and bounded escalation packages.
3. **BEO / RTM fixture bridge**
   - BLK-SYSTEM-023 through BLK-SYSTEM-027 created BEO publication-candidate, published-BEO input, active-vault hash metadata, RTM hash path, and RTM readiness proposal fixtures.
   - BLK-SYSTEM-030 implemented deterministic offline RTM ledger fixture generation under BLK-033, without runtime drift rejection or protected-body reads.
4. **Codex live-dispatch authority ladder**
   - BLK-SYSTEM-038 / BLK-040: deterministic Codex invocation profile fixture.
   - BLK-SYSTEM-039 / BLK-041: deterministic dispatch envelope fixture.
   - BLK-SYSTEM-040 / BLK-042: live-dispatch readiness gate fixture.
   - BLK-SYSTEM-041 / BLK-043: authority-request package plus disabled adapter fixture.
   - BLK-SYSTEM-042 / BLK-044: execution-authority design gate fixture.

### 2.2 Current maturity map

| Area | Current maturity after BLK-SYSTEM-042 | Current authority cutline |
| --- | --- | --- |
| BLK-req legislative gateway | L0/L1 doctrine and fixtures with protected-vault hard-deny semantics | No tactical write access to active/staging/protected BLK-req bodies. No protected body reads by BLK-test, BEO, RTM, Codex, or fixture helpers. |
| BLK-pipe blast shield | Strong local guarded execution surface; validation profiles and Python adapter preflight are mature | Go remains final enforcement authority. Less-trusted/autonomous payloads must not inherit arbitrary shell or broad file authority. |
| Validation profiles | Mature repository-owned command profiles for local guarded operation | Profiles reduce shell-shaped ambiguity but do not grant production BLK-test or arbitrary shell authority. |
| Python adapter layer | Fail-fast convenience layer | Python checks reduce operator mistakes but never replace Go `blk-pipe` enforcement. |
| BLK-test | Disabled/gated with one historical synthetic fixed-tool smoke and design/pilot-readiness boundaries | Generic/production BLK-test MCP remains disabled. BLK-test returns evidence only and must not mutate source, publish BEOs, generate RTMs, or read protected bodies. |
| Operator health / observability | Local fixed-profile advisory pilot is comparatively mature | PASS is advisory only. No L5 production health-check authority or broad command runner exists. |
| BEO publication path | Deterministic local candidate/input fixtures | No authoritative BEO publication, live publication approval capture, signer/storage/ledger/rollback authority, or runtime `PUBLISHED` output. |
| RTM / BLK-link | Hash-only path fixtures and offline RTM ledger fixture generation exist | No protected-body reads, no runtime drift rejection, no public ledger mutation, and no production trace-closure authority. |
| Codex live-dispatch ladder | Review-ready design/request/disabled-adapter fixtures are mature | No live Codex execution, no Codex subprocess start, no BLK-pipe dispatch from the Codex adapter, and no execution authority from BLK-044. |

---

## 3. Roadmap Thesis From Here

The system should stop treating more preparatory scaffolding as the default next step.

The safety cage is now substantial. Future work should be selected by one of two explicit intents:

1. **Activation intent:** turn exactly one bounded runtime path on under a narrow approval envelope.
2. **Completion intent:** finish one missing V-model organ enough that the end-to-end chain becomes closer to real trace closure.

A sprint that adds another doctrine or fixture rung is still valid only if it removes a concrete blocker for one of those two intents. Otherwise it risks becoming safety work without product progress.

The next phase is not "more rungs forever." The next phase is **controlled activation or controlled completion**.

---

## 4. Recommended Strategic Forks

BLK-045 defines three acceptable near-term forks. The operator should choose one before the next major sprint plan.

### Fork A — Consolidation / Current-State Index

**Use if:** the system feels hard to reason about after many sprints.

**Goal:** Produce a concise current-state authority index and operator map without adding runtime authority.

**Candidate scope:**

- one BLK-System current-state index document linking BLK-001 through BLK-044;
- a machine-checkable summary table of enabled, fixture-only, disabled, and future-authority surfaces;
- stale roadmap/doctrine wording cleanup where it conflicts with BLK-045;
- no new runtime capability.

**Maturity:** L0 doctrine / L1 document gate only.

**Why this is useful:** It reduces cognitive load before activation. It should be one short consolidation sprint, not another long chain.

### Fork B — Codex Live-Dispatch Activation

**Use if:** the next objective is to prove Hermes/Codex can run through the prepared dispatch ladder.

**Goal:** Move from BLK-044 review-only design readiness to one explicitly approved L3 synthetic Codex live-dispatch smoke, then optionally an L4 bounded pilot.

**Required first activation rung:**

- explicit human approval naming live Codex execution as the scope;
- exact approved model and CLI profile;
- exact worktree/branch/path allowlists;
- no protected BLK-req paths;
- no package-manager/network/model/cyber/browser tooling unless separately approved;
- BLK-pipe as the execution gate where source mutation is involved;
- validation profile evidence;
- telemetry artifact persistence;
- process timeout/output caps;
- rollback/revert/cleanup behavior;
- replay/expiry handling;
- operator kill/stop controls;
- hostile review before closeout.

**Maturity:** L3 synthetic smoke first. L4 pilot only after L3 closeout and separate approval.

**Stop condition:** Do not jump directly from BLK-044 to broad reusable live dispatch. BLK-044 is sufficient to request a decision; it is not itself execution permission.

### Fork C — Complete the Right Side of the V-Model

**Use if:** the next objective is trace closure rather than Codex runtime activation.

**Goal:** mature BLK-test, BEO publication, and RTM/blk-link in dependency order.

Recommended order:

1. **BLK-test fixed-tool pilot authority**
   - move from disabled/design and local health pilots toward bounded verification evidence;
   - preserve fixed tools only, no arbitrary shell, no source mutation, no protected body reads.
2. **Authoritative BEO publication authority request**
   - only after verification evidence is trustworthy enough;
   - define signer/storage/ledger/rollback/revocation/supersession authority explicitly.
3. **Runtime RTM / blk-link authority request**
   - only after published BEO input and hash-only active-vault metadata are sufficient;
   - keep drift rejection separate from basic RTM ledger generation.
4. **End-to-end pilot**
   - BEB -> BLK-pipe/Codex or tactical worker -> BLK-test evidence -> BEO -> RTM under separate approvals at each stage.

**Maturity:** L3/L4 progression per component; no L5 production authority until reusable monitoring, rollback, and operator controls are proven.

---

## 5. Recommended Default Path

If the operator wants forward progress with controlled risk, BLK-045 recommends this default sequence:

1. **One short consolidation sprint if needed:** create a current-state authority index and reduce roadmap/doctrine ambiguity after BLK-045.
2. **Choose one runtime frontier, not several:** either Codex live-dispatch L3 smoke or BLK-test fixed-tool pilot authority.
3. **If choosing Codex first:** run one synthetic L3 smoke only, then pause for hostile review before any L4 pilot.
4. **If choosing V-model completion first:** mature BLK-test evidence before BEO publication, then RTM/blk-link after BEO publication inputs are real.
5. **Do not pursue BEO publication before verification evidence is trustworthy.** Draft and candidate fixtures are not publication authority.
6. **Do not pursue drift rejection before RTM ledger generation is proven.** Drift rejection is a separate higher authority.

The highest-leverage next step is probably **not** another abstract Codex fixture. It is either:

- a short current-state index so the operator can see the whole system clearly; or
- an explicitly approved L3 runtime smoke for exactly one frontier.

---

## 6. What Is Done Enough For Now

The following surfaces should not receive more preparatory sprints unless a concrete activation blocker is identified:

1. **Codex pre-dispatch evidence shape**
   - BLK-040 through BLK-044 are enough to support a human decision about an L3 live-dispatch smoke request.
2. **Validation profile existence**
   - additional profile work should be tied to a specific sprint need, not generic hardening.
3. **Operator health-check fixture breadth**
   - new health profiles should be added only when they answer a specific operational question.
4. **BEO/RTM fixture packaging**
   - more nested packaging fixtures should stop unless they directly enable publication or RTM authority.

---

## 7. What Is Still Materially Missing

The remaining gaps are real implementation/authority gaps, not mere documentation gaps:

1. **Live Codex execution path**
   - no live Codex subprocess is authorized by BLK-040 through BLK-044;
   - no reusable Codex dispatch service exists;
   - no L3 smoke closeout exists for Codex live dispatch.
2. **Production BLK-test authority**
   - generic BLK-test MCP remains disabled;
   - fixed-tool pilot authority requires explicit approval and physical isolation evidence.
3. **Authoritative BEO publication**
   - no signer/storage/ledger/rollback authority has been granted;
   - publication-candidate fixtures are not publication.
4. **Runtime RTM / drift handling**
   - offline RTM ledger fixtures exist, but runtime trace closure and drift rejection remain separate future authorities;
   - no protected-body read authority should be introduced to solve this.
5. **End-to-end production loop**
   - the full BLK-001 chain is not yet activated as a reusable production system.

---

## 8. Candidate Sprint Selection Rules

A future sprint should be accepted only if it satisfies one of these rules:

1. **Activation rule:** It turns on exactly one bounded runtime capability under explicit approval and keeps every adjacent authority disabled.
2. **Completion rule:** It advances one missing V-model organ toward trace closure without borrowing authority from another organ.
3. **Consolidation rule:** It reduces operator confusion or stale doctrine in a bounded way and avoids adding runtime authority.
4. **Remediation rule:** It fixes a demonstrated hostile-review, test, or doctrine failure.

A future sprint should be rejected or split if it attempts to combine multiple high-authority jumps, such as live Codex dispatch plus production BLK-test plus BEO publication plus RTM generation.

---

## 9. BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-045 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Preserve the V-model separation between BLK-req, planning, tactical execution, BLK-pipe mutation enforcement, BLK-test verification evidence, BEO publication, and blk-link trace closure. |
| BLK-002 — Artifact Lifecycle | Preserve staging, linting, human promotion, active-vault immutability, and protected-vault isolation. |
| BLK-003 — Orchestration Protocol | Preserve human dispatch gates, Layer 2 bounded context, failure ceilings, hostile audit, and no implicit inheritance between execution, testing, publication, and RTM. |
| BLK-004 — BLK-pipe V47 Suite | Preserve Go `blk-pipe` as deterministic final enforcement for mutation, allowlists, validation profile resolution, output caps, cleanup, Git routing, and report evidence. |
| BLK-005 — BLK-Req Specification | Preserve atomic requirements, bounded use cases, immutable IDs, canonical version hashes, and trace binding. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny behavior, no tactical write access, no protected body reads, and Discord/HITL authorization boundaries. |

---

## 10. Updated Stop Conditions

Pause and require hostile review plus human decision if any proposed sprint attempts to:

1. treat review-ready, design-ready, fixture-ready, or disabled-adapter evidence as runtime authority;
2. start Codex without explicit live Codex approval;
3. route Codex into source mutation without BLK-pipe enforcement and exact allowlists;
4. let BLK-test mutate, stage, commit, push, reset, stash, checkout, or revert source;
5. let BLK-test, BEO, RTM, health-check, Codex, or fixture code read protected BLK-req vault bodies;
6. publish authoritative BEOs without separate publication approval and signer/storage/ledger/rollback authority;
7. generate RTM without separate RTM approval and published-BEO/hash-only metadata prerequisites;
8. make RTM drift rejection automatic before drift authority is explicitly granted;
9. replace fixed-tool verification with arbitrary shell;
10. rely on Python adapters as the sole enforcement layer;
11. accept arbitrary validation shell from a less-trusted/autonomous payload boundary;
12. convert missing, malformed, blocked, fatal, transport-error, interrupted, stale, unknown, replayed, or policy-blocked evidence into success;
13. claim production sandbox, firewall, namespace, or host-secret isolation without tests and explicit authority;
14. add another preparatory rung with no named activation/completion/remediation blocker.

---

## 11. Final Roadmap Statement

BLK-System has enough safety scaffolding to make a controlled next decision. The primary question from here is not "what additional fixture can we write?" It is:

```text
Which single authority frontier should be activated or completed next, and under what explicit approval envelope?
```

BLK-045 therefore recommends selective progress:

- consolidate only if the operator needs clarity;
- otherwise activate one narrow L3/L4 frontier;
- keep approvals separate;
- stop at every authority boundary for hostile review;
- preserve BLK-req body isolation throughout.

The intended future is still the BLK-001 autonomous V-model, but BLK-045 changes the mode from broad hardening to deliberate activation.
