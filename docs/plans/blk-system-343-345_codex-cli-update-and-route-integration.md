# BLK-SYSTEM-343..345 — Codex CLI Update and Route Integration Sprint Package

**Status:** Prepared for execution — package plan only
**Date:** 2026-05-30
**Operator directive:** Prepare a BLK-System sprint package to integrate new Codex CLI features that benefit BLK-System; updating Codex is part of the package.

## 1. Package Goal

Upgrade the local Codex CLI and integrate the useful new Codex surfaces into BLK-System’s BEB/L2 → BLK-pipe → Codex route without widening authority.

The package treats Codex CLI improvements as subordinate operational controls and evidence sources. BLK-System remains the route enforcement/checking boundary: it validates externally approved exact manifests, hash-binds submitted BEB/L2 artifacts, route-checks trusted roots/workdirs and target hashes, enforces allowlists/validation profiles, and blocks fail-closed. BLK-System does not author or approve BEB/L2 intent.

## 2. Preflight Evidence Already Observed

From local inspection before preparing this package:

- Installed CLI: `codex-cli 0.130.0`
- npm latest: `@openai/codex 0.135.0`
- `codex exec --help` for `0.135.0` still includes the current BLK route baseline flags:
  - `--sandbox workspace-write`
  - `--ephemeral`
  - `--ignore-user-config`
  - `--ignore-rules`
  - repeated `--disable`
  - `--json`
  - `--output-last-message`
- Release-note review through `rust-v0.135.0` identified useful BLK-facing features:
  - richer `codex doctor` diagnostics;
  - better permission/profile plumbing;
  - non-interactive installer mode via `CODEX_NON_INTERACTIVE=1`;
  - `codex exec resume --output-schema` for explicitly modeled recovery workflows;
  - Python SDK auth/turn/Sandbox improvements for a future SDK adapter.

## 3. Sprint Package

### BLK-SYSTEM-343 — Controlled Codex CLI update and smoke evidence

**Objective:** Update Codex CLI from `0.130.0` to the current stable `0.135.0`, then record deterministic local smoke evidence.

**Scope:**

- Update the installed CLI using the normal npm package path with non-interactive installer controls where applicable.
- The explicit update action is part of this sprint:

```bash
export PATH="$HOME/.local/bin:$PATH"
CODEX_NON_INTERACTIVE=1 npm install -g @openai/codex@0.135.0
```

- Record:
  - `codex --version`;
  - `npm view @openai/codex version`;
  - `codex exec --help` baseline-flag inventory;
  - `codex doctor` advisory diagnostics;
  - BLK-SYSTEM-229 private-bwrap/AppArmor descriptor evidence;
  - a no-op `workspace-write` smoke in a disposable Git repo if private-bwrap setup is present.
  - Scrub/redact any auth/profile/path-sensitive diagnostics before committing smoke evidence.
- Do not change BEB/L2 route behavior yet except for any compatibility fix required to keep current tests passing.

**Candidate files:**

- `scripts/smoke-codex-cli.sh` or `python/codex_cli_capability_probe.py`
- `python/test_codex_cli_capability_probe.py`
- `docs/outcomes/BLK-SYSTEM-343_sprint-closeout.md`

**Verification:**

```bash
export PATH="$HOME/.local/bin:$PATH"
codex --version
npm view @openai/codex version
codex exec --help
codex doctor || true
SMOKE_DIR=$(mktemp -d /var/tmp/blk-codex-smoke.XXXXXX)
git -C "$SMOKE_DIR" init -b smoke
git -C "$SMOKE_DIR" config user.name smoke
git -C "$SMOKE_DIR" config user.email smoke@example.invalid
printf 'smoke\n' > "$SMOKE_DIR/README.md"
git -C "$SMOKE_DIR" add README.md
git -C "$SMOKE_DIR" commit -m smoke
BLK_CODEX_PRIVATE_BWRAP_DIR=/opt/blk-system/codex-bwrap \
PATH=/opt/blk-system/codex-bwrap:$PATH \
codex exec --sandbox workspace-write --ephemeral --ignore-user-config --ignore-rules --disable hooks --disable plugins --disable goals --json --output-last-message "$SMOKE_DIR/final.md" -C "$SMOKE_DIR" 'Report the repository status without modifying files.'
git -C "$SMOKE_DIR" status --short
TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python3 -m unittest python.test_codex_cli_capability_probe
```

**Stop conditions:**

- `codex exec --help` no longer exposes the route baseline flags.
- `workspace-write` fails because private-bwrap/AppArmor setup is missing or blocked.
- Auth changes cause Codex to lose access to the selected model.
- Any upgrade path attempts to read or commit secrets/profile runtime state.
- `codex doctor` or smoke logs expose secrets/auth tokens/profile state that cannot be safely redacted for commit.

### BLK-SYSTEM-344 — Codex capability probe integration into BEB/L2 preflight

