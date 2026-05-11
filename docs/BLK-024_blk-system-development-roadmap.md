# BLK-024 — BLK-System Development Roadmap

> **Superseded by BLK-077:** This document is historical post-BLK-SYSTEM-019 roadmap guidance. BLK-045 later superseded it for post-BLK-SYSTEM-042 planning, BLK-059 later controlled post-BLK-SYSTEM-054 / post-BLK-058 planning, and BLK-077 now controls current roadmap selection after BLK-SYSTEM-078. BLK-024 remains retained for maturity-model lineage and historical context.

**Status:** Superseded roadmap proposal — retained for historical context, not sprint authority
**Date:** 2026-05-07T19:32:19+10:00
**Superseded by:** `docs/BLK-077_blk-system-post-078-roadmap.md` for current roadmap selection; historical intermediate supersession was `docs/BLK-045_blk-system-post-042-roadmap.md` on 2026-05-09, then `docs/BLK-059_blk-system-post-058-roadmap.md` on 2026-05-10
**Purpose:** Provide historical high-level development roadmap context for BLK-System after BLK-SYSTEM-019, honoring BLK-001 through BLK-006 while identifying improvement candidates for later doctrine or implementation sprints.
**Scope:** Historical strategic sequencing, maturity gates, and component boundaries. This document is not a sprint plan, not an execution brief, and not a grant of runtime authority.

---

## 0. Non-Execution and Non-Authority Boundary

BLK-024 is a guiding roadmap only. It does not authorize:

- live Codex or live tactical LLM execution;
- new `blk-pipe` execution runs beyond separately approved sprint payloads;
- production BLK-test MCP;
- rerunning the BLK-SYSTEM-014 / BLK-020 first live fixed-tool smoke;
- arbitrary shell as BLK-test behavior;
- protected BLK-req vault body reads, copying, parsing, hashing, or mutation;
- authoritative BEO publication;
- RTM generation;
- RTM drift rejection authority;
- public ledger mutation;
- signer, storage, rollback, or release authority.

Every item below remains subject to a later explicit sprint plan, deterministic local tests, hostile review, exact authority boundaries, and human approval where required.

---

## 1. Current Baseline After BLK-SYSTEM-019

BLK-System is currently in a guarded pre-production/autonomy-hardening stage.

The system already has strong foundations:

1. **BLK-001 separation of concerns** is mostly intact: Hermes plans and audits, tactical engines implement only inside bounds, `blk-pipe` owns mutation enforcement, `blk-test` verifies reality, and `blk-link` owns future RTM/ledger closure.
2. **BLK-002 / BLK-005 BLK-req doctrine** defines staged drafting, linting, HITL promotion, canonical hashes, and immutable baselines.
3. **BLK-003 orchestration doctrine** defines BEB generation, bounded Layer 2 packets, BLK-pipe invocation, hostile audit, iteration limits, and human escalation.
4. **BLK-004 / BLK-006 BLK-pipe authority** now has working guardrails around trace metadata, explicit allowlists, protected-vault rejection, output caps, Git staging, and verified revert.
5. **BLK-020 through BLK-023** establish careful design/evidence boundaries for BLK-test, draft BEO projection, authoritative BEO publication, and offline RTM design.

The system is not yet a fully live end-to-end autonomous V-model. Production BLK-test MCP, authoritative BEO publication, offline RTM generation, and RTM drift rejection remain disabled unless later active doctrine explicitly grants them.

---

## 2. Roadmap Principles

### 2.1 Build the cage before increasing autonomy

BLK-System should continue to harden deterministic enforcement before enabling broader autonomous behavior. Each new authority should be added only after the surrounding denial, cleanup, audit, replay, and rollback paths are already proven.

### 2.2 Prefer narrow authority ladders over big-bang activation

Every major capability should climb a visible ladder:

