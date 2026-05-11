# BLK-SYSTEM-078 Sprint Closeout — Kuronode Deterministic Smoke Seed and CEB_009 Closeout

**Status:** Complete
**Date:** 2026-05-11

---

## Executive Summary

BLK-SYSTEM-078 made the Kuronode headless smoke test deterministic after the BLK-SYSTEM-077 smoke baseline passed.

The smoke harness now obtains Electron `userData` through the preload API and copies `models/Kuronode.sysml` to `<userData>/model.sysml` before triggering the projection pipeline. This removes hidden dependency on persistent local userData from prior smoke runs.

Kuronode patch commit:

```text
aebea51bed911c781a537d84d38b2dcb838b1368 test: seed smoke model deterministically
```

BLK-System plan commit:

```text
db61f472338aa4e4b1420e89d430e980ef509057 docs: plan blk-system 078 deterministic smoke seed
```

---

## Completed Tasks

| Task | Status | Evidence |
| --- | --- | --- |
| Task 000 — Plan publication | Complete | Plan and task-000 outcome committed/pushed in BLK-System. |
| Task 001 — RED deterministic-seed reproduction | Complete | Static gate failed on missing `kur:user-data-path`, `getUserDataPath`, smoke seed call, and runtime model write. |
| Task 002 — Exact-target Kuronode patch | Complete | Three source files patched; static seed gate and focused TypeScript check passed. |
| Task 003 — Validation and Kuronode closeout | Complete | Build, worker unit, smoke, strict MCP closeout, `CEO_009`, and Kuronode push complete. |
| Task 004 — Hostile audit and BLK-System closeout | Complete | Hostile review PASS; BLK-System Python and Go suites pass. |

---

## Kuronode Files Changed

```text
docs/execution briefs/CEB_009.md
docs/execution briefs/CEO_009_Codex_Execution_Outcome.md
packages/electron/src/main/ipc-handlers.ts
packages/electron/src/preload/index.ts
scripts/smoke_test.ts
```

---

## Validation Summary

Kuronode:

```text
DETERMINISTIC_SEED_GATE_OK
npx tsc --noEmit --skipLibCheck --esModuleInterop --target ES2022 --module NodeNext --moduleResolution NodeNext --lib ES2022,DOM --types node,playwright scripts/smoke_test.ts
npm run build -w @kuronode/electron
npm run test:worker -w @kuronode/electron
npm run test:smoke
Kuronode MCP closeout: PASS / strict / closeoutComplete true
Hostile audit: PASS
```

Smoke PASS evidence:

```text
[SMOKE] Seeded canonical model: /home/dad/.config/@kuronode/electron/model.sysml
[SMOKE] Received projection result: 3cbc1378-6581-40c7-a8a7-773bc74596c9
[PASS] Headless Pipeline Smoke Test Succeeded.
```

BLK-System:

```text
BLK_DOC_FENCE_CHECK_OK
git diff --check -- docs/outcomes/BLK-SYSTEM-078_task-001-outcome.md docs/outcomes/BLK-SYSTEM-078_task-002-outcome.md docs/outcomes/BLK-SYSTEM-078_task-003-outcome.md
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
# Ran 783 tests in 11.447s — OK

go test ./...
# all packages OK
```

---

## Kuronode Closeout Traceability

```text
Requirement: OKR_009
Use case: UCR-003
New requirements: none
New use cases: none
Closeout: PASS, strict, closeoutComplete true
```

---

## Authority and Non-Authority

Authorized and executed:

- exact-target deterministic smoke seed patch;
- one read-only IPC query for Electron `userData` path;
- smoke validation, worker validation, and build validation;
- CEB_009 / CEO_009 documentation reconciliation.

Not authorized and not performed:

- package manifest or lockfile changes;
- generated artifact commits;
- parser, layout worker, graph, renderer feature, or store refactors;
- production/generic BLK-test MCP;
- live Codex dispatch;
- BEO publication or runtime `PUBLISHED` output;
- RTM generation or drift rejection;
- protected BLK-req body read/copy/parse/hash/scan/mutation;
- coverage matrix or coverage-claim promotion;
- production sandbox or host-secret isolation claim.

---

## Remaining Work

The smoke harness is now deterministic and passing at Kuronode `aebea51`. The next logical Kuronode product work can proceed from a cleaner headless validation baseline.
