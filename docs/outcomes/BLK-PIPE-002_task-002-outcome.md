# BLK-pipe Sprint 002 — Task 2 Outcome

**Status:** Complete
**Date:** 2026-05-03
**Task:** Add V47 Payload and Stable Report Contracts With Legacy Normalization
**Commit:** `b123772 feat: add blk-pipe v47 contracts`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Task 2 added BLK-004/V47-compatible payload decoding and stable report fields while preserving Sprint 001 payload compatibility.

The task intentionally stayed within contract/report migration scope. It did **not** implement:

- revert behavior,
- validation command execution,
- branch/fetch/orphan handling,
- bounded Git helper work,
- signal/panic handling,
- Python adapter,
- Codex/live LLM integration.

---

## 2. Files Added/Changed

Changed:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/contracts/report.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`

Added:

- `internal/contracts/report_test.go`

Commit stat:

```text
internal/contracts/payload.go      | 114 ++++++++++++++++++++
internal/contracts/payload_test.go | 191 +++++++++++++++++++++++++++++++++-
internal/contracts/report.go       |  64 ++++++++++--
internal/contracts/report_test.go  |  75 ++++++++++++++
internal/pipe/run.go               |  18 ++--
internal/pipe/run_test.go          | 206 +++++++++++++++++++++++++++++++++++++
6 files changed, 647 insertions(+), 21 deletions(-)
```

---

## 3. Behavior Implemented

### 3.1 Legacy Sprint 001 payload compatibility

Sprint 001 payloads remain accepted:

```json
{
  "action": "execute",
  "workdir": "/absolute/path/to/repo",
  "engine_command": ["sh", "-c", "printf after > README.md"],
  "allowed_modified_files": ["README.md"],
  "allowed_new_files": [],
  "timeout_seconds": 5,
  "max_output_bytes": 4096
}
```

Existing validation still applies to:

- action,
- absolute workdir,
- non-empty engine command,
- timeout/output limits,
- allowlist path cleanliness,
- Git pathspec/glob hazards,
- protected BLK-req paths.

### 3.2 V47-compatible payload decoding

V47-style execute payloads are now accepted and normalized:

```json
{
  "action": "execute",
  "ceb_id": "CEB_011",
  "work_dir": "/absolute/path/to/repo",
  "target_branch": "sprint/ceb-011",
  "engine": "sh",
  "engine_args": ["-c", "printf after > README.md"],
  "l2_packet": "## fake packet for local test",
  "validation_commands": ["go test ./..."],
  "allowed_modified_files": ["README.md"],
  "allowed_new_files": []
}
```

Normalization rules now implemented:

- `work_dir` maps to internal `Workdir`.
- legacy `workdir` remains accepted.
- `engine` plus `engine_args` maps to internal `EngineCommand`.
- legacy `engine_command` remains accepted.
- missing V47 timeout/output fields receive deterministic defaults:
  - `timeout_seconds = 900`,
  - `max_output_bytes = 52428800`.
- protected `docs/requirements/` and `docs/use_cases/` allowlist paths are still rejected.

### 3.3 Mixed-shape conflict hardening

The first implementation review caught an important ambiguity: mixed legacy/V47 payloads could silently prefer V47 fields when both forms were present.

That was fixed before push. BLK-pipe now rejects conflicting mixed fields when:

- `workdir` and `work_dir` are both present and differ,
- `engine_command` and normalized `engine`/`engine_args` are both present and differ.

Matching mixed fields may still be accepted when they normalize to the same internal value.

### 3.4 Stable report JSON fields

The report contract now includes V47-compatible fields while preserving legacy report fields.

Stable fields are emitted even when empty:

- `exit_code`,
- `git_diff`,
- `engine_logs`,
- `validation_logs`,
- `untracked_files`,
- `staged_files`,
- `destroyed_files`,
- legacy `commit_hash`,
- legacy `error`.

`validation_logs` is initialized to an empty object and `untracked_files` to an empty array for every report path.

### 3.5 Pipe report population

`pipe.Run` now:

- initializes stable report fields consistently,
- uses `contracts.DecodePayload` instead of directly unmarshalling into the old struct,
- sets `report.ExitCode` before JSON encoding,
- populates report metadata from payload where available:
  - `action`,
  - legacy `workdir`,
  - V47 `work_dir`,
  - `target_branch`,
  - `ceb_id`.

Invalid payload reports also preserve available metadata when possible, including mixed-shape conflict reports.

---

## 4. TDD Evidence

### 4.1 Initial RED

The implementation subagent wrote tests first, then ran:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/contracts -run 'TestPayload.*V47|TestPayload.*Legacy|TestReport' -v
```

