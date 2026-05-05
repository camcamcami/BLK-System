# BLK-pipe Sprint 008 — BLK-004 Unsafe Gap Closure and Decision Register

> **For Hermes:** Use `blk-system-sprint-execution` to implement this plan task-by-task. This sprint is deterministic local remediation only. Do not use Hindsight. Do not run live Codex, live tactical LLMs, network model services, cyber tooling, live BLK-test MCP, RTM generation, RTM authority, or authoritative BEO publication.

**Goal:** Close the unsafe BLK-004 deviation gaps found by the hostile deviation review, and explicitly document the policy decisions behind every remaining BLK-004/current-state difference.

**Architecture:** Sprint 008 tightens the deterministic BLK-pipe/BLK-test fixture boundary. It makes governed `execute` payloads trace-bound, makes BLK-test handoffs reject malformed trace batons, enforces tracked-vs-new allowlist semantics, moves the no-candidate-diff gate before validation commands, and adds a BLK-004/BLK-010 current-state overlay for accepted hardening and compatibility differences.

**Tech Stack:** Go 1.26.x, POSIX-only BLK-pipe CLI, dependency-free Python fixture/adapter modules, deterministic Go/Python tests, Markdown doctrine/outcome documents.

---

## 0. Current Known State

Repository:

```text
/home/dad/BLK-System
```

Planning preflight when this document was authored:

```text
date                         -> 2026-05-05 18:57:58 AEST
git status --short --branch  -> ## main...origin/main
                               ?? docs/reviews/BLK-004_hostile-deviation-review.md
HEAD                         -> 202ce3e docs: record BLK-pipe sprint 007 task 5 outcome
```

Primary source review artifact:

```text
docs/reviews/BLK-004_hostile-deviation-review.md
```

Important state note: the BLK-004 hostile deviation review document was untracked when this plan was authored. If it remains untracked at sprint start, include it in the sprint branch or commit it with this plan before implementation closeout so the remediation source is preserved in repository history.

---

## 1. Hostile Review Findings Driving This Sprint

Sprint 008 is driven by the unsafe/non-clean items from `docs/reviews/BLK-004_hostile-deviation-review.md`:

| Review ID | Finding | Sprint 008 disposition |
| --- | --- | --- |
| D-001 | Successful BLK-pipe `execute` can still produce `trace_artifacts: []`. | Task 1: enforce non-empty canonical trace artifacts for governed execute payloads. |
| D-002 | BLK-test PASS/FAIL handoff fixture accepts noncanonical trace hashes. | Task 2: add canonical trace validation to handoff fixture path. |
| D-003 | `allowed_new_files` can authorize modification of a tracked file. | Task 3: enforce strict tracked/new allowlist semantics. |
| D-004 | Zero-diff/no-candidate gate runs after validation rather than before. | Task 4: move no-candidate gate before validation commands. |
| D-005 | Health JSON differs from BLK-004 literal `healthy` example. | Task 5: accept current local output and document compatibility overlay. |
| D-006 | BLK-004 examples/source segment lack later trace/current-disabled overlays. | Task 5: add BLK-004 current-state overlay and safe examples. |
| D-007 | Local extension exit codes 6/7/9 extend BLK-004 strict 0-5 router. | Task 5: document as accepted local compatibility extension. |
| D-008 | Cleanup uses stronger `git clean -ffdx -q`, not literal `git clean -fd`. | Task 5: document as accepted hardening and ignored-file deletion behavior. |
| D-009 | Legacy payload/report fields extend BLK-004 schema. | Task 5: document as accepted compatibility/evidence extension. |

This sprint must not treat any item as “BLK-004 missed something.” BLK-004 is intentional authority. Every difference must be closed by code, explicit acceptance, or documented doctrine evolution.

---

## 2. Decision Register and Recommendations

These are the decisions that need to be made before or during Sprint 008. The plan author recommends the decisions below. If the BLK owner disagrees with any recommendation, amend this plan before implementation rather than silently implementing the opposite policy.

