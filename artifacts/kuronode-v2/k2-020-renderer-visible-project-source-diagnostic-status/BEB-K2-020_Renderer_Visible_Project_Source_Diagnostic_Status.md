---
beb_id: "BEB-K2-020"
beo_id: "BEO-K2-020"
l2_id: "L2-K2-020"
model: "gpt-5.5"
reasoning_effort: "xhigh"
route: "BEB-L2 -> BLK-pipe -> Codex workspace-write"
target_repo: "/home/dad/code/Kuronode-v2"
target_branch: "main"
target_hash: "19f825bf33281b20e374a3fcbc8be8f0a0056cdc"
trace_artifacts:
  - kind: "product_convergence_map"
    id: "K2-PRODUCT-CONVERGENCE-MAP"
    version_hash: "sha256:bc70f88549b0939395495861a3797d4d42fcf72b584926927712700c00c69cb9"
  - kind: "roadmap"
    id: "K2-IMPLEMENTATION-ROADMAP"
    version_hash: "sha256:9103f4b40d4106b31fa75ecc4094da070f4cb2f1b52d98d0ae65142e3f299ac1"
  - kind: "process_guard"
    id: "K2-ITERATION-DRIFT-PROTECTION"
    version_hash: "sha256:a2acedfa31dae7134298c39b0f7ec7ee9c47e79cd0d54179cd28a3f3fb76a393"
  - kind: "traceability_index"
    id: "K2-TRACEABILITY-MANIFEST"
    version_hash: "sha256:d83fd5bc2b597ac988db032894147270c491d0f7154e9fc8f98810463068f959"
  - kind: "requirement"
    id: "REQ-KN-008"
    version_hash: "sha256:e7f8860fc625778a3c440d9b91ae195cd5025239f75f484bf25255ebeab2613c"
  - kind: "requirement"
    id: "REQ-KN-015"
    version_hash: "sha256:79c5d26a80f7f206a3898cad31f54a64273ede08b474c0dcb3cdbf05cb0e1af8"
  - kind: "requirement"
    id: "REQ-KN-016"
    version_hash: "sha256:406aedd68ab491fc83bb705df958766228d60efbcdfad9de5a363bb33534dc54"
  - kind: "requirement_supporting"
    id: "REQ-KN-081"
    version_hash: "sha256:5a0fc367c36db330ac6f5588642b66ad3e54fb1692fa4c4a94fc6fd5e1bf6333"
  - kind: "requirement_supporting"
    id: "REQ-KN-082"
    version_hash: "sha256:7e594b3e9fe6116af61c19240c0f037c4d403a715061b4bb1a74a42a2c298751"
  - kind: "requirement_supporting"
    id: "REQ-KN-083"
    version_hash: "sha256:0c0468e9b11e2e65170318edc99501d865d846860c56ee75a6dc7146d993afb0"
  - kind: "requirement_supporting"
    id: "REQ-KN-084"
    version_hash: "sha256:a704f161aee6841737a9d9f355e88ac1f001ed8d77d369a9be291cace3e64a67"
  - kind: "requirement_supporting"
    id: "REQ-KN-104"
    version_hash: "sha256:3c0908d9cf11b08becd9d43c6a83d1d5472448d7aaae0c915f4148eb62ac3f79"
  - kind: "requirement_supporting"
    id: "REQ-KN-129"
    version_hash: "sha256:02295c7bbd637450eaad75f92e64be781feeccb148f63403d08786a1350f948a"
  - kind: "architecture"
    id: "KVA-004-C4-COMPONENT-MODEL"
    version_hash: "sha256:1bffba596fcedf5d6f2cf93d82afc6e7ae3483639f9910f4d7c7b394eb5cbe1b"
  - kind: "architecture"
    id: "KVA-005-ARCHITECTURE-INVARIANTS"
    version_hash: "sha256:51ffbd376dee23e4a12ce064acc55ac30e6902abd8ea2ec4bc4568957725ba0d"
  - kind: "interface_contract"
    id: "ICD-KVA-001"
    version_hash: "sha256:1074a27f2b1d44ccd9336c7257a8fe69f984ffadedb1e1fc8e871c67360612f3"
  - kind: "interface_contract"
    id: "ICD-KVA-003"
    version_hash: "sha256:34ff70aaa1f9a00fdf4942b2b42f079f887b8fbac0872ca6c6d86d59230a13e2"
  - kind: "allocation"
    id: "KVA-013-REQ-ALLOCATION"
    version_hash: "sha256:7e2562c496a37c7ce7d35bb704a10abd0731922acf7f9aaa8d25b14280cc708d"
  - kind: "verification"
    id: "KVA-031-BEB-L2-PREFLIGHT"
    version_hash: "sha256:fd01ddb7ed1a54518e15efc8e238a29695a3c9342235eedcdb8fb6f9ccb512df"
  - kind: "verification"
    id: "KVA-032-EVIDENCE-LEDGER"
    version_hash: "sha256:d88483948373704534f7bf1b574d26f04dc15c2e5e1a3814cbe3e2e0c17abf6a"
  - kind: "prior_outcome"
    id: "BEO-K2-019"
    version_hash: "sha256:8eff3e9455d83918fc326c1d6949c5a3a696ce638cda19dbf221821bd11d6eeb"
