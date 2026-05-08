# BLK-SYSTEM-036 — Task 2 Outcome

**Status:** Complete — pending outcome commit/push at document creation
**Date:** 2026-05-08T22:04:10+10:00
**Task:** Implement isolated-mode `git_status_short_branch` metadata fixture with TDD
**Implementation Commit:** `3f16400 feat: add isolated git status metadata fixture`
**Remote:** implementation pushed to `origin/main`

---

## 1. Objective

Replace the BLK-SYSTEM-035 isolated-mode rejection for `git_status_short_branch` with a safe source-bound Git metadata fixture command shape that runs from the isolated workspace, keeps `.git` excluded from the copy, preserves advisory-only PASS semantics, and does not mutate Git/source state.

---

## 2. Files Added/Changed

- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `docs/outcomes/BLK-SYSTEM-036_task-002-outcome.md`

---

## 3. Behavior Implemented

Task 2 implemented isolated-mode Git status metadata fixture behavior for the existing `git_status_short_branch` profile:

- `workspace_mode="isolated_copy"` no longer raises for `git_status_short_branch`;
- the runner still creates a runner-owned isolated workspace outside `REPO_ROOT`;
- the isolated copy still excludes `.git`, protected BLK-req paths, repo-local cache artifacts, and symlinks;
- the Git status process runs with `cwd` set to the isolated workspace;
- the actual fixed argv is `git --git-dir <source>/.git --work-tree <source> status --short --branch` with a trusted absolute Git executable;
- `GIT_OPTIONAL_LOCKS=0` is set for the metadata command;
- `shell=False`, bounded output, redaction, startup failure handling, timeout cleanup, source status/cache observations, and cleanup observations remain in force;
- result evidence includes `GIT_STATUS_ISOLATED_METADATA_FIXTURE`, `SOURCE_GIT_METADATA_READ_ONLY`, explicit `--git-dir`/`--work-tree` flags, no `.git` copy, no synthetic history, and no clone/worktree setup;
- health-check PASS remains advisory and grants no production authority.

---

## 4. TDD Evidence

### 4.1 RED

Focused tests were added first and failed against the BLK-SYSTEM-035 implementation because isolated `git_status_short_branch` still raised before subprocess startup:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  python.test_blk_operator_health_check_runner.AdvisoryHealthCheckRunnerTest.test_isolated_git_status_uses_source_bound_metadata_fixture_without_copying_git \
  python.test_blk_operator_health_check_runner.AdvisoryHealthCheckRunnerTest.test_isolated_git_status_metadata_fixture_still_blocks_source_change -v

ERROR: test_isolated_git_status_uses_source_bound_metadata_fixture_without_copying_git
ValueError: git_status_short_branch is source-repository mode only

ERROR: test_isolated_git_status_metadata_fixture_still_blocks_source_change
ValueError: git_status_short_branch is source-repository mode only

FAILED (errors=2)
```

### 4.2 GREEN

After implementation, the focused metadata-fixture tests passed:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  python.test_blk_operator_health_check_runner.AdvisoryHealthCheckRunnerTest.test_isolated_git_status_uses_source_bound_metadata_fixture_without_copying_git \
  python.test_blk_operator_health_check_runner.AdvisoryHealthCheckRunnerTest.test_isolated_git_status_metadata_fixture_still_blocks_source_change -v

Ran 2 tests in 0.067s
OK
```

The full runner suite also passed after a readability refactor:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner
Ran 29 tests in 0.452s
OK
```

---

## 5. Review Results

Deterministic local review gates passed:

- Spec gate confirmed fixed `--git-dir`/`--work-tree` argv, isolated `cwd`, `GIT_OPTIONAL_LOCKS=0`, `.git` copy exclusion, metadata fixture markers, source-change blocking, and advisory-only flags.
- Safety gate checked for no `shell=True`, no `git clone`, no `git worktree`, no `git init`, no `git add`, no `git commit`, no `git push`, no `git reset`, no `git checkout`, no `git clean`, and no `git revert` string patterns in the runtime source.
- Source hygiene gate confirmed no trailing whitespace in touched Python files.
- No live Codex/tactical-engine/model reviewer agents were used.

---

## 6. Final Verification

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner
Ran 29 tests in 0.452s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates
Ran 56 tests in 0.005s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 467 tests in 6.927s
OK

go test ./...
PASS across all packages

go vet ./...
PASS

Live source-mode smoke:
git_status_short_branch PASS_ADVISORY_ONLY 0 source_repo SOURCE_REPOSITORY False False
active_doctrine_gate PASS_ADVISORY_ONLY 0 source_repo SOURCE_REPOSITORY False False
python_unittest_discovery PASS_ADVISORY_ONLY 0 source_repo SOURCE_REPOSITORY False False
go_test_all PASS_ADVISORY_ONLY 0 source_repo SOURCE_REPOSITORY False False
go_vet_all PASS_ADVISORY_ONLY 0 source_repo SOURCE_REPOSITORY False False

Live isolated-mode smoke:
git_status_short_branch PASS_ADVISORY_ONLY 0 isolated_copy GIT_STATUS_ISOLATED_METADATA_FIXTURE GIT_STATUS_ISOLATED_METADATA_FIXTURE False False
active_doctrine_gate PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO NOT_USED False False
python_unittest_discovery PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO NOT_USED False False
go_test_all PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO NOT_USED False False
go_vet_all PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO NOT_USED False False

Deterministic safety/source hygiene gate
PASS

git diff --check
PASS
```

Implementation commit and push:

```text
3f16400 feat: add isolated git status metadata fixture
3f16400f6424fe2625bfb834af89e0dadc7887d9 refs/heads/main
```

---

## 7. Deviations / Notes

- The profile ID set remains unchanged. No `git_status_isolated` or other new profile ID was added.
- The Git metadata fixture uses source-bound Git metadata via explicit `--git-dir` and `--work-tree`; it does not copy `.git` into the isolated workspace.
- Python cache artifacts were removed before exact-path staging.
- The initial smoke script missed `PYTHONPATH=python` for a direct import and failed with `ModuleNotFoundError`; this was a command invocation issue, not a product failure. The corrected smoke passed.

---

## 8. Next Task

Task 3 — Hostile review and closeout.
