# BLK-SYSTEM-082 — BLK-058 Mechanical Enforcement Upgrade Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `blk-system-authority-gated-sprints` while executing. This plan is guided by historical maturity vocabulary in `docs/BLK-024_blk-system-development-roadmap.md`, current roadmap selection in `docs/BLK-077_blk-system-post-078-roadmap.md`, current-state indexing in `docs/BLK-079_post-078-current-state-authority-index.md`, target-repo governance in `docs/BLK-081_target-repo-execution-governance-pattern.md`, profile-registry doctrine in `docs/BLK-080_tactical-standard-profile-registry-and-layer-b-extraction.md`, BLK-058, BLK-078, and BLK-001 through BLK-006 as applicable.

**Goal:** Upgrade BLK-058 from target-profile doctrine/static lineage into a BLK-System-owned deterministic mechanical enforcement fixture for submitted Kuronode TypeScript snippets, without scanning or mutating any target repository.
**BLK-024 track:** Track A — Doctrine, alignment, and review gates; Track D — Validation command profile tightening / maturity L0 doctrine-only plus L1 deterministic local fixture/gate tests.
**Architecture:** BLK-SYSTEM-081 made target-repo execution governance explicit. BLK-SYSTEM-082 selects the lower-authority branch of the BLK-SYSTEM-082 decision point: improve BLK-058 mechanical enforcement inside BLK-System using BLK-078 Layer B and BLK-080 Layer C profile machinery. The BEO Publication Decision Package remains a separate alternative if V-model completion is prioritized later.
**Tech Stack:** Markdown doctrine, Python unittest fixture validators/evaluators, active doctrine gates, Go/Python verification.
**Authority boundary:** BLK-System documentation and deterministic local fixture/gate work only. No real target-repository scan, source mutation, Git mutation, staging, commit, push, reset, checkout, revert, cleanup, or autofix. No BEB dispatch or BEO closeout execution. No live Codex execution, BLK-pipe execution, production BLK-test MCP, BEO publication, RTM generation, protected BLK-req body access, package-manager/network/model/browser/cyber tooling, or production sandbox/host-isolation claim.

---

## 0. Current Known State

Captured: `2026-05-11T22:26:44+10:00`

```text
repo: /home/dad/BLK-System
branch: main
local HEAD: 933d400a1e9357aef6def5847ea4a2299c9e8cf9
remote main: 933d400a1e9357aef6def5847ea4a2299c9e8cf9
status: ## main...origin/main
last commit: 933d400 docs: close blk-system 081 target-repo governance
```

Discovery:

```text
existing BLK-082 doc: none
existing BLK-SYSTEM-082 plan/outcomes: none
current roadmap selector: docs/BLK-077_blk-system-post-078-roadmap.md
current authority index: docs/BLK-079_post-078-current-state-authority-index.md
target-repo governance doctrine: docs/BLK-081_target-repo-execution-governance-pattern.md
target-repo governance fixture: python/blk_target_repo_execution_governance.py
profile registry fixture: python/blk_tactical_profile_registry.py
BLK-058 tactical standard: docs/BLK-058_kuronode-typescript-power-of-ten-tactical-standard.md
```

---

## 1. Selection Rationale

BLK-077 and BLK-079 now point to BLK-SYSTEM-082 — BLK-058 Mechanical Enforcement Upgrade or BEO Publication Decision Package.

This plan selects the **BLK-058 Mechanical Enforcement Upgrade** branch because:

1. BLK-SYSTEM-081 just completed target-repo governance, so the next safest local improvement is to strengthen the mechanical gate that future target-repo work will consume.
2. No explicit BEO publication authority, signer/storage/ledger authority, or publication pilot approval was granted in the operator request.
3. A deterministic BLK-058 evaluator can improve future tactical-quality review without touching Kuronode, running TypeScript tooling, invoking BLK-pipe, starting BLK-test, publishing BEOs, or generating RTM.

