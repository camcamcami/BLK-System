# blk-system-011 — Disabled BLK-test MCP Transport Skeleton and Non-Executing Handshake Gate

> **For Hermes:** Use `blk-system-sprint-execution` to implement this plan task-by-task. Use strict RED/GREEN gates for code and documentation artifacts. This sprint is a deterministic local implementation-and-contract sprint for a disabled transport skeleton only. Do not use Hindsight. Do not run live Codex, live tactical LLMs, network model services, cyber tooling, live fixed-tool BLK-test execution, RTM generation, RTM authority, active BLK-req vault reads, or authoritative BEO publication.

**Sprint ID:** `blk-system-011` / `BLK-SYSTEM-011`
**Component emphasis:** BLK-test MCP disabled transport lifecycle and non-executing handshake safety gates, not a `blk-pipe` component sprint.
**Goal:** Create a dependency-free disabled BLK-test MCP transport skeleton and persistent gates proving stdio-only, disabled-by-default, no-test-execution behavior before later workspace/process/approval sprints.

**Architecture:** Sprint 011 implements a local Python contract/probe harness for the future BLK-test MCP transport boundary. The harness produces deterministic transport descriptors, startup refusals, non-executing handshake evidence, lifecycle/shutdown evidence, and fixed-tool registry metadata without opening sockets, spawning subprocesses, launching an MCP server, executing tests, mutating source, publishing BEOs, or generating RTM. A later sprint may replace or extend this with a real TypeScript MCP SDK server only after Sprint 012 workspace/process controls and Sprint 013 approval/source-evidence binding are accepted.

**Tech Stack:** Markdown review/design artifacts, dependency-free Python `unittest` gates, existing BLK-System Python fixture modules, Go verification for `blk-pipe` regression guard only.

---

## 0. Current Known State

Repository:

```text
/home/dad/BLK-System
```

Planning preflight when this document was authored:

```text
date                         -> 2026-05-06 11:26:10 AEST
git status --short --branch  -> ## main...origin/main
HEAD                         -> 714d8b7 docs: close out blk-system sprint 010
```

Sprint 010 source seed:

```text
BLK-SYSTEM-011 — Disabled BLK-test MCP Live-Transport Skeleton and Non-Executing Handshake Gate
```

Naming correction preserved:

- This is a system-level BLK-test MCP readiness sprint, so use `BLK-SYSTEM-011` / `blk-system-011`.
- Do not name this sprint `BLK-PIPE-011`; it is not scoped to the `blk-pipe` component.
- Do not name this sprint `BEB_011`; `BEB` is an artifact type and `beb_id` is a trace/source field, not a sprint namespace.

Source doctrine and review artifacts to align:

```text
docs/BLK-001_blk-system-master-architecture.md
docs/BLK-003_blk-pipe-blk-test-orchestration.md
docs/BLK-008_blk-test-mcp-execution-server.md
docs/BLK-013_blk-test-handoff-fixture-contract.md
docs/BLK-014_blk-execution-outcome-fixture-shape.md
docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md
docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md
docs/outcomes/BLK-SYSTEM-010_sprint-closeout.md
docs/reviews/BLK-SYSTEM-010_fixture-to-live-gap-register.md
docs/reviews/BLK-SYSTEM-010_approval-and-authority-decision-register.md
docs/reviews/BLK-SYSTEM-010_sandbox-capability-readiness-spec.md
docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md
python/blk_test_mcp_adapter_smoke.py
python/test_blk_test_mcp_adapter_smoke.py
python/test_active_doctrine_review_gates.py
```

---

## 1. BLK-001 Alignment Contract

Sprint 011 must preserve BLK-001's isolated-domain model:

| BLK-001 domain | Intent to preserve | Sprint 011 implication |
| --- | --- | --- |
| `blk-req` Legislative Gateway | Requirements/use cases remain HITL-authorized immutable active-vault artifacts. | Do not read protected BLK-req vault bodies, parse requirement bodies, or infer law from `docs/active/`, `docs/requirements/`, or `docs/use_cases/`. |
| Architecture & Feature Planning | Hermes plans bounded work and produces BEB/L2 payloads; BLK-test is not architect/router. | Sprint 011 may define transport boundary contracts only; it must not make BLK-test choose scope, architecture, or requirement interpretation. |
| `blk-pipe` Blast Shield & Forge | `blk-pipe` owns deterministic source mutation, staging, Git allowlists, and forge/blast-shield authority. | The transport skeleton must not mutate source, stage files, commit, or replace `blk-pipe`. |
| `blk-test` Physics Oracle | BLK-test verifies physical reality and returns bounded evidence. | Sprint 011 may define a disabled stdio transport skeleton and handshake refusal; it must not execute fixed-tool tests. |
| RTM Aggregator Ledger | RTM remains a separate offline ledger comparing BEO trace hashes against active-vault hashes. | Sprint 011 must not generate RTM, imply RTM generation, or grant RTM drift rejection authority. |
| Cryptographic baton | `version_hash` is the bridge across domains. | Where source evidence is referenced, preserve canonical `trace_artifacts[*].version_hash == sha256:<64-lowercase-hex>` and keep evidence opaque/source-bound. |

