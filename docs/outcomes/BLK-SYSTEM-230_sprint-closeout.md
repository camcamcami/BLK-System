# BLK-SYSTEM-230 — Live Kuronode Agent A Header Drop Sprint Closeout

**Status:** Complete
**Date:** 2026-05-18T22:14:23+10:00
**BLK-System Commit:** this commit (`feat: execute Agent A header drop via BLK-pipe`)
**Kuronode Base Commit:** `133513b4db5371e629299b5581e05d96269ee52e`
**Kuronode Feature Commit:** `b7de262a51c85c4c6030b327cd490550f96f7491`

## 1. Objective

Execute the prepared BLK-SYSTEM-230 Agent A header feature through the governed BEB-L2 / BLK-pipe / Codex route now that BLK-SYSTEM-229 private-bwrap setup is available.

Feature slice: replace the empty spacer in the Agent A chat header with explicit copy:

- `Agent A Workspace`
- `Context-aware MBSE assistant`

## 2. Route and Evidence

- Source worktree used for validation dependencies: `/home/dad/code/Kuronode-v1`
- Sterile execution worktree: `/tmp/kuronode-blk230-agent-a-header`
- Target branch: `sprint/blk-system-230-agent-a-header`
- Target hash: `133513b4db5371e629299b5581e05d96269ee52e`
- Feature commit: `b7de262a51c85c4c6030b327cd490550f96f7491`
- Required dispatch environment:
  - `BLK_CODEX_PRIVATE_BWRAP_DIR=/opt/blk-system/codex-bwrap`
  - `PATH=/opt/blk-system/codex-bwrap:$PATH`
- Allowed modified files:
  - `packages/kuronode-graph/src/components/KuronodeAppShell.tsx`
  - `packages/kuronode-graph/src/components/KuronodeAppShell.test.tsx`
- Allowed new files: none
- Validation profile: `kuronode-worktree-static`

Evidence hashes:

- BEB: `/tmp/blk-system-230-artifacts/BEB_230.md` — `sha256:18eea3fc1c49c6f691cb08e2c7d890e825865ecc082b0e2cb2c3c18a2a571eba`
- L2 packet: `/tmp/blk-system-230-artifacts/L2_230.md` — `sha256:c39bc7d35b32fa71adfff8b3a3e3f4306cfe68e7c014fbb4e97ce024e61d48dd`
- Approved clean drop manifest: `/tmp/blk-system-230-artifacts/drop-clean-BEB_230.json` — `sha256:db36104598bc2b9d49fa3beb28cad0d2296acc650b251ca85bcd5a196514cc0c`
- Preflight report: `/tmp/blk-system-230-artifacts/preflight-clean.json` — `sha256:0b2017c320542b802ba938d20929c28486b106b50c469c90c493c99565089e01`
- Successful dispatch report: `/tmp/blk-system-230-artifacts/dispatch-report-success.json` — `sha256:cb810a5e08932175e07e869792d860ef35bad3a2f3c8a0652fae6b32754c38a1`
- Kuronode patch: `/tmp/blk-system-230-artifacts/kuronode-blk230.patch` — `sha256:a702f8ef15543b28a100cbfc0b71a26f306821b5de80c0ac056f92f4f0c01ca4`
- Kuronode MCP closeout: `/tmp/blk-system-230-artifacts/mcp-closeout.json` — `sha256:c83f7064d86b13037d2547e78320ce575836beb50596216ec12724593f15fc9a`
- External Codex final message: `/tmp/blk-system-beb-l2-codex/BEB_230/133513b4db53/final-message.md` — `sha256:7b328893a261ddad3b7391a1a0aa6f56cb64a44b388ad06b82c7a6d6f71109e3`

Aggregate BLK-230 evidence hash:

```text
sha256:82c8cbfa501a1f113a5262e71f6b210c42b017884e4754b073b02f55af4ba6d1
```

Provenance command:

```bash
printf '%s  %s\n' \
  18eea3fc1c49c6f691cb08e2c7d890e825865ecc082b0e2cb2c3c18a2a571eba BEB_230.md \
  c39bc7d35b32fa71adfff8b3a3e3f4306cfe68e7c014fbb4e97ce024e61d48dd L2_230.md \
  db36104598bc2b9d49fa3beb28cad0d2296acc650b251ca85bcd5a196514cc0c drop-clean-BEB_230.json \
  0b2017c320542b802ba938d20929c28486b106b50c469c90c493c99565089e01 preflight-clean.json \
  cb810a5e08932175e07e869792d860ef35bad3a2f3c8a0652fae6b32754c38a1 dispatch-report-success.json \
  a702f8ef15543b28a100cbfc0b71a26f306821b5de80c0ac056f92f4f0c01ca4 kuronode-blk230.patch \
  c83f7064d86b13037d2547e78320ce575836beb50596216ec12724593f15fc9a mcp-closeout.json \
  7b328893a261ddad3b7391a1a0aa6f56cb64a44b388ad06b82c7a6d6f71109e3 final-message.md | sha256sum
```

