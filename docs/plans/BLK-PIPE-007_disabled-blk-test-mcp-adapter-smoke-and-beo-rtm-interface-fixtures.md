# BLK-pipe Sprint 007 — Disabled BLK-test MCP Adapter Smoke and BEO/RTM Interface Fixtures

> **For Hermes:** Use `blk-system-sprint-execution` to implement this plan task-by-task. This sprint is deterministic local fixture/interface work only. Do not use Hindsight. Do not run live Codex, live tactical LLMs, network model services, cyber tooling, live BLK-test MCP, RTM generation, RTM authority, or authoritative BEO publication.

**Goal:** Add deterministic smoke coverage and fixture/interface shapes around the disabled BLK-test MCP adapter seam and the BEO/RTM handoff seam without enabling any live tactical execution path.

**Architecture:** Sprint 007 stays on the Sprint 006 authority boundary. The BLK-test MCP adapter remains a disabled local contract wrapper over source-bound request/response shapes; BEO projection remains draft-only; RTM remains an interface placeholder that preserves opaque trace metadata but generates no ledger and reads no protected BLK-req vault files. The sprint adds public fixture helpers, tests, and active-contract documentation so future live-integration work has clear shapes to harden later.

**Tech Stack:** Go 1.26.x, POSIX-only BLK-pipe CLI, dependency-free Python fixture/adapter modules, deterministic Go/Python tests, Markdown doctrine/outcome documents.

---

## 0. Current Known State

Repository:

```text
/home/dad/BLK-System
```

Planning preflight when this document was authored:

```text
date                         -> 2026-05-05 12:29:26 AEST
git status --short --branch  -> ## main...origin/main
HEAD                         -> 23f1a4a docs: close out blk-pipe sprint 006
```

Relevant Sprint 006 source state:

- `python/blk_orchestrator_gate.py`
  - `evaluate_profile_gate(...)` keeps exact-token `codex-live` audit-only: `decision == "APPROVED_BUT_NOT_EXECUTED"`, `allowed is False`, `live_execution_authorized is False`.
  - `build_blk_test_mcp_request(source_report, enabled=False)` returns an evaluation-shaped disabled request only for complete `SUCCESS` source evidence.
  - `send_blk_test_mcp_request(request, enabled=False)` returns `BLOCKED`, `network_called: False`, `subprocess_called: False`.
  - `map_blk_test_mcp_response(response, *, source_request)` requires explicit source context and binds PASS/FAIL to exact source evidence.
- `python/blk_test_handoff_fixtures.py`
  - builds deterministic PASS/FAIL/BLOCKED BLK-test handoff fixtures from supplied BLK-pipe reports only.
- `python/beo_fixture_projection.py`
  - projects supplied PASS/FAIL BLK-test fixture handoffs into draft BEO-shaped objects with `rtm_status: NOT_GENERATED`.
- Active contracts already document Sprint 006 boundaries:
  - `docs/BLK-013_blk-test-handoff-fixture-contract.md`
  - `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
  - `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`

Sprint 007 must preserve those boundaries while adding the missing disabled-adapter smoke and BEO/RTM interface fixture surfaces.

---

## 1. Rationale and Task Map

Sprint 006 remediated hostile-review blockers around:

- authority semantics,
- trace-baton strictness,
- source-bound disabled MCP stubs,
- active doctrine drift,
- metadata gates.

Sprint 007 returns to the next narrow fixture seam without changing authority.

| Rationale item | Sprint 007 task |
| --- | --- |
| Disabled BLK-test MCP request/send/response shapes exist, but there is no adapter-level smoke wrapper proving the composed disabled path | Task 1 |
| Non-success BLK-pipe reports need an explicit disabled/not-run adapter path rather than manual synthetic source requests | Task 2 |
| BEO projection should consume source-bound disabled MCP PASS/FAIL fixture output without treating it as live BLK-test authority | Task 3 |
| RTM-facing shape should be explicit as an interface fixture while RTM generation/authority remains disabled | Task 4 |
| Active docs should describe the Sprint 007 disabled adapter and BEO/RTM interface contract without live-authority drift | Task 5 |
| Closeout should prove no live execution expansion, no stale metadata, and no broadening into sandbox/approval-channel mechanics | Task 6 |

---

## 2. Non-Goals and Hard Blocks

Sprint 007 must not implement, invoke, or imply:

- live Codex invocation,
- live tactical LLM API calls,
- network model services,
- `codex-live` runtime execution,
- cyber tooling or cyber execution,
- execution against real cyber-program repositories or live targets,
- live BLK-test MCP calls,
- live MCP client transport,
- authoritative BLK-test verdict authority,
- authoritative BEO publication,
- complete RTM generation as a traceability ledger,
- RTM drift rejection authority,
- full sandbox/container/cgroup/VM enforcement,
- production host-secret isolation claims,
- production approval-channel mechanics,
- active BLK-req vault reads or requirement-body parsing.

Allowed work:

```text
deterministic local tests
fixture-only execution
source-bound disabled BLK-test MCP adapter smoke helpers
explicit disabled/not-run MCP request shape for non-success source reports
draft-only BEO projection from source-bound fixture data
RTM interface fixture metadata with rtm_status NOT_GENERATED
documentation updates and outcome evidence
```

A later, separate sprint must handle sandbox/capability enforcement and real approval-channel mechanics before any live tactical execution is approved.

---

## 3. Invariants to Preserve

1. BLK-pipe remains a deterministic transport/mutation gate, not an architect, requirement parser, live LLM caller, BLK-test authority, BEO publisher, RTM generator, or sandbox.
2. Hermes/BLK-pipe/BLK-test/BEO/RTM boundaries preserve opaque trace metadata without reading or parsing active BLK-req bodies.
3. `APPROVED_BUT_NOT_EXECUTED` stays non-executable: `allowed=False`, `live_execution_authorized=False`.
4. BLK-test PASS/FAIL-shaped data must never exist without source-bound `beb_id`, `commit_hash`, `pre_engine_hash`, `trace_artifacts`, and non-empty checks.
5. Non-success BLK-pipe reports must not become `blk_test.evaluate_execution`; they may only become explicit disabled/not-run or BLOCKED fixture data.
6. The canonical trace artifact shape remains:

   ```yaml
   trace_artifacts:
     - kind: "REQ"
       id: "REQ-042"
       version_hash: "sha256:<64-lowercase-hex>"
   ```

7. Protected BLK-req vault paths remain denied to all fixture/interface helpers: `docs/active/`, `docs/requirements/`, and `docs/use_cases/`.
8. BEO fixture output remains draft-only and must not claim HITL approval, promotion authority, publication authority, or RTM authority.
9. RTM interface fixtures may preserve source metadata only; they must not generate an RTM, compare hashes to live requirement files, or decide drift.
10. New BLK-System plans and active docs use BLK-native BEB/BEO terminology and `beb_id`, not legacy execution-brief/outcome vocabulary.
11. No production `git add .`, `git add -u`, `git stash`, relative revert anchors, or triple-dot report diffs.

---

## 4. Controller Workflow for Each Task

For each task:

1. Preflight:

   ```bash
   cd /home/dad/BLK-System
   export PATH="$HOME/.local/bin:$PATH"
   git status --short --branch
   ```

2. Use strict TDD for code changes: add a failing test/probe first, capture RED, implement minimal code, capture GREEN.
3. Use deterministic local review gates only. Do not dispatch live Codex, live tactical LLM, network model, cyber, or live BLK-test MCP reviewers.
4. Run focused tests listed in the task.
5. Run shared verification before each implementation commit:

   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   python3 -m unittest discover -s python -p 'test_*.py'
   go test ./...
   go vet ./...
   git diff --check
   ```

