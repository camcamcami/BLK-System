# BLK-pipe Sprint 003 — Integration Readiness and Capability Profiles Implementation Plan

> **For Hermes:** Use `blk-system-sprint-execution` and subagent-driven-development to implement this plan task-by-task. Each task must use TDD, focused verification, two fresh review gates, an implementation commit, and a matching outcome document.

**Goal:** Harden BLK-pipe from a proven local repository mutation gate into an integration-ready BLK-001 subsystem without enabling live Codex, live tactical LLM execution, or cyber execution.

**Architecture:** BLK-pipe remains a deterministic Go transport and repository blast shield. Sprint 003 closes integration-readiness gaps around BLK-req vault protection, BLK-001 trace/hash baton transport, branch-safe revert, input/runtime bounds, adapter status fidelity, and capability-profile documentation. The sprint does not add autonomous decision-making to BLK-pipe.

**Tech Stack:** Go 1.26.x, POSIX-only BLK-pipe CLI, bounded Git helpers, local Python adapter, Markdown doctrine/outcome documents.

---

## 0. Current Known State

Repository:

```text
/home/dad/BLK-System
```

Current HEAD before this plan:

```text
e48c24e docs: close out blk-pipe sprint 002.2
```

Current verified baseline from the Phase 1/2 review:

```text
go test ./...                                                     PASS
python3 -m unittest discover -s python -p 'test_*.py'             PASS
go vet ./...                                                      PASS
go run ./cmd/blk-pipe --health                                    {"status":"OK","component":"blk-pipe"}
production broad-staging grep                                     PASS
production direct-Git-call grep                                   PASS
triple-dot diff grep across selected code/docs                    PASS
git diff --check                                                  PASS
git status --short --branch                                       ## main...origin/main
```

Phase 1 / Sprint 001 established the deterministic execution kernel. Phase 2 / Sprint 002 hardened toward BLK-004/V47. Sprint 002.2 closed hostile-review gaps around physical residue, escaped timeout/flood descendants, validation-authored diffs, validation safety precedence, and `l2_packet` stdin delivery.

Sprint 003 should be treated as **integration readiness**, not as live tactical execution.

---

## 1. Non-Goals

Sprint 003 must not implement or run:

- live Codex invocation,
- live tactical LLM API calls,
- OpenAI/local model orchestration,
- Discord HITL workflows,
- BLK-test MCP execution,
- CEO generation,
- RTM aggregation,
- offensive cyber activity,
- execution against real cyber-program repositories,
- full container/VM/cgroup/network sandboxing,
- general host-secret isolation.

Sprint 003 may define capability-profile contracts and documentation, but live `codex-live` or `cyber-execution` use remains blocked until a later explicitly approved sprint.

---

## 2. Non-Negotiable Invariants To Preserve

Every implementation task must preserve:

1. No production `git add .` or `git add -u`.
2. Stage only explicit allowlisted file paths via `git add -- <file>`.
3. Reject path traversal, Git pathspec/glob widening, absolute allowlist paths, directories, and protected BLK-req vault paths.
4. Clean preflight rejects pre-existing tracked, untracked, ignored, nested-Git, and empty-directory residue before destructive execute/revert behavior.
5. Engine and validation output remain bounded.
6. `l2_packet` remains bounded, delivered to engine stdin, and not echoed into error/report fields by default.
7. Validation remains a read-only gate over the post-engine candidate state.
8. `.git` mutation remains unauthorized and blocks validation/commit as appropriate.
9. Fatal signal/panic paths emit one sterile JSON fatal report and exit `1`.
10. Revert never uses relative anchors such as `HEAD~1`.
11. Diff extraction uses `git diff <Hash> HEAD --`, never triple-dot diff.
12. BLK-pipe remains a deterministic transport and safety layer, not an LLM caller or architecture decision-maker.

---

## 3. Standard Controller Workflow For Each Task

For each task below:

1. Preflight:

   ```bash
   cd /home/dad/BLK-System
   export PATH="$HOME/.local/bin:$PATH"
   git status --short --branch
   ```

2. Dispatch an implementation subagent with the exact task section.
3. Require RED evidence before implementation.
4. Require GREEN focused tests and full relevant tests.
5. Require:

   ```bash
   gofmt -w <changed-go-files>
   go test ./...
   go vet ./...
   git diff --check
   ```

