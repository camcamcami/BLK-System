L2_ID: L2-K2-026
BEB_ID: BEB-K2-026
BEO_ID: BEO-K2-026
MODEL: gpt-5.5
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write
REMEDIATION: R5 exact verified patch replay from hash-bound package file
PATCH_PATH: /home/dad/BLK-System/artifacts/kuronode-v2/k2-026-governed-post-transaction-readiness-refresh-gate-r5-external-patch-file/BDOC-K2-026_R5_verified_exact_patch.diff
PATCH_SHA256: sha256:e7ea3f0f193c0821d16a95e486e4f047302c7d1e84961c8aab41dd755baeb99b
PATCH_BYTES: 49362

You are Codex executing the exact `BEB-K2-026` package through BLK-System.

R5 is **not** exploratory. Do not reimplement from scratch. Do not paste the patch into a heredoc. Use the existing patch file path directly:

`/home/dad/BLK-System/artifacts/kuronode-v2/k2-026-governed-post-transaction-readiness-refresh-gate-r5-external-patch-file/BDOC-K2-026_R5_verified_exact_patch.diff`

Run these exact steps:

```bash
git rev-parse HEAD
git status --porcelain=v1
sha256sum /home/dad/BLK-System/artifacts/kuronode-v2/k2-026-governed-post-transaction-readiness-refresh-gate-r5-external-patch-file/BDOC-K2-026_R5_verified_exact_patch.diff
test "$(sha256sum /home/dad/BLK-System/artifacts/kuronode-v2/k2-026-governed-post-transaction-readiness-refresh-gate-r5-external-patch-file/BDOC-K2-026_R5_verified_exact_patch.diff | awk '{print "sha256:" $1}')" = "sha256:e7ea3f0f193c0821d16a95e486e4f047302c7d1e84961c8aab41dd755baeb99b"
git apply --check /home/dad/BLK-System/artifacts/kuronode-v2/k2-026-governed-post-transaction-readiness-refresh-gate-r5-external-patch-file/BDOC-K2-026_R5_verified_exact_patch.diff
git apply /home/dad/BLK-System/artifacts/kuronode-v2/k2-026-governed-post-transaction-readiness-refresh-gate-r5-external-patch-file/BDOC-K2-026_R5_verified_exact_patch.diff
node tests/governed-post-transaction-readiness-refresh.test.mjs
node tests/governed-write-transaction.test.mjs
node tests/foundation.test.mjs
node scripts/validate-foundation.mjs
npm test
npm run build
npm run typecheck
git diff --check -- package.json scripts/validate-foundation.mjs src/shared/foundation.ts src/shared/governed-post-transaction-readiness-refresh.mjs tests/foundation.test.mjs tests/governed-post-transaction-readiness-refresh.test.mjs
```

If the patch file is inaccessible from the sandbox, stop and report that exact file-access failure; do not improvise a different implementation.

Allowed modified files:
- `package.json`
- `scripts/validate-foundation.mjs`
- `src/shared/foundation.ts`
- `tests/foundation.test.mjs`

Allowed new files:
- `src/shared/governed-post-transaction-readiness-refresh.mjs`
- `tests/governed-post-transaction-readiness-refresh.test.mjs`

Authority boundary: this R5 package grants no provider call, parser/runtime execution, filesystem/source writes beyond the exact patch files, renderer/IPC expansion, BEO publication, RTM generation, production blk link, protected-body access, signer/storage/ledger action, or reusable BLK-pipe/Codex authority.

## Readiness profile probe card

These probes are required pre-dispatch checklist evidence only. They do not authorize source/Git mutation, parser execution, provider/runtime dispatch, BEO publication, RTM generation, or reusable BLK-pipe/Codex authority beyond the exact approved drop.

### kuronode-governed-write-transaction-v1

- [ ] KGWT-001 real K2-024 admission record produced by createAgentAWriteAdmissionRecord commits through the controlled fixture path
- [ ] KGWT-002 minimal or forged admission-shaped records fail closed before transaction commit
- [ ] KGWT-003 admission, promotion request, package, and transaction request identity/hash fields must match exactly
- [ ] KGWT-004 authority, approval, provider, publication, RTM, blk-link, save/export/session, and raw-marker aliases fail closed across admission/package/request metadata
- [ ] KGWT-005 target path, targetPaths, packagePaths, targetPackagePaths, files, absolute path, traversal, and multi-file aliases fail closed
- [ ] KGWT-006 stale before-version hash, candidate replacement hash mismatch, unsupported package kind, and missing operator review evidence return commit-failed no-op recovery
- [ ] KGWT-007 hostile JavaScript objects, proxies, getters, accessors, symbols, functions, revoked proxies, and cyclic evidence fail closed without invoking caller code
- [ ] KGWT-008 transaction IDs, recovery records, denied-authority flags, and evidence hashes are deterministic, deep-frozen, and leak no raw prompt/source/provider/path/body material
- [ ] KGWT-009 readiness-refresh-required evidence is recorded without running RTM, blk-link, provider, filesystem write, publication, signing, storage, or ledger side effects
- [ ] KGWT-010 closeout includes a named hostile matrix for admission spoofing, package/request aliases, raw-marker non-leakage, and commit-or-fail/no-op recovery
