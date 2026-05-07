# BLK-003 — BLK-pipe & BLK-test Orchestration Protocol

**Status:** Active Operating Doctrine
**Purpose:** Define the strict autonomous orchestration rules for Hermes invoking the tactical coding engine via `blk-pipe` and verifying physical reality via `blk-test`. Hermes acts as the autonomous CI/CD pipeline, Architect, and Hostile Auditor; the engine acts as the tactical worker; `blk-pipe` acts as the blast-shield transport layer; `blk-test` acts as the deterministic physics oracle.

---

## 0A. The Orchestration Stack

The `blk-system` execution pipeline utilizes a strict architecture to prevent LLM context-flooding, environment drift, and zombie processes:

### Tier 1 — Architect + Hostile Auditor: **Hermes**
* Reads and retains the full BEB and all governing documents.
* Resolves all architecture, contract, and scope decisions before the worker is invoked.
* Produces the Layer 2 tactical packet and the `SprintPayload` JSON object.
* Manages state iterations via atomic YAML frontmatter updates.
* Performs the two-phase hostile audit (POSIX exit-code routing and `blk-test` physics evaluation).
* **Cost profile:** Expensive for reasoning; cheap for routing/auditing.

### Tier 2a — Transport & Isolation Layer: **BLK-pipe (V47)**
* A compiled, deterministic Go binary executed synchronously by Hermes.
* Mechanically enforces file allowlists, instantly erasing unauthorized hallucinated edits before commits.
* Enforces bounded POSIX process-group termination for runaway engine loops; on clean exits it waits for inherited stdout/stderr pipes to close, while escaped descendants that close or redirect those pipes remain outside portable POSIX containment.
* Hard-aborts on validation failures (Exit 2), unauthorized mutations (Exit 3), or volumetric engine output floods (Exit 5).
* Verifies Git ancestry before reverts (Exit 4), protecting the repository from hallucinated rollbacks.
* **Cost profile:** Negligible. It is a strict, non-reasoning state machine.

### Tier 2b — Physics Oracle: **blk-test**
* A local, stdio-based MCP test execution server in TypeScript that clones the sprint branch into an ephemeral `/var/tmp` directory.
* Executes heavy native verification tests (Electron IPC, memory bounds) safely without granting the agent arbitrary shell access.
* Compresses and deduplicates raw `stderr` logs to protect the token context window.
* Utilizes OS-level atomic file descriptor locks (`wx`) to prevent TOCTOU execution races.

### Tier 3 — Tactical Implementer: **Codex / Engine**
* Receives **only** the Layer 2 tactical packet via standard input from `blk-pipe`.
* Executes bounded tactical work: file edits and evidence generation.
* Has no architectural authority and operates strictly within the 15-minute POSIX execution window enforced by `blk-pipe`.
* **Cost profile:** Expensive; reserved strictly for tactical execution.

---

## 0B. Current implementation boundary after Sprint 007

BLK-003 describes the target orchestration architecture, but it does not by itself authorize every target-state component today. After Sprint 007, the implemented local boundary is narrower:

- `fixture-only BLK-test` handoff objects and source-bound disabled adapter smoke wrappers are supported for deterministic local tests; `live BLK-test MCP remains disabled` under the fail-closed request/response contract in [BLK-015](BLK-015_blk-pipe-approval-and-mcp-integration-design.md) and the Sprint 007 contract in [BLK-016](BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md).
- The disabled adapter smoke helper `run_disabled_blk_test_mcp_adapter_smoke(...)` may return `DISABLED_SEND_BLOCKED` or `FIXTURE_RESPONSE_MAPPED`; the not-run builder `build_blk_test_mcp_not_run_request(...)` preserves non-success source metadata without treating it as evaluation evidence.
- `draft-only BEO` projection is supported through [BLK-014](BLK-014_blk-execution-outcome-fixture-shape.md) and [BLK-016](BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md); authoritative BEO publication remains disabled.
- BEO/RTM interface fixtures may preserve opaque `trace_artifacts` / canonical `version_hash` metadata only; `RTM generation remains disabled` and no fixture compares hashes against live BLK-req vault files.
- `codex-live` approval-token validation is audit-only and remains non-executable until a later sprint explicitly authorizes a live path; sandbox/capability enforcement is later work, and approval-channel mechanics are later work.
- BLK-020 first-smoke evidence contract records the single accepted first live fixed-tool smoke exception from BLK-SYSTEM-014. This exception is historical, source-bound, synthetic, and one-run; generic/production BLK-test MCP remains disabled and there is no new live BLK-test MCP authority.
- The BLK-020 exception does not authorize production BLK-test MCP, does not authorize source mutation as BLK-test behavior, does not read protected BLK-req vault bodies, does not authorize authoritative BEO publication, and does not authorize RTM generation or RTM drift rejection authority.

