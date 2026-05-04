# BLK-013 — BLK-test Handoff Fixture Contract

**Status:** Active fixture contract
**Scope:** BLK-PIPE-004 Task 6

---

## 1. Purpose

This document defines the deterministic BLK-test handoff fixture shape used by
BLK-PIPE-004. The fixture consumes an already-produced BLK-pipe execution report
and derives a local `PASS`, `FAIL`, or `BLOCKED` handoff object without calling
live BLK-test MCP, live Codex, live tactical LLMs, network model services, cyber
tooling, or any requirements-fetching service.

The fixture exists to prove trace-baton continuity and handoff shape only. It is
not an authority for BLK-req promotion, RTM generation, or live BLK-test verdicts.

---

## 2. Inputs

The fixture consumes a supplied BLK-pipe report dictionary. It does not read or
inspect protected BLK-req vault paths, including:

- `docs/active/`
- `docs/requirements/`
- `docs/use_cases/`

For `PASS` and `FAIL`, the source BLK-pipe report must include:

- `status == "SUCCESS"`
- non-empty `beb_id`
- non-empty `commit_hash`
- non-empty `pre_engine_hash`
- `staged_files == ["dry_run_output.txt"]`
- non-empty `trace_artifacts`

A non-success BLK-pipe report is not converted into BLK-test `FAIL`. It is routed
to `BLOCKED` so the handoff states that BLK-test did not run.

---

## 3. PASS shape

```json
{
  "status": "PASS",
  "beb_id": "BEB_004",
  "commit_hash": "<blk-pipe commit>",
  "pre_engine_hash": "<blk-pipe pre_engine_hash>",
  "test_profile": "strict-ci",
  "trace_artifacts": [
    {
      "kind": "REQ",
      "id": "REQ-DRY-001",
      "version_hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
  ],
  "checks": [
    {
      "name": "fixture-output-present",
      "status": "PASS",
      "summary": "dry_run_output.txt exists"
    }
  ],
  "compressed_logs": "bounded deterministic text"
}
```

`PASS` means the source BLK-pipe execution succeeded and the deterministic
fixture check passed.

---

## 4. FAIL shape

```json
{
  "status": "FAIL",
  "beb_id": "BEB_004",
  "commit_hash": "<blk-pipe commit>",
  "pre_engine_hash": "<blk-pipe pre_engine_hash>",
  "test_profile": "strict-ci",
  "trace_artifacts": [
    {
      "kind": "REQ",
      "id": "REQ-DRY-001",
      "version_hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
  ],
  "checks": [
    {
      "name": "fixture-output-present",
      "status": "FAIL",
      "summary": "dry_run_output.txt missing"
    }
  ],
  "compressed_logs": "bounded deterministic text"
}
```

`FAIL` means BLK-pipe succeeded but a deterministic fixture check failed. It does
not represent a BLK-pipe failure.

---

## 5. BLOCKED shape

```json
{
  "status": "BLOCKED",
  "beb_id": "BEB_004",
  "commit_hash": "",
  "pre_engine_hash": "<blk-pipe pre_engine_hash when present>",
  "test_profile": "strict-ci",
  "trace_artifacts": [
    {
      "kind": "REQ",
      "id": "REQ-DRY-001",
      "version_hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
  ],
  "checks": [
    {
      "name": "blk-pipe-success-required",
      "status": "BLOCKED",
      "summary": "BLK-test did not run because BLK-pipe status was SYNTAX_GATE_FAILED"
    }
  ],
  "compressed_logs": "bounded deterministic text"
}
```

`BLOCKED` preserves safe trace artifacts when present, including the opaque
`version_hash` baton, while making clear that the handoff state is: No BLK-test fixture verdict ran.

---

## 6. Determinism and log bounds

- PASS, FAIL, and BLOCKED are derived only from the supplied report and explicit
  fixture status path.
- There is no MCP call, no live test server dependency, and no LLM judgment.
- Logs are line-deduplicated and byte-bounded for fixture use.
- Trace artifacts are copied as opaque fields. The fixture does not parse or
  validate requirement bodies.

---

## 7. Implementation mapping

The local Python fixture module is `python/blk_test_handoff_fixtures.py`:

- `build_blk_test_pass_handoff(source_report, ...)`
- `build_blk_test_fail_handoff(source_report, ...)`
- `build_blk_test_blocked_handoff(source_report, ...)`

The deterministic test suite is `python/test_blk_test_handoff_fixtures.py`.
