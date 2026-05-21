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
    "run_id_reservation_authorized",
    "run_id_consumption_authorized",
    "approval_reuse_authorized",
    "relay_message_dispatch_authorized",
    "signature_generation_authorized",
    "signer_storage_ledger_action_authorized",
    "signer_storage_ledger_action_approved",
    "relay_message_dispatch_approved",
    "kuronode_mutation_authorized",
    "protected_body_hashing_approved",
    "protected_body_scanning_authorized",
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
    "planner_dispatcher_authority",
    "source_of_truth_claimed",
    "production_mcp_started",
    "generic_mcp_started",
    "mcp_transport_started",
    "transport_granted",
    "transport_enabled",
    "target_source_git_mutation",
    "source_git_mutation",
    "beo_closeout_execution",
    "beo_publication",
    "rtm_generation",
    "production_blk_link",
    "coverage_truth",
    "drift_coverage_truth",
    "protected_body_access",
    "runtime_tooling",
    "production_isolation",
    "run_id_reserved",
    "run_id_consumed",
    "run_id_reservation_authorized",
    "run_id_consumption_authorized",
    "approval_reuse_authorized",
    "relay_message_dispatch_authorized",
    "signature_generation_authorized",
    "signer_storage_ledger_action_authorized",
    "signer_storage_ledger_action_approved",
    "relay_message_dispatch_approved",
    "kuronode_mutation_authorized",
    "protected_body_hashing_approved",
    "protected_body_scanning_authorized",
    "signer_storage_ledger_action",
}

