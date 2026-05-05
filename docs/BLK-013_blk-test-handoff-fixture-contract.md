# BLK-013 — BLK-test Handoff Fixture Contract

**Status:** Active fixture contract
**Scope:** BLK-PIPE-004 Task 6

---

## 1. Purpose

This document defines the deterministic BLK-test handoff fixture shape used by
BLK-PIPE-004. The BLK-test fixture consumes an already-produced BLK-pipe execution report
and derives a local `PASS`, `FAIL`, or `BLOCKED` handoff object without calling
live BLK-test MCP, live Codex, live tactical LLMs, network model services, cyber
tooling, or any requirements-fetching service. There is no live BLK-test MCP call.

The fixture exists to prove trace-baton continuity and handoff shape only. It is
not an authority for BLK-req promotion, RTM generation, or live BLK-test verdicts.
Sprint 004 does not run Codex, Sprint 004 does not authorize live LLM execution,
and Sprint 004 does not authorize cyber execution.

---

## 2. Inputs

The fixture consumes a supplied BLK-pipe report dictionary. It does not read or
inspect protected BLK-req vault paths, including:

- `docs/active/`
- `docs/requirements/`
- `docs/use_cases/`

For `PASS` and `FAIL`, the source BLK-pipe report must include:

- `status == "SUCCESS"`
- non-empty `beb_id`
- non-empty `commit_hash`
- non-empty `pre_engine_hash`
- `staged_files == ["dry_run_output.txt"]`
- non-empty `trace_artifacts`
- every `trace_artifacts` entry must be an object with non-empty `kind`, `id`, and `version_hash`
- every `trace_artifacts[*].version_hash` must match `sha256:<64-lowercase-hex>` syntax

PASS requires BLK-pipe SUCCESS plus the exact commit/staging/trace evidence above before the BLK-test fixture may emit `PASS`.

Sprint 008 hardens this boundary: `PASS` and `FAIL` handoff fixtures require non-empty canonical trace artifacts and reject missing, empty, non-object, uppercase-hash, short-hash, or nonhex trace entries. The fixture validates only the opaque metadata syntax; it does not verify hashes against BLK-req files and does not read protected vaults.

A non-success BLK-pipe or adapter report is not converted into BLK-test `FAIL`. It is routed
to `BLOCKED` so the handoff states that BLK-test did not run. Sprint 005 keeps the
non-success dry-run invocation path evidence-preserving: the local no-throw helper returns
return code, parsed report, report status, and stderr so callers can inspect
`commit_hash`, `pre_engine_hash`, `staged_files`, `destroyed_files`, `trace_artifacts`,
and errors before building a `BLOCKED` handoff.

Known source statuses accepted by the fixture layer are:

```text
SUCCESS
FATAL_SYSTEM_PANIC
FATAL_ENGINE_FAILED
INVALID_PAYLOAD
SYNTAX_GATE_FAILED
UNAUTHORIZED_FILE_MUTATION
INVALID_REVERT_ANCHOR
FATAL_OUTPUT_FLOOD
ENGINE_TIMEOUT
GIT_DIRTY
INTERNAL_ERROR
FATAL_CRASH
FATAL_PYTHON_TIMEOUT
```

`FATAL_OUTPUT_FLOOD` is the canonical BLK-pipe output-flood status. The stale
legacy spelling `OUTPUT_FLOOD` is intentionally rejected. `FATAL_CRASH` and
`FATAL_PYTHON_TIMEOUT` are adapter-level statuses accepted because Sprint 005
routes adapter result dictionaries through the same fixture handoff boundary.

---

## 3. PASS shape

```json
{
  "status": "PASS",
  "beb_id": "BEB_004",
  "commit_hash": "<blk-pipe commit>",
  "pre_engine_hash": "<blk-pipe pre_engine_hash>",
  "test_profile": "strict-ci",
  "trace_artifacts": [
    {
      "kind": "REQ",
      "id": "REQ-DRY-001",
      "version_hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
  ],
  "checks": [
    {
      "name": "fixture-output-present",
      "status": "PASS",
      "summary": "dry_run_output.txt exists"
    }
  ],
  "compressed_logs": "bounded deterministic text"
}
```

`PASS` means the source BLK-pipe execution succeeded and the deterministic
fixture check passed.

---

## 4. FAIL shape

```json
{
  "status": "FAIL",
  "beb_id": "BEB_004",
  "commit_hash": "<blk-pipe commit>",
  "pre_engine_hash": "<blk-pipe pre_engine_hash>",
  "test_profile": "strict-ci",
  "trace_artifacts": [
    {
      "kind": "REQ",
      "id": "REQ-DRY-001",
      "version_hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
  ],
  "checks": [
    {
      "name": "fixture-output-present",
      "status": "FAIL",
      "summary": "dry_run_output.txt missing"
    }
  ],
  "compressed_logs": "bounded deterministic text"
}
```

`FAIL` means BLK-pipe succeeded but a deterministic fixture check failed. It does
not represent a BLK-pipe failure.

---

## 5. BLOCKED shape

```json
{
  "status": "BLOCKED",
  "beb_id": "BEB_004",
  "commit_hash": "",
  "pre_engine_hash": "<blk-pipe pre_engine_hash when present>",
  "test_profile": "strict-ci",
  "trace_artifacts": [
    {
      "kind": "REQ",
      "id": "REQ-DRY-001",
      "version_hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
  ],
  "checks": [
    {
      "name": "blk-pipe-success-required",
      "status": "BLOCKED",
      "summary": "BLK-test did not run because BLK-pipe status was SYNTAX_GATE_FAILED"
    }
  ],
  "compressed_logs": "bounded deterministic text"
}
```

