# BLK-SYSTEM-038 — Codex deterministic invocation profile plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, `systematic-debugging`, `code-review`, and `codex` when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable.

**Goal:** Define and implement a deterministic local Codex tactical-engine invocation profile for BLK-System that includes the newly available Codex CLI flags worth adopting now: `--ephemeral`, `--ignore-user-config`, `--ignore-rules`, `--json`, `--output-last-message`, and explicit disabling of Codex ambient features (`hooks`, `plugins`, `goals`).

**BLK-024 track:** Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening; supporting Track C — BLK-pipe blast shield and forge.

**Maturity level:** L1 fixture/local implementation plus L0 doctrine boundary. This sprint creates deterministic command-profile fixtures and validation only. It does not grant live Codex execution authority, production sandbox authority, BLK-pipe dispatch authority, or broader tactical autonomy.

**Architecture:** Hermes remains the architect and hostile auditor. Codex remains an untrusted tactical engine. This sprint defines a repository-owned, testable command-profile builder and advisory evidence shape for future BLK/Hermes use; it does not make Codex the source of truth for mutation, validation, approval, sandboxing, or success.

**Tech Stack:** Markdown doctrine, Python fixtures/tests, active doctrine gates.

**Authority boundary:** Deterministic local profile construction only. No live tactical engine dispatch, no subprocess execution by the profile builder, no network/model/API access, no package-manager execution, no Git/source mutation, no protected BLK-req body reads, no production BLK-test MCP, no BEO publication, no RTM generation, and no drift rejection authority.

---

## 0. Current repository state at planning

Captured before writing this plan:

```text
Date: 2026-05-09T10:25:39+10:00
Branch: main...origin/main
HEAD: 21d995c docs: close blk-system sprint 037 operator escalation packages
Existing highest system plan: docs/plans/blk-system-037_operator-escalation-package-improvements.md
Existing highest BLK boundary doc: docs/BLK-039_track-i-health-check-escalation-package-boundary.md
```

The sprint ID `BLK-SYSTEM-038` and boundary doc ID `BLK-040` were not found in `docs/` or `python/` during pre-plan discovery.

---

## 1. Why this sprint exists

Codex CLI has moved from the earlier local baseline around `0.118.0` to `0.130.0`. The newly useful non-interactive surface includes deterministic-operation flags that BLK-System should capture before any future Codex tactical-engine integration is treated as reusable:

- `--ephemeral`
- `--ignore-user-config`
- `--ignore-rules`
- `--json`
- `--output-last-message <FILE>`
- `--disable hooks`
- `--disable plugins`
- `--disable goals`

These flags are valuable because they reduce hidden ambient behavior, improve observability, and produce stable artifacts. They do **not** by themselves provide sufficient isolation or authority for production Codex execution.

Local sandbox smoke evidence from planning showed that Codex `0.130.0` still fails the Linux sandbox on this host with the known bubblewrap/RTM_NEWADDR failure class. Therefore this sprint must preserve the existing BLK/Hermes external-isolation posture and must not claim that Codex native sandboxing is available.

---

## 2. Governing documents and obligations

### BLK-024 roadmap alignment

- Track I requires operator-visible status/evidence that explains what is blocked, failed, or disabled.
- Track J requires honest sandbox/capability claims and denial-by-default for network/model/cyber/package-manager capability expansion.
- Track C requires `blk-pipe` to remain the deterministic blast shield and forbids replacing BLK enforcement with LLM honesty.

### BLK-001 alignment

BLK-001 separates Hermes planning, Codex tactical work, BLK-pipe mutation enforcement, BLK-test evidence, and BLK-link trace closure. This sprint preserves that separation by treating Codex command-profile construction as advisory fixture/policy support only.

### BLK-002 / BLK-005 / BLK-006 alignment

This sprint must not read, copy, hash, mutate, or scan protected BLK-req bodies. It must not alter the BLK-req staging, promotion, canonical hash, or active-vault authority path.

### BLK-003 alignment

BLK-003 describes Codex as Tier 3 tactical implementer receiving a bounded Layer 2 packet. This sprint updates the *future tactical invocation profile* for such use but does not invoke BLK-pipe or dispatch live Codex. Human dispatch gates, hostile audit, and failure ceilings remain required for any future execution.

### BLK-004 alignment

BLK-004 keeps Go `blk-pipe` as the enforcement authority. This sprint may define helper-side command-profile validation, but Go/BLK audit remains final authority for mutation, allowed files, validation, and rollback.

---

## 3. Non-authority statement

This plan does not authorize production BLK-test MCP, live tactical LLM execution, Codex live execution as a reusable runtime path, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads/copying/parsing/hashing/mutation, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, package-manager/network/model/cyber tooling, browser automation, remote service access, production health-check authority, production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux claims, network firewall claims, or host-secret-isolation claims.

