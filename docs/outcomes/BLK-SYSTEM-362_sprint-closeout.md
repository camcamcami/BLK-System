# BLK-SYSTEM-362 — K2 Route Evidence and Closeout Automation Hardening Sprint Closeout

**Status:** Complete
**Date:** 2026-06-13
**Commit:** this commit (`feat: harden K2 route evidence closeout automation`)

## 1. Objective

Implement the BLK-System maintenance package selected from the K2-023 retrospective:

- archive sanitized K2 route evidence inside each route package instead of relying on `/tmp` paths;
- add a reusable K2 Agent A promotion-request/preflight readiness profile with hostile evidence-graph probes;
- add a final K2 BEO/roadmap/Obsidian mirror reconciliation scanner;
- add a repo-local hygiene scanner for accidental `__pycache__` / `.pyc` residue before exact-path staging;
- keep all changes non-authorizing and route/closeout focused.

No root `docs/BLK-###` doctrine document was created.

## 2. Files Changed

- `python/beb_l2_blk_pipe_route.py`
- `python/test_beb_l2_blk_pipe_route.py`
- `python/test_lean_documentation_policy.py`
- `docs/outcomes/BLK-SYSTEM-362_sprint-closeout.md`

## 3. Implementation Summary

### Route evidence archive helper

Added `archive_k2_route_evidence(...)` to materialize sanitized route evidence under a package-local `route-evidence/` folder:

- compact canonical `route-summary-###.json` copies;
- copied `codex-final-message-###.md` artifacts when present;
- `evidence-index.json` binding per-route summary and final-message hashes;
- explicit false authority flags for dispatch, BEO publication, RTM generation, and reusable Codex dispatch;
- fail-closed rejection of raw route logs (`engine_logs`, `validation_logs`, `stdout`, `stderr`, `raw_report`, `raw_result`, `validation_output`/output aliases, and raw-marker final-message artifacts) or `raw_logs_embedded=true`;
- strict archive allowlisting so caller-supplied extra fields are not copied into package-local route summaries.

### Agent A promotion-request readiness profile

Added `kuronode-agent-a-promotion-request-v1`, with KAPR probes covering:

- pure-data request/preflight-only semantics;
- JSON-like finite evidence graph restriction;
- non-plain container rejection (`Map`, `Set`, typed arrays, class instances, etc.);
- `NaN` / `Infinity` / `null` hash-alias traps;
- own enumerable `__proto__` evidence;
- proxy/getter/revoked-proxy/accessor/descriptor traps;
- primitive `contentFingerprint` / candidate identity requirements;
- nested `blk-link`, RTM, BEO publication, provider-call, source/Git mutation, save/export/session-persistence, and approval-capture denial;
- deep-freeze/false denied-authority requirements;
- hostile closeout probe checklist coverage.

The profile is advisory until explicitly included in a BEB/L2 drop. It does not auto-authorize source/Git mutation or dispatch.

### Final BEO/roadmap/mirror reconciliation scanner

Added `scan_k2_final_closeout_artifacts(...)` to fail closed when final K2 closeout artifacts are inconsistent:

- final BEO placeholder/status/metadata scan;
- mandatory expected final BEO SHA check;
- expected closeout metadata commit binding;
- explicit roadmap `first_unconsumed_sequence: null` check;
- stale pending-dispatch wording check;
- exactly one visible Obsidian `BEO-K2-###` mirror check;
- visible mirror metadata check for non-authoritative header plus canonical SHA/commit.

### Repo-local hygiene scanner

Added `scan_repo_local_hygiene(...)` to report repo-local `__pycache__` and `.pyc` artifacts before staging. It reports only; it does not mutate the repository or authorize staging.

## 4. Verification

RED evidence:

```text
TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python -m unittest python.test_beb_l2_blk_pipe_route
ImportError: cannot import name 'archive_k2_route_evidence' from 'beb_l2_blk_pipe_route'
FAILED (errors=1)

TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python -m unittest python.test_lean_documentation_policy.LeanDocumentationPolicyTest.test_new_sprints_use_one_outcome_only
FAIL: test_new_sprints_use_one_outcome_only
AssertionError: False is not true : BLK-SYSTEM-362 closeout missing
FAILED (failures=1)
```

