"""
SmartFeed AI - Multilingual Farmer Advisory Engine
Generates clear, actionable, and explainable feed safety advice in:
- English (en)
- Telugu (te - తెలుగు)
- Hindi (hi - हिंदी)

Supports optional OpenAI and Claude API integrations when API keys are provided in .env,
and defaults seamlessly to an offline domain rule-based advisory when offline or without keys.
"""

import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "").strip()

# --- Multilingual Offline Rule-Based Knowledge Base ---
ADVISORY_TEMPLATES = {
    "en": {
        "status": {
            "Low": "🟢 Safe for Feeding",
            "Medium": "🟡 Caution - Needs Attention",
            "High": "🔴 High Risk - Do Not Feed Immediately"
        },
        "mould_warning": (
            "⚠️ High fungal/mould risk detected. Ingestion of mouldy feed can cause severe mycotoxin poisoning, "
            "milk yield drop, and reproductive disorders in dairy cattle. Immediately withhold this feed and inspect for visible mould clumps."
        ),
        "urea_warning": (
            "🚨 Suspected chemical / non-protein nitrogen (urea) adulteration risk. Uncontrolled urea intake causes "
            "acute rumen alkalosis and can be fatal to cattle. Quarantine this batch and seek laboratory verification."
        ),
        "moisture_warning": (
            "💧 Elevated moisture detected. Damp feed deteriorates rapidly in warm storage. "
            "Spread the feed under sunlight or in an airy shed on a clean tarpaulin to dry before storage."
        ),
        "particle_warning": (
            "🔍 Visual particulate inclusions detected. Sieve and clean feed to remove sharp foreign stones, grit, "
            "or debris that can injure the mouth or digestive tract of cattle."
        ),
        "protein_deficit": (
            "🥗 Crude protein is below the optimal requirement. Consider supplementing the diet with oil cakes "
            "(groundnut cake, cottonseed cake, or mustard cake) to maintain peak lactation."
        ),
        "healthy_feed": (
            "✅ Feed quality and nutrient balance appear normal and suitable for dairy cattle. "
            "Feed according to recommended animal body weight allowances."
        ),
        "storage": {
            "good": "Maintain current dry, well-ventilated storage. Keep feed bags elevated on wooden pallets.",
            "humid": "Storage area is too damp. Immediately move bags away from damp walls and floor to prevent fungal growth.",
            "poor": "Storage environment exposes feed to moisture and heat. Ensure adequate air circulation and protection from rain.",
            "silage": "Ensure the silage pit/bunker remains tightly compacted and covered with plastic to prevent aerobic rot."
        }
    },
    "te": {
        "status": {
            "Low": "🟢 పశువుల మేత సురక్షితమైనది (Safe)",
            "Medium": "🟡 జాగ్రత్త - పరిశీలన అవసరం (Caution)",
            "High": "🔴 తీవ్ర ప్రమాదం - పశువులకు వెంటనే ఇవ్వవద్దు (High Risk)"
        },
        "mould_warning": (
            "⚠️ మీ పశువుల మేతలో ఫంగస్ లేదా బూజు వచ్చే అవకాశం ఎక్కువగా ఉంది. బూజు పట్టిన మేత తినడం వల్ల పశువులలో పాల దిగుబడి తగ్గిపోతుంది, "
            "జీర్ణ సమస్యలు మరియు తీవ్రమైన అనారోగ్యం కలుగుతాయి. ఈ మేతను వెంటనే పశువులకు ఇవ్వకుండా ముందుగా జాగ్రత్తగా పరిశీలించండి."
        ),
        "urea_warning": (
            "🚨 మేతలో రసాయనాలు లేదా కృత్రిమ యూరియా కల్తీ ఉండే అవకాశం ఉన్నట్లు కనిపిస్తోంది. అధిక యూరియా పశువులకు ప్రాణాంతకం కావచ్చు. "
            "ఈ మేత బస్తాలను వేరు చేసి, నిర్ధారణ కోసం స్థానిక పశువైద్యులను లేదా ల్యాబ్ ను సంప్రదించండి."
        ),
        "moisture_warning": (
            "💧 మేతలో తేమ శాతం ఎక్కువగా ఉంది. అధిక తేమ ఉన్నప్పుడు మేత త్వరగా కుళ్ళిపోతుంది మరియు బూజు పడుతుంది. "
            "మేతను వెంటనే శుభ్రమైన టార్పాలిన్ పై ఎండలో లేదా గాలి తగిలే చోట ఆరబెట్టండి."
        ),
        "particle_warning": (
            "🔍 మేతలో రాళ్ళు లేదా ఇతర పనికిరాని వ్యర్థాలు కనిపించాయి. పశువులకు ఇచ్చే ముందు జల్లెడ పట్టి రాళ్ళు మరియు ముళ్ళను తొలగించండి."
        ),
        "protein_deficit": (
            "🥗 మేతలో ప్రొటీన్ (మాంసకృత్తులు) తక్కువగా ఉన్నాయి. పాల ఉత్పత్తి తగ్గకుండా ఉండటానికి వేరుశనగ చెక్క, పత్తిగింజల చెక్క లేదా మినరల్ మిశ్రమాన్ని జతచేయండి."
        ),
        "healthy_feed": (
            "✅ పశువుల మేత నాణ్యత బాగుంది మరియు పోషకాలు సమతుల్యంగా ఉన్నాయి. పశువులకు నిర్దేశిత పరిమాణంలో నిరభ్యంతరంగా ఇవ్వవచ్చు."
        ),
        "storage": {
            "good": "మేత నిల్వ ఉన్న గది పొడిగా మరియు గాలి బాగా వచ్చేలా చూసుకోండి. బస్తాలను చెక్క పలకలపై నేలకు తగలకుండా పెట్టండి.",
            "humid": "నిల్వ ప్రదేశంలో తేమ ఎక్కువగా ఉంది. బస్తాలను తడి గోడలు మరియు నేల నుండి దూరంగా పొడి ప్రదేశానికి మార్చండి.",
            "poor": "మేతను ఎండ, వాన మరియు తేమ నుండి రక్షించండి. గాలి బాగా ఆడేలా తగిన జాగ్రత్తలు తీసుకోండి.",
            "silage": "సైలేజ్ గుంతలోకి గాలి వెళ్లకుండా ప్లాస్టిక్ పట్టా గట్టిగా కప్పి ఉంచండి, తద్వారా సైలేజ్ పాడవకుండా ఉంటుంది."
        }
    },
    "hi": {
        "status": {
            "Low": "🟢 पशु आहार सुरक्षित है (Safe)",
            "Medium": "🟡 सावधानी - निरीक्षण की आवश्यकता (Caution)",
            "High": "🔴 उच्च जोखिम - पशुओं को तुरंत न खिलाएं (High Risk)"
        },
        "mould_warning": (
            "⚠️ पशु आहार में फफूंद (उल्ली/फंगस) का उच्च जोखिम पाया गया है। फफूंदयुक्त चारा खाने से पशुओं के दूध उत्पादन में भारी गिरावट, "
            "गर्भपात और पाचन संबंधी गंभीर बीमारियां हो सकती हैं। इस चारे को पशुओं को तुरंत न दें और फफूंद लगे हिस्से को अलग करें।"
        ),
        "urea_warning": (
            "🚨 चारे में अवांछित रसायन या यूरिया मिलावट की आशंका है। यूरिया की अधिक मात्रा पशुओं के लिए जानलेवा साबित हो सकती है। "
            "इस आहार को तुरंत रोकें और प्रयोगशाला से जांच करवाएं।"
        ),
        "moisture_warning": (
            "💧 चारे में नमी का स्तर अधिक है। अधिक नमी से चारा बहुत जल्दी सड़ने लगता है। "
            "चारे को तुरंत साफ तिरपाल पर धूप या हवादार जगह पर सुखाएं।"
        ),
        "particle_warning": (
            "🔍 चारे में कंकड़, पत्थर या बाहरी अवांछित कण दिखाई दिए हैं। पशुओं को देने से पहले चारे को छानकर नुकीले कणों को अलग करें।"
        ),
        "protein_deficit": (
            "🥗 चारे में प्रोटीन की मात्रा कम पाई गई है। दूध का उत्पादन बनाए रखने के लिए खली (सरसों/बिनौला/मूंगफली) और खनिज मिश्रण मिलाकर खिलाएं।"
        ),
        "healthy_feed": (
            "✅ चारे की गुणवत्ता और पोषण संतुलन अच्छा है। इसे निर्धारित मात्रा में पशुओं को सुरक्षित रूप से खिलाया जा सकता है।"
        ),
        "storage": {
            "good": "भंडारण कक्ष को सूखा और हवादार रखें। बोरियों को लकड़ी के तख्तों पर रखें ताकि जमीन की नमी न लगे।",
            "humid": "गोदाम में अत्यधिक सीलन और नमी है। बोरियों को गीली दीवारों से दूर किसी सूखे स्थान पर रखें।",
            "poor": "चारे को बारिश, सीलन और कीटों से बचाएं। पर्याप्त हवा का आवागमन सुनिश्चित करें।",
            "silage": "साइलेज गड्ढे (पिट) को प्लास्टिक शीट से कसकर ढंक कर रखें ताकि हवा अंदर न जा सके और साइलेज सुरक्षित रहे।"
        }
    }
}

