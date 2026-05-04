# BLK-pipe Sprint 006 — BLK-001 Alignment Remediation

> **For Hermes:** Use `blk-system-sprint-execution` to implement this plan task-by-task. This sprint is deterministic local remediation only. Do not use Hindsight. Do not run live Codex, live tactical LLMs, network model services, cyber tooling, live BLK-test MCP, RTM generation, or authoritative BEO publication.

**Goal:** Remediate the BLK-PIPE-005 hostile-review findings before any further live-adjacent BLK-test MCP, BEO, RTM, or `codex-live` orchestration work is planned.

**Architecture:** Sprint 006 tightens authority and traceability seams rather than expanding execution. It makes approved-but-not-executed `codex-live` decisions non-executable, makes BLK-test MCP stubs fail closed on missing or mismatched trace evidence, canonicalizes active doctrine against BLK-001, and fixes outcome metadata gates.

**Tech Stack:** Go 1.26.x, POSIX-only BLK-pipe CLI, dependency-free Python fixture/adapter modules, deterministic Go/Python tests, Markdown doctrine/outcome documents.

---

## 0. Hostile Review Verdict Driving This Sprint

The Sprint 005 hostile review concluded:

```text
Sprint 005 is accepted as a deterministic non-live hardening sprint, but it is not a live-integration readiness signoff: approval-gate boolean semantics, MCP trace-baton strictness, active-doctrine drift, and stale Task 6 outcome metadata must be patched before any further live-adjacent orchestration work.
```

Primary source review artifact:

```text
/tmp/BLK-PIPE-005_hostile-review_BLK-001-alignment.md
```

Reusable review reference captured in the sprint-execution skill:

```text
references/blk-pipe-sprint-005-hostile-review.md
```

Sprint 006 exists to close those findings. It does **not** authorize live execution.

No live Codex, live tactical LLM, cyber tooling, live BLK-test MCP, RTM generation, or authoritative BEO publication is authorized by this plan.

---

## 1. Current Known State

Repository:

```text
/home/dad/BLK-System
```

Preflight when this plan was authored:

```text
git status --short --branch -> ## main...origin/main
git fetch origin main       -> PASS
HEAD                        -> e0d8718 docs: close out blk-pipe sprint 005
```

Hostile review verification already proved:

```text
python3 -m unittest discover -s python -p 'test_*.py' -> Ran 69 tests, OK
go test ./...                                         -> PASS
go vet ./...                                         -> PASS
go run ./cmd/blk-pipe --health                       -> {"status":"OK","component":"blk-pipe"}
production broad-staging grep                         -> PASS
production direct-Git grep                            -> PASS
triple-dot diff grep over BLK-pipe active docs         -> PASS
git diff --check                                      -> PASS
```

Hostile review targeted probes found:

```text
APPROVAL_PROBE decision= APPROVED_BUT_NOT_EXECUTED allowed= True live_execution_authorized= False
MCP PASS response without trace_artifacts -> mapped to trace_artifacts: []
ACTIVE_DOC_VOCAB_FAIL -> BLK-002 contains CEOs; BLK-006 contains traced_artifacts
OUTCOME_METADATA_FAIL -> BLK-PIPE-005_task-006-outcome.md says pending push
TRUE_ALLOWED_NEW_PROBE -> PASS; true allowed_new_files works physically
```

---

## 2. Findings-to-Task Map

| Hostile-review finding | Sprint 006 task |
| --- | --- |
| `APPROVED_BUT_NOT_EXECUTED` returns `allowed=True` | Task 1 |
| MCP response mapping can lose `trace_artifacts` | Task 2 and Task 3 |
| Single `trace_hash` approval token does not bind full trace set | Task 2 and Task 3 |
| Active BLK-002 still says `CEOs`; active BLK-006 still says `traced_artifacts` | Task 4 |
| Active BLK-006 hard-deny docs are weaker than implementation | Task 4 |
| Active BLK-003 overstates live BLK-test/BEO current authority | Task 4 |
| Task 6 outcome remote metadata says pending push | Task 5 |

---

## 3. Non-Goals and Hard Blocks

Sprint 006 must not implement or run:

- live Codex invocation,
- live tactical LLM API calls,
- network model services,
- `codex-live` runtime execution,
- cyber tooling or cyber execution,
- execution against real cyber-program repositories or live targets,
- live BLK-test MCP calls,
- authoritative BEO publication,
- complete RTM generation as a traceability ledger,
- full sandbox/container/cgroup/VM enforcement,
- production host-secret isolation claims,
- active BLK-req vault reads or requirement-body parsing.

Allowed work:

```text
deterministic local tests
fixture-only execution
fail-closed approval-gate contract hardening
disabled-by-default MCP request/response shape hardening
documentation cleanup and doctrine alignment
outcome metadata correction
```

Live `codex-live`, live BLK-test MCP, authoritative BEO publication, RTM generation, and cyber execution remain blocked after this sprint unless a later sprint explicitly authorizes and mechanically enforces them.

---

## 4. Invariants to Preserve

1. BLK-pipe remains a deterministic transport/mutation gate, not an architect, requirement parser, live LLM caller, BLK-test authority, BEO publisher, RTM generator, or sandbox.
2. Hermes/BLK-pipe/BLK-test/BEO/RTM boundaries must preserve opaque trace metadata without reading or parsing active BLK-req bodies.
3. `APPROVED_BUT_NOT_EXECUTED` means exactly that: approval-token shape validated for audit, but no current execution permission exists.
4. A generic `allowed` boolean must mean “allowed to execute now,” not “approval token matched.”
5. BLK-test PASS/FAIL-shaped data must never exist without non-empty canonical `trace_artifacts` evidence.
6. The canonical trace artifact shape is:

   ```yaml
   trace_artifacts:
     - kind: "REQ"
       id: "REQ-042"
       version_hash: "sha256:<64-lowercase-hex>"
   ```

7. Protected BLK-req vault paths remain denied to both modified and new allowlists: `docs/active/`, `docs/requirements/`, and `docs/use_cases/`.
8. Active doctrine may describe target architecture only if it clearly distinguishes current disabled/fixture-only state from future live authority.
9. New BLK-System plans and active docs use BLK-native BEB/BEO terminology and `beb_id`, not legacy execution-brief/outcome vocabulary.
10. No production `git add .`, `git add -u`, `git stash`, relative revert anchors, or triple-dot report diffs.

---

## 5. Controller Workflow for Each Task

For each task:

1. Preflight:

   ```bash
   cd /home/dad/BLK-System
   export PATH="$HOME/.local/bin:$PATH"
   git status --short --branch
   ```

2. Use strict TDD for code changes: add a failing test/probe first, capture RED, implement minimal code, capture GREEN.
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

6. Create a matching outcome document for Tasks 1-5:

   ```text
   docs/outcomes/BLK-PIPE-006_task-00N-outcome.md
   ```

7. Commit each implementation/docs task with the listed commit message.
8. Push only after verification passes and `git status --short --branch` is clean/aligned.

---

## 6. Task 1 — Make Approved `codex-live` Decisions Non-Executable

### Objective

Remove the approval-gate footgun where exact-token `codex-live` returns `allowed=True` while also claiming not executed.

### Files

Modify:

- `python/blk_orchestrator_gate.py`
- `python/test_blk_orchestrator_gate.py`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`
- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md` if profile language needs a cross-reference
- `README.md` only if its approval-gate summary becomes stale

Create outcome:

- `docs/outcomes/BLK-PIPE-006_task-001-outcome.md`

### Required behavior

- `dev-smoke`, `strict-ci`, and `codex-dry-run` continue to return:
  - `decision == "ALLOWED_LOCAL_ONLY"`,
  - `allowed is True`,
  - `live_execution_authorized is False`.
- `codex-live` without token continues to return `BLOCKED_APPROVAL_REQUIRED` with `allowed is False`.
- `codex-live` with mismatched token continues to return `BLOCKED_APPROVAL_MISMATCH` with `allowed is False`.
- `codex-live` with exact token must return:
  - `decision == "APPROVED_BUT_NOT_EXECUTED"`,
  - `allowed is False`,
  - `live_execution_authorized is False`,
  - a new explicit audit field such as `approval_token_valid is True` or `approval_recorded is True`.
- `cyber-execution` remains `BLOCKED_CYBER_EXECUTION` regardless of token.
- Unknown profiles remain blocked.
- No code path may spawn Codex, call a model API, open network sockets, run cyber tooling, or call BLK-test MCP.

### TDD RED tests

Add or change tests in `python/test_blk_orchestrator_gate.py` before implementation:

```python
def test_codex_live_exact_token_records_approval_but_is_not_allowed(self):
    decision = evaluate_profile_gate(
        "codex-live",
        beb_id="BEB_006",
        target_branch="sprint/blk-pipe-006",
        trace_hash=TRACE_HASH,
        approval_token=approval_token_for(
            beb_id="BEB_006",
            target_branch="sprint/blk-pipe-006",
            trace_hash=TRACE_HASH,
        ),
    )
    self.assertEqual(decision.decision, "APPROVED_BUT_NOT_EXECUTED")
    self.assertFalse(decision.allowed)
    self.assertFalse(decision.live_execution_authorized)
    self.assertTrue(decision.approval_recorded)
```

