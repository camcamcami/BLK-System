# BLK-SYSTEM-059 — Kuronode CEB_009 Power-of-Ten Static Gate Pilot Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and Kuronode-specific architecture skills while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, by `docs/BLK-059_blk-system-post-058-roadmap.md` for current sequencing, and by BLK-001 through BLK-006 as applicable.

**Goal:** Run a bounded, non-tooling static Power-of-Ten pilot over BLK-System-owned CEB_009 test material, producing deterministic findings without launching Electron, waiting for the 30-second timeout, scanning the live Kuronode repository, or mutating source.
**BLK-024 / BLK-059 track:** Track D/J and BLK-059 Workstream B — Kuronode tactical quality intent; maturity L1 static-fixture pilot over real CEB-derived material, not runtime validation authority.
**Architecture:** BLK-SYSTEM-056 created the fixture-only static profile, BLK-SYSTEM-057 registered the fixture self-test profile, and BLK-SYSTEM-058 created the approval-envelope readiness layer for a future bounded pilot. BLK-SYSTEM-059 uses CEB_009 as concrete test material but keeps the pilot static and BLK-System-owned: the sprint should materialize a fixture corpus from CEB_009/L2-packet snippets and current observed `smoke_test.ts` shape, then run deterministic Python checks only. The pilot must report findings, not fix Kuronode code.
**Tech Stack:** Python deterministic fixture module/tests; Python active doctrine gate; Markdown boundary, review, and outcome docs.
**Authority boundary:** Static fixture pilot only. No live Kuronode repository scan, no Electron launch, no `npm run test:smoke`, no TypeScript tooling/typechecker/linter/formatter execution, no package-manager/network/model/browser/cyber tooling, no source/Git mutation by the gate, no live Codex, no production/generic/reusable BLK-test MCP, no protected BLK-req body reads, no BEO publication, no RTM generation, and no production isolation claim.

---

## 1. Current Known State

Preflight:

```text
date: 2026-05-10T20:29:15+10:00
BLK-System git status --short --branch: ## main...origin/main
BLK-System git log -1 --oneline: a6929ce feat: add kuronode gate pilot approval envelope
BLK-System git ls-remote origin refs/heads/main: a6929cef3478c925a580578ab793ef9db06364ba refs/heads/main
Kuronode git status --short --branch: ## main...origin/main
Kuronode HEAD: cb09d965c0407612c9ce8fc9cc58c5e62c82e1b2
Kuronode git log -1 --oneline: cb09d96 Move EWF_002 and EWF_003 from docs/execution briefs/ to root docs/
```

ID discovery:

```text
BLK-SYSTEM-059 plan: not present before this sprint
BLK-064 document: not present before this sprint
BLK-SYSTEM-059 outcomes: not present before this sprint
```

CEB_009 material discovered:

```text
/home/dad/code/Kuronode-v1/docs/execution briefs/CEB_009.md
/home/dad/code/Kuronode-v1/docs/execution briefs/l2_packets/CEB_009_L2_packet.md
/home/dad/code/Kuronode-v1/scripts/smoke_test.ts
```

No `CEO_009` closeout file was found during planning.

---

## 2. Why CEB_009 Is Good Static Pilot Material

CEB_009 is narrow but non-trivial. It is better than a toy snippet because it exercises Kuronode TypeScript safety concerns in a real Electron/headless-smoke context:

1. timeout false-pass risk: `setTimeout(..., 30000)` resolves a timeout object, but the current handler still logs `[PASS]` and exits 0;
2. bounded wait semantics: `waitForSelector(..., { timeout: 10000 })` and a 30-second projection timeout exist;
3. cleanup semantics: `electronApp.close()` exists in `finally`, and `unsub()` exists for the IPC listener;
4. result-shape validation gap: `streamId`/`ast` validation is required by CEB_009 but absent from the current observed smoke test;
5. unsafe typing/suppression: `@ts-ignore` and `(result as any)` appear in the current observed file and/or CEB_009 packet;
6. Electron IPC/preload boundary risk: the fix touches main-process IPC handler registration and preload context bridge exposure;
7. package/tooling temptation: CEB_009's operational validation command is `npm run test:smoke`, but this sprint must not run it.

