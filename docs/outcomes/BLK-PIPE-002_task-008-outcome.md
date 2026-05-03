# BLK-pipe Sprint 002 — Task 8 Outcome

**Status:** Complete
**Date:** 2026-05-03
**Task:** Task 8 — Add Revert Escape Hatch
**Commit:** `22b08e0 feat: add blk-pipe revert action`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Implement the BLK-004/V47 revert escape hatch for `blk-pipe`:

- support `action: "revert"` payloads,
- require a verified absolute `target_hash`,
- reject relative anchors, branch names, tag names, and pathspec-like values,
- run revert before execute branch/fetch/engine/validation/staging/commit logic,
- preserve pre-existing dirty user work,
- verify ancestry with `git merge-base --is-ancestor`,
- return `INVALID_REVERT_ANCHOR` with exit code `4` for invalid anchors,
- reset to a verified ancestor and clean the workspace on successful revert,
- emit exactly one JSON report.

Task 8 deliberately did not add branch/fetch/orphan behavior and did not invoke Codex or any live tactical LLM engine.

## 2. Files Added/Changed

Changed:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`

No production dependencies were added.

## 3. Behavior Implemented

### 3.1 Payload contract

`contracts.Payload` now supports `target_hash` for revert payloads.

Revert validation now requires:

- `action: "revert"`,
- absolute `workdir` / normalized `work_dir`,
- present `target_hash`,
- hex-only full object-ID-shaped target values,
- no symbolic or relative anchors such as `HEAD`, `HEAD~1`, `HEAD^`, or `@{1}`,
- no branch/tag names,
- no pathspec-ish target values.

### 3.2 Revert fast path

`pipe.Run` now routes `action: "revert"` before execute-path branch/fetch/engine/validation/staging/commit logic.

The revert path:

1. parses and validates the payload,
2. creates a report with stable JSON fields,
3. runs clean preflight before destructive operations,
4. verifies the target hash resolves to a commit object,
5. compares Git's resolved full object ID to the payload target hash so SHA-256 abbreviated prefixes are rejected,
6. checks ancestry with `git merge-base --is-ancestor <target_hash> HEAD`,
7. returns `INVALID_REVERT_ANCHOR` / exit `4` if resolution or ancestry fails,
8. runs `git reset --hard <target_hash>` on success,
9. cleans with double-force ignored cleanup (`git clean -ffdx -q`) to remove nested Git worktrees left by reset transitions,
10. verifies the post-revert workspace is clean before reporting `SUCCESS`,
11. emits one JSON report and returns exit `0`.

### 3.3 Dirty-work preservation

Revert preflight now rejects and preserves:

- dirty tracked files,
- pre-existing untracked files,
- pre-existing ignored files,
- pre-existing empty untracked directories that Git status does not report.

This prevents revert cleanup from deleting user-created filesystem state that existed before the revert request.

### 3.4 Non-goals preserved

Task 8 does not:

- create or switch branches,
- fetch remotes,
- create orphan branches,
- run engine commands,
- run validation commands,
- stage files,
- create commits,
- call Codex or any live LLM.

## 4. TDD Evidence

### 4.1 RED

The implementation subagent added tests before production code.

Initial RED evidence:

```text
go test ./internal/contracts -run 'TestPayload.*Revert' -v
```

Failed because `contracts.Payload` did not yet have the `TargetHash` field / revert validation behavior.

```text
go test ./internal/pipe -run 'TestRun.*Revert' -v
```

Failed because the pipe layer did not yet expose `TargetHash` and had no revert route.

Review-driven RED regression evidence:

```text
TestRunRevertSHA256RejectsAbbreviatedFortyHexTarget
```

Initially returned `SUCCESS` / exit `0` for a 40-hex prefix in a SHA-256 repository; expected `INVALID_REVERT_ANCHOR` / exit `4`.

```text
TestRunRevertCleansNestedGitRepositoryAddedAfterTarget
```

Initially left a nested Git worktree behind after a successful revert.

```text
TestRunRevertPreExistingEmptyUntrackedDirectoryIsPreserved
```

Initially returned `SUCCESS` / exit `0` and deleted the empty directory; expected dirty-preflight abort and preservation.

### 4.2 GREEN

Focused Task 8 tests now pass:

```text
=== RUN   TestPayloadValidateRevertAcceptsAbsoluteWorkdirAndFullTargetHash
--- PASS: TestPayloadValidateRevertAcceptsAbsoluteWorkdirAndFullTargetHash (0.00s)
=== RUN   TestPayloadDecodeRevertV47WorkDirAndTargetHash
--- PASS: TestPayloadDecodeRevertV47WorkDirAndTargetHash (0.00s)
=== RUN   TestPayloadValidateRevertRejectsMissingOrUnsafeTargetHash
--- PASS: TestPayloadValidateRevertRejectsMissingOrUnsafeTargetHash (0.00s)
=== RUN   TestPayloadValidateRevertRequiresAbsoluteWorkdir
--- PASS: TestPayloadValidateRevertRequiresAbsoluteWorkdir (0.00s)
PASS
ok  github.com/camcamcami/BLK-System/internal/contracts
```

```text
=== RUN   TestRunRevertSuccessResetsToVerifiedAncestorAndCleans
--- PASS: TestRunRevertSuccessResetsToVerifiedAncestorAndCleans (0.04s)
=== RUN   TestRunRevertSHA256RejectsAbbreviatedFortyHexTarget
--- PASS: TestRunRevertSHA256RejectsAbbreviatedFortyHexTarget (0.03s)
=== RUN   TestRunRevertSHA256AcceptsFullSixtyFourHexTarget
--- PASS: TestRunRevertSHA256AcceptsFullSixtyFourHexTarget (0.03s)
=== RUN   TestRunRevertCleansNestedGitRepositoryAddedAfterTarget
--- PASS: TestRunRevertCleansNestedGitRepositoryAddedAfterTarget (0.04s)
=== RUN   TestRunRevertInvalidAnchorDoesNotReset
--- PASS: TestRunRevertInvalidAnchorDoesNotReset (0.03s)
=== RUN   TestRunRevertPreExistingEmptyUntrackedDirectoryIsPreserved
--- PASS: TestRunRevertPreExistingEmptyUntrackedDirectoryIsPreserved (0.02s)
=== RUN   TestRunRevertDirtyTrackedWorktreeIsPreserved
--- PASS: TestRunRevertDirtyTrackedWorktreeIsPreserved (0.02s)
=== RUN   TestRunRevertPreExistingUntrackedAndIgnoredFilesArePreserved
--- PASS: TestRunRevertPreExistingUntrackedAndIgnoredFilesArePreserved (0.05s)
=== RUN   TestRunRevertDoesNotRunEngineValidationOrCommit
--- PASS: TestRunRevertDoesNotRunEngineValidationOrCommit (0.03s)
PASS
ok  github.com/camcamcami/BLK-System/internal/pipe 0.296s
```

## 5. Review Results

### 5.1 First review gate

Spec compliance review initially failed on a real gap:

- In SHA-256 repositories, a 40-hex target was accepted as an abbreviated prefix even though Task 8 requires full object IDs.

Code-quality review initially requested changes on two safety gaps:

- successful revert over a nested Git/submodule-like transition could leave the repository dirty while reporting `SUCCESS`,
- pre-existing empty untracked directories were missed by Git status preflight and could be deleted by cleanup.

### 5.2 Fix and amended commit

A fix subagent added regression tests first, implemented the corrections, and amended the unpushed implementation commit.

Fixes added:

- full object-ID resolution comparison for SHA-1/SHA-256 repositories,
- `git clean -ffdx -q` for revert cleanup after clean preflight,
- post-revert clean verification,
- explicit empty untracked directory detection before destructive revert.

### 5.3 Final review gate

Spec compliance re-review:

```text
Verdict: PASS
```

Code-quality/safety re-review:

```text
Verdict: APPROVED
Critical Issues: None.
Important Issues: None.
Minor Issues: None.
```

## 6. Final Verification

Controller final verification before push:

```text
gofmt -l:
```

No files were listed by `gofmt -l`.

```text
go test ./internal/contracts -run 'TestPayload.*Revert' -v
```

Passed.

```text
go test ./internal/pipe -run 'TestRun.*Revert' -v
```

Passed.

```text
go test ./...
```

Passed for all packages:

```text
ok  github.com/camcamcami/BLK-System/cmd/blk-pipe
ok  github.com/camcamcami/BLK-System/internal/contracts
ok  github.com/camcamcami/BLK-System/internal/engine
ok  github.com/camcamcami/BLK-System/internal/execguard
ok  github.com/camcamcami/BLK-System/internal/gitguard
ok  github.com/camcamcami/BLK-System/internal/pipe
ok  github.com/camcamcami/BLK-System/internal/runtimeguard
ok  github.com/camcamcami/BLK-System/internal/testutil
ok  github.com/camcamcami/BLK-System/internal/validation
```

Additional checks:

```text
go vet ./...
```

Passed.

```text
! git grep -n 'exec.Command("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
```

Passed; no disallowed production direct Git calls.

```text
! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go'
```

Passed; no production broad staging commands.

```text
git diff --check HEAD^ HEAD
```

Passed.

Push result:

```text
To https://github.com/camcamcami/BLK-System.git
   8328cc9..22b08e0  main -> main
```

Repository status after push:

```text
## main...origin/main
```

## 7. Deviations / Notes

- The implementation tightened the plan's "full hex commit object IDs" requirement by verifying the resolved Git commit object ID exactly equals the payload `target_hash`. This matters for SHA-256 repositories where 40 hex characters can otherwise be accepted by Git as an abbreviation.
- Revert cleanup uses `git clean -ffdx -q`, not the older BLK-004 text's `git clean -fd`, because Sprint 002 Task 5/Task 7 hardening established double-force ignored cleanup as the safe deterministic cleanup after clean preflight.
- Empty untracked directories required an explicit filesystem scan because Git status/ls-files do not report them.
- No Codex or live LLM integration was introduced.

## 8. Next Task

Next incomplete Sprint 002 task is:

```text
Task 9 — Add Branch/Fetch/Orphan Workspace Preparation For Execute
```

Task 9 should add deterministic execute-path branch preparation, including target branch validation, dirty current-workspace rejection before branch switching, local/remote branch checkout, optional headless `ls-remote`, true empty orphan initialization with `git read-tree --empty`, hook-disabled initialization commit, and pre-engine hash capture after branch preparation.
