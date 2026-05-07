# BLK-025 — BLK-test pilot readiness boundary

**Status:** Design-only boundary contract — not runtime authority  
**Date:** 2026-05-07T22:08:00+10:00  
**Purpose:** Define the proof checklist and stop conditions that must be satisfied before any later BLK-test L4 pilot authority request.  
**Scope:** BLK-024 Track F — BLK-test production-readiness ladder, current L0 doctrine-only boundary with persistent L1 doctrine-gate tests. This document is not a sprint plan, not live BLK-test MCP authority, and not approval to run new smoke or pilot verification.

---

## 0. Non-Execution and Non-Authority Boundary

BLK-025 is design-only. It does not authorize:

- production BLK-test MCP;
- new live BLK-test smoke runs;
- replay of the BLK-SYSTEM-014 / BLK-020 first live fixed-tool smoke;
- arbitrary shell, dynamic command execution, caller-supplied commands, package-manager execution, model calls, network calls, or cyber tooling as BLK-test behavior;
- source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test;
- BLK-test execution against `/home/dad/BLK-System`, real target repositories, `.git` roots, `.git` ancestors, `.git` descendants, root paths, home paths, protected BLK-req vault paths, or host-secret-bearing paths;
- protected BLK-req vault body reads, copying, parsing, hashing, mutation, or drift comparison;
- authoritative BEO publication;
- RTM generation;
- RTM drift rejection authority;
- public ledger mutation;
- signer, storage, rollback, revocation, or supersession authority;
- production sandbox, cgroup, VM, network, or host-secret isolation claims.

BLK-test remains evidence only. PASS, FAIL, BLOCKED, FATAL, transport-error, interrupted, stale, malformed, unknown, or replayed evidence must not mutate source, publish BEOs, generate RTM, promote BLK-req artifacts, create active requirement coverage, or make drift decisions.

Persistent doctrine gate markers: no source mutation; no authoritative BEO publication; no RTM generation; no production BLK-test MCP.

---

## 1. BLK-024 Track and Maturity

BLK-025 implements a design boundary for **Track F — BLK-test production-readiness ladder**.

Current maturity classification:

| Level | Current BLK-025 classification | Meaning |
| --- | --- | --- |
| L0 doctrine-only | Active for this document | Prose, stop conditions, proof checklist, and authority boundaries only. |
| L1 fixture-only | Referenced through existing BLK-018/BLK-019 tests and this document's doctrine gate | Deterministic local shapes and tests only; no live transport. |
| L2 disabled transport | Preserved through BLK-017 | Generic startup and request attempts remain fail-closed. |
| L3 approved synthetic smoke | Historical exception only through BLK-020 | One accepted source-bound synthetic fixed-tool smoke; no reuse or expansion. |
| L4 pilot runtime | Future authority only | L4 pilot authority requires a later explicit sprint, separate human approval, deterministic tests, hostile review, and closeout. |
| L5 production authority | Out of scope | Production authority requires a later explicit active-doctrine grant and operational controls. |

L4 pilot authority requires a later explicit sprint. This document only defines prerequisites for that future request.

---

## 2. Current-State Ladder Preserved

| Contract | Current authority | Preserved boundary |
| --- | --- | --- |
| BLK-017 | Disabled generic transport | Generic live BLK-test MCP remains disabled. Stdio-only disabled metadata, startup refusal, non-executing handshake/lifecycle probes, and descriptor-only fixed-tool registry evidence remain current authority. |
| BLK-018 | Inert workspace/process-control probes | Deterministic local fixture probes cover workspace, cache, lock, process, timeout, output, cleanup, replay, and environment evidence. They do not execute fixed-tool tests or target the primary repository. |
| BLK-019 | One-run/scoped approval/source-evidence validation | Approval records are BLK-test-specific, source-bound, expiry/replay checked, and separate from Codex/live tactical approval. They do not start transport or execute fixed tools. |
| BLK-020 | One historical synthetic fixed-tool smoke exception | Exactly one accepted first-smoke evidence contract exists for `run_ast_validation` in a synthetic isolated workspace. It does not authorize production BLK-test MCP or future smoke reuse. |

BLK-017, BLK-018, BLK-019, and BLK-020 remain active current-state contracts unless a later sprint explicitly supersedes a narrow part of them.

---

## 3. L4 Pilot Authority Prerequisites

The following items are prerequisites only. They do not grant pilot authority.

### 3.1 Separate human approval

A later L4 pilot request must require separate human approval that is distinct from:

- BLK-pipe execution approval;
- Codex/live tactical approval;
- BLK-020 first-smoke approval;
- BEO publication approval;
- RTM generation approval;
- RTM drift rejection authority.

Approval must be BLK-test-specific, one-run/scoped, source-bound, expiry-bound, replay-resistant, and auditable.

### 3.2 Fixed-tool registry

A later pilot must use a fixed-tool registry. The registry must preserve:

- no arbitrary shell;
- no caller-supplied commands;
- no dynamic tool expansion;
- no wildcard or unknown tools;
- no package-manager execution;
- no network/model/cyber capability;
- deterministic command arrays owned by approved repository code or doctrine.

### 3.3 Source-bound evidence envelope

A later pilot request must bind the source envelope to at least:

- BLK-pipe report identity;
- `beb_id`;
- source `commit_hash`;
- `pre_engine_hash`;
- `post_engine_hash`;
- target branch;
- requested fixed tool(s);
- test profile;
- workspace identity;
- timeout/output profile;
- canonical `trace_artifacts` with `sha256:<64-lowercase-hex>` version hashes;
- approval identity and timestamp;
- replay identifiers and envelope hash.

