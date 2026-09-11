# 🐄 SmartFeed AI: Complete Project Architecture & Technical Guide
> **Comprehensive Guide for Developers, Teammates, and Evaluators**  
> *Everything you need to know about SmartFeed AI: system architecture, dual-portal segregation, AI vision math, database schemas, and how to run & test it.*

---

## 🎯 1. Project Overview & Problem Statement

### The Agricultural Crisis in Livestock Nutrition
Rural smallholder dairy farmers, cooperative societies, and gaushalas across India face devastating economic losses, sudden drops in milk yield, and cattle mortality due to degraded or adulterated cattle feed:
1. **Fungal & Mould Mycotoxins**: High-humidity storage triggers fungal mycelium blooms (*Aspergillus flavus*) producing deadly aflatoxins. Ingestion causes acute milk yield drops (up to 40%), severe liver damage, and fatal poisoning.
2. **Urea (Chemical) Adulteration**: Feed suppliers illegally spike cattle feed with cheap fertilizer urea (46% nitrogen) to falsely inflate apparent Crude Protein readings on basic tests, triggering fatal rumen alkalosis in ruminants.
3. **Imbalanced Feeding**: Farmers lack scientific guidance on balanced daily rations (concentrates, green fodder, dry fodder) tailored to cow/buffalo body weight, lactation stages, and daily milk yield.
4. **Hardware & Testing Costs**: Smallholder farmers cannot afford expensive NIR spectrometers ($5,000+) or IoT lab kits.
5. **Lack of Traceability**: When cattle fall sick, there is zero digital audit trail linking the feed batch to supplier quality records.
6. **Cooperative Blind Spots**: District dairy unions lack real-time digital surveillance across villages, making it impossible to detect regional contamination outbreaks or dispatch urgent advisories.

### The Solution: SmartFeed AI
SmartFeed AI is a **100% software-first, offline-ready AI diagnostic and dairy management platform** that turns any smartphone or computer into an intelligent feed testing laboratory. It features:
- **Computer Vision (OpenCV + MobileNetV2)**: Detects discoloration %, fungal mycelium textures, dark charred patches, and foreign debris.
- **Biochemical Adulteration Screening**: Calculates Non-Protein Nitrogen (NPN) ratios to uncover urea spiking and evaluates safe feeding thresholds.
- **ICAR Safe Urea Straw & Feed Calculator**: Computes scientific 4% urea straw ammoniation protocols (boosting crude protein from 3.5% to 8.5%) and enforces a strict 1% NPN maximum in concentrate mixes.
- **100% Offline Rule-Based Veterinary Advisor**: Native Telugu symptom matcher providing immediate clinical first aid for Bloat, Acidosis, Ketosis, Mastitis, Milk Fever, and Urea Poisoning.
- **Nutritional Verification**: Compares Protein, Moisture, and Fiber against Bureau of Indian Standards (BIS Type I & Type II / IS 2052) and ICAR benchmarks.
- **Multi-Factor Risk Engine (0–100 Score)**: Delivers a transparent health score with itemized point deductions ("Why this result?").
- **Animal-Specific Ration Balancer**: Calculates tailored daily feed allowance (kg) and balanced rations for Cows and Buffaloes based on body weight, pregnancy, and milk yield.
- **Time-Based Daily Feeding Planner & Diary**: Morning, Noon, and Evening slot breakdown with daily nutrition intake tracking and hydration reminders.
- **Tamper-Evident QR Digital Passport**: Auto-generates unique sequential Batch IDs (`SFA-YYYY-XXXXXX`) and verifies uploaded QR photos via multipart image decoding.
- **District Dairy Cooperative Admin Command Center**: A dedicated executive portal with live cooperative KPIs, multi-village farmer registries, searchable batch audit logs, village risk heatmaps, and emergency broadcast dispatch.
- **Early Spoilage Trajectory Warnings**: Analyzes consecutive batch trends to alert farmers to moisture and quality deterioration before visible rot forms.
- **Zero-Latency Multilingual Voice**: Localized guidance in **English**, **తెలుగు (Telugu)**, and **हिंदी (Hindi)** with native Web Speech TTS and persistent state synchronization.

---

## 🛠️ 2. Comprehensive Technical Tools & Technology Stack

SmartFeed AI is engineered using industry-standard tools and libraries spanning backend, computer vision, data storage, frontend UI, and automated QA:

| Domain / Layer | Technical Tools & Libraries | Key Versions / Specs | Specific Role in SmartFeed AI |
| :--- | :--- | :--- | :--- |
| **Programming Languages** | **Python**, **JavaScript (ES6+)**, **HTML5 / CSS3**, **SQL** | Python 3.10+, Modern JS | Core backend logic, CV algorithms, reactive single page web frontend, responsive design, and database queries. |
| **Backend & REST APIs** | **FastAPI**, **Uvicorn**, **Pydantic**, **Starlette** | ASGI Framework | Production asynchronous REST API server handling multipart image uploads, payload validation, and static asset delivery. |
| **Computer Vision & AI** | **OpenCV (`cv2`)**, **NumPy**, **Pillow (`PIL`)**, **PyTorch / Torchvision**, **Scikit-Learn** | OpenCV 4.8+, NumPy 1.24+ | Image HSV color space extraction, discoloration detection, Canny edge mycelium texture analysis, matrix operations, and ML defect classification. |
| **Biochemical Standards** | **BIS Standards (IS 2052)**, **ICAR Guidelines**, **NPN Stoichiometric Ratio** | BIS Type I & II | Verification of crude protein, moisture, and fiber against Indian national norms. Mathematical detection of urea adulteration (46% nitrogen). |
| **Veterinary Decision Support** | **Rule-Based Diagnostic Trees**, **Telugu Symptom Knowledgebase** | 100% Offline | Instant clinical first aid protocols for acute cattle disorders without requiring cloud LLM connectivity. |
| **Ration & Nutrition Engine** | **ICAR / NDDB Formulas**, **Dry Matter Balancer** | Domain Standard Formulas | Animal-specific energy and protein calculation based on species (Cow/Buffalo), body weight, lactation status, and daily milk yield. |
| **Database & Persistence** | **SQLite 3**, **JSON Storage** | Embedded Relational DB | Serverless, zero-maintenance database (`smartfeed.db`) storing user accounts, farm setups, animal profiles, batch tests, feeding logs, and broadcast alerts. |
| **Traceability & Barcodes** | **`qrcode` (Python)**, **OpenCV `QRCodeDetector`** | Matrix Barcode Decoders | Generates tamper-evident batch QR codes and decodes uploaded batch photos using multi-stage grayscale/Otsu threshold fallback. |
| **Frontend UI Architecture** | **Vanilla CSS Grid/Flexbox**, **Chart.js 4.4.0 (Offline)** | Viewport-Bounded Layout | Total viewport containment (`calc(100vw - var(--sidebar-width))`), auto-fit KPI grids, `.admin-table-container` horizontal touch scrolling, and 100% offline trend charts. |
| **Multilingual Voice / TTS** | **Web Speech API (`SpeechSynthesis`)** | W3C Browser Audio | Reads AI recommendations out loud in Telugu, Hindi, or English directly in the browser with zero cloud latency and `localStorage` persistence. |
| **Testing & Quality Assurance**| **Python `unittest`** + **End-to-End Audit** | Automated Suites | **86 unit tests passed (100% OK)** in ~46s; **34-point exhaustive system audit passed (100% OK)** covering every endpoint and workflow. |

---

## 📊 3. Datasets & Domain Standards Used

SmartFeed AI integrates real agricultural research data and national standards:

| Dataset / Benchmark | Source & Location | Classes / Benchmarks | How It is Used in SmartFeed AI |
| :--- | :--- | :--- | :--- |
| **1. Mendeley Grain Defects Dataset** | Open Research Dataset<br>`data/grain_defects/` | • `good` (Clean, normal feed)<br>• `moldy` (Fungal mycelium / spores)<br>• `burnt` (Charred, blackened grains)<br>• `pecky` (Punctured / insect damage)<br>• `scorched` (Heat-damaged / off-color)<br>• `greenish` (Immature grains) | Used for training MobileNetV2 transfer learning model and tuning OpenCV HSV / edge detection thresholds for raw feed ingredient inspection. |
| **2. Silage Preservation Quality Dataset** | Agricultural Forage Dataset<br>`data/silage/` | • `fresh` (Olive-green, firm structure, lactic aroma)<br>• `spoiled` (Slimy, dark rot, fungal patches) | Used for training silage fermentation binary classification model to detect spoiled livestock silage. |
| **3. BIS & ICAR Nutrient Reference Dataset** | Bureau of Indian Standards & ICAR<br>`data/nutrient_reference.csv` | • Compound Cattle Feed (BIS Type I & II)<br>• Feed Ingredients (Grains, Brans, Cakes)<br>• Silage (Fermented forage)<br>• Dry Fodder (Straw / stover)<br>• Green Fodder (Berseem, Napier) | Official nutritional benchmark ranges for Crude Protein (min 20–22%), Moisture (max 11–14%), and Crude Fiber (max 7–10%). Used by `nutrition.py` and `adulteration.py` to flag protein deficits and urea spiking. |
| **4. ICAR & NDDB Dairy Feeding Norms** | Indian Council of Agricultural Research | • Cow Maintenance: ~1.5–2.0 kg concentrate<br>• Milk Production: ~0.4 kg concentrate per litre milk<br>• Buffalo Maintenance: ~2.0–2.5 kg concentrate<br>• Milk Production: ~0.5 kg concentrate per litre milk<br>• Pregnancy Allowance: +1.0–1.5 kg concentrate | Used by `ration_engine.py` to dynamically compute balanced feed allowance and green/dry fodder ratios. |
| **5. ICAR Straw Ammoniation Standard** | ICAR National Dairy Research Institute | • 4 kg Urea dissolved in 40 Litres Water per 100 kg Dry Straw<br>• 21-Day airtight anaerobic stacking<br>• Boosts crude protein from 3.5% to 8.5% and improves digestibility by 10-15% | Used by `server.py` (`/api/safe-urea-calculator`) to provide exact step-by-step treatment guidance to farmers. |
| **6. Adaptive OpenCV Vision Fallback** | Algorithmic Fallback Engine<br>`utils/cv_analysis.py` | Real-time mathematical feature extraction (HSV color balance, Canny texture roughness, non-feed debris contours) | Guarantees that SmartFeed AI runs 100% reliably on low-power village computers without requiring expensive GPU hardware or heavy model weights. |

---

## 📁 4. Complete Folder & File Directory Map

| Folder | File Path | Language / Tech | Primary Function & Code Role |
| :--- | :--- | :--- | :--- |
| **Root** | `server.py` | Python (FastAPI) | Production backend server. Exposes 20+ REST API endpoints (`/api/scan`, `/api/check-adulteration`, `/api/safe-urea-calculator`, `/api/farmer-problems`, `/api/advisory`, `/api/animal-recommendation`, `/api/feed-diary/*`, `/api/dashboard`, `/api/passport/*`, `/api/auth/*`, `/api/admin/*`) and hosts the static single-page frontend. |
| **Root** | `smartfeed.db` | SQLite Database | Production database storing users, farm configurations, animal cards, batch scan tests, daily feeding logs, and broadcast alerts. Pre-seeded with Admin (`8341016049 / 6049`). |
| **Root** | `PROJECT_GUIDE.html` | HTML5 / CSS3 | Self-contained, responsive presentation webpage for opening in any browser and sharing with evaluators and teammates. |
| **Root** | `PROJECT_GUIDE.md` | Markdown | Comprehensive developer and evaluator architectural guide. |
| **Root** | `README.md` | Markdown | Master project README with SIH documentation. |
| **`db/`** | `db/database.py` | Python | Database layer: initializes SQLite schemas (`users`, `farms`, `animals`, `tests`, `feeding_diary`, `broadcasts`), generates sequential batch IDs (`SFA-YYYY-XXXXXX`), performs CRUD operations, and includes `wipe_all_except_admin()` helper. |
| **`utils/`** | `utils/cv_analysis.py` | Python (OpenCV) | Computer Vision engine: computes discoloration %, HSV color space distribution, Canny edge texture anomalies, and foreign particle/mould indicators. |
| **`utils/`** | `utils/inference.py` | Python (PyTorch / Heuristic) | ML inference module: classifies feed and silage categories with a robust heuristic image fallback for low-power edge devices. |
| **`utils/`** | `utils/adulteration.py` | Python | Urea and adulteration simulator: calculates Non-Protein Nitrogen to Crude Protein ratios and detects visual chalk/powder adulterants. |
| **`utils/`** | `utils/nutrition.py` | Python | Nutritional assessment: checks Crude Protein (CP%), Moisture%, Crude Fiber%, and NPN against BIS standard ranges. |
| **`utils/`** | `utils/risk_engine.py` | Python | Multi-Factor Risk Intelligence: evaluates 6 risk factors to generate the **0–100 SmartFeed Health Score**, safety badges, and itemized deduction reasons. |
| **`utils/`** | `utils/ration_engine.py` | Python | Animal-Specific Ration Balancer: computes daily concentrate allowance (kg), green fodder, and dry fodder requirements based on animal species, body weight, lactation status, and milk yield. |
| **`utils/`** | `utils/feeding_planner.py` | Python | Time-Based Daily Feeding Planner: splits daily ration into Morning (35%), Noon (25%), and Evening (40%) slots; provides compliance tracking and water intake reminders. |
| **`utils/`** | `utils/advisory.py` | Python | Farmer advisory generator: produces multilingual advice (Telugu, Hindi, English) for 1-click common queries and custom questions. |
| **`utils/`** | `utils/qr_utils.py` | Python (qrcode & OpenCV) | Digital Passport engine: generates high-contrast QR codes and decodes uploaded QR images with multi-stage (RGB, Grayscale, Otsu binarization) fallback. |
| **`utils/`** | `utils/analytics.py` | Python | Trend analytics and Early Spoilage Trajectory engine: detects consecutive batch deterioration before visible mould appears. |
| **`web/`** | `web/index.html` | HTML5 | Single Page Application layout: Splash Screen, Language Selection, Role-Based Auth Gate, 4-Step Farm Setup Wizard, Farmer Toolset, and District Cooperative Admin Command Center. |
| **`web/css/`** | `web/css/style.css` | CSS3 | Responsive emerald UI styling: bounded main viewport, auto-fit KPI grids, touch-scroll table containers, and mobile drawer support. |
| **`web/js/`** | `web/js/app.js` | JavaScript | Frontend engine: dynamic role-based sidebar (`renderSidebarNav`), tab switching, API fetch requests, drag-and-drop file upload, full translation dictionary, and persistent language storage. |
| **`web/js/`** | `web/js/chart.min.js` | JavaScript | Bundled Chart.js library ensuring 100% offline-ready trend line and safety doughnut charts. |
| **`tests/`** | `tests/test_*.py` | Python (unittest) | 86 unit, API, and live integration test cases across 16 test files verifying all modules end-to-end (100% passed). |
| **`scratch/`**| `scratch/audit_entire_system.py` | Python | Exhaustive 34-point integration script testing every REST API endpoint, HTML structure, and auth journey (100% passed). |

