# BLK-SYSTEM-014 Live Fixed-Tool Smoke Boundary Review

**Status:** Boundary review for First live fixed-tool BLK-test MCP smoke under explicit human approval
**Sprint:** BLK-SYSTEM-014

---

## 1. Source docs reviewed

This review preserves the boundaries defined by:

- `docs/BLK-001_blk-system-overview.md`
- `docs/BLK-008_blk-test-mcp-execution-server.md`
- `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md`
- `docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md`
- `docs/BLK-019_blk-test-mcp-approval-source-evidence-authorization.md`
- `docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md`
- `docs/outcomes/BLK-SYSTEM-013_sprint-closeout.md`

## 2. Positive authority

BLK-SYSTEM-014 authorizes exactly one first live fixed-tool BLK-test MCP smoke under explicit human approval, and only after prerequisite gates are accepted. The allowed positive path is one dependency-free JSON-RPC/MCP-subset smoke over stdio-only transport, invoking the fixed tool `run_ast_validation` against a synthetic isolated workspace.

The operator approval must be explicit current human approval for one exact source/request/workspace/profile/tool envelope. No ambient approval is inferred from implementation authority, Codex/Hermes activity, prior sprint outcomes, Discord requests, or any stale approval.

## 3. Prerequisite gates preserved

- BLK-017 remains the active disabled transport contract for default/generic startup paths.
- BLK-018 remains the workspace/process-control probe contract and supplies required workspace, process, timeout, output, cache, and cleanup constraints.
- BLK-019 remains the approval/source-evidence authorization contract and must return `APPROVAL_VALIDATED_SOURCE_BOUND` before Sprint 014 can evaluate its own live-smoke checkpoint.

Sprint 014 adds a narrow positive checkpoint; it does not weaken or replace these prerequisite contracts.

## 4. Live-smoke constraints

The first smoke must be:

- stdio-only;
- dependency-free JSON-RPC/MCP-subset smoke;
- one run, one fixed tool, `run_ast_validation`;
- bounded by the approved timeout/output profile;
- source-bound to the approved synthetic BLK-pipe-shaped source evidence;
- replayable through approval/request/source/transcript hashes;
- executed only against a marker-owned synthetic isolated workspace.

The smoke must not run against `/home/dad/BLK-System`; it does not run against /home/dad/BLK-System and must not run against any real target repository. Workspace guards must reject repository roots, `.git` paths, symlink escapes, protected BLK-req vault prefixes, traversal, and unapproved paths.

## 5. Non-authority markers

BLK-SYSTEM-014 does not use arbitrary shell and does not use non-stdio transport. It does not mutate primary repo, does not stage files, does not commit, does not push, and does not grant source autofix behavior as BLK-test authority.

It does not read protected BLK-req vault bodies, does not authorize authoritative BEO publication, does not authorize RTM generation, and does not make RTM drift decisions.

It does not claim production sandbox or host-secret isolation. The Sprint 014 smoke is a bounded synthetic evidence path, not a production container/cgroup/VM/seccomp/AppArmor/SELinux or host-secret isolation guarantee.

## 6. Stop conditions

Stop before live smoke if the implementation is dirty or unpushed, if the approval does not bind the exact envelope, if `APPROVAL_VALIDATED_SOURCE_BOUND` is absent, if the requested tool is not exactly `run_ast_validation`, if transport is not stdio-only, or if any workspace guard fails.

Stop after Task 4 and do not create BLK-020 if the first live smoke returns `FAIL`, `BLOCKED`, `FATAL_TIMEOUT`, `FATAL_OUTPUT_FLOOD`, `TRANSPORT_ERROR`, or `OPERATOR_INTERRUPTED`.

## 7. Handoff

If and only if BLK-SYSTEM-014 records exactly one approved PASS smoke with cleanup verified, BLK-020 may record the accepted first-smoke evidence contract. BLK-020 must continue to state that BLK-017 remains disabled by default, BLK-018 remains prerequisite workspace/process-control doctrine, and BLK-019 remains prerequisite approval/source-evidence authorization doctrine.
