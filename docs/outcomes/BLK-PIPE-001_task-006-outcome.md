# BLK-pipe Sprint 001 — Task 6 Outcome

**Status:** Complete
**Date:** 2026-05-02
**Task:** Implement allowlist-only staging
**Implementation Commit:** `625061855d23031412d7dcbc2af5f108154ac7e6 feat: stage only allowlisted files`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Task 6 implemented the Git staging boundary for BLK-pipe.

The objective was to stage only explicitly allowlisted modified and new files, and never use broad staging commands that could widen mutation scope. This is a core safety primitive for the eventual BLK-pipe execution path: the engine may change the workspace, but BLK-pipe must only stage files that the caller explicitly allowed.

The governing task requirements were:

- create `internal/gitguard/stage.go`,
- create `internal/gitguard/stage_test.go`,
- stage modified allowlisted files,
- stage new allowlisted files,
- leave unallowlisted changed files unstaged,
- avoid broad staging commands,
- use explicit `git add -- <path>` calls,
- never use `git add .`,
- never use `git add -u`,
- verify with `go test ./internal/gitguard -run TestStageAllowlist -v`,
- commit with `feat: stage only allowlisted files`.

---

## 2. Files Added

```text
internal/gitguard/stage.go
internal/gitguard/stage_test.go
```

No CLI, orchestration, payload, cleanup, or commit-reporting code was changed in this task.

---

## 3. Behavior Implemented

### 3.1 API

Task 6 added this package-level API:

```go
func StageAllowlist(repo string, allowedModified []string, allowedNew []string) error
```

`StageAllowlist` stages only the file paths provided in the two allowlist slices.

The implementation stages each path through an explicit Git invocation:

```text
git add -- <path>
```

The pathspec terminator `--` is intentional. It ensures dash-prefixed file names such as `-allowed.txt` are interpreted as paths rather than Git options.

### 3.2 Explicit-path staging only

The implementation does not stage the whole worktree or all tracked changes. It does not use:

```text
git add .
git add -u
```

This was checked both behaviorally and by review.

### 3.3 Modified-file staging

A tracked file that appears in `allowedModified` is staged when changed.

Test coverage:

```text
TestStageAllowlist/stages_modified_allowlisted_file
```

### 3.4 New-file staging

A new file that appears in `allowedNew` is staged.

Test coverage:

```text
TestStageAllowlist/stages_new_allowlisted_file
```

### 3.5 Unallowlisted files remain unstaged

The tests create a mixed workspace with:

- an allowlisted modified file,
- an allowlisted new file,
- an unallowlisted modified tracked file,
- multiple unallowlisted new files.

Only the exact allowlisted paths appear in:

```text
git diff --cached --name-only
```

Test coverage:

```text
TestStageAllowlist/does_not_stage_unallowlisted_modified_or_new_files
```

### 3.6 Directory entries are rejected

A code quality review found an important safety gap in the first implementation: `git add -- <directory>` recursively stages children under that directory. That would have violated the allowlist-only boundary because a clean relative allowlist entry like `safe` could stage multiple files under `safe/`.

The final implementation prechecks each allowlisted path with `os.Stat` and rejects directories before invoking Git.

Regression coverage:

```text
TestStageAllowlist/rejects_directory_allowlist_entry_without_staging_children
TestStageAllowlist/rejects_unsafe_path_and_pathspec_inputs_before_git_can_widen_scope/directory
```

### 3.7 Deleted files are rejected

The same review identified that `git add -- <deleted tracked file>` stages a deletion. Task 6 is scoped to modified and new files, not removals, so the final implementation requires the allowlisted path to exist in the worktree before staging.

Regression coverage:

```text
TestStageAllowlist/rejects_deleted_allowlisted_file_without_staging_deletion
```

### 3.8 Unsafe path/pathspec inputs are rejected

The implementation rejects unsafe or widening path inputs before Git can interpret them as pathspecs:

- parent traversal: `../x`,
- cleaned traversal: `safe/../x`,
- dot path: `.`,
- wildcard pathspec: `*`,
- magic pathspec: `:(glob)**`,
- directory entries.

Regression coverage:

```text
TestStageAllowlist/rejects_unsafe_path_and_pathspec_inputs_before_git_can_widen_scope
```

---

## 4. TDD Evidence

### 4.1 Initial RED

The implementation subagent wrote `internal/gitguard/stage_test.go` before `StageAllowlist` existed.

Focused test failure before implementation:

```text
go test ./internal/gitguard -run TestStageAllowlist -v
# github.com/camcamcami/BLK-System/internal/gitguard [...]
internal/gitguard/stage_test.go:16:13: undefined: StageAllowlist
internal/gitguard/stage_test.go:27:13: undefined: StageAllowlist
internal/gitguard/stage_test.go:45:13: undefined: StageAllowlist
internal/gitguard/stage_test.go:56:13: undefined: StageAllowlist
FAIL
```

This confirmed the tests were exercising missing behavior rather than passing against existing code.

### 4.2 Initial GREEN

After the first implementation, the focused Task 6 tests passed:

```text
go test ./internal/gitguard -run TestStageAllowlist -v
PASS
ok github.com/camcamcami/BLK-System/internal/gitguard 0.066s
```

### 4.3 Review-fix RED

The quality review requested changes for directory entries and deleted files. Regression tests were added before the fix. They failed against the initial implementation because:

- `git add -- safe` staged files under the `safe/` directory,
- `git add -- delete-me.txt` staged a deletion.

### 4.4 Review-fix GREEN

After adding the precheck that each allowlisted path must be an existing non-directory worktree file, the required tests passed:

```text
go test ./internal/gitguard -run TestStageAllowlist -v
PASS
```

---

## 5. Review Results

### 5.1 First spec compliance review

Result: `PASS`

The spec reviewer confirmed that the initial implementation met the visible Task 6 requirements and used explicit `git add -- <path>` staging.

### 5.2 First code quality review

Result: `REQUEST_CHANGES`

The quality reviewer found a real safety gap:

1. directory allowlist entries could recursively stage children,
2. deleted tracked files could be staged as removals,
3. negative validation tests were missing for traversal/pathspec hazards.

These findings were treated as blocking.

### 5.3 Fix implementation

The unpushed implementation commit was amended after adding regression tests and the minimal fix:

- reject missing paths before `git add`,
- reject directory paths before `git add`,
- keep explicit `git add -- <path>` for valid file paths,
- preserve scope to only `internal/gitguard/stage.go` and `internal/gitguard/stage_test.go`.

### 5.4 Second spec compliance review

Result: `PASS`

The reviewer confirmed:

- explicit path staging only,
- no broad staging commands,
- fixed directory/deletion safety hazards,
- correct file scope,
- focused Task 6 tests passing.

### 5.5 Second code quality review

Result: `APPROVED`

The reviewer confirmed:

- directory entries are rejected via `os.Stat` and `info.IsDir()`,
- deleted/missing allowlisted files are rejected before Git staging,
- traversal/pathspec negative tests are present,
- `exec.Command` is used without shell interpolation,
- existing hermetic `gitEnv()` is reused,
- tests are hermetic and use `internal/testutil`,
- scope is controlled,
- full test suite passes.

---

## 6. Final Verification

Final verification was run before pushing the implementation commit.

### 6.1 Formatting

```text
export PATH="$HOME/.local/bin:$PATH"
gofmt -l internal/gitguard/stage.go internal/gitguard/stage_test.go internal/gitguard/status.go internal/gitguard/status_test.go internal/testutil/gitrepo.go internal/testutil/gitrepo_test.go internal/contracts/payload.go internal/contracts/report.go internal/contracts/payload_test.go cmd/blk-pipe/main.go cmd/blk-pipe/main_test.go internal/pipe/exitcodes.go internal/pipe/exitcodes_test.go internal/engine/runner.go internal/engine/runner_test.go
```

Output was empty, meaning all checked Go files were formatted.

### 6.2 Focused Task 6 test

```text
go test ./internal/gitguard -run TestStageAllowlist -v
```

Result:

```text
PASS
ok github.com/camcamcami/BLK-System/internal/gitguard (cached)
```

Subtests included:

```text
TestStageAllowlist/stages_modified_allowlisted_file
TestStageAllowlist/stages_new_allowlisted_file
TestStageAllowlist/does_not_stage_unallowlisted_modified_or_new_files
TestStageAllowlist/uses_pathspec_terminator_for_dash_prefixed_paths
TestStageAllowlist/rejects_directory_allowlist_entry_without_staging_children
TestStageAllowlist/rejects_deleted_allowlisted_file_without_staging_deletion
TestStageAllowlist/rejects_unsafe_path_and_pathspec_inputs_before_git_can_widen_scope/parent_traversal
TestStageAllowlist/rejects_unsafe_path_and_pathspec_inputs_before_git_can_widen_scope/cleaned_traversal
TestStageAllowlist/rejects_unsafe_path_and_pathspec_inputs_before_git_can_widen_scope/dot
TestStageAllowlist/rejects_unsafe_path_and_pathspec_inputs_before_git_can_widen_scope/wildcard
TestStageAllowlist/rejects_unsafe_path_and_pathspec_inputs_before_git_can_widen_scope/magic_glob_pathspec
TestStageAllowlist/rejects_unsafe_path_and_pathspec_inputs_before_git_can_widen_scope/directory
```

### 6.3 Full gitguard package test

```text
go test ./internal/gitguard -v
```

Result:

```text
PASS
ok github.com/camcamcami/BLK-System/internal/gitguard 0.218s
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
   ec33df1..6250618  main -> main
```

Post-push status:

```text
## main...origin/main
6250618 (HEAD -> main, origin/main) feat: stage only allowlisted files
```

---

## 7. Deviations / Notes

The chosen API splits modified and new allowlists:

```go
func StageAllowlist(repo string, allowedModified []string, allowedNew []string) error
```

This mirrors the payload model already established in Task 2, where modified and new file allowlists are distinct fields.

The implementation intentionally rejects directories and missing files even though the original task text did not spell those checks out. That tightening is consistent with the task's safety objective: stage only explicit modified/new files, never broad or widened path sets.

The implementation does not attempt unauthorized mutation cleanup. That remains a later BLK-pipe task.

---

## 8. Next Task

Task 7 should build on this staging boundary by detecting and destroying unauthorized files after engine execution.

Expected next safety layer:

- compare workspace mutations against the allowlists,
- delete unauthorized new files,
- restore unauthorized modified files from Git,
- ensure the repo can return to a safe state before commit/report generation.
