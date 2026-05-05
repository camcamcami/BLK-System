import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLK003 = ROOT / "docs" / "BLK-003_blk-pipe-blk-test-orchestration.md"
BLK006 = ROOT / "docs" / "BLK-006_blk-req-implementation-brief.md"
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
