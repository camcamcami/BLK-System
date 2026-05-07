# BLK-SYSTEM-020 — Post-Remediation Hostile Self-Review

**Status:** PASS — sprint scope accepted
**Date:** 2026-05-07T20:47:00+10:00
**Reviewer:** Hermes deterministic local hostile review
**Source plan:** `docs/plans/blk-system-020_validation-command-profile-tightening.md`

---

## 1. Hostile Review Verdict

BLK-SYSTEM-020 passes hostile self-review for its planned scope.

The sprint reduced validation-command ambiguity by adding repository-owned named `validation_profiles`, fail-closed payload checks, resolved-command report evidence, BLK-pipe execution wiring, Python adapter compatibility, and active BLK-004 doctrine gates.

No reviewed change grants production BLK-test MCP, new live BLK-test smoke authority, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, or broad source mutation outside exact allowlists.

---

## 2. Checklist Review

### 2.1 Does any code path still treat payload-provided arbitrary shell as preferred future/autonomous validation authority?

**PASS with transitional caveat.** Legacy `validation_commands` still exists for trusted-local compatibility, but Sprint 020 tests and BLK-004 doctrine explicitly label it as `transitional trusted-local compatibility`. Less-trusted/autonomous payload boundaries must use `validation_profiles` or a later explicit human-reviewed doctrine exception.

Evidence:

- `internal/contracts/payload_test.go` includes `TestDecodePayloadLegacyValidationCommandsAreTrustedLocalCompatibilityOnly`.
- `docs/BLK-004_blk-pipe-v47-architecture-suite.md` states free-form `validation_commands` are transitional trusted-local compatibility only.

### 2.2 Are `validation_profiles` resolved only from repository-owned command arrays?

**PASS.** Profile names resolve through `internal/validationprofiles`. The registry is repository-owned and returns defensive copies. No caller-provided command text is interpolated into profile resolution.

Evidence:

- `internal/validationprofiles/profiles.go`
- `internal/validationprofiles/profiles_test.go`

### 2.3 Are unknown, duplicate, or mixed profile/command requests rejected fail-closed before engine execution?

**PASS.** The payload contract rejects:

- unknown profiles such as `curl-production`;
- duplicate profile names;
- mixed `validation_profiles` and `validation_commands`.

Evidence:

- `TestDecodePayloadRejectsUnknownValidationProfile`
- `TestDecodePayloadRejectsDuplicateValidationProfile`
- `TestDecodePayloadRejectsMixedValidationProfilesAndCommands`
- Python adapter local mixed-source rejection test

### 2.4 Does BLK-pipe report exact resolved commands for profile-based validation?

**PASS.** Reports include:

```text
validation_command_source
validation_profiles
resolved_validation_commands
validation_logs
```

Evidence:

- `internal/contracts/report.go`
- `TestReportMarshalIncludesValidationProfileEvidence`
- `TestRunValidationProfileExecutesResolvedCommandsAndReportsEvidence`

### 2.5 Did validation failure routing remain `SYNTAX_GATE_FAILED` with cleanup/revert semantics intact?

**PASS.** Profile-mode validation failure is covered by a hermetic temp Go module. A failing `go-test` profile returns `SYNTAX_GATE_FAILED` / Exit 2, restores `HEAD` to the pre-engine hash, restores `README.md`, and leaves the repo clean.

Evidence:

- `TestRunValidationProfileFailureRoutesToSyntaxGateAndCleans`
- Existing validation failure and cleanup tests still pass under `go test ./...`.

### 2.6 Did protected BLK-req vault allowlist rejection remain Exit 3 / unauthorized mutation and body-isolated?

**PASS.** Sprint 020 did not change protected path classifiers. The existing protected-vault tests remained green in full verification.

Evidence:

- `TestPayloadDecodeProtectedPathsStillFailForLegacyAndV47Allowlists`
- `TestPayloadValidateRejectsInvalidPayloads` protected BLK-req cases
- BLK-004 / BLK-006 doctrine gates remain green.

