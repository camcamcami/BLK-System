# BLK-SYSTEM-012.2 Task 002 Outcome

## Summary

Added a current-doctrine-only component naming drift gate in `python/test_blk_component_naming.py`.

The new test verifies that BLK-001 declares canonical component names for `blk-id`, `blk-relay`, and `blk-link`, and that active/current `docs/BLK-*.md` doctrine does not revert to stale `BLK-Link`, `RTM Aggregator`, or unbranded `Traceability Aggregator` names.

Historical Sprint 010 review wording was intentionally preserved. The existing historical-preservation marker in `python/test_active_doctrine_review_gates.py` was not changed.

## Files Changed

- `python/test_blk_component_naming.py`
- `docs/outcomes/BLK-SYSTEM-012.2_task-002-outcome.md`

## Verification

Captured: `2026-05-06T19:36:32+10:00`

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python/test_blk_component_naming.py -q`: PASS (`2 passed`)
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python/test_active_doctrine_review_gates.py -q`: PASS (`21 passed`)
- `git diff --check`: PASS
- cache cleanup: `rm -rf .pytest_cache python/__pycache__`

## Authority Statement

This task added a deterministic naming gate only. It did not authorize live RTM generation, BEO publication, new message transport, identity-provider implementation, active-vault reads, or drift-rejection behavior.

`BLK-SYSTEM-013` remains reserved for approval/source-evidence authorization mechanics.
