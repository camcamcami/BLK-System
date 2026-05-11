# BLK-SYSTEM-081 — Target-Repo Execution Governance Pattern Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `blk-system-authority-gated-sprints` while executing. This plan is guided by historical maturity vocabulary in `docs/BLK-024_blk-system-development-roadmap.md`, current roadmap selection in `docs/BLK-077_blk-system-post-078-roadmap.md`, current-state indexing in `docs/BLK-079_post-078-current-state-authority-index.md`, tactical-standard profile architecture in `docs/BLK-078_tactical-standard-profile-architecture.md`, profile-registry doctrine in `docs/BLK-080_tactical-standard-profile-registry-and-layer-b-extraction.md`, and BLK-001 through BLK-006 as applicable.

**Goal:** Formalize a BLK-System-owned target-repository execution governance pattern that future exact-target work must consume before any target scan, mutation, BEB dispatch, BEO closeout execution, publication, or RTM authority can be requested.
**BLK-024 track:** Track A — Doctrine, alignment, and review gates; Track C — BLK-pipe blast shield and forge; Track D — Validation command profile tightening / maturity L0 doctrine-only plus L1 deterministic local fixture/gate tests.
**Architecture:** BLK-SYSTEM-080 created profile-selection records and Layer B/Layer C tactical-profile machinery. BLK-SYSTEM-081 uses that machinery to define a reusable target-repo execution chain: request package, profile selection, approval envelope, preflight refusal, approval capture, BLK-pipe invocation boundary, validation evidence, hostile audit, and target-repo closeout. The pattern records what future work must prove; it does not perform target work.
**Tech Stack:** Markdown doctrine, Python unittest fixture validators, active doctrine gates, Go/Python verification.
**Authority boundary:** BLK-System documentation and deterministic local fixture/gate work only. No target-repository scan, source mutation, Git mutation, staging, commit, push, reset, checkout, revert, cleanup, or autofix. No BEB dispatch or BEO closeout execution. No live Codex execution, BLK-pipe execution, production BLK-test MCP, BEO publication, RTM generation, protected BLK-req body access, package-manager/network/model/browser/cyber tooling, or production sandbox/host-isolation claim.

---

## 0. Current Known State

Captured: `2026-05-11T21:20:44+10:00`

```text
repo: /home/dad/BLK-System
branch: main
local HEAD: 78fcc433da76af97261c0471111c62a3bf654926
remote main: 78fcc433da76af97261c0471111c62a3bf654926
status: ## main...origin/main
last commit: 78fcc43 docs: normalize active BLK terminology to BEB/BEO
```

Discovery:

```text
existing BLK-081 doc: none
existing BLK-SYSTEM-081 plan/outcomes: none
current roadmap selector: docs/BLK-077_blk-system-post-078-roadmap.md
current authority index: docs/BLK-079_post-078-current-state-authority-index.md
profile architecture anchor: docs/BLK-078_tactical-standard-profile-architecture.md
profile registry fixture: python/blk_tactical_profile_registry.py
first Layer C source: docs/BLK-058_kuronode-typescript-power-of-ten-tactical-standard.md
```

---

## 1. Selection Rationale

BLK-077 and BLK-079 select BLK-SYSTEM-081 as the default next sprint after BLK-SYSTEM-080.

BLK-SYSTEM-080 finished the tactical profile registry and Layer B extraction, but future external target-repository work still needs a BLK-System governance pattern that makes the target identity, approval envelope, profile-selection record, validation profile, replay policy, expiry, stop conditions, and closeout obligations explicit before any runtime frontier is requested.

BLK-SYSTEM-081 is that L0/L1 governance sprint. It generalizes lessons from the post-078 exact-target chain into reusable BLK-System doctrine and deterministic fixture validation, while preserving that no target work occurs during this sprint.

---

## 2. Governing Alignment

