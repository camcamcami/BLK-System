# BLK-PIPE-002 Task 005 Outcome — Bounded Git Command Helper

Status: COMPLETE
Date: 2026-05-03
Sprint plan: `docs/plans/BLK-PIPE-002_v47-hardening-layer.md`
Task: Sprint 002 Task 5 — route Git calls through a bounded Git helper
Implementation commit: `4dd0bb7 feat: bound blk-pipe git commands`
Remote: pushed to `origin/main`

## Summary

Task 005 centralized production Git command execution for BLK-pipe behind a bounded helper in `internal/gitguard`.

The implementation removes ad hoc production `exec.Command("git", ...)` call sites from BLK-pipe production paths, routes Git execution through `execguard.Run`, preserves strict allowlist staging, keeps Git output/time bounded, and prepares future branch/fetch work by supporting controlled extra environment injection for headless `ls-remote`.

The implementation was pushed to `origin/main` as:

```text
4dd0bb7 feat: bound blk-pipe git commands
```

## Files Changed

```text
internal/gitguard/cleanup.go
internal/gitguard/cleanup_test.go
internal/gitguard/command.go
internal/gitguard/command_test.go
internal/gitguard/stage.go
internal/gitguard/status.go
internal/pipe/run.go
```

Commit stat:

```text
internal/gitguard/cleanup.go      |  20 ++----
internal/gitguard/cleanup_test.go |  16 +++++
internal/gitguard/command.go      |  73 +++++++++++++++++++
internal/gitguard/command_test.go | 148 ++++++++++++++++++++++++++++++++++++++
internal/gitguard/stage.go        |  16 +----
internal/gitguard/status.go       |  32 ++-------
internal/pipe/run.go              |  15 +---
7 files changed, 250 insertions(+), 70 deletions(-)
```

## Implemented Behavior

### Central bounded Git helper

`internal/gitguard/command.go` now provides the Task 005 helper API:

```go
type GitResult struct {
    Stdout []byte
}

func RunGit(ctx context.Context, repo string, args ...string) (GitResult, error)
func RunGitWithLimit(ctx context.Context, repo string, maxOutputBytes int64, args ...string) (GitResult, error)
func RunGitWithEnv(ctx context.Context, repo string, extraEnv []string, args ...string) (GitResult, error)
```

The helper executes Git through `execguard.Run` rather than direct production `os/exec` calls.

Default Git execution now uses:

- a deterministic `30 * time.Second` timeout,
- a bounded output cap,
- `execguard.ScrubbedEnv(repo)` for environment construction,
- direct argv execution with no shell,
- bounded stderr/stdout context in infrastructure errors,
- optional extra environment values for later operations such as headless `ls-remote`.

### Environment scrubbing and future `ls-remote` support

The helper inherits the Task 003 environment baseline from `execguard.ScrubbedEnv`, including scrubbing of inherited Git and SSH-sensitive variables:

```text
GIT_*
SSH_AUTH_SOCK
SSH_AGENT_PID
SSH_ASKPASS
```

It also preserves deterministic Git configuration and working-directory environment behavior:

```text
GIT_CONFIG_GLOBAL=/dev/null
GIT_CONFIG_NOSYSTEM=1
PWD=<repo>
```

`RunGitWithEnv` allows controlled extra env injection, including the future branch/fetch hardening value required by the plan:

```text
GIT_SSH_COMMAND=ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes
```

### Production Git call routing

The following production paths now route through the centralized helper:

- `gitguard.EnsureClean`,
- `gitguard.StageAllowlist`,
- `gitguard.CleanupUnauthorized`,
- the local `runGit` wrapper in `internal/pipe/run.go`.

The remaining direct `exec.Command("git", ...)` usage is intentionally limited to allowed test/support locations:

- `internal/gitguard/command.go`, the bounded helper itself,
- `internal/testutil/**`, hermetic test repository support.

### Strict staging preserved

