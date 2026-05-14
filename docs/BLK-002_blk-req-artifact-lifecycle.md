# BLK-002 — BLK-Req Artifact Lifecycle & Intake Protocol

**Status:** Active Operating Doctrine
**Purpose:** To define the strict state machine for the intake, linting, baselining, and revision of architectural artifacts (Requirements and Use Cases). This protocol acts as the "Legislative Gateway" that produces the immutable, cryptographically hashed baselines consumed by the BLK-native BEB/L2 tactical execution loop.

---

## 0. Fixed Overview Boundary

```text
BLK_001_TO_006_FIXED_OVERVIEW_NOT_SPRINT_STATE
```

This document is a stable overview/contract surface. Do not patch it with sprint-current-state, completion markers, roadmap handoffs, or per-sprint authority updates. Current implementation state belongs in `docs/BLK-077_blk-system-post-078-roadmap.md`, `docs/BLK-079_post-078-current-state-authority-index.md`, component-specific post-root BLK docs, code/tests, and the single sprint closeout outcome.

---

## 1. Phase 1: The Staging Intake (Drafting)

Artifact generation begins exclusively via the Discord Human-in-the-Loop (HITL) gateway. The tactical execution engine (Codex) is entirely dormant during this phase.

### 1.1 Intent Capture & Markdown Generation

* The human operator dictates intent to Hermes via Discord.
* Hermes generates a candidate Markdown file and saves it **strictly** to the isolated staging directories (`/docs/requirements/staging/` or `/docs/use_cases/staging/`).
* Hermes MUST NOT attempt to write to the `/active/` vault.

### 1.2 The Draft YAML Schema

Hermes must generate the candidate file with the following rigid frontmatter:

```yaml
---
id: "TBD"
schema_version: "1.0"
parent_hash: ""
version_hash: "PENDING"
status: "DRAFT"
rationale: "Explicit justification for this constraint or use case."
linked_nodes:
  - '"[[OPTIONAL_TARGET_ID]]"'
---
# Free-text body (governed by linting rules)
```

## 2. Phase 2: Mechanical Linting & The Gatekeeper

Before an artifact can be presented for human approval, Hermes MUST mechanically evaluate it using the `lint_artifacts.py` backend script.

### 2.1 The Linter Fork

Hermes executes the linter against the targeted staging file. The script autonomously routes the validation logic based on the file path:

* **Requirement Path (`/requirements/staging/*.md`):** The script executes the Atomicity Regex. It mechanically rejects the draft if it detects banned conjunctions ("and", "or", "while") outside of bulleted lists, or subjective vocabulary ("fast", "user-friendly").
* **Use Case Path (`/use_cases/staging/*.md`):** The script bypasses atomicity checks and executes the Narrative Bound check. It mechanically rejects the draft if the Markdown body exceeds 500 words.

### 2.2 Diagnostic Parsing & Auto-Fix

If the linter throws a rejection, it outputs a strict JSON diagnostic payload.

1. Hermes parses the JSON.
2. Hermes enters the **Auto-Fix Loop**, silently self-remediating the syntax to satisfy the linter.
3. **Hard Cap:** Hermes is restricted to a maximum of 3 Auto-Fix attempts. If the script still rejects the file after the 3rd attempt, Hermes must halt and post the JSON error payload to the human via Discord for manual intervention.

## 3. Phase 3: Baseline Promotion (The HITL Gateway)

Once `lint_artifacts.py` returns Exit 0 (clean), the artifact is ready for the legal baselining procedure.

### 3.1 The Approval Gate

Hermes posts a Discord embed containing a clean summary of the artifact and an interactive [Approve Baseline] button. The system halts until the human clicks this button.

### 3.2 Cryptographic Execution (Backend Script)

Upon human interaction, Hermes triggers the backend promotion script, which executes the following mechanical sequence:

1. **Signature Capture:** Captures the Discord User.ID, Message.ID, and Interaction.Timestamp from the webhook payload.
2. **ID Generation:** Calculates the next available sequential integer for the target directory and overwrites `id: "TBD"` with the permanent identifier (e.g., `id: "REQ-043"`).
3. **Metadata Injection:** Injects the signature into the YAML (`baseline_authorization: {...}`) and updates status to `"BASELINED"`.
4. **Canonical Hashing:** Serializes the `id`, `schema_version`, `status`, `rationale`, `linked_nodes`, and the exact **Markdown body**. It calculates the SHA-256 hash of this serialized string and writes it to `version_hash`.
5. **Atomic Vault Transfer:** Executes a POSIX atomic move (`os.rename()`), transferring the file from `/staging/` to `/docs/active/`.

*Handoff: The artifact is now permanently baselined and legally available for retrieval by the BLK-native BEB/L2 orchestration loop (State 1.1).*

## 4. Phase 4: The Staged Revision Protocol

Baselines are physically immutable. To alter an existing artifact without corrupting the traceability matrix, Hermes must execute the Copy-on-Write revision loop.

### 4.1 The Checkout

* Hermes receives a revision request via Discord.
* Hermes copies the target file from `/docs/active/` to `/staging/<id>_draft.md`.
* **Critical Injection:** Hermes MUST copy the active file's current `version_hash` and paste it into the draft's `parent_hash` field.

### 4.2 The Edit & Diff

* Hermes applies the requested text modifications.
* Hermes executes the linting procedure (Phase 2).
* Hermes posts a Git-style diff to Discord alongside the [Approve Revision] button.

### 4.3 The Concurrency Lock & Overwrite

When the human approves the revision, the promotion script executes:

1. **Lock Check:** The script reads the `version_hash` of the live file currently sitting in the `/active/` vault. It strictly compares this against the `parent_hash` inside the draft.
2. **Mismatch (Abort):** If the hashes differ, a concurrent edit has occurred. The script aborts the overwrite and throws a "Stale Draft" error.
3. **Match (Execute):** If the hashes match, the script recalculates the new Canonical Hash (as per 3.2.4), overwrites the live file in the `/active/` vault using an atomic rename, and purges the staging draft. Downstream Blk Execution Outcomes (BEOs) tracing to the old hash are instantly invalidated by the mathematical drift.
