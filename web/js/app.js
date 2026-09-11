/**
 * SmartFeed AI - Client-Side JavaScript Application Module
 * Handles:
 * - Tab Navigation (SPA)
 * - File Drag-and-Drop & Preset Sample Previews
 * - Full-Spectrum Diagnostic Scanning (API -> /api/scan)
 * - Animated SVG Radial Score Gauge (0–100)
 * - Explainable AI Itemized Deduction Breakdown
 * - Real-Time Adulteration Simulation (API -> /api/check-adulteration)
 * - Multilingual Voice Advisory (Web Speech API + Audio Soundwaves)
 * - Real-Time Dashboard (Chart.js Trend & Risk Distribution)
 * - Digital Feed Passport & QR Verification
 */

// Global Application State
const state = {
    currentTab: 'home',
    selectedFile: null,
    selectedPreset: '',
    currentScanResult: null,
    language: 'te', // Default to Telugu as requested by user
    advisoryMode: 'auto',
    advisoryInputMode: 'preset', // 'preset' or 'manual'
    isSpeaking: false,
    selectedProblemId: 'milk_drop',
    audioPlayer: null,
    currentAudioUrl: null,
    farmerProblems: [],
    charts: {
        trend: null,
        pie: null
    },
    currentUser: JSON.parse(localStorage.getItem('smartfeed_user') || 'null'),
    farmerProfile: null,
    farmerAnimals: [],
    wizardData: {
        step: 1,
        farmerName: '',
        village: '',
        language: 'te',
        animalCount: 3,
        types: ['Cow', 'Buffalo'],
        animals: [],
        mainFeed: 'Green Fodder',
        storage: 'Shed'
    }
};
window.state = state;

// ===================================================================
// Whole-App Multilingual Dictionary (Telugu, Hindi, English)
// ===================================================================
const I18N_APP = {
    te: {
        // Sidebar Navigation
        'sidebar-brand-title': 'SmartFeed AI',
        'sidebar-brand-slogan': 'మేత స్మార్ట్ • పాడి క్షేమం',
        'sidebar-status-text': 'ఆఫ్‌లైన్ సిద్ధం • స్థానిక AI కార్యాచరణలో ఉంది',
        'nav-home': 'హోమ్',
        'nav-scanner': 'నాణ్యత స్కానర్',
        'nav-adulteration': 'కల్తీ నిర్ధారణ',
        'nav-advisory': 'రైతు AI సలహాలు',
        'nav-dashboard': 'డాష్‌బోర్డ్',
        'nav-passport': 'ఫీడ్ పాస్‌పోర్ట్',
        'nav-lookup': 'బ్యాచ్ శోధన',
        'btn-reopen-lang-text': '🌐 భాష మార్చండి (Language)',
        'mobile-lang-btn-text': 'భాష / Lang',
        'sidebar-lang-label': 'రైతు భాష',
        'sidebar-engine-label': 'సలహా ఇంజిన్',
        'sidebar-footer-text': '<strong>స్మార్ట్ ఇండియా హ్యాకథాన్ 2026</strong><br>తక్కువ ఖర్చుతో కూడిన సాఫ్ట్‌వేర్ నమూనా<br>ప్రత్యేక హార్డ్‌వేర్ అవసరం లేదు',

        // Tab 1: Home
        'hero-badge-text': 'స్మార్ట్ ఇండియా హ్యాకథాన్ 2026 • AI అగ్రి-టెక్ ఆవిష్కరణ',
        'hero-title-text': 'SmartFeed AI',
        'hero-motto-text': 'మేత స్మార్ట్ • పాడి క్షేమం • కలిసి ఎదుగుదాం',
        'hero-desc-text': 'కృత్రిమ మేధస్సు (AI) ఆధారిత పశుగ్రాసం & సైలేజ్ నాణ్యత పరిశీలన, కల్తీ గుర్తింపు, బహుళ అంశాల రిస్క్ విశ్లేషణ మరియు రైతులకు స్పష్టమైన వాయిస్ సలహాలు.',
        'home-btn-scan': 'నాణ్యత స్కానర్',
        'home-btn-adulteration': 'కల్తీ నిర్ధారణ',
        'home-btn-advisory': 'రైతు సలహాలు',
        'home-sci-notice': '<strong>శాస్త్రీయ ప్రయోగ నమూనా సూచన:</strong> స్మార్ట్ ఫీడ్ AI కంప్యూటర్ విజన్, కలర్/టెక్స్చర్ విశ్లేషణ మరియు బహుళ-కారకాల రిస్క్ అంచనాను అందిస్తుంది. ఇది పాడి రైతులకు సహాయక నిర్ణయ వేదికగా రూపొందించబడింది. రసాయనిక నిర్ధారణకు ల్యాబ్ పరీక్ష సిఫార్సు చేయబడింది.',
        'home-tele-edge-label': 'ఎడ్జ్ AI ఇంజిన్',
        'home-tele-edge-val': '< 300ms వేగవంతమైన స్పందన',
        'home-tele-risk-label': 'రిస్క్ నిఘా వేదిక',
        'home-tele-risk-val': '6-కారకాల సమగ్ర విశ్లేషణ',
        'home-tele-voice-label': 'బహుభాషా వాయిస్',
        'home-tele-voice-val': 'తెలుగు • हिंदी • EN',
        'home-tele-trace-label': 'డిజిటల్ ధృవీకరణ',
        'home-tele-trace-val': 'QR డిజిటల్ పాస్‌పోర్ట్',
        'home-why-title': '🌟 స్మార్ట్ ఫీడ్ AI ఎందుకు?',
        'home-why-p1': 'పాడి రైతులు మరియు పాల సహకార సంఘాలు తరచుగా <strong>మేత చెడిపోవడం, ఫంగస్/బూజు టాక్సిన్లు, మరియు యూరియా కల్తీ</strong> కారణంగా పాల దిగుబడి పడిపోవడం, పశువుల అనారోగ్య సమస్యలను ఎదుర్కొంటున్నారు.',
        'home-why-p2': 'సాంప్రదాయ పద్ధతుల్లో ఖరీదైన ప్రయోగశాల పరీక్షలు అవసరమవుతాయి, ఇవి గ్రామీణ రైతులకు సులభంగా అందుబాటులో ఉండవు.',
        'home-pitch-box': '<strong>💡 SIH ప్రాజెక్ట్ లక్ష్యం:</strong><p style="color: var(--slate-700); font-size: 0.92rem; margin-top: 6px;"><em>"స్మార్ట్ ఫీడ్ AI సాధారణ స్మార్ట్‌ఫోన్ కెమెరాను పశుగ్రాస నాణ్యతను పరీక్షించే ఇంటెలిజెంట్ ల్యాబ్‌గా మారుస్తుంది. ఇది కంప్యూటర్ విజన్, యూరియా కల్తీ నిఘా, స్థానిక భాషా వాయిస్ మరియు QR పాస్‌పోర్ట్‌లను అందిస్తుంది."</em></p>',
        'home-usps-title': '🏆 ముఖ్యమైన ఆవిష్కరణలు (USPs)',
        'home-usps-list': `
            <li>⭐ <strong>స్మార్ట్‌ఫీడ్ హెల్త్ స్కోర్ (0–100)</strong>: దృశ్య పరీక్ష, బూజు, పోషకాలు, నిల్వ ఆధారంగా ఏకైక సమగ్ర పారదర్శక స్కోర్.</li>
            <li>🔍 <strong>కారణాల విశ్లేషణ ("ఈ ఫలితం ఎందుకు వచ్చింది?")</strong>: మేత ఎందుకు ప్రమాదకరమో పాయింట్ల వారీగా స్పష్టమైన వివరణ.</li>
            <li>🗣️ <strong>బహుభాషా వాయిస్ సలహాలు</strong>: <strong>తెలుగు, హిందీ, ఇంగ్లీష్</strong> లలో బ్రౌజర్ ఆడియో ద్వారా రైతులకు తక్షణ సూచనలు.</li>
            <li>📦 <strong>QR డిజిటల్ ఫీడ్ పాస్‌పోర్ట్</strong>: పాల సహకార సంఘాల కోసం ట్యాంపర్-ప్రూఫ్ బ్యాచ్ సర్టిఫికేట్లు.</li>
            <li>📈 <strong>ముందస్తు క్షీణత హెచ్చరికలు</strong>: కంటికి కుళ్లు కనిపించకముందే నాణ్యత తగ్గడాన్ని గుర్తించే ట్రాజెక్టరీ విశ్లేషణ.</li>
            <li>📶 <strong>100% ఆఫ్‌లైన్ కార్యాచరణ</strong>: ఇంటర్నెట్ లేకపోయినా నిరంతరాయంగా పనిచేస్తుంది.</li>
        `,
        'home-btn-scan': 'నాణ్యత స్కానర్',
        'home-btn-adulteration': 'కల్తీ నిర్ధారణ',
        'home-btn-advisory': 'రైతు సలహాలు',
        'home-btn-dashboard': 'డాష్‌బోర్డ్',
        'home-quick-title': '🚀 ముఖ్య సేవలు త్వరిత ప్రారంభం',
        'home-card1-title': '1. మేత స్కానర్',
        'home-card1-desc': 'ఫోటో అప్‌లోడ్ చేసి రంగు మార్పులు, బూజు ముద్దలు మరియు కణాలను పరీక్షించండి.',
        'btn-home-card1': '🚀 స్కానర్ తెరవండి',
        'home-card2-title': '2. కల్తీ నిర్ధారణ',
        'home-card2-desc': 'యూరియా స్పైకింగ్ మరియు నాన్-ప్రోటీన్ నైట్రోజన్ రిస్క్‌ను స్లైడర్లతో పరీక్షించండి.',
        'btn-home-card2': '🔬 కల్తీ పరీక్షించండి',
        'home-card3-title': '3. రైతు సలహాలు',
        'home-card3-desc': 'తెలుగు, హిందీ లేదా ఇంగ్లీషులో నిపుణుల వాయిస్ సూచనలను వినండి.',
        'btn-home-card3': '🗣️ వాయిస్ సలహా',
        'home-card4-title': '4. ఎనలిటిక్స్ డాష్‌బోర్డ్',
        'home-card4-desc': 'లైవ్ నాణ్యత ట్రెండ్‌లు, రిస్క్ విభజన మరియు ముందస్తు క్షీణత హెచ్చరికలు.',
        'btn-home-card4': '📈 డాష్‌బోర్డ్ చూడండి',
        'home-card5-title': '5. QR పాస్‌పోర్ట్',
        'home-card5-desc': 'పాల సహకార సంఘాల కోసం డిజిటల్ ఫీడ్ పాస్‌పోర్ట్‌ను డౌన్‌లోడ్ చేయండి.',
        'btn-home-card5': '📜 పాస్‌పోర్ట్ చూడండి',
        'btn-refresh-dashboard': '🔄 తాజా చేయండి',

        // Step 5: Farmer Personalized Dashboard & Tools
        'guest-card-title': 'రైతు లాగిన్ & ఫారమ్ ప్రొఫైల్ సెటప్',
        'guest-card-sub': 'మీ పశువుల సంఖ్యను నమోదు చేయడానికి, ఆవులు & గేదెల ఆరోగ్యాన్ని పర్యవేక్షించడానికి లాగిన్ అవ్వండి!',
        'btn-guest-login': '🔑 లాగిన్ (Sign In)',
        'btn-guest-register': '📝 నమోదు (Register)',
        'title-farmer-features': '🌟 పాడి రైతు నిర్ధారణ & సలహా కేంద్రం (8 ముఖ్య సేవలు)',
        'btn-edit-farm': '⚙️ ఫారమ్ మార్చండి',
        'btn-dash-new-scan': '📸 నేటి మేత పరీక్షించండి',
        'fd-lbl-cows': 'ఆవులు (Cows)',
        'fd-lbl-buffs': 'గేదెలు (Buffs)',
        'fd-lbl-lact': 'పాలిచ్చేవి (Lactating)',
        'fd-lbl-preg': 'చూడి (Pregnant)',
        'fd-lbl-feed': 'ప్రధాన మేత',
        'fd-lbl-storage': 'నిల్వ స్థలం',
        'fd-lbl-tests': 'పరీక్షలు (Tests)',
        'tile1-title': '1. మేత స్కానర్',
        'tile1-sub': 'నాణ్యత & బూజు పరీక్ష',
        'tile1-desc': 'ఫోటో తీసి రంగు మార్పు, బూజు, కణాలు & 0-100 ఆరోగ్య స్కోర్ తెలుసుకోండి.',
        'tile1-btn': '🚀 స్కానర్ తెరవండి →',
        'tile2-title': '2. యూరియా కల్తీ & మోతాదు',
        'tile2-sub': 'సేఫ్ యూరియా గణన',
        'tile2-desc': 'యూరియా కల్తీ నిఘా మరియు ICAR 4% గడ్డి చికిత్స సురక్షిత మోతాదు లెక్కించండి.',
        'tile2-btn': '🔬 సేఫ్ యూరియా లెక్కించండి →',
        'tile3-title': '3. రైతు AI సలహాలు',
        'tile3-sub': 'తెలుగు వాయిస్ సలహాలు',
        'tile3-desc': 'మీ పశువుల స్థితికి అనుగుణంగా తెలుగు, హిందీ లేదా ఇంగ్లీషులో వాయిస్ సలహాలు వినండి.',
        'tile3-btn': '🗣️ వాయిస్ సలహా వినండి →',
        'tile4-title': '4. నా పశువులు',
        'tile4-sub': 'వ్యక్తిగత పశువుల వివరాలు',
        'tile4-desc': 'మీ ఆవులు, గేదెల వయస్సు, పాలిచ్చే స్థితి మరియు మేత లక్ష్యాలను తనిఖీ చేయండి.',
        'tile4-btn': '🐄 పశువుల జాబితా →',
        'tile5-title': '5. మేత డైరీ',
        'tile5-sub': 'రోజువారీ మేత లాగ్',
        'tile5-desc': 'రోజువారీ మేత వివరాలు, నిల్వ తాజాదనం మరియు దాణా వినియోగం నమోదు చేయండి.',
        'tile5-btn': '📝 మేత డైరీ చూడండి →',
        'tile6-title': '6. నా డాష్‌బోర్డ్',
        'tile6-sub': 'ఫారమ్ ఎనలిటిక్స్',
        'tile6-desc': 'మేత నాణ్యత ట్రెండ్‌లు, రిస్క్ విభజన మరియు ముందస్తు క్షీణత హెచ్చరికలు చూడండి.',
        'tile6-btn': '📈 డాష్‌బోర్డ్ తెరవండి →',
        'tile7-title': '7. పరీక్షల చరిత్ర',
        'tile7-sub': 'గత బ్యాచ్ రికార్డులు',
        'tile7-desc': 'గతంలో చేసిన మేత పరీక్షలు, స్కోర్లు మరియు సర్టిఫికేట్లను సమీక్షించండి.',
        'tile7-btn': '📋 చరిత్ర చూడండి →',
        'tile8-title': '8. QR పాస్‌పోర్ట్',
        'tile8-sub': 'డిజిటల్ ఫీడ్ పాస్‌పోర్ట్',
        'tile8-desc': 'పాల సహకార సంఘాల కోసం ధృవీకరించిన QR కోడ్ సర్టిఫికేట్ పొందండి.',
        'tile8-btn': '📦 పాస్‌పోర్ట్ చూడండి →',

        // Farmer History Section
        'farmer-history-section-title': '<span>📜</span> <span>నా గత మేత పరీక్షల రికార్డులు (My Feed Diagnostic History)</span>',
        'farmer-history-section-sub': 'మీ ఫారమ్‌లో గతంలో విశ్లేషించిన మేత బ్యాచ్‌లు, నాణ్యత స్కోర్లు, సేఫ్టీ అలర్టులు మరియు డిజిటల్ పాస్‌పోర్ట్‌లు',
        'btn-refresh-farmer-history': 'రిఫ్రెష్ (Refresh)',
        'btn-new-scan-farmer-history': 'కొత్త పరీక్ష (New Scan)',
        'fth-batch': 'బ్యాచ్ ID (Batch ID)',
        'fth-sample': 'మేత రకం (Sample)',
        'fth-score': 'నాణ్యత స్కోర్ (Score)',
        'fth-badge': 'స్థితి (Status)',
        'fth-concern': 'ప్రధాన రిస్క్ / పరిశీలన (Findings)',
        'fth-shelf': 'షెల్ఫ్ లైఫ్ (Shelf Life)',
        'fth-date': 'తేదీ (Date)',
        'fth-action': 'చర్యలు (Action)',
        'modal-history-title': 'నా మేత పరీక్షల రికార్డులు / Test History',

        // Tab 2: Quality Scanner
        'scanner-header-title': '📸 స్మార్ట్ ఫీడ్ నాణ్యత స్కానర్',
        'scanner-header-subtitle': 'కంప్యూటర్ విజన్, బహుళ-కారకాల రిస్క్ విశ్లేషణ & డిజిటల్ ఫీడ్ పాస్‌పోర్ట్ ఉత్పత్తి',
        'scanner-step1-title': '1. మేత నమూనాను ఎంచుకోండి లేదా ఫోటో తీయండి',
        'scanner-preset-label': '⚡ 1-క్లిక్ డెమో నమూనాల పరీక్ష',
        'scanner-dropzone-title': 'మేత ఫోటోను ఇక్కడ వేయండి లేదా ఎంచుకోండి',
        'scanner-dropzone-sub': 'JPG, PNG, WEBP సపోర్ట్ చేస్తుంది',
        'scanner-sample-type-label': 'నమూనా రకం వర్గీకరణ',
        'scanner-step2-title': '2. పోషక మరియు నిల్వ వివరాలు',
        'label-slider-cp': 'క్రూడ్ ప్రోటీన్ (CP %)',
        'label-slider-moisture': 'తేమ శాతం (Moisture %)',
        'label-slider-npn': 'నాన్-ప్రోటీన్ నైట్రోజన్ (NPN %)',
        'label-slider-days': 'నిల్వ చేసిన రోజులు (Days)',
        'label-check-smell': 'పుల్లని లేదా బూజు దుర్వాసన వస్తోంది',
        'btn-scan': '🚀 సమగ్ర నాణ్యత పరీక్ష చేయండి',
        'scanner-step3-title': '3. స్మార్ట్ ఫీడ్ నిర్ధారణ ఫలితాలు',
        'results-placeholder-title': 'నమూనా కోసం ఎదురుచూస్తోంది',
        'results-placeholder-desc': 'డెమో నమూనాను ఎంచుకోండి లేదా ఫోటో అప్‌లోడ్ చేసి "పరీక్ష చేయండి" బటన్ నొక్కండి.',
        'gauge-heading': '🐄 స్మార్ట్ ఫీడ్ ఆరోగ్య స్కోర్',
        'gauge-score-sub': '100 కి గాను',
        'shelf-life-card-title': '⏳ AI మేత నిల్వ కాలం & పాడయ్యే గడువు అంచనా',
        'shelf-days-label': 'రోజుల పాటు సురక్షితం',
        'shelf-sub-expiry-label': 'సురక్షిత గడువు:',
        'shelf-sub-moist-label': 'తేమ ప్రభావం:',
        'shelf-timeline-now': 'ఈరోజు / తాజా',
        'shelf-timeline-status': 'సాధారణ నిల్వ కాలం',
        'shelf-timeline-spoil': 'పాడయ్యే ప్రమాద సమయం',
        'cert-lbl-shelf': 'నిల్వ కాలం & గడువు',
        'animal-rec-header-title': 'పశువుల వారీగా మేత సిఫార్సు & రోజువారీ మోతాదు',
        'animal-rec-header-sub': 'Animal-Specific Feed Recommendation • ICAR Dairy Cattle Nutrition Benchmarks',
        'btn-speak-animal-rec-txt': 'వాయిస్ సలహా వినండి (Audio)',
        'lbl-quick-animal-select': '⚡ నా పశువుల నుండి ఎంచుకోండి (1-Click Cattle Quick-Pick):',
        'lbl-rec-species': '🐄 పశువు రకం / Animal Type',
        'lbl-rec-stage': '🤰 శారీరక స్థితి / Stage',
        'lbl-rec-milk': '🥛 పాల ఉత్పత్తి / Yield',
        'btn-recalculate-rec-txt': 'సిఫార్సు లెక్కించండి',
        'lbl-rec-daily-dose': 'మొత్తం రోజువారీ మోతాదు',
        'lbl-rec-daily-sub': 'రోజూ ఇవ్వవలసిన దాణా',
        'lbl-rec-morning-dose': '🌅 ఉదయం పూట',
        'lbl-rec-evening-dose': '🌆 సాయంత్రం పూట',
        'lbl-rec-balanced-title': 'సమతుల్య రోజువారీ మేత ప్రణాళిక (ICAR Balanced Daily Diet)',
        'lbl-rec-adaptation-title': 'క్రమంగా అలవాటు చేసే 4 రోజుల విధానం (4-Day Rumen Adaptation)',
        'explainable-ai-title': '🔍 కారణాల విశ్లేషణ: "ఈ ఫలితం ఎందుకు వచ్చింది?"',
        'cv-metrics-title': '👁️ కంప్యూటర్ విజన్ కొలతలు',
        'passport-box-title': '📦 డిజిటల్ ఫీడ్ పాస్‌పోర్ట్ తయారైంది!',
        'btn-view-passport': '📜 ధృవీకరించిన పాస్‌పోర్ట్ & QR చూడండి',

        // Tab 3: Adulteration Check
        'adulteration-header-title': '⚠️ మేత కల్తీ & యూరియా స్పైకింగ్ రిస్క్',
        'adulteration-header-subtitle': 'నాన్-ప్రోటీన్ నైట్రోజన్ (NPN) వ్యత్యాసం & తెల్ల పొడి కణాల గుర్తింపు',
        'adulteration-alert-notice': '<strong>శాస్త్రీయ నోటీసు:</strong> చౌకబారు <strong>ఎరువుల యూరియా</strong> (46% నైట్రోజన్) లేదా సుద్ద పొడిని కలిపి ప్రోటీన్ శాతాన్ని కృత్రిమంగా పెంచే కల్తీని ఈ మాడ్యూల్ గుర్తిస్తుంది. చట్టపరమైన నిర్ధారణకు HPLC లేదా ప్రయోగశాల పరీక్ష అవసరం.',
        'adulteration-params-title': '🧪 కల్తీ అనుకరణ పారామితులు',
        'label-ad-cp': 'క్రూడ్ ప్రోటీన్ (CP %)',
        'label-ad-moisture': 'తేమ శాతం (Moisture %)',
        'label-ad-npn': 'నాన్-ప్రోటీన్ నైట్రోజన్ (NPN %)',
        'label-ad-powder': 'కనిపించే తెల్లటి పొడి / స్పటిక గుళికలు',
        'adulteration-output-title': '📊 కల్తీ అంచనా ఫలితం',
        'urea-calc-title': '🌾 శాస్త్రీయ సురక్షిత యూరియా మోతాదు & ఎండుగడ్డి శుద్ధి కాలిక్యులేటర్',
        'urea-calc-subtitle': 'ICAR & NDDB ప్రామాణిక నాన్-టాక్సిక్ యూరియా గడ్డి శుద్ధి మరియు దాణా మిక్సింగ్ మార్గదర్శి',
        'urea-calc-standard-badge': '✅ ICAR 4% ప్రామాణికం',
        'btn-urea-mode-straw': '🌾 యూరియా గడ్డి శుద్ధి (యూరియా గడ్డి శుద్ధి)',
        'btn-urea-mode-concentrate': '🥣 రోజువారీ దాణాలో మిక్సింగ్ (దాణాలో మిక్సింగ్)',
        'label-kpi-urea': 'శాస్త్రీయ సురక్షిత యూరియా',
        'label-kpi-water': 'అవసరమైన నీరు',
        'label-kpi-curing': 'నిల్వ / పరిపక్వత కాలం',
        'label-kpi-protein': 'పోషక లాభం (ప్రోటీన్)',
        'label-advisory-summary': '📋 సిఫార్సు చేసిన మోతాదు సారాంశం',
        'btn-speak-urea-text': 'వాయిస్ వినండి (Audio)',
        'urea-steps-title': '📝 దశల వారీ ప్రామాణిక తయారీ విధానం (SOP)',
        'urea-precautions-title': '⚠️ ముఖ్యమైన నిబంధనలు & భద్రతా జాగ్రత్తలు',
        'urea-antidote-title': '🚑 అత్యవసర ప్రాణరక్షక విరుగుడు (FIRST AID ANTIDOTE)',

        // Tab 4: AI Advisory
        'advisory-header-title': '🤖 రైతు బహుభాషా సలహాలు & వాయిస్',
        'advisory-header-subtitle': 'స్పష్టమైన తెలుగు, హిందీ, ఇంగ్లీష్ ఆడియో మరియు సులభ సమస్యల పరిష్కారం',
        'audio-speaker-heading': '🔊 స్మార్ట్ ఫీడ్ ఆడియో సహాయకుడు',
        'audio-title': 'రైతు సలహాలను వాయిస్ ద్వారా వినండి',
        'audio-subtitle': 'స్పష్టమైన తెలుగు ఆడియో సిద్ధంగా ఉంది',
        'btn-speak': '▶ వాయిస్ వినండి (Play)',
        'advisory-lang-label': 'రైతు భాష / Language:',
        'btn-mode-preset': '⚡ 1-క్లిక్ సాధారణ సమస్యలు',
        'btn-mode-manual': '✍️ మీ సమస్యను నేరుగా రాయండి',
        'problem-statements-title': '👨‍🌾 సాధారణ పాడి సమస్యలు (రైతులు టైప్ చేయనవసరం లేదు)',
        'problem-statements-subtitle': 'మీ పశువుల పరిస్థితికి సరిపోయే సమస్యను ఎంచుకుంటే తక్షణ పరిష్కారం వస్తుంది:',
        'instant-solution-badge': '⚡ తక్షణ పరిష్కారం',
        'manual-entry-title': '✍️ మీ స్వంత సమస్యను తెలపండి',
        'manual-entry-subtitle': 'మీ సమస్యను తెలుగు, హిందీ లేదా ఇంగ్లీషులో రాయండి లేదా క్రింది ట్యాగ్‌లను నొక్కండి:',
        'symptom-chips-label': '⚡ సాధారణ లక్షణాలు (నొక్కి జోడించండి):',
        'label-manual-problem': 'సమస్య వివరాలు రాయండి:',
        'placeholder-manual-problem': 'ఉదాహరణ: ఆవు పాలు తగ్గిపోయాయి, మేతలో పుల్లని వాసన లేదా బూజు ఉంది...',
        'label-feed-type': 'మేత రకం',
        'label-feed-smell': 'మేత వాసన',
        'label-feed-moisture': 'తేమ స్థితి',
        'label-feed-appearance': 'భౌతిక స్థితి',
        'label-cattle-symptom': 'పశువుల లక్షణాలు',
        'btn-submit-manual-advisory': '🚀 AI విశ్లేషణ చేయండి',
        'btn-clear-manual-advisory': '🔄 క్లియర్ చేయండి',
        'advisory-plan-title': '📜 రైతు సమగ్ర కార్యాచరణ ప్రణాళిక',

        // Tab 5: Dashboard
        'dashboard-header-title': '📊 ఫీడ్ క్వాలిటీ & డాష్‌బోర్డ్',
        'dashboard-header-subtitle': 'రియల్ టైమ్ గణాంకాలు, ట్రెండ్ విశ్లేషణ మరియు ముందస్తు హెచ్చరికలు',
        'dashboard-kpi1-label': 'మొత్తం పరీక్షించిన బ్యాచ్‌లు',
        'dashboard-kpi2-label': 'సగటు ఆరోగ్య స్కోర్',
        'dashboard-kpi3-label': 'సురక్షిత బ్యాచ్‌ల శాతం',
        'dashboard-kpi4-label': 'ప్రమాదకర మేత శాతం',
        'dashboard-chart-trend-title': '📈 నాణ్యత స్కోర్ ట్రెండ్ (గత 15 బ్యాచ్‌లు)',
        'dashboard-chart-pie-title': '🍩 రిస్క్ స్థాయిల విభజన',
        'dashboard-table-title': '📋 ఇటీవలి బ్యాచ్ ఆడిట్ రికార్డులు',
        'th-batch': 'బ్యాచ్ ID',
        'th-type': 'మేత రకం',
        'th-score': 'స్కోర్',
        'th-badge': 'హోదా',
        'th-concern': 'ముఖ్యమైన సమస్య',
        'th-time': 'సమయం',
        'table-loading-msg': 'రికార్డులు లోడ్ అవుతున్నాయి...',

        // Tab 6: Feed Passport
        'passport-header-title': '📦 ధృవీకరించిన డిజిటల్ ఫీడ్ పాస్‌పోర్ట్',
        'passport-header-subtitle': 'అధికారిక ధృవీకరణ ముద్ర మరియు QR కోడ్‌తో కూడిన బ్యాచ్ సర్టిఫికేట్',
        'cert-protocol-label': 'స్మార్ట్ ఫీడ్ డిజిటల్ ట్రేసిబిలిటీ ప్రోటోకాల్',
        'cert-title-label': '📦 డిజిటల్ ఫీడ్ పాస్‌పోర్ట్',
        'cert-lbl-type': 'మేత రకం',
        'cert-lbl-score': 'ఆరోగ్య స్కోర్',
        'cert-lbl-safety': 'భద్రతా స్థితి',
        'cert-lbl-time': 'నమోదైన సమయం',
        'cert-lbl-nutrients': 'ధృవీకరించబడిన పోషక విలువలు',
        'cert-scan-prompt': 'బ్యాచ్ ప్రామాణికతను ధృవీకరించడానికి స్కాన్ చేయండి',
        'btn-print-cert': '🖨️ ప్రింట్ చేయండి',
        'btn-download-qr': '⬇️ QR కోడ్ డౌన్‌లోడ్',

        // Tab 7: Batch Lookup
        'lookup-header-title': '🔎 బ్యాచ్ ట్రేసిబిలిటీ & QR ధృవీకరణ',
        'lookup-header-subtitle': 'పాత రికార్డులను వెతకండి లేదా QR కోడ్‌ను అప్‌లోడ్ చేసి ధృవీకరించండి',
        'lookup-search-title': '🔍 బ్యాచ్ ID ద్వారా శోధించండి',
        'placeholder-lookup-batch': 'ఉదా: SFA-2026-000001',
        'btn-lookup-search': 'శోధించండి',
        'lookup-qr-title': '📷 QR కోడ్ ఫోటో ద్వారా ధృవీకరించండి',
        'lookup-dropzone-title': 'QR ఫోటోను అప్‌లోడ్ చేయండి',
        'lookup-details-title': '📋 బ్యాచ్ రికార్డు వివరాలు',
        'lookup-result-placeholder': 'సర్టిఫికేట్ చూడటానికి బ్యాచ్ ID నమోదు చేయండి లేదా QR అప్‌లోడ్ చేయండి.',
        'animal-rec-header-title': 'పశువుల వారీగా మేత సిఫార్సు & రోజువారీ మోతాదు',
        'animal-rec-header-sub': 'పశువుల వారీగా మేత సిఫార్సు • ICAR పాడి పశువుల పోషకాహార ప్రమాణాలు',
        'btn-speak-animal-rec-txt': 'వాయిస్ సలహా వినండి',
        'lbl-quick-animal-select': '⚡ నా పశువుల నుండి ఎంచుకోండి (1-క్లిక్ ఎంపిక):',
        'lbl-rec-species': '🐄 పశువు రకం',
        'lbl-rec-stage': '🤰 శారీరక స్థితి',
        'lbl-rec-milk': '🥛 పాల ఉత్పత్తి',
        'btn-recalculate-rec-txt': 'సిఫార్సు లెక్కించండి',
        'rec-verdict-title': 'ఈ మేత మీ పశువుకు చాలా అనుకూలమైనది మరియు సురక్షితం!',
        'rec-verdict-note': 'నాణ్యత స్కోర్, ప్రోటీన్ మరియు తేమ సమతుల్యంగా ఉన్నాయి.',
        'lbl-rec-daily-dose': 'మొత్తం రోజువారీ మోతాదు',
        'lbl-rec-daily-sub': 'రోజూ ఇవ్వవలసిన దాణా',
        'lbl-rec-morning-dose': '🌅 ఉదయం పూట',
        'lbl-rec-morning-sub': '50% మోతాదు',
        'lbl-rec-evening-dose': '🌆 సాయంత్రం పూట',
        'lbl-rec-evening-sub': '50% మోతాదు',
        'lbl-rec-balanced-title': 'సమతుల్య రోజువారీ మేత ప్రణాళిక (ICAR ప్రమాణం)',
        'lbl-rec-diet-green': '🌿 పచ్చిగడ్డి',
        'lbl-rec-diet-straw': '🌾 ఎండుగడ్డి',
        'lbl-rec-diet-minerals': '🧂 ఖనిజ లవణాలు',
        'lbl-rec-diet-water': '💧 తాగునీరు',
        'lbl-rec-adaptation-title': 'క్రమంగా అలవాటు చేసే 4 రోజుల విధానం',
        'lbl-rec-rumen-badge': 'రూమెన్ రక్షణ',
        'lbl-rec-vet-prefix': 'ℹ️ పశువైద్య సలహా:',
        'btn-urea-mode-straw': '🌾 యూరియా గడ్డి శుద్ధి',
        'btn-urea-mode-concentrate': '🥣 దాణాలో మిక్సింగ్',
        'label-urea-qty': 'ఎండుగడ్డి పరిమాణం (kg)',
        'label-urea-animals': 'పశువుల సంఖ్య',
        'urea-steps-title': '📝 దశల వారీ విధానం',
        'urea-precautions-title': '⚠️ ముఖ్యమైన భద్రతా జాగ్రత్తలు',
        'urea-antidote-title': 'అత్యవసర ప్రాణరక్షక విరుగుడు',
        'advisory-lang-label': 'రైతు భాష:',
        'btn-mode-preset': '⚡ 1-క్లిక్ సాధారణ సమస్యలు',
        'btn-mode-manual': '✍️ నేరుగా సమస్య రాయండి',
        'label-manual-problem': 'సమస్య వివరాలు రాయండి:',
        'placeholder-manual-problem-input': 'ఉదాహరణ: ఆవు పాలు తగ్గిపోయాయి, మేతలో పుల్లని వాసన లేదా బూజు ఉంది...',
        'label-feed-type': 'మేత రకం',
        'label-feed-smell': 'మేత వాసన',
        'label-feed-moisture': 'తేమ శాతం',
        'label-feed-appearance': 'భౌతిక స్థితి',
        'label-cattle-symptom': 'పశువుల లక్షణాలు',
        'btn-submit-manual-advisory-txt': '🚀 AI విశ్లేషణ చేయండి',
        'btn-clear-manual-advisory-txt': '🔄 క్లియర్ చేయండి',
        'tab-btn-login': '🔑 లాగిన్',
        'tab-btn-register': '📝 నమోదు',
        'auth-demo-logins-title': '🛡️ రోల్ ఎంపిక & త్వరిత వివరాలు (పాస్‌వర్డ్ అవసరం)',
        'lbl-login-mobile': '📱 మొబైల్ నంబర్',
        'lbl-login-password': '🔒 పాస్‌వర్డ్',
        'btn-submit-login': 'లాగిన్ అవ్వండి',
        'lbl-login-new-prompt': 'కొత్త రైతులా?',
        'lnk-create-account': 'ఖాతా సృష్టించండి & ఫారమ్ సెటప్ →',
        'lbl-reg-fullname': '👤 రైతు పూర్తి పేరు',
        'lbl-reg-mobile': '📱 మొబైల్ నంబర్',
        'lbl-reg-email': '📧 ఈమెయిల్ (ఐచ్ఛికం)',
        'lbl-reg-password': '🔒 పాస్‌వర్డ్',
        'lbl-reg-confirm-password': '🔒 పాస్‌వర్డ్ పునఃప్రవేశం',
        'lbl-reg-lang': '🌐 అనుకూలమైన భాష',
        'btn-submit-register': 'నమోదు చేయండి',
        'lbl-reg-existing-prompt': 'ఇప్పటికే ఖాతా ఉందా?',
        'lnk-signin-here': 'ఇక్కడ లాగిన్ అవ్వండి →',
        'wizard-title-main': 'మీ ఫారమ్ వివరాలు సెటప్ చేయండి',
        'wz-nav-step1': 'ప్రాథమిక వివరాలు',
        'wz-nav-step2': 'పశువుల సంఖ్య',
        'wz-nav-step3': 'ప్రతి పశువు వివరాలు',
        'wz-nav-step4': 'మేత & నిల్వ',
        'wz-step1-title': '🌾 దశ 1 — ప్రాథమిక వివరాలు',
        'wz-step1-subtitle': 'మీ ఫారమ్ ప్రాంతం మరియు భాషను ఎంచుకుంటే తగిన మేత సలహాలు ఇవ్వబడతాయి.',
        'lbl-wz-name': '👨‍🌾 రైతు పేరు',
        'lbl-wz-village': '📍 గ్రామం లేదా ప్రాంతం',
        'lbl-wz-lang': '🌐 అనుకూలమైన భాష',
        'btn-wz-next-1': 'తర్వాత →',
        'wz-step2-title': '🐄 దశ 2 — ఎన్ని పశువులు ఉన్నాయి?',
        'wz-step2-subtitle': 'మీ వద్ద ఉన్న పశువుల రకాలు మరియు మొత్తం సంఖ్యను ఎంచుకోండి.',
        'lbl-wz-total-animals': 'మొత్తం పశువులు',
        'wz-step2-types-title': 'పశువుల రకాలు ఎంచుకోండి:',
        'lbl-wz-cow-name': 'ఆవు',
        'wz-type-cow-sub': 'ఆవులు',
        'lbl-wz-buff-name': 'గేదె',
        'wz-type-buff-sub': 'గేదెలు',
        'btn-wz-back-2': '← వెనుకకు',
        'btn-wz-next-2': 'తర్వాత →',
        'wz-step3-title': '🐄 దశ 3 — ప్రతి పశువు వివరాలు',
        'wz-step3-subtitle': 'ప్రతి పశువు వివరాలను అందించండి. గమనిక: చూడి లేదా ఎండిన పశువులకు పాల ఉత్పత్తి అవసరం లేదు.',
        'btn-wz-back-3': '← వెనుకకు',
        'btn-wz-next-3': 'తర్వాత →',
        'wz-step4-title': '🌾 దశ 4 — మేత & నిల్వ వివరాలు',
        'wz-step4-subtitle': 'మీ ప్రధాన మేత రకం మరియు నిల్వ స్థలాన్ని ఎంచుకోండి.',
        'lbl-wz-main-feed': '🌾 ప్రధాన మేత రకం',
        'lbl-opt-green': 'పచ్చి మేత',
        'lbl-opt-green-desc': 'నేపియర్, సూపర్ నేపియర్, మొక్కజొన్న',
        'lbl-opt-dry': 'ఎండు మేత',
        'lbl-opt-dry-desc': 'వరి గడ్డి, గోధుమ గడ్డి, జొన్న చొప్ప',
        'lbl-opt-silage': 'సైలేజ్ (పాతర గడ్డి)',
        'lbl-opt-silage-desc': 'గుంత లేదా బేల్స్‌లో పులియబెట్టిన మొక్కజొన్న సైలేజ్',
        'lbl-opt-conc': 'దాణా / గుళికలు',
        'lbl-opt-conc-desc': 'దాణా పెల్లెట్లు, పిండి దాణా, చెక్కలు',
        'lbl-opt-mixed': 'మిశ్రమ దాణా',
        'lbl-opt-mixed-desc': 'పచ్చిగడ్డి + ఎండుగడ్డి + దాణా సమతుల్య మిశ్రమం',
        'lbl-wz-storage': '🏚️ మేత నిల్వ స్థలం',
        'lbl-opt-shed': 'పాక / షెడ్డు',
        'lbl-opt-shed-desc': 'వర్షం తగలకుండా కప్పబడిన షెడ్డు',
        'lbl-opt-pit': 'సైలేజ్ గుంత',
        'lbl-opt-pit-desc': 'గాలి చొరబడని బంకర్ గుంత లేదా ట్రెంచ్',
        'lbl-opt-room': 'నిల్వ గది',
        'lbl-opt-room-desc': 'గాలి వెలుతురు వచ్చే పక్కా గది',
        'lbl-opt-open': 'బహిరంగ ప్రదేశం',
        'lbl-opt-open-desc': 'టార్పాలిన్ కప్పిన బహిరంగ నిల్వ',
        'btn-wz-back-4': '← వెనుకకు',
        'btn-wz-finish': '🎉 సెటప్ ముగించి డాష్‌బోర్డ్‌కు వెళ్లండి →',
        'my-animals-modal-title': 'నా పశువుల జాబితా',
        'btn-animals-edit-setup': '⚙️ పశువుల సంఖ్య & సెటప్ మార్చండి',
        'btn-animals-done': 'ముగించు',
        'diary-modal-title': 'స్మార్ట్ మేత డైరీ & సమయ ప్రణాళిక',
        'diary-modal-subtitle': 'ఉదయం, మధ్యాహ్నం, సాయంత్రం మేత సమయాలు, రిమైండర్లు & పాల దిగుబడి విశ్లేషణ',
        'diary-animal-select-lbl': '🐄 పశువు ఎంపిక:',
        'btn-diary-voice': 'వాయిస్ ప్రణాళిక వినండి',
        'diary-next-slot-badge': 'తదుపరి మేత సమయం',
        'diary-next-slot-desc': 'మేత ప్రణాళిక సిద్ధం చేయండి.',
        'btn-diary-log-now': '⏱️ ఇప్పుడే నమోదు చేయండి',
        'diary-summary-title': 'నేటి మేత & పాల దిగుబడి సారాంశం',
        'diary-conc-lbl': '🥣 దాణా',
        'diary-green-lbl': '🌿 పచ్చిగడ్డి',
        'diary-straw-lbl': '🌾 ఎండుగడ్డి',
        'diary-milk-lbl': '🥛 నమోదైన పాలు',
        'diary-target-conc': 'లక్ష్యం: 0.0 kg',
        'diary-target-green': 'లక్ష్యం: 0.0 kg',
        'diary-target-straw': 'లక్ష్యం: 0.0 kg',
        'diary-target-milk': 'సగటు: 8.0 L',
        'diary-insights-headline': 'AI మేత విశ్లేషణ & పాల దిగుబడి ఇన్‌సైట్స్',
        'diary-insights-body': 'మీరు రోజూ ఉదయం, మధ్యాహ్నం, సాయంత్రం ఇచ్చిన మేతను నమోదు చేస్తే, ఏ మేత వల్ల పాల దిగుబడి పెరిగిందో సిస్టమ్ ఇక్కడ స్పష్టమైన విశ్లేషణ ఇస్తుంది.',
        'diary-modal-footer-note': '💡 ICAR నేషనల్ డైరీ రీసెర్చ్ ఇన్‌స్టిట్యూట్ (NDRI) ప్రామాణిక ప్రణాళిక',
        'btn-diary-close': 'మూసివేయి',
        'modal-history-title': 'నా మేత పరీక్షల రికార్డులు',
        'modal-history-loading': 'మీ పరీక్ష రికార్డులు లోడ్ అవుతున్నాయి...',
        'btn-modal-history-new': '📸 కొత్త నాణ్యత పరీక్ష చేయండి →',
        'btn-modal-history-close': 'మూసివేయి',
        'guest-card-title': 'రైతు లాగిన్ & ఫారమ్ ప్రొఫైల్ సెటప్',
        'btn-guest-login': 'లాగిన్',
        'home-tele-voice-val': 'తెలుగు • हिंदी • English',
        'farmer-history-section-title': '<span>📜</span> <span>నా మేత పరీక్షల రికార్డులు</span>',
        'btn-start-app-title': '🚀 యాప్‌ను ప్రారంభించండి',
        'btn-start-sublabel': 'డయాగ్నస్టిక్ సిస్టమ్‌ను ప్రారంభించండి',
        'link-splash-login': '🔑 రైతు & అడ్మిన్ లాగిన్ / సైన్ ఇన్ →',
        'link-splash-lang': '🌐 భాషా ఎంపికలు →',
        'entry-lang-heading': 'మీ భాషను ఎంచుకోండి',
        'entry-lang-subheading': 'పరీక్షలు, సలహాలు మరియు వాయిస్ ఆడియో కోసం భాషను ఎంచుకోండి',
        'btn-lang-back-txt': '← వెనుకకు',
        'btn-lang-next-txt': 'తర్వాత (లాగిన్) →',
        'entry-auth-heading': 'రైతు / అడ్మిన్ లాగిన్ & రిజిస్ట్రేషన్',
        'entry-auth-subheading': 'రైతు & పాల సహకార సంఘం సురక్షిత పోర్టల్',
        'entry-tab-login-txt': '🔑 లాగిన్',
        'entry-tab-reg-txt': '📝 ఫారమ్ నమోదు',
        'entry-demo-logins-title': '🛡️ రోల్ ఎంపిక & త్వరిత వివరాలు (పాస్‌వర్డ్ అవసరం)',
        'lbl-entry-login-mobile': '📱 మొబైల్ నంబర్',
        'lbl-entry-login-pwd': '🔒 పాస్‌వర్డ్',
        'btn-entry-signin-txt': '🔑 లాగిన్ అవ్వండి →',
        'lbl-entry-new-farmer-prompt': 'కొత్త రైతులా?',
        'link-entry-create-account': 'ఖాతా తెరిచి ఫారమ్ సెటప్ చేయండి →',
        'lbl-entry-reg-name': '👤 పూర్తి పేరు',
        'lbl-entry-reg-mobile': '📱 మొబైల్ నంబర్',
        'lbl-entry-reg-email': '📧 ఇమెయిల్ (ఐచ్ఛికం)',
        'lbl-entry-reg-pwd': '🔒 పాస్‌వర్డ్ (కనీసం 4 అక్షరాలు)',
        'lbl-entry-reg-cpwd': '🔒 పాస్‌వర్డ్ నిర్ధారించండి',
        'lbl-entry-reg-lang': '🌐 ప్రాధాన్య భాష',
        'btn-entry-reg-txt': '📝 ఖాతా సృష్టించండి →',
        'lbl-entry-already-registered': 'ఇప్పటికే ఖాతా ఉందా?',
        'link-entry-signin': 'ఇక్కడ లాగిన్ అవ్వండి →',
        'btn-entry-back-lang-txt': '← భాషా ఎంపికకు వెళ్లండి',
        'placeholder-entry-login-mobile': '10 అంకెల మొబైల్ నంబర్',
        'placeholder-entry-login-password': 'పాస్‌వర్డ్ నమోదు చేయండి',
        'placeholder-login-mobile': '10 అంకెల మొబైల్ నంబర్',
        'placeholder-login-password': 'పాస్‌వర్డ్ నమోదు చేయండి',
        'placeholder-entry-reg-fullname': 'ఉదా: రమేష్ కుమార్',
        'placeholder-entry-reg-mobile': '10 అంకెల మొబైల్ నంబర్',
        'placeholder-entry-reg-email': 'ఐచ్ఛిక ఇమెయిల్ చిరునామా',
        'placeholder-entry-reg-password': 'కనీసం 4 అక్షరాలు',
        'placeholder-entry-reg-confirm-password': 'పాస్‌వర్డ్‌ను మళ్లీ నమోదు చేయండి'
    },
    hi: {
        // Sidebar Navigation
        'sidebar-brand-title': 'SmartFeed AI',
        'sidebar-brand-slogan': 'स्मार्ट चारा • उन्नत डेयरी',
        'sidebar-status-text': 'ऑफलाइन तैयार • स्थानीय AI सक्रिय',
        'nav-home': 'होम',
        'nav-scanner': 'गुणवत्ता स्कैनर',
        'nav-adulteration': 'मिलावट जांच',
        'nav-advisory': 'किसान AI सलाह',
        'nav-dashboard': 'डैशबोर्ड',
        'nav-passport': 'फीड पासपोर्ट',
        'nav-lookup': 'बैच खोज व सत्यापन',
        'btn-reopen-lang-text': '🌐 भाषा बदलें (Language)',
        'mobile-lang-btn-text': 'भाषा / Lang',
        'sidebar-lang-label': 'किसान भाषा',
        'sidebar-engine-label': 'सलाह इंजन',
        'sidebar-footer-text': '<strong>स्मार्ट इंडिया हैकाथॉन 2026</strong><br>कम लागत वाला सॉफ्टवेयर प्रोटोटाइप<br>विशेष हार्डवेयर की आवश्यकता नहीं',

        // Tab 1: Home
        'hero-badge-text': 'स्मार्ट इंडिया हैकाथॉन 2026 • AI कृषि-तकनीक नवाचार',
        'hero-title-text': 'SmartFeed AI',
        'hero-motto-text': 'स्मार्ट चारा • उन्नत डेयरी • साथ में प्रगति',
        'hero-desc-text': 'एआई-संचालित पशु आहार व साइलेज गुणवत्ता परीक्षण, बहु-कारक जोखिम मूल्यांकन, स्पष्ट किसान सलाह और डिजिटल ट्रेसिबिलिटी।',
        'home-btn-scan': 'गुणवत्ता स्कैनर',
        'home-btn-adulteration': 'मिलावट जांच',
        'home-btn-advisory': 'किसान सलाह',
        'home-sci-notice': '<strong>वैज्ञानिक प्रोटोटाइप सूचना:</strong> स्मार्ट फीड एआई कंप्यूटर विजन, रंग/बनावट विश्लेषण और बहु-कारक जोखिम अनुमान प्रदान करता है। यह डेयरी किसानों के लिए निर्णय सहायता प्रणाली है। रासायनिक पुष्टि के लिए प्रयोगशाला परीक्षण अनुशंसित है।',
        'home-tele-edge-label': 'एज एआई इंजन',
        'home-tele-edge-val': '< 300ms स्थानीय प्रतिक्रिया',
        'home-tele-risk-label': 'जोखिम बुद्धिमत्ता',
        'home-tele-risk-val': '6-कारक विश्लेषण',
        'home-tele-voice-label': 'बहुभाषी आवाज',
        'home-tele-voice-val': 'हिंदी • తెలుగు • EN',
        'home-tele-trace-label': 'ट्रेसेबिलिटी',
        'home-tele-trace-val': 'QR डिजिटल पासपोर्ट',
        'home-why-title': '🌟 स्मार्ट फीड एआई क्यों?',
        'home-why-p1': 'छोटे डेयरी किसान और ग्रामीण दुग्ध समितियां <strong>चारे की खराबी, फंगस/उल्ली और यूरिया मिलावट</strong> के कारण दूध उत्पादन में गिरावट और पशुओं के स्वास्थ्य संकट का सामना करते हैं।',
        'home-why-p2': 'पारंपरिक समाधानों के लिए महंगे प्रयोगशाला परीक्षण की आवश्यकता होती है जो ग्रामीण किसानों की पहुंच से बाहर है।',
        'home-pitch-box': '<strong>💡 SIH प्रोजेक्ट विजन:</strong><p style="color: var(--slate-700); font-size: 0.92rem; margin-top: 6px;"><em>"स्मार्ट फीड एआई एक साधारण स्मार्टफोन कैमरे को चारे की जांच करने वाली प्रयोगशाला में बदल देता है, जिसमें कंप्यूटर विजन, यूरिया मिलावट पहचान, बहुभाषी आवाज और डिजिटल पासपोर्ट शामिल हैं।"</em></p>',
        'home-usps-title': '🏆 प्रमुख नवाचार (USPs)',
        'home-usps-list': `
            <li>⭐ <strong>स्मार्ट फीड हेल्थ स्कोर (0–100)</strong>: दृश्य, फफूंद, पोषक तत्व और भंडारण पर आधारित एकल पारदर्शी स्कोर।</li>
            <li>🔍 <strong>कारणों का विश्लेषण ("यह परिणाम क्यों आया?")</strong>: चारा क्यों जोखिम भरा है, इसका बिंदुवार विवरण।</li>
            <li>🗣️ <strong>बहुभाषी आवाज सलाह</strong>: <strong>हिंदी, तेलुगु, अंग्रेजी</strong> में त्वरित ऑडियो मार्गदर्शन।</li>
            <li>📦 <strong>क्यूआर डिजिटल पासपोर्ट</strong>: दुग्ध सहकारी समितियों के लिए डिजिटल बैच प्रमाणपत्र।</li>
            <li>📈 <strong>पूर्व चेतावनी प्रणाली</strong>: सड़न दिखने से पहले चारे की गिरती गुणवत्ता की पहचान।</li>
            <li>📶 <strong>100% ऑफलाइन कार्यक्षमता</strong>: बिना इंटरनेट के पूरी तरह संचालित।</li>
        `,
        'home-btn-scan': 'गुणवत्ता स्कैनर',
        'home-btn-adulteration': 'मिलावट जांच',
        'home-btn-advisory': 'किसान सलाह',
        'home-btn-dashboard': 'डैशबोर्ड',
        'home-quick-title': '🚀 मुख्य सुविधाएं त्वरित शुरुआत',
        'home-card1-title': '1. फीड स्कैनर',
        'home-card1-desc': 'फोटो अपलोड करें और रंग बदलाव, फफूंद तथा कणों की जांच करें।',
        'btn-home-card1': '🚀 स्कैनर खोलें',
        'home-card2-title': '2. मिलावट जोखिम',
        'home-card2-desc': 'स्लाइडर से यूरिया मिलावट व गैर-प्रोटीन नाइट्रोजन जोखिम परखें।',
        'btn-home-card2': '🔬 मिलावट जांचें',
        'home-card3-title': '3. किसान सलाह',
        'home-card3-desc': 'हिंदी, तेलुगु या अंग्रेजी में विशेषज्ञ की आवाज में सलाह सुनें।',
        'btn-home-card3': '🗣️ आवाज सलाह',
        'home-card4-title': '4. एनालिटिक्स डैशबोर्ड',
        'home-card4-desc': 'लाइव गुणवत्ता स्कोर ट्रेंड, जोखिम स्तर वितरण और पूर्व चेतावनी।',
        'btn-home-card4': '📈 डैशबोर्ड देखें',
        'home-card5-title': '5. क्यूआर पासपोर्ट',
        'home-card5-desc': 'सहकारी समितियों के लिए डिजिटल पासपोर्ट देखें व डाउनलोड करें।',
        'btn-home-card5': '📜 पासपोर्ट देखें',
        'btn-refresh-dashboard': '🔄 रीफ्रेश करें',

        // Step 5: Farmer Personalized Dashboard & Tools
        'guest-card-title': 'किसान लॉगिन व फार्म प्रोफाइल सेटअप',
        'guest-card-sub': 'अपने पशुओं की संख्या दर्ज करने, गाय व भैंसों की स्वास्थ्य निगरानी हेतु लॉगिन करें!',
        'btn-guest-login': '🔑 लॉगिन (Sign In)',
        'btn-guest-register': '📝 पंजीकरण (Register)',
        'title-farmer-features': '🌟 डेयरी किसान निदान व परामर्श केंद्र (8 मुख्य उपकरण)',
        'btn-edit-farm': '⚙️ फार्म विवरण बदलें',
        'btn-dash-new-scan': '📸 आज का चारा जांचें',
        'fd-lbl-cows': 'गायें (Cows)',
        'fd-lbl-buffs': 'भैंसें (Buffs)',
        'fd-lbl-lact': 'दूध देने वाली (Lactating)',
        'fd-lbl-preg': 'गाभिन (Pregnant)',
        'fd-lbl-feed': 'मुख्य चारा',
        'fd-lbl-storage': 'भंडारण स्थान',
        'fd-lbl-tests': 'जांच (Tests)',
        'tile1-title': '1. फीड स्कैनर',
        'tile1-sub': 'गुणवत्ता व फफूंद जांच',
        'tile1-desc': 'फोटो खींचकर रंग बदलाव, फफूंद और 0-100 स्वास्थ्य स्कोर तुरंत जानें।',
        'tile1-btn': '🚀 स्कैनर खोलें →',
        'tile2-title': '2. यूरिया जांच व खुराक',
        'tile2-sub': 'सुरक्षित यूरिया गणना',
        'tile2-desc': 'यूरिया मिलावट पहचानें और ICAR 4% पुआल उपचार की सुरक्षित खुराक निकालें।',
        'tile2-btn': '🔬 सुरक्षित यूरिया निकालें →',
        'tile3-title': '3. किसान AI सलाह',
        'tile3-sub': 'हिंदी आवाज सलाह',
        'tile3-desc': 'अपने पशुओं के अनुसार हिंदी, तेलुगु या अंग्रेजी में आवाज सलाह सुनें।',
        'tile3-btn': '🗣️ आवाज सलाह सुनें →',
        'tile4-title': '4. मेरे पशु',
        'tile4-sub': 'पशुवार प्रोफाइल व रिकॉर्ड',
        'tile4-desc': 'अपनी गायों, भैंसों की उम्र, दुग्ध अवस्था और पोषण लक्ष्यों की जांच करें।',
        'tile4-btn': '🐄 पशु सूची देखें →',
        'tile5-title': '5. चारा डायरी',
        'tile5-sub': 'दैनिक आहार लॉग',
        'tile5-desc': 'दैनिक चारा मात्रा, ताजगी और दाना खपत का विवरण दर्ज करें।',
        'tile5-btn': '📝 चारा डायरी देखें →',
        'tile6-title': '6. मेरा डैशबोर्ड',
        'tile6-sub': 'फार्म एनालिटिक्स',
        'tile6-desc': 'चारा गुणवत्ता ट्रेंड, जोखिम वितरण और प्रारंभिक सड़न चेतावनी देखें।',
        'tile6-btn': '📈 डैशबोर्ड खोलें →',
        'tile7-title': '7. जांच इतिहास',
        'tile7-sub': 'पिछले बैच रिकॉर्ड',
        'tile7-desc': 'अपनी पिछली चारा जांचों, स्कोर और डिजिटल प्रमाणपत्रों की समीक्षा करें।',
        'tile7-btn': '📋 इतिहास देखें →',
        'tile8-title': '8. क्यूआर पासपोर्ट',
        'tile8-sub': 'डिजिटल फीड पासपोर्ट',
        'tile8-desc': 'दुग्ध समितियों के लिए आधिकारिक क्यूआर कोड युक्त बैच पासपोर्ट पाएं।',
        'tile8-btn': '📦 पासपोर्ट देखें →',

        // Farmer History Section
        'farmer-history-section-title': '<span>📜</span> <span>मेरे पिछले चारा परीक्षण रिकॉर्ड (My Feed Diagnostic History)</span>',
        'farmer-history-section-sub': 'आपके फार्म पर पहले जांची गई चारा बैच, गुणवत्ता स्कोर, सुरक्षा अलर्ट और डिजिटल पासपोर्ट',
        'btn-refresh-farmer-history': 'रिफ्रेश (Refresh)',
        'btn-new-scan-farmer-history': 'नई जांच (New Scan)',
        'fth-batch': 'बैच आईडी (Batch ID)',
        'fth-sample': 'चारा प्रकार (Sample)',
        'fth-score': 'गुणवत्ता स्कोर (Score)',
        'fth-badge': 'स्थिति (Status)',
        'fth-concern': 'मुख्य निष्कर्ष (Findings)',
        'fth-shelf': 'सुरक्षित अवधि (Shelf Life)',
        'fth-date': 'दिनांक (Date)',
        'fth-action': 'कार्रवाई (Action)',
        'modal-history-title': 'मेरे चारा परीक्षण रिकॉर्ड / Test History',

        // Tab 2: Quality Scanner
        'scanner-header-title': '📸 स्मार्ट फीड गुणवत्ता स्कैनर',
        'scanner-header-subtitle': 'कंप्यूटर विजन, बहु-कारक जोखिम विश्लेषण और डिजिटल पासपोर्ट निर्माण',
        'scanner-step1-title': '1. चारा नमूना चुनें या फोटो लें',
        'scanner-preset-label': '⚡ डेमो नमूनों का त्वरित परीक्षण',
        'scanner-dropzone-title': 'चारे की फोटो यहां डालें या चुनें',
        'scanner-dropzone-sub': 'JPG, PNG, WEBP समर्थित',
        'scanner-sample-type-label': 'नमूना वर्गीकरण',
        'scanner-step2-title': '2. पोषक तत्व और भंडारण स्थिति',
        'label-slider-cp': 'कच्चा प्रोटीन (CP %)',
        'label-slider-moisture': 'नमी की मात्रा (%)',
        'label-slider-npn': 'गैर-प्रोटीन नाइट्रोजन (NPN %)',
        'label-slider-days': 'भंडारण के दिन (Days)',
        'label-check-smell': 'खट्टी या असामान्य दुर्गंध महसूस हुई',
        'btn-scan': '🚀 पूर्ण गुणवत्ता जांच करें',
        'scanner-step3-title': '3. स्मार्ट फीड विश्लेषण परिणाम',
        'results-placeholder-title': 'नमूने की प्रतीक्षा है',
        'results-placeholder-desc': 'डेमो नमूना चुनें या फोटो अपलोड करके "जांच करें" बटन दबाएं।',
        'gauge-heading': '🐄 स्मार्ट फीड स्वास्थ्य स्कोर',
        'gauge-score-sub': '100 में से',
        'shelf-life-card-title': '⏳ AI चारा शेल्फ-लाइफ व खराब होने का पूर्वानुमान',
        'shelf-days-label': 'दिनों तक सुरक्षित',
        'shelf-sub-expiry-label': 'सुरक्षित तिथि:',
        'shelf-sub-moist-label': 'नमी का प्रभाव:',
        'shelf-timeline-now': 'आज / ताजा',
        'shelf-timeline-status': 'सामान्य भंडारण',
        'shelf-timeline-spoil': 'खराब होने की अवधि',
        'cert-lbl-shelf': 'शेल्फ लाइफ व समाप्ति तिथि',
        'animal-rec-header-title': 'पशु-विशिष्ट चारा अनुशंसा व दैनिक खुराक',
        'animal-rec-header-sub': 'Animal-Specific Feed Recommendation • ICAR Dairy Cattle Nutrition Benchmarks',
        'btn-speak-animal-rec-txt': 'आवाज में सलाह सुनें (Audio)',
        'lbl-quick-animal-select': '⚡ अपने पंजीकृत पशुओं में से चुनें (1-Click Quick-Pick):',
        'lbl-rec-species': '🐄 पशु का प्रकार / Animal Type',
        'lbl-rec-stage': '🤰 शारीरिक स्थिति / Stage',
        'lbl-rec-milk': '🥛 दूध उत्पादन / Yield',
        'btn-recalculate-rec-txt': 'अनुशंसा की गणना करें',
        'lbl-rec-daily-dose': 'कुल दैनिक खुराक',
        'lbl-rec-daily-sub': 'दैनिक चारा मात्रा',
        'lbl-rec-morning-dose': '🌅 सुबह की खुराक',
        'lbl-rec-evening-dose': '🌆 शाम की खुराक',
        'lbl-rec-balanced-title': 'संतुलित दैनिक आहार योजना (ICAR Balanced Daily Diet)',
        'lbl-rec-adaptation-title': 'क्रमिक 4-दिवसीय आदत प्रक्रिया (4-Day Rumen Adaptation)',
        'explainable-ai-title': '🔍 कारणों का विश्लेषण: "यह परिणाम क्यों आया?"',
        'cv-metrics-title': '👁️ कंप्यूटर विजन माप',
        'passport-box-title': '📦 डिजिटल फीड पासपोर्ट तैयार हुआ!',
        'btn-view-passport': '📜 प्रमाणित पासपोर्ट व QR कोड देखें',

        // Tab 3: Adulteration Check
        'adulteration-header-title': '⚠️ चारा मिलावट व यूरिया स्पाइकिंग जोखिम',
        'adulteration-header-subtitle': 'गैर-प्रोटीन नाइट्रोजन (NPN) अंतर व सफेद चूना/पाउडर कण पहचान',
        'adulteration-alert-notice': '<strong>वैज्ञानिक नोटिस:</strong> सस्ते <strong>उर्वरक यूरिया</strong> (46% नाइट्रोजन) या चॉक पाउडर द्वारा प्रोटीन की झूठी मात्रा बढ़ाने वाली मिलावट को यह मॉड्यूल पहचानता है। कानूनी पुष्टि के लिए लैब परीक्षण जरूरी है।',
        'adulteration-params-title': '🧪 मिलावट सिम्युलेटर पैरामीटर',
        'label-ad-cp': 'कच्चा प्रोटीन (CP %)',
        'label-ad-moisture': 'नमी की मात्रा (%)',
        'label-ad-npn': 'गैर-प्रोटीन नाइट्रोजन (NPN %)',
        'label-ad-powder': 'दिखने वाले सफेद पाउडर / कण',
        'adulteration-output-title': '📊 मिलावट भविष्यवाणी परिणाम',
        'urea-calc-title': '🌾 वैज्ञानिक सुरक्षित यूरिया खुराक व पुआल उपचार कैलकुलेटर',
        'urea-calc-subtitle': 'ICAR और NDDB प्रमाणित गैर-विषाक्त यूरिया उपचार व दैनिक दाना मिश्रण गाइड',
        'urea-calc-standard-badge': '✅ ICAR 4% मानक',
        'btn-urea-mode-straw': '🌾 यूरिया पुआल उपचार (Straw Treatment)',
        'btn-urea-mode-concentrate': '🥣 दैनिक दाना मिश्रण (Concentrate Mix)',
        'label-kpi-urea': 'वैज्ञानिक रूप से सुरक्षित यूरिया',
        'label-kpi-water': 'आवश्यक पानी',
        'label-kpi-curing': 'ढकने / परिपक्वता अवधि',
        'label-kpi-protein': 'पोषण लाभ (प्रोटीन)',
        'label-advisory-summary': '📋 अनुशंसित खुराक सारांश',
        'btn-speak-urea-text': 'आवाज सुनें (Audio)',
        'urea-steps-title': '📝 चरण-दर-चरण मानक संचालन प्रक्रिया (SOP)',
        'urea-precautions-title': '⚠️ अनिवार्य नियम व सुरक्षा सावधानियां',
        'urea-antidote-title': '🚑 आपातकालीन विष-निवारक तोड़ (FIRST AID ANTIDOTE)',

        // Tab 4: AI Advisory
        'advisory-header-title': '🤖 किसान बहुभाषी सलाह व आवाज',
        'advisory-header-subtitle': 'स्पष्ट हिंदी, तेलुगु, अंग्रेजी आवाज और आसान समाधान',
        'audio-speaker-heading': '🔊 स्मार्ट फीड ऑडियो सहायक',
        'audio-title': 'किसान सलाह को अपनी भाषा में सुनें',
        'audio-subtitle': 'हिंदी आवाज तैयार है',
        'btn-speak': '▶ आवाज सुनें (Play)',
        'advisory-lang-label': 'किसान भाषा / Language:',
        'btn-mode-preset': '⚡ 1-क्लिक सामान्य समस्याएं',
        'btn-mode-manual': '✍️ अपनी समस्या सीधे लिखें',
        'problem-statements-title': '👨‍🌾 सामान्य डेयरी समस्याएं (टाइप करने की जरूरत नहीं)',
        'problem-statements-subtitle': 'अपनी स्थिति से मेल खाने वाली समस्या पर टैप करें और तुरंत समाधान पाएं:',
        'instant-solution-badge': '⚡ त्वरित समाधान',
        'manual-entry-title': '✍️ अपनी समस्या का विवरण दें',
        'manual-entry-subtitle': 'अपनी समस्या हिंदी, अंग्रेजी या तेलुगु में लिखें या नीचे दिए गए टैग चुनें:',
        'symptom-chips-label': '⚡ सामान्य लक्षण (जोड़ने के लिए टैप करें):',
        'label-manual-problem': 'समस्या या स्थिति का विवरण दें:',
        'placeholder-manual-problem': 'उदाहरण: गाय का दूध अचानक घट गया है, चारे में फफूंद या दुर्गंध आ रही है...',
        'label-feed-type': 'चारे का प्रकार',
        'label-feed-smell': 'चारे की गंध',
        'label-feed-moisture': 'नमी की स्थिति',
        'label-feed-appearance': 'दिखावट',
        'label-cattle-symptom': 'पशु के लक्षण',
        'btn-submit-manual-advisory': '🚀 AI विश्लेषण करें',
        'btn-clear-manual-advisory': '🔄 साफ करें',
        'advisory-plan-title': '📜 किसान कार्य योजना व दिशा-निर्देश',

        // Tab 5: Dashboard
        'dashboard-header-title': '📊 चारा गुणवत्ता व डैशबोर्ड',
        'dashboard-header-subtitle': 'रीयल-टाइम आंकड़े, ट्रेंड विश्लेषण और पूर्व चेतावनी',
        'dashboard-kpi1-label': 'कुल परीक्षित बैच',
        'dashboard-kpi2-label': 'औसत स्वास्थ्य स्कोर',
        'dashboard-kpi3-label': 'सुरक्षित बैच %',
        'dashboard-kpi4-label': 'उच्च जोखिम चारा %',
        'dashboard-chart-trend-title': '📈 गुणवत्ता स्कोर ट्रेंड (पिछले 15 बैच)',
        'dashboard-chart-pie-title': '🍩 जोखिम स्तर वितरण',
        'dashboard-table-title': '📋 हालिया बैच ऑडिट रिकॉर्ड',
        'th-batch': 'बैच आईडी',
        'th-type': 'नमूना प्रकार',
        'th-score': 'स्कोर',
        'th-badge': 'दर्जा',
        'th-concern': 'प्रमुख चिंता',
        'th-time': 'समय',
        'table-loading-msg': 'रिकॉर्ड लोड हो रहे हैं...',

        // Tab 6: Feed Passport
        'passport-header-title': '📦 प्रमाणित डिजिटल फीड पासपोर्ट',
        'passport-header-subtitle': 'आधिकारिक सत्यापन सील व क्यूआर कोड युक्त बैच प्रमाणपत्र',
        'cert-protocol-label': 'स्मार्ट फीड डिजिटल ट्रेसेबिलिटी प्रोटोकॉल',
        'cert-title-label': '📦 डिजिटल फीड पासपोर्ट',
        'cert-lbl-type': 'नमूना प्रकार',
        'cert-lbl-score': 'स्वास्थ्य स्कोर',
        'cert-lbl-safety': 'सुरक्षा स्थिति',
        'cert-lbl-time': 'दर्ज समय',
        'cert-lbl-nutrients': 'सत्यापित पोषक प्रोफाइल',
        'cert-scan-prompt': 'बैच प्रामाणिकता सत्यापित करने के लिए स्कैन करें',
        'btn-print-cert': '🖨️ प्रिंट करें',
        'btn-download-qr': '⬇️ क्यूआर कोड डाउनलोड',

        // Tab 7: Batch Lookup
        'lookup-header-title': '🔎 बैच ट्रेसेबिलिटी व QR सत्यापन',
        'lookup-header-subtitle': 'पुराने रिकॉर्ड खोजें या क्यूआर कोड अपलोड करके सत्यापित करें',
        'lookup-search-title': '🔍 बैच आईडी से खोजें',
        'placeholder-lookup-batch': 'उदा: SFA-2026-000001',
        'btn-lookup-search': 'खोजें',
        'lookup-qr-title': '📷 क्यूआर कोड फोटो से सत्यापित करें',
        'lookup-dropzone-title': 'क्यूआर फोटो अपलोड करें',
        'lookup-details-title': '📋 बैच रिकॉर्ड विवरण',
        'lookup-result-placeholder': 'प्रमाणपत्र देखने के लिए बैच आईडी दर्ज करें या क्यूआर अपलोड करें।',
        'animal-rec-header-title': 'पशु-विशिष्ट चारा अनुशंसा और दैनिक खुराक',
        'animal-rec-header-sub': 'पशु-विशिष्ट चारा अनुशंसा • ICAR डेयरी पोषण मानक',
        'btn-speak-animal-rec-txt': 'आवाज सलाह सुनें',
        'lbl-quick-animal-select': '⚡ अपने पंजीकृत पशुओं में से चुनें (1-क्लिक):',
        'lbl-rec-species': '🐄 पशु का प्रकार',
        'lbl-rec-stage': '🤰 शारीरिक अवस्था',
        'lbl-rec-milk': '🥛 दूध उत्पादन',
        'btn-recalculate-rec-txt': 'खुराक की गणना करें',
        'rec-verdict-title': 'यह चारा आपके पशु के लिए उपयुक्त और सुरक्षित है!',
        'rec-verdict-note': 'गुणवत्ता स्कोर, प्रोटीन और नमी का स्तर संतुलित है।',
        'lbl-rec-daily-dose': 'कुल दैनिक खुराक',
        'lbl-rec-daily-sub': 'अनुशंसित दैनिक दाना',
        'lbl-rec-morning-dose': '🌅 सुबह का समय',
        'lbl-rec-morning-sub': '50% दैनिक हिस्सा',
        'lbl-rec-evening-dose': '🌆 शाम का समय',
        'lbl-rec-evening-sub': '50% दैनिक हिस्सा',
        'lbl-rec-balanced-title': 'संतुलित दैनिक आहार योजना (ICAR मानक)',
        'lbl-rec-diet-green': '🌿 हरा चारा',
        'lbl-rec-diet-straw': '🌾 सूखा भूसा',
        'lbl-rec-diet-minerals': '🧂 खनिज मिश्रण',
        'lbl-rec-diet-water': '💧 साफ पानी',
        'lbl-rec-adaptation-title': '4-दिवसीय क्रमिक अनुकूलन कार्यक्रम',
        'lbl-rec-rumen-badge': 'रूमेन सुरक्षा',
        'lbl-rec-vet-prefix': 'ℹ️ पशु चिकित्सा सलाह:',
        'btn-urea-mode-straw': '🌾 यूरिया भूसा उपचार',
        'btn-urea-mode-concentrate': '🥣 दैनिक दाने में मिलाना',
        'label-urea-qty': 'सूखे भूसे की मात्रा (kg)',
        'label-urea-animals': 'पशुओं की संख्या',
        'urea-steps-title': '📝 मानक संचालन प्रक्रिया',
        'urea-precautions-title': '⚠️ सुरक्षा सावधानियां और अनिवार्य नियम',
        'urea-antidote-title': 'प्राथमिक चिकित्सा व आपातकालीन विषनाशक',
        'advisory-lang-label': 'किसान की भाषा:',
        'btn-mode-preset': '⚡ 1-क्लिक सामान्य समस्याएं',
        'btn-mode-manual': '✍️ अपनी समस्या सीधे लिखें',
        'label-manual-problem': 'समस्या का विवरण दें:',
        'placeholder-manual-problem-input': 'उदाहरण: गाय का दूध अचानक घट गया है, चारे में फफूंद या दुर्गंध आ रही है...',
        'label-feed-type': 'चारे का प्रकार',
        'label-feed-smell': 'चारे की गंध',
        'label-feed-moisture': 'नमी की स्थिति',
        'label-feed-appearance': 'दिखावट',
        'label-cattle-symptom': 'पशु के लक्षण',
        'btn-submit-manual-advisory-txt': '🚀 AI से विश्लेषण करें',
        'btn-clear-manual-advisory-txt': '🔄 फॉर्म साफ करें',
        'tab-btn-login': '🔑 साइन इन',
        'tab-btn-register': '📝 पंजीकरण',
        'auth-demo-logins-title': '🛡️ भूमिका चयन एवं त्वरित विवरण (पासवर्ड आवश्यक)',
        'lbl-login-mobile': '📱 मोबाइल नंबर',
        'lbl-login-password': '🔒 पासवर्ड',
        'btn-submit-login': 'साइन इन करें',
        'lbl-login-new-prompt': 'नए किसान हैं?',
        'lnk-create-account': 'खाता बनाएं और फार्म सेटअप करें →',
        'lbl-reg-fullname': '👤 पूरा नाम',
        'lbl-reg-mobile': '📱 मोबाइल नंबर',
        'lbl-reg-email': '📧 ईमेल (वैकल्पिक)',
        'lbl-reg-password': '🔒 पासवर्ड',
        'lbl-reg-confirm-password': '🔒 पासवर्ड की पुष्टि करें',
        'lbl-reg-lang': '🌐 पसंदीदा भाषा',
        'btn-submit-register': 'खाता बनाएं',
        'lbl-reg-existing-prompt': 'पहले से पंजीकृत हैं?',
        'lnk-signin-here': 'यहां साइन इन करें →',
        'wizard-title-main': 'अपना फार्म प्रोफाइल सेट करें',
        'wz-nav-step1': 'बुनियादी जानकारी',
        'wz-nav-step2': 'पशुओं की संख्या',
        'wz-nav-step3': 'पशु प्रोफाइल',
        'wz-nav-step4': 'चारा और भंडारण',
        'wz-step1-title': '🌾 चरण 1 — फार्म की बुनियादी जानकारी',
        'wz-step1-subtitle': 'एआई चारा सलाह के लिए अपने फार्म का स्थान और पसंदीदा भाषा बताएं।',
        'lbl-wz-name': '👨‍🌾 किसान का नाम',
        'lbl-wz-village': '📍 गांव / स्थान',
        'lbl-wz-lang': '🌐 पसंदीदा भाषा',
        'btn-wz-next-1': 'आगे बढ़ें →',
        'wz-step2-title': '🐄 चरण 2 — आपके पास कितने पशु हैं?',
        'wz-step2-subtitle': 'अपने फार्म के पशु प्रकार और कुल संख्या चुनें।',
        'lbl-wz-total-animals': 'कुल पशु',
        'wz-step2-types-title': 'पशुओं के प्रकार चुनें:',
        'lbl-wz-cow-name': 'गाय',
        'wz-type-cow-sub': 'गायें',
        'lbl-wz-buff-name': 'भैंस',
        'wz-type-buff-sub': 'भैंसें',
        'btn-wz-back-2': '← पीछे जाएं',
        'btn-wz-next-2': 'आगे बढ़ें →',
        'wz-step3-title': '🐄 चरण 3 — प्रत्येक पशु का विवरण',
        'wz-step3-subtitle': 'प्रत्येक पशु का विवरण दें। ध्यान दें: गर्भवती या सूखी गायों के लिए दूध आवश्यक नहीं है।',
        'btn-wz-back-3': '← पीछे जाएं',
        'btn-wz-next-3': 'आगे बढ़ें →',
        'wz-step4-title': '🌾 चरण 4 — चारा व भंडारण विवरण',
        'wz-step4-subtitle': 'अपनी मुख्य चारा आपूर्ति और भंडारण व्यवस्था चुनें।',
        'lbl-wz-main-feed': '🌾 मुख्य चारे का प्रकार',
        'lbl-opt-green': 'हरा चारा',
        'lbl-opt-green-desc': 'नेपियर, मक्का, बरसीम, हरा चारा',
        'lbl-opt-dry': 'सूखा चारा',
        'lbl-opt-dry-desc': 'धान का पुआल, गेहूं का भूसा, कड़बी',
        'lbl-opt-silage': 'साइलेज',
        'lbl-opt-silage-desc': 'गड्ढे या बेल में किण्वित हरा चारा',
        'lbl-opt-conc': 'पशु आहार दाना',
        'lbl-opt-conc-desc': 'कंपाउंड पेलेट, दलिया, खल',
        'lbl-opt-mixed': 'मिश्रित चारा',
        'lbl-opt-mixed-desc': 'हरा + सूखा + दाना संतुलित मिश्रण',
        'lbl-wz-storage': '🏚️ चारा भंडारण स्थान',
        'lbl-opt-shed': 'बाड़ा / शेड',
        'lbl-opt-shed-desc': 'बारिश से सुरक्षित ढका हुआ शेड',
        'lbl-opt-pit': 'साइलेज गड्ढा',
        'lbl-opt-pit-desc': 'वायुरोधी बंकर गड्ढा या साइलो खंदक',
        'lbl-opt-room': 'भंडारण कक्ष',
        'lbl-opt-room-desc': 'हवादार पक्का कमरा',
        'lbl-opt-open': 'खुला क्षेत्र',
        'lbl-opt-open-desc': 'तिरपाल से ढका खुला स्थान',
        'btn-wz-back-4': '← पीछे जाएं',
        'btn-wz-finish': '🎉 सेटअप पूरा करें और डैशबोर्ड पर जाएं →',
        'my-animals-modal-title': 'मेरे पशुओं की सूची',
        'btn-animals-edit-setup': '⚙️ पशु संख्या व सेटअप बदलें',
        'btn-animals-done': 'संपन्न',
        'diary-modal-title': 'स्मार्ट चारा डायरी और समय योजना',
        'diary-modal-subtitle': 'सुबह, दोपहर, शाम के चारा समय, अनुस्मारक और दूध उत्पादन विश्लेषण',
        'diary-animal-select-lbl': '🐄 पशु का चयन:',
        'btn-diary-voice': 'आवाज योजना सुनें',
        'diary-next-slot-badge': 'अगला चारा समय',
        'diary-next-slot-desc': 'योजना के अनुसार चारा तैयार करें।',
        'btn-diary-log-now': '⏱️ अभी दर्ज करें',
        'diary-summary-title': 'आज के चारे और दूध उत्पादन का सारांश',
        'diary-conc-lbl': '🥣 दाना',
        'diary-green-lbl': '🌿 हरा चारा',
        'diary-straw-lbl': '🌾 सूखा भूसा',
        'diary-milk-lbl': '🥛 दर्ज दूध उत्पादन',
        'diary-target-conc': 'लक्ष्य: 0.0 kg',
        'diary-target-green': 'लक्ष्य: 0.0 kg',
        'diary-target-straw': 'लक्ष्य: 0.0 kg',
        'diary-target-milk': 'औसत: 8.0 L',
        'diary-insights-headline': 'एआई चारा विश्लेषण व दूध उत्पादन अंतर्दृष्टि',
        'diary-insights-body': 'सुबह, दोपहर और शाम का चारा दर्ज करें ताकि एआई विश्लेषण से पता चले कि किस चारे से दूध उत्पादन बढ़ा है।',
        'diary-modal-footer-note': '💡 ICAR राष्ट्रीय डेयरी अनुसंधान संस्थान (NDRI) मानक आहार योजना',
        'btn-diary-close': 'बंद करें',
        'modal-history-title': 'मेरे चारा परीक्षण रिकॉर्ड',
        'modal-history-loading': 'आपके सहेजे गए परीक्षण लोड हो रहे हैं...',
        'btn-modal-history-new': '📸 नया गुणवत्ता परीक्षण करें →',
        'btn-modal-history-close': 'बंद करें',
        'guest-card-title': 'किसान लॉगिन और फार्म प्रोफाइल सेटअप',
        'btn-guest-login': 'साइन इन',
        'home-tele-voice-val': 'हिंदी • తెలుగు • English',
        'farmer-history-section-title': '<span>📜</span> <span>मेरे चारा परीक्षण रिकॉर्ड</span>',
        'btn-start-app-title': '🚀 ऐप शुरू करें',
        'btn-start-sublabel': 'नैदानिक प्रणाली प्रारंभ करें',
        'link-splash-login': '🔑 किसान व व्यवस्थापक लॉगिन →',
        'link-splash-lang': '🌐 भाषा विकल्प →',
        'entry-lang-heading': 'अपनी भाषा चुनें',
        'entry-lang-subheading': 'जांच, सलाह और वॉयस ऑडियो के लिए अपनी भाषा चुनें',
        'btn-lang-back-txt': '← वापस',
        'btn-lang-next-txt': 'आगे (लॉगिन) →',
        'entry-auth-heading': 'किसान / व्यवस्थापक लॉगिन व पंजीकरण',
        'entry-auth-subheading': 'किसान व दुग्ध सहकारी समिति सुरक्षित पोर्टल प्रवेश',
        'entry-tab-login-txt': '🔑 साइन इन',
        'entry-tab-reg-txt': '📝 फार्म पंजीकरण',
        'entry-demo-logins-title': '🛡️ भूमिका चयन एवं त्वरित विवरण (पासवर्ड आवश्यक)',
        'lbl-entry-login-mobile': '📱 मोबाइल नंबर',
        'lbl-entry-login-pwd': '🔒 पासवर्ड',
        'btn-entry-signin-txt': '🔑 साइन इन करें →',
        'lbl-entry-new-farmer-prompt': 'नए किसान हैं?',
        'link-entry-create-account': 'खाता बनाएं और फार्म सेटअप करें →',
        'lbl-entry-reg-name': '👤 पूरा नाम',
        'lbl-entry-reg-mobile': '📱 मोबाइल नंबर',
        'lbl-entry-reg-email': '📧 ईमेल (वैकल्पिक)',
        'lbl-entry-reg-pwd': '🔒 पासवर्ड (न्यूनतम 4 अक्षर)',
        'lbl-entry-reg-cpwd': '🔒 पासवर्ड की पुष्टि करें',
        'lbl-entry-reg-lang': '🌐 पसंदीदा भाषा',
        'btn-entry-reg-txt': '📝 खाता बनाएं →',
        'lbl-entry-already-registered': 'पहले से पंजीकृत हैं?',
        'link-entry-signin': 'यहाँ साइन इन करें →',
        'btn-entry-back-lang-txt': '← भाषा चयन पर वापस जाएं',
        'placeholder-entry-login-mobile': '10 अंकों का मोबाइल नंबर',
        'placeholder-entry-login-password': 'पासवर्ड दर्ज करें',
        'placeholder-login-mobile': '10 अंकों का मोबाइल नंबर',
        'placeholder-login-password': 'पासवर्ड दर्ज करें',
        'placeholder-entry-reg-fullname': 'उदा: रमेश कुमार',
        'placeholder-entry-reg-mobile': '10 अंकों का मोबाइल नंबर',
        'placeholder-entry-reg-email': 'वैकल्पिक ईमेल पता',
        'placeholder-entry-reg-password': 'कम से कम 4 अक्षर',
        'placeholder-entry-reg-confirm-password': 'पासवर्ड दोबारा दर्ज करें'
    },
    en: {
        // Sidebar Navigation
        'sidebar-brand-title': 'SmartFeed AI',
        'sidebar-brand-slogan': 'FEED SMART • FARM BETTER',
        'sidebar-status-text': 'OFFLINE READY • LOCAL AI ACTIVE',
        'nav-home': 'Home',
        'nav-scanner': 'Quality Scanner',
        'nav-adulteration': 'Adulteration Check',
        'nav-advisory': 'AI Advisory',
        'nav-dashboard': 'Dashboard',
        'nav-passport': 'Feed Passport',
        'nav-lookup': 'Batch Lookup',
        'btn-reopen-lang-text': '🌐 Change Language',
        'mobile-lang-btn-text': '🌐 Language',
        'sidebar-lang-label': 'Farmer Language',
        'sidebar-engine-label': 'Advisory Engine',
        'sidebar-footer-text': '<strong>Smart India Hackathon 2026</strong><br>Low-Cost Software Prototype<br>Zero Specialized Hardware Required',

        // Tab 1: Home
        'hero-badge-text': 'SMART INDIA HACKATHON 2026 • AI AGRI-TECH INNOVATION',
        'hero-title-text': 'SmartFeed AI',
        'hero-motto-text': 'FEED SMART • FARM BETTER • GROW TOGETHER',
        'hero-desc-text': 'AI-Powered Smart Cattle Feed & Silage Quality Assessment, Multi-Factor Risk Intelligence, Explainable Advisory & QR Digital Traceability.',
        'home-btn-scan': 'Quality Scanner',
        'home-btn-adulteration': 'Adulteration Check',
        'home-btn-advisory': 'Farmer Advisory',
        'home-sci-notice': '<strong>Scientific Prototype Notice:</strong> SmartFeed AI delivers AI-based visual screening, OpenCV color/texture analytics, and multi-factor risk estimation. It is designed as a software decision support tool for dairy farmers. Laboratory testing is recommended for chemical confirmation.',
        'home-tele-edge-label': 'Edge AI Engine',
        'home-tele-edge-val': '< 300ms Local Latency',
        'home-tele-risk-label': 'Risk Intelligence',
        'home-tele-risk-val': '6-Factor Fusion',
        'home-tele-voice-label': 'Multilingual Voice',
        'home-tele-voice-val': 'English • Telugu • Hindi',
        'home-tele-trace-label': 'Traceability',
        'home-tele-trace-val': 'QR Digital Passport',
        'home-why-title': '🌟 Why SmartFeed AI?',
        'home-why-p1': 'Smallholder dairy farmers and rural milk cooperatives frequently face devastating drops in milk production, reproductive failure, and cattle toxicity caused by <strong>spoilage, mould mycotoxins, and urea adulteration</strong> in cattle feed and silage.',
        'home-why-p2': 'Traditional solutions require expensive laboratory testing equipment or physical spectrometers that rural farmers cannot afford.',
        'home-pitch-box': '<strong>💡 SIH Prototype Pitch:</strong><p style="color: var(--slate-700); font-size: 0.92rem; margin-top: 6px;"><em>"SmartFeed AI turns any standard smartphone camera into an intelligent feed diagnostic laboratory combining computer vision, OpenCV visual analysis, multi-factor risk assessment, simulated nutrition inputs, explainable multilingual advisory, and QR digital passports."</em></p>',
        'home-usps-title': '🏆 Core Innovations (USPs)',
        'home-usps-list': `
            <li>⭐ <strong>SmartFeed Health Score (0–100)</strong>: Single transparent score combining visual, fungal, particle, adulteration, nutrient, and storage parameters.</li>
            <li>🔍 <strong>Explainable AI ("Why This Result?")</strong>: Transparent point deduction breakdown explaining why feed is risky.</li>
            <li>🗣️ <strong>Multilingual Voice Advisory</strong>: Instant farmer advice in <strong>English, Telugu, and Hindi</strong> with browser audio synthesis.</li>
            <li>📦 <strong>QR Digital Feed Passport</strong>: Tamper-evident batch certificates (<code style="color: var(--accent-blue);">SFA-YYYY-XXXXXX</code>) for dairy cooperatives.</li>
            <li>📈 <strong>Early Spoilage Trend Warnings</strong>: Trajectory analysis detecting progressive quality deterioration before visible rot.</li>
            <li>📶 <strong>100% Offline Capability</strong>: Fully functional without internet connectivity.</li>
        `,
        'home-btn-scan': 'Quality Scanner',
        'home-btn-adulteration': 'Adulteration Check',
        'home-btn-advisory': 'Farmer Advisory',
        'home-btn-dashboard': 'Dashboard',
        'home-quick-title': '🚀 Interactive Feature Quick-Launch',
        'home-card1-title': '1. Feed Scanner',
        'home-card1-desc': 'Upload photo or use camera to detect discoloration, mould colonies & particles.',
        'btn-home-card1': '🚀 Open Scanner',
        'home-card2-title': '2. Adulteration Risk',
        'home-card2-desc': 'Check urea spiking & simulated non-protein nitrogen risks with interactive sliders.',
        'btn-home-card2': '🔬 Check Adulteration',
        'home-card3-title': '3. Farmer Advisory',
        'home-card3-desc': 'Listen to expert voice recommendations in Telugu, Hindi, or English.',
        'btn-home-card3': '🗣️ Voice Advisory',
        'home-card4-title': '4. Analytics Dashboard',
        'home-card4-desc': 'Live health score trends, risk distributions, and early spoilage warnings.',
        'btn-home-card4': '📈 View Dashboard',
        'home-card5-title': '5. QR Passport',
        'home-card5-desc': 'Inspect and download verifiable digital passports for dairy cooperatives.',
        'btn-home-card5': '📜 Verify Passport',
        'btn-refresh-dashboard': '🔄 Refresh Data',

        // Step 5: Farmer Personalized Dashboard & Tools
        'guest-card-title': 'Farmer Login & Farm Profile Setup',
        'guest-card-sub': 'Sign in or register to record your cattle count, monitor individual cows & buffaloes, and get customized voice advisory!',
        'btn-guest-login': '🔑 Sign In',
        'btn-guest-register': '📝 Register Farm',
        'title-farmer-features': '🌟 Dairy Farmer Diagnostic & Advisory Hub (8 Main Tools)',
        'btn-edit-farm': '⚙️ Edit Farm Setup',
        'btn-dash-new-scan': '📸 Scan Today\'s Feed',
        'fd-lbl-cows': 'Cows',
        'fd-lbl-buffs': 'Buffaloes',
        'fd-lbl-lact': 'Lactating',
        'fd-lbl-preg': 'Pregnant',
        'fd-lbl-feed': 'Main Feed',
        'fd-lbl-storage': 'Storage',
        'fd-lbl-tests': 'Scans Done',
        'tile1-title': '1. Feed Scanner',
        'tile1-sub': 'Visual & Mould AI Vision',
        'tile1-desc': 'Capture photo to detect discoloration, fungal patches, particles & 0-100 health score.',
        'tile1-btn': '🚀 Open Scanner →',
        'tile2-title': '2. Urea Checker',
        'tile2-sub': 'Safe Chemical Ratio',
        'tile2-desc': 'Screen chemical spiking & calculate safe 4% straw ammoniation / 1% concentrate limits.',
        'tile2-btn': '🔬 Calculate Safe Urea →',
        'tile3-title': '3. AI Advisory',
        'tile3-sub': 'Native Voice Guidance',
        'tile3-desc': 'Listen to tailored expert voice guidance in Telugu, Hindi or English for your cattle.',
        'tile3-btn': '🗣️ Listen Advisory →',
        'tile4-title': '4. My Animals',
        'tile4-sub': 'Individual Cattle Profiles',
        'tile4-desc': 'Inspect your registered cows & buffaloes, lactation stages, and tailored feeding targets.',
        'tile4-btn': '🐄 View Cattle Profiles →',
        'tile5-title': '5. Feed Diary',
        'tile5-sub': 'Daily Ration Records',
        'tile5-desc': 'Track daily feeding schedules, storage freshness, and ration consumption records.',
        'tile5-btn': '📝 View Feed Diary →',
        'tile6-title': '6. My Dashboard',
        'tile6-sub': 'Farm Analytics',
        'tile6-desc': 'View quality trends, safety risk charts, and progressive early spoilage warnings.',
        'tile6-btn': '📈 Open Dashboard →',
        'tile7-title': '7. My History',
        'tile7-sub': 'Past Batch Diagnostics',
        'tile7-desc': 'Look back at all past feed scans, health scores, and saved batch audit certificates.',
        'tile7-btn': '📋 View History →',
        'tile8-title': '8. QR Feed Passport',
        'tile8-sub': 'Digital Feed Passport',
        'tile8-desc': 'Generate official tamper-evident batch passports with verified QR for milk cooperatives.',
        'tile8-btn': '📦 View Passport →',

        // Farmer History Section
        'farmer-history-section-title': '<span>📜</span> <span>My Feed Diagnostic History</span>',
        'farmer-history-section-sub': 'Past analyzed feed batches, health scores, risk alerts, and digital passports under your farm account.',
        'btn-refresh-farmer-history': 'Refresh History',
        'btn-new-scan-farmer-history': 'New Quality Scan',
        'fth-batch': 'Batch ID',
        'fth-sample': 'Feed Sample',
        'fth-score': 'Quality Score',
        'fth-badge': 'Status',
        'fth-concern': 'Findings / Primary Risk',
        'fth-shelf': 'Safe Shelf Life',
        'fth-date': 'Date & Time',
        'fth-action': 'Actions',
        'modal-history-title': 'My Feed Test History',

        // Tab 2: Quality Scanner
        'scanner-header-title': '📸 SmartFeed Quality Scanner',
        'scanner-header-subtitle': 'Multi-Factor Computer Vision, Risk Intelligence & Digital Feed Passport Generation',
        'scanner-step1-title': '1. Capture or Select Feed Sample',
        'scanner-preset-label': '⚡ 1-Click Demo Sample Testing',
        'scanner-dropzone-title': 'Drag & Drop Feed Image or Click to Browse',
        'scanner-dropzone-sub': 'Supports JPG, PNG, WEBP',
        'scanner-sample-type-label': 'Sample Classification',
        'scanner-step2-title': '2. Nutritional & Storage Parameters',
        'label-slider-cp': 'Crude Protein (CP %)',
        'label-slider-moisture': 'Moisture Content (%)',
        'label-slider-npn': 'Non-Protein Nitrogen (NPN %)',
        'label-slider-days': 'Storage Duration (Days)',
        'label-check-smell': 'Noticeable Abnormal / Sour Smell Detected',
        'btn-scan': '🚀 Run Full Diagnostic Scan',
        'scanner-step3-title': '3. SmartFeed Diagnostic Assessment',
        'results-placeholder-title': 'Awaiting Sample Submission',
        'results-placeholder-desc': 'Select a preset demo sample or upload a feed image and click Run Diagnostic Scan to compute health score.',
        'gauge-heading': '🐄 SMARTFEED HEALTH SCORE',
        'gauge-score-sub': 'OUT OF 100',
        'shelf-life-card-title': '⏳ AI Feed Shelf-Life & Spoilage Forecast',
        'shelf-days-label': 'Days Safe to Feed',
        'shelf-sub-expiry-label': 'Safe Until Date:',
        'shelf-sub-moist-label': 'Moisture Impact:',
        'shelf-timeline-now': 'Fresh / Today',
        'shelf-timeline-status': 'Safe Storage Window',
        'shelf-timeline-spoil': 'Spoilage Risk Phase',
        'cert-lbl-shelf': 'Shelf Life & Expiry',
        'animal-rec-header-title': 'Animal-Specific Feed Recommendation & Dosage',
        'animal-rec-header-sub': 'Scientific Feeding Dosage • ICAR & NDDB Dairy Cattle Nutrition Standards',
        'btn-speak-animal-rec-txt': 'Listen Voice Guidance (Audio)',
        'lbl-quick-animal-select': '⚡ Quick-Select From Your Registered Cattle (1-Click):',
        'lbl-rec-species': '🐄 Animal Species',
        'lbl-rec-stage': '🤰 Physiological Stage',
        'lbl-rec-milk': '🥛 Milk Yield / Production',
        'btn-recalculate-rec-txt': 'Calculate Feed Dosage',
        'lbl-rec-daily-dose': 'Total Daily Dosage',
        'lbl-rec-daily-sub': 'Recommended Feed Allowance',
        'lbl-rec-morning-dose': '🌅 Morning Ration',
        'lbl-rec-evening-dose': '🌆 Evening Ration',
        'lbl-rec-balanced-title': 'ICAR Balanced Daily Diet Pairing',
        'lbl-rec-adaptation-title': '4-Day Gradual Rumen Adaptation Protocol',
        'explainable-ai-title': '🔍 Explainable AI: "Why This Result?"',
        'cv-metrics-title': '👁️ OpenCV Vision Metrics',
        'passport-box-title': '📦 Digital Feed Passport Generated!',
        'btn-view-passport': '📜 View Certified Passport & QR Code',

        // Tab 3: Adulteration Check
        'adulteration-header-title': '⚠️ Feed Adulteration & Urea Spiking Risk',
        'adulteration-header-subtitle': 'Non-Protein Nitrogen (NPN) Discrepancy & Visual Filler Particle Detection',
        'adulteration-alert-notice': '<strong>Scientific Notice:</strong> Unethical suppliers may artificially inflate apparent crude protein content using inexpensive <strong>fertilizer-grade urea</strong> (46% Nitrogen) or chalk fillers. This module flags anomalous protein-to-nitrogen ratios. Laboratory HPLC/combustion testing is required for legal confirmation.',
        'adulteration-params-title': '🧪 Adulteration Simulator Parameters',
        'label-ad-cp': 'Crude Protein (CP %)',
        'label-ad-moisture': 'Moisture Content (%)',
        'label-ad-npn': 'Non-Protein Nitrogen (NPN %)',
        'label-ad-powder': 'Visual Crystalline / Powder Particles',
        'adulteration-output-title': '📊 Adulteration Prediction Output',
        'urea-calc-title': '🌾 Scientific Safe Urea Dosage & Straw Treatment Calculator',
        'urea-calc-subtitle': 'ICAR & NDDB Certified Non-Toxic Urea Ammoniation & Daily Concentrate Mixing Guide',
        'urea-calc-standard-badge': '✅ ICAR 4% Standard',
        'btn-urea-mode-straw': '🌾 Urea Straw Treatment (4% ICAR Standard)',
        'btn-urea-mode-concentrate': '🥣 Daily Concentrate Ration Mixing (Max 1% DM)',
        'label-kpi-urea': 'Scientifically Safe Urea',
        'label-kpi-water': 'Required Water',
        'label-kpi-curing': 'Curing / Incubation Period',
        'label-kpi-protein': 'Nutritional Gain (Protein)',
        'label-advisory-summary': '📋 RECOMMENDED DOSAGE SUMMARY',
        'btn-speak-urea-text': 'Listen Voice Guide',
        'urea-steps-title': '📝 Standard Operating Procedure (SOP Checklist)',
        'urea-precautions-title': '⚠️ Safety Precautions & Mandatory Rules',
        'urea-antidote-title': '🚑 FIRST AID & EMERGENCY ANTIDOTE',

        // Tab 4: AI Advisory
        'advisory-header-title': '🤖 Farmer Multilingual Advisory & Voice',
        'advisory-header-subtitle': 'Real Native Audio (Telugu, Hindi, English) with 1-Click Problem Statements',
        'audio-speaker-heading': '🔊 SMARTFEED NATIVE AUDIO ASSISTANT',
        'audio-title': 'Listen to Farmer Advisory in Native Voice',
        'audio-subtitle': 'Native Voice Ready: English',
        'btn-speak': '▶ Play Voice Audio',
        'advisory-lang-label': 'Farmer Language:',
        'btn-mode-preset': '⚡ 1-Click Common Statements',
        'btn-mode-manual': '✍️ Manual / Custom Problem Entry',
        'problem-statements-title': '👨‍🌾 1-Click Common Farmer Problem Statements',
        'problem-statements-subtitle': 'Farmers don\'t need to type — simply tap the statement that matches your cattle\'s situation:',
        'instant-solution-badge': '⚡ Instant Solution',
        'manual-entry-title': '✍️ Manual / Custom Problem Diagnosis',
        'manual-entry-subtitle': 'Type your problem in English, Telugu, or Hindi, or click quick symptom tags below:',
        'symptom-chips-label': '⚡ Quick Symptom Tags (Tap to Add):',
        'label-manual-problem': 'Describe What Happened / Details:',
        'placeholder-manual-problem': 'e.g., Milk yield dropped suddenly and feed has sour/musty smell...',
        'label-feed-type': 'Feed Type',
        'label-feed-smell': 'Feed Smell',
        'label-feed-moisture': 'Moisture Status',
        'label-feed-appearance': 'Appearance',
        'label-cattle-symptom': 'Cattle Symptoms',
        'btn-submit-manual-advisory': '🚀 Analyze Problem with AI',
        'btn-clear-manual-advisory': '🔄 Clear Form',
        'advisory-plan-title': '📜 Tailored Farmer Action Plan',

        // Tab 5: Dashboard
        'dashboard-header-title': '📊 Feed Quality & Spoilage Dashboard',
        'dashboard-header-subtitle': 'Real-Time Aggregated Metrics, Trend Analytics & Non-Alarmist Spoilage Warnings',
        'dashboard-kpi1-label': 'Total Batches Tested',
        'dashboard-kpi2-label': 'Average Health Score',
        'dashboard-kpi3-label': 'Safe Batches %',
        'dashboard-kpi4-label': 'High-Risk Feed %',
        'dashboard-chart-trend-title': '📈 Quality Score Trend (Last 15 Batches)',
        'dashboard-chart-pie-title': '🍩 Risk Level Distribution',
        'dashboard-table-title': '📋 Recent Batch Audit Records',
        'th-batch': 'Batch ID',
        'th-type': 'Sample Type',
        'th-score': 'Score',
        'th-badge': 'Badge',
        'th-concern': 'Primary Concern',
        'th-time': 'Timestamp',
        'table-loading-msg': 'Loading records...',

        // Tab 6: Feed Passport
        'passport-header-title': '📦 Certified Digital Feed Passport',
        'passport-header-subtitle': 'Tamper-Evident Batch Certificate with Official Verification Seal & QR Code',
        'cert-protocol-label': 'SMARTFEED DIGITAL TRACEABILITY PROTOCOL',
        'cert-title-label': '📦 DIGITAL FEED PASSPORT',
        'cert-lbl-type': 'Sample Classification',
        'cert-lbl-score': 'Health Score',
        'cert-lbl-safety': 'Safety Status',
        'cert-lbl-time': 'Timestamp',
        'cert-lbl-nutrients': 'Verified Nutrient Profile',
        'cert-scan-prompt': 'Scan to verify batch authenticity',
        'btn-print-cert': '🖨️ Print Certificate',
        'btn-download-qr': '⬇️ Download QR Code',

        // Tab 7: Batch Lookup
        'lookup-header-title': '🔎 Batch Traceability & QR Verification',
        'lookup-header-subtitle': 'Search Historical Test Records or Upload QR Code for Tamper Verification',
        'lookup-search-title': '🔍 Search by Batch ID',
        'placeholder-lookup-batch': 'e.g. SFA-2026-000001',
        'btn-lookup-search': 'Search',
        'lookup-qr-title': '📷 Verify via QR Code Image',
        'lookup-dropzone-title': 'Upload QR Image to Decode Batch',
        'lookup-details-title': '📋 Batch Record Details',
        'lookup-result-placeholder': 'Enter a Batch ID or upload a QR image to verify feed certificate.',
        'animal-rec-header-title': 'Animal-Specific Feed Recommendation & Daily Dosage',
        'animal-rec-header-sub': 'Animal-Specific Feed Recommendation • ICAR Dairy Cattle Nutrition Benchmarks',
        'btn-speak-animal-rec-txt': 'Listen Voice Advisory',
        'lbl-quick-animal-select': '⚡ Select From Your Cattle (1-Click Quick-Pick):',
        'lbl-rec-species': '🐄 Animal Type',
        'lbl-rec-stage': '🤰 Physiological Stage',
        'lbl-rec-milk': '🥛 Milk Yield / Production',
        'btn-recalculate-rec-txt': 'Calculate Dosage',
        'rec-verdict-title': 'This feed is suitable and safe for your cattle!',
        'rec-verdict-note': 'Quality score, crude protein, and moisture levels are well balanced.',
        'lbl-rec-daily-dose': 'Total Daily Dosage',
        'lbl-rec-daily-sub': 'Recommended Daily Concentrate',
        'lbl-rec-morning-dose': '🌅 Morning Feeding',
        'lbl-rec-morning-sub': '50% Daily Share',
        'lbl-rec-evening-dose': '🌆 Evening Feeding',
        'lbl-rec-evening-sub': '50% Daily Share',
        'lbl-rec-balanced-title': 'Balanced Daily Diet Plan (ICAR Benchmark)',
        'lbl-rec-diet-green': '🌿 Green Fodder',
        'lbl-rec-diet-straw': '🌾 Dry Straw',
        'lbl-rec-diet-minerals': '🧂 Mineral Mixture',
        'lbl-rec-diet-water': '💧 Clean Water',
        'lbl-rec-adaptation-title': '4-Day Gradual Adaptation Schedule',
        'lbl-rec-rumen-badge': 'Rumen Protection',
        'lbl-rec-vet-prefix': 'ℹ️ Veterinary Advice:',
        'btn-urea-mode-straw': '🌾 Urea Straw Treatment',
        'btn-urea-mode-concentrate': '🥣 Daily Concentrate Ration Mixing',
        'label-urea-qty': 'Dry Straw Quantity (kg)',
        'label-urea-animals': 'Number of Cattle',
        'urea-steps-title': '📝 Standard Operating Procedure',
        'urea-precautions-title': '⚠️ Safety Precautions & Mandatory Rules',
        'urea-antidote-title': 'FIRST AID & EMERGENCY ANTIDOTE',
        'advisory-lang-label': 'Farmer Language:',
        'btn-mode-preset': '⚡ 1-Click Common Statements',
        'btn-mode-manual': '✍️ Manual / Custom Problem Entry',
        'label-manual-problem': 'Describe What Happened:',
        'placeholder-manual-problem-input': 'Example: Cattle milk yield dropped suddenly, feed has sour smell or mould patches...',
        'label-feed-type': 'Feed Type',
        'label-feed-smell': 'Feed Smell',
        'label-feed-moisture': 'Moisture Status',
        'label-feed-appearance': 'Appearance',
        'label-cattle-symptom': 'Cattle Symptoms',
        'btn-submit-manual-advisory-txt': '🚀 Analyze Problem with AI',
        'btn-clear-manual-advisory-txt': '🔄 Clear Form',
        'tab-btn-login': '🔑 Sign In',
        'tab-btn-register': '📝 Register',
        'auth-demo-logins-title': '🛡️ Role Selector & Quick Fill (Password Required)',
        'lbl-login-mobile': '📱 Mobile Number',
        'lbl-login-password': '🔒 Password',
        'btn-submit-login': 'Sign In',
        'lbl-login-new-prompt': 'New farmer?',
        'lnk-create-account': 'Create Account & Farm Setup →',
        'lbl-reg-fullname': '👤 Full Name',
        'lbl-reg-mobile': '📱 Mobile Number',
        'lbl-reg-email': '📧 Email (Optional)',
        'lbl-reg-password': '🔒 Password',
        'lbl-reg-confirm-password': '🔒 Confirm Password',
        'lbl-reg-lang': '🌐 Preferred Language',
        'btn-submit-register': 'Create Account',
        'lbl-reg-existing-prompt': 'Already registered?',
        'lnk-signin-here': 'Sign In here →',
        'wizard-title-main': 'Set Up Your Farm Profile',
        'wz-nav-step1': 'Farm Basic',
        'wz-nav-step2': 'Animals Count',
        'wz-nav-step3': 'Animal Profiles',
        'wz-nav-step4': 'Feed & Storage',
        'wz-step1-title': '🌾 Step 1 — Farm Basic Details',
        'wz-step1-subtitle': 'Tell us about your farm location and language preference to customize AI feed recommendations.',
        'lbl-wz-name': '👨‍🌾 Farmer Name',
        'lbl-wz-village': '📍 Village / Location',
        'lbl-wz-lang': '🌐 Preferred Language',
        'btn-wz-next-1': 'Next →',
        'wz-step2-title': '🐄 Step 2 — How Many Animals?',
        'wz-step2-subtitle': 'Select animal types and total cattle count on your farm.',
        'lbl-wz-total-animals': 'Total Animals',
        'wz-step2-types-title': 'Select Animal Types:',
        'lbl-wz-cow-name': 'Cow',
        'wz-type-cow-sub': 'Cows',
        'lbl-wz-buff-name': 'Buffalo',
        'wz-type-buff-sub': 'Buffaloes',
        'btn-wz-back-2': '← Back',
        'btn-wz-next-2': 'Next →',
        'wz-step3-title': '🐄 Step 3 — Individual Animal Profiles',
        'wz-step3-subtitle': 'Provide details for each animal. Note: Pregnant or Dry animals do not require milk production.',
        'btn-wz-back-3': '← Back',
        'btn-wz-next-3': 'Next →',
        'wz-step4-title': '🌾 Step 4 — Feed & Storage Details',
        'wz-step4-subtitle': 'Select your primary feed supply and storage infrastructure.',
        'lbl-wz-main-feed': '🌾 Main Feed Type',
        'lbl-opt-green': 'Green Fodder',
        'lbl-opt-green-desc': 'Napier, SSG, Maize, Berseem',
        'lbl-opt-dry': 'Dry Fodder',
        'lbl-opt-dry-desc': 'Paddy Straw, Wheat Straw, Kadbi',
        'lbl-opt-silage': 'Silage',
        'lbl-opt-silage-desc': 'Fermented green fodder in pit/bale',
        'lbl-opt-conc': 'Cattle Feed',
        'lbl-opt-conc-desc': 'Compound pellet, mash feed, cakes',
        'lbl-opt-mixed': 'Mixed Feed',
        'lbl-opt-mixed-desc': 'Green + dry + concentrate balanced mix',
        'lbl-wz-storage': '🏚️ Feed Storage Location',
        'lbl-opt-shed': 'Shed',
        'lbl-opt-shed-desc': 'Covered shelter protected from rain',
        'lbl-opt-pit': 'Silage Pit',
        'lbl-opt-pit-desc': 'Anaerobic bunker pit or silo trench',
        'lbl-opt-room': 'Storage Room',
        'lbl-opt-room-desc': 'Ventilated concrete store room',
        'lbl-opt-open': 'Open Area',
        'lbl-opt-open-desc': 'Outdoor stack with plastic tarpaulin',
        'btn-wz-back-4': '← Back',
        'btn-wz-finish': '🎉 Finish Setup & Go to Dashboard →',
        'my-animals-modal-title': 'My Animals Directory',
        'btn-animals-edit-setup': '⚙️ Edit Animal Count & Setup',
        'btn-animals-done': 'Done',
        'diary-modal-title': 'Smart Feeding Planner & Dairy Intelligence',
        'diary-modal-subtitle': 'Morning, Afternoon & Evening Feeding Times, Reminders & Milk Yield Analysis',
        'diary-animal-select-lbl': '🐄 Select Animal:',
        'btn-diary-voice': 'Listen Voice Plan',
        'diary-next-slot-badge': 'Next Feeding Slot',
        'diary-next-slot-desc': 'Prepare feed according to plan.',
        'btn-diary-log-now': '⏱️ Log Now',
        'diary-summary-title': 'Daily Feeding & Milk Yield Summary',
        'diary-conc-lbl': '🥣 Concentrate',
        'diary-green-lbl': '🌿 Green Fodder',
        'diary-straw-lbl': '🌾 Dry Straw',
        'diary-milk-lbl': '🥛 Logged Milk Yield',
        'diary-target-conc': 'Target: 0.0 kg',
        'diary-target-green': 'Target: 0.0 kg',
        'diary-target-straw': 'Target: 0.0 kg',
        'diary-target-milk': 'Avg: 8.0 L',
        'diary-insights-headline': 'AI Feeding Pattern & Milk Intelligence',
        'diary-insights-body': 'Log morning, afternoon, and evening feeding to get AI-powered insights on which feed combination optimizes your cattle\'s milk yield.',
        'diary-modal-footer-note': '💡 ICAR National Dairy Research Institute (NDRI) Standard Diet Plan',
        'btn-diary-close': 'Close',
        'modal-history-title': 'My Feed Test History',
        'modal-history-loading': 'Loading your saved diagnostic scans...',
        'btn-modal-history-new': '📸 Run New Quality Scan →',
        'btn-modal-history-close': 'Close',
        'guest-card-title': 'Farmer Login & Farm Profile Setup',
        'btn-guest-login': 'Sign In',
        'home-tele-voice-val': 'English • Telugu • Hindi',
        'farmer-history-section-title': '<span>📜</span> <span>My Feed Diagnostic History</span>',
        'btn-start-app-title': '🚀 START THE APP',
        'btn-start-sublabel': 'Launch Diagnostic System',
        'link-splash-login': '🔑 Farmer & Admin Login →',
        'link-splash-lang': '🌐 Language Options →',
        'entry-lang-heading': 'Choose Your Language',
        'entry-lang-subheading': 'Select preferred language for diagnostics, advisories & native voice',
        'btn-lang-back-txt': '← Back',
        'btn-lang-next-txt': 'Next (Sign In) →',
        'entry-auth-heading': 'Sign In to SmartFeed AI',
        'entry-auth-subheading': 'Farmer & Cooperative Admin Secure Portal Access',
        'entry-tab-login-txt': '🔑 Sign In',
        'entry-tab-reg-txt': '📝 Register Farm',
        'entry-demo-logins-title': '🛡️ Role Selector & Quick Fill (Password Required)',
        'lbl-entry-login-mobile': '📱 Mobile Number',
        'lbl-entry-login-pwd': '🔒 Password',
        'btn-entry-signin-txt': '🔑 Sign In →',
        'lbl-entry-new-farmer-prompt': 'New farmer?',
        'link-entry-create-account': 'Create Account & Setup Farm →',
        'lbl-entry-reg-name': '👤 Full Name',
        'lbl-entry-reg-mobile': '📱 Mobile Number',
        'lbl-entry-reg-email': '📧 Email (Optional)',
        'lbl-entry-reg-pwd': '🔒 Password (At least 4 characters)',
        'lbl-entry-reg-cpwd': '🔒 Confirm Password',
        'lbl-entry-reg-lang': '🌐 Preferred Language',
        'btn-entry-reg-txt': '📝 Create Account →',
        'lbl-entry-already-registered': 'Already registered?',
        'link-entry-signin': 'Sign In here →',
        'btn-entry-back-lang-txt': '← Back to Language',
        'placeholder-entry-login-mobile': '10-digit mobile number',
        'placeholder-entry-login-password': 'Enter your password',
        'placeholder-login-mobile': '10-digit mobile number',
        'placeholder-login-password': 'Enter your password',
        'placeholder-entry-reg-fullname': 'e.g. Ramesh Kumar',
        'placeholder-entry-reg-mobile': '10-digit mobile number',
        'placeholder-entry-reg-email': 'Optional email address',
        'placeholder-entry-reg-password': 'At least 4 characters',
        'placeholder-entry-reg-confirm-password': 'Re-enter password'
    }
};

// ===================================================================
// Welcome Portal Overlay & Language Selector Functions
// ===================================================================

function showPortalLanguageStep() {
    const step1 = document.getElementById('portal-step-intro');
    const step2 = document.getElementById('portal-step-language');
    if (step1 && step2) {
        step1.style.display = 'none';
        step2.style.display = 'block';
    }
}

function backToIntroStep() {
    const step1 = document.getElementById('portal-step-intro');
    const step2 = document.getElementById('portal-step-language');
    if (step1 && step2) {
        step2.style.display = 'none';
        step1.style.display = 'block';
    }
}

function dismissWelcomePortal() {
    const overlay = document.getElementById('welcome-portal-overlay');
    if (overlay) {
        overlay.classList.add('portal-fade-out');
        setTimeout(() => {
            overlay.style.display = 'none';
            overlay.classList.remove('portal-fade-out');
        }, 350);
    }
}

function selectPortalLanguage(lang) {
    setLanguage(lang);
    try {
        localStorage.setItem('smartfeed_lang', lang);
    } catch (e) {}

    dismissWelcomePortal();
}

function reopenLanguagePortal() {
    const overlay = document.getElementById('welcome-portal-overlay');
    const step1 = document.getElementById('portal-step-intro');
    const step2 = document.getElementById('portal-step-language');
    if (overlay && step1 && step2) {
        step1.style.display = 'none';
        step2.style.display = 'block';
        overlay.style.display = 'flex';
    }
}

// Expose portal functions globally
window.showPortalLanguageStep = showPortalLanguageStep;
window.backToIntroStep = backToIntroStep;
window.dismissWelcomePortal = dismissWelcomePortal;
window.selectPortalLanguage = selectPortalLanguage;
window.reopenLanguagePortal = reopenLanguagePortal;

// ===================================================================
// Whole-Application Language Application Engine
// ===================================================================

function applyAppLanguage(lang) {
    const dict = I18N_APP[lang] || I18N_APP.en;

    for (const [id, value] of Object.entries(dict)) {
        if (id.startsWith('placeholder-')) {
            const targetId = id.replace('placeholder-', '');
            const el = document.getElementById(targetId);
            if (el) el.placeholder = value;
        } else {
            const el = document.getElementById(id);
            if (el) {
                if (typeof value === 'string' && value.includes('<')) {
                    el.innerHTML = value;
                } else {
                    el.innerText = value;
                }
            }
        }
    }

    // Localize interactive select dropdown options
    updateLocalizedSelectOptions(lang);
}

function updateLocalizedSelectOptions(lang) {
    // 1. Scanner Sample Classification
    const scannerSampleSelect = document.getElementById('scanner-sample-type');
    if (scannerSampleSelect) {
        const labels = {
            te: {
                'Cattle Feed Pellet': 'దాణా పెల్లెట్స్',
                'Maize Silage': 'మొక్కజొన్న సైలేజ్',
                'Cottonseed Cake': 'పత్తి చెక్క',
                'Wheat Bran': 'గోధుమ తవుడు',
                'Mixed Ration (TMR)': 'మిశ్రమ సమతుల్య ఆహారం'
            },
            hi: {
                'Cattle Feed Pellet': 'पशु आहार पेलेट',
                'Maize Silage': 'मक्का साइलेज',
                'Cottonseed Cake': 'बिनौला खल',
                'Wheat Bran': 'गेहूं का चोकर',
                'Mixed Ration (TMR)': 'मिश्रित संतुलित आहार'
            },
            en: {
                'Cattle Feed Pellet': 'Cattle Feed Pellet',
                'Maize Silage': 'Maize Silage',
                'Cottonseed Cake': 'Cottonseed Cake',
                'Wheat Bran': 'Wheat Bran',
                'Mixed Ration (TMR)': 'Total Mixed Ration (TMR)'
            }
        };
        const activeLabels = labels[lang] || labels.en;
        Array.from(scannerSampleSelect.options).forEach(opt => {
            if (activeLabels[opt.value]) opt.text = activeLabels[opt.value];
        });
    }

    // 2. Preset Demo Samples Selector
    const presetSelect = document.getElementById('preset-sample-select');
    if (presetSelect) {
        const presetLabels = {
            te: {
                '': '-- డెమో నమూనాను ఎంచుకోండి --',
                'sample_healthy_feed.jpg': '🟢 ఆరోగ్యకరమైన బంగారు దాణా (సురక్షితం)',
                'sample_mouldy_feed.jpg': '🔴 బూజు పట్టిన దాణా (అధిక రిస్క్)',
                'sample_burnt_feed.jpg': '🟡 మాడిన దాణా (శ్రద్ధ అవసరం)',
                'sample_fresh_silage.jpg': '🟢 తాజా మొక్కజొన్న సైలేజ్ (సురక్షితం)'
            },
            hi: {
                '': '-- डेमो नमूना चुनें --',
                'sample_healthy_feed.jpg': '🟢 स्वस्थ सुनहरा पशु आहार (सुरक्षित)',
                'sample_mouldy_feed.jpg': '🔴 फफूंद लगा आहार (उच्च जोखिम)',
                'sample_burnt_feed.jpg': '🟡 अधिक तपा चारा (ध्यान दें)',
                'sample_fresh_silage.jpg': '🟢 ताजा मक्का साइलेज (सुरक्षित)'
            },
            en: {
                '': '-- Choose a Preset Demo Image --',
                'sample_healthy_feed.jpg': '🟢 Healthy Golden Cattle Feed (Safe)',
                'sample_mouldy_feed.jpg': '🔴 Mouldy Feed with Fungal Patches (High Risk)',
                'sample_burnt_feed.jpg': '🟡 Burnt / Heat Damaged Feed (Needs Attention)',
                'sample_fresh_silage.jpg': '🟢 Fresh Maize Silage (Safe)'
            }
        };
        const activePresetLabels = presetLabels[lang] || presetLabels.en;
        Array.from(presetSelect.options).forEach(opt => {
            if (activePresetLabels[opt.value] !== undefined) opt.text = activePresetLabels[opt.value];
        });
    }

    // 3. Animal Recommendation: Animal Type Dropdown
    const recAnimalType = document.getElementById('rec-animal-type');
    if (recAnimalType) {
        const animalLabels = {
            te: { 'Cow': '🐄 ఆవు', 'Buffalo': '🐃 గేదె' },
            hi: { 'Cow': '🐄 गाय', 'Buffalo': '🐃 भैंस' },
            en: { 'Cow': '🐄 Cow', 'Buffalo': '🐃 Buffalo' }
        };
        const active = animalLabels[lang] || animalLabels.en;
        Array.from(recAnimalType.options).forEach(opt => {
            if (active[opt.value]) opt.text = active[opt.value];
        });
    }

    // 4. Animal Recommendation: Lactation Stage Dropdown
    const recLactStage = document.getElementById('rec-lactation-stage');
    if (recLactStage) {
        const stageLabels = {
            te: { 'Lactating': '🥛 పాలిచ్చేది', 'Pregnant': '🤰 చూడి', 'Dry': '🌾 ఎండినది' },
            hi: { 'Lactating': '🥛 दुधारू', 'Pregnant': '🤰 गर्भवती', 'Dry': '🌾 सूखी' },
            en: { 'Lactating': '🥛 Lactating', 'Pregnant': '🤰 Pregnant', 'Dry': '🌾 Dry' }
        };
        const active = stageLabels[lang] || stageLabels.en;
        Array.from(recLactStage.options).forEach(opt => {
            if (active[opt.value]) opt.text = active[opt.value];
        });
    }

    // 5. Manual Feed Type Select
    const manualFeedSelect = document.getElementById('manual-feed-type');
    if (manualFeedSelect) {
        const manualFeedLabels = {
            te: {
                'Cattle Feed Pellet': 'దాణా పెల్లెట్',
                'Maize Silage': 'మొక్కజొన్న సైలేజ్',
                'Cottonseed Cake': 'పత్తి చెక్క',
                'Groundnut Cake': 'వేరుశనగ చెక్క',
                'Wheat Bran': 'గోధుమ తవుడు',
                'Green Fodder': 'పచ్చిగడ్డి',
                'Dry Straw / Hay': 'ఎండుగడ్డి'
            },
            hi: {
                'Cattle Feed Pellet': 'पशु आहार पेलेट',
                'Maize Silage': 'मक्का साइलेज',
                'Cottonseed Cake': 'बिनौला खल',
                'Groundnut Cake': 'मूंगफली खल',
                'Wheat Bran': 'गेहूं का चोकर',
                'Green Fodder': 'हरा चारा',
                'Dry Straw / Hay': 'सूखा भूसा'
            },
            en: {
                'Cattle Feed Pellet': 'Cattle Feed Pellet',
                'Maize Silage': 'Maize Silage',
                'Cottonseed Cake': 'Cottonseed Cake',
                'Groundnut Cake': 'Groundnut Cake',
                'Wheat Bran': 'Wheat Bran',
                'Green Fodder': 'Green Fodder',
                'Dry Straw / Hay': 'Dry Straw / Hay'
            }
        };
        const active = manualFeedLabels[lang] || manualFeedLabels.en;
        Array.from(manualFeedSelect.options).forEach(opt => {
            if (active[opt.value]) opt.text = active[opt.value];
        });
    }

    // 6. Manual Feed Smell Select
    const smellSelect = document.getElementById('manual-feed-smell');
    if (smellSelect) {
        const smellLabels = {
            te: {
                'Normal': 'సాధారణ సహజ వాసన',
                'Fungal/Musty': 'బూజు వాసన',
                'Sour/Rotten': 'పుల్లని లేదా కుళ్ళిన వాసన',
                'Chemical/Urea': 'యూరియా లేదా రసాయన ఘాటు వాసన',
                'Burnt/Heated': 'మాడిన వాసన'
            },
            hi: {
                'Normal': 'सामान्य प्राकृतिक गंध',
                'Fungal/Musty': 'फफूंद या सीलन की गंध',
                'Sour/Rotten': 'खट्टी या सड़ी हुई गंध',
                'Chemical/Urea': 'यूरिया या तीखी रासायनिक गंध',
                'Burnt/Heated': 'जली हुई गंध'
            },
            en: {
                'Normal': 'Normal Fresh Smell',
                'Fungal/Musty': 'Fungal / Musty Smell',
                'Sour/Rotten': 'Sour / Rotten Smell',
                'Chemical/Urea': 'Chemical / Pungent Urea',
                'Burnt/Heated': 'Burnt / Self-Heated'
            }
        };
        const active = smellLabels[lang] || smellLabels.en;
        Array.from(smellSelect.options).forEach(opt => {
            if (active[opt.value]) opt.text = active[opt.value];
        });
    }

    // 7. Manual Feed Moisture Select
    const moistSelect = document.getElementById('manual-feed-moisture');
    if (moistSelect) {
        const moistLabels = {
            te: {
                'Normal': 'పొడిగా సరైన స్థితిలో ఉంది',
                'Damp': 'తేమగా లేదా ముద్దలుగా ఉంది',
                'Soaked/Rain Damage': 'వర్షంలో బాగా తడిసింది'
            },
            hi: {
                'Normal': 'सामान्य सूखा',
                'Damp': 'सीलन युक्त या ढेलेदार',
                'Soaked/Rain Damage': 'बारिश में भीगा हुआ'
            },
            en: {
                'Normal': 'Normal / Dry',
                'Damp': 'Damp / Clumpy',
                'Soaked/Rain Damage': 'Soaked in Rain'
            }
        };
        const active = moistLabels[lang] || moistLabels.en;
        Array.from(moistSelect.options).forEach(opt => {
            if (active[opt.value]) opt.text = active[opt.value];
        });
    }

    // 8. Manual Feed Appearance Select
    const appearSelect = document.getElementById('manual-feed-appearance');
    if (appearSelect) {
        const appearLabels = {
            te: {
                'Normal': 'సాధారణ సమతుల్య రంగు',
                'Fungus/Mould Patches': 'బూజు ముద్దలు లేదా మచ్చలు',
                'White Powder/Granules': 'తెల్ల పొడి లేదా స్ఫటిక గుళికలు',
                'Inclusions/Debris': 'రాళ్ళు, పురుగులు లేదా కలుషితాలు'
            },
            hi: {
                'Normal': 'सामान्य एकसमान रंग',
                'Fungus/Mould Patches': 'सफेद या काले फफूंद के धब्बे',
                'White Powder/Granules': 'सफेद पाउडर या दानेदार कण',
                'Inclusions/Debris': 'कंकड़, कीड़े या मिलावटी कचरा'
            },
            en: {
                'Normal': 'Normal Uniform Color',
                'Fungus/Mould Patches': 'White / Dark Mould Patches',
                'White Powder/Granules': 'White Powder / Crystalline Granules',
                'Inclusions/Debris': 'Stones / Grit / Foreign Debris'
            }
        };
        const active = appearLabels[lang] || appearLabels.en;
        Array.from(appearSelect.options).forEach(opt => {
            if (active[opt.value]) opt.text = active[opt.value];
        });
    }

    // 9. Manual Cattle Symptoms Select
    const symptomSelect = document.getElementById('manual-cattle-symptom');
    if (symptomSelect) {
        const symLabels = {
            te: {
                'Normal': 'సాధారణంగా చురుగ్గా ఉంది',
                'Sudden Milk Drop': 'పాల దిగుబడి అకస్మాత్తుగా తగ్గింది',
                'Refusing to Eat': 'మేత తినడం మానేసింది',
                'Loose Dung/Diarrhea': 'విరేచనాలు లేదా పారుడు రోగం',
                'Bloat/Indigestion': 'కడుపు ఉబ్బరం లేదా అజీర్తి',
                'Lethargy/Weakness': 'నీరసం లేదా నడవలేకపోవడం'
            },
            hi: {
                'Normal': 'सामान्य व सक्रिय',
                'Sudden Milk Drop': 'दूध उत्पादन में अचानक गिरावट',
                'Refusing to Eat': 'चारा खाने से इनकार',
                'Loose Dung/Diarrhea': 'दस्त या पतला गोबर',
                'Bloat/Indigestion': 'पेट फूलना या अपच',
                'Lethargy/Weakness': 'सुस्ती या कमजोरी'
            },
            en: {
                'Normal': 'Normal / Alert',
                'Sudden Milk Drop': 'Sudden Milk Yield Drop',
                'Refusing to Eat': 'Refusing to Eat Feed',
                'Loose Dung/Diarrhea': 'Loose Dung / Diarrhea',
                'Bloat/Indigestion': 'Bloat / Indigestion',
                'Lethargy/Weakness': 'Lethargy / Weakness'
            }
        };
        const active = symLabels[lang] || symLabels.en;
        Array.from(symptomSelect.options).forEach(opt => {
            if (active[opt.value]) opt.text = active[opt.value];
        });
    }
}

// ===================================================================
// User Authentication & Role-Based Flow (Farmer vs Admin)
// ===================================================================

// ===================================================================
// 🌟 Dedicated Full-Screen Onboarding & Authentication Engine
// Screen 1: Splash Screen (Logo + "START THE APP")
// Screen 2: Language Selection (Logo + Telugu / Hindi / English + "Next →")
// Screen 3: Authentication Gate (Logo + Sign In & Register)
// ===================================================================

async function startTheAppDirectly(chosenLang) {
    if (chosenLang) {
        selectSplashLang(chosenLang);
    }

    // 1. If a user session is already stored, unlock with it
    let savedUser = null;
    try {
        const stored = localStorage.getItem('smartfeed_user');
        if (stored) savedUser = JSON.parse(stored);
    } catch (e) {}

    if (savedUser && savedUser.id) {
        if (chosenLang) savedUser.preferred_language = chosenLang;
        unlockAppWorkspace(savedUser);
        return;
    }

    // 2. Otherwise log in as Demo Farmer
    try {
        const resp = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mobile: '9876543210', password: 'farmer123' })
        });
        if (resp.ok) {
            const data = await resp.json();
            if (data && data.user) {
                if (chosenLang) data.user.preferred_language = chosenLang;
                unlockAppWorkspace(data.user);
                return;
            }
        }
    } catch (err) {
        console.warn('Direct entry network fallback:', err);
    }

    // 3. Fallback guest farmer profile (100% offline ready)
    const fallbackUser = {
        id: 'farmer_demo_1',
        mobile: '9876543210',
        full_name: (state.language === 'te' ? 'రమేష్ పటేల్ (రైతు)' : (state.language === 'hi' ? 'रमेश पटेल (किसान)' : 'Ramesh Patel (Demo Farmer)')),
        role: 'farmer',
        preferred_language: state.language || 'te',
        is_onboarded: true
    };
    unlockAppWorkspace(fallbackUser);
}

function selectSplashLang(lang) {
    ['te', 'hi', 'en'].forEach(l => {
        const btn = document.getElementById(`splash-lang-${l}`);
        if (btn) {
            if (l === lang) {
                btn.classList.add('active');
                btn.style.border = '1.5px solid #10B981';
                btn.style.background = 'rgba(16, 185, 129, 0.18)';
                btn.style.color = '#047857';
            } else {
                btn.classList.remove('active');
                btn.style.border = '1.5px solid #CBD5E1';
                btn.style.background = '#ffffff';
                btn.style.color = '#475569';
            }
        }
    });
    selectEntryLanguage(lang);
}

function goToEntryScreen(screenId) {
    const screens = ['splash', 'language', 'auth'];
    screens.forEach(s => {
        const el = document.getElementById(`entry-screen-${s}`);
        if (el) el.style.display = (s === screenId) ? 'block' : 'none';
    });
    if (screenId === 'auth') {
        const entryMobile = document.getElementById('entry-login-mobile');
        const entryPwd = document.getElementById('entry-login-password');
        if (entryMobile) entryMobile.value = '';
        if (entryPwd) entryPwd.value = '';
        clearEntryAuthError();
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function selectEntryLanguage(lang) {
    ['te', 'hi', 'en'].forEach(l => {
        const card = document.getElementById(`lang-card-${l}`);
        if (card) {
            if (l === lang) card.classList.add('active');
            else card.classList.remove('active');
        }
    });
    setLanguage(lang);
}

function switchEntryAuthTab(tab) {
    const btnLogin = document.getElementById('entry-tab-login');
    const btnReg = document.getElementById('entry-tab-register');
    const formLogin = document.getElementById('entry-form-login');
    const formReg = document.getElementById('entry-form-register');
    const heading = document.getElementById('entry-auth-heading');
    const subheading = document.getElementById('entry-auth-subheading');

    if (tab === 'login') {
        if (btnLogin) btnLogin.classList.add('active');
        if (btnReg) btnReg.classList.remove('active');
        if (formLogin) formLogin.style.display = 'block';
        if (formReg) formReg.style.display = 'none';
        if (heading) heading.innerText = state.language === 'te' ? 'రైతు / అడ్మిన్ లాగిన్' : (state.language === 'hi' ? 'किसान / व्यवस्थापक लॉगिन' : 'Sign In to SmartFeed AI');
        if (subheading) subheading.innerText = state.language === 'te' ? 'మీ మొబైల్ మరియు పాస్‌వర్డ్‌తో లాగిన్ అవ్వండి' : 'Enter your mobile number and password';
    } else {
        if (btnLogin) btnLogin.classList.remove('active');
        if (btnReg) btnReg.classList.add('active');
        if (formLogin) formLogin.style.display = 'none';
        if (formReg) formReg.style.display = 'block';
        if (heading) heading.innerText = state.language === 'te' ? 'కొత్త రైతు ఖాతా నమోదు' : (state.language === 'hi' ? 'नया किसान पंजीकरण' : 'Create Farmer Account');
        if (subheading) subheading.innerText = state.language === 'te' ? 'మీ వివరాలు నమోదు చేసి పశువుల ప్రొఫైల్ సెటప్ చేయండి' : 'Register your details to set up your cattle profile';
    }
    clearEntryAuthError();
}

function showEntryAuthError(msg, isNotice = false) {
    const box = document.getElementById('entry-auth-error-box');
    const modalBox = document.getElementById('auth-error-box');
    [box, modalBox].forEach(b => {
        if (!b) return;
        b.style.display = 'block';
        if (isNotice) {
            b.style.background = '#EFF6FF';
            b.style.borderColor = '#93C5FD';
            b.style.color = '#1E40AF';
        } else {
            b.style.background = '#FEF2F2';
            b.style.borderColor = '#FCA5A5';
            b.style.color = '#991B1B';
        }
        b.innerText = msg;
    });
}

function clearEntryAuthError() {
    const box = document.getElementById('entry-auth-error-box');
    const modalBox = document.getElementById('auth-error-box');
    if (box) {
        box.style.display = 'none';
        box.innerText = '';
    }
    if (modalBox) {
        modalBox.style.display = 'none';
        modalBox.innerText = '';
    }
}

function unlockAppWorkspace(user) {
    state.currentUser = user;
    try {
        sessionStorage.setItem('smartfeed_session_active', '1');
        localStorage.setItem('smartfeed_user', JSON.stringify(user));
    } catch (e) {}

    const entryStage = document.getElementById('app-entry-stage');
    const appContainer = document.getElementById('main-app-container');

    if (entryStage) entryStage.style.display = 'none';
    if (appContainer) appContainer.style.display = 'flex';

    updateUserSessionUI();

    if (user.role === 'admin') {
        showHomeView('admin');
        switchAdminTab('overview');
        loadAdminPortalData();
    } else {
        // Farmer
        showHomeView('farmer');
        if (!user.is_onboarded) {
            startFarmSetupWizard(false);
        } else {
            loadFarmerDashboardData();
        }
    }
    switchTab('home');
    loadDashboardData();
}

function lockAppWorkspace() {
    state.currentUser = null;
    state.farmerProfile = null;
    state.farmerAnimals = [];
    try {
        sessionStorage.removeItem('smartfeed_session_active');
        localStorage.removeItem('smartfeed_user');
    } catch (e) {}

    // Reset all auth input fields so no credentials remain visible
    const idsToClear = ['entry-login-mobile', 'entry-login-password', 'login-mobile', 'login-password'];
    idsToClear.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = '';
    });
    clearEntryAuthError();

    const entryStage = document.getElementById('app-entry-stage');
    const appContainer = document.getElementById('main-app-container');

    if (appContainer) appContainer.style.display = 'none';
    if (entryStage) entryStage.style.display = 'flex';

    goToEntryScreen('splash');
}

async function handleEntryLoginSubmit(e) {
    if (e) e.preventDefault();
    clearEntryAuthError();
    const mobile = (
        (document.getElementById('entry-login-mobile') && document.getElementById('entry-login-mobile').value.trim()) ||
        (document.getElementById('login-mobile') && document.getElementById('login-mobile').value.trim()) ||
        ''
    );
    const password = (
        (document.getElementById('entry-login-password') && document.getElementById('entry-login-password').value.trim()) ||
        (document.getElementById('login-password') && document.getElementById('login-password').value.trim()) ||
        ''
    );

    if (!mobile || !password) {
        const emptyMsg = (state.language === 'te')
            ? 'దయచేసి మొబైల్ నంబర్ మరియు పాస్‌వర్డ్ రెండూ నమోదు చేయండి.'
            : (state.language === 'hi'
                ? 'कृपया मोबाइल नंबर और पासवर्ड दोनों दर्ज करें।'
                : 'Please enter both mobile number and password.');
        showEntryAuthError(emptyMsg, false);
        return;
    }

    try {
        const resp = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mobile, password })
        });
        const data = await resp.json();
        if (!resp.ok) {
            const failMsg = data.detail || ((state.language === 'te')
                ? 'లాగిన్ విఫలమైంది. దయచేసి సరైన మొబైల్ మరియు పాస్‌వర్డ్ నమోదు చేయండి.'
                : (state.language === 'hi'
                    ? 'लॉगिन विफल। कृपया सही मोबाइल और पासवर्ड दर्ज करें।'
                    : 'Login failed. Please check mobile and password.'));
            throw new Error(failMsg);
        }

        const storedLang = localStorage.getItem('smartfeed_lang');
        const targetLang = storedLang || data.user.preferred_language || state.language || 'en';
        setLanguage(targetLang);

        closeAuthModal();
        unlockAppWorkspace(data.user);
    } catch (err) {
        showEntryAuthError(err.message, false);
    }
}

async function handleEntryRegisterSubmit(e) {
    if (e) e.preventDefault();
    clearEntryAuthError();
    const fullName = document.getElementById('entry-reg-fullname').value.trim();
    const mobile = document.getElementById('entry-reg-mobile').value.trim();
    const email = document.getElementById('entry-reg-email').value.trim();
    const password = document.getElementById('entry-reg-password').value.trim();
    const confirmPw = document.getElementById('entry-reg-confirm-password').value.trim();
    const langRadios = document.getElementsByName('entry-reg-lang');
    let lang = 'te';
    for (const r of langRadios) {
        if (r.checked) { lang = r.value; break; }
    }

    if (!fullName || !mobile || !password) {
        showEntryAuthError('Full Name, Mobile Number, and Password are required.');
        return;
    }
    if (password !== confirmPw) {
        showEntryAuthError('Passwords do not match. Please re-enter.');
        return;
    }

    try {
        const resp = await fetch('/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                full_name: fullName,
                mobile,
                email,
                password,
                preferred_language: lang,
                role: 'farmer'
            })
        });
        const data = await resp.json();
        if (!resp.ok) {
            throw new Error(data.detail || 'Registration failed.');
        }

        if (lang !== state.language) {
            setLanguage(lang);
        }

        unlockAppWorkspace(data.user);
    } catch (err) {
        showEntryAuthError(err.message);
    }
}

function prefillAdminLogin() {
    clearEntryAuthError();
    switchEntryAuthTab('login');
    switchAuthTab('login');

    const entryMobile = document.getElementById('entry-login-mobile');
    const entryPwd = document.getElementById('entry-login-password');
    if (entryMobile) {
        entryMobile.value = '';
        entryMobile.focus();
    }
    if (entryPwd) {
        entryPwd.value = '';
    }

    const modalMobile = document.getElementById('login-mobile');
    const modalPwd = document.getElementById('login-password');
    if (modalMobile) {
        modalMobile.value = '';
        modalMobile.focus();
    }
    if (modalPwd) {
        modalPwd.value = '';
    }
}

function quickLoginDemoAdmin() {
    prefillAdminLogin();
}

function quickLoginDemoFarmer() {
    clearEntryAuthError();
    switchEntryAuthTab('login');
    switchAuthTab('login');
    const msg = (state.language === 'te')
        ? 'దయచేసి మీ రిజిస్టర్డ్ మొబైల్ నంబర్ మరియు పాస్‌వర్డ్ నమోదు చేయండి లేదా కొత్త ఖాతా తెరవండి.'
        : 'Please enter your registered mobile and password or register a new account.';
    showEntryAuthError(msg, true);
}

function quickLoginGuest() {
    clearEntryAuthError();
    const guestUser = {
        id: 'farmer_guest_1',
        mobile: '9876543210',
        full_name: (state.language === 'te' ? 'అతిథి రైతు (Guest Farmer)' : (state.language === 'hi' ? 'अतिथि किसान (Guest Farmer)' : 'Guest Farmer')),
        role: 'farmer',
        preferred_language: state.language || 'te',
        is_onboarded: true
    };
    unlockAppWorkspace(guestUser);
}

function logoutUser() {
    lockAppWorkspace();
    goToEntryScreen('auth');
}

function updateUserSessionUI() {
    const bar = document.getElementById('user-session-bar');
    if (!bar) return;

    if (!state.currentUser) {
        bar.innerHTML = `
            <button class="btn-auth-trigger" onclick="lockAppWorkspace()">
                <span>👤</span>
                <span>${state.language === 'te' ? 'లాగిన్ / నమోదు' : (state.language === 'hi' ? 'लॉग इन / रजिस्टर' : 'Sign In / Register')}</span>
            </button>
        `;
        return;
    }

    const u = state.currentUser;
    if (u.role === 'admin') {
        bar.innerHTML = `
            <div class="user-profile-badge admin-profile-badge" style="background: linear-gradient(135deg, #1E3A8A, #1D4ED8); color: #FFF; border: 1.5px solid #60A5FA;">
                <div class="user-profile-avatar" style="background: #F59E0B; color: #FFF; font-size: 1.2rem;">🛡️</div>
                <div class="user-profile-info">
                    <div class="user-profile-name" style="color: #FFF; font-weight: 800;">${u.full_name || 'Cooperative Admin'}</div>
                    <div class="user-profile-meta" style="color: #BFDBFE;">👑 District Union Officer (8341016049)</div>
                </div>
            </div>
            <button class="btn-header-action btn-header-logout" onclick="logoutUser()" title="Logout" style="background: #DC2626; color: #FFF; border: none;">
                <span>🚪</span>
                <span>Sign Out</span>
            </button>
        `;
        applyAdminSidebar(true);
    } else {
        // Farmer
        const villageText = state.farmerProfile ? (state.farmerProfile.village_location || '') : '';
        bar.innerHTML = `
            <div class="user-profile-badge" onclick="startFarmSetupWizard(true)" style="cursor: pointer;" title="Click to view/edit farm setup">
                <div class="user-profile-avatar">🌾</div>
                <div class="user-profile-info">
                    <div class="user-profile-name">${u.full_name || 'Farmer'}</div>
                    <div class="user-profile-meta">${villageText ? '📍 ' + villageText : 'Dairy Farmer'}</div>
                </div>
            </div>
            <button class="btn-header-action" onclick="startFarmSetupWizard(true)" title="Edit Farm Setup">
                <span>⚙️</span>
            </button>
            <button class="btn-header-action btn-header-logout" onclick="logoutUser()" title="Logout">
                <span>🚪</span>
            </button>
        `;
        applyAdminSidebar(false);
    }
}

function renderSidebarNav(role) {
    const menu = document.getElementById('app-nav-menu');
    if (!menu) return;
    const lang = state.language || 'te';

    const elSlogan = document.getElementById('sidebar-brand-slogan');
    const elStatus = document.getElementById('sidebar-status-text');

    if (role === 'admin') {
        if (elSlogan) elSlogan.innerText = 'COOPERATIVE COMMAND & AUDIT';
        if (elStatus) elStatus.innerText = 'DISTRICT SURVEILLANCE • AUDIT ACTIVE';

        const adminLabels = {
            overview: { te: 'సహకార సమాఖ్య ఓవర్‌వ్యూ', en: 'Cooperative Overview', hi: 'सहकारी समग्र रिपोर्ट' },
            farmers: { te: 'పాల రైతుల జాబితా', en: 'Farmer Master Registry', hi: 'किसान मास्टर रजिस्ट्री' },
            batches: { te: 'ఫీడ్ నాణ్యత ఆడిట్ లాగ్', en: 'Batch Quality Audit', hi: 'फ़ीड गुणवत्ता ऑडिट' },
            surveillance: { te: 'గ్రామ సర్వైలెన్స్ నిఘా', en: 'Village Surveillance', hi: 'ग्राम निगरानी मैट्रिक्स' },
            broadcast: { te: 'అత్యవసర ప్రకటనల జారీ', en: 'Broadcast Advisories', hi: 'आपातकालीन प्रसारण' },
            standards: { te: 'BIS IS:2052 ప్రమాణాలు', en: 'BIS Standards', hi: 'बीआईएस मानक' }
        };

        const currentActive = state.currentAdminTab || 'overview';

        menu.innerHTML = `
            <li class="nav-item ${currentActive === 'overview' ? 'active' : ''}" data-admin-tab="overview" onclick="switchAdminSubView('overview')">
                <span class="nav-icon">🏛️</span>
                <span id="nav-admin-overview">${adminLabels.overview[lang] || adminLabels.overview.en}</span>
            </li>
            <li class="nav-item ${currentActive === 'farmers' ? 'active' : ''}" data-admin-tab="farmers" onclick="switchAdminSubView('farmers')">
                <span class="nav-icon">👥</span>
                <span id="nav-admin-farmers">${adminLabels.farmers[lang] || adminLabels.farmers.en}</span>
            </li>
            <li class="nav-item ${currentActive === 'batches' ? 'active' : ''}" data-admin-tab="batches" onclick="switchAdminSubView('batches')">
                <span class="nav-icon">🔬</span>
                <span id="nav-admin-batches">${adminLabels.batches[lang] || adminLabels.batches.en}</span>
            </li>
            <li class="nav-item ${currentActive === 'surveillance' ? 'active' : ''}" data-admin-tab="surveillance" onclick="switchAdminSubView('surveillance')">
                <span class="nav-icon">🗺️</span>
                <span id="nav-admin-surveillance">${adminLabels.surveillance[lang] || adminLabels.surveillance.en}</span>
            </li>
            <li class="nav-item ${currentActive === 'broadcast' ? 'active' : ''}" data-admin-tab="broadcast" onclick="switchAdminSubView('broadcast')">
                <span class="nav-icon">📢</span>
                <span id="nav-admin-broadcast">${adminLabels.broadcast[lang] || adminLabels.broadcast.en}</span>
            </li>
            <li class="nav-item ${currentActive === 'standards' ? 'active' : ''}" data-admin-tab="standards" onclick="switchAdminSubView('standards')">
                <span class="nav-icon">⚖️</span>
                <span id="nav-admin-standards">${adminLabels.standards[lang] || adminLabels.standards.en}</span>
            </li>
        `;
    } else {
        if (elSlogan) elSlogan.innerText = 'FEED SMART • FARM BETTER';
        if (elStatus) elStatus.innerText = 'OFFLINE READY • LOCAL AI ACTIVE';

        const farmerLabels = {
            home: { te: 'హోమ్ (నా ఫారం)', en: 'Home', hi: 'होम (मेरा फार्म)' },
            scanner: { te: 'నాణ్యత స్కానర్', en: 'Quality Scanner', hi: 'गुणवत्ता स्कैनर' },
            adulteration: { te: 'కల్తీ నిరోధక పరీక్ష', en: 'Adulteration Check', hi: 'मिलावट जांच' },
            advisory: { te: 'AI పశువైద్య సలహా', en: 'AI Advisory', hi: 'एआई परामर्श' },
            dashboard: { te: 'విశ్లేషణలు', en: 'Dashboard', hi: 'डैशबोर्ड' },
            passport: { te: 'ఫీడ్ పాస్‌పోర్ట్', en: 'Feed Passport', hi: 'फ़ीड पासपोर्ट' },
            lookup: { te: 'బ్యాచ్ పరిశీలన', en: 'Batch Lookup', hi: 'बैच खोज' }
        };

        const currentActive = state.currentTab || 'home';

        menu.innerHTML = `
            <li class="nav-item ${currentActive === 'home' ? 'active' : ''}" data-tab="home" onclick="switchTab('home')">
                <span class="nav-icon">🏠</span>
                <span id="nav-home">${farmerLabels.home[lang] || farmerLabels.home.en}</span>
            </li>
            <li class="nav-item ${currentActive === 'scanner' ? 'active' : ''}" data-tab="scanner" onclick="switchTab('scanner')">
                <span class="nav-icon">📸</span>
                <span id="nav-scanner">${farmerLabels.scanner[lang] || farmerLabels.scanner.en}</span>
            </li>
            <li class="nav-item ${currentActive === 'adulteration' ? 'active' : ''}" data-tab="adulteration" onclick="switchTab('adulteration')">
                <span class="nav-icon">⚠️</span>
                <span id="nav-adulteration">${farmerLabels.adulteration[lang] || farmerLabels.adulteration.en}</span>
            </li>
            <li class="nav-item ${currentActive === 'advisory' ? 'active' : ''}" data-tab="advisory" onclick="switchTab('advisory')">
                <span class="nav-icon">🤖</span>
                <span id="nav-advisory">${farmerLabels.advisory[lang] || farmerLabels.advisory.en}</span>
            </li>
            <li class="nav-item ${currentActive === 'dashboard' ? 'active' : ''}" data-tab="dashboard" onclick="switchTab('dashboard')">
                <span class="nav-icon">📊</span>
                <span id="nav-dashboard">${farmerLabels.dashboard[lang] || farmerLabels.dashboard.en}</span>
            </li>
            <li class="nav-item ${currentActive === 'passport' ? 'active' : ''}" data-tab="passport" onclick="switchTab('passport')">
                <span class="nav-icon">📦</span>
                <span id="nav-passport">${farmerLabels.passport[lang] || farmerLabels.passport.en}</span>
            </li>
            <li class="nav-item ${currentActive === 'lookup' ? 'active' : ''}" data-tab="lookup" onclick="switchTab('lookup')">
                <span class="nav-icon">🔎</span>
                <span id="nav-lookup">${farmerLabels.lookup[lang] || farmerLabels.lookup.en}</span>
            </li>
        `;
    }
}

function switchAdminSubView(tabKey) {
    state.currentAdminTab = tabKey;
    switchTab('home');
    switchAdminTab(tabKey);
}

function applyAdminSidebar(isAdmin) {
    renderSidebarNav(isAdmin ? 'admin' : 'farmer');
}

function showHomeView(viewName) {
    const guestView = document.getElementById('guest-home-view');
    const farmerView = document.getElementById('farmer-dashboard-view');
    const adminView = document.getElementById('admin-dashboard-view');

    if (guestView) guestView.style.display = (viewName === 'guest') ? 'block' : 'none';
    if (farmerView) farmerView.style.display = (viewName === 'farmer') ? 'block' : 'none';
    if (adminView) adminView.style.display = (viewName === 'admin') ? 'block' : 'none';
}

function openAuthModal(tab = 'login') {
    // Redirect to Screen 3 of app-entry-stage
    lockAppWorkspace();
    goToEntryScreen('auth');
    switchEntryAuthTab(tab);
}

function closeAuthModal() {
    // If not logged in, go back to splash
    if (!state.currentUser) {
        goToEntryScreen('splash');
    }
}

function switchAuthTab(tab) {
    switchEntryAuthTab(tab);
}

function handleLoginSubmit(e) {
    handleEntryLoginSubmit(e);
}

function handleRegisterSubmit(e) {
    handleEntryRegisterSubmit(e);
}

// ===================================================================
// 4-Step Interactive Farm Setup Wizard
// Step 1: Farm Basic Details (Farmer Name, Village, Language)
// Step 2: How Many Animals? (Stepper - 3 +, Cow / Buffalo checkboxes)
// Step 3: Individual Animal Profiles (Dynamic cards, conditional milk production logic)
// Step 4: Feed & Storage Details (Main feed, storage facility)
// ===================================================================

function startFarmSetupWizard(isEdit = false) {
    const modal = document.getElementById('onboarding-wizard-modal');
    if (!modal) return;
    modal.style.display = 'flex';

    // Populate existing values if available
    const u = state.currentUser || {};
    const p = state.farmerProfile || {};
    const f = p.farm || {};

    const nameInput = document.getElementById('wz-farmer-name');
    const villageInput = document.getElementById('wz-village');

    if (nameInput) nameInput.value = f.farmer_name || u.full_name || '';
    if (villageInput) villageInput.value = f.village_location || '';

    // Language radio
    const langRadios = document.getElementsByName('wz-lang');
    const curLang = f.preferred_language || u.preferred_language || state.language;
    for (const r of langRadios) {
        r.checked = (r.value === curLang);
    }

    // Animal count & types
    state.wizardData.animalCount = f.total_animals || (state.farmerAnimals.length || 3);
    const countEl = document.getElementById('wizard-animals-count');
    if (countEl) countEl.innerText = state.wizardData.animalCount;

    const typesStr = f.animal_types || 'Cow,Buffalo';
    const cowBox = document.getElementById('wz-type-cow');
    const buffBox = document.getElementById('wz-type-buffalo');
    if (cowBox) cowBox.checked = typesStr.includes('Cow');
    if (buffBox) buffBox.checked = typesStr.includes('Buffalo');

    // Main feed & storage radios
    const mainFeed = f.main_feed_type || 'Green Fodder';
    const storage = f.feed_storage || 'Shed';
    const feedRadios = document.getElementsByName('wz-main-feed');
    for (const r of feedRadios) { r.checked = (r.value === mainFeed); }
    const storRadios = document.getElementsByName('wz-storage');
    for (const r of storRadios) { r.checked = (r.value === storage); }

    proceedToWizardStep(1);
}

function closeWizardModal() {
    const modal = document.getElementById('onboarding-wizard-modal');
    if (modal) modal.style.display = 'none';
}

function proceedToWizardStep(stepNum) {
    state.wizardData.step = stepNum;

    // Step 1 validation
    if (stepNum > 1) {
        const name = document.getElementById('wz-farmer-name').value.trim();
        const village = document.getElementById('wz-village').value.trim();
        if (!name || !village) {
            showWizardError('Please enter Farmer Name and Village / Location before proceeding.');
            return;
        }
        clearWizardError();
    }

    // Step 2 validation
    if (stepNum > 2) {
        const cowChecked = document.getElementById('wz-type-cow').checked;
        const buffChecked = document.getElementById('wz-type-buffalo').checked;
        if (!cowChecked && !buffChecked) {
            showWizardError('Please select at least one animal type (Cow or Buffalo).');
            return;
        }
        if (state.wizardData.animalCount < 1) {
            showWizardError('Please select at least 1 animal.');
            return;
        }
        clearWizardError();
        generateAnimalCardsForStep3();
    }

    // Step 3 validation
    if (stepNum > 3) {
        clearWizardError();
    }

    // Update Progress Bar
    for (let i = 1; i <= 4; i++) {
        const node = document.getElementById(`wizard-node-${i}`);
        const content = document.getElementById(`wizard-step-${i}`);
        if (node) {
            node.classList.remove('active', 'completed');
            if (i === stepNum) node.classList.add('active');
            else if (i < stepNum) node.classList.add('completed');
        }
        if (content) {
            content.style.display = (i === stepNum) ? 'block' : 'none';
        }
    }
}

function showWizardError(msg) {
    const box = document.getElementById('wizard-error-box');
    if (!box) return;
    box.style.display = 'block';
    box.innerText = msg;
}

function clearWizardError() {
    const box = document.getElementById('wizard-error-box');
    if (box) box.style.display = 'none';
}

function incrementAnimalCount() {
    if (state.wizardData.animalCount < 20) {
        state.wizardData.animalCount++;
        document.getElementById('wizard-animals-count').innerText = state.wizardData.animalCount;
    }
}

function decrementAnimalCount() {
    if (state.wizardData.animalCount > 1) {
        state.wizardData.animalCount--;
        document.getElementById('wizard-animals-count').innerText = state.wizardData.animalCount;
    }
}

function validateAnimalTypes() {
    const cowChecked = document.getElementById('wz-type-cow').checked;
    const buffChecked = document.getElementById('wz-type-buffalo').checked;
    if (!cowChecked && !buffChecked) {
        showWizardError('Select at least one animal type.');
    } else {
        clearWizardError();
    }
}

function generateAnimalCardsForStep3() {
    const container = document.getElementById('wizard-animal-cards-container');
    if (!container) return;

    const count = state.wizardData.animalCount;
    const cowChecked = document.getElementById('wz-type-cow').checked;
    const buffChecked = document.getElementById('wz-type-buffalo').checked;

    let availableTypes = [];
    if (cowChecked) availableTypes.push('Cow');
    if (buffChecked) availableTypes.push('Buffalo');
    if (availableTypes.length === 0) availableTypes = ['Cow'];

    container.innerHTML = '';

    const existingAnimals = state.farmerAnimals || [];

    for (let i = 1; i <= count; i++) {
        const existing = existingAnimals[i - 1] || {};
        const defaultType = existing.animal_type || availableTypes[(i - 1) % availableTypes.length];
        const defaultAge = existing.age_group || '3–5 years';
        const defaultStatus = existing.lactation_status || ((i % 3 === 0) ? 'Pregnant' : 'Lactating');
        const defaultMilk = existing.milk_production || 'Medium (5–10 L)';
        const defaultName = existing.animal_name || `${defaultType} #${i}`;

        const isLactating = (defaultStatus === 'Lactating');

        const card = document.createElement('div');
        card.className = 'animal-profile-card';
        card.id = `animal-card-${i}`;

        const curLang = state.language || 'en';
        const cardI18n = {
            lblType: curLang === 'te' ? 'పశువు రకం' : (curLang === 'hi' ? 'पशु का प्रकार' : 'Animal Type'),
            lblAge: curLang === 'te' ? 'వయస్సు గ్రూప్' : (curLang === 'hi' ? 'आयु वर्ग' : 'Age Group'),
            lblStatus: curLang === 'te' ? 'శారీరక స్థితి' : (curLang === 'hi' ? 'शारीरिक अवस्था' : 'Status'),
            lblMilk: curLang === 'te' ? '🥛 రోజువారీ పాల దిగుబడి' : (curLang === 'hi' ? '🥛 दैनिक दूध उत्पादन' : '🥛 Daily Milk Yield'),
            cowTxt: curLang === 'te' ? '🐄 ఆవు' : (curLang === 'hi' ? '🐄 गाय' : '🐄 Cow'),
            buffTxt: curLang === 'te' ? '🐃 గేదె' : (curLang === 'hi' ? '🐃 भैंस' : '🐃 Buffalo'),
            age1: curLang === 'te' ? '< 1 సంవత్సరం (దూడ)' : (curLang === 'hi' ? '< 1 वर्ष (बछड़ा)' : '< 1 year (Calf)'),
            age13: curLang === 'te' ? '1–3 సంవత్సరాలు (పెయ్య)' : (curLang === 'hi' ? '1–3 वर्ष' : '1–3 years'),
            age35: curLang === 'te' ? '3–5 సంవత్సరాలు (యుక్తవయస్సు)' : (curLang === 'hi' ? '3–5 वर्ष' : '3–5 years'),
            age5: curLang === 'te' ? '5+ సంవత్సరాలు (వృద్ధ)' : (curLang === 'hi' ? '5+ वर्ष' : '5+ years'),
            statLact: curLang === 'te' ? '🥛 పాలిచ్చేది' : (curLang === 'hi' ? '🥛 दुधारू' : '🥛 Lactating'),
            statPreg: curLang === 'te' ? '🤰 చూడి' : (curLang === 'hi' ? '🤰 गर्भवती' : '🤰 Pregnant'),
            statDry: curLang === 'te' ? '🍂 ఎండినది' : (curLang === 'hi' ? '🍂 सूखी' : '🍂 Dry'),
            statCalf: curLang === 'te' ? '🌱 దూడ / పెయ్య' : (curLang === 'hi' ? '🌱 बछड़ा / बछिया' : '🌱 Heifer / Calf'),
            milkLow: curLang === 'te' ? 'తక్కువ (< 5 L / రోజు)' : (curLang === 'hi' ? 'कम (< 5 L / दिन)' : 'Low (< 5 L / day)'),
            milkMed: curLang === 'te' ? 'మధ్యస్థం (5–10 L / రోజు)' : (curLang === 'hi' ? 'मध्यम (5–10 L / दिन)' : 'Medium (5–10 L / day)'),
            milkHigh: curLang === 'te' ? 'ఎక్కువ (> 10 L / రోజు)' : (curLang === 'hi' ? 'अधिक (> 10 L / दिन)' : 'High (> 10 L / day)'),
            naNote: curLang === 'te' ? 'చూడి / పాలివ్వని పశువు — పాల ఉత్పత్తి అవసరం లేదు (N/A)' : (curLang === 'hi' ? 'गर्भवती / सूखी — दूध उत्पादन आवश्यक नहीं (N/A)' : 'Non-lactating / Pregnant — Milk production not required (N/A)')
        };

        card.innerHTML = `
            <div class="animal-card-top">
                <span class="animal-card-tag">
                    <span id="anim-icon-${i}">${defaultType === 'Cow' ? '🐄' : '🐃'}</span>
                    <span>Animal #${i}</span>
                </span>
                <input type="text" id="anim-name-${i}" class="form-input" style="width: auto; max-width: 180px; padding: 4px 8px; font-size: 0.85rem;" value="${defaultName}" placeholder="Tag / Name">
            </div>
            <div class="animal-card-form-grid">
                <div>
                    <label class="form-label" style="font-size: 0.78rem;">${cardI18n.lblType}</label>
                    <select id="anim-type-${i}" class="styled-select" style="margin-bottom: 0; padding: 6px 10px; font-size: 0.85rem;" onchange="onAnimalTypeChange(${i})">
                        ${availableTypes.map(t => `<option value="${t}" ${t === defaultType ? 'selected' : ''}>${t === 'Cow' ? cardI18n.cowTxt : cardI18n.buffTxt}</option>`).join('')}
                    </select>
                </div>
                <div>
                    <label class="form-label" style="font-size: 0.78rem;">${cardI18n.lblAge}</label>
                    <select id="anim-age-${i}" class="styled-select" style="margin-bottom: 0; padding: 6px 10px; font-size: 0.85rem;">
                        <option value="<1 yr" ${defaultAge.includes('<1') ? 'selected' : ''}>${cardI18n.age1}</option>
                        <option value="1–3 years" ${defaultAge.includes('1–3') || defaultAge.includes('1-3') ? 'selected' : ''}>${cardI18n.age13}</option>
                        <option value="3–5 years" ${defaultAge.includes('3–5') || defaultAge.includes('3-5') ? 'selected' : ''}>${cardI18n.age35}</option>
                        <option value="5+ years" ${defaultAge.includes('5+') ? 'selected' : ''}>${cardI18n.age5}</option>
                    </select>
                </div>
                <div>
                    <label class="form-label" style="font-size: 0.78rem;">${cardI18n.lblStatus}</label>
                    <select id="anim-status-${i}" class="styled-select" style="margin-bottom: 0; padding: 6px 10px; font-size: 0.85rem;" onchange="onAnimalStatusChange(${i})">
                        <option value="Lactating" ${defaultStatus === 'Lactating' ? 'selected' : ''}>${cardI18n.statLact}</option>
                        <option value="Pregnant" ${defaultStatus === 'Pregnant' ? 'selected' : ''}>${cardI18n.statPreg}</option>
                        <option value="Dry" ${defaultStatus === 'Dry' ? 'selected' : ''}>${cardI18n.statDry}</option>
                        <option value="Heifer / Calf" ${defaultStatus.includes('Calf') || defaultStatus.includes('Heifer') ? 'selected' : ''}>${cardI18n.statCalf}</option>
                    </select>
                </div>

                <!-- Conditional Milk Production Box -->
                <div id="anim-milk-box-${i}" class="conditional-milk-box ${isLactating ? '' : 'non-lactating'}">
                    <div id="anim-milk-select-wrap-${i}" style="display: ${isLactating ? 'block' : 'none'};">
                        <label class="form-label" style="font-size: 0.78rem; color: #047857;">${cardI18n.lblMilk}</label>
                        <select id="anim-milk-${i}" class="styled-select" style="margin-bottom: 0; padding: 6px 10px; font-size: 0.85rem;">
                            <option value="Low (<5 L)" ${defaultMilk.includes('<5') ? 'selected' : ''}>${cardI18n.milkLow}</option>
                            <option value="Medium (5–10 L)" ${defaultMilk.includes('5–10') || defaultMilk.includes('5-10') ? 'selected' : ''}>${cardI18n.milkMed}</option>
                            <option value="High (>10 L)" ${defaultMilk.includes('>10') ? 'selected' : ''}>${cardI18n.milkHigh}</option>
                        </select>
                    </div>
                    <div id="anim-milk-na-badge-${i}" style="display: ${isLactating ? 'none' : 'flex'}; align-items: center; gap: 8px; color: #1E40AF; font-size: 0.80rem; font-weight: 700; padding: 4px 0;">
                        <span>ℹ️</span>
                        <span>${cardI18n.naNote}</span>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(card);
    }
}

function onAnimalTypeChange(i) {
    const sel = document.getElementById(`anim-type-${i}`);
    const icon = document.getElementById(`anim-icon-${i}`);
    if (sel && icon) {
        icon.innerText = (sel.value === 'Cow') ? '🐄' : '🐃';
    }
}

function onAnimalStatusChange(i) {
    const statusSel = document.getElementById(`anim-status-${i}`);
    const milkBox = document.getElementById(`anim-milk-box-${i}`);
    const milkWrap = document.getElementById(`anim-milk-select-wrap-${i}`);
    const naBadge = document.getElementById(`anim-milk-na-badge-${i}`);

    if (!statusSel || !milkBox || !milkWrap || !naBadge) return;

    const isLactating = (statusSel.value === 'Lactating');
    if (isLactating) {
        milkBox.classList.remove('non-lactating');
        milkWrap.style.display = 'block';
        naBadge.style.display = 'none';
    } else {
        milkBox.classList.add('non-lactating');
        milkWrap.style.display = 'none';
        naBadge.style.display = 'flex';
    }
}

async function submitFarmOnboarding() {
    clearWizardError();
    if (!state.currentUser) {
        showWizardError('Please sign in first.');
        return;
    }

    const farmerName = document.getElementById('wz-farmer-name').value.trim();
    const village = document.getElementById('wz-village').value.trim();
    const langRadios = document.getElementsByName('wz-lang');
    let lang = 'te';
    for (const r of langRadios) { if (r.checked) { lang = r.value; break; } }

    const count = state.wizardData.animalCount;
    const cowChecked = document.getElementById('wz-type-cow').checked;
    const buffChecked = document.getElementById('wz-type-buffalo').checked;
    let types = [];
    if (cowChecked) types.push('Cow');
    if (buffChecked) types.push('Buffalo');
    if (types.length === 0) types = ['Cow'];

    // Collect animals data
    const animals = [];
    for (let i = 1; i <= count; i++) {
        const aName = document.getElementById(`anim-name-${i}`).value.trim() || `Animal #${i}`;
        const aType = document.getElementById(`anim-type-${i}`).value;
        const aAge = document.getElementById(`anim-age-${i}`).value;
        const aStatus = document.getElementById(`anim-status-${i}`).value;
        let aMilk = 'N/A';
        if (aStatus === 'Lactating') {
            const milkEl = document.getElementById(`anim-milk-${i}`);
            aMilk = milkEl ? milkEl.value : 'Medium (5–10 L)';
        }

        animals.push({
            animal_index: i,
            animal_name: aName,
            animal_type: aType,
            age_group: aAge,
            lactation_status: aStatus,
            milk_production: aMilk
        });
    }

    // Step 4 feed and storage
    let mainFeed = 'Green Fodder';
    for (const r of document.getElementsByName('wz-main-feed')) { if (r.checked) mainFeed = r.value; }
    let storage = 'Shed';
    for (const r of document.getElementsByName('wz-storage')) { if (r.checked) storage = r.value; }

    const payload = {
        user_id: state.currentUser.id,
        farmer_name: farmerName,
        village_location: village,
        preferred_language: lang,
        total_animals: count,
        animal_types: types,
        main_feed_type: mainFeed,
        feed_storage: storage,
        animals: animals
    };

    try {
        const resp = await fetch('/api/onboarding/setup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await resp.json();
        if (!resp.ok) {
            throw new Error(data.detail || 'Farm setup failed.');
        }

        state.currentUser = data.user;
        localStorage.setItem('smartfeed_user', JSON.stringify(data.user));
        state.farmerProfile = data.profile;
        state.farmerAnimals = data.profile ? data.profile.animals : animals;

        closeWizardModal();

        if (lang !== state.language) {
            setLanguage(lang);
        }

        // Land immediately on Step 5: Farmer Dashboard!
        updateUserSessionUI();
        switchTab('home');

    } catch (err) {
        showWizardError(err.message);
    }
}

// ===================================================================
// Step 5: Farmer Personalized Dashboard Data & Action Modals
// ===================================================================

async function loadFarmerDashboardData() {
    if (!state.currentUser || state.currentUser.role !== 'farmer') return;

    try {
        const resp = await fetch(`/api/farmer/farm-summary?user_id=${state.currentUser.id}`);
        if (!resp.ok) return;
        const data = await resp.json();
        const p = data.profile || {};
        state.farmerProfile = p;
        state.farmerAnimals = p.animals || [];

        // Update Welcome Hero
        const nameEl = document.getElementById('farmer-dash-name');
        const farmNameEl = document.getElementById('farmer-dash-farm-name');
        const villageEl = document.getElementById('farmer-dash-village');
        const langEl = document.getElementById('farmer-dash-lang');

        const fName = p.farmer_name || state.currentUser.full_name || 'Farmer';
        if (nameEl) nameEl.innerText = fName;
        if (farmNameEl) farmNameEl.innerText = `${fName}'s Farm`;
        if (villageEl) villageEl.innerText = p.village_location || 'Rural';
        if (langEl) langEl.innerText = p.preferred_language === 'te' ? 'తెలుగు' : (p.preferred_language === 'hi' ? 'हिंदी' : 'English');

        // Update 7 KPI Summary Badges
        const elCows = document.getElementById('fd-cows');
        const elBuffs = document.getElementById('fd-buffaloes');
        const elLact = document.getElementById('fd-lactating');
        const elPreg = document.getElementById('fd-pregnant');
        const elFeed = document.getElementById('fd-main-feed');
        const elStor = document.getElementById('fd-storage');
        const elTests = document.getElementById('fd-tests');

        if (elCows) elCows.innerText = p.cows_count || 0;
        if (elBuffs) elBuffs.innerText = p.buffaloes_count || 0;
        if (elLact) elLact.innerText = p.lactating_count || 0;
        if (elPreg) elPreg.innerText = p.pregnant_count || 0;
        if (elFeed) elFeed.innerText = p.main_feed_type || 'Silage';
        if (elStor) elStor.innerText = p.feed_storage || 'Shed';

        // Fetch scan count & history records for this farmer
        const dashResp = await fetch(`/api/dashboard?user_id=${state.currentUser.id}`);
        if (dashResp.ok) {
            const dData = await dashResp.json();
            if (elTests) elTests.innerText = (dData.metrics && dData.metrics.total_tests) || 0;
            renderFarmerHistoryTable(dData.recent_tests || [], dData.metrics || {});
        }

    } catch (e) {
        console.error('Failed to load farmer dashboard:', e);
    }
}

function renderFarmerHistoryTable(tests, metrics) {
    const totalEl = document.getElementById('farmer-hist-total-count');
    const safeEl = document.getElementById('farmer-hist-safe-count');
    const riskEl = document.getElementById('farmer-hist-risk-count');
    const tbody = document.getElementById('farmer-history-tbody');

    if (totalEl) totalEl.innerText = metrics.total_tests !== undefined ? metrics.total_tests : (tests.length || 0);
    if (safeEl) safeEl.innerText = metrics.safe_count !== undefined ? metrics.safe_count : (metrics.safe_tests || 0);
    if (riskEl) riskEl.innerText = metrics.danger_count !== undefined ? metrics.danger_count : (metrics.high_risk_tests || 0);

    if (!tbody) return;
    tbody.innerHTML = '';

    if (!tests || tests.length === 0) {
        const curL = state.language || 'en';
        const emptyTitle = curL === 'te' ? 'ఇంకా ఎలాంటి మేత పరీక్షలు నమోదు కాలేదు' : (curL === 'hi' ? 'अभी तक कोई चारा परीक्षण रिकॉर्ड नहीं हुआ है' : 'No feed diagnostic tests recorded yet');
        const emptySub = curL === 'te' ? 'మీ పశువుల మేత నాణ్యత, బూజు మరియు కల్తీని తనిఖీ చేయడానికి స్కానర్‌ను ప్రారంభించండి.' : (curL === 'hi' ? 'अपने पशुओं के चारे की गुणवत्ता, फफूंद और मिलावट की जांच के लिए स्कैनर शुरू करें।' : 'Start the quality scanner to check feed safety, mould, and adulteration for your cattle.');
        const btnTxt = curL === 'te' ? '📸 మేతను పరీక్షించండి →' : (curL === 'hi' ? '📸 चारा परीक्षण शुरू करें →' : '📸 Start Feed Scan →');
        tbody.innerHTML = `
            <tr>
                <td colspan="8" style="padding: 40px 20px; text-align: center; color: var(--slate-500);">
                    <div style="font-size: 2.2rem; margin-bottom: 8px;">🌾</div>
                    <div style="font-size: 1rem; font-weight: 700; color: var(--slate-800); margin-bottom: 6px;">
                        ${emptyTitle}
                    </div>
                    <div style="font-size: 0.85rem; color: var(--slate-500); margin-bottom: 14px;">
                        ${emptySub}
                    </div>
                    <button class="btn btn-primary" onclick="switchTab('scanner')" style="padding: 8px 18px; font-size: 0.88rem;">
                        ${btnTxt}
                    </button>
                </td>
            </tr>
        `;
        return;
    }

    tests.forEach(t => {
        const tr = document.createElement('tr');
        tr.style.borderBottom = '1px solid var(--slate-200)';
        tr.style.transition = 'background 0.2s ease';
        tr.onmouseenter = () => tr.style.background = 'var(--slate-50)';
        tr.onmouseleave = () => tr.style.background = '';

        const rawDate = t.timestamp || t.created_at || '';
        const dateClean = rawDate.replace('T', ' ').slice(0, 16);
        const score = Math.round(Number(t.quality_score || 0));

        let scoreColor = 'var(--primary-emerald)';
        if (score < 50) scoreColor = 'var(--crimson-danger)';
        else if (score < 80) scoreColor = '#D97706';

        let badgeHtml = t.safety_badge;
        if (!badgeHtml || typeof badgeHtml !== 'string') {
            if (score >= 80 && String(t.overall_risk).toLowerCase() !== 'high') {
                badgeHtml = '<span class="safety-badge badge-safe">🟢 SAFE</span>';
            } else if (score >= 50 && String(t.overall_risk).toLowerCase() !== 'high') {
                badgeHtml = '<span class="safety-badge badge-caution">🟡 CAUTION</span>';
            } else {
                badgeHtml = '<span class="safety-badge badge-danger">🔴 HIGH RISK</span>';
            }
        }

        const shelfDays = t.shelf_life_days !== undefined ? t.shelf_life_days : (t.shelf_life?.shelf_life_days);
        const shelfStatus = t.shelf_life_status || t.shelf_life?.shelf_life_status || 'SAFE';
        let shelfBadge = `<span style="font-size: 0.82rem; font-weight: 700; color: var(--primary-emerald);">🛡️ ${shelfDays || 0}d Safe</span>`;
        if (shelfDays === 0 || shelfStatus === 'EXPIRED') {
            shelfBadge = `<span style="font-size: 0.82rem; font-weight: 700; color: var(--crimson-danger);">⚠️ Expired</span>`;
        } else if (shelfDays <= 5 || shelfStatus === 'ATTENTION') {
            shelfBadge = `<span style="font-size: 0.82rem; font-weight: 700; color: #D97706;">⏳ ${shelfDays}d Left</span>`;
        }

        tr.innerHTML = `
            <td style="padding: 12px; font-family: 'JetBrains Mono', monospace; font-weight: 800; color: var(--accent-blue);">
                <a href="javascript:void(0)" onclick="viewBatchPassport('${t.batch_id}')" style="color: var(--accent-blue); text-decoration: underline;" title="View Digital Passport">
                    ${t.batch_id}
                </a>
            </td>
            <td style="padding: 12px; font-weight: 600; color: var(--slate-800);">${t.sample_type || 'Feed Pellet'}</td>
            <td style="padding: 12px;">
                <div style="font-weight: 800; color: ${scoreColor}; font-size: 0.96rem;">${score} / 100</div>
                <div style="height: 4px; width: 60px; background: var(--slate-200); border-radius: 2px; margin-top: 4px; overflow: hidden;">
                    <div style="width: ${Math.min(100, score)}%; height: 100%; background: ${scoreColor};"></div>
                </div>
            </td>
            <td style="padding: 12px;">${badgeHtml}</td>
            <td style="padding: 12px; font-size: 0.84rem; color: var(--slate-700); max-width: 220px;">
                ${t.primary_concern || 'Standard Sample Quality'}
            </td>
            <td style="padding: 12px;">${shelfBadge}</td>
            <td style="padding: 12px; font-size: 0.8rem; color: var(--slate-500); font-family: monospace;">${dateClean}</td>
            <td style="padding: 12px; text-align: right;">
                <button class="btn btn-sm btn-primary" onclick="viewBatchPassport('${t.batch_id}')" style="padding: 5px 12px; font-size: 0.78rem; white-space: nowrap;">
                    ${state.language === 'te' ? '🪪 పాస్‌పోర్ట్' : (state.language === 'hi' ? '🪪 पासपोर्ट' : '🪪 Passport')}
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function handleTile7Click() {
    const sec = document.getElementById('farmer-history-section');
    if (sec) {
        sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
        sec.style.transition = 'box-shadow 0.3s ease';
        sec.style.boxShadow = '0 0 0 3px var(--primary-emerald)';
        setTimeout(() => { sec.style.boxShadow = ''; }, 1600);
    } else {
        openMyHistoryModal();
    }
}

async function viewBatchPassport(batchId) {
    if (!batchId) return;
    try {
        closeMyHistoryModal();
        switchTab('passport');

        const resp = await fetch(`/api/passport/${encodeURIComponent(batchId)}`);
        if (!resp.ok) throw new Error('Passport record not found for ' + batchId);
        const res = await resp.json();
        const p = res.passport || {};
        p.qr_code_base64 = res.qr_base64;
        p.health_score = p.quality_score;
        p.safety_badge = p.quality_badge;
        p.shelf_life = {
            shelf_life_days: p.shelf_life_days || 0,
            shelf_life_status: p.shelf_life_status || 'SAFE',
            safe_until_date: p.safe_until_date || 'N/A'
        };

        const batchDisplay = document.getElementById('passport-batch-id-display');
        if (batchDisplay) batchDisplay.innerText = p.batch_id;
        updatePassportCard(p);

        const card = document.getElementById('passport-certificate-card');
        if (card) {
            card.scrollIntoView({ behavior: 'smooth' });
        }
    } catch (e) {
        alert('Passport Error: ' + e.message);
    }
}

function openMyAnimalsModal() {
    const modal = document.getElementById('modal-my-animals');
    if (!modal) return;
    modal.style.display = 'flex';

    const container = document.getElementById('my-animals-cards-container');
    if (!container) return;
    container.innerHTML = '';

    const animals = state.farmerAnimals || [];
    const curL = state.language || 'en';
    if (animals.length === 0) {
        const emptyMsg = curL === 'te' 
            ? 'ఇంకా ఎలాంటి పశువులు నమోదు కాలేదు. మీ పశువులను నమోదు చేయడానికి కింద ఉన్న "పశువుల సంఖ్య & సెటప్ మార్చండి" బటన్‌పై క్లిక్ చేయండి.'
            : (curL === 'hi'
                ? 'अभी तक कोई पशु पंजीकृत नहीं है। अपने पशुओं को पंजीकृत करने के लिए नीचे "पशु संख्या व सेटअप बदलें" पर क्लिक करें।'
                : 'No animals registered yet. Click "Edit Animal Count & Setup" below to register your cattle.');
        container.innerHTML = `<div style="text-align: center; color: var(--slate-500); padding: 20px;">${emptyMsg}</div>`;
        return;
    }

    const typeLbl = curL === 'te' ? 'రకం:' : (curL === 'hi' ? 'प्रकार:' : 'Type:');
    const ageLbl = curL === 'te' ? 'వయస్సు:' : (curL === 'hi' ? 'आयु:' : 'Age:');
    const milkLbl = curL === 'te' ? 'పాల దిగుబడి:' : (curL === 'hi' ? 'दूध:' : 'Milk Yield:');
    const rationLbl = curL === 'te' ? 'లక్ష్య దాణా:' : (curL === 'hi' ? 'लक्षित आहार:' : 'Target Ration:');

    animals.forEach((a, idx) => {
        const isCow = a.animal_type === 'Cow';
        const isLactating = a.lactation_status === 'Lactating';
        const isPreg = a.lactation_status === 'Pregnant';
        const badgeColor = isLactating ? 'var(--primary-emerald)' : (isPreg ? '#3B82F6' : '#F59E0B');

        let targetRationText = '';
        if (curL === 'te') {
            targetRationText = isLactating ? '22 kg పచ్చిగడ్డి + 4 kg ఎండుగడ్డి + 3 kg దాణా' : (isPreg ? '20 kg పచ్చిగడ్డి + 5 kg ఎండుగడ్డి + కాల్షియం ఖనిజాలు' : '15 kg పచ్చిగడ్డి + 6 kg ఎండుగడ్డి నిర్వహణ మోతాదు');
        } else if (curL === 'hi') {
            targetRationText = isLactating ? '22 kg हरा चारा + 4 kg सूखा भूसा + 3 kg संतुलित दाना' : (isPreg ? '20 kg हरा चारा + 5 kg भूसा + खनिज मिश्रण' : '15 kg हरा चारा + 6 kg भूसा रख-रखाव खुराक');
        } else {
            targetRationText = isLactating ? '22kg Green Fodder + 4kg Dry Straw + 3kg Concentrate Mash' : (isPreg ? '20kg Green Fodder + 5kg Straw + Mineral Mix (High Calcium)' : '15kg Green + 6kg Straw maintenance ration');
        }

        let stageDisplay = a.lactation_status || 'Active';
        if (curL === 'te') {
            if (stageDisplay === 'Lactating') stageDisplay = '🥛 పాలిచ్చేది';
            else if (stageDisplay === 'Pregnant') stageDisplay = '🤰 చూడి';
            else if (stageDisplay === 'Dry') stageDisplay = '🍂 ఎండినది';
        } else if (curL === 'hi') {
            if (stageDisplay === 'Lactating') stageDisplay = '🥛 दुधारू';
            else if (stageDisplay === 'Pregnant') stageDisplay = '🤰 गर्भवती';
            else if (stageDisplay === 'Dry') stageDisplay = '🍂 सूखी';
        }

        const card = document.createElement('div');
        card.className = 'animal-profile-card';
        card.style.background = '#F8FAFC';
        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-weight: 800; font-size: 1.05rem; color: var(--slate-900);">
                    ${isCow ? '🐄' : '🐃'} ${a.animal_name || (isCow ? (curL === 'te' ? 'ఆవు' : (curL === 'hi' ? 'गाय' : 'Cow')) : (curL === 'te' ? 'గేదె' : (curL === 'hi' ? 'भैंस' : 'Buffalo'))) + ' #' + (idx + 1)}
                </span>
                <span class="safety-badge" style="background: ${isLactating ? '#ECFDF5' : (isPreg ? '#EFF6FF' : '#FFFBEB')}; color: ${badgeColor}; border: 1px solid ${badgeColor};">
                    ${stageDisplay}
                </span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; font-size: 0.82rem; color: var(--slate-600);">
                <div><strong>${typeLbl}</strong> ${isCow ? (curL === 'te' ? 'ఆవు' : (curL === 'hi' ? 'गाय' : 'Cow')) : (curL === 'te' ? 'గేదె' : (curL === 'hi' ? 'भैंस' : 'Buffalo'))}</div>
                <div><strong>${ageLbl}</strong> ${a.age_group || 'Adult'}</div>
                <div><strong>${milkLbl}</strong> <span style="font-weight: 700; color: ${isLactating ? 'var(--primary-emerald)' : 'var(--slate-500)'};">${a.milk_production || 'N/A'}</span></div>
            </div>
            <div style="margin-top: 8px; font-size: 0.78rem; background: #FFFFFF; border-radius: 8px; padding: 6px 10px; border: 1px solid var(--slate-200); color: var(--slate-700);">
                🌾 <strong>${rationLbl}</strong> ${targetRationText}
            </div>
        `;
        container.appendChild(card);
    });
}

function closeMyAnimalsModal() {
    const modal = document.getElementById('modal-my-animals');
    if (modal) modal.style.display = 'none';
}

// ===================================================================
// Step 6: 🐄🌾 Time-Based Smart Feeding Planner & Intelligence Controller
// ===================================================================

let smartDiaryState = {
    selectedAnimalId: null,
    currentPlan: null,
    activeSlotKey: 'morning'
};

function openFeedDiaryModal() {
    const modal = document.getElementById('modal-feed-diary');
    if (!modal) return;
    modal.style.display = 'flex';

    const datePicker = document.getElementById('diary-date-picker');
    if (datePicker && !datePicker.value) {
        datePicker.value = new Date().toISOString().split('T')[0];
    }

    loadSmartFeedDiary();
}

function closeFeedDiaryModal() {
    const modal = document.getElementById('modal-feed-diary');
    if (modal) modal.style.display = 'none';
}

async function loadSmartFeedDiary() {
    if (!state.currentUser) {
        alert(state.language === 'te' ? 'దయచేసి మేత డైరీని చూడటానికి లాగిన్ అవ్వండి.' : 'Please sign in to access your Feed Diary.');
        closeFeedDiaryModal();
        openAuthModal('signin');
        return;
    }

    const datePicker = document.getElementById('diary-date-picker');
    const selectedDate = datePicker ? datePicker.value : new Date().toISOString().split('T')[0];
    const animalId = smartDiaryState.selectedAnimalId || '';

    try {
        const resp = await fetch(`/api/feed-diary/today?user_id=${state.currentUser.id}&animal_id=${animalId}&date=${selectedDate}&language=${state.language}`);
        if (!resp.ok) throw new Error('Failed to load feeding diary.');
        const data = await resp.json();

        smartDiaryState.currentPlan = data.plan;
        smartDiaryState.selectedAnimalId = data.animal ? data.animal.animal_id : null;
        smartDiaryState.activeSlotKey = data.plan.active_slot || 'morning';

        renderDiaryAnimalTabs(data.farmer_animals || [], data.animal);
        renderDiaryReminder(data.plan);
        renderDiarySlots(data.plan.slots, data.date);
        renderDiaryTotals(data.daily_totals, data.plan.daily_targets, data.animal);

        // Load AI Feeding Insights
        loadFeedingInsights(state.currentUser.id, smartDiaryState.selectedAnimalId);

    } catch (err) {
        console.error('Error loading smart feed diary:', err);
    }
}

function selectDiaryAnimal(animalId) {
    smartDiaryState.selectedAnimalId = animalId;
    loadSmartFeedDiary();
}

function renderDiaryAnimalTabs(animals, currentAnimal) {
    const container = document.getElementById('diary-animal-tabs-container');
    if (!container) return;
    container.innerHTML = '';

    if (!animals || animals.length === 0) {
        const btn = document.createElement('button');
        btn.className = 'btn btn-primary';
        btn.style.cssText = 'padding: 4px 12px; font-size: 0.8rem; border-radius: 20px;';
        btn.innerText = `🐄 ${currentAnimal?.animal_name || 'Dairy Cattle'} (8L)`;
        container.appendChild(btn);
        return;
    }

    animals.forEach(a => {
        const isSelected = (smartDiaryState.selectedAnimalId === a.id) || (!smartDiaryState.selectedAnimalId && currentAnimal && currentAnimal.animal_id === a.id);
        const isCow = (a.species || a.animal_type || 'Cow') === 'Cow';
        const milkText = a.daily_milk_litres ? `${a.daily_milk_litres}L` : (a.lactation_stage || 'Active');

        const btn = document.createElement('button');
        btn.style.cssText = `padding: 4px 12px; font-size: 0.8rem; border-radius: 20px; cursor: pointer; transition: all 0.2s; font-weight: 700; ${
            isSelected
                ? 'background: #065F46; color: #FFFFFF; border: 1.5px solid #065F46; box-shadow: 0 2px 6px rgba(6,95,70,0.25);'
                : 'background: #FFFFFF; color: var(--slate-700); border: 1px solid var(--slate-300);'
        }`;
        btn.innerHTML = `${isCow ? '🐄' : '🐃'} ${a.tag_number || a.name || 'Cattle'} (${milkText})`;
        btn.onclick = () => selectDiaryAnimal(a.id);
        container.appendChild(btn);
    });
}

function renderDiaryReminder(plan) {
    const timeEl = document.getElementById('diary-next-slot-time');
    const badgeEl = document.getElementById('diary-next-slot-badge');
    const descEl = document.getElementById('diary-next-slot-desc');

    if (timeEl) timeEl.innerText = plan.next_reminder_time || '--:--';
    if (badgeEl) {
        const slotNames = {
            morning: { te: '🌅 ఉదయపు మేత సమయం', hi: '🌅 सुबह का चारा समय', en: '🌅 Morning Feeding Slot' },
            afternoon: { te: '☀️ మధ్యాహ్న మేత సమయం (Cudding)', hi: '☀️ दोपहर का चारा समय', en: '☀️ Afternoon Rumen Cudding' },
            evening: { te: '🌙 సాయంత్రపు మేత సమయం', hi: '🌙 शाम का चारा समय', en: '🌙 Evening Feeding Slot' }
        };
        const curSlotObj = slotNames[plan.next_reminder_slot] || { te: 'తదుపరి మేత' };
        badgeEl.innerText = curSlotObj[state.language] || curSlotObj.te;
    }
    if (descEl) {
        const d = plan.reminder_description || {};
        descEl.innerText = d[state.language] || d.te || d.en || 'మేత ప్రణాళిక సిద్ధం చేసుకోండి.';
    }
}

function scrollToActiveSlot() {
    const activeCard = document.getElementById(`slot-card-${smartDiaryState.activeSlotKey}`);
    if (activeCard) {
        activeCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
        activeCard.style.transition = 'box-shadow 0.3s';
        activeCard.style.boxShadow = '0 0 0 4px rgba(16,185,129,0.4)';
        setTimeout(() => {
            activeCard.style.boxShadow = '';
        }, 1500);
    }
}

function renderDiarySlots(slots, feedingDate) {
    const container = document.getElementById('diary-slots-container');
    if (!container) return;
    container.innerHTML = '';

    const lang = state.language;

    slots.forEach(slot => {
        const key = slot.slot_key;
        const isActive = (key === smartDiaryState.activeSlotKey);
        const isLogged = Boolean(slot.logged);
        const record = slot.record || {};
        const sugg = slot.suggested || {};

        const card = document.createElement('div');
        card.id = `slot-card-${key}`;
        card.style.cssText = `
            border-radius: 14px;
            padding: 16px 20px;
            background: #FFFFFF;
            transition: all 0.2s ease-in-out;
            border: ${isActive ? '2px solid #059669;' : '1px solid var(--slate-200);'}
            box-shadow: ${isActive ? '0 4px 16px rgba(5,150,105,0.12);' : '0 2px 6px rgba(0,0,0,0.03);'}
        `;

        const slotTitle = slot[`title_${lang}`] || slot.title_te || slot.title_en;
        const purposeText = slot[`purpose_${lang}`] || slot.purpose_te || slot.purpose_en;

        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 10px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-weight: 800; font-size: 1.05rem; color: var(--slate-900);">${slotTitle}</span>
                    <span style="font-size: 0.78rem; background: var(--slate-100); color: var(--slate-600); padding: 2px 8px; border-radius: 6px; font-weight: 600;">
                        ⏱️ ${slot.time_window}
                    </span>
                    ${isActive ? '<span style="font-size: 0.72rem; background: #DCFCE7; color: #15803D; padding: 2px 8px; border-radius: 6px; font-weight: 800; border: 1px solid #86EFAC;">⚡ ACTIVE NOW</span>' : ''}
                </div>
                <div>
                    <span class="safety-badge" style="${
                        isLogged 
                            ? 'background: #ECFDF5; color: #065F46; border: 1.5px solid #059669; font-weight: 800;' 
                            : 'background: #FFFBEB; color: #B45309; border: 1.5px solid #F59E0B; font-weight: 700;'
                    }">
                        ${isLogged ? (lang === 'te' ? '✅ నమోదైంది' : (lang === 'hi' ? '✅ दर्ज हुआ' : '✅ Logged')) : (lang === 'te' ? '⏳ నమోదు చేయాలి' : (lang === 'hi' ? '⏳ लंबित' : '⏳ Pending'))}
                    </span>
                </div>
            </div>

            <!-- Purpose Guide -->
            <div style="font-size: 0.82rem; color: var(--slate-600); margin-bottom: 12px; background: #F8FAFC; padding: 8px 12px; border-radius: 8px; border-left: 3px solid ${isActive ? '#059669' : '#94A3B8'};">
                💡 <strong>${lang === 'te' ? 'ప్రాముఖ్యత:' : (lang === 'hi' ? 'उद्देश्य:' : 'Purpose:')}</strong> ${purposeText}
            </div>

            <!-- Logged View vs Input Form -->
            <div id="slot-body-${key}">
                ${isLogged ? renderSlotLoggedSummary(key, record, sugg) : renderSlotInputForm(key, sugg, feedingDate)}
            </div>
        `;

        container.appendChild(card);
    });
}

function renderSlotLoggedSummary(key, record, sugg) {
    const l = state.language || 'en';
    const sumTitle = l === 'te' ? '🎉 ఈ సమయపు మేత విజయవంతంగా నమోదైంది:' : (l === 'hi' ? '🎉 इस समय का दर्ज चारा:' : '🎉 Recorded Intake for this Slot:');
    const lblConc = l === 'te' ? '🥣 దాణా:' : (l === 'hi' ? '🥣 दाना:' : '🥣 Concentrate:');
    const lblGreen = l === 'te' ? '🌿 పచ్చిగడ్డి:' : (l === 'hi' ? '🌿 हरा चारा:' : '🌿 Green Fodder:');
    const lblStraw = l === 'te' ? '🌾 ఎండుగడ్డి:' : (l === 'hi' ? '🌾 सूखा भूसा:' : '🌾 Dry Straw:');
    const lblMin = l === 'te' ? '🧂 ఖనిజాలు:' : (l === 'hi' ? '🧂 खनिज:' : '🧂 Minerals:');
    const lblMilk = l === 'te' ? '🥛 పాల దిగుబడి:' : (l === 'hi' ? '🥛 दूध उत्पादन:' : '🥛 Milk Yield:');
    const lblNotes = l === 'te' ? '📝 గమనికలు:' : (l === 'hi' ? '📝 टिप्पणियाँ:' : '📝 Notes:');
    const btnEdit = l === 'te' ? '✏️ సవరించండి' : (l === 'hi' ? '✏️ संपादित करें' : '✏️ Edit Log');

    return `
        <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 10px; padding: 12px 16px; margin-bottom: 10px;">
            <div style="font-size: 0.85rem; font-weight: 700; color: #166534; margin-bottom: 6px;">
                ${sumTitle}
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 8px; font-size: 0.84rem; color: #14532D;">
                ${record.concentrate_kg > 0 ? `<div>${lblConc} <strong>${record.concentrate_kg} kg</strong></div>` : ''}
                ${record.green_fodder_kg > 0 ? `<div>${lblGreen} <strong>${record.green_fodder_kg} kg</strong></div>` : ''}
                ${record.dry_straw_kg > 0 ? `<div>${lblStraw} <strong>${record.dry_straw_kg} kg</strong></div>` : ''}
                ${record.minerals_grams > 0 ? `<div>${lblMin} <strong>${record.minerals_grams} g</strong></div>` : ''}
                ${record.milk_yield_litres > 0 ? `<div>${lblMilk} <strong>${record.milk_yield_litres} L</strong></div>` : ''}
            </div>
            ${record.notes ? `<div style="margin-top: 6px; font-size: 0.8rem; color: #15803D; font-style: italic;">${lblNotes} ${record.notes}</div>` : ''}
        </div>
        <div style="text-align: right;">
            <button class="btn btn-secondary" onclick="toggleEditSlotForm('${key}')" style="font-size: 0.78rem; padding: 4px 10px;">
                ${btnEdit}
            </button>
        </div>
    `;
}

function renderSlotInputForm(key, sugg, feedingDate) {
    const isEvening = (key === 'evening');
    const isAfternoon = (key === 'afternoon');
    const l = state.language || 'en';

    const recTitle = l === 'te' ? '🌾 సిఫారసు చేసిన మోతాదు:' : (l === 'hi' ? '🌾 अनुशंसित आहार:' : '🌾 Recommended Diet:');
    let recDesc = '';
    if (isAfternoon) {
        recDesc = l === 'te' 
            ? `${sugg.dry_straw_kg || 4} kg ఎండుగడ్డి + ${sugg.water_litres || 20}L తాగునీరు`
            : (l === 'hi' ? `${sugg.dry_straw_kg || 4} kg सूखा भूसा + ${sugg.water_litres || 20}L पानी` : `${sugg.dry_straw_kg || 4} kg Dry Straw + ${sugg.water_litres || 20}L Water`);
    } else {
        const conc = sugg.concentrate_kg || 0;
        const grn = sugg.green_fodder_kg || 0;
        const min = sugg.minerals_grams || 60;
        if (l === 'te') {
            recDesc = `${conc} kg దాణా + ${grn} kg పచ్చిగడ్డి${isEvening ? ` + ${min}g ఖనిజ లవణాలు` : ''}`;
        } else if (l === 'hi') {
            recDesc = `${conc} kg दाना + ${grn} kg हरा चारा${isEvening ? ` + ${min}g खनिज मिश्रण` : ''}`;
        } else {
            recDesc = `${conc} kg Concentrate + ${grn} kg Green Fodder${isEvening ? ` + ${min}g Minerals` : ''}`;
        }
    }

    const lblConc = l === 'te' ? '🥣 దాణా (kg)' : (l === 'hi' ? '🥣 दाना (kg)' : '🥣 Concentrate (kg)');
    const lblGreen = l === 'te' ? '🌿 పచ్చిగడ్డి (kg)' : (l === 'hi' ? '🌿 हरा चारा (kg)' : '🌿 Green Fodder (kg)');
    const lblStraw = l === 'te' ? '🌾 ఎండుగడ్డి (kg)' : (l === 'hi' ? '🌾 सूखा भूसा (kg)' : '🌾 Dry Straw (kg)');
    const lblWater = l === 'te' ? '💧 తాగునీరు (L)' : (l === 'hi' ? '💧 पानी (L)' : '💧 Drinking Water (L)');
    const lblMin = l === 'te' ? '🧂 ఖనిజ మిశ్రమం (g)' : (l === 'hi' ? '🧂 खनिज मिश्रण (g)' : '🧂 Mineral Mixture (g)');
    const lblMilk = l === 'te' ? '🥛 పితికిన పాలు (L)' : (l === 'hi' ? '🥛 निकाला गया दूध (L)' : '🥛 Milk Yield (L)');
    const phNotes = l === 'te' ? 'గమనికలు e.g. పశువు ఆరోగ్యంగా మేత మేసింది...' : (l === 'hi' ? 'टिप्पणियाँ उदा. पशु ने सामान्य रूप से चारा खाया...' : 'Notes e.g. Cattle fed normally, active...');
    const btnSave = l === 'te' ? 'నమోదు చేయండి' : (l === 'hi' ? 'दर्ज करें' : 'Save Log');

    return `
        <div style="background: #FAFAFA; border: 1px solid var(--slate-200); border-radius: 10px; padding: 14px 16px;">
            <div style="font-size: 0.82rem; color: var(--slate-600); margin-bottom: 10px; font-weight: 600;">
                ${recTitle} 
                <span style="color: #047857; font-weight: 700;">
                    ${recDesc}
                </span>
            </div>

            <!-- Inputs Row -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-bottom: 12px;">
                ${!isAfternoon ? `
                    <div>
                        <label style="display: block; font-size: 0.75rem; font-weight: 700; color: var(--slate-700); margin-bottom: 3px;">${lblConc}</label>
                        <input type="number" id="input-${key}-conc" step="0.1" value="${sugg.concentrate_kg || 0}" style="width: 100%; padding: 6px 10px; border-radius: 8px; border: 1px solid var(--slate-300); font-size: 0.88rem; font-weight: 700;">
                    </div>
                    <div>
                        <label style="display: block; font-size: 0.75rem; font-weight: 700; color: var(--slate-700); margin-bottom: 3px;">${lblGreen}</label>
                        <input type="number" id="input-${key}-green" step="0.5" value="${sugg.green_fodder_kg || 0}" style="width: 100%; padding: 6px 10px; border-radius: 8px; border: 1px solid var(--slate-300); font-size: 0.88rem; font-weight: 700;">
                    </div>
                ` : `
                    <div>
                        <label style="display: block; font-size: 0.75rem; font-weight: 700; color: var(--slate-700); margin-bottom: 3px;">${lblStraw}</label>
                        <input type="number" id="input-${key}-straw" step="0.5" value="${sugg.dry_straw_kg || 4}" style="width: 100%; padding: 6px 10px; border-radius: 8px; border: 1px solid var(--slate-300); font-size: 0.88rem; font-weight: 700;">
                    </div>
                    <div>
                        <label style="display: block; font-size: 0.75rem; font-weight: 700; color: var(--slate-700); margin-bottom: 3px;">${lblWater}</label>
                        <input type="number" id="input-${key}-water" step="1" value="${sugg.water_litres || 20}" style="width: 100%; padding: 6px 10px; border-radius: 8px; border: 1px solid var(--slate-300); font-size: 0.88rem; font-weight: 700;">
                    </div>
                `}

                ${isEvening ? `
                    <div>
                        <label style="display: block; font-size: 0.75rem; font-weight: 700; color: var(--slate-700); margin-bottom: 3px;">${lblMin}</label>
                        <input type="number" id="input-${key}-minerals" step="5" value="${sugg.minerals_grams || 60}" style="width: 100%; padding: 6px 10px; border-radius: 8px; border: 1px solid var(--slate-300); font-size: 0.88rem; font-weight: 700;">
                    </div>
                ` : ''}

                <!-- Milk Recording for Morning or Evening -->
                ${!isAfternoon ? `
                    <div>
                        <label style="display: block; font-size: 0.75rem; font-weight: 700; color: #065F46; margin-bottom: 3px;">${lblMilk}</label>
                        <input type="number" id="input-${key}-milk" step="0.5" value="${sugg.target_milk_litres || 0}" style="width: 100%; padding: 6px 10px; border-radius: 8px; border: 1.5px solid #10B981; background: #F0FDF4; font-size: 0.88rem; font-weight: 800; color: #065F46;">
                    </div>
                ` : ''}
            </div>

            <!-- Notes & Save Button Row -->
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                <input type="text" id="input-${key}-notes" placeholder="${phNotes}" style="flex: 1; min-width: 180px; padding: 6px 10px; border-radius: 8px; border: 1px solid var(--slate-300); font-size: 0.8rem;">
                <button class="btn btn-primary" onclick="submitSlotLog('${key}')" style="font-size: 0.82rem; padding: 7px 16px; background: #059669; border-color: #047857; display: flex; align-items: center; gap: 6px;">
                    <span>💾</span>
                    <span>${btnSave}</span>
                </button>
            </div>
        </div>
    `;
}

function toggleEditSlotForm(key) {
    const slotObj = smartDiaryState.currentPlan?.slots?.find(s => s.slot_key === key);
    if (!slotObj) return;
    const bodyEl = document.getElementById(`slot-body-${key}`);
    if (!bodyEl) return;

    const datePicker = document.getElementById('diary-date-picker');
    const selectedDate = datePicker ? datePicker.value : new Date().toISOString().split('T')[0];
    bodyEl.innerHTML = renderSlotInputForm(key, slotObj.suggested || {}, selectedDate);
}

async function submitSlotLog(key) {
    if (!state.currentUser) return;

    const datePicker = document.getElementById('diary-date-picker');
    const feedingDate = datePicker ? datePicker.value : new Date().toISOString().split('T')[0];

    const concEl = document.getElementById(`input-${key}-conc`);
    const greenEl = document.getElementById(`input-${key}-green`);
    const strawEl = document.getElementById(`input-${key}-straw`);
    const waterEl = document.getElementById(`input-${key}-water`);
    const mineralsEl = document.getElementById(`input-${key}-minerals`);
    const milkEl = document.getElementById(`input-${key}-milk`);
    const notesEl = document.getElementById(`input-${key}-notes`);

    const payload = {
        user_id: state.currentUser.id,
        animal_id: smartDiaryState.selectedAnimalId,
        feeding_date: feedingDate,
        time_slot: key,
        concentrate_kg: concEl ? parseFloat(concEl.value || 0) : 0,
        green_fodder_kg: greenEl ? parseFloat(greenEl.value || 0) : 0,
        dry_straw_kg: strawEl ? parseFloat(strawEl.value || 0) : 0,
        water_litres: waterEl ? parseFloat(waterEl.value || 0) : 0,
        minerals_grams: mineralsEl ? parseFloat(mineralsEl.value || 0) : 0,
        milk_yield_litres: milkEl ? parseFloat(milkEl.value || 0) : 0,
        notes: notesEl ? notesEl.value.trim() : ''
    };

    try {
        const resp = await fetch('/api/feed-diary/log', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!resp.ok) throw new Error('Failed to record feeding log.');
        const result = await resp.json();

        const rem = result.next_reminder || {};
        const curL = state.language || 'en';
        const remDesc = rem.description?.[curL] || rem.description?.te || (curL === 'te' ? 'తదుపరి మేత సమయానికి సిద్ధంగా ఉండండి.' : (curL === 'hi' ? 'अगले चारा समय के लिए तैयार रहें।' : 'Get ready for the next feeding slot.'));
        const alertTitle = curL === 'te' ? `✅ ${key.toUpperCase()} మేత రికార్డు చేయబడింది!` : (curL === 'hi' ? `✅ ${key.toUpperCase()} चारा दर्ज किया गया!` : `✅ ${key.toUpperCase()} Feeding logged successfully!`);
        const remTitle = curL === 'te' ? '🔔 తదుపరి రిమైండర్' : (curL === 'hi' ? '🔔 अगला अनुस्मारक' : '🔔 Next Reminder');
        alert(`${alertTitle}\n\n${remTitle} (${rem.reminder_time}):\n${remDesc}`);

        loadSmartFeedDiary();

    } catch (err) {
        alert('Error saving log: ' + err.message);
    }
}

function renderDiaryTotals(totals, targets, animal) {
    if (!totals) return;

    const elConc = document.getElementById('diary-total-conc');
    const elGreen = document.getElementById('diary-total-green');
    const elStraw = document.getElementById('diary-total-straw');
    const elMilk = document.getElementById('diary-total-milk');
    const elBadge = document.getElementById('diary-slots-progress-badge');

    if (elConc) elConc.innerText = `${totals.concentrate_kg || 0.0} kg`;
    if (elGreen) elGreen.innerText = `${totals.green_fodder_kg || 0.0} kg`;
    if (elStraw) elStraw.innerText = `${totals.dry_straw_kg || 0.0} kg`;
    if (elMilk) elMilk.innerText = `${totals.milk_yield_litres || 0.0} L`;

    if (elBadge) {
        elBadge.innerText = `${totals.slots_logged_count || 0} / ${totals.slots_total_count || 3} Slots Logged`;
        if (totals.slots_logged_count === totals.slots_total_count) {
            elBadge.style.background = '#DCFCE7';
            elBadge.style.color = '#15803D';
            elBadge.innerText = `🎉 All 3 Slots Logged Today!`;
        } else {
            elBadge.style.background = '#E0E7FF';
            elBadge.style.color = '#3730A3';
        }
    }

    if (targets) {
        const tgtConc = document.getElementById('diary-target-conc');
        const tgtGreen = document.getElementById('diary-target-green');
        const tgtStraw = document.getElementById('diary-target-straw');
        const tgtMilk = document.getElementById('diary-target-milk');

        const tgtPrefix = state.language === 'te' ? 'లక్ష్యం:' : (state.language === 'hi' ? 'लक्ष्य:' : 'Target:');
        if (tgtConc) tgtConc.innerText = `${tgtPrefix} ${targets.total_concentrate_kg || 0} kg`;
        if (tgtGreen) tgtGreen.innerText = `${tgtPrefix} ${targets.total_green_fodder_kg || 0} kg`;
        if (tgtStraw) tgtStraw.innerText = `${tgtPrefix} ${targets.total_dry_straw_kg || 0} kg`;
        if (tgtMilk && animal) tgtMilk.innerText = `${tgtPrefix} ${animal.milk_production || 8.0} L`;
    }
}

async function loadFeedingInsights(userId, animalId) {
    const headlineEl = document.getElementById('diary-insights-headline');
    const bodyEl = document.getElementById('diary-insights-body');
    const tipsContainer = document.getElementById('diary-insights-tips');

    try {
        const resp = await fetch(`/api/feed-diary/insights?user_id=${userId}&animal_id=${animalId || ''}&language=${state.language}`);
        if (!resp.ok) return;
        const data = await resp.json();
        const ins = data.insights || {};

        const lang = state.language;

        if (headlineEl) {
            const defHeadline = lang === 'te' ? '⭐ AI మేత విశ్లేషణ & పాల దిగుబడి ఇన్‌సైట్స్' : (lang === 'hi' ? '⭐ AI चारा विश्लेषण व दूध उत्पादन अंतर्दृष्टि' : '⭐ AI Feeding Pattern & Milk Intelligence');
            headlineEl.innerText = ins.headline?.[lang] || ins.headline?.en || defHeadline;
        }
        if (bodyEl) {
            const defBody = lang === 'te' ? 'రోజువారీ మేత నమోదు చేయడం వల్ల మీ పశువుల పాల ఉత్పత్తి మరియు ఆరోగ్యం పెరుగుతుంది.' : (lang === 'hi' ? 'दैनिक चारा दर्ज करने से आपके पशुओं का दूध उत्पादन और स्वास्थ्य सुधरता है।' : 'Logging daily feeds helps optimize your cattle\'s milk yield and nutritional health.');
            bodyEl.innerText = ins.insight_text?.[lang] || ins.insight_text?.en || defBody;
        }

        if (tipsContainer && ins.recommendation_tips) {
            tipsContainer.innerHTML = '';
            ins.recommendation_tips.forEach(t => {
                const tipDiv = document.createElement('div');
                tipDiv.style.cssText = 'background: #FFFFFF; border-radius: 8px; padding: 8px 12px; border: 1px solid #BFDBFE; font-size: 0.82rem; color: #1E3A8A; display: flex; align-items: center; gap: 8px;';
                const tipText = t[`tip_${lang}`] || t.tip_en || t.tip_te;
                tipDiv.innerHTML = `<span>${t.icon || '💡'}</span> <span>${tipText}</span>`;
                tipsContainer.appendChild(tipDiv);
            });
        }
    } catch (e) {
        console.error('Failed to load feeding insights:', e);
    }
}

function speakDailyFeedingPlan() {
    const lang = state.language || 'en';
    if (!smartDiaryState.currentPlan) {
        alert(lang === 'te' ? 'మేత ప్రణాళిక లోడ్ అవ్వలేదు.' : (lang === 'hi' ? 'चारा योजना लोड नहीं हुई।' : 'Feeding plan could not be loaded.'));
        return;
    }

    const plan = smartDiaryState.currentPlan;
    let speechText = '';

    const halfConc = (plan.daily_targets?.total_concentrate_kg ? plan.daily_targets.total_concentrate_kg / 2 : 1.5).toFixed(1);
    const strawKg = (plan.daily_targets?.total_dry_straw_kg || 4.0).toFixed(1);
    const remTime = plan.next_reminder_time || '06:30 AM';

    if (lang === 'te') {
        speechText = `నమస్కారం రైతు సోదరులారా. మీ పశువు కోసం నేటి స్మార్ట్ మేత ప్రణాళిక: ఉదయం పాలు పితికే సమయంలో ${halfConc} కేజీల దాణా మరియు పచ్చిగడ్డి అందించండి. మధ్యాహ్నం నెమరు వేయడానికి ${strawKg} కేజీల ఎండుగడ్డి ఇవ్వండి. సాయంత్రం దాణా మరియు ఖనిజ లవణాలు అందించండి. తదుపరి రిమైండర్: ${remTime}.`;
    } else if (lang === 'hi') {
        speechText = `नमस्ते किसान भाई। आज का दैनिक चारा कार्यक्रम: सुबह दोहन समय ${halfConc} किलो दाना और हरा चारा दें। दोपहर में जुगाली के लिए ${strawKg} किलो सूखा भूसा दें। शाम को दाना और खनिज मिश्रण दें। अगला समय: ${remTime}.`;
    } else {
        speechText = `Smart Feeding Plan for today: Morning milking ration includes ${halfConc} kg concentrate and fresh green fodder. Afternoon roughage provides ${strawKg} kg dry straw for rumen cudding. Evening ration includes concentrate and mineral mix. Next feeding reminder at ${remTime}.`;
    }

    if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(speechText);
        utterance.rate = 0.95;
        if (lang === 'te') utterance.lang = 'te-IN';
        else if (lang === 'hi') utterance.lang = 'hi-IN';
        else utterance.lang = 'en-US';
        window.speechSynthesis.speak(utterance);
    } else {
        alert(speechText);
    }
}

async function openMyHistoryModal() {
    const modal = document.getElementById('modal-my-history');
    if (!modal) return;
    modal.style.display = 'flex';

    const container = document.getElementById('my-history-records-container');
    if (!container) return;

    const curL = state.language || 'en';
    if (!state.currentUser) {
        const msg = curL === 'te' ? 'దయచేసి మీ పరీక్ష రికార్డులను చూడటానికి లాగిన్ అవ్వండి.' : (curL === 'hi' ? 'अपने परीक्षण रिकॉर्ड देखने के लिए कृपया साइन इन करें।' : 'Please sign in to view your test history.');
        container.innerHTML = `<div style="text-align: center; color: var(--slate-500); padding: 30px;">${msg}</div>`;
        return;
    }

    const loadMsg = curL === 'te' ? 'మీ పరీక్ష రికార్డులు లోడ్ అవుతున్నాయి...' : (curL === 'hi' ? 'आपके सहेजे गए परीक्षण लोड हो रहे हैं...' : 'Loading your saved feed tests...');
    container.innerHTML = `<div style="text-align: center; color: var(--slate-500); padding: 30px;">${loadMsg}</div>`;

    try {
        const resp = await fetch(`/api/dashboard?user_id=${state.currentUser.id}`);
        if (!resp.ok) throw new Error('Could not fetch test history.');
        const data = await resp.json();
        const tests = data.recent_tests || [];

        if (tests.length === 0) {
            const emptyTitle = curL === 'te' ? 'ఇంకా ఎలాంటి మేత పరీక్షలు నమోదు కాలేదు' : (curL === 'hi' ? 'अभी तक कोई चारा परीक्षण रिकॉर्ड नहीं हुआ है' : 'No feed diagnostic tests recorded yet');
            const emptySub = curL === 'te' ? 'మీ పశువుల మేత నాణ్యతను తనిఖీ చేయడానికి క్వాలిటీ స్కానర్‌ను ఉపయోగించండి.' : (curL === 'hi' ? 'चारे की गुणवत्ता की जांच के लिए क्वालिटी स्कैनर का उपयोग करें।' : 'Use the Quality Scanner to analyze feed quality, mould, and adulteration.');
            const btnTxt = curL === 'te' ? '📸 మేత స్కానర్ తెరవండి →' : (curL === 'hi' ? '📸 चारा स्कैनर खोलें →' : '📸 Open Feed Scanner →');
            container.innerHTML = `
                <div style="text-align: center; padding: 40px 20px; color: var(--slate-500);">
                    <div style="font-size: 2.4rem; margin-bottom: 8px;">🌾</div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: var(--slate-800); margin-bottom: 6px;">
                        ${emptyTitle}
                    </div>
                    <div style="font-size: 0.85rem; color: var(--slate-500); margin-bottom: 16px;">
                        ${emptySub}
                    </div>
                    <button class="btn btn-primary" onclick="closeMyHistoryModal(); switchTab('scanner');">
                        ${btnTxt}
                    </button>
                </div>
            `;
            return;
        }

        container.innerHTML = '';
        tests.forEach(t => {
            const card = document.createElement('div');
            card.style.cssText = 'background: #FFFFFF; border: 1px solid var(--slate-200); border-radius: 12px; padding: 16px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);';
            const rawDate = t.timestamp || t.created_at || '';
            const dateClean = rawDate.replace('T', ' ').slice(0, 16);
            const score = Math.round(Number(t.quality_score || 0));

            let scoreColor = 'var(--primary-emerald)';
            if (score < 50) scoreColor = 'var(--crimson-danger)';
            else if (score < 80) scoreColor = '#D97706';

            let badgeHtml = t.safety_badge;
            if (!badgeHtml || typeof badgeHtml !== 'string') {
                if (score >= 80 && String(t.overall_risk).toLowerCase() !== 'high') {
                    badgeHtml = '<span class="safety-badge badge-safe">🟢 SAFE</span>';
                } else if (score >= 50 && String(t.overall_risk).toLowerCase() !== 'high') {
                    badgeHtml = '<span class="safety-badge badge-caution">🟡 CAUTION</span>';
                } else {
                    badgeHtml = '<span class="safety-badge badge-danger">🔴 HIGH RISK</span>';
                }
            }

            const shelfDays = t.shelf_life_days !== undefined ? t.shelf_life_days : (t.shelf_life?.shelf_life_days);
            const shelfStatus = t.shelf_life_status || t.shelf_life?.shelf_life_status || 'SAFE';
            let shelfText = `${shelfDays || 0} Days (${shelfStatus})`;
            if (shelfDays === 0 || shelfStatus === 'EXPIRED') {
                shelfText = `⚠️ Expired (0 Days)`;
            }

            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 10px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; color: var(--accent-blue); font-size: 1rem;">${t.batch_id}</span>
                        <span style="font-size: 0.8rem; background: var(--slate-100); color: var(--slate-700); padding: 2px 8px; border-radius: 6px; font-weight: 600;">${t.sample_type || 'Feed'}</span>
                    </div>
                    <div>${badgeHtml}</div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-bottom: 12px; background: var(--slate-50); padding: 10px 14px; border-radius: 8px;">
                    <div>
                        <div style="font-size: 0.72rem; color: var(--slate-500); font-weight: 700;">${curL === 'te' ? 'నాణ్యత స్కోర్' : (curL === 'hi' ? 'गुणवत्ता स्कोर' : 'Quality Score')}</div>
                        <div style="font-size: 1.1rem; font-weight: 900; color: ${scoreColor};">${score} / 100</div>
                    </div>
                    <div>
                        <div style="font-size: 0.72rem; color: var(--slate-500); font-weight: 700;">${curL === 'te' ? 'షెల్ఫ్ లైఫ్' : (curL === 'hi' ? 'शेल्फ लाइफ' : 'Shelf Life')}</div>
                        <div style="font-size: 0.86rem; font-weight: 700; color: var(--slate-800);">${shelfText}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.72rem; color: var(--slate-500); font-weight: 700;">${curL === 'te' ? 'తేదీ / సమయం' : (curL === 'hi' ? 'दिनांक व समय' : 'Timestamp')}</div>
                        <div style="font-size: 0.8rem; color: var(--slate-600); font-family: monospace;">${dateClean}</div>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <div style="font-size: 0.84rem; color: var(--slate-600); flex: 1;">
                        <strong>${curL === 'te' ? 'పరిశీలన:' : (curL === 'hi' ? 'निष्कर्ष:' : 'Findings:')}</strong> ${t.primary_concern || 'Standard Feed Analysis'}
                    </div>
                    <button class="btn btn-sm btn-primary" onclick="viewBatchPassport('${t.batch_id}')" style="padding: 6px 14px; font-size: 0.82rem; white-space: nowrap;">
                        ${curL === 'te' ? '🪪 డిజిటల్ పాస్‌పోర్ట్ చూడండి →' : (curL === 'hi' ? '🪪 डिजिटल पासपोर्ट देखें →' : '🪪 View Digital Passport →')}
                    </button>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (e) {
        container.innerHTML = `<div style="text-align: center; color: var(--crimson-danger); padding: 20px;">Error: ${e.message}</div>`;
    }
}

function closeMyHistoryModal() {
    const modal = document.getElementById('modal-my-history');
    if (modal) modal.style.display = 'none';
}

// ===================================================================
// Cooperative Admin Portal Functions
// ===================================================================

function switchAdminTab(tabKey) {
    state.currentAdminTab = tabKey;
    const tabs = ['overview', 'farmers', 'batches', 'surveillance', 'broadcast', 'standards'];
    tabs.forEach(t => {
        const btn = document.getElementById(`admin-btn-tab-${t}`);
        const view = document.getElementById(`admin-view-${t}`);
        if (btn) btn.classList.toggle('active', t === tabKey);
        if (view) view.style.display = (t === tabKey) ? 'block' : 'none';
    });

    // Synchronize sidebar active highlight
    document.querySelectorAll('#app-nav-menu .nav-item').forEach(item => {
        const t = item.getAttribute('data-admin-tab');
        if (t) item.classList.toggle('active', t === tabKey);
    });
}

async function loadAdminPortalData() {
    try {
        const [kpiResp, farmersResp, batchesResp, survResp, broadResp] = await Promise.all([
            fetch('/api/admin/kpis'),
            fetch('/api/admin/farmers'),
            fetch('/api/admin/batches'),
            fetch('/api/admin/surveillance'),
            fetch('/api/admin/broadcasts')
        ]);

        if (kpiResp.ok) {
            const kpiData = await kpiResp.json();
            const k = kpiData.kpis || {};
            const elFarmers = document.getElementById('admin-kpi-farmers');
            const elCattle = document.getElementById('admin-kpi-cattle');
            const elTests = document.getElementById('admin-kpi-tests');
            const elAlerts = document.getElementById('admin-kpi-alerts');
            const elCompliance = document.getElementById('admin-kpi-compliance');
            const elMilk = document.getElementById('admin-kpi-milk');

            if (elFarmers) elFarmers.innerText = k.total_farmers || 0;
            if (elCattle) elCattle.innerText = k.total_cattle || k.total_animals || 0;
            if (elTests) elTests.innerText = k.total_tests || 0;
            if (elAlerts) elAlerts.innerText = k.high_risk_alerts || 0;
            if (elCompliance) elCompliance.innerText = `${k.compliance_rate !== undefined ? k.compliance_rate : 75.0}%`;
            if (elMilk) elMilk.innerText = `${k.est_milk_litres !== undefined ? k.est_milk_litres : 36} L`;
        }

        if (farmersResp.ok) {
            const fData = await farmersResp.json();
            state.adminFarmers = fData.farmers || [];
            renderAdminFarmersTable(state.adminFarmers);
            populateAdminVillageDropdown(state.adminFarmers);
        }

        if (batchesResp.ok) {
            const bData = await batchesResp.json();
            state.adminBatches = bData.batches || [];
            renderAdminBatchesTable(state.adminBatches);
        }

        if (survResp.ok) {
            const sData = await survResp.json();
            state.adminSurveillance = sData.villages || [];
            renderAdminSurveillanceTable(state.adminSurveillance);
        }

        if (broadResp.ok) {
            const brData = await broadResp.json();
            state.adminBroadcasts = brData.broadcasts || [];
            renderAdminBroadcastsFeed(state.adminBroadcasts);
        }
    } catch (e) {
        console.error('Failed to load admin portal:', e);
    }
}

function populateAdminVillageDropdown(farmers) {
    const sel = document.getElementById('admin-village-filter');
    if (!sel) return;
    const villages = new Set(['Warangal Rural', 'Kankipadu', 'Hanamkonda Dairy Cluster', 'Jangaon Milk Society', 'Narsampet Silage Union', 'Parkal Livestock Zone']);
    farmers.forEach(f => {
        if (f.village_location) villages.add(f.village_location);
    });
    sel.innerHTML = '<option value="all">📍 All Villages</option>';
    villages.forEach(v => {
        sel.innerHTML += `<option value="${v}">${v}</option>`;
    });
}

function renderAdminFarmersTable(farmers) {
    const tbody = document.getElementById('admin-farmers-tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    if (!farmers || farmers.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 20px; color: var(--slate-500);">No matching registered farmers found.</td></tr>';
        return;
    }
    farmers.forEach(f => {
        const tr = document.createElement('tr');
        const fNameEscaped = (f.farmer_name || f.full_name || '').replace(/'/g, "");
        tr.innerHTML = `
            <td style="font-weight: 700; color: var(--slate-900);">👨‍🌾 ${f.farmer_name || f.full_name}</td>
            <td style="font-family: monospace; color: var(--slate-700);">${f.mobile}</td>
            <td>📍 ${f.village_location || 'Rural'}</td>
            <td><strong>${f.cows || 0} Cows</strong>, <strong>${f.buffaloes || 0} Buffaloes</strong> (${f.lactating || 0} Lactating, ${f.pregnant || 0} Pregnant)</td>
            <td>🌾 ${f.main_feed_type || 'Cattle Feed'} / 🏚️ ${f.feed_storage || 'Shed'}</td>
            <td style="font-weight: 800; color: var(--primary-emerald);">${f.test_count || 0}</td>
            <td>
                <button class="btn btn-secondary" style="padding: 4px 10px; font-size: 0.76rem;" onclick="inspectFarmerCattle('${f.user_id}', '${fNameEscaped}')">
                    🐄 Animals
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function filterAdminFarmers() {
    const q = (document.getElementById('admin-farmer-search')?.value || '').toLowerCase().trim();
    const v = (document.getElementById('admin-village-filter')?.value || 'all');

    const filtered = (state.adminFarmers || []).filter(f => {
        const matchName = (f.farmer_name || f.full_name || '').toLowerCase().includes(q);
        const matchPhone = (f.mobile || '').includes(q);
        const matchVillage = (f.village_location || '').toLowerCase().includes(q);
        const matchesText = !q || matchName || matchPhone || matchVillage;

        const matchesVillSelect = (v === 'all') || (f.village_location === v);
        return matchesText && matchesVillSelect;
    });
    renderAdminFarmersTable(filtered);
}

function renderAdminBatchesTable(batches) {
    const tbody = document.getElementById('admin-batches-tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    if (!batches || batches.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; padding: 20px; color: var(--slate-500);">No audit batches recorded.</td></tr>';
        return;
    }
    batches.forEach(b => {
        const tr = document.createElement('tr');
        const score = b.quality_score !== undefined && b.quality_score !== null ? Number(b.quality_score).toFixed(1) : 'N/A';
        const isHighRisk = (b.overall_risk === 'High' || b.adulteration_risk === 'High' || Number(score) < 70);
        const badgeClass = isHighRisk ? 'danger' : 'normal';
        const badgeText = isHighRisk ? '🚨 High Risk' : '🟢 Safe';
        const dt = b.timestamp ? b.timestamp.replace('T', ' ').substring(0, 16) : 'Recent';

        tr.innerHTML = `
            <td><code style="font-weight: 800; color: #1E3A8A;">${b.batch_id}</code></td>
            <td>${b.farmer_name || 'Farmer'} <small style="color: var(--slate-500); display: block;">📍 ${b.village_location || 'Warangal'}</small></td>
            <td>${b.sample_type || 'Feed Pellet'}</td>
            <td style="font-weight: 900; font-size: 1rem; color: ${isHighRisk ? '#DC2626' : '#059669'};">${score} / 100</td>
            <td><span class="admin-status-badge ${badgeClass}">${badgeText}</span></td>
            <td style="font-size: 0.82rem; max-width: 220px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${b.primary_concern || ''}">${b.primary_concern || 'Good Condition'}</td>
            <td style="font-size: 0.82rem;">${b.safe_until_date || '30 Days'}</td>
            <td style="font-size: 0.80rem; color: var(--slate-500);">${dt}</td>
            <td>
                <button class="btn btn-secondary" style="padding: 4px 10px; font-size: 0.74rem;" onclick="viewBatchPassport('${b.batch_id}')">
                    🪪 Passport
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function filterAdminBatches() {
    const q = (document.getElementById('admin-batch-search')?.value || '').toLowerCase().trim();
    const risk = (document.getElementById('admin-batch-risk-filter')?.value || 'all');

    const filtered = (state.adminBatches || []).filter(b => {
        const matchId = (b.batch_id || '').toLowerCase().includes(q);
        const matchFarmer = (b.farmer_name || '').toLowerCase().includes(q);
        const matchType = (b.sample_type || '').toLowerCase().includes(q);
        const matchesText = !q || matchId || matchFarmer || matchType;

        const isHigh = (b.overall_risk === 'High' || b.adulteration_risk === 'High' || Number(b.quality_score) < 70);
        let matchesRisk = true;
        if (risk === 'safe') matchesRisk = !isHigh;
        if (risk === 'high') matchesRisk = isHigh;

        return matchesText && matchesRisk;
    });
    renderAdminBatchesTable(filtered);
}

function exportAdminBatchesCSV() {
    const batches = state.adminBatches || [];
    if (batches.length === 0) {
        alert('No audit batches available to export.');
        return;
    }
    const headers = ['Batch ID', 'Farmer Name', 'Mobile', 'Village', 'Sample Type', 'Quality Score', 'Overall Risk', 'Mould Risk', 'Adulteration Risk', 'Primary Finding', 'Safe Shelf Life', 'Date & Time'];
    const rows = batches.map(b => [
        `"${b.batch_id || ''}"`,
        `"${(b.farmer_name || '').replace(/"/g, '""')}"`,
        `"${b.mobile || ''}"`,
        `"${b.village_location || ''}"`,
        `"${b.sample_type || ''}"`,
        b.quality_score || 0,
        `"${b.overall_risk || ''}"`,
        `"${b.mould_risk || ''}"`,
        `"${b.adulteration_risk || ''}"`,
        `"${(b.primary_concern || '').replace(/"/g, '""')}"`,
        `"${b.safe_until_date || ''}"`,
        `"${b.timestamp || ''}"`
    ]);

    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `SmartFeed_Cooperative_Audit_Report_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function renderAdminSurveillanceTable(villages) {
    const tbody = document.getElementById('admin-surveillance-tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    if (!villages || villages.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 20px; color: var(--slate-500);">No surveillance data.</td></tr>';
        return;
    }
    villages.forEach(v => {
        const tr = document.createElement('tr');
        const st = (v.status || '').toLowerCase();
        let badgeClass = 'normal';
        let badgeText = '🟢 Normal / Safe';
        if (st.includes('attention') || st.includes('watchlist')) {
            badgeClass = 'attention';
            badgeText = '🟡 Attention Needed';
        } else if (st.includes('high') || st.includes('alert') || st.includes('danger')) {
            badgeClass = 'danger';
            badgeText = '🚨 High Risk Alert';
        }

        tr.innerHTML = `
            <td style="font-weight: 700; color: #1E3A8A;">📍 ${v.village}</td>
            <td style="text-align: center; font-weight: 700;">${v.farmer_count || 1}</td>
            <td style="text-align: center;">${v.cattle_count || 3}</td>
            <td style="text-align: center; font-weight: 800;">${v.total_tests || 0}</td>
            <td style="text-align: center; font-weight: 900; color: ${v.high_risk_count > 0 ? '#DC2626' : '#059669'};">${v.high_risk_count || 0}</td>
            <td style="text-align: center; font-weight: 700;">${v.avg_score || 85.0}</td>
            <td><span class="admin-status-badge ${badgeClass}">${badgeText}</span></td>
            <td style="font-size: 0.83rem; color: var(--slate-700);">${v.primary_threat || 'Normal'}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderAdminBroadcastsFeed(broadcasts) {
    const feed = document.getElementById('admin-broadcasts-feed');
    if (!feed) return;
    feed.innerHTML = '';
    if (!broadcasts || broadcasts.length === 0) {
        feed.innerHTML = '<div style="text-align: center; padding: 20px; color: var(--slate-500);">No broadcast advisories dispatched yet.</div>';
        return;
    }
    broadcasts.forEach(b => {
        const div = document.createElement('div');
        const lvl = (b.alert_level || '').toLowerCase();
        const cardClass = lvl.includes('emerg') || lvl.includes('warn') ? 'warning' : 'info';
        const dt = b.created_at ? b.created_at.replace('T', ' ').substring(0, 16) : 'Recent';
        div.className = `admin-bulletin-card ${cardClass}`;
        div.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; margin-bottom: 6px;">
                <strong style="color: var(--slate-900); font-size: 0.95rem;">${b.title}</strong>
                <span class="admin-status-badge ${lvl.includes('emerg') ? 'danger' : (lvl.includes('warn') ? 'attention' : 'normal')}">${b.alert_level || 'Info'}</span>
            </div>
            <p style="font-size: 0.86rem; color: var(--slate-700); margin: 6px 0 8px 0; line-height: 1.45;">${b.message}</p>
            <div style="display: flex; justify-content: space-between; font-size: 0.76rem; color: var(--slate-500);">
                <span>📍 Target: <strong>${b.target_village || 'All Villages'}</strong> • 🏷️ ${b.category || 'Feed Safety'}</span>
                <span>⏱️ ${dt}</span>
            </div>
        `;
        feed.appendChild(div);
    });
}

async function submitAdminBroadcast(e) {
    if (e && e.preventDefault) e.preventDefault();
    const title = document.getElementById('admin-bc-title')?.value;
    const target = document.getElementById('admin-bc-target')?.value;
    const level = document.getElementById('admin-bc-level')?.value;
    const category = document.getElementById('admin-bc-category')?.value;
    const message = document.getElementById('admin-bc-msg')?.value;

    if (!title || !message) {
        alert('Please provide both an Alert Title and an Advisory Message.');
        return;
    }

    try {
        const resp = await fetch('/api/admin/broadcast', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: title,
                target_village: target,
                alert_level: level,
                category: category,
                message: message,
                language: 'te'
            })
        });
        const res = await resp.json();
        if (resp.ok) {
            alert('📢 Cooperative Advisory Broadcast dispatched successfully to all village dairy farmers!');
            document.getElementById('admin-broadcast-form')?.reset();
            // Refresh broadcasts
            const bResp = await fetch('/api/admin/broadcasts');
            if (bResp.ok) {
                const bData = await bResp.json();
                state.adminBroadcasts = bData.broadcasts || [];
                renderAdminBroadcastsFeed(state.adminBroadcasts);
            }
        } else {
            alert(`Failed to dispatch: ${res.detail || 'Server error'}`);
        }
    } catch (err) {
        alert(`Error dispatching advisory: ${err.message}`);
    }
}

async function inspectFarmerCattle(userId, farmerName) {
    try {
        const resp = await fetch(`/api/farmer/animals?user_id=${userId}`);
        if (!resp.ok) return;
        const data = await resp.json();
        state.farmerAnimals = data.animals || [];
        openMyAnimalsModal();
    } catch (e) {
        alert(`Failed to load animals: ${e.message}`);
    }
}

// Expose globals for inline HTML event handlers
window.openAuthModal = openAuthModal;
window.closeAuthModal = closeAuthModal;
window.switchAuthTab = switchAuthTab;
window.handleLoginSubmit = handleLoginSubmit;
window.handleRegisterSubmit = handleRegisterSubmit;
window.prefillAdminLogin = prefillAdminLogin;
window.quickLoginDemoFarmer = quickLoginDemoFarmer;
window.quickLoginDemoAdmin = quickLoginDemoAdmin;
window.logoutUser = logoutUser;
window.startFarmSetupWizard = startFarmSetupWizard;
window.closeWizardModal = closeWizardModal;
window.proceedToWizardStep = proceedToWizardStep;
window.incrementAnimalCount = incrementAnimalCount;
window.decrementAnimalCount = decrementAnimalCount;
window.validateAnimalTypes = validateAnimalTypes;
window.onAnimalTypeChange = onAnimalTypeChange;
window.onAnimalStatusChange = onAnimalStatusChange;
window.submitFarmOnboarding = submitFarmOnboarding;
window.loadFarmerDashboardData = loadFarmerDashboardData;
window.openMyAnimalsModal = openMyAnimalsModal;
window.closeMyAnimalsModal = closeMyAnimalsModal;
window.openFeedDiaryModal = openFeedDiaryModal;
window.closeFeedDiaryModal = closeFeedDiaryModal;
window.openMyHistoryModal = openMyHistoryModal;
window.closeMyHistoryModal = closeMyHistoryModal;
window.renderFarmerHistoryTable = renderFarmerHistoryTable;
window.handleTile7Click = handleTile7Click;
window.viewBatchPassport = viewBatchPassport;
window.loadAdminPortalData = loadAdminPortalData;
window.inspectFarmerCattle = inspectFarmerCattle;
window.switchAdminTab = switchAdminTab;
window.filterAdminFarmers = filterAdminFarmers;
window.filterAdminBatches = filterAdminBatches;
window.exportAdminBatchesCSV = exportAdminBatchesCSV;
window.submitAdminBroadcast = submitAdminBroadcast;
window.setupAnimalRecommendation = setupAnimalRecommendation;
window.loadFarmerAnimalPills = loadFarmerAnimalPills;
window.selectAnimalPill = selectAnimalPill;
window.onRecAnimalTypeChange = onRecAnimalTypeChange;
window.onRecStageChange = onRecStageChange;
window.updateRecMilkBadge = updateRecMilkBadge;
window.recalculateAnimalRecommendation = recalculateAnimalRecommendation;
window.renderAnimalRecommendation = renderAnimalRecommendation;
window.speakAnimalRecommendation = speakAnimalRecommendation;

// ===================================================================
// Initialization & Navigation
// ===================================================================
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initDropzones();
    initLanguageSelectors();

    // Check if saved user session exists in active session; if not, enforce entry stage gating
    try {
        const sessionActive = sessionStorage.getItem('smartfeed_session_active');
        const savedUser = localStorage.getItem('smartfeed_user');
        if (sessionActive === '1' && savedUser) {
            const user = JSON.parse(savedUser);
            unlockAppWorkspace(user);
        } else {
            lockAppWorkspace();
        }
    } catch (e) {
        lockAppWorkspace();
    }

    // Defeat any aggressive browser password manager autofill on load
    [50, 150, 300, 600].forEach(delay => {
        setTimeout(() => {
            const m = document.getElementById('entry-login-mobile');
            const p = document.getElementById('entry-login-password');
            if (m && !m.matches(':focus')) m.value = '';
            if (p && !p.matches(':focus')) p.value = '';
        }, delay);
    });

    runAdulterationCheck(); // initial run with default values
    runSafeUreaCalculator(); // initial run with default ICAR straw values

    // Retrieve saved language or default to Telugu
    const savedLang = localStorage.getItem('smartfeed_lang') || 'te';
    selectEntryLanguage(savedLang);

    // Demo Scan Auto-Execution for Automated UI Testing & Headless Inspection
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('demo_scan') === '1') {
        setTimeout(async () => {
            quickLoginDemoFarmer();
            setTimeout(async () => {
                switchTab('scanner');
                const sel = document.getElementById('preset-sample-select');
                if (sel) {
                    sel.value = 'sample_healthy_feed.jpg';
                    handlePresetSelect();
                    await runFeedScan();
                    setTimeout(() => {
                        const el = document.getElementById('animal-rec-card');
                        if (el) el.scrollIntoView({ behavior: 'instant', block: 'center' });
                    }, 500);
                }
            }, 600);
        }, 600);
    }
});

// Expose entry functions globally
window.startTheAppDirectly = startTheAppDirectly;
window.selectSplashLang = selectSplashLang;
window.goToEntryScreen = goToEntryScreen;
window.selectEntryLanguage = selectEntryLanguage;
window.switchEntryAuthTab = switchEntryAuthTab;
window.handleEntryLoginSubmit = handleEntryLoginSubmit;
window.handleEntryRegisterSubmit = handleEntryRegisterSubmit;
window.prefillAdminLogin = prefillAdminLogin;
window.quickLoginDemoAdmin = quickLoginDemoAdmin;
window.quickLoginDemoFarmer = quickLoginDemoFarmer;
window.quickLoginGuest = quickLoginGuest;
window.logoutUser = logoutUser;
window.unlockAppWorkspace = unlockAppWorkspace;
window.lockAppWorkspace = lockAppWorkspace;
window.renderSidebarNav = renderSidebarNav;
window.switchAdminSubView = switchAdminSubView;
window.switchAdminTab = switchAdminTab;
window.handleLanguageSelectChange = handleLanguageSelectChange;

function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const targetTab = item.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });
}

function switchTab(tabId) {
    state.currentTab = tabId;

    // Update Sidebar Nav UI
    document.querySelectorAll('.nav-item').forEach(item => {
        if (item.getAttribute('data-tab') === tabId) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });

    // Update Tab Content Panels
    document.querySelectorAll('.tab-content').forEach(panel => {
        if (panel.id === `tab-${tabId}`) {
            panel.classList.add('active');
        } else {
            panel.classList.remove('active');
        }
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Refresh Dashboard if switching to Dashboard tab
    if (tabId === 'dashboard') {
        setTimeout(() => {
            loadDashboardData();
        }, 50);
    }
}

function handleLanguageSelectChange(lang) {
    if (!lang) return;
    setLanguage(lang);
}

function initLanguageSelectors() {
    const langSelect = document.getElementById('global-language-select');
    if (langSelect) {
        langSelect.value = state.language;
        langSelect.addEventListener('change', (e) => {
            handleLanguageSelectChange(e.target.value);
        });
    }

    const topLangSelect = document.getElementById('top-language-select');
    if (topLangSelect) {
        topLangSelect.value = state.language;
        topLangSelect.addEventListener('change', (e) => {
            handleLanguageSelectChange(e.target.value);
        });
    }

    const mobileLangSelect = document.getElementById('mobile-language-select');
    if (mobileLangSelect) {
        mobileLangSelect.value = state.language;
        mobileLangSelect.addEventListener('change', (e) => {
            handleLanguageSelectChange(e.target.value);
        });
    }

    const providerSelect = document.getElementById('global-advisory-provider');
    if (providerSelect) {
        providerSelect.addEventListener('change', (e) => {
            state.advisoryMode = e.target.value;
            fetchAdvisoryForCurrentState(state.language);
        });
    }
}

function setLanguage(lang) {
    state.language = lang;
    try {
        localStorage.setItem('smartfeed_lang', lang);
    } catch (e) {}

    const langSelect = document.getElementById('global-language-select');
    if (langSelect && langSelect.value !== lang) langSelect.value = lang;

    const topLangSelect = document.getElementById('top-language-select');
    if (topLangSelect && topLangSelect.value !== lang) topLangSelect.value = lang;

    const mobileLangSelect = document.getElementById('mobile-language-select');
    if (mobileLangSelect && mobileLangSelect.value !== lang) mobileLangSelect.value = lang;

    // Apply entire application localization
    applyAppLanguage(lang);

    // Refresh Sidebar with current user role
    const currentRole = (state.currentUser && state.currentUser.role) ? state.currentUser.role : 'farmer';
    renderSidebarNav(currentRole);

    // Update advisory headers, problem statements, and symptom chips in new language
    updateAdvisoryHeaders(lang);
    loadFarmerProblemStatements(lang);
    renderSymptomChips(lang);
    if (state.advisoryInputMode === 'manual') {
        const manualInput = document.getElementById('manual-problem-input');
        if (manualInput && manualInput.value.trim().length > 0) {
            runManualAdvisoryAnalysis();
        }
    }

    // Refresh Safe Urea Calculator localized advisory
    if (typeof runSafeUreaCalculator === 'function') {
        runSafeUreaCalculator();
    }
}

// ===================================================================
// Dropzone & File Handling
// ===================================================================
function initDropzones() {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('file-input');

    if (dropzone && fileInput) {
        dropzone.addEventListener('click', () => fileInput.click());

        ['dragenter', 'dragover'].forEach(eventName => {
            dropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropzone.classList.add('dragover');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropzone.classList.remove('dragover');
            });
        });

        dropzone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            if (dt.files && dt.files.length > 0) {
                processImageFile(dt.files[0]);
            }
        });
    }

    // QR Lookup Dropzone
    const qrDropzone = document.getElementById('qr-dropzone');
    const qrInput = document.getElementById('qr-file-input');
    if (qrDropzone && qrInput) {
        qrDropzone.addEventListener('click', () => qrInput.click());
        ['dragenter', 'dragover'].forEach(eventName => {
            qrDropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                qrDropzone.classList.add('dragover');
            });
        });
        ['dragleave', 'drop'].forEach(eventName => {
            qrDropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                qrDropzone.classList.remove('dragover');
            });
        });
        qrDropzone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            if (dt.files && dt.files.length > 0) {
                handleQRUpload({ target: { files: dt.files } });
            }
        });
    }
}

function handleFileSelect(event) {
    if (event.target.files && event.target.files.length > 0) {
        processImageFile(event.target.files[0]);
    }
}

function processImageFile(file) {
    state.selectedFile = file;
    state.selectedPreset = '';
    const presetSelect = document.getElementById('preset-sample-select');
    if (presetSelect) presetSelect.value = '';

    const reader = new FileReader();
    reader.onload = (e) => {
        showPreview(e.target.result);
    };
    reader.readAsDataURL(file);
}

function handlePresetSelect() {
    const presetSelect = document.getElementById('preset-sample-select');
    const filename = presetSelect.value;
    if (!filename) return;

    state.selectedPreset = filename;
    state.selectedFile = null;
    const fileInput = document.getElementById('file-input');
    if (fileInput) fileInput.value = '';

    const previewUrl = `/api/sample-image/${filename}`;
    showPreview(previewUrl);

    // Auto-adjust sliders to match preset reality
    if (filename.includes('mouldy')) {
        setSliderVal('cp', 14);
        setSliderVal('moisture', 22);
        setSliderVal('days', 15);
        document.getElementById('check-smell').checked = true;
    } else if (filename.includes('healthy')) {
        setSliderVal('cp', 22);
        setSliderVal('moisture', 9.5);
        setSliderVal('days', 3);
        document.getElementById('check-smell').checked = false;
    } else if (filename.includes('burnt')) {
        setSliderVal('cp', 17);
        setSliderVal('moisture', 7.0);
        setSliderVal('days', 8);
        document.getElementById('check-smell').checked = true;
    } else if (filename.includes('silage')) {
        document.getElementById('scanner-sample-type').value = 'Maize Silage';
        setSliderVal('cp', 8.5);
        setSliderVal('moisture', 65);
        setSliderVal('days', 10);
        document.getElementById('check-smell').checked = false;
    }
}

function showPreview(src) {
    const wrapper = document.getElementById('preview-wrapper');
    const img = document.getElementById('preview-img');
    if (wrapper && img) {
        img.src = src;
        wrapper.style.display = 'flex';
    }
}

function updateSliderBadge(key, val, unit) {
    const badge = document.getElementById(`val-${key}`);
    if (badge) badge.innerText = `${val}${unit}`;
}

function setSliderVal(key, val) {
    const slider = document.getElementById(`slider-${key}`);
    if (slider) {
        slider.value = val;
        updateSliderBadge(key, val, key === 'days' ? ' Days' : '%');
    }
}

// ===================================================================
// Feed Scanner Execution (API -> /api/scan)
// ===================================================================
async function runFeedScan() {
    if (!state.selectedFile && !state.selectedPreset) {
        alert('Please choose a preset demo image or upload a feed sample image first!');
        return;
    }

    const btn = document.getElementById('btn-scan');
    btn.disabled = true;
    btn.innerHTML = '⏳ Analyzing Feed Quality & Risks...';

    const formData = new FormData();
    if (state.selectedFile) {
        formData.append('file', state.selectedFile);
    } else if (state.selectedPreset) {
        formData.append('preset_sample', state.selectedPreset);
    }

    formData.append('sample_type', document.getElementById('scanner-sample-type').value);
    formData.append('crude_protein', document.getElementById('slider-cp').value);
    formData.append('moisture', document.getElementById('slider-moisture').value);
    formData.append('fiber', 12.0);
    formData.append('npn', document.getElementById('slider-npn').value);
    formData.append('adulterant_powder', 0.0);
    formData.append('storage_temp', 25.0);
    formData.append('storage_humidity', 60.0);
    formData.append('storage_days', document.getElementById('slider-days').value);
    formData.append('smell_abnormal', document.getElementById('check-smell').checked);
    formData.append('language', state.language);
    formData.append('advisory_mode', state.advisoryMode);
    if (state.currentUser && state.currentUser.id) {
        formData.append('user_id', state.currentUser.id);
    }

    try {
        const resp = await fetch('/api/scan', {
            method: 'POST',
            body: formData
        });

        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(err.detail || 'Scan processing failed.');
        }

        const data = await resp.json();
        state.currentScanResult = data;
        renderScanResults(data);

        // Refresh farmer dashboard & live history records immediately
        if (state.currentUser && state.currentUser.role === 'farmer') {
            loadFarmerDashboardData();
        }
        loadDashboardData();

    } catch (err) {
        alert(`Diagnostic Error: ${err.message}`);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '🚀 Run Full Diagnostic Scan';
    }
}

function renderScanResults(data) {
    document.getElementById('results-placeholder').style.display = 'none';
    document.getElementById('results-content').style.display = 'block';

    const score = data.health_score;
    const badge = data.safety_badge;
    const concern = data.primary_concern;
    const deductions = data.itemized_deductions || [];
    const cv = data.cv_metrics || {};

    // 1. Animate SVG Radial Score Gauge
    const circle = document.getElementById('gauge-circle');
    const scoreVal = document.getElementById('gauge-score-val');
    const badgeElem = document.getElementById('gauge-badge');
    const badgeText = document.getElementById('gauge-badge-text');
    const concernElem = document.getElementById('gauge-concern');

    const circumference = 439.82;
    const offset = circumference - (score / 100) * circumference;
    circle.style.strokeDashoffset = offset;
    scoreVal.innerText = Math.round(score);

    badgeElem.className = 'safety-badge';
    if (score >= 80 && data.risk_level !== 'High') {
        circle.setAttribute('stroke', '#10B981');
        badgeElem.classList.add('badge-safe');
        badgeElem.children[0].innerText = '🟢';
        badgeText.innerText = 'SAFE FOR USE';
    } else if (score >= 50 && data.risk_level !== 'High') {
        circle.setAttribute('stroke', '#F59E0B');
        badgeElem.classList.add('badge-attention');
        badgeElem.children[0].innerText = '🟡';
        badgeText.innerText = 'NEEDS ATTENTION';
    } else {
        circle.setAttribute('stroke', '#EF4444');
        badgeElem.classList.add('badge-danger');
        badgeElem.children[0].innerText = '🔴';
        badgeText.innerText = 'HIGH RISK - DO NOT FEED';
    }

    concernElem.innerHTML = `<b>Primary Concern:</b> ${concern}`;

    // 2. Populate Explainable AI Deductions List
    const deductionsList = document.getElementById('deductions-list');
    deductionsList.innerHTML = '';
    if (deductions.length === 0) {
        deductionsList.innerHTML = `
            <div class="deduction-item">
                <div>
                    <div class="deduction-name">All Quality Parameters Optimal</div>
                    <div class="deduction-desc">No visual, fungal, or adulteration penalties detected.</div>
                </div>
                <div class="deduction-points points-clean">0 pts</div>
            </div>
        `;
    } else {
        deductions.forEach(item => {
            const div = document.createElement('div');
            div.className = 'deduction-item';
            div.innerHTML = `
                <div>
                    <div class="deduction-name">${item.factor}</div>
                    <div class="deduction-desc">${item.detail}</div>
                </div>
                <div class="deduction-points points-penalty">-${item.points_deducted} pts</div>
            `;
            deductionsList.appendChild(div);
        });
    }

    // 3. Populate Computer Vision Metrics
    const cvGrid = document.getElementById('cv-metrics-grid');
    cvGrid.innerHTML = `
        <div class="telemetry-card">
            <div>
                <div class="telemetry-label">Mould Colony %</div>
                <div class="telemetry-val">${(cv.mould_percentage || 0).toFixed(1)}%</div>
            </div>
        </div>
        <div class="telemetry-card">
            <div>
                <div class="telemetry-label">Discoloration</div>
                <div class="telemetry-val">${(cv.discoloration_percentage || 0).toFixed(1)}%</div>
            </div>
        </div>
        <div class="telemetry-card">
            <div>
                <div class="telemetry-label">Foreign Particles</div>
                <div class="telemetry-val">${cv.foreign_particles || 0} found</div>
            </div>
        </div>
        <div class="telemetry-card">
            <div>
                <div class="telemetry-label">Visual Texture</div>
                <div class="telemetry-val">${cv.texture_roughness || 'Normal'}</div>
            </div>
        </div>
    `;

    // 4. Update Shelf-Life & Spoilage Forecast Widget
    renderShelfLifeForecast(data.shelf_life);

    // 5. Update Digital Passport Card Preview
    document.getElementById('passport-batch-id-display').innerText = data.batch_id;
    updatePassportCard(data);

    // 6. Enrich advisory with Shelf Life Voice Announcement & update Advisory Tab
    if (data.shelf_life) {
        const days = data.shelf_life.shelf_life_days;
        const st = data.shelf_life.shelf_life_status;
        let shelfVoice = '';
        if (days === 0 || st === 'EXPIRED') {
            if (state.language === 'te') {
                shelfVoice = 'హెచ్చరిక: ఈ మేత ఇప్పటికే పాడైపోయింది, బూజు పట్టింది. పశువులకు పెట్టవద్దు.';
            } else if (state.language === 'hi') {
                shelfVoice = 'चेतावनी: यह चारा पहले से ही खराब हो चुका है। मवेशियों को न खिलाएं।';
            } else {
                shelfVoice = 'CRITICAL ALERT: Feed is already spoiled and hazardous. Do not feed to cattle.';
            }
        } else {
            if (state.language === 'te') {
                shelfVoice = `నిల్వ కాలం అంచనా: ఈ మేత సుమారు ${days} రోజుల వరకు సురక్షితంగా ఉంటుంది.`;
            } else if (state.language === 'hi') {
                shelfVoice = `शेल्फ लाइफ: यह चारा लगभग ${days} दिनों तक सुरक्षित रहेगा।`;
            } else {
                shelfVoice = `Shelf Life Forecast: This feed is safe for approximately ${days} more days.`;
            }
        }
        if (data.advisory) {
            data.advisory.full_advisory_text = `${shelfVoice}\n\n${data.advisory.full_advisory_text || ''}`;
        }
    }
    updateAdvisoryView(data.advisory);

    // 7. Setup & Render Animal-Specific Recommendation
    setupAnimalRecommendation(data);
}

function renderShelfLifeForecast(shelf) {
    const card = document.getElementById('shelf-life-card');
    if (!card) return;
    if (!shelf) {
        card.style.display = 'none';
        return;
    }
    card.style.display = 'block';

    const daysNum = document.getElementById('shelf-days-num');
    const badge = document.getElementById('shelf-life-badge');
    const untilDate = document.getElementById('shelf-until-date');
    const moistStatus = document.getElementById('shelf-moist-status');
    const progressBar = document.getElementById('shelf-progress-bar');
    const actionBox = document.getElementById('shelf-action-box');
    const actionIcon = document.getElementById('shelf-action-icon');
    const actionText = document.getElementById('shelf-action-text');

    const safeDays = Math.max(0, Math.round(shelf.shelf_life_days || 0));
    const status = shelf.shelf_life_status || 'SAFE';
    const maxBaseline = shelf.max_baseline_days || 75;

    if (daysNum) daysNum.innerText = safeDays;
    if (untilDate) untilDate.innerText = shelf.safe_until_date || 'Today';
    if (moistStatus) moistStatus.innerText = shelf.moisture_multiplier_label || `${shelf.moisture_impact || 'Normal'} (${shelf.moisture_multiplier || 1.0}x)`;

    badge.className = 'shelf-badge';
    actionBox.className = 'shelf-action-box';

    let fillPct = Math.min(100, Math.max(5, (safeDays / maxBaseline) * 100));

    if (status === 'EXPIRED' || safeDays === 0) {
        badge.classList.add('badge-shelf-expired');
        badge.innerText = state.language === 'te' ? '⚠️ గడువు ముగిసింది' : (state.language === 'hi' ? '⚠️ समाप्त / खराब' : '⚠️ EXPIRED');
        progressBar.style.width = '100%';
        progressBar.style.background = 'linear-gradient(90deg, #EF4444 0%, #B91C1C 100%)';
        actionBox.classList.add('action-expired');
        if (actionIcon) actionIcon.innerText = '🚫';
        if (actionText) {
            actionText.innerText = state.language === 'te'
                ? 'హెచ్చరిక: ఈ మేత ఇప్పటికే పాడైపోయింది లేదా బూజు పట్టింది. పశువులకు పెట్టవద్దు - అనారోగ్యం, విరేచనాలు మరియు పాల దిగుబడి తగ్గే ప్రమాదం ఉంది.'
                : (state.language === 'hi'
                    ? 'चेतावनी: यह चारा पहले से ही खराब या फफूंदयुक्त है। मवेशियों को न खिलाएं - दस्त, बीमारी और दूध उत्पादन में गिरावट का भारी खतरा है।'
                    : 'CRITICAL ALERT: Feed is already spoiled or visibly infested with mould. DO NOT FEED to livestock.');
        }
    } else if (status === 'CRITICAL' || safeDays <= 3) {
        badge.classList.add('badge-shelf-critical');
        badge.innerText = state.language === 'te' ? '⚠️ తీవ్ర ప్రమాదం' : (state.language === 'hi' ? '⚠️ गंभीर' : '⚠️ CRITICAL (≤3 Days)');
        progressBar.style.width = `${Math.max(15, fillPct)}%`;
        progressBar.style.background = 'linear-gradient(90deg, #F87171 0%, #EF4444 100%)';
        actionBox.classList.add('action-critical');
        if (actionIcon) actionIcon.innerText = '⚡';
        if (actionText) {
            actionText.innerText = state.language === 'te'
                ? `త్వరపడండి: మేత కేవలం ${safeDays} రోజులు మాత్రమే బాగుంటుంది. తేమ ఎక్కువగా ఉన్నందున వెంటనే వాడేయండి లేదా ఎండబెట్టండి.`
                : (state.language === 'hi'
                    ? `शीघ्र उपयोग करें: चारा केवल ${safeDays} दिनों तक सुरक्षित है। उच्च नमी के कारण तुरंत खिलाएं या सुखाएं।`
                    : `URGENT ACTION: Only ${safeDays} safe days remaining. Feed immediately or sun-dry to avert rapid fungal bloom.`);
        }
    } else if (status === 'ATTENTION' || safeDays <= 12) {
        badge.classList.add('badge-shelf-attention');
        badge.innerText = state.language === 'te' ? '🟡 జాగ్రత్త' : (state.language === 'hi' ? '🟡 ध्यान दें' : '🟡 ATTENTION');
        progressBar.style.width = `${fillPct}%`;
        progressBar.style.background = 'linear-gradient(90deg, #FBBF24 0%, #D97706 100%)';
        actionBox.classList.add('action-attention');
        if (actionIcon) actionIcon.innerText = '⚠️';
        if (actionText) {
            actionText.innerText = state.language === 'te'
                ? `జాగ్రత్త: ఈ మేత దాదాపు ${safeDays} రోజుల పాటు నిల్వ ఉంటుంది. గాలి ఆడేలా, నేల తగలకుండా ప్యాలెట్లపై భద్రపరచండి.`
                : (state.language === 'hi'
                    ? `सावधानी: यह चारा लगभग ${safeDays} दिनों तक सुरक्षित है। हवादार जगह व लकड़ी के तख्तों पर रखें।`
                    : `CAUTION: Feed has ~${safeDays} days of storage life. Ensure adequate ventilation and elevate off damp floors.`);
        }
    } else {
        badge.classList.add('badge-shelf-safe');
        badge.innerText = state.language === 'te' ? '🟢 సురక్షితం' : (state.language === 'hi' ? '🟢 सुरक्षित' : '🟢 SAFE & FRESH');
        progressBar.style.width = `${fillPct}%`;
        progressBar.style.background = 'linear-gradient(90deg, #10B981 0%, #059669 100%)';
        if (actionIcon) actionIcon.innerText = '✅';
        if (actionText) {
            actionText.innerText = state.language === 'te'
                ? `అద్భుతం: మేత తేమ తక్కువగా ఉండి దాదాపు ${safeDays} రోజుల పాటు (${shelf.safe_until_date || ''} వరకు) సురక్షితంగా ఉంటుంది. తేమ తగలకుండా భద్రపరచండి.`
                : (state.language === 'hi'
                    ? `उत्कृष्ट: चारा अच्छी स्थिति में है और लगभग ${safeDays} दिनों तक (${shelf.safe_until_date || ''} तक) सुरक्षित रहेगा। सीलन से बचाएं।`
                    : `OPTIMAL: Low moisture and clean appearance. Safe for ~${safeDays} days (until ${shelf.safe_until_date || 'forecast date'}). Store in a cool, dry place.`);
        }
    }
}

// ===================================================================
// Animal-Specific Feed Recommendation & Dosage Controller
// ===================================================================

let activeSelectedAnimalIdx = -1;

function setupAnimalRecommendation(scanData) {
    const card = document.getElementById('animal-rec-card');
    if (!card) return;
    card.style.display = 'block';

    // 1. Render herd quick-pick pills from farmer's registered animals
    loadFarmerAnimalPills();

    // 2. If scan response already included recommendation, render it directly
    if (scanData && scanData.animal_recommendation) {
        renderAnimalRecommendation(scanData.animal_recommendation);
    } else {
        recalculateAnimalRecommendation();
    }
}

function loadFarmerAnimalPills() {
    const container = document.getElementById('animal-herd-pills-container');
    if (!container) return;
    container.innerHTML = '';

    const animals = state.farmerAnimals || [];

    if (animals.length > 0) {
        animals.forEach((a, idx) => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = `animal-pick-pill ${idx === activeSelectedAnimalIdx ? 'active' : ''}`;
            const isCow = (a.animal_type || 'Cow').toLowerCase().includes('cow');
            const icon = isCow ? '🐄' : '🐃';
            const name = a.animal_name || `${isCow ? 'Cow' : 'Buffalo'} #${idx + 1}`;
            const status = a.lactation_status || 'Lactating';
            const milk = a.milk_production || '';
            btn.style.cssText = `padding: 6px 12px; border-radius: 20px; font-size: 0.80rem; font-weight: 700; cursor: pointer; transition: all 0.2s; border: 1.5px solid ${idx === activeSelectedAnimalIdx ? '#10B981' : '#CBD5E1'}; background: ${idx === activeSelectedAnimalIdx ? '#ECFDF5' : '#FFFFFF'}; color: ${idx === activeSelectedAnimalIdx ? '#065F46' : '#334155'}; display: flex; align-items: center; gap: 6px;`;
            btn.innerHTML = `<span>${icon}</span> <span>${name}</span> <span style="opacity: 0.75; font-size: 0.74rem;">(${status}${status === 'Lactating' && milk ? ', ' + milk : ''})</span>`;
            btn.onclick = () => selectAnimalPill(idx, a);
            container.appendChild(btn);
        });
    }

    // Always add a "Custom Animal / ప్రత్యేకం" pill at the end
    const customBtn = document.createElement('button');
    customBtn.type = 'button';
    customBtn.className = `animal-pick-pill ${activeSelectedAnimalIdx === -1 ? 'active' : ''}`;
    customBtn.style.cssText = `padding: 6px 12px; border-radius: 20px; font-size: 0.80rem; font-weight: 700; cursor: pointer; transition: all 0.2s; border: 1.5px solid ${activeSelectedAnimalIdx === -1 && animals.length === 0 ? '#10B981' : '#CBD5E1'}; background: ${activeSelectedAnimalIdx === -1 && animals.length === 0 ? '#ECFDF5' : '#FFFFFF'}; color: #334155; display: flex; align-items: center; gap: 6px;`;
    customBtn.innerHTML = `<span>➕</span> <span>${state.language === 'te' ? 'కస్టమ్ పశువు' : (state.language === 'hi' ? 'कस्टम मवेशी' : 'Custom Animal')}</span>`;
    customBtn.onclick = () => selectAnimalPill(-1, null);
    container.appendChild(customBtn);
}

function selectAnimalPill(idx, animal) {
    activeSelectedAnimalIdx = idx;
    loadFarmerAnimalPills();

    if (animal) {
        const typeSelect = document.getElementById('rec-animal-type');
        const stageSelect = document.getElementById('rec-lactation-stage');
        const slider = document.getElementById('slider-rec-milk');

        if (typeSelect) {
            typeSelect.value = (animal.animal_type || 'Cow').includes('Buffalo') ? 'Buffalo' : 'Cow';
        }
        if (stageSelect) {
            let st = animal.lactation_status || 'Lactating';
            if (st.includes('Pregnant')) stageSelect.value = 'Pregnant';
            else if (st.includes('Dry')) stageSelect.value = 'Dry';
            else stageSelect.value = 'Lactating';
        }
        onRecStageChange();

        if (slider && animal.milk_production) {
            const matches = String(animal.milk_production).match(/\d+/g);
            if (matches && matches.length > 0) {
                const val = parseFloat(matches[0]);
                slider.value = val;
                updateRecMilkBadge(val);
            }
        }
    }
    recalculateAnimalRecommendation();
}

function onRecAnimalTypeChange() {
    recalculateAnimalRecommendation();
}

function onRecStageChange() {
    const stage = document.getElementById('rec-lactation-stage')?.value || 'Lactating';
    const milkGroup = document.getElementById('rec-milk-yield-group');
    if (milkGroup) {
        if (stage === 'Lactating') {
            milkGroup.style.opacity = '1';
            milkGroup.style.pointerEvents = 'auto';
            document.getElementById('slider-rec-milk').disabled = false;
        } else {
            milkGroup.style.opacity = '0.4';
            milkGroup.style.pointerEvents = 'none';
            document.getElementById('slider-rec-milk').disabled = true;
        }
    }
    recalculateAnimalRecommendation();
}

function updateRecMilkBadge(val) {
    const badge = document.getElementById('val-rec-milk');
    if (badge) badge.innerText = `${val} L/day`;
}

async function recalculateAnimalRecommendation() {
    const btn = document.getElementById('btn-recalculate-rec');
    if (btn) btn.disabled = true;

    const animalType = document.getElementById('rec-animal-type')?.value || 'Cow';
    const stage = document.getElementById('rec-lactation-stage')?.value || 'Lactating';
    const milkYield = (stage === 'Lactating') ? parseFloat(document.getElementById('slider-rec-milk')?.value || 8) : 0.0;

    const scan = state.currentScanResult || {};
    const sampleType = document.getElementById('scanner-sample-type')?.value || scan.sample_type || 'Cattle Feed Pellet';
    const healthScore = scan.health_score !== undefined ? scan.health_score : 85.0;
    const overallRisk = scan.risk_level || 'Low';
    const mouldRisk = scan.cv_metrics?.mould_percentage > 5 ? 'High' : (scan.cv_metrics?.mould_percentage > 1 ? 'Medium' : 'Low');
    const adultRisk = scan.adulteration?.adulteration_risk || 'Low';
    const cp = parseFloat(document.getElementById('slider-cp')?.value || 20.0);
    const moist = parseFloat(document.getElementById('slider-moisture')?.value || 10.0);
    const shelfDays = scan.shelf_life?.shelf_life_days !== undefined ? scan.shelf_life.shelf_life_days : 14;

    const payload = {
        feed_diagnostics: {
            sample_type: sampleType,
            health_score: healthScore,
            overall_risk: overallRisk,
            mould_risk: mouldRisk,
            adulteration_risk: adultRisk,
            crude_protein: cp,
            moisture: moist,
            shelf_life_days: shelfDays
        },
        animal_params: {
            animal_type: animalType,
            lactation_stage: stage,
            milk_yield_litres: milkYield,
            body_weight_kg: animalType === 'Buffalo' ? 500 : 400
        },
        language: state.language || 'te'
    };

    try {
        const resp = await fetch('/api/animal-recommendation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (!resp.ok) throw new Error('Recommendation computation failed');
        const data = await resp.json();
        renderAnimalRecommendation(data);
    } catch (e) {
        console.error('Failed to compute animal recommendation:', e);
    } finally {
        if (btn) btn.disabled = false;
    }
}

function renderAnimalRecommendation(data) {
    state.currentAnimalRecommendation = data;
    const box = document.getElementById('animal-rec-results-box');
    if (!box) return;
    box.style.display = 'block';

    // 1. Verdict Banner
    const banner = document.getElementById('rec-verdict-banner');
    const icon = document.getElementById('rec-verdict-icon');
    const title = document.getElementById('rec-verdict-title');
    const note = document.getElementById('rec-verdict-note');

    if (data.suitability_code === 'REJECTED_UNSAFE') {
        banner.style.background = '#FEF2F2';
        banner.style.borderColor = '#EF4444';
        icon.innerText = '🔴';
        title.style.color = '#991B1B';
        note.style.color = '#B91C1C';
    } else if (data.suitability_code === 'CAUTION_CONDITIONAL') {
        banner.style.background = '#FFFBEB';
        banner.style.borderColor = '#F59E0B';
        icon.innerText = '🟡';
        title.style.color = '#92400E';
        note.style.color = '#B45309';
    } else {
        banner.style.background = '#ECFDF5';
        banner.style.borderColor = '#10B981';
        icon.innerText = '✅';
        title.style.color = '#065F46';
        note.style.color = '#047857';
    }

    title.innerText = data.headline || (data.is_safe ? 'Feed is Suitable' : 'Feed is Unsafe');
    note.innerText = data.suitability_note || '';

    // 2. Dosage Breakdown
    const valDaily = document.getElementById('rec-val-daily-dose');
    const valMorn = document.getElementById('rec-val-morning-dose');
    const valEve = document.getElementById('rec-val-evening-dose');

    if (valDaily) valDaily.innerText = `${data.recommended_feed_kg} kg`;
    if (valMorn) valMorn.innerText = `${data.morning_dose_kg} kg`;
    if (valEve) valEve.innerText = `${data.evening_dose_kg} kg`;

    // 3. Balanced Diet Pairing
    const b = data.balanced_ration || {};
    const valGreen = document.getElementById('rec-val-green');
    const valStraw = document.getElementById('rec-val-straw');
    const valMin = document.getElementById('rec-val-minerals');
    const valWater = document.getElementById('rec-val-water');

    if (valGreen) valGreen.innerText = `${b.green_fodder_kg || 20} kg`;
    if (valStraw) valStraw.innerText = `${b.dry_straw_kg || 4} kg`;
    if (valMin) valMin.innerText = `${b.mineral_mixture_grams || 60} g`;
    if (valWater) valWater.innerText = `${b.clean_water_litres || 60} L`;

    // 4. 4-Day Adaptation Cards
    const transGrid = document.getElementById('rec-transition-cards-grid');
    if (transGrid && data.transition_schedule) {
        transGrid.innerHTML = '';
        data.transition_schedule.forEach(step => {
            const card = document.createElement('div');
            card.style.cssText = 'background: #FFFFFF; border: 1px solid #FDE68A; border-radius: 8px; padding: 8px 10px; text-align: center;';
            const desc = state.language === 'te' ? (step.desc_te || step.action) : (state.language === 'hi' ? (step.desc_hi || step.action) : (step.desc_en || step.action));
            card.innerHTML = `
                <div style="font-weight: 800; font-size: 0.78rem; color: #B45309; margin-bottom: 2px;">
                    ${state.language === 'te' ? 'రోజు' : (state.language === 'hi' ? 'दिन' : 'Day')} ${step.day}
                </div>
                <div style="font-size: 1.05rem; font-weight: 900; color: #92400E;">${step.pct_new}% <span style="font-size: 0.70rem; font-weight: 600; color: var(--slate-500);">${state.language === 'te' ? 'కొత్తది' : (state.language === 'hi' ? 'नया' : 'New')}</span></div>
                <div style="font-size: 0.70rem; color: var(--slate-600); margin-top: 4px; line-height: 1.3;">${desc || ''}</div>
            `;
            transGrid.appendChild(card);
        });
    }

    // 5. Clinical & Stage Guidance Note
    const clinicalTxt = document.getElementById('rec-clinical-note-txt');
    if (clinicalTxt) {
        clinicalTxt.innerText = `${data.stage_clinical_note || ''} ${data.monitoring_caution || ''}`;
    }
}

function speakAnimalRecommendation() {
    const rec = state.currentAnimalRecommendation;
    if (!rec) {
        alert('Please run a scan or calculate recommendation first.');
        return;
    }
    const voiceText = rec.voice_script || rec.headline || 'Feeding recommendation calculated.';
    speakText(voiceText, state.language || 'te');
}

function updatePassportCard(data) {
    document.getElementById('cert-batch-id').innerText = data.batch_id;
    document.getElementById('cert-sample-type').innerText = data.sample_type;
    document.getElementById('cert-score').innerText = `${data.health_score} / 100`;
    document.getElementById('cert-safety-badge').innerText = data.safety_badge;
    document.getElementById('cert-timestamp').innerText = new Date().toISOString().replace('T', ' ').slice(0, 16);

    const nutr = data.nutrition?.nutrients || {};
    document.getElementById('cert-nutrients').innerText =
        `CP: ${nutr.crude_protein || 20}% | Moisture: ${nutr.moisture || 10}% | Fiber: ${nutr.fiber || 12}% | NPN: ${nutr.non_protein_nitrogen || 0.5}%`;

    const shelfEl = document.getElementById('cert-shelf-life');
    if (shelfEl) {
        if (data.shelf_life) {
            const days = data.shelf_life.shelf_life_days;
            const st = data.shelf_life.shelf_life_status;
            shelfEl.innerText = days > 0 ? `${days} Days (${st} - ${data.shelf_life.safe_until_date})` : `0 Days (${st})`;
            shelfEl.style.color = (days === 0 || st === 'EXPIRED') ? 'var(--crimson-danger)' : (days <= 3 ? '#DC2626' : (days <= 12 ? '#D97706' : 'var(--primary-emerald)'));
        } else {
            shelfEl.innerText = 'Standard Window';
        }
    }

    const qrImg = document.getElementById('cert-qr-image');
    if (data.qr_code_base64) {
        qrImg.src = data.qr_code_base64;
        const dlBtn = document.getElementById('btn-download-qr');
        if (dlBtn) {
            dlBtn.href = data.qr_code_base64;
            dlBtn.download = `${data.batch_id}_passport_qr.png`;
        }
    }
}

// ===================================================================
// Adulteration Simulator (API -> /api/check-adulteration)
// ===================================================================
let adulterationTimeout = null;
function runAdulterationCheck() {
    clearTimeout(adulterationTimeout);
    adulterationTimeout = setTimeout(async () => {
        const cpElem = document.getElementById('slider-ad-cp');
        const moistureElem = document.getElementById('slider-ad-moisture');
        const npnElem = document.getElementById('slider-ad-npn');
        const powderElem = document.getElementById('slider-ad-powder');

        if (!cpElem || !moistureElem || !npnElem || !powderElem) return;

        const payload = {
            sample_type: 'Cattle Feed Pellet',
            crude_protein: parseFloat(cpElem.value),
            moisture: parseFloat(moistureElem.value),
            non_protein_nitrogen: parseFloat(npnElem.value),
            visual_powder_particles: parseFloat(powderElem.value)
        };

        try {
            const resp = await fetch('/api/check-adulteration', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await resp.json();
            if (data && data.result) {
                renderAdulterationOutput(data.result);
            }
        } catch (e) {
            console.error('Adulteration check error:', e);
        }
    }, 120);
}

function renderAdulterationOutput(res) {
    const badge = document.getElementById('ad-badge');
    const badgeText = document.getElementById('ad-badge-text');
    const scoreText = document.getElementById('ad-score-text');
    const detailsList = document.getElementById('ad-details-list');

    if (!badge || !badgeText || !scoreText || !detailsList) return;

    const score = Math.round(res.risk_score !== undefined ? res.risk_score : (res.risk_score_points || 0));
    scoreText.innerText = `Adulteration Risk Score: ${score} / 100`;

    badge.className = 'safety-badge';
    const riskLevel = res.risk_level || res.adulteration_risk || (score >= 40 ? 'High' : (score >= 20 ? 'Medium' : 'Low'));

    if (riskLevel === 'High' || score >= 40) {
        badge.classList.add('badge-danger');
        badge.children[0].innerText = '🔴';
        badgeText.innerText = 'HIGH UREA / ADULTERATION RISK';
    } else if (riskLevel === 'Medium' || score >= 20) {
        badge.classList.add('badge-attention');
        badge.children[0].innerText = '🟡';
        badgeText.innerText = 'POSSIBLE ADULTERATION CONCERN';
    } else {
        badge.classList.add('badge-safe');
        badge.children[0].innerText = '🟢';
        badgeText.innerText = 'LOW ADULTERATION RISK';
    }

    detailsList.innerHTML = '';
    const reasons = res.reasons || [];
    if (reasons.length === 0) {
        detailsList.innerHTML = `
            <div class="deduction-item">
                <div class="deduction-name">Protein-to-Nitrogen Ratio Normal</div>
                <div class="deduction-points points-clean">Safe</div>
            </div>
        `;
    } else {
        reasons.forEach(r => {
            const div = document.createElement('div');
            div.className = 'deduction-item';
            div.innerHTML = `
                <div class="deduction-name">${r}</div>
                <div class="deduction-points points-penalty">Flagged</div>
            `;
            detailsList.appendChild(div);
        });
    }
}

// ===================================================================
// Scientific Safe Urea Dosage & Straw Treatment Calculator
// ===================================================================
let currentUreaMode = 'straw_treatment';
let lastUreaResult = null;
let ureaCalcTimeout = null;
let isSpeakingUrea = false;

function switchUreaMode(mode) {
    currentUreaMode = mode;
    const btnStraw = document.getElementById('btn-urea-mode-straw');
    const btnConc = document.getElementById('btn-urea-mode-concentrate');
    const lblQty = document.getElementById('label-urea-qty');
    const valQty = document.getElementById('val-urea-qty');
    const sliderQty = document.getElementById('slider-urea-qty');
    const stepsContainer = document.getElementById('urea-steps-container');

    if (mode === 'straw_treatment') {
        if (btnStraw) btnStraw.classList.add('active');
        if (btnConc) btnConc.classList.remove('active');
        if (lblQty) {
            lblQty.innerText = state.language === 'te' ? 'ఎండుగడ్డి పరిమాణం (kg)' : (state.language === 'hi' ? 'सूखे पुआल की मात्रा (kg)' : 'Dry Straw Quantity (kg)');
        }
        if (sliderQty) {
            sliderQty.min = 10;
            sliderQty.max = 1000;
            sliderQty.step = 10;
            sliderQty.value = 100;
        }
        if (valQty) valQty.innerText = '100 kg';
        if (stepsContainer) stepsContainer.style.display = 'block';
    } else {
        if (btnStraw) btnStraw.classList.remove('active');
        if (btnConc) btnConc.classList.add('active');
        if (lblQty) {
            lblQty.innerText = state.language === 'te' ? 'రోజువారీ దాణా పరిమాణం (kg)' : (state.language === 'hi' ? 'दैनिक दाने की मात्रा (kg)' : 'Daily Concentrate Quantity (kg)');
        }
        if (sliderQty) {
            sliderQty.min = 1;
            sliderQty.max = 100;
            sliderQty.step = 1;
            sliderQty.value = 10;
        }
        if (valQty) valQty.innerText = '10 kg';
        if (stepsContainer) stepsContainer.style.display = 'none';
    }

    runSafeUreaCalculator();
}

function updateUreaSliderBadge(idPrefix, val, unit) {
    const badge = document.getElementById(`val-${idPrefix}`);
    if (badge) badge.innerText = `${val}${unit}`;
}

function runSafeUreaCalculator() {
    clearTimeout(ureaCalcTimeout);
    ureaCalcTimeout = setTimeout(async () => {
        const sliderQty = document.getElementById('slider-urea-qty');
        const sliderAnimals = document.getElementById('slider-urea-animals');
        if (!sliderQty || !sliderAnimals) return;

        const payload = {
            mode: currentUreaMode,
            quantity_kg: parseFloat(sliderQty.value) || 100.0,
            num_animals: parseInt(sliderAnimals.value) || 1,
            language: state.language || 'en'
        };

        try {
            const resp = await fetch('/api/safe-urea-calculator', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!resp.ok) return;
            const json = await resp.json();
            if (json && json.data) {
                lastUreaResult = json.data;
                renderUreaOutput(json.data);
            }
        } catch (e) {
            console.error('Safe Urea Calculator error:', e);
        }
    }, 80);
}

function renderUreaOutput(data) {
    const safeAmountEl = document.getElementById('urea-kpi-safe-amount');
    const waterAmountEl = document.getElementById('urea-kpi-water-amount');
    const curingDaysEl = document.getElementById('urea-kpi-curing-days');
    const proteinBoostEl = document.getElementById('urea-kpi-protein-boost');
    const summaryTextEl = document.getElementById('urea-summary-text');
    const stepsListEl = document.getElementById('urea-steps-list');
    const precautionsListEl = document.getElementById('urea-precautions-list');
    const antidoteTextEl = document.getElementById('urea-antidote-text');

    if (safeAmountEl) safeAmountEl.innerText = data.safe_urea_display || '--';
    if (waterAmountEl) waterAmountEl.innerText = data.required_water_display || '--';
    if (curingDaysEl) curingDaysEl.innerText = data.curing_days_range || '--';
    if (proteinBoostEl) proteinBoostEl.innerText = data.crude_protein_boost || '--';
    if (summaryTextEl) summaryTextEl.innerText = data.summary || '';

    // Render Steps
    if (stepsListEl) {
        stepsListEl.innerHTML = '';
        const steps = data.steps || [];
        steps.forEach(s => {
            const li = document.createElement('li');
            li.innerHTML = s;
            stepsListEl.appendChild(li);
        });
    }

    // Render Precautions
    if (precautionsListEl) {
        precautionsListEl.innerHTML = '';
        const precautions = state.language === 'te' 
            ? (data.precautions_te || data.precautions) 
            : (state.language === 'hi' ? (data.precautions_hi || data.precautions) : data.precautions);
        (precautions || []).forEach(p => {
            const li = document.createElement('li');
            li.innerHTML = `⚠️ ${p}`;
            precautionsListEl.appendChild(li);
        });
    }

    // Antidote Guide
    if (antidoteTextEl && data.antidote_guide) {
        antidoteTextEl.innerHTML = data.antidote_guide[state.language] || data.antidote_guide.en;
    }
}

async function speakUreaAdvisory() {
    if (!lastUreaResult) return;
    const btn = document.getElementById('btn-speak-urea');
    const btnText = document.getElementById('btn-speak-urea-text');

    if (isSpeakingUrea) {
        if (state.audioPlayer) {
            state.audioPlayer.pause();
            state.audioPlayer = null;
        }
        if (window.speechSynthesis) {
            window.speechSynthesis.cancel();
        }
        isSpeakingUrea = false;
        if (btnText) btnText.innerText = state.language === 'te' ? 'వాయిస్ వినండి' : (state.language === 'hi' ? 'आवाज सुनें' : 'Listen Voice Guide');
        return;
    }

    const textToSpeak = `${lastUreaResult.summary}. ${lastUreaResult.antidote_guide ? (lastUreaResult.antidote_guide[state.language] || lastUreaResult.antidote_guide.en) : ''}`;
    isSpeakingUrea = true;
    if (btnText) btnText.innerText = state.language === 'te' ? '⏹ ఆపండి' : (state.language === 'hi' ? '⏹ रोकें' : '⏹ Stop Audio');

    try {
        const resp = await fetch('/api/tts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: textToSpeak,
                language: state.language || 'en'
            })
        });

        if (resp.ok) {
            const blob = await resp.blob();
            const audioUrl = URL.createObjectURL(blob);
            state.audioPlayer = new Audio(audioUrl);
            state.audioPlayer.onended = () => {
                isSpeakingUrea = false;
                if (btnText) btnText.innerText = state.language === 'te' ? 'వాయిస్ వినండి' : (state.language === 'hi' ? 'आवाज सुनें' : 'Listen Voice Guide');
            };
            state.audioPlayer.play();
            return;
        }
    } catch (e) {
        console.warn('TTS API unavailable, falling back to Web Speech API', e);
    }

    // Fallback: Browser Web Speech API
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(textToSpeak);
        utterance.lang = state.language === 'te' ? 'te-IN' : (state.language === 'hi' ? 'hi-IN' : 'en-US');
        utterance.rate = 0.95;
        utterance.onend = () => {
            isSpeakingUrea = false;
            if (btnText) btnText.innerText = state.language === 'te' ? 'వాయిస్ వినండి' : (state.language === 'hi' ? 'आवाज सुनें' : 'Listen Voice Guide');
        };
        window.speechSynthesis.speak(utterance);
    } else {
        isSpeakingUrea = false;
        if (btnText) btnText.innerText = state.language === 'te' ? 'వాయిస్ వినండి' : (state.language === 'hi' ? 'आवाज सुनें' : 'Listen Voice Guide');
    }
}

// Expose urea calculator functions globally for HTML event attributes
window.switchUreaMode = switchUreaMode;
window.updateUreaSliderBadge = updateUreaSliderBadge;
window.runSafeUreaCalculator = runSafeUreaCalculator;
window.speakUreaAdvisory = speakUreaAdvisory;

// ===================================================================
// Multilingual Farmer Problem Statements & Native Voice Engine
// ===================================================================

function updateAdvisoryHeaders(lang) {
    const titles = {
        te: {
            title: '👨‍🌾 1-క్లిక్ సాధారణ రైతు సమస్యలు',
            subtitle: 'రైతులు ఎలాంటి ప్రశ్నలు రాయనవసరం లేదు — మీ పశువుల సమస్యను కింద ఎంచుకోండి:',
            plan: '📜 రైతులకు స్పష్టమైన సలహా & పరిష్కారం',
            voiceReady: 'స్పష్టమైన తెలుగు ఆడియో సిద్ధంగా ఉంది',
            btnPreset: '⚡ 1-క్లిక్ సాధారణ సమస్యలు',
            btnManual: '✍️ నేరుగా సమస్య రాయండి',
            manualTitle: '✍️ మీ సమస్యను నేరుగా రాయండి',
            manualSubtitle: 'మీ సమస్యను తెలుగు, ఇంగ్లీష్ లేదా హిందీలో రాయండి, లేదా కింద ఉన్న లక్షణాలను నొక్కండి:',
            chipsLabel: '⚡ త్వరిత లక్షణాలు (జతచేయడానికి నొక్కండి):',
            descLabel: 'సమస్య వివరాలు రాయండి:',
            descPlaceholder: 'ఉదాహరణ: ఆవు పాలు తగ్గిపోయాయి, మేతలో పుల్లని వాసన లేదా బూజు ఉంది...',
            submitBtn: '🚀 AI విశ్లేషణ చేయండి',
            feedType: 'మేత రకం',
            smell: 'మేత వాసన',
            moisture: 'తేమ శాతం',
            appearance: 'భౌతిక స్థితి',
            symptom: 'పశువుల లక్షణాలు'
        },
        hi: {
            title: '👨‍🌾 1-क्लिक सामान्य किसान समस्याएं',
            subtitle: 'किसानों को कुछ लिखने की आवश्यकता नहीं — अपनी स्थिति से संबंधित समस्या चुनें:',
            plan: '📜 किसानों के लिए कार्य योजना व सलाह',
            voiceReady: 'हिंदी आवाज तैयार है',
            btnPreset: '⚡ 1-क्लिक सामान्य समस्याएं',
            btnManual: '✍️ अपनी समस्या लिखें',
            manualTitle: '✍️ अपनी समस्या सीधे लिखें',
            manualSubtitle: 'अपनी समस्या हिंदी, अंग्रेजी या तेलुगु में लिखें, या नीचे दिए गए लक्षणों को चुनें:',
            chipsLabel: '⚡ त्वरित लक्षण टैग (जोड़ने के लिए क्लिक करें):',
            descLabel: 'समस्या या स्थिति का विवरण दें:',
            descPlaceholder: 'उदाहरण: गाय का दूध अचानक घट गया है, चारे में फफूंद या दुर्गंध आ रही है...',
            submitBtn: '🚀 AI विश्लेषण करें',
            feedType: 'चारे का प्रकार',
            smell: 'चारे की गंध',
            moisture: 'नमी की स्थिति',
            appearance: 'दिखावट',
            symptom: 'पशु के लक्षण'
        },
        en: {
            title: '👨‍🌾 1-Click Common Farmer Problem Statements',
            subtitle: 'Farmers don\'t need to type — simply tap the statement that matches your cattle\'s situation:',
            plan: '📜 Tailored Farmer Action Plan',
            voiceReady: 'Native Voice Ready: English',
            btnPreset: '⚡ 1-Click Common Statements',
            btnManual: '✍️ Manual / Custom Problem Entry',
            manualTitle: '✍️ Manual / Custom Problem Diagnosis',
            manualSubtitle: 'Type your problem in English, Telugu, or Hindi, or click quick symptom tags below:',
            chipsLabel: '⚡ Quick Symptom Tags (Tap to Add):',
            descLabel: 'Describe What Happened / Details:',
            descPlaceholder: 'e.g., Milk yield dropped suddenly and feed has sour/musty smell...',
            submitBtn: '🚀 Analyze Problem with AI',
            feedType: 'Feed Type',
            smell: 'Feed Smell',
            moisture: 'Moisture Status',
            appearance: 'Appearance',
            symptom: 'Cattle Symptoms'
        }
    };

    const t = titles[lang] || titles.en;
    const probTitle = document.getElementById('problem-statements-title');
    const probSub = document.getElementById('problem-statements-subtitle');
    const planTitle = document.getElementById('advisory-plan-title');
    const audioSub = document.getElementById('audio-subtitle');
    const btnPreset = document.getElementById('btn-mode-preset');
    const btnManual = document.getElementById('btn-mode-manual');
    const manualTitle = document.getElementById('manual-entry-title');
    const manualSub = document.getElementById('manual-entry-subtitle');
    const chipsLabel = document.getElementById('symptom-chips-label');
    const labelProblem = document.getElementById('label-manual-problem');
    const problemInput = document.getElementById('manual-problem-input');
    const btnSubmitManual = document.getElementById('btn-submit-manual-advisory');
    const labelFeedType = document.getElementById('label-feed-type');
    const labelSmell = document.getElementById('label-feed-smell');
    const labelMoisture = document.getElementById('label-feed-moisture');
    const labelAppearance = document.getElementById('label-feed-appearance');
    const labelSymptom = document.getElementById('label-cattle-symptom');

    if (probTitle) probTitle.innerText = t.title;
    if (probSub) probSub.innerText = t.subtitle;
    if (planTitle) planTitle.innerText = t.plan;
    if (audioSub) audioSub.innerText = t.voiceReady;
    if (btnPreset) btnPreset.innerHTML = t.btnPreset;
    if (btnManual) btnManual.innerHTML = t.btnManual;
    if (manualTitle) manualTitle.innerText = t.manualTitle;
    if (manualSub) manualSub.innerText = t.manualSubtitle;
    if (chipsLabel) chipsLabel.innerText = t.chipsLabel;
    if (labelProblem) labelProblem.innerText = t.descLabel;
    if (problemInput) problemInput.placeholder = t.descPlaceholder;
    if (btnSubmitManual) btnSubmitManual.innerHTML = t.submitBtn;
    if (labelFeedType) labelFeedType.innerText = t.feedType;
    if (labelSmell) labelSmell.innerText = t.smell;
    if (labelMoisture) labelMoisture.innerText = t.moisture;
    if (labelAppearance) labelAppearance.innerText = t.appearance;
    if (labelSymptom) labelSymptom.innerText = t.symptom;
}

const SYMPTOM_CHIPS = {
    te: [
        { label: '🥛 పాల తగ్గుదల', text: 'పాల దిగుబడి తగ్గింది', symptom: 'Sudden Milk Drop' },
        { label: '🤢 బూజు / దుర్వాసన', text: 'మేతలో బూజు పట్టి పుల్లని వాసన వస్తోంది', appearance: 'Fungus/Mould Patches', smell: 'Fungal/Musty' },
        { label: '🍽️ మేత తినడం లేదు', text: 'పశువులు మేత తినడానికి నిరాకరిస్తున్నాయి', symptom: 'Refusing to Eat' },
        { label: '🌧️ తడిసిన మేత', text: 'మేత బస్తాలు వర్షంలో తడిసిపోయాయి', moisture: 'Soaked/Rain Damage' },
        { label: '🚨 యూరియా వాసన', text: 'మేతలో ఘాటైన యూరియా వాసన తెల్ల పొడి ఉంది', appearance: 'White Powder/Granules', smell: 'Chemical/Urea' },
        { label: '🩺 విరేచనాలు / ఉబ్బరం', text: 'పశువులకు విరేచనాలు మరియు కడుపు ఉబ్బరం వచ్చింది', symptom: 'Loose Dung/Diarrhea' },
        { label: '🪱 పురుగులు / రాళ్ళు', text: 'మేతలో రాళ్ళు మరియు పురుగులు కనిపించాయి', appearance: 'Inclusions/Debris' }
    ],
    hi: [
        { label: '🥛 दूध में गिरावट', text: 'दूध उत्पादन अचानक घट गया है', symptom: 'Sudden Milk Drop' },
        { label: '🤢 फफूंद / दुर्गंध', text: 'चारे में फफूंद और सड़ी दुर्गंध आ रही है', appearance: 'Fungus/Mould Patches', smell: 'Fungal/Musty' },
        { label: '🍽️ चारा नहीं खा रहे', text: 'पशु चारे को सूंघकर खाने से मना कर रहे हैं', symptom: 'Refusing to Eat' },
        { label: '🌧️ चारा भीग गया', text: 'बारिश से चारे की बोरियां भीग गई हैं', moisture: 'Soaked/Rain Damage' },
        { label: '🚨 यूरिया की गंध', text: 'चारे में यूरिया की तेज गंध और सफेद दाने हैं', appearance: 'White Powder/Granules', smell: 'Chemical/Urea' },
        { label: '🩺 दस्त / पेट फूलना', text: 'चारा खाने के बाद पशुओं को दस्त और पेट फूल गया है', symptom: 'Loose Dung/Diarrhea' },
        { label: '🪱 कंकड़ / कीड़े', text: 'चारे में कंकड़ और कीड़े दिखाई दिए हैं', appearance: 'Inclusions/Debris' }
    ],
    en: [
        { label: '🥛 Sudden Milk Drop', text: 'Milk yield dropped suddenly after feeding', symptom: 'Sudden Milk Drop' },
        { label: '🤢 Mould / Sour Smell', text: 'Feed has musty mould and sour smell', appearance: 'Fungus/Mould Patches', smell: 'Fungal/Musty' },
        { label: '🍽️ Refusing to Eat', text: 'Cattle sniffing feed and refusing to eat', symptom: 'Refusing to Eat' },
        { label: '🌧️ Soaked / Damp Feed', text: 'Feed bags got soaked in rain', moisture: 'Soaked/Rain Damage' },
        { label: '🚨 Urea / Chemical Odor', text: 'Suspected white powder and pungent urea odor in feed', appearance: 'White Powder/Granules', smell: 'Chemical/Urea' },
        { label: '🩺 Loose Dung / Bloat', text: 'Cattle developed loose dung and bloat', symptom: 'Loose Dung/Diarrhea' },
        { label: '🪱 Stones / Insects', text: 'Found foreign stones, grit and insect webbing', appearance: 'Inclusions/Debris' }
    ]
};

function renderSymptomChips(lang) {
    const container = document.getElementById('symptom-chips-container');
    if (!container) return;
    container.innerHTML = '';
    const chips = SYMPTOM_CHIPS[lang] || SYMPTOM_CHIPS.en;

    chips.forEach(chip => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'symptom-chip';
        btn.innerText = chip.label;
        btn.onclick = () => insertSymptomChip(chip.text, {
            symptom: chip.symptom,
            smell: chip.smell,
            appearance: chip.appearance,
            moisture: chip.moisture
        });
        container.appendChild(btn);
    });
}

function insertSymptomChip(text, overrides = {}) {
    const input = document.getElementById('manual-problem-input');
    if (input) {
        const cur = input.value.trim();
        input.value = cur ? `${cur}, ${text}` : text;
        input.focus();
    }
    if (overrides.symptom) {
        const sel = document.getElementById('manual-cattle-symptom');
        if (sel) sel.value = overrides.symptom;
    }
    if (overrides.smell) {
        const sel = document.getElementById('manual-feed-smell');
        if (sel) sel.value = overrides.smell;
    }
    if (overrides.appearance) {
        const sel = document.getElementById('manual-feed-appearance');
        if (sel) sel.value = overrides.appearance;
    }
    if (overrides.moisture) {
        const sel = document.getElementById('manual-feed-moisture');
        if (sel) sel.value = overrides.moisture;
    }
}

function switchAdvisoryInputMode(mode) {
    state.advisoryInputMode = mode;
    const btnPreset = document.getElementById('btn-mode-preset');
    const btnManual = document.getElementById('btn-mode-manual');
    const secPreset = document.getElementById('section-preset-problems');
    const secManual = document.getElementById('section-manual-entry');

    if (mode === 'manual') {
        if (btnPreset) btnPreset.classList.remove('active');
        if (btnManual) btnManual.classList.add('active');
        if (secPreset) secPreset.style.display = 'none';
        if (secManual) secManual.style.display = 'block';
        renderSymptomChips(state.language);
    } else {
        if (btnPreset) btnPreset.classList.add('active');
        if (btnManual) btnManual.classList.remove('active');
        if (secPreset) secPreset.style.display = 'block';
        if (secManual) secManual.style.display = 'none';
        if (state.selectedProblemId) {
            selectFarmerProblem(state.selectedProblemId);
        }
    }
}

async function runManualAdvisoryAnalysis() {
    const inputElem = document.getElementById('manual-problem-input');
    const feedTypeElem = document.getElementById('manual-feed-type');
    const smellElem = document.getElementById('manual-feed-smell');
    const moistureElem = document.getElementById('manual-feed-moisture');
    const appearanceElem = document.getElementById('manual-feed-appearance');
    const symptomElem = document.getElementById('manual-cattle-symptom');

    const queryText = inputElem ? inputElem.value.trim() : '';
    const feedType = feedTypeElem ? feedTypeElem.value : 'Cattle Feed Pellet';
    const smell = smellElem ? smellElem.value : 'Normal';
    const moisture = moistureElem ? moistureElem.value : 'Normal';
    const appearance = appearanceElem ? appearanceElem.value : 'Normal';
    const cattleSymptom = symptomElem ? symptomElem.value : 'Normal';

    const effectiveQuery = queryText || `${feedType}: ${cattleSymptom !== 'Normal' ? cattleSymptom : ''} ${smell !== 'Normal' ? smell : ''} ${appearance !== 'Normal' ? appearance : ''}`.trim();

    const textContainer = document.getElementById('advisory-text-container');
    const loadingMessages = {
        te: '<em>⏳ మీ సమస్యను AI విశ్లేషిస్తోంది... దయచేసి వేచి ఉండండి...</em>',
        hi: '<em>⏳ AI आपकी समस्या का विश्लेषण कर रहा है... कृपया प्रतीक्षा करें...</em>',
        en: '<em>⏳ AI is analyzing your custom problem... Please wait...</em>'
    };
    if (textContainer) {
        textContainer.innerHTML = loadingMessages[state.language] || loadingMessages.en;
    }

    try {
        const resp = await fetch('/api/advisory', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                is_manual: true,
                manual_query: effectiveQuery,
                query: effectiveQuery,
                sample_type: feedType,
                feed_type: feedType,
                smell: smell,
                moisture_status: moisture,
                appearance: appearance,
                cattle_symptom: cattleSymptom,
                language: state.language,
                provider: state.advisoryMode
            })
        });

        const data = await resp.json();
        if (data && data.advisory) {
            updateAdvisoryView(data.advisory);
            const planElem = document.getElementById('advisory-plan-title');
            if (planElem) planElem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    } catch (e) {
        console.error('Manual advisory analysis error:', e);
        if (textContainer) {
            textContainer.innerText = 'Unable to reach advisory engine. Please check connection.';
        }
    }
}

function clearManualAdvisoryForm() {
    const input = document.getElementById('manual-problem-input');
    if (input) input.value = '';
    const smell = document.getElementById('manual-feed-smell');
    if (smell) smell.value = 'Normal';
    const moisture = document.getElementById('manual-feed-moisture');
    if (moisture) moisture.value = 'Normal';
    const appearance = document.getElementById('manual-feed-appearance');
    if (appearance) appearance.value = 'Normal';
    const symptom = document.getElementById('manual-cattle-symptom');
    if (symptom) symptom.value = 'Normal';
}

async function loadFarmerProblemStatements(lang) {
    const container = document.getElementById('farmer-problems-container');
    if (!container) return;

    try {
        const resp = await fetch(`/api/farmer-problems?language=${lang}`);
        const data = await resp.json();
        state.farmerProblems = data.problems || [];
        renderFarmerProblemCards(state.farmerProblems);

        // Select the active problem or default to milk_drop
        const targetId = state.selectedProblemId || (state.farmerProblems[0] ? state.farmerProblems[0].id : 'milk_drop');
        selectFarmerProblem(targetId);
    } catch (e) {
        console.error('Failed to load farmer problem statements:', e);
    }
}

function renderFarmerProblemCards(problems) {
    const container = document.getElementById('farmer-problems-container');
    if (!container) return;
    container.innerHTML = '';

    problems.forEach(p => {
        const card = document.createElement('div');
        const isActive = p.id === state.selectedProblemId;
        card.className = `farmer-problem-card ${isActive ? 'active' : ''}`;
        card.id = `problem-card-${p.id}`;
        card.onclick = () => selectFarmerProblem(p.id);

        card.innerHTML = `
            <div class="farmer-problem-badge">✓ Selected</div>
            <div class="farmer-problem-icon">${p.icon}</div>
            <div class="farmer-problem-body">
                <div class="farmer-problem-title">${p.title}</div>
                <div class="farmer-problem-statement">"${p.statement}"</div>
            </div>
        `;
        container.appendChild(card);
    });
}

async function selectFarmerProblem(problemId) {
    state.selectedProblemId = problemId;

    // Update active UI cards
    document.querySelectorAll('.farmer-problem-card').forEach(c => {
        c.classList.remove('active');
    });
    const activeCard = document.getElementById(`problem-card-${problemId}`);
    if (activeCard) activeCard.classList.add('active');

    // Fetch tailored advisory for this problem
    await fetchAdvisoryForProblem(problemId, state.language);
}

async function fetchAdvisoryForProblem(problemId, lang) {
    const textContainer = document.getElementById('advisory-text-container');
    if (textContainer) {
        const curL = lang || state.language || 'en';
        const msg = curL === 'te' ? '<em>⏳ సలహా సిద్ధమవుతోంది... దయచేసి వేచి ఉండండి...</em>' : (curL === 'hi' ? '<em>⏳ सलाह तैयार हो रही है... कृपया प्रतीक्षा करें...</em>' : '<em>⏳ Generating Farmer Advisory... Please wait...</em>');
        textContainer.innerHTML = msg;
    }

    try {
        const resp = await fetch('/api/advisory', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                problem_id: problemId,
                language: lang,
                provider: state.advisoryMode
            })
        });

        const data = await resp.json();
        if (data && data.advisory) {
            updateAdvisoryView(data.advisory);
        }
    } catch (e) {
        console.error('Problem advisory failed:', e);
        if (textContainer) {
            textContainer.innerText = 'Unable to reach advisory engine. Please check connection.';
        }
    }
}

async function fetchAdvisory(scanData, lang) {
    if (state.selectedProblemId) {
        await fetchAdvisoryForProblem(state.selectedProblemId, lang);
    }
}

function updateAdvisoryView(adv) {
    if (!adv) return;
    const textContainer = document.getElementById('advisory-text-container');
    const badge = document.getElementById('advisory-scenario-badge');

    const content = adv.full_advisory_text || adv.advisory_text || adv.main_problems?.join('\n\n• ') || 'Advisory available.';
    if (textContainer) {
        textContainer.innerText = content;
    }

    if (badge && adv.safety_status) {
        badge.innerText = adv.safety_status;
        badge.className = 'safety-badge';
        const st = adv.safety_status.toLowerCase();
        if (st.includes('safe') || st.includes('సురక్షిత') || st.includes('सुरक्षित')) {
            badge.classList.add('badge-safe');
        } else if (st.includes('caution') || st.includes('జాగ్రత్త') || st.includes('सावधानी') || st.includes('హెచ్చరిక')) {
            badge.classList.add('badge-attention');
        } else {
            badge.classList.add('badge-danger');
        }
    }

    const audioSub = document.getElementById('audio-subtitle');
    const langNames = {
        en: 'Native Voice Ready: English',
        te: 'స్పష్టమైన తెలుగు ఆడియో సిద్ధంగా ఉంది',
        hi: 'हिंदी आवाज तैयार है'
    };
    if (audioSub) {
        audioSub.innerText = langNames[state.language] || 'Native Voice Ready';
    }
}

async function toggleSpeech() {
    const speakBtn = document.getElementById('btn-speak');
    const soundwave = document.getElementById('soundwave');

    // If currently playing, stop it
    if (state.isSpeaking) {
        if (state.audioPlayer) {
            state.audioPlayer.pause();
            state.audioPlayer.currentTime = 0;
        }
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
        }
        stopSpeechUI();
        return;
    }

    const textContainer = document.getElementById('advisory-text-container');
    const rawText = textContainer ? textContainer.innerText : '';
    if (!rawText || rawText.includes('సిద్ధమవుతోంది') || rawText.includes('Loading') || rawText.includes('Generating')) {
        alert('Please wait for advisory text to load before playing audio.');
        return;
    }

    // Clean text for speech
    const cleanText = rawText
        .replace(/[\u{1F300}-\u{1F9FF}]/gu, '')
        .replace(/[\u{2600}-\u{26FF}]/gu, '')
        .replace(/[\u{2700}-\u{27BF}]/gu, '')
        .replace(/[•\*\#\_]/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();

    if (!cleanText) return;

    state.isSpeaking = true;
    if (speakBtn) speakBtn.innerText = '⏳ Loading Audio...';
    if (soundwave) soundwave.classList.add('playing');

    try {
        // 1. PRIMARY: Call backend /api/tts endpoint (Generates REAL native Telugu / Hindi / English MP3)
        const resp = await fetch('/api/tts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: cleanText,
                language: state.language
            })
        });

        if (!resp.ok) {
            throw new Error(`TTS server returned status ${resp.status}`);
        }

        const blob = await resp.blob();
        if (state.currentAudioUrl) {
            URL.revokeObjectURL(state.currentAudioUrl);
        }
        state.currentAudioUrl = URL.createObjectURL(blob);

        if (!state.audioPlayer) {
            state.audioPlayer = new Audio();
        }

        state.audioPlayer.src = state.currentAudioUrl;

        state.audioPlayer.onplay = () => {
            if (speakBtn) speakBtn.innerText = '⏹ Stop Audio';
            if (soundwave) soundwave.classList.add('playing');
        };

        state.audioPlayer.onended = () => {
            stopSpeechUI();
        };

        state.audioPlayer.onerror = (e) => {
            console.warn('Audio playback error, falling back to Web Speech API:', e);
            fallbackBrowserSpeech(cleanText);
        };

        await state.audioPlayer.play();

    } catch (err) {
        console.warn('Backend TTS failed, trying browser speech synthesis fallback:', err);
        fallbackBrowserSpeech(cleanText);
    }
}

function fallbackBrowserSpeech(cleanText) {
    if (!('speechSynthesis' in window)) {
        stopSpeechUI();
        alert('Audio playback could not be started.');
        return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(cleanText);
    const langCodes = { te: 'te-IN', hi: 'hi-IN', en: 'en-IN' };
    utterance.lang = langCodes[state.language] || 'en-IN';

    const voices = window.speechSynthesis.getVoices() || [];
    const targetPrefix = state.language === 'te' ? 'te' : (state.language === 'hi' ? 'hi' : 'en');
    const matchedVoice = voices.find(v => v.lang && v.lang.toLowerCase().startsWith(targetPrefix));
    if (matchedVoice) {
        utterance.voice = matchedVoice;
    }

    utterance.rate = 0.95;

    utterance.onstart = () => {
        const speakBtn = document.getElementById('btn-speak');
        const soundwave = document.getElementById('soundwave');
        if (soundwave) soundwave.classList.add('playing');
        if (speakBtn) speakBtn.innerText = '⏹ Stop Audio';
    };

    utterance.onend = () => stopSpeechUI();
    utterance.onerror = () => stopSpeechUI();

    window.speechSynthesis.speak(utterance);
}

function stopSpeechUI() {
    state.isSpeaking = false;
    if (state.audioPlayer) {
        state.audioPlayer.pause();
    }
    const soundwave = document.getElementById('soundwave');
    const speakBtn = document.getElementById('btn-speak');
    if (soundwave) soundwave.classList.remove('playing');
    if (speakBtn) speakBtn.innerText = '▶ Play Voice Audio';
}

// ===================================================================
// Dashboard Analytics (API -> /api/dashboard)
// ===================================================================
async function loadDashboardData() {
    try {
        let url = '/api/dashboard';
        if (state.currentUser && state.currentUser.role === 'farmer' && state.currentUser.id) {
            url = `/api/dashboard?user_id=${state.currentUser.id}`;
        }
        const resp = await fetch(url);
        if (!resp.ok) {
            console.error('Dashboard API returned error status:', resp.status);
            return;
        }
        const data = await resp.json();

        const m = data.metrics || {};
        const elTotal = document.getElementById('kpi-total-tests');
        const elAvg = document.getElementById('kpi-avg-score');
        const elSafe = document.getElementById('kpi-safe-pct');
        const elRisk = document.getElementById('kpi-risk-pct');

        if (elTotal) elTotal.innerText = m.total_tests || 0;
        if (elAvg) elAvg.innerText = `${Math.round(m.avg_quality_score || 0)} / 100`;
        
        const safeVal = m.safe_feed_percentage !== undefined ? m.safe_feed_percentage : (m.safe_pct || 0);
        const riskVal = m.high_risk_percentage !== undefined ? m.high_risk_percentage : (m.high_risk_pct || 0);
        if (elSafe) elSafe.innerText = `${Math.round(safeVal)}%`;
        if (elRisk) elRisk.innerText = `${Math.round(riskVal)}%`;

        // Early Spoilage Alert Banner
        const sp = data.spoilage_warning || {};
        const banner = document.getElementById('dashboard-spoilage-banner');
        const bannerText = document.getElementById('dashboard-spoilage-text');
        if (banner && bannerText) {
            const hasWarning = Boolean(sp.warning_triggered || sp.has_warning);
            if (hasWarning) {
                banner.className = 'alert-box alert-warning';
                const reasonsList = (sp.reasons && sp.reasons.length) ? sp.reasons.join(' ') : (sp.message || '');
                const recPrefix = state.language === 'te' ? '💡 సిఫార్సు:' : (state.language === 'hi' ? '💡 सिफारिश:' : '💡 Action:');
                const recText = sp.recommendation ? `<div style="margin-top: 6px; font-size: 0.86rem; opacity: 0.95;"><strong>${recPrefix}</strong> ${sp.recommendation}</div>` : '';
                bannerText.innerHTML = `<strong>⚠️ ${sp.title || 'Early Spoilage Alert'}:</strong> ${reasonsList}${recText}`;
            } else {
                banner.className = 'alert-box alert-info';
                bannerText.innerHTML = `<strong>🛡️ Spoilage Trajectory Status:</strong> ${sp.message || 'No progressive feed deterioration detected in recent batches.'}`;
            }
        }

        // Render Recent Batches Table
        const tbody = document.getElementById('recent-batches-tbody');
        if (tbody) {
            tbody.innerHTML = '';
            const tests = data.recent_tests || [];
            if (tests.length === 0) {
                tbody.innerHTML = `<tr><td colspan="6" style="padding: 20px; text-align: center; color: var(--slate-500);">No tests recorded yet. Run a scan to see records.</td></tr>`;
            } else {
                tests.forEach(t => {
                    const tr = document.createElement('tr');
                    tr.style.borderBottom = '1px solid var(--slate-200)';
                    const rawDate = t.timestamp || t.created_at || '';
                    const dateClean = rawDate.replace('T', ' ').slice(0, 16);

                    let badgeHtml = t.safety_badge;
                    if (!badgeHtml || typeof badgeHtml !== 'string' || badgeHtml.includes('undefined')) {
                        const score = Number(t.quality_score || 0);
                        const risk = String(t.overall_risk || '').toLowerCase();
                        if (score >= 80 && risk !== 'high') {
                            badgeHtml = '<span class="safety-badge badge-safe">🟢 SAFE</span>';
                        } else if (score >= 50 && risk !== 'high') {
                            badgeHtml = '<span class="safety-badge badge-caution">🟡 CAUTION</span>';
                        } else {
                            badgeHtml = '<span class="safety-badge badge-danger">🔴 HIGH RISK</span>';
                        }
                    }

                    tr.innerHTML = `
                        <td style="padding: 12px 10px; font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--accent-blue);">${t.batch_id || 'N/A'}</td>
                        <td style="padding: 12px 10px; font-weight: 600; color: var(--slate-800);">${t.sample_type || 'Compound Feed'}</td>
                        <td style="padding: 12px 10px; font-weight: 800; color: var(--slate-900); font-size: 0.96rem;">${Math.round(t.quality_score || 0)} / 100</td>
                        <td style="padding: 12px 10px;">${badgeHtml}</td>
                        <td style="padding: 12px 10px; color: var(--slate-600); font-size: 0.88rem;">${t.primary_concern || 'Standard Feed'}</td>
                        <td style="padding: 12px 10px; font-size: 0.82rem; color: var(--slate-500); font-family: monospace;">${dateClean}</td>
                    `;
                    tbody.appendChild(tr);
                });
            }
        }

        // Render Charts
        renderDashboardCharts(data);

    } catch (e) {
        console.error('Failed to load dashboard data:', e);
    }
}

function renderDashboardCharts(data) {
    if (typeof Chart === 'undefined') {
        console.warn('Chart.js library is not available yet.');
        return;
    }

    const trends = (data.quality_trends || []).slice(-15);
    const labels = trends.map((t, idx) => {
        if (t.batch_id) {
            const parts = t.batch_id.split('-');
            return `#${parts[parts.length - 1]}`;
        }
        return `Batch ${idx + 1}`;
    });
    const scores = trends.map(t => Number(t.quality_score || 0));

    // 1. Trend Line Chart
    const trendCanvas = document.getElementById('chart-quality-trend');
    if (trendCanvas) {
        if (state.charts.trend) {
            try { state.charts.trend.destroy(); } catch (e) {}
            state.charts.trend = null;
        }
        state.charts.trend = new Chart(trendCanvas, {
            type: 'line',
            data: {
                labels: labels.length ? labels : ['B-1', 'B-2', 'B-3', 'B-4'],
                datasets: [{
                    label: state.language === 'te' ? 'ఆరోగ్య స్కోర్ (0-100)' : (state.language === 'hi' ? 'स्वास्थ्य स्कोर (0-100)' : 'Health Score (0-100)'),
                    data: scores.length ? scores : [85, 85, 7, 12],
                    borderColor: '#059669',
                    backgroundColor: 'rgba(16, 185, 129, 0.12)',
                    pointBackgroundColor: '#059669',
                    pointBorderColor: '#FFFFFF',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    borderWidth: 3,
                    fill: true,
                    tension: 0.35
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { 
                        min: 0, 
                        max: 100,
                        grid: { color: 'rgba(0, 0, 0, 0.06)' },
                        ticks: { font: { weight: 'bold' } }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { font: { weight: '600' } }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { font: { weight: 'bold' } }
                    }
                }
            }
        });
    }

    // 2. Risk Level Doughnut Chart
    const pieCanvas = document.getElementById('chart-risk-pie');
    if (pieCanvas) {
        if (state.charts.pie) {
            try { state.charts.pie.destroy(); } catch (e) {}
            state.charts.pie = null;
        }
        const m = data.metrics || {};
        const safe = Number(m.safe_tests !== undefined ? m.safe_tests : (m.safe_count || 0));
        const attention = Number(m.caution_tests !== undefined ? m.caution_tests : (m.attention_count || 0));
        const danger = Number(m.high_risk_tests !== undefined ? m.high_risk_tests : (m.danger_count || 0));

        const hasCounts = (safe + attention + danger) > 0;
        const pieLabels = state.language === 'te'
            ? ['సురక్షితం', 'శ్రద్ధ అవసరం', 'ప్రమాదకరం']
            : (state.language === 'hi'
                ? ['सुरक्षित', 'सावधानी', 'उच्च जोखिम']
                : ['Safe for Use', 'Needs Attention', 'High Risk']);

        state.charts.pie = new Chart(pieCanvas, {
            type: 'doughnut',
            data: {
                labels: pieLabels,
                datasets: [{
                    data: hasCounts ? [safe, attention, danger] : [1, 0, 0],
                    backgroundColor: ['#10B981', '#F59E0B', '#EF4444'],
                    borderWidth: 2,
                    borderColor: '#FFFFFF'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { font: { weight: '600' } }
                    }
                }
            }
        });
    }
}

// ===================================================================
// Batch Lookup & QR Verification
// ===================================================================
async function lookupBatch() {
    const input = document.getElementById('lookup-batch-input');
    const batchId = (input.value || '').trim();
    if (!batchId) {
        alert('Please enter a Batch ID to search.');
        return;
    }

    try {
        const resp = await fetch(`/api/passport/${batchId}`);
        if (!resp.ok) {
            alert(`Batch '${batchId}' not found in audit registry.`);
            return;
        }

        const data = await resp.json();
        renderLookupResult(data.passport, data.qr_base64);
    } catch (e) {
        alert(`Lookup failed: ${e.message}`);
    }
}

async function handleQRUpload(event) {
    if (!event.target.files || event.target.files.length === 0) return;
    const file = event.target.files[0];

    const placeholder = document.getElementById('lookup-result-placeholder');
    const detailsBox = document.getElementById('lookup-result-details');
    if (placeholder) {
        placeholder.style.display = 'block';
        placeholder.innerHTML = '⏳ <strong>Verifying QR & Querying Database...</strong>';
    }
    if (detailsBox) detailsBox.style.display = 'none';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const resp = await fetch('/api/passport/verify-qr', {
            method: 'POST',
            body: formData
        });

        if (!resp.ok) {
            const errData = await resp.json().catch(() => ({}));
            const errDetail = errData.detail || 'No valid SmartFeed QR code found in uploaded image.';
            if (placeholder) {
                placeholder.innerHTML = `<span style="color: var(--crimson-danger); font-weight: 700;">⚠️ ${errDetail}</span><br><small style="color: var(--slate-500);">Please upload a valid SmartFeed QR code image.</small>`;
            }
            alert(errDetail);
            return;
        }

        const data = await resp.json();
        renderLookupResult(data.passport, data.qr_base64, data.verified_in_database);
    } catch (e) {
        if (placeholder) {
            placeholder.innerHTML = `<span style="color: var(--crimson-danger); font-weight: 700;">⚠️ QR Verification error: ${e.message}</span>`;
        }
        alert(`QR Verification error: ${e.message}`);
    }
}

function renderLookupResult(passport, qrBase64, isVerified = true) {
    const placeholder = document.getElementById('lookup-result-placeholder');
    if (placeholder) placeholder.style.display = 'none';

    const box = document.getElementById('lookup-result-details');
    if (!box || !passport) return;
    box.style.display = 'block';

    const badgeClass = isVerified ? 'badge-safe' : 'badge-caution';
    const badgeText = isVerified ? '🟢 VERIFIED IN AUDIT REGISTRY' : '🟡 DECODED FROM QR (UNREGISTERED)';
    const scoreVal = passport.quality_score !== undefined ? `${Math.round(passport.quality_score)} / 100` : '--';
    const dateStr = (passport.timestamp || '').replace('T', ' ').slice(0, 16);

    box.innerHTML = `
        <div style="background: var(--slate-50); border: 1.5px solid ${isVerified ? 'var(--primary-emerald)' : 'var(--amber-500)'}; border-radius: var(--radius-md); padding: 22px; box-shadow: var(--shadow-sm);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 8px;">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; font-weight: 800; color: var(--accent-blue);">
                    ${passport.batch_id}
                </span>
                <span class="safety-badge ${badgeClass}" style="padding: 5px 14px; font-size: 0.82rem;">
                    ${badgeText}
                </span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; font-size: 0.94rem; margin-bottom: 14px;">
                <div><strong style="color: var(--slate-600);">Sample Classification:</strong> <div style="font-weight: 700; color: var(--slate-800);">${passport.sample_type || 'Feed Sample'}</div></div>
                <div><strong style="color: var(--slate-600);">Health Score:</strong> <div style="font-weight: 800; color: var(--primary-emerald); font-size: 1.05rem;">${scoreVal}</div></div>
                <div><strong style="color: var(--slate-600);">Safety Status:</strong> <div style="font-weight: 700;">${passport.quality_badge || passport.overall_risk || 'Normal'}</div></div>
                <div><strong style="color: var(--slate-600);">Recorded Timestamp:</strong> <div style="font-family: monospace; color: var(--slate-700);">${dateStr || 'Recent'}</div></div>
                ${passport.shelf_life_days !== undefined ? `<div><strong style="color: var(--slate-600);">Shelf Life & Expiry:</strong> <div style="font-weight: 700; color: ${passport.shelf_life_days > 0 ? 'var(--primary-emerald)' : 'var(--crimson-danger)'};">${passport.shelf_life_days} Days (${passport.shelf_life_status || 'Safe'}${passport.safe_until_date ? ' - ' + passport.safe_until_date : ''})</div></div>` : ''}
                ${passport.primary_concern ? `<div style="grid-column: span 2;"><strong style="color: var(--slate-600);">Primary Concern:</strong> <div style="color: var(--slate-800); font-weight: 600;">${passport.primary_concern}</div></div>` : ''}
            </div>
            ${qrBase64 ? `<div style="text-align: center; margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--slate-200);"><img src="${qrBase64}" style="width: 110px; height: 110px; border-radius: 8px; border: 1px solid var(--slate-200); background: #FFFFFF; padding: 4px;"><div style="font-size: 0.72rem; color: var(--slate-500); margin-top: 4px;">Official Tamper-Evident QR</div></div>` : ''}
        </div>
    `;
}
