# BLK-SYSTEM-087 Hostile Review — Exact BEO Publication Pilot Execution

**Status:** PASS after blocker remediation
**Date:** 2026-05-12T19:27:17+10:00
**Scope:** `python/beo_publication_pilot_execution.py`, focused tests, BLK-087 doctrine, BLK-077 roadmap alignment, BLK-079 current-state alignment, current-state authority index, active doctrine gates, and task outcome documents.

---

## 1. Review Target

BLK-SYSTEM-087 executes exactly one deterministic local BEO publication pilot bound to the canonical BLK-SYSTEM-086 approval-decision package:

```text
execution_package_id: BEO-PUBLICATION-PILOT-EXECUTION-087-001
approval_decision_package_id: BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-001
approval_decision_package_hash: sha256:2ade9eee61d5688c32f12cf9bec1a2668d03f091d1a14fb6eeef1c7f2f1a54b9
approval_id: APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001
run_id_consumed: RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001
beo_id: BEO-054-001
beo_publication: PILOT_LOCAL_PUBLISHED_BEO_OUTPUT_NOT_AUTHORITATIVE
rtm_status: NOT_GENERATED
```

The review treated all adjacent authority surfaces as denied unless explicitly and structurally bound to this local-only fixture.

---

## 2. Initial Hostile Findings

The first hostile review found two blockers.

### BLOCKER 1 — Approval interval was under-bound

The execution request originally checked only `requested_at > approval.expires_at`. That allowed:

- request `requested_at` before BLK-086 `decided_at`;
- request windows that started before approval expiry but extended after approval expiry;
- requests exactly at approval expiry.

### BLOCKER 2 — Hash-bound output aliased mutable nested input objects

The returned package reused caller-controlled nested objects from:

- `approval["trace_artifacts"]`;
- `request["operator_attestation"]`.

A caller could mutate the original input after hash computation and drift the returned package without recomputing the stored hashes.

---

## 3. Remediation Applied

Remediation added regression tests and implementation hardening:

- rejects execution requests that predate BLK-086 approval `decided_at`;
- rejects `requested_at >= approval.expires_at`;
- rejects request `expires_at` after BLK-086 approval expiry;
- defensively deep-copies `trace_artifacts` and `operator_attestation` before hashing/returning;
- pins canonical BLK-086 package hash in tests and BLK-087 doctrine;
- restores tooling and production-isolation denial language in current-state gates.

Focused RED/GREEN evidence was captured in `python/test_beo_publication_pilot_execution.py`.

---

## 4. Final Hostile Review Result

Final independent hostile review returned:

```text
PASS
Temporal approval interval: PASS
Mutable nested aliasing/hash drift: PASS
Canonical hash exactness: PASS
Self-consistent forged upstream package rejection: PASS
Denied authority laundering strings/keys: PASS
Roadmap/current-state stale authority wording: PASS
Blockers/issues: none
```

Final hostile probes covered:

- approval interval edge cases;
- defensive nested-copy and hash recomputation checks;
- canonical BLK-086 hash exactness;
- self-consistent forged upstream approval package rejection;
- encoded protected-body strings;
- production-isolation strings;
- model/browser/cyber tooling strings;
- `rtmGenerated` and generic `isAuthorized` authority-bearing keys;
- BLK-077/BLK-079/BLK-087 wording for stale RTM/external-publication/tooling/isolation claims.

---

## 5. Verification Evidence

Focused BLK-087/current-state/active-doctrine verification after remediation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_beo_publication_pilot_execution python.test_blk_current_state_authority_index python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint087_exact_beo_publication_pilot_execution_is_local_only python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint087_completion_updates_current_state_without_rtm_authority -v

Ran 22 tests in 1.921s

OK
```

Full verification before closeout:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'

Ran 872 tests in 13.464s

OK
```

Go verification:

```text
go test ./... && go vet ./...

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
```

`go vet ./...` exited 0 with no output.

---

## 6. Authority Boundary Preserved

BLK-SYSTEM-087 authorizes and records only one local deterministic pilot artifact. It does not authorize or perform:

- external authoritative BEO publication;
- live external approval capture;
- signer key-material access;
- cryptographic signing;
- immutable storage writes;
- public ledger append or mutation;
- rollback, revocation, or supersession execution;
- RTM generation or drift rejection;
- active-vault hash comparison or coverage claim authority;
- protected BLK-req body reads;
- target-repo scan or mutation;
- source or Git mutation by the fixture;
- BEB dispatch or BEO closeout execution;
- BLK-pipe, BLK-test, or Codex runtime;
- package/network/model/browser/cyber tooling;
- production sandbox or host-isolation claims.

---

## 7. Final Verdict

PASS. BLK-SYSTEM-087 is hostile-review clean after remediation and is ready for closeout commit/push.
