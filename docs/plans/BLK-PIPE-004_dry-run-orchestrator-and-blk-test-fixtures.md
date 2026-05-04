# BLK-pipe Sprint 004 — Dry-Run Orchestrator and BLK-test Handoff Fixtures Implementation Plan

> **For Hermes:** Use `blk-system-sprint-execution` to implement this plan task-by-task. This sprint is deterministic dry-run fixture work only. Do not run Codex, live LLMs, network model services, cyber tooling, or BLK-test MCP unless a later task plan explicitly authorizes it.

**Goal:** Exercise the right side of the BLK-001 V-model with deterministic dry-run orchestration fixtures before any live Codex path exists.

**Architecture:** BLK-pipe remains the deterministic repository blast shield and bounded transport. Sprint 004 adds dry-run orchestration and handoff fixtures around it: CEB/L2 payload construction, fake Codex command shape, BLK-test PASS/FAIL payload shapes, draft CEO projection, and explicit live approval gate doctrine. The sprint deliberately proves handoff shapes and trace baton continuity without model/API calls.

**Tech Stack:** Go 1.26.x, POSIX-only BLK-pipe CLI, local Python adapter, deterministic Python/Go fixture tests, Markdown doctrine/outcome documents.

---

## 0. Review Verdict Against BLK-001 and BLK-004

### BLK-001 findings

BLK-001 requires strict separation between:

- Hermes as architect/router,
- Codex as tactical worker,
- deterministic binaries/scripts as repository physics,
- BLK-test as the right-side physics oracle,
- traceability/RTM as a later ledger step.

Sprint 003 moved BLK-pipe in the right direction by preserving `trace_artifacts`, blocking protected BLK-req paths, bounding transport work, preserving adapter status detail, and documenting profiles. It did **not** prove the right side of the V-model yet: BLK-test PASS/FAIL handoff, CEO projection, and trace baton continuity across CEB -> L2 -> BLK-pipe -> BLK-test -> CEO are still fixture-only future work.

### BLK-004 findings

BLK-004/V47 defines BLK-pipe as a deterministic transport layer. Current implementation is close enough for dry-run integration fixtures, but two Phase 3 review notes should be resolved before any broader orchestrator work:

1. **Payload-size enforcement:** The CLI caps payload file/stdin ingestion, but direct Go callers can still call `pipe.Run(ctx, payloadJSON, writer)` or `contracts.DecodePayload(data)` with oversized byte slices. Sprint 004 should enforce the same `DefaultMaxPayloadJSONBytes` at the direct decode/run boundary so non-CLI orchestrators cannot bypass the ingress cap.
2. **Adapter status fidelity:** Sprint 003 deliberately preserved compatible report status detail within exit-code families. Sprint 004 should document this as an accepted local V47-compatible extension for BLK-System orchestration rather than collapsing it back to strict V47 status families. Routing must still be by exit-code family and unknown nonzero exits must never report success.

### Next sprint evaluation

The suggested next sprint is correct: **BLK-PIPE-004 — Dry-Run Orchestrator and BLK-test Handoff Fixtures**.

Do **not** go live yet. The next sprint should be planning-first and then implement only deterministic fixtures under `dev-smoke`, `strict-ci`, and `codex-dry-run`. `codex-live` remains blocked behind an explicit hard user approval gate and future sandbox/capability decisions.

---

## 1. Current Known State

Repository:

```text
/home/dad/BLK-System
```

Pre-plan preflight:

```text
git status --short --branch  -> ## main...origin/main
git fetch origin main        -> PASS
go version                   -> go1.26.2 linux/amd64
```

Recently completed sprint:

```text
BLK-PIPE-003 — Integration Readiness and Capability Profiles
Closeout: docs/outcomes/BLK-PIPE-003_sprint-closeout.md
Closeout commit: b106a1b docs: close out blk-pipe sprint 003
```

Sprint 003 next-sprint seed explicitly named:

