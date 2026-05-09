# BLK-SYSTEM-045 — Authority Frontier Selection Gate Hostile Review

**Status:** PASS after remediation
**Date:** 2026-05-09T20:02:26+10:00
**Sprint:** BLK-SYSTEM-045 — Authority Frontier Selection Gate
**Reviewed scope:** BLK-048 boundary, deterministic selection fixture, focused tests, active doctrine gate, and task outcomes.

---

## 1. Verdict

Final verdict: PASS after remediation.

The initial hostile review found blocker-class gaps in the selection fixture validator. Those gaps were remediated with RED/GREEN tests and implementation hardening before closeout.

---

## 2. Blockers Found and Remediated

### BLOCKER 1 — Negative prefix could hide positive runtime authority

Observed hostile probes:

```text
not runtime approval; APPROVED_FOR_LIVE_EXECUTION
not approval; RTM_GENERATION_APPROVAL
next sprint not approval; sprint-dispatch approval is runtime approval
```

Before remediation, the validator's broad negative early-return allowed these strings. Remediation now scans forbidden markers before allowing exact negative non-authority strings. Regression test: `test_negative_prefix_cannot_hide_positive_runtime_authority`.

### BLOCKER 2 — Split key/value authority laundering could pass

Observed hostile probes:

```text
runtime = approved
live = authorized
beo_publication = approved
rtm_generation = authorized
protected_body_read = allowed
```

Before remediation, key and value were scanned independently. Remediation added combined key/value authority laundering detection. Regression test: `test_split_key_value_authority_laundering_fails_closed`.

### BLOCKER 3 — Nested multi-frontier selection could pass

Observed hostile probes:

```text
decision_evidence.frontiers = [blk_test_fixed_tool_pilot_l3_l4, codex_live_dispatch_l3_smoke]
decision_evidence.secondary_frontier = codex_live_dispatch_l3_smoke
```

Before remediation, only top-level `selected_frontier` was checked. Remediation rejects nested frontier keys and frontier tokens outside the single canonical field. Regression test: `test_nested_frontier_selection_fails_closed`.

### BLOCKER 4 — Selected frontier governing docs were not enforced

Observed hostile probe:

```text
selected_frontier = codex_live_dispatch_l3_smoke
governing_docs = [BLK-048]
```

Before remediation, only BLK-048 was required. Remediation now requires frontier-specific governing document sets. Regression test: `test_selected_frontier_requires_its_governing_docs`.

---

## 3. Final Hostile Review Answers

1. **Can “next sprint,” sprint-dispatch approval, BLK-test request readiness, Codex review readiness, BEO fixture readiness, or RTM fixture readiness become runtime approval?** No after remediation.
2. **Can multiple frontiers pass?** No after remediation; nested and top-level multi-frontier forms fail closed.
3. **Can adjacent authorities be inherited?** No after remediation; exact excluded-authority set validation, key/value scanning, and forbidden marker scans block inheritance.
4. **Can recursive generic authority/approval/claim strings bypass validation?** No after remediation.
5. **Does the disabled activation adapter prove no side effects?** Yes for the fixture's no-runtime surface: it reports all Codex, BLK-pipe, BLK-test, source/Git mutation, protected-body, BEO, RTM, package/network/model/browser/cyber, shell, and production-isolation side-effect flags false.
6. **Is the next-step recommendation honest?** Yes: future runtime requires explicit human approval naming one frontier.

---

## 4. Verification

Final verification passed:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_authority_frontier_selection_gate -q
Ran 13 tests in 0.010s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
Ran 66 tests in 0.005s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 566 tests in 7.509s — OK

go test ./...
PASS

go vet ./...
PASS

git diff --check
PASS
```

---

## 5. Final Authority Boundary

BLK-SYSTEM-045 remains review/decision routing only. It does not authorize live Codex execution, Codex subprocess startup, BLK-pipe dispatch, production BLK-test MCP, live BLK-test server/client startup, fixed-tool execution, source/Git mutation, protected BLK-req body reads/copying/scanning, BEO publication, RTM generation, drift rejection, package-manager/network/model/browser/cyber tooling, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, or production isolation claims.
