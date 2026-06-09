L2_ID: L2-K2-016
BEB_ID: BEB-K2-016
BEO_ID: BEO-K2-016
MODEL: gpt-5.5
REASONING_EFFORT: xhigh
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write
TARGET_HASH: 78361d71d78b543c444664dc2242eec80d8c1b38

# L2-K2-016 — Renderer-Visible Read-Only Projection Inspection

## Mission

Implement exactly the K2-016 renderer-visible read-only projection inspection described by `BEB-K2-016`. Keep the change small, test-driven, deterministic, and authority-bounded. The only product-facing delta is that `src/renderer/App.tsx` exposes an inspectable read-only projection refresh summary derived from the existing K2-015 shared refresh capability. Do not implement canvas rendering, layout computation/trust, saved-view persistence, filesystem reads, parser/runtime execution, provider/Agent A behavior, import/export, source repair, or canonical SysML/KerML mutation.

## Allowed files

You may modify only:

- `package.json`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`
- `src/shared/foundation.ts`
- `src/renderer/App.tsx`

You may create only:

- `tests/renderer-projection-inspection.test.mjs`

Do not modify docs, lockfiles, generated outputs, dependencies, parser assets, `src/main/main.ts`, `src/preload/preload.ts`, shared projection/refresh implementation modules, provider/workspace/parser/model-health modules, existing focused tests outside the allowlist, or existing K2 artifacts.

## Required TDD sequence

1. Add `tests/renderer-projection-inspection.test.mjs` first.
2. Run `node tests/renderer-projection-inspection.test.mjs` and record RED because `appViewModel.projectionInspection` / K2-016 renderer inspection is missing from the current target.
3. Implement only the minimum App/view-model and validator/package metadata changes required for GREEN.
4. Rerun `node tests/renderer-projection-inspection.test.mjs` to GREEN.
5. Run all verification commands below and capture exact outputs.

## Implementation constraints

- In `src/renderer/App.tsx`, import and use the existing K2-015 `MODEL_PROJECTION_REFRESH_CAPABILITY_ID` and `createModelProjectionRefreshCapability` (or the existing K2-015 view-model helper) to derive the inspection from one bounded module-owned accepted in-memory model snapshot.
- Expose a renderer-visible inspection entry on `appViewModel` with exact, testable summary fields: capability ID, method names, refresh state, warning reasons, payload counts, sanitized visible node/edge summaries if present, readiness/read-only/bounded/trusted flags, and denied-authority flags.
- Keep public inspection objects frozen/deep-frozen; tests must fail if exposed metadata can be mutated.
- Keep every denied-authority flag false. Do not introduce IPC/preload expansion, filesystem/source reads, parser execution, provider calls, graph/layout engine trust, canvas render trust, source coordinates, canonical mutation, source repair, import/adoption, saved-view persistence, save/export/session persistence, support export, telemetry, dependency changes, RTM/`blk-link`, or BEO publication/storage/ledger.
- Do not duplicate or weaken K2-015 sanitization logic. Derive from `getModelProjectionRefresh()` and copy only bounded/sanitized fields into the renderer inspection summary.
- Update `scripts/validate-foundation.mjs` so K2-016 is required, `tests/renderer-projection-inspection.test.mjs` is part of required files and `npm test`, the K2-015 helper vocabulary remains confined except for the intentional `src/renderer/App.tsx` K2-016 use, and forbidden raw authority/source fields remain blocked.
- Update `tests/foundation.test.mjs` and `src/shared/foundation.ts` for K2-016 metadata only.

## Required tests

Cover at least:

- current target RED for missing K2-016 projection inspection in App;
- deterministic `appViewModel.projectionInspection` shape and exact keys;
- capability ID `model-projection-refresh` and method metadata visible;
- state, warnings, and payload counts visible and matching the K2-015 refresh result;
- visible sanitized node/edge summaries bounded and free of raw source/model/path/provider/diagnostic/credential/telemetry markers;
- all denied-authority flags false;
- read-only/bounded/trusted flags correct (`readOnlyModelProjectionRefresh` true, `boundedModelProjectionRefresh` true, `modelProjectionRefreshTrusted` false);
- inspection object frozen/deep-frozen and no mutable function/prototype handle exposed in `appViewModel`;
- validator rejects K2-015 helper-vocabulary use outside owning modules/tests and the intentional `src/renderer/App.tsx` K2-016 path;
- package scripts include the K2-016 test and no dependency fields.

## Verification commands

```bash
node tests/renderer-projection-inspection.test.mjs
node tests/model-projection-refresh.test.mjs
node tests/projection-payload.test.mjs
node scripts/validate-foundation.mjs
npm test
npm run build
npm run typecheck
git diff --check -- package.json scripts/validate-foundation.mjs tests/foundation.test.mjs src/shared/foundation.ts src/renderer/App.tsx tests/renderer-projection-inspection.test.mjs
```

## Final response requirements to BLK-System

Report the RED command and expected failure excerpt, GREEN focused test output, full verification outputs, final changed file list, exact feature commit hash, denied-authority summary, hostile-review verdict or blockers, and residual blockers/watch items. If BLK-pipe route execution times out or fails due to environment/tooling, preserve the exact approved allowlist/target hash and report whether a supervised Codex fallback or clean-worktree retarget was used.

## Readiness profile probe card

These probes are required pre-dispatch checklist evidence only. They do not authorize source/Git mutation, parser execution, provider/runtime dispatch, BEO publication, RTM generation, or reusable BLK-pipe/Codex authority beyond the exact approved drop.

### kuronode-caller-object-control-plane-v1

- [ ] KCP-001 direct accepted ready input
- [ ] KCP-002 wrapper accepted ready input
- [ ] KCP-003 top-level denied raw/authority/source/provider/parser/import/export/mutation fail closed
- [ ] KCP-004 nested denied raw/authority/source/provider/parser/import/export/mutation fail closed
- [ ] KCP-005 raw marker values fail closed and do not serialize back out
- [ ] KCP-006 duplicate filters or entries beyond cap fail closed
- [ ] KCP-007 proxy/getter/callable/symbol inputs fail closed without invoking caller code
- [ ] KCP-008 public capability/result objects deeply frozen and public getters have no mutable prototype
- [ ] KCP-009 helper vocabulary confined to owning module/tests
- [ ] KCP-010 downstream compatibility probe for the paired payload/capability surface
- [ ] KCP-011 deep hostile object graph hits a bounded circuit breaker without throwing
- [ ] KCP-012 caller authority/status/trust laundering fields force fail-closed false readiness
