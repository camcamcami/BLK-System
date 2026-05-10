# BLK-SYSTEM-064 — CEB_009 Patch Execution Authority Request Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, `test-driven-development`, and hostile review while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, by `docs/BLK-059_blk-system-post-058-roadmap.md` for current sequencing, and by BLK-001 through BLK-006 as applicable.

**Goal:** Convert the BLK-SYSTEM-063 blocked preflight into a deterministic human-decision authority-request package for a future CEB_009 patch execution, without granting approval or executing the patch.
**BLK-024 / BLK-059 track:** Track A/J and Workstream B — authority-boundary hygiene and Kuronode TypeScript Power-of-Ten safety; maturity L0/L1 request/fixture only.
**Architecture:** BLK-SYSTEM-063 proved that a hardened review envelope is not executable without explicit human approval. The next safe non-runtime rung is an authority-request package that preserves the blocked preflight, exact target, validation profile intent, replay/expiry/operator-stop requirements, rollback expectations, and outcome obligations for a future human decision. This sprint does not accept approval, does not invoke BLK-pipe, does not patch Kuronode, and does not run Kuronode validation.
**Tech Stack:** Python deterministic fixture module/tests; Python active doctrine gate; Markdown boundary, hostile review, and outcome docs.
**Authority boundary:** Request/fixture only. No approval is granted by this sprint. No Kuronode source/Git mutation, no live Kuronode repository scan, no live source validation, no Electron launch, no smoke-test execution, no TypeScript tooling/typechecker/linter/formatter execution, no package-manager/network/model/browser/cyber tooling, no live Codex, no BLK-pipe invocation, no production/generic/reusable BLK-test MCP, no protected BLK-req body reads, no BEO/CEO publication, no RTM generation, no coverage/drift claim, and no production isolation claim.

---

## 1. Current Known State

Preflight:

```text
date: 2026-05-11T07:24:25+10:00
BLK-System git status --short --branch: ## main...origin/main
BLK-System git log -1 --oneline: 467908c feat: add ceb009 patch execution preflight refusal
BLK-System git ls-remote origin refs/heads/main: 467908c341ae2e05ec06801c023000a26aff1050 refs/heads/main
```

ID discovery:

```text
BLK-SYSTEM-064 plan: not present before this sprint
BLK-069 document: not present before this sprint
PATCH_EXECUTION_AUTHORITY_REQUEST marker: not present before this sprint
```

Relevant completed state:

```text
BLK-SYSTEM-061 envelope marker: KURONODE_POWER_OF_TEN_CEB009_PATCH_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PATCHED
BLK-SYSTEM-062 hardening marker: KURONODE_POWER_OF_TEN_CEB009_PATCH_APPROVAL_ENVELOPE_INTEGRITY_HARDENED_UPSTREAM_HASH_RECOMPUTED
BLK-SYSTEM-063 preflight marker: KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_PREFLIGHT_BLOCKED_PENDING_HUMAN_APPROVAL_NOT_EXECUTED
No explicit Kuronode patch execution approval exists in current doctrine.
```

---

## 2. Why This Is the Next Logical Sprint

BLK-SYSTEM-063 intentionally stops at `BLOCKED_PENDING_HUMAN_APPROVAL_NOT_EXECUTED`. BLK-068 says a future Kuronode patch sprint still requires separate explicit human approval and a separate execution plan defining exact targets, validation profiles, approval IDs, rollback expectations, replay/expiry semantics, operator stop controls, and hostile-review criteria.

Because the operator has not granted patch/runtime authority, the safe next step is not patch execution. It is a non-executing authority-request package that states exactly what a future human decision would need to approve while preserving the current blocked state.

---

## 3. Governing Doctrine Alignment

- **BLK-001:** Preserves V-model separation between request-readiness, tactical mutation, verification, publication, and trace closure.
- **BLK-002 / BLK-005:** Preserves canonical hash handling and does not introduce protected active-vault reads or body parsing.
- **BLK-003:** Preserves human dispatch gates and does not invoke BLK-pipe, Codex, or BLK-test.
- **BLK-004:** Keeps `blk-pipe` as final mutation enforcement for any future patch; this sprint only describes a future allowed file/profile package and does not invoke it.
- **BLK-006:** Preserves protected-vault hard-deny/no-read semantics.
- **BLK-059:** Continues Kuronode tactical-quality work without silently crossing into runtime/source mutation authority.
- **BLK-066 / BLK-067 / BLK-068:** Supply the review-only envelope, integrity hardening, and preflight refusal boundaries consumed by this authority request.

---

## 4. Non-Authority Boundary

This plan does not authorize production BLK-test MCP, generic BLK-test MCP, reusable BLK-test service startup, live Codex execution, live tactical LLM execution, BLK-pipe invocation, arbitrary shell, caller-supplied commands, Electron launch, headless smoke-test execution, wall-clock timeout waits, TypeScript tooling/typechecker/linter/formatter execution, package-manager/network/model/browser/cyber tooling, live Kuronode repository scans, live Kuronode source validation, Kuronode source mutation, Kuronode Git mutation, source/Git mutation by BLK-test or by a Kuronode gate, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, CEO_009 publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger append/mutation, rollback/revocation/supersession execution, runtime RTM generation, RTM drift rejection, active-vault hash comparison, coverage matrices, coverage claims, drift decisions, or production isolation claims.

