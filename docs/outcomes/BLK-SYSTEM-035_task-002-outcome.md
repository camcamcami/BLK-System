# BLK-SYSTEM-035 — Task 002 Outcome

**Status:** Complete — pending commit/push at document creation
**Date:** 2026-05-08T21:10:00+10:00
**Sprint:** BLK-SYSTEM-035
**Task:** 002 — Implement optional isolated-workspace runner mode with TDD

---

## 1. Summary

Implemented optional `workspace_mode="isolated_copy"` support for eligible non-Git advisory health-check profiles.

The implementation preserves default `workspace_mode="source_repo"` behavior for existing callers and keeps the five BLK-035 fixed profile IDs unchanged.

---

## 2. Files Changed

```text
python/blk_operator_health_check_runner.py
python/test_blk_operator_health_check_runner.py
docs/outcomes/BLK-SYSTEM-035_task-002-outcome.md
```

---

## 3. Implemented Behavior

The runner now supports:

1. `workspace_mode="source_repo"` default behavior, preserving existing source-repository execution semantics;
2. `workspace_mode="isolated_copy"` for eligible non-Git profiles;
3. filtered isolated workspace copies under runner-owned temp directories outside `REPO_ROOT`;
4. copy exclusion for `.git`, `docs/active`, `docs/requirements`, `docs/use_cases`, `.pytest_cache`, `__pycache__`, `.pyc`, and symlinks;
5. isolated-mode `cwd` outside the source repository;
6. isolated-mode `PYTHONPATH` pointing to the isolated workspace's `python/` directory;
7. source-repository Git status/cache observation before and after isolated execution;
8. advisory PASS blocking if source-repository status/cache changes during isolated execution;
9. explicit result fields for `workspace_mode`, `execution_workspace`, `source_repo_is_execution_cwd`, `isolated_workspace_path_inside_repo`, `isolated_workspace_removed`, `source_repo_status_changed`, `source_repo_cache_artifacts_changed`, and isolated-copy exclusions;
10. fail-closed rejection of `git_status_short_branch` in isolated mode because `.git` is deliberately excluded;
11. marked isolated-workspace support for copied runner tests that execute without `.git` in the copied workspace.

---

## 4. RED/GREEN Evidence

RED was observed before implementation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner.AdvisoryHealthCheckRunnerTest.test_isolated_workspace_mode_executes_non_git_profile_outside_source_repo python.test_blk_operator_health_check_runner.AdvisoryHealthCheckRunnerTest.test_isolated_workspace_copy_excludes_git_protected_paths_and_python_cache_artifacts python.test_blk_operator_health_check_runner.AdvisoryHealthCheckRunnerTest.test_git_status_profile_fails_closed_in_isolated_workspace_mode_before_subprocess python.test_blk_operator_health_check_runner.AdvisoryHealthCheckRunnerTest.test_source_repo_change_during_isolated_workspace_run_blocks_advisory_pass
FAILED (errors=4)
TypeError: run_health_check() got an unexpected keyword argument 'workspace_mode'
AttributeError: module 'blk_operator_health_check_runner' has no attribute '_copy_isolated_workspace'
```

A live isolated `python_unittest_discovery` smoke initially failed because copied runner tests expected a `.git` directory. A regression was added first:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner.AdvisoryHealthCheckRunnerTest.test_marked_isolated_workspace_allows_copied_runner_without_git_directory
FAILED (errors=1)
ValueError: repo_root is not a Git repository
```

GREEN verification:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner.AdvisoryHealthCheckRunnerTest.test_isolated_workspace_mode_executes_non_git_profile_outside_source_repo python.test_blk_operator_health_check_runner.AdvisoryHealthCheckRunnerTest.test_isolated_workspace_copy_excludes_git_protected_paths_and_python_cache_artifacts python.test_blk_operator_health_check_runner.AdvisoryHealthCheckRunnerTest.test_git_status_profile_fails_closed_in_isolated_workspace_mode_before_subprocess python.test_blk_operator_health_check_runner.AdvisoryHealthCheckRunnerTest.test_source_repo_change_during_isolated_workspace_run_blocks_advisory_pass
Ran 4 tests in 0.069s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner.AdvisoryHealthCheckRunnerTest.test_marked_isolated_workspace_allows_copied_runner_without_git_directory
Ran 1 test in 0.001s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner
Ran 24 tests in 0.326s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates
Ran 55 tests in 0.005s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 461 tests in 6.789s
OK

go test ./...
PASS across all packages

go vet ./...
exit 0

git diff --check
exit 0
```

---

## 5. Live Profile Smoke

Source mode smoke of all five fixed profiles:

```text
git_status_short_branch PASS_ADVISORY_ONLY 0 source_repo False False True PROCESS_GROUP_KILL_NOT_NEEDED
active_doctrine_gate PASS_ADVISORY_ONLY 0 source_repo False False True PROCESS_GROUP_KILL_NOT_NEEDED
python_unittest_discovery PASS_ADVISORY_ONLY 0 source_repo False False True PROCESS_GROUP_KILL_NOT_NEEDED
go_test_all PASS_ADVISORY_ONLY 0 source_repo False False True PROCESS_GROUP_KILL_NOT_NEEDED
go_vet_all PASS_ADVISORY_ONLY 0 source_repo False False True PROCESS_GROUP_KILL_NOT_NEEDED
```

Isolated mode smoke of eligible non-Git profiles:

```text
active_doctrine_gate PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO False False True
python_unittest_discovery PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO False False True
go_test_all PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO False False True
go_vet_all PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO False False True
```

---

## 6. Authority Boundary Preserved

Task 002 does not authorize new profile IDs, arbitrary shell, caller-supplied commands, network/model/cyber/package tooling, `.git` copying, protected BLK-req path copying or body reads, active-vault scan, Git/source mutation or repair, BLK-pipe dispatch, production BLK-test MCP, BEO publication, runtime RTM generation, drift rejection, production sandbox/cgroup/VM/network/host-secret isolation claims, or production health-check authority.

PASS remains advisory operator context only.

---

## 7. Exact Paths for Commit

```text
python/blk_operator_health_check_runner.py
python/test_blk_operator_health_check_runner.py
docs/outcomes/BLK-SYSTEM-035_task-002-outcome.md
```
