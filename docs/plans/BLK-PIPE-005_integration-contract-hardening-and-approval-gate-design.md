# BLK-pipe Sprint 005 — Integration Contract Hardening and Approval Gate Design

> **For Hermes:** Use `blk-system-sprint-execution` to implement this plan task-by-task. This sprint is deterministic local hardening and design work only. Do not run live Codex, live tactical LLMs, network model services, cyber tooling, or live BLK-test MCP.

**Goal:** Close the BLK-PIPE-004 review gaps before any real `codex-live` or live BLK-test integration is considered.

**Architecture:** Sprint 004 correctly proved a dry-run handoff shape, but the review found that some proof paths were fixture-surrogates rather than production-equivalent paths. Sprint 005 tightens the contracts at the integration seams: true `allowed_new_files`, BLK-pipe status taxonomy, Python evidence preservation, canonical trace metadata, BLK-native doctrine vocabulary, and fail-closed approval/MCP design stubs.

**Tech Stack:** Go 1.26.x, POSIX-only BLK-pipe CLI, dependency-free Python fixture/adapter modules, deterministic Go/Python tests, Markdown doctrine/outcome documents.

---

## 0. Review Verdict on BLK-PIPE-004

BLK-PIPE-004 is directionally correct and useful: it kept live autonomy blocked while proving BEB/L2 dry-run payload construction, fake tactical-engine execution through BLK-pipe, BLK-test fixture handoff shapes, and draft BEO projection.

However, the review found several issues that should be addressed before moving toward orchestrator or live BLK-test integration:

1. **true `allowed_new_files` is not proven.** The dry-run execution helper pre-seeds `dry_run_output.txt` as a tracked file and rewrites the payload from `allowed_new_files` into `allowed_modified_files`. A direct true-new-file payload currently returns `UNAUTHORIZED_FILE_MUTATION` on this machine because the shell-created file inherits group-writable mode (`0664` under umask `0002`) and is treated as unauthorized physical residue.
2. **BLK-test handoff status taxonomy has a real typo/drift.** Go and the Python adapter emit/preserve `FATAL_OUTPUT_FLOOD`, but `python/blk_test_handoff_fixtures.py` accepts `OUTPUT_FLOOD`. A real BLK-pipe output-flood report cannot currently become a deterministic `BLOCKED` handoff.
3. **The Python adapter hides evidence needed by future integration.** `ExecutionResult` exposes status/log fields but not `commit_hash`, `staged_files`, `destroyed_files`, or the raw parsed report. Sprint 004 avoided this by asserting raw JSON in the dry-run helper, but a real orchestrator/BLK-test bridge will need those fields without bypassing the adapter.
4. **The dry-run execution helper raises on nonzero BLK-pipe results.** That makes it hard to deterministically route non-success BLK-pipe reports into `BLOCKED` fixture handoffs during integration tests.
5. **Trace metadata naming is split.** Active BLK-003 examples use `traced_artifacts` string entries, while BLK-pipe payloads/reports and Sprint 004 fixtures use structured `trace_artifacts` objects.
6. **Some active doctrine still uses stale AAA_001 / CEB / CEO terms.** Sprint 004 Task 1 fixed the BLK-pipe transport path, but active docs outside that task still contain stale terms.
7. **Sprint 004 closeout metadata is stale.** `docs/outcomes/BLK-PIPE-004_sprint-closeout.md` still says the closeout commit and remote push are pending even though `31c9126` is pushed at `origin/main`.
8. **The Sprint 005 seed is too broad if interpreted as live integration.** Approval gate, BLK-test MCP, BEO publication, RTM, sandbox/capability, and credential/network policy should not all become live runtime implementation in one sprint. Sprint 005 should implement fail-closed contracts and disabled-by-default design stubs only.

---

## 1. Current Known State

Repository:

```text
/home/dad/BLK-System
```

Review preflight:

```text
git status --short --branch -> ## main...origin/main
git fetch origin main       -> PASS
go version                  -> go version go1.26.2 linux/amd64
python3 --version           -> Python 3.11.15
HEAD                        -> 31c9126 docs: close out blk-pipe sprint 004
```

Non-destructive verification run during the review:

```text
python3 -m unittest discover -s python -p 'test_*.py' -> Ran 48 tests, OK
go test ./...                                         -> PASS
go vet ./...                                         -> PASS
go run ./cmd/blk-pipe --health                       -> {"status":"OK","component":"blk-pipe"}
production broad-staging grep                         -> PASS
production direct-Git grep                            -> PASS
triple-dot diff grep over active Sprint 004 docs       -> PASS
git diff --check                                      -> PASS
git status --short --branch                           -> ## main...origin/main
```

