# BLK-078 — Tactical Standard Profile Architecture

**Status:** Active architecture doctrine — not sprint authority; not runtime authority; not target-work authority
**Date:** 2026-05-11T18:36:37+10:00
**Purpose:** Define how BLK-System supports universal tactical-output safety principles and target-specific tactical standard profiles without hardcoding one target project's technology stack into BLK-System core.
**Scope:** BLK-System architecture doctrine for tactical standards, profile selection, target-specific add-ons, and enforcement layering. This document is not a sprint plan, not a CEB, not a CEO, not a Kuronode development plan, and not permission to scan, mutate, execute, publish, or generate trace artifacts.

---

## 0. Non-Execution and Non-Authority Boundary

BLK-078 is architecture doctrine only. It does not authorize:

- CEB writing, CEB dispatch, CEO writing, or CEO closeout execution;
- Kuronode feature implementation;
- any target-repository source mutation, Git mutation, staging, commit, push, reset, checkout, revert, stash, cleanup, or autofix;
- live Codex execution;
- reusable tactical LLM dispatch;
- new `blk-pipe` execution runs;
- live target-repository scans;
- TypeScript, Go, Python, linter, formatter, package-manager, browser, model-service, network, or cyber tooling execution;
- production or generic BLK-test MCP;
- arbitrary shell as BLK-test behavior;
- source or Git mutation by BLK-test;
- source mutation outside exact approved BLK-pipe allowlists;
- protected BLK-req vault body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison;
- authoritative BEO publication;
- runtime `PUBLISHED` BEO output;
- runtime RTM generation;
- RTM drift rejection;
- active-vault hash comparison;
- coverage matrix or coverage-claim promotion;
- signer, storage, ledger, rollback, revocation, supersession, or release authority;
- production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claims.

Any future implementation of profile registries, validators, validation profiles, live target scans, target patches, BLK-test runs, BEO publication, or RTM generation requires its own sprint plan, exact file boundaries, deterministic verification, hostile review, and explicit human approval at the relevant maturity rung.

---

## 1. Architectural Problem

BLK-058 introduced a valuable tactical coding standard for Kuronode TypeScript. It deliberately aligned with BLK-System's core intent: tactical output should be bounded, reviewable, mechanically checkable, and never trusted merely because an LLM says it is correct.

However, BLK-058 also contains Kuronode-specific technology constraints: Electron, React, Zustand, ELK.js, JointJS, tree-sitter SysML, parser/Wasm lifecycle handling, renderer state ownership, graph adapter boundaries, and Kuronode-specific projected-node limits.

Those target details are correct for Kuronode, but they should not become hardcoded BLK-System core doctrine for every future target. BLK-System needs an architecture that supports both:

1. universal tactical safety rules that apply to any tactical worker output; and
2. target-specific tactical profiles that apply only when a target/repository/language stack is explicitly selected.

BLK-078 defines that architecture as a three-layer model.

---

## 2. The Three Layers

### Layer A — BLK-System Universal Core

Layer A is the non-optional BLK-System authority and governance substrate. It applies to all BLK-System operation regardless of target repository, language, tactical worker, or profile.

Layer A includes:

1. architectural intent and authority separation;
2. BLK-req staging, baselining, canonical hashing, and HITL promotion;
3. exact trace-artifact binding through canonical `version_hash` values;
4. bounded planning and Layer 2 tactical-packet construction;
5. BLK-pipe exact allowlists, validation profile resolution, output bounds, cleanup, target-hash checks, and report evidence;
6. BLK-test evidence-only boundaries;
7. draft/authoritative BEO separation;
8. RTM / blk-link separation from publication and drift authority;
9. protected BLK-req body isolation;
10. hostile review, failure ceilings, replay controls, expiry controls, and human escalation.

Layer A is governed primarily by BLK-001 through BLK-006 and the active boundary documents that refine them. No tactical profile may weaken Layer A.

### Layer B — Universal Tactical Output Safety Standard

