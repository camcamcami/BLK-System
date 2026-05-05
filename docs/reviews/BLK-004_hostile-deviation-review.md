# BLK-004 — Hostile Deviation Review

**Status:** Review outcome / deviation register
**Date:** 2026-05-05
**Reviewer:** Hermes
**Scope:** BLK-004 as intentional V47 / BLK-pipe authority, current implementation on `main`, and sprint outcome evidence through BLK-PIPE-007.
**Repository state before review probes:** `## main...origin/main`

---

## 1. Review posture

BLK-004 is treated as a deliberate authority surface, not as casual stale text. A mismatch is not automatically a defect in BLK-004. Each item below is classified as one of:

- **Accepted deviation** — intentionally different and sufficiently documented.
- **Deferred scope** — intentionally postponed by sprint outcome/closeout.
- **Doctrine evolution** — a later active BLK document narrows or qualifies BLK-004 target-state language.
- **Implementation gap** — current code behavior does not satisfy the BLK-004 clause, or a later doctrine tightening that is now required for BLK-004-aligned operation.
- **Review-documentation gap** — behavior may be intentional, but the deviation record is not explicit enough for audit-grade BLK-004 governance.

The hostile standard used here is: if an implementation, fixture, or later doctrine path differs from BLK-004, that difference must have clause evidence, observed behavior evidence, classification, justification, and remediation/no-op rationale.

No Hindsight, live Codex, live tactical LLMs, network model services, cyber tooling, or live BLK-test MCP were used for this review.

---

## 2. BLK-004 authority clauses checked

Key BLK-004 clauses reviewed:

- BLK-pipe is a compiled deterministic transport layer; it does not parse code, call LLM APIs, or make decisions (`docs/BLK-004_blk-pipe-v47-architecture-suite.md:11-14`).
- Hard bans / safeguards: output cap, orphan init, revert ancestry gate, no broad staging, unauthorized erasure, no silent staging, validation reset, no relative revert anchors, no stash, no triple-dot diff, sequential validation, diff summary, signal reaping, environment scrub, bounded Git, headless SSH hardening (`docs/BLK-004...:16-33`).
- Bounded execution sequence: health, action routing, branch isolation, pre-engine snapshot, engine execution, validation, strict staging, commit, rogue-file audit, diff extraction (`docs/BLK-004...:45-85`).
- Payload and report schema, including `TraceArtifacts []TraceArtifact` (`docs/BLK-004...:121-165`).
- Python adapter expectations (`docs/BLK-004...:170-307`).
- CLI and orchestrator payload examples (`docs/BLK-004...:317-382`).

Related current-state doctrine reviewed:

- BLK-010 current V47-compatible developer contract.
- BLK-012 capability profiles and non-authorizations.
- BLK-013 BLK-test handoff fixture contract.
- BLK-014 draft-only BEO fixture shape.
- BLK-015 fail-closed approval / disabled MCP design.
- BLK-016 Sprint 007 disabled adapter / BEO-RTM interface fixture contract.
- Sprint outcomes BLK-PIPE-001 through BLK-PIPE-007.

---

## 3. Executive verdict

**Verdict: conditional pass, not clean.**

The core BLK-004 deterministic transport kernel is mostly honored and, in several places, later sprints strengthened it beyond the original text. The documented hardening includes bounded Git execution, no broad staging, no stash, revert ancestry/full-hash checks, environment scrub, process-group cleanup, direct payload-size bounds, true-new-file success support, disabled live execution boundaries, and draft/fixture-only BLK-test/BEO/RTM contracts.

The non-clean part is that several deviations are either physically present or under-documented:

1. successful BLK-pipe execution can still produce `trace_artifacts: []`;
2. the BLK-test PASS/FAIL handoff fixture still accepts noncanonical trace hashes;
3. `allowed_new_files` proves true-new success but does not enforce new-file exclusivity;
4. the BLK-004 zero-diff gate order differs from implementation behavior;
5. health output differs from BLK-004's literal example;
6. BLK-004 examples/adapter source segment are not annotated with the later trace and current-disabled authority overlays.

