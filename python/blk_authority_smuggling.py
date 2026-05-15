DENIED_AUTHORITY_KEY_NAMES = (
    "runtime_authority_granted",
    "live_codex_execution_authorized",
    "blk_pipe_dispatch_authorized",
    "production_blk_test_mcp_authorized",
    "authoritative_beo_publication_authorized",
    "runtime_rtm_generation_authorized",
    "rtm_drift_rejection_authorized",
    "protected_blk_req_body_reads_authorized",
    "network_model_cyber_browser_tooling_authorized",
    "package_manager_authorized",
    "production_isolation_claimed",
)

GENERIC_FORBIDDEN_KEYS = {
    "authority",
    "approved",
    "authorized",
    "approval_status",
    "execution_authorized",
    "runtime_authority",
    "live_authority",
    "publication_authorized",
    "rtm_authorized",
    "drift_authorized",
    "protected_body_read_authorized",
    "is_authorized",
}

FORBIDDEN_VALUE_PHRASES = (
    "approved for runtime execution",
    "runtime execution approved",
    "runtime execution authorized",
    "live execution authorized",
    "live codex execution is authorized",
    "authoritative beo publication approved",
    "beo publication authorized",
    "publication authority granted",
    "approved for publication",
    "greenlit for production",
    "production blk-test mcp is authorized",
    "production blk test mcp is authorized",
    "rtm drift rejection is authorized",
    "protected blk req body reads authorized",
    "production sandbox is enforced",
    "exact-id retrieval authorized",
    "exact id retrieval authorized",
    "staged revision overwrite authorized",
    "public-authority ledger rollback authorized",
    "public authority ledger rollback authorized",
    "runtime_authority_granted",
)

FORBIDDEN_COMPACT_VALUE_TOKENS = {
    "approvedforliveexecution",
    "runtimeexecutionauthorized",
    "runtimeexecutionapproved",
    "liveexecutionauthorized",
    "livecodexexecutionisauthorized",
    "authoritativebeopublicationapproved",
    "beopublicationauthorized",
    "publicationauthoritygranted",
    "approvedforpublication",
    "greenlitforproduction",
    "productionblktestmcpisauthorized",
    "rtmdriftrejectionisauthorized",
    "protectedblkreqbodyreadsauthorized",
    "productionsandboxisenforced",
    "exactidretrievalauthorized",
    "stagedrevisionoverwriteisauthorized",
    "publicauthorityledgerrollbackisauthorized",
    "runtimeauthoritygranted",
    "publishbeo",
    "rtmgenerationauthorized",
    "driftrejectionexecuted",
    "productionblklinkenabled",
    "docsrequirementsactive",
}

_GENERIC_FORBIDDEN_KEY_COMPACTS = {"".join(ch.lower() for ch in item if ch.isalnum()) for item in GENERIC_FORBIDDEN_KEYS}


def compact_authority_text(value: str) -> str:
    return "".join(ch.lower() for ch in value if ch.isalnum())


def percent_decode_once(value: str) -> str:
    result = []
    index = 0
    while index < len(value):
        if (
            value[index] == "%"
            and index + 2 < len(value)
            and all(ch in "0123456789abcdefABCDEF" for ch in value[index + 1 : index + 3])
        ):
            result.append(chr(int(value[index + 1 : index + 3], 16)))
            index += 3
            continue
        result.append(value[index])
        index += 1
    return "".join(result)


def decoded_authority_variants(value: str, *, max_rounds: int = 5) -> list[str]:
    variants = [value]
    current = value
    for _ in range(max_rounds):
        decoded = percent_decode_once(current)
        if decoded == current:
            break
        variants.append(decoded)
        current = decoded
    return variants


def scan_for_authority_laundering(value, path: str = "record", denied_keys=DENIED_AUTHORITY_KEY_NAMES) -> list[str]:
    errors = []
    denied_key_set = set(denied_keys)
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            for key_variant in decoded_authority_variants(key_text):
                key_compact = compact_authority_text(key_variant)
                if key_variant in denied_key_set or key_variant in GENERIC_FORBIDDEN_KEYS:
                    errors.append(f"{path}.{key_text} contains forbidden authority key")
                if key_compact in _GENERIC_FORBIDDEN_KEY_COMPACTS:
                    errors.append(f"{path}.{key_text} contains forbidden authority key")
                if key_compact in FORBIDDEN_COMPACT_VALUE_TOKENS:
                    errors.append(f"{path}.{key_text} contains forbidden authority wording {key_compact!r}")
            errors.extend(scan_for_authority_laundering(nested, f"{path}.{key_text}", denied_key_set))
    elif isinstance(value, (list, tuple, set)):
        for index, nested in enumerate(value):
            errors.extend(scan_for_authority_laundering(nested, f"{path}[{index}]", denied_key_set))
    elif isinstance(value, str):
        for variant in decoded_authority_variants(value):
            lowered = variant.lower()
            compact = compact_authority_text(variant)
            if lowered.strip() in {"approved", "authorized"}:
                errors.append(f"{path} contains forbidden authority wording {value!r}")
            for phrase in FORBIDDEN_VALUE_PHRASES:
                if phrase in lowered:
                    errors.append(f"{path} contains forbidden authority wording {phrase!r}")
            for token in FORBIDDEN_COMPACT_VALUE_TOKENS:
                if token in compact:
                    errors.append(f"{path} contains forbidden authority wording {token!r}")
    return errors
