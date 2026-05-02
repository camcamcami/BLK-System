# BLK-pipe Sprint 001 — Task 8 Outcome

**Status:** Complete
**Date:** 2026-05-03
**Task:** Implement pipe execution orchestration
**Implementation Commit:** `0a05ba34d9dceeee703e026ea3962bc44e1695f3 feat: orchestrate bounded blk-pipe execution`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Task 8 wired the deterministic BLK-pipe execution path:

1. parse the payload,
2. validate the payload contract,
3. assert a clean Git worktree before execution,
4. run the bounded fake engine,
5. map timeout, flood, and engine-failure conditions,
6. stage only allowlisted paths,
7. clean unauthorized mutations,
8. create a deterministic commit if a staged diff exists,
9. emit a JSON execution report.

The deterministic commit message used for successful engine mutations is:

```text
blk-pipe: apply bounded engine changes
```

Task 8 does not integrate Codex or any live tactical LLM engine. It keeps Sprint 001 focused on the deterministic local safety kernel.

---

## 2. Files Added or Changed

### Added

- `internal/pipe/run.go`
- `internal/pipe/run_test.go`

### Changed

- `cmd/blk-pipe/main.go`
- `cmd/blk-pipe/main_test.go`
- `internal/gitguard/cleanup.go`
- `internal/gitguard/cleanup_test.go`

---

## 3. Behavior Implemented

### 3.1 Pipe orchestration API

Task 8 added:

```go
func Run(ctx context.Context, payloadJSON []byte, reportWriter io.Writer) int
```

The function returns the BLK-pipe process exit code and writes a deterministic JSON report to the supplied writer.

### 3.2 CLI wiring

The CLI now supports:

```bash
blk-pipe --health
blk-pipe --payload-stdin
```

`--payload-stdin` reads JSON from standard input and calls `pipe.Run`.

Zero-argument invocation remains unsupported and nonblocking. File-based payload support is intentionally left for Task 10, which specifies:

```bash
blk-pipe --payload /absolute/path/to/payload.json
```

### 3.3 Success path

A valid payload whose bounded engine only modifies allowlisted files now:

- exits `0`,
- emits report status `SUCCESS`,
- stages only allowlisted changes,
- commits using `blk-pipe: apply bounded engine changes`,
- disables Git hooks during the commit with `git -c core.hooksPath=/dev/null commit ...`.

### 3.4 Failure mapping

Task 8 maps engine and preflight outcomes to the existing exit-code contract:

| Condition | Report status | Exit |
|---|---:|---:|
| Invalid JSON or invalid payload | `INVALID_PAYLOAD` | 2 |
| Unauthorized mutation | `UNAUTHORIZED_FILE_MUTATION` | 3 |
| Engine nonzero exit | `ENGINE_FAILED` | 4 |
| Engine output flood | `FATAL_OUTPUT_FLOOD` | 5 |
| Engine timeout | `ENGINE_TIMEOUT` | 6 |
| Dirty repo before engine | `GIT_DIRTY` | 7 |
| Internal cleanup/report/commit error | `INTERNAL_ERROR` | 9 |

### 3.5 Unauthorized mutation cleanup

Task 8 preserves the required sequence:

```text
validate payload -> assert clean repo -> run engine -> stage allowlist -> cleanup unauthorized mutations -> commit/report
```

Cleanup remains broad only after allowlisted files have been explicitly staged. This preserves allowlisted staged work while destroying remaining unauthorized worktree changes.

Cleanup was hardened from:

```bash
git clean -fdx
```

to:

```bash
git clean -ffdx
```

The second `-f` is required because Git otherwise refuses to delete untracked nested Git repositories. The orchestration preflight rejects pre-existing untracked and ignored files before engine execution, so this aggressive cleanup is applied only to mutations made during the bounded engine run.

### 3.6 `.git` safety hardening

Task 8 treats `.git` metadata mutations as unauthorized. Regression coverage now includes:

- `.git/info/exclude` mutation cannot hide an unauthorized worktree file,
- engine-installed `.git/hooks/post-commit` is unauthorized and does not run,
- pre-existing Git hooks are disabled during the BLK-pipe commit,
- `rm -rf .git` is detected as unauthorized, `.git` is restored, and the repo remains usable,
- engine-created nested Git repositories are removed before returning.

---

## 4. TDD Evidence