Layer B is the target-agnostic safety standard for tactical worker output. It captures the parts of BLK-058 that are broadly valid beyond Kuronode TypeScript.

Layer B does not decide whether work may start. It constrains how approved tactical output must be shaped once an execution boundary separately exists.

Layer B principles:

1. **Simple, reviewable control flow** — avoid hidden state transitions, callback mazes, and control-flow-by-exception.
2. **Bounded iteration** — no unbounded retry, traversal, polling, queue-drain, or convergence loops without explicit limits.
3. **Bounded runtime state** — no unbounded caches, maps, arrays, queues, listener registries, logs, or pending-operation stores.
4. **Explicit lifecycle management** — resources created by tactical output require visible teardown paths where the platform exposes cleanup semantics.
5. **Small hostile-reviewable units** — authority-sensitive functions should remain small enough for focused review, with validation, transformation, side effects, and reporting separated where practical.
6. **Boundary validation** — externally supplied data, process-boundary data, persistence records, IPC messages, parser outputs, and worker messages must be structurally validated before use.
7. **Checked results and postconditions** — callers must not ignore meaningful return values, nullable/error-shaped outputs, promises, validation results, or critical postconditions.
8. **Minimal mutable scope** — prefer local immutable values and narrow mutation windows; avoid ambient mutable singletons used to bridge architectural gaps.
9. **No dynamic execution laundering** — tactical code must not introduce `eval`, generated executable strings, reflection-like dispatch, unvalidated dynamic imports, or equivalent dynamic execution without an explicit exception.
10. **Flat, validated data access** — nested or external structures must be normalized or validated before authority-sensitive use.
11. **Zero-warning intent under repository-owned profiles** — warnings are blocking evidence when a repository-owned validation profile defines them as blocking; less-trusted/autonomous boundaries must not replace profile-owned checks with arbitrary shell.
12. **No authority laundering** — tactical quality evidence never becomes permission for source mutation, BLK-test production authority, BEO publication, RTM generation, drift rejection, protected-body reads, package-manager execution, network/model/browser/cyber tooling, or sandbox claims.

Layer B should eventually be represented by BLK-System-owned doctrine, fixtures, and validation-profile contracts. Until such implementation exists, BLK-078 is an architecture contract, not a mechanical gate.

### Layer C — Target Tactical Profiles

Layer C is the configurable target-specific add-on layer. A target tactical profile specializes Layer B for a particular repository, language, product architecture, framework stack, and validation ecosystem.

A target tactical profile may define:

1. target profile identifier;
2. target repository or repository family;
3. applicable file globs and excluded paths;
4. language/runtime stack;
5. target architecture invariants;
6. target-specific safety overlays;
7. allowed validation profile names;
8. fixture-only profile checks;
9. live-scan prerequisites;
10. exception format and approval requirements;
11. hostile-review checklist;
12. stop conditions.

Layer C profiles are constraints only. They do not authorize target work. A profile becomes active for a specific run only when a separate sprint plan, approval envelope, or execution boundary explicitly selects that target profile and grants the relevant work authority.

---

## 3. Relationship Between BLK-058 and BLK-078

BLK-058 remains valid. BLK-078 clarifies how it should be interpreted architecturally.

BLK-058 contains two kinds of content:

| BLK-058 content class | BLK-078 layer | Interpretation |
| --- | --- | --- |
| Tactical safety principles such as bounded loops, bounded state, input validation, small functions, checked results, no dynamic execution, and zero-warning intent | Layer B | Universal tactical-output safety candidates that can become target-agnostic BLK-System safety doctrine. |
| Kuronode TypeScript, Electron, React, Zustand, ELK.js, JointJS, tree-sitter SysML, parser/Wasm lifecycle, renderer ownership, GraphAdapter quarantine, smoke harness, and projected-node constraints | Layer C | Kuronode target tactical profile content. Correct for Kuronode; not automatically applicable to every BLK-System target or to BLK-System internals. |
| Non-authority language forbidding Codex activation, source mutation, BLK-test escalation, BEO publication, RTM generation, protected-body reads, package-manager/network/model/browser/cyber tooling, and sandbox claims | Layer A / all layers | Mandatory authority boundary language. Profiles and standards constrain work; they do not grant work. |

