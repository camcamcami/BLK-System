# BLK-pipe Sprint 002.2 — Task 2 Outcome

**Status:** Complete
**Date:** 2026-05-04
**Task:** Enforce Read-Only Validation Semantics
**Implementation Commit:** `cd6898d fix: prevent validation-authored blk-pipe diffs`
**Remote:** pushed to `origin/main`
**Plan:** `docs/plans/BLK-PIPE-002.2_cyber-readiness-remediation.md`

---

## 1. Objective

Task 2 closed the hostile-review finding that validation commands could author or alter the committed diff.

Validation is now enforced as a read-only gate relative to the post-engine candidate state. If validation mutates tracked files, allowed files, unallowlisted files, physical residue, directory modes, or `.git` metadata, BLK-pipe reports `UNAUTHORIZED_FILE_MUTATION` / exit `3`, restores/cleans the run, and does not create a success commit.

---

## 2. Files Changed

Implementation commit:

```text
cd6898d fix: prevent validation-authored blk-pipe diffs
 internal/pipe/run.go      | 219 ++++++++++++++++++++++++++++++++++++++++++++++
 internal/pipe/run_test.go | 150 +++++++++++++++++++++++++++++++
 2 files changed, 369 insertions(+)
```

Changed files:

- `internal/pipe/run.go`
- `internal/pipe/run_test.go`

---

## 3. Behavior Implemented

### 3.1 Post-engine validation baseline

After the engine succeeds and pre-validation safety audits pass, BLK-pipe now records a post-engine candidate baseline before validation runs.

### 3.2 Validation mutation rejection

After validation completes, BLK-pipe compares the post-validation state against the post-engine baseline. Any validation-induced mutation routes to:

```text
UNAUTHORIZED_FILE_MUTATION / exit 3
```

This prevents validation from creating the first commit-worthy diff or altering an engine-produced diff.

### 3.3 Read-only and external-temp validation remain usable

Read-only validation still succeeds, and validation may write to an external temp path outside the repository without triggering worktree mutation failure.

---

## 4. TDD Evidence

### 4.1 RED

The implementation subagent added the required failing regression tests first. Initial RED behavior showed:

```text
TestRunValidationCannotCreateFirstCommitWorthyDiff: validation-created README.md was committed as SUCCESS
TestRunValidationCannotAlterEngineProducedDiff: validation overwrote engine README.md and was committed as SUCCESS
```

These failures reproduced the hostile-review finding that validation could act as a second mutation engine.

### 4.2 GREEN

Final focused verification passed:

```text
go test ./internal/pipe -run 'TestRunValidationCannot|TestRunValidationCanRead|TestRunValidationMayUseExternalTemp' -v
PASS

go test ./internal/pipe -run 'TestRun.*Validation' -v
PASS

go test ./...
PASS

go vet ./...
PASS

git diff --check
PASS
```

---

## 5. Review Results

Task 2 used the required two-stage review loop.

### 5.1 Spec-compliance review

Final result:

```text
PASS
```

The reviewer confirmed:

- validation-created first diffs are rejected,
- validation alteration of engine-produced diffs is rejected,
- read-only validation still succeeds,
- external temp writes outside the worktree still succeed,
- no success commit is created from validation-authored changes.

### 5.2 Code-quality / security review

Final result:

```text
APPROVED
```

The reviewer confirmed:

- validation baseline is taken after engine mutations and before validation,
- cleanup ordering restores Git metadata and resets to `pre_engine_hash`,
- validation logs are preserved,
- existing `.git` mutation/restoration tests still pass,
- report output includes paths rather than file contents,
- clean preflight still protects pre-existing user work.

---

## 6. Final Verification Evidence

Controller verification before push:

```text
gofmt -l internal/pipe/run.go internal/pipe/run_test.go
# no output

go test ./internal/pipe -run 'TestRunValidationCannot|TestRunValidationCanRead|TestRunValidationMayUseExternalTemp' -v
PASS

go test ./internal/pipe -run 'TestRun.*Validation' -v
PASS

go test ./...
PASS

go vet ./...
PASS

git diff --check
PASS

git push origin main
origin/main updated to cd6898d
```

Post-push status:

```text
## main...origin/main
cd6898d (HEAD -> main, origin/main) fix: prevent validation-authored blk-pipe diffs
```

---

## 7. Safety Invariants Preserved

- No production `git add .`.
- No production `git add -u`.
- No live Codex or live LLM integration.
- No offensive cyber behavior.
- Validation remains a gate, not a mutation authority.
- Validation logs are preserved on failure paths.
- Pre-existing user work remains protected by clean preflight.

---

## 8. Deviations / Notes

Task 2 intentionally does not introduce repository-internal validation scratch paths. Validation scratch behavior remains outside the repository unless future doctrine explicitly grants validator write authority.

---

## 9. Next Task

Proceed to Sprint 002.2 Task 3: route validation safety violations above syntax failure so `.git` or unauthorized worktree mutation during failing validation reports `UNAUTHORIZED_FILE_MUTATION` rather than `SYNTAX_GATE_FAILED`.
