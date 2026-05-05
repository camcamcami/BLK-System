# BLK-012 — BLK-pipe Integration Readiness and Capability Profiles

**Status:** Active Sprint 006 operator guidance
**Scope:** BLK-pipe integration readiness boundaries, capability profiles, fail-closed approval contracts, and blocked live-execution scope
**Date:** 2026-05-04

---

## 1. Boundary Statement

BLK-pipe is a deterministic repository mutation gate and bounded local command transport. Sprint 004 closes the deterministic dry-run loop around BEB/L2 payload fixtures, fake tactical-engine command shape, BLK-test fixture handoff, and draft BEO projection so future orchestration can be tested against explicit safety boundaries.

Sprint 004 does not run Codex. Sprint 004 does not authorize live LLM execution. Sprint 004 does not authorize cyber execution. It does not call OpenAI, local LLMs, network model services, offensive cyber tooling, real cyber-program repositories, live tactical engines, or live BLK-test MCP. BLK-test is fixture-only, BEO is fixture/draft-only, and RTM is not generated.

BLK-pipe is not a full sandbox. BLK-pipe is not general host-secret isolation. It does not replace container, VM, cgroup, namespace, seccomp/AppArmor/SELinux, network, filesystem, secret-management, or malware-analysis controls.

`codex-live` and `cyber-execution` remain blocked until explicitly approved in a future sprint. Sprint 005 added `python/blk_orchestrator_gate.py` and BLK-015 as a fail-closed approval contract surface. Sprint 006 clarifies the executable semantics: `ProfileDecision.allowed` means executable now; local profiles may be classified as `ALLOWED_LOCAL_ONLY` with `allowed=True`; exact-token `codex-live` returns `APPROVED_BUT_NOT_EXECUTED` with `allowed=False`, `approval_recorded=True`, and `live_execution_authorized=False`; and `cyber-execution` remains blocked regardless of token. Approval-token validation is audit-only until a future sprint authorizes live execution, and the gate does not call Codex, live LLMs, cyber tooling, or BLK-test MCP.

---

## 2. Capability Profiles

These profiles are operator-facing readiness labels. They describe what a BLK-pipe run is allowed to mean at this stage; they are not implemented as a runtime policy engine in Sprint 004.

Default operator profiles remain `dev-smoke`, `strict-ci`, or `codex-dry-run`. The Sprint 004 dry-run fixture builder defaults to `codex-dry-run`; any attempt to construct a `codex-live` dry-run payload fails closed before payload construction.

| Profile | Allowed use | Required posture | Sprint 006 status |
|---|---|---|---|
| `dev-smoke` | Local fake-engine / deterministic local command work only. | Use disposable local fixtures, no live secrets, no real cyber targets, no model calls. | `ALLOWED_LOCAL_ONLY` for local development and tests. |
| `strict-ci` | Ephemeral clean clone/worktree with deterministic commands. | Minimal non-secret environment, clean preflight by construction, no inherited credentials, fail closed on residue. | `ALLOWED_LOCAL_ONLY` for CI-style verification. |
| `codex-dry-run` | Fake/dry-run parity fixtures for Codex command shape. | No live model call, no Codex API invocation, deterministic fixture output only. | `ALLOWED_LOCAL_ONLY` as a dry-run compatibility harness. |
| `codex-live` | Future live Codex tactical execution. | Exact approval-token shape plus future sandbox/capability decisions, traceability handoff, review gates, and rollback policy. | Blocked without or with a mismatched token; exact token records audit approval only as `APPROVED_BUT_NOT_EXECUTED` with `allowed=False`. |
| `cyber-execution` | Future cyber-capable execution profile. | Separate sandbox, secret, network, filesystem, process, and audit controls; explicit user approval. | `BLOCKED_CYBER_EXECUTION` regardless of token. |

Short-form profile definitions:

```text
dev-smoke       local fake-engine / deterministic local command work only
strict-ci       ephemeral clean clone/worktree, minimal non-secret environment, no live secrets
codex-dry-run   fake/dry-run parity fixtures for Codex command shape, no live model call
codex-live      future blocked profile requiring explicit user approval and sandbox/capability decisions
cyber-execution future blocked profile requiring separate sandbox/secret/network/process controls
```

---

## 3. Sprint 003 Integration Readiness Improvements

Sprint 003 improves integration readiness without crossing into live tactical execution:

1. **protected vault path coverage** — allowlist validation rejects `docs/active/`, `docs/requirements/`, and `docs/use_cases/` so BLK-req active-vault artifacts remain under HITL/canonical lifecycle control rather than tactical mutation.
2. **trace artifact hash baton transport** — payloads, reports, and the Python adapter carry bounded opaque `trace_artifacts` metadata for BLK-001 `version_hash` baton handoff. BLK-pipe does not parse requirement/use-case bodies, verify hashes against files, generate RTMs, or generate BEOs.
3. **branch-safe revert** — revert payloads that include `target_branch` assert the current branch before destructive reset. Revert does not checkout, fetch, create, or sterilize branches.
4. **payload/validation bounds** — payload JSON ingestion is capped at 2 MiB at CLI file/stdin ingress and at direct `contracts.DecodePayload(data)` / `pipe.Run(ctx, payloadJSON, writer)` boundaries, validation commands are capped by count and command-string length, and validation runs under one overall deadline rather than multiplying work by command count.
5. **adapter status fidelity** — the Python adapter preserves compatible parsed report statuses within the subprocess exit-code family as a BLK-System local V47-compatible extension, distinguishing cases such as `INVALID_PAYLOAD` versus `SYNTAX_GATE_FAILED` while still forcing incompatible statuses to the family default and unknown nonzero outcomes away from `SUCCESS`.