BLK-058 is therefore the first concrete target tactical standard profile source: `kuronode-typescript`.

Future BLK-System work may extract the universal Layer B content into a standalone tactical-output safety standard, while retaining BLK-058 as the Kuronode-specific Layer C profile source.

---

## 4. Target Profile Selection Model

BLK-System should treat target tactical profiles as explicit inputs to planning and execution boundaries.

A future profile selection record should bind at minimum:

| Field | Meaning |
| --- | --- |
| `profile_id` | Stable profile identifier, e.g. `kuronode-typescript`. |
| `profile_source_doc` | Governing BLK document or target document, e.g. BLK-058. |
| `target_repo_identity` | Repository path/name/remote identity the profile applies to. |
| `applicable_paths` | Exact file globs or allowlisted path families. |
| `excluded_paths` | Paths that must not be scanned or modified under this profile. |
| `profile_maturity` | L0 doctrine, L1 fixture, L2 validation profile, L3 synthetic smoke, L4 real-repo pilot, or L5 production authority. |
| `selected_by` | Sprint plan, approval envelope, or execution boundary selecting the profile. |
| `denied_authorities` | Exact denied-authority set preserved by the profile. |
| `validation_profiles` | Repository-owned validation profile names, if any. |
| `exception_policy` | How bounded exceptions are requested, approved, and reviewed. |

Conceptual example, not an implemented schema and not execution authority:

```yaml
profile_id: kuronode-typescript
profile_source_doc: docs/BLK-058_kuronode-typescript-power-of-ten-tactical-standard.md
target_repo_identity: Kuronode-v1
profile_maturity: L0_DOCTRINE_OR_L1_FIXTURE_UNLESS_SEPARATELY_APPROVED
applicable_paths:
  - "**/*.ts"
  - "**/*.tsx"
validation_profiles:
  - kuronode-power-of-ten-static
  - kuronode-typecheck-strict
  - kuronode-eslint-zero-warning
denied_authorities:
  - NO_TARGET_REPO_MUTATION_FROM_PROFILE_SELECTION_ALONE
  - NO_LIVE_SCAN_FROM_PROFILE_SELECTION_ALONE
  - NO_CODEX_EXECUTION_FROM_PROFILE_SELECTION_ALONE
  - NO_BLK_TEST_PRODUCTION_MCP_FROM_PROFILE_SELECTION_ALONE
  - NO_BEO_PUBLICATION_FROM_PROFILE_SELECTION_ALONE
  - NO_RTM_GENERATION_FROM_PROFILE_SELECTION_ALONE
```

The example above is deliberately non-authoritative. A later sprint must implement any real schema, registry, validator, fixture, or profile-selection mechanism.

---

## 5. How Existing BLK-System Architecture Supports the Layers

### 5.1 Planning and Layer 2 Packets

Hermes can use Layer A to decide what authority exists, Layer B to constrain tactical output shape, and Layer C to add target-specific constraints. When a future approved execution boundary exists, the Layer 2 packet can include:

1. exact task objective;
2. exact target repository and target hash;
3. exact allowlists;
4. trace artifacts;
5. selected profile ID and source document;
6. Layer B universal safety constraints;
7. Layer C target-specific constraints;
8. denied authorities and stop conditions.

This preserves context economy: the tactical worker receives only the relevant profile constraints, not every BLK-System document.

### 5.2 BLK-pipe

BLK-pipe remains the mutation blast shield. Profile selection must never bypass BLK-pipe.

Future BLK-pipe payloads may carry selected validation profile names or profile evidence metadata, but BLK-pipe remains responsible for exact allowlists, staging discipline, output bounds, cleanup, target-hash checks, and report evidence.