Expected RED before implementation:

```text
AssertionError: True is not false
AttributeError: 'ProfileDecision' object has no attribute 'approval_recorded'
```

### Implementation guidance

- Treat `ProfileDecision.allowed` as “this profile is allowed to execute now.”
- Add a separate frozen dataclass field, for example:

  ```python
  approval_recorded: bool = False
  ```

- Set `approval_recorded=True` only for exact-token `APPROVED_BUT_NOT_EXECUTED`.
- Do not rename the existing `allowed` field in this task; changing its meaning by documentation and tests is enough.

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_blk_orchestrator_gate.py' -v
python3 - <<'PY'
import sys
sys.path.insert(0, 'python')
from blk_orchestrator_gate import approval_token_for, evaluate_profile_gate
h = 'sha256:' + 'a' * 64
t = approval_token_for(beb_id='BEB_006', target_branch='sprint/blk-pipe-006', trace_hash=h)
d = evaluate_profile_gate('codex-live', beb_id='BEB_006', target_branch='sprint/blk-pipe-006', trace_hash=h, approval_token=t)
assert d.decision == 'APPROVED_BUT_NOT_EXECUTED'
assert d.allowed is False
assert d.live_execution_authorized is False
assert getattr(d, 'approval_recorded') is True
print('approval semantics probe PASS')
PY
python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
```

### Deterministic review gates

Spec / traceability gate must verify:

- exact-token `codex-live` is not executable now,
- docs state `allowed` means executable now,
- docs state approval-token validation is audit-only until a later sprint authorizes live execution.

Safety / docs gate must verify:

- no forbidden live-execution tokens were introduced in runtime code,
- Markdown fences are balanced,
- touched files have final newlines and no trailing whitespace.

### Commit message

```text
fix: fail closed approved blk-pipe live profile
```

---

## 7. Task 2 — Require Canonical Trace Artifact Hashes

### Objective

Align BLK-pipe and Python fixture contracts with BLK-001’s cryptographic baton by requiring canonical `sha256:<64-lowercase-hex>` `version_hash` values without reading or verifying active BLK-req files.

### Files

Modify:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/contracts/report_test.go` if short hashes remain in report tests
- `python/blk_orchestrator_gate.py`
- `python/test_blk_orchestrator_gate.py`
- `python/blk_pipe_dry_run_orchestrator.py` only if fixture parser does not validate canonical hash shape
- `python/test_blk_pipe_dry_run_orchestrator.py` if parser tests need canonical-hash coverage
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-006_task-002-outcome.md`

### Required behavior

- Go `contracts.ValidateTraceArtifacts(...)` must reject:
  - missing `version_hash`,
  - missing `sha256:` prefix,
  - short hashes such as `sha256:0123456789abcdef`,
  - uppercase hex,
  - non-hex characters,
  - oversized values without echoing the full value.
- Go must continue to reject more than 64 trace artifacts and overlong `kind`/`id` fields.
- Python trace helpers used by approval/MCP stubs must reject malformed `version_hash` values with the same canonical regex:

  ```text
  ^sha256:[0-9a-f]{64}$
  ```

- Fixture parsing must preserve `REQ-DRY-001` as a synthetic ID but require a canonical synthetic hash.
- No code may read, parse, or verify files under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`.
- This task validates syntax only. It does not generate RTM, compare hashes against live BLK-req vault files, or publish BEOs.

### TDD RED tests

Add Go tests before implementation:

```go
func TestPayloadDecodeRejectsTraceArtifactShortSHA256Hash(t *testing.T) { ... }
func TestPayloadDecodeRejectsTraceArtifactUppercaseSHA256Hash(t *testing.T) { ... }
func TestPayloadDecodeRejectsTraceArtifactNonHexSHA256Hash(t *testing.T) { ... }
```

Expected RED before implementation:

```text
DecodePayload() error = nil, want non-nil
```

Add Python tests before implementation:

```python
def test_blk_test_mcp_request_rejects_short_trace_hash(self): ...
def test_blk_test_mcp_response_mapping_rejects_uppercase_trace_hash(self): ...
def test_load_dry_run_fixture_rejects_noncanonical_trace_hash(self): ...
```

Expected RED before implementation:

```text
AssertionError: ValueError not raised
```

### Implementation guidance