---
# BEB-K2-020

## Executive intent / plain-English goal

K2-020 exposes the K2-019 bounded project-source intake / parser model-health result as a renderer-visible, sanitized, read-only diagnostic status surface. A user or tester should be able to see whether the active project's source diagnostic state is accepted, denied, degraded, malformed, unavailable, or not-ready, and see bounded warning/degraded reasons without raw source text, raw paths, filenames, OS errors, parser handles, provider payloads, prompt/credential data, source coordinates, filesystem authority, or mutation controls.

This slice is a presentation/status bridge only. It does not add renderer filesystem reads, new Electron IPC/preload privileges, parser process spawning, parser runtime expansion, source repair, source adoption, external-edit import/promotion, save/export/session persistence, projection-layout trust, provider/Agent A behavior, RTM generation, production `blk-link`, or BEO publication/signing/storage/ledger.

## Why this slice exists now

K2-019 proved that package-internal SysML/KerML source can be read under strict main-process read-only gates and normalized into sanitized parser/model-health metadata. The next meaningful product delta is to make that existing diagnostic status visible at the renderer/App surface so degraded source/model-health conditions are not hidden from the user. K2-020 therefore strengthens the bridge among project package inspection, parser/model-health state, and renderer-visible status while preserving the no-mutation/no-provider/no-layout-trust boundary.

## Direct product requirement stance

Direct requirements for this slice:

- `REQ-KN-008`: project/source load failures and unavailable/denied source diagnostic states must be visibly reported as sanitized renderer status rather than thrown, hidden, or leaked.
- `REQ-KN-015`: the status surface must represent one normalized model-health/source-diagnostic state for the active project-source diagnostic seam; contradictory ready/trusted claims must fail closed or choose the stricter degraded/untrusted state.
- `REQ-KN-016`: degraded model-health/source diagnostic states must be user-visible through the renderer/App status surface.

## Supporting / prepared requirement stance

Supporting context only: `REQ-KN-081`, `REQ-KN-082`, `REQ-KN-083`, `REQ-KN-084`, `REQ-KN-104`, and `REQ-KN-129`. They inform current-model/projection context, truth/view separation, degraded visible warning discipline, local project package/source identity, and parser-runtime readiness. K2-020 does not close projection correctness, package persistence, canonical-source mutation, parser asset packaging, or multi-file SysML behavior.

## Lifecycle / enabling trace

K2-020 is product-facing status/presentation behavior at a narrow seam. It consumes only sanitized evidence shaped by prior K2-009/K2-010/K2-019 work and exposes a frozen renderer-visible status object/markup. It prepares later user workflows that need honest model-health/source warning visibility, but it is not itself a save/import/adoption/projection-layout feature.

## Architecture/readiness guidance

Use the hash-bound trace artifacts in frontmatter as authority context. Relevant boundaries:

- `ICD-KVA-001`: package-internal source and project package boundaries remain main-process/read-only evidence only.
- `ICD-KVA-003`: parser/model-health envelope and sanitized diagnostic status semantics are the source of status vocabulary.
- `KVA-004` and `KVA-005`: component/invariant guidance requires renderer/public surfaces to avoid hidden authority expansion.
- `KVA-013`, `KVA-031`, and `KVA-032`: requirement allocation, BEB/L2 preflight, and evidence-readiness constraints.
- BLK-SYSTEM-357 renderer public-surface readiness: exact public keys, fixed denied-authority catalogs, proxy/getter/callable fail-closed probes, deep-frozen handles, static escaped markup, and raw-fragment non-leakage must be covered.

## Exact implementation scope

Allowed modified files:

- `package.json`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`
- `src/shared/foundation.ts`
- `src/renderer/App.tsx`
- `src/renderer/main.tsx`
- `src/renderer/styles.css`

Allowed new files:

- `tests/renderer-project-source-diagnostic-status.test.mjs`

No other files may be modified or created by the implementation commit. In particular, do not modify docs, lockfiles, generated outputs, dependencies, parser assets, main-process privileged source-intake code, preload IPC files, shared parser/projection implementation modules, provider/workspace/candidate modules, existing focused tests outside the allowlist, or K2 artifacts during route execution.

## Required TDD evidence

1. Add `tests/renderer-project-source-diagnostic-status.test.mjs` first.
2. Run `node tests/renderer-project-source-diagnostic-status.test.mjs` and record RED because current `App` / `rendererFoundation` lacks the K2-020 source diagnostic status surface.
3. Implement only the minimum App/main/styling, validator/package, and foundation metadata changes required for GREEN.
4. Rerun the focused test to GREEN, then run the full verification plan in L2.

## Acceptance criteria

- `src/renderer/App.tsx` exposes `appViewModel.projectSourceDiagnosticStatus` or an equivalent deterministic K2-020 status object derived only from a sanitized source-diagnostic/model-health evidence shape, not from raw source, paths, filesystem APIs, parser handles, provider payloads, or caller authority flags.
- `src/renderer/main.tsx` exposes the K2-020 status through `rendererFoundation` with an exact public key set; do not re-expose the full App/view model.
- The status object has exact, bounded, frozen/deep-frozen fields for status/slice/role/label, model-health state, source-diagnostic state, warning/degraded reasons, read-only/bounded/trusted/visible flags, fixed denied-authority rows, class names, and escaped static markup.
- The public surface must not expose raw source body, raw path, filename, directory listing, OS errors, stack traces, source coordinates, raw diagnostic parser input, provider/prompt/credential/token payloads, function handles, DOM/browser handles, mutable prototypes, or executable callbacks.
- Malformed/missing/proxy/getter/callable/contradictory evidence must fail closed to a bounded degraded/untrusted visible status without invoking caller code or leaking hostile fields.
- All adjacent denied authorities remain visibly denied/false: renderer filesystem expansion, main-process filesystem expansion beyond K2-019, parser process spawning, provider/Agent A, import/export, source repair/adoption/promotion, canonical mutation, projection/layout/canvas/SVG trust, saved-view/session persistence, support export, telemetry, dependency changes, RTM/`blk-link`, and BEO publication/storage/ledger.
- Static markup is escaped and non-canvas/non-SVG/non-form/non-button. It may use inert semantic tags similar to K2-018 and must not use DOM/browser APIs, event handlers, `dangerouslySetInnerHTML`, network fonts/assets, localStorage/sessionStorage, or external assets.
- `scripts/validate-foundation.mjs`, `tests/foundation.test.mjs`, and `package.json` include the K2-020 focused test/file surface and preserve existing K2-001..K2-019 gates.

## Required hostile probes

Before closeout, verify:

1. exact renderer public export/key sets and exact K2-020 status keys;
2. fixed denied-authority/status row catalogs, not arbitrary object-key enumeration;
3. hostile JavaScript objects, proxies, getters, symbols, callable inputs, and descriptor traps fail closed without invoking caller code;
4. frozen/deep-frozen public status and markup handles expose no callable, DOM, prototype, or mutable handles;
5. escaped/static markup contains no raw source/model/path/filename/provider/prompt/credential/token/diagnostic/telemetry fragments outside constrained denied labels;
6. malformed, missing, stale, contradictory, warning, degraded, denied, or untrusted evidence chooses the stricter visible fail-closed state;
7. changed renderer text does not introduce canvas/SVG/layout/ELK/JointJS/saved-view/storage/fetch/provider/parser/import/export/canonical-mutation behavior except explicit denied labels;
8. package and validator gates include the focused K2-020 test and governed file metadata.

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

## Verification commands and acceptance evidence

Codex should run and preserve evidence for:

- `node tests/renderer-project-source-diagnostic-status.test.mjs`
- `node tests/renderer-projection-panel-presentation.test.mjs`
- `node tests/renderer-projection-panel.test.mjs`
- `node tests/project-package-inspection.test.mjs`
- `node tests/parser-diagnostic-loop.test.mjs`
- `node scripts/validate-foundation.mjs`
- `npm test`
- `npm run build`
- `npm run typecheck`
- `git diff --check -- package.json scripts/validate-foundation.mjs tests/foundation.test.mjs src/shared/foundation.ts src/renderer/App.tsx src/renderer/main.tsx src/renderer/styles.css tests/renderer-project-source-diagnostic-status.test.mjs`

Acceptance requires the focused RED/GREEN evidence, full static validation, full test-suite pass, exact allowed-file diff, no raw/leaky fragments in public status/markup, no denied behavior introduced in renderer text, and hostile-review PASS or a narrow remediation BEB/L2 before BEO closeout.

## blk-link / RTM stance

This package produces bounded product/status evidence only. It does not run RTM generation, production `blk-link`, protected-body read/copy/scan/hash, drift rejection, coverage truth, BEO publication/signing/storage/ledger, reusable BLK-pipe/Codex dispatch, or any runtime/provider/filesystem authority beyond the exact approved drop and existing K2-019 sanitized source-diagnostic seam.

## Denied adjacent behaviors

K2-020 does not authorize project writes, source repair, source adoption, external-edit import/promotion, save/export/session persistence, provider/Agent A behavior, live provider payload retention, renderer filesystem authority, new Electron IPC/preload privileges, parser process spawning or runtime expansion, source-coordinate truth claims, multi-file SysML support, projection/layout/canvas/SVG trust, support-bundle export, telemetry, dependency/package-manager changes, RTM generation, production `blk-link`, or BEO publication/signing/storage/ledger.

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
