# BLK-pipe Sprint 005 — Task 2 Outcome

**Status:** Complete
**Date:** 2026-05-04
**Task:** Repair True `allowed_new_files` Dry-Run Execution
**Commit:** `99c88f2 fix: support true blk-pipe allowed_new files`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Make a true new file listed only in `allowed_new_files` succeed through BLK-pipe without pre-seeding a tracked placeholder or rewriting the payload into `allowed_modified_files`.

Task 2 was executed locally only. No Hindsight, live Codex, live tactical LLMs, network model services, cyber tooling, or live BLK-test MCP were used.

---

## 2. Files Added/Changed

Implementation commit `99c88f2` changed:

- `internal/pipe/run.go`
  - Added safe allowed-new regular-file mode normalization for non-executable group-writable files created under `umask 0002`.
  - Normalizes accepted `0664` allowed-new files to deterministic `0644` before staging.
  - Preserves fail-closed handling for setuid/setgid/sticky, world-writable, unsupported/exotic modes, non-regular paths, and unsafe parent directory modes.
- `internal/pipe/run_test.go`
  - Added `TestRunAllowedNewFileWithGroupWritableUmaskSucceeds`.
- `python/blk_pipe_dry_run_orchestrator.py`
  - Removed the Sprint 004 execution-helper workaround that mirrored `allowed_new_files` into `allowed_modified_files` and cleared `allowed_new_files` before invoking BLK-pipe.
- `python/test_blk_pipe_dry_run_orchestrator.py`
  - Removed `dry_run_output.txt` placeholder pre-seeding from hermetic dry-run repo setup.
  - Added a payload-capture regression proving the invocation helper preserves `allowed_modified_files: []` and `allowed_new_files: ["dry_run_output.txt"]` at the BLK-pipe subprocess boundary.
  - Updated the default test binary path to `/tmp/blk-pipe-sprint-005` so tests rebuild against current source rather than accidentally reusing the old Sprint 004 test binary.
- `python/test_beo_fixture_projection.py`
  - Removed `dry_run_output.txt` placeholder pre-seeding from the end-to-end BEO trace test repo setup.
  - Updated the default test binary path to `/tmp/blk-pipe-sprint-005`.
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
  - Documented the Sprint 005 true `allowed_new_files` proof and mode normalization rule.
- `docs/outcomes/BLK-PIPE-004_sprint-closeout.md`
  - Marked the historical Task 5 caveat as resolved by Sprint 005 Task 2 without rewriting Sprint 004 evidence.

Created by the outcome step:

- `docs/outcomes/BLK-PIPE-005_task-002-outcome.md`

---

## 3. Behavior Implemented

Task 2 requirements landed as follows:

1. A BLK-pipe payload with only:

   ```json
   {
     "allowed_modified_files": [],
     "allowed_new_files": ["dry_run_output.txt"]
   }
   ```

   now succeeds when the engine creates `dry_run_output.txt` as a previously untracked file under `umask 0002`.

2. The successful report includes:

   - `status: SUCCESS`,
   - non-empty `pre_engine_hash`,
   - non-empty `commit_hash`,
   - `staged_files == ["dry_run_output.txt"]`,
   - preserved `trace_artifacts`,
   - clean final Git status.

3. The Python dry-run fixture repo setup no longer commits a placeholder `dry_run_output.txt`.

4. `run_blk_pipe_dry_run_fixture(...)` no longer rewrites the payload allowlists. The subprocess payload preserves:

   ```json
   {
     "allowed_modified_files": [],
     "allowed_new_files": ["dry_run_output.txt"]
   }
   ```

5. Mode safety is preserved with a narrow rule:

   - regular allowed-new files with physical mode `0664` are accepted only as safe non-executable group-writable files and normalized to `0644` before staging,
   - existing accepted modes `0644` and `0755` remain accepted,
   - `0600`, setuid/setgid/sticky modes, unsafe parent directory modes, world-writable/exotic modes, device nodes, FIFOs, directories, and traversal/path validation hazards remain fail-closed.

---

## 4. TDD Evidence

### 4.1 RED

#### Go RED

The new Go regression failed before the implementation fix:

```text
$ go test ./internal/pipe -run 'TestRunAllowedNewFileWithGroupWritableUmaskSucceeds' -v
=== RUN   TestRunAllowedNewFileWithGroupWritableUmaskSucceeds
    run_test.go:3192: exit code = 3, want 0; report={Status:UNAUTHORIZED_FILE_MUTATION ExitCode:3 ... DestroyedFiles:[dry_run_output.txt] ... Error:engine modified files outside the allowlist}
--- FAIL: TestRunAllowedNewFileWithGroupWritableUmaskSucceeds (0.03s)
FAIL
FAIL	github.com/camcamcami/BLK-System/internal/pipe	0.032s
```

This reproduced the plan’s root cause: a shell-created true new file under `umask 0002` had physical mode `0664`, which BLK-pipe treated as unauthorized physical residue.

#### Python RED

