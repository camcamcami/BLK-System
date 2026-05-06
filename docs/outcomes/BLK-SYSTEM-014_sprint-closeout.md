# BLK-SYSTEM-014 — Sprint Closeout

**Status:** Complete
**Date:** 2026-05-07T07:06:27+10:00
**Sprint:** BLK-SYSTEM-014 — First Live Fixed-Tool BLK-test MCP Smoke
**Final task-line commit before closeout:** `b20c8dc docs: record blk-system sprint 014 task 5 outcome`
**Remote:** pushed to `origin/main`

---

## 1. Summary

BLK-SYSTEM-014 completed the approved first fixed-tool stdio smoke for BLK-test MCP evidence. The sprint preserved BLK-017 disabled transport, BLK-018 workspace/process-control constraints, and BLK-019 approval/source-evidence authorization, then ran exactly one approved live smoke against a synthetic isolated workspace.

The smoke used `run_ast_validation` over stdio-only dependency-free JSON-RPC/MCP-subset communication and returned `PASS` with cleanup verified.

## 2. Task Commit Table

| Task | Commit | Summary |
| --- | --- | --- |
| Task 0 | `8781088 docs: plan blk-system sprint 014 live smoke` | Committed the Sprint 014 plan before implementation. |
| Task 1 | `9c06795 docs: define blk-system sprint 014 live smoke boundary` | Added boundary review and active doctrine gate. |
| Task 2 | `89a4d47 feat: add blk-test sprint 014 live smoke preflight` | Added non-executing Sprint 014 preflight aggregator. |
| Task 3 | `181c2eb feat: add bounded stdio fixed-tool smoke harness` | Added bounded stdio fixed-tool smoke harness. |
| Task 4 | `dc29fd5 feat: prepare approved blk-test fixed-tool live smoke` | Added wrapper/envelope/replay enforcement before approval. |
| Task 5 | `a586ebf docs: define blk-test first live fixed-tool smoke contract` | Added BLK-020 and cross-reference gates. |

## 3. Outcome Documents

| Outcome | Commit |
| --- | --- |
| `docs/outcomes/BLK-SYSTEM-014_task-000-outcome.md` | `4684b0d docs: record blk-system sprint 014 task 0 outcome` |
| `docs/outcomes/BLK-SYSTEM-014_task-001-outcome.md` | `82952e0 docs: record blk-system sprint 014 task 1 outcome` |
| `docs/outcomes/BLK-SYSTEM-014_task-002-outcome.md` | `e14b39b docs: record blk-system sprint 014 task 2 outcome` |
| `docs/outcomes/BLK-SYSTEM-014_task-003-outcome.md` | `1fa50b4 docs: record blk-system sprint 014 task 3 outcome` |
| `docs/outcomes/BLK-SYSTEM-014_task-004-outcome.md` | `48883bf docs: record blk-system sprint 014 first smoke outcome` |
| `docs/outcomes/BLK-SYSTEM-014_task-005-outcome.md` | `b20c8dc docs: record blk-system sprint 014 task 5 outcome` |

## 4. First-Smoke Evidence Summary

Approved first-smoke envelope:

```text
Sprint: BLK-SYSTEM-014
Run ID: BLK-SYSTEM-014-SMOKE-001
Approval ID: BLKTEST-S14-SMOKE-APPROVAL-001
Implementation commit hash: dc29fd5
Driver hash: sha256:4ff89f4ba9f1d3772ea7adbe6293bc0a4156436fa0ee47013de7226d15de2397
Tool: run_ast_validation
Transport: stdio-only
Workspace: synthetic isolated workspace
Timeout/output: 5s / 4096 bytes
```

Smoke result:

```text
status: PASS
cleanup_status: CLEANED
envelope_hash: sha256:97e0071915ffdbfa7246260cc91deeaaa04032a3d27650add327a924f42aed41
approval_record_hash: sha256:59a06be4ab95d21a27e491b8115cec69a2ea66cbaa78acdff3c01a11de4b243d
authorization_request_hash: sha256:dbdd958c8ab0d7466d3131a5e88088a4f9217b3479affdfb4f1e51fab10fe8f3
source_evidence_hash: sha256:21b395b7863f540ac70c70222aa6414f5bdc71d82d21939f164236d36faaeef9
transcript_hash: sha256:4c72f491a11cac31171f7d77adb5461b0c09faa127f9e58d2863ab1ae6301eac
output_bytes_observed: 235
output_bytes_returned: 235
```

Bounded output excerpt:

```text
{"id": 1, "jsonrpc": "2.0", "result": {"sprint": "BLK-SYSTEM-014"}}
{"id": 2, "jsonrpc": "2.0", "result": {"tools": ["run_ast_validation"]}}
{"id": 3, "jsonrpc": "2.0", "result": {"message": "AST validation passed", "status": "PASS"}}
```

## 5. Non-Authority Boundary

Sprint 014 ran only the approved first fixed-tool stdio smoke against a synthetic isolated workspace.

Sprint 014 does not authorize production BLK-test MCP, does not use arbitrary shell, does not use non-stdio transport, does not run against real target repositories, does not mutate primary repo, does not stage/commit/push as BLK-test behavior, does not authorize authoritative BEO publication, does not authorize RTM generation, does not perform RTM drift rejection, does not read protected BLK-req vault bodies, does not claim production sandbox enforcement, and does not claim host-secret isolation.

BLK-020 records first-smoke evidence only. BLK-017 remains disabled by default for generic startup paths. BLK-018 remains prerequisite workspace/process-control doctrine. BLK-019 remains prerequisite approval/source-evidence authorization doctrine.

## 6. Full Verification Evidence

Final verification commands and results:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s python -p 'test_*.py'
Ran 279 tests in 6.402s
OK
```

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python
281 passed in 6.61s
```

```text
go test ./...
ok github.com/camcamcami/BLK-System/cmd/blk-pipe
ok github.com/camcamcami/BLK-System/internal/contracts
ok github.com/camcamcami/BLK-System/internal/engine
ok github.com/camcamcami/BLK-System/internal/execguard
ok github.com/camcamcami/BLK-System/internal/gitguard
ok github.com/camcamcami/BLK-System/internal/pipe
ok github.com/camcamcami/BLK-System/internal/runtimeguard
ok github.com/camcamcami/BLK-System/internal/testutil
ok github.com/camcamcami/BLK-System/internal/validation
```

```text
go vet ./...
PASS
```

```text
git diff --check
PASS
```

Final pre-closeout status:

```text
## main...origin/main
```

No `python/__pycache__`, `python/.pytest_cache`, or `.pytest_cache` artifacts remained after cleanup.

## 7. Sprint 015 Handoff Seed

```text
BLK-SYSTEM-015 — Draft BEO publication gate review, still not authoritative unless explicitly approved
```

Narrow Sprint 015 prerequisites:

1. BLK-020 first-smoke evidence must remain source-bound and replayable.
2. Draft BEO projection, if reviewed, must preserve `beo_publication: "DRAFT_ONLY"` unless a later explicit publication sprint grants authority.
3. BLOCKED smoke evidence must not project to success.
4. RTM generation remains disabled and separately owned by a later RTM sprint.
5. Active BLK-req vault bodies remain unread unless a later explicit access-policy sprint grants authority.

## 8. Deviations / Notes

No scope deviations. The driver was an approved one-run `/tmp` driver bound by its SHA-256 hash and was not committed as production source. The sprint outcome docs and BLK-020 contain the replay-relevant driver hash, envelope hash, and transcript hash.
