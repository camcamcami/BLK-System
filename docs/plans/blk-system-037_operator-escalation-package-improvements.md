# BLK-SYSTEM-037 — Operator Escalation Package Improvements Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, `systematic-debugging`, and `code-review` when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable.

**Goal:** Improve Track I operator escalation packages so existing advisory health-check evidence can be compressed into decision-ready, token-bounded escalation context without granting production health-check, BLK-test, BEO, RTM, drift, Git mutation, protected-vault, or sandbox authority.
**BLK-024 track:** Track I — Operator UX, observability, and escalation; supporting Track J safety vocabulary. Maturity level: L4 local pilot evidence packaging for existing fixed-profile health-check results only; not L5 production authority.
**Architecture:** BLK-SYSTEM-037 adds a package boundary and deterministic local helper that consumes already-returned health-check result dictionaries. It does not start subprocesses, add health-check profiles, run BLK-pipe, dispatch BLK-test, publish BEOs, generate RTMs, read protected bodies, mutate source, or make drift decisions. Existing `blk_operator_health_check_runner` remains the only local pilot runner for fixed profiles; this sprint only summarizes its advisory outputs.
**Tech Stack:** Python `unittest`, Markdown doctrine/outcome/review docs, existing BLK-System Go verification.
**Authority boundary:** Advisory escalation packaging only. This plan does not authorize production BLK-test MCP, live tactical LLM execution, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads, authoritative BEO publication, RTM generation, RTM drift rejection authority, Git/source mutation, new health-check profile IDs, production health-check service/daemon behavior, network/model/cyber/package tooling, production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux claims, network firewall claims, or host-secret isolation claims.

---

## 0. Current Known State

Captured during planning:

```text
Date: 2026-05-09T07:06:36+10:00
Branch: main...origin/main
HEAD: b012bb0 docs: close blk-system sprint 036 git metadata fixture
Go: go version go1.26.2 linux/amd64
Working tree: clean at preflight
```

Recent governing closeout: `docs/outcomes/BLK-SYSTEM-036_sprint-closeout.md` lists operator escalation package improvements as the safe next Track I candidate while preserving advisory-only health-check evidence.

No existing `docs/BLK-039*`, `docs/plans/blk-system-037*`, `docs/outcomes/BLK-SYSTEM-037*`, or `docs/reviews/BLK-SYSTEM-037*` path was tracked at plan creation.

---

## 1. BLK-024-First Scope

BLK-024 Track I requires:

1. concise status reports;
2. escalation packages that preserve raw evidence without token-flooding Discord or Hermes context;
3. obvious failure ceilings and human decisions;
4. health checks for local tools and fixtures;
5. runbooks that identify policy blocks, broken code, failed verification, missing approval, dirty state, and disabled future authority.

BLK-SYSTEM-032 through BLK-SYSTEM-036 created the fixed-profile advisory health-check runner, profile expansion, side-effect observation, isolated workspace execution, and safe Git metadata fixture. BLK-SYSTEM-037 must not redo those profiles or expand runner authority. Its job is to package their advisory outputs into operator-facing escalation bundles.

---

## 2. BLK-001 through BLK-006 Alignment Matrix

| Doc | Governing obligation for BLK-SYSTEM-037 |
| --- | --- |
| BLK-001 | Preserve V-model domain separation. Escalation packages report state; they do not merge BLK-req, Hermes planning, BLK-pipe, BLK-test, BEO, or blk-link authority. |
| BLK-002 | Protected BLK-req body access remains outside scope. Packages may reference supplied IDs/hashes only; no vault reads or staging/promotion operations. |
| BLK-003 | Escalation explains failure ceilings and needed human decisions. It does not dispatch retries, tactical agents, BLK-test, BEO publication, or RTM generation. |
| BLK-004 | BLK-pipe remains deterministic enforcement authority. Python escalation packaging is advisory context and cannot mutate Git or validate source. |
| BLK-005 | Trace binding remains opaque `version_hash` metadata only. No active-vault comparison or artifact-body parsing. |
| BLK-006 | Protected BLK-req vault hard-deny and body-read prohibition remain active. Package helper must reject protected-body/path laundering. |

---

## 3. Deliverables

### 3.1 Doctrine / boundary

- Add `docs/BLK-039_track-i-health-check-escalation-package-boundary.md`.
- Add or update persistent active-doctrine gates so BLK-039 markers remain checked.

