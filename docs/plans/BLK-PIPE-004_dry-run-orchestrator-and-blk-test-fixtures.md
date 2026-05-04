# BLK-pipe Sprint 004 — Dry-Run Orchestrator and BLK-test Handoff Fixtures Implementation Plan

> **For Hermes:** Use `blk-system-sprint-execution` to implement this plan task-by-task. This sprint is deterministic dry-run fixture work only. Do not run live tactical LLMs, network model services, cyber tooling, or BLK-test MCP unless a later task plan explicitly authorizes it.

**Goal:** Exercise the right side of the BLK-001 V-model with deterministic dry-run orchestration fixtures before any live Codex path exists.

**Architecture:** BLK-pipe remains the deterministic repository blast shield and bounded transport. Sprint 004 adds dry-run orchestration and handoff fixtures around it: BEB/L2 payload construction, fake tactical-engine command shape, BLK-test PASS/FAIL payload shapes, draft BEO projection, and explicit live approval gate doctrine. The sprint deliberately proves handoff shapes and trace baton continuity without model/API calls.

**Tech Stack:** Go 1.26.x, POSIX-only BLK-pipe CLI, local Python adapter, deterministic Python/Go fixture tests, Markdown doctrine/outcome documents.

---

## 0. Review Verdict Against BLK-001 and BLK-004

### BLK-001 findings

BLK-001 requires strict separation between:

- Hermes as architect/router,
- a tactical engine as bounded worker,
- deterministic binaries/scripts as repository physics,
- BLK-test as the right-side physics oracle,
- traceability/RTM as a later ledger step.

Sprint 003 moved BLK-pipe in the right direction by preserving `trace_artifacts`, blocking protected BLK-req paths, bounding transport work, preserving adapter status detail, and documenting profiles. It did **not** prove the right side of the V-model yet: BLK-test PASS/FAIL handoff, BEO projection, and trace baton continuity across BEB -> L2 -> BLK-pipe -> BLK-test -> BEO are still fixture-only future work.

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
2. Fake tactical-engine fixtures must use `codex-dry-run`, not `codex-live`, and must not invoke a real `codex` binary unless it is a local fake fixture under a temporary PATH.
3. `trace_artifacts` remain opaque: preserve `kind`, `id`, and `version_hash`; do not parse requirements/use-case bodies or verify hashes against active vault files in BLK-pipe.
4. `l2_packet` remains bounded and is delivered to engine stdin without being echoed into error/report fields by default.
5. Protected BLK-req vault paths remain denied: `docs/active/`, `docs/requirements/`, and `docs/use_cases/`.
6. No production `git add .`, `git add -u`, `git stash`, relative revert anchors, or triple-dot report diffs.
7. Python subprocess calls remain shell-free. This does not change the existing BLK-pipe validation-command contract: `validation_commands` remain payload command strings executed by the validation gate.
8. Adapter routing remains exit-code-family first; compatible detailed statuses may be preserved; nonzero unknown exits must not report `SUCCESS`.
9. BLK-test handoff is a fixture contract only unless future approval explicitly scopes MCP.
10. BEO output in this sprint is a draft deterministic shape only; it must not claim full RTM generation.

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
docs/outcomes/BLK-PIPE-004_task-008-outcome.md
docs/outcomes/BLK-PIPE-004_sprint-closeout.md
```

---

## 5. Task 1 — Rename Execution Identity From `ceb_id` to BLK-Native `beb_id`

### Objective

Remove stale AAA_001/CEB terminology from the BLK-pipe transport contract before dry-run orchestration work begins. BLK-System now uses BLK-native BEB/BEO terminology only; `beb_id` is the execution identity field and `beb_id`/CEB compatibility must not remain the canonical path.

### Files

Modify:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/contracts/report.go`
- `internal/pipe/run_test.go`
- `python/blk_pipe_adapter.py`
- `python/test_blk_pipe_adapter.py`
- `docs/BLK-001_blk-system-master-architecture.md`
- `docs/BLK-004_blk-pipe-v47-architecture-suite.md`
- `docs/BLK-005_blk-req-specification.md`
- `docs/BLK-006_blk-req-implementation-brief.md`
- `docs/BLK-009_blk-pipe-sprint-001-cli.md`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-004_task-001-outcome.md`

### Required behavior

- Payloads use `beb_id` for execution identity.
- Reports emit `beb_id` for execution identity.
- Python adapter `execute_sprint(...)` accepts `beb_id` and writes `beb_id` into payload JSON.
- Revert payloads use `beb_id: "REVERT"`.
- New tests and docs must use BEB/BEO naming.
- `ceb_id` must not remain the canonical field in BLK-System code, docs, or tests. If a temporary migration alias is unavoidable for already-shipped payload compatibility, it must be explicitly marked deprecated, tested as non-canonical, and scheduled for removal; do not use it in Sprint 004 fixtures.
- AAA_001 is obsolete for BLK-System and must not be cited as governing doctrine.

### TDD RED tests

Add or update tests:

```go
func TestDecodePayloadAcceptsBEBID(t *testing.T) { ... }
func TestReportEmitsBEBID(t *testing.T) { ... }
func TestDecodePayloadDoesNotRequireLegacyCEBID(t *testing.T) { ... }
```

```python
def test_execute_sprint_writes_beb_id(self): ...
def test_revert_payload_uses_beb_id(self): ...
```

Expected RED before implementation:

```text
payload/report/adapter still use ceb_id or CEB fixture IDs
```

### Implementation guidance

Rename public structs/fields deliberately rather than adding shadow fields that keep stale terminology alive. Update JSON tags, test fixture IDs, docs tables, examples, and Python dataclass/API names together so the executor does not carry both vocabularies into later tasks.

### Focused verification

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/contracts -run 'Test.*BEB|Test.*Beb|Test.*Payload' -v
go test ./internal/pipe -run 'Test.*BEB|Test.*Beb|Test.*Report|TestRun.*InvalidPayload' -v
python3 -m unittest discover -s python -p 'test_blk_pipe_adapter.py' -v
go test ./...
python3 -m unittest discover -s python -p 'test_*.py'
go vet ./...
git diff --check
```

