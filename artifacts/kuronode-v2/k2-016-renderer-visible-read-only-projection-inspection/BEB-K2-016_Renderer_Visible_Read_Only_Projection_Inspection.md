---
beb_id: "BEB-K2-016"
beo_id: "BEO-K2-016"
l2_id: "L2-K2-016"
model: "gpt-5.5"
reasoning_effort: "xhigh"
route: "BEB-L2 -> BLK-pipe -> Codex workspace-write"
target_repo: "/home/dad/code/Kuronode-v2"
target_branch: "main"
target_hash: "78361d71d78b543c444664dc2242eec80d8c1b38"
trace_artifacts:
  - kind: "product_convergence_map"
    id: "K2-PRODUCT-CONVERGENCE-MAP"
    version_hash: "sha256:bc70f88549b0939395495861a3797d4d42fcf72b584926927712700c00c69cb9"
  - kind: "roadmap"
    id: "K2-IMPLEMENTATION-ROADMAP"
    version_hash: "sha256:ae08f74613df5df88b21f11f1d8ea2e2ed00e8c9808325c7e15598bba9c8823f"
  - kind: "process_guard"
    id: "K2-ITERATION-DRIFT-PROTECTION"
    version_hash: "sha256:a2acedfa31dae7134298c39b0f7ec7ee9c47e79cd0d54179cd28a3f3fb76a393"
  - kind: "traceability_index"
    id: "K2-TRACEABILITY-MANIFEST"
    version_hash: "sha256:f399a83b18ffa79bde517b0616ec33b949df1e4b8cf0defe4c4360fa375e154e"
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
    id: "BEO-K2-015"
    version_hash: "sha256:cb6222729e605155b56cd25e4a26f3d7a830b2dd69e8a84c4ea6699133aff0a8"
---
# BEB-K2-016 — Renderer-Visible Read-Only Projection Inspection

## 1. Executive intent / plain-English goal

Make the read-only projection refresh work delivered by `K2-015` visible to the Kuronode renderer/App view model. A user or tester should be able to inspect the currently exposed projection refresh state in the renderer-facing model: capability ID/method metadata, refresh state, payload counts, visible warning reasons, read-only/trust flags, and sanitized visible node/edge summaries. This slice is read/projection UI inspection only. It is not canvas rendering, layout computation, saved-view persistence, filesystem source reading, parser execution, Agent A/provider behavior, import/promotion, export, or canonical SysML/KerML mutation.

## 2. Why this slice exists now

`K2-015` produced a bounded in-memory refresh seam: accepted model snapshot evidence plus model-health status can produce a sanitized K2-013-compatible projection payload. That seam is still mostly invisible from `src/renderer/App.tsx`; the renderer currently exposes provider/workspace/parser/model-health/projection status metadata only. `K2-016` advances Milestone D by making the existing projection payload inspectable in the app-facing model before any higher-risk canvas, layout, saved-view, import, or AI-candidate generation work.

## 3. Direct product requirement stance

- `REQ-KN-081` is directly advanced at the read-only inspection level: the renderer-visible projection inspection must derive from the current accepted in-memory model snapshot and accepted projection parameters already handled by K2-015, rather than from stale hard-coded rendered graph state.
- `REQ-KN-082` is directly advanced: the view model must keep canonical model truth separate from view/presentation state and must not add persistence or mutation authority.
- `REQ-KN-083` is directly advanced for visible degraded/empty warning behavior: no-anchor/unresolved-anchor/empty/degraded states must remain visible through warning reasons and readiness flags.

This slice does not claim full production rendering, layout correctness, canonical SysML truth, saved-view behavior, or RTM trace closure.

## 4. Supporting / prepared requirement stance

The following requirements remain supporting/prepared only for this slice: `REQ-KN-039`, `REQ-KN-040`, `REQ-KN-041`, `REQ-KN-042`, `REQ-KN-048`, `REQ-KN-077`, `REQ-KN-080`, `REQ-KN-084`, and `REQ-KN-107`. They inform warning/degraded/read-only/bounded-payload semantics but are not fully closed by a renderer App inspection surface.

## 5. Architecture and readiness guidance

Use the hash-bound trace artifacts in this BEB as fixed context. The implementation must stay within the Projection / view compartment. It may consume the existing K2-015 shared refresh capability; it must not open a new privileged IPC, preload, filesystem, parser, provider, runtime, layout, save/export, or package-management seam. The renderer may display or expose a sanitized summary derived from the K2-015 result, but must not accept caller-controlled source text, file paths, graph/layout engines, provider payloads, diagnostics, credentials, or mutation/trust claims.

## 6. Exact implementation scope