6. Run two fresh review gates:
   - spec compliance against this plan and BLK-001/BLK-004,
   - code quality/security/scope review.
7. Patch/amend until both reviews pass.
8. Commit the task with the listed commit message.
9. Create and commit the matching outcome document.
10. Push only after the controller verifies the final state.

Outcome documents for this sprint:

```text
docs/outcomes/BLK-PIPE-003_task-001-outcome.md
docs/outcomes/BLK-PIPE-003_task-002-outcome.md
docs/outcomes/BLK-PIPE-003_task-003-outcome.md
docs/outcomes/BLK-PIPE-003_task-004-outcome.md
docs/outcomes/BLK-PIPE-003_task-005-outcome.md
docs/outcomes/BLK-PIPE-003_task-006-outcome.md
docs/outcomes/BLK-PIPE-003_sprint-closeout.md
```

---

## 4. Task 1 — Freeze and Enforce Protected BLK-req Vault Paths

### Objective

Resolve the BLK-001 `/docs/active/` ambiguity defensively by extending BLK-pipe allowlist denial to every active BLK-req vault candidate until the doctrine path convention is formally frozen.

### Rationale

BLK-001 names `/docs/active/` as the immutable active vault. Existing BLK-pipe validation rejects `docs/requirements/` and `docs/use_cases/`, which protects type-specific vault layouts. Sprint 003 should also reject `docs/active/` so no tactical payload can mutate a shared active vault if that doctrine path is used.

### Files

Modify:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/pipe/run_test.go`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-003_task-001-outcome.md`

### Required behavior

Allowlist validation rejects any entry with these prefixes:

```text
docs/active/
docs/requirements/
docs/use_cases/
```

The rejection must happen before engine execution.

### TDD RED tests

Add or extend table coverage in `internal/contracts/payload_test.go`:

```go
{
    name: "protected shared active vault modified",
    mutate: func(p *Payload) {
        p.AllowedModifiedFiles = []string{"docs/active/REQ-001.md"}
    },
    want: "protected docs/active path",
},
{
    name: "protected shared active vault new",
    mutate: func(p *Payload) {
        p.AllowedNewFiles = []string{"docs/active/UC-001.md"}
    },
    want: "protected docs/active path",
},
```

Add a pipe-level regression in `internal/pipe/run_test.go`:

```go
func TestRunRejectsDocsActiveAllowlistBeforeEngine(t *testing.T) {
    repo := testutil.NewGitRepo(t)
    marker := filepath.Join(repo, "engine-ran")
    payload := payloadJSON(t, contracts.Payload{
        Action:               "execute",
        Workdir:              repo,
        EngineCommand:        []string{"sh", "-c", "touch engine-ran"},
        AllowedModifiedFiles: []string{"docs/active/REQ-001.md"},
        TimeoutSeconds:       5,
        MaxOutputBytes:       4096,
    })

    var stdout bytes.Buffer
    exitCode := Run(context.Background(), payload, &stdout)
    report := decodeReport(t, stdout.Bytes())

    if exitCode != ExitInvalidPayload {
        t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitInvalidPayload, report)
    }
    if report.Status != "INVALID_PAYLOAD" {
        t.Fatalf("status = %q, want INVALID_PAYLOAD", report.Status)
    }
    if !strings.Contains(report.Error, "docs/active") {
        t.Fatalf("error = %q, want docs/active", report.Error)
    }
    if _, err := os.Stat(marker); !os.IsNotExist(err) {
        t.Fatalf("engine marker exists or unexpected stat error: %v", err)
    }
    assertClean(t, repo)
}
```

Expected RED:

```text
TestPayload...docs/active... FAIL
TestRunRejectsDocsActiveAllowlistBeforeEngine FAIL
```

### Implementation guidance

Update `isProtectedDocsPath` and `protectedDocsPrefix` in `internal/contracts/payload.go` to include `docs/active/`.

Do not broaden denial to all `docs/` paths. BLK-pipe docs, plans, and outcomes are legitimate future allowlist targets for documentation-only work. Only active BLK-req vault candidates are protected here.

