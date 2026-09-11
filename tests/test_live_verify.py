"""
SmartFeed AI - Live Verification of Animal Feed Recommendation System
"""

import requests
import unittest
from db.database import seed_demo_farmer, wipe_all_except_admin

BASE = "http://localhost:8000"


class TestLiveAnimalSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        seed_demo_farmer()

    @classmethod
    def tearDownClass(cls):
        wipe_all_except_admin()

    def test_01_farmer_login_and_animals(self):
        login_res = requests.post(f"{BASE}/api/auth/login", json={"mobile": "9876543210", "password": "farmer123"})
        self.assertEqual(login_res.status_code, 200)
        farmer = login_res.json()["user"]
        self.assertIn("Ramesh Kumar", farmer["full_name"])

        animals_res = requests.get(f"{BASE}/api/farmer/animals?user_id={farmer['id']}")
        self.assertEqual(animals_res.status_code, 200)
        animals = animals_res.json()["animals"]
        self.assertGreater(len(animals), 0)

    def test_02_scan_with_animal_recommendation(self):
        with open("data/sample_images/sample_healthy_feed.jpg", "rb") as f:
            scan_res = requests.post(
                f"{BASE}/api/scan",
                data={
                    "sample_type": "Cattle Feed Pellet",
                    "crude_protein": "18.0",
                    "moisture": "10.0",
                    "storage_days": "3",
                    "language": "te",
                    "user_id": 2
                },
                files={"file": ("sample.jpg", f, "image/jpeg")}
            )
        self.assertEqual(scan_res.status_code, 200)
        data = scan_res.json()
        self.assertIn("animal_recommendation", data)
        rec = data["animal_recommendation"]
        self.assertEqual(rec["status"], "success")
        self.assertEqual(rec["suitability_code"], "SUITABLE")
        self.assertGreater(rec["recommended_feed_kg"], 0)
        self.assertIn("balanced_ration", rec)
        self.assertEqual(len(rec["transition_schedule"]), 4)

    def test_03_dedicated_endpoint_buffalo(self):
        buff_res = requests.post(
            f"{BASE}/api/animal-recommendation",
            json={
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
                    "lactation_stage": "Lactating",
                    "milk_yield_litres": 10.0
                },
                "language": "en"
            }
        )
        self.assertEqual(buff_res.status_code, 200)
        data = buff_res.json()
        self.assertEqual(data["suitability_code"], "SUITABLE")
        self.assertAlmostEqual(data["recommended_feed_kg"], 6.8, delta=0.2)
        self.assertIn("Buffalo", data["headline"])

    def test_04_tts_voice_guidance(self):
        tts_res = requests.post(f"{BASE}/api/tts", json={"text": "Feed is suitable for your cow.", "language": "en"})
        self.assertEqual(tts_res.status_code, 200)
        self.assertGreater(len(tts_res.content), 500)


if __name__ == "__main__":
    unittest.main()
