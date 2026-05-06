# BLK-System Sprint 012 — Task 3 Outcome

**Status:** Complete
**Date:** 2026-05-06
**Task:** Prove Inert Fixture Clone, Startup Purge, Teardown, and Primary Manifest Guards
**Sprint:** BLK-SYSTEM-012 — Workspace Isolation and Process-Control Implementation Probes
**Implementation Commit:** `565f45548cf7a2c64228ae603cfbcd4cda2beef5 test: prove inert workspace clone teardown guards`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Task 3 extends the BLK-SYSTEM-012 dependency-free Python probe module with inert fixture lifecycle guards. The work proves marker-protected synthetic fixture validation, deterministic source manifests, workspace fixture creation under a test-owned scratch root, startup purge of owned stale probe paths, terminal teardown cleanup, and primary source manifest verification.

The task remains probe-only. It does not authorize live BLK-test MCP, does not authorize live MCP client/server startup, does not execute fixed-tool tests, does not mutate the primary repo from probe code, does not stage files from probe code, does not commit from probe code, does not authorize authoritative BEO publication, does not authorize RTM generation, and does not authorize RTM drift rejection authority.

---

## 2. Files Added/Changed

Modified:

- `python/blk_test_mcp_workspace_process_probes.py`
- `python/test_blk_test_mcp_workspace_process_probes.py`

No documentation doctrine, Go code, transport code, MCP server/client code, BEO publication code, RTM code, network code, or live fixed-tool execution code was added in this implementation commit.

---

## 3. Behavior Implemented

### 3.1 Inert fixture source guard

Added:

```python
def assert_inert_fixture_source(source_root) -> dict[str, object]:
```

The source guard accepts only locally owned synthetic fixture roots containing the literal marker file:

```text
.blk-system-012-inert-fixture
```

It rejects unsafe fixture roots with explicit status values, including:

- `INERT_FIXTURE_REJECTED_RESERVED_ROOT` for `/`, `$HOME`, `/home/dad/BLK-System`, the current working directory, and repository-owned paths;
- `INERT_FIXTURE_REJECTED_MISSING_MARKER` for unmarked roots;
- `INERT_FIXTURE_REJECTED_GIT_DIRECTORY` for roots containing `.git`;
- `INERT_FIXTURE_REJECTED_SYMLINK_ESCAPE` for source-root symlinks or symlinks that escape the fixture tree;
- `INERT_FIXTURE_REJECTED_UNOWNED_ROOT` / `INERT_FIXTURE_REJECTED_UNOWNED_MARKER` for unowned roots or markers.

Accepted sources return `INERT_FIXTURE_SOURCE_ACCEPTED` and preserve non-authority fields such as `authority: PROBE_ONLY`, `primary_repo_mutation_allowed: False`, `source_staging_allowed: False`, `source_commit_allowed: False`, `active_vault_read_allowed: False`, and `production_sandbox_claimed: False`.

### 3.2 Deterministic source manifest and primary manifest verification

Added:

```python
def manifest_source_tree(source_root) -> dict[str, object]:

def verify_primary_repo_manifest(source_root, manifest) -> dict[str, object]:
```

`manifest_source_tree()` validates the inert fixture first, then records deterministic file metadata and SHA-256 hashes. The manifest includes path, type, size, mode, and content hash data sorted by relative path, plus a stable `manifest_sha256` over the manifest entries.

`verify_primary_repo_manifest()` re-manifests the source fixture after probes and returns:

- `PRIMARY_MANIFEST_UNCHANGED` when the source manifest matches;
- `PRIMARY_MANIFEST_CHANGED` with added/removed path lists and hash metadata if the source fixture changed.

### 3.3 Inert workspace fixture creation

Added:

```python
def create_inert_workspace_fixture(
    source_root,
    scratch_root,
    *,
    run_id: str,
) -> dict[str, object]:
```

The workspace fixture helper validates the inert source and scratch root before creating a run-scoped workspace under:

```text
<scratch_root>/.blk-system-012-workspaces/<run_id>/workspace
```

The helper rejects unsafe source roots, unsafe scratch roots, scratch escapes, and pre-existing run paths. It writes Sprint 012 ownership markers to the run root and workspace fixture, clones source files without modifying the source, and records `hardlinks_are_write_isolation: False` to preserve the Task 2 hardlink-safety invariant.

