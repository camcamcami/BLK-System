# BLK-SYSTEM-145 — Authority Ladder Simplification / Hardening

## Lean scope

Stop the post-RTM authority ladder and perform hardening only. Do not request, approve, or execute a new production authority rung. Do not create a `docs/BLK-145_*.md` sprint document. Close with one sprint outcome only.

## Objective

Make the post-144 state harder to misuse and easier to maintain by pinning an explicit hardening-only mode after BLK-SYSTEM-144 reconciliation.

## Tasks

1. Add RED tests for a deterministic hardening-only policy package that consumes `POST-RTM-GENERATION-RECONCILIATION-144-001` by exact ID/hash and refuses any requested authority rung.
2. Implement `python/authority_ladder_hardening_policy.py` with closed schemas, canonical hash binding, defensive copies, and explicit false side-effect flags.
3. Update BLK-077, BLK-079, executable current-state index, active doctrine gates, and lean-doc gates so the active next frontier is hardening-only, not a post-RTM authority decision.
4. Run a hostile audit for authority creep, protected-body leakage, stale next-frontier wording, and documentation bloat.
5. Run focused and full verification, write exactly one closeout, commit, and push.

## Stop conditions

Stop if any change grants or asks for drift rejection, coverage truth, reusable production `blk-link`, protected-body access, BEB/BEO dispatch or closeout, signer/storage/ledger behavior, target/source/Git mutation beyond this repository sprint work, BLK-pipe/BLK-test/Codex/runtime execution, package/network/model/browser/cyber tooling, or production-isolation claims.
