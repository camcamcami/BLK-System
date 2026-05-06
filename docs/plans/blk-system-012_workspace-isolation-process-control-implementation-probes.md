# blk-system-012 — Workspace Isolation and Process-Control Implementation Probes

> **For Hermes:** Use `blk-system-sprint-execution` to execute this plan task-by-task with strict RED/GREEN gates, exact-path staging, outcome documentation, and GitHub push discipline. This sprint implements deterministic local workspace/process-control probes only. Do not use Hindsight. Do not invoke BLK-test MCP live transport, live MCP client/server startup, live fixed-tool BLK-test execution, BEO publication, RTM generation, active BLK-req vault reads, cyber tooling, or production sandbox/secret-isolation claims.

**Sprint ID:** `blk-system-012` / `BLK-SYSTEM-012`
**Title:** Workspace Isolation and Process-Control Implementation Probes
**Component emphasis:** BLK-test MCP readiness controls using inert local fixtures only; not a `blk-pipe` component sprint.
**Goal:** Prove deterministic local probes for workspace clone/isolation decisions, path guards, teardown, locking, process-tree kill, timeout handling, output-flood cleanup, cache/environment bounds, and replay evidence without granting live BLK-test MCP authority.

**Architecture:** Sprint 012 adds a dependency-free Python probe module and unittest gates that operate only on synthetic, marker-protected local fixtures under test-owned temporary roots. The probes may spawn fixed inert Python child processes to verify timeout/flood/process-tree cleanup, but they must not expose arbitrary command execution or call existing fixed BLK-test tool descriptors. Sprint 012 may create active doctrine for the probe contract, but BLK-017 remains the disabled transport contract and no live MCP server/client startup is authorized.

**Tech Stack:** Markdown review/design artifacts, dependency-free Python `unittest` gates, Python standard library (`tempfile`, `pathlib`, `os`, `shutil`, `subprocess`, `signal`, `threading`/`multiprocessing` as needed), existing Go verification as regression guard only.

---

## 0. Current Known State

Repository:

```text
/home/dad/BLK-System
```

Planning preflight when this document was authored:

```text
date                         -> 2026-05-06 13:27:15 AEST
git status --short --branch  -> ## main...origin/main
HEAD                         -> 6ae3e44 docs: add blk-system sprint 011 plan
```

Source seed:

```text
BLK-SYSTEM-012 — Workspace Isolation and Process-Control Implementation Probes
```

Source doctrine and review artifacts to align:

```text
docs/BLK-001_blk-system-master-architecture.md
docs/BLK-003_blk-pipe-blk-test-orchestration.md
docs/BLK-008_blk-test-mcp-execution-server.md
docs/BLK-013_blk-test-handoff-fixture-contract.md
docs/BLK-014_blk-execution-outcome-fixture-shape.md
docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md
docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md
docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md
docs/outcomes/BLK-SYSTEM-011_sprint-closeout.md
docs/reviews/BLK-SYSTEM-010_fixture-to-live-gap-register.md
docs/reviews/BLK-SYSTEM-010_sandbox-capability-readiness-spec.md
docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md
docs/reviews/BLK-SYSTEM-011_transport-boundary-review.md
python/blk_test_mcp_disabled_transport.py
python/test_blk_test_mcp_disabled_transport.py
python/test_active_doctrine_review_gates.py
```

Naming correction preserved:

- Use `BLK-SYSTEM-012` / `blk-system-012` for this system-level BLK-test MCP readiness sprint.
- Do **not** use `BLK-012`; `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md` already exists as active BLK-pipe guidance.
- Do **not** use `BLK-PIPE-012`; this sprint is not scoped to `blk-pipe` mutation logic.
- Do **not** use `BEB_012`; `BEB` is an artifact type and `beb_id` is a source/evidence field, not a sprint namespace.

---

## 1. BLK-001 Alignment Contract

Sprint 012 must preserve BLK-001's isolated-domain model:

| BLK-001 domain | Intent to preserve | Sprint 012 implication |
| --- | --- | --- |
| `blk-req` Legislative Gateway | Requirements/use cases remain HITL-authorized immutable active-vault artifacts. | Do not read protected BLK-req vault bodies, parse requirement bodies, or copy `docs/active/`, `docs/requirements/`, or `docs/use_cases/` body text into probes, logs, replay bundles, BEO-like fields, or RTM-like fields. |
| Architecture & Feature Planning | Hermes plans bounded work and produces implementation handoffs; BLK-test is not an architect/router. | Sprint 012 may define local probe contracts and evidence shapes only; it must not let BLK-test choose scope, architecture, approval, or requirement interpretation. |
| `blk-pipe` Blast Shield & Forge | `blk-pipe` owns deterministic source mutation, staging, Git allowlists, and forge/blast-shield authority. | Probe code must not mutate the primary repo, stage files, commit, push, run `git add`, run `git commit`, or replace `blk-pipe`. Human sprint execution may commit/push reviewed task work and outcome docs. |
| `blk-test` Physics Oracle | BLK-test may later verify physical reality and return bounded evidence. | Sprint 012 proves local workspace/process/resource controls with inert fixtures only. It must not execute the Sprint 011 fixed-tool registry, run real repo tests, or start live MCP. |
| RTM Aggregator Ledger | RTM remains a separate offline ledger comparing BEO trace hashes against active-vault hashes. | Sprint 012 must not generate RTM, emit coverage matrices, reject drift, or imply RTM authority. |
| Cryptographic baton | `version_hash` remains opaque source-bound evidence shared across domains. | If trace evidence is mentioned, preserve canonical `trace_artifacts[*].version_hash == sha256:<64-lowercase-hex>` as opaque metadata only; do not inspect active-vault bodies or generate new trace authority. |