None of these should be papered over as “BLK-004 missed something.” They are deviation-register items requiring explicit acceptance, remediation, or current-state overlay documentation.

---

## 4. Hostile deviation register

### D-001 — Successful execute can still carry an empty trace baton

**Severity:** HIGH

**BLK-004 clause / context:**

- BLK-004 payload schema includes `TraceArtifacts []TraceArtifact` (`docs/BLK-004...:123-141`).
- BLK-004 report schema includes `TraceArtifacts []TraceArtifact` (`docs/BLK-004...:154-165`).
- BLK-003 later active flow says Hermes must inject `trace_artifacts` into BEB frontmatter and BEO inheritance (`docs/BLK-003_blk-pipe-blk-test-orchestration.md:81-83`, `:176`).

**Observed behavior:**

Physical probe against current `main`:

```text
PROBE_EMPTY_TRACE_EXECUTION {"exit_code": 0, "process_rc": 0, "staged_files": ["dry_run_output.txt"], "status": "SUCCESS", "trace_artifacts": []}
```

Current implementation evidence:

- `contracts.ValidateTraceArtifacts(...)` validates entries when present but returns success for an empty slice (`internal/contracts/payload.go:215-245`).
- Reports normalize missing/nil trace artifacts to `[]` (`internal/contracts/report.go:35-64`).
- BLK-010 explicitly documents `trace_artifacts` as optional and “May be empty” (`docs/BLK-010_blk-pipe-v47-hardening-cli.md:81`).

**Classification:** Implementation gap if BLK-004 + BLK-001 trace baton is interpreted as mandatory for V47 execute; accepted/documented deviation if BLK-pipe is intentionally allowed to transport legacy/dev-smoke/revert payloads without traces.

**Justification status:** Not yet clean. The optional behavior is documented in BLK-010 and Sprint 003 outcome, but the justification is transport-focused and does not explicitly state when a trace-empty successful execute is allowed under BLK-001/BLK-004 governance.

**Required remediation:** Decide and document one of:

1. enforce non-empty canonical `trace_artifacts` for V47 `execute` payloads, with explicit exemptions for legacy/dev-smoke/revert if required; or
2. add an explicit BLK-004/BLK-010 deviation note that BLK-pipe itself remains trace-optional and that orchestrator/profile/BLK-test layers must enforce trace presence before any BLK-001-governed execution is considered valid.

---

### D-002 — BLK-test PASS/FAIL handoff accepts noncanonical trace hashes

**Severity:** HIGH

**BLK-004 clause / context:**

- BLK-004 names `version_hash` in the trace artifact schema (`docs/BLK-004...:123-127`).
- BLK-013 requires every PASS/FAIL `trace_artifacts[*].version_hash` to match `sha256:<64-lowercase-hex>` (`docs/BLK-013_blk-test-handoff-fixture-contract.md:32-40`).
- BLK-014 and BLK-015 also require canonical trace hashes at later fixture/MCP boundaries (`docs/BLK-014...:10-14`, `docs/BLK-015...:89-95`).

**Observed behavior:**

Physical probe against current `main`:

```text
PROBE_HANDOFF_UPPERCASE_HASH_ACCEPTED sha256:AAAAAAAAAAAAA
PROBE_MCP_UPPERCASE_HASH_REJECTED ValueError trace_artifacts[0].version_hash must match sha256:<64-lowercase-hex>
```

Current code evidence:

- `python/blk_test_handoff_fixtures.py` only checks that `kind`, `id`, and `version_hash` are non-empty before copying them (`python/blk_test_handoff_fixtures.py:154-173`).
- `python/blk_orchestrator_gate.py` performs canonical regex validation (`python/blk_orchestrator_gate.py:333-396`), so the issue is localized to the older handoff fixture path.

**Classification:** Implementation gap against later active fixture doctrine and the intended BLK-004 trace-baton semantics.

