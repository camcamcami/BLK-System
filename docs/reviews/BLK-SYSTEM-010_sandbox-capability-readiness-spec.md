# BLK-SYSTEM-010 — Sandbox, Workspace, and Tool Capability Readiness Spec

**Status:** Task 4 review artifact
**Sprint:** `blk-system-010`
**Purpose:** Specify readiness controls for a future live BLK-test MCP environment while preserving Sprint 010 as deterministic local review/design work only.

---

## 1. Boundary statement

This spec is a readiness and gate-design artifact only. Sprint 010 does not authorize live BLK-test MCP. Sprint 010 does not authorize authoritative BEO publication. Sprint 010 does not authorize RTM generation. It does not authorize live MCP transport, live Codex, live tactical LLM calls, cyber execution, authoritative BEO publication, RTM drift rejection authority, active BLK-req vault reads, production approval-channel mechanics, or production host-secret isolation claims.

This spec is not production sandbox/cgroup/VM enforcement. It does not claim that a later Node/TypeScript MCP process, filesystem clone, lockfile, process group, cache jail, environment scrubber, or network policy is equivalent to a production container, cgroup, VM, SELinux/AppArmor profile, or hardware isolation boundary.

The future BLK-test MCP role remains fixed: a deterministic Physics Oracle that consumes already-produced BLK-pipe source evidence and emits bounded PASS/FAIL/BLOCKED evidence. It must not mutate source, choose architecture, publish BEOs, generate RTM, reject RTM drift, parse protected BLK-req vault bodies, or replace `blk-pipe` as the blast shield/forge.

---

## 2. Workspace lifecycle requirements

A future implementation sprint must prove the workspace lifecycle before any live transport is allowed:

1. stdio-only MCP transport readiness is the only permitted transport target; HTTP, WebSocket, daemon, network callback, and ambient service modes remain out of scope.
2. Startup purge must run before transport readiness is declared. It must remove only known stale BLK-test MCP workspace/cache paths and stale dead-PID lockfiles, never arbitrary directories.
3. The hardlink/same-filesystem clone decision and fallback must be explicit. The preferred path is a same-filesystem hardlink clone of the approved source tree; if the source and scratch location are not on the same filesystem, the process must fail closed or use a predeclared same-filesystem fallback, never silently copy from the primary repo into an unbounded location.
4. The live workspace must be isolated from the primary repo. Primary repo corruption prevention requires all test commands to operate only inside the approved ephemeral workspace and to reject path traversal or symlink escape back to the primary repository.
5. Per-run teardown must run in `finally`-equivalent paths after PASS, FAIL, BLOCKED, FATAL_TIMEOUT, FATAL_OUTPUT_FLOOD, transport error, and operator interruption. Teardown must remove the workspace, run-scoped cache directories, and run-scoped lock metadata after child processes are dead.
6. Stale lockfile behavior must distinguish a live PID from a dead PID, remove only dead-PID lockfiles, and produce deterministic BLOCKED/LOCKED evidence when a valid live lock exists beyond the bounded wait policy.
7. Single-run mutex/lock behavior must be atomic. Parallel prevention must be mechanically tested so a second concurrent request cannot interleave process execution, workspace mutation, log capture, or teardown with the active run.

Required future evidence: tests that simulate stale lockfiles, live lockfiles, same-filesystem and non-same-filesystem clone decisions, path traversal, interrupted runs, and all terminal status teardown paths.

---

## 3. Tool capability registry requirements

A future BLK-test MCP server may expose only a fixed tool list with Zod/schema validation on every tool input and output. Tool names, accepted fields, enum values, timeout classes, output budgets, workspace path policies, and source-evidence bindings must be statically declared and reviewable.

The registry must prove:

| Capability area | Readiness requirement | Disallowed authority |
| --- | --- | --- |
| Transport | stdio-only MCP transport readiness with fail-closed startup preconditions. | No HTTP/WebSocket listener, daemon socket, background network service, or live transport without human authorization. |
| Tool list | A fixed tool list for deterministic BLK-test profiles only. | No wildcard tools, plugin-discovered tools, arbitrary user-supplied test definitions, or generated tool names. |
| Validation | Zod/schema validation rejects missing fields, extra fields, changed types, path escapes, unapproved profile names, and unbound source evidence. | No permissive JSON passthrough or free-form shell argument surface. |
| Commands | Each tool maps to a predeclared physical check with bounded args. | No dynamic command execution tool, no shell/eval/exec tool, no arbitrary subprocess wrapper, no auto-fix, no source mutation. |
| Source binding | Each request must bind `beb_id`, source `commit_hash`, `pre_engine_hash`, canonical `trace_artifacts`, source BLK-pipe report identity, test profile, and workspace identity. | No verification of a guessed branch, unbound working tree, stale report, or protected BLK-req vault body. |