Sprint 012 passes alignment only if every implementation and review artifact says what authority it does **not** grant.

---

## 2. Decision Register

| Decision ID | Question | Decision | Rationale | Implementation effect |
| --- | --- | --- | --- | --- |
| DEC-001 | Is Sprint 012 a `blk-pipe` sprint? | **No. It is `BLK-SYSTEM-012`.** | The scope crosses BLK-test workspace/process/resource readiness boundaries. | Use `BLK-SYSTEM-012` prefixes for review/outcome docs and `blk-system-012` plan naming. |
| DEC-002 | Does Sprint 012 authorize live BLK-test MCP? | **No.** | Sprint 010 sliced Sprint 012 as inert implementation probes before approval/source-evidence and first live smoke sprints. | No MCP server/client startup, no JSON-RPC handshake, no fixed-tool execution. |
| DEC-003 | Does Sprint 012 replace Sprint 011 disabled transport code? | **No.** | BLK-017 remains the active disabled transport contract. | Add a new module `python/blk_test_mcp_workspace_process_probes.py`; do not retrofit `python/blk_test_mcp_disabled_transport.py` unless a later gate explicitly requires a cross-reference. |
| DEC-004 | May Sprint 012 spawn subprocesses? | **Yes, but only fixed inert local process probes.** | Process-tree kill/timeout/flood behavior cannot be proven without controlled child processes. | Use hardcoded Python child/grandchild snippets; no shell, dynamic command API, package manager, repo tests, MCP client/server, network, or fixed BLK-test tool execution. |
| DEC-005 | May Sprint 012 use hardlinks? | **Only with synthetic marked fixtures and manifest guards.** | BLK-008 target-state wants same-filesystem hardlink decisions, but hardlinks are not write isolation. | Tests may hardlink inert fixture files under temp roots; no in-place writes to hardlinked source files; source manifests must remain unchanged. |
| DEC-006 | May Sprint 012 use global `/var/tmp` lock/purge paths? | **No for this sprint.** | Global purge/lock paths are too destructive for inert probes. | Use test-owned temporary roots, marker files, and ownership tokens. Future production-like paths need a later authority gate. |
| DEC-007 | How are task outcome docs handled? | **Commit and push after each task.** | User policy supersedes older sprint plans that deferred outcome docs until closeout. | Each task implementation commit is pushed; then the matching `docs/outcomes/BLK-SYSTEM-012_task-00N-outcome.md` is validated, committed, and pushed as a separate docs commit. |
| DEC-008 | Does Sprint 012 implement approval/source-evidence authorization? | **No. Sprint 013 owns that.** | Approval and source evidence binding are separate authority mechanics. | Any approval-looking input remains non-authorizing metadata and cannot enable execution. |
| DEC-009 | Does Sprint 012 create active doctrine? | **Yes, only as a probe contract if gates prove it.** | Future sprints need a discoverable current contract after probes exist. | Create `docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md` late in the sprint and cross-reference BLK-008/BLK-017 without enabling live MCP. |

---

## 3. Non-Goals and Hard Blocks

Sprint 012 must not implement, invoke, or imply:

- live BLK-test MCP;
- live MCP client/server startup;
- JSON-RPC/MCP handshake;
- Sprint 011 fixed-tool registry execution (`run_ast_validation`, `run_ipc_race_test`, `run_svg_export_purity_test`, `run_architecture_lint`);
- arbitrary shell, dynamic command execution, plugin-discovered tools, `shell=True`, `os.system`, `eval`, `exec`, auto-fix, source-write, stage, or commit tools;
- tests against real project repositories;
- mutation of `/home/dad/BLK-System` as a probe target;
- `git clone`, `git worktree`, `git add`, `git commit`, `git stash`, broad reset/checkout, or source staging inside probe code/tests;
- authoritative BLK-test verdict authority;
- authoritative BEO publication;
- RTM generation;
- RTM drift rejection authority;
- active BLK-req vault reads or requirement-body parsing;
- approval-channel mechanics, operator token validation, or source-evidence authorization;
- live Codex/ExecutionPipe/BLK-pipe tactical execution as a probe behavior;
- package-manager network installs, TypeScript MCP SDK runtime, sockets, HTTP, WebSockets, TCP, UDP, daemons, listeners, or network callbacks;
- production sandbox/container/cgroup/VM/namespace/seccomp/AppArmor/SELinux enforcement claims;
- production host-secret isolation claims;
- cyber tooling or execution against live targets.

Allowed work:

```text
dependency-free Python probe code
Python unittest RED/GREEN gates
synthetic marker-protected temp fixture trees
same-filesystem/hardlink clone decision probes
path traversal / symlink escape / protected-vault rejection probes
root-anchored startup purge and teardown probes under test-owned roots
atomic temp-root lock and stale/live lock probes
fixed inert Python child/grandchild process probes
bounded timeout/output-flood cleanup probes
cache path, synthetic environment scrubber, output compression, replay evidence probes
Markdown review/outcome/closeout artifacts
active BLK-018 probe-contract doctrine after implementation gates pass
```

---

## 4. Invariants to Preserve