| Decision ID | Question | Recommendation | Rationale | Implementation effect |
| --- | --- | --- | --- | --- |
| DEC-001 | Should successful governed `execute` payloads be allowed with `trace_artifacts: []`? | **No. Require non-empty canonical `trace_artifacts` for `action: "execute"`.** Exempt only `revert`, `--health`, and invalid-payload reports that fail before a valid trace can be decoded. | BLK-001 traceability and BLK-004 V47 trace-baton intent are more important than preserving trace-empty smoke paths. Dev-smoke tests can use deterministic synthetic trace artifacts rather than empty traces. | Add Go payload validation and run-level regression tests. Update all execute test fixtures to supply canonical traces. Update BLK-010 and BLK-004 overlay. |
| DEC-002 | Should BLK-test handoff fixtures validate canonical hashes or preserve whatever source report carries? | **Validate canonical hash syntax in handoff fixtures.** PASS/FAIL require non-empty canonical traces. BLOCKED validates any supplied trace entries; if trace is absent because the source failed before decode, preserve `[]` with explicit absence reason. | PASS/FAIL-shaped data must never carry malformed trace evidence. BLOCKED can record source failure, but must not launder malformed trace metadata into later BEO/RTM fixture paths. | Patch `python/blk_test_handoff_fixtures.py` and tests. Consider a small shared helper only if it reduces duplication without broad refactor. |
| DEC-003 | Are `allowed_modified_files` and `allowed_new_files` a combined path boundary, or strict tracked/new authorization classes? | **Use strict tracked/new semantics.** `allowed_modified_files` must be tracked before engine execution. `allowed_new_files` must be untracked/nonexistent before engine execution. Reject overlap. | BLK-004 intentionally names two allowlists. Strict semantics close an authorization footgun and make sprint wording (“true new file”) match physical behavior. | Add repo-state precheck after branch/workspace prep and before engine. Wrong-class paths fail closed without running the engine. Update BLK-010. |
| DEC-004 | Should BLK-pipe run validation commands when the engine produced no candidate diff? | **No. Move the no-candidate/zero-diff gate before validation.** Keep the current `UNAUTHORIZED_FILE_MUTATION` status/exit family for no candidate diff unless a future compatibility sprint reopens exit-code mapping. | Validation commands are intended to validate an engine candidate, not create or discover one. Running them with no candidate expands side-effect surface. | Add pre-validation no-candidate gate after engine residue checks. Assert `validation_logs == {}` on no-candidate failure. |
| DEC-005 | Should health output be changed to BLK-004 literal `{"status":"healthy"}`? | **Do not change current CLI output in this sprint.** Accept `{"status":"OK","component":"blk-pipe"}` as the BLK-System local health contract and document the BLK-004 literal as superseded/qualified by current local contract. | Current output is consistently documented/tested in BLK-010 and outcomes. Changing it risks breaking local callers for low safety gain. | Documentation-only. If external V47 exact compatibility is needed later, add adapter normalization or compatibility mode in a separate sprint. |
| DEC-006 | Should BLK-004 source segments/examples be rewritten wholesale? | **No wholesale rewrite. Add a current-state overlay/appendix and corrected current examples.** | BLK-004 source segments were intentional and historically meaningful. Overlay preserves intent while preventing unsafe copy-paste of old examples. | Patch BLK-004 near the top and add an appendix with Sprint 008 current-state clauses. |
| DEC-007 | Should local extension exit codes 6/7/9 be collapsed into BLK-004 0-5 now? | **No. Accept as local V47-compatible extensions.** | They improve status fidelity and have existing documentation. Collapse only if a future external compatibility requirement appears. | Documentation-only. |
| DEC-008 | Should stronger `git clean -ffdx -q` be reverted to BLK-004 literal `git clean -fd`? | **No. Accept stronger cleanup as hardening.** | It better supports BLK-004’s safety intent by removing ignored-file residue, but operators must know ignored files can be deleted. | Documentation-only. |
| DEC-009 | Should legacy payload fields and extra report fields be removed? | **No. Accept as migration/evidence extensions.** | They preserve local compatibility and improve auditability without weakening deterministic transport. | Documentation-only. |

Recommended default if executing this plan: adopt DEC-001 through DEC-009 exactly as listed.

---

## 3. Non-Goals and Hard Blocks

Sprint 008 must not implement, invoke, or imply:

- live Codex invocation;
- live tactical LLM API calls;
- network model services;
- `codex-live` runtime execution;
- cyber tooling or cyber execution;
- execution against real cyber-program repositories or live targets;
- live BLK-test MCP calls;
- live MCP client transport;
- authoritative BLK-test verdict authority;
- authoritative BEO publication;
- complete RTM generation as a traceability ledger;
- RTM drift rejection authority;
- full sandbox/container/cgroup/VM enforcement;
- production host-secret isolation claims;
- production approval-channel mechanics;
- active BLK-req vault reads or requirement-body parsing.

Allowed work:

```text
deterministic local tests
fixture-only execution
BLK-pipe payload validation hardening
BLK-pipe staging/validation sequencing hardening
BLK-test handoff fixture validation hardening
BLK-004/BLK-010 current-state documentation overlay
outcome documents and hostile closeout evidence
```

---

## 4. Invariants to Preserve

1. BLK-pipe remains a deterministic transport/mutation gate, not an architect, requirement parser, live LLM caller, BLK-test authority, BEO publisher, RTM generator, or sandbox.
2. BLK-pipe may validate trace metadata shape and presence, but must not read requirement/use-case bodies or verify hashes against files.
3. Governed `execute` payloads must carry non-empty canonical `trace_artifacts` after this sprint.
4. The canonical trace artifact shape remains:

   ```yaml
   trace_artifacts:
     - kind: "REQ"
       id: "REQ-042"
       version_hash: "sha256:<64-lowercase-hex>"
   ```

5. BLK-test PASS/FAIL-shaped fixture data must never exist with missing, empty, or malformed trace artifacts.
6. `allowed_modified_files` and `allowed_new_files` are strict authorization classes after this sprint, not only a combined path boundary.
7. The engine must produce a candidate mutation before validation commands run.
8. Validation commands remain local, bounded, sequential, and check-oriented; they do not become tactical decision makers.
9. Protected BLK-req vault paths remain denied: `docs/active/`, `docs/requirements/`, and `docs/use_cases/`.
10. New BLK-System plans and active docs use BLK-native BEB/BEO terminology and `beb_id`, not legacy execution-brief/outcome vocabulary.
11. No production `git add .`, `git add -u`, `git stash`, relative revert anchors, or triple-dot report diffs.
12. Do not broaden this sprint into live approval-channel mechanics or full sandbox/capability enforcement.

---

## 5. Controller Workflow for Each Task

For each task:

1. Preflight:

   ```bash
   cd /home/dad/BLK-System
   export PATH="$HOME/.local/bin:$PATH"
   git status --short --branch
   ```

