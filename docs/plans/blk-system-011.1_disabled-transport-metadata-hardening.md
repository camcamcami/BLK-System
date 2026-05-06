# blk-system-011.1 — Disabled Transport Metadata Hardening Sprint Plan

> **For Hermes:** Execute with `blk-system-sprint-execution`, `test-driven-development`, and hostile review discipline. This is a surgical hardening sub-sprint, not a live BLK-test MCP enablement sprint.

**Sprint ID:** `BLK-SYSTEM-011.1` / `blk-system-011.1`

**Goal:** Harden the BLK-SYSTEM-011 disabled transport skeleton so all public metadata/probe APIs mechanically preserve the stdio-only, non-executing, no-source-authority contract proven by BLK-001 alignment review.

**Architecture:** Add dependency-free Python `unittest` regressions first, then minimally patch `python/blk_test_mcp_disabled_transport.py` and active doctrine. Reject tainted non-stdio descriptor metadata instead of normalizing it, add explicit no-source-write/no-staging/no-commit/no-push evidence fields, and replace brittle live-surface scans with an AST-aware gate that preserves required public evidence keys.

**Tech Stack:** Python standard library, `unittest`, Markdown doctrine/outcome artifacts, existing Go verification.

---

## 0. Live preflight facts

Captured before this plan was written:

```text
Date: Wed May  6 06:21:15 PM AEST 2026
Repository: /home/dad/BLK-System
Git status: ## main...origin/main
HEAD: ef1574d docs: close out blk-system sprint 012
Existing BLK-SYSTEM-011.1 plan: none found
```

Source review artifact preserved at:

```text
docs/reviews/BLK-SYSTEM-011.1_disabled-transport-hardening-source-review.md
```

---

## 1. BLK-001 Alignment Contract

BLK-SYSTEM-011.1 must preserve BLK-001's isolated-domain model:

| BLK-001 domain/component contract | Intent to preserve | Sprint 011.1 implication |
| --- | --- | --- |
| `blk-req` Legislative Gateway | Requirements/use cases remain HITL-authorized immutable active-vault artifacts. | Do not read protected BLK-req vault bodies, parse requirement bodies, or infer law from `docs/active/`, `docs/requirements/`, or `docs/use_cases/`. |
| `blk-id` Identity Spine | Identity/provenance records actor, artifact, source, approval, and canonical-hash metadata without creating authority. | Sprint 011.1 may preserve operator/source metadata vocabulary only; it must not implement identity-provider mechanics or approval decisions. |
| `blk-relay` Signal Bus | Typed messages may be carried between services without the relay authorizing payload truth or execution. | Sprint 011.1 must not add live transport, message bus behavior, JSON-RPC/MCP handshake, or routing authority. |
| Architecture & Feature Planning | Hermes plans bounded work; BLK-test is not architect/router. | Sprint 011.1 may harden disabled transport metadata contracts only; it must not make BLK-test choose scope, architecture, approval, or requirement interpretation. |
| `blk-pipe` Blast Shield & Forge | `blk-pipe` owns deterministic source mutation, staging, Git allowlists, and forge/blast-shield authority. | Runtime evidence must explicitly deny source-write, staging, commit, and push authority. Probe code must not call Git, stage files, commit, push, or replace `blk-pipe`. |
| `blk-test` Physics Oracle | BLK-test may later verify physical reality and return bounded evidence. | Sprint 011.1 hardens disabled stdio metadata and non-executing handshake/lifecycle evidence only. It must not execute fixed-tool tests or start live MCP. |
| `blk-link` Ledger | RTM remains a separate future/offline ledger comparing BEO trace hashes against active-vault hashes. | Sprint 011.1 must not generate RTM, emit coverage matrices, reject drift, or imply `blk-link` authority. |
| Cryptographic `version_hash` baton | `version_hash` remains opaque source-bound evidence shared across domains. | If trace evidence is mentioned, preserve `sha256:<64-lowercase-hex>` as opaque metadata only; do not inspect active-vault bodies or create trace authority. |

Sprint 011.1 passes alignment only if every implementation, test, doctrine, outcome, and closeout artifact says what authority it does **not** grant.

---

## 2. Decision Register