## 3. Implementation Summary

Codex, invoked through the approved BEB-L2 / BLK-pipe route with private-bwrap `workspace-write`, changed only the two allowed Kuronode files:

- Added a focused Vitest assertion that `Agent A Workspace` and `Context-aware MBSE assistant` render in `KuronodeAppShell`.
- Replaced the empty header spacer beside the Agent A sparkle icon with the two user-facing labels.

The first live retry exposed a BLK-pipe cleanup edge: Codex can create empty ambient metadata directories such as `.agents/` or `.codex/` that are not target source changes but still appear as physical residue. BLK-System now scrubs those exact empty ambient directories after a successful engine run and before physical-residue enforcement. Non-empty ambient directories remain unauthorized and fail closed.

## 4. Verification

RED/GREEN evidence:

- Focused Kuronode RED gate: a string assertion script failed before dispatch because `Agent A Workspace` and `Context-aware MBSE assistant` were absent.
- Initial BLK-pipe/Codex retry after private-bwrap setup failed closed as `UNAUTHORIZED_FILE_MUTATION` due only to empty `.agents/` / `.codex/` ambient metadata directories; no source diff was accepted.
- Go RED/GREEN hardening: `TestRunSuccessScrubsEmptyCodexAmbientMetadataDirs` and `TestRunRejectsNonEmptyCodexAmbientMetadataDirs` now cover the cleanup boundary.
- Successful dispatch report status: `SUCCESS`; committed files exactly match the allowlist; destroyed files empty.

Kuronode validation:

- Targeted Vitest: `npm run test -w @kuronode/kuronode-graph -- KuronodeAppShell.test.tsx` — 1 file passed, 4 tests passed.
- Full graph package Vitest: `npm run test -w @kuronode/kuronode-graph` — 16 files passed, 57 tests passed.
- Graph package build: `npm run build -w @kuronode/kuronode-graph` — passed with existing bundle-size warnings only.
- Validation used existing installed dependencies via temporary symlinks into the sterile worktree and did not run package-manager install commands.
- Post-validation sterile worktree status was clean after removing ignored build output.

Kuronode MCP closeout:

- `sysml_task_closeout_review` returned strict `PASS` with `closeoutComplete: true`.
- Traceability: `R-AIC-045`, `R-UIX-169`, and `UC-VIS-003`.
- No new requirements or use cases were surfaced.

BLK-System verification:

- `go test ./internal/pipe -run 'TestRun(SuccessScrubsEmptyCodexAmbientMetadataDirs|RejectsNonEmptyCodexAmbientMetadataDirs)' -count=1` — passed.
- `go test ./internal/pipe -count=1` — passed.
- `go build -o /tmp/blk-pipe ./cmd/blk-pipe` and `/tmp/blk-pipe --health` — passed.

## 5. Hostile Review / Risk Check

Local hostile review found and remediated one blocker before closeout: empty Codex ambient metadata directories caused successful source-bounded runs to be reported as unauthorized physical residue. The remediation is intentionally narrow:

- It removes only `.agents/` and `.codex/` when they exist as empty directories.
- It does not remove files, non-empty directories, symlinks, or arbitrary ignored residue.
- It runs only after a successful engine exit; engine failure, timeout, and output-flood paths still use failure cleanup and fail closed.
- It preserves the target file allowlist and physical-residue enforcement.

Authority review findings:

- The BEB/L2/drop manifest was hash-bound and approved before dispatch.
- The target worktree and target hash were pinned before dispatch.
- The diff is non-empty and restricted to exactly the two allowed Kuronode files.
- The private-bwrap path was exactly `/opt/blk-system/codex-bwrap` and descriptor-ready before dispatch.
- No package-manager install/update command was run in the sterile worktree.
- No Hermes-direct Kuronode source edit was used.
- No protected-body, RTM, BEO publication, production BLK-test MCP, reusable Codex dispatch, broad BLK-pipe runtime, or production-isolation authority was introduced.

## 6. Authority Boundary

BLK-SYSTEM-230 authorizes only the exact completed BEB-L2 / BLK-pipe / Codex run recorded here. It does not grant broad BLK-pipe runtime, reusable live Codex dispatch, Hermes-direct Kuronode mutation, broad source/Git mutation, protected-body migration/access, RTM generation, BEO closeout/publication, production BLK-test MCP, package-manager/network/model/browser/cyber tooling, future runs without fresh exact manifest approval, or production-isolation claims.

The private-bwrap setup keeps `kernel.apparmor_restrict_unprivileged_userns=1` and avoids the prior host-wide sysctl relaxation, but it remains a host setup route for exact Codex `workspace-write` dispatches, not a reusable production isolation proof.

## 7. Documentation Burden Check

No new root `BLK-###` document was created. BLK-077 and BLK-079 were updated only for active current-state/frontier movement. This is the single sprint outcome document for BLK-SYSTEM-230; the earlier `BLK-SYSTEM-230_blocked-attempt.md` remains a historical failed-attempt record, not a second sprint closeout.
