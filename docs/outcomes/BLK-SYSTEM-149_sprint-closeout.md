# BLK-SYSTEM-149 — Authority-Smuggling Scanner Centralization Sprint Closeout

**Status:** Complete
**Date:** 2026-05-15
**Commit:** this commit (`feat: complete blk-system 148-150 hardening sequence`)

## 1. Objective

Centralize authority-smuggling normalization and scanning so current-state and future authority preflight gates do not duplicate fragile denylist and percent-decoding logic.

## 2. Files Changed

- `docs/plans/blk-system-149_authority-smuggling-scanner-centralization.md`
- `python/blk_authority_smuggling.py`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_authority_smuggling.py`
- `python/test_blk_current_state_authority_index.py`

## 3. Implementation Summary

- Added reusable scanner module `blk_authority_smuggling.py`.
- Moved compact/camel/percent-decoding authority scans out of the current-state index.
- Routed `validate_current_state_authority_index` through the shared scanner while preserving the exact denied-flag false contract.
- Extended scanning to percent-decoded keys as well as values after the BLK-SYSTEM-150 RED test exposed encoded protected-path key laundering.

## 4. Verification

- RED observed: `python.test_blk_authority_smuggling` initially failed because `blk_authority_smuggling` did not exist.
- GREEN observed: scanner and current-state focused tests passed.
- Final focused verification: `24 tests OK` across scanner, resumption preflight, current-state index, and lean policy suites.
- Final full Python verification: `1172 tests OK / 35 skipped`.
- Go verification: `go test ./... && go vet ./...` OK.

## 5. Hostile Review / Risk Check

- Scanner rejects encoded/compact authority claims including `BEO%20publication%20authorized`, `publish%2542EO`, `RTMGenerationAuthorized`, `driftRejectionExecuted`, `productionBlkLinkEnabled`, and encoded `docs/.../requirements/active` keys.
- Denial prose remains allowed when it states authority is not granted.
- No runtime or production authority is added by centralizing the scanner.

## 6. Authority Boundary

This sprint is hardening-only. It selects no authority rung and grants no runtime, BEB/BEO, RTM, drift, publication, protected-body, signer/storage/ledger, tooling, BLK-pipe/BLK-test/Codex, target/source/Git mutation outside this repo patch, or production-isolation authority.

## 7. Documentation Burden Check

No new `docs/BLK-149_*.md` was created. Exactly one sprint outcome was produced for BLK-SYSTEM-149.
