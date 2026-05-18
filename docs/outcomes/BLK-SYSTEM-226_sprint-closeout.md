# BLK-SYSTEM-226 Sprint Closeout — Kuronode Worktree Static Validation Profile

**Status:** Closed
**Date:** 2026-05-18T16:26:14+10:00
**Commit:** pending at closeout draft

## Intent

Make the clean-worktree BEB-L2 route one step closer to a real Kuronode feature drop by adding a repository-owned validation profile that is safe to run inside the target Kuronode worktree without package-manager, network, shell-wrapper, or caller-supplied command authority.

## Result

BLK-SYSTEM-226 added `kuronode-worktree-static`, a structured validation profile that resolves to:

```text
git diff --check -- .
```

The profile is intentionally narrow: it provides local whitespace/static diff evidence for exact clean-worktree BEB-L2 drops and nothing else.

## Changes

- Added `kuronode-worktree-static` to `internal/validationprofiles/profiles.go` with structured argv `git diff --check -- .` and capability label `local-git-diff-check`.
- Added Go RED/GREEN tests proving the profile resolves, uses structured argv without shell interpretation, and exposes the explicit safe capability.
- Added the profile to the BEB-L2 drop manifest allowlist in `python/beb_l2_blk_pipe_route.py`.
- Added route test coverage proving an approved drop can request `kuronode-worktree-static` and that BLK-System forwards it through the closed adapter path.
- Updated BLK-077, BLK-079, and current-state tests to record BLK-SYSTEM-226 as a validation-profile readiness increment, not live dispatch authority.

## Authority Boundaries

- No Kuronode source worktree mutation was performed.
- No clean worktree was created by this sprint.
- No BEB-L2 dispatch was performed by this sprint.
- No caller-supplied validation commands are allowed.
- No package-manager, network, browser, model-service, cyber, RTM, BEO, production-isolation, or BLK-test MCP authority was granted.
- `kuronode-worktree-static` is local diagnostic/static evidence only and does not itself authorize BLK-pipe runtime.

## Verification

Focused RED/GREEN verification passed before closeout drafting:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_route_accepts_kuronode_worktree_static_validation_profile -v

go test ./internal/validationprofiles -run 'TestResolveKuronodeWorktreeStaticProfile|TestProfileCapabilitiesAreExplicitAndSafe' -count=1
```

Final verification recorded for this closeout:

```text
Focused Python/Go profile and authority tests: PASS
Full Python unittest discovery: 1397 tests OK, 35 skipped
Full Go suite: PASS
git diff --check: PASS
```

## Hostile Review

Hostile review target: the new profile must not launder validation-command authority into clean-worktree dispatch.

Hostile review conclusion:

- The profile uses structured argv and no shell wrapper.
- The profile does not invoke package managers, network tools, model services, or runtime build/test commands.
- Python route allowlisting accepts only the repository-owned profile name, not caller-supplied command text.
- BLK-SYSTEM-226 narrows the next feature-drop validation surface; it does not grant dispatch or mutation authority.

## Next Frontier

`NEXT_FRONTIER_EXACT_KURONODE_FEATURE_DROP_FROM_CLEAN_WORKTREE_NOT_BLANKET_AUTHORITY` remains active: select/create a trusted sterile Kuronode worktree, retarget an approved BEB-L2 manifest with BLK-SYSTEM-225, preflight it with BLK-SYSTEM-223, validate using `kuronode-worktree-static`, then dispatch only the exact approved payload through BLK-pipe/Codex.