```text
BLK-PIPE-004 — Dry-Run Orchestrator and BLK-test Handoff Fixtures
```

---

## 2. Non-Goals and Hard Blocks

Sprint 004 must not implement or run:

- live Codex invocation,
- live tactical LLM API calls,
- OpenAI/local model orchestration,
- network model services,
- real `codex-live` profile execution,
- cyber tooling or cyber execution,
- execution against real cyber-program repositories or live targets,
- BLK-test MCP calls unless a later approved sprint scopes live MCP integration,
- RTM generation as a claimed complete traceability ledger,
- broad sandbox/capability enforcement beyond documented approval gates.

Allowed profiles in this sprint:

```text
dev-smoke
strict-ci
codex-dry-run
```

Blocked profiles in this sprint:

```text
codex-live
cyber-execution
```

---

## 3. Invariants to Preserve

Every task must preserve:

1. BLK-pipe does not call LLM APIs and does not make architecture decisions.
2. Fake Codex fixtures must use `codex-dry-run`, not `codex-live`, and must not invoke a real `codex` binary unless it is a local fake fixture under a temporary PATH.
3. `trace_artifacts` remain opaque: preserve `kind`, `id`, and `version_hash`; do not parse requirements/use-case bodies or verify hashes against active vault files in BLK-pipe.
4. `l2_packet` remains bounded and is delivered to engine stdin without being echoed into error/report fields by default.
5. Protected BLK-req vault paths remain denied: `docs/active/`, `docs/requirements/`, and `docs/use_cases/`.
6. No production `git add .`, `git add -u`, `git stash`, relative revert anchors, or triple-dot report diffs.
7. Python subprocess calls remain shell-free.
8. Adapter routing remains exit-code-family first; compatible detailed statuses may be preserved; nonzero unknown exits must not report `SUCCESS`.
9. BLK-test handoff is a fixture contract only unless future approval explicitly scopes MCP.
10. CEO output in this sprint is a draft deterministic shape only; it must not claim full RTM generation.

---

## 4. Controller Workflow for Each Task

For each implementation task:

1. Preflight:

   ```bash
   cd /home/dad/BLK-System
   export PATH="$HOME/.local/bin:$PATH"
   git status --short --branch
   ```