Focused GREEN evidence:

```text
TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python -m unittest python.test_beb_l2_blk_pipe_route
.........................................................
----------------------------------------------------------------------
Ran 57 tests in 0.952s

OK
```

Hostile-review remediation RED evidence:

```text
python -m unittest \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_archive_k2_route_evidence_materializes_sanitized_index_inside_package \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_k2_final_closeout_scan_checks_beo_hash_roadmap_and_visible_mirrors
FAIL: unexpected_safe_field unexpectedly archived in route-summary-001.json
```

Post-remediation focused GREEN evidence:

```text
python -m unittest \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_archive_k2_route_evidence_materializes_sanitized_index_inside_package \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_k2_final_closeout_scan_checks_beo_hash_roadmap_and_visible_mirrors
..
----------------------------------------------------------------------
Ran 2 tests in 0.010s

OK
```

Second-review remediation RED evidence:

```text
python -m unittest \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_archive_k2_route_evidence_materializes_sanitized_index_inside_package \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_k2_final_closeout_scan_checks_beo_hash_roadmap_and_visible_mirrors
FAIL: beo_publication_authorized archived as True
FAIL: MISSING_ROADMAP_PATHS not reported
```

Third-review remediation RED evidence:

```text
python -m unittest \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_archive_k2_route_evidence_materializes_sanitized_index_inside_package \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_k2_final_closeout_scan_checks_beo_hash_roadmap_and_visible_mirrors
FAIL: final_message_sha256 missing did not raise
FAIL: uppercase NULL accepted as explicit null
```

Fourth-review remediation RED evidence:

```text
python -m unittest \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_archive_k2_route_evidence_materializes_sanitized_index_inside_package \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_k2_final_closeout_scan_checks_beo_hash_roadmap_and_visible_mirrors
FAIL: invalid archived SHA fields were copied
FAIL: blank Canonical commit passed mirror metadata scan
FAIL: whitespace-mutated first_unconsumed_sequence line passed
```

Fifth-review remediation RED evidence:

```text
python -m unittest \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_archive_k2_route_evidence_materializes_sanitized_index_inside_package \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_k2_final_closeout_scan_checks_beo_hash_roadmap_and_visible_mirrors
FAIL: nested status object with authority claims archived
FAIL: uppercase FIRST_UNCONSUMED_SEQUENCE duplicate passed
```

Sixth-review remediation RED evidence:

```text
python -m unittest python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_archive_k2_route_evidence_materializes_sanitized_index_inside_package
FAIL: final-message authority claims archived
FAIL: protected-looking final-message artifact path accepted
```

Final focused GREEN evidence:

```text
python -m unittest \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_archive_k2_route_evidence_materializes_sanitized_index_inside_package \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_k2_final_closeout_scan_checks_beo_hash_roadmap_and_visible_mirrors
..
----------------------------------------------------------------------
Ran 2 tests in 0.010s

OK

python -m unittest python.test_beb_l2_blk_pipe_route
.........................................................
----------------------------------------------------------------------
Ran 57 tests in 0.967s

OK

python -m unittest python.test_lean_documentation_policy
........
----------------------------------------------------------------------
Ran 8 tests in 0.146s

OK
```

Final chunked Python verification evidence:

```text
python -m unittest $(sed -n '1,40p' /var/tmp/blk-system-modules.txt)
Ran 510 tests in 76.818s
OK (skipped=34)

python -m unittest $(sed -n '41,80p' /var/tmp/blk-system-modules.txt)
Ran 597 tests in 15.191s
OK

python -m unittest $(sed -n '81,120p' /var/tmp/blk-system-modules.txt)
Ran 248 tests in 3.855s
OK (skipped=1)

python -m unittest $(sed -n '121,160p' /var/tmp/blk-system-modules.txt)
Ran 247 tests in 3.880s
OK

python -m unittest $(sed -n '161,162p' /var/tmp/blk-system-modules.txt)
Ran 12 tests in 238.100s
OK

python -m unittest $(sed -n '163,164p' /var/tmp/blk-system-modules.txt)
Ran 8 tests in 225.769s
OK

python -m unittest $(sed -n '165p' /var/tmp/blk-system-modules.txt)
Ran 8 tests in 107.369s
OK

python -m unittest $(sed -n '166p' /var/tmp/blk-system-modules.txt)
Ran 6 tests in 288.746s
OK

Aggregate chunked coverage: 1,636 tests, 35 skipped, all passing.
```