### 3.4 Startup purge of owned stale paths and locks

Added:

```python
def startup_purge_owned_stale_paths(
    scratch_root,
    *,
    pid_alive=None,
) -> dict[str, object]:
```

Startup purge is constrained to a validated scratch root and Sprint 012 prefixes:

```text
.blk-system-012-workspaces
.blk-system-012-cache
.blk-system-012-locks
```

It removes only paths carrying the Sprint 012 owned marker or owned lock text, preserves unmarked Sprint 012 paths, preserves unrelated temp paths, preserves symlinks/escapes, preserves live-PID locks, and removes dead-PID owned locks only when they are under the validated scratch root.

### 3.5 Terminal teardown cleanup

Added:

```python
def teardown_run_paths(
    *,
    workspace_path,
    cache_paths,
    lock_path=None,
    status: str,
) -> dict[str, object]:
```

Teardown cleanup runs only for terminal statuses:

```text
PASS
FAIL
BLOCKED
FATAL_TIMEOUT
FATAL_OUTPUT_FLOOD
TRANSPORT_ERROR
OPERATOR_INTERRUPTED
```

For those statuses, it removes owned workspace/cache/lock paths under Sprint 012 prefixes and records removed/preserved paths. It skips non-terminal statuses, preserves unmarked paths, preserves symlinks, and refuses reserved roots or repository-owned paths.

---

## 4. TDD Evidence

### 4.1 RED — Task 3 tests against the pre-implementation module

After Task 3 tests were added, the focused RED state was independently reconstructed and verified by running the new Task 3 test file against the pre-Task-3 implementation module from `HEAD^`.

Command shape:

```bash
python3 -m unittest discover -s <temp-red-copy> -p 'test_blk_test_mcp_workspace_process_probes.py' -v
```

Expected RED was observed because the new public APIs did not exist in the pre-Task-3 module:

```text
RED_EXIT_CODE= 1
test_marker_protected_temp_fixture_passes ... ERROR
test_real_blk_system_repo_path_rejects_as_reserved_root ... ERROR
test_roots_containing_git_reject_even_with_marker ... ERROR
test_symlink_escape_inside_marked_fixture_rejects ... ERROR
test_unmarked_roots_reject_without_primary_authority ... ERROR
test_source_manifest_is_unchanged_after_clone_and_teardown ... ERROR
test_workspace_fixture_is_created_only_under_scratch_root ... ERROR
test_dead_pid_locks_are_removed_only_under_owned_scratch_root ... ERROR
test_live_pid_locks_are_preserved ... ERROR
test_startup_purge_removes_only_owned_stale_sprint_012_prefix_paths ... ERROR
test_teardown_removes_workspace_cache_and_lock_for_terminal_statuses ... ERROR

AttributeError: module 'blk_test_mcp_workspace_process_probes' has no attribute 'assert_inert_fixture_source'
```

This is the expected missing-function RED for Task 3.

### 4.2 GREEN — focused Task 3 gate

After implementation, the focused BLK-test MCP workspace/process probe suite passed.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
```

Result:

```text
Ran 22 tests in 0.017s

OK
```

The focused GREEN gate covers the Task 2 retained probes plus Task 3 lifecycle probes:

- unmarked roots reject;
- roots containing `.git` reject;
- the real BLK-System repo path rejects;
- marker-protected temp fixtures pass;
- symlink escapes inside a marked fixture reject;
- workspace fixture is created only under the scratch root;
- source manifest is unchanged after clone/teardown;
- startup purge removes only owned stale Sprint 012 prefix paths;
- unrelated temp paths are preserved;
- live-PID locks are preserved;
- dead-PID owned locks are removed only under the validated scratch root;
- teardown removes workspace/cache/lock for `PASS`, `FAIL`, `BLOCKED`, `FATAL_TIMEOUT`, `FATAL_OUTPUT_FLOOD`, `TRANSPORT_ERROR`, and `OPERATOR_INTERRUPTED`.

---

## 5. Review Results

### 5.1 Spec compliance review

Result: `PASS`

Reviewer summary:

```text
PASS

Required public APIs are present:
- assert_inert_fixture_source
- manifest_source_tree
- create_inert_workspace_fixture
- startup_purge_owned_stale_paths
- teardown_run_paths
- verify_primary_repo_manifest

