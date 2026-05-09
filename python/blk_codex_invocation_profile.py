from __future__ import annotations

from pathlib import PurePosixPath
from typing import Any

PROFILE_ID = "codex_deterministic_invocation_profile"
ARTIFACT_ROOT = PurePosixPath("artifacts/codex")
MAX_ARTIFACT_PATH_LENGTH = 160
APPROVED_MODELS = frozenset({"gpt-5.4", "gpt-5.4-codex"})
REQUIRED_FLAGS = (
    "--ephemeral",
    "--ignore-user-config",
    "--ignore-rules",
    "--json",
    "--output-last-message",
)
DISABLED_AMBIENT_FEATURES = ("hooks", "plugins", "goals")
FORBIDDEN_EXTRA_FLAGS = frozenset(
    {
        "--dangerously-bypass-approvals-and-sandbox",
        "--enable",
        "--plugin",
        "--plugins",
        "--hook",
        "--hooks",
        "--goal",
        "--goals",
        "--config",
        "--mcp-server",
        "--server",
        "--browser",
        "--web-search",
    }
)
FORBIDDEN_AUTHORITY_KEYS = frozenset(
    {
        "profile_grants_execution_authority",
        "production_authority_granted",
        "production_sandbox_claimed",
        "network_model_cyber_tooling_authorized",
        "package_manager_authorized",
        "protected_body_read_authorized",
        "protected_body_copy_authorized",
        "active_vault_scan_authorized",
        "beo_publication_authorized",
        "rtm_generation_authorized",
        "drift_rejection_authorized",
        "source_mutation_authorized",
        "git_mutation_authorized",
        "blk_pipe_dispatch_authorized",
        "blk_test_mcp_authorized",
        "live_codex_execution_authorized",
    }
)
FORBIDDEN_STRING_MARKERS = tuple(
    marker.casefold()
    for marker in (
        "PRODUCTION_SANDBOX_ENFORCED",
        "PRODUCTION_SANDBOX_AUTHORITY",
        "NETWORK_FIREWALL_ENFORCED",
        "HOST_SECRET_ISOLATION_ENFORCED",
        "CODEX_LIVE_APPROVAL",
        "BLK_PIPE_EXECUTION_APPROVAL",
        "BLK_TEST_PASS grants execution authority",
        "BEO_PUBLICATION_APPROVAL",
        "RTM_GENERATION_APPROVAL",
        "DRIFT_REJECTION_AUTHORITY",
        "PROTECTED_BODY_READ_ALLOWED",
    )
)


