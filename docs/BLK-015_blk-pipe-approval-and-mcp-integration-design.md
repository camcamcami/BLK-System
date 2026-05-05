# BLK-015 — BLK-pipe Approval and MCP Integration Design

**Status:** Active fail-closed design contract with Sprint 006 approval semantics and Sprint 007 disabled adapter interfaces
**Scope:** Fail-closed `codex-live` approval gate, disabled BLK-test MCP request/response stubs, adapter smoke wrapper, and not-run request shape

---

## 1. Purpose

BLK-015 defines the deterministic contract surfaces needed before any future live integration is considered:

1. a fail-closed profile gate for `dev-smoke`, `strict-ci`, `codex-dry-run`, `codex-live`, and `cyber-execution`, and
2. disabled-by-default BLK-test MCP request/response shapes, and
3. Sprint 007 disabled adapter smoke and not-run request interfaces.

The current contract does not run Codex. It does not authorize live LLM execution. It does not run cyber tooling. It does not call live BLK-test MCP. It does not generate RTM artifacts or publish authoritative BEOs.

The implementation is dependency-free Python contract code in `python/blk_orchestrator_gate.py` and `python/blk_test_mcp_adapter_smoke.py`. It does not open network sockets, spawn subprocesses, call model services, call MCP servers, inspect active BLK-req vault paths, generate RTMs, or publish BEOs.

---

## 2. Profile gate decisions

The profile gate API is:

```python
evaluate_profile_gate(
    profile: str,
    *,
    beb_id: str,
    target_branch: str,
    trace_hash: str,
    approval_token: str | None = None,
) -> ProfileDecision
```

Decision meanings:

| Profile | Decision | Executable now (`allowed`)? | Approval recorded? | Live execution authorized? |
|---|---|---:|---:|---:|
| `dev-smoke` | `ALLOWED_LOCAL_ONLY` | Yes | No | No |
| `strict-ci` | `ALLOWED_LOCAL_ONLY` | Yes | No | No |
| `codex-dry-run` | `ALLOWED_LOCAL_ONLY` | Yes | No | No |
| `codex-live` without token | `BLOCKED_APPROVAL_REQUIRED` | No | No | No |
| `codex-live` with mismatched token | `BLOCKED_APPROVAL_MISMATCH` | No | No | No |
| `codex-live` with exact token | `APPROVED_BUT_NOT_EXECUTED` | No | Yes | No |
| `cyber-execution` | `BLOCKED_CYBER_EXECUTION` | No | No | No |
| unknown profile | `BLOCKED_UNKNOWN_PROFILE` | No | No | No |

`ProfileDecision.allowed` means the profile is executable now. `APPROVED_BUT_NOT_EXECUTED` is therefore not allowed to execute: exact-token `codex-live` validation records `approval_recorded=True` for audit evidence, keeps `allowed=False`, and keeps `live_execution_authorized=False`.

Even when the `codex-live` approval token validates, Sprint 006 records only the deterministic audit decision. It does not invoke Codex, live tactical LLMs, network model services, cyber tooling, or any future tactical engine. Approval-token validation remains audit-only until a future sprint explicitly authorizes a live execution path.

---

## 3. Approval-token shape

The `codex-live` approval-token shape is exact and auditable:

```text
BLK_APPROVE_CODEX_LIVE beb_id=<BEB_ID> target_branch=<branch> trace_hash=sha256:<64-lowercase-hex>
```

Example:

```text
BLK_APPROVE_CODEX_LIVE beb_id=BEB_006 target_branch=sprint/blk-pipe-006 trace_hash=sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Validation is deterministic:

- `beb_id` is required and must not contain whitespace.
- `target_branch` is required and must not contain whitespace.
- `trace_hash` must match `sha256:<64-lowercase-hex>`.
- The provided token must exactly match the token generated from the same `beb_id`, `target_branch`, and `trace_hash`.

This token is not a live-execution trigger in Sprint 006. It records audit-only approval evidence for the exact BEB/branch/trace context. A future sprint must separately authorize live execution before any `codex-live` path may run.

---

## 4. Disabled BLK-test MCP request shape

The Sprint 006 request builder is:

```python
build_blk_test_mcp_request(source_report: dict, *, enabled: bool = False) -> dict
```

With `enabled=False`, it validates source evidence before returning any evaluation-shaped disabled object. The source report must contain:

- a known BLK-pipe `status`,
- non-empty `beb_id`,
- non-empty `pre_engine_hash`,
- non-empty `trace_artifacts` whose `version_hash` values match `sha256:<64-lowercase-hex>`.

An evaluation request shape is returned only when `source_report.status == "SUCCESS"` and the report also includes non-empty `commit_hash` plus non-empty `staged_files`. Non-success reports raise `ValueError` instead of being treated as BLK-test evaluation requests; non-success handling belongs to a disabled/not-run or BLOCKED handoff path, not to `blk_test.evaluate_execution`.

Successful disabled request shape:

```json
{
  "enabled": false,
  "transport": "DISABLED_STUB",
  "method": "blk_test.evaluate_execution",
  "source_status": "SUCCESS",
  "beb_id": "BEB_005",
  "commit_hash": "<blk-pipe commit>",
  "pre_engine_hash": "<pre-engine hash>",
  "staged_files": ["dry_run_output.txt"],
  "destroyed_files": [],
  "trace_artifacts": [
    {
      "kind": "REQ",
      "id": "REQ-DRY-001",
      "version_hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
  ],
  "rtm_status": "NOT_GENERATED",
  "beo_publication": "DRAFT_ONLY",
  "reason": "live BLK-test MCP disabled in Sprint 006"
}
```

With `enabled=True`, the builder raises a clear disabled-path error instead of creating a live request. The send stub also fails closed and records that no network or subprocess call occurred.

---

## 4A. Sprint 007 disabled not-run request shape

Sprint 007 adds an explicit non-success disabled request builder:

```python
build_blk_test_mcp_not_run_request(source_report: dict, *, enabled: bool = False) -> dict
```

With `enabled=False`, known non-success source reports return disabled/not-run metadata with:

```text
method = "blk_test.not_run"
rtm_status = NOT_GENERATED
beo_publication = DRAFT_ONLY
```

This shape preserves non-success `beb_id`, `pre_engine_hash`, canonical `trace_artifacts`, and any available commit/staging metadata without claiming that BLK-test evaluated the source. Non-success reports must not be shaped as `blk_test.evaluate_execution`, and `SUCCESS` reports must use `build_blk_test_mcp_request(...)` instead.

---

## 5. Future BLK-test MCP response mapping

Future BLK-test MCP response shapes may map only to the existing fixture handoff statuses:

- `PASS`
- `FAIL`
- `BLOCKED`

The Sprint 006 mapper requires explicit source context:

```python
map_blk_test_mcp_response(response: dict, *, source_request: dict) -> dict
```

`PASS` and `FAIL` mapping requires all of the following:

- `source_request.source_status == "SUCCESS"`,
- exact `beb_id` match between response and source request,
- exact `commit_hash` match between response and source request,
- exact `pre_engine_hash` match between response and source request,
- exact `trace_artifacts` match between response and source request,
- non-empty response `checks`.

`BLOCKED` mapping preserves source-request `trace_artifacts` and may omit commit evidence when the source context never succeeded. In all cases, preserved trace artifacts must use canonical `sha256:<64-lowercase-hex>` `version_hash` values.

Mapped responses force:

```text
rtm_status = NOT_GENERATED
beo_publication = DRAFT_ONLY
```

Unknown response statuses reject deterministically. Mapping a response does not publish an authoritative BEO and does not generate RTM artifacts.

---

## 5A. Sprint 007 disabled adapter smoke helper

Sprint 007 adds the public adapter smoke helper:

```python
run_disabled_blk_test_mcp_adapter_smoke(source_report, *, response_fixture=None, enabled=False)
```

The helper composes `build_blk_test_mcp_request(...)` or `build_blk_test_mcp_not_run_request(...)`, `send_blk_test_mcp_request(...)`, and `map_blk_test_mcp_response(...)` without opening a live transport. With no response fixture it returns `DISABLED_SEND_BLOCKED`. With a source-bound PASS/FAIL fixture response it returns `FIXTURE_RESPONSE_MAPPED`.

Both paths preserve disabled authority markers: `live BLK-test MCP remains disabled`, `RTM generation remains disabled`, and `authoritative BEO publication remains disabled`. The helper records `network_called: false`, `subprocess_called: false`, `rtm_status: "NOT_GENERATED"`, and `beo_publication: "DRAFT_ONLY"`.

---

## 6. Authority and safety boundaries

BLK-015 is a contract/design stub only:

- no live Codex execution,
- no live tactical LLM execution,
- no network model service calls,
- no cyber execution,
- no live BLK-test MCP calls; live BLK-test MCP remains disabled,
- no requirement-vault reads from `docs/active/`, `docs/requirements/`, or `docs/use_cases/`,
- no RTM generation; RTM generation remains disabled,
- no authoritative BEO publication; authoritative BEO publication remains disabled,
- no claim that BLK-pipe is a full sandbox or host-secret isolation boundary.

Future work that proposes live execution must add a separate sprint plan with explicit sandbox/capability decisions, secret/network policy, audit logging, and human approval before execution. For Sprint 007, sandbox/capability enforcement is later work, and approval-channel mechanics are later work.

---

## 7. Implementation and tests

Implementation:

- `python/blk_orchestrator_gate.py`
- `python/blk_test_mcp_adapter_smoke.py`

Tests:

- `python/test_blk_orchestrator_gate.py`
- `python/test_blk_test_mcp_adapter_smoke.py`

Focused verification:

```bash
python3 -m unittest discover -s python -p 'test_blk_orchestrator_gate.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```
