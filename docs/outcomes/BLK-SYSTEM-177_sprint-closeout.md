# BLK-SYSTEM-177 — Authority-Laundering Bypass Hardening Sprint Closeout

**Status:** Complete
**Date:** 2026-05-16
**Commit:** this commit (`feat: deliver protected-body verification engine`)

## 1. Objective
Harden only because hostile review found concrete bypasses in the BLK-175/176 feature batch.

## 2. Files Changed
- `python/protected_body_verification_decision_engine_175.py`
- `python/rtm_blk_link_protected_body_verification_integration_176.py`
- `python/test_protected_body_verification_decision_engine_175_176.py`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_lean_documentation_policy.py`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `docs/outcomes/BLK-SYSTEM-177_sprint-closeout.md`

## 3. Implementation Summary
- Added percent-decoding before BLK-176 freeform authority scans so encoded and double-encoded authority/protected-path text fails closed.
- Added regression coverage for encoded `integration_notes` authority laundering.
- Scanned supported `validation_errors` in the current-state validator instead of excluding it from recursive authority checks.
- Scanned active roadmap/current-state document text for authority-laundering phrases, not only required/stale markers.
- Updated active current-state marker to `BLK_SYSTEM_177_AUTHORITY_LAUNDERING_BYPASS_HARDENED`.

## 4. Verification
```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_protected_body_verification_decision_engine_175_176 python.test_blk_current_state_authority_index -v
Ran 24 tests
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py' -v
Ran 1257 tests
OK (skipped=35)

go test ./...
ok all packages

git diff --check
PASS

Local hostile audit probes:
- encoded BLK-176 integration note laundering rejected
- double-encoded protected path in BLK-176 integration notes rejected
- `validation_errors` authority text rejected
- active-doc authority text drift rejected
LOCAL_HOSTILE_AUDIT_PASS
```

## 5. Hostile Review / Risk Check
Independent hostile review identified three concrete blockers: encoded `integration_notes` laundering in BLK-176, supported-field `validation_errors` laundering in the current-state validator, and active-doc authority text drift not being scanned. All three were reproduced as RED regressions and remediated. A targeted delegated re-review timed out, so final confidence is based on focused regression tests plus local hostile repro probes listed above.

## 6. Authority Boundary
BLK-SYSTEM-177 is hardening only. It grants no protected-body text return, protected-file read/copy/parse/hash/scan, drift rejection, coverage truth, RTM generation, reusable production `blk-link`, BLK-pipe/BLK-test/Codex/tooling, target/source/Git mutation, signer/storage/ledger reuse, or production-isolation claim.

## 7. Documentation Burden Check
No new `docs/BLK-###` document was created. Exactly one sprint outcome was created for BLK-SYSTEM-177 and no per-task outcome documents were created.
