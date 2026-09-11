"""
SmartFeed AI - Step 5 Unit Tests: User Authentication, Role Management & Farm Onboarding
"""

import sys
import unittest
import tempfile
import os
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from db.database import (
    initialize_database,
    register_user,
    authenticate_user,
    get_user_by_id,
    save_farm_onboarding,
    get_farmer_profile,
    get_farmer_animals,
    get_all_farmers_admin_summary,
    get_admin_kpis,
    create_test,
    get_all_tests
)


class TestAuthAndFarmOnboarding(unittest.TestCase):
    def setUp(self):
        """Create a temporary SQLite database for clean test isolation."""
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        initialize_database(self.temp_db_path)

    def tearDown(self):
        """Clean up temporary database file."""
        os.close(self.temp_db_fd)
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def test_default_seed_accounts(self):
        """Verify Admin and Demo Farmer accounts are seeded automatically."""
        admin = authenticate_user("8341016049", "6049", db_path=self.temp_db_path)
        self.assertIsNotNone(admin)
        self.assertEqual(admin["role"], "admin")
        self.assertNotIn("password_hash", admin)

        farmer = authenticate_user("9876543210", "farmer123", db_path=self.temp_db_path)
        self.assertIsNotNone(farmer)
        self.assertEqual(farmer["role"], "farmer")
        self.assertEqual(farmer["is_onboarded"], 1)

    def test_register_new_farmer(self):
        """Verify farmer registration with full details."""
        user = register_user(
            full_name="Suresh Reddy",
            mobile="9123456780",
            password="secretpassword",
            email="suresh@guntur.in",
            language="te",
            role="farmer",
            db_path=self.temp_db_path
        )
        self.assertEqual(user["full_name"], "Suresh Reddy")
        self.assertEqual(user["mobile"], "9123456780")
        self.assertEqual(user["preferred_language"], "te")
        self.assertEqual(user["is_onboarded"], 0)

        # Duplicate registration should raise ValueError
        with self.assertRaises(ValueError):
            register_user(
                full_name="Suresh Copy",
                mobile="9123456780",
                password="anotherpassword",
                db_path=self.temp_db_path
            )

    def test_authentication(self):
        """Verify login credentials check."""
        register_user(
            full_name="Anitha Devi",
            mobile="9848012345",
            password="dairyfarm2026",
            language="te",
            db_path=self.temp_db_path
        )
        # Correct password
        user = authenticate_user("9848012345", "dairyfarm2026", db_path=self.temp_db_path)
        self.assertIsNotNone(user)
        self.assertEqual(user["mobile"], "9848012345")

        # Incorrect password
        wrong = authenticate_user("9848012345", "wrongpass", db_path=self.temp_db_path)
        self.assertIsNone(wrong)

    def test_4step_farm_onboarding_with_conditional_milk(self):
        """
        Verify the 4-step onboarding flow:
        Step 1: Farm Basic Details
        Step 2: Number of Animals (3)
        Step 3: Animal Profiles with conditional milk production
        Step 4: Feed & Storage Details
        Step 5: Farmer Dashboard breakdown
        """
        user = register_user(
            full_name="Venkatesh Rao",
            mobile="9955112233",
            password="pass1234",
            language="te",
            db_path=self.temp_db_path
        )
        user_id = user["id"]

        farm_data = {
            "farmer_name": "Venkatesh Rao",
            "village_location": "Tenali (తెనాలి)",
            "preferred_language": "te",
            "total_animals": 3,
            "animal_types": "Cow,Buffalo",
            "main_feed_type": "Silage",
            "feed_storage": "Shed"
        }

        # 3 animals as requested by user prompt:
        # Animal 1: Cow, 3-5 yrs, Lactating, Medium
        # Animal 2: Cow, 5+ yrs, Pregnant (Milk should become N/A)
        # Animal 3: Buffalo, 3-5 yrs, Lactating, High
        animals_data = [
            {
                "animal_name": "Gauri",
                "animal_type": "Cow",
                "age_group": "3–5 years",
                "lactation_status": "Lactating",
                "milk_production": "Medium (5–10 L)"
            },
            {
                "animal_name": "Lakshmi",
                "animal_type": "Cow",
                "age_group": "5+ years",
                "lactation_status": "Pregnant",
                "milk_production": "High (>10 L)"
            },
            {
                "animal_name": "Kaali",
                "animal_type": "Buffalo",
                "age_group": "3–5 years",
                "lactation_status": "Lactating",
                "milk_production": "High (>10 L)"
            }
        ]

        profile = save_farm_onboarding(user_id, farm_data, animals_data, db_path=self.temp_db_path)
        self.assertIsNotNone(profile)
        self.assertEqual(profile["user"]["is_onboarded"], 1)

        # Check breakdown for Step 5 Farmer Dashboard
        summary = profile["summary"]
        self.assertEqual(summary["total_animals"], 3)
        self.assertEqual(summary["cows"], 2)
        self.assertEqual(summary["buffaloes"], 1)
        self.assertEqual(summary["lactating"], 2)
        self.assertEqual(summary["pregnant"], 1)

        # Verify Conditional Rule: Animal 2 (Pregnant) MUST have milk_production == 'N/A'
        animals = profile["animals"]
        self.assertEqual(animals[0]["milk_production"], "Medium (5–10 L)")
        self.assertEqual(animals[1]["milk_production"], "N/A")
        self.assertEqual(animals[2]["milk_production"], "High (>10 L)")

    def test_farmer_data_isolation(self):
        """Ensure farmer sees only his tests, and admin sees all."""
        # Create test for demo farmer (id 2)
        create_test({
            "batch_id": "SFA-TEST-001",
            "user_id": 2,
            "sample_type": "Silage",
            "quality_score": 85.0
        }, db_path=self.temp_db_path)

        # Create test for another farmer (id 99)
        create_test({
            "batch_id": "SFA-TEST-002",
            "user_id": 99,
            "sample_type": "Pellet",
            "quality_score": 75.0
        }, db_path=self.temp_db_path)

        farmer_tests = get_all_tests(user_id=2, db_path=self.temp_db_path)
        self.assertEqual(len(farmer_tests), 1)
        self.assertEqual(farmer_tests[0]["batch_id"], "SFA-TEST-001")

        all_tests = get_all_tests(user_id=None, db_path=self.temp_db_path)
        self.assertGreaterEqual(len(all_tests), 2)


if __name__ == "__main__":
    unittest.main()
