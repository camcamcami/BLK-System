# BLK-003 — BLK-pipe & BLK-test Orchestration Protocol

**Status:** Active Operating Doctrine
**Purpose:** Define the strict autonomous orchestration rules for Hermes invoking the tactical coding engine via `blk-pipe` and verifying physical reality via `blk-test`. Hermes acts as the autonomous CI/CD pipeline, Architect, and Hostile Auditor; the engine acts as the tactical worker; `blk-pipe` acts as the blast-shield transport layer; `blk-test` acts as the deterministic physics oracle.

---

## 0. Fixed Overview Boundary

```text
BLK_001_TO_006_FIXED_OVERVIEW_NOT_SPRINT_STATE
```

This document is a stable overview/contract surface. Do not patch it with sprint-current-state, completion markers, roadmap handoffs, or per-sprint authority updates. Current implementation state belongs in `docs/BLK-077_blk-system-post-078-roadmap.md`, `docs/BLK-079_post-078-current-state-authority-index.md`, component-specific post-root BLK docs, code/tests, and the single sprint closeout outcome.

---

## 0A. The Orchestration Stack

The `blk-system` execution pipeline utilizes a strict architecture to prevent LLM context-flooding, environment drift, and zombie processes:

### Tier 1 — Architect/System Engineer + Hostile Auditor: **Hermes role**
* Reads and retains the full BEB and all governing documents.
* Resolves all architecture, contract, and scope decisions before the worker is invoked.
* The architect/system-engineer agent owns BEB and L2 authorship because those artifacts define product intent, architecture intent, execution intent, capability boundary, acceptance criteria, and target workflow.
* BLK-System validates, normalizes, hash-binds, performs route enforcement, and constructs `SprintPayload` JSON from the architect/system-engineer-authored BEB and L2; BLK-System must not author or rewrite L2 execution intent.
* BLK-System must not silently author its own BEB mission or L2 mission. A missing or underspecified BEB or L2 is a clarification required state, not permission for the execution layer to invent product, architecture, or execution intent.
* Manages state iterations via atomic YAML frontmatter updates.
* Performs the two-phase hostile audit (POSIX exit-code routing and `blk-test` physics evaluation).
* **Cost profile:** Expensive for reasoning; cheap for routing/auditing.

### Tier 2a — Transport & Isolation Layer: **BLK-pipe (V47)**
* A compiled, deterministic Go binary executed synchronously by Hermes.
* Mechanically enforces file allowlists, instantly erasing unauthorized hallucinated edits before commits.
* Enforces bounded POSIX process-group termination for runaway engine loops; on clean exits it waits for inherited stdout/stderr pipes to close, while escaped descendants that close or redirect those pipes remain outside portable POSIX containment.
* Hard-aborts on invalid payloads (Exit 8), validation failures (Exit 2), unauthorized mutations/protected allowlist violations (Exit 3), or volumetric engine output floods (Exit 5).
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
* Has no architectural authority and operates within the BLK-pipe execution-cap profile enforced by `blk-pipe`: the default profile is a 15-minute POSIX execution window and 50MB combined `stdout`/`stderr` output cap, but a caller may explicitly select different finite `timeout_seconds` / `max_output_bytes` values for a bounded run.
* **Cost profile:** Expensive; reserved strictly for tactical execution.

---

## 0B. Target-State vs Current Authority Boundary

BLK-003 defines the orchestration target model and durable handoff rules. It does not by itself grant current runtime authority for live Codex, BLK-pipe execution, BLK-test MCP, BEO publication, RTM generation, protected-body reads, or target/source/Git mutation. Current authority cutlines live in BLK-077, BLK-079, component-specific post-root BLK docs, code/tests, and sprint closeouts.

---

## 1. The Autonomous Orchestration Loop

Hermes must execute the following state machine for every engine-driven task.

### State 1 — BEB Intake/Authorship & YAML State Tracking
Before invoking the engine, the architect/system-engineer role must provide a formal **Blk Execution Brief (BEB)** and architect-authored L2 execution intent, then save the BEB to `docs/execution briefs/BEB_###.md`. BLK-System may validate, normalize, and bind the BEB and L2 into the `SprintPayload`, but BLK-System must not generate its own mission brief or L2 intent when architecture intent is absent.

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

The brief must define the exact task objective, architectural constraints, explicitly prohibited actions, required validation commands, **allowed modified files**, and **allowed new files**. Hermes must never send open-ended requests. If the BEB lacks product intent, architecture intent, target workflow, or acceptance criteria, the correct result is BEB clarification required before any L2 packet or engine invocation.

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
* **Hard Boundaries:** `blk-pipe` bounds the engine to an explicit execution-cap profile. If the payload omits caps, the defaults are a 15-minute execution window and 50MB combined `stdout`/`stderr` output cap. If the payload includes `timeout_seconds` or `max_output_bytes`, those caller-selected finite values become the mechanical caps for that run and must be preserved in the execution evidence.
* **Caller-Tunable Cap Boundary:** Raising or lowering timeout/output caps is an operational sizing choice, not an authority promotion. It does not authorize broader file allowlists, protected BLK-req body reads, live BLK-test MCP, authoritative BEO publication, RTM generation, RTM drift rejection, or source mutation outside the exact BLK-pipe allowlists.
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
    * If `INVALID_PAYLOAD` (Exit 8): Skip Phase 4.2 and proceed to Loop Control / operator correction.
    * If `FATAL_OUTPUT_FLOOD` (Exit 5): Skip Phase 4.2 and proceed to Loop Control.
    * If `FATAL_SYSTEM_PANIC` or `FATAL_PYTHON_TIMEOUT` (Exit 1): Halt immediately and escalate to human.

### Phase 4.2 — The Physics Oracle (blk-test Evaluation; Target Architecture)
In the future approved target architecture, Hermes invokes `blk-test` against the newly committed branch to run deep structural verification.
* Hermes reads the compressed, deduplicated JSON payload.
* *Target Verdict 4.2:* If status is `PASS`, Hermes may generate a successful BEO document. If `FAIL` or `FATAL_OUTPUT_FLOOD`, Hermes extracts the 1-sentence Root Cause Hypothesis and Affected Files, then proceeds to Loop Control.

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
In the future approved target architecture, after execution completes Hermes generates the `BEO_###.md` document alongside the BEB. Current publication authority is not granted by this root overview and is tracked outside BLK-003.

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

**Escalation procedure:**
1.  **Halt the loop.** Do not invoke `blk-pipe` again.
2.  **Create only a draft-only BEO-shaped fixture** with status: `FATAL: ESCALATION` if a BEO-shaped artifact is needed for the human escalation package. This is not authoritative BEO publication.
3.  **Write the human escalation package** to `.kuronode-packets/BEB_XXX_escalation.md`, including raw, un-truncated JSON payloads from `blk-pipe` and any currently available source-bound fixture BLK-test payloads. Do not invent live BLK-test evidence.
4.  **Present the handoff to the human operator**.
