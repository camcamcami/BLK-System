# BLK-SYSTEM-056 — Kuronode TypeScript Power-of-Ten Static Profile Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, by `docs/BLK-059_blk-system-post-058-roadmap.md` for current sequencing, and by BLK-001 through BLK-006 as applicable.

**Goal:** Convert BLK-058 from Kuronode TypeScript safety doctrine into a deterministic fixture-only static validation profile contract without executing against Kuronode or granting runtime authority.
**BLK-024 / BLK-059 track:** Track D/F and BLK-059 Workstream B — Kuronode tactical quality intent; maturity L1 fixture-only profile definition.
**Architecture:** BLK-058 defines a Kuronode TypeScript Power-of-Ten tactical standard, but it is doctrine only. BLK-SYSTEM-056 defines a repository-owned static profile fixture that can evaluate submitted TypeScript/TSX descriptors for high-risk rule violations and produce deterministic PASS/BLOCKED evidence. It does not run package managers, typecheck Kuronode, mutate source, start BLK-test MCP, or execute Codex.
**Tech Stack:** Python deterministic fixture module/tests; Markdown boundary, review, and outcome docs.
**Authority boundary:** Fixture-only static profile contract. No live Kuronode repo scan, no source mutation, no live Codex, no production/generic/reusable BLK-test MCP, no arbitrary shell, no package-manager/network/model/browser/cyber tooling, no BEO publication, no RTM, and no protected BLK-req body reads.

---

## 1. Current Known State

Preflight:

```text
date: 2026-05-10T16:02:44+10:00
git status --short --branch: ## main...origin/main
git log -1 --oneline: 8a5dd2f docs: add blk-system 055 beo publication approval envelope
git rev-parse HEAD: 8a5dd2f916829feb213aa5678952e44a9f4a2ea5
```

ID discovery:

```text
BLK-SYSTEM-056 plan: not present before this sprint
BLK-061 document: not present before this sprint
BLK-SYSTEM-056 outcomes: not present before this sprint
```

---

## 2. Next-Sprint Selection Rationale

BLK-059 lists four active frontier intents after BLK-SYSTEM-054 / BLK-058. BLK-SYSTEM-055 completed Workstream C: approval-envelope/preflight for BEO publication. Workstream D, an actual bounded publication pilot, explicitly requires separate human publication authority naming the exact envelope and target. This request asks for the next logical sprint but does not separately grant actual BEO publication authority. Therefore the next unblocked logical sprint is BLK-059 Workstream B: turn BLK-058 from doctrine into repository-owned static validation fixtures.

This selection preserves the authority boundary while still advancing Kuronode readiness before broader implementation sprints.

---

## 3. Governing Doctrine Alignment

- **BLK-059:** Workstream B asks for `kuronode-power-of-ten-static` and related deterministic validation contracts before broader Kuronode execution.
- **BLK-058:** Defines the Kuronode TypeScript Power-of-Ten tactical standard and explicitly says mechanical gates require a later sprint.
- **BLK-001:** Keeps Hermes as architect/auditor, `blk-pipe` as mutation blast shield, and BLK-test as evidence only.
- **BLK-004:** Validation profiles must be repository-owned deterministic command/profile contracts and must not authorize arbitrary shell, package-manager/network access, protected-body reads, BEO publication, or RTM.
- **BLK-006:** Protected BLK-req bodies remain unread; this sprint must not accept protected paths as validation targets.
- **BLK-060:** Publication pilot remains blocked pending separate explicit authority; this sprint deliberately avoids BEO publication and RTM frontiers.

---

## 4. Non-Authority Boundary

This plan does not authorize production BLK-test MCP, generic BLK-test MCP, reusable BLK-test service startup, live Codex execution, arbitrary shell, caller-supplied commands, TypeScript tooling/typechecker/linter/formatter execution by the static profile, package-manager/network/model/browser/cyber tooling, source/Git mutation by BLK-test or by the profile, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger append/mutation, rollback/revocation/supersession execution, runtime RTM generation, RTM drift rejection, active-vault hash comparison, coverage matrices, coverage claims, or production isolation claims.

BLK-System sprint-closeout verification and the final exact-path Git commit/push are normal repository maintenance performed by Hermes for this sprint. They are not capabilities of the Kuronode static profile and must not be reused as Kuronode source-mutation, BLK-test MCP, arbitrary-shell, package-manager, or live-tooling authority.