1. `BLK-SYSTEM-012` / `blk-system-012` naming is mandatory for this sprint.
2. `BEB` and `BEO` remain artifact types, not sprint IDs.
3. BLK-017 remains the active disabled transport contract; Sprint 012 must not enable transport.
4. No server starts, no client starts, no JSON-RPC handshake occurs, and no fixed BLK-test tool executes.
5. Process probes may spawn only fixed inert local child processes and must mark them as `inert_subprocess_called`, not live MCP or fixed-tool execution.
6. The process-kill path for timeout and output flood must be shared and awaited before lock release/teardown completion.
7. Any workspace source fixture must be synthetic, marker-protected, and under a test-owned temporary root; real repos and `.git` roots are rejected.
8. Cleanup helpers must be root-anchored, marker-validated, and unable to delete `/`, `$HOME`, the repo root, current working directory, unmarked directories, symlink escapes, or arbitrary glob matches.
9. Hardlink clone probes must acknowledge hardlinks are not write isolation; tests must prove the source manifest remains unchanged.
10. Cache and environment probes use run-scoped cache roots and synthetic env maps; never dump real host secrets into evidence.
11. Replay bundles are bounded, deterministic, and non-authoritative; they exclude protected bodies, secrets, raw unbounded logs, BEO publication fields, and RTM generation/drift fields.
12. Outcome documents are detailed Markdown files in `docs/outcomes/` and are committed/pushed after each task. Do not defer outcome-document commits/pushes until sprint closure.
13. Remove `python/__pycache__` before exact-path staging.
14. Do not use `git add .`, `git add -u`, `git stash`, broad reset, broad checkout, broad revert, or exact-path commits that include generated caches.

---

## 5. Controller Workflow for Each Task

For each task:

1. Preflight:

   ```bash
   cd /home/dad/BLK-System
   export PATH="$HOME/.local/bin:$PATH"
   git fetch origin main
   git status --short --branch
   git log -1 --oneline
   ```

2. Read the task's exact source docs before editing.
3. Add the focused RED gate first.
4. Run the focused test and capture expected RED.
5. Patch only the files named in the task.
6. Rerun the focused test for GREEN.
7. Run shared verification before the task implementation commit:

   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   python3 -m unittest discover -s python -p 'test_*.py'
   go test ./...
   go vet ./...
   git diff --check
   rm -rf python/__pycache__
   git status --short --branch
   ```

8. Stage only exact implementation/review files for the task. Exclude the outcome doc at this step.
9. Commit the task implementation/review artifact with the listed task commit message.
10. Push the task implementation/review commit:

    ```bash
    git push origin main
    git status --short --branch
    ```

11. Create the matching outcome document after the task commit is pushed:

    ```text
    docs/outcomes/BLK-SYSTEM-012_task-00N-outcome.md
    ```

    Outcome docs must record:

    - task objective;
    - exact files changed;
    - RED evidence;
    - GREEN evidence;
    - shared verification evidence;
    - review results;
    - implementation commit hash and remote push status;
    - explicit non-authority statement;
    - next task.

12. Validate, commit, and push the outcome document as a separate docs commit:

    ```bash
    python3 - <<'PY'
    from pathlib import Path
    p = Path('docs/outcomes/BLK-SYSTEM-012_task-00N-outcome.md')
    text = p.read_text()
    assert text.startswith('# BLK-System Sprint 012')
    assert text.count('```') % 2 == 0
    for i, line in enumerate(text.splitlines(), 1):
        assert line.rstrip() == line, f'trailing whitespace line {i}'
    required = [
        'BLK-SYSTEM-012',
        'Remote:',
        'does not authorize live BLK-test MCP',
        'does not authorize authoritative BEO publication',
        'does not authorize RTM generation',
    ]
    missing = [marker for marker in required if marker not in text]
    assert not missing, missing
    PY
    git diff --check
    git add docs/outcomes/BLK-SYSTEM-012_task-00N-outcome.md
    git diff --cached --check
    git commit -m "docs: record blk-system sprint 012 task N outcome"
    git push origin main
    git status --short --branch
    ```

13. Discord closeout for each task should be concise and attach the pushed outcome doc:

    ```text
    Done — BLK-SYSTEM-012 Task N implementation and outcome doc are committed and pushed.

    - Implementation commit: `<hash> <subject>`
    - Outcome commit: `<hash> docs: record blk-system sprint 012 task N outcome`
    - GitHub: `origin/main` aligned

    MEDIA:/home/dad/BLK-System/docs/outcomes/BLK-SYSTEM-012_task-00N-outcome.md
    ```

---

## 6. Task 1 — Add Sprint 012 Workspace/Process Boundary Review Gate

### Objective

Create the governing Sprint 012 review artifact and a persistent doctrine gate before writing workspace/process probe code.

### Files

Create:

- `docs/reviews/BLK-SYSTEM-012_workspace-process-control-review.md`

Modify:

- `python/test_active_doctrine_review_gates.py`

Outcome after implementation commit:

- `docs/outcomes/BLK-SYSTEM-012_task-001-outcome.md`

### Required behavior

The review artifact must include:

- `BLK-SYSTEM-012`;
- `Workspace Isolation and Process-Control Implementation Probes`;
- `deterministic local inert fixtures only`;
- `does not authorize live BLK-test MCP`;
- `does not authorize live MCP client/server startup`;
- `does not execute fixed-tool tests`;
- `does not mutate primary repo`;
- `does not stage files`;
- `does not commit`;
- `does not authorize authoritative BEO publication`;
- `does not authorize RTM generation`;
- `does not authorize RTM drift rejection authority`;
- `does not read protected BLK-req vault bodies`;
- `does not claim production sandbox/cgroup/VM enforcement`;
- `does not claim production host-secret isolation`;
- `Sprint 013 owns approval/source-evidence authorization mechanics`;
- `Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke`.

The doctrine test should add a focused assertion such as:

```python
def test_sprint012_workspace_process_review_is_inert_and_non_authorizing(self):
    self.assertTrue(SPRINT012_WORKSPACE_PROCESS_REVIEW.exists(), "Sprint 012 workspace/process review missing")
    text = SPRINT012_WORKSPACE_PROCESS_REVIEW.read_text()
    required = [
        "BLK-SYSTEM-012",
        "Workspace Isolation and Process-Control Implementation Probes",
        "deterministic local inert fixtures only",
        "does not authorize live BLK-test MCP",
        "does not authorize live MCP client/server startup",
        "does not execute fixed-tool tests",
        "does not mutate primary repo",
        "does not stage files",
        "does not commit",
        "does not authorize authoritative BEO publication",
        "does not authorize RTM generation",
        "does not authorize RTM drift rejection authority",
        "does not read protected BLK-req vault bodies",
        "does not claim production sandbox/cgroup/VM enforcement",
        "does not claim production host-secret isolation",
        "Sprint 013 owns approval/source-evidence authorization mechanics",
        "Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke",
    ]
    missing = [marker for marker in required if marker not in text]
    self.assertEqual(missing, [], f"Sprint 012 review markers missing: {missing}")
