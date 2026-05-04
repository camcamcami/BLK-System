# BLK-pipe Sprint 006 — Task 1 Outcome

**Status:** Complete
**Date:** 2026-05-05
**Task:** Make Approved `codex-live` Decisions Non-Executable
**Commit:** `555a872 fix: fail closed approved blk-pipe live profile`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Remediate the Sprint 005 hostile-review blocker where exact-token `codex-live` returned `APPROVED_BUT_NOT_EXECUTED` while also exposing `allowed=True`.

Task 1 tightens the approval-gate contract so `allowed` means executable now. Exact-token `codex-live` approval validation is now audit-only: it records that the approval token matched, but it does not authorize execution.

This task did not run or implement live Codex, live tactical LLM calls, network model services, cyber tooling, live BLK-test MCP, RTM generation, or authoritative BEO publication.

---

## 2. Files Added/Changed

Modified:

- `python/blk_orchestrator_gate.py`
- `python/test_blk_orchestrator_gate.py`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`
- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md`
- `README.md`

Added:

- `docs/outcomes/BLK-PIPE-006_task-001-outcome.md`

---

## 3. Behavior Implemented

### 3.1 Runtime profile semantics

`ProfileDecision` now includes an explicit audit field:

```python
approval_recorded: bool = False
```

The semantics are now split cleanly:

- `allowed` means the profile is executable now.
- `approval_recorded` means the exact `codex-live` approval token matched and was recorded as audit evidence.
- `live_execution_authorized` remains separate and stays `False` for all current paths.

Current profile behavior after Task 1:

| Profile / condition | Decision | `allowed` | `approval_recorded` | `live_execution_authorized` |
| --- | --- | --- | --- | --- |
| `dev-smoke` | `ALLOWED_LOCAL_ONLY` | `True` | `False` | `False` |
| `strict-ci` | `ALLOWED_LOCAL_ONLY` | `True` | `False` | `False` |
| `codex-dry-run` | `ALLOWED_LOCAL_ONLY` | `True` | `False` | `False` |
| `codex-live` without token | `BLOCKED_APPROVAL_REQUIRED` | `False` | `False` | `False` |
| `codex-live` with mismatched token | `BLOCKED_APPROVAL_MISMATCH` | `False` | `False` | `False` |
| `codex-live` with exact token | `APPROVED_BUT_NOT_EXECUTED` | `False` | `True` | `False` |
| `cyber-execution` | `BLOCKED_CYBER_EXECUTION` | `False` | `False` | `False` |
| unknown profile | `BLOCKED_UNKNOWN_PROFILE` | `False` | `False` | `False` |

### 3.2 Documentation updates

`docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md` now states that:

- `ProfileDecision.allowed` means executable now,
- `APPROVED_BUT_NOT_EXECUTED` is not allowed to execute,
- exact-token `codex-live` validation records `approval_recorded=True`,
- `allowed=False` and `live_execution_authorized=False` remain in force,
- approval-token validation is audit-only until a future sprint explicitly authorizes a live execution path.

`docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md` and `README.md` were updated so their capability-profile summaries no longer imply that exact-token `codex-live` is executable.

---

## 4. TDD Evidence

### 4.1 RED

Before production changes, the new focused regression test failed on the hostile-review bug:

```text
test_codex_live_exact_token_records_approval_but_is_not_allowed ... FAIL

AssertionError: True is not false

Ran 10 tests in 0.001s
FAILED (failures=1)
```

The failing assertion proved that the previous exact-token `codex-live` path still returned `allowed=True`.

### 4.2 GREEN

After implementation, the focused test suite passed:

```text
python3 -m unittest discover -s python -p 'test_blk_orchestrator_gate.py' -v
Ran 11 tests in 0.001s
OK
```

The explicit approval-semantics probe also passed:

```text
approval semantics probe PASS
```

Full Python suite after implementation:

```text
python3 -m unittest discover -s python -p 'test_*.py'
Ran 70 tests in 0.666s
OK
```

---

## 5. Review Results

Sprint 006 review gates for this task were deterministic local gates. No live Codex, live BLK-test MCP, cyber tooling, RTM generation, or authoritative BEO publication was used.

### 5.1 Spec / traceability gate

Passed. The gate verified:

- `dev-smoke`, `strict-ci`, and `codex-dry-run` still return `ALLOWED_LOCAL_ONLY` with `allowed=True` and no live authorization,
- `codex-live` without token still returns `BLOCKED_APPROVAL_REQUIRED` with `allowed=False`,
- `codex-live` with mismatched token still returns `BLOCKED_APPROVAL_MISMATCH` with `allowed=False`,
- exact-token `codex-live` returns `APPROVED_BUT_NOT_EXECUTED` with `allowed=False`, `approval_recorded=True`, and `live_execution_authorized=False`,
- `cyber-execution` remains blocked regardless of token,
- unknown profiles remain blocked,
- BLK-015 states that `allowed` means executable now,
- BLK-015 states approval-token validation is audit-only until a future sprint authorizes live execution,
- BLK-012 and README summarize the Sprint 006 audit-only approval semantics.

Result:

```text
spec gate: profile decisions PASS
spec gate: docs traceability PASS
```

### 5.2 Safety / docs-quality gate

Passed. The gate verified:

- runtime code did not import or call live-execution surfaces such as sockets, subprocesses, HTTP clients, or model SDKs,
- touched Markdown fences are balanced,
- touched files have final newlines,
- touched lines have no trailing whitespace,
- `git diff --check HEAD^ HEAD` passed.

Result:

```text
safety gate: runtime no live-execution surfaces PASS
safety gate: file hygiene PASS
```

---

## 6. Final Verification

Final verification before push passed:

```text
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check HEAD^ HEAD
git status --short --branch
git log --oneline --decorate -4
git push origin main
git status --short --branch
```

Observed key results:

```text
Ran 70 tests in 0.650s
OK
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	6.785s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)
555a872 (HEAD -> main) fix: fail closed approved blk-pipe live profile
To https://github.com/camcamcami/BLK-System.git
   821f0c1..555a872  main -> main
```

After cleanup of Python test cache files, repository status returned to clean/aligned:

```text
## main...origin/main
```

---

## 7. Deviations / Notes

- The hostile-review blocker is closed for Task 1: exact-token `codex-live` no longer exposes `allowed=True`.
- `approval_recorded=True` is intentionally limited to the exact-token `APPROVED_BUT_NOT_EXECUTED` path.
- The task intentionally did not rename `allowed`; tests and docs now pin its meaning as executable now.
- BLK-test MCP strings that still mention Sprint 005 remain part of later Sprint 006 remediation scope, not Task 1.
- No Hindsight was used.

---

## 8. Next Task

BLK-PIPE-006 Task 2 should require canonical `trace_artifacts[*].version_hash` values in Go and Python fixture contracts without reading or verifying active BLK-req vault files.
