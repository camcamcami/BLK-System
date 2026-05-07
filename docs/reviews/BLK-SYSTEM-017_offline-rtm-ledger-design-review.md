# BLK-SYSTEM-017 — Offline RTM Ledger Design Review

**Status:** Boundary review artifact
**Sprint:** BLK-SYSTEM-017 — Offline RTM ledger design, not implementation
**Purpose:** Define the future offline `blk-link` RTM ledger and drift-rejection envelope while keeping Sprint 017 design only and non-authorizing.

---

## 1. Source documents reviewed

- `docs/BLK-001_blk-system-master-architecture.md`
- `docs/BLK-008_blk-test-mcp-execution-server.md`
- `docs/BLK-014_blk-execution-outcome-fixture-shape.md`
- `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`
- `docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md`
- `docs/BLK-021_beo-draft-publication-gate-review.md`
- `docs/BLK-022_authoritative-beo-publication-design-boundary.md`
- `docs/reviews/BLK-SYSTEM-010_fixture-to-live-gap-register.md`
- `docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md`
- `docs/reviews/BLK-SYSTEM-015_draft-beo-publication-gate-review.md`
- `docs/outcomes/BLK-SYSTEM-015_sprint-closeout.md`
- `docs/reviews/BLK-SYSTEM-016_authoritative-beo-publication-design-review.md`
- `docs/outcomes/BLK-SYSTEM-016_sprint-closeout.md`

---

## 2. Positive design scope

BLK-SYSTEM-017 may describe the future offline RTM ledger authority envelope for `blk-link`. This includes future RTM ledger identity, BEO/outcome identity binding, source BLK-pipe evidence identity, BLK-test evidence identity, hash-only active-vault comparison policy, coverage vocabulary, stale/missing/replayed hash rejection policy, future drift review, and rollback or supersession interaction policy.

This artifact is design only. It may define future gates but cannot execute them.

---

## 3. Non-authority markers

BLK-SYSTEM-017:

- does not authorize RTM generation;
- does not authorize RTM drift rejection authority;
- does not generate RTM;
- does not implement `generate_rtm.py`;
- does not emit rtm_id;
- does not create coverage matrices;
- does not claim coverage;
- does not compare active-vault hashes at runtime;
- does not make drift decisions;
- does not read protected BLK-req vault bodies;
- does not parse protected requirement or use-case bodies;
- does not authorize authoritative BEO publication;
- does not mutate public outcome ledgers;
- does not grant signer/storage/rollback authority;
- does not start live BLK-test MCP;
- does not rerun BLK-SYSTEM-014 first live smoke;
- does not use arbitrary shell;
- does not run against real target repositories;
- does not mutate primary repo as BLK-test or RTM behavior;
- does not claim production sandbox or host-secret isolation.

Current runtime interfaces remain constrained by `beo_publication: "DRAFT_ONLY"`, `rtm_status: "NOT_GENERATED"`, and `rtm_authority: "DISABLED_INTERFACE_ONLY"`.

beo_publication: "DRAFT_ONLY" remains mandatory.
rtm_status: "NOT_GENERATED" remains mandatory.
rtm_authority: "DISABLED_INTERFACE_ONLY" remains mandatory.

---

## 4. Approval separation

RTM generation approval must be a separate future human approval act. It cannot be inherited from tactical execution approval, BLK-test smoke approval, BEO publication approval, or any Codex/Hermes implementation-support event.

Required approval separation markers:

- RTM generation approval is separate from BEO publication approval;
- RTM generation approval is separate from BLK-test MCP approval;
- RTM generation approval is separate from codex-live approval;
- RTM generation approval is separate from BLK-pipe execution success;
- RTM generation approval is separate from draft BEO projection;
- RTM drift rejection authority requires separate future review and cannot be inferred from BLK-test PASS or FAIL.

Any future RTM implementation must bind approval to exact RTM identity, BEO identity, BEO content hash, source evidence hash, BLK-test evidence identity, active-vault hash policy, operator identity, ledger target, drift policy, rollback/supersession policy, and timestamp.

---

## 5. Hash-only active-vault policy

protected BLK-req vault bodies remain unread. Sprint 017 may describe future use of opaque `trace_artifacts[*].version_hash` values and active-vault hashes, but it does not parse, compare, quote, summarize, or expose bodies under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`.

hash-only active-vault comparison remains future authority. Any future implementation must prove it compares canonical hashes only, avoids requirement body text, excludes secrets and protected bodies from replay bundles, and rejects any attempt to use BLK-test MCP as a requirement interpreter.

---

## 6. Future RTM ledger checklist

A future offline RTM implementation sprint must define, review, and test all of the following before it can request authority:

1. RTM generation approval schema and human approval channel.
2. RTM ledger ID, source BEO ID, source BEO hash, and source outcome identity.
3. Source BLK-pipe evidence identity, BLK-test evidence identity, and BLK-021/BLK-022 lineage.
4. Hash-only active BLK-req vault comparison policy.
5. Coverage vocabulary for traced, missing, stale, unknown, superseded, and rejected evidence.
6. Drift rejection vocabulary and human review boundary.
7. Rollback, supersession, and BEO-publication interaction policy.
8. Rejection for stale, missing, malformed, replayed, or mismatched `version_hash` values.
9. Audit bundle shape that excludes secrets, active-vault body text, and unbounded logs.
10. Persistent proof that BLK-test MCP and BEO fixtures do not emit generated RTM fields.

RTM ledger mutation rules remain future authority. Sprint 017 records design constraints only.

---

## 7. Forbidden runtime field matrix

| Field/status | Sprint 017 boundary |
| --- | --- |
| `rtm_status: "NOT_GENERATED"` | Remains mandatory for current runtime outputs. |
| `rtm_authority: "DISABLED_INTERFACE_ONLY"` | Remains mandatory for current BEO/RTM interface fixtures. |
| `rtm_id` | Must not be emitted at runtime in Sprint 017. |
| `rtm` | Must not be emitted at runtime in Sprint 017. |
| `requirements` | Must not be emitted or resolved at runtime in Sprint 017. |
| `coverage_matrix` | Must not be emitted at runtime in Sprint 017. |
| `coverage_status` | Must not be emitted at runtime in Sprint 017. |
| `drift`, `drift_decision`, `drift_status` | Must not be emitted as runtime decisions in Sprint 017. |
| `active_vault_read: True` | Must remain rejected or absent. |

---

## 8. BEO publication and BLK-test exclusions

BEO publication remains separate from RTM design. Sprint 017 does not authorize authoritative BEO publication, public outcome ledger mutation, signer identity, storage writes, rollback executors, release authority, or publication approval handling.

BLK-test MCP remains separate from RTM design. Sprint 017 does not start live BLK-test MCP, does not broaden fixed tools, does not run real target repositories, does not read protected BLK-req vault bodies, and does not emit RTM coverage or drift decisions from BLK-test evidence.

---

## 9. Handoff

BLK-SYSTEM-017 may hand off to a later explicit offline RTM implementation sprint only after this design boundary is accepted. That later sprint must request separate human approval before implementing `generate_rtm.py`, active-vault hash scanning, coverage matrix output, RTM ledger writing, drift rejection, rollback/supersession behavior, or any public ledger mutation.

BLK-SYSTEM-017 may also hand off interaction constraints to a future explicit BEO publication implementation sprint, but BEO publication approval does not authorize RTM generation and RTM generation approval does not authorize BEO publication.
