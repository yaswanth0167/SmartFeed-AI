"""
SmartFeed AI - Step 8 End-to-End Pipeline Integration Test
Validates the entire 17-step SIH demo flow:
SCAN -> ANALYZE -> RISK ASSESSMENT -> HEALTH SCORE -> EXPLAIN RESULT ->
ADVISORY -> SAVE -> QR -> PASSPORT -> DASHBOARD TREND
"""

import sys
import unittest
from pathlib import Path
from PIL import Image

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from db.database import initialize_database, create_test, delete_test
from utils.inference import predict_feed_quality
from utils.adulteration import check_adulteration_risk
from utils.nutrition import analyze_nutrition
from utils.risk_engine import evaluate_smartfeed_risks
from utils.advisory import generate_advisory
from utils.qr_utils import generate_feed_passport_qr, decode_qr_image, get_digital_feed_passport
from utils.analytics import compute_dashboard_metrics, detect_early_spoilage_warning


class TestEndToEndPipeline(unittest.TestCase):
    def setUp(self):
        initialize_database()
        self.sample_img_path = PROJECT_ROOT / "data" / "sample_images" / "sample_mouldy_feed.jpg"
        self.created_batch_id = None

    def tearDown(self):
        if self.created_batch_id:
            delete_test(self.created_batch_id)

    def test_full_demo_workflow(self):
        """Executes the complete 17-step SIH demo flow without errors."""
        self.assertTrue(self.sample_img_path.exists(), "Demo sample image must exist")

        # 1 & 2: Load sample & run computer vision inference
        visual_res = predict_feed_quality(self.sample_img_path, sample_type="Compound Cattle Feed")
        self.assertEqual(visual_res["mould_risk"], "High")
        self.assertIn("moldy", visual_res["predicted_class"])

        # 3: Adulteration risk check
        adulteration_res = check_adulteration_risk(
            feed_type="Compound Cattle Feed",
            color_desc="White Patches",
            texture_desc="Fine",
            smell_desc="Fungal",
            storage_condition="Damp & Humid Shed",
            foreign_particles="Low",
            crude_protein=19.0,
            moisture=16.5,
            fiber=11.0
        )
        self.assertIn(adulteration_res["adulteration_risk"], ["Medium", "High"])

        # 4: Nutrition evaluation
        nutrition_res = analyze_nutrition(
            sample_type="Compound Cattle Feed",
            crude_protein=19.0,
            moisture=16.5,
            fiber=11.0
        )
        self.assertIn("Excessive", nutrition_res["parameter_status"]["moisture"])

        # 5: Multi-Factor Risk Intelligence Engine & Health Score
        risk_res = evaluate_smartfeed_risks(
            visual_res=visual_res,
            adulteration_res=adulteration_res,
            nutrition_res=nutrition_res,
            storage_condition="Damp & Humid Shed"
        )
        self.assertLess(risk_res["health_score"], 70.0)
        self.assertEqual(risk_res["overall_risk"], "High")
        self.assertIn("Fungal & Mould", risk_res["primary_concern"])

        # 6: "Why This Result?" Explainable AI check
        why = risk_res["why_this_result"]
        self.assertTrue(len(why["concerns_list"]) >= 1)
        self.assertTrue(len(why["deductions_list"]) >= 1)

        # 7: Multilingual Advisory in Telugu
        advisory_payload = {
            "sample_type": "Compound Cattle Feed",
            "health_score": risk_res["health_score"],
            "overall_risk": risk_res["overall_risk"],
            "farmer_label": visual_res["farmer_label"],
            "mould_risk": visual_res["mould_risk"],
            "foreign_particle_risk": visual_res["foreign_particle_risk"],
            "adulteration_risk": adulteration_res["adulteration_risk"],
            "crude_protein": 19.0,
            "moisture": 16.5,
            "fiber": 11.0,
            "storage_condition": "Damp Shed",
            "primary_concern": risk_res["primary_concern"],
            "recommended_action": risk_res["recommended_action"],
            "protein_status": "Optimal",
            "flagged_hazards": []
        }
        adv_te = generate_advisory(advisory_payload, language="te", provider="offline")
        self.assertIn("ఫంగస్", adv_te["full_advisory_text"])

        # 8: Save test to SQLite
        self.created_batch_id = "SFA-2026-DEMO01"
        create_test({
            "batch_id": self.created_batch_id,
            "sample_type": "Compound Cattle Feed",
            "image_path": str(self.sample_img_path),
            "visual_prediction": visual_res["farmer_label"],
            "confidence": visual_res["confidence"],
            "quality_score": risk_res["health_score"],
            "mould_risk": visual_res["mould_risk"],
            "foreign_particle_risk": visual_res["foreign_particle_risk"],
            "adulteration_risk": adulteration_res["adulteration_risk"],
            "nutrition_status": nutrition_res["nutrition_status"],
            "crude_protein": 19.0,
            "moisture": 16.5,
            "fiber": 11.0,
            "storage_condition": "Damp Shed",
            "overall_risk": risk_res["overall_risk"],
            "primary_concern": risk_res["primary_concern"],
            "advisory": adv_te["full_advisory_text"],
            "language": "te"
        })

        # 9: Generate QR code passport
        qr_file = generate_feed_passport_qr(self.created_batch_id)
        self.assertTrue(Path(qr_file).exists())

        # 10: Decode QR image
        decoded_batch = decode_qr_image(qr_file)
        self.assertEqual(decoded_batch, self.created_batch_id)

        # 11: Fetch full digital passport
        passport = get_digital_feed_passport(decoded_batch)
        self.assertIsNotNone(passport)
        self.assertEqual(passport["batch_id"], self.created_batch_id)
        self.assertIn("ఫంగస్", passport["advisory"])

        # 12: Trend and Early Spoilage warning
        trend_sample = [
            {"quality_score": 85.0, "moisture": 10.0, "mould_risk": "Low"},
            {"quality_score": 75.0, "moisture": 12.0, "mould_risk": "Low"},
            {"quality_score": risk_res["health_score"], "moisture": 16.5, "mould_risk": "High"}
        ]
        spoilage = detect_early_spoilage_warning(trend_sample)
        self.assertTrue(spoilage["has_warning"])
        self.assertIn("Potential Spoilage Risk", spoilage["disclaimer"])


if __name__ == "__main__":
    unittest.main()
