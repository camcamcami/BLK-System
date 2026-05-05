# BLK-pipe Sprint 008 — Task 3 Outcome

**Status:** Complete
**Date:** 2026-05-05
**Task:** Enforce Strict Tracked/New Allowlist Semantics
**Implementation Commit:** included in the Task 3 commit containing this outcome document
**Remote:** pushed to `origin/main` after task verification

---

## 1. Objective

Task 3 closes Sprint 008 finding D-003 by making `allowed_modified_files` and `allowed_new_files` strict authorization classes rather than only a combined path boundary.

Implemented behavior:

- Payload validation rejects overlap between `allowed_modified_files` and `allowed_new_files`.
- After target-branch preparation and clean preflight, before engine execution:
  - each `allowed_modified_files` path must already be tracked by Git;
  - each `allowed_new_files` path must not be tracked by Git;
  - wrong-class authorization fails closed as `UNAUTHORIZED_FILE_MUTATION` / exit code `3`.
- True-new success remains supported for paths listed only in `allowed_new_files`.
- Tracked-file modification success remains supported for paths listed only in `allowed_modified_files`.
- No broad staging, `git add .`, `git add -u`, stash, or triple-dot report diff was introduced.

---

## 2. Files Changed

Updated:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`

Created outcome:

- `docs/outcomes/BLK-PIPE-008_task-003-outcome.md`

---

## 3. RED Evidence

### Payload overlap RED

After adding `TestPayloadValidateRejectsOverlappingModifiedAndNewAllowlists`, current validation accepted overlap:

```text
=== RUN   TestPayloadValidateRejectsOverlappingModifiedAndNewAllowlists
    payload_test.go:72: Validate() error = nil, want allowlist overlap rejection
--- FAIL: TestPayloadValidateRejectsOverlappingModifiedAndNewAllowlists (0.00s)
FAIL
FAIL	github.com/camcamcami/BLK-System/internal/contracts	0.002s
FAIL
```

### Tracked path listed only as allowed-new RED

Before the fix, a tracked file authorized only via `allowed_new_files` reached the engine and committed successfully:

```text
=== RUN   TestRunRejectsTrackedPathListedOnlyAsAllowedNew
    run_test.go:121: exit code = 0, want 3; report={Status:SUCCESS ... GitDiff:diff --git a/tracked.txt b/tracked.txt ... TraceArtifacts:[{Kind:REQ ID:REQ-DRY-001 VersionHash:sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}] ValidationLogs:map[validation_001:] ... StagedFiles:[tracked.txt] ...}
--- FAIL: TestRunRejectsTrackedPathListedOnlyAsAllowedNew (0.05s)
```

### New path listed only as allowed-modified RED

Before the fix, a true new file authorized only via `allowed_modified_files` reached the engine and committed successfully:

```text
=== RUN   TestRunRejectsNewPathListedOnlyAsAllowedModified
    run_test.go:152: exit code = 0, want 3; report={Status:SUCCESS ... GitDiff:diff --git a/new.txt b/new.txt ... TraceArtifacts:[{Kind:REQ ID:REQ-DRY-001 VersionHash:sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}] ValidationLogs:map[validation_001:] ... StagedFiles:[new.txt] ...}
