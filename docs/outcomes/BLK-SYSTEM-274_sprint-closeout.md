# BLK-SYSTEM-274 — RTM / blk-link Approval Preflight Blocked Sprint Closeout

**Status:** Complete
**Date:** 2026-05-20
**Commit:** this commit (`feat: prepare blk-system 272-275 request challenge package`)

## 1. Objective
Record that the operator's generic package directive is not RTM / `blk-link` approval, and harden short-Approve validation against pre-issued, expired, forged, or authority-laundered replies.

## 2. Files Changed
- `python/rtm_blk_link_drift_coverage_request_package_272_275.py`
- `python/test_rtm_blk_link_drift_coverage_request_package_272_275.py`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_lean_documentation_policy.py`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`

## 3. Implementation Summary
Added `evaluate_rtm_blk_link_drift_coverage_approval_preflight_274(...)`. The canonical package directive path returns `NOT_BOUND_APPROVE_FOR_CHALLENGE`; `Approve` only matches inside the challenge window and still performs no execution. Hostile-review regressions cover pre-issued `Approve`, expired `Approve`, wrong operator identity, forged BOUND preflight hash, and authority/protected-path laundering in replies.

Hash evidence:
- generic-block preflight hash: `sha256:a3ab1310a900b9ee8fa99b872d782ccdfb3af4f05d4cbc135a032b913cbfa912`
- next preflight-safe statuses: `NOT_BOUND_APPROVE_FOR_CHALLENGE`, `CHALLENGE_NOT_YET_ISSUED_NOT_APPROVAL`, `EXPIRED_CHALLENGE_NOT_APPROVAL`, `BOUND_APPROVE_FOR_CHALLENGE`

## 4. Verification
- RED: `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_rtm_blk_link_drift_coverage_request_package_272_275` failed first with `ModuleNotFoundError` for the missing 272..275 module.
- GREEN: same focused package command passed: `Ran 4 tests ... OK`.
- Hostile review remediation: added regressions and code checks for pre-issued `Approve` replies and forged BOUND preflight records with non-Approve hashes; focused package command passed again: `Ran 4 tests ... OK`.
- Focused package/current-state/lean-doc gate: `python -m unittest python.test_rtm_blk_link_drift_coverage_request_package_272_275 python.test_blk_current_state_authority_index python.test_lean_documentation_policy` passed: `Ran 28 tests ... OK`.
- Full Python discovery: `TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover -s python -p 'test_*.py'` passed: `Ran 1460 tests in 17.705s — OK (skipped=35)`.
- Go verification: `go test ./...` passed for all packages.
- Whitespace verification: `git diff --check -- <exact changed paths>` passed with no output.

## 5. Hostile Review / Risk Check
Independent hostile review initially returned BLOCKERS, not PASS. Remediation added:
- `Approve` before challenge `issued_at` is `CHALLENGE_NOT_YET_ISSUED_NOT_APPROVAL` and does not set `short_approve_matched`.
- BOUND preflight records require `operator_reply_hash == sha256("Approve")` and `issued_at <= evaluated_at < expires_at`.
- The RTM / `blk-link` current-state cutline now explicitly denies run-ID reservation/consumption.
- Active-doc/current-state tests were updated for BLK-SYSTEM-272..275 and the current frontier.
Follow-up hostile re-review returned PASS: pre-issued `Approve` is blocked, forged BOUND preflight is rejected, closeouts are present, and the executable RTM / `blk-link` cutline contains `no RTM generation` plus `no run-ID reservation or consumption`.
No code path performs RTM generation, production `blk-link`, drift rejection, coverage truth, protected-body reads, runtime/tooling, run-ID reservation/consumption, or target/source/Git mutation.

## 6. Authority Boundary
This sprint grants no RTM generation, no production `blk-link`, no drift rejection, no coverage truth, no protected-body read/copy/parse/hash/scan/mutation, no active-vault comparison, no run-ID reservation or consumption, no BEO publication reuse, no signer/storage/ledger reuse, no BLK-pipe/BLK-test/Codex runtime, no package/network/model/browser/cyber tooling, no production-isolation claim, and no target/source/Git mutation.

## 7. Documentation Burden Check
No new BLK-### document was created. Exactly one outcome doc was produced for this numbered sprint; no task outcome docs were introduced.
