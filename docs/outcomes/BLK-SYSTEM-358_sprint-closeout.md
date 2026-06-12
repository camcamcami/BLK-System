# BLK-SYSTEM-358 — BEB/L2 Route Ergonomics Hardening Sprint Closeout

**Status:** Complete
**Date:** 2026-06-12
**Commit:** `ab68bdf` (`fix: harden BEB-L2 route ergonomics`)

## 1. Objective

Fix the BLK-System route/operator/audit issues observed during K2-022 execution without expanding product/runtime authority:

1. Align Python BEB/L2 `--preflight` output with the Go `internal/gitguard.EnsureClean` dirty-worktree semantics that BLK-pipe actually enforces.
2. Add a helper/CLI output path that writes the retargeted clean-worktree manifest in the exact compact canonical JSON bytes whose SHA is reported for approval.
3. Emit a BLK-System/Git-owned authoritative route summary artifact after dispatch so closeout evidence does not rely on Codex final-message self-report.
4. Keep progress/log evidence compact and hash-bound rather than embedding raw engine, validation, or stderr logs.

## 2. Files Changed

- `python/beb_l2_blk_pipe_route.py`
- `python/blk_pipe_adapter.py`
- `python/test_beb_l2_blk_pipe_route.py`
- `docs/plans/blk-system-358-359_route-ergonomics-and-k2-022-closeout.md`
- `docs/outcomes/BLK-SYSTEM-358_sprint-closeout.md`

## 3. Implementation Summary

### Preflight parity

- `preflight_drop_file(...)` now includes `clean_preflight_parity` metadata naming the parity source as `internal/gitguard.EnsureClean` and the exact command surface: `git status --porcelain --untracked-files=all`.
- Preflight now reports whether BLK-pipe would fail with dirty-worktree semantics, including operator-local untracked residues such as `.agents/` and `.codex/` even when local Git config hides untracked files.
- Dirty or ignored residue now recommends retargeting to a trusted sterile clean worktree while keeping `source_cleanup_authorized`, `worktree_creation_authorized`, and `dispatch_authorized` false.

### Compact clean-worktree manifest writer

- `build_clean_worktree_drop_manifest(...)` accepts `manifest_output_path=...`.
- CLI accepts `--clean-worktree-manifest-output` with `--clean-worktree-manifest`.
- The written bytes are exactly `json.dumps(..., sort_keys=True, separators=(",", ":"))` encoded as UTF-8.
- `drop_manifest_sha256` is now the file hash when the helper writes the manifest, eliminating pretty-JSON approval-hash drift.

### Authoritative route summary

- `process_drop_file(...)` now wraps adapter/BLK-pipe results with a sanitized `route_summary`.
- Real dataclass results expose first-class `route_summary` via `ExecutionResult.route_summary`, so CLI JSON includes it through `asdict(...)`.
- Route summary includes status, exit code, BEB/L2/BEO IDs, worktree, target branch/hash, commit hash, drop manifest path/hash, payload hash, final-message path/hash/byte count, and compact hashes/byte counts for engine logs, validation logs, and stderr.
- Route summary explicitly sets these non-authority flags false:
  - `codex_final_message_authoritative`
  - `raw_logs_embedded`
  - `reusable_codex_dispatch_authorized`
  - `broad_blk_pipe_dispatch_authorized`
  - `beo_publication_authorized`
  - `rtm_generation_authorized`
  - `source_cleanup_authorized`
  - `worktree_creation_authorized`
- The summary artifact is written under `/tmp/blk-system-route-summaries/<BEB>/<target-prefix>/...json` with private directory mode handling.

## 4. TDD Evidence

### RED

Command:

```bash
cd /home/dad/BLK-System
rm -rf /tmp/blk-system-pycache
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_preflight_reports_blk_pipe_clean_preflight_parity_for_agent_residue \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_clean_worktree_manifest_output_writes_exact_compact_canonical_approval_bytes \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_clean_worktree_manifest_cli_emits_retargeted_manifest_without_dispatch \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_process_drop_file_returns_authoritative_route_summary_not_codex_self_report
```

