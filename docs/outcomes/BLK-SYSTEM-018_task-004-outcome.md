# BLK-SYSTEM-018 — Task 004 Outcome

**Task:** Task 4 — Make Revert Reachable Before Execute-Mode Clean Preflight
**Status:** Complete
**Date:** 2026-05-07T17:50:21+10:00
**Repository:** `/home/dad/BLK-System`
**Task 3 RED commit:** `2edbd15 test: expose revert preflight reachability gap`

---

## 1. Objective

Task 004 patched BLK-pipe run ordering so valid `Action == "revert"` payloads reach the verified emergency reset/clean path before execute-mode clean preflight rejects dirty workspace residue.

The change preserves target branch, target hash, full-object-ID, and ancestry validation inside `runRevert(...)` before any destructive reset/clean operation.

---

## 2. Files Changed

```text
internal/pipe/run.go
docs/outcomes/BLK-SYSTEM-018_task-004-outcome.md
```

`internal/pipe/run_test.go` carried the Task 003 RED tests and required no additional production-fix adjustment in Task 004.

---

## 3. Behavior Implemented

`internal/pipe/run.go` now branches to `runRevert(...)` immediately after `parseAndValidatePayload(...)` succeeds:

```text
parse and validate payload
if payload.Action == "revert" -> runRevert(...)
else -> execute-mode cleanPreflight(...)
```

This means execute-mode clean preflight remains unchanged for non-revert payloads, while revert payloads use the dedicated emergency path:

1. verify `target_branch` if supplied,
2. verify `target_hash` resolves exactly to a full commit object ID in the repository,
3. verify `target_hash` is an ancestor of `HEAD`,
4. reset hard to the verified target,
5. run `git clean -ffdx -q`,
6. verify the workspace is clean before reporting `SUCCESS`.

---

## 4. TDD Evidence

### 4.1 RED Reference

Task 003 captured the expected failure: dirty tracked, untracked, ignored, empty-directory, and nested `.git` residue all returned `GIT_DIRTY` / Exit 7 before the revert path could run.

### 4.2 GREEN Focused Test

Command:

```text
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestRunRevert(BypassesCleanPreflight|CleansPreExistingNestedGitRepository|InvalidAnchor|WithTargetBranch|SHA256)' -count=1 -v
```

Output:

```text
=== RUN   TestRunRevertWithTargetBranchRejectsWrongCurrentBranch
--- PASS: TestRunRevertWithTargetBranchRejectsWrongCurrentBranch (0.03s)
=== RUN   TestRunRevertWithTargetBranchAcceptsMatchingCurrentBranch
--- PASS: TestRunRevertWithTargetBranchAcceptsMatchingCurrentBranch (0.03s)
=== RUN   TestRunRevertSHA256RejectsAbbreviatedFortyHexTarget
--- PASS: TestRunRevertSHA256RejectsAbbreviatedFortyHexTarget (0.02s)
=== RUN   TestRunRevertSHA256AcceptsFullSixtyFourHexTarget
--- PASS: TestRunRevertSHA256AcceptsFullSixtyFourHexTarget (0.03s)
=== RUN   TestRunRevertCleansPreExistingNestedGitRepositoryAfterValidAnchor
--- PASS: TestRunRevertCleansPreExistingNestedGitRepositoryAfterValidAnchor (0.04s)
=== RUN   TestRunRevertInvalidAnchorDoesNotReset
--- PASS: TestRunRevertInvalidAnchorDoesNotReset (0.03s)
=== RUN   TestRunRevertBypassesCleanPreflightForEmptyUntrackedDirectory
--- PASS: TestRunRevertBypassesCleanPreflightForEmptyUntrackedDirectory (0.03s)
=== RUN   TestRunRevertBypassesCleanPreflightForDirtyTrackedWorkspace
--- PASS: TestRunRevertBypassesCleanPreflightForDirtyTrackedWorkspace (0.02s)
=== RUN   TestRunRevertBypassesCleanPreflightForUntrackedAndIgnoredResidue
=== RUN   TestRunRevertBypassesCleanPreflightForUntrackedAndIgnoredResidue/untracked
=== RUN   TestRunRevertBypassesCleanPreflightForUntrackedAndIgnoredResidue/ignored
--- PASS: TestRunRevertBypassesCleanPreflightForUntrackedAndIgnoredResidue (0.05s)
PASS
ok  	github.com/camcamcami/BLK-System/internal/pipe	0.286s
```

### 4.3 Regression Command

```text
go test ./internal/pipe -count=1
ok  	github.com/camcamcami/BLK-System/internal/pipe	6.962s
```

---

## 5. Shared Verification

Command block:

```text
export PATH="$HOME/.local/bin:$PATH"
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

Output:

```text
Ran 310 tests in 6.749s
OK

ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	0.035s
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	8.708s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)

go vet ./...
exit 0, no output

git diff --check
exit 0, no output
```

---

## 6. Review Notes

- Invalid anchors remain protected: the focused gate reran `TestRunRevertInvalidAnchorDoesNotReset`, SHA-256 abbreviation rejection, and target-branch mismatch tests.
- Execute-mode clean preflight remains unchanged because only the `revert` branch moved before `cleanPreflight(...)`.
- Nested `.git` residue is remediated, not deferred: valid revert removes it through `reset --hard` plus `git clean -ffdx -q` after target validation.

---

## 7. Non-Execution Statement

Task 004 did not invoke Codex or live tactical LLMs, did not call network model services, did not run cyber tooling, did not start production BLK-test MCP, did not read or mutate protected BLK-req vault bodies, did not generate RTM, did not assert RTM drift rejection authority, and did not publish authoritative BEOs.

---

## 8. Next Task

Task 005 adds persistent doctrine gates and active doctrine cross-references for the Sprint 018 authority boundaries.
