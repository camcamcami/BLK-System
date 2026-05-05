# BLK-pipe Sprint 008 — Task 2 Outcome

**Status:** Complete
**Date:** 2026-05-05
**Task:** Harden BLK-test Handoff Fixture Trace Validation
**Implementation Commit:** included in the Task 2 commit containing this outcome document
**Remote:** pending push at time of writing

---

## 1. Objective

Task 2 closes Sprint 008 finding D-002: BLK-test handoff fixture builders must not preserve malformed trace batons as PASS/FAIL-shaped evidence.

Implemented behavior:

- `build_blk_test_pass_handoff(...)` rejects missing, empty, non-object, malformed, uppercase, short, or nonhex trace artifacts.
- `build_blk_test_fail_handoff(...)` rejects the same malformed trace artifacts.
- `build_blk_test_blocked_handoff(...)` rejects malformed trace artifacts when trace metadata is supplied.
- BLOCKED reports that genuinely lack decoded trace metadata preserve `trace_artifacts: []` and add:

```json
"trace_absence_reason": "source report did not include decoded trace_artifacts"
```

- Trace-absent BLOCKED evidence remains non-authoritative blocked evidence only and must not become PASS, FAIL, draft BEO success evidence, RTM generation, or BLK-req promotion evidence.
- No handoff builder reads protected BLK-req vault paths.

---

## 2. Files Changed

Updated:

- `python/blk_test_handoff_fixtures.py`
- `python/test_blk_test_handoff_fixtures.py`
- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
- `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`

Created outcome:

- `docs/outcomes/BLK-PIPE-008_task-002-outcome.md`

---

## 3. RED Evidence

After adding malformed-trace tests, the focused test suite failed as expected because uppercase/noncanonical hashes and malformed BLOCKED trace metadata were accepted or silently dropped:

```text
test_blk_test_blocked_payload_records_trace_absence_reason_when_absent ... ERROR
test_blk_test_blocked_payload_rejects_malformed_trace_when_present ... FAIL
test_blk_test_blocked_payload_rejects_non_object_trace_entry_when_present ... FAIL
test_blk_test_fail_payload_rejects_missing_trace_hash ... FAIL
test_blk_test_fail_payload_rejects_short_trace_hash ... FAIL
test_blk_test_pass_payload_rejects_uppercase_trace_hash ... FAIL

KeyError: 'trace_absence_reason'
AssertionError: ValueError not raised
AssertionError: "version_hash" does not match "BLK-pipe report must include non-empty trace_artifacts"
AssertionError: ValueError not raised

----------------------------------------------------------------------
Ran 21 tests in 0.002s

FAILED (failures=5, errors=1)
```

Representative RED acceptance evidence:

- `build_blk_test_pass_handoff(...)` accepted `sha256:` followed by uppercase `A` characters.
- `build_blk_test_fail_handoff(...)` accepted a short `sha256:abc123` hash.
- `build_blk_test_blocked_handoff(...)` accepted `sha256:` followed by nonhex `g` characters when trace metadata was present.
- BLOCKED trace absence did not record an explicit absence reason.

---

## 4. GREEN Implementation

Implementation details:

- Added `_TRACE_HASH_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")`.
- Reworked `_trace_artifacts(...)` to validate trace entries strictly instead of silently dropping malformed entries.
- PASS/FAIL now call the trace validator with `require_non_empty=True`.
- BLOCKED validates any supplied trace entries with `require_non_empty=False`, but preserves `[]` plus `trace_absence_reason` when decoded trace metadata is absent.
- Added `_required_string(...)` to reject missing/non-string/blank trace fields and bound trace-field error handling without echoing oversized trace bodies.
- Updated fixture docs to state canonical PASS/FAIL trace requirements, BLOCKED trace absence semantics, and no protected-vault reads or hash-file verification.

---

## 5. GREEN Focused Test Evidence

Focused handoff suite after implementation:

```text
PYTHONPATH=python python3 -m unittest python/test_blk_test_handoff_fixtures.py -v
...
test_blk_test_blocked_payload_records_trace_absence_reason_when_absent ... ok
test_blk_test_blocked_payload_rejects_malformed_trace_when_present ... ok
test_blk_test_blocked_payload_rejects_non_object_trace_entry_when_present ... ok
test_blk_test_fail_payload_rejects_missing_trace_hash ... ok
test_blk_test_fail_payload_rejects_short_trace_hash ... ok
test_blk_test_pass_payload_rejects_empty_trace_artifacts ... ok
test_blk_test_pass_payload_rejects_non_object_trace_entry ... ok
test_blk_test_pass_payload_rejects_uppercase_trace_hash ... ok

----------------------------------------------------------------------
Ran 21 tests in 0.001s

OK
```

Python discovery:

```text
python3 -m unittest discover -s python -p 'test_*.py'
.........................................................................................................................
----------------------------------------------------------------------
Ran 121 tests in 0.658s

OK
```

Documentation gate:

```text
BLK_PIPE_008_TASK_002_DOC_GATE_PASS
```

The documentation gate checked BLK-013, BLK-014, and BLK-016 for the new PASS/FAIL canonical trace requirement, explicit BLOCKED trace absence reason, and non-authoritative blocked evidence boundary.

---

## 6. Protected Vault / Authority Evidence

The existing focused test `test_blk_test_fixture_does_not_read_active_vault` remained green. It patches `Path.read_text` to fail if any code attempts to read:

- `docs/active`
- `docs/requirements`
- `docs/use_cases`

The Task 2 implementation uses only supplied source report dictionaries and does not read requirement/use-case bodies or protected vault paths.

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

Task 2 did not run or enable:

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

The change only hardens deterministic local BLK-test handoff fixture validation and updates local tests/docs for that boundary.

---

## 9. Remaining Sprint 008 Work

Task 2 closes D-002 only. Remaining Sprint 008 tasks still own:

- Task 3 / D-003: strict tracked-vs-new allowlist semantics;
- Task 4 / D-004: no-candidate gate before validation;
- Task 5 / D-005 through D-009: BLK-004/BLK-010 current-state decision overlay;
- Task 6: sprint closeout and hostile self-review.