6. Create a matching outcome document for Tasks 1-5:

   ```text
   docs/outcomes/BLK-PIPE-007_task-00N-outcome.md
   ```

7. Use the sprint closeout document as Task 6 outcome:

   ```text
   docs/outcomes/BLK-PIPE-007_sprint-closeout.md
   ```

8. Commit each task after verification with the listed commit message.
9. Push only after verification passes and `git status --short --branch` is clean/aligned.

---

## 5. Task 1 — Add Disabled BLK-test MCP Adapter Smoke Wrapper for SUCCESS PASS/FAIL Paths

### Objective

Add a small dependency-free adapter-smoke helper that composes the existing disabled request builder, disabled send stub, and source-bound response mapper for `SUCCESS` source reports.

This proves the disabled adapter seam end-to-end without opening a live MCP transport.

### Files

Create:

- `python/blk_test_mcp_adapter_smoke.py`
- `python/test_blk_test_mcp_adapter_smoke.py`
- `docs/outcomes/BLK-PIPE-007_task-001-outcome.md`

Modify only if needed:

- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md` after Task 5, not during Task 1 unless test docs become stale.

### Required behavior

Create a public helper shaped like:

```python
def run_disabled_blk_test_mcp_adapter_smoke(
    source_report: dict[str, object],
    *,
    response_fixture: dict[str, object] | None = None,
    enabled: bool = False,
) -> dict[str, object]:
    ...
```

Required semantics:

- `enabled=True` raises `RuntimeError` before any request/send/mapping work.
- For a complete `SUCCESS` source report and no `response_fixture`, it:
  - builds `build_blk_test_mcp_request(source_report, enabled=False)`,
  - calls `send_blk_test_mcp_request(request, enabled=False)`,
  - returns an adapter smoke result with `adapter_status: "DISABLED_SEND_BLOCKED"`,
  - preserves request `trace_artifacts`,
  - records `network_called: False`, `subprocess_called: False`,
  - records `rtm_status: "NOT_GENERATED"`,
  - records `beo_publication: "DRAFT_ONLY"`.
- For a complete `SUCCESS` source report plus a PASS/FAIL `response_fixture`, it:
  - builds the disabled request,
  - records the disabled send result,
  - maps the response with `map_blk_test_mcp_response(response_fixture, source_request=request)`,
  - returns `adapter_status: "FIXTURE_RESPONSE_MAPPED"`,
  - preserves source-bound `beb_id`, `commit_hash`, `pre_engine_hash`, and exact `trace_artifacts`.
- It must not import or call `socket`, `requests`, `urllib`, `http.client`, `subprocess`, MCP SDKs, live model clients, or cyber tooling.

Suggested result shape:

```json
{
  "adapter_status": "FIXTURE_RESPONSE_MAPPED",
  "source": "disabled-blk-test-mcp-adapter-smoke",
  "transport": "DISABLED_STUB",
  "request": {"method": "blk_test.evaluate_execution"},
  "send_result": {"status": "BLOCKED", "network_called": false, "subprocess_called": false},
  "mapped_response": {"status": "PASS"},
  "network_called": false,
  "subprocess_called": false,
  "rtm_status": "NOT_GENERATED",
  "beo_publication": "DRAFT_ONLY"
}
```

### TDD RED gates

Add tests first in `python/test_blk_test_mcp_adapter_smoke.py`:

```python
from blk_test_mcp_adapter_smoke import run_disabled_blk_test_mcp_adapter_smoke


