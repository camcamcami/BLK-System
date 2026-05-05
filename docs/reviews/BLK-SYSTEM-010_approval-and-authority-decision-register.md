# BLK-SYSTEM-010 — Approval and Authority Boundary Decision Register

**Status:** Task 3 review artifact  
**Sprint:** `blk-system-010`  
**Purpose:** Define the approval and authority boundary that any future live BLK-test MCP transport must satisfy before startup, without implementing approval-channel mechanics or granting live authority.

---

## 1. Scope and source doctrine

This decision register is deterministic local review/design work only. It records future approval requirements for BLK-test MCP readiness and does not authorize live BLK-test MCP, live MCP transport, live Codex, live tactical LLM calls, cyber execution, authoritative BEO publication, RTM generation, RTM drift rejection authority, active BLK-req vault reads, or production sandbox/host-secret claims.

Source doctrine reviewed for this boundary:

- `docs/BLK-001_blk-system-master-architecture.md`
- `docs/BLK-008_blk-test-mcp-execution-server.md`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`
- `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`
- `docs/reviews/BLK-SYSTEM-010_blk001-alignment-review.md`
- `docs/reviews/BLK-SYSTEM-010_fixture-to-live-gap-register.md`

The governing distinction is exact: codex-live approval is not BLK-test MCP approval. `codex-live` approval in BLK-015 records audit-only tactical-engine approval evidence and still does not execute live Codex. A future BLK-test MCP approval must be a separate human authorization record for a fixed-tool physics-oracle transport startup.

---

## 2. Decision register

| Decision ID | Boundary question | Decision | BLK-001 rationale | Future mechanical gate |
| --- | --- | --- | --- | --- |
| AUTH-001 | Can `codex-live` approval authorize live BLK-test MCP? | No. codex-live approval is not BLK-test MCP approval. | Tactical implementation approval and physics-oracle approval bind different authority surfaces. BLK-test must not inherit tactical LLM approval semantics. | A future gate must reject BLK-test MCP startup when only a `BLK_APPROVE_CODEX_LIVE` token or `codex-live` audit record is present. |
| AUTH-002 | What source identity must future approval bind? | BLK-test MCP approval must bind the source BLK-pipe report identity, `beb_id`, source commit_hash, `pre_engine_hash`, canonical trace_artifacts, target branch/workspace identity, and the exact test profile. | The cryptographic baton crosses domains as opaque metadata; BLK-test must verify the source evidence produced by `blk-pipe`, not a guessed branch, stale commit, or unbound workspace. | Startup must fail closed unless approval fields exactly match the source BLK-pipe report and request envelope. |
| AUTH-003 | When must approval occur? | Live BLK-test MCP approval must require human authorization before transport startup. | HITL authority remains explicit and cannot be inferred by an agent, fixture, transport process, or prior sprint document. | The MCP server/client startup path must check approval before opening stdio transport, allocating workspace, acquiring lock for execution, or spawning native test processes. |
| AUTH-004 | What capabilities can approval never grant? | Approval must not grant arbitrary shell; approval must not grant source mutation; approval must not grant BEO publication; approval must not grant RTM generation; approval must not grant active-vault read authority. | BLK-test is a fixed-tool Physics Oracle. Source mutation remains with `blk-pipe`; publication and ledger authority remain separate; `blk-req` protected vault bodies remain outside the BLK-test domain. | Future contract tests must enumerate tools and reject shell/eval/exec/command capabilities, write/stage/commit paths, BEO publication fields, RTM output fields, and protected active-vault file reads. |
| AUTH-005 | Which request/tool fields must be bound? | Approval record must include requested fixed BLK-test tool(s), target branch/workspace identity, timeout/output profile, and operator identity/approval timestamp when implemented. | Fixed tool, workspace, resource, and human identity binding prevents broad reusable approvals from becoming ambient live-execution authority. | A future approval validator must reject missing tools, extra tools, changed workspace identity, changed timeout/output profile, missing operator identity/approval timestamp, or replay outside the approved time/window policy. |
| AUTH-006 | Does Sprint 010 implement the approval channel? | No. Sprint 010 records requirements only and does not implement approval-channel mechanics. | This sprint is a review/design sprint; implementing tokens, transport, server skeletons, or approval storage would silently expand authority beyond the plan. | The current repository must remain fixture-only/disabled; any future implementation requires a separate sprint with RED/GREEN transport, approval, audit, rollback, and non-authority gates. |

---

## 3. Future approval record fields

A later implementation sprint must define the exact storage, signature, replay, expiry, and operator workflow. This Task 3 register only records field requirements.

Minimum future approval record fields:

1. `beb_id` copied from the approved BLK-pipe report.
2. source commit_hash copied from the source report and bound to the working tree under test.
3. `pre_engine_hash` copied from the source report.
4. canonical trace_artifacts copied from the source report, with `trace_artifacts[*].version_hash == sha256:<64-lowercase-hex>`.
5. source BLK-pipe report identity, including a stable report path/hash/id when implemented.
6. requested fixed BLK-test tool(s), never a wildcard or dynamic command.
7. test profile, such as a named fixed-tool profile rather than a free-form shell command.
8. target branch/workspace identity, including the exact branch, workspace clone id, and source path policy when implemented.
9. timeout/output profile, including timeout class and output byte/compression budget.
10. operator identity/approval timestamp, with later sprint policy for expiry, replay resistance, and audit trail.

The approval must be one-run/scoped. It must not become a reusable ambient permission for arbitrary BLK-test MCP sessions.

---

## 4. Blocked-token example for future design only

The following blocked-token example is deliberately non-executable and incomplete. It illustrates what Sprint 010 refuses to treat as sufficient approval:

```text
blocked-token example: BLK_APPROVE_CODEX_LIVE beb_id=BEB_010 target_branch=sprint/blk-system-010 trace_hash=sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Why this is blocked for BLK-test MCP:

- it is a `codex-live` token, not a BLK-test MCP approval;
- it does not bind the source BLK-pipe report identity;
- it does not bind source commit_hash, `pre_engine_hash`, or canonical trace_artifacts as a complete source evidence envelope;
- it does not list requested fixed BLK-test tool(s) or test profile;
- it does not bind target branch/workspace identity beyond a branch label;
- it does not bind timeout/output profile;
- it does not carry operator identity/approval timestamp for a BLK-test MCP approval event;
- it must not start live transport, spawn processes, mutate source, publish BEOs, generate RTM, or read active-vault bodies.

This document does not define a replacement executable token. Future token/storage design belongs to a later sprint after the approval boundary is accepted.

---

## 5. Acceptance criteria for future implementation work

Future live BLK-test MCP approval design is acceptable only if all of the following are mechanically proven in a later sprint:

- no live transport starts without exact BLK-test-specific human authorization before transport startup;
- codex-live approval is not BLK-test MCP approval and cannot be accepted as a substitute;
- approval binds `beb_id`, source commit_hash, `pre_engine_hash`, canonical trace_artifacts, source BLK-pipe report identity, requested fixed BLK-test tool(s), test profile, target branch/workspace identity, timeout/output profile, and operator identity/approval timestamp;
- approval must not grant arbitrary shell, source mutation, BEO publication, RTM generation, or active-vault read authority;
- BLOCKED or incomplete evidence cannot be laundered into PASS/FAIL, authoritative BEO, RTM, or BLK-req promotion paths;
- the implementation includes replay/audit evidence without storing secrets or protected BLK-req vault bodies.

---

## 6. Review disposition

Task 3 records approval and authority boundary requirements only. It does not implement approval-channel mechanics, does not create an MCP server skeleton, does not create an executable approval token, and does not authorize live BLK-test MCP. Future live approval work remains blocked until a later explicitly approved sprint adds fail-closed gates for approval validation, transport startup, fixed-tool registry, source binding, sandbox/workspace controls, and audit evidence.
