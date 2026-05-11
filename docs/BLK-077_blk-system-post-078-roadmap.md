# BLK-077 — BLK-System Post-078 Development Roadmap

**Status:** Active roadmap guidance — supersedes BLK-059 for post-BLK-SYSTEM-078 planning; not sprint authority
**Date:** 2026-05-11T17:58:58+10:00
**Purpose:** Realign BLK-System development after the BLK-SYSTEM-059 through BLK-SYSTEM-078 chain, with explicit alignment to BLK-001 through BLK-006, BLK-058, and BLK-078.
**Scope:** BLK-System development roadmap only. This document governs strategic sequencing, current authority cutlines, and candidate BLK-System sprint frontiers. It is not a Kuronode development plan, not a BEB, not a BEO, not a sprint plan, and not runtime authority.

---

## 0. Supersession Notice

BLK-077 supersedes `docs/BLK-059_blk-system-post-058-roadmap.md` for roadmap selection after BLK-SYSTEM-078.

BLK-059 remains retained as historical roadmap lineage after BLK-SYSTEM-054 / BLK-058. BLK-045 remains retained as post-BLK-SYSTEM-042 strategic-fork lineage. BLK-024 remains retained for maturity-model lineage and historical post-BLK-SYSTEM-019 context.

Where BLK-024, BLK-045, BLK-059, and BLK-077 conflict about current state, recommended next work, or authority cutlines, BLK-077 controls current roadmap selection.

BLK-077 does not supersede or weaken BLK-001 through BLK-006. It also does not weaken BLK-058 or BLK-078.

BLK-078 now clarifies the tactical-standard profile architecture that BLK-077 must consume for roadmap selection: Layer A is BLK-System universal core, Layer B is the universal tactical-output safety standard, and Layer C is configurable target tactical profiles. BLK-058 remains the authoritative Kuronode TypeScript target-profile source under that architecture when BLK-System is separately authorized to govern Kuronode tactical work.

---

## 1. Non-Execution and Non-Authority Boundary

BLK-077 is roadmap guidance only. It does not authorize:

- BEB writing, BEB dispatch, BEO writing, or BEO closeout execution;
- Kuronode feature implementation;
- Kuronode source mutation, Git mutation, staging, commit, push, reset, checkout, revert, stash, cleanup, or autofix;
- live Codex execution;
- reusable tactical LLM dispatch;
- new `blk-pipe` execution runs outside separately approved sprint payloads;
- production or generic BLK-test MCP;
- reusable BLK-test service startup;
- arbitrary shell as BLK-test behavior;
- source or Git mutation by BLK-test;
- source mutation outside exact approved BLK-pipe allowlists;
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

Every candidate below requires its own sprint plan, deterministic evidence where implementation is involved, hostile review, exact file boundaries, and separate human approval where the maturity rung requires it.

---

## 2. Why This Roadmap Exists

BLK-059 correctly identified four frontier intents after BLK-SYSTEM-054 and BLK-058:

1. BEO publication approval envelope / pilot boundary.
2. Kuronode TypeScript Power-of-Ten mechanical gates.
3. One Codex L3 live-dispatch smoke.
4. Later runtime RTM / blk-link authority after publication prerequisites.

Since then, BLK-System completed a long authority-bound chain through BLK-SYSTEM-078. That chain materially changed current state:

- BLK-058's Kuronode tactical TypeScript doctrine was converted into fixture/static-profile artifacts and approval envelopes.
- A static CEB_009 findings/remediation/approval/preflight/authority-request chain was built and hardened.
- Multiple exact-target BLK-pipe and preflight attempts proved drift, dirty-worktree, ignored-artifact, local-head, and target-hash gates.
- A successful exact-target Kuronode patch path was completed for CEB_009-adjacent smoke harness work.
- A read-only BLK-test functional-module pilot against the Kuronode workspace produced valid FAIL evidence.
- That evidence was converted through remediation packet, approval envelope, exact-target patch execution, follow-up smoke blocker remediation, and deterministic smoke seeding.
- Kuronode now has a passing deterministic headless smoke baseline at commit `aebea51bed911c781a537d84d38b2dcb838b1368`.

This does **not** mean BLK-System should now drift into Kuronode product development by default.

The post-078 question is:

```text
What BLK-System capability, boundary, index, or approval envelope should be developed next so future target-repo work remains mechanically governed?
```

BLK-078 answers one newly clarified part of that question: BLK-System should not hardcode Kuronode-specific tactical standards into core. It should support a layered tactical-standard architecture where universal safety constraints are separated from target-specific profiles. BLK-077 is updated to treat that architecture as a roadmap input rather than as runtime or target-work authority.

---

## 3. Baseline After BLK-SYSTEM-078

### 3.1 Completed since BLK-059

1. **Kuronode Power-of-Ten mechanical-gate ladder**
   - BLK-SYSTEM-056 created the fixture-only static profile boundary under BLK-061.
   - BLK-SYSTEM-057 registered a repository-owned fixture self-test validation profile under BLK-062.
   - BLK-SYSTEM-058 created a future human-review gate-pilot approval envelope under BLK-063.
   - BLK-SYSTEM-059 applied the static gate pilot to CEB_009 as fixture/test material only under BLK-064.

2. **CEB_009 remediation and patch authority ladder**
   - BLK-SYSTEM-060 created a remediation packet under BLK-065.
   - BLK-SYSTEM-061 created a review-only patch approval envelope under BLK-066.
   - BLK-SYSTEM-062 hardened envelope integrity under BLK-067.
   - BLK-SYSTEM-063 created a fail-closed execution preflight under BLK-068.
   - BLK-SYSTEM-064 created a patch execution authority-request package under BLK-069.
   - BLK-SYSTEM-065 captured approval but blocked on exact-target drift under BLK-070.
   - BLK-SYSTEM-066 and BLK-SYSTEM-068 consumed authorized attempts but blocked safely before Kuronode patching.
   - BLK-SYSTEM-067 cleaned ignored artifacts under explicit cleanup scope.
   - BLK-SYSTEM-069 added an exact-target local-head gate.
   - BLK-SYSTEM-070 completed a target-hash BLK-pipe patch attempt and produced the local Kuronode patch commit later pushed under approved follow-up handling.

3. **BLK-test Kuronode workspace evidence ladder**
   - BLK-SYSTEM-071 created a read-only BLK-test pilot request under BLK-072.
   - BLK-SYSTEM-072 created an exact-target approval envelope under BLK-073.
   - BLK-SYSTEM-073 executed one approved read-only BLK-test functional-module pilot against the Kuronode workspace under BLK-074.
   - That pilot returned valid evidence, not production BLK-test authority.

4. **Lifecycle cleanup remediation and exact-target patch chain**
   - BLK-SYSTEM-074 created a remediation packet under BLK-075.
   - BLK-SYSTEM-075 created a review-only exact-target patch approval envelope under BLK-076.
   - BLK-SYSTEM-076 executed the exact-target lifecycle cleanup patch and identified a separate preload smoke blocker.
   - BLK-SYSTEM-077 fixed the preload/API and worker path smoke context blocker.
   - BLK-SYSTEM-078 fixed deterministic smoke seeding and closed CEB_009 / CEO_009 documentation in the target repo as part of that previously authorized chain.

### 3.2 Current maturity map