The BEO Publication Decision Package remains an available future L0/L1 decision-package alternative if V-model completion becomes the operator priority.

---

## 2. Governing Alignment

| Document | Relevance | Preserved boundary |
| --- | --- | --- |
| BLK-001 | Defines V-model separation between planning, tactical implementation, BLK-pipe enforcement, BLK-test evidence, BEO publication, and trace closure. | Mechanical enforcement is review evidence only; it does not become execution, target, publication, or trace authority. |
| BLK-002 | Defines staged requirements/use-case intake and protected-vault isolation. | The fixture evaluates caller-supplied snippets/records only and must not read protected BLK-req bodies or target files. |
| BLK-003 | Defines orchestration, human dispatch gates, BLK-pipe invocation, hostile audit, BLK-test evidence, and BEO handoff. | This sprint creates no BEB/BEO artifacts and performs no orchestration run. |
| BLK-004 | Defines BLK-pipe validation-profile and mutation boundaries. | Mechanical profiles remain repository-owned metadata and not shell commands; BLK-pipe remains the final mutation authority in future approved work. |
| BLK-005 | Defines trace binding and canonical hashes. | Fixture evidence is local quality evidence only; no RTM, coverage, drift rejection, or active-vault comparison is produced. |
| BLK-006 | Defines protected-vault hard-deny and Discord/HITL authorization. | The fixture does not grant target, protected-body, or runtime authority and captures no live approval. |
| BLK-058 | Defines the Kuronode TypeScript Power-of-Ten tactical standard. | BLK-082 converts selected BLK-058 constraints into deterministic local gates for submitted snippets only. |
| BLK-078 | Defines Layer A/B/C tactical-standard profile architecture. | BLK-082 consumes Layer B universal safety and Layer C `kuronode-typescript` constraints without weakening Layer A. |
| BLK-080 | Defines profile registry and Layer B extraction. | BLK-082 must consume profile IDs/profile names as metadata and preserve review-only profile-selection status. |
| BLK-081 | Defines target-repo execution governance. | BLK-082 must remain inside BLK-System fixture scope and must not start a target frontier. |

---

## 3. Exact Scope and File Allowlist

### Planning, outcomes, and review docs

```text
docs/plans/blk-system-082_blk058-mechanical-enforcement-upgrade.md
docs/outcomes/BLK-SYSTEM-082_task-000-outcome.md
docs/outcomes/BLK-SYSTEM-082_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-082_task-002-outcome.md
docs/outcomes/BLK-SYSTEM-082_task-003-outcome.md
docs/reviews/BLK-SYSTEM-082_hostile-review.md
docs/outcomes/BLK-SYSTEM-082_sprint-closeout.md
```

### Doctrine docs

```text
docs/BLK-077_blk-system-post-078-roadmap.md
docs/BLK-079_post-078-current-state-authority-index.md
docs/BLK-082_blk058-mechanical-enforcement-upgrade.md
```

### Deterministic local fixtures/gates

```text
python/blk_058_mechanical_enforcement.py
python/test_blk_058_mechanical_enforcement.py
python/blk_current_state_authority_index.py
python/test_blk_current_state_authority_index.py
python/test_active_doctrine_review_gates.py
```

No target repository path is in scope. The fixture may evaluate hardcoded test snippets or caller-supplied strings only; it must not walk, read, stat, parse, or execute real target files.

---

## 4. Explicitly Forbidden

This sprint does not authorize:

- target-repository scans, TypeScript tooling over real target files, package-manager execution, or semantic target analysis;
- target-repository source or Git mutation, staging, commit, push, reset, checkout, revert, stash, cleanup, or autofix;
- BEB writing, BEB dispatch, BEO writing, BEO publication, BEO closeout execution, or BEO-as-success claims;
- live Codex execution or tactical worker subprocesses;
- BLK-pipe execution, BLK-test execution, production BLK-test MCP startup, or evidence refresh;
- runtime RTM generation, RTM drift rejection, active-vault hash comparison, coverage matrix production, or public ledger mutation;
- protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation;
- network, model-service, browser, cyber, package-manager, signer, immutable storage, or release tooling;
- production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claims.