def test_disabled_adapter_smoke_without_response_blocks_send_only(self):
    result = run_disabled_blk_test_mcp_adapter_smoke(success_report())
    self.assertEqual(result["adapter_status"], "DISABLED_SEND_BLOCKED")
    self.assertFalse(result["network_called"])
    self.assertFalse(result["subprocess_called"])
    self.assertNotIn("mapped_response", result)


def test_disabled_adapter_smoke_maps_source_bound_pass_fixture(self):
    report = success_report()
    request = build_blk_test_mcp_request(report)
    response = pass_response_for(request)
    result = run_disabled_blk_test_mcp_adapter_smoke(report, response_fixture=response)
    self.assertEqual(result["adapter_status"], "FIXTURE_RESPONSE_MAPPED")
    self.assertEqual(result["mapped_response"]["status"], "PASS")
    self.assertEqual(result["mapped_response"]["trace_artifacts"], report["trace_artifacts"])


def test_disabled_adapter_smoke_rejects_response_source_mismatch(self):
    report = success_report()
    request = build_blk_test_mcp_request(report)
    response = pass_response_for(request)
    response["beb_id"] = "BEB_OTHER"
    with self.assertRaisesRegex(ValueError, "beb_id"):
        run_disabled_blk_test_mcp_adapter_smoke(report, response_fixture=response)
```

Expected RED before implementation:

```text
ModuleNotFoundError: No module named 'blk_test_mcp_adapter_smoke'
```

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_blk_test_mcp_adapter_smoke.py' -v
python3 -m unittest discover -s python -p 'test_blk_orchestrator_gate.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

### Outcome evidence

Create `docs/outcomes/BLK-PIPE-007_task-001-outcome.md` with:

- RED failure summary,
- implementation summary,
- focused test output,
- shared verification output,
- explicit authority statement: no live BLK-test MCP, no network/subprocess, no RTM generation, no authoritative BEO publication.

### Commit message

```bash
git add python/blk_test_mcp_adapter_smoke.py python/test_blk_test_mcp_adapter_smoke.py docs/outcomes/BLK-PIPE-007_task-001-outcome.md
git commit -m "test: add disabled blk-test mcp adapter smoke wrapper"
```

---

## 6. Task 2 — Add Explicit Disabled Not-Run MCP Request Shape for Non-SUCCESS Source Reports

### Objective

Add a public non-success disabled request builder so adapter smoke can represent `BLOCKED`/not-run paths without manually mutating a SUCCESS evaluation request.

Sprint 006 correctly made `build_blk_test_mcp_request(...)` reject non-success reports as evaluation requests. Sprint 007 may add a separate disabled/not-run shape because this plan explicitly requires adapter smoke paths for BEO/RTM interface fixture coverage.

### Files

Modify:

- `python/blk_orchestrator_gate.py`
- `python/test_blk_orchestrator_gate.py`
- `python/blk_test_mcp_adapter_smoke.py`
- `python/test_blk_test_mcp_adapter_smoke.py`

Create outcome:

- `docs/outcomes/BLK-PIPE-007_task-002-outcome.md`

### Required behavior

Add a public helper shaped like:

```python
def build_blk_test_mcp_not_run_request(
    source_report: dict[str, object],
    *,
    enabled: bool = False,
) -> dict[str, object]:
    ...
```

Required semantics:

- `enabled=True` raises `RuntimeError("live BLK-test MCP ... disabled")`.
- It requires a known non-success BLK-pipe status.
- It rejects `status == "SUCCESS"` with an error that points callers to `build_blk_test_mcp_request` for evaluation-shaped disabled requests.
- It requires:
  - non-empty `beb_id`,
  - non-empty `pre_engine_hash`,
  - non-empty canonical `trace_artifacts`.
- It may preserve optional `commit_hash`, `staged_files`, and `destroyed_files`, but must not require success-only commit/staging evidence.
- It returns:

  ```json
  {
    "enabled": false,
    "transport": "DISABLED_STUB",
    "method": "blk_test.not_run",
    "source_status": "SYNTAX_GATE_FAILED",
    "beb_id": "BEB_007",
    "commit_hash": "",
    "pre_engine_hash": "<pre-engine hash>",
    "staged_files": [],
    "destroyed_files": [],
    "trace_artifacts": [{"kind": "REQ", "id": "REQ-DRY-001", "version_hash": "sha256:..."}],
    "rtm_status": "NOT_GENERATED",
    "beo_publication": "DRAFT_ONLY",
    "reason": "BLK-test did not run because BLK-pipe source_status was SYNTAX_GATE_FAILED"
  }
  ```

- Existing `build_blk_test_mcp_request(...)` behavior must not be weakened: non-success source reports still raise rather than producing `blk_test.evaluate_execution`.
- `map_blk_test_mcp_response(..., source_request=not_run_request)` may map only `BLOCKED`; PASS/FAIL must continue to reject with `source_status SUCCESS`.
- The adapter smoke helper should select:
  - `build_blk_test_mcp_request(...)` for `SUCCESS`,
  - `build_blk_test_mcp_not_run_request(...)` for known non-success statuses.

### TDD RED gates

Add tests before implementation:

```python
from blk_orchestrator_gate import build_blk_test_mcp_not_run_request