| Decision ID | Question | Decision | Rationale | Implementation effect |
| --- | --- | --- | --- | --- |
| DEC-001 | Is `BLK-SYSTEM-011.1` allowed after Sprint 012 is complete? | **Yes, as a surgical hardening backfill.** | The human requested an 011.1 hardening sprint after a hostile review. It targets Sprint 011 metadata proof gaps and must not reorder or reopen Sprint 012 scope. | Use `BLK-SYSTEM-011.1` prefixes for outcomes/reviews and `blk-system-011.1` for the plan filename. |
| DEC-002 | Does Sprint 011.1 authorize live BLK-test MCP? | **No.** | The reviewed alignment depends on disabled/non-executing scope. | All live startup, JSON-RPC/MCP handshake, server/client, network, SDK, and fixed-tool execution remains blocked. |
| DEC-003 | Should tainted non-stdio descriptor metadata be normalized to `stdio`? | **No. Reject it.** | Silent normalization can launder bad evidence. Rejection proves the invariant. | Add a shared descriptor guard and tests expecting `ValueError` for direct tainted descriptors. |
| DEC-004 | Should no-Git authority be explicit in runtime evidence? | **Yes.** | BLK-001 makes `blk-pipe` the forge/blast shield. Evidence should deny source-write/stage/commit/push authority, not merely omit it. | Add `source_write_allowed: False`, `staging_allowed: False`, `commit_allowed: False`, and `push_allowed: False` to public result shapes. |
| DEC-005 | Should the source-scan gate keep forbidding the broad string `subprocess`? | **No.** | Public evidence key `subprocess_called` is required; broad string scans collide with safe evidence vocabulary. | Replace with AST-aware import/call checks and literal marker checks that do not forbid public evidence keys. |
| DEC-006 | Should BLK-017 active doctrine mention 011.1? | **Yes, narrowly.** | BLK-017 is the active disabled transport contract. The hardening should be discoverable there without enabling transport. | Patch BLK-017 and `python/test_active_doctrine_review_gates.py` with hardening markers. |
| DEC-007 | Are task docs pushed after each task? | **Yes.** | Current BLK-System user policy is commit/push after each task, including outcome docs. | Each task has an implementation/docs commit and a matching pushed outcome doc commit unless the task is docs-only and combines them explicitly. |

---

## 3. Non-Goals and Hard Blocks

Sprint 011.1 must not implement, invoke, or imply:

- live BLK-test MCP transport;
- live MCP client/server startup;
- JSON-RPC/MCP handshake;
- live fixed-tool test execution;
- arbitrary shell, dynamic command execution, plugin-discovered tools, auto-fix, source-write, staging, commit, or push tools;
- Git operations inside disabled transport probe code;
- authoritative BLK-test verdict authority;
- authoritative BEO publication;
- RTM generation;
- RTM drift rejection authority;
- active BLK-req vault reads or requirement-body parsing;
- identity-provider implementation, `blk-relay` message bus behavior, approval-channel mechanics, operator token validation, or source-evidence authorization;
- live Codex/ExecutionPipe/BLK-pipe tactical execution as probe behavior;
- package-manager network installs, TypeScript MCP SDK runtime, sockets, HTTP, WebSockets, TCP, UDP, daemons, listeners, or network callbacks;
- production sandbox/container/cgroup/VM/namespace/seccomp/AppArmor/SELinux enforcement claims;
- production host-secret isolation claims;
- cyber tooling or execution against live targets.

Allowed work:

```text
dependency-free Python metadata/probe code
Python unittest RED/GREEN gates
AST-aware source-scan test helper
active BLK-017 disabled-contract doctrine hardening markers
Markdown review/outcome/closeout artifacts
exact-path Git staging by the sprint executor only
```

---

## 4. Invariants to Preserve

