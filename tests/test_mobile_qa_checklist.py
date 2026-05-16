import re
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHECKLIST_PATH = PROJECT_ROOT / "issues" / "mobile-qa-checklist.md"
LANDSCAPE_DECISION_PATH = PROJECT_ROOT / "issues" / "landscape-layout-decision.md"


class MobileQaChecklistTests(unittest.TestCase):
    def test_real_device_checklist_covers_required_mobile_qa(self):
        self.assertTrue(CHECKLIST_PATH.exists(), "Mobile QA checklist should exist")
        checklist = CHECKLIST_PATH.read_text(encoding="utf-8")

        required_sections = (
            "Small Portrait Phone",
            "Tall Portrait Phone",
            "Landscape Phone",
            "Safari iPhone Observations",
            "Chrome Android Observations",
            "Follow-up Decisions",
        )
        for section in required_sections:
            self.assertIn(section, checklist)

        required_checks = (
            "maze readability",
            "D-pad reachability",
            "page scrolling",
            "held direction",
            "pause",
            "restart",
            "desktop keyboard regression",
        )
        for check in required_checks:
            self.assertRegex(checklist, re.compile(re.escape(check), re.IGNORECASE))

        required_decisions = (
            "sizing",
            "landscape",
            "held state",
            "restart safety",
            "test needs",
        )
        for decision in required_decisions:
            self.assertRegex(checklist, re.compile(re.escape(decision), re.IGNORECASE))

    def test_landscape_layout_decision_is_recorded(self):
        self.assertTrue(LANDSCAPE_DECISION_PATH.exists(), "Landscape layout decision should exist")
        decision = LANDSCAPE_DECISION_PATH.read_text(encoding="utf-8")

        required_content = (
            "issues/005-landscape-mobile-layout-decision.md",
            "Representative Mobile Landscape Viewports",
            "Decision",
            "landscape layout required",
            "controls reachable",
            "controls do not cover the canvas",
            "gameplay-disrupting page scroll",
            "portrait layout remains unchanged",
        )
        for content in required_content:
            self.assertRegex(decision, re.compile(re.escape(content), re.IGNORECASE))


if __name__ == "__main__":
    unittest.main()
