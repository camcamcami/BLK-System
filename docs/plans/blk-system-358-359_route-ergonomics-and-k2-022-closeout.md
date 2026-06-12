# BLK-SYSTEM-358..359 — Route Ergonomics and K2-022 Closeout Sprint Package Plan

**Status:** Planned for immediate execution
**Scope:** Fix concrete BLK-System route/operator/audit issues observed during K2-022, then archive/finalize K2-022 evidence.
**Authority stance:** BLK-System repository-development work only. This package does not grant reusable Codex dispatch, broad BLK-pipe dispatch, runtime/tooling expansion, BEO publication, RTM generation, production `blk-link`, protected-body access, or Kuronode source/Git mutation beyond exact already-executed K2-022 evidence reconciliation.

## Sprint 358 — BEB/L2 Route Ergonomics Hardening

### Objective
Close the route/operator gaps observed in K2-022:

1. Align Python `--preflight` with the Go `gitguard.EnsureClean` dirty check so source-worktree residue that would produce BLK-pipe `GIT_DIRTY` is blocked before dispatch.
2. Make clean-worktree manifest bytes unambiguous by letting BLK-System write the exact compact canonical manifest file whose SHA matches the reported approval hash.
3. Emit an authoritative route summary record after BLK-pipe/Codex returns so closeout relies on BLK-System/Git route evidence, not Codex's sandbox-local Git self-report.
4. Improve compact progress/log evidence so long routes provide bounded structured evidence without requiring giant raw log spelunking.

### Planned files
- `python/beb_l2_blk_pipe_route.py`
- `python/test_beb_l2_blk_pipe_route.py`
- `docs/outcomes/BLK-SYSTEM-358_sprint-closeout.md`

### Test-first gates
- RED: preflight must block exactly the same `git status --porcelain --untracked-files=all` residue that Go `EnsureClean` blocks and expose `clean_preflight_parity` evidence.
- RED: `--clean-worktree-manifest-output` must write compact canonical JSON bytes; the written file SHA must equal `drop_manifest_sha256`.
- RED: `process_drop_file` must return an authoritative route summary containing status, exit code, commit hash, payload/drop hashes, final-message path/hash when present, bounded validation/log fingerprints, and explicit non-authority flags.
- RED: CLI output must include the summary and not embed raw engine logs or validation logs in the route summary.

## Sprint 359 — K2-022 Evidence Archive / Closeout Reconciliation

### Objective
Archive the K2-022 BEB/L2/BEO/drop evidence in BLK-System and reconcile closeout metadata after Sprint 358 route-summary support exists.

### Planned files
- `artifacts/kuronode-v2/k2-022-agent-a-pre-write-promotion-readiness-disposition-gate/**`
- `docs/outcomes/BLK-SYSTEM-359_sprint-closeout.md`
- Obsidian view mirrors only if the canonical K2-022 BEO/metadata changes and the mirror is stale.

### Test/verification gates
- Verify K2-022 artifact hashes and route evidence are inspectable.
- Ensure no extra visible/canonical K2 BEO is created; one `BEO-K2-022` remains the visible outcome/evidence document.
- Archive exact BLK-System artifacts with exact-path staging only.
- Preserve pre-existing K2-019/K2-020 untracked artifacts unless separately selected.

## Package closeout checklist

- One closeout per sprint number, no per-task outcome docs.
- No new root `docs/BLK-###` unless a durable contract becomes necessary; current plan avoids one.
- Focused Python RED/GREEN, focused Go parity tests if touched, full Python discovery/chunking if required, `go test ./...`, and `git diff --check` on exact changed paths.
- Independent hostile review before commit for authority laundering, raw-log leakage, manifest hash ambiguity, and stale closeout/active-doc wording.
- Exact-path commit(s) and push to `origin/main` only after verification.