Observed expected failures:

```text
FAILED (errors=4)
KeyError: 'clean_preflight_parity'
TypeError: build_clean_worktree_drop_manifest() got an unexpected keyword argument 'manifest_output_path'
SystemExit: 2 (--clean-worktree-manifest-output unrecognized)
KeyError: 'route_summary'
```

### GREEN

Command:

```bash
cd /home/dad/BLK-System
rm -rf /tmp/blk-system-pycache
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_preflight_reports_blk_pipe_clean_preflight_parity_for_agent_residue \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_clean_worktree_manifest_output_writes_exact_compact_canonical_approval_bytes \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_clean_worktree_manifest_cli_emits_retargeted_manifest_without_dispatch \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_process_drop_file_returns_authoritative_route_summary_not_codex_self_report
```

Output:

```text
....
----------------------------------------------------------------------
Ran 4 tests in 0.064s

OK
```

## 5. Verification

Focused route module:

```bash
cd /home/dad/BLK-System
rm -rf /tmp/blk-system-pycache
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_beb_l2_blk_pipe_route
```

Output:

```text
.....................................................
----------------------------------------------------------------------
Ran 53 tests in 0.930s

OK
```

Adapter module after `ExecutionResult.route_summary` field addition:

```bash
cd /home/dad/BLK-System
rm -rf python/__pycache__ /tmp/blk-system-pycache
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_pipe_adapter
```

Output:

```text
..................................................
----------------------------------------------------------------------
Ran 50 tests in 3.913s

OK
```

Lean documentation policy gate after extending sprint-range coverage to 358:

```bash
cd /home/dad/BLK-System
rm -rf /tmp/blk-system-pycache
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_lean_documentation_policy
```

Output:

```text
........
----------------------------------------------------------------------
Ran 8 tests in 0.134s

OK
```

Go suite:

```bash
cd /home/dad/BLK-System
go test ./...
```

Output:

```text
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	0.032s
ok  	github.com/camcamcami/BLK-System/internal/contracts	0.065s
ok  	github.com/camcamcami/BLK-System/internal/engine	0.206s
ok  	github.com/camcamcami/BLK-System/internal/execguard	9.268s
ok  	github.com/camcamcami/BLK-System/internal/gitguard	2.096s
ok  	github.com/camcamcami/BLK-System/internal/pipe	12.849s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	0.016s
ok  	github.com/camcamcami/BLK-System/internal/testutil	0.338s
ok  	github.com/camcamcami/BLK-System/internal/validation	0.366s
ok  	github.com/camcamcami/BLK-System/internal/validationprofiles	0.006s
```

Python full-suite discovery first hit the tool wrapper timeout at 600s, so verification used the BLK-System chunked fallback pattern. Chunked verification produced no failures and one individual module timeout at the runner's 240s cap:

```text
{
  "duration_seconds_total": 2129.355,
  "fail_results": [],
  "log_dir": "/tmp/blk-system-python-chunk-logs",
  "module_total": 166,
  "pass_results": 13,
  "result_total": 19,
  "split_timeout_count": 5,
  "timeout_results": [
    {
      "label": "chunk08bbb_018",
      "modules": [
        "python.test_verified_loop_beo_publication_side_effect_trace_closure_330_333"
      ],
      "status": "TIMEOUT"
    }
  ]
}
```

The timed-out individual module was rerun directly with the tool's longer 600s foreground cap:

```bash
cd /home/dad/BLK-System
rm -rf /var/tmp/blk-system-testtmp /tmp/blk-system-pycache
mkdir -p /var/tmp/blk-system-testtmp
TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_verified_loop_beo_publication_side_effect_trace_closure_330_333
```

Output:

```text
......
----------------------------------------------------------------------
Ran 6 tests in 288.553s

OK
```

Diff whitespace check:

```bash
git diff --check -- python/beb_l2_blk_pipe_route.py python/blk_pipe_adapter.py python/test_beb_l2_blk_pipe_route.py python/test_lean_documentation_policy.py docs/plans/blk-system-358-359_route-ergonomics-and-k2-022-closeout.md docs/outcomes/BLK-SYSTEM-358_sprint-closeout.md
```