1. `BLK-SYSTEM-011.1` / `blk-system-011.1` naming is mandatory for this sub-sprint.
2. `BEB` and `BEO` remain artifact types, not sprint IDs.
3. BLK-017 remains the active disabled transport contract until live authority is separately approved.
4. The disabled transport skeleton is stdio-only metadata; no HTTP, WebSocket, TCP, UDP, daemon, listener, MCP SDK startup, or live client/server runtime is authorized.
5. Every public helper that consumes a descriptor must reject non-stdio `transport` metadata.
6. Rejection is preferred over normalization for tainted descriptor evidence.
7. No server starts, no client starts, no JSON-RPC handshake occurs, no subprocess is spawned, no network is called, and no fixed BLK-test tool executes.
8. Runtime evidence explicitly denies source-write, staging, commit, push, BEO publication, RTM generation, RTM drift rejection, active-vault body reads, and approval mechanics.
9. Public evidence keys such as `subprocess_called` may exist; source-scan gates must target live imports/calls, not required safe vocabulary.
10. Every task outcome records RED evidence, GREEN evidence, shared verification evidence, exact files touched, commit/push evidence, and explicit non-authority statements.
11. Remove `python/__pycache__` before exact-path staging.
12. Do not use `git add .`, `git add -u`, broad stash, broad revert, broad reset, or broad checkout operations.

---

## 5. Controller Workflow for Each Task

For each task:

1. Preflight:

   ```bash
   cd /home/dad/BLK-System
   export PATH="$HOME/.local/bin:$PATH"
   git status --short --branch
   git log -1 --oneline
   ```

2. Read the task section, source review, and exact files before editing.
3. Add the focused RED gate first.
4. Run the focused test and capture expected RED.
5. Patch only the files named in the task.
6. Rerun the focused test for GREEN.
7. Run shared verification:

   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   python3 -m unittest discover -s python -p 'test_*.py'
   go test ./...
   go vet ./...
   git diff --check
   ```

8. Create the matching task outcome document:

   ```text
   docs/outcomes/BLK-SYSTEM-011.1_task-00N-outcome.md
   ```

9. Rerun any content gate for the outcome document.
10. Remove generated Python caches:

    ```bash
    rm -rf python/__pycache__
    ```

11. Stage exact files only.
12. Commit with the task's listed commit message.
13. Push immediately:

    ```bash
    git push origin main
    git status --short --branch
    ```

---

## 6. Task 1 — Reject Tainted Non-stdio Descriptor Metadata Across Public Helpers

### Objective

Prove every public disabled-transport helper that consumes descriptor metadata rejects tainted non-stdio transport values instead of echoing or normalizing them.

### Files

Modify:

- `python/test_blk_test_mcp_disabled_transport.py`
- `python/blk_test_mcp_disabled_transport.py`

Create outcome:

- `docs/outcomes/BLK-SYSTEM-011.1_task-001-outcome.md`

### Required behavior

These direct tainted descriptor inputs must raise `ValueError` containing `stdio-only`:

- `evaluate_disabled_transport_startup({"transport": "tcp", ...})`
- `build_non_executing_handshake_probe({"transport": "tcp", ...})`
- `build_disabled_lifecycle_probe({"transport": "tcp", ...})`

Normal descriptors from `build_disabled_transport_descriptor()` must continue to produce disabled/non-executing evidence.

### RED steps

Add tests first to `DisabledTransportStartupTest`:

```python
def test_startup_decision_rejects_tainted_non_stdio_descriptor_metadata(self):
    descriptor = build_disabled_transport_descriptor()
    descriptor["transport"] = "tcp"

    with self.assertRaisesRegex(ValueError, "stdio-only"):
        evaluate_disabled_transport_startup(descriptor)


def test_handshake_probe_rejects_tainted_non_stdio_descriptor_metadata(self):
    descriptor = build_disabled_transport_descriptor()
    descriptor["transport"] = "http"

    with self.assertRaisesRegex(ValueError, "stdio-only"):
        build_non_executing_handshake_probe(descriptor)


def test_lifecycle_probe_rejects_tainted_non_stdio_descriptor_metadata(self):
    descriptor = build_disabled_transport_descriptor()
    descriptor["transport"] = "websocket"

    with self.assertRaisesRegex(ValueError, "stdio-only"):
        build_disabled_lifecycle_probe(descriptor, event="startup_refused")
```

Run focused RED:

```bash
PYTHONPATH=python python3 -m unittest \
  python.test_blk_test_mcp_disabled_transport.DisabledTransportStartupTest.test_startup_decision_rejects_tainted_non_stdio_descriptor_metadata \
  python.test_blk_test_mcp_disabled_transport.DisabledTransportStartupTest.test_handshake_probe_rejects_tainted_non_stdio_descriptor_metadata \
  python.test_blk_test_mcp_disabled_transport.DisabledTransportStartupTest.test_lifecycle_probe_rejects_tainted_non_stdio_descriptor_metadata -v