FORBIDDEN_VALUE_PHRASES = (
    "approved for runtime execution",
    "runtime execution approved",
    "runtime execution authorized",
    "live execution authorized",
    "live codex execution is authorized",
    "authoritative beo publication approved",
    "beo publication authorized",
    "beo publication approved",
    "publication authority granted",
    "publication approval granted",
    "publication approval captured",
    "publication approval matched",
    "generic directive is publication approval",
    "generic operator directive is publication approval",
    "generic operator directive counts as publication approval",
    "execute next sprints is publication approval",
    "approved for publication",
    "greenlit for production",
    "production blk-test mcp is authorized",
    "production blk test mcp is authorized",
    "production blk-test mcp transport enabled",
    "production blk test mcp transport enabled",
    "production blk-test mcp transport granted",
    "production blk test mcp transport granted",
    "generic blk-test mcp transport enabled",
    "generic blk-test mcp transport granted",
    "mcp transport granted",
    "mcp transport enabled",
    "mcp transport active",
    "production mcp enabled",
    "production mcp started",
    "generic mcp started",
    "mcp service started",
    "planner dispatcher source of truth",
    "beo publication is now enabled",
    "beo published",
    "beo was published",
    "signer reused",
    "storage written",
    "ledger appended",
    "public ledger appended",
    "rtm generation enabled",
    "production blk-link enabled",
    "production blk link enabled",
    "protected-body access enabled",
    "protected body access enabled",
    "rtm drift rejection is authorized",
    "coverage truth established",
    "coverage truth is established",
    "coverage truth authorized",
    "coverage truth granted",
    "coverage truth executed",
    "drift truth established",
    "drift truth is established",
    "drift truth authorized",
    "drift truth granted",
    "production blk-link execution authorized",
    "production blk link execution authorized",
    "rtm generated",
    "rtm was generated",
    "rtm generation executed",
    "protected blk req body reads authorized",
    "production sandbox is enforced",
    "exact-id retrieval authorized",
    "exact id retrieval authorized",
    "staged revision overwrite authorized",
    "public-authority ledger rollback authorized",
    "public authority ledger rollback authorized",
    "run id reserved",
    "run id consumed",
    "run-id reservation authorized",
    "run-id consumption authorized",
    "run id reservation authorized",
    "run id consumption authorized",
    "consume at most one run id",
    "signature generated",
    "signature generation authorized",
    "signature generation approved",
    "signature generation is approved",
    "signer storage ledger action authorized",
    "signer storage ledger action approved",
    "signer storage ledger action executed",
    "signer storage ledger action is executed",
    "relay message dispatch authorized",
    "relay message dispatch approved",
    "relay message dispatch executed",
    "relay message dispatch is executed",
    "kuronode mutation authorized",
    "kuronode mutation executed",
    "kuronode mutation is executed",
    "protected body scanning authorized",
    "protected body hashed",
    "protected body hash authorized",
    "protected body hash is authorized",
    "protected body hashing authorized",
    "protected body hashing approved",
    "protected blk-req body hashing authorized",
    "protected blk req body hashing authorized",
    "protected body hash scan allowed",
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
    "beopublicationapproved",
    "publicationauthoritygranted",
    "publicationapprovalgranted",
    "publicationapprovalcaptured",
    "publicationapprovalmatched",
    "genericdirectiveispublicationapproval",
    "genericoperatordirectiveispublicationapproval",
    "genericoperatordirectivecountsaspublicationapproval",
    "executenextsprintsispublicationapproval",
    "approvedforpublication",
    "greenlitforproduction",
    "productionblktestmcpisauthorized",
    "productionblktestmcptransportenabled",
    "productionblktestmcptransportgranted",
    "genericblktestmcptransportenabled",
    "genericblktestmcptransportgranted",
    "mcptransportgranted",
    "mcptransportenabled",
    "mcptransportactive",
    "productionmcpenabled",
    "productionmcpstarted",
    "genericmcpstarted",
    "mcpservicestarted",
    "transportgranted",
    "transportenabled",
    "mcpstarted",
    "plannerdispatcherauthority",
    "sourceoftruthclaimed",
    "beopublicationenabled",
    "beopublished",
    "beowaspublished",
    "signerreused",
    "storagewritten",
    "ledgerappended",
    "publicledgerappended",
    "rtmgenerationenabled",
    "productionblklinkenabled",
    "productionblklinkauthorized",
    "productionblklinkexecutionauthorized",
    "productionblklinkexecutiongranted",
    "coveragetruthestablished",
    "coveragetruthauthorized",
    "coveragetruthgranted",
    "coveragetruthexecuted",
    "drifttruthestablished",
    "drifttruthauthorized",
    "drifttruthgranted",
    "rtmgenerated",
    "rtmgenerationexecuted",
    "protectedbodyaccessenabled",
    "rtmdriftrejectionisauthorized",
    "protectedblkreqbodyreadsauthorized",
    "productionsandboxisenforced",
    "exactidretrievalauthorized",
    "stagedrevisionoverwriteisauthorized",
    "publicauthorityledgerrollbackisauthorized",
    "runidreserved",
    "runidconsumed",
    "runidreservationauthorized",
    "runidconsumptionauthorized",
    "runidreservationapproved",
    "runidconsumptionapproved",
    "runidreservationconsumptionapproved",
    "runidreservationconsumptionauthorized",
    "runidreservationconsumptionisapproved",
    "runidreservationconsumptionisauthorized",
    "runidreservationandconsumptionapproved",
    "runidreservationandconsumptionauthorized",
    "runidreservationandconsumptionisapproved",
    "runidreservationandconsumptionisauthorized",
    "runidreservationisapproved",
    "runidconsumptionisapproved",
    "runidreservedapproved",
    "runidreservedauthorized",
    "runidreservedisapproved",
    "runidreservedisauthorized",
    "runidconsumedapproved",
    "runidconsumedauthorized",
    "runidconsumedisapproved",
    "runidconsumedisauthorized",
    "consumeatmostonerunid",
    "signaturegenerated",
    "signaturegenerationauthorized",
    "signaturegenerationapproved",
    "signaturegenerationisapproved",
    "signerstorageledgeractionauthorized",
    "signerstorageledgeractionapproved",
    "signerstorageledgeractionexecuted",
    "signerstorageledgeractionisexecuted",
    "signerstorageledgeractionisapproved",
    "relaymessagedispatchauthorized",
    "relaymessagedispatchapproved",
    "relaymessagedispatchexecuted",
    "relaymessagedispatchisexecuted",
    "relaymessagedispatchisauthorized",
    "relaymessagedispatchisapproved",
    "kuronodemutationauthorized",
    "kuronodemutationapproved",
    "kuronodemutationexecuted",
    "kuronodemutationisexecuted",
    "kuronodemutationgranted",
    "kuronodemutationisauthorized",
    "kuronodemutationisapproved",
    "protectedbodyhashed",
    "protectedbodyhashauthorized",
    "protectedbodyhashisauthorized",
    "protectedbodyhashingauthorized",
    "protectedbodyhashingapproved",
    "protectedbodyhashingisapproved",
    "protectedbodyscanningauthorized",
    "protectedbodyscanningapproved",
    "protectedbodyscanningisauthorized",
    "protectedbodyscanningisapproved",
    "protectedbodyscanauthorized",
    "protectedbodyscanapproved",
    "protectedbodyscanisauthorized",
    "protectedbodyscanisapproved",
    "protectedblkreqbodyhashingauthorized",
    "protectedbodyhashscanallowed",
    "runtimeauthoritygranted",
    "publishbeo",
    "rtmgenerationauthorized",
    "driftrejectionexecuted",
    "productionblklinkenabled",
    "docsrequirementsactive",
}