2. Use strict TDD for code changes: write a failing test/probe first, capture RED, implement minimal code, capture GREEN.
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
   docs/outcomes/BLK-PIPE-008_task-00N-outcome.md
   ```

7. Use the sprint closeout document as Task 6 outcome:

   ```text
   docs/outcomes/BLK-PIPE-008_sprint-closeout.md
   ```

8. Commit each task after verification with the listed commit message.
9. Push only after verification passes and `git status --short --branch` is clean/aligned.

---

## 6. Task 1 — Enforce Non-Empty Canonical Trace Artifacts for Execute Payloads

### Objective

Close D-001 by preventing successful governed `execute` payloads from reaching the engine without a non-empty canonical trace baton.

### Files

Modify:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/pipe/run_test.go`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-008_task-001-outcome.md`

### Required behavior

- `action: "execute"` requires `len(trace_artifacts) >= 1`.
- Each supplied trace artifact still uses existing canonical validation:
  - `kind` non-empty, <= 256 bytes;
  - `id` non-empty, <= 256 bytes;
  - `version_hash` matches `sha256:<64-lowercase-hex>`;
  - at most 64 artifacts.
- `action: "revert"` does not require trace artifacts.
- `--health` remains payload-free.
- Invalid-payload reports still emit stable empty report fields and do not echo oversized/malformed trace bodies.
- Legacy migration fields may remain accepted, but legacy `execute` payloads must also include canonical trace artifacts.

### TDD steps

#### Step 1 — RED: add execute trace-presence contract tests

Add tests similar to:

```go
func TestPayloadValidateRejectsExecuteWithoutTraceArtifacts(t *testing.T) {
    payload := Payload{
        Action:               "execute",
        Workdir:              "/tmp/blk-pipe-repo",
        EngineCommand:        []string{"/tmp/fake-engine.sh"},
        ValidationCommands:   []string{"true"},
        AllowedModifiedFiles: []string{"README.md"},
        TimeoutSeconds:       60,
        MaxOutputBytes:       4096,
    }

    err := payload.Validate()
    if err == nil {
        t.Fatal("Validate() error = nil, want trace_artifacts rejection")
    }
    if !strings.Contains(err.Error(), "trace_artifacts") || !strings.Contains(err.Error(), "non-empty") {
        t.Fatalf("Validate() error = %q, want non-empty trace_artifacts", err.Error())
    }
}

