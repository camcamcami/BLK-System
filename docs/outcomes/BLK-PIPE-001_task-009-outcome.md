# BLK-pipe Sprint 001 — Task 9 Outcome

**Status:** Complete
**Date:** 2026-05-03
**Task:** Add protected BLK-req path deny tests
**Implementation Commit:** `fbc3a6c feat: hard-deny blk-req artifact mutations`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Task 9 locks the BLK-006 hard-deny rule for BLK-req artifact paths at both the payload-contract and pipe-orchestration layers.

The protected path families are:

```text
docs/requirements/*
docs/use_cases/*
```

The intended matcher is equivalent to:

```regexp
^docs/(requirements|use_cases)/.*
```

The safety requirement is not only that these paths fail payload validation, but also that BLK-pipe refuses them before invoking the engine. A protected requirements or use-case artifact must not be editable through an execution payload, and an engine must not get a chance to produce side effects when such a payload is submitted.

---

## 2. Files Changed

### `internal/contracts/payload_test.go`

Updated existing invalid-payload table coverage so the BLK-req protected artifact cases explicitly cover the Task 9 payload examples:

- `allowed_modified_files: ["docs/requirements/active/REQ-001.md"]`
- `allowed_new_files: ["docs/use_cases/staging/UC-001.md"]`

The tests assert validation fails and that the reported validation error identifies the protected path family.

### `internal/pipe/run_test.go`

Added pipe-level regression coverage in `TestRunProtectedDocsAllowlistRejectsBeforeEngine`.

The new test exercises both protected path families and verifies:

- BLK-pipe returns `ExitInvalidPayload`,
- the report status is `INVALID_PAYLOAD`,
- the report error identifies the protected path family,
- the fake engine marker file is absent, proving the engine did not run,
- the hermetic Git repository remains clean.

---

## 3. Behavior Locked

Production validation already rejected protected BLK-req paths before this task. Task 9 therefore did not require production-code changes; it added and refined regression coverage to make the behavior explicit and hard to regress.

Current production behavior in `internal/contracts/payload.go` rejects allowlist entries with these prefixes:

```go
strings.HasPrefix(entry, "docs/requirements/")
strings.HasPrefix(entry, "docs/use_cases/")
```

For cleaned relative allowlist entries, this is equivalent to the Task 9 required regex:

```regexp
^docs/(requirements|use_cases)/.*
```

Because `internal/pipe.Run` validates the payload before clean-repo preflight and engine execution, protected BLK-req allowlist entries fail pre-execution.

---

## 4. TDD / Regression Evidence

### 4.1 Contract-layer coverage

Focused contract verification passed:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/contracts -run 'TestPayloadValidateRejectsInvalidPayloads/protected_BLK-req' -v
```

Observed result:

```text
=== RUN   TestPayloadValidateRejectsInvalidPayloads
=== RUN   TestPayloadValidateRejectsInvalidPayloads/protected_BLK-req_requirements_artifact_path
=== RUN   TestPayloadValidateRejectsInvalidPayloads/protected_BLK-req_use_case_artifact_path
--- PASS: TestPayloadValidateRejectsInvalidPayloads
PASS
ok  github.com/camcamcami/BLK-System/internal/contracts
```

### 4.2 Pipe-layer pre-execution coverage

Focused pipe verification passed:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run TestRunProtectedDocsAllowlistRejectsBeforeEngine -v
```

Observed result:

```text
=== RUN   TestRunProtectedDocsAllowlistRejectsBeforeEngine
=== RUN   TestRunProtectedDocsAllowlistRejectsBeforeEngine/modified_requirements_artifact
=== RUN   TestRunProtectedDocsAllowlistRejectsBeforeEngine/new_use_case_artifact
--- PASS: TestRunProtectedDocsAllowlistRejectsBeforeEngine
PASS
ok  github.com/camcamcami/BLK-System/internal/pipe
```

### 4.3 TDD note

The new Task 9 assertions described the required behavior before any production-code edits. They revealed that the existing Task 2/Task 8 implementation already enforced the hard deny. The correct minimal implementation for Task 9 was therefore tests-only: keep the existing production behavior and add explicit regression locks.

