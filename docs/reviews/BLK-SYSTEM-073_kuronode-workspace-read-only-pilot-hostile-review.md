# BLK-SYSTEM-073 Hostile Review — Kuronode Workspace Read-Only Pilot Runtime

**Status:** Complete — blockers found and remediated with regression tests
**Date:** 2026-05-11
**Scope:** `python/blk_test_kuronode_workspace_read_only_pilot_runtime.py`, focused runtime tests, BLK-074 boundary, runtime evidence, and BLK-SYSTEM-073 outcome chain.

---

## Review Summary

A hostile review of BLK-SYSTEM-073 found that the initial implementation correctly executed a read-only evidence pilot and did not mutate Kuronode, but the wrapper still exposed several authority-laundering and replay-safety gaps after the one real run consumed its production IDs.

The review treated these as blockers because BLK-SYSTEM-073 is a one-run, exact-target, read-only runtime pilot. Evidence is not authority; a FAIL/PASS/BLOCKED result must not create production BLK-test MCP, source/Git mutation, BEO, RTM, coverage, drift, or rerun authority.

---

## Original Runtime Evidence

The real pilot result remains authoritative evidence and was not rerun:

```text
status: FAIL
pilot_status: BLK_TEST_KURONODE_WORKSPACE_READ_ONLY_PILOT_FAIL_EVIDENCE_ONLY
finding: smoke_test.ts:53 LIFECYCLE_CLEANUP_REQUIRED
source_mutation_detected: false
git_mutation_detected: false
workspace_cleanup_verified: true
```

The production IDs are consumed and retired:

```text
APPROVAL-BLK-SYSTEM-073-KURONODE-WORKSPACE-001
RUN-BLK-SYSTEM-073-KURONODE-WORKSPACE-001
```

---

## Blockers and Remediation

### 1. Public custom-envelope target laundering

**Finding:** The public runtime entrypoint accepted a caller-supplied `PilotRuntimeEnvelope`, so a caller could run synthetic or arbitrary targets while presenting the operation as BLK-SYSTEM-073.

**Remediation:** Split the runtime into:

- production `run_blk_test_kuronode_workspace_read_only_pilot(...)`, which always uses `default_runtime_envelope()`;
- private `_run_blk_test_kuronode_workspace_read_only_pilot_for_tests(...)`, which accepts synthetic envelopes for regression tests only.

The envelope now requires `sprint == "BLK-SYSTEM-073"` rather than substring binding.

### 2. Replay bypass after `/tmp` ledger deletion

**Finding:** The real run wrote its durable ledger under `/tmp`; after process restart and ledger deletion, process-local replay state would be gone.

**Remediation:** The production entrypoint now checks the committed runtime evidence artifact and rejects the production IDs as already retired when `docs/outcomes/BLK-SYSTEM-073_runtime-evidence.json` records those IDs. This preserves the historical one-run boundary without rerunning the real pilot.

### 3. Remote-head truth laundering

**Finding:** The wrapper trusted caller-provided `observed_remote_head` and evidence hardcoded expected remote head.

**Remediation:** Runtime now resolves the actual local remote-tracking ref `refs/remotes/origin/main` (including `packed-refs`) and compares it to both caller-provided evidence and the expected SHA. Evidence records the actual observed remote-tracking value, not the expected value.

### 4. PASS-as-approval and publication wording

**Finding:** Free-text scanning missed variants such as `PASS is approval to publish BEO`.

**Remediation:** Expanded forbidden text detection for PASS-as-approval, BEO publication, publish-BEO, approval-to-publish/release, release/deployment approval, RTM, coverage, and drift wording. The upstream `workspace_status` is now exact-string validated as `main...origin/main`.

### 5. Post-replay exception paths

**Finding:** Some exceptions after replay consumption could skip bounded BLOCKED evidence and after-snapshots.

**Remediation:** Post-replay runtime execution is now wrapped so exceptions after replay become bounded BLOCKED evidence with exception class only, workspace cleanup, and source/Git after-snapshot reporting when measurable.

### 6. Findings and output-bound truthfulness

**Finding:** `findings_count` represented emitted findings rather than total findings, and compact evidence was not checked after compaction.

**Remediation:** Added total `findings_count`, emitted `findings_emitted_count`, correct truncation semantics, and final compact-evidence size enforcement.

### 7. Secret-like descendant coverage

**Finding:** Additional secret-bearing filenames were not blocked.

**Remediation:** Expanded secret-like descendant rejection to include `.envrc`, `.npmrc`, `.pypirc`, `.netrc`, `service-account.json`, `kubeconfig`, and `key.json` in addition to existing secret/token/private-key patterns.

---

## Regression Coverage Added

Focused tests now cover:

- public production entrypoint retirement after committed evidence;
- private test-only runner for synthetic fixtures;
- actual remote-tracking head mismatch blocking after replay and before tool execution;
- exact upstream `workspace_status` validation;
- PASS-as-approval / publication wording rejection through forbidden text scans;
- post-replay BLOCKED evidence semantics;
- findings-count and bounded-output hardening;
- expanded secret-like descendant rejection.

---

## Remaining Non-Blocking Notes

- BLK-SYSTEM-073 did not claim production sandbox or host-secret isolation; the runtime still uses deterministic local file snapshots rather than sandbox proof.
- `.git` mutation observation hashes `.git` metadata bytes for change detection. It does not emit raw `.git` contents or secrets.
- The original pilot FAIL finding remains open as Kuronode/BLK-test evidence only. It is not remediated in BLK-SYSTEM-073 because this sprint has no Kuronode source-mutation authority.

---

## Verification

Focused verification after remediation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_kuronode_workspace_read_only_pilot_runtime -q
----------------------------------------------------------------------
Ran 8 tests in 0.011s

OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint073_blk_test_kuronode_workspace_read_only_pilot_runtime_is_evidence_only -q
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```

Full verification is recorded in the sprint closeout.

---

## Boundary Statement

No remediation reran the real Kuronode pilot. No remediation started production/generic BLK-test MCP, ran Electron/smoke/TypeScript/package-manager tooling, invoked Codex, invoked BLK-pipe, mutated Kuronode source or Git state, pushed Kuronode, read protected BLK-req bodies, published BEOs, generated RTM, or promoted coverage/drift authority.
