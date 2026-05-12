# BLK-SYSTEM-086 — BEO Publication Pilot Approval Decision Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, `test-driven-development`, and hostile review when executing. This plan is guided by historical BLK-024 first, then active BLK-077/BLK-079 post-078 current-state doctrine, and BLK-001 through BLK-006 as applicable.

**Goal:** Capture an exact human approval decision for the canonical BLK-SYSTEM-085 BEO publication pilot execution request package without executing the publication pilot.

**BLK-024 track:** Track G — BEO publication path / maturity L1 approval-decision fixture with authority-bearing approval capture; no runtime publication.

**Architecture:** BLK-SYSTEM-086 consumes the BLK-085 request package as immutable upstream evidence, validates its canonical hash and exact identity, and emits a deterministic approval-decision package. The package may record that the exact BLK-085 request is approved for one future publication-pilot execution sprint, but it does not run that sprint and does not perform signer, storage, ledger, rollback, RTM, protected-body, target-repo, BLK-test, Codex, BLK-pipe, package, network, model, browser, cyber, or production-isolation side effects.

**Tech stack:** Python fixture module/tests, Markdown doctrine/outcome/review docs, active doctrine gates, roadmap/current-state index alignment.

**Authority boundary:** Exact approval-decision capture only. No publication pilot execution, no runtime `PUBLISHED` BEO output, no live external approval system, no signer key-material access, no cryptographic signing, no immutable storage write, no public ledger mutation, no rollback/revocation/supersession execution, no RTM generation or drift rejection, no protected BLK-req body reads, no target-repo scan or mutation, no BEB dispatch or BEO closeout execution, no BLK-test/Codex/BLK-pipe runtime, no package/network/model/browser/cyber tooling, and no production sandbox/host-isolation claim.

---

## 0. Preflight State

- Date: `2026-05-12T15:50:04+10:00`
- Branch: `main...origin/main`
- HEAD: `57e1586 docs: close blk-system 085 beo publication pilot request gate`
- Working tree at plan start: clean
- Git identity: `camcamcami <cam.elvey@gmail.com>`
- ID search: no existing `BLK-SYSTEM-086`, `BLK-086`, or `beo_publication_pilot_approval` artifacts.

Canonical BLK-085 request package binding for BLK-SYSTEM-086:

```text
request_package_id: BEO-PUBLICATION-PILOT-EXECUTION-REQUEST-085-001
request_package_hash: sha256:6dc1b6eac1d85b3a2d3b7c01eb8efa2f3f5ed0f91e04227a3a7b43554271db10
upstream_decision_package_id: BEO-PUBLICATION-DECISION-PACKAGE-083-001
upstream_decision_package_hash: sha256:2abdc185164bfef129f9011f53192e70c8f01af76d00ab0039c6072c4358ff5b
beo_id: BEO-054-001
beo_hash: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
target_id: BEO-PUBLICATION-TARGET-055-001
target_ref: fixture://beo-publication-targets/055/001
pilot_request_id: BEO-PUBLICATION-PILOT-EXECUTION-REQUEST-085-PILOT-001
approval_id_to_capture: APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001
future_run_id_to_reserve: RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001
```

---

## 1. Governing Doctrine

- BLK-001: preserve the V-model separation between requirements, execution, BLK-test evidence, BEO publication, and blk-link trace closure.
- BLK-002: preserve HITL approval and immutable artifact lifecycle boundaries; do not read protected BLK-req bodies.
- BLK-003: preserve human dispatch gates, bounded context, hostile audit, failure ceilings, and separation between execution/test/publication/RTM approval.
- BLK-004: BLK-pipe remains final source-mutation enforcement and is not invoked by this sprint.
- BLK-005: preserve immutable IDs, canonical hashes, trace binding, and drift separation.
- BLK-006: preserve protected-vault hard-deny and no protected body reads.
- BLK-022/057/060/083/085: publication-specific approval cannot be inherited from other gates; request packages are not publication; a later pilot must be exact, one-run, and separately controlled.
- BLK-077/079: post-085 current state says actual pilot movement requires a fresh explicit human decision bound to the exact BLK-085 request package.

---

## 2. Deliverables

