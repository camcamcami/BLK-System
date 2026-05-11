from copy import deepcopy
import re

PROFILE_ID = "blk-058-kuronode-typescript-mechanical-enforcement"
PROFILE_STATUS = "BLK_058_MECHANICAL_ENFORCEMENT_L0_L1_FIXTURE_ONLY"
PASS = "BLK_058_MECHANICAL_ENFORCEMENT_PASS_FIXTURE_ONLY"
BLOCKED = "BLK_058_MECHANICAL_ENFORCEMENT_BLOCKED_FIXTURE_ONLY"

MECHANICAL_RULE_IDS = (
    "no_recursion",
    "bounded_iteration",
    "bounded_runtime_state",
    "explicit_lifecycle_cleanup",
    "small_reviewable_units",
    "boundary_validation",
    "checked_results",
    "minimal_mutable_scope",
    "no_dynamic_execution",
    "flat_validated_data_access",
    "zero_warning_repository_profiles",
    "no_authority_laundering",
)

DENIED_AUTHORITIES = (
    "NO_BLK_058_MECHANICAL_PASS_RUNTIME_AUTHORITY",
    "NO_TARGET_REPO_SCAN_AUTHORITY",
    "NO_TARGET_REPO_MUTATION_AUTHORITY",
    "NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_AUTHORITY",
    "NO_LIVE_CODEX_EXECUTION_AUTHORITY",
    "NO_BLK_PIPE_EXECUTION_AUTHORITY",
    "NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY",
    "NO_BEO_PUBLICATION_AUTHORITY",
    "NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY",
    "NO_PROTECTED_BLK_REQ_BODY_READS",
    "NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY",
    "NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM",
)

SIDE_EFFECT_FLAGS = (
    "mechanical_pass_runtime_authority_granted",
    "target_repo_scan_authorized",
    "target_repo_mutation_authorized",
    "beb_dispatch_authorized",
    "beo_closeout_execution_authorized",
    "live_codex_execution_authorized",
    "blk_pipe_execution_authorized",
    "production_blk_test_mcp_authorized",
    "beo_publication_authorized",
    "rtm_generation_authorized",
    "protected_body_reads_authorized",
    "package_network_model_browser_cyber_tooling_authorized",
    "production_isolation_claimed",
)

PROFILE_KEYS = {
    "profile_id",
    "profile_status",
    "source_doc",
    "architecture_doc",
    "registry_doc",
    "governance_doc",
    "target_profile_id",
    "mechanical_rules",
    "validation_profiles",
    "denied_authorities",
    "authority_cutline",
    *SIDE_EFFECT_FLAGS,
}

RULE_KEYS = {"id", "source_rule", "summary", "mechanical_gate", "maturity"}
CANDIDATE_KEYS = {"snippet_id", "source_text", "metadata"}

COMMAND_MARKERS = (
    " ",
    "/",
    "\\",
    "http:",
    "https:",
    "&&",
    "||",
    ";",
    "`",
    "$(",
)

FORBIDDEN_NORMALIZED_MARKERS = (
    "approvedforliveexecution",
    "approvedforruntimeexecution",
    "runtimeexecutionauthorized",
    "mechanicalpassgrantsruntimeauthority",
    "targetreposcanauthorized",
    "targetrepomutationauthorized",
    "targetrepopath",
    "targetrepositorypath",
    "targetsourcepath",
    "targetgitpath",
    "bebdispatchauthorized",
    "beocloseoutexecutionauthorized",
    "livecodexexecutionauthorized",
    "blkpipeexecutionauthorized",
    "productionblktestmcpisauthorized",
    "beopublicationauthorized",
    "authoritativebeopublication",
    "publishbeo",
    "rtmgeneration",
    "rtmdriftrejectionauthorized",
    "protectedblkreqbodyreadsauthorized",
    "protectedblkreqbodyreadsareauthorized",
    "protectedblkreqbodypath",
    "protectedbodyreadsauthorized",
    "protectedbodypath",
    "docsactive",
    "npmrun",
    "npminstall",
    "pnpminstall",
    "yarninstall",
    "pipinstall",
    "goget",
    "packagemanagertoolingisauthorized",
    "packagemanagerauthorized",
    "networktoolingauthorized",
    "modelservicetoolingauthorized",
    "browsertoolingauthorized",
    "cybertoolingauthorized",
    "productionsandboxisenforced",
    "productionsandboxenforced",
    "hostisolationclaimed",
)

