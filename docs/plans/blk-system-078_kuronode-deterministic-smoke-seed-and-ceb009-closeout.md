# BLK-SYSTEM-078 — Kuronode Deterministic Smoke Seed and CEB_009 Closeout Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, `kuronode-headless-smoke-test`, and AAA_001/Kuronode closeout procedures while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first for maturity vocabulary, then by active roadmap `docs/BLK-059_blk-system-post-058-roadmap.md`, and by BLK-001 through BLK-006 as applicable.

**Goal:** Remove the remaining hidden-state dependency in Kuronode's headless smoke test by seeding a canonical SysML model into Electron `userData` at runtime, then close the historical `CEB_009` smoke-fix execution record.
**BLK-024 / BLK-059 track:** BLK-024 Track D/C validation hardening and BLK-059 Workstream B Kuronode tactical quality; maturity L1/L2 local deterministic validation fixture/profile behavior, not new runtime authority.
**Architecture:** BLK-SYSTEM-076/077 made the headless smoke path pass, but live inspection shows `scripts/smoke_test.ts` still relies on whatever `model.sysml` happens to exist in Electron `userData`. The next logical sprint is the smallest follow-up that makes the smoke test self-contained and reconciles it with the existing `CEB_009` CA-2/CA-3 closeout contract.
**Tech Stack:** TypeScript, Electron preload/main IPC, Playwright Electron smoke test, Markdown outcome docs.
**Authority boundary:** Exact-target Kuronode patch plus documentation closeout only. No production BLK-test MCP, no live Codex dispatch, no BEO publication, no RTM generation, no protected-vault body access, no package-manager changes, and no source mutation outside exact allowlists.

---

## 0. Current Known State

Captured: `2026-05-11T16:34:24+10:00`

### BLK-System

```text
repo: /home/dad/BLK-System
branch: main
local HEAD: 71ae77067516ee267cd2c32c8aa26eb5fc4b8204
remote main: 71ae77067516ee267cd2c32c8aa26eb5fc4b8204
status: ## main...origin/main
last commit: 71ae770 docs: close out blk-system 077 smoke fix
```

### Kuronode

```text
repo: /home/dad/code/Kuronode-v1
branch: main
local HEAD: 80e75e3b4f26c4654f00a703a83c00c8cb76e4cd
remote main: 80e75e3b4f26c4654f00a703a83c00c8cb76e4cd
status: ## main...origin/main
last commit: 80e75e3 test: fix headless smoke renderer context
```

---

## 1. Selection Rationale

The previous sprint closed the preload API and bundled worker path blockers and produced a passing smoke result. However, the old `CEB_009` corrective action CA-2 required the smoke test to seed canonical SysML into `<userData>/model.sysml` before triggering the pipeline. Current code still reads `userData/model.sysml` in `ipc-handlers.ts`, but the smoke test does not deterministically create it.

This means the pass can depend on persistent local userData from prior runs. That is the next logical quality blocker because it undermines the smoke test as clean-room evidence.

---

## 2. Governing Alignment

| Document | Relevance | Preserved boundary |
| --- | --- | --- |
| BLK-001 | Separates planning/audit, bounded source mutation, and verification evidence. | Hermes plans/audits; Kuronode patch remains exact-path; smoke evidence does not become publication/RTM authority. |
| BLK-002 | Protected requirements lifecycle. | No active/staging/protected BLK-req body reads or writes. |
| BLK-003 | Orchestration and hostile-audit doctrine. | Exact allowlist, validation commands, hostile audit, and failure closeout are required. |
| BLK-004 | BLK-pipe/validation profile authority. | No arbitrary broad validation shell as reusable authority; this sprint runs trusted-local exact commands only. |
| BLK-005 | Traceability and artifact binding doctrine. | Outcome docs bind to exact commits and observed validation evidence without claiming RTM closure. |
| BLK-006 | Protected vault hard-deny. | No BLK-req vault access or tactical mutation of protected docs. |
| BLK-059 | Current roadmap. | Advances Kuronode tactical quality/mechanical validation; does not activate BEO publication, RTM, Codex live dispatch, or production BLK-test MCP. |
| CEB_009 | Historical Kuronode smoke corrective action. | Completes deterministic runtime seed and result-shape evidence while recording `CEO_009`. |

---

## 3. Exact Scope

### Kuronode source/doc allowlist

Source files:

1. `scripts/smoke_test.ts`
2. `packages/electron/src/main/ipc-handlers.ts`
3. `packages/electron/src/preload/index.ts`

Documentation files:

4. `docs/execution briefs/CEB_009.md` — status-only reconciliation if needed.
5. `docs/execution briefs/CEO_009_Codex_Execution_Outcome.md` — required closeout/outcome record.

### BLK-System docs allowlist