A target tactical profile may require certain validation profiles, but it does not authorize arbitrary validation shell, package-manager execution, network access, protected-body reads, BLK-test production MCP, BEO publication, or RTM generation.

### 5.3 Validation Profiles

Repository-owned validation profiles are the natural bridge from doctrine to deterministic checking.

Layer B may define universal checks such as bounded-loop markers, dynamic-execution denial, function-size thresholds, lifecycle cleanup evidence, and result-check evidence.

Layer C may bind those checks to target-specific tooling and surfaces, such as TypeScript/ESLint for Kuronode or future Go/Python validators for BLK-System internals.

Validation profiles remain evidence and enforcement aids. They do not grant target work authority.

### 5.4 BLK-test

BLK-test, when separately authorized, may return evidence about selected profile compliance. That evidence remains evidence only. It does not mutate source, publish BEOs, generate RTM, declare coverage truth, or grant production MCP authority.

### 5.5 BEO and RTM

A future BEO may record which Layer B standard and Layer C target profile constrained the tactical output. That record is trace metadata, not proof that publication or RTM authority exists.

RTM / blk-link remains separate. Profile compliance evidence must not become drift rejection, coverage truth, protected-body access, or public-ledger mutation without separate authority.

---

## 6. Universal Versus Target-Specific Classification

The following classification should guide future extraction work:

| Standard element | Layer B universal? | Layer C target-specific? | Notes |
| --- | --- | --- | --- |
| Bounded loops and retries | Yes | Target may set concrete bounds | Universal principle; target defines thresholds. |
| No unbounded caches/queues/maps/logs | Yes | Target may define concrete resource classes | Universal principle; target identifies risky structures. |
| Explicit cleanup | Yes | Target defines concrete resources | Universal principle; Electron, workers, parser trees, JointJS cells are Kuronode-specific examples. |
| Small hostile-reviewable functions | Yes | Target may set line thresholds by language | BLK-058 uses 60 physical lines for Kuronode TypeScript. |
| Input/output validation | Yes | Target defines schemas and boundaries | Universal principle; IPC/parser/layout/persistence specifics are target overlays. |
| No dynamic execution | Yes | Target names language-specific constructs | `eval` and `new Function` are TypeScript/JavaScript examples. |
| Zero-warning intent | Yes | Target names tooling/profile stack | TypeScript/ESLint are Kuronode-specific tools. |
| Electron IPC boundary | No | Yes | Kuronode-specific. |
| Zustand renderer ownership | No | Yes | Kuronode-specific. |
| ELK geometry authority | No | Yes | Kuronode-specific. |
| JointJS GraphAdapter quarantine | No | Yes | Kuronode-specific. |
| tree-sitter SysML/Wasm lifecycle | Partially | Yes | Cleanup is universal; this concrete lifecycle is Kuronode-specific. |
| Projected-node circuit breaker | No | Yes | Kuronode-specific unless another target adopts it explicitly. |

---

## 7. Profile Maturity Ladder

Target tactical profiles should advance through the same kind of authority maturity discipline used elsewhere in BLK-System:

1. **L0 Doctrine-only** — prose constraints and hostile-review checklist only.
2. **L1 Fixture-only** — local synthetic snippets/descriptors and deterministic fixture validators; no live target scan.
3. **L2 Repository-owned validation profiles** — profile names resolve to deterministic repository-owned commands or checks; no arbitrary shell expansion.
4. **L3 Synthetic smoke** — one explicitly approved synthetic run against controlled non-production inputs.
5. **L4 Real-repo pilot** — one exact-target real-repository scan or enforcement run under explicit approval, exact HEAD, exact paths, replay protection, output bounds, and hostile review.
6. **L5 Production authority** — reusable capability only after monitoring, rollback, false-positive handling, operator controls, and hostile review are proven.

No rung inherits authority from a previous rung. A PASS at one rung is not permission to advance to the next rung.

---

