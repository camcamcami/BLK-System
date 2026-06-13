L2_ID: L2-K2-025
BEB_ID: BEB-K2-025
BEO_ID: BEO-K2-025
MODEL: gpt-5.5
REASONING_EFFORT: xhigh
TARGET_HASH: 778c795ee7a423f4a6385c5720c689c2eeb78c8e

Objective: remediate the single remaining hostile-review blocker from R4. Package records containing path-list/alias fields must fail closed even if the alias is a singleton exact controlled path.

Critical route-control instruction: Do not run `git add`, `git commit`, `git reset`, `git checkout`, `git clean`, or any command that writes Git metadata. BLK-pipe owns staging, commit creation, cleanup, and route-summary evidence after you exit. After tests pass, write a concise final message and stop.

Required RED tests first in `tests/governed-write-transaction.test.mjs`:
- Package record `{ targetPaths: [CONTROLLED_FIXTURE_PACKAGE_PATH] }` blocks.
- Package record `{ packagePaths: [CONTROLLED_FIXTURE_PACKAGE_PATH] }` blocks.
- Package record `{ targetPackagePaths: [CONTROLLED_FIXTURE_PACKAGE_PATH] }` blocks.
- Package record `{ files: [CONTROLLED_FIXTURE_PACKAGE_PATH] }` blocks.
- Keep existing real K2-024 admission commit test and alias-denial tests green.

Implementation guidance:
- Remove or neutralize package-side support for `targetPaths`, `packagePaths`, `targetPackagePaths`, and `files` as accepted fields.
- If those fields appear anywhere in package evidence, add `unsupported-package-record` and/or `target-package-path-mismatch`; do not permit a commit.
- Preserve request-side alias blocking and all prior R4 hostile mitigations.

Verification commands:
- `node tests/governed-write-transaction.test.mjs`
- `node scripts/validate-foundation.mjs`
- `npm test`
- `npm run build`
- `npm run typecheck`
- `git diff --check -- src/shared/governed-write-transaction.mjs tests/governed-write-transaction.test.mjs scripts/validate-foundation.mjs`


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
