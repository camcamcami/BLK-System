# BLK-018 — BLK-test MCP Workspace/Process-Control Probes

**Status:** Active workspace/process-control probe contract
**Scope:** BLK-SYSTEM-012 dependency-free local probes for inert workspace isolation, process control, cache/environment bounds, and replay evidence.

---

## 1. Purpose

BLK-018 makes the BLK-SYSTEM-012 accepted probe contract discoverable as active doctrine. It records what has been proven with deterministic local probes and preserves the boundary that those probes are inert local fixtures only.

BLK-018 is a successor readiness probe to BLK-017, not a live transport authorization. BLK-008 remains future target-state planning doctrine; BLK-017 remains the active disabled transport contract for stdio-only disabled transport metadata until live authority is separately approved by a later sprint.

---

## 2. Authority boundary

BLK-SYSTEM-012 and BLK-018 do not authorize live BLK-test MCP and do not authorize live MCP client/server startup. They do not execute fixed-tool tests, do not mutate primary repo, do not stage files, and do not commit as BLK-test behavior.

The contract also does not authorize authoritative BEO publication, does not authorize RTM generation, does not authorize RTM drift rejection authority, does not read protected BLK-req vault bodies, does not claim production sandbox/cgroup/VM enforcement, and does not claim production host-secret isolation.

Sprint 013 owns approval/source-evidence authorization mechanics. Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke. BLK-020 records the accepted BLK-SYSTEM-014 first-smoke evidence contract for a synthetic isolated workspace, but does not authorize production BLK-test MCP.

Human sprint-executor commits and pushes for reviewed probe code and outcome documentation are project-maintenance actions; they are not BLK-test source-mutation authority.

---

## 3. Accepted probe surface

BLK-018 covers only deterministic local probe functions and tests added during BLK-SYSTEM-012:

- workspace boundary descriptors and clone decisions;
- workspace-relative path guards and protected-vault rejection;
- run-scoped cache jail path selection;
- marker-protected fixture clone and teardown helpers;
- startup purge and root-anchored cleanup guards;
- atomic temp-root locks, stale-lock handling, and live-lock preservation;
- fixed inert child-process timeout, output-flood, descendant-kill, and pipe-holder no-hang probes;
- synthetic environment scrubbing;
- bounded output compression and replay evidence sanitization.

These probes may spawn fixed inert local Python subprocess probes only through the Sprint 012 process-probe harness. They must not expose shell execution, dynamic command construction, package manager execution, network listeners, live MCP transports, or fixed BLK-test tool execution.

---

## 4. Implementation and tests

Implementation and gate files:

- `python/blk_test_mcp_workspace_process_probes.py`
- `python/test_blk_test_mcp_workspace_process_probes.py`
- `python/test_active_doctrine_review_gates.py`

The implementation remains dependency-free Python standard library probe code. The test gates are `unittest` gates against synthetic marker-protected temporary fixtures. The probes must not target the primary repository as a workspace fixture and must not read protected active BLK-req vault bodies.

---

## 5. Relationship to BLK-008 and BLK-017

BLK-008 describes a future target-state BLK-test MCP execution server. BLK-018 does not make BLK-008 live; it supplies an inert workspace/process-control probe contract that informs future implementation readiness.

BLK-017 remains the active disabled transport contract. It proves disabled-by-default stdio transport metadata, startup refusal, and non-executing lifecycle shapes. BLK-018 does not supersede BLK-017 transport authority, does not start a server, does not start a client, and does not perform a JSON-RPC/MCP handshake.

Any future live BLK-test MCP work must explicitly preserve BLK-017 until it is separately superseded, satisfy BLK-018 workspace/process-control gates, and pass BLK-019 approval/source-evidence authorization before Sprint 014 may request explicit human approval for first live fixed-tool BLK-test MCP smoke. BLK-019 is the Sprint 013 approval/source-evidence authorization contract, but it does not authorize live BLK-test MCP, does not authorize authoritative BEO publication, and does not authorize RTM generation. It records validation evidence before Sprint 014, not live startup authority.

---

## 6. Non-authority checklist

BLK-018 preserves these explicit non-authority markers:

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
- does not claim production host-secret isolation.

---

## 7. Stop conditions

Stop and treat any future change as out of BLK-018 authority if it attempts to:

- start live MCP server/client transport;
- invoke fixed BLK-test tools against a real repository;
- mutate, stage, commit, or push source as BLK-test behavior;
- publish authoritative BEO output;
- generate RTM or make drift decisions;
- read active BLK-req vault body text;
- claim production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, or host-secret isolation enforcement.
