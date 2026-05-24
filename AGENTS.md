# BLK-System Agent Instructions

These instructions apply to agents operating inside this repository.

## Project framing

BLK-System is a local-first engineering control loop for AI-assisted software work. Frame the project through the Systems Engineering V-Model and system-of-systems development:

1. start from high-level intent;
2. decompose into requirements, architecture, BEB, L2, and exact route inputs;
3. execute bounded tactical work through the approved route;
4. climb back up through verification evidence, outcome records, and traceability.

The problem BLK-System addresses is the same class of problem the V-Model addresses: requirements, design, implementation, and verification drift. In AI-assisted development, that drift can happen faster because chat context, tool output, repository state, tactical edits, tests, and closeout evidence can disagree. BLK-System exists to keep those layers connected without letting chat memory or a passing test become the source of truth.

## Required skills / operating knowledge

When using Hermes Agent in this repository, load these skills before planning or editing:

- `blk-system-sprint-execution`
- `blk-system-authority-gated-sprints`

Also load `hermes-agent` when changing Hermes profiles, gateway behavior, tools, skills, or agent setup.

## Role boundary

Preserve this split:

- Architect/System Engineer Hermes owns intent: requirements, BEB, L2, acceptance boundaries, and architecture decisions.
- BLK-System validates, schema-checks, hash-binds, routes, and records evidence from the architect-authored inputs.
- `blkhermes` is the dedicated executor/status-relay profile for BLK-System work on this host.
- Codex is the tactical coding worker for implementation routed through BLK-System when feature work requires tactical code changes.

BLK-System must not invent a missing BEB or L2. If BEB/L2 intent is absent or underspecified, stop and ask for clarification or create an explicit architect-authored packet first.

## Authority boundary

Evidence is not authority. A PASSing test, successful route report, green hostile review, or closeout record does not grant adjacent runtime/product authority.

Unless an exact bounded package explicitly grants it, keep these denied:

- BEO publication or closeout execution;
- RTM generation or production `blk-link`;
- run-ID reservation or consumption;
- signer, storage, ledger, rollback, or reuse actions;
- protected-body reads, copying, parsing, hashing, scanning, or mutation;
- production BLK-test MCP or generic runtime/tooling expansion;
- target/source/Git mutation outside exact BLK-System development authority and exact allowlists;
- package-manager, network, browser, model-service, cyber tooling, or production-isolation claims.

Development authority for this BLK-System repository is separate from product/runtime gates. Normal source, docs, tests, commits, and pushes for BLK-System development are allowed under the operator's standing development authority, but product/runtime side effects still require exact gates.

## Standard repo preflight

Before editing, run or otherwise establish equivalent evidence:

```bash
cd /home/dad/BLK-System
export PATH="$HOME/.local/bin:$PATH"
git status --short --branch
git fetch origin main
git status --short --branch
git log -1 --oneline --decorate
git config user.name camcamcami
git config user.email cam.elvey@gmail.com
```

If the repo is dirty or behind remote, inspect and reconcile before changing files. Do not overwrite uncommitted user work.

## Execution discipline

- Use strict TDD for source-code behavior changes.
- Use exact-path file staging; never use `git add .` or broad cleanup commands.
- Keep BLK-001 through BLK-006 as stable doctrine, not moving status dashboards.
- Prefer one lean outcome closeout per sprint/run under `docs/outcomes/BLK-SYSTEM-###_sprint-closeout.md`.
- Avoid creating new root `docs/BLK-###` files unless the change is durable doctrine, a reusable contract, or an authority boundary.
- Run hostile review before every commit that could affect authority, evidence trust, execution routing, protected data, runtime behavior, or current-state wording.
- Replace secrets, tokens, API keys, OAuth state, Discord tokens, private credentials, and personal access tokens with `[REDACTED]` in any committed artifact.

## Verification defaults

For Python verification, prefer the cache-safe environment used by this repo:

```bash
rm -rf /var/tmp/blk-system-testtmp /var/tmp/blk-system-pycache
mkdir -p /var/tmp/blk-system-testtmp /var/tmp/blk-system-pycache
TMPDIR=/var/tmp/blk-system-testtmp \
PYTHONPATH=python \
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache \
python3 -m unittest discover -s python -p 'test_*.py'
```

For Go changes, run:

```bash
go test ./...
```

For docs-only changes, run focused policy/link/whitespace checks plus `git diff --check -- <exact paths>`.

## `blkhermes` communication contract

When `blkhermes` runs BLK-System work with Discord relay, communicate meaningful milestones only. Prefer these events:

- run started;
- requirement snapshot or drop hash prepared;
- preflight started;
- preflight blocked or ready;
- BLK-pipe/Codex route started;
- Codex completed or failed;
- validation started;
- validation passed or failed;
- route report hash emitted;
- target commit hash observed;
- closeout written, committed, or pushed.

Do not send scheduled status spam. Do not describe product/runtime side effects as authorized unless the exact package grants them.

## Do not commit runtime profile state

Keep Hermes runtime configuration local. Do not commit:

- `.env` files;
- profile exports;
- Discord bot tokens;
- OAuth credentials;
- API keys;
- session stores;
- local memory files;
- generated caches;
- ignored build/dependency outputs unless explicitly authorized.

Commit only sanitized source, tests, fixtures, and documentation needed to reproduce the BLK-System workflow.
