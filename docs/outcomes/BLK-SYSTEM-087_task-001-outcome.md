# BLK-SYSTEM-087 Task 001 Outcome — Exact Publication-Pilot Execution Fixture RED/GREEN

**Status:** Complete
**Date:** 2026-05-12T17:45:00+10:00
**Task:** Task 001 — Exact publication-pilot execution fixture RED/GREEN
**Commit:** pending at author time
**Remote:** pending at author time

---

## 1. Objective

Add a deterministic local fixture that consumes the BLK-SYSTEM-086 approval-decision package and executes exactly one local BEO publication pilot for `BEO-054-001`, without external authoritative publication or adjacent side effects.

## 2. Files Added/Changed

```text
python/test_beo_publication_pilot_execution.py
python/beo_publication_pilot_execution.py
docs/outcomes/BLK-SYSTEM-087_task-001-outcome.md
```

## 3. Behavior Implemented

- Added `build_beo_publication_pilot_execution`.
- The fixture validates the exact BLK-086 approval-decision package identity and recomputed hash.
- The fixture consumes the reserved run ID locally: `RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001`.
- The fixture emits a hash-bound local pilot publication artifact for `BEO-054-001` with `publication_mode: LOCAL_DETERMINISTIC_PILOT_ONLY`.
- Adjacent side effects remain false: no external authoritative publication, no live approval capture, no signer key material, no cryptographic signing, no immutable storage write, no public ledger mutation, no rollback/revocation/supersession, no RTM generation or drift rejection, no protected-body reads, no target-repo scan/mutation, no BLK-test/Codex/BLK-pipe runtime, no package/network/model/browser/cyber tooling, and no production isolation claim.

## 4. TDD Evidence

### 4.1 RED

The focused BLK-087 test module was written before implementation. Importing it failed because the production module did not exist:

```text
ModuleNotFoundError: No module named 'beo_publication_pilot_execution'
```

### 4.2 GREEN

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache-087 python -m unittest -v python.test_beo_publication_pilot_execution

test_builds_exact_local_pilot_publication_output_without_adjacent_side_effects ... ok
test_module_does_not_import_or_call_live_execution_tooling ... ok
test_rejects_bad_expiry_replay_proof_obligations_and_denied_authorities ... ok
test_rejects_forged_or_mismatched_upstream_approval_package ... ok
test_rejects_secret_adjacent_authority_source_git_and_tooling_laundering ... ok
test_rejects_wrong_frontier_or_adjacent_side_effect_flags ... ok
test_requires_exact_ids_from_blk086_approval_decision ... ok

Ran 7 tests in 0.028s

OK
```

## 5. Review Results

The fixture is closed-schema and hash-bound. The test suite includes forged-upstream, stale/replay/expiry, exact-ID, exact-set, forbidden-side-effect, authority-laundering, and live-tooling import/call regressions.

## 6. Final Verification

```text
git diff --check
```

`git diff --check` passed before commit.

## 7. Deviations / Notes

The first GREEN run exposed expected message-order mismatches in two negative tests. Implementation ordering was tightened so the validator reports `approval package must remain not executed` before lower-level flag checks and reports consumed execution IDs as stale/freshness violations before exact-ID mismatch.

## 8. Next Task

Task 002 — Doctrine and persistent gates.
