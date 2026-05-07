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
BLK025 = ROOT / "docs" / "BLK-025_blk-test-pilot-readiness-boundary.md"
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
