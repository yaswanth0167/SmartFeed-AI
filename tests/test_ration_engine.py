"""
SmartFeed AI - Unit Tests for Scientific Ration & Animal Feed Recommendation Engine
Validates ICAR dairy cattle nutrition standards, suitability classifications, and multilingual guidance.
"""

import sys
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.ration_engine import calculate_animal_feed_recommendation


class TestRationEngine(unittest.TestCase):

    def setUp(self):
        self.safe_feed = {
            "sample_type": "Cattle Feed Pellet",
            "health_score": 88.0,
            "overall_risk": "Low",
            "mould_risk": "Low",
            "adulteration_risk": "Low",
            "crude_protein": 18.0,
            "moisture": 10.0,
            "shelf_life_days": 18
        }

        self.mouldy_feed = {
            "sample_type": "Cattle Feed Pellet",
            "health_score": 35.0,
            "overall_risk": "High",
            "mould_risk": "High",
            "adulteration_risk": "Low",
            "crude_protein": 14.0,
            "moisture": 22.0,
            "shelf_life_days": 0
        }

        self.urea_spiked_feed = {
            "sample_type": "Cattle Feed Pellet",
            "health_score": 42.0,
            "overall_risk": "High",
            "mould_risk": "Low",
            "adulteration_risk": "High",
            "crude_protein": 28.0,
            "moisture": 9.0,
            "shelf_life_days": 10
        }

    def test_lactating_cow_safe_feed(self):
        """Lactating cow (8L/day) with safe feed should be SUITABLE with ~4.5kg concentrate."""
        res = calculate_animal_feed_recommendation(
            feed_diagnostics=self.safe_feed,
            animal_params={
                "animal_type": "Cow",
                "lactation_stage": "Lactating",
                "milk_yield_litres": 8.0,
                "body_weight_kg": 400.0
            },
            language="te"
        )
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["suitability_code"], "SUITABLE")
        self.assertTrue(res["is_safe"])
        self.assertEqual(res["animal_type"], "Cow")
        self.assertEqual(res["lactation_stage"], "Lactating")
        # 1.25 maint + 8/2.5 (=3.2) = 4.45 ~ 4.5 kg
        self.assertAlmostEqual(res["recommended_feed_kg"], 4.5, delta=0.2)
        self.assertGreater(res["morning_dose_kg"], 0)
        self.assertGreater(res["evening_dose_kg"], 0)
        self.assertIn("green_fodder_kg", res["balanced_ration"])
        self.assertIn("dry_straw_kg", res["balanced_ration"])
        self.assertEqual(len(res["transition_schedule"]), 4)
        self.assertIn("ఆవు", res["headline"])
        self.assertIn("voice_script", res)

    def test_lactating_buffalo_higher_fat_ratio(self):
        """Buffalo requires 1kg concentrate per 2.0L milk (due to higher fat 6-8%)."""
        res = calculate_animal_feed_recommendation(
            feed_diagnostics=self.safe_feed,
            animal_params={
                "animal_type": "Buffalo",
                "lactation_stage": "Lactating",
                "milk_yield_litres": 10.0,
                "body_weight_kg": 500.0
            },
            language="en"
        )
        self.assertEqual(res["suitability_code"], "SUITABLE")
        # 1.75 maint + 10/2.0 (=5.0) = 6.75 ~ 6.8 kg
        self.assertAlmostEqual(res["recommended_feed_kg"], 6.8, delta=0.2)
        self.assertGreater(res["balanced_ration"]["clean_water_litres"], 60)
        self.assertIn("Buffalo", res["headline"])

    def test_pregnant_cattle_allowance(self):
        """Pregnant cattle should have 0 milk yield and include pregnancy allowance."""
        res = calculate_animal_feed_recommendation(
            feed_diagnostics=self.safe_feed,
            animal_params={
                "animal_type": "Cow",
                "lactation_stage": "Pregnant",
                "milk_yield_litres": 10.0 # should be overridden to 0
            },
            language="hi"
        )
        self.assertEqual(res["milk_yield_litres"], 0.0)
        # 1.25 maint + 1.25 preg = 2.5 kg
        self.assertAlmostEqual(res["recommended_feed_kg"], 2.5, delta=0.2)
        self.assertIn("गर्भवती", res["headline"])

    def test_dry_cattle_maintenance_only(self):
        """Dry cattle should only receive maintenance concentrate."""
        res = calculate_animal_feed_recommendation(
            feed_diagnostics=self.safe_feed,
            animal_params={
                "animal_type": "Cow",
                "lactation_stage": "Dry"
            },
            language="te"
        )
        self.assertEqual(res["milk_yield_litres"], 0.0)
        self.assertAlmostEqual(res["recommended_feed_kg"], 1.25, delta=0.2)

    def test_unsafe_mouldy_feed_rejection(self):
        """Mouldy feed must be strictly REJECTED_UNSAFE with 0 kg recommended dosage."""
        res = calculate_animal_feed_recommendation(
            feed_diagnostics=self.mouldy_feed,
            animal_params={
                "animal_type": "Cow",
                "lactation_stage": "Pregnant"
            },
            language="te"
        )
        self.assertEqual(res["suitability_code"], "REJECTED_UNSAFE")
        self.assertFalse(res["is_safe"])
        self.assertEqual(res["recommended_feed_kg"], 0.0)
        self.assertEqual(res["morning_dose_kg"], 0.0)
        self.assertEqual(res["evening_dose_kg"], 0.0)
        # Verify clinical abortion warning for pregnant animal
        self.assertIn("గర్భస్రావం", res["stage_clinical_note"])

    def test_unsafe_urea_spiked_feed_rejection(self):
        """Urea adulterated feed must be strictly rejected with 0 kg dosage."""
        res = calculate_animal_feed_recommendation(
            feed_diagnostics=self.urea_spiked_feed,
            animal_params={
                "animal_type": "Cow",
                "lactation_stage": "Lactating",
                "milk_yield_litres": 12.0
            },
            language="en"
        )
        self.assertEqual(res["suitability_code"], "REJECTED_UNSAFE")
        self.assertEqual(res["recommended_feed_kg"], 0.0)
        self.assertIn("REJECTED", res["verdict_badge"])

    def test_silage_feed_dosage(self):
        """Silage should recommend forage-scale volume (~18-22 kg fresh silage)."""
        silage_feed = {
            "sample_type": "Maize Silage",
            "health_score": 85.0,
            "overall_risk": "Low",
            "mould_risk": "Low",
            "adulteration_risk": "Low",
            "crude_protein": 8.5,
            "moisture": 65.0,
            "shelf_life_days": 10
        }
        res = calculate_animal_feed_recommendation(
            feed_diagnostics=silage_feed,
            animal_params={
                "animal_type": "Cow",
                "lactation_stage": "Lactating",
                "milk_yield_litres": 8.0
            },
            language="te"
        )
        self.assertEqual(res["suitability_code"], "SUITABLE")
        self.assertGreaterEqual(res["recommended_feed_kg"], 15.0)

    def test_all_languages_populated(self):
        """Ensure Telugu, Hindi, and English are all generated in all_languages dict."""
        res = calculate_animal_feed_recommendation(
            feed_diagnostics=self.safe_feed,
            animal_params={"animal_type": "Cow", "lactation_stage": "Lactating", "milk_yield_litres": 6.0}
        )
        self.assertIn("te", res["all_languages"])
        self.assertIn("hi", res["all_languages"])
        self.assertIn("en", res["all_languages"])
        self.assertTrue(len(res["all_languages"]["te"]["voice_script"]) > 10)
        self.assertTrue(len(res["all_languages"]["hi"]["voice_script"]) > 10)
        self.assertTrue(len(res["all_languages"]["en"]["voice_script"]) > 10)


if __name__ == "__main__":
    unittest.main()
