#!/usr/bin/env bash
# BLK-SYSTEM-229: install/recreate the private Codex bubblewrap AppArmor setup.
#
# This script intentionally keeps kernel.apparmor_restrict_unprivileged_userns=1.
# It installs a private copy of bwrap and loads an AppArmor profile for that
# exact path only, so Codex workspace-write can use bubblewrap without relaxing
# host-wide user namespace policy.

set -euo pipefail

INSTALL_DIR="${1:-${BLK_CODEX_PRIVATE_BWRAP_DIR:-/opt/blk-system/codex-bwrap}}"
PROFILE_NAME="blk-codex-bwrap"
PROFILE_PATH="/etc/apparmor.d/${PROFILE_NAME}"
PRIVATE_BWRAP="${INSTALL_DIR%/}/bwrap"

if [[ "${EUID}" -ne 0 ]]; then
  echo "error: run with sudo, e.g. sudo scripts/setup-codex-private-bwrap.sh" >&2
  exit 1
fi

if [[ "${INSTALL_DIR}" != /opt/blk-system/codex-bwrap ]]; then
  echo "error: INSTALL_DIR must remain /opt/blk-system/codex-bwrap for the audited BLK-229 route" >&2
  exit 2
fi

BWRAP_SRC="$(command -v bwrap || true)"
if [[ -z "${BWRAP_SRC}" || ! -x "${BWRAP_SRC}" ]]; then
  echo "error: bwrap is not installed or not executable" >&2
  exit 3
fi

if [[ "${BWRAP_SRC}" == "${PRIVATE_BWRAP}" ]]; then
  echo "error: source bwrap unexpectedly resolves to the private destination" >&2
  exit 4
fi

SYSCTL_VALUE="$(sysctl -n kernel.apparmor_restrict_unprivileged_userns 2>/dev/null || true)"
if [[ "${SYSCTL_VALUE}" != "1" ]]; then
  echo "error: kernel.apparmor_restrict_unprivileged_userns must be 1; refusing host-wide relaxed state (${SYSCTL_VALUE:-unknown})" >&2
  exit 5
fi

install -d -m 0755 "${INSTALL_DIR}"
install -m 0755 "${BWRAP_SRC}" "${PRIVATE_BWRAP}"

cat > "${PROFILE_PATH}" <<EOF_PROFILE
# Generated for BLK-SYSTEM-229: Codex private bwrap userns profile.
# Keep kernel.apparmor_restrict_unprivileged_userns=1; do not relax it globally.
abi <abi/4.0>,
include <tunables/global>

profile blk-codex-bwrap ${PRIVATE_BWRAP} flags=(unconfined) {
  userns,

  include if exists <local/blk-codex-bwrap>
}
EOF_PROFILE

apparmor_parser -r "${PROFILE_PATH}"

cat <<EOF_DONE
BLK-SYSTEM-229 private bwrap setup ready.
private_bwrap=${PRIVATE_BWRAP}
profile=${PROFILE_NAME}
profile_path=${PROFILE_PATH}
sysctl kernel.apparmor_restrict_unprivileged_userns=${SYSCTL_VALUE}

Use this environment for BLK-pipe/Codex workspace-write runs:
export BLK_CODEX_PRIVATE_BWRAP_DIR=${INSTALL_DIR}
export PATH=${INSTALL_DIR}:\$PATH
EOF_DONE
