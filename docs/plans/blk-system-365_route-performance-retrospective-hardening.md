# BLK-SYSTEM-365 — Route Performance Retrospective Hardening Plan

## Goal

Reduce avoidable BLK-System/Kuronode route waste observed in K2-025 while preserving the improved no-fallback discipline.

## Retrospective inputs

K2-025 improved over the prior 17-round pattern because all product implementation/remediation commits stayed on BLK-pipe and no external fallback was used. Remaining waste came from:

1. attempting or recording a source-worktree route when preflight evidence already showed dirty/ignored residue;
2. allowing repeated clean `ENGINE_TIMEOUT` attempts before a scope/budget review was mechanically classified;
3. discovering core hostile-matrix gaps only after the first successful implementation route;
4. closeout/mirror/hash semantics causing final reconciliation friction.

## Scope

Implement a small executable route-performance layer in `python/beb_l2_blk_pipe_route.py` and tests in `python/test_beb_l2_blk_pipe_route.py`:

- add an explicit K2 governed-write transaction readiness profile / hostile matrix gate for packages touching `src/shared/governed-write-transaction.mjs` or its tests;
- classify dirty/ignored source preflight as a skip-source-dispatch/retarget requirement, not as a route attempt to spend;
- classify repeated no-commit/no-final-message `ENGINE_TIMEOUT` route summaries as requiring route performance review before another normal retry;
- keep all outputs non-authorizing: no fallback, no cleanup, no worktree creation, no dispatch, no BEO/RTM/`blk-link` side effects.

## Non-goals

- No Kuronode product code changes.
- No live BLK-pipe/Codex dispatch.
- No BEO publication, RTM generation, production `blk-link`, protected-body access, runtime/tooling expansion, source cleanup, or automatic worktree creation.
- No new root `docs/BLK-###` doctrine document; this is route-helper hardening plus one closeout.

## TDD plan

1. RED: high-risk governed-write package without the readiness matrix blocks before dispatch.
2. RED: dirty/ignored source preflight is classified as skip-source-dispatch and sterile retarget required.
3. RED: two clean `ENGINE_TIMEOUT` summaries with empty commit/final-message evidence require route performance review before normal retry.
4. GREEN: implement the minimal profile/gate/evaluator.
5. Verify focused route tests, lean documentation policy, broad Python suite in chunks if needed.

## Closeout

Write exactly one outcome:

```text
docs/outcomes/BLK-SYSTEM-365_sprint-closeout.md
```
