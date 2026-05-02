# BLK-System

BLK-System is the autonomous development-process architecture for Kuronode.
It adapts the Systems Engineering V-Model for AI-assisted software delivery by separating architectural intent, tactical execution, physical verification, and traceability into bounded subsystems.

## Initial doctrine documents

- [`docs/BLK-001_blk-system-master-architecture.md`](docs/BLK-001_blk-system-master-architecture.md) — master architecture and subsystem map.
- [`docs/BLK-002_blk-req-artifact-lifecycle.md`](docs/BLK-002_blk-req-artifact-lifecycle.md) — `blk-req` artifact intake and lifecycle protocol.
- [`docs/BLK-003_blk-pipe-blk-test-orchestration.md`](docs/BLK-003_blk-pipe-blk-test-orchestration.md) — `blk-pipe` / `blk-test` orchestration protocol.
- [`docs/reviews/BLK-000_initial-doctrine-review.md`](docs/reviews/BLK-000_initial-doctrine-review.md) — initial review notes and unresolved design issues.

## Core idea

Hermes acts as Architect and Hostile Auditor. Codex/engine acts as a tactical worker. Deterministic tooling (`blk-req`, `blk-pipe`, `blk-test`, and the traceability aggregator) enforces repository physics and prevents LLM memory, scope drift, or chat context from becoming the source of truth.