### Commit message

```text
fix: rename blk-pipe execution identity to beb_id
```

---

## 6. Task 2 — Enforce Payload Byte Cap at Direct Decode/Run Boundary

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

- `docs/outcomes/BLK-PIPE-004_task-002-outcome.md`

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
go test ./internal/contracts -run 'TestDecodePayloadRejectsOversized' -v
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

## 7. Task 3 — Freeze Adapter Status Fidelity as a Local V47-Compatible Extension

### Objective

Resolve the Phase 3 adapter-status review note by documenting the decision: preserve compatible status detail within exit-code families as a BLK-System local V47-compatible extension.

### Files

Modify:

- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md`
- `python/test_blk_pipe_adapter.py` only if coverage is missing
- `python/blk_pipe_adapter.py` only if tests expose drift

Create outcome:

- `docs/outcomes/BLK-PIPE-004_task-003-outcome.md`

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

## 8. Task 4 — Add BEB/L2 to BLK-pipe Payload Construction Fixtures

### Objective

Create deterministic Python fixture code that converts representative BEB/L2 input into a BLK-004-compatible BLK-pipe payload using the `codex-dry-run` profile.

### Files

Create:

- `python/blk_pipe_dry_run_orchestrator.py`
- `python/test_blk_pipe_dry_run_orchestrator.py`
- `testdata/orchestrator/BEB_004_dry_run.md`
- `testdata/orchestrator/L2_004_dry_run.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-004_task-004-outcome.md`

### Required behavior

The fixture builder must produce payload JSON with:

```json
{
  "action": "execute",
  "beb_id": "BEB_004",
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
- Validate structure with deterministic unit tests only. BLK-pipe/adapter invocation is deferred to Task 5.
- `REQ-DRY-001` is a synthetic fixture identifier only. It is not a BLK-req baseline and must not be created, edited, promoted, or reconciled under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`.
- Include `trace_artifacts` and preserve `version_hash` exactly.
- The dry-run command shape must include the BLK-003 required isolation envelope: `--json`, `--isolated`, `--yes`, and deny-read flags for `.git`, `node_modules`, and `.env*`.
- Keep BEB and L2 fixture text small and deterministic.

### TDD RED tests

```python
def test_build_payload_uses_codex_dry_run_profile(self): ...
def test_build_payload_includes_blk003_required_isolation_args(self): ...
def test_build_payload_preserves_l2_packet_and_trace_artifacts(self): ...
def test_build_payload_rejects_codex_live_profile(self): ...
def test_build_payload_rejects_empty_unknown_and_cyber_profiles(self): ...
def test_build_payload_uses_absolute_work_dir(self): ...
def test_build_payload_uses_l2_fixture_bytes_exactly(self): ...
def test_build_payload_rejects_beb_l2_id_mismatch(self): ...
def test_build_payload_rejects_missing_trace_artifact_in_beb_fixture(self): ...
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
    beb_id: str
    profile: str
    work_dir: str
    target_branch: str
    l2_packet: str
    trace_artifacts: list[TraceArtifact]
    allowed_new_files: list[str]
    validation_commands: list[str]

def build_codex_dry_run_payload(input: DryRunSprintInput) -> dict: ...

def load_dry_run_fixture(
    beb_path: Path,
    l2_path: Path,
    work_dir: str,
    profile: str = "codex-dry-run",
) -> DryRunSprintInput: ...
```

The BEB fixture must use this narrow YAML frontmatter shape; do not invent a broader parser:

```yaml
---
beb_id: "BEB_004"
l2_id: "L2_004"
iteration: 1
status: "FIXTURE"
sprint_base_hash: "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
traced_artifacts:
  - kind: "REQ"
    id: "REQ-DRY-001"
    version_hash: "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
---
```

The L2 fixture must include matching identity markers such as `L2_ID: L2_004` and `BEB_ID: BEB_004`; the loader must use the L2 fixture bytes exactly as the payload `l2_packet`.

Do not introduce broad YAML parsing or broad BEB parsing in this sprint. These are handoff fixtures, not a full orchestrator. Do require narrow fixture binding so `testdata/orchestrator/BEB_004_dry_run.md` and `testdata/orchestrator/L2_004_dry_run.md` are not ornamental: the loader must reject BEB/L2 ID mismatches and missing trace-artifact metadata, and the payload must use the L2 fixture bytes exactly.

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

## 9. Task 5 — Prove Fake Tactical-Engine Command Shape Through BLK-pipe

### Objective

Execute a deterministic fake tactical-engine command shape through BLK-pipe using the payload fixture from Task 4, with no live Codex, no model calls, and no network dependency.

### Files

Modify:

- `python/blk_pipe_dry_run_orchestrator.py`
- `python/test_blk_pipe_dry_run_orchestrator.py`

Create:

- `testdata/engines/codex-dry-run`

Create outcome:

- `docs/outcomes/BLK-PIPE-004_task-005-outcome.md`

### Required behavior

- The fixture engine command shape must look like a tactical-engine dry-run path but invoke only the local fake `codex-dry-run` fixture.
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
5. Invoke with a thin helper around `[binary, "--payload", temp_payload_path]` and assert directly against the raw JSON report for `status`, `beb_id`, `pre_engine_hash`, `commit_hash`, `staged_files`, `trace_artifacts`, and `engine_logs`. Only use `BlkPipeAdapter.ExecutionResult` for these assertions if this task first extends the adapter to expose every required field and adds adapter regression tests for those fields. Do not silently skip commit/staging assertions.
6. Assert no `codex-live` payload path, live `codex` binary, live model API call, or network model configuration is used. Poisoned environment tests may include `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, and Codex OAuth/session variables to prove fixture fail-closed provenance, but they do not prove host-secret isolation unless a separate production engine environment-scrub task is explicitly added. Do not assume Codex live auth is API-key only; future live Codex support must allow both OAuth/session auth and API-key auth behind the approval gate.
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

## 10. Task 6 — Add BLK-test PASS/FAIL Handoff Fixture Contract

### Objective

Define deterministic BLK-test PASS/FAIL payload shapes that can consume a BLK-pipe execution report without calling live BLK-test MCP.

### Files

Create or modify:

- `python/blk_test_handoff_fixtures.py`
- `python/test_blk_test_handoff_fixtures.py`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-004_task-006-outcome.md`

### Required PASS shape

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
  "compressed_logs": "...bounded deterministic text..."
}
```

### Required FAIL shape

```json
{
  "status": "FAIL",
  "beb_id": "BEB_004",
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
- PASS/FAIL/BLOCKED is derived deterministically from fixture inputs.
- PASS requires a source BLK-pipe report with `status == SUCCESS`, non-empty `commit_hash`, non-empty `pre_engine_hash`, `staged_files == ["dry_run_output.txt"]`, and non-empty `trace_artifacts`.
- BLK-test FAIL represents fixture checks failing after a successful BLK-pipe execution; it still requires source `status == SUCCESS`, non-empty `commit_hash`, non-empty `pre_engine_hash`, and preserved `trace_artifacts`.
- A non-success BLK-pipe report must not be converted into BLK-test FAIL. It must produce a separate `BLOCKED` handoff or rejection object that preserves safe trace artifacts when present and clearly states BLK-test did not run.
- Trace artifacts are preserved from the BLK-pipe report when present for PASS, FAIL, and BLOCKED payloads; failure status must not erase the `version_hash` baton.
- Logs are bounded and deduplicated enough for fixture purposes.
- Fixture code must not read or inspect `docs/active/`, `docs/requirements/`, `docs/use_cases/`, or call any requirements-fetching tool; it consumes only the supplied BLK-pipe report fixture.

### TDD RED tests

```python
def test_blk_test_pass_payload_preserves_trace_artifacts(self): ...
def test_blk_test_pass_payload_rejects_non_success_blk_pipe_report(self): ...
def test_blk_test_fail_payload_rejects_non_success_blk_pipe_report(self): ...
def test_blk_test_blocked_payload_handles_non_success_blk_pipe_report(self): ...
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

## 11. Task 7 — Draft BEO Shape From BLK-test PASS Fixture

### Objective

Show how a successful BLK-test fixture result becomes a draft Blk Execution Outcome shape while preserving trace baton fields.

### Files

Create or modify:

- `python/beo_fixture_projection.py`
- `python/test_beo_fixture_projection.py`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-004_task-007-outcome.md`

### Required BEO draft shape

```json
{
  "beo_id": "BEO_004",
  "beb_id": "BEB_004",
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

- PASS BLK-test fixture can produce a draft BEO fixture.
- FAIL BLK-test fixture cannot produce a success BEO; it must produce either a failed BEO fixture or a clear rejection object while preserving trace artifacts when present.
- `trace_artifacts` / `version_hash` must survive unchanged.
- Include an end-to-end deterministic test proving exact trace baton continuity across BEB/L2 payload construction -> real BLK-pipe fake-engine invocation -> raw BLK-pipe JSON report -> BLK-test PASS payload -> BEO projection. Do not satisfy this only by passing the same synthetic Python dict through multiple functions.
- Do not claim full RTM generation.
- Do not inspect active BLK-req files; tests must prove no reads of `docs/active/`, `docs/requirements/`, or `docs/use_cases/`.

### TDD RED tests

```python
def test_pass_blk_test_result_projects_to_beo_shape(self): ...
def test_beo_projection_preserves_trace_artifacts_exactly(self): ...
def test_fail_blk_test_result_does_not_project_success_beo(self): ...
def test_beo_projection_marks_rtm_not_generated(self): ...
def test_trace_baton_exact_across_dry_run_loop(self): ...
def test_beo_projection_does_not_read_active_vault(self): ...
```

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_beo_fixture_projection.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
git diff --check
```

### Commit message

```text
feat: draft beo fixture projection
```

---

## 12. Task 8 — Document Hard Live Approval Gate and Close Dry-Run Loop

### Objective

Add operator-facing docs and fixture-builder tests that prevent Sprint 004 fixture code from constructing `codex-live` payloads. This is fixture-level fail-closed enforcement only; it is not a system-wide live approval gate implementation.

### Files

Modify:

- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
- `README.md`
- `python/test_blk_pipe_dry_run_orchestrator.py`

Create outcome:

- `docs/outcomes/BLK-PIPE-004_task-008-outcome.md`

### Required behavior

- Default profile remains one of `dev-smoke`, `strict-ci`, or `codex-dry-run`.
- Any `codex-live` path in Sprint 004 fixture builders must fail closed before payload construction. A future real `codex-live` path must require a hard user approval gate with explicit approval token/phrase and future sandbox/capability decisions.
- Sprint 004 docs must state:
  - no live Codex,
  - no live LLM,
  - no cyber execution,
  - BLK-test is fixture-only,
  - BEO is fixture/draft-only,
  - RTM is not generated.
- Python tests must reject attempts to build a dry-run payload with `codex-live`.

### Deterministic docs gate

```bash
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md'),
    Path('docs/BLK-013_blk-test-handoff-fixture-contract.md'),
    Path('docs/BLK-014_blk-execution-outcome-fixture-shape.md'),
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
    Path('docs/BLK-014_blk-execution-outcome-fixture-shape.md'): [
        'BEO is fixture/draft-only',
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
    Path('python/beo_fixture_projection.py'),
    Path('testdata/engines/codex-dry-run'),
]
for p in fixture_paths:
    if not p.exists():
        continue
    text = p.read_text()
    for token in ['docs/active', 'docs/requirements', 'docs/use_cases', 'fetch_requirements_context']:
        assert token not in text, f'{p}: forbidden active-vault access token {token}'
    # These tokens are forbidden as executable behavior. The literals `codex-live`,
    # `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, and Codex OAuth/session variable names
    # may appear only in explicit rejection/poisoned-env tests or fake-engine
    # fail-closed checks. They must not appear in command construction for a live call.
    forbidden_exec_tokens = ['curl ', 'wget ', 'nc ', 'ssh ', 'https://api.openai.com', 'api.anthropic.com']
    for token in forbidden_exec_tokens:
        assert token not in text, f'{p}: forbidden live-model/network execution token {token}'
    for live_binary_pattern in ['["codex"', "['codex'", ' exec codex', ' codex exec']:
        assert live_binary_pattern not in text, f'{p}: forbidden real codex invocation token {live_binary_pattern}'
PY
```

The static gate intentionally allows literal credential names and `codex-live` inside rejection tests. Future `codex-live` support must be approval-gated and must support both Codex OAuth/session authentication and API-key authentication; Sprint 004 must not require or exercise either live credential path.

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

## 13. Sprint Closeout Requirements

After Tasks 1-8 are complete and pushed, create:

```text
docs/outcomes/BLK-PIPE-004_sprint-closeout.md
```

Closeout must include:

1. Final task-line implementation commit before closeout.
2. Task commits and outcome docs table.
3. BLK-001 alignment summary:
   - BEB/L2 dry-run handoff exercised,
   - BLK-pipe payload/report trace baton preserved,
   - BLK-test fixture PASS/FAIL handoff defined,
   - draft BEO shape created,
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
   - full BEO publication workflow,
   - RTM aggregator implementation,
   - sandbox/capability enforcement beyond docs,
   - hard user approval gate implementation with a real approval channel,
   - Codex live authentication support for both OAuth/session auth and API-key auth,
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
! git grep -n -E 'git.*diff.*\.\.\.' -- '*.go' ':!*_test.go' docs/BLK-009_blk-pipe-sprint-001-cli.md docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md docs/BLK-013_blk-test-handoff-fixture-contract.md docs/BLK-014_blk-execution-outcome-fixture-shape.md docs/plans/BLK-PIPE-004_dry-run-orchestrator-and-blk-test-fixtures.md docs/outcomes/BLK-PIPE-004_task-001-outcome.md docs/outcomes/BLK-PIPE-004_task-002-outcome.md docs/outcomes/BLK-PIPE-004_task-003-outcome.md docs/outcomes/BLK-PIPE-004_task-004-outcome.md docs/outcomes/BLK-PIPE-004_task-005-outcome.md docs/outcomes/BLK-PIPE-004_task-006-outcome.md docs/outcomes/BLK-PIPE-004_task-007-outcome.md docs/outcomes/BLK-PIPE-004_task-008-outcome.md docs/outcomes/BLK-PIPE-004_sprint-closeout.md
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

## 14. Recommended Next Sprint After BLK-PIPE-004

If Sprint 004 closes cleanly, the system should still avoid immediate live autonomy unless explicitly approved. Recommended next seed:

```text
BLK-PIPE-005 — Orchestrator Approval Gate and BLK-test MCP Integration Design
```

Possible scope:

- implement a real hard approval gate for `codex-live`,
- support future live Codex authentication through both OAuth/session auth and API keys,
- wire BLK-test MCP in a disabled-by-default or fixture-first mode,
- define BEO publication workflow,
- define RTM aggregation interface,
- decide sandbox/capability enforcement for live tactical execution.

`codex-live` should remain blocked until that later sprint is explicitly approved and verified.

---

## 15. Quick Resume Prompt

```text
We are in /home/dad/BLK-System. Execute docs/plans/BLK-PIPE-004_dry-run-orchestrator-and-blk-test-fixtures.md using blk-system-sprint-execution. Do not use Hindsight. Do not run live Codex, live tactical LLMs, network model services, cyber tooling, or live BLK-test MCP. Start with Task 1. Use TDD, commit each task, create matching docs/outcomes/BLK-PIPE-004_task-00N-outcome.md, run deterministic review gates, and push only after verification passes.
```
