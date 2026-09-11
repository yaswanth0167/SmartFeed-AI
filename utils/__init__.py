"""
SmartFeed AI Utilities Package
"""

from utils.cv_analysis import analyze_feed_image, load_image_to_cv
from utils.inference import predict_feed_quality
from utils.nutrition import analyze_nutrition, load_reference_ranges
from utils.adulteration import check_adulteration_risk, AdulterationEngine
from utils.risk_engine import evaluate_smartfeed_risks, RiskIntelligenceEngine
from utils.advisory import generate_advisory, generate_offline_advisory
from utils.qr_utils import generate_feed_passport_qr, decode_qr_image, get_digital_feed_passport
from utils.analytics import (
    compute_dashboard_metrics,
    detect_early_spoilage_warning,
    create_quality_trend_chart,
    create_risk_distribution_chart,
    create_sample_type_pie
)

__all__ = [
    "analyze_feed_image",
    "load_image_to_cv",
    "predict_feed_quality",
    "analyze_nutrition",
    "load_reference_ranges",
    "check_adulteration_risk",
    "AdulterationEngine",
    "evaluate_smartfeed_risks",
    "RiskIntelligenceEngine",
    "generate_advisory",
    "generate_offline_advisory",
    "generate_feed_passport_qr",
    "decode_qr_image",
    "get_digital_feed_passport",
    "compute_dashboard_metrics",
    "detect_early_spoilage_warning",
    "create_quality_trend_chart",
    "create_risk_distribution_chart",
    "create_sample_type_pie",
]
