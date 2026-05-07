# BLK-SYSTEM-020 — Task 002 Outcome

**Task:** Implement repository-owned validation profile registry  
**Status:** Complete  
**Date:** 2026-05-07T20:24:00+10:00

---

## 1. Objective

Add the Go validation profile registry and payload/report contract needed to turn profile names into deterministic repository-owned command arrays.

---

## 2. Files Changed

```text
internal/validationprofiles/profiles.go
internal/validationprofiles/profiles_test.go
internal/contracts/payload.go
internal/contracts/payload_test.go
internal/contracts/report.go
internal/contracts/report_test.go
docs/outcomes/BLK-SYSTEM-020_task-002-outcome.md
```

---

## 3. Behavior Implemented

- Added `internal/validationprofiles` with the initial approved local-only profile set:
  - `go-test` -> `go test ./...`
  - `go-vet` -> `go vet ./...`
  - `go-full` -> `go test ./...`; `go vet ./...`
  - `python-unittest` -> local Python unittest discovery
  - `docs-doctrine-gates` -> active doctrine unittest gate
- Added validation for unknown, duplicate, and empty profile names.
- Added defensive-copy resolution so callers cannot mutate registry state.
- Added `validation_profiles` support to the Go payload contract.
- Added fail-closed rejection for mixed `validation_profiles` and `validation_commands`.
- Added resolved validation command storage on decoded payloads.
- Added report evidence fields for profile source, requested profiles, and resolved commands.
- Preserved legacy `validation_commands` as trusted-local compatibility only when profiles are absent.

---

## 4. TDD Evidence

### 4.1 Prior RED from Task 001

```text
internal/contracts/payload_test.go:184:27: payload.ValidationProfiles undefined
internal/contracts/report_test.go:102:3: unknown field ValidationCommandSource in struct literal of type Report
internal/contracts/report_test.go:103:3: unknown field ValidationProfiles in struct literal of type Report
internal/contracts/report_test.go:104:3: unknown field ResolvedValidationCommands in struct literal of type Report
```

### 4.2 Focused GREEN

Commands run:

```bash
go test ./internal/validationprofiles ./internal/contracts -count=1
go test ./internal/contracts -run 'TestDecodePayload.*ValidationProfile|TestReport.*ValidationProfile|TestDecodePayload.*Legacy' -count=1
```

Observed output:

```text
ok  	github.com/camcamcami/BLK-System/internal/validationprofiles	0.002s
ok  	github.com/camcamcami/BLK-System/internal/contracts	0.014s
ok  	github.com/camcamcami/BLK-System/internal/contracts	0.002s
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
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	0.067s
ok  	github.com/camcamcami/BLK-System/internal/contracts	0.045s
ok  	github.com/camcamcami/BLK-System/internal/pipe	6.984s
ok  	github.com/camcamcami/BLK-System/internal/validationprofiles	0.002s
Ran 313 tests in 6.401s
OK
```

`go vet ./...` and `git diff --check` produced no errors.

---

## 6. Non-Execution / No-Authority-Expansion Statement

Task 002 did not invoke Hindsight, Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads/copying/parsing/hashing/mutation, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, or source mutation outside exact approved allowlists.

The task only added repository-owned validation profile contract support; Task 003 owns BLK-pipe execution wiring.

---

## 7. Next Task

Task 003 must wire resolved profile commands into BLK-pipe execution and add Python adapter payload support.
