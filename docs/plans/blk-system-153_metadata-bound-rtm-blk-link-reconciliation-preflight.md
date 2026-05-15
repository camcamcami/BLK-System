# BLK-SYSTEM-153 — Metadata-Bound RTM / blk-link Reconciliation Preflight

## Goal

Create one review-only preflight package for the operator-selected RTM / `blk-link` reconciliation path after BLK-SYSTEM-152 BEO publication finality.

## Scope

- Add a deterministic Python fixture that selects the metadata-bound RTM / `blk-link` reconciliation path as **preflight only**.
- Bind the preflight to exact BLK-SYSTEM-152 finality evidence and the current authority index.
- Require metadata/hash-only evidence for future reconciliation.
- Preserve denials for protected-body access, RTM generation/execution, drift rejection, coverage truth, reusable production `blk-link`, signer/storage/ledger reuse, runtime tooling, and source/Git mutation.
- Update BLK-077, BLK-079, and executable current-state surfaces only enough to show the selected preflight is complete and the next authority step remains ungranted.

## Files

Expected additions:

- `python/metadata_bound_rtm_blk_link_reconciliation_preflight.py`
- `python/test_metadata_bound_rtm_blk_link_reconciliation_preflight.py`
- `docs/outcomes/BLK-SYSTEM-153_sprint-closeout.md`

Expected updates:

- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/blk_authority_resumption_preflight.py`
- `python/test_blk_authority_resumption_preflight.py`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`

## Validation

- RED first: focused tests fail because the preflight module does not exist.
- GREEN: focused tests pass for the new preflight and current-state updates.
- Hostile audit: probe authority laundering, protected-body snippets/paths, drift/coverage claims, reusable `blk-link`, signer/storage/ledger reuse, and runtime/source/Git/tooling side effects.
- Final verification: focused suites, full Python discovery, Go tests/vet if meaningful, and `git diff --check`.

## Authority Boundary

This sprint does **not** authorize RTM generation, production `blk-link` execution, drift rejection, coverage truth, protected BLK-req body reads/copying/parsing/hashing/scanning/mutation, reusable publication/signing/storage/ledger authority, rollback/revocation/supersession, BLK-pipe/BLK-test/Codex runtime, target/source/Git mutation, package/network/model/browser/cyber tooling, or production-isolation claims.

## Documentation Burden

No new `docs/BLK-153_*.md` is warranted. One sprint closeout is sufficient.
