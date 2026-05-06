# BLK-SYSTEM-011 — Transport Boundary Review

**Status:** Active Sprint 011 review gate
**Purpose:** Govern the disabled BLK-test MCP transport skeleton before any transport code is written.
**Scope:** Deterministic local review artifact for a disabled BLK-test MCP transport skeleton and non-executing handshake gate.

---

## 1. Scope and source documents

This review binds BLK-SYSTEM-011 to the current BLK-System doctrine and Sprint 010 readiness artifacts:

- `docs/BLK-001_blk-system-master-architecture.md`
- `docs/BLK-003_blk-pipe-blk-test-orchestration.md`
- `docs/BLK-008_blk-test-mcp-execution-server.md`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`
- `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`
- `docs/outcomes/BLK-SYSTEM-010_sprint-closeout.md`
- `docs/reviews/BLK-SYSTEM-010_fixture-to-live-gap-register.md`
- `docs/reviews/BLK-SYSTEM-010_approval-and-authority-decision-register.md`
- `docs/reviews/BLK-SYSTEM-010_sandbox-capability-readiness-spec.md`
- `docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md`

Sprint 011 is a local contract/probe sprint only. It records the transport boundary that later implementation tasks must preserve. It is stdio-only, disabled by default, and non-executing. It does not create live BLK-test MCP authority.

---

## 2. BLK-001 domain preservation matrix

| BLK-001 domain | Sprint 011 preservation requirement | Transport-boundary rule |
| --- | --- | --- |
| `blk-req` Legislative Gateway | Requirements and use cases remain HITL-authorized immutable active-vault artifacts. | Sprint 011 does not read protected BLK-req vault bodies, does not parse requirement bodies, and does not infer law from protected requirement/use-case content. |
| Architecture & Feature Planning | Hermes/planning artifacts translate bounded work; BLK-test is not an architect or router. | Sprint 011 may define disabled transport metadata and gate criteria only. It does not assign scope, architecture, requirements, or sprint authority to BLK-test. |
| `blk-pipe` Blast Shield & Forge | Source mutation, staging, forge/blast-shield control, and deterministic mutation remain owned outside BLK-test. | The disabled skeleton must not mutate source, must not stage files, must not commit, and must not replace `blk-pipe`. |
| `blk-test` Physics Oracle | BLK-test may later verify physical reality and return bounded evidence. | Sprint 011 defines a disabled BLK-test MCP transport skeleton and a non-executing handshake gate only; it does not execute fixed-tool tests. |
| RTM Aggregator Ledger | RTM remains a separate offline ledger comparing BEO trace hashes against active-vault hashes. | Sprint 011 does not authorize RTM generation and does not authorize RTM drift rejection authority. |
| Cryptographic baton | `version_hash` remains opaque source-bound evidence shared across domains. | Sprint 011 may preserve the concept of canonical `trace_artifacts[*].version_hash == sha256:<64-lowercase-hex>` but does not inspect active-vault bodies or publish authoritative outcomes. |

---

## 3. Sprint 011 authority-denied list

BLK-SYSTEM-011 explicitly denies these authorities:

- does not authorize live BLK-test MCP;
- does not authorize live MCP client/server startup;
- does not execute fixed-tool tests;
- does not authorize authoritative BEO publication;
- does not authorize RTM generation;
- does not authorize RTM drift rejection authority;
- does not read protected BLK-req vault bodies;
- must not mutate source;
- must not grant arbitrary shell;
- must not create HTTP, WebSocket, TCP, UDP, daemon, listener, background service, or network callback behavior;
- must not spawn subprocesses, launch MCP SDK clients/servers, install package-manager dependencies, run cyber tooling, call model services, or run live tactical LLMs;
- must not grant active-vault read authority, source-write authority, stage/commit authority, BEO publication authority, or RTM authority.

Any later approval-looking input, token, flag, or operator assertion remains unsupported in Sprint 011. Approval data may be described as future-boundary metadata only; it cannot enable live transport or execution.

---

## 4. Dependency-free disabled transport approach

The permitted Sprint 011 implementation shape is dependency-free Python contract/probe code and Markdown gates. The transport descriptor may state a future target transport of `stdio`, but that descriptor is metadata only.

Required approach:

1. The skeleton is stdio-only metadata and cannot open sockets or listeners.
2. Startup is disabled by default and must fail closed.
3. The non-executing handshake gate records that no MCP handshake is performed.
4. Fixed tool registry entries, if added in later Sprint 011 tasks, are descriptors only and have no executor.
5. All live side-effect indicators must remain false: no server process, no client process, no subprocess, no network call, no fixed-tool test, no source mutation, no active-vault body read, no BEO publication, and no RTM generation.
6. Persistent gates must scan/verify these markers before allowing later Sprint 011 task commits.

---

## 5. Handoff boundaries to Sprint 012 and Sprint 013

Sprint 012 owns workspace/process controls. Sprint 011 cannot claim production workspace isolation, process kill, timeout, output flood handling, stale lock cleanup, sandbox/cgroup/VM enforcement, cache jailing, network policy enforcement, or secret isolation. Any lifecycle artifact in Sprint 011 is a deterministic data-shape probe only.

Sprint 013 owns approval/source-evidence authorization mechanics. Sprint 011 cannot implement the approval channel, validate human approval tokens, bind operator identity, authorize source evidence, authorize `beb_id` evidence, permit live startup, or convert approval-looking records into execution authority.

The handoff condition is therefore narrow: Sprint 011 may leave behind review artifacts, disabled metadata, startup refusal decisions, non-executing handshake evidence, lifecycle data-shape evidence, and fixed registry descriptors. It may not cross into Sprint 012 execution controls or Sprint 013 approval/source-evidence authorization.

---

## 6. Pass/fail criteria

Sprint 011 Task 1 passes only when:

1. This review artifact exists at `docs/reviews/BLK-SYSTEM-011_transport-boundary-review.md`.
2. A persistent unittest gate proves the artifact includes all required disabled/non-executing authority-denial markers.
3. The focused doctrine review gate passes after the artifact is written.
4. Shared Python and Go verification passes without introducing execution behavior.
5. The task outcome records RED/GREEN evidence and repeats the explicit non-execution statement.

Sprint 011 Task 1 fails if any artifact implies that BLK-SYSTEM-011 authorizes live BLK-test MCP, live MCP client/server startup, fixed-tool test execution, authoritative BEO publication, RTM generation, RTM drift rejection authority, active BLK-req vault reads, source mutation, arbitrary shell, workspace/process controls, or approval/source-evidence authorization mechanics.
