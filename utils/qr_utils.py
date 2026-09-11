"""
SmartFeed AI - QR Code & Digital Feed Passport Module
Generates tamper-evident QR Digital Feed Passports for batches (e.g., SFA-2026-000001),
decodes uploaded QR images (via pyzbar and OpenCV QRCodeDetector), and packages
complete traceability passport records from SQLite.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, Union
import qrcode
from PIL import Image
import numpy as np
import cv2

from db.database import get_test_by_batch, get_quality_trend

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QR_DIR = PROJECT_ROOT / "generated_qr"


def ensure_qr_dir() -> Path:
    """Ensures the generated_qr directory exists."""
    QR_DIR.mkdir(parents=True, exist_ok=True)
    return QR_DIR


def generate_feed_passport_qr(
    batch_id: str,
    output_path: Optional[str] = None
) -> str:
    """
    Generates a high-contrast QR code storing the unique Batch ID for digital traceability.
    
    Args:
        batch_id: Unique batch string (e.g., SFA-2026-000001).
        output_path: Optional custom file path to save the QR image.
        
    Returns:
        str: Absolute file path to the saved QR PNG file.
    """
    ensure_qr_dir()
    
    clean_id = batch_id.strip()
    if not output_path:
        filename = f"{clean_id.replace('-', '_')}.png"
        target_path = QR_DIR / filename
    else:
        target_path = Path(output_path)

    # QR Code Configuration
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=3,
    )
    # The payload is the unique Batch ID
    qr.add_data(clean_id)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    target_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(target_path))

    return str(target_path)


def decode_qr_image(image_input: Union[str, np.ndarray, Image.Image]) -> Optional[str]:
    """
    Decodes the Batch ID from an image containing a QR code.
    Uses OpenCV QRCodeDetector with fallback to pyzbar for maximum reliability.
    
    Args:
        image_input: File path, numpy array, or PIL Image.
        
    Returns:
        str: Extracted Batch ID string if found, else None.
    """
    # 1. Convert input to BGR numpy array
    img = None
    if isinstance(image_input, (str, Path)):
        img = cv2.imread(str(image_input))
        if img is None:
            try:
                pil_img = Image.open(str(image_input)).convert("RGB")
                img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            except Exception:
                return None
    elif isinstance(image_input, Image.Image):
        img = cv2.cvtColor(np.array(image_input.convert("RGB")), cv2.COLOR_RGB2BGR)
    elif isinstance(image_input, np.ndarray):
        img = image_input
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    else:
        return None

    if img is None or img.size == 0:
        return None

    # Multi-Stage QR Detection Pipeline
    detector = cv2.QRCodeDetector()
    candidates = [img]

    # Add Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    candidates.append(gray)

    # Add Otsu Threshold & Inverted Threshold
    try:
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        candidates.append(thresh)
        candidates.append(cv2.bitwise_not(thresh))
    except Exception:
        pass

    # Stage 1: Try OpenCV QRCodeDetector across candidates
    for c in candidates:
        try:
            data, bbox, _ = detector.detectAndDecode(c)
            if data and data.strip():
                return data.strip()
        except Exception:
            pass

    # Stage 2: Try pyzbar Fallback across candidates
    try:
        from pyzbar.pyzbar import decode as pyzbar_decode
        for c in candidates:
            decoded_objs = pyzbar_decode(c)
            for obj in decoded_objs:
                text = obj.data.decode("utf-8", errors="ignore").strip()
                if text:
                    return text
    except Exception:
        pass

    # Stage 3: Try resizing if image is very large or very small
    h, w = img.shape[:2]
    if w > 1200 or w < 300:
        target_w = 600
        target_h = int(h * (target_w / w))
        resized = cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_AREA if w > 1200 else cv2.INTER_LINEAR)
        try:
            data, _, _ = detector.detectAndDecode(resized)
            if data and data.strip():
                return data.strip()
        except Exception:
            pass

        try:
            from pyzbar.pyzbar import decode as pyzbar_decode
            objs = pyzbar_decode(resized)
            for obj in objs:
                text = obj.data.decode("utf-8", errors="ignore").strip()
                if text:
                    return text
        except Exception:
            pass

    return None


def get_digital_feed_passport(batch_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves and formats complete digital passport details for a given batch.
    Includes test scores, visual findings, risks, nutrients, advisory, and historical trend.
    
    Args:
        batch_id: Unique Batch ID.
        
    Returns:
        dict: Full passport data dictionary, or None if batch_id is not found in database.
    """
    test_record = get_test_by_batch(batch_id)
    if not test_record:
        return None

    # Retrieve quality trend for this sample type for chronological traceability
    sample_type = test_record.get("sample_type", "Feed Ingredient")
    trend_history = get_quality_trend(sample_type=sample_type)

    # Format score badge and styling
    score = float(test_record.get("quality_score", 0.0))
    if score >= 80.0:
        badge_color = "🟢 Safe / Good Quality"
    elif score >= 50.0:
        badge_color = "🟡 Caution / Needs Attention"
    else:
        badge_color = "🔴 High Risk / Reject"

    return {
        "batch_id": test_record["batch_id"],
        "sample_type": test_record["sample_type"],
        "timestamp": test_record["timestamp"],
        "quality_score": score,
        "quality_badge": badge_color,
        "overall_risk": test_record.get("overall_risk", "Unknown"),
        "primary_concern": test_record.get("primary_concern", "None"),
        "visual_prediction": test_record.get("visual_prediction", "Unknown"),
        "confidence_pct": round(float(test_record.get("confidence", 0.0)) * 100, 1),
        "mould_risk": test_record.get("mould_risk", "Low"),
        "foreign_particle_risk": test_record.get("foreign_particle_risk", "Low"),
        "adulteration_risk": test_record.get("adulteration_risk", "Low"),
        "nutrition_status": test_record.get("nutrition_status", "Balanced"),
        "nutrients": {
            "crude_protein": test_record.get("crude_protein", 0.0),
            "moisture": test_record.get("moisture", 0.0),
            "fiber": test_record.get("fiber", 0.0),
        },
        "storage_condition": test_record.get("storage_condition", "Standard"),
        "shelf_life_days": test_record.get("shelf_life_days", 0),
        "shelf_life_status": test_record.get("shelf_life_status", "SAFE"),
        "safe_until_date": test_record.get("safe_until_date", "N/A"),
        "advisory": test_record.get("advisory", ""),
        "language": test_record.get("language", "en"),
        "image_path": test_record.get("image_path", ""),
        "history_count": len(trend_history),
        "disclaimer": "This Digital Feed Passport is generated by SmartFeed AI based on visual assessment and risk intelligence. Laboratory testing is recommended for chemical confirmation."
    }
