# BLK-047 — BLK-test Fixed-Tool Pilot Authority Request Boundary

**Status:** Active request-boundary contract — review package only; not runtime BLK-test authority
**Date:** 2026-05-09T19:28:48+10:00
**Purpose:** Define the non-executing authority request package required before any later BLK-test fixed-tool pilot runtime sprint can be approved.
**Scope:** BLK-045 Fork C — Complete the Right Side of the V-Model, first BLK-test frontier. This boundary is L0/L1 request/doctrine/fixture evidence only. It is not a sprint plan, not production BLK-test MCP authority, not live BLK-test transport authority, and not permission to execute fixed tools.

---

## 0. Boundary Markers

```text
BLK_TEST_FIXED_TOOL_PILOT_AUTHORITY_REQUEST_PACKAGE
BLK_TEST_PILOT_REQUEST_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY
FIXED_TOOL_PILOT_APPROVAL_REQUIRED_BEFORE_TRANSPORT
PRODUCTION_BLK_TEST_MCP_REMAINS_DISABLED
BLK_TEST_EVIDENCE_ONLY_NO_SOURCE_MUTATION
PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN
BEO_PUBLICATION_AND_RTM_REMAIN_SEPARATE_AUTHORITIES
PHYSICAL_ISOLATION_PROOF_REQUIRED_BEFORE_PILOT
REPLAY_EXPIRY_AND_SOURCE_BINDING_REQUIRED
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_044
```

Persistent doctrine gate marker: BLK-SYSTEM-044 pins BLK-test fixed-tool pilot authority request review-only scope.

---

## 1. Non-Execution and Non-Authority Boundary

BLK-047 is an authority request boundary and review package contract only. It does not authorize:

- production BLK-test MCP;
- live BLK-test server or client startup;
- new BLK-test smoke runs;
- replay of the BLK-SYSTEM-014 / BLK-020 historical first fixed-tool smoke;
- fixed-tool execution;
- arbitrary shell, caller-supplied commands, dynamic tool expansion, package-manager execution, model calls, network calls, browser tooling, or cyber tooling;
- source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test;
- BLK-test execution against `/home/dad/BLK-System`, real target repositories, `.git` roots, `.git` ancestors, `.git` descendants, root paths, home paths, protected BLK-req vault paths, host-secret-bearing paths, symlink escapes, traversal aliases, or unowned workspaces;
- protected BLK-req vault body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison;
- authoritative BEO publication;
- runtime RTM generation or RTM drift rejection;
- public ledger mutation;
- signer, storage, rollback, revocation, supersession, or release authority;
- production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claims.

Operator shorthand:

- No production BLK-test MCP authority.
- No live BLK-test server or client startup.
- No fixed-tool execution.
- No source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test.
- No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison.
- No authoritative BEO publication.
- No runtime RTM generation or RTM drift rejection.
- No package-manager, network, model-service, browser, or cyber tooling authority.
- No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim.

BLK-test remains evidence only. PASS, FAIL, BLOCKED, FATAL, transport-error, interrupted, stale, malformed, unknown, replayed, or policy-blocked evidence must not mutate source, publish BEOs, generate RTM, promote BLK-req artifacts, read protected bodies, create active requirement coverage, or make drift decisions.

---

## 2. Roadmap and Current-State Relationship

BLK-045 controls current roadmap selection after BLK-SYSTEM-042. BLK-046 identifies BLK-test as disabled/gated evidence only, with production MCP disabled and one historical synthetic fixed-tool smoke exception recorded by BLK-020.

BLK-047 advances BLK-045 Fork C only by defining the request package required before a later human approval decision. It does not skip from BLK-025 prerequisites to L3/L4 runtime. A later runtime sprint must explicitly cite BLK-047, name the approved maturity rung, and satisfy the approval/proof package here before any transport or fixed-tool execution can be considered.

---

## 3. Required Future Approval Envelope

A later BLK-test fixed-tool pilot runtime request must include a separate BLK-test-specific human approval grant. The grant must be distinct from:

1. Codex/live tactical approval.
2. BLK-pipe execution approval.
3. BLK-SYSTEM-014 / BLK-020 first-smoke approval.
4. BEO publication approval.
5. RTM generation approval.
6. RTM drift rejection authority.

The approval envelope must name:

- grant ID;
- source system and operator identity;
- message/event ID when available;
- issued timestamp and expiry timestamp;
- exact approved scope;
- exact target repository or synthetic workspace class;
- exact fixed tool registry and requested tool IDs;
- exact validation/test profile;
- exact timeout/output profile;
- exact forbidden adjacent authorities;
- replay IDs and used-run tracking;
- hostile-review checklist;
- operator stop/kill controls;
- cleanup and rollback obligations.

The envelope must be one-run/scoped, source-bound, expiry-bound, replay-resistant, and auditable. It must not be inferred from a sprint request, plan publication, previous smoke evidence, or a fixture's `READY_FOR_HUMAN_REVIEW` status.

