import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLK001 = ROOT / "docs" / "BLK-001_blk-system-master-architecture.md"
BLK003 = ROOT / "docs" / "BLK-003_blk-pipe-blk-test-orchestration.md"
BLK004 = ROOT / "docs" / "BLK-004_blk-pipe-v47-architecture-suite.md"
BLK006 = ROOT / "docs" / "BLK-006_blk-req-implementation-brief.md"
BLK008 = ROOT / "docs" / "BLK-008_blk-test-mcp-execution-server.md"
BLK015 = ROOT / "docs" / "BLK-015_blk-pipe-approval-and-mcp-integration-design.md"
BLK016 = ROOT / "docs" / "BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md"
BLK017 = ROOT / "docs" / "BLK-017_blk-test-mcp-disabled-transport-skeleton.md"
BLK018 = ROOT / "docs" / "BLK-018_blk-test-mcp-workspace-process-control-probes.md"
BLK019 = ROOT / "docs" / "BLK-019_blk-test-mcp-approval-source-evidence-authorization.md"
BLK020 = ROOT / "docs" / "BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md"
BLK021 = ROOT / "docs" / "BLK-021_beo-draft-publication-gate-review.md"
BLK022 = ROOT / "docs" / "BLK-022_authoritative-beo-publication-design-boundary.md"
BLK023 = ROOT / "docs" / "BLK-023_offline-rtm-ledger-design-boundary.md"
BLK024 = ROOT / "docs" / "BLK-024_blk-system-development-roadmap.md"
BLK025 = ROOT / "docs" / "BLK-025_blk-test-pilot-readiness-boundary.md"
BLK026 = ROOT / "docs" / "BLK-026_beo-publication-candidate-fixture-boundary.md"
BLK027 = ROOT / "docs" / "BLK-027_rtm-hash-only-metadata-path-boundary.md"
BLK028 = ROOT / "docs" / "BLK-028_published-beo-input-boundary.md"
BLK029 = ROOT / "docs" / "BLK-029_active-vault-hash-metadata-backend-boundary.md"
BLK030 = ROOT / "docs" / "BLK-030_rtm-generation-readiness-proposal-boundary.md"
BLK031 = ROOT / "docs" / "BLK-031_operator-ux-observability-runbook-boundary.md"
BLK032 = ROOT / "docs" / "BLK-032_track-i-live-health-check-boundary.md"
BLK033 = ROOT / "docs" / "BLK-033_offline-rtm-generation-boundary.md"
BLK034 = ROOT / "docs" / "BLK-034_track-i-advisory-health-check-runner-boundary.md"
SPRINT030_PLAN = ROOT / "docs" / "plans" / "blk-system-030_offline-rtm-generation.md"
SPRINT030_CLOSEOUT = ROOT / "docs" / "outcomes" / "BLK-SYSTEM-030_sprint-closeout.md"
SPRINT006_CLOSEOUT = ROOT / "docs" / "outcomes" / "BLK-PIPE-006_sprint-closeout.md"
SPRINT006_AMENDMENT = ROOT / "docs" / "outcomes" / "BLK-PIPE-006_post-closeout-hostile-review-amendment.md"
SPRINT006_REVIEW = ROOT / "docs" / "reviews" / "BLK-PIPE-006_hostile-review_BLK-001-alignment.md"
SPRINT006_SCOPE_ADDENDUM = ROOT / "docs" / "reviews" / "BLK-PIPE-006_BLK-008_review-scope-addendum.md"
SPRINT010_ALIGNMENT = ROOT / "docs" / "reviews" / "BLK-SYSTEM-010_blk001-alignment-review.md"
SPRINT010_GAP_REGISTER = ROOT / "docs" / "reviews" / "BLK-SYSTEM-010_fixture-to-live-gap-register.md"
SPRINT010_APPROVAL_REGISTER = ROOT / "docs" / "reviews" / "BLK-SYSTEM-010_approval-and-authority-decision-register.md"
SPRINT010_SANDBOX_SPEC = ROOT / "docs" / "reviews" / "BLK-SYSTEM-010_sandbox-capability-readiness-spec.md"
SPRINT010_SLICING = ROOT / "docs" / "reviews" / "BLK-SYSTEM-010_future-sprint-slicing.md"
SPRINT011_TRANSPORT_REVIEW = ROOT / "docs" / "reviews" / "BLK-SYSTEM-011_transport-boundary-review.md"
SPRINT012_WORKSPACE_PROCESS_REVIEW = ROOT / "docs" / "reviews" / "BLK-SYSTEM-012_workspace-process-control-review.md"
SPRINT013_APPROVAL_REVIEW = ROOT / "docs" / "reviews" / "BLK-SYSTEM-013_approval-source-evidence-boundary-review.md"
SPRINT014_LIVE_SMOKE_REVIEW = ROOT / "docs" / "reviews" / "BLK-SYSTEM-014_live-fixed-tool-smoke-boundary-review.md"
SPRINT015_BEO_GATE_REVIEW = ROOT / "docs" / "reviews" / "BLK-SYSTEM-015_draft-beo-publication-gate-review.md"
SPRINT016_BEO_PUBLICATION_REVIEW = ROOT / "docs" / "reviews" / "BLK-SYSTEM-016_authoritative-beo-publication-design-review.md"
SPRINT017_RTM_LEDGER_REVIEW = ROOT / "docs" / "reviews" / "BLK-SYSTEM-017_offline-rtm-ledger-design-review.md"
SPRINT010_REVIEW_DOCS = [
    SPRINT010_ALIGNMENT,
    SPRINT010_GAP_REGISTER,
    SPRINT010_APPROVAL_REGISTER,
    SPRINT010_SANDBOX_SPEC,
    SPRINT010_SLICING,
]
ACTIVE_BLK_DOCS = sorted((ROOT / "docs").glob("BLK-*.md"))
TRUNCATED_SHA_RE = re.compile(r"sha256:(?:[0-9a-fA-F]{1,63})?\.\.\.")
YAML_FENCE_RE = re.compile(r"```yaml\n(.*?)\n\s*```", re.DOTALL)


def yaml_fences(path: Path) -> list[str]:
    return YAML_FENCE_RE.findall(path.read_text())