1. **Design-only doctrine** — prose and gates; no runtime authority.
2. **Fixture-only implementation** — deterministic local shapes; no live transport.
3. **Disabled transport / fail-closed adapter** — startup and request attempts prove refusal semantics.
4. **Synthetic fixed-tool smoke** — one or more human-approved, source-bound, replayable, isolated checks.
5. **Pilot authority** — bounded real-repo verification or publication under narrow approval.
6. **Production authority** — only after hostile review, rollback, monitoring, and operator controls exist.

No sprint should silently skip a rung.

### 2.3 Keep approvals separate

Execution approval, BLK-test approval, BEO publication approval, RTM generation approval, and drift rejection authority must remain separate. Passing one gate must never imply permission to perform the next gate.

### 2.4 Preserve hash-based traceability without protected-body leakage

`version_hash` and `trace_artifacts` are the baton. Future traceability work should use opaque canonical hashes and approved metadata paths. BLK-test, BEO, and RTM work must not read protected BLK-req vault bodies unless a later BLK-req authority model explicitly grants a safe hash-only or metadata-only backend path.

### 2.5 Treat docs as authority-bearing surfaces

BLK-System documentation is not commentary only. Active doctrine can grant or deny authority. Roadmap, sprint, and design docs must therefore distinguish current runtime authority from target architecture.

---

## 3. Component Roadmap Tracks

### Track A — Doctrine, alignment, and review gates

**Goal:** Keep the doctrine set internally consistent as implementation matures.

Current state:

- BLK-SYSTEM-018 remediated protected-vault Exit 3 routing and emergency revert reachability.
- BLK-SYSTEM-019 remediated the BLK-020 active-doctrine contradiction and BEO authority wording ambiguity.

Roadmap direction:

1. Maintain persistent doctrine gates for any new authority boundary.
2. Add explicit current-state overlays when older docs describe target architecture.
3. Keep hostile reviews scoped against BLK-001 through BLK-006 before activating new runtime authority.
4. Prefer remediation sprints that close one authority ambiguity at a time.

Exit marker for this track:

- A new reader can distinguish current runtime authority, design-only doctrine, fixture-only behavior, and future target architecture without relying on tribal knowledge.

---

### Track B — BLK-req legislative gateway

**Goal:** Make the requirements/use-case baseline path mechanically reliable and safe enough to feed BEB trace artifacts without leaking protected body authority to tactical or verification layers.

Current state:

- BLK-002 and BLK-005 define staging, linting, baseline promotion, canonical hashing, staged revision, and concurrency locks.
- BLK-006 defines implementation directives for the immutable vault and BLK-pipe hard-deny behavior.

Roadmap direction:

1. Harden and document the exact backend scripts for staging, linting, promotion, and revision.
2. Prove canonical hash determinism with regression fixtures.
3. Define an approved retrieval boundary for Hermes planning that returns only requested artifact bodies plus canonical metadata.
4. Define a separate future hash-only metadata path for RTM comparison, without exposing protected bodies to BLK-test or tactical engines.
5. Add operator-facing diagnostics for stale drafts, lint failures, schema mismatches, and approval mismatch.

Exit marker for this track:

- A baselined requirement/use-case can safely travel from human intent to canonical `trace_artifacts` in a BEB, with repeatable hash evidence and no tactical write access to the active vault.

---

### Track C — BLK-pipe blast shield and forge

**Goal:** Keep `blk-pipe` as the deterministic, compiled, non-reasoning authority for source mutation and Git safety.

Current state:

- BLK-pipe validates payload structure, trace artifacts, path classes, and allowlists.
- It enforces strict staging, unauthorized mutation cleanup, output caps, validation aborts, and verified revert.
- Sprint 018 closed the protected-vault Exit 3 and dirty-workspace revert gaps.

Roadmap direction:

1. Continue to treat Go `blk-pipe` as the authority, not Python wrappers.
2. Tighten validation command semantics through named profiles or explicit allowlists.
3. Preserve exact-path staging and prohibit broad Git operations.
4. Expand report evidence only when it improves auditability without leaking secrets or protected content.
5. Add negative tests for each new authority path before enabling it.

