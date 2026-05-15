# BLK-SYSTEM-140 — Exact Active-Vault Hash Comparison Execution Plan

**Status:** Active execution plan
**Scope:** BLK-SYSTEM-140 only

## Goal

Consume the exact BLK-SYSTEM-139 approval capture and reserved run ID to emit one record-only metadata/hash comparison package.

## Scope

- Consume `ACTIVE-VAULT-HASH-COMPARISON-APPROVAL-CAPTURE-139-001` by exact ID and canonical hash.
- Consume `RUN-BLK-SYSTEM-140-ACTIVE-VAULT-HASH-COMPARISON-001` once inside the returned evidence package.
- Compare caller-supplied metadata records against the exact trace identities approved in BLK-SYSTEM-139.
- Emit match/mismatch evidence without treating mismatch as drift rejection or authoritative drift decision.

## Non-Authority Boundary

BLK-SYSTEM-140 must not read/copy/parse/hash/scan protected requirement bodies, read active-vault files directly, generate RTM, reject drift, establish coverage truth, run reusable production `blk-link`, mutate source/Git, run BLK-pipe/BLK-test/Codex/tooling, perform signer/storage/ledger behavior, or claim production isolation.

## Expected Files

- `python/active_vault_hash_comparison_execution_record.py`
- `python/test_active_vault_hash_comparison_execution_record.py`
- concise updates to `docs/BLK-077_blk-system-post-078-roadmap.md`, `docs/BLK-079_post-078-current-state-authority-index.md`, `python/blk_current_state_authority_index.py`, and focused gates
- `docs/outcomes/BLK-SYSTEM-140_sprint-closeout.md`

## Validation

- RED/GREEN focused unittest for BLK-SYSTEM-140.
- Hostile audit for exact approval/run binding, replay/stale/expiry, protected-body/path rejection, metadata bijection, mismatch-not-drift semantics, and forbidden side effects.
- Focused current-state/lean-doc/doctrine gates.
- Full Python unittest discovery.

## Documentation Burden Rule

No new BLK-### document. One sprint closeout only.
