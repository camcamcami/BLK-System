# BLK-000 — Initial Doctrine Review

**Status:** Review notes for initial repository seed  
**Date:** 2026-05-02  
**Reviewer:** Hermes  
**Scope:** BLK-001, BLK-002, BLK-003 as provided by Camcamcam

---

## 1. Overall Assessment

The three documents define a coherent separation-of-concerns model for a standalone `blk-system` project: `blk-req` creates immutable legislative baselines, Hermes translates bounded architecture into execution payloads, `blk-pipe` mechanically isolates tactical implementation, `blk-test` verifies physical reality, and a traceability aggregator closes the requirements loop.

The architecture is directionally strong because it treats LLMs as bounded reasoning workers rather than trusted state holders. The cryptographic `version_hash` baton is the correct central invariant.

---

## 2. Mechanical Fixes Applied Before Commit

These edits were applied because they are formatting/numbering corrections rather than doctrine changes:

1. **BLK-001 subsystem headings:** corrected `3.3`, `4.4`, and `5.5` to `2.3`, `2.4`, and `2.5` under the "Core Subsystems" section.
2. **BLK-002 Markdown validity:** closed the unclosed YAML code fence in the draft schema block.
3. **BLK-003 state numbering:** changed `State 1.5` to `State 1.4` because no `State 1.4` existed.
4. **BLK-003 escalation section:** changed the final section heading from `## 6` to `## 10` to match the internal `§10` references.

---

## 3. Issues to Resolve in the Next Doctrine Pass

### 3.1 BLK-002 is currently incomplete

BLK-002 stops after the draft YAML schema. It does not yet define the full lifecycle implied by the title and by BLK-001/BLK-003:

- lint phase,
- human approval gate,
- canonical hash generation,
- promotion from staging to active vault,
- revision protocol,
- supersession / parent hash handling,
- rejection handling,
- exact active-vault path conventions,
- `fetch_requirements_context` response schema.

**Recommendation:** expand BLK-002 before implementing `blk-req` tooling.

### 3.2 Active vault paths need canonicalization

BLK-001 says active artifacts are stored in `/docs/active/`, while BLK-002 uses separate staging paths:

- `/docs/requirements/staging/`
- `/docs/use_cases/staging/`

The active paths should be made equally explicit, for example:

- `/docs/requirements/active/`
- `/docs/use_cases/active/`

or BLK-002 should formally define why `/docs/active/` is shared.

### 3.3 CEB/CEO vs BEB/BEO naming bridge needs explicit migration language

BLK-001 still references CEB/CEO in places, while BLK-003 establishes BEB/BEO. This may be intentional as a Kuronode-to-BLK migration bridge, but it should be made explicit.

**Recommendation:** define whether BLK-System supersedes AAA_001 `CEB/CEO` terms with `BEB/BEO`, or whether it wraps them for Kuronode compatibility.

### 3.4 Tool schemas are named before they are specified

The documents refer to tools such as:

- `fetch_requirements_context`
- `analyze_dependency_graph`
- `ExecuteSprintTool`
- `abort_sprint_and_revert`

Those names are useful, but their JSON input/output contracts should become first-class doctrine documents or appendices.

### 3.5 BLK-pipe engine args may be engine-specific

BLK-003 mandates `--json`, `--isolated`, `--yes`, and deny-read flags. These should be validated against the selected tactical engine's actual CLI. If the engine is Codex CLI, the final flag set must match the installed Codex CLI version.

---

## 4. Commit Disposition

The doctrine is suitable to commit as an initial repository seed, with the above issues tracked as review notes. No implementation should begin until BLK-002 is completed and the BEB/BEO vs CEB/CEO naming boundary is resolved.
