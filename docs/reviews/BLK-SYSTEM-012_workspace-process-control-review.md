# BLK-SYSTEM-012 — Workspace Process-Control Boundary Review

**Status:** Active Sprint 012 review gate
**Date:** 2026-05-06
**Purpose:** Govern Workspace Isolation and Process-Control Implementation Probes before any workspace/process probe code is written.
**Scope:** Deterministic local review artifact for BLK-test MCP readiness controls using deterministic local inert fixtures only.

---

## 1. Scope and source documents

This review binds BLK-SYSTEM-012 to active BLK-System doctrine and prior readiness artifacts:

- `docs/BLK-001_blk-system-master-architecture.md`
- `docs/BLK-003_blk-pipe-blk-test-orchestration.md`
- `docs/BLK-008_blk-test-mcp-execution-server.md`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`
- `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`
- `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md`
- `docs/outcomes/BLK-SYSTEM-011_sprint-closeout.md`
- `docs/reviews/BLK-SYSTEM-010_fixture-to-live-gap-register.md`
- `docs/reviews/BLK-SYSTEM-010_sandbox-capability-readiness-spec.md`
- `docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md`
- `docs/reviews/BLK-SYSTEM-011_transport-boundary-review.md`

BLK-SYSTEM-012 is a local probe sprint only. It records and gates workspace clone/isolation decisions, path guards, teardown shape, lock behavior, process-tree kill paths, timeout handling, output-flood cleanup, cache/environment bounds, and replay evidence shapes. It does not create live BLK-test MCP authority.

Sprint 012 may use dependency-free Python `unittest` probes and synthetic marker-protected temp fixture trees. Those probes are deterministic local inert fixtures only, not production execution authority and not a substitute for later human-approved live smoke work.

---

## 2. BLK-001 domain preservation matrix

| BLK-001 domain | Sprint 012 preservation requirement | Workspace/process boundary rule |
| --- | --- | --- |
| `blk-req` Legislative Gateway | Requirements and use cases remain HITL-authorized immutable active-vault artifacts. | Sprint 012 does not read protected BLK-req vault bodies, does not parse protected requirement/use-case bodies, and does not copy those bodies into probe output, replay evidence, BEO-like fields, or RTM-like fields. |
| Architecture & Feature Planning | Hermes/planning artifacts define bounded work; BLK-test is not an architect, router, or source-of-truth selector. | Sprint 012 may define local probe contracts and evidence shapes only. It does not assign scope, choose architecture, interpret requirements, or approve work. |
| `blk-pipe` Blast Shield & Forge | Deterministic source mutation, staging, Git allowlists, forge authority, and blast-shield authority remain outside BLK-test. | Sprint 012 probe code does not mutate primary repo, does not stage files, does not commit, does not push, and does not replace `blk-pipe`. Human sprint execution may commit reviewed task work and outcome docs through the normal BLK-System Git workflow. |
| `blk-test` Physics Oracle | BLK-test may later verify physical reality and return bounded evidence. | Sprint 012 proves only inert workspace/process/resource controls. It does not authorize live BLK-test MCP, does not authorize live MCP client/server startup, and does not execute fixed-tool tests. |
| RTM Aggregator Ledger | RTM remains a separate offline ledger comparing BEO trace hashes against active-vault hashes. | Sprint 012 does not authorize RTM generation and does not authorize RTM drift rejection authority. Replay evidence cannot become an RTM or RTM rejection gate. |
| Cryptographic baton | `version_hash` remains opaque source-bound evidence shared across domains. | Sprint 012 may preserve canonical trace metadata shape references such as `sha256:<64-lowercase-hex>` but does not inspect active-vault bodies and does not authorize authoritative BEO publication. |

---

## 3. Authority-denied list

BLK-SYSTEM-012 explicitly denies these authorities:

- does not authorize live BLK-test MCP;
- does not authorize live MCP client/server startup;
- does not execute fixed-tool tests;
- does not mutate primary repo;
- does not stage files;
- does not commit;
- does not authorize authoritative BEO publication;
- does not authorize RTM generation;
- does not authorize RTM drift rejection authority;
- does not read protected BLK-req vault bodies;
- does not claim production sandbox/cgroup/VM enforcement;
- does not claim production host-secret isolation;
- must not grant arbitrary shell, dynamic command execution, source-write, staging, commit, autofix, cyber tooling, network callbacks, daemons, sockets, HTTP, WebSockets, TCP, or UDP;
- must not run live BLK-pipe, live Codex, live tactical LLM execution, package-manager installs, production sandbox/container/cgroup/VM setup, or production secret-isolation enforcement.

Any approval-looking field, token, operator assertion, source evidence reference, or `beb_id` reference remains non-authorizing metadata in this sprint. Sprint 013 owns approval/source-evidence authorization mechanics.

Any future first live fixed-tool BLK-test MCP smoke is out of scope. Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke.

---

## 4. Allowed probe shapes

Sprint 012 may add only deterministic local probes with these properties:

1. Dependency-free Python standard-library code and `unittest` gates.
2. Synthetic source/workspace fixtures under test-owned temporary roots.
3. Marker files and ownership tokens before any cleanup helper may delete a directory.
4. Path guards that reject absolute paths, `..` traversal, symlink escapes, and protected vault prefixes such as `docs/active`, `docs/requirements`, and `docs/use_cases`.
5. Hardlink/same-filesystem clone-decision probes that acknowledge hardlinks are not write isolation and prove the source manifest remains unchanged.
6. Startup purge and teardown probes limited to marked test-owned roots, never `/`, `$HOME`, the repository root, the current working directory, unmarked directories, glob expansion, or symlink escapes.
7. Atomic lock probes under test-owned temporary roots only, with stale/live lock distinctions and parallel prevention evidence.
8. Fixed inert Python child/grandchild process probes for timeout, process-tree kill, and output-flood cleanup. The process descriptor may say `inert_subprocess_called`; it must not expose arbitrary command execution.
9. Cache and environment probes using run-scoped cache roots and synthetic environment maps, never real host-secret dumps.
10. Replay bundles that are bounded, deterministic, non-authoritative, and scrubbed of protected bodies, secrets, raw unbounded logs, BEO publication fields, RTM generation fields, and RTM drift rejection fields.

---

## 5. Stop conditions

Sprint 012 work must stop for human review if an implementation or artifact attempts to:

- start any live MCP client or server;
- perform a JSON-RPC/MCP handshake;
- call the Sprint 011 fixed-tool registry executors or execute any fixed-tool test;
- target `/home/dad/BLK-System` as a probe workspace;
- run `git clone`, `git worktree`, `git add`, `git commit`, `git stash`, broad reset/checkout/revert, or source staging inside probe code/tests;
- inspect protected active-vault requirement/use-case bodies;
- publish authoritative BEO data or generate an RTM;
- claim production sandbox/cgroup/VM enforcement or production host-secret isolation;
- add shell execution, `shell=True`, `os.system`, `eval`, `exec`, package-manager network installs, network sockets, daemons, listeners, HTTP, WebSocket, TCP, UDP, or cyber tooling.

---

## 6. Pass/fail criteria

Sprint 012 Task 1 passes only when:

1. This review artifact exists at `docs/reviews/BLK-SYSTEM-012_workspace-process-control-review.md`.
2. A persistent `unittest` doctrine gate verifies the required inert/non-authorizing markers.
3. The focused doctrine review gate passes after the artifact is written.
4. Shared Python and Go verification passes without introducing workspace/process execution behavior.
5. The task outcome records RED/GREEN evidence, shared verification evidence, review results, implementation commit/push status, and the explicit non-authority statement.

Sprint 012 Task 1 fails if any artifact implies that BLK-SYSTEM-012 authorizes live BLK-test MCP, live MCP client/server startup, fixed-tool test execution, primary repo mutation, staging, commits, authoritative BEO publication, RTM generation, RTM drift rejection authority, active BLK-req vault body reads, production sandbox/cgroup/VM enforcement, production host-secret isolation, approval/source-evidence authorization, or the first live fixed-tool BLK-test MCP smoke.
