L2_ID: L2-K2-023
BEB_ID: BEB-K2-023
BEO_ID: BEO-K2-023
MODEL: gpt-5.5
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write

Implement only the hostile-review remediation for K2-023.

TDD sequence:
1. Add failing tests in `tests/agent-a-promotion-request.test.mjs` for top-level readiness array getter execution, nested readiness array getter execution, and exact nested `blk-link` denied field names with non-marker values.
2. Run `node tests/agent-a-promotion-request.test.mjs` and capture RED showing the current implementation throws or fails to block.
3. Patch only `src/shared/agent-a-promotion-request.mjs` to avoid array `.map`/ordinary element property access during canonical snapshotting and to detect explicit `blk-link` denied fields.
4. Rerun K2-023 focused test to GREEN, then run compatibility and foundation checks.

Implementation constraints:
- Do not change public K2-023 vocabularies except if needed to add fixed existing blocked reasons already present.
- Do not modify package/foundation/validator metadata unless tests prove absolutely necessary; expected scope is only the K2-023 module and test.
- Use descriptor-based array/object snapshotting so hostile getters/callables/symbols/proxies are represented inertly and do not execute.
- Preserve deterministic `readinessEvidenceHash` for safe readiness records.
- Preserve all authority denial flags and no-product-behavior boundaries.

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

Final response must report RED excerpt, GREEN/full verification outputs, exact changed files, feature/remediation commit hash, and confirmation that no adjacent authority was added.

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