---

## 1. The Autonomous Orchestration Loop

Hermes must execute the following state machine for every engine-driven task.

### State 1 — BEB Generation & YAML State Tracking
Before invoking the engine, Hermes must write a formal **Blk Execution Brief (BEB)** and save it to `docs/execution briefs/BEB_###.md`.

**MANDATORY STATE TRACKING:** Hermes must inject a strict YAML frontmatter block at the very top of every BEB to permanently track the iteration state on the SSD:
```yaml
---
beb_id: "BEB_010"
iteration: 1
status: "IN_PROGRESS"
sprint_base_hash: "0123456789abcdef0123456789abcdef01234567"
trace_artifacts:
  - kind: "REQ"
    id: "REQ-042"
    version_hash: "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  - kind: "UC"
    id: "UC-004"
    version_hash: "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
---
```

The hash values above are synthetic fixture values for example shape only; a real BEB must use the canonical hashes returned by the BLK-002 retrieval/baseline path. They are not live BLK-req vault values.

The brief must define the exact task objective, architectural constraints, explicitly prohibited actions, required validation commands, **allowed modified files**, and **allowed new files**. Hermes must never send open-ended requests.

#### State 1.1 — Bounded Constraint Retrieval (BLK-002 Handshake)
Hermes is **STRICTLY FORBIDDEN** from reciting, inferring, or hallucinating architectural constraints from memory.
* Before defining the task objective, Hermes **MUST** execute the `fetch_requirements_context` tool, targeting the specific artifact IDs (e.g., `REQ-042`, `UC-004`) formally baselined via the **BLK-002 Protocol**.
* Hermes **MUST** extract the exact Canonical Hash returned by the tool and inject it into the structured `trace_artifacts` array in the BEB YAML frontmatter.

#### State 1.2 — The Scope Reconnaissance
Before constructing the BEB and finalizing the YAML frontmatter, Hermes **MUST** call the `analyze_dependency_graph` tool on the primary target file.

- Hermes **MUST** populate the `AllowedModifiedFiles` array using **only** the exact paths returned in the `dependencies` field of the tool response.
- Hermes is **STRICTLY FORBIDDEN** from guessing, hallucinating, or adding any file paths that were not explicitly returned by the `analyze_dependency_graph` tool.
- If the initial task directive explicitly names additional files that must be modified, Hermes may append them **after** incorporating the tool’s output, but must clearly document the reason in the BEB.

#### State 1.3 — Known Operational Limitation (V1.0)
The `analyze_dependency_graph` tool currently only resolves **outbound dependencies**. It does **not** scan the entire workspace for **inbound dependents**.

- **Rationale:** Deliberate V1 optimization to avoid parsing the entire repository's AST during planning, minimizing latency.
- **Impact:** Upstream files relying on an altered exported contract may not be included in `AllowedModifiedFiles`, causing an Exit 3 on the next iteration.

#### State 1.4 — Human Confirmation Gate (MANDATORY)
Hermes **MUST NOT** invoke the `ExecuteSprintTool` (which triggers `blk-pipe`) until the human operator has explicitly approved the dispatch for `iteration: 1`.
* **Presentation:** Hermes must present the generated `SprintPayload` parameters, a one-line summary, and the ALLOWLIST/FORBIDDEN constraints to the human.

### State 2 — BLK-pipe Invocation (Hermes → BLK-pipe)

#### State 2.1 — The Git Fortress
Hermes provides the `TargetBranch` in the `SprintPayload`.
* `blk-pipe` assumes complete control of the workspace upon invocation.
* It mechanically isolates the state by fetching from origin, establishing the target branch, and sterilizing the environment using `git clean -fd`.