class ActiveDoctrineReviewGateTest(unittest.TestCase):
    def test_blk003_strict_yaml_examples_do_not_use_truncated_trace_hashes(self):
        offenders = []
        for block in yaml_fences(BLK003):
            if "trace_artifacts:" not in block:
                continue
            for match in TRUNCATED_SHA_RE.finditer(block):
                offenders.append(match.group(0))
        self.assertEqual(offenders, [], f"BLK-003 strict YAML uses truncated hashes: {offenders}")

    def test_blk003_escalation_is_current_boundary_safe(self):
        text = BLK003.read_text()
        required = [
            "human escalation package",
            "draft-only BEO",
            "source-bound fixture",
            "live BLK-test MCP remains disabled",
            "authoritative BEO publication remains disabled",
            "RTM generation remains disabled",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-003 escalation boundary missing: {missing}")

    def test_blk006_yaml_examples_do_not_use_truncated_sha256_placeholders(self):
        offenders = []
        for block in yaml_fences(BLK006):
            for match in TRUNCATED_SHA_RE.finditer(block):
                offenders.append(match.group(0))
        self.assertEqual(offenders, [], f"BLK-006 YAML uses truncated hashes: {offenders}")

    def test_blk006_documents_new_draft_and_staged_revision_lifecycles(self):
        text = BLK006.read_text()
        required = [
            'parent_hash: ""',
            'version_hash: "PENDING"',
            'parent_hash: "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"',
            "promotion",
            "DRAFT documents must not invent future hashes",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-006 lifecycle markers missing: {missing}")

    def test_sprint018_exit3_and_revert_boundaries_are_active_doctrine(self):
        checks = {
            BLK006: [
                "protected BLK-req vault allowlist violations return POSIX Exit 3",
                "UNAUTHORIZED_FILE_MUTATION",
                "does not authorize BLK-req vault body reads",
                "does not authorize live BLK-test MCP",
                "does not authorize authoritative BEO publication",
                "does not authorize RTM generation",
            ],
            BLK004: [
                "revert bypasses execute-mode clean preflight only after target hash validation",
                "target_hash",
                "sprint_base_hash",
                "UNAUTHORIZED_FILE_MUTATION",
                "does not authorize BLK-req vault body reads",
                "does not authorize live BLK-test MCP",
                "does not authorize authoritative BEO publication",
                "does not authorize RTM generation",
            ],
        }
        missing = []
        for path, markers in checks.items():
            text = path.read_text()
            for marker in markers:
                if marker not in text:
                    missing.append(f"{path.relative_to(ROOT)} missing {marker}")
        self.assertEqual(missing, [])

    def test_sprint019_blk020_exception_overlay_preserves_disabled_authority(self):
        checks = {
            BLK003: [
                "BLK-020 first-smoke evidence contract",
                "single accepted first live fixed-tool smoke exception",
                "generic/production BLK-test MCP remains disabled",
                "no new live BLK-test MCP authority",
                "does not authorize production BLK-test MCP",
                "does not authorize source mutation as BLK-test behavior",
                "does not read protected BLK-req vault bodies",
                "does not authorize authoritative BEO publication",
                "does not authorize RTM generation",
            ],
            BLK017: [
                "BLK-020 first-smoke evidence contract",
                "single accepted first live fixed-tool smoke exception",
                "disabled transport contract remains active for generic startup paths",
                "no new live BLK-test MCP authority",
                "does not authorize production BLK-test MCP",
                "does not authorize authoritative BEO publication",
                "does not authorize RTM generation",
            ],
            BLK018: [
                "BLK-020 records the accepted BLK-SYSTEM-014 first-smoke evidence contract",
                "synthetic isolated workspace",
                "not production BLK-test MCP authority",
            ],
        }
        missing = []
        for path, markers in checks.items():
            text = path.read_text()
            for marker in markers:
                if marker not in text:
                    missing.append(f"{path.relative_to(ROOT)} missing {marker}")
        self.assertEqual(missing, [])

    def test_sprint020_validation_profile_boundary_preserves_go_authority(self):
        text = BLK004.read_text()
        required = [
            "validation_profiles",
            "repository-owned named validation profiles",
            "exact resolved commands",
            "transitional trusted-local compatibility",
            "less-trusted/autonomous payload boundaries must use profiles",
            "Go remains the enforcement authority",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-004 validation profile boundary markers missing: {missing}")

    def test_sprint021_python_adapter_policy_boundary_preserves_go_authority(self):
        text = BLK004.read_text()
        required = [
            "Python adapter policy checks are fail-fast convenience only",
            "Go remains the final deterministic enforcement authority",
            "canonical trace_artifacts",
            "validation profiles",
            "exact allowlists",
            "raw report evidence",
            "SSH_AUTH_SOCK",
            "does not authorize production BLK-test MCP",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-004 Python adapter policy boundary markers missing: {missing}")

    def test_sprint022_blk_test_pilot_readiness_boundary_preserves_evidence_only_authority(self):
        self.assertTrue(BLK025.exists(), "BLK-025 pilot readiness boundary missing")
        text = BLK025.read_text()
        required = [
            "BLK-test pilot readiness boundary",
            "Design-only boundary contract",
            "Track F — BLK-test production-readiness ladder",
            "evidence only",
            "fixed-tool registry",
            "no arbitrary shell",
            "no source mutation",
            "no protected BLK-req vault body reads",
            "no authoritative BEO publication",
            "no RTM generation",
            "no production BLK-test MCP",
            "new live BLK-test smoke runs",
            "caller-supplied commands",
            "dynamic tool expansion",
            "RTM drift rejection authority",
            "public ledger mutation",
            "signer, storage, rollback",
            "production sandbox, cgroup, VM, network, or host-secret isolation claims",
            "separate human approval",
            "L4 pilot authority requires a later explicit sprint",
            "Future-Sprint Split Table",
            "Synthetic-smoke expansion",
            "L4 BLK-test pilot runtime",
            "BEO publication implementation",
            "RTM hash-only metadata path",
            "real target-repo escape",
            "symlink escape",
            "host-secret-bearing path access",
            "timeout failure",
            "output flood failure",
            "descendant process kill",
            "replayed approval IDs",
            "BLK-017",
            "BLK-018",
            "BLK-019",
            "BLK-020",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-025 pilot readiness markers missing: {missing}")

        current_contract_checks = {
            BLK017: ["does not authorize live BLK-test MCP", "does not authorize RTM generation"],
            BLK018: ["does not authorize live BLK-test MCP", "does not authorize RTM generation"],
            BLK019: ["does not authorize live BLK-test MCP", "does not authorize RTM generation"],
            BLK020: ["does not authorize production BLK-test MCP", "does not authorize RTM generation"],
        }
        missing_current = []
        for path, markers in current_contract_checks.items():
            contract_text = path.read_text()
            for marker in markers:
                if marker not in contract_text:
                    missing_current.append(f"{path.relative_to(ROOT)} missing {marker}")
        self.assertEqual(missing_current, [])

    def test_sprint023_beo_publication_candidate_fixture_boundary_preserves_no_publication_authority(self):
        self.assertTrue(BLK026.exists(), "BLK-026 BEO publication candidate fixture boundary missing")
        text = BLK026.read_text()
        required = [
            "BEO publication candidate fixture boundary",
            "Active fixture boundary contract — not publication authority",
            "Track G — BEO publication path",
            "PUBLICATION_CANDIDATE_FIXTURE_ONLY",
            'beo_publication: "DRAFT_ONLY"',
            'rtm_status: "NOT_GENERATED"',
            "no authoritative BEO publication",
            "no runtime `PUBLISHED` BEO output",
            "no signer key material",
            "no immutable storage writes",
            "no public ledger mutation",
            "no rollback, revocation, or supersession execution",
            "no RTM generation",
            "no RTM drift rejection authority",
            "no protected BLK-req vault body reads",
            "publication-specific approval cannot be inherited from execution, BLK-test, draft BEO projection, codex-live approval, or RTM approval",
            "BLOCKED/fatal/transport/interrupted/unknown/missing/malformed/stale/replayed evidence cannot publish success",
            "future authoritative publication requires a later explicit sprint and human approval",
            "Source evidence identity requires canonical replay hashes",
            "Missing or malformed source evidence fails closed",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-026 candidate fixture boundary markers missing: {missing}")

        implementation_text = (ROOT / "python" / "beo_publication_candidate_fixtures.py").read_text()
        forbidden_live_markers = [
            "publish_authoritative_beo",
            "beo_publication = \"PUBLISHED\"",
            "generate_rtm",
            "public outcome ledger writer",
            "subprocess",
            "socket",
            "requests",
            "urllib",
            "http.client",
            "discord",
            "boto3",
            "google.cloud",
            "azure",
            "kms",
            "storage_writer",
            "ledger_writer",
            "rollback_executor",
            "live_blk_test",
        ]
        offenders = [marker for marker in forbidden_live_markers if marker in implementation_text]
        self.assertEqual(offenders, [], f"Sprint 023 implementation introduced live markers: {offenders}")

    def test_sprint024_rtm_hash_metadata_path_boundary_preserves_no_rtm_authority(self):
        self.assertTrue(BLK027.exists(), "BLK-027 RTM hash-only metadata path boundary missing")
        text = BLK027.read_text()
        required = [
            "RTM hash-only metadata path boundary",
            "Active fixture boundary contract — not RTM generation authority",
            "Track H — BLK-link offline RTM ledger",
            "RTM_HASH_METADATA_PATH_FIXTURE_ONLY",
            'rtm_status: "NOT_GENERATED"',
            'comparison_state: "NOT_EVALUATED_FIXTURE_ONLY"',
            "no RTM generation",
            "no RTM drift rejection authority",
            "no protected BLK-req vault body reads",
            "BEO publication candidates are not published BEOs",
            "hash-only metadata records must not contain protected bodies",
            "Missing or malformed hash-only metadata fails closed",
            "future RTM generation requires a later explicit sprint and human approval",
            "RTM drift rejection authority requires a still-later explicit authority boundary",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-027 hash metadata path boundary markers missing: {missing}")

        implementation_text = (ROOT / "python" / "rtm_hash_only_metadata_path_fixtures.py").read_text()
        forbidden_live_markers = [
            "def generate_rtm",
            "class RtmLedger",
            "rtm_status = \"GENERATED\"",
            "publish_authoritative_beo",
            "active_vault_hash_compare",
            "subprocess",
            "socket",
            "requests",
            "urllib",
            "http.client",
            "discord",
            "boto3",
            "google.cloud",
            "azure",
            "storage_writer",
            "ledger_writer",
            "rollback_executor",
            "live_blk_test",
        ]
        offenders = [marker for marker in forbidden_live_markers if marker in implementation_text]
        self.assertEqual(offenders, [], f"Sprint 024 implementation introduced live markers: {offenders}")

    def test_sprint025_published_beo_input_boundary_preserves_no_publication_or_rtm_authority(self):
        self.assertTrue(BLK028.exists(), "BLK-028 published-BEO input boundary missing")
        text = BLK028.read_text()
        required = [
            "Published BEO input boundary",
            "Active fixture boundary contract — not BEO publication authority",
            "Track G — BEO publication path",
            "Track H — BLK-link offline RTM ledger",
            "PUBLISHED_BEO_INPUT_FIXTURE_ONLY",
            'rtm_status: "NOT_GENERATED"',
            "no authoritative BEO publication",
            "no runtime `PUBLISHED` BEO output",
            "no signer key material",
            "no immutable storage writes",
            "no public ledger mutation",
            "no rollback, revocation, or supersession execution",
            "no RTM generation",
            "no RTM drift rejection authority",
            "no protected BLK-req vault body reads",
            "publication candidates are not published-BEO inputs",
            "Published-BEO input fixtures are not authoritative publication",
            "Missing or malformed publication receipt fails closed",
            "Top-level side-effect flags fail closed",
            "Secret-bearing fields fail closed",
            "Nested protected-body, RTM, publication, and secret-bearing fields fail closed",
            "Malformed non-string identity fields fail closed",
            "future RTM generation requires a later explicit sprint and human approval",
            "RTM drift rejection authority requires a still-later explicit authority boundary",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-028 published-BEO input boundary markers missing: {missing}")

        implementation_text = (ROOT / "python" / "published_beo_input_boundary_fixtures.py").read_text()
        forbidden_live_markers = [
            "def publish",
            "publish_authoritative_beo",
            "beo_publication = \"PUBLISHED\"",
            "generate_rtm",
            "active_vault_hash_compare",
            "subprocess",
            "socket",
            "requests",
            "urllib",
            "http.client",
            "discord",
            "boto3",
            "google.cloud",
            "azure",
            "storage_writer",
            "ledger_writer",
            "rollback_executor",
            "live_blk_test",
        ]
        offenders = [marker for marker in forbidden_live_markers if marker in implementation_text]
        self.assertEqual(offenders, [], f"Sprint 025 implementation introduced live markers: {offenders}")

    def test_sprint019_beo_authority_wording_is_draft_or_future_only(self):
        checks = {
            BLK001: [
                "BLK-test returns verification evidence, not authoritative BEO publication authority",
                "current BEO handling remains draft-only/design-only",
                "authoritative BEO publication remains disabled",
                "RTM generation remains disabled",
                "future/offline publication requires later explicit authority",
            ],
            BLK003: [
                "BLK-test returns verification evidence, not authoritative BEO publication authority",
                "draft-only BEO fixture",
                "authoritative BEO publication remains disabled",
                "RTM generation remains disabled",
                "future/offline publication requires later explicit authority",
            ],
        }
        missing = []
        for path, markers in checks.items():
            text = path.read_text()
            for marker in markers:
                if marker not in text:
                    missing.append(f"{path.relative_to(ROOT)} missing {marker}")
        self.assertEqual(missing, [])

    def test_blk008_declares_target_state_boundary_and_trace_contract(self):
        text = BLK008.read_text()
        required = [
            "target-state planning doctrine",
            "not current live MCP authorization",
            "BLK-013",
            "BLK-014",
            "BLK-015",
            "BLK-016",
            "PASS/FAIL payload shapes require non-empty canonical trace_artifacts",
            "sha256:<64-lowercase-hex>",
            "malformed trace hashes are rejected",
            "authoritative BEO publication remains disabled",
            "RTM generation remains disabled",
            "RTM drift rejection authority remains disabled",
            "source-binding requirements",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-008 boundary markers missing: {missing}")

    def test_sprint006_post_closeout_amendment_records_residual_trace_gaps(self):
        self.assertTrue(SPRINT006_AMENDMENT.exists(), "Sprint 006 post-closeout amendment missing")
        amendment = SPRINT006_AMENDMENT.read_text()
        required = [
            "conditional pass, not clean",
            "not a full BLK-001 traceability signoff",
            "HIGH-1",
            "HIGH-2",
            "BLK-PIPE-008",
            "HIGH-3",
            "MEDIUM-1",
            "MEDIUM-2",
            "MEDIUM-3",
            "BLK-PIPE-009",
            "does not authorize live Codex",
            "does not authorize live BLK-test MCP",
            "does not authorize authoritative BEO publication",
            "does not authorize RTM generation",
        ]
        missing = [marker for marker in required if marker not in amendment]
        self.assertEqual(missing, [], f"Sprint 006 amendment markers missing: {missing}")

    def test_sprint006_closeout_links_post_closeout_amendment(self):
        text = SPRINT006_CLOSEOUT.read_text()
        self.assertIn("BLK-PIPE-006_post-closeout-hostile-review-amendment.md", text)

    def test_active_yaml_fences_do_not_use_truncated_sha256_examples(self):
        offenders = []
        for path in ACTIVE_BLK_DOCS:
            text = path.read_text()
            if "**Status:** Active" not in text:
                continue
            for block in yaml_fences(path):
                for match in TRUNCATED_SHA_RE.finditer(block):
                    offenders.append(f"{path.relative_to(ROOT)}: {match.group(0)}")
        self.assertEqual(offenders, [], "truncated SHA examples in active YAML fences: " + repr(offenders))

    def test_sprint006_review_sources_are_preserved(self):
        self.assertTrue(SPRINT006_REVIEW.exists(), "Sprint 006 hostile review source missing")
        self.assertTrue(SPRINT006_SCOPE_ADDENDUM.exists(), "Sprint 006 BLK-008 addendum source missing")
        self.assertIn("BLK-PIPE-006 Hostile Review", SPRINT006_REVIEW.read_text())
        self.assertIn("BLK-008 Scope Check", SPRINT006_SCOPE_ADDENDUM.read_text())

    def test_sprint010_blk001_alignment_review_preserves_v_model_intent(self):
        self.assertTrue(SPRINT010_ALIGNMENT.exists(), "Sprint 010 BLK-001 alignment review missing")
        text = SPRINT010_ALIGNMENT.read_text()
        required = [
            "blk-req",
            "Architecture & Feature Planning",
            "blk-pipe",
            "blk-test",
            "Traceability Aggregator",
            "cryptographic version_hash baton",
            "does not authorize live BLK-test MCP",
            "does not authorize authoritative BEO publication",
            "does not authorize RTM generation",
            "does not authorize RTM drift rejection authority",
            "must not mutate source",
            "must not read protected BLK-req vault bodies",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"Sprint 010 BLK-001 alignment markers missing: {missing}")

    def test_sprint010_fixture_to_live_gap_register_is_complete(self):
        self.assertTrue(SPRINT010_GAP_REGISTER.exists(), "Sprint 010 fixture-to-live gap register missing")
        text = SPRINT010_GAP_REGISTER.read_text()
        required = [
            "MCP transport lifecycle",
            "Fixed tool registry",
            "no arbitrary shell",
            "Workspace clone/isolation and teardown",
            "Locking and parallel execution prevention",
            "Process tree kill/timeout/flood behavior",
            "Output compression",
            "Source evidence binding",
            "PASS/FAIL/BLOCKED",
            "BEO draft-only boundary",
            "RTM non-generation",
            "Approval-channel mechanics",
            "Secret/network isolation policy",
            "Active BLK-req vault read prohibition",
            "Audit logging and replay evidence",
            "Future implementation slice recommendations",
            "does not authorize live BLK-test MCP",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"Sprint 010 gap register markers missing: {missing}")

    def test_sprint010_approval_and_authority_decisions_bind_future_live_mcp(self):
        self.assertTrue(SPRINT010_APPROVAL_REGISTER.exists(), "Sprint 010 approval and authority decision register missing")
        text = SPRINT010_APPROVAL_REGISTER.read_text()
        required = [
            "codex-live approval is not BLK-test MCP approval",
            "source BLK-pipe report identity",
            "test profile",
            "human authorization before transport startup",
            "must not grant arbitrary shell",
            "must not grant source mutation",
            "must not grant BEO publication",
            "must not grant RTM generation",
            "must not grant active-vault read authority",
            "beb_id",
            "source commit_hash",
            "pre_engine_hash",
            "canonical trace_artifacts",
            "requested fixed BLK-test tool(s)",
            "target branch/workspace identity",
            "timeout/output profile",
            "operator identity/approval timestamp",
            "does not implement approval-channel mechanics",
            "blocked-token example",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"Sprint 010 approval-boundary markers missing: {missing}")

    def test_sprint010_sandbox_capability_readiness_spec_is_complete(self):
        self.assertTrue(SPRINT010_SANDBOX_SPEC.exists(), "Sprint 010 sandbox capability readiness spec missing")
        text = SPRINT010_SANDBOX_SPEC.read_text()
        required = [
            "stdio-only MCP transport readiness",
            "fixed tool list",
            "Zod/schema validation",
            "no dynamic command execution tool",
            "hardlink/same-filesystem clone decision and fallback",
            "startup purge",
            "per-run teardown",
            "stale lockfile behavior",
            "single-run mutex/lock",
            "parallel prevention",
            "child process group kill behavior",
            "timeout and output-flood response",
            "cache jailing",
            "environment scrubbing",
            "network policy",
            "secret exposure policy",
            "primary repo corruption prevention",
            "evidence artifacts required for replay",
            "not production sandbox/cgroup/VM enforcement",
            "does not authorize live BLK-test MCP",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"Sprint 010 sandbox-readiness markers missing: {missing}")

    def test_sprint010_future_sprint_slicing_defines_safe_candidates(self):
        self.assertTrue(SPRINT010_SLICING.exists(), "Sprint 010 future sprint slicing missing")
        text = SPRINT010_SLICING.read_text()
        required = [
            "BLK-SYSTEM-011",
            "BLK-test MCP disabled live-transport skeleton",
            "still non-executing",
            "BLK-SYSTEM-012",
            "Workspace isolation and process-control implementation probes",
            "BLK-SYSTEM-013",
            "Approval-channel and source-evidence authorization mechanics",
            "BLK-SYSTEM-014",
            "First live fixed-tool BLK-test MCP smoke under explicit human approval",
            "BLK-SYSTEM-015",
            "Draft BEO publication gate review",
            "Later RTM sprint",
            "offline RTM generation and drift rejection",
            "allowed scope",
            "explicit non-goals",
            "prerequisite gates",
            "BLK-001 domain protected",
            "stop condition",
            "does not authorize live BLK-test MCP",
            "does not authorize authoritative BEO publication",
            "does not authorize RTM generation",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"Sprint 010 future-slicing markers missing: {missing}")

    def test_sprint010_review_docs_do_not_authorize_live_authority(self):
        forbidden_missing = []
        required = [
            "does not authorize live BLK-test MCP",
            "does not authorize authoritative BEO publication",
            "does not authorize RTM generation",
        ]
        for path in SPRINT010_REVIEW_DOCS:
            self.assertTrue(path.exists(), f"Sprint 010 review doc missing: {path.relative_to(ROOT)}")
            text = path.read_text()
            missing = [marker for marker in required if marker not in text]
            if missing:
                forbidden_missing.append(f"{path.relative_to(ROOT)} missing {missing}")
        self.assertEqual(forbidden_missing, [])

    def test_sprint011_transport_boundary_review_is_disabled_and_non_executing(self):
        self.assertTrue(SPRINT011_TRANSPORT_REVIEW.exists(), "Sprint 011 transport boundary review missing")
        text = SPRINT011_TRANSPORT_REVIEW.read_text()
        required = [
            "BLK-SYSTEM-011",
            "disabled BLK-test MCP transport skeleton",
            "non-executing handshake gate",
            "stdio-only",
            "disabled by default",
            "does not authorize live BLK-test MCP",
            "does not authorize live MCP client/server startup",
            "does not execute fixed-tool tests",
            "does not authorize authoritative BEO publication",
            "does not authorize RTM generation",
            "does not authorize RTM drift rejection authority",
            "does not read protected BLK-req vault bodies",
            "must not mutate source",
            "must not grant arbitrary shell",
            "Sprint 012 owns workspace/process controls",
            "Sprint 013 owns approval/source-evidence authorization mechanics",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"Sprint 011 transport-boundary markers missing: {missing}")

    def test_sprint012_workspace_process_review_is_inert_and_non_authorizing(self):
        self.assertTrue(
            SPRINT012_WORKSPACE_PROCESS_REVIEW.exists(),
            "Sprint 012 workspace/process review missing",
        )
        text = SPRINT012_WORKSPACE_PROCESS_REVIEW.read_text()
        required = [
            "BLK-SYSTEM-012",
            "Workspace Isolation and Process-Control Implementation Probes",
            "deterministic local inert fixtures only",
            "does not authorize live BLK-test MCP",
            "does not authorize live MCP client/server startup",
            "does not execute fixed-tool tests",
            "does not mutate primary repo",
            "does not stage files",
            "does not commit",
            "does not authorize authoritative BEO publication",
            "does not authorize RTM generation",
            "does not authorize RTM drift rejection authority",
            "does not read protected BLK-req vault bodies",
            "does not claim production sandbox/cgroup/VM enforcement",
            "does not claim production host-secret isolation",
            "Sprint 013 owns approval/source-evidence authorization mechanics",
            "Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"Sprint 012 review markers missing: {missing}")

    def test_sprint013_approval_source_evidence_review_is_source_bound_and_non_executing(self):
        self.assertTrue(
            SPRINT013_APPROVAL_REVIEW.exists(),
            "Sprint 013 approval/source-evidence review missing",
        )
        text = SPRINT013_APPROVAL_REVIEW.read_text()
        required = [
            "BLK-SYSTEM-013",
            "Approval-channel and source-evidence authorization mechanics",
            "codex-live approval is not BLK-test MCP approval",
            "source BLK-pipe report identity",
            "beb_id",
            "source commit_hash",
            "pre_engine_hash",
            "canonical trace_artifacts",
            "requested fixed BLK-test tool(s)",
            "test profile",
            "workspace identity",
            "timeout/output profile",
            "operator identity/approval timestamp",
            "does not authorize live BLK-test MCP",
            "does not authorize live MCP client/server startup",
            "does not execute fixed-tool tests",
            "does not mutate primary repo",
            "does not authorize authoritative BEO publication",
            "does not authorize RTM generation",
            "does not read protected BLK-req vault bodies",
            "Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(
            missing,
            [],
            f"Sprint 013 approval/source-evidence markers missing: {missing}",
        )

    def test_sprint014_live_fixed_tool_smoke_review_preserves_prerequisite_boundaries(self):
        self.assertTrue(SPRINT014_LIVE_SMOKE_REVIEW.exists(), "Sprint 014 live smoke boundary review missing")
        text = SPRINT014_LIVE_SMOKE_REVIEW.read_text()
        required = [
            "BLK-SYSTEM-014",
            "First live fixed-tool BLK-test MCP smoke under explicit human approval",
            "BLK-017 remains the active disabled transport contract",
            "BLK-018 remains the workspace/process-control probe contract",
            "BLK-019 remains the approval/source-evidence authorization contract",
            "APPROVAL_VALIDATED_SOURCE_BOUND",
            "explicit current human approval",
            "one exact source/request/workspace/profile/tool envelope",
            "stdio-only",
            "dependency-free JSON-RPC/MCP-subset smoke",
            "run_ast_validation",
            "synthetic isolated workspace",
            "does not use arbitrary shell",
            "does not use non-stdio transport",
            "does not run against /home/dad/BLK-System",
            "does not mutate primary repo",
            "does not authorize authoritative BEO publication",
            "does not authorize RTM generation",
            "does not read protected BLK-req vault bodies",
            "does not claim production sandbox or host-secret isolation",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"Sprint 014 review markers missing: {missing}")

    def test_sprint015_draft_beo_publication_gate_review_is_draft_only(self):
        self.assertTrue(SPRINT015_BEO_GATE_REVIEW.exists(), "Sprint 015 BEO gate review missing")
        text = SPRINT015_BEO_GATE_REVIEW.read_text()
        required = [
            "BLK-SYSTEM-015",
            "Draft BEO publication gate review",
            "BLK-020 first-smoke evidence",
            "beo_publication: \"DRAFT_ONLY\"",
            "rtm_status: \"NOT_GENERATED\"",
            "source-bound and replayable",
            "PASS/FAIL evidence may project only to draft BEO fixtures",
            "BLOCKED evidence must not project to success",
            "does not authorize authoritative BEO publication",
            "does not mutate public outcome ledgers",
            "does not grant signer/storage/rollback authority",
            "does not authorize RTM generation",
            "does not claim RTM coverage",
            "does not read protected BLK-req vault bodies",
            "does not rerun BLK-SYSTEM-014 first live smoke",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"Sprint 015 BEO gate review markers missing: {missing}")

    def test_sprint016_beo_publication_design_review_preserves_non_authority(self):
        self.assertTrue(
            SPRINT016_BEO_PUBLICATION_REVIEW.exists(),
            "Sprint 016 BEO publication design review missing",
        )
        text = SPRINT016_BEO_PUBLICATION_REVIEW.read_text()
        required = [
            "BLK-SYSTEM-016",
            "BEO publication design, not implementation",
            "design only",
            "does not authorize authoritative BEO publication",
            "does not mutate public outcome ledgers",
            "does not grant signer/storage/rollback authority",
            "codex-live approval is not BEO publication approval",
            "BLK-test MCP approval is not BEO publication approval",
            "public ledger mutation rules remain future authority",
            "RTM generation remains disabled",
            "does not read protected BLK-req vault bodies",
            "PASS stays PASS",
            "FAIL stays FAIL",
            "BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"Sprint 016 BEO publication review markers missing: {missing}")

    def test_sprint017_offline_rtm_ledger_design_review_preserves_non_authority(self):
        self.assertTrue(
            SPRINT017_RTM_LEDGER_REVIEW.exists(),
            "Sprint 017 RTM ledger design review missing",
        )
        text = SPRINT017_RTM_LEDGER_REVIEW.read_text()
        required = [
            "BLK-SYSTEM-017",
            "Offline RTM ledger design, not implementation",
            "design only",
            "does not authorize RTM generation",
            "does not authorize RTM drift rejection authority",
            "does not generate RTM",
            "does not emit rtm_id",
            "does not create coverage matrices",
            "does not make drift decisions",
            "RTM generation approval is separate from BEO publication approval",
            "RTM generation approval is separate from BLK-test MCP approval",
            "RTM generation approval is separate from codex-live approval",
            "protected BLK-req vault bodies remain unread",
            "hash-only active-vault comparison remains future authority",
            "beo_publication: \"DRAFT_ONLY\" remains mandatory",
            "rtm_status: \"NOT_GENERATED\" remains mandatory",
            "rtm_authority: \"DISABLED_INTERFACE_ONLY\" remains mandatory",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"Sprint 017 RTM design review markers missing: {missing}")

    def test_blk022_records_design_only_authoritative_beo_publication_boundary(self):
        self.assertTrue(BLK022.exists(), "BLK-022 BEO publication design boundary missing")
        text = BLK022.read_text()
        required = [
            "**Status:** Active design-only boundary contract",
            "BLK-SYSTEM-016",
            "does not authorize authoritative BEO publication",
            "does not implement BEO publication",
            "does not mutate public outcome ledgers",
            "does not grant signer/storage/rollback authority",
            "does not emit runtime PUBLISHED BEOs",
            "beo_publication: \"DRAFT_ONLY\" remains the only current runtime output",
            "rtm_status: \"NOT_GENERATED\" remains mandatory",
            "codex-live approval is not BEO publication approval",
            "BLK-test MCP approval is not BEO publication approval",
            "PASS stays PASS",
            "FAIL stays FAIL",
            "BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success",
            "protected BLK-req vault bodies remain unread",
            "Later RTM sprint",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-022 boundary markers missing: {missing}")

    def test_blk022_hands_off_later_rtm_design_to_blk023_without_authority(self):
        text = BLK022.read_text()
        required = [
            "BLK-023",
            "offline RTM ledger design boundary",
            "does not authorize RTM generation",
            "does not authorize RTM drift rejection authority",
            "rtm_status: \"NOT_GENERATED\" remains mandatory",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-022 to BLK-023 handoff markers missing: {missing}")

    def test_blk023_records_design_only_offline_rtm_ledger_boundary(self):
        self.assertTrue(BLK023.exists(), "BLK-023 offline RTM ledger design boundary missing")
        text = BLK023.read_text()
        required = [
            "**Status:** Active design-only boundary contract",
            "BLK-SYSTEM-017",
            "offline RTM ledger design boundary",
            "does not authorize RTM generation",
            "does not authorize RTM drift rejection authority",
            "does not implement generate_rtm.py",
            "does not emit runtime rtm_id",
            "does not create coverage matrices",
            "does not make drift decisions",
            "RTM generation approval is separate from BEO publication approval",
            "RTM generation approval is separate from BLK-test MCP approval",
            "RTM generation approval is separate from codex-live approval",
            "hash-only active-vault comparison remains future authority",
            "protected BLK-req vault bodies remain unread",
            "beo_publication: \"DRAFT_ONLY\" remains mandatory",
            "rtm_status: \"NOT_GENERATED\" remains mandatory",
            "rtm_authority: \"DISABLED_INTERFACE_ONLY\" remains mandatory",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-023 boundary markers missing: {missing}")

    def test_blk017_records_disabled_transport_skeleton_without_live_authority(self):
        self.assertTrue(BLK017.exists(), "BLK-017 disabled transport skeleton doctrine missing")
        text = BLK017.read_text()
        required = [
            "**Status:** Active disabled transport contract",
            "disabled by default",
            "stdio-only",
            "non-executing handshake gate",
            "does not authorize live BLK-test MCP",
            "does not authorize live MCP client/server startup",
            "does not execute fixed-tool tests",
            "does not authorize authoritative BEO publication",
            "does not authorize RTM generation",
            "does not authorize RTM drift rejection authority",
            "does not read protected BLK-req vault bodies",
            "must not mutate source",
            "must not grant arbitrary shell",
            "Sprint 012 owns workspace/process controls",
            "Sprint 013 owns approval/source-evidence authorization mechanics",
            "BLK-SYSTEM-011.1",
            "tainted descriptor metadata is rejected, not normalized",
            "all public disabled-transport helper APIs enforce stdio-only metadata",
            "source_write_allowed: false",
            "staging_allowed: false",
            "commit_allowed: false",
            "push_allowed: false",
            "AST-aware source-scan gate",
            "subprocess_called public evidence key remains allowed",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-017 disabled transport markers missing: {missing}")

    def test_blk018_workspace_process_probe_contract_is_active_and_non_authorizing(self):
        self.assertTrue(BLK018.exists(), "BLK-018 workspace/process probe contract missing")
        text = BLK018.read_text()
        required = [
            "**Status:** Active workspace/process-control probe contract",
            "BLK-SYSTEM-012",
            "inert local fixtures only",
            "does not authorize live BLK-test MCP",
            "does not authorize live MCP client/server startup",
            "does not execute fixed-tool tests",
            "does not mutate primary repo",
            "does not stage files",
            "does not commit",
            "does not authorize authoritative BEO publication",
            "does not authorize RTM generation",
            "does not authorize RTM drift rejection authority",
            "does not read protected BLK-req vault bodies",
            "does not claim production sandbox/cgroup/VM enforcement",
            "does not claim production host-secret isolation",
            "Sprint 013 owns approval/source-evidence authorization mechanics",
            "BLK-020 records the accepted BLK-SYSTEM-014 first-smoke evidence contract",
            "not production BLK-test MCP authority",
            "python/blk_test_mcp_workspace_process_probes.py",
            "python/test_blk_test_mcp_workspace_process_probes.py",
            "python/test_active_doctrine_review_gates.py",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-018 workspace/process markers missing: {missing}")

    def test_blk019_records_sprint013_approval_source_evidence_without_live_startup(self):
        self.assertTrue(BLK019.exists(), "BLK-019 approval/source-evidence doctrine missing")
        text = BLK019.read_text()
        required = [
            "**Status:** Active approval/source-evidence authorization contract",
            "BLK-SYSTEM-013",
            "codex-live approval is not BLK-test MCP approval",
            "source BLK-pipe report identity",
            "beb_id",
            "source commit_hash",
            "pre_engine_hash",
            "canonical trace_artifacts",
            "requested fixed BLK-test tool(s)",
            "workspace identity",
            "timeout/output profile",
            "operator identity/approval timestamp",
            "one-run/scoped",
            "replay",
            "does not authorize live BLK-test MCP",
            "does not authorize live MCP client/server startup",
            "does not execute fixed-tool tests",
            "does not authorize authoritative BEO publication",
            "does not authorize RTM generation",
            "does not read protected BLK-req vault bodies",
            "Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke",
            "python/blk_test_mcp_approval_authorization.py",
            "python/test_blk_test_mcp_approval_authorization.py",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-019 markers missing: {missing}")

    def test_blk020_records_sprint014_first_live_smoke_without_production_authority(self):
        self.assertTrue(BLK020.exists(), "BLK-020 first live smoke doctrine missing")
        text = BLK020.read_text()
        required = [
            "**Status:** Active first-smoke evidence contract",
            "BLK-SYSTEM-014",
            "First live fixed-tool BLK-test MCP smoke under explicit human approval",
            "BLK-017 remains the active disabled transport contract",
            "BLK-018 remains the workspace/process-control probe contract",
            "BLK-019 remains the approval/source-evidence authorization contract",
            "run_ast_validation",
            "stdio-only",
            "dependency-free JSON-RPC/MCP-subset smoke",
            "synthetic isolated workspace",
            "one exact source/request/workspace/profile/tool envelope",
            "PASS/FAIL/BLOCKED evidence",
            "does not authorize production BLK-test MCP",
            "does not use arbitrary shell",
            "does not use non-stdio transport",
            "does not run against real target repositories",
            "does not mutate primary repo",
            "does not authorize authoritative BEO publication",
            "does not authorize RTM generation",
            "does not read protected BLK-req vault bodies",
            "does not claim production sandbox or host-secret isolation",
            "python/blk_test_mcp_fixed_tool_live_smoke.py",
            "python/test_blk_test_mcp_fixed_tool_live_smoke.py",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-020 markers missing: {missing}")

    def test_blk021_records_sprint015_draft_beo_gate_without_publication_authority(self):
        self.assertTrue(BLK021.exists(), "BLK-021 draft BEO gate doctrine missing")
        text = BLK021.read_text()
        required = [
            "**Status:** Active draft-only BEO gate review contract",
            "BLK-SYSTEM-015",
            "Draft BEO publication gate review",
            "BLK-020 first-smoke evidence",
            "source-bound and replayable",
            "beo_publication: \"DRAFT_ONLY\"",
            "rtm_status: \"NOT_GENERATED\"",
            "PASS/FAIL evidence may project only to draft BEO fixtures",
            "BLOCKED evidence must not project to success",
            "does not authorize authoritative BEO publication",
            "does not mutate public outcome ledgers",
            "does not grant signer/storage/rollback authority",
            "does not authorize RTM generation",
            "does not claim RTM coverage",
            "does not read protected BLK-req vault bodies",
            "does not rerun BLK-SYSTEM-014 first live smoke",
            "python/beo_fixture_projection.py",
            "python/test_beo_fixture_projection.py",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-021 markers missing: {missing}")

    def test_blk021_hands_off_publication_design_to_blk022_without_authority(self):
        text = BLK021.read_text()
        required = [
            "BLK-022",
            "authoritative BEO publication design boundary",
            "does not authorize authoritative BEO publication",
            "beo_publication: \"DRAFT_ONLY\" remains mandatory",
            "rtm_status: \"NOT_GENERATED\" remains mandatory",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-021 to BLK-022 handoff markers missing: {missing}")

    def test_blk016_020_021_cross_reference_draft_beo_without_publication_authority(self):
        expectations = {
            BLK016: ["BLK-021", "DRAFT_ONLY", "does not authorize authoritative BEO publication"],
            BLK020: ["BLK-021", "Draft BEO publication gate review", "does not authorize authoritative BEO publication"],
            BLK021: ["BLK-016", "BLK-020", "BLK-SYSTEM-015"],
        }
        for path, markers in expectations.items():
            text = path.read_text()
            missing = [marker for marker in markers if marker not in text]
            self.assertEqual(missing, [], f"{path.relative_to(ROOT)} missing {missing}")

    def test_blk017_018_019_020_cross_reference_first_smoke_without_broad_authority(self):
        expectations = {
            BLK017: ["BLK-020", "first live fixed-tool", "BLK-017 remains the active disabled transport contract"],
            BLK018: ["BLK-020", "synthetic isolated workspace", "does not authorize production BLK-test MCP"],
            BLK019: ["BLK-020", "explicit human approval", "one exact source/request/workspace/profile/tool envelope"],
            BLK020: ["BLK-017", "BLK-018", "BLK-019", "BLK-SYSTEM-014"],
        }
        for path, markers in expectations.items():
            text = path.read_text()
            missing = [marker for marker in markers if marker not in text]
            self.assertEqual(missing, [], f"{path.relative_to(ROOT)} missing {missing}")

    def test_blk017_018_019_cross_reference_approval_contract_without_live_authority(self):
        expectations = {
            BLK017: ["BLK-019", "Sprint 013", "approval/source-evidence"],
            BLK018: ["BLK-019", "approval/source-evidence authorization", "before BLK-020"],
            BLK019: ["BLK-017", "BLK-018", "Sprint 014"],
        }
        missing = []
        for path, markers in expectations.items():
            text = path.read_text()
            for marker in markers + [
                "does not authorize live BLK-test MCP",
                "does not authorize RTM generation",
                "does not authorize authoritative BEO publication",
            ]:
                if marker not in text:
                    missing.append(f"{path.relative_to(ROOT)} missing {marker}")
        self.assertEqual(missing, [])

    def test_blk008_017_018_cross_reference_workspace_process_contract_without_live_authority(self):
        expectations = {
            BLK008: [
                "BLK-018",
                "inert workspace/process-control probe contract",
                "target-state planning doctrine",
                "not current live MCP authorization",
            ],
            BLK017: [
                "BLK-018",
                "successor readiness probe",
                "BLK-017 remains the active disabled transport contract",
                "generic startup paths",
                "no new live BLK-test MCP authority",
            ],
            BLK018: [
                "BLK-008",
                "BLK-017",
                "active disabled transport contract",
            ],
        }
        missing = []
        for path, markers in expectations.items():
            text = path.read_text()
            for marker in markers + [
                "does not authorize live BLK-test MCP",
                "does not authorize RTM generation",
                "does not authorize authoritative BEO publication",
            ]:
                if marker not in text:
                    missing.append(f"{path.relative_to(ROOT)} missing {marker}")
        self.assertEqual(missing, [])

    def test_blk008_015_016_cross_reference_blk017_without_live_authority(self):
        docs = [BLK008, BLK015, BLK016]
        missing = []
        for path in docs:
            text = path.read_text()
            for marker in [
                "BLK-017",
                "does not authorize live BLK-test MCP",
                "does not authorize RTM generation",
                "does not authorize authoritative BEO publication",
            ]:
                if marker not in text:
                    missing.append(f"{path.relative_to(ROOT)} missing {marker}")
        self.assertEqual(missing, [])


    def test_sprint026_active_vault_hash_metadata_backend_preserves_no_read_or_rtm_authority(self):
        self.assertTrue(BLK029.exists(), "BLK-029 active-vault hash metadata backend boundary missing")
        text = BLK029.read_text()
        required = [
            "Active fixture boundary contract — not active-vault read authority and not RTM generation authority",
            "Track B — BLK-req legislative gateway",
            "Track H — BLK-link offline RTM ledger",
            "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY",
            "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY",
            'rtm_status: "NOT_GENERATED"',
            "no active-vault filesystem scanning",
            "no protected BLK-req vault body reads",
            "does not authorize RTM generation",
            "does not authorize RTM drift rejection authority",
            "does not authorize authoritative BEO publication",
            "future RTM generation requires a later explicit sprint and human approval",
            "Missing or malformed backend manifest metadata fails closed",
            "No active-vault scanner module is authorized",
            "No protected-vault body reader",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-029 boundary markers missing: {missing}")

        source = (ROOT / "python" / "active_vault_hash_metadata_backend_fixtures.py").read_text()
        forbidden_markers = [
            "subprocess",
            "socket",
            "requests",
            "urllib",
            "http.client",
            "discord",
            "boto3",
            "google.cloud",
            "azure",
            "open(",
            "Path(",
            "read_text",
            "glob(",
            "rglob(",
            "active_vault_scanner",
            "generate_rtm",
            "coverage_matrix_generator",
            "drift_decision_runtime",
            "publish_authoritative_beo",
        ]
        offenders = [marker for marker in forbidden_markers if marker in source]
        self.assertEqual(offenders, [], f"Sprint 026 implementation introduced live markers: {offenders}")

    def test_sprint027_rtm_generation_readiness_proposal_preserves_no_runtime_rtm_authority(self):
        self.assertTrue(BLK030.exists(), "BLK-030 RTM generation readiness proposal boundary missing")
        text = BLK030.read_text()
        required = [
            "RTM generation readiness proposal boundary",
            "Active proposal fixture boundary contract — not runtime RTM generation authority",
            "Track H — BLK-link offline RTM ledger",
            "RTM_GENERATION_READINESS_PROPOSAL_FIXTURE_ONLY",
            'rtm_status: "NOT_GENERATED"',
            'rtm_authority: "PROPOSAL_ONLY_NOT_AUTHORIZED"',
            "proposal-only fixture",
            "no runtime RTM generation",
            "no RTM IDs",
            "no RTM ledgers",
            "no coverage matrices",
            "no RTM drift rejection authority",
            "no active-vault filesystem scanning",
            "no protected BLK-req vault body reads",
            "no runtime active-vault hash comparison",
            "no authoritative BEO publication",
            "future runtime RTM generation requires a later explicit sprint and human approval",
            "This proposal request is not RTM generation approval",
            "Context-specific allowlists reject unsupported top-level fields",
            "Extra hash metadata identities, duplicate trace identities, duplicate metadata identities",
            "Persistent doctrine gate marker: BLK-SYSTEM-027 pins proposal-only no-runtime-RTM authority",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-030 boundary markers missing: {missing}")

        source = (ROOT / "python" / "rtm_generation_readiness_proposal_fixtures.py").read_text()
        forbidden_markers = [
            "def generate_rtm",
            "class RtmLedger",
            "subprocess",
            "socket",
            "requests",
            "urllib",
            "http.client",
            "discord",
            "boto3",
            "google.cloud",
            "azure",
            "open(",
            "Path(",
            "read_text",
            "glob(",
            "rglob(",
            "coverage_matrix_generator",
            "drift_decision_runtime",
            "publish_authoritative_beo",
            "ledger_writer",
            "storage_writer",
            "active_vault_scanner",
            "protected_vault_body_reader",
        ]
        offenders = [marker for marker in forbidden_markers if marker in source]
        self.assertEqual(offenders, [], f"Sprint 027 implementation introduced live markers: {offenders}")

    def test_sprint028_operator_observability_boundary_preserves_no_execution_authority(self):
        self.assertTrue(BLK031.exists(), "BLK-031 operator observability boundary missing")
        text = BLK031.read_text()
        required = [
            "Operator UX / observability runbook boundary",
            "Active fixture/runbook boundary contract — not execution authority",
            "Track I — Operator UX, observability, and escalation",
            "OPERATOR_OBSERVABILITY_FIXTURE_ONLY",
            "OPERATOR_ESCALATION_PACKAGE_FIXTURE_ONLY",
            "OBSERVABILITY_ONLY_NOT_EXECUTION",
            "invalid payload",
            "unauthorized mutation",
            "validation failed",
            "output limit exceeded",
            "revert anchor mismatch",
            "workspace is dirty",
            "missing approval",
            "approval stale or replayed",
            "protected BLK-req vault access denied",
            "BLK-test transport disabled",
            "BEO remains draft-only",
            "RTM not generated",
            "OFFLINE_RTM_LEDGER_GENERATED_FIXTURE_ONLY",
            "Fixture RTM ledger generated: BLK-033 fixture-only evidence",
            "FORBIDDEN_RUNTIME_RTM_GENERATION",
            "DRIFT_REVIEW_REQUIRED_NOT_REJECTED",
            "Drift review required: human review only, not drift rejection",
            "fixture RTM does not authorize live vault comparison",
            "fixture RTM does not authorize production RTM generation",
            "fixture RTM does not authorize drift rejection",
            "unknown or malformed",
            "does not run live health checks",
            "does not execute commands",
            "does not inspect files",
            "does not read protected BLK-req vault bodies",
            "does not authorize production BLK-test MCP",
            "does not authorize authoritative BEO publication",
            "does not authorize RTM generation",
            "does not authorize RTM drift rejection",
            "derivative/suffix authority fields fail closed",
            "escalation packages have package-level count/size bounds",
            "retry wording never implies approval",
            "dirty/reverted indicators must be class-consistent",
            "caller-supplied references/IDs are bounded",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-031 boundary markers missing: {missing}")

        source = (ROOT / "python" / "blk_operator_observability_fixtures.py").read_text()
        forbidden_markers = [
            "import subprocess",
            "from subprocess",
            "import socket",
            "import requests",
            "import urllib",
            "from pathlib",
            "Path(",
            "read_text",
            "glob(",
            "rglob(",
            "http.client",
            "os.system",
            "Popen",
            "shell=True",
            "eval(",
            "exec(",
            "__import__",
            "open(",
            "Path.read_text",
            "discord",
            "github",
            "publish_authoritative_beo",
            "generate_rtm",
            "coverage_matrix_generator",
            "drift_decision_runtime",
            "active_vault_scanner",
            "protected_vault_body_reader",
        ]
        offenders = [marker for marker in forbidden_markers if marker in source]
        self.assertEqual(offenders, [], f"Sprint 028 implementation introduced live markers: {offenders}")

    def test_sprint029_health_check_boundary_preserves_no_execution_authority(self):
        self.assertTrue(BLK032.exists(), "BLK-032 health-check boundary missing")
        text = BLK032.read_text()
        required = [
            "Track I live health-check boundary",
            "Boundary contract — not live health-check authority",
            "Track I — Operator UX, observability, and escalation",
            "HEALTH_CHECK_BOUNDARY_FIXTURE_ONLY",
            "HEALTH_CHECK_PROFILE_FIXTURE_ONLY",
            "HEALTH_CHECK_RESULT_FIXTURE_ONLY",
            "HEALTH_CHECK_ESCALATION_FIXTURE_ONLY",
            "HEALTH_CHECKS_NOT_EXECUTED",
            "HEALTH_CHECK_AUTHORITY_NOT_GRANTED",
            "ADVISORY_ONLY",
            "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED",
            "FORBIDDEN_IN_HEALTH_CHECK",
            "fixed argv arrays only",
            "shell strings are forbidden",
            "network commands are forbidden",
            "package-manager commands are forbidden",
            "Git mutation commands are forbidden",
            "protected-vault path/body scans are forbidden",
            "BEO/RTM/drift authority fields are forbidden",
            "does not execute commands",
            "does not start subprocesses",
            "does not call network services",
            "does not run package managers",
            "does not inspect files",
            "does not read protected BLK-req vault bodies",
            "does not scan active-vault paths",
            "does not mutate Git or source state",
            "does not capture approvals",
            "does not authorize production BLK-test MCP",
            "does not authorize authoritative BEO publication",
            "does not authorize RTM generation",
            "does not authorize RTM drift rejection",
            "health-check PASS remains advisory",
            "caller-supplied excerpts are bounded and redacted",
            "environment and secret leakage is rejected",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-032 boundary markers missing: {missing}")

        source = (ROOT / "python" / "blk_operator_health_check_fixtures.py").read_text()
        forbidden_markers = [
            "import subprocess",
            "from subprocess",
            "import socket",
            "import requests",
            "import urllib",
            "from pathlib",
            "Path(",
            "read_text",
            "glob(",
            "rglob(",
            "http.client",
            "os.system",
            "Popen",
            "shell=True",
            "eval(",
            "exec(",
            "__import__",
            "open(",
            "discord",
            "github",
            "publish_authoritative_beo",
            "generate_rtm",
            "coverage_matrix_generator",
            "drift_decision_runtime",
            "active_vault_scanner",
            "protected_vault_body_reader",
        ]
        offenders = [marker for marker in forbidden_markers if marker in source]
        self.assertEqual(offenders, [], f"Sprint 029 implementation introduced live markers: {offenders}")

    def test_sprint030_offline_rtm_generation_boundary_preserves_narrow_authority(self):
        self.assertTrue(BLK033.exists(), "BLK-033 offline RTM generation boundary missing")
        text = BLK033.read_text()
        required = [
            "Offline RTM generation boundary",
            "narrow fixture-only offline RTM ledger generation from supplied fixture inputs",
            "Track H — BLK-link offline RTM ledger",
            "OFFLINE_RTM_GENERATION_APPROVAL_FIXTURE_ONLY",
            "OFFLINE_RTM_LEDGER_GENERATED_FIXTURE_ONLY",
            "OFFLINE_RTM_COVERAGE_MATRIX_FIXTURE_ONLY",
            "OFFLINE_RTM_GENERATION_APPROVED_NARROW",
            "DRIFT_REVIEW_REQUIRED_NOT_REJECTED",
            "PROTECTED_BODY_NOT_READ",
            "ACTIVE_VAULT_NOT_SCANNED",
            "BEO_PUBLICATION_NOT_PERFORMED",
            "NO_SIGNER_STORAGE_OR_PUBLIC_LEDGER_SIDE_EFFECTS",
            "does not read protected BLK-req vault bodies",
            "does not scan active-vault paths",
            "does not publish BEOs",
            "does not access signer key material",
            "does not write immutable storage",
            "does not mutate public ledgers",
            "does not reject drift",
            "does not inherit approval",
            "hash-only metadata records",
            "coverage records are generated only by trace/hash metadata bijection",
            "Persistent doctrine gate marker: BLK-SYSTEM-030 pins narrow offline RTM generation only",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-033 boundary markers missing: {missing}")

        maturity_sources = {
            "BLK-033": BLK033.read_text(),
            "BLK-SYSTEM-030 plan": SPRINT030_PLAN.read_text(),
            "BLK-SYSTEM-030 closeout": SPRINT030_CLOSEOUT.read_text(),
        }
        required_maturity_markers = [
            "BLK-024 L1 fixture-only deterministic local RTM ledger fixture generation",
            "not L2 disabled transport",
            "not L4 pilot runtime",
            "not L5 production authority",
        ]
        stale_maturity_markers = [
            "L2-style approved local generation",
            "Maturity: Narrow approved local RTM generation",
        ]
        for label, content in maturity_sources.items():
            missing = [marker for marker in required_maturity_markers if marker not in content]
            self.assertEqual(missing, [], f"{label} missing BLK-024 maturity markers: {missing}")
            stale = [marker for marker in stale_maturity_markers if marker in content]
            self.assertEqual(stale, [], f"{label} retains stale maturity markers: {stale}")

        source = (ROOT / "python" / "offline_rtm_generation_fixtures.py").read_text()
        forbidden_markers = [
            "import subprocess",
            "from subprocess",
            "import socket",
            "import requests",
            "import urllib",
            "from pathlib",
            "Path(",
            "read_text",
            "glob(",
            "rglob(",
            "http.client",
            "os.system",
            "Popen",
            "shell=True",
            "eval(",
            "exec(",
            "__import__",
            "open(",
            "discord",
            "github",
            "publish_authoritative_beo",
            "active_vault_scanner",
            "protected_vault_body_reader",
            "drift_decision_runtime",
            "ledger_writer",
            "storage_writer",
            "public_ledger_writer",
        ]
        offenders = [marker for marker in forbidden_markers if marker in source]
        self.assertEqual(offenders, [], f"Sprint 030 implementation introduced live markers: {offenders}")

    def test_sprint032_advisory_health_check_runner_boundary_preserves_no_adjacent_authority(self):
        self.assertTrue(BLK034.exists(), "BLK-034 advisory health-check runner boundary missing")
        text = BLK034.read_text()
        required = [
            "Track I advisory health-check runner boundary",
            "Active pilot boundary — local advisory fixed-profile execution only",
            "Track I — Operator UX, observability, and escalation",
            "Track J — Security, sandbox, and capability hardening",
            "BLK-024 L4 pilot runtime for local fixed profiles only",
            "not L5 production authority",
            "HEALTH_CHECK_RUNNER_PILOT_ADVISORY_ONLY",
            "HEALTH_CHECK_EXECUTED_LOCAL_FIXED_PROFILE",
            "HEALTH_CHECK_PASS_GRANTS_NO_AUTHORITY",
            "NO_ARBITRARY_SHELL",
            "NO_NETWORK_MODEL_CYBER_TOOLING",
            "NO_PACKAGE_MANAGER",
            "NO_GIT_MUTATION",
            "NO_SOURCE_MUTATION",
            "NO_PROTECTED_BODY_READ",
            "NO_ACTIVE_VAULT_SCAN",
            "NO_BEO_PUBLICATION",
            "NO_RTM_GENERATION",
            "NO_DRIFT_REJECTION",
            "NOT_PRODUCTION_HEALTH_CHECK_AUTHORITY",
            "git_status_short_branch",
            "active_doctrine_gate",
            "shell=False",
            "unknown profiles fail closed",
            "caller-supplied argv is not accepted",
            "bounded stdout/stderr excerpts",
            "scrubbed environment",
            "Persistent doctrine gate marker: BLK-SYSTEM-032 pins advisory fixed-profile health-check runner only",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-034 boundary markers missing: {missing}")

    def test_blk024_requires_sprint_dispatch_approval_provenance_for_authority_sprints(self):
        text = BLK024.read_text()
        required = [
            "Sprint-dispatch approval provenance for authority-bearing plans",
            "source system",
            "operator identity",
            "message/event ID when available",
            "timestamp",
            "exact approved scope",
            "explicit excluded authorities",
            "sprint-dispatch approval does not substitute for runtime approval fixtures",
            "runtime/fixture approval hashes remain separate",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-024 approval provenance markers missing: {missing}")
