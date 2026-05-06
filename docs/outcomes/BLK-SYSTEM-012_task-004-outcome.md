# BLK-System Sprint 012 — Task 4 Outcome

**Status:** Complete
**Date:** 2026-05-06
**Task:** Add Atomic Probe Lock and Parallel-Prevention Gates
**Sprint:** BLK-SYSTEM-012 — Workspace Isolation and Process-Control Implementation Probes
**Implementation Commit:** `8e5d61a test: add blk-test process lock probes`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Task 4 extends the BLK-SYSTEM-012 dependency-free Python probe module with atomic probe-lock inspection, acquisition, release, bounded wait decisions, stale/live lock handling, and single-run exclusion under test-owned temporary roots.

The implementation remains a deterministic local inert-probe layer only. It does not authorize live BLK-test MCP, does not authorize live MCP client/server startup, does not execute fixed-tool tests, does not mutate the primary repo from probe code, does not stage files from probe code, does not commit from probe code, does not authorize authoritative BEO publication, does not authorize RTM generation, and does not authorize RTM drift rejection authority.

---

## 2. Files Added/Changed

Modified:

- `python/blk_test_mcp_workspace_process_probes.py`
- `python/test_blk_test_mcp_workspace_process_probes.py`

Outcome document:

- `docs/outcomes/BLK-SYSTEM-012_task-004-outcome.md`

No documentation doctrine, Go code, live MCP server/client code, fixed BLK-test tool execution code, BEO publication code, RTM generation code, network code, shell execution code, or production sandbox code was added.

---

## 3. Behavior Implemented

### 3.1 Probe lock state inspection

Added:

```python
def probe_lock_state(
    lock_path,
    *,
    pid_alive=None,
) -> dict[str, object]:
```

The state probe inspects only root-anchored Sprint 012 lock files under a safe test-owned scratch root and `.blk-system-012-locks`. It returns deterministic evidence without killing arbitrary host PIDs. PID checks use liveness probing only (`os.kill(pid, 0)` through the default checker, or an injected test checker).

Key statuses include:

- `LOCK_ABSENT` for a safe, absent lock path;
- `LOCK_BLOCKED_UNOWNED` for unsafe, malformed, non-JSON, symlink, directory, non-Sprint, non-`PROBE_ONLY`, or otherwise unowned locks;
- `LOCK_BLOCKED_LIVE_PID` for owned locks whose PID is live;
- `STALE_LOCK_DETECTED` for owned locks whose PID is dead.

### 3.2 Atomic lock acquisition and bounded wait

Added:

```python
def acquire_probe_lock(
    lock_path,
    *,
    run_id: str,
    pid=None,
    max_wait_seconds: float = 0.0,
    poll_interval_seconds: float = 0.01,
    pid_alive=None,
) -> dict[str, object]:
```

Acquisition uses atomic exclusive file creation:

```python
os.open(lock_path_obj, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
```

Lock files are JSON and record at least:

```json
{
  "sprint": "BLK-SYSTEM-012",
  "authority": "PROBE_ONLY",
  "run_id": "...",
  "pid": 12345
}
```

Acquisition behavior:

- writes only Sprint 012 `PROBE_ONLY` JSON locks;
- rejects nested lock paths so acquisition and startup-purge discovery share the same direct-child `.blk-system-012-locks` surface;
- removes stale dead-PID JSON locks before acquiring;
- preserves live PID locks and returns `LOCK_BLOCKED_LIVE_PID` with bounded wait evidence;
- preserves malformed/unowned locks and returns `LOCK_BLOCKED_UNOWNED`;
- serializes cooperative in-process operations with `_LOCK_OPERATION_MUTEX`;
- rechecks stale lock identity before unlinking stale locks;
- returns `LOCK_ACQUIRED` only after exclusive creation succeeds.

### 3.3 Ownership-aware release

Added:

```python
def release_probe_lock(
    lock_path,
    *,
    run_id: str,
) -> dict[str, object]:
```

Release behavior:

- deletes only JSON locks whose `run_id` matches the releasing run;
- skips malformed, unowned, absent, unsafe, or different-owner locks with `LOCK_RELEASE_SKIPPED_NOT_OWNER`;
- rechecks JSON lock identity before unlinking;
- returns `LOCK_RELEASED` only for a verified same-run lock.

### 3.4 Teardown and startup purge hardening

Task 4 also hardened Task 3 lifecycle cleanup around lock ownership:

- terminal teardown removes JSON locks only when the lock run ID matches the workspace run ID derived from `.blk-system-012-workspaces/<run_id>/workspace`;
- terminal teardown preserves JSON locks owned by a different run;
- terminal teardown holds `_LOCK_OPERATION_MUTEX` and rechecks lock ownership before unlinking;
- startup purge now preserves owned workspace/cache paths when a matching live JSON/legacy lock exists;
- nested lock paths are rejected at acquisition so startup purge and acquisition cannot diverge on lock discovery.

### 3.5 Explicit scope limitation

Lock decisions include:

```text
filesystem_race_scope = COOPERATIVE_IN_PROCESS_ONLY
```

This is deliberate. Task 4 proves deterministic local cooperative probe behavior under test-owned temporary roots. It does not claim production sandbox/cgroup/VM enforcement, production host-secret isolation, or adversarial same-user filesystem lock-manager guarantees.

---

## 4. TDD Evidence

### 4.1 Initial RED — missing Task 4 APIs

The initial Task 4 tests were written before implementing the public APIs. The focused suite failed as expected against the pre-Task-4 module because the new lock APIs did not exist.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
```

RED evidence:

```text
FAILED (errors=15)
AttributeError: module 'blk_test_mcp_workspace_process_probes' has no attribute 'probe_lock_state'
AttributeError: module 'blk_test_mcp_workspace_process_probes' has no attribute 'acquire_probe_lock'
AttributeError: module 'blk_test_mcp_workspace_process_probes' has no attribute 'release_probe_lock'
```

### 4.2 Review-driven RED — race and ownership regressions

The first code-quality/safety review found real defects in the initial implementation. I added focused regressions before fixing them. The focused suite failed as expected.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
```

RED evidence after adding the first review-regression tests:

```text
FAILED (failures=2, errors=2)

test_release_rechecks_identity_before_unlinking ... ERROR
test_stale_lock_cleanup_rechecks_identity_before_unlinking ... FAIL
test_teardown_preserves_json_probe_lock_owned_by_different_run ... ERROR
test_live_json_lock_preserves_matching_workspace_and_cache ... FAIL
```

A later review found one remaining cooperative teardown race. I added another focused regression and verified RED:

```text
FAILED (errors=1)

test_teardown_rechecks_json_lock_identity_before_unlinking ... ERROR
FileNotFoundError: ... .blk-system-012-locks/first-run.lock
```

These RED gates proved the review findings before the fixes were implemented.

### 4.3 GREEN — focused Task 4 gate

After implementation and review-driven fixes, the focused workspace/process probe suite passed.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
```

Result:

```text
Ran 36 tests in 0.059s

OK
```

The focused GREEN gate covers Task 2 and Task 3 retained behavior plus Task 4 lock behavior:

- atomic `os.O_CREAT | os.O_EXCL` exclusive creation;
- stale dead-PID lock removal and acquisition;
- live PID lock preservation and bounded wait evidence;
- malformed/unowned lock fail-closed behavior;
- exactly one acquisition among concurrent attempts;
- non-owner release skip and owner release;
- release identity recheck before unlink;
- stale lock identity recheck before unlink;
- direct-child lock path guard;
- startup purge preserves matching live-run workspace/cache;
- terminal teardown removes same-run JSON locks;
- terminal teardown preserves different-run JSON locks;
- terminal teardown rechecks lock identity before unlink;
- second run can acquire only after terminal cleanup removes the first run lock.

---

## 5. Review Results

### 5.1 Spec compliance review

Final result: `PASS`

Reviewer summary:

```text
PASS
```

Final spec review confirmed that Task 4 required APIs, statuses, JSON lock fields, direct-file scope, stale/live/unowned behavior, bounded wait behavior, terminal teardown behavior, and review-driven regressions are present and passing.

### 5.2 Code quality and safety review

Final result: `APPROVED`

Reviewer summary:

```text
APPROVED