#### State 2.2 — 2-Layer Handoff Protocol & Payload Constraints
Hermes constructs the `SprintPayload` JSON. The `l2_packet` string is the tactical execution brief injected into the engine.

Hermes MUST inject the following into `engine_args`:
* `"--json"`, `"--isolated"`, `"--yes"`.
* `"--deny-read=**/.git/**"`, `"--deny-read=**/node_modules/**"`, `"--deny-read=**/.env*"` to enforce filesystem blast radius confinement.

**MANDATORY VALIDATION CONSTRAINT:** Hermes **MUST** include a global workspace syntax check (e.g. `npx tsc --noEmit`) in the `validation_commands` array. This ensures upstream contract breakages are caught mechanically at the Syntax Gate (Exit 2).

**MANDATORY TACTICAL CONTEXT:** To satisfy the Context Economy constraint, the `l2_packet` MUST NOT contain the entire `BLK-Req` repository. Hermes MUST inject the exact, verbatim Markdown body of only the artifacts explicitly listed in the `trace_artifacts` array into the `l2_packet`. Truncating or summarizing these constraints before handing them to the tactical engine is strictly prohibited.

### State 3 — Tactical Execution (BLK-pipe / Codex)
`blk-pipe` pipes the `l2_packet` to the engine.
* **Hard Boundaries:** `blk-pipe` bounds the engine to a 15-minute execution window.
* **Mechanical Validation (Syntax Gate):** `blk-pipe` independently runs the shallow validation commands specified in the payload.
* **Strict Staging & Lockdown:** `blk-pipe` mechanically enforces the file allowlist. It selectively stages only authorized paths and silently runs `git checkout -- .` to erase unauthorized LLM edits, ensuring a sterile commit.

---

## 4. The Two-Phase Hostile Audit (Hermes)

Once the tactical engine completes its run, Hermes evaluates the physical reality of the code in two strict phases.

### Phase 4.1 — The Syntax & Scope Gate (POSIX Routing)
Hermes receives the `ExecutionResult` JSON and routes control flow strictly off mapped POSIX exit statuses:

* **Token Harvest:** Parse `engine_logs` as JSON to extract reasoning-token burn.
* **Status Evaluation:**
    * If `SUCCESS` (Exit 0): Proceed to Phase 4.2.
    * If `SYNTAX_GATE_FAILED` (Exit 2): Skip Phase 4.2 and proceed to Loop Control.
    * If `UNAUTHORIZED_FILE_MUTATION` (Exit 3): Skip Phase 4.2 and proceed to Loop Control.
    * If `FATAL_OUTPUT_FLOOD` (Exit 5): Skip Phase 4.2 and proceed to Loop Control.
    * If `FATAL_SYSTEM_PANIC` or `FATAL_PYTHON_TIMEOUT` (Exit 1): Halt immediately and escalate to human.

### Phase 4.2 — The Physics Oracle (blk-test Evaluation; Target Architecture)
In the future approved target architecture, Hermes invokes `blk-test` against the newly committed branch to run deep structural verification.
* Hermes reads the compressed, deduplicated JSON payload.
* *Target Verdict 4.2:* If status is `PASS`, Hermes may generate a successful BEO document. If `FAIL` or `FATAL_OUTPUT_FLOOD`, Hermes extracts the 1-sentence Root Cause Hypothesis and Affected Files, then proceeds to Loop Control.

**Current implementation boundary after Sprint 019:** Phase 4.2 target architecture remains broader than current production authority. BLK-020 first-smoke evidence contract records the single accepted first live fixed-tool smoke exception under explicit human approval; that evidence is synthetic, source-bound, and one-run only. Generic/production BLK-test MCP remains disabled, and the BLK-020 exception grants no new live BLK-test MCP authority, no source mutation as BLK-test behavior, no protected BLK-req vault body reads, no authoritative BEO publication, no RTM generation, and no RTM drift rejection authority. Outside that recorded BLK-020 evidence contract, Phase 4.2 is represented only by `fixture-only BLK-test` handoff objects, disabled adapter smoke shapes in [BLK-016](BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md), and disabled BLK-test MCP stubs; PASS/FAIL mapping is source-bound under [BLK-015](BLK-015_blk-pipe-approval-and-mcp-integration-design.md), and any BEO-shaped projection remains `draft-only BEO` fixture output under [BLK-014](BLK-014_blk-execution-outcome-fixture-shape.md) and [BLK-016](BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md). Authoritative BEO publication and RTM generation remain disabled.

