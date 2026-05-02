# BLK-pipe Sprint 001 — Task 4 Outcome

**Status:** Complete
**Date:** 2026-05-02
**Task:** Implement preflight clean-repo check
**Commit:** `8fa61c6 feat: enforce clean git preflight`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Abort BLK-pipe execution before the fake engine starts if the target Git worktree is dirty.

This task adds the first safety preflight in `internal/gitguard`: a deterministic clean-repository check that detects both tracked modifications and untracked files before later sprint tasks add engine execution, allowlist staging, unauthorized mutation cleanup, and orchestration.

This task intentionally does **not** implement engine execution, staging policy, unauthorized mutation cleanup, report emission, Codex integration, Discord integration, or BLK-req artifact mutation behavior.

---

## 2. Files Added

```text
internal/gitguard/status.go
internal/gitguard/status_test.go
```

---

## 3. Behavior Implemented

### 3.1 Public API

```go
func EnsureClean(repo string) error
```

`EnsureClean` verifies that the supplied path is a clean Git repository before any engine process is allowed to run.

### 3.2 Clean repository behavior

A repository is considered clean only when Git reports no tracked modifications and no untracked files.

Implementation command:

```bash
git status --porcelain --untracked-files=all
```

Empty output means the repository is clean and `EnsureClean` returns `nil`.

### 3.3 Dirty repository behavior

Any non-empty porcelain status output returns a typed `*DirtyError`:

```go
type DirtyError struct {
    Status string
}
```

The raw Git status output is preserved in `DirtyError.Status` so later BLK-pipe orchestration can distinguish a deliberate dirty-preflight rejection from an infrastructure failure.

Covered dirty cases:

- modified tracked file,
- untracked file,
- untracked file when local repo config sets `status.showUntrackedFiles=no`.

The implementation uses explicit `--untracked-files=all` so local repository config cannot hide untracked files from the safety preflight.

### 3.4 Git infrastructure failure behavior

If `git status` itself fails, `EnsureClean` returns a normal error that includes:

- the command context,
- the repository path,
- the wrapped Git command error,
- Git stderr/stdout when available.

This is covered by a non-Git-directory test that asserts the returned error includes Git's `not a git repository` diagnostic.

### 3.5 Git environment hardening

The status check filters inherited `GIT_*` environment variables, then explicitly sets:

```text
GIT_CONFIG_GLOBAL=/dev/null
GIT_CONFIG_NOSYSTEM=1
```

This mirrors the hermetic Git discipline established by Task 3's test utility and reduces the risk that global/system Git configuration or inherited Git environment variables alter preflight behavior.

---

## 4. TDD Evidence

### 4.1 RED

Tests were written before production implementation.

Initial focused test command:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/gitguard -run TestCleanRepo -v
```

Initial failure evidence included missing `gitguard` implementation symbols because `internal/gitguard/status.go` did not exist yet.

The final test suite covers the original required cases plus review-driven hardening cases:

```text
TestCleanRepo/clean_repo_returns_nil
TestCleanRepo/modified_tracked_file_returns_dirty_error
TestCleanRepo/untracked_file_returns_dirty_error
TestCleanRepo/untracked_file_returns_dirty_error_when_local_config_hides_untracked_files
TestCleanRepo/non_git_repo_error_includes_git_stderr
```

### 4.2 GREEN

Final focused verification:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/gitguard -v
```

Result:

```text
=== RUN   TestCleanRepo
=== RUN   TestCleanRepo/clean_repo_returns_nil
=== RUN   TestCleanRepo/modified_tracked_file_returns_dirty_error
=== RUN   TestCleanRepo/untracked_file_returns_dirty_error
=== RUN   TestCleanRepo/untracked_file_returns_dirty_error_when_local_config_hides_untracked_files
=== RUN   TestCleanRepo/non_git_repo_error_includes_git_stderr
--- PASS: TestCleanRepo
PASS
ok github.com/camcamcami/BLK-System/internal/gitguard
```

Full repository verification:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./...
git diff --check
```

All passed.

---

## 5. Review Results

### 5.1 Spec Compliance Review

Verdict: **PASS**

Gaps: none.

Spec review confirmed that Task 4's required behavior was implemented:

- clean repo returns nil,
- modified tracked file returns a dirty error,
- untracked file returns a dirty error,
- status check runs before later engine behavior exists,
- scope remains limited to the clean-Git preflight.

### 5.2 Code Quality Review

Verdict: **APPROVED**

Critical issues: none.

Important issues: none.

Minor issues: none.

The final implementation was accepted after hardening the status command to use explicit untracked-file detection and to include useful Git diagnostics on command failure.

---

## 6. Final Verification

Final verification before pushing the implementation commit:

```bash
export PATH="$HOME/.local/bin:$PATH"; gofmt -l internal/gitguard/status.go internal/gitguard/status_test.go internal/testutil/gitrepo.go internal/testutil/gitrepo_test.go internal/contracts/payload.go internal/contracts/report.go internal/contracts/payload_test.go cmd/blk-pipe/main.go cmd/blk-pipe/main_test.go internal/pipe/exitcodes.go internal/pipe/exitcodes_test.go
export PATH="$HOME/.local/bin:$PATH"; go test ./internal/gitguard -v
export PATH="$HOME/.local/bin:$PATH"; go test ./...
git diff --check
git status --short --branch
git log --oneline --decorate -4
git push origin main
git status --short --branch
```

Result:

```text
gofmt check                  PASS
go test ./internal/gitguard  PASS
go test ./...                PASS
git diff --check             PASS
implementation push          PASS
repo state after push        clean, aligned with origin/main
```

Outcome-document verification before the documentation commit:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/gitguard -v
go test ./...
git diff --check
```

Result:

```text
go test ./internal/gitguard  PASS
go test ./...                PASS
git diff --check             PASS
```

---

## 7. Deviations / Notes

- The plan suggested `git status --porcelain`; the implementation deliberately uses `git status --porcelain --untracked-files=all` so local Git config cannot hide untracked files from BLK-pipe's safety preflight.
- `EnsureClean` returns a typed `*DirtyError` for dirty repositories and normal wrapped errors for infrastructure/Git command failures. This gives future orchestration clear error mapping for `GIT_DIRTY` versus `INTERNAL_ERROR`.
- Git environment hardening was included in the production status check, not just the test utility, to keep safety checks deterministic under hostile or polluted shell environments.
- No external Go dependencies were added.
- No live LLM, network, Discord, or Codex behavior was added.

---

## 8. Next Task

Proceed to Sprint 001 Task 5: implement the bounded fake engine runner.

Task 5 will add:

```text
internal/engine/runner.go
internal/engine/runner_test.go
testdata/engines/success.sh
testdata/engines/fail.sh
testdata/engines/flood.sh
```

The runner must execute a local command with timeout handling and output byte caps before later tasks wire staging, cleanup, commit, and report generation.
