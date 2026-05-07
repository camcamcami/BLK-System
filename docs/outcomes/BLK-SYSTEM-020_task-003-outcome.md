# BLK-SYSTEM-020 — Task 003 Outcome

**Task:** Wire validation profiles through BLK-pipe execution and Python adapter payloads  
**Status:** Complete  
**Date:** 2026-05-07T20:33:00+10:00

---

## 1. Objective

Ensure BLK-pipe runs resolved profile commands from the repository-owned Go registry, reports profile evidence, preserves validation cleanup semantics, and lets the Python adapter construct profile-based payloads without becoming the enforcement authority.

---

## 2. Files Changed

```text
internal/pipe/run.go
internal/pipe/run_test.go
python/blk_pipe_adapter.py
python/test_blk_pipe_adapter.py
docs/outcomes/BLK-SYSTEM-020_task-003-outcome.md
```

---

## 3. Behavior Implemented

- BLK-pipe now runs `payload.ResolvedValidationCommands` instead of raw payload `validation_commands`.
- Reports now include:
  - `validation_command_source` (`profile`, `legacy`, or `none`);
  - `validation_profiles`;
  - `resolved_validation_commands`.
- Profile-based validation success is covered with a hermetic temp Go module using the `go-test` profile.
- Profile-based validation failure routes to `SYNTAX_GATE_FAILED` / POSIX Exit 2 and restores the candidate mutation to the pre-engine hash.
- Python adapter can emit `validation_profiles` payloads and omits `validation_commands` in that mode.
- Python adapter rejects locally if both `validation_profiles` and `validation_commands` are supplied.
- Python adapter remains a payload construction convenience layer; Go remains final enforcement authority.

---

## 4. TDD Evidence

### 4.1 RED

Commands run after adding focused tests:

```bash
go test ./internal/pipe -run 'TestRun.*ValidationProfile|TestRun.*ValidationFailure' -count=1
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_pipe_adapter -v
```

Observed RED summary:

```text
--- FAIL: TestRunValidationProfileExecutesResolvedCommandsAndReportsEvidence
    ValidationCommandSource = "", want profile
--- FAIL: TestRunValidationProfileFailureRoutesToSyntaxGateAndCleans
    exit code = 0, want 2
FAIL	github.com/camcamcami/BLK-System/internal/pipe

ERROR: test_execute_sprint_writes_validation_profiles_and_omits_commands
TypeError: BlkPipeAdapter.execute_sprint() got an unexpected keyword argument 'validation_profiles'

ERROR: test_execute_sprint_rejects_mixed_validation_profiles_and_commands
TypeError: BlkPipeAdapter.execute_sprint() got an unexpected keyword argument 'validation_profiles'
```

### 4.2 Focused GREEN

Commands run after implementation:

```bash
go test ./internal/pipe -run 'TestRun.*ValidationProfile|TestRun.*ValidationFailure' -count=1
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_pipe_adapter -v
```

Observed GREEN summary:

```text
ok  	github.com/camcamcami/BLK-System/internal/pipe	0.488s
Ran 22 tests in 0.447s
OK
```

---

## 5. Shared Verification

Commands run:

```bash
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
```

Observed output summary:

```text
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	0.039s
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	7.480s
ok  	github.com/camcamcami/BLK-System/internal/validationprofiles	(cached)
Ran 315 tests in 6.388s
OK
```

`go vet ./...` and `git diff --check` produced no errors.

---

## 6. Profile Report Evidence

Profile-mode reports now carry these keys:

```text
validation_command_source
validation_profiles
resolved_validation_commands
validation_logs
```

The focused pipe test asserts `validation_command_source == "profile"`, `validation_profiles == ["go-test"]`, and `resolved_validation_commands == ["go test ./..."]`.

---

## 7. Non-Execution / No-Authority-Expansion Statement

Task 003 did not invoke Hindsight, Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads/copying/parsing/hashing/mutation, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, or source mutation outside exact approved allowlists.

The task only wired repository-owned validation profile commands through existing local BLK-pipe validation execution and adapter payload construction.

---

## 8. Next Task

Task 004 must patch BLK-004 doctrine and persistent review gates to preserve the validation profile authority boundary.
