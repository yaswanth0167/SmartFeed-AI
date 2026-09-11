"""
SmartFeed AI - Time-Based Smart Feeding Planner & Dairy Intelligence Engine
Calculates time-slotted daily feeding plans (Morning, Afternoon, Evening) for dairy cattle,
manages slot reminders, and computes milk production / rumen health correlation insights.
"""

import datetime
from typing import Dict, Any, List, Optional


def get_daily_time_slots_plan(
    animal_profile: Dict[str, Any],
    feed_diagnostics: Optional[Dict[str, Any]] = None,
    current_hour: Optional[int] = None,
    language: str = "te"
) -> Dict[str, Any]:
    """
    Computes a 3-slot daily feeding schedule (Morning, Afternoon, Evening)
    customized to the animal's species, lactation status, and milk yield.
    
    Args:
        animal_profile:
            - animal_type: 'Cow' or 'Buffalo'
            - lactation_status: 'Lactating', 'Pregnant', 'Dry'
            - milk_production: e.g. '8 Litres', '8', 8.0
            - animal_name: str
        feed_diagnostics: Optional quality scores from recent scan.
        current_hour: Hour of the day (0-23) for active slot & reminder calculation.
        language: 'te', 'hi', 'en'
    """
    if current_hour is None:
        current_hour = datetime.datetime.now().hour

    animal_type = str(animal_profile.get("animal_type") or "Cow").capitalize()
    is_buffalo = "buff" in animal_type.lower() or "గేదె" in animal_type or "भैंस" in animal_type
    species_key = "Buffalo" if is_buffalo else "Cow"

    status = str(animal_profile.get("lactation_status") or "Lactating").capitalize()
    if "preg" in status.lower() or "చూడి" in status or "गर्भवती" in status:
        stage_key = "Pregnant"
    elif "dry" in status.lower() or "ఎండిన" in status or "सूखी" in status:
        stage_key = "Dry"
    else:
        stage_key = "Lactating"

    # Extract numeric milk yield
    raw_milk = animal_profile.get("milk_production", 8.0)
    import re
    nums = re.findall(r'\d+(?:\.\d+)?', str(raw_milk))
    milk_yield = float(nums[0]) if nums else 8.0
    if stage_key in ["Pregnant", "Dry"]:
        milk_yield = 0.0

    # ICAR Benchmark Calculations
    # Concentrate requirement:
    maint_conc = 1.75 if is_buffalo else 1.25
    prod_ratio = 2.0 if is_buffalo else 2.5
    prod_conc = (milk_yield / prod_ratio) if stage_key == "Lactating" else 0.0
    preg_conc = 1.25 if stage_key == "Pregnant" else 0.0
    total_conc_kg = round(maint_conc + prod_conc + preg_conc, 1)

    # Roughage requirement:
    total_green_kg = 24.0 if is_buffalo else 20.0
    total_straw_kg = 5.0 if is_buffalo else 4.0
    mineral_mix_grams = 100 if stage_key == "Pregnant" else (80 if is_buffalo else 60)
    total_water_l = 80 if is_buffalo else 60

    # -------------------------------------------------------------
    # 3 Biological Time Slots Distribution
    # -------------------------------------------------------------
    # Slot 1: Morning (06:00 - 08:30 AM) -> Milking Concentrate + Early Green Fodder
    morn_conc = round(total_conc_kg * 0.5, 1)
    morn_green = round(total_green_kg * 0.45, 1)
    morn_water = int(total_water_l * 0.4)

    # Slot 2: Afternoon (01:00 - 02:30 PM) -> High Fiber Dry Straw for Rumen Cudding & Chew
    afternoon_straw = total_straw_kg
    afternoon_water = int(total_water_l * 0.3)

    # Slot 3: Evening (06:00 - 07:30 PM) -> Evening Milking Concentrate + Night Green Fodder + Minerals
    eve_conc = round(total_conc_kg - morn_conc, 1)
    eve_green = round(total_green_kg - morn_green, 1)
    eve_water = int(total_water_l - morn_water - afternoon_water)

    # Determine Active Slot and Next Reminder
    if current_hour < 11:
        active_slot = "morning"
        next_slot = "afternoon"
        reminder_time = "01:00 PM"
        reminder_desc_te = "మధ్యాహ్న సమయానికి ఎండుగడ్డి (Cudding Straw) మరియు తాగునీరు సిద్ధం చేయండి."
        reminder_desc_hi = "दोपहर के लिए सूखा भूसा (जुगाली हेतु) और ताजा पानी तैयार रखें।"
        reminder_desc_en = "Prepare afternoon dry straw for rumen cudding and clean water."
    elif current_hour < 16:
        active_slot = "afternoon"
        next_slot = "evening"
        reminder_time = "06:00 PM"
        reminder_desc_te = "సాయంత్రం పాలు పితికే సమయానికి దాణా మరియు ఖనిజ లవణాలు అందించండి."
        reminder_desc_hi = "शाम के दोहन समय के लिए दाना और खनिज मिश्रण तैयार रखें।"
        reminder_desc_en = "Prepare evening milking concentrate and mineral mixture."
    else:
        active_slot = "evening"
        next_slot = "morning"
        if language == "hi":
            reminder_time = "06:30 AM (कल)"
        elif language == "te":
            reminder_time = "06:30 AM (రేపు)"
        else:
            reminder_time = "06:30 AM (Tomorrow)"
        reminder_desc_te = "రేపు ఉదయపు మేతకు దాణా మరియు తాజా పచ్చిగడ్డి సిద్ధం చేసుకోండి."
        reminder_desc_hi = "कल सुबह के लिए दाना और ताजा हरा चारा तैयार रखें।"
        reminder_desc_en = "Prepare tomorrow morning milking concentrate and fresh green fodder."

    slots_data = [
        {
            "slot_key": "morning",
            "time_window": "06:00 AM – 08:30 AM",
            "title_te": "🌅 ఉదయపు మేత (దోహన సమయం)",
            "title_hi": "🌅 सुबह का चारा (दोहन खुराक)",
            "title_en": "🌅 Morning Milking Ration",
            "purpose_te": "ఉదయం పాలు పితికే సమయంలో శక్తినిచ్చి జీర్ణక్రియను ఉత్తేజితం చేస్తుంది.",
            "purpose_hi": "सुबह दूध दोहन के समय ऊर्जा और पाचन को सक्रिय करता है।",
            "purpose_en": "Boosts lactation energy during morning milking and stimulates digestion.",
            "suggested": {
                "feed_name": "Concentrate Feed + Fresh Green Fodder",
                "concentrate_kg": morn_conc,
                "green_fodder_kg": morn_green,
                "dry_straw_kg": 0.0,
                "water_litres": morn_water,
                "minerals_grams": 0.0,
                "target_milk_litres": round(milk_yield * 0.55, 1) if stage_key == "Lactating" else 0.0
            }
        },
        {
            "slot_key": "afternoon",
            "time_window": "01:00 PM – 02:30 PM",
            "title_te": "☀️ మధ్యాహ్న మేత (నెమరు వేత)",
            "title_hi": "☀️ दोपहर का चारा (जुगाली व पाचन)",
            "title_en": "☀️ Afternoon Cudding Roughage",
            "purpose_te": "పశువు నెమరు వేయడానికి అవసరమైన ఫైబర్ అందించి కడుపులో ఎసిడిటీని తగ్గిస్తుంది.",
            "purpose_hi": "पशु की जुगाली के लिए फाइबर प्रदान करता है और रूमेन एसिडोसिस रोकता है।",
            "purpose_en": "Essential long fiber to stimulate rumination cudding and buffer rumen pH.",
            "suggested": {
                "feed_name": "Dry Straw",
                "concentrate_kg": 0.0,
                "green_fodder_kg": 0.0,
                "dry_straw_kg": afternoon_straw,
                "water_litres": afternoon_water,
                "minerals_grams": 0.0,
                "target_milk_litres": 0.0
            }
        },
        {
            "slot_key": "evening",
            "time_window": "06:00 PM – 07:30 PM",
            "title_te": "🌙 సాయంత్రపు మేత (ఖనిజ సమతుల్యం)",
            "title_hi": "🌙 शाम का चारा (दाना व खनिज मिश्रण)",
            "title_en": "🌙 Evening Milking Feed & Minerals",
            "purpose_te": "రాత్రి వేళ పాల ఉత్పత్తి నిరంతరాయంగా సాగడానికి మరియు ఖనిజాల భర్తీకి దోహదపడుతుంది.",
            "purpose_hi": "रात में दूध निर्माण निरंतर रखने और खनिजों की पूर्ति हेतु संतुलित आहार।",
            "purpose_en": "Sustains overnight milk synthesis and provides vital mineral balance.",
            "suggested": {
                "feed_name": "Concentrate Mash + Night Green Fodder + Minerals",
                "concentrate_kg": eve_conc,
                "green_fodder_kg": eve_green,
                "dry_straw_kg": 0.0,
                "water_litres": eve_water,
                "minerals_grams": mineral_mix_grams,
                "target_milk_litres": round(milk_yield * 0.45, 1) if stage_key == "Lactating" else 0.0
            }
        }
    ]

    return {
        "status": "success",
        "animal_name": animal_profile.get("animal_name") or f"{species_key} ({stage_key})",
        "animal_type": species_key,
        "lactation_status": stage_key,
        "daily_milk_yield": milk_yield,
        "active_slot": active_slot,
        "next_reminder_slot": next_slot,
        "next_reminder_time": reminder_time,
        "reminder_description": {
            "te": reminder_desc_te,
            "hi": reminder_desc_hi,
            "en": reminder_desc_en
        },
        "daily_targets": {
            "total_concentrate_kg": total_conc_kg,
            "total_green_fodder_kg": total_green_kg,
            "total_dry_straw_kg": total_straw_kg,
            "total_water_litres": total_water_l,
            "mineral_mix_grams": mineral_mix_grams
        },
        "slots": slots_data
    }