### Focused verification

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/contracts -run 'TestPayload.*Protected|TestPayload.*Invalid|TestPayloadDecode' -v
go test ./internal/pipe -run 'TestRunRejectsDocsActive|TestRunProtected|TestRun.*InvalidPayload' -v
go test ./...
go vet ./...
git diff --check
```

### Review gate focus

Reviewers must check that:

- `docs/active/` is rejected in both modified and new allowlists,
- engine execution is not reached for protected paths,
- legitimate documentation paths outside active BLK-req vaults are not accidentally blocked,
- docs explain the defensive path-convention stance.

### Commit message

```text
fix: protect shared blk-req active vault paths
```

---

## 5. Task 2 — Add Opaque Trace Artifact Hash Baton Fields

### Objective

Add a bounded, opaque trace-artifact contract so BLK-pipe can carry BLK-001 canonical hash baton metadata from CEB/L2 input through execution reports without interpreting architecture semantics.

### Rationale

BLK-001 relies on an unbroken `version_hash` chain. BLK-pipe should not validate requirements or generate RTMs, but it should preserve enough metadata for later CEO/RTM linkage without relying on Hermes or Codex memory.

### Files

Modify:

- `internal/contracts/payload.go`
- `internal/contracts/report.go`
- `internal/contracts/payload_test.go`
- `internal/contracts/report_test.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- `python/blk_pipe_adapter.py`
- `python/test_blk_pipe_adapter.py`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-003_task-002-outcome.md`

### Target payload/report shape

Add a field named `trace_artifacts`:

```json
{
  "trace_artifacts": [
    {
      "kind": "REQ",
      "id": "REQ-042",
      "version_hash": "sha256:0123456789abcdef..."
    },
    {
      "kind": "UC",
      "id": "UC-007",
      "version_hash": "sha256:abcdef0123456789..."
    }
  ]
}
```

Recommended Go type:

```go
type TraceArtifact struct {
    Kind        string `json:"kind"`
    ID          string `json:"id"`
    VersionHash string `json:"version_hash"`
}
```

Add to `Payload` and `Report`:

```go
TraceArtifacts []TraceArtifact `json:"trace_artifacts"`
```

Add the same field to the Python adapter integration surface:

```python
@dataclass
class ExecutionResult:
    trace_artifacts: list[dict[str, str]] | None = None

class BlkPipeAdapter:
    def execute_sprint(
        ...,
        trace_artifacts: list[dict[str, str]] | None = None,
    ) -> ExecutionResult:
        ...
