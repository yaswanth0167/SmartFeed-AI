"""
SmartFeed AI - Nutrition Assessment Module
Evaluates simulated or farmer-entered nutrient values against domain reference ranges
(e.g., BIS standards and ICAR dairy cattle guidelines).
"""

import os
import csv
from pathlib import Path
from typing import Dict, Any, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REFERENCE_FILE = PROJECT_ROOT / "data" / "nutrient_reference.csv"

# Fallback in-memory domain reference benchmarks if CSV is moved
DEFAULT_REFERENCES = {
    "Compound Cattle Feed": {
        "protein_min": 18.0, "protein_max": 22.0,
        "moisture_min": 8.0, "moisture_max": 12.0,
        "fiber_min": 8.0, "fiber_max": 14.0,
        "ideal_protein": 20.0, "ideal_moisture": 10.0, "ideal_fiber": 12.0
    },
    "Feed Ingredient": {
        "protein_min": 10.0, "protein_max": 28.0,
        "moisture_min": 6.0, "moisture_max": 12.0,
        "fiber_min": 4.0, "fiber_max": 18.0,
        "ideal_protein": 18.0, "ideal_moisture": 10.0, "ideal_fiber": 10.0
    },
    "Silage": {
        "protein_min": 7.0, "protein_max": 11.0,
        "moisture_min": 60.0, "moisture_max": 72.0,
        "fiber_min": 18.0, "fiber_max": 30.0,
        "ideal_protein": 8.5, "ideal_moisture": 65.0, "ideal_fiber": 24.0
    }
}


def load_reference_ranges() -> Dict[str, Dict[str, float]]:
    """Loads nutrient benchmarks from data/nutrient_reference.csv."""
    ref_data = DEFAULT_REFERENCES.copy()
    if REFERENCE_FILE.exists():
        try:
            with open(REFERENCE_FILE, "r", encoding="utf-8") as f:
                # Filter out comment lines starting with #
                lines = [line for line in f if not line.strip().startswith("#")]
                reader = csv.DictReader(lines)
                for row in reader:
                    ft = row.get("feed_type", "").strip()
                    if ft:
                        ref_data[ft] = {
                            "protein_min": float(row["protein_min"]),
                            "protein_max": float(row["protein_max"]),
                            "moisture_min": float(row["moisture_min"]),
                            "moisture_max": float(row["moisture_max"]),
                            "fiber_min": float(row["fiber_min"]),
                            "fiber_max": float(row["fiber_max"]),
                            "ideal_protein": float(row.get("ideal_protein", (float(row["protein_min"]) + float(row["protein_max"])) / 2)),
                            "ideal_moisture": float(row.get("ideal_moisture", (float(row["moisture_min"]) + float(row["moisture_max"])) / 2)),
                            "ideal_fiber": float(row.get("ideal_fiber", (float(row["fiber_min"]) + float(row["fiber_max"])) / 2)),
                        }
        except Exception:
            pass
    return ref_data