---

## 🧠 5. The 6-Factor Risk Intelligence Algorithm & Scoring Math

The SmartFeed AI Health Score starts at a pristine **100 points** and applies transparent, mathematically calibrated penalties across 6 biological, chemical, and physical risk factors:

$$\text{Health Score} = 100 - \sum_{i=1}^{6} \text{Penalty}_i$$

| Factor # | Risk Factor Evaluated | Detection Source | Mathematical Condition | Score Deduction | Safety Impact |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1** | **Visual Mould & Fungal Growth** | OpenCV HSV + Texture | Canny texture roughness $> 25\%$ or Discoloration $> 15\%$ | **-25 to -35 pts** | Prevents aflatoxin poisoning and acute milk drop. |
| **2** | **Chemical Urea Spiking** | Stoichiometric NPN Ratio | $\text{NPN} / \text{CP} > 0.35$ or $\text{Urea} > 1\%$ | **-25 to -35 pts** | Prevents fatal rumen alkalosis and ammonia toxicity. |
| **3** | **Excess Moisture Content** | Numerical / Sensor Metric | Moisture $> 14.0\%$ (BIS IS:2052 Max Limit) | **-15 to -20 pts** | Flags active microbial decomposition and storage spoilage. |
| **4** | **Crude Protein Deficit** | BIS Benchmark Comparison | $\text{CP} < 20.0\%$ (BIS Type II Minimum) | **-10 to -15 pts** | Prevents protein malnutrition and poor lactation persistence. |
| **5** | **Excess Crude Fiber / Foreign Matter** | Physical Contour Analysis | $\text{CF} > 12.0\%$ or Non-feed inclusion count $> 5$ | **-10 to -15 pts** | Detects sawdust, sand, or inedible crop residue fillers. |
| **6** | **Consecutive Batch Degradation** | 5-Batch Trend Slope | Score drop $> 10\text{ pts}$ over 3 consecutive batches | **-10 pts** | Early warning before visible mold colonies form. |

