"""
SmartFeed AI - Step 5 Unit Tests
Validates Multilingual Farmer Advisory Engine across English, Telugu, and Hindi,
ensuring robust offline rule generation and fallback behavior.
"""

import sys
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.advisory import generate_advisory, generate_offline_advisory


class TestAdvisoryEngine(unittest.TestCase):
    def setUp(self):
        self.sample_safe = {
            "sample_type": "Compound Cattle Feed",
            "health_score": 88.0,
            "overall_risk": "Low",
            "farmer_label": "Good Quality",
            "mould_risk": "Low",
            "foreign_particle_risk": "Low",
            "adulteration_risk": "Low",
            "storage_condition": "Well-Ventilated Dry Area",
            "moisture": 10.5,
            "crude_protein": 19.5,
            "fiber": 10.0,
            "protein_status": "Optimal",
            "flagged_hazards": []
        }

        self.sample_mouldy = {
            "sample_type": "Feed Ingredient",
            "health_score": 42.0,
            "overall_risk": "High",
            "farmer_label": "High Mould/Fungal Risk",
            "mould_risk": "High",
            "foreign_particle_risk": "Low",
            "adulteration_risk": "Low",
            "storage_condition": "Damp & Humid Shed",
            "moisture": 16.0,
            "crude_protein": 18.0,
            "fiber": 12.0,
            "protein_status": "Optimal",
            "flagged_hazards": []
        }

        self.sample_urea = {
            "sample_type": "Compound Cattle Feed",
            "health_score": 40.0,
            "overall_risk": "High",
            "farmer_label": "Normal Appearance",
            "mould_risk": "Low",
            "foreign_particle_risk": "Low",
            "adulteration_risk": "High",
            "storage_condition": "Dry Area",
            "moisture": 9.5,
            "crude_protein": 30.0,
            "fiber": 8.0,
            "protein_status": "Abnormally High",
            "flagged_hazards": ["Possible Urea / Non-Protein Nitrogen (NPN) Adulteration Risk"]
        }

    def test_english_safe_advisory(self):
        """Safe feed in English should produce reassuring guidance and high score note."""
        adv = generate_advisory(self.sample_safe, language="en", provider="offline")
        self.assertEqual(adv["language"], "en")
        self.assertIn("Safe for Feeding", adv["safety_status"])
        self.assertTrue(adv["is_offline_fallback"])
        self.assertIn("dry", adv["storage_advice"].lower())

    def test_telugu_mould_advisory(self):
        """High mould sample in Telugu must warn about fungal toxicity in Telugu script."""
        adv = generate_advisory(self.sample_mouldy, language="te", provider="offline")
        self.assertEqual(adv["language"], "te")
        self.assertIn("తీవ్ర ప్రమాదం", adv["safety_status"])
        # Check for presence of Telugu text warning
        full_text = adv["full_advisory_text"]
        self.assertIn("ఫంగస్", full_text)
        self.assertIn("బూజు", full_text)
        self.assertIn("మేత", full_text)

    def test_hindi_urea_advisory(self):
        """Urea adulteration in Hindi must warn in Devanagari script."""
        adv = generate_advisory(self.sample_urea, language="hi", provider="offline")
        self.assertEqual(adv["language"], "hi")
        self.assertIn("उच्च जोखिम", adv["safety_status"])
        full_text = adv["full_advisory_text"]
        self.assertIn("यूरिया", full_text)
        self.assertIn("प्रयोगशाला", full_text)

    def test_advisory_keys_complete(self):
        """Ensure all required keys exist in response."""
        adv = generate_advisory(self.sample_safe, language="en")
        required_keys = ["safety_status", "main_problems", "recommended_actions", "storage_advice", "full_advisory_text", "language"]
        for k in required_keys:
            self.assertIn(k, adv)


if __name__ == "__main__":
    unittest.main()
