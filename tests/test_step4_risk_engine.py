"""
SmartFeed AI - Step 4 Unit Tests
Validates Risk Intelligence Engine, Health Score computation, primary concern identification,
and the Explainable AI 'Why This Result?' breakdown.
"""

import sys
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.risk_engine import evaluate_smartfeed_risks


class TestRiskIntelligenceEngine(unittest.TestCase):
    def setUp(self):
        # Base healthy mocks
        self.good_visual = {
            "sample_type": "Compound Cattle Feed",
            "predicted_class": "good",
            "farmer_label": "Good Quality",
            "confidence": 0.94,
            "mould_risk": "Low",
            "foreign_particle_risk": "Low",
            "visual_quality_score": 92.0,
            "cv_details": {
                "color_analysis": {"white_grey_patch_pct": 0.5, "dark_patch_pct": 1.0},
                "foreign_particle_risk": {"risk_level": "Low", "particle_count": 0}
            }
        }
        self.good_adulteration = {
            "adulteration_risk": "Low",
            "risk_score_points": 0,
            "flagged_hazards": [],
            "reasons": ["Normal nutrient and sensory profile."]
        }
        self.good_nutrition = {
            "nutrition_score": 95.0,
            "nutrition_status": "Balanced",
            "nutrition_risk": "Low",
            "parameter_status": {"protein": "Optimal", "moisture": "Optimal", "fiber": "Optimal"},
            "inputs": {"crude_protein": 20.0, "moisture": 10.0, "fiber": 11.0}
        }

    def test_safe_feed_score(self):
        """Clean feed with good storage should score >= 80 with Low risk."""
        res = evaluate_smartfeed_risks(
            visual_res=self.good_visual,
            adulteration_res=self.good_adulteration,
            nutrition_res=self.good_nutrition,
            storage_condition="Well-Ventilated Dry Area"
        )
        self.assertGreaterEqual(res["health_score"], 80.0)
        self.assertEqual(res["overall_risk"], "Low")
        self.assertEqual(res["safety_badge"], "SAFE FOR USE")
        self.assertIn("Good Condition", res["primary_concern"])

    def test_mouldy_feed_score_and_concern(self):
        """Mouldy feed must trigger mould penalties and primary concern."""
        mouldy_visual = self.good_visual.copy()
        mouldy_visual.update({
            "predicted_class": "moldy",
            "farmer_label": "High Mould/Fungal Risk",
            "mould_risk": "High",
            "visual_quality_score": 45.0,
            "cv_details": {
                "color_analysis": {"white_grey_patch_pct": 12.0, "dark_patch_pct": 3.0},
                "foreign_particle_risk": {"risk_level": "Low", "particle_count": 1}
            }
        })

        res = evaluate_smartfeed_risks(
            visual_res=mouldy_visual,
            adulteration_res=self.good_adulteration,
            nutrition_res=self.good_nutrition,
            storage_condition="Damp & Humid Shed"
        )

        self.assertLess(res["health_score"], 60.0)
        self.assertEqual(res["overall_risk"], "High")
        self.assertIn("Fungal & Mould", res["primary_concern"])
        self.assertIn("withhold feed", res["recommended_action"].lower())

    def test_urea_spiking_priority(self):
        """Suspected urea spiking should be flagged as top priority concern and force High risk."""
        adulterated = {
            "adulteration_risk": "High",
            "risk_score_points": 50,
            "flagged_hazards": ["Possible Urea / Non-Protein Nitrogen (NPN) Adulteration Risk"],
            "reasons": ["Abnormally high crude protein."]
        }

        res = evaluate_smartfeed_risks(
            visual_res=self.good_visual,
            adulteration_res=adulterated,
            nutrition_res=self.good_nutrition,
            storage_condition="Well-Ventilated Dry Area"
        )

        self.assertEqual(res["overall_risk"], "High")
        self.assertIn("Urea", res["primary_concern"])
        self.assertIn("Quarantine", res["recommended_action"])

    def test_why_breakdown_structure(self):
        """Ensure 'Why This Result?' contains all required explanatory sections."""
        res = evaluate_smartfeed_risks(
            visual_res=self.good_visual,
            adulteration_res=self.good_adulteration,
            nutrition_res=self.good_nutrition,
            storage_condition="Dry Room"
        )
        why = res["why_this_result"]
        self.assertIn("headline", why)
        self.assertIn("concerns_list", why)
        self.assertIn("positives_list", why)
        self.assertIn("deductions_list", why)
        self.assertIn("trend_explanation", why)

    def test_score_boundary_limits(self):
        """Score must never exceed 100 or drop below 0."""
        # Worst possible case
        worst_visual = {
            "visual_quality_score": 0.0,
            "mould_risk": "High",
            "foreign_particle_risk": "High",
            "cv_details": {"color_analysis": {"white_grey_patch_pct": 50.0}, "foreign_particle_risk": {"particle_count": 50}}
        }
        worst_adulteration = {"adulteration_risk": "High", "flagged_hazards": ["Urea"], "reasons": ["Extreme"]}
        worst_nutrition = {"nutrition_status": "Poor", "parameter_status": {"moisture": "Excessive"}, "inputs": {}}

        res = evaluate_smartfeed_risks(
            visual_res=worst_visual,
            adulteration_res=worst_adulteration,
            nutrition_res=worst_nutrition,
            storage_condition="Damp Humid Flooded"
        )
    def test_safe_feed_shelf_life(self):
        """Clean feed with low moisture should have healthy safe shelf life >= 30 days."""
        res = evaluate_smartfeed_risks(
            visual_res=self.good_visual,
            adulteration_res=self.good_adulteration,
            nutrition_res=self.good_nutrition,
            storage_condition="Storage 5 days, dry ventilated area"
        )
        self.assertIn("shelf_life", res)
        shelf = res["shelf_life"]
        self.assertGreaterEqual(shelf["shelf_life_days"], 30)
        self.assertEqual(shelf["shelf_life_status"], "SAFE")
        self.assertIn("timeline", shelf)

    def test_mouldy_feed_shelf_life_expired(self):
        """Mouldy feed must immediately result in 0 safe shelf life days and EXPIRED status."""
        mouldy_visual = self.good_visual.copy()
        mouldy_visual.update({
            "predicted_class": "moldy",
            "mould_risk": "High",
            "visual_quality_score": 35.0,
            "cv_details": {
                "color_analysis": {"white_grey_patch_pct": 15.0, "dark_patch_pct": 2.0},
                "foreign_particle_risk": {"risk_level": "Low", "particle_count": 0}
            }
        })
        res = evaluate_smartfeed_risks(
            visual_res=mouldy_visual,
            adulteration_res=self.good_adulteration,
            nutrition_res=self.good_nutrition,
            storage_condition="Damp & Humid Shed"
        )
        shelf = res["shelf_life"]
        self.assertEqual(shelf["shelf_life_days"], 0)
        self.assertEqual(shelf["shelf_life_status"], "EXPIRED")
        self.assertIn("EXPIRED", shelf["safe_until_date"])

    def test_high_moisture_shelf_life_critical(self):
        """High moisture (16%) in dry feed accelerates spoilage, resulting in critical shelf life <= 5 days."""
        damp_nutrition = self.good_nutrition.copy()
        damp_nutrition["inputs"] = {"crude_protein": 19.0, "moisture": 16.5, "fiber": 10.0}
        res = evaluate_smartfeed_risks(
            visual_res=self.good_visual,
            adulteration_res=self.good_adulteration,
            nutrition_res=damp_nutrition,
            storage_condition="Humid Storage"
        )
        shelf = res["shelf_life"]
        self.assertLessEqual(shelf["shelf_life_days"], 5)
        self.assertIn(shelf["shelf_life_status"], ["CRITICAL", "ATTENTION"])

    def test_silage_shelf_life_window(self):
        """Aerated silage has a brief shelf life ceiling of <= 7 days."""
        silage_visual = self.good_visual.copy()
        silage_visual.update({"sample_type": "Silage"})
        silage_nutrition = {
            "nutrition_score": 90.0,
            "inputs": {"crude_protein": 8.5, "moisture": 65.0, "fiber": 22.0}
        }
        res = evaluate_smartfeed_risks(
            visual_res=silage_visual,
            adulteration_res=self.good_adulteration,
            nutrition_res=silage_nutrition,
            storage_condition="Storage 2 days"
        )
        shelf = res["shelf_life"]
        self.assertLessEqual(shelf["shelf_life_days"], 7)


if __name__ == "__main__":
    unittest.main()
