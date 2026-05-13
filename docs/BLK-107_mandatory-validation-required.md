# BLK-107 — Mandatory Validation Required

**Status:** Active BLK-pipe enforcement hardening record — not runtime dispatch authority
**Date:** 2026-05-14
**Sprint:** BLK-SYSTEM-107
**Source finding:** `docs/reviews/BLK-SYSTEM_post-103_all-codebase-hostile-review-and-completion-roadmap.md` HR-003

## Purpose

BLK-SYSTEM-107 closes the HR-003 no-validation execute path. Before this sprint, an execute payload could omit `validation_profiles` and `validation_commands`, reach the engine, and produce a commit with `validation_command_source: none`. That contradicted the BLK-003 syntax-gate requirement and weakened hostile audit evidence.

## Required Markers

```text
BLK_SYSTEM_107_MANDATORY_VALIDATION_REQUIRED
EXECUTE_PAYLOAD_REQUIRES_VALIDATION_PROFILE_OR_COMMAND
VALIDATION_REQUIRED_BEFORE_ENGINE_SIDE_EFFECTS
PYTHON_ADAPTER_VALIDATION_REQUIRED_FAIL_FAST_ONLY_GO_REMAINS_AUTHORITY
```

## Enforced Behavior

1. Go `Payload.Validate()` rejects execute payloads when both `validation_profiles` and `validation_commands` are empty.
2. Go `Run()` returns `INVALID_PAYLOAD` / `ExitInvalidPayload` before invoking the engine when validation is absent or explicitly empty.
3. Python `BlkPipeAdapter.execute_sprint()` rejects absent or explicitly empty validation before invoking `blk-pipe`.
4. Existing non-empty repository-owned `validation_profiles` remain accepted.
5. Existing non-empty `validation_commands` remain accepted only as transitional trusted-local compatibility; less-trusted/autonomous payload boundaries still require repository-owned profiles under BLK-004.
6. `revert` and `--health` remain outside the execute validation requirement.

## Explicit Non-Authority

This record does not authorize:

- BLK-pipe runtime dispatch against Kuronode or any target repository;
- BLK-test runtime, production MCP, or oracle promotion;
- BEO publication, signer/storage/ledger/rollback policy, or publication authority;
- RTM generation, RTM drift rejection, or production `blk-link`;
- protected BLK-req body reads or active-vault hash comparison;
- network/package-manager/model/browser/cyber execution;
- source/Git mutation outside the BLK-System sprint commit.

## Residual Follow-Up Boundary

BLK-SYSTEM-107 closes the no-validation bypass. It intentionally does not complete HR-006 validation-shell/profile hardening: free-form `validation_commands` and repository profile commands still execute through the existing shell-command validation runner. Future work must tighten that profile/command model before expanding less-trusted or autonomous execution authority.