--- FAIL: TestRunRejectsNewPathListedOnlyAsAllowedModified (0.05s)
```

These RED probes proved the combined-boundary behavior: each allowlist could authorize the other class of mutation.

---

## 4. GREEN Implementation

Implementation details:

- Added `validateAllowlistDisjoint(...)` in `internal/contracts/payload.go` so pure payload validation rejects overlap between the two allowlists.
- Added `failWrongClassAllowlistPaths(...)` in `internal/pipe/run.go` after target branch preparation and clean preflight, before `pre_engine_hash` snapshot and before engine execution.
- Added `isTrackedPath(...)` using bounded Git plumbing:

```text
git ls-files -- <path>
```

- Wrong-class paths fail closed with bounded errors:
  - `allowed_modified_files path is not tracked before engine execution`
  - `allowed_new_files path is already tracked before engine execution`
- Updated V47 success test fixture for target-branch orphan behavior: a file created on a new orphan branch is authorized through `allowed_new_files`, not `allowed_modified_files`.
- Updated BLK-010 to replace combined-boundary language with strict tracked/new semantics and to state wrong-class authorization fails before engine execution.

---

## 5. GREEN Focused Test Evidence

Payload/contract focused gate:

```text
go test ./internal/contracts -run 'Allowlist|Allowed' -v
=== RUN   TestPayloadValidateRejectsOverlappingModifiedAndNewAllowlists
--- PASS: TestPayloadValidateRejectsOverlappingModifiedAndNewAllowlists (0.00s)
...
PASS
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
```

Run-level focused gate:

```text
go test ./internal/pipe -run 'AllowedNew|AllowedModified|Allowlist|Success' -v
=== RUN   TestRunRejectsTrackedPathListedOnlyAsAllowedNew
--- PASS: TestRunRejectsTrackedPathListedOnlyAsAllowedNew (0.02s)
=== RUN   TestRunRejectsNewPathListedOnlyAsAllowedModified
--- PASS: TestRunRejectsNewPathListedOnlyAsAllowedModified (0.01s)
=== RUN   TestRunSuccessCommitsAllowedModification
--- PASS: TestRunSuccessCommitsAllowedModification (0.05s)
=== RUN   TestRunSuccessAllowedNewFileMode0644Commits
--- PASS: TestRunSuccessAllowedNewFileMode0644Commits (0.04s)
=== RUN   TestRunAllowedNewFileWithGroupWritableUmaskSucceeds
--- PASS: TestRunAllowedNewFileWithGroupWritableUmaskSucceeds (0.04s)
=== RUN   TestRunSuccessAllowedNewExecutableFileMode0755Commits
--- PASS: TestRunSuccessAllowedNewExecutableFileMode0755Commits (0.04s)
PASS
ok  	github.com/camcamcami/BLK-System/internal/pipe	0.819s
```

Whole Go gate:

```text
go test ./...
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	0.058s
ok  	github.com/camcamcami/BLK-System/internal/contracts	0.042s
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	6.924s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)
```

Python discovery remained green:

```text
python3 -m unittest discover -s python -p 'test_*.py'
.........................................................................................................................
----------------------------------------------------------------------
Ran 121 tests in 0.677s

OK
```

---

## 6. Broad Staging / Diff Safety Evidence

Search evidence:

```text
search internal/pipe for "git add .", "git add -u", "git stash" -> 0 matches
search internal/gitguard for "git add .", "git add -u", "git stash" -> only documentation comment: "staging forms such as git add . or git add -u are intentionally not used."
```

Report diff generation remains two-dot explicit from `pre_engine_hash` to `HEAD`:

```go
runGit(repo, "diff", preEngineHash, "HEAD", "--")
runGit(repo, "diff", preEngineHash, "HEAD", "--numstat", "--")
```

No triple-dot report diff, broad staging, or stash behavior was introduced.

---

## 7. Shared Verification

Final shared verification before commit:

```text
python3 -m unittest discover -s python -p 'test_*.py' -> Ran 121 tests, OK

go test ./... -> PASS

go vet ./... -> PASS

go run ./cmd/blk-pipe --health -> {"status":"OK","component":"blk-pipe"}

git diff --check -> PASS
```

Post-test cleanup:

```text
python/__pycache__/ removed before committing.
```

---

## 8. Authority / Safety Boundary

Task 3 did not run or enable:

- live Codex;
- live tactical LLM APIs;
- network model services;
- cyber tooling or cyber execution;
- live BLK-test MCP;
- live MCP transport;
- authoritative BLK-test verdict authority;
- authoritative BEO publication;
- RTM generation;
- RTM drift authority;
- sandbox/container/cgroup/VM enforcement;
- production approval-channel mechanics;
- active BLK-req vault reads or requirement-body parsing.

The change only hardens deterministic local BLK-pipe payload validation and repository-state authorization before local engine execution.

---

## 9. Remaining Sprint 008 Work

Task 3 closes D-003 only. Remaining Sprint 008 tasks still own:

- Task 4 / D-004: no-candidate gate before validation;
- Task 5 / D-005 through D-009: BLK-004/BLK-010 current-state decision overlay;
- Task 6: sprint closeout and hostile self-review.