- In Go, add a package-level regex or small validation function for `sha256:<64 lowercase hex>`.
- Keep error strings sterile and bounded. Do not echo the rejected hash value.
- Update existing tests currently using short hashes, such as `sha256:0123456789abcdef`, to 64 lowercase hex.
- In Python, use a shared helper in `blk_orchestrator_gate.py` and a parser-local helper in `blk_pipe_dry_run_orchestrator.py` if needed. Do not introduce dependencies.
- If report serialization tests intentionally preserve trace artifacts without validating them, update fixtures to canonical values rather than adding validation to report marshaling.

### Focused verification

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/contracts -run 'TestPayloadDecode.*Trace|TestReportMarshal.*Trace' -v
python3 -m unittest discover -s python -p 'test_blk_orchestrator_gate.py' -v
python3 -m unittest discover -s python -p 'test_blk_pipe_dry_run_orchestrator.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
git diff --check
```

### Deterministic review gates

Spec / traceability gate must verify:

- Go rejects short, uppercase, and non-hex trace hashes,
- Python rejects short, uppercase, and non-hex trace hashes,
- docs use `sha256:<64-lowercase-hex>` language consistently,
- no active BLK-req vault reads were introduced.

Safety / docs gate must verify:

- no hash body leak in error messages,
- no network/model/MCP/Codex execution tokens introduced,
- Markdown hygiene passes.

### Commit message

```text
fix: require canonical blk trace artifact hashes
```

---

## 8. Task 3 — Bind BLK-test MCP Stubs to Source Trace Evidence

### Objective

Prevent PASS/FAIL-shaped BLK-test MCP mapping from existing without exact source evidence and trace-baton preservation.

### Files

Modify:

- `python/blk_orchestrator_gate.py`
- `python/test_blk_orchestrator_gate.py`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
- `README.md` only if its MCP summary becomes stale

Create outcome:

- `docs/outcomes/BLK-PIPE-006_task-003-outcome.md`

### Required behavior

- `build_blk_test_mcp_request(source_report, enabled=False)` must fail closed unless `source_report` contains:
  - known `status`,
  - non-empty `beb_id`,
  - non-empty `pre_engine_hash`,
  - non-empty canonical `trace_artifacts`.
- If `source_report.status == "SUCCESS"`, the request must also require:
  - non-empty `commit_hash`,
  - non-empty `staged_files`,
  - source evidence sufficient for future BLK-test evaluation.
- If `source_report.status != "SUCCESS"`, the request must not claim it is an evaluation request. It may either:
  - raise `ValueError`, or
  - return a disabled BLOCKED design object with `method: "blk_test.not_run"`.

  Choose one behavior and document it. Prefer raising for clarity unless existing callers need a blocked stub.

- `map_blk_test_mcp_response(...)` must require source context, for example:

  ```python
  def map_blk_test_mcp_response(response: dict[str, Any], *, source_request: dict[str, Any]) -> dict[str, Any]: ...
  ```

- PASS and FAIL mapping must require:
  - `source_request.source_status == "SUCCESS"`,
  - exact `beb_id` match,
  - exact `commit_hash` match,
  - exact `pre_engine_hash` match,
  - exact `trace_artifacts` match,
  - non-empty checks list.
- BLOCKED mapping must preserve source trace artifacts and may omit commit evidence if the source never succeeded.
- Unknown response statuses still reject.
- No live BLK-test MCP call is made. The send path remains disabled and records no network/subprocess calls.

### TDD RED tests

Add tests before implementation:

```python
def test_blk_test_mcp_response_mapping_requires_source_request(self): ...
def test_blk_test_mcp_response_mapping_rejects_pass_without_trace_artifacts(self): ...
def test_blk_test_mcp_response_mapping_rejects_trace_artifact_mismatch(self): ...
def test_blk_test_mcp_response_mapping_rejects_pass_without_checks(self): ...
def test_blk_test_mcp_request_rejects_non_success_as_evaluation_request(self): ...
```

Expected RED before implementation:

```text
TypeError not raised or ValueError not raised
mapped['trace_artifacts'] == []
```

### Implementation guidance

- Use deterministic deep copies for preserved evidence.
- Compare canonicalized trace artifact lists exactly. Do not sort unless documented; if sorting is desired, define a canonical order first.
- Keep API changes explicit. If changing `map_blk_test_mcp_response` signature, update all tests in the same task.
- Do not add MCP client dependencies.
- Do not add subprocess/network calls.

### Focused verification

```bash
python3 -m unittest discover -s python -p 'test_blk_orchestrator_gate.py' -v
python3 - <<'PY'
import sys
sys.path.insert(0, 'python')
from blk_orchestrator_gate import map_blk_test_mcp_response
try:
    map_blk_test_mcp_response({'status': 'PASS', 'beb_id': 'BEB_X'})
