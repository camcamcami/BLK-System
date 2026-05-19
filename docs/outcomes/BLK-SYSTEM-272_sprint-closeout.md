# BLK-SYSTEM-272 — RTM / blk-link Drift-Coverage Request Ready Sprint Closeout

**Status:** Complete
**Date:** 2026-05-20
**Commit:** this commit (`feat: prepare blk-system 272-275 request challenge package`)

## 1. Objective
Prepare a request-only RTM / production `blk-link` drift-coverage package after exact BEO publication finality evidence, without treating the request as approval or execution authority.

## 2. Files Changed
- `python/rtm_blk_link_drift_coverage_request_package_272_275.py`
- `python/test_rtm_blk_link_drift_coverage_request_package_272_275.py`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_lean_documentation_policy.py`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`

## 3. Implementation Summary
Added `build_rtm_blk_link_drift_coverage_request_272(...)`, binding canonical BLK-SYSTEM-271 reconciliation, BLK-SYSTEM-270 execution, finality-record hash, and receipt hashes into a request package. The request records metadata requirements and short-approval rules but captures no approval and reserves no run ID.

Hash evidence:
- request hash: `sha256:71a299dcecc0c2c2e5a617924ef6de67fce99cdfa96c682db1cfdd3a93295ee5`
- upstream BLK-SYSTEM-271 hash: `sha256:19195c218d30eb18b5343d40b3177e3c1cce3260c8519810b3e424cdccc1d49c`

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
