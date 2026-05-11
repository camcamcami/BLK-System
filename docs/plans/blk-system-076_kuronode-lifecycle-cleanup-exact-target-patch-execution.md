# BLK-SYSTEM-076 — Kuronode Lifecycle Cleanup Exact-Target Patch Execution Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, `blk-system-authority-gated-sprints`, `aaa-001-multi-agent-codex-orchestration`, and Kuronode closeout skills while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, `docs/BLK-059_blk-system-post-058-roadmap.md` for current selection, BLK-001 through BLK-006 for authority boundaries, and BLK-SYSTEM-075 for the exact-target approval envelope.

**Goal:** Apply one exact-target Kuronode lifecycle cleanup patch for `scripts/smoke_test.ts` at `38e332b188e45edcb484765694112c9041ad1a3b`, then verify and close out without expanding adjacent authority.
**BLK-024 track:** Track F — BLK-test production-readiness ladder / Track C — BLK-pipe blast shield and forge / Track A — doctrine and review gates; maturity level L4 exact-target approved source mutation through bounded forge.
**Architecture:** BLK-SYSTEM-076 consumes the BLK-SYSTEM-075 review-only approval envelope plus the operator's explicit instruction: `Write the plan for BLK-SYSTEM-076 and execute it with exact-target Kuronode patch authority for scripts/smoke_test.ts at 38e332b. Then execute all tasks`. The sprint re-checks local and remote Kuronode `main` at the approved SHA, executes only the allowlisted patch via BLK-pipe exact-target payload, runs approved Kuronode validation, performs Kuronode MCP closeout review, hostile-audits the result, and records BLK-System outcomes.
**Tech Stack:** Markdown, Python/Go BLK-pipe payloads, TypeScript smoke test source, npm validation commands, Kuronode MCP closeout.
**Authority boundary:** Exact-target Kuronode source mutation authority for `scripts/smoke_test.ts` at `38e332b188e45edcb484765694112c9041ad1a3b` only. Kuronode Git commit/push authority is granted only for the BLK-pipe-produced allowlisted patch commit and only after validation/hostile audit. No other Kuronode files may change.

---

## 0. Current Known State

Captured 2026-05-11T14:59:38+10:00.

BLK-System:

```text
## main...origin/main
213cdfb docs: close out blk-system 075 patch envelope
213cdfb3b928bea2c142728472e005b26c1b8c8a refs/heads/main
```

Kuronode:

```text
## main...origin/main
38e332b blk-pipe: apply bounded engine changes
38e332b188e45edcb484765694112c9041ad1a3b refs/heads/main
```

Approved target:

```text
target_repo_path: /home/dad/code/Kuronode-v1
target_branch: main
target_head_sha: 38e332b188e45edcb484765694112c9041ad1a3b
allowed_modified_files: scripts/smoke_test.ts
allowed_new_files: []
fresh_patch_approval_id: APPROVAL-BLK-SYSTEM-076-KURONODE-LIFECYCLE-CLEANUP-PATCH-001
fresh_patch_run_id: RUN-BLK-SYSTEM-076-KURONODE-LIFECYCLE-CLEANUP-PATCH-001
```

Source finding:

```text
smoke_test.ts:53 LIFECYCLE_CLEANUP_REQUIRED
```

---

## 1. Governing Doctrine

| Governing doc | Obligation for BLK-SYSTEM-076 |
| --- | --- |
| BLK-001 | Preserve V-model separation: this patch fixes Kuronode source only; it is not BLK-test PASS, BEO publication, RTM closure, coverage truth, or drift authority. |
| BLK-002 | Preserve HITL approval boundaries and protected-vault isolation. |
| BLK-003 | Use bounded orchestration and hostile audit; do not rerun BLK-test functional-module runtime or reuse retired BLK-SYSTEM-073 IDs. |
| BLK-004 | Use BLK-pipe as deterministic mutation forge with exact allowlist, target hash, output caps, validation, and Git evidence. |
| BLK-005 | Preserve trace binding and avoid coverage/drift promotion. |
| BLK-006 | Preserve protected BLK-req hard-deny and no body reads. |
| BLK-076 | Review-only envelope is consumed as target/allowlist evidence; it does not itself create publication/RTM/BLK-test authority. |

---

## 2. Authorized Scope

Authorized:

1. Re-check local and observed remote Kuronode `main` equal `38e332b188e45edcb484765694112c9041ad1a3b` before mutation.
2. Add a RED focused lifecycle cleanup gate proving `scripts/smoke_test.ts` lacks deterministic timeout/subscription cleanup.
3. Invoke BLK-pipe exactly once for the approved target SHA with:
   - `allowed_modified_files: ["scripts/smoke_test.ts"]`
   - `allowed_new_files: []`
   - target hash `38e332b188e45edcb484765694112c9041ad1a3b`
   - fresh run ID `RUN-BLK-SYSTEM-076-KURONODE-LIFECYCLE-CLEANUP-PATCH-001`
4. Patch only the smoke test lifecycle boundary so the projection-result listener unsubscribes and timeout guard clears deterministically on success, timeout, invalid shape, or thrown error.
5. Run approved validation:
   - static lifecycle cleanup check;
   - `git diff --check` / post-commit clean status;
   - TypeScript/package validation needed to verify the touched smoke script;
   - `npm run test:smoke` as Kuronode validation if environment permits.
6. Commit and push the resulting Kuronode patch only after hostile audit and Kuronode MCP closeout review pass.
7. Record BLK-System outcomes and closeout.

---

## 3. Explicit Non-Authority Boundary

This sprint does not authorize mutation of any Kuronode file except `scripts/smoke_test.ts`; does not authorize arbitrary Kuronode refactors; does not authorize package installs, dependency changes, generated artifact commits, or lockfile changes; does not authorize BLK-test functional-module runtime rerun or reuse of BLK-SYSTEM-073 IDs; does not authorize production/generic BLK-test MCP; does not authorize BEO publication, runtime `PUBLISHED` BEO output, RTM generation, RTM drift rejection, coverage matrix/claim promotion, active-vault hash comparison, protected BLK-req body reads/copying/parsing/hashing/scanning/mutation, public ledger mutation, signer/storage/rollback/release authority, or production sandbox/host-secret-isolation claims.

`npm run test:smoke` is allowed only as Kuronode validation for the patched smoke script, not as BLK-test functional-module authority or publication/RTM evidence.

---

## 4. Task Plan

### Task 000 — Publish plan

- Write this plan and Task 000 outcome.
- Verify exact-path Markdown fences and diff hygiene.
- Commit/push BLK-System plan publication.

### Task 001 — Exact-target preflight and RED gate

- Verify BLK-System and Kuronode status are clean/synced.
- Verify local `HEAD` and observed `origin/main` equal approved SHA.
- Run a focused RED lifecycle cleanup check against `scripts/smoke_test.ts` that fails on the existing missing cleanup.
- Record Task 001 outcome.

### Task 002 — BLK-pipe exact-target patch execution

- Build a deterministic BLK-pipe payload with target hash, exact allowlist, fresh approval/run IDs, and no adjacent authority.
- Use a deterministic Python engine script to patch only `scripts/smoke_test.ts`.
- BLK-pipe validation must include `git diff --check -- scripts/smoke_test.ts` and the focused lifecycle cleanup assertion.
- Record raw BLK-pipe report, commit hash, diff summary, and Task 002 outcome.

### Task 003 — Kuronode validation and closeout review

- Run approved Kuronode validation without mutating additional files.
- Run Kuronode MCP closeout review (`sysml_get_closeout_policy`, `sysml_task_closeout_review`) and record result.
- Commit/push the Kuronode patch if not already pushed by Task 002 and verify remote sync.
- Record Task 003 outcome.

### Task 004 — Hostile audit

- Hostile-audit exact file allowlist, target SHA binding, no forbidden files, no generated artifacts, no retired ID reuse, no BLK-test/BEO/RTM/coverage/drift laundering, and Kuronode closeout evidence.
- Remediate only if findings remain within exact authority; otherwise stop and escalate.
- Record review and Task 004 outcome.

### Task 005 — BLK-System verification and closeout

- Run BLK-System focused/full verification as needed.
- Run Markdown fence checks and `git diff --check`.
- Write BLK-SYSTEM-076 sprint closeout.
- Commit/push BLK-System outcomes and verify BLK-System/Kuronode remote sync.

---

## 5. Success Criteria

BLK-SYSTEM-076 is complete only when:

- plan/outcomes/review/closeout are committed and pushed to BLK-System;
- Kuronode contains exactly one approved patch commit derived from `38e332b188e45edcb484765694112c9041ad1a3b` and touching only `scripts/smoke_test.ts`;
- focused lifecycle cleanup RED/GREEN evidence is recorded;
- approved Kuronode validation is recorded;
- Kuronode MCP closeout review passes or is explicitly dispositioned under its configured policy;
- hostile audit finds no remaining blockers;
- BLK-System and Kuronode are clean and synced.
