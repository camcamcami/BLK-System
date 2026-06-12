L2_ID: L2-K2-020
BEB_ID: BEB-K2-020
BEO_ID: BEO-K2-020
MODEL: gpt-5.5
REASONING_EFFORT: xhigh
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write
TARGET_HASH: 19f825bf33281b20e374a3fcbc8be8f0a0056cdc

# L2-K2-020 — Renderer-visible project source diagnostic status

## Mission

Implement exactly the K2-020 renderer-visible project source diagnostic status surface described by `BEB-K2-020`. Keep the change small, test-driven, deterministic, and authority-bounded. The only product-facing delta is that existing sanitized K2-019 source-intake/model-health status becomes visible through the renderer/App surface and renderer entry. Do not implement renderer filesystem reads, new IPC/preload authority, parser process spawning, source repair/adoption/import/promotion, provider/Agent A behavior, projection-layout trust, save/export/session persistence, or canonical SysML/KerML mutation.

## Allowed files

You may modify only:

- `package.json`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`
- `src/shared/foundation.ts`
- `src/renderer/App.tsx`
- `src/renderer/main.tsx`
- `src/renderer/styles.css`

You may create only:

- `tests/renderer-project-source-diagnostic-status.test.mjs`

Do not modify docs, lockfiles, generated outputs, dependencies, parser assets, privileged main-process source-intake modules, preload IPC files, shared parser/projection implementation modules, provider/workspace/candidate modules, existing focused tests outside the allowlist, or existing K2 artifacts during route execution.

## Required TDD sequence

1. Add `tests/renderer-project-source-diagnostic-status.test.mjs` first.
2. Run `node tests/renderer-project-source-diagnostic-status.test.mjs` and record RED because the current target lacks the K2-020 source diagnostic status surface in App/rendererFoundation.
3. Implement only the minimum App/main/styling, validator/package, and foundation metadata changes required for GREEN.
4. Rerun `node tests/renderer-project-source-diagnostic-status.test.mjs` to GREEN.
5. Run all verification commands below and capture exact outputs.

## Implementation constraints

- In `src/renderer/App.tsx`, create a deterministic K2-020 source diagnostic status construction path from a sanitized evidence object. Do not import `fs`, `path`, main-process modules, parser-runtime modules, provider modules, or Electron APIs into the renderer.
- The public App view model should expose a narrowly named status surface such as `projectSourceDiagnosticStatus`. It must not expose raw K2-019 source-intake objects wholesale, the full App model, function handles, DOM handles, or arbitrary source diagnostic input.
- In `src/renderer/main.tsx`, expose only the K2-020 public status surface through `rendererFoundation` with an exact public key set. Do not re-expose the entire App/view model or additional renderer internals.
- Public status fields should be exact, frozen/deep-frozen, and bounded. Include status/slice/role/label, source diagnostic state, model-health state, warning/degraded reasons, read-only/bounded/visible/trusted flags, fixed denied-authority rows, CSS class names, and escaped static markup.
- Use fixed catalogs for denied authority rows and class names. Do not generate rows by iterating arbitrary caller object keys.
- Missing/malformed/stale/contradictory/proxy/getter/callable/symbol evidence must fail closed to a visible degraded/untrusted status without invoking caller code or leaking raw hostile fields. If a helper is exported only for tests, keep the export narrow and prove it cannot mutate public state or grant authority.
- Static markup must be escaped and non-canvas/non-SVG. It may use inert tags such as `<section>`, `<header>`, `<dl>`, `<dt>`, `<dd>`, `<ul>`, `<li>`, `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>`, and `<span>`. Do not add `<script>`, `<canvas>`, `<svg>`, `<form>`, `<input>`, `<button>`, event handlers, `dangerouslySetInnerHTML`, DOM/browser API calls, network fonts/assets, localStorage/sessionStorage, or external assets.
- Keep every denied-authority indicator false/unauthorized. Do not introduce renderer filesystem expansion, new IPC/preload expansion, parser execution/process spawning, provider calls, graph/layout/canvas/SVG trust, source coordinates, canonical mutation, source repair, import/adoption/promotion, saved-view persistence, save/export/session persistence, support export, telemetry, dependency changes, RTM/`blk-link`, or BEO publication/storage/ledger.
- If stylesheet changes are made, keep them inert local classes for the diagnostic status only; no generated assets, network fonts, external imports, layout engines, animation/event semantics, or hidden authority wording.
- Update `scripts/validate-foundation.mjs` so K2-020 is required, the focused test is part of required files and `npm test`, and forbidden raw authority/source fields remain blocked.
- Update `tests/foundation.test.mjs` and `src/shared/foundation.ts` for K2-020 metadata only while preserving K2-001..K2-019 evidence.

## Required tests

Cover at least:

- current target RED for missing K2-020 project source diagnostic status in App/rendererFoundation;
- deterministic `appViewModel.projectSourceDiagnosticStatus` or equivalent shape and exact approved keys;
- `rendererFoundation` exposes the same status/markup through exact public keys and does not expose the full app/view model;
- source diagnostic state, model-health state, visible status text, warnings, degraded reasons, and denied-authority rows are visible and bounded;
- raw source/body/path/filename/provider/prompt/credential/token/diagnostic/parser/telemetry fragments are absent from public status, rows, and markup except constrained denied labels;
- malformed, missing, proxy/getter/callable/symbol, and contradictory evidence fails closed without invoking caller code;
- all denied-authority indicators are present, visible, and false/unauthorized;
- read-only/bounded/visible flags remain true as appropriate and trusted remains false unless inherited sanitized evidence is explicitly trusted without warnings/degraded reasons;
- public status and nested rows/class names/markup are frozen/deep-frozen and expose no mutable function/prototype/DOM handles;
- changed renderer executable text does not introduce canvas/SVG/layout/ELK/JointJS/saved-view/localStorage/sessionStorage/fetch/provider/parser/import/export/canonical-mutation behavior except explicit denied labels;
- `styles.css` contains only inert local classes for the status surface if touched;
- package scripts include the K2-020 test and no dependency fields.

## Verification commands

```bash
node tests/renderer-project-source-diagnostic-status.test.mjs
node tests/renderer-projection-panel-presentation.test.mjs
node tests/renderer-projection-panel.test.mjs
node tests/project-package-inspection.test.mjs
node tests/parser-diagnostic-loop.test.mjs
node scripts/validate-foundation.mjs
npm test
npm run build
npm run typecheck
git diff --check -- package.json scripts/validate-foundation.mjs tests/foundation.test.mjs src/shared/foundation.ts src/renderer/App.tsx src/renderer/main.tsx src/renderer/styles.css tests/renderer-project-source-diagnostic-status.test.mjs
```

## Final response requirements to BLK-System

Report the RED command and expected failure excerpt, GREEN focused test output, full verification outputs, final changed file list, exact feature commit hash, denied-authority summary, hostile-review verdict or blockers, and residual blockers/watch items. If BLK-pipe route execution times out or fails due to environment/tooling, preserve the exact approved allowlist/target hash and report whether clean-worktree retargeting or remediation was used.

## Adversarial readiness card

Slice: K2-020 — Renderer-visible project source diagnostic status.
Milestone: C/D bridge — read-only source/model-health status visibility.
Compartment: Workspace / project package, Parser / semantic model, and Projection / view at the read-only status-presentation seam.
One authority boundary: renderer-visible presentation of already-sanitized project-source diagnostic/model-health status.
Direct requirements: `REQ-KN-008`, `REQ-KN-015`, `REQ-KN-016`.
Supporting-only requirements: `REQ-KN-081`, `REQ-KN-082`, `REQ-KN-083`, `REQ-KN-084`, `REQ-KN-104`, `REQ-KN-129`.
Explicitly denied capabilities: project writes, source repair, source adoption/import/promotion, renderer filesystem authority, new IPC/preload authority, parser process spawning/runtime expansion, provider/Agent A behavior, projection-layout/canvas/SVG trust, saved-view/session persistence, save/export/support export, telemetry, dependency changes, RTM generation, production `blk-link`, and BEO publication/signing/storage/ledger.
Malformed input behavior: K2-020 must not trust caller-supplied source diagnostic objects. Missing/malformed/proxy/getter/callable/symbol evidence must fail closed to bounded degraded/untrusted visible status rather than executing callbacks, reading files, or serializing hostile fields.
Contradictory input behavior: any status claiming ready/accepted/trusted while warning/degraded/denied/unavailable/malformed evidence exists must expose the stricter degraded/untrusted status or fail closed.
Spoofing seams to forbid: raw source/body/path/filename/directory listing/OS error/stack trace fields, provider/prompt/credential/token fields, parser handles, function/callback/DOM handles, mutable prototypes, source-coordinate truth, filesystem claims, provider/Agent A claims, import/export/save/session/canonical-mutation claims, layout/canvas/SVG claims, BEO/RTM/`blk-link` claims.
Raw/leaky fields to forbid: `raw`, `sourceText`, `content`, `modelText`, `path`, `filename`, `dirname`, `diagnostics`, `parserInput`, `providerPayload`, `providerRequest`, `prompt`, `credential`, `token`, `errorBody`, `stack`, `sourceCoordinates`, `layoutCoordinates`, `canvas`, `svg`, `elk`, `jointjs`, `save`, `export`, `rtm`, `blk-link`, `beoPublication`, except fixed denied-authority labels that tests constrain.
Closeout docs/mirrors to update after successful implementation: canonical `BEO-K2-020`, `docs/roadmaps/K2_implementation-roadmap.md`, `docs/traceability/K2_traceability.yaml`, and view-only Obsidian BEB/BEO/L2/outcome/roadmap/traceability mirrors after final commit.

## Readiness profile probe card

These probes are required pre-dispatch checklist evidence only. They do not authorize source/Git mutation, parser execution, provider/runtime dispatch, BEO publication, RTM generation, or reusable BLK-pipe/Codex authority beyond the exact approved drop.

### kuronode-renderer-public-surface-v1

- [ ] KRP-001 exact public renderer export/key set is asserted; no full app/model/view-model exposure unless explicitly authorized
- [ ] KRP-002 denied-authority/status/security rows derive from a fixed catalog, not arbitrary object keys
- [ ] KRP-003 hostile JavaScript objects, proxies, getters, symbols, and descriptor traps fail closed without leaking raw fields
- [ ] KRP-004 public presentation objects are deeply frozen and expose no callable, DOM, prototype, or mutable handles
- [ ] KRP-005 markup and visible rows are static and escaped; raw source/model/path/provider/prompt/credential/diagnostic/telemetry fragments are forbidden
- [ ] KRP-006 canvas/layout/persistence/filesystem/provider/import/export/mutation/RTM/blk-link/BEO-publication authorities remain visibly denied
- [ ] KRP-007 degraded, warning, stale, contradictory, or untrusted evidence chooses the stricter visible fail-closed state
- [ ] KRP-008 conditional pre-dispatch evidence for renderer-visible public surfaces only; the profile does not authorize source/Git mutation and does not make this profile mandatory for non-renderer slices

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