func TestPayloadValidateRevertDoesNotRequireTraceArtifacts(t *testing.T) {
    payload := Payload{
        Action:     "revert",
        Workdir:    "/tmp/blk-pipe-repo",
        TargetHash: "0123456789abcdef0123456789abcdef01234567",
    }

    if err := payload.Validate(); err != nil {
        t.Fatalf("Validate() error = %v, want nil", err)
    }
}
```

Run:

```bash
go test ./internal/contracts -run 'TestPayloadValidateRejectsExecuteWithoutTraceArtifacts|TestPayloadValidateRevertDoesNotRequireTraceArtifacts' -v
```

Expected RED: execute-without-trace test fails because empty execute traces are currently accepted.

#### Step 2 — RED: add run-level rejection test

Add a run test that proves the engine does not run when traces are absent:

```go
func TestRunRejectsExecuteWithoutTraceArtifactsBeforeEngine(t *testing.T) {
    repo := testutil.NewGitRepo(t)
    payload := payloadJSON(t, contracts.Payload{
        Action:               "execute",
        Workdir:              repo,
        EngineCommand:        []string{"sh", "-c", "printf ran > SHOULD_NOT_EXIST.txt"},
        ValidationCommands:   []string{"true"},
        AllowedNewFiles:      []string{"SHOULD_NOT_EXIST.txt"},
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
    if _, err := os.Stat(filepath.Join(repo, "SHOULD_NOT_EXIST.txt")); !os.IsNotExist(err) {
        t.Fatalf("engine appears to have run; stat err=%v", err)
    }
}
```

Run:

```bash
go test ./internal/pipe -run TestRunRejectsExecuteWithoutTraceArtifactsBeforeEngine -v
```

Expected RED: current code runs the engine and succeeds or fails later rather than rejecting before engine execution.

#### Step 3 — GREEN: implement minimal contract change

Implementation guidance:

- In `Payload.Validate()`, after action/l2 sizing and before or within trace validation, require non-empty traces for `Action == "execute"`.
- Keep `ValidateTraceArtifacts(...)` reusable for shape validation and allow it to validate an empty slice when used for non-execute/report-copy contexts if needed; put action-specific presence in `Payload.Validate()`.
- Add/update helper test fixtures:

  ```go
  func canonicalTraceArtifacts() []TraceArtifact {
      return []TraceArtifact{{Kind: "REQ", ID: "REQ-DRY-001", VersionHash: "sha256:" + strings.Repeat("a", 64)}}
  }
  ```

- Update `validPayload()`, V47 payload JSON helpers, and success-oriented run tests to include canonical traces.
- Do not change report marshaling: invalid/absent traces should still render `trace_artifacts: []` on failure reports.

#### Step 4 — GREEN verification

Run:

```bash
go test ./internal/contracts -run 'Trace|PayloadValidate|DecodePayload' -v
go test ./internal/pipe -run 'Trace|WithoutTrace|V47|Success' -v
go test ./...
```

Expected GREEN: all relevant tests pass and the old physical probe for empty successful trace cannot reproduce a `SUCCESS` with `trace_artifacts: []`.

#### Step 5 — Documentation/outcome

Update `docs/BLK-010_blk-pipe-v47-hardening-cli.md`:

- Change `trace_artifacts` from “Optional ... May be empty” to “Required for execute; omitted/empty invalid for execute; not required for revert.”
- Keep “opaque metadata; BLK-pipe does not parse requirement/use-case bodies or verify hashes against files.”

Outcome doc must include:

- RED failing test output;
- GREEN focused test output;
- proof that execute-without-trace rejects before engine execution;
- statement that no live execution authority was added.

Suggested commit:

```bash
git add internal/contracts/payload.go internal/contracts/payload_test.go internal/pipe/run_test.go docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/outcomes/BLK-PIPE-008_task-001-outcome.md
git commit -m "fix: require trace artifacts for blk-pipe execute payloads"
```

---

## 7. Task 2 — Harden BLK-test Handoff Fixture Trace Validation

### Objective

Close D-002 by ensuring BLK-test handoff fixture builders cannot preserve uppercase, short, nonhex, missing, non-object, or empty trace artifacts as PASS/FAIL-shaped evidence.

### Files

Modify:

- `python/blk_test_handoff_fixtures.py`
- `python/test_blk_test_handoff_fixtures.py`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md` if BEO projection wording needs cross-reference
- `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md` if disabled adapter wording needs cross-reference

Create outcome:

- `docs/outcomes/BLK-PIPE-008_task-002-outcome.md`

### Required behavior

- `build_blk_test_pass_handoff(...)` rejects missing, empty, malformed, uppercase, short, nonhex, or non-object trace artifacts.
- `build_blk_test_fail_handoff(...)` rejects the same malformed trace artifacts.
- `build_blk_test_blocked_handoff(...)` rejects malformed trace artifacts when supplied.
- For BLOCKED source reports that genuinely lack trace because the source payload failed before trace decode, preserve `trace_artifacts: []` and add an explicit field such as:

  ```python
  "trace_absence_reason": "source report did not include decoded trace_artifacts"
  ```

  Do not allow that BLOCKED shape to become PASS/FAIL or draft BEO success evidence.
- No handoff builder may read protected BLK-req vault paths.

### TDD steps

#### Step 1 — RED: add malformed trace tests

Add table-driven Python tests covering all handoff builders:

```python
def test_blk_test_pass_payload_rejects_uppercase_trace_hash(self):
    bad = [{"kind": "REQ", "id": "REQ-DRY-001", "version_hash": "sha256:" + "A" * 64}]
    with self.assertRaisesRegex(ValueError, "sha256:<64-lowercase-hex>"):
        build_blk_test_pass_handoff(self._success_report(trace_artifacts=bad))


def test_blk_test_fail_payload_rejects_short_trace_hash(self):
    bad = [{"kind": "REQ", "id": "REQ-DRY-001", "version_hash": "sha256:abc123"}]
    with self.assertRaisesRegex(ValueError, "sha256:<64-lowercase-hex>"):
        build_blk_test_fail_handoff(self._success_report(trace_artifacts=bad))


def test_blk_test_blocked_payload_rejects_malformed_trace_when_present(self):
    bad = [{"kind": "REQ", "id": "REQ-DRY-001", "version_hash": "sha256:" + "g" * 64}]
    with self.assertRaisesRegex(ValueError, "sha256:<64-lowercase-hex>"):
        build_blk_test_blocked_handoff(self._non_success_report(trace_artifacts=bad))
```

Also add missing/non-object tests:

```python
def test_blk_test_pass_payload_rejects_non_object_trace_entry(self):
    with self.assertRaisesRegex(ValueError, "trace_artifacts"):
        build_blk_test_pass_handoff(self._success_report(trace_artifacts=["not-an-object"]))


def test_blk_test_pass_payload_rejects_empty_trace_artifacts(self):
    with self.assertRaisesRegex(ValueError, "non-empty trace_artifacts"):
        build_blk_test_pass_handoff(self._success_report(trace_artifacts=[]))
```

Run:

```bash
PYTHONPATH=python python3 -m unittest python/test_blk_test_handoff_fixtures.py -v
```

Expected RED: uppercase/noncanonical hashes are currently accepted.

#### Step 2 — GREEN: add canonical validation

Implementation guidance:

- Add `_TRACE_HASH_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")`.
- Make `_trace_artifacts(...)` strict instead of silently dropping malformed entries for PASS/FAIL.
- Preserve bounded error strings; never echo full oversized trace bodies.
- Keep dependency-free local Python.
- Prefer minimal local helper unless a shared trace helper can be introduced without broad refactor.

Suggested helper shape:

```python
def _trace_artifacts(source_report: dict[str, Any], *, require_non_empty: bool) -> list[dict[str, str]]:
    artifacts = source_report.get("trace_artifacts")
    if not isinstance(artifacts, list):
        if require_non_empty:
            raise ValueError("BLK-test handoff requires non-empty trace_artifacts")
        return []
    if require_non_empty and not artifacts:
        raise ValueError("BLK-test handoff requires non-empty trace_artifacts")
    normalized = []
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            raise ValueError(f"trace_artifacts[{index}] must be an object")
        kind = _required_string(artifact.get("kind"), f"trace_artifacts[{index}].kind")
        artifact_id = _required_string(artifact.get("id"), f"trace_artifacts[{index}].id")
        version_hash = _required_string(artifact.get("version_hash"), f"trace_artifacts[{index}].version_hash")
        if not _TRACE_HASH_PATTERN.match(version_hash):
            raise ValueError("trace_artifacts.version_hash must match sha256:<64-lowercase-hex>")
        normalized.append({"kind": kind, "id": artifact_id, "version_hash": version_hash})
    return normalized
```

Adjust PASS/FAIL to call `require_non_empty=True`; BLOCKED may call `False` but must reject malformed entries when present.

#### Step 3 — GREEN verification

Run:

```bash
PYTHONPATH=python python3 -m unittest python/test_blk_test_handoff_fixtures.py -v
python3 -m unittest discover -s python -p 'test_*.py'
```

Expected GREEN: uppercase, short, nonhex, missing, non-object, and empty PASS/FAIL traces all reject; valid fixtures still pass.

#### Step 4 — Documentation/outcome

Update fixture docs to say:

- PASS/FAIL handoff fixtures require non-empty canonical traces.
- BLOCKED handoff fixtures may record trace absence only as blocked/non-authoritative evidence.
- No handoff fixture validates hashes against BLK-req files or reads protected vaults.

Outcome doc must include:

- RED uppercase-hash acceptance evidence;
- GREEN rejection evidence;
- no protected-vault read evidence;
- no live MCP/network/model evidence.

Suggested commit:

```bash
git add python/blk_test_handoff_fixtures.py python/test_blk_test_handoff_fixtures.py docs/BLK-013_blk-test-handoff-fixture-contract.md docs/BLK-014_blk-execution-outcome-fixture-shape.md docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md docs/outcomes/BLK-PIPE-008_task-002-outcome.md
git commit -m "fix: validate canonical trace hashes in blk-test handoffs"
```

---

## 8. Task 3 — Enforce Strict Tracked/New Allowlist Semantics

### Objective

Close D-003 by making `allowed_modified_files` and `allowed_new_files` strict authorization classes rather than only a combined path allowlist.

### Files

Modify:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-008_task-003-outcome.md`

### Required behavior

- Payload validation rejects any path appearing in both `allowed_modified_files` and `allowed_new_files`.
- After branch preparation and clean preflight, before engine execution:
  - each `allowed_modified_files` path must already be tracked in Git;
  - each `allowed_new_files` path must not be tracked in Git;
  - wrong-class paths fail closed before engine execution.
- Failure status recommendation: `UNAUTHORIZED_FILE_MUTATION` with exit code `3`, because this is a repository-state authorization mismatch rather than pure JSON syntax invalidity.
- True-new success remains supported for files listed only in `allowed_new_files`.
- Tracked modifications remain supported for files listed only in `allowed_modified_files`.
- No broad staging, `git add .`, `git add -u`, stash, or triple-dot diff is introduced.

### TDD steps

#### Step 1 — RED: reject overlap in pure payload validation

Add:

```go
func TestPayloadValidateRejectsOverlappingModifiedAndNewAllowlists(t *testing.T) {
    payload := validPayload()
    payload.AllowedModifiedFiles = []string{"README.md"}
    payload.AllowedNewFiles = []string{"README.md"}

    err := payload.Validate()
    if err == nil {
        t.Fatal("Validate() error = nil, want allowlist overlap rejection")
    }
    if !strings.Contains(err.Error(), "allowed_modified_files") || !strings.Contains(err.Error(), "allowed_new_files") {
        t.Fatalf("Validate() error = %q, want both allowlist names", err.Error())
    }
}
```

Run:

```bash
go test ./internal/contracts -run TestPayloadValidateRejectsOverlappingModifiedAndNewAllowlists -v
```

Expected RED: current validation accepts overlap.

#### Step 2 — RED: reject tracked file listed only as allowed new

Add run test:

```go
func TestRunRejectsTrackedPathListedOnlyAsAllowedNew(t *testing.T) {
    repo := testutil.NewGitRepo(t)
    testutil.WriteFile(t, repo, "tracked.txt", "before\n")
    testutil.RunGit(t, repo, "add", "--", "tracked.txt")
    testutil.RunGit(t, repo, "commit", "-m", "add tracked")

    payload := payloadJSON(t, contracts.Payload{
        Action:          "execute",
        Workdir:         repo,
        TraceArtifacts:  defaultRunTraceArtifacts(),
        EngineCommand:   []string{"sh", "-c", "printf after > tracked.txt"},
        ValidationCommands: []string{"true"},
        AllowedNewFiles: []string{"tracked.txt"},
        TimeoutSeconds:  5,
        MaxOutputBytes:  4096,
    })

    var stdout bytes.Buffer
    exitCode := Run(context.Background(), payload, &stdout)
    report := decodeReport(t, stdout.Bytes())

    if exitCode != ExitUnauthorizedMutation {
        t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitUnauthorizedMutation, report)
    }
    if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
        t.Fatalf("status = %q, want UNAUTHORIZED_FILE_MUTATION", report.Status)
    }
    if got := readFile(t, filepath.Join(repo, "tracked.txt")); got != "before\n" {
        t.Fatalf("tracked.txt = %q, want unchanged", got)
    }
}
```

Expected RED: current code can succeed with a tracked modification authorized only by `allowed_new_files`.

#### Step 3 — RED: reject new file listed only as allowed modified

Add run test:

```go
func TestRunRejectsNewPathListedOnlyAsAllowedModified(t *testing.T) {
    repo := testutil.NewGitRepo(t)
    payload := payloadJSON(t, contracts.Payload{
        Action:               "execute",
        Workdir:              repo,
        TraceArtifacts:      defaultRunTraceArtifacts(),
        EngineCommand:        []string{"sh", "-c", "printf new > new.txt"},
        ValidationCommands:   []string{"true"},
        AllowedModifiedFiles: []string{"new.txt"},
        TimeoutSeconds:       5,
        MaxOutputBytes:       4096,
    })

    var stdout bytes.Buffer
    exitCode := Run(context.Background(), payload, &stdout)
    report := decodeReport(t, stdout.Bytes())

    if exitCode != ExitUnauthorizedMutation {
        t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitUnauthorizedMutation, report)
    }
    if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
        t.Fatalf("status = %q, want UNAUTHORIZED_FILE_MUTATION", report.Status)
    }
    assertClean(t, repo)
}
```

Expected RED: current combined-boundary behavior may accept the new file under `allowed_modified_files`.

#### Step 4 — GREEN: implement repository-state class check

Implementation guidance:

- Add overlap detection to payload validation after path validation.
- Add a repo-state helper in `internal/pipe/run.go` or a small gitguard helper. Keep all Git calls bounded through existing `runGit`/bounded helpers.
- Run the repo-state check after branch preparation and clean preflight, before engine execution.
- Use Git tracked state, not filesystem existence alone. Suggested behavior:
  - `git ls-files --error-unmatch -- <path>` success -> tracked;
  - exit nonzero -> untracked/nonexistent;
  - unexpected command error -> `INTERNAL_ERROR`.
- If an `allowed_modified_files` path is not tracked, fail with `UNAUTHORIZED_FILE_MUTATION` and a bounded error such as `allowed_modified_files path is not tracked before engine execution`.
- If an `allowed_new_files` path is tracked, fail with `UNAUTHORIZED_FILE_MUTATION` and a bounded error such as `allowed_new_files path is already tracked before engine execution`.
- Do not run the engine after wrong-class authorization failure.

#### Step 5 — GREEN verification

Run:

```bash
go test ./internal/contracts -run 'Allowlist|Allowed' -v
go test ./internal/pipe -run 'AllowedNew|AllowedModified|Allowlist|Success' -v
go test ./...
```

Expected GREEN:

- true-new `allowed_new_files` success still passes;
- tracked `allowed_modified_files` success still passes;
- tracked-as-new and new-as-modified fail before success commit;
- no broad staging/stash/triple-dot patterns appear.

#### Step 6 — Documentation/outcome

Update `docs/BLK-010_blk-pipe-v47-hardening-cli.md`:

- Replace combined-boundary language with strict tracked/new semantics.
- Preserve the statement that both arrays are explicit path allowlists and no broad staging is allowed.
- State wrong-class path authorization fails closed before engine execution.

Outcome doc must include:

- RED probe for tracked file under `allowed_new_files`;
- RED/green overlap behavior;
- GREEN true-new success evidence;
- production broad-staging grep evidence.

Suggested commit:

```bash
git add internal/contracts/payload.go internal/contracts/payload_test.go internal/pipe/run.go internal/pipe/run_test.go docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/outcomes/BLK-PIPE-008_task-003-outcome.md
git commit -m "fix: enforce tracked and new allowlist semantics"
```

---

## 9. Task 4 — Move No-Candidate Diff Gate Before Validation

### Objective

Close D-004 by ensuring validation commands do not run unless the engine has produced a candidate mutation.

### Files

Modify:

- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-008_task-004-outcome.md`

