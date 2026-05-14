# BLK-SYSTEM-128 — External BEO Publication Approval Capture Plan

**Status:** Planned for execution
**Date:** 2026-05-15T08:52:12+10:00
**Documentation model:** Lean — no BLK-### sprint doc; one closeout outcome only.

## 1. Objective

Capture an explicit human approval decision for exact package `BEO-PUBLICATION-PREREQUISITE-REQUEST-127-001` without executing external BEO publication.

## 2. Scope

Implement a local deterministic fixture that:

- accepts only the exact BLK-SYSTEM-127 prerequisite request ID and canonical request hash;
- binds operator identity, raw approval text, normalized request ID, decision ID, approval ID, and one future execution run ID;
- records approval capture as a decision package only;
- keeps publication execution, signer/storage/ledger/rollback, RTM, drift, BLK-pipe, BLK-test, Codex, protected-body reads, and target/source/Git mutation disabled.

## 3. TDD Tasks

1. Add RED tests for a valid approval-capture package and hostile rejects.
2. Implement the smallest fixture module to pass the tests.
3. Update current-state/roadmap markers to move the next frontier to separately authorized external publication execution.
4. Run focused tests, hostile audit probes, full suite, and whitespace checks.
5. Write exactly one sprint closeout in `docs/outcomes/BLK-SYSTEM-128_sprint-closeout.md`.

## 4. Authority Boundary

This sprint may capture a record-only approval decision. It does not publish a BEO and does not authorize execution in this same sprint. Publication execution remains a separate future rung requiring exact IDs, replay controls, and fresh hostile review.