Allowed modified files:

- `package.json`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`
- `src/shared/foundation.ts`
- `src/renderer/App.tsx`

Allowed new files:

- `tests/renderer-projection-inspection.test.mjs`

No other files may be modified or created by the implementation commit. In particular, do not modify docs, lockfiles, generated outputs, dependencies, parser assets, main/preload IPC files, local filesystem inspection files, existing projection payload/refresh modules, view-intent modules, candidate staging modules, provider modules, or existing tests outside the allowlist.

## 7. Required renderer-visible behavior

`src/renderer/App.tsx` must expose a deterministic `projectionInspection` (or equivalently named, test-bound) entry on `appViewModel` that is derived from `createModelProjectionRefreshCapability` / `getModelProjectionRefresh` using a bounded module-owned accepted in-memory model snapshot. The inspection entry must expose only sanitized summary/metadata:

- capability ID `model-projection-refresh`;
- capability method names and renderer/client-visible method metadata;
- refresh `state` and `warningReasons`;
- projection payload `counts`;
- sanitized visible node/edge summaries from `projectionPayload.nodes` / `projectionPayload.edges` if present, bounded by the existing payload bounds;
- `modelProjectionRefreshReady`, `acceptedModelSnapshotRefreshed`, `readOnlyModelProjectionRefresh`, `boundedModelProjectionRefresh`, and `modelProjectionRefreshTrusted` flags;
- explicit denied-authority flags must remain false for filesystem reads, parser execution, graph/projection/layout trust, render trust, source coordinates, canonical mutation, source repair, Agent A/provider behavior, import/adoption, saved-view persistence, save/export/session persistence, support export, telemetry, Electron IPC/preload/renderer filesystem expansion, dependency changes, RTM/`blk-link`, and BEO publication/storage/ledger.

The public `appViewModel` and projection inspection object must be frozen/deep-frozen enough that tests cannot mutate the exposed inspection metadata. Do not expose raw source/model text, diagnostic arrays, paths, coordinates, stack traces, prompts, credentials, provider payloads, support/export payloads, telemetry, functions other than the already frozen getter internally used to derive the summary, or mutable handles.

## 8. Required TDD sequence

1. Create `tests/renderer-projection-inspection.test.mjs` first.
2. Run `node tests/renderer-projection-inspection.test.mjs` and record RED because `App.tsx` does not yet expose K2-016 projection inspection.
3. Implement the smallest renderer/App changes needed to pass the focused test.
4. Update `package.json`, `scripts/validate-foundation.mjs`, `tests/foundation.test.mjs`, and `src/shared/foundation.ts` only as needed to register K2-016 metadata, exact scripts, validator gates, helper-vocabulary confinement, and slice boundary text.
5. Rerun the focused test to GREEN, then run the full verification commands.

## 9. Required tests and validator gates

Cover at least:

- `appViewModel.projectionInspection` exists and is deterministic across two reads;
- inspection state/warnings/counts come from a K2-015 refresh result, not from duplicated stale literals;
- no-anchor/degraded warning reasons are visible when the renderer-owned sample has no matching anchors, or a ready sample is visible when an anchor is supplied;
- capability ID and method metadata are visible without exposing privileged IPC/preload/raw filesystem authority;
- all denied-authority flags exposed by the inspection remain `false`;
- sanitized node/edge summaries are bounded and do not include raw source/model/path/provider/diagnostic/credential/telemetry markers;
- exposed inspection objects are frozen and cannot be mutated;
- the K2-015 refresh helper vocabulary is allowed in `src/renderer/App.tsx` only for this K2-016 inspection path and remains confined elsewhere;
- package scripts include the new focused test in `npm test` without adding dependencies.

## 10. Verification commands

Run and leave exact output evidence:

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

## 11. Acceptance criteria

- Focused K2-016 test shows RED before implementation and GREEN after implementation.
- `npm test`, `npm run build`, and `npm run typecheck` pass.
- The implementation commit changes only the allowed files.
- No dependencies, lockfiles, generated outputs, parser/runtime assets, filesystem reads, provider calls, IPC expansion, persistence, import/export, canonical mutation, or BEO/RTM/`blk-link` behavior are introduced.
- Hostile review has no blockers for raw leakage, helper-vocabulary drift, mutable public handles, authority laundering, stale roadmap/trace wording, or overclaiming product requirement closure.

## 12. `blk-link` / RTM stance

Metadata is prepared only. RTM generation and production `blk-link` are not authorized or performed by this slice. Protected requirement/body reads, source-body scans, coverage truth, drift rejection, BEO publication, signing, storage, and ledger actions remain denied.

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
