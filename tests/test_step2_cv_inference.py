"""
SmartFeed AI - Step 2 CV & Inference Unit Tests
Validates OpenCV image processing, color thresholding, texture metrics,
foreign particle detection, and heuristic inference pipeline.
"""

import sys
import unittest
import numpy as np
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.cv_analysis import analyze_feed_image
from utils.inference import predict_feed_quality


class TestCVAndInference(unittest.TestCase):
    def setUp(self):
        # 1. Clean synthetic feed image (uniform golden/yellow hue)
        self.clean_feed = np.full((300, 300, 3), (30, 160, 210), dtype=np.uint8)

        # 2. Mouldy synthetic image (golden background + bright white/pale patches)
        self.mouldy_feed = self.clean_feed.copy()
        # Add white/grey fungal patch in center
        self.mouldy_feed[100:200, 100:200] = (240, 240, 240)

        # 3. Burnt synthetic image (golden background + large dark patches)
        self.burnt_feed = self.clean_feed.copy()
        self.burnt_feed[50:220, 50:220] = (15, 15, 20)

        # 4. Foreign particle synthetic image (stark dark speckles)
        self.speckled_feed = self.clean_feed.copy()
        for x in range(30, 280, 25):
            for y in range(30, 280, 25):
                self.speckled_feed[y:y+8, x:x+8] = (0, 0, 0)

    def test_clean_feed_analysis(self):
        """Clean feed should have high visual quality score and low risks."""
        res = analyze_feed_image(self.clean_feed)
        self.assertIn("color_analysis", res)
        self.assertIn("texture_analysis", res)
        self.assertIn("foreign_particle_risk", res)

        self.assertGreaterEqual(res["visual_quality_score"], 80.0)
        self.assertEqual(res["cv_mould_indicator"], "Low")
        self.assertEqual(res["foreign_particle_risk"]["risk_level"], "Low")

    def test_mouldy_feed_detection(self):
        """Feed with white/grey patches should trigger mould warning."""
        res = analyze_feed_image(self.mouldy_feed)
        self.assertGreater(res["color_analysis"]["white_grey_patch_pct"], 8.0)
        self.assertEqual(res["cv_mould_indicator"], "High")

        # Test inference integration
        pred = predict_feed_quality(self.mouldy_feed, sample_type="Feed Ingredient")
        self.assertEqual(pred["predicted_class"], "moldy")
        self.assertEqual(pred["mould_risk"], "High")
        self.assertEqual(pred["farmer_label"], "High Mould/Fungal Risk")

    def test_burnt_feed_detection(self):
        """Feed with dark regions should detect dark patches and burnt/scorched defect."""
        res = analyze_feed_image(self.burnt_feed)
        self.assertGreater(res["color_analysis"]["dark_patch_pct"], 10.0)

        pred = predict_feed_quality(self.burnt_feed, sample_type="Feed Ingredient")
        self.assertIn(pred["predicted_class"], ["burnt", "scorched"])

    def test_foreign_particle_detection(self):
        """Feed with multiple distinct speckles should flag particle risk."""
        res = analyze_feed_image(self.speckled_feed)
        self.assertGreater(res["foreign_particle_risk"]["particle_count"], 5)
        self.assertIn(res["foreign_particle_risk"]["risk_level"], ["Medium", "High"])

    def test_silage_inference(self):
        """Silage samples should map to fresh or spoiled classes."""
        fresh_pred = predict_feed_quality(self.clean_feed, sample_type="Silage")
        self.assertEqual(fresh_pred["predicted_class"], "fresh")
        self.assertEqual(fresh_pred["farmer_label"], "Fresh / Well-Preserved Silage")

        spoiled_pred = predict_feed_quality(self.mouldy_feed, sample_type="Silage")
        self.assertEqual(spoiled_pred["predicted_class"], "spoiled")
        self.assertEqual(spoiled_pred["farmer_label"], "Spoiled / High Fungal Risk Silage")


if __name__ == "__main__":
    unittest.main()
