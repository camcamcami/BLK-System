---
beb_id: "BEB-K2-018"
beo_id: "BEO-K2-018"
l2_id: "L2-K2-018"
model: "gpt-5.5"
reasoning_effort: "xhigh"
route: "BEB-L2 -> BLK-pipe -> Codex workspace-write"
target_repo: "/home/dad/code/Kuronode-v2"
target_branch: "main"
target_hash: "db12ddd298b2d47d5ed87d0e8efe856fe94b2eca"
trace_artifacts:
  - kind: "product_convergence_map"
    id: "K2-PRODUCT-CONVERGENCE-MAP"
    version_hash: "sha256:bc70f88549b0939395495861a3797d4d42fcf72b584926927712700c00c69cb9"
  - kind: "roadmap"
    id: "K2-IMPLEMENTATION-ROADMAP"
    version_hash: "sha256:85aa16b66b8195f9e8f931f75e98a0522337fe997b1a7ddfe03119cd07ac6fd8"
  - kind: "process_guard"
    id: "K2-ITERATION-DRIFT-PROTECTION"
    version_hash: "sha256:a2acedfa31dae7134298c39b0f7ec7ee9c47e79cd0d54179cd28a3f3fb76a393"
  - kind: "traceability_index"
    id: "K2-TRACEABILITY-MANIFEST"
    version_hash: "sha256:85c6936486fdde965fb3f66476ba2d6942312136e872e1282bf81dc52d08c913"
  - kind: "requirement"
    id: "REQ-KN-081"
    version_hash: "sha256:5a0fc367c36db330ac6f5588642b66ad3e54fb1692fa4c4a94fc6fd5e1bf6333"
  - kind: "requirement"
    id: "REQ-KN-082"
    version_hash: "sha256:7e594b3e9fe6116af61c19240c0f037c4d403a715061b4bb1a74a42a2c298751"
  - kind: "requirement"
    id: "REQ-KN-083"
    version_hash: "sha256:0c0468e9b11e2e65170318edc99501d865d846860c56ee75a6dc7146d993afb0"
  - kind: "requirement_supporting"
    id: "REQ-KN-039"
    version_hash: "sha256:37d189928e366cd75e1e619c6cd96839ea879b1f275119bc8e06723aabe47846"
  - kind: "requirement_supporting"
    id: "REQ-KN-040"
    version_hash: "sha256:c6f9513a449b3acd3fde5575410f75c394121370aca3fdf5ffc97db7b7558e90"
  - kind: "requirement_supporting"
    id: "REQ-KN-041"
    version_hash: "sha256:8ef1252ec985e5ba797e117df5c690fb64dcfafd27929ca6151892d83a959a19"
  - kind: "requirement_supporting"
    id: "REQ-KN-042"
    version_hash: "sha256:921b06da4206c8407f21a9afadbdde0e04b048e5d73c695194fa205cb1856eb4"
  - kind: "requirement_supporting"
    id: "REQ-KN-048"
    version_hash: "sha256:884e222872cf8ddeaada8bfb72819272b5f613cdaf1b61fb14d1921cf10cffa0"
  - kind: "requirement_supporting"
    id: "REQ-KN-077"
    version_hash: "sha256:4515b1457f48848c81a86283707787582899c66815b0d6529a303bc696628f79"
  - kind: "requirement_supporting"
    id: "REQ-KN-080"
    version_hash: "sha256:c19a3a1d51d80ffb8a87fb0decfff3eaa3233cc1948e6d3b62d497dddaf378d7"
  - kind: "requirement_supporting"
    id: "REQ-KN-084"
    version_hash: "sha256:a704f161aee6841737a9d9f355e88ac1f001ed8d77d369a9be291cace3e64a67"
  - kind: "requirement_supporting"
    id: "REQ-KN-107"
    version_hash: "sha256:1b523c3472541f685d223313c0603d8ab1e18c23ecbfb209ba3bc5f8fce27bce"
  - kind: "architecture"
    id: "KVA-004"
    version_hash: "sha256:1bffba596fcedf5d6f2cf93d82afc6e7ae3483639f9910f4d7c7b394eb5cbe1b"
  - kind: "architecture"
    id: "KVA-005"
    version_hash: "sha256:51ffbd376dee23e4a12ce064acc55ac30e6902abd8ea2ec4bc4568957725ba0d"
  - kind: "runtime_flow"
    id: "RTF-KVA-007"
    version_hash: "sha256:0e51f9b3a7fafd6f319128309452ad23f4d71074ba18007fbdf036f51f726469"
  - kind: "state_machine"
    id: "SM-KVA-010"
    version_hash: "sha256:9055944208258f34c299597eb20e22f3373311ce77bb3d2b37792d5a47d187ff"
  - kind: "interface_contract"
    id: "ICD-KVA-011"
    version_hash: "sha256:593487a624e4cbaad5066c553217ad5d0d58575cf4c0a5fc43f2faf60f4e184e"
  - kind: "prior_outcome"
    id: "BEO-K2-017"
    version_hash: "sha256:600d0be09db6e5f1f7289f9874d58c29fcef52ed3e725f0f10ba48e7b6c5ac65"
