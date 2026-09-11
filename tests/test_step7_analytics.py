"""
SmartFeed AI - Step 7 Unit Tests
Validates Dashboard KPI aggregation, Plotly chart generation, and Early Spoilage Alert logic.
"""

import sys
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.analytics import (
    compute_dashboard_metrics,
    detect_early_spoilage_warning,
    create_quality_trend_chart,
    create_risk_distribution_chart
)


class TestAnalyticsAndSpoilage(unittest.TestCase):
    def setUp(self):
        # Synthetic historical test timeline
        self.mock_tests = [
            {"batch_id": "SFA-01", "sample_type": "Compound Cattle Feed", "quality_score": 88.0, "overall_risk": "Low", "moisture": 10.0, "mould_risk": "Low", "timestamp": "2026-09-01T10:00:00"},
            {"batch_id": "SFA-02", "sample_type": "Compound Cattle Feed", "quality_score": 82.0, "overall_risk": "Low", "moisture": 11.0, "mould_risk": "Low", "timestamp": "2026-09-03T10:00:00"},
            {"batch_id": "SFA-03", "sample_type": "Compound Cattle Feed", "quality_score": 68.0, "overall_risk": "Medium", "moisture": 13.5, "mould_risk": "Medium", "timestamp": "2026-09-05T10:00:00"},
            {"batch_id": "SFA-04", "sample_type": "Compound Cattle Feed", "quality_score": 45.0, "overall_risk": "High", "moisture": 16.0, "mould_risk": "High", "timestamp": "2026-09-07T10:00:00"},
        ]

    def test_compute_dashboard_metrics(self):
        """Validates metric aggregation for total tests, average score, and counts."""
        metrics = compute_dashboard_metrics(self.mock_tests)
        self.assertEqual(metrics["total_tests"], 4)
        # Average: (88 + 82 + 68 + 45) / 4 = 70.75 -> 70.8
        self.assertAlmostEqual(metrics["avg_quality_score"], 70.8, delta=0.2)
        self.assertEqual(metrics["safe_tests"], 2)
        self.assertEqual(metrics["caution_tests"], 1)
        self.assertEqual(metrics["high_risk_tests"], 1)

    def test_empty_metrics(self):
        """Empty input must not crash and should return clean zero defaults."""
        metrics = compute_dashboard_metrics([])
        self.assertEqual(metrics["total_tests"], 0)
        self.assertEqual(metrics["avg_quality_score"], 0.0)

    def test_early_spoilage_warning_triggered(self):
        """Progressive quality decline (88 -> 82 -> 68 -> 45) must trigger early spoilage warning."""
        alert = detect_early_spoilage_warning(self.mock_tests)
        self.assertTrue(alert["has_warning"])
        self.assertEqual(alert["severity"], "Severe")
        self.assertGreaterEqual(alert["total_drop"], 20.0)
        self.assertIn("Potential Spoilage Risk", alert["disclaimer"])
        self.assertTrue(len(alert["reasons"]) >= 2)

    def test_stable_trajectory_no_warning(self):
        """Stable scores should not trigger early spoilage warning."""
        stable_records = [
            {"quality_score": 86.0, "moisture": 10.0, "mould_risk": "Low"},
            {"quality_score": 88.0, "moisture": 10.2, "mould_risk": "Low"},
            {"quality_score": 87.0, "moisture": 10.1, "mould_risk": "Low"},
        ]
        alert = detect_early_spoilage_warning(stable_records)
        self.assertFalse(alert["has_warning"])
        self.assertEqual(alert["severity"], "None")

    def test_plotly_trend_figure_generation(self):
        """Verifies that Plotly figures are constructed with data traces."""
        fig = create_quality_trend_chart(self.mock_tests)
        self.assertIsNotNone(fig)
        self.assertEqual(len(fig.data), 1)
        self.assertEqual(fig.data[0].name, "Quality Score")

        # Bar chart
        bar_fig = create_risk_distribution_chart(self.mock_tests)
        self.assertIsNotNone(bar_fig)


if __name__ == "__main__":
    unittest.main()
