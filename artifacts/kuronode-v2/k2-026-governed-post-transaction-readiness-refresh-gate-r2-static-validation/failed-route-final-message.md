Implemented K2-026 with strict TDD.

RED was captured first: `node tests/governed-post-transaction-readiness-refresh.test.mjs` failed with `ERR_MODULE_NOT_FOUND` for the new shared module.

Changes made:
- Added pure-data readiness refresh gate: [src/shared/governed-post-transaction-readiness-refresh.mjs](/tmp/blk-system-clean-worktrees/kuronode-v2-k2-026-7cbb698bf7ad/src/shared/governed-post-transaction-readiness-refresh.mjs:1)
- Added KGRR-001 through KGRR-010 focused tests: [tests/governed-post-transaction-readiness-refresh.test.mjs](/tmp/blk-system-clean-worktrees/kuronode-v2-k2-026-7cbb698bf7ad/tests/governed-post-transaction-readiness-refresh.test.mjs:1)
- Updated `npm test`: [package.json](/tmp/blk-system-clean-worktrees/kuronode-v2-k2-026-7cbb698bf7ad/package.json:1)
- Updated K2-026 static classification/guardrails: [scripts/validate-foundation.mjs](/tmp/blk-system-clean-worktrees/kuronode-v2-k2-026-7cbb698bf7ad/scripts/validate-foundation.mjs:1), [tests/foundation.test.mjs](/tmp/blk-system-clean-worktrees/kuronode-v2-k2-026-7cbb698bf7ad/tests/foundation.test.mjs:1), [src/shared/foundation.ts](/tmp/blk-system-clean-worktrees/kuronode-v2-k2-026-7cbb698bf7ad/src/shared/foundation.ts:1)

Verification passed:
- `node tests/governed-post-transaction-readiness-refresh.test.mjs`
- `node tests/governed-write-transaction.test.mjs`
- `node tests/foundation.test.mjs`
- `node scripts/validate-foundation.mjs`
- `npm test`
- `npm run build`
- `npm run typecheck`

No generated artifacts, package lock, `dist`, or `node_modules` were created. No git commit was made.