1. `docs/plans/blk-system-078_kuronode-deterministic-smoke-seed-and-ceb009-closeout.md`
2. `docs/outcomes/BLK-SYSTEM-078_task-000-outcome.md`
3. `docs/outcomes/BLK-SYSTEM-078_task-001-outcome.md`
4. `docs/outcomes/BLK-SYSTEM-078_task-002-outcome.md`
5. `docs/outcomes/BLK-SYSTEM-078_task-003-outcome.md`
6. `docs/reviews/BLK-SYSTEM-078_hostile-review.md`
7. `docs/outcomes/BLK-SYSTEM-078_sprint-closeout.md`

### Explicitly forbidden

- Package manifest or lockfile edits.
- Generated build artifacts or `node_modules` commits.
- Parser, layout worker, renderer feature, store, or graph refactors.
- New Electron IPC channels except `kur:user-data-path`.
- Arbitrary filesystem exposure through preload beyond returning Electron's `app.getPath('userData')` for the smoke harness.
- Production/generic BLK-test MCP, live Codex dispatch, BEO publication, runtime `PUBLISHED` output, RTM generation, drift rejection, coverage claim promotion, protected BLK-req body reads/copying/parsing/hashing/scanning/mutation, or production sandbox claims.

---

## 4. Required Implementation Contract

1. Main process must register:

```typescript
ipcMain.handle('kur:user-data-path', () => app.getPath('userData'));
```

2. Preload bridge must expose:

```typescript
getUserDataPath: () => ipcRenderer.invoke('kur:user-data-path'),
```

3. Smoke test must, after `#root` bootstrap and before `intentTrigger`:
   - call `window.KuronodeAPI.getUserDataPath()` using Playwright string evaluation;
   - read a canonical in-repo SysML seed (prefer `models/Kuronode.sysml`, the currently verified smoke model);
   - create the returned directory if needed;
   - write `<userData>/model.sysml`;
   - then start the projection listener and trigger `intentTrigger`.

4. Smoke test must preserve the BLK-SYSTEM-077 fixes:
   - string-based renderer evaluation for `window.KuronodeAPI`;
   - timeout failure is an actual failure;
   - projection result must have a non-timeout `streamId` and `ast` payload;
   - listener cleanup remains present.

---

## 5. Task Plan

### Task 000 — Plan publication

- Write this plan.
- Write `docs/outcomes/BLK-SYSTEM-078_task-000-outcome.md`.
- Verify markdown fences and `git diff --check` for exact paths.
- Commit and push BLK-System plan publication.

### Task 001 — RED deterministic-seed reproduction

- Prove current Kuronode HEAD lacks deterministic userData seeding.
- RED gate must fail before implementation by checking for:
  - `kur:user-data-path` handler,
  - `getUserDataPath` preload bridge,
  - smoke-side runtime seed write to `model.sysml`,
  - preservation of string-based Playwright evaluation.
- Record evidence in `docs/outcomes/BLK-SYSTEM-078_task-001-outcome.md`.

### Task 002 — Patch Kuronode exact target

- Mutate only the three source allowlist files.
- Add the minimal userData path IPC and preload method.
- Add deterministic smoke seeding before `intentTrigger`.
- Run focused TypeScript validation.
- Record evidence in `docs/outcomes/BLK-SYSTEM-078_task-002-outcome.md`.

### Task 003 — Full validation and Kuronode closeout

- Run:
  - static deterministic seed gate,
  - `git diff --check -- <allowlist>` in Kuronode,
  - focused smoke-script TypeScript check,
  - `npm run build -w @kuronode/electron`,
  - `npm run test:worker -w @kuronode/electron`,
  - `npm run test:smoke`.
- Run strict Kuronode closeout review.
- Write `CEO_009_Codex_Execution_Outcome.md` and reconcile `CEB_009` status if needed.
- Commit and push Kuronode exact-path changes.
- Record BLK-System task outcome.

### Task 004 — Hostile audit and BLK-System closeout

- Audit file boundaries, forbidden authority, CEB_009/CEO_009 reconciliation, and validation evidence.
- Run BLK-System verification:
  - `git diff --check` for exact BLK-System docs,
  - Python unittest suite with safe pycache controls,
  - Go tests.
- Write `docs/reviews/BLK-SYSTEM-078_hostile-review.md` and final closeout.
- Commit and push BLK-System closeout.

---

## 6. Definition of Done

- BLK-System plan and all outcome/review/closeout docs are committed and pushed.
- Kuronode source mutation is confined to the exact allowlist.
- Headless smoke creates/overwrites `<userData>/model.sysml` from a canonical repo seed during the test run.
- Smoke passes from the patched code and logs a real projection result.
- Kuronode MCP closeout is strict PASS or an explicitly documented blocker.
- `CEO_009` exists and records the execution outcome.
- No forbidden authority was granted or implied.
