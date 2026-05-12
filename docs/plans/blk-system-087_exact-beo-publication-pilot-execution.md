# BLK-SYSTEM-087 — Exact BEO Publication Pilot Execution Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, `test-driven-development`, and hostile review when executing. This plan is guided by historical BLK-024 first, then active BLK-077/BLK-079 post-078 current-state doctrine, and BLK-001 through BLK-006 as applicable.

**Goal:** Execute exactly one deterministic local BEO publication pilot bound to the BLK-SYSTEM-086 approval-decision package, producing a hash-bound local pilot publication artifact while preserving all external publication, signer, storage, ledger, rollback, RTM, protected-body, target-repo, BLK-test, Codex, BLK-pipe, tooling, and isolation boundaries.

**BLK-024 track:** Track G — BEO publication path / maturity L1 activation of one local exact pilot fixture under the BLK-077 activation rule. It is not L5 production publication.

**Architecture:** BLK-SYSTEM-087 consumes the exact BLK-086 approval-decision package for the canonical BLK-085 request and validates package identity, hash, approval ID, reserved run ID, BEO identity, target identity, signer/storage/ledger/rollback policy hashes, expiry, replay, and no-adjacent-authority flags. The sprint may consume the reserved run ID and emit one deterministic local pilot publication artifact for `BEO-054-001`; it must not access signer key material, cryptographically sign, write immutable storage, append or mutate a public ledger, execute rollback/revocation/supersession, generate RTM, read protected bodies, scan or mutate target repositories, run BLK-test/Codex/BLK-pipe, invoke package/network/model/browser/cyber tooling, or claim production isolation.

**Tech stack:** Python fixture module/tests, Markdown doctrine/outcome/review docs, active doctrine gates, roadmap/current-state index alignment.

**Authority boundary:** Exact local publication-pilot execution only for `BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-001`, `APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001`, and `RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001`. No authoritative external BEO publication, no live external approval-system capture, no signer key-material access, no cryptographic signing, no immutable storage write, no public ledger mutation, no rollback/revocation/supersession execution, no RTM generation or drift rejection, no protected BLK-req body reads, no target-repo scan or mutation, no source/Git mutation by the fixture, no BEB dispatch or BEO closeout execution, no BLK-test/Codex/BLK-pipe runtime, no package/network/model/browser/cyber tooling, and no production sandbox/host-isolation claim.

---

## 0. Preflight State

- Date: `2026-05-12T17:30:09+10:00`
- Branch: `main...origin/main`
- HEAD: `9de5fc9 docs: close blk-system 086 approval decision sprint`
- Working tree at plan start: clean
- Git identity: `camcamcami <cam.elvey@gmail.com>`
- ID search: no existing `BLK-SYSTEM-087`, `BLK-087`, or `beo_publication_pilot_execution` artifacts.

Canonical BLK-086 approval-decision binding for BLK-SYSTEM-087:

```text
approval_decision_package_id: BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-001
approval_decision_status: BEO_PUBLICATION_PILOT_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK085_REQUEST_NOT_EXECUTED
approval_decision_package_hash: hash recomputed from submitted BLK-086 package
request_package_id: BEO-PUBLICATION-PILOT-EXECUTION-REQUEST-085-001
request_package_hash: sha256:6dc1b6eac1d85b3a2d3b7c01eb8efa2f3f5ed0f91e04227a3a7b43554271db10
upstream_decision_package_id: BEO-PUBLICATION-DECISION-PACKAGE-083-001
upstream_decision_package_hash: sha256:2abdc185164bfef129f9011f53192e70c8f01af76d00ab0039c6072c4358ff5b
beo_id: BEO-054-001
beo_hash: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
target_id: BEO-PUBLICATION-TARGET-055-001
target_ref: fixture://beo-publication-targets/055/001
approved_pilot_request_id: BEO-PUBLICATION-PILOT-EXECUTION-REQUEST-085-PILOT-001
approval_id: APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001
run_id_to_consume: RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001
```

---

## 1. Governing Doctrine

- BLK-001: advance one bounded V-model closure rung while preserving separation between planning, execution, evidence, publication, and trace closure.
- BLK-002: preserve HITL approval, immutable artifact lifecycle language, staged promotion, and protected-vault isolation.
- BLK-003: preserve human dispatch gates, hostile audit, failure ceilings, and no implicit inheritance across execution, testing, publication, and RTM.
- BLK-004: BLK-pipe remains final source-mutation enforcement and is not invoked by this sprint.
- BLK-005: preserve immutable IDs, canonical hashes, trace binding, and drift separation.
- BLK-006: preserve protected-vault hard-deny and no protected body reads.
- BLK-022/057/060/083/085/086: publication-specific approval must be exact; BLK-087 may run only the one local pilot bound to BLK-086 and must not become signer/storage/ledger/rollback/RTM or production publication authority.
- BLK-077/079: current-state guidance allows an activation sprint only when it turns on exactly one bounded runtime capability under explicit approval and keeps adjacent authorities disabled.

---

## 2. Deliverables