---

## 5. Required Mechanical Enforcement Contract

The deterministic fixture must define and validate:

1. a `kuronode-typescript` BLK-058 mechanical profile bound to BLK-058, BLK-078, BLK-080, and BLK-081;
2. a stable mechanical rule set for submitted TypeScript snippets, including bounded iteration, recursion rejection, explicit lifecycle cleanup, small reviewable units, boundary validation, checked results, minimal mutable scope, dynamic execution rejection, flat validated data access, zero-warning profile names, and no authority laundering;
3. exact denied-authority set equality and false side-effect flags;
4. repository-owned validation profile metadata only, never command strings;
5. deterministic evaluation statuses such as `BLK_058_MECHANICAL_ENFORCEMENT_PASS_FIXTURE_ONLY` and `BLK_058_MECHANICAL_ENFORCEMENT_BLOCKED_FIXTURE_ONLY`;
6. recursive rejection of BEO publication, RTM generation, protected-body, target scan/mutation, shell/tooling, live Codex, BLK-pipe, BLK-test, and production-sandbox claims inside submitted snippets/metadata.

The evaluator may be conservative. False positives are acceptable for this L1 fixture if they fail closed and are documented. False negatives for denied authority or live tooling are blockers.

---

## 6. Task Plan

### Task 000 — Plan publication

**Objective:** Publish this sprint plan and task-000 outcome with exact-path staging.

**Files:**

```text
docs/plans/blk-system-082_blk058-mechanical-enforcement-upgrade.md
docs/outcomes/BLK-SYSTEM-082_task-000-outcome.md
```

**Verification:**

```bash
git diff --check -- docs/plans/blk-system-082_blk058-mechanical-enforcement-upgrade.md docs/outcomes/BLK-SYSTEM-082_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
for name in [
    'docs/plans/blk-system-082_blk058-mechanical-enforcement-upgrade.md',
    'docs/outcomes/BLK-SYSTEM-082_task-000-outcome.md',
]:
    text = Path(name).read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, name
PY
git status --short --branch
```

**Commit:** `docs: plan blk-system 082 mechanical enforcement`

### Task 001 — RED/GREEN BLK-058 mechanical enforcement fixture

**Objective:** Add deterministic fixture code and tests for submitted-snippet BLK-058 mechanical enforcement.

**Files:**

```text
python/blk_058_mechanical_enforcement.py
python/test_blk_058_mechanical_enforcement.py
docs/outcomes/BLK-SYSTEM-082_task-001-outcome.md
```

**RED:** Add tests first proving the fixture is missing and must enforce mechanical profile identity, rule IDs, clean snippet PASS, recursion/unbounded loop/dynamic execution FAIL, command-shaped validation-profile FAIL, authority-laundering FAIL, exact denied-authority equality, false side-effect flags, and no live-surface imports/calls.

