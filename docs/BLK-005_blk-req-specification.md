# BLK-005 — BLK-Req Specification

**Status:** Active Operating Doctrine
**Purpose:** Define the structural and behavioral constraints for managing engineering requirements and use cases in an AI-orchestrated CI/CD pipeline.

---

## 1. Data Structure & Storage

* **1.1 Context Economy:** The system MUST structure artifact data to allow the tactical agent to acquire necessary task context without exceeding strict token-burn thresholds.
* **1.2 Strict Atomicity (Requirements):** For artifacts classified as Requirements, the system MUST mechanically enforce singular, non-compound constraint statements.
* **1.3 Narrative Bounding (Use Cases):** For artifacts classified as Use Cases, the system MUST suspend strict atomicity enforcement and instead enforce a maximum narrative threshold of 500 words.
* **1.4 Mandatory Rationale:** Every artifact MUST contain a `rationale` field in its metadata.
* **1.5 Schema Versioning:** The YAML metadata schema MUST be version-controlled.
* **1.6 Schema Enforcement:** The system MUST reject artifact files that do not conform to the active metadata schema using version-aware routing.
* **1.7 Diagnostic Feedback:** The system MUST return structured, deterministic diagnostic payloads identifying specific rule violations when rejecting a drafted artifact.
* **1.8 Historical Preservation:** The system MUST preserve a permanent, auditable record of deprecated and rejected artifacts via the Git ledger.
* **1.9 Quarantine Isolation:** The system MUST mechanically isolate deprecated and rejected artifacts from active agent retrieval operations.
* **1.10 Staging Isolation:** The system MUST maintain a dedicated staging environment for drafted artifact candidates, physically isolated from the baselined vault until explicit human promotion.
* **1.11 Tool-Agnostic Interoperability:** The system MUST store artifact data in a universally readable flat-file format.
* **1.12 State Enumeration:** The system MUST restrict artifact status values to a predefined, mechanically validated enumeration.
* **1.13 Identifier Immutability:** The system MUST assign a globally unique, immutable identifier to each artifact upon initial baselining.
* **1.14 Identifier Syntax:** The system MUST enforce a strict, category-agnostic numeric sequence syntax for all artifact identifiers prefixed by their type (e.g., `REQ-###` or `UC-###`).

## 2. Execution Boundaries

* **2.1 Execution Immutability:** The system MUST write-protect baselined artifact data from the tactical execution agent at the transport layer via BLK-pipe's hard-deny rules during implementation sprints.
* **2.2 Canonical Version-Locking:** The system MUST assign a deterministic version hash (calculated via a strict canonical serialization function) to every artifact revision upon baselining.
* **2.3 Artifact Binding:** Codex Execution Briefs (CEBs) and Codex Execution Outcomes (CEOs) MUST bind to the deterministic canonical version hash of their target artifacts.
* **2.4 Drift Rejection:** The system MUST reject execution artifacts (CEOs) if their traced version hash does not match the active baselined artifact hash.

## 3. Traceability

* **3.1 V&V Traceability:** The system MUST support a machine-readable traceability link between an artifact and any associated Verification or Validation (V&V) execution artifacts.
* **3.2 Graph-Link Syntax:** The system MUST format all internal relational links within metadata fields using a standardized, parser-safe bracket syntax (e.g., `"[[Target_ID]]"`).

## 4. Human-Machine Interface & Baseline Authorization

* **4.1 Centralized HITL Gateway:** The system MUST expose artifact drafting, editing, and baseline-promotion workflows exclusively through an authenticated chat-based Human-in-the-Loop (HITL) gateway (Discord).
* **4.2 Gateway Write-Protection:** The HITL gateway MUST NOT possess direct write access to the active vault; it MUST execute writes and file promotions exclusively through deterministic backend scripts.
* **4.3 Tamper-Evident IdP Upgrades:** The system MUST utilize the HITL gateway's native Identity Provider (IdP) mechanisms (User ID, Message ID, Timestamp) to generate tamper-evident audit records authorizing the promotion of drafted artifacts into the active baselined vault.
* **4.4 Staged Revisions:** The system MUST execute revisions to baselined artifacts via a staged draft, mechanical linting, and explicit HITL promotion workflow, preventing direct mutation of the active baseline.
* **4.5 Concurrency Locking:** The system MUST abort the promotion of a staged revision if the deterministic version hash of the active baselined artifact has mutated since the draft was initiated.
