# BLK-SYSTEM-029 — Track I Health-Check Boundary Inventory

**Status:** Complete inventory — future health-check boundary evidence only
**Date:** 2026-05-08T11:52:55+10:00
**Plan:** `docs/plans/blk-system-029_track-i-live-health-check-boundary.md`
**BLK-024 track:** Track I — Operator UX, observability, and escalation
**Maturity:** L0 doctrine boundary supporting L1 local fixtures

---

## 1. Inventory Boundary

This inventory separates candidate Track I health checks from authority to execute them. It is not a live health-check runner, not a command executor, not a host-state inspector, not a package-manager/network probe, and not approval to mutate BLK-System or publish downstream artifacts.

Future commands are recorded as inert argv metadata only. Task 2 fixtures may normalize caller-supplied profile/result dictionaries and reject unsafe inputs, but must not run, spawn, read, scan, fetch, install, publish, generate RTM, decide drift, capture approval, or claim a live health-check PASS.

---

## 2. Classification Vocabulary

Each candidate surface is classified as one of:

- `ADVISORY_ONLY` — useful operator context if a later authorized runner supplies evidence, but never approval to mutate or proceed.
- `BLOCKING_IF_LATER_EXECUTION_AUTHORIZED` — a failed check could block a later explicitly approved live runner from continuing, but only after that later sprint grants execution authority.
- `FORBIDDEN_IN_HEALTH_CHECK` — must never be run or represented as a valid health-check action.

---

## 3. Candidate Health-Check Surface Inventory

| Surface | Candidate inert argv / evidence shape | Classification | Boundary rationale |
| --- | --- | --- | --- |
| Go toolchain readiness | `['go', 'test', './...']` | `BLOCKING_IF_LATER_EXECUTION_AUTHORIZED` | Tracks Go contract/build readiness. In this sprint the argv is metadata only; no subprocess starts. |
| Go vet readiness | `['go', 'vet', './...']` | `BLOCKING_IF_LATER_EXECUTION_AUTHORIZED` | Useful preflight once live execution is separately approved. It cannot mutate source or imply BLK-pipe success. |
| Python unittest readiness | `['python3', '-m', 'unittest', 'discover', 'python', 'test_*.py']` | `BLOCKING_IF_LATER_EXECUTION_AUTHORIZED` | Mirrors repository convention `PYTHONPATH=python` / `PYTHONDONTWRITEBYTECODE=1`; fixture does not execute or inspect imports. |
| Active doctrine gate readiness | `['python3', '-m', 'unittest', 'python.test_active_doctrine_review_gates']` | `BLOCKING_IF_LATER_EXECUTION_AUTHORIZED` | Later live runner may verify doctrine gates. This sprint only pins expected profile semantics. |
| Schema/doctrine fixture readiness | Caller-supplied result dictionary naming fixture suites and hashes | `ADVISORY_ONLY` | Health status can summarize supplied evidence; it cannot read protected requirement bodies or compute new canonical hashes. |
| Disabled BLK-test transport stub readiness | Caller-supplied descriptor/result showing disabled transport state | `ADVISORY_ONLY` | Confirms disabled-state vocabulary only. It must not start production BLK-test MCP or run a new smoke. |
| BLK-pipe binary/profile readiness | Caller-supplied result for fixed validation profiles or binary presence | `ADVISORY_ONLY` | BLK-pipe remains the execution/enforcement authority. Health fixtures cannot dispatch BLK-pipe. |
| Git clean-state advisory readiness | `['git', 'status', '--short', '--branch']` | `ADVISORY_ONLY` | Read-only candidate for later explicit execution authority. It must not become `commit`, `push`, `reset`, `checkout`, `stash`, `clean`, `merge`, or `rebase`. |
| Output-bound and redaction readiness | Caller-supplied bounded excerpt plus redaction markers | `BLOCKING_IF_LATER_EXECUTION_AUTHORIZED` | Later runners must bound output before presenting evidence. Fixtures must reject token floods and raw environment/secret leakage. |
| Network-denial readiness | Absence of network/API commands and explicit `network_called: false` | `BLOCKING_IF_LATER_EXECUTION_AUTHORIZED` | Health checks cannot call `curl`, `wget`, `ssh`, `scp`, `nc`, browsers, GitHub/Discord APIs, or model/network services. |
| Package-manager-denial readiness | Absence of install/update commands and explicit `package_manager_called: false` | `BLOCKING_IF_LATER_EXECUTION_AUTHORIZED` | Health checks cannot run `npm install`, `pip install`, `uv pip install`, `go get`, or package/update operations. |
| Protected-vault no-read readiness | Explicit `protected_body_read: false` and `active_vault_scanned: false` | `BLOCKING_IF_LATER_EXECUTION_AUTHORIZED` | Health checks must not read/copy/parse/hash protected BLK-req bodies or scan active-vault paths. |
| RTM/BEO disabled-authority readiness | Explicit `beo_published: false`, `rtm_generated: false`, `drift_decision_made: false` | `ADVISORY_ONLY` | Indicates disabled downstream authority only. It cannot publish BEOs, generate RTM, create coverage matrices, or reject drift. |
| Arbitrary shell strings | Any single shell string such as `go test ./...` or `bash -lc ...` | `FORBIDDEN_IN_HEALTH_CHECK` | Fixed argv arrays are required to avoid shell expansion and command-injection laundering. |
| Network commands | `curl`, `wget`, `ssh`, `scp`, `nc`, browser/API clients | `FORBIDDEN_IN_HEALTH_CHECK` | Network/API/model-service/cyber-tooling remains outside Track I fixture boundary. |
| Package installation/update commands | `npm install`, `pip install`, `uv pip install`, `go get`, package update commands | `FORBIDDEN_IN_HEALTH_CHECK` | Installing dependencies mutates environment and may contact network. |
| Git mutation commands | `commit`, `push`, `reset`, `checkout`, `stash`, `clean`, `revert`, `merge`, `rebase` | `FORBIDDEN_IN_HEALTH_CHECK` | Health checks cannot mutate repository state or perform rollback/rewrite actions. |
| Protected path/body scan commands | Any `docs/active`, protected-vault, body/read/parse/hash path scan | `FORBIDDEN_IN_HEALTH_CHECK` | Preserves BLK-req protected-body isolation and avoids active-vault scanning. |
| BEO/RTM/drift authority fields | Publication, signer, ledger, RTM ID/ledger/matrix, drift reject fields | `FORBIDDEN_IN_HEALTH_CHECK` | Prevents status/report fields from laundering downstream authority. |

