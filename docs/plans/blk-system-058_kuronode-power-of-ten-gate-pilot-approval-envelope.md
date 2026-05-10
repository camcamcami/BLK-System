# BLK-SYSTEM-058 — Kuronode Power-of-Ten Gate Pilot Approval Envelope Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, by `docs/BLK-059_blk-system-post-058-roadmap.md` for current sequencing, and by BLK-001 through BLK-006 as applicable.

**Goal:** Create a deterministic non-runtime approval-envelope fixture for a future bounded Kuronode Power-of-Ten gate pilot, without scanning Kuronode or executing the pilot.
**BLK-024 / BLK-059 track:** Track D/J and BLK-059 Workstream B — Kuronode tactical quality intent; maturity L0/L1 approval-envelope readiness only.
**Architecture:** BLK-SYSTEM-056 created a fixture-only static profile and BLK-SYSTEM-057 registered a repository-owned fixture self-test validation profile. BLK-SYSTEM-058 defines the exact approval envelope that a later human could review before any future live Kuronode gate pilot. The envelope binds target identity, expected profile evidence, approval/run IDs, expiry, controls, and excluded authorities, but it does not run a live scan or start TypeScript tooling.
**Tech Stack:** Python deterministic fixture module/tests; Python active doctrine gate; Markdown boundary, review, and outcome docs.
**Authority boundary:** Non-runtime approval-envelope readiness only. No live Kuronode repository scan, no TypeScript tooling execution, no package-manager/network/model/browser/cyber tooling, no source/Git mutation by the gate, no live Codex, no production/generic/reusable BLK-test MCP, no protected BLK-req body reads, no BEO publication, no RTM generation, and no production isolation claim.

---

## 1. Current Known State

Preflight:

```text
date: 2026-05-10T19:54:23+10:00
git status --short --branch: ## main...origin/main
git log -1 --oneline: 740a998 feat: add kuronode validation profile fixture registry
git ls-remote origin refs/heads/main: 740a998f74f932785ba770ad979437b9ab89cc33 refs/heads/main
```

ID discovery:

```text
BLK-SYSTEM-058 plan: not present before this sprint
BLK-063 document: not present before this sprint
BLK-SYSTEM-058 outcomes: not present before this sprint
```

---

## 2. Next-Sprint Selection Rationale

BLK-059 recommends either a publication pilot or a Kuronode gate pilot after the BEO approval envelope and Kuronode mechanical gates are in place. This operator request does not separately grant actual BEO publication, live Codex execution, runtime RTM generation, production BLK-test MCP, package-manager/tooling authority, or live Kuronode scan authority.

BLK-SYSTEM-057 completed the safe fixture self-test registry rung, but a real Kuronode gate pilot still needs an exact target, approval ID, run ID, expiry, output bounds, operator-stop controls, replay policy, and hostile-review boundary. Therefore the next logical unblocked sprint is a non-runtime approval-envelope fixture for that future pilot.

This is not another generic preparatory rung: it removes the concrete blocker that BLK-059 line 242-244 identifies for a future bounded Kuronode gate pilot, while preserving the stop condition that no live scan/tooling can occur without explicit later approval.

---

## 3. Governing Doctrine Alignment

- **BLK-059:** Workstream B calls for Kuronode static validation profiles and checks before broader Kuronode execution, and says a bounded Kuronode gate pilot requires explicit scope.
- **BLK-058:** Defines the Kuronode TypeScript Power-of-Ten tactical standard that the future pilot would check.
- **BLK-061:** Defines fixture-only static profile semantics and denies live scans/tooling/source mutation.
- **BLK-062:** Registers only a fixture self-test validation profile and denies PASS-as-live-validation.
- **BLK-001:** Preserves separation between planning, deterministic enforcement, verification evidence, BEO publication, and future RTM.
- **BLK-003:** Preserves human dispatch gates and prevents validation readiness from inheriting runtime/publication/RTM approval.
- **BLK-004:** Keeps validation profile resolution repository-owned and deterministic; future pilot controls must not reintroduce arbitrary shell.
- **BLK-006:** Preserves protected-vault hard-deny semantics and no protected BLK-req body reads.
- **BLK-060:** Keeps actual authoritative BEO publication blocked pending separate explicit authority.

---

## 4. Non-Authority Boundary

This plan does not authorize production BLK-test MCP, generic BLK-test MCP, reusable BLK-test service startup, live Codex execution, arbitrary shell, caller-supplied commands, TypeScript tooling/typechecker/linter/formatter execution, package-manager/network/model/browser/cyber tooling, live Kuronode repository scans, source/Git mutation by BLK-test or by the Kuronode gate, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger append/mutation, rollback/revocation/supersession execution, runtime RTM generation, RTM drift rejection, active-vault hash comparison, coverage matrices, coverage claims, drift decisions, or production isolation claims.

