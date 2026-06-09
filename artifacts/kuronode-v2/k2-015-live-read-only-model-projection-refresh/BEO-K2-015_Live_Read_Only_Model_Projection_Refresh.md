---
beo_id: "BEO-K2-015"
beb_id: "BEB-K2-015"
l2_id: "L2-K2-015"
title: "Live Read-Only Model/Projection Refresh"
status: "closed"
artifact_stage: "final_beo_closeout"
target_hash: "68a9b8c0b9b056a9c8a80d8bae32c093ade4c8e6"
feature_commit: "c4ebb5c82cb0354728f55be9b28bcf107a6cd453"
closeout_metadata_commit: "4b83f7ebc026188c48b78eecbc0625f7dffb0db0"
execution_mode: "supervised_external_codex_fallback_after_governed_route_timeouts"
trace_artifacts:
  - kind: "product_convergence_map"
    id: "K2-PRODUCT-CONVERGENCE-MAP"
    version_hash: "sha256:bc70f88549b0939395495861a3797d4d42fcf72b584926927712700c00c69cb9"
  - kind: "roadmap"
    id: "K2-IMPLEMENTATION-ROADMAP"
    version_hash: "sha256:a1ea64058864785a0530b365ec27069d3256bce0f66d9304ff76460736a03fd0"
  - kind: "process_guard"
    id: "K2-ITERATION-DRIFT-PROTECTION"
    version_hash: "sha256:a2acedfa31dae7134298c39b0f7ec7ee9c47e79cd0d54179cd28a3f3fb76a393"
  - kind: "traceability_index"
    id: "K2-TRACEABILITY-MANIFEST"
    version_hash: "sha256:894f69016511b7dabb42d2fcdfc9dbe66e612f6c2d2a75b3fa372c63d3f2a6ec"
  - kind: "requirement"
    id: "REQ-KN-081"
    version_hash: "sha256:5a0fc367c36db330ac6f5588642b66ad3e54fb1692fa4c4a94fc6fd5e1bf6333"
  - kind: "requirement"
    id: "REQ-KN-082"
    version_hash: "sha256:7e594b3e9fe6116af61c19240c0f037c4d403a715061b4bb1a74a42a2c298751"
  - kind: "requirement_supporting"
    id: "REQ-KN-039"
    version_hash: "sha256:37d189928e366cd75e1e619c6cd96839ea879b1f275119bc8e06723aabe47846"
  - kind: "requirement_supporting"
    id: "REQ-KN-040"
    version_hash: "sha256:c6f9513a449b3acd3fde5575410f75c394121370aca3fdf5ffc97db7b7558e90"
  - kind: "requirement_supporting"
    id: "REQ-KN-041"
    version_hash: "sha256:8ef1252ec985e5ba797e117df5c690fb64dcfafd27929ca6151892d83a959a19"
  - kind: "requirement_supporting"
    id: "REQ-KN-042"
    version_hash: "sha256:921b06da4206c8407f21a9afadbdde0e04b048e5d73c695194fa205cb1856eb4"
  - kind: "requirement_supporting"
    id: "REQ-KN-048"
    version_hash: "sha256:884e222872cf8ddeaada8bfb72819272b5f613cdaf1b61fb14d1921cf10cffa0"
  - kind: "requirement_supporting"
    id: "REQ-KN-077"
    version_hash: "sha256:4515b1457f48848c81a86283707787582899c66815b0d6529a303bc696628f79"
  - kind: "requirement_supporting"
    id: "REQ-KN-080"
    version_hash: "sha256:c19a3a1d51d80ffb8a87fb0decfff3eaa3233cc1948e6d3b62d497dddaf378d7"
  - kind: "requirement_supporting"
    id: "REQ-KN-083"
    version_hash: "sha256:0c0468e9b11e2e65170318edc99501d865d846860c56ee75a6dc7146d993afb0"
  - kind: "requirement_supporting"
    id: "REQ-KN-084"
    version_hash: "sha256:a704f161aee6841737a9d9f355e88ac1f001ed8d77d369a9be291cace3e64a67"
  - kind: "requirement_supporting"
    id: "REQ-KN-107"
    version_hash: "sha256:1b523c3472541f685d223313c0603d8ab1e18c23ecbfb209ba3bc5f8fce27bce"
  - kind: "architecture"
    id: "KVA-004"
    version_hash: "sha256:1bffba596fcedf5d6f2cf93d82afc6e7ae3483639f9910f4d7c7b394eb5cbe1b"
  - kind: "architecture"
    id: "KVA-005"
    version_hash: "sha256:51ffbd376dee23e4a12ce064acc55ac30e6902abd8ea2ec4bc4568957725ba0d"
  - kind: "runtime_flow"
    id: "RTF-KVA-007"
    version_hash: "sha256:0e51f9b3a7fafd6f319128309452ad23f4d71074ba18007fbdf036f51f726469"
  - kind: "state_machine"
    id: "SM-KVA-010"
    version_hash: "sha256:9055944208258f34c299597eb20e22f3373311ce77bb3d2b37792d5a47d187ff"
  - kind: "interface_contract"
    id: "ICD-KVA-011"
    version_hash: "sha256:593487a624e4cbaad5066c553217ad5d0d58575cf4c0a5fc43f2faf60f4e184e"
  - kind: "prior_outcome"
    id: "BEO-K2-014"
    version_hash: "sha256:427640fa1c7adc145710fe5f0f5c3c8e88994b911e512cdbdf62b8be9acdee08"
