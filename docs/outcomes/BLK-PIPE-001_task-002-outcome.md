# BLK-pipe Sprint 001 — Task 2 Outcome

**Status:** Complete
**Date:** 2026-05-02
**Task:** Define payload and report contracts
**Commit:** `95f01b8 feat: define blk-pipe payload contracts`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Add typed Go structs for the Sprint 001 payload/report contracts and implement deterministic payload validation before any future execution/orchestration logic exists.

This task intentionally did **not** implement engine execution, Git orchestration, staging, cleanup, commit creation, Codex integration, or BLK-test integration.

---

## 2. Files Added

```text
internal/contracts/payload.go
internal/contracts/report.go
internal/contracts/payload_test.go
```

---

## 3. Behavior Implemented

### 3.1 Payload Contract

Added `contracts.Payload` with JSON tags for:

```text
action
workdir
engine_command
allowed_modified_files
allowed_new_files
timeout_seconds
max_output_bytes
```

### 3.2 Report Contract

Added `contracts.Report` with JSON tags for:

```text
status
action
workdir
commit_hash
staged_files
destroyed_files
engine_exit_code
engine_output_bytes
error
```

### 3.3 Payload Validation

Added:

```go
func (p Payload) Validate() error
```

Validation currently enforces:

- `action` must equal `execute`.
- `workdir` must be absolute.
- `engine_command` must contain at least one element.
- `engine_command` elements must not be empty or whitespace-only.
- allowlist paths must be relative file paths.
- allowlist paths must be clean.
- allowlist paths must not contain `..`.
- allowlist paths must not be `.`.
- allowlist paths must not contain Git pathspec/glob metacharacters.
- protected BLK-req paths matching `^docs/(requirements|use_cases)/.*` are rejected.
- `timeout_seconds` must be greater than 0.
- `max_output_bytes` must be greater than 0.

---

## 4. TDD Evidence

### 4.1 RED

Tests were written before production code.

Initial failing command:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/contracts -v
```

Failure evidence included missing production symbols:

```text
undefined: Payload
```

After quality review requested stronger validation, additional failing tests were written first for:

- `engine_command: []string{""}`,
- `engine_command: []string{"   "}`,
- allowlist path `.`,
- allowlist path `*`,
- allowlist path `src/*`,
- allowlist path `:(glob)**`.

Those tests failed against the prior implementation before the validation fix was added.

### 4.2 GREEN

After implementation and review-requested fix:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/contracts -v
go test ./...
git diff --check
```

Verified result:

```text
ok  	github.com/camcamcami/BLK-System/internal/contracts
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe
ok  	github.com/camcamcami/BLK-System/internal/pipe
```

---

## 5. Review Results

### 5.1 Initial Spec Compliance Review

Verdict: **PASS**

Gaps: none.

### 5.2 Initial Code Quality Review

Verdict: **REQUEST_CHANGES**

Issues found:

- allowlist validation accepted dangerous future Git pathspec/glob values (`.`, `*`, `src/*`, `:(glob)**`),
- `engine_command` accepted empty string elements.

### 5.3 Fix Applied

The implementation was amended to reject:

- dot path,
- glob/pathspec metacharacters,
- leading Git pathspec magic `:`,
- blank engine command elements.

### 5.4 Final Spec Compliance Re-review

Verdict: **PASS**

Gaps: none.

### 5.5 Final Code Quality Re-review

Verdict: **APPROVED**

Critical issues: none.
Important issues: none.
Minor issues: none.

---

## 6. Final Verification

Final verification before push:

```bash
export PATH="$HOME/.local/bin:$PATH"; gofmt -l internal/contracts/payload.go internal/contracts/report.go internal/contracts/payload_test.go cmd/blk-pipe/main.go cmd/blk-pipe/main_test.go internal/pipe/exitcodes.go internal/pipe/exitcodes_test.go
export PATH="$HOME/.local/bin:$PATH"; go test ./...
git diff --check
git status --short --branch
```

Result:

```text
gofmt check               PASS
go test ./...             PASS
git diff --check          PASS
repo state after push     clean, aligned with origin/main
```

---

## 7. Deviations / Notes

- The final Task 2 commit was amended before push to incorporate the code quality review fix.
- No execution/orchestration behavior was added.
- No external Go dependencies were added.
- The stricter allowlist validation was added proactively because later Sprint 001 tasks will pass these paths to Git staging commands.

---

## 8. Next Task

Proceed to Sprint 001 Task 3: add the Git test repository utility for integration tests using real temporary Git repositories.
