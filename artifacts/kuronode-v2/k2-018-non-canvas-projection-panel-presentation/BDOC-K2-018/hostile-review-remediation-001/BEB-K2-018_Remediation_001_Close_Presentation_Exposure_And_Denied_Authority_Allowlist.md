---
beb_id: "BEB-K2-018"
beo_id: "BEO-K2-018"
l2_id: "L2-K2-018"
remediation_id: "K2-018-R2-remediation-001"
model: "gpt-5.5"
reasoning_effort: "xhigh"
route: "BEB-L2 -> BLK-pipe -> Codex workspace-write"
target_hash: "d93473deada433bdfd49df7a686b52a423ef4b29"
parent_feature_commit: "d93473deada433bdfd49df7a686b52a423ef4b29"
blocked_review_source: "independent hostile review after BEB-K2-018 R1"
original_beb_sha256: "sha256:28e8a8cae16127f6413497e7f4888274c855ded5f8907fb201e78c12e8df6591"
original_l2_sha256: "sha256:15c6fcaefa1d89ffefcfb0ef159e115cf4e41d251ba841ba11cddd008b5933be"
original_drop_sha256: "sha256:2a940f546104ce8ad0115ecb17692a694981099381c7ba1cc92255df051daaae"
original_feature_commit: "d93473deada433bdfd49df7a686b52a423ef4b29"
trace_artifacts:
  - kind: "prior_feature_patch"
    id: "K2-018-R1-FEATURE-PATCH"
    version_hash: "sha256:0a132e2332a2ec23bb8a26332f72ce33b358358371a8cec04b0ad58f7c8a46de"
  - kind: "prior_codex_final_message"
    id: "K2-018-R1-CODEX-FINAL-MESSAGE"
    version_hash: "sha256:8901db4bd5784fbe1fd4230bba0919dddb176b91b0305bd0fbff6cba76f8716e"
  - kind: "prior_route_report"
    id: "K2-018-R1-ROUTE-REPORT"
    version_hash: "sha256:5be24700b2091fff07d8d43aded0bdb638d43f9bb2df54a1c81848e9670312af"
---
# BEB-K2-018 Remediation 001 — Close Presentation Exposure and Denied-Authority Allowlist

## Objective

Remediate the two K2-018 hostile-review blockers found after the route-produced feature commit `d93473deada433bdfd49df7a686b52a423ef4b29`:

1. `rendererFoundation` overexposes the full App view-model and a redundant raw markup string. It must expose only the renderer process marker plus the frozen `projectionPanelPresentation` object; markup remains reachable as `rendererFoundation.projectionPanelPresentation.markup`.
2. Projection presentation denied-authority rows are not closed over the approved catalog. Extra or missing denied-authority keys must fail closed and must never be mirrored into `deniedAuthorityRows`, markup, tests, or validator-approved behavior.

## Authority boundary

This remediation is K2-018 presentation-surface hardening only. It does not authorize new product behavior, canvas/SVG/ELK/JointJS/layout trust, saved-view persistence, filesystem source reads, parser/provider expansion, Agent A/provider behavior, candidate import/promotion, import/export, canonical mutation, telemetry/network, RTM/`blk-link`, BEO publication/storage/ledger, or future source/Git mutation outside this exact drop.

## Allowed modified files

- `src/renderer/App.tsx`
- `src/renderer/main.tsx`
- `tests/renderer-projection-panel-presentation.test.mjs`
- `scripts/validate-foundation.mjs`

No new files and no other modifications are authorized.

## Acceptance criteria

- `rendererFoundation` has exact public keys `process` and `projectionPanelPresentation` only.
- `rendererFoundation.projectionPanelMarkup` is removed; tests prove markup remains reachable as `rendererFoundation.projectionPanelPresentation.markup`.
- `rendererFoundation.app` is removed; tests prove the full App view-model is not re-exposed through the renderer entry surface.
- `createProjectionPanelPresentationDeniedAuthorityRows` maps only the fixed approved `projectionPanelDeniedAuthorityFields` catalog, never `Object.keys(panel.deniedAuthorities)`.
- Denied-authority evidence must be exact: missing keys, extra keys, getter/proxy-like descriptors, or any non-false value force fail-closed/untrusted presentation evidence without copying caller/source keys into markup.
- Tests include a negative probe that injects an extra raw/leaky denied-authority key such as `sourceText` and proves it does not appear in `deniedAuthorityRows` or markup.
- Validator tokens are updated so they require the exact allowlist-closure helper/probe terms and no longer require `projectionPanelMarkup`.

## Required verification

```bash
node tests/renderer-projection-panel-presentation.test.mjs
node tests/renderer-projection-panel.test.mjs
node tests/renderer-projection-inspection.test.mjs
node tests/model-projection-refresh.test.mjs
node scripts/validate-foundation.mjs
npm test
npm run build
npm run typecheck
git diff --check -- src/renderer/App.tsx src/renderer/main.tsx tests/renderer-projection-panel-presentation.test.mjs scripts/validate-foundation.mjs
```

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