Sprint 011 passes alignment only if every implementation and review artifact says what authority it does **not** grant.

---

## 2. Decision Register

| Decision ID | Question | Decision | Rationale | Implementation effect |
| --- | --- | --- | --- | --- |
| DEC-001 | Is Sprint 011 a `blk-pipe` sprint? | **No. It is `BLK-SYSTEM-011`.** | The scope crosses BLK-test transport, approval, evidence, BEO, RTM, and active-vault boundaries. | Use `BLK-SYSTEM-011` prefixes for review/outcome docs and `blk-system-011` plan naming. |
| DEC-002 | Does Sprint 011 authorize live BLK-test MCP? | **No.** | Sprint 010 explicitly sliced 011 as disabled and non-executing. | Startup defaults to refused/blocked; no live MCP server/client is launched. |
| DEC-003 | Does Sprint 011 install or run the TypeScript MCP SDK? | **No.** | The repo currently has no Node package boundary for BLK-test MCP, and package/SDK startup risks authority drift. | Implement dependency-free Python contract/probe skeleton only. A later sprint may introduce TypeScript SDK after prerequisite gates. |
| DEC-004 | Does Sprint 011 implement approval mechanics? | **No.** | Sprint 013 owns human approval and source-evidence authorization mechanics. | Any approval-looking input is recorded as unsupported future authority and still blocked. |
| DEC-005 | Does Sprint 011 implement workspace/process controls? | **No.** | Sprint 012 owns workspace clone/isolation, process kill, timeout, flood, and teardown mechanics. | Lifecycle probes are non-executing descriptors only; no child processes or workspaces are created. |
| DEC-006 | May Sprint 011 define a fixed tool registry? | **Yes, as metadata only.** | A fixed registry is needed before transport can be reviewed, but execution remains blocked. | Registry descriptors are static and non-executable; all tool execution attempts raise/block. |
| DEC-007 | May Sprint 011 touch active doctrine? | **Yes, narrowly.** | The disabled transport skeleton should be discoverable as current active disabled contract. | Create `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md` and cross-link BLK-008/015/016 only if deterministic gates require it. |

---

## 3. Non-Goals and Hard Blocks

Sprint 011 must not implement, invoke, or imply:

- live BLK-test MCP transport;
- live MCP client/server startup;
- live fixed-tool test execution;
- arbitrary shell, `exec`, dynamic command execution, plugin-discovered tools, auto-fix, source-write, stage, or commit tools;
- authoritative BLK-test verdict authority;
- authoritative BEO publication;
- RTM generation;
- RTM drift rejection authority;
- active BLK-req vault reads or requirement-body parsing;
- live Codex execution;
- live tactical LLM API calls;
- network model services;
- cyber tooling or cyber execution;
- execution against real cyber-program repositories or live targets;
- production sandbox/container/cgroup/VM enforcement claims;
- production host-secret isolation claims;
- production approval-channel mechanics;
- package-manager network installs, new external dependencies, or SDK startup.

Allowed work:

```text
dependency-free Python contract/probe code
Python unittest RED/GREEN gates
static transport descriptor metadata
non-executing handshake refusal descriptors
fixed tool registry metadata with no executor
Markdown active disabled-contract doctrine
Markdown review/outcome/closeout artifacts
```

---

## 4. Invariants to Preserve

1. BLK-System sprint naming uses `BLK-SYSTEM-###` / `blk-system-###` for system-level work.
2. `BEB` and `BEO` are artifact types, not sprint IDs.
3. The disabled transport skeleton is stdio-only metadata; no HTTP, WebSocket, TCP, UDP, daemon, or listener behavior.
4. Default startup is disabled and fail-closed.
5. Any `enabled=True`, approval-token, or future-approval path still blocks in Sprint 011.
6. No server process starts, no client process starts, no subprocess is spawned, no network is called, and no tests execute.
7. Fixed tool registry entries are descriptors only; there is no arbitrary shell and no dynamic command execution tool.
8. Source mutation, staging, commit, BEO publication, RTM generation, active-vault reads, and cyber execution remain unavailable.
9. Lifecycle/shutdown probes are deterministic data-shape probes only; Sprint 012 owns real process/workspace controls.
10. Every outcome document records RED/GREEN evidence and the explicit non-execution statement.
11. Remove `python/__pycache__` before exact-path staging.
12. Do not use `git add .`, `git add -u`, `git stash`, broad staging, or broad revert operations.
13. Do not push until sprint closeout unless the human explicitly asks.