| Area | Current maturity after BLK-SYSTEM-078 | Current authority cutline |
| --- | --- | --- |
| BLK-req legislative gateway | L0/L1 doctrine and fixtures with protected-vault hard-deny semantics | No tactical, BLK-test, BEO, RTM, Codex, health-check, or fixture helper may read/copy/parse/hash/summarize/scan/mutate protected BLK-req bodies. |
| BLK-pipe blast shield | Mature local guarded execution with validation profiles, exact allowlists, output caps, cleanup, Git routing, local target-hash gates, and report evidence | Go `blk-pipe` remains final enforcement authority. It is not generic autonomous permission and does not remove the need for exact human approval. |
| Python adapter layer | Fail-fast convenience layer | Python checks reduce operator mistakes but never replace Go `blk-pipe` enforcement and never prove sandbox/host-secret isolation. |
| Validation profiles | Repository-owned profile concept exists; Kuronode Power-of-Ten fixture/static-profile chain exists | Live Kuronode repository scans, package-manager/tooling execution, and semantic TypeScript analysis still require separate authority. |
| BLK-test fixed-tool evidence | Non-disposable L4 path exists and one read-only Kuronode workspace pilot produced valid evidence | Evidence remains evidence only. No production BLK-test MCP, no source/Git mutation by BLK-test, no BEO/RTM authority. Fresh runs require fresh exact approval. |
| BEO publication path | Request and approval-envelope fixtures exist, including BLK-060 | No actual authoritative BEO publication, no runtime `PUBLISHED` output, no signer/storage/ledger/rollback authority. |
| RTM / blk-link | Hash-only path fixtures and offline RTM fixture generation exist | No runtime RTM generation authority after a real published BEO, no drift rejection authority, no protected-body reads, no public ledger mutation. |
| Codex live-dispatch ladder | Review-ready design/request/disabled-adapter fixtures exist | No live Codex execution, no Codex subprocess start, no execution authority from readiness/design/request documents. |
| BLK-078 tactical standard profile architecture | L0 architecture doctrine exists | BLK-078 separates Layer A BLK-System universal core, Layer B universal tactical-output safety, and Layer C target tactical profiles. No registry, validator, live scan, or runtime authority exists from BLK-078 alone. |
| BLK-058 Kuronode TypeScript tactical standard | Doctrine exists and L1/L2-style fixture/static profile boundary exists | Under BLK-078, BLK-058 is the authoritative `kuronode-typescript` Layer C profile source and a source of Layer B universal-safety candidates. It constrains future approved Kuronode TypeScript work; it does not grant target work. |
| Current-state documentation | BLK-079 supersedes BLK-046 for post-078 current-state indexing; BLK-046 and BLK-059 remain historical lineage | Future sprint selection should use `docs/BLK-079_post-078-current-state-authority-index.md` plus BLK-077/BLK-078, not stale BLK-045/046/059 maps. |

---

## 4. Roadmap Thesis From Here

BLK-System should now develop its own governance organs rather than defaulting to Kuronode feature work.

The post-078 evidence proves that BLK-System can govern an exact-target external-repo patch chain, find reality failures, convert them to remediation packets, request/capture approval, invoke BLK-pipe under target-hash constraints, validate, and close out with hostile review.

That is a BLK-System capability milestone.

The next development question is not "what Kuronode feature should be implemented?" It is:

```text
Which BLK-System organ should be strengthened so future target-repo work is safer, clearer, and less dependent on ad hoc operator memory?
```

Valid answers must satisfy one of these selection rules:

1. **Consolidation rule:** reduce stale roadmap/current-state confusion caused by the post-078 evidence chain.
2. **Mechanical-gate rule:** convert existing doctrine into deterministic repository-owned BLK-System checks or profiles.
3. **Profile-architecture rule:** implement BLK-078 profile-selection records, Layer B universal-safety extraction, Layer C target-profile registration, or denied-authority fixtures without live scans or target mutation.
4. **Approval-envelope rule:** prepare exactly one future authority decision without executing it.
5. **Evidence-refresh rule:** run exactly one separately approved evidence-only check without treating evidence as source, publication, or trace authority.
6. **Activation rule:** turn on exactly one bounded runtime capability under explicit approval while keeping adjacent authorities disabled.

A sprint that attempts to implement Kuronode features, publish BEOs, generate RTM, start Codex, and run BLK-test in one movement must be rejected or split.

---

## 5. Recommended Workstreams

### Workstream A — Current-State Authority Index Refresh

**Scope:** BLK-System documentation and doctrine-gate development only.

Needed work:

1. supersede or refresh BLK-046 so it no longer says BLK-045 controls current roadmap selection;
2. record BLK-077 as current roadmap authority and BLK-078 as tactical-standard/profile architecture authority;
3. update the operator-facing authority map through BLK-SYSTEM-078;
4. preserve all non-authorities: no BEB dispatch or BEO closeout execution, no Kuronode mutation, no runtime BLK-test, no BEO publication, no RTM;
5. add or update persistent doctrine gates if the current-state index is relied upon by future sprint selection.

This is the safest immediate next sprint because it develops BLK-System itself and removes stale operator guidance before any new frontier is selected.