### 4.1 Initial Task 8 implementation

The implementation was built with tests for the required Task 8 cases:

- success engine modifies `src/allowed.txt`, run exits `0`, report status is `SUCCESS`, and a commit exists,
- unauthorized engine modifies `src/unauthorized.txt`, run exits `3`, and unauthorized output is absent after the run,
- dirty repository before execution exits `7`,
- failing engine exits `4`.

### 4.2 Review-driven regressions

Review gates found additional safety gaps. Each fix was covered by regression tests before the implementation was amended:

1. `.git/info/exclude` could hide unauthorized files.
2. Engine-installed hooks in `.git/hooks` could run during `git commit`.
3. `.git` root deletion could break recovery.
4. `git clean -fdx` could delete pre-existing ignored files unless preflight rejected them.
5. CLI execution was not yet wired to `pipe.Run`.
6. Nested untracked Git repositories survived `git clean -fdx`.

The final nested-repo fix followed strict TDD:

- added failing `gitguard.CleanupUnauthorized` regression,
- added failing `pipe.Run` regression,
- confirmed failures showed `evil` nested Git repository survived cleanup,
- changed cleanup to `git clean -ffdx`,
- reran focused and full test suites successfully,
- amended the existing unpushed Task 8 commit.

---

## 5. Review Results

### 5.1 Spec compliance review

Final result: `PASS`

The spec reviewer confirmed Task 8 satisfies the plan requirements for validation, clean preflight, bounded engine execution, failure mapping, allowlist staging, unauthorized cleanup, deterministic commit generation, JSON reporting, and CLI wiring via explicit `--payload-stdin`.

### 5.2 Code quality and safety review

Final result: `APPROVED`

The safety reviewer confirmed:

- `.git/info/exclude` bypass is covered,
- Git hook install/execution paths are covered,
- `.git` root deletion is recovered safely,
- pre-existing ignored/untracked files are rejected before cleanup can delete them,
- nested Git repositories created by the engine are removed via `git clean -ffdx`,
- CLI behavior is explicit and nonblocking,
- focused, full, race, gofmt, and diff-check commands pass.

---

## 6. Final Verification

Final controller verification before push ran:

```bash
export PATH="$HOME/.local/bin:$PATH"
git status --short --branch
git log --oneline --decorate -4
gofmt -l internal/pipe/run.go internal/pipe/run_test.go cmd/blk-pipe/main.go cmd/blk-pipe/main_test.go internal/gitguard/cleanup.go internal/gitguard/cleanup_test.go
go test ./internal/gitguard -v
go test ./internal/pipe -v
go test ./cmd/blk-pipe -v
go test ./...
go test -race ./...
git diff --check HEAD^ HEAD
git status --short --branch
git push origin main
git status --short --branch
git rev-parse HEAD
```

Results:

- `gofmt -l ...`: no output
- `go test ./internal/gitguard -v`: PASS
- `go test ./internal/pipe -v`: PASS
- `go test ./cmd/blk-pipe -v`: PASS
- `go test ./...`: PASS
- `go test -race ./...`: PASS
- `git diff --check HEAD^ HEAD`: PASS
- push to `origin/main`: PASS
- final HEAD: `0a05ba34d9dceeee703e026ea3962bc44e1695f3`

---

## 7. Deviations and Notes

- Task 8 added `--payload-stdin` so the CLI has an explicit execution path for internal orchestration testing.
- Task 10 remains responsible for file-based payload execution via `--payload /absolute/path/to/payload.json`.
- Cleanup now uses `git clean -ffdx`, not `git clean -fd`, because unauthorized ignored files and nested Git repositories created by the engine must be destroyed before BLK-pipe returns.
- This is safe only because Task 8 now treats pre-existing untracked and ignored files as dirty and exits before running the engine.
- Codex/live LLM invocation remains deferred until after Sprint 001 and the planned Sprint 002 hardening layer.

---

## 8. Next Task

The next Sprint 001 task is Task 9: Add protected BLK-req path deny tests.

Task 9 objective:

```text
Enforce BLK-006 hard-deny for docs/requirements/* and docs/use_cases/* allowlist entries.
```

Planned files:

- `internal/contracts/payload_test.go`
- `internal/pipe/run_test.go`

Expected commit message:

```text
feat: hard-deny blk-req artifact mutations
```
