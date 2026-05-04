# BLK-pipe Sprint 003 — Task 1 Outcome

**Status:** Complete
**Date:** 2026-05-04
**Task:** Freeze and Enforce Protected BLK-req Vault Paths
**Implementation Commit:** `ca4bdc6 fix: protect shared blk-req active vault paths`
**Remote:** pushed to `origin/main`
**Plan:** `docs/plans/BLK-PIPE-003_integration-readiness-and-capability-profiles.md`

---

## 1. Objective

Task 1 defensively resolved the BLK-001 `/docs/active/` ambiguity by extending BLK-pipe allowlist denial to every active BLK-req vault candidate path currently named by doctrine or historical planning.

BLK-001 says BLK-req outputs immutably hashed Markdown files into `/docs/active/` and that tactical agents are physically locked out of BLK-req baselines. Existing BLK-pipe validation already rejected type-specific BLK-req vault layouts under `docs/requirements/` and `docs/use_cases/`. This task adds the shared active-vault candidate `docs/active/` to the same deterministic deny rule.

The implementation intentionally does **not** block all `docs/` paths. Documentation-only sprint work may still allowlist legitimate non-vault paths such as `docs/plans/` and `docs/outcomes/` when authorized by a sprint controller.

---

## 2. Files Changed

Implementation commit:

```text
ca4bdc6 fix: protect shared blk-req active vault paths
 docs/BLK-010_blk-pipe-v47-hardening-cli.md         |  4 ++-
 ...K-011_blk-pipe-cyber-readiness-and-usability.md |  2 ++
 internal/contracts/payload.go                      |  5 ++-
 internal/contracts/payload_test.go                 | 40 ++++++++++++++++++++++
 internal/pipe/run_test.go                          | 10 ++++++
 5 files changed, 59 insertions(+), 2 deletions(-)
```

Changed files:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/pipe/run_test.go`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md`

---

## 3. Behavior Implemented

### 3.1 Shared active vault denial

`internal/contracts/payload.go` now treats these prefixes as protected BLK-req vault/artifact paths during allowlist validation:

```text
docs/active/
docs/requirements/
docs/use_cases/
```

Any `allowed_modified_files` or `allowed_new_files` entry under those prefixes returns an invalid-payload validation error before BLK-pipe reaches engine execution.

### 3.2 Prefix-specific error context

`protectedDocsPrefix` now returns `docs/active`, `docs/requirements`, or `docs/use_cases` so reports identify the protected vault class that caused rejection.

For `docs/active/` inputs, the existing error style produces substrings such as:

```text
protected docs/active path
```

### 3.3 Non-vault documentation paths remain valid

`TestPayloadValidateAllowsNonProtectedDocsPaths` now proves that non-protected documentation paths remain valid allowlist entries:

```text
docs/plans/BLK-PIPE-003_integration-readiness-and-capability-profiles.md
docs/outcomes/BLK-PIPE-003_task-001-outcome.md
```

This preserves Sprint 003's requirement not to broaden denial to all `docs/` paths.

### 3.4 Documentation updated

`docs/BLK-010_blk-pipe-v47-hardening-cli.md` now states that allowlist entries must not target protected BLK-req vault/artifact paths under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`. It also explains that `docs/active/` is blocked defensively because BLK-001 names the active BLK-req vault while doctrine path conventions are still being frozen.

`docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md` now gives operator-facing guidance that BLK-req active vault candidates are repository-law paths, not tactical execution targets, and that BLK-req artifact revisions must use the HITL/staged revision path rather than direct tactical mutation.

---

## 4. TDD Evidence

### 4.1 RED

The implementation subagent first added failing tests before changing production validation. Expected failures were observed:

```text
go test ./internal/contracts -run 'TestPayload.*Protected|TestPayload.*Invalid|TestPayloadDecode' -v

TestPayloadDecodeProtectedPathsStillFailForLegacyAndV47Allowlists/...active_vault_path:
DecodePayload() error = nil, want non-nil

TestPayloadValidateRejectsInvalidPayloads/protected_BLK-req_active_vault_modified_path:
Validate() error = nil, want non-nil

