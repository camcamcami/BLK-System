# BLK-SYSTEM-038 — Sprint Closeout

**Status:** Complete
**Date:** 2026-05-09T10:49:46+10:00
**Sprint:** BLK-SYSTEM-038 — Codex deterministic invocation profile

---

## 1. Summary

BLK-SYSTEM-038 defined and implemented a deterministic local Codex tactical-engine invocation profile fixture for future BLK/Hermes use. The sprint captured the include-now Codex CLI flags and non-authority evidence shape without granting live Codex execution authority.

Final state includes:

1. `docs/BLK-040_codex-deterministic-invocation-profile-boundary.md` — active boundary document for fixture-only profile construction.
2. `python/blk_codex_invocation_profile.py` — pure profile builder/validator that constructs dictionaries and argv arrays only.
3. `python/test_blk_codex_invocation_profile.py` — tests proving deterministic flags, ambient-feature disables, bounded relative artifact paths, no subprocess startup, advisory telemetry, and authority-laundering rejection.
4. `python/test_active_doctrine_review_gates.py` — persistent BLK-040 active-doctrine gate.
5. Task outcomes, hostile review, and this closeout document.

---

## 2. Final Commits

```text
79a9886 docs: plan blk-system sprint 038 codex invocation profile
061125b docs: define blk040 codex invocation boundary
49dc69b feat: add codex deterministic invocation profile fixtures
<pending at document write time> docs: close blk-system sprint 038 codex invocation profile
```

The final closeout commit hash is reported by the controller after push because a commit cannot contain its own final hash without changing that hash.

---

## 3. Task Outcomes

```text
docs/outcomes/BLK-SYSTEM-038_task-000-outcome.md
docs/outcomes/BLK-SYSTEM-038_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-038_task-002-outcome.md
docs/outcomes/BLK-SYSTEM-038_task-003-outcome.md
```

Task 0 published the plan.

Task 1 added BLK-040 and the active doctrine gate.

Task 2 added the pure deterministic Codex invocation profile builder and validation tests.

Task 3 performed hostile review, remediated a derivative authority-field gap, and closed the sprint.

---

## 4. Hostile Review Verdict

Final hostile review verdict: **PASS after remediation**.

The review found one blocker-class edge before final closeout: the authority-laundering heuristic rejected explicit forbidden keys and forbidden string markers, but derivative keys ending in `_authority` were under-tested. Remediation added RED cases for `rtm_generation_authority`, `beo_publication_allowed`, and `production_sandbox_authority`, then tightened the heuristic so forbidden authority terms fail closed regardless of suffix.

Review document:

```text
docs/reviews/BLK-SYSTEM-038_codex-deterministic-invocation-profile-hostile-review.md
```

---

## 5. Final Verification Suite

Final verification passed:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q
Ran 12 tests in 0.004s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
Ran 58 tests in 0.004s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 486 tests in 6.960s — OK

export PATH="$HOME/.local/bin:$PATH"; go test ./...
PASS

export PATH="$HOME/.local/bin:$PATH"; go vet ./...
PASS

git diff --check
PASS
```

---

## 6. Final Repository Status

Repository status after Task 2 push and before Task 3 review/remediation changes:

```text
## main...origin/main
```

Expected repository status after final closeout push:

```text
## main...origin/main
```

---

## 7. Authority Boundary

BLK-SYSTEM-038 did **not** authorize live Codex execution, reusable runtime dispatch, production sandbox trust, BLK-pipe dispatch, production BLK-test MCP, authoritative BEO publication, RTM generation, drift rejection, protected BLK-req vault body reads/copying/parsing/hashing/summarizing, active-vault scans, source mutation outside exact authorized sprint files, package-manager/network/model/cyber/browser tooling, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.

BLK-SYSTEM-038 created only:

```text
CODEX_DETERMINISTIC_INVOCATION_PROFILE_FIXTURE_ONLY
CODEX_AMBIENT_FEATURES_DISABLED
CODEX_PROFILE_BUILDER_STARTS_NO_SUBPROCESS
CODEX_JSONL_EVENTS_ADVISORY_ONLY
CODEX_FINAL_MESSAGE_ARTIFACT_ADVISORY_ONLY
CODEX_NATIVE_SANDBOX_NOT_TRUSTED_ON_THIS_HOST
CODEX_PROFILE_GRANTS_NO_EXECUTION_AUTHORITY
```

Codex JSONL events and final-message artifacts remain advisory telemetry only. Git diff, BLK-pipe enforcement, separately authorized BLK-test evidence, and hostile review remain the canonical evidence surfaces for future execution plans.

No protected BLK-req body reads occurred during BLK-SYSTEM-038 execution.

---

## 8. Future Work

Future work may wire this deterministic profile into a later explicit dispatch plan only if that plan separately defines approval provenance, file-boundary enforcement, sandbox/containment evidence, validation gates, telemetry storage, hostile review, failure ceilings, rollback behavior, and operator escalation. BLK-040 alone grants no execution authority.