Exit marker for this track:

- `blk-pipe` can run bounded implementation work, reject unauthorized changes, recover from failure ceilings, and emit enough structured evidence for Hermes hostile audit without relying on LLM honesty.

---

### Track D — Validation command profile tightening

**Goal:** Replace or constrain free-form validation command strings before BLK-System crosses less-trusted or more autonomous boundaries.

Current state:

- Validation commands are bounded, timed, output-limited, and run after candidate mutation.
- They are still payload-provided shell strings, which is acceptable under current trusted-local assumptions but risky for broader operation.

Roadmap direction:

1. Introduce named validation profiles such as `go-full`, `python-unittest`, `node-typecheck`, or `docs-doctrine-gates`.
2. Bind profiles to deterministic command arrays owned by the repository, not by arbitrary payload text.
3. Allow per-sprint additions only through explicit human-reviewed doctrine or plan approval.
4. Preserve sequential aggregation and full failure reporting.
5. Reject network, package-manager, secret-reading, or broad host-inspection commands unless explicitly approved for a narrow operator-maintenance sprint.

Exit marker for this track:

- A BEB can request validation by profile name, and BLK-pipe can prove which exact commands ran without treating arbitrary shell text as trusted authority.

---

### Track E — Python adapter and orchestrator policy layer

**Goal:** Make Python orchestration a safe convenience layer without pretending it replaces the Go blast shield.

Current state:

- Python adapter surfaces forward payload fields into BLK-pipe.
- The Go binary remains the actual authority.

Roadmap direction:

1. Clearly document that adapters are transport helpers unless explicitly upgraded.
2. Add adapter-side preflight checks that mirror, but do not replace, Go authority checks.
3. Require adapter payload construction to preserve trace artifacts, deny-read flags, validation profiles, and exact allowlists.
4. Add tests proving the adapter cannot silently drop required trace metadata or broaden authority fields.
5. Preserve Go-side enforcement as the final source of truth.

Exit marker for this track:

- Python orchestration reduces operator mistakes while fail-closed Go enforcement still catches malicious or broken payloads.

---

### Track F — BLK-test production-readiness ladder

**Goal:** Move BLK-test from disabled/fixture/smoke evidence toward a production physics oracle without granting it planning, mutation, publication, or RTM authority.

Current state:

- Generic/production BLK-test MCP remains disabled.
- BLK-020 records one accepted first live fixed-tool smoke under explicit human approval.
- BLK-017, BLK-018, and BLK-019 define disabled transport, workspace/process-control probes, and approval/source-evidence boundaries.

Roadmap direction:

1. Keep fixed-tool registry semantics: no arbitrary shell, no caller-supplied command execution, no dynamic tool expansion.
2. Expand synthetic smoke coverage only through separate approval envelopes and replay hashes.
3. Prove workspace isolation against real target-repo escape, `.git` ancestry/descendant escape, symlink escape, secret exposure, timeout failure, output flood, and cleanup failure.
4. Define pilot real-repo verification authority separately from synthetic smoke authority.
5. Ensure every BLK-test output is evidence only: PASS/FAIL/BLOCKED/FATAL evidence must not publish BEOs, mutate source, or generate RTM.

Exit marker for this track:

- BLK-test can run approved verification against bounded workspaces and return replayable evidence while remaining physically unable to mutate source or escalate into publication/ledger authority.

---

### Track G — BEO publication path

**Goal:** Progress from draft-only BEO fixtures toward authoritative BEO publication only after signer, storage, ledger, approval, and rollback rules exist.

Current state:

- Draft-only BEO projection is allowed under BLK-014, BLK-016, and BLK-021.
- BLK-022 records authoritative BEO publication as design-only.
- Current runtime outputs must preserve `beo_publication: "DRAFT_ONLY"` and `rtm_status: "NOT_GENERATED"`.

Roadmap direction:

1. Define a publication candidate schema with canonical BEO hash, source evidence identity, BLK-pipe report identity, BLK-test evidence identity, and trace artifacts.
2. Require publication-specific human approval that cannot be inherited from execution or BLK-test approval.
3. Define signer identity, key-handling, immutable storage, public ledger append rules, rollback, revocation, and supersession.
4. Reject any attempt to publish success from BLOCKED, fatal, transport-error, interrupted, missing, malformed, stale, or unknown evidence.
5. Keep RTM generation separate from publication.

Exit marker for this track:

- A BEO can be published only through a replayable, signed, approval-bound path, and publication can be revoked or superseded without rewriting history.

---

### Track H — BLK-link offline RTM ledger

**Goal:** Implement trace closure after BEO publication without giving RTM code hidden access to planning, testing, source mutation, or protected body authority.

Current state:

- BLK-023 is design-only.
- Runtime RTM fields remain disabled-interface only: `rtm_status: "NOT_GENERATED"` and `rtm_authority: "DISABLED_INTERFACE_ONLY"`.

Roadmap direction:

1. Keep RTM generation approval separate from execution, BLK-test, and BEO publication approval.
2. Define hash-only active-vault comparison through an approved backend path.
3. Generate coverage matrices only from published BEO metadata and canonical active-vault hashes, not requirement body reads.
4. Define coverage states for traced, missing, stale, malformed, superseded, unknown, and rejected evidence.
5. Treat RTM drift rejection as a later authority beyond basic ledger generation.

Exit marker for this track:

- `blk-link` can create an offline RTM ledger from published BEO metadata and approved hash-only vault metadata, while preserving protected-body isolation and human-review boundaries for drift decisions.

---

### Track I — Operator UX, observability, and escalation

**Goal:** Make BLK-System understandable and recoverable for the human operator.

Roadmap direction:

1. Standardize concise status reports for BLK-pipe, BLK-test, BEO, and RTM stages.
2. Build escalation packages that preserve raw evidence without token-flooding Discord or Hermes context.
3. Make failure ceilings obvious: what failed, what was reverted, what remains dirty, and what human decision is needed.
4. Add health checks for local binaries, Python tools, schemas, test fixtures, and disabled transport stubs.
5. Record runbooks for common failures: invalid payload, unauthorized mutation, syntax gate failure, output flood, invalid revert anchor, disabled BLK-test, draft-only BEO, and RTM non-generation.

Exit marker for this track:

- A human can tell whether the system is blocked by policy, broken code, missing approval, failed verification, or disabled future authority.

---

### Track J — Security, sandbox, and capability hardening

**Goal:** Ensure any future live or pilot authority is surrounded by explicit capability boundaries.

Roadmap direction:

1. Document current sandbox claims honestly; do not claim production host-secret isolation until proven.
2. Scrub environment variables, SSH agents, askpass, tokens, and host-specific credentials from child processes.
3. Bound process groups, timeouts, output sizes, temp directories, symlink handling, nested Git behavior, and cleanup semantics.
4. Prefer fixed tools over general shell.
5. Require network/model-service/cyber-tooling denial by default, with explicit one-off operator approval for maintenance-only exceptions.

Exit marker for this track:

- A future live path can state exactly which filesystem, process, network, credential, and tool capabilities are available, and tests prove forbidden capabilities fail closed.

---

## 4. Suggested Development Sequence

This sequence is intentionally high-level. Each item should become its own later sprint plan only when selected.

### Stage 1 — Stabilize current guarded local operation

Focus:

- validation command profiles;
- Python adapter policy hardening;
- doctrine-gate upkeep;
- clearer current-state overlays in older target-architecture docs.

Reason:

- These are prerequisite safety improvements before broader live BLK-test or publication work.

Do not include:

- production BLK-test MCP;
- BEO publication;
- RTM generation.

---

### Stage 2 — Prepare BLK-test for controlled pilot authority

Focus:

- fixed-tool registry expansion only under approval;
- workspace isolation proofs;
- replay/source evidence bundles;
- PASS/FAIL/BLOCKED semantics;
- cleanup and timeout failure behavior.