def build_codex_deterministic_invocation_profile(
    *,
    approved_model: str,
    worktree: str,
    final_message_artifact: str,
    prompt: str,
    extra_flags: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Build a pure, non-executing Codex deterministic invocation profile fixture."""
    if approved_model not in APPROVED_MODELS:
        raise ValueError(f"approved_model is not in the allowed deterministic profile set: {approved_model!r}")
    if not isinstance(worktree, str) or not worktree.strip():
        raise ValueError("worktree must be a non-empty string")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt must be a non-empty bounded tactical packet string")
    _validate_extra_flags(extra_flags)
    artifact = _validate_artifact_path(final_message_artifact)

    argv = [
        "codex",
        "exec",
        "--model",
        approved_model,
        "-C",
        worktree,
        "-s",
        "danger-full-access",
        "-a",
        "never",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--disable",
        "hooks",
        "--disable",
        "plugins",
        "--disable",
        "goals",
        "--json",
        "--output-last-message",
        artifact,
    ]
    profile = {
        "profile_id": PROFILE_ID,
        "profile_status": "CODEX_DETERMINISTIC_INVOCATION_PROFILE_FIXTURE_ONLY",
        "argv": argv,
        "prompt": prompt,
        "model": approved_model,
        "worktree": worktree,
        "final_message_artifact": artifact,
        "required_flags": list(REQUIRED_FLAGS),
        "ambient_features": {feature: "disabled" for feature in DISABLED_AMBIENT_FEATURES},
        "sandbox_mode": "danger-full-access",
        "sandbox_authority": "CODEX_NATIVE_SANDBOX_NOT_TRUSTED_ON_THIS_HOST",
        "sandbox_workaround_scope": "local host workaround inside external BLK/Hermes containment only",
        "jsonl_events_authority": "CODEX_JSONL_EVENTS_ADVISORY_ONLY",
        "final_message_artifact_authority": "CODEX_FINAL_MESSAGE_ARTIFACT_ADVISORY_ONLY",
        "subprocess_started_by_profile_helper": False,
        "command_executed": False,
        "profile_grants_execution_authority": False,
        "production_authority_granted": False,
        "production_sandbox_claimed": False,
        "network_model_cyber_tooling_authorized": False,
        "package_manager_authorized": False,
        "protected_body_read_authorized": False,
        "protected_body_copy_authorized": False,
        "active_vault_scan_authorized": False,
        "beo_publication_authorized": False,
        "rtm_generation_authorized": False,
        "drift_rejection_authorized": False,
        "source_mutation_authorized": False,
        "git_mutation_authorized": False,
        "blk_pipe_dispatch_authorized": False,
        "blk_test_mcp_authorized": False,
        "live_codex_execution_authorized": False,
    }
    return validate_codex_deterministic_invocation_profile(profile)


def validate_codex_deterministic_invocation_profile(profile: dict[str, Any]) -> dict[str, Any]:
    """Validate the non-authorizing deterministic profile shape and return it unchanged."""
    if not isinstance(profile, dict):
        raise ValueError("profile must be a dictionary")
    argv = profile.get("argv")
    if not isinstance(argv, list) or argv[:2] != ["codex", "exec"]:
        raise ValueError("argv must start with codex exec")

    _require_argv_pair(argv, "--model")
    _require_argv_pair(argv, "-C")
    if _require_argv_pair(argv, "-s") != "danger-full-access":
        raise ValueError("-s must be danger-full-access as a documented local host workaround")
    if _require_argv_pair(argv, "-a") != "never":
        raise ValueError("-a must be never for deterministic non-interactive profile shape")
    for flag in REQUIRED_FLAGS[:-1]:
        if flag not in argv:
            raise ValueError(f"missing required flag {flag}")
    artifact = _require_argv_pair(argv, "--output-last-message")
    if profile.get("final_message_artifact", artifact) != artifact:
        raise ValueError("final_message_artifact must match --output-last-message")
    _validate_artifact_path(artifact)

    for feature in DISABLED_AMBIENT_FEATURES:
        if profile.get("ambient_features", {}).get(feature) != "disabled":
            raise ValueError(f"ambient feature {feature} must be disabled")
        if not _has_argv_pair(argv, "--disable", feature):
            raise ValueError(f"argv must include --disable {feature}")

    for item in argv:
        if item in FORBIDDEN_EXTRA_FLAGS:
            raise ValueError(f"forbidden Codex flag in deterministic profile: {item}")
    _scan_for_authority_laundering(profile)
    return profile


def _validate_extra_flags(extra_flags: list[str] | tuple[str, ...] | None) -> None:
    if extra_flags is None:
        return
    if len(extra_flags) != 0:
        raise ValueError(f"caller-supplied extra Codex flags are not allowed: {list(extra_flags)!r}")


def _validate_artifact_path(path: str) -> str:
    if not isinstance(path, str) or not path.strip():
        raise ValueError("artifact path must be a non-empty relative string")
    if len(path) > MAX_ARTIFACT_PATH_LENGTH:
        raise ValueError("artifact path exceeds deterministic profile length bound")
    posix_path = PurePosixPath(path)
    if posix_path.is_absolute():
        raise ValueError("artifact path must be relative")
    parts = posix_path.parts
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError("artifact path must not contain empty/current/parent traversal segments")
    if ".git" in parts:
        raise ValueError("artifact path must not target .git")
    if parts[:2] != ARTIFACT_ROOT.parts or len(parts) <= len(ARTIFACT_ROOT.parts):
        raise ValueError(f"artifact path must be under {ARTIFACT_ROOT}/")
    protected_prefixes = (
        PurePosixPath("docs/active"),
        PurePosixPath("docs/requirements"),
        PurePosixPath("docs/use_cases"),
    )
    for prefix in protected_prefixes:
        if parts[: len(prefix.parts)] == prefix.parts:
            raise ValueError("artifact path must not reference protected BLK-req paths")
    return posix_path.as_posix()


def _require_argv_pair(argv: list[Any], flag: str) -> str:
    try:
        index = argv.index(flag)
    except ValueError as exc:
        raise ValueError(f"missing required flag {flag}") from exc
    try:
        value = argv[index + 1]
    except IndexError as exc:
        raise ValueError(f"{flag} must have a value") from exc
    if not isinstance(value, str) or value == "":
        raise ValueError(f"{flag} must have a non-empty string value")
    return value


def _has_argv_pair(argv: list[Any], flag: str, value: str) -> bool:
    return any(left == flag and right == value for left, right in zip(argv, argv[1:]))


def _scan_for_authority_laundering(value: Any, path: str = "profile") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            if key_text in FORBIDDEN_AUTHORITY_KEYS and child is not False:
                raise ValueError(f"forbidden authority claim at {path}.{key_text}")
            if _looks_like_forbidden_authority_key(key_text) and child is not False:
                raise ValueError(f"forbidden authority-like field at {path}.{key_text}")
            _scan_for_authority_laundering(child, f"{path}.{key_text}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _scan_for_authority_laundering(child, f"{path}[{index}]")
    elif isinstance(value, str):
        lowered = value.casefold()
        for marker in FORBIDDEN_STRING_MARKERS:
            if marker in lowered:
                raise ValueError(f"forbidden authority wording at {path}")


def _looks_like_forbidden_authority_key(key: str) -> bool:
    lowered = key.casefold()
    authority_terms = (
        "protected_body",
        "active_vault",
        "beo_publication",
        "rtm_generation",
        "drift_rejection",
        "production_sandbox",
        "network_firewall",
        "host_secret_isolation",
        "live_codex",
        "blk_pipe_dispatch",
        "blk_test_mcp",
    )
    return any(term in lowered for term in authority_terms)