**Justification status:** Not justified. It is a leftover weak boundary, not an intentional BLK-004 deviation.

**Required remediation:** Add canonical regex validation to `python/blk_test_handoff_fixtures.py` and negative tests for uppercase, short, nonhex, empty, non-object, and missing trace entries. The fix should preserve BLOCKED source behavior only if it still carries canonical trace artifacts or explicitly records why trace is absent.

---

### D-003 — `allowed_new_files` proves true-new success but does not enforce new-file exclusivity

**Severity:** HIGH/MEDIUM

**BLK-004 clause / context:**

- BLK-004 requires strict iteration through `AllowedModifiedFiles` and `AllowedNewFiles`, with no `git add .` or `git add -u` (`docs/BLK-004...:21`, `:75`).
- Sprint 002 explicitly recorded that allowlist names preserved intent, not separate tracked/new semantics (`docs/outcomes/BLK-PIPE-002_sprint-002-closeout.md:379`).
- Sprint 005 Task 2 fixed true new-file success without placeholder pre-seeding (`docs/outcomes/BLK-PIPE-005_task-002-outcome.md:11-14`, `:51-88`).
- BLK-010 currently says the two allowlists form a combined staging boundary, while `allowed_new_files` proves true new-file execution (`docs/BLK-010...:83-84`).

**Observed behavior:**

Physical probe against current `main`:

```text
PROBE_ALLOWED_NEW_TRACKED_MODIFICATION {"error": "", "exit_code": 0, "process_rc": 0, "staged_files": ["tracked.txt"], "status": "SUCCESS", "trace_artifacts": [{"id": "REQ-DRY-001", "kind": "REQ", "version_hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}]}
```

This means a tracked file modification can be authorized solely by `allowed_new_files`.

Implementation evidence:

- `existingAllowedNewFiles(...)` includes an `allowed_new_files` path if it exists after engine execution; it does not check whether it was tracked before engine execution (`internal/pipe/run.go:533-546`).
- `StageAllowlist(...)` stages both arrays by path without tracked/new differentiation (`internal/gitguard/stage.go:12-27`).

**Classification:** Review-documentation gap unless BLK-004 intended strict new-vs-modified semantics; implementation gap if it did.

**Justification status:** Partially documented, but not clean. Sprint 002 documented combined-boundary semantics. Sprint 005/006 later use “true `allowed_new_files`” phrasing that can be read as exclusivity rather than only true-new success.

**Required remediation:** Decide explicitly:

- If BLK-004 intended **combined explicit path allowlists**, keep current behavior but add an explicit deviation note: `allowed_new_files` proves new-file success but is not an exclusivity gate.
- If BLK-004 intended **strict tracked/new semantics**, add pre-engine tracked-state checks so paths in `allowed_new_files` must be untracked/nonexistent before engine execution, and paths in `allowed_modified_files` must already be tracked when required.

---

### D-004 — Zero-diff gate currently runs after validation, not before validation

**Severity:** MEDIUM

**BLK-004 clause / context:**

- BLK-004 sequence places the zero-diff gate before bounded validation (`docs/BLK-004...:66-72`).
- BLK-004 then stages/commits after validation (`docs/BLK-004...:74-80`).

**Observed behavior:**

Physical probe against current `main` with an engine that made no diff and a validation command that printed a marker:

```text
PROBE_ZERO_DIFF_VALIDATION_ORDER {"error": "engine produced no staged allowlisted diff", "exit_code": 3, "process_rc": 1, "status": "UNAUTHORIZED_FILE_MUTATION", "validation_logs": {"validation_001": "VALIDATION_RAN"}}
```

Implementation evidence:

- Current `run.go` runs validation at `internal/pipe/run.go:172-249`.
- It stages/checks for no staged files later at `internal/pipe/run.go:265-315`.

**Classification:** Implementation sequencing deviation.

