# BLK-032 — Track I live health-check boundary

**Status:** Active boundary contract — fixture-only / not live health-check authority
**Sprint:** BLK-SYSTEM-029
**BLK-024 track:** Track I — Operator UX, observability, and escalation
**Maturity:** L0 doctrine boundary with L1 local fixtures

---

## 1. Boundary contract — not live health-check authority

BLK-032 defines the Track I live health-check boundary. It is a boundary contract — not live health-check authority. It exists so a later sprint can request tightly scoped execution authority with fixed command profiles, bounded output, and explicit no-authority semantics.

The active fixture vocabulary is:

- `HEALTH_CHECK_BOUNDARY_FIXTURE_ONLY`
- `HEALTH_CHECK_PROFILE_FIXTURE_ONLY`
- `HEALTH_CHECK_RESULT_FIXTURE_ONLY`
- `HEALTH_CHECK_ESCALATION_FIXTURE_ONLY`
- `HEALTH_CHECKS_NOT_EXECUTED`
- `HEALTH_CHECK_AUTHORITY_NOT_GRANTED`

These markers mean that health-check profiles and results are caller-supplied fixture metadata. They do not prove a command ran and do not authorize a command to run.

---

## 2. Classification vocabulary

Health-check surfaces use exactly three planning classifications:

- `ADVISORY_ONLY` — useful operator context only.
- `BLOCKING_IF_LATER_EXECUTION_AUTHORIZED` — may block a later explicitly approved live runner, but only after that later sprint grants execution authority.
- `FORBIDDEN_IN_HEALTH_CHECK` — not a valid health-check action or field.

A fixture result may report caller-supplied PASS or FAIL evidence, but health-check PASS remains advisory. A PASS never grants approval to dispatch BLK-pipe, start BLK-test, publish BEOs, generate RTM, reject drift, mutate source, clean Git state, or read protected vaults.

---

## 3. Allowed future command profile shape

Future live command candidates must be fixed argv arrays only. Shell strings are forbidden.

The boundary records these inert candidate arrays for later human review:

1. `['go', 'test', './...']`
2. `['go', 'vet', './...']`
3. `['python3', '-m', 'unittest', 'discover', 'python', 'test_*.py']`
4. `['python3', '-m', 'unittest', 'python.test_active_doctrine_review_gates']`
5. `['git', 'status', '--short', '--branch']` as advisory read-only metadata only

The BLK-SYSTEM-029 fixture layer may preserve these arrays in normalized profiles. It does not execute commands, does not start subprocesses, does not call network services, and does not inspect files.

---

## 4. Forbidden health-check actions and fields

The following are explicitly forbidden in health-check profiles/results/escalation fixtures:

- shell strings are forbidden;
- network commands are forbidden;
- package-manager commands are forbidden;
- Git mutation commands are forbidden;
- protected-vault path/body scans are forbidden;
- BEO/RTM/drift authority fields are forbidden;
- environment and secret leakage is rejected.

This boundary does not run package managers, does not mutate Git or source state, does not capture approvals, does not authorize production BLK-test MCP, does not authorize authoritative BEO publication, does not authorize RTM generation, and does not authorize RTM drift rejection.

Forbidden examples include `curl`, `wget`, `ssh`, `scp`, `nc`, browser/API clients, `npm install`, `pip install`, `uv pip install`, `go get`, Git `commit`, `push`, `reset`, `checkout`, `stash`, `clean`, `revert`, `merge`, `rebase`, protected-vault body/path scans, BEO publication, signer/ledger/storage mutation, RTM IDs/ledgers/coverage matrices, and drift decisions.

---

## 5. No-read and no-side-effect flags

Every health-check fixture must expose explicit false side-effect booleans:

- `command_executed: false`
- `subprocess_started: false`
- `network_called: false`
- `file_read: false`
- `git_called: false`
- `package_manager_called: false`
- `source_mutated: false`
- `approval_captured: false`
- `protected_body_read: false`
- `active_vault_scanned: false`
- `beo_published: false`
- `rtm_generated: false`
- `drift_decision_made: false`

The boundary does not read protected BLK-req vault bodies, does not scan active-vault paths, does not inspect files, does not compute active-vault hashes, does not copy protected text, and does not expose raw host environment values.

---

## 6. Output bounds and redaction

Caller-supplied excerpts are bounded and redacted. The boundary requires that caller-supplied excerpts are bounded and redacted. Fixtures may preserve bounded stdout/stderr excerpts, evidence references, and evidence hashes, but must not embed raw logs or fetch referenced evidence.

Environment and secret leakage is rejected, including token-like, key-like, authorization, agent-socket, or `.env` material. Evidence references remain operator-supplied pointers only.

---

## 7. Future authority handoff

A later sprint may request live Track I health-check execution only if it preserves this boundary:

1. execution approval is explicit and current;
2. command profiles remain fixed argv arrays only;
3. output bounds and redaction are mechanically enforced;
4. network and package-manager denial is mechanically enforced;
5. protected-vault body reads and active-vault scans remain denied;
6. Git checks remain read-only advisory checks;
7. health-check PASS remains advisory and never implies BLK-pipe, BLK-test, BEO, RTM, drift, publication, storage, signing, or approval authority.

BLK-SYSTEM-029 grants no such live execution authority.
