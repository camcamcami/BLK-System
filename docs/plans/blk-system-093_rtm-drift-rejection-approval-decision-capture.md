# BLK-SYSTEM-093 — RTM Drift-Rejection Approval Decision Capture Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. BLK-024 is maturity lineage only; BLK-077/BLK-079/BLK-092 control current post-091 sequencing.

**Goal:** Capture the exact human approval decision for the BLK-SYSTEM-091 RTM drift-rejection request package without executing drift rejection.
**BLK-024 track:** Track H — BLK-link offline RTM ledger plus Track A doctrine gates / maturity L0/L1 approval-decision capture.
**Architecture:** This sprint consumes the exact BLK-SYSTEM-091 request package by hash and records one future local drift-rejection execution approval decision. It does not perform the execution, does not compare active-vault hashes, does not read protected bodies, and does not mutate any ledger.
**Tech Stack:** Python deterministic fixture, Python `unittest`, Markdown doctrine/outcomes.
**Authority boundary:** Approval-decision capture only. No RTM drift-rejection execution, no drift decision, no active-vault hash comparison, no protected-body reads/hashing, no external ledger/publication/signing/storage/rollback side effects, no target/source/Git mutation by fixture, no BEB/BEO execution, no BLK-pipe/BLK-test/Codex runtime, no package/network/model/browser/cyber tooling, and no production isolation claim.

## Current Known State

- Date: `2026-05-13T07:05:27+10:00`
- Git status: `## main...origin/main`
- HEAD: `c2b2ca5 docs: reconcile blk-system post 091 state`

## Governing Docs

- BLK-024: maturity ladder and separate-approval principles.
- BLK-001: preserve V-model component separation.
- BLK-002 / BLK-005 / BLK-006: protected BLK-req bodies remain unread/unhashed.
- BLK-003 / BLK-004: BEB/BEO and BLK-pipe execution remain separate.
- BLK-077 / BLK-079 / BLK-092: current post-091/post-092 selection and non-authority boundary.
- BLK-089 / BLK-090 / BLK-091: upstream RTM ladder evidence.

## Task Sequence

1. **Task 000 — Plan and scope**
   - Publish this plan and task outcome.
   - Pin approval-capture vs execution separation.

2. **Task 001 — Approval-decision RED/GREEN**
   - Add RED tests for exact BLK-SYSTEM-091 request binding, recomputed request hash, exact schema/proof/denial validation, decision IDs, expiry/replay/stale guards, side-effect false flags, laundering probes, and defensive copies.
   - Implement `python/rtm_drift_rejection_approval_decision.py` minimally to pass.

3. **Task 002 — Doctrine and current-state gates**
   - Publish `docs/BLK-093_rtm-drift-rejection-approval-decision-capture.md`.
   - Update BLK-077/BLK-079 and executable current-state index to expose BLK-093 as approval-decision evidence only.

4. **Task 003 — Hostile review and remediation**
   - Review for approval-as-execution laundering, upstream request/hash substitution, missing exact sets, active-vault/protected-body side effects, external ledger claims, replay/expiry gaps, and stale next-frontier wording.
   - Remediate blockers with tests/code/docs before closeout.

5. **Task 004 — Verification and closeout**
   - Run focused tests, full Python suite, Go checks, and diff hygiene.
   - Publish task outcomes and sprint closeout.

## Expected Status Markers

```text
RTM_DRIFT_REJECTION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK091_REQUEST_NOT_EXECUTED
APPROVED_FOR_ONE_FUTURE_LOCAL_RTM_DRIFT_REJECTION_EXECUTION_NOT_EXECUTED
EXACT_LOCAL_RTM_DRIFT_REJECTION_EXECUTION_REQUIRED_NOT_RUN
BLK_SYSTEM_093_GRANTS_NO_RTM_DRIFT_REJECTION_EXECUTION
```