**GREEN:** Implement the smallest pure-Python, no-file-read, no-live-surface fixture/evaluator needed for the tests to pass.

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python3 python/test_blk_058_mechanical_enforcement.py -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python3 -m unittest discover python 'test_*.py'
export PATH="$HOME/.local/bin:$PATH" && go test ./...
git diff --check -- python/blk_058_mechanical_enforcement.py python/test_blk_058_mechanical_enforcement.py docs/outcomes/BLK-SYSTEM-082_task-001-outcome.md
```

**Commit:** `feat: add blk 058 mechanical enforcement fixture`

### Task 002 — BLK-082 doctrine and active doctrine gate

**Objective:** Publish BLK-082 as the BLK-058 mechanical enforcement upgrade doctrine and pin it with active doctrine gates.

**Files:**

```text
docs/BLK-082_blk058-mechanical-enforcement-upgrade.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-082_task-002-outcome.md
```

**RED:** Add an active doctrine gate that fails until BLK-082 contains exact markers for BLK-058 mechanical enforcement, fixture-only scope, submitted-snippet evaluation, denied authorities, no target scan/mutation, no BEB/BEO/publication/RTM/protected-body/tooling authority, and no production-isolation claim.

**GREEN:** Write the doctrine document with the minimum markers and alignment required by the gate.

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python3 -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_blk082_blk058_mechanical_enforcement_boundary -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python3 -m unittest discover python 'test_*.py'
export PATH="$HOME/.local/bin:$PATH" && go test ./...
git diff --check -- docs/BLK-082_blk058-mechanical-enforcement-upgrade.md python/test_active_doctrine_review_gates.py docs/outcomes/BLK-SYSTEM-082_task-002-outcome.md
```

**Commit:** `docs: add blk 082 mechanical enforcement doctrine`

### Task 003 — Roadmap/current-state alignment after BLK-SYSTEM-082

**Objective:** Update BLK-077, BLK-079, and current-state fixtures so BLK-SYSTEM-082 is complete and future work requires explicit operator frontier selection.

**Files:**

```text
docs/BLK-077_blk-system-post-078-roadmap.md
docs/BLK-079_post-078-current-state-authority-index.md
python/blk_current_state_authority_index.py
python/test_blk_current_state_authority_index.py
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-082_task-003-outcome.md
```

**RED:** Add tests that fail until the current docs/fixture surface include BLK-082 completion markers, remove active BLK-SYSTEM-082-as-next guidance, and require explicit operator decision before any higher-authority frontier.

**GREEN:** Update docs and fixtures minimally.

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python3 -m unittest python.test_blk_current_state_authority_index -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python3 -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint082_completion_requires_explicit_frontier_decision -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python3 -m unittest discover python 'test_*.py'
export PATH="$HOME/.local/bin:$PATH" && go test ./...
git diff --check -- docs/BLK-077_blk-system-post-078-roadmap.md docs/BLK-079_post-078-current-state-authority-index.md python/blk_current_state_authority_index.py python/test_blk_current_state_authority_index.py python/test_active_doctrine_review_gates.py docs/outcomes/BLK-SYSTEM-082_task-003-outcome.md
```

**Commit:** `docs: align roadmap after blk-system 082`

### Task 004 — Hostile review and sprint closeout

**Objective:** Hostile-review the completed sprint and publish the closeout.

**Files:**

```text
docs/reviews/BLK-SYSTEM-082_hostile-review.md
docs/outcomes/BLK-SYSTEM-082_sprint-closeout.md
```

**Review focus:** target-snippet fixture becoming live scan; validation-profile-as-shell; BLK-058-as-Kuronode-mutation; mechanical PASS as target approval; mechanical PASS as BEO publication, BEO closeout, RTM, coverage, or drift truth; protected-body/path smuggling; command/tooling/network strings; production sandbox claims; stale roadmap guidance.

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python3 -m unittest discover python 'test_*.py'
export PATH="$HOME/.local/bin:$PATH" && go test ./...
git diff --check
git status --short --branch
```

**Commit:** `docs: close blk-system 082 mechanical enforcement`

---

## 7. Stop Conditions

Stop and require explicit human decision if implementation attempts to:

- touch any target repository;
- run TypeScript, package-manager, browser, model-service, cyber, or network tooling;
- start Codex or another tactical executor;
- dispatch BEBs, create/close BEOs, publish BEOs, generate RTM, or claim coverage/drift truth;
- invoke BLK-pipe or BLK-test;
- read protected BLK-req bodies;
- treat BLK-058, BLK-078, BLK-080, BLK-081, BLK-082, or a mechanical PASS as runtime authority.
