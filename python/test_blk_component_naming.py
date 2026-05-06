from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLK001 = ROOT / "docs" / "BLK-001_blk-system-master-architecture.md"
CURRENT_DOCTRINE = sorted((ROOT / "docs").glob("BLK-*.md"))


def test_blk001_declares_canonical_component_names():
    text = BLK001.read_text(encoding="utf-8")
    required = [
        "`blk-id` (The Identity Spine)",
        "`blk-relay` (The Signal Bus)",
        "`blk-link` (The Ledger)",
        "version_hash",
        "does not authorize the payload it carries",
    ]
    missing = [marker for marker in required if marker not in text]
    assert missing == []


def test_current_blk_doctrine_uses_blk_link_not_stale_aggregator_names():
    assert CURRENT_DOCTRINE, "expected current BLK doctrine files"
    stale_terms = ("BLK-Link", "RTM Aggregator", "Traceability Aggregator")
    stale_hits = []
    for path in CURRENT_DOCTRINE:
        text = path.read_text(encoding="utf-8")
        for term in stale_terms:
            if term in text:
                stale_hits.append(f"{path.relative_to(ROOT)}: {term}")
    assert stale_hits == []
