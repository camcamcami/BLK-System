# BLK-SYSTEM-036 — Health-Check Git Metadata Fixture Inventory

**Status:** Complete
**Date:** 2026-05-08T21:58:00+10:00
**Sprint:** BLK-SYSTEM-036
**Boundary:** `docs/BLK-038_track-i-health-check-git-metadata-fixture-boundary.md`

---

## 1. Inventory Summary

BLK-SYSTEM-036 follows BLK-SYSTEM-035 isolated-workspace execution by addressing the one fixed profile that remained source-repository mode only: `git_status_short_branch`.

The safe design is a Git metadata fixture, not `.git` copying and not synthetic repository creation. The runner may create an isolated workspace outside `REPO_ROOT`, keep `.git` excluded from that copy, and run the trusted Git binary from the isolated workspace with explicit `--git-dir <source>/.git` and `--work-tree <source>` arguments plus `GIT_OPTIONAL_LOCKS=0`.

---

## 2. Existing Preserved Surfaces

The sprint preserves:

- five fixed profile IDs only: `git_status_short_branch`, `active_doctrine_gate`, `python_unittest_discovery`, `go_test_all`, `go_vet_all`;
- trusted absolute executable resolution;
- no arbitrary shell or caller-supplied argv;
- output byte limits and excerpts;
- secret redaction;
- runner-owned `TMPDIR`, `TMP`, `TEMP`, and `PYTHONPYCACHEPREFIX` outside the source repository;
- source repository Git status before/after observation;
- source repository repo-local `__pycache__` / `.pyc` observation;
- process-group timeout cleanup;
- bounded startup failure evidence;
- advisory-only PASS/FAIL/BLOCKED vocabulary;
- BLK-037 isolated copy exclusions for `.git`, protected BLK-req paths, cache artifacts, and symlinks.

---

## 3. Git Metadata Fixture Design Surface

Task 2 should implement isolated-mode `git_status_short_branch` without adding a new profile ID. Expected behavior:

1. default source-repository mode remains unchanged for all callers;
2. `workspace_mode="isolated_copy"` for `git_status_short_branch` creates a runner-owned isolated workspace outside `REPO_ROOT`;
3. the isolated workspace does not contain `.git`;
4. the fixed Git command executes with `cwd` set to the isolated workspace;
5. the fixed Git command uses explicit source repository metadata pointers: `--git-dir <source>/.git` and `--work-tree <source>`;
6. `GIT_OPTIONAL_LOCKS=0` is set;
7. `shell=False` is preserved;
8. output remains bounded and redacted;
9. before/after source status/cache observations still block advisory PASS on source change;
10. result evidence states that this is `GIT_STATUS_ISOLATED_METADATA_FIXTURE`, `SOURCE_GIT_METADATA_READ_ONLY`, and `DOT_GIT_NOT_COPIED`.

---

## 4. Forbidden Implementation Shapes

The implementation must not:

- add a new profile ID;
- copy `.git`;
- create a synthetic Git history;
- run `git clone`, `git worktree`, `git init`, `git add`, `git commit`, `git push`, `git reset`, `git checkout`, `git clean`, `git revert`, `git merge`, `git rebase`, `git switch`, or `git restore`;
- run a shell or caller-supplied argv;
- read, copy, parse, hash, summarize, or compare protected BLK-req bodies;
- scan active-vault bodies for RTM or drift purposes;
- call BLK-pipe, BLK-test MCP, live Codex, tactical LLMs, model APIs, network services, package managers, browser automation, or cyber tools;
- claim production sandbox, network firewall, host-secret isolation, L5 health-check authority, BEO publication, RTM generation, or drift rejection.

---

## 5. Review Notes for Task 2

Task 2 tests should prove both paths:

- source mode for `git_status_short_branch` remains compatible with existing callers and still uses the source repository as the fixed-profile working directory;
- isolated mode uses a metadata fixture command shape with `cwd` outside the source repo, `.git` excluded from the copy, fixed `--git-dir`/`--work-tree`, `GIT_OPTIONAL_LOCKS=0`, bounded evidence, no authority grants, and source status/cache blocking still active.