The pilot therefore tests the static gate's ability to produce useful review findings without requiring a 30-to-40-second headless Electron timeout path.

---

## 3. Governing Doctrine Alignment

- **BLK-059:** Workstream B says Kuronode TypeScript Power-of-Ten doctrine should become deterministic repository-owned checks before broader Kuronode execution. This sprint satisfies the mechanical-gate rule without adding runtime authority.
- **BLK-058:** Supplies the Power-of-Ten rules and Kuronode overlays: bounded loops/timeouts, no dynamic execution, validated IPC/parser boundaries, lifecycle cleanup, small functions, checked results, no unsafe warnings, and no authority laundering.
- **BLK-061:** Supplies the fixture-only static-profile boundary. BLK-SYSTEM-059 may reuse the evaluator but must not convert fixture PASS/BLOCKED into live Kuronode validation authority.
- **BLK-062:** Registers only the `kuronode-power-of-ten-static-fixture` self-test profile. A self-test PASS is not a live Kuronode scan.
- **BLK-063:** Provides a future human-review approval envelope. This plan does not claim BLK-063 is runtime approval; it stays static and fixture-owned.
- **BLK-001:** Preserves V-model separation between planning, deterministic enforcement, verification evidence, BEO publication, and future RTM trace closure.
- **BLK-002 / BLK-005:** Do not change BLK-req staging, linting, baselining, canonical hashes, or artifact lifecycle.
- **BLK-003:** Preserves human dispatch gates, Layer 2 bounded context, failure ceilings, and no implicit inheritance between execution, testing, publication, and RTM.
- **BLK-004:** Keeps validation behavior repository-owned and deterministic; no caller-supplied shell and no arbitrary validation command expansion.
- **BLK-006:** Preserves protected-vault hard-deny semantics and no protected BLK-req body reads.

---

## 4. Non-Authority Boundary

This plan does not authorize production BLK-test MCP, generic BLK-test MCP, reusable BLK-test service startup, live Codex execution, arbitrary shell, caller-supplied commands, TypeScript tooling/typechecker/linter/formatter execution, package-manager/network/model/browser/cyber tooling, live Kuronode repository scans, source/Git mutation by BLK-test or by the Kuronode gate, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger append/mutation, rollback/revocation/supersession execution, runtime RTM generation, RTM drift rejection, active-vault hash comparison, coverage matrices, coverage claims, drift decisions, or production isolation claims.

Hermes sprint-closeout verification and exact-path Git commit/push are BLK-System repository maintenance. They are not capabilities granted to the Kuronode static gate pilot.

---

## 5. Implementation Intent

Create a deterministic Python pilot module that materializes a BLK-System-owned CEB_009 static corpus and evaluates it through existing BLK-058/BLK-061 static profile logic plus CEB_009-specific findings.

The report should return a marker such as:

```text
KURONODE_POWER_OF_TEN_CEB009_STATIC_GATE_PILOT_FINDINGS_READY_NOT_RUNTIME
```

The report must include:

1. source corpus identity for CEB_009 and Kuronode HEAD observed during planning;
2. explicit no-side-effect flags showing no live scan, no Electron launch, no smoke test, no tooling/package manager, no source/Git mutation, no Codex/BLK-test MCP, no BEO/RTM, and no protected-body read;
3. static profile findings from `evaluate_kuronode_power_of_ten_static_profile` over the corpus descriptors;
4. CEB_009-specific semantic findings, including at minimum:
   - `CEB009_TIMEOUT_FALSE_PASS_RISK` when a timeout sentinel can flow to `[PASS]`/exit 0;
   - `CEB009_RESULT_SHAPE_VALIDATION_MISSING` when `streamId` and `ast` are not checked before PASS;
   - `CEB009_TIMEOUT_BOUND_RECORDED` as positive evidence when the 30-second bound exists but was not executed;
   - `CEB009_CLEANUP_PATH_RECORDED` as positive evidence when `finally`/`close()` and listener unsubscribe cleanup are present;
   - `CEB009_UNSAFE_ANY_OR_TS_IGNORE_RECORDED` for unsafe suppressions/casts;
