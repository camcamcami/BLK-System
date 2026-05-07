# BLK-SYSTEM-018 — Task 002 Outcome

**Task:** Task 2 — Route Protected Vault Allowlist Hits to Exit 3
**Status:** Complete
**Date:** 2026-05-07T17:44:39+10:00
**Repository:** `/home/dad/BLK-System`
**Task 1 RED commit:** `c47dba2 test: expose protected vault exit routing gap`

---

## 1. Objective

Task 002 patched BLK-pipe payload/run routing so protected BLK-req vault allowlist hits under `docs/active/`, `docs/requirements/`, and `docs/use_cases/` return `UNAUTHORIZED_FILE_MUTATION` / POSIX Exit 3.

Ordinary malformed payloads continue to route through `INVALID_PAYLOAD` / Exit 2.

---

## 2. Files Changed

```text
internal/contracts/payload.go
internal/pipe/run.go
internal/pipe/run_test.go
docs/outcomes/BLK-SYSTEM-018_task-002-outcome.md
```

`internal/pipe/run_test.go` is staged because it carries the Task 001 RED tests that now pass after the Task 002 production fix.

---

## 3. Behavior Implemented

- Added exported path-string classifiers in `internal/contracts/payload.go`:
  - `IsProtectedDocsPath(...)`
  - `ProtectedDocsPrefix(...)`
  - `HasProtectedDocsAllowlistEntry(...)`
- Preserved existing contract-level validation: protected paths are still invalid payload content at the contract boundary.
- Added pipe-level classification in `parseAndValidatePayload(...)`: if decode/validation returns an error and the partially decoded allowlists contain a protected BLK-req vault path, BLK-pipe reports `UNAUTHORIZED_FILE_MUTATION` and returns `ExitUnauthorizedMutation`.
- Kept the classifier path-string-only. It does not stat, open, parse, hash, or read protected BLK-req vault files.
- Engine execution remains skipped because classification happens before execute-mode engine startup.

---

## 4. TDD Evidence

### 4.1 RED Reference

Task 001 captured the expected failure:

```text
TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation
exit code = 2, want 3; report={Status:INVALID_PAYLOAD ExitCode:2 ... protected docs/... path}
```

### 4.2 GREEN Focused Test

Command:

```text
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestRunProtectedVaultAllowlist' -count=1 -v
```

Output:

```text
=== RUN   TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation
=== RUN   TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation/active_modified
=== RUN   TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation/requirements_modified
=== RUN   TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation/use-cases_new
=== RUN   TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation/active_new
--- PASS: TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation (0.05s)
    --- PASS: TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation/active_modified (0.01s)
    --- PASS: TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation/requirements_modified (0.01s)
    --- PASS: TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation/use-cases_new (0.01s)
    --- PASS: TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation/active_new (0.01s)
PASS
ok  	github.com/camcamcami/BLK-System/internal/pipe	0.052s
```

### 4.3 Regression Command

```text
go test ./internal/contracts ./internal/pipe -count=1
ok  	github.com/camcamcami/BLK-System/internal/contracts	0.019s
ok  	github.com/camcamcami/BLK-System/internal/pipe	7.148s
```

---

## 5. Shared Verification

Command block:

```text
export PATH="$HOME/.local/bin:$PATH"
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

Output:

```text
Ran 310 tests in 6.755s
OK

ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	0.058s
ok  	github.com/camcamcami/BLK-System/internal/contracts	0.035s
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	7.818s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)

go vet ./...
exit 0, no output

git diff --check
exit 0, no output
```

---

## 6. Review Notes

- Protected body reads were not introduced; classification uses only payload path strings already present in the JSON payload.
- Ordinary malformed payloads still route to `INVALID_PAYLOAD` / Exit 2 when no protected allowlist path is present.
- No allowlist semantics were broadened.
- The engine sentinel cases prove protected allowlist payloads do not start the engine.

---

## 7. Non-Execution Statement

Task 002 did not invoke Codex or live tactical LLMs, did not call network model services, did not run cyber tooling, did not start production BLK-test MCP, did not read or mutate protected BLK-req vault bodies, did not generate RTM, did not assert RTM drift rejection authority, and did not publish authoritative BEOs.

---

## 8. Next Task

Task 003 adds RED tests exposing the revert clean-preflight reachability gap.