except TypeError:
    print('source-required probe PASS')
except ValueError:
    print('source-required probe PASS')
else:
    raise AssertionError('PASS mapping without source context was accepted')
PY
python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
```

### Deterministic review gates

Spec / traceability gate must verify:

- PASS/FAIL cannot map without exact source trace evidence,
- BLOCKED preserves source trace evidence,
- non-success BLK-pipe status cannot be treated as a live BLK-test evaluation request,
- docs describe disabled/current vs future-live behavior.

Safety / docs gate must verify:

- no network/subprocess/MCP live call introduced,
- no active-vault access introduced,
- Markdown hygiene passes.

### Commit message

```text
fix: bind blk-test mcp stubs to source evidence
```

---

## 9. Task 4 — Repair Active Doctrine Drift Against BLK-001

### Objective

Patch active doctrine so BLK-001 authority, trace, and BLK-req protection boundaries are not contradicted by stale active documents.

### Files

Modify:

- `docs/BLK-002_blk-req-artifact-lifecycle.md`
- `docs/BLK-003_blk-pipe-blk-test-orchestration.md`
- `docs/BLK-006_blk-req-implementation-brief.md`
- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md` if the active-doctrine gate belongs there
- `README.md` only if links or current-state summaries need updates

Create outcome:

- `docs/outcomes/BLK-PIPE-006_task-004-outcome.md`

### Required behavior

- `docs/BLK-002_blk-req-artifact-lifecycle.md` must use BLK-native BEO terminology for downstream execution outcomes.
- `docs/BLK-006_blk-req-implementation-brief.md` must use canonical `trace_artifacts` structured objects, not legacy trace-key spelling.
- `docs/BLK-006_blk-req-implementation-brief.md` must require BLK-pipe hard-deny checks for both:
  - `allowed_modified_files`,
  - `allowed_new_files`.
- `docs/BLK-006_blk-req-implementation-brief.md` must hard-deny all protected active vault paths:
  - `docs/active/`,
  - `docs/requirements/`,
  - `docs/use_cases/`.
- `docs/BLK-003_blk-pipe-blk-test-orchestration.md` must distinguish:
  - target architecture: live BLK-test and authoritative BEO generation in a future approved state,
  - current implementation state after Sprint 006: fixture-only BLK-test handoff, draft-only BEO projection, disabled live BLK-test MCP, no authoritative BEO publication, no RTM generation.
- BLK-003 should cross-link BLK-014 and BLK-015 where it discusses Phase 4.2 and BEO generation.
- Do not rewrite historical outcome evidence unless explicitly necessary.

### TDD / docs RED gates

Before editing, run and record the active vocabulary gate failure:

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
                line = text[:m.start()].count('\n') + 1
                failures.append((p, line, label, status))
        elif pat in text:
            line = text[:text.index(pat)].count('\n') + 1
            failures.append((p, line, label, status))
if failures:
    for failure in failures:
        print('ACTIVE_DOC_VOCAB_FAIL', *failure, sep=' | ')
    raise SystemExit(1)
print('ACTIVE_DOC_VOCAB_PASS')
PY
```

Expected RED before implementation:

```text
ACTIVE_DOC_VOCAB_FAIL | docs/BLK-002_blk-req-artifact-lifecycle.md | ... | standalone CEO/CEOs | **Status:** Active Operating Doctrine
ACTIVE_DOC_VOCAB_FAIL | docs/BLK-006_blk-req-implementation-brief.md | ... | traced_artifacts | **Status:** Active Planning Doctrine
```

Also run a BLK-006 hard-deny docs gate before edits and expect failure:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('docs/BLK-006_blk-req-implementation-brief.md').read_text()
for token in ['allowed_modified_files', 'allowed_new_files', 'docs/active/', 'docs/requirements/', 'docs/use_cases/']:
    assert token in text, f'BLK-006 missing {token}'
PY
```

### Focused verification

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
                failures.append((p, label))
        elif pat in text:
            failures.append((p, label))
if failures:
    raise AssertionError(failures)
print('ACTIVE_DOC_VOCAB_PASS')
PY
python3 - <<'PY'
from pathlib import Path
text = Path('docs/BLK-006_blk-req-implementation-brief.md').read_text()
for token in ['allowed_modified_files', 'allowed_new_files', 'docs/active/', 'docs/requirements/', 'docs/use_cases/']:
    assert token in text, f'BLK-006 missing {token}'
text3 = Path('docs/BLK-003_blk-pipe-blk-test-orchestration.md').read_text()
for phrase in ['fixture-only BLK-test', 'draft-only BEO', 'live BLK-test MCP remains disabled', 'RTM generation remains disabled']:
    assert phrase in text3, f'BLK-003 missing phrase: {phrase}'