# --- Predefined Common Farmer Problem Statements Knowledge Base ---
FARMER_STATEMENTS_KB = {
    "milk_drop": {
        "id": "milk_drop",
        "icon": "🥛",
        "en": {
            "title": "Milk Drop After Feeding",
            "statement": "Milk yield dropped suddenly after feeding this batch",
            "status": "🟡 Caution - Nutritional Deficit or Early Toxins",
            "diagnosis": "Feed likely lacks sufficient crude protein (CP < 16%) or contains early sub-clinical fungal mycotoxins that suppress rumen fermentation.",
            "action": "Withhold this batch. Supplement livestock with high-protein oil cakes (cottonseed or groundnut cake) and fresh green fodder.",
            "warning": "Do not wait for multiple milkings if cows look lethargic; check the feed aroma immediately.",
            "storage": "Store feed off the ground on wooden pallets in dry ventilation.",
            "audio_summary": "Milk production drop detected. Withhold this feed batch immediately. Supplement cattle diet with protein oil cake and green fodder."
        },
        "te": {
            "title": "పాల దిగుబడి తగ్గింది",
            "statement": "ఈ మేత పెట్టిన తర్వాత పాల దిగుబడి అకస్మాత్తుగా తగ్గింది",
            "status": "🟡 జాగ్రత్త - పోషకాల లోపం లేదా విషతుల్యత",
            "diagnosis": "మేతలో ప్రొటీన్ (మాంసకృత్తులు) తక్కువగా ఉండటం లేదా కంటికి కనిపించని బూజు టాక్సిన్లు ఉండటం వల్ల పశువులలో పాల ఉత్పత్తి తగ్గుతుంది.",
            "action": "ఈ మేతను తాత్కాలికంగా ఆపివేయండి. పశువులకు వేరుశనగ చెక్క లేదా పత్తిగింజల చెక్క మరియు తాజా పచ్చిగడ్డిని అందించండి.",
            "warning": "పాల దిగుబడి తగ్గినప్పుడు పశువులను నిర్లక్ష్యం చేయవద్దు, పశువైద్యుని సంప్రదించండి.",
            "storage": "మేత బస్తాలను తడి నేలపై కాకుండా చెక్క పలకలపై గాలి ఆడేలా భద్రపరచండి.",
            "audio_summary": "పాల దిగుబడి అకస్మాత్తుగా తగ్గింది. ఈ మేతను వెంటనే ఆపండి. పశువులకు పత్తిగింజల చెక్క లేదా వేరుశనగ చెక్క మరియు తాజా పచ్చిగడ్డి ఇవ్వండి."
        },
        "hi": {
            "title": "दूध उत्पादन में गिरावट",
            "statement": "यह चारा खिलाने के बाद दूध उत्पादन अचानक घट गया",
            "status": "🟡 सावधानी - पोषण की कमी या टॉक्सिन",
            "diagnosis": "चारे में प्रोटीन की कमी या सूक्ष्म फफूंद के कारण रुमेन पाचन प्रभावित हुआ है, जिससे दूध का उत्पादन गिरा है।",
            "action": "इस चारे को तुरंत रोकें। पशुओं को बिनौला या सरसों की खली और ताजा हरा चारा दें।",
            "warning": "दूध घटने पर चारे की मात्रा जबरदस्ती न बढ़ाएं, पहले गुणवत्ता की जांच करें।",
            "storage": "चारे को जमीन की नमी से दूर लकड़ी के तख्तों पर रखें।",
            "audio_summary": "दूध उत्पादन में अचानक गिरावट आई है। यह चारा तुरंत रोकें। पशुओं को सरसों या बिनौले की खली और हरा चारा खिलाएं।"
        }
    },
    "mould_smell": {
        "id": "mould_smell",
        "icon": "🤢",
        "en": {
            "title": "Mould or Bad Smell",
            "statement": "Feed has sour/musty smell or visible white/dark mould",
            "status": "🔴 High Risk - Severe Mycotoxin Threat",
            "diagnosis": "Fungal colony growth produces harmful aflatoxins that cause liver damage, milk drop, and abortion in cows.",
            "action": "Immediately stop feeding this batch to all livestock! Separate and dispose of mouldy clumps safely.",
            "warning": "Never feed mouldy feed to pregnant cows or calves even in small amounts.",
            "storage": "Sun-dry unaffected bags on a clean tarpaulin and ensure well-ventilated dry storage.",
            "audio_summary": "High mould and fungal danger detected. Stop feeding this batch immediately. Ingestion causes severe poisoning and milk drop in cattle."
        },
        "te": {
            "title": "బూజు లేదా దుర్వాసన",
            "statement": "మేతలో బూజు పట్టి దుర్వాసన లేదా పుల్లని వాసన వస్తోంది",
            "status": "🔴 తీవ్ర ప్రమాదం - ఫంగస్ మరియు బూజు విషం",
            "diagnosis": "మేతలో ఫంగస్ బూజు పెరగడం వల్ల ప్రమాదకరమైన మైకోటాక్సిన్ విషాలు చేరాయి. ఇది తింటే పశువుల కాలేయం పాడవుతుంది మరియు చూడి పశువులకు గర్భస్రావం జరిగే ప్రమాదం ఉంది.",
            "action": "ఈ మేతను పశువులకు ఇవ్వడం వెంటనే ఆపండి! బూజు పట్టిన ముద్దలను వేరు చేసి పారవేయండి.",
            "warning": "చూడి పశువులకు లేదా దూడలకు ఎట్టి పరిస్థితుల్లోనూ ఈ మేతను కొద్దిగా కూడా పెట్టవద్దు.",
            "storage": "మిగిలిన మేతను శుభ్రమైన టార్పాలిన్ పై ఎండబెట్టి గాలి బాగా ఆడే పొడి ప్రదేశంలో నిల్వ చేయండి.",
            "audio_summary": "మేతలో తీవ్రమైన బూజు విషం ఉంది. పశువులకు వెంటనే ఈ మేతను ఆపివేయండి. బూజు పట్టిన మేత తినడం వల్ల పశువులు తీవ్ర అనారోగ్యానికి గురవుతాయి."
        },
        "hi": {
            "title": "फफूंद या दुर्गंध",
            "statement": "चारे में फफूंद (उल्ली) और सड़ी हुई दुर्गंध आ रही है",
            "status": "🔴 उच्च जोखिम - फफूंद और टॉक्सिन खतरा",
            "diagnosis": "चारे में फंगल इंफेक्शन से खतरनाक मायकोटॉक्सिन पैदा हो गए हैं जो पशुओं के लिवर को नुकसान पहुंचाते हैं।",
            "action": "पशुओं को यह चारा तुरंत बंद करें! फफूंद लगे हिस्से को अलग करके नष्ट करें।",
            "warning": "गाभिन गाय-भैंसों या छोटे बछड़ों को यह चारा बिल्कुल न खिलाएं।",
            "storage": "बचे हुए चारे को साफ तिरपाल पर धूप में सुखाएं और सूखे हवादार स्थान पर रखें।",
            "audio_summary": "चारे में खतरनाक फफूंद का संक्रमण है। पशुओं को यह चारा तुरंत रोकें। फफूंदयुक्त चारा खाने से पशु गंभीर रूप से बीमार हो सकते हैं।"
        }
    },
    "cattle_refusal": {
        "id": "cattle_refusal",
        "icon": "🍽️",
        "en": {
            "title": "Cattle Refusing Feed",
            "statement": "Cattle sniffing feed and refusing to eat / loss of appetite",
            "status": "🟡 Caution - Palatability or Contamination",
            "diagnosis": "Livestock possess keen olfactory senses; refusal usually signals rancidity, high salt/urea, or chemical stench.",
            "action": "Check feed for foul chemical odor or bitter taste. Offer plain hay/green grass to test appetite.",
            "warning": "Do not mix molasses or jaggery to trick cattle into eating rejected feed.",
            "storage": "Store feed away from pesticides, fuels, or chemical fertilizers.",
            "audio_summary": "Cattle are refusing to eat. Check feed for chemical odor, rancidity, or urea. Do not force animals to eat rejected feed."
        },
        "te": {
            "title": "పశువులు మేత తినడం లేదు",
            "statement": "పశువులు మేతను వాసన చూసి తినడం మానేస్తున్నాయి",
            "status": "🟡 జాగ్రత్త - మేతలో రసాయనాలు లేదా రుచి మార్పు",
            "diagnosis": "పశువులకు వాసన చూసే శక్తి చాలా ఎక్కువ. మేతలో రసాయనాల వాసన, అధిక ఉప్పు, లేదా నూనె వాసన వచ్చినప్పుడు అవి తినడానికి నిరాకరిస్తాయి.",
            "action": "మేతలో ఘాటైన రసాయనాల వాసన లేదా చేదు రుచి ఉందేమో పరిశీలించండి. పశువులకు సాధారణ ఎండుగడ్డి లేదా పచ్చిగడ్డి ఇచ్చి చూడండి.",
            "warning": "బెల్లం లేదా ఉప్పు కలిపి పశువులతో బలవంతంగా ఈ మేతను తినిపించవద్దు.",
            "storage": "పురుగుమందులు మరియు రసాయనిక ఎరువులకు దూరంగా మేతను భద్రపరచండి.",
            "audio_summary": "పశువులు మేత తినడానికి నిరాకరిస్తున్నాయి. మేతలో రసాయనాలు లేదా పుల్లని వాసన ఉందేమో చూడండి. బలవంతంగా తినిపించవద్దు."
        },
        "hi": {
            "title": "पशु चारा नहीं खा रहे",
            "statement": "पशु चारे को सूंघकर खाने से मना कर रहे हैं",
            "status": "🟡 सावधानी - दुर्गंध या रासायनिक मिलावट",
            "diagnosis": "पशुओं की सूंघने की क्षमता तेज होती है। चारे में दुर्गंध, कड़वापन या यूरिया होने पर वे चारा छोड़ देते हैं।",
            "action": "चारे में किसी रासायनिक या सड़ी गंध की जांच करें। पशुओं को ताजा हरा चारा या सूखा भूसा देकर भूख जांचें।",
            "warning": "गुड़ या नमक मिलाकर जबरदस्ती खराब चारा न खिलाएं।",
            "storage": "कीटनाशक और खाद से चारे को दूर रखें।",
            "audio_summary": "पशु चारा खाने से मना कर रहे हैं। चारे में दुर्गंध या रसायन की जांच करें। पशुओं को जबरन यह चारा न खिलाएं।"
        }
    },
    "wet_feed": {
        "id": "wet_feed",
        "icon": "🌧️",
        "en": {
            "title": "Wet / Damp Feed",
            "statement": "Feed bags got soaked in rain or damp moisture from floor",
            "status": "🟡 Warning - Moisture Spoilage Hazard",
            "diagnosis": "Moisture above 13% causes rapid microbial heating, souring, and fungal infestation within 24 to 48 hours.",
            "action": "Immediately untie and spread feed on a clean tarpaulin under sunlight or a breezy covered shed.",
            "warning": "Never leave wet feed tightly sealed inside bags; fermentation will rot the batch quickly.",
            "storage": "Never place feed bags directly on bare concrete ground. Always use wooden slats.",
            "audio_summary": "Feed is damp or soaked. High moisture causes rapid rot and mould. Spread on clean sheet immediately to sun-dry."
        },
        "te": {
            "title": "మేత తడిసిపోయింది",
            "statement": "వర్షం వల్ల లేదా తడి నేల వల్ల మేత బస్తాలు తడిసిపోయాయి",
            "status": "🟡 హెచ్చరిక - అధిక తేమ వల్ల మేత కుళ్ళే ప్రమాదం",
            "diagnosis": "మేతలో తేమ ఎక్కువైతే 24 నుండి 48 గంటల్లోనే పులిసిపోయి, వేడెక్కి బూజు పట్టి పూర్తిగా పాడైపోతుంది.",
            "action": "వెంటనే బస్తాలు విప్పి శుభ్రమైన టార్పాలిన్ లేదా పరదాపై ఎండలో లేదా గాలి తగిలేలా ఆరబెట్టండి.",
            "warning": "తడిసిన మేతను అలాగే బస్తాలలో కట్టి ఉంచవద్దు, వెంటనే కుళ్ళిపోతుంది.",
            "storage": "ఎప్పుడూ నేరుగా నేలపై బస్తాలు పెట్టకండి, చెక్క బల్లలపై నేలకు తగలకుండా ఉంచండి.",
            "audio_summary": "మేత తడిసిపోయింది. తడిసిన మేత త్వరగా కుళ్ళిపోతుంది. వెంటనే బస్తాలు విప్పి ఎండలో లేదా గాలికి బాగా ఆరబెట్టండి."
        },
        "hi": {
            "title": "चारा भीग गया है",
            "statement": "बारिश या सीलन वाली जमीन से चारे की बोरियां भीग गईं",
            "status": "🟡 चेतावनी - नमी से सड़न का खतरा",
            "diagnosis": "चारे में नमी बढ़ने से 24-48 घंटों के भीतर फफूंद और सड़न शुरू हो जाती है।",
            "action": "बोरियों को तुरंत खोलकर साफ तिरपाल पर धूप या खुली हवा में अच्छी तरह सुखाएं।",
            "warning": "भीगे हुए चारे को बंद बोरियों में न छोड़ें, इससे चारा गर्म होकर सड़ जाएगा।",
            "storage": "बोरियों को कभी भी सीधे गीली जमीन पर न रखें, लकड़ी के पटरों पर रखें।",
            "audio_summary": "चारा भीग गया है। अधिक नमी से चारा सड़ने लगता है। तुरंत बोरियां खोलकर धूप में अच्छी तरह सुखाएं।"
        }
    },
    "urea_spiking": {
        "id": "urea_spiking",
        "icon": "🚨",
        "en": {
            "title": "Suspected Urea Spiking",
            "statement": "Found white granules/powder or strong chemical odor in feed",
            "status": "🔴 High Risk - Deadly Chemical Adulteration",
            "diagnosis": "Unethical vendors spike feed with fertilizer-grade urea (46% N) to cheat protein testing. High urea triggers fatal rumen alkalosis.",
            "action": "Quarantine this entire batch immediately! Do not feed. Contact your local veterinary doctor or milk union officer for lab testing.",
            "warning": "DO NOT FEED to calves or milking animals under any circumstances! Urea poisoning can kill cattle in 1-2 hours.",
            "storage": "Segregate and label this feed clearly as 'HAZARDOUS - NOT FOR FEEDING'.",
            "audio_summary": "Critical urea adulteration suspected. Stop feeding immediately! Urea poisoning is fatal to cattle. Quarantine batch for lab testing."
        },
        "te": {
            "title": "యూరియా కల్తీ అనుమానం",
            "statement": "మేతలో తెల్లటి గుళికలు లేదా ఘాటైన యూరియా వాసన వస్తోంది",
            "status": "🔴 అత్యంత ప్రమాదం - యూరియా కల్తీ ప్రాణాంతకం",
            "diagnosis": "ప్రొటీన్ ఎక్కువగా ఉన్నట్లు చూపించడానికి కొందరు వ్యాపారులు ఎరువుల యూరియా కలుపుతారు. యూరియా పశువుల పొట్టలో తీవ్ర విషంగా మారి పశువు మరణానికి దారితీస్తుంది.",
            "action": "ఈ మేతను వెంటనే పక్కన పెట్టండి! ఒక్క పిడికిలి కూడా పశువులకు ఇవ్వవద్దు. పరీక్ష కోసం డైరీ లేదా పశువైద్యునికి తెలియజేయండి.",
            "warning": "ఎట్టి పరిస్థితుల్లోనూ పశువులకు లేదా దూడలకు ఈ మేత పెట్టవద్దు! యూరియా విషం వల్ల పశువులు గంటల వ్యవధిలోనే చనిపోతాయి.",
            "storage": "ఈ బస్తాలపై 'విషపూరితం - పశువులకు ఇవ్వవద్దు' అని గుర్తుపెట్టి వేరుగా ఉంచండి.",
            "audio_summary": "తీవ్రమైన యూరియా కల్తీ అనుమానం. పశువులకు ఈ మేతను ఒక్క పిడికిలి కూడా ఇవ్వవద్దు! అధిక యూరియా పశువులకు ప్రాణాంతకం."
        },
        "hi": {
            "title": "यूरिया मिलावट की आशंका",
            "statement": "चारे में सफेद दाने या यूरिया/अमोनिया की तेज गंध आ रही है",
            "status": "🔴 अत्यंत खतरनाक - यूरिया विषाक्तता का खतरा",
            "diagnosis": "प्रोटीन अधिक दिखाने के लिए खाद वाली यूरिया मिलाई जाती है। यूरिया पशुओं के पेट में जहर बनकर उनकी जान ले सकती है।",
            "action": "इस चारे को तुरंत अलग करें! पशुओं को बिल्कुल न दें। डेयरी अधिकारी या पशु चिकित्सक से जांच कराएं।",
            "warning": "बछड़ों या गाय-भैंसों को यह चारा भूलकर भी न खिलाएं! यूरिया से कुछ ही घंटों में पशु की मौत हो सकती है।",
            "storage": "इन बोरियों पर 'खतरा - पशुओं को न दें' लिखकर अलग रखें।",
            "audio_summary": "यूरिया मिलावट की गंभीर आशंका है। पशुओं को यह चारा तुरंत रोकें! यूरिया पशुओं के लिए जानलेवा साबित हो सकती है।"
        }
    },
    "loose_dung": {
        "id": "loose_dung",
        "icon": "🩺",
        "en": {
            "title": "Cattle Loose Dung / Bloat",
            "statement": "Cattle developed loose dung, bloat, or indigestion after feeding",
            "status": "🔴 High Risk - Rumen Acidosis / Enteritis",
            "diagnosis": "Feed spoilage, fungal toxins, or excessively rapid starch fermentation causes severe digestive tract inflammation.",
            "action": "Withdraw concentrate feed immediately. Provide clean dry straw/hay and clean drinking water with electrolytes. Call veterinary doctor.",
            "warning": "Do not give heavy grain mixes until the animal's digestion normalizes.",
            "storage": "Inspect feed for dampness, rodent contamination, or insect webbing.",
            "audio_summary": "Digestive disorder detected in cattle. Stop concentrate feed immediately. Provide dry hay, fresh water, and call a veterinarian."
        },
        "te": {
            "title": "పశువులకు విరేచనాలు / ఉబ్బరం",
            "statement": "మేత తిన్నాక పశువులకు కడుపు ఉబ్బరం లేదా విరేచనాలు అయ్యాయి",
            "status": "🔴 తీవ్ర ప్రమాదం - జీర్ణకోశ సమస్య / పశువుల అనారోగ్యం",
            "diagnosis": "మేత పాడైపోవడం లేదా విషతుల్యమైన బ్యాక్టీరియా/ఫంగస్ వల్ల పశువుల పొట్టలో అసిడోసిస్ మరియు విరేచనాలు వస్తాయి.",
            "action": "ఈ దాణా మేతను వెంటనే ఆపేయండి. పశువులకు మంచి ఎండుగడ్డి మరియు శుభ్రమైన నీరు అందించండి. వెంటనే పశువైద్యుని పిలిపించండి.",
            "warning": "పశువులు కోలుకునే వరకు ఎలాంటి దాణా లేదా నూనె చెక్కను ఎక్కువగా తినిపించవద్దు.",
            "storage": "మేతలో ఎలుకల మలమూత్రాలు లేదా పురుగులు చేరకుండా శుభ్రమైన గదిలో భద్రపరచండి.",
            "audio_summary": "పశువులకు విరేచనాలు లేదా కడుపు ఉబ్బరం వచ్చింది. దాణా మేతను వెంటనే ఆపండి. ఎండుగడ్డి, మంచినీరు ఇచ్చి పశువైద్యుని సంప్రదించండి."
        },
        "hi": {
            "title": "पशुओं को दस्त या पेट फूलना",
            "statement": "चारा खाने के बाद पशुओं को पेट फूलना या दस्त हो गए हैं",
            "status": "🔴 उच्च जोखिम - पाचन तंत्र में खराबी",
            "diagnosis": "चारे की खराबी या फंगल इन्फेक्शन से पशुओं के पेट में एसिडोसिस और आंतों में सूजन हो गई है।",
            "action": "यह दाना/चारा तुरंत रोकें। पशुओं को सूखा भूसा और स्वच्छ पानी दें। तुरंत पशु चिकित्सक को दिखाएं।",
            "warning": "पशु के ठीक होने तक कोई भारी अनाज या सड़ा चारा न दें।",
            "storage": "चारे को चूहों और कीड़ों से बचाकर रखें।",
            "audio_summary": "पशुओं को दस्त या पेट फूलने की समस्या हुई है। दाना तुरंत बंद करें। सूखा भूसा और पानी देकर डॉक्टर को बुलाएं।"
        }
    }
}