---

## 5. Implementation Intent

Create a deterministic local fixture module that evaluates submitted Kuronode TypeScript descriptors under profile:

```text
kuronode-power-of-ten-static
```

The profile must return one of:

```text
KURONODE_POWER_OF_TEN_STATIC_PROFILE_PASS_FIXTURE_ONLY
KURONODE_POWER_OF_TEN_STATIC_PROFILE_BLOCKED_FIXTURE_ONLY
```

It must check at least these BLK-058 static surfaces:

1. recursion by same-name function self-call;
2. unbounded `while (true)` loops;
3. `eval(...)` and `new Function(...)`;
4. `var` declarations;
5. explicit `any` annotations;
6. floating-promise markers such as `void saveModel(...)`;
7. non-null assertions at architecture boundaries;
8. function bodies over 60 physical lines excluding blank/comment-only lines;
9. lifecycle constructs for workers, intervals/timeouts, observers, parser trees, or JointJS paper/cell objects without nearby cleanup vocabulary;
10. protected-path and authority-laundering metadata.

The profile must be fixture-only: it evaluates caller-supplied descriptors and does not scan the live Kuronode filesystem.

---

## 6. Task Plan

### Task 000 — Plan and publish this sprint plan

Deliverables:

```text
docs/plans/blk-system-056_kuronode-typescript-power-of-ten-static-profile.md
docs/outcomes/BLK-SYSTEM-056_task-000-outcome.md
```

Actions:

1. Record preflight state and governing docs.
2. Publish the plan and Task 000 outcome.
3. Do not implement runtime validation in Task 000.

### Task 001 — Static profile fixture via TDD

Deliverables:

```text
python/kuronode_power_of_ten_static_profile.py
python/test_kuronode_power_of_ten_static_profile.py
docs/outcomes/BLK-SYSTEM-056_task-001-outcome.md
```

Actions:

1. Write RED tests for PASS fixture output and no-side-effect flags.
2. Write RED tests for recursion, `while (true)`, `eval`, `new Function`, `var`, `any`, floating promises, non-null assertions, long functions, lifecycle cleanup gaps, protected paths, authority-laundering metadata, non-TS paths, and exact excluded-authority mismatch.
3. Implement the smallest deterministic fixture/validator that passes.
4. Verify focused tests.

### Task 002 — BLK-061 boundary, active doctrine gate, and hostile review

Deliverables:

```text
docs/BLK-061_kuronode-typescript-power-of-ten-static-profile-boundary.md
python/test_active_doctrine_review_gates.py
docs/reviews/BLK-SYSTEM-056_kuronode-typescript-power-of-ten-static-profile-hostile-review.md
docs/outcomes/BLK-SYSTEM-056_task-002-outcome.md
```

Actions:

1. Add BLK-061 markers proving fixture-only static profile readiness.
2. Add persistent active doctrine gate coverage for BLK-061.
3. Hostile-review for source mutation laundering, live-Kuronode scan laundering, package-manager/typecheck laundering, BLK-test MCP escalation, Codex activation, protected-body/path laundering, BEO/RTM authority leakage, and weak static analysis claims.
4. Remediate blockers with tests and docs.

### Task 003 — Verification, closeout, commit, and push

Deliverables:

```text
docs/outcomes/BLK-SYSTEM-056_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-056_sprint-closeout.md
```

Actions:

1. Run focused static profile tests, active doctrine gate, full Python discovery, Go tests, Go vet, and `git diff --check`.
2. Record final verification output.
3. Stage exact paths only.
4. Commit and push to `origin/main`.
5. Report final commit hash.

---

## 7. Stop Conditions

Stop and report before closeout if any implementation:

1. scans live Kuronode files instead of fixture descriptors;
2. runs package-manager, typechecker, linter, formatter, shell, network, browser, model-service, or cyber tooling as part of the static profile;
3. starts BLK-test MCP or Codex;
4. mutates source or Git;
5. reads protected BLK-req bodies or accepts protected paths as validation targets;
6. claims production sandbox/host-secret isolation;
7. publishes BEOs, generates RTM, claims coverage, or performs drift rejection;
8. treats static profile PASS as publication, RTM, Codex, BLK-test MCP, or source-mutation authority;
9. fails hostile review or verification.
