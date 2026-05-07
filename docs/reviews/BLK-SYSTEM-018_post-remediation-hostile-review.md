# BLK-SYSTEM-018 — Post-Remediation Hostile Review

**Status:** Complete
**Date:** 2026-05-07T17:54:25+10:00
**Repository:** `/home/dad/BLK-System`
**Source review:** `docs/reviews/BLK-SYSTEM_current-implementation_BLK-001-through-BLK-006_hostile-alignment-review.md`
**Reviewed remediation commits:** `c47dba2`, `21f37f4`, `2edbd15`, `a12fb7a`, `ddd4203`

---

## 1. Verdict

BLK-SYSTEM-018 remediated the two implementation blockers owned by the sprint.

- `BLOCKING-1` is fixed: protected BLK-req vault allowlist hits now route as `UNAUTHORIZED_FILE_MUTATION` / POSIX Exit 3.
- `BLOCKING-2` is fixed: verified `revert` reaches the emergency reset/clean path before execute-mode clean preflight rejects dirty residue.
- `BLOCKING-3` remains out of scope and is still assigned to `BLK-SYSTEM-019` for doctrine cleanup around BLK-020 first-smoke authority.

No evidence in this sprint introduced live BLK-test MCP authority, authoritative BEO publication, RTM generation, RTM drift rejection authority, cyber tooling, network model services, or protected BLK-req vault body reads.

---

## 2. Hostile Checks

### 2.1 Protected vault allowlist hits now return Exit 3 and `UNAUTHORIZED_FILE_MUTATION`

**Result:** PASS.

Evidence:

```text
go test ./internal/pipe -run 'TestRunProtectedVaultAllowlist' -count=1 -v
--- PASS: TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation
```

The regression table covers protected paths under:

```text
docs/active/
docs/requirements/
docs/use_cases/
```

### 2.2 Ordinary malformed payloads still return Exit 2 / `INVALID_PAYLOAD`

**Result:** PASS.

Evidence:

```text
go test ./internal/contracts ./internal/pipe -count=1
ok  	github.com/camcamcami/BLK-System/internal/contracts
ok  	github.com/camcamcami/BLK-System/internal/pipe
```

The production change only special-cases partially decoded payloads whose allowlists contain protected BLK-req vault paths. Generic decode/validation errors without protected allowlist entries remain on `INVALID_PAYLOAD` / Exit 2.

### 2.3 Protected vault body reads are not introduced

**Result:** PASS.

Evidence:

- `internal/contracts.HasProtectedDocsAllowlistEntry(...)` inspects only `Payload.AllowedModifiedFiles` and `Payload.AllowedNewFiles` strings.
- `internal/pipe.parseAndValidatePayload(...)` uses only the partially decoded payload strings and formats an error message containing field, entry, and prefix.
- No `os.ReadFile`, `os.Open`, hashing, parsing, or filesystem stat was added to classify protected allowlist entries.

### 2.4 Engine execution does not start for protected allowlist hits

**Result:** PASS.

Evidence:

`TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation` uses a sentinel engine command that would write `engine-ran.txt`; every protected-vault case asserts the sentinel file does not exist and the repo remains clean.

### 2.5 Valid revert can run from dirty/untracked/ignored residue after target validation

**Result:** PASS.

Evidence:

```text
go test ./internal/pipe -run 'TestRunRevert(BypassesCleanPreflight|CleansPreExistingNestedGitRepository|InvalidAnchor|WithTargetBranch|SHA256)' -count=1 -v
--- PASS: TestRunRevertBypassesCleanPreflightForDirtyTrackedWorkspace
--- PASS: TestRunRevertBypassesCleanPreflightForUntrackedAndIgnoredResidue
--- PASS: TestRunRevertBypassesCleanPreflightForEmptyUntrackedDirectory
--- PASS: TestRunRevertCleansPreExistingNestedGitRepositoryAfterValidAnchor
```

### 2.6 Invalid revert anchors still fail and do not reset

**Result:** PASS.

Evidence:

The focused revert gate includes:

```text
TestRunRevertInvalidAnchorDoesNotReset
TestRunRevertSHA256RejectsAbbreviatedFortyHexTarget
TestRunRevertWithTargetBranchRejectsWrongCurrentBranch
```

These confirm invalid branch/hash/ancestry cases do not reset the repository.

### 2.7 Execute-mode clean preflight remains in force

**Result:** PASS.

Evidence:

The production reorder only moves `if payload.Action == "revert" { return runRevert(...) }` above `cleanPreflight(...)`. Non-revert execute payloads still enter `cleanPreflight(...)` before branch prep, engine execution, validation, staging, or commit. Existing execute dirty-preflight tests remain in `go test ./internal/pipe` and full `go test ./...`.

### 2.8 No live BLK-test MCP, BEO publication, or RTM authority was introduced

**Result:** PASS.

Evidence:

Task 005 added persistent active doctrine gates requiring Sprint 018 docs to state:

```text
does not authorize live BLK-test MCP
does not authorize authoritative BEO publication
does not authorize RTM generation
```

No runtime BLK-test MCP, BEO publication, or RTM files were modified by the sprint.

### 2.9 `BLK-SYSTEM-019` remains follow-up owner for BLK-020 doctrine contradiction cleanup

**Result:** PASS.

Evidence:

The Sprint 018 plan explicitly excludes `BLOCKING-3` and identifies `BLK-SYSTEM-019` as the owner. This review preserves that assignment and does not broaden Sprint 018 into doctrine cleanup beyond the Task 005 active boundary notes.

---

## 3. Final Verification

Final verification is recorded in `docs/outcomes/BLK-SYSTEM-018_sprint-closeout.md`.

---

## 4. Non-Execution Statement

This hostile self-review did not invoke Codex or live tactical LLMs, did not call network model services, did not run cyber tooling, did not start production BLK-test MCP, did not read or mutate protected BLK-req vault bodies, did not generate RTM, did not assert RTM drift rejection authority, and did not publish authoritative BEOs.