**Objective:** Make BLK-System record and validate a Codex capability inventory before exact BEB/L2 dispatch.

**Scope:**

- Add a deterministic capability probe that classifies the local CLI as READY/BLOCKED/ADVISORY.
- Require baseline non-interactive route flags before BLK-pipe dispatch:
  - `--sandbox workspace-write`
  - `--ephemeral`
  - `--ignore-user-config`
  - `--ignore-rules`
  - `--disable`
  - `--json`
  - `--output-last-message`
- Treat `codex doctor` as advisory evidence only; it may explain failures but must not grant dispatch authority.
- Preserve fail-closed behavior: if required flags or private-bwrap evidence are missing, block before Codex invocation.

**Candidate files:**

- `python/beb_l2_blk_pipe_route.py`
- `python/codex_cli_capability_probe.py`
- `python/test_beb_l2_blk_pipe_route.py`
- `python/test_codex_cli_capability_probe.py`
- `docs/outcomes/BLK-SYSTEM-344_sprint-closeout.md`

**Verification:**

```bash
TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python3 -m unittest python.test_codex_cli_capability_probe python.test_beb_l2_blk_pipe_route
```

**Hostile probes:**

- Forged help output omits `--ignore-rules` but claims READY.
- `codex doctor` says OK but required `exec` flags are missing.
- Caller-controlled drop manifest attempts to override probe result or engine args.
- Probe evidence contains authority/protected-body wording; it must remain diagnostic only.

### BLK-SYSTEM-345 — Structured Codex final artifact schema and route evidence binding

**Objective:** Use Codex’s structured final-output support for BLK route observability while preserving the rule that Codex output is evidence, not authority.

**Scope:**

- Add a repository-owned JSON schema for the Codex final message artifact.
- Pass `--output-schema <repo-owned-schema>` from BLK-System-owned engine args only after compatibility is verified.
- Keep `--output-last-message <artifact>` and `--json` event stream evidence.
- Ensure caller manifests cannot choose the schema path, output artifact path, or engine flags.
- The schema may request fields such as summary, files_changed, tests_run, blockers, and self-reported confidence; these remain advisory and must be hostile-audited against Git diff and validation evidence.

**Candidate files:**

- `schemas/codex/final-message.schema.json`
- `python/beb_l2_blk_pipe_route.py`
- `python/test_beb_l2_blk_pipe_route.py`
- `docs/outcomes/BLK-SYSTEM-345_sprint-closeout.md`

**Verification:**

```bash
python3 -m json.tool schemas/codex/final-message.schema.json >/dev/null
TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python3 -m unittest python.test_beb_l2_blk_pipe_route
```

**Hostile probes:**

- Caller-controlled manifest attempts `output_schema`, `output_last_message`, `engine_args`, or equivalent aliases.
- Codex final JSON claims PASS while validation profile evidence fails.
- Schema text or output fields contain BEO/RTM/`blk-link`/protected-body authority claims.
- Structured output is mistaken for approval, BEO closeout execution, RTM truth, or source-of-truth evidence.

## 4. Authority Boundary

This package does not authorize:

- BEB or L2 authorship by BLK-System;
- live Codex dispatch outside an exact approved BEB/L2/drop manifest;
- reusable Codex dispatch or broad BLK-pipe dispatch;
- BEO publication or BEO closeout execution;
- RTM generation, production `blk-link`, drift rejection, coverage truth, or active-vault comparison;
- protected-body reads/copying/parsing/hashing/scanning/mutation;
- production BLK-test MCP or generic runtime/tooling expansion;
- Kuronode source/Git mutation except through separately approved exact BEB/L2 payloads;
- package/network/model/browser/cyber tooling beyond the explicit local Codex CLI update and smoke checks in BLK-SYSTEM-343.

Updating Codex is operational setup for BLK-System development. It is not product/runtime authority and not proof of production isolation.

## 5. Documentation Burden Decision

No new root `docs/BLK-###` document is planned. This package is intentionally split into three separately auditable sprints, so it uses one closeout per sprint: BLK-SYSTEM-343 for the CLI update/smoke, BLK-SYSTEM-344 for capability-probe preflight integration, and BLK-SYSTEM-345 for structured final-artifact binding. A root BLK document should be considered only if BLK-SYSTEM-344 or 345 creates a durable new route contract that cannot be captured in code/tests and closeouts.

## 6. Execution Notes

- Use exact-path staging only; never `git add .`.
- Keep BLK-001 through BLK-006 fixed.
- Run hostile review before each commit because the package touches Codex dispatch, route evidence, and authority-adjacent tooling.
- If Codex upgrade breaks `workspace-write`, stop after BLK-SYSTEM-343 smoke evidence and report the setup blocker instead of silently downgrading to `danger-full-access`.
- If output-schema support behaves differently in the updated CLI, keep BLK-SYSTEM-345 as a follow-up compatibility sprint rather than forcing it into the route.
