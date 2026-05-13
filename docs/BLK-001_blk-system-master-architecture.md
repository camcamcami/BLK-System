# BLK-001 — The `blk-system` Master Architecture

**Status:** Active Operating Doctrine  
**Purpose:** To define the holistic, end-to-end autonomous CI/CD orchestration suite for the Kuronode project. `blk-system` adapts the classic Systems Engineering V-Model for autonomous AI agents, ensuring absolute physical isolation between architectural intent, tactical execution, and physical verification.

---

## 1. The Autonomous V-Model Philosophy

Traditional AI-assisted software engineering relies on monolithic context windows and agentic chatrooms, inevitably leading to prompt drift, hallucinated scope creep, and untraceable code.

`blk-system` rejects this. It enforces a strict separation of concerns through isolated microservices. The LLM (Hermes) acts as the Architect and Router, the LLM (Codex) acts as the Tactical Worker, and deterministic compiled binaries and Python scripts enforce the physical laws of the repository. The only trust-bearing trace baton crossing these isolated domains is the cryptographic `version_hash`; `blk-id` records identity/provenance and `blk-relay` carries typed messages, but neither creates truth, approval, mutation, verification, or trace authority.

---

## 2. Core Subsystems & Component Contracts

The `blk-system` is composed of strictly bounded operational domains and named component contracts:

### 2.1. `blk-req` (The Legislative Gateway)
**The left side of the V-Model. Defines the absolute laws of the system.**
* **Function:** Intake, linting, canonical hashing, and baselining of Requirements (`REQ-###`) and Use Cases (`UC-###`).
* **Enforcement:** Deterministic Python scripts (`lint_artifacts.py`) enforce atomicity, word counts, and schema conformance.
* **Write-Authority:** Human-in-the-Loop (HITL) via Discord native Identity Provider authorization. The tactical agent is physically locked out.
* **Output:** Immutably hashed Markdown files stored in the `/docs/active/` vault.

### 2.2. `blk-id` (The Identity Spine)
**Every actor and artifact has a stable name.**
* **Function:** Deterministic identity and provenance binding for humans, agents, requirements, use cases, briefs, outcomes, commits, approval events, and source systems.
* **Enforcement:** Canonical IDs, source-bound metadata, approved identity-provider references, and cryptographic hashes where applicable.
* **Mechanics:** Binds every meaningful action to an actor ID, artifact ID, source system, timestamp, and canonical hash without granting mutation or approval authority by itself.
* **Output:** Stable identity records that prove who approved what, which artifact was used, and which execution outcome inherited which requirement.

### 2.3. `blk-relay` (The Signal Bus)
**Controlled communication without authority.**
* **Function:** Routes authenticated messages, execution requests, status payloads, and HITL approvals between humans, Hermes, tactical agents, and BLK-System services.
* **Enforcement:** Typed payload schemas, deterministic routing rules, source binding, and metadata preservation.
* **Mechanics:** Accepts only structured payloads from approved sources, forwards them to the correct component, and records enough identity/provenance metadata for later traceability.
* **Output:** Validated communication events consumable by `blk-req`, Architecture & Feature Planning, `blk-pipe`, `blk-test`, and `blk-link`; `blk-relay` does not authorize the payload it carries.

### 2.4. Architecture & Feature Planning (The Translation Layer)
**The brain of the operation. Translates laws into tactical bounds.**
* **Function:** Scope reconnaissance, dependency mapping, and Blk Execution Brief (BEB) generation.
* **Enforcement:** Hermes (Tier 1 Agent).
* **Mechanics:** Hermes retrieves specific artifacts from `blk-req` using `fetch_requirements_context`, maps dependencies via `analyze_dependency_graph`, and binds the artifact hashes to the BEB frontmatter.
* **Output:** A strict, machine-readable BEB and the `l2_packet` payload.

### 2.5. `blk-pipe` (The Blast Shield & Forge)
**The bottom of the V-Model. Where code is physically forged.**
* **Function:** Transport layer, POSIX isolation, and Git allowlist enforcement.
* **Enforcement:** Compiled, deterministic Go binary (V47).
* **Mechanics:** Executes the Tier 3 Tactical Agent (Codex) within a 15-minute timebox. It mechanically enforces the `AllowedModifiedFiles` array. If Codex attempts to mutate unapproved files (especially `blk-req` baselines), `blk-pipe` instantly wipes the edits and aborts with POSIX Exit 3.
* **Output:** Sterile, strictly bounded source code commits.

