# BLK-SYSTEM-014 — First Live Fixed-Tool BLK-test MCP Smoke Implementation Plan

> **For Hermes:** Use `blk-system-sprint-execution`, `writing-plans`, and strict TDD to implement this plan task-by-task. Any Codex/Hermes delegation is project-maintenance implementation support only; it must not be used by BLK-test MCP, the live smoke child process, approval evidence, tool execution, or replay evidence. If delegating implementation work to Codex CLI, use model `gpt-5.4` and run a hostile audit after every execution packet before accepting changes.

**Goal:** Implement and run the first bounded stdio fixed-tool BLK-test MCP smoke only after exact BLK-019 approval/source-evidence validation and explicit human approval for one synthetic isolated workspace/profile/tool envelope.

**Architecture:** Add a new Sprint 014 live-smoke module rather than weakening BLK-017/018/019. BLK-017 remains the active disabled transport contract, BLK-018 remains the workspace/process-control probe contract, and BLK-019 remains the approval/source-evidence authorization contract. Sprint 014 creates a dependency-free stdio JSON-RPC/MCP-subset smoke harness for one approved fixed tool, bounded output/timeout, replay-safe evidence, cleanup, and explicit non-authority fields.

**Tech Stack:** Python standard library only (`unittest`, `ast`, `copy`, `hashlib`, `json`, `os`, `pathlib`, `signal`, `subprocess`, `sys`, `tempfile`, `time`, `uuid`), existing BLK-System Python probes, Markdown doctrine/review/outcome docs, Go verification gates.

---

## 0. Live preflight facts

Captured before writing this plan:

```text
Date: 2026-05-07T06:23:33+10:00
Repository: /home/dad/BLK-System
Branch/status: ## main...origin/main
HEAD: ba7e5a3 docs: close out blk-system sprint 013
Plan file: docs/plans/blk-system-014_first-live-fixed-tool-blk-test-mcp-smoke.md
```

Sprint ID ownership check:

- `BLK-SYSTEM-014` is reserved by `docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md` for `First live fixed-tool BLK-test MCP smoke under explicit human approval`.
- The existing `docs/BLK-014_blk-execution-outcome-fixture-shape.md` is a BLK doctrine document for execution outcome fixture shape. It is not this system sprint plan and must not be renamed or repurposed.
- Sprint 013 closeout explicitly hands off to `BLK-SYSTEM-014` only after BLK-017, BLK-018, and BLK-019 prerequisite gates are accepted.

---

## 1. BLK-001 domain matrix

| Domain/component | Sprint 014 relationship | Authority statement |
| --- | --- | --- |
| `blk-req` | May carry opaque synthetic `trace_artifacts[*].version_hash` metadata in approval/source evidence only. | Does not read protected BLK-req vault bodies, parse active requirements, promote requirements, or mutate requirement docs. |
| Architecture & Feature Planning / HITL | Requires explicit current human approval for one exact live-smoke envelope before any live smoke run. | No ambient approval is inferred from Codex, prior sprint docs, Discord status, or agent implementation authority. |
| `blk-id` | May emit deterministic hashes for approval, authorization request, source evidence, smoke transcript, and replay bundle. | Hashes are evidence identifiers only; they do not create mutation, publication, ledger, RTM, or active-vault authority. |
| `blk-relay` | Uses local stdio only for a dependency-free JSON-RPC/MCP-subset smoke. | No HTTP, WebSocket, TCP, UDP, daemon, listener, callback, Discord-mediated execution token, or production relay is authorized. |
| `blk-pipe` | Source evidence is a synthetic BLK-pipe-shaped source report bound exactly through BLK-019. | BLK-test still must not mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source as BLK-test behavior. |
| `blk-test` | Owns the first bounded fixed-tool live-smoke evidence path. | Executes at most one approved fixed tool against one synthetic isolated workspace under explicit approval; no arbitrary shell, dynamic command, cyber target, real repo test, or production MCP authority. |
| `blk-link` / RTM | Smoke evidence may state `rtm_status: NOT_GENERATED`. | Does not generate RTM, make drift decisions, claim coverage, or write ledgers. |
| BEO/outcomes | Sprint outcome docs may record replay-safe smoke evidence. | Does not publish authoritative BEOs; any BEO-adjacent field remains `DRAFT_ONLY`. |
| Cryptographic `version_hash` baton | Requires canonical `sha256:<64-lowercase-hex>` trace hashes in approval/source metadata. | Hashes remain opaque and source-bound; Sprint 014 does not verify protected requirement bodies. |

---

## 2. Scope boundary

### Allowed scope

- A new dependency-free Python module for Sprint 014 live-smoke preflight, fixed-tool registry, synthetic workspace guard, stdio subprocess runner, transcript bounding, and replay evidence.
- A local stdio JSON-RPC/MCP-subset child process for one fixed tool smoke. This is a bounded smoke harness, not a production MCP implementation or MCP SDK adoption.
- Exactly one initial fixed tool: `run_ast_validation` against a synthetic isolated fixture workspace.
- Exact BLK-019 validation of approval/source evidence before any live smoke.
- A Sprint 014 live-smoke approval extension that binds `approval_kind == "blk-test-mcp-live-smoke"`, `run_id`, operator identity, approval timestamp, expiry, exact envelope hash, implementation commit hash, driver hash, requested tool, workspace identity, and timeout/output profile.
- Mandatory replay protection for live smoke using exact approval ID and run ID checks before execution.
- BLK-018-style workspace/path/cache/lock/output/cleanup constraints reused or mirrored where safe, including marker-owned synthetic workspace roots, run-scoped cache/lock roots, startup purge, guarded teardown, no `.git`, no protected-prefix tree acceptance, and no symlink escape.
- PASS/FAIL/BLOCKED/FATAL/TRANSPORT evidence that is source-bound, bounded, sanitized, and replayable.
- Review/doc gates that preserve BLK-017/018/019 and define BLK-020 as first-smoke doctrine after successful execution.
- Matching outcome docs after each task, committed and pushed separately during execution.

### Hard blocks / stop conditions

Stop and escalate if any implementation or smoke attempt tries to:

- start live BLK-test MCP without committed/pushed implementation code and explicit current human approval for the exact source/request/workspace/profile/tool envelope, implementation commit hash, driver hash, run ID, approval ID, timeout/output profile, and workspace policy;
- reuse `codex-live` or `BLK_APPROVE_CODEX_LIVE` as BLK-test MCP approval;
- broaden approval beyond one exact source/request/workspace/profile/tool envelope;
- use arbitrary shell, `shell=True`, caller-supplied commands, dynamic command construction, package-manager installs, model calls, cyber tooling, or tactical LLM calls;
- use non-stdio transport, socket/listener, HTTP, WebSocket, TCP/UDP, daemon, callback, or network service;
- run against `/home/dad/BLK-System`, a workspace with a `.git` root/ancestor/descendant, any known repository root/descendant, or another real project repository as the BLK-test target;
- mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source as BLK-test behavior;
- read protected BLK-req vault bodies or active-vault body paths;
- publish authoritative BEOs;
- generate RTM or make RTM drift decisions;
- claim production sandbox/container/cgroup/VM/seccomp/AppArmor/SELinux or host-secret isolation enforcement;
- exceed bounded timeout/output limits;
- leave child processes, unreleased locks, or run-owned workspace/cache paths after terminal status;
- leak host secrets, environment dumps, protected bodies, approval secrets, or unbounded raw logs;
- return an unknown status or unreplayable evidence.

---

## 3. Decision register

| ID | Decision | Rationale | Mechanical gate |
| --- | --- | --- | --- |
| S14-SMOKE-001 | Sprint 014 adds a new module instead of enabling BLK-017 globally. | BLK-017 must remain the active disabled transport contract for default startup paths. | Tests assert `evaluate_sprint013_approval_preflight` still returns `STARTUP_BLOCKED_SPRINT014_REQUIRED`; new positive path lives in `python/blk_test_mcp_fixed_tool_live_smoke.py`. |
| S14-SMOKE-002 | First smoke is stdio-only and dependency-free. | Avoid a broad SDK/network/runtime leap while proving process/stdio physics. | Source scan rejects sockets/listeners/HTTP/WebSocket/MCP SDK/package manager imports. |
| S14-SMOKE-003 | First smoke executes exactly one fixed tool: `run_ast_validation`. | Multi-tool execution broadens authority and evidence surface. | Registry/preflight rejects unknown, wildcard, duplicate, multi-tool, shell-like, or caller-command requests. |
| S14-SMOKE-004 | First target is a synthetic isolated workspace, not the BLK-System repo or a real project. | Sprint 010 explicitly blocks real target execution and source mutation for first smoke. | Workspace guard rejects `/home/dad/BLK-System`, repo roots, home/root paths, protected prefixes, traversal, and symlink escape. |
| S14-SMOKE-005 | Positive smoke requires both BLK-019 validation and a Sprint 014 explicit live flag/approval checkpoint. | Approval validation alone was intentionally non-executing in Sprint 013. | Preflight requires `APPROVAL_VALIDATED_SOURCE_BOUND`, matching hashes/envelope, `live_smoke_enabled is True`, and human approval evidence. |
| S14-SMOKE-006 | Child process execution is allowed only through a static stdio server command. | A live smoke needs process physics but must not expose arbitrary execution. | Tests assert list command, `shell=False`, static code/entrypoint, `stdin/stdout` pipes, `start_new_session=True`, bounded timeout/output, and shared kill path. |
| S14-SMOKE-007 | Smoke evidence may be PASS/FAIL/BLOCKED but remains non-authoritative for BEO/RTM. | Physical evidence must not become publication or traceability authority. | Returned evidence contains `beo_publication: DRAFT_ONLY`, `rtm_status: NOT_GENERATED`, no BEO publication, no RTM fields, no active-vault reads. |
| S14-SMOKE-008 | First live smoke must run only from committed/pushed implementation code. | Approval must bind reviewed source, not a dirty worktree. | Task 4 commits/pushes wrapper/tests first, verifies clean status, then asks for human approval containing implementation commit hash and driver hash. |
| S14-SMOKE-009 | Approval/replay is mechanically enforced, not a magic string only. | `live_smoke_enabled=True` alone is too weak. | Sprint 014 rejects non-`blk-test-mcp-live-smoke` approval kind, missing run ID, stale/future timestamps, duplicate approval/run IDs, and envelope hash mismatch. |
| S14-SMOKE-010 | BLK-020 is published only after a PASS first smoke with cleanup verified. | Active first-smoke doctrine must not describe failed or blocked evidence as accepted behavior. | If Task 4 returns `FAIL`, `BLOCKED`, `FATAL_*`, `TRANSPORT_ERROR`, or `OPERATOR_INTERRUPTED`, stop after outcome/closeout and do not create BLK-020. |

---

## 4. Controller workflow for execution

1. Create an implementation branch, for example `sprint/blk-system-014`.
2. Commit this plan first if it is still uncommitted.
3. For every task below:
   1. Write/patch the failing test first.
   2. Run the focused RED command and confirm expected failure.
   3. Implement the smallest code/doc change.
   4. Run focused GREEN verification.
   5. Run task shared gates.
   6. Remove Python/pytest caches.
   7. Stage exact paths only.
   8. Verify `git diff --cached --name-only` contains only expected files.
   9. Commit implementation/doc change.
   10. Push the implementation/doc commit to GitHub.
   11. Create `docs/outcomes/BLK-SYSTEM-014_task-00N-outcome.md` with RED/GREEN and pre-commit verification evidence.
   12. Commit and push the outcome doc separately.
   13. Send concise Discord summary with `MEDIA:/home/dad/BLK-System/docs/outcomes/BLK-SYSTEM-014_task-00N-outcome.md` after push.
4. Task 4 contains a mandatory commit-before-approval checkpoint and human approval checkpoint. Do not run the first live smoke until wrapper/test code is committed and pushed, `git status --short --branch` is clean, and the operator approves the exact envelope recorded by that task.
5. Close the sprint with `docs/outcomes/BLK-SYSTEM-014_sprint-closeout.md`, committed and pushed separately.

