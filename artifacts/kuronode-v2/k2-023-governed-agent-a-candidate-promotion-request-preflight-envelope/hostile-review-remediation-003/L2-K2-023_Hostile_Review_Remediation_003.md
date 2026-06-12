L2_ID: L2-K2-023
BEB_ID: BEB-K2-023
BEO_ID: BEO-K2-023
MODEL: gpt-5.5
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write

Implement only hostile-review remediation 003 for K2-023.

TDD sequence:
1. Add failing tests in `tests/agent-a-promotion-request.test.mjs` for:
   - `readiness.blockedReasons` as `new Proxy([], { get(...) { throw or increment } })` does not execute traps and yields a blocked envelope.
   - provider-called `contentFingerprint` as an object with `toString` does not execute/coerce and does not appear in `candidateContentFingerprint` or serialized output.
2. Run `node tests/agent-a-promotion-request.test.mjs` and capture RED.
3. Patch only `src/shared/agent-a-promotion-request.mjs`.
   - Avoid `.length`/ordinary property reads on caller-owned readiness arrays before they are descriptor-safe; use descriptors or fail closed.
   - Require `typeof contentFingerprint === "string"` before regex testing in all branches; non-string returns `unavailable` and adds malformed-fingerprint evidence as appropriate.
   - Do not introduce filesystem/network/provider/parser/runtime calls.
4. Rerun focused and full verification.

Regression requirements:
- Prior array getter hostile probes remain blocked/inert.
- Exact nested `blk-link` remains blocked.
- Own enumerable `__proto__` object/array evidence changes hash or fails closed; it must not alias clean readiness while reviewable.
- Safe readiness records retain deterministic stable hashes.

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

Final response must include the RED excerpt, GREEN outputs, exact changed files, final commit hash, and explicit no-adjacent-authority confirmation.

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