**Justification status:** Not explicitly justified. The final status is still fail-closed (`UNAUTHORIZED_FILE_MUTATION`), but validation commands can execute even when the engine produced no candidate diff.

**Required remediation:** Either move a zero-diff/no-candidate check before validation, or explicitly document why validation-before-zero-diff is accepted and why validation side-effect gates are sufficient mitigation.

---

### D-005 — Health-check JSON differs from BLK-004 literal contract

**Severity:** MEDIUM/LOW

**BLK-004 clause / context:**

- BLK-004 says `--health` prints `{"status": "healthy"}` and exits `0` (`docs/BLK-004...:47-49`).

**Observed behavior:**

Current command output:

```text
go run ./cmd/blk-pipe --health
{"status":"OK","component":"blk-pipe"}
```

Implementation evidence:

- `cmd/blk-pipe/main.go:51-53` prints `{"status":"OK","component":"blk-pipe"}`.
- BLK-010 and Sprint 002/006/007 outcomes consistently document the current output as `OK` with `component` (`docs/BLK-010...:37-40`; `docs/outcomes/BLK-PIPE-006_sprint-closeout.md:208`; `docs/outcomes/BLK-PIPE-007_task-005-outcome.md:127`).

**Classification:** Accepted implementation deviation if current CLI consumers rely on `OK`; review-documentation gap because the BLK-004 literal remains unqualified.

**Justification status:** Current output is consistently tested/documented, but the deviation from BLK-004's literal `healthy` string is not called out as a deviation.

**Required remediation:** Either restore BLK-004's exact health shape, or add a BLK-004/BLK-010 compatibility note that `OK`/`component` is the accepted BLK-System local health output.

---

### D-006 — BLK-004 examples and Python source segment lack later trace/current-state overlays

**Severity:** MEDIUM

**BLK-004 clause / context:**

- BLK-004's Python adapter source segment has no `trace_artifacts` argument or result field (`docs/BLK-004...:185-245`, `:288-298`).
- BLK-004's CLI/orchestrator JSON examples omit `trace_artifacts` (`docs/BLK-004...:317-330`, `:352-365`).
- BLK-004 examples show live-looking `engine: "codex"` payloads (`docs/BLK-004...:324-325`, `:359-360`).

**Observed behavior:**

- Current adapter has `trace_artifacts` in `ExecutionResult`, accepts optional `trace_artifacts`, includes it in payload when supplied, and maps it back from the report (`python/blk_pipe_adapter.py:17-33`, `:74-102`, `:169-185`).
- BLK-012/015/016 make current `codex-live`, live BLK-test MCP, BEO publication, and RTM generation disabled/fixture-only (`docs/BLK-012...:13-18`, `docs/BLK-015...:16-18`, `docs/BLK-016...:12-21`).
- Sprint 005 Task 5 explicitly says BLK-004 remains active with historical source segments and was only partially canonicalized (`docs/outcomes/BLK-PIPE-005_task-005-outcome.md:174-180`).

**Classification:** Doctrine evolution plus review-documentation gap.

**Justification status:** Partially justified by Sprint 005 Task 5, but not ideal for future implementers. BLK-004 is active planning doctrine; examples that omit trace artifacts or look live-Codex-capable need a current-state overlay so readers do not treat target-state examples as current authorization.

**Required remediation:** Add a BLK-004 appendix or header overlay rather than rewriting historical source segments wholesale:

- `trace_artifacts` is part of current payload/report contract;
- trace presence policy is decided by D-001;
- `codex` examples are target-state/future-approved examples only;
- current executable profiles are local/fixture-only unless later sprint explicitly authorizes live execution.

---

### D-007 — Local extension exit codes 6/7/9 remain outside BLK-004 strict 0-5 router

**Severity:** LOW/MEDIUM

**BLK-004 clause / context:**

- BLK-004's POSIX router names strict exit-code families `0-5` (`docs/BLK-004...:341-345`).

**Observed behavior:**

