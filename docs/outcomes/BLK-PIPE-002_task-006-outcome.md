# BLK-PIPE-002 Task 006 Outcome — V47 Execution Report Details

Status: COMPLETE
Date: 2026-05-03
Sprint plan: `docs/plans/BLK-PIPE-002_v47-hardening-layer.md`
Task: Sprint 002 Task 6 — add pre-engine hash, mandatory zero-diff abort, diff summary, Git diff, and untracked report fields
Implementation commit: `9819f01 feat: report blk-pipe v47 execution details`
Remote: pushed to `origin/main`

## Summary

Task 006 completed the V47 execution-report detail layer for successful BLK-pipe execute runs and enforced BLK-004's mandatory no-silent-staging-failure rule.

The implementation records the pre-engine `HEAD`, fills V47 diff/report fields after successful bounded engine execution, parses a deterministic diff summary, reports final untracked files using the BLK-004 rogue-audit shape, and converts zero staged allowlisted changes into `UNAUTHORIZED_FILE_MUTATION` / exit `3` instead of allowing a silent success.

The implementation was pushed to `origin/main` as:

```text
9819f01 feat: report blk-pipe v47 execution details
```

## Files Changed

```text
internal/pipe/run.go
internal/pipe/run_test.go
```

Commit stat:

```text
internal/pipe/run.go      | 163 +++++++++++++++++++++++++++++++++++++++---
internal/pipe/run_test.go | 175 ++++++++++++++++++++++++++++++++++++++++++++--
2 files changed, 323 insertions(+), 15 deletions(-)
```

`internal/contracts/report.go` was not modified because the V47 `Report` fields and `DiffSummary` type already existed from Sprint 002 Task 2.

## Implemented Behavior

### Pre-engine hash capture

`pipe.Run` now captures the current `HEAD` after clean preflight and before engine execution:

```text
pre_engine_hash = git rev-parse HEAD
```

This value is assigned to `report.PreEngineHash` for execute paths after payload validation and clean-worktree checks, before the engine can mutate the workspace.

### Mandatory zero-diff abort

Task 006 enforces BLK-004's no-silent-staging-failure rule:

```text
If no allowlisted change is staged, return UNAUTHORIZED_FILE_MUTATION and exit 3.
```

The implementation covers both:

- allowlisted existing files where the engine exits `0` but makes no content change, and
- allowlisted new files that the engine was expected to create but did not.

In these cases BLK-pipe now:

- returns exit code `3`,
- reports status `UNAUTHORIZED_FILE_MUTATION`,
- preserves `HEAD`,
- does not create a commit,
- cleans the workspace.

### Successful report fields

For successful execute runs, the report now includes:

- `pre_engine_hash` — the pre-engine commit hash,
- `git_diff` — from `git diff <PreEngineHash> HEAD --`,
- `diff_summary` — parsed from `git diff <PreEngineHash> HEAD --numstat --`,
- `untracked_files` — from the final rogue-file audit shape,
- `exit_code` — already set by the outer report writer,
- `engine_logs` — already wired by Task 3 and preserved here.

The final untracked report collection uses the BLK-004-compatible command shape:

```text
git ls-files -z --others --exclude-standard --directory
```

Internal dirty/preflight and unauthorized-file detection keep their stricter no-exclude behavior so ignored-file protections from Sprint 001 / Sprint 002 Task 5 are not weakened.

### Diff and summary extraction

The implementation deliberately uses two-dot range diff commands from the pre-engine hash to final `HEAD`:

```text
git diff <PreEngineHash> HEAD --
git diff <PreEngineHash> HEAD --numstat --
```

No triple-dot diff is introduced.

The `diff_summary` parser records:

- `files_changed`,
- `insertions`,
- `deletions`,
- `files`.

Binary `-` numstat entries are treated as zero insertions/deletions while still counting the file.

### Post-commit report failure safety

The first code-quality review identified that post-commit report-generation failures could leave a commit behind while returning `INTERNAL_ERROR`.

The final implementation fixes this by rolling back and cleaning to the pre-engine state if any post-commit report generation step fails after the commit is created. On those internal-error rollback paths, `commit_hash` is cleared so the report does not imply that a successful commit was retained.

