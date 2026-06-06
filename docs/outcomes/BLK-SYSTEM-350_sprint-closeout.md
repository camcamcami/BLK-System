# BLK-SYSTEM-350 Sprint Closeout — Kuronode K2 Filename Convention Support

## Scope

BLK-SYSTEM-350 updated the Kuronode BEB/L2 route package helper so future governed Kuronode V2 packages can use the local filename/ID convention without inheriting BLK-System sprint numbering.

Supported by this sprint:

- legacy `BEB_*` / `L2_*` route IDs remain accepted;
- new Kuronode V2 route IDs such as `BEB-K2-001` and `L2-K2-001` are accepted;
- optional artifact slugs can produce filenames such as `BEB-K2-001_Provider_Readiness_Status_Display.md` and `L2-K2-001_Provider_Readiness_Status_Display.md` inside the canonical BLK-System route package;
- optional Obsidian mirror generation writes view-only copies with canonical source/hash headers;
- BLK-System continues to consume the canonical route package and drop manifest, not the Obsidian mirror.

Not authorized or changed by this sprint:

- no Kuronode product implementation was dispatched;
- no BLK-pipe/Codex runtime route was executed;
- no BEO publication, RTM generation, protected-body access, production `blk-link`, signer/storage/ledger action, or product/source mutation authority was granted;
- no `BEO-K2-*` convention was introduced.

## Changed files

- `python/beb_l2_blk_pipe_route.py`
- `python/test_beb_l2_blk_pipe_route.py`

## RED / GREEN evidence

RED evidence:

- Added `test_prepare_kuronode_k2_drop_package_writes_named_artifacts_and_view_only_obsidian_mirrors`.
- Initial focused run failed because `prepare_beb_l2_drop_package()` did not accept the new `artifact_slug` parameter:
  - `TypeError: prepare_beb_l2_drop_package() got an unexpected keyword argument 'artifact_slug'`
- Added hostile-review-driven regression `test_obsidian_mirror_refuses_symlinked_roots_and_non_generated_overwrites`.
- Initial focused run failed because a symlinked mirror directory was accepted:
  - `AssertionError: RouteError not raised`

GREEN implementation:

- Extended BEB/L2 ID validation to accept `BEB-K2-###` and `L2-K2-###` while preserving legacy underscore IDs.
- Added optional `artifact_slug` support for route-package artifact filenames.
- Added optional `obsidian_mirror_dir` support for generated view-only mirrors.
- Hardened Obsidian mirror writes by rejecting symlinked mirror roots/components, rejecting destination symlinks, refusing to overwrite non-generated notes, and writing through a temporary file before final replacement.

## Hostile review

A hostile review was run against the initial diff. It found two blockers:

1. `obsidian_mirror_dir` was resolved before checking symlink components, allowing a symlinked mirror path to redirect writes.
2. Existing mirror destination files were chmodded and overwritten without proving they were generated view copies.

Both blockers were remediated with regression coverage and implementation changes. The resulting mirror behavior is intentionally bounded: mirrors are generated operator views only; canonical BEB/L2/drop files remain the route-package source of truth.

## Verification

Focused verification:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python3 -m unittest python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_prepare_kuronode_k2_drop_package_writes_named_artifacts_and_view_only_obsidian_mirrors -v
Ran 1 test in 0.022s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python3 -m unittest python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_obsidian_mirror_refuses_symlinked_roots_and_non_generated_overwrites -v
Ran 1 test in 0.015s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python3 -m unittest python.test_beb_l2_blk_pipe_route -v
Ran 32 tests in 0.615s
OK
```

Full Python discovery with `python3 -m unittest discover -s python -p 'test_*.py'` hit the 600-second Hermes foreground wrapper timeout, so the suite was verified by sorted module chunks under the same cache-safe environment.

Chunked verification summary:

```text
Chunk 1: 321 tests, OK, skipped=34
Chunk 2: 163 tests, OK
Chunk 3: 280 tests, OK
Chunk 4: 315 tests, OK
Chunk 5: 108 tests, OK
Chunk 6: 139 tests, OK, skipped=1
Chunk 7: 126 tests, OK
Chunk 8: 121 tests, OK
Chunk 9 split due long-running modules:
  test_verified_loop_beo_publication_approval_request_306_309: 8 tests, OK
  test_verified_loop_beo_publication_bounded_execution_kernel_329: 4 tests, OK
  test_verified_loop_beo_publication_live_challenge_guard_313_315: 4 tests, OK
  test_verified_loop_beo_publication_refresh_challenge_310_312: 4 tests, OK
  test_verified_loop_beo_publication_review_302_305: 8 tests, OK
  test_verified_loop_beo_publication_side_effect_trace_closure_330_333: 6 tests, OK
```

Whitespace verification:

```text
git diff --check -- python/beb_l2_blk_pipe_route.py python/test_beb_l2_blk_pipe_route.py
exit 0
```

## Outcome

BLK-SYSTEM-350 is complete. BLK-System can now prepare hash-bound Kuronode V2 route packages using `BEB-K2-###` / `L2-K2-###` names and produce non-authoritative Obsidian view mirrors while keeping dispatch authority tied to the canonical BLK-System route package.
