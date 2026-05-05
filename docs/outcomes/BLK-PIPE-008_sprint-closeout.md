# BLK-pipe Sprint 008 — Sprint Closeout

**Status:** Complete
**Date:** 2026-05-05
**Sprint:** BLK-PIPE-008 — BLK-004 Unsafe Gap Closure and Decision Register
**Final task-line commit before closeout:** `0bd74f0 docs: record blk-004 current-state decisions`
**Remote:** pushed to `origin/main` after closeout verification

---

## 1. Objective

Sprint 008 closed the unsafe/non-clean BLK-004 deviation findings from `docs/reviews/BLK-004_hostile-deviation-review.md` by combining deterministic BLK-pipe/BLK-test hardening with explicit current-state doctrine decisions.

The sprint did not treat BLK-004 as accidental or obsolete. BLK-004 remains intentional V47/BLK-pipe authority context. The sprint either fixed unsafe behavior physically or documented accepted local compatibility/hardening overlays so future implementers do not infer policy from stale examples or old probe output.

---

## 2. Task Outcome Links

| Task | Scope | Commit | Outcome |
|---:|---|---|---|
| 1 | Enforce non-empty canonical trace artifacts for execute payloads | `c349d89 fix: require trace artifacts for blk-pipe execute payloads` | [`BLK-PIPE-008_task-001-outcome.md`](BLK-PIPE-008_task-001-outcome.md) |
| 2 | Harden BLK-test handoff fixture trace validation | `1a83330 fix: validate canonical trace hashes in blk-test handoffs` | [`BLK-PIPE-008_task-002-outcome.md`](BLK-PIPE-008_task-002-outcome.md) |
| 3 | Enforce strict tracked/new allowlist semantics | `dc710a8 fix: enforce tracked and new allowlist semantics` | [`BLK-PIPE-008_task-003-outcome.md`](BLK-PIPE-008_task-003-outcome.md) |
| 4 | Move no-candidate diff gate before validation | `d00db7a fix: gate validation on engine candidate diff` | [`BLK-PIPE-008_task-004-outcome.md`](BLK-PIPE-008_task-004-outcome.md) |
| 5 | Add BLK-004 current-state overlay and decision documentation | `0bd74f0 docs: record blk-004 current-state decisions` | [`BLK-PIPE-008_task-005-outcome.md`](BLK-PIPE-008_task-005-outcome.md) |

---

## 3. Final Decision Register

| Decision | Final adopted decision | Closeout status |
|---|---|---|
| DEC-001 | `execute` payloads require non-empty canonical `trace_artifacts`; `revert` and `--health` do not. | Physically enforced and documented. |
| DEC-002 | BLK-test PASS/FAIL handoff fixtures require non-empty canonical trace artifacts. BLOCKED may preserve explicit trace absence only as non-authoritative blocked evidence. | Physically enforced and documented. |
| DEC-003 | `allowed_modified_files` and `allowed_new_files` are strict tracked/new authorization classes. Wrong-class paths fail closed before engine execution. | Physically enforced and documented. |
| DEC-004 | Validation commands run only after the engine produces a candidate mutation. | Physically enforced and documented. |
| DEC-005 | Current local health output remains `{"status":"OK","component":"blk-pipe"}`; BLK-004's older `{"status":"healthy"}` literal is superseded for the current local CLI contract. | Accepted/documented compatibility overlay. |
| DEC-006 | BLK-004 source segments are preserved with a current-state overlay and corrected current examples, not wholesale rewritten. | Accepted/documented preservation policy. |
| DEC-007 | Local exit codes 6/7/9 remain accepted BLK-System local V47-compatible extensions. | Accepted/documented compatibility extension. |
| DEC-008 | Stronger ignored-file cleanup remains accepted hardening; cleanup paths may delete ignored-file residue. | Accepted/documented hardening extension. |
| DEC-009 | Legacy migration payload fields and additional report fields remain accepted compatibility/evidence extensions. | Accepted/documented compatibility/evidence extension. |

