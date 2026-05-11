# BLK-SYSTEM-080 — Tactical Standard Profile Registry / Layer B Extraction Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `blk-doctrine-gate-remediation` while executing. This plan is guided by historical maturity vocabulary in `docs/BLK-024_blk-system-development-roadmap.md`, current roadmap selection in `docs/BLK-077_blk-system-post-078-roadmap.md`, current-state indexing in `docs/BLK-079_post-078-current-state-authority-index.md`, tactical-standard profile architecture in `docs/BLK-078_tactical-standard-profile-architecture.md`, and BLK-001 through BLK-006 as applicable.

**Goal:** Implement the first BLK-System-owned tactical profile registry fixture and extract BLK-078 Layer B universal tactical-output safety into deterministic doctrine/gates while registering BLK-058 as the first Layer C `kuronode-typescript` profile source.
**BLK-024 track:** Track A — Doctrine, alignment, and review gates; Track D — Validation command profile tightening / maturity L0 doctrine-only plus L1 deterministic local fixture/gate tests.
**Architecture:** BLK-078 defines Layer A universal BLK-System core, Layer B universal tactical-output safety, and Layer C target tactical profiles. BLK-SYSTEM-080 converts that architecture into a BLK-System-owned fixture shape and boundary doctrine without authorizing live target scans, target mutation, runtime execution, BLK-test, BEO publication, or RTM.
**Tech Stack:** Markdown doctrine, Python unittest fixture validators, Go test/vet verification.
**Authority boundary:** BLK-System documentation and deterministic local fixture/gate work only. No CEB/CEO execution, no Kuronode source or Git mutation, no target-repo scan, no live Codex dispatch, no BLK-pipe execution, no production BLK-test MCP, no BEO publication, no RTM generation, no protected BLK-req body access, no package-manager/network/model/browser/cyber tooling, and no production sandbox or host-isolation claim.

---

## 0. Current Known State

Captured: `2026-05-11T19:48:20+10:00`

```text
repo: /home/dad/BLK-System
branch: main
local HEAD: 77ce12e51453b8944dbf510f5777288069a1ff26
remote main: 77ce12e51453b8944dbf510f5777288069a1ff26
status: ## main...origin/main
last commit: 77ce12e docs: close blk-system 079 authority index refresh
```

Discovery:

```text
existing BLK-080 doc: none
existing BLK-SYSTEM-080 plan/outcomes: none
current roadmap selector: docs/BLK-077_blk-system-post-078-roadmap.md
current authority index: docs/BLK-079_post-078-current-state-authority-index.md
profile architecture anchor: docs/BLK-078_tactical-standard-profile-architecture.md
first Layer C source: docs/BLK-058_kuronode-typescript-power-of-ten-tactical-standard.md
```

---

## 1. Selection Rationale

BLK-077 and BLK-079 now select BLK-SYSTEM-080 as the next logical sprint after BLK-SYSTEM-079.

BLK-078 already defines the three-layer model, but it intentionally leaves the real schema, registry, validator, fixture, and profile-selection mechanism to a later sprint. BLK-SYSTEM-080 is that sprint at the L0/L1 maturity rung:

1. extract Layer B universal tactical-output safety principles into BLK-System-owned doctrine and deterministic fixture data;
2. define a profile-selection/registry record shape that is review-only unless a later authority envelope selects it;
3. register BLK-058 as the first Layer C `kuronode-typescript` profile source;
4. preserve exact denied-authority equality for profile registry and selection records;
5. update roadmap/current-state docs so the next default sprint becomes BLK-SYSTEM-081 — Target-Repo Execution Governance Pattern.

This sprint deliberately does not implement broader target-repo execution governance, live scans, target mutation, BEO publication, RTM generation, live Codex, or Kuronode work. Those remain future frontiers.

---

## 2. Governing Alignment