BLK-SYSTEM-079 completed the current-state authority index refresh by publishing `docs/BLK-079_post-078-current-state-authority-index.md`, retaining BLK-046 as historical lineage, and preserving all denied runtime, target-repo, publication, RTM, protected-body, and tooling authorities.

### Workstream B — BLK-System Target-Repo Execution Governance

**Scope:** Define BLK-System rules for future target-repo execution chains without performing target-repo execution.

Needed work:

1. formalize the post-078 exact-target chain as a reusable governance pattern;
2. distinguish request package, approval envelope, preflight refusal, approval capture, BLK-pipe invocation, validation, hostile audit, and target-repo closeout;
3. require exact repo/path/branch/SHA, allowlists, validation profiles, run IDs, approval IDs, expiry, replay policy, and stop conditions;
4. require a BLK-078 profile-selection record whenever a target tactical standard is relevant;
5. preserve Layer A authority boundaries, Layer B universal tactical-output safety constraints, and Layer C target-profile constraints without allowing any layer to grant runtime authority;
6. state that BEB/BEO artifacts are target-repo execution artifacts and are not created or executed unless a future sprint explicitly authorizes them.

This would develop the BLK-System execution doctrine around target repos, not Kuronode product code. BLK-078 should be consumed as the tactical-standard/profile model for this workstream.

BLK-SYSTEM-081 completed the target-repo execution governance pattern by publishing `docs/BLK-081_target-repo-execution-governance-pattern.md`, implementing `python/blk_target_repo_execution_governance.py`, and defining request package, profile selection, approval envelope, preflight refusal, approval capture, BLK-pipe invocation boundary, validation evidence, hostile audit, and target-repo closeout stages while preserving denied runtime, target-repo, publication, RTM, protected-body, tooling, and isolation authorities.

Historical post-081 selector closed by BLK-SYSTEM-082:

```text
BLK-SYSTEM-082 — BLK-058 Mechanical Enforcement Upgrade
```

Target-repo execution governance is now an L0/L1 fixture/doctrine surface. No target-repo scan, no target-repo mutation, no BEB dispatch, and no BEO closeout execution unless a future sprint explicitly authorizes it.

BLK-SYSTEM-082 completed the BLK-058 mechanical enforcement upgrade by publishing `docs/BLK-082_blk058-mechanical-enforcement-upgrade.md`, implementing `python/blk_058_mechanical_enforcement.py`, and adding submitted-snippet fixture checks for selected BLK-058 constraints. After BLK-SYSTEM-082, require explicit operator decision before any higher-authority frontier. BEO Publication Decision Package remains an unselected future L0/L1 alternative. No target-repo scan, no target-repo mutation, no BEB dispatch, no BEO closeout execution, no BEO publication, and no RTM authority is granted.

### Workstream C — BLK-078 Tactical Standard Profile Architecture Implementation

**Scope:** BLK-System profile architecture, registry, fixture, and doctrine-gate development only.

Needed work:

1. extract BLK-078 Layer B universal tactical-output safety principles into a BLK-System-owned standard, fixture shape, or validation-profile contract;
2. define a target tactical profile selection schema or record shape without granting profile-selection runtime authority;
3. register BLK-058 as the first Layer C target profile source for `kuronode-typescript`;
4. map existing BLK-061 and BLK-062 Kuronode static/profile artifacts into the BLK-078 maturity ladder;
5. define fixture-only validators for profile records and denied-authority equality;
6. define a later approval-envelope shape for any bounded live target scan, while preserving no live scan, no target mutation, no package-manager/tool-install authority, and no Codex/BLK-pipe/BLK-test/BEO/RTM authority unless separately approved.

This is useful before broader target-repo execution because it prevents target-specific standards such as BLK-058 from being confused with BLK-System core or target-work authority.

BLK-SYSTEM-080 completed the tactical profile registry / Layer B extraction by publishing `docs/BLK-080_tactical-standard-profile-registry-and-layer-b-extraction.md`, implementing `python/blk_tactical_profile_registry.py`, extracting BLK-078 Layer B principle identifiers, and registering BLK-058 as the first `kuronode-typescript` Layer C source while preserving denied runtime, target-repo, publication, RTM, protected-body, tooling, and isolation authorities.

### Workstream D — BEO Publication Path Completion

**Scope:** Continue the right side of the V-model without borrowing authority from BLK-test or target-repo success.

