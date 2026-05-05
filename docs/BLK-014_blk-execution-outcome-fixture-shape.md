# BLK-014 — BLK Execution Outcome Fixture Shape

**Status:** Active fixture contract
**Scope:** BLK-PIPE-004 Task 7

---

## 1. Purpose

This document defines the deterministic draft Blk Execution Outcome (BEO) shape
used by BLK-PIPE-004 fixture tests. The fixture projects an already-supplied
BLK-test fixture handoff into a BEO-shaped object while preserving the opaque
`trace_artifacts` / canonical `version_hash` baton (`sha256:<64-lowercase-hex>`).

BEO is fixture/draft-only in Sprint 004 and remains fixture/draft-only in Sprint 005. The fixture does not publish an outcome,
does not generate an RTM, does not call live BLK-test MCP, does not run Codex,
does not call live LLMs or network model services, and does not inspect active BLK-req files.
Sprint 004 does not run Codex, Sprint 004 does not authorize live LLM execution,
and Sprint 004 does not authorize cyber execution. Sprint 005 adds a fail-closed
approval-token contract and disabled BLK-test MCP request/response stubs only;
even a valid `codex-live` approval-token decision remains `APPROVED_BUT_NOT_EXECUTED`,
RTM is not generated, and authoritative BEO publication remains blocked. Sprint
006 binds disabled MCP PASS/FAIL response mapping to exact source-request evidence
before any future BEO-shaped projection may consume it: `beb_id`, `commit_hash`,
`pre_engine_hash`, `trace_artifacts`, and non-empty checks must be source-bound,
while BLOCKED mapping preserves source trace artifacts without claiming a verdict.

---

## 2. Inputs

The projection consumes a supplied BLK-test fixture handoff dictionary. It does
not read or inspect protected BLK-req vault paths, including:

- `docs/active/`
- `docs/requirements/`
- `docs/use_cases/`

Supported source fixture statuses:

- `PASS`
- `FAIL`

`BLOCKED` is not projected into a BEO fixture by Task 7 because BLK-test did not
produce a PASS/FAIL fixture verdict.

---

## 3. PASS BEO draft shape

```json
{
  "beo_id": "BEO_004",
  "beb_id": "BEB_004",
  "status": "PASS",
  "source": "blk-test-fixture",
  "commit_hash": "<blk-pipe commit>",
  "pre_engine_hash": "<blk-pipe pre_engine_hash>",
  "trace_artifacts": [
    {
      "kind": "REQ",
      "id": "REQ-DRY-001",
      "version_hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
  ],
  "test_summary": {
    "profile": "strict-ci",
    "checks_passed": 1,
    "checks_failed": 0
  },
  "rtm_status": "NOT_GENERATED",
  "beo_publication": "DRAFT_ONLY"
}
```

`PASS` means the supplied BLK-test fixture handoff passed. The BEO fixture copies
`beb_id`, `commit_hash`, `pre_engine_hash`, and `trace_artifacts` from the source
handoff and summarizes check counts deterministically.

---

## 4. FAIL BEO draft shape

```json
{
  "beo_id": "BEO_004",
  "beb_id": "BEB_004",
  "status": "FAIL",
  "source": "blk-test-fixture",
  "commit_hash": "<blk-pipe commit>",
  "pre_engine_hash": "<blk-pipe pre_engine_hash>",
  "trace_artifacts": [
    {
      "kind": "REQ",
      "id": "REQ-DRY-001",
      "version_hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
  ],
  "test_summary": {
    "profile": "strict-ci",
    "checks_passed": 0,
    "checks_failed": 1
  },
  "rtm_status": "NOT_GENERATED",
  "beo_publication": "DRAFT_ONLY"
}
```

`FAIL` cannot produce a success BEO. It produces a failed draft BEO fixture while
preserving trace artifacts when present.

---

## 5. RTM and authority boundaries

`live BLK-test MCP remains disabled`, and `RTM generation remains disabled` for this fixture projection. The `rtm_status` field is always
`NOT_GENERATED`, and `beo_publication` is always `DRAFT_ONLY`. This document and the associated
Python fixture do not claim full RTM generation, authoritative BEO publication, BLK-req
promotion authority, or HITL approval.

The fixture treats `REQ-DRY-001` as a synthetic fixture identifier only. It requires
`version_hash` syntax to match `sha256:<64-lowercase-hex>`, but it does not verify the hash against requirement files and does not parse
requirements or use-case bodies.

---

## 6. End-to-end trace baton test

The deterministic test suite includes an end-to-end fixture test that exercises:

1. BEB/L2 payload construction from `testdata/orchestrator/` fixtures.
2. Real BLK-pipe invocation through the local fake `codex-dry-run` engine.
3. Raw BLK-pipe JSON report parsing.
4. BLK-test PASS handoff construction.
5. BEO fixture projection.

The test asserts the exact `trace_artifacts` list survives unchanged across the
whole dry-run loop. It does not call live Codex, live tactical LLMs, network model
services, cyber tooling, or live BLK-test MCP.

---

## 7A. Sprint 007 disabled MCP PASS/FAIL projection

Sprint 007 adds `project_mapped_mcp_response_to_beo(...)` as a draft-only projection from source-bound disabled MCP mapped response fixtures. The input source must be `blk-test-mcp-response-shape`, the status must be `PASS` or `FAIL`, and the mapped response must include non-empty checks plus canonical `trace_artifacts`.

The output preserves `beb_id`, `commit_hash`, `pre_engine_hash`, and exact trace metadata while forcing:

```text
beo_publication: "DRAFT_ONLY"
rtm_status: "NOT_GENERATED"
```

`BLOCKED` mapped responses reject because BLK-test did not produce a PASS/FAIL fixture verdict. See [BLK-016](BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md) for the Sprint 007 disabled adapter and BEO/RTM interface contract.

---

## 7. Implementation mapping

The local Python fixture module is `python/beo_fixture_projection.py`:

- `project_blk_test_handoff_to_beo(blk_test_handoff, *, beo_id)`
- `project_mapped_mcp_response_to_beo(mapped_response, *, beo_id, test_profile="strict-ci")`

The BEO/RTM disabled interface module is `python/beo_rtm_interface_fixtures.py`:

- `build_beo_rtm_interface_fixture(beo_fixture, *, interface_id)`

The deterministic test suite is `python/test_beo_fixture_projection.py` plus `python/test_beo_rtm_interface_fixtures.py` for the RTM-facing interface fixture.