Cache-safe command pattern:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s python -p 'test_*.py'
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
find python -type d -name __pycache__ -prune -exec rm -rf {} +
git diff --check
git status --short --branch
```

---

## 5. Shared deterministic fixture values

Use these values across Sprint 014 tests unless a task says otherwise:

```python
TRACE_S14 = {
    "kind": "REQ",
    "id": "REQ-S14-SMOKE-001",
    "version_hash": "sha256:" + "1" * 64,
}
SOURCE_REPORT_IDENTITY_S14 = {
    "report_path": "reports/BLK-SYSTEM-014/synthetic-source-report.json",
    "report_hash": "sha256:" + "2" * 64,
    "report_id": "source-report-BLK-SYSTEM-014-smoke",
}
SOURCE_REPORT_S14 = {
    "status": "SUCCESS",
    "source_report_identity": SOURCE_REPORT_IDENTITY_S14,
    "beb_id": "BEB_S14_SYNTHETIC_SMOKE",
    "commit_hash": "synthetic-fixture-no-git-commit",
    "pre_engine_hash": "sha256:" + "3" * 64,
    "trace_artifacts": [TRACE_S14],
}
WORKSPACE_IDENTITY_S14 = {
    "target_branch": "synthetic-sprint-014-smoke",
    "workspace_clone_id": "workspace-BLK-SYSTEM-014-smoke-run-001",
    "source_path_policy": "synthetic-isolated-copy-only",
}
TIMEOUT_OUTPUT_PROFILE_S14 = {
    "timeout_class": "bounded-live-smoke-short",
    "timeout_seconds": 5,
    "output_byte_limit": 4096,
    "compression": "line-dedupe-byte-bound",
}
REQUESTED_TOOLS_S14 = ["run_ast_validation"]
ISSUED_AT_S14 = "2026-05-07T00:00:00Z"
EXPIRES_AT_S14 = "2026-05-07T00:15:00Z"
NOW_S14 = "2026-05-07T00:05:00Z"
```

---

## 6. Task 0 — Commit the plan before implementation

**Objective:** Make this reviewed plan durable before implementation starts.

**Files:**

- Add: `docs/plans/blk-system-014_first-live-fixed-tool-blk-test-mcp-smoke.md`
- Outcome: `docs/outcomes/BLK-SYSTEM-014_task-000-outcome.md`

**Step 1: Verify plan file markers**

Run:

```bash
python - <<'PY'
from pathlib import Path
path = Path('docs/plans/blk-system-014_first-live-fixed-tool-blk-test-mcp-smoke.md')
text = path.read_text()
required = [
    'BLK-SYSTEM-014',
    'First Live Fixed-Tool BLK-test MCP Smoke',
    'explicit human approval',
    'BLK-017 remains the active disabled transport contract',
    'BLK-018 remains the workspace/process-control probe contract',
    'BLK-019 remains the approval/source-evidence authorization contract',
    'run_ast_validation',
    'synthetic isolated workspace',
    'does not publish authoritative BEOs',
    'does not generate RTM',
    'does not read protected BLK-req vault bodies',
]
missing = [marker for marker in required if marker not in text]
if missing:
    raise SystemExit(f'missing plan markers: {missing}')
fence = chr(96) * 3
if text.count(fence) % 2:
    raise SystemExit('unbalanced markdown fences')
print('BLK-SYSTEM-014 plan markers: PASS')
PY
```

Expected: `BLK-SYSTEM-014 plan markers: PASS`.

**Step 2: Stage exact path and commit**

Run:

```bash
git add docs/plans/blk-system-014_first-live-fixed-tool-blk-test-mcp-smoke.md
git diff --cached --name-only
git commit -m "docs: plan blk-system sprint 014 live smoke"
git push
```

Expected staged path only:

```text
docs/plans/blk-system-014_first-live-fixed-tool-blk-test-mcp-smoke.md
```

**Step 3: Outcome doc**

Create, validate, exact-path commit, and push `docs/outcomes/BLK-SYSTEM-014_task-000-outcome.md`.

---

## 7. Task 1 — Boundary review artifact and persistent doctrine gate

**Objective:** Preserve Sprint 014 authority boundaries before live-smoke code exists.

**Files:**

- Create: `docs/reviews/BLK-SYSTEM-014_live-fixed-tool-smoke-boundary-review.md`
- Modify: `python/test_active_doctrine_review_gates.py`
- Outcome: `docs/outcomes/BLK-SYSTEM-014_task-001-outcome.md`

**Step 1: Write failing test**

Add constant near existing Sprint review constants:

```python
SPRINT014_LIVE_SMOKE_REVIEW = ROOT / "docs" / "reviews" / "BLK-SYSTEM-014_live-fixed-tool-smoke-boundary-review.md"
```

Add test:

```python
def test_sprint014_live_fixed_tool_smoke_review_preserves_prerequisite_boundaries(self):
    self.assertTrue(SPRINT014_LIVE_SMOKE_REVIEW.exists(), "Sprint 014 live smoke boundary review missing")
    text = SPRINT014_LIVE_SMOKE_REVIEW.read_text()
    required = [
        "BLK-SYSTEM-014",
        "First live fixed-tool BLK-test MCP smoke under explicit human approval",
        "BLK-017 remains the active disabled transport contract",
        "BLK-018 remains the workspace/process-control probe contract",
        "BLK-019 remains the approval/source-evidence authorization contract",
        "APPROVAL_VALIDATED_SOURCE_BOUND",
        "explicit current human approval",
        "one exact source/request/workspace/profile/tool envelope",
        "stdio-only",
        "dependency-free JSON-RPC/MCP-subset smoke",
        "run_ast_validation",
        "synthetic isolated workspace",
        "does not use arbitrary shell",
        "does not use non-stdio transport",
        "does not run against /home/dad/BLK-System",
        "does not mutate primary repo",
        "does not authorize authoritative BEO publication",
        "does not authorize RTM generation",
        "does not read protected BLK-req vault bodies",
        "does not claim production sandbox or host-secret isolation",
    ]
    missing = [marker for marker in required if marker not in text]
    self.assertEqual(missing, [], f"Sprint 014 review markers missing: {missing}")
```

**Step 2: Run RED**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint014_live_fixed_tool_smoke_review_preserves_prerequisite_boundaries
```

Expected: FAIL because the review doc does not exist yet.

**Step 3: Create review doc**

Required sections:

1. Source docs reviewed: BLK-001, BLK-008, BLK-017, BLK-018, BLK-019, Sprint 010 future slicing, Sprint 013 closeout.
2. Positive authority: exactly one first live stdio fixed-tool smoke after explicit human approval.
3. Prerequisite gates: BLK-017/018/019 accepted and preserved.
4. Live-smoke constraints: dependency-free stdio JSON-RPC/MCP subset, one fixed tool, synthetic isolated workspace, bounded timeout/output, replay bundle.
5. Non-authority markers: no arbitrary shell, no non-stdio transport, no real target repo, no primary source mutation, no active-vault reads, no authoritative BEO, no RTM, no production sandbox/host-secret claims.
6. Stop conditions and handoff to BLK-020 after successful smoke.