| Document | Relevance | Preserved boundary |
| --- | --- | --- |
| BLK-001 | Defines V-model separation between architectural intent, tactical execution, deterministic enforcement, BLK-test evidence, BEO publication, and trace closure. | Target-repo governance records constrain future authority requests; they do not become execution, evidence, publication, or trace authority. |
| BLK-002 | Defines staging, linting, HITL approval, canonical hashing, active-vault immutability, and protected-vault isolation. | Governance records must not read/copy/parse/hash/summarize/scan/mutate protected BLK-req bodies and must bind only opaque trace identifiers/hashes. |
| BLK-003 | Defines orchestration, human dispatch gates, Layer 2 packets, BLK-pipe invocation, hostile audit, BLK-test evidence, and BEO handoff. | This sprint names the future stages but does not create BEBs, dispatch them, run BLK-pipe, run BLK-test, write BEOs, or close BEOs. |
| BLK-004 | Defines BLK-pipe as deterministic final mutation enforcement with exact allowlists, validation profile resolution, output caps, cleanup, Git routing, target-hash checks, and reports. | Future governance must require exact allowlists and validation profiles, but this sprint does not invoke BLK-pipe or mutate targets. |
| BLK-005 | Defines requirement/use-case trace binding and canonical version hashes. | Governance records may require trace artifact descriptors and hashes, but no RTM, coverage matrix, drift rejection, or protected-body comparison is authorized. |
| BLK-006 | Defines protected-vault hard-deny and Discord/HITL authorization boundaries. | Approval IDs and operator identities are future evidence fields only; they do not imply protected-body access or target mutation. |
| BLK-058 | Defines the Kuronode TypeScript Layer C tactical profile source. | BLK-058 remains a constraint input for future approved Kuronode TypeScript work only, not a dispatch or mutation grant. |
| BLK-078 | Defines Layer A universal core, Layer B universal tactical-output safety, and Layer C target tactical profiles. | Target-repo governance must preserve Layer A and consume profile-selection records without letting Layer B/Layer C grant runtime authority. |
| BLK-079 | Current-state index selecting BLK-SYSTEM-081. | After this sprint, BLK-079 should point the default next sprint to BLK-SYSTEM-082 selection guidance. |
| BLK-080 | Profile registry and Layer B extraction. | Target-repo governance consumes `python/blk_tactical_profile_registry.py` records and preserves their review-only/non-runtime boundary. |

---

## 3. Exact Scope and File Allowlist

### Planning, outcomes, and review docs

```text
docs/plans/blk-system-081_target-repo-execution-governance-pattern.md
docs/outcomes/BLK-SYSTEM-081_task-000-outcome.md
docs/outcomes/BLK-SYSTEM-081_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-081_task-002-outcome.md
docs/outcomes/BLK-SYSTEM-081_task-003-outcome.md
docs/reviews/BLK-SYSTEM-081_hostile-review.md
docs/outcomes/BLK-SYSTEM-081_sprint-closeout.md
```

### Doctrine docs

```text
docs/BLK-077_blk-system-post-078-roadmap.md
docs/BLK-079_post-078-current-state-authority-index.md
docs/BLK-081_target-repo-execution-governance-pattern.md
```

### Deterministic local fixtures/gates

```text
python/blk_target_repo_execution_governance.py
python/test_blk_target_repo_execution_governance.py
python/blk_current_state_authority_index.py
python/test_blk_current_state_authority_index.py
python/test_active_doctrine_review_gates.py
```

No target repository path is in scope. `/home/dad/code/Kuronode-v1`, `/home/dad/Kuronode-v1`, and any other target checkout are out of scope except as literal documentation examples that do not run.

---

## 4. Explicitly Forbidden

This sprint does not authorize:

- target-repository scans, static analysis over real target files, package-manager execution, or TypeScript tooling;
- target-repository source or Git mutation, staging, commit, push, reset, checkout, revert, stash, cleanup, or autofix;
- BEB writing, BEB dispatch, BEO writing, BEO publication, BEO closeout execution, or BEO-as-success claims;
- live Codex execution or tactical worker subprocesses;
- BLK-pipe execution, BLK-test execution, production BLK-test MCP startup, or evidence refresh;
- runtime RTM generation, RTM drift rejection, active-vault hash comparison, coverage matrix production, or public ledger mutation;
- protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation;
- network, model-service, browser, cyber, package-manager, signer, immutable storage, or release tooling;
- production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claims.

---

## 5. Required Governance Contract

The deterministic fixture must define and validate a target-repo governance record with these stages:

1. `request_package` — future operator/repository intent, not approval.
2. `profile_selection` — BLK-080 profile-selection record, review-only until separately approved.
3. `approval_envelope` — exact target identity, operator approval ID, run ID, expiry, replay policy, and denied-authority preservation.
4. `preflight_refusal` — fail-closed blocker state when approval or exact target evidence is absent, stale, expired, replayed, or mismatched.
5. `approval_capture` — future capture boundary, not retargeting authority.
6. `blk_pipe_invocation_boundary` — future exact BLK-pipe payload boundary, no invocation in this sprint.
7. `validation_evidence` — repository-owned validation profile names and bounded evidence descriptors only.
8. `hostile_audit` — mandatory review for authority laundering, exact target drift, replay/expiry, side effects, and profile weakening.
9. `target_repo_closeout` — target-repo outcome/BEO closeout obligations only when separately authorized.

The record must require:

- exact target repository ID, absolute path string, branch, target HEAD SHA, and remote HEAD SHA evidence fields;
- exact source allowlist and protected denylist strings;
- repository-owned validation profile names, not shell commands;
- BLK-080 profile-selection record identity for `kuronode-typescript` where BLK-058 applies;
- approval ID, run ID, request ID, expiry, replay policy, and stop conditions;
- exact denied-authority set equality and false side-effect flags;
- deterministic `READY_FOR_HUMAN_REVIEW_NOT_RUNTIME` versus `BLOCKED` evaluation states.

---

## 6. Task Plan

### Task 000 — Plan publication

**Objective:** Publish this sprint plan and task-000 outcome with exact-path staging.

**Files:**

```text
docs/plans/blk-system-081_target-repo-execution-governance-pattern.md
docs/outcomes/BLK-SYSTEM-081_task-000-outcome.md
```

**Verification:**

```bash
git diff --check -- docs/plans/blk-system-081_target-repo-execution-governance-pattern.md docs/outcomes/BLK-SYSTEM-081_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
for name in [
    'docs/plans/blk-system-081_target-repo-execution-governance-pattern.md',
    'docs/outcomes/BLK-SYSTEM-081_task-000-outcome.md',
]:
    text = Path(name).read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, name
PY
git status --short --branch
```

**Commit:** `docs: plan blk-system 081 target-repo governance`

### Task 001 — RED/GREEN target-repo governance fixture

**Objective:** Add deterministic fixture code and tests for the target-repo execution governance pattern.

**Files:**

```text
python/blk_target_repo_execution_governance.py
python/test_blk_target_repo_execution_governance.py
docs/outcomes/BLK-SYSTEM-081_task-001-outcome.md
```

**RED:** Add tests first proving the fixture is missing and must enforce exact stages, exact target identity, profile-selection binding, denied-authority equality, validation-profile metadata, replay/expiry/stop-condition fields, no live-surface calls, and fail-closed laundering rejection.

