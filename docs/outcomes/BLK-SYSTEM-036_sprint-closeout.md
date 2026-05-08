# BLK-SYSTEM-036 — Sprint Closeout

**Status:** Complete — pending closeout commit/push at document creation
**Date:** 2026-05-08T22:06:22+10:00
**Sprint:** BLK-SYSTEM-036
**Plan:** `docs/plans/blk-system-036_git-metadata-fixture-isolated-health-check.md`
**BLK-024 alignment:** Track I / Track J, L4 local fixed-profile pilot runtime only, not L5 production authority

---

## 1. Closeout Summary

BLK-SYSTEM-036 implemented the first future-work candidate from BLK-SYSTEM-035: safe Git metadata fixture support for isolated-mode `git_status_short_branch`.

The sprint adds BLK-038 as the Git metadata fixture boundary and changes the existing advisory health-check runner so all five fixed profiles can return isolated-mode advisory evidence. `git_status_short_branch` now runs as a source-bound metadata fixture from the runner-owned isolated workspace using trusted Git, explicit `--git-dir` and `--work-tree`, and `GIT_OPTIONAL_LOCKS=0`. The implementation preserves `.git` exclusion from the isolated copy, avoids synthetic Git state, keeps source status/cache observations, and keeps PASS advisory only.

---

## 2. Delivered Artifacts

### Doctrine / planning

- `docs/plans/blk-system-036_git-metadata-fixture-isolated-health-check.md`
- `docs/BLK-038_track-i-health-check-git-metadata-fixture-boundary.md`

### Reviews

- `docs/reviews/BLK-SYSTEM-036_health-check-git-metadata-fixture-inventory.md`
- `docs/reviews/BLK-SYSTEM-036_health-check-git-metadata-fixture-hostile-review.md`

### Outcomes

- `docs/outcomes/BLK-SYSTEM-036_task-000-outcome.md`
- `docs/outcomes/BLK-SYSTEM-036_task-001-outcome.md`
- `docs/outcomes/BLK-SYSTEM-036_task-002-outcome.md`
- `docs/outcomes/BLK-SYSTEM-036_task-003-outcome.md`
- `docs/outcomes/BLK-SYSTEM-036_sprint-closeout.md`

### Code / tests

- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `python/test_active_doctrine_review_gates.py`

---

## 3. Implemented Behavior

The runner now adds these safe Git metadata fixture behaviors:

1. default `workspace_mode="source_repo"` remains compatible with existing callers;
2. `workspace_mode="isolated_copy"` is now accepted for `git_status_short_branch`;
3. isolated Git status still creates a runner-owned workspace outside the source repository;
4. `.git`, protected BLK-req paths, repo-local cache artifacts, and symlinks remain excluded from the isolated copy;
5. the Git status subprocess `cwd` is the isolated workspace, not the source repository;
6. the Git status argv uses trusted Git with explicit `--git-dir <source>/.git` and `--work-tree <source>`;
7. `GIT_OPTIONAL_LOCKS=0` is set for the metadata fixture command;
8. result evidence reports `GIT_STATUS_ISOLATED_METADATA_FIXTURE`, `SOURCE_GIT_METADATA_READ_ONLY`, `git_optional_locks_disabled=True`, `git_dir_and_work_tree_explicit=True`, and no `.git` copy / synthetic history / clone-worktree setup;
9. source repository status/cache changes still block advisory PASS;
10. all five fixed profiles now pass source-mode and isolated-mode live smokes;
11. health-check PASS remains advisory and grants no production authority.

---

## 4. Hostile Review Outcome

Hostile review status: PASS.

Closed findings:

1. `.git` copying or synthetic Git state risk;
2. Git metadata command source-cwd risk;
3. optional lock / Git mutation risk;
4. profile ID or command-surface expansion risk;
5. source-change blocking risk;
6. production sandbox / production authority overclaim risk.

---

## 5. Verification

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner
Ran 29 tests in 0.449s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates
Ran 56 tests in 0.005s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 467 tests in 6.932s
OK

go test ./...
PASS across all packages

go vet ./...
PASS

Spec traceability gate
PASS

Safety/docs gate
PASS

git diff --check
PASS
```

Live profile smoke:

```text
SOURCE MODE
git_status_short_branch PASS_ADVISORY_ONLY 0 source_repo SOURCE_REPOSITORY False False
active_doctrine_gate PASS_ADVISORY_ONLY 0 source_repo SOURCE_REPOSITORY False False
python_unittest_discovery PASS_ADVISORY_ONLY 0 source_repo SOURCE_REPOSITORY False False
go_test_all PASS_ADVISORY_ONLY 0 source_repo SOURCE_REPOSITORY False False
go_vet_all PASS_ADVISORY_ONLY 0 source_repo SOURCE_REPOSITORY False False

ISOLATED MODE
git_status_short_branch PASS_ADVISORY_ONLY 0 isolated_copy GIT_STATUS_ISOLATED_METADATA_FIXTURE GIT_STATUS_ISOLATED_METADATA_FIXTURE True False False False
active_doctrine_gate PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO NOT_USED False False False False
python_unittest_discovery PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO NOT_USED False False False False
go_test_all PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO NOT_USED False False False False
go_vet_all PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO NOT_USED False False False False
```

---

## 6. Authority Boundary Preserved

BLK-SYSTEM-036 does not authorize:

- production health-check service/daemon authority;
- arbitrary shell or caller-supplied commands;
- new health-check profile IDs;
- network/API/model/cyber tooling;
- package-manager execution or dependency installation;
- `.git` copying, synthetic Git history, clone setup, worktree setup, staging, committing, reverting, or Git/source repair;
- protected BLK-req body reads/copying/parsing/hashing/summarizing;
- active-vault path scans beyond existing Git status metadata;
- runtime active-vault comparisons;
- BLK-pipe dispatch or validation authority;
- production BLK-test MCP or new BLK-test smoke authority;
- BEO publication;
- signer/storage/public-ledger mutation;
- runtime RTM generation;
- RTM drift rejection or final drift decisions;
- production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux enforcement;
- network firewall enforcement;
- host-secret isolation;
- L5 production health-check authority.

PASS remains advisory operator context only.

---

## 7. Commit Chain

Known sprint commits before final closeout:

- `f05bf68 docs: plan blk-system sprint 036 git metadata fixture`
- `3b61a57 docs: define blk038 git metadata fixture boundary`
- `62dab34 docs: record blk-system sprint 036 task 1 outcome`
- `3f16400 feat: add isolated git status metadata fixture`
- `aac703d docs: record blk-system sprint 036 task 2 outcome`

Final closeout commit is pending at document creation and will be recorded by Git history after exact-path staging and push.

---

## 8. Future Work

Potential future BLK-024-aligned work requires a new sprint and explicit scope:

1. production health-check authority proposal only after separate doctrine, approval provenance, monitoring, rollback, and hostile review;
2. deeper OS-level sandbox/cgroup/namespace/network policy design only if explicitly approved and still separated from BLK-pipe, BLK-test, BEO, RTM, and drift authority;
3. operator escalation package improvements that keep health-check evidence advisory-only;
4. broader BLK-024 Track H or Track I continuation only through a fresh plan and authority boundary.