| Document | Relevance | Preserved boundary |
| --- | --- | --- |
| BLK-001 | Defines separation between architecture, tactical execution, deterministic enforcement, verification evidence, BEO publication, and trace closure. | Profile registry records clarify constraints; they do not become execution or publication authority. |
| BLK-002 | Defines staged requirements/use-case intake and HITL promotion. | Profile registry/selection records must not read/copy/parse/hash/summarize/scan/mutate protected BLK-req bodies. |
| BLK-003 | Defines orchestration, human dispatch gates, BLK-pipe invocation, hostile audit, BLK-test evidence, and BEO handoff. | Profile selection may be future Layer 2 packet metadata, but this sprint does not create CEB/CEO artifacts or run execution. |
| BLK-004 | Defines BLK-pipe V47 and validation profile boundaries. | Repository-owned validation profile names remain metadata/constraints only; no arbitrary shell, BLK-pipe run, package-manager command, or target scan is authorized. |
| BLK-005 | Defines requirement/use-case trace binding and canonical hashes. | Profile records may bind to doc IDs, but they do not generate RTM, coverage, drift decisions, or protected-body comparisons. |
| BLK-006 | Defines protected-vault hard-deny and Discord/HITL authorization. | Protected-vault body reads/writes remain denied and no tactical worker receives protected-body access from this sprint. |
| BLK-058 | Defines the Kuronode TypeScript tactical standard. | BLK-058 is registered only as the first Layer C source for future approved work, not as Kuronode dispatch or mutation authority. |
| BLK-078 | Defines Layer A/B/C profile architecture. | This sprint implements L0/L1 registry and Layer B extraction fixtures without weakening any non-authority boundary. |
| BLK-079 | Current-state index selecting BLK-SYSTEM-080. | After this sprint, BLK-079 should point the default next sprint to BLK-SYSTEM-081. |

---

## 3. Exact Scope and File Allowlist

### Planning, outcomes, and review docs

```text
docs/plans/blk-system-080_tactical-standard-profile-registry-layer-b-extraction.md
docs/outcomes/BLK-SYSTEM-080_task-000-outcome.md
docs/outcomes/BLK-SYSTEM-080_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-080_task-002-outcome.md
docs/outcomes/BLK-SYSTEM-080_task-003-outcome.md
docs/reviews/BLK-SYSTEM-080_hostile-review.md
docs/outcomes/BLK-SYSTEM-080_sprint-closeout.md
```

### Doctrine docs

```text
docs/BLK-080_tactical-standard-profile-registry-and-layer-b-extraction.md
docs/BLK-077_blk-system-post-078-roadmap.md
docs/BLK-079_post-078-current-state-authority-index.md
```

### Deterministic local fixtures/gates

```text
python/blk_tactical_profile_registry.py
python/test_blk_tactical_profile_registry.py
python/test_active_doctrine_review_gates.py
```

No other files are in scope without a new human decision.

---

## 4. Explicitly Forbidden

This sprint does not authorize or perform:

- CEB writing, CEB dispatch, CEO writing, or CEO closeout execution;
- Kuronode feature implementation;
- Kuronode source mutation, Git mutation, staging, commit, push, reset, checkout, revert, stash, cleanup, or autofix;
- live target-repository scans or target-repository validation runs;
- TypeScript, Go, Python, linter, formatter, package-manager, browser, model-service, network, or cyber tooling execution against a target repository;
- live Codex execution, Codex subprocess startup, or reusable tactical LLM dispatch;
- BLK-pipe execution or source mutation outside exact approved allowlists;
- production/generic BLK-test MCP or reusable BLK-test service startup;
- arbitrary shell as BLK-test behavior;
- source or Git mutation by BLK-test;
- protected BLK-req vault body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison;
- authoritative BEO publication, runtime `PUBLISHED` output, signer/storage/ledger/rollback/revocation/supersession/release authority;
- runtime RTM generation, RTM drift rejection, public ledger mutation, active-vault hash comparison, or coverage-matrix authority;
- production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claims.

---

## 5. Required Registry and Layer B Contract

The sprint must produce a deterministic fixture module and doctrine document that:

1. define a stable registry ID and status for BLK-System tactical profile registry evidence;
2. extract all 12 BLK-078 Layer B universal tactical-output safety principles into stable identifiers;
3. register `kuronode-typescript` as the first Layer C profile with source doc BLK-058 and architecture anchor BLK-078;
4. define a profile-selection record that is planning/review metadata only and never runtime approval;
5. require exact denied-authority sets for registry and selection records;
6. reject missing, extra, duplicate, non-string, or unhashable denied-authority entries;
7. reject natural-language, key, and nested authority laundering for live scan, target mutation, live Codex, BLK-pipe execution, BLK-test production MCP, BEO publication, RTM, protected-body reads, package/network/model/browser/cyber tooling, and production isolation claims;
8. reject command-shaped validation profiles or target tooling strings such as package-manager, network, browser, or arbitrary shell commands;
9. force every denied runtime/target/publication/RTM flag to `False` when evaluating blocked records;
10. avoid live-surface imports/calls such as subprocess, socket, HTTP clients, dynamic imports, `eval`, `exec`, or file reads in the fixture module;
11. update persistent active doctrine gates for BLK-080 markers;
12. update BLK-077/BLK-079 after completion so BLK-SYSTEM-081 is the default next sprint.

