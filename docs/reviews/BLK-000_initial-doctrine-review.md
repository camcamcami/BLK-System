# BLK-000 — Initial Doctrine Review

**Status:** Review notes for initial repository seed; updated after BLK-002 completion
**Date:** 2026-05-02
**Reviewer:** Hermes
**Scope:** BLK-001, BLK-002, BLK-003 as provided by Camcamcam; BLK-002 full lifecycle update supplied via Discord

---

## 1. Overall Assessment

The seed doctrine defines a coherent separation-of-concerns model for a standalone `blk-system` project: `blk-req` creates immutable legislative baselines, Hermes translates bounded architecture into execution payloads, `blk-pipe` mechanically isolates tactical implementation, `blk-test` verifies physical reality, and a traceability aggregator closes the requirements loop.

The architecture is directionally strong because it treats LLMs as bounded reasoning workers rather than trusted state holders. The cryptographic `version_hash` baton is the correct central invariant.

The full BLK-002 update materially strengthens the doctrine. It now defines the lifecycle mechanics that were missing from the initial seed: staged drafting, mechanical linting, bounded auto-fix, HITL approval, signature capture, canonical hashing, atomic promotion, copy-on-write revision, stale-draft detection, and downstream invalidation by hash drift.

---

## 2. Mechanical Fixes Applied Before Initial Commit

These edits were applied because they were formatting/numbering corrections rather than doctrine changes:

1. **BLK-001 subsystem headings:** corrected `3.3`, `4.4`, and `5.5` to `2.3`, `2.4`, and `2.5` under the "Core Subsystems" section.
2. **BLK-002 Markdown validity:** closed the unclosed YAML code fence in the draft schema block.
3. **BLK-003 state numbering:** changed `State 1.5` to `State 1.4` because no `State 1.4` existed.
4. **BLK-003 escalation section:** changed the final section heading from `## 6` to `## 10` to match the internal `§10` references.

---

## 3. Post-Seed Doctrine Update

### 3.1 BLK-002 lifecycle gap resolved

The initial seed version of BLK-002 stopped after the draft YAML schema. The full BLK-002 update now resolves the major lifecycle gap by specifying:

- Discord-only staging intake,
- strict staging-only write boundaries,
- draft YAML schema,
- `lint_artifacts.py` gatekeeping,
- requirement/use-case validation fork,
- strict JSON diagnostic parsing,
- 3-attempt auto-fix cap,
- HITL approval gate,
- Discord signature capture,
- sequential ID generation,
- baseline metadata injection,
- canonical SHA-256 hash generation,
- POSIX atomic vault transfer,
- copy-on-write revision checkout,
- `parent_hash` concurrency locking,
- stale-draft abort semantics,
- downstream invalidation when `version_hash` changes.

**Disposition:** The blocker "BLK-002 is currently incomplete" is closed for the lifecycle/intake protocol layer.

### 3.2 Remaining active-vault path decision

BLK-002 now explicitly names staging directories:

- `/docs/requirements/staging/`
- `/docs/use_cases/staging/`

It also refers to promotion into `/docs/active/` and revision checkout from `/docs/active/`. That may be intentional as a shared active vault, but the doctrine should eventually decide whether active artifacts live in:

- one shared vault: `/docs/active/`, or
- type-specific vaults: `/docs/requirements/active/` and `/docs/use_cases/active/`.

**Recommendation:** keep implementation flexible until this path convention is explicitly frozen.

### 3.3 AAA_001 / CEB / CEO / BEB / BEO naming bridge remains open

BLK-002 currently says baselined artifacts become available for retrieval by `AAA_001 (State 1.1)`, while BLK-003 establishes BLK-native BEB/BEO terminology. This may be intentional as a Kuronode-to-BLK migration bridge, but it should be made explicit.

**Recommendation:** define whether BLK-System supersedes AAA_001 `CEB/CEO` terms with `BEB/BEO`, or whether it wraps/extends AAA_001 for Kuronode compatibility.

### 3.4 Tool schemas remain named before full specification

The documents refer to tools such as:

- `fetch_requirements_context`,
- `analyze_dependency_graph`,
- `ExecuteSprintTool`,
- `abort_sprint_and_revert`.

Those names are useful, but their JSON input/output contracts should become first-class doctrine documents or appendices before implementation hardening.

### 3.5 BLK-pipe engine args may be engine-specific

BLK-003 mandates `--json`, `--isolated`, `--yes`, and deny-read flags. These should be validated against the selected tactical engine's actual CLI. If the engine is Codex CLI, the final flag set must match the installed Codex CLI version.

---

## 4. Commit Disposition

The doctrine is suitable to keep as the active repository seed with BLK-002 now promoted from partial sketch to active lifecycle protocol. Implementation may proceed for `blk-req` only after the active-vault path convention and BLK-vs-AAA naming bridge are explicitly frozen or treated as configurable boundaries.