print('ACTIVE_DOCTRINE_ALIGNMENT_PASS')
PY
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('docs/BLK-002_blk-req-artifact-lifecycle.md'),
    Path('docs/BLK-003_blk-pipe-blk-test-orchestration.md'),
    Path('docs/BLK-006_blk-req-implementation-brief.md'),
    Path('docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md'),
]
fence = chr(96) * 3
for p in paths:
    if not p.exists():
        continue
    text = p.read_text()
    assert text.endswith('\n'), f'{p}: missing final newline'
    assert text.count(fence) % 2 == 0, f'{p}: unbalanced fences'
    for i, line in enumerate(text.splitlines(), 1):
        assert line.rstrip() == line, f'{p}:{i}: trailing whitespace'
print('MARKDOWN_PASS')
PY
git diff --check
```

### Deterministic review gates

Spec / traceability gate must verify:

- active docs no longer contain stale legacy vocabulary,
- BLK-006 is not weaker than current hard-deny implementation,
- BLK-003 does not imply live BLK-test/BEO/RTM authority exists today,
- BLK-003 links current disabled/draft state to BLK-014/BLK-015.

Safety / docs gate must verify:

- doctrine does not authorize live Codex, live LLM, cyber tooling, live BLK-test MCP, RTM generation, or authoritative BEO publication,
- Markdown hygiene passes.

### Commit message

```text
docs: align active blk doctrine with sprint 006 findings
```

---

## 10. Task 5 — Fix Outcome Remote Metadata and Extend Metadata Gates

### Objective

Correct stale Sprint 005 Task 6 outcome metadata and extend metadata checks so closed-sprint task outcomes cannot retain pending remote-push language.

### Files

Modify:

- `docs/outcomes/BLK-PIPE-005_task-006-outcome.md`
- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md` if reusable closeout/outcome metadata gate text belongs there

Create outcome:

- `docs/outcomes/BLK-PIPE-006_task-005-outcome.md`

### Required behavior

- Replace the Task 6 outcome header line:

  ```text
  **Remote:** pending push after outcome commit
  ```

  with:

  ```text
  **Remote:** pushed to `origin/main`
  ```

- Do not rewrite Sprint 005 Task 6 implementation evidence.
- Add or update a reusable metadata gate that checks closed-sprint outcome docs for stale remote metadata.
- The gate should scan per-task outcomes and sprint closeouts, not only closeout documents.
- The gate must tolerate historical task evidence that quotes `pending push` inside RED/OLD examples only if the current header remote line is clean. Prefer checking the first 12 lines for the `**Remote:**` header rather than banning every occurrence across the full document.

### TDD / docs RED gate

Before editing, run and record failure:

```bash
python3 - <<'PY'
from pathlib import Path
for p in sorted(Path('docs/outcomes').glob('BLK-PIPE-005*.md')):
    text = p.read_text()
    for line in text.splitlines()[:12]:
        if line.startswith('**Remote:**') and 'pending' in line.lower():
            raise AssertionError(f'{p}: stale pending remote metadata: {line}')
print('OUTCOME_REMOTE_METADATA_PASS')
PY
```

Expected RED before implementation:

```text
AssertionError: docs/outcomes/BLK-PIPE-005_task-006-outcome.md: stale pending remote metadata: **Remote:** pending push after outcome commit
```

### Focused verification

```bash
python3 - <<'PY'
from pathlib import Path
for p in sorted(Path('docs/outcomes').glob('BLK-PIPE-005*.md')):
    text = p.read_text()
    for line in text.splitlines()[:12]:
        if line.startswith('**Remote:**') and 'pending' in line.lower():
            raise AssertionError(f'{p}: stale pending remote metadata: {line}')
print('OUTCOME_REMOTE_METADATA_PASS')
PY
python3 - <<'PY'
from pathlib import Path
p = Path('docs/outcomes/BLK-PIPE-005_task-006-outcome.md')
text = p.read_text()
assert '**Remote:** pushed to `origin/main`' in '\n'.join(text.splitlines()[:12])
fence = chr(96) * 3
assert text.endswith('\n')
assert text.count(fence) % 2 == 0
for i, line in enumerate(text.splitlines(), 1):
    assert line.rstrip() == line, f'trailing whitespace line {i}'
print('TASK6_METADATA_PASS')
PY
git diff --check
```

### Deterministic review gates

Spec / traceability gate must verify:

- Task 6 outcome header remote metadata is pushed/aligned,
- metadata gate checks per-task outcomes and closeouts,
- no unrelated historical outcomes are rewritten.