---

## 4. Required Proof Obligations Before Pilot Runtime

A later runtime sprint must prove all of the following before startup or fixed-tool execution:

### 4.1 Fixed-tool registry proof

- No arbitrary shell.
- No caller-supplied command arrays.
- No wildcard or unknown tools.
- No dynamic tool expansion.
- No package-manager execution.
- No network, model-service, browser, or cyber capability.
- Deterministic repository-owned tool descriptors.

### 4.2 Source and evidence binding proof

- BLK-pipe report identity, `beb_id`, source commit hash, `pre_engine_hash`, and `post_engine_hash` bind to the request.
- Canonical trace artifacts use `sha256:<64-lowercase-hex>` version hashes.
- Requested fixed tools, test profile, workspace identity, timeout/output profile, approval identity, replay identifiers, and request hash bind exactly.
- Missing, mismatched, stale, replayed, malformed, BLOCKED, unknown, transport-error, interrupted, or policy-blocked evidence fails closed.

### 4.3 Physical and workspace isolation proof

- No execution against `/home/dad/BLK-System` unless a later plan explicitly approves that exact boundary and proves rollback/cleanup behavior.
- No `.git` root, `.git` ancestor, `.git` descendant, root path, home path, protected-vault path, host-secret path, symlink escape, traversal alias, or unowned workspace.
- Cleanup is verified before any success report.
- Protected-vault checks use path/metadata guards only and preserve no protected body reads.

### 4.4 Process, output, and operator-control proof

- Missing approval refuses before process start.
- Timeout, output flood, interrupt, descendant process, pipe-holder, and cleanup-failure paths return non-success evidence.
- Output is bounded and secret-redacted.
- Operator stop/kill controls exist and are tested.
- Runtime logs must not include protected body content or secret-bearing environment values.

---

## 5. Required Request Fixture Semantics

The deterministic request fixture created by BLK-SYSTEM-044 may report only:

```text
BLK_TEST_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
BLK_TEST_PILOT_REQUEST_BLOCKED_NOT_AUTHORIZED
BLK_TEST_PILOT_DISABLED_NOT_AUTHORIZED
```

The fixture must set every adjacent authority flag to false, including production BLK-test MCP, live transport, fixed-tool execution, source mutation, Git mutation, protected-body reads/copy/scan, BEO publication, RTM generation, drift rejection, package-manager/network/model/cyber/browser tooling, and production isolation claims.

A future runtime sprint must treat fixture readiness as advisory request evidence only. It is not BLK-test approval, not transport approval, not execution approval, not source mutation authority, not BEO publication authority, and not RTM trace-closure authority.

---

## 6. Stop Conditions

Pause and require hostile review plus a new human decision if any future sprint attempts to:

1. treat BLK-047 or the BLK-SYSTEM-044 fixture as runtime approval;
2. start live BLK-test MCP server/client transport before a separate BLK-test-specific approval grant exists;
3. reuse Codex, BLK-pipe, BLK-020, BEO, or RTM approvals as BLK-test pilot approval;
4. execute fixed tools before the proof obligations in Section 4 pass;
5. run against real repositories, `.git` paths, root/home/protected/host-secret paths, symlink escapes, or unowned workspaces without exact approval and proof;
6. let BLK-test mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source;
7. let BLK-test read, copy, parse, hash, summarize, scan, mutate, or compare protected BLK-req bodies;
8. convert PASS evidence into BEO publication, RTM generation, drift rejection, active coverage, or protected-vault truth;
9. use arbitrary shell, package managers, network, model-service, browser, or cyber tooling;
10. claim production sandbox or host-secret isolation without explicit authority and tests.

---

## 7. BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-047 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Preserve BLK-test as evidence oracle only; keep planning, mutation, publication, and trace closure separate. |
| BLK-002 — Artifact Lifecycle | Preserve HITL approval, staging isolation, active-vault immutability, and protected-vault boundaries. |
| BLK-003 — Orchestration Protocol | Preserve human gates, bounded context, hostile review, and no implicit inheritance between execution, verification, BEO, and RTM. |
| BLK-004 — BLK-pipe V47 Suite | Preserve BLK-pipe as source mutation/Git enforcement authority; BLK-test cannot broaden allowlists. |
| BLK-005 — BLK-Req Specification | Preserve canonical trace binding without protected-body leakage or coverage/drift claims. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny semantics and no tactical/verifier body reads. |

---

## 8. Final Boundary Thesis

BLK-047 makes the next BLK-test decision auditable without making it automatic. The system can now ask for a future BLK-test fixed-tool pilot approval using a bounded request package, but no transport, fixed-tool execution, or runtime verification authority exists until a later sprint receives explicit human approval and proves the required isolation, replay, output, cleanup, and stop-control behavior.