### 2.7 Did Python adapter support remain a convenience layer rather than final authority?

**PASS.** Python adapter support only controls emitted payload fields and local mixed-source refusal. Go payload validation and BLK-pipe execution remain final authority. BLK-004 now states: `Go remains the enforcement authority`.

Evidence:

- `python/blk_pipe_adapter.py`
- `python/test_blk_pipe_adapter.py`
- `python/test_active_doctrine_review_gates.py`

### 2.8 Did the sprint avoid forbidden live/future authorities?

**PASS.** The sprint did not run Hindsight, Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, arbitrary shell as BLK-test behavior, authoritative BEO publication, RTM generation, or drift authority.

The only command execution was local deterministic verification (`go test`, `go vet`, Python `unittest`, and Git).

### 2.9 Are follow-up candidates separated cleanly?

**PASS.** Follow-ups remain separate:

- BLK-SYSTEM-021 Python adapter policy-layer hardening (BLK-024 Track E);
- BEB generator/profile migration for remaining trusted-local producers that emit `validation_commands`;
- later explicit removal or stricter gating of legacy free-form validation commands after approved producers migrate.

---

## 3. BLK-001 through BLK-006 Review

| Governing doc | Verdict | Notes |
| --- | --- | --- |
| BLK-001 | PASS | Separation between BLK-pipe mutation and BLK-test/BEO/RTM authority remains intact. |
| BLK-002 | PASS | No requirement/use-case staging, promotion, active-vault read, or protected body access was introduced. |
| BLK-003 | PASS | Validation profile reporting improves hostile-audit evidence without changing BEB, BLK-test, BEO, or RTM authority. |
| BLK-004 | PASS | Current-state overlay now captures `validation_profiles`, resolved command evidence, compatibility limits, and Go enforcement authority. |
| BLK-005 | PASS | No requirement schema or trace-baton weakening. Trace artifacts remain opaque hash metadata. |
| BLK-006 | PASS | Protected-vault hard-deny remains enforced; profile code does not access protected bodies. |

---

## 4. Verification Evidence

Final verification commands:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
git status --short --branch
```

Observed verification summary before closeout doc creation:

```text
ok      github.com/camcamcami/BLK-System/cmd/blk-pipe    (cached)
ok      github.com/camcamcami/BLK-System/internal/contracts    (cached)
ok      github.com/camcamcami/BLK-System/internal/engine    0.133s
ok      github.com/camcamcami/BLK-System/internal/execguard    9.009s
ok      github.com/camcamcami/BLK-System/internal/gitguard    1.081s
ok      github.com/camcamcami/BLK-System/internal/pipe    7.575s
ok      github.com/camcamcami/BLK-System/internal/runtimeguard    (cached)
ok      github.com/camcamcami/BLK-System/internal/testutil    0.143s
ok      github.com/camcamcami/BLK-System/internal/validation    0.172s
ok      github.com/camcamcami/BLK-System/internal/validationprofiles    (cached)
Ran 316 tests in 6.476s
OK
```

---

## 5. Residual Risks / Follow-Ups

1. Legacy `validation_commands` remains available for trusted-local compatibility. This is accepted for Sprint 020 but must not become future less-trusted/autonomous authority.
2. Python adapter policy-layer hardening remains a separate BLK-024 Track E sprint.
3. Any BEB/profile producer migration should be planned separately and should not silently remove compatibility until approved producers are identified.

---

## 6. Non-Execution Statement

This hostile self-review did not invoke Hindsight, Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads/copying/parsing/hashing/mutation, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, or source mutation outside exact approved allowlists.

---

## 7. Final Verdict

BLK-SYSTEM-020 is accepted for sprint scope. Validation authority is now less shell-shaped at future BLK-native boundaries, profile requests fail closed where required, profile execution is auditable, and active doctrine preserves Go-side enforcement authority.
