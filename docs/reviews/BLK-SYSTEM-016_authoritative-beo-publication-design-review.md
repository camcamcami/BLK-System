# BLK-SYSTEM-016 — Authoritative BEO Publication Design Review

**Status:** Boundary review artifact
**Sprint:** BLK-SYSTEM-016 — BEO publication design, not implementation
**Purpose:** Define the future authoritative BEO publication envelope while keeping Sprint 016 design only and non-authorizing.

---

## 1. Source documents reviewed

- `docs/BLK-001_blk-system-master-architecture.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
- `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`
- `docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md`
- `docs/BLK-021_beo-draft-publication-gate-review.md`
- `docs/reviews/BLK-SYSTEM-010_fixture-to-live-gap-register.md`
- `docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md`
- `docs/reviews/BLK-SYSTEM-015_draft-beo-publication-gate-review.md`
- `docs/outcomes/BLK-SYSTEM-015_sprint-closeout.md`

---

## 2. Positive design scope

BLK-SYSTEM-016 may describe the future publication-authority envelope for authoritative BEOs. This includes human approval prerequisites, source-bound draft BEO identity, future signer identity policy, future storage target policy, future public ledger mutation rules, and future rollback or revocation policy.

This artifact is design only. It may define future gates but cannot execute them.

---

## 3. Non-authority markers

BLK-SYSTEM-016:

- does not authorize authoritative BEO publication;
- does not implement BEO publication;
- does not mutate public outcome ledgers;
- does not grant signer/storage/rollback authority;
- does not write storage records;
- does not create signer keys or signer identities;
- does not create rollback executors;
- does not emit runtime `beo_publication: "PUBLISHED"`;
- does not start live BLK-test MCP;
- does not rerun BLK-SYSTEM-014 first live smoke;
- does not use arbitrary shell;
- does not run against real target repositories;
- does not mutate primary repo as BLK-test behavior;
- does not authorize RTM generation;
- RTM generation remains disabled;
- does not claim RTM coverage;
- does not read protected BLK-req vault bodies;
- does not claim production sandbox or host-secret isolation.

Current runtime BEO projection remains `beo_publication: "DRAFT_ONLY"` and `rtm_status: "NOT_GENERATED"`.

---

## 4. Approval separation

Publication approval must be a separate future human approval act. It cannot be inherited from tactical execution approval, BLK-test smoke approval, or any Codex/Hermes implementation-support event.

Required approval separation markers:

- codex-live approval is not BEO publication approval;
- BLK-test MCP approval is not BEO publication approval;
- BLK-pipe execution success is not BEO publication approval;
- draft BEO projection is not BEO publication approval.

Any future BEO publication implementation must bind a publication approval to exact BEO identity, BEO content hash, source evidence hash, operator identity, signer identity, storage target identity, public ledger target, rollback policy, and timestamp.

---

## 5. Status matrix

| Candidate evidence status | Future publication interpretation |
| --- | --- |
| `PASS` | PASS stays PASS; it may be a future publication candidate only after explicit publication approval. |
| `FAIL` | FAIL stays FAIL; it may be a future publication candidate as failed evidence only and must not become success. |
| `BLOCKED` | BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success. |
| `FATAL_TIMEOUT` | BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success. |
| `FATAL_OUTPUT_FLOOD` | BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success. |
| `TRANSPORT_ERROR` | BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success. |
| `OPERATOR_INTERRUPTED` | BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success. |
| unknown/missing | BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success. |

---

## 6. Future signer/storage/rollback/public-ledger checklist

A future publication implementation sprint must define, review, and test all of the following before it can request authority:

1. Publication approval schema and human approval channel.
2. Source-bound draft BEO identity and canonical BEO content hash.
3. Source BLK-pipe evidence identity, BLK-test evidence identity, and BLK-021 draft projection lineage.
4. Signer identity policy and key/secret handling policy.
5. Storage target policy and immutable write semantics.
6. Public ledger mutation schema.
7. Rollback, revocation, supersession, and recovery policy.
8. Failure handling for rejected, expired, mismatched, or replayed approval.
9. Audit bundle shape that excludes secrets, active-vault body text, and unbounded logs.
10. Explicit rollback evidence before any public mutation is accepted.

public ledger mutation rules remain future authority. Sprint 016 records design constraints only.

---

## 7. RTM and active-vault exclusion

RTM generation remains disabled in Sprint 016. Publication design does not generate RTM, does not create `rtm_id`, does not create coverage matrices, does not claim coverage, and does not make drift decisions.

Protected BLK-req vault bodies remain unread. Sprint 016 may preserve opaque `trace_artifacts[*].version_hash` values but does not parse, compare, or expose bodies under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`.

A Later RTM sprint remains separate and must define any offline hash comparison, coverage, drift, and active-vault access policy independently.

---

## 8. Handoff

BLK-SYSTEM-016 may hand off to a later explicit BEO publication implementation sprint only after this design boundary is accepted. That later sprint must request separate human approval before implementing any publisher, signer, storage writer, public ledger writer, or rollback executor.

BLK-SYSTEM-016 may also hand off constraints to a Later RTM sprint, but it does not authorize RTM generation or RTM drift rejection authority.
