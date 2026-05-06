# BLK-SYSTEM-014 — Task 5 Outcome

**Status:** Complete
**Date:** 2026-05-07T07:04:54+10:00
**Task:** Active BLK-020 doctrine and cross-reference gates
**Commit:** `a586ebf docs: define blk-test first live fixed-tool smoke contract`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Publish Sprint 014 first-smoke behavior as active doctrine without broadening BLK-test MCP into production authority.

## 2. Files Added/Changed

- Added `docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md`.
- Modified `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md`.
- Modified `docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md`.
- Modified `docs/BLK-019_blk-test-mcp-approval-source-evidence-authorization.md`.
- Modified `python/test_active_doctrine_review_gates.py`.
- Added this outcome document.

## 3. Behavior Implemented

BLK-020 now records the accepted BLK-SYSTEM-014 first-smoke evidence contract:

- first live fixed-tool BLK-test MCP smoke under explicit human approval;
- `run_ast_validation` only;
- stdio-only dependency-free JSON-RPC/MCP-subset smoke;
- synthetic isolated workspace only;
- one exact source/request/workspace/profile/tool envelope;
- PASS/FAIL/BLOCKED evidence vocabulary;
- replay hashes and non-authority markers.

BLK-017/018/019 now cross-reference BLK-020 narrowly while preserving their prerequisite boundaries. BLK-020 does not authorize production BLK-test MCP, arbitrary shell, non-stdio transport, real target execution, source mutation, authoritative BEO, RTM generation, or protected BLK-req vault body reads.

## 4. TDD Evidence

### 4.1 RED

The active doctrine suite failed before BLK-020 and cross-references existed:

```text
FAIL: test_blk020_records_sprint014_first_live_smoke_without_production_authority
AssertionError: False is not true : BLK-020 first live smoke doctrine missing

FAIL: test_blk017_018_019_020_cross_reference_first_smoke_without_broad_authority
... docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md missing ['BLK-020']
```

### 4.2 GREEN

Active doctrine suite after BLK-020 and cross-reference patches:

```text
Ran 27 tests in 0.002s

OK
```

## 5. Review Results

Self-review confirmed:

- BLK-020 records first-smoke evidence rather than production MCP authority.
- BLK-017 remains disabled by default for generic startup paths.
- BLK-018 remains prerequisite workspace/process-control doctrine.
- BLK-019 remains prerequisite approval/source-evidence authorization doctrine.
- BLK-020 references implementation/tests and Task 4 PASS evidence.

## 6. Final Verification

```text
git diff --check: PASS
Staged paths:
docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md
docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md
docs/BLK-019_blk-test-mcp-approval-source-evidence-authorization.md
docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md
python/test_active_doctrine_review_gates.py
```

Implementation commit:

```text
a586ebf docs: define blk-test first live fixed-tool smoke contract
```

## 7. Deviations / Notes

No deviations. Task 5 was allowed because Task 4 recorded exactly one approved live smoke with status `PASS` and cleanup verified.

## 8. Next Task

Task 6 — full-suite verification and Sprint 015 handoff closeout.