5. exact denied-authority set equality and authority-laundering rejection for metadata or source text;
6. deterministic `report_hash` over the report body excluding the hash field.

The sprint must not run `npm run test:smoke`; the `30000` timeout is fixture content, not a wall-clock wait.

---

## 6. Task Plan

### Task 000 — Plan and publish this sprint plan

Deliverables:

```text
docs/plans/blk-system-059_kuronode-ceb009-power-of-ten-static-gate-pilot.md
docs/outcomes/BLK-SYSTEM-059_task-000-outcome.md
```

Actions:

1. Record preflight state, ID discovery, CEB_009 material discovery, and governing docs.
2. Publish the plan and Task 000 outcome.
3. Do not implement static-pilot behavior in Task 000.

### Task 001 — CEB_009 static pilot corpus and report via TDD

Deliverables:

```text
python/kuronode_power_of_ten_ceb009_static_gate_pilot.py
python/test_kuronode_power_of_ten_ceb009_static_gate_pilot.py
docs/outcomes/BLK-SYSTEM-059_task-001-outcome.md
```

Actions:

1. Write RED tests for a valid CEB_009 corpus producing the ready-not-runtime marker and no-side-effect flags.
2. Write RED tests that the report captures timeout false-pass risk, missing result-shape validation, unsafe `any`/`@ts-ignore`, positive timeout bound evidence, and positive cleanup evidence.
3. Write RED tests for authority-laundering rejection, exact denied-authority mismatch, protected BLK-req path rejection, and source-bundle/report hash mismatch.
4. Implement the smallest deterministic corpus/report builder that passes.
5. Verify focused tests.

### Task 002 — BLK-064 boundary, active doctrine gate, and hostile review

Deliverables:

```text
docs/BLK-064_kuronode-ceb009-power-of-ten-static-gate-pilot-boundary.md
python/test_active_doctrine_review_gates.py
docs/reviews/BLK-SYSTEM-059_kuronode-ceb009-power-of-ten-static-gate-pilot-hostile-review.md
docs/outcomes/BLK-SYSTEM-059_task-002-outcome.md
```

Actions:

1. Add BLK-064 boundary markers for a CEB_009 static gate pilot that is findings-ready, not runtime authority.
2. Add a persistent active doctrine gate proving BLK-064 exists and denies live Kuronode scans, Electron/smoke-test execution, TypeScript tooling, package managers, source/Git mutation, live Codex, BLK-test MCP, BEO publication, RTM generation, protected-body reads, coverage/drift claims, and production isolation claims.
3. Hostile-review for static-PASS-as-live-validation, CEB_009-findings-as-Kuronode-fix, timeout-bound-as-executed-test, cleanup-vocabulary false positives, `any`/`@ts-ignore` under-reporting, package-manager/smoke-test laundering, BLK-test/Codex escalation, protected-path leakage, BEO/RTM authority leakage, and under-scoped doctrine gates.
4. Remediate blockers with tests or docs before closeout.

### Task 003 — Verification, closeout, commit, and push

Deliverables:

```text
docs/outcomes/BLK-SYSTEM-059_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-059_sprint-closeout.md
```

Actions:

1. Run focused CEB_009 static gate pilot tests.
2. Run focused BLK-064 active doctrine gate.
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

1. runs `npm run test:smoke`, launches Electron, or waits for the 30-second timeout path;
2. scans the live Kuronode checkout beyond explicitly copied BLK-System-owned fixture material;
3. executes TypeScript tooling, package managers, shell, network, browser, model-service, or cyber tooling;
4. starts BLK-test MCP or Codex;
5. mutates Kuronode source or Git;
6. reads protected BLK-req bodies or accepts protected paths as pilot targets;
7. claims production sandbox/host-secret isolation;
8. publishes BEOs, generates RTM, claims coverage, or performs drift rejection;
9. treats fixture self-test PASS, static-pilot findings, timeout bounds, or CEB_009 material as live Kuronode validation, publication, RTM, Codex, BLK-test MCP, source-mutation, or production authority;
10. fails hostile review or verification.
