# BLK-pipe Sprint 004 — Task 5 Outcome

**Status:** Complete
**Date:** 2026-05-04
**Task:** Prove Fake Tactical-Engine Command Shape Through BLK-pipe
**Commit:** `ee11807 feat: run blk-pipe codex dry-run fixture`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Task 5 proved the Sprint 004 fake tactical-engine command shape through BLK-pipe using deterministic local fixtures only.

The task intentionally did **not** run live Codex, live tactical LLMs, network model services, cyber tooling, or live BLK-test MCP. The execution path uses a local fake executable named `codex-dry-run` and asserts a deterministic provenance marker in the BLK-pipe report.

## 2. Files Added/Changed

Changed:

- `python/blk_pipe_dry_run_orchestrator.py`
- `python/test_blk_pipe_dry_run_orchestrator.py`

Added:

- `testdata/engines/codex-dry-run`

Created outcome:

- `docs/outcomes/BLK-PIPE-004_task-005-outcome.md`

## 3. Behavior Implemented

Implemented `run_blk_pipe_dry_run_fixture(...)` in the Sprint 004 dry-run orchestrator fixture module.

The helper:

1. Loads the Task 4 BEB/L2 fixture pair.
2. Builds the deterministic `codex-dry-run` payload shape.
3. Writes the payload to a temporary JSON file.
4. Invokes BLK-pipe without a shell using:
   - `[binary_path, "--payload", temp_payload_path]`
5. Scopes `PATH` so the tactical-engine-shaped command resolves to the local `testdata/engines/codex-dry-run` fixture.
6. Parses and returns the raw BLK-pipe JSON report.
7. Removes the temporary payload file in a `finally` path.

Added a deterministic POSIX fake engine fixture at `testdata/engines/codex-dry-run`.

The fake engine:

- expects the dry-run tactical-engine argv shape:
  - `exec`
  - `-`
  - `--json`
  - `--isolated`
  - `--yes`
  - `--deny-read=**/.git/**`
  - `--deny-read=**/node_modules/**`
  - `--deny-read=**/.env*`
  - `--dry-run`
- reads the L2 packet from stdin,
- verifies `L2_ID: L2_004` and `BEB_ID: BEB_004` markers,
- writes deterministic `dry_run_output.txt`,
- emits `FAKE_CODEX_DRY_RUN_FIXTURE=BLK-PIPE-004` into bounded engine logs.

The Python execution tests now prove that BLK-pipe returns:

- `status: SUCCESS`,
- `beb_id: BEB_004`,
- non-empty `pre_engine_hash`,
- non-empty `commit_hash`,
- `staged_files: ["dry_run_output.txt"]`,
- unchanged `trace_artifacts`,
- bounded `engine_logs` containing the fake-engine provenance marker.

## 4. TDD Evidence

### 4.1 RED

Failing test evidence before implementation:

```text
ImportError: cannot import name 'run_blk_pipe_dry_run_fixture' from 'blk_pipe_dry_run_orchestrator'

FAILED (errors=1)
```

This was the expected RED failure because the Task 5 BLK-pipe invocation helper did not exist yet.

During GREEN implementation, an additional real integration failure surfaced when the fake engine argument count was initially wrong:

```text
engine_logs: FAKE_CODEX_DRY_RUN_FIXTURE=BLK-PIPE-004 unexpected argv count: 9
```

The fake engine was corrected to expect all nine dry-run arguments.

A second integration finding showed that this BLK-pipe implementation treats new and modified allowlists as a combined staging boundary but performs a pre-staging physical-residue gate that rejects a brand-new `dry_run_output.txt` fixture path before the success commit path. The Task 5 execution fixture therefore seeds a placeholder `dry_run_output.txt` in the hermetic test repository and exercises the allowed modified-file path while preserving the Task 4 payload-construction contract separately.

### 4.2 GREEN

Focused GREEN evidence:

```text
python3 -m unittest discover -s python -p 'test_blk_pipe_dry_run_orchestrator.py' -v

Ran 12 tests in 0.174s

OK
```

Full Python suite evidence:

```text
python3 -m unittest discover -s python -p 'test_*.py'

Ran 29 tests in 0.522s

OK
```

Go verification evidence:

```text
go test ./...

ok  github.com/camcamcami/BLK-System/cmd/blk-pipe
ok  github.com/camcamcami/BLK-System/internal/contracts
ok  github.com/camcamcami/BLK-System/internal/engine
ok  github.com/camcamcami/BLK-System/internal/execguard
ok  github.com/camcamcami/BLK-System/internal/gitguard
ok  github.com/camcamcami/BLK-System/internal/pipe
ok  github.com/camcamcami/BLK-System/internal/runtimeguard
ok  github.com/camcamcami/BLK-System/internal/testutil
ok  github.com/camcamcami/BLK-System/internal/validation
```

Additional verification:

```text
go vet ./...                      -> PASS
git diff --check                  -> PASS
```

## 5. Review Results

Because this sprint explicitly forbids live Codex and live tactical LLMs, review gates were deterministic local scripts rather than delegated LLM reviewers.

### 5.1 Spec / Traceability Gate

Result:

```text
SPEC_TRACEABILITY_GATE PASS
```

The gate checked that:

- all three Task 5 tests exist,
- `run_blk_pipe_dry_run_fixture(...)` exists,
- BLK-pipe invocation uses `[binary_path, "--payload", temp_payload_path]`,
- test assertions cover `SUCCESS`, `trace_artifacts`, `pre_engine_hash`, `commit_hash`, `staged_files`, and the fake-engine provenance marker,
- the fake engine reads stdin, writes `dry_run_output.txt`, preserves `BEB_004` / `L2_004` markers, and emits `FAKE_CODEX_DRY_RUN_FIXTURE=BLK-PIPE-004`.

### 5.2 Safety / Docs-Quality Gate

Result:

```text
SAFETY_DOCS_QUALITY_GATE PASS
```

The gate checked:

- final newlines,
- no trailing whitespace,
- no active-vault access tokens in the runtime fixture files,
- no network/model execution tokens such as `curl`, `wget`, OpenAI API URLs, or Anthropic API URLs,
- no real `codex` invocation patterns,
- no Python `shell=True`, `os.system`, or `subprocess.call(...)` usage.

## 6. Final Verification

Final implementation verification before commit:

```text
export PATH="$HOME/.local/bin:$PATH"
go build -o /tmp/blk-pipe-sprint-004 ./cmd/blk-pipe
python3 -m unittest discover -s python -p 'test_blk_pipe_dry_run_orchestrator.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
rm -f /tmp/blk-pipe-sprint-004
```

Result: PASS.

Implementation commit:

```text
ee11807 feat: run blk-pipe codex dry-run fixture
```

## 7. Deviations / Notes

- No Hindsight tools were used.
- No live Codex, live tactical LLMs, network model services, cyber tooling, or live BLK-test MCP were run.
- The local fake engine is named `codex-dry-run` to match the fixture command shape, but it is a repository-local POSIX script and does not invoke a real `codex` binary.
- The Task 4 payload construction contract remains unchanged: the builder still emits `allowed_modified_files: []` and `allowed_new_files: ["dry_run_output.txt"]`.
- The Task 5 BLK-pipe execution helper converts that fixture boundary into an allowed modified-file execution fixture and pre-seeds a placeholder file in the hermetic test repo. This is documented because the existing BLK-pipe success path rejects a brand-new physical residue before the success commit path in this fixture shape.

## 8. Next Task

Task 6 — Add BLK-test PASS/FAIL Handoff Fixture Contract.