```

### RED/GREEN steps

1. Add the test and constant for the missing review artifact.
2. Run focused RED:

   ```bash
   python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v
   ```

   Expected RED: Sprint 012 workspace/process review missing.

3. Create `docs/reviews/BLK-SYSTEM-012_workspace-process-control-review.md` with the required markers, BLK-001 matrix, non-goals, allowed probe shapes, stop conditions, and pass/fail criteria.
4. Rerun focused GREEN:

   ```bash
   python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v
   ```

### Shared verification

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
rm -rf python/__pycache__
```

### Commit and push

```bash
git add python/test_active_doctrine_review_gates.py \
  docs/reviews/BLK-SYSTEM-012_workspace-process-control-review.md
git diff --cached --check
git commit -m "docs: add blk-system sprint 012 workspace process boundary gate"
git push origin main
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-012_task-001-outcome.md`.

---

## 7. Task 2 — Add Workspace Policy Descriptor, Clone Decision, Path Guards, and Cache Path Probes

### Objective

Add the first dependency-free Python probe module with inert workspace policy decisions, path escape rejection, protected-vault rejection, cache-jail path selection, and non-authority descriptors.

### Files

Create:

- `python/blk_test_mcp_workspace_process_probes.py`
- `python/test_blk_test_mcp_workspace_process_probes.py`

Outcome after implementation commit:

- `docs/outcomes/BLK-SYSTEM-012_task-002-outcome.md`

### Required public APIs

```python
def build_workspace_process_boundary_descriptor() -> dict[str, object]:
    """Return Sprint 012 non-authority descriptor metadata."""


def decide_clone_strategy(
    source_root,
    scratch_root,
    *,
    fallback_root=None,
    source_device=None,
    scratch_device=None,
    fallback_device=None,
) -> dict[str, object]:
    """Return a fail-closed hardlink/same-filesystem clone decision."""


def validate_workspace_relative_path(
    workspace_root,
    candidate_relative_path,
    *,
    protected_prefixes=("docs/active", "docs/requirements", "docs/use_cases"),
) -> dict[str, object]:
    """Validate a workspace-relative path without allowing escape or protected-vault access."""


def build_run_cache_paths(
    scratch_root,
    *,
    run_id: str,
) -> dict[str, object]:
    """Return run-scoped cache paths outside source/workspace roots."""
```

Required status vocabulary:

```text
HARDLINK_CLONE_SELECTED
SAME_FILESYSTEM_FALLBACK_SELECTED
CLONE_BLOCKED_DIFFERENT_FILESYSTEM
PATH_ACCEPTED
PATH_REJECTED_ABSOLUTE
PATH_REJECTED_TRAVERSAL
PATH_REJECTED_SYMLINK_ESCAPE
PATH_REJECTED_PROTECTED_VAULT
CACHE_JAIL_SELECTED
```

Descriptor fields must include:

```python
{
    "sprint": "BLK-SYSTEM-012",
    "authority": "PROBE_ONLY",
    "fixture_scope": "INERT_LOCAL_FIXTURES_ONLY",
    "live_mcp_authorized": False,
    "mcp_server_started": False,
    "mcp_client_started": False,
    "fixed_tool_tests_executed": [],
    "primary_repo_mutation_allowed": False,
    "source_staging_allowed": False,
    "source_commit_allowed": False,
    "beo_publication": "DRAFT_ONLY",
    "rtm_status": "NOT_GENERATED",
    "active_vault_read_allowed": False,
    "production_sandbox_claimed": False,
}
```

### RED/GREEN steps

1. Write failing tests proving:
   - the descriptor returns all non-authority fields;
   - same-device source/scratch selects hardlink clone;
   - different-device without fallback fails closed;
   - explicit same-device fallback is selected only when provided;
   - absolute paths reject;
   - `..` traversal rejects;
   - symlink escape rejects;
   - `docs/active`, `docs/requirements`, and `docs/use_cases` reject;
   - cache paths are run-scoped under scratch root and not inside source/workspace roots.
2. Run focused RED:

   ```bash
   python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
   ```

   Expected RED: module/functions missing.

3. Implement the minimal APIs in `python/blk_test_mcp_workspace_process_probes.py`.
4. Rerun focused GREEN:

   ```bash
   python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
   ```

### Shared verification

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
rm -rf python/__pycache__
```

### Commit and push

```bash
git add python/blk_test_mcp_workspace_process_probes.py \
  python/test_blk_test_mcp_workspace_process_probes.py