def test_not_run_request_preserves_non_success_trace_without_evaluation_claim(self):
    request = build_blk_test_mcp_not_run_request(non_success_report(status="SYNTAX_GATE_FAILED"))
    self.assertEqual(request["method"], "blk_test.not_run")
    self.assertEqual(request["source_status"], "SYNTAX_GATE_FAILED")
    self.assertEqual(request["trace_artifacts"], TRACE_ARTIFACTS)
    self.assertEqual(request["rtm_status"], "NOT_GENERATED")
    self.assertEqual(request["beo_publication"], "DRAFT_ONLY")


def test_not_run_request_rejects_success_report(self):
    with self.assertRaisesRegex(ValueError, "SUCCESS"):
        build_blk_test_mcp_not_run_request(success_report())


def test_not_run_source_can_only_map_blocked_response(self):
    source_request = build_blk_test_mcp_not_run_request(non_success_report())
    blocked = map_blk_test_mcp_response({"status": "BLOCKED"}, source_request=source_request)
    self.assertEqual(blocked["status"], "BLOCKED")
    with self.assertRaisesRegex(ValueError, "source_status SUCCESS"):
        map_blk_test_mcp_response(pass_response_for(source_request), source_request=source_request)
```

Expected RED before implementation:

```text
ImportError: cannot import name 'build_blk_test_mcp_not_run_request'
```

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_blk_orchestrator_gate.py' -v
python3 -m unittest discover -s python -p 'test_blk_test_mcp_adapter_smoke.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

### Outcome evidence

Create `docs/outcomes/BLK-PIPE-007_task-002-outcome.md` with:

- RED import/error evidence,
- proof that `build_blk_test_mcp_request(non_success_report)` still rejects evaluation-shaped requests,
- proof that `build_blk_test_mcp_not_run_request(non_success_report)` returns `method: "blk_test.not_run"`,
- proof that PASS/FAIL mapping remains impossible for non-success source context.

### Commit message

```bash
git add python/blk_orchestrator_gate.py python/test_blk_orchestrator_gate.py python/blk_test_mcp_adapter_smoke.py python/test_blk_test_mcp_adapter_smoke.py docs/outcomes/BLK-PIPE-007_task-002-outcome.md
git commit -m "feat: add disabled blk-test mcp not-run request shape"
```

---

## 7. Task 3 — Project Source-Bound Disabled MCP PASS/FAIL Fixtures into Draft BEO Shape

### Objective

Allow draft BEO projection from a source-bound disabled MCP PASS/FAIL fixture result without treating it as a live BLK-test verdict or authoritative BEO publication.

### Files

Modify:

- `python/beo_fixture_projection.py`
- `python/test_beo_fixture_projection.py`
- `python/test_blk_test_mcp_adapter_smoke.py` if end-to-end smoke through BEO is added there.

Create outcome:

- `docs/outcomes/BLK-PIPE-007_task-003-outcome.md`

### Required behavior

Add a helper shaped like:

```python
def project_mapped_mcp_response_to_beo(
    mapped_response: dict[str, object],
    *,
    beo_id: str,
    test_profile: str = "strict-ci",
) -> dict[str, object]:
    ...
```

Required semantics:

- Accepts only mapped source `"blk-test-mcp-response-shape"` or the adapter smoke `mapped_response` object produced by Task 1/2.
- Accepts only `status in {"PASS", "FAIL"}`.
- Rejects `BLOCKED`; a not-run source did not produce a BLK-test verdict and must not produce a BEO fixture verdict.
- Requires non-empty `beb_id`, `commit_hash`, `pre_engine_hash`, canonical non-empty `trace_artifacts`, and non-empty `checks`.
- Injects an explicit local fixture `test_profile` for BEO summary purposes; it must not call a live BLK-test profile.
- Returns a draft-only BEO shape with:
  - source-bound `beb_id`, `commit_hash`, `pre_engine_hash`, `trace_artifacts`,
  - deterministic `test_summary`,
  - `rtm_status: "NOT_GENERATED"`,
  - `beo_publication: "DRAFT_ONLY"`,
  - no `rtm` object,
  - no `published_at`, `approved_by`, or HITL authority fields.

Also add `beo_publication: "DRAFT_ONLY"` to the existing `project_blk_test_handoff_to_beo(...)` return shape so every BEO fixture states its publication boundary explicitly.

### TDD RED gates

Add tests before implementation:

```python
from beo_fixture_projection import project_mapped_mcp_response_to_beo


def test_mapped_disabled_mcp_pass_projects_to_draft_beo(self):
    mapped = mapped_mcp_pass_response()
    beo = project_mapped_mcp_response_to_beo(mapped, beo_id="BEO_007")
    self.assertEqual(beo["beo_id"], "BEO_007")
    self.assertEqual(beo["status"], "PASS")
    self.assertEqual(beo["source"], "blk-test-mcp-response-shape")
    self.assertEqual(beo["beo_publication"], "DRAFT_ONLY")
    self.assertEqual(beo["rtm_status"], "NOT_GENERATED")
    self.assertNotIn("rtm", beo)