The no dynamic command execution tool rule is absolute. A future registry that exposes `shell`, `exec`, `run_command`, `bash`, `npm <freeform>`, `python <freeform>`, remote fetch, auto-fix, file-write, stage, commit, BEO publication, RTM generation, or active-vault read capabilities fails readiness.

---

## 4. Process/resource controls

Future process controls must be proven under deterministic local tests before live BLK-test MCP can run against any real repository:

1. Child process group kill behavior must terminate the full process tree, including descendants that outlive the direct child. The lock must not release until process death is observed or a deterministic fatal cleanup status is emitted.
2. Timeout and output-flood response must share the same kill path. A timeout and a volumetric flood both produce bounded evidence, preserve the fatal reason, stop reading unbounded output, kill descendants, and run teardown before allowing another run.
3. Output limits must be enforced before context-flooding Hermes. Output compression must preserve first/last relevant failure context, deduplicate repeated errors, record truncation metadata, and cap emitted logs.
4. Exit-code mapping must preserve PASS/FAIL/BLOCKED/FATAL distinctions. Infrastructure failure, approval failure, locked state, timeout, and output flood must not be laundered into PASS or authoritative BEO/RTM evidence.
5. Process execution must inherit only the approved scrubbed environment, approved working directory, and approved cache paths.

Required future gates: native process tests for timeout, output flood, nonzero exit, orphan descendant, signal interruption, cache write attempt, workspace escape attempt, and second-run-after-failure cleanup.

---

## 5. Cache/network/secret policy requirements

Cache jailing and environment scrubbing are readiness prerequisites, not production sandbox claims.

Future implementation must define:

- cache jailing for every tool and child process, using run-scoped cache roots that are outside the primary repo and removed during teardown;
- environment scrubbing with an explicit allowlist, rejecting credentials, tokens, API keys, SSH agents, cloud provider variables, package-manager auth, and unrelated host paths;
- network policy that is disabled by default or strictly bounded per explicitly approved test profile, with evidence that no uncontrolled network call occurs;
- secret exposure policy that prevents host secrets, protected BLK-req vault bodies, active requirements/use-case bodies, and operator approval secrets from being copied into logs, replay bundles, BEO fixtures, or RTM-like fields;
- dependency/cache behavior that avoids writing into the hardlinked workspace or primary repo.

This policy must be verified by deterministic probes that inspect the effective child environment, network posture, cache paths, and replay output. Passing these probes still does not create production sandbox/cgroup/VM enforcement.

---

## 6. Evidence and replay requirements

Evidence artifacts required for replay must be bounded, deterministic, and sufficient for Hermes hostile audit without storing protected bodies or secrets.

A future replay bundle must include at least:

1. approval record identity and operator timestamp when implemented;
2. source BLK-pipe report identity;
3. `beb_id`, source `commit_hash`, `pre_engine_hash`, canonical `trace_artifacts`, test profile, and workspace identity;
4. tool name, schema version, fixed argument set, timeout/output profile, and transport mode;
5. workspace clone decision, fallback decision if any, lock acquisition/release events, startup purge result, and per-run teardown result;
6. child process status, exit code or fatal reason, process group kill result, output byte counts, compression/truncation metadata, and deduplicated failure summaries;
7. cache/network/secret policy probe summaries;
8. explicit PASS/FAIL/BLOCKED/FATAL status mapping and non-authority notes for BEO/RTM.

Replay artifacts must exclude protected BLK-req vault bodies, host secrets, package tokens, raw unbounded logs, arbitrary filesystem listings, and any authority fields that imply BEO publication or RTM generation.

---

## 7. Future implementation gates

A later sprint may start implementation only after the following gates are accepted:

1. A non-executing disabled transport skeleton gate proves stdio-only MCP transport readiness while still disabled by default.
2. A fixed tool registry gate proves fixed tool list and Zod/schema validation, plus rejection of any no dynamic command execution tool violation.
3. Workspace gates prove hardlink/same-filesystem clone decision and fallback, startup purge, per-run teardown, stale lockfile behavior, single-run mutex/lock, parallel prevention, and primary repo corruption prevention.
4. Process gates prove child process group kill behavior, timeout and output-flood response, output compression, and status preservation.
5. Cache/network/secret gates prove cache jailing, environment scrubbing, network policy, secret exposure policy, and exclusion of protected BLK-req vault bodies.
6. Replay gates prove evidence artifacts required for replay are complete, bounded, deterministic, and non-authoritative.
7. Non-authority gates prove the implementation does not authorize authoritative BEO publication, does not authorize RTM generation, does not authorize RTM drift rejection authority, and does not grant active-vault read authority.

Task 4 therefore records readiness controls only. It does not implement the controls, start a server, run a live MCP client, run cyber tooling, contact network model services, or approve any live BLK-test MCP execution.
