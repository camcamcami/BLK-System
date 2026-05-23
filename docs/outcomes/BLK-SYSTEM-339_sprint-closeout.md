# BLK-SYSTEM-339 — BLK-pipe/Codex Progress Status Sprint Closeout

**Status:** Complete
**Date:** 2026-05-24
**Commit:** this commit (`feat: add BLK-pipe progress status events`)

## 1. Objective

Add operator-visible progress updates for governed BEB/L2 → BLK-pipe/Codex runs so blkhermes can surface meaningful status when a run starts, when Codex/engine completes or fails, when the engine timeout fires, and when validation/testing completes.

## 2. Files Changed

- `cmd/blk-pipe/main.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- `python/blk_pipe_adapter.py`
- `python/test_blk_pipe_adapter.py`
- `python/beb_l2_blk_pipe_route.py`
- `python/test_beb_l2_blk_pipe_route.py`
- `python/test_lean_documentation_policy.py`
- `docs/outcomes/BLK-SYSTEM-339_sprint-closeout.md`

## 3. Implementation Summary

- Added `RunWithProgress` to BLK-pipe as an observational progress stream.
- BLK-pipe now emits `BLK_PROGRESS_JSON` events on stderr at real phase boundaries:
  - `codex_started`
  - `codex_completed`
  - `codex_failed`
  - `testing_completed`
  - `testing_failed`
- Engine timeout events include `status=ENGINE_TIMEOUT`, `failure_class=engine_timeout`, `denial_route=timeout`, and `timeout_seconds`.
- The Python adapter streams stderr concurrently, relays `BLK_PROGRESS_JSON` to its existing progress callback, and avoids duplicate inferred Codex/testing events when real phase events are present.
- The Python adapter now reports launch failure and Python-side deadlock timeout through progress events instead of only returning a final object.
- The BEB/L2 route CLI gained `--progress-stderr`, which prints concise `[BLK status] ...` lines for operator/blkhermes relay on both `--drop` and `--inbox` dispatch paths.
- Heartbeat events remain available to callbacks but are intentionally not printed by the user-facing stderr formatter, avoiding status spam.

## 4. Verification

- RED evidence:
  - Python adapter progress tests initially failed because `codex_started`, `codex_completed`, `codex_failed`, and `testing_completed` were absent.
  - Route CLI progress test initially failed because `--progress-stderr` was not accepted.
  - Go progress tests initially failed because `RunWithProgress` did not exist.
- GREEN evidence:
  - `TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python -W error::ResourceWarning -m unittest python.test_blk_pipe_adapter python.test_beb_l2_blk_pipe_route python.test_lean_documentation_policy -q` — 75 tests OK.
  - `go test ./...` — OK.
  - `git diff --check` — OK.
  - `test ! -e python/__pycache__` — OK.

## 5. Hostile Review / Risk Check

Initial hostile review found blockers: inferred Codex completion was too late, Python timeout lacked a Codex-failure event, launch failure could create false starts, failure coverage was incomplete, and `--inbox` did not receive progress wiring.

Remediation:

- Moved true Codex/testing phase events into Go BLK-pipe at the engine and validation boundaries.
- Streamed Go progress through the Python adapter instead of waiting for final JSON.
- Added Python timeout and launch-failure progress events.
- Wired `--progress-stderr` through both direct drop and inbox dispatch.
- Kept stderr status output minimal: BEB ID, phase, status, failure class, timeout seconds, and validation command count only. It does not print L2 packet text, engine logs, validation logs, git diff, report stderr, protected body text, credentials, or source content.

Residual boundary: progress events are observability only. They do not grant approval, dispatch authority, BEO publication, RTM generation, production `blk-link`, protected-body access, runtime authority, or target/source/Git mutation beyond the already approved exact route.

## 6. Authority Boundary

This sprint adds communication/observability only. It does not authorize:

- new BEB dispatch beyond an exact approved payload;
- live Codex execution outside the governed BLK-pipe route;
- reusable BLK-pipe runtime authority;
- BEO publication/signing/storage/ledger action;
- RTM generation or production `blk-link`;
- protected BLK-req body reads/copying/parsing/hashing/scanning;
- package/network/model/browser/cyber tooling expansion;
- target/source/Git mutation outside exact route allowlists.

## 7. Documentation Burden Check

No new root `BLK-###` document was created. This sprint produced one outcome closeout only: `docs/outcomes/BLK-SYSTEM-339_sprint-closeout.md`.
