# BLK-016 — Disabled BLK-test MCP Adapter Smoke and BEO/RTM Interface Fixtures

**Status:** Active fixture/interface contract
**Scope:** BLK-PIPE-007 disabled adapter smoke, not-run request, draft BEO projection, and BEO/RTM interface fixtures

---

## 1. Purpose

BLK-016 records the Sprint 007 local fixture/interface contract. It makes the new disabled BLK-test MCP adapter smoke path and BEO/RTM handoff shapes discoverable without opening any live authority path.

Sprint 007 remains deterministic local fixture work only:

- live BLK-test MCP remains disabled;
- RTM generation remains disabled;
- authoritative BEO publication remains disabled;
- live tactical execution remains blocked;
- sandbox/capability enforcement is later work;
- approval-channel mechanics are later work.

This contract preserves source-bound `beb_id`, `commit_hash`, `pre_engine_hash`, and opaque canonical `trace_artifacts` metadata. It does not read protected BLK-req vault files under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`.

---

## 2. Disabled BLK-test MCP adapter smoke helper

The public adapter smoke helper is:

```python
run_disabled_blk_test_mcp_adapter_smoke(
    source_report: dict[str, object],
    *,
    response_fixture: dict[str, object] | None = None,
    enabled: bool = False,
) -> dict[str, object]
```

The helper lives in `python/blk_test_mcp_adapter_smoke.py` and composes the disabled request builder, disabled send stub, and source-bound response mapper.

Required authority behavior:

- `enabled=True` raises before request/send/mapping work.
- The helper does not open network sockets, spawn subprocesses, call live MCP transports, call model services, run cyber tooling, generate RTM, or publish BEOs.
- With no response fixture, it returns `adapter_status: "DISABLED_SEND_BLOCKED"` and records `network_called: false`, `subprocess_called: false`, `rtm_status: "NOT_GENERATED"`, and `beo_publication: "DRAFT_ONLY"`.
- With a source-bound PASS/FAIL response fixture, it returns `adapter_status: "FIXTURE_RESPONSE_MAPPED"` and includes the mapped disabled response.
- The response mapping is source-bound: `beb_id`, `commit_hash`, `pre_engine_hash`, `trace_artifacts`, and non-empty checks must match the request evidence.

---

## 3. Non-success not-run request shape

The public non-success request builder is:

```python
build_blk_test_mcp_not_run_request(
    source_report: dict[str, object],
    *,
    enabled: bool = False,
) -> dict[str, object]
```

For non-success BLK-pipe reports, the disabled request method is:

```text
method: "blk_test.not_run"
```

Non-success reports must not become `method: "blk_test.evaluate_execution"`. They may preserve source metadata only as disabled/not-run evidence. `SUCCESS` reports continue to use `build_blk_test_mcp_request(...)` for evaluation-shaped disabled request fixtures, and non-success PASS/FAIL response projection rejects because no fixture verdict exists.

---

## 4. Draft BEO projection from disabled MCP PASS/FAIL mappings

The public disabled-MCP-to-BEO projection helper is:

```python
project_mapped_mcp_response_to_beo(
    mapped_response: dict[str, object],
    *,
    beo_id: str,
    test_profile: str = "strict-ci",
) -> dict[str, object]
```

It consumes only source-bound disabled MCP mapped response fixtures whose source is `blk-test-mcp-response-shape` and status is `PASS` or `FAIL`. It rejects `BLOCKED` because BLK-test did not produce a PASS/FAIL fixture verdict.

Every projected BEO fixture must include:

```text
beo_publication: "DRAFT_ONLY"
rtm_status: "NOT_GENERATED"
```

The projection preserves canonical `trace_artifacts` exactly and does not claim HITL approval, promotion authority, BEO publication authority, or RTM authority.

---

## 5. BEO/RTM disabled interface fixture

The public BEO/RTM interface helper is:

```python
build_beo_rtm_interface_fixture(
    beo_fixture: dict[str, object],
    *,
    interface_id: str,
) -> dict[str, object]
```

The output is an interface fixture only. It preserves draft BEO identifiers and opaque trace metadata while declaring:

```text
rtm_authority: "DISABLED_INTERFACE_ONLY"
rtm_status: "NOT_GENERATED"
beo_publication: "DRAFT_ONLY"
```

The helper rejects generated or authority-bearing fields including `rtm`, `rtm_id`, `requirements`, `coverage_matrix`, `published_at`, and `approved_by`. Output must not include `rtm`, `coverage_matrix`, resolved requirements, drift decisions, publication approval, or active-vault reads.

---

## 6. Future-work boundary

Sprint 007 deliberately stops at deterministic local fixture/interface shapes. A later sprint must define and verify all live execution mechanics before any tactical live path is authorized.

Out of scope for BLK-016:

- live MCP client transport;
- live BLK-test verdict authority;
- live tactical engine dispatch;
- network model service calls;
- cyber tooling or cyber execution;
- authoritative BEO publication;
- full RTM generation or drift rejection authority;
- sandbox/capability enforcement;
- approval-channel mechanics;
- protected BLK-req vault reads or requirement-body parsing.

---

## 7. Implementation and tests

Implementation modules:

- `python/blk_orchestrator_gate.py`
- `python/blk_test_mcp_adapter_smoke.py`
- `python/beo_fixture_projection.py`
- `python/beo_rtm_interface_fixtures.py`

Focused tests:

- `python/test_blk_orchestrator_gate.py`
- `python/test_blk_test_mcp_adapter_smoke.py`
- `python/test_beo_fixture_projection.py`
- `python/test_beo_rtm_interface_fixtures.py`

Canonical documentation touchpoints:

- [BLK-003](BLK-003_blk-pipe-blk-test-orchestration.md) — orchestration target/current boundary split.
- [BLK-013](BLK-013_blk-test-handoff-fixture-contract.md) — fixture-only BLK-test handoff contract.
- [BLK-014](BLK-014_blk-execution-outcome-fixture-shape.md) — draft-only BEO projection contract.
- [BLK-015](BLK-015_blk-pipe-approval-and-mcp-integration-design.md) — fail-closed approval and disabled MCP design contract.