### Required behavior

- After the engine exits successfully and after unauthorized engine-residue checks, BLK-pipe checks for an engine-produced candidate diff before validation commands run.
- If no candidate mutation exists:
  - validation commands do not run;
  - `validation_logs` is `{}`;
  - status is `UNAUTHORIZED_FILE_MUTATION`;
  - exit code is `3`;
  - no commit is created;
  - workspace is clean/restored.
- Validation commands continue to run sequentially only when there is an engine candidate to validate.

### TDD steps

#### Step 1 — RED: validation must not run with no candidate diff

Add:

```go
func TestRunSkipsValidationWhenEngineProducesNoCandidateDiff(t *testing.T) {
    repo := testutil.NewGitRepo(t)
    beforeHead := git(t, repo, "rev-parse", "HEAD")
    payload := payloadJSON(t, contracts.Payload{
        Action:               "execute",
        Workdir:              repo,
        TraceArtifacts:       defaultRunTraceArtifacts(),
        EngineCommand:        []string{"sh", "-c", "true"},
        ValidationCommands:   []string{"printf VALIDATION_RAN"},
        AllowedModifiedFiles: []string{"README.md"},
        TimeoutSeconds:       5,
        MaxOutputBytes:       4096,
    })

    var stdout bytes.Buffer
    exitCode := Run(context.Background(), payload, &stdout)
    report := decodeReport(t, stdout.Bytes())

    if exitCode != ExitUnauthorizedMutation {
        t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitUnauthorizedMutation, report)
    }
    if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
        t.Fatalf("status = %q, want UNAUTHORIZED_FILE_MUTATION", report.Status)
    }
    if len(report.ValidationLogs) != 0 {
        t.Fatalf("validation logs = %#v, want empty because validation must not run", report.ValidationLogs)
    }
    if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
        t.Fatalf("HEAD = %q, want unchanged %q", got, beforeHead)
    }
    assertClean(t, repo)
}
```