Needed work:

1. decide whether BLK-060 approval-envelope readiness is sufficient for a publication pilot request;
2. if not, harden the envelope or operator decision package;
3. if yes and explicitly approved later, execute exactly one publication pilot in a separate sprint;
4. preserve no RTM generation, no protected-body reads, no signer key-material leakage, no public ledger mutation unless specifically authorized.

This remains a core BLK-System V-model organ, but it is higher authority than a roadmap/index refresh.

### Workstream E — Runtime RTM / blk-link Authority Request

**Scope:** Trace closure only after actual authorized publication prerequisites exist.

Needed work:

1. consume actual published-BEO input, not a draft/candidate/request fixture;
2. consume hash-only active-vault metadata without protected body reads;
3. generate a runtime RTM ledger only under exact approval;
4. keep drift rejection separate from RTM ledger generation;
5. prevent coverage matrices or coverage claims from laundering publication or drift authority.

This should not be selected before publication authority is resolved.

### Workstream F — Codex Live-Dispatch L3 Smoke

**Scope:** One explicit live-dispatch activation frontier if the operator chooses Codex activation.

Needed work:

1. explicit human approval naming live Codex execution;
2. exact model/CLI profile and worktree/path allowlists;
3. BLK-pipe enforcement for any source mutation;
4. no protected BLK-req paths;
5. no package-manager/network/model/browser/cyber authority unless separately approved;
6. timeout/output/replay/rollback/cleanup controls;
7. hostile review before any L4 Codex pilot.

This is not the default recommendation after the user's post-078 clarification because it activates runtime execution rather than developing BLK-System roadmap/index clarity.

---

## 6. Recommended Near-Term Sequence

Given the explicit operator clarification that this is about developing BLK-System and not Kuronode, the recommended sequence is:

1. **BLK-SYSTEM-079 — Post-078 Current-State Authority Index Refresh** — completed by `docs/BLK-079_post-078-current-state-authority-index.md`
   - L0/L1 documentation and doctrine-gate sprint.
   - Updated/superseded BLK-046's stale post-042/post-045 map.
   - Made BLK-077 the current roadmap selector.
   - Recorded BLK-078 as the current tactical-standard/profile architecture anchor.
   - No BEB, no BEO, no Kuronode source mutation, no runtime.

2. **BLK-SYSTEM-080 — Tactical Standard Profile Registry / Layer B Extraction** — completed by `docs/BLK-080_tactical-standard-profile-registry-and-layer-b-extraction.md` and `python/blk_tactical_profile_registry.py`
   - L0/L1 doctrine/fixture sprint.
   - Converted BLK-078 into a concrete BLK-System-owned profile-selection record shape, denied-authority fixture, and Layer B universal tactical-output safety extraction.
   - Registered BLK-058 as the first `kuronode-typescript` Layer C profile source without scanning or mutating Kuronode.
   - The profile-selection registry and Layer B extraction are now L0/L1 fixture/doctrine surfaces.
   - No target-repo mutation, no live scan, no BEB dispatch or BEO closeout execution, no Codex, no BLK-pipe run, no BLK-test run, no BEO publication, and no RTM.

3. **BLK-SYSTEM-081 — Target-Repo Execution Governance Pattern** — completed by `docs/BLK-081_target-repo-execution-governance-pattern.md` and `python/blk_target_repo_execution_governance.py`
   - L0/L1 doctrine/fixture sprint.
   - Generalized the post-078 exact-target chain as a BLK-System governance pattern.
   - Defined how future external target work must be requested, profile-selected, approved, preflighted, validated, hostile-reviewed, and closed.
   - Target-repo execution governance is now an L0/L1 fixture/doctrine surface.
   - No target-repo scan, no target-repo mutation, no BEB dispatch, no BEO closeout execution, no publication, and no RTM.

4. **BLK-SYSTEM-082 — BLK-058 Mechanical Enforcement Upgrade** — completed by `docs/BLK-082_blk058-mechanical-enforcement-upgrade.md` and `python/blk_058_mechanical_enforcement.py`
   - Selected the lower-authority mechanical-enforcement branch of the BLK-SYSTEM-082 decision point.
   - Added a deterministic submitted-snippet fixture for selected BLK-058 / `kuronode-typescript` enforcement through BLK-078 Layer B/Layer C machinery inside BLK-System.
   - BEO Publication Decision Package remains an unselected future L0/L1 alternative if V-model completion is prioritized later.
   - No target-repo scan, no target-repo mutation, no BEB dispatch, no BEO closeout execution, no BEO publication, and no RTM.

