# BLK-SYSTEM-029 — Track I Live Health-Check Boundary Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, `systematic-debugging`, and adversarial review skills when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable.

**Goal:** Define and fixture a safe boundary for future live Track I health checks without yet authorizing command execution as a reusable runtime capability.
**BLK-024 track:** Track I — Operator UX, observability, and escalation / maturity level L1 fixture-only with L0 doctrine-boundary updates.
**Architecture:** BLK-SYSTEM-029 follows BLK-031 by moving from passive operator observability fixtures toward a reviewable health-check boundary. The sprint may define deterministic local health-check request/profile/result fixtures, explicit command allowlists, output/redaction rules, network-denial claims, path boundaries, and escalation vocabulary; it must not implement a live command runner or claim that live health checks have executed successfully.
**Tech Stack:** Markdown doctrine, Python `unittest` fixtures, and static source/doctrine gates.
**Authority boundary:** L1 fixture-only / L0 doctrine. No live health-check command execution, no arbitrary shell, no network/model-service/cyber-tooling, no protected BLK-req body reads, no active-vault filesystem scanning, no BLK-pipe source mutation, no production BLK-test MCP, no BEO publication, no RTM generation, no RTM drift rejection, no production sandbox/host-secret isolation claim, and no approval inheritance.

---

## 0. Current Known State

- **Date:** 2026-05-08T11:24:39+10:00
- **Branch state:** `## main...origin/main`
- **HEAD:** `92cd5b1 docs: close blk-system sprint 028 operator observability`
- **Latest completed sprint:** BLK-SYSTEM-028 created `OPERATOR_OBSERVABILITY_FIXTURE_ONLY` and `OPERATOR_ESCALATION_PACKAGE_FIXTURE_ONLY` local fixtures, hardened BLK-031, and explicitly left live health checks to a separate future sprint.
- **ID discovery:** `BLK-SYSTEM-029` has no existing plan/outcome collision. `BLK-032` is the next available root BLK boundary document ID after BLK-031.

---

## 1. Non-Execution and Non-Authority Boundary

This plan does not authorize Hindsight use, Codex use, live tactical LLM execution, network model services, cyber tooling, live health-check command execution, arbitrary shell, package-manager execution, Git mutation, source mutation, production BLK-test MCP, new live BLK-test smoke runs, active-vault filesystem scanning, protected BLK-req vault body reads/copying/parsing/hashing/mutation, runtime active-vault hash comparison, backend promotion, staged revision execution, authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, runtime RTM generation, runtime RTM IDs, RTM ledgers, runtime coverage matrices, RTM drift rejection authority, production sandbox/cgroup/VM/network/host-secret isolation claims, or source mutation outside exact approved allowlists.

This sprint may describe future health-check commands as inert profile metadata. It must not execute those commands through a product helper, spawn subprocesses, inspect host state, inspect filesystem paths, call `git`, call package managers, call network APIs, or report a health-check PASS from the fixture layer.

---

## 2. BLK-024 Selection Rationale

BLK-024 Track I explicitly calls for health checks for local binaries, Python tools, schemas, test fixtures, and disabled transport stubs. BLK-SYSTEM-028 closed the passive observability/runbook rung and left health checks as the next Track I candidate.

The safe next step is not a live runner. It is a boundary sprint that defines:

1. which checks may eventually exist;
2. which commands they would map to if later authorized;
3. which checks are advisory vs blocking;
4. how outputs would be bounded and redacted;
5. which path/network/credential/protected-vault surfaces remain denied;
6. how a later sprint must request actual execution authority.

---

## 3. BLK-001 Through BLK-006 Alignment Matrix

| Governing doc | Relevance to BLK-SYSTEM-029 | Preserved boundary |
| --- | --- | --- |
| BLK-001 — Master Architecture | Health status should explain whether BLK-req, Hermes planning, BLK-pipe, BLK-test, BEO, or blk-link is blocked. | Health checks do not merge domain authorities or become execution/publishing/RTM authority. |
| BLK-002 — Artifact Lifecycle | Future health checks may report whether lint/promotion scripts exist as toolchain readiness metadata. | No staging, promotion, revision, active-vault scanning, or protected-body access. |
| BLK-003 — Orchestration Protocol | Health status should support escalation by distinguishing disabled policy from missing tools or failed verification. | No BEB dispatch, BLK-pipe invocation, BLK-test startup, retry approval, or failure-ceiling reset. |
| BLK-004 — BLK-pipe V47 Suite | Health profiles may describe checks for Go build/test/vet availability and BLK-pipe validation profile readiness. | Go `blk-pipe` remains the enforcement authority; health fixtures are advisory and non-mutating. |
| BLK-005 — BLK-Req Specification | Health profiles may mention schema fixture readiness and canonical-hash shape validation. | No requirement/use-case body parsing, hashing, comparison, or drift decisions. |
| BLK-006 — BLK-Req Implementation Brief | Health boundary must preserve protected-vault hard-deny and HITL authorization boundaries. | No Discord/HITL approval capture, protected body reads, or backend promotion authority. |

