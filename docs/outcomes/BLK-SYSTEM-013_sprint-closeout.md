# BLK-SYSTEM-013 Sprint Closeout — Approval/Source-Evidence Authorization

**Sprint ID:** `BLK-SYSTEM-013` / `blk-system-013`  
**Sprint title:** Approval-channel and Source-Evidence Authorization Mechanics  
**Status:** COMPLETE  
**Closeout timestamp:** 2026-05-06T21:03:53+10:00  
**Closeout commit subject:** `docs: close out blk-system sprint 013`

---

## 1. Executive Summary

BLK-SYSTEM-013 implemented deterministic local BLK-test-specific approval/source-evidence validation only.

The sprint adds:

- a durable implementation plan;
- a Sprint 013 approval/source-evidence boundary review;
- dependency-free Python approval validation helpers;
- exact approval/request/source-evidence binding gates;
- expiry/replay rejection and deterministic audit hashes;
- disabled transport preflight evidence that remains blocked until Sprint 014;
- active doctrine `BLK-019` for the approval/source-evidence authorization contract;
- task outcome docs for every implementation task.

BLK-SYSTEM-013 does not authorize live BLK-test MCP, does not authorize live MCP client/server startup, does not execute fixed-tool tests, and does not create first-live-smoke authority. Sprint 014 remains the future owner for any first live fixed-tool BLK-test MCP smoke under explicit human approval.

---

## 2. Commit Ledger

| Task | Implementation / docs commit | Outcome commit | Summary |
| --- | --- | --- | --- |
| Task 0 | `7bf42fa docs: plan blk-system sprint 013 approval authorization` | `70e8082 docs: record blk-system sprint 013 task 0 outcome` | Committed the sprint plan as durable execution contract. |
| Task 1 | `ed762ef docs: define blk-system sprint 013 approval boundary` | `710ec2f docs: record blk-system sprint 013 task 1 outcome` | Added boundary review and active-doctrine gate for Sprint 013 markers. |
| Task 2 | `1917536 feat: add blk-test approval record validator` | `16b59fc docs: record blk-system sprint 013 task 2 outcome` | Added dependency-free approval record schema/parser and fail-closed non-authority output. |
| Task 3 | `a7e8f17 test: bind blk-test approval to exact source evidence` | `2bd04fb docs: record blk-system sprint 013 task 3 outcome` | Added exact binding gates for source evidence, tools, profile, workspace, and timeout/output profiles. |
| Task 4 | `67a8479 feat: add blk-test approval replay and audit gates` | `cb33822 docs: record blk-system sprint 013 task 4 outcome` | Added expiry/replay rejection and deterministic audit hashes. |
| Task 5 | `2129b7a feat: bind sprint 013 approval preflight without live startup` | `39a694a docs: record blk-system sprint 013 task 5 outcome` | Added disabled transport approval preflight that remains blocked until Sprint 014. |
| Task 6 | `0a847c0 docs: define blk-test approval source evidence contract` | `a2517a6 docs: record blk-system sprint 013 task 6 outcome` | Added BLK-019 active doctrine and BLK-017/018 cross-reference gates. |
| Task 7 | planned closeout commit subject: `docs: close out blk-system sprint 013` | this document | Final verification and closeout. |

---

## 3. Artifact Ledger

```text
docs/plans/blk-system-013_approval-source-evidence-authorization.md
docs/reviews/BLK-SYSTEM-013_approval-source-evidence-boundary-review.md
python/blk_test_mcp_approval_authorization.py
python/test_blk_test_mcp_approval_authorization.py
python/blk_test_mcp_disabled_transport.py
python/test_blk_test_mcp_disabled_transport.py
python/test_active_doctrine_review_gates.py
docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md
docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md
docs/BLK-019_blk-test-mcp-approval-source-evidence-authorization.md
docs/outcomes/BLK-SYSTEM-013_task-000-outcome.md
docs/outcomes/BLK-SYSTEM-013_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-013_task-002-outcome.md
docs/outcomes/BLK-SYSTEM-013_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-013_task-004-outcome.md
docs/outcomes/BLK-SYSTEM-013_task-005-outcome.md
docs/outcomes/BLK-SYSTEM-013_task-006-outcome.md
docs/outcomes/BLK-SYSTEM-013_sprint-closeout.md
```

---

## 4. Implemented Contract

### 4.1 Approval record schema

`python/blk_test_mcp_approval_authorization.py` now validates BLK-test-specific approval records with required:

- approval kind;
- approval ID;
- operator identity;
- approval timestamp;
- issued timestamp;
- expiry timestamp;
- source evidence;
- requested fixed BLK-test tool(s);
- test profile;
- workspace identity;
- timeout/output profile.

### 4.2 Exact source/request binding

Approval records are fail-closed unless these fields exactly match the authorization request envelope:

- source BLK-pipe report identity;
- `beb_id`;
- source `commit_hash`;
- `pre_engine_hash`;
- canonical `trace_artifacts`;
- requested fixed BLK-test tool(s);
- test profile;
- workspace identity;
- timeout/output profile.

### 4.3 Rejection gates

The validator rejects:

- `codex-live` and `BLK_APPROVE_CODEX_LIVE` as BLK-test approval;
- missing required fields;
- malformed canonical trace hashes;
- unknown, wildcard, duplicate, shell-like, or dynamic requested tools;
- source-evidence mismatches;
- profile/workspace/timeout-output mismatches;
- protected BLK-req vault body references;
- shell/command/exec/eval/source-mutation/BEO-publication/RTM-generation authority fields;
- malformed UTC timestamps;
- expired approvals;
- replayed approval IDs.

