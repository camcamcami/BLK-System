# BLK-pipe Sprint 002 — Task 10 Outcome

**Status:** Complete
**Date:** 2026-05-03
**Task:** Add Python Adapter Skeleton and Tests
**Commit:** `91aa93bae0272aa0277279f45e816f32423d04d3 feat: add blk-pipe python adapter`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Task 10 introduced a local Python adapter around the existing `blk-pipe --payload <tempfile>` CLI path, matching the BLK-004/V47 adapter expectations without invoking Codex, OpenAI, a local LLM, or any live tactical engine.

The adapter is intentionally thin: it writes a JSON payload to a temporary file, shells out to the deterministic Go `blk-pipe` binary without using a shell, parses the resulting JSON report, and routes control flow by POSIX return code.

---

## 2. Files Added/Changed

Added:

- `python/blk_pipe_adapter.py`
- `python/test_blk_pipe_adapter.py`

No production Go files were modified for this task.

Implementation commit stats:

```text
91aa93b feat: add blk-pipe python adapter
 python/blk_pipe_adapter.py      | 159 ++++++++++++++++++++
 python/test_blk_pipe_adapter.py | 311 ++++++++++++++++++++++++++++++++++++++++
 2 files changed, 470 insertions(+)
```

---

## 3. Behavior Implemented

`python/blk_pipe_adapter.py` now provides:

- `ExecutionResult` dataclass with V47-compatible result fields:
  - `status`
  - `exit_code`
  - `pre_engine_hash`
  - `git_diff`
  - `engine_logs`
  - `validation_logs`
  - `diff_summary`
  - `error`
  - `untracked_files`
- `BlkPipeAdapter(binary_path="blk-pipe")`
- `run_health_check()` invoking `[binary_path, "--health"]` without a shell.
- `execute_sprint(...)` that writes an execute payload with:
  - `action: "execute"`
  - `ceb_id`
  - `work_dir`
  - `target_branch`
  - `engine`
  - `engine_args`
  - `l2_packet`
  - `validation_commands`
  - `allowed_modified_files`
  - `allowed_new_files`
- `abort_sprint_and_revert(...)` that writes a revert payload with:
  - `action: "revert"`
  - `work_dir`
  - `target_branch`
  - `target_hash` from `pre_engine_hash`
  - `ceb_id: "REVERT"`
  - empty engine, L2 packet, validation, and allowlist fields.
- `_invoke_binary(...)` using `tempfile.NamedTemporaryFile(delete=False, suffix=".json")`, invoking `[binary_path, "--payload", temp_payload_path]` without a shell, parsing stdout JSON, and always attempting temporary payload cleanup in `finally`.

Return-code routing implemented:

```text
0 -> parsed report status, default SUCCESS
1 -> FATAL_SYSTEM_PANIC
2 -> SYNTAX_GATE_FAILED
3 -> UNAUTHORIZED_FILE_MUTATION
4 -> INVALID_REVERT_ANCHOR
5 -> FATAL_OUTPUT_FLOOD
6 -> ENGINE_TIMEOUT
7 -> GIT_DIRTY
9 -> INTERNAL_ERROR
unknown nonzero -> INTERNAL_ERROR
```

The strict V47 router codes remain `0-5`; local extension codes `6`, `7`, and `9` are handled defensively so nonzero local failures cannot be misreported as success.

Error paths implemented:

- Non-JSON stdout returns `ExecutionResult(status="FATAL_CRASH", ...)` with stderr context.
- `subprocess.TimeoutExpired` returns `ExecutionResult(status="FATAL_PYTHON_TIMEOUT", exit_code=1, validation_logs={}, ...)`.
- Temporary payload files are removed after normal runs, timeout runs, and payload serialization failures.

---

## 4. TDD Evidence

### 4.1 RED

Initial Task 10 RED evidence before adapter implementation:

```text
Command: python3 -m unittest discover -s python -p 'test_*.py'
Failure: ModuleNotFoundError: No module named 'blk_pipe_adapter'
Result: FAILED (errors=1)
```

After the first review gate requested hardening, regression tests were added before fixes. RED evidence:

```text
Command: python3 -m unittest discover -s python -p 'test_*.py'
Result: FAILED (failures=6)

Observed failures:
- return code 6 reported SHOULD_BE_OVERRIDDEN instead of ENGINE_TIMEOUT
- return code 7 reported SHOULD_BE_OVERRIDDEN instead of GIT_DIRTY
- return code 9 reported SHOULD_BE_OVERRIDDEN instead of INTERNAL_ERROR
- unknown return code 42 with {} stdout reported SUCCESS
- unknown return code 42 with {"status":"SUCCESS"} stdout reported SUCCESS
- payload serialization failure left a temp .json file behind
```

### 4.2 GREEN

Focused Python adapter suite after implementation and review fixes:

```text
Command: python3 -m unittest discover -s python -p 'test_*.py'
.........
----------------------------------------------------------------------
Ran 9 tests in 0.256s

OK
```

Go regression suite after implementation:

```text
Command: export PATH="$HOME/.local/bin:$PATH" && go test ./...
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)
```

Health check smoke:

```text
Command: go run ./cmd/blk-pipe --health
{"status":"OK","component":"blk-pipe"}
```

---

## 5. Review Results

### 5.1 Spec Compliance Review

Final spec-compliance subagent result:

```text
PASS
```

The reviewer confirmed the implementation satisfies the Task 10 public API, payload shape, no-shell invocation, strict V47 return-code routing, fake-binary unittest coverage, temp-file cleanup expectations, and no live Codex/LLM integration.

### 5.2 Code Quality / Safety Review

First code-quality review result:

```text
Verdict: REQUEST_CHANGES
```

The reviewer identified three hardening gaps:

1. Nonzero local extension or unknown exit codes could be reported as success.
2. Temporary file cleanup did not cover payload serialization failures.
3. Timeout behavior was implemented but untested.

Fixes were implemented with failing regression tests first, then the unpushed implementation commit was amended.

Final code-quality review result:

```text
Critical Issues: None.
Important Issues: None.
Minor Issues: None.
Verdict: APPROVED
```

The reviewer confirmed:

- no `shell=True` or command-string subprocess invocation,
- robust temp payload cleanup for normal, timeout, and serialization-failure paths,
- deterministic JSON parse and timeout behavior,
- unknown/local-extension nonzero return codes cannot report success,
- tests are local/deterministic and do not call external network services, GitHub, Codex, or LLMs.

---

## 6. Final Verification

Controller final verification before pushing the implementation commit:

```text
Command:
set -e
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
git diff --check
git status --short --branch
git log --oneline --decorate -4
git push origin main
git status --short --branch

Result:
.........
----------------------------------------------------------------------
Ran 9 tests in 0.256s

OK
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)
91aa93b (HEAD -> main) feat: add blk-pipe python adapter
7464eff (origin/main) docs: record BLK-pipe sprint 002 task 9 outcome
2d7582c feat: add blk-pipe branch preparation
45c1c7a docs: record BLK-pipe sprint 002 task 8 outcome
To https://github.com/camcamcami/BLK-System.git
   7464eff..91aa93b  main -> main
```

A generated `python/__pycache__/` directory appeared after Python test execution and was removed before writing this outcome document. Final implementation status after cleanup:

```text
## main...origin/main
```

---

## 7. Deviations / Notes

- Task 10 did not modify README or Sprint 001/Sprint 002 docs; the plan made that optional only if documentation needed to point at the adapter. The matching outcome document records the new adapter path.
- No Codex, OpenAI, local LLM, or live tactical engine integration was introduced.
- The implementation defensively handles local extension return codes `6`, `7`, and `9` in addition to strict V47 router codes `0-5`; this avoids reporting local nonzero failures as success while preserving the strict V47 code separation documented in Sprint 002.
- The adapter uses Python standard-library `unittest` only.

---

## 8. Next Task

Next incomplete Sprint 002 task after Task 10 is Task 11 — Sprint 002 Documentation and Closeout.

Expected next files from the plan:

- create `docs/BLK-010_blk-pipe-v47-hardening-cli.md`,
- create `docs/outcomes/BLK-PIPE-002_sprint-002-closeout.md`,
- update `README.md`,
- commit `docs: describe blk-pipe v47 hardening layer`,
- commit `docs: close out blk-pipe sprint 002`.