FORBIDDEN_RAW_MARKERS = (
    "npm install",
    "npm run",
    "pnpm install",
    "yarn install",
    "curl ",
    "wget ",
    "ssh ",
    "pip install",
    "go get ",
    "docs/active",
    "protected blk-req body",
)

MECHANICAL_RULES = (
    {
        "id": "no_recursion",
        "source_rule": "BLK-058 Rule 1",
        "summary": "Submitted tactical snippets must not use recursion unless a future authority envelope grants a bounded exception.",
        "mechanical_gate": "reject direct self-calls in function declarations",
        "maturity": "L1_SUBMITTED_SNIPPET_FIXTURE_ONLY",
    },
    {
        "id": "bounded_iteration",
        "source_rule": "BLK-058 Rule 2",
        "summary": "Loops require visible bounds; obvious infinite loops fail closed.",
        "mechanical_gate": "reject while true and for-empty infinite loops",
        "maturity": "L1_SUBMITTED_SNIPPET_FIXTURE_ONLY",
    },
    {
        "id": "bounded_runtime_state",
        "source_rule": "BLK-058 Rule 3",
        "summary": "Runtime collections and state must remain visibly bounded in snippets submitted to this fixture.",
        "mechanical_gate": "require explicit max/limit/cap vocabulary for accepted loop-heavy snippets",
        "maturity": "L1_SUBMITTED_SNIPPET_FIXTURE_ONLY",
    },
    {
        "id": "explicit_lifecycle_cleanup",
        "source_rule": "BLK-058 Rule 3 / lifecycle overlay",
        "summary": "Lifecycle-sensitive snippets must show cleanup intent where they create listeners, timers, workers, or parser resources.",
        "mechanical_gate": "reject obvious resource creation without cleanup vocabulary",
        "maturity": "L1_SUBMITTED_SNIPPET_FIXTURE_ONLY",
    },
    {
        "id": "small_reviewable_units",
        "source_rule": "BLK-058 Rule 4",
        "summary": "Submitted snippets must stay small enough for hostile review.",
        "mechanical_gate": "reject snippets with oversized function bodies",
        "maturity": "L1_SUBMITTED_SNIPPET_FIXTURE_ONLY",
    },
    {
        "id": "boundary_validation",
        "source_rule": "BLK-058 Rule 5",
        "summary": "External and boundary data must be validated before authority-sensitive use.",
        "mechanical_gate": "recorded as required review rule in this fixture profile",
        "maturity": "L1_PROFILE_RULE_ONLY",
    },
    {
        "id": "checked_results",
        "source_rule": "BLK-058 Rule 7",
        "summary": "Meaningful results and postconditions must not be ignored.",
        "mechanical_gate": "recorded as required review rule in this fixture profile",
        "maturity": "L1_PROFILE_RULE_ONLY",
    },
    {
        "id": "minimal_mutable_scope",
        "source_rule": "BLK-058 Rule 6",
        "summary": "Mutable state should be narrow and local.",
        "mechanical_gate": "recorded as required review rule in this fixture profile",
        "maturity": "L1_PROFILE_RULE_ONLY",
    },
    {
        "id": "no_dynamic_execution",
        "source_rule": "BLK-058 Rule 8",
        "summary": "Dynamic executable strings and reflection-like execution fail closed.",
        "mechanical_gate": "reject eval, Function constructors, string timers, and dynamic import",
        "maturity": "L1_SUBMITTED_SNIPPET_FIXTURE_ONLY",
    },
    {
        "id": "flat_validated_data_access",
        "source_rule": "BLK-058 Rule 9",
        "summary": "Nested structures must be normalized or validated before authority-sensitive use.",
        "mechanical_gate": "recorded as required review rule in this fixture profile",
        "maturity": "L1_PROFILE_RULE_ONLY",
    },
    {
        "id": "zero_warning_repository_profiles",
        "source_rule": "BLK-058 Rule 10",
        "summary": "Zero-warning intent is enforced through repository-owned validation profile names only.",
        "mechanical_gate": "reject command-shaped validation profile metadata",
        "maturity": "L1_PROFILE_RULE_ONLY",
    },
    {
        "id": "no_authority_laundering",
        "source_rule": "BLK-058 / BLK-078 / BLK-081 authority overlay",
        "summary": "Mechanical PASS remains quality evidence only and never grants adjacent runtime frontiers.",
        "mechanical_gate": "reject denied authority wording, protected paths, and tooling strings recursively",
        "maturity": "L1_SUBMITTED_SNIPPET_FIXTURE_ONLY",
    },
)


