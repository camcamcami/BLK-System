# BLK-125 — Exact Quarantine-Gated BLK-003 Loop Execution Contract

**Status:** Active component/authority contract
**Purpose:** Define the exact package that consumes BLK-SYSTEM-290..293 request-path evidence and records one quarantine-contained BLK-003 loop execution report.

---

## 1. Core invariant

An exact quarantine-gated BLK-003 loop package may proceed only after the BLK-SYSTEM-290..293 request path is revalidated as ready and fresh target/worktree/sandbox evidence still matches the route binding.

The package records bounded quarantine evidence only. It does not create reusable Codex dispatch, broad BLK-pipe dispatch, durable target/source/Git mutation, BEO closeout execution, BEO publication, RTM generation, production `blk-link`, production BLK-test MCP transport, package-manager use, network/model/browser/cyber tooling, or a production-isolation claim.

---

## 2. Sprint state model

```text
BLK_SYSTEM_294_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_PACKAGE_READY
BLK_SYSTEM_295_FRESH_TARGET_WORKTREE_SANDBOX_PREFLIGHT_READY
BLK_SYSTEM_296_QUARANTINE_BOUNDED_BLK003_LOOP_EXECUTION_RECORDED
BLK_SYSTEM_297_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_RECONCILED
NEXT_FRONTIER_EXACT_BLK_TEST_ORACLE_VERIFICATION_AFTER_LOOP_EXECUTION_REQUIRED_NOT_GRANTED
```

State meanings:

- `BLK_SYSTEM_294_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_PACKAGE_READY` — request-path reconciliation, BEB-L2 route fields, one exact run ID, failure ceiling, stop conditions, and BEO draft requirement are bound into a package record.
- `BLK_SYSTEM_295_FRESH_TARGET_WORKTREE_SANDBOX_PREFLIGHT_READY` — target hash, trusted root/workdir hashes, private-bwrap descriptor hash, validation-profile hash, sandbox state, and worktree state are rechecked before any runtime handoff.
- `BLK_SYSTEM_296_QUARANTINE_BOUNDED_BLK003_LOOP_EXECUTION_RECORDED` — one quarantine-contained loop report is recorded with at most three attempts, cleanup evidence, preserved durable target hash, and BEO draft hash.
- `BLK_SYSTEM_297_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_RECONCILED` — execution evidence is reconciled and the next exact BLK-test oracle verification frontier is named.

---

## 3. Exact package rules

The package requires:

- a ready BLK-SYSTEM-293 request-path reconciliation;
- a fresh exact target hash recheck;
- fresh trusted root and workdir hash rechecks;
- private-bwrap descriptor and validation-profile hash rechecks;
- sandbox state `PRIVATE_BWRAP_DESCRIPTOR_READY`;
- worktree state `CLEAN_EXACT_TARGET_WORKTREE`;
- failure ceiling `3` with `STOP_AFTER_THREE_FAILED_ATTEMPTS`;
- cleanup evidence hash;
- BEO draft hash before any future closeout path.

A blocked or stale preflight cannot be promoted into execution evidence by rehashing its fields. Reconciliation must re-run the full validator chain rather than trusting submitted hashes.

---

## 4. Authority boundary

This contract grants none of the following:

- no reusable Codex dispatch;
- no broad BLK-pipe dispatch;
- no approval reuse;
- no run ID reuse or replay;
- no global replay ledger claim;
- no durable target/source/Git mutation;
- no source Git commit creation;
- no BEO closeout execution;
- no BEO publication;
- no RTM generation;
- no production `blk-link`;
- no production BLK-test MCP transport;
- no package-manager use;
- no network/model/browser/cyber tooling;
- no production-isolation claim.

The next frontier is explicitly separate:

```text
NEXT_FRONTIER_EXACT_BLK_TEST_ORACLE_VERIFICATION_AFTER_LOOP_EXECUTION_REQUIRED_NOT_GRANTED
```

---

## 5. Stable evidence hashes

```text
blk294_execution_package_hash=sha256:1e2baea95f88e9a569661d36f688b2936092e47bff0b5bc784dec2314e2be95a
blk295_fresh_preflight_hash=sha256:f4dd57b92af66453f9f1cb58faa359df2ba4ef329e57b41fc8d7670a553c285a
blk296_execution_record_hash=sha256:cb9bb4d9c04af2b7e82054da872a47ff6df3077fb468ba8eef32810512a3c5ed
blk297_reconciliation_hash=sha256:acf58ee2ddff633848eefc393ee65ac7de08d967c0042e8ad62c7179324efbed
```