Targeted review probes:

```text
FATAL_OUTPUT_FLOOD handoff probe -> ValueError: unknown BLK-pipe status: FATAL_OUTPUT_FLOOD
true allowed_new dry-run probe   -> rc=3, status=UNAUTHORIZED_FILE_MUTATION, destroyed_files=["dry_run_output.txt"]
```

---

## 2. Non-Goals and Hard Blocks

Sprint 005 must not implement or run:

- live Codex invocation,
- live tactical LLM API calls,
- network model services,
- `codex-live` runtime execution,
- cyber tooling or cyber execution,
- execution against real cyber-program repositories or live targets,
- live BLK-test MCP calls,
- RTM generation as a complete traceability ledger,
- BEO publication as an authoritative HITL-approved outcome,
- full sandbox/container/cgroup/VM enforcement,
- production host-secret isolation claims.

Allowed work:

```text
deterministic local tests
fixture-only execution
fail-closed approval-gate contract code
disabled-by-default MCP request shape/stub design
documentation cleanup and doctrine alignment
```

Blocked after this sprint unless separately approved:

```text
codex-live
live BLK-test MCP
live BEO publication
RTM generation
cyber-execution
```

---

## 3. Invariants to Preserve

1. BLK-pipe remains a deterministic transport/mutation gate, not an architect, requirement parser, live LLM caller, or sandbox.
2. Hermes/BLK-pipe/BLK-test/BEO boundaries must preserve opaque trace metadata without parsing active requirement bodies.
3. Protected BLK-req vault paths remain denied to engine allowlists: `docs/active/`, `docs/requirements/`, and `docs/use_cases/`.
4. No production `git add .`, `git add -u`, `git stash`, relative revert anchors, or triple-dot report diffs.
5. Python subprocess calls remain shell-free except existing BLK-pipe validation-command strings, which are payload-controlled validation gate inputs.
6. `codex-live` remains fail-closed. Any future live path must require a hard user approval token/phrase and separate sandbox/capability decisions.
7. BLK-test and BEO outputs in Sprint 005 remain fixture/design-only unless a future approved sprint wires live services.
8. New BLK-System plans and active docs use BLK-native BEB/BEO terminology and `beb_id`, not AAA_001 / CEB / CEO / `ceb_id`.

---

## 4. Controller Workflow for Each Task

For each task:

1. Preflight:

   ```bash
   cd /home/dad/BLK-System
   export PATH="$HOME/.local/bin:$PATH"
   git status --short --branch
   ```

2. Use TDD for code changes: add a failing test/probe first, capture RED, implement minimal code, capture GREEN.
3. Use deterministic local review gates only for this sprint. Do not dispatch live Codex, live tactical LLM, network model, cyber, or live BLK-test MCP reviewers.
4. Run focused tests listed in the task.
5. Run shared verification before each implementation commit:

   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   python3 -m unittest discover -s python -p 'test_*.py'
   go test ./...
   go vet ./...
   git diff --check
   ```

6. Create a matching outcome document for every task:

   ```text
   docs/outcomes/BLK-PIPE-005_task-00N-outcome.md
   ```

7. Commit each implementation/docs task with the listed commit message.
8. Push only after verification passes and `git status --short --branch` is clean/aligned.

---

## 5. Task 1 — Finalize Sprint 004 Closeout Metadata and Add Metadata Gate

### Objective

Fix the stale Sprint 004 closeout metadata and add a deterministic closeout metadata gate so future closeouts do not remain self-referentially pending after they are pushed.

### Files

Modify:

- `docs/outcomes/BLK-PIPE-004_sprint-closeout.md`
- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md` if a closeout convention note belongs there

Create outcome:

- `docs/outcomes/BLK-PIPE-005_task-001-outcome.md`

### Required behavior

- Replace the pending closeout commit line with:

  ```text
  **Closeout commit:** `31c9126 docs: close out blk-pipe sprint 004`
  ```

- Replace the pending remote line with a pushed/aligned statement:

  ```text
  **Remote:** pushed to `origin/main`
  ```

- Add a closeout metadata gate that checks current sprint closeouts do not contain `pending until this document is committed` or `pending push` after the relevant sprint closeout has landed.
- Do not rewrite historical Sprint 001/002/003 closeouts unless a gate proves they contain the same active metadata defect and the task explicitly scopes the update.

### TDD / docs RED gate

Before editing, run a deterministic check that fails on the current Sprint 004 closeout:

```bash
python3 - <<'PY'
from pathlib import Path
p = Path('docs/outcomes/BLK-PIPE-004_sprint-closeout.md')
text = p.read_text()
assert 'pending until this document is committed' not in text
assert 'pending push' not in text
assert '31c9126 docs: close out blk-pipe sprint 004' in text
PY
```

Expected RED:

```text
AssertionError
```

### Focused verification

```bash
python3 - <<'PY'
from pathlib import Path
p = Path('docs/outcomes/BLK-PIPE-004_sprint-closeout.md')
text = p.read_text()
assert 'pending until this document is committed' not in text
assert 'pending push' not in text
assert '31c9126 docs: close out blk-pipe sprint 004' in text
assert 'pushed to `origin/main`' in text
assert text.endswith('\n')
fence = chr(96) * 3
assert text.count(fence) % 2 == 0
for i, line in enumerate(text.splitlines(), 1):
    assert line.rstrip() == line, f'trailing whitespace line {i}'
PY
git diff --check
```

### Commit message

```text
docs: finalize blk-pipe sprint 004 metadata
```

---

## 6. Task 2 — Repair True `allowed_new_files` Dry-Run Execution

### Objective

Make a true new file listed only in `allowed_new_files` succeed through BLK-pipe without pre-seeding a tracked placeholder or rewriting the payload into `allowed_modified_files`.

### Files

Modify:

- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- `python/blk_pipe_dry_run_orchestrator.py`
- `python/test_blk_pipe_dry_run_orchestrator.py`
- `python/test_beo_fixture_projection.py`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/outcomes/BLK-PIPE-004_sprint-closeout.md` only to mark the Task 5 caveat as resolved by Sprint 005, not to rewrite its historical evidence

Create outcome:

- `docs/outcomes/BLK-PIPE-005_task-002-outcome.md`

### Required behavior

- A payload with:

  ```json
  {
    "allowed_modified_files": [],
    "allowed_new_files": ["dry_run_output.txt"]
  }
  ```

  must succeed when the engine creates `dry_run_output.txt` as a previously untracked file.

- The dry-run Python tests must initialize the hermetic repo without a pre-existing `dry_run_output.txt`.
- `run_blk_pipe_dry_run_fixture(...)` must not mirror `allowed_new_files` into `allowed_modified_files`.
- The successful BLK-pipe report must include:
  - `status: SUCCESS`,
  - non-empty `pre_engine_hash`,
  - non-empty `commit_hash`,
  - `staged_files == ["dry_run_output.txt"]`,
  - preserved `trace_artifacts`,
  - clean final Git status.
- The fix must preserve mode safety. Do not silently allow setuid/setgid/sticky, device nodes, FIFOs, directories, symlink surprises, or path traversal.
- If the root cause is group-writable file mode from umask `0002`, normalize or explicitly accept safe non-executable group-writable regular files before staging. Record the chosen safety rule in docs/tests.

### TDD RED tests

Add a Go regression in `internal/pipe/run_test.go`, for example:

```go
func TestRunAllowedNewFileWithGroupWritableUmaskSucceeds(t *testing.T) { ... }
```

Test shape:

- hermetic temp Git repo with only `README.md` committed,
- fake engine command creates `dry_run_output.txt` with `umask 0002`,
- payload uses only `allowed_new_files: ["dry_run_output.txt"]`,
- expected pre-fix RED: `ExitUnauthorizedMutation`, report `destroyed_files` contains `dry_run_output.txt`,
- expected GREEN: exit `0`, `SUCCESS`, `staged_files == ["dry_run_output.txt"]`, `git show --name-only HEAD` contains `dry_run_output.txt`, final repo clean.

Update Python fixture tests:

- remove `(repo / "dry_run_output.txt").write_text("placeholder\n")`,
- remove `git add dry_run_output.txt` from fixture repo setup,
- assert the payload still uses `allowed_new_files` and does not rewrite it before invocation.

### Implementation guidance

Inspect this path first:

```text
internal/pipe/run.go
failUnauthorizedAllowedNewPhysicalModes(...)
allowedNewPhysicalModeResidue(...)
```

The current review probe indicates that a shell-created new file can be reported as unauthorized physical residue before staging. On this machine `umask` is `0002`, so a shell redirection commonly creates `0664` files. Git commits that as a normal `100644` file, but BLK-pipe currently treats the physical mode as suspicious for new files.

Acceptable implementation approaches:

1. Normalize safe allowed-new regular files to deterministic worktree modes (`0644` for non-executable, `0755` for executable) before staging; or
2. Permit safe group-writable regular files while still rejecting setuid/setgid/sticky/world-writable/exotic modes.

Do not weaken path validation or allow directories as allowlist entries.

### Focused verification

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestRunAllowedNew|TestRun.*DryRun|TestRun.*Unauthorized' -v
python3 -m unittest discover -s python -p 'test_blk_pipe_dry_run_orchestrator.py' -v
python3 -m unittest discover -s python -p 'test_beo_fixture_projection.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

### Commit message

```text
fix: support true blk-pipe allowed_new files
```

---

## 7. Task 3 — Align BLK-pipe Status Taxonomy Through BLK-test Handoff

### Objective

Fix status vocabulary drift so every BLK-pipe/adapter non-success status routes deterministically to `BLOCKED` instead of being rejected as unknown.

### Files

Modify:

- `python/blk_test_handoff_fixtures.py`
- `python/test_blk_test_handoff_fixtures.py`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md` only if the status table needs a cross-reference

