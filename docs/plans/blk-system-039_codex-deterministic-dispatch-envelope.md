# BLK-SYSTEM-039 — Codex deterministic dispatch envelope plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, `systematic-debugging`, `code-review`, and `codex` when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable.

**Goal:** Define and implement a non-executing Codex deterministic dispatch envelope fixture that binds BLK-040's deterministic invocation profile to approval provenance, exact file boundaries, validation gates, telemetry artifact paths, failure ceilings, hostile-audit requirements, and operator escalation metadata without granting live Codex execution authority.

**BLK-024 track:** Track C — BLK-pipe blast shield and forge; Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening.

**Maturity level:** L1 fixture/local implementation plus L0 doctrine boundary. This sprint creates deterministic envelope fixtures and validation only. It does not grant live Codex execution authority, BLK-pipe dispatch authority, production sandbox authority, production BLK-test MCP authority, BEO publication authority, RTM generation authority, or drift rejection authority.

**Architecture:** Hermes remains architect and hostile auditor. Codex remains an untrusted tactical engine. BLK-pipe remains the deterministic mutation enforcement authority. BLK-SYSTEM-039 creates a repository-owned pre-dispatch envelope shape that future authority-bearing sprints can use, but this sprint itself starts no subprocesses and performs no dispatch.

**Tech Stack:** Markdown doctrine, Python fixtures/tests, active doctrine gates.

**Authority boundary:** Deterministic local dispatch-envelope fixture only. No live tactical engine dispatch, no subprocess execution by the envelope helper, no network/model/API access, no package-manager execution, no Git/source mutation, no protected BLK-req body reads, no BLK-pipe execution, no production BLK-test MCP, no BEO publication, no RTM generation, and no drift rejection authority.

---

## 0. Current repository state at planning

Captured before writing this plan:

```text
Date: 2026-05-09T13:35:58+10:00
Branch: main...origin/main
HEAD: ec5b66d docs: close blk-system sprint 038 codex invocation profile
Existing highest system plan: docs/plans/blk-system-038_codex-deterministic-invocation-profile.md
Existing highest BLK boundary doc: docs/BLK-040_codex-deterministic-invocation-profile-boundary.md
```

Discovery found no existing `BLK-SYSTEM-039`, `blk-system-039`, `BLK-041`, `codex-deterministic-dispatch`, or `dispatch envelope` owner in `docs/` or `python/` before planning.

---

## 1. Why this sprint exists

BLK-SYSTEM-038 created a deterministic Codex invocation profile fixture. BLK-040 explicitly states that future work may wire that profile into dispatch only after a separate sprint defines approval provenance, file-boundary enforcement, sandbox/containment evidence, validation gates, telemetry storage, hostile review, failure ceilings, rollback behavior, and operator escalation.

BLK-SYSTEM-039 is that next safe rung. It does not run Codex. It creates a non-executing dispatch-envelope fixture that can prove a future Codex dispatch request is fully bounded before any authority-bearing sprint asks to activate live execution.

---

## 2. Governing documents and obligations

### BLK-024 roadmap alignment

- Track C requires deterministic enforcement, exact allowlists, and negative tests before new authority paths.
- Track I requires operator-visible status and escalation evidence that explains what is missing, blocked, failed, or excluded.
- Track J requires honest sandbox/capability claims, environment and process-boundary clarity, and denial-by-default for network/model/cyber/package-manager capability expansion.

### BLK-001 alignment

BLK-001 separates Hermes planning, Codex tactical work, BLK-pipe mutation enforcement, BLK-test evidence, BEO handling, and blk-link trace closure. This sprint preserves separation by producing only a dispatch envelope fixture; it does not collapse planning, dispatch, mutation, verification, publication, or trace closure into one helper.

### BLK-002 / BLK-005 / BLK-006 alignment

This sprint must not read, copy, parse, hash, mutate, summarize, or scan protected BLK-req vault bodies. It may preserve opaque `trace_artifacts` and hash-like metadata supplied by tests, but must not compare those hashes against live protected vault content.

### BLK-003 alignment

BLK-003 describes Codex as Tier 3 tactical implementer receiving a bounded Layer 2 packet. This sprint creates an envelope fixture that must require bounded packet identity, approval provenance, exact file boundaries, validation gates, failure ceilings, and hostile audit expectations before any future live dispatch.