```

Expected RED:

```text
AssertionError: ValueError not raised
```

### GREEN implementation

Add a private guard near the top of `python/blk_test_mcp_disabled_transport.py`:

```python
def _require_stdio_transport_metadata(descriptor: dict[str, object]) -> str:
    transport = descriptor.get("transport", "stdio")
    if transport != "stdio":
        raise ValueError("BLK-SYSTEM-011.1 descriptor transport is stdio-only")
    return "stdio"
```

Use it in:

- `evaluate_disabled_transport_startup(...)`
- `build_non_executing_handshake_probe(...)`
- `build_disabled_lifecycle_probe(...)`

Do not silently rewrite bad transport metadata. Reject it before constructing evidence.

### GREEN verification

Run:

```bash
PYTHONPATH=python python3 -m unittest python.test_blk_test_mcp_disabled_transport.DisabledTransportStartupTest -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

### Outcome and commit

Create `docs/outcomes/BLK-SYSTEM-011.1_task-001-outcome.md` with RED/GREEN/shared verification evidence and explicit non-authority statement.

Stage exact files only:

```bash
rm -rf python/__pycache__
git add \
  python/test_blk_test_mcp_disabled_transport.py \
  python/blk_test_mcp_disabled_transport.py \
  docs/outcomes/BLK-SYSTEM-011.1_task-001-outcome.md
git diff --cached --check
git commit -m "test: harden disabled transport descriptor metadata"
git push origin main
```

---

## 7. Task 2 — Add Explicit No Source-Write, Staging, Commit, and Push Evidence Fields

### Objective

Make the BLK-001 `blk-pipe`/BLK-test boundary explicit in every public Sprint 011 disabled-transport evidence shape.

### Files

Modify:

- `python/test_blk_test_mcp_disabled_transport.py`
- `python/blk_test_mcp_disabled_transport.py`

Create outcome:

- `docs/outcomes/BLK-SYSTEM-011.1_task-002-outcome.md`

### Required behavior

Each public result shape must include these fields set to `False`:

```python
"source_write_allowed": False
"staging_allowed": False
"commit_allowed": False
"push_allowed": False
```

Required surfaces:

- `build_disabled_transport_descriptor(...)`
- `evaluate_disabled_transport_startup(...)`
- `build_non_executing_handshake_probe(...)`
- `build_disabled_lifecycle_probe(...)`
- each entry from `fixed_tool_registry_descriptor()`
- `evaluate_disabled_tool_execution(...)`

### RED steps

Add a helper in the test file:

```python
def assert_no_git_authority_fields(test_case, evidence):
    for key in (
        "source_write_allowed",
        "staging_allowed",
        "commit_allowed",
        "push_allowed",
    ):
        test_case.assertIn(key, evidence)
        test_case.assertFalse(evidence[key])
```

Call it from existing tests for each public evidence shape. The first RED should fail on missing keys.

Run focused RED:

```bash
PYTHONPATH=python python3 -m unittest python.test_blk_test_mcp_disabled_transport.DisabledTransportStartupTest -v
```

Expected RED:

```text
AssertionError: 'source_write_allowed' not found
```

### GREEN implementation

Add a private helper:

```python
def _no_source_write_authority_fields() -> dict[str, bool]:
    return {
        "source_write_allowed": False,
        "staging_allowed": False,
        "commit_allowed": False,
        "push_allowed": False,
    }
```

Merge it into every public result shape listed above. Preserve existing fields such as `source_mutation_allowed: False` for backward compatibility.

### GREEN verification

Run:

```bash
PYTHONPATH=python python3 -m unittest python.test_blk_test_mcp_disabled_transport.DisabledTransportStartupTest -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

### Outcome and commit

Create `docs/outcomes/BLK-SYSTEM-011.1_task-002-outcome.md` with RED/GREEN/shared verification evidence and explicit non-authority statement.

Stage exact files only:

```bash
rm -rf python/__pycache__
git add \
  python/test_blk_test_mcp_disabled_transport.py \
  python/blk_test_mcp_disabled_transport.py \
  docs/outcomes/BLK-SYSTEM-011.1_task-002-outcome.md
