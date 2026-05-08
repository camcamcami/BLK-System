# BLK-SYSTEM-035 — Sprint Closeout

**Status:** Complete — pending commit/push at document creation
**Date:** 2026-05-08T21:24:23+10:00
**Sprint:** BLK-SYSTEM-035
**Plan:** `docs/plans/blk-system-035_health-check-isolated-workspace-execution-boundary.md`
**BLK-024 alignment:** Track I / Track J, L4 local fixed-profile pilot runtime only, not L5 production authority

---

## 1. Closeout Summary

BLK-SYSTEM-035 implemented the next logical sprint after BLK-SYSTEM-034: optional isolated-workspace execution for the advisory health-check runner.

The sprint adds BLK-037 as the isolated-workspace execution boundary and implements `workspace_mode="isolated_copy"` for eligible non-Git fixed profiles. It preserves default source-repository behavior, preserves exactly the five BLK-035 fixed profile IDs, excludes `.git` and protected BLK-req path families from isolated copies, observes source repository status/cache before and after isolated execution, blocks advisory PASS on cleanup/source-change failures, and keeps PASS advisory only.

---

## 2. Delivered Artifacts

### Doctrine / planning

- `docs/plans/blk-system-035_health-check-isolated-workspace-execution-boundary.md`
- `docs/BLK-037_track-i-health-check-isolated-workspace-execution-boundary.md`

### Reviews

- `docs/reviews/BLK-SYSTEM-035_health-check-isolated-workspace-inventory.md`
- `docs/reviews/BLK-SYSTEM-035_health-check-isolated-workspace-hostile-review.md`

### Outcomes

- `docs/outcomes/BLK-SYSTEM-035_task-000-outcome.md`
- `docs/outcomes/BLK-SYSTEM-035_task-001-outcome.md`
- `docs/outcomes/BLK-SYSTEM-035_task-002-outcome.md`
- `docs/outcomes/BLK-SYSTEM-035_task-003-outcome.md`
- `docs/outcomes/BLK-SYSTEM-035_sprint-closeout.md`

### Code / tests

- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `python/test_active_doctrine_review_gates.py`

---

## 3. Implemented Behavior

The runner now adds these isolated-workspace behaviors:

1. `workspace_mode="source_repo"` remains default and preserves existing behavior;
2. `workspace_mode="isolated_copy"` creates a runner-owned filtered workspace outside the source repository;
3. eligible non-Git profiles execute with `cwd` set to the isolated workspace;
4. isolated-mode `PYTHONPATH` points to the isolated workspace's `python/` directory;
5. isolated copies exclude `.git`, protected BLK-req path families, repo-local cache artifacts, `.pytest_cache`, and symlinks;
6. `git_status_short_branch` fails closed for isolated mode before subprocess startup;
7. source repository Git status and repo-local Python cache snapshots are observed before and after isolated execution;
8. source repository status/cache changes block advisory PASS;
9. cleanup failure returns bounded `BLOCKED_ADVISORY_ONLY` evidence and recomputed final evidence hash;
10. copied full-discovery selftests use a skip marker for `.git`-root assumptions rather than a production root-validation bypass;
11. result evidence exposes `workspace_mode`, `execution_workspace`, source/isolated path flags, cleanup flags, copy exclusions, and explicit non-claims.

---

## 4. Hostile Review Outcome

Hostile review status: PASS after remediation.

Closed findings:

1. cleanup failure escaped rather than returning bounded blocked evidence;
2. inherited `.git`-less copied-runner allowance weakened the Git/source-root boundary;
3. cleanup failure over process-level FAIL did not force final blocked evidence;
4. cleanup-failure result had stale `evidence_hash` after final mutation.

All blockers were remediated with tests.

---

## 5. Verification

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner
Ran 28 tests in 0.385s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates
Ran 55 tests in 0.005s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 465 tests in 6.858s
OK

go test ./...
PASS across all packages

go vet ./...
exit 0

git diff --check
exit 0
```

Live profile smoke:

```text
SOURCE MODE
git_status_short_branch PASS_ADVISORY_ONLY 0 source_repo False False True PROCESS_GROUP_KILL_NOT_NEEDED
active_doctrine_gate PASS_ADVISORY_ONLY 0 source_repo False False True PROCESS_GROUP_KILL_NOT_NEEDED
python_unittest_discovery PASS_ADVISORY_ONLY 0 source_repo False False True PROCESS_GROUP_KILL_NOT_NEEDED
go_test_all PASS_ADVISORY_ONLY 0 source_repo False False True PROCESS_GROUP_KILL_NOT_NEEDED
go_vet_all PASS_ADVISORY_ONLY 0 source_repo False False True PROCESS_GROUP_KILL_NOT_NEEDED

ISOLATED MODE
active_doctrine_gate PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO False False True
python_unittest_discovery PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO False False True
go_test_all PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO False False True
go_vet_all PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO False False True
```

---

## 6. Authority Boundary Preserved

BLK-SYSTEM-035 does not authorize:

- production health-check service/daemon authority;
- arbitrary shell or caller-supplied commands;
- new health-check profile IDs;
- network/API/model/cyber tooling;
- package-manager execution or dependency installation;
- `.git` copying, synthetic Git history, clone setup, worktree setup, staging, committing, or Git repair for isolated health checks;
- protected BLK-req body reads/copying/parsing/hashing/summarizing;
- active-vault path scans or runtime active-vault comparisons;
- BLK-pipe dispatch or validation authority;
- production BLK-test MCP or new BLK-test smoke authority;
- BEO publication;
- signer/storage/public-ledger mutation;
- runtime RTM generation;
- RTM drift rejection or final drift decisions;
- Git/source repair or cleanup authority;
- production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux enforcement;
- network firewall enforcement;
- host-secret isolation;
- L5 production health-check authority.

PASS remains advisory operator context only.

---

## 7. Commit Chain

Known sprint commits before final closeout:

- `75a3cad docs: plan blk-system sprint 035 isolated health-check`
- `ce67dfc docs: define blk037 isolated health-check boundary`
- `4e9de32 feat: add isolated health-check workspace mode`

Final closeout commit is pending at document creation and will be recorded by Git history after exact-path staging and push.

---

## 8. Future Work

Potential future BLK-024-aligned work requires a new sprint and explicit scope:

1. safe Git-metadata fixture design for isolated `git_status_short_branch`, if source-mode Git profile isolation is required;
2. production health-check authority proposal only after separate doctrine, approval provenance, monitoring, rollback, and hostile review;
3. deeper OS-level sandbox/cgroup/namespace/network policy design only if explicitly approved and still separated from BLK-pipe, BLK-test, BEO, RTM, and drift authority.