---

## 5. Controller Workflow for Each Task

For each task:

1. Preflight:

   ```bash
   cd /home/dad/BLK-System
   export PATH="$HOME/.local/bin:$PATH"
   git status --short --branch
   ```

2. Read the task's exact source docs before editing.
3. Add the focused RED gate first.
4. Run the focused test and capture expected RED.
5. Patch only the files named in the task.
6. Rerun the focused test for GREEN.
7. Create the matching outcome document:

   ```text
   docs/outcomes/BLK-SYSTEM-011_task-00N-outcome.md
   ```

8. Run shared verification before each implementation commit:

   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   python3 -m unittest discover -s python -p 'test_*.py'
   go test ./...
   go vet ./...
   git diff --check
   ```

9. Remove generated Python caches before staging:

   ```bash
   rm -rf python/__pycache__
   ```

10. Stage only exact task files and commit with the task's listed commit message.
11. Do not push until closeout unless the human explicitly requests it.

---

## 6. Task 1 — Add Sprint 011 Transport Boundary Review Gate

### Objective

Create the governing Sprint 011 review artifact and persistent doctrine gate proving the sprint is disabled/non-executing and BLK-001-aligned before writing transport skeleton code.

### Files

Create:

- `docs/reviews/BLK-SYSTEM-011_transport-boundary-review.md`
- `docs/outcomes/BLK-SYSTEM-011_task-001-outcome.md`

Modify:

- `python/test_active_doctrine_review_gates.py`

### Required behavior

The review artifact must include:

- `BLK-SYSTEM-011`;
- `disabled BLK-test MCP transport skeleton`;
- `non-executing handshake gate`;
- `stdio-only`;
- `disabled by default`;
- `does not authorize live BLK-test MCP`;
- `does not authorize live MCP client/server startup`;
- `does not execute fixed-tool tests`;
- `does not authorize authoritative BEO publication`;
- `does not authorize RTM generation`;
- `does not authorize RTM drift rejection authority`;
- `does not read protected BLK-req vault bodies`;
- `must not mutate source`;
- `must not grant arbitrary shell`;
- `Sprint 012 owns workspace/process controls`;
- `Sprint 013 owns approval/source-evidence authorization mechanics`.

### TDD steps

#### Step 1 — RED: add the review artifact gate

Add constants and a test similar to:

```python
SPRINT011_TRANSPORT_REVIEW = ROOT / "docs" / "reviews" / "BLK-SYSTEM-011_transport-boundary-review.md"


def test_sprint011_transport_boundary_review_is_disabled_and_non_executing(self):
    self.assertTrue(SPRINT011_TRANSPORT_REVIEW.exists(), "Sprint 011 transport boundary review missing")
    text = SPRINT011_TRANSPORT_REVIEW.read_text()
    required = [
        "BLK-SYSTEM-011",
        "disabled BLK-test MCP transport skeleton",
        "non-executing handshake gate",
        "stdio-only",
        "disabled by default",
        "does not authorize live BLK-test MCP",
        "does not authorize live MCP client/server startup",
        "does not execute fixed-tool tests",
        "does not authorize authoritative BEO publication",
        "does not authorize RTM generation",
        "does not authorize RTM drift rejection authority",
        "does not read protected BLK-req vault bodies",
        "must not mutate source",
        "must not grant arbitrary shell",
        "Sprint 012 owns workspace/process controls",
        "Sprint 013 owns approval/source-evidence authorization mechanics",
    ]
    missing = [marker for marker in required if marker not in text]
    self.assertEqual(missing, [], f"Sprint 011 transport-boundary markers missing: {missing}")
```

Run:

```bash
python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v
```

Expected RED: fails because `BLK-SYSTEM-011_transport-boundary-review.md` does not exist.

#### Step 2 — GREEN: write the review artifact

Create `docs/reviews/BLK-SYSTEM-011_transport-boundary-review.md` with sections:

1. Scope and source documents.
2. BLK-001 domain preservation matrix.
3. Sprint 011 authority-denied list.
4. Dependency-free disabled transport approach.
5. Handoff boundaries to Sprint 012 and Sprint 013.
6. Pass/fail criteria.

#### Step 3 — outcome and shared verification

Create `docs/outcomes/BLK-SYSTEM-011_task-001-outcome.md` with RED/GREEN evidence and non-execution statement.

Run shared verification.

#### Step 4 — commit

```bash
git add python/test_active_doctrine_review_gates.py \
  docs/reviews/BLK-SYSTEM-011_transport-boundary-review.md \
  docs/outcomes/BLK-SYSTEM-011_task-001-outcome.md
