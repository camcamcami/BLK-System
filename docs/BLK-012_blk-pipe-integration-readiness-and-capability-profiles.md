# BLK-012 — BLK-pipe Integration Readiness and Capability Profiles

**Status:** Active Sprint 003 operator guidance
**Scope:** BLK-pipe integration readiness boundaries, capability profiles, and blocked live-execution scope
**Date:** 2026-05-04

---

## 1. Boundary Statement

BLK-pipe is a deterministic repository mutation gate and bounded local command transport. Sprint 003 improves the handoff surface between doctrine, payloads, reports, and the Python adapter so future orchestration can be tested against explicit safety boundaries.

Sprint 003 does not run Codex. Sprint 003 does not authorize live LLM execution. Sprint 003 does not authorize cyber execution. It does not call OpenAI, local LLMs, network model services, offensive cyber tooling, real cyber-program repositories, or live tactical engines.

BLK-pipe is not a full sandbox. BLK-pipe is not general host-secret isolation. It does not replace container, VM, cgroup, namespace, seccomp/AppArmor/SELinux, network, filesystem, secret-management, or malware-analysis controls.

`codex-live` and `cyber-execution` remain blocked until explicitly approved in a future sprint. Approval must be separate from this document and must include concrete sandbox, capability, network, secret, process, and review decisions before any live tactical execution.

---

## 2. Capability Profiles

These profiles are operator-facing readiness labels. They describe what a BLK-pipe run is allowed to mean at this stage; they are not implemented as a runtime policy engine in Sprint 003.

| Profile | Allowed use | Required posture | Sprint 003 status |
|---|---|---|---|
| `dev-smoke` | Local fake-engine / deterministic local command work only. | Use disposable local fixtures, no live secrets, no real cyber targets, no model calls. | Allowed for local development and tests. |
| `strict-ci` | Ephemeral clean clone/worktree with deterministic commands. | Minimal non-secret environment, clean preflight by construction, no inherited credentials, fail closed on residue. | Allowed for CI-style verification. |
| `codex-dry-run` | Fake/dry-run parity fixtures for Codex command shape. | No live model call, no Codex API invocation, deterministic fixture output only. | Allowed only as a dry-run compatibility harness. |
| `codex-live` | Future live Codex tactical execution. | Explicit user approval plus sandbox/capability decisions, traceability handoff, review gates, and rollback policy. | Blocked. |
| `cyber-execution` | Future cyber-capable execution profile. | Separate sandbox, secret, network, filesystem, process, and audit controls; explicit user approval. | Blocked. |

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
4. **payload/validation bounds** — payload JSON ingestion is capped at 2 MiB, validation commands are capped by count and command-string length, and validation runs under one overall deadline rather than multiplying work by command count.
5. **adapter status fidelity** — the Python adapter preserves compatible parsed report statuses within the subprocess exit-code family, distinguishing cases such as `INVALID_PAYLOAD` versus `SYNTAX_GATE_FAILED` while still forcing unsafe or unknown nonzero outcomes away from `SUCCESS`.

Together, these changes make later orchestration easier to test: the deterministic boundary can carry trace metadata, reject protected authority paths, bound input/work, preserve failure detail, and keep revert semantics branch-safe.

---

## 4. Explicit Non-Authorizations

This document does not authorize:

- live Codex execution,
- live local or remote LLM execution,
- offensive cyber activity,
- execution against real cyber-program repositories or live targets,
- use of host secrets in payloads, environment variables, packets, validation commands, or engine commands,
- treating BLK-pipe as a full sandbox or host-secret isolation layer,
- broad staging (`git add .`, `git add -u`), stash-based rollback, relative revert anchors, or triple-dot report diffs.

Any future sprint that proposes `codex-live` or `cyber-execution` must state its profile explicitly and must include a separate human approval gate before live execution begins.

---

## 5. Operator Readiness Checklist

Before using a Sprint 003 BLK-pipe path, classify it:

1. If it calls a fake engine or deterministic local command with no secrets, classify it as `dev-smoke`.
2. If it runs in an ephemeral clean clone/worktree with a minimal non-secret environment, classify it as `strict-ci`.
3. If it only exercises Codex command shape with deterministic fixtures and no live model call, classify it as `codex-dry-run`.
4. If it would call Codex, any live LLM, or any network model service, stop: the profile is `codex-live` and remains blocked.
5. If it would run cyber tooling, touch real cyber-program repositories, use live targets, or require sandbox/secret/network/process policy, stop: the profile is `cyber-execution` and remains blocked.

Use the most restrictive applicable profile. When in doubt, treat the run as blocked until the sprint plan and user approval explicitly say otherwise.

---

## 6. Related Documents

- [`BLK-010 — BLK-pipe Sprint 002 V47 Hardening CLI Contract`](BLK-010_blk-pipe-v47-hardening-cli.md) defines the CLI, payload/report fields, router codes, validation, revert, branch behavior, and Python adapter path.
- [`BLK-011 — BLK-pipe Cyber Readiness and Usability Guardrails`](BLK-011_blk-pipe-cyber-readiness-and-usability.md) documents operator safety expectations, host-secret limitations, and why BLK-pipe is not a complete cyber sandbox.
- [`docs/plans/BLK-PIPE-003_integration-readiness-and-capability-profiles.md`](plans/BLK-PIPE-003_integration-readiness-and-capability-profiles.md) records the Sprint 003 implementation plan and verification requirements.
