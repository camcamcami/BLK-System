L2_ID: L2-K2-015
BEB_ID: BEB-K2-015
BEO_ID: BEO-K2-015
MODEL: gpt-5.5
REASONING_EFFORT: xhigh
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write
TARGET_HASH: 68a9b8c0b9b056a9c8a80d8bae32c093ade4c8e6

# L2-K2-015 — Live Read-Only Model/Projection Refresh

## Mission

Implement exactly the K2-015 live read-only model/projection refresh described by `BEB-K2-015`. Keep the change small, test-driven, deterministic, and authority-bounded. This is a bounded Projection / view slice over accepted in-memory model snapshot/model-health evidence and accepted view-intent parameters only. It is not filesystem source reading, parser process/runtime loading, provider/Agent A behavior, layout geometry/trust, saved-view persistence, renderer canvas behavior, source-coordinate truth, or canonical SysML/KerML mutation.

## Allowed files

You may modify only:

- `package.json`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`
- `src/shared/foundation.ts`
- `src/main/main.ts`
- `src/shared/projection-payload.mjs`

You may create only:

- `src/shared/model-projection-refresh.mjs`
- `tests/model-projection-refresh.test.mjs`

Do not modify docs, lockfiles, generated outputs, dependencies, parser assets, renderer UI files, preload files, workspace/project inspection files, provider modules, candidate-staging modules, parser/model-health modules, existing tests outside the allowlist, or existing K2 artifacts.

## Required TDD sequence

1. Add `tests/model-projection-refresh.test.mjs` first.
2. Run `node tests/model-projection-refresh.test.mjs` and record RED because the module/export/behavior is missing.
3. Implement `src/shared/model-projection-refresh.mjs` plus the smallest `src/shared/projection-payload.mjs` accepted-model-snapshot payload export needed to reuse existing payload bounds/sanitization.
4. Rerun `node tests/model-projection-refresh.test.mjs` to GREEN.
5. Update `package.json`, `scripts/validate-foundation.mjs`, `tests/foundation.test.mjs`, `src/shared/foundation.ts`, and `src/main/main.ts` only as needed for K2-015 static metadata, validation, and descriptor wiring.
6. Run all required verification commands.

## Implementation constraints

- Export exactly from the new module: `MODEL_PROJECTION_REFRESH_STATES`, `MODEL_PROJECTION_REFRESH_WARNING_REASONS`, `MODEL_PROJECTION_REFRESH_BOUNDS`, `MODEL_PROJECTION_REFRESH_CAPABILITY_ID`, `MODEL_PROJECTION_REFRESH_METHODS`, `refreshReadOnlyProjectionFromModelSnapshot`, `createModelProjectionRefreshViewModel`, and `createModelProjectionRefreshCapability`.
- Add one bounded snapshot payload export to `src/shared/projection-payload.mjs` such as `createProjectionPayloadFromAcceptedModelSnapshot(input)`; do not weaken `createFixtureBackedProjectionPayload(input)` or fixture-key validation.
- Build only from bounded structured accepted model snapshot, model-health evidence, and accepted view-intent parameters. Do not use caller-supplied projection functions, layout functions, parser functions, provider functions, raw graph/layout payloads, raw model/source text, diagnostic arrays, safe-mutation claims, or authority flags.
- Public output and capability objects must be frozen/deep-frozen, exact-shape, and sanitized. They must not expose raw source/model text, diagnostic arrays, raw graph/layout payloads, paths, coordinates, stack traces, prompts, credentials, provider payloads, support/export payloads, telemetry, or mutable handles.
- Public getter handles must be frozen arrow functions or otherwise have no mutable own `.prototype` surface.
- Explicit denied-authority flags must remain false for Agent A/provider behavior, filesystem source reads, parser execution/process/runtime loading, projection engine trust, graph traversal engine trust, layout engine trust, render trust, source coordinates, canonical mutation, source repair, import/promotion/adoption, saved-view persistence, save/export/session persistence, support export, telemetry, Electron IPC/preload/renderer filesystem expansion, dependency changes, RTM/`blk-link`, and BEO publication/storage/ledger.

## Required tests

Cover at least:

- same accepted model snapshot + view intent -> identical deterministic refreshed payload across two calls;
- direct accepted ready input and wrapper accepted ready input -> `ready`, bounded projection payload, read-only refresh flags, all denied authority false;
- healthy/recovered/degraded model-health evidence refreshes read-only payloads while unsafe/invalid/malformed/unknown health fails closed;
- no-anchor snapshot -> empty/degraded no-anchor warning, not ready/trusted;
- unresolved-anchor view intent -> blocked/degraded warning, not ready/trusted;
- oversized node/edge/string/payload -> truncated/circuit-breaker warning and bounded fields;
- duplicate node IDs, missing edge endpoints, non-object, missing snapshot, unknown/hostile fields, function-valued fields, hostile getters/proxies, symbol-keyed inputs, and contradictory caller authority/model-truth fields fail closed or are ignored;
- caller-supplied projection/layout/parser/provider/model-health functions are not invoked;
- raw marker strings in source/model/path/credential/provider/diagnostic/parser/graph/layout fields do not leak;
- public result/capability shape is exact and frozen/deep-frozen;
- no network/env/filesystem/process/package-manager access;
- K2-013 fixture-backed payload compatibility continues to pass and the new snapshot payload builder does not weaken fixture-key validation.

## Verification commands

Run and leave exact output evidence:

```bash
node tests/model-projection-refresh.test.mjs
node tests/projection-payload.test.mjs
node scripts/validate-foundation.mjs
npm test
npm run build
npm run typecheck
git diff --check -- package.json scripts/validate-foundation.mjs tests/foundation.test.mjs src/shared/foundation.ts src/main/main.ts src/shared/projection-payload.mjs src/shared/model-projection-refresh.mjs tests/model-projection-refresh.test.mjs
```

## Final response requirements to BLK-System

Report RED command and expected failure, GREEN focused test output, full verification outputs, final changed file list, exact feature commit hash, denied-authority summary, hostile-review verdict or blockers, and residual blockers/watch items.

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
