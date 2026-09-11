"""
SmartFeed AI - API Integration Tests for Animal Feed Recommendation Endpoint
Tests POST /api/animal-recommendation with TestClient.
"""

import unittest
from fastapi.testclient import TestClient
from server import app


class TestApiRation(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_api_animal_recommendation_lactating_cow(self):
        """API should return structured suitability and dosage for a lactating cow."""
        payload = {
            "feed_diagnostics": {
                "sample_type": "Cattle Feed Pellet",
                "health_score": 86.0,
                "overall_risk": "Low",
                "mould_risk": "Low",
                "adulteration_risk": "Low",
                "crude_protein": 18.0,
                "moisture": 10.0,
                "shelf_life_days": 15
            },
            "animal_params": {
                "animal_type": "Cow",
                "lactation_stage": "Lactating",
                "milk_yield_litres": 8.0,
                "body_weight_kg": 400.0
            },
            "language": "te"
        }
        res = self.client.post("/api/animal-recommendation", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["suitability_code"], "SUITABLE")
        self.assertTrue(data["is_safe"])
        self.assertEqual(data["animal_type"], "Cow")
        self.assertAlmostEqual(data["recommended_feed_kg"], 4.5, delta=0.2)
        self.assertIn("balanced_ration", data)
        self.assertIn("green_fodder_kg", data["balanced_ration"])
        self.assertIn("voice_script", data)

    def test_api_animal_recommendation_buffalo_pregnant(self):
        """API should calculate pregnancy allowance and 0 milk yield for buffalo."""
        payload = {
            "feed_diagnostics": {
                "sample_type": "Cattle Feed Pellet",
                "health_score": 88.0,
                "overall_risk": "Low",
                "mould_risk": "Low",
                "adulteration_risk": "Low",
                "crude_protein": 20.0,
                "moisture": 9.5,
                "shelf_life_days": 20
            },
            "animal_params": {
                "animal_type": "Buffalo",
                "lactation_stage": "Pregnant",
                "milk_yield_litres": 10.0
            },
            "language": "en"
        }
        res = self.client.post("/api/animal-recommendation", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["animal_type"], "Buffalo")
        self.assertEqual(data["lactation_stage"], "Pregnant")
        self.assertEqual(data["milk_yield_litres"], 0.0)
        # 1.75 maint + 1.25 preg = 3.0 kg
        self.assertAlmostEqual(data["recommended_feed_kg"], 3.0, delta=0.2)

    def test_api_animal_recommendation_high_risk_feed(self):
        """API should reject feed with 0 kg recommended for unsafe feed."""
        payload = {
            "feed_diagnostics": {
                "sample_type": "Cattle Feed Pellet",
                "health_score": 38.0,
                "overall_risk": "High",
                "mould_risk": "High",
                "adulteration_risk": "Low",
                "crude_protein": 15.0,
                "moisture": 20.0,
                "shelf_life_days": 0
            },
            "animal_params": {
                "animal_type": "Cow",
                "lactation_stage": "Pregnant"
            },
            "language": "te"
        }
        res = self.client.post("/api/animal-recommendation", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["suitability_code"], "REJECTED_UNSAFE")
        self.assertFalse(data["is_safe"])
        self.assertEqual(data["recommended_feed_kg"], 0.0)

    def test_api_scan_includes_animal_recommendation(self):
        """Verify that /api/scan response contains animal_recommendation payload."""
        with open("data/sample_images/sample_healthy_feed.jpg", "rb") as img:
            res = self.client.post(
                "/api/scan",
                data={
                    "sample_type": "Cattle Feed Pellet",
                    "crude_protein": "20.0",
                    "moisture": "10.0",
                    "fiber": "12.0",
                    "npn": "0.5",
                    "adulterant_powder": "0.0",
                    "storage_temp": "25.0",
                    "storage_humidity": "60.0",
                    "storage_days": "3",
                    "smell_abnormal": "false",
                    "language": "te"
                },
                files={"file": ("sample.jpg", img, "image/jpeg")}
            )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("animal_recommendation", data)
        self.assertIn("suitability_code", data["animal_recommendation"])
        self.assertIn("recommended_feed_kg", data["animal_recommendation"])


if __name__ == "__main__":
    unittest.main()
