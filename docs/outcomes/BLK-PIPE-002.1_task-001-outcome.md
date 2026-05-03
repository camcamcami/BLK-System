# BLK-pipe Sprint 002.1 — Task 1 Outcome

**Status:** Complete
**Date:** 2026-05-03
**Task:** Enforce No-Success-With-Physical-Residue
**Implementation Commit:** `277501bf5a95ba135199748b128621aed995824b fix: block blk-pipe success with physical residue`
**Remote:** pushed to `origin/main`
**Plan:** `docs/plans/BLK-PIPE-002.1_hostile-review-remediation.md`

---

## 1. Objective

Task 1 remediated the hostile-review finding that `blk-pipe` could return `SUCCESS` while unauthorized physical residue remained on disk.

The original trigger case was:

```text
engine: modify allowlisted README.md and create ghostdir/
old result: SUCCESS, Git status clean, ghostdir/ physically survived
```

The required behavior is now enforced: no `SUCCESS` path may leave unauthorized physical residue. Unauthorized empty directories, non-empty directories, ignored files, untracked files, nested Git directories, unreadable residue, and hidden filesystem mode residue route to `UNAUTHORIZED_FILE_MUTATION` / exit `3`, clean the workspace, preserve `HEAD`, and do not create a success commit.

---

## 2. Files Changed

Implementation commit:

```text
277501b fix: block blk-pipe success with physical residue
 internal/gitguard/cleanup.go |   91 +++
 internal/pipe/run.go         |  761 ++++++++++++++++++--
 internal/pipe/run_test.go    | 1600 +++++++++++++++++++++++++++++++++++++-----
 3 files changed, 2239 insertions(+), 213 deletions(-)
```

Changed files:

- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- `internal/gitguard/cleanup.go`

---

## 3. Behavior Implemented

### 3.1 Physical residue audit

`blk-pipe` now audits unauthorized physical residue before any success commit can be created. The audit covers:

- unstaged tracked mutations outside the allowlist,
- untracked files,
- ignored files,
- empty untracked directories,
- non-empty untracked directories,
- empty and non-empty nested `.git` directories,
- unreadable/unwalkable residue directories,
- valid pathnames that look like Git diagnostics, including `warning:*` and newline-containing names,
- root, `.git`, directory, tracked-file, and allowed-new file physical mode mutations that Git would otherwise hide.

### 3.2 Cleanup hardening

`internal/gitguard.CleanupUnauthorized` now makes post-engine residue directories traversable before `git clean -ffdx -q`, so non-empty unreadable engine-created directories can be removed instead of converting cleanup into an `INTERNAL_ERROR`.

Root `.git` restore also handles unreadable `.git` subdirectories before removal decisions, so hidden files such as `.git/objects/zz/evil` or `.git/hooks/evil` cannot survive cleanup.

### 3.3 Mode preservation and hidden-mode rejection

The implementation now snapshots and restores relevant physical modes for pre-existing worktree paths and Git metadata paths. It rejects unauthorized mode-only mutations that Git status/diff would otherwise miss.

For allowed-new files, the physical file mode must be safe and Git-representable:

- allowed: `0644` regular files,
- allowed: `0755` executable files,
- rejected: hidden/special modes such as `0600`, `4755`, setuid/setgid/sticky, and unsafe parent directory modes such as `1777`.

### 3.4 Preflight preservation

Pre-existing nested `.git` directories and physical residue are rejected during clean preflight before engine execution. This preserves user work and prevents later destructive cleanup from deleting residue that existed before the bounded engine ran.

---

## 4. TDD Evidence

### 4.1 RED

The implementation used strict test-first development. Initial RED evidence included the planned hostile probe and additional review-discovered edge cases:

```text
go test ./internal/pipe -run TestRunUnauthorizedEmptyDirectoryFailsAndCleans -v
```

Observed pre-fix behavior:

```text
exit code = 0, want 3
status = SUCCESS
untracked_files included ghostdir/
ghostdir/ physically survived after return
```

Additional RED regressions were added as reviews found deeper physical residue hazards:

- non-empty directories,
- ignored files,
- unreadable empty and non-empty directories,
- empty and non-empty nested `.git` directories,
- pre-existing nested `.git` preflight rejection,
- root/worktree/`.git` directory permission mutations,
- root `.git` hidden residue inside unreadable `.git` subdirectories,
- valid `warning:`/newline pathnames,
- tracked-file mode mutations,
- allowed-new file and parent-directory hidden modes.

