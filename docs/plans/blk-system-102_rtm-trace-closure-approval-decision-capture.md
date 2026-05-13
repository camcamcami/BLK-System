# BLK-SYSTEM-102 — RTM Trace-Closure Approval Decision Capture Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` when executing.

**Goal:** Capture the operator's explicit approval decision for the exact BLK-SYSTEM-101 RTM trace-closure authority request without executing trace closure.
**BLK-024 track:** Track H — BLK-link offline RTM ledger; maturity L0/L1 approval-decision capture.
**Architecture:** BLK-101 is request-only. BLK-102 may capture an exact approval decision and reserve one future run ID, but must not execute runtime `blk-link`, generate RTM, reject drift, compare active-vault hashes, or read protected bodies.
**Tech Stack:** Python deterministic fixture, Markdown doctrine/outcome/review artifacts, unittest gates.
**Authority boundary:** Approval-decision capture only; no execution.

## Preflight State

```text
date: 2026-05-13T20:58:01+10:00
git: main at 2e08420 feat: request blk-system 101 rtm trace closure authority
working tree: clean before sprint planning
```

## Exact Inputs

- `docs/outcomes/BLK-SYSTEM-101_rtm-trace-closure-authority-request.json`
- `authority_request_package_id: RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-101-001`
- `authority_request_package_hash: sha256:b050261c1c1938423795f56427571d49dcf1d028c5811b5e3985b644cfadbcde`
- Operator instruction in this Discord session: sequentially plan and execute BLK-SYSTEM-101, BLK-SYSTEM-102, and BLK-SYSTEM-103.

## Non-Authority Boundary

This sprint captures approval for exactly one future local RTM trace-closure execution sprint only. It does not execute trace closure, generate RTM, perform drift rejection, compare active-vault hashes, read protected bodies, mutate target/source/Git state, run BLK-pipe/BLK-test/Codex/tooling, or claim production isolation.

## Tasks

0. Publish this plan and `docs/outcomes/BLK-SYSTEM-102_task-000-outcome.md`.
1. Add RED tests for exact BLK-101 hash binding, approval timestamp/expiry binding, future run-ID reservation, no execution, denied-authority equality, and authority-laundering rejection.
2. Implement `python/rtm_trace_closure_approval_decision.py`.
3. Generate `docs/BLK-102_rtm-trace-closure-approval-decision-capture.md` and approval-decision artifact.
4. Run hostile review, focused tests, closeout, commit, and push exact paths.

## Expected Output Marker

```text
RTM_TRACE_CLOSURE_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK101_REQUEST_NOT_EXECUTED
RTM-TRACE-CLOSURE-APPROVAL-DECISION-102-001
RUN-BLK-SYSTEM-103-RTM-TRACE-CLOSURE-001
```
