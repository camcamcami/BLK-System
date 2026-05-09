# BLK-SYSTEM-047 Hostile Review — BLK-test L4 Real-Repo Approval Boundary

**Status:** PASS after remediation
**Date:** 2026-05-09T21:30:17+10:00
**Sprint:** BLK-SYSTEM-047 — BLK-test Fixed-Tool Pilot L4 Real-Repo Approval Boundary

---

## 1. Review Scope

Reviewed the BLK-SYSTEM-047 approval-boundary doctrine and implementation:

```text
docs/BLK-050_blk-test-fixed-tool-pilot-l4-real-repo-approval-boundary.md
python/blk_test_fixed_tool_pilot_l4_real_repo_approval_boundary.py
python/test_blk_test_fixed_tool_pilot_l4_real_repo_approval_boundary.py
python/test_active_doctrine_review_gates.py
```

The hostile review focused on authority laundering and L4 real-repo scope escalation:

- exact approval-kind enforcement;
- strict request, approval, extension, source-evidence, and timeout schemas;
- recursive natural-language authority laundering;
- replay and expiry semantics;
- path traversal, protected subtree, host-secret, `.git`, symlink, and workspace marker boundaries;
- runtime entrypoint denial;
- PASS/readiness-as-publication/RTM/coverage/drift laundering.

---

## 2. Initial Verdict

Initial verdict: BLOCKED.

The first hostile review found six blockers:

1. authority-laundering scan was too narrow;
2. `source_evidence` was an unbounded nested schema escape hatch;
3. replay protection checked replay sets but did not consume IDs on ready preflight;
4. proof/hash placeholders and malformed proof identities were accepted;
5. path boundary missed nested `.git`, workspace host-secret paths, workspace primary-repo overlap, and marker-only workspace ownership;
6. expiry validation used lexicographic string comparison rather than parsed timestamps.

A second hostile review after remediation found four remaining blocker classes:

1. missing/empty exact envelope fields were still accepted;
2. protected/host-secret descendants under the approved source scope were under-blocked;
3. traversal aliases could still be accepted after path resolution;
4. workspace marker symlinks could be read before symlink escape rejection.

A third narrow hostile check after final remediation returned PASS.

---

## 3. Remediations

### 3.1 Recursive laundering and strict schemas

Remediation:

- added recursive value scanning across authorization request and approval record;
- added strict `source_evidence` schema validation;
- rejected unknown nested source-evidence keys;
- required canonical `sha256:<64 lowercase hex>` values for report, trace, commit, pre-engine, implementation, and driver proof fields;
- rejected placeholder repeated-character hashes.

Regression coverage:

```text
test_laundering_in_allowed_nested_strings_and_source_evidence_fail_closed
test_malformed_placeholder_hashes_and_timestamps_fail_closed
```

### 3.2 Replay consumption

Remediation:

- successful preflight-ready now consumes approval ID and run ID;
- blocked/error paths remain non-consuming;
- second use of the same approval/run IDs fails closed.

Regression coverage:

```text
test_complete_exact_target_envelope_is_ready_but_not_executed
test_replay_sets_expiry_and_exact_approval_kind_are_required
```

### 3.3 Path and workspace boundaries

Remediation:

- rejected primary BLK-System repo targets and workspace overlap;
- rejected protected source paths and protected descendants;
- rejected host-secret source paths, workspace paths, and descendants;
- rejected nested `.git` descendants under source scope;
- rejected traversal aliases before path resolution;
- rejected source and workspace symlink escapes;
- replaced nonce-only marker acceptance with a structured JSON workspace marker binding nonce, clone ID, repo path, source subtree, branch, and worktree ID;
- rejected marker symlinks before reading marker content.

Regression coverage:

```text
test_rejects_primary_repo_protected_subtree_and_workspace_escape
test_nested_git_workspace_host_secret_and_primary_overlap_fail_closed
test_protected_secret_descendants_traversal_alias_and_marker_symlink_fail_closed
test_empty_runtime_slice_empty_proof_lists_and_source_symlink_secret_fail_closed
```

### 3.4 Exact approval envelope requirements

Remediation:

- required `approval_id`, `operator_identity`, and `source_system` to be non-empty;
- required all extension fields to be present;
- required exact `approved_runtime_slice`;
- rejected empty proof/obligation/criteria placeholders;
- required `timeout_class` and `compression` in addition to numeric timeout/output bounds;
- parsed timezone-aware ISO/RFC3339 timestamps and required `issued_at < now < expires_at`.

Regression coverage:

```text
test_missing_required_approval_fields_and_timeout_descriptors_fail_closed
test_malformed_placeholder_hashes_and_timestamps_fail_closed
```

---

## 4. Final Hostile Review Verdict

Final verdict: PASS after remediation.

Final narrow hostile check verified:

- blank `approved_runtime_slice` fails closed;
- empty proof lists fail closed;
- source-scope symlink escapes to host-secret paths fail closed;
- source-scope symlink escapes to protected paths fail closed;
- runtime remains preflight-only;
- fixed tool, subprocess, network, source/Git mutation, publication, RTM, drift, package-manager, browser, cyber, and production-isolation authorities remain denied.

---

## 5. Final Authority Boundary

BLK-SYSTEM-047 remains approval-boundary/preflight-only. It does not authorize or perform L4 real-repo BLK-test runtime execution.

It does not authorize production BLK-test MCP, generic BLK-test MCP, arbitrary shell, caller-supplied commands, source/Git mutation by BLK-test, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime RTM generation, RTM drift rejection, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, package-manager/network/model/browser/cyber tooling, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.
