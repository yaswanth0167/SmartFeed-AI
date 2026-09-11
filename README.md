# 🐄 SMARTFEED AI
### AI-Powered Smart Cattle Feed & Silage Quality Assessment, Risk Intelligence, Ration Balancer & Traceability System
**Smart India Hackathon (SIH) — AI & Agriculture Innovation**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Production%20REST%20API-009688.svg)](https://fastapi.tiangolo.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8.svg)](https://opencv.org/)
[![Unit Tests](https://img.shields.io/badge/Unit%20Tests-86%20Passed%20(100%25)-brightgreen.svg)]()
[![System Audit](https://img.shields.io/badge/System%20Audit-34%2F34%20Operational-success.svg)]()
[![Multilingual](https://img.shields.io/badge/Languages-EN%20%7C%20TE%20%7C%20HI-orange.svg)]()
[![Offline Mode](https://img.shields.io/badge/Offline%20Mode-100%25%20Functional-28a745.svg)]()

---

## 🎯 1. Problem Statement & Solution

### The Crisis in Livestock Nutrition
Smallholder dairy farmers, rural dairy cooperatives, and gaushalas across India suffer severe economic losses and animal health emergencies due to poor quality, degraded, and adulterated cattle feed:
1. **Fungal & Mould Mycotoxins**: Moisture ingress during humid storage produces dangerous fungal mycelium and aflatoxins, causing acute milk yield drops (up to 40%), liver failure, and cattle mortality.
2. **Urea & NPN Adulteration**: Unethical manufacturers illicitly blend industrial chemical fertilizer (urea, 46% nitrogen) into cattle feed to fake high protein readings (Crude Protein), causing fatal rumen alkalosis and ammonia toxicity.
3. **Imbalanced Daily Rations**: Farmers feed cattle without balancing dry matter, crude protein, and green/dry fodder proportions according to lactation status and milk yield, causing metabolic disorders.
4. **Lack of Digital Traceability**: When cattle fall ill or milk production collapses, there is zero verifiable trail linking feed batches to supplier safety records.
5. **Administrative Disconnect**: District dairy unions lack real-time digital surveillance across villages, unable to track local contamination outbreaks or broadcast emergency feed advisories before epidemics spread.

### The SmartFeed AI Solution
SmartFeed AI is a **100% software-first, low-cost AI diagnostic and dairy decision-support platform** that turns any smartphone or computer into an intelligent feed testing laboratory without requiring expensive spectrometers or IoT hardware:
- **Computer Vision (MobileNetV2 + OpenCV)**: Discoloration %, fungal mycelium textures, dark charred patches, and foreign particle detection.
- **Biochemical Adulteration Screening**: Stoichiometric Non-Protein Nitrogen (NPN) calculation and safe urea dosage limits.
- **ICAR Safe Urea Straw & Feed Calculator**: Formulates scientific 4% urea straw ammoniation protocols and enforces strict 1% NPN maximum concentrate mixing.
- **Offline Rule-Based Veterinary Advisory**: 100% offline diagnostic decision tree with native Telugu symptom matching for rapid emergency first aid.
- **Simulated Nutrient Profiling**: Evaluates Crude Protein (CP), Moisture, and Fiber against Bureau of Indian Standards (BIS Type I & II / IS 2052) and ICAR norms.
- **Multi-Factor Risk Intelligence Engine**: Computes a transparent **0–100 SmartFeed Health Score** with itemized deduction explanations ("Why This Result?").
- **Animal-Specific Feed Recommendation**: Calculates tailored daily feed allowance (kg) and balanced rations for Cows and Buffaloes based on body weight, pregnancy, and milk yield.
- **Time-Based Smart Feeding Planner & Diary**: Morning, Noon, and Evening slot breakdown with daily nutrition intake tracking.
- **Tamper-Evident QR Digital Feed Passport**: Auto-generates unique sequential Batch IDs (`SFA-YYYY-XXXXXX`) with instant multipart QR image verification.
- **District Dairy Union Cooperative Admin Command Center**: Segregated executive command portal offering live cooperative KPIs, multi-village farmer registries, batch audit ledgers, risk heatmaps, and emergency broadcast dispatch.
- **Early Spoilage Warning**: Trajectory analytics flagging quality degradation across consecutive batches before visible mold appears.
- **Zero-Latency Multilingual Voice**: Real-time actionable guidance in pure **English**, **తెలుగు (Telugu)**, and **हिंदी (Hindi)** with native Web Speech TTS and persistent state synchronization.

---

## 🌟 2. Dual-Portal Architecture & 10 Integrated Core Systems

SmartFeed AI implements **strict role-based portal segregation** (`renderSidebarNav(role)`). When logged in as a Farmer, the portal displays farmer-centric tools; when logged in as a District Cooperative Admin, the interface dynamically transitions into an executive oversight command center.

```
                              🌐 SMARTFEED AI UNIFIED ARCHITECTURE
                              ─────────────────────────────────────
     [ Farmer Mobile Device / Tablet ]              [ Dairy Cooperative Admin PC ]
                    │                                              │
                    └──────────────────────┬───────────────────────┘
                                           ▼
                 ┌──────────────────────────────────────────────────┐
                 │       FastAPI High-Performance Server (Port 8000)│
                 │   - Pure HTML5 / CSS3 / Vanilla JS Reactive SPA  │
                 │   - Zero Language Mixing: English / Telugu / Hindi│
                 │   - Viewport-Bounded Responsive Overflow Layout  │
                 └────────────────────────┬─────────────────────────┘
                                          │
        ┌─────────────────────────────────┴─────────────────────────────────┐
        ▼                                                                   ▼
┌──────────────────────────────────────┐            ┌──────────────────────────────────────┐
│        FARMER PORTAL (7 TOOLS)       │            │      ADMIN COMMAND CENTER (6 TOOLS)  │
├──────────────────────────────────────┤            ├──────────────────────────────────────┤
│ 1. Feed Quality Vision Scanner       │            │ 1. Cooperative Overview & Live KPIs  │
│ 2. Urea & NPN Adulteration Screening │            │ 2. Farmer Master Registry Directory  │
│ 3. ICAR Safe Urea Straw Calculator   │            │ 3. District Batch Quality Audit Log  │
│ 4. Offline Veterinary AI Advisor     │            │ 4. Village Risk Surveillance Matrix  │
│ 5. Animal Ration Balancer (ICAR/NDDB)│            │ 5. Emergency Broadcast Advisory Stream│
│ 6. Daily Feeding Planner & Diary     │            │ 6. BIS IS:2052 Regulatory Standards  │
│ 7. QR Feed Passport Verification     │            │                                      │
└──────────────────┬───────────────────┘            └──────────────────┬───────────────────┘
                   │                                                   │
                   └──────────────────────┬────────────────────────────┘
                                          ▼
                         ┌──────────────────────────────────┐
                         │      SQLite3 (smartfeed.db)      │
                         │ users | farms | animals | tests  │
                         │ feeding_diary | broadcasts       │
                         └──────────────────────────────────┘
```

### Complete System Breakdown

| # | System Module | Technology / Algorithm | Key Capability |
|---|---|---|---|
| **1** | **Onboarding & Role Gate** | Dynamic Session Gate + 4-Step Wizard | Splash screen, synchronized language picker, Admin 1-Click (`8341016049 / 6049`), farm setup wizard (Cows & Buffaloes). |
| **2** | **Feed Quality Vision Scanner** | OpenCV 4.8 + MobileNetV2 DL | Discoloration index, Canny fungal texture detection, foreign inclusion contours, defect classification. |
| **3** | **Biochemical Adulteration** | Stoichiometric NPN / CP Ratio | Detects chemical urea spiking (46% N), evaluates chemical adulteration risk, calculates safe urea feeding dosage. |
| **4** | **ICAR Safe Urea Calculator** | ICAR Ammoniation Formulas | Generates exact 4% urea 40% water straw treatment protocols and enforces strict 1% NPN limits in concentrate feeds. |
| **5** | **Offline Veterinary Advisor** | Rule-Based Diagnostic Tree | Native Telugu farmer symptom matcher for Bloat, Acidosis, Ketosis, Mastitis, Milk Fever, and Urea Poisoning. |
| **6** | **Animal Ration Balancer** | ICAR & NDDB Livestock Formulas | Species-specific feed calculation (body weight, lactation, milk yield in litres); green/dry fodder balancing. |
| **7** | **Daily Feeding Planner & Diary** | Time-Slot Distribution Algorithm | Morning (35%), Noon (25%), Evening (40%) feeding schedule; intake tracking, hydration reminders, and compliance insights. |
| **8** | **Digital Feed Passport** | `qrcode` + OpenCV Multi-Pass Decoder | Unique `SFA-YYYY-XXXXXX` Batch IDs; verifiable high-contrast QR codes with multipart image upload validation. |
| **9** | **Analytics & Early Spoilage** | Chart.js 4.4.0 (Offline) + Slope Engine| Historical batch health trends, risk distribution doughnut, early spoilage alert before visible decay. |
| **10**| **Admin Command Center** | Responsive Grid + Touch Scroll Tables | Comprehensive multi-village surveillance, farmer cattle registry, searchable batch audit logs, and broadcast alert dispatcher. |

---

## 🛡️ 3. Pre-Configured Accounts & Clean Database State

The production database (`smartfeed.db`) is initialized with a verified **District Cooperative Admin** account and clean tables:

```
DATABASE STATUS (smartfeed.db):
 - users: 1 row (District Cooperative Admin)
 - farms: 0 rows (Ready for fresh onboarding)
 - animals: 0 rows (Ready for herd registration)
 - tests: 0 rows (Clean scan history)
 - feeding_diary: 0 rows (Clean log sheet)
```

### Admin Credentials
- **Role**: `admin`
- **Mobile Number**: `8341016049`
- **Password**: `6049`
- **Name**: `District Cooperative Admin`
- **Features**: Full cooperative overview, farmer registry monitoring, batch audit logs, village surveillance heatmap, and emergency broadcast dispatch.
- **Sidebar Experience**: Farmer-specific tools are hidden; only dedicated executive tools appear.

### Farmer Onboarding
- New farmers click **`📝 Register Farm`** on the Auth screen.
- Provide Name, Mobile Number, Password, and Preferred Language.
- Complete the intuitive **4-Step Farm Setup Wizard**:
  1. Farm Location & Preferred Language
  2. Main Feed Type & Storage Conditions
  3. Herd Size (Total Cows & Buffaloes)
  4. Individual Animal Cards (Species, Age, Lactation Status, Daily Milk Yield)

---

## 💻 4. Tech Stack & Quality Metrics

| Layer | Component | Details |
|---|---|---|
| **Backend** | Python 3.10+, FastAPI, Uvicorn | High-throughput asynchronous ASGI web server and REST APIs. |
| **Computer Vision** | OpenCV (`cv2`), Pillow, NumPy | HSV color space segmentation, Canny edge detection, contour analysis. |
| **Machine Learning** | PyTorch, MobileNetV2, Scikit-Learn | Transfer learning defect classifier with heuristic image analysis fallback. |
| **Frontend UI** | HTML5, Modern CSS3, JavaScript (ES6+) | Single-Page Application (SPA) with responsive mobile layout and zero dependencies. |
| **Charts & Trends**| Chart.js 4.4.0 (Local Offline Bundle) | 100% offline quality trend lines and risk distribution charts. |
| **Audio & Speech** | W3C Web Speech API (`SpeechSynthesis`) | Browser-native voice readout in Telugu, Hindi, and English (no external APIs needed). |
| **Database** | SQLite3 (`smartfeed.db`) | Relational storage with foreign key cascades and auto-increment sequence resets. |
| **Testing & QA** | Python `unittest` | **86 automated unit tests passed (100% OK)** in ~46 seconds. |
| **System Audit** | Full-Spectrum API & DOM Audit | **34 / 34 functional endpoints and workflows verified operational (100%)**. |

---

## 📁 5. Directory Structure

```
smartfeed-ai/
├── server.py                  # Production FastAPI REST backend and static SPA server
├── smartfeed.db               # SQLite database (users, farms, animals, tests, feeding_diary)
├── PROJECT_GUIDE.html         # Interactive, responsive project presentation guide
├── PROJECT_GUIDE.md           # Developer and evaluator architectural guide
├── README.md                  # Master SIH project documentation
├── requirements.txt           # Python dependency specifications
│
├── db/
│   ├── __init__.py
│   └── database.py            # SQLite schema, CRUD operations, wipe_all_except_admin helper
│
├── utils/
│   ├── __init__.py            # Clean module exports
│   ├── cv_analysis.py         # OpenCV HSV color thresholding, mycelium texture & particle analysis
│   ├── inference.py           # Deep learning inference pipeline with heuristic fallback
│   ├── adulteration.py        # Biochemical urea adulteration and safe dosage calculation
│   ├── nutrition.py           # BIS and ICAR nutrient reference evaluation
│   ├── risk_engine.py         # Multi-factor Risk Intelligence Engine (0–100 Health Score)
│   ├── ration_engine.py       # Animal-specific nutritional requirements & ration balancer
│   ├── feeding_planner.py     # Time-based daily feeding schedule & compliance engine
│   ├── advisory.py            # Multilingual farmer advisory generation (en, te, hi)
│   ├── qr_utils.py            # QR code passport generation and multi-pass image decoding
│   └── analytics.py           # Executive KPIs and early spoilage trajectory detection
│
├── web/
│   ├── index.html             # Responsive Single-Page Application (Dual-Portal Navigation)
│   ├── css/
│   │   └── style.css          # Viewport-contained responsive design, horizontal scroll tables
│   └── js/
│       ├── app.js             # Reactive frontend engine, state management, persistent i18n
│       └── chart.min.js       # Offline bundled Chart.js library
│
├── data/
│   ├── README_DATASET.md      # Dataset instructions and download guidelines
│   ├── nutrient_reference.csv # BIS & ICAR official nutrient benchmark standards
│   ├── sample_images/         # Preset test photos for 1-click demonstration
│   ├── grain_defects/         # Mendeley Grain Defects dataset folders
│   └── silage/                # Silage preservation quality dataset (fresh vs. spoiled)
│
└── tests/                     # 86 automated unit, API, and live integration tests
    ├── test_all_live_processes.py
    ├── test_api_auth_onboarding.py
    ├── test_api_feed_diary.py
    ├── test_api_ration.py
    ├── test_db.py
    ├── test_feeding_planner.py
    ├── test_live_verify.py
    ├── test_ration_engine.py
    ├── test_step2_cv_inference.py
    ├── test_step3_nutrition_adulteration.py
    ├── test_step4_risk_engine.py
    ├── test_step5_advisory.py
    ├── test_step5_auth_onboarding.py
    ├── test_step6_qr_passport.py
    ├── test_step7_analytics.py
    └── test_step8_end_to_end.py
```

---

## ⚡ 6. Installation & Quick Start

### 1. Prerequisites
- Python 3.10 or higher
- Windows, Linux, or macOS

### 2. Clone & Navigate
```powershell
cd y:\smartfeed-ai
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Run Automated Unit Tests (86 Tests)
Verify that all 86 unit and integration tests pass:
```powershell
python -m unittest discover tests/ "test_*.py"
```
*Expected Output:*
```
Ran 86 tests in 46.978s
OK
```

### 5. Run Full 360° System Audit (34 Modules)
Execute the complete end-to-end integration audit:
```powershell
python scratch/audit_entire_system.py
```
*Expected Output:*
```
🏆 ALL 34 SYSTEM MODULES & API ROUTES TESTED AND 100% OPERATIONAL!
```

### 6. Launch the Production Server
```powershell
python -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```
Open your browser and navigate to:
👉 **`http://localhost:8000/`**

---

## 🔬 7. Scientific Honesty & Regulatory Alignment

SmartFeed AI upholds rigorous scientific integrity:
- ❌ **No Sensor/Hardware Pretense**: Does NOT falsely claim to embed NIR spectrometers, chemical test strips, or electronic noses inside the software.
- ❌ **No Absolute Chemical Claims from Pixels**: Avoids stating *"100% aflatoxin confirmed"* from a photograph.
- ✅ **Scientifically Rigorous Terminology**: Always reports **"Visual Mould Risk"**, **"Suspected Urea Adulteration Risk"**, and **"Potential Quality Deviation"**.
- ✅ **Mandatory Disclaimers**: Prominently presented on every scan result and printable digital passport:
  > *"This software provides AI-assisted visual quality screening and decision support. It does not replace certified laboratory testing. Chemical toxins, mycotoxins, and microscopic adulterants require chemical verification."*

---

## 🎤 8. SIH Final Pitch Summary

> **"SmartFeed AI is an affordable, 100% offline-ready, software-first dairy intelligence platform. By synthesizing computer vision, biochemical adulteration screening, ICAR-compliant animal ration balancing, daily feeding planning, explainable multilingual AI guidance, tamper-evident QR digital batch passports, and a dedicated District Dairy Cooperative Admin Command Center, SmartFeed AI protects livestock health and boosts dairy farmer prosperity across rural India."**