`BLOCKED` preserves safe canonical trace artifacts when present, including the opaque
canonical `version_hash` baton (`sha256:<64-lowercase-hex>`), while making clear that the handoff state is: No BLK-test fixture verdict ran. If a non-success source report lacks decoded trace metadata because payload validation failed before trace decode, the fixture preserves `trace_artifacts: []` and adds `trace_absence_reason: "source report did not include decoded trace_artifacts"`. That trace-absent `BLOCKED` shape is non-authoritative blocked evidence only; it must not be converted into `PASS`, `FAIL`, draft BEO success evidence, RTM generation, or BLK-req promotion evidence.

---

## 6. Determinism and log bounds

- PASS, FAIL, and BLOCKED are derived only from the supplied report and explicit
  fixture status path.
- There is no MCP call, no live test server dependency, and no LLM judgment.
- Logs are line-deduplicated and byte-bounded for fixture use.
- Trace artifacts are copied as opaque fields after canonical structure and `version_hash` syntax validation. PASS/FAIL require non-empty canonical trace artifacts. BLOCKED may record explicit trace absence only as blocked/non-authoritative evidence. The fixture does not parse or
  validate requirement bodies, verify hashes against files, or read protected BLK-req vault paths.

---

## 7. Disabled BLK-test MCP design stub

Sprint 005 added `python/blk_orchestrator_gate.py` as a disabled-by-default request/response contract for future BLK-test MCP integration. Sprint 006 hardens that stub so source evidence must be present before an evaluation-shaped disabled request or PASS/FAIL-shaped response mapping can exist.

The request builder records source BLK-pipe evidence, opaque `trace_artifacts`, `rtm_status: NOT_GENERATED`, and `beo_publication: DRAFT_ONLY`, but only after validating a known source status, non-empty `beb_id`, non-empty `pre_engine_hash`, and non-empty canonical `trace_artifacts`. It returns `method: "blk_test.evaluate_execution"` only for `source_report.status == "SUCCESS"` with non-empty `commit_hash` and non-empty `staged_files`; non-success reports raise instead of being treated as evaluation requests.

The send stub returns `BLOCKED` with `network_called: false` and `subprocess_called: false`. It does not open sockets, spawn MCP, call live services, generate RTM artifacts, or publish authoritative BEOs.

Future BLK-test MCP response mapping may accept only `PASS`, `FAIL`, and `BLOCKED`; unknown response statuses reject deterministically. `PASS` and `FAIL` mapping require explicit `source_request` context, exact `beb_id` / `commit_hash` / `pre_engine_hash` / `trace_artifacts` matches, and non-empty checks. `BLOCKED` mapping preserves source trace artifacts and may omit commit evidence if the source never succeeded.

---

## 8. Implementation mapping

The local Python fixture module is `python/blk_test_handoff_fixtures.py`:

- `build_blk_test_pass_handoff(source_report, ...)`
- `build_blk_test_fail_handoff(source_report, ...)`
- `build_blk_test_blocked_handoff(source_report, ...)`

The Sprint 005/007 disabled MCP stub module is `python/blk_orchestrator_gate.py`:

- `build_blk_test_mcp_request(source_report, enabled=False)`
- `build_blk_test_mcp_not_run_request(source_report, enabled=False)`
- `send_blk_test_mcp_request(request, enabled=False)`
- `map_blk_test_mcp_response(response, source_request=source_request)`

The Sprint 007 disabled adapter smoke module is `python/blk_test_mcp_adapter_smoke.py`:

- `run_disabled_blk_test_mcp_adapter_smoke(source_report, response_fixture=None, enabled=False)`

The deterministic test suites are `python/test_blk_test_handoff_fixtures.py`, `python/test_blk_orchestrator_gate.py`, and `python/test_blk_test_mcp_adapter_smoke.py`.

---

## 9. Sprint 007 disabled adapter smoke and not-run request contract

Sprint 007 extends this active fixture contract with a source-bound disabled BLK-test MCP adapter smoke wrapper and explicit non-success not-run request shape. `live BLK-test MCP remains disabled` and `RTM generation remains disabled`; the additions preserve trace metadata only and do not create live BLK-test verdict authority.

New public helpers:

- `run_disabled_blk_test_mcp_adapter_smoke(...)` composes the disabled request builder, disabled send stub, and source-bound response mapper. With no response fixture it returns `DISABLED_SEND_BLOCKED`; with a PASS/FAIL response fixture it returns `FIXTURE_RESPONSE_MAPPED`. Both paths record `network_called: false`, `subprocess_called: false`, `rtm_status: "NOT_GENERATED"`, and `beo_publication: "DRAFT_ONLY"`.
- `build_blk_test_mcp_not_run_request(...)` returns `method: "blk_test.not_run"` for known non-success source reports. Non-success reports must not become `blk_test.evaluate_execution`; they preserve source `beb_id`, `pre_engine_hash`, and canonical `trace_artifacts` as disabled/not-run evidence only.

The Sprint 007 adapter smoke helper may map PASS/FAIL-shaped disabled MCP fixtures only when they exactly match SUCCESS source evidence. A BLOCKED or not-run path is not a PASS/FAIL BLK-test verdict and cannot be projected as a successful evaluation. See [BLK-016](BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md) for the complete disabled adapter contract.
