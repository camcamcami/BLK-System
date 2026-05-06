# BLK-020 — BLK-test MCP First Live Fixed-Tool Smoke

**Status:** Active first-smoke evidence contract
**Scope:** BLK-SYSTEM-014 accepted first live fixed-tool BLK-test MCP smoke evidence under explicit human approval, with no production BLK-test MCP authority.

---

## 1. Purpose

BLK-020 records the accepted first-smoke evidence contract created by BLK-SYSTEM-014 after exactly one approved First live fixed-tool BLK-test MCP smoke under explicit human approval returned `PASS` with cleanup verified.

This document makes the first-smoke evidence discoverable without broadening BLK-test MCP authority. It records what happened and what remains non-authorized.

---

## 2. Current first-smoke authority boundary

BLK-020 records a first-smoke evidence contract only. It does not authorize production BLK-test MCP, does not use arbitrary shell, does not use non-stdio transport, does not run against real target repositories, does not mutate primary repo, does not authorize authoritative BEO publication, does not authorize RTM generation, does not read protected BLK-req vault bodies, and does not claim production sandbox or host-secret isolation.

The accepted BLK-SYSTEM-014 smoke used a synthetic isolated workspace and the one fixed tool `run_ast_validation`. It produced PASS/FAIL/BLOCKED evidence vocabulary, but only the approved first run recorded `PASS`.

---

## 3. Prerequisite contracts

BLK-017 remains the active disabled transport contract for generic startup paths and disabled-by-default behavior.

BLK-018 remains the workspace/process-control probe contract and supplies synthetic workspace, process-control, bounded timeout/output, cache, and cleanup constraints.

BLK-019 remains the approval/source-evidence authorization contract and must return `APPROVAL_VALIDATED_SOURCE_BOUND` before any future first-smoke-like live checkpoint can be considered.

BLK-SYSTEM-014 did not weaken these contracts. It added a narrow one-run approval extension and wrapper path in `python/blk_test_mcp_fixed_tool_live_smoke.py` and tests in `python/test_blk_test_mcp_fixed_tool_live_smoke.py`.

---

## 4. Approved first-smoke envelope

The accepted envelope was:

```text
Sprint: BLK-SYSTEM-014
Run ID: BLK-SYSTEM-014-SMOKE-001
Approval ID: BLKTEST-S14-SMOKE-APPROVAL-001
Implementation commit hash: dc29fd5
Driver hash: sha256:4ff89f4ba9f1d3772ea7adbe6293bc0a4156436fa0ee47013de7226d15de2397
Envelope hash: sha256:97e0071915ffdbfa7246260cc91deeaaa04032a3d27650add327a924f42aed41
Tool: run_ast_validation
Transport: stdio-only
Workspace: synthetic isolated workspace
Timeout/output: 5s / 4096 bytes
```

The envelope was one exact source/request/workspace/profile/tool envelope and not an ambient approval token.

---

## 5. Fixed-tool registry and stdio-only rule

The first-smoke registry contains exactly one fixed tool: `run_ast_validation`.

The transport is stdio-only and implemented as a dependency-free JSON-RPC/MCP-subset smoke. The subset supports `initialize`, `tools/list`, and `tools/call` for `run_ast_validation` only.

Caller-supplied commands, wildcard tools, multiple tools, arbitrary shell, HTTP, WebSocket, TCP, UDP, daemon/listener startup, package manager execution, model calls, cyber tooling, and dynamic command construction remain outside authority.

---

## 6. Synthetic workspace and protected-vault exclusions

The smoke may use only a marker-owned synthetic isolated workspace. It must not run against `/home/dad/BLK-System`, any real target repository, any `.git` root/ancestor/descendant, root/home paths, protected BLK-req vault prefixes, traversal, or symlink escapes.

Protected BLK-req vault bodies remain unread. `active_vault_read` remains false in accepted smoke evidence.

---

## 7. PASS/FAIL/BLOCKED and replay evidence shape

First-smoke evidence is replayable through approval/request/source/transcript hashes:

```text
approval_record_hash: sha256:59a06be4ab95d21a27e491b8115cec69a2ea66cbaa78acdff3c01a11de4b243d
authorization_request_hash: sha256:dbdd958c8ab0d7466d3131a5e88088a4f9217b3479affdfb4f1e51fab10fe8f3
source_evidence_hash: sha256:21b395b7863f540ac70c70222aa6414f5bdc71d82d21939f164236d36faaeef9
transcript_hash: sha256:4c72f491a11cac31171f7d77adb5461b0c09faa127f9e58d2863ab1ae6301eac
```

Evidence may use PASS/FAIL/BLOCKED evidence statuses plus fatal/transport statuses for bounded process outcomes. BLOCKED evidence must not project to success, authoritative BEO, RTM generation, or active requirement coverage.

---

## 8. Non-authority checklist

BLK-020 preserves these markers:

- does not authorize production BLK-test MCP;
- does not use arbitrary shell;
- does not use non-stdio transport;
- does not run against real target repositories;
- does not mutate primary repo;
- does not stage, commit, push, reset, stash, checkout, or revert source as BLK-test behavior;
- does not authorize authoritative BEO publication;
- does not authorize RTM generation;
- does not read protected BLK-req vault bodies;
- does not claim production sandbox or host-secret isolation.

---

## 9. Stop conditions

Any future replay or extension must fail closed if approval IDs or run IDs are reused, if the envelope hash changes, if the implementation commit or driver hash changes without fresh approval, if the tool set broadens, if transport is not stdio-only, if workspace guards fail, or if BLK-017/018/019 prerequisite semantics are weakened.

---

## 10. Implementation and tests

Implementation and test files:

- `python/blk_test_mcp_fixed_tool_live_smoke.py`
- `python/test_blk_test_mcp_fixed_tool_live_smoke.py`
- `python/test_active_doctrine_review_gates.py`

Outcome evidence:

- `docs/outcomes/BLK-SYSTEM-014_task-004-outcome.md`

---

## 11. Handoff to future sprint

BLK-SYSTEM-015 may review draft BEO publication gates only if it preserves `beo_publication: "DRAFT_ONLY"` unless a later explicit publication sprint grants authority. RTM generation remains disabled and separately owned by a later RTM sprint.