def get_farmer_statements(language: str = "en") -> List[Dict[str, Any]]:
    """Returns the list of farmer common statements localized in the specified language."""
    lang = language.lower() if language.lower() in ["en", "te", "hi"] else "en"
    result = []
    for pid, data in FARMER_STATEMENTS_KB.items():
        entry = data.get(lang, data["en"])
        result.append({
            "id": pid,
            "icon": data["icon"],
            "title": entry["title"],
            "statement": entry["statement"],
            "status": entry["status"]
        })
    return result


def generate_offline_advisory(analysis_data: Dict[str, Any], language: str = "en") -> Dict[str, Any]:
    """
    Generates deterministic, agricultural expert rule-based farmer advice in the selected language.
    Does not require internet or API keys.
    """
    lang = language.lower() if language.lower() in ["en", "te", "hi"] else "en"
    tpl = ADVISORY_TEMPLATES[lang]

    # Check if a specific farmer problem statement was chosen
    prob_id = analysis_data.get("problem_id") or analysis_data.get("statement_id")
    if prob_id and prob_id in FARMER_STATEMENTS_KB:
        kb_entry = FARMER_STATEMENTS_KB[prob_id].get(lang, FARMER_STATEMENTS_KB[prob_id]["en"])
        
        headings = {
            "en": ("🛑 Problem Diagnosis:", "🚨 Immediate Action:", "⚠️ What NOT to Do:", "🏠 Storage Recommendation:"),
            "te": ("🛑 సమస్య విశ్లేషణ:", "🚨 వెంటనే చేయవలసిన పని:", "⚠️ ఖచ్చితంగా చేయకూడని పని:", "🏠 నిల్వ జాగ్రత్త:"),
            "hi": ("🛑 समस्या विश्लेषण:", "🚨 तुरंत क्या करें:", "⚠️ क्या न करें:", "🏠 भंडारण सलाह:")
        }[lang]

        full_text = (
            f"{kb_entry['status']}\n\n"
            f"{headings[0]}\n{kb_entry['diagnosis']}\n\n"
            f"{headings[1]}\n{kb_entry['action']}\n\n"
            f"{headings[2]}\n{kb_entry['warning']}\n\n"
            f"{headings[3]}\n{kb_entry['storage']}"
        )

        return {
            "safety_status": kb_entry["status"],
            "problem_id": prob_id,
            "farmer_statement": kb_entry["statement"],
            "main_problems": [kb_entry["diagnosis"]],
            "recommended_actions": [kb_entry["action"], kb_entry["warning"]],
            "storage_advice": kb_entry["storage"],
            "full_advisory_text": full_text.strip(),
            "audio_summary": kb_entry.get("audio_summary", kb_entry["action"]),
            "language": lang,
            "provider": "SmartFeed Farmer Statement Knowledge Base",
            "is_offline_fallback": True
        }

    overall_risk = analysis_data.get("overall_risk", "Low")
    health_score = analysis_data.get("health_score", 85.0)
    mould_risk = analysis_data.get("mould_risk", "Low")
    adulteration_risk = analysis_data.get("adulteration_risk", "Low")
    flagged_hazards = analysis_data.get("flagged_hazards", [])
    storage_condition = analysis_data.get("storage_condition", "").lower()
    moisture = analysis_data.get("moisture", 10.0)
    sample_type = analysis_data.get("sample_type", "Feed Ingredient")
    protein_status = analysis_data.get("protein_status", "Optimal")
    foreign_risk = analysis_data.get("foreign_particle_risk", "Low")

    safety_heading = tpl["status"].get(overall_risk, tpl["status"]["Low"])

    main_problems: List[str] = []
    actions: List[str] = []

    # 1. Mould Risk
    if mould_risk == "High":
        main_problems.append(tpl["mould_warning"])
        actions.append("Withhold feed immediately / వెంటనే మేతను ఆపండి / तुरंत चारा रोकें")
    elif mould_risk == "Medium":
        main_problems.append(tpl["mould_warning"])

    # 2. Urea / Adulteration Hazard
    has_urea = any("urea" in str(h).lower() for h in flagged_hazards)
    if has_urea or adulteration_risk == "High":
        main_problems.append(tpl["urea_warning"])
        actions.append("Quarantine batch for lab testing / ల్యాబ్ పరీక్ష కోసం మేతను వేరు చేయండి / प्रयोगशाला जांच कराएं")

    # 3. Moisture
    if (sample_type != "Silage" and moisture > 13.5) or (sample_type == "Silage" and moisture > 73.0):
        main_problems.append(tpl["moisture_warning"])
        actions.append("Sun-dry feed on clean sheet / ఎండలో ఆరబెట్టండి / धूप में सुखाएं")

    # 4. Foreign Particles
    if foreign_risk in ["High", "Medium"]:
        main_problems.append(tpl["particle_warning"])
        actions.append("Sieve feed before use / జల్లెడ పట్టండి / छानकर खिलाएं")

    # 5. Protein Deficit
    if protein_status == "Deficient":
        main_problems.append(tpl["protein_deficit"])
        actions.append("Supplement with oil cake / పశువులకు చెక్క కలపండి / खली मिलाएं")

    # If completely safe
    if not main_problems:
        main_problems.append(tpl["healthy_feed"])
        actions.append("Feed as normal / యధావిధిగా తినిపించండి / सामान्य रूप से खिलाएं")

    # Storage advice
    storage_key = "good"
    if "silage" in sample_type.lower():
        storage_key = "silage"
    elif "humid" in storage_condition or "damp" in storage_condition:
        storage_key = "humid"
    elif "poor" in storage_condition or "outdoor" in storage_condition:
        storage_key = "poor"

    storage_advice = tpl["storage"].get(storage_key, tpl["storage"]["good"])

    # Full consolidated narrative
    full_text = f"{safety_heading}\n\n"
    for prob in main_problems:
        full_text += f"• {prob}\n\n"
    full_text += f"🏠 నిల్వ సలహా / भंडारण सलाह / Storage Advice:\n{storage_advice}"

    return {
        "safety_status": safety_heading,
        "main_problems": main_problems,
        "recommended_actions": actions,
        "storage_advice": storage_advice,
        "full_advisory_text": full_text.strip(),
        "language": lang,
        "provider": "Offline Rule-Based Advisory",
        "is_offline_fallback": True
    }


