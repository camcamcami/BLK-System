# BLK-SYSTEM-117 Sprint Closeout — Version-Aware Staging Linter

**Status:** COMPLETE
**Date:** 2026-05-14
**Sprint:** BLK-SYSTEM-117
**Plan:** `docs/plans/blk-system-117_version-aware-staging-linter.md`
**Record:** `docs/BLK-117_version-aware-staging-linter.md`
**Hostile review:** `docs/reviews/BLK-SYSTEM-117_hostile-review.md`

## Summary

BLK-SYSTEM-117 adds the version-aware staging linter backend to `python/lint_artifacts.py`. Requirement drafts and use-case drafts are routed by staging path, draft metadata is validated against schema version 1.0, and violations return deterministic structured diagnostics.

## Required Markers

```text
BLK_SYSTEM_117_VERSION_AWARE_STAGING_LINTER
LINTER_ROUTES_REQUIREMENTS_AND_USE_CASES_BY_STAGING_PATH
DRAFT_METADATA_SCHEMA_VERSION_1_0_ENFORCED
ACTIVE_VAULT_BODY_READS_REJECTED_BY_LINTER
STRUCTURED_JSON_DIAGNOSTICS_RETURNED
NO_ACTIVE_PROMOTION_OR_HASH_ASSIGNMENT_BY_117
```

## RED/GREEN Evidence

RED failure observed before implementation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_req_legislative_gateway -v
ImportError: cannot import name 'lint_artifact' from 'lint_artifacts'
```

Focused GREEN check after implementation and BLK-117 record creation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_req_legislative_gateway -v
Ran 10 tests
OK
```

## Authority Boundary

BLK-SYSTEM-117 grants no active-vault body reads, no active-vault writes, no HITL approval capture, no baseline promotion, no exact-ID retrieval, no BLK-pipe dispatch, no BLK-test runtime, no BEO publication, no RTM generation or drift rejection, no target/source/Git mutation, no tooling authority, no signer/storage/ledger/rollback authority, and no production isolation claim.

## Next Slice

BLK-SYSTEM-118 may implement the staging draft writer using this linter as a gate. It must write only under staging directories and must keep `id: "TBD"`, `status: "DRAFT"`, and `version_hash: "PENDING"` for new drafts.
