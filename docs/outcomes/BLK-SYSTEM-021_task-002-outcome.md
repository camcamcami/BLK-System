# BLK-SYSTEM-021 — Task 002 Outcome

**Status:** Complete — adapter payload policy preflight implemented
**Date:** 2026-05-07T21:18:00+10:00
**Plan:** `docs/plans/blk-system-021_python-adapter-policy-layer-hardening.md`

---

## 1. Summary

Task 002 implemented Python adapter execute-payload preflight helpers in `python/blk_pipe_adapter.py` and adjusted adapter tests so valid execute calls carry canonical `trace_artifacts`.

The adapter now rejects common malformed execute payloads before writing a temporary payload file or invoking `blk-pipe`, while preserving Go `blk-pipe` as the final enforcement authority.

---

## 2. Files Changed

```text
python/blk_pipe_adapter.py
python/test_blk_pipe_adapter.py
docs/outcomes/BLK-SYSTEM-021_task-002-outcome.md
```

---

## 3. RED Evidence From Task 001

Task 001 RED command:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_pipe_adapter -v
```

Observed RED summary:

```text
Ran 30 tests in 0.879s
FAILED (failures=23)
```

Representative missing behaviors were `ValueError not raised` for malformed `trace_artifacts`, non-absolute `work_dir`, empty execute fields, invalid `validation_profiles`, and protected BLK-req allowlist paths.

---

## 4. GREEN Evidence

Focused command:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_pipe_adapter -v
```

Observed result:

```text
Ran 30 tests in 0.476s
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
ok  	github.com/camcamcami/BLK-System/internal/pipe	7.416s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validationprofiles	(cached)
Ran 324 tests in 6.395s
OK
```

---

## 5. Implemented Policy Surface

- Execute payloads require non-empty canonical `trace_artifacts`.
- `trace_artifacts.version_hash` must match `sha256:<64-lowercase-hex>`.
- `work_dir` must be absolute.
- `beb_id`, `target_branch`, `engine`, and `l2_packet` must be non-empty strings.
- `allowed_modified_files` and `allowed_new_files` must be relative non-traversing paths.
- Protected BLK-req prefixes are rejected early:
  - `docs/active/`
  - `docs/requirements/`
  - `docs/use_cases/`
- `validation_profiles` must be non-empty strings without duplicates.
- `validation_commands` must be non-empty strings when used as trusted-local compatibility.
- Revert payloads remain separate and are not forced to provide execute-only trace/profile/L2 fields.

---

## 6. Non-Execution Statement

Task 002 did not invoke Hindsight, Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads/copying/parsing/hashing/mutation, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, or source mutation outside exact approved allowlists.

---

## 7. No-Authority-Expansion Statement

The implemented Python checks are fail-fast convenience only. They reduce operator/orchestrator mistakes before subprocess invocation but do not replace Go `blk-pipe` payload validation, protected-path classification, validation-profile resolution, execution, cleanup, or report authority.