def generate_llm_advisory(
    analysis_data: Dict[str, Any],
    language: str = "en",
    provider: str = "auto"
) -> Optional[Dict[str, Any]]:
    """
    Calls OpenAI or Anthropic Claude API to generate a personalized multilingual advisory.
    Returns None if no API keys are present or if network/API error occurs.
    """
    lang_name = {"en": "English", "te": "Telugu (తెలుగు)", "hi": "Hindi (हिंदी)"}.get(language.lower(), "English")

    system_prompt = (
        "You are an expert agricultural and dairy feed advisory assistant for SmartFeed AI. "
        "Provide practical, simple, compassionate recommendations for rural dairy farmers in India. "
        "Avoid complex scientific jargon. Clearly distinguish between AI visual predictions and laboratory confirmations. "
        "Never claim chemical contamination is confirmed unless laboratory data is provided. "
        f"You must respond ENTIRELY in {lang_name}."
    )

    user_prompt = f"""
Farmer Feed Assessment Data:
- Sample Type: {analysis_data.get('sample_type', 'Feed Ingredient')}
- SmartFeed Health Score: {analysis_data.get('health_score', 0)} / 100
- Overall Risk: {analysis_data.get('overall_risk', 'Low')}
- Visual Finding: {analysis_data.get('farmer_label', 'Normal')}
- Mould Risk: {analysis_data.get('mould_risk', 'Low')}
- Foreign Particle Risk: {analysis_data.get('foreign_particle_risk', 'Low')}
- Adulteration Risk: {analysis_data.get('adulteration_risk', 'Low')}
- Crude Protein: {analysis_data.get('crude_protein', 0)}%
- Moisture: {analysis_data.get('moisture', 0)}%
- Fiber: {analysis_data.get('fiber', 0)}%
- Storage Condition: {analysis_data.get('storage_condition', 'Normal')}
- Primary Concern: {analysis_data.get('primary_concern', 'None')}

Please provide a structured response with:
1. Safety Status Headline
2. Main Risks & Concerns Explained Simply
3. Step-by-Step Recommended Farmer Actions
4. Storage & Handling Advice
"""

    # Check OpenAI
    if (provider in ["auto", "openai"]) and OPENAI_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY, timeout=10.0)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=600,
                temperature=0.3
            )
            text = response.choices[0].message.content.strip()
            return {
                "safety_status": f"{analysis_data.get('overall_risk', 'Safe')} Advisory",
                "main_problems": [analysis_data.get("primary_concern", "")],
                "recommended_actions": [analysis_data.get("recommended_action", "")],
                "storage_advice": analysis_data.get("storage_condition", ""),
                "full_advisory_text": text,
                "language": language,
                "provider": "OpenAI GPT-4o-mini",
                "is_offline_fallback": False
            }
        except Exception:
            pass

    # Check Claude / Anthropic
    if (provider in ["auto", "claude", "anthropic"]) and ANTHROPIC_API_KEY:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY, timeout=10.0)
            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=600,
                temperature=0.3,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            text = message.content[0].text.strip()
            return {
                "safety_status": f"{analysis_data.get('overall_risk', 'Safe')} Advisory",
                "main_problems": [analysis_data.get("primary_concern", "")],
                "recommended_actions": [analysis_data.get("recommended_action", "")],
                "storage_advice": analysis_data.get("storage_condition", ""),
                "full_advisory_text": text,
                "language": language,
                "provider": "Anthropic Claude 3 Haiku",
                "is_offline_fallback": False
            }
        except Exception:
            pass

    return None