2. Use TDD where code changes are required: write failing tests first, capture RED, implement minimal code, capture GREEN.
3. Run focused tests listed in the task.
4. Run shared verification:

   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   go test ./...
   python3 -m unittest discover -s python -p 'test_*.py'
   go vet ./...
   git diff --check
   ```

5. Run two deterministic review gates without live Codex/live LLM reviewers:
   - deterministic spec/traceability gate,
   - deterministic safety/docs-quality gate.
6. For tasks that add fixture/orchestration code, include static gates proving no active-vault reads, no live model/network tokens, no shell-based Python subprocess invocation, and no `codex-live` fixture construction unless the task explicitly scopes a fail-closed rejection test.
7. Commit implementation with the listed commit message.
8. Create and commit a matching outcome document.
9. Push only after verification passes.

Outcome documents for this sprint:

```text
docs/outcomes/BLK-PIPE-004_task-001-outcome.md
docs/outcomes/BLK-PIPE-004_task-002-outcome.md
docs/outcomes/BLK-PIPE-004_task-003-outcome.md
docs/outcomes/BLK-PIPE-004_task-004-outcome.md
docs/outcomes/BLK-PIPE-004_task-005-outcome.md
docs/outcomes/BLK-PIPE-004_task-006-outcome.md
docs/outcomes/BLK-PIPE-004_task-007-outcome.md
docs/outcomes/BLK-PIPE-004_sprint-closeout.md
```

---

## 5. Task 1 — Enforce Payload Byte Cap at Direct Decode/Run Boundary

### Objective

Resolve the Phase 3 payload-size review note by making the 2 MiB payload cap apply to direct `contracts.DecodePayload` and `pipe.Run` callers, not only CLI file/stdin ingress.

### Files

Modify:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/pipe/run_test.go`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-004_task-001-outcome.md`

### Required behavior

- `contracts.DecodePayload(data)` rejects `len(data) > contracts.DefaultMaxPayloadJSONBytes` before JSON unmarshal.
- `pipe.Run(ctx, payloadJSON, writer)` returns `ExitInvalidPayload` and report status `INVALID_PAYLOAD` for oversized payload JSON.
- Error messages must not echo payload body.
- Existing CLI bounded-read tests must continue to pass.

### TDD RED tests

Add or extend tests:

```go
func TestDecodePayloadRejectsOversizedPayloadBytes(t *testing.T) { ... }
func TestRunRejectsOversizedPayloadBytesBeforeDecode(t *testing.T) { ... }
```

Expected RED before implementation:

```text
DecodePayload oversized direct byte slice unexpectedly accepted or unmarshaled
pipe.Run oversized direct byte slice does not return INVALID_PAYLOAD
```

### Implementation guidance

Add a helper near `DecodePayload`:

```go
func ValidatePayloadJSONSize(data []byte) error {
    if len(data) > DefaultMaxPayloadJSONBytes {
        return fmt.Errorf("payload JSON exceeds maximum size of %d bytes", DefaultMaxPayloadJSONBytes)
    }
    return nil
}
```

Call it as the first line of `DecodePayload`. `pipe.Run` already calls `parseAndValidatePayload`, so the report path should naturally become `INVALID_PAYLOAD`; add explicit tests to prove it.

### Focused verification

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/contracts -run 'TestDecodePayloadRejectsOversized|TestPayloadFile|TestPayloadStdin' -v
go test ./internal/pipe -run 'TestRunRejectsOversized|TestRun.*InvalidPayload' -v
go test ./cmd/blk-pipe -run 'TestPayload.*Oversized' -v
go test ./...
go vet ./...
git diff --check
```

### Commit message

```text
fix: enforce blk-pipe payload cap for direct callers
```

---

## 6. Task 2 — Freeze Adapter Status Fidelity as a Local V47-Compatible Extension

### Objective

Resolve the Phase 3 adapter-status review note by documenting the decision: preserve compatible status detail within exit-code families as a BLK-System local V47-compatible extension.

### Files

Modify:

- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md`
- `python/test_blk_pipe_adapter.py` only if coverage is missing
- `python/blk_pipe_adapter.py` only if tests expose drift

Create outcome:

- `docs/outcomes/BLK-PIPE-004_task-002-outcome.md`

### Required behavior

Document that:

- strict V47 core codes `0-5` remain the routing backbone,
- local extension codes `6`, `7`, and `9` remain BLK-System local statuses,
- exit code `2` may preserve `INVALID_PAYLOAD` or `SYNTAX_GATE_FAILED`,
- exit code `1` may preserve `FATAL_SYSTEM_PANIC` or `FATAL_ENGINE_FAILED`,
- incompatible report statuses collapse to the family default,
- unknown nonzero exits force `INTERNAL_ERROR`, even if stdout claims `SUCCESS`.

### TDD / docs RED gate

Before doc changes, run a deterministic check that fails if the docs do not state:

```text
local V47-compatible extension
exit-code family
INVALID_PAYLOAD
unknown nonzero
```

If adapter tests already cover the behavior, do not add duplicate tests. If coverage is missing, add narrow Python unit tests for the missing mapping.

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_*.py'
python3 - <<'PY'
from pathlib import Path
required = [
    'local V47-compatible extension',
    'exit-code family',
    'INVALID_PAYLOAD',
    'unknown nonzero',
]
text = Path('docs/BLK-010_blk-pipe-v47-hardening-cli.md').read_text() + '\n' + Path('docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md').read_text()
for phrase in required:
    assert phrase in text, phrase
PY
git diff --check
```

### Commit message

```text
docs: freeze blk-pipe adapter status fidelity decision
```

---

## 7. Task 3 — Add CEB/L2 to BLK-pipe Payload Construction Fixtures

