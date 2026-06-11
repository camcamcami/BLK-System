---
beb_id: "BEB-K2-018"
beo_id: "BEO-K2-018"
l2_id: "L2-K2-018"
remediation_id: "K2-018-R3-remediation-002"
model: "gpt-5.5"
reasoning_effort: "xhigh"
route: "BEB-L2 -> BLK-pipe -> Codex workspace-write"
target_hash: "ada7332df3cd092e2f1f27b47c7d5613454ec13a"
parent_feature_commit: "ada7332df3cd092e2f1f27b47c7d5613454ec13a"
trace_artifacts:
  - kind: "prior_remediation_patch"
    id: "K2-018-R2-REMEDIATION-PATCH"
    version_hash: "sha256:c7c7e332f240e115279b66508def8a41a18019e78cbbba2c2b17fcd8ade587b0"
  - kind: "prior_codex_final_message"
    id: "K2-018-R2-CODEX-FINAL-MESSAGE"
    version_hash: "sha256:8cc96926b66f35edca5274990788b08dc4798e6487a9dde715aa6e20d2af5beb"
  - kind: "prior_route_report"
    id: "K2-018-R2-ROUTE-REPORT"
    version_hash: "sha256:8a71fd1c825b79d1e4af90d8f3e2ab7c15e976d9482e0cfbdbcabeb5d52e2824"
---
# BEB-K2-018 Remediation 002 — Trap-Safe Denied-Authority Fail Closed

## Objective

Close the residual K2-018 R2 hostile-review blocker: descriptor/ownKeys proxy traps on `panel.deniedAuthorities` can throw out of `hasExactProjectionPanelPresentationDeniedAuthorityEvidence` instead of returning an untrusted fail-closed presentation. Descriptor and key introspection must be trap-safe.

## Authority boundary

This is a narrow K2-018 fail-closed hardening patch only. It does not authorize product behavior, canvas/SVG/ELK/JointJS/layout trust, filesystem source reads, parser/provider expansion, saved-view persistence, Agent A/provider behavior, import/export, canonical mutation, telemetry/network, RTM/`blk-link`, or BEO publication/storage/ledger.

## Allowed modified files

- `src/renderer/App.tsx`
- `tests/renderer-projection-panel-presentation.test.mjs`
- `scripts/validate-foundation.mjs`

No new files and no other files may be modified.

## Acceptance criteria

- `hasExactProjectionPanelPresentationDeniedAuthorityEvidence` catches descriptor/key introspection failures and returns false.
- A hostile proxy whose `ownKeys`, `getOwnPropertyDescriptor`, or other descriptor introspection path throws must not escape import/presentation construction.
- The public presentation must remain frozen, untrusted/fail-closed, and must not serialize the hostile raw key/value.
- Focused tests include the proxy trap case and prove no raw marker leakage.
- Validator K2-018 tokens require the trap-safe evidence/probe terms.

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
git diff --check -- src/renderer/App.tsx tests/renderer-projection-panel-presentation.test.mjs scripts/validate-foundation.mjs
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

