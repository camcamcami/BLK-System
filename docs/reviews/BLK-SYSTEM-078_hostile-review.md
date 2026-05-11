# BLK-SYSTEM-078 Hostile Review — Kuronode Deterministic Smoke Seed

**Status:** PASS
**Date:** 2026-05-11

## Reviewed Scope

Kuronode commit reviewed:

```text
aebea51bed911c781a537d84d38b2dcb838b1368 test: seed smoke model deterministically
```

BLK-System sprint docs reviewed:

```text
docs/plans/blk-system-078_kuronode-deterministic-smoke-seed-and-ceb009-closeout.md
docs/outcomes/BLK-SYSTEM-078_task-000-outcome.md
docs/outcomes/BLK-SYSTEM-078_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-078_task-002-outcome.md
docs/outcomes/BLK-SYSTEM-078_task-003-outcome.md
```

## Findings

| Gate | Verdict | Evidence |
| --- | --- | --- |
| File boundary | PASS | Kuronode changed only `scripts/smoke_test.ts`, `packages/electron/src/main/ipc-handlers.ts`, `packages/electron/src/preload/index.ts`, `docs/execution briefs/CEB_009.md`, and `docs/execution briefs/CEO_009_Codex_Execution_Outcome.md`. |
| Forbidden source surfaces | PASS | No package manifests, lockfiles, generated artifacts, parser, layout worker, graph, renderer feature, or store refactors were changed. |
| IPC exposure | PASS | New handler accepts no renderer-controlled path/input and returns only `app.getPath('userData')`. |
| Preload exposure | PASS | New bridge method exposes only `getUserDataPath`; existing broad `readFile`/`writeFile` surfaces were pre-existing and not expanded. |
| Smoke determinism | PASS | Smoke seeds `models/Kuronode.sysml` to `<userData>/model.sysml` before `intentTrigger`. |
| BLK-SYSTEM-077 regression guard | PASS | String-based Playwright evaluation, timeout failure, `streamId`/`ast` checks, and listener cleanup remain present. |
| CEB_009 closeout | PASS | `CEB_009` status reconciled and `CEO_009_Codex_Execution_Outcome.md` created with validation and authority boundaries. |
| Kuronode closeout | PASS | Strict MCP closeout passed for `OKR_009` / `UCR-003`; no new requirements or use cases. |
| BLK-System authority boundary | PASS | No production BLK-test MCP, live Codex dispatch, BEO publication, RTM generation, coverage claim promotion, protected BLK-req body access, or production sandbox claim was granted. |

## Validation Reviewed

```text
DETERMINISTIC_SEED_GATE_OK
npx tsc --noEmit --skipLibCheck --esModuleInterop --target ES2022 --module NodeNext --moduleResolution NodeNext --lib ES2022,DOM --types node,playwright scripts/smoke_test.ts
npm run build -w @kuronode/electron
npm run test:worker -w @kuronode/electron
npm run test:smoke
BLK-System Python unittest: 783 tests OK
BLK-System Go tests: all packages OK
```

Smoke evidence:

```text
[SMOKE] Seeded canonical model: /home/dad/.config/@kuronode/electron/model.sysml
[SMOKE] Received projection result: 3cbc1378-6581-40c7-a8a7-773bc74596c9
[PASS] Headless Pipeline Smoke Test Succeeded.
```

## Disposition

PASS. The sprint closes the hidden userData dependency without broadening runtime authority.