```

The adapter must include `trace_artifacts` in the JSON payload when provided, default missing values to `[]`, and preserve parsed report `trace_artifacts` without interpreting them.

### Validation requirements

Keep validation lightweight and transport-focused:

- `trace_artifacts` may be empty.
- Max trace artifacts: `64`.
- `kind`, `id`, and `version_hash` must be non-empty when an artifact is present.
- Max length per string: `256` bytes.
- `version_hash` must start with `sha256:`.
- Do not parse requirement/use-case bodies.
- Do not verify hashes against files in this task.
- Do not echo oversized/invalid long values in errors.

### TDD RED tests

In `internal/contracts/payload_test.go`:

```go
func TestPayloadDecodePreservesTraceArtifacts(t *testing.T) { ... }
func TestPayloadDecodeRejectsTooManyTraceArtifacts(t *testing.T) { ... }
func TestPayloadDecodeRejectsTraceArtifactMissingFields(t *testing.T) { ... }
func TestPayloadDecodeRejectsTraceArtifactWithoutSHA256Prefix(t *testing.T) { ... }
func TestPayloadDecodeTraceArtifactErrorDoesNotEchoLongHash(t *testing.T) { ... }
```

In `internal/contracts/report_test.go`:

```go
func TestReportMarshalEmitsTraceArtifactsAsStableEmptyList(t *testing.T) { ... }
func TestReportMarshalPreservesTraceArtifacts(t *testing.T) { ... }
```

In `internal/pipe/run_test.go`:

```go
func TestRunSuccessReportsTraceArtifacts(t *testing.T) { ... }
func TestRunInvalidPayloadReportsTraceArtifactsWhenDecodedBeforeValidationFailure(t *testing.T) { ... }
```

In `python/test_blk_pipe_adapter.py`:

```python
def test_execute_sprint_payload_includes_trace_artifacts(self): ...
def test_execution_result_preserves_trace_artifacts(self): ...
def test_execution_result_defaults_missing_trace_artifacts_to_empty_list(self): ...
```

Expected RED:

```text
unknown field TraceArtifacts / missing trace_artifacts report field
```

### Implementation guidance

- Add `TraceArtifacts` to `payloadWire`, `Payload`, and `Report`.
- Initialize `Report.TraceArtifacts` to `[]TraceArtifact{}` in `NewReport` and `MarshalJSON`.
- In `parseAndValidatePayload`, copy decoded trace artifacts into the report before returning validation errors where possible.
- Extend `python/blk_pipe_adapter.py` so `execute_sprint` accepts optional `trace_artifacts`, writes them into the payload JSON, and maps parsed report `trace_artifacts` back onto `ExecutionResult`.
- Preserve adapter backward compatibility: existing callers that omit `trace_artifacts` must still work.
- Keep trace artifacts opaque. This is transport, not RTM verification.

### Focused verification

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/contracts -run 'TestPayload.*Trace|TestReport.*Trace' -v
go test ./internal/pipe -run 'TestRun.*Trace' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

### Review gate focus

Reviewers must check that:

- the field is stable JSON and defaults to `[]`, not `null`,
- invalid long values are not leaked in full,
- BLK-pipe remains opaque and does not become an RTM/verifier,
- invalid payload reports preserve useful trace context when safely decoded,
- the Python adapter does not drop trace artifacts at the integration boundary,
- adapter changes remain backward-compatible for existing callers.

### Commit message

```text
feat: carry blk-pipe trace artifact hashes
```

---

## 6. Task 3 — Make Revert Branch-Safe

### Objective

Prevent `action: "revert"` from resetting the wrong clean branch when `target_branch` is provided.

### Rationale

V47 revert payloads and the Python adapter carry `target_branch`. Current revert logic validates target hash and ancestry relative to current `HEAD`, then resets the currently checked-out branch. Before autonomous orchestration, branch intent must be enforced mechanically.

### Files

Modify:

- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `python/blk_pipe_adapter.py` only if adapter docs or behavior need wording updates
- `python/test_blk_pipe_adapter.py` only if adapter status expectations change

Create outcome:

- `docs/outcomes/BLK-PIPE-003_task-003-outcome.md`

### Required behavior

If `payload.Action == "revert"` and `payload.TargetBranch != ""`:

1. The repository must already be clean from preflight.
2. BLK-pipe must verify the currently checked-out branch equals `payload.TargetBranch` before reset.
3. If it does not match, BLK-pipe must return:

   ```text
   status: INVALID_REVERT_ANCHOR
   exit: 4
   no reset
   clean repo preserved
   ```

This sprint should **not** make revert run full execute-path branch preparation. That can be a later design if needed. The safe minimum is to refuse wrong-branch reset.

### TDD RED tests

Add in `internal/pipe/run_test.go`:

```go
func TestRunRevertWithTargetBranchRejectsWrongCurrentBranch(t *testing.T) { ... }
func TestRunRevertWithTargetBranchAcceptsMatchingCurrentBranch(t *testing.T) { ... }
func TestRunRevertWithoutTargetBranchPreservesLegacyCurrentBranchBehavior(t *testing.T) { ... }
```

Test shape for wrong branch:

1. Create repo.
2. Create branch `sprint/right` with two commits.
3. Capture first commit hash.
4. Checkout `main` or `sprint/wrong` where the target hash is also reachable if needed.
5. Invoke revert with `target_branch: "sprint/right"`.
6. Assert exit `4`, status `INVALID_REVERT_ANCHOR`, HEAD unchanged, repo clean.

### Implementation guidance

Add helper:

```go
func currentBranch(repo string) (string, error) {
    out, err := runGit(repo, "rev-parse", "--abbrev-ref", "HEAD")
    if err != nil {
        return "", err
    }
    branch := strings.TrimSpace(string(out))
    if branch == "HEAD" {
        return "", fmt.Errorf("repository is in detached HEAD; target_branch %q cannot be verified", targetBranch)
    }
    return branch, nil
}
```

Use a signature that passes `targetBranch` if needed for the error message.

In `runRevert`, perform branch verification before `verifyRevertTargetCommit` and `verifyRevertAncestry` when `TargetBranch` is non-empty.

Do not call engine, validation, staging, branch fetch, or commit.

### Focused verification

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestRunRevert.*Branch|TestRunRevert' -v
go test ./...
go vet ./...
git diff --check
```