Safety / docs gate must verify:

- Markdown hygiene passes,
- no live-execution authorization text was introduced.

### Commit message

```text
docs: fix blk-pipe outcome metadata gate
```

---

## 11. Task 6 — Sprint 006 Closeout and Next-Sprint Seed

### Objective

Close Sprint 006 with audit-grade verification evidence and a narrow next-sprint seed that does not imply live autonomy is approved.

### Files

Create:

- `docs/outcomes/BLK-PIPE-006_sprint-closeout.md`

Modify only if needed:

- `README.md`
- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`

Create outcome:

- The sprint closeout document is the Task 6 outcome artifact. If a separate task outcome is preferred, create `docs/outcomes/BLK-PIPE-006_task-006-outcome.md` and then a separate closeout doc.

### Required closeout contents

- Final task-line implementation commit before closeout.
- Task 1-5 implementation/outcome commit table.
- BLK-PIPE-005 hostile-review findings addressed.
- Remaining blocked scope before live Codex/live BLK-test MCP.
- Explicit non-execution statement:
  - Sprint 006 did not run Codex,
  - Sprint 006 did not run live LLMs,
  - Sprint 006 did not run cyber tooling,
  - Sprint 006 did not call live BLK-test MCP,
  - Sprint 006 did not generate RTM or publish authoritative BEOs.
- Verification evidence from the final gate.
- Recommended next sprint seed. If Sprint 006 lands cleanly, recommended seed should return to the previously deferred narrow track:

  ```text
  BLK-PIPE-007 — Disabled BLK-test MCP Adapter Smoke and BEO/RTM Interface Fixtures
  ```

  or, if sandbox/approval work remains more urgent:

  ```text
  BLK-PIPE-007 — Sandbox and Capability Profile Enforcement Design
  ```

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
! git grep -n -E 'git.*diff.*\.\.\.' -- '*.go' ':!*_test.go' docs/BLK-009_blk-pipe-sprint-001-cli.md docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md docs/BLK-013_blk-test-handoff-fixture-contract.md docs/BLK-014_blk-execution-outcome-fixture-shape.md docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md docs/plans/BLK-PIPE-006_blk001-alignment-remediation.md docs/outcomes/BLK-PIPE-006_task-001-outcome.md docs/outcomes/BLK-PIPE-006_task-002-outcome.md docs/outcomes/BLK-PIPE-006_task-003-outcome.md docs/outcomes/BLK-PIPE-006_task-004-outcome.md docs/outcomes/BLK-PIPE-006_task-005-outcome.md docs/outcomes/BLK-PIPE-006_sprint-closeout.md
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
                failures.append((p, label))
        elif pat in text:
            failures.append((p, label))
if failures:
    raise AssertionError(failures)
print('ACTIVE_DOC_VOCAB_PASS')
PY
python3 - <<'PY'
from pathlib import Path
for pattern in ['BLK-PIPE-005*.md', 'BLK-PIPE-006*.md']:
    for p in sorted(Path('docs/outcomes').glob(pattern)):
        text = p.read_text()
        for line in text.splitlines()[:12]:
            if line.startswith('**Remote:**') and 'pending' in line.lower():
                raise AssertionError(f'{p}: stale pending remote metadata: {line}')
print('OUTCOME_REMOTE_METADATA_PASS')
PY
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
docs: close out blk-pipe sprint 006
```

---

## 12. Whole-Sprint Deterministic Gates

Run these gates before closing Sprint 006.

### 12.1 Approval semantics gate

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, 'python')
from blk_orchestrator_gate import approval_token_for, evaluate_profile_gate
h = 'sha256:' + 'a' * 64
t = approval_token_for(beb_id='BEB_006', target_branch='sprint/blk-pipe-006', trace_hash=h)
d = evaluate_profile_gate('codex-live', beb_id='BEB_006', target_branch='sprint/blk-pipe-006', trace_hash=h, approval_token=t)
assert d.decision == 'APPROVED_BUT_NOT_EXECUTED'
assert d.allowed is False
assert d.live_execution_authorized is False
assert getattr(d, 'approval_recorded') is True
print('APPROVAL_SEMANTICS_PASS')
PY
```

### 12.2 Trace-baton syntax gate

```bash
python3 - <<'PY'
from pathlib import Path
for p in [Path('internal/contracts/payload_test.go'), Path('python/test_blk_orchestrator_gate.py')]:
    text = p.read_text()
    assert 'short' in text.lower() and 'trace' in text.lower(), f'{p}: missing short-hash trace regression'
    assert 'uppercase' in text.lower() and 'trace' in text.lower(), f'{p}: missing uppercase trace regression'
