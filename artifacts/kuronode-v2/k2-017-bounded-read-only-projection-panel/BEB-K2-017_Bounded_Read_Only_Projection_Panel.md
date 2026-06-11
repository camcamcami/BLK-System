---
beb_id: "BEB-K2-017"
beo_id: "BEO-K2-017"
l2_id: "L2-K2-017"
model: "gpt-5.5"
reasoning_effort: "xhigh"
route: "BEB-L2 -> BLK-pipe -> Codex workspace-write"
target_repo: "/home/dad/code/Kuronode-v2"
target_branch: "main"
target_hash: "747846ce741ec586b76b8a5edd7b96c25001cc58"
trace_artifacts:
  - kind: "product_convergence_map"
    id: "K2-PRODUCT-CONVERGENCE-MAP"
    version_hash: "sha256:bc70f88549b0939395495861a3797d4d42fcf72b584926927712700c00c69cb9"
  - kind: "roadmap"
    id: "K2-IMPLEMENTATION-ROADMAP"
    version_hash: "sha256:9050223579bf5c6fc4a9bb135dfa7f34e3925dd5045ae44a0e1c8dac8be026e6"
  - kind: "process_guard"
    id: "K2-ITERATION-DRIFT-PROTECTION"
    version_hash: "sha256:a2acedfa31dae7134298c39b0f7ec7ee9c47e79cd0d54179cd28a3f3fb76a393"
  - kind: "traceability_index"
    id: "K2-TRACEABILITY-MANIFEST"
    version_hash: "sha256:2f508d9290304ee2f2b8493a324ca2dae67aaf24ae54b41f4e196cde15c57911"
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
    id: "BEO-K2-016"
    version_hash: "sha256:c5da53a0668cbdb2e8395c581614832cb5e00ebc472ebcf8659f7ad9002fff6b"
---
# BEB-K2-017 — Bounded Read-Only Projection Panel

## 1. Executive intent / plain-English goal

Turn the K2-016 renderer-visible projection inspection into a bounded, user-facing read-only projection panel model in the renderer/App surface. A user or tester should be able to see a non-canvas panel that presents model/projection state, warning or degraded reasons, bounded node and edge summaries, and explicit denied-authority indicators. This slice is read/projection UI presentation only. It is not canvas rendering, layout computation, saved-view persistence, filesystem source reading, parser-runtime expansion, Agent A/provider behavior, candidate staging/import/promotion, export, or canonical SysML/KerML mutation.

## 2. Why this slice exists now

K2-016 made sanitized projection refresh data inspectable in the renderer/App view model, but it remains a hidden inspection object rather than a bounded panel-shaped presentation surface. K2-017 advances Milestone D by producing a renderer-visible read-only panel from that already-sanitized data before any higher-risk canvas, layout, persistence, provider, candidate, import, export, or canonical mutation work.

## 3. Direct product requirement stance

- `REQ-KN-081` is directly advanced at the bounded panel level: the panel must derive from the current K2-016 projection inspection / K2-015 refresh seam rather than hard-coded stale graph truth.
- `REQ-KN-082` is directly advanced: the panel must keep canonical model truth separate from view/presentation state and must not add persistence or mutation authority.
- `REQ-KN-083` is directly advanced: warning, degraded, empty, stale, untrusted, or unavailable states must remain visible and fail closed rather than being hidden behind a happy-path panel.

This slice does not claim full production rendering, layout correctness, canonical SysML truth, saved-view behavior, multi-file model truth, support export, RTM trace closure, or production `blk-link`.

## 4. Supporting / prepared requirement stance

The following requirements remain supporting/prepared only for this slice: `REQ-KN-039`, `REQ-KN-040`, `REQ-KN-041`, `REQ-KN-042`, `REQ-KN-048`, `REQ-KN-077`, `REQ-KN-080`, `REQ-KN-084`, and `REQ-KN-107`. They inform read-only, warning, bounded-payload, traceability, and inspectability semantics but are not fully closed by a renderer panel model.

## 5. Architecture and readiness guidance

Use the hash-bound trace artifacts in this BEB as fixed context. Stay inside the Projection / view compartment. K2-017 may consume the existing K2-016 `appViewModel.projectionInspection` / K2-015 refresh output and may add a deterministic panel-shaped renderer model or minimal renderer presentation data. It must not create new privileged IPC, preload, filesystem, parser, provider, runtime, layout, save/export, candidate, or package-management seams. Renderer-facing panel data must be sanitized, frozen/deep-frozen, bounded, and explicit about denied authorities.

## 6. Exact implementation scope

Allowed modified files:

- `package.json`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`
- `src/shared/foundation.ts`
- `src/renderer/App.tsx`
- `src/renderer/styles.css`

Allowed new files:

- `tests/renderer-projection-panel.test.mjs`

No other files may be modified or created by the implementation commit. In particular, do not modify docs, lockfiles, generated outputs, dependencies, parser assets, main/preload IPC files, shared projection/refresh implementation modules, view-intent modules, candidate staging modules, provider modules, or existing focused tests outside the allowlist.

## 7. Required renderer-visible behavior

`src/renderer/App.tsx` must expose a deterministic `projectionPanel` or equivalently named test-bound panel entry on `appViewModel` that is derived from the existing K2-016 `projectionInspection` object. The panel must be presentation-shaped, not a second projection engine.

The panel must expose only sanitized and bounded fields such as:

- panel ID/title and read-only status text;
- source capability ID `model-projection-refresh`;
- projection/refresh state and visible warning/degraded/empty reasons;
- payload counts copied from the sanitized inspection counts;
- bounded visible node summaries and edge summaries copied from sanitized inspection summaries;
- explicit read-only/bounded/trusted flags (`readOnly` true, `bounded` true, `trusted` false unless existing inspection truth says otherwise);
- explicit denied-authority indicators or badges showing filesystem reads, parser/runtime expansion, layout/canvas trust, saved-view persistence, provider/Agent A behavior, candidate import/promotion, import/export, canonical mutation, RTM/`blk-link`, and BEO publication/storage/ledger remain unauthorized.

The public `appViewModel` and panel object must be frozen/deep-frozen enough that tests cannot mutate the exposed panel metadata. Do not expose raw source/model text, diagnostic arrays, file paths, coordinates, stack traces, prompts, credentials, provider payloads, support/export payloads, telemetry, functions/callables/getters/proxies, DOM handles, mutable class instances, or mutable arrays/objects.

## 8. Required TDD sequence

1. Create `tests/renderer-projection-panel.test.mjs` first.
2. Run `node tests/renderer-projection-panel.test.mjs` and record RED because K2-017 panel data is not yet exposed.
3. Implement the smallest renderer/App and optional stylesheet changes needed to pass the focused test.
4. Update `package.json`, `scripts/validate-foundation.mjs`, `tests/foundation.test.mjs`, and `src/shared/foundation.ts` only as needed to register K2-017 metadata, test wiring, validator gates, helper-vocabulary confinement, and boundary text.
5. Rerun the focused test to GREEN, then run the full verification commands.

## 9. Required tests and validator gates

Cover at least:

- `appViewModel.projectionPanel` or the chosen test-bound panel name exists and is deterministic across two reads;
- the panel is derived from `appViewModel.projectionInspection`, not from a duplicated stale graph literal;
- panel fields use an exact approved field set and do not expose raw inspection internals beyond sanitized copies;
- state/warnings/counts/node summaries/edge summaries agree with projection inspection;
- empty/degraded/warning states are visible in the panel model when present;
- all denied-authority indicators remain false/unauthorized and visible;
- no canvas/layout/ELK/JointJS/saved-view/localStorage/sessionStorage/fetch/provider/import/export/canonical-mutation vocabulary appears in executable renderer behavior except as explicit denied labels;
- public panel objects are frozen/deep-frozen and cannot be mutated;
- bounded node/edge rows do not include raw source/model/path/provider/diagnostic/credential/telemetry markers;
- package scripts include the new focused test in `npm test` without adding dependencies;
- validator/foundation gates classify the new test and any K2-017 renderer/style surface explicitly.

## 10. Verification commands

Run and leave exact output evidence:

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

## 11. Acceptance criteria

- Focused K2-017 test shows RED before implementation and GREEN after implementation.
- `npm test`, `npm run build`, and `npm run typecheck` pass.
- The implementation commit changes only the allowed files.
- No dependencies, lockfiles, generated outputs, parser/runtime assets, filesystem reads, provider calls, IPC expansion, layout/canvas engine trust, saved-view persistence, import/export, canonical mutation, or BEO/RTM/`blk-link` behavior are introduced.
- Hostile review has no blockers for raw leakage, helper-vocabulary drift, mutable public handles, authority laundering, stale roadmap/trace wording, overclaiming product requirement closure, or panel readiness contradicting projection inspection state.

## 12. `blk-link` / RTM stance

Metadata is prepared only. RTM generation and production `blk-link` are not authorized or performed by this slice. Protected requirement/body reads, source-body scans, coverage truth, drift rejection, BEO publication, signing, storage, and ledger actions remain denied.

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