FORBIDDEN_EXACT_COMPACT_VALUE_TOKENS = {
    "signerstorageledgeraction",
}

SAFE_RUN_ID_MARKER_COMPACTS = {
    "norunidreserved",
    "norunidconsumed",
    "norunidreservedorconsumed",
    "norunidreservationorconsumption",
    "futurerunidreservednotconsumed",
    "futurepublicationexecutionrunidreservednotconsumed",
    "freshapprovalidandrunidreservedforfutureapproval",
    "onerunidreservednotconsumed",
    "blksystem264norunidreservedorconsumed",
}

_GENERIC_FORBIDDEN_KEY_COMPACTS = {"".join(ch.lower() for ch in item if ch.isalnum()) for item in GENERIC_FORBIDDEN_KEYS}


def compact_authority_text(value: str) -> str:
    return "".join(ch.lower() for ch in value if ch.isalnum())


def _safe_run_id_marker(compact: str) -> bool:
    return compact in SAFE_RUN_ID_MARKER_COMPACTS


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
                if key_compact == "isauthorized":
                    errors.append(f"{path}.{key_text} contains forbidden authority key")
                if nested is not False and (key_variant in denied_key_set or key_variant in GENERIC_FORBIDDEN_KEYS):
                    errors.append(f"{path}.{key_text} contains forbidden authority key")
                if nested is not False and key_compact in _GENERIC_FORBIDDEN_KEY_COMPACTS:
                    errors.append(f"{path}.{key_text} contains forbidden authority key")
                if nested is not False and key_compact in FORBIDDEN_COMPACT_VALUE_TOKENS:
                    errors.append(f"{path}.{key_text} contains forbidden authority wording {key_compact!r}")
                if nested is not False and key_compact in FORBIDDEN_EXACT_COMPACT_VALUE_TOKENS:
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
                    if phrase in {"run id reserved", "run id consumed"} and _safe_run_id_marker(compact):
                        continue
                    errors.append(f"{path} contains forbidden authority wording {phrase!r}")
            for token in FORBIDDEN_COMPACT_VALUE_TOKENS:
                if token in compact:
                    if token in {"runidreserved", "runidconsumed"} and _safe_run_id_marker(compact):
                        continue
                    errors.append(f"{path} contains forbidden authority wording {token!r}")
            for token in FORBIDDEN_EXACT_COMPACT_VALUE_TOKENS:
                if token == compact:
                    errors.append(f"{path} contains forbidden authority wording {token!r}")
    return errors
