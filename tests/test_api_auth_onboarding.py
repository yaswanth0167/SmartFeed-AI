"""
Unit tests for Auth, 4-Step Onboarding Wizard, and Role-Based APIs.
"""
import unittest
import time
from fastapi.testclient import TestClient
from server import app
from db.database import seed_demo_farmer, wipe_all_except_admin

class TestApiAuthOnboarding(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        seed_demo_farmer()

    @classmethod
    def tearDownClass(cls):
        wipe_all_except_admin()

    def setUp(self):
        self.client = TestClient(app)

    def test_seed_demo_farmer_login(self):
        """Seed demo farmer (9876543210 / farmer123) should login successfully."""
        res = self.client.post("/api/auth/login", json={
            "mobile": "9876543210",
            "password": "farmer123"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["user"]["role"], "farmer")
        self.assertEqual(data["user"]["is_onboarded"], 1)

    def test_seed_admin_login(self):
        """Seed admin (8341016049 / 6049) should login successfully."""
        res = self.client.post("/api/auth/login", json={
            "mobile": "8341016049",
            "password": "6049"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["user"]["role"], "admin")

    def test_admin_security_rejects_unauthorized(self):
        """Admin login must reject wrong passwords and empty credentials to prevent unauthorized access."""
        # Wrong password
        res_wrong = self.client.post("/api/auth/login", json={
            "mobile": "8341016049",
            "password": "wrongpassword123"
        })
        self.assertEqual(res_wrong.status_code, 401)
        self.assertIn("Invalid mobile number or password", res_wrong.json()["detail"])

        # Missing password
        res_empty = self.client.post("/api/auth/login", json={
            "mobile": "8341016049",
            "password": ""
        })
        self.assertEqual(res_empty.status_code, 400)

        # Unregistered number
        res_unreg = self.client.post("/api/auth/login", json={
            "mobile": "9999999999",
            "password": "somepassword"
        })
        self.assertEqual(res_unreg.status_code, 401)

    def test_farmer_summary_and_animals_api(self):
        """Farmer farm summary and animals directory return valid data."""
        # Get demo farmer id
        login_res = self.client.post("/api/auth/login", json={
            "mobile": "9876543210",
            "password": "farmer123"
        })
        user_id = login_res.json()["user"]["id"]

        summary_res = self.client.get(f"/api/farmer/farm-summary?user_id={user_id}")
        self.assertEqual(summary_res.status_code, 200)
        summary = summary_res.json()["profile"]
        self.assertIn("Ramesh Kumar", summary["farmer_name"])
        self.assertEqual(summary["total_animals"], 3)
        self.assertEqual(summary["cows_count"], 2)
        self.assertEqual(summary["buffaloes_count"], 1)

        animals_res = self.client.get(f"/api/farmer/animals?user_id={user_id}")
        self.assertEqual(animals_res.status_code, 200)
        animals = animals_res.json()["animals"]
        self.assertEqual(len(animals), 3)

    def test_admin_kpis_and_farmers_api(self):
        """Admin can fetch all farmers and cooperative KPIs."""
        farmers_res = self.client.get("/api/admin/farmers")
        self.assertEqual(farmers_res.status_code, 200)
        farmers = farmers_res.json()["farmers"]
        self.assertGreaterEqual(len(farmers), 1)

        kpis_res = self.client.get("/api/admin/kpis")
        self.assertEqual(kpis_res.status_code, 200)
        kpis = kpis_res.json()["kpis"]
        self.assertIn("total_farmers", kpis)
        self.assertIn("total_cattle", kpis)

    def test_new_farmer_registration_and_onboarding_pipeline(self):
        """New farmer registers -> is_onboarded is 0 -> completes 4-step wizard -> is_onboarded becomes 1."""
        test_mobile = f"91{int(time.time() * 1000) % 100000000:08d}"
        # Register
        reg_res = self.client.post("/api/auth/register", json={
            "full_name": "Suresh Reddy",
            "mobile": test_mobile,
            "email": "suresh@example.com",
            "password": "secretpassword",
            "preferred_language": "te"
        })
        self.assertEqual(reg_res.status_code, 200)
        new_user = reg_res.json()["user"]
        self.assertEqual(new_user["is_onboarded"], 0)
        user_id = new_user["id"]

        # Run 4-Step Onboarding Setup
        onboard_res = self.client.post("/api/onboarding/setup", json={
            "user_id": user_id,
            "farmer_name": "Suresh Reddy",
            "village_location": "Warangal Rural",
            "preferred_language": "te",
            "total_animals": 2,
            "animal_types": ["Cow", "Buffalo"],
            "main_feed_type": "Silage",
            "feed_storage": "Silage Pit",
            "animals": [
                {
                    "animal_name": "Lakshmi (Cow #1)",
                    "animal_type": "Cow",
                    "age_group": "3-5 yrs",
                    "lactation_status": "Lactating",
                    "milk_production": "High (>10 L)"
                },
                {
                    "animal_name": "Ganga (Buffalo #1)",
                    "animal_type": "Buffalo",
                    "age_group": "3-5 yrs",
                    "lactation_status": "Pregnant",
                    "milk_production": "N/A" # Conditional rule: Pregnant does not require milk production
                }
            ]
        })
        self.assertEqual(onboard_res.status_code, 200)
        resp_data = onboard_res.json()
        self.assertEqual(resp_data["status"], "success")
        self.assertEqual(resp_data["user"]["is_onboarded"], 1)
        self.assertEqual(resp_data["profile"]["total_animals"], 2)
        self.assertEqual(resp_data["profile"]["cows_count"], 1)
        self.assertEqual(resp_data["profile"]["buffaloes_count"], 1)
        self.assertEqual(resp_data["profile"]["pregnant_count"], 1)
        self.assertEqual(resp_data["profile"]["lactating_count"], 1)

if __name__ == "__main__":
    unittest.main()
