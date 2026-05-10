# BLK-SYSTEM-057 — Kuronode Power-of-Ten Validation Profile Registry Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, by `docs/BLK-059_blk-system-post-058-roadmap.md` for current sequencing, and by BLK-001 through BLK-006 as applicable.

**Goal:** Register a repository-owned Kuronode Power-of-Ten fixture self-test validation profile so BLK-System can verify the BLK-SYSTEM-056 static profile contract without scanning Kuronode or granting runtime authority.
**BLK-024 / BLK-059 track:** Track D/J and BLK-059 Workstream B — Kuronode tactical quality intent; maturity L1 fixture-only plus L2-style repository-owned profile resolution.
**Architecture:** BLK-SYSTEM-056 created a deterministic Python fixture evaluator for submitted TypeScript descriptors. BLK-SYSTEM-057 wires that fixture into the existing Go `internal/validationprofiles` registry as a repository-owned self-test profile, preserving BLK-pipe as final validation-profile resolution authority. The profile proves the fixture contract and doctrine gates are healthy; it does not run against a live Kuronode checkout or evaluate tactical source by itself.
**Tech Stack:** Go validation-profile registry/tests; Python active doctrine gate; Markdown boundary, review, and outcome docs.
**Authority boundary:** Fixture self-test profile only. No live Kuronode repository scan, no TypeScript tooling execution, no package-manager/network/model/browser/cyber tooling, no source/Git mutation by the profile, no live Codex, no production/generic/reusable BLK-test MCP, no protected BLK-req body reads, no BEO publication, no RTM generation, and no production isolation claim.

---

## 1. Current Known State

Preflight:

```text
date: 2026-05-10T19:01:01+10:00
git status --short --branch: ## main...origin/main
git log -1 --oneline: 6fbd40b feat: add kuronode power-of-ten static profile
git ls-remote origin refs/heads/main: 6fbd40b3214002f83843fd988edb17d3132be25a refs/heads/main
```

ID discovery:

```text
BLK-SYSTEM-057 plan: not present before this sprint
BLK-062 document: not present before this sprint
BLK-SYSTEM-057 outcomes: not present before this sprint
```

---

## 2. Next-Sprint Selection Rationale

BLK-059's post-058 sequence says the next unblocked frontiers after BLK-SYSTEM-055 and BLK-SYSTEM-056 are either an actual publication pilot, a Kuronode gate pilot, Codex L3 smoke, or later RTM authority. This operator request does not separately grant actual authoritative BEO publication, live Codex execution, runtime RTM generation, production BLK-test MCP, or a live Kuronode scan.

Therefore the next logical unblocked sprint remains within BLK-059 Workstream B: make the newly created Kuronode Power-of-Ten static profile mechanically reachable through repository-owned validation-profile resolution, but only as a fixture self-test. This advances Kuronode tactical quality readiness without crossing into live execution or publication.

---

## 3. Governing Doctrine Alignment

- **BLK-059:** Workstream B asks for repository-owned static validation profiles and checks before broader Kuronode execution.
- **BLK-058:** Defines the Kuronode TypeScript Power-of-Ten tactical standard that the fixture self-test protects.
- **BLK-061:** Establishes `KURONODE_POWER_OF_TEN_STATIC_PROFILE_PASS_FIXTURE_ONLY` and `KURONODE_POWER_OF_TEN_STATIC_PROFILE_BLOCKED_FIXTURE_ONLY` as fixture-only outcomes, not runtime authority.
- **BLK-001:** Preserves separation between Hermes planning/audit, BLK-pipe deterministic enforcement, BLK-test evidence, BEO publication, and future blk-link RTM.
- **BLK-003:** Preserves human dispatch gates and no implicit inheritance from validation/profile readiness into BLK-test, publication, or RTM.
- **BLK-004:** Keeps validation profiles repository-owned and deterministic, while denying arbitrary caller-supplied shell across less-trusted boundaries.
- **BLK-006:** Preserves protected-vault hard-deny semantics and no protected body reads by validation fixtures.
- **BLK-060:** Keeps actual authoritative BEO publication blocked pending separate explicit authority.

---

## 4. Non-Authority Boundary

