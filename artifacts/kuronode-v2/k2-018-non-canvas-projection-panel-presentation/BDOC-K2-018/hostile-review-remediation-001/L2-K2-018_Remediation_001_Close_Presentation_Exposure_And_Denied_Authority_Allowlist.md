L2_ID: L2-K2-018
BEB_ID: BEB-K2-018
BEO_ID: BEO-K2-018
REMEDIATION_ID: K2-018-R2-remediation-001
MODEL: gpt-5.5
REASONING_EFFORT: xhigh
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write
TARGET_HASH: d93473deada433bdfd49df7a686b52a423ef4b29

# L2-K2-018 Remediation 001 — Close Presentation Exposure and Denied-Authority Allowlist

## Mission

Patch exactly the two hostile-review blockers from K2-018 R1. Keep the implementation minimal and test-driven. Do not add new user behavior beyond narrowing renderer exposure and closing denied-authority rows over the fixed approved catalog.

## Allowed files

Modify only:

- `src/renderer/App.tsx`
- `src/renderer/main.tsx`
- `tests/renderer-projection-panel-presentation.test.mjs`
- `scripts/validate-foundation.mjs`

No new files.

## Required implementation details

1. In `src/renderer/main.tsx`, export `rendererFoundation` with exact keys `process` and `projectionPanelPresentation`. Do not expose `app` or a separate `projectionPanelMarkup`; the markup is already inside the frozen presentation object.
2. In `src/renderer/App.tsx`, close denied-authority rows over the existing `projectionPanelDeniedAuthorityFields` catalog. Do not use caller/object key enumeration as the output row catalog.
3. Add exact denied-authority evidence checking: missing keys, extra keys, accessor descriptors/getters, and non-false values must make the presentation fail closed/untrusted without serializing the unexpected key.
4. Update the focused test to prove the two blocker fixes, including an injected extra raw/leaky key (for example `sourceText`) that cannot appear in presentation rows or markup.
5. Update foundation validator K2-018 token gates to require the new exact allowlist closure/probe terms and remove `projectionPanelMarkup` as a required token.

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
git diff --check -- src/renderer/App.tsx src/renderer/main.tsx tests/renderer-projection-panel-presentation.test.mjs scripts/validate-foundation.mjs
```

## Final response requirements

Report the RED/GREEN or focused remediation evidence, verification outputs, exact changed files, final remediation commit hash, and a hostile-review-focused explanation of how both blockers are closed. Explicitly state that no denied adjacent authorities were added and no final BEO publication/storage/ledger occurred.

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

