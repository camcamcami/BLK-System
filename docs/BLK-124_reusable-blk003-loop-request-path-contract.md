# BLK-124 — Reusable BLK-003 Loop Request Path Contract

**Status:** Active component/authority contract
**Purpose:** Define the hash-bound request path that connects the BLK-003 loop kernel to BLK-SYSTEM-286..289 speculative-quarantine HITL gate evidence without granting live runtime.

---

## 1. Core invariant

A reusable BLK-003 loop request path may be prepared only as local evidence until a separate exact execution package exists:

> BLK-003 loop requests must bind the loop kernel, exact BEB-L2 payload hashes, target hash, validation profile, trusted root/workdir hashes, and the BLK-SYSTEM-289 promotion/purge gate before any future runtime package can be considered.

The contract is a review surface. It does not start BLK-pipe, call Codex, dispatch relay messages, mutate source/Git state, perform BEO publication, generate RTM, touch production `blk-link`, read protected bodies, or claim production isolation.

---

## 2. Sprint state model

```text
BLK_SYSTEM_290_BLK003_LOOP_REQUEST_CONTRACT_READY
BLK_SYSTEM_291_BEB_L2_ROUTE_REQUEST_BINDING_READY
BLK_SYSTEM_292_QUARANTINE_GATED_REQUEST_PREFLIGHT_READY
BLK_SYSTEM_293_REUSABLE_BLK003_LOOP_REQUEST_PATH_RECONCILED
NEXT_FRONTIER_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_PACKAGE_REQUIRED_NOT_GRANTED
```

State meanings:

- `BLK_SYSTEM_290_BLK003_LOOP_REQUEST_CONTRACT_READY` — BLK-003 loop kernel and BLK-SYSTEM-286 approval timing contract are bound into a reusable request contract.
- `BLK_SYSTEM_291_BEB_L2_ROUTE_REQUEST_BINDING_READY` — exact BEB/L2/manifest/target/profile/trusted-root/trusted-workdir hashes are bound to the promotion/purge gate.
- `BLK_SYSTEM_292_QUARANTINE_GATED_REQUEST_PREFLIGHT_READY` — target hash, validation profile hash, and private-bwrap descriptor hash are checked as preflight evidence only.
- `BLK_SYSTEM_293_REUSABLE_BLK003_LOOP_REQUEST_PATH_RECONCILED` — the request path is reconciled and the next exact runtime package frontier is named, but runtime remains denied.

---

## 3. Required request fields

Every route-bound request must carry:

- `request_id`
- `beb_hash`
- `l2_packet_hash`
- `manifest_hash`
- `target_hash`
- `allowed_modified_files_hash`
- `validation_profile_id`
- `trusted_root_hash`
- `trusted_workdir_hash`
- `promotion_or_purge_gate_hash`
- `codex_model`

The request path requires the existing BLK-SYSTEM-289 gate stack to validate the original HITL interaction and quarantine evidence. A self-reported gate hash alone is not enough.

---

## 4. Quarantine gate preflight

The BLK-SYSTEM-292 preflight returns one of three outcomes:

- `REQUEST_PATH_READY_FOR_SEPARATE_EXACT_EXECUTION`
- `REQUEST_PATH_BLOCKED_BY_QUARANTINE_GATE`
- `REQUEST_PATH_BLOCKED_BY_TARGET_HASH_DRIFT`

Readiness means only that the exact request path has enough local evidence for a future exact package. It is not execution. The preflight preserves the BLK-SYSTEM-286..289 blockers:

- `QUARANTINE_RUNNING` cannot be promoted or rehashed into request readiness.
- Gate decision time must not precede the HITL decision or quarantine completion.
- Target hash drift blocks the path instead of retargeting the approved result.
- Rejection, expiry, dry-run-only, and stale-target outcomes remain purge/block evidence.

---

## 5. Authority boundary

This contract grants none of the following:

- no BLK-pipe runtime;
- no reusable Codex dispatch;
- no relay network runtime;
- no message dispatch;
- no approval reuse;
- no durable target/source/Git mutation;
- no protected-body access;
- no BEO closeout execution;
- no BEO publication;
- no RTM generation;
- no production `blk-link`;
- no production BLK-test MCP;
- no package/network/model/browser/cyber tooling;
- no production-isolation claim.

The next frontier is explicitly separate:

```text
NEXT_FRONTIER_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_PACKAGE_REQUIRED_NOT_GRANTED
```

---

## 6. Stable evidence hashes

```text
blk290_loop_request_contract_hash=sha256:c41030bda0df8850050dd7c816f73582b96e78632de262a50bee52cdeecf50e6
blk291_route_request_binding_hash=sha256:8e50dc3839097d8a16a4364895fe3d9a30703e315ee2e2395c57e153cad15b42
blk292_preflight_hash=sha256:11b31a7dd58d8da3aea064da6798c529d99a0c9a834b944cfcda57b23d4794be
blk293_reconciliation_hash=sha256:087d904b8f60d95529a73b71c4e36ee9dbbc0baeabc020510581b2624d4db0e7
```