git commit -m "docs: add blk-system sprint 011 transport boundary gate"
```

---

## 7. Task 2 — Implement Disabled Startup Preflight Skeleton

### Objective

Add dependency-free Python code that represents the disabled BLK-test MCP startup boundary and proves startup is blocked by default without launching any live transport.

### Files

Create:

- `python/blk_test_mcp_disabled_transport.py`
- `python/test_blk_test_mcp_disabled_transport.py`
- `docs/outcomes/BLK-SYSTEM-011_task-002-outcome.md`

### Required API

Implement public functions:

```python
def build_disabled_transport_descriptor(
    *,
    transport: str = "stdio",
    enabled: bool = False,
    requested_profile: str = "strict-ci",
    approval_record: dict[str, object] | None = None,
) -> dict[str, object]:
    """Return a static disabled BLK-test MCP transport descriptor."""


def evaluate_disabled_transport_startup(descriptor: dict[str, object]) -> dict[str, object]:
    """Return a fail-closed startup decision without launching a server/client."""
```

Required descriptor fields:

```text
component = "blk-test-mcp-disabled-transport"
transport = "stdio"
enabled = False
startup_status = "DISABLED_BY_DEFAULT"
live_mcp_authorized = False
server_started = False
client_started = False
network_called = False
subprocess_called = False
tools_executed = []
rtm_status = "NOT_GENERATED"
beo_publication = "DRAFT_ONLY"
active_vault_read = False
source_mutation_allowed = False
reason includes "does not authorize live BLK-test MCP"
```

Startup decision behavior:

| Input | Expected result |
| --- | --- |
| default descriptor | returns `decision: "STARTUP_BLOCKED_DISABLED"`, all live side-effect booleans false |
| `enabled=True` descriptor request | raises or returns `STARTUP_BLOCKED_UNAUTHORIZED_ENABLE_REQUEST`; no side effects |
| non-`stdio` transport | rejects with `ValueError` mentioning `stdio-only` |
| approval-looking record | still blocks with `STARTUP_BLOCKED_APPROVAL_NOT_IMPLEMENTED`; Sprint 013 owns approval mechanics |

### TDD steps

#### Step 1 — RED: create tests first

Create `python/test_blk_test_mcp_disabled_transport.py` with tests similar to:

```python
import unittest

from blk_test_mcp_disabled_transport import (
    build_disabled_transport_descriptor,
    evaluate_disabled_transport_startup,
)


class DisabledTransportStartupTest(unittest.TestCase):
    def test_default_descriptor_is_stdio_only_disabled_and_non_executing(self):
        descriptor = build_disabled_transport_descriptor()

        self.assertEqual(descriptor["component"], "blk-test-mcp-disabled-transport")
        self.assertEqual(descriptor["transport"], "stdio")
        self.assertFalse(descriptor["enabled"])
        self.assertFalse(descriptor["live_mcp_authorized"])
        self.assertFalse(descriptor["server_started"])
        self.assertFalse(descriptor["client_started"])
        self.assertFalse(descriptor["network_called"])
        self.assertFalse(descriptor["subprocess_called"])
        self.assertEqual(descriptor["tools_executed"], [])
        self.assertEqual(descriptor["rtm_status"], "NOT_GENERATED")
        self.assertEqual(descriptor["beo_publication"], "DRAFT_ONLY")
        self.assertFalse(descriptor["active_vault_read"])
        self.assertFalse(descriptor["source_mutation_allowed"])
        self.assertIn("does not authorize live BLK-test MCP", descriptor["reason"])

    def test_startup_decision_blocks_default_descriptor_without_side_effects(self):
        decision = evaluate_disabled_transport_startup(build_disabled_transport_descriptor())

        self.assertEqual(decision["decision"], "STARTUP_BLOCKED_DISABLED")
        self.assertFalse(decision["server_started"])
        self.assertFalse(decision["client_started"])
        self.assertFalse(decision["network_called"])
        self.assertFalse(decision["subprocess_called"])
        self.assertEqual(decision["tools_executed"], [])

    def test_non_stdio_transport_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "stdio-only"):
            build_disabled_transport_descriptor(transport="http")

    def test_enabled_request_is_blocked_not_started(self):
        with self.assertRaisesRegex(RuntimeError, "disabled"):
            build_disabled_transport_descriptor(enabled=True)

    def test_approval_record_does_not_enable_transport_in_sprint011(self):
        descriptor = build_disabled_transport_descriptor(
            approval_record={"operator": "human", "approved": True}
        )
        decision = evaluate_disabled_transport_startup(descriptor)

        self.assertEqual(decision["decision"], "STARTUP_BLOCKED_APPROVAL_NOT_IMPLEMENTED")
        self.assertFalse(decision["server_started"])
        self.assertFalse(decision["client_started"])
