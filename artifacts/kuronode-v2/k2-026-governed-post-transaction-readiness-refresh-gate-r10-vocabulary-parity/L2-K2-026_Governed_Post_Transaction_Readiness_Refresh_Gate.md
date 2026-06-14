L2_ID: L2-K2-026
BEB_ID: BEB-K2-026
BEO_ID: BEO-K2-026
MODEL: gpt-5.5
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write
REMEDIATION: R10 vocabulary parity exact patch replay
TARGET_HASH: cebe3d06b21b377f23adad0cf55f89d579dff804
PATCH_PATH: /home/dad/BLK-System/artifacts/kuronode-v2/k2-026-governed-post-transaction-readiness-refresh-gate-r10-vocabulary-parity/BDOC-K2-026_R10_vocabulary_parity_exact_patch.diff
PATCH_SHA256: sha256:7c434bf82237c1906a670815da9d735861a2f0e1aef0a0d9ff031bd06f9cb683
PATCH_BYTES: 1318
APPLY_HELPER_PATH: /home/dad/BLK-System/artifacts/kuronode-v2/k2-026-governed-post-transaction-readiness-refresh-gate-r10-vocabulary-parity/BDOC-K2-026_R10_apply_exact_patch_without_git.py
APPLY_HELPER_SHA256: sha256:289373520059ba5c6ec396161951e6650b40a8eddc38cb0475ab08e65602a0e0
APPLY_HELPER_BYTES: 976

You are Codex executing the exact `BEB-K2-026` R10 remediation package through BLK-System.

R10 is **not exploratory**. Do not reimplement from scratch. Do not paste the patch into a heredoc. Do not run any `git` command inside the engine: BLK-pipe already performed target-hash preflight and BLK-pipe owns Git validation, staging, and commit.

Run this exact non-Git apply step from the repository workdir:

```bash
python3 /home/dad/BLK-System/artifacts/kuronode-v2/k2-026-governed-post-transaction-readiness-refresh-gate-r10-vocabulary-parity/BDOC-K2-026_R10_apply_exact_patch_without_git.py
```

Then run only non-Git product validation commands:

```bash
node tests/governed-post-transaction-readiness-refresh.test.mjs
node tests/governed-write-transaction.test.mjs
node tests/foundation.test.mjs
node scripts/validate-foundation.mjs
npm test
npm run build
npm run typecheck
```

Do not run `git status`, `git rev-parse`, `git diff`, `git apply`, `git add`, `git commit`, or any other Git command. If the patch file or helper file is inaccessible, stop and report the exact file-access failure; do not improvise a different implementation.

Allowed modified files:
- `src/shared/governed-post-transaction-readiness-refresh.mjs`
- `tests/governed-post-transaction-readiness-refresh.test.mjs`

Allowed new product files: none.

Authority boundary: this R10 package grants no provider call, parser/runtime execution, filesystem/source writes beyond the exact two product files changed by the exact patch, renderer/IPC expansion, BEO publication, RTM generation, production BLK link, protected-body access, signer/storage/ledger action, or reusable BLK-pipe/Codex authority.

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




