# BLK-PIPE-006 Hostile Review Addendum — BLK-008 Scope Check

**Question:** Does BLK-PIPE-006 touch BLK-008, and should BLK-008 be reviewed against?

## Short answer

Yes, BLK-008 should be reviewed as a **secondary/target-state BLK-test authority anchor**, but BLK-PIPE-006 did **not** directly modify or reference BLK-008.

## Evidence

- Located active BLK-008 document: `docs/BLK-008_blk-test-mcp-execution-server.md`.
- BLK-008 status/purpose:
  - `docs/BLK-008_blk-test-mcp-execution-server.md:3` — `**Status:** Active Planning Doctrine`
  - `docs/BLK-008_blk-test-mcp-execution-server.md:4` — specifies the local stdio MCP test execution server as deterministic physics oracle.
- BLK-008 objective is a future/live MCP server shape:
  - `docs/BLK-008_blk-test-mcp-execution-server.md:8-16` — build local stdio MCP server, never arbitrary shell, prevent parallel execution, isolate workspaces, compress output, avoid repo corruption.
- BLK-PIPE-006 plan has no direct BLK-008 reference:
  - search in `docs/plans/BLK-PIPE-006_blk001-alignment-remediation.md` for `BLK-008|blk-008` returned zero matches.
- BLK-PIPE-006 outcomes have no direct BLK-008 reference:
  - search in `docs/outcomes/BLK-PIPE-006*.md` for `BLK-008|blk-008` returned zero matches.
- BLK-008 *was* in Sprint 005 Task 5 scope:
  - `docs/plans/BLK-PIPE-005_integration-contract-hardening-and-approval-gate-design.md:537`
  - `docs/outcomes/BLK-PIPE-005_task-005-outcome.md:28`

## Hostile interpretation

BLK-PIPE-006 remediated disabled BLK-test MCP stubs and source binding, while BLK-008 is the active planning doctrine for the real/live BLK-test MCP server. That makes BLK-008 a target-state doctrine dependency even though it was not directly touched.

The risk is not “Sprint 006 changed BLK-008 incorrectly”; the risk is “Sprint 006 claims BLK-test MCP/BEO/RTM boundaries are clean while the active BLK-test MCP planning document may still lack the current disabled/fixture-only qualifier and trace-baton/source-binding requirements.”

## Should review against BLK-008?

Yes. Use BLK-008 as a required secondary review target whenever auditing sprints that touch any of:

- BLK-test MCP request/response stubs;
- BLK-test PASS/FAIL/BLOCKED handoff fixtures;
- source-bound MCP adapter smoke;
- BEO draft projection from BLK-test evidence;
- RTM interface/traceability claims;
- live BLK-test readiness or “physics oracle” language.

## What to check in BLK-008

A BLK-PIPE-006/BLK-008 cross-review should verify:

1. BLK-008 is explicitly target-state/planning only until a later sprint authorizes live BLK-test MCP.
2. BLK-008 cross-links BLK-015/BLK-016 disabled/source-bound current behavior.
3. BLK-008 requires non-empty canonical `trace_artifacts[*].version_hash` on any PASS/FAIL payload shape.
4. BLK-008 cannot imply authoritative BEO publication or RTM generation.
5. BLK-008’s MCP server output contract aligns with BLK-013/014/015/016 status vocabulary and source-binding requirements.
6. BLK-008’s test server isolation design does not contradict BLK-001’s separation of authority or BLK-pipe’s role as blast shield/forge.

## Recommended report amendment

Treat BLK-008 omission as a review-scope gap, not as a Sprint 006 failure by itself. Add BLK-008 to the next remediation slice alongside the existing BLK-003/BLK-006 fixes.