def test_mapped_disabled_mcp_blocked_does_not_project_to_beo(self):
    mapped = mapped_mcp_blocked_response()
    with self.assertRaisesRegex(ValueError, "PASS/FAIL"):
        project_mapped_mcp_response_to_beo(mapped, beo_id="BEO_007")


def test_all_beo_fixture_outputs_are_draft_only(self):
    beo = project_blk_test_handoff_to_beo(pass_handoff(), beo_id="BEO_004")
    self.assertEqual(beo["beo_publication"], "DRAFT_ONLY")
```

Expected RED before implementation:

```text
ImportError: cannot import name 'project_mapped_mcp_response_to_beo'
KeyError: 'beo_publication'
```

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_beo_fixture_projection.py' -v
python3 -m unittest discover -s python -p 'test_blk_test_mcp_adapter_smoke.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

### Outcome evidence

Create `docs/outcomes/BLK-PIPE-007_task-003-outcome.md` with:

- RED import/key evidence,
- proof mapped PASS/FAIL can become draft BEO fixture output,
- proof mapped BLOCKED cannot become BEO verdict output,
- proof every BEO fixture declares `beo_publication: DRAFT_ONLY` and `rtm_status: NOT_GENERATED`.

### Commit message

```bash
git add python/beo_fixture_projection.py python/test_beo_fixture_projection.py python/test_blk_test_mcp_adapter_smoke.py docs/outcomes/BLK-PIPE-007_task-003-outcome.md
git commit -m "feat: project disabled mcp fixtures to draft beo shape"
```

---

## 8. Task 4 — Add BEO/RTM Interface Fixture Shape Without RTM Generation

### Objective

Add an explicit BEO/RTM interface fixture that preserves draft BEO trace metadata for future RTM integration while keeping RTM generation and authority disabled.

This is an interface contract, not a traceability ledger.

### Files

Create:

- `python/beo_rtm_interface_fixtures.py`
- `python/test_beo_rtm_interface_fixtures.py`
- `docs/outcomes/BLK-PIPE-007_task-004-outcome.md`

Modify if helpful:

- `python/test_beo_fixture_projection.py` to include an end-to-end draft BEO -> RTM interface smoke.

### Required behavior

Add a public helper shaped like:

```python
def build_beo_rtm_interface_fixture(
    beo_fixture: dict[str, object],
    *,
    interface_id: str,
) -> dict[str, object]:
    ...
