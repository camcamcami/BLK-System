# BLK-019 — BLK-test MCP Approval/Source-Evidence Authorization

**Status:** Active approval/source-evidence authorization contract
**Scope:** BLK-SYSTEM-013 dependency-free local validation for BLK-test-specific approval records, exact source-evidence binding, expiry/replay checks, and disabled startup preflight evidence.

---

## 1. Purpose

BLK-019 makes the BLK-SYSTEM-013 approval/source-evidence authorization contract discoverable as active doctrine. It records what must be true before a future BLK-test MCP live smoke can even be considered, while preserving that Sprint 013 itself does not start live transport and does not execute fixed-tool tests.

The governing distinction is exact: codex-live approval is not BLK-test MCP approval. A `BLK_APPROVE_CODEX_LIVE` token, tactical implementation approval, or `codex-live` audit record cannot authorize BLK-test MCP startup.

---

## 2. Current authority boundary

BLK-SYSTEM-013 and BLK-019 authorize local approval/source-evidence validation evidence only. They do not authorize live BLK-test MCP and do not authorize live MCP client/server startup.

The contract also does not execute fixed-tool tests, does not mutate primary repo, does not stage files, does not commit, does not push as BLK-test behavior, does not authorize authoritative BEO publication, does not authorize RTM generation, does not authorize RTM drift rejection authority, does not read protected BLK-req vault bodies, does not parse active-vault requirement bodies, does not grant arbitrary shell or dynamic command execution, does not claim production sandbox/cgroup/VM enforcement, and does not claim production host-secret isolation.

Human sprint-executor commits and pushes for reviewed validation code and outcome documentation are project-maintenance actions; they are not BLK-test source-mutation authority.

Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke.

---

## 3. Approval record required fields

A BLK-test approval record must be BLK-test-specific and one-run/scoped. It must bind:

- source BLK-pipe report identity;
- `beb_id`;
- source commit_hash;
- `pre_engine_hash`;
- canonical trace_artifacts with `trace_artifacts[*].version_hash == sha256:<64-lowercase-hex>`;
- requested fixed BLK-test tool(s);
- test profile;
- workspace identity;
- timeout/output profile;
- operator identity/approval timestamp;
- approval ID;
- issued timestamp;
- expiry timestamp;
- replay/audit metadata.

The approval record must not contain wildcard tools, unknown tools, shell/command/exec/eval capability fields, source mutation fields, BEO publication fields, RTM generation fields, active-vault body references, or protected BLK-req vault body paths.

---

## 4. Source-evidence binding rules

The approval validator must bind the approval record exactly to the authorization request envelope. These fields must match byte-for-byte after normalization:

- source BLK-pipe report identity;
- `beb_id`;
- source commit_hash;
- `pre_engine_hash`;
- canonical trace_artifacts;
- requested fixed BLK-test tool(s);
- test profile;
- workspace identity;
- timeout/output profile.

Mismatches fail closed. BLOCKED or incomplete source evidence cannot be laundered into PASS/FAIL, authoritative BEO, RTM, BLK-req promotion, live transport, or source mutation authority.

---

## 5. Expiry/replay/audit evidence

Sprint 013 approval evidence is one-run/scoped and replay-resistant through caller-supplied used approval IDs. Approval validation must reject:

- expired approval windows;
- malformed timestamps;
- approval timestamps outside the issued/expires window;
- replayed approval IDs;
- `codex-live` or `BLK_APPROVE_CODEX_LIVE` approval reuse.

Accepted local validation may produce deterministic audit hashes:

- `approval_record_hash`;
- `source_evidence_hash`;
- `authorization_request_hash`.

These hashes are `sha256:<64-lowercase-hex>` evidence identifiers only. They do not create truth, mutation, publication, RTM, active-vault, transport, or fixed-tool execution authority.

---

## 6. Relationship to BLK-017 and BLK-018

BLK-017 remains the active disabled transport contract. It proves disabled-by-default stdio transport metadata, startup refusal, non-executing handshake/lifecycle evidence, and descriptor-only fixed tool registry metadata.

BLK-018 remains the active inert workspace/process-control probe contract. It proves deterministic local workspace/process/resource controls with synthetic fixtures only.

BLK-019 adds approval/source-evidence authorization validation evidence only. A future live BLK-test MCP path must preserve BLK-017, satisfy BLK-018, and satisfy BLK-019 before Sprint 014 may request explicit human approval for any first live fixed-tool BLK-test MCP smoke.

---

## 7. Non-authority checklist

BLK-019 preserves these explicit non-authority markers:

- does not authorize live BLK-test MCP;
- does not authorize live MCP client/server startup;
- does not execute fixed-tool tests;
- does not mutate primary repo;
- does not stage files;
- does not commit;
- does not push as BLK-test behavior;
- does not grant arbitrary shell;
- does not authorize authoritative BEO publication;
- does not authorize RTM generation;
- does not authorize RTM drift rejection authority;
- does not read protected BLK-req vault bodies;
- does not parse active-vault requirement bodies;
- does not claim production sandbox/cgroup/VM enforcement;
- does not claim production host-secret isolation.

---

## 8. Stop conditions

Stop and treat any future change as out of BLK-019 authority if it attempts to:

- start live MCP server/client transport;
- invoke fixed BLK-test tools against any repository;
- mutate, stage, commit, or push source as BLK-test behavior;
- accept `codex-live` as BLK-test MCP approval;
- broaden approval beyond one exact source/request/workspace/profile envelope;
- publish authoritative BEO output;
- generate RTM or make drift decisions;
- read active BLK-req vault body text;
- claim production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, or host-secret isolation enforcement.

---

## 9. Implementation and tests

Implementation and gate files:

- `python/blk_test_mcp_approval_authorization.py`
- `python/test_blk_test_mcp_approval_authorization.py`
- `python/blk_test_mcp_disabled_transport.py`
- `python/test_blk_test_mcp_disabled_transport.py`
- `python/test_active_doctrine_review_gates.py`

The implementation remains dependency-free Python standard library validation code. It is local evidence only and does not import or invoke live transport, process, network, package-manager, source-mutation, BEO publication, RTM generation, or active-vault body-read surfaces.
