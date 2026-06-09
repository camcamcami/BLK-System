L2_ID: L2-K2-016
BEB_ID: BEB-K2-016
BEO_ID: BEO-K2-016
MODEL: gpt-5.5
REASONING_EFFORT: xhigh
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write
TARGET_HASH: cea9b29e539de74f7bbf49dbd49e4957b7e95cad
SUPPORT_ARTIFACT: BDOC-K2-016/hostile-review-remediation-001

# L2-K2-016 Remediation 001 — Freeze Renderer App View Model

## Mission

Fix only the hostile-review blocker in K2-016: the public `appViewModel` and `App()` output are mutable even though `projectionInspection` itself is deep-frozen. Keep the existing K2-016 read-only projection inspection behavior intact and do not expand authority.

## Allowed files

You may modify only:

- `src/renderer/App.tsx`
- `tests/renderer-projection-inspection.test.mjs`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`

You may create no new files. Do not modify package scripts, docs, lockfiles, generated outputs, dependencies, main/preload files, shared projection/refresh modules, provider/workspace/parser/model-health/projection modules, or K2 artifacts.

## Required RED/GREEN sequence

1. In `tests/renderer-projection-inspection.test.mjs`, add a failing regression for the current parent `cea9b29e539de74f7bbf49dbd49e4957b7e95cad`. It must prove `appViewModel` and `App()` output are frozen and that `projectionInspection` cannot be reassigned. It must also prove adjacent public nested metadata such as `appViewModel.boundary` is frozen/deep-frozen enough that `boundary.slice` cannot be changed.
2. Run `node tests/renderer-projection-inspection.test.mjs` and capture RED. Expected failure is equivalent to `appViewModel must be frozen` or inability to prevent reassignment/mutation.
3. Make the smallest code change in `src/renderer/App.tsx` to deep-freeze the exported public view model. Prefer wrapping the object assigned to `export const appViewModel` with the existing local `deepFreeze(...)`; adjust the helper only if required. Preserve deterministic public shape and current projection inspection fields.
4. Add/tighten `scripts/validate-foundation.mjs` and `tests/foundation.test.mjs` only if needed to require the new K2-016 freeze regression tokens. Do not weaken existing K2-015 helper-vocabulary confinement or authority scans.
5. Rerun the focused test to GREEN, then run every verification command below.

## Required verification commands

```bash
node tests/renderer-projection-inspection.test.mjs
node tests/model-projection-refresh.test.mjs
node tests/projection-payload.test.mjs
node scripts/validate-foundation.mjs
npm test
npm run build
npm run typecheck
git diff --check -- src/renderer/App.tsx tests/renderer-projection-inspection.test.mjs scripts/validate-foundation.mjs tests/foundation.test.mjs
```

## Authority constraints

All K2-016 denied authorities remain false/non-authorized: filesystem/source reads, parser execution/runtime loading, provider/Agent A behavior, IPC/preload/main expansion, graph/projection/layout/render trust, source coordinates, canonical mutation, source repair, import/adoption, saved-view persistence, save/export/session persistence, support export, telemetry, dependency changes, RTM/`blk-link`, BEO publication/storage/ledger, protected-body reads, source-body scans, coverage truth, and drift rejection.

## Final response requirements to BLK-System

Report RED output, GREEN focused output, full verification outputs, changed file list, remediation commit hash, and whether hostile-review blockers remain. If Codex cannot commit because of read-only `.git`, still leave the working tree staged/clean as BLK-pipe expects and report the exact failure; BLK-pipe will own final staging/commit if the route succeeds.

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
