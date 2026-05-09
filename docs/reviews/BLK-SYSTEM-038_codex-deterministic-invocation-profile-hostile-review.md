# BLK-SYSTEM-038 — Codex deterministic invocation profile hostile review

**Status:** PASS after remediation
**Date:** 2026-05-09T10:49:46+10:00
**Sprint:** BLK-SYSTEM-038
**Reviewer:** Hermes direct hostile review; no live Codex execution or tactical LLM delegation used

---

## 1. Review Scope

Reviewed Task 1 and Task 2 deliverables against the BLK-SYSTEM-038 hostile review focus:

```text
docs/BLK-040_codex-deterministic-invocation-profile-boundary.md
python/blk_codex_invocation_profile.py
python/test_blk_codex_invocation_profile.py
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-038_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-038_task-002-outcome.md
```

No protected BLK-req body content was read for this review.

---

## 2. Hostile Review Questions

### 2.1 Does the profile builder accidentally start subprocesses?

**Verdict:** PASS.

Evidence:

- `python/blk_codex_invocation_profile.py` imports only `__future__`, `pathlib.PurePosixPath`, and `typing.Any`.
- The helper constructs dictionaries and argv arrays only.
- Tests include an AST/source gate rejecting subprocess, shell, Git/network process calls, and dangerous call names.
- Returned profile records `subprocess_started_by_profile_helper: false` and `command_executed: false`.

### 2.2 Can caller-supplied flags re-enable hooks/plugins/goals?

**Verdict:** PASS.

Evidence:

- Builder rejects any non-empty `extra_flags`.
- Validator rejects forbidden flags such as `--enable`, `--plugin`, `--plugins`, `--hook`, `--hooks`, `--goal`, `--goals`, `--config`, and `--mcp-server`.
- Validator requires `ambient_features` to preserve `hooks`, `plugins`, and `goals` as `disabled`.
- Validator requires exact argv pairs: `--disable hooks`, `--disable plugins`, and `--disable goals`.

### 2.3 Can caller-supplied flags remove required deterministic flags?

**Verdict:** PASS.

Evidence:

- Validator fails closed if `--ephemeral`, `--ignore-user-config`, `--ignore-rules`, `--json`, or `--output-last-message` is missing.
- Validator also requires `-s danger-full-access` and `-a never` with exact values.

### 2.4 Can artifact paths escape the approved relative artifact root?

**Verdict:** PASS.

Evidence:

- Artifact path validation requires a relative path under `artifacts/codex/`.
- Rejected cases cover absolute paths, parent traversal, `.git` paths, protected BLK-req paths, paths outside the root, and overlong paths.

### 2.5 Does `danger-full-access` get laundered into production sandbox authority?

**Verdict:** PASS after review-driven remediation.

Evidence:

- The builder records `sandbox_mode: danger-full-access` only alongside `sandbox_authority: CODEX_NATIVE_SANDBOX_NOT_TRUSTED_ON_THIS_HOST`.
- `production_sandbox_claimed` remains false.
- BLK-040 states `CODEX_NATIVE_SANDBOX_NOT_TRUSTED_ON_THIS_HOST` and denies production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.

Review found one under-tested edge: derivative authority field names ending in `_authority` could avoid the broad key heuristic. Remediation added RED cases for:

```text
rtm_generation_authority: APPROVED
beo_publication_allowed: true
production_sandbox_authority: ENFORCED
```

The RED test failed for `rtm_generation_authority` and `production_sandbox_authority`; the heuristic was then tightened to reject forbidden authority terms regardless of `_authority` suffix.

### 2.6 Does the sprint imply live Codex authority, BLK-pipe dispatch, BLK-test authority, BEO publication, RTM generation, or protected-vault access?

**Verdict:** PASS.

Evidence:

- BLK-040 explicitly denies live Codex execution authority, BLK-pipe dispatch authority, production BLK-test MCP authority, protected body reads/copying, active-vault scans, BEO publication, RTM generation, drift rejection, source/Git mutation, package-manager/network/model/cyber/browser tooling, and production sandbox claims.
- The builder returns false non-authority fields for the same surfaces.
- Recursive validation rejects nested authority-laundering fields and strings.

### 2.7 Are JSONL events/final messages treated as advisory only rather than canonical mutation evidence?

**Verdict:** PASS.

Evidence:

- Builder records `jsonl_events_authority: CODEX_JSONL_EVENTS_ADVISORY_ONLY`.
- Builder records `final_message_artifact_authority: CODEX_FINAL_MESSAGE_ARTIFACT_ADVISORY_ONLY`.
- BLK-040 states that Codex telemetry is not canonical proof of mutation safety, validation success, approval, trace closure, publication, or drift status.

---

## 3. Review-Driven Remediation

**Finding:** Authority-laundering heuristic was too narrow for derivative keys ending in `_authority`.

**Risk:** A future caller-mutated profile could include nested fields like `rtm_generation_authority` or `production_sandbox_authority` without failing validation, even though BLK-040 denies those surfaces.

**Fix:** Added regression cases and tightened `_looks_like_forbidden_authority_key` so forbidden authority terms are rejected regardless of suffix.

**RED evidence:**

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile.CodexDeterministicInvocationProfileTest.test_validate_rejects_production_and_live_authority_claims_even_when_nested -q
FAILED (failures=2)
```

**GREEN evidence:**

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q
----------------------------------------------------------------------
Ran 12 tests in 0.005s

OK
```

---

## 4. Final Verification Evidence

Full verification after implementation and review remediation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q
Ran 12 tests in 0.004s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
Ran 58 tests in 0.004s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 486 tests in 6.960s — OK

go test ./...
PASS

go vet ./...
PASS

git diff --check
PASS
```

---

## 5. Final Verdict

PASS after remediation. BLK-SYSTEM-038 remains inside its stated L1 fixture/local implementation plus L0 doctrine boundary. It creates deterministic command-profile fixtures and validation only. It does not authorize live Codex execution, production sandbox trust, BLK-pipe dispatch, production BLK-test MCP, BEO publication, RTM generation, drift rejection, protected BLK-req body reads, or source mutation beyond the sprint's exact authorized files.