Create outcome:

- `docs/outcomes/BLK-PIPE-005_task-003-outcome.md`

### Required behavior

- Replace stale `OUTPUT_FLOOD` with canonical `FATAL_OUTPUT_FLOOD`.
- Keep `SUCCESS` as the only source status allowed for BLK-test `PASS` and `FAIL` handoffs.
- Non-success BLK-pipe statuses must become `BLOCKED` handoffs when passed to `build_blk_test_blocked_handoff(...)`.
- Unknown statuses must still reject.
- Preserve safe trace artifacts in `BLOCKED` when present.
- Do not call live BLK-test MCP.

Canonical source statuses for this fixture layer should include at least:

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

`FATAL_CRASH` and `FATAL_PYTHON_TIMEOUT` are adapter-level statuses; include them only if the integration path may feed adapter result dictionaries into handoff code. If they are not included, document why the handoff fixture consumes raw BLK-pipe reports only.

### TDD RED tests

Add tests:

```python
def test_blk_test_blocked_payload_handles_fatal_output_flood_report(self): ...
def test_blk_test_blocked_payload_handles_all_known_non_success_statuses(self): ...
def test_blk_test_fixture_rejects_legacy_output_flood_status(self): ...
```

Expected RED before implementation:

```text
ValueError: unknown BLK-pipe status: FATAL_OUTPUT_FLOOD
```

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_blk_test_handoff_fixtures.py' -v
python3 - <<'PY'
from pathlib import Path
text = Path('python/blk_test_handoff_fixtures.py').read_text()
assert 'FATAL_OUTPUT_FLOOD' in text
assert '"OUTPUT_FLOOD"' not in text
PY
python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
```

### Commit message

```text
fix: align blk-test handoff status taxonomy
```

---

## 8. Task 4 — Preserve BLK-pipe Execution Evidence in Python Adapters

### Objective

Make the Python adapter and dry-run invocation path preserve the evidence that future orchestration and BLK-test handoff code must inspect: commit hash, staged files, destroyed files, raw report, stderr, and nonzero return-code family.

### Files

Modify:

- `python/blk_pipe_adapter.py`
- `python/test_blk_pipe_adapter.py`
- `python/blk_pipe_dry_run_orchestrator.py`
- `python/test_blk_pipe_dry_run_orchestrator.py`
- `python/test_beo_fixture_projection.py`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-005_task-004-outcome.md`

### Required behavior

- Extend `ExecutionResult` with:
  - `commit_hash: str = ""`,
  - `staged_files: list[str] | None = None`,
  - `destroyed_files: list[str] | None = None`,
  - `raw_report: dict | None = None`,
  - `stderr: str = ""`.
- Preserve these fields on success and non-success parsed JSON reports.
- Unknown nonzero exits must still force `INTERNAL_ERROR` even if stdout claims `SUCCESS`.
- Non-JSON stdout must still map to `FATAL_CRASH` and must not claim success.
- Temp payload cleanup must remain in `finally`.
- Subprocess invocation must remain shell-free.
- Add a dry-run invocation helper that can return non-success report evidence without raising, for example:

  ```python
  @dataclass(frozen=True)
  class DryRunExecutionResult:
      returncode: int
      status: str
      report: dict
      stderr: str

  def invoke_blk_pipe_dry_run_fixture(...) -> DryRunExecutionResult: ...
  ```

- Preserve the existing success-focused `run_blk_pipe_dry_run_fixture(...)` wrapper if useful, but implement it on top of the no-throw helper.

### TDD RED tests

Add/update tests:

```python
def test_execution_result_preserves_commit_and_staging_evidence(self): ...
def test_execution_result_preserves_destroyed_files_on_non_success(self): ...
def test_execution_result_preserves_raw_report_and_stderr(self): ...
def test_dry_run_fixture_invocation_returns_non_success_report_without_raising(self): ...
def test_dry_run_non_success_can_build_blocked_handoff(self): ...
```

Expected RED before implementation:

```text
AttributeError: 'ExecutionResult' object has no attribute 'commit_hash'
RuntimeError raised before BLOCKED handoff can inspect report
```

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_blk_pipe_adapter.py' -v
python3 -m unittest discover -s python -p 'test_blk_pipe_dry_run_orchestrator.py' -v
python3 -m unittest discover -s python -p 'test_blk_test_handoff_fixtures.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
```

### Commit message

```text
feat: preserve blk-pipe execution evidence in python adapters
```

---

## 9. Task 5 — Canonicalize Trace Metadata and BLK-Native Vocabulary in Active Doctrine

### Objective

Resolve split trace terminology and remove stale AAA_001 / CEB / CEO language from active BLK-System doctrine that affects new planning and integration work.

### Files

Modify active/current docs only:

- `docs/BLK-002_blk-req-artifact-lifecycle.md`
- `docs/BLK-003_blk-pipe-blk-test-orchestration.md`
- `docs/BLK-004_blk-pipe-v47-architecture-suite.md`
- `docs/BLK-007_dependency-graph-recon-tool.md`
- `docs/BLK-008_blk-test-mcp-execution-server.md`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
- `README.md`
- `testdata/orchestrator/BEB_004_dry_run.md`
- `python/blk_pipe_dry_run_orchestrator.py`
- `python/test_blk_pipe_dry_run_orchestrator.py`
- `python/test_beo_fixture_projection.py`

Create outcome:

- `docs/outcomes/BLK-PIPE-005_task-005-outcome.md`

### Required behavior

- Use `trace_artifacts` as the canonical field name across:
  - BEB frontmatter examples,
  - BLK-pipe payload JSON,
  - BLK-pipe report JSON,
  - BLK-test PASS/FAIL/BLOCKED handoff fixtures,
  - BEO fixture projection,
  - future RTM interface notes.
- Use structured trace artifact objects consistently:

  ```yaml
  trace_artifacts:
    - kind: "REQ"
      id: "REQ-042"
      version_hash: "sha256:<64-hex>"
  ```

- Update the Sprint 004 BEB fixture frontmatter from `traced_artifacts` to `trace_artifacts`.
- Update the narrow BEB fixture parser to require the canonical parent key rather than accepting any `- kind:` list accidentally.
- Remove stale governing references to `AAA_001`, `CEB`, `CEO`, `ceb_id`, and `Codex Execution Brief` from active/current docs. Replace with BLK-native `BEB`, `BEO`, `beb_id`, and BLK-System orchestration wording.
- Do not rewrite clearly historical plans/outcomes/reviews unless they are in the current active docs set above.
- Preserve the fact that `REQ-DRY-001` is a synthetic fixture identifier only.

### TDD / docs RED gates

Run before edits and expect failure:

```bash
python3 - <<'PY'
from pathlib import Path
active = [
    Path('docs/BLK-002_blk-req-artifact-lifecycle.md'),
    Path('docs/BLK-003_blk-pipe-blk-test-orchestration.md'),
    Path('docs/BLK-004_blk-pipe-v47-architecture-suite.md'),
    Path('docs/BLK-007_dependency-graph-recon-tool.md'),
    Path('docs/BLK-008_blk-test-mcp-execution-server.md'),
    Path('docs/BLK-010_blk-pipe-v47-hardening-cli.md'),
    Path('docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md'),
    Path('docs/BLK-013_blk-test-handoff-fixture-contract.md'),
    Path('docs/BLK-014_blk-execution-outcome-fixture-shape.md'),
    Path('README.md'),
]
for p in active:
    text = p.read_text()
    for token in ['AAA_001', 'ceb_id', 'Codex Execution Brief']:
        assert token not in text, f'{p}: stale token {token}'
    assert 'trace_artifacts' in text or p.name in {'BLK-002_blk-req-artifact-lifecycle.md', 'BLK-007_dependency-graph-recon-tool.md', 'BLK-008_blk-test-mcp-execution-server.md'}
