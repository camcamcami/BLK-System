# BLK-SYSTEM-011.1 — Disabled Transport Hardening Source Review

**Status:** Planning input for BLK-SYSTEM-011.1
**Date:** 2026-05-06
**Source:** Hermes hostile review of BLK-SYSTEM-011 and BLK-SYSTEM-012 outcomes against BLK-001 intent/context.

---

## 1. Review verdict being preserved

The hostile review found that `BLK-SYSTEM-011` conditionally aligned with BLK-001 as a disabled, non-executing transport-skeleton sprint. It found no material evidence that Sprint 011 authorized live BLK-test MCP, live MCP client/server startup, fixed-tool execution, BLK-test source mutation/staging/commit, authoritative BEO publication, RTM generation/drift authority, protected BLK-req body reads, or production sandbox/host-secret isolation.

The review also found that `BLK-SYSTEM-012` aligned with BLK-001 as an inert local workspace/process-control probe sprint. BLK-SYSTEM-011.1 must not reopen Sprint 012 scope except by preserving the documented handoff: Sprint 012 owns workspace/process controls, Sprint 013 owns approval/source-evidence authorization, and Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke.

---

## 2. Findings that justify BLK-SYSTEM-011.1

### Finding A — tainted descriptor metadata can weaken the stdio-only proof

`build_disabled_transport_descriptor(...)` rejects non-stdio transport input. However, `build_non_executing_handshake_probe(...)` and `build_disabled_lifecycle_probe(...)` read `descriptor["transport"]` from caller-supplied dictionaries and currently echo that value into metadata evidence. An adversarial direct descriptor such as `{"transport": "tcp"}` can therefore produce non-stdio metadata while remaining non-executing.

Impact: metadata-only drift. This does not start live transport, but it weakens BLK-017's `stdio-only` evidence claim.

Required hardening: all public disabled-transport helper APIs must reject tainted non-stdio descriptor metadata instead of normalizing or echoing it.

### Finding B — no-git authority evidence is implicit in some runtime shapes

Sprint 011 doctrine and outcomes deny source mutation, staging, and commit authority. Some runtime descriptors expose `source_mutation_allowed: False`, but the evidence shape does not consistently expose explicit `source_write_allowed: False`, `staging_allowed: False`, `commit_allowed: False`, and `push_allowed: False` fields.

Impact: evidence-shape gap, not behavior drift. No executor exists.

Required hardening: every public disabled-transport descriptor/probe/evaluator shape should explicitly carry no-source-write/no-staging/no-commit/no-push fields.

### Finding C — live-surface source scan is too lexical

The current `test_disabled_transport_module_does_not_import_live_execution_surfaces` gate is a literal substring blacklist. The implementation intentionally constructs the public evidence key `subprocess_called` as `"sub" + "process_called"` to avoid a broad source-scan collision. This preserves behavior but makes the proof brittle.

Impact: low test-strength issue. The current module still contains no live execution imports/calls.

Required hardening: replace or supplement the broad literal scan with an AST-aware source-scan gate that forbids live imports/calls while allowing required public evidence keys such as `subprocess_called`.

### Finding D — Sprint 011 closeout trace should be self-contained after hardening

Sprint 011 closeout had an audit-trace oddity around the original plan file lifecycle. BLK-SYSTEM-011.1 should close with a self-contained closeout that lists its plan, source review artifact, implementation commits, outcome docs, verification evidence, and final remote status.

Impact: audit hygiene, not BLK-001 authority drift.

Required hardening: closeout must record the final post-push commit and clean/aligned repository state after the sprint closeout push.

---

## 3. BLK-001 boundaries that must remain unchanged

BLK-SYSTEM-011.1 is a surgical hardening sub-sprint. It does not authorize live BLK-test MCP. It does not authorize live MCP client/server startup. It does not execute fixed-tool tests. It does not mutate source, stage files, commit, or push as BLK-test behavior. It does not authorize authoritative BEO publication. It does not authorize RTM generation. It does not authorize RTM drift rejection authority. It does not read protected BLK-req vault bodies. It does not implement approval-channel mechanics. It does not claim production sandbox/cgroup/VM enforcement or production host-secret isolation.

The only authorized implementation behavior is dependency-free Python metadata/probe hardening, Python `unittest` gates, active doctrine marker updates, and outcome/closeout documentation. It may preserve identity/provenance metadata vocabulary but must not implement `blk-id` providers, `blk-relay` transport behavior, or `blk-link` ledger behavior.
