# BLK-SYSTEM-077 Hostile Review — Kuronode Preload API Smoke Context Fix

**Status:** PASS
**Date:** 2026-05-11
**Reviewer:** Hermes hostile audit plus delegated adversarial audit

---

## Audit Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| Exact target | PASS | Parent target `3bf24938df32fb4843713a41bb2a0234e0ecf324` preserved before patch. |
| Commit identity | PASS | Kuronode commit `80e75e3 test: fix headless smoke renderer context`. |
| File allowlist | PASS | Only `scripts/smoke_test.ts` and `packages/electron/src/main/file-watcher.ts` changed. |
| Plan amendment before widened scope | PASS | BLK-System commit `305c0d5` amended plan authority before file-watcher mutation. |
| RED/GREEN evidence | PASS | RED preload missing; RED `__name`; RED worker path; GREEN smoke PASS. |
| Electron security | PASS | No `BrowserWindow` security options, CSP, preload exposure, `nodeIntegration`, or `contextIsolation` weakening. |
| Generated artifacts | PASS | `dist/` and `node_modules/` remain ignored/uncommitted; no package/lock changes. |
| Validation | PASS | Focused static, TypeScript, Electron build, worker unit test, smoke test all passed. |
| Kuronode closeout | PASS | MCP strict closeout PASS and `closeoutComplete: true`. |
| Forbidden authority | PASS | No Codex, production BLK-test MCP, BEO publication, RTM generation, protected-body read, coverage/drift claim, or source mutation outside allowlist. |

---

## Hostile Findings and Disposition

### Finding 1 — Page object vs renderer window

**Risk:** A smoke script can falsely claim preload API absence by reading the wrong object.

**Disposition:** Fixed by moving the check into renderer context with Playwright evaluation.

### Finding 2 — `tsx`/esbuild function serialization

**Risk:** Playwright callback functions serialized by `tsx` can carry helper references such as `__name` that do not exist in the browser context.

**Disposition:** Fixed by using string evaluation for simple renderer-side smoke interactions.

### Finding 3 — Bundled worker path from chunk directory

**Risk:** Worker paths based on bundled chunk `MODULE_DIR` point to `dist/main/chunks/workers` while electron-vite emits workers to `dist/main/workers`.

**Disposition:** Fixed by resolving both `MODULE_DIR/workers` and `MODULE_DIR/../workers`.

---

## Final Disposition

PASS. BLK-SYSTEM-077 is safe to close. The Kuronode headless smoke test now reaches `[PASS] Headless Pipeline Smoke Test Succeeded.`
