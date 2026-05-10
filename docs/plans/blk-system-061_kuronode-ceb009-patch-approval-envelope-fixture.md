# BLK-SYSTEM-061 — Kuronode CEB_009 Patch Approval Envelope Fixture Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, `test-driven-development`, and hostile review while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, by `docs/BLK-059_blk-system-post-058-roadmap.md` for current sequencing, and by BLK-001 through BLK-006 as applicable.

**Goal:** Convert BLK-SYSTEM-060's CEB_009 remediation packet into a deterministic patch approval-envelope fixture that is ready for future human review, without applying a Kuronode patch or executing validation tooling.
**BLK-024 / BLK-059 track:** Track D/J and BLK-059 Workstream B — Kuronode tactical quality intent; maturity L0/L1 approval-envelope fixture for a future exact-target patch, not source mutation or runtime validation authority.
**Architecture:** BLK-SYSTEM-059 produced static CEB_009 findings; BLK-SYSTEM-060 packaged those findings into remediation obligations. BLK-SYSTEM-061 builds the next authority rung: an exact-target, not-approved-yet patch approval envelope that binds the remediation packet hash to a future target repository identity, target path, allowed file set, required patch obligations, expiry/replay controls, and denied authority set. The envelope is review evidence only; it does not edit Kuronode, invoke Codex, run `npm run test:smoke`, launch Electron, or claim the patch is approved.
**Tech Stack:** Python deterministic fixture module/tests; Python active doctrine gate; Markdown boundary, hostile review, and outcome docs.
**Authority boundary:** Patch approval-envelope fixture only. No approval is granted by this sprint. No Kuronode source/Git mutation, no live Kuronode repository scan, no live source validation, no Electron launch, no smoke-test execution, no TypeScript tooling/typechecker/linter/formatter execution, no package-manager/network/model/browser/cyber tooling, no live Codex, no production/generic/reusable BLK-test MCP, no protected BLK-req body reads, no BEO publication, no RTM generation, and no production isolation claim.

---

## 1. Current Known State

Preflight:

```text
date: 2026-05-10T21:07:55+10:00
BLK-System git status --short --branch: ## main...origin/main
BLK-System git log -1 --oneline: 0523696 feat: add ceb009 remediation packet fixture
BLK-System git ls-remote origin refs/heads/main: 0523696f0b165d0e4bf0c61fd350a2af142d0590 refs/heads/main
```

ID discovery:

```text
BLK-SYSTEM-061 plan: not present before this sprint
BLK-066 document: not present before this sprint
BLK-SYSTEM-061 outcomes: not present before this sprint
```

Relevant completed state:

```text
BLK-SYSTEM-060 ready marker: KURONODE_POWER_OF_TEN_CEB009_REMEDIATION_PACKET_READY_NOT_PATCHED
BLK-SYSTEM-060 required obligations: CEB009_REMEDIATION_TIMEOUT_MUST_FAIL, CEB009_REMEDIATION_RESULT_SHAPE_VALIDATE_STREAM_ID, CEB009_REMEDIATION_RESULT_SHAPE_VALIDATE_AST, CEB009_REMEDIATION_REMOVE_ANY_AND_TS_IGNORE, CEB009_REMEDIATION_PRESERVE_CLEANUP_UNSUB_AND_CLOSE, CEB009_REMEDIATION_NOT_RUNTIME_VALIDATION
Kuronode target HEAD retained as fixture identity: cb09d965c0407612c9ce8fc9cc58c5e62c82e1b2
```

---

## 2. Why This Is the Next Logical Sprint

BLK-SYSTEM-060 deliberately stopped before patch approval. The next safe non-runtime step is to prepare an exact approval envelope for a future patch. This adds concrete safety value because it prevents a future operator or agent from treating the remediation packet as implicit approval, while still making the eventual patch request reviewable.

The envelope must force future review of:

1. exact target repository identity and target path;
2. exact allowed file set for the future patch;
3. remediation packet hash and required obligation set;
4. replay, expiry, output-bound, cleanup, and operator-stop controls;
5. explicit denial that this envelope is already approved, patched, tested, published, or trace-closed.

---

## 3. Governing Doctrine Alignment

- **BLK-059:** Workstream B supports progressing Kuronode TypeScript quality through deterministic gates and bounded approval envelopes without laundering runtime authority.
- **BLK-058:** Supplies the tactical TypeScript constraints to be enforced by any future patch: bounded waits, validated IPC outputs, explicit cleanup, checked results, and no unsafe suppressions at architecture boundaries.
- **BLK-064 / BLK-065:** Supply the static findings and remediation-packet boundaries. This sprint consumes those artifacts but must not reinterpret them as source mutation or live validation approval.
- **BLK-061 / BLK-062 / BLK-063:** Remain fixture/static/profile/envelope boundaries only; no live scan or tooling authority is inherited.
- **BLK-001:** Preserves V-model separation between approval request, tactical implementation, deterministic enforcement, BLK-test evidence, publication, and trace closure.
- **BLK-002 / BLK-005:** No BLK-req lifecycle change; no active or protected artifact read/mutation authority.
- **BLK-003:** Preserves human dispatch gates, bounded tactical packets, and separation between execution, testing, publication, and RTM authorities.
- **BLK-004:** Keeps `blk-pipe` as final mutation authority for any future source change; this sprint does not invoke BLK-pipe or broaden validation command authority.
- **BLK-006:** Preserves protected-vault hard-deny semantics and no protected BLK-req body reads.

---

## 4. Non-Authority Boundary

This plan does not authorize production BLK-test MCP, generic BLK-test MCP, reusable BLK-test service startup, live Codex execution, arbitrary shell, caller-supplied commands, Electron launch, headless smoke-test execution, wall-clock timeout waits, TypeScript tooling/typechecker/linter/formatter execution, package-manager/network/model/browser/cyber tooling, live Kuronode repository scans, live Kuronode source validation, Kuronode source mutation, Kuronode Git mutation, source/Git mutation by BLK-test or by the Kuronode gate, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger append/mutation, rollback/revocation/supersession execution, runtime RTM generation, RTM drift rejection, active-vault hash comparison, coverage matrices, coverage claims, drift decisions, or production isolation claims.

Hermes sprint-closeout verification and exact-path Git commit/push are BLK-System repository maintenance. They are not capabilities granted to the CEB_009 patch approval envelope.

---

## 5. Implementation Intent

Create a deterministic Python approval-envelope module that consumes the BLK-SYSTEM-060 remediation packet and emits:

```text
KURONODE_POWER_OF_TEN_CEB009_PATCH_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PATCHED
```

The envelope must include:

1. remediation packet identity and `remediation_packet_hash` bound to BLK-SYSTEM-060 output;
2. exact future target repository identity, target branch, target HEAD, and target path `scripts/smoke_test.ts`;
3. exact allowed modified files and allowed new files for the future patch;
4. required remediation obligations inherited from BLK-SYSTEM-060;
5. future approval identifiers, run identifiers, requested/expires timestamps, replay ledger identity, output bounds, cleanup requirements, and operator-stop control;
6. exact denied-authority set equality and metadata laundering rejection;
7. no-side-effect flags proving no approval granted, no patch applied, no live scan, no Electron/smoke execution, no tooling/package-manager, no source/Git mutation, no Codex/BLK-test MCP, no protected-body read, no BEO publication, no RTM generation, no coverage claim, and no production-isolation claim;
8. deterministic `envelope_hash` over the envelope body excluding the hash field.

The sprint must not create `CEO_009`, must not edit `/home/dad/code/Kuronode-v1/scripts/smoke_test.ts`, and must not run Kuronode validation commands.

---

## 6. Task Plan

### Task 000 — Plan and publish this sprint plan

Deliverables:

```text
docs/plans/blk-system-061_kuronode-ceb009-patch-approval-envelope-fixture.md
docs/outcomes/BLK-SYSTEM-061_task-000-outcome.md
```

Actions:

1. Record preflight state, ID discovery, governing docs, and selected scope.
2. Publish the plan and Task 000 outcome.
3. Do not implement approval-envelope behavior in Task 000.

### Task 001 — CEB_009 patch approval envelope fixture via TDD

Deliverables:

```text
python/kuronode_power_of_ten_ceb009_patch_approval_envelope.py
python/test_kuronode_power_of_ten_ceb009_patch_approval_envelope.py
docs/outcomes/BLK-SYSTEM-061_task-001-outcome.md
```

Actions:

1. Write RED tests for a valid BLK-SYSTEM-060 remediation packet producing the ready-for-human-review-not-approved-not-patched marker and no-side-effect flags.
2. Write RED tests that the envelope binds target repo/path/head, allowed file set, required obligations, replay/expiry controls, output bounds, cleanup, and operator stop.
3. Write RED tests for authority-laundering rejection, exact denied-authority mismatch, remediation packet hash mismatch, missing required obligations, expired/malformed timestamps, target path mismatch, and forbidden runtime/tooling/source-mutation claims.
4. Implement the smallest deterministic envelope builder that passes.
5. Verify focused tests.

### Task 002 — BLK-066 boundary, active doctrine gate, and hostile review

Deliverables:

```text
docs/BLK-066_kuronode-ceb009-patch-approval-envelope-boundary.md
python/test_active_doctrine_review_gates.py
docs/reviews/BLK-SYSTEM-061_kuronode-ceb009-patch-approval-envelope-hostile-review.md
docs/outcomes/BLK-SYSTEM-061_task-002-outcome.md
```

Actions:

1. Add BLK-066 boundary markers for a CEB_009 patch approval envelope that is ready for human review, not approved, not patched, and not runtime validation.
2. Add a persistent active doctrine gate proving BLK-066 denies live Kuronode scans, source/Git mutation, Electron/smoke-test execution, TypeScript tooling, package managers, live Codex, BLK-test MCP, BEO publication, RTM generation, protected-body reads, coverage/drift claims, and production isolation claims.
3. Hostile-review for approval-envelope-as-approval, target-envelope-as-patch, remediation packet as source mutation, static finding as live validation, replay/expiry weakening, target/path mismatch, package-manager/smoke-test laundering, protected-path leakage, BEO/RTM authority leakage, and under-scoped doctrine gates.
4. Remediate blockers with tests or docs before closeout.

### Task 003 — Verification, closeout, commit, and push

Deliverables:

```text
docs/outcomes/BLK-SYSTEM-061_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-061_sprint-closeout.md
```

Actions:

1. Run focused CEB_009 patch approval envelope tests.
2. Run focused BLK-066 active doctrine gate.
3. Run full Python discovery.
4. Run Go tests and Go vet.
5. Run `git diff --check` and markdown fence checks.
6. Record final verification output.
7. Stage exact paths only.
8. Commit and push to `origin/main`.
9. Report final commit hash.

---

## 7. Stop Conditions

Stop and report before closeout if any implementation:

1. treats this sprint as approval to patch Kuronode;
2. edits Kuronode source or Git;
3. runs `npm run test:smoke`, launches Electron, or waits for the 30-second timeout path;
4. scans the live Kuronode checkout beyond existing BLK-System-owned fixture material;
5. executes TypeScript tooling, package managers, shell, network, browser, model-service, or cyber tooling;
6. starts BLK-test MCP or Codex;
7. reads protected BLK-req bodies or accepts protected paths as envelope targets;
8. claims production sandbox/host-secret isolation;
9. publishes BEOs, generates RTM, claims coverage, or performs drift rejection;
10. treats the approval envelope as granted approval, source fix, live validation, BEO/CEO publication, RTM, Codex, BLK-test MCP, source-mutation, or production authority;
11. fails hostile review or verification.