```

Required input validation:

- Requires non-empty `interface_id`.
- Requires `beo_id`, `beb_id`, `status`, `pre_engine_hash`, and non-empty canonical `trace_artifacts`.
- Requires `beo_publication == "DRAFT_ONLY"`.
- Requires `rtm_status == "NOT_GENERATED"`.
- Accepts only BEO fixture `status in {"PASS", "FAIL"}`.
- Rejects any input that already contains generated RTM authority fields such as `rtm`, `rtm_id`, `requirements`, `coverage_matrix`, `published_at`, or `approved_by`.

Required output shape:

```json
{
  "interface_id": "BEO_RTM_IFACE_007",
  "source": "beo-rtm-interface-fixture",
  "beo_id": "BEO_007",
  "beb_id": "BEB_007",
  "beo_status": "PASS",
  "beo_publication": "DRAFT_ONLY",
  "rtm_status": "NOT_GENERATED",
  "rtm_authority": "DISABLED_INTERFACE_ONLY",
  "trace_artifacts": [
    {
      "kind": "REQ",
      "id": "REQ-DRY-001",
      "version_hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
  ],
  "active_vault_read": false,
  "requirements_resolved": false,
  "reason": "RTM generation remains disabled; fixture preserves opaque trace metadata only"
}
```

Required negative guarantees:

- Output must not include `rtm`, `rtm_id`, `requirements`, `coverage_matrix`, `published_at`, `approved_by`, or any claim of drift authority.
- The helper must not read protected BLK-req vault paths.
- The helper must not call network, subprocess, MCP, live model, or cyber tooling.

### TDD RED gates

Add tests before implementation:

```python
from beo_rtm_interface_fixtures import build_beo_rtm_interface_fixture


def test_beo_rtm_interface_fixture_preserves_trace_but_generates_no_rtm(self):
    interface = build_beo_rtm_interface_fixture(draft_beo(), interface_id="BEO_RTM_IFACE_007")
    self.assertEqual(interface["rtm_status"], "NOT_GENERATED")
    self.assertEqual(interface["rtm_authority"], "DISABLED_INTERFACE_ONLY")
    self.assertEqual(interface["trace_artifacts"], TRACE_ARTIFACTS)
    self.assertNotIn("rtm", interface)
    self.assertFalse(interface["active_vault_read"])
    self.assertFalse(interface["requirements_resolved"])


def test_beo_rtm_interface_rejects_authoritative_or_generated_inputs(self):
    beo = draft_beo(beo_publication="PUBLISHED")
    with self.assertRaisesRegex(ValueError, "DRAFT_ONLY"):
        build_beo_rtm_interface_fixture(beo, interface_id="BEO_RTM_IFACE_007")


def test_beo_rtm_interface_does_not_read_active_vault(self):
    with patch.object(Path, "read_text", fail_forbidden_read):
        interface = build_beo_rtm_interface_fixture(draft_beo(), interface_id="BEO_RTM_IFACE_007")
    self.assertEqual(interface["rtm_status"], "NOT_GENERATED")
```

Expected RED before implementation:

```text
ModuleNotFoundError: No module named 'beo_rtm_interface_fixtures'
```

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_beo_rtm_interface_fixtures.py' -v
python3 -m unittest discover -s python -p 'test_beo_fixture_projection.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

### Outcome evidence

Create `docs/outcomes/BLK-PIPE-007_task-004-outcome.md` with:

- RED missing-module evidence,
- PASS evidence for draft BEO -> RTM interface fixture,
- negative guarantee evidence: no generated RTM keys, no active vault reads, no publication authority.

### Commit message

```bash
git add python/beo_rtm_interface_fixtures.py python/test_beo_rtm_interface_fixtures.py python/test_beo_fixture_projection.py docs/outcomes/BLK-PIPE-007_task-004-outcome.md
git commit -m "feat: add draft beo rtm interface fixture"
```

---

## 9. Task 5 — Document Sprint 007 Disabled Adapter and BEO/RTM Interface Contracts

### Objective

Update active doctrine so the new Sprint 007 fixtures are discoverable and authority-bounded, without implying live BLK-test MCP, RTM generation, BEO publication, sandbox enforcement, or approval-channel mechanics.

### Files

Create:

- `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`
- `docs/outcomes/BLK-PIPE-007_task-005-outcome.md`

Modify:

- `docs/BLK-003_blk-pipe-blk-test-orchestration.md`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`
- `README.md`

### Required documentation behavior

`docs/BLK-016...` must define:

1. Disabled BLK-test MCP adapter smoke helper:
   - `run_disabled_blk_test_mcp_adapter_smoke(...)`
   - no live MCP/network/subprocess,
   - `DISABLED_SEND_BLOCKED` and `FIXTURE_RESPONSE_MAPPED` statuses.
2. Non-success not-run request shape:
   - `build_blk_test_mcp_not_run_request(...)`,
   - `method: "blk_test.not_run"`,
   - no non-success `blk_test.evaluate_execution`.
3. Draft BEO projection from source-bound disabled MCP PASS/FAIL mapped fixtures:
   - `project_mapped_mcp_response_to_beo(...)`,
   - `beo_publication: "DRAFT_ONLY"`,
   - `rtm_status: "NOT_GENERATED"`.
4. BEO/RTM interface fixture:
   - `build_beo_rtm_interface_fixture(...)`,
   - `rtm_authority: "DISABLED_INTERFACE_ONLY"`,
   - no `rtm`, no `coverage_matrix`, no protected-vault reads.
5. Explicit future-work boundary:
   - sandbox/capability enforcement is later work,
   - real approval-channel mechanics are later work,
   - live tactical execution remains blocked.

Update existing docs:

- `docs/BLK-003...`
  - Replace stale “Current Sprint 006 boundary” headings with an “Current implementation boundary after Sprint 007” section where needed.
  - Preserve the target-architecture/current-boundary distinction.
- `docs/BLK-013...`
  - Cross-link the disabled adapter smoke wrapper and not-run request shape.
- `docs/BLK-014...`
  - Document `beo_publication: "DRAFT_ONLY"` and mapped disabled MCP PASS/FAIL projection.
- `docs/BLK-015...`
  - Document the public not-run builder and adapter smoke helper while retaining fail-closed Sprint 006 semantics.
- `README.md`
  - Add BLK-016 to active contract list.
  - State that Sprint 007 remains disabled/fixture-only and does not authorize live execution.

### TDD / docs RED gates

Before editing docs, add or run documentation probes that fail on the missing Sprint 007 contract:

```bash
python3 - <<'PY'
from pathlib import Path
p = Path('docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md')
if not p.exists():
    raise AssertionError('RED: BLK-016 Sprint 007 contract doc missing')
text = p.read_text()
for phrase in [
    'run_disabled_blk_test_mcp_adapter_smoke',
    'build_blk_test_mcp_not_run_request',
    'project_mapped_mcp_response_to_beo',
    'build_beo_rtm_interface_fixture',
    'live BLK-test MCP remains disabled',
    'RTM generation remains disabled',
    'authoritative BEO publication remains disabled',
    'sandbox/capability enforcement is later work',
    'approval-channel mechanics are later work',
]:
    assert phrase in text, f'BLK-016 missing phrase: {phrase}'
PY
```

Expected RED before doc creation:

```text
AssertionError: RED: BLK-016 Sprint 007 contract doc missing
```

### Documentation verification gates

Run these after docs are updated:

```bash
python3 - <<'PY'
from pathlib import Path
p = Path('docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md')
text = p.read_text()
for phrase in [
    'run_disabled_blk_test_mcp_adapter_smoke',
    'build_blk_test_mcp_not_run_request',
    'project_mapped_mcp_response_to_beo',
    'build_beo_rtm_interface_fixture',
    'live BLK-test MCP remains disabled',
    'RTM generation remains disabled',
    'authoritative BEO publication remains disabled',
    'sandbox/capability enforcement is later work',
    'approval-channel mechanics are later work',
]:
    assert phrase in text, f'BLK-016 missing phrase: {phrase}'
readme = Path('README.md').read_text()
assert 'BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md' in readme
print('BLK_016_CONTRACT_DOC_PASS')
PY

python3 - <<'PY'
from pathlib import Path
for path in [
    Path('docs/BLK-003_blk-pipe-blk-test-orchestration.md'),
    Path('docs/BLK-013_blk-test-handoff-fixture-contract.md'),
    Path('docs/BLK-014_blk-execution-outcome-fixture-shape.md'),
    Path('docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md'),
]:
    text = path.read_text()
    for phrase in [
        'live BLK-test MCP remains disabled',
        'RTM generation remains disabled',
    ]:
        assert phrase in text, f'{path} missing phrase: {phrase}'
print('SPRINT_007_ACTIVE_DOC_BOUNDARY_PASS')
PY

git diff --check
```

Also preserve Sprint 006 active-doctrine vocabulary gates:

```bash
python3 - <<'PY'
from pathlib import Path
import re
root = Path('.')
failures = []
for p in sorted((root / 'docs').glob('BLK-*.md')):
    text = p.read_text(errors='replace')
    status = next((line for line in text.splitlines()[:8] if line.startswith('**Status:**')), '')
    if 'Active' not in status:
        continue
    patterns = {
        'AAA_001': 'AAA_001',
        'ceb_id': 'ceb_id',
        'Codex Execution Brief': 'Codex Execution Brief',
        'traced_artifacts': 'traced_artifacts',
        'standalone CEB/CEBs': r'\bCEBs?\b',
        'standalone CEO/CEOs': r'\bCEOs?\b',
    }
    for label, pat in patterns.items():
        if label.startswith('standalone'):
            for m in re.finditer(pat, text):
                failures.append((str(p), label))
        elif pat in text:
            failures.append((str(p), label))
if failures:
    raise AssertionError(failures)
print('ACTIVE_DOC_VOCAB_PASS')
PY
```

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

### Outcome evidence

Create `docs/outcomes/BLK-PIPE-007_task-005-outcome.md` with:

- RED missing-doc evidence,
- doc update summary,
- BLK-016 contract gate output,
- active-doc boundary/vocabulary gate output,
- shared verification output.

### Commit message

```bash
git add docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md docs/BLK-003_blk-pipe-blk-test-orchestration.md docs/BLK-013_blk-test-handoff-fixture-contract.md docs/BLK-014_blk-execution-outcome-fixture-shape.md docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md README.md docs/outcomes/BLK-PIPE-007_task-005-outcome.md
git commit -m "docs: define blk-pipe sprint 007 fixture interfaces"
```

---

## 10. Task 6 — Sprint Closeout and Hostile Self-Review Gates

### Objective

Close Sprint 007 with evidence that the implementation stayed fixture-only and did not expand into live tactical execution, sandbox/capability enforcement, real approval-channel mechanics, RTM generation, or authoritative BEO publication.

### Files

Create:

- `docs/outcomes/BLK-PIPE-007_sprint-closeout.md`

Modify only if metadata gates expose a stale active header:

- `docs/outcomes/BLK-PIPE-007_task-001-outcome.md`
- `docs/outcomes/BLK-PIPE-007_task-002-outcome.md`
- `docs/outcomes/BLK-PIPE-007_task-003-outcome.md`
- `docs/outcomes/BLK-PIPE-007_task-004-outcome.md`
- `docs/outcomes/BLK-PIPE-007_task-005-outcome.md`

### Required closeout content

The closeout must include:

- final task-line implementation commit list,
- explicit statement that Sprint 007 did not run Codex, live LLMs, cyber tooling, live BLK-test MCP, RTM generation, or authoritative BEO publication,
- proof that sandbox/capability enforcement and real approval-channel mechanics remain future work,
- focused RED/GREEN evidence summary for Tasks 1-5,
- full verification output,
- metadata gate output,
- hostile self-review verdict.

### Required hostile self-review checks

Run after Task 5 and before closeout commit:

```bash
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
go run ./cmd/blk-pipe --health
git diff --check
```

Production-module no-live-import gate:

```bash
python3 - <<'PY'
from pathlib import Path
production_files = [
    Path('python/blk_orchestrator_gate.py'),
    Path('python/blk_test_mcp_adapter_smoke.py'),
    Path('python/blk_test_handoff_fixtures.py'),
    Path('python/beo_fixture_projection.py'),
    Path('python/beo_rtm_interface_fixtures.py'),
]
for path in production_files:
    text = path.read_text()
    forbidden = [
        'import socket',
        'from socket',
        'import subprocess',
        'from subprocess',
        'import requests',
        'from requests',
        'import urllib',
        'from urllib',
        'http.client',
        'mcp.Client',
        'codex',
        'OPENAI_API_KEY',
        'ANTHROPIC_API_KEY',
    ]
    for token in forbidden:
        assert token not in text, f'{path}: forbidden live-capability token {token!r}'
print('PRODUCTION_FIXTURE_NO_LIVE_IMPORTS_PASS')
PY
```

Authority-boundary fixture gate:

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, 'python')
from blk_orchestrator_gate import build_blk_test_mcp_request, build_blk_test_mcp_not_run_request
from blk_test_mcp_adapter_smoke import run_disabled_blk_test_mcp_adapter_smoke
from beo_fixture_projection import project_mapped_mcp_response_to_beo
from beo_rtm_interface_fixtures import build_beo_rtm_interface_fixture