### Objective

Create deterministic Python fixture code that converts representative CEB/L2 input into a BLK-004-compatible BLK-pipe payload using the `codex-dry-run` profile.

### Files

Create:

- `python/blk_pipe_dry_run_orchestrator.py`
- `python/test_blk_pipe_dry_run_orchestrator.py`
- `testdata/orchestrator/CEB_004_dry_run.md`
- `testdata/orchestrator/L2_004_dry_run.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-004_task-003-outcome.md`

### Required behavior

The fixture builder must produce payload JSON with:

```json
{
  "action": "execute",
  "ceb_id": "CEB_004",
  "work_dir": "/absolute/path/to/ephemeral/repo",
  "target_branch": "sprint/blk-pipe-004-dry-run",
  "engine": "codex-dry-run",
  "engine_args": [
    "exec",
    "-",
    "--json",
    "--isolated",
    "--yes",
    "--deny-read=**/.git/**",
    "--deny-read=**/node_modules/**",
    "--deny-read=**/.env*",
    "--dry-run"
  ],
  "l2_packet": "...bounded fixture text...",
  "trace_artifacts": [
    {
      "kind": "REQ",
      "id": "REQ-DRY-001",
      "version_hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
  ],
  "validation_commands": ["test -f dry_run_output.txt"],
  "allowed_modified_files": [],
  "allowed_new_files": ["dry_run_output.txt"]
}
```

Requirements:

- Use `codex-dry-run`, not `codex-live`.
- Do not call the adapter or BLK-pipe in this task; this is payload construction only.
- Validate structure with deterministic unit tests only. BLK-pipe/adapter invocation is deferred to Task 4.
- `REQ-DRY-001` is a synthetic fixture identifier only. It is not a BLK-req baseline and must not be created, edited, promoted, or reconciled under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`.
- Include `trace_artifacts` and preserve `version_hash` exactly.
- The dry-run command shape must include the BLK-003 required isolation envelope: `--json`, `--isolated`, `--yes`, and deny-read flags for `.git`, `node_modules`, and `.env*`.
- Keep CEB and L2 fixture text small and deterministic.

### TDD RED tests

```python
def test_build_payload_uses_codex_dry_run_profile(self): ...
def test_build_payload_includes_blk003_required_isolation_args(self): ...
def test_build_payload_preserves_l2_packet_and_trace_artifacts(self): ...
def test_build_payload_rejects_codex_live_profile(self): ...
def test_build_payload_rejects_empty_unknown_and_cyber_profiles(self): ...
def test_build_payload_uses_absolute_work_dir(self): ...
def test_build_payload_uses_l2_fixture_bytes_exactly(self): ...
def test_build_payload_rejects_ceb_l2_id_mismatch(self): ...
def test_build_payload_rejects_missing_trace_artifact_in_ceb_fixture(self): ...
```

### Implementation guidance

Prefer a small, dependency-free API:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class TraceArtifact:
    kind: str
    id: str
    version_hash: str

@dataclass(frozen=True)
class DryRunSprintInput:
    ceb_id: str
    profile: str
    work_dir: str
    target_branch: str
    l2_packet: str
    trace_artifacts: list[TraceArtifact]
    allowed_new_files: list[str]
    validation_commands: list[str]

def build_codex_dry_run_payload(input: DryRunSprintInput) -> dict: ...
```

Do not introduce YAML parsing or broad CEB parsing in this sprint. These are handoff fixtures, not a full orchestrator. Do require narrow fixture binding so `testdata/orchestrator/CEB_004_dry_run.md` and `testdata/orchestrator/L2_004_dry_run.md` are not ornamental: the loader must reject CEB/L2 ID mismatches and missing trace-artifact metadata, and the payload must use the L2 fixture bytes exactly.