print('TRACE_REGRESSION_NAME_GATE_PASS')
PY
go test ./internal/contracts -run 'TestPayloadDecode.*Trace|TestReportMarshal.*Trace' -v
python3 -m unittest discover -s python -p 'test_blk_orchestrator_gate.py' -v
```

### 12.3 MCP source-binding gate

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, 'python')
from blk_orchestrator_gate import map_blk_test_mcp_response
try:
    map_blk_test_mcp_response({'status': 'PASS', 'beb_id': 'BEB_X'})
except (TypeError, ValueError):
    print('MCP_SOURCE_REQUIRED_PASS')
else:
    raise AssertionError('PASS mapping without source context was accepted')
PY
```

### 12.4 Active doctrine alignment gate

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
                failures.append((p, label))
        elif pat in text:
            failures.append((p, label))
if failures:
    raise AssertionError(failures)
print('ACTIVE_DOC_VOCAB_PASS')
PY
python3 - <<'PY'
from pathlib import Path
text = Path('docs/BLK-006_blk-req-implementation-brief.md').read_text()
for token in ['allowed_modified_files', 'allowed_new_files', 'docs/active/', 'docs/requirements/', 'docs/use_cases/']:
    assert token in text, f'BLK-006 missing {token}'
print('BLK006_HARDDENY_DOC_PASS')
PY
```

### 12.5 Outcome metadata gate

```bash
python3 - <<'PY'
from pathlib import Path
for pattern in ['BLK-PIPE-005*.md', 'BLK-PIPE-006*.md']:
    for p in sorted(Path('docs/outcomes').glob(pattern)):
        text = p.read_text()
        for line in text.splitlines()[:12]:
            if line.startswith('**Remote:**') and 'pending' in line.lower():
                raise AssertionError(f'{p}: stale pending remote metadata: {line}')
print('OUTCOME_REMOTE_METADATA_PASS')
PY
```

### 12.6 No-live-execution gate

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
print('NO_LIVE_EXECUTION_PASS')
PY
```

### 12.7 Markdown hygiene gate

```bash
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('docs/plans/BLK-PIPE-006_blk001-alignment-remediation.md'),
    *Path('docs/outcomes').glob('BLK-PIPE-006*.md'),
]
fence = chr(96) * 3
for p in paths:
    text = p.read_text()
    assert text.endswith('\n'), f'{p}: missing final newline'
    assert text.count(fence) % 2 == 0, f'{p}: unbalanced fences'
    for i, line in enumerate(text.splitlines(), 1):
        assert line.rstrip() == line, f'{p}:{i}: trailing whitespace'
print('MARKDOWN_HYGIENE_PASS')
PY
```

---

## 13. Outcome Documents

Expected outcome documents:

```text
docs/outcomes/BLK-PIPE-006_task-001-outcome.md
docs/outcomes/BLK-PIPE-006_task-002-outcome.md
docs/outcomes/BLK-PIPE-006_task-003-outcome.md
docs/outcomes/BLK-PIPE-006_task-004-outcome.md
docs/outcomes/BLK-PIPE-006_task-005-outcome.md
docs/outcomes/BLK-PIPE-006_sprint-closeout.md
```

If Task 6 gets its own separate outcome in addition to the closeout, use:

```text
docs/outcomes/BLK-PIPE-006_task-006-outcome.md
```

---

## 14. Recommended Next Sprint After BLK-PIPE-006

If Sprint 006 lands cleanly, do not recommend live Codex immediately. Return to a narrow disabled/fixture track:

```text
BLK-PIPE-007 — Disabled BLK-test MCP Adapter Smoke and BEO/RTM Interface Fixtures
```

Live `codex-live` execution remains blocked until a later sprint explicitly approves and verifies:

- real approval-channel mechanics,
- approval token binding to canonical BEB/L2/trace artifacts,
- sandbox/capability enforcement,
- production credential/network isolation policy,
- live BLK-test MCP policy,
- authoritative BEO publication authority,
- RTM generation and drift rejection mechanics.

---

## 15. Quick Resume Prompt

```text
We are in /home/dad/BLK-System. Execute docs/plans/BLK-PIPE-006_blk001-alignment-remediation.md using blk-system-sprint-execution. Do not use Hindsight. Do not run live Codex, live tactical LLMs, network model services, cyber tooling, or live BLK-test MCP. Start with Task 1. Use TDD, commit each task, create matching docs/outcomes/BLK-PIPE-006_task-00N-outcome.md for Tasks 1-5, run deterministic local review gates, and push only after verification passes.
```