trace = [{'kind': 'REQ', 'id': 'REQ-DRY-001', 'version_hash': 'sha256:' + 'a' * 64}]
success = {
    'status': 'SUCCESS',
    'beb_id': 'BEB_007',
    'commit_hash': 'abc123',
    'pre_engine_hash': 'def456',
    'staged_files': ['dry_run_output.txt'],
    'trace_artifacts': trace,
}
request = build_blk_test_mcp_request(success)
response = {
    'status': 'PASS',
    'beb_id': request['beb_id'],
    'commit_hash': request['commit_hash'],
    'pre_engine_hash': request['pre_engine_hash'],
    'trace_artifacts': request['trace_artifacts'],
    'checks': [{'name': 'fixture-output-present', 'status': 'PASS'}],
}
smoke = run_disabled_blk_test_mcp_adapter_smoke(success, response_fixture=response)
assert smoke['network_called'] is False
assert smoke['subprocess_called'] is False
mapped = smoke['mapped_response']
beo = project_mapped_mcp_response_to_beo(mapped, beo_id='BEO_007')
assert beo['beo_publication'] == 'DRAFT_ONLY'
assert beo['rtm_status'] == 'NOT_GENERATED'
interface = build_beo_rtm_interface_fixture(beo, interface_id='BEO_RTM_IFACE_007')
assert interface['rtm_status'] == 'NOT_GENERATED'
assert interface['rtm_authority'] == 'DISABLED_INTERFACE_ONLY'
assert 'rtm' not in interface
not_run = build_blk_test_mcp_not_run_request({
    'status': 'SYNTAX_GATE_FAILED',
    'beb_id': 'BEB_007',
    'commit_hash': '',
    'pre_engine_hash': 'def456',
    'staged_files': [],
    'trace_artifacts': trace,
})
assert not_run['method'] == 'blk_test.not_run'
print('SPRINT_007_AUTHORITY_BOUNDARY_FIXTURE_PASS')
PY
```

Outcome metadata gate:

```bash
python3 - <<'PY'
from pathlib import Path
sprint_prefix = 'BLK-PIPE-007'
for p in sorted(Path('docs/outcomes').glob(f'{sprint_prefix}*.md')):
    text = p.read_text()
    for line in text.splitlines()[:12]:
        if line.startswith('**Remote:**') and 'pending' in line.lower():
            raise AssertionError(f'{p}: stale pending remote metadata: {line}')
