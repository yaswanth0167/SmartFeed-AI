"""
SmartFeed AI - Risk Intelligence Engine & SmartFeed Health Score
Calculates a transparent, weighted multi-factor Health Score (0–100), determines
the overall risk level, identifies the primary concern, and produces the
explainable 'Why This Result?' farmer breakdown.
"""

import re
import datetime
from typing import Dict, Any, List, Optional


class RiskIntelligenceEngine:
    """
    Combines computer vision findings, OpenCV metrics, adulteration analysis,
    nutrition inputs, storage conditions, and historical trends into an explainable
    composite health score and actionable risk determination.
    """

    def calculate_health_score(
        self,
        visual_res: Dict[str, Any],
        adulteration_res: Dict[str, Any],
        nutrition_res: Dict[str, Any],
        storage_condition: str,
        historical_tests: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Calculates the SmartFeed Health Score (0-100) using a transparent weighted penalty system.
        
        Weights:
        - Visual Quality: 40% (Contribution from CV & Defect Classifier)
        - Mould / Fungal Risk: 20%
        - Possible Foreign Particle Risk: 10%
        - Possible Adulteration Risk: 10%
        - Nutrition Balance: 10%
        - Storage Condition: 10%
        
        Args:
            visual_res: Output from predict_feed_quality()
            adulteration_res: Output from check_adulteration_risk()
            nutrition_res: Output from analyze_nutrition()
            storage_condition: Farmer's storage condition description
            historical_tests: Optional list of past tests for trend context
            
        Returns:
            dict: Health score, risk level, primary concern, score deductions,
                  and 'Why This Result?' explainability breakdown.
        """
        # --- 1. Base Score & Component Contributions ---
        # Visual quality score provides baseline 0 to 40 points
        raw_vq = visual_res.get("visual_quality_score", 85.0)
        visual_points = (raw_vq / 100.0) * 40.0

        score = visual_points + 60.0  # Total available: 100.0
        deductions: List[Dict[str, Any]] = []

        # --- 2. Mould / Fungal Risk Deduction (Max 20 pts) ---
        mould_risk = visual_res.get("mould_risk", "Low")
        if mould_risk == "High":
            penalty = 20.0
            score -= penalty
            deductions.append({
                "factor": "Mould / Fungal Risk",
                "severity": "High",
                "points": -penalty,
                "reason": "Visible fungal mycelium or high white/grey patch coverage detected."
            })
        elif mould_risk == "Medium":
            penalty = 10.0
            score -= penalty
            deductions.append({
                "factor": "Mould / Fungal Risk",
                "severity": "Medium",
                "points": -penalty,
                "reason": "Mild fungal or spore indications observed on the surface."
            })

        # --- 3. Possible Foreign Particle Risk Deduction (Max 10 pts) ---
        foreign_risk = visual_res.get("foreign_particle_risk", "Low")
        if foreign_risk == "High":
            penalty = 10.0
            score -= penalty
            deductions.append({
                "factor": "Possible Foreign Particle Risk",
                "severity": "High",
                "points": -penalty,
                "reason": "Multiple high-contrast anomalous inclusions visually observed."
            })
        elif foreign_risk == "Medium":
            penalty = 5.0
            score -= penalty
            deductions.append({
                "factor": "Possible Foreign Particle Risk",
                "severity": "Medium",
                "points": -penalty,
                "reason": "A few distinct particulate inclusions detected."
            })

        # --- 4. Possible Adulteration Risk Deduction (Max 10 pts) ---
        adulteration_risk = adulteration_res.get("adulteration_risk", "Low")
        if adulteration_risk == "High":
            penalty = 10.0
            score -= penalty
            deductions.append({
                "factor": "Possible Adulteration Risk",
                "severity": "High",
                "points": -penalty,
                "reason": "Sensory markers and nutrient profiles indicate potential adulteration."
            })
        elif adulteration_risk == "Medium":
            penalty = 5.0
            score -= penalty
            deductions.append({
                "factor": "Possible Adulteration Risk",
                "severity": "Medium",
                "points": -penalty,
                "reason": "Minor sensory or composition discrepancies flagged."
            })

        # --- 5. Nutrition Balance Deduction (Max 10 pts) ---
        nutr_status = nutrition_res.get("nutrition_status", "Balanced")
        if nutr_status == "Poor":
            penalty = 10.0
            score -= penalty
            deductions.append({
                "factor": "Nutrition Balance",
                "severity": "High",
                "points": -penalty,
                "reason": "Critical nutrient imbalance (severe protein deficiency or excess moisture)."
            })
        elif nutr_status == "Needs Improvement":
            penalty = 5.0
            score -= penalty
            deductions.append({
                "factor": "Nutrition Balance",
                "severity": "Medium",
                "points": -penalty,
                "reason": "One or more nutrient parameters deviate from target reference ranges."
            })

        # --- 6. Storage Condition Deduction (Max 10 pts) ---
        storage_lower = storage_condition.lower()
        if "damp" in storage_lower or "humid shed" in storage_lower or "humid storage" in storage_lower or "high humidity" in storage_lower or "flooded" in storage_lower:
            penalty = 10.0
            score -= penalty
            deductions.append({
                "factor": "Storage Condition",
                "severity": "High",
                "points": -penalty,
                "reason": "Damp / high humidity storage drastically accelerates fungal germination."
            })
        elif "poor" in storage_lower or "outdoor" in storage_lower or "warm" in storage_lower or "unventilated" in storage_lower:
            penalty = 6.0
            score -= penalty
            deductions.append({
                "factor": "Storage Condition",
                "severity": "Medium",
                "points": -penalty,
                "reason": "Sub-optimal ventilation or exposure to heat and pests."
            })

        # --- 7. Historical Trend Impact ---
        trend_warning = False
        trend_note = "No previous test history available."
        if historical_tests and len(historical_tests) >= 1:
            latest_past_score = float(historical_tests[-1].get("quality_score", 0.0))
            if latest_past_score > 0 and score < (latest_past_score - 15.0):
                trend_warning = True
                penalty = 5.0
                score -= penalty
                trend_note = f"Quality score has dropped significantly from previous batch ({latest_past_score:.0f} → {score:.0f})."
                deductions.append({
                    "factor": "Historical Trend",
                    "severity": "Medium",
                    "points": -penalty,
                    "reason": trend_note
                })
            else:
                trend_note = "Quality trend is stable or consistent with recent batches."

        # Clamp score between 0.0 and 100.0
        final_health_score = round(max(0.0, min(100.0, score)), 1)

        # --- 8. Overall Risk Level Interpretation ---
        # Biological safety rule: High mould or high adulteration forces overall risk to High
        if final_health_score >= 80.0 and mould_risk != "High" and adulteration_risk != "High":
            overall_risk = "Low"
            risk_label = "🟢 GOOD / SAFE"
            safety_badge = "SAFE FOR USE"
        elif final_health_score >= 50.0 and mould_risk != "High" and adulteration_risk != "High":
            overall_risk = "Medium"
            risk_label = "🟡 NEEDS ATTENTION"
            safety_badge = "NEEDS ATTENTION"
        else:
            overall_risk = "High"
            risk_label = "🔴 HIGH RISK"
            safety_badge = "HIGH RISK - DO NOT FEED"

        # --- 9. Primary Concern Identification ---
        primary_concern, recommended_action = self._identify_primary_concern(
            mould_risk=mould_risk,
            adulteration_res=adulteration_res,
            nutrition_res=nutrition_res,
            storage_condition=storage_condition,
            foreign_risk=foreign_risk,
            trend_warning=trend_warning
        )

        # --- 10. Explainable AI: "WHY THIS RESULT?" ---
        why_breakdown = self._generate_why_breakdown(
            visual_res=visual_res,
            adulteration_res=adulteration_res,
            nutrition_res=nutrition_res,
            storage_condition=storage_condition,
            trend_note=trend_note,
            deductions=deductions,
            final_score=final_health_score
        )

        # --- 11. Predictive Shelf Life & Spoilage Forecast ---
        cv_details = visual_res.get("cv_details", {})
        color_res = cv_details.get("color_analysis", {})
        white_grey_pct = float(color_res.get("white_grey_patch_pct", 0.0))
        dark_pct = float(color_res.get("dark_patch_pct", 0.0))

        nutr_inputs = nutrition_res.get("inputs", {})
        moist_val = float(nutr_inputs.get("moisture", nutrition_res.get("moisture", 10.0)))

        days_match = re.search(r'storage\s+(\d+)\s+days', storage_condition, re.IGNORECASE)
        if days_match:
            elapsed_days = int(days_match.group(1))
        else:
            elapsed_days = int(nutr_inputs.get("storage_days", 5))

        sample_type_val = visual_res.get("sample_type", "Cattle Feed")

        shelf_life_info = self.estimate_shelf_life(
            sample_type=sample_type_val,
            moisture_pct=moist_val,
            storage_days_elapsed=elapsed_days,
            mould_risk=mould_risk,
            visual_quality_score=raw_vq,
            storage_condition=storage_condition,
            white_grey_patch_pct=white_grey_pct,
            dark_patch_pct=dark_pct,
            smell_abnormal=("fungal" in storage_condition.lower() or adulteration_risk == "High")
        )

        return {
            "health_score": final_health_score,
            "overall_risk": overall_risk,
            "risk_label": risk_label,
            "safety_badge": safety_badge,
            "primary_concern": primary_concern,
            "recommended_action": recommended_action,
            "deductions": deductions,
            "why_this_result": why_breakdown,
            "trend_warning": trend_warning,
            "trend_note": trend_note,
            "shelf_life": shelf_life_info,
            "components": {
                "visual_quality_score": raw_vq,
                "mould_risk": mould_risk,
                "foreign_particle_risk": foreign_risk,
                "adulteration_risk": adulteration_risk,
                "nutrition_status": nutr_status,
                "storage_condition": storage_condition,
                "shelf_life_days": shelf_life_info["shelf_life_days"],
                "shelf_life_status": shelf_life_info["shelf_life_status"]
            }
        }

    def estimate_shelf_life(
        self,
        sample_type: str,
        moisture_pct: float,
        storage_days_elapsed: int,
        mould_risk: str,
        visual_quality_score: float,
        storage_condition: str,
        white_grey_patch_pct: float = 0.0,
        dark_patch_pct: float = 0.0,
        smell_abnormal: bool = False
    ) -> Dict[str, Any]:
        """
        Estimates the remaining safe shelf life and future spoilage window (in days)
        based on feed commodity baselines, moisture content, elapsed storage days,
        and OpenCV visual defect/fungal patch coverage.
        """
        st_lower = sample_type.lower()
        
        # 1. Base Shelf Life Ceiling by Commodity (Days from production under ideal dry conditions)
        if "silage" in st_lower:
            base_days = 7
        elif "green" in st_lower or "fodder" in st_lower:
            base_days = 3
        elif "cake" in st_lower or "cotton" in st_lower or "groundnut" in st_lower:
            base_days = 45
        elif "straw" in st_lower or "hay" in st_lower:
            base_days = 120
        elif "bran" in st_lower:
            base_days = 45
        else:
            base_days = 75
            
        # 2. Storage Days Elapsed Factor
        elapsed = max(0, int(storage_days_elapsed))
        remaining_base = max(0, base_days - elapsed)
        
        # 3. Critical Spoilage Override: If high mould or severe visual damage detected, shelf life is 0
        if mould_risk == "High" or visual_quality_score < 40.0 or white_grey_patch_pct > 6.0:
            status = "EXPIRED"
            status_label_en = "Already Spoiled / 0 Days Remaining"
            status_label_te = "ఇప్పటికే పాడైంది (0 రోజులు)"
            status_label_hi = "पहले से खराब (0 दिन)"
            action_tip_en = "Fungal mold / severe spoilage detected. Do NOT feed to cattle. Risk of aflatoxicosis and acute milk yield drop."
            action_tip_te = "తీవ్రమైన బూజు చేరినందున పశువులకు వేయడం సురక్షితం కాదు. వెంటనే తొలగించండి లేదా ఎండబెట్టండి."
            action_tip_hi = "गंभीर फफूंद पाई गई है। पशुओं को न खिलाएं। विषैले तत्वों का खतरा है।"
            safe_until = "EXPIRED"
            timeline = [
                {"phase": "Optimal Quality", "days": "Past", "condition": "Nutritional value decayed", "status": "Expired"},
                {"phase": "Spoilage Progress", "days": "Active", "condition": "Fungal mycelium & mycotoxins present", "status": "Active Mould"},
                {"phase": "Safety Action", "days": "Immediate", "condition": "Discard / Do not feed to lactating cows", "status": "Do Not Feed"}
            ]
            return {
                "shelf_life_days": 0,
                "shelf_life_range": "0 Days (Expired)",
                "shelf_life_status": status,
                "status_label_en": status_label_en,
                "status_label_te": status_label_te,
                "status_label_hi": status_label_hi,
                "safe_until_date": safe_until,
                "action_tip_en": action_tip_en,
                "action_tip_te": action_tip_te,
                "action_tip_hi": action_tip_hi,
                "timeline": timeline,
                "moisture_factor": 0.0,
                "storage_factor": 0.0
            }

        # 4. Moisture Factor (Nonlinear biological multiplier)
        if "silage" in st_lower:
            moisture_factor = 1.0 if moisture_pct <= 70.0 else 0.7
        else:
            if moisture_pct <= 11.0:
                moisture_factor = 1.0
            elif moisture_pct <= 12.5:
                moisture_factor = 0.80
            elif moisture_pct <= 14.0:
                moisture_factor = 0.50
            elif moisture_pct <= 16.0:
                moisture_factor = 0.25
            else:
                moisture_factor = 0.10

        # 5. Visual Spore & Defect Factor
        if mould_risk == "Medium" or white_grey_patch_pct > 2.0:
            defect_factor = 0.35
        elif dark_patch_pct > 8.0:
            defect_factor = 0.55
        else:
            defect_factor = 1.0

        # 6. Storage Environment Factor
        cond_lower = storage_condition.lower()
        if "humid" in cond_lower or "damp" in cond_lower:
            storage_factor = 0.45
        elif "poor" in cond_lower or "outdoor" in cond_lower or "warm" in cond_lower:
            storage_factor = 0.65
        else:
            storage_factor = 1.0
            
        if smell_abnormal:
            storage_factor *= 0.50

        # 7. Compute Projected Safe Days
        calculated_days = remaining_base * moisture_factor * defect_factor * storage_factor
        shelf_days = int(round(max(0, calculated_days)))

        # Cap according to risk boundaries
        if mould_risk == "Medium" and shelf_days > 5:
            shelf_days = 5

        if shelf_days <= 2:
            status = "CRITICAL"
            shelf_range = f"{shelf_days} Days" if shelf_days > 0 else "1-2 Days"
            status_label_en = f"Critical Spoilage Risk ({shelf_range})"
            status_label_te = f"అత్యవసర నిల్వ వ్యవధి ({shelf_range})"
            status_label_hi = f"अति संवेदनशील अवधि ({shelf_range})"
            action_tip_en = "Moisture or early spores detected. Sun-dry immediately or feed within 48 hours to prevent mold."
            action_tip_te = "తేమ లేదా బూజు ప్రారంభం ఉంది. వెంటనే ఎండబెట్టండి లేదా 48 గంటల్లో వాడండి."
            action_tip_hi = "सीलन या फफूंद के संकेत हैं। तुरंत धूप में सुखाएं या 48 घंटे में उपयोग करें।"
        elif shelf_days <= 10:
            status = "ATTENTION"
            shelf_range = f"{shelf_days}-{shelf_days + 3} Days"
            status_label_en = f"Moderate Safe Window ({shelf_range})"
            status_label_te = f"పరిమిత నిల్వ కాలం ({shelf_range})"
            status_label_hi = f"मध्यम सुरक्षित अवधि ({shelf_range})"
            action_tip_en = "Keep in a dry, ventilated shed. Ensure bags are placed on wooden pallets off the damp floor."
            action_tip_te = "గాలి ఆడే పొడి ప్రదేశంలో ఉంచండి. నేలపై తేమ తగలకుండా చెక్క పలకలపై బస్తాలు పెట్టండి."
            action_tip_hi = "हवादार सूखे स्थान पर रखें। बोरियों को फर्श की नमी से बचाने के लिए तख्तों पर रखें।"
        else:
            status = "SAFE"
            shelf_range = f"{shelf_days}-{shelf_days + 5} Days"
            status_label_en = f"Safe Storage Window (~{shelf_range})"
            status_label_te = f"సురక్షిత నిల్వ కాలం (~{shelf_range})"
            status_label_hi = f"सुरक्षित भंडारण अवधि (~{shelf_range})"
            action_tip_en = "Feed is in healthy condition. Maintain current dry, shaded storage conditions."
            action_tip_te = "మేత మంచి స్థితిలో ఉంది. ప్రస్తుత పొడి వాతావరణ నిల్వను కొనసాగించండి."
            action_tip_hi = "चारा अच्छी स्थिति में है। वर्तमान सूखी भंडारण स्थिति बनाए रखें।"

        # 8. Date Projection
        now = datetime.datetime.now()
        safe_until_dt = now + datetime.timedelta(days=shelf_days)
        safe_until = safe_until_dt.strftime("%d %b %Y")

        # 9. Spoilage Timeline Breakdown
        p1_end = max(1, shelf_days // 2)
        timeline = [
            {
                "phase": "Optimal Safe",
                "days": f"Day 0 to {p1_end}",
                "condition": "High nutritional potency, safe daily ration",
                "status": "Safe"
            },
            {
                "phase": "Caution Window",
                "days": f"Day {p1_end + 1} to {shelf_days}",
                "condition": "Moisture & fungal spore monitoring window",
                "status": "Inspect"
            },
            {
                "phase": "Spoilage Danger",
                "days": f"After {safe_until}",
                "condition": "Risk of fungal bloom, mycotoxins & souring",
                "status": "Risk"
            }
        ]

        return {
            "shelf_life_days": shelf_days,
            "shelf_life_range": shelf_range,
            "shelf_life_status": status,
            "status_label_en": status_label_en,
            "status_label_te": status_label_te,
            "status_label_hi": status_label_hi,
            "safe_until_date": safe_until,
            "action_tip_en": action_tip_en,
            "action_tip_te": action_tip_te,
            "action_tip_hi": action_tip_hi,
            "timeline": timeline,
            "moisture_factor": round(moisture_factor, 2),
            "storage_factor": round(storage_factor, 2)
        }

    def _identify_primary_concern(
        self,
        mould_risk: str,
        adulteration_res: Dict[str, Any],
        nutrition_res: Dict[str, Any],
        storage_condition: str,
        foreign_risk: str,
        trend_warning: bool
    ) -> tuple[str, str]:
        """Prioritizes the most critical hazard requiring farmer attention."""
        flagged = adulteration_res.get("flagged_hazards", [])

        # Priority 1: High Mould / Fungal
        if mould_risk == "High":
            return (
                "🚨 Fungal & Mould Proliferation Risk",
                "Immediately withhold feed from dairy animals. Inspect feed for visible mould clumps and store in dry, sunlight-exposed conditions."
            )

        # Priority 2: Urea / NPN Spiking
        if any("Urea" in h for h in flagged):
            return (
                "🚨 Possible Urea / NPN Chemical Spiking Risk",
                "Do NOT feed to livestock immediately. Quarantine this feed batch and submit a sample to an accredited dairy testing lab for chemical analysis."
            )

        # Priority 3: High Moisture Spoilage
        param_moist = nutrition_res.get("parameter_status", {}).get("moisture", "")
        if "Excessive" in param_moist or "Too Wet" in param_moist:
            return (
                "⚠️ Dangerous Feed Moisture Level",
                "Spread feed on a clean, dry tarpaulin under proper ventilation or direct sunlight. Do not bag damp feed."
            )

        # Priority 4: Foreign Particles
        if foreign_risk == "High":
            return (
                "⚠️ High Foreign Particle Inclusions",
                "Sieve and clean the feed to remove foreign stones, hardware, or large particles that could injure cattle digestive tracts."
            )

        # Priority 5: High Adulteration Hazard
        if adulteration_res.get("adulteration_risk") == "High":
            return (
                "⚠️ Suspected Feed Composition Irregularity",
                "Feed displays abnormal texture and nutrient markers. Inspect thoroughly or seek cooperative verification."
            )

        # Priority 6: Rapid Spoilage Trend
        if trend_warning:
            return (
                "⚠️ Rapid Feed Quality Degradation",
                "Feed quality is deteriorating faster than expected. Inspect storage room ventilation and check for moisture seepage."
            )

        # Priority 7: Poor Storage
        storage_low = storage_condition.lower()
        if "damp" in storage_low or "humid shed" in storage_low or "humid storage" in storage_low or "high humidity" in storage_low or "flooded" in storage_low:
            return (
                "⚠️ High Storage Humidity",
                "Relocate feed bags onto wooden pallets away from damp floors and ensure continuous cross-ventilation."
            )

        # Priority 8: Low Protein Deficiency
        if nutrition_res.get("parameter_status", {}).get("protein") == "Deficient":
            return (
                "🥗 Crude Protein Deficiency",
                "Feed is safe but low in protein. Supplement with oil cakes (cottonseed/mustard/groundnut cake) or mineral mixture to sustain milk yield."
            )

        # Default
        return (
            "✅ Feed in Good Condition",
            "Feed parameters are optimal. Maintain dry storage and feed according to recommended animal body weight allowances."
        )

    def _generate_why_breakdown(
        self,
        visual_res: Dict[str, Any],
        adulteration_res: Dict[str, Any],
        nutrition_res: Dict[str, Any],
        storage_condition: str,
        trend_note: str,
        deductions: List[Dict[str, Any]],
        final_score: float
    ) -> Dict[str, Any]:
        """Constructs transparent, jargon-free explanations of the evaluation."""
        reasons_summary = []
        positive_factors = []

        # Visual reasoning
        pred_label = visual_res.get("farmer_label", "Unknown")
        color = visual_res.get("cv_details", {}).get("color_analysis", {})
        if visual_res.get("mould_risk") == "High":
            reasons_summary.append(f"🍄 Mould-like visual patterns ({color.get('white_grey_patch_pct', 0):.1f}% pale area) were detected by computer vision.")
        elif visual_res.get("predicted_class") == "good":
            positive_factors.append("Clean, uniform grain appearance with minimal discoloration.")

        # OpenCV foreign particles
        particles = visual_res.get("cv_details", {}).get("foreign_particle_risk", {})
        if particles.get("risk_level") in ["High", "Medium"]:
            reasons_summary.append(f"🔍 Foreign particle screening observed {particles.get('particle_count', 0)} contrasting inclusions.")
        else:
            positive_factors.append("No significant foreign particle inclusions visually detected.")

        # Nutrition reasoning
        inputs = nutrition_res.get("inputs", {})
        moist = inputs.get("moisture", 0.0)
        protein = inputs.get("crude_protein", 0.0)
        if "Excessive" in nutrition_res.get("parameter_status", {}).get("moisture", ""):
            reasons_summary.append(f"💧 Moisture level ({moist:.1f}%) is higher than the safe storage threshold.")
        else:
            positive_factors.append(f"Moisture ({moist:.1f}%) is within safe storage limits.")

        if protein < 16.0 and visual_res.get("sample_type") != "Silage":
            reasons_summary.append(f"📉 Crude Protein ({protein:.1f}%) is below optimal cattle diet requirements.")

        # Adulteration reasoning
        if adulteration_res.get("adulteration_risk") in ["High", "Medium"]:
            for r in adulteration_res.get("reasons", [])[:2]:
                reasons_summary.append(f"⚠️ {r}")

        # Storage reasoning
        if "humid" in storage_condition.lower() or "damp" in storage_condition.lower() or "poor" in storage_condition.lower():
            reasons_summary.append(f"🏠 Storage environment ({storage_condition}) increases spoilage and mould propagation risk.")
        else:
            positive_factors.append(f"Storage environment ({storage_condition}) is favorable.")

        # Trend reasoning
        if "dropped" in trend_note.lower() or "decreasing" in trend_note.lower():
            reasons_summary.append(f"📊 {trend_note}")

        if not reasons_summary:
            reasons_summary.append("All visual, nutritional, and storage checks meet optimal dairy standards.")

        return {
            "headline": f"Why Score is {final_score:.0f}/100",
            "concerns_list": reasons_summary,
            "positives_list": positive_factors,
            "deductions_list": deductions,
            "trend_explanation": trend_note
        }


# Singleton engine instance
_risk_engine = RiskIntelligenceEngine()


def evaluate_smartfeed_risks(
    visual_res: Dict[str, Any],
    adulteration_res: Dict[str, Any],
    nutrition_res: Dict[str, Any],
    storage_condition: str,
    historical_tests: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Convenience function calling the singleton RiskIntelligenceEngine."""
    return _risk_engine.calculate_health_score(
        visual_res=visual_res,
        adulteration_res=adulteration_res,
        nutrition_res=nutrition_res,
        storage_condition=storage_condition,
        historical_tests=historical_tests
    )
