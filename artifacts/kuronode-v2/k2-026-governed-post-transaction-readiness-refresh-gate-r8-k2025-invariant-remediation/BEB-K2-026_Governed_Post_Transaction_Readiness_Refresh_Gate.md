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

# BEB-K2-026 — R8 K2-025 Invariant Remediation

**BEB ID:** BEB-K2-026
**Route revision:** R8 K2-025 invariant remediation
**Target repository:** Kuronode-v2
**Target hash:** `e9395787ac1b5a7abe4a053d451216a90602178a`
**Model:** `gpt-5.5`
**Direct requirement:** `REQ-KN-075`

## Objective

Remediate the post-R7 hostile-review blocker: the gate accepted self-consistent but impossible K2-025 transaction-shaped records as ready. R8 keeps the exact K2-026 scope and adds strict K2-025 structural invariant checks before ready presentation can be allowed.

## Blocker Being Remediated

A caller could clone a real K2-025 transaction record, mutate an impossible field, recompute the copied transaction/recovery evidence hashes, provide matching refresh evidence, and receive `post-transaction-ready`. The missing invariants were:

1. `transactionId` must be derived from `writeIntentId` using the K2-025 sequence suffix.
2. `promotionRequestId` must be the K2-025 prefix plus exactly four digits.
3. `targetVersionHash` must equal `afterVersionHash` for K2-025 transaction records.

## Exact Artifacts

- Patch path: `BDOC-K2-026_R8_k2025_invariant_remediation_exact_patch.diff`
- Patch SHA256: `sha256:bf890b0a920ecf28c8dd3162614d4538cc60f5ed7d7b67ee4c9cf4ccb6824d6b`
- Patch bytes: `6564`
- Non-Git apply helper: `BDOC-K2-026_R8_apply_exact_patch_without_git.py`
- Helper SHA256: `sha256:b6c8977e5084b58ea83ecbf0daa0dad54ba27252b66b5d76dbe63fc42e639c4b`
- Helper bytes: `993`

## Allowed Source Scope

Modified files only:

- `src/shared/governed-post-transaction-readiness-refresh.mjs`
- `tests/governed-post-transaction-readiness-refresh.test.mjs`

No new product files are authorized by R8.

## Acceptance Criteria

- Add hostile regression coverage proving recomputed/self-consistent impossible K2-025 transaction records remain not-ready.
- Enforce the K2-025 transaction ID/write-intent suffix derivation, exact four-digit promotion request IDs, and `targetVersionHash === afterVersionHash` before allowing readiness.
- Preserve all prior R7 behavior: strict schema, exact false authority flags, hostile JS/proxy/getter/accessor/symbol/class rejection, no raw/protected material leakage, deterministic frozen outputs, and no provider/parser/filesystem/source/renderer/RTM/BLK-link/BEO/signer/storage/ledger/reusable-dispatch authority.

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