---

## 4. Future Command Candidate Rules

Allowed future command candidates are inert fixed argv arrays only:

1. `['go', 'test', './...']`
2. `['go', 'vet', './...']`
3. `['python3', '-m', 'unittest', 'discover', 'python', 'test_*.py']`
4. `['python3', '-m', 'unittest', 'python.test_active_doctrine_review_gates']`
5. `['git', 'status', '--short', '--branch']` as advisory read-only metadata only

The fixture layer must reject shell strings, nested shell invocations, wrappers such as `bash`, `sh`, `python -c`, `node -e`, network tools, package managers, Git mutation subcommands, and any command candidate containing protected-vault/path/body scanning semantics.

---

## 5. Result Evidence Rules

A later authorized runner could supply result dictionaries, but this sprint's fixtures only normalize already-supplied evidence. A valid result fixture must preserve:

1. `HEALTH_CHECK_RESULT_FIXTURE_ONLY` as result vocabulary;
2. `HEALTH_CHECKS_NOT_EXECUTED` and `HEALTH_CHECK_AUTHORITY_NOT_GRANTED` markers;
3. bounded stdout/stderr excerpts only;
4. caller-supplied evidence references/hashes without fetching the referenced evidence;
5. explicit false side-effect booleans for command/subprocess/network/file/git/package/source/approval/protected-vault/BEO/RTM/drift surfaces;
6. `health_check_pass_grants_authority: false`.

It must reject PASS-as-approval wording, raw environment values, secret-looking keys, unbounded excerpts, unsupported top-level fields, and nested forbidden authority fields.

---

## 6. Acceptance Mapping for Task 2

Task 2 should prove via RED/GREEN tests that the health-check fixture layer:

- emits `HEALTH_CHECK_BOUNDARY_FIXTURE_ONLY`, `HEALTH_CHECK_PROFILE_FIXTURE_ONLY`, `HEALTH_CHECK_RESULT_FIXTURE_ONLY`, and `HEALTH_CHECK_ESCALATION_FIXTURE_ONLY` vocabulary;
- preserves `HEALTH_CHECKS_NOT_EXECUTED` and `HEALTH_CHECK_AUTHORITY_NOT_GRANTED` markers;
- allows only fixed inert argv candidate arrays listed above;
- rejects shell strings, wrappers, network commands, package managers, Git mutation commands, protected-vault/body/path scans, RTM/BEO/publication/drift fields, environment/secret leakage, and token floods;
- sets all no-side-effect booleans to `False`;
- packages bounded escalation evidence without embedding raw logs;
- contains no live execution, network, file-read, path-scan, GitHub/Discord API, or package-manager implementation surface.