The new payload-capture regression failed before removing the execution-helper allowlist rewrite:

```text
$ python3 -m unittest discover -s python -p 'test_blk_pipe_dry_run_orchestrator.py' -k preserves_true_allowed_new_payload -v
test_dry_run_fixture_invocation_preserves_true_allowed_new_payload ... FAIL

AssertionError: Lists differ: ['dry_run_output.txt'] != []
```

This proved `run_blk_pipe_dry_run_fixture(...)` still mirrored `allowed_new_files` into `allowed_modified_files` before invoking BLK-pipe.

### 4.2 GREEN

After implementation, the focused Task 2 verification passed:

```text
$ go test ./internal/pipe -run 'TestRunAllowedNew|TestRun.*DryRun|TestRun.*Unauthorized' -v
PASS
ok  	github.com/camcamcami/BLK-System/internal/pipe	1.073s

$ python3 -m unittest discover -s python -p 'test_blk_pipe_dry_run_orchestrator.py' -v
Ran 15 tests in 0.403s
OK

$ python3 -m unittest discover -s python -p 'test_beo_fixture_projection.py' -v
Ran 7 tests in 0.049s
OK
```

---

## 5. Deterministic Review Results

Because this sprint explicitly forbids live tactical LLMs, review was performed with deterministic local gates instead of delegated reviewer agents.

### 5.1 Spec / Traceability Gate

```text
SPEC_TRACEABILITY_GATE PASS
```

The gate verified:

- exactly the expected Task 2 files changed,
- `internal/pipe/run.go` contains a narrow `0664` -> `0644` allowed-new normalization helper,
- the Go regression exists and proves `umask 0002` true-new-file success,
- the Python dry-run helper no longer mirrors `allowed_new_files` into `allowed_modified_files`,
- Python fixture tests no longer pre-seed `dry_run_output.txt`,
- docs record the true `allowed_new_files` proof and safety rule,
- the Sprint 004 closeout caveat is marked resolved by Sprint 005 Task 2.

### 5.2 Safety / Docs Gate

```text
SAFETY_DOCS_GATE PASS
```

The gate verified:

- touched runtime/test fixture files do not introduce live network/model/Codex invocation patterns or `shell=True`,
- touched Markdown files have final newlines,
- Markdown fences are balanced,
- no trailing whitespace was introduced.

### 5.3 Repository Safety Greps

The following deterministic greps passed with no matches:

```text
production broad-staging grep -> PASS
production direct-Git grep    -> PASS
triple-dot diff grep          -> PASS
```

---

## 6. Final Verification

Focused verification:

```text
$ go test ./internal/pipe -run 'TestRunAllowedNew|TestRun.*DryRun|TestRun.*Unauthorized' -v
PASS
ok  	github.com/camcamcami/BLK-System/internal/pipe	1.073s

$ python3 -m unittest discover -s python -p 'test_blk_pipe_dry_run_orchestrator.py' -v
Ran 15 tests in 0.403s
OK

$ python3 -m unittest discover -s python -p 'test_beo_fixture_projection.py' -v
Ran 7 tests in 0.049s
OK
```

Shared verification before commit:

```text
$ python3 -m unittest discover -s python -p 'test_*.py'
Ran 49 tests in 0.613s
OK

$ go test ./...
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	0.059s
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	6.740s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)

$ go vet ./...
PASS

$ git diff --check
PASS
```

Final verification after commit, before push:

```text
$ python3 -m unittest discover -s python -p 'test_*.py'
Ran 49 tests in 0.718s
OK

$ go test ./...
ok  	github.com/camcamcami/BLK-System/internal/pipe	6.741s
[all packages PASS]

$ go vet ./...
PASS

$ git diff --check HEAD^ HEAD
PASS

$ git status --short --branch
## main...origin/main [ahead 1]
```

Implementation commit and push:

```text
[main 99c88f2] fix: support true blk-pipe allowed_new files
 7 files changed, 103 insertions(+), 18 deletions(-)

$ git push origin main
29458e0..99c88f2  main -> main

$ git status --short --branch
## main...origin/main
```

---

## 7. Deviations / Notes

- The implementation chose normalization rather than broad permission acceptance: `0664` safe non-executable allowed-new files are normalized to `0644` before staging. This keeps the worktree and Git tree deterministic while preserving safety checks for unsafe file types and modes.
- The Python test default binary was moved from `/tmp/blk-pipe-sprint-004` to `/tmp/blk-pipe-sprint-005` to avoid stale-binary false failures and to ensure the tests build against current source by default.
- `docs/outcomes/BLK-PIPE-004_sprint-closeout.md` was updated only to mark the Sprint 004 Task 5 caveat as resolved by Sprint 005 Task 2; the historical Sprint 004 evidence was not rewritten.
- No live Codex, tactical LLM, network model service, cyber tooling, live BLK-test MCP, RTM generation, or authoritative BEO publication was performed.

---

## 8. Next Task

Next planned task: Task 3 — Align BLK-pipe Status Taxonomy Through BLK-test Handoff.
