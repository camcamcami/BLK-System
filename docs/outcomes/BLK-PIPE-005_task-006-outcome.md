# BLK-pipe Sprint 005 — Task 6 Outcome

**Status:** Complete
**Date:** 2026-05-05
**Task:** Define Fail-Closed Approval Gate and Disabled BLK-test MCP Design Stubs
**Commit:** `5d61359 feat: define fail-closed blk-pipe approval gate`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Implement deterministic contract surfaces required before any future live integration is considered:

- a fail-closed approval/profile gate for `dev-smoke`, `strict-ci`, `codex-dry-run`, `codex-live`, and `cyber-execution`, and
- disabled-by-default BLK-test MCP request/response design stubs.

Task 6 explicitly did not run Codex, live tactical LLMs, network model services, cyber tooling, or live BLK-test MCP. It did not generate RTM artifacts or publish authoritative BEOs.

---

## 2. Files Added/Changed

Added:

- `python/blk_orchestrator_gate.py`
- `python/test_blk_orchestrator_gate.py`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`

Modified:

- `README.md`
- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`

---

## 3. Behavior Implemented

### 3.1 Profile gate

`python/blk_orchestrator_gate.py` now exposes:

- `ProfileDecision`
- `evaluate_profile_gate(...)`
- `approval_token_for(...)`

Profile behavior:

- `dev-smoke`, `strict-ci`, and `codex-dry-run` return `ALLOWED_LOCAL_ONLY` with `live_execution_authorized=False`.
- `codex-live` without a token returns `BLOCKED_APPROVAL_REQUIRED`.
- `codex-live` with a mismatched token returns `BLOCKED_APPROVAL_MISMATCH`.
- `codex-live` with the exact token returns `APPROVED_BUT_NOT_EXECUTED`; Sprint 005 still does not authorize or perform live Codex execution.
- `cyber-execution` returns `BLOCKED_CYBER_EXECUTION` regardless of token.
- Unknown profiles fail closed as `BLOCKED_UNKNOWN_PROFILE`.

The approval token shape is deterministic:

```text
BLK_APPROVE_CODEX_LIVE beb_id=<BEB_ID> target_branch=<branch> trace_hash=<sha256:64-lowercase-hex>
```

### 3.2 Disabled BLK-test MCP stubs

`python/blk_orchestrator_gate.py` now exposes:

- `build_blk_test_mcp_request(source_report, enabled=False)`
- `send_blk_test_mcp_request(request, enabled=False)`
- `map_blk_test_mcp_response(response)`

The request builder returns a disabled design object by default and records:

- source status,
- `beb_id`,
- commit/pre-engine evidence,
- staged/destroyed files,
- opaque `trace_artifacts`,
- `rtm_status: NOT_GENERATED`,
- `beo_publication: DRAFT_ONLY`.

Passing `enabled=True` raises instead of creating or sending a live request. The send stub returns `BLOCKED` with `network_called: False` and `subprocess_called: False`.

Future BLK-test MCP response mapping accepts only `PASS`, `FAIL`, and `BLOCKED`; unknown statuses reject deterministically.

### 3.3 Documentation

`docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md` defines the new contract. BLK-012, BLK-013, BLK-014, and README now link or summarize the Sprint 005 approval/MCP design boundary.

---

## 4. TDD Evidence

### 4.1 RED

Before implementation, the new focused test file failed because the module did not exist:

```text
test_blk_orchestrator_gate (unittest.loader._FailedTest.test_blk_orchestrator_gate) ... ERROR
ModuleNotFoundError: No module named 'blk_orchestrator_gate'
FAILED (errors=1)
```

### 4.2 GREEN

After implementation:

```text
python3 -m unittest discover -s python -p 'test_blk_orchestrator_gate.py' -v
Ran 10 tests in 0.001s
OK
```

Full Python suite:

```text
python3 -m unittest discover -s python -p 'test_*.py'
Ran 69 tests in 0.649s
OK
```

---

## 5. Review Results

Live tactical LLM/reviewer agents were forbidden for this sprint, so Task 6 used deterministic local review gates.

### 5.1 Spec / traceability gate

Passed. The gate verified:

- required profile decision names exist in runtime code,
- required Task 6 tests exist,
- BLK-015 documents the approval-token shape,
- BLK-015 documents `APPROVED_BUT_NOT_EXECUTED`,
- BLK-015 documents the disabled BLK-test MCP path,
- README links BLK-015.

Result:

```text
spec/traceability gate PASS
```

### 5.2 Safety / docs-quality gate

Passed. The gate verified:

- runtime modules do not contain forbidden live-execution tokens such as `curl`, `wget`, `nc`, live model API endpoints, `shell=True`, or real Codex invocation patterns,
- Markdown fences are balanced,
- touched files have final newlines,
- touched lines have no trailing whitespace.

Result:

```text
runtime live-execution safety gate PASS
docs/format safety gate PASS
```

Additional deterministic grep gates passed:

```text
! git grep -n -E 'exec\.Command(Context)?\("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
! git grep -n -E 'git.*diff.*\.\.\.' -- '*.go' ':!*_test.go' docs/BLK-009_blk-pipe-sprint-001-cli.md docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md docs/BLK-013_blk-test-handoff-fixture-contract.md docs/BLK-014_blk-execution-outcome-fixture-shape.md docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md docs/plans/BLK-PIPE-005_integration-contract-hardening-and-approval-gate-design.md docs/outcomes/BLK-PIPE-005_task-00*-outcome.md
```

---

## 6. Final Verification

Final verification before the implementation commit passed:

```text
python3 -m unittest discover -s python -p 'test_blk_orchestrator_gate.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
go run ./cmd/blk-pipe --health
git diff --check
```

Observed key results:

```text
Ran 10 tests in 0.000s
OK
Ran 69 tests in 0.649s
OK
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	6.751s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)
{"status":"OK","component":"blk-pipe"}
```

---

## 7. Deviations / Notes

- No live Codex, live tactical LLMs, network model services, cyber tooling, or live BLK-test MCP were used.
- No Hindsight was used.
- Because live LLM reviewers were forbidden, both review gates were deterministic local scripts rather than delegated model reviewers.
- `codex-live` approval-token validation intentionally records only `APPROVED_BUT_NOT_EXECUTED`; it is not a runtime live-execution trigger.
- BLK-test MCP request/response support is a disabled design stub only.

---

## 8. Next Task

BLK-PIPE-005 Task 7 should close Sprint 005 with audit-grade verification evidence and a narrow next-sprint seed that does not imply live autonomy is approved.
