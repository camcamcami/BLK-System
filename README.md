# BLK-System

BLK-System is an experimental, local-first development control system for AI-assisted software work.

It was built around Kuronode, but the core idea is general: keep product intent, tactical coding, verification, and traceability separate so an AI agent can help write software without chat memory or a passing test becoming the source of authority.

## What problem it is trying to solve

AI coding agents are useful, but they can blur boundaries:

- a vague request becomes an implementation plan;
- a passing test is treated as product approval;
- generated code changes are hard to trace back to requirements;
- agent context, tool output, and repository state drift apart.

BLK-System adds a deterministic process layer around that work. Requirements, execution briefs, route manifests, validation profiles, and outcome records are hash-bound and checked locally before any tactical worker is allowed to act.

## Current status

**Ready for controlled real use. Not a turnkey production platform.**

The current working vertical is:

1. write or update a requirement;
2. snapshot and hash-bind the requirement;
3. write architect-owned BEB and L2 packets;
4. create an approved drop manifest;
5. route the work through `blkhermes -> BLK-pipe -> Codex`;
6. relay progress back to Discord;
7. verify the target repository result;
8. record a lean closeout.

The latest end-to-end validation changed a Kuronode dashboard requirement back to a yellow validation element, ran the BEB/L2/drop path through `blkhermes`, patched a clean target worktree through Codex, and verified the expected source result.

## What BLK-System is not

BLK-System intentionally does **not** currently grant:

- reusable autonomous production authority;
- reusable `blk-link` or RTM generation;
- broad protected-body access;
- generic BLK-pipe/Codex dispatch;
- production BLK-test MCP server/client runtime;
- blanket permission for an agent to mutate any target repository.

Those surfaces remain exact, bounded, and separately reviewed.

## Main components

| Component | Purpose |
| --- | --- |
| `blk-req` | Requirement and use-case lifecycle concepts, including snapshots and exact IDs. |
| `blk-pipe` | Bounded execution route / blast shield around tactical code changes. |
| `blk-test` | Functional verification/oracle layer. This is a BLK-System module, not the repository's own test suite. |
| BEB | Build Execution Brief: architect-authored product intent and acceptance boundary. |
| L2 | Architect-authored execution packet that narrows the BEB into a tactical route. |
| BEO | Build Execution Outcome: evidence record produced after a bounded run. |
| RTM / `blk-link` | Traceability closure concepts. Current reusable production authority is still intentionally denied. |
| `blkhermes` | Dedicated Hermes profile/gateway path used to run and report BLK-System work. |

## Repository layout

```text
BLK-System/
├── cmd/blk-pipe/             # Go CLI entrypoint for blk-pipe
├── internal/pipe/            # Go implementation/tests for pipe execution behavior
├── python/                   # Python fixtures, validators, route adapters, and tests
├── docs/                     # Doctrine, roadmap, current state, and closeout records
├── scripts/                  # Host setup helpers, including private Codex bwrap setup
├── testdata/                 # Hash-bound validation examples and route fixtures
├── go.mod
└── README.md
```

Start with these documents:

- [`docs/BLK-001_blk-system-master-architecture.md`](docs/BLK-001_blk-system-master-architecture.md) — original architecture map.
- [`docs/BLK-003_blk-pipe-blk-test-orchestration.md`](docs/BLK-003_blk-pipe-blk-test-orchestration.md) — BLK-pipe / BLK-test orchestration doctrine.
- [`docs/BLK-077_blk-system-post-078-roadmap.md`](docs/BLK-077_blk-system-post-078-roadmap.md) — current roadmap.
- [`docs/BLK-079_post-078-current-state-authority-index.md`](docs/BLK-079_post-078-current-state-authority-index.md) — compact current-state authority index.
- [`docs/outcomes/BLK-SYSTEM-341_sprint-closeout.md`](docs/outcomes/BLK-SYSTEM-341_sprint-closeout.md) — latest blkhermes-relayed end-to-end validation closeout.

## Quick start

Clone the repository:

```bash
git clone https://github.com/camcamcami/BLK-System.git
cd BLK-System
```

Run the Go tests:

```bash
go test ./...
```

Run the Python test suite:

```bash
TMPDIR=/var/tmp/blk-system-testtmp \
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache \
python3 -m unittest discover -s python -p 'test_*.py'
```

Check the local BLK-pipe CLI:

```bash
go run ./cmd/blk-pipe --health
```

## Using BLK-System with Hermes

The intended operator workflow uses Hermes as the architect / auditor and Codex as the tactical worker. For serious use, keep a dedicated Hermes profile for BLK-System execution instead of mixing it into a general chat profile.

Recommended profile stance:

- use a local profile such as `blkhermes` for execution/status relay;
- keep API keys, Discord tokens, OAuth state, sessions, and memory out of this repository;
- commit only sanitized docs, fixtures, source, and tests;
- let Hermes/architect author the BEB and L2, then let BLK-System validate and route those inputs;
- do not let BLK-System invent its own mission when a BEB or L2 is missing.

Example local setup commands:

```bash
hermes profile create blkhermes --clone default
hermes -p blkhermes config set terminal.cwd /path/to/BLK-System
hermes -p blkhermes config set agent.max_turns 500
```

If Discord progress relay is needed, configure it locally in the `blkhermes` profile:

```bash
hermes -p blkhermes gateway setup
hermes -p blkhermes gateway install
hermes -p blkhermes gateway start
```

Do **not** commit a Hermes profile export, `.env`, gateway token, session store, or profile memory. A profile is runtime configuration; the repository should contain only the reproducible project artifacts and documentation needed to recreate the workflow.

## Codex sandbox note

The preferred Codex route uses workspace-write containment with a private `bwrap` path rather than relaxing AppArmor user namespace policy globally.

On a host that needs this setup:

```bash
sudo scripts/setup-codex-private-bwrap.sh
export BLK_CODEX_PRIVATE_BWRAP_DIR=/opt/blk-system/codex-bwrap
export PATH=/opt/blk-system/codex-bwrap:$PATH
```

This is host-specific setup. Review the script before running it.

## Development rules of thumb

- Treat evidence as evidence, not authority.
- Keep requirement snapshots and route manifests hash-bound.
- Prefer one lean outcome record per sprint/run.
- Run hostile review before committing authority-sensitive changes.
- Patch real blockers as they appear; avoid paperwork-only sprints.
- Keep BLK-001 through BLK-006 as doctrine/architecture references, not moving sprint-status documents.

## Collaboration notes

This repository is currently private. To share it with a friend, add them as a GitHub collaborator or move the repository to an organization/team with appropriate access.

Useful GitHub commands:

```bash
# View repository visibility and URL
gh repo view camcamcami/BLK-System --json nameWithOwner,visibility,url

# Invite a collaborator by username
gh api \
  --method PUT \
  repos/camcamcami/BLK-System/collaborators/GITHUB_USERNAME \
  -f permission=push
```

Replace `GITHUB_USERNAME` with the friend's GitHub username.
