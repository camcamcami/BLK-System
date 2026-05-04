# BLK-006 — BLK-Req Architectural Implementation Brief

**Status:** Active Planning Doctrine
**Purpose:** Provide strict implementation directives for SYS-REQ-001 across multi-artifact types using Discord, Python, and the compiled BLK-pipe transport layer.
**Target Audience:** Implementation Agent (Hermes/Codex)

---

**Context & Rationale:** This architecture establishes a lean, deterministic, multi-artifact engineering baseline. Humans authorize intent via Discord, Python scripts enforce schema compliance and cryptographic hashing, and the LLM handles bounded semantic translation. The tactical executing agent must never possess write access to the engineering baseline.

---

## A. The Immutable Vault & BLK-pipe Hard-Deny

**Implementation Directive:** Modify the compiled Go binary of `blk-pipe` to act as a physical blast shield for all architectural artifacts.
* **Mechanism:** Insert a pre-flight execution check. Before the tactical LLM container is spawned, the binary must scan the `AllowedModifiedFiles` array provided by the `SprintPayload`.
* **Rule:** If any string matches the regex pattern `^docs/(requirements|use_cases)/.*`, `blk-pipe` must instantly abort the sprint, wipe the workspace, and return POSIX Exit 3.

---

## B. Intake, Schema Validation, & The Linter Fork

**Implementation Directive:** Construct a unidirectional staging funnel handled by a bifurcated gatekeeper script (`lint_artifacts.py`).
* **The Universal YAML Schema:** ```yaml
  ---
  id: "TBD"                     # New drafts use "TBD". Revisions use existing ID.
  schema_version: "1.0"         # Drives version-aware linter routing
  parent_hash: "sha256:..."     # ONLY required during Staged Revisions
  version_hash: "sha256:..."
  status: "DRAFT"               # Enum: DRAFT, BASELINED, DEPRECATED, REJECTED
  rationale: "Justification text..."
  linked_nodes:
    - '"[[REQ-012]]"'
  ---
  ```
* **Schema Routing:** The script reads `schema_version` and validates against the corresponding JSON schema (e.g., `schemas/req_v1.0.json`).
* **The Linter Fork (Path-Based):** * *Path:* `/requirements/staging/` -> Run Atomicity Regex. Reject banned conjunctions outside bullet lists and subjective words.
  * *Path:* `/use_cases/staging/` -> Disable Atomicity Regex. Run Word Count. Reject if `len(body.split()) > 500`.
* **Baseline ID Assignment:** Upon promotion, the backend script mechanically calculates the next sequential integer for that directory (e.g., `REQ-043`), assigns it, and commits.

---

## C. The Staged Revision & Concurrency Lock

**Implementation Directive:** Establish a copy-on-write workflow for updating active baselined artifacts.
* **Mechanism:** For edits, Hermes copies the active artifact from the vault to `/staging/<id>_draft.md`. Hermes MUST inject the active vault's current hash into the draft's `parent_hash` YAML field.
* **Concurrency Lock Check:** When approved, the backend promotion script reads the `version_hash` of the active file in the vault and compares it strictly to the draft's `parent_hash`.
  * *Match:* Overwrite active file, delete draft.
  * *Mismatch:* Abort overwrite. Alert Discord: "Stale Draft: Active baseline has mutated since checkout."

---

## D. Canonical Hashing, Traceability, & Context Economy

**Implementation Directive:** Build a mathematically stable hashing function that protects both narrative and structural traces.
* **Canonical Serialization Scope:** The script extracts `id`, `schema_version`, `status`, `rationale`, `linked_nodes`, and the full **Markdown body**. It serializes them into a whitespace-stripped JSON string and calculates the SHA-256 hash. *Any* textual or structural alteration generates a new hash and invalidates downstream traces.
* **Context Economy via Lazy Loading (Spec 1.1):** To prevent token bloat, the tactical engine MUST NOT ingest monolithic baseline documents. The `fetch_requirements_context` tool is restricted to retrieving only the specific, individual artifacts explicitly listed by ID. Artifacts are injected fully intact; truncation of constraints is strictly prohibited.
* **The BLK-native Binding Mechanic:** Hermes injects the target artifact's `version_hash` into the BEB's `traced_artifacts` array. The BEO inherits this hash. `generate_rtm.py` compares the BEO's hash against the live artifact file to mathematically verify the trace.

---

## E. Graph-Linking & External Visualization Boundary

**Implementation Directive:** Ensure flat-file data natively supports external graphical RTM dashboards (e.g., Obsidian).
* **Graph-Link Syntax:** All internal relational traces MUST use double brackets wrapped in quotes (`"[[Target_ID]]"`). The linter rejects non-conforming links.
* **Artifact Tolerance:** The tactical agent and linter MUST ignore external tool artifacts (e.g., `.obsidian/`, `.stfolder/`).
* **The Immutability Rule:** External tools operate strictly as "glass-box" viewers. They MUST NOT be used to directly mutate baselined files in the `/active/` vault.

---

## F. Discord as the Authorization Authority

**Implementation Directive:** Utilize Discord's native API payloads as the cryptographic-adjacent signing authority.
* **Mechanism:** When a draft passes the staging linter, Hermes presents an `[Approve Baseline]` Discord button.
* **Signature Capture:** When clicked, the backend script captures the Discord `User.ID`, `Message.ID`, and `Interaction.Timestamp`.
* **Record Injection:** The script calculates the final Canonical Hash (Section D), then appends the signature to the metadata (e.g., `baseline_authorization: { idp: "discord", ... }`), sets `status` to `"BASELINED"`, and moves it to the active vault.