---

## 4. Planned Artifacts

Task execution should create or modify exactly these primary artifacts unless hostile review requires an exact-scope remediation:

- `docs/BLK-032_track-i-live-health-check-boundary.md`
- `python/blk_operator_health_check_fixtures.py`
- `python/test_blk_operator_health_check_fixtures.py`
- `python/test_active_doctrine_review_gates.py`
- `docs/reviews/BLK-SYSTEM-029_health-check-boundary-inventory.md`
- `docs/reviews/BLK-SYSTEM-029_health-check-boundary-hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-029_task-000-outcome.md`
- `docs/outcomes/BLK-SYSTEM-029_task-001-outcome.md`
- `docs/outcomes/BLK-SYSTEM-029_task-002-outcome.md`
- `docs/outcomes/BLK-SYSTEM-029_task-003-outcome.md`
- `docs/outcomes/BLK-SYSTEM-029_sprint-closeout.md`

---

## 5. Planned Tasks

### Task 0 — Publish plan and task-000 outcome

**Deliverables:**

- `docs/plans/blk-system-029_track-i-live-health-check-boundary.md`
- `docs/outcomes/BLK-SYSTEM-029_task-000-outcome.md`

**Acceptance criteria:**

- Plan records live preflight facts.
- Plan states BLK-024 Track I / L1-L0 boundary.
- Plan explicitly does not authorize live health-check execution.
- Plan is committed and pushed with exact-path staging.

**Verification:**

```bash
git diff --check -- docs/plans/blk-system-029_track-i-live-health-check-boundary.md docs/outcomes/BLK-SYSTEM-029_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
for p in [
    Path('docs/plans/blk-system-029_track-i-live-health-check-boundary.md'),
    Path('docs/outcomes/BLK-SYSTEM-029_task-000-outcome.md'),
]:
    text = p.read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, p
PY
```

**Commit:** `docs: plan blk-system sprint 029 health-check boundary`

### Task 1 — Inventory future health-check surfaces and authority risks

**Deliverables:**

- `docs/reviews/BLK-SYSTEM-029_health-check-boundary-inventory.md`
- `docs/outcomes/BLK-SYSTEM-029_task-001-outcome.md`

**Acceptance criteria:**

- Inventory separates health-check categories from execution authority.
- Must cover at minimum:
  - local Go toolchain / `go test` / `go vet` readiness;
  - Python unittest readiness and `PYTHONPATH=python` convention;
  - schema/doctrine fixture readiness;
  - disabled BLK-test transport stub readiness;
  - BLK-pipe binary/profile readiness;
  - Git clean-state advisory readiness;
  - output-bound/redaction readiness;
  - network-denial and package-manager-denial readiness;
  - protected-vault no-read readiness;
  - RTM/BEO disabled-authority readiness.
- Must classify each candidate check as one of:
  - `ADVISORY_ONLY`;
  - `BLOCKING_IF_LATER_EXECUTION_AUTHORIZED`;
  - `FORBIDDEN_IN_HEALTH_CHECK`.
- Must list exact future command candidates as inert strings only and explain that Task 2 fixtures must not run them.

**Verification:**

```bash
git diff --check -- docs/reviews/BLK-SYSTEM-029_health-check-boundary-inventory.md docs/outcomes/BLK-SYSTEM-029_task-001-outcome.md
```

**Commit:** `docs: inventory blk health-check boundary surfaces`

### Task 2 — Implement health-check boundary fixtures and BLK-032 doctrine

**Deliverables:**

- `python/blk_operator_health_check_fixtures.py`
- `python/test_blk_operator_health_check_fixtures.py`
- `docs/BLK-032_track-i-live-health-check-boundary.md`
- update `python/test_active_doctrine_review_gates.py`
- `docs/outcomes/BLK-SYSTEM-029_task-002-outcome.md`

**Required fixture vocabulary:**

- `HEALTH_CHECK_BOUNDARY_FIXTURE_ONLY`
- `HEALTH_CHECK_PROFILE_FIXTURE_ONLY`
- `HEALTH_CHECK_RESULT_FIXTURE_ONLY`
- `HEALTH_CHECK_ESCALATION_FIXTURE_ONLY`
- `HEALTH_CHECKS_NOT_EXECUTED`
- `HEALTH_CHECK_AUTHORITY_NOT_GRANTED`

**Acceptance criteria:**

