# BLK-System Sprint 012 — Task 6 Outcome

**Status:** Complete
**Date:** 2026-05-06
**Task:** Add Cache Jail, Synthetic Environment Scrub, Output Compression, Replay Bundle, and Source-Scan Gates
**Sprint:** BLK-SYSTEM-012 — Workspace Isolation and Process-Control Implementation Probes
**Implementation Commit:** `ae049ff test: add blk-test cache env replay probes`
**Remote:** implementation pushed to `origin/main`

---

## 1. Objective

Task 6 extends the BLK-SYSTEM-012 dependency-free Python probe module with deterministic cache-jail, synthetic environment, bounded output, replay-bundle, and source-scan probes.

The implementation remains local and inert. It does not authorize live BLK-test MCP, does not authorize live MCP client/server startup, does not execute fixed-tool tests, does not authorize authoritative BEO publication, does not authorize RTM generation, does not authorize RTM drift rejection authority, does not read protected BLK-req vault bodies, and does not claim production sandbox/cgroup/VM or production host-secret isolation.

---

## 2. Files Changed

Modified:

- `python/blk_test_mcp_workspace_process_probes.py`
- `python/test_blk_test_mcp_workspace_process_probes.py`

Outcome document:

- `docs/outcomes/BLK-SYSTEM-012_task-006-outcome.md`

---

## 3. Behavior Implemented

Added Task 6 public APIs:

```python
def build_scrubbed_probe_environment(run_id: str, cache_root, inherited_env=None) -> dict[str, object]: ...
def inspect_environment_policy(env) -> dict[str, object]: ...
def compress_bounded_output(stdout: bytes, stderr: bytes, max_bytes: int, max_error_entries: int = 7) -> dict[str, object]: ...
def build_workspace_process_replay_bundle(run_record: dict[str, object]) -> dict[str, object]: ...
```

Implemented gates for:

- run-scoped cache-jail acceptance under `.blk-system-012-cache/<run_id>`;
- rejection of non-cache-jail roots for scrubbed child environments;
- synthetic environment policy inspection without recording disallowed values;
- stripping `TOKEN`, `SECRET`, credential-like `KEY`, password, credential, `AWS_*`, `GITHUB_TOKEN`, `SSH_AUTH_SOCK`, package-manager auth variables, and unrelated host paths;
- non-inheritance of real host environment by fixed inert process probes;
- ANSI stripping, output byte caps, first/last bounded context, repeated-error deduplication, and secret/auth redaction;
- replay bundles containing bounded workspace, lock, process, cache, output, and non-authority summaries only;
- replay exclusion of raw logs, protected BLK-req body text, host-secret values, publication/approval/source-evidence-looking fields, BEO authority-looking fields, RTM fields, requirements, coverage matrices, drift-decision fields, and cyclic/unbounded structures;
- source-scan gates that preserve fixed inert `subprocess.Popen` use while rejecting live/network/MCP/Git-write/dynamic-execution surfaces.

Task 6 also hardened the Task 5 process runner by using a minimal inert child environment by default and making the descendant timeout snippet non-mutating.

---

## 4. RED Evidence

Initial Task 6 tests were added before the public APIs existed. Focused RED failed as expected:

```text
FAILED (errors=4)
AttributeError: module 'blk_test_mcp_workspace_process_probes' has no attribute 'inspect_environment_policy'
AttributeError: module 'blk_test_mcp_workspace_process_probes' has no attribute 'compress_bounded_output'
AttributeError: module 'blk_test_mcp_workspace_process_probes' has no attribute 'build_workspace_process_replay_bundle'
AttributeError: module 'blk_test_mcp_workspace_process_probes' has no attribute 'build_scrubbed_probe_environment'
```

Hostile review then found multiple real hardening gaps. Review-driven RED regressions failed before fixes for:

- public API positional-call compatibility;
- missing cache-jail rejection;
- incomplete credential/package-manager environment stripping;
- output cap accounting and secret redaction;
- replay alternate-key/raw-log/protected-body/authority-field bypasses;
- real host environment inheritance by fixed inert process probes;
- descendant timeout mutation timing;
- very-small output-cap behavior;
- bounded/cycle-safe replay bundles.

---

## 5. GREEN Evidence

Focused Task 6 gate after fixes:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
```

Result:

```text
Ran 64 tests in 4.487s

OK
```

Focused coverage includes the original Task 6 requirements plus review-driven regressions for API signatures, cache jail fail-closed behavior, AWS stripping, Basic/auth/API-key redaction, bounded deduplicated errors, tiny output caps, replay cycle safety, and alternate authority/raw-log key rejection.

---

## 6. Review Evidence

Final review status after the hostile review/fix cycles:

```text
Spec compliance review: PASS
Code quality/safety review: APPROVED
```

Notable review-driven fixes:

- made Task 6 API signatures match the plan's positional parameters;
- enforced cache-jail shape before exporting `BLK_SYSTEM_012_CACHE_ROOT`;
- broadened synthetic env stripping for compact credential keys, password/credential keys, all `AWS_*`, and package-manager auth variants;
- prevented allowed environment values from carrying secret/auth-looking strings;
- made fixed inert process probes use a minimal child environment instead of inheriting real host env;
- removed descendant timeout cwd mutation;
- bounded actual output evidence including deduplicated errors;
- redacted secret/auth/API-key patterns in output and replay strings;
- broadened replay exclusion for camelCase/raw/authority variants;
- capped replay strings, item counts, depth, and cycles;
- added AST-backed source-scan checks in addition to literal forbidden-marker checks.

---

## 7. Verification

Commands run from `/home/dad/BLK-System`:

```bash
export PATH="$HOME/.local/bin:$PATH"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_blk_test_mcp_workspace_process_probes.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
rm -rf python/__pycache__
```

Results:

```text
Focused Task 6 suite: Ran 64 tests in 4.487s — OK
Full Python unittest suite: Ran 218 tests in 5.192s — OK
go test ./...: OK
go vet ./...: OK
git diff --check: OK
```

Implementation commit:

```text
ae049ff test: add blk-test cache env replay probes
```

Remote:

```text
origin/main aligned after implementation push
```

---

## 8. Scope and Non-Authority Statement

Task 6 does not add or authorize:

- live BLK-test MCP execution;
- live MCP server/client startup;
- fixed-tool BLK-test execution;
- arbitrary shell or dynamic command execution;
- network clients, network servers, or MCP transports;
- Git staging/commit/push behavior from probe code;
- primary repo mutation from probe code;
- authoritative BEO publication;
- RTM generation;
- RTM drift rejection authority;
- protected BLK-req vault reads or protected body replay;
- production sandbox/cgroup/VM enforcement claims;
- production host-secret isolation claims.

Human sprint-executor Git commits and pushes remain separate from BLK-test/source-mutation authority.

---

## 9. Next Task

Next: BLK-SYSTEM-012 Task 7 — Define Active BLK-018 Probe Contract and Cross-Reference Gates.
