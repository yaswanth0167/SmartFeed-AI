"""
SmartFeed AI - Adulteration Risk Assessment Module
Combines rule-based expert logic and an embedded Scikit-Learn classifier to detect
potential feed adulteration, non-protein nitrogen spiking, filler contamination,
and moisture dilution risks.
"""

from typing import Dict, Any, List, Optional
import numpy as np
from sklearn.ensemble import RandomForestClassifier


class AdulterationEngine:
    """
    Expert risk intelligence engine for feed adulteration screening.
    Scientifically cautious: flags 'Possible Adulteration Risk' rather than claiming chemical certainty.
    """

    def __init__(self):
        self._ml_model = None
        self._initialize_ml_model()

    def _initialize_ml_model(self):
        """
        Initializes an embedded domain-trained RandomForest classifier on synthetic
        adulteration indicator matrices to provide ML validation alongside rules.
        """
        # Feature vector: [protein, moisture, fiber, is_powdery, is_unusual_color, is_fungal_smell, has_particles]
        X_syn = np.array([
            # Normal balanced samples (Class 0: Low Risk)
            [19.0, 10.0, 10.0, 0, 0, 0, 0],
            [20.5, 9.5, 11.0, 0, 0, 0, 0],
            [18.0, 11.0, 12.0, 0, 0, 0, 0],
            [21.0, 10.2, 9.0, 0, 0, 0, 0],
            # Suspect Urea / NPN Spiking (Class 2: High Risk)
            [28.5, 9.0, 8.0, 1, 0, 0, 0],
            [32.0, 10.0, 7.0, 1, 1, 0, 0],
            [29.0, 11.0, 6.0, 1, 0, 0, 0],
            # Filler / Sand / Silica Contamination (Class 2: High Risk or Class 1: Medium)
            [12.0, 10.0, 22.0, 0, 1, 0, 1],
            [14.0, 9.0, 24.0, 0, 0, 0, 1],
            [11.0, 12.0, 20.0, 0, 1, 0, 1],
            # Excessive Moisture / Dilution (Class 1: Medium Risk)
            [18.0, 17.0, 11.0, 0, 0, 1, 0],
            [19.0, 19.0, 10.0, 0, 1, 1, 0],
            # Visible foreign inclusion (Class 1: Medium Risk)
            [19.5, 10.5, 10.5, 0, 0, 0, 1]
        ])
        y_syn = np.array([0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 1, 1, 1])

        try:
            clf = RandomForestClassifier(n_estimators=25, random_state=42)
            clf.fit(X_syn, y_syn)
            self._ml_model = clf
        except Exception:
            self._ml_model = None

    def assess_adulteration_risk(
        self,
        feed_type: str,
        color_desc: str,
        texture_desc: str,
        smell_desc: str,
        storage_condition: str,
        foreign_particles: Any,
        crude_protein: float,
        moisture: float,
        fiber: float,
        non_protein_nitrogen: Optional[float] = None,
        visual_powder_particles: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Evaluates physical characteristics, nutrient profile, and NPN to screen for adulteration risks.
        """
        # Normalize inputs
        c_desc = str(color_desc).lower()
        t_desc = str(texture_desc).lower()
        s_desc = str(smell_desc).lower()
        store = str(storage_condition).lower()

        has_particles = False
        if isinstance(foreign_particles, bool):
            has_particles = foreign_particles
        elif isinstance(foreign_particles, (int, float)):
            has_particles = foreign_particles > 3
        elif isinstance(foreign_particles, str):
            has_particles = foreign_particles.lower() in ["high", "medium", "yes", "true"]

        reasons: List[str] = []
        flagged_hazards: List[str] = []
        risk_points = 0

        # --- RULE 0: Direct Non-Protein Nitrogen (NPN) & Urea Evaluation ---
        if non_protein_nitrogen is not None:
            if non_protein_nitrogen >= 2.0:
                risk_points += 55
                flagged_hazards.append("Critical Urea / Non-Protein Nitrogen (NPN) Spiking Risk")
                reasons.append(
                    f"Non-Protein Nitrogen (NPN) of {non_protein_nitrogen:.1f}% indicates deliberate urea spiking. Normal safe limit for compound feed is <1.0%."
                )
            elif non_protein_nitrogen >= 1.2:
                risk_points += 30
                flagged_hazards.append("Elevated NPN Adulteration Concern")
                reasons.append(
                    f"Non-Protein Nitrogen (NPN) of {non_protein_nitrogen:.1f}% exceeds typical commercial feed benchmarks (0.4–0.8%)."
                )

        if visual_powder_particles is not None:
            if visual_powder_particles >= 20:
                risk_points += 30
                flagged_hazards.append("Excessive Powder / Chalk Residue")
                reasons.append(
                    f"High concentration of white powder/crystalline particles ({int(visual_powder_particles)}) indicates urea granules or calcite chalk adulteration."
                )
            elif visual_powder_particles >= 10:
                risk_points += 15
                reasons.append(f"Noticeable fine powder particles ({int(visual_powder_particles)}) observed in sample.")

        # --- RULE 1: Possible Urea / Non-Protein Nitrogen (NPN) Spiking ---
        # Cattle feed is often artificially spiked with urea/fertilizer to inflate apparent protein tests
        if feed_type != "Silage":
            if crude_protein >= 26.0 and ("powdery" in t_desc or "unusual" in s_desc or "chemical" in s_desc or "unusual" in c_desc or (non_protein_nitrogen and non_protein_nitrogen >= 1.2)):
                risk_points += 45
                if "Critical Urea / Non-Protein Nitrogen (NPN) Spiking Risk" not in flagged_hazards:
                    flagged_hazards.append("Possible Urea / Non-Protein Nitrogen (NPN) Adulteration Risk")
                reasons.append(
                    f"Abnormally high Crude Protein ({crude_protein:.1f}%) combined with powdery texture or chemical aroma indicates possible urea spiking to falsely inflate crude protein readings."
                )
            elif crude_protein >= 27.0:
                risk_points += 30
                if "Unusually High Nitrogen Profile" not in flagged_hazards:
                    flagged_hazards.append("Unusually High Nitrogen Profile")
                reasons.append(
                    f"Crude protein ({crude_protein:.1f}%) significantly exceeds standard commercial cattle feed benchmarks (18–22%)."
                )

        # --- RULE 2: Possible Sand / Silica / Industrial Filler Contamination ---
        # Low protein + high fiber + rough gritty texture or visible particles
        if fiber > 18.0 and crude_protein < 16.0:
            risk_points += 35
            flagged_hazards.append("Possible Filler / Low-Grade Byproduct Contamination Risk")
            reasons.append(
                f"Elevated fiber ({fiber:.1f}%) paired with depressed protein ({crude_protein:.1f}%) suggests dilution with fibrous hulls, ground husks, or non-nutritive fillers."
            )

        # --- RULE 3: Visible Foreign Object / Physical Adulteration ---
        if has_particles and ("unusual" in c_desc or "rough" in t_desc):
            risk_points += 35
            flagged_hazards.append("Visible Foreign Particle Contamination Risk")
            reasons.append(
                "Unusual visual coloration combined with distinct foreign particles indicates potential physical contamination or debris."
            )
        elif has_particles:
            risk_points += 20
            flagged_hazards.append("Visible Inclusions Detected")
            reasons.append("Visual inclusions differing from regular feed grains were observed.")

        # --- RULE 4: Moisture Spoilage / Water Dilution Risk ---
        if feed_type != "Silage":
            if moisture > 15.0 and ("sour" in s_desc or "fungal" in s_desc):
                risk_points += 30
                flagged_hazards.append("Moisture Dilution & Fermentative Spoilage Risk")
                reasons.append(
                    f"Dangerous moisture level ({moisture:.1f}%) combined with {smell_desc.lower()} odor creates severe mold and mycotoxin hazard."
                )
            elif moisture > 13.5:
                risk_points += 15
                reasons.append(f"Moisture ({moisture:.1f}%) is higher than safe dry storage limits (max 12%).")

        # --- RULE 5: Abnormal Sensory / Physical Markers ---
        if "white" in c_desc or "fungal" in s_desc:
            risk_points += 25
            flagged_hazards.append("Fungal / Mould Contamination Warning")
            reasons.append("Sensory and visual cues suggest fungal mycelium or spore formation.")

        if "unusual" in c_desc and "unusual" in s_desc:
            risk_points += 25
            reasons.append("Simultaneous abnormal discoloration and irregular odor indicate degraded batch quality.")

        # --- ML Classifier Cross-Validation ---
        ml_prediction = "Low"
        if self._ml_model is not None:
            feat = np.array([[
                crude_protein,
                moisture,
                fiber,
                1 if "powdery" in t_desc else 0,
                1 if "unusual" in c_desc else 0,
                1 if ("fungal" in s_desc or "sour" in s_desc) else 0,
                1 if has_particles else 0
            ]])
            pred_idx = self._ml_model.predict(feat)[0]
            ml_prediction = ["Low", "Medium", "High"][pred_idx]
            if ml_prediction == "High" and risk_points < 35:
                risk_points = max(risk_points, 40)

        # Map to Risk Level
        if risk_points >= 40 or len(flagged_hazards) >= 2:
            adulteration_risk = "High"
        elif risk_points >= 20 or len(flagged_hazards) >= 1:
            adulteration_risk = "Medium"
        else:
            adulteration_risk = "Low"

        if not reasons:
            reasons.append("Nutrient parameters and physical characteristics align with standard non-adulterated feed.")

        # Recommended action
        if adulteration_risk == "High":
            rec_action = "Do NOT feed to livestock immediately. Quarantine the batch and send a sample for chemical laboratory verification."
        elif adulteration_risk == "Medium":
            rec_action = "Inspect feed thoroughly before feeding. Check for chemical odors, foreign stones, or clumped powder."
        else:
            rec_action = "Feed parameters appear within normal safe thresholds for general dairy feeding."

        clamped_score = min(100, max(0, risk_points))

        return {
            "adulteration_risk": adulteration_risk,
            "risk_level": adulteration_risk,
            "risk_score": clamped_score,
            "risk_score_points": clamped_score,
            "flagged_hazards": flagged_hazards,
            "reasons": reasons,
            "recommended_action": rec_action,
            "ml_validation_indicator": ml_prediction,
            "disclaimer": "This prototype provides AI-based visual assessment and risk prediction. Laboratory testing is recommended for chemical confirmation."
        }


# Singleton engine instance for simple import
_engine = AdulterationEngine()


def check_adulteration_risk(
    feed_type: str,
    color_desc: str,
    texture_desc: str,
    smell_desc: str,
    storage_condition: str,
    foreign_particles: Any,
    crude_protein: float,
    moisture: float,
    fiber: float,
    non_protein_nitrogen: Optional[float] = None,
    visual_powder_particles: Optional[float] = None
) -> Dict[str, Any]:
    """Convenience function calling the singleton AdulterationEngine."""
    return _engine.assess_adulteration_risk(
        feed_type=feed_type,
        color_desc=color_desc,
        texture_desc=texture_desc,
        smell_desc=smell_desc,
        storage_condition=storage_condition,
        foreign_particles=foreign_particles,
        crude_protein=crude_protein,
        moisture=moisture,
        fiber=fiber,
        non_protein_nitrogen=non_protein_nitrogen,
        visual_powder_particles=visual_powder_particles
    )


def calculate_safe_urea_dosage(
    mode: str = "straw_treatment",
    quantity_kg: float = 100.0,
    num_animals: int = 1,
    language: str = "en"
) -> Dict[str, Any]:
    """
    Computes scientifically calibrated safe urea treatment and feeding dosages
    grounded in ICAR (Indian Council of Agricultural Research) & NDDB guidelines.

    Supports two modes:
    1. 'straw_treatment': Urea ammoniation of dry paddy/wheat straw (4% Urea + 45% Water w/w).
    2. 'concentrate_mix': Safe non-protein nitrogen inclusion in daily dairy concentrate rations (max 1% dry matter, 50-80g/cow/day).
    """
    qty = max(1.0, float(quantity_kg))
    animals = max(1, int(num_animals))
    lang = (language or "en").lower()

    if mode == "straw_treatment":
        safe_urea_kg = round(qty * 0.04, 2)
        safe_water_l = round(qty * 0.45, 1)
        curing_days = 21
        curing_range = "21–28 Days"
        cp_boost = "+5.0% CP (3.5% → 8.5%)"
        tdn_boost = "+10% to +15% Digestibility"

        steps = [
            {
                "en": f"Dissolve exactly {safe_urea_kg} kg of fertilizer/feed-grade urea in {safe_water_l} Liters of clean water in a drum until fully dissolved.",
                "te": f"{qty:.0f} కేజీల ఎండుగడ్డి కోసం {safe_urea_kg} కేజీల యూరియాను {safe_water_l} లీటర్ల శుభ్రమైన నీటిలో గడ్డలు లేకుండా పూర్తిగా కరిగించండి.",
                "hi": f"{qty:.0f} किग्रा सूखे चारे के लिए {safe_urea_kg} किग्रा यूरिया को {safe_water_l} लीटर पानी में अच्छी तरह घोलें।"
            },
            {
                "en": "Spread a 10–15 cm layer of dry straw on a clean elevated ground or polythene sheet.",
                "te": "ఎత్తైన, శుభ్రమైన నేలపై లేదా ప్లాస్టిక్ పట్టాపై ఎండుగడ్డిని 10–15 సెం.మీ మందంతో సమానంగా పరచండి.",
                "hi": "साफ जमीन या तिरपाल पर 10–15 सेमी मोटी सूखे पुआल की परत बिछाएं।"
            },
            {
                "en": "Sprinkle the urea solution uniformly across the straw layer using a garden rose sprinkler or perforated container.",
                "te": "కరిగించిన యూరియా ద్రావణాన్ని జల్లెడ డబ్బా లేదా స్ప్రేయర్‌తో గడ్డిపై సమానంగా చిలకరించండి.",
                "hi": "हजारे या मग की मदद से यूरिया के घोल को पुआल की परत पर समान रूप से छिड़कें।"
            },
            {
                "en": "Trample firmly to expel air pockets, repeat layering straw and urea solution until the stack is finished.",
                "te": "గాలి బుడగలు పోయేలా కాళ్ళతో బాగా తొక్కి, ఇదే విధంగా ఒకదానిపై ఒకటి పొరలుగా పేర్చుతూ మొత్తం గడ్డిని పూర్తి చేయండి.",
                "hi": "पैरों से दबाकर हवा निकालें और इसी तरह परत-दर-परत सारा पुआल ढेर बनाएं।"
            },
            {
                "en": "Cover the entire stack airtight with a heavy black polythene sheet. Weigh down edges with soil or stones for 21 days (summer) or 28 days (winter).",
                "te": "మొత్తం గడ్డి కుప్పపై నల్లటి ప్లాస్టిక్ పట్టా వేసి, గాలి చొరబడకుండా అంచులను మట్టి లేదా రాళ్ళతో గట్టిగా మూసివేసి 21 నుండి 28 రోజులు నిల్వ ఉంచండి.",
                "hi": "पॉलीथीन शीट से ढेर को हवा-बंद ढकें और किनारों पर मिट्टी रखें। 21 से 28 दिनों तक बंद रखें।"
            },
            {
                "en": "AERATION MANDATORY: Take out the daily needed quantity and spread in open shade for 20–30 minutes before feeding so pungent ammonia fumes dissipate.",
                "te": "ముఖ్యమైన నిబంధన: గడ్డిని బయటకు తీసిన తర్వాత 20-30 నిమిషాలు నీడలో ఆరబెట్టాలి. ఘాటైన అమ్మోనియా వాయువు పోయిన తర్వాతే పశువులకు వేయాలి.",
                "hi": "अनिवार्य नियम: खिलाने से पहले 20–30 मिनट छाया में फैलाएं ताकि अमोनिया की तेज गंध निकल जाए।"
            }
        ]

        summary_texts = {
            "en": f"For {qty:.0f} kg dry straw, mix {safe_urea_kg} kg Urea in {safe_water_l} Liters of water (4% ICAR standard). Seal airtight for 21–28 days. Increases Crude Protein from 3.5% to 8.5%.",
            "te": f"{qty:.0f} కేజీల ఎండుగడ్డి శుద్ధికి {safe_urea_kg} కేజీల యూరియాను {safe_water_l} లీటర్ల నీటిలో కలపాలి (ICAR 4% ప్రమాణం). 21-28 రోజులు గాలి తగలకుండా ఉంచితే ప్రోటీన్ 3.5% నుండి 8.5% కి పెరుగుతుంది.",
            "hi": f"{qty:.0f} किग्रा सूखे चारे के उपचार के लिए {safe_urea_kg} किग्रा यूरिया को {safe_water_l} लीटर पानी में मिलाएं। 21–28 दिन ढक कर रखें। कच्चा प्रोटीन 3.5% से बढ़कर 8.5% हो जाएगा।"
        }

        return {
            "status": "success",
            "mode": "straw_treatment",
            "mode_label": "Urea Straw Treatment (4% ICAR Standard)",
            "mode_label_te": "యూరియా గడ్డి శుద్ధి (ICAR 4% ప్రామాణిక పద్ధతి)",
            "mode_label_hi": "यूरिया पुआल उपचार (ICAR 4% मानक)",
            "quantity_kg": qty,
            "num_animals": animals,
            "safe_urea_kg": safe_urea_kg,
            "safe_urea_display": f"{safe_urea_kg} kg",
            "required_water_liters": safe_water_l,
            "required_water_display": f"{safe_water_l} L",
            "curing_days": curing_days,
            "curing_days_range": curing_range,
            "crude_protein_boost": cp_boost,
            "digestibility_boost": tdn_boost,
            "summary": summary_texts.get(lang, summary_texts["en"]),
            "steps": [s.get(lang, s["en"]) for s in steps],
            "precautions": [
                "Never feed freshly opened treated straw directly; always aerate 20-30 minutes.",
                "Do not use wet or already mouldy straw for treatment.",
                "Ensure strict airtight sealing during the 21-day curing window."
            ],
            "precautions_te": [
                "శుద్ధి చేసిన గడ్డిని తీసిన వెంటనే పశువులకు వేయరాదు; 20-30 నిమిషాలు ఆరబెట్టాలి.",
                "ఇప్పటికే బూజు పట్టిన లేదా తడిసిన గడ్డిని శుద్ధి చేయకూడదు.",
                "21 రోజుల పాటు గాలి చొరబడకుండా ప్లాస్టిక్ పట్టాను పక్కాగా మూసి ఉంచాలి."
            ],
            "precautions_hi": [
                "उपचारित पुआल को तुरंत न खिलाएं; 20-30 मिनट हवा में सुखाएं।",
                "फफूंद लगे या सड़े हुए पुआल का उपयोग न करें।",
                "21 दिनों तक पूरी तरह वायुरोधी (airtight) रखें।"
            ],
            "antidote_guide": {
                "en": "Emergency Antidote: If accidental poisoning occurs, drench with 2–3 Liters of Vinegar (5% acetic acid) mixed with cold water immediately.",
                "te": "అత్యవసర విరుగుడు: పొరపాటున విషప్రభావం (కడుపుబ్బరం/నురుగులు) వస్తే వెంటనే 2-3 లీటర్ల వెనిగర్ (Vinegar) ను చల్లని నీటిలో కలిపి తాగించాలి.",
                "hi": "आपातकालीन तोड़: यदि यूरिया विषाक्तता के लक्षण दिखें, तो तुरंत 2-3 लीटर सिरका (Vinegar) ठंडे पानी में मिलाकर पिलाएं।"
            }
        }

    else:
        max_daily_per_cow_g = 70.0
        safe_total_g = min(animals * max_daily_per_cow_g, qty * 15.0)
        per_cow_g = safe_total_g / animals

        summary_texts = {
            "en": f"For {qty:.1f} kg concentrate shared across {animals} cattle, safely mix at most {safe_total_g:.0f} grams Urea ({per_cow_g:.0f}g per cow/day). Never exceed 100g per cow.",
            "te": f"{animals} పశువుల కోసం {qty:.1f} కేజీల దాణాలో గరిష్టంగా {safe_total_g:.0f} గ్రాముల యూరియా (పశువుకు రోజుకు {per_cow_g:.0f} గ్రాములు) మాత్రమే కలపాలి. 100 గ్రాములకు ఎట్టి పరిస్థితుల్లోనూ మించరాదు.",
            "hi": f"{animals} मवेशियों के लिए {qty:.1f} किग्रा दाने में अधिकतम {safe_total_g:.0f} ग्राम यूरिया (प्रति गाय {per_cow_g:.0f} ग्राम/दिन) मिलाएं। कभी भी 100 ग्राम से अधिक न दें।"
        }

        return {
            "status": "success",
            "mode": "concentrate_mix",
            "mode_label": "Concentrate Ration Mixing (Max 1% Dry Matter Limit)",
            "mode_label_te": "రోజువారీ దాణాలో సురక్షిత యూరియా మిక్సింగ్ (గరిష్టంగా 1% పరిమితి)",
            "mode_label_hi": "दैनिक दाना मिश्रण (अधिकतम 1% सीमा)",
            "quantity_kg": qty,
            "num_animals": animals,
            "safe_urea_kg": round(safe_total_g / 1000.0, 3),
            "safe_urea_display": f"{safe_total_g:.0f} grams" if safe_total_g < 1000 else f"{(safe_total_g/1000):.2f} kg",
            "per_animal_display": f"{per_cow_g:.0f} g / animal / day",
            "required_water_liters": 0.0,
            "required_water_display": "Mix dry / with molasses",
            "curing_days": 0,
            "curing_days_range": "Immediate / Daily Mix",
            "crude_protein_boost": "Supplies non-protein nitrogen for rumen microbial synthesis",
            "digestibility_boost": "Optimizes rumen fiber fermentation",
            "summary": summary_texts.get(lang, summary_texts["en"]),
            "precautions": [
                "CRITICAL: STRICTLY ZERO UREA FOR CALVES UNDER 6 MONTHS (causes fatal ammonia poisoning).",
                "NEVER dissolve urea in cattle drinking water.",
                "Mix thoroughly with molasses, cereal grains, or bran to prevent pure urea clumps.",
                "Introduce gradually over 10-14 days starting with 1/3rd dose so rumen microbes adapt.",
                "Absolute maximum safety ceiling is 100g per adult animal per day."
            ],
            "precautions_te": [
                "తీవ్రమైన హెచ్చరిక: 6 నెలల లోపు లేగదూడలకు యూరియా అస్సలు పెట్టకూడదు (తక్షణం ప్రాణాలు కోల్పోతాయి).",
                "తాగునీటిలో యూరియాను ఎప్పుడూ కలపరాదు.",
                "యూరియా గడ్డలు కట్టకుండా బెల్లం పాకం లేదా తవుడుతో సమానంగా కలపాలి.",
                "మొదటి 10-14 రోజులు తక్కువ మోతాదుతో ప్రారంభించి క్రమంగా పెంచాలి.",
                "ఒక పశువుకు రోజుకు 100 గ్రాములకు మించి ఎట్టి పరిస్థితుల్లోనూ ఇవ్వకూడదు."
            ],
            "precautions_hi": [
                "गंभीर चेतावनी: 6 महीने से छोटे बछड़ों को यूरिया बिल्कुल न दें (जानलेवा अमोनिया विषाक्तता होती है)।",
                "पीने के पानी में यूरिया कभी न घोलें।",
                "शीरे (molasses) या चोकर में अच्छी तरह मिलाएं ताकि गांठें न रहें।",
                "शुरुआत में 10-14 दिनों तक 1/3 मात्रा देकर आदत डालें।",
                "किसी भी परिस्थिति में वयस्क पशु को 100 ग्राम/दिन से अधिक न दें।"
            ],
            "antidote_guide": {
                "en": "EMERGENCY ANTIDOTE: If bloat, muscle tremors, or frothing occurs, immediately drench with 2–3 Liters of Vinegar (5% acetic acid) mixed with 2-3 Liters of cold water.",
                "te": "అత్యవసర ప్రాణరక్షక విరుగుడు: కడుపుబ్బరం, నోటిలో నురుగులు, నడవలేకపోవడం వంటి లక్షణాలు కనిపిస్తే వెంటనే 2-3 లీటర్ల వెనిగర్ (Vinegar) ను చల్లని నీటిలో కలిపి తాగించాలి.",
                "hi": "आपातकालीन विष-निवारक: यदि पेट फूलना, मुंह से झाग या कंपन हो, तो तुरंत 2-3 लीटर सिरका (Vinegar) ठंडे पानी में मिलाकर पिलाएं।"
            }
        }

