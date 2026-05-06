# BLK-SYSTEM-013 — Approval/Source-Evidence Boundary Review

**Status:** Task 1 boundary review artifact
**Sprint:** `BLK-SYSTEM-013`
**Purpose:** Define the approval-channel and source-evidence authorization mechanics that Sprint 013 may implement before any future live BLK-test MCP smoke.

---

## 1. Source doctrine reviewed

This review preserves the authority boundaries in:

- `docs/BLK-001_blk-system-master-architecture.md`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md`
- `docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md`
- `docs/reviews/BLK-SYSTEM-010_approval-and-authority-decision-register.md`
- `docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md`
- `docs/outcomes/BLK-SYSTEM-012_sprint-closeout.md`

BLK-SYSTEM-013 owns Approval-channel and source-evidence authorization mechanics. It does not inherit live authority from earlier disabled transport, fixture, or workspace/process-control probe sprints.

---

## 2. Governing approval distinction

The governing distinction is exact: codex-live approval is not BLK-test MCP approval.

A `BLK_APPROVE_CODEX_LIVE` token, `codex-live` profile, tactical-engine approval record, or implementation-run approval does not authorize BLK-test MCP startup. BLK-test MCP approval must be a separate BLK-test-specific human authorization record bound to one exact source/request/workspace/profile envelope.

---

## 3. Allowed Sprint 013 authorization mechanics

Sprint 013 may implement deterministic local validation for an approval record that binds all of the following fields:

- source BLK-pipe report identity;
- `beb_id`;
- source commit_hash;
- `pre_engine_hash`;
- canonical trace_artifacts with `trace_artifacts[*].version_hash == sha256:<64-lowercase-hex>`;
- requested fixed BLK-test tool(s);
- test profile;
- workspace identity;
- timeout/output profile;
- operator identity/approval timestamp;
- one-run/scoped approval identity, expiry, replay/audit metadata.

The approval validator may return deterministic audit evidence, including source-evidence hash, approval-record hash, authorization-request hash, and a fail-closed decision. Those hashes are evidence identifiers only; they are not truth, mutation, publication, RTM, or live transport authority.

---

## 4. Non-authority markers

Sprint 013 explicitly:

- does not authorize live BLK-test MCP;
- does not authorize live MCP client/server startup;
- does not execute fixed-tool tests;
- does not mutate primary repo;
- does not stage files;
- does not commit;
- does not push as BLK-test behavior;
- does not grant arbitrary shell or dynamic command execution;
- does not authorize authoritative BEO publication;
- does not authorize RTM generation;
- does not authorize RTM drift rejection authority;
- does not read protected BLK-req vault bodies;
- does not parse active-vault requirement bodies;
- does not claim production sandbox/cgroup/VM/seccomp/AppArmor/SELinux enforcement;
- does not claim production host-secret isolation.

Human executor commits/pushes for reviewed Sprint 013 code and outcome documentation are project-maintenance actions, not BLK-test source-mutation authority.

---

## 5. BLK-001 domain preservation

- `blk-req` remains the protected requirement gateway; Sprint 013 binds opaque trace metadata only and does not read protected bodies.
- `blk-pipe` remains source-mutation and staging authority; Sprint 013 only copies exact source evidence.
- `blk-test` remains a physics oracle boundary; Sprint 013 validates approval/source evidence but does not execute the oracle.
- `blk-link` remains offline traceability/RTM ledger authority; Sprint 013 preserves `rtm_status: NOT_GENERATED`.
- BEO publication authority remains separate; Sprint 013 preserves `beo_publication: DRAFT_ONLY` for fixture/preflight evidence.

---

## 6. Rejection requirements

Sprint 013 gates must reject approval records or preflight decisions when:

- required source evidence is missing;
- source BLK-pipe report identity does not match;
- `beb_id`, source commit_hash, or `pre_engine_hash` differs;
- canonical trace_artifacts differ or contain malformed hashes;
- requested fixed BLK-test tool(s) are missing, extra, wildcard, unknown, shell-like, or dynamic;
- test profile, workspace identity, or timeout/output profile differs;
- operator identity/approval timestamp is missing;
- approval is expired or replayed;
- approval text attempts to reuse `codex-live` or `BLK_APPROVE_CODEX_LIVE`;
- any record attempts source mutation, BEO publication, RTM generation, active-vault body reads, or arbitrary shell authority.

---

## 7. Handoff boundary

Sprint 013 may make approval/source-evidence validation pass for a future exact BLK-test MCP startup envelope, but Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke.

Sprint 014 must still require explicit human approval, intact BLK-017/BLK-018/BLK-019 gates, fixed-tool-only scope, bounded workspace/process controls, and continued non-authority for arbitrary shell, source mutation, authoritative BEO publication, RTM generation, and protected BLK-req vault body reads unless a later human-approved sprint explicitly grants those authorities.
