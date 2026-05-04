# BLK-pipe Sprint 003 — Task 3 Outcome

**Status:** Complete
**Date:** 2026-05-04
**Task:** Make Revert Branch-Safe
**Commit:** `9710da6 fix: require matching branch for blk-pipe revert`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Prevent `action: "revert"` from resetting the wrong clean branch when `target_branch` is provided.

This implements the BLK-001 context appropriately by keeping BLK-pipe as a deterministic blast shield and repository forge:

- BLK-pipe mechanically enforces the caller's branch intent before a destructive reset.
- BLK-pipe does not infer, fetch, checkout, create, or prepare the requested branch on the revert route.
- BLK-pipe does not invoke Codex, live LLM APIs, Discord HITL flows, BLK-test MCP execution, CEO generation, RTM aggregation, or cyber execution.
- BLK-pipe remains a deterministic transport and safety layer rather than an autonomous decision-maker.

## 2. Files Added/Changed

Implementation commit `9710da6` changed:

```text
docs/BLK-010_blk-pipe-v47-hardening-cli.md
internal/pipe/run.go
internal/pipe/run_test.go
```

No Python adapter changes were required. `BlkPipeAdapter.abort_sprint_and_revert(...)` already includes `target_branch` in revert payloads; this task made the Go pipe enforce that value safely.

## 3. Behavior Implemented

### 3.1 Revert current-branch assertion

`internal/pipe/run.go` now checks `payload.TargetBranch` inside `runRevert` before target-hash resolution, ancestry verification, and `git reset --hard`:

- If `target_branch` is empty, legacy revert behavior is preserved.
- If `target_branch` is non-empty, BLK-pipe reads the current branch using bounded Git helper routing.
- If the repository is detached at `HEAD`, BLK-pipe returns `INVALID_REVERT_ANCHOR` / exit `4`.
- If the current branch differs from `target_branch`, BLK-pipe returns `INVALID_REVERT_ANCHOR` / exit `4`.
- On mismatch, BLK-pipe does not reset, does not create a commit, and preserves the clean worktree.
- On a matching current branch, the existing full-hash target verification, ancestry verification, hard reset, cleanup, and clean verification continue to run.

The new helper path is deterministic and shell-free:

```text
git rev-parse --abbrev-ref HEAD
```

It is invoked through the existing bounded `runGit`/`gitguard.RunGit` stack, not through a shell.

### 3.2 Revert remains a fast path

The routing order remains:

```text
parse and validate payload
clean preflight
if action == "revert": runRevert(...)
execute-path branch preparation only after the revert branch returns
```

Therefore revert still does not run:

- execute-path branch preparation,
- `git fetch`,
- `git checkout` for `target_branch`,
- orphan branch creation,
- engine execution,
- validation commands,
- allowlist staging,
- success commit creation.

### 3.3 Documentation

`docs/BLK-010_blk-pipe-v47-hardening-cli.md` now documents Sprint 003 revert semantics:

- `target_branch` is an optional current-branch assertion for `revert`, not a checkout/fetch directive.
- A different current branch or detached `HEAD` is rejected as `INVALID_REVERT_ANCHOR` with exit `4`.
- BLK-pipe leaves `HEAD` and the clean workspace unchanged on that rejection.

## 4. TDD Evidence

### 4.1 RED

The implementation subagent added failing tests before production changes and ran the focused revert suite.

Command:

```text
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestRunRevertWithTargetBranch|TestRunRevertWithoutTargetBranchPreservesLegacyCurrentBranchBehavior' -v
```

Observed expected RED failure before implementation:

```text
=== RUN   TestRunRevertWithTargetBranchRejectsWrongCurrentBranch
    run_test.go:545: exit code = 0, want 4; report={Status:SUCCESS ... TargetBranch:sprint/right ...}
--- FAIL: TestRunRevertWithTargetBranchRejectsWrongCurrentBranch
```

The failure demonstrated the precise bug: a revert payload with `target_branch: "sprint/right"` could reset the currently checked-out wrong branch because the current branch was not mechanically verified before reset.

The matching-branch and empty-target-branch tests passed at RED time, which was expected because they document preserved behavior rather than the missing guard.

### 4.2 GREEN

Focused revert tests passed after implementation:

```text
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestRunRevert.*Branch|TestRunRevert' -v
```

Controller rerun excerpt:

```text
=== RUN   TestRunRevertSuccessResetsToVerifiedAncestorAndCleans
--- PASS: TestRunRevertSuccessResetsToVerifiedAncestorAndCleans
=== RUN   TestRunRevertWithTargetBranchRejectsWrongCurrentBranch
--- PASS: TestRunRevertWithTargetBranchRejectsWrongCurrentBranch
=== RUN   TestRunRevertWithTargetBranchAcceptsMatchingCurrentBranch
--- PASS: TestRunRevertWithTargetBranchAcceptsMatchingCurrentBranch
=== RUN   TestRunRevertWithoutTargetBranchPreservesLegacyCurrentBranchBehavior
--- PASS: TestRunRevertWithoutTargetBranchPreservesLegacyCurrentBranchBehavior
=== RUN   TestRunRevertSHA256RejectsAbbreviatedFortyHexTarget
--- PASS: TestRunRevertSHA256RejectsAbbreviatedFortyHexTarget
=== RUN   TestRunRevertSHA256AcceptsFullSixtyFourHexTarget
--- PASS: TestRunRevertSHA256AcceptsFullSixtyFourHexTarget
=== RUN   TestRunRevertPreExistingNestedGitRepositoryExitsSevenBeforeReset
--- PASS: TestRunRevertPreExistingNestedGitRepositoryExitsSevenBeforeReset
=== RUN   TestRunRevertInvalidAnchorDoesNotReset
--- PASS: TestRunRevertInvalidAnchorDoesNotReset
=== RUN   TestRunRevertPreExistingEmptyUntrackedDirectoryIsPreserved
--- PASS: TestRunRevertPreExistingEmptyUntrackedDirectoryIsPreserved
=== RUN   TestRunRevertDirtyTrackedWorktreeIsPreserved
--- PASS: TestRunRevertDirtyTrackedWorktreeIsPreserved
=== RUN   TestRunRevertPreExistingUntrackedAndIgnoredFilesArePreserved
--- PASS: TestRunRevertPreExistingUntrackedAndIgnoredFilesArePreserved
=== RUN   TestRunRevertDoesNotRunEngineValidationOrCommit
--- PASS: TestRunRevertDoesNotRunEngineValidationOrCommit
PASS
ok github.com/camcamcami/BLK-System/internal/pipe
```

Full Go and Python suites also passed:

```text
go test ./... PASS
go vet ./... PASS
python3 -m unittest discover -s python -p 'test_*.py' PASS
```

## 5. Review Results

Two fresh review gates were run before pushing the implementation commit.

### 5.1 Spec compliance review

Result: `PASS`

Reviewer findings:

- `run()` still performs `cleanPreflight()` before entering the revert fast path.
- `run()` routes `revert` before execute `target_branch` preparation, engine, validation, staging, or commit logic.
- `runRevert()` now checks nonempty `TargetBranch` before target commit/ancestry checks and before `resetHardTo()`.
- Wrong branch and detached `HEAD` route to `INVALID_REVERT_ANCHOR` / exit `4`.
- Empty `TargetBranch` skips the branch assertion and preserves legacy current-branch behavior.
- Added tests cover wrong branch rejection/no reset/clean preservation, matching branch success, and empty-target-branch legacy behavior.
- BLK-010 documents Sprint 003 `target_branch` assertion behavior.

Focused verification rerun by reviewer:

```text
go test ./internal/pipe -run 'TestRunRevert.*Branch|TestRunRevert' -v PASS
```

### 5.2 Code-quality/security review

Result: `APPROVED`

Reviewer findings:

- New Git usage is deterministic and bounded through `gitguard.RunGit` / `execguard`.
- The current-branch check uses fixed argv and no shell.
- `target_branch` is not passed to Git on the revert route, so it cannot create a checkout/pathspec surface there.
- `target_hash` remains full-hex validated and commit-resolved before reset.
- No broad staging, direct production Git escape, live Codex/LLM/cyber behavior, or branch-preparation scope creep was introduced.
- Tests assert preservation/no reset for wrong-branch failure and success for matching branch.
- Documentation accurately describes `target_branch` as an assertion only and does not overclaim checkout/fetch/create/sterilize behavior on revert.

## 6. Final Verification

Final verification before pushing implementation commit `9710da6`:

```text
gofmt -l internal/pipe/run.go internal/pipe/run_test.go
# no output

go test ./internal/pipe -run 'TestRunRevert.*Branch|TestRunRevert' -v PASS
go test ./... PASS
go vet ./... PASS
python3 -m unittest discover -s python -p 'test_*.py' PASS
```

Safety greps:

```text
! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go' PASS
! git grep -n -E 'exec\.Command(Context)?\("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**' PASS
! git grep -n -E 'git[^\n]*diff[^\n]*\.\.\.' -- '*.go' ':!*_test.go' docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/plans/BLK-PIPE-003_integration-readiness-and-capability-profiles.md docs/outcomes/BLK-PIPE-003_task-001-outcome.md docs/outcomes/BLK-PIPE-003_task-002-outcome.md PASS
```

Diff/status/push:

```text
git diff --check HEAD^ HEAD PASS

git status --short --branch
## main...origin/main [ahead 1]

git push origin main
f7f842f..9710da6 main -> main

git status --short --branch
## main...origin/main
```

## 7. Deviations / Notes

- No Python adapter code change was required because the adapter already transmits `target_branch` in revert payloads.
- `target_branch` on revert is deliberately not branch preparation. It is only a mechanical assertion that the caller already placed the repository on the intended clean branch.
- The first spec reviewer correctly noted that the outcome document was not present during the pre-push implementation review. Per the standard BLK-System workflow, this outcome document is created after implementation review and push, then committed separately as documentation.
- Python adapter tests create `python/__pycache__/`; it was removed before final status/push checks.

## 8. Next Task

Task 4 in `docs/plans/BLK-PIPE-003_integration-readiness-and-capability-profiles.md`: **Bound Payload Ingestion and Validation Work**.