This plan does not authorize production BLK-test MCP, generic BLK-test MCP, reusable BLK-test service startup, live Codex execution, arbitrary shell, caller-supplied commands, TypeScript tooling/typechecker/linter/formatter execution, package-manager/network/model/browser/cyber tooling, live Kuronode repository scans, source/Git mutation by BLK-test or by the Kuronode profile, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger append/mutation, rollback/revocation/supersession execution, runtime RTM generation, RTM drift rejection, active-vault hash comparison, coverage matrices, coverage claims, or production isolation claims.

Hermes sprint-closeout verification and exact-path Git commit/push are BLK-System repository maintenance. They are not capabilities granted to the Kuronode profile.

---

## 5. Implementation Intent

Register this repository-owned validation profile name:

```text
kuronode-power-of-ten-static-fixture
```

The profile must resolve to the existing deterministic Python fixture tests only:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_kuronode_power_of_ten_static_profile -q
```

It must not be named as if it scans live Kuronode source. It is a fixture self-test proving the static-profile validator and its hostile regressions remain healthy.

---

## 6. Task Plan

### Task 000 — Plan and publish this sprint plan

Deliverables:

```text
docs/plans/blk-system-057_kuronode-power-of-ten-validation-profile-registry.md
docs/outcomes/BLK-SYSTEM-057_task-000-outcome.md
```

Actions:

1. Record preflight state, ID discovery, and governing docs.
2. Publish the plan and Task 000 outcome.
3. Do not change validation-profile registry behavior in Task 000.

### Task 001 — Register fixture self-test validation profile via TDD

Deliverables:

```text
internal/validationprofiles/profiles.go
internal/validationprofiles/profiles_test.go
docs/outcomes/BLK-SYSTEM-057_task-001-outcome.md
```

Actions:

1. Write RED Go tests proving `kuronode-power-of-ten-static-fixture` resolves to the exact fixture unittest command.
2. Write RED Go tests proving the profile command contains no package-manager, network, TypeScript tooling, live scan, Codex, BLK-test MCP, BEO, RTM, or protected-vault authority wording.
3. Implement the smallest registry change to pass.
4. Run focused Go tests for GREEN.

### Task 002 — BLK-062 boundary, active doctrine gate, and hostile review

Deliverables:

```text
docs/BLK-062_kuronode-power-of-ten-validation-profile-registry-boundary.md
python/test_active_doctrine_review_gates.py
docs/reviews/BLK-SYSTEM-057_kuronode-power-of-ten-validation-profile-registry-hostile-review.md
docs/outcomes/BLK-SYSTEM-057_task-002-outcome.md
```

Actions:

1. Add BLK-062 boundary markers for fixture self-test profile readiness and exact non-authority.
2. Add a persistent active doctrine gate proving BLK-062 exists and denies runtime/live-scan/tooling/publication/RTM authority.
3. Hostile-review for profile-name laundering, self-test PASS as live Kuronode validation, package-manager/typecheck laundering, BLK-test/Codex escalation, protected-body/path leakage, BEO/RTM authority leakage, and under-scoped doctrine gates.
4. Remediate blockers with tests or docs before closeout.

### Task 003 — Verification, closeout, commit, and push

Deliverables:

```text
docs/outcomes/BLK-SYSTEM-057_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-057_sprint-closeout.md
```

Actions:

1. Run focused Go profile tests, focused active doctrine gate, focused Python static-profile tests, full Python discovery, Go tests, Go vet, and `git diff --check`.
2. Record final verification output.
3. Stage exact paths only.
4. Commit and push to `origin/main`.
5. Report final commit hash.

---

## 7. Stop Conditions

Stop and report before closeout if any implementation:

1. names the profile as live Kuronode validation instead of fixture self-test readiness;
2. scans live Kuronode files, reads protected BLK-req bodies, or accepts protected paths as runtime targets;
3. runs package-manager, TypeScript tooling, network, browser, model-service, cyber tooling, Codex, BLK-test MCP, or caller-supplied shell;
4. mutates source or Git as part of the profile;
5. claims production sandbox or host-secret isolation;
6. publishes BEOs, generates RTM, claims coverage, or performs drift rejection;
7. treats fixture self-test PASS as publication, RTM, Codex, BLK-test MCP, live Kuronode validation, or source-mutation authority;
8. fails hostile review or verification.
