"""
SmartFeed AI - Model Inference Module
Handles visual defect classification for cattle feed ingredients and silage.
Supports trained MobileNetV2 Keras models with an intelligent OpenCV heuristic fallback
so the application remains fully functional if weights are not yet generated.
"""

import os
import json
from pathlib import Path
from typing import Union, Dict, Any
import numpy as np
from PIL import Image

from utils.cv_analysis import analyze_feed_image, load_image_to_cv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEED_MODEL_PATH = PROJECT_ROOT / "models" / "feed_quality_model.keras"
SILAGE_MODEL_PATH = PROJECT_ROOT / "models" / "silage_quality_model.keras"
FEED_LABELS_PATH = PROJECT_ROOT / "models" / "labels.json"
SILAGE_LABELS_PATH = PROJECT_ROOT / "models" / "silage_labels.json"

# In-memory cache for loaded models
_CACHED_MODELS: Dict[str, Any] = {}


def load_label_config(labels_path: Path) -> Dict[str, Any]:
    """Loads class definitions, farmer labels, and risk mappings from json."""
    if labels_path.exists():
        try:
            with open(labels_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def heuristic_feed_classifier(cv_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Intelligent heuristic classifier used when deep learning weights are not yet trained.
    Translates OpenCV color and texture findings into Mendeley grain defect classes.
    """
    color = cv_results["color_analysis"]
    particle = cv_results["foreign_particle_risk"]
    texture = cv_results["texture_analysis"]

    white_grey = color["white_grey_patch_pct"]
    dark = color["dark_patch_pct"]
    green = color["greenish_patch_pct"]
    particle_count = particle["particle_count"]

    if white_grey > 6.0:
        predicted_class = "moldy"
        confidence = min(0.96, 0.70 + (white_grey / 20.0))
        farmer_label = "High Mould/Fungal Risk"
        risk_level = "High"
    elif dark > 12.0:
        predicted_class = "burnt"
        confidence = min(0.94, 0.65 + (dark / 25.0))
        farmer_label = "Heat-Damaged / Quality Warning"
        risk_level = "Medium"
    elif dark > 5.0:
        predicted_class = "scorched"
        confidence = min(0.92, 0.65 + (dark / 15.0))
        farmer_label = "Heat Damage / Spoilage Warning"
        risk_level = "High"
    elif particle_count > 6 or particle["risk_level"] == "High":
        predicted_class = "pecky"
        confidence = min(0.90, 0.60 + (particle_count * 0.03))
        farmer_label = "Defective / Contamination Warning"
        risk_level = "Medium"
    elif green > 10.0:
        predicted_class = "greenish"
        confidence = min(0.88, 0.65 + (green / 30.0))
        farmer_label = "Abnormal Color / Quality Warning"
        risk_level = "Medium"
    else:
        predicted_class = "good"
        confidence = 0.91
        farmer_label = "Good Quality"
        risk_level = "Low"

    return {
        "predicted_class": predicted_class,
        "farmer_label": farmer_label,
        "confidence": round(confidence, 2),
        "risk_level": risk_level,
        "is_fallback": True,
        "note": "Visual heuristic assessment (run 'python models/train_feed_model.py' once dataset is added for deep learning inference)."
    }


def heuristic_silage_classifier(cv_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Intelligent heuristic classifier for silage samples (fresh vs spoiled).
    """
    color = cv_results["color_analysis"]
    white_grey = color["white_grey_patch_pct"]
    dark = color["dark_patch_pct"]

    if white_grey > 4.0 or dark > 15.0:
        predicted_class = "spoiled"
        confidence = min(0.95, 0.72 + (white_grey / 20.0) + (dark / 30.0))
        farmer_label = "Spoiled / High Fungal Risk Silage"
        risk_level = "High"
    else:
        predicted_class = "fresh"
        confidence = 0.89
        farmer_label = "Fresh / Well-Preserved Silage"
        risk_level = "Low"

    return {
        "predicted_class": predicted_class,
        "farmer_label": farmer_label,
        "confidence": round(confidence, 2),
        "risk_level": risk_level,
        "is_fallback": True,
        "note": "Silage heuristic assessment (train silage model for neural inference)."
    }


def predict_feed_quality(
    image_input: Union[str, np.ndarray, Image.Image],
    sample_type: str = "Feed Ingredient"
) -> Dict[str, Any]:
    """
    Main prediction pipeline:
    1. Runs OpenCV analysis for color, texture, and foreign particle risk.
    2. Runs MobileNetV2 if model file exists and TensorFlow is present.
    3. Otherwise applies domain-grounded visual heuristic classifier.
    
    Args:
        image_input: Path, numpy array, or PIL Image.
        sample_type: 'Feed Ingredient', 'Compound Cattle Feed', or 'Silage'.
        
    Returns:
        dict: Complete prediction including raw class, farmer-friendly label,
              confidence score, risk level, and full OpenCV breakdown.
    """
    # 1. Run OpenCV Visual Analysis
    cv_results = analyze_feed_image(image_input)

    is_silage = (sample_type.strip().lower() == "silage")
    model_path = SILAGE_MODEL_PATH if is_silage else FEED_MODEL_PATH
    labels_path = SILAGE_LABELS_PATH if is_silage else FEED_LABELS_PATH
    label_cfg = load_label_config(labels_path)

    # 2. Check for TensorFlow and trained weights
    model_available = model_path.exists()
    tf_available = False

    try:
        import tensorflow as tf
        tf_available = True
    except ImportError:
        tf_available = False

    if tf_available and model_available:
        try:
            cache_key = str(model_path)
            if cache_key not in _CACHED_MODELS:
                _CACHED_MODELS[cache_key] = tf.keras.models.load_model(str(model_path))
            model = _CACHED_MODELS[cache_key]

            # Preprocess image
            if isinstance(image_input, (str, Path)):
                pil_img = Image.open(image_input).convert("RGB")
            elif isinstance(image_input, np.ndarray):
                bgr = load_image_to_cv(image_input)
                pil_img = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
            else:
                pil_img = image_input.convert("RGB")

            resized = pil_img.resize((224, 224))
            img_array = np.expand_dims(np.array(resized, dtype=np.float32), axis=0)

            # Predict
            preds = model.predict(img_array, verbose=0)[0]
            class_idx = int(np.argmax(preds))
            confidence = float(preds[class_idx])

            classes = label_cfg.get("classes", ["good", "moldy", "burnt", "pecky", "scorched", "greenish"])
            predicted_class = classes[class_idx] if class_idx < len(classes) else "unknown"

            farmer_labels = label_cfg.get("farmer_labels", {})
            risk_levels = label_cfg.get("risk_levels", {})

            farmer_label = farmer_labels.get(predicted_class, predicted_class.title())
            risk_level = risk_levels.get(predicted_class, "Medium")

            prediction_result = {
                "predicted_class": predicted_class,
                "farmer_label": farmer_label,
                "confidence": round(confidence, 2),
                "risk_level": risk_level,
                "is_fallback": False,
                "note": "Predicted using trained MobileNetV2 Deep Learning Model."
            }
        except Exception as e:
            # Graceful fallback in case of loading / dimension issue
            prediction_result = heuristic_silage_classifier(cv_results) if is_silage else heuristic_feed_classifier(cv_results)
            prediction_result["note"] = f"Model execution warning ({e}); reverted to heuristic classifier."
    else:
        # Fallback to OpenCV-guided heuristic classifier
        prediction_result = heuristic_silage_classifier(cv_results) if is_silage else heuristic_feed_classifier(cv_results)

    # 3. Assemble unified result
    return {
        "sample_type": sample_type,
        "predicted_class": prediction_result["predicted_class"],
        "farmer_label": prediction_result["farmer_label"],
        "confidence": prediction_result["confidence"],
        "mould_risk": "High" if prediction_result["predicted_class"] == "moldy" or cv_results["cv_mould_indicator"] == "High" else cv_results["cv_mould_indicator"],
        "foreign_particle_risk": cv_results["foreign_particle_risk"]["risk_level"],
        "visual_quality_score": cv_results["visual_quality_score"],
        "is_fallback": prediction_result["is_fallback"],
        "inference_note": prediction_result["note"],
        "cv_details": cv_results
    }
