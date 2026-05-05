# BLK-pipe Sprint 008 — Task 4 Outcome

**Status:** Complete
**Date:** 2026-05-05
**Task:** Move No-Candidate Diff Gate Before Validation
**Implementation Commit:** included in the Task 4 commit containing this outcome document
**Remote:** pushed to `origin/main` after task verification

---

## 1. Objective

Task 4 closes Sprint 008 finding D-004 by ensuring BLK-pipe does not run validation commands unless the engine has first produced a candidate mutation.

Implemented behavior:

- After engine success, output/flood/timeout checks, `.git` residue checks, and unauthorized physical-residue checks, BLK-pipe compares the post-engine worktree to the pre-engine worktree snapshot.
- If the engine produced no candidate mutation:
  - status is `UNAUTHORIZED_FILE_MUTATION`;
  - exit code is `3`;
  - `validation_logs` remains `{}`;
  - no success commit is created;
  - the workspace is cleaned/restored;
  - validation commands do not run.
- The later staged-file empty gate remains in place as defense in depth.
- Validation success/failure behavior remains unchanged when an engine candidate exists.

---

## 2. Files Changed

Updated:

- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`

Created outcome:

- `docs/outcomes/BLK-PIPE-008_task-004-outcome.md`

---

## 3. RED Evidence

After adding `TestRunSkipsValidationWhenEngineProducesNoCandidateDiff`, the current implementation still executed validation even though the engine produced no candidate diff:

```text
go test ./internal/pipe -run TestRunSkipsValidationWhenEngineProducesNoCandidateDiff -v
=== RUN   TestRunSkipsValidationWhenEngineProducesNoCandidateDiff
    run_test.go:2248: validation logs = map[string]string{"validation_001":"VALIDATION_RAN"}, want empty because validation must not run
--- FAIL: TestRunSkipsValidationWhenEngineProducesNoCandidateDiff (0.04s)
FAIL
FAIL	github.com/camcamcami/BLK-System/internal/pipe	0.043s
FAIL
```

This proved D-004: the old no-candidate/zero-diff gate occurred only after validation had already run.

---

## 4. GREEN Implementation

Implementation details:

- Added a pre-engine physical worktree snapshot beside the existing Git metadata and directory-mode snapshots.
- Added `failNoEngineCandidateDiff(...)` after engine success and unauthorized engine-residue checks, before `snapshotValidationBaseline(...)` and before `validation.Run(...)`.
- The new gate uses the physical worktree snapshot to detect engine-produced candidate mutations before staging.
- If no candidate exists, BLK-pipe returns `UNAUTHORIZED_FILE_MUTATION` / exit `3`, with bounded error `engine produced no candidate diff`, and leaves `validation_logs` empty.
- Updated `TestRunValidationCannotCreateFirstCommitWorthyDiff` so validation can no longer be the first mutator that creates a commit-worthy diff.
- Updated BLK-010 to document that validation runs only after an engine-produced candidate mutation exists.

---

## 5. GREEN Focused Test Evidence

No-candidate focused gate:

```text
go test ./internal/pipe -run TestRunSkipsValidationWhenEngineProducesNoCandidateDiff -v
=== RUN   TestRunSkipsValidationWhenEngineProducesNoCandidateDiff
--- PASS: TestRunSkipsValidationWhenEngineProducesNoCandidateDiff (0.04s)
PASS
ok  	github.com/camcamcami/BLK-System/internal/pipe	0.039s
```

Task 4 focused regression set:

```text
go test ./internal/pipe -run 'NoCandidate|Validation|Unauthorized|Success' -v
=== RUN   TestRunSkipsValidationWhenEngineProducesNoCandidateDiff
--- PASS: TestRunSkipsValidationWhenEngineProducesNoCandidateDiff (0.03s)
=== RUN   TestRunValidationFailureAbortsBeforeCommitAndRestores
--- PASS: TestRunValidationFailureAbortsBeforeCommitAndRestores (0.03s)
=== RUN   TestRunValidationFailureWithoutMutationStillReportsSyntaxGateFailed
--- PASS: TestRunValidationFailureWithoutMutationStillReportsSyntaxGateFailed (0.04s)
=== RUN   TestRunValidationCannotCreateFirstCommitWorthyDiff
--- PASS: TestRunValidationCannotCreateFirstCommitWorthyDiff (0.03s)
=== RUN   TestRunValidationCannotAlterEngineProducedDiff
--- PASS: TestRunValidationCannotAlterEngineProducedDiff (0.03s)
=== RUN   TestRunValidationCanReadWithoutMutating
--- PASS: TestRunValidationCanReadWithoutMutating (0.04s)
=== RUN   TestRunValidationSuccessAllowsCommitAndReportsLogs
--- PASS: TestRunValidationSuccessAllowsCommitAndReportsLogs (0.04s)
PASS
ok  	github.com/camcamcami/BLK-System/internal/pipe	1.901s
```

The focused run also covered existing success and unauthorized-mutation paths, proving validation still runs when the engine produces a candidate and remains blocked or restored on validation-side mutation/failure.

---

## 6. Shared Verification

Final shared verification before commit:

```text
python3 -m unittest discover -s python -p 'test_*.py'
.........................................................................................................................
----------------------------------------------------------------------
Ran 121 tests in 0.660s

OK

go test ./... -> PASS

go vet ./... -> PASS

go run ./cmd/blk-pipe --health -> {"status":"OK","component":"blk-pipe"}

git diff --check -> PASS
```

Post-test cleanup:

```text
python/__pycache__/ removed before committing.
```

---

## 7. Authority / Safety Boundary

Task 4 did not run or enable:

- live Codex;
- live tactical LLM APIs;
- network model services;
- cyber tooling or cyber execution;
- live BLK-test MCP;
- live MCP transport;
- authoritative BLK-test verdict authority;
- authoritative BEO publication;
- RTM generation;
- RTM drift authority;
- sandbox/container/cgroup/VM enforcement;
- production approval-channel mechanics;
- active BLK-req vault reads or requirement-body parsing.

The change only hardens deterministic local BLK-pipe sequencing so validation commands cannot create or discover the first candidate mutation.

---

## 8. Remaining Sprint 008 Work

Task 4 closes D-004 only. Remaining Sprint 008 tasks still own:

- Task 5 / D-005 through D-009: BLK-004/BLK-010 current-state decision overlay;
- Task 6: sprint closeout and hostile self-review.