def build_blk058_mechanical_enforcement_profile():
    profile = {
        "profile_id": PROFILE_ID,
        "profile_status": PROFILE_STATUS,
        "source_doc": "BLK-058",
        "architecture_doc": "BLK-078",
        "registry_doc": "BLK-080",
        "governance_doc": "BLK-081",
        "target_profile_id": "kuronode-typescript",
        "mechanical_rules": deepcopy(list(MECHANICAL_RULES)),
        "validation_profiles": [
            "kuronode-power-of-ten-static",
            "kuronode-typecheck-strict",
            "kuronode-eslint-zero-warning",
        ],
        "denied_authorities": list(DENIED_AUTHORITIES),
        "authority_cutline": "BLK-058 mechanical enforcement is submitted-snippet fixture evidence only; it grants no target scan, target mutation, BEB dispatch, BEO closeout, Codex, BLK-pipe, BLK-test, BEO publication, RTM, protected-body, tooling, or sandbox authority.",
    }
    for flag in SIDE_EFFECT_FLAGS:
        profile[flag] = False
    return profile


def validate_blk058_mechanical_enforcement_profile(profile):
    errors = []
    if not isinstance(profile, dict):
        return ["profile must be a dictionary"]
    _validate_closed_schema(profile, PROFILE_KEYS, "profile", errors)
    expected = {
        "profile_id": PROFILE_ID,
        "profile_status": PROFILE_STATUS,
        "source_doc": "BLK-058",
        "architecture_doc": "BLK-078",
        "registry_doc": "BLK-080",
        "governance_doc": "BLK-081",
        "target_profile_id": "kuronode-typescript",
    }
    for key, value in expected.items():
        if profile.get(key) != value:
            errors.append(f"{key} must be {value!r}")
    _validate_mechanical_rules(profile.get("mechanical_rules"), errors)
    _validate_profile_names(profile.get("validation_profiles"), "validation_profiles", errors)
    _validate_denied_authorities(profile.get("denied_authorities"), "denied_authorities", errors)
    _validate_side_effect_flags(profile, errors)
    _scan_for_laundering(profile, "profile", errors)
    return errors


