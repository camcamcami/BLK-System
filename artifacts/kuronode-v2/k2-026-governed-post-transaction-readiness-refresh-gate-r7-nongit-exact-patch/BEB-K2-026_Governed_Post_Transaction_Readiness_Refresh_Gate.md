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

# BEB-K2-026 — R7 Non-Git Exact Patch Replay for Hostile-Review Remediation

**BEB ID:** BEB-K2-026
**Route revision:** R7 non-Git exact-patch replay
**Target repository:** Kuronode-v2
**Target hash:** `35ae20f309dd5b365225d6484429925e7b886999`
**Model:** `gpt-5.5`
**Direct requirement:** `REQ-KN-075`

## Objective

Route the same hostile-review remediation patch as R6, but avoid engine-side Git commands. R6 proved the patch itself and all requested validations were green, but BLK-pipe failed closed before repository-owned validation because engine-side Git/status/apply-check bookkeeping dirtied the Git metadata snapshot. R7 therefore keeps the exact same product diff and applies it with package-owned non-Git tooling so BLK-pipe can own Git validation, staging, and commit.

## R7 Scope

R7 remediates the R5 hostile-review blockers:

1. Spoofed/non-K2-025 transaction-shaped records accepted as ready.
2. Nested refresh evidence authority/raw fields, symbol keys, and class/prototype evidence laundering.
3. Caller-controlled `failureReasons` proxies executing caller code or crashing the gate.
4. Overclaimed hostile-input foundation coverage before these gaps were closed.

## Exact Artifacts

- Patch path: `BDOC-K2-026_R7_hostile_review_remediation_exact_patch.diff`
- Patch SHA256: `sha256:e068c0c71d135374cc1840eccc27ff9eeabc11dcfe9c5de7da35819ef2f97adf`
- Patch bytes: `21871`
- Non-Git apply helper: `BDOC-K2-026_R7_apply_exact_patch_without_git.py`
- Helper SHA256: `sha256:7c0c06819ac3c5808429a94cbce06443f9ccf00c0e23a73c809148debd1264d7`
- Helper bytes: `1215`

## Allowed Source Scope

Modified files only:

- `src/shared/governed-post-transaction-readiness-refresh.mjs`
- `tests/governed-post-transaction-readiness-refresh.test.mjs`

No new product files are authorized by R7.

## Acceptance Criteria

- Recompute/validate K2-025 transaction evidence and recovery evidence hashes from exact public record fields before allowing ready presentation.
- Validate exact K2-025 transaction authority flags and exact K2-026 refresh authority flags as all false.
- Reject symbol keys, non-plain records/class instances/prototype evidence, extra nested authority/raw fields, malformed hashes, and caller proxy/getter/accessor hazards without throwing.
- Add regression coverage for spoofed transactions, nested authority/raw laundering, symbol keys, class/prototype evidence, and hostile `failureReasons` proxies.
- Preserve pure-data/non-authorizing behavior: no provider calls, parser/runtime execution, filesystem/source writes outside the two exact allowlisted files, renderer/IPC expansion, RTM generation, production BLK link, BEO publication, signer/storage/ledger, protected-body access, or reusable dispatch authority.

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

