# BLK-SYSTEM-038 — Task 2 Outcome

**Status:** Complete
**Date:** 2026-05-09T10:46:58+10:00
**Sprint:** BLK-SYSTEM-038
**Task:** Task 2 — Deterministic profile builder fixtures

---

## 1. Objective

Implement the pure deterministic Codex invocation profile builder and validation tests for the include-now Codex CLI flags:

```text
--ephemeral
--ignore-user-config
--ignore-rules
--disable hooks
--disable plugins
--disable goals
--json
--output-last-message <relative-artifact-path>
```

The helper remains a fixture/profile builder only. It constructs dictionaries and argv arrays, validates the deterministic profile shape, and grants no execution authority.

---

## 2. Files Changed

```text
python/blk_codex_invocation_profile.py
python/test_blk_codex_invocation_profile.py
docs/outcomes/BLK-SYSTEM-038_task-002-outcome.md
```

---

## 3. RED Evidence

The Task 2 tests were written before the helper module existed. The focused test run failed for the expected missing-helper reason:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q

ImportError: Failed to import test module: test_blk_codex_invocation_profile
ModuleNotFoundError: No module named 'blk_codex_invocation_profile'
FAILED (errors=1)
```

During GREEN work, one test was corrected after root-cause inspection because it attempted to build an invalid artifact path before reaching validation. The builder is intentionally fail-closed for invalid paths, so the validation-only case now mutates a valid fixture before invoking `validate_codex_deterministic_invocation_profile`.

---

## 4. Behavior Implemented

Added `python/blk_codex_invocation_profile.py` with:

- `build_codex_deterministic_invocation_profile(...)`
- `validate_codex_deterministic_invocation_profile(profile)`

Implemented behavior:

1. deterministic argv construction beginning with `codex exec`;
2. approved model field and `-C <worktree>` inclusion;
3. `-s danger-full-access` recorded only as `CODEX_NATIVE_SANDBOX_NOT_TRUSTED_ON_THIS_HOST` host-workaround evidence;
4. `-a never`, `--ephemeral`, `--ignore-user-config`, `--ignore-rules`, `--json`, and `--output-last-message` required;
5. explicit `--disable hooks`, `--disable plugins`, and `--disable goals` ambient feature suppression;
6. bounded relative final-message artifact path under `artifacts/codex/`;
7. rejection of absolute paths, parent traversal, `.git` paths, protected BLK-req paths, and paths outside the approved artifact root;
8. rejection of caller-supplied extra Codex flags, including `--dangerously-bypass-approvals-and-sandbox`;
9. recursive rejection of production/live authority laundering fields and strings;
10. advisory telemetry fields for JSONL events and final-message artifacts;
11. explicit false non-authority flags for execution, subprocess startup, source/Git mutation, protected body reads, BEO publication, RTM generation, drift rejection, package-manager use, and network/model/cyber tooling.

---

## 5. GREEN Evidence

Focused builder tests passed:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q
----------------------------------------------------------------------
Ran 12 tests in 0.004s

OK
```

Task 2 plan verification passed:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q
PASS

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
PASS

git diff --check -- python/blk_codex_invocation_profile.py python/test_blk_codex_invocation_profile.py docs/outcomes/BLK-SYSTEM-038_task-002-outcome.md
PASS
```

---

## 6. Authority Boundary Statement

Task 2 added a pure Python fixture/helper only. It does not import or call subprocess, shell, Git, BLK-pipe, BLK-test, network clients, package managers, browser tools, model APIs, BEO tooling, RTM tooling, protected-vault readers, or Codex itself.

The profile returned by the builder explicitly records:

```text
subprocess_started_by_profile_helper: false
command_executed: false
profile_grants_execution_authority: false
production_sandbox_claimed: false
```

No live Codex execution, live tactical LLM execution, BLK-pipe dispatch, production BLK-test MCP, protected BLK-req body reads/copying, active-vault scans, source mutation outside the allowed files, BEO publication, RTM generation, drift rejection, package-manager/network/model/cyber/browser tooling, or production sandbox/firewall/host-secret-isolation claims occurred.

No protected BLK-req body reads occurred.

---

## 7. Commit

Planned task commit message:

```text
feat: add codex deterministic invocation profile fixtures
```

The exact pushed commit hash is recorded in the sprint closeout because a commit cannot contain its own final hash without changing that hash.

---

## 8. Next Task

Proceed to Task 3: hostile review, blocker remediation if needed, review doc, outcome doc, and sprint closeout.