git diff --cached --check
git commit -m "test: expose disabled transport no-git authority fields"
git push origin main
```

---

## 8. Task 3 — Replace Brittle Live-Surface Source Scan With AST-Aware Gate

### Objective

Prove the disabled transport module has no live execution imports/calls while preserving required public evidence vocabulary such as `subprocess_called`.

### Files

Modify:

- `python/test_blk_test_mcp_disabled_transport.py`

Create outcome:

- `docs/outcomes/BLK-SYSTEM-011.1_task-003-outcome.md`

### Required behavior

The source-scan gate must:

1. reject live imports such as `subprocess`, `socket`, `requests`, `http.server`, `urllib`, and `asyncio`;
2. reject live calls such as `os.system(...)`, `eval(...)`, `exec(...)`, `__import__(...)`, `subprocess.Popen(...)`, and dynamic command helpers;
3. reject forbidden literal capabilities such as `shell=True`, `publish_beo`, `generate_rtm`, and `read_active_vault`;
4. allow safe public evidence keys such as `subprocess_called`.

### RED steps

Add `import ast` at the top of the test file and add a missing helper call with synthetic cases before implementing the helper:

```python
def test_live_surface_source_scan_rejects_ast_imports_and_calls_but_allows_public_evidence_keys(self):
    safe_public_evidence = "descriptor['subprocess_called'] = False"
    _assert_disabled_transport_source_has_no_live_surfaces(safe_public_evidence)

    bad_sources = [
        "import subprocess\n",
        "from socket import socket\n",
        "import os\nos.system('echo bad')\n",
        "eval('1 + 1')\n",
        "__import__('subprocess')\n",
        "subprocess.Popen(['true'])\n",
        "shell=True\n",
        "publish_beo\n",
        "generate_rtm\n",
        "read_active_vault\n",
    ]
    for source in bad_sources:
        with self.assertRaises(AssertionError, msg=source):
            _assert_disabled_transport_source_has_no_live_surfaces(source)
```

Run focused RED:

```bash
PYTHONPATH=python python3 -m unittest \
  python.test_blk_test_mcp_disabled_transport.DisabledTransportStartupTest.test_live_surface_source_scan_rejects_ast_imports_and_calls_but_allows_public_evidence_keys -v
```

Expected RED:

```text
NameError: name '_assert_disabled_transport_source_has_no_live_surfaces' is not defined
```

### GREEN implementation

Implement the helper in the test file, not production code. It should parse AST where possible and fail on forbidden imports/calls. Then update `test_disabled_transport_module_does_not_import_live_execution_surfaces` to call the helper on the actual module source.

Do not keep a broad `"subprocess"` substring ban. Required public evidence fields may contain `subprocess_called`.

### GREEN verification

Run:

```bash
PYTHONPATH=python python3 -m unittest python.test_blk_test_mcp_disabled_transport.DisabledTransportStartupTest -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

### Outcome and commit

Create `docs/outcomes/BLK-SYSTEM-011.1_task-003-outcome.md` with RED/GREEN/shared verification evidence and explicit non-authority statement.

Stage exact files only:

```bash
rm -rf python/__pycache__
git add \
  python/test_blk_test_mcp_disabled_transport.py \
  docs/outcomes/BLK-SYSTEM-011.1_task-003-outcome.md
git diff --cached --check
git commit -m "test: add ast disabled transport source-surface gate"
git push origin main
```

---

## 9. Task 4 — Patch BLK-017 Active Doctrine With 011.1 Hardening Markers

### Objective

Make the BLK-SYSTEM-011.1 hardening discoverable in active doctrine without enabling live BLK-test MCP.

### Files

Modify:

- `python/test_active_doctrine_review_gates.py`
- `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md`

Create outcome:

- `docs/outcomes/BLK-SYSTEM-011.1_task-004-outcome.md`

### Required doctrine markers

BLK-017 must explicitly include:

- `BLK-SYSTEM-011.1`
- `tainted descriptor metadata is rejected, not normalized`
- `all public disabled-transport helper APIs enforce stdio-only metadata`
- `source_write_allowed: false`
- `staging_allowed: false`
- `commit_allowed: false`
- `push_allowed: false`
- `AST-aware source-scan gate`
- `subprocess_called public evidence key remains allowed`
- `does not authorize live BLK-test MCP`
- `does not authorize live MCP client/server startup`
- `does not execute fixed-tool tests`
- `does not authorize authoritative BEO publication`
- `does not authorize RTM generation`
- `does not read protected BLK-req vault bodies`

