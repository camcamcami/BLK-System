# BLK-SYSTEM-041 — Codex Live-Dispatch Authority Request Hostile Review

**Status:** PASS after remediation
**Date:** 2026-05-09T15:20:37+10:00
**Sprint:** BLK-SYSTEM-041 — Codex live-dispatch authority request disabled adapter

---

## 1. Review Scope

This hostile review examined the BLK-SYSTEM-041 boundary, authority-request fixture, disabled adapter fixture, and tests:

```text
docs/BLK-043_codex-live-dispatch-authority-request-disabled-adapter-boundary.md
python/blk_codex_live_dispatch_authority_request.py
python/test_blk_codex_live_dispatch_authority_request.py
python/test_active_doctrine_review_gates.py
```

The review objective was to determine whether the sprint accidentally created live Codex execution authority, BLK-pipe dispatch authority, protected-vault access, BEO/RTM/drift authority, readiness-as-execution laundering, or production sandbox claims.

---

## 2. Hostile Questions and Findings

### 2.1 Does any helper start subprocesses, call Codex, call Git, call BLK-pipe, install packages, use network/model/cyber/browser tooling, or inspect protected vaults?

**Verdict:** PASS.

`python/blk_codex_live_dispatch_authority_request.py` imports only:

```text
__future__.annotations
datetime.datetime
typing.Any
blk_codex_live_dispatch_readiness_gate.validate_codex_live_dispatch_readiness_gate
```

AST tests reject live-surface imports and calls for subprocess, shell, socket, network clients, `system`, `popen`, `run`, `Popen`, `call`, `check_call`, `check_output`, `exec`, `eval`, and `__import__`.

### 2.2 Can `AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_EXECUTION` become execution approval?

**Verdict:** PASS.

The fixture always records:

```text
execution_authorized: false
codex_subprocess_started: false
blk_pipe_dispatched: false
source_mutation_authorized: false
```

Tests reject direct attempts to change those flags and reject `READY_FOR_EXECUTION` / `APPROVED_FOR_LIVE_EXECUTION` wording as authority laundering.

### 2.3 Can a readiness record with `BLOCKED_NOT_AUTHORIZED` pass?

**Verdict:** PASS.

Blocked readiness records produce `DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED`, with blocked reasons tied to readiness invalidity or non-ready status.

### 2.4 Can a missing separate human-grant requirement pass?

**Verdict:** PASS.

Missing, expired, replayed, malformed, or non-review-only human grants block. Request replay IDs and omitted replay-state inputs fail closed.

### 2.5 Can disabled adapter simulation be bypassed into live dispatch?

**Verdict:** PASS.

`simulate_disabled_codex_live_dispatch_adapter(...)` has only one result: `DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED`. It records no execution, Codex subprocess, BLK-pipe dispatch, source mutation, Git mutation, BEO publication, RTM generation, drift rejection, or production sandbox claim.

### 2.6 Can telemetry become canonical mutation, validation, approval, BEO, RTM, or drift evidence?

**Verdict:** PASS.

The module packages review metadata only and delegates embedded readiness validation to BLK-042. It does not read telemetry artifacts or convert telemetry into canonical evidence.

### 2.7 Can recursive authority-laundering keys/strings bypass validation?

**Verdict:** PASS after remediation.

See blocker below.

---

## 3. Blocker Found During Review

**Blocker:** Task 2 validation rejected authority-laundering strings when `validate_codex_live_dispatch_authority_request(...)` was called, but the builder/evaluator could still return `AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_EXECUTION` for a separate human grant whose scope string was `APPROVED_FOR_LIVE_EXECUTION`.

This was blocker-class because operator-facing evaluation must fail closed before a later validator is invoked. A review-only helper cannot mark an authority request review-ready while a human grant contains execution-approval wording.

---

## 4. Remediation

Remediation added a RED regression proving that `build_codex_live_dispatch_authority_request(...)` returns `DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED` and a forbidden-wording blocked reason when human-grant text contains `APPROVED_FOR_LIVE_EXECUTION`.

The first focused run failed as expected:

```text
AssertionError: 'AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_EXECUTION' != 'DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED'
```

The implementation now scans request scope and separate human grant content during evaluation, not just validation. Forbidden authority wording becomes a blocked reason before readiness can be reported.

---

## 5. Post-Remediation Verification

Focused and full verification passed after remediation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_live_dispatch_authority_request -q
Ran 8 tests in 0.040s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_live_dispatch_readiness_gate -q
Ran 10 tests in 0.033s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_dispatch_envelope -q
Ran 11 tests in 0.018s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q
Ran 12 tests in 0.005s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
Ran 61 tests in 0.005s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 518 tests in 7.028s — OK

go test ./...
PASS

go vet ./...
PASS

git diff --check
PASS
```

---

## 6. Final Verdict

**PASS after remediation.**

BLK-SYSTEM-041 creates a fail-closed non-executing authority-request package and disabled adapter fixture only. It does not authorize live Codex execution, BLK-pipe dispatch, source mutation, protected-vault access, production BLK-test MCP, BEO publication, RTM generation, drift rejection, network/model/cyber/browser tooling, package-manager execution, or production sandbox/firewall/host-secret-isolation claims.

No protected BLK-req body reads occurred during the sprint or hostile review.