The literal marker .blk-system-012-inert-fixture is present.
Source guard rejects reserved roots, .git, missing marker, unowned roots, and symlink escapes.
Tests cover unmarked root rejection, .git rejection, real repo rejection, marked temp fixture acceptance, workspace under scratch, manifest unchanged after clone/teardown, startup purge, live/dead locks, and terminal teardown statuses.
No prohibited live MCP, server/client startup, subprocess use, fixed-tool execution, git operation in probe code/tests, protected-vault read, BEO publication, RTM generation, or production-sandbox claim was found.
```

### 5.2 Code quality and safety review

Result: `APPROVED`

Reviewer summary:

```text
APPROVED

Reviewed only the scoped probe/test files and ran the focused unittest plus git diff --check HEAD^ HEAD; both passed.
No prohibited execution/scope creep found: no subprocess/shell/eval/network/live MCP/JSON-RPC/git operations; stdlib-only dependencies.
Cleanup paths are guarded by scratch/root validation, Sprint 012 prefixes, owned markers/lock evidence, and symlink preservation; no blocking unsafe deletion pattern found.
Tests cover required source rejection/acceptance, scratch workspace clone, manifest unchanged verification, startup purge cases, and teardown for all terminal statuses.
```

---

## 6. Final Verification

Before closing Task 3, I reran the focused and shared verification gates after the implementation commit was pushed.

Commands:

```bash
export PATH="$HOME/.local/bin:$PATH"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check HEAD^ HEAD
rm -rf python/__pycache__
git status --short --branch
```

Verification result:

```text
Ran 22 tests in 0.017s
OK

Ran 176 tests in 0.715s
OK

ok  github.com/camcamcami/BLK-System/cmd/blk-pipe
ok  github.com/camcamcami/BLK-System/internal/contracts
ok  github.com/camcamcami/BLK-System/internal/engine
ok  github.com/camcamcami/BLK-System/internal/execguard
ok  github.com/camcamcami/BLK-System/internal/gitguard
ok  github.com/camcamcami/BLK-System/internal/pipe
ok  github.com/camcamcami/BLK-System/internal/runtimeguard
ok  github.com/camcamcami/BLK-System/internal/testutil
ok  github.com/camcamcami/BLK-System/internal/validation

go vet ./...: PASS
git diff --check HEAD^ HEAD: PASS
python/__pycache__ removed
status: ## main...origin/main
```

Implementation push:

```text
565f45548cf7a2c64228ae603cfbcd4cda2beef5 test: prove inert workspace clone teardown guards
Remote: pushed to origin/main
```

---

## 7. Explicit Non-Authority Statement

BLK-SYSTEM-012 Task 3 is a deterministic local probe task only. It does not authorize live BLK-test MCP, does not authorize live MCP client/server startup, does not execute fixed-tool tests, does not mutate primary repo from probe code, does not stage files from probe code, does not commit from probe code, does not authorize authoritative BEO publication, does not authorize RTM generation, does not authorize RTM drift rejection authority, does not read protected BLK-req vault bodies, does not claim production sandbox/cgroup/VM enforcement, and does not claim production host-secret isolation.

Sprint 013 owns approval/source-evidence authorization mechanics. Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke.

---

## 8. Deviations / Notes

- The initial implementation subagent completed the local implementation commit but timed out before returning its summary. I independently verified the committed diff, reconstructed RED against the pre-Task-3 module, reran GREEN and shared verification, and used fresh review gates before pushing.
- A first code-quality review attempt also timed out without a final verdict. I reran a bounded code-quality/safety review over the exact Task 3 files and received `APPROVED`.
- The implementation uses `shutil.copytree(..., copy_function=shutil.copy2)` for inert fixture copy behavior. It does not claim hardlinks provide write isolation. The source manifest unchanged gate is the primary corruption guard for this task.
- Outcome-document policy follows the updated user instruction: outcome docs are committed and pushed after each task, not deferred until sprint closeout.
- No Hindsight tools were used.

---

## 9. Next Task

Task 4 — Add Atomic Probe Lock and Parallel-Prevention Gates.

Task 4 should extend `python/blk_test_mcp_workspace_process_probes.py` and `python/test_blk_test_mcp_workspace_process_probes.py` with probe lock inspection, atomic acquisition, bounded wait decisions, stale/live lock behavior, ownership-aware release, and parallel prevention evidence under test-owned temporary roots.