- Current Python adapter recognizes local extension codes `6`, `7`, and `9` (`python/blk_pipe_adapter.py:36-58`).
- Sprint 002 closeout records this as a retained local extension (`docs/outcomes/BLK-PIPE-002_sprint-002-closeout.md:379-380`).
- BLK-010 documents Sprint 004's adapter status fidelity decision and the local extension codes (`docs/BLK-010...:171-180`).

**Classification:** Accepted documented deviation.

**Justification status:** Sufficient for current local BLK-System execution because it prevents unknown nonzero failures from being misreported as success while preserving strict V47 family routing.

**Required remediation:** No code change required unless BLK-004 strictness is reasserted. If strict V47 external compatibility is required, add a compatibility mode or collapse local extension codes into the strict families at the CLI boundary.

---

### D-008 — Cleanup uses stronger `git clean -ffdx -q`, not BLK-004's literal `git clean -fd`

**Severity:** LOW/MEDIUM

**BLK-004 clause / context:**

- BLK-004 repeatedly names `git clean -fd` for unauthorized erasure and revert cleanup (`docs/BLK-004...:22`, `:53`, `:59`, `:70-76`).

**Observed behavior:**

- Current workspace/revert cleanup uses stronger ignored-file cleanup (`git clean -ffdx -q`) in key paths (`internal/pipe/run.go:369-375`, `:487-491`).
- Current preflight and residue logic also checks ignored files, empty untracked directories, nested Git dirs, and directory modes (`internal/pipe/run.go:377-419`, `:780-842`).

**Classification:** Implementation hardening deviation.

**Justification status:** Justified as stronger cleanup against ignored-file and nested-repo residue. This is not a regression against BLK-004's safety intent, but it should be recorded as a local strengthening because `-x` deletes ignored files.

**Required remediation:** Document as accepted hardening in BLK-010/BLK-004 overlay if operators need to understand ignored-file deletion behavior.

---

### D-009 — Legacy compatibility fields and extra report fields extend BLK-004's schema

**Severity:** LOW

**BLK-004 clause / context:**

- BLK-004 schema centers V47 fields such as `work_dir`, `engine`/`engine_args`, `l2_packet`, allowlists, and V47 report fields (`docs/BLK-004...:121-165`).

**Observed behavior:**

- Current payload contract still accepts legacy `workdir` and `engine_command`, plus `timeout_seconds` and `max_output_bytes` (`internal/contracts/payload.go:40-55`, `:84-100`, `:131-147`).
- Current report includes extensions such as `commit_hash`, `staged_files`, `destroyed_files`, `engine_exit_code`, and `engine_output_bytes` (`internal/contracts/report.go:12-33`).
- BLK-010 documents the legacy migration fields and stable report extensions (`docs/BLK-010...:86-93`, `:140-165`).

**Classification:** Accepted documented compatibility extension.

**Justification status:** Sufficient. These extensions improve local orchestration/evidence preservation and do not weaken BLK-004's deterministic transport constraints.

**Required remediation:** No immediate change. Keep extensions documented as BLK-System local V47-compatible behavior.

---

## 5. Explicitly documented deferrals / non-deviations

The following are **not** undocumented BLK-004 misses; they are already documented as deferred, blocked, or accepted:

1. **No live Codex / live LLM execution.** Sprint 001/002/004/006/007 outcomes and BLK-012/015/016 keep live execution blocked. This is current-state doctrine evolution, not accidental noncompliance.
2. **No live BLK-test MCP, authoritative BEO publication, or RTM generation.** BLK-013/014/015/016 deliberately keep these disabled/fixture-only.
3. **BLK-pipe is not a full sandbox.** BLK-010/011/012 document that process-group/procfs cleanup is not host-secret isolation or full OS sandboxing.
4. **POSIX-only target.** This matches BLK-004 and is not a deviation.
5. **No broad staging/stash/triple-dot report diff.** Current production implementation uses explicit staging and `git diff <preEngineHash> HEAD --`; no evidence of production broad staging or stash use was found in reviewed code paths.
6. **Revert hardening.** Current implementation is stricter than BLK-004 in requiring a full commit object ID and current-branch assertion before destructive reset.