### 3.2 Implementation / tests

- Extend `python/blk_operator_observability_fixtures.py` with a health-check escalation package builder that consumes already-returned `run_health_check(...)` result dictionaries.
- Extend `python/test_blk_operator_observability_fixtures.py` with RED/GREEN tests for the new helper.
- Update `python/test_active_doctrine_review_gates.py` to include BLK-039 boundary markers.

### 3.3 Reviews / outcomes

- Create per-task outcome docs under `docs/outcomes/`.
- Create `docs/reviews/BLK-SYSTEM-037_operator-escalation-package-hostile-review.md`.
- Create final `docs/outcomes/BLK-SYSTEM-037_sprint-closeout.md`.

---

## 4. Required Package Contract

The new helper must produce a deterministic package with status `HEALTH_CHECK_ESCALATION_PACKAGE_ADVISORY_ONLY` and authority `HEALTH_CHECK_PASS_GRANTS_NO_AUTHORITY`.

It must preserve, at minimum:

- package ID;
- profile IDs;
- advisory statuses (`PASS_ADVISORY_ONLY`, `FAIL_ADVISORY_ONLY`, `BLOCKED_ADVISORY_ONLY`);
- exit codes;
- evidence hashes;
- bounded stdout/stderr excerpts only;
- failure categories that distinguish passed, failed verification/broken code, blocked/policy-environment, and unknown/malformed evidence;
- human decision requirement when any result is not advisory PASS;
- next operator actions that do not approve retry or authority expansion;
- source workspace labels and advisory execution scope where supplied;
- raw evidence embedded: false;
- production authority granted: false;
- health-check PASS grants authority: false;
- no new subprocess-starting behavior inside the package helper.

It must reject:

- unknown profile IDs;
- unsupported top-level fields;
- missing or malformed `sha256:<64 lowercase hex>` evidence hashes;
- package-level raw output embedding;
- oversized excerpts and package totals;
- `health_check_pass_grants_authority: true` or `production_authority_granted: true`;
- package-manager/network/BEO/RTM/drift/protected-body active claims other than explicit non-claims already emitted by the runner;
- forbidden authority-laundering keys such as runtime RTM, publication, signer, ledger, active-vault path, protected body/path, shell, command line, secret/token/private key, clone/worktree/setup, Git mutation, sandbox/cgroup/VM/firewall/host-secret enforcement claims.

The helper must not call `subprocess`, `os.system`, `eval`, `exec`, network clients, package managers, Git, BLK-pipe, BLK-test, BEO, or RTM tooling. It is a pure dictionary normalizer.

---

## 5. Task Plan

### Task 0 — Plan publication

**Objective:** Save this plan and task-000 outcome, validate Markdown, commit, and push.

**Files:**

- `docs/plans/blk-system-037_operator-escalation-package-improvements.md`
- `docs/outcomes/BLK-SYSTEM-037_task-000-outcome.md`

**Verification:**

```bash
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('docs/plans/blk-system-037_operator-escalation-package-improvements.md'),
    Path('docs/outcomes/BLK-SYSTEM-037_task-000-outcome.md'),
]
fence = chr(96) * 3
for path in paths:
    text = path.read_text()
    assert text.count(fence) % 2 == 0, path
    for i, line in enumerate(text.splitlines(), 1):
        assert line.rstrip() == line, f'{path}:{i}: trailing whitespace'
PY
git diff --check -- docs/plans/blk-system-037_operator-escalation-package-improvements.md docs/outcomes/BLK-SYSTEM-037_task-000-outcome.md
```

**Commit:** `docs: plan blk-system sprint 037 operator escalation packages`

---

### Task 1 — BLK-039 boundary and doctrine gate

**Objective:** Define the health-check escalation package boundary and pin it in active-doctrine tests.

**Files:**

- `docs/BLK-039_track-i-health-check-escalation-package-boundary.md`
- `python/test_active_doctrine_review_gates.py`
- `docs/outcomes/BLK-SYSTEM-037_task-001-outcome.md`

**TDD RED:** Add a doctrine gate requiring BLK-039 markers and run it before creating BLK-039.