Reason:

- BLK-test is the next major missing organ in the BLK-001 V-model, but it is also a high-risk authority boundary.

Do not include:

- source mutation;
- arbitrary shell;
- publication;
- RTM generation;
- protected-vault body reads.

---

### Stage 3 — Turn BEO from draft fixture into approved publication candidate

Focus:

- publication candidate schema;
- separate human publication approval;
- signer/storage/ledger design;
- rollback/revocation/supersession;
- rejection of stale or invalid evidence.

Reason:

- A published BEO is the bridge between execution evidence and future RTM. It must not be created casually.

Do not include:

- RTM generation;
- drift rejection authority;
- BLK-test authority expansion.

---

### Stage 4 — Implement offline RTM ledger generation

Focus:

- hash-only active-vault metadata comparison;
- published BEO input validation;
- coverage matrix generation;
- missing/stale/malformed/superseded evidence states;
- human-review handoff for drift.

Reason:

- This closes the V-model trace, but only after BEO publication is safe enough to serve as ledger input.

Do not include:

- protected-vault body reads;
- automatic drift rejection unless separately authorized;
- source mutation.

---

### Stage 5 — Integrate the full autonomous loop under human gates

Focus:

- BEB generation from BLK-req artifacts;
- BLK-pipe bounded implementation;
- BLK-test verification evidence;
- draft or published BEO handling according to current authority;
- optional offline RTM generation if separately authorized;
- failure ceiling and revert recovery;
- human escalation packages.

Reason:

- This is the target BLK-001 V-model, assembled only after each component path has independently proven its boundary.

Do not include:

- any implicit authority inheritance between stages.

---

## 5. BLK-001 through BLK-006 Alignment Matrix

| Governing doc | Roadmap obligation | Suggested improvement candidate |
| --- | --- | --- |
| BLK-001 — Master Architecture | Preserve strict separation between requirements, planning, source mutation, verification, and ledger closure. | Add a more formal current-state vs target-state summary table so future docs do not accidentally imply disabled components are live. |
| BLK-002 — Artifact Lifecycle | Keep HITL staging, linting, baseline promotion, canonical hashes, and staged revisions as the only path into active BLK-req baselines. | Specify exact backend script/API names for retrieval, promotion, revision, and hash-only metadata access once implemented. |
| BLK-003 — Orchestration Protocol | Preserve BEB trace binding, Layer 2 context economy, human dispatch gate, POSIX routing, hostile audit, failure ceiling, and escalation. | Split target Phase 4.2 BLK-test behavior from current disabled/smoke/pilot authority with explicit maturity levels. |
| BLK-004 — BLK-pipe V47 Suite | Keep `blk-pipe` deterministic, compiled, non-reasoning, strict about allowlists, Git routing, output caps, and verified reverts. | Replace arbitrary validation command strings with named profiles or a strict allowlist before broader autonomy. |
| BLK-005 — BLK-Req Specification | Preserve atomic requirements, bounded use cases, immutable IDs, canonical hashes, and trace binding. | Clarify which drift-rejection statements are target-state until authoritative BEO publication and RTM generation are enabled. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny, staged revisions, canonical hashing, Discord/HITL authorization, and external-viewer read-only rules. | Add adapter/orchestrator implementation boundaries so Python helpers cannot be mistaken for the final authority layer. |

These improvement candidates are not automatic edits to BLK-001 through BLK-006. They are roadmap guidance for later doctrine cleanup or implementation sprints.

---

## 6. Maturity Model

| Level | Name | Meaning | Allowed authority |
| --- | --- | --- | --- |
| L0 | Doctrine-only | Prose, diagrams, and gates only. | No runtime authority. |
| L1 | Fixture-only | Deterministic local shapes and tests. | No live transport or source mutation beyond normal repo maintenance. |
| L2 | Disabled transport | Requests prove refusal/fail-closed behavior. | No success claims from live systems. |
| L3 | Approved synthetic smoke | One or more explicit, source-bound, replayable, synthetic checks. | Narrow evidence only; no production authority. |
| L4 | Pilot runtime | Bounded real-repo or real-artifact operation under separate approval. | Limited pilot authority only. |
| L5 | Production authority | Reusable runtime capability with monitoring, rollback, docs, tests, and human governance. | Explicit active doctrine authority only. |