### RED steps

Extend `test_blk017_records_disabled_transport_skeleton_without_live_authority` or add a new focused doctrine test requiring the markers above.

Run focused RED:

```bash
PYTHONPATH=python python3 -m unittest \
  python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_blk017_records_disabled_transport_skeleton_without_live_authority -v
```

Expected RED:

```text
BLK-017 disabled transport markers missing: ['BLK-SYSTEM-011.1', ...]
```

### GREEN implementation

Patch BLK-017 with a concise hardening section after `## 2. Current authority boundary` or before `## 8. Implementation and tests`.

Required tone:

- say the hardening tightens metadata evidence only;
- repeat that live BLK-test MCP remains disabled;
- say tainted descriptors are rejected, not normalized;
- say all no-source-write/no-staging/no-commit/no-push evidence fields are false;
- say the AST-aware scan forbids live imports/calls while allowing safe public evidence keys.

### GREEN verification

Run:

```bash
PYTHONPATH=python python3 -m unittest \
  python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_blk017_records_disabled_transport_skeleton_without_live_authority -v
PYTHONPATH=python python3 -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

### Outcome and commit

Create `docs/outcomes/BLK-SYSTEM-011.1_task-004-outcome.md` with RED/GREEN/shared verification evidence and explicit non-authority statement.

Stage exact files only:

```bash
rm -rf python/__pycache__
git add \
  python/test_active_doctrine_review_gates.py \
  docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md \
  docs/outcomes/BLK-SYSTEM-011.1_task-004-outcome.md
git diff --cached --check
git commit -m "docs: record blk-system 011.1 transport hardening doctrine"
git push origin main
```

---

## 10. Task 5 — Sprint Closeout and 013 Handoff Preservation

### Objective

Close BLK-SYSTEM-011.1 with self-contained audit evidence and preserve the existing BLK-SYSTEM-013 handoff boundary.

### Files

Create:

- `docs/outcomes/BLK-SYSTEM-011.1_sprint-closeout.md`

No code changes unless final verification reveals a defect.

### Required closeout content

The closeout must include:

- `BLK-SYSTEM-011.1` / `blk-system-011.1`;
- source review path;
- plan path;
- BLK-001 alignment verdict;
- task commit table for Tasks 1-4 plus closeout;
- created/modified file list;
- RED/GREEN evidence summary for Tasks 1-4;
- final verification evidence;
- explicit non-authority statement;
- final post-push commit hash and `git status --short --branch` evidence;
- statement that Sprint 012 remains the workspace/process-control owner;
- statement that Sprint 013 remains the approval/source-evidence authorization owner;
- statement that Sprint 014 remains any future first live fixed-tool BLK-test MCP smoke owner.

The closeout must explicitly say Sprint 011.1 did not:

- authorize live BLK-test MCP;
- start a live MCP server/client;
- execute fixed-tool tests;
- spawn subprocesses for BLK-test;
- open network sockets or HTTP/WebSocket transports;
- mutate source, stage files, commit, or push as BLK-test behavior;
- publish authoritative BEOs;
- generate RTM;
- grant RTM drift rejection authority;
- read active BLK-req vault bodies;
- implement approval-channel mechanics;
- claim production sandbox/cgroup/VM/host-secret isolation.

### RED/GREEN steps

Run RED before creating the file:

```bash
python3 - <<'PY'
from pathlib import Path
path = Path('docs/outcomes/BLK-SYSTEM-011.1_sprint-closeout.md')
assert path.exists(), 'RED: Sprint 011.1 closeout doc missing'
PY
```

Expected RED:

```text
AssertionError: RED: Sprint 011.1 closeout doc missing
```

Create the closeout and run content gate:

```bash
python3 - <<'PY'
from pathlib import Path
path = Path('docs/outcomes/BLK-SYSTEM-011.1_sprint-closeout.md')
text = path.read_text()
required = [
    'BLK-SYSTEM-011.1',
    'BLK-001 alignment verdict',
    'docs/plans/blk-system-011.1_disabled-transport-metadata-hardening.md',
    'docs/reviews/BLK-SYSTEM-011.1_disabled-transport-hardening-source-review.md',
    'tainted descriptor metadata is rejected, not normalized',
    'AST-aware source-scan gate',
    'source_write_allowed: false',
    'staging_allowed: false',
    'commit_allowed: false',
    'push_allowed: false',
    'does not authorize live BLK-test MCP',
    'does not authorize live MCP client/server startup',
    'does not execute fixed-tool tests',
    'does not authorize authoritative BEO publication',
    'does not authorize RTM generation',
    'does not read active BLK-req vault bodies',
    'BLK-SYSTEM-013',
    'BLK-SYSTEM-014',
]
missing = [marker for marker in required if marker not in text]
assert not missing, missing
fence = chr(96) * 3
assert text.count(fence) % 2 == 0
for i, line in enumerate(text.splitlines(), 1):
    assert line.rstrip() == line, f'trailing whitespace line {i}'