### Classification Verdicts
- 🟢 **80 – 100 Score**: **SAFE** (Approved for daily livestock feeding)
- 🟡 **50 – 79 Score**: **CAUTION** (Moderate risk; adjust ration, aerate, or dilute)
- 🔴 **0 – 49 Score**: **HIGH RISK / UNSAFE** (Reject batch; chemical contamination or toxic mould)

---

## ✨ 6. Ten Integrated Core Systems & Innovations

SmartFeed AI integrates 10 high-impact systems into a cohesive, user-friendly platform:

### 1. Onboarding, Auth & Farm Setup Wizard
- Progressive 3-screen entry (Splash Screen $\to$ Language Selector $\to$ Role-Based Auth).
- Pre-configured Admin 1-Click (`8341016049 / 6049`) for instant evaluator review.
- 4-step guided setup wizard for new farmers: Location, Main Feed Type, Herd Count, and Individual Cattle Cards (Cow/Buffalo, Age, Lactation Status, Milk Yield).

### 2. Feed Quality Vision Scanner
- Multi-factor computer vision pipeline combining HSV color space segmentation, Canny edge mycelium texture analysis, and MobileNetV2 defect classification.
- Delivers instantaneous quality classification, visual defect highlights, and an itemized deduction ledger.

### 3. Biochemical Urea & NPN Screening
- Analyzes the ratio of Non-Protein Nitrogen (NPN) to apparent Crude Protein.
- Uncovers artificial protein inflation from illicit agricultural fertilizer blending (urea is 46% nitrogen).

### 4. ICAR Safe Urea Straw & Feed Calculator
- Implements the official ICAR/NDRI Straw Ammoniation Protocol:
  - 4 kg Urea dissolved in 40 Litres Water per 100 kg Dry Straw.
  - 21-day airtight polythene curing improves crude protein from 3.5% to 8.5% and boosts digestibility by 10-15%.
- Formulates safe concentrate feeds enforcing the strict 1% NPN maximum limit with automatic toxicity alerts.

### 5. 100% Offline Rule-Based Veterinary Advisor
- Native Telugu symptom matcher for common livestock ailments:
  - *కడుపు ఉబ్బరం (Bloat / Tympany)*: Vegetable oil + ginger first aid.
  - *అసిడోసిస్ (Rumen Acidosis)*: Sodium bicarbonate drenching.
  - *కీటోసిస్ (Ketosis)*: Jaggery / oral glucose therapy.
  - *పాల జ్వరం (Milk Fever)*: Calcium borogluconate protocol.
  - *పొదుగు వాపు (Mastitis)*: Immediate milking, cold compress, intramammary antibiotics.
  - *యూరియా విషం (Urea Toxicity)*: Vinegar drenching (weak acid to neutralize rumen ammonia).

### 6. Animal-Specific Ration Balancer
- Dynamically computes tailored daily concentrate, green fodder, and dry fodder allowances based on species (Cow vs. Buffalo), body weight, lactation status, and daily milk yield in litres using ICAR and NDDB norms.

### 7. Time-Based Smart Daily Feeding Planner & Diary
- Splits the daily ration into optimal feeding slots: Morning (35%), Noon (25%), Evening (40%).
- Digital diary tracking intake compliance, highlighting feeding deficits, and providing daily hydration reminders.

### 8. Tamper-Evident QR Digital Feed Passport
- Generates a unique sequential batch identifier (`SFA-YYYY-XXXXXX`) and a high-contrast QR code for every inspected batch.
- Allows buyers, cooperatives, or veterinarians to verify batch test records by either scanning or uploading a QR code photo.

### 9. Analytical Risk Intelligence Dashboard
- Live visual analytics powered by offline Chart.js: 30-day health trends, risk distribution doughnut, and early spoilage trajectory alarms.

### 10. District Dairy Union Cooperative Admin Command Center
- **Dedicated Executive Oversight Portal** featuring 6 specialized tools:
  1. 🏛️ **Cooperative Overview**: Global KPIs, total registered dairy farmers, aggregate livestock population, and quick alert dispatch.
  2. 👥 **Farmer Master Registry**: Multi-village farmer directory displaying village locations, cattle breakdown, and primary feed types.
  3. 🔬 **District Batch Audit Log**: Complete ledger of all feed tests conducted across the cooperative, with search and status filters.
  4. 🗺️ **Village Risk Surveillance**: Village-level contamination risk matrix identifying local hotspots before outbreaks spread.
  5. 📢 **Broadcast Advisories**: Cooperative-wide urgent alert dispatch system and real-time advisory stream.
  6. ⚖️ **BIS IS:2052 Standards**: Comprehensive national specifications for Cattle Feed Type I & Type II.
