# BLK-SYSTEM-363 — Fallback Prohibition / Route-Closeout Gate Plan

**Status:** planned-for-execution
**Created:** 2026-06-13T19:43:32+10:00
**Repository HEAD:** `14345e4 docs: archive K2-024 route package`

## 1. Goal

Make the K2 route-closeout path fail closed when a feature/remediation loop did not produce a successful BLK-pipe route commit. Supervised external Codex fallback must become an explicit operator-authorized exception package, not a normal alternate route that can be normalized by BEO prose.

## 2. Scope

Implement a deterministic local validator in `python/beb_l2_blk_pipe_route.py` and persistent tests in `python/test_beb_l2_blk_pipe_route.py`.

The gate must distinguish:

1. **Normal governed route closeout:** at least one BLK-pipe route summary reports success, exit code `0`, a full 40-character commit hash, non-zero engine/final-message evidence, and validation evidence.
2. **Blocked closeout:** all route summaries are pre-dispatch/failed/non-executed evidence (`GIT_DIRTY`, `ENGINE_TIMEOUT`, empty commit, zero engine/final-message/validation counts) and no explicit fallback authorization is supplied.
3. **One-off fallback exception:** an explicit operator fallback authorization record binds the exact failed route status, target hash, allowed files, denied authorities, remediation ceiling, model, and required evidence. This is not a normal route closeout and does not grant reusable fallback authority.

## 3. Files to Touch

- Modify: `python/beb_l2_blk_pipe_route.py`
- Modify: `python/test_beb_l2_blk_pipe_route.py`
- Modify: `python/test_lean_documentation_policy.py` (extend lean closeout range to include sprint 363)
- Create: `docs/outcomes/BLK-SYSTEM-363_sprint-closeout.md`
- Create: this plan file, `docs/plans/blk-system-363_fallback-prohibition-route-closeout-gate.md`

No new root `docs/BLK-###` doctrine document is planned.

## 4. TDD Tasks

### Task 1 — RED: route summaries without route commit block closeout

Add a test that calls the new gate with a K2-024-like summary:

- `status: GIT_DIRTY`
- `exit_code: 7`
- `commit_hash: ""`
- `engine_logs_bytes: 0`
- `final_message_bytes: 0`
- `validation_log_count: 0`

Expected: gate status is blocked, normal closeout is false, external fallback is false, and blockers include missing route commit / non-executed route evidence.

### Task 2 — RED: successful BLK-pipe route passes normal closeout

Add a test with a successful BLK-pipe route summary:

- `status: SUCCESS`
- `exit_code: 0`
- full `commit_hash`
- non-zero `engine_logs_bytes`
- non-zero `final_message_bytes`
- `validation_log_count >= 1`

Expected: gate passes normal closeout and no fallback authorization is required.

### Task 3 — RED: fallback text/authorization is strict and bounded

Add tests proving:

- generic fallback authorization or prose is rejected;
- valid one-off authorization is accepted only as `fallback_exception_allowed`, not normal closeout;
- remediation rounds above the authorization ceiling are blocked;
- missing denied authorities or required evidence markers are blocked.

### Task 4 — GREEN implementation

Implement minimal helpers in `python/beb_l2_blk_pipe_route.py`:

- `evaluate_route_closeout_gate(route_summaries, fallback_authorization=None, fallback_remediation_rounds=0)`
- internal route-summary validator for success/non-executed classification;
- internal fallback-authorization validator with exact required fields and denied/evidence sets.

Integrate the gate into `scan_k2_final_closeout_artifacts(...)` by requiring route summaries for K2 final closeout scans. Existing tests must pass by supplying successful synthetic summaries.

### Task 5 — verification and closeout

Run:

```bash
TMPDIR=/var/tmp/blk-system-testtmp \
PYTHONPATH=python \
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache \
python3 -m unittest python.test_beb_l2_blk_pipe_route python.test_lean_documentation_policy -v

TMPDIR=/var/tmp/blk-system-testtmp \
PYTHONPATH=python \
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache \
python3 -m unittest discover -s python -p 'test_*.py'

git diff --check -- <exact changed paths>
```

If full discovery times out, use the repository-standard chunked module fallback and record it honestly.

## 5. Authority Boundary

This sprint grants no product/runtime authority. It does not authorize:

- external Codex fallback;
- live BLK-pipe dispatch;
- BEO publication or closeout execution;
- RTM generation or production `blk-link`;
- protected-body access;
- Kuronode source/Git mutation;
- package/network/model/browser/cyber tooling;
- reusable fallback policy.

It only adds a local deterministic gate that makes missing governed-route evidence fail closed unless an explicit one-off fallback authorization record is present.

## 6. Stop Conditions

Stop before commit if:

- focused tests do not go RED before implementation;
- fallback authorization can pass with generic prose or missing exact fields;
- K2 final closeout scan can pass without route summaries;
- hostile review finds fallback wording that can imply reusable or implicit authorization;
- lean documentation policy fails for sprint 363.
