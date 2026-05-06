# BLK-SYSTEM-014 — Task 4 Outcome

**Status:** Complete
**Date:** 2026-05-07T07:00:17+10:00
**Task:** Commit-before-approval checkpoint and first live smoke
**Commit:** `dc29fd5 feat: prepare approved blk-test fixed-tool live smoke`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Commit and push the live-smoke wrapper/tests, verify a clean worktree, obtain explicit human approval for the exact envelope, then run exactly one approved fixed-tool BLK-test MCP live smoke against a marker-owned synthetic isolated workspace.

## 2. Files Added/Changed

- Modified `python/blk_test_mcp_fixed_tool_live_smoke.py`.
- Modified `python/test_blk_test_mcp_fixed_tool_live_smoke.py`.
- Added this outcome document.

## 3. Behavior Implemented

Task 4 added the top-level `run_sprint014_first_live_smoke(...)` wrapper and `sprint014_live_smoke_envelope_hash(...)`.

The wrapper enforces:

- `approval_kind == "blk-test-mcp-live-smoke"`;
- exact run ID;
- exact implementation commit hash;
- exact driver hash;
- exact requested tool `run_ast_validation`;
- exact workspace identity and timeout/output profile;
- exact envelope hash;
- duplicate approval ID and duplicate run ID rejection before process start;
- explicit Sprint 014 human checkpoint before execution.

## 4. TDD Evidence

### 4.1 RED

Focused wrapper tests failed before wrapper helpers existed:

```text
ImportError: cannot import name 'run_sprint014_first_live_smoke'
```

### 4.2 GREEN

Focused Sprint 014 suite after wrapper implementation:

```text
Ran 21 tests in 1.154s

OK
```

Pre-approval clean/pushed checkpoint:

```text
## main...origin/main
dc29fd5 feat: prepare approved blk-test fixed-tool live smoke
```

## 5. Human Approval Envelope

The operator explicitly approved:

```text
APPROVE exact BLK-SYSTEM-014-SMOKE-001 envelope
```

Approved envelope:

```text
Sprint: BLK-SYSTEM-014
Run ID: BLK-SYSTEM-014-SMOKE-001
Approval ID: BLKTEST-S14-SMOKE-APPROVAL-001
Implementation commit hash: dc29fd5
Driver path: /tmp/blk-system-014-live-smoke-driver.py
Driver hash: sha256:4ff89f4ba9f1d3772ea7adbe6293bc0a4156436fa0ee47013de7226d15de2397
Tool: run_ast_validation
Transport: stdio only
Workspace: marker-owned synthetic isolated temporary workspace only, under approved run-scoped scratch root, with no .git and no repo ancestor/descendant
Source report identity: reports/BLK-SYSTEM-014/synthetic-source-report.json / source-report-BLK-SYSTEM-014-smoke
Trace artifact: REQ-S14-SMOKE-001 / sha256:1111111111111111111111111111111111111111111111111111111111111111
Timeout/output: 5s / 4096 bytes
Approval kind: blk-test-mcp-live-smoke
Replay policy: reject duplicate approval ID and duplicate run ID before process start
Non-authority: no arbitrary shell, no non-stdio transport, no real target repo, no source mutation, no authoritative BEO, no RTM, no protected BLK-req vault reads
```

## 6. Smoke Evidence

The first approved live smoke ran exactly once from committed/pushed implementation code and returned `PASS`.

Key evidence:

```text
status: PASS
run_id: BLK-SYSTEM-014-SMOKE-001
approval_id: BLKTEST-S14-SMOKE-APPROVAL-001
approval_timestamp: 2026-05-06T20:59:55Z
expires_at: 2026-05-06T21:14:55Z
implementation_commit_hash: dc29fd5
driver_hash: sha256:4ff89f4ba9f1d3772ea7adbe6293bc0a4156436fa0ee47013de7226d15de2397
envelope_hash: sha256:97e0071915ffdbfa7246260cc91deeaaa04032a3d27650add327a924f42aed41
approval_record_hash: sha256:59a06be4ab95d21a27e491b8115cec69a2ea66cbaa78acdff3c01a11de4b243d
authorization_request_hash: sha256:dbdd958c8ab0d7466d3131a5e88088a4f9217b3479affdfb4f1e51fab10fe8f3
source_evidence_hash: sha256:21b395b7863f540ac70c70222aa6414f5bdc71d82d21939f164236d36faaeef9
transcript_hash: sha256:4c72f491a11cac31171f7d77adb5461b0c09faa127f9e58d2863ab1ae6301eac
cleanup_status: CLEANED
output_bytes_observed: 235
output_bytes_returned: 235
```

Bounded transcript excerpt:

```text
{"id": 1, "jsonrpc": "2.0", "result": {"sprint": "BLK-SYSTEM-014"}}
{"id": 2, "jsonrpc": "2.0", "result": {"tools": ["run_ast_validation"]}}
{"id": 3, "jsonrpc": "2.0", "result": {"message": "AST validation passed", "status": "PASS"}}
```

## 7. Non-Authority Confirmation

The evidence confirms:

- no real target repo was used;
- no source mutation occurred;
- no source staging/commit/push occurred as BLK-test behavior;
- no arbitrary shell was used;
- no non-stdio transport was used;
- no authoritative BEO publication occurred (`beo_publication: DRAFT_ONLY`);
- no RTM was generated (`rtm_status: NOT_GENERATED`);
- no protected BLK-req vault body was read (`active_vault_read: false`);
- bounded output remained below the approved 4096-byte limit;
- cleanup completed with `cleanup_status: CLEANED`.

## 8. Final Verification

Smoke validation gate:

```text
BLK-SYSTEM-014 first live smoke evidence: PASS
```

## 9. Deviations / Notes

No deviations. Because Task 4 returned `PASS` with cleanup verified, Task 5 may proceed to create BLK-020 first-smoke doctrine and cross-reference gates.

## 10. Next Task

Task 5 — active BLK-020 doctrine and cross-reference gates.
