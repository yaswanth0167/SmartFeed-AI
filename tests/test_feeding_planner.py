"""
SmartFeed AI - Unit Tests for Feeding Planner & Intelligence Engine
"""
import unittest
from utils.feeding_planner import get_daily_time_slots_plan, generate_feeding_insights


class TestFeedingPlanner(unittest.TestCase):

    def test_daily_time_slots_plan_lactating_cow(self):
        profile = {
            "animal_type": "Cow",
            "lactation_status": "Lactating",
            "milk_production": 8.0,
            "animal_name": "Gauri (Cow #1)"
        }
        plan = get_daily_time_slots_plan(animal_profile=profile, current_hour=7, language="te")
        self.assertEqual(plan["status"], "success")
        self.assertEqual(plan["animal_type"], "Cow")
        self.assertEqual(plan["lactation_status"], "Lactating")
        self.assertEqual(plan["active_slot"], "morning")
        self.assertEqual(plan["next_reminder_slot"], "afternoon")
        self.assertIn("01:00 PM", plan["next_reminder_time"])

        slots = plan["slots"]
        self.assertEqual(len(slots), 3)
        self.assertEqual(slots[0]["slot_key"], "morning")
        self.assertEqual(slots[1]["slot_key"], "afternoon")
        self.assertEqual(slots[2]["slot_key"], "evening")

        morn = slots[0]["suggested"]
        self.assertGreater(morn["concentrate_kg"], 0)
        self.assertGreater(morn["green_fodder_kg"], 0)
        self.assertEqual(morn["dry_straw_kg"], 0)

        aft = slots[1]["suggested"]
        self.assertEqual(aft["concentrate_kg"], 0)
        self.assertGreater(aft["dry_straw_kg"], 0)

        eve = slots[2]["suggested"]
        self.assertGreater(eve["concentrate_kg"], 0)
        self.assertGreater(eve["minerals_grams"], 0)

    def test_time_slot_hour_progression(self):
        profile = {"animal_type": "Cow", "lactation_status": "Lactating", "milk_production": 10.0}
        plan_aft = get_daily_time_slots_plan(profile, current_hour=13)
        self.assertEqual(plan_aft["active_slot"], "afternoon")
        self.assertEqual(plan_aft["next_reminder_slot"], "evening")
        self.assertEqual(plan_aft["next_reminder_time"], "06:00 PM")

        plan_eve = get_daily_time_slots_plan(profile, current_hour=19)
        self.assertEqual(plan_eve["active_slot"], "evening")
        self.assertEqual(plan_eve["next_reminder_slot"], "morning")
        self.assertIn("06:30 AM", plan_eve["next_reminder_time"])

    def test_buffalo_pregnant_ration_scaling(self):
        profile = {
            "animal_type": "Buffalo",
            "lactation_status": "Pregnant",
            "milk_production": 0.0
        }
        plan = get_daily_time_slots_plan(profile, current_hour=8)
        self.assertEqual(plan["animal_type"], "Buffalo")
        self.assertEqual(plan["lactation_status"], "Pregnant")
        targets = plan["daily_targets"]
        self.assertGreaterEqual(targets["total_concentrate_kg"], 3.0)
        self.assertEqual(targets["mineral_mix_grams"], 100)

    def test_generate_feeding_insights_empty(self):
        res = generate_feeding_insights([])
        self.assertFalse(res["has_data"])
        self.assertIn("headline", res)
        self.assertIn("te", res["headline"])

    def test_generate_feeding_insights_with_data(self):
        history = [
            {"feeding_date": "2026-09-05", "time_slot": "morning", "concentrate_kg": 2.0, "green_fodder_kg": 10.0, "dry_straw_kg": 0.0, "milk_yield_litres": 4.5},
            {"feeding_date": "2026-09-05", "time_slot": "afternoon", "concentrate_kg": 0.0, "green_fodder_kg": 0.0, "dry_straw_kg": 4.0, "milk_yield_litres": 0.0},
            {"feeding_date": "2026-09-05", "time_slot": "evening", "concentrate_kg": 2.0, "green_fodder_kg": 10.0, "dry_straw_kg": 0.0, "milk_yield_litres": 4.0},
            {"feeding_date": "2026-09-06", "time_slot": "morning", "concentrate_kg": 2.5, "green_fodder_kg": 12.0, "dry_straw_kg": 0.0, "milk_yield_litres": 5.5},
            {"feeding_date": "2026-09-06", "time_slot": "afternoon", "concentrate_kg": 0.0, "green_fodder_kg": 0.0, "dry_straw_kg": 4.0, "milk_yield_litres": 0.0},
            {"feeding_date": "2026-09-06", "time_slot": "evening", "concentrate_kg": 2.5, "green_fodder_kg": 12.0, "dry_straw_kg": 0.0, "milk_yield_litres": 5.0}
        ]
        res = generate_feeding_insights(history, language="te")
        self.assertTrue(res["has_data"])
        self.assertEqual(res["total_days_logged"], 2)
        self.assertGreater(res["peak_milk_litres"], 8.0)
        self.assertIn("headline", res)
        self.assertIn("te", res["headline"])
        self.assertIn("insight_text", res)
        self.assertGreaterEqual(len(res["recommendation_tips"]), 3)


if __name__ == "__main__":
    unittest.main()