import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLK003 = ROOT / "docs" / "BLK-003_blk-pipe-blk-test-orchestration.md"
BLK006 = ROOT / "docs" / "BLK-006_blk-req-implementation-brief.md"
BLK008 = ROOT / "docs" / "BLK-008_blk-test-mcp-execution-server.md"
BLK015 = ROOT / "docs" / "BLK-015_blk-pipe-approval-and-mcp-integration-design.md"
BLK016 = ROOT / "docs" / "BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md"
BLK017 = ROOT / "docs" / "BLK-017_blk-test-mcp-disabled-transport-skeleton.md"
BLK018 = ROOT / "docs" / "BLK-018_blk-test-mcp-workspace-process-control-probes.md"
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
            "Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke",
            "python/blk_test_mcp_workspace_process_probes.py",
            "python/test_blk_test_mcp_workspace_process_probes.py",
            "python/test_active_doctrine_review_gates.py",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-018 workspace/process markers missing: {missing}")

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
                "until live authority is separately approved",
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
