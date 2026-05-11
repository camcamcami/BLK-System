# BLK-SYSTEM-077 Task 001 Outcome — RED Reproduction and Root Cause

**Status:** Complete
**Date:** 2026-05-11

---

## RED Evidence

Focused static RED gate failed before patch:

```text
RED_PRELOAD_CONTEXT_FAIL: smoke script checks KuronodeAPI on Playwright Page object instead of renderer window
```

Runtime RED reproduced the BLK-SYSTEM-076 blocker at exact target `3bf24938df32fb4843713a41bb2a0234e0ecf324`:

```text
npm run test:smoke
[SMOKE] Launching Electron...
[SMOKE] Window captured. Waiting for renderer bootstrap (#root)...
[FAIL] Smoke test failed: Error: Kuronode preload API missing
    at <anonymous> (/home/dad/code/Kuronode-v1/scripts/smoke_test.ts:41:13)
```

---

## Root Cause

The smoke script used the Playwright `Page` object named `window` as if it were the renderer DOM `window`:

```text
const kuronodeApi = (window as Window & { KuronodeAPI?: KuronodeSmokeApi }).KuronodeAPI;
```

That check always reads from the Node-side Playwright page wrapper, not from the renderer context where `contextBridge.exposeInMainWorld('KuronodeAPI', ...)` installs the API.

---

## Secondary RED Evidence After First Fix

After moving the preload check into renderer context, smoke advanced and exposed a function-serialization issue:

```text
page.evaluate: ReferenceError: __name is not defined
```

Root cause: `tsx`/esbuild serialized helper-wrapped callback functions into Playwright `page.evaluate()`. BLK-SYSTEM-077 therefore converted smoke-script renderer interactions to string evaluation.

After that fix, smoke advanced further and exposed a bundled worker path issue:

```text
Cannot find module '/home/dad/code/Kuronode-v1/packages/electron/dist/main/chunks/workers/parser.worker.js'
```

Root cause: `file-watcher.ts` was bundled into `dist/main/chunks`, so `MODULE_DIR/workers/parser.worker.js` resolved under `chunks/workers` while electron-vite emits workers under `dist/main/workers`.

---

## Authorized Patch Paths

The committed plan amendment authorized exactly:

```text
scripts/smoke_test.ts
packages/electron/src/main/file-watcher.ts
```
