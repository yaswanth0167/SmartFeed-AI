"""
SmartFeed AI - Step 3 Unit Tests
Validates nutrition analysis benchmarks and adulteration risk screening.
"""

import sys
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.nutrition import analyze_nutrition, load_reference_ranges
from utils.adulteration import check_adulteration_risk, calculate_safe_urea_dosage


class TestNutritionAndAdulteration(unittest.TestCase):
    def test_load_reference_ranges(self):
        """Verify nutrient reference ranges are loaded from CSV."""
        refs = load_reference_ranges()
        self.assertIn("Compound Cattle Feed", refs)
        self.assertIn("Silage", refs)
        self.assertIn("Feed Ingredient", refs)
        self.assertEqual(refs["Compound Cattle Feed"]["protein_min"], 18.0)

    def test_nutrition_balanced(self):
        """Standard balanced concentrate feed should yield Balanced status."""
        res = analyze_nutrition(
            sample_type="Compound Cattle Feed",
            crude_protein=20.0,
            moisture=10.0,
            fiber=11.0
        )
        self.assertEqual(res["nutrition_status"], "Balanced")
        self.assertEqual(res["nutrition_risk"], "Low")
        self.assertGreaterEqual(res["nutrition_score"], 80.0)

    def test_nutrition_high_moisture_dry_feed(self):
        """High moisture in dry cattle feed should trigger spoilage warning."""
        res = analyze_nutrition(
            sample_type="Compound Cattle Feed",
            crude_protein=19.0,
            moisture=16.5,
            fiber=10.0
        )
        self.assertIn("Excessive", res["parameter_status"]["moisture"])
        self.assertNotEqual(res["nutrition_status"], "Balanced")

    def test_nutrition_silage_balance(self):
        """Silage with typical 65% moisture should be optimal."""
        res = analyze_nutrition(
            sample_type="Silage",
            crude_protein=8.5,
            moisture=66.0,
            fiber=24.0
        )
        self.assertEqual(res["nutrition_status"], "Balanced")
        self.assertEqual(res["parameter_status"]["moisture"], "Optimal")

    def test_adulteration_normal_sample(self):
        """Standard feed without anomalies should have Low adulteration risk."""
        res = check_adulteration_risk(
            feed_type="Compound Cattle Feed",
            color_desc="Normal",
            texture_desc="Fine",
            smell_desc="Normal",
            storage_condition="Dry & Ventilated",
            foreign_particles="Low",
            crude_protein=19.5,
            moisture=10.0,
            fiber=10.5
        )
        self.assertEqual(res["adulteration_risk"], "Low")
        self.assertIn("Laboratory testing is recommended", res["disclaimer"])

    def test_adulteration_urea_hazard(self):
        """Spiked protein + powdery texture should flag Possible Urea Adulteration Risk."""
        res = check_adulteration_risk(
            feed_type="Compound Cattle Feed",
            color_desc="Normal",
            texture_desc="Powdery",
            smell_desc="Unusual",
            storage_condition="Dry & Ventilated",
            foreign_particles=False,
            crude_protein=29.0,
            moisture=9.5,
            fiber=9.0
        )
        self.assertEqual(res["adulteration_risk"], "High")
        self.assertTrue(any("Urea" in hazard for hazard in res["flagged_hazards"]))
        # Crucial: Check that certainty claims are NOT made
        self.assertFalse(any("Urea Confirmed" in r for r in res["reasons"]))

    def test_adulteration_foreign_particle_hazard(self):
        """Unusual color + distinct visible particles should flag high contamination risk."""
        res = check_adulteration_risk(
            feed_type="Feed Ingredient",
            color_desc="Unusual",
            texture_desc="Rough",
            smell_desc="Normal",
            storage_condition="Poorly Ventilated",
            foreign_particles="High",
            crude_protein=18.0,
            moisture=10.0,
            fiber=12.0
        )
        self.assertIn(res["adulteration_risk"], ["Medium", "High"])
        self.assertTrue(len(res["flagged_hazards"]) > 0)

    def test_safe_urea_straw_treatment_100kg(self):
        """Test ICAR 4% straw treatment benchmark for 100kg dry straw."""
        res = calculate_safe_urea_dosage(
            mode="straw_treatment",
            quantity_kg=100.0,
            num_animals=2,
            language="en"
        )
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["safe_urea_kg"], 4.0)
        self.assertEqual(res["required_water_liters"], 45.0)
        self.assertEqual(res["curing_days"], 21)
        self.assertIn("+5.0% CP", res["crude_protein_boost"])
        self.assertTrue(len(res["steps"]) >= 5)
        self.assertIn("Vinegar", res["antidote_guide"]["en"])

    def test_safe_urea_straw_treatment_te(self):
        """Test Telugu language support for straw treatment."""
        res = calculate_safe_urea_dosage(
            mode="straw_treatment",
            quantity_kg=200.0,
            num_animals=4,
            language="te"
        )
        self.assertEqual(res["safe_urea_kg"], 8.0)
        self.assertEqual(res["required_water_liters"], 90.0)
        self.assertIn("యూరియా", res["summary"])
        self.assertIn("వెనిగర్", res["antidote_guide"]["te"])

    def test_safe_urea_concentrate_mix_cows(self):
        """Test concentrate mixing capped at safe daily allowance and calf warnings."""
        res = calculate_safe_urea_dosage(
            mode="concentrate_mix",
            quantity_kg=20.0,
            num_animals=3,
            language="en"
        )
        self.assertEqual(res["status"], "success")
        # 3 cows * 70g max = 210g total
        self.assertLessEqual(res["safe_urea_kg"] * 1000, 210.0)
        self.assertTrue(any("ZERO UREA FOR CALVES" in p for p in res["precautions"]))
        self.assertIn("Vinegar", res["antidote_guide"]["en"])


if __name__ == "__main__":
    unittest.main()
