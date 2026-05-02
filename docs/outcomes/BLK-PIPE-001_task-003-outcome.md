# BLK-pipe Sprint 001 — Task 3 Outcome

**Status:** Complete
**Date:** 2026-05-02
**Task:** Add Git test repository utility
**Commit:** `fc2bd98 test: add git repository test utility`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Provide reusable test helpers for integration tests that require real temporary Git repositories.

This task creates test infrastructure only. It intentionally does **not** implement BLK-pipe execution, Git staging policy, cleanup, commit orchestration, Codex integration, or BLK-test integration.

---

## 2. Files Added

```text
internal/testutil/gitrepo.go
internal/testutil/gitrepo_test.go
```

---

## 3. Helpers Implemented

```go
func NewGitRepo(t testing.TB) string
func WriteFile(t testing.TB, repo string, rel string, content string)
func RunGit(t testing.TB, repo string, args ...string) string
```

### 3.1 `NewGitRepo`

Creates a temporary Git repository suitable for integration tests.

Verified behavior:

- creates a temp directory,
- runs `git init`,
- configures local `user.name`,
- configures local `user.email`,
- creates an initial commit,
- returns the repo path,
- leaves the worktree clean.

### 3.2 `WriteFile`

Writes a file under a temp repo and creates parent directories as needed.

### 3.3 `RunGit`

Runs `git` in the provided repo directory, returns combined output for assertions/debugging, and fails the test via `t.Fatalf` on non-zero exit.

---

## 4. Hermetic Git Environment Hardening

The initial implementation passed normal tests but code review identified hidden global-environment hazards. The final implementation now filters inherited `GIT_*` environment variables for helper Git invocations and then explicitly sets:

```text
GIT_CONFIG_GLOBAL=/dev/null
GIT_CONFIG_NOSYSTEM=1
```

This prevents test behavior from being changed by:

- hostile global `core.hooksPath`,
- env-injected `commit.gpgsign=true`,
- hostile `GIT_TEMPLATE_DIR`,
- hostile `GIT_DIR`,
- other repo-shaping inherited `GIT_*` variables.

Non-Git environment such as `PATH` and `HOME` remains available.

---

## 5. TDD Evidence

### 5.1 RED

Tests were written before production code.

Initial failing command:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/testutil -run TestNewGitRepoCreatesCleanRepositoryWithInitialCommit -v
```

Failure evidence included missing helper symbols:

```text
undefined: NewGitRepo
undefined: RunGit
```

Additional code-review-driven RED tests were added before each robustness fix:

- hostile global `core.hooksPath` caused the initial commit to run a failing pre-commit hook,
- env-injected `commit.gpgsign=true` caused Git to attempt GPG signing,
- hostile `GIT_TEMPLATE_DIR` caused a template pre-commit hook to run,
- inherited `GIT_DIR` caused Git to operate against an external repository.

Each failed before the corresponding hermeticity fix was added.

### 5.2 GREEN

Final focused verification:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/testutil -v
```

Verified tests:

```text
TestNewGitRepoIgnoresEnvironmentConfigInjection
TestNewGitRepoIgnoresGlobalHooksPath
TestNewGitRepoIgnoresTemplateDirHooks
TestNewGitRepoIgnoresInheritedGitDir
TestNewGitRepoCreatesCleanRepositoryWithInitialCommit
TestWriteFileCreatesParentsAndRunGitReturnsOutput
```

All passed.

Full verification:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./...
git diff --check
```

All passed.

---

## 6. Review Results

### 6.1 Initial Spec Compliance Review

Verdict: **PASS**

Gaps: none.

### 6.2 Initial Code Quality Review

Verdict: **REQUEST_CHANGES**

Issue found:

- Git commands inherited global/system config; hostile `core.hooksPath` could break the initial commit.

### 6.3 First Fix

Added environment isolation for global/system Git config:

```text
GIT_CONFIG_GLOBAL=/dev/null
GIT_CONFIG_NOSYSTEM=1
```

### 6.4 Second Code Quality Review

Verdict: **REQUEST_CHANGES**

Issue found:

- environment-based Git config injection (`GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_*`, `GIT_CONFIG_VALUE_*`, `GIT_CONFIG_PARAMETERS`) could still override local config.

### 6.5 Second Fix

Filtered env-based Git config injection and added regression coverage.

### 6.6 Third Code Quality Review

Verdict: **REQUEST_CHANGES**

Issue found:

- inherited repo-shaping variables such as `GIT_TEMPLATE_DIR` and `GIT_DIR` could still mutate behavior.

### 6.7 Final Fix

Filtered inherited `GIT_*` variables broadly, then explicitly restored only safe Git environment overrides required by the helper.

### 6.8 Final Reviews

Spec compliance: **PASS**

Code quality: **APPROVED**

Critical issues: none.
Important issues: none.
Minor issues: none.

---

## 7. Final Verification

Final verification before push:

```bash
export PATH="$HOME/.local/bin:$PATH"; gofmt -l internal/testutil/gitrepo.go internal/testutil/gitrepo_test.go internal/contracts/payload.go internal/contracts/report.go internal/contracts/payload_test.go cmd/blk-pipe/main.go cmd/blk-pipe/main_test.go internal/pipe/exitcodes.go internal/pipe/exitcodes_test.go
export PATH="$HOME/.local/bin:$PATH"; go test ./internal/testutil -v
export PATH="$HOME/.local/bin:$PATH"; go test ./...
git diff --check
git status --short --branch
```

Result:

```text
gofmt check                  PASS
go test ./internal/testutil  PASS
go test ./...                PASS
git diff --check             PASS
repo state after push        clean, aligned with origin/main
```

---

## 8. Deviations / Notes

- No production BLK-pipe execution behavior was added.
- No external Go dependencies were added.
- Review-driven hardening expanded the helper beyond the original minimal spec, but only to make future integration tests hermetic and reliable.
- `WriteFile` remains a trusted internal test helper and does not enforce repo confinement against `..` or absolute paths.

---

## 9. Next Task

Proceed to Sprint 001 Task 4: implement the preflight clean-repo check in `internal/gitguard/status.go` using the new `internal/testutil` Git repository helper.
