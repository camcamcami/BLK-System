---
beb_id: "BEB-K2-015"
beo_id: "BEO-K2-015"
l2_id: "L2-K2-015"
model: "gpt-5.5"
reasoning_effort: "xhigh"
route: "BEB-L2 -> BLK-pipe -> Codex workspace-write"
target_repo: "/home/dad/code/Kuronode-v2"
target_branch: "main"
target_hash: "68a9b8c0b9b056a9c8a80d8bae32c093ade4c8e6"
trace_artifacts:
  - kind: "product_convergence_map"
    id: "K2-PRODUCT-CONVERGENCE-MAP"
    version_hash: "sha256:bc70f88549b0939395495861a3797d4d42fcf72b584926927712700c00c69cb9"
  - kind: "roadmap"
    id: "K2-IMPLEMENTATION-ROADMAP"
    version_hash: "sha256:a1ea64058864785a0530b365ec27069d3256bce0f66d9304ff76460736a03fd0"
  - kind: "process_guard"
    id: "K2-ITERATION-DRIFT-PROTECTION"
    version_hash: "sha256:a2acedfa31dae7134298c39b0f7ec7ee9c47e79cd0d54179cd28a3f3fb76a393"
  - kind: "traceability_index"
    id: "K2-TRACEABILITY-MANIFEST"
    version_hash: "sha256:894f69016511b7dabb42d2fcdfc9dbe66e612f6c2d2a75b3fa372c63d3f2a6ec"
  - kind: "requirement"
    id: "REQ-KN-081"
    version_hash: "sha256:5a0fc367c36db330ac6f5588642b66ad3e54fb1692fa4c4a94fc6fd5e1bf6333"
  - kind: "requirement"
    id: "REQ-KN-082"
    version_hash: "sha256:7e594b3e9fe6116af61c19240c0f037c4d403a715061b4bb1a74a42a2c298751"
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
    id: "REQ-KN-083"
    version_hash: "sha256:0c0468e9b11e2e65170318edc99501d865d846860c56ee75a6dc7146d993afb0"
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
    id: "BEO-K2-014"
    version_hash: "sha256:427640fa1c7adc145710fe5f0f5c3c8e88994b911e512cdbdf62b8be9acdee08"
---
# BEB-K2-015 — Live Read-Only Model/Projection Refresh

## 1. Executive intent

`BEB-K2-015` authorizes one bounded Kuronode V2 implementation slice after `K2-014`: connect accepted bounded in-memory model snapshot/model-health evidence and accepted view-intent parameters to a refreshed sanitized read-only projection payload. The slice continues product-convergence **Milestone D — First read-only useful projection** in the **Projection / view** compartment.

Plain-English goal: Kuronode should be able to take an already-accepted, in-memory model snapshot plus model-health evidence and derive a read-only projection payload using the same bounded payload semantics as the K2-013/K2-014 projection path. This moves the projection seam beyond module-owned fixture keys while still staying fully read-only, local, deterministic, and fail-closed.

This is not filesystem source reading, not parser process spawning, not parser runtime/binary loading, not provider or Agent A behavior, not layout computation/trust, not renderer canvas behavior, not saved-view persistence, not source-coordinate truth, not multi-file SysML support, not RTM/`blk-link`, and not canonical SysML/KerML mutation.

## 2. Why this slice exists now

`K2-013` produced a fixture-backed read-only projection payload. `K2-014` added deterministic accepted view-intent parameter derivation for that path. The remaining Milestone D seam is to refresh the projection payload from bounded current model evidence rather than only from module-owned fixture keys.

The selected roadmap row for `K2-015` at target hash `68a9b8c0b9b056a9c8a80d8bae32c093ade4c8e6` names this exact boundary: accepted bounded model-snapshot/model-health evidence may refresh a sanitized read-only projection payload, without granting filesystem source reads, parser process/runtime loading, layout trust, persistence, Agent A/provider behavior, or canonical source mutation.

## 3. Direct requirement stance

Directly targeted by this slice:

- `REQ-KN-081` — projection from current canonical model state. K2-015 may treat accepted in-memory model-snapshot evidence as the current model evidence for a read-only refresh seam. It must not read canonical source files or claim broad canonical truth.
- `REQ-KN-082` — model truth and view-control state separation. K2-015 must keep accepted model snapshot evidence, view-intent parameters, and projection payload/view state explicitly separated and must not let caller-provided view/control data override model truth or authority flags.

Supporting/prepared only, not directly satisfied by this slice:

- `REQ-KN-039`, `REQ-KN-040`, `REQ-KN-041`, `REQ-KN-042`, and `REQ-KN-048` — projection read-path/payload/degradation/truncation behavior remains bounded support evidence unless directly exercised by the new model-refresh payload tests.
- `REQ-KN-077` — K2-015 consumes accepted view-intent parameters; it does not implement Agent A view-intent translation or provider request/response behavior.
- `REQ-KN-080` — K2-015 consumes K2-014 deterministic parameters as support; it does not broaden that derivation contract.
- `REQ-KN-083` — no-anchor degraded projection behavior remains supporting evidence; K2-015 must preserve it when model snapshots lack usable anchors.
- `REQ-KN-084` — local project/package contents remain supporting only; K2-015 does not persist local project state or saved views.
- `REQ-KN-107` — layout failure degraded view remains supporting only; K2-015 must not call, trust, or simulate a layout engine.

## 4. Architecture/readiness guidance

This slice follows:

- `docs/roadmaps/K2_product-convergence-map.md` — Milestone D, Projection / view compartment, one-authority-boundary rule.
- `docs/roadmaps/K2_implementation-roadmap.md` — explicit K2-015 selection at target hash `68a9b8c0b9b056a9c8a80d8bae32c093ade4c8e6`.
- `docs/process/K2_iteration-drift-protection.md` — exact selection source, vocabulary drift guard, validator lifecycle, and split trigger.
- `docs/traceability/K2_traceability.yaml` — closed evidence through K2-014 and verification conventions.
- `KVA-004` C4 component model and `KVA-005` invariants — projection/model-health/read-only boundary context.
- `RTF-KVA-007` / `SM-KVA-010` / `ICD-KVA-011` — view-intent, projection, degraded/stale/discarded state context as guidance only.
- `BEO-K2-014` — existing deterministic view-intent parameter derivation and denied adjacent authority list.

## 5. Allowed product changes

The route may modify only these existing files:

- `package.json`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`
- `src/shared/foundation.ts`
- `src/main/main.ts`
- `src/shared/projection-payload.mjs`

The route may create only these new files:

- `src/shared/model-projection-refresh.mjs`
- `tests/model-projection-refresh.test.mjs`

No other source, docs, lockfiles, generated outputs, dependency artifacts, package-manager files, parser assets, renderer UI files, preload IPC files, workspace/project inspection files, provider modules, candidate-staging modules, parser/model-health modules, existing tests outside the allowlist, existing K2 artifacts, or Obsidian files are authorized by this drop.

## 6. Required implementation behavior

Implement a deterministic model/projection refresh module at `src/shared/model-projection-refresh.mjs` with tests in `tests/model-projection-refresh.test.mjs`. The module may also add the smallest export needed in `src/shared/projection-payload.mjs` so accepted in-memory model snapshots can reuse the existing projection-payload sanitization, counts, warnings, bounds, and denied-authority semantics.

Required exported public vocabulary for the new module:

- `MODEL_PROJECTION_REFRESH_STATES`
- `MODEL_PROJECTION_REFRESH_WARNING_REASONS`
- `MODEL_PROJECTION_REFRESH_BOUNDS`
- `MODEL_PROJECTION_REFRESH_CAPABILITY_ID`
- `MODEL_PROJECTION_REFRESH_METHODS`
- `refreshReadOnlyProjectionFromModelSnapshot(input)`
- `createModelProjectionRefreshViewModel(input)`
- `createModelProjectionRefreshCapability(input)`

Required exported public vocabulary added to `src/shared/projection-payload.mjs`:

- A bounded function such as `createProjectionPayloadFromAcceptedModelSnapshot(input)` or an equivalent exact name chosen by Codex and confined by the validator.
- The new export must build the same public read-only projection payload shape as `createFixtureBackedProjectionPayload`, but from accepted in-memory model snapshot data rather than from module-owned fixture keys.

Public states must include exact auditable vocabulary for ready, degraded, empty/no-anchor, blocked/unresolved-anchor, truncated, malformed, stale/discarded, and unknown/fail-closed conditions. Public outputs must be immutable/deep-frozen and sanitized. They may expose stable state/category, bounded model snapshot summary, model-health state, view-intent parameter summary, sanitized projection payload, warning reasons, counts, and explicit false denied-authority flags. They must not expose raw source/model text, raw Agent A/provider output, prompts, credentials, raw diagnostics, raw filesystem paths, source coordinates, stack traces, support/export payloads, telemetry, mutation/write/import/promotion claims, or mutable handles.

The refresh must be deterministic and pure. Caller-supplied functions, getters/proxies that throw, parser/provider/layout functions, raw graph/layout payloads, canonical source objects, diagnostic arrays, filesystem objects, safe-mutation claims, authority flags, paths, or provider payloads must not be invoked or trusted. K2-015 may use fixed module-owned normalization tables only. It must preserve K2-013 projection payload bounds and K2-014 view-intent parameter compatibility without modifying unrelated modules.

Expected internal behavior:

1. Accept only a tiny structured input such as `{ modelSnapshot, modelHealth, viewIntent }` or `{ acceptedModelSnapshot, modelHealth, viewIntentParameters }` where the model snapshot is an in-memory object containing bounded `nodes` and `edges` arrays with stable IDs/labels/kinds/anchors.
2. Accept direct and wrapper input shapes for the already-accepted model snapshot path; unsupported wrappers fail closed.
3. Evaluate model-health evidence using existing model-health semantics or a bounded equivalent: healthy/recovered/degraded may refresh read-only payloads, while malformed/invalid/unsafe/unknown must produce degraded/fail-closed payload/status with all mutation/trust flags false.
4. Derive or consume K2-014-compatible view-intent parameters, but do not invoke Agent A/provider behavior.
5. Sanitize model nodes/edges, enforce unique node IDs, valid edge endpoints, max node/edge/string/warning counts, anchor availability, and deterministic ordering.
6. Return ready projection payload only when model snapshot, model-health evidence, and accepted view-intent parameters are mutually consistent.
7. Return empty/degraded/blocked/truncated/malformed/stale/discarded states for empty model, no anchor, unresolved anchor, oversized model, duplicate node IDs, missing edge endpoints, stale/discarded model evidence, contradictory health/view/model flags, callable fields, hostile accessors/proxies, raw markers, unsupported shapes, or denied adjacent authority fields.
8. Keep every adjacent authority false: Agent A/provider behavior, provider request/response handling, filesystem source reads, source hashing, directory scans, parser execution/process/runtime loading, projection engine trust, graph traversal engine trust, layout engine trust, render/canvas trust, source coordinates, canonical mutation, source repair, import/promotion/adoption, saved-view persistence, save/export/session persistence, support export, telemetry, RTM/`blk-link`, and BEO publication/storage/ledger.

## 7. Pre-dispatch adversarial readiness card

Slice: K2-015 — Live read-only model/projection refresh.
Milestone: D — First read-only useful projection.
Compartment: Projection / view, with parser/model-health evidence as support input only.
One authority boundary: accepted bounded model-snapshot/model-health evidence may refresh a sanitized read-only projection payload; it does not grant filesystem source reads, parser process/runtime loading, layout trust, persistence, Agent A/provider behavior, or canonical source mutation.
Direct requirements: `REQ-KN-081`, `REQ-KN-082`.
Supporting-only requirements: `REQ-KN-039`, `REQ-KN-040`, `REQ-KN-041`, `REQ-KN-042`, `REQ-KN-048`, `REQ-KN-077`, `REQ-KN-080`, `REQ-KN-083`, `REQ-KN-084`, `REQ-KN-107`.
Explicitly denied capabilities: Agent A/provider lifecycle, provider request/response handling, raw Agent A/provider output acceptance, canonical SysML/KerML generation, filesystem source-body reads, source-file hashing, directory scans, project/package writes, parser process spawning, parser runtime/binary loading, dependency/package-manager changes, source-coordinate truth claims, full SysML/KerML correctness claims, projection engine trust, graph traversal engine trust, layout engine geometry/trust, renderer canvas rendering, saved-view persistence, external-edit adoption/import/promotion, canonical SysML/KerML mutation, source/model repair, save/export/session persistence, support-bundle export, telemetry/upload, RTM generation, production `blk-link`, BEO publication/signing/storage/ledger.
Malformed input behavior: non-object, missing model snapshot, unknown/unsafe/malformed model health, no anchor, unresolved anchor marker, duplicate node IDs, missing edge endpoints, oversized node/edge/string/payload, callable/function-valued object, hostile getter/proxy, raw-marker-heavy fields, contradictory ready/error/trusted claims, path/source/provider/parser/graph/layout fields, and unsupported shapes return sanitized fail-closed/degraded/truncated payload/status with all denied authority flags false.
Contradictory input behavior: caller-supplied `state`, `projectionReady`, `payloadTrusted`, `modelTruthTrusted`, `fullyTrustedProjection`, `canonicalMutationAllowed`, `layoutTrustAllowed`, `renderTrustAllowed`, `safeMutationAllowed`, `providerAccessAuthorized`, `agentAViewIntentTranslationAuthorized`, graph/layout payloads, diagnostics, source/model text, parser runtime handles, or provider payloads must not override module-owned validation.
Spoofing seams to forbid: no caller-supplied projection function, graph traversal function, layout function, parser function, provider function, filesystem object, runtime adapter, raw graph payload, raw layout payload, model-health function, source-coordinate object, canonical source object, renderer bridge, preload bridge, provider payload, or Agent A output object may drive the result.
Raw/leaky fields to forbid: raw source text, canonical SysML/KerML text, raw model payload, parser input, source snippets, path/filename/line/column coordinates, stack traces, raw diagnostics, raw graph/layout payloads, provider prompts/responses, credentials, support/export payloads, telemetry, mutable handles.
Required hostile probes: same accepted model snapshot/view intent derives identical payload twice; direct accepted ready input and wrapper accepted ready input both return ready payload; healthy/recovered/degraded health preserves read-only refresh semantics while unsafe/invalid/malformed health fails closed; no-anchor snapshot produces empty/degraded warning payload; unresolved-anchor view intent produces blocked/degraded warning payload; oversized node/edge/string/payload returns truncated/circuit-breaker warning and bounded fields; duplicate node IDs and missing edge endpoints fail closed; contradictory caller authority/model-truth fields fail closed; caller functions are not invoked; hostile getters/proxies fail closed; raw marker strings in source/model/path/credential/provider/parser/graph/layout fields do not leak; public output/capability shape is exact and frozen/deep-frozen; public getter is an arrow function/frozen handle with no mutable own `.prototype`; validator scan confines K2-015 vocabulary; no fs/path/process/provider/parser/import/export/save/canonical mutation/source-coordinate/layout-engine behavior.
Closeout docs/mirrors to update after implementation: `BEO-K2-015`, `docs/traceability/K2_traceability.yaml`, `docs/roadmaps/K2_implementation-roadmap.md`, Obsidian BEB/BEO view copies, Obsidian roadmap/trace mirrors, and `BDOC-K2-015` support folder only if remediation/pending-template support docs are needed.

## 8. Validator requirements

Update `scripts/validate-foundation.mjs` to:

- add K2-015 comments, constants, required files, boundary marker files, no-authority field files, and helper-vocabulary confinement gates;
- update `EXACT_SCRIPTS.test` so `tests/model-projection-refresh.test.mjs` runs after `tests/view-intent-parameters.test.mjs` and before `tests/candidate-staging.test.mjs`;
- add K2-015 expected states, warning reasons, public names, method names, and required hostile test-token gates;
- require the new module/test and the projection-payload snapshot export to carry `K2-015` and `NO_PRODUCT_BEHAVIOR_K2_001` boundary markers;
- confine K2-015 helper vocabulary to `src/shared/model-projection-refresh.mjs`, `tests/model-projection-refresh.test.mjs`, `src/shared/projection-payload.mjs`, and exact allowed descriptor/import sites in `src/main/main.ts` / `src/shared/foundation.ts` / foundation tests;
- preserve existing no-filesystem, no-path, no-process, no-provider, no-parser, no-source-coordinate, no-layout-engine, no-renderer-canvas, no-import/export/persistence, no-support-export, no-canonical-mutation, and no-generated-artifact gates outside exact allowed files.

## 9. Required tests / RED-GREEN evidence

Use strict TDD:

1. Add `tests/model-projection-refresh.test.mjs` first and run `node tests/model-projection-refresh.test.mjs`; the RED failure should be missing module/export or missing behavior.
2. Implement `src/shared/model-projection-refresh.mjs` and the minimal `src/shared/projection-payload.mjs` snapshot-export change.
3. Rerun `node tests/model-projection-refresh.test.mjs` to GREEN.
4. Update `package.json`, `scripts/validate-foundation.mjs`, `tests/foundation.test.mjs`, `src/shared/foundation.ts`, and `src/main/main.ts` only as needed for K2-015 static metadata, validation, and descriptor wiring.
5. Run required verification commands.

Tests must cover at least:

- same accepted model snapshot + view intent -> identical deterministic refreshed payload across two calls;
- direct accepted ready input and wrapper accepted ready input -> `ready`, bounded projection payload, read-only refresh flags, all denied authority false;
- healthy/recovered/degraded model-health evidence -> read-only refresh semantics with model-health state preserved and mutation/trust denied;
- unsafe/invalid/malformed/unknown model-health evidence -> fail-closed/degraded/blocked semantics, not ready/trusted;
- no-anchor model snapshot -> empty/degraded no-anchor warning, not ready/trusted;
- unresolved-anchor view-intent parameters -> blocked/degraded warning, not ready/trusted;
- oversized node/edge/string/payload -> truncated/circuit-breaker warning and bounded fields;
- duplicate node IDs, missing edge endpoints, non-object, missing snapshot, function-valued fields, hostile getters/proxies, symbol-keyed inputs, and contradictory caller authority/model-truth fields fail closed or are ignored;
- caller-supplied projection/layout/parser/provider/model-health functions are not invoked;
- raw marker strings in source/model/path/credential/provider/diagnostic/parser/graph/layout fields do not leak;
- public result/capability shape is exact and frozen/deep-frozen;
- no network/env/filesystem/process/package-manager access and no canonical mutation/import/export/save/provider/Agent A/layout-engine behavior;
- K2-013 fixture-backed payload compatibility continues to pass and the new snapshot payload builder does not weaken fixture-key validation.

## 10. Verification commands

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

## 11. BEO closeout obligations

The final `BEO-K2-015` must record exact files changed, feature commit, selection target hash, BEB/L2/drop/pending-BEO/final-BEO hashes, Codex final-message path and SHA-256, route log/status when available, RED/GREEN/final verification output, hostile-review verdict, denied-authority confirmation, residual blockers/watch items, and mirror/trace/roadmap update status. If Codex self-reports commit failure but live Git shows BLK-pipe committed, treat live Git as the commit authority and explain the discrepancy.

## 12. blk-link / RTM stance

K2-015 may produce product implementation evidence for later metadata-only trace closure, but this drop does not run `blk-link`, generate an RTM, claim coverage truth, reject drift, read/scan/hash protected requirement bodies, publish/sign/store/ledger a BEO, or grant reusable dispatch authority.

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