### Phase 4.3 — Loop Control & Iteration Tracking
When Phase 4.1 or 4.2 fails, Hermes MUST manage the state to prevent infinite loops using a **MANDATORY POSIX ATOMIC RENAME** (write to `.tmp`, then `os.rename()`).

1. **Read & Increment:** Hermes increments `next_iteration = current_iteration + 1` in the active BEB YAML.
2. **The Fix BEB Generation (If next_iteration <= 3):**
   * Hermes writes the updated brief to `BEB_010.md.tmp`, executes atomic rename to overwrite `BEB_010.md`.
   * Hermes constructs the new `l2_packet` using *only* the Affected Files and the 1-sentence Root Cause Hypothesis extracted from the `blk-test` or `blk-pipe` failure.
   * If failure was `UNAUTHORIZED_FILE_MUTATION`, the `l2_packet` must reprimand the engine.
   * Hermes fires `blk-pipe` to execute the fix.
3. **The Failure Ceiling (If next_iteration > 3):**
   * Loop is physically halted.
   * Hermes invokes `abort_sprint_and_revert` via BLK-pipe using the **`sprint_base_hash`** to eradicate broken commits.
   * If `abort_sprint_and_revert` returns `INVALID_REVERT_ANCHOR` (Exit Code 4), halt immediately.
   * Hermes immediately triggers the **Human Escalation Protocol (§10)**.

---

## 5. Post-Execution: BEO — Blk Execution Outcome
In the future approved target architecture, after execution completes Hermes generates the `BEO_###.md` document alongside the BEB. In the current implementation boundary after Sprint 019, BLK-test returns verification evidence, not authoritative BEO publication authority. BEO handling is limited to a draft-only BEO fixture projection defined by [BLK-014](BLK-014_blk-execution-outcome-fixture-shape.md) and [BLK-016](BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md); authoritative BEO publication remains disabled, RTM generation remains disabled, and future/offline publication requires later explicit authority.

A target-state BEO must record:
* Summary of implementation.
* `blk-pipe` validation logs, `blk-test` physics results, and diff evidence.
* **Total token burn and telemetry extracted from `engine_logs`**.
* Constraint violations detected during the Hostile Audit.
* Was it an autonomous success, or did §10 trigger?
* **Traceability Inheritance:** Hermes **MUST** copy the `trace_artifacts` YAML array exactly as it appears in the BEB and inject it into the BEO's frontmatter. This mathematically binds the execution evidence to the BLK-002 architectural constraints for RTM aggregation.

---

## 10. Human Escalation Protocol (§10)

When the engine hits the failure ceiling (`iteration > 3`), triggers a system panic, or loses state coherence, Hermes MUST trigger a Human Escalation.

**Current implementation boundary after Sprint 019:** this escalation path halts the loop and creates a human escalation package. Any BEO-shaped artifact created for escalation is a `draft-only BEO` fixture unless a future sprint explicitly authorizes authoritative publication. BLK-test payloads may be included only when a source-bound fixture exists under the current disabled/fixture-only boundary, or when a future sprint explicitly authorizes a broader live BLK-test MCP path. BLK-020 first-smoke evidence contract remains the only recorded single accepted first live fixed-tool smoke exception and does not authorize production BLK-test MCP, source mutation as BLK-test behavior, protected BLK-req vault body reads, authoritative BEO publication, RTM generation, or RTM drift rejection authority. Generic/production BLK-test MCP remains disabled; authoritative BEO publication remains disabled; RTM generation remains disabled.

**Escalation procedure:**
1.  **Halt the loop.** Do not invoke `blk-pipe` again.
2.  **Create only a draft-only BEO-shaped fixture** with status: `FATAL: ESCALATION` if a BEO-shaped artifact is needed for the human escalation package. This is not authoritative BEO publication.
3.  **Write the human escalation package** to `.kuronode-packets/BEB_XXX_escalation.md`, including raw, un-truncated JSON payloads from `blk-pipe` and any currently available source-bound fixture BLK-test payloads. Do not invent live BLK-test evidence.
4.  **Present the handoff to the human operator**.
