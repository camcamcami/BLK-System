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

## BLK-pipe Sprint 001 CLI

- [`docs/BLK-009_blk-pipe-sprint-001-cli.md`](docs/BLK-009_blk-pipe-sprint-001-cli.md) — local developer command contract for `blk-pipe --health`, `blk-pipe --payload /absolute/path/to/payload.json`, and `blk-pipe --payload-stdin`, plus Sprint 001 safety guarantees and BLK-004/V47 deferrals.

## BLK-pipe Sprint 002 V47 hardening

- [`docs/BLK-010_blk-pipe-v47-hardening-cli.md`](docs/BLK-010_blk-pipe-v47-hardening-cli.md) — current local developer contract for `go run ./cmd/blk-pipe --health`, illustrative `go run ./cmd/blk-pipe --payload /tmp/payload.json` with a prepared absolute payload file, optional/internal `go run ./cmd/blk-pipe --payload-stdin`, V47-compatible payload/report fields, strict router exit codes, validation gates, revert route, branch/fetch/orphan behavior, and the `python/blk_pipe_adapter.py` adapter. Sprint 002.2 does not run Codex.
- [`docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md`](docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md) — Sprint 002.2 usability and cyber-readiness guardrails. It distinguishes `dev-smoke`, `strict-ci`, and future `cyber-execution` guidance without claiming cyber-execution is implemented.

## Core idea

Hermes acts as Architect and Hostile Auditor. Codex/engine acts as a tactical worker. Deterministic tooling (`blk-req`, `blk-pipe`, `blk-test`, and the traceability aggregator) enforces repository physics and prevents LLM memory, scope drift, or chat context from becoming the source of truth.