## TDD Evidence

### Initial RED evidence

The implementation subagent wrote Task 006 tests before production changes. The initial focused test run failed against the pre-Task-006 code:

```text
TestRunSuccessReportsBoundedEngineLogs
run_test.go:...: PreEngineHash is empty

TestRunZeroDiffAfterSuccessfulEngineIsUnauthorizedMutation
run_test.go:...: exit code = 0, want 3
```

This proved the report fields were not populated and zero-diff success was still incorrectly permitted.

### Review-fix RED evidence

After the first review gate found gaps, the fix subagent added regression tests before patching production code.

The missing-allowed-new regression failed against the first Task 006 implementation:

```text
TestRunMissingAllowedNewAfterSuccessfulEngineIsUnauthorizedMutation
exit code = 9, want 3
```

The post-commit report-generation rollback regression also failed against the first Task 006 implementation:

```text
TestRunReportGenerationFailureRollsBackCommittedChange
CommitHash remained set after report-generation failure
```

Those RED failures matched the review findings and were fixed before the commit was amended.

### GREEN evidence

Final focused verification passed:

```text
go test ./internal/pipe -run 'TestRunSuccess.*Report|TestRun.*ZeroDiff|TestRun.*MissingAllowedNew|TestRun.*ReportGeneration' -v
=== RUN   TestRunSuccessReportsBoundedEngineLogs
--- PASS: TestRunSuccessReportsBoundedEngineLogs (0.03s)
=== RUN   TestRunSuccessReportUntrackedFilesUsesRogueAuditShape
--- PASS: TestRunSuccessReportUntrackedFilesUsesRogueAuditShape (0.01s)
=== RUN   TestRunZeroDiffAfterSuccessfulEngineIsUnauthorizedMutation
--- PASS: TestRunZeroDiffAfterSuccessfulEngineIsUnauthorizedMutation (0.03s)
=== RUN   TestRunMissingAllowedNewAfterSuccessfulEngineIsUnauthorizedMutation
--- PASS: TestRunMissingAllowedNewAfterSuccessfulEngineIsUnauthorizedMutation (0.03s)
=== RUN   TestRunReportGenerationFailureRollsBackCommittedChange
--- PASS: TestRunReportGenerationFailureRollsBackCommittedChange (0.04s)
PASS
ok  github.com/camcamcami/BLK-System/internal/pipe  0.146s
```

Full-suite verification also passed:

```text
go test ./...
ok  github.com/camcamcami/BLK-System/cmd/blk-pipe        (cached)
ok  github.com/camcamcami/BLK-System/internal/contracts   (cached)
ok  github.com/camcamcami/BLK-System/internal/engine      (cached)
ok  github.com/camcamcami/BLK-System/internal/execguard   (cached)
ok  github.com/camcamcami/BLK-System/internal/gitguard    (cached)
ok  github.com/camcamcami/BLK-System/internal/pipe        (cached)
ok  github.com/camcamcami/BLK-System/internal/runtimeguard (cached)
ok  github.com/camcamcami/BLK-System/internal/testutil    (cached)
```

## Review Results

Task 006 used the Sprint 002 two-stage review gate. The controller did not push until final spec and quality reviews passed.

### Spec compliance review

Initial spec review verdict:

```text
REQUEST_CHANGES
```

The reviewer found two concrete gaps:

1. Missing allowlisted new files were still treated as staging infrastructure errors (`INTERNAL_ERROR` / exit `9`) rather than zero-diff unauthorized mutations (`UNAUTHORIZED_FILE_MUTATION` / exit `3`).
2. Final `untracked_files` collection used a generic `git ls-files --others -z` shape rather than the BLK-004 rogue-audit shape with `--exclude-standard --directory`.

Fixes applied:

- added and passed `TestRunMissingAllowedNewAfterSuccessfulEngineIsUnauthorizedMutation`,
- added and passed `TestRunSuccessReportUntrackedFilesUsesRogueAuditShape`,
- separated final report untracked collection from stricter internal dirty/unauthorized detection.