fixture = Path('testdata/orchestrator/BEB_004_dry_run.md').read_text()
assert 'trace_artifacts:' in fixture
assert 'traced_artifacts:' not in fixture
PY
```

Add parser tests:

```python
def test_load_dry_run_fixture_requires_trace_artifacts_key(self): ...
def test_load_dry_run_fixture_rejects_legacy_traced_artifacts_key(self): ...
```

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_blk_pipe_dry_run_orchestrator.py' -v
python3 -m unittest discover -s python -p 'test_beo_fixture_projection.py' -v
python3 - <<'PY'
from pathlib import Path
active = [
    Path('docs/BLK-002_blk-req-artifact-lifecycle.md'),
    Path('docs/BLK-003_blk-pipe-blk-test-orchestration.md'),
    Path('docs/BLK-004_blk-pipe-v47-architecture-suite.md'),
    Path('docs/BLK-007_dependency-graph-recon-tool.md'),
    Path('docs/BLK-008_blk-test-mcp-execution-server.md'),
    Path('docs/BLK-010_blk-pipe-v47-hardening-cli.md'),
    Path('docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md'),
    Path('docs/BLK-013_blk-test-handoff-fixture-contract.md'),
    Path('docs/BLK-014_blk-execution-outcome-fixture-shape.md'),
    Path('README.md'),
]
for p in active:
    text = p.read_text()
    for token in ['AAA_001', 'ceb_id', 'Codex Execution Brief']:
        assert token not in text, f'{p}: stale token {token}'
fixture = Path('testdata/orchestrator/BEB_004_dry_run.md').read_text()
assert 'trace_artifacts:' in fixture
assert 'traced_artifacts:' not in fixture
PY
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

### Commit message

```text
docs: canonicalize blk trace artifacts and execution terminology
```

---

## 10. Task 6 — Define Fail-Closed Approval Gate and Disabled BLK-test MCP Design Stubs

### Objective

Implement only the deterministic contract surfaces needed before live integration: a fail-closed `codex-live` approval gate and disabled-by-default BLK-test MCP request/response shapes. Do not call Codex or BLK-test MCP.

### Files

Create:

- `python/blk_orchestrator_gate.py`
- `python/test_blk_orchestrator_gate.py`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`

Modify:

- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
- `README.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-005_task-006-outcome.md`

### Required behavior

- Add a dependency-free approval/profile gate that returns deterministic decisions for profiles:
  - `dev-smoke`, `strict-ci`, `codex-dry-run` -> allowed for fixture/local paths,
  - `codex-live` -> blocked unless a caller provides an exact explicit approval token shape,
  - `cyber-execution` -> blocked regardless of token in Sprint 005.
- The approval token shape must be explicit and auditable, for example:

  ```text
  BLK_APPROVE_CODEX_LIVE beb_id=<BEB_ID> target_branch=<branch> trace_hash=<sha256:...>
  ```

  The exact shape may be refined during implementation, but it must be deterministic, testable, and documented.

- Even when `codex-live` approval validates, Sprint 005 must not run Codex. The gate may return an `APPROVED_BUT_NOT_EXECUTED` decision or equivalent; live invocation remains future work.
- Define disabled BLK-test MCP request and response shapes, but keep the send path blocked by default. A function may build a request object; it must not open network sockets, spawn MCP, or call live services.
- Define how a future live BLK-test MCP response would map to existing PASS/FAIL/BLOCKED handoff fixtures.
- Keep RTM as an interface/field contract only. Do not generate RTM artifacts.
- Keep BEO as fixture/draft-only. Do not publish authoritative BEOs.

### TDD RED tests

Add tests:

```python
def test_profile_gate_allows_dry_run_profiles(self): ...
def test_profile_gate_rejects_codex_live_without_token(self): ...
def test_profile_gate_accepts_codex_live_token_but_does_not_execute(self): ...
def test_profile_gate_always_rejects_cyber_execution_in_sprint_005(self): ...
def test_build_blk_test_mcp_request_is_disabled_by_default(self): ...
def test_blk_test_mcp_stub_does_not_call_network_or_subprocess(self): ...
```

Expected RED before implementation:

```text
ModuleNotFoundError: No module named 'blk_orchestrator_gate'
```

### Implementation guidance

Suggested API shape:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ProfileDecision:
    profile: str
    allowed: bool
    reason: str
    live_execution_authorized: bool = False

def evaluate_profile_gate(profile: str, *, beb_id: str, target_branch: str, trace_hash: str, approval_token: str | None = None) -> ProfileDecision: ...