Current rough maturity after BLK-SYSTEM-019:

- BLK-req doctrine: L0/L1 depending on implemented script coverage.
- BLK-pipe blast shield: L3/L4 for local guarded execution surfaces.
- BLK-test: L2 with one recorded L3 first-smoke exception under BLK-020.
- BEO: L1 draft-only fixtures; publication remains L0 design-only.
- RTM / BLK-link: L0 design-only.

---

## 7. Roadmap Stop Conditions

Pause and require a hostile review if any proposed sprint attempts to:

1. treat target architecture as current authority;
2. make BLK-test mutate, stage, commit, push, reset, stash, checkout, or revert source;
3. let BLK-test, BEO, or RTM code read protected BLK-req vault bodies;
4. publish authoritative BEOs without separate publication approval;
5. generate RTM without separate RTM approval;
6. make RTM drift rejection automatic before drift authority is explicitly granted;
7. replace fixed-tool verification with arbitrary shell;
8. rely on Python adapters as the sole enforcement layer;
9. accept arbitrary validation shell from a less-trusted payload boundary;
10. convert missing, malformed, blocked, fatal, transport-error, interrupted, stale, unknown, or replayed evidence into success.

---

## 8. Operating Guidance for Future Sprint Plans

A future sprint plan derived from this roadmap should include:

1. exact scope and non-goals;
2. governing BLK documents;
3. current authority boundary;
4. files allowed to change;
5. RED/GREEN or equivalent deterministic evidence;
6. explicit non-execution statement for out-of-scope authorities;
7. hostile review step;
8. outcome documentation;
9. exact verification commands;
10. clear statement whether the sprint is doctrine-only, fixture-only, disabled transport, synthetic smoke, pilot, or production authority.

For future authority-bearing sprint plans, include **Sprint-dispatch approval provenance for authority-bearing plans** as a durable audit block. The block should record the source system, operator identity, message/event ID when available, timestamp, exact approved scope, and explicit excluded authorities. It must also state that sprint-dispatch approval does not substitute for runtime approval fixtures and that runtime/fixture approval hashes remain separate from planning or dispatch approval.

BLK-024 should be used as a compass, not as a queue. The next sprint should be selected by risk and dependency order, not by document order alone.

---

## 9. Recommended Near-Term Direction

The safest near-term sequence is:

1. **Validation command profile tightening** — reduce shell-shaped authority before increasing autonomy.
2. **Python adapter policy-layer hardening** — make the orchestration path harder to misuse while preserving Go-side enforcement as final authority.
3. **BLK-test pilot design review** — define exactly what must be proven before any broader live BLK-test authority.
4. **BEO publication implementation design-to-fixture bridge** — move from prose-only design toward signed candidate fixtures, still not published.
5. **RTM hash-only metadata path design** — define how `blk-link` may compare hashes without reading protected bodies.

This order honors BLK-001 through BLK-006 because it keeps requirements protected, source mutation bounded, verification separate, publication separately approved, and traceability hash-bound.

---

## 10. Final Roadmap Thesis

BLK-System should mature by making each boundary mechanically boring before making the system more autonomous.

The development path is not:

```text
LLM writes code -> LLM says tests passed -> LLM publishes outcome
```

The intended path is:

```text
Human-approved requirement hash
  -> Hermes-scoped BEB
  -> BLK-pipe-bounded source mutation
  -> BLK-test evidence only
  -> separately approved BEO publication
  -> separately approved offline RTM ledger
  -> human-reviewable drift decisions
```

The roadmap should therefore prioritize safety surfaces first, live verification second, publication third, and trace closure last.