### BLK-004 alignment

BLK-004 keeps Go `blk-pipe` as the enforcement authority. Python dispatch-envelope checks are pre-dispatch convenience only. They must not claim that Python replaces Go allowlist enforcement, process control, validation execution, cleanup, Git staging, or report evidence.

### BLK-040 alignment

BLK-040 owns the deterministic Codex invocation profile. BLK-SYSTEM-039 must bind to that fixture shape without weakening it, removing required flags, converting telemetry into canonical evidence, or treating `danger-full-access` as trusted production sandboxing.

---

## 3. Non-authority statement

This plan does not authorize live Codex execution, reusable runtime dispatch, BLK-pipe execution, production BLK-test MCP, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads/copying/parsing/hashing/summarizing/scanning/mutation, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, source mutation outside exact approved allowlists, package-manager/network/model/cyber/browser tooling, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.

Passing this sprint does not grant permission to execute Codex against source. A later authority-bearing dispatch sprint must explicitly request and prove that authority.

---

## 4. Proposed implementation surface

### New boundary document

- `docs/BLK-041_codex-deterministic-dispatch-envelope-boundary.md`

Purpose: define the active BLK-System boundary for non-executing Codex deterministic dispatch-envelope fixture construction.

Required vocabulary:

```text
CODEX_DETERMINISTIC_DISPATCH_ENVELOPE_FIXTURE_ONLY
CODEX_DISPATCH_ENVELOPE_STARTS_NO_SUBPROCESS
CODEX_DISPATCH_REQUIRES_APPROVAL_PROVENANCE
CODEX_DISPATCH_REQUIRES_EXACT_FILE_BOUNDARIES
CODEX_DISPATCH_REQUIRES_VALIDATION_GATES
CODEX_DISPATCH_REQUIRES_FAILURE_CEILING
CODEX_DISPATCH_REQUIRES_HOSTILE_AUDIT
CODEX_DISPATCH_TELEMETRY_ADVISORY_ONLY
CODEX_DISPATCH_GRANTS_NO_EXECUTION_AUTHORITY
```

### New Python module

- `python/blk_codex_dispatch_envelope.py`

Proposed functions:

- `build_codex_deterministic_dispatch_envelope(...)`
- `validate_codex_deterministic_dispatch_envelope(envelope)`

The helper must build/validate structured dictionaries only. It may import and validate `blk_codex_invocation_profile` output. It must not run subprocesses, call Codex, create worktrees, call Git, call BLK-pipe, read Codex config, inspect network state, mutate files, stage/commit/push, or inspect protected BLK-req bodies.

### New tests

- `python/test_blk_codex_dispatch_envelope.py`

Test scope:

1. valid envelope includes BLK-040 deterministic profile identity and validates the profile;
2. envelope requires sprint-dispatch approval provenance fields: source system, operator identity, message/event ID when available, timestamp, exact approved scope, and explicit excluded authorities;
3. envelope rejects stale/expired/replayed approval IDs and missing used-approval/run state;
4. envelope requires non-empty exact allowed modified/new file boundaries and rejects broad pathspecs, protected BLK-req paths, `.git` paths, and parent traversal;
5. envelope requires repository-owned validation profiles or exact validation gate descriptors, not free-form shell;
6. envelope requires telemetry paths to be bounded relative artifact paths and advisory only;
7. envelope requires failure ceiling metadata and hostile-audit checklist entries;
8. envelope requires operator escalation metadata for missing approval, validation failure, policy block, and failure ceiling cases;
9. envelope rejects live execution, BLK-pipe dispatch, source/Git mutation, protected-vault access, BEO publication, RTM generation, drift rejection, package-manager/network/model/cyber/browser authority claims;
10. envelope returns `dispatch_started_by_envelope_helper: false` and `subprocess_started_by_envelope_helper: false`.

### Doctrine gate update

- `python/test_active_doctrine_review_gates.py`

Add a persistent gate requiring BLK-041 to preserve the deterministic dispatch-envelope boundary and to deny live Codex authority, BLK-pipe dispatch, native sandbox trust, protected-vault reads, BEO publication, RTM generation, and drift rejection.

---

## 5. Exact allowed implementation paths

