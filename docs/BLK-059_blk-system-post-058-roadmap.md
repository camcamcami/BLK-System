# BLK-059 — BLK-System Post-058 Development Roadmap

> **Superseded by BLK-077:** This document is historical post-BLK-SYSTEM-054 / post-BLK-058 roadmap guidance. BLK-077 now controls current roadmap selection after BLK-SYSTEM-078. BLK-059 remains retained for roadmap lineage and authority-boundary history.

**Status:** Superseded roadmap guidance — retained for historical context, not current sprint authority
**Date:** 2026-05-10T15:09:29+10:00
**Superseded by:** `docs/BLK-077_blk-system-post-078-roadmap.md` for post-BLK-SYSTEM-078 roadmap selection
**Purpose:** Provide historical BLK-System roadmap context after the non-disposable BLK-test L4 evidence path, repeatable L4 wrapper cleanup, authoritative BEO publication authority request, and Kuronode TypeScript Power-of-Ten tactical standard.
**Scope:** Historical strategic sequencing, maturity assessment, remaining work scope, candidate sprint frontiers, and authority cutlines. This document is not a sprint plan, not an execution brief, and not a grant of runtime authority.

---

## 0. Supersession Notice

BLK-059 superseded `docs/BLK-045_blk-system-post-042-roadmap.md` for roadmap selection after:

- BLK-SYSTEM-050 — non-disposable L4 exact-target approval envelope;
- BLK-SYSTEM-051 — non-disposable L4 runtime pilot wrapper with safe BLOCKED stale-HEAD evidence;
- BLK-SYSTEM-052 — fresh non-disposable L4 `run_ast_validation` PASS evidence;
- BLK-SYSTEM-053 — repeatable non-disposable L4 approval-envelope wrapper cleanup;
- BLK-SYSTEM-054 — authoritative BEO publication authority request readiness;
- BLK-058 — Kuronode TypeScript Power-of-Ten tactical standard.

BLK-077 now supersedes BLK-059 for current roadmap selection after BLK-SYSTEM-078. BLK-059 remains retained for lineage, not current sprint selection.

BLK-024 remains retained for maturity-model lineage and historical post-BLK-SYSTEM-019 context. BLK-045 remains retained for post-BLK-SYSTEM-042 strategic-fork lineage. Where BLK-024, BLK-045, BLK-059, and BLK-077 conflict about current state, recommended next work, or authority cutlines, BLK-077 is controlling.

BLK-059 did not supersede or weaken BLK-001 through BLK-006. It also did not weaken active boundary documents BLK-047 through BLK-058. Those documents remain authoritative within their scoped surfaces unless a later BLK document explicitly changes them.

---

## 1. Non-Execution and Non-Authority Boundary

BLK-059 is roadmap guidance only. It does not authorize:

- live Codex execution;
- reusable tactical LLM dispatch;
- new `blk-pipe` execution runs outside separately approved sprint payloads;
- production or generic BLK-test MCP;
- reusable BLK-test service startup;
- arbitrary shell as BLK-test behavior;
- any additional L4 non-disposable runtime run;
- source or Git mutation by BLK-test;
- source mutation outside exact approved allowlists;
- protected BLK-req vault body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison;
- authoritative BEO publication;
- runtime `PUBLISHED` BEO output;
- live publication approval capture;
- signer key-material access;
- cryptographic signing;
- immutable storage writes;
- public ledger mutation;
- rollback, revocation, or supersession execution;
- runtime RTM generation;
- RTM drift rejection;
- coverage matrix or coverage-claim promotion;
- active-vault hash comparison;
- package-manager, network, model-service, browser, or cyber tooling authority;
- production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claims.

Every candidate below requires its own sprint plan, deterministic RED/GREEN evidence where implementation is involved, hostile review, exact file boundaries, and separate human approval where the maturity rung requires it.

---

## 2. Baseline After BLK-SYSTEM-054 and BLK-058

BLK-System is now past generic pre-activation scaffolding. It has a meaningful evidence chain and multiple explicit authority request packages, but it is still not a production autonomous V-model.

### 2.1 Completed since BLK-045

