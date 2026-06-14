# BLK-SYSTEM-365 — Route Performance Retrospective Hardening Sprint Closeout

**Status:** Complete
**Date:** 2026-06-14
**Commit:** this commit (`feat: harden route performance preflight gates`)

## 1. Objective

Reduce avoidable BLK-System/Kuronode route waste observed in K2-025 without weakening the BLK-pipe-or-stop discipline established in BLK-SYSTEM-363/364.

The sprint focused on executable pre-dispatch and route-evidence classification:

- dirty or ignored source worktrees are explicitly classified as source-dispatch-skip / sterile-retarget conditions;
- repeated clean `ENGINE_TIMEOUT` route evidence with no commit, no final message, and no validation logs is classified as a route-performance review blocker before another normal retry;
- governed-write transaction packages now require an explicit hostile-readiness matrix before dispatch.

## 2. Files Changed

- `python/beb_l2_blk_pipe_route.py`
- `python/test_beb_l2_blk_pipe_route.py`
- `python/test_lean_documentation_policy.py`
- `docs/plans/blk-system-365_route-performance-retrospective-hardening.md`
- `docs/outcomes/BLK-SYSTEM-365_sprint-closeout.md`

## 3. Implementation Summary

### Governed-write transaction hostile-readiness profile

Added the explicit readiness profile:

```text
kuronode-governed-write-transaction-v1
```

The profile emits `KGWT-001` through `KGWT-010` probe-card rows covering K2-024 admission authenticity, forged admission records, identity/hash matching, authority/publication/RTM/provider aliases, package/path alias denial, stale-version/no-op recovery, hostile JS object handling, deterministic deep-frozen recovery records, readiness-refresh non-authority, and closeout hostile-matrix evidence.

Preflight now treats packages touching:

- `src/shared/governed-write-transaction.mjs`
- `tests/governed-write-transaction.test.mjs`

as requiring that readiness profile before BLK-pipe dispatch. Missing profile evidence returns `MISSING_REQUIRED_READINESS_PROFILE`, keeps `source_dispatch_should_be_skipped=true`, and requires `add_governed_write_transaction_hostile_matrix`.

Post-hostile-review remediation also rejects dot-segment allowlist aliases such as `src/shared/./governed-write-transaction.mjs` instead of allowing them to bypass exact candidate detection.

### Source-dispatch skip classification

Preflight reports now include:

- `source_dispatch_should_be_skipped`
- `route_performance_required_action`
- `fallback_authorized=false`

Dirty/untracked/ignored source worktree evidence is classified with `route_performance_required_action=build_default_clean_worktree_retarget_plan`, preserving the existing clean-worktree retarget path and avoiding fallback normalization.

### Route-performance retry budget gate

Added `evaluate_route_performance_gate(...)` to classify accumulated route summaries before spending another normal retry.

Two or more `ENGINE_TIMEOUT` summaries with:

- empty `commit_hash`,
- `final_message_bytes == 0`,
- `validation_log_count == 0`,

return `ROUTE_PERFORMANCE_REVIEW_REQUIRED`, `normal_retry_allowed=false`, blocker `ENGINE_TIMEOUT_RETRY_BUDGET_EXCEEDED`, and required action `perform_route_performance_review_or_split_scope`.

The evaluator is non-authorizing: it does not grant fallback, source cleanup, worktree creation, dispatch, BEO publication, RTM generation, or product/source mutation.

Post-hostile-review remediation makes malformed timeout evidence fail closed: whitespace-only commit hashes and string-valued numeric counters such as `"0"` now produce `MALFORMED_ROUTE_TIMEOUT_EVIDENCE` and require `repair_route_summary_inputs` rather than passing as normal retry evidence.

## 4. Verification

### RED evidence

Focused RED run before implementation:

```text
Ran 4 tests in 0.063s
FAILED (failures=1, errors=3)
```

Expected missing behavior was observed:

- governed-write transaction package preflight returned `READY` instead of `BLOCKED`;
- `kuronode-governed-write-transaction-v1` was unsupported;
- `source_dispatch_should_be_skipped` was absent;
- `evaluate_route_performance_gate` was absent.

### GREEN focused evidence

New focused tests after implementation:

```text
Ran 4 tests in 0.066s
OK
```

Full route helper suite:

```text
Ran 84 tests in 1.084s
OK
```

### Post-hostile-review RED/GREEN remediation

Independent hostile review found two blockers:

1. dot-segment allowlist aliases could bypass the governed-write hostile-readiness profile requirement;
2. malformed `ENGINE_TIMEOUT` evidence using whitespace commit hashes and string zero counters could pass the retry gate.

Regression RED before remediation:

```text
Ran 2 tests in 0.020s
FAILED (failures=2)
```

Regression GREEN after remediation:

```text
Ran 2 tests in 0.016s
OK
```

### Final verification evidence

Focused route + lean policy:

```text
Ran 92 tests in 1.290s
OK
```

Diff and added-line hygiene checks:

```text
git diff --check: clean
SECURITY_SCAN_ADDED_LINES: clean
```

Broad Python discovery first hit the foreground wrapper cap at 600s, so broad verification used the established chunked module method.

Chunked broad verification summary:

```text
166 modules checked
1,663 tests passed
35 skipped
0 failures
0 errors
```

Chunk evidence:

```text
CHUNK 1: PASS tests=373 skipped=34
CHUNK 2: PASS tests=164 skipped=0
CHUNK 3: PASS tests=282 skipped=0
CHUNK 4: PASS tests=315 skipped=0
CHUNK 5: PASS tests=108 skipped=0
CHUNK 6: PASS tests=140 skipped=1
CHUNK 7: PASS tests=126 skipped=0
CHUNK 8: PASS tests=121 skipped=0
CHUNK 9 split modules: PASS tests=34 skipped=0
```

One long verified-loop module exceeded a 300s wrapper cap after five tests on its first split run; the same single module was immediately rerun with the 600s foreground cap and passed:

```text
Ran 6 tests in 287.316s
OK
```

## 5. Hostile Review / Risk Check

Reviewed against BLK-System authority-gated sprint risks:

- **Fallback laundering:** new fields keep `fallback_authorized=false`; the timeout evaluator blocks normal retry review but does not authorize external Codex fallback.
- **Source cleanup laundering:** dirty/ignored worktree handling points to sterile retarget planning while keeping `source_cleanup_authorized=false` and `worktree_creation_authorized=false`.
- **Dispatch laundering:** missing governed-write hostile matrix sets `source_dispatch_should_be_skipped=true`; no dispatch args, target hash, trusted roots, validation profiles, or engine settings are expanded by the readiness profile.
- **Path alias laundering:** dot-segment allowlist aliases are rejected by the manifest path normalizer before they can evade governed-write candidate detection.
- **Authority expansion:** KGWT probes are pre-dispatch checklist evidence only; they do not authorize provider calls, filesystem writes, BEO publication, RTM generation, production `blk-link`, signing/storage/ledger, protected-body access, or reusable BLK-pipe/Codex authority.
- **Evidence substitution:** timeout review is based on route-summary shape (`ENGINE_TIMEOUT`, empty commit, zero final-message bytes, zero validation logs), not on prose claims; malformed timeout evidence now fails closed instead of being skipped.

Final post-remediation independent hostile review was attempted but timed out without returning a usable report. A local hostile self-review then executed explicit probes for the two remediated blocker classes:

```text
ALIAS_REJECTED ./src/shared/governed-write-transaction.mjs :: allowed_new_files entries must be explicit relative files
ALIAS_REJECTED src/shared/./governed-write-transaction.mjs :: allowed_new_files entries must be explicit relative files
ALIAS_REJECTED tests/./governed-write-transaction.test.mjs :: allowed_new_files entries must be explicit relative files
MALFORMED_TIMEOUT_GATE ROUTE_PERFORMANCE_REVIEW_REQUIRED repair_route_summary_inputs ['MALFORMED_ROUTE_TIMEOUT_EVIDENCE', 'MALFORMED_ROUTE_TIMEOUT_EVIDENCE']
HOSTILE_SELF_REVIEW_PROBES: pass
```

Post-review spot check:

```text
Ran 10 tests in 0.172s
OK
```

## 6. Authority Boundary

This sprint changes BLK-System development helpers and tests only.

It does not authorize:

- Kuronode product code changes;
- live BLK-pipe/Codex dispatch;
- external/supervised Codex fallback;
- source cleanup or worktree creation;
- BEO closeout execution or publication;
- RTM generation or production `blk-link`;
- protected BLK-req body reads/copying/parsing/hashing/scanning/mutation;
- package-manager, network, model-service, browser, cyber tooling, or production-isolation claims.

## 7. Documentation Burden Check

No new root `docs/BLK-###` doctrine document was created. The sprint used one plan and exactly one outcome closeout. No per-task outcome documents were created.