### Review gate focus

Reviewers must check that:

- wrong branch cannot be reset,
- matching branch still succeeds,
- empty `target_branch` preserves current documented behavior,
- dirty preflight still happens before destructive revert,
- revert remains a fast path and does not run engine/validation/staging.

### Commit message

```text
fix: require matching branch for blk-pipe revert
```

---

## 7. Task 4 — Bound Payload Ingestion and Validation Work

### Objective

Add deterministic upper bounds before payload JSON is fully read, and bound validation command count/size/global runtime so payloads cannot multiply work unboundedly.

### Files

Modify:

- `cmd/blk-pipe/main.go`
- `cmd/blk-pipe/main_test.go`
- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/validation/validation.go`
- `internal/validation/validation_test.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-003_task-004-outcome.md`

### Required behavior

Add constants:

```go
const DefaultMaxPayloadJSONBytes = 2 * 1024 * 1024
const DefaultMaxValidationCommands = 16
const DefaultMaxValidationCommandBytes = 4096
```

Exact constant location is implementer’s choice, but prefer `internal/contracts` for payload-facing validation constants and a CLI helper for read limits.

Payload file/stdin behavior:

- `--payload /absolute/path` rejects files larger than `DefaultMaxPayloadJSONBytes` before reading all bytes where possible.
- `--payload-stdin` reads at most `DefaultMaxPayloadJSONBytes + 1` and rejects oversized input.
- Oversized payload input returns `ExitInvalidPayload` (`2`).
- Error must not echo payload body.

Validation behavior:

- Reject more than `DefaultMaxValidationCommands` during payload validation.
- Reject any validation command whose byte length exceeds `DefaultMaxValidationCommandBytes`.
- Add an overall validation context deadline so many commands cannot each consume a full independent timeout without a sprint-level cap.

Recommended first implementation:

```text
overall validation deadline = payload.TimeoutSeconds
```

This means the whole validation phase, not each command independently, is bounded by the payload timeout. If this breaks intended workflows, document the decision and propose a future separate field.

### TDD RED tests

In `cmd/blk-pipe/main_test.go`:

```go
func TestPayloadFileRejectsOversizedPayloadBeforePipeRun(t *testing.T) { ... }
func TestPayloadStdinRejectsOversizedPayload(t *testing.T) { ... }
```

In `internal/contracts/payload_test.go`:

```go
func TestPayloadValidateRejectsTooManyValidationCommands(t *testing.T) { ... }
func TestPayloadValidateRejectsValidationCommandTooLong(t *testing.T) { ... }
```

In `internal/validation/validation_test.go` or `internal/pipe/run_test.go`:

```go
func TestValidationRunUsesOverallDeadline(t *testing.T) { ... }
```

The deadline test should use very small timeouts and deterministic shell commands. Avoid long sleeps.

### Implementation guidance

- For stdin, use a limited reader helper rather than `io.ReadAll(stdin)` directly.
- For file mode, use `os.Stat` when available to reject obviously oversized regular files before read, then still use a limited reader to avoid races or special-file surprises.
- Keep unsupported invocation behavior unchanged.
- Do not add a new exit code.
- Do not log payload body.

### Focused verification

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./cmd/blk-pipe -run 'TestPayload.*Oversized|TestRunPayload' -v
go test ./internal/contracts -run 'TestPayload.*ValidationCommand|TestPayload.*TooMany' -v
go test ./internal/validation -v
go test ./internal/pipe -run 'Test.*Validation' -v
go test ./...
go vet ./...
git diff --check
```

### Review gate focus

Reviewers must check that:

- oversized payloads are rejected before unbounded memory use,
- validation count and command length are bounded,
- validation total runtime is bounded,
- errors do not echo payload or long command bodies,
- existing valid payloads still pass.

### Commit message

```text
fix: bound blk-pipe payload and validation work
```

---

## 8. Task 5 — Preserve Adapter Status Fidelity

### Objective

Make the Python adapter preserve parsed Go report status where it is more specific than the exit-code family, especially `INVALID_PAYLOAD` vs `SYNTAX_GATE_FAILED` under exit code `2`.

