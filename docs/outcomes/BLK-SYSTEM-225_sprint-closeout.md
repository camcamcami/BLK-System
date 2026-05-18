# BLK-SYSTEM-225 Sprint Closeout — Clean Worktree Manifest Route

**Status:** CLOSED — clean-worktree approach selected and made testable without granting dispatch or mutation authority
**Date:** 2026-05-18

## Outcome
BLK-SYSTEM-225 converts the post-224 operator decision into a concrete clean-worktree route: an approved BEB-L2 drop can be retargeted to a trusted clean worktree manifest, then re-approved and preflighted before any BLK-pipe/Codex dispatch.

## Implemented
- Added `build_clean_worktree_drop_manifest(...)` to `python/beb_l2_blk_pipe_route.py`.
- Added CLI mode `--clean-worktree-manifest` with `--clean-work-dir` and `--clean-worktree-root`.
- Added RED/GREEN coverage proving:
  - source worktree with ignored residue remains blocked;
  - sterile clone can pass preflight using the retargeted manifest;
  - clean worktree destination must be under trusted clean roots;
  - destination cannot be the source worktree or nested under it;
  - manifest creation does not create worktrees, clean files, dispatch BLK-pipe, or authorize source mutation.
- Updated BLK-077 and BLK-079 to move the roadmap from “clean vs split decision” to “exact Kuronode feature drop from trusted clean worktree.”

## Verification
- Focused route/current-state/docs suite: `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_beb_l2_blk_pipe_route python.test_blk_current_state_authority_index python.test_lean_documentation_policy -v` — 40 tests PASS.
- Full Python suite: `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover -s python -p 'test*.py'` — 1395 tests PASS, 35 skipped.
- Go suite: `go test ./...` — PASS.
- Hostile review found one blocking lean-policy coverage gap; fixed by extending BLK-SYSTEM-225 marker/range gates and rerunning focused verification.

## Authority Cutline
This closeout does **not** authorize worktree creation, cleanup execution, BLK-pipe dispatch, Hermes-direct Kuronode mutation, reusable Codex authority, broad source/Git mutation, runtime/tooling, protected-body access, RTM generation, BEO publication, production BLK-test MCP, blanket `blk-link`, or production-isolation claims.

## Next Frontier
`NEXT_FRONTIER_EXACT_KURONODE_FEATURE_DROP_FROM_CLEAN_WORKTREE_NOT_BLANKET_AUTHORITY`: create/select a sterile trusted clean worktree, produce an approved clean-worktree drop manifest, preflight it, and dispatch one exact Kuronode feature payload through BLK-pipe/Codex only.
