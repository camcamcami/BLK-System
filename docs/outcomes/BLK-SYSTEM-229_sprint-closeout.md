# BLK-SYSTEM-229 — Private bwrap AppArmor Setup Sprint Closeout

**Status:** Complete for BLK-System code/runbook; privileged host install still operator-run
**Date:** 2026-05-18T20:14:49+10:00
**BLK-System Commit:** this commit (`feat: add Codex private-bwrap workspace-write setup`)
**Aggregate BLK-229 package hash:** `sha256:1cadd6e9f379bb814f86a50e22cd1e351b8961bbfb7e3c6778ca771075d5722f`

## 1. Objective

Make the native Codex `workspace-write` route reproducible without permanently relaxing the host-wide AppArmor userns sysctl. Document the setup so BLK-System can be rebuilt on this host or a new host.

## 2. Implementation Summary

BLK-SYSTEM-229 added:

- `python/codex_private_bwrap_setup.py` — non-mutating setup descriptor, AppArmor profile text, setup-summary evidence, and private-bwrap environment builder.
- `scripts/setup-codex-private-bwrap.sh` — root-run setup script that copies `/usr/bin/bwrap` to `/opt/blk-system/codex-bwrap/bwrap`, writes `/etc/apparmor.d/blk-codex-bwrap`, loads it with `apparmor_parser -r`, and refuses to run unless `kernel.apparmor_restrict_unprivileged_userns=1`.
- `docs/runbooks/codex-private-bwrap-apparmor.md` — rebuild/runbook instructions, smoke-test recipe, BLK-pipe route environment, verification checklist, and rollback.
- `python/blk_pipe_adapter.py` — propagates `BLK_CODEX_PRIVATE_BWRAP_DIR` and prepends it to `PATH` for `blk-pipe` subprocesses.
- `python/beb_l2_blk_pipe_route.py` — injects Codex `--sandbox workspace-write` for Kuronode BEB-L2 drops instead of the BLK-228 `danger-full-access` fallback.

## 3. Evidence

Package-hash provenance:

```text
886d1d478617ef8e1faf13751f10827f5c22b56770a17fa408c3821c2a525ec7  python/codex_private_bwrap_setup.py
5d7558c46c654e7d9d15cf3bdc81c2e71868787155c913b69f6355866466527e  python/test_codex_private_bwrap_setup_229.py
805e9d666ee336790436a5af6d308d9ebdba553b215a1cf6e1a0364dc1c36c04  python/blk_pipe_adapter.py
a9ed69da2d8b07bdba17242973ee04e8290b1ac0e6ecbc4feaf7822b5bab96fa  python/beb_l2_blk_pipe_route.py
13f4f5a35072e0930ed2af301919375ab73d7700400286f7c9404e96057619b2  python/test_beb_l2_blk_pipe_route.py
5b0c18d8fdbb8b36537759b9bac1fad8fa652a56a66d9e466a54e32f34927182  scripts/setup-codex-private-bwrap.sh
33ece1d462d5205fc9480030b0e9245de1ccf744d3e2d1d3c1e01ec8416de4d5  docs/runbooks/codex-private-bwrap-apparmor.md
```

Aggregate command:

```bash
sha256sum \
  python/codex_private_bwrap_setup.py \
  python/test_codex_private_bwrap_setup_229.py \
  python/blk_pipe_adapter.py \
  python/beb_l2_blk_pipe_route.py \
  python/test_beb_l2_blk_pipe_route.py \
  scripts/setup-codex-private-bwrap.sh \
  docs/runbooks/codex-private-bwrap-apparmor.md | sha256sum
```

## 4. Verification

- RED: `PYTHONPATH=python python -m unittest python/test_codex_private_bwrap_setup_229.py` initially failed because `codex_private_bwrap_setup` did not exist.
- GREEN focused: `PYTHONPATH=python python -m unittest python/test_codex_private_bwrap_setup_229.py python/test_beb_l2_blk_pipe_route.py` — 26 tests passed.
- Current-state focused: `PYTHONPATH=python python -m unittest python/test_codex_private_bwrap_setup_229.py python/test_beb_l2_blk_pipe_route.py python/test_blk_current_state_authority_index.py` — 44 tests passed.
- Full Python: `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache PYTHONPATH=python python -m unittest discover -s python -p 'test*.py'` — 1405 tests passed, 35 skipped.
- Go: `go test ./...` — passed.
- Script syntax: `bash -n scripts/setup-codex-private-bwrap.sh` — passed.
- Setup descriptor on current host returned `BLOCKED` because `/opt/blk-system/codex-bwrap/bwrap` is missing and `blk-codex-bwrap` is not loaded.
- Attempted `sudo -n scripts/setup-codex-private-bwrap.sh` proved Hermes cannot perform the privileged install in this session (`sudo: a password is required`).

## 5. Hostile Review / Risk Check

- The setup script refuses a host-wide relaxed sysctl and does not run `kernel.apparmor_restrict_unprivileged_userns=0`.
- The profile target is the exact private path `/opt/blk-system/codex-bwrap/bwrap`; tests reject `/usr/bin/bwrap`, symlinked private paths, and missing private paths.
- The adapter only prepends the private bwrap directory when `BLK_CODEX_PRIVATE_BWRAP_DIR` resolves to `/opt/blk-system/codex-bwrap`; hostile review added a regression that rejects untrusted environment path injection.
- `workspace-write` still relies on Codex/bwrap/AppArmor host behavior. This is not a production-isolation, VM, cgroup, firewall, or host-secret-isolation proof.

## 6. Operator Rebuild Command

```bash
cd /home/dad/BLK-System
sudo scripts/setup-codex-private-bwrap.sh
export BLK_CODEX_PRIVATE_BWRAP_DIR=/opt/blk-system/codex-bwrap
export PATH="$BLK_CODEX_PRIVATE_BWRAP_DIR:$PATH"
```

## 7. Authority Boundary

BLK-SYSTEM-229 provides a recreatable environment setup and routes future exact BEB-L2/Codex payloads to `workspace-write`. It does not grant broad BLK-pipe runtime, reusable live Codex dispatch, Hermes-direct Kuronode mutation, package-manager/network/model/browser/cyber tooling, protected-body access, RTM generation, BEO publication, production BLK-test MCP, target/source/Git mutation outside exact approved payloads, or production-isolation authority.
