L2_ID: L2-K2-026
BEB_ID: BEB-K2-026
BEO_ID: BEO-K2-026
MODEL: gpt-5.5
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write

You are Codex executing the exact `BEB-K2-026` package through BLK-System. Use strict TDD.

1. Inspect K2-025 transaction APIs and existing pure-data K2 modules/tests for style, but do not change their behavior unless necessary for a K2-026 failing test.
2. Write `tests/governed-post-transaction-readiness-refresh.test.mjs` first. Include RED tests for `KGRR-001` through `KGRR-010` where applicable. Run the new test and capture the expected missing-module/API failure before implementing.
3. Implement the smallest pure-data shared module `src/shared/governed-post-transaction-readiness-refresh.mjs` that passes the tests.
4. Update `package.json` so `npm test` runs the new focused test.
5. Update `scripts/validate-foundation.mjs` and `tests/foundation.test.mjs` only if needed for static guardrails: the evidence should say this slice is bounded post-transaction readiness/status behavior and does not authorize provider calls, parser execution, filesystem/source writes, renderer/IPC expansion, RTM/blk-link, BEO publication, or protected-body access.
6. Verify with:
   - `node tests/governed-post-transaction-readiness-refresh.test.mjs`
   - `node tests/governed-write-transaction.test.mjs`
   - `node tests/foundation.test.mjs`
   - `node scripts/validate-foundation.mjs`
   - `npm test`
   - `npm run build`
   - `npm run typecheck`
7. Keep changes within the exact allowlist. Do not create docs, route archives, mirrors, package-lock files, build outputs, node_modules, dist, or unlisted files.
8. Commit message is route-owned by BLK-System; do not create your own Git commit inside Codex if the sandbox blocks `.git` writes.

Public API guidance (adapt if tests show a cleaner name): export a capability/method vocabulary, allowed status/reason constants, and a function such as `createPostTransactionReadinessRefreshGate(transactionRecord, refreshEvidence)`. Records should expose deterministic fields such as `readinessGateId`, `transactionId`, `writeIntentId`, `targetVersionHash`, `afterVersionHash`, `readinessState`, `readyPresentationAllowed`, `refreshEvidenceStatus`, `failureReasons`, `readinessEvidenceHash`, `gateEvidenceHash`, and `authorityFlags`.

Do not serialize raw caller evidence back out. If accepted evidence needs reviewable metadata, copy only exact primitive identifiers/hashes/booleans through a fixed schema.

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