---

## 6. Task Plan

### Task 000 — Plan publication

- Write this plan.
- Write `docs/outcomes/BLK-SYSTEM-080_task-000-outcome.md`.
- Verify markdown fences and `git diff --check` for exact plan paths.
- Commit and push the plan publication.

### Task 001 — RED/GREEN tactical profile registry fixture

- Add failing tests first in `python/test_blk_tactical_profile_registry.py` requiring:
  - all Layer B principles from BLK-078 have stable IDs;
  - `kuronode-typescript` is registered from BLK-058 as a Layer C source;
  - selection records are review-only and not runtime authority;
  - denied-authority set validation is exact and hostile;
  - natural-language and nested authority laundering fails closed;
  - command-shaped validation profile/tooling strings are rejected;
  - module source contains no live-surface imports/calls.
- Run the focused test and capture RED failure.
- Implement `python/blk_tactical_profile_registry.py` minimally.
- Rerun focused tests for GREEN.
- Write `docs/outcomes/BLK-SYSTEM-080_task-001-outcome.md`.
- Commit and push exact paths.

### Task 002 — BLK-080 doctrine document and active gate

- Add a failing active-doctrine gate in `python/test_active_doctrine_review_gates.py` requiring BLK-080 markers, non-authority language, Layer B extraction, Layer C registration, and persistent gate marker.
- Run the focused gate and capture RED failure.
- Create `docs/BLK-080_tactical-standard-profile-registry-and-layer-b-extraction.md`.
- Rerun the focused gate and fixture tests for GREEN.
- Write `docs/outcomes/BLK-SYSTEM-080_task-002-outcome.md`.
- Commit and push exact paths.

### Task 003 — Roadmap/current-state alignment after BLK-SYSTEM-080

- Add/update focused gates requiring BLK-077 and BLK-079 to record BLK-SYSTEM-080 completion and default next sprint BLK-SYSTEM-081.
- Run RED if those markers are not yet present.
- Patch `docs/BLK-077_blk-system-post-078-roadmap.md` and `docs/BLK-079_post-078-current-state-authority-index.md`.
- Rerun focused gates and fixture tests for GREEN.
- Write `docs/outcomes/BLK-SYSTEM-080_task-003-outcome.md`.
- Commit and push exact paths.

### Task 004 — Hostile review and closeout

- Review all changed paths for file-boundary drift, runtime-authority laundering, BLK-058/078 scope confusion, validation-profile command leakage, and stale next-sprint guidance.
- Run full verification:
  - markdown fence balance for new/changed markdown;
  - `git diff --check` for exact changed paths;
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'`;
  - `go test ./...`;
  - `go vet ./...`.
- Write `docs/reviews/BLK-SYSTEM-080_hostile-review.md`.
- Write `docs/outcomes/BLK-SYSTEM-080_sprint-closeout.md`.
- Commit and push exact paths.

---

## 7. Definition of Done

- Plan, task outcomes, hostile review, and sprint closeout are committed and pushed.
- `python/blk_tactical_profile_registry.py` provides deterministic registry/selection fixtures and fail-closed validators.
- `docs/BLK-080_tactical-standard-profile-registry-and-layer-b-extraction.md` exists and states the L0/L1 no-runtime boundary.
- BLK-058 is registered only as the first `kuronode-typescript` Layer C source.
- BLK-078 Layer B principles are extracted into stable IDs without hardcoding Kuronode-specific overlays as universal core.
- BLK-077 and BLK-079 point the default next sprint to BLK-SYSTEM-081 after BLK-SYSTEM-080 closes.
- Focused tests, full Python unittest discovery, Go tests, Go vet, markdown fence checks, and `git diff --check` pass.
- No forbidden runtime, target-repo, publication, RTM, protected-body, tooling, or production-isolation authority is granted or implied.
