# BLK-pipe Sprint 001 — Task 7 Outcome

**Status:** Complete
**Date:** 2026-05-02
**Task:** Implement unauthorized mutation cleanup
**Implementation Commit:** `cbe11b01cc209d02c35c56888fcbff7ad2be0d17 feat: destroy unauthorized mutations`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Task 7 implemented BLK-pipe's unauthorized mutation cleanup primitive.

After Task 6, BLK-pipe can stage only explicitly allowlisted modified and new files. Task 7 adds the next safety layer: once the allowlisted files are safely staged, all remaining unallowlisted workspace mutations are physically destroyed or reverted before later orchestration/commit/reporting steps run.

The governing task requirements were:

- create `internal/gitguard/cleanup.go`,
- create `internal/gitguard/cleanup_test.go`,
- revert unallowlisted tracked modifications,
- delete unallowlisted untracked files,
- preserve staged allowlisted changes,
- implement cleanup with carefully bounded Git commands:
  - `git checkout -- .`,
  - `git clean -fd`,
- only run this cleanup after explicit allowlisted files have already been staged,
- verify with `go test ./internal/gitguard -run TestCleanup -v`,
- commit with `feat: destroy unauthorized mutations`.

---

## 2. Files Added

```text
internal/gitguard/cleanup.go
internal/gitguard/cleanup_test.go
```

No CLI, pipe orchestration, commit generation, report generation, payload-contract, or engine-runner code was changed in this task.

---

## 3. Behavior Implemented

### 3.1 API

Task 7 added this package-level API:

```go
func CleanupUnauthorized(repo string) error
```

The function is documented as an operation that must only be called after the complete allowlist has already been explicitly staged.

### 3.2 Cleanup sequence

The implementation runs exactly these Git operations in the target repo:

```text
git checkout -- .
git clean -fd
```

The commands are intentionally broad, but only in this post-staging cleanup phase:

1. `git checkout -- .` reverts remaining unstaged tracked worktree modifications back to the index.
2. `git clean -fd` deletes remaining untracked files and directories.

Because allowlisted modified and new files are staged before cleanup, their staged diff remains in the index while unauthorized unstaged mutations are destroyed.

### 3.3 Hermetic Git execution

The cleanup implementation uses:

- `exec.Command`, not shell interpolation,
- `cmd.Dir = repo`,
- existing `gitEnv()` from `internal/gitguard/status.go`.

That preserves the hermetic Git behavior already established in earlier BLK-pipe tasks.

### 3.4 Unauthorized tracked modifications are reverted

The test creates a tracked file, modifies it without staging, runs cleanup, and verifies the file content returns to the original committed version.

Coverage:

```text
TestCleanupUnauthorized/removes_unauthorized_mutations_while_preserving_staged_allowlist
```

### 3.5 Unauthorized untracked files and directories are deleted

The test creates untracked files under a nested directory, runs cleanup, and verifies both the untracked files and their directory are gone.

Coverage:

```text
scratch/unauthorized.txt
scratch/nested/unauthorized.txt
scratch/
```

### 3.6 Staged allowlisted changes remain staged

The test stages:

- an allowlisted modified tracked file,
- an allowlisted new file.

After cleanup, it verifies:

- both remain present in the worktree,
- both remain in `git diff --cached --name-only`,
- only those staged allowlisted paths remain staged.

This confirms that `git clean -fd` does not delete the staged new file and that `git checkout -- .` preserves the staged allowlisted modified content in the worktree.

---

## 4. TDD Evidence

### 4.1 RED

The implementation subagent wrote `internal/gitguard/cleanup_test.go` before `CleanupUnauthorized` existed.

Focused test failure before implementation:

```text
go test ./internal/gitguard -run TestCleanup -v
# github.com/camcamcami/BLK-System/internal/gitguard [...]
internal/gitguard/cleanup_test.go:31:13: undefined: CleanupUnauthorized
FAIL
```

This confirmed the tests were exercising missing behavior rather than passing against existing code.

### 4.2 GREEN

After implementing `CleanupUnauthorized`, the focused Task 7 test passed:

```text
go test ./internal/gitguard -run TestCleanup -v
=== RUN   TestCleanupUnauthorized
=== RUN   TestCleanupUnauthorized/removes_unauthorized_mutations_while_preserving_staged_allowlist
--- PASS: TestCleanupUnauthorized (0.02s)
    --- PASS: TestCleanupUnauthorized/removes_unauthorized_mutations_while_preserving_staged_allowlist (0.02s)
PASS
ok github.com/camcamcami/BLK-System/internal/gitguard 0.026s
```

---

## 5. Review Results

### 5.1 Spec compliance review

Result: `PASS`

The spec reviewer confirmed:

- `cleanup.go` and `cleanup_test.go` were created,
- the implementation uses `git checkout -- .` followed by `git clean -fd`,
- unauthorized tracked modifications are reverted,
- unauthorized untracked files/directories are deleted,
- staged allowlisted modified and new files remain staged,
- the focused Task 7 test passes,
- the commit scope is limited to the two Task 7 files.

### 5.2 Code quality review

Result: `APPROVED`

The quality reviewer confirmed:

- direct `exec.Command` Git calls are used,
- no shell execution is used,
- no hardcoded secrets are present,
- existing hermetic `gitEnv()` is reused,
- cleanup command order matches the spec,
- tests cover tracked, untracked, nested untracked directory, staged modified, and staged new behavior,
- scope is controlled and does not include CLI/orchestration/report work,
- full tests pass.

No review fixes were required.

---

## 6. Final Verification

Final verification was run before pushing the implementation commit.

### 6.1 Formatting

```text
export PATH="$HOME/.local/bin:$PATH"
gofmt -l internal/gitguard/cleanup.go internal/gitguard/cleanup_test.go internal/gitguard/stage.go internal/gitguard/stage_test.go internal/gitguard/status.go internal/gitguard/status_test.go internal/testutil/gitrepo.go internal/testutil/gitrepo_test.go internal/contracts/payload.go internal/contracts/report.go internal/contracts/payload_test.go cmd/blk-pipe/main.go cmd/blk-pipe/main_test.go internal/pipe/exitcodes.go internal/pipe/exitcodes_test.go internal/engine/runner.go internal/engine/runner_test.go
```

Output was empty, meaning all checked Go files were formatted.

### 6.2 Focused Task 7 test

```text
go test ./internal/gitguard -run TestCleanup -v
```

Result:

```text
PASS
ok github.com/camcamcami/BLK-System/internal/gitguard 0.026s
```

### 6.3 Full gitguard package test

```text
go test ./internal/gitguard -v
```

Result:

```text
PASS
ok github.com/camcamcami/BLK-System/internal/gitguard 0.264s
```

### 6.4 Full Go suite

```text
go test ./...
```

Result:

```text
ok github.com/camcamcami/BLK-System/cmd/blk-pipe
ok github.com/camcamcami/BLK-System/internal/contracts
ok github.com/camcamcami/BLK-System/internal/engine
ok github.com/camcamcami/BLK-System/internal/gitguard
ok github.com/camcamcami/BLK-System/internal/pipe
ok github.com/camcamcami/BLK-System/internal/testutil
```

### 6.5 Whitespace check

```text
git diff --check
```

Result: exit code `0`.

### 6.6 Push

Implementation push succeeded:

```text
To https://github.com/camcamcami/BLK-System.git
   bfcd39d..cbe11b0  main -> main
```

Post-push status:

```text
## main...origin/main
cbe11b0 (HEAD -> main, origin/main) feat: destroy unauthorized mutations
```

---

## 7. Deviations / Notes

The chosen API was:

```go
func CleanupUnauthorized(repo string) error
```

This intentionally takes only the repository path because the allowlist has already been resolved into the Git index by Task 6 staging. Cleanup then destroys all remaining unstaged worktree mutations.

The broad cleanup commands are acceptable only because the correct call order is:

1. validate payload,
2. ensure clean repo,
3. run engine,
4. stage explicit allowlisted files,
5. cleanup unauthorized mutations.

Task 8 will be responsible for enforcing that sequence in the pipe orchestrator.

---

## 8. Next Task

Task 8 is the major orchestration step.

It should wire together:

- payload validation,
- clean Git preflight,
- bounded engine execution,
- allowlist-only staging,
- unauthorized mutation cleanup,
- deterministic commit creation,
- final execution report generation,
- CLI payload-file execution.

This is the first point where BLK-pipe's individual safety primitives become an end-to-end execution pipeline.
