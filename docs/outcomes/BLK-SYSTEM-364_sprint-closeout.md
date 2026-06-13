# BLK-SYSTEM-364 — Route Retarget / Fallback Record / Remediation Wording Gates Sprint Closeout

**Status:** Complete
**Date:** 2026-06-13
**Commit:** this commit (`feat: harden K2 route exception records`)

## 1. Objective

Strengthen the BLK-SYSTEM-363 route-closeout gate coverage for operator items 1 and 3–6:

1. Treat dirty/source-residue dispatch as a sterile clean-worktree retarget planning case, not as fallback pressure.
2. Require fallback exception authorization to be represented by a persistent, hash-bound record shape.
3. Enforce remediation round ceilings beyond the fallback-authorization happy path.
4. Require hostile-review remediation evidence to remain BLK-pipe-routed unless explicitly classified as a fallback exception.
5. Treat fallback/timeout/dirty/no-route wording in K2 BEO/closeout prose as toxic unless successful BLK-pipe route evidence or a valid fallback exception record is bound.

## 2. Files Changed

- `python/beb_l2_blk_pipe_route.py`
  - Added fallback authorization record write/load helpers.
  - Hardened one-off fallback exception validation to require persisted record identity, trusted-root loading, record hash verification, exact record-object comparison, observed failed-route artifact file verification, target-hash binding, and K2 sequence binding.
  - Added `build_default_clean_worktree_retarget_plan` for deterministic sterile retarget planning without cleanup, worktree creation, dispatch, or fallback authority.
  - Added `evaluate_remediation_route_policy` with BLK-pipe route artifact checks, contiguous remediation-round rules, file/hash-bound round-3 root-cause review evidence, and over-ceiling blocking.
  - Extended `scan_k2_final_closeout_artifacts` with final-BEO target-hash binding, remediation policy integration, and fallback-wording scans across BEO text, caller-supplied closeout paths, and discovered sibling closeout files.
- `python/test_beb_l2_blk_pipe_route.py`
  - Added RED/GREEN coverage for sterile retarget planning, fallback record round-tripping, fabricated/unbound fallback records, missing and mismatched route-summary artifacts, BEO/route target-hash mismatch, remediation identity mismatch, non-list/sparse remediation attempts, boolean-only and unverified review evidence, and broad fallback wording variants.
- `python/test_lean_documentation_policy.py`
  - Extended lean closeout range coverage through BLK-SYSTEM-364.
- `docs/plans/blk-system-364_route-retarget-fallback-record-remediation-wording-gates.md`
  - Captured the authority-sensitive sprint plan and stop conditions.
- `docs/outcomes/BLK-SYSTEM-364_sprint-closeout.md`
  - This single outcome closeout.

## 3. Implementation Summary

### Sterile retarget planning

`build_default_clean_worktree_retarget_plan(...)` now turns a dirty/source-residue preflight into a deterministic clean-worktree manifest candidate using the default clean-worktree path. The result remains advisory/planning-only:

- `fallback_authorized: False`
- `source_cleanup_authorized: False`
- `worktree_creation_authorized: False`
- `dispatch_authorized: False`
- `manifest_approval_required: True`

### Persistent fallback authorization records

The route-closeout fallback exception path now rejects fabricated in-memory authorization dictionaries. A valid exception must bind:

- a persisted `FALLBACK-AUTH-K2-###.json` record under trusted roots;
- record SHA-256 via `authorization_record_sha256`;
- exact object equality between loaded record + supplied authorization object;
- observed failed route summary path and SHA, verified against an actual persisted route summary file;
- observed failed route status;
- observed target hash;
- matching K2 sequence in `fallback_auth_id`;
- exact denied-authority and evidence-required sets.

Fallback exceptions still return `ROUTE_CLOSEOUT_GATE_FALLBACK_EXCEPTION`, not normal BLK-pipe success.

### Remediation route policy

`evaluate_remediation_route_policy(...)` now classifies hostile-review remediation evidence separately from primary route success:

- non-BLK-pipe remediation attempts block closeout;
- remediation route summaries must carry successful BLK-pipe route evidence backed by a regular hash-verified route-summary artifact;
- scanner-integrated remediation must match the closeout BEO/BEB/L2 identity and route target context;
- remediation rounds must be contiguous and one-record-per-round;
- round 2 emits warning evidence;
- round 3 requires structured root-cause review evidence whose file exists and matches the bound SHA-256;
- more than 3 rounds blocks closeout.

### Route and BEO target binding

Normal successful route closeout now requires regular hash-verified route-summary artifact evidence rather than only an in-memory summary dictionary. The K2 final closeout scanner also compares final BEO `target_hash` to the target hashes carried by route summaries so route evidence from another target cannot satisfy the closeout.

### Toxic fallback wording scan

The K2 final closeout scanner now detects fallback-like prose variants including:

- supervised/external Codex fallback;
- manual Codex patch;
- dirty source fallback;
- fallback remediation/final-message wording;
- `ENGINE_TIMEOUT` and `engine timeout`;
- `GIT_DIRTY`, `git dirty`, and dirty-worktree wording;
- no-route/no route commit wording;
- empty `commit_hash` fields.

Such wording blocks when route-closeout evidence is blocked and no valid fallback exception record is bound.

## 4. Verification

### RED evidence observed

The new hostile-review remediation regressions initially failed as intended before hardening:

```text
test_route_closeout_gate_rejects_fabricated_or_unbound_fallback_authorization_records ... ERROR
TypeError: evaluate_route_closeout_gate() got an unexpected keyword argument 'fallback_authorization_trusted_roots'

test_remediation_route_policy_rejects_non_list_sparse_rounds_and_boolean_review ... FAIL
AssertionError: 'REMEDIATION_ROUTE_POLICY_PASS' != 'REMEDIATION_ROUTE_POLICY_BLOCKED'

test_k2_final_closeout_scan_rejects_remediation_route_summary_identity_mismatch ... FAIL
AssertionError: 'K2_FINAL_CLOSEOUT_SCAN_PASS' != 'K2_FINAL_CLOSEOUT_SCAN_BLOCKED'

test_k2_final_closeout_scan_blocks_fallback_wording_variants_and_discovers_closeout_files ... FAIL
AssertionError: 'FALLBACK_WORDING_REQUIRES_ROUTE_GATE_EVIDENCE' not found in {'ROUTE_CLOSEOUT_GATE_BLOCKED'}
```

A second hostile review found four additional fail-open classes. Their RED regressions also failed before the second hardening pass:

```text
test_route_closeout_gate_rejects_successful_route_without_verified_artifact ... FAIL
AssertionError: 'ROUTE_CLOSEOUT_GATE_PASS' != 'ROUTE_CLOSEOUT_GATE_BLOCKED'

test_route_closeout_gate_rejects_fabricated_or_unbound_fallback_authorization_records ... FAIL
AssertionError: 'ROUTE_CLOSEOUT_GATE_FALLBACK_EXCEPTION' != 'ROUTE_CLOSEOUT_GATE_BLOCKED'

test_remediation_route_policy_rejects_non_list_sparse_rounds_and_boolean_review ... FAIL
AssertionError: 'REMEDIATION_ROUTE_POLICY_BLOCKED' != 'REMEDIATION_ROUTE_POLICY_PASS'

test_k2_final_closeout_scan_rejects_primary_route_target_hash_mismatch ... FAIL
AssertionError: 'K2_FINAL_CLOSEOUT_SCAN_PASS' != 'K2_FINAL_CLOSEOUT_SCAN_BLOCKED'
```

A final targeted review found one remaining fallback artifact-content laundering gap. Its RED regression failed before the final hardening pass:

```text
test_route_closeout_gate_rejects_fabricated_or_unbound_fallback_authorization_records ... FAIL
AssertionError: 'ROUTE_CLOSEOUT_GATE_FALLBACK_EXCEPTION' != 'ROUTE_CLOSEOUT_GATE_BLOCKED'
```

### Focused GREEN evidence

Focused hostile-review remediation tests now pass:

```text
Ran 4 tests in 0.005s

OK
```

Full touched route module now passes:

```text
Ran 78 tests in 1.003s

OK
```

Lean documentation policy now passes after creating this one closeout:

```text
Ran 8 tests in 0.140s

OK
```

Focused combined suite passes:

```text
Ran 86 tests in 1.169s

OK
```

Broad Python verification was run in cache-safe chunks after a single all-module wrapper hit the 600s tool limit. Aggregate evidence:

```text
166 test modules covered
1657 tests run
35 skipped
0 failures
0 errors
```

Chunk evidence:

```text
modules 001-020: Ran 367 tests in 2.062s — OK (skipped=34)
modules 021-040: Ran 164 tests in 74.843s — OK
modules 041-060: Ran 282 tests in 6.566s — OK
modules 061-080: Ran 315 tests in 8.737s — OK
modules 081-100: Ran 108 tests in 2.810s — OK
modules 101-120: Ran 140 tests in 1.035s — OK (skipped=1)
modules 121-140: Ran 126 tests in 0.680s — OK
modules 141-160: Ran 121 tests in 3.217s — OK
module 161: Ran 8 tests in 95.467s — OK
module 162: Ran 4 tests in 143.435s — OK
module 163: Ran 4 tests in 169.217s — OK
module 164: Ran 4 tests in 59.899s — OK
module 165: Ran 8 tests in 107.725s — OK
module 166: Ran 6 tests in 289.258s — OK
```

Commands used with cache-safe environment:

```bash
TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python3 -m unittest python.test_beb_l2_blk_pipe_route python.test_lean_documentation_policy -v
TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python3 -m unittest -q <chunked module list>
```

## 5. Hostile Review / Risk Check

Independent hostile review found six fail-open classes after the first GREEN pass:

1. fabricated fallback authorization dictionaries could pass without loading a persisted record;
2. fallback records were not bound to observed failed route-summary artifacts;
3. remediation evidence could be borrowed from another BEO/BEB/L2 target;
4. remediation rounds were fail-open for sparse/non-list inputs and bare boolean review evidence;
5. toxic fallback wording patterns missed common prose variants;
6. closeout wording scans checked only caller-supplied closeout paths.

All six classes were remediated with targeted RED tests and implementation changes. The resulting gate now requires trusted-root record loading, exact record equality, route-summary artifact binding, identity-bound remediation evidence, contiguous remediation rounds, structured review evidence, broader wording patterns, and sibling closeout discovery.

The second hostile review found four remaining fail-open classes:

1. fallback authorization could still reference a nonexistent failed route-summary artifact file;
2. final closeout could still pass when route `target_hash` did not match final BEO `target_hash`;
3. round-3 root-cause review evidence was syntactic and not file/hash-bound;
4. normal and remediation route success evidence could still be fabricated as in-memory summaries.

Those four were remediated with additional RED/GREEN coverage. Successful route summaries now require a regular hash-verified JSON artifact whose core fields match the in-memory summary, fallback authorization verifies the failed route-summary artifact file under trusted roots, final BEO `target_hash` must match route targets, and root-cause review evidence must point to an existing file whose bytes match the declared SHA-256.

The last targeted review found that a hash-bound but non-JSON arbitrary file could still be used as a fallback route-summary artifact. That gap was closed by admitting failed-route artifact refs to the fallback authorization set only after the same JSON/core-field verification used for successful route summaries.

## 6. Authority Boundary

This sprint does not authorize or perform:

- external Codex fallback;
- live BLK-pipe dispatch;
- BEO publication, signing, storage, ledger, rollback, or closeout execution;
- RTM generation or production `blk-link`;
- protected-body access;
- Kuronode source/Git mutation;
- source cleanup;
- worktree creation;
- package-manager/network/model/browser/cyber tooling;
- reusable fallback policy.

The changes are deterministic local validators, scanners, tests, a plan, and one closeout.

## 7. Documentation Burden Check

No new root `docs/BLK-###` doctrine document was created. BLK-SYSTEM-364 produced one sprint outcome document plus one pre-execution plan because the sprint changed authority-sensitive route/fallback/remediation gates. No per-task outcome documents were created.
