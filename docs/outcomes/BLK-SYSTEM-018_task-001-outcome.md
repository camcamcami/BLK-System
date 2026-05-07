# BLK-SYSTEM-018 — Task 001 Outcome

**Task:** Task 1 — Add RED Tests for Protected Vault Allowlist Exit 3 Routing
**Status:** Complete — RED test gap exposed
**Date:** 2026-05-07T17:40:49+10:00
**Repository:** `/home/dad/BLK-System`
**Source finding:** `BLOCKING-1` in `docs/reviews/BLK-SYSTEM_current-implementation_BLK-001-through-BLK-006_hostile-alignment-review.md`

---

## 1. Objective

Task 001 converted the existing protected-docs allowlist regression into the Sprint 018 target behavior: protected BLK-req vault allowlist entries under `docs/active/`, `docs/requirements/`, and `docs/use_cases/` must route as `UNAUTHORIZED_FILE_MUTATION` / POSIX Exit 3 instead of ordinary `INVALID_PAYLOAD` / Exit 2.

This task intentionally changed only tests and documentation. It did not patch production routing.

---

## 2. Files Changed

```text
internal/pipe/run_test.go
docs/outcomes/BLK-SYSTEM-018_task-001-outcome.md
```

---

## 3. Tests Added / Changed

`internal/pipe/run_test.go` now contains:

```text
TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation
```

The table covers:

```text
allowed_modified_files -> docs/active/REQ-001.md
allowed_modified_files -> docs/requirements/REQ-001.md
allowed_new_files      -> docs/use_cases/UC-001.md
allowed_new_files      -> docs/active/UC-001.md
```

Each case uses an engine sentinel command that would create `engine-ran.txt` if execution incorrectly proceeds, and asserts the repo remains clean.

---

## 4. RED Evidence

Command:

```text
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestRunProtectedVaultAllowlist' -count=1 -v
```

Observed RED failure excerpt:

```text
=== RUN   TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation
=== RUN   TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation/active_modified
    run_test.go:2951: exit code = 2, want 3; report={Status:INVALID_PAYLOAD ExitCode:2 ... Error:allowed_modified_files entry "docs/active/REQ-001.md" matches protected docs/active path}
=== RUN   TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation/requirements_modified
    run_test.go:2951: exit code = 2, want 3; report={Status:INVALID_PAYLOAD ExitCode:2 ... Error:allowed_modified_files entry "docs/requirements/REQ-001.md" matches protected docs/requirements path}
=== RUN   TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation/use-cases_new
    run_test.go:2951: exit code = 2, want 3; report={Status:INVALID_PAYLOAD ExitCode:2 ... Error:allowed_new_files entry "docs/use_cases/UC-001.md" matches protected docs/use_cases path}
=== RUN   TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation/active_new
    run_test.go:2951: exit code = 2, want 3; report={Status:INVALID_PAYLOAD ExitCode:2 ... Error:allowed_new_files entry "docs/active/UC-001.md" matches protected docs/active path}
--- FAIL: TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation
FAIL
```

This is the expected RED: current production code classifies protected allowlist hits as `INVALID_PAYLOAD` / Exit 2.

---

## 5. Verification

```text
gofmt -w internal/pipe/run_test.go
git diff --check
exit 0, no output
```

Full shared verification is intentionally deferred to Task 002 because Task 001 commits a RED regression test that is expected to fail until the production routing fix lands.

---

## 6. Non-Execution Statement

Task 001 did not invoke Codex or live tactical LLMs, did not call network model services, did not run cyber tooling, did not start production BLK-test MCP, did not read or mutate protected BLK-req vault bodies, did not generate RTM, did not assert RTM drift rejection authority, and did not publish authoritative BEOs.

---

## 7. Next Task

Task 002 patches `internal/contracts/payload.go` and `internal/pipe/run.go` so the RED test passes while ordinary malformed payloads remain Exit 2.
