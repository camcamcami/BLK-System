# BLK-SYSTEM-022 Task 001 Outcome — BLK-test Current-State Inventory

**Status:** Complete  
**Date:** 2026-05-07T22:00:00+10:00  
**Plan:** `docs/plans/blk-system-022_blk-test-pilot-readiness-design-review.md`

---

## 1. Objective

Produce a bounded inventory of current BLK-test doctrine, code, tests, evidence vocabulary, and hard stop conditions before writing any new BLK-test pilot-readiness boundary document.

---

## 2. Exact Paths Inspected

Doctrine and roadmap:

- `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md`
- `docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md`
- `docs/BLK-019_blk-test-mcp-approval-source-evidence-authorization.md`
- `docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md`
- `docs/BLK-024_blk-system-development-roadmap.md`

Implementation and tests:

- `python/blk_test_mcp_disabled_transport.py`
- `python/test_blk_test_mcp_disabled_transport.py`
- `python/blk_test_mcp_workspace_process_probes.py`
- `python/test_blk_test_mcp_workspace_process_probes.py`
- `python/blk_test_mcp_approval_authorization.py`
- `python/test_blk_test_mcp_approval_authorization.py`
- `python/blk_test_mcp_fixed_tool_live_smoke.py`
- `python/test_blk_test_mcp_fixed_tool_live_smoke.py`
- `python/test_active_doctrine_review_gates.py`

---

## 3. Current-State Doctrine Inventory

| Surface | Current state | Pilot-readiness implication |
| --- | --- | --- |
| Disabled generic startup | BLK-017 records the active disabled transport contract. Generic live BLK-test MCP startup remains disabled by default and stdio-only metadata/probe evidence is the safe current shape. | A later pilot must explicitly supersede or narrow this disabled boundary; no ambient live startup is available. |
| Fixed-tool registry | BLK-017 exposes descriptor-only fixed-tool metadata. BLK-020 records exactly one historical first-smoke fixed tool, `run_ast_validation`, under a source-bound synthetic envelope. | A pilot must use a fixed-tool registry and reject caller-supplied commands, wildcard tools, dynamic tool expansion, arbitrary shell, package-manager execution, and model/network/cyber calls. |
| Workspace/process probes | BLK-018 records inert local fixture probes for workspace boundary descriptors, clone decisions, path guards, cache jails, marker-protected fixture clone/teardown, timeout/output flood/descendant-kill/pipe-holder probes, and replay evidence sanitization. | Pilot readiness must require stronger proof before any real target-repo operation: `.git` ancestry/descendant escape, symlink escape, protected paths, root/home paths, host-secret paths, timeout, output flood, descendant process, and cleanup failure must fail closed. |
| Approval/source evidence | BLK-019 records BLK-test-specific one-run/scoped approval and source-evidence binding. Codex-live approval is explicitly not BLK-test MCP approval. | Any L4 pilot must require separate human pilot approval distinct from execution, BLK-test smoke, BEO publication, and RTM approval. Approval reuse, expiry, source mismatch, wildcard tools, protected body references, and authority-like fields must fail closed. |
| First live smoke exception | BLK-020 records one accepted first-smoke evidence contract from BLK-SYSTEM-014. It used a synthetic isolated workspace and one fixed tool, `run_ast_validation`, and does not authorize production BLK-test MCP. | Future live activity cannot treat BLK-020 as reusable production authority. Any additional smoke or pilot needs a fresh source/request/workspace/profile/tool envelope and separate approval. |
| Evidence vocabulary | Current evidence vocabulary includes PASS/FAIL/BLOCKED plus fatal/transport statuses for bounded process outcomes. BLOCKED/fatal/transport statuses cannot project to success. | Pilot readiness must preserve evidence-only semantics. BLK-test output must not mutate source, publish BEOs, generate RTM, promote BLK-req, or make drift decisions. |
| Production sandbox claims | BLK-018 and BLK-020 explicitly do not claim production sandbox/cgroup/VM enforcement or production host-secret isolation. | A later pilot cannot claim production isolation unless separate tests prove it. Sprint 022 should document missing production-isolation authority rather than imply it exists. |

---

## 4. Code/Test Surface Inventory

