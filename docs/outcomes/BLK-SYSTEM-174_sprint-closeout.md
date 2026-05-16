# BLK-SYSTEM-174 — Protected-Body Verification Decision Request Sprint Closeout

**Status:** Complete
**Date:** 2026-05-16
**Commit:** this commit (`feat: advance protected-body verification frontier`)

## 1. Objective
Emit a request-only next-authority package for future exact protected-body verification decision approval after clean BLK-SYSTEM-173 reconciliation.

## 2. Files Changed
- `python/metadata_bound_drift_coverage_decision_ladder_172_174.py`
- `python/test_metadata_bound_drift_coverage_decision_ladder_172_174.py`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_lean_documentation_policy.py`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `docs/plans/blk-system-174_protected-body-verification-decision-request.md`
- `docs/outcomes/BLK-SYSTEM-174_sprint-closeout.md`

## 3. Implementation Summary
- Added BLK-SYSTEM-174 request-only builder and validator.
- Bound BLK-SYSTEM-174 to clean BLK-SYSTEM-173 reconciliation and canonical BLK-SYSTEM-172 evidence.
- Emitted authority request package hash `sha256:328c0d4a99020e7764d5f5bf834eb0c3f895801f883a22a8d67d5ca0375347ef`.
- Updated BLK-077, BLK-079, and executable current-state gates to make `NEXT_FRONTIER_PROTECTED_BODY_VERIFICATION_DECISION_APPROVAL_NOT_GRANTED` the active frontier.

## 4. Verification
```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_metadata_bound_drift_coverage_decision_ladder_172_174 python.test_blk_current_state_authority_index python.test_lean_documentation_policy
Ran 28 tests
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover -s python -p 'test_*.py' -v
Ran 1250 tests
OK (skipped=35)

go test ./...
ok all packages

git diff --check
PASS
```

## 5. Hostile Review / Risk Check
Hostile checks covered forged/rehashed upstream evidence, schema extras, exact proof/denial set equality and duplicate rejection, compact/camel authority-laundering keys, protected-body access claims, coverage-truth promotion, next-frontier grant smuggling, decision-window hash binding, defensive copies, side-effect flag defaults, and AST checks for live runtime/tooling/file access. Independent hostile review initially found operator-identity laundering gaps across 172/173/174 plus stale closeout placeholders; remediation added upstream operator identity binding, a 173 type/authority scan, negative regression probes, and a lean-doc placeholder gate. Targeted hostile re-review result: PASS, with no remaining concrete blockers.

## 6. Authority Boundary
BLK-SYSTEM-174 is request-only. It grants no approval capture, run-ID reservation/consumption, protected-body reads/copying/parsing/hashing/scanning, drift rejection, coverage truth, RTM generation, reusable production `blk-link`, BLK-pipe/BLK-test/Codex/tooling, target/source/Git mutation, signer/storage/ledger reuse, or production-isolation claim.

## 7. Documentation Burden Check
No new `docs/BLK-###` document was created. Exactly one sprint outcome was created for BLK-SYSTEM-174 and no per-task outcome documents were created.