Hermes sprint-closeout verification and exact-path Git commit/push are BLK-System repository maintenance. They are not capabilities granted to the Kuronode gate pilot envelope.

---

## 5. Implementation Intent

Create a deterministic Python fixture module that validates a future one-run Kuronode Power-of-Ten gate pilot approval envelope and returns:

```text
KURONODE_POWER_OF_TEN_GATE_PILOT_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
```

The envelope must require at least:

1. target package with exact `target_repo_identity`, `target_branch`, `target_head_sha`, `target_workspace_identity`, and `target_scope` values;
2. readiness evidence binding to BLK-061 and BLK-062 markers, the `kuronode-power-of-ten-static-fixture` profile name, exact profile command hash, and a source-bundle hash from the fixture static profile contract;
3. approval package with `approval_id`, `run_id`, `operator_identity`, `requested_at`, `expires_at`, and exact denied-authority set;
4. pilot controls with timeout/output bounds, operator stop, replay ledger identity, and cleanup obligation markers;
5. no-side-effect flags proving this sprint did not perform the future pilot.

The fixture must reject runtime-approval wording, live-scan claims, tooling/package-manager/network/Codex/BLK-test/BEO/RTM/protected-body laundering, stale or malformed timestamps, non-hex target hashes, weak proof markers, and any exact denied-authority mismatch.

---

## 6. Task Plan

### Task 000 — Plan and publish this sprint plan

Deliverables:

```text
docs/plans/blk-system-058_kuronode-power-of-ten-gate-pilot-approval-envelope.md
docs/outcomes/BLK-SYSTEM-058_task-000-outcome.md
```

Actions:

1. Record preflight state, ID discovery, and governing docs.
2. Publish the plan and Task 000 outcome.
3. Do not implement approval-envelope behavior in Task 000.

### Task 001 — Approval-envelope fixture via TDD

Deliverables:

```text
python/kuronode_power_of_ten_gate_pilot_approval_envelope.py
python/test_kuronode_power_of_ten_gate_pilot_approval_envelope.py
docs/outcomes/BLK-SYSTEM-058_task-001-outcome.md
```

Actions:

1. Write RED tests for a valid envelope producing the ready marker and no-side-effect flags.
2. Write RED tests for timestamp expiry, approval/run ID binding, target hash shape, exact profile command hash, exact denied-authority set, runtime/live-scan/tooling/package-manager/Codex/BLK-test/BEO/RTM/protected-body laundering, weak proof markers, and side-effect booleans.
3. Implement the smallest deterministic validator/builder that passes.
4. Verify focused tests.

### Task 002 — BLK-063 boundary, active doctrine gate, and hostile review

Deliverables:

```text
docs/BLK-063_kuronode-power-of-ten-gate-pilot-approval-envelope-boundary.md
python/test_active_doctrine_review_gates.py
docs/reviews/BLK-SYSTEM-058_kuronode-power-of-ten-gate-pilot-approval-envelope-hostile-review.md
docs/outcomes/BLK-SYSTEM-058_task-002-outcome.md
```

Actions:

1. Add BLK-063 boundary markers for non-runtime approval-envelope readiness.
2. Add a persistent active doctrine gate proving BLK-063 exists and denies live scan/tooling/source mutation/publication/RTM authority.
3. Hostile-review for PASS-as-live-validation, approval-as-runtime, profile-fixture-as-Kuronode-scan, package-manager/typecheck laundering, BLK-test/Codex escalation, protected-body/path leakage, BEO/RTM authority leakage, and under-scoped doctrine gates.
4. Remediate blockers with tests or docs before closeout.

### Task 003 — Verification, closeout, commit, and push

Deliverables:

```text
docs/outcomes/BLK-SYSTEM-058_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-058_sprint-closeout.md
```

Actions:

1. Run focused approval-envelope tests, focused active doctrine gate, full Python discovery, Go tests, Go vet, and `git diff --check`.
2. Record final verification output.
3. Stage exact paths only.
4. Commit and push to `origin/main`.
5. Report final commit hash.

---

## 7. Stop Conditions

Stop and report before closeout if any implementation:

1. runs a live Kuronode scan or treats the envelope as runtime approval;
2. executes TypeScript tooling, package managers, shell, network, browser, model-service, or cyber tooling;
3. starts BLK-test MCP or Codex;
4. mutates source or Git;
5. reads protected BLK-req bodies or accepts protected paths as pilot targets;
6. claims production sandbox/host-secret isolation;
7. publishes BEOs, generates RTM, claims coverage, or performs drift rejection;
8. treats fixture self-test PASS as live Kuronode validation, publication, RTM, Codex, BLK-test MCP, or source-mutation authority;
9. fails hostile review or verification.