### 4.4 Audit evidence

Accepted local validation returns deterministic:

- `approval_record_hash`;
- `source_evidence_hash`;
- `authorization_request_hash`.

Each hash is `sha256:<64-lowercase-hex>` computed from canonical JSON. These are evidence identifiers only and do not create live, publication, ledger, mutation, or active-vault authority.

### 4.5 Disabled transport preflight

`python/blk_test_mcp_disabled_transport.py` now records Sprint 013 validated approval evidence through `evaluate_sprint013_approval_preflight(...)`, but returns:

```text
STARTUP_BLOCKED_SPRINT014_REQUIRED
```

The preflight keeps `server_started`, `client_started`, `network_called`, `subprocess_called`, and tool execution fields false/empty.

---

## 5. Active Doctrine Result

`docs/BLK-019_blk-test-mcp-approval-source-evidence-authorization.md` is now the active approval/source-evidence authorization contract.

Boundary preservation:

- BLK-017 remains the active disabled transport contract.
- BLK-018 remains the active inert workspace/process-control probe contract.
- BLK-019 records approval/source-evidence validation evidence only.
- Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke.

---

## 6. Final Verification Evidence

Verification was run from `/home/dad/BLK-System` on `main` at/after `a2517a6` before closeout staging.

### 6.1 Python unittest discovery

Command:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s python -p 'test_*.py'
```

Result:

```text
Ran 255 tests in 5.199s

OK
```

### 6.2 Pytest suite

Command:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python
```

Result:

```text
collected 257 items

============================= 257 passed in 5.43s ==============================
```

### 6.3 Go tests

Command:

```bash
go test ./...
```

Result:

```text
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	6.937s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	0.140s
```

### 6.4 Go vet

Command:

```bash
go vet ./...
```

Result:

```text
PASS (no output)
```

### 6.5 Git whitespace check

Command:

```bash
git diff --check
```

Result:

```text
PASS (no output)
```

### 6.6 Cache/status hygiene

Commands:

```bash
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
find python -type d -name __pycache__ -prune -exec rm -rf {} +
git status --short --branch
```

Pre-closeout result:

```text
## main...origin/main
```

---

## 7. Non-Authority Statement

BLK-SYSTEM-013 implemented approval/source-evidence validation only.

It does not authorize live BLK-test MCP. It does not authorize live MCP client/server startup. It does not execute fixed-tool tests. It does not authorize arbitrary shell or dynamic command execution. It does not mutate primary repo as BLK-test behavior. It does not stage, commit, push, reset, stash, or checkout source as BLK-test behavior. It does not authorize authoritative BEO publication. It does not authorize RTM generation. It does not authorize RTM drift rejection authority. It does not read protected BLK-req vault bodies. It does not parse active-vault requirement bodies. It does not claim production sandbox/container/cgroup/VM/seccomp/AppArmor/SELinux enforcement. It does not claim production host-secret isolation. It does not authorize first live smoke.

Human sprint-executor commits and pushes for reviewed Sprint 013 code and outcome documentation are project-maintenance actions, not BLK-test source-mutation authority.

---

## 8. BLK-SYSTEM-014 Handoff Seed

Next candidate sprint:

```text
BLK-SYSTEM-014 — First live fixed-tool BLK-test MCP smoke under explicit human approval
```

Narrow prerequisites for Sprint 014:

1. BLK-017 disabled transport contract remains intact or is explicitly superseded by a Sprint 014 plan and human approval.
2. BLK-018 workspace/process controls must pass.
3. BLK-019 approval/source-evidence validation must pass for the exact source/request/workspace/profile envelope.
4. Human approval must be explicit, current, and BLK-test-specific.
5. Fixed-tool scope must remain bounded and deterministic.
6. No arbitrary shell, source mutation, BEO publication, RTM generation, active-vault body reads, production sandbox claims, or host-secret claims may be added unless a later explicit human-approved sprint grants those authorities.

---

## 9. Closeout Staging Requirements

Before committing this closeout:

```bash
python - <<'PY'
from pathlib import Path
path = Path('docs/outcomes/BLK-SYSTEM-013_sprint-closeout.md')
text = path.read_text()
required = [
    'BLK-SYSTEM-013',
    'approval/source-evidence validation only',
    'does not authorize live BLK-test MCP',
    'does not authorize live MCP client/server startup',
    'does not execute fixed-tool tests',
    'does not authorize authoritative BEO publication',
    'does not authorize RTM generation',
    'does not read protected BLK-req vault bodies',
    'BLK-SYSTEM-014',
    'First live fixed-tool BLK-test MCP smoke under explicit human approval',
]
missing = [marker for marker in required if marker not in text]
if missing:
    raise SystemExit(f'missing closeout markers: {missing}')
fence = chr(96) * 3
if text.count(fence) % 2:
    raise SystemExit('unbalanced markdown fences')
print('BLK-SYSTEM-013 closeout markers: PASS')
PY

git diff --check -- docs/outcomes/BLK-SYSTEM-013_sprint-closeout.md
git add docs/outcomes/BLK-SYSTEM-013_sprint-closeout.md
git diff --cached --name-only
```

Expected staged path:

```text
docs/outcomes/BLK-SYSTEM-013_sprint-closeout.md
```
