# BLK-SYSTEM-010 — Future Sprint Slicing and Doctrine Cross-Reference Gate

**Status:** Task 5 review artifact
**Sprint:** `blk-system-010`
**Purpose:** Convert the Sprint 010 fixture-to-live gap register into safe future sprint candidates while preventing Sprint 010 review artifacts from implying live BLK-test MCP, authoritative BEO, or RTM authority.

---

## 1. Boundary statement

Sprint 010 remains deterministic local review/design work only. Sprint 010 does not authorize live BLK-test MCP. Sprint 010 does not authorize authoritative BEO publication. Sprint 010 does not authorize RTM generation. Sprint 010 does not authorize RTM drift rejection authority.

This slicing document is a planning artifact, not an implementation brief. It does not authorize live MCP transport, live MCP client/server startup, live Codex, live tactical LLM calls, cyber tooling, cyber execution, production sandbox/container/cgroup/VM enforcement, host-secret isolation claims, active BLK-req vault reads, BEO publication, RTM ledger generation, or RTM drift rejection.

Source doctrine cross-referenced by this slicing gate:

- `docs/BLK-001_blk-system-master-architecture.md`
- `docs/BLK-003_blk-pipe-blk-test-orchestration.md`
- `docs/BLK-008_blk-test-mcp-execution-server.md`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`
- `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`
- `docs/reviews/BLK-SYSTEM-010_blk001-alignment-review.md`
- `docs/reviews/BLK-SYSTEM-010_fixture-to-live-gap-register.md`
- `docs/reviews/BLK-SYSTEM-010_approval-and-authority-decision-register.md`
- `docs/reviews/BLK-SYSTEM-010_sandbox-capability-readiness-spec.md`

The governing cross-reference rule is: BLK-008 may remain target-state planning doctrine, BLK-015/016 may remain disabled fixture/interface doctrine, and this Sprint 010 artifact may only slice future work. None of these documents may be read as current live BLK-test MCP authorization.

---

## 2. Future sprint candidate register

| Candidate sprint | allowed scope | explicit non-goals | prerequisite gates | BLK-001 domain protected | stop condition |
| --- | --- | --- | --- | --- | --- |
| `BLK-SYSTEM-011` — BLK-test MCP disabled live-transport skeleton, still non-executing | Define a stdio-only MCP server/client skeleton behind a disabled-by-default gate; prove startup refuses without explicit future approval; add lifecycle and shutdown probes that do not execute tests. | No live fixed-tool test execution, no source mutation, no network service, no HTTP/WebSocket transport, no BEO publication, no RTM generation, no active-vault reads, no production sandbox claims. | Non-executing transport tests; fail-closed approval preflight; no arbitrary shell registry test; proof that disabled default prevents transport startup. | `blk-test` Physics Oracle boundary and `blk-pipe` Blast Shield separation. | Any live process execution, socket/listener behavior, ambient approval acceptance, or source-write capability appears. |
| `BLK-SYSTEM-012` — Workspace isolation and process-control implementation probes | Implement deterministic probes for workspace clone/isolation, teardown, lock behavior, process-tree kill, timeout handling, and output-flood cleanup using inert local fixtures only. | No live MCP invocation against real repositories, no primary repo mutation, no source staging/commit, no host-secret exposure, no production container/cgroup/VM enforcement claims. | Same-filesystem/hardlink clone decision tests; path traversal rejection; stale/live lock tests; process group kill tests; timeout/output-flood tests; teardown after all statuses. | `blk-pipe` retains source mutation and allowlist authority; `blk-test` inspects only isolated copies. | A probe can alter the primary repo, leave orphan processes/workspaces, or claim production sandbox authority. |
| `BLK-SYSTEM-013` — Approval-channel and source-evidence authorization mechanics | Design and implement a BLK-test-specific approval validator that binds source BLK-pipe report identity, `beb_id`, source `commit_hash`, `pre_engine_hash`, canonical `trace_artifacts`, requested fixed BLK-test tool(s), test profile, workspace identity, timeout/output profile, and operator identity/timestamp. | No reuse of `codex-live` approval as BLK-test MCP approval; no live transport before validation; no arbitrary shell; no source mutation; no BEO publication; no RTM generation; no active-vault read authority. | Approval rejection tests for missing/extra/mismatched fields; replay/expiry tests; `codex-live` insufficiency test; exact source-evidence binding tests; audit evidence tests. | HITL Architecture & Feature Planning authority remains explicit; cryptographic baton remains opaque and source-bound. | Approval can be reused broadly, omits source identity, accepts `codex-live`, authorizes shell/mutation/publication/RTM, or starts transport before validation. |
| `BLK-SYSTEM-014` — First live fixed-tool BLK-test MCP smoke under explicit human approval | Run the first bounded fixed-tool BLK-test MCP smoke only after explicit human approval and only against an approved isolated workspace/profile. | No arbitrary shell, no cyber execution, no real target execution, no active BLK-req vault reads, no production sandbox claims, no source mutation, no authoritative BEO publication, no RTM generation. | Accepted gates from `BLK-SYSTEM-011` through `BLK-SYSTEM-013`; human approval record; fixed-tool registry; source binding; workspace/process controls; bounded output; replay bundle. | `blk-test` Physics Oracle emits deterministic PASS/FAIL/BLOCKED evidence while `blk-pipe` and RTM boundaries remain separate. | Approval absent, tool/profile mismatch, workspace/source mismatch, unbounded output, unknown status, blocked cleanup, secret leakage, or evidence cannot be replayed. |
| `BLK-SYSTEM-015` — Draft BEO publication gate review, still not authoritative unless explicitly approved | Review whether source-bound live BLK-test evidence may feed draft BEO fixture projection while preserving `beo_publication: "DRAFT_ONLY"` unless a later explicit publication sprint grants authority. | No authoritative BEO publication, no public outcome ledger mutation, no signer/storage/rollback authority, no RTM coverage claim, no BLOCKED-to-success projection. | Draft-only BEO gates; PASS/FAIL evidence source-binding gates; BLOCKED rejection; publication-field rejection; operator approval review for any future authority change. | BEO publication authority remains separate from `blk-test`; Hermes/outcome publication remains controlled. | Any document, test, or fixture implies Sprint 010 or `BLK-SYSTEM-015` has already authorized authoritative BEO publication. |
| Later RTM sprint — offline RTM generation and drift rejection | Separately design offline RTM generation and drift rejection using BEO trace hashes and active-vault hashes, after BEO publication authority and BLK-req access policy are explicitly settled. | No hidden RTM inside BLK-test MCP, no active-vault body parsing by BLK-test, no live MCP drift rejection, no requirement promotion, no RTM authority inherited from BEO or BLK-test PASS. | Active-vault hash-only access policy; ledger schema tests; drift decision tests; protected body exclusion tests; operator review and rollback plan; fixture-to-live cross-checks. | Traceability Aggregator owns ledger/drift authority; `blk-req` Legislative Gateway protects requirement bodies. | RTM reads protected bodies without authorization, BLK-test emits RTM fields, BEO fixtures imply coverage, or drift rejection occurs in a BLK-test MCP path. |

---

## 3. Cross-reference gate interpretation

The persistent doctrine gate introduced by Task 5 has two jobs:

1. Require this future sprint slicing document to use `BLK-SYSTEM-011` and later system-level sprint names instead of `BLK-PIPE-010`/`BLK-PIPE-011` for BLK-test MCP readiness work.
2. Require Sprint 010 review artifacts to repeat the exact non-authority markers: `does not authorize live BLK-test MCP`, `does not authorize authoritative BEO publication`, and `does not authorize RTM generation`.

The gate intentionally does not patch active doctrine unless a RED failure proves a missing or misleading cross-reference. At Task 5 time, the already-active BLK-008/015/016 boundary tests continue to pass, so this task records the cross-reference rule in Sprint 010 review artifacts rather than changing active doctrine text.

---

## 4. Derived future-sprint sequencing

Safe sequencing from the gap register is:

1. `BLK-SYSTEM-011` proves disabled, non-executing transport lifecycle shape.
2. `BLK-SYSTEM-012` proves workspace/process/resource controls without live MCP authority.
3. `BLK-SYSTEM-013` proves human approval and source-evidence binding mechanics.
4. `BLK-SYSTEM-014` may request explicit human authorization for first fixed-tool live smoke.
5. `BLK-SYSTEM-015` reviews draft BEO projection boundaries but remains draft-only unless a separate explicit publication sprint changes authority.
6. A Later RTM sprint separately owns offline RTM generation and drift rejection.

No candidate may combine live transport, arbitrary tools, source mutation, BEO publication, RTM generation, and active-vault reads in one broad authority leap.

---

## 5. Acceptance criteria

This slicing passes only if:

- every candidate includes allowed scope, explicit non-goals, prerequisite gates, BLK-001 domain protected, and stop condition;
- future sprint names use `BLK-SYSTEM-011` through `BLK-SYSTEM-015` for system readiness work;
- RTM remains a Later RTM sprint, separate from BLK-test MCP;
- Sprint 010 review artifacts carry exact non-authority markers;
- no active doctrine patch is made unless a deterministic RED gate proves the active doctrine cross-reference is missing or misleading;
- this task remains review/design only and does not start live BLK-test MCP, publish BEOs, generate RTM, read active vault bodies, or claim production sandbox authority.
