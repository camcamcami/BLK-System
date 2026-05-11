# BLK-SYSTEM-074 — Kuronode Lifecycle Cleanup Remediation Packet Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `blk-system-authority-gated-sprints` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, `docs/BLK-059_blk-system-post-058-roadmap.md` as current roadmap authority, and BLK-001 through BLK-006 as applicable.

**Goal:** Convert the BLK-SYSTEM-073 read-only BLK-test finding `smoke_test.ts:53 LIFECYCLE_CLEANUP_REQUIRED` into a deterministic remediation packet and active boundary without rerunning the pilot or mutating Kuronode.
**BLK-024 track:** Track F — BLK-test production-readiness ladder / Track A — doctrine and review gates / maturity level L1 fixture-only with L0 boundary doctrine.
**Architecture:** BLK-test evidence remains evidence only. BLK-SYSTEM-074 consumes committed BLK-SYSTEM-073 evidence and emits a review-ready remediation packet for a future Kuronode cleanup patch, while preserving source/Git sterility and one-run ID retirement. The sprint does not execute Electron, TypeScript tooling, package managers, Codex, BLK-pipe, production BLK-test MCP, BEO publication, or RTM generation.
**Tech Stack:** Markdown, Python `unittest`, deterministic JSON/hash fixtures.
**Authority boundary:** Fixture-only remediation packet and doctrine gate. No Kuronode source mutation, no Kuronode Git mutation, no pilot rerun, no patch approval, no production BLK-test MCP.

---

## 0. Current Known State

Captured 2026-05-11T13:46:35+10:00.

BLK-System:

```text
## main...origin/main
ccc1835 docs: close out blk-system 073 read-only pilot
ccc1835c351e32fa5f22367b01c198000fc74d95 refs/heads/main
```

Kuronode:

```text
## main...origin/main
38e332b blk-pipe: apply bounded engine changes
38e332b188e45edcb484765694112c9041ad1a3b refs/heads/main
```

BLK-SYSTEM-073 runtime evidence:

```text
status: FAIL
pilot_status: BLK_TEST_KURONODE_WORKSPACE_READ_ONLY_PILOT_FAIL_EVIDENCE_ONLY
finding: smoke_test.ts:53 LIFECYCLE_CLEANUP_REQUIRED
approval_id: APPROVAL-BLK-SYSTEM-073-KURONODE-WORKSPACE-001
run_id: RUN-BLK-SYSTEM-073-KURONODE-WORKSPACE-001
```

Those IDs are consumed and retired. This sprint must not rerun them.

---

## 1. Governing Doctrine

| Governing doc | Obligation for BLK-SYSTEM-074 |
| --- | --- |
| BLK-001 | Preserve separation between planning, BLK-pipe mutation, BLK-test evidence, BEO publication, and blk-link trace closure. |
| BLK-002 | Preserve HITL and staged authority boundaries; do not mutate or read protected active-vault bodies. |
| BLK-003 | Treat BLK-test as evidence-only and keep production/generic BLK-test MCP disabled. |
| BLK-004 | Keep BLK-pipe as the only bounded mutation forge; this sprint does not invoke it. |
| BLK-005 | Preserve trace binding and avoid coverage/drift promotion from a BLK-test finding. |
| BLK-006 | Preserve protected-vault hard-deny and no protected body reads. |
| BLK-059 | Satisfies the Remediation rule: fixes a demonstrated BLK-test finding without combining authority jumps. |
| BLK-074 | Consumes BLK-SYSTEM-073 runtime evidence as evidence-only; does not inherit rerun or mutation authority. |

---

## 2. Non-Authority Boundary

This sprint does not authorize production BLK-test MCP, generic BLK-test MCP, reusable BLK-test service startup, arbitrary shell as BLK-test behavior, Electron launch, smoke-test execution, TypeScript compiler/linter/formatter runs, package-manager invocation, network/model/browser/cyber tooling, live Codex execution, BLK-pipe execution, Kuronode source mutation, Kuronode Git mutation, staging, commit, push, reset, checkout, cleanup, protected BLK-req vault body reads/copying/parsing/hashing/summarizing/scanning/mutation, authoritative BEO publication, runtime `PUBLISHED` BEO output, RTM generation, RTM drift rejection, coverage matrix/claim promotion, active-vault hash comparison, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, or production sandbox/host-secret-isolation claims.

A remediation packet is not patch approval. A future patch requires a separate explicit authority envelope and exact allowlist.

---

## 3. Deliverables

1. `docs/outcomes/BLK-SYSTEM-074_task-000-outcome.md` — plan-publication outcome.
2. `python/blk_test_kuronode_lifecycle_cleanup_remediation_packet.py` — deterministic packet builder consuming committed BLK-SYSTEM-073 evidence.
3. `python/test_blk_test_kuronode_lifecycle_cleanup_remediation_packet.py` — RED/GREEN fixture and hostile-input tests.
4. `docs/BLK-075_blk-test-kuronode-lifecycle-cleanup-remediation-boundary.md` — active boundary for evidence-to-remediation packet semantics.
5. `python/test_active_doctrine_review_gates.py` update pinning BLK-075 markers.
6. `docs/outcomes/BLK-SYSTEM-074_task-001-outcome.md` through closeout.
7. `docs/reviews/BLK-SYSTEM-074_kuronode-lifecycle-cleanup-remediation-hostile-review.md`.
8. `docs/outcomes/BLK-SYSTEM-074_sprint-closeout.md`.

---

## 4. Task Plan

### Task 000 — Publish plan

- Write this plan.
- Write Task 000 outcome.
- Verify Markdown fences and exact-path diff hygiene.
- Commit and push exact paths only.

### Task 001 — RED/GREEN remediation packet fixture

- Add RED tests for a missing remediation packet builder.
- Implement a deterministic builder that:
  - loads/validates committed BLK-SYSTEM-073 evidence;
  - requires exact FAIL evidence for `smoke_test.ts:53 LIFECYCLE_CLEANUP_REQUIRED`;
  - rejects reused BLK-SYSTEM-073 approval/run IDs as future runtime IDs;
  - rejects nested/free-text authority laundering;
  - emits exact denied authorities and no-side-effect booleans;
  - emits review-ready lifecycle cleanup obligations for a future patch.
- Record Task 001 outcome.

### Task 002 — Boundary doctrine and persistent gate

- Add BLK-075 boundary doctrine.
- Add active doctrine gate proving BLK-075 exists and preserves evidence-only/no-authority markers.
- Record Task 002 outcome.

### Task 003 — Hostile review and remediation

- Review for authority laundering, PASS-as-approval, patch-authority laundering, runtime-ID reuse, evidence-hash forgery, nested protected-path/secret strings, and incomplete no-side-effect flags.
- Remediate blockers with tests/code/doc patches before closeout.
- Record hostile review and Task 003 outcome.

### Task 004 — Verification and closeout

- Run focused packet tests.
- Run focused active doctrine gate.
- Run full Python suite.
- Run Go suite.
- Run `git diff --check` and Markdown fence checks.
- Write closeout and Task 004 outcome.
- Commit, push, and verify remote sync.

---

## 5. Success Criteria

BLK-SYSTEM-074 is complete only when:

- the plan and all outcomes are committed and pushed;
- the remediation packet validates the exact committed BLK-SYSTEM-073 evidence and rejects forged/laundered inputs;
- BLK-075 is pinned by an active doctrine gate;
- hostile review blockers are remediated;
- full verification is green;
- Kuronode remains clean/synced and unmodified by this sprint.
