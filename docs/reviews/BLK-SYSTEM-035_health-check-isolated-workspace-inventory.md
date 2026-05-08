# BLK-SYSTEM-035 — Health-Check Isolated Workspace Inventory

**Status:** Complete
**Date:** 2026-05-08T20:56:00+10:00
**Sprint:** BLK-SYSTEM-035
**Boundary:** `docs/BLK-037_track-i-health-check-isolated-workspace-execution-boundary.md`

---

## 1. Inventory Summary

BLK-SYSTEM-035 follows the BLK-SYSTEM-034 side-effect boundary by adding an optional isolated-workspace execution mode for eligible non-Git fixed profiles. The current runner already provides fixed-profile execution, trusted executable resolution, environment scrubbing, runner-owned temp/cache placement outside the repository, source Git status observation, source repo-local Python cache observation, output bounds, redaction, startup failure handling, and process-group timeout cleanup.

The gap is that current source mode still uses the source repository as subprocess `cwd`. That is acceptable for BLK-036 advisory operation but does not provide the stronger no-source-cwd posture called out as future work by the BLK-SYSTEM-034 closeout.

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
- advisory-only PASS/FAIL/BLOCKED vocabulary.

---

## 3. New Isolated Workspace Design Surface

BLK-SYSTEM-035 adds an optional `workspace_mode="isolated_copy"` path for eligible non-Git profiles.

Expected isolated-workspace setup:

1. create a runner-owned temporary directory under the existing safe temp parent outside `REPO_ROOT`;
2. copy a filtered repository snapshot into a child isolated workspace directory;
3. exclude `.git`, `__pycache__`, `.pyc`, `.pytest_cache`, and protected BLK-req path families: `docs/active/`, `docs/requirements/`, `docs/use_cases/`;
4. execute eligible non-Git profiles with `cwd` set to the isolated workspace;
5. set `PYTHONPATH` to the isolated workspace's `python/` directory, not the source repository's `python/` directory;
6. keep temp/cache environment variables under the runner-owned temp directory outside `REPO_ROOT`;
7. observe source repository status/cache before and after execution;
8. block advisory PASS if source repository status/cache changed or isolated workspace cleanup failed.

---

## 4. Git Profile Boundary

The `git_status_short_branch` profile remains source-repository mode only for BLK-SYSTEM-035. The isolated copy excludes `.git` by design, so the runner must fail closed before subprocess startup when asked to run `git_status_short_branch` in isolated mode.

This avoids silently copying `.git`, synthesizing Git history, creating worktrees, running clone-like setup, staging, committing, or claiming Git health from a `.git`-less copy.

---

## 5. Non-Authority Inventory

BLK-SYSTEM-035 does not authorize:

- new profile IDs;
- arbitrary shell;
- caller-supplied commands or argv;
- network/API/model/cyber tooling;
- package-manager execution;
- Git/source mutation or repair;
- `.git` copying;
- protected BLK-req body reads, copying, parsing, hashing, summarizing, or inspection;
- active-vault scans or runtime active-vault comparisons;
- BLK-pipe dispatch or validation authority;
- production BLK-test MCP or new BLK-test smoke;
- BEO publication;
- signer/storage/public-ledger mutation;
- runtime RTM generation;
- RTM drift rejection or final drift decisions;
- production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux enforcement;
- network firewall enforcement;
- host-secret isolation;
- L5 production health-check authority.

---

## 6. Review Notes for Task 2

Task 2 tests should prove both paths:

- default source mode remains compatible with existing callers and smoke runs all five profiles;
- isolated mode runs the four eligible non-Git profiles from outside `REPO_ROOT`, uses isolated `PYTHONPATH`, excludes protected and Git paths from the copy, observes source status/cache, removes the isolated workspace, and fails closed for `git_status_short_branch` before subprocess startup.
