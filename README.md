# BLK-System

BLK-System is the autonomous development-process architecture for Kuronode.
It adapts the Systems Engineering V-Model for AI-assisted software delivery by separating architectural intent, tactical execution, physical verification, and traceability into bounded subsystems.

## Initial doctrine documents

- [`docs/BLK-001_blk-system-master-architecture.md`](docs/BLK-001_blk-system-master-architecture.md) — master architecture and subsystem map.
- [`docs/BLK-002_blk-req-artifact-lifecycle.md`](docs/BLK-002_blk-req-artifact-lifecycle.md) — `blk-req` artifact intake and lifecycle protocol.
- [`docs/BLK-003_blk-pipe-blk-test-orchestration.md`](docs/BLK-003_blk-pipe-blk-test-orchestration.md) — `blk-pipe` / `blk-test` orchestration protocol.
- [`docs/reviews/BLK-000_initial-doctrine-review.md`](docs/reviews/BLK-000_initial-doctrine-review.md) — initial review notes and unresolved design issues.
- [`docs/BLK-004_blk-pipe-v47-architecture-suite.md`](docs/BLK-004_blk-pipe-v47-architecture-suite.md) — `blk-pipe` V47 architecture suite and deterministic transport constraints.
- [`docs/BLK-005_blk-req-specification.md`](docs/BLK-005_blk-req-specification.md) — `blk-req` requirements/use-case specification.
- [`docs/BLK-006_blk-req-implementation-brief.md`](docs/BLK-006_blk-req-implementation-brief.md) — `blk-req` implementation architecture and solutions brief.
- [`docs/BLK-007_dependency-graph-recon-tool.md`](docs/BLK-007_dependency-graph-recon-tool.md) — read-only dependency graph reconnaissance tool instructions.
- [`docs/BLK-008_blk-test-mcp-execution-server.md`](docs/BLK-008_blk-test-mcp-execution-server.md) — `blk-test` MCP physics oracle / test execution server instructions.
- [`docs/BLK-009_blk-pipe-sprint-001-cli.md`](docs/BLK-009_blk-pipe-sprint-001-cli.md) — first local `blk-pipe` Sprint 001 CLI contract and safety guarantees.
- [`docs/BLK-010_blk-pipe-v47-hardening-cli.md`](docs/BLK-010_blk-pipe-v47-hardening-cli.md) — Sprint 002 V47-compatible `blk-pipe` hardening CLI contract, report fields, router codes, validation/revert/branch behavior, and Python adapter path.
- [`docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md`](docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md) — Sprint 002.2 operator guardrails for clean preflight, validation mutation failures, unsafe generated modes, `l2_packet` stdin handling, host-secret limitations, and why BLK-pipe is not a complete sandbox.
- [`docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md`](docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md) — Sprint 006 integration-readiness and capability-profile guidance. The gate does not run Codex, authorize live LLM execution, authorize cyber execution, or call BLK-test MCP; exact-token `codex-live` records audit-only `APPROVED_BUT_NOT_EXECUTED` with `allowed=False`.
- [`docs/BLK-013_blk-test-handoff-fixture-contract.md`](docs/BLK-013_blk-test-handoff-fixture-contract.md) — Sprint 004/005 BLK-test fixture handoff contract. It uses fixture-only PASS/FAIL/BLOCKED objects, no live BLK-test MCP, and PASS requires BLK-pipe SUCCESS evidence.
- [`docs/BLK-014_blk-execution-outcome-fixture-shape.md`](docs/BLK-014_blk-execution-outcome-fixture-shape.md) — Sprint 004/005 BEO fixture/draft-only projection contract. RTM is not generated and the fixture does not inspect active BLK-req files.
- [`docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`](docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md) — fail-closed approval gate with Sprint 006 audit-only `codex-live` approval semantics and source-bound disabled BLK-test MCP request/response design stubs.
- [`docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`](docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md) — Sprint 007 disabled adapter smoke, explicit not-run MCP request, draft-only BEO projection, and BEO/RTM interface fixture contract; it keeps live BLK-test MCP, RTM generation, and authoritative BEO publication disabled and does not authorize live execution.

## BLK-pipe Sprint 001 CLI

- [`docs/BLK-009_blk-pipe-sprint-001-cli.md`](docs/BLK-009_blk-pipe-sprint-001-cli.md) — local developer command contract for `blk-pipe --health`, `blk-pipe --payload /absolute/path/to/payload.json`, and `blk-pipe --payload-stdin`, plus Sprint 001 safety guarantees and BLK-004/V47 deferrals.

## BLK-pipe Sprint 002 V47 hardening

- [`docs/BLK-010_blk-pipe-v47-hardening-cli.md`](docs/BLK-010_blk-pipe-v47-hardening-cli.md) — current local developer contract for `go run ./cmd/blk-pipe --health`, illustrative `go run ./cmd/blk-pipe --payload /tmp/payload.json` with a prepared absolute payload file, optional/internal `go run ./cmd/blk-pipe --payload-stdin`, V47-compatible payload/report fields, strict router exit codes, validation gates, revert route, branch/fetch/orphan behavior, and the `python/blk_pipe_adapter.py` adapter. Sprint 002.2 does not run Codex.
- [`docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md`](docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md) — Sprint 002.2 usability and cyber-readiness guardrails. It distinguishes `dev-smoke`, `strict-ci`, and future `cyber-execution` guidance without claiming cyber-execution is implemented.
- [`docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md`](docs/BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md) — Sprint 006 readiness boundaries and capability profiles. BLK-pipe is not a full sandbox, `codex-live` approval-token validation is audit-only with `allowed=False`, and `cyber-execution` remains blocked.
- [`docs/BLK-013_blk-test-handoff-fixture-contract.md`](docs/BLK-013_blk-test-handoff-fixture-contract.md) — Sprint 004/005 BLK-test fixture contract with no live BLK-test MCP.
- [`docs/BLK-014_blk-execution-outcome-fixture-shape.md`](docs/BLK-014_blk-execution-outcome-fixture-shape.md) — Sprint 004/005 BEO fixture/draft-only projection; RTM is not generated.
- [`docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`](docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md) — fail-closed approval-token and source-bound disabled BLK-test MCP request/response design contract; `allowed` means executable now.
- [`docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`](docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md) — Sprint 007 fixture-only contract for disabled adapter smoke, not-run request shape, draft BEO projection, and disabled BEO/RTM interface fixtures. Sprint 007 remains disabled/fixture-only and does not authorize live execution.

## Core idea

Hermes acts as Architect and Hostile Auditor. Codex/engine acts as a tactical worker. Deterministic tooling (`blk-req`, `blk-pipe`, `blk-test`, and the traceability aggregator) enforces repository physics and preserves structured `trace_artifacts` / `version_hash` evidence so LLM memory, scope drift, or chat context cannot become the source of truth.