Run:

```bash
go test ./internal/pipe -run TestRunSkipsValidationWhenEngineProducesNoCandidateDiff -v
```

Expected RED: current implementation records validation output before returning `UNAUTHORIZED_FILE_MUTATION`.

#### Step 2 — GREEN: add pre-validation no-candidate gate

Implementation guidance:

- Place the new gate after engine execution and after unauthorized engine residue checks.
- Do not use staged files for this gate because staging has not happened yet.
- Check for worktree/Git candidate changes created by the engine. Existing snapshot helpers may be reused if they distinguish changed paths without validating command side effects.
- If no candidate exists, call the same cleanup path currently used for no staged allowlisted diff and return `ExitUnauthorizedMutation`.
- Keep the later staged-files empty gate as defense in depth.

#### Step 3 — GREEN verification

Run:

```bash
go test ./internal/pipe -run 'NoCandidate|Validation|Unauthorized|Success' -v
go test ./...
```

Expected GREEN:

- no-candidate validation log stays empty;
- validation still runs when the engine produces a candidate;
- validation failure cleanup/status behavior remains unchanged;
- later staged-file gate remains intact.

#### Step 4 — Documentation/outcome

Update `docs/BLK-010_blk-pipe-v47-hardening-cli.md` to say validation runs only after an engine-produced candidate exists.