Implementation may modify or create only these paths unless a hostile review finds a required exact-path correction:

```text
docs/plans/blk-system-039_codex-deterministic-dispatch-envelope.md
docs/outcomes/BLK-SYSTEM-039_task-000-outcome.md
docs/BLK-041_codex-deterministic-dispatch-envelope-boundary.md
python/blk_codex_dispatch_envelope.py
python/test_blk_codex_dispatch_envelope.py
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-039_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-039_task-002-outcome.md
docs/reviews/BLK-SYSTEM-039_codex-deterministic-dispatch-envelope-hostile-review.md
docs/outcomes/BLK-SYSTEM-039_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-039_sprint-closeout.md
```

No `docs/active/`, `docs/requirements/`, or `docs/use_cases/` path may be modified or read for protected body content.

---

## 6. Task breakdown

### Task 0 — Plan publication

**Objective:** Commit and push this plan plus a task-000 outcome document.

**Allowed files:**

```text
docs/plans/blk-system-039_codex-deterministic-dispatch-envelope.md
docs/outcomes/BLK-SYSTEM-039_task-000-outcome.md
```

**Verification:**

```bash
git diff --check -- docs/plans/blk-system-039_codex-deterministic-dispatch-envelope.md docs/outcomes/BLK-SYSTEM-039_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
for path in [
    Path('docs/plans/blk-system-039_codex-deterministic-dispatch-envelope.md'),
    Path('docs/outcomes/BLK-SYSTEM-039_task-000-outcome.md'),
]:
    text = path.read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, path
print('markdown sanity PASS')
PY
```

**Commit:** `docs: plan blk-system sprint 039 codex dispatch envelope`

### Task 1 — Doctrine boundary and active gate

**Objective:** Add BLK-041 as an active boundary document and persistent doctrine gate tests.

**RED tests first:**

- Add tests proving BLK-041 must mention non-executing dispatch-envelope fixtures, approval provenance, exact file boundaries, validation gates, telemetry advisory-only status, failure ceilings, hostile audit, no subprocess startup, no live Codex authority, no BLK-pipe dispatch authority, and no protected-vault/BEO/RTM authority.
- The focused gate test must fail before BLK-041 exists or before required markers are present.

**Allowed files:**

```text
docs/BLK-041_codex-deterministic-dispatch-envelope-boundary.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-039_task-001-outcome.md
```

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- docs/BLK-041_codex-deterministic-dispatch-envelope-boundary.md python/test_active_doctrine_review_gates.py docs/outcomes/BLK-SYSTEM-039_task-001-outcome.md
```

**Commit:** `docs: define blk041 codex dispatch envelope boundary`

### Task 2 — Dispatch envelope fixtures

**Objective:** Implement the non-executing Codex deterministic dispatch-envelope builder and validation tests.

**RED tests first:**

- Tests must first prove the missing helper fails to build/validate approval provenance, exact file boundaries, validation gates, telemetry paths, failure ceiling metadata, hostile audit metadata, and non-authority flags.
- GREEN implementation must be minimal and pure: dictionary construction and validation only.

**Required envelope properties:**

```text
profile_id: codex_deterministic_dispatch_envelope
dispatch_status: CODEX_DETERMINISTIC_DISPATCH_ENVELOPE_FIXTURE_ONLY
codex_profile.profile_id: codex_deterministic_invocation_profile
approval_provenance.source_system
approval_provenance.operator_identity
approval_provenance.message_event_id
approval_provenance.timestamp
approval_provenance.exact_approved_scope
approval_provenance.explicit_excluded_authorities
allowed_modified_files
allowed_new_files
validation_profiles or validation_gates
telemetry_artifacts
failure_ceiling.max_iterations
hostile_audit.required_checks
operator_escalation.required_cases
dispatch_started_by_envelope_helper: false
subprocess_started_by_envelope_helper: false
```

**Allowed files:**

```text
python/blk_codex_dispatch_envelope.py
python/test_blk_codex_dispatch_envelope.py
docs/outcomes/BLK-SYSTEM-039_task-002-outcome.md
```

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_dispatch_envelope -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- python/blk_codex_dispatch_envelope.py python/test_blk_codex_dispatch_envelope.py docs/outcomes/BLK-SYSTEM-039_task-002-outcome.md
```

