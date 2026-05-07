from pathlib import Path
import unittest
from unittest.mock import patch

from beo_rtm_interface_fixtures import build_beo_rtm_interface_fixture

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / "python"
TRACE_ARTIFACTS = [
    {"kind": "REQ", "id": "REQ-S17-001", "version_hash": "sha256:" + "1" * 64}
]


def draft_beo(**overrides):
    beo = {
        "beo_id": "BEO_S17_GUARD_001",
        "beb_id": "BEB_S17_GUARD_001",
        "status": "PASS",
        "pre_engine_hash": "sha256:" + "2" * 64,
        "trace_artifacts": list(TRACE_ARTIFACTS),
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
    }
    beo.update(overrides)
    return beo


class RtmLedgerDesignGateTest(unittest.TestCase):
    def test_existing_beo_rtm_interface_remains_disabled_only(self):
        interface = build_beo_rtm_interface_fixture(
            draft_beo(), interface_id="RTM_IFACE_S17_GUARD_001"
        )

        self.assertEqual(interface["rtm_status"], "NOT_GENERATED")
        self.assertEqual(interface["rtm_authority"], "DISABLED_INTERFACE_ONLY")
        self.assertFalse(interface["active_vault_read"])
        self.assertFalse(interface["requirements_resolved"])
        forbidden = {
            "rtm",
            "rtm_id",
            "requirements",
            "coverage_matrix",
            "coverage_status",
            "drift",
            "drift_decision",
        }
        self.assertTrue(forbidden.isdisjoint(interface))

    def test_generated_rtm_fields_still_reject(self):
        for field in ("rtm", "rtm_id", "requirements", "coverage_matrix"):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, "generated RTM authority field"):
                    build_beo_rtm_interface_fixture(
                        draft_beo(**{field: "forbidden"}),
                        interface_id="RTM_IFACE_S17_GUARD_002",
                    )

    def test_active_vault_paths_are_not_read_by_disabled_interface(self):
        forbidden = ("docs/active", "docs/requirements", "docs/use_cases")

        def fail_forbidden_read(self_path, *args, **kwargs):
            as_text = str(self_path)
            if any(token in as_text for token in forbidden):
                raise AssertionError(f"forbidden active vault read: {as_text}")
            return ""

        with patch.object(Path, "read_text", fail_forbidden_read):
            interface = build_beo_rtm_interface_fixture(
                draft_beo(), interface_id="RTM_IFACE_S17_GUARD_003"
            )

        self.assertEqual(interface["rtm_status"], "NOT_GENERATED")
        self.assertFalse(interface["active_vault_read"])

    def test_production_python_does_not_define_rtm_generator_or_drift_runtime(self):
        forbidden_markers = [
            "def generate_rtm",
            "class RtmLedger",
            "rtm_status = \"GENERATED\"",
            "rtm_status='GENERATED'",
            "coverage_matrix =",
            "drift_decision =",
            "active_vault_hash_compare",
        ]
        offenders = []
        for path in PYTHON.glob("*.py"):
            if path.name.startswith("test_"):
                continue
            text = path.read_text()
            for marker in forbidden_markers:
                if marker in text:
                    offenders.append(f"{path.relative_to(ROOT)}: {marker}")
        self.assertEqual(offenders, [], f"Sprint 017 introduced runtime RTM markers: {offenders}")


if __name__ == "__main__":
    unittest.main()
