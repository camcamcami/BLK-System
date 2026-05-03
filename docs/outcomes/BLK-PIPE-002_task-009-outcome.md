# BLK-pipe Sprint 002 — Task 9 Outcome

**Status:** Complete
**Date:** 2026-05-03
**Task:** Task 9 — Add Branch/Fetch/Orphan Workspace Preparation For Execute
**Commit:** `2d7582c feat: add blk-pipe branch preparation`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Implement BLK-004/V47 branch preparation for execute payloads that provide `target_branch`:

- validate branch names before Git sees them,
- reject dirty current workspaces before branch switching,
- fetch `origin` when present,
- check out an existing local branch when available,
- otherwise track `origin/<target_branch>` when available,
- otherwise create an initialized orphan branch,
- initialize orphan branches with an empty tree before `PreEngineHash` capture,
- keep revert as a fast path that does not run branch preparation,
- preserve Sprint 001/002 file-boundary and Git safety invariants.

Task 9 deliberately did not invoke Codex or any live tactical LLM engine.

## 2. Files Added/Changed

Added:

- `internal/gitguard/branch.go`
- `internal/gitguard/branch_test.go`

Changed:

- `internal/contracts/payload.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`

No production dependencies were added.

## 3. Behavior Implemented

### 3.1 Branch-name validation

`internal/gitguard.ValidateBranchName` now applies a conservative branch policy before `target_branch` values are passed to Git argv.

It accepts normal branch names such as:

- `feature/local`,
- `sprint/ceb-011`,
- `release-2026.05`,
- `users/alice_task-123`.

It rejects unsafe branch names including:

- empty values,
- leading/trailing whitespace,
- control characters,
- names starting with `-`,
- absolute/path traversal syntax,
- `refs/...` inputs,
- `HEAD` / `HEAD~1`-style revision syntax,
- reflog syntax such as `@{upstream}`,
- shell metacharacters,
- pathspec/glob metacharacters,
- hidden or `.lock` ref path components.

`contracts.Payload.Validate` now rejects non-empty invalid `target_branch` values during payload validation before repository mutation. Empty `target_branch` remains the legacy/no-branch-prep path.

### 3.2 Bounded branch preparation helper

`internal/gitguard.PrepareTargetBranch` now provides the execute-path branch preparation sequence:

1. validate `target_branch`,
2. run clean preflight before switching,
3. detect whether `origin` exists,
4. run bounded `git fetch origin` when `origin` exists,
5. check out an existing local branch if present,
6. otherwise check out `-t origin/<target_branch>` if a remote-tracking branch is present,
7. otherwise use bounded `git ls-remote --symref --heads origin refs/heads/<target_branch>` with hardened SSH environment if needed,
8. otherwise create an orphan branch,
9. clear inherited index/tree with `git read-tree --empty`,
10. create a hooks-disabled empty initialization commit with message `Initialize branch`.

The `ls-remote` fallback injects:

```text
GIT_SSH_COMMAND=ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes
```

All production Git execution remains routed through `internal/gitguard/command.go` bounded helpers. Branch values are passed as argv; no shell is introduced.

### 3.3 Execute-path integration

`pipe.Run` now calls branch preparation for execute payloads with non-empty `target_branch` before `PreEngineHash` capture.

The execute path now follows this ordering:

1. parse and validate payload,
2. run initial clean preflight,
3. keep `action: "revert"` on the existing fast path,
4. for execute payloads with `target_branch`, prepare the target branch,
5. run post-prep clean preflight/sterilization checks,
6. capture `PreEngineHash` from the prepared branch,
7. proceed with engine execution, `.git` audit, validation, staging, cleanup, commit, and report generation.

The revert route remains isolated from branch prep and still does not run engine, validation, staging, or commit logic.

### 3.4 Orphan branch safety

Orphan fallback now avoids BLK-004's “orphan amnesia” failure mode:

- `git checkout --orphan <target_branch>` creates the branch,
- `git read-tree --empty` prevents inherited tree/index contents from being committed,
- `git -c core.hooksPath=/dev/null commit --allow-empty -m "Initialize branch"` establishes a valid `HEAD` before the engine path captures `PreEngineHash`,
- tests assert the initialization commit tree is empty and does not include inherited `README.md`.

## 4. TDD Evidence

### 4.1 RED

The implementation subagent wrote failing tests before production code.

Initial gitguard RED evidence:

```text
go test ./internal/gitguard -run 'Test.*Branch|TestPrepareTargetBranch' -v
```

Failed initially because `ValidateBranchName` and `PrepareTargetBranch` did not exist.

Initial pipe RED evidence:

```text
go test ./internal/pipe -run 'TestRun.*Branch|TestRun.*Orphan' -v
```

Failed initially because execute runs stayed on the current branch instead of preparing and executing on the requested target branch.

### 4.2 GREEN

Focused Task 9 gitguard tests now pass:

```text
=== RUN   TestValidateBranchNameAcceptsSafeBranchNames
--- PASS: TestValidateBranchNameAcceptsSafeBranchNames (0.00s)
=== RUN   TestValidateBranchNameRejectsUnsafeBranchNames
--- PASS: TestValidateBranchNameRejectsUnsafeBranchNames (0.00s)
=== RUN   TestPrepareTargetBranchRejectsDirtyCurrentWorkspaceBeforeCheckout
--- PASS: TestPrepareTargetBranchRejectsDirtyCurrentWorkspaceBeforeCheckout (0.02s)
=== RUN   TestPrepareTargetBranchChecksOutExistingLocalBranch
--- PASS: TestPrepareTargetBranchChecksOutExistingLocalBranch (0.03s)
=== RUN   TestPrepareTargetBranchTracksRemoteBranch
--- PASS: TestPrepareTargetBranchTracksRemoteBranch (0.07s)
=== RUN   TestPrepareTargetBranchCreatesEmptyInitializedOrphan
--- PASS: TestPrepareTargetBranchCreatesEmptyInitializedOrphan (0.02s)
PASS
ok  github.com/camcamcami/BLK-System/internal/gitguard
```

Focused Task 9 pipe tests now pass:

```text
=== RUN   TestRunTargetBranchRejectsDirtyCurrentWorkspaceBeforeCheckout
--- PASS: TestRunTargetBranchRejectsDirtyCurrentWorkspaceBeforeCheckout (0.02s)
=== RUN   TestRunTargetBranchExecutesOnExistingLocalBranch
--- PASS: TestRunTargetBranchExecutesOnExistingLocalBranch (0.06s)
=== RUN   TestRunTargetBranchTracksRemoteBranch
--- PASS: TestRunTargetBranchTracksRemoteBranch (0.09s)
=== RUN   TestRunTargetBranchOrphanInitializesEmptyTreeBeforeEngine
--- PASS: TestRunTargetBranchOrphanInitializesEmptyTreeBeforeEngine (0.05s)
PASS
ok  github.com/camcamcami/BLK-System/internal/pipe
```

## 5. Review Results

### 5.1 Spec compliance review

A fresh subagent reviewed HEAD commit `2d7582c` against Sprint 002 Task 9 and BLK-004 snippets.

Result:

```text
Verdict: PASS
```

Reviewer confirmed:

- branch validation coverage,
- clean-workspace abort before switching,
- origin fetch,
- local/tracking/`ls-remote`/orphan fallback flow,
- empty orphan initialization commit with hooks disabled,
- post-branch preflight/sterilization before `PreEngineHash`,
- revert path does not run branch prep,
- TDD coverage for validation, dirty abort, local checkout, remote tracking, orphan empty-tree/final execution, and post-checkout behavior.

### 5.2 Code-quality/safety review

A fresh code-quality reviewer inspected HEAD commit `2d7582c` and ran the required checks.

Result:

```text
Critical Issues: None.
Important Issues: None.
Minor Issues: None.
Verdict: APPROVED
```

Reviewer confirmed:

- conservative `target_branch` validation,
- no shell invocation for branch handling,
- Git execution routes through bounded helpers,
- no production broad staging,
- dirty preflight before branch switching,
- orphan initialization uses an empty tree and disables hooks,
- revert path remains isolated from branch preparation.

No review-requested code changes were required after the initial implementation commit.

## 6. Final Verification

Controller final verification before pushing the implementation commit:

```text
== gofmt check ==
PASS: no files listed by gofmt -l

== focused gitguard ==
PASS: go test ./internal/gitguard -run 'Test.*Branch|TestPrepareTargetBranch' -v

== focused pipe ==
PASS: go test ./internal/pipe -run 'TestRun.*Branch|TestRun.*Orphan' -v

== full go test ==
ok  github.com/camcamcami/BLK-System/cmd/blk-pipe
ok  github.com/camcamcami/BLK-System/internal/contracts
ok  github.com/camcamcami/BLK-System/internal/engine
ok  github.com/camcamcami/BLK-System/internal/execguard
ok  github.com/camcamcami/BLK-System/internal/gitguard
ok  github.com/camcamcami/BLK-System/internal/pipe
ok  github.com/camcamcami/BLK-System/internal/runtimeguard
ok  github.com/camcamcami/BLK-System/internal/testutil
ok  github.com/camcamcami/BLK-System/internal/validation

== go vet ==
PASS: go vet ./...

== direct git grep ==
PASS: no forbidden production exec.Command("git") outside internal/gitguard/command.go and internal/testutil/**

== broad staging grep ==
PASS: no production git add . / git add -u argv pattern

== diff checks ==
PASS: git diff --check
PASS: git diff --check HEAD^ HEAD
```

Implementation push evidence:

```text
To https://github.com/camcamcami/BLK-System.git
   45c1c7a..2d7582c  main -> main
## main...origin/main
2d7582c (HEAD -> main, origin/main) feat: add blk-pipe branch preparation
```

## 7. Deviations / Notes

- Sprint 002 chooses orphan initialization message `Initialize branch` to match the execution-sequence source segment, as planned.
- Empty `target_branch` continues to mean no branch preparation, preserving legacy execute payload behavior.
- No live Codex/LLM engine integration was added.
- No outcome or documentation changes were included in the implementation commit; this outcome document is committed separately.

## 8. Next Task

Next incomplete Sprint 002 task:

```text
Task 10 — Add Python Adapter Skeleton and Tests
```

Expected implementation commit from the plan:

```text
feat: add blk-pipe python adapter
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002_task-010-outcome.md
```
