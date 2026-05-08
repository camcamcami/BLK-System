# BLK-SYSTEM-027 — RTM Generation Readiness Proposal Hostile Review

**Status:** PASS after remediation
**Date:** 2026-05-08T10:09:30+10:00
**Scope:** `docs/BLK-030_rtm-generation-readiness-proposal-boundary.md`, `python/rtm_generation_readiness_proposal_fixtures.py`, `python/test_rtm_generation_readiness_proposal_fixtures.py`, and `python/test_active_doctrine_review_gates.py`

---

## Verdict

PASS after remediation.

The initial hostile review returned BLOCKED with three findings. All findings were remediated before closeout, and focused/full verification now passes.

---

## Findings and Remediation

### BLK-SYSTEM-027-HR-001 — BLOCKER — Authority laundering fields accepted instead of fail-closed

Initial finding: exact-key forbidden checks allowed authority-shaped fields such as `rtm`, `rtm_authority`, and unsupported runtime-authority containers to be supplied and ignored.

Remediation:

- Added `rtm` and `rtm_authority` to recursive forbidden-key rejection.
- Added context-specific top-level allowlists for published-BEO input fixtures, backend fixtures, metadata records, and proposal requests.
- Added regression tests for top-level and nested `rtm`, `rtm_authority`, coverage, drift, publication, body, path, secret, and unsupported `runtime_authority` fields.

Status: PASS.

### BLK-SYSTEM-027-HR-002 — BLOCKER — Trace/hash metadata matching not bijective

Initial finding: every trace artifact required matching metadata, but extra backend metadata and duplicate identities could still be accepted and emitted.

Remediation:

- Enforced bijection between trace artifact identities and metadata record identities by `(kind, id)`.
- Rejected extra backend metadata records not represented in trace artifacts.
- Rejected duplicate trace identities and duplicate metadata identities.
- Added regression tests for extra metadata, duplicate metadata, duplicate trace identities, and hash mismatch.

Status: PASS.

### BLK-SYSTEM-027-HR-003 — BLOCKER — Required fail-closed RED matrix incomplete

Initial finding: the negative test matrix under-covered malformed hashes, missing IDs, non-string identities, request identity mismatches, broader authority laundering, and side-effect classes.

Remediation:

- Added table-driven regression tests for malformed hashes, missing IDs, non-string identities, request input/BEO/backend mismatch, stale/replayed/expired/generated request flags, side-effect flags, unsupported fields, and nested authority laundering.
- Expanded BLK-030 doctrine and active doctrine gate markers to pin the stricter allowlist and bijection invariants.

Status: PASS.

---

## Hostile Probe Evidence

Manual hostile probes after remediation rejected the exact initial gaps:

```text
published rtm_authority REJECTED published_beo_input rejects forbidden field: rtm_authority
request rtm_authority REJECTED proposal_request rejects forbidden field: rtm_authority
backend rtm REJECTED active_vault_backend_fixture rejects forbidden field: rtm
extra metadata REJECTED extra hash metadata identity not present in trace artifacts
hostile probes rejected
```

---

## Verification

Focused and full verification after remediation:

```text
Ran 12 tests in 0.002s
OK
Ran 47 tests in 0.005s
OK
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validationprofiles	(cached)
Ran 383 tests in 6.428s
OK
git diff --check completed with no output
```

---

## Residual Risk

No blocking residual risk remains inside BLK-SYSTEM-027 scope. The sprint remains proposal-only; runtime RTM generation, RTM IDs/ledgers, coverage matrices, drift rejection, active-vault scanning/reads, protected-body access, BEO publication, signer/storage/ledger/rollback, production BLK-test MCP, and live smoke remain unauthorized.