TestPayloadValidateRejectsInvalidPayloads/protected_BLK-req_active_vault_new_path:
Validate() error = nil, want non-nil
```

The pipe-level regression also failed before the production change:

```text
go test ./internal/pipe -run 'TestRunRejectsDocsActive|TestRunProtected|TestRun.*InvalidPayload' -v

TestRunProtectedDocsAllowlistRejectsBeforeEngine/modified_active_vault_artifact
TestRunProtectedDocsAllowlistRejectsBeforeEngine/new_active_vault_artifact

Observed failure shape:
exit code = 3, want 2
```

That RED failure proved `docs/active/` was not rejected at payload-validation time and the engine path could still be reached.

### 4.2 GREEN

Final focused verification passed after adding `docs/active/` to the protected prefix logic:

```text
gofmt -l internal/contracts/payload.go internal/contracts/payload_test.go internal/pipe/run_test.go
# no output

go test ./internal/contracts -run 'TestPayload.*Protected|TestPayload.*Invalid|TestPayloadDecode' -v
PASS

go test ./internal/pipe -run 'TestRunRejectsDocsActive|TestRunProtected|TestRun.*InvalidPayload' -v
PASS

go test ./...
PASS

go vet ./...
PASS

git diff --check HEAD^ HEAD
PASS
```

---

## 5. Review Results

Task 1 used the required two-stage review loop after the implementation commit.

### 5.1 Spec-compliance review

Result:

```text
PASS
```

The reviewer confirmed:

- `docs/active/` is rejected in both modified and new allowlists.
- `docs/requirements/` and `docs/use_cases/` protections are preserved.
- Engine execution is not reached for protected allowlist entries.
- Legitimate non-vault docs paths are not accidentally blocked.
- The documentation explains the defensive BLK-001 path-convention stance.

### 5.2 Code-quality/security review

Result:

```text
APPROVED
```

The reviewer found no critical, important, or minor issues. It confirmed:

- the implementation is narrow, deterministic, and idiomatic,
- tests cover legacy and V47 payload shapes, modified/new allowlists, pre-engine rejection, and non-protected docs paths,
- documentation does not overclaim sandbox, host-secret isolation, live LLM, Codex, or cyber-execution capability,
- hardening invariant greps passed for broad Git staging, direct production Git command construction, and triple-dot diff additions.

---

## 6. Final Verification Evidence

Controller verification before pushing the implementation commit:

```text
export PATH="$HOME/.local/bin:$PATH"

gofmt -l internal/contracts/payload.go internal/contracts/payload_test.go internal/pipe/run_test.go
# no output

go test ./internal/contracts -run 'TestPayload.*Protected|TestPayload.*Invalid|TestPayloadDecode' -v
PASS

go test ./internal/pipe -run 'TestRunRejectsDocsActive|TestRunProtected|TestRun.*InvalidPayload' -v
PASS

go test ./...
PASS

go vet ./...
PASS

! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go'
PASS

! git grep -n -E 'exec\.Command(Context)?\("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
PASS

! git grep -n -E 'git[^\n]*diff[^\n]*\.\.\.' -- '*.go' ':!*_test.go' docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md docs/plans/BLK-PIPE-003_integration-readiness-and-capability-profiles.md
PASS

git diff --check HEAD^ HEAD
PASS
```

Push result:

```text
git push origin main
origin/main updated from d569e73 to ca4bdc6

git status --short --branch
## main...origin/main
```

---

## 7. Safety Invariants Preserved

- No live Codex invocation.
- No live tactical LLM execution.
- No cyber execution.
- No broad `docs/` allowlist denial.
- No production `git add .`.
- No production `git add -u`.
- Existing protected BLK-req denials for `docs/requirements/` and `docs/use_cases/` are preserved.
- BLK-pipe remains a deterministic transport and repository blast shield, not a BLK-req authoring path or architecture decision-maker.

---

## 8. Deviations / Notes

No deviations from Task 1 scope.

The only deliberate addition beyond the literal RED snippets was a positive contract regression for non-protected docs paths. That was included to satisfy the Task 1 review focus: legitimate documentation paths outside active BLK-req vaults must not be accidentally blocked.

---

## 9. Next Task

Proceed to Sprint 003 Task 2: add opaque trace artifact hash baton fields so BLK-pipe can preserve BLK-001 trace/hash metadata across payload/report and Python adapter boundaries without interpreting architecture semantics.