**Commit:** `feat: add codex deterministic dispatch envelope fixtures`

### Task 3 — Hostile review and sprint closeout

**Objective:** Perform hostile review, remediate blockers, write review and closeout docs, and push final state.

**Hostile review focus:**

1. Does the envelope helper accidentally start subprocesses, call Codex, call Git, create worktrees, call BLK-pipe, or inspect protected vaults?
2. Can missing/stale/replayed approval provenance pass?
3. Can broad pathspecs, protected paths, `.git` paths, parent traversal, or empty allowlists pass?
4. Can validation gates become free-form shell or package-manager/network/model/cyber/browser execution?
5. Can telemetry artifacts become canonical mutation, validation, approval, BEO, RTM, or drift evidence?
6. Does the envelope launder `danger-full-access` or BLK-040 telemetry into production sandbox or execution authority?
7. Does the sprint imply live Codex authority, BLK-pipe dispatch, BLK-test authority, BEO publication, RTM generation, protected-vault access, source mutation, or drift rejection?

**Allowed files:**

```text
docs/reviews/BLK-SYSTEM-039_codex-deterministic-dispatch-envelope-hostile-review.md
docs/outcomes/BLK-SYSTEM-039_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-039_sprint-closeout.md
```

If hostile review finds code or doctrine blockers, remediation may touch only the exact files already authorized by Tasks 1 and 2, and the outcome must record the reason.

**Final verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_dispatch_envelope -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
export PATH="$HOME/.local/bin:$PATH"; go test ./... && go vet ./...
git diff --check
```

**Commit:** `docs: close blk-system sprint 039 codex dispatch envelope`

---

## 7. Required implementation invariants

1. The dispatch-envelope builder must be pure and side-effect free.
2. The dispatch-envelope builder must not call `codex`, subprocess, shell, Git, BLK-pipe, BLK-test, network APIs, package managers, browsers, model services, BEO tooling, RTM tooling, or protected-vault readers.
3. The envelope must validate and preserve a BLK-040 deterministic invocation profile without weakening its required flags or advisory telemetry markers.
4. The envelope must require sprint-dispatch approval provenance and must fail closed on missing, stale, expired, or replayed approval/run identifiers.
5. The envelope must require exact file boundaries and reject broad pathspecs, parent traversal, `.git`, protected BLK-req paths, active-vault paths, empty path elements, and shell metacharacter-like file entries.
6. The envelope must require deterministic validation profiles or gate descriptors and reject free-form shell, network, package-manager, model, browser, or cyber wording.
7. The envelope must require failure-ceiling metadata and hostile-audit checklist entries before any future dispatch request can be considered complete.
8. The envelope must preserve operator escalation cases for missing approval, policy block, validation failure, failure ceiling, malformed telemetry, and denied authority.
9. Codex JSONL events and final-message artifacts remain advisory telemetry only; Git diff, BLK-pipe report evidence, separately authorized BLK-test evidence, and hostile audit remain canonical physical evidence.
10. No future executor may treat this envelope as permission to run Codex without a separate dispatch approval and hostile audit envelope that explicitly grants live execution authority.

---

## 8. Outcome document requirements

Each task outcome must include:

- task ID and status;
- exact files changed;
- RED/GREEN evidence where applicable;
- verification commands and results;
- authority boundary statement;
- planned commit message and final hash reported by controller/closeout where self-referential hashing would be impossible;
- note that no protected BLK-req body reads occurred.

Task 3 closeout must additionally include:

- final hostile review verdict;
- final verification suite results;
- final commits;
- final repo status;
- statement that BLK-SYSTEM-039 did not authorize live Codex execution, BLK-pipe dispatch, source mutation, or production sandbox claims.

---

## 9. Expected final state

After successful closeout, BLK-System will have:

1. BLK-041 documenting deterministic Codex dispatch-envelope boundaries;
2. a pure Python fixture/helper that builds and validates a complete non-executing dispatch envelope;
3. tests proving approval provenance, exact file boundaries, validation gates, telemetry paths, failure ceilings, hostile audit metadata, and operator escalation are required;
4. tests proving forbidden authority laundering fails closed;
5. outcome/review/closeout docs recording the sprint.

This creates a safer future path for explicit Codex tactical dispatch compatibility without granting live tactical authority now.