### 4.2 GREEN

Final focused Task 1 verification passed:

```text
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/pipe/run.go internal/pipe/run_test.go internal/gitguard/cleanup.go
go test ./internal/pipe -run 'TestRunUnauthorized.*|TestRunSuccess.*Clean' -v
go test ./internal/pipe -v
go test ./...
go vet ./...
! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go'
! git grep -n -E 'exec\.Command(Context)?\("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
git diff --check
```

Result summary:

```text
PASS: go test ./internal/pipe -run 'TestRunUnauthorized.*|TestRunSuccess.*Clean' -v
PASS: go test ./internal/pipe -v
PASS: go test ./...
PASS: go vet ./...
PASS: production broad-staging grep
PASS: production direct-Git-call grep
PASS: git diff --check
```

---

## 5. Review Results

Task 1 used the required two-stage review loop.

### 5.1 Spec-compliance review

Final result:

```text
PASS
```

Spec review confirmed:

- no `SUCCESS` path remains for the covered unauthorized physical residue cases,
- pre-existing nested `.git` and physical residue are rejected before engine cleanup,
- unauthorized residue exits `3` and preserves `HEAD`,
- changed files stayed within Task 1 scope,
- no Codex/live LLM or Sprint 003 integration was introduced.

### 5.2 Code-quality / safety review

Final result:

```text
Critical Issues: None.
Important Issues: None.
Minor Issues: None.
Verdict: APPROVED
```

The review sequence was deliberately hostile. Earlier reviewers found and the implementation fixed hazards not explicit in the first pseudocode snippet, including:

- unreadable non-empty residue cleanup converting to `INTERNAL_ERROR`,
- diagnostic-looking valid paths being hidden as warnings,
- success-path chmod leakage into pre-existing directory modes,
- root and `.git` permission mutations,
- nested `.git` non-empty residue,
- root `.git` residue inside unreadable subdirectories,
- tracked-file mode mutation success,
- allowed-new file and parent directory hidden mode residue.

---

## 6. Final Verification Evidence

Controller verification before the implementation commit:

```text
Command:
set -e
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/pipe/run.go internal/pipe/run_test.go internal/gitguard/cleanup.go
go test ./internal/pipe -run 'TestRunUnauthorized.*|TestRunSuccess.*Clean' -v
go test ./internal/pipe -v
go test ./...
go vet ./...
! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go'
! git grep -n -E 'exec\.Command(Context)?\("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
git diff --check
git status --short --branch

Result:
PASS, with only intended modified files before commit:
 M internal/gitguard/cleanup.go
 M internal/pipe/run.go
 M internal/pipe/run_test.go
```

Implementation commit and push:

```text
git add internal/gitguard/cleanup.go internal/pipe/run.go internal/pipe/run_test.go
git diff --cached --check
git commit -m "fix: block blk-pipe success with physical residue"
git push origin main

Result:
277501b fix: block blk-pipe success with physical residue
origin/main updated: 3c2f8d0..277501b
```

Post-push status:

```text
## main...origin/main
277501b (HEAD -> main, origin/main) fix: block blk-pipe success with physical residue
3c2f8d0 docs: plan blk-pipe sprint 002.1 remediation
76f3cea docs: record blk-pipe sprint 002 closeout hash
```

---

## 7. Safety Invariants Preserved

- No production `git add .`.
- No production `git add -u`.
- Production Git calls remain routed through the bounded helper.
- No triple-dot diffs were introduced.
- No Codex/live LLM integration was introduced.
- Revert remains a fast path before engine/validation/staging/commit.
- Clean preflight remains the boundary before destructive cleanup.
- Unauthorized cleanup remains post-engine/post-validation only after preflight proved there was no pre-existing residue.

---

## 8. Deviations / Notes

The final patch is larger than the initial Task 1 pseudocode because hostile review found that “physical residue” is broader than empty directories. Git can hide residue through permissions, nested Git internals, ignored files, diagnostic-looking filenames, and mode-only filesystem mutations. Those hazards were fixed under the Task 1 policy decision: no `SUCCESS` may leave unauthorized physical state.

No live Codex, live LLM, Sprint 003, BLK-req, BLK-test, or orchestration integration was added.

---

## 9. Next Task

Proceed to Sprint 002.1 Task 2: reap escaped descendants on timeout, flood, and context cancellation.