The builder must fail closed unless `input.profile == "codex-dry-run"`. It must reject `codex-live`, `cyber-execution`, empty profile strings, and unknown profiles before payload construction.

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_blk_pipe_dry_run_orchestrator.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
git diff --check
```

### Commit message

```text
feat: add blk-pipe dry-run payload fixtures
```

---

## 8. Task 4 — Prove Fake Codex Command Shape Through BLK-pipe

### Objective

Execute a deterministic fake Codex command shape through BLK-pipe using the payload fixture from Task 3, with no live Codex, no model calls, and no network dependency.

### Files

Modify:

- `python/blk_pipe_dry_run_orchestrator.py`
- `python/test_blk_pipe_dry_run_orchestrator.py`

Create:

- `testdata/engines/codex-dry-run`

Create outcome:

- `docs/outcomes/BLK-PIPE-004_task-004-outcome.md`

### Required behavior

- The fixture engine command shape must look like a Codex dry-run path but invoke only the local fake `codex-dry-run` fixture.
- Fake engine reads `l2_packet` from stdin and writes deterministic `dry_run_output.txt` in the workdir.
- BLK-pipe commits only `dry_run_output.txt` on success.
- Report includes:
  - `status: SUCCESS`,
  - `trace_artifacts` unchanged,
  - non-empty `pre_engine_hash`,
  - non-empty `commit_hash`,
  - `staged_files` containing `dry_run_output.txt`,
  - bounded `engine_logs`.

### TDD RED tests

```python
def test_dry_run_fixture_invokes_blk_pipe_and_commits_allowed_file(self): ...
def test_dry_run_fixture_preserves_trace_artifacts_in_report(self): ...
def test_dry_run_fixture_does_not_call_real_codex(self): ...
```

### Implementation guidance

Use a hermetic temporary Git repo in the Python test:

1. Initialize a temp repo.
2. Commit a baseline file.
3. Prepend `testdata/engines` or a temp copied fake binary directory to `PATH` only for the subprocess under test.
4. Build or invoke the BLK-pipe binary without shell.
5. Invoke with a thin helper around `[binary, "--payload", temp_payload_path]` and assert directly against the raw JSON report, or first extend `BlkPipeAdapter.ExecutionResult` to expose `commit_hash` and `staged_files`. Do not rely on the current adapter shape for these assertions.
6. Assert no `codex-live`, live `codex` binary, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, other model credentials, or network model configuration is used. Use a poisoned environment in tests and make the fake engine fail if common LLM credentials are visible.
7. The fake engine must emit a deterministic provenance marker such as `FAKE_CODEX_DRY_RUN_FIXTURE=BLK-PIPE-004` in bounded `engine_logs`, and tests must assert the marker so PATH drift cannot silently call the wrong executable.

If using a script fixture, keep it POSIX shell and deterministic. It must not call `codex` or any network command.

### Focused verification

```bash
export PATH="$HOME/.local/bin:$PATH"
go build -o /tmp/blk-pipe-sprint-004 ./cmd/blk-pipe
python3 -m unittest discover -s python -p 'test_blk_pipe_dry_run_orchestrator.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
rm -f /tmp/blk-pipe-sprint-004
```

### Commit message

```text
feat: run blk-pipe codex dry-run fixture
```

---

## 9. Task 5 — Add BLK-test PASS/FAIL Handoff Fixture Contract

### Objective

Define deterministic BLK-test PASS/FAIL payload shapes that can consume a BLK-pipe execution report without calling live BLK-test MCP.

### Files

Create or modify:

- `python/blk_test_handoff_fixtures.py`
- `python/test_blk_test_handoff_fixtures.py`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-004_task-005-outcome.md`

### Required PASS shape

```json
{
  "status": "PASS",
  "ceb_id": "CEB_004",
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
  "compressed_logs": "...bounded deterministic text..."
}
```

### Required FAIL shape

```json
{
  "status": "FAIL",
  "ceb_id": "CEB_004",
  "commit_hash": "<optional blk-pipe commit or empty>",
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
  "compressed_logs": "...bounded deterministic text..."
}
```

### Required behavior

