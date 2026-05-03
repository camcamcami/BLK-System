# BLK-pipe Sprint 002.2 — Task 1 Outcome

**Status:** Complete
**Date:** 2026-05-04
**Task:** Reap Escaped Descendants on Timeout, Flood, and Context Cancel
**Implementation Commit:** `e991515 fix: reap blk-pipe escaped descendants before return`
**Remote:** pushed to `origin/main`
**Plan:** `docs/plans/BLK-PIPE-002.2_cyber-readiness-remediation.md`

---

## 1. Objective

Task 1 closed the hostile-review finding that an escaped descendant could survive BLK-pipe timeout/flood/cancel handling and mutate the repository after BLK-pipe returned.

The required behavior is now enforced for BLK-pipe-owned process groups, visible descendants, inherited-output pipe holders, and visible descendants of those pipe holders. This remains POSIX process cleanup, not a full sandbox or arbitrary detached-daemon containment guarantee.

---

## 2. Files Changed

Implementation commit:

```text
e991515 fix: reap blk-pipe escaped descendants before return
 internal/execguard/command.go      |  68 ++++--
 internal/execguard/command_test.go | 440 ++++++++++++++++++++++++++++++++++++-
 internal/pipe/run_test.go          | 102 +++++++++
 3 files changed, 594 insertions(+), 16 deletions(-)
```

Changed files:

- `internal/execguard/command.go`
- `internal/execguard/command_test.go`
- `internal/pipe/run_test.go`

---

## 3. Behavior Implemented

### 3.1 Scoped active cleanup

`execguard.Run` now performs scoped cleanup for its own active command on timeout, output flood, and context cancellation before unregistering and returning.

The fix preserves the existing global fatal cleanup path through `KillActiveProcessGroups()`, but ordinary per-command timeout/flood/cancel cleanup no longer kills every command in the global active registry.

### 3.2 Redirected escaped descendant coverage

The hostile redirected shape is now covered:

```text
setsid sh -c 'sleep 1; printf late > late.txt' >/dev/null 2>&1 & sleep 10
```

This matters because a redirected child does not keep inherited stdout/stderr pipe file descriptors open, so pipe-holder discovery alone is insufficient.

### 3.3 Concurrent command safety

A new regression verifies that one command timing out, flooding, or being cancelled does not kill an unrelated concurrent `execguard.Run`.

---

## 4. TDD Evidence

### 4.1 RED

The implementation subagent first added failing hostile tests. Initial failures included:

```text
TestRunTimeoutReapsEscapedDescendantBeforeReturn: late.txt appeared after return
TestRunOutputFloodReapsEscapedDescendantBeforeReturn: late.txt appeared after return
TestRunContextCancelReapsEscapedDescendantBeforeReturn: late.txt appeared after return
TestRunTimeoutEscapedDescendantCannotMutateAfterReturn: late.txt appeared after pipe return
```

First review then found an uncovered redirected descendant case and an overbroad global cleanup issue. Fix RED coverage added the exact redirected `setsid ... >/dev/null 2>&1` shape and a concurrent-run safety regression.

### 4.2 GREEN

Final focused verification passed:

```text
go test ./internal/execguard -run 'TestRun.*EscapedDescendant.*BeforeReturn|TestRun.*DoesNotKillUnrelated|TestKillActive|TestActiveCleanup|TestRegistry' -v
PASS

go test -race ./internal/execguard
PASS

go test ./internal/engine -v
PASS

go test ./internal/pipe -run 'TestRun.*Timeout.*Escaped|TestRun.*OutputFlood|TestRun.*EngineTimeout' -v
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

Task 1 used the required two-stage review loop.

### 5.1 First review gate

Spec review initially found that the implementation did not cover redirected escaped descendants that do not hold inherited output pipes. Code-quality review initially found per-command cleanup was using the global active registry and could kill unrelated concurrent `Run` calls.

Both findings were fixed before push.

### 5.2 Final spec-compliance review

Final result:

```text
PASS
```

The reviewer confirmed:

- exact redirected escaped descendant shape is covered,
- scoped cleanup includes root/visible descendants while `directLive` is true,
- cleanup occurs before unregister/return on timeout, flood, and cancel paths,
- Darwin limitation is documented,
- full tests and safety greps pass.

### 5.3 Final code-quality/security review

Final result:

```text
APPROVED
```

The reviewer confirmed:

- per-command cleanup is scoped to the current active command,
- global fatal cleanup remains global,
- unrelated concurrent `Run` calls survive scoped timeout/flood/cancel cleanup,
- race and focused test suites pass,
- bounded return behavior is preserved.

---

## 6. Final Verification Evidence

Controller verification before push:

```text
gofmt -l internal/execguard/command.go internal/execguard/command_test.go internal/pipe/run_test.go
# no output

go test ./internal/execguard -run 'TestRun.*EscapedDescendant.*BeforeReturn|TestRun.*DoesNotKillUnrelated|TestKillActive|TestActiveCleanup|TestRegistry' -v
PASS

go test -race ./internal/execguard
PASS

go test ./internal/engine -v
PASS

go test ./internal/pipe -run 'TestRun.*Timeout.*Escaped|TestRun.*OutputFlood|TestRun.*EngineTimeout' -v
PASS

go test ./...
PASS

go vet ./...
PASS

git diff --check
PASS

git push origin main
origin/main updated to e991515
```

Post-push status:

```text
## main...origin/main
e991515 (HEAD -> main, origin/main) fix: reap blk-pipe escaped descendants before return
```

---

## 7. Safety Invariants Preserved

- No production `git add .`.
- No production `git add -u`.
- No live Codex or live LLM integration.
- No offensive cyber behavior.
- BLK-pipe still does not claim full sandbox containment.
- Global fatal-system cleanup remains available for fatal signal/panic handling.
- Per-command timeout/flood/cancel cleanup is scoped to the current command.

---

## 8. Deviations / Notes

The final implementation is stricter than the first attempted fix because review caught a real kill-targeting usability hazard: ordinary timeout cleanup must not kill unrelated active `execguard.Run` calls.

Task 1 closes the known post-return mutation risk for discoverable BLK-pipe-owned process trees and Linux pipe-holder/visible-descendant cases. Full daemon containment remains deferred to a future sandbox/capability-profile sprint.

---

## 9. Next Task

Proceed to Sprint 002.2 Task 2: enforce read-only validation semantics so validation commands cannot create or alter the committed diff.