1. **Frontier selection and BLK-test L3/L4 ladder**
   - BLK-SYSTEM-044 created the BLK-test fixed-tool pilot authority request under BLK-047.
   - BLK-SYSTEM-045 created the authority-frontier selection gate under BLK-048.
   - BLK-SYSTEM-046 executed an L3 synthetic fixed-tool pilot and preserved L4 as blocked pending exact target approval under BLK-049.
   - BLK-SYSTEM-047 created the L4 real-repo approval boundary/preflight under BLK-050.
   - BLK-SYSTEM-048 executed a disposable real-repo L4 fixed-tool runtime boundary under BLK-051.
   - BLK-SYSTEM-049 created the L4 evidence-trust and non-disposable request gate under BLK-052.
2. **Non-disposable BLK-test L4 evidence path**
   - BLK-SYSTEM-050 created an exact-target approval-envelope readiness gate under BLK-053.
   - BLK-SYSTEM-051 proved stale exact-target drift blocks safely and consumes replay IDs before runtime.
   - BLK-SYSTEM-052 produced one approved non-disposable L4 `run_ast_validation` PASS evidence artifact with no source or `.git` mutation and verified cleanup under BLK-055.
   - BLK-SYSTEM-053 parameterized the L4 runtime wrapper so future fresh approval envelopes can be constructed without reusing consumed IDs or weak nonce/path bindings under BLK-056.
3. **BEO publication authority request**
   - BLK-SYSTEM-054 created a deterministic authoritative BEO publication authority-request package under BLK-057.
   - The positive state is `AUTHORITATIVE_BEO_PUBLICATION_AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_PUBLICATION`.
   - This is request-readiness only and cannot be reused as publication authority.
4. **Kuronode tactical TypeScript standard**
   - BLK-058 formalized the Kuronode TypeScript Power-of-Ten tactical standard.
   - It targets TypeScript/Electron/React/Zustand/parser/renderer code forged for Kuronode through BLK-System.
   - It is doctrine only, not a mechanical validation profile and not live execution authority.

### 2.2 Current maturity map

| Area | Current maturity after BLK-SYSTEM-054 / BLK-058 | Current authority cutline |
| --- | --- | --- |
| BLK-req legislative gateway | L0/L1 doctrine and fixtures with protected-vault hard-deny semantics | No tactical write access to active/staging/protected BLK-req bodies. No protected body reads by BLK-test, BEO, RTM, Codex, or fixture helpers. |
| BLK-pipe blast shield | Mature local guarded execution surface with exact allowlists, validation profiles, output caps, cleanup, Git routing, and report evidence | Go `blk-pipe` remains final enforcement authority. Less-trusted/autonomous payloads must not inherit arbitrary shell or broad file authority. |
| Validation profiles | Repository-owned profile concept exists and is mature for BLK-System local operation | Kuronode-specific TypeScript Power-of-Ten profiles are not yet implemented. Arbitrary validation shell remains forbidden for less-trusted/autonomous boundaries. |
| Python adapter layer | Fail-fast convenience layer | Python checks reduce operator mistakes but never replace Go `blk-pipe` enforcement. |
| BLK-test fixed-tool evidence | One approved non-disposable L4 `run_ast_validation` PASS evidence path exists | Evidence is not production BLK-test MCP, not a reusable BLK-test service, not source mutation authority, and not BEO/RTM authority. Fresh runtime runs require fresh exact approval. |
| BEO publication path | Publication-candidate/input fixtures exist; BLK-057 authority-request package is ready for human review | No actual authoritative BEO publication, no runtime `PUBLISHED` output, no signer/storage/ledger/rollback authority. |
| RTM / blk-link | Hash-only path fixtures and offline RTM ledger fixture generation exist | No runtime RTM generation authority after a real published BEO, no drift rejection authority, no protected-body reads, and no public ledger mutation. |
| Codex live-dispatch ladder | Review-ready design/request/disabled-adapter fixtures are mature | No live Codex execution, no Codex subprocess start, and no execution authority from readiness/design/request documents. |
| Kuronode TypeScript tactical standard | BLK-058 doctrine exists | No static Power-of-Ten gates, no Kuronode validation profile enforcement, and no runtime execution authority are granted by the doctrine alone. |
| Operator health / observability | Local fixed-profile advisory pilots and runbooks are comparatively mature | PASS is advisory only. No L5 production health-check authority or broad command runner exists. |

---

## 3. Roadmap Thesis From Here

The system has enough safety and evidence scaffolding to make targeted progress. Additional doctrine-only work should be accepted only when it removes a concrete blocker.

The current question is no longer "what generic safety rung can we add?" It is:

