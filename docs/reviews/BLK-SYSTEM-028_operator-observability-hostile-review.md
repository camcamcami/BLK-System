# BLK-SYSTEM-028 — Operator Observability Hostile Review

**Status:** PASS after remediation
**Date:** 2026-05-08T11:09:14+10:00
**Plan:** `docs/plans/blk-system-028_operator-ux-observability-runbooks.md`
**Implementation commit under review:** `d285a1b feat: add operator observability fixtures`
**Boundary:** `docs/BLK-031_operator-ux-observability-runbook-boundary.md`

---

## 1. Review Scope

This hostile review evaluated BLK-SYSTEM-028 against the Track I L1/L0 boundary:

- deterministic local observability fixtures only;
- no live health checks;
- no command execution;
- no file inspection or raw log fetching;
- no network/API calls;
- no source mutation;
- no approval capture;
- no BEO publication;
- no RTM generation;
- no drift decision;
- no active-vault scanning;
- no protected BLK-req body reads.

The review focused on authority laundering, status/action confusion, raw-log token flooding, protected-body leakage, path/body/secret recursion, runtime RTM/publication/drift field acceptance, misleading retry approval, dirty workspace ambiguity, and doctrine-gate depth.

---

## 2. Initial Verdict

Initial verdict: **BLOCKED**.

A hostile subagent review found six blockers. The blockers were accepted as valid and remediated in Task 003 before closeout.

---

## 3. Blocking Findings and Remediation

### BLK-SYSTEM-028-HR-001 — Nested authority/protected/secret fields were only rejected by exact key match

**Severity:** BLOCKER

**Problem:** The implementation rejected exact forbidden keys such as `rtm`, `publication`, `body`, or `path`, but accepted derivative nested keys under trace metadata, including `rtm_status`, `runtime_rtm_status`, `beo_publication`, `publication_status`, `protected_body_text`, `path_hint`, `secret_value`, `token_value`, and `private_key_ref`.

**Risk:** Authority-laundering fields and protected/secret-bearing fields could be accepted silently and then dropped, making hostile evidence look clean.

**Remediation:**

- Added normalized token and composite forbidden-key detection.
- Kept explicit top-level exceptions only for approved report/status public fields.
- Added RED/GREEN regression cases for derivative/suffix runtime RTM, publication, drift, body/text, path, active-vault, secret, token, and private-key fields.

**Final status:** PASS.

### BLK-SYSTEM-028-HR-002 — Escalation packages accepted tampered unbounded excerpts

**Severity:** BLOCKER

**Problem:** Package validation accepted status fixtures with huge tampered `bounded_evidence_excerpt` values and did not cap status count or total package excerpt size.

**Risk:** A token-flood payload could be embedded into an escalation package despite the raw-log boundary.

**Remediation:**

- Added `MAX_STATUS_COUNT`, `MAX_EXCERPT_CHARS`, `MAX_RAW_REF_CHARS`, `MAX_ID_CHARS`, `MAX_TRACE_ARTIFACTS`, and `MAX_TOTAL_PACKAGE_EXCERPT_CHARS`.
- Added strict `_STATUS_ALLOWED_KEYS` validation.
- Added package-level status-count and excerpt-size bounds.
- Added tests for huge tampered excerpts and too many statuses.

**Final status:** PASS.

### BLK-SYSTEM-028-HR-003 — Failure-class/status-action invariants were not enforced

**Severity:** BLOCKER

**Problem:** `DIRTY_WORKSPACE` could be emitted with `dirty: false`, and `UNAUTHORIZED_MUTATION` could emit `Blocked and reverted` while `reverted: false`.

**Risk:** Operator status could contradict the actual revert/dirty indicators and mislead next-step decisions.

**Remediation:**

- Added class-specific invariant validation:
  - `DIRTY_WORKSPACE` requires `dirty is True`;
  - `UNAUTHORIZED_MUTATION` requires `reverted is True`.
- Updated tests to construct valid class-specific cases and added negative contradiction tests.

**Final status:** PASS.

### BLK-SYSTEM-028-HR-004 — Retry ceiling reached still emitted retry-oriented action

**Severity:** BLOCKER

**Problem:** When `retry_count == failure_ceiling`, the fixture still emitted retry-oriented next action wording.

**Risk:** A status fixture could look like it approved another retry after the failure ceiling.

**Remediation:**

- Added `retry_approved_by_fixture: False` to every status fixture.
- Forced ceiling-reached action to: `stop and escalate; failure ceiling reached; no retry is approved by this fixture`.
- Reworded non-ceiling retry-adjacent actions to require separate human decision.
- Added ceiling and non-ceiling regression tests.

**Final status:** PASS.

### BLK-SYSTEM-028-HR-005 — Raw evidence references and identities were unbounded

**Severity:** BLOCKER

**Problem:** Raw evidence references, IDs, actor identities, and trace artifact counts were unbounded.

**Risk:** Caller-supplied identity/reference fields could become token-flood surfaces even if evidence excerpts were bounded.

**Remediation:**

- Added bounded-string validation for fixture IDs, package IDs, source report IDs, `beb_id`, raw evidence refs, trace artifact `kind`/`id`, approval IDs, and actor identities.
- Added maximum trace artifact count.
- Added oversized reference/identity/list regression tests.

**Final status:** PASS.

### BLK-SYSTEM-028-HR-006 — Doctrine gates were marker-only and missed hostile failure modes

**Severity:** BLOCKER

**Problem:** Active doctrine gates checked BLK-031 marker strings and implementation live-surface markers, but did not pin hostile-review hardening semantics.

**Risk:** Future changes could remove derivative-key rejection, package bounds, retry non-approval, class-indicator consistency, or bounded ID/reference behavior without doctrine-level signal.

**Remediation:**

- Added BLK-031 hard-gate language for derivative/suffix authority fields, package count/size bounds, retry non-approval, dirty/reverted class consistency, bounded caller references/IDs, and nested side-effect rejection.
- Extended `test_sprint028_operator_observability_boundary_preserves_no_execution_authority` to require those markers.
- Extended implementation live-surface marker scanning with file/path/glob/read markers.
- Expanded API-level tests for all HR-001 through HR-005 failure modes.

**Final status:** PASS.

---

## 4. Final Verdict

Final verdict: **PASS after remediation**.

All blockers were remediated with persistent tests and doctrine markers. The implementation remains L1 deterministic local fixture-only and L0 doctrine/runbook-only. It still does not authorize live health checks, command execution, file inspection, network/API calls, source mutation, approval capture, BEO publication, RTM generation, drift decisions, active-vault scanning, or protected-body reads.

---

## 5. Final Verification Evidence

Focused remediation verification:

```text
Ran 14 tests in 0.004s
OK
Ran 48 tests in 0.005s
OK
```

Full verification:

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
Ran 398 tests in 6.419s
OK
git diff --check completed with no output
```