Hygiene/static verification:

```text
scan_repo_local_hygiene('.')
REPO_LOCAL_HYGIENE_PASS
[]

git diff --check -- python/beb_l2_blk_pipe_route.py python/test_beb_l2_blk_pipe_route.py python/test_lean_documentation_policy.py docs/outcomes/BLK-SYSTEM-362_sprint-closeout.md
# no output

Static added-line scan:
hardcoded secret patterns: none
shell/eval/deserialization/SQL patterns: none
```

## 5. Hostile Review / Risk Check

Risk surfaces reviewed locally before final verification:

- helpers are package/evidence/scan utilities only;
- no helper dispatches BLK-pipe or Codex;
- no helper mutates Kuronode source/Git state;
- no helper publishes BEOs, generates RTM, runs production `blk-link`, starts runtime tooling, or selects K2-024;
- route evidence archive rejects raw logs and binds copied artifacts by SHA;
- final closeout scanner requires explicit null next-sequence state and one visible BEO mirror;
- repo-local hygiene scan reports cache residue without deleting it.

Independent hostile review #1 returned **BLOCKED** and was remediated before final verification:

1. Route evidence archive could embed raw logs under unrecognized fields such as `validation_output`.
   - Remediation: route summaries are written from a strict allowlist, and raw-log key/value aliases fail closed.
2. Final BEO/mirror scanner could pass without an expected final BEO hash.
   - Remediation: missing `expected_final_beo_sha256` now returns `EXPECTED_FINAL_BEO_SHA_REQUIRED` and blocks reconciliation.
3. Final scanner could pass a roadmap that omitted `first_unconsumed_sequence` entirely.
   - Remediation: absence now returns `MISSING_FIRST_UNCONSUMED_SEQUENCE_NULL`; closed K2 roadmaps must explicitly say `first_unconsumed_sequence: null`.
4. Closeout verification/review placeholders were present.
   - Remediation: placeholders were replaced with concrete RED/GREEN, chunked full-suite, hygiene, diff-check, and hostile-review remediation evidence.

Independent hostile review #2 returned **BLOCKED** and was remediated before final verification:

1. Archived route summaries could carry caller-provided `true` values for denied authority fields.
   - Remediation: package-local archived route summaries now force `dispatch_authorized`, `beo_publication_authorized`, `rtm_generation_authorized`, reusable/broad dispatch, cleanup/worktree, and Codex-final-message-authoritative flags to `false` regardless of caller input.
2. The final scanner could pass when no roadmap paths or Obsidian execution root were supplied.
   - Remediation: missing roadmap inputs now return `MISSING_ROADMAP_PATHS`; missing mirror root returns `MISSING_OBSIDIAN_EXECUTION_ROOT`.
3. The roadmap null check accepted `none` or blank/comment-only values.
   - Remediation: the scanner now accepts only exact `first_unconsumed_sequence: null`; all other values block as `NEXT_K2_SEQUENCE_STILL_SELECTED` or missing-null evidence.

Independent hostile review #3 returned **BLOCKED** and was remediated before final verification:

1. The archive copied `final_message_artifact_path` verbatim even when it contained raw engine/validation markers.
   - Remediation: final-message artifact bytes are decoded with replacement and scanned for raw-route-log markers before copying.
2. The archive allowed a final-message artifact path without a submitted `final_message_sha256`.
   - Remediation: `route_summary.final_message_sha256` is now mandatory whenever `final_message_artifact_path` is archived and is verified before copying.
