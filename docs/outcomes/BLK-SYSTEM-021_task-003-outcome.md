# BLK-SYSTEM-021 — Task 003 Outcome

**Status:** Complete — subprocess environment and report preservation hardened
**Date:** 2026-05-07T21:24:00+10:00
**Plan:** `docs/plans/blk-system-021_python-adapter-policy-layer-hardening.md`

---

## 1. Summary

Task 003 hardened `python/blk_pipe_adapter.py` subprocess invocation by adding a scrubbed environment helper and preserving Go report evidence for success and non-success reports.

The adapter remains shell-free: subprocess invocation still uses `[self.binary_path, "--payload", temp_payload_path]`.

---

## 2. Files Changed

```text
python/blk_pipe_adapter.py
python/test_blk_pipe_adapter.py
docs/outcomes/BLK-SYSTEM-021_task-003-outcome.md
```

---

## 3. RED Evidence

Focused RED command after adding Task 003 tests:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_pipe_adapter -v
```

Observed RED:

```text
test_invoke_binary_scrubs_high_risk_ssh_environment_and_sets_pwd ... ERROR
KeyError: 'env'
Ran 32 tests in 0.482s
FAILED (errors=1)
```

Root cause: `_invoke_binary` did not pass an explicit `env` keyword to `subprocess.run`, so tests could not prove high-risk SSH/askpass variables were scrubbed or that `PWD` was audit-bound to the payload work directory.

---

## 4. GREEN Evidence

Focused command:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_pipe_adapter -v
```

Observed result:

```text
Ran 32 tests in 0.479s
OK
```

Shared verification commands:

```bash
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
```

Observed summary:

```text
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	7.341s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validationprofiles	(cached)
Ran 326 tests in 6.402s
OK
```

---

## 5. Implemented Behavior

- Added `_build_subprocess_env(work_dir: str | None = None)`.
- Scrubbed:
  - `SSH_AUTH_SOCK`
  - `SSH_AGENT_PID`
  - `SSH_ASKPASS`
- Set `PWD` to payload `work_dir` when available for audit clarity.
- Preserved shell-free subprocess invocation.
- Added tests proving raw Go report preservation for non-success reports, including:
  - `raw_report`
  - `stderr`
  - `trace_artifacts`
  - `validation_profiles`
  - `resolved_validation_commands`
  - `staged_files`
  - `destroyed_files`

---

## 6. Non-Execution Statement

Task 003 did not invoke Hindsight, Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads/copying/parsing/hashing/mutation, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, or source mutation outside exact approved allowlists.

---

## 7. No-Authority-Expansion Statement

Environment scrubbing reduces subprocess invocation risk but is not a production sandbox, cgroup, VM, network, or host-secret isolation claim. Go `blk-pipe` remains the final enforcement authority and report evidence source.
