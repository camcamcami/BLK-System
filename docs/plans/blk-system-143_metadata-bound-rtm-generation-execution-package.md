# BLK-SYSTEM-143 — Metadata-Bound RTM Generation Execution Package Plan

## Objective

Execute the next production-driving BLK-System sprint under the lean documentation model by creating one bounded, deterministic RTM-generation execution package that consumes the exact BLK-SYSTEM-142 request.

## Scope

- Consume `RTM-GENERATION-AUTHORITY-REQUEST-142-001` by exact package ID and canonical package hash only.
- Capture exact operator approval as preflight inside the package rather than creating an approval-only micro-sprint.
- Assign and consume `RUN-BLK-SYSTEM-143-RTM-GENERATION-001` inside the same package.
- Emit metadata-bound RTM-generation record evidence for exact trace identities and hashes only.
- Update BLK-077, BLK-079, and executable current-state gates to move the frontier to post-execution reconciliation.
- Write exactly one sprint closeout in `docs/outcomes/BLK-SYSTEM-143_sprint-closeout.md`.

## Non-Authority Boundary

This sprint does not authorize drift rejection, authoritative coverage truth, reusable production `blk-link`, protected BLK-req body reads/copy/parse/hash/scan, active-vault filesystem reads/scans, signer/storage/ledger/rollback behavior, BEB dispatch, BEO closeout/publication, target/source/Git mutation outside this repository change, BLK-pipe/BLK-test/Codex runtime, package/network/model/browser/cyber tooling, or production-isolation claims.

## TDD / Verification Plan

1. RED: add `python/test_metadata_bound_rtm_generation_execution_package.py` with exact approval/run/record expectations and hostile negative cases.
2. GREEN: implement `python/metadata_bound_rtm_generation_execution_package.py` with closed schemas, canonical hash binding, exact IDs, timestamp-window binding, and false side-effect flags.
3. Reconcile current-state gates and lean docs.
4. Run focused tests, hostile audit, full Python suite, `go test ./...`, `go vet ./...`, and `git diff --check`.