Mismatches, missing fields, malformed hashes, expired approvals, replayed approval IDs, replayed run IDs, BLOCKED source evidence, and unknown evidence must fail closed.

### 3.4 Workspace isolation proof

A later pilot must prove fail-closed behavior for:

- real target-repo escape;
- `.git` root escape;
- `.git` ancestor escape;
- `.git` descendant escape;
- symlink escape;
- hardlink/same-filesystem clone ambiguity;
- protected BLK-req path access;
- root path access;
- home path access;
- host-secret-bearing path access;
- workspace-relative traversal;
- stale or unowned workspace/cache/lock artifacts;
- cleanup failure.

Protected-vault checks must preserve no protected BLK-req vault body reads.

### 3.5 Process and output proof

A later pilot must prove bounded behavior for:

- startup refusal when approval is missing;
- timeout failure;
- output flood failure;
- descendant process kill;
- pipe-holder no-hang behavior;
- interrupted child process handling;
- process group cleanup;
- bounded stdout/stderr evidence;
- secret redaction in returned evidence;
- replay evidence hashing;
- cleanup verification before reporting success.

### 3.6 Evidence status semantics

BLK-test evidence must remain evidence only.

Allowed evidence statuses for future pilot design may include PASS, FAIL, BLOCKED, FATAL, transport-error, interrupted, stale, malformed, unknown, and replay-rejected states. None of these states authorizes source mutation, active-vault reads, BEO publication, RTM generation, RTM drift rejection, or BLK-req promotion.

PASS evidence may support a later human review package only. It is not publication authority and not trace-closure authority.

---

## 4. Stop Conditions

Stop and require hostile review before proceeding if any proposed sprint or patch attempts to:

1. treat BLK-020's historical first-smoke PASS as reusable production BLK-test MCP authority;
2. start a live BLK-test MCP server without separate BLK-test-specific human approval;
3. allow arbitrary shell, caller-supplied commands, dynamic tools, package managers, model calls, network calls, or cyber tooling;
4. let BLK-test mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source;
5. let BLK-test read, copy, parse, hash, mutate, or compare protected BLK-req vault bodies;
6. run BLK-test against `/home/dad/BLK-System`, a real target repository, a `.git` root, a `.git` ancestor, a `.git` descendant, root, home, protected-vault, or host-secret paths without a later explicit pilot authority and proof envelope;
7. convert BLOCKED, FATAL, transport-error, interrupted, malformed, stale, unknown, replayed, or missing evidence into success;
8. publish authoritative BEOs from BLK-test evidence;
9. generate RTM or make RTM drift decisions from BLK-test evidence;
10. claim production sandbox/cgroup/VM/network/host-secret isolation without tests and explicit authority.

---

## 5. Future-Sprint Split Table

| Future work | Required authority request | Must not inherit from |
| --- | --- | --- |
| Synthetic-smoke expansion | New one-run source/request/workspace/profile/tool approval envelope, deterministic tests, hostile review, and closeout. | BLK-020 first-smoke approval, Codex/live approval, execution approval, BEO approval, RTM approval. |
| L4 BLK-test pilot runtime | Separate pilot sprint with approved real-repo or real-artifact boundary, fixed tools, isolation proof, replay evidence, cleanup proof, and operator controls. | Synthetic smoke, disabled startup metadata, draft BEO fixtures, RTM design. |
| BEO publication implementation | Separate Track G publication sprint with signer/storage/ledger/rollback/revocation approval. | BLK-test PASS evidence, BLK-pipe execution approval, BLK-test approval, RTM approval. |
| RTM hash-only metadata path | Separate Track H design/implementation path with approved hash-only active-vault metadata access and no protected body reads. | BLK-test evidence, BEO draft fixtures, BEO publication approval, execution approval. |
| Production BLK-test MCP | Later L5 authority with monitoring, rollback, audit, sandbox/capability proof, operator controls, and active doctrine. | L4 pilot, synthetic smoke, disabled transport skeleton, local probes. |

---

## 6. BLK-001 through BLK-006 Alignment

| Governing doc | BLK-025 preservation |
| --- | --- |
| BLK-001 — Master Architecture | BLK-test remains the physics/evidence oracle, not a planner, source mutator, publication engine, or ledger generator. |
| BLK-002 — Artifact Lifecycle | BLK-req staging, approval, canonical hashing, and active-vault isolation remain separate from BLK-test. |
| BLK-003 — Orchestration Protocol | Phase 4.2 target architecture remains separate from current disabled/smoke/pilot authority; human gates and hostile audit remain required. |
| BLK-004 — BLK-pipe V47 Suite | BLK-pipe remains source mutation and Git authority; BLK-test cannot broaden allowlists or mutate source. |
| BLK-005 — BLK-Req Specification | Traceability uses opaque canonical metadata only; BLK-test cannot make active-vault truth or coverage claims. |
| BLK-006 — BLK-Req Implementation Brief | Protected-vault body reads remain denied to tactical and verification layers unless a later safe backend path is explicitly authorized. |

---

## 7. Final Boundary Thesis

BLK-test is allowed to become more useful only by becoming more bounded first. The next safe step is not production BLK-test MCP; it is explicit pilot-readiness doctrine that names every proof required before pilot runtime can be requested.

BLK-025 therefore keeps BLK-test as evidence only, preserves the existing BLK-017 through BLK-020 ladder, and blocks implicit authority inheritance between smoke evidence, pilot runtime, BEO publication, and RTM trace closure.