5. **After BLK-SYSTEM-082:** require explicit operator decision before any higher-authority frontier.
   - one bounded BLK-test evidence refresh;
   - one publication decision package or pilot request;
   - one Codex L3 smoke;
   - or one RTM authority request after publication prerequisites exist.

This sequence keeps BLK-System development first and prevents accidental drift into Kuronode product implementation.

---

## 7. BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-077 alignment obligation |
| --- | --- |
| BLK-001 — Master Architecture | Preserve V-model separation between BLK-req, planning, tactical execution, BLK-pipe mutation enforcement, BLK-test evidence, BEO publication, and blk-link trace closure. Post-078 target-repo patch evidence is treated as proof of BLK-System governance capability, not as broad target-repo authority. |
| BLK-002 — Artifact Lifecycle | Preserve staging, linting, HITL promotion, active-vault immutability, staged revision, and canonical hash promotion. Future roadmap/index work must not read or mutate protected BLK-req bodies. |
| BLK-003 — Orchestration Protocol | Preserve human dispatch gates, Layer 2 bounded context, failure ceilings, hostile audit, and no implicit inheritance between execution, testing, publication, and RTM. BLK-077 explicitly forbids BEB dispatch or BEO closeout execution as part of roadmap work. |
| BLK-004 — BLK-pipe V47 Suite | Preserve Go `blk-pipe` as deterministic final enforcement for mutation, allowlists, validation profile resolution, output caps, cleanup, Git routing, local target-hash checks, and report evidence. Python helpers and roadmap docs do not replace Go enforcement. |
| BLK-005 — BLK-Req Specification | Preserve atomic requirements, bounded use cases, immutable IDs, canonical version hashes, trace binding, and drift semantics without granting drift rejection prematurely. Coverage/RTM claims remain disabled unless separately authorized. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny behavior, no tactical write access, no protected body reads, and Discord/HITL authorization boundaries. Protected path classifiers do not authorize protected body reads. |

---

## 8. BLK-058 and BLK-078 Alignment

BLK-078 now provides the architecture for interpreting BLK-058 inside BLK-System. BLK-058 remains active tactical coding-standard doctrine, but BLK-078 separates it into universal and target-specific roles.

BLK-077 interprets BLK-058 through BLK-078 as follows:

1. BLK-078 Layer A remains BLK-System universal core and cannot be weakened by BLK-058 or any target profile.
2. BLK-058 contributes Layer B universal tactical-output safety candidates: bounded control flow, bounded state, lifecycle cleanup, validation, checked results, no dynamic execution, repository-owned validation profiles, and no authority laundering.
3. BLK-058 also supplies Layer C `kuronode-typescript` target-profile content: Electron, React, Zustand, ELK.js, JointJS, tree-sitter SysML, parser/Wasm lifecycle, renderer ownership, GraphAdapter quarantine, smoke harness, and projected-node constraints.
4. BLK-058 constrains future approved Kuronode TypeScript output; it does not authorize Kuronode work.
5. BLK-078 profile selection does not authorize BEB dispatch or BEO closeout execution, source mutation, live scans, Codex, BLK-pipe, BLK-test, BEO publication, RTM, protected-body reads, package managers, model services, browser/cyber tooling, or sandbox claims.
6. BLK-System development work may improve BLK-058 enforcement by implementing BLK-078 Layer B/Layer C machinery through local fixtures, validators, profile registries, doctrine gates, and approval envelopes in the BLK-System repository.
7. Any later live Kuronode scan, Kuronode patch, or Kuronode feature implementation requires a separate exact-target authority envelope.

BLK-058 should therefore be treated as a **Layer B/Layer C constraint input** for BLK-System governance, not as a **dispatch instruction** to modify Kuronode.

---

## 9. What Is Done Enough For Now

The following surfaces should not receive more generic preparatory rungs unless a concrete blocker is identified:

1. **Generic BLK-test fixed-tool evidence theory**
   - The system has non-disposable L4 evidence patterns and one read-only Kuronode workspace pilot chain.
   - Future runs need fresh exact approvals and concrete purpose.

2. **CEB_009-specific patch ladder**
   - The exact CEB_009/smoke harness chain is closed through BLK-SYSTEM-078.
   - Do not create more CEB_009 preparatory packages unless a new finding appears.

3. **Kuronode deterministic smoke repair**
   - Smoke is passing at Kuronode `aebea51`.
   - This is a validation baseline, not a request to start Kuronode product implementation.

4. **BLK-059-era roadmap selection**
   - BLK-059 is superseded by this document for current planning.
   - Future references should use BLK-077 for post-078 sprint selection.

---

## 10. Material Gaps Remaining

These are still real gaps in BLK-System after BLK-SYSTEM-080:

1. **No generalized target-repo execution governance pattern**
   - BLK-SYSTEM-080 created the profile-selection registry and Layer B extraction, but BLK-System still lacks a reusable target-repo governance pattern that explains how future exact-target work is requested, approved, preflighted, profile-selected, executed, hostile-reviewed, and closed.
   - This is the default BLK-SYSTEM-081 workstream.

2. **No actual authoritative BEO publication authority**
   - BLK-060 is approval-envelope readiness only.
   - No signer/storage/ledger/rollback authority has been granted.
   - No runtime `PUBLISHED` BEO output exists.

3. **No runtime RTM / drift authority**
   - Offline fixtures exist, but no runtime trace-closure authority exists after a real published BEO.
   - Drift rejection remains a separate higher authority.

4. **No production BLK-test MCP**
   - Fixed-tool evidence exists, but generic/reusable BLK-test service authority remains disabled.

5. **No live Codex execution**
   - The Codex ladder remains request/design/disabled-adapter readiness, not execution.

6. **BLK-058 / `kuronode-typescript` enforcement is still partial**
   - Fixture/static-profile checks exist, but deeper TypeScript analysis, live-repo scans, and profile integration remain future authority-bound work under BLK-078.

7. **No full end-to-end production loop**
   - BLK-001's full target chain is not yet activated as a reusable production system.

---

## 11. Candidate Sprint Selection Rules

A future sprint should be accepted only if it satisfies one rule:

1. **Consolidation rule:** It reduces stale roadmap, index, runbook, or operator-authority confusion in a bounded way.
2. **Mechanical-gate rule:** It converts existing doctrine into deterministic repository-owned checks without adding runtime authority.
3. **Profile-architecture rule:** It implements BLK-078 profile-selection records, Layer B universal-safety extraction, Layer C target-profile registration, or denied-authority fixtures without live scans or target mutation.
4. **Approval-envelope rule:** It prepares exactly one future human decision without granting or executing that decision.
5. **Evidence-refresh rule:** It runs exactly one explicitly approved evidence-only check and keeps evidence separate from mutation, publication, RTM, and coverage authority.
6. **Activation rule:** It turns on exactly one bounded runtime capability under explicit approval and keeps adjacent authorities disabled.
7. **Remediation rule:** It fixes a demonstrated hostile-review, test, or doctrine failure.

A future sprint should be rejected or split if it:

- combines multiple authority jumps;
- treats roadmap or index docs as runtime approval;
- treats BLK-058, BLK-078, Layer B safety language, or Layer C profile selection as target-repo mutation authority;
- creates BEB/BEO execution artifacts without explicit future approval;
- lets target-repo validation success imply BEO publication or RTM authority;
- lets BLK-test evidence imply source mutation authority;
- uses protected BLK-req body access as a shortcut for trace closure.

---

## 12. Updated Stop Conditions

Pause and require hostile review plus human decision if any proposed sprint attempts to:

