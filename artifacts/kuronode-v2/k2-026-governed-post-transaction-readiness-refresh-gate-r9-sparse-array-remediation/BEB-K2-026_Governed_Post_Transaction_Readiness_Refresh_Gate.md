---
beb_id: "BEB-K2-026"
beo_id: "BEO-K2-026"
l2_id: "L2-K2-026"
trace_artifacts:
  - kind: "requirement"
    id: "REQ-KN-075"
    version_hash: "sha256:bdf3c6bb9bc5d2fb3b1562126647b4d2d9f8d58086215b003dcb6a3a429c2931"
  - kind: "requirement"
    id: "REQ-KN-072"
    version_hash: "sha256:b26e55993345b2b07bb1d31d62fa0f33280b684cfc764603d0cbec4c7447bd20"
  - kind: "requirement"
    id: "REQ-KN-073"
    version_hash: "sha256:6e43197e174704f0c2ec5d401fbf2c0e83743dfc0727e0f3ef5194a80a09b19c"
  - kind: "requirement"
    id: "REQ-KN-076"
    version_hash: "sha256:00922100541a76a834128dec91cb0d99637e3d0368dbf26e3b508ca6543d6273"
  - kind: "requirement"
    id: "REQ-KN-085"
    version_hash: "sha256:c8b80d8422c7913fe8f4129872d3c405f0c9de22b92e623711327fab1d00202d"
  - kind: "requirement"
    id: "REQ-KN-128"
    version_hash: "sha256:cec62edb7fcd10c310c65712843922eb40b94e0a22456e3b55dedbdb1cba3dc5"
  - kind: "requirement"
    id: "REQ-KN-134"
    version_hash: "sha256:8778997655ffb3c2650a27a2814f97cf386a0a3b679c09b2b6bf43d39c5f8a67"
  - kind: "requirement"
    id: "REQ-KN-135"
    version_hash: "sha256:2d026cd78ba7681c47fe18a81deeb0f51511fb416ef578acc1e771611ac68f84"
  - kind: "roadmap"
    id: "K2_implementation-roadmap"
    version_hash: "sha256:d95bb5a61a5498e6118233fc4ccd47d29d3001d52cf0aa46f2c2124564722095"
---

# BEB-K2-026 — R9 Sparse Array Fail-Closed Remediation

**BEB ID:** BEB-K2-026
**Route revision:** R9 sparse failureReasons remediation
**Target repository:** Kuronode-v2
**Target hash:** `961cb4fe2b6479c90b7ac2c66762c493eeafeece`
**Model:** `gpt-5.5`
**Direct requirement:** `REQ-KN-075`

## Objective

Remediate the post-R8 hostile-review blocker: a caller-supplied sparse `failureReasons` array with a huge declared length could force unbounded iteration before the K2-026 readiness gate returned fail-closed evidence.

## Blocker Being Remediated

`safeStringArray()` validated safe integer length but did not cap it before iterating `0..length`. A hostile transaction-shaped object could set `failureReasons = new Array(1_000_000_000)` and make the gate hang rather than returning a deterministic blocked/not-ready record.

## Exact Artifacts

- Patch path: `BDOC-K2-026_R9_sparse_array_remediation_exact_patch.diff`
- Patch SHA256: `sha256:cd797537082f6016417bf9c2a46f74cae61223488c0adc43e7b429f4cf4c460a`
- Patch bytes: `1834`
- Non-Git apply helper: `BDOC-K2-026_R9_apply_exact_patch_without_git.py`
- Helper SHA256: `sha256:f80460765d56ae162e162602b37825d90bbeac74094d460400f0d5c32d62f310`
- Helper bytes: `987`

## Allowed Source Scope

Modified files only:

- `src/shared/governed-post-transaction-readiness-refresh.mjs`
- `tests/governed-post-transaction-readiness-refresh.test.mjs`

No new product files are authorized by R9.

## Acceptance Criteria

- Add a regression requiring oversized caller-controlled `failureReasons` arrays to return blocked/not-ready evidence with `oversized-transaction-failure-reasons`.
- Cap copied caller string arrays before index iteration so sparse/huge arrays fail closed quickly.
- Preserve all prior K2-026 behavior, including R8 K2-025 structural invariant checks and all non-authorizing/no-leakage guarantees.

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



