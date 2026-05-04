# BLK-pipe Sprint 003 — Task 5 Outcome

**Status:** Complete
**Date:** 2026-05-04
**Task:** Preserve Adapter Status Fidelity
**Commit:** `144c1c9 fix: preserve blk-pipe adapter status detail`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Make the Python adapter preserve parsed Go report status when the status is more specific than the exit-code family, especially distinguishing `INVALID_PAYLOAD` from `SYNTAX_GATE_FAILED` under exit code `2`.

This implements the task in the BLK-001 context by keeping BLK-pipe and its adapter as deterministic transport and safety infrastructure:

- The adapter uses the process return code as a mechanical routing family.
- The adapter preserves only known report statuses compatible with that family.
- Unknown nonzero exits cannot be promoted to `SUCCESS` by hostile or inconsistent JSON stdout.
- The adapter remains a local subprocess bridge only: no Codex invocation, no live LLM calls, no cyber execution, no Discord/HITL orchestration, and no shell invocation were added.

## 2. Files Added/Changed

Implementation commit `144c1c9` changed:

```text
docs/BLK-010_blk-pipe-v47-hardening-cli.md
python/blk_pipe_adapter.py
python/test_blk_pipe_adapter.py
```

Outcome document added separately:

```text
docs/outcomes/BLK-PIPE-003_task-005-outcome.md
```

## 3. Behavior Implemented

### 3.1 Status-family routing

`python/blk_pipe_adapter.py` now defines explicit status routing tables:

```text
0 -> SUCCESS
1 -> FATAL_SYSTEM_PANIC, FATAL_ENGINE_FAILED
2 -> INVALID_PAYLOAD, SYNTAX_GATE_FAILED
3 -> UNAUTHORIZED_FILE_MUTATION
4 -> INVALID_REVERT_ANCHOR
5 -> FATAL_OUTPUT_FLOOD
6 -> ENGINE_TIMEOUT
7 -> GIT_DIRTY
9 -> INTERNAL_ERROR
```

The adapter behavior is now:

- If the subprocess return code is known and parsed JSON contains a compatible `status`, preserve that report status.
- If the subprocess return code is known and parsed JSON contains a missing or incompatible `status`, use the deterministic family default.
- If the subprocess return code is unknown and nonzero, force `INTERNAL_ERROR` even when parsed JSON claims `SUCCESS`.
- If stdout is not JSON, preserve the existing `FATAL_CRASH` behavior.

### 3.2 Exit code 2 detail preservation

Exit code `2` now distinguishes:

```text
return 2 + report INVALID_PAYLOAD    -> INVALID_PAYLOAD
return 2 + report SYNTAX_GATE_FAILED -> SYNTAX_GATE_FAILED
```

This fixes the adapter fidelity gap where all exit-code-2 failures previously collapsed to `SYNTAX_GATE_FAILED`, which obscured invalid-payload failures at the Python integration boundary.

### 3.3 Safety and compatibility retained

The adapter still invokes BLK-pipe with argument-list subprocess calls:

```text
[binary_path, "--payload", temp_payload_path]
```

No shell execution was introduced. Existing temporary payload cleanup remains in the `finally` path and remains covered by tests for normal runs, timeout, and serialization failure.

### 3.4 Documentation

`docs/BLK-010_blk-pipe-v47-hardening-cli.md` now documents that the Python adapter treats the return code as the routing family while preserving compatible parsed report statuses, including the `INVALID_PAYLOAD` vs `SYNTAX_GATE_FAILED` distinction for exit code `2`.

## 4. TDD Evidence

### 4.1 RED

The implementation subagent first added the required status-preservation test before code changes.

Command:

```bash
python3 -m unittest discover -s python -p 'test_*.py'
```

Expected RED failure:

```text
FAIL: test_invalid_payload_status_preserved_for_exit_code_2
Expected: INVALID_PAYLOAD
Actual:   SYNTAX_GATE_FAILED
```

This demonstrated the pre-existing adapter collapse of exit code `2` to the family default.

### 4.2 GREEN