1. treat request-ready, review-ready, design-ready, fixture-ready, static-profile-ready, roadmap-ready, or disabled-adapter evidence as runtime authority;
2. create or execute BEB/BEO artifacts from this roadmap alone;
3. mutate Kuronode source or Git state without a separate exact-target approval envelope;
4. reuse consumed approval/run IDs from BLK-SYSTEM-051, BLK-SYSTEM-052, BLK-SYSTEM-073, BLK-SYSTEM-076, BLK-SYSTEM-077, or BLK-SYSTEM-078;
5. run another BLK-test pilot without fresh exact target HEAD, workspace, approval ID, run ID, expiry, replay ledger, and operator approval;
6. treat BLK-test PASS evidence as BEO publication, RTM generation, coverage truth, drift truth, or production MCP authority;
7. publish authoritative BEOs without separate publication approval and signer/storage/ledger/rollback authority;
8. generate RTM without separate RTM approval and actual published-BEO/hash-only metadata prerequisites;
9. make RTM drift rejection automatic before drift authority is explicitly granted;
10. start Codex without explicit live Codex approval;
11. route Codex into source mutation without BLK-pipe enforcement and exact allowlists;
12. replace fixed-tool verification with arbitrary shell;
13. accept arbitrary validation shell from a less-trusted/autonomous payload boundary;
14. use BLK-058, BLK-078, Layer B safety language, or Layer C profile selection to justify live execution, live scans, source mutation, package-manager installs, or broad Kuronode authority;
15. let BLK-test, BEO, RTM, health-check, Codex, or fixture code read protected BLK-req vault bodies;
16. claim production sandbox, firewall, namespace, or host-secret isolation without tests and explicit authority;
17. add another preparatory rung with no named consolidation, mechanical-gate, approval-envelope, evidence-refresh, activation, or remediation purpose.

---

## 13. Final Roadmap Statement

BLK-System has now proven a meaningful external-target governance chain, but that proof should make the system more disciplined, not more casual.

The post-078 roadmap is now:

```text
First, BLK-SYSTEM-079 made the BLK-System authority map current.
Then, BLK-SYSTEM-080 implemented the BLK-078 tactical-standard/profile architecture as BLK-System fixtures and records.
Then, BLK-SYSTEM-081 formalized reusable target-repo governance patterns that consume explicit profile selection.
Then, BLK-SYSTEM-082 completed the lower-authority BLK-058 mechanical enforcement upgrade as a submitted-snippet fixture.
Next, require explicit operator decision before any higher-authority frontier.
```

Historical post-079 selector closed by BLK-SYSTEM-080:

```text
BLK-SYSTEM-080 — Tactical Standard Profile Registry / Layer B Extraction
```

BLK-SYSTEM-080 developed BLK-System documentation/fixtures/gates only. It extracted BLK-078 Layer B universal tactical-output safety, defined profile-selection records, and registered BLK-058 as the first Layer C source without writing BEBs, BEOs, Kuronode feature code, target-repo scans, or runtime execution artifacts.

BLK-SYSTEM-080 completed the tactical profile registry / Layer B extraction, so the profile-selection registry and Layer B extraction are now L0/L1 fixture/doctrine surfaces feeding BLK-SYSTEM-081 target-repo governance.

Historical post-080 selector closed by BLK-SYSTEM-081:

```text
BLK-SYSTEM-081 — Target-Repo Execution Governance Pattern
```

BLK-SYSTEM-081 completed the target-repo execution governance pattern, so target-repo execution governance is now an L0/L1 fixture/doctrine surface.

Historical post-081 selector closed by BLK-SYSTEM-082:

```text
BLK-SYSTEM-082 — BLK-058 Mechanical Enforcement Upgrade
```

BLK-SYSTEM-082 completed the BLK-058 mechanical enforcement upgrade by publishing `docs/BLK-082_blk058-mechanical-enforcement-upgrade.md`, implementing `python/blk_058_mechanical_enforcement.py`, and adding submitted-snippet fixture checks for selected BLK-058 constraints. After BLK-SYSTEM-082, require explicit operator decision before any higher-authority frontier. BEO Publication Decision Package remains an unselected future L0/L1 alternative. No target-repo scan, no target-repo mutation, no BEB dispatch, no BEO closeout execution, no BEO publication, and no RTM authority is granted.

After BLK-SYSTEM-082, the next architecture-development movement must name exactly one frontier under a fresh operator decision. BLK-058 remains an essential constraint for future approved Kuronode TypeScript work, but BLK-077 routes it through BLK-078's Layer B/Layer C split and keeps the boundary explicit:

```text
BLK-System development may build the cage; it does not enter the Kuronode cage unless separately authorized.
```
