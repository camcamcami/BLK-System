# BLK-SYSTEM-325 — Overall 9/10 Directive Guard and Scanner Hardening Sprint Closeout

**Status:** Complete
**Date:** 2026-05-22
**Commit:** this commit (`fix: guard overall 9 directive authority`)

## 1. Objective

The operator asked to plan and execute all BLK-System sprints needed to get BLK-System to 9/10 overall. This sprint records that practical-overall target without laundering the broad directive into BEO publication, run-ID movement, signer/storage/ledger action, RTM generation, production `blk-link`, protected-body access, runtime/tooling, or broad mutation authority.

## 2. Files Changed

- `python/blk_authority_smuggling.py`
- `python/test_blk_authority_smuggling.py`
- `python/blk_system_overall_9_guard_325.py`
- `python/test_blk_system_overall_9_guard_325.py`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_lean_documentation_policy.py`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `docs/outcomes/BLK-SYSTEM-325_sprint-closeout.md`

## 3. Implementation Summary

- Added BLK-SYSTEM-325 package logic with canonical guard hash `sha256:18f9550996bc0388e67666237c0e95d81906ce30162c184401149eeffb31dd3e`.
- Bound the exact operator directive `plan and execute all blk-system sprints to get blk-system to 9/10 overall` as repository-development direction only.
- Recorded the truthful scoring cutline: current practical overall is still a 7/10 baseline; the 9/10 overall target requires a separate exact no-clock side-effect decision for the current verified-loop BEO publication lane before RTM / production `blk-link` can reopen.
- Hardened the shared authority-smuggling scanner for run-ID reservation/consumption, signature generation, signer/storage/ledger action, protected-body hashing, and relay/message dispatch wording.
- Advanced BLK-077, BLK-079, and the executable current-state index to the BLK-SYSTEM-325 frontier.

## 4. Verification

RED evidence:

```text
python.test_blk_authority_smuggling initially failed because run-ID/signature/protected-body side-effect claims were not detected.
python.test_blk_system_overall_9_guard_325 initially failed because the BLK-SYSTEM-325 module did not exist.
python.test_blk_current_state_authority_index and python.test_lean_documentation_policy initially failed because BLK-077/079/current-state and the BLK-SYSTEM-325 closeout had not been updated.
```

GREEN focused verification completed:

```text
TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python -m unittest python.test_blk_authority_smuggling python.test_blk_system_overall_9_guard_325 python.test_blk_current_state_authority_index python.test_lean_documentation_policy python.test_exact_beo_publication_approval_capture_264_265 python.test_exact_beo_publication_run_package_266_268 python.test_exact_beo_publication_execution_package_269_271 python.test_rtm_blk_link_drift_coverage_request_package_272_275 python.test_rtm_blk_link_drift_coverage_refresh_challenge_package_276_278 python.test_rtm_blk_link_drift_coverage_refresh_challenge_package_279_281 -v
Ran 51 tests
OK
```

Full Python verification completed:

```text
TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python -m unittest discover -s python -p 'test_*.py'
Ran 1550 tests in 502.321s
OK (skipped=35)
```

## 5. Hostile Review / Risk Check

Hostile review classified the broad overall-9 directive as safe only when treated as BLK-System repository-development direction under standing approval, not as any side-effect grant. Review then found two concrete scanner blockers, both remediated with regression coverage:

- Canonical safe run-ID markers are exact-only; appended claims such as `BLK_SYSTEM_264_NO_RUN_ID_RESERVED_OR_CONSUMED_RUNIDRESERVED` are rejected.
- Run-ID, signature, protected-body hash, signer/storage/ledger, relay/message dispatch, and Kuronode mutation approval/execution variants are rejected in both strings and keys.
- Final hostile re-probe confirmed the blocker probes are rejected while exact denial markers such as `NO_RUN_ID_RESERVED_OR_CONSUMED` still avoid false positives.
- The exact overall-9 directive remains development-only and cannot retarget lane decisions to `approved_by_all_sprints_directive`.
- The active docs preserve the 7/10 practical baseline and make the 9/10 overall target depend on a separate exact side-effect decision.

## 6. Authority Boundary

This sprint grants no BEB dispatch, BEO closeout execution, BEO publication, reusable BEO publication, run-ID reservation/consumption, signer/storage/ledger action or reuse, rollback/revocation/supersession, RTM generation, production `blk-link`, drift rejection, coverage truth, active-vault comparison, protected-body reads/copying/parsing/hashing/scanning/mutation, package/network/model/browser/cyber tooling, live Codex/BLK-pipe/BLK-test MCP runtime, relay/message dispatch, production-isolation claim, Kuronode mutation, or target/source/Git mutation outside exact BLK-System sprint discipline.

## 7. Documentation Burden Check

No new BLK-### root doctrine file was created. This sprint produced exactly one outcome document: `docs/outcomes/BLK-SYSTEM-325_sprint-closeout.md`.
