L2_ID: L2-K2-023
BEB_ID: BEB-K2-023
BEO_ID: BEO-K2-023
MODEL: gpt-5.5
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write

Implement only the second hostile-review remediation for K2-023.

TDD sequence:
1. Add failing tests in `tests/agent-a-promotion-request.test.mjs` proving own enumerable `__proto__` readiness evidence cannot be silently omitted from `readinessEvidenceHash` while the envelope remains reviewable. Include object and array/snapshot special-key coverage for `__proto__`, `constructor`, or `prototype` as appropriate.
2. Re-run `node tests/agent-a-promotion-request.test.mjs` and capture RED.
3. Patch only `src/shared/agent-a-promotion-request.mjs`. Preferred fix: use null-prototype containers plus `Object.defineProperty` for canonical snapshot objects/properties, or encode object entries as deterministic arrays, so special keys are data, not prototype operations. Do not reintroduce `.map`/ordinary element getter execution.
4. Rerun focused and full verification.

Regression requirements:
- Prior array getter hostile probes remain blocked/inert.
- Exact nested `blk-link` remains blocked.
- Safe readiness records retain deterministic stable hashes.
- Hostile/special-key readiness evidence cannot produce the same evidence hash as clean readiness while remaining reviewable.

Verification commands:
- `node tests/agent-a-promotion-request.test.mjs`
- `node tests/agent-a-promotion-readiness.test.mjs`
- `node tests/agent-a-candidate-generation.test.mjs`
- `node tests/candidate-staging.test.mjs`
- `node scripts/validate-foundation.mjs`
- `npm test`
- `npm run build`
- `npm run typecheck`
- `git diff --check -- src/shared/agent-a-promotion-request.mjs tests/agent-a-promotion-request.test.mjs`

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
