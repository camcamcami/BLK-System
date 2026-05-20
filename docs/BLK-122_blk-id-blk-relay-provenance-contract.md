# BLK-122 — `blk-id` / `blk-relay` Provenance Contract

**Status:** Active component contract
**Purpose:** Define the durable local contract for deterministic identity records and typed relay envelopes used by BLK-System HITL and BLK-003 loop evidence.

---

## 1. Scope

This document covers the non-runtime provenance spine created by BLK-SYSTEM-283..285:

- `blk-id` identity records bind actors, artifacts, approvals, runs, and source systems to exact ASCII IDs, timestamps, source-system IDs, and canonical hashes.
- `blk-relay` envelopes bind typed signals to source identity records, payload hashes, target components, and trace identity hashes.
- BLK-003 loop evidence consumes both contracts so future HITL/request wiring can prove which identity and signal evidence caused each bounded action.

This contract is local deterministic evidence only. It is not a network relay, runtime dispatcher, approval source, BEO publisher, RTM generator, production `blk-link`, protected-body reader, source mutator, or production-isolation claim.

---

## 2. `blk-id` Identity Record Contract

An identity record is valid only when it contains the exact fields enforced by `python/blk_identity_relay_spine_283_285.py`:

- `record_kind`: one of `actor`, `artifact`, `approval`, `run`, `source_system`.
- `record_id`: an ASCII uppercase exact ID with the required kind prefix (`ACTOR-`, `ARTIFACT-`, `APPROVAL-`, `RUN-`, or `SOURCE-`).
- `source_system_id`: an ASCII `SOURCE-*` exact ID.
- `subject_hash`: canonical `sha256:<64 lowercase hex>` metadata hash.
- `created_at`: timezone-aware ISO-8601 timestamp.
- `metadata`: closed optional string map using only `display_name`, `external_ref`, `summary`, `version`, and `purpose`.
- `identity_hash`: canonical JSON SHA256 over the full record excluding the hash field.

Unsupported fields, Unicode digit IDs, forged hashes, and authority/protected-body wording fail closed.

---

## 3. `blk-relay` Envelope Contract

A relay envelope is valid only when it consumes a valid `blk-id` source record and contains:

- `envelope_id`: an ASCII `RELAY-*` exact ID.
- `message_type`: one of the repository-owned signal vocabularies (`HITL_APPROVAL_SIGNAL`, `BEB_PACKET_SIGNAL`, `BEO_DRAFT_SIGNAL`, `STATUS_SIGNAL`, `RTM_TRACE_SIGNAL`).
- `target_component`: one of the fixed component names (`hermes`, `operator`, `blk-id`, `blk-relay`, `blk-req`, `blk-pipe`, `blk-test`, `blk-link`, `codex`).
- `source_identity_hash`: the exact source identity record hash.
- `payload_hash`: canonical `sha256:<64 lowercase hex>` payload hash.
- `trace_identity_hashes`: non-empty identity-hash list that includes the source identity hash.
- `relay_hash`: canonical JSON SHA256 over the full envelope excluding the hash field.

The envelope proves typed signal provenance. It does not start transport, route a live message, approve execution, dispatch BLK-pipe, or mutate any target.

---

## 4. BLK-003 Loop Binding

BLK-SYSTEM-285 binds the BLK-SYSTEM-283 identity contract, BLK-SYSTEM-284 relay contract, and BLK-SYSTEM-241 reusable BLK-003 loop kernel into one evidence package:

- per-iteration identity evidence is required;
- a relay envelope is required for each future signal;
- an approval identity record is required before future dispatch;
- dispatch authority remains external to identity/relay evidence;
- BEO closeout execution remains external to identity/relay evidence.

This binding is the next dependency for HITL gateway and BLK-003 loop wiring. It does not grant reusable runtime, reusable Codex, production BLK-test MCP, BEO publication, RTM generation, production `blk-link`, protected-body access, or source/Git mutation.

---

## 5. Stable Evidence Hashes

```text
blk283_identity_contract_hash=sha256:b7bdbb14890a4ebadcf2e286ca7cf78a899b02cf55cf336bc0681d095662c251
blk284_relay_contract_hash=sha256:d209df42c15863a373c7338bd249d24d5f6ae1cba1f1ddd873d2ef8acfdf54ca
blk285_identity_relay_loop_evidence_hash=sha256:574b9bfcc919331a28b7919c5412362440f8447a3a0df4d2ad27dc751e16a373
```
