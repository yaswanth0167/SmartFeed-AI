"""
SmartFeed AI - Full Live Process Verification Suite
Verifies all 8 systems on running server:
1. Auth & Admin/Farmer Isolation
2. Feed Quality Vision Scanner
3. Biochemical Adulteration & NPN Screening
4. Multilingual Advisory & TTS
5. Animal-Specific Feed Recommendation Engine
6. Time-Based Smart Feeding Planner & Dairy Intelligence
7. Digital Feed Passport & QR Traceability
8. Analytics Dashboard & Early Spoilage Alerting
"""
import unittest
import requests
from db.database import seed_demo_farmer, wipe_all_except_admin

BASE = "http://localhost:8000"


class TestAllLiveProcesses(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        seed_demo_farmer()

    @classmethod
    def tearDownClass(cls):
        wipe_all_except_admin()

    def test_01_authentication_and_isolation(self):
        # Admin signin
        admin_res = requests.post(f"{BASE}/api/auth/login", json={"mobile": "8341016049", "password": "6049"})
        self.assertEqual(admin_res.status_code, 200)
        admin_data = admin_res.json()
        self.assertEqual(admin_data["user"]["role"], "admin")

        # Admin farmers and KPIs
        kpis_res = requests.get(f"{BASE}/api/admin/kpis")
        self.assertEqual(kpis_res.status_code, 200)
        farmers_res = requests.get(f"{BASE}/api/admin/farmers")
        self.assertEqual(farmers_res.status_code, 200)
        self.assertGreater(len(farmers_res.json()["farmers"]), 0)

        # Farmer signin
        farmer_res = requests.post(f"{BASE}/api/auth/login", json={"mobile": "9876543210", "password": "farmer123"})
        self.assertEqual(farmer_res.status_code, 200)
        farmer_data = farmer_res.json()
        self.assertEqual(farmer_data["user"]["role"], "farmer")
        farmer_id = farmer_data["user"]["id"]

        # Farmer summary and herd
        farm_sum = requests.get(f"{BASE}/api/farmer/farm-summary?user_id={farmer_id}")
        self.assertEqual(farm_sum.status_code, 200)
        farm_animals = requests.get(f"{BASE}/api/farmer/animals?user_id={farmer_id}")
        self.assertEqual(farm_animals.status_code, 200)
        self.assertGreater(len(farm_animals.json()["animals"]), 0)

    def test_02_feed_quality_scanner(self):
        with open("data/sample_images/sample_healthy_feed.jpg", "rb") as img:
            scan_res = requests.post(
                f"{BASE}/api/scan",
                files={"file": ("healthy.jpg", img, "image/jpeg")},
                data={
                    "sample_type": "Cattle Feed Pellet",
                    "crude_protein": 20.0,
                    "moisture": 10.0,
                    "fiber": 8.0,
                    "storage_condition": "Shed",
                    "language": "te",
                    "user_id": 2
                }
            )
        self.assertEqual(scan_res.status_code, 200)
        data = scan_res.json()
        self.assertIn("batch_id", data)
        self.assertGreater(data["health_score"], 70)
        self.assertIn("animal_recommendation", data)
        self.assertEqual(data["animal_recommendation"]["suitability_code"], "SUITABLE")

    def test_03_adulteration_and_urea_calculator(self):
        # Standalone adulteration
        payload = {
            "sample_type": "Compound Cattle Feed",
            "crude_protein": 20.0,
            "moisture": 10.0,
            "fiber": 10.0,
            "non_protein_nitrogen": 0.5,
            "visual_powder_particles": 0.0
        }
        res = requests.post(f"{BASE}/api/check-adulteration", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["result"]["adulteration_risk"], "Low")

        # Safe urea dosage calculator
        calc_payload = {
            "mode": "concentrate_mix",
            "cattle_type": "Adult Cow",
            "daily_concentrate_kg": 4.0,
            "language": "te"
        }
        calc_res = requests.post(f"{BASE}/api/safe-urea-calculator", json=calc_payload)
        self.assertEqual(calc_res.status_code, 200)
        calc_data = calc_res.json()
        self.assertIn("safe_urea_kg", calc_data["data"])
        self.assertGreater(calc_data["data"]["safe_urea_kg"], 0)

    def test_04_multilingual_advisory_and_tts(self):
        adv_payload = {
            "sample_type": "Cattle Feed Pellet",
            "health_score": 85,
            "overall_risk": "Low",
            "crude_protein": 20.0,
            "moisture": 10.0,
            "fiber": 8.0,
            "storage_condition": "Shed",
            "language": "te"
        }
        res = requests.post(f"{BASE}/api/advisory", json=adv_payload)
        self.assertEqual(res.status_code, 200)
        self.assertIn("full_advisory_text", res.json())

        # TTS returns audio/mpeg binary stream
        tts_res = requests.post(f"{BASE}/api/tts", json={"text": "మేత నాణ్యత బాగుంది.", "language": "te"})
        self.assertEqual(tts_res.status_code, 200)
        self.assertIn("audio", tts_res.headers.get("content-type", ""))
        self.assertGreater(len(tts_res.content), 100)

    def test_05_animal_feed_recommendation(self):
        rec_payload = {
            "feed_diagnostics": {
                "sample_type": "Cattle Feed Pellet",
                "health_score": 88,
                "overall_risk": "Low",
                "mould_risk": "Low",
                "adulteration_risk": "Low",
                "crude_protein": 20.0,
                "moisture": 10.0
            },
            "animal_params": {
                "animal_type": "Cow",
                "lactation_stage": "Lactating",
                "milk_yield_litres": 8.0,
                "body_weight_kg": 400.0
            },
            "language": "te"
        }
        res = requests.post(f"{BASE}/api/animal-recommendation", json=rec_payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["is_safe"])
        self.assertEqual(data["suitability_code"], "SUITABLE")
        self.assertGreater(data["recommended_feed_kg"], 4.0)

    def test_06_time_based_smart_feeding_diary(self):
        # 1. GET today's plan
        today_res = requests.get(f"{BASE}/api/feed-diary/today?user_id=2&language=te")
        self.assertEqual(today_res.status_code, 200)
        today_data = today_res.json()
        self.assertEqual(len(today_data["plan"]["slots"]), 3)
        self.assertIn("active_slot", today_data["plan"])
        self.assertIn("next_reminder_slot", today_data["plan"])

        # 2. POST morning slot
        morn_res = requests.post(f"{BASE}/api/feed-diary/log", json={
            "user_id": 2,
            "feeding_date": "2026-09-08",
            "time_slot": "morning",
            "concentrate_kg": 2.2,
            "green_fodder_kg": 11.0,
            "milk_yield_litres": 5.0
        })
        self.assertEqual(morn_res.status_code, 200)
        self.assertEqual(morn_res.json()["next_reminder"]["next_slot"], "afternoon")

        # 3. GET insights
        ins_res = requests.get(f"{BASE}/api/feed-diary/insights?user_id=2&language=te")
        self.assertEqual(ins_res.status_code, 200)
        ins_data = ins_res.json()
        self.assertTrue(ins_data["insights"]["has_data"])

    def test_07_passport_and_qr(self):
        # Fetch passport for demo batch
        res = requests.get(f"{BASE}/api/passport/SFA-2026-000001")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("passport", data)
        self.assertIn("qr_base64", data)

    def test_08_dashboard_analytics_and_spoilage(self):
        res = requests.get(f"{BASE}/api/dashboard?user_id=2")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("metrics", data)
        self.assertIn("recent_tests", data)
        self.assertIn("spoilage_warning", data)


if __name__ == "__main__":
    unittest.main()