def evaluate_blk058_candidate_snippet(candidate, profile=None):
    active_profile = build_blk058_mechanical_enforcement_profile() if profile is None else profile
    violations = [
        _violation("mechanical_profile", error)
        for error in validate_blk058_mechanical_enforcement_profile(active_profile)
    ]
    if not isinstance(candidate, dict):
        result = {"snippet_id": None, "violations": violations + [_violation("candidate_schema", "candidate must be a dictionary")]}
        return _finish_result(result)

    _validate_closed_schema(candidate, CANDIDATE_KEYS, "candidate", violations, as_violation=True)
    snippet_id = candidate.get("snippet_id")
    source_text = candidate.get("source_text")
    metadata = candidate.get("metadata")
    if not isinstance(snippet_id, str) or not snippet_id:
        violations.append(_violation("candidate_schema", "snippet_id must be a non-empty string"))
    if not isinstance(source_text, str) or not source_text.strip():
        violations.append(_violation("candidate_schema", "source_text must be a non-empty string"))
        source_text = ""
    if metadata is not None and not isinstance(metadata, dict):
        violations.append(_violation("candidate_schema", "metadata must be a dictionary when present"))

    violations.extend(_evaluate_source_text(source_text))
    violations.extend(_scan_for_laundering(candidate, "candidate", [], as_violation=True))
    result = {"snippet_id": snippet_id, "violations": violations}
    return _finish_result(result)


def _evaluate_source_text(source_text):
    violations = []
    violations.extend(_detect_direct_recursion(source_text))
    if re.search(r"while\s*\(\s*true\s*\)", source_text) or re.search(r"for\s*\(\s*;\s*;\s*\)", source_text):
        violations.append(_violation("bounded_iteration", "obvious unbounded loop rejected"))
    if re.search(r"\bwhile\s*\(", source_text) and not re.search(r"\b(limit|max|cap|bound|count)\b", source_text, re.I):
        violations.append(_violation("bounded_iteration", "while loop lacks visible bound vocabulary"))
    if re.search(r"\b(eval|Function)\s*\(", source_text) or "new Function" in source_text:
        violations.append(_violation("no_dynamic_execution", "dynamic execution primitive rejected"))
    if re.search(r"set(?:Timeout|Interval)\s*\(\s*['\"]", source_text):
        violations.append(_violation("no_dynamic_execution", "string timer rejected"))
    if re.search(r"\bimport\s*\(", source_text):
        violations.append(_violation("no_dynamic_execution", "dynamic import rejected"))
    if len(source_text.splitlines()) > 80:
        violations.append(_violation("small_reviewable_units", "submitted snippet exceeds fixture line budget"))
    resource_created = re.search(r"addEventListener|setInterval|setTimeout|new\s+Worker|createParser", source_text)
    cleanup_present = re.search(r"removeEventListener|clearInterval|clearTimeout|terminate\s*\(|dispose\s*\(|cleanup", source_text)
    if resource_created and not cleanup_present:
        violations.append(_violation("explicit_lifecycle_cleanup", "resource creation lacks visible cleanup"))
    return violations


def _detect_direct_recursion(source_text):
    violations = []
    names = re.findall(r"function\s+([A-Za-z_$][\w$]*)\s*\(", source_text)
    names.extend(re.findall(r"const\s+([A-Za-z_$][\w$]*)\s*=\s*\([^)]*\)\s*=>", source_text))
    for name in names:
        if len(re.findall(rf"\b{re.escape(name)}\s*\(", source_text)) > 1:
            violations.append(_violation("no_recursion", f"direct self-call rejected for {name}"))
    return violations


def _finish_result(result):
    violations = result.get("violations", [])
    result["evaluation"] = BLOCKED if violations else PASS
    for flag in SIDE_EFFECT_FLAGS:
        result[flag] = False
    return result


def _validate_mechanical_rules(rules, errors):
    if not isinstance(rules, list):
        errors.append("mechanical_rules must be a list")
        return
    ids = []
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            errors.append(f"mechanical_rules[{index}] must be a dictionary")
            continue
        _validate_closed_schema(rule, RULE_KEYS, f"mechanical_rules[{index}]", errors)
        ids.append(rule.get("id"))
        for key in RULE_KEYS:
            if not isinstance(rule.get(key), str) or not rule.get(key):
                errors.append(f"mechanical_rules[{index}].{key} must be a non-empty string")
    if ids != list(MECHANICAL_RULE_IDS):
        errors.append("mechanical_rules must exactly match BLK-058 mechanical rule IDs")


