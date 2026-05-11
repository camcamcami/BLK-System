# BLK-SYSTEM-071 Hostile Review — BLK-test Kuronode Workspace Pilot Request

**Status:** Complete — findings remediated
**Date:** 2026-05-11T11:20:00+10:00
**Scope:** `python/blk_test_kuronode_workspace_pilot_request.py`, `python/test_blk_test_kuronode_workspace_pilot_request.py`, `docs/BLK-072_blk-test-kuronode-workspace-read-only-pilot-request-boundary.md`, active doctrine gate, and Task 001/002 outcomes.

---

## Summary

Hostile review found authority-laundering gaps in the first implementation. All blocking findings were remediated before closeout.

The remediated package remains request/doctrine/fixture-only:

```text
BLK_TEST_KURONODE_WORKSPACE_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
```

It preserves the naming boundary:

```text
BLK-test is a BLK-System functional module, not BLK-System's test suite.
```

---

## Findings and Remediation

| Severity | Finding | Remediation |
| --- | --- | --- |
| CRITICAL | Authority laundering was accepted through valid fields such as `target_scope` and `historical_references_only`. Examples included runtime approval, BEO publication, coverage truth, drift decision, executable fixture input, and approval/run ID reuse. | Closed `target_scope` to an exact literal; made `historical_references_only` an exact set; expanded RED tests to inject laundering strings into permitted fields; expanded forbidden pattern coverage. |
| HIGH | Exact target binding used path normalization, allowing spellings such as `/home/dad/code/Kuronode-v1/.`. | Switched to raw exact string equality for `/home/dad/code/Kuronode-v1`; added tests for `/.`, trailing slash, double slash, `..`, and `~` aliases. |
| HIGH | CEB_009 / BLK-SYSTEM-070 artifact reuse gate missed task-002, BLK-071, executable fixture input, approval-id, and run-id aliases. | Expanded reuse rejection and exact historical-reference validation; added RED cases for BLK-SYSTEM-070 task-002, approval/run ID reuse, and BLK-071 patch-authority fixture input. |
| HIGH | BEO/RTM/coverage/drift inheritance checks were incomplete. | Added tests and forbidden patterns for `BEO is PUBLISHED`, published BEO output, BEO publication granted, RTM generated, coverage complete/truth, and drift decision. |
| HIGH | Active doctrine gate was presence-only. | Added forbidden-claim absence checks to the BLK-072 active doctrine gate. |
| MEDIUM | BLK-test naming laundering was possible outside the exact role statement. | Closed `target_scope` to the exact request-only phrase and retained recursive BLK-test naming checks. |
| MEDIUM | Protected paths/secrets denylist was under-scoped. | Added tests and forbidden patterns for `.env`, secrets, `SECRET_KEY`, authorization, bearer tokens, credentials, private/API keys. |
| MEDIUM | Some tests overclaimed recursive laundering because extra-field rejection fired first. | Added valid-field hostile cases for `historical_references_only` and `target_scope`, preserving extra-field rejection only as secondary coverage. |

---

## Verification

Focused verification after remediation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_kuronode_workspace_pilot_request -q
----------------------------------------------------------------------
Ran 8 tests in 0.009s

OK
```

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint071_blk_test_kuronode_workspace_pilot_request_is_module_request_not_blk_system_test -q
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```

---

## Remaining Risk

No runtime BLK-test module execution was performed. That is intentional and required by the sprint boundary. A future Kuronode workspace runtime pilot must use a separate exact-target approval envelope with fresh replay IDs and explicit operator approval.

---

## Non-Authority Statement

This hostile review did not run BLK-test runtime against Kuronode, did not start BLK-test MCP, did not run Electron/smoke/TypeScript/package-manager tooling, did not invoke Codex, did not invoke BLK-pipe, did not mutate Kuronode source or Git state, did not push Kuronode, did not read protected BLK-req bodies, did not publish BEOs, and did not generate RTM.