def analyze_nutrition(
    sample_type: str,
    crude_protein: float,
    moisture: float,
    fiber: float,
    energy_mcal: Optional[float] = None
) -> Dict[str, Any]:
    """
    Analyzes entered nutrient levels against reference ranges for the specified sample type.
    
    Args:
        sample_type: 'Compound Cattle Feed', 'Feed Ingredient', or 'Silage'.
        crude_protein: Crude protein percentage (0–30%).
        moisture: Moisture percentage (0–100%).
        fiber: Crude fiber percentage (0–50%).
        energy_mcal: Optional metabolizable energy (Mcal/kg).
        
    Returns:
        dict: Nutritional balance score, status, warnings, and breakdown.
    """
    ref_map = load_reference_ranges()
    # Normalize sample type key
    matched_key = "Feed Ingredient"
    for k in ref_map:
        if k.lower() in sample_type.lower():
            matched_key = k
            break

    target = ref_map.get(matched_key, DEFAULT_REFERENCES["Feed Ingredient"])

    issues = []
    penalties = 0.0

    # 1. Crude Protein Evaluation
    protein_status = "Optimal"
    if crude_protein < target["protein_min"]:
        deficit = target["protein_min"] - crude_protein
        protein_status = "Deficient"
        issues.append(f"Crude Protein ({crude_protein:.1f}%) is below optimal minimum ({target['protein_min']:.1f}%). May reduce milk production.")
        penalties += min(35.0, deficit * 4.0)
    elif crude_protein > (target["protein_max"] * 1.35):
        # Abnormally high protein alert
        protein_status = "Abnormally High"
        issues.append(f"Crude Protein ({crude_protein:.1f}%) is unusually high for {sample_type} (norm: {target['protein_max']:.1f}%). Possible non-protein nitrogen / urea addition risk.")
        penalties += 25.0
    elif crude_protein > target["protein_max"]:
        protein_status = "High"
        issues.append(f"Crude Protein ({crude_protein:.1f}%) is higher than typical range ({target['protein_max']:.1f}%).")
        penalties += 10.0

    # 2. Moisture Evaluation
    moisture_status = "Optimal"
    if matched_key != "Silage":
        # Dry feed: moisture > 13% is dangerous for mould growth
        if moisture > 14.0:
            moisture_status = "Excessive (High Spoilage Risk)"
            issues.append(f"Moisture ({moisture:.1f}%) exceeds the 12.0% safe storage threshold. Rapid fungal and mould proliferation risk.")
            penalties += min(40.0, (moisture - 12.0) * 5.0)
        elif moisture > target["moisture_max"]:
            moisture_status = "Slightly Elevated"
            issues.append(f"Moisture ({moisture:.1f}%) is slightly above recommended max ({target['moisture_max']:.1f}%).")
            penalties += 12.0
        elif moisture < target["moisture_min"]:
            moisture_status = "Dry"
    else:
        # Silage: requires 60-70% for proper lactic fermentation
        if moisture < target["moisture_min"]:
            moisture_status = "Too Dry for Silage"
            issues.append(f"Silage moisture ({moisture:.1f}%) is too low (min {target['moisture_min']:.1f}%). Poor compaction leads to trapped air and aerobic rot.")
            penalties += 25.0
        elif moisture > target["moisture_max"]:
            moisture_status = "Too Wet (Clostridial Risk)"
            issues.append(f"Silage moisture ({moisture:.1f}%) is excessive (max {target['moisture_max']:.1f}%). High risk of nutrient runoff and clostridial/butyric fermentation.")
            penalties += 25.0

    # 3. Crude Fiber Evaluation
    fiber_status = "Optimal"
    if fiber > target["fiber_max"]:
        excess = fiber - target["fiber_max"]
        fiber_status = "Excessive"
        issues.append(f"Crude Fiber ({fiber:.1f}%) exceeds recommended max ({target['fiber_max']:.1f}%). May reduce digestibility and energy density.")
        penalties += min(20.0, excess * 2.0)
    elif fiber < target["fiber_min"]:
        fiber_status = "Low"
        issues.append(f"Crude Fiber ({fiber:.1f}%) is lower than minimum ({target['fiber_min']:.1f}%). Adequate roughage is necessary for rumen health.")
        penalties += 10.0

    # Nutrition Score & Status Calculation
    nutrition_score = max(10.0, min(100.0, 100.0 - penalties))

    if nutrition_score >= 80.0:
        nutrition_status = "Balanced"
        nutrition_risk = "Low"
    elif nutrition_score >= 50.0:
        nutrition_status = "Needs Improvement"
        nutrition_risk = "Medium"
    else:
        nutrition_status = "Poor"
        nutrition_risk = "High"

    if not issues:
        issues.append("All nutrient values align well with standard domain nutritional recommendations.")

    return {
        "nutrition_score": round(nutrition_score, 1),
        "nutrition_status": nutrition_status,
        "nutrition_risk": nutrition_risk,
        "sample_type": sample_type,
        "inputs": {
            "crude_protein": crude_protein,
            "moisture": moisture,
            "fiber": fiber,
            "energy_mcal": energy_mcal
        },
        "target_ranges": target,
        "parameter_status": {
            "protein": protein_status,
            "moisture": moisture_status,
            "fiber": fiber_status
        },
        "findings": issues,
        "caveat": "SIMULATED INPUTS: Simulated manual entry for advisory calculation; laboratory testing recommended for precision."
    }
