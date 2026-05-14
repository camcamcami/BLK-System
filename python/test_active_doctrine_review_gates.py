import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLK001 = ROOT / "docs" / "BLK-001_blk-system-master-architecture.md"
BLK003 = ROOT / "docs" / "BLK-003_blk-pipe-blk-test-orchestration.md"
BLK004 = ROOT / "docs" / "BLK-004_blk-pipe-v47-architecture-suite.md"
BLK005 = ROOT / "docs" / "BLK-005_blk-req-specification.md"
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
BLK035 = ROOT / "docs" / "BLK-035_track-i-health-check-profile-expansion-boundary.md"
BLK036 = ROOT / "docs" / "BLK-036_track-i-health-check-sandbox-side-effect-observation-boundary.md"
BLK037 = ROOT / "docs" / "BLK-037_track-i-health-check-isolated-workspace-execution-boundary.md"
BLK038 = ROOT / "docs" / "BLK-038_track-i-health-check-git-metadata-fixture-boundary.md"
BLK039 = ROOT / "docs" / "BLK-039_track-i-health-check-escalation-package-boundary.md"
BLK040 = ROOT / "docs" / "BLK-040_codex-deterministic-invocation-profile-boundary.md"
BLK041 = ROOT / "docs" / "BLK-041_codex-deterministic-dispatch-envelope-boundary.md"
BLK042 = ROOT / "docs" / "BLK-042_codex-live-dispatch-readiness-gate-boundary.md"
BLK043 = ROOT / "docs" / "BLK-043_codex-live-dispatch-authority-request-disabled-adapter-boundary.md"
BLK044 = ROOT / "docs" / "BLK-044_codex-live-dispatch-execution-authority-design-gate.md"
BLK045 = ROOT / "docs" / "BLK-045_blk-system-post-042-roadmap.md"
BLK046 = ROOT / "docs" / "BLK-046_blk-system-current-state-authority-index.md"
BLK047 = ROOT / "docs" / "BLK-047_blk-test-fixed-tool-pilot-authority-request-boundary.md"
BLK048 = ROOT / "docs" / "BLK-048_authority-frontier-selection-gate-boundary.md"
BLK049 = ROOT / "docs" / "BLK-049_blk-test-fixed-tool-pilot-l3-l4-boundary.md"
BLK050 = ROOT / "docs" / "BLK-050_blk-test-fixed-tool-pilot-l4-real-repo-approval-boundary.md"
BLK051 = ROOT / "docs" / "BLK-051_blk-test-fixed-tool-l4-disposable-real-repo-runtime-boundary.md"
BLK052 = ROOT / "docs" / "BLK-052_blk-test-l4-evidence-trust-and-non-disposable-request-gate.md"
BLK053 = ROOT / "docs" / "BLK-053_non-disposable-l4-exact-target-approval-envelope-boundary.md"
BLK054 = ROOT / "docs" / "BLK-054_blk-test-non-disposable-l4-runtime-pilot-boundary.md"
BLK055 = ROOT / "docs" / "BLK-055_blk-test-fresh-non-disposable-l4-runtime-pass-boundary.md"
BLK056 = ROOT / "docs" / "BLK-056_repeatable-non-disposable-l4-wrapper-approval-boundary.md"
BLK057 = ROOT / "docs" / "BLK-057_authoritative-beo-publication-authority-request-boundary.md"
BLK058 = ROOT / "docs" / "BLK-058_kuronode-typescript-power-of-ten-tactical-standard.md"
BLK059 = ROOT / "docs" / "BLK-059_blk-system-post-058-roadmap.md"
BLK060 = ROOT / "docs" / "BLK-060_authoritative-beo-publication-approval-envelope-boundary.md"
BLK061 = ROOT / "docs" / "BLK-061_kuronode-typescript-power-of-ten-static-profile-boundary.md"
BLK062 = ROOT / "docs" / "BLK-062_kuronode-power-of-ten-validation-profile-registry-boundary.md"
BLK063 = ROOT / "docs" / "BLK-063_kuronode-power-of-ten-gate-pilot-approval-envelope-boundary.md"
BLK064 = ROOT / "docs" / "BLK-064_kuronode-ceb009-power-of-ten-static-gate-pilot-boundary.md"
BLK065 = ROOT / "docs" / "BLK-065_kuronode-ceb009-remediation-packet-boundary.md"
BLK066 = ROOT / "docs" / "BLK-066_kuronode-ceb009-patch-approval-envelope-boundary.md"
BLK067 = ROOT / "docs" / "BLK-067_ceb009-patch-approval-envelope-integrity-hardening-boundary.md"
BLK068 = ROOT / "docs" / "BLK-068_ceb009-patch-execution-preflight-refusal-boundary.md"
BLK069 = ROOT / "docs" / "BLK-069_ceb009-patch-execution-authority-request-boundary.md"
BLK070 = ROOT / "docs" / "BLK-070_ceb009-patch-execution-approval-capture-and-run-boundary.md"
BLK071 = ROOT / "docs" / "BLK-071_ceb009-fresh-target-patch-execution-boundary.md"
BLK072 = ROOT / "docs" / "BLK-072_blk-test-kuronode-workspace-read-only-pilot-request-boundary.md"
BLK073 = ROOT / "docs" / "BLK-073_blk-test-kuronode-workspace-exact-target-approval-envelope-boundary.md"
BLK074 = ROOT / "docs" / "BLK-074_blk-test-kuronode-workspace-read-only-pilot-runtime-boundary.md"
BLK075 = ROOT / "docs" / "BLK-075_blk-test-kuronode-lifecycle-cleanup-remediation-boundary.md"
BLK076 = ROOT / "docs" / "BLK-076_kuronode-lifecycle-cleanup-patch-approval-envelope-boundary.md"
BLK077 = ROOT / "docs" / "BLK-077_blk-system-post-078-roadmap.md"
BLK078 = ROOT / "docs" / "BLK-078_tactical-standard-profile-architecture.md"
BLK079 = ROOT / "docs" / "BLK-079_post-078-current-state-authority-index.md"
BLK080 = ROOT / "docs" / "BLK-080_tactical-standard-profile-registry-and-layer-b-extraction.md"
BLK081 = ROOT / "docs" / "BLK-081_target-repo-execution-governance-pattern.md"
BLK082 = ROOT / "docs" / "BLK-082_blk058-mechanical-enforcement-upgrade.md"
BLK083 = ROOT / "docs" / "BLK-083_beo-publication-decision-package-pilot-request.md"
BLK084 = ROOT / "docs" / "BLK-084_post-083-frontier-selection-gate-refresh.md"
BLK085 = ROOT / "docs" / "BLK-085_beo-publication-pilot-execution-request-gate.md"
BLK086 = ROOT / "docs" / "BLK-086_beo-publication-pilot-approval-decision.md"
BLK087 = ROOT / "docs" / "BLK-087_exact-beo-publication-pilot-execution.md"
BLK088 = ROOT / "docs" / "BLK-088_rtm-authority-request-after-local-beo-pilot-prerequisites.md"
BLK089 = ROOT / "docs" / "BLK-089_rtm-authority-approval-decision-capture.md"
BLK090 = ROOT / "docs" / "BLK-090_exact-local-rtm-generation-pilot.md"
BLK091 = ROOT / "docs" / "BLK-091_rtm-drift-rejection-authority-request.md"
BLK092 = ROOT / "docs" / "BLK-092_post-091-roadmap-current-state-reconciliation.md"
BLK093 = ROOT / "docs" / "BLK-093_rtm-drift-rejection-approval-decision-capture.md"
BLK094 = ROOT / "docs" / "BLK-094_post-093-roadmap-rtm-ladder-alignment.md"
BLK095 = ROOT / "docs" / "BLK-095_exact-local-rtm-drift-rejection-execution.md"
BLK096 = ROOT / "docs" / "BLK-096_post-095-local-rtm-ladder-reconciliation.md"
BLK097 = ROOT / "docs" / "BLK-097_bounded-blk-test-evidence-refresh-exact-target-frontier.md"
BLK098 = ROOT / "docs" / "BLK-098_beo-publication-prerequisite-request-after-evidence-refresh.md"
BLK099 = ROOT / "docs" / "BLK-099_external-beo-publication-approval-decision.md"
BLK100 = ROOT / "docs" / "BLK-100_external-beo-publication-execution.md"
BLK101 = ROOT / "docs" / "BLK-101_rtm-trace-closure-authority-request-after-external-beo.md"
BLK102 = ROOT / "docs" / "BLK-102_rtm-trace-closure-approval-decision-capture.md"
BLK103 = ROOT / "docs" / "BLK-103_exact-local-rtm-trace-closure-execution.md"
BLK104 = ROOT / "docs" / "BLK-104_post-103-current-state-reconciliation-and-frontier-selection-gate.md"
BLK105 = ROOT / "docs" / "BLK-105_root-doctrine-post-103-reconciliation.md"
BLK112 = ROOT / "docs" / "BLK-112_structured-validation-profile-argv-hardening.md"
BLK113 = ROOT / "docs" / "BLK-113_validation-trust-boundary-and-capability-policy.md"
BLK114 = ROOT / "docs" / "BLK-114_blk-pipe-report-evidence-hardening.md"
BLK115 = ROOT / "docs" / "BLK-115_production-hardening-reconciliation-gate.md"
BLK116 = ROOT / "docs" / "BLK-116_blk-req-legislative-gateway-contract.md"
BLK117 = ROOT / "docs" / "BLK-117_version-aware-staging-linter.md"
BLK118 = ROOT / "docs" / "BLK-118_staging-intake-draft-writer.md"
BLK119 = ROOT / "docs" / "BLK-119_canonical-version-hash-engine.md"
BLK120 = ROOT / "docs" / "BLK-120_hitl-baseline-promotion.md"
BLK109 = ROOT / "docs" / "BLK-109_protected-exact-root-directory-hardening.md"
BLK110 = ROOT / "docs" / "BLK-110_exit-code-taxonomy-split.md"
BLK111 = ROOT / "docs" / "BLK-111_doctrine-gate-coverage-and-runbook-vocabulary.md"
SPRINT097_EVIDENCE = ROOT / "docs" / "outcomes" / "BLK-SYSTEM-097_runtime-evidence.json"
SPRINT087_CLOSEOUT = ROOT / "docs" / "outcomes" / "BLK-SYSTEM-087_sprint-closeout.md"
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
    LEAN_DOC_RETIRED_MARKER_GATES = {
        "test_blk003_escalation_is_current_boundary_safe",
        "test_sprint018_exit3_and_revert_boundaries_are_active_doctrine",
        "test_sprint019_beo_authority_wording_is_draft_or_future_only",
        "test_sprint019_blk020_exception_overlay_preserves_disabled_authority",
        "test_sprint020_validation_profile_boundary_preserves_go_authority",
        "test_sprint021_python_adapter_policy_boundary_preserves_go_authority",
        "test_sprint079_post_078_current_state_authority_index_refresh_boundary",
        "test_sprint080_completion_updates_current_roadmap_and_next_sprint_to_081",
        "test_sprint081_completion_updates_current_roadmap_and_next_sprint_to_082",
        "test_sprint082_completion_routes_to_historical_sprint083_selection",
        "test_sprint083_completion_requires_explicit_publication_pilot_approval",
        "test_sprint084_completion_preserves_post083_frontier_authority_boundary",
        "test_sprint085_completion_preserves_publication_pilot_authority_boundary",
        "test_sprint086_completion_preserves_approval_decision_not_execution_boundary",
        "test_sprint087_completion_updates_current_state_without_rtm_authority",
        "test_sprint088_completion_updates_current_state_without_rtm_generation_authority",
        "test_sprint091_completion_updates_current_state_after_rtm_sequence",
        "test_sprint092_post091_reconciliation_preserves_no_approval_capture",
        "test_sprint093_rtm_drift_rejection_approval_capture_preserves_no_execution",
        "test_sprint094_post093_cleanup_aligns_local_pilot_ladder_before_execution",
        "test_sprint095_exact_local_rtm_drift_rejection_execution_is_local_only",
        "test_sprint096_post095_reconciliation_closes_local_ladder_without_runtime_authority",
        "test_sprint097_bounded_blk_test_evidence_refresh_is_one_run_evidence_only",
        "test_sprint098_beo_publication_prerequisite_request_after_evidence_refresh_is_review_only",
        "test_sprint099_external_beo_publication_approval_decision_capture_is_not_publication_execution",
        "test_sprint100_external_beo_publication_execution_boundary_and_adjacent_denials",
        "test_sprint101_102_103_rtm_trace_closure_ladder_boundaries_and_denials",
        "test_sprint104_post103_roadmap_current_state_reconciliation_boundary_and_completion_milestones",
        "test_sprint105_root_doctrine_post103_reconciliation_markers",
        "test_sprint111_blk_test_functional_module_warning_is_operator_visible",
        "test_sprint111_post103_frontier_markers_replace_stale_go_no_read_frontier",
        "test_sprint115_production_hardening_bridge_markers_and_next_frontier_are_pinned",
        "test_sprint119_blk_req_gateway_foundation_markers_and_next_frontier_are_pinned",
    }

    def setUp(self):
        if (
            self._testMethodName in self.LEAN_DOC_RETIRED_MARKER_GATES
            and BLK077.exists()
            and "LEAN_DOCUMENTATION_MODEL_ACTIVE" in BLK077.read_text()
        ):
            self.skipTest(
                "Retired by BLK-SYSTEM-121 lean documentation model; "
                "historical sprint marker gates must not force BLK-077 or BLK-001..006 bloat."
            )

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
                "Sprint-019-era draft-only/design-only fixture language remains historical/local-fixture lineage",
                "PUBLISHED_EXTERNAL_BEO_RECORD",
                "record-only external BEO publication evidence",
                "signer/storage/ledger publication remains disabled",
                "RTM generation remains disabled",
            ],
            BLK003: [
                "Historical Sprint-019-era local handling used draft-only BEO fixture projection",
                "PUBLISHED_EXTERNAL_BEO_RECORD",
                "record-only external BEO publication evidence",
                "signer/storage/ledger publication remains disabled",
                "production/reusable `blk-link`",
                "future authoritative publication remain separately authorized future frontiers",
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
            "trusted absolute paths",
            "canonical BLK-System repository root",
            "process-output byte gate",
            "scrubbed environment",
            "Persistent doctrine gate marker: BLK-SYSTEM-032 pins advisory fixed-profile health-check runner only",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-034 boundary markers missing: {missing}")

    def test_sprint033_health_check_profile_expansion_boundary_preserves_advisory_only_authority(self):
        self.assertTrue(BLK035.exists(), "BLK-035 health-check profile expansion boundary missing")
        text = BLK035.read_text()
        required = [
            "Track I health-check profile expansion boundary",
            "Active pilot boundary — expanded local advisory fixed-profile execution only",
            "Track I — Operator UX, observability, and escalation",
            "Track J — Security, sandbox, and capability hardening",
            "BLK-024 L4 pilot runtime for local fixed profiles only",
            "not L5 production authority",
            "HEALTH_CHECK_PROFILE_EXPANSION_ADVISORY_ONLY",
            "PYTHON_UNITTEST_DISCOVERY_PROFILE_ADVISORY_ONLY",
            "GO_TEST_ALL_PROFILE_ADVISORY_ONLY",
            "GO_VET_ALL_PROFILE_ADVISORY_ONLY",
            "TRUSTED_ABSOLUTE_EXECUTABLES_ONLY",
            "CANONICAL_REPO_ROOT_REQUIRED",
            "PROCESS_OUTPUT_BYTE_GATE_REQUIRED",
            "PYTHON_BYTECODE_CACHE_OUTSIDE_REPO_REQUIRED",
            "WORKSPACE_STATUS_CHANGE_OBSERVED_NOT_SOURCE_MUTATION_PROOF",
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
            "python_unittest_discovery",
            "go_test_all",
            "go_vet_all",
            "full Python discovery",
            "go test ./...",
            "go vet ./...",
            "trusted absolute executables",
            "canonical BLK-System repository root",
            "health-check PASS remains advisory",
            "Persistent doctrine gate marker: BLK-SYSTEM-033 pins fixed-profile health-check expansion only",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-035 boundary markers missing: {missing}")

    def test_sprint034_health_check_sandbox_side_effect_boundary_preserves_honest_observation(self):
        self.assertTrue(BLK036.exists(), "BLK-036 health-check sandbox/side-effect boundary missing")
        text = BLK036.read_text()
        required = [
            "Track I health-check sandbox and side-effect observation boundary",
            "Active pilot boundary — local advisory side-effect observation only",
            "Track I — Operator UX, observability, and escalation",
            "Track J — Security, sandbox, and capability hardening",
            "BLK-024 L4 pilot runtime for local fixed profiles only",
            "not L5 production authority",
            "HEALTH_CHECK_SANDBOX_SIDE_EFFECT_OBSERVATION_BOUNDARY",
            "RUNNER_TEMP_CONTAINMENT_OUTSIDE_REPO",
            "PYTHON_BYTECODE_CACHE_PER_RUN_OUTSIDE_REPO",
            "PROCESS_GROUP_TIMEOUT_CLEANUP_REQUIRED",
            "REPO_CACHE_ARTIFACT_OBSERVATION_REQUIRED",
            "GIT_STATUS_BEFORE_AFTER_OBSERVATION_REQUIRED",
            "OBSERVED_SIDE_EFFECTS_BLOCK_ADVISORY_PASS",
            "NO_PRODUCTION_SANDBOX_CGROUP_VM_CLAIM",
            "NO_NETWORK_FIREWALL_CLAIM",
            "NO_HOST_SECRET_ISOLATION_CLAIM",
            "NO_NEW_PROFILE_IDS",
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
            "runner-owned temporary directories outside the repository",
            "repo-local cache artifacts block advisory PASS",
            "process-group timeout cleanup",
            "health-check PASS remains advisory",
            "Persistent doctrine gate marker: BLK-SYSTEM-034 pins sandbox and side-effect observation only",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-036 boundary markers missing: {missing}")

    def test_sprint035_health_check_isolated_workspace_boundary_preserves_advisory_only_scope(self):
        self.assertTrue(BLK037.exists(), "BLK-037 isolated health-check workspace boundary missing")
        text = BLK037.read_text()
        required = [
            "Track I health-check isolated workspace execution boundary",
            "Active pilot boundary — optional local isolated-workspace advisory execution only",
            "Track I — Operator UX, observability, and escalation",
            "Track J — Security, sandbox, and capability hardening",
            "BLK-024 L4 pilot runtime for local fixed profiles only",
            "not L5 production authority",
            "HEALTH_CHECK_ISOLATED_WORKSPACE_EXECUTION_BOUNDARY",
            "ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO",
            "SOURCE_REPO_NOT_EXECUTION_CWD",
            "PROTECTED_BLK_REQ_PATHS_EXCLUDED_FROM_COPY",
            "DOT_GIT_EXCLUDED_FROM_COPY",
            "SOURCE_REPO_STATUS_BEFORE_AFTER_OBSERVATION_REQUIRED",
            "SOURCE_REPO_CACHE_OBSERVATION_REQUIRED",
            "ISOLATED_WORKSPACE_REMOVAL_REQUIRED",
            "GIT_STATUS_PROFILE_SOURCE_REPO_ONLY",
            "NO_NEW_PROFILE_IDS",
            "NO_ARBITRARY_SHELL",
            "NO_NETWORK_MODEL_CYBER_TOOLING",
            "NO_PACKAGE_MANAGER",
            "NO_GIT_MUTATION",
            "NO_SOURCE_MUTATION",
            "NO_PROTECTED_BODY_READ",
            "NO_PROTECTED_BODY_COPY",
            "NO_ACTIVE_VAULT_SCAN",
            "NO_BEO_PUBLICATION",
            "NO_RTM_GENERATION",
            "NO_DRIFT_REJECTION",
            "NO_PRODUCTION_SANDBOX_CGROUP_VM_CLAIM",
            "NO_NETWORK_FIREWALL_CLAIM",
            "NO_HOST_SECRET_ISOLATION_CLAIM",
            "NOT_PRODUCTION_HEALTH_CHECK_AUTHORITY",
            "isolated workspace PASS remains advisory",
            "Persistent doctrine gate marker: BLK-SYSTEM-035 pins isolated-workspace execution only",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-037 boundary markers missing: {missing}")

    def test_sprint036_health_check_git_metadata_fixture_boundary_preserves_isolated_advisory_scope(self):
        self.assertTrue(BLK038.exists(), "BLK-038 Git metadata fixture boundary missing")
        text = BLK038.read_text()
        required = [
            "Track I health-check Git metadata fixture boundary",
            "Active pilot boundary — isolated Git metadata fixture advisory evidence only",
            "Track I — Operator UX, observability, and escalation",
            "Track J — Security, sandbox, and capability hardening",
            "BLK-024 L4 pilot runtime for local fixed profiles only",
            "not L5 production authority",
            "HEALTH_CHECK_GIT_METADATA_FIXTURE_BOUNDARY",
            "GIT_STATUS_ISOLATED_METADATA_FIXTURE",
            "SOURCE_GIT_METADATA_READ_ONLY",
            "GIT_OPTIONAL_LOCKS_DISABLED",
            "GIT_STATUS_CWD_IS_ISOLATED_WORKSPACE",
            "GIT_DIR_AND_WORK_TREE_EXPLICIT",
            "DOT_GIT_NOT_COPIED",
            "SYNTHETIC_GIT_HISTORY_FORBIDDEN",
            "NO_CLONE_OR_WORKTREE_SETUP",
            "NO_NEW_PROFILE_IDS",
            "NO_ARBITRARY_SHELL",
            "NO_NETWORK_MODEL_CYBER_TOOLING",
            "NO_PACKAGE_MANAGER",
            "NO_GIT_MUTATION",
            "NO_SOURCE_MUTATION",
            "NO_PROTECTED_BODY_READ",
            "NO_PROTECTED_BODY_COPY",
            "NO_ACTIVE_VAULT_SCAN",
            "NO_BEO_PUBLICATION",
            "NO_RTM_GENERATION",
            "NO_DRIFT_REJECTION",
            "NO_PRODUCTION_SANDBOX_CGROUP_VM_CLAIM",
            "NO_NETWORK_FIREWALL_CLAIM",
            "NO_HOST_SECRET_ISOLATION_CLAIM",
            "NOT_PRODUCTION_HEALTH_CHECK_AUTHORITY",
            "health-check PASS remains advisory",
            "Persistent doctrine gate marker: BLK-SYSTEM-036 pins Git metadata fixture only",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-038 boundary markers missing: {missing}")

    def test_sprint037_health_check_escalation_package_boundary_preserves_advisory_scope(self):
        self.assertTrue(BLK039.exists(), "BLK-039 health-check escalation package boundary missing")
        text = BLK039.read_text()
        required = [
            "Track I health-check escalation package boundary",
            "Active pilot boundary — advisory health-check evidence packaging only",
            "Track I — Operator UX, observability, and escalation",
            "Track J — Security, sandbox, and capability hardening",
            "BLK-024 L4 local pilot evidence packaging",
            "not L5 production authority",
            "HEALTH_CHECK_ESCALATION_PACKAGE_ADVISORY_ONLY",
            "HEALTH_CHECK_PASS_GRANTS_NO_AUTHORITY",
            "ADVISORY_PASS",
            "FAILED_VERIFICATION_OR_BROKEN_CODE",
            "POLICY_OR_ENVIRONMENT_BLOCKED",
            "UNKNOWN_OR_MALFORMED_HEALTH_CHECK_EVIDENCE",
            "raw_evidence_embedded: false",
            "NO_NEW_PROFILE_IDS",
            "NO_SUBPROCESS_START_FROM_PACKAGE_HELPER",
            "NO_ARBITRARY_SHELL",
            "NO_NETWORK_MODEL_CYBER_TOOLING",
            "NO_PACKAGE_MANAGER",
            "NO_GIT_MUTATION",
            "NO_SOURCE_MUTATION",
            "NO_PROTECTED_BODY_READ",
            "NO_PROTECTED_BODY_COPY",
            "NO_ACTIVE_VAULT_SCAN",
            "NO_BEO_PUBLICATION",
            "NO_RTM_GENERATION",
            "NO_DRIFT_REJECTION",
            "NO_PRODUCTION_SANDBOX_CGROUP_VM_CLAIM",
            "NO_NETWORK_FIREWALL_CLAIM",
            "NO_HOST_SECRET_ISOLATION_CLAIM",
            "NOT_PRODUCTION_HEALTH_CHECK_AUTHORITY",
            "Persistent doctrine gate marker: BLK-SYSTEM-037 pins health-check escalation package advisory-only evidence packaging",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-039 boundary markers missing: {missing}")

    def test_sprint038_codex_deterministic_invocation_profile_boundary_denies_live_authority(self):
        self.assertTrue(BLK040.exists(), "BLK-040 Codex deterministic invocation profile boundary missing")
        text = BLK040.read_text()
        required = [
            "Codex deterministic invocation profile boundary",
            "Active fixture boundary — deterministic Codex invocation profile construction only",
            "Track I — Operator UX, observability, and escalation",
            "Track J — Security, sandbox, and capability hardening",
            "Track C — BLK-pipe blast shield and forge",
            "BLK-024 L1 fixture/local implementation plus L0 doctrine boundary",
            "not L5 production authority",
            "CODEX_DETERMINISTIC_INVOCATION_PROFILE_FIXTURE_ONLY",
            "CODEX_AMBIENT_FEATURES_DISABLED",
            "CODEX_PROFILE_BUILDER_STARTS_NO_SUBPROCESS",
            "CODEX_JSONL_EVENTS_ADVISORY_ONLY",
            "CODEX_FINAL_MESSAGE_ARTIFACT_ADVISORY_ONLY",
            "CODEX_NATIVE_SANDBOX_NOT_TRUSTED_ON_THIS_HOST",
            "CODEX_PROFILE_GRANTS_NO_EXECUTION_AUTHORITY",
            "--ephemeral",
            "--ignore-user-config",
            "--ignore-rules",
            "--json",
            "--output-last-message",
            "--disable hooks",
            "--disable plugins",
            "--disable goals",
            "NO_LIVE_CODEX_EXECUTION_AUTHORITY",
            "NO_BLK_PIPE_DISPATCH_AUTHORITY",
            "NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY",
            "NO_PROTECTED_BODY_READ",
            "NO_PROTECTED_BODY_COPY",
            "NO_ACTIVE_VAULT_SCAN",
            "NO_BEO_PUBLICATION",
            "NO_RTM_GENERATION",
            "NO_DRIFT_REJECTION",
            "NO_NETWORK_MODEL_CYBER_TOOLING",
            "NO_PACKAGE_MANAGER",
            "NO_GIT_MUTATION",
            "NO_SOURCE_MUTATION",
            "NO_PRODUCTION_SANDBOX_CGROUP_VM_CLAIM",
            "NO_NETWORK_FIREWALL_CLAIM",
            "NO_HOST_SECRET_ISOLATION_CLAIM",
            "Persistent doctrine gate marker: BLK-SYSTEM-038 pins Codex deterministic invocation profile fixture-only scope",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-040 boundary markers missing: {missing}")

    def test_sprint039_codex_deterministic_dispatch_envelope_boundary_denies_live_authority(self):
        self.assertTrue(BLK041.exists(), "BLK-041 Codex deterministic dispatch envelope boundary missing")
        text = BLK041.read_text()
        required = [
            "Codex deterministic dispatch envelope boundary",
            "Active fixture boundary — deterministic Codex dispatch envelope construction only",
            "Track C — BLK-pipe blast shield and forge",
            "Track I — Operator UX, observability, and escalation",
            "Track J — Security, sandbox, and capability hardening",
            "BLK-024 L1 fixture/local implementation plus L0 doctrine boundary",
            "not L5 production authority",
            "CODEX_DETERMINISTIC_DISPATCH_ENVELOPE_FIXTURE_ONLY",
            "CODEX_DISPATCH_ENVELOPE_STARTS_NO_SUBPROCESS",
            "CODEX_DISPATCH_REQUIRES_APPROVAL_PROVENANCE",
            "CODEX_DISPATCH_REQUIRES_EXACT_FILE_BOUNDARIES",
            "CODEX_DISPATCH_REQUIRES_VALIDATION_GATES",
            "CODEX_DISPATCH_REQUIRES_FAILURE_CEILING",
            "CODEX_DISPATCH_REQUIRES_HOSTILE_AUDIT",
            "CODEX_DISPATCH_TELEMETRY_ADVISORY_ONLY",
            "CODEX_DISPATCH_GRANTS_NO_EXECUTION_AUTHORITY",
            "NO_LIVE_CODEX_EXECUTION_AUTHORITY",
            "NO_BLK_PIPE_DISPATCH_AUTHORITY",
            "NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY",
            "NO_PROTECTED_BODY_READ",
            "NO_PROTECTED_BODY_COPY",
            "NO_ACTIVE_VAULT_SCAN",
            "NO_BEO_PUBLICATION",
            "NO_RTM_GENERATION",
            "NO_DRIFT_REJECTION",
            "NO_NETWORK_MODEL_CYBER_TOOLING",
            "NO_PACKAGE_MANAGER",
            "NO_GIT_MUTATION",
            "NO_SOURCE_MUTATION",
            "NO_PRODUCTION_SANDBOX_CGROUP_VM_CLAIM",
            "NO_NETWORK_FIREWALL_CLAIM",
            "NO_HOST_SECRET_ISOLATION_CLAIM",
            "approval provenance",
            "exact file boundaries",
            "validation gates",
            "failure ceiling",
            "hostile audit",
            "operator escalation",
            "Persistent doctrine gate marker: BLK-SYSTEM-039 pins Codex deterministic dispatch envelope fixture-only scope",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-041 boundary markers missing: {missing}")

    def test_sprint040_codex_live_dispatch_readiness_gate_boundary_denies_execution_authority(self):
        self.assertTrue(BLK042.exists(), "BLK-042 Codex live dispatch readiness gate boundary missing")
        text = BLK042.read_text()
        required = [
            "Codex live-dispatch readiness gate boundary",
            "Active fail-closed fixture boundary — Codex live-dispatch readiness gate only",
            "Track A — Doctrine, alignment, and review gates",
            "Track C — BLK-pipe blast shield and forge",
            "Track I — Operator UX, observability, and escalation",
            "Track J — Security, sandbox, and capability hardening",
            "BLK-024 L1 fixture/local implementation plus L2 disabled/fail-closed transport semantics",
            "not L5 production authority",
            "CODEX_LIVE_DISPATCH_READINESS_GATE_FIXTURE_ONLY",
            "CODEX_LIVE_DISPATCH_GATE_FAILS_CLOSED",
            "CODEX_LIVE_DISPATCH_GATE_STARTS_NO_SUBPROCESS",
            "CODEX_LIVE_DISPATCH_GATE_REQUIRES_RUNTIME_APPROVAL",
            "CODEX_LIVE_DISPATCH_GATE_REQUIRES_BLK_PIPE_WIRING_PLAN",
            "CODEX_LIVE_DISPATCH_GATE_REQUIRES_CONTAINMENT_EVIDENCE",
            "CODEX_LIVE_DISPATCH_GATE_REQUIRES_VALIDATION_EXECUTION_PLAN",
            "CODEX_LIVE_DISPATCH_GATE_REQUIRES_TELEMETRY_PERSISTENCE_PLAN",
            "CODEX_LIVE_DISPATCH_GATE_REQUIRES_ROLLBACK_PLAN",
            "CODEX_LIVE_DISPATCH_GATE_REQUIRES_MONITORING_PLAN",
            "CODEX_LIVE_DISPATCH_GATE_REQUIRES_OPERATOR_CONTROLS",
            "CODEX_LIVE_DISPATCH_GATE_GRANTS_NO_EXECUTION_AUTHORITY",
            "READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION",
            "BLOCKED_NOT_AUTHORIZED",
            "NO_LIVE_CODEX_EXECUTION_AUTHORITY",
            "NO_BLK_PIPE_DISPATCH_AUTHORITY",
            "NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY",
            "NO_PROTECTED_BODY_READ",
            "NO_PROTECTED_BODY_COPY",
            "NO_ACTIVE_VAULT_SCAN",
            "NO_BEO_PUBLICATION",
            "NO_RTM_GENERATION",
            "NO_DRIFT_REJECTION",
            "NO_NETWORK_MODEL_CYBER_TOOLING",
            "NO_PACKAGE_MANAGER",
            "NO_GIT_MUTATION",
            "NO_SOURCE_MUTATION",
            "NO_PRODUCTION_SANDBOX_CGROUP_VM_CLAIM",
            "NO_NETWORK_FIREWALL_CLAIM",
            "NO_HOST_SECRET_ISOLATION_CLAIM",
            "runtime approval",
            "BLK-pipe wiring plan",
            "containment evidence",
            "validation execution plan",
            "telemetry persistence plan",
            "rollback plan",
            "monitoring plan",
            "operator controls",
            "Persistent doctrine gate marker: BLK-SYSTEM-040 pins Codex live-dispatch readiness gate fail-closed non-execution scope",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-042 boundary markers missing: {missing}")

    def test_sprint041_codex_live_dispatch_authority_request_disabled_adapter_boundary_denies_execution(self):
        self.assertTrue(BLK043.exists(), "BLK-043 Codex live dispatch authority request disabled adapter boundary missing")
        text = BLK043.read_text()
        required = [
            "Codex live-dispatch authority request disabled adapter boundary",
            "Active disabled/fail-closed boundary — Codex live-dispatch authority request package and disabled adapter only",
            "Track A — Doctrine, alignment, and review gates",
            "Track C — BLK-pipe blast shield and forge",
            "Track I — Operator UX, observability, and escalation",
            "Track J — Security, sandbox, and capability hardening",
            "BLK-024 L2 disabled/fail-closed transport with L1 fixture evidence and L0 doctrine boundary",
            "not L5 production authority",
            "CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_FIXTURE_ONLY",
            "CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_FIXTURE_ONLY",
            "CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_REQUIRES_READY_REVIEW",
            "CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_REQUIRES_SEPARATE_HUMAN_GRANT",
            "CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_FAILS_CLOSED",
            "CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_STARTS_NO_SUBPROCESS",
            "CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_CALLS_NO_CODEX",
            "CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_CALLS_NO_BLK_PIPE",
            "CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_GRANTS_NO_EXECUTION_AUTHORITY",
            "AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_EXECUTION",
            "DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED",
            "NO_LIVE_CODEX_EXECUTION_AUTHORITY",
            "NO_BLK_PIPE_DISPATCH_AUTHORITY",
            "NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY",
            "NO_PROTECTED_BODY_READ",
            "NO_PROTECTED_BODY_COPY",
            "NO_ACTIVE_VAULT_SCAN",
            "NO_BEO_PUBLICATION",
            "NO_RTM_GENERATION",
            "NO_DRIFT_REJECTION",
            "NO_NETWORK_MODEL_CYBER_TOOLING",
            "NO_PACKAGE_MANAGER",
            "NO_GIT_MUTATION",
            "NO_SOURCE_MUTATION",
            "NO_PRODUCTION_SANDBOX_CGROUP_VM_CLAIM",
            "NO_NETWORK_FIREWALL_CLAIM",
            "NO_HOST_SECRET_ISOLATION_CLAIM",
            "separate human grant",
            "ready review",
            "disabled adapter",
            "Persistent doctrine gate marker: BLK-SYSTEM-041 pins Codex live-dispatch authority request disabled-adapter non-execution scope",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-043 boundary markers missing: {missing}")

    def test_sprint042_codex_live_dispatch_execution_authority_design_gate_boundary_denies_execution(self):
        self.assertTrue(BLK044.exists(), "BLK-044 Codex live dispatch execution authority design gate boundary missing")
        text = BLK044.read_text()
        required = [
            "Codex live-dispatch execution authority design gate",
            "Active design/fixture boundary — Codex live-dispatch execution-authority design gate only",
            "Track A — Doctrine, alignment, and review gates",
            "Track C — BLK-pipe blast shield and forge",
            "Track I — Operator UX, observability, and escalation",
            "Track J — Security, sandbox, and capability hardening",
            "BLK-024 L0 doctrine boundary plus L1 fixture/local implementation",
            "not L5 production authority",
            "CODEX_LIVE_DISPATCH_EXECUTION_AUTHORITY_DESIGN_GATE_FIXTURE_ONLY",
            "CODEX_EXECUTION_AUTHORITY_DESIGN_GATE_FAILS_CLOSED",
            "CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_AUTHORITY_REQUEST_PACKAGE",
            "CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_APPROVAL_ENVELOPE_CONTRACT",
            "CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_BLK_PIPE_INTEGRATION_CONTRACT",
            "CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_CONTAINMENT_CONTRACT",
            "CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_TELEMETRY_CONTRACT",
            "CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_ROLLBACK_CONTRACT",
            "CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_MONITORING_OPERATOR_CONTROL_CONTRACT",
            "CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_FAILURE_CEILING_CONTRACT",
            "CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_REPLAY_PROTECTION_CONTRACT",
            "CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_HOSTILE_AUDIT_CONTRACT",
            "CODEX_EXECUTION_AUTHORITY_DESIGN_GRANTS_NO_EXECUTION_AUTHORITY",
            "EXECUTION_AUTHORITY_DESIGN_READY_FOR_REVIEW_NOT_EXECUTION",
            "EXECUTION_AUTHORITY_DESIGN_BLOCKED",
            "NO_LIVE_CODEX_EXECUTION_AUTHORITY",
            "NO_BLK_PIPE_DISPATCH_AUTHORITY",
            "NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY",
            "NO_PROTECTED_BODY_READ",
            "NO_PROTECTED_BODY_COPY",
            "NO_ACTIVE_VAULT_SCAN",
            "NO_BEO_PUBLICATION",
            "NO_RTM_GENERATION",
            "NO_DRIFT_REJECTION",
            "NO_NETWORK_MODEL_CYBER_TOOLING",
            "NO_PACKAGE_MANAGER",
            "NO_GIT_MUTATION",
            "NO_SOURCE_MUTATION",
            "NO_PRODUCTION_SANDBOX_CGROUP_VM_CLAIM",
            "NO_NETWORK_FIREWALL_CLAIM",
            "NO_HOST_SECRET_ISOLATION_CLAIM",
            "approval envelope contract",
            "BLK-pipe integration contract",
            "containment contract",
            "telemetry contract",
            "rollback contract",
            "monitoring/operator controls contract",
            "failure ceiling contract",
            "replay protection contract",
            "hostile audit contract",
            "Persistent doctrine gate marker: BLK-SYSTEM-042 pins Codex live-dispatch execution-authority design-gate non-execution scope",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-044 boundary markers missing: {missing}")

    def test_blk045_is_retained_as_superseded_post_042_roadmap_lineage(self):
        self.assertTrue(BLK045.exists(), "BLK-045 post-042 roadmap missing")
        text = BLK045.read_text()
        required = [
            "Superseded by BLK-059",
            "Superseded roadmap guidance — retained for historical context, not sprint authority",
            "docs/BLK-059_blk-system-post-058-roadmap.md",
            "BLK-045 remains retained for strategic-fork lineage and post-042 historical context",
            "Fork A — Consolidation / Current-State Index",
            "Fork B — Codex Live-Dispatch Activation",
            "Fork C — Complete the Right Side of the V-Model",
            "BLK-044 is sufficient to request a decision; it is not itself execution permission.",
            "Do not pursue BEO publication before verification evidence is trustworthy.",
            "Do not pursue drift rejection before RTM ledger generation is proven.",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-045 superseded-roadmap lineage markers missing: {missing}")

    def test_blk059_controls_post_058_roadmap_selection_without_runtime_authority(self):
        self.assertTrue(BLK059.exists(), "BLK-059 post-058 roadmap missing")
        text = BLK059.read_text()
        required = [
            "Superseded roadmap guidance — retained for historical context, not current sprint authority",
            "BLK-059 superseded `docs/BLK-045_blk-system-post-042-roadmap.md`",
            "BLK-077 now supersedes BLK-059 for current roadmap selection after BLK-SYSTEM-078.",
            "BLK-024 remains retained for maturity-model lineage and historical post-BLK-SYSTEM-019 context.",
            "BLK-059 did not supersede or weaken BLK-001 through BLK-006.",
            "BLK-SYSTEM-052 produced one approved non-disposable L4 `run_ast_validation` PASS evidence artifact",
            "BLK-SYSTEM-054 created a deterministic authoritative BEO publication authority-request package under BLK-057.",
            "BLK-058 formalized the Kuronode TypeScript Power-of-Ten tactical standard.",
            "Publication completion intent",
            "Kuronode tactical quality intent",
            "Codex activation intent",
            "Trace-closure intent",
            "Workstream B — Kuronode TypeScript Power-of-Ten mechanical gates",
            "Workstream C — BEO publication approval envelope",
            "BLK-SYSTEM-055 — Authoritative BEO Publication Approval Envelope / Pilot Boundary",
            "BLK-SYSTEM-056 — Kuronode TypeScript Power-of-Ten Mechanical Gate Fixtures",
            "No actual authoritative BEO publication authority",
            "No Kuronode Power-of-Ten mechanical enforcement",
            "The default recommendation is **A first if V-model completion is the priority**, with **B as the strongest safety-hardening interlock before broader Kuronode tactical execution**.",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-059 current-roadmap markers missing: {missing}")

    def test_sprint055_beo_publication_approval_envelope_boundary_denies_publication_authority(self):
        self.assertTrue(BLK060.exists(), "BLK-060 BEO publication approval envelope boundary missing")
        text = BLK060.read_text()
        required = [
            "Authoritative BEO Publication Approval Envelope / Pilot Boundary",
            "Active approval-envelope boundary — human-review package and pilot-boundary only; not publication authority",
            "AUTHORITATIVE_BEO_PUBLICATION_APPROVAL_ENVELOPE_BOUNDARY",
            "AUTHORITATIVE_BEO_PUBLICATION_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_PUBLICATION",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_055_BEO_PUBLICATION_APPROVAL_ENVELOPE",
            "approval-envelope / pilot-boundary readiness only",
            "No authoritative BEO publication",
            "No runtime `PUBLISHED` BEO output",
            "No live publication approval capture",
            "No signer key material access",
            "No cryptographic signing",
            "No immutable storage writes",
            "No public ledger append or mutation",
            "No rollback, revocation, or supersession execution",
            "No runtime RTM generation or RTM drift rejection",
            "No active-vault hash comparison, coverage matrix, coverage claim, or drift decision",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No reusable BLK-test service startup",
            "No live Codex execution authority",
            "No arbitrary shell or caller-supplied commands",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
            "BLK-057 request-readiness is not publication approval and is not publication authority",
            "A future one-run publication pilot requires separate explicit human approval",
            "RTM generation and RTM drift rejection remain later separate authority boundaries",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-060 approval-envelope boundary markers missing: {missing}")
        forbidden_authority_claims = [
            "authorizes authoritative BEO publication",
            "publication authority is granted",
            "runtime `PUBLISHED` BEO output is enabled",
            "live publication approval capture is authorized",
            "signer key material access is authorized",
            "cryptographic signing is authorized",
            "immutable storage writes are authorized",
            "public ledger mutation is authorized",
            "RTM generation is authorized",
            "RTM drift rejection is authorized",
            "protected BLK-req body reads are authorized",
            "production BLK-test MCP authority is granted",
            "live Codex execution authority is granted",
        ]
        leaked = [claim for claim in forbidden_authority_claims if claim in text]
        self.assertEqual(leaked, [], f"BLK-060 contains forbidden authority claims: {leaked}")

    def test_sprint056_kuronode_power_of_ten_static_profile_boundary_denies_runtime_authority(self):
        self.assertTrue(BLK061.exists(), "BLK-061 Kuronode Power-of-Ten static profile boundary missing")
        text = BLK061.read_text()
        required = [
            "Kuronode TypeScript Power-of-Ten Static Profile Boundary",
            "Active fixture-only static validation profile boundary — not runtime execution authority",
            "KURONODE_TYPESCRIPT_POWER_OF_TEN_STATIC_PROFILE_BOUNDARY",
            "KURONODE_POWER_OF_TEN_STATIC_PROFILE_PASS_FIXTURE_ONLY",
            "KURONODE_POWER_OF_TEN_STATIC_PROFILE_BLOCKED_FIXTURE_ONLY",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_056_KURONODE_POWER_OF_TEN_STATIC_PROFILE",
            "fixture-only static profile contract",
            "No live Kuronode repository scan",
            "No source or Git mutation",
            "No live Codex execution",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No reusable BLK-test service startup",
            "No arbitrary shell or caller-supplied commands",
            "No TypeScript tooling, typechecker, linter, or formatter execution",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime RTM generation or RTM drift rejection",
            "Static profile PASS is evidence only and not source-mutation, BLK-test, BEO, RTM, Codex, or production authority",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-061 static-profile markers missing: {missing}")
        forbidden_claims = [
            "authorizes live Kuronode scanning",
            "authorizes source mutation",
            "authorizes live Codex execution",
            "authorizes TypeScript tooling execution",
            "authorizes production BLK-test MCP",
            "authorizes authoritative BEO publication",
            "authorizes runtime RTM generation",
            "authorizes package-manager execution",
            "authorizes protected BLK-req body reads",
        ]
        leaked = [claim for claim in forbidden_claims if claim in text]
        self.assertEqual(leaked, [], f"BLK-061 contains forbidden authority claims: {leaked}")

    def test_sprint057_kuronode_power_of_ten_validation_profile_registry_denies_runtime_authority(self):
        self.assertTrue(BLK062.exists(), "BLK-062 Kuronode Power-of-Ten validation-profile registry boundary missing")
        text = BLK062.read_text()
        required = [
            "Kuronode Power-of-Ten Validation Profile Registry Boundary",
            "Active fixture self-test validation-profile boundary — not live Kuronode validation authority",
            "KURONODE_POWER_OF_TEN_VALIDATION_PROFILE_REGISTRY_BOUNDARY",
            "kuronode-power-of-ten-static-fixture",
            "PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_kuronode_power_of_ten_static_profile -q",
            "KURONODE_POWER_OF_TEN_STATIC_FIXTURE_SELFTEST_PROFILE_REGISTERED",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_057_KURONODE_VALIDATION_PROFILE_REGISTRY",
            "Fixture self-test PASS is evidence only and not live Kuronode source validation",
            "No live Kuronode repository scan",
            "No TypeScript tooling, typechecker, linter, or formatter execution",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No source or Git mutation by the profile",
            "No live Codex execution",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No reusable BLK-test service startup",
            "No arbitrary shell or caller-supplied commands",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime RTM generation or RTM drift rejection",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-062 validation-profile registry markers missing: {missing}")
        forbidden_claims = [
            "authorizes live Kuronode validation",
            "authorizes live Kuronode scanning",
            "authorizes TypeScript tooling execution",
            "authorizes package-manager execution",
            "authorizes source mutation",
            "authorizes live Codex execution",
            "authorizes production BLK-test MCP",
            "authorizes authoritative BEO publication",
            "authorizes runtime RTM generation",
            "authorizes protected BLK-req body reads",
        ]
        leaked = [claim for claim in forbidden_claims if claim in text]
        self.assertEqual(leaked, [], f"BLK-062 contains forbidden authority claims: {leaked}")

    def test_sprint058_kuronode_gate_pilot_approval_envelope_denies_runtime_authority(self):
        self.assertTrue(BLK063.exists(), "BLK-063 Kuronode gate pilot approval-envelope boundary missing")
        text = BLK063.read_text()
        required = [
            "Kuronode Power-of-Ten Gate Pilot Approval Envelope Boundary",
            "Active non-runtime approval-envelope boundary — not live Kuronode gate pilot authority",
            "KURONODE_POWER_OF_TEN_GATE_PILOT_APPROVAL_ENVELOPE_BOUNDARY",
            "KURONODE_POWER_OF_TEN_GATE_PILOT_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_058_KURONODE_GATE_PILOT_APPROVAL_ENVELOPE",
            "kuronode-power-of-ten-static-fixture",
            "Future human review package only; not runtime approval",
            "No live Kuronode repository scan",
            "No live Kuronode source validation from this approval envelope",
            "No TypeScript tooling, typechecker, linter, or formatter execution",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No source or Git mutation by the gate",
            "No live Codex execution",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No reusable BLK-test service startup",
            "No arbitrary shell or caller-supplied commands",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime RTM generation or RTM drift rejection",
            "No active-vault hash comparison, coverage matrix, coverage claim, or drift decision",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-063 gate-pilot approval-envelope markers missing: {missing}")
        forbidden_claims = [
            "authorizes live Kuronode validation",
            "authorizes live Kuronode scanning",
            "authorizes the Kuronode gate pilot runtime",
            "authorizes TypeScript tooling execution",
            "authorizes package-manager execution",
            "authorizes source mutation",
            "authorizes live Codex execution",
            "authorizes production BLK-test MCP",
            "authorizes authoritative BEO publication",
            "authorizes runtime RTM generation",
            "authorizes protected BLK-req body reads",
        ]
        leaked = [claim for claim in forbidden_claims if claim in text]
        self.assertEqual(leaked, [], f"BLK-063 contains forbidden authority claims: {leaked}")

    def test_sprint059_kuronode_ceb009_static_gate_pilot_denies_runtime_authority(self):
        self.assertTrue(BLK064.exists(), "BLK-064 CEB_009 static gate pilot boundary missing")
        text = BLK064.read_text()
        required = [
            "Kuronode CEB_009 Power-of-Ten Static Gate Pilot Boundary",
            "Active static-fixture pilot boundary — findings-ready, not runtime validation authority",
            "KURONODE_POWER_OF_TEN_CEB009_STATIC_GATE_PILOT_BOUNDARY",
            "KURONODE_POWER_OF_TEN_CEB009_STATIC_GATE_PILOT_FINDINGS_READY_NOT_RUNTIME",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_059_KURONODE_CEB009_STATIC_GATE_PILOT",
            "CEB_009 static fixture material only; not a Kuronode source fix",
            "No live Kuronode repository scan",
            "No live Kuronode source validation from this static pilot",
            "No Electron launch, no headless smoke-test execution, and no wall-clock timeout wait",
            "No TypeScript tooling, typechecker, linter, or formatter execution",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No source or Git mutation by the gate",
            "No live Codex execution",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No reusable BLK-test service startup",
            "No arbitrary shell or caller-supplied commands",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime RTM generation or RTM drift rejection",
            "No active-vault hash comparison, coverage matrix, coverage claim, or drift decision",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-064 CEB_009 static gate pilot markers missing: {missing}")
        forbidden_claims = [
            "authorizes live Kuronode validation",
            "authorizes live Kuronode scanning",
            "authorizes Electron execution",
            "authorizes smoke-test execution",
            "authorizes TypeScript tooling execution",
            "authorizes package-manager execution",
            "authorizes source mutation",
            "authorizes live Codex execution",
            "authorizes production BLK-test MCP",
            "authorizes authoritative BEO publication",
            "authorizes runtime RTM generation",
            "authorizes protected BLK-req body reads",
        ]
        leaked = [claim for claim in forbidden_claims if claim in text]
        self.assertEqual(leaked, [], f"BLK-064 contains forbidden authority claims: {leaked}")

    def test_sprint060_kuronode_ceb009_remediation_packet_denies_patch_and_runtime_authority(self):
        self.assertTrue(BLK065.exists(), "BLK-065 CEB_009 remediation packet boundary missing")
        text = BLK065.read_text()
        required = [
            "Kuronode CEB_009 Remediation Packet Boundary",
            "Active remediation-packet boundary — ready for human review, not patched and not runtime validation authority",
            "KURONODE_POWER_OF_TEN_CEB009_REMEDIATION_PACKET_BOUNDARY",
            "KURONODE_POWER_OF_TEN_CEB009_REMEDIATION_PACKET_READY_NOT_PATCHED",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_060_KURONODE_CEB009_REMEDIATION_PACKET",
            "CEB_009 remediation packet fixture only; not a Kuronode source patch",
            "No Kuronode source or Git mutation",
            "No live Kuronode repository scan",
            "No live Kuronode source validation from this remediation packet",
            "No Electron launch, no headless smoke-test execution, and no wall-clock timeout wait",
            "No TypeScript tooling, typechecker, linter, or formatter execution",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No live Codex execution",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No reusable BLK-test service startup",
            "No arbitrary shell or caller-supplied commands",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime RTM generation or RTM drift rejection",
            "No active-vault hash comparison, coverage matrix, coverage claim, or drift decision",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
            "Remediation fragment guidance is not applied code",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-065 CEB_009 remediation packet markers missing: {missing}")
        forbidden_claims = [
            "authorizes Kuronode source mutation",
            "authorizes live Kuronode validation",
            "authorizes live Kuronode scanning",
            "authorizes Electron execution",
            "authorizes smoke-test execution",
            "authorizes TypeScript tooling execution",
            "authorizes package-manager execution",
            "authorizes live Codex execution",
            "authorizes production BLK-test MCP",
            "authorizes authoritative BEO publication",
            "authorizes runtime RTM generation",
            "authorizes protected BLK-req body reads",
        ]
        leaked = [claim for claim in forbidden_claims if claim in text]
        self.assertEqual(leaked, [], f"BLK-065 contains forbidden authority claims: {leaked}")

    def test_sprint061_kuronode_ceb009_patch_approval_envelope_denies_approval_patch_and_runtime_authority(self):
        self.assertTrue(BLK066.exists(), "BLK-066 CEB_009 patch approval envelope boundary missing")
        text = BLK066.read_text()
        required = [
            "Kuronode CEB_009 Patch Approval Envelope Boundary",
            "Active patch approval-envelope boundary — ready for human review, not approved, not patched, and not runtime validation authority",
            "KURONODE_POWER_OF_TEN_CEB009_PATCH_APPROVAL_ENVELOPE_BOUNDARY",
            "KURONODE_POWER_OF_TEN_CEB009_PATCH_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PATCHED",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_061_KURONODE_CEB009_PATCH_APPROVAL_ENVELOPE",
            "CEB_009 patch approval envelope fixture only; not approval to patch Kuronode",
            "No patch approval granted by this envelope",
            "No Kuronode source or Git mutation",
            "No live Kuronode repository scan",
            "No live Kuronode source validation from this patch approval envelope",
            "No Electron launch, no headless smoke-test execution, and no wall-clock timeout wait",
            "No TypeScript tooling, typechecker, linter, or formatter execution",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No live Codex execution",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No reusable BLK-test service startup",
            "No arbitrary shell or caller-supplied commands",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime RTM generation or RTM drift rejection",
            "No active-vault hash comparison, coverage matrix, coverage claim, or drift decision",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
            "Exact future target path: scripts/smoke_test.ts",
            "allowed_modified_files=[scripts/smoke_test.ts]",
            "allowed_new_files=[]",
            "Approval envelope is review evidence only until separate explicit human approval",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-066 CEB_009 patch approval envelope markers missing: {missing}")
        forbidden_claims = [
            "authorizes Kuronode source mutation",
            "authorizes patch application",
            "authorizes live Kuronode validation",
            "authorizes live Kuronode scanning",
            "authorizes Electron execution",
            "authorizes smoke-test execution",
            "authorizes TypeScript tooling execution",
            "authorizes package-manager execution",
            "authorizes live Codex execution",
            "authorizes production BLK-test MCP",
            "authorizes authoritative BEO publication",
            "authorizes runtime RTM generation",
            "authorizes protected BLK-req body reads",
        ]
        leaked = [claim for claim in forbidden_claims if claim in text]
        self.assertEqual(leaked, [], f"BLK-066 contains forbidden authority claims: {leaked}")

    def test_sprint062_ceb009_patch_approval_envelope_integrity_hardening_denies_forgery_and_runtime_authority(self):
        self.assertTrue(BLK067.exists(), "BLK-067 CEB_009 patch approval envelope integrity hardening boundary missing")
        text = BLK067.read_text()
        required = [
            "CEB_009 Patch Approval Envelope Integrity Hardening Boundary",
            "Active integrity-hardening boundary — upstream remediation packet hash is recomputed; review-only, not approved, not patched, and not runtime validation authority",
            "KURONODE_POWER_OF_TEN_CEB009_PATCH_APPROVAL_ENVELOPE_INTEGRITY_HARDENING_BOUNDARY",
            "KURONODE_POWER_OF_TEN_CEB009_PATCH_APPROVAL_ENVELOPE_INTEGRITY_HARDENED_UPSTREAM_HASH_RECOMPUTED",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_062_CEB009_PATCH_APPROVAL_ENVELOPE_INTEGRITY_HARDENING",
            "Upstream remediation packet hash must be recomputed from the submitted packet body excluding packet_hash",
            "Forged self-reported packet_hash values are not trusted",
            "Request remediation_packet_hash matching a forged upstream self-report is not sufficient",
            "Exact upstream excluded_authorities equality is required",
            "Recursive upstream authority-laundering rejection is required",
            "Compact, camelCase, PascalCase, ALLCAPS, acronym, URL-encoded, and double-encoded variants must be rejected",
            "No patch approval granted by this hardening",
            "No Kuronode source or Git mutation",
            "No live Kuronode repository scan",
            "No live Kuronode source validation from this hardening",
            "No Electron launch, no headless smoke-test execution, and no wall-clock timeout wait",
            "No TypeScript tooling, typechecker, linter, or formatter execution",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No live Codex execution",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No reusable BLK-test service startup",
            "No arbitrary shell or caller-supplied commands",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime RTM generation or RTM drift rejection",
            "No active-vault hash comparison, coverage matrix, coverage claim, or drift decision",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
            "Approval envelope remains review evidence only until separate explicit human approval",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-067 CEB_009 integrity-hardening markers missing: {missing}")
        forbidden_claims = [
            "trusts self-reported packet_hash",
            "authorizes Kuronode source mutation",
            "authorizes patch application",
            "authorizes live Kuronode validation",
            "authorizes live Kuronode scanning",
            "authorizes Electron execution",
            "authorizes smoke-test execution",
            "authorizes TypeScript tooling execution",
            "authorizes package-manager execution",
            "authorizes live Codex execution",
            "authorizes production BLK-test MCP",
            "authorizes authoritative BEO publication",
            "authorizes runtime RTM generation",
            "authorizes protected BLK-req body reads",
        ]
        leaked = [claim for claim in forbidden_claims if claim in text]
        self.assertEqual(leaked, [], f"BLK-067 contains forbidden authority claims: {leaked}")

    def test_sprint063_ceb009_patch_execution_preflight_refusal_denies_inherited_patch_authority(self):
        self.assertTrue(BLK068.exists(), "BLK-068 CEB_009 patch execution preflight refusal boundary missing")
        text = BLK068.read_text()
        required = [
            "CEB_009 Patch Execution Preflight Refusal Boundary",
            "Active preflight-refusal boundary — blocked pending explicit human patch approval; not executed, not patched, and not runtime validation authority",
            "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_PREFLIGHT_REFUSAL_BOUNDARY",
            "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_PREFLIGHT_BLOCKED_PENDING_HUMAN_APPROVAL_NOT_EXECUTED",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_063_CEB009_PATCH_EXECUTION_PREFLIGHT_REFUSAL",
            "Review-ready approval envelope status is not patch approval",
            "Integrity hardening marker is not patch approval",
            "Blocked preflight result is not execution success",
            "Explicit human patch approval is required before any future patch runner",
            "No BLK-pipe invocation",
            "No Kuronode source or Git mutation",
            "No live Kuronode repository scan",
            "No live Kuronode source validation",
            "No Electron launch, no headless smoke-test execution, and no wall-clock timeout wait",
            "No TypeScript tooling, typechecker, linter, formatter, or package-manager execution",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No live Codex execution",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No reusable BLK-test service startup",
            "No arbitrary shell or caller-supplied commands",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No CEO_009 publication",
            "No runtime RTM generation or RTM drift rejection",
            "No active-vault hash comparison, coverage matrix, coverage claim, or drift decision",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-068 CEB_009 preflight-refusal markers missing: {missing}")
        forbidden_claims = [
            "authorizes Kuronode source mutation",
            "authorizes patch application",
            "authorizes live Kuronode validation",
            "authorizes live Kuronode scanning",
            "authorizes BLK-pipe invocation",
            "authorizes Electron execution",
            "authorizes smoke-test execution",
            "authorizes TypeScript tooling execution",
            "authorizes package-manager execution",
            "authorizes live Codex execution",
            "authorizes production BLK-test MCP",
            "authorizes authoritative BEO publication",
            "authorizes CEO_009 publication",
            "authorizes runtime RTM generation",
            "authorizes protected BLK-req body reads",
        ]
        leaked = [claim for claim in forbidden_claims if claim in text]
        self.assertEqual(leaked, [], f"BLK-068 contains forbidden authority claims: {leaked}")

    def test_sprint064_ceb009_patch_execution_authority_request_denies_approval_and_execution_authority(self):
        self.assertTrue(BLK069.exists(), "BLK-069 CEB_009 patch execution authority request boundary missing")
        text = BLK069.read_text()
        required = [
            "CEB_009 Patch Execution Authority Request Boundary",
            "Active authority-request boundary — ready for human decision only; not approved, not executed, not patched, and not runtime validation authority",
            "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_AUTHORITY_REQUEST_BOUNDARY",
            "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_AUTHORITY_REQUEST_READY_FOR_HUMAN_DECISION_NOT_EXECUTED",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_064_CEB009_PATCH_EXECUTION_AUTHORITY_REQUEST",
            "Authority-request readiness is not patch approval",
            "Blocked preflight evidence is not patch approval",
            "Future validation profile identifiers are not executable commands",
            "Human patch execution approval must be captured by a separate future sprint before any BLK-pipe invocation",
            "No approval captured by BLK-SYSTEM-064",
            "No BLK-pipe invocation",
            "No Kuronode source or Git mutation",
            "No live Kuronode repository scan",
            "No live Kuronode source validation",
            "No Electron launch, no headless smoke-test execution, and no wall-clock timeout wait",
            "No TypeScript tooling, typechecker, linter, formatter, or package-manager execution",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No live Codex execution",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No reusable BLK-test service startup",
            "No arbitrary shell or caller-supplied commands",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No CEO_009 publication",
            "No runtime RTM generation or RTM drift rejection",
            "No active-vault hash comparison, coverage matrix, coverage claim, or drift decision",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-069 CEB_009 authority-request markers missing: {missing}")
        forbidden_claims = [
            "authorizes Kuronode source mutation",
            "authorizes patch application",
            "authorizes approval capture",
            "authorizes live Kuronode validation",
            "authorizes live Kuronode scanning",
            "authorizes BLK-pipe invocation",
            "authorizes Electron execution",
            "authorizes smoke-test execution",
            "authorizes TypeScript tooling execution",
            "authorizes package-manager execution",
            "authorizes live Codex execution",
            "authorizes production BLK-test MCP",
            "authorizes authoritative BEO publication",
            "authorizes CEO_009 publication",
            "authorizes runtime RTM generation",
            "authorizes protected BLK-req body reads",
        ]
        leaked = [claim for claim in forbidden_claims if claim in text]
        self.assertEqual(leaked, [], f"BLK-069 contains forbidden authority claims: {leaked}")

    def test_sprint065_ceb009_patch_execution_approval_capture_boundary_blocks_target_drift(self):
        self.assertTrue(BLK070.exists(), "BLK-070 CEB_009 patch execution approval capture boundary missing")
        text = BLK070.read_text()
        required = [
            "CEB_009 Patch Execution Approval Capture and Run Boundary",
            "Active exact-target approval-capture boundary",
            "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_APPROVAL_CAPTURE_AND_RUN_BOUNDARY",
            "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_READY_FOR_ONE_EXACT_BLK_PIPE_PATCH_ATTEMPT",
            "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_BLOCKED_TARGET_DRIFT_NOT_EXECUTED",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_065_CEB009_PATCH_EXECUTION_APPROVAL_CAPTURE_AND_RUN",
            "Operator approval captured in BLK-SYSTEM-065 is exact-target approval only",
            "Approval capture is not retargeting authority",
            "A local HEAD match is insufficient if the observed remote target branch differs from the approved target SHA",
            "TARGET_HEAD_DRIFT_REQUIRES_FRESH_APPROVAL",
            "No retargeting to `70b6062b92cf61c12bf190f92dc6b45ea4dcd438` or any other SHA without fresh approval",
            "No Kuronode remote push",
            "No source or Git mutation outside exact BLK-pipe allowlists",
            "No live Codex execution",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No Electron launch, no headless smoke-test execution, and no wall-clock timeout wait",
            "No TypeScript tooling, typechecker, linter, formatter, or package-manager execution",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No CEO_009 publication",
            "No runtime RTM generation or RTM drift rejection",
            "No active-vault hash comparison, coverage matrix, coverage claim, or drift decision",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-070 CEB_009 approval-capture markers missing: {missing}")
        forbidden_claims = [
            "authorizes retargeting",
            "authorizes live Codex execution",
            "authorizes production BLK-test MCP",
            "authorizes Electron execution",
            "authorizes smoke-test execution",
            "authorizes TypeScript tooling execution",
            "authorizes package-manager execution",
            "authorizes authoritative BEO publication",
            "authorizes CEO_009 publication",
            "authorizes runtime RTM generation",
            "authorizes protected BLK-req body reads",
            "authorizes Kuronode remote push",
        ]
        leaked = [claim for claim in forbidden_claims if claim in text]
        self.assertEqual(leaked, [], f"BLK-070 contains forbidden authority claims: {leaked}")

    def test_sprint066_ceb009_fresh_target_patch_execution_boundary_denies_adjacent_authority(self):
        self.assertTrue(BLK071.exists(), "BLK-071 CEB_009 fresh-target patch execution boundary missing")
        text = BLK071.read_text()
        required = [
            "CEB_009 Fresh-Target Patch Execution Boundary",
            "Active exact-target execution boundary",
            "KURONODE_POWER_OF_TEN_CEB009_FRESH_TARGET_PATCH_EXECUTION_BOUNDARY",
            "KURONODE_POWER_OF_TEN_CEB009_FRESH_TARGET_PATCH_EXECUTION_READY_FOR_BLK_PIPE",
            "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_BLK_PIPE_COMMITTED_NOT_PUSHED",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_066_CEB009_FRESH_TARGET_PATCH_EXECUTION",
            "70b6062b92cf61c12bf190f92dc6b45ea4dcd438",
            "No Kuronode remote push",
            "No source or Git mutation outside exact BLK-pipe allowlists",
            "No retargeting to any SHA other than `70b6062b92cf61c12bf190f92dc6b45ea4dcd438`",
            "No live Codex execution",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No Electron launch, no headless smoke-test execution, and no wall-clock timeout wait",
            "No TypeScript tooling, typechecker, linter, formatter, or package-manager execution",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No CEO_009 publication",
            "No runtime RTM generation or RTM drift rejection",
            "No active-vault hash comparison, coverage matrix, coverage claim, or drift decision",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-071 fresh-target patch markers missing: {missing}")

    def test_sprint043_current_state_authority_index_boundary_denies_runtime_authority(self):
        self.assertTrue(BLK046.exists(), "BLK-046 current-state authority index missing")
        text = BLK046.read_text()
        required = [
            "BLK-System Current-State Authority Index",
            "BLK-046 is retained as historical current-state authority index lineage",
            "BLK_SYSTEM_CURRENT_STATE_AUTHORITY_INDEX",
            "BLK_045_HISTORICAL_ROADMAP_CONTROLLED_POST_042_SELECTION",
            "CONSOLIDATION_INDEX_ONLY_NO_RUNTIME_AUTHORITY",
            "CURRENT_STATE_INDEX_L0_L1_ONLY",
            "CODEX_LIVE_DISPATCH_REVIEW_READY_NOT_EXECUTION_AUTHORIZED",
            "BLK_TEST_EVIDENCE_ONLY_PRODUCTION_MCP_DISABLED",
            "BEO_PUBLICATION_DISABLED_DRAFT_AND_FIXTURE_ONLY",
            "RTM_RUNTIME_GENERATION_AND_DRIFT_REJECTION_DISABLED",
            "PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN",
            "BLK_PIPE_REMAINS_FINAL_MUTATION_ENFORCEMENT_AUTHORITY",
            "CURRENT_STATE_INDEX_GRANTS_NO_LIVE_AUTHORITY",
            "No live Codex execution authority",
            "No production BLK-test MCP authority",
            "No authoritative BEO publication authority",
            "No runtime RTM generation authority",
            "No RTM drift rejection authority",
            "No protected BLK-req body reads",
            "No network, model-service, cyber, browser, or package-manager tooling authority",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
            "Persistent doctrine gate marker: BLK-SYSTEM-043 pins current-state authority index non-execution scope",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-046 boundary markers missing: {missing}")

    def test_sprint079_post_078_current_state_authority_index_refresh_boundary(self):
        self.assertTrue(BLK077.exists(), "BLK-077 post-078 roadmap missing")
        self.assertTrue(BLK078.exists(), "BLK-078 tactical-standard profile architecture missing")
        self.assertTrue(BLK079.exists(), "BLK-079 post-078 current-state authority index missing")

        index_text = BLK079.read_text()
        required_index_markers = [
            "BLK-System Post-078 Current-State Authority Index",
            "Active current-state authority index — supersedes BLK-046 for current selection and reconciles post-103 state; not sprint authority and not runtime authority",
            "BLK_SYSTEM_POST_103_CURRENT_STATE_AUTHORITY_INDEX",
            "BLK_SYSTEM_POST_078_CURRENT_STATE_AUTHORITY_INDEX",
            "BLK_077_CURRENT_ROADMAP_SELECTOR",
            "BLK_078_TACTICAL_PROFILE_ARCHITECTURE_ANCHOR",
            "BLK_046_SUPERSEDED_BY_BLK_079_POST_078_INDEX",
            "BLK_058_LAYER_C_PROFILE_SOURCE_NOT_DISPATCH_AUTHORITY",
            "CONSOLIDATION_INDEX_ONLY_NO_RUNTIME_AUTHORITY",
            "CURRENT_STATE_INDEX_L0_L1_ONLY",
            "NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_AUTHORITY",
            "NO_KURONODE_MUTATION_AUTHORITY",
            "CODEX_LIVE_DISPATCH_REVIEW_READY_NOT_EXECUTION_AUTHORIZED",
            "BLK_TEST_EVIDENCE_ONLY_PRODUCTION_MCP_DISABLED",
            "BEO_PUBLICATION_RECORD_ONLY_SIGNER_STORAGE_LEDGER_DISABLED",
            "RTM_TRACE_CLOSURE_LOCAL_RECORD_ONLY_PRODUCTION_BLK_LINK_DISABLED",
            "BLK_SYSTEM_104_POST_103_ROADMAP_CURRENT_STATE_RECONCILED",
            "NEXT_SAFE_IMPLEMENTATION_FRONTIER_GO_PROTECTED_BODY_NO_READ_REMEDIATION",
            "PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN",
            "BLK_PIPE_REMAINS_FINAL_MUTATION_ENFORCEMENT_AUTHORITY",
            "CURRENT_STATE_INDEX_GRANTS_NO_LIVE_AUTHORITY",
            "docs/BLK-077_blk-system-post-078-roadmap.md",
            "docs/BLK-078_tactical-standard-profile-architecture.md",
            "BLK-SYSTEM-080 — Tactical Standard Profile Registry / Layer B Extraction",
            "Persistent doctrine gate marker: BLK-SYSTEM-079 pins post-078 current-state authority index non-execution scope; BLK-SYSTEM-104 pins post-103 reconciliation non-execution scope",
            "No live Codex execution authority",
            "No production BLK-test MCP authority",
            "No authoritative BEO publication authority",
            "No runtime RTM generation authority",
            "No RTM drift rejection authority",
            "No protected BLK-req body reads",
            "No BEB dispatch or BEO closeout execution authority",
            "No Kuronode mutation authority",
            "No network, model-service, cyber, browser, or package-manager tooling authority",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
        ]
        missing_index_markers = [marker for marker in required_index_markers if marker not in index_text]
        self.assertEqual(missing_index_markers, [], f"BLK-079 boundary markers missing: {missing_index_markers}")

        blk046_text = BLK046.read_text()
        required_blk046_supersession = [
            "Superseded by BLK-079",
            "docs/BLK-079_post-078-current-state-authority-index.md",
            "BLK-046 is retained as historical current-state authority index lineage",
            "BLK-077 controls current roadmap selection after BLK-SYSTEM-078",
        ]
        missing_blk046_markers = [marker for marker in required_blk046_supersession if marker not in blk046_text]
        self.assertEqual(missing_blk046_markers, [], f"BLK-046 supersession markers missing: {missing_blk046_markers}")
        forbidden_blk046_active_markers = [
            "BLK_045_CURRENT_ROADMAP_CONTROLS_POST_042_SELECTION",
            "BLK-045 controls current roadmap selection after BLK-SYSTEM-042.",
        ]
        leaked_blk046_markers = [marker for marker in forbidden_blk046_active_markers if marker in blk046_text]
        self.assertEqual(leaked_blk046_markers, [], f"BLK-046 retains active selector wording: {leaked_blk046_markers}")

        roadmap_text = BLK077.read_text()
        required_roadmap_markers = [
            "BLK-SYSTEM-079 completed the current-state authority index refresh",
            "docs/BLK-079_post-078-current-state-authority-index.md",
            "Historical post-079 selector closed by BLK-SYSTEM-080:",
            "BLK-SYSTEM-080 — Tactical Standard Profile Registry / Layer B Extraction",
        ]
        missing_roadmap_markers = [marker for marker in required_roadmap_markers if marker not in roadmap_text]
        self.assertEqual(missing_roadmap_markers, [], f"BLK-077 post-079 markers missing: {missing_roadmap_markers}")
        forbidden_roadmap_markers = [
            "Current-state index drift",
            "BLK-046 still describes post-042/post-045 selection and is stale relative to BLK-077 and BLK-SYSTEM-078.",
        ]
        leaked_roadmap_markers = [marker for marker in forbidden_roadmap_markers if marker in roadmap_text]
        self.assertEqual(leaked_roadmap_markers, [], f"BLK-077 retains stale post-079 gap wording: {leaked_roadmap_markers}")

    def test_sprint080_tactical_profile_registry_and_layer_b_extraction_boundary(self):
        self.assertTrue(BLK080.exists(), "BLK-080 tactical profile registry and Layer B extraction doctrine missing")
        text = BLK080.read_text()
        required = [
            "BLK-080 — Tactical Standard Profile Registry and Layer B Extraction",
            "Active L0/L1 profile-registry boundary — deterministic fixture and doctrine gate only; not runtime authority",
            "BLK_SYSTEM_TACTICAL_PROFILE_REGISTRY_AND_LAYER_B_EXTRACTION",
            "TACTICAL_PROFILE_REGISTRY_L0_L1_FIXTURE_ONLY",
            "LAYER_A_UNIVERSAL_CORE_NOT_WEAKENED",
            "LAYER_B_UNIVERSAL_TACTICAL_OUTPUT_SAFETY_STANDARD",
            "LAYER_C_TARGET_PROFILE_REGISTRY",
            "BLK_058_REGISTERED_AS_KURONODE_TYPESCRIPT_LAYER_C_SOURCE",
            "PROFILE_SELECTION_RECORD_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY",
            "EXACT_DENIED_AUTHORITIES_REQUIRED",
            "NO_PROFILE_SELECTION_RUNTIME_AUTHORITY",
            "NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_AUTHORITY",
            "NO_TARGET_REPO_SCAN_AUTHORITY",
            "NO_TARGET_REPO_MUTATION_AUTHORITY",
            "NO_KURONODE_MUTATION_AUTHORITY",
            "NO_LIVE_CODEX_EXECUTION_AUTHORITY",
            "NO_BLK_PIPE_EXECUTION_AUTHORITY",
            "NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY",
            "NO_BEO_PUBLICATION_AUTHORITY",
            "NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY",
            "NO_PROTECTED_BLK_REQ_BODY_READS",
            "NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY",
            "NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM",
            "simple_reviewable_control_flow",
            "bounded_iteration",
            "bounded_runtime_state",
            "explicit_lifecycle_management",
            "small_hostile_reviewable_units",
            "boundary_validation",
            "checked_results_and_postconditions",
            "minimal_mutable_scope",
            "no_dynamic_execution_laundering",
            "flat_validated_data_access",
            "zero_warning_intent_under_repository_owned_profiles",
            "no_authority_laundering",
            "kuronode-typescript",
            "docs/BLK-058_kuronode-typescript-power-of-ten-tactical-standard.md",
            "docs/BLK-078_tactical-standard-profile-architecture.md",
            "python/blk_tactical_profile_registry.py",
            "No live target-repository scans",
            "No Kuronode source or Git mutation",
            "No live Codex execution authority",
            "No BLK-pipe execution authority",
            "No production BLK-test MCP authority",
            "No authoritative BEO publication authority",
            "No runtime RTM generation or RTM drift rejection authority",
            "No protected BLK-req body reads",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
            "Persistent doctrine gate marker: BLK-SYSTEM-080 pins tactical profile registry and Layer B extraction as L0/L1 non-runtime scope",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-080 boundary markers missing: {missing}")
        forbidden = [
            "profile selection grants runtime authority",
            "BLK-058 authorizes Kuronode mutation",
            "Layer B authorizes live target scans",
            "profile compliance authorizes BEO publication",
            "profile compliance authorizes RTM generation",
        ]
        leaked = [marker for marker in forbidden if marker in text]
        self.assertEqual(leaked, [], f"BLK-080 leaked forbidden authority wording: {leaked}")

    def test_blk081_target_repo_execution_governance_boundary(self):
        self.assertTrue(BLK081.exists(), "BLK-081 target-repo execution governance doctrine missing")
        text = BLK081.read_text()
        required = [
            "BLK-081 — Target-Repo Execution Governance Pattern",
            "Active L0/L1 target-repository execution governance boundary — deterministic fixture and doctrine gate only; not runtime authority",
            "BLK_SYSTEM_TARGET_REPO_EXECUTION_GOVERNANCE_PATTERN",
            "TARGET_REPO_EXECUTION_GOVERNANCE_L0_L1_FIXTURE_ONLY",
            "TARGET_REPO_GOVERNANCE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME",
            "REQUEST_PACKAGE_NOT_APPROVAL",
            "PROFILE_SELECTION_RECORD_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY",
            "APPROVAL_ENVELOPE_REQUIRED_NOT_GRANTED",
            "PREFLIGHT_REFUSAL_REQUIRED_FOR_ABSENT_STALE_EXPIRED_REPLAYED_OR_MISMATCHED_AUTHORITY",
            "BLK_PIPE_INVOCATION_BOUNDARY_NOT_EXECUTED",
            "VALIDATION_EVIDENCE_PROFILE_NAMES_ONLY_NOT_SHELL",
            "HOSTILE_AUDIT_REQUIRED_BEFORE_TARGET_CLOSEOUT",
            "TARGET_REPO_CLOSEOUT_REQUIRES_SEPARATE_AUTHORITY",
            "NO_GOVERNANCE_RECORD_RUNTIME_AUTHORITY",
            "NO_TARGET_REPO_SCAN_AUTHORITY",
            "NO_TARGET_REPO_MUTATION_AUTHORITY",
            "NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_AUTHORITY",
            "NO_APPROVAL_ENVELOPE_RETARGETING_AUTHORITY",
            "NO_LIVE_CODEX_EXECUTION_AUTHORITY",
            "NO_BLK_PIPE_EXECUTION_AUTHORITY",
            "NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY",
            "NO_BEO_PUBLICATION_AUTHORITY",
            "NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY",
            "NO_PROTECTED_BLK_REQ_BODY_READS",
            "NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY",
            "NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM",
            "python/blk_target_repo_execution_governance.py",
            "python/blk_tactical_profile_registry.py",
            "docs/BLK-080_tactical-standard-profile-registry-and-layer-b-extraction.md",
            "Persistent doctrine gate marker: BLK-SYSTEM-081 pins target-repo execution governance as L0/L1 non-runtime scope",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-081 boundary markers missing: {missing}")
        forbidden = [
            "profile selection grants runtime authority",
            "approval envelope grants target mutation",
            "BLK-081 authorizes target-repo scans",
            "BLK-081 authorizes target-repo mutation",
            "BLK-081 authorizes BEB dispatch",
            "BLK-081 authorizes BEO closeout execution",
            "BLK-081 authorizes BEO publication",
            "BLK-081 authorizes RTM generation",
        ]
        leaked = [marker for marker in forbidden if marker in text]
        self.assertEqual(leaked, [], f"BLK-081 leaked forbidden authority wording: {leaked}")

    def test_blk082_blk058_mechanical_enforcement_boundary(self):
        self.assertTrue(BLK082.exists(), "BLK-082 BLK-058 mechanical enforcement doctrine missing")
        text = BLK082.read_text()
        required = [
            "BLK-082 — BLK-058 Mechanical Enforcement Upgrade",
            "Active L0/L1 BLK-058 mechanical enforcement boundary — deterministic submitted-snippet fixture and doctrine gate only; not runtime authority",
            "BLK_058_MECHANICAL_ENFORCEMENT_UPGRADE",
            "BLK_058_MECHANICAL_ENFORCEMENT_L0_L1_FIXTURE_ONLY",
            "SUBMITTED_SNIPPET_EVALUATION_ONLY_NOT_TARGET_SCAN",
            "BLK_058_MECHANICAL_ENFORCEMENT_PASS_FIXTURE_ONLY_NOT_RUNTIME_AUTHORITY",
            "BLK_058_MECHANICAL_ENFORCEMENT_BLOCKED_FIXTURE_ONLY",
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
            "python/blk_058_mechanical_enforcement.py",
            "python/blk_target_repo_execution_governance.py",
            "docs/BLK-058_kuronode-typescript-power-of-ten-tactical-standard.md",
            "Persistent doctrine gate marker: BLK-SYSTEM-082 pins BLK-058 mechanical enforcement as L0/L1 submitted-snippet fixture scope",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-082 boundary markers missing: {missing}")
        forbidden = [
            "BLK-082 authorizes target-repo scans",
            "BLK-082 authorizes target-repo mutation",
            "mechanical PASS authorizes target mutation",
            "mechanical PASS authorizes BEB dispatch",
            "mechanical PASS authorizes BEO closeout execution",
            "mechanical PASS authorizes BEO publication",
            "mechanical PASS authorizes RTM generation",
            "mechanical PASS authorizes protected-body reads",
        ]
        leaked = [marker for marker in forbidden if marker in text]
        self.assertEqual(leaked, [], f"BLK-082 leaked forbidden authority wording: {leaked}")

    def test_blk083_beo_publication_decision_package_boundary(self):
        self.assertTrue(BLK083.exists(), "BLK-083 BEO publication decision-package doctrine missing")
        text = BLK083.read_text()
        required = [
            "BLK-083 — BEO Publication Decision Package / Pilot Request",
            "Active L0/L1 BEO publication decision-package boundary — deterministic human-review fixture and doctrine gate only; not publication approval and not publication authority",
            "BEO_PUBLICATION_DECISION_PACKAGE_PILOT_REQUEST",
            "BEO_PUBLICATION_DECISION_PACKAGE_READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PUBLISHED",
            "beo_publication_pilot_request",
            "FUTURE_EXPLICIT_HUMAN_PUBLICATION_PILOT_APPROVAL_REQUIRED_NOT_GRANTED",
            "BEO_PUBLICATION_DECISION_PACKAGE_ONLY_NOT_PUBLICATION_APPROVAL",
            "NO_ACTUAL_AUTHORITATIVE_BEO_PUBLICATION_AUTHORITY",
            "NO_PUBLICATION_APPROVAL_GRANTED",
            "NO_PUBLICATION_PILOT_EXECUTION_AUTHORITY",
            "NO_RUNTIME_PUBLISHED_BEO_OUTPUT",
            "NO_LIVE_PUBLICATION_APPROVAL_CAPTURE",
            "NO_SIGNER_KEY_MATERIAL_ACCESS",
            "NO_CRYPTOGRAPHIC_SIGNING_AUTHORITY",
            "NO_IMMUTABLE_STORAGE_WRITE_AUTHORITY",
            "NO_PUBLIC_LEDGER_APPEND_OR_MUTATION_AUTHORITY",
            "NO_ROLLBACK_REVOCATION_OR_SUPERSESSION_EXECUTION_AUTHORITY",
            "NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY",
            "NO_ACTIVE_VAULT_HASH_COMPARISON_OR_COVERAGE_CLAIM_AUTHORITY",
            "NO_PROTECTED_BLK_REQ_BODY_READS",
            "NO_TARGET_REPO_SCAN_OR_MUTATION_AUTHORITY",
            "NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_EXECUTION_AUTHORITY",
            "NO_BLK_PIPE_BLK_TEST_OR_CODEX_RUNTIME_AUTHORITY",
            "NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY",
            "NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM",
            "docs/BLK-057_authoritative-beo-publication-authority-request-boundary.md",
            "docs/BLK-060_authoritative-beo-publication-approval-envelope-boundary.md",
            "python/beo_publication_decision_package.py",
            "Persistent doctrine gate marker: BLK-SYSTEM-083 pins BEO publication decision package as L0/L1 human-review request scope",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-083 boundary markers missing: {missing}")
        forbidden = [
            "BLK-083 authorizes BEO publication",
            "BLK-083 grants publication approval",
            "decision package PASS authorizes publication",
            "pilot request authorizes pilot execution",
            "approval envelope authorizes publication",
            "BLK-083 authorizes signer key access",
            "BLK-083 authorizes immutable storage writes",
            "BLK-083 authorizes public ledger mutation",
            "BLK-083 authorizes rollback execution",
            "BLK-083 authorizes RTM generation",
            "BLK-083 authorizes protected-body reads",
            "BLK-083 authorizes target-repo scans",
            "BLK-083 authorizes BLK-test runtime",
            "BLK-083 authorizes live Codex execution",
        ]
        leaked = [marker for marker in forbidden if marker in text]
        self.assertEqual(leaked, [], f"BLK-083 leaked forbidden authority wording: {leaked}")

    def test_current_active_doctrine_uses_beb_beo_terminology(self):
        current_surfaces = [
            BLK058,
            BLK077,
            BLK078,
            BLK079,
            BLK080,
            BLK081,
            BLK082,
            BLK083,
            ROOT / "python" / "blk_current_state_authority_index.py",
            ROOT / "python" / "blk_tactical_profile_registry.py",
            ROOT / "python" / "blk_target_repo_execution_governance.py",
            ROOT / "python" / "blk_058_mechanical_enforcement.py",
        ]
        forbidden = re.compile(r"NO_CEB_CEO|CEB/CEO|(?<![A-Za-z0-9_])CEBs?(?![A-Za-z0-9_])|(?<![A-Za-z0-9_])CEOs?(?![A-Za-z0-9_])")
        leaks = []
        for path in current_surfaces:
            text = path.read_text()
            for line_number, line in enumerate(text.splitlines(), start=1):
                if forbidden.search(line):
                    leaks.append(f"{path.relative_to(ROOT)}:{line_number}: {line.strip()}")
        self.assertEqual(leaks, [], "current active surfaces retain antiquated CEB/CEO terminology")

    def test_sprint080_completion_updates_current_roadmap_and_next_sprint_to_081(self):
        self.assertTrue(BLK077.exists(), "BLK-077 post-078 roadmap missing")
        self.assertTrue(BLK079.exists(), "BLK-079 current-state authority index missing")
        self.assertTrue(BLK080.exists(), "BLK-080 tactical profile registry doctrine missing")

        roadmap_text = BLK077.read_text()
        index_text = BLK079.read_text()
        required_roadmap_markers = [
            "BLK-SYSTEM-080 completed the tactical profile registry / Layer B extraction",
            "docs/BLK-080_tactical-standard-profile-registry-and-layer-b-extraction.md",
            "python/blk_tactical_profile_registry.py",
            "Historical post-080 selector closed by BLK-SYSTEM-081:",
            "BLK-SYSTEM-081 — Target-Repo Execution Governance Pattern",
            "profile-selection registry and Layer B extraction are now L0/L1 fixture/doctrine surfaces",
            "No target-repo scan, no target-repo mutation, no BEB dispatch, and no BEO closeout execution unless a future human-approved exact sprint payload grants that target-repo scope",
        ]
        missing_roadmap_markers = [marker for marker in required_roadmap_markers if marker not in roadmap_text]
        self.assertEqual(missing_roadmap_markers, [], f"BLK-077 post-080 markers missing: {missing_roadmap_markers}")

        required_index_markers = [
            "Post-BLK-SYSTEM-080 current-state update",
            "BLK-SYSTEM-080 completed the tactical profile registry / Layer B extraction",
            "docs/BLK-080_tactical-standard-profile-registry-and-layer-b-extraction.md",
            "python/blk_tactical_profile_registry.py",
            "BLK-080 tactical profile registry / Layer B extraction",
            "L0/L1 fixture/doctrine complete",
            "Historical next sprint selected after BLK-SYSTEM-080 (now completed by BLK-SYSTEM-081):",
            "BLK-SYSTEM-081 — Target-Repo Execution Governance Pattern",
            "No live target-repository scans",
            "No target-repository source or Git mutation",
            "No BEB dispatch or BEO closeout execution authority",
        ]
        missing_index_markers = [marker for marker in required_index_markers if marker not in index_text]
        self.assertEqual(missing_index_markers, [], f"BLK-079 post-080 markers missing: {missing_index_markers}")

        forbidden_roadmap_markers = [
            "Then, implement the BLK-078 tactical-standard/profile architecture as BLK-System fixtures and records.",
            "The default next sprint after BLK-SYSTEM-079 is therefore:",
            "That sprint should develop BLK-System documentation/fixtures/gates only.",
        ]
        leaked_roadmap_markers = [marker for marker in forbidden_roadmap_markers if marker in roadmap_text]
        self.assertEqual(leaked_roadmap_markers, [], f"BLK-077 retains stale active BLK-SYSTEM-080 guidance: {leaked_roadmap_markers}")

        forbidden_index_markers = [
            "The default next sprint after BLK-SYSTEM-079 is:",
            "BLK-SYSTEM-080 should remain BLK-System documentation/fixture/gate work",
            "If the operator asks for the default next BLK-System sprint after BLK-SYSTEM-079, select `BLK-SYSTEM-080 — Tactical Standard Profile Registry / Layer B Extraction`.",
        ]
        leaked_index_markers = [marker for marker in forbidden_index_markers if marker in index_text]
        self.assertEqual(leaked_index_markers, [], f"BLK-079 retains stale active BLK-SYSTEM-080 guidance: {leaked_index_markers}")

    def test_sprint081_completion_updates_current_roadmap_and_next_sprint_to_082(self):
        self.assertTrue(BLK077.exists(), "BLK-077 post-078 roadmap missing")
        self.assertTrue(BLK079.exists(), "BLK-079 current-state authority index missing")
        self.assertTrue(BLK080.exists(), "BLK-080 tactical profile registry doctrine missing")
        self.assertTrue(BLK081.exists(), "BLK-081 target-repo governance doctrine missing")

        roadmap_text = BLK077.read_text()
        index_text = BLK079.read_text()
        required_roadmap_markers = [
            "BLK-SYSTEM-081 completed the target-repo execution governance pattern",
            "docs/BLK-081_target-repo-execution-governance-pattern.md",
            "python/blk_target_repo_execution_governance.py",
            "Historical post-081 selector closed by BLK-SYSTEM-082:",
            "BLK-SYSTEM-082 — BLK-058 Mechanical Enforcement Upgrade",
            "Target-repo execution governance is now an L0/L1 fixture/doctrine surface",
            "No target-repo scan, no target-repo mutation, no BEB dispatch, and no BEO closeout execution unless a future human-approved exact sprint payload grants that target-repo scope",
        ]
        missing_roadmap_markers = [marker for marker in required_roadmap_markers if marker not in roadmap_text]
        self.assertEqual(missing_roadmap_markers, [], f"BLK-077 post-081 markers missing: {missing_roadmap_markers}")

        required_index_markers = [
            "Post-BLK-SYSTEM-081 current-state update",
            "BLK-SYSTEM-081 completed the target-repo execution governance pattern",
            "docs/BLK-081_target-repo-execution-governance-pattern.md",
            "python/blk_target_repo_execution_governance.py",
            "BLK-081 target-repo execution governance pattern",
            "L0/L1 target-repo governance fixture/doctrine complete",
            "Historical next sprint selected after BLK-SYSTEM-081 (now completed by BLK-SYSTEM-082):",
            "BLK-SYSTEM-082 — BLK-058 Mechanical Enforcement Upgrade",
            "No live target-repository scans",
            "No target-repository source or Git mutation",
            "No BEB dispatch or BEO closeout execution authority",
        ]
        missing_index_markers = [marker for marker in required_index_markers if marker not in index_text]
        self.assertEqual(missing_index_markers, [], f"BLK-079 post-081 markers missing: {missing_index_markers}")

        forbidden_roadmap_markers = [
            "The default next sprint after BLK-SYSTEM-080 is therefore:",
            "BLK-SYSTEM-081 — Target-Repo Execution Governance Pattern\n   - L0/L1 doctrine/fixture sprint.",
        ]
        leaked_roadmap_markers = [marker for marker in forbidden_roadmap_markers if marker in roadmap_text]
        self.assertEqual(leaked_roadmap_markers, [], f"BLK-077 retains stale active BLK-SYSTEM-081 guidance: {leaked_roadmap_markers}")

        forbidden_index_markers = [
            "The default next sprint after BLK-SYSTEM-080 is:",
            "If the operator asks for the default next BLK-System sprint after BLK-SYSTEM-080, select `BLK-SYSTEM-081 — Target-Repo Execution Governance Pattern`.",
        ]
        leaked_index_markers = [marker for marker in forbidden_index_markers if marker in index_text]
        self.assertEqual(leaked_index_markers, [], f"BLK-079 retains stale active BLK-SYSTEM-081 guidance: {leaked_index_markers}")

    def test_sprint082_completion_routes_to_historical_sprint083_selection(self):
        self.assertTrue(BLK077.exists(), "BLK-077 post-078 roadmap missing")
        self.assertTrue(BLK079.exists(), "BLK-079 current-state authority index missing")
        self.assertTrue(BLK082.exists(), "BLK-082 mechanical enforcement doctrine missing")
        self.assertTrue(BLK083.exists(), "BLK-083 decision-package doctrine missing")

        roadmap_text = BLK077.read_text()
        index_text = BLK079.read_text()
        required_roadmap_markers = [
            "BLK-SYSTEM-082 completed the BLK-058 mechanical enforcement upgrade",
            "docs/BLK-082_blk058-mechanical-enforcement-upgrade.md",
            "python/blk_058_mechanical_enforcement.py",
            "Historical post-082 selector closed by BLK-SYSTEM-083:",
            "BLK-SYSTEM-083 — BEO Publication Decision Package / Pilot Request",
            "BEO Publication Decision Package is now a completed L0/L1 human-review request surface",
        ]
        missing_roadmap_markers = [marker for marker in required_roadmap_markers if marker not in roadmap_text]
        self.assertEqual(missing_roadmap_markers, [], f"BLK-077 post-082 markers missing: {missing_roadmap_markers}")

        required_index_markers = [
            "Post-BLK-SYSTEM-082 current-state update",
            "BLK-SYSTEM-082 completed the BLK-058 mechanical enforcement upgrade",
            "docs/BLK-082_blk058-mechanical-enforcement-upgrade.md",
            "python/blk_058_mechanical_enforcement.py",
            "Historical post-082 selector closed by BLK-SYSTEM-083:",
            "BLK-SYSTEM-083 — BEO Publication Decision Package / Pilot Request",
            "BLK-082 BLK-058 mechanical enforcement upgrade",
            "L0/L1 BLK-058 mechanical enforcement fixture complete",
        ]
        missing_index_markers = [marker for marker in required_index_markers if marker not in index_text]
        self.assertEqual(missing_index_markers, [], f"BLK-079 post-082 markers missing: {missing_index_markers}")

        forbidden_roadmap_markers = [
            "BEO Publication Decision Package remains an unselected future L0/L1 alternative",
            "The default next sprint after BLK-SYSTEM-081 is therefore:",
            "BLK-SYSTEM-082 — BLK-058 Mechanical Enforcement Upgrade or BEO Publication Decision Package\n```\n\nNo target-repo scan",
            "These are still real gaps in BLK-System after BLK-SYSTEM-080:",
            "No generalized target-repo execution governance pattern",
            "still lacks a reusable target-repo governance pattern",
            "This is the default BLK-SYSTEM-081 workstream.",
        ]
        leaked_roadmap_markers = [marker for marker in forbidden_roadmap_markers if marker in roadmap_text]
        self.assertEqual(leaked_roadmap_markers, [], f"BLK-077 retains stale active BLK-SYSTEM-082 guidance: {leaked_roadmap_markers}")

        forbidden_index_markers = [
            "BEO Publication Decision Package remains an unselected future L0/L1 alternative",
            "After BLK-SYSTEM-082, require explicit operator decision before any higher-authority frontier; candidate frontiers include one bounded BLK-test evidence refresh, one BEO Publication Decision Package or pilot request",
            "The default next sprint after BLK-SYSTEM-081 is:",
            "If the operator asks for the default next BLK-System sprint after BLK-SYSTEM-081, select `BLK-SYSTEM-082 — BLK-058 Mechanical Enforcement Upgrade or BEO Publication Decision Package`.",
        ]
        leaked_index_markers = [marker for marker in forbidden_index_markers if marker in index_text]
        self.assertEqual(leaked_index_markers, [], f"BLK-079 retains stale active BLK-SYSTEM-082 guidance: {leaked_index_markers}")

    def test_sprint083_completion_requires_explicit_publication_pilot_approval(self):
        self.assertTrue(BLK077.exists(), "BLK-077 post-078 roadmap missing")
        self.assertTrue(BLK079.exists(), "BLK-079 current-state authority index missing")
        self.assertTrue(BLK083.exists(), "BLK-083 decision-package doctrine missing")

        roadmap_text = BLK077.read_text()
        index_text = BLK079.read_text()
        required_roadmap_markers = [
            "BLK-SYSTEM-083 completed the BEO Publication Decision Package / Pilot Request",
            "docs/BLK-083_beo-publication-decision-package-pilot-request.md",
            "python/beo_publication_decision_package.py",
            "Actual publication pilot execution still requires separate explicit human approval in a future sprint",
            "No publication approval, no publication pilot execution, no signer/storage/ledger/rollback side effects, no RTM, no protected-body reads, no target-repo scan or mutation, no BLK-test/Codex/BLK-pipe runtime authority is granted",
        ]
        missing_roadmap_markers = [marker for marker in required_roadmap_markers if marker not in roadmap_text]
        self.assertEqual(missing_roadmap_markers, [], f"BLK-077 post-083 markers missing: {missing_roadmap_markers}")

        required_index_markers = [
            "Post-BLK-SYSTEM-083 current-state update",
            "BLK-SYSTEM-083 completed the BEO Publication Decision Package / Pilot Request",
            "docs/BLK-083_beo-publication-decision-package-pilot-request.md",
            "python/beo_publication_decision_package.py",
            "BLK-083 BEO publication decision package / pilot request",
            "L0/L1 BEO publication decision package review fixture complete",
            "Actual publication pilot execution still requires separate explicit human approval in a future sprint",
            "No publication approval, no publication pilot execution, no signer/storage/ledger/rollback side effects, no RTM, no protected-body reads, no target-repo scan or mutation, no BLK-test/Codex/BLK-pipe runtime authority is granted",
        ]
        missing_index_markers = [marker for marker in required_index_markers if marker not in index_text]
        self.assertEqual(missing_index_markers, [], f"BLK-079 post-083 markers missing: {missing_index_markers}")

        forbidden_markers = [
            "BLK-SYSTEM-083 authorizes BEO publication",
            "BLK-SYSTEM-083 grants publication approval",
            "BLK-SYSTEM-083 authorizes publication pilot execution",
            "BLK-SYSTEM-083 authorizes RTM generation",
            "BLK-SYSTEM-083 authorizes protected-body reads",
        ]
        leaked = [marker for marker in forbidden_markers if marker in roadmap_text or marker in index_text]
        self.assertEqual(leaked, [], f"BLK-SYSTEM-083 leaked forbidden authority wording: {leaked}")

    def test_sprint084_post083_frontier_selection_gate_refresh_denies_runtime_authority(self):
        self.assertTrue(BLK084.exists(), "BLK-084 post-083 frontier selection gate refresh missing")
        text = BLK084.read_text()
        required = [
            "BLK-084 — Post-083 Frontier Selection Gate Refresh",
            "Active L0/L1 post-083 frontier-selection gate — review-only; not runtime authority",
            "BLK_SYSTEM_POST_083_FRONTIER_SELECTION_GATE",
            "POST_083_FRONTIER_SELECTION_READY_FOR_HUMAN_DECISION_NOT_AUTHORITY",
            "POST_083_FRONTIER_SELECTION_BLOCKED_NOT_AUTHORIZED",
            "POST_083_FRONTIER_SELECTION_BLOCKED_PENDING_PUBLICATION_PREREQUISITES",
            "NEXT_LOGICAL_SPRINT_IS_NOT_APPROVAL",
            "BLK_083_DECISION_PACKAGE_IS_NOT_PUBLICATION_APPROVAL",
            "bounded_blk_test_evidence_refresh",
            "beo_publication_pilot_execution_request",
            "codex_live_dispatch_l3_smoke",
            "rtm_authority_request_after_publication_prerequisites",
            "bounded_consolidation_or_remediation_sprint",
            "No actual authoritative BEO publication authority",
            "No publication approval capture",
            "No publication pilot execution",
            "No signer key material access or cryptographic signing",
            "No immutable storage writes or public ledger mutation",
            "No runtime RTM generation or RTM drift rejection",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No target-repo scan or mutation",
            "No BLK-pipe dispatch, BLK-test runtime, production BLK-test MCP, or live Codex execution",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
            "Persistent doctrine gate marker: BLK-SYSTEM-084 pins post-083 frontier selection as review-only and non-runtime",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-084 boundary markers missing: {missing}")

        forbidden = [
            "BLK-SYSTEM-084 authorizes BEO publication",
            "BLK-SYSTEM-084 grants publication approval",
            "BLK-SYSTEM-084 authorizes publication pilot execution",
            "BLK-SYSTEM-084 authorizes RTM generation",
            "BLK-SYSTEM-084 authorizes BLK-test runtime",
            "BLK-SYSTEM-084 authorizes Codex live execution",
            "BLK-SYSTEM-084 authorizes target-repo mutation",
            "BLK-SYSTEM-084 authorizes protected-body reads",
        ]
        leaked = [marker for marker in forbidden if marker in text]
        self.assertEqual(leaked, [], f"BLK-084 leaked forbidden authority wording: {leaked}")

    def test_sprint085_beo_publication_pilot_execution_request_gate_denies_publication_authority(self):
        self.assertTrue(BLK085.exists(), "BLK-085 BEO publication pilot execution request gate missing")
        text = BLK085.read_text()
        required = [
            "BLK-085 — BEO Publication Pilot Execution Request Gate",
            "Active L0/L1 request-gate boundary — explicit human-approval request only; not publication approval and not publication execution",
            "BEO_PUBLICATION_PILOT_EXECUTION_REQUEST_GATE",
            "BEO_PUBLICATION_PILOT_EXECUTION_REQUEST_READY_FOR_EXPLICIT_HUMAN_APPROVAL_NOT_EXECUTED",
            "beo_publication_pilot_execution_request",
            "EXPLICIT_HUMAN_PUBLICATION_PILOT_APPROVAL_REQUIRED_NOT_GRANTED",
            "BEO_PUBLICATION_PILOT_EXECUTION_REQUEST_GATE_ONLY_NOT_APPROVAL_NOT_EXECUTION",
            "python/beo_publication_pilot_execution_request.py",
            "BLK-083",
            "BLK-084",
            "UPSTREAM_DECISION_PACKAGE_IDENTITY_AND_HASH_BOUND",
            "FRESH_APPROVAL_ID_AND_RUN_ID_RESERVED_FOR_FUTURE_APPROVAL",
            "HOSTILE_REVIEW_REQUIRED_BEFORE_ANY_PUBLICATION_PILOT_EXECUTION",
            "NO_PUBLICATION_APPROVAL_GRANTED",
            "NO_PUBLICATION_PILOT_EXECUTION_PERFORMED",
            "NO_RUNTIME_PUBLISHED_BEO_OUTPUT",
            "NO_LIVE_PUBLICATION_APPROVAL_CAPTURE",
            "NO_SIGNER_KEY_MATERIAL_ACCESS",
            "NO_CRYPTOGRAPHIC_SIGNING_AUTHORITY",
            "NO_IMMUTABLE_STORAGE_WRITE_AUTHORITY",
            "NO_PUBLIC_LEDGER_APPEND_OR_MUTATION_AUTHORITY",
            "NO_ROLLBACK_REVOCATION_OR_SUPERSESSION_EXECUTION_AUTHORITY",
            "NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY",
            "NO_ACTIVE_VAULT_HASH_COMPARISON_OR_COVERAGE_CLAIM_AUTHORITY",
            "NO_PROTECTED_BLK_REQ_BODY_READS",
            "NO_TARGET_REPO_SCAN_OR_MUTATION_AUTHORITY",
            "NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_EXECUTION_AUTHORITY",
            "NO_BLK_PIPE_BLK_TEST_OR_CODEX_RUNTIME_AUTHORITY",
            "NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY",
            "NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM",
            "Persistent doctrine gate marker: BLK-SYSTEM-085 pins BEO publication pilot execution request as request-only and non-runtime",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-085 boundary markers missing: {missing}")

        forbidden = [
            "BLK-SYSTEM-085 grants publication approval",
            "BLK-SYSTEM-085 authorizes publication pilot execution",
            "BLK-SYSTEM-085 authorizes signer key access",
            "BLK-SYSTEM-085 authorizes immutable storage writes",
            "BLK-SYSTEM-085 authorizes public ledger mutation",
            "BLK-SYSTEM-085 authorizes RTM generation",
            "BLK-SYSTEM-085 authorizes target-repo scan",
            "BLK-SYSTEM-085 authorizes target-repo mutation",
            "BLK-SYSTEM-085 authorizes protected-body reads",
        ]
        leaked = [marker for marker in forbidden if marker in text]
        self.assertEqual(leaked, [], f"BLK-085 leaked forbidden authority wording: {leaked}")

    def test_sprint086_beo_publication_pilot_approval_decision_captures_exact_request_without_execution(self):
        self.assertTrue(BLK086.exists(), "BLK-086 BEO publication pilot approval decision missing")
        text = BLK086.read_text()
        required = [
            "BLK-086 — BEO Publication Pilot Approval Decision",
            "Active exact approval-decision boundary — human approval decision captured for the exact BLK-085 request; not publication pilot execution",
            "BEO_PUBLICATION_PILOT_APPROVAL_DECISION",
            "BEO_PUBLICATION_PILOT_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK085_REQUEST_NOT_EXECUTED",
            "beo_publication_pilot_approval_decision",
            "BEO_PUBLICATION_PILOT_APPROVAL_DECISION_ONLY_NOT_EXECUTION",
            "APPROVED_FOR_ONE_FUTURE_BEO_PUBLICATION_PILOT_EXECUTION_NOT_EXECUTED",
            "EXACT_BEO_PUBLICATION_PILOT_EXECUTION_SPRINT_REQUIRED_NOT_RUN",
            "request_package_hash: sha256:6dc1b6eac1d85b3a2d3b7c01eb8efa2f3f5ed0f91e04227a3a7b43554271db10",
            "approval_decision_package_id: BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-001",
            "approval_id: APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001",
            "future_run_id: RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001",
            "python/beo_publication_pilot_approval_decision.py",
            "BLK085_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
            "HUMAN_APPROVAL_DECISION_CAPTURED_FOR_EXACT_REQUEST",
            "FUTURE_RUN_ID_RESERVED_NOT_CONSUMED",
            "NEXT_EXECUTION_SPRINT_REQUIRED_BEFORE_ANY_PUBLICATION_PILOT_RUN",
            "NO_PUBLICATION_PILOT_EXECUTION_PERFORMED_BY_BLK_SYSTEM_086",
            "NO_RUNTIME_PUBLISHED_BEO_OUTPUT",
            "NO_LIVE_EXTERNAL_PUBLICATION_APPROVAL_CAPTURE",
            "NO_APPROVAL_RETARGETING_OR_SCOPE_EXPANSION",
            "NO_FUTURE_RUN_ID_CONSUMPTION",
            "NO_SIGNER_KEY_MATERIAL_ACCESS",
            "NO_CRYPTOGRAPHIC_SIGNING_AUTHORITY",
            "NO_IMMUTABLE_STORAGE_WRITE_AUTHORITY",
            "NO_PUBLIC_LEDGER_APPEND_OR_MUTATION_AUTHORITY",
            "NO_ROLLBACK_REVOCATION_OR_SUPERSESSION_EXECUTION_AUTHORITY",
            "NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY",
            "NO_ACTIVE_VAULT_HASH_COMPARISON_OR_COVERAGE_CLAIM_AUTHORITY",
            "NO_PROTECTED_BLK_REQ_BODY_READS",
            "NO_TARGET_REPO_SCAN_OR_MUTATION_AUTHORITY",
            "NO_SOURCE_OR_GIT_MUTATION_AUTHORITY",
            "NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_EXECUTION_AUTHORITY",
            "NO_BLK_PIPE_BLK_TEST_OR_CODEX_RUNTIME_AUTHORITY",
            "NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY",
            "NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM",
            "Persistent doctrine gate marker: BLK-SYSTEM-086 pins BEO publication pilot approval decision as exact request-bound approval capture, not execution",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-086 boundary markers missing: {missing}")

        forbidden = [
            "BLK-SYSTEM-086 executes publication pilot",
            "BLK-SYSTEM-086 creates runtime PUBLISHED BEO output",
            "BLK-SYSTEM-086 authorizes signer key access",
            "BLK-SYSTEM-086 authorizes immutable storage writes",
            "BLK-SYSTEM-086 authorizes public ledger mutation",
            "BLK-SYSTEM-086 authorizes RTM generation",
            "BLK-SYSTEM-086 authorizes target-repo scan",
            "BLK-SYSTEM-086 authorizes target-repo mutation",
            "BLK-SYSTEM-086 authorizes protected-body reads",
        ]
        leaked = [marker for marker in forbidden if marker in text]
        self.assertEqual(leaked, [], f"BLK-086 leaked forbidden authority wording: {leaked}")

    def test_sprint086_completion_preserves_approval_decision_not_execution_boundary(self):
        self.assertTrue(BLK077.exists(), "BLK-077 post-078 roadmap missing")
        self.assertTrue(BLK079.exists(), "BLK-079 current-state authority index missing")
        self.assertTrue(BLK086.exists(), "BLK-086 BEO publication pilot approval decision missing")

        roadmap_text = BLK077.read_text()
        index_text = BLK079.read_text()
        doctrine_text = BLK086.read_text()
        required_roadmap_markers = [
            "BLK-SYSTEM-086 captured the exact BEO Publication Pilot Approval Decision",
            "docs/BLK-086_beo-publication-pilot-approval-decision.md",
            "python/beo_publication_pilot_approval_decision.py",
            "BEO_PUBLICATION_PILOT_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK085_REQUEST_NOT_EXECUTED",
            "approval_decision_package_id: BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-001",
            "APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001",
            "RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001",
            "exact execution sprint bound to the BLK-086 approval-decision package",
            "no publication pilot execution",
            "no runtime `PUBLISHED` BEO output",
            "no signer/storage/ledger/rollback side effects",
            "no RTM generation",
            "no protected-body reads",
            "no target-repo scan or mutation",
        ]
        missing_roadmap = [marker for marker in required_roadmap_markers if marker not in roadmap_text]
        self.assertEqual(missing_roadmap, [], f"BLK-077 post-086 markers missing: {missing_roadmap}")

        required_index_markers = [
            "Post-BLK-SYSTEM-086 current-state update",
            "BLK-SYSTEM-086 completed the BEO Publication Pilot Approval Decision",
            "docs/BLK-086_beo-publication-pilot-approval-decision.md",
            "python/beo_publication_pilot_approval_decision.py",
            "BEO_PUBLICATION_PILOT_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK085_REQUEST_NOT_EXECUTED",
            "sha256:6dc1b6eac1d85b3a2d3b7c01eb8efa2f3f5ed0f91e04227a3a7b43554271db10",
            "future run ID remains unconsumed",
            "separate exact execution sprint",
            "No publication pilot execution",
            "no runtime `PUBLISHED` BEO output",
        ]
        missing_index = [marker for marker in required_index_markers if marker not in index_text]
        self.assertEqual(missing_index, [], f"BLK-079 post-086 markers missing: {missing_index}")

        required_doctrine_markers = [
            "BEO_PUBLICATION_PILOT_APPROVAL_DECISION",
            "BEO_PUBLICATION_PILOT_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK085_REQUEST_NOT_EXECUTED",
            "NO_PUBLICATION_PILOT_EXECUTION_PERFORMED_BY_BLK_SYSTEM_086",
            "NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY",
            "NO_TARGET_REPO_SCAN_OR_MUTATION_AUTHORITY",
        ]
        missing_doctrine = [marker for marker in required_doctrine_markers if marker not in doctrine_text]
        self.assertEqual(missing_doctrine, [], f"BLK-086 doctrine markers missing: {missing_doctrine}")

        forbidden = [
            "BLK-SYSTEM-086 executes publication pilot",
            "BLK-SYSTEM-086 creates runtime PUBLISHED BEO output",
            "BLK-SYSTEM-086 authorizes signer key access",
            "BLK-SYSTEM-086 authorizes immutable storage writes",
            "BLK-SYSTEM-086 authorizes public ledger mutation",
            "BLK-SYSTEM-086 authorizes RTM generation",
            "BLK-SYSTEM-086 authorizes target-repo scan",
            "BLK-SYSTEM-086 authorizes target-repo mutation",
            "BLK-SYSTEM-086 authorizes protected-body reads",
        ]
        leaked = [marker for marker in forbidden if marker in roadmap_text or marker in index_text]
        self.assertEqual(leaked, [], f"BLK-SYSTEM-086 leaked forbidden authority wording: {leaked}")


    def test_sprint088_rtm_authority_request_after_local_beo_pilot_is_request_only(self):
        self.assertTrue(BLK088.exists(), "BLK-088 RTM authority request boundary missing")
        text = BLK088.read_text()
        required = [
            "BLK-088 — RTM Authority Request After Local BEO Pilot Prerequisites",
            "Active RTM authority request boundary — review package only; not RTM generation authority",
            "RTM_AUTHORITY_REQUEST_AFTER_LOCAL_BEO_PILOT_PREREQUISITES",
            "RTM_AUTHORITY_REQUEST_READY_AFTER_LOCAL_BEO_PILOT_PREREQUISITES_NOT_GRANTED",
            "rtm_authority_request_after_local_beo_pilot_prerequisites",
            "RTM_AUTHORITY_REQUEST_AFTER_LOCAL_BEO_PILOT_PREREQUISITES_REVIEW_ONLY",
            "EXPLICIT_HUMAN_RTM_GENERATION_APPROVAL_REQUIRED_NOT_GRANTED",
            "authority_request_package_id: RTM-AUTHORITY-REQUEST-AFTER-BEO-PILOT-088-001",
            "upstream_execution_package_id: BEO-PUBLICATION-PILOT-EXECUTION-087-001",
            "RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001",
            "PILOT_LOCAL_PUBLISHED_BEO_OUTPUT_NOT_AUTHORITATIVE",
            "python/rtm_authority_request_after_beo_pilot.py",
            "BLK087_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND",
            "PILOT_PUBLICATION_ARTIFACT_IDENTITY_AND_HASH_BOUND",
            "RTM_AUTHORITY_REQUESTED_FOR_REVIEW_NOT_GRANTED",
            "NO_RUNTIME_RTM_GENERATION_BY_BLK_SYSTEM_088",
            "NO_RTM_DRIFT_REJECTION_OR_DRIFT_DECISION_AUTHORITY",
            "NO_ACTIVE_VAULT_HASH_COMPARISON_OR_COVERAGE_CLAIM_AUTHORITY",
            "NO_PROTECTED_BLK_REQ_BODY_READS",
            "NO_AUTHORITATIVE_EXTERNAL_BEO_PUBLICATION_BY_BLK_SYSTEM_088",
            "NO_SIGNER_KEY_MATERIAL_ACCESS",
            "NO_PUBLIC_LEDGER_APPEND_OR_MUTATION_AUTHORITY",
            "NO_TARGET_REPO_SCAN_OR_MUTATION_AUTHORITY",
            "NO_BLK_PIPE_BLK_TEST_OR_CODEX_RUNTIME_AUTHORITY",
            "NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY",
            "NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM",
            "Persistent doctrine gate marker: BLK-SYSTEM-088 pins RTM authority request as review-only and not generation authority",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-088 boundary markers missing: {missing}")

        forbidden = [
            "BLK-SYSTEM-088 authorizes RTM generation",
            "BLK-SYSTEM-088 authorizes drift rejection",
            "BLK-SYSTEM-088 authorizes protected-body reads",
            "BLK-SYSTEM-088 authorizes active-vault hash comparison",
            "BLK-SYSTEM-088 authorizes external authoritative publication",
            "BLK-SYSTEM-088 authorizes target-repo scan",
            "BLK-SYSTEM-088 authorizes target-repo mutation",
        ]
        leaked = [marker for marker in forbidden if marker in text]
        self.assertEqual(leaked, [], f"BLK-088 leaked forbidden authority wording: {leaked}")

    def test_sprint088_completion_updates_current_state_without_rtm_generation_authority(self):
        self.assertTrue(BLK077.exists(), "BLK-077 post-078 roadmap missing")
        self.assertTrue(BLK079.exists(), "BLK-079 current-state authority index missing")
        self.assertTrue(BLK088.exists(), "BLK-088 RTM authority request boundary missing")

        roadmap_text = BLK077.read_text()
        index_text = BLK079.read_text()
        doctrine_text = BLK088.read_text()
        required_roadmap_markers = [
            "BLK-SYSTEM-088 packaged the BLK-SYSTEM-087 local BEO publication-pilot evidence into an RTM authority request",
            "docs/BLK-088_rtm-authority-request-after-local-beo-pilot-prerequisites.md",
            "python/rtm_authority_request_after_beo_pilot.py",
            "RTM_AUTHORITY_REQUEST_READY_AFTER_LOCAL_BEO_PILOT_PREREQUISITES_NOT_GRANTED",
            "EXPLICIT_HUMAN_RTM_GENERATION_APPROVAL_REQUIRED_NOT_GRANTED",
            "no RTM generation or drift rejection",
            "no active-vault hash comparison or coverage claim",
            "no protected-body reads",
            "no external authoritative publication",
            "no target-repo scan or mutation",
            "no tooling authority",
            "production-isolation claim",
        ]
        missing_roadmap = [marker for marker in required_roadmap_markers if marker not in roadmap_text]
        self.assertEqual(missing_roadmap, [], f"BLK-077 post-088 markers missing: {missing_roadmap}")

        required_index_markers = [
            "Post-BLK-SYSTEM-088 current-state update",
            "BLK-SYSTEM-088 completed the RTM Authority Request After Local BEO Pilot Prerequisites",
            "docs/BLK-088_rtm-authority-request-after-local-beo-pilot-prerequisites.md",
            "python/rtm_authority_request_after_beo_pilot.py",
            "RTM_AUTHORITY_REQUEST_READY_AFTER_LOCAL_BEO_PILOT_PREREQUISITES_NOT_GRANTED",
            "RTM-AUTHORITY-REQUEST-AFTER-BEO-PILOT-088-001",
            "REQUEST_ONLY_NOT_GRANTED",
            "no RTM generation or drift rejection",
            "no active-vault hash comparison or coverage claim",
            "no package/network/model/browser/cyber tooling",
            "no production isolation authority",
        ]
        missing_index = [marker for marker in required_index_markers if marker not in index_text]
        self.assertEqual(missing_index, [], f"BLK-079 post-088 markers missing: {missing_index}")

        required_doctrine_markers = [
            "RTM_AUTHORITY_REQUEST_READY_AFTER_LOCAL_BEO_PILOT_PREREQUISITES_NOT_GRANTED",
            "NO_RUNTIME_RTM_GENERATION_BY_BLK_SYSTEM_088",
            "NO_RTM_DRIFT_REJECTION_OR_DRIFT_DECISION_AUTHORITY",
            "NO_ACTIVE_VAULT_HASH_COMPARISON_OR_COVERAGE_CLAIM_AUTHORITY",
            "NO_TARGET_REPO_SCAN_OR_MUTATION_AUTHORITY",
            "NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY",
            "NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM",
        ]
        missing_doctrine = [marker for marker in required_doctrine_markers if marker not in doctrine_text]
        self.assertEqual(missing_doctrine, [], f"BLK-088 doctrine markers missing: {missing_doctrine}")

        forbidden = [
            "BLK-SYSTEM-088 authorizes RTM generation",
            "BLK-SYSTEM-088 authorizes drift rejection",
            "BLK-SYSTEM-088 authorizes active-vault hash comparison",
            "BLK-SYSTEM-088 authorizes protected-body reads",
            "BLK-SYSTEM-088 authorizes target-repo scan",
        ]
        leaked = [marker for marker in forbidden if marker in roadmap_text or marker in index_text]
        self.assertEqual(leaked, [], f"BLK-SYSTEM-088 leaked forbidden authority wording: {leaked}")

    def test_sprint087_exact_beo_publication_pilot_execution_is_local_only(self):
        self.assertTrue(BLK087.exists(), "BLK-087 exact BEO publication pilot execution missing")
        text = BLK087.read_text()
        required = [
            "BLK-087 — Exact BEO Publication Pilot Execution",
            "Active exact local publication-pilot execution boundary — one BLK-086-bound pilot executed locally; not external authoritative publication and not RTM authority",
            "EXACT_BEO_PUBLICATION_PILOT_EXECUTION",
            "BEO_PUBLICATION_PILOT_EXECUTED_FOR_EXACT_BLK086_APPROVAL_LOCAL_ONLY",
            "exact_beo_publication_pilot_execution",
            "EXACT_BEO_PUBLICATION_PILOT_EXECUTION_LOCAL_ONLY_NO_SIGNER_STORAGE_LEDGER_RTM",
            "PILOT_LOCAL_PUBLISHED_BEO_OUTPUT_NOT_AUTHORITATIVE",
            "RTM_AUTHORITY_REQUEST_AFTER_PUBLISHED_BEO_PREREQUISITES_NOT_GRANTED",
            "execution_package_id: BEO-PUBLICATION-PILOT-EXECUTION-087-001",
            "approval_decision_package_id: BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-001",
            "approval_decision_package_hash: sha256:2ade9eee61d5688c32f12cf9bec1a2668d03f091d1a14fb6eeef1c7f2f1a54b9",
            "approval_id: APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001",
            "run_id_consumed: RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001",
            "python/beo_publication_pilot_execution.py",
            "BLK086_APPROVAL_DECISION_IDENTITY_AND_HASH_BOUND",
            "RUN_ID_MATCHES_BLK086_RESERVED_RUN_ID_AND_CONSUMED_ONCE",
            "LOCAL_PILOT_PUBLICATION_ARTIFACT_HASH_BOUND",
            "NO_AUTHORITATIVE_EXTERNAL_BEO_PUBLICATION_BY_BLK_SYSTEM_087",
            "NO_LIVE_EXTERNAL_PUBLICATION_APPROVAL_CAPTURE",
            "NO_SIGNER_KEY_MATERIAL_ACCESS",
            "NO_CRYPTOGRAPHIC_SIGNING_AUTHORITY",
            "NO_IMMUTABLE_STORAGE_WRITE_AUTHORITY",
            "NO_PUBLIC_LEDGER_APPEND_OR_MUTATION_AUTHORITY",
            "NO_ROLLBACK_REVOCATION_OR_SUPERSESSION_EXECUTION_AUTHORITY",
            "NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY",
            "NO_ACTIVE_VAULT_HASH_COMPARISON_OR_COVERAGE_CLAIM_AUTHORITY",
            "NO_PROTECTED_BLK_REQ_BODY_READS",
            "NO_TARGET_REPO_SCAN_OR_MUTATION_AUTHORITY",
            "NO_SOURCE_OR_GIT_MUTATION_BY_FIXTURE",
            "NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_EXECUTION_AUTHORITY",
            "NO_BLK_PIPE_BLK_TEST_OR_CODEX_RUNTIME_AUTHORITY",
            "NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY",
            "NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM",
            "Persistent doctrine gate marker: BLK-SYSTEM-087 pins exact BEO publication pilot execution as local-only and no-adjacent-authority",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-087 boundary markers missing: {missing}")

        forbidden = [
            "BLK-SYSTEM-087 authorizes external authoritative publication",
            "BLK-SYSTEM-087 authorizes signer key access",
            "BLK-SYSTEM-087 authorizes immutable storage writes",
            "BLK-SYSTEM-087 authorizes public ledger mutation",
            "BLK-SYSTEM-087 authorizes RTM generation",
            "BLK-SYSTEM-087 authorizes target-repo scan",
            "BLK-SYSTEM-087 authorizes target-repo mutation",
            "BLK-SYSTEM-087 authorizes protected-body reads",
        ]
        leaked = [marker for marker in forbidden if marker in text]
        self.assertEqual(leaked, [], f"BLK-087 leaked forbidden authority wording: {leaked}")

    def test_sprint087_completion_updates_current_state_without_rtm_authority(self):
        self.assertTrue(BLK077.exists(), "BLK-077 post-078 roadmap missing")
        self.assertTrue(BLK079.exists(), "BLK-079 current-state authority index missing")
        self.assertTrue(BLK087.exists(), "BLK-087 exact BEO publication pilot execution missing")

        roadmap_text = BLK077.read_text()
        index_text = BLK079.read_text()
        doctrine_text = BLK087.read_text()
        required_roadmap_markers = [
            "BLK-SYSTEM-087 executed the exact local BEO publication pilot bound to BLK-086",
            "docs/BLK-087_exact-beo-publication-pilot-execution.md",
            "python/beo_publication_pilot_execution.py",
            "BEO_PUBLICATION_PILOT_EXECUTED_FOR_EXACT_BLK086_APPROVAL_LOCAL_ONLY",
            "PILOT_LOCAL_PUBLISHED_BEO_OUTPUT_NOT_AUTHORITATIVE",
            "`RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001` is consumed by the local fixture",
            "automatic RTM generation",
            "no external authoritative publication",
            "no signer/storage/ledger/rollback side effects",
            "no RTM generation or drift rejection",
            "no protected-body reads",
            "no target-repo scan or mutation",
            "no tooling authority",
            "production-isolation claim",
        ]
        missing_roadmap = [marker for marker in required_roadmap_markers if marker not in roadmap_text]
        self.assertEqual(missing_roadmap, [], f"BLK-077 post-087 markers missing: {missing_roadmap}")

        required_index_markers = [
            "Post-BLK-SYSTEM-087 current-state update",
            "BLK-SYSTEM-087 completed the Exact BEO Publication Pilot Execution",
            "docs/BLK-087_exact-beo-publication-pilot-execution.md",
            "python/beo_publication_pilot_execution.py",
            "BEO_PUBLICATION_PILOT_EXECUTED_FOR_EXACT_BLK086_APPROVAL_LOCAL_ONLY",
            "execution_package_id: BEO-PUBLICATION-PILOT-EXECUTION-087-001",
            "RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001",
            "PILOT_LOCAL_PUBLISHED_BEO_OUTPUT_NOT_AUTHORITATIVE",
            "External authoritative publication remains disabled",
            "no RTM generation or drift rejection",
            "no package/network/model/browser/cyber tooling",
            "no production isolation authority",
        ]
        missing_index = [marker for marker in required_index_markers if marker not in index_text]
        self.assertEqual(missing_index, [], f"BLK-079 post-087 markers missing: {missing_index}")

        required_doctrine_markers = [
            "BEO_PUBLICATION_PILOT_EXECUTED_FOR_EXACT_BLK086_APPROVAL_LOCAL_ONLY",
            "NO_AUTHORITATIVE_EXTERNAL_BEO_PUBLICATION_BY_BLK_SYSTEM_087",
            "NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY",
            "NO_TARGET_REPO_SCAN_OR_MUTATION_AUTHORITY",
            "NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY",
            "NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM",
        ]
        missing_doctrine = [marker for marker in required_doctrine_markers if marker not in doctrine_text]
        self.assertEqual(missing_doctrine, [], f"BLK-087 doctrine markers missing: {missing_doctrine}")

        forbidden = [
            "BLK-SYSTEM-087 authorizes RTM generation",
            "BLK-SYSTEM-087 authorizes drift rejection",
            "BLK-SYSTEM-087 authorizes signer key access",
            "BLK-SYSTEM-087 authorizes target-repo scan",
            "BLK-SYSTEM-087 authorizes protected-body reads",
        ]
        leaked = [marker for marker in forbidden if marker in roadmap_text or marker in index_text]
        self.assertEqual(leaked, [], f"BLK-SYSTEM-087 leaked forbidden authority wording: {leaked}")

    def test_sprint085_completion_preserves_publication_pilot_authority_boundary(self):
        self.assertTrue(BLK077.exists(), "BLK-077 post-078 roadmap missing")
        self.assertTrue(BLK079.exists(), "BLK-079 current-state authority index missing")
        self.assertTrue(BLK085.exists(), "BLK-085 BEO publication pilot execution request gate missing")

        roadmap_text = BLK077.read_text()
        index_text = BLK079.read_text()
        doctrine_text = BLK085.read_text()
        required_roadmap_markers = [
            "BLK-SYSTEM-085 completed the BEO Publication Pilot Execution Request Gate",
            "docs/BLK-085_beo-publication-pilot-execution-request-gate.md",
            "python/beo_publication_pilot_execution_request.py",
            "BEO_PUBLICATION_PILOT_EXECUTION_REQUEST_READY_FOR_EXPLICIT_HUMAN_APPROVAL_NOT_EXECUTED",
            "beo_publication_pilot_execution_request",
            "explicit human publication pilot approval is still required",
            "no publication approval, no publication pilot execution",
            "no signer/storage/ledger/rollback side effects",
            "no RTM generation",
            "no protected-body reads",
            "no target-repo scan or mutation",
        ]
        missing_roadmap = [marker for marker in required_roadmap_markers if marker not in roadmap_text]
        self.assertEqual(missing_roadmap, [], f"BLK-077 post-085 markers missing: {missing_roadmap}")

        required_index_markers = [
            "Post-BLK-SYSTEM-085 current-state update",
            "BLK-SYSTEM-085 completed the BEO Publication Pilot Execution Request Gate",
            "docs/BLK-085_beo-publication-pilot-execution-request-gate.md",
            "python/beo_publication_pilot_execution_request.py",
            "BLK-085 BEO publication pilot execution request gate",
            "L0/L1 request gate complete; not publication approval and not publication execution",
            "explicit human publication pilot approval is still required",
            "No publication approval, no publication pilot execution",
        ]
        missing_index = [marker for marker in required_index_markers if marker not in index_text]
        self.assertEqual(missing_index, [], f"BLK-079 post-085 markers missing: {missing_index}")

        required_doctrine_markers = [
            "BEO_PUBLICATION_PILOT_EXECUTION_REQUEST_GATE",
            "NO_PUBLICATION_APPROVAL_GRANTED",
            "NO_PUBLICATION_PILOT_EXECUTION_PERFORMED",
            "NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY",
            "NO_TARGET_REPO_SCAN_OR_MUTATION_AUTHORITY",
        ]
        missing_doctrine = [marker for marker in required_doctrine_markers if marker not in doctrine_text]
        self.assertEqual(missing_doctrine, [], f"BLK-085 doctrine markers missing: {missing_doctrine}")

        forbidden = [
            "BLK-SYSTEM-085 grants publication approval",
            "BLK-SYSTEM-085 authorizes publication pilot execution",
            "BLK-SYSTEM-085 authorizes signer key access",
            "BLK-SYSTEM-085 authorizes immutable storage writes",
            "BLK-SYSTEM-085 authorizes public ledger mutation",
            "BLK-SYSTEM-085 authorizes RTM generation",
            "BLK-SYSTEM-085 authorizes target-repo scan",
            "BLK-SYSTEM-085 authorizes target-repo mutation",
            "BLK-SYSTEM-085 authorizes protected-body reads",
        ]
        leaked = [marker for marker in forbidden if marker in roadmap_text or marker in index_text]
        self.assertEqual(leaked, [], f"BLK-SYSTEM-085 leaked forbidden authority wording: {leaked}")

    def test_sprint084_completion_preserves_post083_frontier_authority_boundary(self):
        self.assertTrue(BLK077.exists(), "BLK-077 post-078 roadmap missing")
        self.assertTrue(BLK079.exists(), "BLK-079 current-state authority index missing")
        self.assertTrue(BLK084.exists(), "BLK-084 post-083 selection gate missing")

        hostile_review = ROOT / "docs" / "reviews" / "BLK-SYSTEM-084_hostile-review.md"
        closeout = ROOT / "docs" / "outcomes" / "BLK-SYSTEM-084_sprint-closeout.md"
        self.assertTrue(hostile_review.exists(), "BLK-SYSTEM-084 hostile review missing")
        self.assertTrue(closeout.exists(), "BLK-SYSTEM-084 sprint closeout missing")

        roadmap_text = BLK077.read_text()
        index_text = BLK079.read_text()
        hostile_review_text = hostile_review.read_text()
        closeout_text = closeout.read_text()
        required_roadmap_markers = [
            "BLK-SYSTEM-084 administrative closeout is complete",
            "docs/BLK-084_post-083-frontier-selection-gate-refresh.md",
            "python/blk_post083_frontier_selection_gate.py",
            "POST_083_FRONTIER_SELECTION_READY_FOR_HUMAN_DECISION_NOT_AUTHORITY",
            "next logical sprint is not approval",
            "docs/reviews/BLK-SYSTEM-084_hostile-review.md",
            "docs/outcomes/BLK-SYSTEM-084_sprint-closeout.md",
            "BLK-001 prioritization guidance, not authority",
            "end-to-end V-model closure",
            "beo_publication_pilot_execution_request",
            "rtm_authority_request_after_publication_prerequisites",
            "This guidance grants no BEB writing or dispatch",
            "no BEO writing, closeout, or publication",
            "Actual higher-authority frontier execution still requires a separate explicit human decision naming exactly one frontier",
            "No publication approval, no publication pilot execution, no BLK-test runtime, no Codex execution, no BLK-pipe dispatch, no RTM generation, no protected-body reads, no target-repo scan or mutation authority is granted",
        ]
        missing_roadmap = [marker for marker in required_roadmap_markers if marker not in roadmap_text]
        self.assertEqual(missing_roadmap, [], f"BLK-077 post-084 markers missing: {missing_roadmap}")

        required_index_markers = [
            "Post-BLK-SYSTEM-084 current-state update",
            "BLK-SYSTEM-084 administrative closeout is complete",
            "docs/BLK-084_post-083-frontier-selection-gate-refresh.md",
            "python/blk_post083_frontier_selection_gate.py",
            "BLK-084 post-083 frontier selection gate refresh",
            "L0/L1 post-083 frontier selection fixture complete; closeout complete",
            "next logical sprint is not approval",
            "docs/reviews/BLK-SYSTEM-084_hostile-review.md",
            "docs/outcomes/BLK-SYSTEM-084_sprint-closeout.md",
            "BLK-001 prioritization guidance, not authority",
            "end-to-end V-model closure",
            "beo_publication_pilot_execution_request",
            "rtm_authority_request_after_publication_prerequisites",
            "This guidance grants no BEB writing or dispatch",
            "no BEO writing, closeout, or publication",
            "No publication approval, no publication pilot execution, no BLK-test runtime, no Codex execution, no BLK-pipe dispatch, no RTM generation, no protected-body reads, no target-repo scan or mutation authority is granted",
        ]
        missing_index = [marker for marker in required_index_markers if marker not in index_text]
        self.assertEqual(missing_index, [], f"BLK-079 post-084 markers missing: {missing_index}")

        required_closeout_markers = [
            "BLK-SYSTEM-084 administrative closeout is complete",
            "final hostile review passed at `c77cf82`",
            "843 Python tests",
            "go test ./...",
            "go vet ./...",
            "git diff --check",
            "No publication approval, no publication pilot execution, no BLK-test runtime, no Codex execution, no BLK-pipe dispatch, no RTM generation, no protected-body reads, no target-repo scan or mutation authority is granted",
        ]
        missing_closeout = [marker for marker in required_closeout_markers if marker not in hostile_review_text + closeout_text]
        self.assertEqual(missing_closeout, [], f"BLK-SYSTEM-084 closeout markers missing: {missing_closeout}")

        forbidden = [
            "BLK-SYSTEM-084 grants publication approval",
            "BLK-SYSTEM-084 authorizes publication pilot execution",
            "BLK-SYSTEM-084 authorizes BLK-test runtime",
            "BLK-SYSTEM-084 authorizes Codex execution",
            "BLK-SYSTEM-084 authorizes BLK-pipe dispatch",
            "BLK-SYSTEM-084 authorizes RTM generation",
            "BLK-SYSTEM-084 authorizes target-repo scan",
            "BLK-SYSTEM-084 authorizes target-repo mutation",
            "BLK-SYSTEM-084 authorizes protected-body reads",
            "0b79038c9779eb6dc2f9ba091a46c443f16c686c",
            "final hostile re-review after `0b79038`",
            "administrative closeout remains pending",
            "administrative closeout pending",
            "latest pushed pre-closeout BLK-SYSTEM-084",
            "immediate next work remains BLK-SYSTEM-084 administrative closeout",
        ]
        leaked = [marker for marker in forbidden if marker in roadmap_text or marker in index_text]
        self.assertEqual(leaked, [], f"BLK-SYSTEM-084 leaked forbidden authority/stale-closeout wording: {leaked}")

    def test_sprint044_blk_test_pilot_authority_request_boundary_denies_runtime_authority(self):
        self.assertTrue(BLK047.exists(), "BLK-047 BLK-test pilot authority request boundary missing")
        text = BLK047.read_text()
        required = [
            "BLK-test Fixed-Tool Pilot Authority Request Boundary",
            "Active request-boundary contract — review package only; not runtime BLK-test authority",
            "BLK_TEST_FIXED_TOOL_PILOT_AUTHORITY_REQUEST_PACKAGE",
            "BLK_TEST_PILOT_REQUEST_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY",
            "FIXED_TOOL_PILOT_APPROVAL_REQUIRED_BEFORE_TRANSPORT",
            "PRODUCTION_BLK_TEST_MCP_REMAINS_DISABLED",
            "BLK_TEST_EVIDENCE_ONLY_NO_SOURCE_MUTATION",
            "PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN",
            "BEO_PUBLICATION_AND_RTM_REMAIN_SEPARATE_AUTHORITIES",
            "PHYSICAL_ISOLATION_PROOF_REQUIRED_BEFORE_PILOT",
            "REPLAY_EXPIRY_AND_SOURCE_BINDING_REQUIRED",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_044",
            "No production BLK-test MCP authority",
            "No live BLK-test server or client startup",
            "No fixed-tool execution",
            "No source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime RTM generation or RTM drift rejection",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
            "Persistent doctrine gate marker: BLK-SYSTEM-044 pins BLK-test fixed-tool pilot authority request review-only scope",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-047 boundary markers missing: {missing}")

    def test_sprint045_authority_frontier_selection_gate_denies_runtime_authority(self):
        self.assertTrue(BLK048.exists(), "BLK-048 authority frontier selection gate boundary missing")
        text = BLK048.read_text()
        required = [
            "Authority Frontier Selection Gate Boundary",
            "Active selection-gate contract — review/decision routing only; not runtime authority",
            "BLK_SYSTEM_AUTHORITY_FRONTIER_SELECTION_GATE",
            "FRONTIER_SELECTION_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY",
            "EXACTLY_ONE_FRONTIER_REQUIRED",
            "RUNTIME_APPROVAL_NOT_INFERRED_FROM_NEXT_SPRINT",
            "BLK_TEST_REQUEST_READY_IS_NOT_PILOT_APPROVAL",
            "CODEX_REVIEW_READY_IS_NOT_LIVE_EXECUTION_APPROVAL",
            "BEO_AND_RTM_BLOCKED_UNTIL_VERIFICATION_FRONTIER_APPROVED",
            "PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN",
            "ADJACENT_AUTHORITY_INHERITANCE_FORBIDDEN",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_045",
            "No live Codex execution authority",
            "No production BLK-test MCP authority",
            "No BLK-test fixed-tool execution authority",
            "No authoritative BEO publication authority",
            "No runtime RTM generation or drift rejection authority",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
            "Persistent doctrine gate marker: BLK-SYSTEM-045 pins authority frontier selection as review-only and non-runtime",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-048 boundary markers missing: {missing}")

    def test_sprint046_blk_test_fixed_tool_pilot_l3_l4_boundary_scopes_synthetic_runtime(self):
        self.assertTrue(BLK049.exists(), "BLK-049 BLK-test fixed-tool pilot L3/L4 boundary missing")
        text = BLK049.read_text()
        required = [
            "BLK-test Fixed-Tool Pilot L3/L4 Boundary",
            "Active bounded pilot boundary — L3 synthetic fixed-tool execution only; L4 real-repo pilot blocked pending exact target approval",
            "BLK_TEST_FIXED_TOOL_PILOT_L3_L4_BOUNDARY",
            "BLK_TEST_FRONTIER_SELECTED_BY_OPERATOR",
            "L3_SYNTHETIC_FIXED_TOOL_PILOT_ONLY_THIS_SPRINT",
            "L4_REAL_REPO_PILOT_BLOCKED_PENDING_EXACT_TARGET_APPROVAL",
            "FIXED_TOOL_REGISTRY_RUN_AST_VALIDATION_ONLY",
            "SOURCE_BOUND_REPLAY_PROTECTED_APPROVAL_REQUIRED",
            "SYNTHETIC_WORKSPACE_ISOLATION_REQUIRED",
            "BLK_TEST_EVIDENCE_ONLY_NO_SOURCE_MUTATION",
            "PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN",
            "BEO_PUBLICATION_AND_RTM_REMAIN_SEPARATE_AUTHORITIES",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_046",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No arbitrary shell or caller-supplied commands",
            "No L4 real-repo runtime without exact target approval",
            "No source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime RTM generation or RTM drift rejection",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
            "Persistent doctrine gate marker: BLK-SYSTEM-046 pins BLK-test fixed-tool pilot as L3 synthetic-only with L4 real-repo runtime blocked",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-049 boundary markers missing: {missing}")

    def test_sprint047_blk_test_l4_real_repo_approval_boundary_blocks_runtime_without_exact_target(self):
        self.assertTrue(BLK050.exists(), "BLK-050 BLK-test L4 real-repo approval boundary missing")
        text = BLK050.read_text()
        required = [
            "BLK-test Fixed-Tool Pilot L4 Real-Repo Approval Boundary",
            "Active L4 approval-boundary contract — exact-target real-repo preflight only; no runtime execution this sprint",
            "BLK_TEST_FIXED_TOOL_PILOT_L4_REAL_REPO_APPROVAL_BOUNDARY",
            "L4_REAL_REPO_APPROVAL_BOUNDARY_ONLY_NO_RUNTIME_THIS_SPRINT",
            "EXACT_TARGET_REPO_PATH_BRANCH_WORKSPACE_REQUIRED",
            "READ_ONLY_FIXED_TOOL_RUN_AST_VALIDATION_ONLY",
            "REAL_REPO_SOURCE_MUTATION_FORBIDDEN",
            "PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN",
            "BEO_PUBLICATION_AND_RTM_REMAIN_SEPARATE_AUTHORITIES",
            "EXACT_TARGET_APPROVAL_DOES_NOT_AUTHORIZE_PRODUCTION_MCP",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_047",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No arbitrary shell or caller-supplied commands",
            "No real-repo BLK-test runtime in BLK-SYSTEM-047 without a complete exact target approval envelope",
            "No source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime RTM generation or RTM drift rejection",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
            "Persistent doctrine gate marker: BLK-SYSTEM-047 pins L4 real-repo pilot as approval-boundary-only until exact target approval exists",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-050 boundary markers missing: {missing}")

    def test_sprint048_blk_test_l4_disposable_real_repo_runtime_boundary_scopes_runtime(self):
        self.assertTrue(BLK051.exists(), "BLK-051 BLK-test L4 disposable real-repo runtime boundary missing")
        text = BLK051.read_text()
        required = [
            "BLK-test Fixed-Tool L4 Disposable Real-Repo Runtime Boundary",
            "Active bounded L4 runtime boundary — disposable exact-target real-repo only; not production BLK-test MCP",
            "BLK_TEST_FIXED_TOOL_L4_DISPOSABLE_REAL_REPO_RUNTIME_BOUNDARY",
            "L4_DISPOSABLE_REAL_REPO_RUN_AST_VALIDATION_ONLY_THIS_SPRINT",
            "EXACT_TARGET_DISPOSABLE_GIT_REPO_REQUIRED",
            "READ_ONLY_FIXED_TOOL_RUN_AST_VALIDATION_ONLY",
            "REPLAY_CONSUMED_BEFORE_RUNTIME",
            "NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST",
            "PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN",
            "BEO_PUBLICATION_AND_RTM_REMAIN_SEPARATE_AUTHORITIES",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_048",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No arbitrary shell or caller-supplied commands",
            "No execution against /home/dad/BLK-System or arbitrary operator repositories",
            "No source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime RTM generation or RTM drift rejection",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
            "Persistent doctrine gate marker: BLK-SYSTEM-048 pins L4 runtime to one disposable exact-target real-repo run_ast_validation pilot",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-051 boundary markers missing: {missing}")

    def test_sprint049_blk_test_l4_evidence_trust_request_gate_blocks_runtime(self):
        self.assertTrue(BLK052.exists(), "BLK-052 BLK-test L4 evidence trust request gate missing")
        text = BLK052.read_text()
        required = [
            "BLK-test L4 Evidence Trust and Non-Disposable Request Gate",
            "Active request-gate boundary — evidence trust review only; no non-disposable runtime this sprint",
            "BLK_TEST_L4_EVIDENCE_TRUST_AND_NON_DISPOSABLE_REQUEST_GATE",
            "NON_DISPOSABLE_L4_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME",
            "DISPOSABLE_L4_EVIDENCE_TRUST_REVIEW_ONLY",
            "NO_NON_DISPOSABLE_RUNTIME_THIS_SPRINT",
            "EXACT_TARGET_NON_DISPOSABLE_REPO_REQUIRED_FOR_FUTURE_RUNTIME",
            "BEO_PUBLICATION_AND_RTM_REMAIN_SEPARATE_AUTHORITIES",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_049",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No non-disposable runtime execution authority",
            "No source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime RTM generation or RTM drift rejection",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
            "Persistent doctrine gate marker: BLK-SYSTEM-049 pins non-disposable L4 advancement to evidence-trust request readiness only",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-052 boundary markers missing: {missing}")

    def test_sprint050_non_disposable_l4_exact_target_approval_envelope_blocks_runtime(self):
        self.assertTrue(BLK053.exists(), "BLK-053 non-disposable L4 exact-target approval envelope boundary missing")
        text = BLK053.read_text()
        required = [
            "Non-Disposable L4 Exact-Target Approval Envelope Boundary",
            "Active approval-envelope boundary — human-review package only; no non-disposable runtime this sprint",
            "BLK_TEST_NON_DISPOSABLE_L4_EXACT_TARGET_APPROVAL_ENVELOPE",
            "NON_DISPOSABLE_L4_EXACT_TARGET_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME",
            "EXACTLY_ONE_NON_DISPOSABLE_TARGET_REQUIRED",
            "APPROVAL_ENVELOPE_DOES_NOT_AUTHORIZE_RUNTIME",
            "READ_ONLY_RUN_AST_VALIDATION_ONLY_FUTURE_RUNTIME",
            "NO_NON_DISPOSABLE_RUNTIME_THIS_SPRINT",
            "BEO_PUBLICATION_AND_RTM_REMAIN_SEPARATE_AUTHORITIES",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_050",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No non-disposable runtime execution authority",
            "No live Codex execution authority",
            "No source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime RTM generation or RTM drift rejection",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
            "Persistent doctrine gate marker: BLK-SYSTEM-050 pins non-disposable L4 advancement to exact-target approval-envelope review only",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-053 boundary markers missing: {missing}")

    def test_sprint051_non_disposable_l4_runtime_pilot_is_exact_one_run_evidence_only(self):
        self.assertTrue(BLK054.exists(), "BLK-054 non-disposable L4 runtime pilot boundary missing")
        text = BLK054.read_text()
        required = [
            "BLK-test Non-Disposable L4 Runtime Pilot Boundary",
            "Active one-run L4 pilot runtime boundary — exact target only; evidence only; not production BLK-test MCP",
            "BLK_TEST_NON_DISPOSABLE_L4_RUNTIME_PILOT",
            "BLK_TEST_NON_DISPOSABLE_L4_RUNTIME_PILOT_PASS_EVIDENCE_ONLY",
            "APPROVED_ONE_RUN_ONLY_APPROVAL_BLK_SYSTEM_051_001",
            "RUN_ID_RUN_BLK_SYSTEM_051_001_CONSUMED_BEFORE_RUNTIME",
            "TARGET_REPO_PATH_HOME_DAD_BLK_SYSTEM",
            "SOURCE_SUBTREE_PATH_HOME_DAD_BLK_SYSTEM_PYTHON",
            "TARGET_HEAD_75E44C4066F7CBAD38ED15AFDC93A8EAFD703340_REQUIRED",
            "WORKSPACE_CLONE_PATH_TMP_BLK_SYSTEM_051_NON_DISPOSABLE_L4_RUNTIME_WORKSPACE",
            "READ_ONLY_RUN_AST_VALIDATION_ONLY",
            "WRAPPER_OWNED_WORKSPACE_MARKER_NONCE_REQUIRED",
            "SOURCE_AND_GIT_SNAPSHOTS_MUST_MATCH_AFTER_RUNTIME",
            "WORKSPACE_CLEANUP_REQUIRED_ON_PASS_FAIL_BLOCKED_TIMEOUT_OUTPUT_OVERFLOW",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_051",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No reusable BLK-test service startup",
            "No second or reusable non-disposable runtime run",
            "No live Codex execution authority",
            "No arbitrary shell or caller-supplied commands",
            "No source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime RTM generation or RTM drift rejection",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-054 boundary markers missing: {missing}")

    def test_sprint053_repeatable_non_disposable_l4_wrapper_approval_cleanup_is_not_runtime_authority(self):
        self.assertTrue(BLK056.exists(), "BLK-056 repeatable non-disposable L4 wrapper approval boundary missing")
        text = BLK056.read_text()
        required = [
            "Repeatable Non-Disposable L4 Wrapper Approval Boundary",
            "Active wrapper-hardening boundary — repeatable approval-envelope support only; no new runtime run",
            "BLK_TEST_REPEATABLE_NON_DISPOSABLE_L4_WRAPPER_APPROVAL_BOUNDARY",
            "REPEATABLE_APPROVAL_ENVELOPE_SUPPORT_READY_NOT_RUNTIME_AUTHORITY",
            "Typed L4RuntimeApprovalEnvelope required for future fresh approvals",
            "Envelope fixed_tool must remain run_ast_validation",
            "workspace_marker_name must be a single hidden filename inside the wrapper-owned workspace",
            "Future envelopes must bind sprint, approval_id, run_id, expected_head, approved paths, replay ledger path, marker nonce binding, and workspace marker name",
            "marker_nonce_binding must equal the approval envelope sprint, not a weak substring",
            "approval_id and run_id must bind to the approval envelope sprint and public fresh-envelope construction must not reuse consumed BLK-SYSTEM-051 or BLK-SYSTEM-052 IDs",
            "The internal legacy BLK-SYSTEM-051 default envelope is retained only to preserve historical tests/callers and must not be used as a fresh approval path",
            "replay_ledger_path must not overlap target_repo_path, source_subtree_path, `.git`, protected BLK-req descendants, or workspace_clone_path",
            "Legacy BLK-SYSTEM-051 wrapper path remains historical compatibility only",
            "No reuse of BLK-SYSTEM-051 or BLK-SYSTEM-052 consumed approval/run IDs",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_053_WRAPPER_APPROVAL_CLEANUP",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No reusable BLK-test service startup",
            "No new non-disposable runtime run",
            "No live Codex execution authority",
            "No arbitrary shell or caller-supplied commands",
            "No dynamic tool expansion",
            "No source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime RTM generation or RTM drift rejection",
            "No public ledger mutation",
            "No package-manager, network, model-service, browser, or cyber tooling authority",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-056 boundary markers missing: {missing}")

    def test_sprint054_authoritative_beo_publication_authority_request_is_not_publication(self):
        self.assertTrue(BLK057.exists(), "BLK-057 authoritative BEO publication authority request boundary missing")
        text = BLK057.read_text()
        required = [
            "Authoritative BEO Publication Authority Request Boundary",
            "Active authority-request boundary — human-review package only; not publication authority",
            "AUTHORITATIVE_BEO_PUBLICATION_AUTHORITY_REQUEST_BOUNDARY",
            "AUTHORITATIVE_BEO_PUBLICATION_AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_PUBLICATION",
            "Publication-specific approval request cannot be inherited from BLK-test PASS, BLK-pipe success, Codex approval, publication candidate fixtures, or published-input fixtures",
            "excluded_authorities must equal the exact denied authority set",
            "No authoritative BEO publication",
            "No runtime `PUBLISHED` BEO output",
            "No live publication approval capture",
            "No signer key material access",
            "No cryptographic signing",
            "No immutable storage writes",
            "No public ledger mutation",
            "No rollback, revocation, or supersession execution",
            "No runtime RTM generation or RTM drift rejection",
            "No active-vault hash comparison, coverage matrix, coverage claim, or drift decision",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No live Codex execution authority",
            "No source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_054_BEO_PUBLICATION_AUTHORITY_REQUEST",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-057 boundary markers missing: {missing}")

    def test_sprint071_blk_test_kuronode_workspace_pilot_request_is_module_request_not_blk_system_test(self):
        self.assertTrue(BLK072.exists(), "BLK-072 BLK-test Kuronode workspace pilot request boundary missing")
        text = BLK072.read_text()
        required = [
            "BLK-test Kuronode Workspace Read-Only Pilot Request Boundary",
            "Active request/doctrine/fixture boundary — human-review package only; no Kuronode BLK-test runtime this sprint",
            "BLK_TEST_KURONODE_WORKSPACE_PILOT_REQUEST_BOUNDARY",
            "BLK_TEST_KURONODE_WORKSPACE_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME",
            "BLK-test is a BLK-System functional module, not BLK-System's test suite",
            "BLK_TEST_MODULE_NOT_BLK_SYSTEM_TEST_SUITE",
            "KURONODE_WORKSPACE_EXACT_TARGET_BOUND",
            "READ_ONLY_FIXED_TOOL_ONLY",
            "NO_CEB009_REUSE",
            "NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST",
            "NO_PROTECTED_BODY_READ",
            "BEO_RTM_AND_COVERAGE_AUTHORITY_SEPARATE",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_071_KURONODE_WORKSPACE_PILOT_REQUEST",
            "/home/dad/code/Kuronode-v1",
            "38e332b188e45edcb484765694112c9041ad1a3b",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No reusable BLK-test service startup",
            "No Kuronode BLK-test runtime execution in BLK-SYSTEM-071",
            "No CEB_009 approval IDs, run IDs, BLK-pipe payloads, reports, or patch authority reused as executable BLK-test fixture input",
            "No source mutation, staging, commit, push, reset, stash, checkout, revert, cleanup, or autofix by BLK-test",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime RTM generation or RTM drift rejection",
            "No coverage matrix, coverage claim, active-vault hash comparison, or drift decision",
            "No Electron launch, no smoke-test execution, no TypeScript tooling, no package-manager invocation, no network/model/browser/cyber tooling",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
            "Persistent doctrine gate marker: BLK-SYSTEM-071 pins BLK-test Kuronode workspace work to module request readiness only, not BLK-System test-suite semantics and not runtime",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-072 boundary markers missing: {missing}")
        forbidden_claims = [
            r"runtime approved by operator",
            r"live run permitted",
            r"source writes enabled",
            r"git staging enabled",
            r"BEO is PUBLISHED",
            r"published BEO output enabled",
            r"BEO publication granted",
            r"RTM generated",
            r"coverage is complete",
            r"coverage truth established",
            r"drift decision made",
            r"read \.env secrets",
            r"SECRET_KEY",
            r"APPROVED_FOR_LIVE_EXECUTION",
        ]
        offenders = [pattern for pattern in forbidden_claims if re.search(pattern, text, re.IGNORECASE)]
        self.assertEqual(offenders, [], f"BLK-072 contains forbidden authority claims: {offenders}")

    def test_sprint072_blk_test_kuronode_workspace_exact_target_approval_envelope_is_review_only(self):
        self.assertTrue(BLK073.exists(), "BLK-073 Kuronode workspace exact-target approval envelope boundary missing")
        text = BLK073.read_text()
        required = [
            "BLK-test Kuronode Workspace Exact-Target Approval Envelope Boundary",
            "Active approval-envelope fixture boundary — human-review package only; no Kuronode BLK-test runtime this sprint",
            "BLK_TEST_KURONODE_WORKSPACE_EXACT_TARGET_APPROVAL_ENVELOPE_BOUNDARY",
            "BLK_TEST_KURONODE_WORKSPACE_EXACT_TARGET_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME",
            "BLK-test is a BLK-System functional module, not BLK-System's test suite",
            "UPSTREAM_REQUEST_HASH_RECOMPUTED",
            "EXACT_KURONODE_TARGET_BOUND",
            "FRESH_BLK_SYSTEM_072_APPROVAL_ID_REQUIRED",
            "FRESH_BLK_SYSTEM_072_RUN_ID_REQUIRED",
            "REPLAY_POLICY_REVIEW_ONLY",
            "READ_ONLY_FIXED_TOOL_FUTURE_RUNTIME_ONLY",
            "NO_RUNTIME_APPROVAL_GRANTED",
            "NO_CEB009_REUSE",
            "NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST",
            "BEO_RTM_AND_COVERAGE_AUTHORITY_SEPARATE",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_072_KURONODE_WORKSPACE_EXACT_TARGET_APPROVAL_ENVELOPE",
            "/home/dad/code/Kuronode-v1",
            "38e332b188e45edcb484765694112c9041ad1a3b",
            "APPROVAL-BLK-SYSTEM-072-KURONODE-WORKSPACE-001",
            "RUN-BLK-SYSTEM-072-KURONODE-WORKSPACE-001",
            "No runtime approval",
            "No Kuronode BLK-test runtime execution in BLK-SYSTEM-072",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No CEB_009 approval IDs, run IDs, BLK-pipe payloads, reports, or patch authority reused as executable BLK-test fixture input",
            "No source mutation, staging, commit, push, reset, stash, checkout, revert, cleanup, or autofix by BLK-test",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime RTM generation or RTM drift rejection",
            "No coverage matrix, coverage claim, active-vault hash comparison, or drift decision",
            "No Electron launch, no smoke-test execution, no TypeScript tooling, no package-manager invocation, no network/model/browser/cyber tooling",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim",
            "No arbitrary shell or caller-supplied commands",
            "No dynamic tool expansion",
            "No public ledger mutation",
            "No signer, storage, rollback, revocation, supersession, or release authority",
            "No live Codex execution authority",
            "No live tactical LLM dispatch",
            "future one-use ID candidates",
            "No replay consumption occurs in BLK-SYSTEM-072",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-073 boundary markers missing: {missing}")
        forbidden_claims = [
            r"runtime approved by operator",
            r"live run permitted",
            r"source writes enabled",
            r"git staging enabled",
            r"BEO is PUBLISHED",
            r"published BEO output enabled",
            r"BEO publication granted",
            r"RTM generated",
            r"coverage truth established",
            r"drift decision made",
            r"read \.env secrets",
            r"SECRET_KEY",
            r"APPROVED_FOR_LIVE_EXECUTION",
        ]
        offenders = [pattern for pattern in forbidden_claims if re.search(pattern, text, re.IGNORECASE)]
        self.assertEqual(offenders, [], f"BLK-073 contains forbidden authority claims: {offenders}")

    def test_sprint073_blk_test_kuronode_workspace_read_only_pilot_runtime_is_evidence_only(self):
        self.assertTrue(BLK074.exists(), "BLK-074 Kuronode workspace read-only pilot runtime boundary missing")
        text = BLK074.read_text()
        required = [
            "BLK-test Kuronode Workspace Read-Only Pilot Runtime Boundary",
            "Active one-run runtime boundary — read-only evidence pilot only; no production BLK-test MCP",
            "BLK_TEST_KURONODE_WORKSPACE_READ_ONLY_PILOT_RUNTIME_BOUNDARY",
            "BLK_TEST_KURONODE_WORKSPACE_READ_ONLY_PILOT_PASS_EVIDENCE_ONLY",
            "BLK_TEST_KURONODE_WORKSPACE_READ_ONLY_PILOT_FAIL_EVIDENCE_ONLY",
            "BLK_TEST_KURONODE_WORKSPACE_READ_ONLY_PILOT_BLOCKED_EVIDENCE_ONLY",
            "BLK-test is a BLK-System functional module, not BLK-System's test suite",
            "APPROVAL-BLK-SYSTEM-073-KURONODE-WORKSPACE-001",
            "RUN-BLK-SYSTEM-073-KURONODE-WORKSPACE-001",
            "/home/dad/code/Kuronode-v1",
            "/home/dad/code/Kuronode-v1/scripts",
            "/tmp/blk-system-073-kuronode-workspace-read-only-pilot-workspace",
            "/tmp/blk-system-073-kuronode-workspace-read-only-pilot-replay-ledger.json",
            "38e332b188e45edcb484765694112c9041ad1a3b",
            "USER_REQUESTED_EXECUTE_ALL_TASKS_FOR_BLK_SYSTEM_073",
            "UPSTREAM_BLK_SYSTEM_072_ENVELOPE_BOUND_NOT_RUNTIME_APPROVAL",
            "KURONODE_ORIGIN_MAIN_HEAD_RECHECKED",
            "READ_ONLY_RUN_AST_VALIDATION_ONLY",
            "REPLAY_CONSUMED_BEFORE_RUNTIME",
            "NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST",
            "NO_PROTECTED_BODY_READ",
            "NO_BEO_RTM_COVERAGE_DRIFT_AUTHORITY",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_073_KURONODE_WORKSPACE_READ_ONLY_PILOT_RUNTIME",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No reusable BLK-test service startup",
            "No arbitrary shell or caller-supplied commands",
            "No dynamic tool expansion",
            "No Electron launch, no Playwright launch, no smoke-test execution, no TypeScript compiler, no linter, no formatter, no package-manager invocation",
            "No network/model/browser/cyber tooling",
            "No Kuronode source mutation",
            "No Kuronode Git mutation, staging, commit, push, reset, checkout, revert, stash, cleanup, autofix, or remote writes by BLK-test",
            "No CEB_009, BLK-SYSTEM-070, BLK-SYSTEM-071, or BLK-SYSTEM-072 artifact reuse as executable runtime authority",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime PUBLISHED BEO output",
            "No RTM generation or RTM drift rejection",
            "No coverage matrix, coverage claim, active-vault hash comparison, or drift decision",
            "No public ledger mutation",
            "No signer, storage, rollback, revocation, supersession, or release authority",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation proof",
            "Replay IDs are consumed before runtime and cannot be reused even if the pilot BLOCKS",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-074 boundary markers missing: {missing}")
        forbidden_claims = [
            r"BLK-test validates BLK-System",
            r"BLK-System test suite",
            r"production BLK-test MCP is authorized",
            r"generic BLK-test MCP is authorized",
            r"source writes enabled",
            r"git staging enabled",
            r"BEO is PUBLISHED",
            r"RTM generated",
            r"coverage truth established",
            r"drift decision made",
            r"production sandbox is proven",
            r"read \.env secrets",
            r"APPROVED_FOR_LIVE_EXECUTION",
        ]
        offenders = [pattern for pattern in forbidden_claims if re.search(pattern, text, re.IGNORECASE)]
        self.assertEqual(offenders, [], f"BLK-074 contains forbidden authority claims: {offenders}")

    def test_sprint074_kuronode_lifecycle_cleanup_remediation_packet_is_fixture_only(self):
        self.assertTrue(BLK075.exists(), "BLK-075 Kuronode lifecycle cleanup remediation boundary missing")
        text = BLK075.read_text()
        required = [
            "BLK-test Kuronode Lifecycle Cleanup Remediation Boundary",
            "Active fixture-only remediation boundary — review-ready packet only; no Kuronode patch authority",
            "BLK_TEST_KURONODE_LIFECYCLE_CLEANUP_REMEDIATION_BOUNDARY",
            "KURONODE_LIFECYCLE_CLEANUP_REMEDIATION_PACKET_READY_NOT_PATCHED",
            "BLK-test is a BLK-System functional module, not BLK-System's test suite",
            "smoke_test.ts:53 LIFECYCLE_CLEANUP_REQUIRED",
            "APPROVAL-BLK-SYSTEM-073-KURONODE-WORKSPACE-001",
            "RUN-BLK-SYSTEM-073-KURONODE-WORKSPACE-001",
            "RETIRED_IDS_MUST_NOT_BE_REUSED",
            "SOURCE_EVIDENCE_HASH_RECOMPUTED",
            "EXACT_LIFECYCLE_FINDING_BOUND",
            "FRESH_RUNTIME_IDS_REQUIRED_BY_SEPARATE_AUTHORITY_NOT_ALLOCATED",
            "NO_PILOT_RERUN",
            "NO_PATCH_APPROVAL_GRANTED",
            "NO_KURONODE_SOURCE_OR_GIT_MUTATION",
            "NO_PROTECTED_BODY_READ",
            "NO_BEO_RTM_COVERAGE_DRIFT_AUTHORITY",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_074_KURONODE_LIFECYCLE_CLEANUP_REMEDIATION",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No reusable BLK-test service startup",
            "No arbitrary shell or caller-supplied commands",
            "No Electron launch, no smoke-test execution, no TypeScript compiler, no linter, no formatter, no package-manager invocation",
            "No network/model/browser/cyber tooling",
            "No live Codex execution authority",
            "No BLK-pipe execution",
            "No Kuronode source mutation",
            "No Kuronode Git mutation, staging, commit, push, reset, checkout, revert, stash, cleanup, autofix, or remote writes",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime PUBLISHED BEO output",
            "No RTM generation or RTM drift rejection",
            "No coverage matrix, coverage claim, active-vault hash comparison, or drift decision",
            "No public ledger mutation",
            "No signer, storage, rollback, revocation, supersession, or release authority",
            "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation proof",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-075 boundary markers missing: {missing}")
        from blk_test_kuronode_lifecycle_cleanup_remediation_packet import (
            EXACT_EXCLUDED_AUTHORITIES as SPRINT074_EXCLUDED_AUTHORITIES,
            PACKET_FALSE_SIDE_EFFECT_FLAGS as SPRINT074_FALSE_FLAGS,
        )

        required_authorities = {
            "DYNAMIC_TOOL_EXPANSION",
            "PROTECTED_BLK_REQ_BODY_COPY_PARSE_HASH_SUMMARIZE_SCAN_MUTATE_OR_DRIFT_COMPARE",
            "KURONODE_REVERT_STASH_AUTOFIX_OR_REMOTE_WRITE",
            "RELEASE_AUTHORITY",
            "ACTIVE_VAULT_HASH_COMPARISON",
            "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
        }
        missing_authorities = sorted(required_authorities - SPRINT074_EXCLUDED_AUTHORITIES)
        self.assertEqual(missing_authorities, [], f"BLK-SYSTEM-074 code denied-authority set missing: {missing_authorities}")
        required_false_flags = {
            "dynamic_tool_expansion_performed",
            "reusable_blk_test_service_started",
            "kuronode_revert_performed",
            "kuronode_stash_performed",
            "kuronode_autofix_performed",
            "kuronode_remote_write_performed",
            "runtime_published_beo_output_emitted",
            "public_ledger_mutated",
            "active_vault_hash_comparison_performed",
            "release_authority_exercised",
            "production_sandbox_or_host_secret_isolation_claimed",
        }
        missing_false_flags = sorted(required_false_flags - SPRINT074_FALSE_FLAGS)
        self.assertEqual(missing_false_flags, [], f"BLK-SYSTEM-074 packet false-flag set missing: {missing_false_flags}")
        forbidden_claims = [
            r"patch authority granted",
            r"pilot rerun approved",
            r"production BLK-test MCP is authorized",
            r"generic BLK-test MCP is authorized",
            r"source writes enabled",
            r"git staging enabled",
            r"BEO is PUBLISHED",
            r"RTM generated",
            r"coverage truth established",
            r"drift decision made",
            r"APPROVED_FOR_LIVE_EXECUTION",
        ]
        offenders = [pattern for pattern in forbidden_claims if re.search(pattern, text, re.IGNORECASE)]
        self.assertEqual(offenders, [], f"BLK-075 contains forbidden authority claims: {offenders}")

    def test_sprint075_kuronode_lifecycle_cleanup_patch_approval_envelope_is_review_only(self):
        self.assertTrue(BLK076.exists(), "BLK-076 Kuronode lifecycle cleanup patch approval envelope boundary missing")
        text = BLK076.read_text()
        required = [
            "Kuronode Lifecycle Cleanup Patch Approval Envelope Boundary",
            "Active review-only approval-envelope boundary — not patch approval; not patch execution",
            "KURONODE_LIFECYCLE_CLEANUP_PATCH_APPROVAL_ENVELOPE_BOUNDARY",
            "KURONODE_LIFECYCLE_CLEANUP_PATCH_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PATCHED",
            "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_075_KURONODE_LIFECYCLE_CLEANUP_PATCH_APPROVAL_ENVELOPE",
            "smoke_test.ts:53 LIFECYCLE_CLEANUP_REQUIRED",
            "/home/dad/code/Kuronode-v1",
            "38e332b188e45edcb484765694112c9041ad1a3b",
            "scripts/smoke_test.ts",
            "APPROVAL-BLK-SYSTEM-075-KURONODE-LIFECYCLE-CLEANUP-PATCH-001",
            "RUN-BLK-SYSTEM-075-KURONODE-LIFECYCLE-CLEANUP-PATCH-001",
            "FUTURE_CANDIDATE_NOT_CONSUMED",
            "UPSTREAM_REMEDIATION_PACKET_HASH_RECOMPUTED",
            "EXACT_TARGET_SHA_BOUND",
            "EXACT_PATCH_ALLOWLIST_BOUND",
            "READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PATCHED",
            "NO_PATCH_APPROVAL_GRANTED",
            "NO_PATCH_EXECUTION",
            "NO_BLK_PIPE_EXECUTION",
            "NO_CODEX_EXECUTION",
            "NO_KURONODE_SOURCE_OR_GIT_MUTATION",
            "NO_BLK_TEST_RERUN_OR_RETIRED_ID_REUSE",
            "NO_BEO_RTM_COVERAGE_DRIFT_AUTHORITY",
            "No production BLK-test MCP authority",
            "No generic BLK-test MCP authority",
            "No Electron launch, no smoke-test execution, no TypeScript compiler, no linter, no formatter, no package-manager invocation",
            "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
            "No authoritative BEO publication",
            "No runtime PUBLISHED BEO output",
            "No RTM generation or RTM drift rejection",
            "No coverage matrix, coverage claim, active-vault hash comparison, or drift decision",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-076 boundary markers missing: {missing}")
        from kuronode_lifecycle_cleanup_patch_approval_envelope import (
            EXACT_EXCLUDED_AUTHORITIES as SPRINT075_EXCLUDED_AUTHORITIES,
            PATCH_FALSE_SIDE_EFFECT_FLAGS as SPRINT075_FALSE_FLAGS,
        )
        expected_authorities = {
            "PATCH_APPROVAL_GRANTED",
            "PATCH_EXECUTION",
            "BLK_PIPE_EXECUTION",
            "CODEX_EXECUTION",
            "LIVE_TACTICAL_LLM_DISPATCH",
            "KURONODE_SOURCE_MUTATION",
            "KURONODE_GIT_MUTATION",
            "KURONODE_STAGING_COMMIT_PUSH_RESET_CHECKOUT_REVERT_STASH_CLEANUP_AUTOFIX_OR_REMOTE_WRITE",
            "BLK_SYSTEM_073_RUNTIME_ID_REUSE",
            "BLK_TEST_PILOT_RERUN",
            "PRODUCTION_BLK_TEST_MCP",
            "GENERIC_BLK_TEST_MCP",
            "REUSABLE_BLK_TEST_SERVICE_STARTUP",
            "ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS",
            "DYNAMIC_TOOL_EXPANSION",
            "ELECTRON_OR_SMOKE_TEST_EXECUTION",
            "TYPESCRIPT_TOOLING_EXECUTION",
            "PACKAGE_MANAGER_INVOCATION",
            "NETWORK_ACCESS",
            "MODEL_SERVICE_ACCESS",
            "BROWSER_OR_CYBER_TOOLING",
            "PROTECTED_BLK_REQ_BODY_READ",
            "PROTECTED_BLK_REQ_BODY_COPY_PARSE_HASH_SUMMARIZE_SCAN_MUTATE_OR_DRIFT_COMPARE",
            "AUTHORITATIVE_BEO_PUBLICATION",
            "RUNTIME_PUBLISHED_BEO_OUTPUT",
            "LIVE_PUBLICATION_APPROVAL_CAPTURE",
            "SIGNER_KEY_MATERIAL_ACCESS",
            "CRYPTOGRAPHIC_SIGNING",
            "IMMUTABLE_STORAGE_WRITE",
            "PUBLIC_LEDGER_APPEND_OR_MUTATION",
            "ROLLBACK_REVOCATION_SUPERSESSION_EXECUTION",
            "RELEASE_AUTHORITY",
            "RUNTIME_RTM_GENERATION",
            "RTM_DRIFT_REJECTION",
            "ACTIVE_VAULT_HASH_COMPARISON",
            "COVERAGE_MATRIX_OR_CLAIM",
            "DRIFT_DECISION",
            "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
        }
        self.assertEqual(SPRINT075_EXCLUDED_AUTHORITIES, expected_authorities)
        expected_false_flags = {
            "approval_granted",
            "patch_executed",
            "runtime_validation_executed",
            "blk_pipe_invoked",
            "codex_started",
            "live_tactical_llm_dispatched",
            "kuronode_source_mutation_performed",
            "kuronode_git_mutation_performed",
            "kuronode_staging_performed",
            "kuronode_commit_performed",
            "kuronode_push_performed",
            "kuronode_reset_performed",
            "kuronode_checkout_performed",
            "kuronode_revert_performed",
            "kuronode_stash_performed",
            "kuronode_cleanup_performed",
            "kuronode_autofix_performed",
            "kuronode_remote_write_performed",
            "retired_blk_system_073_id_reused",
            "blk_test_pilot_rerun_performed",
            "production_blk_test_mcp_started",
            "generic_blk_test_mcp_started",
            "reusable_blk_test_service_started",
            "arbitrary_shell_or_caller_command_executed",
            "dynamic_tool_expansion_performed",
            "electron_launched",
            "smoke_test_executed",
            "typescript_tooling_executed",
            "package_manager_invoked",
            "network_accessed",
            "model_service_called",
            "browser_or_cyber_tooling_called",
            "protected_body_read",
            "protected_body_copied_parsed_hashed_summarized_scanned_mutated_or_drift_compared",
            "beo_published",
            "runtime_published_beo_output_emitted",
            "live_publication_approval_captured",
            "signer_key_material_accessed",
            "cryptographic_signature_generated",
            "immutable_storage_written",
            "public_ledger_mutated",
            "rollback_revocation_supersession_executed",
            "release_authority_exercised",
            "rtm_generated",
            "rtm_drift_rejection_performed",
            "active_vault_hash_comparison_performed",
            "coverage_matrix_generated",
            "coverage_claim_promoted",
            "drift_decision_performed",
            "production_sandbox_or_host_secret_isolation_claimed",
        }
        self.assertEqual(SPRINT075_FALSE_FLAGS, expected_false_flags)
        forbidden_claims = [
            r"patch authority granted",
            r"patch execution approved",
            r"BLK-pipe execution authorized",
            r"source writes enabled",
            r"git staging enabled",
            r"BEO is PUBLISHED",
            r"RTM generated",
            r"coverage truth established",
            r"drift decision made",
            r"APPROVED_FOR_LIVE_EXECUTION",
        ]
        offenders = [pattern for pattern in forbidden_claims if re.search(pattern, text, re.IGNORECASE)]
        self.assertEqual(offenders, [], f"BLK-076 contains forbidden authority claims: {offenders}")

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

    def test_sprint089_090_091_rtm_sequence_boundaries_are_persistent(self):
        checks = {
            BLK089: [
                "BLK-089 — RTM Authority Approval Decision Capture",
                "Active RTM generation approval-decision boundary — exact approval capture only; not RTM generation execution",
                "RTM_GENERATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK088_REQUEST_NOT_GENERATED",
                "APPROVED_FOR_ONE_FUTURE_LOCAL_RTM_GENERATION_PILOT_NOT_GENERATED",
                "EXACT_LOCAL_RTM_GENERATION_PILOT_REQUIRED_NOT_RUN",
                "RTM-GENERATION-APPROVAL-DECISION-089-001",
                "APPROVAL-BLK-SYSTEM-088-RTM-GENERATION-001",
                "RUN-BLK-SYSTEM-088-RTM-GENERATION-001",
                "python/rtm_generation_approval_decision.py",
                "RTM_NOT_GENERATED_BY_APPROVAL_DECISION",
                "DRIFT_REJECTION_AND_DRIFT_DECISION_EXCLUDED",
            ],
            BLK090: [
                "BLK-090 — Exact Local RTM Generation Pilot",
                "Active exact local RTM generation pilot boundary — local deterministic RTM ledger evidence only; not drift rejection authority",
                "LOCAL_RTM_GENERATION_PILOT_EXECUTED_FOR_EXACT_BLK089_APPROVAL",
                "PILOT_LOCAL_RTM_LEDGER_GENERATED_NOT_AUTHORITATIVE",
                "RTM_DRIFT_REJECTION_AUTHORITY_REQUEST_REQUIRED_NOT_GRANTED",
                "RTM-GENERATION-PILOT-EXECUTION-090-001",
                "RTM-090-001",
                "python/exact_local_rtm_generation_pilot.py",
                "LOCAL_RTM_LEDGER_HASH_BOUND",
                "FUTURE_DRIFT_REJECTION_AUTHORITY_REQUEST_REQUIRED",
            ],
            BLK091: [
                "BLK-091 — RTM Drift-Rejection Authority Request",
                "Active RTM drift-rejection authority request boundary — review package only; not drift rejection approval or execution",
                "RTM_DRIFT_REJECTION_AUTHORITY_REQUEST_READY_AFTER_LOCAL_RTM_GENERATION_NOT_GRANTED",
                "DRIFT_REJECTION_REQUEST_ONLY_NOT_GRANTED",
                "EXPLICIT_HUMAN_RTM_DRIFT_REJECTION_APPROVAL_REQUIRED_NOT_GRANTED",
                "RTM-DRIFT-REJECTION-AUTHORITY-REQUEST-091-001",
                "python/rtm_drift_rejection_authority_request.py",
                "DRIFT_REJECTION_REQUESTED_FOR_REVIEW_NOT_GRANTED",
                "NO_DRIFT_REJECTION_OR_DRIFT_DECISION_PERFORMED",
            ],
        }
        missing = []
        for path, markers in checks.items():
            self.assertTrue(path.exists(), f"{path.name} missing")
            body = path.read_text()
            for marker in markers:
                if marker not in body:
                    missing.append(f"{path.name} missing {marker}")
        self.assertEqual(missing, [])

    def test_sprint091_completion_updates_current_state_after_rtm_sequence(self):
        roadmap_text = BLK077.read_text()
        index_text = BLK079.read_text()
        required = [
            "Post-BLK-SYSTEM-091 boundary update",
            "BLK-SYSTEM-089 captured the exact RTM generation approval decision",
            "RTM_GENERATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK088_REQUEST_NOT_GENERATED",
            "BLK-SYSTEM-090 executed the exact local RTM generation pilot",
            "LOCAL_RTM_GENERATION_PILOT_EXECUTED_FOR_EXACT_BLK089_APPROVAL",
            "BLK-SYSTEM-091 packaged a review-only RTM drift-rejection authority request",
            "RTM_DRIFT_REJECTION_AUTHORITY_REQUEST_READY_AFTER_LOCAL_RTM_GENERATION_NOT_GRANTED",
            "historical as-of-BLK-091 marker `EXPLICIT_HUMAN_RTM_DRIFT_REJECTION_APPROVAL_REQUIRED_NOT_GRANTED`",
            "BLK-SYSTEM-093 later captured exact approval",
        ]
        missing = []
        for source, body in [("BLK-077", roadmap_text), ("BLK-079", index_text)]:
            for marker in required:
                if marker not in body:
                    missing.append(f"{source} missing {marker}")
        self.assertEqual(missing, [])

    def test_sprint092_post091_reconciliation_preserves_no_approval_capture(self):
        checks = {
            BLK092: [
                "BLK-092 — Post-091 Roadmap / Current-State Reconciliation",
                "BLK_SYSTEM_092_POST_091_ROADMAP_CURRENT_STATE_RECONCILED",
                "POST_091_RECONCILIATION_ONLY_NO_APPROVAL_CAPTURE",
                "NEXT_EXACT_FRONTIER_AFTER_092_REQUIRES_SEPARATE_AUTHORITY_DECISION",
                "BLK_SYSTEM_092_GRANTS_NO_DRIFT_REVIEW_APPROVAL_OR_EXECUTION",
                "BLK_SYSTEM_092_GRANTS_NO_RTM_DRIFT_REJECTION_APPROVAL_OR_EXECUTION",
                "RTM-DRIFT-REJECTION-AUTHORITY-REQUEST-091-001",
                "EXPLICIT_HUMAN_RTM_DRIFT_REJECTION_APPROVAL_REQUIRED_NOT_GRANTED",
                "does not capture drift-review approval",
                "does not capture RTM drift-rejection approval",
                "does not execute drift review",
                "does not execute RTM drift rejection",
            ],
            BLK077: [
                "Post-BLK-SYSTEM-092 reconciliation update",
                "BLK_SYSTEM_092_POST_091_ROADMAP_CURRENT_STATE_RECONCILED",
                "BLK-SYSTEM-093 — RTM Drift-Rejection Approval Decision Capture",
            ],
            BLK079: [
                "Post-BLK-SYSTEM-092 reconciliation update",
                "BLK_SYSTEM_092_POST_091_ROADMAP_CURRENT_STATE_RECONCILED",
                "BLK-SYSTEM-093 — RTM Drift-Rejection Approval Decision Capture",
            ],
        }
        missing = []
        for path, markers in checks.items():
            self.assertTrue(path.exists(), f"{path.name} missing")
            body = path.read_text()
            for marker in markers:
                if marker not in body:
                    missing.append(f"{path.name} missing {marker}")
        self.assertEqual(missing, [])

    def test_sprint093_rtm_drift_rejection_approval_capture_preserves_no_execution(self):
        checks = {
            BLK093: [
                "BLK-093 — RTM Drift-Rejection Approval Decision Capture",
                "Active RTM drift-rejection approval-decision boundary — exact approval capture only; not drift-rejection execution and not a drift decision",
                "RTM_DRIFT_REJECTION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK091_REQUEST_NOT_EXECUTED",
                "APPROVED_FOR_ONE_FUTURE_LOCAL_RTM_DRIFT_REJECTION_EXECUTION_NOT_EXECUTED",
                "EXACT_LOCAL_RTM_DRIFT_REJECTION_EXECUTION_REQUIRED_NOT_RUN",
                "BLK_SYSTEM_093_GRANTS_NO_RTM_DRIFT_REJECTION_EXECUTION",
                "RTM-DRIFT-REJECTION-APPROVAL-DECISION-093-001",
                "APPROVAL-BLK-SYSTEM-091-RTM-DRIFT-REJECTION-001",
                "RUN-BLK-SYSTEM-091-RTM-DRIFT-REJECTION-001",
                "python/rtm_drift_rejection_approval_decision.py",
                "DRIFT_REJECTION_NOT_EXECUTED_BY_APPROVAL_DECISION",
                "DRIFT_DECISION_NOT_MADE_BY_APPROVAL_DECISION",
            ],
            BLK077: [
                "Post-BLK-SYSTEM-093 boundary update",
                "RTM_DRIFT_REJECTION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK091_REQUEST_NOT_EXECUTED",
                "Historical pre-BLK-SYSTEM-095 marker `EXACT_LOCAL_RTM_DRIFT_REJECTION_EXECUTION_REQUIRED_NOT_RUN`",
            ],
            BLK079: [
                "Post-BLK-SYSTEM-093 boundary update",
                "RTM_DRIFT_REJECTION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK091_REQUEST_NOT_EXECUTED",
                "Historical pre-BLK-SYSTEM-095 marker `EXACT_LOCAL_RTM_DRIFT_REJECTION_EXECUTION_REQUIRED_NOT_RUN`",
            ],
        }
        missing = []
        for path, markers in checks.items():
            self.assertTrue(path.exists(), f"{path.name} missing")
            body = path.read_text()
            for marker in markers:
                if marker not in body:
                    missing.append(f"{path.name} missing {marker}")
        self.assertEqual(missing, [])

    def test_sprint094_post093_cleanup_aligns_local_pilot_ladder_before_execution(self):
        checks = {
            BLK094: [
                "BLK-094 — Post-093 Roadmap / RTM-Ladder Alignment",
                "BLK_SYSTEM_094_POST_093_RTM_LADDER_ALIGNED",
                "LOCAL_NON_AUTHORITATIVE_RTM_PILOT_LADDER_NOT_RUNTIME_BLK_LINK_CLOSURE",
                "ACTUAL_AUTHORITATIVE_BEO_PUBLICATION_REMAINS_PREREQUISITE_FOR_RUNTIME_BLK_LINK",
                "BLK_SYSTEM_093_APPROVAL_CAPTURE_IS_NOT_EXECUTION_SELECTION",
                "FUTURE_AUTHORITY_RUNGS_MUST_BE_INDEPENDENTLY_AUDITABLE",
                "NO_RTM_DRIFT_REJECTION_EXECUTION_BY_BLK_SYSTEM_094",
                "no protected-body reads or hashing",
                "no active-vault comparison",
                "no external ledger mutation",
            ],
            BLK077: [
                "BLK-SYSTEM-094 — Post-093 Roadmap / RTM-Ladder Alignment",
                "LOCAL_NON_AUTHORITATIVE_RTM_PILOT_LADDER_NOT_RUNTIME_BLK_LINK_CLOSURE",
                "runtime `blk-link` trace closure still requires actual authoritative BEO publication prerequisites",
                "BLK-SYSTEM-093 approval-decision capture is not execution selection",
                "Future authority rungs should be independently auditable",
                "BLK-094 remains alignment-only evidence; BLK-SYSTEM-095 later consumed the exact local run ID",
                "BLK-094 remains alignment-only evidence",
            ],
            BLK079: [
                "BLK-SYSTEM-094 — Post-093 Roadmap / RTM-Ladder Alignment",
                "LOCAL_NON_AUTHORITATIVE_RTM_PILOT_LADDER_NOT_RUNTIME_BLK_LINK_CLOSURE",
                "BLK-SYSTEM-095 later consumed the exact local run ID",
                "No additional RTM drift-rejection approval is granted by this index",
                "BLK-094 post-093 roadmap / RTM-ladder alignment",
            ],
        }
        missing = []
        for path, markers in checks.items():
            self.assertTrue(path.exists(), f"{path.name} missing")
            body = path.read_text()
            for marker in markers:
                if marker not in body:
                    missing.append(f"{path.name} missing {marker}")
        self.assertEqual(missing, [])

    def test_sprint094_removes_current_state_stale_post093_contradictions(self):
        roadmap_text = BLK077.read_text()
        index_text = BLK079.read_text()
        forbidden_current_phrases = [
            "These are remaining gaps after BLK-SYSTEM-092:",
            "or RTM drift-rejection approval/execution has occurred",
            "next, any RTM drift-rejection approval movement requires a separate exact human decision for the BLK-SYSTEM-091 request package",
            "no RTM drift-rejection approval/execution",
        ]
        offenders = []
        for source, body in [("BLK-077", roadmap_text), ("BLK-079", index_text)]:
            for phrase in forbidden_current_phrases:
                if phrase in body:
                    offenders.append(f"{source} still contains stale current-state phrase: {phrase}")
        self.assertEqual(offenders, [])

    def test_sprint094_cleans_stale_087_closeout_pending_language(self):
        text = SPRINT087_CLOSEOUT.read_text()
        forbidden = [
            "Final local state before closeout commit: pending final status check",
            "Final commit and push pending at author time",
        ]
        offenders = [phrase for phrase in forbidden if phrase in text]
        self.assertEqual(offenders, [])
        required = [
            "Final local state before closeout commit: BLK-SYSTEM-087 closeout later reconciled by BLK-SYSTEM-094; completion is historical, not a moving present-tense repository-state claim",
            "Final commit and push completion was reconciled by BLK-SYSTEM-094; this line does not assert current working-tree cleanliness",
        ]
        missing = [phrase for phrase in required if phrase not in text]
        self.assertEqual(missing, [])

    def test_sprint095_exact_local_rtm_drift_rejection_execution_is_local_only(self):
        checks = {
            BLK095: [
                "BLK-095 — Exact Local RTM Drift-Rejection Execution",
                "LOCAL_RTM_DRIFT_REJECTION_EXECUTED_FOR_EXACT_BLK093_APPROVAL",
                "RTM-DRIFT-REJECTION-EXECUTION-095-001",
                "RUN-BLK-SYSTEM-091-RTM-DRIFT-REJECTION-001",
                "PILOT_LOCAL_RTM_DRIFT_REJECTION_RECORDED_NOT_AUTHORITATIVE",
                "AUTHORITATIVE_DRIFT_DECISION_NOT_MADE",
                "NO_RUNTIME_BLK_LINK_TRACE_CLOSURE_BY_BLK_SYSTEM_095",
                "POST_LOCAL_RTM_DRIFT_REJECTION_RECONCILIATION_REQUIRED_NOT_RUNTIME_BLK_LINK",
                "no protected-body reads or hashing",
                "no active-vault hash comparison",
                "no external ledger mutation",
                "no target-repo scan or mutation",
                "no source/Git mutation by fixture",
                "no BEB dispatch",
                "no BEO closeout execution",
                "no BLK-pipe/BLK-test/Codex runtime",
                "no package/network/model/browser/cyber tooling",
                "no production isolation claim",
            ],
            BLK077: [
                "BLK-SYSTEM-095",
                "PILOT_LOCAL_RTM_DRIFT_REJECTION_RECORDED_NOT_AUTHORITATIVE",
                "local RTM drift-rejection execution remains non-authoritative",
                "runtime `blk-link` trace closure still requires actual authoritative BEO publication prerequisites",
                "no target/source/Git mutation by fixtures",
                "no BLK-pipe/BLK-test/Codex runtime",
                "no package/network/model/browser/cyber tooling",
            ],
            BLK079: [
                "BLK-095 exact local RTM drift-rejection execution",
                "RTM-DRIFT-REJECTION-EXECUTION-095-001",
                "PILOT_LOCAL_RTM_DRIFT_REJECTION_RECORDED_NOT_AUTHORITATIVE",
                "No reusable/runtime RTM drift-rejection grant",
                "no target/source/Git mutation",
                "no BEB/BEO execution",
                "no runtime/tooling",
            ],
        }
        missing = []
        for path, markers in checks.items():
            self.assertTrue(path.exists(), f"{path.name} missing")
            body = path.read_text()
            for marker in markers:
                if marker not in body:
                    missing.append(f"{path.name} missing {marker}")
        self.assertEqual(missing, [])

    def test_sprint095_active_docs_do_not_keep_unqualified_pre095_execution_pending_wording(self):
        forbidden = [
            "BLK-093 remains approval-decision package evidence with execution unrun",
            "approval-decision package exists; execution remains unrun",
            "one exact local RTM drift-rejection execution sprint remains only a candidate frontier if separately selected",
            "Current candidate frontiers after BLK-SYSTEM-094 are: one exact local RTM drift-rejection execution sprint if separately selected",
            "next marker `EXACT_LOCAL_RTM_DRIFT_REJECTION_EXECUTION_REQUIRED_NOT_RUN`",
            "but no RTM drift-rejection execution has occurred",
            "next marker `EXPLICIT_HUMAN_RTM_DRIFT_REJECTION_APPROVAL_REQUIRED_NOT_GRANTED`",
        ]
        offenders = []
        for label, path in [("BLK-077", BLK077), ("BLK-079", BLK079)]:
            body = path.read_text()
            for phrase in forbidden:
                if phrase in body:
                    offenders.append(f"{label} still contains stale post-095 wording: {phrase}")
        self.assertEqual(offenders, [])

    def test_sprint096_post095_reconciliation_closes_local_ladder_without_runtime_authority(self):
        checks = {
            BLK096: [
                "BLK-096 — Post-095 Local RTM Ladder Reconciliation",
                "BLK_SYSTEM_096_POST_095_LOCAL_RTM_LADDER_RECONCILED",
                "LOCAL_RTM_DRIFT_REJECTION_EVIDENCE_CONSUMED_NOT_AUTHORITY",
                "POST_LOCAL_RTM_RECONCILIATION_COMPLETE_NOT_RUNTIME_BLK_LINK",
                "NEXT_FRONTIER_REQUIRES_EXPLICIT_OPERATOR_DECISION_AFTER_LOCAL_LADDER",
                "NO_RUNTIME_BLK_LINK_TRACE_CLOSURE_BY_BLK_SYSTEM_096",
                "NO_AUTHORITATIVE_DRIFT_DECISION_BY_BLK_SYSTEM_096",
                "NO_ACTIVE_VAULT_HASH_COMPARISON_BY_BLK_SYSTEM_096",
                "no protected-body reads or hashing",
                "no external authoritative BEO publication",
                "no runtime `PUBLISHED` BEO output",
                "no runtime RTM generation",
                "no signer/storage/ledger/rollback",
                "no target/source/Git mutation",
                "no BLK-pipe/BLK-test/Codex runtime",
                "no package/network/model/browser/cyber tooling",
            ],
            BLK077: [
                "Post-BLK-SYSTEM-096 boundary update",
                "Historical roadmap status snapshot — 2026-05-13 lineage through BLK-SYSTEM-100 (superseded by post-103 reconciliation)",
                "BLK_SYSTEM_096_POST_095_LOCAL_RTM_LADDER_RECONCILED",
                "BLK-SYSTEM-096 reconciled the post-local RTM ladder state",
                "current candidate frontiers after BLK-SYSTEM-096",
                "Historical BLK-SYSTEM-096/098 markers are retained only as lineage for regression gates",
                "Current state is advanced through BLK-SYSTEM-103 and reconciled by BLK-SYSTEM-104",
                "one bounded BLK-test evidence refresh",
                "one Codex L3 smoke",
                "one separately approved authoritative BEO/RTM runtime frontier only after actual authoritative publication prerequisites are satisfied",
                "no external authoritative publication",
                "no runtime RTM generation",
                "no signer/storage/rollback side effect",
                "no runtime `blk-link` trace closure",
            ],
            BLK079: [
                "Post-BLK-SYSTEM-096 current-state update",
                "BLK-096 post-095 local RTM ladder reconciliation",
                "BLK_SYSTEM_096_POST_095_LOCAL_RTM_LADDER_RECONCILED",
                "LOCAL_RTM_DRIFT_REJECTION_EVIDENCE_CONSUMED_NOT_AUTHORITY",
                "NEXT_FRONTIER_REQUIRES_EXPLICIT_OPERATOR_DECISION_AFTER_LOCAL_LADDER",
                "No runtime `blk-link` trace closure",
                "no external authoritative publication",
                "no runtime RTM generation",
                "no signer/storage/rollback",
                "no runtime/tooling",
            ],
        }
        missing = []
        for path, markers in checks.items():
            self.assertTrue(path.exists(), f"{path.name} missing")
            body = path.read_text()
            for marker in markers:
                if marker not in body:
                    missing.append(f"{path.name} missing {marker}")
        self.assertEqual(missing, [])

    def test_sprint096_active_docs_do_not_leave_post095_reconciliation_required_as_current_state(self):
        forbidden_current = [
            "POST_LOCAL_RTM_DRIFT_REJECTION_RECONCILIATION_REQUIRED_NOT_RUNTIME_BLK_LINK",
            "Current candidate frontiers after BLK-SYSTEM-095 are:",
            "Current candidate frontiers after BLK-SYSTEM-095 are: one bounded post-local-execution reconciliation/current-state cleanup sprint",
            "Current roadmap status snapshot — 2026-05-13 after BLK-SYSTEM-095",
            "These are remaining gaps after BLK-SYSTEM-095",
            "After BLK-SYSTEM-095, any next architecture-development movement",
        ]
        offenders = []
        for label, path in [("BLK-077", BLK077), ("BLK-079", BLK079)]:
            body = path.read_text()
            for phrase in forbidden_current:
                if phrase in body:
                    offenders.append(f"{label} still carries unclosed post-095 reconciliation state: {phrase}")
        self.assertEqual(offenders, [])

    def test_sprint097_bounded_blk_test_evidence_refresh_is_one_run_evidence_only(self):
        import json

        checks = {
            BLK097: [
                "BLK-097 — Bounded BLK-test Evidence Refresh Request / Exact-Target Frontier",
                "Completed consumed one-run BLK-test evidence-refresh boundary — exact-target evidence only; no production BLK-test MCP",
                "BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_BOUNDARY",
                "BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_PASS_EVIDENCE_ONLY",
                "BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_FAIL_EVIDENCE_ONLY",
                "BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_BLOCKED_EVIDENCE_ONLY",
                "BLK-test is a BLK-System functional module, not BLK-System's test suite",
                "APPROVAL-BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-001",
                "RUN-BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-001",
                "/home/dad/code/Kuronode-v1",
                "/home/dad/code/Kuronode-v1/scripts",
                "/tmp/blk-system-097-kuronode-evidence-refresh-workspace",
                "/tmp/blk-system-097-kuronode-evidence-refresh-replay-ledger.json",
                "aebea51bed911c781a537d84d38b2dcb838b1368",
                "USER_REQUESTED_EXECUTE_ALL_TASKS_FOR_BLK_SYSTEM_097",
                "KURONODE_ORIGIN_MAIN_HEAD_RECHECKED",
                "READ_ONLY_RUN_AST_VALIDATION_ONLY",
                "REPLAY_CONSUMED_BEFORE_RUNTIME",
                "NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST",
                "NO_PROTECTED_BODY_READ",
                "NO_BEO_RTM_COVERAGE_DRIFT_AUTHORITY",
                "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_097_KURONODE_BOUNDED_EVIDENCE_REFRESH",
                "No production BLK-test MCP authority",
                "No generic BLK-test MCP authority",
                "No reusable BLK-test service startup",
                "No arbitrary shell or caller-supplied commands",
                "No dynamic tool expansion",
                "No Electron launch, no Playwright launch, no smoke-test execution, no TypeScript compiler, no linter, no formatter, no package-manager invocation",
                "No network/model/browser/cyber tooling",
                "No BLK-pipe execution",
                "No Codex execution",
                "No Kuronode source mutation",
                "No Kuronode Git mutation, staging, commit, push, reset, checkout, revert, stash, cleanup, autofix, or remote writes by BLK-test",
                "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
                "No authoritative BEO publication",
                "No runtime PUBLISHED BEO output",
                "No RTM generation or RTM drift rejection",
                "No coverage matrix, coverage claim, active-vault hash comparison, or drift decision",
                "No public ledger mutation",
                "No signer, storage, rollback, revocation, supersession, or release authority",
                "No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation proof",
                "Replay IDs are consumed before runtime and cannot be reused even if the refresh BLOCKS",
            ],
            BLK077: [
                "Post-BLK-SYSTEM-097 boundary update",
                "BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_PASS_EVIDENCE_ONLY",
                "BLK-SYSTEM-097 executed exactly one bounded BLK-test evidence refresh",
                "no production BLK-test MCP",
                "no source/Git mutation",
                "no BEO publication",
                "no RTM generation",
                "no coverage truth",
                "no protected-body reads",
            ],
            BLK079: [
                "Post-BLK-SYSTEM-097 current-state update",
                "BLK-097 bounded BLK-test evidence refresh",
                "BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_PASS_EVIDENCE_ONLY",
                "one exact evidence-only BLK-test refresh",
                "no production BLK-test MCP",
                "no source/Git mutation",
                "no BEO publication",
                "no RTM generation",
                "no runtime/tooling",
            ],
        }
        missing = []
        for path, markers in checks.items():
            self.assertTrue(path.exists(), f"{path.name} missing")
            body = path.read_text()
            for marker in markers:
                if marker not in body:
                    missing.append(f"{path.name} missing {marker}")
        self.assertEqual(missing, [])

        self.assertTrue(SPRINT097_EVIDENCE.exists(), "BLK-SYSTEM-097 runtime evidence missing")
        evidence = json.loads(SPRINT097_EVIDENCE.read_text())
        self.assertEqual(evidence["sprint"], "BLK-SYSTEM-097")
        self.assertEqual(evidence["approval_id"], "APPROVAL-BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-001")
        self.assertEqual(evidence["run_id"], "RUN-BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-001")
        self.assertEqual(evidence["target_repo_path"], "/home/dad/code/Kuronode-v1")
        self.assertEqual(evidence["source_subtree_path"], "/home/dad/code/Kuronode-v1/scripts")
        self.assertEqual(evidence["expected_head"], "aebea51bed911c781a537d84d38b2dcb838b1368")
        self.assertEqual(evidence["observed_remote_head"], "aebea51bed911c781a537d84d38b2dcb838b1368")
        self.assertIn(evidence["status"], {"PASS", "FAIL", "BLOCKED"})
        self.assertTrue(evidence["replay_consumed_before_runtime"])
        self.assertFalse(evidence["source_mutation_detected"])
        self.assertFalse(evidence["git_mutation_detected"])
        self.assertTrue(evidence["workspace_cleanup_verified"])
        self.assertEqual(evidence["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(evidence["rtm_status"], "NOT_GENERATED")
        self.assertFalse(evidence["coverage_claim_promoted"])
        self.assertFalse(evidence["protected_body_read"])

        forbidden_claims = [
            r"BLK-test validates BLK-System",
            r"BLK-System test suite",
            r"production BLK-test MCP is authorized",
            r"generic BLK-test MCP is authorized",
            r"source writes enabled",
            r"git staging enabled",
            r"BEO is PUBLISHED",
            r"RTM generated",
            r"coverage truth established",
            r"drift decision made",
            r"production sandbox is proven",
            r"read \.env secrets",
            r"APPROVED_FOR_LIVE_EXECUTION",
        ]
        body = BLK097.read_text()
        offenders = [pattern for pattern in forbidden_claims if re.search(pattern, body, re.IGNORECASE)]
        self.assertEqual(offenders, [], f"BLK-097 contains forbidden authority claims: {offenders}")

    def test_sprint097_active_docs_do_not_leave_unqualified_post096_evidence_refresh_as_current_frontier(self):
        offenders = []
        stale_phrases = [
            "BLK-SYSTEM-096 reconciled the post-local RTM ladder state. The current candidate frontiers after BLK-SYSTEM-096 are:",
            "BLK-SYSTEM-096 reconciled the post-local RTM ladder state. The current candidate frontiers after BLK-SYSTEM-096 are: one bounded BLK-test evidence refresh",
            "Active one-run BLK-test evidence-refresh boundary",
        ]
        for label, path in [("BLK-077", BLK077), ("BLK-079", BLK079), ("BLK-097", BLK097)]:
            body = path.read_text()
            for phrase in stale_phrases:
                if phrase in body:
                    offenders.append(f"{label} still contains stale BLK-SYSTEM-097 frontier wording: {phrase}")
        self.assertEqual(offenders, [])

    def test_sprint098_beo_publication_prerequisite_request_after_evidence_refresh_is_review_only(self):
        checks = {
            BLK098: [
                "BLK-098 — BEO Publication Prerequisite Request After Evidence Refresh",
                "BEO_PUBLICATION_PREREQUISITE_REQUEST_AFTER_EVIDENCE_REFRESH_BOUNDARY",
                "BEO_PUBLICATION_PREREQUISITE_REQUEST_READY_AFTER_BLK_TEST_REFRESH_NOT_GRANTED",
                "BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001",
                "EXPLICIT_HUMAN_EXTERNAL_BEO_PUBLICATION_APPROVAL_REQUIRED_NOT_GRANTED",
                "sha256:ebf3121a3a62dabaea589dc796ad645ef56d71d59574326bf278fbf563b66580",
                "sha256:78df1c4420bebd3da4e568bff8dd9f424f093e2548248b2825f2781ab8f31a7e",
                "sha256:6ee76d749bdb809bb39ae2f6f26c22c302370f9bf30da54acfc208a6661e875a",
                "future external BEO publication decision only",
                "No external authoritative BEO publication",
                "No runtime PUBLISHED BEO output",
                "No live publication approval capture",
                "No signer key-material access or cryptographic signing",
                "No immutable storage writes or public ledger mutation",
                "No rollback, revocation, or supersession execution",
                "No runtime RTM generation or RTM drift rejection",
                "No authoritative drift decision, active-vault hash comparison, coverage truth, or coverage-claim promotion",
                "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
                "No target-repo scan or mutation",
                "No source/Git mutation by fixtures",
                "No BLK-pipe, BLK-test runtime, Codex, package/network/model/browser/cyber tooling, or production-isolation authority",
                "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_098_BEO_PUBLICATION_PREREQUISITE_REQUEST",
            ],
            BLK077: [
                "Post-BLK-SYSTEM-098 boundary update",
                "BEO_PUBLICATION_PREREQUISITE_REQUEST_READY_AFTER_BLK_TEST_REFRESH_NOT_GRANTED",
                "BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001",
                "future external BEO publication decision only",
                "no external BEO publication",
                "no runtime RTM generation",
                "no signer/storage/ledger/rollback",
                "no protected-body reads",
            ],
            BLK079: [
                "Post-BLK-SYSTEM-098 current-state update",
                "BLK-098 BEO publication prerequisite request after evidence refresh",
                "BEO_PUBLICATION_PREREQUISITE_REQUEST_READY_AFTER_BLK_TEST_REFRESH_NOT_GRANTED",
                "BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001",
                "future external BEO publication decision only",
                "no external BEO publication",
                "no runtime RTM generation",
                "no protected-body reads",
            ],
        }
        missing = []
        for path, markers in checks.items():
            self.assertTrue(path.exists(), f"{path.name} missing")
            body = path.read_text()
            for marker in markers:
                if marker not in body:
                    missing.append(f"{path.name} missing {marker}")
        self.assertEqual(missing, [])

    def test_sprint098_active_docs_do_not_leave_unqualified_post097_frontier_wording(self):
        offenders = []
        stale_phrases = [
            "After BLK-SYSTEM-097, future movement still requires a separately scoped operator decision",
            "current state records the local BEO/RTM ladder as reconciled local evidence only and BLK-SYSTEM-097 as one exact evidence-only BLK-test refresh",
            "These are remaining gaps after BLK-SYSTEM-096, with BLK-SYSTEM-097 now additionally recording one completed bounded BLK-test evidence refresh",
        ]
        for label, path in [("BLK-077", BLK077), ("BLK-079", BLK079)]:
            body = path.read_text()
            for phrase in stale_phrases:
                if phrase in body:
                    offenders.append(f"{label} still carries unclosed post-097 frontier state: {phrase}")
        self.assertEqual(offenders, [])

    def test_sprint099_external_beo_publication_approval_decision_capture_is_not_publication_execution(self):
        checks = {
            BLK099: [
                "BLK-099 — External BEO Publication Approval Decision Capture",
                "EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION_CAPTURE_BOUNDARY",
                "EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK098_REQUEST_NOT_PUBLISHED",
                "BEO-PUBLICATION-APPROVAL-DECISION-099-001",
                "BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001",
                "sha256:a782b223c88ae155a37519b87313dd2085450515c78ba60e93277c636ba6e041",
                "APPROVAL-BLK-SYSTEM-099-EXTERNAL-BEO-PUBLICATION-001",
                "RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001",
                "one future separately scoped external BEO publication execution sprint",
                "Future publication execution run ID is reserved but not consumed",
                "No external authoritative BEO publication execution",
                "No runtime PUBLISHED BEO output",
                "No signer key-material access or cryptographic signing",
                "No immutable storage writes or public ledger mutation",
                "No rollback, revocation, or supersession execution",
                "No runtime RTM generation or RTM drift rejection",
                "No authoritative drift decision, active-vault hash comparison, coverage truth, or coverage-claim promotion",
                "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
                "No target-repo scan or mutation",
                "No source/Git mutation by fixtures",
                "No BLK-pipe, BLK-test runtime, Codex, package/network/model/browser/cyber tooling, or production-isolation authority",
                "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_099_EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION",
            ],
            BLK077: [
                "Post-BLK-SYSTEM-099 boundary update",
                "EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK098_REQUEST_NOT_PUBLISHED",
                "BEO-PUBLICATION-APPROVAL-DECISION-099-001",
                "one future separately scoped external BEO publication execution sprint",
                "external publication not executed",
                "run ID reserved but not consumed",
                "no signer/storage/ledger/rollback",
                "no runtime RTM generation",
                "no protected-body reads",
            ],
            BLK079: [
                "Post-BLK-SYSTEM-099 current-state update",
                "BLK-099 external BEO publication approval decision capture",
                "EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK098_REQUEST_NOT_PUBLISHED",
                "BEO-PUBLICATION-APPROVAL-DECISION-099-001",
                "one future separately scoped external BEO publication execution sprint",
                "external publication not executed",
                "run ID reserved but not consumed",
                "no signer/storage/ledger/rollback",
                "no runtime RTM generation",
                "no protected-body reads",
            ],
        }
        missing = []
        for path, markers in checks.items():
            self.assertTrue(path.exists(), f"{path.name} missing")
            body = path.read_text()
            for marker in markers:
                if marker not in body:
                    missing.append(f"{path.name} missing {marker}")
        self.assertEqual(missing, [])

    def test_sprint099_active_docs_do_not_leave_unqualified_post098_frontier_wording(self):
        offenders = []
        stale_phrases = [
            "After BLK-SYSTEM-098, future movement still requires a separately scoped operator decision",
            "BLK-SYSTEM-098 is review-only prerequisite evidence for future external BEO publication decision only",
            "EXPLICIT_HUMAN_EXTERNAL_BEO_PUBLICATION_APPROVAL_REQUIRED_NOT_GRANTED",
        ]
        for label, path in [("BLK-077", BLK077), ("BLK-079", BLK079)]:
            body = path.read_text()
            for phrase in stale_phrases:
                if phrase in body:
                    offenders.append(f"{label} still carries unclosed post-098 frontier state: {phrase}")
        self.assertEqual(offenders, [])

    def test_sprint100_external_beo_publication_execution_boundary_and_adjacent_denials(self):
        checks = {
            BLK100: [
                "BLK-100 — External BEO Publication Execution",
                "EXTERNAL_BEO_PUBLICATION_EXECUTION_BOUNDARY",
                "EXTERNAL_BEO_PUBLICATION_EXECUTED_FOR_EXACT_BLK099_APPROVAL_RECORD_ONLY",
                "BEO-PUBLICATION-EXECUTION-100-001",
                "BEO-PUBLICATION-APPROVAL-DECISION-099-001",
                "RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001",
                "PUBLISHED_EXTERNAL_BEO_RECORD",
                "sha256:5269146b6b46e27e38878a327b1ac6180068d5c9e427067604b611512a72289d",
                "sha256:1efbfd9b6b9d828b7b793c1c9c2b0f8115c36db69ef850e5a2f2ff94195923b4",
                "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_100_EXTERNAL_BEO_PUBLICATION_EXECUTION",
                "No reuse of `RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001`",
                "No signer key-material access or cryptographic signing",
                "No immutable storage writes or public ledger mutation",
                "No rollback, revocation, or supersession execution",
                "No runtime RTM generation or RTM drift rejection",
                "No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison",
                "No target-repo scan or mutation",
                "No source/Git mutation by fixtures",
                "No BLK-pipe, BLK-test runtime, Codex, package/network/model/browser/cyber tooling, or production-isolation authority",
            ],
            BLK077: [
                "Post-BLK-SYSTEM-100 boundary update",
                "EXTERNAL_BEO_PUBLICATION_EXECUTED_FOR_EXACT_BLK099_APPROVAL_RECORD_ONLY",
                "BEO-PUBLICATION-EXECUTION-100-001",
                "PUBLISHED_EXTERNAL_BEO_RECORD",
                "run ID consumed once",
                "no signer/storage/ledger/rollback",
                "no runtime RTM generation",
                "no protected-body reads",
                "no target/source/Git mutation",
            ],
            BLK079: [
                "Post-BLK-SYSTEM-100 current-state update",
                "BLK-100 external BEO publication execution",
                "EXTERNAL_BEO_PUBLICATION_EXECUTED_FOR_EXACT_BLK099_APPROVAL_RECORD_ONLY",
                "BEO-PUBLICATION-EXECUTION-100-001",
                "PUBLISHED_EXTERNAL_BEO_RECORD",
                "run ID consumed once",
                "no signer/storage/ledger/rollback",
                "no runtime RTM generation",
                "no protected-body reads",
                "no target/source/Git mutation",
            ],
        }
        missing = []
        for path, markers in checks.items():
            self.assertTrue(path.exists(), f"{path.name} missing")
            body = path.read_text()
            for marker in markers:
                if marker not in body:
                    missing.append(f"{path.name} missing {marker}")
        self.assertEqual(missing, [])

    def test_sprint101_102_103_rtm_trace_closure_ladder_boundaries_and_denials(self):
        checks = {
            BLK101: [
                "BLK-101 — RTM Trace-Closure Authority Request After External BEO Publication",
                "RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_AFTER_EXTERNAL_BEO_BOUNDARY",
                "RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_READY_AFTER_EXTERNAL_BEO_PUBLICATION_NOT_GRANTED",
                "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-101-001",
                "sha256:b050261c1c1938423795f56427571d49dcf1d028c5811b5e3985b644cfadbcde",
                "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_101_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST",
                "no approval",
                "no execution",
                "no RTM generation",
                "no active-vault hash comparison",
                "no protected-body reads",
            ],
            BLK102: [
                "BLK-102 — RTM Trace-Closure Approval Decision Capture",
                "RTM_TRACE_CLOSURE_APPROVAL_DECISION_BOUNDARY",
                "RTM_TRACE_CLOSURE_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK101_REQUEST_NOT_EXECUTED",
                "RTM-TRACE-CLOSURE-APPROVAL-DECISION-102-001",
                "RUN-BLK-SYSTEM-103-RTM-TRACE-CLOSURE-001",
                "sha256:9211e14961b8c0f380812372d2b2a1ae091daf17709af375985f94015af0fecb",
                "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_102_RTM_TRACE_CLOSURE_APPROVAL_DECISION",
                "does not execute trace closure",
                "generate RTM",
                "read protected bodies",
            ],
            BLK103: [
                "BLK-103 — Exact Local RTM Trace-Closure Execution",
                "EXACT_LOCAL_RTM_TRACE_CLOSURE_EXECUTION_BOUNDARY",
                "LOCAL_RTM_TRACE_CLOSURE_EXECUTED_FOR_EXACT_BLK102_APPROVAL",
                "RTM-TRACE-CLOSURE-EXECUTION-103-001",
                "PILOT_LOCAL_RTM_TRACE_CLOSURE_RECORDED_NOT_AUTHORITATIVE",
                "RUN-BLK-SYSTEM-103-RTM-TRACE-CLOSURE-001",
                "sha256:3aba65a44d221cba04a80cb8d1342026a095c699d5c58fe3daf5a34886ae820a",
                "sha256:f58d7c1d370d136c94364076339728c08c2cded30e44866fd48d7f93c0eb2d2c",
                "PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_103_EXACT_LOCAL_RTM_TRACE_CLOSURE_EXECUTION",
                "no reusable/production blk-link authority",
                "no active-vault hash comparison",
                "no protected-body reads",
            ],
            BLK077: [
                "Post-BLK-SYSTEM-101/102/103 boundary update",
                "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-101-001",
                "RTM-TRACE-CLOSURE-APPROVAL-DECISION-102-001",
                "RTM-TRACE-CLOSURE-EXECUTION-103-001",
                "PILOT_LOCAL_RTM_TRACE_CLOSURE_RECORDED_NOT_AUTHORITATIVE",
                "no reusable/production blk-link authority",
                "no protected-body reads",
            ],
            BLK079: [
                "Post-BLK-SYSTEM-101/102/103 current-state update",
                "RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_READY_AFTER_EXTERNAL_BEO_PUBLICATION_NOT_GRANTED",
                "RTM_TRACE_CLOSURE_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK101_REQUEST_NOT_EXECUTED",
                "LOCAL_RTM_TRACE_CLOSURE_EXECUTED_FOR_EXACT_BLK102_APPROVAL",
                "no reusable/production blk-link authority",
                "no protected-body reads",
            ],
        }
        missing = []
        for path, markers in checks.items():
            self.assertTrue(path.exists(), f"{path.name} missing")
            body = path.read_text()
            for marker in markers:
                if marker not in body:
                    missing.append(f"{path.name} missing {marker}")
        self.assertEqual(missing, [])

    def test_sprint104_post103_roadmap_current_state_reconciliation_boundary_and_completion_milestones(self):
        checks = {
            BLK104: [
                "BLK-104 — Post-103 Current-State Reconciliation and Frontier Selection Gate",
                "POST_103_CURRENT_STATE_RECONCILIATION_BOUNDARY",
                "BLK_SYSTEM_104_POST_103_ROADMAP_CURRENT_STATE_RECONCILED",
                "HOSTILE_REVIEW_SOURCE_BLK_SYSTEM_POST_103_ALL_CODEBASE",
                "BEO_PUBLICATION_RECORD_ONLY_SIGNER_STORAGE_LEDGER_DISABLED",
                "RTM_TRACE_CLOSURE_LOCAL_RECORD_ONLY_PRODUCTION_BLK_LINK_DISABLED",
                "NEXT_SAFE_IMPLEMENTATION_FRONTIER_GO_PROTECTED_BODY_NO_READ_REMEDIATION",
                "No BLK-pipe runtime execution",
                "No BLK-test runtime",
                "No BEO publication",
                "No RTM generation or drift rejection",
                "No protected BLK-req body reads",
            ],
            BLK077: [
                "Post-BLK-SYSTEM-103 Active Roadmap Reconciliation",
                "BLK-SYSTEM-104 — Post-103 Current-State Reconciliation and Frontier Selection Gate",
                "High-Level Roadmap to Complete BLK-System",
                "Milestone 0 — Hostile-review patch closure",
                "Milestone 1 — BLK-req legislative gateway implementation",
                "Milestone 2 — BLK-pipe production hardening",
                "Milestone 3 — Hermes planning/BEB generation and dependency routing",
                "Milestone 4 — BLK-test production functional module",
                "Milestone 5 — Authoritative BEO publication",
                "Milestone 6 — Production `blk-link` RTM trace closure",
                "Milestone 7 — Drift detection and rejection authority",
                "Milestone 8 — Integrated autonomous V-model operations",
                "Milestone 9 — Operations, security, and release governance",
                "NEXT_SAFE_IMPLEMENTATION_FRONTIER_GO_PROTECTED_BODY_NO_READ_REMEDIATION",
                "BLK-test is a BLK-System functional module, not BLK-System's test suite",
            ],
            BLK079: [
                "BLK_SYSTEM_POST_103_CURRENT_STATE_AUTHORITY_INDEX",
                "BEO_PUBLICATION_RECORD_ONLY_SIGNER_STORAGE_LEDGER_DISABLED",
                "RTM_TRACE_CLOSURE_LOCAL_RECORD_ONLY_PRODUCTION_BLK_LINK_DISABLED",
                "BLK-104 post-103 roadmap/current-state reconciliation",
                "BLK_SYSTEM_104_POST_103_ROADMAP_CURRENT_STATE_RECONCILED",
                "NEXT_SAFE_IMPLEMENTATION_FRONTIER_GO_PROTECTED_BODY_NO_READ_REMEDIATION",
                "BLK-test is a BLK-System functional module, not BLK-System's test suite",
            ],
        }
        missing = []
        for path, markers in checks.items():
            self.assertTrue(path.exists(), f"{path.name} missing")
            body = path.read_text()
            for marker in markers:
                if marker not in body:
                    missing.append(f"{path.name} missing {marker}")
        self.assertEqual(missing, [])

    def test_sprint104_active_roadmap_and_index_do_not_leave_unqualified_pre103_frontier_wording(self):
        stale_by_path = {
            BLK077: [
                "Current roadmap status snapshot — 2026-05-13 after BLK-SYSTEM-096",
                "### 3.2 Current maturity map",
                "| Area | Current maturity after BLK-SYSTEM-078 | Current authority cutline |",
                "| BEO publication path | Request and approval-envelope fixtures exist, including BLK-060 |",
                "| RTM / blk-link | Hash-only path fixtures and offline RTM fixture generation exist |",
                "These are remaining gaps after BLK-SYSTEM-098",
                "external publication and RTM remain unauthorized",
                "Current state is now advanced through BLK-SYSTEM-098",
            ],
            BLK079: [
                "BEO_PUBLICATION_DISABLED_DRAFT_AND_FIXTURE_ONLY",
                "RTM_RUNTIME_GENERATION_AND_DRIFT_REJECTION_DISABLED",
                "| BEO publication path | Draft/candidate/input/request/approval-envelope/decision-package fixtures exist |",
                "| RTM / blk-link | Hash-only path fixtures and offline local RTM fixture generation exist |",
            ],
        }
        offenders = []
        for path, stale_phrases in stale_by_path.items():
            body = path.read_text()
            for phrase in stale_phrases:
                if phrase in body:
                    offenders.append(f"{path.name} still carries stale pre/post-103 wording: {phrase}")
        self.assertEqual(offenders, [])

    def test_sprint105_root_doctrine_post103_reconciliation_markers(self):
        checks = {
            BLK105: [
                "BLK-105 — Root Doctrine Post-103 Reconciliation",
                "BLK_SYSTEM_105_ROOT_DOCTRINE_POST_103_RECONCILED",
                "POST_103_ROOT_DOCTRINE_RECONCILIATION_BOUNDARY",
                "BEO_PUBLICATION_RECORD_ONLY_SIGNER_STORAGE_LEDGER_DISABLED",
                "RTM_TRACE_CLOSURE_LOCAL_RECORD_ONLY_PRODUCTION_BLK_LINK_DISABLED",
                "NO_PROTECTED_BODY_READS_FOR_TRACE_CLOSURE",
                "No BLK-pipe runtime execution",
                "No BLK-test runtime",
                "No BEO publication by this reconciliation document",
                "No RTM generation or drift rejection",
            ],
            BLK001: [
                "Post-BLK-SYSTEM-103 root doctrine reconciliation",
                "PUBLISHED_EXTERNAL_BEO_RECORD",
                "record-only external BEO publication evidence",
                "signer/storage/ledger publication remains disabled",
                "PILOT_LOCAL_RTM_TRACE_CLOSURE_RECORDED_NOT_AUTHORITATIVE",
                "local non-authoritative trace-closure evidence",
                "production/reusable `blk-link` remains disabled",
            ],
            BLK003: [
                "Post-BLK-SYSTEM-103 orchestration boundary",
                "record-only external BEO publication evidence",
                "local non-authoritative trace-closure evidence",
                "BLK-test is a BLK-System functional module, not BLK-System's test suite",
            ],
            BLK005: [
                "Post-BLK-SYSTEM-103 BLK-req trace boundary",
                "NO_PROTECTED_BODY_READS_FOR_TRACE_CLOSURE",
                "local non-authoritative trace-closure evidence",
            ],
            BLK006: [
                "Post-BLK-SYSTEM-103 implementation boundary",
                "approved hash-only metadata",
                "NO_PROTECTED_BODY_READS_FOR_TRACE_CLOSURE",
                "production/reusable `blk-link` remains disabled",
            ],
        }
        missing = []
        for path, markers in checks.items():
            self.assertTrue(path.exists(), f"{path.name} missing")
            body = path.read_text()
            for marker in markers:
                if marker not in body:
                    missing.append(f"{path.name} missing {marker}")
        self.assertEqual(missing, [])

    def test_sprint105_root_doctrine_does_not_leave_stale_post019_as_current_state(self):
        stale_by_path = {
            BLK001: [
                "**Current BEO authority boundary after Sprint 019:**",
                "current BEO handling remains draft-only/design-only until a later publication authority is granted",
                "mechanically flags any BEO as a \"Drift Rejection\"",
            ],
            BLK003: [
                "In the current implementation boundary after Sprint 019, BLK-test returns verification evidence",
                "BEO handling is limited to a draft-only BEO fixture projection",
                "**Current implementation boundary after Sprint 019:** this escalation path",
            ],
            BLK005: [
                "target drift rejection as an unconditional current `MUST`",
            ],
            BLK006: [
                "`generate_rtm.py` compares each BEO hash against the live artifact file",
            ],
        }
        offenders = []
        for path, stale_phrases in stale_by_path.items():
            body = path.read_text()
            for phrase in stale_phrases:
                if phrase in body:
                    offenders.append(f"{path.name} still carries stale root doctrine wording: {phrase}")
        self.assertEqual(offenders, [])

    def test_sprint100_active_docs_do_not_leave_unqualified_post099_frontier_wording(self):
        offenders = []
        stale_phrases = [
            "External BEO publication execution still requires a separate future exact sprint",
            "external publication not executed and the future run ID reserved but not consumed",
            "next_required_authority: SEPARATELY_SCOPED_EXTERNAL_BEO_PUBLICATION_EXECUTION_REQUIRED_NOT_RUN",
        ]
        for label, path in [("BLK-077", BLK077), ("BLK-079", BLK079)]:
            body = path.read_text()
            for phrase in stale_phrases:
                if phrase in body:
                    offenders.append(f"{label} still carries unclosed post-099 frontier state: {phrase}")
        self.assertEqual(offenders, [])


    def test_sprint111_post103_frontier_markers_replace_stale_go_no_read_frontier(self):
        required_markers = [
            "BLK_SYSTEM_111_DOCTRINE_GATE_COVERAGE_RUNBOOK_VOCABULARY",
            "POST_103_FRONTIER_GATES_PINNED",
            "HOSTILE_REVIEW_PATCH_CLOSURE_THROUGH_BLK_SYSTEM_111",
            "NEXT_HIGH_LEVEL_BLK_SYSTEM_COMPLETION_MILESTONE_BLK_REQ_LEGISLATIVE_GATEWAY",
        ]
        for label, path in [("BLK-077", BLK077), ("BLK-079", BLK079), ("BLK-111", BLK111)]:
            self.assertTrue(path.exists(), f"{label} missing")
            body = path.read_text()
            missing = [marker for marker in required_markers if marker not in body]
            self.assertEqual(missing, [], f"{label} missing post-111 frontier markers: {missing}")

        stale_active = []
        for label, path in [("BLK-077", BLK077), ("BLK-079", BLK079)]:
            for line in path.read_text().splitlines():
                if "NEXT_SAFE_IMPLEMENTATION_FRONTIER_GO_PROTECTED_BODY_NO_READ_REMEDIATION" in line and "HISTORICAL_" not in line:
                    stale_active.append(f"{label}: {line}")
                if "The next safe implementation frontier is Go protected-body no-read remediation" in line:
                    stale_active.append(f"{label}: {line}")
                if "records `NEXT_SAFE_IMPLEMENTATION_FRONTIER_GO_PROTECTED_BODY_NO_READ_REMEDIATION` as priority guidance only" in line:
                    stale_active.append(f"{label}: {line}")
        self.assertEqual(stale_active, [], f"stale active post-103 frontier wording remains: {stale_active}")

    def test_sprint111_blk_test_functional_module_warning_is_operator_visible(self):
        warning = "BLK-test is a BLK-System functional module, not BLK-System's test suite"
        for label, path in [("BLK-077", BLK077), ("BLK-079", BLK079), ("BLK-111", BLK111)]:
            self.assertTrue(path.exists(), f"{label} missing")
            self.assertIn(warning, path.read_text(), f"{label} missing exact BLK-test module warning")

        index_rows = [line for line in BLK079.read_text().splitlines() if line.startswith("| BLK-test |")]
        self.assertEqual(len(index_rows), 1, f"expected one BLK-test row in BLK-079, got {index_rows}")
        self.assertIn(warning, index_rows[0])

    def test_sprint111_runbook_pins_post100_post103_record_only_statuses(self):
        self.assertTrue(BLK031.exists(), "BLK-031 runbook missing")
        body = BLK031.read_text()
        required = [
            "PUBLISHED_EXTERNAL_BEO_RECORD",
            "Record-only external BEO publication: signer/storage/ledger disabled",
            "PILOT_LOCAL_RTM_TRACE_CLOSURE_RECORDED_NOT_AUTHORITATIVE",
            "Local trace-closure evidence only: production blk-link disabled",
            "RUNBOOK_POST_100_103_RECORD_ONLY_STATES_PINNED",
            "does not authorize authoritative BEO publication",
            "does not authorize production blk-link",
            "does not authorize runtime RTM generation",
            "does not authorize RTM drift rejection",
        ]
        missing = [marker for marker in required if marker not in body]
        self.assertEqual(missing, [], f"BLK-031 missing post-100/post-103 runbook vocabulary: {missing}")

    def test_sprint115_production_hardening_bridge_markers_and_next_frontier_are_pinned(self):
        bridge_docs = [
            ("BLK-112", BLK112, [
                "BLK_SYSTEM_112_STRUCTURED_VALIDATION_PROFILE_ARGV_HARDENING",
                "REPOSITORY_OWNED_PROFILES_DO_NOT_EXECUTE_THROUGH_SH_C",
            ]),
            ("BLK-113", BLK113, [
                "BLK_SYSTEM_113_VALIDATION_TRUST_BOUNDARY_CAPABILITY_POLICY",
                "AUTONOMOUS_PAYLOADS_REQUIRE_REPOSITORY_OWNED_VALIDATION_PROFILES",
            ]),
            ("BLK-114", BLK114, [
                "BLK_SYSTEM_114_REPORT_EVIDENCE_HARDENING",
                "REPORT_EXPOSES_FAILURE_CLASS_DENIAL_ROUTE_AND_CLEANUP_STATUS",
            ]),
            ("BLK-115", BLK115, [
                "BLK_SYSTEM_115_PRODUCTION_HARDENING_BRIDGE_RECONCILED",
                "BLK_PIPE_PRODUCTION_HARDENING_BRIDGE_112_115_COMPLETE",
                "NEXT_FRONTIER_BLK_REQ_LEGISLATIVE_GATEWAY_PLANNING_NOT_EXECUTION_AUTHORITY",
            ]),
        ]
        for label, path, markers in bridge_docs:
            self.assertTrue(path.exists(), f"{label} missing")
            body = path.read_text()
            missing = [marker for marker in markers if marker not in body]
            self.assertEqual(missing, [], f"{label} missing BLK-115 bridge markers: {missing}")

        required_shared_markers = [
            "BLK_SYSTEM_115_PRODUCTION_HARDENING_BRIDGE_RECONCILED",
            "BLK_PIPE_PRODUCTION_HARDENING_BRIDGE_112_115_COMPLETE",
            "STRUCTURED_VALIDATION_PROFILE_ARGV_HARDENING_CLOSED",
            "VALIDATION_TRUST_BOUNDARY_CAPABILITY_POLICY_CLOSED",
            "REPORT_EVIDENCE_HARDENING_CLOSED",
            "NEXT_FRONTIER_BLK_REQ_LEGISLATIVE_GATEWAY_PLANNING_NOT_EXECUTION_AUTHORITY",
            "BLK-test is a BLK-System functional module, not BLK-System's test suite",
        ]
        for label, path in [("BLK-077", BLK077), ("BLK-079", BLK079), ("BLK-115", BLK115)]:
            self.assertTrue(path.exists(), f"{label} missing")
            body = path.read_text()
            missing = [marker for marker in required_shared_markers if marker not in body]
            self.assertEqual(missing, [], f"{label} missing production-hardening bridge markers: {missing}")

        forbidden_active = [
            "After BLK-SYSTEM-111, the active next high-level BLK-System completion milestone",
            "BLK-SYSTEM-112 remains pending",
            "BLK-SYSTEM-113 remains pending",
            "BLK-SYSTEM-114 remains pending",
            "structured validation profile argv hardening remains pending",
            "validation trust-boundary policy remains pending",
            "report/evidence hardening remains pending",
        ]
        leaks = []
        for label, path in [("BLK-077", BLK077), ("BLK-079", BLK079)]:
            body = path.read_text()
            for phrase in forbidden_active:
                if phrase in body:
                    leaks.append(f"{label}: {phrase}")
        self.assertEqual(leaks, [], f"stale active bridge wording remains: {leaks}")

    def test_sprint119_blk_req_gateway_foundation_markers_and_next_frontier_are_pinned(self):
        foundation_docs = [
            ("BLK-116", BLK116, [
                "BLK_SYSTEM_116_BLK_REQ_LEGISLATIVE_GATEWAY_CONTRACT",
                "CONTRACT_READY_NOT_EXECUTION_AUTHORITY",
            ]),
            ("BLK-117", BLK117, [
                "BLK_SYSTEM_117_VERSION_AWARE_STAGING_LINTER",
                "STRUCTURED_JSON_DIAGNOSTICS_RETURNED",
            ]),
            ("BLK-118", BLK118, [
                "BLK_SYSTEM_118_STAGING_DRAFT_WRITER",
                "DRAFT_WRITER_OUTPUTS_ONLY_TO_STAGING_DIRECTORIES",
            ]),
            ("BLK-119", BLK119, [
                "BLK_SYSTEM_119_CANONICAL_VERSION_HASH_ENGINE",
                "VERSION_HASH_SHA256_LOWERCASE_HEX",
            ]),
        ]
        for label, path, markers in foundation_docs:
            self.assertTrue(path.exists(), f"{label} missing")
            body = path.read_text()
            missing = [marker for marker in markers if marker not in body]
            self.assertEqual(missing, [], f"{label} missing BLK-req foundation markers: {missing}")

        required_shared_markers = [
            "BLK_REQ_LEGISLATIVE_GATEWAY_FOUNDATION_116_119_COMPLETE",
            "STAGING_LINTER_DRAFT_WRITER_AND_HASH_ENGINE_COMPLETE",
            "NEXT_FRONTIER_BLK_REQ_HITL_BASELINE_PROMOTION_PLANNING_NOT_EXECUTION_AUTHORITY",
            "BLK-test is a BLK-System functional module, not BLK-System's test suite",
        ]
        for label, path in [("BLK-077", BLK077), ("BLK-079", BLK079), ("BLK-119", BLK119)]:
            self.assertTrue(path.exists(), f"{label} missing")
            body = path.read_text()
            missing = [marker for marker in required_shared_markers if marker not in body]
            self.assertEqual(missing, [], f"{label} missing BLK-req foundation markers: {missing}")

        forbidden_active = [
            "BLK-SYSTEM-117 remains pending",
            "BLK-SYSTEM-118 remains pending",
            "BLK-SYSTEM-119 remains pending",
            "Current boundary after BLK-SYSTEM-115: the active next high-level BLK-System completion milestone",
            "staging linter remains pending",
            "draft writer remains pending",
            "hash engine remains pending",
        ]
        leaks = []
        for label, path in [("BLK-077", BLK077), ("BLK-079", BLK079)]:
            body = path.read_text()
            for phrase in forbidden_active:
                if phrase in body:
                    leaks.append(f"{label}: {phrase}")
        self.assertEqual(leaks, [], f"stale active BLK-req foundation wording remains: {leaks}")

    def test_sprint120_hitl_baseline_promotion_markers_and_next_frontier_are_pinned(self):
        self.assertTrue(BLK120.exists(), "BLK-120 missing")
        blk120_body = BLK120.read_text()
        blk120_markers = [
            "BLK_SYSTEM_120_HITL_BASELINE_PROMOTION",
            "DISCORD_HITL_APPROVAL_CAPTURED_FOR_NEW_BASELINES",
            "NEW_BASELINE_PROMOTION_WRITES_ACTIVE_VAULT_BY_BACKEND_ONLY",
            "BASELINE_VERSION_HASH_ASSIGNED_ON_PROMOTION",
            "ACTIVE_VAULT_WRITE_PATH_REJECTS_SYMLINKS_AND_COLLISIONS",
            "ACTIVE_VAULT_PUBLISH_IS_NO_OVERWRITE_EXCLUSIVE_CREATE",
            "APPROVAL_REPLAY_LEDGER_CONSUMES_BASELINE_APPROVAL_IDS",
            "APPROVAL_REPLAY_LEDGER_NOT_CONSUMED_ON_PUBLISH_FAILURE",
            "DISCORD_IDENTITY_VALUES_MUST_BE_SNOWFLAKE_STRINGS",
            "NO_REVISION_OVERWRITE_OR_EXACT_ID_RETRIEVAL_BY_120",
            "NEXT_FRONTIER_BLK_REQ_STAGED_REVISION_AND_EXACT_ID_RETRIEVAL_PLANNING_NOT_EXECUTION_AUTHORITY",
            "BLK-test is a BLK-System functional module, not BLK-System's test suite",
        ]
        missing = [marker for marker in blk120_markers if marker not in blk120_body]
        self.assertEqual(missing, [], f"BLK-120 missing markers: {missing}")

        shared = [
            "BLK_SYSTEM_120_HITL_BASELINE_PROMOTION_COMPLETE",
            "DISCORD_HITL_APPROVAL_CAPTURED_FOR_NEW_BASELINES",
            "NEW_BASELINE_PROMOTION_WRITES_ACTIVE_VAULT_BY_BACKEND_ONLY",
            "NEXT_FRONTIER_BLK_REQ_STAGED_REVISION_AND_EXACT_ID_RETRIEVAL_PLANNING_NOT_EXECUTION_AUTHORITY",
            "NO_REVISION_OVERWRITE_OR_EXACT_ID_RETRIEVAL_BY_120",
        ]
        for label, path in [("BLK-079", BLK079), ("BLK-120", BLK120)]:
            body = path.read_text()
            missing = [marker for marker in shared if marker not in body]
            self.assertEqual(missing, [], f"{label} missing BLK-120 shared markers: {missing}")

        roadmap_body = BLK077.read_text()
        if "BLK_SYSTEM_126_BEO_PUBLICATION_PATH_DECISION_GATE_COMPLETE" in roadmap_body:
            current_markers = [
                "BLK_SYSTEM_126_BEO_PUBLICATION_PATH_DECISION_GATE_COMPLETE",
                "BEO_PUBLICATION_PATH_DECISION_GATE_REVIEW_ONLY_BY_126",
                "NEXT_FRONTIER_METADATA_BOUND_BEO_PUBLICATION_PREREQUISITE_REQUEST_PLANNING_NOT_EXECUTION_AUTHORITY",
                "BLK_SYSTEM_125_BEB_BEO_METADATA_HANDOFF_COMPLETE",
            ]
            missing = [marker for marker in current_markers if marker not in roadmap_body]
            self.assertEqual(missing, [], f"BLK-077 missing post-126 current markers: {missing}")
        elif "BLK_SYSTEM_125_BEB_BEO_METADATA_HANDOFF_COMPLETE" in roadmap_body:
            current_markers = [
                "BLK_SYSTEM_125_BEB_BEO_METADATA_HANDOFF_COMPLETE",
                "EXACT_BLK_REQ_TRACE_METADATA_HANDOFF_COMPLETE_BY_125",
                "BEB_BEO_METADATA_HANDOFF_NO_PROTECTED_BODY_COPY_BY_125",
            ]
            missing = [marker for marker in current_markers if marker not in roadmap_body]
            self.assertEqual(missing, [], f"BLK-077 missing post-125 current markers: {missing}")
        elif "BLK_SYSTEM_124_STAGED_REVISION_PROMOTION_COMPLETE" in roadmap_body:
            current_markers = [
                "BLK_SYSTEM_124_STAGED_REVISION_PROMOTION_COMPLETE",
                "EXACT_ID_RETRIEVAL_BACKEND_COMPLETE_BY_122",
                "STAGED_REVISION_DRAFTS_WITH_PARENT_HASH_COMPLETE_BY_123",
                "HITL_STAGED_REVISION_PROMOTION_CONCURRENCY_COMPLETE_BY_124",
                "NEXT_FRONTIER_BEB_BEO_METADATA_HANDOFF_HARDENING_PLANNING_NOT_EXECUTION_AUTHORITY",
            ]
            missing = [marker for marker in current_markers if marker not in roadmap_body]
            self.assertEqual(missing, [], f"BLK-077 missing post-124 current markers: {missing}")
        else:
            missing = [marker for marker in shared if marker not in roadmap_body]
            self.assertEqual(missing, [], f"BLK-077 missing BLK-120 shared markers: {missing}")

        forbidden_active = [
            "Current boundary after BLK-SYSTEM-119: the active next high-level BLK-System completion frontier is BLK-req HITL baseline promotion planning/implementation",
            "NO_ACTIVE_VAULT_PROMOTION_OR_RETRIEVAL_BY_119",
            "BLK-SYSTEM-120 remains pending",
            "HITL baseline promotion remains pending",
            "the next frontier is `NEXT_FRONTIER_BLK_REQ_LEGISLATIVE_GATEWAY_PLANNING_NOT_EXECUTION_AUTHORITY`, not runtime authority",
            "now pins the active next high-level completion milestone as BLK-req legislative gateway implementation",
            "Current boundary after BLK-SYSTEM-111: the active next high-level BLK-System completion milestone is BLK-req legislative gateway implementation",
            "next frontier is publication-path decision gate only",
            "BLK-SYSTEM-125 now pins the active next frontier as `NEXT_FRONTIER_BEO_PUBLICATION_PATH_DECISION_GATE_PLANNING_NOT_EXECUTION_AUTHORITY`",
            "selects the BEO publication path decision gate as planning-only next frontier",
        ]
        leaks = []
        for label, path in [("BLK-077", BLK077), ("BLK-079", BLK079)]:
            body = path.read_text()
            for phrase in forbidden_active:
                if phrase in body:
                    leaks.append(f"{label}: {phrase}")
        self.assertEqual(leaks, [], f"stale active BLK-120 frontier wording remains: {leaks}")