def analyze_manual_farmer_entry(
    analysis_data: Dict[str, Any],
    language: str = "en",
    provider: str = "auto"
) -> Dict[str, Any]:
    """
    Intelligently analyzes a custom farmer-written query and physical parameters.
    Supports English, Telugu, and Hindi (both native scripts and transliterated/phonetic text).
    Generates structured AI diagnosis, immediate action, contraindications, storage tips,
    and voice audio summary.
    """
    lang = language.lower() if language.lower() in ["en", "te", "hi"] else "en"
    
    # Extract query text & physical dropdown conditions
    query = str(
        analysis_data.get("query")
        or analysis_data.get("manual_query")
        or analysis_data.get("farmer_text")
        or analysis_data.get("statement")
        or ""
    ).strip()
    
    feed_type = str(analysis_data.get("sample_type") or analysis_data.get("feed_type") or "Cattle Feed").strip()
    smell = str(analysis_data.get("smell") or analysis_data.get("feed_smell") or "Normal").strip()
    moisture = str(analysis_data.get("moisture_status") or analysis_data.get("moisture") or "Normal").strip()
    appearance = str(analysis_data.get("appearance") or analysis_data.get("feed_appearance") or "Normal").strip()
    cattle_symptom = str(analysis_data.get("cattle_symptom") or analysis_data.get("symptom") or "Normal").strip()

    # 1. Attempt Online LLM if API Key is available
    if provider.lower() != "offline" and (OPENAI_API_KEY or ANTHROPIC_API_KEY):
        lang_name = {"en": "English", "te": "Telugu (తెలుగు)", "hi": "Hindi (हिंदी)"}.get(lang, "English")
        llm_prompt = f"""
A dairy farmer has submitted a custom inquiry regarding feed quality and cattle symptoms:
- Farmer's Own Words: "{query if query else 'Not specified'}"
- Feed Type: {feed_type}
- Feed Smell: {smell}
- Moisture Condition: {moisture}
- Physical Appearance: {appearance}
- Cattle Symptoms: {cattle_symptom}

Please generate an agricultural advisory specifically tailored for an Indian smallholder dairy farmer.
Respond entirely in {lang_name}.
Provide the following sections clearly:
1. Safety Status Headline (with 🟢 / 🟡 / 🔴)
2. 🛑 AI Diagnosis (What is likely wrong with the feed or animal)
3. 🚨 Immediate Action (Step-by-step what the farmer should do right now)
4. ⚠️ What NOT to Do (Dangerous mistakes to avoid)
5. 🏠 Feed Storage & Future Prevention Advice
6. AUDIO SUMMARY: (A short 1-2 sentence spoken summary)
"""
        if OPENAI_API_KEY and provider in ["auto", "openai"]:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=OPENAI_API_KEY, timeout=10.0)
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": f"You are a veterinarian and livestock feed expert. Respond in {lang_name}."},
                        {"role": "user", "content": llm_prompt}
                    ],
                    max_tokens=650,
                    temperature=0.3
                )
                txt = resp.choices[0].message.content.strip()
                return {
                    "safety_status": "🟡 AI Custom Evaluation" if "🔴" not in txt else "🔴 High Risk Advisory",
                    "farmer_statement": query or f"{feed_type} Custom Assessment",
                    "full_advisory_text": txt,
                    "audio_summary": txt.split("AUDIO SUMMARY:")[-1].strip() if "AUDIO SUMMARY:" in txt else txt[:200],
                    "language": lang,
                    "provider": "OpenAI GPT-4o-mini (Farmer Custom Analysis)",
                    "is_offline_fallback": False
                }
            except Exception:
                pass

        if ANTHROPIC_API_KEY and provider in ["auto", "claude", "anthropic"]:
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY, timeout=10.0)
                resp = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=650,
                    temperature=0.3,
                    system=f"You are a veterinarian and livestock feed expert. Respond in {lang_name}.",
                    messages=[{"role": "user", "content": llm_prompt}]
                )
                txt = resp.content[0].text.strip()
                return {
                    "safety_status": "🟡 AI Custom Evaluation" if "🔴" not in txt else "🔴 High Risk Advisory",
                    "farmer_statement": query or f"{feed_type} Custom Assessment",
                    "full_advisory_text": txt,
                    "audio_summary": txt.split("AUDIO SUMMARY:")[-1].strip() if "AUDIO SUMMARY:" in txt else txt[:200],
                    "language": lang,
                    "provider": "Anthropic Claude 3 Haiku (Farmer Custom Analysis)",
                    "is_offline_fallback": False
                }
            except Exception:
                pass

    # 2. Expert Offline NLP & Agricultural Knowledge Engine
    q_low = query.lower()

    # Hazard Detection Flags
    urea_flag = (
        any(k in q_low for k in [
            'యూరియా', 'రసాయన', 'తెల్ల పొడి', 'ఎరువుల', 'కల్తీ', 'ఘాటైన',
            'urea', 'chemical', 'ammonia', 'fertilizer', 'pungent', 'white powder', 'granules',
            'यूरिया', 'रसायन', 'सफेद पाउडर', 'तेज गंध', 'खाद', 'मिलावट'
        ])
        or "chemical" in smell.lower() or "urea" in smell.lower()
        or "white powder" in appearance.lower() or "granule" in appearance.lower()
        or "యూరియా" in appearance.lower()
    )

    mould_flag = (
        any(k in q_low for k in [
            'బూజు', 'పులిసి', 'శిలీంధ్రం', 'నల్లటి', 'వాసన', 'ముద్దలు',
            'booju', 'buju', 'fungus', 'mould', 'mold', 'mycotoxin', 'musty', 'sour', 'rot', 'spoiled',
            'फफूंद', 'उल्ली', 'सड़ा', 'दुर्गंध', 'खट्टा', 'fafund'
        ])
        or "fungal" in smell.lower() or "musty" in smell.lower() or "sour" in smell.lower()
        or "mould" in appearance.lower() or "fungus" in appearance.lower()
        or "బూజు" in appearance.lower() or "फफूंद" in appearance.lower()
    )

    milk_drop_flag = (
        any(k in q_low for k in [
            'పాలు తగ్గి', 'పాల దిగుబడి', 'పాలు తగ్గాయి', 'దిగుబడి తగ్గింది', 'పాలు రావడం లేదు',
            'paalu tagg', 'palu tagg', 'milk drop', 'yield drop', 'less milk', 'low milk', 'milk decrease',
            'दूध घट', 'दूध कम', 'दूध गिर', 'दूध नहीं दे रही', 'doodh kam', 'doodh ghat'
        ])
        or "milk" in cattle_symptom.lower() or "పాలు" in cattle_symptom.lower() or "दूध" in cattle_symptom.lower()
    )

    digestive_flag = (
        any(k in q_low for k in [
            'విరేచనాలు', 'ఉబ్బరం', 'కడుపు ఉబ్బరం', 'పల్చటి పేడ', 'మోషన్స్', 'జీర్ణం',
            'virechanalu', 'ubbaram', 'loose motions', 'loose dung', 'diarrhea', 'bloat', 'indigestion', 'tympany', 'acidosis',
            'दस्त', 'पेट फूलना', 'पतला गोबर', 'अपच', 'गैस', 'dast'
        ])
        or "loose" in cattle_symptom.lower() or "diarrhea" in cattle_symptom.lower()
        or "bloat" in cattle_symptom.lower() or "విరేచనాలు" in cattle_symptom.lower()
        or "दस्त" in cattle_symptom.lower()
    )

    refusal_flag = (
        any(k in q_low for k in [
            'తినడం లేదు', 'మేత ముట్టడం లేదు', 'ఆకలి లేదు', 'వాసన చూసి', 'వదిలేస్తున్నాయి',
            'tinadam ledu', 'thinadam ledu', 'not eating', 'refusing', 'refusal', 'loss of appetite', 'off feed',
            'चारा नहीं खा रही', 'चारा छोड़ दिया', 'भूख नहीं', 'सूंघकर'
        ])
        or "refusing" in cattle_symptom.lower() or "appetite" in cattle_symptom.lower()
        or "తినడం లేదు" in cattle_symptom.lower() or "चारा नहीं" in cattle_symptom.lower()
    )

    moisture_flag = (
        any(k in q_low for k in [
            'తడిసిన', 'వర్షం', 'నీరు', 'తేమ', 'బస్తాలు తడిచాయి',
            'thadisi', 'varsham', 'wet', 'damp', 'soaked', 'rain', 'water', 'moisture',
            'भीग गया', 'बारिश', 'नमी', 'सीलन', 'गीला', 'geela', 'bheeg'
        ])
        or "damp" in moisture.lower() or "wet" in moisture.lower() or "soaked" in moisture.lower()
        or "rain" in moisture.lower() or "తడి" in moisture.lower() or "भीग" in moisture.lower()
    )

    insects_particles_flag = (
        any(k in q_low for k in [
            'రాళ్ళు', 'పురుగులు', 'ముళ్ళు', 'చెత్త', 'ధూళి',
            'raallu', 'purugulu', 'stones', 'insects', 'worms', 'weevils', 'dirt', 'grit',
            'कंकड़', 'पत्थर', 'कीड़े', 'कचरा', 'धूल', 'kankad'
        ])
        or "inclusions" in appearance.lower() or "debris" in appearance.lower()
        or "పురుగులు" in appearance.lower() or "कीड़े" in appearance.lower()
    )

    # Multi-lingual Knowledge Pack for Custom Cases
    kbp = {
        "en": {
            "headers": ("🛑 AI Diagnosis & Root Cause:", "🚨 Immediate Action Required:", "⚠️ What NOT to Do (Contraindications):", "🏠 Feed Storage & Future Prevention:"),
            "urea": {
                "status": "🔴 High Risk - Deadly Chemical / Urea Spiking Threat",
                "diag": f"Feed parameters indicate high suspicion of non-protein nitrogen (urea) contamination in {feed_type}. Excess urea produces massive ammonia in the rumen, causing severe rumen alkalosis, muscle tremors, and fatal poisoning within 1-2 hours.",
                "action": f"Withhold this {feed_type} immediately! Do not feed even a handful. Segregate the bags and immediately report to your local veterinarian or dairy union testing lab.",
                "warn": "Never feed to pregnant cows or calves under any condition. Do not try washing or cooking spiked feed; it does not remove toxic urea.",
                "storage": "Store segregated bags marked as 'HAZARDOUS' completely away from all livestock and normal feeds.",
                "audio": f"Critical urea adulteration suspected in {feed_type}. Stop feeding immediately! Urea poisoning is fatal to cattle. Quarantine batch for lab testing."
            },
            "mould": {
                "status": "🔴 High Risk - Toxic Mould / Mycotoxin Contamination",
                "diag": f"Fungal colony growth detected in {feed_type}. Ingestion of mouldy feed introduces dangerous mycotoxins (aflatoxins) that damage cattle liver, crash milk yields, and induce abortions in pregnant livestock.",
                "action": f"Stop feeding this batch of {feed_type} right now! Separate and discard all mouldy clumps. Administer veterinary toxin binders and provide fresh green grass.",
                "warn": "Never blend mouldy feed with good feed to 'use it up'. Sun-drying does NOT destroy heat-stable mycotoxin poisons.",
                "storage": "Keep remaining unaffected feed elevated on wooden pallets in a dry, ventilated shed away from damp walls.",
                "audio": f"Severe mould danger detected in {feed_type}. Stop feeding immediately to prevent cattle poisoning and sudden milk drop."
            },
            "digestive": {
                "status": "🔴 High Risk - Acute Digestive Acidosis / Spoilage Infection",
                "diag": f"The symptoms (loose dung / bloat / diarrhea) indicate acute rumen acidosis or gut infection caused by spoiled feed, fungal pathogens, or excessive rapid-fermenting starch.",
                "action": f"Withdraw all concentrate feeds and {feed_type} immediately. Provide clean dry straw/hay and clean water with oral electrolytes. Call a veterinarian for antacid treatment.",
                "warn": "Do not give heavy grain mixes, oil cakes, or molasses until normal dung consistency and appetite are restored.",
                "storage": "Check storage shed thoroughly for floor moisture, rodent droppings, and insect infestation.",
                "audio": "Digestive disorder detected in cattle. Stop concentrate feed immediately. Provide dry hay, clean water, and consult a veterinarian."
            },
            "milk_drop": {
                "status": "🟡 Caution - Nutritional Deficit or Early Toxins",
                "diag": f"Sudden milk yield drop after consuming {feed_type} points to either crude protein deficit (< 16%), deficient metabolic energy, or early sub-clinical fungal toxins inhibiting rumen microflora.",
                "action": f"Pause this batch of {feed_type}. Supplement cows with quality protein oil cakes (cottonseed or groundnut cake), 50g mineral mixture, and plenty of clean water and green fodder.",
                "warn": "Do not suddenly overfeed grains to boost milk, as this can trigger severe acidosis.",
                "storage": "Store oil cakes and concentrate bags on wooden slats in a cool, moisture-free room.",
                "audio": "Milk yield drop detected. Withhold current feed. Supplement cattle diet with high-protein oil cake and fresh green fodder."
            },
            "moisture": {
                "status": "🟡 Warning - Moisture Spoilage & Heat Rot Hazard",
                "diag": f"Damp or soaked {feed_type} creates optimal conditions for rapid bacterial heating, sour fermentation, and mould multiplication within 24 to 48 hours.",
                "action": "Untie the bags immediately and spread the feed evenly on a clean plastic tarpaulin under bright sunlight or dry airy shed.",
                "warn": "Never leave wet or soaked feed tied in plastic sacks; anaerobic heat rot will ruin the batch within 24 hours.",
                "storage": "Always elevate bags at least 1 foot above bare floors on wooden pallets. Never store against damp masonry walls.",
                "audio": f"Feed is damp or soaked. High moisture causes rapid rot. Spread {feed_type} on a clean tarpaulin immediately to sun-dry."
            },
            "refusal": {
                "status": "🟡 Caution - Feed Palatability or Contamination Refusal",
                "diag": f"Cattle possess an acute sense of smell. Refusal of {feed_type} usually indicates bitter rancidity, high salt/urea, chemical contamination, or early souring.",
                "action": "Inspect feed for sharp chemical smell, sourness, or burnt odor. Offer a small amount of fresh hay or greens to verify the cow's appetite.",
                "warn": "Do not mix jaggery or molasses to force cattle to consume feed they have rejected.",
                "storage": "Store feed strictly away from fertilizers, diesel, pesticides, and household chemicals.",
                "audio": "Cattle are refusing feed. Check for chemical odor, rancidity, or sourness. Do not force animals to eat rejected feed."
            },
            "particles": {
                "status": "🟡 Warning - Physical Debris / Foreign Contaminant Risk",
                "diag": f"Presence of foreign stones, grit, or insects in {feed_type} causes physical mouth lesions, dental wear, and intestinal blockages in livestock.",
                "action": "Sieve and clean the feed batch through an appropriate mesh before offering it to cattle.",
                "warn": "Do not feed un-sieved feed containing hard gravel or sharp wire debris to calves or cows.",
                "storage": "Keep storage containers tightly covered to prevent insect and rodent access.",
                "audio": f"Foreign debris detected in {feed_type}. Sieve and clean feed thoroughly before giving it to cattle."
            },
            "normal": {
                "status": "🟢 Safe - Standard Feed Guidance",
                "diag": f"Based on your inputs, {feed_type} does not show critical signs of spoilage or chemical contamination.",
                "action": "Feed according to standard dairy ration recommendations with balanced green fodder and fresh drinking water.",
                "warn": "Avoid sudden changes in diet; transition new feed batches gradually over 3 to 5 days.",
                "storage": "Maintain clean, dry, well-ventilated pallet storage protected from rain and pests.",
                "audio": f"{feed_type} appears normal and safe. Feed according to recommended body weight allowances."
            }
        },
        "te": {
            "headers": ("🛑 AI సమస్య విశ్లేషణ (AI Diagnosis):", "🚨 వెంటనే చేయవలసిన పని (Immediate Action):", "⚠️ ఖచ్చితంగా చేయకూడని పని (What NOT to Do):", "🏠 నిల్వ జాగ్రత్త & నివారణ (Storage & Prevention):"),
            "urea": {
                "status": "🔴 అత్యంత ప్రమాదం - యూరియా లేదా రసాయన కల్తీ అనుమానం (High Risk - Urea Spiking)",
                "diag": f"మీరు తెలిపిన వివరాల ప్రకారం {feed_type} మేతలో ఎరువుల యూరియా లేదా ప్రమాదకర రసాయన కల్తీ ఉండే అవకాశం చాలా ఎక్కువగా ఉంది. అధిక యూరియా పశువుల పొట్టలో అమోనియా విషంగా మారి, 1-2 గంటల్లోనే అక్యూట్ రూమెన్ ఆల్కలోసిస్ మరియు ప్రాణాపాయం కలిగిస్తుంది.",
                "action": f"ఈ {feed_type} మేతను పశువులకు ఒక్క పిడికిలి కూడా ఇవ్వవద్దు! వెంటనే బస్తాలను వేరు చేసి భద్రపరచండి. పరీక్ష కోసం స్థానిక డైరీ లేదా పశువైద్యునికి సమాచారం ఇవ్వండి.",
                "warn": "చూడి ఆవులు లేదా దూడలకు ఎట్టి పరిస్థితుల్లోనూ ఈ మేత పెట్టవద్దు. కడిగినా లేదా ఉడకబెట్టినా యూరియా విషం పోదు.",
                "storage": "ఈ బస్తాలపై 'విషపూరితం - పశువులకు ఇవ్వవద్దు' అని స్పష్టంగా రాసి, ఇతర మేత నుండి దూరంగా ఉంచండి.",
                "audio": f"మేతలో తీవ్రమైన యూరియా కల్తీ అనుమానం ఉంది. పశువులకు {feed_type} మేతను వెంటనే ఆపండి! అధిక యూరియా పశువులకు ప్రాణాంతకం."
            },
            "mould": {
                "status": "🔴 తీవ్ర ప్రమాదం - ఫంగస్ మరియు బూజు విషం (High Risk - Mould & Toxins)",
                "diag": f"{feed_type} మేతలో బూజు (ఫంగస్) చేరి ప్రమాదకరమైన మైకోటాక్సిన్లను విడుదల చేసింది. ఇది తింటే పశువుల కాలేయం దెబ్బతింటుంది, పాల దిగుబడి తీవ్రంగా పడిపోతుంది మరియు చూడి పశువులలో గర్భస్రావం జరిగే ప్రమాదం ఉంది.",
                "action": f"ఈ {feed_type} మేతను పశువులకు ఇవ్వడం వెంటనే ఆపండి! బూజు పట్టిన ముద్దలను వేరు చేసి పారవేయండి. పశువులకు టాక్సిన్ బైండర్ మరియు తాజా పచ్చిగడ్డి అందించండి.",
                "warn": "బూజు పట్టిన మేతను మంచి మేతతో కలిపి తినిపించవద్దు. ఎండబెట్టినా మైకోటాక్సిన్ విషాలు నశించవు.",
                "storage": "మిగిలిన మంచి మేతను నేలకు తగలకుండా చెక్క పలకలపై గాలి బాగా ఆడేలా, తేమ లేని గదిలో నిల్వ చేయండి.",
                "audio": f"మేతలో తీవ్రమైన బూజు విషం ఉంది. {feed_type} మేతను వెంటనే ఆపండి! బూజు పట్టిన మేత తింటే పశువులు తీవ్ర అనారోగ్యానికి గురవుతాయి."
            },
            "digestive": {
                "status": "🔴 తీవ్ర ప్రమాదం - విరేచనాలు / కడుపు ఉబ్బరం (High Risk - Digestive Disorder)",
                "diag": f"పశువులకు విరేచనాలు లేదా కడుపు ఉబ్బరం రావడం అనేది మేతలో తడి, కుళ్ళిన పదార్థాలు లేదా మితిమీరిన పిండి పదార్థాల వేగవంతమైన పులియబెట్టడం (రూమెన్ అసిడోసిస్) వల్ల వస్తుంది.",
                "action": f"దాణా మరియు {feed_type} మేతను వెంటనే నిలిపివేయండి! పశువులకు మంచి ఎండుగడ్డి, ఎలక్ట్రోలైట్ లేదా ఉప్పు నీరు ఇవ్వండి. వెంటనే పశువైద్యుని పిలిపించండి.",
                "warn": "విరేచనాలు తగ్గే వరకు ఎలాంటి పిండి పదార్థాలు లేదా నూనె చెక్క ఎక్కువగా తినిపించవద్దు.",
                "storage": "మేతలో ఎలుకల మలమూత్రాలు, వర్షపు నీరు లేదా బూజు చేరకుండా శుభ్రమైన గదిలో భద్రపరచండి.",
                "audio": "పశువులకు విరేచనాలు లేదా కడుపు ఉబ్బరం వచ్చింది. దాణా మేతను వెంటనే ఆపండి. ఎండుగడ్డి, మంచినీరు ఇచ్చి పశువైద్యుని సంప్రదించండి."
            },
            "milk_drop": {
                "status": "🟡 జాగ్రత్త - పోషకాల లోపం లేదా జీర్ణ అసమతుల్యత (Caution - Milk Drop)",
                "diag": f"{feed_type} తిన్న తర్వాత పాల దిగుబడి తగ్గడానికి ప్రధాన కారణం మేతలో ప్రొటీన్ (మాంసకృత్తులు) తక్కువగా ఉండటం లేదా కంటికి కనిపించని బూజు టాక్సిన్లు జీర్ణక్రియను అణచివేయడం.",
                "action": f"ఈ {feed_type} మేతను తాత్కాలికంగా ఆపివేయండి. పశువులకు వేరుశనగ చెక్క లేదా పత్తిగింజల చెక్క, 50 గ్రాముల మినరల్ మిశ్రమం మరియు తాజా పచ్చిగడ్డిని అందించండి.",
                "warn": "పాల దిగుబడి పెంచడానికి ఒకేసారి అధిక మోతాదులో దాణా ఇవ్వవద్దు, ఇది కడుపు ఉబ్బరానికి దారితీస్తుంది.",
                "storage": "దాణా మరియు చెక్క బస్తాలను తేమ నేలకు తగలకుండా చెక్క పలకలపై గాలి ఆడేలా భద్రపరచండి.",
                "audio": f"పాల దిగుబడి అకస్మాత్తుగా తగ్గింది. ప్రస్తుత {feed_type} మేతను ఆపి, పత్తిగింజల చెక్క లేదా వేరుశనగ చెక్క మరియు తాజా పచ్చిగడ్డి ఇవ్వండి."
            },
            "moisture": {
                "status": "🟡 హెచ్చరిక - అధిక తేమ వల్ల మేత కుళ్ళే ప్రమాదం (Moisture Spoilage)",
                "diag": f"{feed_type} మేత తడిసిపోవడం వల్ల తేమ శాతం పెరిగి 24 నుండి 48 గంటల్లోనే వేడెక్కి, పులిసిపోయి బూజు పడుతుంది.",
                "action": "వెంటనే బస్తాలు విప్పి శుభ్రమైన టార్పాలిన్ లేదా పరదాపై ఎండలో లేదా గాలి తగిలేలా బాగా ఆరబెట్టండి.",
                "warn": "తడిసిన మేతను అలాగే బస్తాల్లో కట్టి ఉంచవద్దు, గాలి ఆడక లోపల తీవ్రంగా కుళ్ళిపోతుంది.",
                "storage": "ఎప్పుడూ నేరుగా నేలపై బస్తాలు పెట్టకండి, చెక్క బల్లలపై నేలకు 1 అడుగు ఎత్తులో ఉంచండి.",
                "audio": f"మేత తడిసిపోయింది. తడిసిన {feed_type} త్వరగా కుళ్ళిపోతుంది. వెంటనే బస్తాలు విప్పి ఎండలో బాగా ఆరబెట్టండి."
            },
            "refusal": {
                "status": "🟡 జాగ్రత్త - మేత రుచి లేదా వాసన మార్పు (Feed Refusal)",
                "diag": f"పశువులకు వాసన చూసే శక్తి చాలా ఎక్కువ. {feed_type} మేతలో రసాయనాల వాసన, అధిక ఉప్పు, లేదా నూనె వాసన వచ్చినప్పుడు అవి తినడానికి నిరాకరిస్తాయి.",
                "action": f"ఈ {feed_type} మేతలో ఘాటైన రసాయనాల వాసన లేదా చేదు రుచి ఉందేమో పరిశీలించండి. పశువులకు సాధారణ ఎండుగడ్డి లేదా పచ్చిగడ్డి ఇచ్చి చూడండి.",
                "warn": "బెల్లం లేదా ఉప్పు కలిపి పశువులతో బలవంతంగా పాడైన మేతను తినిపించవద్దు.",
                "storage": "పురుగుమందులు మరియు రసాయనిక ఎరువులకు దూరంగా మేతను భద్రపరచండి.",
                "audio": "పశువులు మేత తినడానికి నిరాకరిస్తున్నాయి. మేతలో రసాయనాలు లేదా పుల్లని వాసన ఉందేమో చూడండి. బలవంతంగా తినిపించవద్దు."
            },
            "particles": {
                "status": "🟡 హెచ్చరిక - రాళ్ళు లేదా పనికిరాని వ్యర్థాలు (Physical Particles)",
                "diag": f"{feed_type} మేతలో రాళ్ళు, పురుగులు లేదా ముళ్ళు ఉండటం వల్ల పశువుల నోటికి గాయాలు మరియు కడుపులో అడ్డంకులు ఏర్పడతాయి.",
                "action": "పశువులకు ఇచ్చే ముందు జల్లెడ పట్టి రాళ్ళు, పురుగులు మరియు ఇతర వ్యర్థాలను పూర్తిగా తొలగించండి.",
                "warn": "రాళ్ళు మరియు పదునైన చెత్త ఉన్న మేతను దూడలకు ఎట్టి పరిస్థితుల్లోనూ ఇవ్వవద్దు.",
                "storage": "పురుగులు చేరకుండా మేత నిల్వ పాత్రలను మూసి ఉంచండి.",
                "audio": f"మేతలో రాళ్ళు లేదా వ్యర్థాలు కనిపించాయి. {feed_type} మేతను జల్లెడ పట్టి శుభ్రం చేసిన తర్వాతే పశువులకు ఇవ్వండి."
            },
            "normal": {
                "status": "🟢 పశువుల మేత సాధారణమైనది - సురక్షితం (Normal & Safe)",
                "diag": f"మీరు అందించిన వివరాల ప్రకారం {feed_type} మేత సాధారణ స్థితిలో ఉన్నట్లు కనిపిస్తోంది.",
                "action": "పశువుల శరీర బరువును బట్టి తగిన మోతాదులో సమతుల్య ఆహారం మరియు మంచి తాగునీరు అందించండి.",
                "warn": "మేత రకాన్ని మార్చేటప్పుడు 3-5 రోజుల వ్యవధిలో నెమ్మదిగా మార్చండి.",
                "storage": "మేత నిల్వ ఉన్న గది పొడిగా మరియు గాలి బాగా వచ్చేలా చూసుకోండి.",
                "audio": f"{feed_type} మేత సాధారణంగా మరియు సురక్షితంగా ఉంది. నిర్దేశిత పరిమాణంలో పశువులకు ఇవ్వవచ్చు."
            }
        },
        "hi": {
            "headers": ("🛑 AI समस्या विश्लेषण (AI Diagnosis):", "🚨 तुरंत क्या करें (Immediate Action):", "⚠️ क्या न करें (What NOT to Do):", "🏠 भंडारण सलाह व रोकथाम (Storage & Prevention):"),
            "urea": {
                "status": "🔴 अत्यंत खतरनाक - यूरिया या रासायनिक मिलावट की आशंका (High Risk - Urea Spiking)",
                "diag": f"{feed_type} में यूरिया या रासायनिक मिलावट की गंभीर आशंका है। अत्यधिक यूरिया से पशुओं के पेट में तीव्र अमोनिया जहर बनता है जो 1-2 घंटे में जानलेवा हो सकता है।",
                "action": f"पशुओं को यह {feed_type} एक मुट्ठी भी न दें! बोरियों को तुरंत अलग करें और डेयरी अधिकारी या डॉक्टर से जांच करवाएं।",
                "warn": "गाभिन गाय-भैंसों या बछड़ों को यह बिल्कुल न खिलाएं। धोने या पकाने से भी यूरिया का जहर खत्म नहीं होता।",
                "storage": "इन बोरियों पर 'खतरा - पशुओं को न दें' लिखकर अलग रखें।",
                "audio": f"चारे में यूरिया मिलावट की गंभीर आशंका है। पशुओं को {feed_type} तुरंत रोकें! यूरिया पशुओं के लिए जानलेवा है।"
            },
            "mould": {
                "status": "🔴 उच्च जोखिम - फफूंद और मायकोटॉक्सिन खतरा (High Risk - Mould & Toxins)",
                "diag": f"{feed_type} में फफूंद (उल्ली) संक्रमण से खतरनाक मायकोटॉक्सिन पैदा हो गए हैं, जो पशुओं के लिवर को नुकसान पहुंचाते हैं और दूध उत्पादन घटाते हैं।",
                "action": f"पशुओं को यह {feed_type} तुरंत बंद करें! फफूंद लगे हिस्से को अलग करके नष्ट करें। पशुओं को टॉक्सिन बाइंडर और ताजा हरा चारा दें।",
                "warn": "फफूंद लगे चारे को अच्छे चारे में मिलाकर न खिलाएं। सुखाने से भी फंगल टॉक्सिन नष्ट नहीं होते।",
                "storage": "बचे हुए चारे को साफ तिरपाल पर धूप में सुखाएं और सूखे हवादार स्थान पर रखें।",
                "audio": f"चारे में फफूंद और टॉक्सिन का खतरा है। पशुओं को {feed_type} तुरंत बंद करें।"
            },
            "digestive": {
                "status": "🔴 उच्च जोखिम - दस्त या पेट फूलना (High Risk - Acidosis / Bloat)",
                "diag": f"पशुओं को दस्त या पेट फूलना सड़े हुए चारे, फफूंद या बहुत जल्दी पचने वाले स्टार्च से होने वाले एसिडोसिस का परिणाम है।",
                "action": f"दाना और {feed_type} तुरंत रोकें! पशुओं को सूखा भूसा और पानी में इलेक्ट्रोलाइट दें। तुरंत पशु चिकित्सक को बुलाएं।",
                "warn": "पशु के ठीक होने तक कोई भारी अनाज या तेल वाली खली न खिलाएं।",
                "storage": "चारे को सीलन और चूहों की गंदगी से सुरक्षित रखें।",
                "audio": "पशुओं को दस्त या पेट फूलने की समस्या है। दाना तुरंत बंद करें। सूखा भूसा दें और डॉक्टर को बुलाएं।"
            },
            "milk_drop": {
                "status": "🟡 सावधानी - पोषण की कमी या शुरुआती टॉक्सिन (Caution - Milk Drop)",
                "diag": f"{feed_type} खाने के बाद दूध उत्पादन में गिरावट का मुख्य कारण चारे में प्रोटीन की कमी या सूक्ष्म फफूंद टॉक्सिन है।",
                "action": f"इस {feed_type} को अस्थायी रूप से रोकें। पशुओं को बिनौला या सरसों की खली, खनिज मिश्रण और ताजा हरा चारा दें।",
                "warn": "दूध बढ़ाने के लिए अचानक बहुत अधिक दाना न दें, इससे एसिडोसिस हो सकता है।",
                "storage": "दाने और खली की बोरियों को लकड़ी के तख्तों पर रखें।",
                "audio": f"दूध उत्पादन में गिरावट आई है। {feed_type} रोककर पशुओं को खली और हरा चारा दें।"
            },
            "moisture": {
                "status": "🟡 चेतावनी - नमी से सड़न का खतरा (Moisture Spoilage)",
                "diag": f"{feed_type} में नमी बढ़ने से 24-48 घंटों के भीतर तेजी से फफूंद और सड़न शुरू हो जाती है।",
                "action": "बोरियों को तुरंत खोलकर साफ तिरपाल पर धूप या खुली हवा में अच्छी तरह सुखाएं।",
                "warn": "भीगे हुए चारे को बंद बोरियों में न छोड़ें, इससे चारा गर्म होकर सड़ जाएगा।",
                "storage": "बोरियों को जमीन की नमी से दूर लकड़ी के पटरों पर रखें।",
                "audio": f"चारा भीग गया है। {feed_type} को तुरंत धूप में फैलाकर सुखाएं ताकि फफूंद न लगे।"
            },
            "refusal": {
                "status": "🟡 सावधानी - चारा न खाने की समस्या (Feed Refusal)",
                "diag": f"पशुओं की सूंघने की क्षमता तेज होती है। {feed_type} में रासायनिक गंध, कड़वापन या यूरिया होने पर वे चारा छोड़ देते हैं।",
                "action": f"{feed_type} में किसी रासायनिक या सड़ी गंध की जांच करें। पशुओं को ताजा हरा चारा देकर भूख जांचें।",
                "warn": "गुड़ या नमक मिलाकर जबरदस्ती खराब चारा न खिलाएं।",
                "storage": "कीटनाशक और खाद से चारे को दूर रखें।",
                "audio": "पशु चारा खाने से मना कर रहे हैं। चारे में दुर्गंध या रसायन की जांच करें।"
            },
            "particles": {
                "status": "🟡 चेतावनी - कंकड़ या कीड़े (Physical Contaminants)",
                "diag": f"{feed_type} में कंकड़, पत्थर या कीड़े होने से पशुओं के मुंह में घाव और पेट में रुकावट हो सकती है।",
                "action": "पशुओं को देने से पहले चारे को अच्छी तरह छानकर नुकीले कणों और कीड़ों को अलग करें।",
                "warn": "कंकड़-युक्त चारे को बिना छाने छोटे बछड़ों को न दें।",
                "storage": "भंडारण कक्ष को साफ रखें और चारे के बर्तनों को ढंक कर रखें।",
                "audio": f"चारे में कंकड़ या कीड़े दिखाई दिए हैं। {feed_type} को अच्छी तरह छानकर ही पशुओं को खिलाएं।"
            },
            "normal": {
                "status": "🟢 पशु आहार सामान्य व सुरक्षित है (Normal & Safe)",
                "diag": f"आपके विवरण के अनुसार {feed_type} सामान्य स्थिति में है।",
                "action": "पशुओं को संतुलित आहार, हरा चारा और स्वच्छ पानी निर्धारित मात्रा में दें।",
                "warn": "चारा बदलते समय अचानक न बदलें, 3-5 दिन में धीरे-धीरे बदलें।",
                "storage": "भंडारण कक्ष को सूखा और हवादार रखें।",
                "audio": f"{feed_type} सामान्य और सुरक्षित है। इसे पशुओं को सुरक्षित रूप से खिलाया जा सकता है।"
            }
        }
    }

    pack = kbp.get(lang, kbp["en"])
    headers = pack["headers"]

    # Priority Evaluation Order: Urea -> Mould -> Digestive -> Milk Drop -> Moisture -> Refusal -> Particles -> Normal
    chosen_cat = "normal"
    if urea_flag:
        chosen_cat = "urea"
    elif mould_flag:
        chosen_cat = "mould"
    elif digestive_flag:
        chosen_cat = "digestive"
    elif milk_drop_flag:
        chosen_cat = "milk_drop"
    elif moisture_flag:
        chosen_cat = "moisture"
    elif refusal_flag:
        chosen_cat = "refusal"
    elif insects_particles_flag:
        chosen_cat = "particles"

    rec = pack[chosen_cat]

    full_text = (
        f"{rec['status']}\n\n"
        f"{headers[0]}\n{rec['diag']}\n\n"
        f"{headers[1]}\n{rec['action']}\n\n"
        f"{headers[2]}\n{rec['warn']}\n\n"
        f"{headers[3]}\n{rec['storage']}"
    )

    return {
        "safety_status": rec["status"],
        "farmer_statement": query or f"Custom Inspection: {feed_type}",
        "main_problems": [rec["diag"]],
        "recommended_actions": [rec["action"], rec["warn"]],
        "storage_advice": rec["storage"],
        "full_advisory_text": full_text.strip(),
        "audio_summary": rec.get("audio", rec["action"]),
        "language": lang,
        "provider": "SmartFeed AI Multilingual Diagnostic Engine",
        "is_offline_fallback": True,
        "is_manual": True
    }


