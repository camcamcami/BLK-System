# BLK-test Kuronode Lifecycle Cleanup Remediation Boundary

**Status:** Active fixture-only remediation boundary — review-ready packet only; no Kuronode patch authority
**Boundary marker:** `BLK_TEST_KURONODE_LIFECYCLE_CLEANUP_REMEDIATION_BOUNDARY`
**Sprint:** BLK-SYSTEM-074
**Packet status:** `KURONODE_LIFECYCLE_CLEANUP_REMEDIATION_PACKET_READY_NOT_PATCHED`
**Persistent doctrine gate:** `PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_074_KURONODE_LIFECYCLE_CLEANUP_REMEDIATION`

---

## Purpose

BLK-SYSTEM-074 converts the BLK-SYSTEM-073 read-only BLK-test functional-module finding into a deterministic review-ready remediation packet.

BLK-test is a BLK-System functional module, not BLK-System's test suite.

The exact finding is:

```text
smoke_test.ts:53 LIFECYCLE_CLEANUP_REQUIRED
```

This document does not authorize a Kuronode patch. It records the boundary for turning evidence into a future patch-decision package.

---

## Source Evidence Boundary

The only source evidence consumed by this boundary is the committed BLK-SYSTEM-073 runtime evidence artifact:

```text
docs/outcomes/BLK-SYSTEM-073_runtime-evidence.json
```

Required evidence identity:

```text
source_sprint: BLK-SYSTEM-073
source_status: FAIL
source_pilot_status: BLK_TEST_KURONODE_WORKSPACE_READ_ONLY_PILOT_FAIL_EVIDENCE_ONLY
finding: smoke_test.ts:53 LIFECYCLE_CLEANUP_REQUIRED
target_repo_path: /home/dad/code/Kuronode-v1
target_head_sha: 38e332b188e45edcb484765694112c9041ad1a3b
approval_id: APPROVAL-BLK-SYSTEM-073-KURONODE-WORKSPACE-001
run_id: RUN-BLK-SYSTEM-073-KURONODE-WORKSPACE-001
```

Required proof markers:

```text
RETIRED_IDS_MUST_NOT_BE_REUSED
SOURCE_EVIDENCE_HASH_RECOMPUTED
EXACT_LIFECYCLE_FINDING_BOUND
FRESH_RUNTIME_IDS_REQUIRED_BY_SEPARATE_AUTHORITY_NOT_ALLOCATED
NO_PILOT_RERUN
NO_PATCH_APPROVAL_GRANTED
NO_KURONODE_SOURCE_OR_GIT_MUTATION
NO_PROTECTED_BODY_READ
NO_BEO_RTM_COVERAGE_DRIFT_AUTHORITY
```

The BLK-SYSTEM-073 approval/run IDs are historical evidence identifiers and retired replay identifiers. They are not future-runtime candidates.

---

## Allowed Fixture Behavior

BLK-SYSTEM-074 may only:

1. load the committed BLK-SYSTEM-073 evidence JSON;
2. recompute a deterministic source-evidence hash;
3. require exact FAIL evidence for `smoke_test.ts:53 LIFECYCLE_CLEANUP_REQUIRED`;
4. verify the historical source evidence recorded no source mutation, no Git mutation, no protected body reads, no BEO publication, no RTM generation, no coverage/drift promotion, no package-manager or TypeScript tooling, and no production/generic BLK-test MCP authority;
5. reject any request attempting to reuse `APPROVAL-BLK-SYSTEM-073-KURONODE-WORKSPACE-001` or `RUN-BLK-SYSTEM-073-KURONODE-WORKSPACE-001` as future runtime identity;
6. reject nested authority-laundering text, protected BLK-req path strings, exact denied-authority mismatches, and forged source-evidence hashes;
7. emit a review-ready remediation packet containing future patch obligations;
8. preserve all no-side-effect flags as explicit false values.

---

## Remediation Obligation Surface

The remediation packet may describe future patch obligations only:

```text
LIFECYCLE_CLEANUP_ADD_DETERMINISTIC_TEARDOWN
LIFECYCLE_CLEANUP_ASSERT_NO_ESCAPED_PROCESS_OR_LISTENER
LIFECYCLE_CLEANUP_PRESERVE_TIMEOUT_AS_FAILURE
LIFECYCLE_CLEANUP_ADD_FOCUSED_REGRESSION
LIFECYCLE_CLEANUP_REQUIRE_FRESH_RUNTIME_IDS_FOR_RECHECK
LIFECYCLE_CLEANUP_NOT_PATCH_AUTHORITY
```

These obligations mean a future, separately approved Kuronode patch should add deterministic cleanup around the lifecycle boundary, preserve timeout-as-failure behavior, and add focused regression coverage. They do not mean a patch has been accepted or applied.

---

## Explicit Non-Authority Boundary

- No production BLK-test MCP authority
- No generic BLK-test MCP authority
- No reusable BLK-test service startup
- No arbitrary shell or caller-supplied commands
- No dynamic tool expansion
- No Electron launch, no smoke-test execution, no TypeScript compiler, no linter, no formatter, no package-manager invocation
- No network/model/browser/cyber tooling
- No live Codex execution authority
- No live tactical LLM dispatch
- No BLK-pipe execution
- No Kuronode source mutation
- No Kuronode Git mutation, staging, commit, push, reset, checkout, revert, stash, cleanup, autofix, or remote writes
- No Kuronode patch approval capture
- No pilot rerun under BLK-SYSTEM-073 IDs
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

The remediation packet must fail closed if:

- the source evidence is not BLK-SYSTEM-073 FAIL evidence;
- the exact lifecycle finding is absent or altered;
- target repo identity or target head identity differs from the committed evidence boundary;
- any source evidence side-effect flag claims source mutation, Git mutation, protected-body reads, BEO publication, RTM generation, coverage/drift promotion, package-manager/tooling execution, or production/generic BLK-test MCP authority;
- a request proposes the retired BLK-SYSTEM-073 approval/run IDs as future runtime IDs;
- a request includes protected BLK-req paths, nested authority-laundering text, runtime approval wording, publication/RTM/coverage/drift wording, secret-like key material, or exact denied-authority mismatches;
- a source-evidence hash is forged or stale.

---

## Future Authority Requirement

A future Kuronode lifecycle cleanup patch requires a separate sprint and explicit authority envelope naming:

1. exact Kuronode repository path, branch, local HEAD, and observed remote HEAD;
2. exact modified-file allowlist;
3. exact patch mechanism, preferably BLK-pipe-mediated if mutation authority is granted;
4. validation commands or profiles;
5. fresh runtime IDs for any later BLK-test recheck;
6. Kuronode repository closeout review obligations.

This BLK-SYSTEM-074 boundary is only the evidence-to-remediation-packet bridge.

---

## Doctrine Persistence

This boundary is pinned by `python/test_active_doctrine_review_gates.py` so later sprints cannot silently convert a BLK-test finding into patch authority, pilot rerun authority, production BLK-test MCP, protected-body read authority, BEO publication, RTM generation, coverage/drift truth, source/Git mutation authority, or host-isolation claims.