```text
Which single frontier should be activated, completed, or mechanically gated next, and under what exact approval envelope?
```

BLK-059 recognizes four valid next-frontier intents:

1. **Publication completion intent:** move from BEO publication request-readiness to an exact-target publication approval envelope, and only later to a one-run publication pilot.
2. **Kuronode tactical quality intent:** turn BLK-058 from doctrine into repository-owned static validation profiles and BLK-test checks before broader Kuronode execution.
3. **Codex activation intent:** run one explicitly approved L3 synthetic live-dispatch smoke using the existing Codex ladder.
4. **Trace-closure intent:** after publication authority is resolved, request runtime RTM / blk-link authority without protected-body reads or drift rejection bundling.

A sprint that attempts to combine these frontiers should be split.

---

## 4. Recommended Scope of Remaining Work

### Workstream A — Current doctrine and authority map maintenance

**Scope:** Keep active docs coherent as new frontier documents supersede older roadmap guidance.

Needed work:

1. maintain active doctrine gates for BLK-059 and future roadmap supersession;
2. keep BLK-046 current-state index aligned with BLK-052 through BLK-058 if it is used as an operator dashboard;
3. mark historical roadmap documents as retained lineage rather than current authority;
4. preserve BLK-001 through BLK-006 boundaries in every future sprint.

Do not use this workstream as a substitute for activation/completion progress unless a concrete confusion or stale-doctrine blocker exists.

### Workstream B — Kuronode TypeScript Power-of-Ten mechanical gates

**Scope:** Convert BLK-058 from doctrine into project-owned deterministic validation.

Needed work:

1. define a Kuronode validation-profile contract such as `kuronode-typecheck-strict`, `kuronode-eslint-zero-warning`, and `kuronode-power-of-ten-static`;
2. add static checks for no recursion by default, no `while (true)`, banned `eval` / `new Function`, max function length, unsafe `any` / floating promises where lint tooling supports it, and cleanup markers for IPC/React/worker/JointJS/tree-sitter lifecycles;
3. bind checks to Kuronode TypeScript surfaces, not BLK-System Go/Python internals;
4. keep package-manager or tool-install activity behind separate explicit approval;
5. run first as L1 fixtures and L2 disabled/profile definitions before any L3/L4 Kuronode runtime use.

This is a high-leverage safety hardening path before broader Kuronode implementation sprints.

### Workstream C — BEO publication approval envelope

**Scope:** Decide whether the BLK-057 request-readiness package is sufficient to draft an exact-target authoritative BEO publication approval envelope.

Needed work:

1. identify the exact BEO/candidate/evidence bundle to publish;
2. define signer identity without exposing signer key material until separately approved;
3. define immutable storage target and public ledger target;
4. define rollback, revocation, and supersession policy;
5. define one-run approval ID, run ID, expiry, replay protection, output bounds, audit bundle, and operator stop controls;
6. preserve no RTM generation, no drift rejection, no protected-body reads, and no production BLK-test MCP;
7. hostile-review PASS-as-publication, BLK-test-PASS-as-publication, inherited approval, signer/storage/ledger side effects, and protected-path laundering.

Recommended first step: approval-envelope/preflight only, not immediate publication.

### Workstream D — One bounded publication pilot

**Scope:** Only after Workstream C produces an exact approval envelope and the operator grants explicit publication authority, execute one bounded publication pilot.

Needed work:

1. perform exactly one publication against the approved target;
2. bind output to exact BEO hash, evidence hash, operator approval, signer/storage/ledger policies, and audit bundle hash;
3. verify no protected BLK-req body reads and no RTM/drift side effects;
4. record rollback/revocation/supersession readiness without executing those paths unless separately authorized;
5. close out with hostile review and exact evidence.

This is a higher-authority rung than BLK-SYSTEM-054 and must not inherit authority from BLK-057 automatically.

### Workstream E — Runtime RTM / blk-link authority request

**Scope:** Mature trace closure only after actual publication prerequisites are in place.

Needed work:

1. consume a real authorized published-BEO input, not a draft/candidate/request fixture;
2. consume hash-only active-vault metadata without protected body reads;
3. generate a runtime RTM ledger under exact approval;
4. keep drift rejection separate from basic RTM ledger generation;
5. prevent coverage matrices or coverage claims from laundering publication or drift authority;
6. preserve public ledger mutation as a separate authority if applicable.