**GREEN:** Create BLK-039 with explicit package contract, preserved non-authorities, rejection surface, and stop conditions.

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check -- docs/BLK-039_track-i-health-check-escalation-package-boundary.md python/test_active_doctrine_review_gates.py docs/outcomes/BLK-SYSTEM-037_task-001-outcome.md
```

**Commit:** `docs: define blk039 health-check escalation package boundary`

---

### Task 2 — Deterministic health-check escalation package builder

**Objective:** Implement the pure escalation package builder and hostile input gates.

**Files:**

- `python/blk_operator_observability_fixtures.py`
- `python/test_blk_operator_observability_fixtures.py`
- `docs/outcomes/BLK-SYSTEM-037_task-002-outcome.md`

**TDD RED:** Add focused tests proving the new builder is missing and that forbidden authority/oversized/raw-output cases must be rejected.

**GREEN:** Implement minimal pure dictionary normalization. Do not add runner profiles or subprocess execution.

**Required focused tests:**

- builds a package from PASS/FAIL/BLOCKED existing health-check result dictionaries;
- classifies PASS as `ADVISORY_PASS`, FAIL as `FAILED_VERIFICATION_OR_BROKEN_CODE`, BLOCKED as `POLICY_OR_ENVIRONMENT_BLOCKED`;
- keeps `raw_evidence_embedded` false and bounded excerpts only;
- sets `human_decision_required` true for FAIL/BLOCKED and false only for all PASS;
- rejects malformed hashes, unknown profile IDs, unsupported fields, raw-output fields, oversize excerpts, production authority, pass-grants-authority, RTM/BEO/drift/protected-body/sandbox/secret laundering;
- persistent BLK-039 doc marker test passes.

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_observability_fixtures
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check -- python/blk_operator_observability_fixtures.py python/test_blk_operator_observability_fixtures.py docs/outcomes/BLK-SYSTEM-037_task-002-outcome.md
```

**Commit:** `feat: add health-check escalation package builder`

---

### Task 3 — Hostile review and sprint closeout

**Objective:** Review the sprint for authority laundering, token-flood risk, and scope creep; close the sprint.

**Files:**

- `docs/reviews/BLK-SYSTEM-037_operator-escalation-package-hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-037_sprint-closeout.md`

**Review gates:**

- BLK-039 boundary matches implementation and tests;
- no new health-check profile IDs;
- no new subprocess, Git, network, package-manager, BLK-pipe, BLK-test, BEO, or RTM execution inside the package helper;
- raw outputs are not embedded;
- PASS remains advisory only;
- production sandbox/firewall/host-secret isolation is not claimed;
- protected-body/path and authority-laundering fields fail closed.

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_observability_fixtures
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('docs/reviews/BLK-SYSTEM-037_operator-escalation-package-hostile-review.md'),
    Path('docs/outcomes/BLK-SYSTEM-037_sprint-closeout.md'),
]
fence = chr(96) * 3
for path in paths:
    text = path.read_text()
    assert text.count(fence) % 2 == 0, path
    for i, line in enumerate(text.splitlines(), 1):
        assert line.rstrip() == line, f'{path}:{i}: trailing whitespace'
PY
git diff --check -- docs/reviews/BLK-SYSTEM-037_operator-escalation-package-hostile-review.md docs/outcomes/BLK-SYSTEM-037_sprint-closeout.md
git status --short --branch
git log --oneline --decorate -8
```

**Commit:** `docs: close blk-system sprint 037 operator escalation packages`

---

## 6. Non-Goals

BLK-SYSTEM-037 must not:

- create production health-check authority;
- add or alter health-check runner profiles;
- run new live smoke tests beyond existing local fixed-profile unit/full-suite verification;
- claim OS-level sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, network firewall, or host-secret isolation enforcement;
- read, copy, parse, hash, summarize, or scan protected BLK-req body/path contents;
- mutate Git/source, repair workspaces, stage, commit, push, reset, clean, checkout, stash, merge, rebase, switch, restore, clone, or create worktrees inside the helper;
- dispatch BLK-pipe, BLK-test, tactical LLMs, Codex, BEO publication, RTM generation, or drift rejection;
- accept arbitrary caller command/argv/shell data;
- embed raw unbounded logs in Discord/Hermes context.

---

## 7. Quick Resume Prompt

Resume BLK-SYSTEM-037 from `docs/plans/blk-system-037_operator-escalation-package-improvements.md`. Preserve Track I advisory-only scope. Implement tasks in order with exact-path staging, per-task outcome docs, RED/GREEN tests, hostile review, `git diff --check`, full Python unittest discovery, `go test ./...`, `go vet ./...`, and push each completed commit to `origin/main`.
