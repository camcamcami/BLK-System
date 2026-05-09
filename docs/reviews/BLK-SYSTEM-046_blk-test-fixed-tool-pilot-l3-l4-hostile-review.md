# BLK-SYSTEM-046 — BLK-test Fixed-Tool Pilot L3/L4 Hostile Review

**Status:** PASS after remediation
**Date:** 2026-05-09T20:38:30+10:00
**Sprint:** BLK-SYSTEM-046 — BLK-test Fixed-Tool Pilot L3/L4
**Reviewed scope:** BLK-049 boundary, L3/L4 Python fixture, focused tests, active doctrine gate, and task outcomes.

---

## 1. Verdict

Final verdict: PASS after remediation.

The initial hostile review found five blocker-class gaps. Each blocker was remediated with RED/GREEN tests and implementation hardening before closeout.

---

## 2. Blockers Found and Remediated

### BLOCKER 1 — Approval-kind laundering could authorize BLK-test pilot runtime

Observed hostile probe: `approval_kind = blk-pipe-dispatch-approval` returned `BLK_TEST_L3_SYNTHETIC_PREFLIGHT_ACCEPTED`.

Risk: BLK-pipe, BEO, RTM, BLK-020 first-smoke, sprint-dispatch, or generic runtime approval could be laundered into BLK-test pilot approval.

Remediation:

- required exact approval kind `blk-test-fixed-tool-pilot-l3-synthetic`;
- added regression test `test_laundered_approval_kinds_and_authority_claim_fields_fail_closed` covering BLK-pipe, BEO, RTM, drift, BLK-020, sprint-dispatch, and generic runtime approval kinds.

### BLOCKER 2 — Authority-claim fields were accepted and sanitized after acceptance

Observed hostile probes: tainted request/extension fields such as `beo_publication = PUBLISHED`, `rtm_status = GENERATED`, `coverage_status = ACTIVE_TRUTH`, and `production_isolation_claimed = true` could reach accepted preflight.

Risk: sanitizing output after acceptance is not enough for an authority-bearing runtime boundary; tainted input must fail before process start.

Remediation:

- added strict schema checks for authorization requests, approval records, `sprint046_pilot` extensions, workspace identity, and timeout/output profile;
- required authority booleans to be false, `beo_publication` to be `DRAFT_ONLY`, `rtm_status` to be `NOT_GENERATED`, and no unknown extension authority fields;
- added RED/GREEN coverage for tainted BEO and production-isolation fields.

### BLOCKER 3 — Replay IDs were consumed only after successful cleanup

Observed hostile path: if the fixed-tool process started and cleanup failed, the approval/run IDs were not marked used.

Risk: same approval/run could be retried after runtime side effects occurred.

Remediation:

- moved replay consumption to after all pre-start validation and workspace ownership checks but before process start;
- never unconsumes replay on FAIL/BLOCKED/FATAL/output flood/timeout/cleanup failure;
- returns `replay_consumed: true`;
- added `test_cleanup_failure_is_non_success_and_still_consumes_replay_ids`.

### BLOCKER 4 — Arbitrary marked directories could be accepted and recursively deleted

Observed hostile path: any non-git directory outside `/home/dad/BLK-System` with `.blk-system-046-synthetic-workspace` could be accepted and then deleted.

Risk: fake marker could convert fixture into an arbitrary deletion primitive.

Remediation:

- bound `approved_workspace_path` and `workspace_marker_nonce` into `workspace_identity` and the envelope hash;
- required marker content to equal the approved nonce;
- rejected path mismatch and nonce mismatch before process start;
- added `test_unowned_workspace_marker_and_path_mismatch_are_rejected_before_cleanup`.

### BLOCKER 5 — Process/output/operator-control proof was under-scoped

Observed gap: initial tests covered output flood but not timeout/operator stop evidence under the BLK-SYSTEM-046 boundary.

Risk: BLK-047 process-control obligations were inherited by prose rather than pinned under the new boundary.

Remediation:

- added BLK-SYSTEM-046 timeout regression `test_timeout_is_non_success_and_uses_fixed_harness_operator_stop_control`;
- exposed evidence marker `operator_stop_control: fixed_harness_process_group_timeout_kill`;
- preserved bounded output flood regression.

---

## 3. Final Hostile Review Answers

1. **Can sprint-dispatch, BLK-047 request readiness, BLK-048 selection readiness, Codex, BLK-pipe, BEO, RTM, or BLK-020 evidence become BLK-test pilot approval?** No after remediation; exact approval kind is enforced and adjacent approval markers fail closed.
2. **Can L4 real-repo runtime start without exact target approval?** No; `target_mode=real_repo_l4` raises and `evaluate_l4_real_repo_pilot_preflight` reports blocked with no side effects.
3. **Can arbitrary shell, caller-supplied commands, wildcard tools, package/network/model/browser/cyber tooling, or dynamic tool expansion bypass the fixed registry?** No; only `run_ast_validation` is accepted and inherited fixed harness rejects caller-supplied command expansion.
4. **Can protected-vault bodies or active-vault paths be read or compared?** No; workspace/protected-prefix checks are path/metadata only and output preserves `active_vault_read: false`.
5. **Can PASS publish BEOs, generate RTM, mutate source, claim coverage/drift truth, or claim production isolation?** No; strict input schema and output fields preserve evidence-only semantics.
6. **Are replay state, output bounds, timeout handling, cleanup, and operator controls proven?** Yes for the L3 synthetic slice: replay is consumed before process start, output flood is bounded, timeout is non-success, cleanup failure blocks success and still consumes replay, and operator stop control is pinned to the fixed harness process-group timeout kill path.

---

## 4. Final Verification

Final verification passed:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_test_fixed_tool_pilot_l3_l4 -q
Ran 11 tests in 1.107s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_test_fixed_tool_pilot_authority_request -q
Ran 11 tests in 0.008s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
Ran 67 tests in 0.005s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 578 tests in 8.610s — OK

go test ./...
PASS

go vet ./...
PASS

git diff --check
PASS
```

---

## 5. Final Authority Boundary

BLK-SYSTEM-046 remains a bounded L3 synthetic fixed-tool pilot only. L4 real-repo pilot runtime remains blocked pending exact target approval. The sprint does not authorize production/generic BLK-test MCP, arbitrary shell, source/Git mutation by BLK-test, protected-body reads, BEO publication, RTM generation, drift rejection, package/network/model/browser/cyber tooling, or production isolation claims.
