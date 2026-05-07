# BLK-SYSTEM-021 — Post-Remediation Hostile Review

**Status:** PASS after Task 005 remediation
**Date:** 2026-05-07T21:38:00+10:00
**Plan:** `docs/plans/blk-system-021_python-adapter-policy-layer-hardening.md`

---

## 1. Review Scope

This review checks BLK-SYSTEM-021 against BLK-024 Track E, BLK-001 through BLK-006, and the Task 5 checklist in the sprint plan.

Reviewed implementation/docs:

- `python/blk_pipe_adapter.py`
- `python/test_blk_pipe_adapter.py`
- `docs/BLK-004_blk-pipe-v47-architecture-suite.md`
- `python/test_active_doctrine_review_gates.py`
- `docs/outcomes/BLK-SYSTEM-021_task-000-outcome.md` through `docs/outcomes/BLK-SYSTEM-021_task-004-outcome.md`

---

## 2. Initial Hostile Findings

An independent hostile review initially returned **FAIL** before closeout because:

1. Task 005 closeout artifacts did not yet exist.
2. Python preflight bounded `validation_commands` only by non-empty string checks, while Go already bounds count and bytes.
3. `_invoke_binary` used scrubbed env but `run_health_check()` did not yet pass the scrubbed environment helper.

The task-005 closeout artifacts are created by this closeout task. The two implementation gaps were remediated before final closeout.

---

## 3. Remediation Applied During Task 005

Task 005 added final hardening before closeout:

- `python/blk_pipe_adapter.py`
  - Added Python-side `validation_commands` maximum count bound of 16.
  - Added Python-side `validation_commands` maximum command-size bound of 4096 bytes.
  - Updated `run_health_check()` to use `_build_subprocess_env()`.
- `python/test_blk_pipe_adapter.py`
  - Added validation-command bound tests for too many and oversized trusted-local commands.
  - Added health-check environment scrub test for `SSH_AUTH_SOCK`, `SSH_AGENT_PID`, and `SSH_ASKPASS`.

This remediation is still preflight/convenience only. Go remains final authority.

---

## 4. Hostile Checklist Verdict

| Check | Verdict | Evidence |
| --- | --- | --- |
| Python remains convenience/preflight, not final authority | PASS | BLK-004 Sprint 021 overlay says Python policy checks are fail-fast convenience only and Go remains final deterministic enforcement authority. |
| Go owns final payload validation/protected-path/profile/execution/cleanup/report authority | PASS | Go code and BLK-004 remain authoritative; Python mirrors obvious operator mistakes only. |
| Execute payloads require canonical non-empty `trace_artifacts` without protected body reads | PASS | `python/blk_pipe_adapter.py` validates metadata shape/hash only; no BLK-req body reads are added. |
| Protected BLK-req allowlists are rejected early while Go Exit 3 remains authoritative | PASS | Python rejects `docs/active/`, `docs/requirements/`, and `docs/use_cases/`; BLK-004 preserves Go protected-path authority. |
| `validation_profiles` are preserved and mixed profile/command requests fail | PASS | Python tests cover profile preservation and mixed-source rejection. |
| Trusted-local `validation_commands` compatibility remains bounded | PASS | Python now mirrors Go count/byte bounds in addition to non-empty string checks; Go remains final authority. |
| Subprocess invocation is shell-free and high-risk SSH/askpass env is scrubbed | PASS | Payload invocation and health check use list argv and scrubbed env helper. |
| Raw Go report fields are preserved without hiding non-success statuses | PASS | Python preserves `raw_report`, `stderr`, `trace_artifacts`, `validation_profiles`, `resolved_validation_commands`, `staged_files`, and `destroyed_files`; unknown nonzero codes cannot report success. |
| No BLK-test/BEO/RTM/live authority expansion | PASS | BLK-004 and outcome docs explicitly deny production BLK-test MCP, live tactical LLM execution, authoritative BEO publication, RTM generation, and drift rejection. |
| Follow-up candidates are separated | PASS | Closeout lists BEB generator/profile migration and later legacy-command removal/gating separately. |

---

## 5. Final Verdict

**PASS.** BLK-SYSTEM-021 satisfies Track E as a local Python adapter policy-layer hardening sprint.

The sprint improves fail-fast adapter behavior and subprocess hygiene while preserving the governing authority boundary: Python is convenience/preflight only, and compiled Go `blk-pipe` remains the final deterministic enforcement and report-evidence authority.

---

## 6. Non-Execution Statement

This review did not authorize Hindsight use, Codex use, live tactical LLM execution, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads/copying/parsing/hashing/mutation, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, or source mutation outside exact approved allowlists.
