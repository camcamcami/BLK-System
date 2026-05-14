# BLK-112 — Structured Validation Profile argv Hardening

**Status:** Active BLK-pipe validation-profile hardening record — not runtime dispatch authority
**Date:** 2026-05-14
**Sprint:** BLK-SYSTEM-112
**Source finding:** `docs/reviews/BLK-SYSTEM_post-103_all-codebase-hostile-review-and-completion-roadmap.md` HR-006

## Purpose

BLK-SYSTEM-112 closes the repository-owned profile side of HR-006. Validation profiles no longer resolve to shell command strings for execution. They resolve to deterministic repository-owned argv/env specs, and Go `blk-pipe` executes those specs without `sh -c`.

## Required Markers

```text
BLK_SYSTEM_112_STRUCTURED_VALIDATION_PROFILE_ARGV_HARDENING
VALIDATION_PROFILES_RESOLVE_TO_STRUCTURED_ARGV_ENV_SPECS
REPOSITORY_OWNED_PROFILES_DO_NOT_EXECUTE_THROUGH_SH_C
RESOLVED_VALIDATION_ARGV_REPORTED_FOR_HOSTILE_AUDIT
LEGACY_VALIDATION_COMMANDS_REMAIN_TRUSTED_LOCAL_COMPATIBILITY_ONLY
```

## Enforced Behavior

1. `internal/validationprofiles` exposes structured `CommandSpec` records with `Argv` and `Env` fields.
2. `ResolveSpecs()` returns deep-copy structured specs; mutating a returned spec cannot mutate the registry.
3. `validation.RunSpecs()` invokes `execguard` with argv directly, not `sh -c`.
4. `blk-pipe` uses `RunSpecs()` for repository-owned `validation_profiles`.
5. Reports preserve human-readable `resolved_validation_commands` and exact `resolved_validation_argv` evidence.
6. Legacy free-form `validation_commands` still use the legacy shell runner and remain trusted-local compatibility only.

## Explicit Non-Authority

This record does not authorize BLK-pipe runtime dispatch against Kuronode or any target repository, BLK-test runtime, production MCP, BEO publication, RTM generation, RTM drift rejection, active-vault hash comparison, protected BLK-req body reads, package/network/model/browser/cyber tooling, signer/storage/ledger/rollback behavior, production sandbox/isolation claims, or source/Git mutation outside this BLK-System sprint commit.

## Finding Disposition

- HR-006 repository-owned profile shell execution: CLOSED for `validation_profiles`.
- HR-006 legacy free-form command shell execution: INTENTIONALLY RETAINED as trusted-local compatibility only and carried forward to BLK-SYSTEM-113 policy hardening.