**GREEN:** Implement the smallest pure-Python, no-live-surface fixture/validator/evaluator needed for the tests to pass.

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_target_repo_execution_governance -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
export PATH="$HOME/.local/bin:$PATH" && go test ./...
git diff --check -- python/blk_target_repo_execution_governance.py python/test_blk_target_repo_execution_governance.py docs/outcomes/BLK-SYSTEM-081_task-001-outcome.md
```

**Commit:** `feat: add target-repo governance fixture`

### Task 002 — BLK-081 doctrine and active doctrine gate

**Objective:** Publish BLK-081 as the target-repo execution governance pattern doctrine and pin it with active doctrine gates.

**Files:**

```text
docs/BLK-081_target-repo-execution-governance-pattern.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-081_task-002-outcome.md
```

**RED:** Add an active doctrine gate that fails until BLK-081 contains exact markers for target identity, profile selection, approval envelope, preflight refusal, BLK-pipe boundary, validation evidence, hostile audit, closeout, denied authorities, and no target-repo/BEB/BEO/publication/RTM/protected-body/tooling authority.

**GREEN:** Write the doctrine document with the minimum markers and alignment required by the gate.

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGatesTest.test_blk081_target_repo_execution_governance_boundary -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
export PATH="$HOME/.local/bin:$PATH" && go test ./...
git diff --check -- docs/BLK-081_target-repo-execution-governance-pattern.md python/test_active_doctrine_review_gates.py docs/outcomes/BLK-SYSTEM-081_task-002-outcome.md
```

**Commit:** `docs: add blk 081 target-repo governance doctrine`

### Task 003 — Roadmap/current-state alignment after BLK-SYSTEM-081

**Objective:** Update BLK-077, BLK-079, and current-state fixtures so BLK-SYSTEM-081 is complete and BLK-SYSTEM-082 becomes the next decision point.

**Files:**

```text
docs/BLK-077_blk-system-post-078-roadmap.md
docs/BLK-079_post-078-current-state-authority-index.md
python/blk_current_state_authority_index.py
python/test_blk_current_state_authority_index.py
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-081_task-003-outcome.md
```

**RED:** Add tests that fail until the current docs/fixture surface include BLK-081 completion markers and BLK-SYSTEM-082 selection guidance while removing stale active BLK-SYSTEM-081 guidance.

**GREEN:** Update docs and fixtures minimally.

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_current_state_authority_index -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGatesTest.test_sprint081_completion_updates_current_roadmap_and_next_sprint_to_082 -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
export PATH="$HOME/.local/bin:$PATH" && go test ./...
git diff --check -- docs/BLK-077_blk-system-post-078-roadmap.md docs/BLK-079_post-078-current-state-authority-index.md python/blk_current_state_authority_index.py python/test_blk_current_state_authority_index.py python/test_active_doctrine_review_gates.py docs/outcomes/BLK-SYSTEM-081_task-003-outcome.md
```

**Commit:** `docs: align roadmap after blk-system 081`

### Task 004 — Hostile review and sprint closeout

**Objective:** Hostile-review the completed sprint and publish the closeout.

**Files:**

```text
docs/reviews/BLK-SYSTEM-081_hostile-review.md
docs/outcomes/BLK-SYSTEM-081_sprint-closeout.md
```

**Review focus:** authority laundering; stale target identity; profile-selection-as-approval; approval-ID-as-retargeting; validation-profile-as-shell; PASS-as-publication; BEB/BEO work smuggling; BEO publication and RTM drift authority smuggling; protected-body path/reference smuggling; target-work side effects; production sandbox claims.

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
export PATH="$HOME/.local/bin:$PATH" && go test ./...
git diff --check
git status --short --branch
```

**Commit:** `docs: close blk-system 081 target-repo governance`

---

## 7. Stop Conditions

Stop and require explicit human decision if implementation attempts to:

- touch any target repository;
- run TypeScript, package-manager, browser, model-service, cyber, or network tooling;
- start Codex or another tactical executor;
- dispatch BEBs, create/close BEOs, publish BEOs, generate RTM, or claim coverage/drift truth;
- invoke BLK-pipe or BLK-test;
- read protected BLK-req bodies;
- treat BLK-058, BLK-078, BLK-080, or BLK-081 as runtime authority.