print('OUTCOME_REMOTE_METADATA_PASS')
PY
```

Active-doc vocabulary gate from Task 5 must also pass.

### Closeout RED gate

Before creating the closeout doc, run:

```bash
python3 - <<'PY'
from pathlib import Path
p = Path('docs/outcomes/BLK-PIPE-007_sprint-closeout.md')
if not p.exists():
    raise AssertionError('RED: Sprint 007 closeout doc missing')
PY
```

Expected RED:

```text
AssertionError: RED: Sprint 007 closeout doc missing
```

### Commit message

```bash
git add docs/outcomes/BLK-PIPE-007_sprint-closeout.md docs/outcomes/BLK-PIPE-007_task-*.md
git commit -m "docs: close out blk-pipe sprint 007"
```

---

## 11. Final Sprint Acceptance Criteria

Sprint 007 is complete only when all of the following are true:

- Disabled BLK-test MCP adapter smoke helper exists and proves both disabled-send and source-bound PASS/FAIL mapping paths.
- Non-success BLK-pipe reports have an explicit `blk_test.not_run` disabled request shape.
- Non-success source context cannot map PASS/FAIL responses.
- Source-bound mapped PASS/FAIL disabled MCP fixtures can project into draft BEO fixture shape.
- Mapped BLOCKED/not-run fixture output cannot project into BEO verdict output.
- Every BEO fixture states `beo_publication: DRAFT_ONLY` and `rtm_status: NOT_GENERATED`.
- BEO/RTM interface fixture exists, preserves trace artifacts, and explicitly states `rtm_authority: DISABLED_INTERFACE_ONLY`.
- No helper reads protected BLK-req vault files.
- No helper imports or uses live network/subprocess/MCP/model/cyber capabilities.
- Active docs and README describe Sprint 007 without live-authority drift.
- Task outcome docs and sprint closeout exist with RED/GREEN verification evidence.
- Full verification passes:

  ```bash
  python3 -m unittest discover -s python -p 'test_*.py'
  go test ./...
  go vet ./...
  go run ./cmd/blk-pipe --health
  git diff --check
  ```

- `git status --short --branch` is clean/aligned after push.

---

## 12. Explicit Future Work Not Authorized Here

Do not fold these into Sprint 007:

1. Sandbox/capability enforcement for live tactical execution.
2. Real approval-channel mechanics, user identity binding, replay protection, or approval revocation.
3. Live Codex execution.
4. Live BLK-test MCP transport.
5. Live LLM or network model execution.
6. Cyber execution or target interaction.
7. RTM generation, requirement-hash comparison against protected vaults, or drift rejection authority.
8. Authoritative BEO publication or BLK-req promotion.

Those require a later sprint plan with explicit approval, mechanical enforcement design, and hostile pre-review before implementation.