### 2.6. `blk-test` (The Physics Oracle)
**The right side of the V-Model. Verification of reality.**
* **Function:** The MCP Test Execution Server.
* **Enforcement:** Native OS physics and TypeScript test runners.
* **Mechanics:** Clones the sprint branch into an ephemeral directory and runs native verification tests (IPC races, memory bounds, syntax gates). It strips the LLM of the authority to declare success. It returns compressed, deduplicated logs to prevent token-flooding.
* **Output:** A deterministic `PASS`/`FAIL` payload that drives Hermes' Two-Phase Hostile Audit.

**Historical Sprint 019 BEO authority boundary, superseded by post-BLK-SYSTEM-103 reconciliation:** BLK-test returns verification evidence, not authoritative BEO publication authority. Sprint-019-era draft-only/design-only fixture language remains historical/local-fixture lineage. The active post-103 root doctrine state records BLK-SYSTEM-100 `PUBLISHED_EXTERNAL_BEO_RECORD` as record-only external BEO publication evidence while signer/storage/ledger publication remains disabled, RTM generation remains disabled, and future production publication still requires later explicit authority.

### 2.7. `blk-link` (The Ledger)
**Closing the V-Model. Proving the trace.**
* **Function:** Offline Requirements Traceability Matrix (RTM) generation.
* **Enforcement:** Deterministic Python script contract (`generate_rtm.py`, future/offline implementation target) operating under the `blk-link` component name.
* **Mechanics:** In the target architecture, consumes authoritative published BEO metadata plus approved hash-only BLK-req metadata. It must not read, copy, parse, hash, summarize, scan, or mutate protected BLK-req body bytes during trace closure.
* **Output:** Trace-closure evidence and later drift signals only after separate authority. The active post-103 state includes BLK-SYSTEM-103 `PILOT_LOCAL_RTM_TRACE_CLOSURE_RECORDED_NOT_AUTHORITATIVE` as local non-authoritative trace-closure evidence; production/reusable `blk-link` remains disabled and drift rejection remains a separate future authority.


### 2.8. Post-BLK-SYSTEM-103 root doctrine reconciliation

```text
BLK_SYSTEM_105_ROOT_DOCTRINE_POST_103_RECONCILED
POST_103_ROOT_DOCTRINE_RECONCILIATION_BOUNDARY
BEO_PUBLICATION_RECORD_ONLY_SIGNER_STORAGE_LEDGER_DISABLED
RTM_TRACE_CLOSURE_LOCAL_RECORD_ONLY_PRODUCTION_BLK_LINK_DISABLED
NO_PROTECTED_BODY_READS_FOR_TRACE_CLOSURE
```

Post-BLK-SYSTEM-103 root doctrine reconciliation: BLK-SYSTEM-100 produced `PUBLISHED_EXTERNAL_BEO_RECORD` as record-only external BEO publication evidence. It does not grant signer/storage/ledger publication, reusable publication authority, protected-body reads, RTM generation, target/source/Git mutation, or BLK-test/BLK-pipe/Codex runtime authority.

BLK-SYSTEM-103 produced `PILOT_LOCAL_RTM_TRACE_CLOSURE_RECORDED_NOT_AUTHORITATIVE` as local non-authoritative trace-closure evidence. Production/reusable `blk-link` remains disabled; no runtime RTM generation, drift rejection, active-vault hash comparison, coverage truth, protected-body read, public ledger mutation, or authoritative drift decision is granted.

---

## 3. The Cryptographic Thread (The Baton Pass)

The integrity of `blk-system` relies entirely on the unbroken chain of the Canonical Version Hash. At no point does the system rely on an LLM to "remember" why code was written.

1. **Generation:** `blk-req` calculates `sha256:7f8b9...` for `REQ-042` upon human baseline approval.
2. **Injection:** Hermes injects `sha256:7f8b9...` into `BEB_010` during sprint planning.
3. **Execution:** `blk-pipe` isolates the engine; `blk-test` verifies the code.
4. **Inheritance:** `BEO_010` inherits `sha256:7f8b9...` upon a `PASS` from the Physics Oracle.
5. **Verification:** `blk-link` confirms `BEO_010` matches the live vault hash for `REQ-042` after authorized offline RTM implementation exists.

If a single comma changes in `REQ-042`'s Markdown body, the hash mutates, the chain breaks, and the system mechanically demands re-verification.

---

## 4. Operational Boundaries & External Tools

* **Visual RTMs:** The system natively supports external graph-visualization tools (e.g., Obsidian) and synchronization protocols (e.g., Syncthing) by storing all architecture as standard Markdown and YAML.
* **The Immutability Rule:** External tools are strictly read-only glass-box viewers for the active vault. Direct file mutation via any channel other than the Discord HITL gateway and the Staged Revision protocol will corrupt the Canonical Hash and paralyze the pipeline.
