# BLK-SYSTEM-085 Hostile Review — BEO Publication Pilot Execution Request Gate

**Status:** Passed after remediation
**Review date:** 2026-05-12
**Final functional review target HEAD:** `b9d43d3` (`b9d43d3a57768ff365247c029e5f0f4257262651`)
**Scope:** Task 004 hostile review for `BLK-SYSTEM-085 — BEO Publication Pilot Execution Request Gate`

## Verdict

BLK-SYSTEM-085 passes hostile review after three remediation rounds. The fixture remains a deterministic L0/L1 request gate only: it prepares a future explicit human approval request for a BEO publication pilot, but it does not approve, execute, publish, sign, store, append, roll back, generate RTM, read protected bodies, run BLK-test/Codex/BLK-pipe, scan or mutate target/source/Git state, invoke package/network/model/browser/cyber tooling, or claim production isolation.

The final passed review targeted the functional remediation now committed as `b9d43d3`.

## Required Probe Surface

Hostile review covered the Task 004 probe classes:

1. request package becoming publication approval;
2. request package becoming publication pilot execution;
3. self-consistent forged BLK-083 decision packages;
4. reused approval/run/request IDs, including cross-type reuse and upstream BEO/target/candidate IDs;
5. stale, expired, or replayed request envelopes;
6. multiple-frontier or secondary-frontier selection;
7. BEO decision-package readiness laundering into actual publication;
8. RTM authority before publication prerequisites;
9. percent-encoded, compact, camelCase, and acronym authority terms;
10. hidden target-repo, source/Git, protected-body, package-manager, network, model, browser, cyber, signer/storage/ledger/rollback, and production-isolation claims;
11. missing false side-effect flags and incomplete or duplicate denied-authority sets.

## Remediation History

### Round 1 — Initial hostile review failed

Initial hostile review failed with blockers:

- self-consistent forged BLK-083 decision packages were accepted when the attacker recomputed `decision_package_hash` and aligned request fields;
- fresh ID checks missed cross-type reuse of upstream envelope/run/approval/request IDs;
- calendar-expired request windows from 2000 were accepted if `expired`, `replayed`, and `stale` flags were false;
- compact/camel authority strings were accepted in future approval/run IDs for RTM, protected body, package manager, network, model, browser, cyber, signer/storage/ledger/rollback, production isolation, and target repo authority.

RED evidence after adding regression tests:

```text
Ran 7 tests in 0.034s

FAILED (failures=21)
```

GREEN remediation added:

- canonical BLK-083 fixture field and hash binding;
- cross-type upstream approval/run/request ID reuse rejection;
- fixed-baseline calendar-expiry rejection;
- expanded normalized authority marker coverage.

Focused GREEN evidence:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest -v python.test_beo_publication_pilot_execution_request

Ran 7 tests in 0.032s

OK
```

### Round 2 — Follow-up hostile review failed

A broad review attempt timed out and was discarded fail-closed. A follow-up hostile review then found two blockers:

- ID freshness still missed request package / pilot request / future approval / future run reuse across several upstream and current request identifiers;
- authority-marker coverage still missed variants such as `RTMAuthorized`, `targetRepositoryAuthority`, `sourceGitAuthorized`, `packageManagersAuthorized`, `networkAccessAuthorized`, `modelServicesAuthorized`, `browserToolsAuthorized`, `cyberToolsAuthorized`, `signerAuthorized`, `storageAuthorized`, `ledgerAuthorized`, `rollbackAuthorityGranted`, `productionSandboxAuthorized`, and `protectedBodyAuthorized`.

RED evidence after expanding regression tests:

```text
Ran 7 tests in 0.045s

FAILED (failures=27)
```

GREEN remediation added:

- exact uniqueness across request package, pilot request, future approval, and future run IDs;
- rejection of all upstream decision/envelope/pilot/future identifiers for every request identity field;
- no `datetime.now` dependency, using `FIXTURE_EVALUATION_AT = 2026-05-12T00:00:00+10:00` for deterministic stale-window rejection;
- expanded compact/camel authority marker coverage for the second-review variants.

Focused GREEN evidence:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest -v python.test_beo_publication_pilot_execution_request

Ran 7 tests in 0.043s

OK
```

### Round 3 — Final concern remediated

The next quick hostile review passed all explicitly requested probes but raised one concern: request identity fields could still reuse upstream `beo_id`, `target_id`, or `candidate_id`.

RED evidence after adding those cases:

```text
Ran 1 test in 0.014s

FAILED (failures=12)
```

GREEN remediation added upstream BEO, target, and candidate IDs to the consumed-identifier set for all request identity fields.

Focused GREEN evidence:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest -v python.test_beo_publication_pilot_execution_request

Ran 7 tests in 0.043s

OK
```

## Final Hostile Review Evidence

Final quick hostile review reported:

```json
{"passed":true,"blockers":[],"concerns":[],"summary":"Verified the current uncommitted remediation rejects request_package_id, pilot_request_id, future_approval_id_candidate, and future_run_id_candidate duplicates against each other and all listed upstream identifiers, including beo_id/target_id/candidate_id and prior pilot/future IDs. Compact authority strings still reject with authority-laundering errors. No datetime.now occurrence found in the reviewed module/test files. No files were created or modified."}
```

Final probe count:

```text
88 probes, 0 failures
```

The reviewed code was then committed as:

```text
b9d43d3 fix: harden blk 085 pilot request gate
```

## Verification Evidence

Closeout verification for the post-remediation line included:

```text
rm -rf /tmp/blk-system-pycache python/__pycache__ && PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'

Ran 852 tests

OK
```

```text
go test ./...

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

```text
go vet ./...
```

```text
git diff --check
```

## Authority Boundary

BLK-SYSTEM-085 grants no publication approval and performs no publication pilot execution. It does not write or publish a BEO, capture live approval, access signer key material, generate signatures, write immutable storage, append a ledger, run rollback/revocation/supersession, generate RTM, reject drift, compare active-vault hashes, read protected BLK-req bodies, dispatch BEBs, close out BEOs, run BLK-test/Codex/BLK-pipe, scan or mutate target repositories, mutate source/Git state, invoke package/network/model/browser/cyber tooling, or claim production isolation.

Any actual publication pilot still requires a fresh explicit human approval decision bound to the exact BLK-SYSTEM-085 request package.
