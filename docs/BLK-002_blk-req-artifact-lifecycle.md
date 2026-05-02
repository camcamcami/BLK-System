# BLK-002 — BLK-Req Artifact Lifecycle & Intake Protocol

**Status:** Active Operating Doctrine  
**Purpose:** To define the strict state machine for the intake, linting, baselining, and revision of architectural artifacts (Requirements and Use Cases). This protocol acts as the "Legislative Gateway" that produces the immutable, cryptographically hashed baselines consumed by the `AAA_001` tactical execution loop.

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
