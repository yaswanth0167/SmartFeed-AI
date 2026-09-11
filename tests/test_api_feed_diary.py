"""
SmartFeed AI - API Integration Tests for Feed Diary Endpoints
"""
import unittest
from fastapi.testclient import TestClient
from server import app
from db.database import register_user, get_db, save_farm_onboarding, wipe_all_except_admin


class TestApiFeedDiary(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        wipe_all_except_admin()

    def setUp(self):
        self.client = TestClient(app)
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE mobile = ?", ("8888800001",))
            row = cursor.fetchone()
            if row:
                self.user_id = row["id"]
            else:
                reg = register_user("Diary Farmer", "8888800001", "pass123", role="farmer")
                self.user_id = reg["id"]

        farm_data = {
            "farmer_name": "Diary Test Dairy",
            "village_location": "Anandapuram",
            "preferred_language": "te",
            "total_animals": 2,
            "animal_types": "Cow,Buffalo",
            "main_feed_type": "Green Fodder",
            "feed_storage": "Shed"
        }
        animals_data = [
            {"species": "Cow", "tag_number": "DIARY-COW-1", "lactation_stage": "Lactating", "daily_milk_litres": 9.0},
            {"species": "Buffalo", "tag_number": "DIARY-BUFF-1", "lactation_stage": "Lactating", "daily_milk_litres": 11.0}
        ]
        save_farm_onboarding(self.user_id, farm_data, animals_data)

    def test_get_feed_diary_today(self):
        res = self.client.get(f"/api/feed-diary/today?user_id={self.user_id}&language=te")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("plan", data)
        self.assertEqual(len(data["plan"]["slots"]), 3)
        self.assertIn("daily_totals", data)
        self.assertEqual(data["daily_totals"]["slots_total_count"], 3)

    def test_post_feed_diary_log_and_progression(self):
        payload = {
            "user_id": self.user_id,
            "feeding_date": "2026-09-08",
            "time_slot": "morning",
            "feed_name": "Super Pellet + Napier Grass",
            "concentrate_kg": 2.2,
            "green_fodder_kg": 11.0,
            "dry_straw_kg": 0.0,
            "milk_yield_litres": 5.0,
            "notes": "Good appetite"
        }
        log_res = self.client.post("/api/feed-diary/log", json=payload)
        self.assertEqual(log_res.status_code, 200)
        log_data = log_res.json()
        self.assertEqual(log_data["status"], "success")
        self.assertEqual(log_data["logged_slot"], "morning")
        self.assertEqual(log_data["next_reminder"]["next_slot"], "afternoon")

        today_res = self.client.get(f"/api/feed-diary/today?user_id={self.user_id}&date=2026-09-08")
        self.assertEqual(today_res.status_code, 200)
        today_data = today_res.json()
        morn_slot = today_data["plan"]["slots"][0]
        self.assertTrue(morn_slot["logged"])
        self.assertIn("Logged", morn_slot["status_badge"])
        self.assertEqual(today_data["daily_totals"]["slots_logged_count"], 1)

    def test_feed_diary_insights(self):
        self.client.post("/api/feed-diary/log", json={
            "user_id": self.user_id,
            "feeding_date": "2026-09-08",
            "time_slot": "evening",
            "concentrate_kg": 2.2,
            "green_fodder_kg": 11.0,
            "dry_straw_kg": 0.0,
            "milk_yield_litres": 4.5
        })
        res = self.client.get(f"/api/feed-diary/insights?user_id={self.user_id}&language=te")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("insights", data)
        self.assertTrue(data["insights"]["has_data"])


if __name__ == "__main__":
    unittest.main()