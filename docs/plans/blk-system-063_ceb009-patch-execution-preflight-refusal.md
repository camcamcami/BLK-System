# BLK-SYSTEM-063 — CEB_009 Patch Execution Preflight Refusal Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, `test-driven-development`, and hostile review while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, by `docs/BLK-059_blk-system-post-058-roadmap.md` for current sequencing, and by BLK-001 through BLK-006 as applicable.

**Goal:** Add a deterministic CEB_009 patch execution preflight fixture that consumes the hardened patch approval envelope and refuses execution because no explicit patch approval exists.
**BLK-024 / BLK-059 track:** Track A/J and Workstream B — authority-boundary hygiene and Kuronode TypeScript Power-of-Ten safety; maturity L1 fixture-only / L2-style fail-closed preflight.
**Architecture:** BLK-SYSTEM-061 created a review-only exact-target patch approval envelope and BLK-SYSTEM-062 hardened its upstream identity. The next safe non-runtime rung is a preflight refusal adapter that proves the system will not treat a review-ready envelope as execution approval. The fixture returns a blocked status unless a later separate sprint grants explicit human patch authority; it does not call BLK-pipe, Codex, npm, TypeScript tooling, Electron, smoke tests, or Kuronode source mutation.
**Tech Stack:** Python deterministic fixture module/tests; Python active doctrine gate; Markdown boundary, hostile review, and outcome docs.
**Authority boundary:** Fixture-only preflight refusal. No approval is granted by this sprint. No Kuronode source/Git mutation, no live Kuronode repository scan, no live source validation, no Electron launch, no smoke-test execution, no TypeScript tooling/typechecker/linter/formatter execution, no package-manager/network/model/browser/cyber tooling, no live Codex, no BLK-pipe invocation, no production/generic/reusable BLK-test MCP, no protected BLK-req body reads, no BEO publication, no RTM generation, and no production isolation claim.

---

## 1. Current Known State

Preflight:

```text
date: 2026-05-11T06:55:54+10:00
BLK-System git status --short --branch: ## main...origin/main
BLK-System git log -1 --oneline: 241f7b7 feat: harden ceb009 approval envelope integrity
BLK-System git ls-remote origin refs/heads/main: 241f7b72edf129183ffd608f28aeea052b6fb074 refs/heads/main
```

ID discovery:

```text
BLK-SYSTEM-063 plan: not present before this sprint
BLK-068 document: not present before this sprint
BLK-SYSTEM-063 outcomes: not present before this sprint
```

Relevant completed state:

```text
BLK-SYSTEM-061 envelope marker: KURONODE_POWER_OF_TEN_CEB009_PATCH_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PATCHED
BLK-SYSTEM-062 hardening marker: KURONODE_POWER_OF_TEN_CEB009_PATCH_APPROVAL_ENVELOPE_INTEGRITY_HARDENED_UPSTREAM_HASH_RECOMPUTED
No explicit Kuronode patch approval exists in current doctrine.
```

---

## 2. Why This Is the Next Logical Sprint

After a hardened review-only approval envelope exists, the remaining dangerous ambiguity is operational: a later runner could accidentally consume the review envelope as if it were approval to patch. Because the operator has not explicitly granted patch/runtime authority, the safe next step is not a patch. It is a fail-closed preflight fixture that demonstrates the envelope is recognized but blocked pending explicit human approval.

This sprint creates the blocked handoff shape needed before any future patch sprint. It preserves audit value without crossing into source mutation or runtime validation.

---

## 3. Governing Doctrine Alignment

- **BLK-001:** Preserves V-model separation between evidence, approval, tactical mutation, verification, publication, and trace closure.
- **BLK-002 / BLK-005:** Preserves canonical hash handling without introducing protected BLK-req active-vault reads or body parsing.
- **BLK-003:** Preserves human confirmation gates and does not invoke BLK-pipe, Codex, or BLK-test.
- **BLK-004:** Keeps `blk-pipe` as final mutation authority for future source changes; this sprint does not invoke it or broaden validation command authority.
- **BLK-006:** Preserves protected-vault hard-deny/no-read semantics.
- **BLK-059:** Continues Kuronode tactical-quality work without silently crossing into runtime/source mutation authority.
- **BLK-066 / BLK-067:** Supply the review-only envelope and integrity hardening boundaries consumed by this preflight refusal.

---

## 4. Non-Authority Boundary

This plan does not authorize production BLK-test MCP, generic BLK-test MCP, reusable BLK-test service startup, live Codex execution, live tactical LLM execution, BLK-pipe invocation, arbitrary shell, caller-supplied commands, Electron launch, headless smoke-test execution, wall-clock timeout waits, TypeScript tooling/typechecker/linter/formatter execution, package-manager/network/model/browser/cyber tooling, live Kuronode repository scans, live Kuronode source validation, Kuronode source mutation, Kuronode Git mutation, source/Git mutation by BLK-test or by a Kuronode gate, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger append/mutation, rollback/revocation/supersession execution, runtime RTM generation, RTM drift rejection, active-vault hash comparison, coverage matrices, coverage claims, drift decisions, or production isolation claims.