- No MCP call.
- No live test server dependency.
- No LLM judgment of pass/fail.
- PASS/FAIL is derived deterministically from fixture inputs.
- PASS requires a source BLK-pipe report with `status == SUCCESS`, non-empty `commit_hash`, non-empty `pre_engine_hash`, `staged_files == ["dry_run_output.txt"]`, and non-empty `trace_artifacts`.
- Trace artifacts are preserved from the BLK-pipe report when present for both PASS and FAIL payloads; FAIL status must not erase the `version_hash` baton.
- Logs are bounded and deduplicated enough for fixture purposes.
- Fixture code must not read or inspect `docs/active/`, `docs/requirements/`, `docs/use_cases/`, or call any requirements-fetching tool; it consumes only the supplied BLK-pipe report fixture.

### TDD RED tests

```python
def test_blk_test_pass_payload_preserves_trace_artifacts(self): ...
def test_blk_test_pass_payload_rejects_non_success_blk_pipe_report(self): ...
def test_blk_test_pass_payload_rejects_missing_commit_hash(self): ...
def test_blk_test_pass_payload_requires_expected_staged_file(self): ...
def test_blk_test_fail_payload_preserves_trace_artifacts_when_present(self): ...
def test_blk_test_fail_payload_uses_fail_status_and_bounded_logs(self): ...
def test_blk_test_fixture_rejects_unknown_status(self): ...
def test_blk_test_fixture_does_not_read_active_vault(self): ...
```

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_blk_test_handoff_fixtures.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
git diff --check
```

### Commit message

```text
feat: add blk-test handoff fixtures
```

---

## 10. Task 6 — Draft CEO Shape From BLK-test PASS Fixture

### Objective

Show how a successful BLK-test fixture result becomes a draft Codex Execution Outcome shape while preserving trace baton fields.

### Files

Create or modify:

- `python/ceo_fixture_projection.py`
- `python/test_ceo_fixture_projection.py`
- `docs/BLK-014_codex-execution-outcome-fixture-shape.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-004_task-006-outcome.md`

### Required CEO draft shape

```json
{
  "ceo_id": "CEO_004",
  "ceb_id": "CEB_004",
  "status": "PASS",
  "source": "blk-test-fixture",
  "commit_hash": "<blk-pipe commit>",
  "pre_engine_hash": "<blk-pipe pre_engine_hash>",
  "trace_artifacts": [
    {
      "kind": "REQ",
      "id": "REQ-DRY-001",
      "version_hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
  ],
  "test_summary": {
    "profile": "strict-ci",
    "checks_passed": 1,
    "checks_failed": 0
  },
  "rtm_status": "NOT_GENERATED"
}
```

### Required behavior

- PASS BLK-test fixture can produce a draft CEO fixture.
- FAIL BLK-test fixture cannot produce a success CEO; it must produce either a failed CEO fixture or a clear rejection object while preserving trace artifacts when present.
- `trace_artifacts` / `version_hash` must survive unchanged.
- Include an end-to-end deterministic test proving exact trace baton continuity across CEB/L2 payload construction -> BLK-pipe fixture report -> BLK-test PASS payload -> CEO projection.
- Do not claim full RTM generation.
- Do not inspect active BLK-req files; tests must prove no reads of `docs/active/`, `docs/requirements/`, or `docs/use_cases/`.

### TDD RED tests

```python
def test_pass_blk_test_result_projects_to_ceo_shape(self): ...
def test_ceo_projection_preserves_trace_artifacts_exactly(self): ...
def test_fail_blk_test_result_does_not_project_success_ceo(self): ...
def test_ceo_projection_marks_rtm_not_generated(self): ...
def test_trace_baton_exact_across_dry_run_loop(self): ...
def test_ceo_projection_does_not_read_active_vault(self): ...
```

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_ceo_fixture_projection.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
git diff --check
```

### Commit message

```text
feat: draft ceo fixture projection
```

---

## 11. Task 7 — Document Hard Live Approval Gate and Close Dry-Run Loop

### Objective

Add operator-facing docs and fixture-builder tests that prevent Sprint 004 fixture code from constructing `codex-live` payloads. This is fixture-level fail-closed enforcement only; it is not a system-wide live approval gate implementation.

### Files

Modify:

- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_codex-execution-outcome-fixture-shape.md`
- `README.md`
- `python/test_blk_pipe_dry_run_orchestrator.py`

Create outcome:

- `docs/outcomes/BLK-PIPE-004_task-007-outcome.md`

### Required behavior

- Default profile remains one of `dev-smoke`, `strict-ci`, or `codex-dry-run`.
- Any `codex-live` path in Sprint 004 fixture builders must fail closed before payload construction. A future real `codex-live` path must require a hard user approval gate with explicit approval token/phrase and future sandbox/capability decisions.
- Sprint 004 docs must state:
  - no live Codex,
  - no live LLM,
  - no cyber execution,
  - BLK-test is fixture-only,
  - CEO is fixture/draft-only,
  - RTM is not generated.
- Python tests must reject attempts to build a dry-run payload with `codex-live`.

### Deterministic docs gate

```bash
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md'),
    Path('docs/BLK-013_blk-test-handoff-fixture-contract.md'),
    Path('docs/BLK-014_codex-execution-outcome-fixture-shape.md'),
    Path('README.md'),
]
required = [
    'codex-live',
    'hard user approval gate',
    'Sprint 004 does not run Codex',
    'Sprint 004 does not authorize live LLM execution',
    'BLK-test fixture',
    'RTM is not generated',
    'fixture-level fail-closed enforcement only',
    'does not inspect active BLK-req files',
]
fence = chr(96) * 3
for p in paths:
    text = p.read_text()
    assert text.endswith('\n'), f'{p}: missing final newline'
    assert text.count(fence) % 2 == 0, f'{p}: unbalanced fences'
    for i, line in enumerate(text.splitlines(), 1):
        assert line.rstrip() == line, f'{p}:{i}: trailing whitespace'
