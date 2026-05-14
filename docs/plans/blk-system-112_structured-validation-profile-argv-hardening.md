# BLK-SYSTEM-112 — Structured Validation Profile argv Hardening Plan

**Status:** Planned / executing
**Date:** 2026-05-14
**Source finding:** `docs/reviews/BLK-SYSTEM_post-103_all-codebase-hostile-review-and-completion-roadmap.md` HR-006
**Track:** Milestone 2 — BLK-pipe production hardening

## Purpose

Close the repository-owned profile half of HR-006 by converting validation profiles from shell command strings into structured argv/env specs. Preserve free-form `validation_commands` only as explicitly visible trusted-local compatibility for later BLK-SYSTEM-113 policy hardening.

## Scope

- Go validation profile registry and validation runner.
- Go payload resolution and report evidence fields needed to prove profile argv execution.
- Python adapter result parsing for new evidence fields only.
- BLK-004 and BLK-112 doctrine record.

## RED Tests First

1. `internal/validationprofiles` must expose structured profile specs whose `argv` entries are not `sh -c` shell wrappers.
2. `internal/validation` must run structured specs literally, proving shell expansion/metacharacters do not execute.
3. `internal/pipe` must execute repository-owned profiles through structured argv while preserving profile evidence.

## Explicit Non-Authority

This sprint does not authorize BLK-pipe runtime dispatch against Kuronode or any target repository, BLK-test runtime, BEO publication, RTM generation, RTM drift rejection, protected BLK-req body reads, target/source/Git mutation outside this BLK-System sprint, package/network/model/browser/cyber tooling, signer/storage/ledger behavior, or production sandbox/isolation claims.

## Exit Criteria

- Focused RED/GREEN checks pass.
- `go test ./internal/validationprofiles ./internal/validation ./internal/contracts ./internal/pipe` passes.
- `git diff --check` passes.
- Hostile review and closeout docs record HR-006 repository-profile closure and residual trusted-local shell compatibility.
