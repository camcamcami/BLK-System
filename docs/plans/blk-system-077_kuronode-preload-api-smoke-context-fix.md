# BLK-SYSTEM-077 — Kuronode Preload API Smoke Context Fix Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `systematic-debugging`, `test-driven-development`, `kuronode-headless-smoke-test`, and `repo-mcp-closeout-via-stdio` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first for maturity vocabulary, `docs/BLK-059_blk-system-post-058-roadmap.md` for current roadmap authority, and BLK-001 through BLK-006 as applicable.

**Goal:** Fix the Kuronode headless smoke blocker `Kuronode preload API missing` at exact Kuronode HEAD `3bf24938df32fb4843713a41bb2a0234e0ecf324`, then run the smoke test and close out.
**BLK-024 track:** Track F — BLK-test evidence ladder / Track C — BLK-pipe blast shield and forge / Track A — doctrine and review gates; maturity level L4 exact-target Kuronode runtime smoke remediation.
**Architecture:** BLK-SYSTEM-077 follows BLK-SYSTEM-076. The failure is now before projection-result observation: the smoke script checks `KuronodeAPI` on the Playwright `Page` object instead of inside the renderer `window` context. The patch must correct only that smoke-script preflight context boundary and preserve Electron security settings.
**Tech Stack:** TypeScript, Electron, Playwright, Xvfb, Markdown, Kuronode MCP closeout.
**Authority boundary:** Exact-target Kuronode source mutation authority for `/home/dad/code/Kuronode-v1/scripts/smoke_test.ts` and `/home/dad/code/Kuronode-v1/packages/electron/src/main/file-watcher.ts` only at `3bf24938df32fb4843713a41bb2a0234e0ecf324`. Initial RED evidence found the smoke script checks the preload API in the wrong execution context; post-fix smoke advanced and surfaced a second exact runtime blocker in worker path resolution from bundled `dist/main/chunks`. This committed plan amendment authorizes the minimal file-watcher worker-path fix needed to complete the same smoke-test objective.

---

## 0. Current Known State

Captured 2026-05-11T16:05:18+10:00.

BLK-System:

```text
## main...origin/main
b921c66 docs: close out blk-system 076 patch execution
b921c6626e28ec5a652b784d8d40167351a79f7c
b921c6626e28ec5a652b784d8d40167351a79f7c
```

Kuronode:

```text
## main...origin/main
3bf2493 blk-pipe: apply bounded engine changes
3bf24938df32fb4843713a41bb2a0234e0ecf324
3bf24938df32fb4843713a41bb2a0234e0ecf324
```

BLK-SYSTEM-076 remaining blocker:

```text
npm run test:smoke
[FAIL] Smoke test failed: Error: Kuronode preload API missing
scripts/smoke_test.ts:41
```

Initial diagnosis from source inspection:

```text
scripts/smoke_test.ts checks (window as Window).KuronodeAPI on the Playwright Page object.
The preload API lives on the renderer's DOM window and must be checked with page.evaluate().
```

---

## 1. Governing Doctrine

| Governing doc | BLK-SYSTEM-077 obligation |
| --- | --- |
| BLK-001 | Keep BLK-System planning/audit separate from Kuronode source mutation and runtime evidence. |
| BLK-003 | Treat smoke output as evidence only; no BEO/RTM/coverage promotion. |
| BLK-004 | Use exact allowlists, exact target SHA, exact staging, and hostile audit for source mutation. |
| BLK-006 | Do not read or mutate protected BLK-req bodies. |
| BLK-059 | Current roadmap allows targeted Kuronode tactical quality work only under exact authority boundaries. |
| Kuronode AGENTS.md | Run validation, requirement/use-case causality review, and MCP closeout before declaring completion. |

---

## 2. Authorized Scope

Authorized:

1. Re-check BLK-System and Kuronode clean/synced state.
2. Reproduce the `Kuronode preload API missing` failure or use the recorded BLK-SYSTEM-076 failure as RED evidence if unchanged.
3. Add/execute a focused RED static gate proving the smoke script performs preload API access outside `page.evaluate()`.
4. Patch only `scripts/smoke_test.ts` so the smoke script verifies `window.KuronodeAPI` inside renderer context.
5. Preserve the existing lifecycle cleanup patch from BLK-SYSTEM-076.
6. Run focused TypeScript validation and `npm run test:smoke`.
7. Run Kuronode MCP closeout review.
8. Hostile-audit file boundaries, smoke evidence, no authority laundering, and no generated artifact commits.
9. Commit/push Kuronode and BLK-System docs.

---

## 3. Explicit Non-Authority Boundary

This sprint does not authorize mutation of any Kuronode file except `scripts/smoke_test.ts` and `packages/electron/src/main/file-watcher.ts`; does not authorize arbitrary Electron refactors; does not authorize dependency or lockfile changes; does not authorize BLK-test functional-module runtime beyond the Kuronode smoke validation command; does not authorize production/generic BLK-test MCP; does not authorize BEO publication, runtime `PUBLISHED` BEO output, RTM generation, RTM drift rejection, coverage matrix/claim promotion, protected BLK-req body reads/copying/parsing/hashing/scanning/mutation, public ledger mutation, signer/storage/rollback/release authority, or production sandbox/host-secret-isolation claims.

---

## 4. Task Plan

### Task 000 — Publish plan

- Write this plan and Task 000 outcome.
- Verify Markdown/diff hygiene.
- Commit/push the BLK-System plan publication.

### Task 001 — RED reproduction and root cause record

- Reproduce or cite the unchanged smoke failure.
- Run a focused static RED gate that fails on Playwright `Page`-context preload API access outside `page.evaluate()`.
- Record root cause and allowed patch path.

### Task 002 — Patch exact target

- Patch only `scripts/smoke_test.ts` and, if required by the advanced smoke failure, `packages/electron/src/main/file-watcher.ts`.
- Move the preload API presence check into renderer context via Playwright string evaluation so tsx/esbuild helper functions are not serialized into the browser.
- Resolve bundled worker paths from both `dist/main` and `dist/main/chunks` without changing worker behavior.
- Keep lifecycle cleanup, timeout, and projection-result semantics unchanged.
- Commit/push Kuronode after validation and hostile audit.

### Task 003 — Validation and Kuronode closeout

- Run focused TypeScript check:

```text
npx tsc --noEmit --skipLibCheck --target ES2022 --module NodeNext --moduleResolution NodeNext --lib ES2022,DOM --types node,playwright scripts/smoke_test.ts
```

- Run Electron build if needed:

```text
npm run build -w @kuronode/electron
```

- Run:

```text
npm run test:smoke
```

- Run Kuronode MCP closeout review and record strict PASS.

### Task 004 — Hostile audit

- Verify only `scripts/smoke_test.ts` changed.
- Verify smoke test reaches `[PASS] Headless Pipeline Smoke Test Succeeded.` or record any new blocker with exact line/evidence.
- Verify no generated artifacts are staged/committed.
- Verify no BEO/RTM/coverage/drift/protected-body authority laundering.

### Task 005 — BLK-System closeout

- Write outcomes, hostile review, and sprint closeout.
- Run BLK-System verification.
- Commit/push and verify both repos are clean/synced.

---

## 5. Success Criteria

BLK-SYSTEM-077 is complete only when:

- BLK-System plan/outcomes/review/closeout are committed and pushed;
- Kuronode contains one exact patch commit derived from `3bf24938df32fb4843713a41bb2a0234e0ecf324` touching only `scripts/smoke_test.ts`;
- focused RED/GREEN evidence is recorded;
- `npm run test:smoke` passes or a newly surfaced post-preload blocker is explicitly escalated;
- Kuronode MCP closeout review passes strict mode;
- hostile audit passes;
- both repositories are clean and synced.