**Step 4: Run GREEN and shared gate**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint014_live_fixed_tool_smoke_review_preserves_prerequisite_boundaries
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates
git diff --check
```

Expected: PASS.

**Step 5: Commit/push/outcome**

```bash
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
git add docs/reviews/BLK-SYSTEM-014_live-fixed-tool-smoke-boundary-review.md python/test_active_doctrine_review_gates.py
git diff --cached --name-only
git commit -m "docs: define blk-system sprint 014 live smoke boundary"
git push
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-014_task-001-outcome.md`.

---

## 8. Task 2 — Non-executing Sprint 014 live-smoke preflight aggregator

**Objective:** Add a new module that accepts a Sprint 014 live-smoke preflight only when BLK-017/018/019 evidence and explicit live-smoke gating match exactly, without spawning a process yet.

**Files:**

- Create: `python/blk_test_mcp_fixed_tool_live_smoke.py`
- Create: `python/test_blk_test_mcp_fixed_tool_live_smoke.py`
- Outcome: `docs/outcomes/BLK-SYSTEM-014_task-002-outcome.md`

**Step 1: Write failing tests**

Create tests for:

- exact BLK-019 approval decision + `live_smoke_enabled=True` accepts preflight;
- default/absent `live_smoke_enabled` rejects;
- `codex-live`/`BLK_APPROVE_CODEX_LIVE` approval cannot pass because BLK-019 validation rejects it;
- mismatched source evidence hash, authorization request hash, requested tool, test profile, workspace identity, or timeout/output profile rejects;
- non-stdio transport rejects;
- multi-tool, unknown-tool, wildcard-tool, and shell-like tool requests reject;
- returned preflight evidence carries no source-write/BEO/RTM/active-vault authority.

Core test shape:

```python
import unittest

from blk_test_mcp_approval_authorization import build_authorization_request, validate_blk_test_approval_record
from blk_test_mcp_disabled_transport import build_disabled_transport_descriptor
from blk_test_mcp_fixed_tool_live_smoke import evaluate_sprint014_live_smoke_preflight