- **Responsive Architecture**: Bounded viewport (`calc(100vw - var(--sidebar-width))`), auto-fit KPI grids, and smooth horizontal touch-scrolling data table wrappers (`.admin-table-container`).

---

## 🔄 7. Step-by-Step Data Flow (End-to-End Pipeline)

```
[ 1. User Opens Application: http://localhost:8000/ ]
                       │
                       ▼
[ 2. Splash Screen & Language Selection ]
  • Synchronized dropdowns (Header & Sidebar)
  • English, Telugu (తెలుగు), or Hindi (हिंदी)
  • Saved to localStorage; zero language mixing
                       │
                       ▼
[ 3. Role-Based Auth Gate ]
  ├── [ ADMIN LOGIN ] ──> Enter 8341016049 / 6049
  │                         │
  │                         ▼
  │               [ ADMIN COMMAND CENTER ]
  │               • Cooperative Overview & KPIs
  │               • Multi-Village Farmer Registry
  │               • Cooperative Batch Audit Ledger
  │               • Village Risk Surveillance Heatmap
  │               • Emergency Broadcast Dispatcher
  │               • BIS IS:2052 Quality Standards
  │
  └── [ FARMER LOGIN / REGISTRATION / GUEST ]
                            │
                            ▼
                  [ 4-Step Farm Setup Wizard ]
                  • Location & Language
                  • Feed Type & Storage
                  • Herd Count (Cows & Buffaloes)
                  • Individual Cattle Cards
                            │
                            ▼
                  [ FARMER TOOL SUITE ]
                  ├── 1. Feed Quality Vision Scanner (/api/scan)
                  ├── 2. Biochemical Adulteration Screening (/api/check-adulteration)
                  ├── 3. ICAR Safe Urea Straw Calculator (/api/safe-urea-calculator)
                  ├── 4. Offline Veterinary AI Advisor (/api/advisory)
                  ├── 5. Animal Ration Balancer (/api/animal-recommendation)
                  ├── 6. Daily Feeding Planner & Diary (/api/feed-diary/*)
                  ├── 7. Risk Intelligence Dashboard (/api/dashboard)
                  └── 8. QR Feed Passport Verification (/api/passport/*)
```

---

## 💡 8. Top Presentation & Viva Voce Questions

### Q1: How does SmartFeed AI detect Urea adulteration without sensors?
**Answer:** In cattle feed, protein is measured as Crude Protein via total nitrogen. Unscrupulous suppliers add cheap industrial fertilizer (urea, which is 46% nitrogen) to fake high protein readings. SmartFeed AI analyzes the ratio of **Non-Protein Nitrogen (NPN) to total apparent crude protein**. Natural cattle feed contains only small amounts of natural NPN. If the NPN ratio spikes beyond biological safety levels ($> 0.35$ or $> 1\%$ urea in concentrate), the system flags **Urea Spiking / Adulteration**, protecting cows from fatal rumen alkalosis.

### Q2: Why is the SmartFeed Health Score designed as a 0–100 scale?
**Answer:** Dairy farmers find technical units (such as ppm, percentages, and HSV histograms) hard to interpret under field conditions. A single 0–100 score gives an instant, intuitive verdict:
- **80 – 100**: 🟢 **SAFE** (Good quality feed)
- **50 – 79**: 🟡 **CAUTION** (Moderate risk; feed with adjustments)
- **0 – 49**: 🔴 **UNSAFE** (High risk; do not feed to cattle)  
Crucially, our **Explainable AI** module prints exact point deductions (e.g. *"-25 pts: Urea adulteration detected"*, *"-15 pts: High moisture 15.2%"*), ensuring complete transparency.

### Q3: How does the Animal Ration Balancer calculate feed requirements?
**Answer:** In `utils/ration_engine.py`, we implement official **ICAR and NDDB nutritional standards**:
- **Maintenance Requirement**: Based on animal species (Cow vs. Buffalo) and body weight (e.g. 1.5–2.0 kg concentrate for a 400 kg cow, 2.0–2.5 kg for a buffalo).
- **Production Allowance**: ~0.4 kg concentrate per litre of cow milk; ~0.5 kg per litre of higher-fat buffalo milk.
- **Pregnancy Allowance**: Additional +1.0–1.5 kg concentrate in the last trimester.
- **Ration Balancing**: Automatically computes optimal daily Green Fodder (e.g. 15–20 kg) and Dry Fodder (e.g. 4–6 kg) to ensure optimal rumen fermentation and prevent acidosis.