print('SPRINT011_1_CLOSEOUT_CONTENT_PASS')
PY
```

### Final verification

Run:

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
rm -rf python/__pycache__
git status --short --branch
git log --oneline --decorate -12
```

### Commit and push

```bash
git add docs/outcomes/BLK-SYSTEM-011.1_sprint-closeout.md
git diff --cached --check
git commit -m "docs: close out blk-system sprint 011.1"
git push origin main
git status --short --branch
git log -1 --oneline
```

After push, patch the closeout if necessary to include final post-push hash/status evidence, then rerun the closeout content gate and commit/push that patch as:

```bash
git add docs/outcomes/BLK-SYSTEM-011.1_sprint-closeout.md
git commit -m "docs: record blk-system sprint 011.1 post-push closeout evidence"
git push origin main
```

---

## 11. Expected File Summary

Plan/source review files already created by the planning step:

```text
docs/plans/blk-system-011.1_disabled-transport-metadata-hardening.md
docs/reviews/BLK-SYSTEM-011.1_disabled-transport-hardening-source-review.md
```

Expected modified implementation/test/doctrine files during execution:

```text
python/blk_test_mcp_disabled_transport.py
python/test_blk_test_mcp_disabled_transport.py
python/test_active_doctrine_review_gates.py
docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md
```

Expected outcome files:

```text
docs/outcomes/BLK-SYSTEM-011.1_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-011.1_task-002-outcome.md
docs/outcomes/BLK-SYSTEM-011.1_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-011.1_task-004-outcome.md
docs/outcomes/BLK-SYSTEM-011.1_sprint-closeout.md
```

No other files are in scope.

---

## 12. Final Acceptance Criteria

BLK-SYSTEM-011.1 is complete only when:

- every public descriptor-consuming helper rejects tainted non-stdio metadata with `ValueError`;
- every public disabled-transport evidence shape explicitly contains `source_write_allowed: False`, `staging_allowed: False`, `commit_allowed: False`, and `push_allowed: False`;
- the source-scan gate is AST-aware and permits safe public evidence vocabulary such as `subprocess_called`;
- BLK-017 records BLK-SYSTEM-011.1 hardening markers without implying live authority;
- all task outcome docs and sprint closeout exist, are committed, and are pushed;
- full Python unittest, Go test, Go vet, and `git diff --check` pass;
- no generated `python/__pycache__` files are staged;
- `git status --short --branch` ends clean and aligned with `origin/main`;
- every artifact repeats that Sprint 011.1 does not authorize live BLK-test MCP, fixed-tool execution, source mutation/staging/commit/push as BLK-test behavior, authoritative BEO publication, RTM generation, active-vault reads, approval mechanics, or production sandbox/host-secret isolation.

---

## 13. Quick Resume Prompt

```text
Execute BLK-SYSTEM-011.1 from docs/plans/blk-system-011.1_disabled-transport-metadata-hardening.md. Follow strict TDD, exact-path staging, commit/push after each task, and create matching outcome docs. Preserve BLK-001 boundaries: this hardens disabled transport metadata only and does not authorize live BLK-test MCP, fixed-tool execution, source mutation/staging/commit/push as BLK-test behavior, BEO publication, RTM generation, active-vault reads, approval mechanics, or production sandbox/host-secret claims.
```