## 8. BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-078 alignment |
| --- | --- |
| BLK-001 — Master Architecture | Preserves separation between architectural intent, tactical execution, deterministic enforcement, physical verification, BEO publication, and trace closure. Layer A remains the non-optional core. |
| BLK-002 — Artifact Lifecycle | Does not change BLK-req staging, linting, HITL approval, active-vault immutability, staged revision, or canonical hashing. Profile documents and profile selection records must not mutate protected artifacts. |
| BLK-003 — Orchestration Protocol | Clarifies how universal and target-specific constraints can be included in future Layer 2 packets while preserving human dispatch gates, bounded context, failure ceilings, hostile audit, and disabled/authority-bound BLK-test/BEO/RTM surfaces. |
| BLK-004 — BLK-pipe V47 Suite | Preserves BLK-pipe as final mutation enforcement for exact allowlists, validation profile resolution, output caps, cleanup, Git routing, local target-hash checks, and report evidence. Profiles do not replace BLK-pipe. |
| BLK-005 — BLK-Req Specification | Preserves canonical version hashes, trace binding, schema enforcement, protected artifact boundaries, and drift semantics without granting drift rejection prematurely. |
| BLK-006 — BLK-Req Implementation Brief | Preserves protected-vault hard-deny behavior, no tactical write access, no protected body reads, staged revision discipline, and Discord/HITL authorization boundaries. |

---

## 9. Conflict and Precedence Rules

1. Layer A beats every Layer B or Layer C rule.
2. Layer B may constrain Layer C but cannot weaken target-specific architecture constraints.
3. Layer C may add stricter target-specific rules but cannot grant authority or weaken Layer A.
4. Product-specific architecture documents may add constraints to a target profile but cannot authorize BLK-System runtime action without a BLK-System approval boundary.
5. If a target profile conflicts with exact approval, exact allowlists, protected BLK-req isolation, validation-profile ownership, BLK-test evidence-only boundaries, BEO publication boundaries, RTM boundaries, or stop conditions, BLK-System must fail closed and require human review.

---

## 10. Stop Conditions

Pause and require hostile review plus human decision if any future change attempts to use BLK-078 to:

1. treat a target profile as permission to scan or mutate a target repository;
2. treat BLK-058 or `kuronode-typescript` profile selection as permission to do Kuronode work;
3. start Codex, tactical LLM dispatch, BLK-pipe execution, BLK-test, TypeScript tooling, package managers, browser, network, model-service, or cyber tooling without separate approval;
4. route source mutation outside exact BLK-pipe allowlists;
5. replace repository-owned validation profiles with arbitrary shell from a less-trusted/autonomous boundary;
6. read, copy, parse, hash, summarize, scan, mutate, or compare protected BLK-req vault bodies;
7. publish BEOs, emit runtime `PUBLISHED` BEO output, generate RTM, make drift decisions, claim coverage truth, or mutate ledgers;
8. claim sandbox, host-secret isolation, firewall, namespace, cgroup, VM, seccomp, AppArmor, or SELinux guarantees from profile architecture alone;
9. hardcode Kuronode-specific technology rules as universal BLK-System core rules;
10. strip universal tactical safety constraints from a target profile because the target profile is configurable.

---

## 11. Final Architecture Statement

BLK-System should support tactical standards through layered composition:

```text
Layer A: BLK-System Universal Core
  Authority, traceability, HITL, BLK-pipe, BLK-test evidence boundaries, BEO/RTM separation.

Layer B: Universal Tactical Output Safety Standard
  Bounded, reviewable, lifecycle-safe, validated, statically analyzable tactical output.

Layer C: Target Tactical Profile
  Target-specific stack, file surfaces, validation profiles, architecture invariants, and stop conditions.
```

BLK-058 remains the authoritative Kuronode TypeScript profile source until superseded or split by later doctrine.

BLK-078 makes that relationship explicit:

```text
BLK-System owns the layered profile mechanism.
BLK-058 supplies Kuronode TypeScript profile content.
Universal BLK-058 principles may be extracted into Layer B.
Kuronode-specific BLK-058 overlays remain Layer C.
No layer grants runtime authority by itself.
```