After implementation, the Python adapter suite passed:

```text
................
----------------------------------------------------------------------
Ran 16 tests in 0.369s

OK
```

Full Go test suite passed:

```text
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe
ok  	github.com/camcamcami/BLK-System/internal/contracts
ok  	github.com/camcamcami/BLK-System/internal/engine
ok  	github.com/camcamcami/BLK-System/internal/execguard
ok  	github.com/camcamcami/BLK-System/internal/gitguard
ok  	github.com/camcamcami/BLK-System/internal/pipe
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard
ok  	github.com/camcamcami/BLK-System/internal/testutil
ok  	github.com/camcamcami/BLK-System/internal/validation
```

`go vet ./...` completed successfully.

## 5. Review Results

### 5.1 Spec compliance review

Result: **PASS for implementation behavior; outcome document pending at review time.**

The spec reviewer confirmed:

- adapter uses return code as routing family;
- compatible parsed statuses are preserved;
- exit `2` preserves both `INVALID_PAYLOAD` and `SYNTAX_GATE_FAILED`;
- unknown nonzero return codes force `INTERNAL_ERROR`;
- non-JSON stdout still maps to `FATAL_CRASH`;
- required status-preservation tests are present;
- temp payload cleanup behavior appears unchanged;
- subprocess usage remains shell-free;
- no Codex/live LLM/cyber execution was added.

The only gap reported by the spec reviewer was that this outcome document had not yet been created. This document closes that gap.

### 5.2 Code quality and safety review

Result: **APPROVED.**

The code-quality reviewer confirmed:

- known nonzero codes preserve only statuses compatible with that return-code family;
- exit `2` now preserves the required status detail;
- unknown nonzero codes cannot report `SUCCESS`;
- exit `0` falls back to `SUCCESS` only within the success family;
- adapter subprocess calls remain argument-list invocations with no `shell=True`;
- temporary payload cleanup remains intact;
- docs match implementation behavior;
- adapter remains deterministic BLK-pipe bridge infrastructure and does not introduce live LLM/Codex/cyber scope.

The reviewer independently ran:

```text
python3 -m unittest discover -s python -p 'test_*.py'  -> PASS, 16 tests
go test ./...                                          -> PASS
go vet ./...                                           -> PASS
git diff --check HEAD^ HEAD                            -> PASS
```

## 6. Final Verification

Final controller verification before pushing the implementation commit:

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
! git grep -n -E 'exec\.Command(Context)?\("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go'
! git grep -n -E 'git[^\n]*diff[^\n]*\.\.\.' -- '*.go' ':!*_test.go' docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/plans/BLK-PIPE-003_integration-readiness-and-capability-profiles.md docs/outcomes/BLK-PIPE-003_task-00*-outcome.md
git diff --check HEAD^ HEAD
git status --short --branch
git push origin main
```

Observed verification summary:

```text
Python adapter tests: PASS, 16 tests
Go tests: PASS
go vet: PASS
direct production Git-call grep: PASS
broad-staging grep: PASS
triple-dot diff grep: PASS
git diff --check HEAD^ HEAD: PASS
git status before push: ## main...origin/main [ahead 1]
git push origin main: f48dbf4..144c1c9 main -> main
git status after push: ## main...origin/main
```

Python test execution created `python/__pycache__/`; it was removed before push and the implementation tree was clean.

## 7. Deviations / Notes

- The unknown-nonzero success-suppression behavior was already covered by an existing test; that test was preserved rather than duplicated under a new exact function name.
- The docs update was intentionally narrow and limited to the Python adapter status-fidelity paragraph in `docs/BLK-010_blk-pipe-v47-hardening-cli.md`.
- No BLK-001 architecture semantics were interpreted by the adapter. The adapter does not parse requirement/use-case bodies, verify trace artifact hashes, generate RTM/CEO artifacts, or make autonomous decisions.
- No live Codex, live LLM, or cyber-execution path was enabled.

## 8. Next Task

Next planned Sprint 003 task: **Task 6 — Document Integration Readiness and Capability Profiles**.
