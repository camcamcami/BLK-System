# BLK-SYSTEM-137..139 — Active-Vault Hash Comparison Authority Ladder Plan

**Status:** Active execution plan
**Scope:** BLK-SYSTEM-137, BLK-SYSTEM-138, BLK-SYSTEM-139

## Goal

Move from post-execution reconciliation into the narrowest safe active-vault comparison path:

1. **137:** choose metadata/hash-only active-vault comparison as the next production-driving capability.
2. **138:** package an exact authority request for metadata/hash-only active-vault comparison.
3. **139:** capture exact approval or fail closed, reserving one future comparison run without executing it.

## Non-Authority Boundary

This sequence must not perform active-vault comparison, read protected requirement bodies, hash/copy/parse protected bodies, generate RTM, reject drift, establish coverage truth, run reusable production `blk-link`, mutate target/source/Git state, run BLK-pipe/BLK-test/Codex/tooling, write signer/storage/ledger state, or claim production isolation.

## Expected Files

- `python/active_vault_hash_comparison_decision_package.py`
- `python/active_vault_hash_comparison_authority_request.py`
- `python/active_vault_hash_comparison_approval_capture.py`
- `python/test_active_vault_hash_comparison_authority_ladder.py`
- `docs/outcomes/BLK-SYSTEM-137_sprint-closeout.md`
- `docs/outcomes/BLK-SYSTEM-138_sprint-closeout.md`
- `docs/outcomes/BLK-SYSTEM-139_sprint-closeout.md`
- concise updates to `docs/BLK-077_blk-system-post-078-roadmap.md`, `docs/BLK-079_post-078-current-state-authority-index.md`, and executable current-state/doctrine gates.

## Validation

- RED/GREEN focused unittest for the new authority ladder.
- Current-state/lean-doc/doctrine focused tests.
- Hostile audit for authority laundering, protected-body wording, exact hash/ID binding, stale/replay/expiry, and side-effect flags.
- Full Python unittest discovery before commit.

## Documentation Burden Rule

No new BLK-### document is created. Each sprint receives exactly one closeout outcome.
