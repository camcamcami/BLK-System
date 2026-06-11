L2_ID: L2-K2-018
BEB_ID: BEB-K2-018
BEO_ID: BEO-K2-018
REMEDIATION_ID: K2-018-R3-remediation-002
MODEL: gpt-5.5
REASONING_EFFORT: xhigh
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write
TARGET_HASH: ada7332df3cd092e2f1f27b47c7d5613454ec13a

# L2-K2-018 Remediation 002 — Trap-Safe Denied-Authority Fail Closed

## Mission

Patch exactly the residual R2 hostile-review blocker. Keep the change small and limited to denied-authority evidence introspection and its focused tests/validator tokens.

## Allowed files

Modify only:

- `src/renderer/App.tsx`
- `tests/renderer-projection-panel-presentation.test.mjs`
- `scripts/validate-foundation.mjs`

No new files.

## Required implementation details

1. Wrap denied-authority descriptor/key introspection in `try/catch` so hostile proxy traps return `false` from the exact-evidence helper instead of throwing.
2. Add a focused test that injects a proxy/trap denied-authority object and proves the module import/presentation creation does not throw, remains untrusted/fail-closed, and does not leak raw markers.
3. Update validator K2-018 token gates to require the trap-safe helper/probe terms.

## Verification commands

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