Together, these changes make later orchestration easier to test: the deterministic boundary can carry trace metadata, reject protected authority paths, bound input/work, preserve failure detail, and keep revert semantics branch-safe.

---

## 4. Explicit Non-Authorizations

Sprint 004 does not authorize:

- live Codex execution,
- live local or remote LLM execution,
- offensive cyber activity,
- live BLK-test MCP calls,
- execution against real cyber-program repositories or live targets,
- use of host secrets in payloads, environment variables, packets, validation commands, or engine commands,
- treating BLK-pipe as a full sandbox or host-secret isolation layer,
- broad staging (`git add .`, `git add -u`), stash-based rollback, relative revert anchors, or triple-dot report diffs.

Any future sprint that proposes executable `codex-live` or `cyber-execution` must state its profile explicitly and must include a hard user approval gate with an explicit approval token or phrase before live execution begins. Sprint 006 approval-token validation is audit-only and not sufficient to execute; BLK-015 keeps `allowed=False` for `APPROVED_BUT_NOT_EXECUTED` until a later sprint separately authorizes a live path. Sprint 004 provides fixture-level fail-closed enforcement only for its dry-run builders; it is not a system-wide live approval gate implementation.

---

## 5. Operator Readiness Checklist

Before using a Sprint 004 BLK-pipe path, classify it:

1. If it calls a fake engine or deterministic local command with no secrets, classify it as `dev-smoke`.
2. If it runs in an ephemeral clean clone/worktree with a minimal non-secret environment, classify it as `strict-ci`.
3. If it only exercises Codex command shape with deterministic fixtures and no live model call, classify it as `codex-dry-run`.
4. If it would call Codex, any live LLM, or any network model service, stop: the profile is `codex-live` and remains blocked.
5. If it would run cyber tooling, touch real cyber-program repositories, use live targets, or require sandbox/secret/network/process policy, stop: the profile is `cyber-execution` and remains blocked.

Use the most restrictive applicable profile. When in doubt, treat the run as blocked until the sprint plan and user approval explicitly say otherwise.

---

## 6. Outcome Metadata Gate

After a sprint lands and is pushed, active outcome metadata for that closed sprint must not retain self-referential pending remote state. This applies to both per-task outcome documents and sprint closeouts. Current header metadata should record a pushed remote statement such as ``**Remote:** pushed to `origin/main` ``.

Because historical outcome documents may quote older pending strings as RED evidence or OLD examples, the gate checks the current metadata header only. For each closed sprint under review, scan the first 12 lines of every matching outcome document:

```bash
python3 - <<'PY'
from pathlib import Path
sprint_prefix = 'BLK-PIPE-005'
for p in sorted(Path('docs/outcomes').glob(f'{sprint_prefix}*.md')):
    text = p.read_text()
    for line in text.splitlines()[:12]:
        if line.startswith('**Remote:**') and 'pending' in line.lower():
            raise AssertionError(f'{p}: stale pending remote metadata: {line}')
print('OUTCOME_REMOTE_METADATA_PASS')
PY
```

Future sprint task outcomes and closeouts should use the same gate shape with that sprint's outcome prefix before declaring per-task outcomes or closeouts pushed/aligned.

---

## 7. Related Documents

- [`BLK-010 — BLK-pipe Sprint 002 V47 Hardening CLI Contract`](BLK-010_blk-pipe-v47-hardening-cli.md) defines the CLI, payload/report fields, router codes, validation, revert, branch behavior, and Python adapter path.
- [`BLK-011 — BLK-pipe Cyber Readiness and Usability Guardrails`](BLK-011_blk-pipe-cyber-readiness-and-usability.md) documents operator safety expectations, host-secret limitations, and why BLK-pipe is not a complete cyber sandbox.
- [`BLK-013 — BLK-test Handoff Fixture Contract`](BLK-013_blk-test-handoff-fixture-contract.md) defines fixture-only BLK-test PASS/FAIL/BLOCKED handoff objects with no live BLK-test MCP.
- [`BLK-014 — BLK Execution Outcome Fixture Shape`](BLK-014_blk-execution-outcome-fixture-shape.md) defines the fixture/draft-only BEO projection shape and states that RTM is not generated.
- [`BLK-015 — BLK-pipe Approval and MCP Integration Design`](BLK-015_blk-pipe-approval-and-mcp-integration-design.md) defines the fail-closed approval-token contract, Sprint 006 audit-only `codex-live` approval semantics, and disabled BLK-test MCP request/response stubs.
- [`docs/plans/BLK-PIPE-004_dry-run-orchestrator-and-blk-test-fixtures.md`](plans/BLK-PIPE-004_dry-run-orchestrator-and-blk-test-fixtures.md) records the Sprint 004 implementation plan and verification requirements.