Outcome doc must include:

- RED probe proving validation ran before this fix;
- GREEN output proving `validation_logs == {}` for no-candidate diff;
- unchanged validation success/failure evidence.

Suggested commit:

```bash
git add internal/pipe/run.go internal/pipe/run_test.go docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/outcomes/BLK-PIPE-008_task-004-outcome.md
git commit -m "fix: gate validation on engine candidate diff"
```

---

## 10. Task 5 — Add BLK-004 Current-State Overlay and Decision Documentation

### Objective

Close D-005 through D-009, and document Sprint 008 decisions for D-001 through D-004 so future implementers do not have to infer policy from code alone.

### Files

Modify:

- `docs/BLK-004_blk-pipe-v47-architecture-suite.md`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md` if current-disabled wording needs cross-reference
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`
- `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`
- `README.md` if the active contract list or quick summary becomes stale

Create outcome:

- `docs/outcomes/BLK-PIPE-008_task-005-outcome.md`

### Required documentation decisions

Add a BLK-004 current-state overlay near the top of `docs/BLK-004_blk-pipe-v47-architecture-suite.md`, before the source segments, with language equivalent to:

```markdown
## Current-State Overlay after BLK-PIPE-008

BLK-004 remains intentional V47/BLK-pipe authority. The source segments below are preserved as authority context, but current BLK-System operation applies these explicit overlays:

1. `execute` payloads require non-empty canonical `trace_artifacts`; `revert` and `--health` do not.
2. BLK-pipe validates trace metadata shape and presence only; it does not parse requirement/use-case bodies, generate RTMs, or verify hashes against BLK-req files.
3. `allowed_modified_files` and `allowed_new_files` are strict tracked/new authorization classes. Wrong-class paths fail closed before engine execution.
4. Validation commands run only after the engine produces a candidate mutation.
5. Current local health output is `{"status":"OK","component":"blk-pipe"}`. The older `{"status":"healthy"}` literal is not the current BLK-System local CLI contract.
6. `codex`/live examples in source segments are target-state examples only. Current live Codex, live BLK-test MCP, authoritative BEO publication, and RTM generation remain disabled unless later active doctrine explicitly authorizes them.
7. Local exit codes 6/7/9, stronger ignored-file cleanup, legacy migration fields, and additional report fields are accepted BLK-System local V47-compatible extensions.
```

Also add a corrected current execute example containing canonical `trace_artifacts` and no live-Codex authorization implication.

### Documentation gates

Run active doctrine vocabulary and boundary checks:

```bash
python3 - <<'PY'
from pathlib import Path
import re
failures = []
for p in sorted(Path('docs').glob('BLK-*.md')):
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

Run BLK-004 overlay gate:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('docs/BLK-004_blk-pipe-v47-architecture-suite.md').read_text()
for phrase in [
    'Current-State Overlay after BLK-PIPE-008',
    'execute payloads require non-empty canonical `trace_artifacts`',
    'strict tracked/new authorization classes',
    'Validation commands run only after the engine produces a candidate mutation',
    '{"status":"OK","component":"blk-pipe"}',
    'live Codex, live BLK-test MCP, authoritative BEO publication, and RTM generation remain disabled',
    'accepted BLK-System local V47-compatible extensions',
]:
    assert phrase in text, f'BLK-004 overlay missing phrase: {phrase}'
print('BLK004_CURRENT_STATE_OVERLAY_PASS')
PY
```

### Outcome requirements

Outcome doc must include:

- decision table DEC-001 through DEC-009 with final adopted decisions;
- BLK-004 overlay gate output;
- active-doc vocabulary gate output;
- explicit statement that source segments were not casually rewritten or invalidated;
- current-disabled live authority statement.

Suggested commit:

```bash
git add docs/BLK-004_blk-pipe-v47-architecture-suite.md docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md docs/BLK-013_blk-test-handoff-fixture-contract.md docs/BLK-014_blk-execution-outcome-fixture-shape.md docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md README.md docs/outcomes/BLK-PIPE-008_task-005-outcome.md
git commit -m "docs: record blk-004 current-state decisions"
```

