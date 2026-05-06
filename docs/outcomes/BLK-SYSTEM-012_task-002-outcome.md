# BLK-System Sprint 012 — Task 2 Outcome

**Status:** Complete
**Date:** 2026-05-06
**Task:** Add Workspace Policy Descriptor, Clone Decision, Path Guards, and Cache Path Probes
**Sprint:** BLK-SYSTEM-012 — Workspace Isolation and Process-Control Implementation Probes
**Implementation Commit:** `0c7650e09f503b9815ddb1c6825e88138ead6ec5 test: add blk-test workspace policy probes`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Task 2 added the first dependency-free Python probe module for BLK-SYSTEM-012. The implementation provides deterministic local workspace-policy decisions, path escape rejection, protected-vault rejection, cache-jail path selection, and non-authority descriptor metadata.

The task remains probe-only. It does not authorize live BLK-test MCP, does not authorize live MCP client/server startup, does not execute fixed-tool tests, does not mutate the primary repo, does not stage files from probe code, does not commit from probe code, does not authorize authoritative BEO publication, does not authorize RTM generation, and does not authorize RTM drift rejection authority.

---

## 2. Files Added/Changed

Added:

- `python/blk_test_mcp_workspace_process_probes.py`
- `python/test_blk_test_mcp_workspace_process_probes.py`

No documentation, Go code, transport code, MCP server/client code, BEO publication code, RTM code, or live fixed-tool execution code was added in this task.

---

## 3. Behavior Implemented

### 3.1 Non-authority descriptor

Added:

```python
def build_workspace_process_boundary_descriptor() -> dict[str, object]:
```

The descriptor returns the required BLK-SYSTEM-012 non-authority fields:

```text
sprint = BLK-SYSTEM-012
authority = PROBE_ONLY
fixture_scope = INERT_LOCAL_FIXTURES_ONLY
live_mcp_authorized = False
mcp_server_started = False
mcp_client_started = False
fixed_tool_tests_executed = []
primary_repo_mutation_allowed = False
source_staging_allowed = False
source_commit_allowed = False
beo_publication = DRAFT_ONLY
rtm_status = NOT_GENERATED
active_vault_read_allowed = False
production_sandbox_claimed = False
```

### 3.2 Clone decision probe

Added:

```python
def decide_clone_strategy(
    source_root,
    scratch_root,
    *,
    fallback_root=None,
    source_device=None,
    scratch_device=None,
    fallback_device=None,
) -> dict[str, object]:
```

The function is decision-only and does not clone, hardlink, stage, commit, or mutate source. It returns fail-closed decisions using the required vocabulary:

- `HARDLINK_CLONE_SELECTED` when source and scratch are on the same device;
- `SAME_FILESYSTEM_FALLBACK_SELECTED` when scratch differs but an explicit same-device fallback is provided;
- `CLONE_BLOCKED_DIFFERENT_FILESYSTEM` when neither scratch nor explicit fallback is on the same device.

The decision payload explicitly records that hardlinks are not write isolation and that primary repo mutation, source staging, and source commit are not allowed.

### 3.3 Workspace-relative path guard

Added:

```python
def validate_workspace_relative_path(
    workspace_root,
    candidate_relative_path,
    *,
    protected_prefixes=("docs/active", "docs/requirements", "docs/use_cases"),
) -> dict[str, object]:
```

The path guard returns the required status vocabulary:

- `PATH_ACCEPTED`
- `PATH_REJECTED_ABSOLUTE`
- `PATH_REJECTED_TRAVERSAL`
- `PATH_REJECTED_SYMLINK_ESCAPE`
- `PATH_REJECTED_PROTECTED_VAULT`

It rejects absolute paths, any `..` traversal token, symlink escapes outside the workspace, direct protected vault prefixes, and symlink aliases that resolve into protected vault prefixes. Protected BLK-req vault body reads remain disallowed.

### 3.4 Run-scoped cache path selection

Added:

```python
def build_run_cache_paths(
    scratch_root,
    *,
    run_id: str,
) -> dict[str, object]:
```

The cache path selector returns `CACHE_JAIL_SELECTED` and chooses deterministic run-scoped paths under:

```text
<scratch_root>/.blk-system-012-cache/<run_id>/
```

It does not create paths. It records that the cache is outside source/workspace roots and that source staging/commit remain disallowed.

---

## 4. TDD Evidence

### 4.1 Initial RED — module missing

After writing `python/test_blk_test_mcp_workspace_process_probes.py` first, I ran the focused test before creating the implementation module.

Command:

```bash
python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
```

Expected RED was observed:

```text
ImportError: Failed to import test module: test_blk_test_mcp_workspace_process_probes
ModuleNotFoundError: No module named 'blk_test_mcp_workspace_process_probes'

Ran 1 test in 0.000s
FAILED (errors=1)
```

This was the expected missing-module failure for Task 2.

### 4.2 First GREEN — required APIs and base gates

After creating `python/blk_test_mcp_workspace_process_probes.py`, I reran the focused gate.

Command:

```bash
python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
```

Focused GREEN result:

```text
Ran 10 tests in 0.002s
OK
```

