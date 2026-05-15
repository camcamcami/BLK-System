# BLK-SYSTEM-147 — Hardening-Only Regression Sweep Sprint Closeout

**Status:** Complete
**Date:** 2026-05-15T21:33:44+10:00
**Commit:** this commit (`test: harden lean index regression gates`)

## 1. Objective

Prove the BLK-SYSTEM-146 lean current-state/index model stays stable under regression pressure and closes authority-smuggling gaps without reopening any authority rung.

## 2. Files Changed

- `docs/plans/blk-system-147_hardening-only-regression-sweep.md`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_active_doctrine_review_gates.py`
- `python/test_lean_documentation_policy.py`
- `docs/outcomes/BLK-SYSTEM-147_sprint-closeout.md`

## 3. Implementation Summary

- Added BLK-SYSTEM-147 hardening-only markers to BLK-077 and BLK-079 without adding ledger content.
- Extended current-state authority probes for percent-encoded, compact/camel, and protected-path variants.
- Added bounded percent-decoding inside the current-state validator without introducing live/network imports.
- Added compact-token denials for `publishBEO`, RTM-generation authorization, drift-rejection execution, production `blk-link` enablement, and encoded protected active requirement paths.
- Extended lean one-closeout policy to BLK-SYSTEM-147.
- Added stale frontier regression coverage for `NEXT_FRONTIER_NARROW_POST_RTM_AUTHORITY_DECISION_NOT_GRANTED`.

## 4. Verification

RED evidence:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_current_state_authority_index python.test_lean_documentation_policy python.test_active_doctrine_review_gates
FAILED (failures=3)
Representative failures: encoded BEO publication authority was not rejected; BLK-SYSTEM-147 roadmap marker missing; BLK-SYSTEM-147 closeout missing.
```

GREEN / final verification:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_current_state_authority_index python.test_active_doctrine_review_gates python.test_lean_documentation_policy
Ran 162 tests in 0.116s
OK (skipped=34)

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
Ran 1168 tests in 13.243s
OK (skipped=35)

go test ./... && go vet ./...
ok for all Go packages

git diff --check -- <changed paths>
diff_check_and_markdown_fences_pass
```

## 5. Hostile Review / Risk Check

Local hostile audit result:

```text
HOSTILE_AUDIT_PASS
```

Audit scope:

- BLK-077/079 remain lean and line-bounded.
- No BLK-147 sprint document exists.
- No per-task outcome docs exist.
- BLK-001 through BLK-006 remain untouched.
- Encoded/camel/compact authority wording fails closed.
- Hardening-only remains the active frontier.

## 6. Authority Boundary

BLK-SYSTEM-147 is hardening-only. It grants no BEB dispatch, BEO closeout/publication execution, live Codex/tactical LLM dispatch, BLK-pipe runtime, production BLK-test MCP, RTM generation, production `blk-link`, drift rejection, coverage truth, protected BLK-req body reads/copying/parsing/hashing/scanning/mutation, target/source/Git mutation outside this repository patch, signer/storage/ledger/rollback behavior, package/network/model/browser/cyber tooling, or production-isolation claim.

## 7. Documentation Burden Check

No `docs/BLK-147_*.md` sprint document was created. No per-task outcome docs were created. BLK-001 through BLK-006 were not changed. This is the single BLK-SYSTEM-147 outcome document.
