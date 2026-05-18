# BLK-SYSTEM-233 — BLK-pipe/Codex Progress Reporting Closeout

## Result
PASS — added adapter-level progress callbacks for long BLK-pipe/Codex runs.

## Evidence
- `BlkPipeAdapter.execute_sprint(...)` now accepts `progress_callback` and `progress_interval_seconds`.
- Events emitted: `blk_pipe_started`, periodic `blk_pipe_running`, and `blk_pipe_finished` with elapsed seconds and scoped BEB/workdir/branch metadata.
- Callback failures are swallowed so observability cannot kill a governed run.
- RED/GREEN tests added in `python/test_blk_pipe_adapter.py`.

## Authority
This is observability only. Progress events are not execution approval, validation truth, package-manager authority, runtime tooling authority, host containment proof, or production-isolation evidence.