combined = '\n'.join(p.read_text() for p in paths)
for phrase in required:
    assert phrase in combined, phrase
per_file_required = {
    Path('docs/BLK-013_blk-test-handoff-fixture-contract.md'): [
        'BLK-test fixture',
        'no live BLK-test MCP',
        'PASS requires BLK-pipe SUCCESS',
    ],
    Path('docs/BLK-014_codex-execution-outcome-fixture-shape.md'): [
        'CEO is fixture/draft-only',
        'RTM is not generated',
        'does not inspect active BLK-req files',
    ],
    Path('README.md'): [
        'Sprint 004 does not run Codex',
        'Sprint 004 does not authorize live LLM execution',
        'hard user approval gate',
    ],
}
for p, phrases in per_file_required.items():
    text = p.read_text()
    for phrase in phrases:
        assert phrase in text, f'{p}: {phrase}'
PY
```

Additional static fixture safety gate:

```bash
python3 - <<'PY'
from pathlib import Path
fixture_paths = [
    Path('python/blk_pipe_dry_run_orchestrator.py'),
    Path('python/blk_test_handoff_fixtures.py'),
    Path('python/ceo_fixture_projection.py'),
    Path('testdata/engines/codex-dry-run'),
]
for p in fixture_paths:
    if not p.exists():
        continue
    text = p.read_text()
    for token in ['docs/active', 'docs/requirements', 'docs/use_cases', 'fetch_requirements_context']:
        assert token not in text, f'{p}: forbidden active-vault access token {token}'
    for token in ['curl ', 'wget ', 'nc ', 'ssh ', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'codex-live']:
        assert token not in text, f'{p}: forbidden live-model/network token {token}'