---
# BEO-K2-015 — Live Read-Only Model/Projection Refresh

## 1. Outcome summary

K2-015 is complete. Kuronode now has a bounded live read-only model/projection refresh seam: accepted in-memory model snapshots, paired with accepted model-health evidence, can produce the same sanitized projection payload shape as the K2-013 fixture-backed path while keeping every adjacent mutation, runtime, layout, provider, persistence, and publication authority denied.

The implementation landed in Kuronode commit `c4ebb5c82cb0354728f55be9b28bcf107a6cd453`.

## 2. Execution route evidence

- Canonical BEB: `BEB-K2-015_Live_Read_Only_Model_Projection_Refresh.md` (`sha256:efe45c82c614c3aad22e538e2cb75b7d78214850867b36305f13f6f397a4ef8c`).
- Canonical L2: `L2-K2-015_Live_Read_Only_Model_Projection_Refresh.md` (`sha256:f7b2c486403008d55f911e07eff30992f9b5ab35ee112412ce4c89e91735aa4b`).
- Pending BEO preimage: `sha256:cb6222729e605155b56cd25e4a26f3d7a830b2dd69e8a84c4ea6699133aff0a8`.
- Source-worktree drop: `drop.json` (`sha256:bf59f4bf38dc50f2034f1dd2c5d00113d3074fa44930ca96be7d48db014eaa53`).
- Clean-worktree drop: `drop.clean-worktree.json` (`sha256:1488633135623857e79031628f19680582c704f25656710b9aba1ca2920c141a`).
- Target parent: `68a9b8c0b9b056a9c8a80d8bae32c093ade4c8e6`.
- Clean worktree: `/tmp/blk-system-clean-worktrees/kuronode-v2-k2-015-68a9b8c0b9b0`.
- Route note: governed preflight accepted the clean-worktree package, but the BLK-pipe engine path timed out twice. Implementation continued through a supervised external Codex fallback in the same sterile worktree, with the same allowlist and denied-authority boundary.
- External Codex model/reasoning/sandbox: `gpt-5.5`, `xhigh`, `workspace-write`, private bwrap env/PATH.
- External Codex final message: `/tmp/k2-015-external-codex-final.md` (`sha256:99dc9e4c48a39a7d40e6d87620f273f9949aff167233fe0209eaeef955cc1d48`).
- External Codex JSONL log: `/tmp/k2-015-external-codex.jsonl` (`sha256:c60f3993e0e75dfd084976cfadd56493db9f9b3f0c6d0f6b62d5a5c40ca052fa`).
- Feature patch from selected target to implementation commit: `/tmp/k2-015-feature.patch` (`sha256:29452a817aa52e527bd443d621e6709417eb3d09832182a84ad4ff1501b54227`, 100579 bytes).

## 3. Exact files changed

Allowed modified files:

- `package.json`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`
- `src/shared/foundation.ts`
- `src/main/main.ts`
- `src/shared/projection-payload.mjs`

Allowed new files:

- `src/shared/model-projection-refresh.mjs`
- `tests/model-projection-refresh.test.mjs`

No other Kuronode files were changed in the implementation commit.

## 4. Implementation summary

- Added `createProjectionPayloadFromAcceptedModelSnapshot(...)` so accepted bounded in-memory model snapshots can produce the same public projection payload shape as fixture-backed payloads, with `fixtureBackedProjectionPayload: false`.
- Added `src/shared/model-projection-refresh.mjs` exposing the `model-projection-refresh` capability, `refreshReadOnlyProjectionFromModelSnapshot(...)`, model-health gating, bounded recursion, denied-authority flags, frozen outputs, and fail-closed behavior.
- Added K2-015 metadata to `src/main/main.ts`, `src/shared/foundation.ts`, `package.json`, `tests/foundation.test.mjs`, and `scripts/validate-foundation.mjs` without adding dependencies or privileged runtime behavior.
- Added `tests/model-projection-refresh.test.mjs` covering direct and wrapper snapshots, health gates, fixture compatibility, bounds, hostile inputs, immutable handles, and authority denials.

## 5. Verification evidence

Focused and full local verification after remediation:

```text
node tests/model-projection-refresh.test.mjs
→ Model projection refresh tests passed.