### Q4: How does the Time-Based Daily Feeding Planner work?
**Answer:** In `utils/feeding_planner.py`, the daily feed allocation is divided into optimal time slots:
- **Morning Slot (35%)**: High energy concentrate + portion of green fodder after morning milking.
- **Noon Slot (25%)**: Dry fodder and digestive roughage.
- **Evening Slot (40%)**: Balanced concentrate + remaining green fodder before evening milking.
Farmers log actual feed fed in the **Feed Diary**, which highlights deficit/surplus compliance against recommendations and gives daily hydration reminders.

### Q5: How does the Digital Feed Passport QR system work?
**Answer:** Each inspection creates an audit entry in `smartfeed.db` and assigns a sequential identifier like `SFA-2026-000008`. A high-contrast QR code is generated embedding this record. Any buyer, dairy cooperative, or veterinarian can scan or upload this QR code in the **Batch Lookup** tab to verify the feed's authentic test history and safety score.

### Q6: Does SmartFeed AI require the internet to function?
**Answer:** No, the system is **100% offline-ready**:
- Computer vision runs locally using OpenCV.
- Database runs locally using SQLite (`smartfeed.db`).
- Visual charts are powered by locally bundled `chart.min.js`.
- Voice playback uses the browser's built-in Web Speech API without external cloud fees or delays.
- Veterinary advisory uses offline diagnostic trees.

### Q7: How does the Cooperative Admin Command Center differ from the Farmer Portal?
**Answer:** SmartFeed AI uses dynamic role-based navigation via `renderSidebarNav(role)`:
- **When logged in as Admin (`8341016049` / `6049`)**: Farmer-centric tools (Scanner, Urea Checker, Ration Balancer) are hidden. The sidebar presents 6 dedicated executive tools: Cooperative Overview, Farmer Master Registry, District Batch Audit Log, Village Risk Surveillance Matrix, Emergency Broadcast Stream, and BIS IS:2052 Standards.
- **When logged in as a Farmer**: The sidebar displays 7 day-to-day farm management tools.
- Data tables in the Admin portal are wrapped in responsive `.admin-table-container` divs with smooth horizontal scrolling to prevent viewport spill.

### Q8: How does the ICAR Safe Urea Straw Ammoniation Calculator work?
**Answer:** In rural India, feeding untreated dry paddy or wheat straw leads to poor nutrition because straw is low in crude protein (~3.5%) and high in indigestible lignin. SmartFeed AI provides the official **ICAR 4% Urea Treatment Protocol**:
1. Dissolve 4 kg fertilizer urea in 40 litres of water for every 100 kg dry straw.
2. Sprinkle uniformly layer by layer.
3. Seal airtight under polythene or mud plaster for 21 days.
4. Aerate before feeding. This breaks lignocellulose bonds, doubles crude protein to 8.5%, and increases milk yield by 1–2 litres per cow.

### Q9: How is language preference preserved without resetting across logins?
**Answer:** We eliminated intrusive modal popup buttons. The user selects English, Telugu, or Hindi using synchronized dropdowns in the header or sidebar. The choice is instantly committed to `localStorage.setItem('smartfeed_lang', lang)`. When the user logs in as a Farmer or Admin, the login handler preserves the user's active language preference rather than overriding it with database defaults.

---

## ▶️ 9. How to Run and Test the Project

### 1. Launch the Production Web Application
```powershell
python -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```
Open your browser and navigate to:
👉 **`http://localhost:8000/`**

### 2. Run All 86 Automated Unit Tests
```powershell
python -m unittest discover tests/ "test_*.py"
```
*Expected result: 86 tests run successfully (`OK`).*

### 3. Run Full 360° System Integration Audit (34 Modules)
```powershell
python scratch/audit_entire_system.py
```
*Expected result: All 34 system modules and API routes verified and 100% operational.*

### 4. Open the Presentation Guide in Any Browser
Double-click **`PROJECT_GUIDE.html`** in your file explorer, or open it directly in Google Chrome, Microsoft Edge, or Safari!