### Files

Modify:

- `python/blk_pipe_adapter.py`
- `python/test_blk_pipe_adapter.py`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-003_task-005-outcome.md`

### Required behavior

The adapter should use return code as the routing family, but preserve report status when it is known and compatible.

Expected mapping examples:

```text
return 0 + report SUCCESS                         -> SUCCESS
return 2 + report INVALID_PAYLOAD                 -> INVALID_PAYLOAD
return 2 + report SYNTAX_GATE_FAILED              -> SYNTAX_GATE_FAILED
return 3 + report UNAUTHORIZED_FILE_MUTATION      -> UNAUTHORIZED_FILE_MUTATION
return 9 + report INTERNAL_ERROR                  -> INTERNAL_ERROR
unknown nonzero + report SUCCESS                  -> INTERNAL_ERROR
non-JSON stdout                                   -> FATAL_CRASH
```

### TDD RED tests

Add in `python/test_blk_pipe_adapter.py`:

```python
def test_invalid_payload_status_preserved_for_exit_code_2(self): ...
def test_validation_failure_status_preserved_for_exit_code_2(self): ...
def test_success_status_not_trusted_for_nonzero_unknown_exit(self): ...
```

If existing tests already cover unknown nonzero success suppression, preserve them and add the missing status-preservation cases.

### Implementation guidance

Create an allowed-status family map:

```python
_ALLOWED_STATUSES_BY_CODE = {
    1: {"FATAL_SYSTEM_PANIC", "FATAL_ENGINE_FAILED"},
    2: {"INVALID_PAYLOAD", "SYNTAX_GATE_FAILED"},
    3: {"UNAUTHORIZED_FILE_MUTATION"},
    4: {"INVALID_REVERT_ANCHOR"},
    5: {"FATAL_OUTPUT_FLOOD"},
    6: {"ENGINE_TIMEOUT"},
    7: {"GIT_DIRTY"},
    9: {"INTERNAL_ERROR"},
}
```

If `parsed_output["status"]` belongs to the family for the return code, preserve it. Otherwise use the family default. For unknown nonzero return codes, force `INTERNAL_ERROR` even if parsed output says `SUCCESS`.

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
git diff --check
```

### Review gate focus

Reviewers must check that:

- invalid payload and validation failure are distinguishable,
- nonzero exits cannot report success,
- temp payload cleanup behavior remains unchanged,
- adapter still uses no shell.

### Commit message

```text
fix: preserve blk-pipe adapter status detail
```

---

## 9. Task 6 — Document Integration Readiness and Capability Profiles

### Objective

Create an operator-facing doctrine document that defines Sprint 003 readiness boundaries, capability profiles, and explicit blocks before live Codex/cyber execution.

### Files

Create:

- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md`

Modify:

- `README.md`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-003_task-006-outcome.md`

### Required document content

The new document must define these profiles:

```text
dev-smoke       local fake-engine / deterministic local command work only
strict-ci       ephemeral clean clone/worktree, minimal non-secret environment, no live secrets
codex-dry-run   fake/dry-run parity fixtures for Codex command shape, no live model call
codex-live      future blocked profile requiring explicit user approval and sandbox/capability decisions
cyber-execution future blocked profile requiring separate sandbox/secret/network/process controls
```

The document must state:

- Sprint 003 does not run Codex.
- Sprint 003 does not authorize live LLM execution.
- Sprint 003 does not authorize cyber execution.
- BLK-pipe is not a full sandbox.
- BLK-pipe is not general host-secret isolation.
- `codex-live` and `cyber-execution` remain blocked until explicitly approved in a future sprint.

The document must also summarize which Sprint 003 fixes improve integration readiness:

- protected vault path coverage,
- trace artifact hash baton transport,
- branch-safe revert,
- payload/validation bounds,
- adapter status fidelity.

### Documentation validation RED/GREEN

Before writing `docs/BLK-012...`, run a small validation snippet that fails because the file does not exist and required phrases are absent. Record that as RED evidence in the outcome doc.

After writing docs, validate:

```bash
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md'),
    Path('docs/BLK-010_blk-pipe-v47-hardening-cli.md'),
    Path('docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md'),
    Path('README.md'),
]
required = [
    'Sprint 003 does not run Codex',
    'BLK-pipe is not a full sandbox',
    'codex-live',
    'cyber-execution',
]
fence = chr(96) * 3
for p in paths:
    text = p.read_text()
    assert text.endswith('\n'), f'{p}: missing final newline'
    assert text.count(fence) % 2 == 0, f'{p}: unbalanced fences'
    for i, line in enumerate(text.splitlines(), 1):
        assert line.rstrip() == line, f'{p}:{i}: trailing whitespace'
main = paths[0].read_text()
for phrase in required:
    assert phrase in main, f'missing phrase: {phrase}'
PY
```

### Focused verification

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./...
python3 -m unittest discover -s python -p 'test_*.py'
go vet ./...
git diff --check
```

### Review gate focus

Reviewers must check that:

- profile language does not imply live Codex approval,
- cyber-execution remains blocked,
- host-secret and sandbox limitations are explicit,
- links from README and existing docs are correct,
- docs do not introduce unsafe commands such as broad Git staging, stash use, relative revert anchors, or triple-dot diffs.

### Commit message

```text
docs: define blk-pipe integration readiness profiles
```

---

## 10. Sprint Closeout Requirements

After Tasks 1-6 are complete and pushed, create:

```text
docs/outcomes/BLK-PIPE-003_sprint-closeout.md
```

Closeout must include:

1. Final task-line commit before closeout.
2. Task commits and outcome docs table.
3. Summary of BLK-001 alignment improvements.
4. Explicit statement that Sprint 003 did not run Codex/live LLM/cyber execution.
5. Remaining blocked scope before live Codex:
   - sandbox/capability enforcement beyond docs,
   - BLK-test MCP integration,
   - CEO generation,
   - RTM aggregation,
   - live orchestrator approval gate.
6. Verification evidence.
7. Recommended next sprint seed scope.

Final closeout verification:

```bash
set -e
export PATH="$HOME/.local/bin:$PATH"
go test ./...
python3 -m unittest discover -s python -p 'test_*.py'
go vet ./...
go run ./cmd/blk-pipe --health
! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go'
! git grep -n -E 'exec\.Command(Context)?\("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
! git grep -n -E 'git[^\n]*diff[^\n]*\.\.\.' -- '*.go' ':!*_test.go' docs/BLK-009_blk-pipe-sprint-001-cli.md docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md docs/plans/BLK-PIPE-003_integration-readiness-and-capability-profiles.md docs/outcomes/BLK-PIPE-003_task-001-outcome.md docs/outcomes/BLK-PIPE-003_task-002-outcome.md docs/outcomes/BLK-PIPE-003_task-003-outcome.md docs/outcomes/BLK-PIPE-003_task-004-outcome.md docs/outcomes/BLK-PIPE-003_task-005-outcome.md docs/outcomes/BLK-PIPE-003_task-006-outcome.md docs/outcomes/BLK-PIPE-003_sprint-closeout.md
git diff --check
git status --short --branch
```

If Python tests create `python/__pycache__/`, remove it before committing docs:

```bash
rm -rf python/__pycache__
```

---

## 11. Recommended Next Sprint After BLK-PIPE-003

If Sprint 003 closes cleanly, the next sprint should still avoid immediate live autonomy unless explicitly approved.

Recommended next sprint seed:

```text
BLK-PIPE-004 — Dry-Run Orchestrator and BLK-test Handoff Fixtures
```

Possible scope:

- fake Codex command-shape fixtures,
- CEB/L2 packet construction fixtures,
- trace-artifact propagation into a draft CEO shape,
- BLK-test handoff contract fixtures,
- explicit user approval gate before any `codex-live` profile can run,
- no live LLM call unless separately approved.

---

## 12. Quick Resume Prompt

Use this prompt to resume execution later:

```text
We are in /home/dad/BLK-System. Execute docs/plans/BLK-PIPE-003_integration-readiness-and-capability-profiles.md using blk-system-sprint-execution. Do not use Hindsight. Do not run live Codex, live LLMs, or cyber tooling. Start with Task 1. Use TDD, commit each task, create the matching docs/outcomes/BLK-PIPE-003_task-00N-outcome.md, run two review gates per task, and push only after verification passes.
```