Output: no findings.

## 6. Hostile Review / Risk Check

Pre-commit checklist:

- **Authority laundering:** PASS. New summary is evidence only; all product/runtime side effects and reusable route authorities remain false.
- **Codex self-report ambiguity:** PASS. Summary marks `codex_final_message_authoritative=false` and binds final-message file only by path/hash/bytes.
- **Raw-log leakage:** PASS. Summary uses SHA/byte counts for raw engine logs, validation logs, and stderr; it does not embed raw content.
- **Manifest hash ambiguity:** PASS. Helper/CLI can write compact canonical bytes directly and report the same file SHA.
- **Source cleanup/worktree creation:** PASS. Dirty/ignored-residue recommendations remain non-mutating and non-authorizing.
- **K2 artifact residue mixing:** PASS. This sprint stages only exact route-hardening source/tests/docs paths and does not stage untracked K2-019/K2-020/K2-022 artifact trees.

Independent hostile review result:

- Verdict: **PASS — no BLOCKER findings**.
- Reviewer verified preflight parity against `internal/gitguard/status.go`, compact manifest writer semantics, route-summary non-authority flags, no raw logs embedded in route-summary/artifact, and no accidental K2 artifact staging.
- Nonblockers recorded for future consideration:
  - full CLI/result output can still include raw adapter fields outside `route_summary`; the route summary itself remains compact/hash-only;
  - route summary trusts BLK-pipe adapter result fields rather than independently post-reading Git in Python;
  - route-summary artifact hash covers the on-disk artifact record, while in-memory returned summary additionally carries artifact path/hash metadata.

## 7. Authority Boundary

This sprint does **not** authorize:

- live BLK-pipe/Codex dispatch beyond exact already-approved payloads;
- reusable Codex/tactical-LLM dispatch;
- source cleanup or clean-worktree creation;
- BEO publication/signing/storage/ledger/rollback;
- RTM generation, production `blk-link`, drift rejection, or coverage truth;
- protected BLK-req body reads/copying/parsing/hashing/scanning/mutation;
- Kuronode source/Git mutation;
- package-manager/network/browser/cyber tooling expansion;
- production-isolation claims.

## 8. Documentation Burden Check

- No new root `docs/BLK-###` document was created.
- One sprint closeout was created for BLK-SYSTEM-358.
- One durable plan file was created because the user explicitly asked to plan and execute a grouped sprint package: `docs/plans/blk-system-358-359_route-ergonomics-and-k2-022-closeout.md`.
- No per-task outcome docs were created.

## 9. Final Verification / Commit / Push

Pre-staging status confirmed only exact Sprint 358 paths were staged; pre-existing K2 artifact residue remained untracked and unstaged:

```text
## main...origin/main
 M python/beb_l2_blk_pipe_route.py
 M python/blk_pipe_adapter.py
 M python/test_beb_l2_blk_pipe_route.py
 M python/test_lean_documentation_policy.py
?? artifacts/kuronode-v2/k2-019-bounded-read-only-project-source-diagnostic-intake/
?? artifacts/kuronode-v2/k2-020-renderer-visible-project-source-diagnostic-status/
?? artifacts/kuronode-v2/k2-022-agent-a-pre-write-promotion-readiness-disposition-gate/
?? docs/outcomes/BLK-SYSTEM-358_sprint-closeout.md
?? docs/plans/blk-system-358-359_route-ergonomics-and-k2-022-closeout.md
```

Exact-path commit evidence:

```text
[main ab68bdf] fix: harden BEB-L2 route ergonomics
 6 files changed, 608 insertions(+), 11 deletions(-)
 create mode 100644 docs/outcomes/BLK-SYSTEM-358_sprint-closeout.md
 create mode 100644 docs/plans/blk-system-358-359_route-ergonomics-and-k2-022-closeout.md
```

Push is intentionally batched with BLK-SYSTEM-359 so the complete user-request package lands together on `origin/main`.