Hermes sprint-closeout verification and exact-path Git commit/push are BLK-System repository maintenance. They are not capabilities granted to the CEB_009 patch execution authority request.

---

## 5. Implementation Intent

Create `python/kuronode_power_of_ten_ceb009_patch_execution_authority_request.py` that consumes the BLK-SYSTEM-063 blocked preflight record and returns:

```text
KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_AUTHORITY_REQUEST_READY_FOR_HUMAN_DECISION_NOT_EXECUTED
```

The authority request must:

1. recompute the submitted preflight hash excluding `preflight_hash`;
2. require `KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_PREFLIGHT_BLOCKED_PENDING_HUMAN_APPROVAL_NOT_EXECUTED`;
3. require `execution_blocked=True` and `block_reason=EXPLICIT_HUMAN_PATCH_APPROVAL_REQUIRED`;
4. require all preflight side-effect flags false;
5. require exact target repo/head/path/allowlist identity inherited from the preflight;
6. require exact denied-authority equality and no approval acceptance in this sprint;
7. define future-approval obligations for one exact run ID, expiry, replay ledger, operator stop, rollback expectation, cleanup expectation, output bound, outcome doc requirement, and hostile-review requirement;
8. define future validation profile identifiers as fixture strings only, not executable commands;
9. emit `approval_captured=False`, `execution_authorized=False`, `patch_executed=False`, `blk_pipe_invoked=False`, and no runtime/publication/RTM/protected-read side effects;
10. reject authority-laundering metadata, nested runtime approval, command strings (`npm run test:smoke`, `tsc`, package-manager/network/cyber tooling), BLK-pipe invocation claims, BEO/CEO/RTM claims, protected paths, and production-isolation claims.

The sprint must not create `CEO_009`, must not edit `/home/dad/code/Kuronode-v1/scripts/smoke_test.ts`, must not run Kuronode validation commands, and must not invoke BLK-pipe.

---

## 6. Task Plan

### Task 000 — Plan and publish this sprint plan

Deliverables:

```text
docs/plans/blk-system-064_ceb009-patch-execution-authority-request.md
docs/outcomes/BLK-SYSTEM-064_task-000-outcome.md
```

Actions:

1. Record preflight state, ID discovery, governing docs, and selected scope.
2. Publish the plan and Task 000 outcome.
3. Do not implement authority-request behavior in Task 000.

### Task 001 — Patch execution authority-request fixture via TDD

Deliverables:

```text
python/kuronode_power_of_ten_ceb009_patch_execution_authority_request.py
python/test_kuronode_power_of_ten_ceb009_patch_execution_authority_request.py
docs/outcomes/BLK-SYSTEM-064_task-001-outcome.md
```

Actions:

1. Add RED tests for a valid BLK-SYSTEM-063 blocked preflight producing a ready-for-human-decision authority request with no approval or side effects.
2. Add RED tests rejecting stale preflight hashes, non-blocked preflight state, target/allowlist mismatch, side-effect flag flips, and denied-authority weakening.
3. Add RED tests for authority-laundering request metadata and future validation profile command strings.
4. Implement the smallest GREEN authority-request builder that passes.
5. Preserve no source/Git/runtime/tooling/publication/RTM side effects.

### Task 002 — BLK-069 boundary, active doctrine gate, and hostile review

Deliverables:

```text
docs/BLK-069_ceb009-patch-execution-authority-request-boundary.md
python/test_active_doctrine_review_gates.py
docs/reviews/BLK-SYSTEM-064_ceb009-patch-execution-authority-request-hostile-review.md
docs/outcomes/BLK-SYSTEM-064_task-002-outcome.md
```

Actions:

1. Add BLK-069 boundary markers for human-decision request only, not approval, not patch execution, not BLK-pipe invocation, not runtime validation, not BEO/CEO publication, not RTM, and no protected-body reads.
2. Add a persistent active doctrine gate proving BLK-069 denies inherited approval from the review envelope, integrity hardening, preflight block, or authority-request readiness.
3. Hostile-review request-readiness-as-approval, preflight-block-as-approval, validation-profile-name-as-command, exact target/allowlist weakening, stale preflight hash acceptance, approval-capture claims, and under-scoped doctrine gates.
4. Remediate blockers with tests or docs before closeout.

### Task 003 — Verification, closeout, commit, and push

Deliverables:

```text
docs/outcomes/BLK-SYSTEM-064_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-064_sprint-closeout.md
```

Actions:

1. Run focused CEB_009 patch execution authority-request tests.
2. Run focused BLK-069 active doctrine gate.
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
2. accepts explicit approval as captured by this sprint;
3. edits Kuronode source or Git;
4. invokes BLK-pipe or starts a patch runner;
5. runs `npm run test:smoke`, launches Electron, or waits for the 30-second timeout path;
6. scans the live Kuronode checkout beyond existing BLK-System-owned fixture material;
7. executes TypeScript tooling, package managers, network, browser, model-service, or cyber tooling;
8. starts Codex or BLK-test MCP;
9. reads protected BLK-req bodies or accepts protected paths as future targets;
10. claims production sandbox/host-secret isolation;
11. publishes BEO/CEO artifacts, generates RTM, claims coverage, or performs drift rejection;
12. treats request-readiness as success, approval, source fix, live validation, BEO/CEO publication, RTM, Codex, BLK-test MCP, BLK-pipe execution, source mutation, or production authority;
13. fails hostile review or verification.
