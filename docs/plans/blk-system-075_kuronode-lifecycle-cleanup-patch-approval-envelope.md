# BLK-SYSTEM-075 — Kuronode Lifecycle Cleanup Patch Approval Envelope Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `blk-system-authority-gated-sprints` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, `docs/BLK-059_blk-system-post-058-roadmap.md` as current roadmap authority, and BLK-001 through BLK-006 as applicable.

**Goal:** Convert the BLK-SYSTEM-074 lifecycle cleanup remediation packet into a deterministic review-only exact-target Kuronode patch approval envelope without applying or authorizing a patch.
**BLK-024 track:** Track F — BLK-test production-readiness ladder / Track C — BLK-pipe blast shield / Track A — doctrine and review gates / maturity level L1 fixture-only with L0 boundary doctrine.
**Architecture:** BLK-SYSTEM-075 packages a future human decision surface for the exact `smoke_test.ts:53 LIFECYCLE_CLEANUP_REQUIRED` patch. It binds the committed BLK-SYSTEM-074 remediation packet, exact Kuronode target path/branch/SHA, exact patch allowlist, candidate future patch mechanism, validation obligations, and fresh future runtime ID requirements while preserving no patch approval and no execution.
**Tech Stack:** Markdown, Python `unittest`, deterministic JSON/hash fixtures.
**Authority boundary:** Review-only patch approval envelope. No Kuronode source mutation, no Kuronode Git mutation, no BLK-pipe execution, no Codex execution, no BLK-test pilot rerun, no runtime validation, no BEO publication, no RTM generation.

---

## 0. Current Known State

Captured 2026-05-11T14:27:14+10:00.

BLK-System:

```text
## main...origin/main
60002c7 docs: close out blk-system 074 remediation packet
60002c778d3a6f20dc1ca404f2061467e39e9ed0 refs/heads/main
```

Kuronode:

```text
## main...origin/main
38e332b blk-pipe: apply bounded engine changes
38e332b188e45edcb484765694112c9041ad1a3b refs/heads/main
```

Upstream remediation packet status:

```text
KURONODE_LIFECYCLE_CLEANUP_REMEDIATION_PACKET_READY_NOT_PATCHED
```

Exact finding:

```text
smoke_test.ts:53 LIFECYCLE_CLEANUP_REQUIRED
```

---

## 1. Governing Doctrine

| Governing doc | Obligation for BLK-SYSTEM-075 |
| --- | --- |
| BLK-001 | Preserve V-model separation: planning/envelope readiness is not tactical mutation, BLK-test evidence, BEO publication, or RTM closure. |
| BLK-002 | Preserve HITL approval separation and protected-vault isolation. |
| BLK-003 | Keep BLK-test evidence-only; do not rerun the pilot or start production/generic BLK-test MCP. |
| BLK-004 | Treat BLK-pipe as the only approved mutation forge for any future patch; this sprint does not invoke it. |
| BLK-005 | Preserve trace binding and avoid coverage/drift promotion from a remediation packet or approval envelope. |
| BLK-006 | Preserve protected BLK-req hard-deny and no body reads. |
| BLK-075 | BLK-SYSTEM-074 remediation packet is review-ready not patched; future patch needs a separate explicit authority envelope. |

---

## 2. Non-Authority Boundary

This sprint does not authorize Kuronode source mutation, Kuronode Git mutation, staging, commit, push, reset, checkout, revert, stash, cleanup, autofix, remote writes, BLK-pipe execution, Codex execution, live tactical LLM dispatch, Electron launch, smoke-test execution, TypeScript compiler/linter/formatter runs, package-manager invocation, production or generic BLK-test MCP, reusable BLK-test service startup, arbitrary shell as BLK-test behavior, pilot reruns, reuse of BLK-SYSTEM-073 runtime IDs, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation, authoritative BEO publication, runtime `PUBLISHED` BEO output, RTM generation, RTM drift rejection, coverage matrix/claim promotion, active-vault hash comparison, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, or production sandbox/host-secret-isolation claims.

A patch approval envelope is not patch approval. A future patch sprint must receive explicit human approval and must re-check exact target state before any mutation.

---

## 3. Deliverables

1. `docs/outcomes/BLK-SYSTEM-075_task-000-outcome.md` — plan publication.
2. `python/kuronode_lifecycle_cleanup_patch_approval_envelope.py` — deterministic review-only envelope builder.
3. `python/test_kuronode_lifecycle_cleanup_patch_approval_envelope.py` — RED/GREEN tests for envelope readiness and hostile inputs.
4. `docs/BLK-076_kuronode-lifecycle-cleanup-patch-approval-envelope-boundary.md` — active boundary doctrine.
5. `python/test_active_doctrine_review_gates.py` update pinning BLK-076 markers and key code constants.
6. Task outcomes, hostile review, closeout.

---

## 4. Task Plan

### Task 000 — Publish plan

- Write this plan and Task 000 outcome.
- Verify Markdown fences and exact-path diff hygiene.
- Commit and push exact paths only.

### Task 001 — RED/GREEN approval-envelope fixture

- Add RED tests for a missing approval-envelope builder.
- Implement a deterministic builder that:
  - consumes a validated BLK-SYSTEM-074 remediation packet;
  - recomputes and binds the upstream packet hash;
  - binds exact Kuronode target repo/path/branch/SHA;
  - declares `READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PATCHED` status;
  - includes exact allowed modified files and no new files;
  - includes patch mechanism proposal only, not execution;
  - rejects `approval_granted=True`, runtime execution claims, retired BLK-SYSTEM-073 ID reuse, nested laundering, protected paths, and denied-authority mismatches;
  - emits complete false side-effect flags.
- Record Task 001 outcome.

### Task 002 — Boundary doctrine and active gate

- Add BLK-076 boundary doctrine.
- Add active doctrine gate proving BLK-076 exists and preserving review-only/no-authority markers.
- Record Task 002 outcome.

### Task 003 — Hostile review and remediation

- Hostile-review for approval laundering, target retargeting, stale/upstream packet forgery, exact allowlist gaps, protected-path smuggling, runtime ID reuse, BLK-pipe/Codex/source mutation laundering, BEO/RTM/coverage/drift laundering, and incomplete false flags.
- Remediate blockers with additional tests/code/doc patches.
- Record review and Task 003 outcome.

### Task 004 — Verification and closeout

- Run focused envelope tests.
- Run focused active doctrine gate.
- Run full Python suite.
- Run Go suite.
- Run `git diff --check` and Markdown fence checks.
- Write closeout and Task 004 outcome.
- Commit, push, and verify remote sync.

---

## 5. Success Criteria

BLK-SYSTEM-075 is complete only when:

- the plan and all outcomes are committed and pushed;
- the approval envelope is review-ready only and not executable approval;
- upstream BLK-SYSTEM-074 packet identity is recomputed and bound;
- exact Kuronode target SHA/path/allowlist is pinned;
- BLK-076 is pinned by active doctrine gates;
- hostile review blockers are remediated;
- focused/full verification is green;
- Kuronode remains clean/synced and unmodified by this sprint.