node tests/projection-payload.test.mjs
→ Projection payload tests passed.

node scripts/validate-foundation.mjs
→ Foundation validation passed for 40 files.

npm test
→ Foundation tests passed.
→ Provider status tests passed.
→ Status capability tests passed.
→ Workspace status tests passed.
→ Project package inspection tests passed.
→ Parser runtime status tests passed.
→ Model health status tests passed.
→ Parser diagnostic loop tests passed.
→ Parser runtime diagnostic adapter tests passed.
→ Parser runtime execution smoke tests passed.
→ Projection status tests passed.
→ Projection payload tests passed.
→ Model projection refresh tests passed.
→ View intent parameter tests passed.
→ Candidate staging tests passed.

npm run build
→ Foundation validation passed for 40 files.

npm run typecheck
→ Foundation validation passed for 40 files.

git diff --check -- <exact K2-015 allowlist>
→ exit 0, no output.
```

Static added-line scan found zero hardcoded secret, shell-injection, `eval`/`exec`, pickle, or SQL-formatting hits.

Hostile probe after remediation returned:

```text
trapCount: 0
proxyRefresh: malformed + hostile-input + acceptedModelSnapshotRefreshed=false
proxyPayload: malformed + hostile-input
missingRefresh: malformed + missing-snapshot + acceptedModelSnapshotRefreshed=false
authorityRefresh: malformed + caller-authority-ignored + acceptedModelSnapshotRefreshed=false
deepRefresh: malformed + circuit-breaker + acceptedModelSnapshotRefreshed=false
deepPayload: malformed + circuit-breaker
```

## 6. Hostile review and remediation

Initial independent hostile review found three blockers:

1. non-throwing proxies were accepted and their traps were invoked;
2. fail-closed refresh results could still report `acceptedModelSnapshotRefreshed: true`;
3. deeply nested hostile object graphs could throw `RangeError: Maximum call stack size exceeded` instead of returning a frozen fail-closed result.

Remediation added trap-free proxy rejection via Node's proxy detector, bounded descriptor traversal (`maxScanDepth: 8`, `maxScanObjectCount: 64`), `acceptedModelSnapshotRefreshed=false` on malformed/fail-closed results, and direct regression tests for non-throwing proxies and deep object graphs.

Final independent re-review verdicts:

- Authority/scope hostile re-review: **PASS — no blockers found**.
- Contract/test adequacy re-review: **PASS — no blockers found**.

## 7. Requirement stance

Directly advanced:

- `REQ-KN-081`: read-only projection refresh from accepted current model evidence.
- `REQ-KN-082`: preservation of model truth versus view-control/projection separation.

Supporting/prepared only:

- `REQ-KN-039`, `REQ-KN-040`, `REQ-KN-041`, `REQ-KN-042`, `REQ-KN-048`, `REQ-KN-077`, `REQ-KN-080`, `REQ-KN-083`, `REQ-KN-084`, `REQ-KN-107`.

## 8. Authority boundary

K2-015 does not authorize or implement:

- filesystem source-body reads, source-file hashing, directory scans, or project/package writes;
- parser process spawning, parser runtime/binary/WebAssembly loading, runtime download, rebuild, or user-side build;
- projection/layout engine trust, graph traversal trust, canvas rendering trust, or source-coordinate truth claims;
- Agent A lifecycle behavior, provider requests/responses, provider payload retention, credentials, telemetry, or network behavior;
- saved-view persistence, save/export/session persistence, support-bundle export, external-edit adoption/import/promotion, or canonical SysML/KerML mutation;
- RTM generation, production `blk-link`, protected-body reads/scans/hashes, coverage truth, drift rejection, BEO publication/signing/storage/ledger, or reusable BLK-System live dispatch authority.

## 9. Residual blockers and next slice

No K2-015 implementation blockers remain. No `K2-016` slice is selected by this closeout. The next K2 sequence requires an explicit operator/architecture roadmap selection and a fresh BEB/L2/BEO package.

## 10. Mirror, roadmap, and traceability status

- Canonical BEO finalized at this path.
- Obsidian BEO mirror to be synchronized from this final canonical BEO as a non-authoritative view copy.
- Roadmap to be updated to `first_unconsumed_sequence: null`, mark K2-015 closed, and state that no K2-016 is selected.
- Traceability manifest to add K2-015 with exact artifact and patch hashes.
