"""Private bubblewrap/AppArmor setup helpers for Codex workspace-write.

BLK-SYSTEM-229 keeps the host-wide AppArmor userns restriction enabled and
routes Codex to a private copy of ``bwrap`` whose path has an explicit AppArmor
profile allowing user namespace setup. These helpers are deliberately
non-mutating: the privileged setup itself lives in ``scripts/setup-codex-private-bwrap.sh``.
"""

from __future__ import annotations

import os
import stat
from pathlib import Path
from typing import Iterable, Mapping

DEFAULT_INSTALL_DIR = Path("/opt/blk-system/codex-bwrap")
DEFAULT_PRIVATE_BWRAP_PATH = DEFAULT_INSTALL_DIR / "bwrap"
DEFAULT_PROFILE_NAME = "blk-codex-bwrap"
DEFAULT_PROFILE_PATH = Path("/etc/apparmor.d") / DEFAULT_PROFILE_NAME
REQUIRED_SYSCTL_VALUE = "1"


def apparmor_profile_text(private_bwrap_path: str | Path = DEFAULT_PRIVATE_BWRAP_PATH) -> str:
    """Return the AppArmor profile for the private Codex bubblewrap binary."""
    private_bwrap = Path(private_bwrap_path)
    if not private_bwrap.is_absolute():
        raise ValueError("private_bwrap_path must be absolute")
    return (
        "# Generated for BLK-SYSTEM-229: Codex private bwrap userns profile.\n"
        "# Keep kernel.apparmor_restrict_unprivileged_userns=1; do not relax it globally.\n"
        "abi <abi/4.0>,\n"
        "include <tunables/global>\n\n"
        f"profile {DEFAULT_PROFILE_NAME} {private_bwrap} flags=(unconfined) {{\n"
        "  userns,\n\n"
        f"  include if exists <local/{DEFAULT_PROFILE_NAME}>\n"
        "}\n"
    )


def build_codex_private_bwrap_env(
    base_env: Mapping[str, str] | None = None,
    *,
    private_bwrap_dir: str | Path = DEFAULT_INSTALL_DIR,
) -> dict[str, str]:
    """Return an environment that makes Codex resolve the private ``bwrap`` first."""
    env = dict(os.environ if base_env is None else base_env)
    private_dir = str(Path(private_bwrap_dir).expanduser().resolve())
    current_path = env.get("PATH", "")
    path_parts = [part for part in current_path.split(os.pathsep) if part]
    path_parts = [part for part in path_parts if Path(part).expanduser().resolve() != Path(private_dir)]
    env["PATH"] = os.pathsep.join([private_dir, *path_parts]) if path_parts else private_dir
    env["BLK_CODEX_PRIVATE_BWRAP_DIR"] = private_dir
    return env


def build_setup_summary() -> dict[str, object]:
    """Return operator-facing reconstruction commands for the BLK-229 setup."""
    return {
        "status": "DOCUMENTED_RECREATABLE_SETUP",
        "install_dir": str(DEFAULT_INSTALL_DIR),
        "private_bwrap_path": str(DEFAULT_PRIVATE_BWRAP_PATH),
        "profile_name": DEFAULT_PROFILE_NAME,
        "profile_path": str(DEFAULT_PROFILE_PATH),
        "required_sysctl": "kernel.apparmor_restrict_unprivileged_userns=1",
        "operator_rebuild_commands": [
            "cd /home/dad/BLK-System",
            "sudo scripts/setup-codex-private-bwrap.sh",
            f"sudo apparmor_parser -r {DEFAULT_PROFILE_PATH}",
            f"export BLK_CODEX_PRIVATE_BWRAP_DIR={DEFAULT_INSTALL_DIR}",
            "BLK_CODEX_PRIVATE_BWRAP_DIR=/opt/blk-system/codex-bwrap codex exec --sandbox workspace-write --model gpt-5.5 -c model_reasoning_effort='\"high\"' - < /tmp/blk-codex-smoke-prompt.txt",
        ],
        "forbidden_commands": [
            "sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0",
        ],
    }


def validate_private_bwrap_setup_descriptor(
    *,
    private_bwrap_path: str | Path = DEFAULT_PRIVATE_BWRAP_PATH,
    profile_names: Iterable[str] | None = None,
    apparmor_restrict_unprivileged_userns: str | int | None = REQUIRED_SYSCTL_VALUE,
) -> dict[str, object]:
    """Validate observable setup facts without mutating host policy."""
    path = Path(private_bwrap_path).expanduser()
    blockers: list[dict[str, object]] = []

    sysctl_value = "" if apparmor_restrict_unprivileged_userns is None else str(apparmor_restrict_unprivileged_userns).strip()
    if sysctl_value != REQUIRED_SYSCTL_VALUE:
        blockers.append(
            {
                "code": "HOSTWIDE_USERNS_RELAXED_OR_UNKNOWN",
                "message": "kernel.apparmor_restrict_unprivileged_userns must remain 1 for this route",
                "actual": sysctl_value,
                "expected": REQUIRED_SYSCTL_VALUE,
            }
        )

    if path == Path("/usr/bin/bwrap") or str(path) == "/bin/bwrap":
        blockers.append(
            {
                "code": "GLOBAL_BWRAP_PATH",
                "message": "Codex must use a private bwrap copy, not the global system bwrap path",
                "path": str(path),
            }
        )

    if path.exists() and path.is_symlink():
        blockers.append(
            {
                "code": "BWRAP_PATH_SYMLINK",
                "message": "private bwrap path must not be a symlink",
                "path": str(path),
            }
        )
    elif not path.exists():
        blockers.append(
            {
                "code": "BWRAP_PATH_MISSING",
                "message": "private bwrap binary is missing",
                "path": str(path),
            }
        )
    elif not path.is_file():
        blockers.append(
            {
                "code": "BWRAP_PATH_NOT_FILE",
                "message": "private bwrap path must be a regular file",
                "path": str(path),
            }
        )
    elif not _owner_executable(path):
        blockers.append(
            {
                "code": "BWRAP_PATH_NOT_EXECUTABLE",
                "message": "private bwrap path must be owner-executable",
                "path": str(path),
            }
        )

    profile_set = set(profile_names or [])
    if DEFAULT_PROFILE_NAME not in profile_set:
        blockers.append(
            {
                "code": "APPARMOR_PROFILE_NOT_LOADED",
                "message": f"loaded AppArmor profiles must include {DEFAULT_PROFILE_NAME}",
                "profile_name": DEFAULT_PROFILE_NAME,
            }
        )

    return {
        "status": "BLOCKED" if blockers else "READY",
        "private_bwrap_path": str(path),
        "profile_name": DEFAULT_PROFILE_NAME,
        "required_sysctl": "kernel.apparmor_restrict_unprivileged_userns=1",
        "blockers": blockers,
    }


def _owner_executable(path: Path) -> bool:
    return bool(path.stat().st_mode & stat.S_IXUSR)
