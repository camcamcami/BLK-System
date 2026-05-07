# BLK-SYSTEM-018 — Task 003 Outcome

**Task:** Task 3 — Add RED Tests for Revert Reachability from Dirty Workspaces
**Status:** Complete — RED revert reachability gap exposed
**Date:** 2026-05-07T17:48:17+10:00
**Repository:** `/home/dad/BLK-System`
**Source finding:** `BLOCKING-2` in `docs/reviews/BLK-SYSTEM_current-implementation_BLK-001-through-BLK-006_hostile-alignment-review.md`

---

## 1. Objective

Task 003 converted existing revert preflight-preservation tests into the Sprint 018 target behavior: a valid emergency `revert` payload must reach target hash verification and reset/clean even when the workspace contains dirty tracked changes, untracked files, ignored files, empty untracked directories, or nested `.git` residue.

This task intentionally changed only tests and documentation. It did not patch production run ordering.

---

## 2. Files Changed

```text
internal/pipe/run_test.go
docs/outcomes/BLK-SYSTEM-018_task-003-outcome.md
```

---

## 3. Tests Added / Changed

`internal/pipe/run_test.go` now contains Sprint 018 revert reachability expectations:

```text
TestRunRevertBypassesCleanPreflightForDirtyTrackedWorkspace
TestRunRevertBypassesCleanPreflightForUntrackedAndIgnoredResidue
TestRunRevertBypassesCleanPreflightForEmptyUntrackedDirectory
TestRunRevertCleansPreExistingNestedGitRepositoryAfterValidAnchor
```

The nested `.git` behavior is intentionally remediated rather than deferred. This follows the hostile review finding and the sprint plan's strict branch: valid emergency revert should clean nested `.git` residue through the already hardened reset/clean path after target hash/ancestry validation.

---

## 4. RED Evidence

Command:

```text
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestRunRevert(BypassesCleanPreflight|CleansPreExistingNestedGitRepository)' -count=1 -v
```

Observed RED failure excerpt:

```text
=== RUN   TestRunRevertCleansPreExistingNestedGitRepositoryAfterValidAnchor
    run_test.go:846: exit code = 7, want 0; report={Status:GIT_DIRTY ExitCode:7 ... Error:git worktree has pre-existing untracked or ignored files:
        vendor/sub/.git/}
--- FAIL: TestRunRevertCleansPreExistingNestedGitRepositoryAfterValidAnchor
=== RUN   TestRunRevertBypassesCleanPreflightForEmptyUntrackedDirectory
    run_test.go:913: exit code = 7, want 0; report={Status:GIT_DIRTY ExitCode:7 ... Error:git worktree has pre-existing untracked or ignored files:
        scratch/empty/}
--- FAIL: TestRunRevertBypassesCleanPreflightForEmptyUntrackedDirectory
=== RUN   TestRunRevertBypassesCleanPreflightForDirtyTrackedWorkspace
    run_test.go:945: exit code = 7, want 0; report={Status:GIT_DIRTY ExitCode:7 ... Error:git worktree is dirty:
         M README.md
        }
--- FAIL: TestRunRevertBypassesCleanPreflightForDirtyTrackedWorkspace
=== RUN   TestRunRevertBypassesCleanPreflightForUntrackedAndIgnoredResidue/untracked
    run_test.go:1003: exit code = 7, want 0; report={Status:GIT_DIRTY ExitCode:7 ... Error:git worktree is dirty:
        ?? scratch.txt
        }
=== RUN   TestRunRevertBypassesCleanPreflightForUntrackedAndIgnoredResidue/ignored
    run_test.go:1003: exit code = 7, want 0; report={Status:GIT_DIRTY ExitCode:7 ... Error:git worktree has pre-existing untracked or ignored files:
        keep.cache}
--- FAIL: TestRunRevertBypassesCleanPreflightForUntrackedAndIgnoredResidue
FAIL
```

This is the expected RED: current `run(...)` calls execute-mode `cleanPreflight(...)` before `runRevert(...)`, returning `GIT_DIRTY` / Exit 7 before the verified revert path can run.

---

## 5. Verification

```text
gofmt -w internal/pipe/run_test.go
git diff --check
exit 0, no output
```

Full shared verification is intentionally deferred to Task 004 because Task 003 commits RED tests that are expected to fail until the production ordering fix lands.

---

## 6. Non-Execution Statement

Task 003 did not invoke Codex or live tactical LLMs, did not call network model services, did not run cyber tooling, did not start production BLK-test MCP, did not read or mutate protected BLK-req vault bodies, did not generate RTM, did not assert RTM drift rejection authority, and did not publish authoritative BEOs.

---

## 7. Next Task

Task 004 moves the `Action == "revert"` branch before execute-mode clean preflight while preserving target branch/hash/ancestry validation and invalid-anchor protections.
