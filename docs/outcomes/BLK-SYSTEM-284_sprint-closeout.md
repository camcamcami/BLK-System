# BLK-SYSTEM-284 — `blk-relay` Envelope Contract Sprint Closeout

**Status:** Complete
**Date:** 2026-05-20T20:29:19+10:00
**Commit:** this commit (`feat: add identity relay spine sprint package`)

## 1. Objective

Create the typed local `blk-relay` envelope contract that consumes valid `blk-id` records and binds future HITL/BLK-003 signals to payload hashes without granting transport or dispatch authority.

## 2. Files Changed

- `python/blk_identity_relay_spine_283_285.py`
- `python/test_blk_identity_relay_spine_283_285.py`
- `docs/BLK-122_blk-id-blk-relay-provenance-contract.md`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_lean_documentation_policy.py`

## 3. Implementation Summary

BLK-SYSTEM-284 adds `BLK_SYSTEM_284_BLK_RELAY_ENVELOPE_CONTRACT_READY` and a typed envelope API over the BLK-SYSTEM-283 identity contract:

- closed message types: HITL approval signal, BEB packet signal, BEO draft signal, status signal, RTM trace signal;
- fixed target components: Hermes, operator, `blk-id`, `blk-relay`, `blk-req`, `blk-pipe`, `blk-test`, `blk-link`, Codex;
- exact `RELAY-*` envelope IDs;
- source identity hash validation against a valid identity record;
- payload-hash and trace-identity hash binding;
- exact false side-effect flags for network runtime, dispatch, approval, runtime tooling, mutation, protected-body, BEO, and RTM surfaces.

Stable package hash:

```text
blk284_relay_contract_hash=sha256:d209df42c15863a373c7338bd249d24d5f6ae1cba1f1ddd873d2ef8acfdf54ca
```

## 4. Verification

- RED: forged source identity hashes, authority wording in metadata, and rehashed extra fields were represented in tests before GREEN implementation.
- GREEN: `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache-green python -m unittest python.test_blk_identity_relay_spine_283_285 -v` → 6 tests OK.
- Documentation gate RED after expansion: missing current-state identity surface and missing 284 closeout were observed before remediation.
- Package verification: `TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache-full-final python -m unittest discover -s python -p 'test_*.py'` → Ran 1472 tests; OK (skipped=35).
- Hostile review: PASS after replacing the initial `__import__("hashlib")` helper with a normal `hashlib` import so the new module has no live-call scanner finding.

## 5. Hostile Review / Risk Check

The hostile review focused on signal-provenance laundering:

- Forged identity hashes are rejected by recomputing the source identity record hash.
- Envelopes must include the source identity hash in trace identity hashes.
- Caller metadata cannot smuggle MCP transport/runtime authority wording.
- Rehashed extra top-level authority fields fail closed.
- The relay contract is evidence-only and does not start transport, invoke a process, or send a message.

## 6. Authority Boundary

BLK-SYSTEM-284 grants no relay network runtime, no message dispatch, no approval reuse, no approval authority, no BLK-pipe runtime, no live Codex, no production BLK-test MCP, no BEO closeout/publication, no RTM generation, no production `blk-link`, no protected-body access, no target/source/Git mutation, no package/network/model/browser/cyber tooling, and no production-isolation claim.

## 7. Documentation Burden Check

Exactly one sprint closeout exists for BLK-SYSTEM-284. No per-task outcome docs were created. The durable BLK-122 contract is shared by the identity/relay package because it defines a reusable component boundary, and BLK-001 through BLK-006 were not modified.
