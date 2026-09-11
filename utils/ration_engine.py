"""
SmartFeed AI - Scientific Animal Ration & Feed Suitability Engine
Calculates animal-specific feeding guidance based on ICAR (Indian Council of Agricultural Research)
and NDDB (National Dairy Development Board) dairy cattle nutritional guidelines.

Converts feed quality diagnostics (Health Score, Moisture, Protein, Urea, Mould)
into personalized, actionable feeding dosages, balanced roughage pairings, and adaptation protocols.
"""

from typing import Dict, Any, Optional, List


def calculate_animal_feed_recommendation(
    feed_diagnostics: Dict[str, Any],
    animal_params: Dict[str, Any],
    language: str = "te"
) -> Dict[str, Any]:
    """
    Computes precise feeding recommendation for a specific animal based on feed quality.
    
    Args:
        feed_diagnostics:
            - sample_type: str (e.g. 'Cattle Feed Pellet', 'Maize Silage', 'Cottonseed Cake', etc.)
            - health_score: float (0 - 100)
            - overall_risk: str ('Low', 'Medium', 'High')
            - mould_risk: str ('Low', 'Medium', 'High')
            - adulteration_risk: str ('Low', 'Medium', 'High')
            - crude_protein: float (percentage)
            - moisture: float (percentage)
            - shelf_life_days: int
        animal_params:
            - animal_type: str ('Cow' / 'Buffalo')
            - lactation_stage: str ('Lactating' / 'Pregnant' / 'Dry')
            - milk_yield_litres: float (0.0 to 35.0)
            - body_weight_kg: Optional[float]
            - animal_name: Optional[str]
        language: 'te', 'hi', or 'en'
        
    Returns:
        Structured recommendation dictionary.
    """
    # 1. Normalize animal inputs
    animal_type = str(animal_params.get("animal_type") or "Cow").strip().capitalize()
    if "buff" in animal_type.lower() or "గేదె" in animal_type or "भैंस" in animal_type:
        animal_type = "Buffalo"
    else:
        animal_type = "Cow"

    lactation_stage = str(animal_params.get("lactation_stage") or "Lactating").strip().capitalize()
    if "preg" in lactation_stage.lower() or "చూడి" in lactation_stage or "गर्भवती" in lactation_stage:
        lactation_stage = "Pregnant"
    elif "dry" in lactation_stage.lower() or "ఎండిన" in lactation_stage or "सूखी" in lactation_stage:
        lactation_stage = "Dry"
    else:
        lactation_stage = "Lactating"

    try:
        raw_yield = float(animal_params.get("milk_yield_litres", 8.0))
    except (ValueError, TypeError):
        raw_yield = 8.0
    
    # If Dry or Pregnant, milk yield is effectively 0
    milk_yield = 0.0 if lactation_stage in ["Pregnant", "Dry"] else max(0.0, min(raw_yield, 35.0))

    # Standard body weights if not specified (ICAR crossbred cow ~400kg, Murrah buffalo ~500kg)
    body_weight = float(animal_params.get("body_weight_kg") or (500.0 if animal_type == "Buffalo" else 400.0))

    # 2. Normalize feed diagnostics
    sample_type = str(feed_diagnostics.get("sample_type") or "Cattle Feed Pellet").strip()
    is_silage = "silage" in sample_type.lower()

    health_score = float(feed_diagnostics.get("health_score", 85.0))
    overall_risk = str(feed_diagnostics.get("overall_risk") or "Low").strip().capitalize()
    mould_risk = str(feed_diagnostics.get("mould_risk") or "Low").strip().capitalize()
    adulteration_risk = str(feed_diagnostics.get("adulteration_risk") or "Low").strip().capitalize()
    crude_protein = float(feed_diagnostics.get("crude_protein", 20.0))
    moisture = float(feed_diagnostics.get("moisture", 10.0))
    shelf_days = int(feed_diagnostics.get("shelf_life_days", 14))

    # 3. Determine Suitability Verdict
    # High risk or score < 50 or High mould/urea -> Strict Rejection
    is_unsafe = (
        health_score < 50.0 or
        overall_risk == "High" or
        mould_risk == "High" or
        adulteration_risk == "High" or
        shelf_days <= 0
    )
    is_caution = (
        not is_unsafe and (
            health_score < 80.0 or
            overall_risk == "Medium" or
            mould_risk == "Medium" or
            ((not is_silage and moisture > 14.0) or (is_silage and (moisture < 55.0 or moisture > 75.0))) or
            shelf_days <= 3
        )
    )

    if is_unsafe:
        suitability_code = "REJECTED_UNSAFE"
    elif is_caution:
        suitability_code = "CAUTION_CONDITIONAL"
    else:
        suitability_code = "SUITABLE"

    # 4. ICAR Scientific Ration Calculations
    # A. Dry Matter Intake (DMI): Cow ~2.5% BW, Buffalo ~3.0% BW
    dmi_pct = 0.030 if animal_type == "Buffalo" else 0.025
    total_dmi_kg = round(body_weight * dmi_pct, 1)

    # B. Daily Concentrate Requirement:
    # - Maintenance: Cow ~1.25 kg, Buffalo ~1.75 kg
    # - Milk Production: Cow 1 kg per 2.5 L milk, Buffalo 1 kg per 2.0 L milk (due to higher 6-8% fat)
    # - Pregnancy Allowance: +1.25 kg (last trimester growth & fetal development)
    maint_conc = 1.75 if animal_type == "Buffalo" else 1.25
    prod_ratio = 2.0 if animal_type == "Buffalo" else 2.5
    prod_conc = (milk_yield / prod_ratio) if lactation_stage == "Lactating" else 0.0
    preg_conc = 1.25 if lactation_stage == "Pregnant" else 0.0

    raw_concentrate_kg = maint_conc + prod_conc + preg_conc

    # If the tested feed is Silage (roughage/succulent)
    if is_silage:
        # Silage standard allowance: 18 - 25 kg/day fresh silage
        if lactation_stage == "Lactating":
            recommended_feed_kg = 22.0 if animal_type == "Buffalo" else 18.0
        elif lactation_stage == "Pregnant":
            recommended_feed_kg = 18.0 if animal_type == "Buffalo" else 15.0
        else: # Dry
            recommended_feed_kg = 14.0 if animal_type == "Buffalo" else 12.0
        
        feed_unit = "kg/day"
        concentrate_companion_kg = round(raw_concentrate_kg, 1)
        green_fodder_kg = 8.0 # reduced because silage supplies succulent forage
        dry_straw_kg = 4.0 if animal_type == "Buffalo" else 3.5
    else:
        # Tested feed is concentrate / pellet / oilcake
        recommended_feed_kg = round(raw_concentrate_kg, 1)
        feed_unit = "kg/day"
        concentrate_companion_kg = recommended_feed_kg
        green_fodder_kg = 24.0 if animal_type == "Buffalo" else 20.0
        dry_straw_kg = 5.0 if animal_type == "Buffalo" else 4.0

    # If unsafe, recommended quantity is 0 kg!
    if suitability_code == "REJECTED_UNSAFE":
        recommended_feed_kg = 0.0
        morning_dose_kg = 0.0
        evening_dose_kg = 0.0
    elif suitability_code == "CAUTION_CONDITIONAL":
        # Recommend reduced feeding with strict dilution and observation
        recommended_feed_kg = round(recommended_feed_kg * 0.65, 1)
        morning_dose_kg = round(recommended_feed_kg * 0.5, 1)
        evening_dose_kg = round(recommended_feed_kg - morning_dose_kg, 1)
    else:
        morning_dose_kg = round(recommended_feed_kg * 0.5, 1)
        evening_dose_kg = round(recommended_feed_kg - morning_dose_kg, 1)

    # Mineral mixture and water
    if lactation_stage == "Lactating":
        mineral_mix_grams = 80 if animal_type == "Buffalo" else 60
        water_litres = int(body_weight * 0.10 + milk_yield * 2.5) # ~70 to 90 L
    elif lactation_stage == "Pregnant":
        mineral_mix_grams = 100 if animal_type == "Buffalo" else 80
        water_litres = int(body_weight * 0.10 + 15) # ~55 to 65 L
    else:
        mineral_mix_grams = 50
        water_litres = int(body_weight * 0.09) # ~40 to 50 L

    # 5. 4-Day Gradual Adaptation Schedule
    if suitability_code == "REJECTED_UNSAFE":
        transition_schedule = [
            {"day": 1, "pct_new": 0, "pct_old": 100, "dose_kg": 0.0, "desc_te": "మేత ఇవ్వవద్దు (వెంటనే వేరు చేయండి)", "desc_hi": "चारा न दें (तुरंत अलग करें)", "desc_en": "Do NOT feed. Quarantine batch immediately."},
            {"day": 2, "pct_new": 0, "pct_old": 100, "dose_kg": 0.0, "desc_te": "మేత ఇవ్వవద్దు (వెంటనే వేరు చేయండి)", "desc_hi": "चारा न दें (तुरंत अलग करें)", "desc_en": "Do NOT feed. Quarantine batch immediately."},
            {"day": 3, "pct_new": 0, "pct_old": 100, "dose_kg": 0.0, "desc_te": "మేత ఇవ్వవద్దు (వెంటనే వేరు చేయండి)", "desc_hi": "चारा न दें (तुरंत अलग करें)", "desc_en": "Do NOT feed. Quarantine batch immediately."},
            {"day": 4, "pct_new": 0, "pct_old": 100, "dose_kg": 0.0, "desc_te": "మేత ఇవ్వవద్దు (వెంటనే వేరు చేయండి)", "desc_hi": "चारा न दें (तुरंत अलग करें)", "desc_en": "Do NOT feed. Quarantine batch immediately."}
        ]
    else:
        transition_schedule = [
            {
                "day": 1,
                "pct_new": 25,
                "pct_old": 75,
                "dose_kg": round(recommended_feed_kg * 0.25, 1),
                "desc_te": "25% కొత్త మేత + 75% పాత మేత కలపండి (రెండు పూటలా విభజించి ఇవ్వండి)",
                "desc_hi": "25% नया चारा + 75% पुराना चारा मिलाकर दें",
                "desc_en": "25% new feed mixed with 75% familiar ration"
            },
            {
                "day": 2,
                "pct_new": 50,
                "pct_old": 50,
                "dose_kg": round(recommended_feed_kg * 0.50, 1),
                "desc_te": "50% కొత్త మేత + 50% పాత మేత కలపండి (నెమరు వేయడం గమనించండి)",
                "desc_hi": "50% नया चारा + 50% पुराना चारा मिलाकर दें (जुगाली पर ध्यान दें)",
                "desc_en": "50% new feed + 50% familiar ration (observe cudding)"
            },
            {
                "day": 3,
                "pct_new": 75,
                "pct_old": 25,
                "dose_kg": round(recommended_feed_kg * 0.75, 1),
                "desc_te": "75% కొత్త మేత + 25% పాత మేత కలపండి (మల విసర్జన తనిఖీ చేయండి)",
                "desc_hi": "75% नया चारा + 25% पुराना चारा मिलाकर दें (गोबर की जांच करें)",
                "desc_en": "75% new feed + 25% familiar ration (check dung consistency)"
            },
            {
                "day": 4,
                "pct_new": 100,
                "pct_old": 0,
                "dose_kg": round(recommended_feed_kg, 1),
                "desc_te": "100% పూర్తి సిఫార్సు మోతాదు ఇవ్వవచ్చు (పూర్తిగా అలవాటు పడింది)",
                "desc_hi": "100% पूरी अनुशंसित मात्रा दें (रूमेन पूरी तरह अनुकूलित)",
                "desc_en": "100% full recommended daily ration (rumen fully adapted)"
            }
        ]

    # 6. Multilingual Text Generation
    rec_texts = _generate_multilingual_recommendation(
        animal_type=animal_type,
        lactation_stage=lactation_stage,
        milk_yield=milk_yield,
        suitability_code=suitability_code,
        health_score=health_score,
        crude_protein=crude_protein,
        moisture=moisture,
        mould_risk=mould_risk,
        adulteration_risk=adulteration_risk,
        recommended_feed_kg=recommended_feed_kg,
        morning_dose_kg=morning_dose_kg,
        evening_dose_kg=evening_dose_kg,
        green_fodder_kg=green_fodder_kg,
        dry_straw_kg=dry_straw_kg,
        mineral_mix_grams=mineral_mix_grams,
        water_litres=water_litres,
        is_silage=is_silage,
        sample_type=sample_type
    )

    lang_data = rec_texts.get(language, rec_texts["te"])

    return {
        "status": "success",
        "animal_type": animal_type,
        "lactation_stage": lactation_stage,
        "milk_yield_litres": milk_yield,
        "body_weight_kg": body_weight,
        "suitability_code": suitability_code,
        "is_safe": suitability_code == "SUITABLE",
        "health_score": health_score,
        "recommended_feed_kg": recommended_feed_kg,
        "morning_dose_kg": morning_dose_kg,
        "evening_dose_kg": evening_dose_kg,
        "unit": feed_unit,
        "total_dmi_kg": total_dmi_kg,
        "balanced_ration": {
            "tested_feed_kg": recommended_feed_kg,
            "green_fodder_kg": green_fodder_kg,
            "dry_straw_kg": dry_straw_kg,
            "mineral_mixture_grams": mineral_mix_grams,
            "clean_water_litres": water_litres
        },
        "transition_schedule": transition_schedule,
        "verdict_badge": lang_data["verdict_badge"],
        "headline": lang_data["headline"],
        "suitability_note": lang_data["suitability_note"],
        "dosage_summary": lang_data["dosage_summary"],
        "stage_clinical_note": lang_data["stage_clinical_note"],
        "monitoring_caution": lang_data["monitoring_caution"],
        "voice_script": lang_data["voice_script"],
        "all_languages": rec_texts
    }