The sprint may record the local Codex version and command-profile shape as evidence. Passing this sprint does not grant permission to execute Codex against source except through a later explicit dispatch plan and audit envelope.

---

## 4. Proposed implementation surface

### New boundary document

- `docs/BLK-040_codex-deterministic-invocation-profile-boundary.md`

Purpose: define the active BLK-System boundary for deterministic Codex tactical invocation profile construction and explicitly deny ambient features.

Required vocabulary:

```text
CODEX_DETERMINISTIC_INVOCATION_PROFILE_FIXTURE_ONLY
CODEX_AMBIENT_FEATURES_DISABLED
CODEX_PROFILE_BUILDER_STARTS_NO_SUBPROCESS
CODEX_JSONL_EVENTS_ADVISORY_ONLY
CODEX_FINAL_MESSAGE_ARTIFACT_ADVISORY_ONLY
CODEX_NATIVE_SANDBOX_NOT_TRUSTED_ON_THIS_HOST
CODEX_PROFILE_GRANTS_NO_EXECUTION_AUTHORITY
```

### New Python module

- `python/blk_codex_invocation_profile.py`

Proposed functions:

- `build_codex_deterministic_invocation_profile(...)`
- `validate_codex_deterministic_invocation_profile(profile)`

The helper must build/validate structured dictionaries and argv arrays only. It must not run subprocesses, read Codex config, inspect network state, mutate files, create directories, stage/commit/push, or invoke BLK-pipe.

### New tests

- `python/test_blk_codex_invocation_profile.py`

Test scope:

1. valid profile includes required include-now flags;
2. valid profile includes explicit ambient feature disables for `hooks`, `plugins`, and `goals`;
3. profile requires `--ephemeral`;
4. profile requires `--ignore-user-config`;
5. profile requires `--ignore-rules`;
6. profile requires `--json`;
7. profile requires `--output-last-message` with a bounded relative artifact path;
8. profile rejects absolute artifact paths outside approved artifact roots;
9. profile rejects missing or enabled ambient features;
10. profile rejects caller-supplied extra Codex flags unless explicitly allowlisted;
11. profile rejects `--dangerously-bypass-approvals-and-sandbox` in the deterministic profile shape;
12. profile records `sandbox_mode: "danger-full-access"` only as host workaround evidence, not as production sandbox proof;
13. profile rejects production authority claims;
14. profile rejects network/model/package-manager/cyber/browser/tooling authority claims;
15. builder output contains `subprocess_started_by_profile_helper: false`.

### Doctrine gate update

- `python/test_active_doctrine_review_gates.py`

Add a persistent gate requiring BLK-040 to preserve the deterministic invocation profile boundary and to deny live Codex authority, native sandbox trust, ambient features, protected-vault reads, BEO publication, RTM generation, and drift rejection.

---

## 5. Exact allowed implementation paths

Implementation may modify or create only these paths unless a hostile review finds a required exact-path correction:

```text
docs/plans/blk-system-038_codex-deterministic-invocation-profile.md
docs/outcomes/BLK-SYSTEM-038_task-000-outcome.md
docs/BLK-040_codex-deterministic-invocation-profile-boundary.md
python/blk_codex_invocation_profile.py
python/test_blk_codex_invocation_profile.py
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-038_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-038_task-002-outcome.md
docs/reviews/BLK-SYSTEM-038_codex-deterministic-invocation-profile-hostile-review.md
docs/outcomes/BLK-SYSTEM-038_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-038_sprint-closeout.md
```

No `docs/active/`, `docs/requirements/`, or `docs/use_cases/` path may be modified or read for protected body content.

---

## 6. Task breakdown

### Task 0 — Plan publication

**Objective:** Commit and push this plan plus a task-000 outcome document.

**Allowed files:**

```text
docs/plans/blk-system-038_codex-deterministic-invocation-profile.md
docs/outcomes/BLK-SYSTEM-038_task-000-outcome.md
```

**Verification:**

```bash
git diff --check -- docs/plans/blk-system-038_codex-deterministic-invocation-profile.md docs/outcomes/BLK-SYSTEM-038_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
for path in [
    Path('docs/plans/blk-system-038_codex-deterministic-invocation-profile.md'),
    Path('docs/outcomes/BLK-SYSTEM-038_task-000-outcome.md'),
]:
    text = path.read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, path
print('markdown sanity PASS')
PY
```

**Commit:** `docs: plan blk-system sprint 038 codex invocation profile`

### Task 1 — Doctrine boundary and active gate

**Objective:** Add BLK-040 as an active boundary document and persistent doctrine gate tests.

**RED tests first:**

- Add tests proving BLK-040 must mention deterministic fixture-only profile construction, disabled ambient features, no subprocess startup, no live Codex authority, no native sandbox trust, and no protected-vault/BEO/RTM authority.
- The focused gate test must fail before BLK-040 exists or before required markers are present.

**Allowed files:**