def generate_advisory(
    analysis_data: Dict[str, Any],
    language: str = "en",
    provider: str = "auto"
) -> Dict[str, Any]:
    """
    Main advisory dispatch function:
    1. If manual query / custom symptoms provided, routes to analyze_manual_farmer_entry.
    2. If preset problem statement requested, generates preset KB advisory.
    3. Attempts online LLM generation if configured and accessible.
    4. Automatically falls back to offline multilingual rule-based advisory.
    
    Args:
        analysis_data: Complete dictionary with scores, hazards, nutrients, query or problem_id.
        language: 'en', 'te', or 'hi'.
        provider: 'auto', 'openai', 'claude', or 'offline'.
        
    Returns:
        dict: Complete structured multilingual advisory.
    """
    # Check if manual query / symptom inputs exist
    is_manual = (
        analysis_data.get("is_manual")
        or bool(analysis_data.get("manual_query"))
        or (bool(analysis_data.get("query")) and not analysis_data.get("problem_id"))
        or bool(analysis_data.get("cattle_symptom") and analysis_data.get("cattle_symptom") != "Normal")
    )
    if is_manual:
        return analyze_manual_farmer_entry(analysis_data, language=language, provider=provider)

    if provider.lower() != "offline":
        llm_res = generate_llm_advisory(analysis_data, language=language, provider=provider)
        if llm_res is not None:
            return llm_res

    # Default to robust offline advisory
    return generate_offline_advisory(analysis_data, language=language)
