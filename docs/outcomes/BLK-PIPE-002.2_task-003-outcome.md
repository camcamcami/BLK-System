# BLK-pipe Sprint 002.2 — Task 3 Outcome

**Status:** Complete
**Date:** 2026-05-04
**Task:** Route Validation Safety Violations Above Syntax Failure
**Implementation Commit:** `8727e39 fix: prioritize blk-pipe validation safety failures`
**Remote:** pushed to `origin/main`
**Plan:** `docs/plans/BLK-PIPE-002.2_cyber-readiness-remediation.md`

---

## 1. Objective

Task 3 closed the hostile-review finding that a validation command could fail and mutate `.git` or unauthorized worktree paths while BLK-pipe reported only `SYNTAX_GATE_FAILED` / exit `2`.

Validation safety violations now outrank ordinary validation/syntax failure. If validation mutates `.git`, worktree state, or physical residue, BLK-pipe reports `UNAUTHORIZED_FILE_MUTATION` / exit `3` even when the validation command itself exits non-zero.

---

## 2. Files Changed

Implementation commit:

```text
8727e39 fix: prioritize blk-pipe validation safety failures
 internal/pipe/run.go      |  21 ++++----
 internal/pipe/run_test.go | 131 ++++++++++++++++++++++++++++++++++++++++++++++
 2 files changed, 142 insertions(+), 10 deletions(-)
```

Changed files:

- `internal/pipe/run.go`
- `internal/pipe/run_test.go`

---

## 3. Behavior Implemented

### 3.1 Classification precedence

After validation commands run, BLK-pipe now performs safety audits before ordinary validation failure classification.

Precedence is:

```text
INTERNAL_ERROR if safe cleanup/reporting fails
UNAUTHORIZED_FILE_MUTATION / exit 3 for `.git`, worktree, physical residue, or read-only validation violations
SYNTAX_GATE_FAILED / exit 2 for validation failure without safety mutation
SUCCESS path only when validation succeeds and no safety mutation exists
```

### 3.2 Validation logs preserved

Validation logs remain populated before the safety classification step, so unauthorized mutation reports caused by validation still retain validation output context.

---

## 4. TDD Evidence

### 4.1 RED

The implementation subagent added failing regression tests first. Initial RED behavior:

```text
TestRunValidationFailureWithGitMutationReportsUnauthorized: got SYNTAX_GATE_FAILED / exit 2
TestRunValidationFailureWithUnauthorizedWorktreeMutationReportsUnauthorized: got SYNTAX_GATE_FAILED / exit 2
```

This reproduced the hostile-review finding that safety violations were masked as syntax failures.

### 4.2 GREEN

Final focused verification passed:

```text
go test ./internal/pipe -run 'TestRunValidationFailure.*Unauthorized|TestRunValidationFailureWithoutMutation' -v
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

Task 3 used the required two-stage review loop.

### 5.1 Spec-compliance review

Final result:

```text
PASS
```

The reviewer confirmed:

- validation failure with `.git/hooks/post-commit` mutation returns `UNAUTHORIZED_FILE_MUTATION` / exit `3`,
- validation failure with `rogue.txt` mutation returns `UNAUTHORIZED_FILE_MUTATION` / exit `3`,
- validation failure without mutation still returns `SYNTAX_GATE_FAILED` / exit `2`,
- full tests, vet, and diff checks pass.

### 5.2 Code-quality / security review

Final result:

```text
APPROVED
```

The reviewer confirmed:

- safety audits run before syntax-gate classification,
- validation logs are preserved,
- infrastructure errors remain `INTERNAL_ERROR`,
- Task 2 read-only validation semantics are not regressed,
- no content-leak regression was introduced.

---

## 6. Final Verification Evidence

Controller verification before push:

```text
gofmt -l internal/pipe/run.go internal/pipe/run_test.go
# no output

go test ./internal/pipe -run 'TestRunValidationFailure.*Unauthorized|TestRunValidationFailureWithoutMutation' -v
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
origin/main updated to 8727e39
```

Post-push status:

```text
## main...origin/main
8727e39 (HEAD -> main, origin/main) fix: prioritize blk-pipe validation safety failures
```

---

## 7. Safety Invariants Preserved

- No production `git add .`.
- No production `git add -u`.
- No live Codex or live LLM integration.
- No offensive cyber behavior.
- Validation remains read-only relative to the post-engine candidate state.
- Safety violations outrank ordinary syntax/validation failure.
- No success commit is created on validation failure.

---

## 8. Deviations / Notes

Task 3 builds directly on Task 2's read-only validation baseline. The two tasks together ensure validation cannot become a mutation engine and cannot hide a safety violation behind a syntax-failure status.

---

## 9. Next Task

Proceed to Sprint 002.2 Task 4: deliver bounded V47 `l2_packet` content to engine stdin without logging packet contents by default.