def _generate_multilingual_recommendation(
    animal_type: str,
    lactation_stage: str,
    milk_yield: float,
    suitability_code: str,
    health_score: float,
    crude_protein: float,
    moisture: float,
    mould_risk: str,
    adulteration_risk: str,
    recommended_feed_kg: float,
    morning_dose_kg: float,
    evening_dose_kg: float,
    green_fodder_kg: float,
    dry_straw_kg: float,
    mineral_mix_grams: int,
    water_litres: int,
    is_silage: bool,
    sample_type: str
) -> Dict[str, Dict[str, str]]:
    """Builds comprehensive localized narratives for Telugu, Hindi, and English."""

    type_names = {
        "Cow": {"te": "ఆవు", "hi": "गाय", "en": "Cow"},
        "Buffalo": {"te": "గేదె", "hi": "भैंस", "en": "Buffalo"}
    }
    stage_names = {
        "Lactating": {"te": "పాలిచ్చే", "hi": "दूध देने वाली", "en": "Lactating"},
        "Pregnant": {"te": "చూడి / గర్భస్థ", "hi": "गर्भवती / गाभिन", "en": "Pregnant"},
        "Dry": {"te": "ఎండిన (ఈత ఆగిన)", "hi": "सूखी (ड्राई)", "en": "Dry (Non-lactating)"}
    }

    t_te = type_names[animal_type]["te"]
    s_te = stage_names[lactation_stage]["te"]
    t_hi = type_names[animal_type]["hi"]
    s_hi = stage_names[lactation_stage]["hi"]
    t_en = type_names[animal_type]["en"]
    s_en = stage_names[lactation_stage]["en"]

    if suitability_code == "REJECTED_UNSAFE":
        if lactation_stage == "Pregnant":
            stage_te_warn = "గర్భస్థ పశువులకు బూజు / రసాయన మేత ఇవ్వడం వల్ల గర్భస్రావం (Abortion) జరిగే తీవ్ర ప్రమాదం ఉంది. పిండం రక్షణ కోసం ఈ మేతను అస్సలు వాడవద్దు."
            stage_hi_warn = "गर्भवती पशुओं को फफूंद या रसायन युक्त चारा देने से गर्भपात (Abortion) का भारी खतरा होता है। इसे बिल्कुल न खिलाएं।"
            stage_en_warn = "CRITICAL: Severe risk of mycotoxin-induced abortion and placental damage in pregnant cattle. Do NOT feed this batch."
        elif lactation_stage == "Lactating":
            stage_te_warn = "పాలిచ్చే పశువులకు ఇవ్వడం వల్ల పాల దిగుబడి ఒక్కసారిగా పడిపోవడమే కాకుండా, పాలలో టాక్సిన్స్ చేరి దూడలకు మరియు తాగే మనుషులకు విషతుల్యం కావచ్చు."
            stage_hi_warn = "दूध देने वाले पशुओं को खिलाने से दूध में भारी गिरावट आ सकती है और दूध में विषाक्त पदार्थ पहुंच सकते हैं।"
            stage_en_warn = "Ingestion by lactating cattle causes rapid drop in milk yield, rumen toxicity, and harmful mycotoxin excretion into milk."
        else:
            stage_te_warn = "తీవ్రమైన జీర్ణకోశ సమస్యలు, డయేరియా మరియు కాలేయ వ్యాధులు కలిగించే ప్రమాదం ఉంది."
            stage_hi_warn = "गंभीर पाचन संबंधी विकार, अपच और यकृत संक्रमण का खतरा है।"
            stage_en_warn = "Severe risk of rumen acidosis, enteritis, and liver pathology."

        te = {
            "verdict_badge": "🔴 రద్దు చేయబడింది - పశువులకు ఇవ్వవద్దు (UNSAFE)",
            "headline": f"❌ ఈ మేత మీ {s_te} {t_te}కి అస్సలు అనుకూలమైనది కాదు!",
            "suitability_note": f"ఆరోగ్య స్కోర్ కేవలం {round(health_score)}/100 మాత్రమే ఉంది. బూజు ({mould_risk}) లేదా కల్తీ ({adulteration_risk}) రిస్క్ ఎక్కువగా ఉన్నందున పశువుల ఆరోగ్యం దెబ్బతింటుంది.",
            "dosage_summary": "సిఫార్సు మోతాదు: 0 కిలోలు (వెంటనే ఈ మేతను వేరు చేయండి)",
            "stage_clinical_note": stage_te_warn,
            "monitoring_caution": "⚠️ ఈ బ్యాచ్‌ను పశువులు ముట్టుకోకుండా దూరంగా ఉంచండి. స్థానిక పశువైద్యులను లేదా మేత సరఫరాదారుని సంప్రదించండి.",
            "voice_script": f"హెచ్చరిక: ఈ మేత మీ {s_te} {t_te}కి సురక్షితమైనది కాదు. ఆరోగ్య స్కోర్ చాలా తక్కువగా ఉంది. పశువులకు అస్సలు పెట్టవద్దు."
        }

        hi = {
            "verdict_badge": "🔴 असुरक्षित - पशुओं को न खिलाएं (UNSAFE)",
            "headline": f"❌ यह चारा आपकी {s_hi} {t_hi} के लिए बिल्कुल उपयुक्त नहीं है!",
            "suitability_note": f"हेल्थ स्कोर केवल {round(health_score)}/100 है। फफूंद ({mould_risk}) या मिलावट ({adulteration_risk}) के कारण मवेशी गंभीर रूप से बीमार हो सकते हैं।",
            "dosage_summary": "अनुशंसित खुराक: 0 किग्रा (इस चारे को तुरंत अलग करें)",
            "stage_clinical_note": stage_hi_warn,
            "monitoring_caution": "⚠️ इस चारे को पशुओं की पहुंच से दूर रखें और स्थानीय पशु चिकित्सक से सलाह लें।",
            "voice_script": f"चेतावनी: यह चारा आपकी {s_hi} {t_hi} के लिए सुरक्षित नहीं है। स्वास्थ्य स्कोर बहुत कम है। कृपया इसे न खिलाएं।"
        }

        en = {
            "verdict_badge": "🔴 REJECTED - DO NOT FEED (UNSAFE)",
            "headline": f"❌ This feed is UNSUITABLE for your {s_en} {t_en}!",
            "suitability_note": f"Health score is only {round(health_score)}/100 with elevated {mould_risk} mould risk / {adulteration_risk} chemical risk.",
            "dosage_summary": "Recommended Dosage: 0 kg/day (Quarantine this batch immediately)",
            "stage_clinical_note": stage_en_warn,
            "monitoring_caution": "⚠️ Keep cattle away from this batch. Consult your veterinary officer or feed supplier.",
            "voice_script": f"Critical warning: This feed is unsafe for your {s_en} {t_en}. Health score is too low. Do not feed."
        }

    elif suitability_code == "CAUTION_CONDITIONAL":
        if lactation_stage == "Pregnant":
            stage_te_warn = "చూడి పశువులకు ఇచ్చేటప్పుడు అత్యంత జాగ్రత్త వహించండి. కాస్త బూజు లేదా తేమ ఉన్నా మేతను ఎండబెట్టిన తర్వాతే ఇవ్వాలి."
            stage_hi_warn = "गाभिन पशुओं को देते समय बहुत सतर्क रहें। धूप में सुखाने के बाद ही सीमित मात्रा में दें।"
            stage_en_warn = "Feed with extreme caution to pregnant cattle. Sun-dry thoroughly before offering any portion."
        elif lactation_stage == "Lactating":
            stage_te_warn = "పాల దిగుబడి తగ్గకుండా ఉండటానికి, మేతతో పాటు ఎండుగడ్డి తప్పనిసరిగా సమృద్ధిగా ఇవ్వండి. జీర్ణక్రియను నిశితంగా గమనించండి."
            stage_hi_warn = "दूध उत्पादन बनाए रखने के लिए सूखे चारे के साथ मिलाकर दें और जुगाली पर नजर रखें।"
            stage_en_warn = "Mix thoroughly with dry straw to buffer rumen pH and prevent drop in butterfat percentage."
        else:
            stage_te_warn = "పరిమిత మోతాదులో మాత్రమే ఇవ్వండి, పశువుల మల విసర్జన మరియు నెమరు వేయడాన్ని గమనించండి."
            stage_hi_warn = "सीमित मात्रा में दें और पशु के स्वास्थ्य की निगरानी करें।"
            stage_en_warn = "Feed in reduced quantities and closely monitor rumination."

        te = {
            "verdict_badge": "🟡 జాగ్రత్త - నిబంధనలతో కూడిన మేత (CAUTION)",
            "headline": f"⚠️ మీ {s_te} {t_te}కి జాగ్రత్తగా పరిశీలిస్తూ పరిమితంగా ఇవ్వవచ్చు",
            "suitability_note": f"నాణ్యత స్కోర్ {round(health_score)}/100. తేమ లేదా నిల్వ ప్రభావం ఉంది. మేతను ముందుగా శుభ్రమైన టార్పాలిన్‌పై ఆరబెట్టి ఆ తర్వాతే ఇవ్వండి.",
            "dosage_summary": f"పరిమిత మోతాదు: రోజుకు {recommended_feed_kg} కిలోలు (ఉదయం {morning_dose_kg} kg, సాయంత్రం {evening_dose_kg} kg)",
            "stage_clinical_note": stage_te_warn,
            "monitoring_caution": "⚠️ నేరుగా పూర్తి మోతాదు ఇవ్వవద్దు. పాత మేతతో కలిపి 4 రోజుల వ్యవధిలో నెమ్మదిగా అలవాటు చేయండి.",
            "voice_script": f"జాగ్రత్త: ఈ మేత మీ {s_te} {t_te}కి పరిమితంగా మాత్రమే అనుకూలమైనది. రోజుకు {recommended_feed_kg} కిలోలు, ఎండబెట్టిన తర్వాత మాత్రమే విభజించి ఇవ్వండి."
        }

        hi = {
            "verdict_badge": "🟡 सावधानी - सीमित उपयोग (CAUTION)",
            "headline": f"⚠️ आपकी {s_hi} {t_hi} के लिए सावधानीपूर्वक और सीमित मात्रा में उपयुक्त",
            "suitability_note": f"स्वास्थ्य स्कोर {round(health_score)}/100 है। चारे को धूप में सुखाकर साफ करने के बाद ही सीमित मात्रा में खिलाएं।",
            "dosage_summary": f"सीमित दैनिक खुराक: {recommended_feed_kg} किग्रा (सुबह {morning_dose_kg} किग्रा, शाम {evening_dose_kg} किग्रा)",
            "stage_clinical_note": stage_hi_warn,
            "monitoring_caution": "⚠️ एकदम से पूरा चारा न बदलें। पुराने चारे के साथ मिलाकर 4 दिनों में धीरे-धीरे आदत डालें।",
            "voice_script": f"सावधानी: यह चारा आपकी {s_hi} {t_hi} के लिए सीमित मात्रा में उपयुक्त है। दैनिक खुराक {recommended_feed_kg} किग्रा है।"
        }

        en = {
            "verdict_badge": "🟡 CAUTION - CONDITIONAL FEEDING",
            "headline": f"⚠️ Conditional Suitability for your {s_en} {t_en}",
            "suitability_note": f"Health score is {round(health_score)}/100. Sun-dry the feed on a tarpaulin to eliminate residual moisture before serving.",
            "dosage_summary": f"Controlled Dosage: {recommended_feed_kg} kg/day (Morning: {morning_dose_kg} kg, Evening: {evening_dose_kg} kg)",
            "stage_clinical_note": stage_en_warn,
            "monitoring_caution": "⚠️ Do not switch abruptly. Follow the 4-day gradual rumen adaptation protocol.",
            "voice_script": f"Caution: This feed has minor quality warnings. Recommended ration is {recommended_feed_kg} kg per day after sun-drying."
        }

    else:
        if lactation_stage == "Lactating":
            stage_te_detail = f"రోజుకు {milk_yield} లీటర్ల పాల ఉత్పత్తికి ఈ మేత ఉత్తమ పోషణను అందిస్తుంది. పాల వెన్న శాతం (Fat %) మరియు SNF స్థిరంగా ఉంటాయి."
            stage_hi_detail = f"दैनिक {milk_yield} लीटर दूध उत्पादन के लिए यह चारा उत्कृष्ट पोषण प्रदान करता है। वसा और एसएनएफ बना रहेगा।"
            stage_en_detail = f"Provides balanced nutrition for your daily target of {milk_yield} Litres milk yield, stabilizing milk fat and SNF."
        elif lactation_stage == "Pregnant":
            stage_te_detail = "గర్భంలో దూడ ఎదుగుదలకు మరియు ఈత తర్వాత తగినంత పాల ఉత్పత్తికి ఇది శ్రేష్టమైనది. ఖనిజ లవణాల మిశ్రమం తప్పనిసరిగా కలపండి."
            stage_hi_detail = "गर्भ में बछड़े के विकास और प्रसव बाद अच्छे दूध उत्पादन के लिए यह पौष्टिक है। खनिज मिश्रण अवश्य दें।"
            stage_en_detail = "Supports healthy fetal development in the final trimester and prepares the mammary glands for upcoming lactation."
        else: # Dry
            stage_te_detail = "ఈత ఆగిన పశువుల శరీర బరువు మరియు జీర్ణశక్తిని సరైన స్థితిలో ఉంచడానికి ఇది సమతుల్యమైనది."
            stage_hi_detail = "सूखे पशुओं के शारीरिक रखरखाव और पाचन तंत्र को स्वस्थ रखने के लिए उपयुक्त है।"
            stage_en_detail = "Maintains optimal body condition score without excessive fattening during the dry rest period."

        te = {
            "verdict_badge": "✅ మేత చాలా అనుకూలమైనది (SUITABLE)",
            "headline": f"✅ ఈ మేత మీ {s_te} {t_te}కి చాలా అనుకూలమైనది మరియు సురక్షితం!",
            "suitability_note": f"ఆరోగ్య స్కోర్ {round(health_score)}/100 (ఉత్తమం). క్రూడ్ ప్రోటీన్ {crude_protein}% మరియు తేమ {moisture}% సరైన స్థాయిలో ఉన్నాయి. ఎలాంటి కల్తీ లేదు.",
            "dosage_summary": f"సిఫార్సు మోతాదు: రోజుకు {recommended_feed_kg} కిలోలు (ఉదయం {morning_dose_kg} kg, సాయంత్రం {evening_dose_kg} kg)",
            "stage_clinical_note": stage_te_detail,
            "monitoring_caution": "⚠️ పశువుల కడుపులోని రూమెన్ బ్యాక్టీరియా దెబ్బతినకుండా ఉండటానికి, 4 రోజుల వ్యవధిలో పాత మేతతో కలుపుతూ క్రమంగా మార్చండి.",
            "voice_script": f"ఈ మేత మీ {s_te} {t_te}కి చాలా అనుకూలమైనది. రోజుకు {recommended_feed_kg} కిలోలు ఇవ్వండి, ఉదయం {morning_dose_kg} కిలోలు మరియు సాయంత్రం {evening_dose_kg} కిలోలు. దీంతో పాటు {green_fodder_kg} కిలోల పచ్చిగడ్డి, {dry_straw_kg} కిలోల ఎండుగడ్డి ఇవ్వండి. క్రమంగా 4 రోజుల్లో అలవాటు చేయండి."
        }

        hi = {
            "verdict_badge": "✅ चारा पूरी तरह उपयुक्त है (SUITABLE)",
            "headline": f"✅ यह चारा आपकी {s_hi} {t_hi} के लिए पूरी तरह उपयुक्त और सुरक्षित है!",
            "suitability_note": f"स्वास्थ्य स्कोर {round(health_score)}/100 (उत्कृष्ट)। क्रूड प्रोटीन {crude_protein}% और नमी {moisture}% संतुलित हैं। कोई मिलावट नहीं है।",
            "dosage_summary": f"अनुशंसित दैनिक मात्रा: {recommended_feed_kg} किग्रा (सुबह {morning_dose_kg} किग्रा, शाम {evening_dose_kg} किग्रा)",
            "stage_clinical_note": stage_hi_detail,
            "monitoring_caution": "⚠️ पाचन तंत्र (रूमेन) की सुरक्षा के लिए 4 दिनों में धीरे-धीरे आदत डालें।",
            "voice_script": f"यह चारा आपकी {s_hi} {t_hi} के लिए बहुत उपयुक्त है। दैनिक खुराक {recommended_feed_kg} किग्रा है। सुबह {morning_dose_kg} किग्रा और शाम {evening_dose_kg} किग्रा दें। 4 दिनों में धीरे-धीरे आदत डालें।"
        }

        en = {
            "verdict_badge": "✅ FEED IS SUITABLE & SAFE",
            "headline": f"✅ Excellent feed suitability for your {s_en} {t_en}!",
            "suitability_note": f"Health score is {round(health_score)}/100 (Optimal). Crude protein {crude_protein}% and moisture {moisture}% are well balanced with zero adulteration detected.",
            "dosage_summary": f"Recommended Quantity: {recommended_feed_kg} kg/day (Morning: {morning_dose_kg} kg, Evening: {evening_dose_kg} kg)",
            "stage_clinical_note": stage_en_detail,
            "monitoring_caution": "⚠️ Protect rumen microbes by transitioning gradually over 4 days (25% → 50% → 75% → 100%).",
            "voice_script": f"Feed is suitable for your {s_en} {t_en}. Recommended daily quantity is {recommended_feed_kg} kilograms, split into {morning_dose_kg} kg morning and {evening_dose_kg} kg evening. Pair with {green_fodder_kg} kg green fodder and {dry_straw_kg} kg dry straw. Introduce gradually over 4 days."
        }

    return {"te": te, "hi": hi, "en": en}
