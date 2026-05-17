# BLK-SYSTEM-216 — Codex Permission Profile Containment Drill Sprint Closeout

**Status:** Complete
**Date:** 2026-05-17
**Commit:** this commit (`feat: record Codex containment contract`)

## 1. Objective

Plan and execute BLK-SYSTEM-216 as a bounded Codex configuration containment drill, then create a durable BLK-### document for Codex configuration because no current root BLK doc captured the Codex 0.130.0 permission-profile contract.

## 2. Files Changed

- `docs/BLK-121_codex-configuration-and-containment-contract.md`
- `python/product_codex_config_containment_216.py`
- `python/test_product_codex_config_containment_216.py`
- `python/blk_pipe_dry_run_orchestrator.py`
- `python/test_blk_pipe_dry_run_orchestrator.py`
- `testdata/engines/codex-dry-run`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_lean_documentation_policy.py`
- `docs/outcomes/BLK-SYSTEM-216_sprint-closeout.md`

## 3. Implementation Summary

- Added BLK-121 as the durable Codex configuration and containment contract.
- Recorded Codex CLI 0.130.0 permission-profile behavior in `product_codex_config_containment_216.py` with exact denied-authority flags, advisory telemetry rules, sandbox failure evidence, and external-containment fallback.
- Updated the dry-run Codex fixture payload away from stale legacy `--isolated`, `--yes`, `--dry-run`, and direct `--deny-read` flags toward modern `--ephemeral`, `--ignore-user-config`, `--ignore-rules`, disabled hooks/plugins/goals, JSONL telemetry, and final-message artifact capture.
- Advanced BLK-077/079 and the executable current-state gate to the BLK-SYSTEM-216 marker and package hash.

BLK-SYSTEM-216 package hash:

```text
blk216_codex_config_containment_package_hash=sha256:3e1cf8a9dcbb6dc8826d203d65b26ed01649ad1de0b6a3eda7e8d7741ec7434e
```

## 4. Verification

RED evidence was observed before implementation:

```text
FAILED (failures=1, errors=1)
ModuleNotFoundError: No module named 'product_codex_config_containment_216'
AssertionError: '--ephemeral' not found in ['exec', '-', '--json', '--isolated', '--yes', '--deny-read=**/.git/**', '--deny-read=**/node_modules/**', '--deny-read=**/.env*', '--dry-run']
```

Focused GREEN evidence after implementation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_product_codex_config_containment_216 python.test_blk_pipe_dry_run_orchestrator.DryRunOrchestratorPayloadTest.test_build_payload_includes_modern_codex_exec_isolation_args
```

Codex sandbox smoke evidence:

```text
CODEX_HOME=<temp-with-config-toml-containing-permissions.blk-smoke> codex sandbox linux --permissions-profile blk-smoke -C /home/dad/BLK-System true
bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
```

Final verification after hostile-review remediation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
Ran 1347 tests in 14.461s
OK (skipped=35)

go test ./...
ok github.com/camcamcami/BLK-System/cmd/blk-pipe
ok github.com/camcamcami/BLK-System/internal/contracts
ok github.com/camcamcami/BLK-System/internal/engine
ok github.com/camcamcami/BLK-System/internal/execguard
ok github.com/camcamcami/BLK-System/internal/gitguard
ok github.com/camcamcami/BLK-System/internal/pipe
ok github.com/camcamcami/BLK-System/internal/runtimeguard
ok github.com/camcamcami/BLK-System/internal/testutil
ok github.com/camcamcami/BLK-System/internal/validation
ok github.com/camcamcami/BLK-System/internal/validationprofiles

git diff --check -- <exact changed paths>
PASS
```

## 5. Hostile Review / Risk Check

PASS after remediation.

- Legacy exec flag drift: remediated by removing direct dry-run `--deny-read`, `--isolated`, `--yes`, and `--dry-run` from the repository dry-run fixture payload.
- Permission-profile overclaim: BLK-121 and the package state that permission profiles are direct enforcement only when native sandbox/external containment enforces them; local host sandbox remains unavailable.
- Approval/sandbox conflation: BLK-121 explicitly separates sandbox mode from approval policy.
- Telemetry overclaim: JSONL/final-message artifacts remain advisory only; canonical evidence remains Git diff, exact allowlists, validation, and hostile audit.
- Authority laundering: tests reject Codex approval wording, production sandbox overclaims, protected body references, package/network tooling, and BEO publication wording in caller-controlled fields.

## 6. Authority Boundary

BLK-SYSTEM-216 does not grant live tactical LLM execution, live Codex execution, reusable Codex dispatch, BLK-pipe dispatch, production BLK-test MCP, BEB dispatch, BEO closeout execution, BEO publication/signing/storage/ledger authority, RTM generation, production `blk-link`, drift rejection, coverage truth, protected BLK-req body reads/copying/parsing/hashing/scanning/mutation, broad target/source/Git mutation, package-manager/network/model/browser/cyber tooling, or production-isolation claims.

`danger-full-access` remains a host workaround only inside external containment. Codex telemetry remains advisory evidence only.

## 7. Documentation Burden Check

A new BLK doc was intentionally created as `BLK-121` because the user requested a durable Codex configuration document and the existing Codex BLK docs (`BLK-040`/`BLK-041`) covered old deterministic fixture boundaries rather than the current Codex 0.130.0 permission-profile contract.

Only one BLK-SYSTEM-216 outcome document was produced.