git diff --cached --check
git commit -m "test: add blk-test workspace policy probes"
git push origin main
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-012_task-002-outcome.md`.

---

## 8. Task 3 — Prove Inert Fixture Clone, Startup Purge, Teardown, and Primary Manifest Guards

### Objective

Prove lifecycle cleanup using only synthetic marker-protected fixture trees under test-owned temporary roots.

### Files

Modify:

- `python/blk_test_mcp_workspace_process_probes.py`
- `python/test_blk_test_mcp_workspace_process_probes.py`

Outcome after implementation commit:

- `docs/outcomes/BLK-SYSTEM-012_task-003-outcome.md`

### Required public APIs

```python
def assert_inert_fixture_source(source_root) -> dict[str, object]:
    """Accept only marker-protected synthetic fixtures; reject real repos and unmarked roots."""


def manifest_source_tree(source_root) -> dict[str, object]:
    """Return deterministic file metadata/hash manifest for primary-corruption checks."""


def create_inert_workspace_fixture(
    source_root,
    scratch_root,
    *,
    run_id: str,
) -> dict[str, object]:
    """Create a temp-root workspace fixture only after inert marker validation."""


def startup_purge_owned_stale_paths(
    scratch_root,
    *,
    pid_alive=None,
) -> dict[str, object]:
    """Remove only marked Sprint 012 stale probe paths/locks under scratch root."""


def teardown_run_paths(
    *,
    workspace_path,
    cache_paths,
    lock_path=None,
    status: str,
) -> dict[str, object]:
    """Root-anchored cleanup for terminal statuses after child death is confirmed."""


def verify_primary_repo_manifest(source_root, manifest) -> dict[str, object]:
    """Verify source fixture manifest remains unchanged after probes."""
```

The inert fixture marker should be a literal file such as:

```text
.blk-system-012-inert-fixture
```

Reject sources that:

- lack the inert marker;
- contain `.git`;
- resolve to `/`, `$HOME`, `/home/dad/BLK-System`, current working directory, or an unowned path;
- are symlink escapes.

### RED/GREEN steps

1. Write failing tests proving:
   - unmarked roots reject;
   - roots containing `.git` reject;
   - the real BLK-System repo path rejects;
   - marker-protected temp fixtures pass;
   - workspace fixture is created only under scratch root;
   - source manifest is unchanged after clone/teardown;
   - startup purge removes only owned stale Sprint 012 prefixes;
   - unrelated temp paths are preserved;
   - live-PID locks are preserved;
   - dead-PID stale locks are removed only when under the owned scratch root;
   - teardown removes workspace/cache/lock for `PASS`, `FAIL`, `BLOCKED`, `FATAL_TIMEOUT`, `FATAL_OUTPUT_FLOOD`, `TRANSPORT_ERROR`, and `OPERATOR_INTERRUPTED`.
2. Run focused RED:

   ```bash
   python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
   ```

3. Implement minimal lifecycle helpers.
4. Rerun focused GREEN:

   ```bash
   python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
   ```

### Shared verification

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
rm -rf python/__pycache__
```

### Commit and push

```bash
git add python/blk_test_mcp_workspace_process_probes.py \
  python/test_blk_test_mcp_workspace_process_probes.py
git diff --cached --check
git commit -m "test: prove inert workspace clone teardown guards"
git push origin main
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-012_task-003-outcome.md`.

---

## 9. Task 4 — Add Atomic Probe Lock and Parallel-Prevention Gates

### Objective

Prove stale/live lock behavior, bounded wait decisions, ownership-aware release, and single-run exclusion under test-owned temporary roots.

### Files

Modify:

- `python/blk_test_mcp_workspace_process_probes.py`
- `python/test_blk_test_mcp_workspace_process_probes.py`

Outcome after implementation commit:

- `docs/outcomes/BLK-SYSTEM-012_task-004-outcome.md`

### Required public APIs

```python
def probe_lock_state(
    lock_path,
    *,
    pid_alive=None,
) -> dict[str, object]:
    """Inspect a probe-owned lock without killing arbitrary host PIDs."""


def acquire_probe_lock(
    lock_path,
    *,
    run_id: str,
    pid=None,
    max_wait_seconds: float = 0.0,
    poll_interval_seconds: float = 0.01,
    pid_alive=None,
) -> dict[str, object]:
    """Acquire a lock with atomic exclusive creation and bounded wait."""


def release_probe_lock(
    lock_path,
    *,
    run_id: str,
) -> dict[str, object]:
    """Release only locks owned by this run_id."""
```

Required status vocabulary:

```text
LOCK_ACQUIRED
LOCK_BLOCKED_LIVE_PID
STALE_LOCK_REMOVED
LOCK_RELEASED
LOCK_RELEASE_SKIPPED_NOT_OWNER
LOCK_BLOCKED_UNOWNED
```

Lock files must record at least:

```json
{
  "sprint": "BLK-SYSTEM-012",
  "authority": "PROBE_ONLY",
  "run_id": "...",
  "pid": 12345
}
```

### RED/GREEN steps

1. Write failing tests proving:
   - atomic exclusive creation is used (`os.O_CREAT | os.O_EXCL` or equivalent);
   - stale dead-PID probe lock is removed and acquired;
   - live PID lock is preserved and returns deterministic locked/BLOCKED evidence;
   - unowned or malformed lock fails closed without deleting arbitrary files;
   - two concurrent attempts produce exactly one `LOCK_ACQUIRED`;
   - non-owner release is skipped;
   - release happens in `finally`-equivalent paths after all terminal statuses from Task 3;
   - a second run can acquire only after cleanup.
2. Run focused RED:

   ```bash
   python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
   ```

3. Implement minimal lock helpers.
4. Rerun focused GREEN:

   ```bash
   python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
   ```

### Shared verification

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
rm -rf python/__pycache__
```

### Commit and push

```bash
git add python/blk_test_mcp_workspace_process_probes.py \
  python/test_blk_test_mcp_workspace_process_probes.py
