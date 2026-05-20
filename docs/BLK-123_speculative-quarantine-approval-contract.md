# BLK-123 — Speculative Quarantine Approval Contract

**Status:** Active component/authority contract
**Purpose:** Define the review-obvious HITL approval timing model that separates pre-approval computation from approved durable promotion.

---

## 1. Core invariant

BLK-System may use acceleration only under this invariant:

> pre-approval execution may compute only in a disposable quarantine; durable promotion to target/source/Git/production state requires an exact HITL decision or an explicit policy-bypass evidence record.

This contract exists so reviewers can immediately understand why BLK-pipe/Codex-shaped work may appear before the operator notices an approval prompt, while still proving that durable target state cannot be changed by unnoticed work.

---

## 2. Approval UX

The primary HITL UX is Discord button/selector interaction, not long exact-text copy-paste.

Required decision shape:

- `APPROVE`
- `DENY`
- `APPROVE_DRY_RUN_ONLY`
- `NEEDS_CHANGES`

Fallback short challenge:

- short reply: `Approve`
- bound to an approval request hash;
- bound to a time window;
- single-use;
- `long_copy_paste_required=false`.

Long exact-text copy-paste remains a historical/fallback pattern only, not the production UX target.

---

## 3. Execution timing modes

The executable contract recognizes exactly these modes:

- `pre_approval_blocked` — no pre-approval compute; quarantine/run start timestamps must not precede the operator decision.
- `speculative_quarantine` — compute may start before the operator clicks, but only in disposable quarantine and with durable target mutation false.
- `config_policy_bypass` — HITL may be bypassed only by explicit policy hash, policy source ID, eligible operation class, policy scope hash, and resulting evidence that records the bypass source.

`config_policy_bypass` is not a silent skip. It must produce a policy-bound decision record that downstream code can audit like any other approval source, and it cannot override a recorded `DENY`, `NEEDS_CHANGES`, or `APPROVE_DRY_RUN_ONLY` HITL decision.

---

## 4. State model

```text
REQUESTED
QUARANTINE_RUNNING
QUARANTINE_COMPLETE_AWAITING_DECISION
APPROVED_PROMOTED
DRY_RUN_ONLY_PURGED
REJECTED_PURGED
EXPIRED_PURGED
STALE_TARGET_HASH_BLOCKED
```

State meanings:

- `REQUESTED` — approval card/request exists; no durable promotion has occurred.
- `QUARANTINE_RUNNING` — state-model concept for in-flight disposable compute; it is not promotable completion evidence.
- `QUARANTINE_COMPLETE_AWAITING_DECISION` — result/report hashes exist, still not promoted, and this is the only state accepted by the BLK-SYSTEM-288 completion evidence builder.
- `APPROVED_PROMOTED` — the gate opened only for the exact quarantined result hash after target-hash recheck. In BLK-SYSTEM-289 this is local gate evidence, not live source mutation.
- `DRY_RUN_ONLY_PURGED` — a dry-run-only approval preserves review evidence but still refuses durable promotion and purges quarantine output.
- `REJECTED_PURGED` — rejection requires purge receipt evidence.
- `EXPIRED_PURGED` — expired approval windows fail closed and purge.
- `STALE_TARGET_HASH_BLOCKED` — approval cannot retarget changed source; refresh is required.

---

## 5. Evidence requirements

A quarantine approval package must bind:

- canonical BLK-SYSTEM-283 identity contract hash;
- canonical BLK-SYSTEM-284 relay contract hash;
- canonical BLK-SYSTEM-285 loop evidence hash;
- approval request hash and time window;
- Discord user/message/interaction IDs for button/selector decisions;
- HITL decision and decision timestamp carried through quarantine evidence;
- original HITL interaction package supplied again at promotion/purge validation, not only a self-reported interaction hash;
- `blk-id` actor and approval identity hashes;
- `blk-relay` HITL signal hash;
- target hash before quarantine;
- manifest/result/report hashes;
- quarantine workspace identity;
- external side-effect flags (`codex_model_api_called`, `network_called`, `package_manager_called`);
- `target_repo_mutated=false` and `promotion_performed=false` before decision;
- speculative pre-approval compute start time before the HITL decision timestamp when that claim is made;
- promotion/purge gate decision matching the bound HITL interaction decision, except explicit expiry or typed policy-bypass evidence;
- promotion/purge gate decision timestamp not preceding either the HITL decision timestamp or quarantine completion timestamp;
- purge receipt hash for rejection/expiry/stale target;
- exact result hash and target-hash recheck before promotion gate opens.

---

## 6. Review-obvious code shape

Implementation names should make the boundary obvious:

- `start_speculative_quarantine_run`
- `record_quarantine_result`
- `approve_and_promote_quarantined_result`
- `reject_and_purge_quarantined_result`
- `expire_and_purge_quarantined_result`

Avoid vague names such as `fast_mode`, `async_approval`, or `background_execute` because they hide the authority boundary.

---

## 7. Authority boundary

This contract does not grant:

- relay network runtime;
- message dispatch authority;
- approval reuse;
- BLK-pipe runtime outside a separately approved exact payload;
- reusable Codex dispatch;
- durable target/source/Git mutation from pre-approval compute;
- protected-body access;
- BEO closeout/publication;
- RTM generation;
- production `blk-link`;
- production BLK-test MCP;
- package/network/model/browser/cyber tooling by default;
- production-isolation claims.

Speculative compute may still create external side effects if explicitly configured to use Codex/API/model/network services. Those effects cannot be deleted after rejection, so they must be denied by default or explicitly recorded by policy.

---

## 8. Stable evidence hashes

```text
blk286_approval_timing_contract_hash=sha256:24f0cf02e473374a6af4360189bd8271acebf906a263baea541cd6db2d004d0c
blk287_hitl_interaction_hash=sha256:11e5aa001ccf6c2a49b78bc84c07563c8230582a7cc2c4ec8e3d69c1999ee166
blk288_quarantine_evidence_hash=sha256:ac23809cfedc346d465810d399cc8d89fb5403c2d7c328c04ac35836e8c8df34
blk289_promotion_purge_gate_hash=sha256:eb8001a1fd0de19f96dc1dec8cba33586f7404397396db0bb8ff026b7892abef
```