- Strict TDD: write failing tests first, observe RED, then implement minimal fixture code.
- Helper may normalize caller-supplied profile/result dictionaries only.
- Fixture output must include explicit false side-effect booleans:
  - `command_executed: false`
  - `subprocess_started: false`
  - `network_called: false`
  - `file_read: false`
  - `git_called: false`
  - `package_manager_called: false`
  - `source_mutated: false`
  - `approval_captured: false`
  - `protected_body_read: false`
  - `active_vault_scanned: false`
  - `beo_published: false`
  - `rtm_generated: false`
  - `drift_decision_made: false`
- Profiles must reject forbidden command categories:
  - shell strings not represented as fixed argv arrays;
  - network commands (`curl`, `wget`, `ssh`, `scp`, `nc`, browser/API clients);
  - package managers (`npm install`, `pip install`, `uv pip install`, `go get`, etc.);
  - Git mutation commands (`commit`, `push`, `reset`, `checkout`, `stash`, `clean`, `revert`, `merge`, `rebase`);
  - protected-vault/body/path scans;
  - RTM/BEO publication/drift authority fields.
- Profiles may allow inert candidate argv arrays for later human-reviewed health checks, such as:
  - `['go', 'test', './...']`
  - `['go', 'vet', './...']`
  - `['python3', '-m', 'unittest', 'discover', 'python', 'test_*.py']`
  - `['python3', '-m', 'unittest', 'python.test_active_doctrine_review_gates']`
  - `['git', 'status', '--short', '--branch']` as advisory read-only candidate only.
- Fixture code must not import or call live execution/network/file-scanning APIs (`subprocess`, `socket`, `requests`, `urllib`, `http.client`, `os.system`, `eval`, `exec`, `__import__`, `open`, `Path`, `read_text`, `glob`, `rglob`, Discord/GitHub APIs).
- BLK-032 must state that it is a boundary contract, not live health-check authority.
- `python/test_active_doctrine_review_gates.py` must pin BLK-032 markers and implementation live-surface denial.

**Focused verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_fixtures -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
```

**Commit:** `feat: add health-check boundary fixtures`

### Task 3 — Hostile review, remediation, full verification, and closeout

**Deliverables:**

- `docs/reviews/BLK-SYSTEM-029_health-check-boundary-hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-029_task-003-outcome.md`
- `docs/outcomes/BLK-SYSTEM-029_sprint-closeout.md`
- exact remediation changes required by hostile review, if any

**Hostile review must probe:**

- command execution sneaking in through fixture construction;
- fixed argv arrays being converted into shell strings;
- `git status` advisory checks becoming Git mutation authority;
- network/package-manager commands hidden under aliases or arguments;
- protected-vault path/body scans disguised as health checks;
- active-vault scanning or runtime hash comparison;
- output-bound bypass and token flooding;
- environment/secret leakage (`SSH_AUTH_SOCK`, `GITHUB_TOKEN`, API keys, `.env`);
- production sandbox/host-secret isolation claims;
- health-check PASS being treated as approval to execute, publish BEOs, generate RTM, or reject drift;
- marker-only doctrine gates that do not assert the actual boundary.

**Full verification:**

```bash
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover python 'test_*.py'
git diff --check
git status --short --branch
```

**Commit:** `docs: close blk-system sprint 029 health-check boundary`

---

## 6. Exact-Path Git Discipline

Every task must stage exact paths only. Do not use `git add .`, broad globs, stash, reset, or checkout to manage task files. After each task:

```bash
git add <exact task paths>
git diff --cached --name-only
git commit -m "<task message>"
git push origin main
git status --short --branch
git log -1 --oneline
git ls-remote origin refs/heads/main
```

Remove Python bytecode/cache artifacts before staging using a short Python cleanup or exact cache paths only.

---

## 7. Stop Conditions

Stop and escalate rather than broadening scope if any task appears to require:

- executing live health-check commands through a product helper;
- accepting arbitrary shell strings;
- reading raw filesystem paths or protected-vault bodies;
- scanning `docs/active/` or other active-vault paths;
- calling network services or package managers;
- mutating Git or source state;
- capturing approvals;
- treating health-check status as permission to dispatch BLK-pipe, start BLK-test, publish BEOs, generate RTM, or reject drift;
- claiming production sandbox, cgroup, VM, network, or host-secret isolation;
- storing secrets or raw environment values in fixtures or docs.

---

## 8. Future Authority Handoff

After BLK-SYSTEM-029 closes, a later sprint may request actual live health-check execution authority only if:

1. BLK-032 exists and passes doctrine gates;
2. health-check profiles are fixed argv arrays, not shell strings;
3. output bounds and redaction are mechanically tested;
4. network and package-manager denial are mechanically tested;
5. path boundaries and protected-vault no-read guarantees are mechanically tested;
6. Git checks are read-only and cannot mutate state;
7. health-check PASS remains advisory and does not imply execution, BLK-test, BEO, RTM, or drift authority.