git diff --cached --check
git commit -m "test: add blk-test process lock probes"
git push origin main
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-012_task-004-outcome.md`.

---

## 10. Task 5 — Prove Fixed Inert Process Timeout, Output Flood, and Process-Tree Kill Path

### Objective

Prove process-control mechanics with hardcoded inert Python child/grandchild probes only, using one shared kill path for timeout and output flood.

### Files

Modify:

- `python/blk_test_mcp_workspace_process_probes.py`
- `python/test_blk_test_mcp_workspace_process_probes.py`

Outcome after implementation commit:

- `docs/outcomes/BLK-SYSTEM-012_task-005-outcome.md`

### Required public API

```python
def run_fixed_inert_process_probe(
    probe_name: str,
    *,
    cwd,
    timeout_seconds: float,
    max_output_bytes: int,
    env=None,
) -> dict[str, object]:
    """Run only fixed inert local probes and return bounded process-control evidence."""
```

Allowed `probe_name` values only:

```text
exit_zero
exit_nonzero
timeout
output_flood
descendant_timeout
```

Unknown probe names must reject with `PROBE_BLOCKED_UNKNOWN_NAME`.

Allowed implementation mechanics:

- `subprocess.Popen(...)` is allowed only for fixed inert child snippets in this module.
- Use `sys.executable` for child snippets.
- Use `start_new_session=True` or equivalent process-group isolation.
- Use a single helper for timeout and output-flood process-tree termination.
- Never use `shell=True`.
- Never call `pytest`, `go test`, `npm`, `node`, browsers, MCP clients/servers, Git write commands, package managers, network clients, or Sprint 011 fixed-tool descriptors.

Required process-result fields:

```python
{
    "authority": "PROBE_ONLY",
    "probe_status": "PASS|FAIL|FATAL_TIMEOUT|FATAL_OUTPUT_FLOOD|PROBE_BLOCKED_UNKNOWN_NAME",
    "inert_subprocess_called": True,
    "live_mcp_subprocess_called": False,
    "fixed_tool_tests_executed": [],
    "network_called": False,
    "process_tree_dead": True,
    "kill_path": "SHARED_TIMEOUT_FLOOD_KILL" | None,
    "stdout_bytes_captured": 0,
    "stderr_bytes_captured": 0,
    "output_truncated": False,
}
```

### RED/GREEN steps

1. Write failing tests proving:
   - `exit_zero` returns `PASS`;
   - `exit_nonzero` returns `FAIL` and preserves exit code;
   - `timeout` returns `FATAL_TIMEOUT`, kills the process group, and reports `process_tree_dead`;
   - `output_flood` returns `FATAL_OUTPUT_FLOOD`, uses the same kill helper as timeout, and caps output while reading;
   - `descendant_timeout` kills descendants before lock/cleanup release;
   - unknown probe names reject and do not spawn;
   - no `shell=True` or dynamic command dispatch exists in module source;
   - process results do not contain BEO publication or RTM authority fields.
2. Run focused RED:

   ```bash
   python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
   ```

3. Implement minimal fixed inert process runner.
4. Rerun focused GREEN:

   ```bash
   python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
   ```

### Shared verification

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
rm -rf python/__pycache__
```

### Commit and push

```bash
git add python/blk_test_mcp_workspace_process_probes.py \
  python/test_blk_test_mcp_workspace_process_probes.py
git diff --cached --check
git commit -m "test: prove inert process timeout flood kill probes"
git push origin main
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-012_task-005-outcome.md`.

---

## 11. Task 6 — Add Cache Jail, Synthetic Environment Scrub, Output Compression, Replay Bundle, and Source-Scan Gates

### Objective

Prove bounded replay evidence and host-secret/protected-body exclusion using synthetic env/log fixtures and deterministic source-scan gates.

### Files

Modify:

- `python/blk_test_mcp_workspace_process_probes.py`
- `python/test_blk_test_mcp_workspace_process_probes.py`

Outcome after implementation commit:

- `docs/outcomes/BLK-SYSTEM-012_task-006-outcome.md`

### Required public APIs

```python
def build_scrubbed_probe_environment(
    *,
    run_id: str,
    cache_root,
    inherited_env=None,
) -> dict[str, object]:
    """Return an approved child environment from a synthetic input map."""


def inspect_environment_policy(env) -> dict[str, object]:
    """Return deterministic policy evidence for allowed/disallowed environment fields."""


def compress_bounded_output(
    stdout: bytes,
    stderr: bytes,
    *,
    max_bytes: int,
    max_error_entries: int = 7,
) -> dict[str, object]:
    """Return bounded, deduplicated first/last output evidence."""


def build_workspace_process_replay_bundle(run_record: dict[str, object]) -> dict[str, object]:
    """Return bounded replay metadata without secrets, protected bodies, BEO authority, or RTM authority."""
```

### Required gates

Tests must prove:

- cache paths are run-scoped and outside source/workspace roots;
- synthetic inherited env strips/disallows keys containing or matching:
  - `TOKEN`;
  - `SECRET`;
  - `KEY` when credential-like;
  - `AWS_*`;
  - `GITHUB_TOKEN`;
  - `SSH_AUTH_SOCK`;
  - package-manager auth variables;
  - unrelated host paths;
- no real `os.environ` dump is stored in replay output;
- output compression strips ANSI codes, caps bytes, preserves first/last relevant context, deduplicates repeated errors, and records truncation metadata;
- replay bundle includes workspace, lock, process, cache, output, and non-authority summaries;
- replay bundle excludes host secrets, protected BLK-req body text, raw unbounded logs, `published_at`, `approved_by`, `rtm`, `rtm_id`, `requirements`, `coverage_matrix`, or drift-decision fields;
- source scan rejects forbidden live surfaces.

Source scan should reject these markers in `python/blk_test_mcp_workspace_process_probes.py`:

```text
import socket
from socket
requests
http.server
urllib
@modelcontextprotocol
StdioServerTransport
shell=True
os.system
eval(
exec(
npm install
git add
git commit
publish_beo
generate_rtm
read_active_vault
```

Do **not** reject the literal string `subprocess` globally in this module; Task 5 requires fixed inert child-process probes. Instead assert subprocess use is routed through `run_fixed_inert_process_probe(...)` and fixed probe names.

### RED/GREEN steps

1. Write failing tests for env scrub, compression, replay exclusion, and source-scan gates.
2. Run focused RED:

   ```bash
   python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
   ```

3. Implement minimal helpers.
4. Rerun focused GREEN:

   ```bash
   python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
   ```

### Shared verification

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
rm -rf python/__pycache__
```

### Commit and push

```bash
git add python/blk_test_mcp_workspace_process_probes.py \
  python/test_blk_test_mcp_workspace_process_probes.py
git diff --cached --check
git commit -m "test: add blk-test cache env replay probes"
git push origin main
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-012_task-006-outcome.md`.

---

## 12. Task 7 — Define Active BLK-018 Probe Contract and Cross-Reference Gates

### Objective

Make Sprint 012's accepted current contract discoverable as active doctrine without enabling live BLK-test MCP or superseding BLK-017 disabled transport authority.

### Files

Create:

- `docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md`

Modify:

- `docs/BLK-008_blk-test-mcp-execution-server.md`
- `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md`
- `python/test_active_doctrine_review_gates.py`

Outcome after implementation commit:

- `docs/outcomes/BLK-SYSTEM-012_task-007-outcome.md`

### Required behavior

`docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md` must include:

- `**Status:** Active workspace/process-control probe contract`;
- `BLK-SYSTEM-012`;
- `inert local fixtures only`;
- `does not authorize live BLK-test MCP`;
- `does not authorize live MCP client/server startup`;
- `does not execute fixed-tool tests`;
- `does not mutate primary repo`;
- `does not stage files`;
- `does not commit`;
- `does not authorize authoritative BEO publication`;
- `does not authorize RTM generation`;
- `does not authorize RTM drift rejection authority`;
- `does not read protected BLK-req vault bodies`;
- `does not claim production sandbox/cgroup/VM enforcement`;
- `does not claim production host-secret isolation`;
- `Sprint 013 owns approval/source-evidence authorization mechanics`;
- `Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke`;
- a section naming implementation/test files:
  - `python/blk_test_mcp_workspace_process_probes.py`;
  - `python/test_blk_test_mcp_workspace_process_probes.py`;
  - `python/test_active_doctrine_review_gates.py`.

Cross-reference gates should require:

- BLK-008 mentions BLK-018 as an inert workspace/process-control probe contract and keeps target-state/live-authority warnings.
- BLK-017 mentions BLK-018 as a successor readiness probe while preserving that BLK-017 remains the disabled transport contract until live authority is separately approved.
- BLK-008, BLK-017, and BLK-018 all retain non-authority markers for live BLK-test MCP, BEO publication, and RTM generation.

### RED/GREEN steps

1. Add failing active-doctrine tests for BLK-018 and BLK-008/017 cross-references.
2. Run focused RED:

   ```bash
   python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v
   ```

   Expected RED: BLK-018/cross-reference markers missing.

3. Create BLK-018 and patch BLK-008/BLK-017 narrowly.
4. Rerun focused GREEN:

   ```bash
   python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v
   ```

5. Also rerun the workspace/process probe tests:

   ```bash
   python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
   ```

### Shared verification

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
rm -rf python/__pycache__
```

### Commit and push

```bash
git add python/test_active_doctrine_review_gates.py \
  docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md \
  docs/BLK-008_blk-test-mcp-execution-server.md \
  docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md
git diff --cached --check
git commit -m "docs: define blk-test workspace process probe contract"
git push origin main
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-012_task-007-outcome.md`.

---

## 13. Task 8 — Sprint Closeout and BLK-SYSTEM-013 Handoff Seed

### Objective

Close Sprint 012 with explicit BLK-001 alignment verdict, task commit table, RED/GREEN evidence summary, non-authority statement, and narrow handoff to Sprint 013.

### Files

Create:

- `docs/outcomes/BLK-SYSTEM-012_sprint-closeout.md`

### Required closeout content

The closeout document must include:

- `BLK-SYSTEM-012` / `blk-system-012`;
- `BLK-001 alignment verdict`;
- task commit table for Tasks 1-7 plus closeout;
- created/modified file list;
- RED/GREEN evidence summary for Tasks 1-7;
- final verification evidence;
- explicit non-authority statement;
- `does not authorize live BLK-test MCP`;
- `does not authorize live MCP client/server startup`;
- `does not execute fixed-tool tests`;
- `does not mutate primary repo`;
- `does not stage files`;
- `does not commit` as BLK-test behavior;
- `does not authorize authoritative BEO publication`;
- `does not authorize RTM generation`;
- `does not authorize RTM drift rejection authority`;
- `does not read protected BLK-req vault bodies`;
- `does not claim production sandbox/cgroup/VM enforcement`;
- `does not claim production host-secret isolation`;
- statement that human sprint-executor Git commits/pushes are distinct from BLK-test/source-mutation authority;
- recommended next sprint seed:

  ```text
  BLK-SYSTEM-013 — Approval-channel and Source-Evidence Authorization Mechanics
  ```

### RED/GREEN steps

1. Run RED closeout gate before creating the file:

   ```bash
   python3 - <<'PY'
   from pathlib import Path
   path = Path('docs/outcomes/BLK-SYSTEM-012_sprint-closeout.md')
   assert path.exists(), 'RED: Sprint 012 closeout doc missing'
   PY
   ```