```

Run:

```bash
python3 -m unittest discover -s python -p 'test_blk_test_mcp_disabled_transport.py' -v
```

Expected RED: import/module failure because implementation does not exist.

#### Step 2 — GREEN: implement minimal descriptor/preflight code

Create `python/blk_test_mcp_disabled_transport.py` with no external dependencies, no `socket`, no `subprocess`, no `os.system`, no filesystem mutation, and no imports outside standard typing/copy if needed.

Minimal implementation must validate:

- `transport == "stdio"`;
- `enabled is False`;
- if `approval_record` is present, record that approval mechanics are not implemented and startup remains blocked.

#### Step 3 — source-scan safety gate

Add tests that scan the implementation source and reject forbidden imports/strings:

```python
def test_disabled_transport_module_does_not_import_live_execution_surfaces(self):
    text = Path(__file__).with_name("blk_test_mcp_disabled_transport.py").read_text()
    forbidden = ["import socket", "from socket", "subprocess", "Popen", "os.system", "requests", "http.server"]
    offenders = [marker for marker in forbidden if marker in text]
    self.assertEqual(offenders, [])
```

#### Step 4 — outcome and shared verification

Create Task 2 outcome and run shared verification.

#### Step 5 — commit

```bash
git add python/blk_test_mcp_disabled_transport.py \
  python/test_blk_test_mcp_disabled_transport.py \
  docs/outcomes/BLK-SYSTEM-011_task-002-outcome.md
git commit -m "test: add disabled blk-test mcp transport startup gate"
```

---

## 8. Task 3 — Add Non-Executing Handshake and Lifecycle Probes

### Objective

Extend the disabled transport skeleton with deterministic handshake/lifecycle evidence that proves no MCP handshake, server process, client process, tool call, or test execution occurs in Sprint 011.

### Files

Modify:

- `python/blk_test_mcp_disabled_transport.py`
- `python/test_blk_test_mcp_disabled_transport.py`

Create:

- `docs/outcomes/BLK-SYSTEM-011_task-003-outcome.md`

### Required API

Add public functions:

```python
def build_non_executing_handshake_probe(descriptor: dict[str, object]) -> dict[str, object]:
    """Return deterministic evidence that handshake is blocked before transport startup."""


def build_disabled_lifecycle_probe(descriptor: dict[str, object], *, event: str = "startup_refused") -> dict[str, object]:
    """Return deterministic lifecycle/shutdown evidence without processes or workspaces."""
```

Required behavior:

- `build_non_executing_handshake_probe(...)` returns:
  - `handshake_status: "HANDSHAKE_NOT_ATTEMPTED_DISABLED"`;
  - `jsonrpc_initialized: False`;
  - `server_started: False`;
  - `client_started: False`;
  - `tools_listed: False`;
  - `tools_executed: []`;
  - `tests_executed: []`;
  - `network_called: False`;
  - `subprocess_called: False`.
- `build_disabled_lifecycle_probe(...)` supports at least:
  - `startup_refused`;
  - `operator_shutdown_noop`;
  - `config_rejected`.
- Lifecycle output must include ordered events but no process IDs, workspaces, or child process metadata because none are created in Sprint 011.
- Unknown lifecycle events reject deterministically.

### TDD steps

#### Step 1 — RED: add handshake/lifecycle tests

Add tests similar to:

```python
def test_non_executing_handshake_never_initializes_jsonrpc_or_lists_tools(self):
    probe = build_non_executing_handshake_probe(build_disabled_transport_descriptor())

    self.assertEqual(probe["handshake_status"], "HANDSHAKE_NOT_ATTEMPTED_DISABLED")
    self.assertFalse(probe["jsonrpc_initialized"])
    self.assertFalse(probe["server_started"])
    self.assertFalse(probe["client_started"])
    self.assertFalse(probe["tools_listed"])
    self.assertEqual(probe["tools_executed"], [])
    self.assertEqual(probe["tests_executed"], [])
    self.assertFalse(probe["network_called"])
    self.assertFalse(probe["subprocess_called"])


def test_disabled_lifecycle_probe_records_shutdown_noop_without_processes(self):
    probe = build_disabled_lifecycle_probe(
        build_disabled_transport_descriptor(),
        event="operator_shutdown_noop",
    )

    self.assertEqual(probe["lifecycle_status"], "NOOP_SHUTDOWN_RECORDED")
    self.assertEqual(probe["process_ids"], [])
    self.assertEqual(probe["workspace_paths"], [])
    self.assertFalse(probe["server_started"])
    self.assertFalse(probe["client_started"])