1. `docs/plans/blk-system-087_exact-beo-publication-pilot-execution.md`
2. `python/test_beo_publication_pilot_execution.py`
3. `python/beo_publication_pilot_execution.py`
4. `docs/BLK-087_exact-beo-publication-pilot-execution.md`
5. `python/test_active_doctrine_review_gates.py` BLK-087 doctrine/current-state gates
6. `python/blk_current_state_authority_index.py` and `python/test_blk_current_state_authority_index.py` BLK-087 surface alignment
7. `docs/BLK-077_blk-system-post-078-roadmap.md` and `docs/BLK-079_post-078-current-state-authority-index.md` alignment
8. Per-task outcome docs, hostile-review doc, and sprint closeout doc under `docs/outcomes/` and `docs/reviews/`

---

## 3. Task Plan

### Task 000 — Plan and publish sprint scope

- Write this plan.
- Write `docs/outcomes/BLK-SYSTEM-087_task-000-outcome.md`.
- Verify `git diff --check` and balanced Markdown fences.
- Commit exact paths with `docs: plan blk-system 087 exact beo publication pilot execution`.

### Task 001 — Exact publication-pilot execution fixture RED/GREEN

- Add RED tests for `beo_publication_pilot_execution` proving the missing fixture must:
  - consume only the canonical BLK-086 approval-decision package;
  - recompute and bind the approval-decision package hash;
  - consume exactly `RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001` once for this local fixture package;
  - bind `APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001`, `BEO-054-001`, the BEO hash, target ID/ref, source evidence, trace artifacts, and policy hashes;
  - emit one deterministic local pilot publication artifact and artifact hash;
  - reject forged/self-consistent upstream approval packages;
  - reject stale/replayed/expired execution attempts;
  - reject signer/storage/ledger/rollback/RTM/protected-body/target-repo/tooling/source-Git laundering.
- Implement the smallest deterministic local fixture to pass.
- Write `docs/outcomes/BLK-SYSTEM-087_task-001-outcome.md`.
- Commit exact paths.

### Task 002 — Doctrine and persistent gates

- Publish `docs/BLK-087_exact-beo-publication-pilot-execution.md`.
- Add active doctrine gates proving BLK-087 executed only the exact local pilot and did not authorize adjacent authorities.
- Write `docs/outcomes/BLK-SYSTEM-087_task-002-outcome.md`.
- Commit exact paths.

### Task 003 — Roadmap/current-state alignment

- Update BLK-077 and BLK-079 with post-BLK-SYSTEM-087 current state.
- Add BLK-087 as a current-state surface in `blk_current_state_authority_index.py` and tests.
- State that RTM authority remains unavailable until separately requested after publication prerequisites are reviewed.
- Preserve all denied adjacent authorities.
- Write `docs/outcomes/BLK-SYSTEM-087_task-003-outcome.md`.
- Commit exact paths.

### Task 004 — Hostile review and remediation

- Run hostile review against fixture, doctrine, roadmap/current-state, and tests.
- Remediate any blocker with new regression tests and implementation/docs patches.
- Record `docs/reviews/BLK-SYSTEM-087_hostile-review.md`.
- Commit exact paths.

### Task 005 — Full verification and closeout

- Run focused BLK-087 tests.
- Run active doctrine/current-state focused tests.
- Run full Python unittest suite.
- Run `go test ./...`, `go vet ./...`, and `git diff --check`.
- Write `docs/outcomes/BLK-SYSTEM-087_sprint-closeout.md`.
- Commit closeout, push `origin main`, and verify remote head.

---

## 4. Stop Conditions

Stop and require a new explicit operator decision if any task attempts to:

1. execute more than the one exact local publication pilot bound to BLK-086;
2. retarget approval, BEO, target, run ID, approval ID, or policy hashes;
3. publish to external or authoritative storage;
4. access signer key material or generate cryptographic signatures;
5. write immutable storage or mutate a public ledger;
6. execute rollback, revocation, or supersession;
7. generate RTM or make drift-rejection decisions;
8. read, copy, parse, hash, summarize, scan, or mutate protected BLK-req bodies;
9. scan or mutate any target repository;
10. dispatch BEBs or execute BEO closeout;
11. start BLK-test, Codex, or BLK-pipe runtime;
12. use package-manager, network, model-service, browser, or cyber tooling;
13. claim production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret isolation.

---

## 5. Expected Final State

BLK-SYSTEM-087 should end with a deterministic local pilot status:

```text
BEO_PUBLICATION_PILOT_EXECUTED_FOR_EXACT_BLK086_APPROVAL_LOCAL_ONLY
```

The output should include:

```text
execution_package_id: BEO-PUBLICATION-PILOT-EXECUTION-087-001
approval_decision_package_id: BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-001
approval_id: APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001
run_id_consumed: RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001
beo_id: BEO-054-001
beo_publication: PILOT_LOCAL_PUBLISHED_BEO_OUTPUT_NOT_AUTHORITATIVE
rtm_status: NOT_GENERATED
next_required_authority: RTM_AUTHORITY_REQUEST_AFTER_PUBLISHED_BEO_PREREQUISITES_NOT_GRANTED
```

No external authoritative publication, signer/storage/ledger/rollback side effect, RTM generation, protected-body read, target-repo scan/mutation, BLK-test/Codex/BLK-pipe runtime, package/network/model/browser/cyber tooling, or production isolation claim is expected or allowed.