Do not start runtime RTM before BEO publication authority is resolved.

### Workstream F — Codex live-dispatch L3 smoke

**Scope:** If the operator chooses Codex activation instead of V-model completion, use the existing BLK-040 through BLK-044 ladder to run one explicitly approved synthetic L3 smoke.

Needed work:

1. explicit human approval naming live Codex execution;
2. exact model/CLI profile and worktree/path allowlists;
3. BLK-pipe enforcement for any source mutation;
4. no protected BLK-req paths;
5. no network/package-manager/model/browser/cyber tooling unless separately approved;
6. timeout/output/replay/rollback/cleanup controls;
7. hostile review before any L4 Codex pilot.

Do not combine Codex live-dispatch activation with BEO publication or RTM authority in the same sprint.

### Workstream G — Production BLK-test / reusable BLK-test service

**Scope:** Move from fixed-tool evidence toward production BLK-test MCP only if a concrete need justifies it.

Needed work:

1. preserve fixed-tool registry semantics;
2. prove isolation and cleanup against target-repo escape, `.git` mutation, symlink escape, secret exposure, timeout, output flood, and cleanup failure;
3. keep BLK-test evidence-only;
4. deny source/Git mutation by BLK-test;
5. deny BEO publication and RTM generation;
6. require monitoring, operator stop, replay prevention, and bounded tool expansion.

This remains a major authority frontier and should not be treated as a small follow-up to BLK-SYSTEM-052.

---

## 5. Recommended Near-Term Sequence

If the operator wants V-model completion with controlled risk, the recommended sequence is:

1. **BLK-SYSTEM-055 — Authoritative BEO Publication Approval Envelope / Pilot Boundary**
   - L0/L1 approval-envelope/preflight first.
   - No actual publication unless the sprint explicitly includes and receives separate publication authority.
2. **BLK-SYSTEM-056 — Kuronode TypeScript Power-of-Ten Mechanical Gate Fixtures**
   - L1/L2 static validation-profile design and fixture checks derived from BLK-058.
   - No live Codex execution and no package-manager/tool-install authority unless separately approved.
3. **Publication pilot or Kuronode gate pilot, depending on operator priority**
   - If publication approval envelope is accepted, run one exact publication pilot.
   - If Kuronode implementation quality is the blocker, pilot the Power-of-Ten checks on a bounded Kuronode branch/workspace.
4. **Runtime RTM / blk-link authority request**
   - Only after actual published-BEO input exists.
   - Drift rejection remains separate.
5. **End-to-end pilot**
   - BEB/CEB -> BLK-pipe/Codex or tactical worker -> BLK-test evidence -> authoritative BEO -> RTM, with separate approvals at each authority boundary.

If the operator wants Codex activation instead, replace steps 1-3 with exactly one Codex L3 synthetic live-dispatch smoke and pause for hostile review.

---

## 6. What Is Done Enough For Now

The following surfaces should not receive more generic preparatory rungs unless a concrete blocker is identified:

1. **BLK-test non-disposable fixed-tool evidence path**
   - One L4 `run_ast_validation` PASS evidence artifact exists.
   - Future L4 runs need fresh approvals, not more generic wrapper theory.
2. **Non-disposable wrapper parameterization**
   - BLK-SYSTEM-053 removed the known mixed-nonce wart and made future fresh envelopes safer.
3. **BEO publication request-readiness**
   - BLK-SYSTEM-054 is sufficient to support a human decision about the next publication approval-envelope sprint.
4. **Codex request/design fixtures**
   - BLK-040 through BLK-044 remain sufficient for a decision about one L3 live-dispatch smoke.
5. **Kuronode TypeScript coding doctrine**
   - BLK-058 is sufficient as doctrine; the next useful step is mechanical gate implementation, not more prose.

---

## 7. Material Gaps Remaining

The following are still real gaps, not merely documentation gaps:

1. **No actual authoritative BEO publication authority**
   - No signer/storage/ledger/rollback authority has been granted.
   - No runtime `PUBLISHED` BEO output exists.
2. **No runtime RTM / drift authority**
   - Offline fixtures exist, but no runtime trace-closure authority exists after a real published BEO.
   - Drift rejection remains a separate higher authority.
3. **No production BLK-test MCP**
   - Fixed-tool evidence exists, but generic/reusable BLK-test service authority remains disabled.
4. **No live Codex execution**
   - The Codex ladder remains request/design/disabled-adapter readiness, not execution.