```

Run focused test and capture RED because functions are missing.

#### Step 2 — GREEN: implement probes minimally

Patch `python/blk_test_mcp_disabled_transport.py` to return static deterministic dictionaries. Do not add live imports or filesystem/process calls.

#### Step 3 — outcome and shared verification

Create Task 3 outcome and run shared verification.

#### Step 4 — commit

```bash
git add python/blk_test_mcp_disabled_transport.py \
  python/test_blk_test_mcp_disabled_transport.py \
  docs/outcomes/BLK-SYSTEM-011_task-003-outcome.md
git commit -m "test: gate non-executing blk-test mcp handshake lifecycle"
```

---

## 9. Task 4 — Add Fixed Tool Registry Metadata and No-Arbitrary-Shell Gate

### Objective

Define a static fixed-tool registry descriptor for future BLK-test MCP tools while proving Sprint 011 cannot execute tools, run shell commands, mutate source, publish BEOs, or generate RTM.

### Files

Modify:

- `python/blk_test_mcp_disabled_transport.py`
- `python/test_blk_test_mcp_disabled_transport.py`

Create:

- `docs/outcomes/BLK-SYSTEM-011_task-004-outcome.md`

### Required API

Add public functions:

```python
def fixed_tool_registry_descriptor() -> list[dict[str, object]]:
    """Return static metadata for future fixed BLK-test MCP tools."""


def evaluate_disabled_tool_execution(tool_name: str, *, arguments: dict[str, object] | None = None) -> dict[str, object]:
    """Always block tool execution in Sprint 011."""
```

Allowed metadata-only tool names:

```text
run_ast_validation
run_ipc_race_test
run_svg_export_purity_test
run_architecture_lint
```

Each descriptor must include:

```text
name
status = "DESCRIPTOR_ONLY"
executor_available = False
requires_future_workspace_controls = True
requires_future_approval_controls = True
source_mutation_allowed = False
beo_publication_allowed = False
rtm_generation_allowed = False
active_vault_read_allowed = False
```

Forbidden tool names/markers:

```text
shell
exec
run_command
bash
python
node
npm
curl
wget
git_write
stage
commit
autofix
publish_beo
generate_rtm
read_active_vault
```

### TDD steps

#### Step 1 — RED: add fixed-registry tests

Add tests similar to:

```python
def test_fixed_tool_registry_is_descriptor_only_and_has_no_arbitrary_shell(self):
    registry = fixed_tool_registry_descriptor()
    names = {entry["name"] for entry in registry}

    self.assertEqual(
        names,
        {
            "run_ast_validation",
            "run_ipc_race_test",
            "run_svg_export_purity_test",
            "run_architecture_lint",
        },
    )
    forbidden = {"shell", "exec", "run_command", "bash", "publish_beo", "generate_rtm", "read_active_vault"}
    self.assertTrue(names.isdisjoint(forbidden))
    for entry in registry:
        self.assertEqual(entry["status"], "DESCRIPTOR_ONLY")
        self.assertFalse(entry["executor_available"])
        self.assertFalse(entry["source_mutation_allowed"])
        self.assertFalse(entry["beo_publication_allowed"])
        self.assertFalse(entry["rtm_generation_allowed"])
        self.assertFalse(entry["active_vault_read_allowed"])


def test_disabled_tool_execution_always_blocks_even_for_known_tool(self):
    result = evaluate_disabled_tool_execution("run_ast_validation", arguments={})

    self.assertEqual(result["decision"], "TOOL_EXECUTION_BLOCKED_DISABLED")
    self.assertFalse(result["subprocess_called"])
    self.assertFalse(result["network_called"])
    self.assertEqual(result["tests_executed"], [])
```

Run focused test and capture RED because functions are missing.

#### Step 2 — GREEN: implement descriptor-only registry

Patch the implementation. Keep the registry pure-data only.

#### Step 3 — add source-scan gate for forbidden strings

Extend source scan to reject actual executable surfaces while avoiding false positives from test labels. Scan implementation file only.

#### Step 4 — outcome and shared verification

Create Task 4 outcome and run shared verification.

#### Step 5 — commit

```bash
git add python/blk_test_mcp_disabled_transport.py \
  python/test_blk_test_mcp_disabled_transport.py \
  docs/outcomes/BLK-SYSTEM-011_task-004-outcome.md
git commit -m "test: define disabled blk-test mcp fixed tool registry"
```

---

## 10. Task 5 — Add Active Disabled-Transport Doctrine and Cross-Reference Gate

### Objective

Make Sprint 011's disabled transport skeleton discoverable in active doctrine without implying live MCP authorization.

### Files

Create:

- `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md`
- `docs/outcomes/BLK-SYSTEM-011_task-005-outcome.md`

Modify:

- `docs/BLK-008_blk-test-mcp-execution-server.md`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`
- `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`
- `python/test_active_doctrine_review_gates.py`