### 4.3 Review-found regression RED — protected-vault symlink alias

The first safety review found that a symlink alias inside the workspace could resolve into `docs/active` and bypass the textual protected-prefix check.

I added a regression test before fixing implementation:

```text
test_symlink_alias_to_protected_vault_is_rejected_without_reads
```

Command:

```bash
python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
```

Expected RED was observed:

```text
test_symlink_alias_to_protected_vault_is_rejected_without_reads ... FAIL

AssertionError: 'PATH_ACCEPTED' != 'PATH_REJECTED_PROTECTED_VAULT'

Ran 11 tests in 0.003s
FAILED (failures=1)
```

The failure proved the review-identified bypass before the implementation fix was applied.

### 4.4 Final GREEN — symlink alias fixed

I updated `validate_workspace_relative_path()` to re-check the resolved in-workspace path against protected prefixes after symlink resolution.

Focused GREEN result:

```text
Ran 11 tests in 0.003s
OK
```

---

## 5. Review Results

### 5.1 First spec compliance review

Result: `PASS`

The first spec review found the Task 2 API/status/descriptor/test coverage compliant with the plan.

### 5.2 First code quality and safety review

Result: `REQUEST_CHANGES`

The reviewer identified a real path-guard gap:

```text
validate_workspace_relative_path() can be bypassed for protected BLK-req vault paths through an in-workspace symlink alias.
```

Concrete fix requested:

```text
Add a regression test for alias -> docs/active and re-check the resolved workspace-relative path for protected prefixes.
```

The fix was implemented with strict RED/GREEN evidence in Section 4.3 and 4.4.

### 5.3 Final spec compliance review

Result: `PASS`

Reviewer summary:

```text
PASS

Required public APIs are present.
Required descriptor non-authority fields are implemented exactly.
Required status vocabulary is present.
Clone behavior covers same-device hardlink selection, different-device fail-closed, and explicit same-device fallback selection.
Path guards cover absolute, traversal, symlink escape, direct protected vault, and symlink alias to protected vault rejection.
Cache paths are run-scoped under scratch and marked outside source/workspace roots.
No prohibited execution/network/subprocess/git/fixed-tool patterns were found in the new module or tests.
```

### 5.4 Final code quality and safety review

Result: `APPROVED`

Reviewer summary:

```text
APPROVED

Probe module is dependency-free standard library only: pathlib and re.
No live MCP, server/client startup, subprocess execution, fixed-tool execution, git staging/commit/mutation, authoritative BEO publication, RTM generation, or production sandbox/isolation claims.
Protected BLK-req vault prefixes are rejected both directly and after symlink resolution.
Regression coverage exists for symlink aliasing into docs/active.
Focused tests passed: Ran 11 tests ... OK.
```

---

## 6. Final Verification

Before committing and pushing the Task 2 implementation, I reran the focused and shared verification gates.

Commands:

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
rm -rf python/__pycache__
git status --short --branch
git add python/blk_test_mcp_workspace_process_probes.py python/test_blk_test_mcp_workspace_process_probes.py
git diff --cached --check
git commit -m "test: add blk-test workspace policy probes"
git push origin main
```

Verification result:

```text
Ran 11 tests in 0.003s
OK

Ran 165 tests in 0.713s
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
git diff --check: PASS
git diff --cached --check: PASS
python/__pycache__ removed before exact-path staging
implementation push: 4badb5c..0c7650e main -> main
```

Post-push status:

```text
## main...origin/main
0c7650e (HEAD -> main, origin/main) test: add blk-test workspace policy probes
```

---

## 7. Explicit Non-Authority Statement

BLK-SYSTEM-012 Task 2 is a deterministic local probe task only. It does not authorize live BLK-test MCP, does not authorize live MCP client/server startup, does not execute fixed-tool tests, does not mutate primary repo, does not stage files from probe code, does not commit from probe code, does not authorize authoritative BEO publication, does not authorize RTM generation, does not authorize RTM drift rejection authority, does not read protected BLK-req vault bodies, does not claim production sandbox/cgroup/VM enforcement, and does not claim production host-secret isolation.

Sprint 013 owns approval/source-evidence authorization mechanics. Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke.

---

## 8. Deviations / Notes

- The review-requested protected-vault symlink-alias regression was added during Task 2. This strengthened the plan-required protected-vault rejection without broadening scope.
- `build_run_cache_paths()` validates `run_id` as a non-empty relative token and only selects paths; it does not create cache directories.
- `decide_clone_strategy()` is decision-only; it does not create hardlinks or workspaces. Task 3 owns fixture clone and teardown probes.
- No Hindsight tools were used.
- Outcome-document policy follows the updated user instruction: outcome docs are committed and pushed after each task, not deferred until sprint closeout.

---

## 9. Next Task

Task 3 — Prove Inert Fixture Clone, Startup Purge, Teardown, and Primary Manifest Guards.

Task 3 should extend `python/blk_test_mcp_workspace_process_probes.py` and `python/test_blk_test_mcp_workspace_process_probes.py` with marker-protected synthetic fixture validation, deterministic source manifests, inert workspace fixture creation, root-anchored startup purge, teardown guards, and source-manifest unchanged checks.