---

## 11. Task 6 — Hostile Closeout, Regression Probes, and Sprint Outcome

### Objective

Prove all unsafe gaps are closed or explicitly accepted, create sprint closeout, and leave repository clean.

### Files

Create:

- `docs/outcomes/BLK-PIPE-008_sprint-closeout.md`

Modify if needed:

- `docs/reviews/BLK-004_hostile-deviation-review.md` only to append a closure note pointing to Sprint 008 outcomes. Do not rewrite the original hostile findings.

### Required closeout probes

Run or create deterministic probes proving the old bad behaviors no longer reproduce:

```text
PROBE_EMPTY_TRACE_EXECUTION_REJECTED
PROBE_HANDOFF_UPPERCASE_HASH_REJECTED
PROBE_ALLOWED_NEW_TRACKED_MODIFICATION_REJECTED
PROBE_ALLOWED_MODIFIED_NEW_FILE_REJECTED
PROBE_ZERO_DIFF_VALIDATION_SKIPPED
BLK004_CURRENT_STATE_OVERLAY_PASS
```

Recommended probe expectations:

- empty execute trace -> `INVALID_PAYLOAD`, no engine marker file;
- uppercase handoff hash -> `ValueError` with `sha256:<64-lowercase-hex>`;
- tracked file under `allowed_new_files` -> `UNAUTHORIZED_FILE_MUTATION`, tracked file unchanged, no success commit;
- new file under `allowed_modified_files` -> `UNAUTHORIZED_FILE_MUTATION`, workspace clean;
- no-candidate engine -> `UNAUTHORIZED_FILE_MUTATION`, `validation_logs: {}`;
- health -> current accepted output `{"status":"OK","component":"blk-pipe"}`.

### Full verification stack

Run:

```bash
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
go run ./cmd/blk-pipe --health
git diff --check
python3 - <<'PY'
from pathlib import Path
prefix = 'BLK-PIPE-008'
for p in sorted(Path('docs/outcomes').glob(f'{prefix}*.md')):
    text = p.read_text()
    for line in text.splitlines()[:12]:
        if line.startswith('**Remote:**') and 'pending' in line.lower():
            raise AssertionError(f'{p}: stale pending remote metadata: {line}')
print('OUTCOME_REMOTE_METADATA_PASS')
PY
git status --short --branch
```

After Python tests, remove generated cache before final status/commit:

```bash
rm -rf python/__pycache__
git status --short --branch
```

### Closeout contents

`docs/outcomes/BLK-PIPE-008_sprint-closeout.md` must include:

- final decision register DEC-001 through DEC-009;
- task outcome links;
- RED/GREEN summary for each unsafe gap;
- physical probe outputs;
- full verification output;
- explicit non-authorization statement for live Codex, live BLK-test MCP, authoritative BEO publication, RTM generation, cyber execution, and full sandbox claims;
- remaining deferred items, if any.

Suggested commit:

```bash
git add docs/outcomes/BLK-PIPE-008_sprint-closeout.md docs/reviews/BLK-004_hostile-deviation-review.md
git commit -m "docs: close out blk-pipe sprint 008"
```

---

## 12. Final Acceptance Criteria

Sprint 008 is accepted only if all of the following are true:

1. `execute` payloads without non-empty canonical `trace_artifacts` cannot reach engine execution.
2. Valid `revert` payloads remain trace-optional.
3. BLK-test PASS/FAIL handoff fixtures reject malformed trace artifacts.
4. BLOCKED handoff fixtures do not launder malformed trace artifacts into later fixture paths.
5. A tracked file cannot be authorized solely by `allowed_new_files`.
6. A new file cannot be authorized solely by `allowed_modified_files`.
7. True-new file creation under `allowed_new_files` still succeeds.
8. Tracked modification under `allowed_modified_files` still succeeds.
9. Validation commands do not run when the engine produced no candidate diff.
10. Current health output is explicitly accepted/documented or deliberately changed with matching tests. This plan recommends acceptance/documentation, not change.
11. BLK-004 contains a current-state overlay documenting trace policy, allowlist semantics, zero-diff sequencing, health output, disabled live boundaries, extension exit codes, cleanup hardening, and schema/report extensions.
12. No live execution authority, BLK-test authority, BEO publication authority, or RTM authority is added.
13. Full verification passes:

    ```text
    python3 -m unittest discover -s python -p 'test_*.py'
    go test ./...
    go vet ./...
    go run ./cmd/blk-pipe --health
    git diff --check
    ```

14. `python/__pycache__/` is removed before commit.
15. Outcome documents and sprint closeout exist for all tasks.
16. Repository is clean and pushed only after verification.

---

## 13. Recommended Execution Order

1. Commit/preserve the BLK-004 hostile deviation review and this plan.
2. Task 1 first: trace-empty success is the highest architecture gap.
3. Task 2 second: handoff hash validation is localized and high confidence.
4. Task 3 third: allowlist class enforcement is more invasive; isolate it after trace work.
5. Task 4 fourth: sequencing change may interact with run tests; keep separate from allowlist changes.
6. Task 5 fifth: update doctrine after code behavior is final.
7. Task 6 last: hostile probe closeout and verification.

Do not combine Tasks 1, 3, and 4 in one implementation commit. They touch the same run/contract surfaces but represent separate safety decisions and need separate RED/GREEN evidence.