Expected RED occurred because the new decoder/defaults/report fields did not exist yet:

```text
internal/contracts/payload_test.go:30:18: undefined: DecodePayload
internal/contracts/payload_test.go:78:31: undefined: DefaultTimeoutSeconds
internal/contracts/payload_test.go:81:31: undefined: DefaultMaxOutputBytes
FAIL github.com/camcamcami/BLK-System/internal/contracts [build failed]
```

The pipe-level tests also failed as expected because the report did not yet expose V47 fields:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestRun.*V47|TestRun.*Report' -v
```

Observed RED summary:

```text
report.ExitCode undefined
report.WorkDir undefined
report.TargetBranch undefined
report.CebID undefined
FAIL github.com/camcamcami/BLK-System/internal/pipe [build failed]
```

### 4.2 Review-fix RED — mixed payload conflicts and stable legacy fields

The code-quality reviewer requested conflict hardening and stable legacy `commit_hash` / `error` fields.

Regression tests were added first and failed before implementation:

```bash
go test ./internal/contracts -run 'TestPayloadDecodeRejectsMixed|TestReportJSONIncludesStableV47FieldsWhenEmpty' -v
```

Expected RED summary:

```text
TestPayloadDecodeRejectsMixedWorkdirConflict: conflict was silently accepted
TestPayloadDecodeRejectsMixedEngineCommandConflict: conflict was silently accepted
TestReportJSONIncludesStableV47FieldsWhenEmpty: missing "commit_hash"
```

### 4.3 Review-fix RED — invalid payload metadata preservation

The spec re-review found that conflict reports lost available metadata because `DecodePayload` returned a zero `Payload` with the conflict error.

Pipe-level regression tests were added first and failed before implementation:

```text
TestRunInvalidPayloadWorkdirConflictPreservesReportMetadata
TestRunInvalidPayloadEngineConflictPreservesReportMetadata
```

Expected RED showed empty report metadata:

```text
Action = ""
Workdir = ""
WorkDir = ""
TargetBranch = ""
CebID = ""
```

### 4.4 GREEN

After implementation and review fixes, focused and full verification passed:

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/contracts/*.go internal/pipe/run.go internal/pipe/run_test.go
go test ./internal/contracts -v
go test ./internal/pipe -v
go test ./...
go vet ./...
git diff --check
```

Observed summary:

```text
ok github.com/camcamcami/BLK-System/internal/contracts
ok github.com/camcamcami/BLK-System/internal/pipe
ok github.com/camcamcami/BLK-System/cmd/blk-pipe
ok github.com/camcamcami/BLK-System/internal/engine
ok github.com/camcamcami/BLK-System/internal/gitguard
ok github.com/camcamcami/BLK-System/internal/testutil
```

---

## 5. Review Results

### 5.1 First Spec Compliance Review

Result: **PASS initially, then superseded by later stricter spec re-review after quality fixes**

The first spec reviewer confirmed core Task 2 behavior:

- legacy and V47 payload decoding,
- V47 defaults,
- protected BLK-req validation,
- stable V47 fields,
- `contracts.DecodePayload` usage,
- `report.ExitCode` assignment,
- no revert or live LLM/Codex integration.

