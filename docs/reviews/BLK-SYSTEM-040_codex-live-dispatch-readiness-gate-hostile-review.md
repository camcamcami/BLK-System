# BLK-SYSTEM-040 — Codex Live-Dispatch Readiness Gate Hostile Review

**Status:** PASS after remediation
**Date:** 2026-05-09T14:34:21+10:00
**Sprint:** BLK-SYSTEM-040 — Codex live-dispatch readiness gate

---

## 1. Review Scope

This hostile review examined the BLK-SYSTEM-040 doctrine boundary, readiness-gate fixture implementation, and tests:

```text
docs/BLK-042_codex-live-dispatch-readiness-gate-boundary.md
python/blk_codex_live_dispatch_readiness_gate.py
python/test_blk_codex_live_dispatch_readiness_gate.py
python/test_active_doctrine_review_gates.py
```

The review objective was to determine whether the sprint accidentally created live Codex execution authority, BLK-pipe dispatch authority, protected-vault access, BEO/RTM authority, readiness-as-execution laundering, or production sandbox claims.

---

## 2. Hostile Questions and Findings

### 2.1 Does the helper start subprocesses, call Codex, call Git, create worktrees, call BLK-pipe, invoke package managers, or inspect protected vaults?

**Verdict:** PASS.

`python/blk_codex_live_dispatch_readiness_gate.py` imports only:

```text
__future__.annotations
datetime.datetime
pathlib.PurePosixPath
typing.Any
blk_codex_dispatch_envelope.validate_codex_deterministic_dispatch_envelope
```

AST tests reject live-surface imports and calls for subprocess, shell, socket, network clients, `system`, `popen`, `run`, `Popen`, `call`, `check_call`, `check_output`, `exec`, `eval`, and `__import__`.

### 2.2 Can `READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION` become execution approval?

**Verdict:** PASS.

The fixture always records:

```text
execution_authorized: false
codex_subprocess_started: false
blk_pipe_dispatched: false
source_mutation_authorized: false
```

Tests reject direct attempts to change those flags and reject `READY_FOR_EXECUTION` wording as authority laundering.

### 2.3 Can missing/stale/replayed runtime approval pass?

**Verdict:** PASS.

Missing runtime approval returns `BLOCKED_NOT_AUTHORIZED`. Expired approvals, replayed runtime approval IDs, replayed readiness run IDs, and omitted replay-state inputs fail closed.

### 2.4 Can missing readiness prerequisites pass?

**Verdict:** PASS.

Missing BLK-pipe wiring plan, containment evidence, validation execution plan, telemetry persistence plan, rollback plan, monitoring plan, operator controls, failure ceiling, or hostile audit evidence returns `BLOCKED_NOT_AUTHORIZED` with operator-visible reasons.

### 2.5 Can malformed evidence paths or execution-authority status pass?

**Verdict:** PASS.

Evidence artifact references must be bounded relative paths under `artifacts/codex-readiness/`. Absolute paths, parent traversal, protected-vault paths, invalid evidence status, and execution-authority strings block readiness.

### 2.6 Can generic authority-laundering keys/strings bypass recursive scanning?

**Verdict:** PASS after remediation.

See blocker below.

---

## 3. Blocker Found During Review

**Blocker:** The original `validate_codex_live_dispatch_readiness_gate(...)` recursive authority scanner was not usable as a final validator for a valid record because it recursed into the embedded BLK-041/BLK-040 fixture and treated legitimate advisory keys such as `sandbox_authority` as forbidden.

At the same time, the scanner had a broad exception for a generic `authority` key. That could mask arbitrary nested metadata such as:

```text
metadata.authority = APPROVED
metadata.authority = EXECUTION_AUTHORITY_GRANTED
```

This was blocker-class because hostile review needs the validator to both accept valid readiness fixtures and reject generic authority laundering.

---

## 4. Remediation

Remediation added a RED regression proving a valid readiness record must pass `validate_codex_live_dispatch_readiness_gate(...)` unchanged.

Remediation also added authority-laundering regression cases for:

```text
metadata.authority = APPROVED
metadata.authority = EXECUTION_AUTHORITY_GRANTED
```

Then the scanner was tightened:

1. legitimate BLK-040/BLK-041 advisory fixture keys are explicit exceptions;
2. generic `authority` is no longer globally trusted;
3. `authority` is accepted only when its value is exactly `REVIEW_ONLY_NOT_EXECUTION`;
4. arbitrary authority-like metadata keys or execution-authority strings still fail closed.

---

## 5. Post-Remediation Verification

Focused and full verification passed after remediation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_live_dispatch_readiness_gate -q
Ran 10 tests in 0.032s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_dispatch_envelope -q
Ran 11 tests in 0.018s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q
Ran 12 tests in 0.005s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
Ran 60 tests in 0.004s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 509 tests in 7.014s — OK

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

BLK-SYSTEM-040 creates a fail-closed non-executing readiness gate fixture only. It does not authorize live Codex execution, BLK-pipe dispatch, source mutation, protected-vault access, production BLK-test MCP, authoritative BEO publication, RTM generation, drift rejection, network/model/cyber/browser tooling, package-manager execution, or production sandbox/firewall/host-secret-isolation claims.

No protected BLK-req body reads occurred during the sprint or hostile review.
