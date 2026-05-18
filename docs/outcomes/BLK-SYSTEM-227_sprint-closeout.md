# BLK-SYSTEM-227 Sprint Closeout — External Codex Final-Message Artifact Hygiene

**Status:** Closed
**Date:** 2026-05-18T17:12:08+10:00
**Commit:** pending local commit

## Intent

Prepare the first real clean-worktree Kuronode BEB-L2 feature drop by removing a target-worktree residue hazard in the BLK-SYSTEM-222 route: Codex `--output-last-message` was pointed at `artifacts/codex/final-message.md`, which would either fail if the directory was missing or create untracked target-worktree residue outside the exact feature allowlist.

## Result

BLK-System now builds route-owned Codex argv for approved BEB-L2 drops with an external final-message artifact path:

```text
/tmp/blk-system-beb-l2-codex/<BEB_ID>/<target_hash_prefix>/final-message.md
```

The artifact parent directory is created by BLK-System before dispatch, outside the target Kuronode worktree. The default generic Codex invocation helper behavior remains unchanged when no BEB/target binding is provided.

## Changes

- Added BEB/target-bound external artifact path support to `build_kuronode_codex_engine_args(...)` in `python/beb_l2_blk_pipe_route.py`.
- Updated `process_drop_file(...)` to pass the exact `beb_id` and `target_hash` into the Codex argv builder.
- Added route regression coverage proving the adapter payload uses an absolute external final-message artifact path, not a path inside the target worktree, and that the parent directory is created.
- Updated BLK-077, BLK-079, executable current-state index tests, and lean documentation gates for BLK-SYSTEM-227.

## Authority Boundaries

- No Kuronode source worktree mutation was performed.
- No clean worktree was created by this sprint.
- No BEB-L2 dispatch was performed by this sprint.
- No caller-supplied engine args or validation commands are allowed.
- The external final-message artifact is advisory execution evidence only; it does not grant broad dispatch, reusable Codex authority, source/Git mutation authority, package-manager/network/runtime authority, RTM/BEO authority, BLK-test MCP authority, or production-isolation claims.

## Verification

Focused RED/GREEN evidence:

```text
RED: python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_process_drop_file_uses_adapter_payload_file_path_with_fake_blk_pipe failed because build_kuronode_codex_engine_args lacked BEB/target-bound artifact parameters.
GREEN: python.test_beb_l2_blk_pipe_route passed after the route emitted the external artifact path.
```

Focused route/current-state/lean verification: PASS.
Full Python unittest discovery: 1398 tests OK, 35 skipped.
Go full suite: PASS.
`git diff --check`: PASS.

## Hostile Review

Hostile review target: the artifact path change must not launder broader Codex dispatch authority or create a new target-worktree mutation path.

Local hostile review conclusion:

- The route still injects Codex args; manifests cannot supply `engine`, `engine_args`, `engine_command`, `validation_commands`, `l2_packet`, or `trace_artifacts`.
- External artifact directory naming is derived from already-validated BEB ID and 40-character target hash.
- A hostile-review symlink/preexisting-path blocker was remediated: the route now rejects symlinked artifact path components, creates private artifact directories, verifies the resolved artifact directory remains under the external artifact root, and removes stale regular final-message files before dispatch.
- The final-message artifact is outside the target worktree, so it is not staged or committed by BLK-pipe allowlist mechanics.
- This sprint removes a dispatch hygiene blocker; it does not perform or authorize the feature drop itself.

## Next Frontier

`NEXT_FRONTIER_EXACT_KURONODE_FEATURE_DROP_FROM_CLEAN_WORKTREE_NOT_BLANKET_AUTHORITY` remains active: create/select a trusted sterile Kuronode worktree, retarget an approved BEB-L2 manifest with BLK-SYSTEM-225, preflight it with BLK-SYSTEM-223, validate with BLK-SYSTEM-226 `kuronode-worktree-static`, keep BLK-SYSTEM-227 Codex final-message output outside the target worktree, and dispatch only the exact approved payload through BLK-pipe/Codex.