class Sprint014LiveSmokePreflightTest(unittest.TestCase):
    def test_accepts_exact_approval_and_explicit_live_smoke_flag_without_starting_process(self):
        request = valid_authorization_request()
        approval = valid_approval_record(request)
        approval_decision = validate_blk_test_approval_record(approval, request, now=NOW_S14)
        descriptor = build_disabled_transport_descriptor(transport="stdio")

        decision = evaluate_sprint014_live_smoke_preflight(
            descriptor=descriptor,
            authorization_request=request,
            approval_decision=approval_decision,
            requested_tool="run_ast_validation",
            live_smoke_enabled=True,
            human_approval_checkpoint="EXPLICIT_SPRINT014_OPERATOR_APPROVAL_RECORDED",
        )

        self.assertEqual(decision["decision"], "LIVE_SMOKE_PREFLIGHT_ACCEPTED")
        self.assertEqual(decision["sprint"], "BLK-SYSTEM-014")
        self.assertTrue(decision["live_smoke_authorized"])
        self.assertEqual(decision["live_mcp_authorized_scope"], "ONE_RUN_ONE_APPROVED_FIXED_TOOL_STDIO_ONLY")
        self.assertFalse(decision["server_started"])
        self.assertFalse(decision["client_started"])
        self.assertEqual(decision["tools_executed"], [])
        self.assertFalse(decision["source_write_allowed"])
        self.assertEqual(decision["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(decision["rtm_status"], "NOT_GENERATED")
        self.assertFalse(decision["active_vault_read"])
```

**Step 2: Run RED**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_mcp_fixed_tool_live_smoke
```

Expected: FAIL because the module does not exist.

**Step 3: Implement minimal preflight module**

Required public API:

```python
ALLOWED_SPRINT014_FIXED_TOOLS = ("run_ast_validation",)


def build_sprint014_live_smoke_authorization_request(*, source_report, workspace_identity, timeout_output_profile):
    """Return a BLK-019 authorization request for the first fixed-tool live smoke only."""


def evaluate_sprint014_live_smoke_preflight(
    *,
    descriptor,
    authorization_request,
    approval_decision,
    requested_tool,
    live_smoke_enabled,
    human_approval_checkpoint,
    transport="stdio",
):
    """Accept one-run Sprint 014 preflight evidence; do not start processes."""
```

Implementation constraints:

- Import only safe existing helper modules and standard library modules needed for hash/copy validation.
- Call/replicate stdio metadata checks so non-stdio rejects.
- Require `approval_decision["decision"] == "APPROVAL_VALIDATED_SOURCE_BOUND"`.
- Require `approval_decision["authorization_request_hash"]` to equal the stable hash of `authorization_request`.
- Require `approval_decision["source_evidence_hash"]` to equal the stable hash of `authorization_request["source_evidence"]`.
- Require `requested_tool == "run_ast_validation"` and `authorization_request["requested_tools"] == ["run_ast_validation"]`.
- Require `live_smoke_enabled is True` and `human_approval_checkpoint == "EXPLICIT_SPRINT014_OPERATOR_APPROVAL_RECORDED"`.
- Return non-executing preflight evidence with `server_started: False`, `client_started: False`, `network_called: False`, `subprocess_called: False`, and `tools_executed: []`.

**Step 4: Run GREEN and gates**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_mcp_fixed_tool_live_smoke
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_mcp_approval_authorization python.test_blk_test_mcp_disabled_transport
python -m py_compile python/blk_test_mcp_fixed_tool_live_smoke.py
git diff --check
```

Expected: PASS.

**Step 5: Commit/push/outcome**

```bash
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
git add python/blk_test_mcp_fixed_tool_live_smoke.py python/test_blk_test_mcp_fixed_tool_live_smoke.py
git diff --cached --name-only
git commit -m "feat: add blk-test sprint 014 live smoke preflight"
git push
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-014_task-002-outcome.md`.

---

## 9. Task 3 — Dependency-free stdio fixed-tool smoke harness

**Objective:** Implement the bounded local stdio process path and one fixed `run_ast_validation` tool against synthetic isolated workspaces, still without running the official first live smoke.

**Files:**

- Modify: `python/blk_test_mcp_fixed_tool_live_smoke.py`
- Modify: `python/test_blk_test_mcp_fixed_tool_live_smoke.py`
- Outcome: `docs/outcomes/BLK-SYSTEM-014_task-003-outcome.md`

**Step 1: Write failing tests**

Add tests for:

- fixed live registry exposes only `run_ast_validation` for first smoke;
- `resolve_sprint014_fixed_tool_command(...)` returns a static list command and rejects caller-supplied command/args;
- workspace guard rejects `/home/dad/BLK-System`, `/`, `$HOME`, absolute protected-vault paths, traversal, and symlink escape;
- workspace guard accepts a temp synthetic workspace containing `src/smoke_fixture.py`;
- successful stdio server transcript returns PASS when the fixture parses and contains `SMOKE_FIXTURE = True`;
- parse error returns FAIL with bounded output;
- missing fixture returns BLOCKED and remains non-authoritative;
- timeout kills the process group and returns `FATAL_TIMEOUT`;
- output flood kills through the same cleanup path and returns `FATAL_OUTPUT_FLOOD`;
- AST-aware source scan rejects unsafe capability surfaces (`shell=True`, `os.system`, socket/listener imports, `requests`, `urllib`, `http.server`, `eval`, `exec`, `importlib`, package-manager execution, `git commit`, `git push`) while allowing protected-prefix constants only inside guard/rejection data.

**Step 2: Run RED**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_mcp_fixed_tool_live_smoke
```

Expected: new tests fail until the runner/guards exist.

**Step 3: Implement fixed-tool stdio harness**

Add public helpers:

```python
def fixed_sprint014_live_tool_registry_descriptor():
    """Return descriptor metadata for the one first-smoke fixed tool."""


def validate_sprint014_smoke_workspace(*, workspace_path, workspace_identity, authorization_request):
    """Validate an approved synthetic isolated workspace without reading protected vaults."""


def resolve_sprint014_fixed_tool_command(*, tool_name, workspace_path):
    """Return a static stdio child-process command for the approved fixed tool."""


def run_sprint014_fixed_tool_stdio_smoke(
    *,
    preflight_decision,
    workspace_path,
    timeout_seconds,
    output_byte_limit,
):
    """Run one bounded stdio JSON-RPC/MCP-subset smoke and return sanitized evidence."""
```

Harness requirements:

- Use `subprocess.Popen([...], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True, shell=False, start_new_session=True, cwd=str(workspace_path), env=scrubbed_env)`.
- Child command must be static: Python interpreter + isolated flags + an in-module child entrypoint flag such as `--sprint014-stdio-child` + `--tool run_ast_validation` + a prevalidated workspace path. Do not use dynamic `-c`, caller-supplied commands, or caller-supplied extra arguments.
- Child process reads line-delimited JSON requests and writes line-delimited JSON responses for a minimal MCP subset:
  - `initialize`
  - `tools/list`
  - `tools/call` for `run_ast_validation`
- `run_ast_validation` may only inspect `src/smoke_fixture.py` inside the synthetic workspace and run `ast.parse` on that file.
- The tool must return:
  - `PASS` when the file parses and contains `SMOKE_FIXTURE = True`;
  - `FAIL` when AST parsing fails;
  - `BLOCKED` when the expected synthetic fixture is absent or workspace validation fails.
- Use binary pipe reads for byte-accurate output limits, then decode bounded excerpts with `errors="replace"`.
- Use one shared kill path for timeout and output flood.
- Bound stdout/stderr/transcript bytes and return compressed/sanitized first/last lines only.
- Always set non-authority fields: no source write/staging/commit/push, `beo_publication: DRAFT_ONLY`, `rtm_status: NOT_GENERATED`, `active_vault_read: False`.

**Step 4: Run GREEN and source-scan gate**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_mcp_fixed_tool_live_smoke
python - <<'PY'
from pathlib import Path
text = Path('python/blk_test_mcp_fixed_tool_live_smoke.py').read_text()
forbidden = [
    'shell=True', 'os.system', 'socket', 'requests', 'urllib', 'http.server',
    'importlib', 'pip ', 'npm ', 'npx ', 'git commit', 'git push',
]
violations = [marker for marker in forbidden if marker in text]
if violations:
    raise SystemExit(f'forbidden live-smoke source markers: {violations}')
required_guard_markers = ['docs/active', 'docs/requirements', 'docs/use_cases']
missing_guards = [marker for marker in required_guard_markers if marker not in text]
if missing_guards:
    raise SystemExit(f'missing protected-prefix guard constants: {missing_guards}')
print('Sprint 014 live-smoke source scan: PASS')
PY
git diff --check
```

Expected: PASS.

**Step 5: Commit/push/outcome**

```bash
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
git add python/blk_test_mcp_fixed_tool_live_smoke.py python/test_blk_test_mcp_fixed_tool_live_smoke.py
git diff --cached --name-only
git commit -m "feat: add bounded stdio fixed-tool smoke harness"
git push
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-014_task-003-outcome.md`.

---

## 10. Task 4 — Commit-before-approval checkpoint and first live smoke

**Objective:** Commit/push the live-smoke wrapper first, verify a clean worktree, pause for explicit human approval bound to that committed implementation, then run exactly one approved fixed-tool live smoke against a marker-owned synthetic isolated workspace and record replay-safe evidence.

**Files:**

- Modify: `python/blk_test_mcp_fixed_tool_live_smoke.py` if a small orchestration wrapper is needed
- Modify: `python/test_blk_test_mcp_fixed_tool_live_smoke.py` if wrapper tests are needed
- Create: `docs/outcomes/BLK-SYSTEM-014_task-004-outcome.md`

**Step 1: Write failing orchestration tests**

Add tests for a top-level wrapper:

```python
def test_first_live_smoke_requires_human_checkpoint_and_exact_envelope(self):
    with self.assertRaisesRegex(ValueError, "explicit human approval"):
        run_sprint014_first_live_smoke(
            source_report=SOURCE_REPORT_S14,
            approval_record=valid_approval_record(valid_authorization_request()),
            requested_tool="run_ast_validation",
            workspace_path=self.synthetic_workspace,
            run_id="BLK-SYSTEM-014-SMOKE-001",
            now=NOW_S14,
            live_smoke_enabled=False,
            human_approval_checkpoint="",
        )
```

Also add a positive test with a temp synthetic workspace, current approval record, and explicit checkpoint. The positive test may run the same bounded stdio harness in test mode but must use temp fixtures only.

**Step 2: Run RED**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_mcp_fixed_tool_live_smoke
```

Expected: wrapper tests fail until orchestration exists.

**Step 3: Implement orchestration wrapper with mechanical approval/replay enforcement**

Required public API:

```python
def run_sprint014_first_live_smoke(
    *,
    source_report,
    approval_record,
    requested_tool,
    workspace_path,
    run_id,
    now,
    live_smoke_enabled,
    human_approval_checkpoint,
    used_approval_ids=None,
    used_run_ids=None,
    implementation_commit_hash=None,
    driver_hash=None,
):
    """Validate BLK-019/Sprint014 approval, accept preflight, run one stdio fixed-tool smoke, and return replay evidence."""
```

Behavior:

1. Build authorization request with `build_sprint014_live_smoke_authorization_request(...)`.
2. Validate approval with `validate_blk_test_approval_record(...)`.
3. Require `approval_record["approval_kind"] == "blk-test-mcp-live-smoke"`.
4. Require current live-smoke timestamps; the shared static timestamps in §5 are test-only and must not be used for the real live smoke.
5. Require exact `run_id`, `implementation_commit_hash`, `driver_hash`, requested tool, workspace identity, timeout/output profile, and envelope hash in the approval record or Sprint 014 approval extension.
6. Reject replay by requiring caller-supplied `used_approval_ids` and `used_run_ids` sets and rejecting duplicates before process start.
7. Evaluate Sprint 014 preflight with `evaluate_sprint014_live_smoke_preflight(...)`.
8. Validate marker-owned synthetic workspace, run-scoped cache root, run-scoped lock root, startup purge, no `.git`, no repo ancestor/descendant, protected-prefix rejection, and no symlink escape.
9. Run exactly one `run_ast_validation` stdio smoke.
10. Own guarded cleanup in the wrapper on every terminal status; the ad hoc driver must not be the primary cleanup authority.
11. Sanitize and return evidence:
   - `sprint: BLK-SYSTEM-014`
   - `run_id`
   - `tool_name`
   - `status` in `PASS`, `FAIL`, `BLOCKED`, `FATAL_TIMEOUT`, `FATAL_OUTPUT_FLOOD`, `TRANSPORT_ERROR`, `OPERATOR_INTERRUPTED`
   - approval/request/source hashes
   - transcript/replay hash
   - bounded first/last output excerpts
   - cleanup status
   - non-authority fields.

**Step 4: Focused GREEN**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_mcp_fixed_tool_live_smoke
git diff --check
```

Expected: PASS.

**Step 5: Commit/push wrapper code before requesting approval**

Before requesting human approval, commit and push any Task 4 wrapper/test changes, then verify the worktree is clean. Approval must bind to committed implementation code, not an unreviewed dirty worktree.

```bash
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
git add python/blk_test_mcp_fixed_tool_live_smoke.py python/test_blk_test_mcp_fixed_tool_live_smoke.py
git diff --cached --name-only
git commit -m "feat: prepare approved blk-test fixed-tool live smoke"
git push
git status --short --branch
git log -1 --oneline
```

Expected: clean status and a commit hash to include in the approval envelope.

**Step 6: Mandatory human approval checkpoint before real smoke**

Before running the first non-test live smoke, present the exact envelope to the operator and stop until they approve. The request must include:

```text
Sprint: BLK-SYSTEM-014
Run ID: BLK-SYSTEM-014-SMOKE-001
Approval ID: fresh one-run approval ID
Implementation commit hash: <current pushed Task 4 commit>
Driver hash: <sha256 of the exact live-smoke driver content>
Tool: run_ast_validation
Transport: stdio only
Workspace: marker-owned synthetic isolated temporary workspace only, under approved run-scoped scratch root, with no .git and no repo ancestor/descendant
Source report identity: reports/BLK-SYSTEM-014/synthetic-source-report.json / source-report-BLK-SYSTEM-014-smoke
Trace artifact: REQ-S14-SMOKE-001 / sha256:1111111111111111111111111111111111111111111111111111111111111111
Timeout/output: 5s / 4096 bytes
Approval kind: blk-test-mcp-live-smoke
Approval timestamp/expiry: current operator approval time with fresh bounded expiry; do not use static test fixture timestamps
Replay policy: reject duplicate approval ID and duplicate run ID before process start
Non-authority: no arbitrary shell, no non-stdio transport, no real target repo, no source mutation, no authoritative BEO, no RTM, no protected BLK-req vault reads
```

Do not proceed unless the operator explicitly approves this exact envelope.

**Step 7: Run first approved smoke**

After approval only, run a small Python driver from the repository root that:

1. Creates a temp synthetic workspace.
2. Writes `src/smoke_fixture.py` with `SMOKE_FIXTURE = True`.
3. Builds the exact source report and approval record.
4. Calls `run_sprint014_first_live_smoke(...)` with `live_smoke_enabled=True` and `human_approval_checkpoint="EXPLICIT_SPRINT014_OPERATOR_APPROVAL_RECORDED"`.
5. Prints bounded JSON evidence.
6. Lets `run_sprint014_first_live_smoke(...)` own guarded cleanup and return cleanup evidence.

Expected status: `PASS`. If status is `FAIL`, `BLOCKED`, `FATAL_TIMEOUT`, `FATAL_OUTPUT_FLOOD`, `TRANSPORT_ERROR`, or `OPERATOR_INTERRUPTED`, record the evidence, create the Task 4 outcome/aborted closeout, and stop; do not retry with a broader envelope and do not create BLK-020.

**Step 8: Outcome only after smoke**

Create `docs/outcomes/BLK-SYSTEM-014_task-004-outcome.md` with:

- RED/GREEN test evidence;
- exact human approval envelope and timestamp;
- smoke command/driver summary;
- PASS/FAIL/BLOCKED evidence;
- approval/request/source/transcript hashes;
- cleanup result;
- explicit statement that no real target repo, source mutation, authoritative BEO, RTM, active-vault body read, arbitrary shell, or non-stdio transport occurred.

Commit and push the outcome doc separately:

```bash
git add docs/outcomes/BLK-SYSTEM-014_task-004-outcome.md
git diff --cached --name-only
git commit -m "docs: record blk-system sprint 014 first smoke outcome"
git push
```

---

## 11. Task 5 — Active BLK-020 doctrine and cross-reference gates

**Objective:** Publish Sprint 014 first-smoke behavior as active doctrine without broadening BLK-test MCP into production authority.

**Hard prerequisite:** Task 5 is allowed only after Task 4 records exactly one approved live smoke with status `PASS` and cleanup verified. If Task 4 records `FAIL`, `BLOCKED`, `FATAL_TIMEOUT`, `FATAL_OUTPUT_FLOOD`, `TRANSPORT_ERROR`, or `OPERATOR_INTERRUPTED`, stop and do not create BLK-020.

**Files:**

- Create: `docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md`
- Modify: `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md`
- Modify: `docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md`
- Modify: `docs/BLK-019_blk-test-mcp-approval-source-evidence-authorization.md`
- Modify: `python/test_active_doctrine_review_gates.py`
- Outcome: `docs/outcomes/BLK-SYSTEM-014_task-005-outcome.md`

**Step 1: Write failing doctrine gates**

Add constant:

```python
BLK020 = ROOT / "docs" / "BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md"
```

Add test:

```python
def test_blk020_records_sprint014_first_live_smoke_without_production_authority(self):
    self.assertTrue(BLK020.exists(), "BLK-020 first live smoke doctrine missing")
    text = BLK020.read_text()
    required = [
        "**Status:** Active first-smoke evidence contract",
        "BLK-SYSTEM-014",
        "First live fixed-tool BLK-test MCP smoke under explicit human approval",
        "BLK-017 remains the active disabled transport contract",
        "BLK-018 remains the workspace/process-control probe contract",
        "BLK-019 remains the approval/source-evidence authorization contract",
        "run_ast_validation",
        "stdio-only",
        "dependency-free JSON-RPC/MCP-subset smoke",
        "synthetic isolated workspace",
        "one exact source/request/workspace/profile/tool envelope",
        "PASS/FAIL/BLOCKED evidence",
        "does not authorize production BLK-test MCP",
        "does not use arbitrary shell",
        "does not use non-stdio transport",
        "does not run against real target repositories",
        "does not mutate primary repo",
        "does not authorize authoritative BEO publication",
        "does not authorize RTM generation",
        "does not read protected BLK-req vault bodies",
        "does not claim production sandbox or host-secret isolation",
        "python/blk_test_mcp_fixed_tool_live_smoke.py",
        "python/test_blk_test_mcp_fixed_tool_live_smoke.py",
    ]
    missing = [marker for marker in required if marker not in text]
    self.assertEqual(missing, [], f"BLK-020 markers missing: {missing}")
```

Add cross-reference test:

```python
def test_blk017_018_019_020_cross_reference_first_smoke_without_broad_authority(self):
    expectations = {
        BLK017: ["BLK-020", "first live fixed-tool", "BLK-017 remains the active disabled transport contract"],
        BLK018: ["BLK-020", "synthetic isolated workspace", "does not authorize production BLK-test MCP"],
        BLK019: ["BLK-020", "explicit human approval", "one exact source/request/workspace/profile/tool envelope"],
        BLK020: ["BLK-017", "BLK-018", "BLK-019", "BLK-SYSTEM-014"],
    }
    for path, markers in expectations.items():
        text = path.read_text()
        missing = [marker for marker in markers if marker not in text]
        self.assertEqual(missing, [], f"{path.relative_to(ROOT)} missing {missing}")
```

**Step 2: Run RED**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates
```

Expected: FAIL because BLK-020 and cross-references are missing.

**Step 3: Create BLK-020 and patch cross-references narrowly**

BLK-020 required sections:

1. Purpose.
2. Current first-smoke authority boundary.
3. Prerequisite contracts: BLK-017, BLK-018, BLK-019.
4. Approved first-smoke envelope.
5. Fixed-tool registry and stdio-only rule.
6. Synthetic workspace and protected-vault exclusions.
7. PASS/FAIL/BLOCKED and replay evidence shape.
8. Non-authority checklist.
9. Stop conditions.
10. Implementation and tests.
11. Handoff to future sprint.

Patch BLK-017/018/019 only to say:

- BLK-020 records the accepted first-smoke evidence contract.
- BLK-017 remains disabled by default for generic startup paths.
- BLK-018 workspace/process controls remain prerequisite constraints.
- BLK-019 approval/source-evidence remains prerequisite authorization validation.
- BLK-020 does not authorize production BLK-test MCP, arbitrary tools, real target execution, source mutation, authoritative BEO, RTM, or protected-vault body reads.

**Step 4: Run GREEN and gates**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates
git diff --check
```

Expected: PASS.

**Step 5: Commit/push/outcome**

```bash
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
git add docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md docs/BLK-019_blk-test-mcp-approval-source-evidence-authorization.md python/test_active_doctrine_review_gates.py
git diff --cached --name-only
git commit -m "docs: define blk-test first live fixed-tool smoke contract"
git push
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-014_task-005-outcome.md`.

---

## 12. Task 6 — Full-suite verification and Sprint 015 handoff closeout

**Objective:** Close BLK-SYSTEM-014 with full verification evidence and a narrow Sprint 015 handoff seed.

**Files:**

- Create: `docs/outcomes/BLK-SYSTEM-014_sprint-closeout.md`
- Optionally modify: `docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md` only if a RED gate proves stale post-Sprint-014 wording; otherwise preserve history.

**Step 1: Full verification**

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s python -p 'test_*.py'
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python
go test ./...
go vet ./...
git diff --check
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
find python -type d -name __pycache__ -prune -exec rm -rf {} +
git status --short --branch
```

Expected:

- Python `unittest` suite passes.
- Python pytest suite passes with cache provider disabled.
- `go test ./...` passes.
- `go vet ./...` passes.
- `git diff --check` passes.
- No `python/__pycache__` or pytest cache remains staged/untracked.

**Step 2: Create closeout doc**

`docs/outcomes/BLK-SYSTEM-014_sprint-closeout.md` must include:

- sprint ID and timestamp;
- task commit table;
- outcome doc table;
- exact verification commands and results;
- explicit statement that Sprint 014 ran only the approved first fixed-tool stdio smoke against a synthetic isolated workspace;
- explicit statement that Sprint 014 does not authorize production BLK-test MCP, arbitrary shell, non-stdio transport, cyber execution, real target execution, source mutation/staging/commit/push as BLK-test behavior, authoritative BEO publication, RTM generation, RTM drift rejection, active BLK-req vault body reads, production sandbox claims, or host-secret isolation claims;
- first-smoke evidence summary: approval/request/source/transcript hashes, status, bounded output, cleanup result;
- Sprint 015 handoff seed:

```text
BLK-SYSTEM-015 — Draft BEO publication gate review, still not authoritative unless explicitly approved
```

Narrow Sprint 015 prerequisites:

1. BLK-020 first-smoke evidence must remain source-bound and replayable.
2. Draft BEO projection, if reviewed, must preserve `beo_publication: "DRAFT_ONLY"` unless a later explicit publication sprint grants authority.
3. BLOCKED smoke evidence must not project to success.
4. RTM generation remains disabled and separately owned by a later RTM sprint.
5. Active BLK-req vault bodies remain unread unless a later explicit access-policy sprint grants authority.

**Step 3: Validate closeout**

```bash
python - <<'PY'
from pathlib import Path
path = Path('docs/outcomes/BLK-SYSTEM-014_sprint-closeout.md')
text = path.read_text()
required = [
    'BLK-SYSTEM-014',
    'approved first fixed-tool stdio smoke',
    'synthetic isolated workspace',
    'does not authorize production BLK-test MCP',
    'does not use arbitrary shell',
    'does not use non-stdio transport',
    'does not run against real target repositories',
    'does not mutate primary repo',
    'does not authorize authoritative BEO publication',
    'does not authorize RTM generation',
    'does not read protected BLK-req vault bodies',
    'BLK-SYSTEM-015',
    'Draft BEO publication gate review',
]
missing = [marker for marker in required if marker not in text]
if missing:
    raise SystemExit(f'missing closeout markers: {missing}')
fence = chr(96) * 3
if text.count(fence) % 2:
    raise SystemExit('unbalanced markdown fences')
print('BLK-SYSTEM-014 closeout markers: PASS')
PY
```

Expected: PASS.

**Step 4: Commit/push closeout**

```bash
git add docs/outcomes/BLK-SYSTEM-014_sprint-closeout.md
git diff --cached --name-only
git commit -m "docs: close out blk-system sprint 014"
git push
```

Then send concise Discord summary with:

```text
MEDIA:/home/dad/BLK-System/docs/outcomes/BLK-SYSTEM-014_sprint-closeout.md
```

---

## 13. Final acceptance criteria

BLK-SYSTEM-014 is complete only when all are true:

- `docs/plans/blk-system-014_first-live-fixed-tool-blk-test-mcp-smoke.md` is committed.
- `docs/reviews/BLK-SYSTEM-014_live-fixed-tool-smoke-boundary-review.md` exists and passes the active doctrine gate.
- `python/blk_test_mcp_fixed_tool_live_smoke.py` exists and is dependency-free standard-library code.
- `python/test_blk_test_mcp_fixed_tool_live_smoke.py` proves:
  - explicit Sprint 014 human approval checkpoint;
  - exact BLK-019 approval/source/request binding;
  - stdio-only transport;
  - single fixed-tool `run_ast_validation` registry;
  - no arbitrary shell or caller-supplied command path;
  - synthetic workspace guard and real-repo/protected-vault rejection;
  - bounded timeout/output and shared kill path;
  - PASS/FAIL/BLOCKED/FATAL evidence mapping;
  - replay-safe transcript/source/request/approval hashes;
  - no source-write, BEO, RTM, or active-vault authority.
- BLK-017/018/019 remain intact and cross-reference BLK-020 without implying broad production authority.
- `docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md` exists as active first-smoke doctrine.
- The first approved live smoke ran exactly once from committed/pushed code against a marker-owned synthetic isolated workspace and returned `PASS` with cleanup verified; if it did not PASS, the sprint stopped after documenting the failure and BLK-020 was not created.
- Every task has a matching pushed `docs/outcomes/BLK-SYSTEM-014_task-00N-outcome.md`.
- Sprint closeout is pushed.
- Final verification passes:
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s python -p 'test_*.py'`
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python`
  - `go test ./...`
  - `go vet ./...`
  - `git diff --check`
- Final worktree is clean except any deliberate, reported, user-approved untracked files.

---

## 14. Expected artifact set

```text
docs/plans/blk-system-014_first-live-fixed-tool-blk-test-mcp-smoke.md
docs/reviews/BLK-SYSTEM-014_live-fixed-tool-smoke-boundary-review.md
python/blk_test_mcp_fixed_tool_live_smoke.py
python/test_blk_test_mcp_fixed_tool_live_smoke.py
python/test_active_doctrine_review_gates.py
docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md
docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md
docs/BLK-019_blk-test-mcp-approval-source-evidence-authorization.md
docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md
docs/outcomes/BLK-SYSTEM-014_task-000-outcome.md
docs/outcomes/BLK-SYSTEM-014_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-014_task-002-outcome.md
docs/outcomes/BLK-SYSTEM-014_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-014_task-004-outcome.md
docs/outcomes/BLK-SYSTEM-014_task-005-outcome.md
docs/outcomes/BLK-SYSTEM-014_sprint-closeout.md
```

---

## 15. Executor notes

- Do not stage with `git add .`, `git add -A`, or broad wildcards.
- Remove `python/__pycache__`, `python/.pytest_cache`, and `.pytest_cache` before status/commit.
- Do not weaken BLK-017 disabled default behavior; create Sprint 014 positive path only in the new module.
- Do not repurpose Sprint 012 inert process probes as arbitrary executor authority.
- Do not treat BLK-019 validation as sufficient to start live smoke; Task 4 requires a fresh Sprint 014 explicit human approval checkpoint.
- Do not make outcome docs self-referential with their own final commit hash. Record pre-commit verification in the doc; record post-push hash/status in executor summary or sprint closeout.
- If the first approved smoke fails, document the bounded failure evidence and stop. Do not silently retry with broader tools, longer timeouts, real repos, or altered approvals.
- Keep Discord updates concise and only after meaningful task completion/push events.