---

## 4. RED/GREEN Summary by Finding

| Finding | Old unsafe/non-clean behavior | Sprint 008 closeout state |
|---|---|---|
| D-001 | A successful governed `execute` could produce `trace_artifacts: []`. | Empty/missing execute trace rejects before engine execution as `INVALID_PAYLOAD`; `revert` remains trace-optional. |
| D-002 | BLK-test PASS/FAIL handoff fixture accepted noncanonical trace hashes. | PASS/FAIL require non-empty canonical trace artifacts; malformed uppercase/short/nonhex/non-object entries reject. BLOCKED validates supplied traces and records explicit trace absence only when source failure lacked decoded trace metadata. |
| D-003 | `allowed_new_files` could authorize modification of an already tracked file. | `allowed_modified_files` and `allowed_new_files` are strict tracked/new classes. Overlap and wrong-class paths fail closed before engine execution. |
| D-004 | Validation could run before proving the engine produced a candidate diff. | Engine no-candidate success fails before validation; `validation_logs` remains `{}` and no commit is created. |
| D-005 | BLK-004 health literal differed from current local output. | Current local health output `{"status":"OK","component":"blk-pipe"}` is explicitly accepted/documented. |
| D-006 | BLK-004 examples/source segments lacked later trace/current-disabled overlays. | BLK-004 now has a top current-state overlay plus corrected deterministic local execute example with canonical `trace_artifacts`; source segments remain preserved authority context. |
| D-007 | Local extension exit codes 6/7/9 extend BLK-004's strict 0-5 router. | Documented as accepted BLK-System local V47-compatible extension. |
| D-008 | Cleanup uses stronger ignored-file cleanup than BLK-004's literal `git clean -fd`. | Documented as accepted hardening; operators are warned cleanup paths may delete ignored-file residue. |
| D-009 | Legacy payload/report fields extend BLK-004 schema. | Documented as accepted migration/evidence extension that does not weaken deterministic transport constraints. |

---

## 5. Physical Probe Outputs

Task 6 hostile probes were rerun after Task 5 and before this closeout document was committed.

```text
=== RUN   TestRunRejectsTrackedPathListedOnlyAsAllowedNew
--- PASS: TestRunRejectsTrackedPathListedOnlyAsAllowedNew (0.03s)
=== RUN   TestRunRejectsNewPathListedOnlyAsAllowedModified
--- PASS: TestRunRejectsNewPathListedOnlyAsAllowedModified (0.05s)
=== RUN   TestRunRejectsExecuteWithoutTraceArtifactsBeforeEngine
--- PASS: TestRunRejectsExecuteWithoutTraceArtifactsBeforeEngine (0.04s)
=== RUN   TestRunSkipsValidationWhenEngineProducesNoCandidateDiff
--- PASS: TestRunSkipsValidationWhenEngineProducesNoCandidateDiff (0.04s)
PASS
ok  	github.com/camcamcami/BLK-System/internal/pipe	0.171s
PROBE_HANDOFF_UPPERCASE_HASH_REJECTED ValueError trace_artifacts.version_hash must match sha256:<64-lowercase-hex>
BLK004_CURRENT_STATE_OVERLAY_PASS
{"status":"OK","component":"blk-pipe"}
```

Probe label mapping:

| Required probe | Evidence above |
|---|---|
| `PROBE_EMPTY_TRACE_EXECUTION_REJECTED` | `TestRunRejectsExecuteWithoutTraceArtifactsBeforeEngine` passed. |
| `PROBE_HANDOFF_UPPERCASE_HASH_REJECTED` | Python fixture probe printed `PROBE_HANDOFF_UPPERCASE_HASH_REJECTED ValueError ... sha256:<64-lowercase-hex>`. |
| `PROBE_ALLOWED_NEW_TRACKED_MODIFICATION_REJECTED` | `TestRunRejectsTrackedPathListedOnlyAsAllowedNew` passed. |
| `PROBE_ALLOWED_MODIFIED_NEW_FILE_REJECTED` | `TestRunRejectsNewPathListedOnlyAsAllowedModified` passed. |
| `PROBE_ZERO_DIFF_VALIDATION_SKIPPED` | `TestRunSkipsValidationWhenEngineProducesNoCandidateDiff` passed. |
| `BLK004_CURRENT_STATE_OVERLAY_PASS` | Overlay gate printed `BLK004_CURRENT_STATE_OVERLAY_PASS`. |