Final spec review verdict:

```text
PASS
```

Final spec review confirmed:

- `pre_engine_hash` is captured after clean preflight and before engine execution,
- `git_diff` and `diff_summary` are populated from `git diff <PreEngineHash> HEAD --` and matching numstat,
- final `untracked_files` uses the expected rogue-audit shape,
- zero-diff and missing-allowed-new cases return `UNAUTHORIZED_FILE_MUTATION` / exit `3`, preserve `HEAD`, and leave the repo clean,
- ignored/untracked protections remain intact.

### Code-quality/safety review

Initial code-quality review verdict:

```text
REQUEST_CHANGES
```

The reviewer found one important issue:

- post-commit report-generation failures could return `INTERNAL_ERROR` after a commit had already been created, leaving `HEAD` mutated despite a non-success result.

Fix applied:

- added and passed `TestRunReportGenerationFailureRollsBackCommittedChange`,
- changed report-generation error handling so post-commit failures roll back to the pre-engine state, clean the repo, and clear `commit_hash`.

Final code-quality review verdict:

```text
APPROVED
```

Final quality review confirmed:

- bounded Git helper usage is preserved,
- no direct production `exec.Command("git")` is introduced outside the allowed helper,
- no broad staging commands are introduced,
- no triple-dot diff is introduced,
- zero-diff and missing-allowed-new behavior leave the repo clean with no commit,
- post-commit report-generation failures no longer leave retained commits behind,
- report-only untracked collection does not weaken ignored-file protections,
- tests are meaningful and deterministic.

## Final Controller Verification

Final controller verification before pushing the implementation used:

```bash
export PATH="$HOME/.local/bin:$PATH"
test -z "$(gofmt -l internal/pipe/run.go internal/pipe/run_test.go internal/contracts/report.go)"
go test ./internal/pipe -run 'TestRunSuccess.*Report|TestRun.*ZeroDiff|TestRun.*MissingAllowedNew|TestRun.*ReportGeneration' -v
go test ./...
go vet ./...
! git grep -n 'exec.Command("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
git diff --check HEAD^ HEAD
git status --short --branch
git log --oneline --decorate -4
git push origin main
git status --short --branch
```

Final verification results:

```text
== gofmt check ==
# no output

== focused tests ==
PASS
ok  github.com/camcamcami/BLK-System/internal/pipe  (cached)

== full tests ==
ok  github.com/camcamcami/BLK-System/cmd/blk-pipe        (cached)
ok  github.com/camcamcami/BLK-System/internal/contracts   (cached)
ok  github.com/camcamcami/BLK-System/internal/engine      (cached)
ok  github.com/camcamcami/BLK-System/internal/execguard   (cached)
ok  github.com/camcamcami/BLK-System/internal/gitguard    (cached)
ok  github.com/camcamcami/BLK-System/internal/pipe        (cached)
ok  github.com/camcamcami/BLK-System/internal/runtimeguard (cached)
ok  github.com/camcamcami/BLK-System/internal/testutil    (cached)

== vet ==
# no output

== safety greps ==
# no output

== diff check ==
# no output
```

Push result:

```text
To https://github.com/camcamcami/BLK-System.git
   fd269d6..9819f01  main -> main
## main...origin/main
```

## Deviations / Notes

- No Codex or live LLM integration was introduced.
- `internal/contracts/report.go` did not require modification because Task 2 had already added the necessary V47 report schema fields.
- The implementation keeps strict internal ignored-file detection for preflight/unauthorized cleanup while using the BLK-004 `--exclude-standard --directory` form for the final success report's `untracked_files` field.
- The rollback regression intentionally exercises a bounded diff-output failure after commit by making the final report generation exceed the Git helper output cap; this ensures non-success report paths do not retain a newly created commit.

## Next Task

The next planned Sprint 002 task is Task 7: add the sequential validation command gate.

Task 7 should run validation commands only after engine success and `.git` mutation audit, aggregate bounded validation logs, abort before staging/commit on validation failure, restore to `PreEngineHash`, and ensure validation never runs after detected `.git` mutation.