def generate_feeding_insights(
    history_logs: List[Dict[str, Any]],
    language: str = "te"
) -> Dict[str, Any]:
    """
    Analyzes historical feeding diary logs to correlate feeding quantities
    against recorded milk yield and rumen cudding health.
    """
    if not history_logs or len(history_logs) == 0:
        return {
            "has_data": False,
            "headline": {
                "te": "మేత డైరీ డేటా సరిపోదు (కనీసం 2-3 రోజులు లాగ్ చేయండి)",
                "hi": "अपर्याप्त डेटा (कृपया 2-3 दिन चारा दर्ज करें)",
                "en": "Insufficient Diary Data (Log 2-3 days to reveal insights)"
            },
            "insight_text": {
                "te": "మీరు రోజూ ఉదయం, మధ్యాహ్నం, సాయంత్రం ఇచ్చిన మేతను నమోదు చేస్తే, ఏ మేత వల్ల పాల దిగుబడి పెరిగిందో సిస్టమ్ ఇక్కడ స్పష్టమైన విశ్లేషణ ఇస్తుంది.",
                "hi": "दैनिक चारा दर्ज करने पर AI बताएगा कि किस आहार से दूध उत्पादन में वृद्धि हुई है।",
                "en": "Log your daily feedings to uncover actionable correlations between feed ration balance and peak milk yield."
            },
            "recommendation_tips": [
                {"icon": "🌾", "tip_te": "రోజూ మధ్యాహ్నం 4 kg ఎండుగడ్డి తప్పనిసరిగా ఇవ్వండి.", "tip_en": "Feed 4kg dry straw in the afternoon for optimal cudding."}
            ]
        }

    # Group by feeding_date
    daily_groups: Dict[str, Dict[str, float]] = {}
    for log in history_logs:
        d = log.get("feeding_date")
        if not d:
            continue
        if d not in daily_groups:
            daily_groups[d] = {
                "concentrate_kg": 0.0,
                "green_fodder_kg": 0.0,
                "dry_straw_kg": 0.0,
                "milk_yield": 0.0,
                "slots_count": 0
            }
        daily_groups[d]["concentrate_kg"] += float(log.get("concentrate_kg") or 0.0)
        daily_groups[d]["green_fodder_kg"] += float(log.get("green_fodder_kg") or 0.0)
        daily_groups[d]["dry_straw_kg"] += float(log.get("dry_straw_kg") or 0.0)
        daily_groups[d]["milk_yield"] += float(log.get("milk_yield_litres") or 0.0)
        daily_groups[d]["slots_count"] += 1

    total_days = len(daily_groups)
    avg_conc = sum(v["concentrate_kg"] for v in daily_groups.values()) / total_days
    avg_green = sum(v["green_fodder_kg"] for v in daily_groups.values()) / total_days
    avg_straw = sum(v["dry_straw_kg"] for v in daily_groups.values()) / total_days
    milk_days = [v["milk_yield"] for v in daily_groups.values() if v["milk_yield"] > 0]
    avg_milk = (sum(milk_days) / len(milk_days)) if milk_days else 8.0

    # Best milk yield day correlation
    best_day = max(daily_groups.items(), key=lambda x: x[1]["milk_yield"], default=(None, None))
    best_milk = best_day[1]["milk_yield"] if best_day[1] else avg_milk
    best_conc = best_day[1]["concentrate_kg"] if best_day[1] else avg_conc
    best_green = best_day[1]["green_fodder_kg"] if best_day[1] else avg_green

    # Generate insights in Telugu, Hindi, English
    headline_te = f"⭐ మేత విశ్లేషణ: రోజువారీ సగటు పాల దిగుబడి {round(avg_milk, 1)} లీటర్లు"
    headline_hi = f"⭐ चारा विश्लेषण: दैनिक औसत दूध उत्पादन {round(avg_milk, 1)} लीटर"
    headline_en = f"⭐ Feeding Pattern Insights: Average Milk Yield is {round(avg_milk, 1)} L/day"

    if best_milk > avg_milk * 1.05 and best_conc > 0:
        insight_te = (
            f"మీ పశువుకు రోజుకు {round(best_conc, 1)} kg దాణా మరియు {round(best_green, 1)} kg పచ్చిగడ్డి అందించిన రోజులలో "
            f"పాల దిగుబడి అత్యధికంగా {round(best_milk, 1)} లీటర్లు (+{round(best_milk - avg_milk, 1)} L మెరుగుదల) నమోదైంది!"
        )
        insight_hi = (
            f"जिस दिन {round(best_conc, 1)} किग्रा दाना और {round(best_green, 1)} किग्रा हरा चारा दिया गया, "
            f"उस दिन दूध उत्पादन सर्वाधिक {round(best_milk, 1)} लीटर (+{round(best_milk - avg_milk, 1)} L अधिक) रहा!"
        )
        insight_en = (
            f"Optimal Feeding Peak: On days with {round(best_conc, 1)} kg concentrate and {round(best_green, 1)} kg green fodder, "
            f"milk production reached a high of {round(best_milk, 1)} Litres (+{round(best_milk - avg_milk, 1)} L improvement)!"
        )
    else:
        insight_te = (
            f"గత {total_days} రోజులుగా సగటున {round(avg_conc, 1)} kg దాణా మరియు {round(avg_green, 1)} kg పచ్చిగడ్డి ఇచ్చారు. "
            f"పాల దిగుబడి స్థిరంగా కొనసాగుతోంది. మధ్యాహ్నం తప్పనిసరిగా 4 kg ఎండుగడ్డి ఇవ్వడం వల్ల పాల వెన్న శాతం (Fat %) పెరుగుతుంది."
        )
        insight_hi = (
            f"पिछले {total_days} दिनों में औसत {round(avg_conc, 1)} किग्रा दाना दिया गया। "
            f"उत्पादन स्थिर है। दोपहर में सूखा चारा देने से दूध में फैट बना रहता है।"
        )
        insight_en = (
            f"Consistent Feeding: Average intake of {round(avg_conc, 1)} kg concentrate and {round(avg_green, 1)} kg green fodder. "
            f"Ensure afternoon dry straw feeding to maintain optimal butterfat percentage."
        )

    approx_water_l = 60.0 + (avg_milk * 2.5)

    tips = [
        {
            "icon": "🥛",
            "tip_te": "ఉదయం 50% మరియు సాయంత్రం 50% దాణా విభజించి ఇవ్వడం వల్ల జీర్ణక్రియ సులభతరం అవుతుంది.",
            "tip_hi": "सुबह 50% और शाम 50% दाना बांटकर खिलाने से पाचन सही रहता है।",
            "tip_en": "Splitting concentrate 50% morning and 50% evening stabilizes rumen fermentation."
        },
        {
            "icon": "🌾",
            "tip_te": "మధ్యాహ్నం వేళ పచ్చిగడ్డి బదులు ఎండుగడ్డి ఇవ్వడం వల్ల పశువు నెమరు వేయడం (Cudding) రెట్టింపు అవుతుంది.",
            "tip_hi": "दोपहर में सूखे चारे से पशु की जुगाली बढ़ती है और रूमेन एसिडिटी घटती है।",
            "tip_en": "Feeding dry straw at midday doubles chewing/cudding and prevents rumen acidosis."
        },
        {
            "icon": "💧",
            "tip_te": f"ల్యాక్టేటింగ్ పశువులకు ప్రతి లీటరు పాల ఉత్పత్తికి అదనంగా 2.5 లీటర్ల నీరు అవసరం. రోజూ {round(approx_water_l)}L నీరు అందుబాటులో ఉంచండి.",
            "tip_hi": "प्रति लीटर दूध पर 2.5 लीटर अतिरिक्त पानी चाहिए। ताजा पानी हमेशा सुलभ रखें।",
            "tip_en": f"High yielders require 2.5L water per 1L milk produced. Maintain {round(approx_water_l)}L clean water daily."
        }
    ]

    return {
        "has_data": True,
        "total_days_logged": total_days,
        "avg_daily_concentrate_kg": round(avg_conc, 1),
        "avg_daily_green_fodder_kg": round(avg_green, 1),
        "avg_daily_dry_straw_kg": round(avg_straw, 1),
        "avg_daily_milk_litres": round(avg_milk, 1),
        "peak_milk_litres": round(best_milk, 1),
        "headline": {
            "te": headline_te,
            "hi": headline_hi,
            "en": headline_en
        },
        "insight_text": {
            "te": insight_te,
            "hi": insight_hi,
            "en": insight_en
        },
        "recommendation_tips": tips
    }