---

## 6. Recommended remediation package

Recommended follow-up sprint/review slice:

```text
BLK-PIPE-00X — BLK-004 Deviation Register Closure
```

Minimum tasks:

1. Decide trace-empty policy at BLK-pipe execution boundary and either enforce or document explicit exemptions.
2. Fix `python/blk_test_handoff_fixtures.py` canonical trace validation.
3. Decide `allowed_new_files` exclusivity semantics and either enforce tracked/new state or document combined-boundary behavior as an accepted BLK-004 deviation.
4. Decide zero-diff-before-validation ordering and either move the gate or document current ordering.
5. Resolve health output compatibility (`healthy` vs `OK`/`component`).
6. Add a BLK-004 current-state overlay/appendix for trace artifacts, live-Codex non-authorization, health output, extension exit codes, cleanup hardening, and schema extensions.

---

## 7. Review probes and verification evidence

Physical probes run during this review:

```text
PROBE_EMPTY_TRACE_EXECUTION {"exit_code": 0, "process_rc": 0, "staged_files": ["dry_run_output.txt"], "status": "SUCCESS", "trace_artifacts": []}
PROBE_ALLOWED_NEW_TRACKED_MODIFICATION {"error": "", "exit_code": 0, "process_rc": 0, "staged_files": ["tracked.txt"], "status": "SUCCESS", "trace_artifacts": [{"id": "REQ-DRY-001", "kind": "REQ", "version_hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}]}
PROBE_HANDOFF_UPPERCASE_HASH_ACCEPTED sha256:AAAAAAAAAAAAA
PROBE_MCP_UPPERCASE_HASH_REJECTED ValueError trace_artifacts[0].version_hash must match sha256:<64-lowercase-hex>
PROBE_ZERO_DIFF_VALIDATION_ORDER {"error": "engine produced no staged allowlisted diff", "exit_code": 3, "process_rc": 1, "status": "UNAUTHORIZED_FILE_MUTATION", "validation_logs": {"validation_001": "VALIDATION_RAN"}}
go run ./cmd/blk-pipe --health -> {"status":"OK","component":"blk-pipe"}
```

Repository status after probes and Python cache cleanup:

```text
## main...origin/main
```

Post-document verification after writing this review:

```text
BLK004_REVIEW_DOC_HYGIENE_PASS
python3 -m unittest discover -s python -p 'test_*.py' -> Ran 113 tests, OK
go test ./... -> PASS
go vet ./... -> PASS
go run ./cmd/blk-pipe --health -> {"status":"OK","component":"blk-pipe"}
git diff --check -> PASS
```

Final repository status after cleanup:

```text
## main...origin/main
?? docs/reviews/BLK-004_hostile-deviation-review.md
```

---

## 8. Sprint 008 closure note

BLK-PIPE-008 closed the unsafe/non-clean findings in this review.

Closure artifacts:

- `docs/outcomes/BLK-PIPE-008_task-001-outcome.md` — D-001 execute trace enforcement.
- `docs/outcomes/BLK-PIPE-008_task-002-outcome.md` — D-002 BLK-test handoff canonical trace validation.
- `docs/outcomes/BLK-PIPE-008_task-003-outcome.md` — D-003 strict tracked/new allowlist semantics.
- `docs/outcomes/BLK-PIPE-008_task-004-outcome.md` — D-004 no-candidate gate before validation.
- `docs/outcomes/BLK-PIPE-008_task-005-outcome.md` — D-005 through D-009 BLK-004 current-state overlay and decision documentation.
- `docs/outcomes/BLK-PIPE-008_sprint-closeout.md` — final hostile closeout, regression probes, and acceptance evidence.

The original review evidence above is preserved as historical RED evidence. Current behavior is governed by the Sprint 008 outcomes and the BLK-004/BLK-010 current-state overlay.
