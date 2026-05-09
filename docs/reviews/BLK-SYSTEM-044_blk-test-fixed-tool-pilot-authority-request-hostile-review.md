# BLK-SYSTEM-044 — BLK-test Fixed-Tool Pilot Authority Request Hostile Review

**Status:** PASS after remediation
**Date:** 2026-05-09T19:28:48+10:00
**Sprint:** BLK-SYSTEM-044 — BLK-test Fixed-Tool Pilot Authority Request
**Reviewed scope:** BLK-047 boundary, deterministic request fixture, focused tests, active doctrine gate, and task outcomes.

---

## 1. Verdict

Final verdict: PASS after remediation.

The initial hostile review found blocker-class gaps in the request fixture validator. Those gaps were remediated with new RED/GREEN tests and implementation hardening before closeout.

---

## 2. Hostile Review Questions

### Q1 — Does the sprint accidentally grant runtime BLK-test authority?

Final answer: No.

BLK-047 and the fixture preserve review-only status. The fixture sets and re-sets all runtime side-effect and adjacent authority flags to false. The disabled adapter returns only `BLK_TEST_PILOT_DISABLED_NOT_AUTHORIZED` and no side-effect flags.

### Q2 — Are approvals separated from Codex, BLK-pipe, BLK-020, BEO, and RTM?

Final answer: Yes.

The package requires separate future BLK-test-specific approval and rejects adjacent approval reuse markers, including Codex live approval, BLK-pipe execution approval, BLK-020 historical first-smoke approval, BEO publication approval, RTM generation approval, and drift rejection authority.

### Q3 — Does the request require physical/isolation proof, replay/expiry, fixed-tool constraints, timeout/output caps, cleanup proof, operator controls, and hostile review before runtime?

Final answer: Yes after remediation.

The validator now requires exact proof markers for fixed-tool registry, source binding, physical isolation, process/output controls, and evidence semantics. Non-empty placeholder lists no longer pass.

### Q4 — Can recursive generic authority-laundering keys/strings bypass validation?

Final answer: No after remediation.

The validator rejects recursive authority-like keys and positive runtime approval language. Regression tests cover `authority`, `approval_status`, `claim`, `APPROVED_FOR_LIVE_BLK_TEST`, `production sandbox is enforced`, `runtime pilot approved by operator; live pilot allowed`, and nested denied authority flags.

### Q5 — Does the disabled adapter prove no side effects rather than merely reporting blocked status?

Final answer: Yes after remediation.

The adapter now reports a complete false side-effect surface for MCP server/client startup, fixed-tool execution, source/Git mutation, protected body read/copy/scan, BEO publication, RTM generation, drift rejection, network/model/browser/cyber/package-manager calls, arbitrary shell, and production isolation claims.

---

## 3. Blockers Found and Remediated

### BLOCKER 1 — Generic authority-laundering strings could pass validation

Observed hostile probe:

```text
future_approval_envelope["grant_text"] = "runtime pilot approved by operator; live pilot allowed"
```

Before remediation, this evaluated as review-ready. Remediation added:

- closed nested `future_approval_envelope` schema;
- generic positive runtime/live/execution/transport/pilot wording detection;
- regression test `test_generic_runtime_approval_language_in_nested_strings_fails_closed`.

### BLOCKER 2 — `excluded_adjacent_authorities` accepted extra unscanned values

Observed hostile probe:

```text
excluded_adjacent_authorities.append("APPROVED_FOR_LIVE_EXECUTION")
```

Before remediation, this evaluated as review-ready. Remediation changed required-set validation from missing-only to exact-set validation and added `test_excluded_adjacent_authorities_rejects_extra_values`.

### BLOCKER 3 — Proof obligations accepted meaningless non-empty placeholders

Observed hostile probe:

```text
proof_obligations[*] = ["ok"]
fixed_tool_registry_constraints = ["ok"]
```

Before remediation, this evaluated as review-ready. Remediation added exact required marker checks for every proof section and fixed-tool constraint list, plus `test_proof_obligations_and_fixed_tool_constraints_require_required_content`.

### NON-BLOCKER HARDENING — Disabled adapter side-effect surface was incomplete

Remediation expanded the adapter returned false side-effect keyset and test assertions to include Git mutation, protected body copy/scan, drift rejection, model/browser/cyber calls, arbitrary shell, and production isolation claims.

---

## 4. Verification

Final verification passed:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_test_fixed_tool_pilot_authority_request -q
Ran 11 tests in 0.008s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
Ran 65 tests in 0.005s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 552 tests in 7.503s — OK

go test ./...
PASS

go vet ./...
PASS

git diff --check
PASS
```

---

## 5. Final Authority Boundary

BLK-SYSTEM-044 remains review/request fixture only. It does not authorize production BLK-test MCP, live BLK-test server/client startup, new smoke runs, BLK-020 replay, fixed-tool execution, arbitrary shell, source mutation by BLK-test, protected BLK-req body reads/copying/scanning, BEO publication, RTM generation, drift rejection, package-manager/network/model/browser/cyber tooling, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.