### 5.2 First Code Quality / Safety Review

Result: **REQUEST_CHANGES**

Important findings:

1. Mixed legacy/V47 payload fields had ambiguous precedence:
   - `workdir` vs `work_dir`,
   - `engine_command` vs `engine`/`engine_args`.
2. Legacy report fields `commit_hash` and `error` had become `omitempty`, weakening Sprint 001 report-shape stability.

Fixes applied:

- conflicting mixed payload fields now reject with validation errors,
- `commit_hash` and `error` are stable JSON fields again,
- clean non-duplicated V47 payload tests were added.

### 5.3 Second Spec Compliance Review

Result: **REQUEST_CHANGES**

The stricter spec re-review found that invalid mixed-field conflict reports lost available payload metadata.

Fix applied:

- `DecodePayload` now returns decoded raw metadata alongside conflict errors,
- conflict reports preserve available `action`, `workdir`, `work_dir`, `target_branch`, and `ceb_id`.

### 5.4 Final Spec Compliance Review

Result: **PASS**

The final spec reviewer verified amended commit `b123772` and ran:

```bash
go test ./internal/contracts -v
go test ./internal/pipe -v
go test ./...
git diff --check HEAD~1..HEAD
```

All checks passed.

### 5.5 Final Code Quality / Safety Review

Result: **APPROVED**

The final code-quality reviewer found:

```text
Critical Issues: None.
Important Issues: None.
Minor Issues: None.
Verdict: APPROVED
```

The reviewer specifically confirmed:

- payload normalization is clear,
- ambiguous mixed legacy/V47 precedence is hardened,
- Sprint 001 payload compatibility remains intact,
- allowlist validation remains intact,
- report JSON stability is robust,
- conflict reports preserve available metadata,
- no revert, branch handling, validation execution, Codex/live LLM integration, or out-of-scope engine-log capture was added.

---

## 6. Final Verification

Controller verification before pushing the implementation commit:

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -l internal/contracts/payload.go internal/contracts/payload_test.go internal/contracts/report.go internal/contracts/report_test.go internal/pipe/run.go internal/pipe/run_test.go
go test ./internal/contracts -v
go test ./internal/pipe -v
go test ./...
go vet ./...
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
git diff --check HEAD^ HEAD
git status --short --branch
git push origin main
git status --short --branch
```

Observed final state:

```text
b123772 (HEAD -> main, origin/main) feat: add blk-pipe v47 contracts
57ffc64 docs: record BLK-pipe sprint 002 task 1 outcome
f30ead8 feat: reconcile blk-pipe v47 exit codes
3ee6ded docs: plan blk-pipe sprint 002
```

All Go tests and `go vet ./...` passed. The production broad-staging grep printed no matches. `git diff --check HEAD^ HEAD` passed. The implementation commit was pushed to `origin/main`.

---

## 7. Deviations / Notes

- The implementation commit was amended twice before push:
  - first to address code-quality findings around mixed-field ambiguity and stable legacy report fields,
  - second to address spec-review findings around invalid-payload conflict report metadata.
- Final pushed implementation commit: `b123772 feat: add blk-pipe v47 contracts`.
- `validation_commands` are decoded/stored for future use but are not executed in Task 2.
- `engine_logs`, `git_diff`, `diff_summary`, and `untracked_files` are contract/report fields now, but later Sprint 002 tasks will populate them with real execution data.
- Revert remains unimplemented until a later Sprint 002 task.
- Codex/live tactical engine integration remains deferred.

---

## 8. Next Task

Next planned work:

```text
BLK-pipe Sprint 002 — Task 3: Add Reusable Bounded Command Guard, Engine Log Capture, and Environment Scrub
```

Task 3 should build the reusable bounded command guard, add deterministic environment scrubbing, and wire bounded engine output into `report.EngineLogs`.
