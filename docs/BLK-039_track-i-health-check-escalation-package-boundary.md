# BLK-039 — Track I health-check escalation package boundary

**Status:** Active pilot boundary — advisory health-check evidence packaging only
**Sprint:** BLK-SYSTEM-037
**BLK-024 track:** Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening
**Maturity:** BLK-024 L4 local pilot evidence packaging for already-returned fixed-profile health-check results only; not L5 production authority

---

## 1. Purpose

BLK-039 records the BLK-SYSTEM-037 boundary for packaging advisory health-check evidence into concise operator escalation bundles. It follows BLK-031 observability/runbook doctrine and BLK-034 through BLK-038 advisory health-check boundaries.

BLK-039 does not add health-check profiles, does not execute subprocesses, does not run Git, does not run BLK-pipe, does not dispatch BLK-test, does not publish BEOs, does not generate RTMs, does not inspect protected BLK-req bodies, and does not mutate source. It only normalizes already-returned local health-check result dictionaries into bounded escalation evidence for human operators.

Active boundary vocabulary:

- `HEALTH_CHECK_ESCALATION_PACKAGE_ADVISORY_ONLY`
- `HEALTH_CHECK_PASS_GRANTS_NO_AUTHORITY`
- `ADVISORY_PASS`
- `FAILED_VERIFICATION_OR_BROKEN_CODE`
- `POLICY_OR_ENVIRONMENT_BLOCKED`
- `UNKNOWN_OR_MALFORMED_HEALTH_CHECK_EVIDENCE`
- `raw_evidence_embedded: false`
- `NO_NEW_PROFILE_IDS`
- `NO_SUBPROCESS_START_FROM_PACKAGE_HELPER`
- `NO_ARBITRARY_SHELL`
- `NO_NETWORK_MODEL_CYBER_TOOLING`
- `NO_PACKAGE_MANAGER`
- `NO_GIT_MUTATION`
- `NO_SOURCE_MUTATION`
- `NO_PROTECTED_BODY_READ`
- `NO_PROTECTED_BODY_COPY`
- `NO_ACTIVE_VAULT_SCAN`
- `NO_BEO_PUBLICATION`
- `NO_RTM_GENERATION`
- `NO_DRIFT_REJECTION`
- `NO_PRODUCTION_SANDBOX_CGROUP_VM_CLAIM`
- `NO_NETWORK_FIREWALL_CLAIM`
- `NO_HOST_SECRET_ISOLATION_CLAIM`
- `NOT_PRODUCTION_HEALTH_CHECK_AUTHORITY`

Persistent doctrine gate marker: BLK-SYSTEM-037 pins health-check escalation package advisory-only evidence packaging.

---

## 2. Authorized Input Surface

The package helper may accept only dictionaries already returned by the existing advisory health-check runner for these fixed profile IDs:

```text
git_status_short_branch
active_doctrine_gate
python_unittest_discovery
go_test_all
go_vet_all
```

The helper does not own subprocess startup and must not accept caller-supplied commands, argv strings, inline snippets, shell text, wrappers, aliases, network tools, package-manager tools, tactical model tools, or cyber tools.

Allowed health-check statuses are:

```text
PASS_ADVISORY_ONLY
FAIL_ADVISORY_ONLY
BLOCKED_ADVISORY_ONLY
```

The package helper must reject unknown profile IDs, unknown statuses, missing/malformed `evidence_hash` values, raw-output fields, package-level raw log embedding, unsupported top-level fields, and any authority-laundering side-effect claim.

---

## 3. Escalation Package Contract

A valid `HEALTH_CHECK_ESCALATION_PACKAGE_ADVISORY_ONLY` record must preserve:

1. `package_id`;
2. `package_status`;
3. `authority: "HEALTH_CHECK_PASS_GRANTS_NO_AUTHORITY"`;
4. profile IDs;
5. advisory statuses;
6. exit codes;
7. evidence hashes;
8. bounded stdout/stderr excerpts only;
9. failure categories;
10. human-decision requirement;
11. non-authorizing next operator actions;
12. workspace labels and side-effect observation scope where supplied;
13. `raw_evidence_embedded: false`;
14. `health_check_pass_grants_authority: false`;
15. `production_authority_granted: false`.

Failure categories must be deterministic:

| Health-check status | Package category | Meaning |
| --- | --- | --- |
| `PASS_ADVISORY_ONLY` | `ADVISORY_PASS` | Useful context only; no authority granted. |
| `FAIL_ADVISORY_ONLY` | `FAILED_VERIFICATION_OR_BROKEN_CODE` | A fixed profile ran and returned non-zero/failing evidence; human/developer inspection required. |
| `BLOCKED_ADVISORY_ONLY` | `POLICY_OR_ENVIRONMENT_BLOCKED` | A fixed profile was blocked by policy, startup, timeout, output, cleanup, source-change, or environment evidence; human inspection required. |
| malformed evidence | `UNKNOWN_OR_MALFORMED_HEALTH_CHECK_EVIDENCE` | Reject rather than guess. |

If every result is `PASS_ADVISORY_ONLY`, `human_decision_required` may be false and the next action must still state that PASS is advisory and grants no execution, publication, RTM, drift, protected-vault, Git mutation, or production authority. If any result is `FAIL_ADVISORY_ONLY` or `BLOCKED_ADVISORY_ONLY`, `human_decision_required` must be true and the next action must require human inspection without approving retry or authority expansion.

---

## 4. Token-Flood and Raw Evidence Rules

The package may include bounded excerpts only. Raw stdout, raw stderr, unbounded logs, serialized full reports, environment dumps, protected artifact bodies, markdown/text/content fields, and secret-bearing values must not be embedded.

The package must enforce per-result excerpt limits and a package-level total excerpt limit. Oversized caller-supplied excerpts must fail closed rather than silently become an unbounded Discord/Hermes context flood.

Raw evidence remains identified by `evidence_hash` and any existing bounded fields from the runner. BLK-039 does not fetch logs, read files, contact APIs, or inspect paths to retrieve raw evidence.

---

## 5. Explicit Non-Authorities

BLK-039 does not authorize arbitrary shell, caller-supplied commands, caller-supplied argv, new health-check profile IDs, network/API/model/cyber tooling, package-manager execution, browser automation, remote service access, dependency installation, or production health-check service/daemon behavior.

BLK-039 does not authorize Git mutation or source mutation. The package helper must not stage, commit, push, reset, checkout, stash, clean, revert, merge, rebase, switch, restore, edit source files, delete source files, synthesize Git history, clone, create worktrees, initialize repositories, or repair source state.

BLK-039 does not authorize protected BLK-req vault body reads, copying, parsing, hashing, summarizing, active-vault path scans, runtime active-vault comparison, backend promotion, or requirement/use-case body inspection by the helper.

BLK-039 does not authorize production BLK-test MCP, new BLK-test smoke, BLK-pipe dispatch, live tactical LLM execution, Codex execution, authoritative BEO publication, runtime `PUBLISHED` BEO output, publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, runtime RTM generation, RTM drift rejection, or final drift decisions.

BLK-039 does not claim production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux enforcement, network firewall enforcement, host-secret isolation, kernel containment, or comprehensive host side-effect observation. It may preserve explicit non-claims from the health-check runner but must not transform those non-claims into enforcement claims.

---

## 6. Rejection Surface

The package helper must reject evidence that includes or attempts to launder:

- raw command lines, shell snippets, caller-supplied argv, wrappers, aliases, or inline code;
- `raw_stdout`, `raw_stderr`, `raw_output`, log blobs, file contents, markdown, text, or artifact bodies;
- protected path/body references, active-vault path references, requirement/use-case body fields, or `.env`/secret/private-key/token fields;
- runtime RTM, RTM authority, RTM IDs, coverage matrices, drift rejection, publication, signer, storage, ledger, rollback, revocation, or supersession fields;
- production sandbox, VM, cgroup, namespace, seccomp, AppArmor, SELinux, firewall, network-denial, or host-secret isolation enforcement claims;
- `health_check_pass_grants_authority: true` or `production_authority_granted: true`;
- side-effect claims for Git/source mutation, protected-body reads, BEO publication, RTM generation, drift decisions, network calls, package-manager calls, or approval capture.

Forbidden fields must fail closed even when nested under metadata. Dropping unknown dangerous fields silently is not allowed.

---

## 7. Stop Conditions

Stop and treat any proposed change as outside BLK-039 authority if it attempts to add or modify runner profiles, start subprocesses from the package helper, accept arbitrary command text, call Git, call BLK-pipe, call BLK-test, fetch logs, read files, contact services, mutate source, inspect protected vault bodies, compare active-vault hashes, publish BEOs, generate RTMs, make drift decisions, grant production authority, or claim production sandbox/firewall/host-secret isolation.

---

## 8. Future Handoff

Future work may improve operator display formatting, raw-evidence storage references, or decision dashboards only through a fresh plan that preserves this advisory boundary. Production health-check authority, deeper OS sandboxing, monitoring, rollback, drift authority, BEO publication, RTM generation, or BLK-test runtime authority require separate explicit doctrine, approval provenance, tests, and hostile review.
