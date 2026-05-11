# Kuronode Lifecycle Cleanup Patch Approval Envelope Boundary

**Status:** Active review-only approval-envelope boundary — not patch approval; not patch execution
**Boundary marker:** `KURONODE_LIFECYCLE_CLEANUP_PATCH_APPROVAL_ENVELOPE_BOUNDARY`
**Sprint:** BLK-SYSTEM-075
**Envelope status:** `KURONODE_LIFECYCLE_CLEANUP_PATCH_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PATCHED`
**Persistent doctrine gate:** `PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_075_KURONODE_LIFECYCLE_CLEANUP_PATCH_APPROVAL_ENVELOPE`

---

## Purpose

BLK-SYSTEM-075 creates a review-only exact-target approval envelope for a future Kuronode lifecycle cleanup patch. It consumes the BLK-SYSTEM-074 remediation packet and presents a future human decision surface. It does not approve or execute any patch.

The source finding remains:

```text
smoke_test.ts:53 LIFECYCLE_CLEANUP_REQUIRED
```

---

## Exact Target Boundary

```text
target_repo_path: /home/dad/code/Kuronode-v1
target_branch: main
target_head_sha: 38e332b188e45edcb484765694112c9041ad1a3b
allowed_modified_files: scripts/smoke_test.ts
allowed_new_files: []
patch_mechanism: BLK_PIPE_EXACT_TARGET_PATCH_PROPOSED_NOT_EXECUTED
```

The envelope must re-bind the BLK-SYSTEM-074 remediation packet by recomputing the packet hash. The required proof markers are:

```text
UPSTREAM_REMEDIATION_PACKET_HASH_RECOMPUTED
EXACT_TARGET_SHA_BOUND
EXACT_PATCH_ALLOWLIST_BOUND
READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PATCHED
NO_PATCH_APPROVAL_GRANTED
NO_PATCH_EXECUTION
NO_BLK_PIPE_EXECUTION
NO_CODEX_EXECUTION
NO_KURONODE_SOURCE_OR_GIT_MUTATION
NO_BLK_TEST_RERUN_OR_RETIRED_ID_REUSE
NO_BEO_RTM_COVERAGE_DRIFT_AUTHORITY
```

---

## Future Candidate IDs

The envelope may name future candidate IDs for human review, but they are not consumed and not executable authority:

```text
APPROVAL-BLK-SYSTEM-075-KURONODE-LIFECYCLE-CLEANUP-PATCH-001
RUN-BLK-SYSTEM-075-KURONODE-LIFECYCLE-CLEANUP-PATCH-001
FUTURE_CANDIDATE_NOT_CONSUMED
```

The retired BLK-SYSTEM-073 IDs must not be reused for this or any future patch/recheck path.

---

## Required Patch Obligation Surface

A future patch sprint, if explicitly approved, must preserve these obligations:

```text
PATCH_ADD_DETERMINISTIC_LIFECYCLE_TEARDOWN
PATCH_ASSERT_NO_ESCAPED_PROCESS_OR_LISTENER
PATCH_PRESERVE_TIMEOUT_AS_FAILURE
PATCH_ADD_FOCUSED_CLEANUP_REGRESSION
PATCH_RUN_KURONODE_CLOSEOUT_REVIEW_BEFORE_COMPLETION
PATCH_REQUIRE_FRESH_BLK_TEST_RECHECK_IDS_AFTER_PATCH
```

These obligations are review criteria only in BLK-SYSTEM-075. They are not proof that a patch exists.

---

## Explicit Non-Authority Boundary

- No Kuronode patch approval granted
- No Kuronode patch execution
- No BLK-pipe execution
- No Codex execution
- No live tactical LLM dispatch
- No Kuronode source mutation
- No Kuronode Git mutation, staging, commit, push, reset, checkout, revert, stash, cleanup, autofix, or remote writes
- No BLK-test pilot rerun
- No reuse of retired BLK-SYSTEM-073 runtime IDs
- No production BLK-test MCP authority
- No generic BLK-test MCP authority
- No reusable BLK-test service startup
- No arbitrary shell or caller-supplied commands
- No dynamic tool expansion
- No Electron launch, no smoke-test execution, no TypeScript compiler, no linter, no formatter, no package-manager invocation
- No network/model/browser/cyber tooling
- No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison
- No authoritative BEO publication
- No runtime PUBLISHED BEO output
- No RTM generation or RTM drift rejection
- No coverage matrix, coverage claim, active-vault hash comparison, or drift decision
- No public ledger mutation
- No signer, storage, rollback, revocation, supersession, or release authority
- No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation proof

---

## Stop Conditions

The envelope must fail closed if:

- the upstream remediation packet hash is forged, stale, or not recomputed from the submitted body;
- the upstream packet status is not `KURONODE_LIFECYCLE_CLEANUP_REMEDIATION_PACKET_READY_NOT_PATCHED`;
- target repo/path/branch/SHA differs from the exact target boundary;
- the patch allowlist differs from `scripts/smoke_test.ts` or includes any new file;
- `approval_granted` is true;
- a request claims BLK-pipe, Codex, source/Git mutation, runtime validation, BLK-test rerun, package-manager/tooling execution, BEO publication, RTM generation, coverage/drift truth, protected-body access, or production BLK-test MCP;
- a request reuses retired BLK-SYSTEM-073 IDs;
- requested/expiry timestamps are malformed, timezone-naive, or expired.

---

## Future Authority Requirement

A later patch sprint must receive explicit human approval after this envelope is reviewed. Before any mutation, the future sprint must re-check local and observed remote Kuronode HEAD, verify exact allowlists, invoke only the approved patch mechanism, run approved validation, perform Kuronode closeout review, and preserve fresh BLK-test recheck IDs for any later runtime verification.

---

## Doctrine Persistence

This boundary is pinned by `python/test_active_doctrine_review_gates.py` so later sprints cannot silently convert the review-only envelope into patch approval, patch execution, BLK-pipe execution, Codex execution, source/Git mutation, BLK-test rerun authority, production BLK-test MCP, BEO publication, RTM generation, coverage/drift authority, protected-body reads, or host-isolation claims.