```text
docs/BLK-040_codex-deterministic-invocation-profile-boundary.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-038_task-001-outcome.md
```

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- docs/BLK-040_codex-deterministic-invocation-profile-boundary.md python/test_active_doctrine_review_gates.py docs/outcomes/BLK-SYSTEM-038_task-001-outcome.md
```

**Commit:** `docs: define blk040 codex invocation boundary`

### Task 2 — Deterministic profile builder fixtures

**Objective:** Implement the deterministic Codex invocation profile builder and validation tests.

**RED tests first:**

- Tests must first prove the missing helper fails to build/validate the include-now flags and ambient-feature disables.
- GREEN implementation must be minimal and pure: dictionary/argv construction and validation only.

**Required include-now argv properties:**

```text
codex exec
--model <approved-model>
-C <worktree>
-s danger-full-access
-a never
--ephemeral
--ignore-user-config
--ignore-rules
--disable hooks
--disable plugins
--disable goals
--json
--output-last-message <relative-artifact-path>
```

`danger-full-access` must be represented as a local host workaround because the current host's Codex Linux sandbox still fails. It must not be represented as production sandbox authority.

**Allowed files:**

```text
python/blk_codex_invocation_profile.py
python/test_blk_codex_invocation_profile.py
docs/outcomes/BLK-SYSTEM-038_task-002-outcome.md
```

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- python/blk_codex_invocation_profile.py python/test_blk_codex_invocation_profile.py docs/outcomes/BLK-SYSTEM-038_task-002-outcome.md
```

**Commit:** `feat: add codex deterministic invocation profile fixtures`

### Task 3 — Hostile review and sprint closeout

**Objective:** Perform hostile review, remediate blockers, write review and closeout docs, and push final state.

**Hostile review focus:**

1. Does the profile builder accidentally start subprocesses?
2. Can caller-supplied flags re-enable hooks/plugins/goals?
3. Can caller-supplied flags remove `--ephemeral`, `--ignore-user-config`, `--ignore-rules`, `--json`, or `--output-last-message`?
4. Can artifact paths escape the approved relative artifact root?
5. Does `danger-full-access` get laundered into production sandbox authority?
6. Does the sprint imply live Codex authority, BLK-pipe dispatch, BLK-test authority, BEO publication, RTM generation, or protected-vault access?
7. Are JSONL events/final messages treated as advisory only rather than canonical mutation evidence?

**Allowed files:**

```text
docs/reviews/BLK-SYSTEM-038_codex-deterministic-invocation-profile-hostile-review.md
docs/outcomes/BLK-SYSTEM-038_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-038_sprint-closeout.md
```

If hostile review finds code or doctrine blockers, remediation may touch only the exact files already authorized by Tasks 1 and 2, and the outcome must record the reason.

**Final verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
export PATH="$HOME/.local/bin:$PATH"; go test ./... && go vet ./...
git diff --check
```

**Commit:** `docs: close blk-system sprint 038 codex invocation profile`

---

## 7. Required implementation invariants

1. The profile builder must be pure and side-effect free.
2. The profile builder must not call `codex`, `subprocess`, shell, Git, BLK-pipe, BLK-test, network APIs, package managers, browsers, or model services.
3. The deterministic profile must include `--ephemeral`, `--ignore-user-config`, `--ignore-rules`, `--json`, and `--output-last-message`.
4. The deterministic profile must explicitly disable `hooks`, `plugins`, and `goals`.
5. The deterministic profile must reject authority-laundering fields and unsupported caller-supplied flags.
6. `danger-full-access` may be present only as a documented host workaround inside external BLK/Hermes containment.
7. Codex JSONL events and final-message artifacts are advisory telemetry only; Git diff and BLK validation remain canonical physical evidence.
8. No future executor may treat this profile as permission to run Codex without a separate dispatch approval and hostile audit envelope.

---

## 8. Outcome document requirements

Each task outcome must include:

- task ID and status;
- exact files changed;
- RED/GREEN evidence where applicable;
- verification commands and results;
- authority boundary statement;
- exact commit hash after commit;
- note that no protected BLK-req body reads occurred.

Task 3 closeout must additionally include:

- final hostile review verdict;
- final verification suite results;
- final commits;
- final repo status;
- statement that BLK-SYSTEM-038 did not authorize live Codex execution or production sandbox claims.

---

## 9. Expected final state

After successful closeout, BLK-System will have:

1. BLK-040 documenting deterministic Codex invocation profile boundaries;
2. a pure Python fixture/helper that builds and validates the include-now Codex flags;
3. tests proving ambient Codex hooks/plugins/goals remain disabled in the BLK deterministic profile;
4. tests proving hidden user config/rules are suppressed;
5. tests proving Codex telemetry artifacts are advisory only;
6. outcome/review/closeout docs recording the sprint.

This creates a safer future path for Codex tactical execution compatibility without granting live tactical authority now.