Positive regression guard for success paths:

```text
=== RUN   TestRunSuccessReportsTraceArtifacts
--- PASS: TestRunSuccessReportsTraceArtifacts (0.04s)
=== RUN   TestRunSuccessAllowedNewFileMode0644Commits
--- PASS: TestRunSuccessAllowedNewFileMode0644Commits (0.04s)
PASS
ok  	github.com/camcamcami/BLK-System/internal/pipe	0.087s
```

This proves tracked modifications with canonical trace evidence and true-new allowed file creation remain viable while wrong-class allowlist use is rejected.

---

## 6. Full Verification Output

Final verification before closeout commit:

```text
python3 -m unittest discover -s python -p 'test_*.py'
.........................................................................................................................
----------------------------------------------------------------------
Ran 121 tests in 0.651s

OK

go test ./...
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	6.858s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)

go vet ./... -> PASS

go run ./cmd/blk-pipe --health -> {"status":"OK","component":"blk-pipe"}

git diff --check -> PASS

OUTCOME_REMOTE_METADATA_PASS
```

Post-test cleanup requirement:

```text
python/__pycache__/ removed before final status/commit.
```

---

## 7. Explicit Non-Authorization Statement

Sprint 008 did not run, enable, authorize, or imply:

- live Codex;
- live tactical LLM APIs;
- network model services;
- cyber tooling or cyber execution;
- live BLK-test MCP;
- live MCP client transport;
- authoritative BLK-test verdict authority;
- authoritative BEO publication;
- RTM generation;
- RTM drift rejection authority;
- full sandbox/container/cgroup/VM enforcement;
- production host-secret isolation claims;
- production approval-channel mechanics;
- active BLK-req vault reads or requirement-body parsing.

The current disabled-live boundary remains: live Codex, live BLK-test MCP, authoritative BEO publication, and RTM generation remain disabled unless later active doctrine explicitly authorizes them.

---

## 8. Remaining Deferred Items

No Sprint 008 unsafe gap remains open. Deferred work is intentionally outside Sprint 008 scope:

1. Any executable `codex-live` path requires a future sprint with explicit approval mechanics, sandbox/capability decisions, secret/network policy, and verification.
2. Live BLK-test MCP, authoritative BLK-test verdict authority, authoritative BEO publication, RTM generation, and RTM drift rejection remain future work.
3. Full sandbox/container/cgroup/VM enforcement and production host-secret isolation remain future infrastructure work.
4. External strict V47 compatibility mode for health output or exit-code normalization may be added later if required, but current local BLK-System behavior is explicitly documented.

---

## 9. Acceptance Criteria Status

Sprint 008 meets all acceptance criteria in the plan:

- execute without non-empty canonical trace cannot reach engine execution;
- valid revert remains trace-optional;
- BLK-test PASS/FAIL handoff fixtures reject malformed trace artifacts;
- BLOCKED paths do not launder malformed trace artifacts;
- tracked files cannot be authorized solely by `allowed_new_files`;
- new files cannot be authorized solely by `allowed_modified_files`;
- true-new file creation and tracked modification success paths still pass;
- validation does not run when the engine produced no candidate diff;
- current health output is explicitly accepted/documented;
- BLK-004 contains the current-state overlay;
- no new live execution, BLK-test, BEO publication, or RTM authority was added;
- full verification passed;
- Python cache was removed before commit;
- task outcomes and this sprint closeout exist;
- repository was pushed only after verification.
