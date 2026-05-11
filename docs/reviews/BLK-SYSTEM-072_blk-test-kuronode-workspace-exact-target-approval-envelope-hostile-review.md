# BLK-SYSTEM-072 Hostile Review — Kuronode Workspace Exact-Target Approval Envelope

**Status:** Complete — blockers found and remediated
**Date:** 2026-05-11T12:06:00+10:00
**Sprint:** BLK-SYSTEM-072
**Scope:** Hostile review of the review-only exact-target approval-envelope fixture, BLK-073 boundary, tests, and active doctrine gate.

---

## Summary

Hostile review found real authority-laundering blockers in the first implementation. The initial fixture correctly rejected many direct envelope edits, but it still trusted attacker-recomputed upstream request packages too broadly and allowed runtime/frontier wording to be smuggled through `operator_identity`.

All blockers listed below were remediated with RED regressions and GREEN implementation changes before closeout.

---

## Blocker 1 — Upstream Request Hash Was Self-Consistency Only

**Finding:** `_validate_upstream_request()` recomputed the submitted upstream request hash but did not validate all authority-bearing upstream fields. An attacker could alter closed-schema fields, recompute `request_hash`, and still receive BLK-SYSTEM-072 review-ready output.

Accepted forged surfaces before remediation included:

- runtime/execution booleans set true;
- production/generic BLK-test MCP booleans set true;
- source/Git/protected-body/isolation booleans set true;
- BEO/RTM/coverage statuses promoted;
- weakened upstream proof markers, excluded authorities, historical references, or no-side-effect flags.

**Remediation:** Added `test_upstream_authority_fields_are_exact_even_when_attacker_recomputes_hash` and enforced exact upstream values for request identity, scope, target, tool mode, status strings, all authority booleans, proof markers, historical references, excluded authorities, and no-side-effect flags.

---

## Blocker 2 — Valid-Field Natural-Language Smuggling in Operator Identity

**Finding:** `operator_identity` was prefix-only. Hostile strings after `discord:684235178083745819:` could carry runtime/frontier approval wording and be returned in the result.

**Remediation:** Made `operator_identity` exact (`discord:684235178083745819:camcamcami`) and added hostile regressions for punctuation variants including dotted, slash, colon, selected-frontier, live-execution, and approved-for-runtime strings.

---

## Blocker 3 — Laundering Tests Were Masked by Exact-String Fields

**Finding:** Several laundering probes used `operator_stop_control`, which is already exact-string checked. That produced false confidence because rejection did not necessarily prove laundering detection coverage.

**Remediation:** Added smuggling probes to `operator_identity`, a non-output-normalized authority surface in the first implementation, and added broader normalized forbidden patterns for runtime/frontier variants.

---

## Blocker 4 — Replay / One-Use IDs Were Declarative Only

**Finding:** BLK-SYSTEM-072 is review-only and has no durable replay ledger or consumed-ID input. Therefore, one-use ID enforcement cannot honestly be claimed as performed by this sprint.

**Remediation:** Preserved fresh BLK-SYSTEM-072 future candidate IDs while making the result and BLK-073 explicit:

```text
replay_consumed: false
one_use_id_status: FUTURE_RUNTIME_CANDIDATES_NOT_CONSUMED_BY_REVIEW
No replay consumption occurs in BLK-SYSTEM-072.
```

This keeps review-only readiness honest and reserves actual once-only consumption for a later explicitly approved runtime sprint.

---

## Blocker 5 — Active Doctrine Gate Under-Scoped

**Finding:** The initial active doctrine gate checked existence and selected boundary markers but did not pin all explicit non-authority surfaces or replay-consumption honesty.

**Remediation:** Expanded the active doctrine gate to require BLK-073 markers for fixed-tool future runtime only, arbitrary shell/caller-supplied command denial, dynamic tool expansion denial, public ledger mutation denial, signer/storage/rollback/revocation/supersession/release denial, live Codex denial, live tactical LLM dispatch denial, future one-use ID candidate wording, and no replay consumption in BLK-SYSTEM-072.

---

## Post-Remediation Hostile Probe

A direct hostile probe over recomputed upstream authority mutations and operator-identity smuggling returned no accepted probes:

```text
accepted hostile probes: []
exit 0
```

---

## Verification

Focused approval-envelope fixture:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_kuronode_workspace_exact_target_approval_envelope -q
----------------------------------------------------------------------
Ran 9 tests in 0.024s

OK
```

Focused active doctrine gate:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint072_blk_test_kuronode_workspace_exact_target_approval_envelope_is_review_only -q
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```

Full verification:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest discover python 'test_*.py'
----------------------------------------------------------------------
Ran 750 tests in 9.470s

OK

go test ./...
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validationprofiles	(cached)

git diff --check
```

---

## Non-Execution Statement

Hostile review and remediation did not run BLK-test runtime against Kuronode, did not start BLK-test MCP, did not run Electron/smoke/TypeScript/package-manager tooling, did not invoke Codex, did not invoke BLK-pipe, did not mutate Kuronode source or Git state, did not push Kuronode, did not read protected BLK-req bodies, did not publish BEOs, and did not generate RTM.