`StageAllowlist` still validates each allowlist entry before Git sees it and stages only explicit file paths using:

```text
git add -- <file>
```

The implementation preserves the Sprint 001 safety properties:

- no `git add .`,
- no `git add -u`,
- no directory allowlist staging,
- no deleted allowlisted-file staging,
- no path traversal or Git pathspec/glob widening,
- no shell execution.

### Cleanup robustness hardening from review

Initial code-quality review found that routing `CleanupUnauthorized` through the bounded Git helper made verbose `git clean -ffdx` susceptible to helper output flooding when a repo contained a very large unauthorized/untracked tree.

The review fix changed cleanup to:

```text
git clean -ffdx -q
```

This keeps cleanup destructive semantics intact while suppressing expected per-file deletion output, preventing the helper output cap from killing Git cleanup midway and leaving unauthorized files behind.

A regression test now creates thousands of unauthorized untracked files and proves cleanup completes without output flood and leaves the repo clean.

## TDD Evidence

### Initial RED evidence

The implementation subagent wrote Task 005 helper tests before production code. The first focused run failed because the new helper API did not exist yet:

```text
export PATH="$HOME/.local/bin:$PATH"; go test ./internal/gitguard -run 'TestRunGit' -v
# github.com/camcamcami/BLK-System/internal/gitguard [github.com/camcamcami/BLK-System/internal/gitguard.test]
internal/gitguard/command_test.go:18:14: undefined: RunGit
internal/gitguard/command_test.go:30:12: undefined: RunGit
internal/gitguard/command_test.go:56:17: undefined: RunGit
internal/gitguard/command_test.go:91:17: undefined: RunGitWithLimit
internal/gitguard/command_test.go:111:12: undefined: RunGit
internal/gitguard/command_test.go:128:17: undefined: RunGitWithEnv
FAIL
```

### Review-fix RED evidence

After the first code-quality review requested cleanup hardening, the fix subagent added a regression before changing production cleanup. The focused regression failed against verbose `git clean -ffdx`:

```text
go test ./internal/gitguard -run 'TestCleanupUnauthorized|TestRunGitScrubs' -v
...
git clean -ffdx ... infrastructure error: output exceeded max output bytes (4198400 > 4194304)
FAIL
```

This proved the reviewer-identified cleanup output-flood hazard was real before the quiet-clean fix was applied.

### GREEN evidence

After implementation and review fixes, focused Git helper and cleanup tests passed:

```text
go test ./internal/gitguard -run 'TestCleanupUnauthorized|TestRunGitScrubs' -v
=== RUN   TestCleanupUnauthorized
=== RUN   TestCleanupUnauthorized/removes_unauthorized_mutations_while_preserving_staged_allowlist
=== RUN   TestCleanupUnauthorized/removes_unauthorized_untracked_nested_git_repository
=== RUN   TestCleanupUnauthorized/removes_many_untracked_files_without_output_flood
--- PASS: TestCleanupUnauthorized (0.41s)
=== RUN   TestRunGitScrubsInheritedGitAndSSHEnvironment
--- PASS: TestRunGitScrubsInheritedGitAndSSHEnvironment (0.00s)
PASS
ok  github.com/camcamcami/BLK-System/internal/gitguard 0.421s
```

Full focused package verification also passed:

```text
go test ./internal/gitguard -v
PASS
ok  github.com/camcamcami/BLK-System/internal/gitguard 0.638s

go test ./internal/pipe -v
PASS
ok  github.com/camcamcami/BLK-System/internal/pipe 0.364s
```

## Review Results

Task 005 used the Sprint 002 two-stage gate: spec compliance first, then code-quality/safety review. The controller did not push until both final reviews passed.

### Spec compliance review

Final spec review verdict:

```text
PASS
```

Spec review confirmed:

- `GitResult`, `RunGit`, `RunGitWithLimit`, and `RunGitWithEnv` exist;
- Git execution uses `execguard.Run` with bounded output and timeout;
- `EnsureClean`, `StageAllowlist`, `CleanupUnauthorized`, and `pipe.runGit` route through the helper;
- no production direct `exec.Command("git", ...)` remains outside the allowed helper/test-support locations;
- required tests cover success, failure stderr context, env scrubbing, output flood, timeout, extra env injection, and cleanup flood regression;
- BLK-004 invariants around no shell, no broad staging, and scrubbed Git/SSH environment are preserved.

### Code-quality/safety review

Initial code-quality review verdict:

```text
REQUEST_CHANGES
```

The reviewer identified one important issue:

- verbose `git clean -ffdx` through the bounded helper could exceed the helper output cap while deleting a large unauthorized tree, killing cleanup mid-stream and potentially leaving unauthorized files behind.

The reviewer also noted a minor test weakness in the `SSH_AUTH_SOCK` scrub assertion.

Fixes applied before re-review:

- changed cleanup to `git clean -ffdx -q`,
- added a many-untracked-files cleanup regression,
- strengthened the `SSH_AUTH_SOCK` scrub test to assert no `SSH_AUTH_SOCK=` entry survives.

Final code-quality review verdict:

```text
APPROVED
```

Final quality review confirmed:

- the prior cleanup hazard is fixed;
- the scrub test is effective;
- helper behavior is bounded and deterministic;
- staging remains explicit and safe;
- cleanup and preflight invariants remain intact;
- `pipe.runGit` status/error semantics are preserved;
- tests are deterministic and non-flaky;
- no production scope creep or Codex/live LLM integration was introduced.

## Final Controller Verification

Final controller verification before the implementation push used:

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -l internal/gitguard/*.go internal/pipe/run.go
go test ./internal/gitguard -v
go test ./internal/pipe -v
go test ./...
go vet ./...
! git grep -n 'exec.Command("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
git diff --check
git status --short --branch
git log --oneline --decorate -4
git push origin main
git status --short --branch
```

Full-suite result:

```text
ok  github.com/camcamcami/BLK-System/cmd/blk-pipe        (cached)
ok  github.com/camcamcami/BLK-System/internal/contracts   (cached)
ok  github.com/camcamcami/BLK-System/internal/engine      (cached)
ok  github.com/camcamcami/BLK-System/internal/execguard   (cached)
ok  github.com/camcamcami/BLK-System/internal/gitguard    0.673s
ok  github.com/camcamcami/BLK-System/internal/pipe        0.408s
ok  github.com/camcamcami/BLK-System/internal/runtimeguard (cached)
ok  github.com/camcamcami/BLK-System/internal/testutil    (cached)
```

Safety grep results:

```text
! git grep -n 'exec.Command("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
# no output

! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
# no output
```

Push result:

```text
To https://github.com/camcamcami/BLK-System.git
   f247746..4dd0bb7  main -> main
## main...origin/main
```

## Deviations / Notes

- No Codex or live LLM integration was introduced.
- The helper keeps one direct production Git process spawn location by design: `internal/gitguard/command.go`.
- `internal/testutil/**` remains excluded from the direct-Git grep because it is hermetic test support code.
- Cleanup now uses quiet `git clean -ffdx -q` specifically to preserve bounded cleanup robustness under large unauthorized trees.
- The optional command-argument sanitization suggestion from the first code-quality review was not expanded in this task because current production call sites are bounded, argv-only, and not shell-interpreted. Future remote/branch work can revisit argument display sanitization if user-controlled remote URLs become report-visible.

## Next Task

The next planned Sprint 002 task is Task 6: add pre-engine hash, mandatory zero-diff abort, diff summary, Git diff, and untracked report fields.

Task 6 should build on the Task 005 Git helper so final diff extraction and `git diff <PreEngineHash> HEAD --numstat --` are bounded and never use triple-dot diff.