No blocking code quality or safety findings in the scoped deterministic local inert-probe context.
Teardown lock cleanup now holds _LOCK_OPERATION_MUTEX and rechecks ownership before unlinking.
Direct-child lock acquisition guard and startup purge direct-child discovery remain aligned.
No shell/eval/exec/os.system/subprocess/network/Git command/library usage found in the reviewed code/tests.
Only PID probing found is the intended os.kill(pid, 0) liveness check.
Scope claims remain appropriately limited: probe-only, non-authority, no production sandbox/adversarial FS-manager claim.
```

### 5.3 Notable review fixes

The code-quality review caught multiple meaningful landmines before push:

1. stale lock removal could delete a fresh replacement lock after a check-then-unlink interleaving;
2. release could delete a fresh replacement lock after an owner check;
3. teardown could delete a JSON lock owned by another run;
4. startup purge could remove live-run workspace/cache paths if a matching live lock existed;
5. nested lock paths made acquisition and startup-purge discovery surfaces diverge;
6. teardown still needed an in-process cooperative recheck before lock unlink.

All were fixed with focused regression tests before final push.

---

## 6. Final Verification

Final verification was rerun after the amended implementation commit.

Commands:

```bash
export PATH="$HOME/.local/bin:$PATH"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check HEAD^ HEAD
rm -rf python/__pycache__
git status --short --branch
```

Verification result:

```text
Ran 36 tests in 0.059s
OK

Ran 190 tests in 0.738s
OK

ok  github.com/camcamcami/BLK-System/cmd/blk-pipe
ok  github.com/camcamcami/BLK-System/internal/contracts
ok  github.com/camcamcami/BLK-System/internal/engine
ok  github.com/camcamcami/BLK-System/internal/execguard
ok  github.com/camcamcami/BLK-System/internal/gitguard
ok  github.com/camcamcami/BLK-System/internal/pipe
ok  github.com/camcamcami/BLK-System/internal/runtimeguard
ok  github.com/camcamcami/BLK-System/internal/testutil
ok  github.com/camcamcami/BLK-System/internal/validation

go vet ./...: PASS
git diff --check HEAD^ HEAD: PASS
python/__pycache__ removed
status: ## main...origin/main [ahead 1]
```

Implementation push:

```text
8e5d61a test: add blk-test process lock probes
Remote: pushed to origin/main
```

---

## 7. Explicit Non-Authority Statement

BLK-SYSTEM-012 Task 4 is a deterministic local probe task only. It does not authorize live BLK-test MCP, does not authorize live MCP client/server startup, does not execute fixed-tool tests, does not mutate primary repo from probe code, does not stage files from probe code, does not commit from probe code, does not authorize authoritative BEO publication, does not authorize RTM generation, does not authorize RTM drift rejection authority, does not read protected BLK-req vault bodies, does not claim production sandbox/cgroup/VM enforcement, and does not claim production host-secret isolation.

Sprint 013 owns approval/source-evidence authorization mechanics. Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke.

---

## 8. Deviations / Notes

- The implementation uses Python standard library only.
- The lock implementation is intentionally scoped as `COOPERATIVE_IN_PROCESS_ONLY`; it is not a production adversarial filesystem lock manager.
- Lock path acceptance is direct-child only under `.blk-system-012-locks` to keep acquisition, startup purge, and teardown surfaces aligned.
- Outcome-document policy follows the updated user instruction: outcome docs are committed and pushed after each task, not deferred until sprint closeout.
- No Hindsight tools were used.

---

## 9. Next Task

Task 5 — Prove Fixed Inert Process Timeout, Output Flood, and Process-Tree Kill Path.

Task 5 should extend `python/blk_test_mcp_workspace_process_probes.py` and `python/test_blk_test_mcp_workspace_process_probes.py` with hardcoded fixed inert process probes only, covering `exit_zero`, `exit_nonzero`, `timeout`, `output_flood`, and `descendant_timeout`, with one shared awaited kill path for timeout and output flood.
