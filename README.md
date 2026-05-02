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

## BLK-pipe Sprint 001 CLI

- [`docs/BLK-009_blk-pipe-sprint-001-cli.md`](docs/BLK-009_blk-pipe-sprint-001-cli.md) — local developer command contract for `blk-pipe --health`, `blk-pipe --payload /absolute/path/to/payload.json`, and `blk-pipe --payload-stdin`, plus Sprint 001 safety guarantees and BLK-004/V47 deferrals.

## Core idea

Hermes acts as Architect and Hostile Auditor. Codex/engine acts as a tactical worker. Deterministic tooling (`blk-req`, `blk-pipe`, `blk-test`, and the traceability aggregator) enforces repository physics and prevents LLM memory, scope drift, or chat context from becoming the source of truth.