---

## 5. Review Results

Two independent review gates were run before pushing.

### 5.1 Spec compliance review

Result: `PASS`

Reviewer confirmed:

- the commit touched only the expected files,
- contract coverage includes the exact protected requirements and use-case payload examples,
- pipe coverage proves protected path validation fails before engine invocation,
- current prefix checks are equivalent to `^docs/(requirements|use_cases)/.*` for cleaned relative allowlist entries,
- `go test ./internal/contracts ./internal/pipe -v` passed.

### 5.2 Code quality and safety review

Initial result: `REQUEST_CHANGES`

The reviewer found the first version added a standalone contract test that duplicated existing protected path cases in `TestPayloadValidateRejectsInvalidPayloads`. The requested fix was to remove duplication or consolidate the Task 9 cases into the existing table while keeping the useful pipe-level orchestration test.

Fix applied:

- removed the duplicated standalone contract test,
- renamed/refined the existing invalid-payload table cases to BLK-req terminology,
- changed the use-case path to the exact Task 9 example `docs/use_cases/staging/UC-001.md`,
- kept the pipe-level engine-noninvocation regression test.

Final result: `APPROVED`

Reviewer confirmed:

- no production files changed,
- no duplicated/unhelpful test coverage remained,
- assertions are appropriate and not overly brittle,
- `gofmt`, `git diff --check`, and `go test -count=1 ./...` passed,
- repository status remained clean.

---

## 6. Final Verification

Final controller-side verification before push:

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -l internal/contracts/payload_test.go internal/pipe/run_test.go
go test ./internal/contracts -run 'TestPayloadValidateRejectsInvalidPayloads/protected_BLK-req' -v
go test ./internal/pipe -run TestRunProtectedDocsAllowlistRejectsBeforeEngine -v
go test ./internal/contracts ./internal/pipe -v
go test ./...
git diff --check HEAD^ HEAD
git status --short --branch
git log --oneline --decorate -4
git push origin main
git status --short --branch
git log --oneline --decorate -4
```

Final results:

- `gofmt -l`: no output
- focused contract tests: passed
- focused pipe tests: passed
- `go test ./internal/contracts ./internal/pipe -v`: passed
- `go test ./...`: passed
- `git diff --check HEAD^ HEAD`: passed
- push to `origin/main`: succeeded
- final Git status: `## main...origin/main`

Latest implementation commit after push:

```text
fbc3a6c (HEAD -> main, origin/main) feat: hard-deny blk-req artifact mutations
```

---

## 7. Deviations / Notes

### Tests-only implementation

Task 9 did not require production-code changes because the hard deny already existed in `internal/contracts/payload.go` and `internal/pipe.Run` already validates payloads before engine execution.

This is acceptable for Task 9 because its objective was to lock the BLK-006 deny behavior with explicit tests.

### Review-driven cleanup

The first local implementation commit contained duplicated contract coverage. The implementation commit was amended before push to remove the duplication while preserving exact Task 9 coverage.

### Scope preserved

This task does not implement any broader BLK-004/V47 behavior. The following remain intentionally deferred to later tasks/sprints:

- CLI payload file support via `blk-pipe --payload /absolute/path/to/payload.json`,
- full V47 payload/report schema,
- revert behavior,
- validation-command sequencing,
- Python adapter integration,
- full environment scrub and bounded Git wrapper policy.

---

## 8. Next Task

Task 10 is next.

Task 10 objective: add CLI payload-file support while preserving the existing explicit stdin path.

Expected CLI behaviors:

```text
blk-pipe --payload /absolute/path/to/payload.json
blk-pipe --payload-stdin
```

Important Task 10 constraints:

- zero-argument invocation must remain unsupported and nonblocking,
- `--payload-stdin` must keep working,
- `--payload` should require an absolute file path,
- missing, relative, or extra payload arguments should fail deterministically,
- this is the bridge needed for the BLK-004 Python adapter expectation.
