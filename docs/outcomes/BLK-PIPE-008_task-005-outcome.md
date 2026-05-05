# BLK-pipe Sprint 008 — Task 5 Outcome

**Status:** Complete
**Date:** 2026-05-05
**Task:** Add BLK-004 Current-State Overlay and Decision Documentation
**Implementation Commit:** included in the Task 5 commit containing this outcome document
**Remote:** pushed to `origin/main` after Task 5 verification

---

## 1. Objective

Task 5 closes Sprint 008 findings D-005 through D-009 and records the adopted decisions for D-001 through D-004 so future implementers do not have to infer current BLK-System policy from code alone.

This task is documentation-only. It does not change BLK-pipe runtime code or enable any live execution path.

---

## 2. Files Changed

Updated:

- `docs/BLK-004_blk-pipe-v47-architecture-suite.md`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md`
- `README.md`

Created outcome:

- `docs/outcomes/BLK-PIPE-008_task-005-outcome.md`

Reviewed and left unchanged because their current Sprint 008 wording already preserved the required trace/current-disabled boundaries:

- `docs/BLK-013_blk-test-handoff-fixture-contract.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`
- `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`

---

## 3. Adopted Decision Register

| Decision | Final adopted decision | Disposition |
|---|---|---|
| DEC-001 | `execute` payloads require non-empty canonical `trace_artifacts`; `revert` and `--health` do not. | Closed by Task 1 code/tests and documented in BLK-004/BLK-010. |
| DEC-002 | BLK-test PASS/FAIL handoff fixtures require non-empty canonical trace artifacts. BLOCKED may preserve explicit trace absence only as non-authoritative blocked evidence. | Closed by Task 2 fixture validation and documented in BLK-010/BLK-013. |
| DEC-003 | `allowed_modified_files` and `allowed_new_files` are strict tracked/new authorization classes. Wrong-class paths fail closed before engine execution. | Closed by Task 3 code/tests and documented in BLK-004/BLK-010. |
| DEC-004 | Validation commands run only after the engine produces a candidate mutation. | Closed by Task 4 code/tests and documented in BLK-004/BLK-010. |
| DEC-005 | Current local health output remains `{"status":"OK","component":"blk-pipe"}`; BLK-004's older `{"status":"healthy"}` literal is superseded for the current local CLI contract. | Accepted compatibility overlay. |
| DEC-006 | BLK-004 source segments are not wholesale rewritten; a current-state overlay and corrected local example qualify them. | Accepted preservation/overlay policy. |
| DEC-007 | Local exit codes 6/7/9 remain BLK-System local V47-compatible extensions. | Accepted compatibility extension. |
| DEC-008 | Stronger ignored-file cleanup remains accepted hardening; cleanup paths may delete ignored-file residue. | Accepted hardening extension. |
| DEC-009 | Legacy migration payload fields and additional report fields remain accepted compatibility/evidence extensions. | Accepted compatibility/evidence extension. |

---

## 4. Documentation Implementation

`docs/BLK-004_blk-pipe-v47-architecture-suite.md` now has a `Current-State Overlay after BLK-PIPE-008` before the preserved source segments. The overlay states that:

- execute payloads require non-empty canonical `trace_artifacts`;
- BLK-pipe validates trace metadata shape/presence only and does not parse requirement/use-case bodies, generate RTMs, or verify hashes against BLK-req files;
- `allowed_modified_files` and `allowed_new_files` are strict tracked/new authorization classes;
- validation commands run only after an engine-produced candidate mutation exists;
- current health output is `{"status":"OK","component":"blk-pipe"}`;
- source-segment `codex`/live examples are target-state examples only;
- live Codex, live BLK-test MCP, authoritative BEO publication, and RTM generation remain disabled unless later active doctrine explicitly authorizes them;
- local exit codes 6/7/9, stronger cleanup, legacy migration fields, and additional report fields are accepted BLK-System local V47-compatible extensions.

The overlay also adds a corrected deterministic local execute example with canonical `trace_artifacts` and a local `sh` command rather than any live-Codex authorization implication.

`docs/BLK-010_blk-pipe-v47-hardening-cli.md` now carries the DEC-001 through DEC-009 current-state table and points to the BLK-004 overlay.

`docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md` now cross-references the BLK-004 overlay and repeats the current-disabled live authority boundary.

`README.md` now makes the BLK-004 overlay and BLK-010 Sprint 008 decision register discoverable from the active document list.

---

## 5. Gate Evidence

BLK-004 overlay gate:

```text
BLK004_CURRENT_STATE_OVERLAY_PASS
```

Active doctrine vocabulary gate:

```text
ACTIVE_DOC_VOCAB_PASS
```

Shared verification before commit:

```text
python3 -m unittest discover -s python -p 'test_*.py'
.........................................................................................................................
----------------------------------------------------------------------
Ran 121 tests in 0.659s

OK

go test ./... -> PASS

go vet ./... -> PASS

go run ./cmd/blk-pipe --health -> {"status":"OK","component":"blk-pipe"}

git diff --check -> PASS

OUTCOME_REMOTE_METADATA_PASS
```

---

## 6. Source Segment Preservation Statement

The BLK-004 source segments were not casually rewritten or invalidated. They remain intentional V47/BLK-pipe authority context. Sprint 008 adds an explicit current-state overlay before those source segments so readers can distinguish preserved target-state/historical authority examples from the current local BLK-System contract.

---

## 7. Authority / Safety Boundary

Task 5 did not run or enable:

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

The current-disabled authority statement after Task 5 is: live Codex, live BLK-test MCP, authoritative BEO publication, and RTM generation remain disabled unless later active doctrine explicitly authorizes them.

---

## 8. Remaining Sprint 008 Work

Task 5 closes D-005 through D-009 by accepted/documented current-state decisions. Remaining Sprint 008 work is Task 6: hostile closeout, regression probes, and sprint outcome.