def build_blk_test_mcp_request(source_report: dict, *, enabled: bool = False) -> dict: ...
```

If `enabled=False`, `build_blk_test_mcp_request(...)` may return a fixture/design object or raise a clear disabled error. It must not perform a call.

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_blk_orchestrator_gate.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
python3 - <<'PY'
from pathlib import Path
runtime = [
    Path('python/blk_orchestrator_gate.py'),
    Path('python/blk_pipe_dry_run_orchestrator.py'),
    Path('python/blk_test_handoff_fixtures.py'),
    Path('python/beo_fixture_projection.py'),
]
for p in runtime:
    text = p.read_text()
    for token in ['curl ', 'wget ', 'nc ', 'ssh ', 'https://api.openai.com', 'api.anthropic.com', 'shell=True']:
        assert token not in text, f'{p}: forbidden live execution token {token}'
    for live_binary_pattern in ['["codex"', "['codex'", ' exec codex', ' codex exec']:
        assert live_binary_pattern not in text, f'{p}: forbidden real codex invocation token {live_binary_pattern}'
PY
git diff --check
```

### Commit message

```text
feat: define fail-closed blk-pipe approval gate
```

---

## 11. Task 7 — Sprint 005 Closeout and Next-Sprint Seed

### Objective

Close Sprint 005 with audit-grade verification evidence and a narrow next-sprint seed that does not imply live autonomy is approved.

### Files

Create:

- `docs/outcomes/BLK-PIPE-005_sprint-closeout.md`

Modify only if needed:

- `README.md`
- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`

Create outcome:

- The sprint closeout document is the Task 7 outcome. If a separate task outcome is preferred, create `docs/outcomes/BLK-PIPE-005_task-007-outcome.md` and then a separate closeout doc.

### Required closeout contents

- Final task-line implementation commit before closeout.
- Task 1-6 implementation/outcome commit table.
- BLK-PIPE-004 review findings addressed.
- Remaining blocked scope before live Codex/live BLK-test MCP.
- Explicit non-execution statement:
  - Sprint 005 did not run Codex,
  - Sprint 005 did not run live LLMs,
  - Sprint 005 did not run cyber tooling,
  - Sprint 005 did not call live BLK-test MCP,
  - Sprint 005 did not generate RTM or publish authoritative BEOs.
- Verification evidence from the final gate.
- Recommended next sprint seed, likely one of:
  - `BLK-PIPE-006 — Disabled BLK-test MCP Adapter Smoke and BEO/RTM Interface Fixtures`, or
  - `BLK-PIPE-006 — Sandbox and Capability Profile Enforcement Design`,
  depending on which Sprint 005 work lands cleanly.

### Final verification

```bash
set -e
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
go run ./cmd/blk-pipe --health
! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go'
! git grep -n -E 'exec\.Command(Context)?\("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
! git grep -n -E 'git.*diff.*\.\.\.' -- '*.go' ':!*_test.go' docs/BLK-009_blk-pipe-sprint-001-cli.md docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md docs/BLK-013_blk-test-handoff-fixture-contract.md docs/BLK-014_blk-execution-outcome-fixture-shape.md docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md docs/plans/BLK-PIPE-005_integration-contract-hardening-and-approval-gate-design.md docs/outcomes/BLK-PIPE-005_task-001-outcome.md docs/outcomes/BLK-PIPE-005_task-002-outcome.md docs/outcomes/BLK-PIPE-005_task-003-outcome.md docs/outcomes/BLK-PIPE-005_task-004-outcome.md docs/outcomes/BLK-PIPE-005_task-005-outcome.md docs/outcomes/BLK-PIPE-005_task-006-outcome.md docs/outcomes/BLK-PIPE-005_sprint-closeout.md
python3 - <<'PY'
from pathlib import Path
import shutil
shutil.rmtree(Path('python/__pycache__'), ignore_errors=True)
PY
git diff --check
git status --short --branch
```

### Commit message

```text
docs: close out blk-pipe sprint 005
```

---

## 12. Deterministic Review Gates for the Whole Sprint

Run these gates before closing Sprint 005.

### 12.1 `allowed_new_files` proof gate

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('python/blk_pipe_dry_run_orchestrator.py').read_text()
assert 'allowed_modified_files"] = list(payload["allowed_new_files"])' not in text
assert 'allowed_new_files"] = []' not in text
for p in [Path('python/test_blk_pipe_dry_run_orchestrator.py'), Path('python/test_beo_fixture_projection.py')]:
    t = p.read_text()
    assert 'placeholder' not in t or 'dry_run_output.txt' not in t
PY
```

