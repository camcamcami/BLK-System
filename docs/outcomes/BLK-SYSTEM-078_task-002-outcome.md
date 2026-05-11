# BLK-SYSTEM-078 Task 002 Outcome — Kuronode Exact-Target Patch

**Status:** Complete
**Date:** 2026-05-11

## Kuronode Patch Scope

Modified exact allowlist only:

```text
packages/electron/src/main/ipc-handlers.ts
packages/electron/src/preload/index.ts
scripts/smoke_test.ts
```

## Changes

1. Added main-process IPC handler:

```text
kur:user-data-path -> app.getPath('userData')
```

2. Added preload bridge method:

```text
getUserDataPath: () => ipcRenderer.invoke('kur:user-data-path')
```

3. Updated `scripts/smoke_test.ts` to:
   - preserve string-based renderer evaluation for `window.KuronodeAPI`;
   - retrieve Electron `userData` at runtime;
   - copy `models/Kuronode.sysml` to `<userData>/model.sysml` before `intentTrigger`;
   - preserve timeout failure, projection result shape validation, and listener cleanup.

## GREEN Static Gate

```text
PASS: ipc handler exposes userData path
PASS: preload exposes getUserDataPath
PASS: smoke calls getUserDataPath
PASS: smoke writes runtime model.sysml
PASS: smoke uses string eval for KuronodeAPI
PASS: smoke seeds before intentTrigger
DETERMINISTIC_SEED_GATE_OK
```

## Focused Validation

```text
npx tsc --noEmit --skipLibCheck --esModuleInterop --target ES2022 --module NodeNext --moduleResolution NodeNext --lib ES2022,DOM --types node,playwright scripts/smoke_test.ts
# exit 0

git diff --check -- scripts/smoke_test.ts packages/electron/src/main/ipc-handlers.ts packages/electron/src/preload/index.ts
# exit 0
```

## Authority Boundary

No package manifests, lockfiles, generated artifacts, parser code, layout worker code, renderer feature code, BLK-test MCP, BEO publication, RTM generation, or protected BLK-req body access were changed or authorized.