Hermes sprint-closeout verification and exact-path Git commit/push are BLK-System repository maintenance. They are not capabilities granted to the CEB_009 patch execution preflight.

---

## 5. Implementation Intent

Create `python/kuronode_power_of_ten_ceb009_patch_execution_preflight.py` that consumes a hardened BLK-SYSTEM-061/062 envelope and returns:

```text
KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_PREFLIGHT_BLOCKED_PENDING_HUMAN_APPROVAL_NOT_EXECUTED
```

The preflight must:

1. recompute the submitted envelope hash excluding `envelope_hash`;
2. require the review-only/not-approved/not-patched envelope status;
3. require BLK-SYSTEM-062 integrity marker and `remediation_packet_hash_recomputed=True`;
4. require `approval_granted=False` and reject any attempt to flip it to true in this sprint;
5. require exact target repo/head/path/allowlist identity inherited from the envelope;
6. require exact denied-authority equality and no-side-effect flags;
7. emit `execution_blocked=True`, `block_reason=EXPLICIT_HUMAN_PATCH_APPROVAL_REQUIRED`, and no execution side effects;
8. reject runtime/tooling/patch/Codex/BLK-test/BEO/RTM/protected-path laundering in preflight request metadata.

The sprint must not create `CEO_009`, must not edit `/home/dad/code/Kuronode-v1/scripts/smoke_test.ts`, and must not run Kuronode validation commands.

---

## 6. Task Plan

### Task 000 — Plan and publish this sprint plan

Deliverables:

```text
docs/plans/blk-system-063_ceb009-patch-execution-preflight-refusal.md
docs/outcomes/BLK-SYSTEM-063_task-000-outcome.md
```

Actions:

1. Record preflight state, ID discovery, governing docs, and selected scope.
2. Publish the plan and Task 000 outcome.
3. Do not implement preflight behavior in Task 000.

### Task 001 — Patch execution preflight refusal via TDD

Deliverables:

```text
python/kuronode_power_of_ten_ceb009_patch_execution_preflight.py
python/test_kuronode_power_of_ten_ceb009_patch_execution_preflight.py
docs/outcomes/BLK-SYSTEM-063_task-001-outcome.md
```

Actions:

1. Add RED tests for a valid hardened review-only envelope returning blocked pending human approval with no side effects.
2. Add RED tests rejecting missing BLK-SYSTEM-062 integrity markers, stale envelope hashes, approval flags flipped to true, exact target mismatch, allowlist mismatch, and denied-authority weakening.
3. Add RED tests for authority-laundering request metadata (`APPROVED_FOR_LIVE_EXECUTION`, `patch Kuronode now`, `npm run test:smoke`, `Codex`, `RTMGenerated`, double-encoded protected paths).
4. Implement the smallest GREEN preflight builder that passes.
5. Preserve no source/Git/runtime/tooling/publication/RTM side effects.

### Task 002 — BLK-068 boundary, active doctrine gate, and hostile review

Deliverables:

```text
docs/BLK-068_ceb009-patch-execution-preflight-refusal-boundary.md
python/test_active_doctrine_review_gates.py
docs/reviews/BLK-SYSTEM-063_ceb009-patch-execution-preflight-refusal-hostile-review.md
docs/outcomes/BLK-SYSTEM-063_task-002-outcome.md
```

Actions:

1. Add BLK-068 boundary markers for blocked pending human approval, no execution, no patch, no runtime validation, no BLK-pipe/Codex/BLK-test invocation, and no protected-body reads.
2. Add a persistent active doctrine gate proving BLK-068 denies inherited approval, forged execution from review envelope readiness, live Kuronode scans, source/Git mutation, Electron/smoke-test execution, TypeScript tooling, package managers, live Codex, BLK-pipe invocation, BLK-test MCP, BEO publication, RTM generation, protected-body reads, coverage/drift claims, and production isolation claims.
3. Hostile-review review-envelope-as-approval, hardening-marker-as-approval, block-status-as-success, PASS-as-patch, request metadata laundering, exact target/allowlist weakening, stale envelope hash acceptance, approval-flag flip acceptance, and under-scoped doctrine gates.
4. Remediate blockers with tests or docs before closeout.

### Task 003 — Verification, closeout, commit, and push

Deliverables:

```text
docs/outcomes/BLK-SYSTEM-063_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-063_sprint-closeout.md
```

Actions:

1. Run focused CEB_009 patch execution preflight tests.
2. Run focused BLK-068 active doctrine gate.
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
5. executes TypeScript tooling, package managers, network, browser, model-service, or cyber tooling;
6. invokes BLK-pipe, starts BLK-test MCP, or starts Codex;
7. reads protected BLK-req bodies or accepts protected paths as preflight targets;
8. claims production sandbox/host-secret isolation;
9. publishes BEOs, generates RTM, claims coverage, or performs drift rejection;
10. treats the preflight blocked result as success, approval, source fix, live validation, BEO/CEO publication, RTM, Codex, BLK-test MCP, BLK-pipe execution, source-mutation, or production authority;
11. fails hostile review or verification.