2. Create the closeout doc.
3. Run GREEN content gate:

   ```bash
   python3 - <<'PY'
   from pathlib import Path
   path = Path('docs/outcomes/BLK-SYSTEM-012_sprint-closeout.md')
   text = path.read_text()
   required = [
       'BLK-SYSTEM-012',
       'BLK-001 alignment verdict',
       'does not authorize live BLK-test MCP',
       'does not authorize live MCP client/server startup',
       'does not execute fixed-tool tests',
       'does not mutate primary repo',
       'does not stage files',
       'does not authorize authoritative BEO publication',
       'does not authorize RTM generation',
       'does not authorize RTM drift rejection authority',
       'does not read protected BLK-req vault bodies',
       'does not claim production sandbox/cgroup/VM enforcement',
       'BLK-SYSTEM-013',
   ]
   missing = [marker for marker in required if marker not in text]
   assert not missing, missing
   assert text.count('```') % 2 == 0
   for i, line in enumerate(text.splitlines(), 1):
       assert line.rstrip() == line, f'trailing whitespace line {i}'
   print('SPRINT012_CLOSEOUT_CONTENT_PASS')
   PY
   ```

### Final verification

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
rm -rf python/__pycache__
git status --short --branch
git log --oneline --decorate -10
```

### Commit and push

```bash
git add docs/outcomes/BLK-SYSTEM-012_sprint-closeout.md
git diff --cached --check
git commit -m "docs: close out blk-system sprint 012"
git push origin main
git status --short --branch
```

The sprint closeout doc is the closeout task outcome artifact and must be pushed immediately after the closeout task.

---

## 14. Final Acceptance Criteria

BLK-SYSTEM-012 is complete only when:

- `docs/reviews/BLK-SYSTEM-012_workspace-process-control-review.md` exists and passes doctrine gates;
- `python/blk_test_mcp_workspace_process_probes.py` exists with dependency-free inert probe helpers;
- `python/test_blk_test_mcp_workspace_process_probes.py` proves workspace policy, path guards, teardown, locks, process-tree kill, timeout, output flood, cache/env scrub, output compression, replay evidence, and source-scan gates;
- `docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md` exists and active doctrine cross-references pass;
- BLK-008 and BLK-017 cross-reference BLK-018 without implying live authority;
- all task outcome docs for Tasks 1-7 are committed and pushed after their corresponding tasks;
- `docs/outcomes/BLK-SYSTEM-012_sprint-closeout.md` is committed and pushed;
- full Python unittest, Go test, Go vet, and `git diff --check` pass;
- no generated `python/__pycache__` files are staged;
- `git status --short --branch` ends clean and aligned with `origin/main`;
- every artifact repeats that Sprint 012 does not authorize live BLK-test MCP, fixed-tool execution, source mutation, authoritative BEO publication, RTM generation, active-vault reads, approval mechanics, or production sandbox/host-secret isolation.

---

## 15. Risks, Landmines, and Stop Conditions

### Risks / landmines

- **Hardlink false isolation:** hardlinks share inodes. Treat hardlink clone behavior as a decision/fixture probe only; do not write through hardlinked fixture files.
- **Global cleanup danger:** never purge broad `/var/tmp`, `/tmp`, `$HOME`, repo root, or globbed paths. Use marker-protected test-owned roots only.
- **Process-control scope creep:** process probes may spawn inert Python children only. Any generic command runner becomes an arbitrary shell gateway.
- **Output flood danger:** use small deterministic byte caps in tests; do not generate 50 MiB logs just because BLK-008 target-state mentions 50 MiB.
- **Secret leakage:** use synthetic env maps. Never dump real host environment into output or replay bundles.
- **Approval drift:** approval-looking records remain non-authorizing; Sprint 013 owns approval/source-evidence mechanics.
- **Live smoke drift:** Sprint 014 owns any first live fixed-tool BLK-test MCP smoke under explicit human approval.
- **Namespace drift:** do not confuse `BLK-SYSTEM-012` with active `docs/BLK-012_*` BLK-pipe doctrine.
- **Push cadence drift:** do not copy Sprint 011's old "do not push until closeout" rule. Outcome docs are pushed after each task.

### Stop conditions

Stop and ask the human before proceeding if any task would require:

- running probes against `/home/dad/BLK-System` as a target workspace;
- starting an MCP server/client or JSON-RPC handshake;
- executing Sprint 011 fixed-tool descriptors;
- using package manager installs or new external dependencies;
- exposing arbitrary command execution;
- touching protected BLK-req body paths;
- claiming container/cgroup/VM/production host-secret isolation;
- publishing authoritative BEOs or generating RTM;
- implementing approval mechanics earlier than Sprint 013;
- using broad Git staging/revert/stash operations;
- deferring task outcome docs until sprint closeout.

---

## 16. Quick Resume Prompt

```text
Resume BLK-SYSTEM-012 from docs/plans/blk-system-012_workspace-isolation-process-control-implementation-probes.md in /home/dad/BLK-System. Use blk-system-sprint-execution. Preflight git status/fetch first. Execute the next incomplete task only. Use RED/GREEN TDD, exact-path staging, full Python + Go verification, implementation commit push, then create/validate/commit/push the matching docs/outcomes/BLK-SYSTEM-012_task-00N-outcome.md after the task. Do not defer outcome docs until sprint closeout. Preserve all non-authority boundaries: no live BLK-test MCP, no fixed-tool execution, no primary repo mutation as probe behavior, no BEO publication, no RTM generation, no approval mechanics, no protected active-vault reads, and no production sandbox/host-secret isolation claims.
```
