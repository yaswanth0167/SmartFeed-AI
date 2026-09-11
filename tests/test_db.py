"""
SmartFeed AI - Database Tests
Validates database initialization, schema integrity, and CRUD operations.
"""

import os
import sys
import unittest
import tempfile
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from db.database import (
    initialize_database,
    create_test,
    get_test_by_batch,
    get_all_tests,
    get_recent_tests,
    get_quality_trend,
    delete_test,
    generate_batch_id,
    get_db,
)


class TestSmartFeedDatabase(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file for isolated testing
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.temp_db_fd)
        initialize_database(self.temp_db_path)

    def tearDown(self):
        # Clean up temporary database file
        if os.path.exists(self.temp_db_path):
            try:
                os.remove(self.temp_db_path)
            except PermissionError:
                pass

    def test_initialize_database(self):
        """Verify table exists and columns match the specification."""
        with get_db(self.temp_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(tests);")
            columns = {row["name"]: row["type"] for row in cursor.fetchall()}

        expected_columns = [
            "id", "batch_id", "sample_type", "image_path", "visual_prediction",
            "confidence", "quality_score", "mould_risk", "foreign_particle_risk",
            "adulteration_risk", "nutrition_status", "crude_protein", "moisture",
            "fiber", "storage_condition", "overall_risk", "primary_concern",
            "advisory", "language", "timestamp"
        ]
        for col in expected_columns:
            self.assertIn(col, columns, f"Column '{col}' missing from schema")

    def test_generate_batch_id_sequential(self):
        """Verify Batch IDs format and sequential progression."""
        batch_id_1 = generate_batch_id(self.temp_db_path)
        self.assertTrue(batch_id_1.startswith("SFA-"))
        self.assertTrue(batch_id_1.endswith("000001"))

        # Insert one record
        create_test({
            "batch_id": batch_id_1,
            "sample_type": "Silage",
            "quality_score": 85.0
        }, db_path=self.temp_db_path)

        batch_id_2 = generate_batch_id(self.temp_db_path)
        self.assertTrue(batch_id_2.endswith("000002"))

    def test_create_and_get_test(self):
        """Verify inserting a complete test record and retrieving it."""
        sample_data = {
            "batch_id": "SFA-2026-000100",
            "sample_type": "Compound Cattle Feed",
            "image_path": "uploads/sample_01.jpg",
            "visual_prediction": "Good Quality",
            "confidence": 0.94,
            "quality_score": 88.5,
            "mould_risk": "Low",
            "foreign_particle_risk": "Low",
            "adulteration_risk": "Low",
            "nutrition_status": "Balanced",
            "crude_protein": 18.5,
            "moisture": 11.2,
            "fiber": 12.0,
            "storage_condition": "Well-Ventilated Dry Area",
            "overall_risk": "Low",
            "primary_concern": "None",
            "advisory": "Feed is safe for livestock consumption.",
            "language": "en",
            "timestamp": "2026-09-05T10:00:00"
        }

        created_id = create_test(sample_data, db_path=self.temp_db_path)
        self.assertEqual(created_id, "SFA-2026-000100")

        fetched = get_test_by_batch("SFA-2026-000100", db_path=self.temp_db_path)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["batch_id"], "SFA-2026-000100")
        self.assertEqual(fetched["quality_score"], 88.5)
        self.assertEqual(fetched["overall_risk"], "Low")
        self.assertEqual(fetched["sample_type"], "Compound Cattle Feed")

    def test_duplicate_batch_id_raises_value_error(self):
        """Verify uniqueness enforcement on batch_id."""
        sample_data = {
            "batch_id": "SFA-2026-UNIQUE-1",
            "sample_type": "Feed Ingredient",
            "quality_score": 75.0
        }
        create_test(sample_data, db_path=self.temp_db_path)

        with self.assertRaises(ValueError):
            create_test(sample_data, db_path=self.temp_db_path)

    def test_quality_trend_and_recent_tests(self):
        """Verify historical trend ordering and recent tests limiting."""
        # Insert 3 tests with varying dates
        test_records = [
            {"batch_id": "SFA-001", "sample_type": "Silage", "quality_score": 88.0, "timestamp": "2026-09-01T10:00:00"},
            {"batch_id": "SFA-002", "sample_type": "Silage", "quality_score": 70.0, "timestamp": "2026-09-03T10:00:00"},
            {"batch_id": "SFA-003", "sample_type": "Feed Ingredient", "quality_score": 92.0, "timestamp": "2026-09-05T10:00:00"},
        ]
        for rec in test_records:
            create_test(rec, db_path=self.temp_db_path)

        # All tests
        all_tests = get_all_tests(db_path=self.temp_db_path)
        self.assertEqual(len(all_tests), 3)

        # Recent tests (limit 2)
        recent = get_recent_tests(limit=2, db_path=self.temp_db_path)
        self.assertEqual(len(recent), 2)
        # Should be ordered descending by id
        self.assertEqual(recent[0]["batch_id"], "SFA-003")

        # Trend for Silage only
        silage_trend = get_quality_trend(sample_type="Silage", db_path=self.temp_db_path)
        self.assertEqual(len(silage_trend), 2)
        self.assertEqual(silage_trend[0]["batch_id"], "SFA-001")
        self.assertEqual(silage_trend[1]["batch_id"], "SFA-002")

    def test_delete_test(self):
        """Verify record deletion."""
        create_test({"batch_id": "SFA-TO-DELETE", "sample_type": "Silage", "quality_score": 50.0}, db_path=self.temp_db_path)
        self.assertIsNotNone(get_test_by_batch("SFA-TO-DELETE", db_path=self.temp_db_path))

        deleted = delete_test("SFA-TO-DELETE", db_path=self.temp_db_path)
        self.assertTrue(deleted)
        self.assertIsNone(get_test_by_batch("SFA-TO-DELETE", db_path=self.temp_db_path))

        # Deleting non-existent returns False
        self.assertFalse(delete_test("NON-EXISTENT", db_path=self.temp_db_path))


if __name__ == "__main__":
    unittest.main()
