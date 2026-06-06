# Native private-bwrap AppArmor setup

**Sprint:** BLK-SYSTEM-229
**Purpose:** recreate the host setup that lets Codex use `--sandbox workspace-write` while keeping Ubuntu's host-wide unprivileged-userns restriction enabled.

## Authority boundary

This is an environment setup runbook, not blanket execution authority. It only installs a private copy of `bwrap` at `/opt/blk-system/codex-bwrap/bwrap` and loads an AppArmor profile for that exact path. BEB-L2 drops must still go through the BLK-222/BLK-229 route, approved manifest hashes, trusted workdirs, exact target hashes, and BLK-pipe allowlists.

**No host-wide AppArmor userns relaxation:** do not run `sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0` for the persistent route.

## Recreate setup on a new BLK-System host

From the BLK-System repository root:

```bash
cd /home/dad/BLK-System
sudo scripts/setup-codex-private-bwrap.sh
export BLK_CODEX_PRIVATE_BWRAP_DIR=/opt/blk-system/codex-bwrap
export PATH="$BLK_CODEX_PRIVATE_BWRAP_DIR:$PATH"
```

Expected persistent host policy:

```bash
sysctl kernel.apparmor_restrict_unprivileged_userns
# kernel.apparmor_restrict_unprivileged_userns = 1
```

Expected AppArmor profile file:

```bash
sudo apparmor_parser -r /etc/apparmor.d/blk-codex-bwrap
```

The generated profile is intentionally narrow:

```apparmor
profile blk-codex-bwrap /opt/blk-system/codex-bwrap/bwrap flags=(unconfined) {
  userns,
}
```

## Smoke test

Use a disposable worktree; never smoke-test by editing Kuronode directly.

```bash
TMP=$(mktemp -d)
cd "$TMP"
git init -b smoke
git config user.name smoke
git config user.email smoke@example.invalid
printf 'before\n' > README.md
git add README.md
git commit -m initial
printf 'Append the word smoke to README.md and do nothing else.\n' >/tmp/blk-codex-smoke-prompt.txt
BLK_CODEX_PRIVATE_BWRAP_DIR=/opt/blk-system/codex-bwrap \
PATH="/opt/blk-system/codex-bwrap:$PATH" \
codex exec --sandbox workspace-write --model gpt-5.5 -c model_reasoning_effort='"xhigh"' - < /tmp/blk-codex-smoke-prompt.txt
git diff -- README.md
```

A successful smoke shows Codex can run shell tools under `--sandbox workspace-write`. If it fails with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted` or `uid_map`, the private `bwrap` path is not first in `PATH`, the AppArmor profile is not loaded, or the host policy changed.

## BLK-pipe/Codex route usage

For BEB-L2 dispatch, export the private path before running the Python route or any helper that invokes `blk-pipe`:

```bash
export BLK_CODEX_PRIVATE_BWRAP_DIR=/opt/blk-system/codex-bwrap
export PATH="$BLK_CODEX_PRIVATE_BWRAP_DIR:$PATH"
PYTHONPATH=python python python/beb_l2_blk_pipe_route.py \
  --drop /absolute/path/to/drop.json \
  --allowed-work-dir /absolute/path/to/kuronode-clean-worktree \
  --trusted-root /absolute/trusted/root \
  --approved-drop-sha256 sha256:<approved-drop-manifest-hash>
```

`python/blk_pipe_adapter.py` propagates `BLK_CODEX_PRIVATE_BWRAP_DIR` into the `blk-pipe` process environment only when it resolves to the trusted `/opt/blk-system/codex-bwrap` install dir, and prepends that directory to `PATH`, so Codex resolves the private `bwrap` when BLK-System injects `--sandbox workspace-write`.

## Verification checklist

- `kernel.apparmor_restrict_unprivileged_userns = 1`
- `/opt/blk-system/codex-bwrap/bwrap` exists, is executable, and is not a symlink
- `/sys/kernel/security/apparmor/profiles` or `aa-status` shows `blk-codex-bwrap`
- `BLK_CODEX_PRIVATE_BWRAP_DIR=/opt/blk-system/codex-bwrap`
- `PATH` starts with `/opt/blk-system/codex-bwrap`
- Codex smoke uses `codex --model gpt-5.5`, `model_reasoning_effort='"xhigh"'`, and `--sandbox workspace-write`
- BEB-L2 dispatch still uses exact approved drop manifest hashes and BLK-pipe allowlists

## Rollback

```bash
sudo apparmor_parser -R /etc/apparmor.d/blk-codex-bwrap || true
sudo rm -f /etc/apparmor.d/blk-codex-bwrap
sudo rm -rf /opt/blk-system/codex-bwrap
unset BLK_CODEX_PRIVATE_BWRAP_DIR
```

Rollback removes the private route. It does not change the host-wide AppArmor userns sysctl.