| File | Observed surface |
| --- | --- |
| `python/blk_test_mcp_disabled_transport.py` | Builds disabled transport descriptors, startup refusal evidence, non-executing handshake/lifecycle probes, descriptor-only fixed-tool registry, and blocked disabled-tool execution. |
| `python/test_blk_test_mcp_disabled_transport.py` | Verifies disabled-by-default behavior, stdio-only metadata rejection, approval-looking records not enabling live startup, descriptor-only registry, and AST-aware no-live-surface scanning. |
| `python/blk_test_mcp_workspace_process_probes.py` | Implements inert workspace/process-control helper surfaces: clone decisions, relative path guards, protected-prefix rejection, run cache paths, fixture-source guard, marker-owned clone/teardown, probe locks, process-control probes, output compression, and replay sanitization. |
| `python/test_blk_test_mcp_workspace_process_probes.py` | Verifies workspace path guards including symlink alias to protected vault, real BLK-System repo rejection, marker-protected fixtures, startup purge ownership, lock handling, timeout/flood/descendant/pipe-holder behavior, replay/output/env redaction, and non-authority fields. |
| `python/blk_test_mcp_approval_authorization.py` | Builds authorization requests and validates BLK-test approval records against exact source evidence, canonical hashes, requested tools, workspace identity, timeout/output profile, expiry, replay, and forbidden authority fields. |
| `python/test_blk_test_mcp_approval_authorization.py` | Verifies valid normalization, missing fields, Codex-live rejection, wildcard/unknown tool rejection, protected-vault body reference rejection, source mismatch rejection, authority-like field rejection, expiry/replay rejection, stable hashes, and secret omission. |
| `python/blk_test_mcp_fixed_tool_live_smoke.py` | Contains BLK-SYSTEM-014 fixed-tool smoke wrapper and dependency-free stdio harness for the one synthetic first-smoke path. It includes fixed registry descriptor, workspace validation, fixed command resolution, bounded process communication, process-group kill, and environment scrubbing. |
| `python/test_blk_test_mcp_fixed_tool_live_smoke.py` | Verifies explicit live-smoke flag/checkpoint, Codex-live rejection, exact envelope binding, stdio-only fixed tool, primary repo/home/root/git/protected/symlink workspace rejection, PASS/BLOCKED/FATAL evidence, output flood/timeout handling, source scan, and replay set requirements. |
| `python/test_active_doctrine_review_gates.py` | Existing persistent doctrine gates cover BLK-017 through BLK-020 and related BEO/RTM boundary documents, but no dedicated BLK-025 pilot-readiness boundary gate exists yet. |

---

## 5. Candidate Pilot Prerequisites Identified

These are candidate prerequisites only; they do not grant pilot authority.

1. A dedicated BLK-test pilot-readiness boundary document must exist and be explicit that it is design-only unless a later sprint requests L4 pilot authority.
2. Generic disabled transport must remain active until a later plan explicitly narrows the startup envelope.
3. Pilot approval must be human, BLK-test-specific, one-run/scoped, source-bound, and separate from Codex/live execution approval, BEO publication approval, and RTM approval.
4. Fixed-tool registry must stay static and reject caller-supplied command strings, unknown/wildcard tools, dynamic tool expansion, arbitrary shell, package managers, model/network calls, and cyber tooling.
5. Source evidence must bind BLK-pipe report identity, `beb_id`, commit hash, `pre_engine_hash`, `post_engine_hash`, requested tool, workspace identity, timeout/output profile, and canonical `trace_artifacts`.
6. Workspace readiness must prove failure for real target-repo escape, `.git` ancestry/descendant escape, symlink escape, protected paths, root/home paths, and host-secret-bearing paths.
7. Process readiness must prove timeout, output-flood, descendant kill, pipe-holder no-hang, cleanup failure, and replay evidence handling.
8. Evidence statuses must remain evidence-only and must not project to BEO publication, RTM generation, source mutation, BLK-req promotion, or drift rejection.
9. Production sandbox/cgroup/VM/network/host-secret isolation must not be claimed without separate proof and authority.

---

## 6. Verification

Command run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  python.test_blk_test_mcp_disabled_transport \
  python.test_blk_test_mcp_workspace_process_probes \
  python.test_blk_test_mcp_approval_authorization \
  python.test_blk_test_mcp_fixed_tool_live_smoke \
  python.test_active_doctrine_review_gates -v
```

Observed result:

```text
Ran 173 tests in 5.654s

OK
```

Task doc verification before commit:

```bash
git diff --check -- docs/outcomes/BLK-SYSTEM-022_task-001-outcome.md
```

---

## 7. Files Changed

Created:

- `docs/outcomes/BLK-SYSTEM-022_task-001-outcome.md`

No implementation or doctrine files were changed in Task 001.

---

## 8. Non-Execution and No-Authority-Expansion Statement

Task 001 did not authorize Hindsight use, Codex use, live tactical LLM execution, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, replay of the BLK-SYSTEM-014/BLK-020 smoke, arbitrary shell as BLK-test behavior, source mutation by BLK-test, protected BLK-req vault body reads/copying/parsing/hashing/mutation, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, production sandbox/cgroup/VM/network/host-secret isolation claims, or source mutation outside exact approved allowlists.
