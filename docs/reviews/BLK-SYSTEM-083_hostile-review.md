# BLK-SYSTEM-083 Hostile Review — BEO Publication Decision Package / Pilot Request

**Status:** PASS after remediation
**Date:** 2026-05-12
**Scope:** BLK-SYSTEM-083 plan, fixture, doctrine, roadmap/current-state alignment, and closeout readiness

## 1. Review Question

Does BLK-SYSTEM-083 accidentally turn a review-only BEO Publication Decision Package / Pilot Request into publication approval, pilot execution, signer/storage/ledger/rollback side effects, RTM authority, protected-body access, target-repo authority, BLK-test/Codex/BLK-pipe runtime, tooling authority, or production isolation claims?

## 2. Reviewed Surfaces

```text
docs/plans/blk-system-083_beo-publication-decision-package-pilot-request.md
docs/BLK-083_beo-publication-decision-package-pilot-request.md
docs/BLK-077_blk-system-post-078-roadmap.md
docs/BLK-079_post-078-current-state-authority-index.md
python/beo_publication_decision_package.py
python/test_beo_publication_decision_package.py
python/blk_current_state_authority_index.py
python/test_blk_current_state_authority_index.py
python/test_active_doctrine_review_gates.py
```

## 3. Initial Hostile Review Result

Independent hostile review returned **BLOCKER** before remediation.

Findings:

1. The decision-package fixture recomputed `envelope_hash` but did not require the full BLK-060 envelope key set or validate nested signer/storage/ledger/rollback/audit/pilot-control objects.
2. The returned decision package did not expose enough review-visible upstream binding fields for pilot ID, run ID, approval ID, and policy hashes.
3. Future approval/run candidate IDs were not checked for reuse against the submitted BLK-060 envelope IDs.
4. Some allowed scalar fields used `scan=False`, permitting authority/secret laundering through IDs.
5. A second review found percent-encoded laundering variants such as `approved%2Dfor%2Dpublication`, `publish%42EO`, `RTM%47eneration`, `se%63ret`, and `to%6ben` were not decoded before scanning.

## 4. Remediation Applied

Remediation commit:

```text
a59329f fix: harden blk 083 decision package validation
```

Changes:

- Added exact top-level BLK-060 envelope key validation.
- Added exact nested policy/control/audit validators for signer, storage, ledger, rollback, audit bundle, and pilot controls.
- Required every nested no-side-effect flag to be explicitly false.
- Validated nested policy hashes and cross-bound audit hashes.
- Added review-visible upstream bindings to the output package:
  - target ref;
  - envelope pilot ID;
  - envelope run ID;
  - envelope approval ID;
  - signer/storage/ledger/rollback policy hashes;
  - audit bundle hash;
  - operator stop control;
  - pilot replay protection.
- Rejected future approval/run candidates that reuse the submitted envelope approval/run IDs.
- Scanned caller-controlled scalar IDs and identity strings for authority/secret laundering.
- Added iterative percent-decoding before normalization so encoded authority/secret strings fail closed.
- Added regression tests for all blockers.

## 5. Hostile Probe Evidence

Focused remediation tests:

```bash
rm -rf /tmp/blk-system-pycache && PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest -v python.test_beo_publication_decision_package
```

```text
Ran 10 tests in 0.033s

OK
```

Manual encoded-laundering probes:

```text
blocked 1: secret-bearing field
blocked 2: authority-laundering text
blocked 3: authority-laundering text
blocked 4: authority-laundering text
blocked 5: secret-bearing field
blocked 6: authority-laundering text
all encoded laundering probes blocked
```

Full suite after remediation:

```bash
rm -rf /tmp/blk-system-pycache && PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
```

```text
Ran 825 tests in 12.082s

OK
```

```bash
go test ./...
```

```text
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validationprofiles	(cached)
```

## 6. PASS / Denied Authority Matrix

| Risk | Result |
| --- | --- |
| Decision package becomes publication approval | PASS — approval flags remain false and exact denied-authority sets are tested. |
| Pilot request becomes pilot execution | PASS — execution flag is false and future explicit approval is required. |
| Self-consistent forged BLK-060 envelope laundering | PASS — exact envelope schema, nested validators, and canonical hash recomputation are enforced. |
| Nested signer/storage/ledger/rollback/audit/pilot-control side effects | PASS — nested explicit false flags are required and tested. |
| Reuse of submitted approval/run IDs as future candidates | PASS — reuse is rejected. |
| Scalar authority/secret laundering | PASS — caller-controlled strings are scanned, including percent-encoded variants. |
| RTM/drift/coverage/protected-body laundering | PASS — denied authorities and hostile probes fail closed. |
| Target-repo, BLK-test, Codex, BLK-pipe, tooling, production-isolation authority | PASS — fixture has no live-surface imports/calls and doctrine/index deny authority. |
| Stale roadmap guidance | PASS — BLK-077 and BLK-079 record BLK-SYSTEM-083 completion and require fresh approval for actual pilot execution. |

## 7. Final Verdict

**PASS after remediation.** BLK-SYSTEM-083 is review-ready as an L0/L1 BEO Publication Decision Package / Pilot Request fixture. It does not authorize actual BEO publication, publication pilot execution, signer/storage/ledger/rollback side effects, RTM generation, protected-body reads, target-repo scans/mutation, BLK-test/Codex/BLK-pipe runtime, tooling, or production-isolation claims.