5. **No Kuronode Power-of-Ten mechanical enforcement**
   - BLK-058 is doctrine only until validation profiles/static checks are implemented.
6. **No full end-to-end production loop**
   - BLK-001's full target chain is not yet activated as a reusable production system.

---

## 8. Candidate Sprint Selection Rules

A future sprint should be accepted only if it satisfies one rule:

1. **Activation rule:** It turns on exactly one bounded runtime capability under explicit approval and keeps adjacent authorities disabled.
2. **Completion rule:** It advances one missing V-model organ toward trace closure without borrowing authority from another organ.
3. **Mechanical-gate rule:** It converts existing doctrine into deterministic repository-owned checks without adding runtime authority.
4. **Consolidation rule:** It reduces operator confusion or stale doctrine in a bounded way.
5. **Remediation rule:** It fixes a demonstrated hostile-review, test, or doctrine failure.

A future sprint should be rejected or split if it combines multiple authority jumps, such as live Codex dispatch plus production BLK-test plus BEO publication plus RTM generation, or if it uses BLK-058 quality language to launder source mutation or execution authority.

---

## 9. BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-059 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Preserve V-model separation between BLK-req, planning, tactical execution, BLK-pipe mutation enforcement, BLK-test evidence, BEO publication, and blk-link trace closure. |
| BLK-002 — Artifact Lifecycle | Preserve staging, linting, HITL promotion, active-vault immutability, staged revision, and canonical hash promotion. |
| BLK-003 — Orchestration Protocol | Preserve human dispatch gates, Layer 2 bounded context, failure ceilings, hostile audit, and no implicit inheritance between execution, testing, publication, and RTM. |
| BLK-004 — BLK-pipe V47 Suite | Preserve Go `blk-pipe` as deterministic final enforcement for mutation, allowlists, validation profile resolution, output caps, cleanup, Git routing, and report evidence. |
| BLK-005 — BLK-Req Specification | Preserve atomic requirements, bounded use cases, immutable IDs, canonical version hashes, trace binding, and drift semantics without granting drift rejection prematurely. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny behavior, no tactical write access, no protected body reads, and Discord/HITL authorization boundaries. |

---

## 10. Updated Stop Conditions

Pause and require hostile review plus human decision if any proposed sprint attempts to:

1. treat request-ready, review-ready, design-ready, fixture-ready, or disabled-adapter evidence as runtime authority;
2. reuse consumed BLK-SYSTEM-051 or BLK-SYSTEM-052 approval/run IDs;
3. run another non-disposable L4 pilot without fresh exact target HEAD, workspace, approval ID, run ID, expiry, replay ledger, and operator approval;
4. treat BLK-test PASS evidence as BEO publication, RTM generation, coverage truth, drift truth, or production MCP authority;
5. publish authoritative BEOs without separate publication approval and signer/storage/ledger/rollback authority;
6. generate RTM without separate RTM approval and actual published-BEO/hash-only metadata prerequisites;
7. make RTM drift rejection automatic before drift authority is explicitly granted;
8. start Codex without explicit live Codex approval;
9. route Codex into source mutation without BLK-pipe enforcement and exact allowlists;
10. replace fixed-tool verification with arbitrary shell;
11. accept arbitrary validation shell from a less-trusted/autonomous payload boundary;
12. use BLK-058 to justify live execution, source mutation, package-manager installs, or broad Kuronode authority;
13. let BLK-test, BEO, RTM, health-check, Codex, or fixture code read protected BLK-req vault bodies;
14. claim production sandbox, firewall, namespace, or host-secret isolation without tests and explicit authority;
15. add another preparatory rung with no named activation, completion, mechanical-gate, consolidation, or remediation blocker.

---

## 11. Final Roadmap Statement

BLK-System is now ready for deliberate frontier selection, not more generic scaffolding.

The highest-value next choices are:

```text
A. BEO publication approval envelope / pilot boundary,
B. Kuronode TypeScript Power-of-Ten mechanical gates,
C. one Codex L3 live-dispatch smoke,
D. later runtime RTM / blk-link authority after actual publication prerequisites exist.
```

The default recommendation is **A first if V-model completion is the priority**, with **B as the strongest safety-hardening interlock before broader Kuronode tactical execution**.

All frontier moves must preserve separate approvals, exact scopes, hostile review, replay protection, and protected BLK-req body isolation.