### Required behavior

`BLK-017` must state:

- `**Status:** Active disabled transport contract`;
- Sprint 011 is `disabled by default`;
- Sprint 011 is `stdio-only` metadata/probe work;
- Sprint 011 has a `non-executing handshake gate`;
- Sprint 011 `does not authorize live BLK-test MCP`;
- Sprint 011 `does not authorize live MCP client/server startup`;
- Sprint 011 `does not execute fixed-tool tests`;
- Sprint 011 `does not authorize authoritative BEO publication`;
- Sprint 011 `does not authorize RTM generation`;
- Sprint 011 `does not authorize RTM drift rejection authority`;
- Sprint 011 `does not read protected BLK-req vault bodies`;
- Sprint 011 `must not mutate source`;
- Sprint 011 `must not grant arbitrary shell`;
- `Sprint 012 owns workspace/process controls`;
- `Sprint 013 owns approval/source-evidence authorization mechanics`.

Cross-reference patches:

- BLK-008 §0 should include `BLK-017` in the current disabled/fixture-only cross-reference list.
- BLK-015 should mention that Sprint 011 adds disabled transport skeleton descriptors but no approval/live startup.
- BLK-016 future-work boundary should mention BLK-017 as the disabled transport skeleton contract.

### TDD steps

#### Step 1 — RED: add active doctrine gate

Add constants and a test similar to:

```python
BLK017 = ROOT / "docs" / "BLK-017_blk-test-mcp-disabled-transport-skeleton.md"


def test_blk017_records_disabled_transport_skeleton_without_live_authority(self):
    self.assertTrue(BLK017.exists(), "BLK-017 disabled transport skeleton doctrine missing")
    text = BLK017.read_text()
    required = [
        "**Status:** Active disabled transport contract",
        "disabled by default",
        "stdio-only",
        "non-executing handshake gate",
        "does not authorize live BLK-test MCP",
        "does not authorize live MCP client/server startup",
        "does not execute fixed-tool tests",
        "does not authorize authoritative BEO publication",
        "does not authorize RTM generation",
        "does not authorize RTM drift rejection authority",
        "does not read protected BLK-req vault bodies",
        "must not mutate source",
        "must not grant arbitrary shell",
        "Sprint 012 owns workspace/process controls",
        "Sprint 013 owns approval/source-evidence authorization mechanics",
    ]
    missing = [marker for marker in required if marker not in text]
    self.assertEqual(missing, [], f"BLK-017 disabled transport markers missing: {missing}")
```

Add a cross-reference gate similar to:

```python
def test_blk008_015_016_cross_reference_blk017_without_live_authority(self):
    docs = [BLK008, BLK015, BLK016]
    missing = []
    for path in docs:
        text = path.read_text()
        for marker in [
            "BLK-017",
            "does not authorize live BLK-test MCP",
            "does not authorize RTM generation",
            "does not authorize authoritative BEO publication",
        ]:
            if marker not in text:
                missing.append(f"{path.relative_to(ROOT)} missing {marker}")
    self.assertEqual(missing, [])
```

Run focused gate and capture RED because BLK-017/cross-references are missing.

#### Step 2 — GREEN: write BLK-017 and patch cross-references

Create `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md` with sections:

1. Purpose.
2. Current authority boundary.
3. Disabled startup preflight shape.
4. Non-executing handshake/lifecycle evidence.
5. Fixed tool registry descriptor-only rule.
6. Prohibited authority list.
7. Future-work handoff to Sprint 012/013/014.
8. Implementation and tests.

Patch only small current-boundary/cross-reference paragraphs in BLK-008, BLK-015, and BLK-016.

#### Step 3 — outcome and shared verification

Create Task 5 outcome and run shared verification.

#### Step 4 — commit

```bash
git add python/test_active_doctrine_review_gates.py \
  docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md \
  docs/BLK-008_blk-test-mcp-execution-server.md \
  docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md \
  docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md \
  docs/outcomes/BLK-SYSTEM-011_task-005-outcome.md
git commit -m "docs: define disabled blk-test mcp transport contract"
```

---

## 11. Task 6 — Closeout and Future Sprint Seed

### Objective

Close Sprint 011 with audit-grade evidence, explicit non-execution statements, and a narrow next-sprint seed for workspace/process/resource controls.

### Files

Create:

- `docs/outcomes/BLK-SYSTEM-011_sprint-closeout.md`

No code changes unless final verification reveals a doc/gate defect.

### Required closeout content

The closeout must include:

- BLK-001 alignment verdict;
- task commit table;
- created/modified files list;
- RED/GREEN evidence summary for Tasks 1-5;
- final verification evidence;
- explicit non-execution statement;
- remaining blocked scope before live BLK-test MCP;
- recommended next sprint seed:

```text
BLK-SYSTEM-012 — Workspace Isolation and Process-Control Implementation Probes
```

The closeout must explicitly say Sprint 011 did not:

- authorize live BLK-test MCP;
- start a live MCP server/client;
- execute fixed-tool tests;
- spawn subprocesses for BLK-test;
- open network sockets or HTTP/WebSocket transports;
- mutate source, stage files, or commit via BLK-test;
- publish authoritative BEOs;
- generate RTM;
- grant RTM drift rejection authority;
- read active BLK-req vault bodies;
- implement approval-channel mechanics;
- claim production sandbox/cgroup/VM/host-secret isolation.

### TDD steps

#### Step 1 — RED: missing closeout gate

Run a small closeout gate before creating the file:

```bash
python3 - <<'PY'
from pathlib import Path
path = Path('docs/outcomes/BLK-SYSTEM-011_sprint-closeout.md')
assert path.exists(), 'RED: Sprint 011 closeout doc missing'
PY
```

Expected RED:

```text
AssertionError: RED: Sprint 011 closeout doc missing
```

#### Step 2 — GREEN: create closeout

Create the closeout document and run a content gate:

```bash
python3 - <<'PY'
from pathlib import Path
path = Path('docs/outcomes/BLK-SYSTEM-011_sprint-closeout.md')
text = path.read_text()
required = [
    'BLK-SYSTEM-011',
    'BLK-001 alignment verdict',
    'does not authorize live BLK-test MCP',
    'does not authorize live MCP client/server startup',
    'does not execute fixed-tool tests',
    'does not authorize authoritative BEO publication',
    'does not authorize RTM generation',
    'BLK-SYSTEM-012',
]
missing = [marker for marker in required if marker not in text]
assert not missing, missing
print('SPRINT011_CLOSEOUT_CONTENT_PASS')
PY
```

#### Step 3 — final verification

Run:

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
rm -rf python/__pycache__
git status --short --branch
```

#### Step 4 — commit

```bash
git add docs/outcomes/BLK-SYSTEM-011_sprint-closeout.md
git commit -m "docs: close out blk-system sprint 011"
```

Do not push unless the human explicitly requests it.

---

## 12. Expected File Summary

Expected new files:

```text
docs/plans/blk-system-011_disabled-blk-test-mcp-transport-skeleton.md
docs/reviews/BLK-SYSTEM-011_transport-boundary-review.md
docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md
docs/outcomes/BLK-SYSTEM-011_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-011_task-002-outcome.md
docs/outcomes/BLK-SYSTEM-011_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-011_task-004-outcome.md
docs/outcomes/BLK-SYSTEM-011_task-005-outcome.md
docs/outcomes/BLK-SYSTEM-011_sprint-closeout.md
python/blk_test_mcp_disabled_transport.py
python/test_blk_test_mcp_disabled_transport.py
```

Expected modified files:

```text
python/test_active_doctrine_review_gates.py
docs/BLK-008_blk-test-mcp-execution-server.md
docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md
docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md
```

---

## 13. Shared Verification Commands

Use these after each task before commit:

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

Focused commands by task:

```bash
# Task 1 / Task 5 doctrine gates
python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v

# Tasks 2-4 disabled transport implementation gates
python3 -m unittest discover -s python -p 'test_blk_test_mcp_disabled_transport.py' -v
```

Expected final Python suite count will increase from Sprint 010's 136 tests by the new Sprint 011 tests.

---

## 14. Stop Conditions

Stop and ask the human before proceeding if any task requires or accidentally introduces:

- real MCP SDK dependency installation;
- `package.json` / `npm install` / package-manager network access;
- live MCP client/server startup;
- HTTP/WebSocket/TCP/UDP transport;
- subprocess execution for BLK-test;
- actual test execution through BLK-test MCP;
- workspace clone/isolation implementation beyond static descriptors;
- approval-token acceptance that changes `live_mcp_authorized` to true;
- source mutation, staging, or commit from the BLK-test path;
- BEO publication, RTM generation, RTM drift rejection;
- protected active-vault body reads;
- production sandbox/host-secret isolation claims.

---

## 15. Recommended Next Sprint After Sprint 011

If Sprint 011 closes cleanly, the next safe seed is:

```text
BLK-SYSTEM-012 — Workspace Isolation and Process-Control Implementation Probes
```

BLK-SYSTEM-012 should still avoid live fixed-tool BLK-test execution. It should mechanically prove inert local probes for workspace clone/isolation, teardown, stale/live lock handling, child process group kill, timeout, output-flood cleanup, cache jailing, and primary-repo corruption prevention before Sprint 013 attempts approval/source-evidence authorization mechanics.