1. `docs/plans/blk-system-086_beo-publication-pilot-approval-decision.md`
2. `python/test_beo_publication_pilot_approval_decision.py`
3. `python/beo_publication_pilot_approval_decision.py`
4. `docs/BLK-086_beo-publication-pilot-approval-decision.md`
5. `python/test_active_doctrine_review_gates.py` BLK-086 doctrine/current-state gates
6. `python/blk_current_state_authority_index.py` and `python/test_blk_current_state_authority_index.py` BLK-086 surface alignment
7. `docs/BLK-077_blk-system-post-078-roadmap.md` and `docs/BLK-079_post-078-current-state-authority-index.md` alignment
8. Per-task outcome docs, hostile-review doc, and sprint closeout doc under `docs/outcomes/` and `docs/reviews/`

---

## 3. Task Plan

### Task 000 — Plan and publish sprint scope

- Write this plan.
- Write `docs/outcomes/BLK-SYSTEM-086_task-000-outcome.md`.
- Verify `git diff --check` and balanced Markdown fences.
- Commit exact paths with `docs: plan blk-system 086 beo publication pilot approval decision`.

### Task 001 — Approval-decision fixture RED/GREEN

- Add RED tests for `beo_publication_pilot_approval_decision` proving the missing fixture must:
  - consume only the canonical BLK-085 request package;
  - recompute and bind the request package hash;
  - capture exactly `APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001` for the exact request;
  - reserve but not consume `RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001`;
  - reject forged/self-consistent upstream request packages;
  - reject stale/replayed/expired decisions;
  - reject approval/run/request ID reuse outside the canonical BLK-085 binding;
  - reject adjacent-frontier, signer/storage/ledger/rollback/RTM/protected-body/target-repo/tooling/source-Git laundering.
- Implement the smallest deterministic local fixture to pass.
- Write `docs/outcomes/BLK-SYSTEM-086_task-001-outcome.md`.
- Commit exact paths.

### Task 002 — Doctrine and persistent gates

- Publish `docs/BLK-086_beo-publication-pilot-approval-decision.md`.
- Add active doctrine gates proving BLK-086 captures an exact approval decision but does not execute publication or adjacent authorities.
- Write `docs/outcomes/BLK-SYSTEM-086_task-002-outcome.md`.
- Commit exact paths.

### Task 003 — Roadmap/current-state alignment

- Update BLK-077 and BLK-079 with post-BLK-SYSTEM-086 current state.
- Add BLK-086 as a current-state surface in `blk_current_state_authority_index.py` and tests.
- State that the next possible movement is an exact publication-pilot execution sprint, but this sprint did not execute it.
- Preserve all denied adjacent authorities.
- Write `docs/outcomes/BLK-SYSTEM-086_task-003-outcome.md`.
- Commit exact paths.

### Task 004 — Hostile review and remediation

- Run hostile review against fixture, doctrine, roadmap/current-state, and tests.
- Remediate any blocker with new regression tests and implementation/docs patches.
- Record `docs/reviews/BLK-SYSTEM-086_hostile-review.md`.
- Commit exact paths.

### Task 005 — Full verification and closeout

- Run focused BLK-086 tests.
- Run active doctrine/current-state focused tests.
- Run full Python unittest suite.
- Run `go test ./...`, `go vet ./...`, and `git diff --check`.
- Write `docs/outcomes/BLK-SYSTEM-086_sprint-closeout.md`.
- Commit closeout, push `origin main`, and verify remote head.

---

## 4. Stop Conditions

Stop and require a new explicit operator decision if any task attempts to:

1. execute a publication pilot;
2. emit runtime `PUBLISHED` BEO output;
3. access signer key material or generate cryptographic signatures;
4. write immutable storage or mutate a public ledger;
5. execute rollback, revocation, or supersession;
6. generate RTM or make drift-rejection decisions;
7. read, copy, parse, hash, summarize, scan, or mutate protected BLK-req bodies;
8. scan or mutate any target repository;
9. dispatch BEBs or execute BEO closeout;
10. start BLK-test, Codex, or BLK-pipe runtime;
11. use package-manager, network, model-service, browser, or cyber tooling;
12. claim production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret isolation.

---

## 5. Expected Final State

BLK-SYSTEM-086 should end with a deterministic approval-decision package status:

```text
BEO_PUBLICATION_PILOT_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK085_REQUEST_NOT_EXECUTED
```

The package should make the next step exact and reviewable:

```text
NEXT_REQUIRED_AUTHORITY: EXACT_BEO_PUBLICATION_PILOT_EXECUTION_SPRINT_REQUIRED_NOT_RUN
```

This next step remains outside BLK-SYSTEM-086 unless separately selected and executed as its own sprint.