PY
```

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

### Commit message

```text
docs: define blk-pipe live approval gate
```

---

## 12. Sprint Closeout Requirements

After Tasks 1-7 are complete and pushed, create:

```text
docs/outcomes/BLK-PIPE-004_sprint-closeout.md
```

Closeout must include:

1. Final task-line implementation commit before closeout.
2. Task commits and outcome docs table.
3. BLK-001 alignment summary:
   - CEB/L2 dry-run handoff exercised,
   - BLK-pipe payload/report trace baton preserved,
   - BLK-test fixture PASS/FAIL handoff defined,
   - draft CEO shape created,
   - RTM explicitly not generated,
   - fixture-level `codex-live` rejection implemented without claiming a real system-wide approval gate.
4. BLK-004 alignment summary:
   - V47-compatible payload fields preserved,
   - payload cap direct caller gap resolved,
   - adapter status fidelity decision documented,
   - no broad staging/stash/relative anchor/triple-dot drift.
5. Explicit non-execution statement:
   - Sprint 004 did not run Codex,
   - Sprint 004 did not run live LLMs,
   - Sprint 004 did not run cyber tooling,
   - Sprint 004 did not call live BLK-test MCP.
6. Remaining blocked scope before live Codex:
   - actual orchestrator service wiring,
   - live BLK-test MCP integration,
   - full CEO publication workflow,
   - RTM aggregator implementation,
   - sandbox/capability enforcement beyond docs,
   - hard user approval gate implementation with a real approval channel,
   - production credential/network isolation policy for live tactical engines.
7. Verification evidence.
8. Recommended next sprint seed.

Final closeout verification:

```bash
set -e
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
go run ./cmd/blk-pipe --health
! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go'
! git grep -n -E 'exec\.Command(Context)?\("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
! git grep -n -E 'git.*diff.*\.\.\.' -- '*.go' ':!*_test.go' docs/BLK-009_blk-pipe-sprint-001-cli.md docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md docs/BLK-013_blk-test-handoff-fixture-contract.md docs/BLK-014_codex-execution-outcome-fixture-shape.md docs/plans/BLK-PIPE-004_dry-run-orchestrator-and-blk-test-fixtures.md docs/outcomes/BLK-PIPE-004_task-001-outcome.md docs/outcomes/BLK-PIPE-004_task-002-outcome.md docs/outcomes/BLK-PIPE-004_task-003-outcome.md docs/outcomes/BLK-PIPE-004_task-004-outcome.md docs/outcomes/BLK-PIPE-004_task-005-outcome.md docs/outcomes/BLK-PIPE-004_task-006-outcome.md docs/outcomes/BLK-PIPE-004_task-007-outcome.md docs/outcomes/BLK-PIPE-004_sprint-closeout.md
git diff --check
git status --short --branch
```

If Python tests create `python/__pycache__/`, remove it before committing docs:

```bash
python3 - <<'PY'
import shutil
from pathlib import Path
shutil.rmtree(Path('python/__pycache__'), ignore_errors=True)
PY
```

---

## 13. Recommended Next Sprint After BLK-PIPE-004

If Sprint 004 closes cleanly, the system should still avoid immediate live autonomy unless explicitly approved. Recommended next seed:

```text
BLK-PIPE-005 — Orchestrator Approval Gate and BLK-test MCP Integration Design
```

Possible scope:

- implement a real hard approval gate for `codex-live`,
- wire BLK-test MCP in a disabled-by-default or fixture-first mode,
- define CEO publication workflow,
- define RTM aggregation interface,
- decide sandbox/capability enforcement for live tactical execution.

`codex-live` should remain blocked until that later sprint is explicitly approved and verified.

---

## 14. Quick Resume Prompt

```text
We are in /home/dad/BLK-System. Execute docs/plans/BLK-PIPE-004_dry-run-orchestrator-and-blk-test-fixtures.md using blk-system-sprint-execution. Do not use Hindsight. Do not run live Codex, live LLMs, network model services, cyber tooling, or live BLK-test MCP. Start with Task 1. Use TDD, commit each task, create matching docs/outcomes/BLK-PIPE-004_task-00N-outcome.md, run deterministic review gates, and push only after verification passes.
```