---
# BEB-K2-018 — Actual Non-Canvas Projection Panel Presentation

## 1. Executive intent / plain-English goal

Turn the K2-017 bounded read-only projection panel data into an actual renderer-visible, non-canvas presentation surface. A user or tester should be able to inspect static UI markup/presentation metadata for the projection panel from the renderer entry surface, with model state, warning/degraded reasons, payload counts, sanitized node/edge rows, and denied-authority indicators visible. This slice is presentation-only. It is not canvas rendering, graph/layout computation, saved-view persistence, filesystem source reading, parser-runtime expansion, Agent A/provider behavior, candidate staging/import/promotion, import/export, or canonical SysML/KerML mutation.

## 2. Why this slice exists now

K2-017 created safe panel-shaped data, but the renderer entry still exposes a placeholder object rather than a visible panel presentation. K2-018 completes the next bounded Milestone D step by making that safe panel data presentable in the renderer without opening higher-risk rendering, layout, persistence, provider, parser, candidate, import/export, or mutation surfaces.

## 3. Direct product requirement stance

- `REQ-KN-081` is directly advanced at the bounded presentation level: the presentation must derive from the existing K2-017 panel / K2-016 inspection / K2-015 refresh seam, not from stale hard-coded graph truth.
- `REQ-KN-082` is directly advanced: the presentation must keep model truth and view state separate and must not add persistence, save, import/export, or canonical mutation authority.
- `REQ-KN-083` is directly advanced: degraded, warning, untrusted, empty, or not-ready states must remain visible in the presentation and must not be hidden behind happy-path UI text.

This slice does not claim production canvas rendering, layout correctness, full React/Electron runtime rendering, saved-view behavior, parser correctness, multi-file model truth, support export, RTM trace closure, or production `blk-link`.

## 4. Supporting / prepared requirement stance

The following requirements remain supporting/prepared only for this slice: `REQ-KN-039`, `REQ-KN-040`, `REQ-KN-041`, `REQ-KN-042`, `REQ-KN-048`, `REQ-KN-077`, `REQ-KN-080`, `REQ-KN-084`, and `REQ-KN-107`. They inform read-only, degraded, bounded-payload, traceability, inspectability, and future projection semantics but are not fully closed by a static non-canvas presentation surface.

## 5. Architecture and readiness guidance

Stay inside the Projection / view compartment. K2-018 may consume only `appViewModel.projectionPanel` or the existing sanitized K2-017 panel construction path. It may add deterministic renderer presentation metadata, static escaped markup, and inert CSS class/style definitions. It must not create new privileged IPC, preload, filesystem, parser, provider, network, runtime, layout, save/export, candidate, or package-management seams. Renderer-facing presentation data must be sanitized, bounded, deep-frozen, static/read-only, and explicit about denied authorities.

## 6. Exact implementation scope

Allowed modified files:

- `package.json`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`
- `src/shared/foundation.ts`
- `src/renderer/App.tsx`
- `src/renderer/main.tsx`
- `src/renderer/styles.css`

Allowed new files:

- `tests/renderer-projection-panel-presentation.test.mjs`

No other files may be modified or created by the implementation commit. In particular, do not modify docs, lockfiles, generated outputs, dependencies, parser assets, main-process privileged code, preload IPC files, shared projection/refresh implementation modules, view-intent modules, candidate staging modules, provider modules, or existing focused tests outside the allowlist.

## 7. Required TDD evidence

1. Add `tests/renderer-projection-panel-presentation.test.mjs` first.
2. Run `node tests/renderer-projection-panel-presentation.test.mjs` and record RED because the current target lacks K2-018 presentation data/markup in the App/renderer entry surface.
3. Implement only the minimum App/main/styling, validator/package, and foundation metadata changes required for GREEN.
4. Rerun the focused test to GREEN, then run the full verification plan.

## 8. Acceptance criteria

- `src/renderer/App.tsx` exposes a deterministic K2-018 presentation object or equivalent renderer presentation surface derived from `appViewModel.projectionPanel`.
- `src/renderer/main.tsx` exposes the K2-018 presentation/markup through `rendererFoundation` so the renderer entry is no longer only the prior process/app object for this panel.
- Presentation markup is static, escaped, non-canvas, and read-only. It must not expose function handles, DOM handles, mutable objects, raw source/model/path/provider/prompt/credential/diagnostic/telemetry fields, or executable callbacks.
- Presentation includes panel title/ID, read-only state/status text, capability/source ID, warning/degraded reasons, payload counts, sanitized node/edge rows, and denied-authority indicators.
- Inert CSS may style the panel, but must not import network fonts/assets, create hidden generated assets, or imply layout/canvas/saved-view authority.
- Public presentation objects are frozen/deep-frozen and bounded.
- `scripts/validate-foundation.mjs`, `tests/foundation.test.mjs`, and `package.json` include the K2-018 test/file surface.

## 9. Explicitly forbidden actions

Do not implement or introduce:

- `<canvas>`, Canvas API, SVG/graph rendering engine, ELK, JointJS, layout computation/trust, graph traversal trust, render trust, layout coordinates, or saved-view persistence;
- filesystem/source reads, source path/body exposure, parser-runtime expansion, parser process spawning, runtime loading/download/rebuild, source repair, import/export, save/session persistence, support-bundle export, telemetry/upload, network/fetch/XHR/WebSocket, provider/Agent A behavior, prompt/credential/payload handling;
- candidate staging/import/adoption/promotion, external-state adoption, canonical SysML/KerML mutation, package dependency/lockfile changes, privileged IPC/preload expansion, RTM generation, production `blk-link`, BEO publication/signing/storage/ledger, or reusable BLK-System route authority.

## 10. Required hostile probes

Before closeout, verify:

- exact allowed presentation field set and frozen/deep-frozen public handles;
- escaped markup and no raw/leaky fragments in panel/node/edge/authority rows;
- all denied-authority indicators are visible and false/unauthorized;
- no callable/prototype/DOM handles, no `dangerouslySetInnerHTML`, no `<script>`, no `<canvas>`, no forms/inputs/buttons pretending to grant action;
- no canvas/layout/ELK/JointJS/saved-view/localStorage/sessionStorage/fetch/provider/parser/import/export/canonical-mutation behavior in changed renderer text except explicit denied labels;
- degraded/warning/empty/untrusted state information is visible in presentation text;
- package and validator gates include the K2-018 focused test and governed file metadata.

## 11. Adversarial readiness card

Slice: K2-018 — Actual non-canvas projection panel presentation
Milestone: D — First read-only useful projection
Compartment: Projection / view
One authority boundary: renderer-visible static/non-canvas presentation of already-sanitized K2-017 projection panel data.
Direct requirements: REQ-KN-081, REQ-KN-082, REQ-KN-083.
Supporting-only requirements: REQ-KN-039, REQ-KN-040, REQ-KN-041, REQ-KN-042, REQ-KN-048, REQ-KN-077, REQ-KN-080, REQ-KN-084, REQ-KN-107.
Explicitly denied capabilities: canvas rendering, graph/layout engine trust, saved-view persistence, filesystem source reads, parser-runtime expansion, Agent A/provider behavior, candidate staging/import/promotion, import/export, canonical SysML/KerML mutation, RTM generation, production `blk-link`, and BEO publication/signing/storage/ledger.
Malformed input behavior: K2-018 must not accept caller-supplied graph/source/provider/input objects. If presentation construction receives missing or malformed panel evidence, it must degrade to bounded static fail-closed presentation rather than executing callbacks, reading files, or trusting raw fields.
Contradictory input behavior: any state where presentation claims ready/trusted while underlying panel/inspection evidence is degraded, warning, untrusted, stale, or denied must expose the stricter degraded/untrusted state or fail closed.
Spoofing seams to forbid: raw source/model/path/provider/prompt/credential/diagnostic/telemetry fields, function/getter/proxy/callable panel inputs, mutable public handles, prototype pollution, DOM handles, layout/canvas claims, saved-view claims, filesystem claims, provider/Agent A claims, import/promotion/canonical-mutation claims.
Raw/leaky fields to forbid: `raw`, `source`, `sourceText`, `modelText`, `path`, `provider`, `prompt`, `credential`, `token`, `diagnostic`, `telemetry`, `parser`, `canonical`, `mutation`, `layoutCoordinates`, `canvas`, `elk`, `jointjs`, `save`, `export`, `rtm`, `blk-link`, `beoPublication` except explicit denied-authority labels that tests constrain.
Required hostile probes: frozen/deep-frozen public presentation; exact allowed presentation field set; escaped/static markup; no raw/leaky fragments in node/edge/detail rows; all denied-authority indicators visible and false; bounded visible node/edge/detail counts; no callable/prototype/DOM handles exposed; no canvas/layout/saved-view/storage/fetch/provider/import/export dependencies; stale/degraded/empty/warning states remain visible; package and validator gates include the focused test and new K2-018 governed files.
Closeout docs/mirrors to update: canonical `BEO-K2-018`, `docs/roadmaps/K2_implementation-roadmap.md`, `docs/traceability/K2_traceability.yaml`, and view-only Obsidian BEB/BEO/L2/outcome/roadmap mirrors after final commit.

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
