# BLK-SYSTEM-041 — Codex Live-Dispatch Authority Request Disabled Adapter Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `code-review` when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable.

**Goal:** Create a fail-closed Codex live-dispatch authority-request package and disabled adapter fixture that packages BLK-040/041/042 evidence for review while refusing to start Codex, BLK-pipe, Git, or source mutation.

**BLK-024 track:** Track A — Doctrine, alignment, and review gates; Track C — BLK-pipe blast shield and forge; Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening.

**Maturity level:** BLK-024 L2 disabled/fail-closed transport with L1 fixture evidence and L0 boundary doctrine. This is not L3 smoke, not L4 pilot runtime, and not L5 production authority.

**Architecture:** BLK-SYSTEM-038 created a deterministic Codex invocation profile. BLK-SYSTEM-039 wrapped it in a deterministic dispatch envelope. BLK-SYSTEM-040 added a readiness gate proving prerequisite evidence for review. BLK-SYSTEM-041 now packages that review evidence into an authority-request artifact and proves the live-dispatch adapter stays disabled/fail-closed unless a later separate sprint grants execution authority.

**Tech Stack:** Markdown doctrine, Python fixtures/tests, active doctrine gates.

**Authority boundary:** Disabled adapter and authority-request package only. No live Codex execution, no runtime dispatch, no subprocess start, no BLK-pipe invocation, no Git/source mutation, no worktree creation, no package-manager/network/model/cyber/browser tooling, no protected BLK-req vault body reads, no production BLK-test MCP, no BEO publication, no RTM generation, no drift rejection, and no production sandbox/cgroup/VM/firewall/host-secret-isolation claims.

---

## 0. Current Repository State at Planning

```text
Date: 2026-05-09T15:06:49+10:00
Branch: main...origin/main
HEAD: 69e07f8 docs: close blk-system sprint 040 codex live dispatch readiness gate
Existing highest system plan: docs/plans/blk-system-040_codex-live-dispatch-readiness-gate.md
Existing highest BLK boundary doc: docs/BLK-042_codex-live-dispatch-readiness-gate-boundary.md
```

Discovery found no existing `BLK-SYSTEM-041`, `blk-system-041`, or `BLK-043` owner in `docs/` or `python/`.

---

## 1. Why This Sprint Exists

BLK-SYSTEM-040 deliberately stopped at `READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION`. It proved that future live-dispatch prerequisite evidence can be validated, but it did not define the exact authority-request package or a disabled adapter seam that refuses dispatch attempts.

BLK-SYSTEM-041 creates that seam safely. It lets operators and future doctrine inspect a complete live-dispatch authority request while proving that the adapter returns `DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED` and records no subprocess, Codex, BLK-pipe, Git, or source mutation side effects.

This sprint is not permission to run Codex. It is the last disabled/fail-closed package before any later sprint could request actual live-dispatch authority.

---

## 2. Governing Documents and Obligations

- **BLK-024:** Use explicit maturity rungs. This sprint is L2 disabled/fail-closed transport plus L1 fixture evidence, not L5 production authority.
- **BLK-001:** Preserve separation between Hermes planning/audit, Codex tactical work, BLK-pipe mutation enforcement, BLK-test evidence, BEO publication, and RTM closure.
- **BLK-002 / BLK-005 / BLK-006:** Do not read, copy, parse, hash, summarize, scan, or mutate protected BLK-req vault bodies.
- **BLK-003:** Target Codex/BLK-pipe orchestration does not become current authority without a later explicit approval envelope.
- **BLK-004:** Go `blk-pipe` remains the mutation enforcement authority. Python authority-request fixtures are review and disabled-adapter artifacts only.
- **BLK-040:** Invocation profile remains fixture-only and starts no Codex process.
- **BLK-041:** Dispatch envelope remains fixture-only and starts no subprocess.
- **BLK-042:** Readiness gate remains review-only; `READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION` is not execution approval.

---

## 3. Proposed Implementation Surface

### New Boundary Document

```text
docs/BLK-043_codex-live-dispatch-authority-request-disabled-adapter-boundary.md
```

Required vocabulary:

```text
CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_FIXTURE_ONLY
CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_FIXTURE_ONLY
CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_REQUIRES_READY_REVIEW
CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_REQUIRES_SEPARATE_HUMAN_GRANT
CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_FAILS_CLOSED
CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_STARTS_NO_SUBPROCESS
CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_CALLS_NO_CODEX
CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_CALLS_NO_BLK_PIPE
CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_GRANTS_NO_EXECUTION_AUTHORITY
AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_EXECUTION
DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED
```

### New Python Module

```text
python/blk_codex_live_dispatch_authority_request.py
```

Proposed functions:

```text
build_codex_live_dispatch_authority_request(...)
validate_codex_live_dispatch_authority_request(record, ...)
simulate_disabled_codex_live_dispatch_adapter(record, ...)
```

The module must validate a BLK-042 readiness record, package human-review request metadata, and return a disabled adapter result. It must not run subprocesses, call Codex, call BLK-pipe, call Git, create worktrees, mutate files, read artifact bodies, read Codex configuration, inspect protected BLK-req bodies, use network clients, or install packages.

### New Tests

```text
python/test_blk_codex_live_dispatch_authority_request.py
```

Test scope:

1. complete authority request packages a BLK-042 readiness record and returns `AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_EXECUTION`;
2. disabled adapter simulation always returns `DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED` and all side-effect flags false;
3. missing, blocked, expired, replayed, or stale readiness evidence blocks request creation;
4. missing separate human grant marker blocks; present marker must still be review-only and not execution authority;
5. live execution flags, subprocess flags, BLK-pipe dispatch flags, source/Git mutation flags, protected-vault flags, BEO/RTM/drift flags, network/package/model/cyber flags, and production sandbox claims fail closed;
6. recursive authority-laundering strings/keys fail closed;
7. source AST contains no live imports/calls for subprocess, shell, Git, network clients, package managers, `exec`, or `eval`.

### Doctrine Gate Update

```text
python/test_active_doctrine_review_gates.py
```

Add a persistent gate requiring BLK-043 to preserve the disabled adapter and review-only authority-request boundary.

---

## 4. Exact Allowed Implementation Paths

```text
docs/plans/blk-system-041_codex-live-dispatch-authority-request-disabled-adapter.md
docs/outcomes/BLK-SYSTEM-041_task-000-outcome.md
docs/BLK-043_codex-live-dispatch-authority-request-disabled-adapter-boundary.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-041_task-001-outcome.md
python/blk_codex_live_dispatch_authority_request.py
python/test_blk_codex_live_dispatch_authority_request.py
docs/outcomes/BLK-SYSTEM-041_task-002-outcome.md
docs/reviews/BLK-SYSTEM-041_codex-live-dispatch-authority-request-hostile-review.md
docs/outcomes/BLK-SYSTEM-041_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-041_sprint-closeout.md
```

No `docs/active/`, `docs/requirements/`, or `docs/use_cases/` path may be modified or read for protected body content.

---

## 5. Task Breakdown

### Task 0 — Plan Publication

Create and publish this plan plus `docs/outcomes/BLK-SYSTEM-041_task-000-outcome.md`.

Verification:

```bash
git diff --check -- docs/plans/blk-system-041_codex-live-dispatch-authority-request-disabled-adapter.md docs/outcomes/BLK-SYSTEM-041_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
for path in [
    Path('docs/plans/blk-system-041_codex-live-dispatch-authority-request-disabled-adapter.md'),
    Path('docs/outcomes/BLK-SYSTEM-041_task-000-outcome.md'),
]:
    text = path.read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, path
print('markdown sanity PASS')
PY
```

Commit: `docs: plan blk-system sprint 041 codex live dispatch disabled adapter`

### Task 1 — BLK-043 Boundary and Doctrine Gate

Add BLK-043 and a persistent active doctrine gate. RED first: add the focused gate and verify failure before writing the doc.

Allowed files:

```text
docs/BLK-043_codex-live-dispatch-authority-request-disabled-adapter-boundary.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-041_task-001-outcome.md
```

Verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- docs/BLK-043_codex-live-dispatch-authority-request-disabled-adapter-boundary.md python/test_active_doctrine_review_gates.py docs/outcomes/BLK-SYSTEM-041_task-001-outcome.md
```

Commit: `docs: define blk043 codex live dispatch disabled adapter`

### Task 2 — Authority Request and Disabled Adapter Fixture

Implement the pure fixture/helper and tests. RED first: create the tests and verify failure before implementing the helper.

Required record shape:

```text
authority_request_id: codex_live_dispatch_authority_request
authority_request_status: CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_FIXTURE_ONLY
adapter_status: CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_FIXTURE_ONLY
evaluation: AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_EXECUTION or DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED
execution_authorized: false
codex_subprocess_started: false
blk_pipe_dispatched: false
source_mutation_authorized: false
separate_human_grant_required: true
```

Allowed files:

```text
python/blk_codex_live_dispatch_authority_request.py
python/test_blk_codex_live_dispatch_authority_request.py
docs/outcomes/BLK-SYSTEM-041_task-002-outcome.md
```

Verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_live_dispatch_authority_request -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_live_dispatch_readiness_gate -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_dispatch_envelope -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- python/blk_codex_live_dispatch_authority_request.py python/test_blk_codex_live_dispatch_authority_request.py docs/outcomes/BLK-SYSTEM-041_task-002-outcome.md
```

Commit: `feat: add codex live dispatch authority request disabled adapter`

### Task 3 — Hostile Review and Closeout

Perform hostile review, remediate blockers, write review and closeout docs, run final verification, commit, and push.

Hostile review questions:

1. Does any helper start subprocesses, call Codex, call Git, call BLK-pipe, install packages, use network/model/cyber/browser tooling, or inspect protected vaults?
2. Can `AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_EXECUTION` become execution approval?
3. Can a readiness record with `BLOCKED_NOT_AUTHORIZED` pass?
4. Can a missing separate human-grant requirement pass?
5. Can disabled adapter simulation be bypassed into live dispatch?
6. Can telemetry become canonical mutation, validation, approval, BEO, RTM, or drift evidence?
7. Can recursive authority-laundering keys/strings bypass validation?

Final verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_live_dispatch_authority_request -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_live_dispatch_readiness_gate -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_dispatch_envelope -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
export PATH="$HOME/.local/bin:$PATH"; go test ./... && go vet ./...
git diff --check
```

Commit: `docs: close blk-system sprint 041 codex live dispatch disabled adapter`

---

## 6. Expected Final State

BLK-SYSTEM-041 should leave the repository with:

1. BLK-043 documenting a review-only authority-request package and disabled/fail-closed adapter boundary;
2. a pure Python fixture that packages BLK-042 readiness evidence and always blocks adapter dispatch;
3. tests proving missing/blocked readiness, missing review-only human grant metadata, direct side-effect flags, live-surface imports/calls, and recursive authority laundering fail closed;
4. outcome, hostile review, and closeout docs recording the sprint.

This sprint creates an auditable package for a later explicit live-dispatch authority request, but grants no live execution authority now.
