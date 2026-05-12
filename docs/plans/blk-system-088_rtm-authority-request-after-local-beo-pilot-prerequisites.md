# BLK-SYSTEM-088 — RTM Authority Request After Local BEO Pilot Prerequisites

**Status:** Planned for execution
**Date:** 2026-05-12T20:08:17+10:00
**Sprint ID:** `BLK-SYSTEM-088`
**Model header:** Hermes Agent `gpt-5.5`; Codex preference if delegated: `gpt-5.4-codex`, fallback `gpt-5.4`

---

## 1. Objective

Package the completed BLK-SYSTEM-087 local BEO publication-pilot evidence into an exact RTM authority request for human review.

The sprint must produce deterministic local request evidence only. It must not generate RTM, reject drift, read protected BLK-req bodies, compare active-vault hashes, create coverage matrices, perform external authoritative BEO publication, access signer key material, write storage, append ledgers, mutate source/Git, run BLK-test/Codex/BLK-pipe, use package/network/model/browser/cyber tooling, or claim production isolation.

Canonical intended status marker:

```text
RTM_AUTHORITY_REQUEST_READY_AFTER_LOCAL_BEO_PILOT_PREREQUISITES_NOT_GRANTED
```

Canonical intended next-authority marker:

```text
EXPLICIT_HUMAN_RTM_GENERATION_APPROVAL_REQUIRED_NOT_GRANTED
```

---

## 2. Authority Surface

BLK-SYSTEM-088 touches the BEO/RTM boundary only as a request-readiness fixture. It asks for a future explicit human RTM generation decision, but does not capture approval and does not execute generation.

What remains unauthorized:

- runtime RTM generation;
- RTM drift rejection or drift decision;
- active-vault hash comparison;
- coverage matrix creation or coverage-claim promotion;
- protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning;
- external authoritative BEO publication;
- live external approval capture;
- signer key-material access or cryptographic signing;
- immutable storage writes;
- public ledger append/mutation;
- rollback, revocation, or supersession execution;
- target-repo scan or mutation;
- source/Git mutation by the fixture;
- BEB dispatch or BEO closeout execution;
- BLK-pipe, BLK-test, or Codex runtime;
- package/network/model/browser/cyber tooling;
- production sandbox or host-isolation claims.

---

## 3. Tasks

### Task 000 — Plan and publish sprint scope

Create this plan with explicit authority boundaries and sprint tasks.

### Task 001 — RTM authority-request fixture RED/GREEN

Files:

- `python/test_rtm_authority_request_after_beo_pilot.py`
- `python/rtm_authority_request_after_beo_pilot.py`

Required behavior:

1. Build a deterministic request package bound to the canonical BLK-087 execution package and local pilot artifact hash.
2. Recompute and validate the submitted BLK-087 execution package hash.
3. Reject self-consistent forged BLK-087 packages even if their hashes recompute.
4. Require exact proof-obligation and denied-authority sets with duplicate rejection.
5. Reject RTM-generation/drift/protected-body/publication/signer/storage/ledger/source/Git/runtime/tooling/isolation side-effect flags.
6. Reject forbidden authority-laundering keys/strings including compact/camel/percent-encoded forms.
7. Deep-copy nested hash-bound evidence before returning output.

### Task 002 — Doctrine and persistent gates

Files:

- `docs/BLK-088_rtm-authority-request-after-local-beo-pilot-prerequisites.md`
- `python/test_active_doctrine_review_gates.py`

Required behavior:

1. Publish BLK-088 doctrine/boundary markers.
2. Add persistent active-doctrine gates proving BLK-088 is request-only and not RTM generation authority.
3. Pin exact denied-authority markers.

### Task 003 — Roadmap/current-state alignment

Files:

- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_active_doctrine_review_gates.py`

Required behavior:

1. Mark BLK-SYSTEM-088 as the completed request-readiness step after BLK-SYSTEM-087.
2. Keep the current state explicit that RTM generation and drift rejection remain unauthorized.
3. Add a BLK-088 current-state surface with exact authority cutline.

### Task 004 — Hostile review and remediation

Files:

- `docs/reviews/BLK-SYSTEM-088_hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-088_task-004-outcome.md`

Review for authority laundering, forged upstream evidence, missing denied-authority coverage, stale roadmap/index wording, mutable nested aliasing, timestamp/replay gaps, and protected-body/active-vault/coverage/drift loopholes. Remediate with tests where needed.

### Task 005 — Full verification and closeout

Files:

- `docs/outcomes/BLK-SYSTEM-088_task-005-outcome.md`
- `docs/outcomes/BLK-SYSTEM-088_sprint-closeout.md`

Run focused verification, full Python suite, Go tests/vet, and `git diff --check`. Commit and push only after the outcome and closeout docs exist.

---

## 4. Verification Commands

Focused RED/GREEN:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_rtm_authority_request_after_beo_pilot -v
```

Focused doctrine/current-state:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_active_doctrine_review_gates python.test_blk_current_state_authority_index -v
```

Full verification:

```bash
rm -rf /tmp/blk-system-pycache
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
go test ./... && go vet ./...
git diff --check
```

---

## 5. Non-Goals

This sprint does not approve or perform RTM generation. It does not decide drift, read protected bodies, compare active-vault hashes, create coverage matrices, mutate target/source/Git state, publish externally, sign, write storage, append ledger records, execute BLK-pipe/BLK-test/Codex, or claim production isolation.