3. The roadmap null check still accepted uppercase `NULL` and inline-comment `null` values.
   - Remediation: roadmap closeout evidence now requires exactly one stripped line equal to `first_unconsumed_sequence: null`; comments, uppercase, blanks, duplicates, or alternate spellings fail closed.

Independent hostile review #4 returned **BLOCKED** and was remediated before final verification:

1. Archived allowlisted hash fields such as `engine_logs_sha256` and `validation_logs_sha256` could carry arbitrary text.
   - Remediation: optional archived SHA fields are validated as `sha256:<64 lowercase hex>` whenever non-empty.
2. Visible BEO mirror metadata could pass with a blank `Canonical commit:` line.
   - Remediation: visible BEO mirrors now require a full 40-character lowercase canonical commit hash.
3. Roadmap exact-line handling still tolerated leading/trailing whitespace.
   - Remediation: the scanner now compares the raw line exactly to `first_unconsumed_sequence: null`; leading spaces, trailing spaces, tabs, comments, duplicates, or alternate spellings fail closed.

Independent hostile review #5 returned **BLOCKED** and was remediated before final verification:

1. Nested allowlisted fields such as `status` could carry authority-laundering objects.
   - Remediation: archived allowlisted fields now require scalar sanitized evidence; integers, path/branch tokens, status tokens, booleans, and SHA fields each have explicit constraints.
2. Compact allowlisted strings could still carry raw/authority prose.
   - Remediation: archive scalar validation rejects raw-log markers and authority-laundering words such as approval/publication/RTM/blk-link/K2-024 markers; status must be a compact uppercase token.
3. Uppercase duplicate roadmap keys could evade the exact lowercase line check.
   - Remediation: roadmap selection-key detection is case-insensitive, while the only passing raw line remains exactly `first_unconsumed_sequence: null`.

Independent hostile review #6 returned **BLOCKED** and was remediated before final verification:

1. Copied Codex final-message artifacts could carry authority-laundering prose.
   - Remediation: final-message artifact text is now scanned for approval/publication/RTM/blk-link/K2-024 authority markers before copying.
2. `final_message_artifact_path` could point at protected-looking BLK-req/body paths.
   - Remediation: final-message artifact paths are rejected through the protected-artifact guard before regular-file checks, hashing, reading, or copying; resolved paths are checked again before SHA verification.

Independent hostile review #7 returned **PASS** after the sixth remediation:

```text
PASS
Blockers: none.
Focused tests: 65 tests OK.
Hygiene: REPO_LOCAL_HYGIENE_PASS.
Hostile probes: AUTHORITY_BLOCKED; PROTECTED_BLOCKED; duplicate uppercase roadmap selection blocked.
```

Local authority-risk recheck after remediation:

- helpers remain package/evidence/scan utilities only;
- no helper dispatches BLK-pipe or Codex;
- no helper mutates Kuronode source/Git state;
- no helper publishes BEOs, generates RTM, runs production `blk-link`, starts runtime tooling, or selects K2-024;
- route evidence archive rejects raw logs and binds copied artifacts by SHA;
- final closeout scanner requires explicit null next-sequence state and one visible BEO mirror;
- repo-local hygiene scan reports cache residue without deleting it.

## 6. Authority Boundary

BLK-SYSTEM-362 grants no new product/runtime authority. It does not authorize:

- Kuronode source/Git mutation;
- BEB/L2 dispatch beyond future exact approved drops;
- reusable Codex dispatch;
- BEO publication/signing/storage/ledger;
- BEO closeout execution;
- RTM generation;
- production `blk-link`;
- protected-body reads/copying/parsing/hashing/scanning;
- K2-024 or any next K2 selection;
- cleanup/deletion of cache artifacts.

## 7. Documentation Burden Check

Lean documentation preserved:

- one sprint closeout: `docs/outcomes/BLK-SYSTEM-362_sprint-closeout.md`;
- no per-task outcome docs;
- no new root `docs/BLK-###` document;
- BLK-001 through BLK-006 left untouched.
