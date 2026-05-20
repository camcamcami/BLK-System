# BLK-SYSTEM-290 — BLK-003 Loop Request Contract Sprint Closeout

**Status:** Complete
**Date:** 2026-05-21
**Commit:** this commit (`feat: add reusable BLK003 loop request path`)

## 1. Objective

Create the reusable BLK-003 loop request contract that binds the existing BLK-SYSTEM-241 loop kernel to the BLK-SYSTEM-286 speculative-quarantine approval timing contract.

## 2. Files Changed

- `python/blk003_loop_request_path_290_293.py`
- `python/test_blk003_loop_request_path_290_293.py`
- `docs/BLK-124_reusable-blk003-loop-request-path-contract.md`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_lean_documentation_policy.py`

## 3. Implementation Summary

BLK-SYSTEM-290 added `build_loop_request_contract_290(...)` and `validate_loop_request_contract_290(...)`. The contract requires exact request fields for future BEB-L2 routing, requires a promotion/purge gate hash, requires target-hash recheck, requires private-bwrap descriptor evidence for workspace-write, and keeps a separate exact execution package boundary.

Stable evidence:

```text
blk290_loop_request_contract_hash=sha256:c41030bda0df8850050dd7c816f73582b96e78632de262a50bee52cdeecf50e6
```

## 4. Verification

Final verification executed after hostile-review remediation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache-hostilefix2 python -m unittest python.test_blk003_loop_request_path_290_293 python.test_blk_current_state_authority_index python.test_lean_documentation_policy -v
Ran 32 tests in 0.961s — OK
```

```text
TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache-full python -m unittest discover -s python -p 'test_*.py'
Ran 1493 tests in 19.748s — OK (skipped=35)
```

```text
go test ./... — OK
security/trailing-whitespace scan OK for 12 paths
```

## 5. Hostile Review / Risk Check

Independent hostile review found three initial blockers: reconciliation trusted self-hashed binding/preflight dependencies, marker lists were presence-only, and documented hash assertions were static. Remediation now requires full upstream gate-stack revalidation in BLK-SYSTEM-293 reconciliation, exact marker tuple validation on all package levels, and dynamic doc-hash assertions. A second review found a BLK-124 scanner hit on `publish BEOs`; wording was changed and a BLK-124 scanner regression was added. Final hostile re-review result: PASS.

## 6. Authority Boundary

This sprint grants no BLK-pipe runtime, no live Codex dispatch, no reusable Codex dispatch, no relay runtime, no message dispatch, no approval reuse, no protected-body access, no BEO closeout execution, no BEO publication, no RTM generation, no production `blk-link`, no BLK-test MCP runtime, no source/Git mutation, no package-manager/network/model/browser/cyber tooling, and no production-isolation claim.

## 7. Documentation Burden Check

A new BLK-124 durable contract was created because the work defines a reusable request-path interface and authority boundary. Exactly one outcome closeout was produced for BLK-SYSTEM-290, with no per-task outcome documents.