def _validate_profile_names(values, path, errors):
    if not isinstance(values, list) or not values:
        errors.append(f"{path} must be a non-empty list")
        return
    for value in values:
        if not isinstance(value, str):
            errors.append(f"{path} entries must be strings")
            continue
        lowered = value.lower()
        if any(marker in lowered for marker in COMMAND_MARKERS):
            errors.append(f"{path} contains forbidden command-shaped profile name {value!r}")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", value):
            errors.append(f"{path} profile name must be repository-owned kebab-case metadata: {value!r}")


def _validate_denied_authorities(values, path, errors):
    if not isinstance(values, list):
        errors.append(f"{path} must be a list")
        return
    if any(not isinstance(value, str) for value in values):
        errors.append(f"{path} entries must all be strings")
        return
    if len(values) != len(set(values)):
        errors.append(f"{path} must not contain duplicate entries")
    if tuple(values) != DENIED_AUTHORITIES:
        missing = sorted(set(DENIED_AUTHORITIES) - set(values))
        extra = sorted(set(values) - set(DENIED_AUTHORITIES))
        errors.append(f"{path} must exactly match denied_authorities; missing={missing!r} extra={extra!r}")


def _validate_side_effect_flags(profile, errors):
    for flag in SIDE_EFFECT_FLAGS:
        if profile.get(flag) is not False:
            errors.append(f"{flag} must be False")


def _validate_closed_schema(mapping, allowed_keys, path, errors, as_violation=False):
    if not isinstance(mapping, dict):
        message = f"{path} must be a dictionary"
        errors.append(_violation("candidate_schema", message) if as_violation else message)
        return
    for key in sorted(set(mapping) - allowed_keys, key=str):
        message = f"{path} unsupported key {key!r}"
        errors.append(_violation("candidate_schema", message) if as_violation else message)


def _scan_for_laundering(value, path, errors, as_violation=False):
    local_errors = errors
    if path.endswith(".denied_authorities") or path in {"profile.denied_authorities"}:
        return local_errors
    if isinstance(value, dict):
        scan_keys = path.startswith("candidate")
        for key, nested in value.items():
            child_path = f"{path}.{key}"
            if scan_keys and isinstance(key, str) and _contains_forbidden_laundering_marker(key):
                local_errors = _append_laundering_error(child_path, local_errors, as_violation)
            if key == "denied_authorities" or (isinstance(nested, bool) and nested is False):
                continue
            local_errors = _scan_for_laundering(nested, child_path, local_errors, as_violation=as_violation)
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            local_errors = _scan_for_laundering(nested, f"{path}[{index}]", local_errors, as_violation=as_violation)
    elif isinstance(value, str):
        if _contains_forbidden_laundering_marker(value):
            local_errors = _append_laundering_error(path, local_errors, as_violation)
    elif value is True and path.startswith("candidate") and _contains_forbidden_laundering_marker(path):
        local_errors = _append_laundering_error(path, local_errors, as_violation)
    return local_errors


def _contains_forbidden_laundering_marker(text):
    normalized = _normalize(str(text))
    lowered = str(text).lower()
    return any(marker in normalized for marker in FORBIDDEN_NORMALIZED_MARKERS) or any(
        marker in lowered for marker in FORBIDDEN_RAW_MARKERS
    )


def _append_laundering_error(path, errors, as_violation):
    message = f"forbidden authority/tooling wording at {path}"
    errors.append(_violation("no_authority_laundering", message) if as_violation else message)
    return errors


def _violation(rule_id, message):
    return {"rule_id": rule_id, "message": message}


def _normalize(text):
    return re.sub(r"[^a-z0-9]+", "", _split_camel(str(text)).lower())


def _split_camel(text):
    return re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
