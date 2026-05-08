# BLK-SYSTEM-036 — Health-Check Git Metadata Fixture Hostile Review

**Status:** PASS after deterministic hostile review
**Date:** 2026-05-08T22:06:22+10:00
**Sprint:** BLK-SYSTEM-036
**Plan:** `docs/plans/blk-system-036_git-metadata-fixture-isolated-health-check.md`
**Boundary:** `docs/BLK-038_track-i-health-check-git-metadata-fixture-boundary.md`

---

## 1. Review Scope

This hostile review covered the BLK-SYSTEM-036 safe Git metadata fixture work:

- `docs/plans/blk-system-036_git-metadata-fixture-isolated-health-check.md`
- `docs/BLK-038_track-i-health-check-git-metadata-fixture-boundary.md`
- `docs/reviews/BLK-SYSTEM-036_health-check-git-metadata-fixture-inventory.md`
- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `python/test_active_doctrine_review_gates.py`
- BLK-SYSTEM-036 task outcome documents

Review lens: BLK-024 Track I / Track J, BLK-034, BLK-035, BLK-036, BLK-037, BLK-038, and the sprint plan's no-adjacent-authority exclusions.

---

## 2. Finding Register

| Finding ID | Severity | Challenge | Status |
| --- | --- | --- | --- |
| BLK-SYSTEM-036-HR-001 | High | Isolated `git_status_short_branch` could copy `.git` or synthesize Git state to make status work. | CLOSED |
| BLK-SYSTEM-036-HR-002 | High | Git metadata command could run from the source repository, weakening the isolated-cwd claim. | CLOSED |
| BLK-SYSTEM-036-HR-003 | Medium | Git status could acquire optional locks or otherwise mutate Git metadata. | CLOSED |
| BLK-SYSTEM-036-HR-004 | High | Implementation could add a new profile ID or caller-supplied command surface. | CLOSED |
| BLK-SYSTEM-036-HR-005 | High | Source changes during metadata fixture execution could still return advisory PASS. | CLOSED |
| BLK-SYSTEM-036-HR-006 | Medium | Result evidence could overclaim production sandbox, network firewall, host-secret isolation, or production health-check authority. | CLOSED |

---

## 3. Findings Detail

### BLK-SYSTEM-036-HR-001 — CLOSED

The isolated workspace copy still excludes `.git`, and the runtime result reports `dot_git_copied_to_isolated_workspace=False`. The Git metadata fixture uses explicit `--git-dir <source>/.git` and `--work-tree <source>` instead of copying `.git`, creating synthetic history, cloning, initializing, or creating a worktree.

Evidence:

- `test_isolated_git_status_uses_source_bound_metadata_fixture_without_copying_git`
- `test_isolated_workspace_copy_excludes_git_protected_paths_and_python_cache_artifacts`
- deterministic safety gate banning `git clone`, `git worktree`, and `git init` strings in runtime source

### BLK-SYSTEM-036-HR-002 — CLOSED

The metadata command executes with `cwd` set to the runner-owned isolated workspace. The test asserts `cwd != ROOT`, `ROOT` is not in the captured `cwd`, and result evidence reports `git_status_cwd_is_isolated_workspace=True`.

### BLK-SYSTEM-036-HR-003 — CLOSED

The metadata command sets `GIT_OPTIONAL_LOCKS=0`, and the result evidence reports `git_optional_locks_disabled=True`. Existing source status snapshot behavior also preserves `GIT_OPTIONAL_LOCKS=0`.

### BLK-SYSTEM-036-HR-004 — CLOSED

The profile registry remains exactly the five BLK-035 profile IDs. No `git_status_isolated` or caller-supplied profile ID was added. Existing unknown-profile and caller-supplied command tests remain green.

### BLK-SYSTEM-036-HR-005 — CLOSED

`test_isolated_git_status_metadata_fixture_still_blocks_source_change` proves source repository status changes still route to `BLOCKED_ADVISORY_ONLY`, not PASS.

### BLK-SYSTEM-036-HR-006 — CLOSED

BLK-038 and runtime evidence preserve advisory-only language and explicit non-claims:

- `health_check_pass_grants_authority=False`
- `production_authority_granted=False`
- `production_sandbox_enforced="NOT_ENFORCED_BY_PILOT"`
- `network_firewall_enforced="NOT_ENFORCED_BY_PILOT"`
- `host_secret_isolation_enforced="NOT_ENFORCED_BY_PILOT"`

---

## 4. Deterministic Review Gates

```text
Spec traceability gate: PASS
- required BLK-SYSTEM-036 docs and outcomes exist
- runtime source contains GIT_STATUS_ISOLATED_METADATA_FIXTURE
- runtime source contains SOURCE_GIT_METADATA_READ_ONLY
- runtime source contains GIT_OPTIONAL_LOCKS
- runtime source contains --git-dir / --work-tree
- runtime source exposes dot_git_copied_to_isolated_workspace=False
- runtime source exposes synthetic_git_history_created=False
- runtime source exposes clone_or_worktree_setup_used=False
- no git_status_isolated profile ID appears

Safety/docs gate: PASS
- no shell=True in runtime source
- no git clone/worktree/init/add/commit/push/reset/checkout/clean/revert string patterns in runtime source
- Markdown fences balanced
- no trailing whitespace in touched runtime/doc files
```

---

## 5. Verification Evidence

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

Source-mode smoke:
git_status_short_branch PASS_ADVISORY_ONLY 0 source_repo SOURCE_REPOSITORY False False
active_doctrine_gate PASS_ADVISORY_ONLY 0 source_repo SOURCE_REPOSITORY False False
python_unittest_discovery PASS_ADVISORY_ONLY 0 source_repo SOURCE_REPOSITORY False False
go_test_all PASS_ADVISORY_ONLY 0 source_repo SOURCE_REPOSITORY False False
go_vet_all PASS_ADVISORY_ONLY 0 source_repo SOURCE_REPOSITORY False False

Isolated-mode smoke:
git_status_short_branch PASS_ADVISORY_ONLY 0 isolated_copy GIT_STATUS_ISOLATED_METADATA_FIXTURE GIT_STATUS_ISOLATED_METADATA_FIXTURE True False False False
active_doctrine_gate PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO NOT_USED False False False False
python_unittest_discovery PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO NOT_USED False False False False
go_test_all PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO NOT_USED False False False False
go_vet_all PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO NOT_USED False False False False

git diff --check
PASS
```

---

## 6. Verdict

PASS. BLK-SYSTEM-036 safely closes the BLK-SYSTEM-035 gap for isolated-mode `git_status_short_branch` evidence without copying `.git`, adding profile IDs, creating synthetic Git state, running caller-supplied commands, or granting adjacent authority.

The sprint remains advisory-only L4 local pilot runtime for fixed profiles. It is not production health-check authority, not a production sandbox, not network firewall enforcement, not host-secret isolation, not BLK-pipe dispatch, not production BLK-test MCP, not BEO publication, not RTM generation, and not drift rejection.

---

## 7. Future Work

Future work requires a separate sprint and explicit scope. Safe candidates include:

1. production health-check authority proposal only with approval provenance, monitoring, rollback, and hostile review;
2. deeper OS-level sandbox/cgroup/namespace/network policy design if explicitly approved;
3. broader operator escalation package improvements that keep health-check evidence advisory-only.