### 12.2 Status taxonomy gate

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('python/blk_test_handoff_fixtures.py').read_text()
assert 'FATAL_OUTPUT_FLOOD' in text
assert '"OUTPUT_FLOOD"' not in text
PY
```

### 12.3 Active doctrine vocabulary gate

```bash
python3 - <<'PY'
from pathlib import Path
active = [
    Path('docs/BLK-002_blk-req-artifact-lifecycle.md'),
    Path('docs/BLK-003_blk-pipe-blk-test-orchestration.md'),
    Path('docs/BLK-004_blk-pipe-v47-architecture-suite.md'),
    Path('docs/BLK-007_dependency-graph-recon-tool.md'),
    Path('docs/BLK-008_blk-test-mcp-execution-server.md'),
    Path('docs/BLK-010_blk-pipe-v47-hardening-cli.md'),
    Path('docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md'),
    Path('docs/BLK-013_blk-test-handoff-fixture-contract.md'),
    Path('docs/BLK-014_blk-execution-outcome-fixture-shape.md'),
    Path('docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md'),
    Path('README.md'),
]
for p in active:
    if not p.exists():
        continue
    text = p.read_text()
    for token in ['AAA_001', 'ceb_id', 'Codex Execution Brief']:
        assert token not in text, f'{p}: stale token {token}'
PY
```

### 12.4 No-live-execution gate

```bash
python3 - <<'PY'
from pathlib import Path
runtime = [
    Path('python/blk_orchestrator_gate.py'),
    Path('python/blk_pipe_dry_run_orchestrator.py'),
    Path('python/blk_test_handoff_fixtures.py'),
    Path('python/beo_fixture_projection.py'),
    Path('testdata/engines/codex-dry-run'),
]
for p in runtime:
    if not p.exists():
        continue
    text = p.read_text()
    for token in ['curl ', 'wget ', 'nc ', 'ssh ', 'https://api.openai.com', 'api.anthropic.com', 'shell=True']:
        assert token not in text, f'{p}: forbidden live execution token {token}'
    for live_binary_pattern in ['["codex"', "['codex'", ' exec codex', ' codex exec']:
        assert live_binary_pattern not in text, f'{p}: forbidden real codex invocation token {live_binary_pattern}'
PY
```

### 12.5 Markdown hygiene gate

```bash
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('docs/plans/BLK-PIPE-005_integration-contract-hardening-and-approval-gate-design.md'),
    *Path('docs/outcomes').glob('BLK-PIPE-005*.md'),
]
fence = chr(96) * 3
for p in paths:
    text = p.read_text()
    assert text.endswith('\n'), f'{p}: missing final newline'
    assert text.count(fence) % 2 == 0, f'{p}: unbalanced fences'
    for i, line in enumerate(text.splitlines(), 1):
        assert line.rstrip() == line, f'{p}:{i}: trailing whitespace'
PY
```

---

## 13. Outcome Documents

Expected outcome documents:

```text
docs/outcomes/BLK-PIPE-005_task-001-outcome.md
docs/outcomes/BLK-PIPE-005_task-002-outcome.md
docs/outcomes/BLK-PIPE-005_task-003-outcome.md
docs/outcomes/BLK-PIPE-005_task-004-outcome.md
docs/outcomes/BLK-PIPE-005_task-005-outcome.md
docs/outcomes/BLK-PIPE-005_task-006-outcome.md
docs/outcomes/BLK-PIPE-005_sprint-closeout.md
```

If Task 7 gets its own separate outcome in addition to the closeout, use:

```text
docs/outcomes/BLK-PIPE-005_task-007-outcome.md
```

---

## 14. Recommended Next Sprint After BLK-PIPE-005

Do not recommend live Codex immediately just because Sprint 005 lands. Depending on results, the next seed should be one of these narrow tracks:

```text
BLK-PIPE-006 — Disabled BLK-test MCP Adapter Smoke and BEO/RTM Interface Fixtures
```

or:

```text
BLK-PIPE-006 — Sandbox and Capability Profile Enforcement Design
```

Live `codex-live` execution remains blocked until a later sprint explicitly approves and verifies:

- the real approval channel,
- sandbox/capability enforcement,
- production credential/network isolation policy,
- live BLK-test MCP policy,
- BEO publication authority,
- RTM generation and drift rejection mechanics.

---

## 15. Quick Resume Prompt

```text
We are in /home/dad/BLK-System. Execute docs/plans/BLK-PIPE-005_integration-contract-hardening-and-approval-gate-design.md using blk-system-sprint-execution. Do not use Hindsight. Do not run live Codex, live tactical LLMs, network model services, cyber tooling, or live BLK-test MCP. Start with Task 1. Use TDD, commit each task, create matching docs/outcomes/BLK-PIPE-005_task-00N-outcome.md, run deterministic review gates, and push only after verification passes.
```
