L2_ID: L2-K2-017
BEB_ID: BEB-K2-017
BEO_ID: BEO-K2-017
MODEL: gpt-5.5
REASONING_EFFORT: xhigh
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write
TARGET_HASH: 747846ce741ec586b76b8a5edd7b96c25001cc58

# L2-K2-017 — Bounded Read-Only Projection Panel

## Mission

Implement exactly the K2-017 bounded read-only projection panel described by `BEB-K2-017`. Keep the change small, test-driven, deterministic, and authority-bounded. The only product-facing delta is that `src/renderer/App.tsx` exposes a panel-shaped, non-canvas, read-only projection presentation derived from the existing K2-016 `projectionInspection` / K2-015 projection refresh seam. Do not implement canvas rendering, layout computation/trust, saved-view persistence, filesystem reads, parser/runtime expansion, provider/Agent A behavior, candidate import/promotion, import/export, source repair, or canonical SysML/KerML mutation.

## Allowed files

You may modify only:

- `package.json`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`
- `src/shared/foundation.ts`
- `src/renderer/App.tsx`
- `src/renderer/styles.css`

You may create only:

- `tests/renderer-projection-panel.test.mjs`

Do not modify docs, lockfiles, generated outputs, dependencies, parser assets, `src/main/main.ts`, `src/preload/preload.ts`, shared projection/refresh implementation modules, provider/workspace/parser/model-health modules, candidate-staging modules, existing focused tests outside the allowlist, or existing K2 artifacts.

## Required TDD sequence

1. Add `tests/renderer-projection-panel.test.mjs` first.
2. Run `node tests/renderer-projection-panel.test.mjs` and record RED because K2-017 projection panel data is missing from the current target.
3. Implement only the minimum App/view-model, optional stylesheet, validator/package, and foundation metadata changes required for GREEN.
4. Rerun `node tests/renderer-projection-panel.test.mjs` to GREEN.
5. Run all verification commands below and capture exact outputs.

## Implementation constraints

- In `src/renderer/App.tsx`, derive the panel from existing `appViewModel.projectionInspection` or from the same already-sanitized K2-016 inspection construction path. Do not create a second graph/projection/layout engine.
- Expose a renderer-visible panel entry with exact, testable summary fields: panel ID/title, read-only state/status text, source capability ID, warning/degraded reasons, payload counts, bounded sanitized visible node/edge rows, and explicit denied-authority indicators.
- Keep public panel objects frozen/deep-frozen; tests must fail if exposed panel metadata can be mutated.
- Keep every denied-authority indicator false/unauthorized. Do not introduce IPC/preload expansion, filesystem/source reads, parser execution, provider calls, graph/layout/canvas trust, source coordinates, canonical mutation, source repair, import/adoption/promotion, saved-view persistence, save/export/session persistence, support export, telemetry, dependency changes, RTM/`blk-link`, or BEO publication/storage/ledger.
- Do not duplicate or weaken K2-015/K2-016 sanitization logic. Copy only bounded/sanitized fields from the inspection into the panel model.
- If stylesheet changes are made, keep them inert presentation-only CSS; no generated assets, network fonts, external imports, or hidden authority wording.
- Update `scripts/validate-foundation.mjs` so K2-017 is required, `tests/renderer-projection-panel.test.mjs` is part of required files and `npm test`, and forbidden raw authority/source fields remain blocked.
- Update `tests/foundation.test.mjs` and `src/shared/foundation.ts` for K2-017 metadata only.

## Required tests

Cover at least:

- current target RED for missing K2-017 projection panel in App;
- deterministic `appViewModel.projectionPanel` shape and exact approved keys;
- source capability ID `model-projection-refresh` visible;
- panel state, warnings, and payload counts match `appViewModel.projectionInspection`;
- visible sanitized node/edge summaries are bounded and free of raw source/model/path/provider/diagnostic/credential/telemetry markers;
- all denied-authority indicators are present and false/unauthorized;
- read-only/bounded/trusted flags remain correct (`readOnly` true, `bounded` true, `trusted` false unless inherited inspection truth changes);
- panel object is frozen/deep-frozen and no mutable function/prototype/DOM handle is exposed in `appViewModel`;
- renderer executable text does not introduce canvas/layout/ELK/JointJS/saved-view/localStorage/sessionStorage/fetch/provider/import/export/canonical-mutation behavior except explicit denied labels;
- package scripts include the K2-017 test and no dependency fields.

## Verification commands

```bash
node tests/renderer-projection-panel.test.mjs
node tests/renderer-projection-inspection.test.mjs
node tests/model-projection-refresh.test.mjs
node scripts/validate-foundation.mjs
npm test
npm run build
npm run typecheck
git diff --check -- package.json scripts/validate-foundation.mjs tests/foundation.test.mjs src/shared/foundation.ts src/renderer/App.tsx src/renderer/styles.css tests/renderer-projection-panel.test.mjs
```

## Final response requirements to BLK-System

Report the RED command and expected failure excerpt, GREEN focused test output, full verification outputs, final changed file list, exact feature commit hash, denied-authority summary, hostile-review verdict or blockers, and residual blockers/watch items. If BLK-pipe route execution times out or fails due to environment/tooling, preserve the exact approved allowlist/target hash and report whether a supervised Codex fallback or clean-worktree retarget was used.

## Adversarial readiness card

Slice: K2-017 — Bounded read-only projection panel
Milestone: D — First read-only useful projection
Compartment: Projection / view
One authority boundary: renderer-visible non-canvas presentation of already-sanitized projection inspection data.
Direct requirements: REQ-KN-081, REQ-KN-082, REQ-KN-083.
Supporting-only requirements: REQ-KN-039, REQ-KN-040, REQ-KN-041, REQ-KN-042, REQ-KN-048, REQ-KN-077, REQ-KN-080, REQ-KN-084, REQ-KN-107.
Explicitly denied capabilities: canvas rendering, ELK/JointJS/layout engine trust, saved-view persistence, filesystem source reads, parser-runtime expansion, Agent A/provider behavior, candidate staging/import/promotion, import/export, canonical SysML/KerML mutation, RTM generation, production `blk-link`, and BEO publication/signing/storage/ledger.
Malformed input behavior: K2-017 must not accept caller-supplied graph/source/provider/input objects; if panel construction receives missing or malformed inspection evidence, it must degrade to bounded empty/fail-closed panel state rather than executing callbacks, reading files, or trusting raw fields.
Contradictory input behavior: any state where panel readiness/visibility says ready while underlying projection inspection flags are degraded, stale, untrusted, or denied must expose the stricter degraded/untrusted state or fail closed.
Spoofing seams to forbid: raw source/model/path/provider/diagnostic/credential/telemetry fields, function/getter/proxy/callable panel inputs, mutable public handles, prototype pollution, layout/canvas claims, saved-view claims, filesystem claims, provider/Agent A claims, import/promotion/canonical-mutation claims.
Raw/leaky fields to forbid: `raw`, `source`, `sourceText`, `modelText`, `path`, `provider`, `prompt`, `credential`, `token`, `diagnostic`, `telemetry`, `parser`, `canonical`, `mutation`, `layoutCoordinates`, `canvas`, `elk`, `jointjs`, `save`, `export`, `rtm`, `blk-link`, `beoPublication`.
Required hostile probes: frozen/deep-frozen public panel; exact allowed panel field set; no raw/leaky fragments in node/edge/detail rows; all denied-authority indicators visible and false; bounded visible node/edge/detail counts; no callable/prototype/mutable handles exposed; no canvas/layout/saved-view/localStorage/sessionStorage/fetch/provider/import/export dependencies; stale/degraded/empty/warning states remain visible; package and validator gates include the focused test and new K2-017 governed files.
Closeout docs/mirrors to update: canonical `BEO-K2-017`, `docs/roadmaps/K2_implementation-roadmap.md`, `docs/traceability/K2_traceability.yaml`, and view-only Obsidian BEB/BEO mirrors after final commit.

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

