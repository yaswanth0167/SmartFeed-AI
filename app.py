"""
SmartFeed AI - Web Prototype Application (UI/UX Redesign)
AI-Powered Cattle Feed & Silage Quality Assessment, Risk Intelligence & Traceability System
Built for Smart India Hackathon (SIH).
"""

import os
import sys
from pathlib import Path
import streamlit as st
from PIL import Image
import numpy as np

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from db.database import (
    initialize_database,
    create_test,
    get_test_by_batch,
    get_all_tests,
    get_recent_tests,
    get_quality_trend,
    generate_batch_id,
)
from utils.cv_analysis import analyze_feed_image
from utils.inference import predict_feed_quality
from utils.nutrition import analyze_nutrition
from utils.adulteration import check_adulteration_risk
from utils.risk_engine import evaluate_smartfeed_risks
from utils.advisory import generate_advisory
from utils.qr_utils import generate_feed_passport_qr, decode_qr_image, get_digital_feed_passport
from utils.analytics import (
    compute_dashboard_metrics,
    detect_early_spoilage_warning,
    create_quality_trend_chart,
    create_risk_distribution_chart,
    create_sample_type_pie
)
from utils.ui_components import (
    render_circular_score_gauge,
    render_passport_certificate,
    render_audio_speaker_button,
    render_opening_hero,
    render_sidebar_logo,
    render_page_header,
    get_logo_base64
)

# ---------------------------------------------------------
# Page Configuration & Master Agri-Tech Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="SmartFeed AI - Cattle Feed Intelligence",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Master Modern Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #0F172A;
    }

    /* Gradient Brand Headers */
    .brand-hero {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px !important;
        background: linear-gradient(135deg, #064E3B 0%, #059669 45%, #2563EB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem !important;
        line-height: 1.15;
    }

    .brand-tagline {
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        color: #475569 !important;
        margin-bottom: 1.2rem !important;
    }

    /* Live System Status Chip */
    .live-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #DCFCE7;
        color: #166534;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #22C55E;
        border-radius: 50%;
        box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.25);
    }

    /* Modern Card System */
    .glass-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.04), 0 4px 8px -2px rgba(15, 23, 42, 0.02);
        margin-bottom: 22px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        box-shadow: 0 14px 35px -5px rgba(15, 23, 42, 0.07);
    }

    /* Step Banner */
    .step-banner {
        display: flex;
        align-items: center;
        gap: 12px;
        background: #F1F5F9;
        border-left: 5px solid #059669;
        padding: 12px 18px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.05rem;
        color: #0F172A;
        margin: 16px 0 12px 0;
    }

    /* Notice & Disclaimer Boxes */
    .clean-disclaimer {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-left: 4px solid #16A34A;
        padding: 12px 16px;
        border-radius: 10px;
        font-size: 0.88rem;
        color: #166534;
        margin-bottom: 1.2rem;
    }

    .clean-warning {
        background-color: #FEF2F2;
        border: 1px solid #FECACA;
        border-left: 4px solid #DC2626;
        padding: 12px 16px;
        border-radius: 10px;
        font-size: 0.88rem;
        color: #991B1B;
        margin-bottom: 1.2rem;
    }

    /* Buttons */
    .stButton>button {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        border: none !important;
        transition: all 0.2s ease !important;
        height: 3.2rem !important;
        font-size: 1.05rem !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(5, 150, 105, 0.25);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F1F5F9;
        padding: 6px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 8px 18px !important;
        color: #475569 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #059669 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
    }
</style>
""", unsafe_allow_html=True)

# Ensure Database is Initialized
initialize_database()

# ---------------------------------------------------------
# Sidebar Navigation & Farmer Configuration
# ---------------------------------------------------------
with st.sidebar:
    # Official Animated Glowing Logo
    st.markdown(render_sidebar_logo(), unsafe_allow_html=True)
    
    st.markdown("""
    <div class="live-status-pill" style="margin: 0 auto 14px auto; display: flex; justify-content: center;">
        <div class="pulse-dot"></div>
        <span>OFFLINE READY • LOCAL AI ACTIVE</span>
    </div>
    """, unsafe_allow_html=True)

    NAV_PAGES = [
        "🏠 Home",
        "📸 Quality Scanner",
        "⚠️ Adulteration Check",
        "🤖 AI Advisory",
        "📊 Dashboard",
        "📦 Feed Passport",
        "🔎 Batch Lookup"
    ]
    if "nav_radio" not in st.session_state:
        st.session_state.nav_radio = "🏠 Home"

    menu_option = st.radio(
        "Navigation",
        NAV_PAGES,
        key="nav_radio"
    )

    st.divider()
    st.markdown("#### 🌐 Farmer Language")
    selected_lang = st.selectbox(
        "Language / భాష / भाषा",
        options=["🇬🇧 English", "🇮🇳 తెలుగు (Telugu)", "🇮🇳 हिंदी (Hindi)"],
        index=0
    )
    lang_code = "en"
    if "Telugu" in selected_lang or "తెలుగు" in selected_lang:
        lang_code = "te"
    elif "Hindi" in selected_lang or "हिंदी" in selected_lang:
        lang_code = "hi"

    st.markdown("#### ⚙️ Advisory Engine Mode")
    provider_choice = st.selectbox(
        "Advisory Source",
        options=["⚡ Auto (Cloud LLM if key exists, else Offline)", "📶 100% Offline Rule-Based (Guaranteed)"],
        index=0
    )
    chosen_provider = "offline" if "Offline" in provider_choice else "auto"

    st.divider()
    st.caption("🏆 **Smart India Hackathon 2026**\nSoftware Prototype • No Hardware Required")


# ---------------------------------------------------------
# PAGE 1: 🏠 HOME
# ---------------------------------------------------------
if menu_option == "🏠 Home":
    # Grand Opening Hero Screen with Floating Animated Logo and Glowing Halo
    st.markdown(render_opening_hero(), unsafe_allow_html=True)

    st.markdown("""
    <div class='clean-disclaimer'>
        <strong>⚠️ Scientific Prototype Disclaimer:</strong> SmartFeed AI provides AI-based visual screening, OpenCV color/texture analytics, and multi-factor risk predictions. 
        It is a low-cost, software-only decision support tool designed for dairy farmers. Laboratory testing is recommended for chemical confirmation.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        ### 🌟 Why SmartFeed AI?
        Smallholder dairy farmers and rural milk cooperatives often face devastating drops in milk production, reproductive failure, and cattle toxicity caused by **spoilage, mould mycotoxins, and urea adulteration** in cattle feed and silage.
        
        Traditional solutions require expensive laboratory testing equipment or physical spectrometers that rural farmers cannot afford.
        
        **SmartFeed AI solves this by turning any standard smartphone camera into an intelligent feed diagnostic laboratory.**
        """)

        st.markdown("""
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; margin: 16px 0;">
            <h4 style="color: #059669; margin-top: 0;">💡 SIH Prototype Pitch</h4>
            <p style="color: #334155; font-size: 0.95rem; margin-bottom: 0;">
                <em>"SmartFeed AI is a low-cost, software-first feed intelligence platform combining computer vision, OpenCV visual analysis, multi-factor risk assessment, simulated nutrition inputs, explainable multilingual AI advisory, historical spoilage monitoring, and QR-based digital traceability to help dairy farmers make safer feed decisions."</em>
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 🏆 Core Innovations (USPs)")
        st.markdown("""
        - ⭐ **SmartFeed Health Score (0–100)**: Single transparent score combining visual, fungal, particle, adulteration, nutrient, and storage parameters.
        - 🔍 **Explainable AI ("Why This Result?")**: Clearly explains *why* feed is risky with itemized point deductions.
        - 🗣️ **Multilingual Advisory & Voice**: Native recommendations in **English**, **Telugu**, and **Hindi** with audio speech.
        - 📦 **QR Digital Feed Passport**: Permanent traceability with unique Batch IDs (`SFA-YYYY-XXXXXX`) for dairy cooperatives.
        - 📈 **Early Spoilage Trend Warnings**: Detects progressive deterioration trajectories before feed rots.
        - 📶 **100% Offline Capability**: Works reliably without internet connectivity.
        """)

    st.divider()

    # System Capabilities Telemetry Bar
    st.markdown("""
    <div style="
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 14px;
        margin: 6px 0 24px 0;
    ">
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px; padding: 14px 18px; display: flex; align-items: center; gap: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
            <span style="font-size: 1.8rem;">⚡</span>
            <div>
                <div style="font-size: 0.72rem; font-weight: 800; color: #64748B; text-transform: uppercase; letter-spacing: 0.8px;">Edge AI Engine</div>
                <div style="font-size: 1.05rem; font-weight: 800; color: #0F172A;">&lt; 300ms Local Latency</div>
            </div>
        </div>
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px; padding: 14px 18px; display: flex; align-items: center; gap: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
            <span style="font-size: 1.8rem;">🛡️</span>
            <div>
                <div style="font-size: 0.72rem; font-weight: 800; color: #64748B; text-transform: uppercase; letter-spacing: 0.8px;">Risk Intelligence</div>
                <div style="font-size: 1.05rem; font-weight: 800; color: #0F172A;">6-Factor Fusion Engine</div>
            </div>
        </div>
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px; padding: 14px 18px; display: flex; align-items: center; gap: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
            <span style="font-size: 1.8rem;">🗣️</span>
            <div>
                <div style="font-size: 0.72rem; font-weight: 800; color: #64748B; text-transform: uppercase; letter-spacing: 0.8px;">Multilingual Voice</div>
                <div style="font-size: 1.05rem; font-weight: 800; color: #0F172A;">English • తెలుగు • हिंदी</div>
            </div>
        </div>
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px; padding: 14px 18px; display: flex; align-items: center; gap: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
            <span style="font-size: 1.8rem;">📦</span>
            <div>
                <div style="font-size: 0.72rem; font-weight: 800; color: #64748B; text-transform: uppercase; letter-spacing: 0.8px;">Traceability</div>
                <div style="font-size: 1.05rem; font-weight: 800; color: #0F172A;">QR Digital Passport</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🚀 Interactive Feature Quick-Launch")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="glass-card" style="text-align: center; height: 165px; margin-bottom: 8px;">
            <div style="font-size: 2.2rem;">📸</div>
            <h4 style="margin: 8px 0 4px 0; color: #064E3B;">1. Feed Scanner</h4>
            <p style="font-size: 0.84rem; color: #64748B;">Upload photo or use camera to detect discoloration & mould.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Open Scanner", key="btn_open_scanner", use_container_width=True, type="primary"):
            st.session_state.nav_radio = "📸 Quality Scanner"
            st.rerun()

    with c2:
        st.markdown("""
        <div class="glass-card" style="text-align: center; height: 165px; margin-bottom: 8px;">
            <div style="font-size: 2.2rem;">⚠️</div>
            <h4 style="margin: 8px 0 4px 0; color: #064E3B;">2. Adulteration Risk</h4>
            <p style="font-size: 0.84rem; color: #64748B;">Check urea spiking & simulated non-protein nitrogen risks.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔬 Check Adulteration", key="btn_open_adulteration", use_container_width=True):
            st.session_state.nav_radio = "⚠️ Adulteration Check"
            st.rerun()

    with c3:
        st.markdown("""
        <div class="glass-card" style="text-align: center; height: 165px; margin-bottom: 8px;">
            <div style="font-size: 2.2rem;">🤖</div>
            <h4 style="margin: 8px 0 4px 0; color: #064E3B;">3. Farmer Advisory</h4>
            <p style="font-size: 0.84rem; color: #64748B;">Listen to voice advice in English, Telugu, or Hindi.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🗣️ Voice Advisory", key="btn_open_advisory", use_container_width=True):
            st.session_state.nav_radio = "🤖 AI Advisory"
            st.rerun()

    with c4:
        st.markdown("""
        <div class="glass-card" style="text-align: center; height: 165px; margin-bottom: 8px;">
            <div style="font-size: 2.2rem;">📦</div>
            <h4 style="margin: 8px 0 4px 0; color: #064E3B;">4. QR Passport</h4>
            <p style="font-size: 0.84rem; color: #64748B;">Inspect verifiable digital passports for dairy cooperatives.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📜 Verify Passport", key="btn_open_passport", use_container_width=True):
            st.session_state.nav_radio = "📦 Feed Passport"
            st.rerun()


# ---------------------------------------------------------
# PAGE 2: 📸 QUALITY SCANNER (The Core Demo Flow)
# ---------------------------------------------------------
elif menu_option == "📸 Quality Scanner":
    st.markdown(render_page_header("📸 SmartFeed Quality Scanner", "Multi-Factor Computer Vision, Risk Intelligence & Digital Feed Passport Generation"), unsafe_allow_html=True)

    st.markdown("""
    <div class='clean-disclaimer'>
        <strong>Scientific Notice:</strong> This prototype provides AI-based visual assessment and risk prediction. Laboratory testing is recommended for chemical confirmation.
    </div>
    """, unsafe_allow_html=True)

    # STEP 1: INPUTS CARD
    st.markdown("<div class='step-banner'>STEP 1 &nbsp;•&nbsp; Feed Sample & Nutrient Entry</div>", unsafe_allow_html=True)

    with st.container():
        col_img_in, col_sliders = st.columns([3, 2])

        with col_img_in:
            sample_type = st.selectbox(
                "Select Feed Category",
                ["Compound Cattle Feed", "Feed Ingredient", "Silage"],
                index=0
            )

            input_tab1, input_tab2, input_tab3 = st.tabs(["🧪 Demo Samples (1-Click Test)", "📁 Upload Image", "📷 Live Camera"])
            image_to_process = None

            with input_tab1:
                st.write("Select a pre-configured sample for instant SIH demonstration:")
                demo_sample = st.radio(
                    "Choose Demo Feed Condition:",
                    ["Healthy Golden Cattle Feed", "Mouldy Feed (High Fungal Risk)", "Heat-Damaged / Burnt Feed", "Fresh Silage"],
                    index=1,  # Default to mouldy to demonstrate the risk engine
                    horizontal=True
                )
                sample_dir = PROJECT_ROOT / "data" / "sample_images"
                if demo_sample == "Healthy Golden Cattle Feed":
                    p = sample_dir / "sample_healthy_feed.jpg"
                elif demo_sample == "Mouldy Feed (High Fungal Risk)":
                    p = sample_dir / "sample_mouldy_feed.jpg"
                elif demo_sample == "Heat-Damaged / Burnt Feed":
                    p = sample_dir / "sample_burnt_feed.jpg"
                else:
                    p = sample_dir / "sample_fresh_silage.jpg"

                if p.exists():
                    image_to_process = Image.open(p)
                    st.image(image_to_process, width=280, caption=f"Selected: {demo_sample}")

            with input_tab2:
                uploaded_file = st.file_uploader("Upload feed or silage photo", type=["jpg", "jpeg", "png", "webp"])
                if uploaded_file:
                    image_to_process = Image.open(uploaded_file)
                    st.image(image_to_process, width=280, caption="Uploaded Feed Photo")

            with input_tab3:
                camera_file = st.camera_input("Take photo of feed")
                if camera_file:
                    image_to_process = Image.open(camera_file)

        with col_sliders:
            st.markdown("##### 🥗 Manual Nutrient Entry *(Simulated)*")
            st.caption("Enter estimated lab or supplier label nutrient parameters:")

            is_silage = (sample_type == "Silage")
            default_protein = 8.5 if is_silage else 19.5
            default_moist = 65.0 if is_silage else 11.0
            default_fiber = 24.0 if is_silage else 11.5

            crude_protein = st.slider("Crude Protein % (Optimal: 18–22% concentrate)", 0.0, 35.0, default_protein, 0.5)
            moisture = st.slider("Moisture % (Safe dry limit: <12%)", 0.0, 100.0, default_moist, 0.5)
            fiber = st.slider("Crude Fiber % (Optimal: 8–14%)", 0.0, 50.0, default_fiber, 0.5)

            storage_condition = st.selectbox(
                "Farm Storage Environment",
                [
                    "Well-Ventilated Dry Area (Pallet Elevated)",
                    "Damp & Humid Shed (High Moisture Risk)",
                    "Poorly Ventilated / Warm Room",
                    "Outdoor / Exposed to Sunlight & Rain"
                ],
                index=0
            )

    # Big Analysis Action Button
    st.write("")
    analyze_clicked = st.button("🚀 Analyze Feed Quality & Generate Risk Intelligence Report", type="primary", use_container_width=True)

    if analyze_clicked and image_to_process is not None:
        with st.spinner("Executing Computer Vision, OpenCV Spectral Analysis & Risk Intelligence Engine..."):
            # 1. Save uploaded image
            uploads_dir = PROJECT_ROOT / "uploads"
            uploads_dir.mkdir(parents=True, exist_ok=True)
            temp_filename = f"scan_{np.random.randint(100000, 999999)}.jpg"
            saved_img_path = uploads_dir / temp_filename
            image_to_process.convert("RGB").save(str(saved_img_path))

            # 2. Run Computer Vision Inference
            visual_res = predict_feed_quality(saved_img_path, sample_type=sample_type)

            # 3. Run Adulteration Risk Screening
            adulteration_res = check_adulteration_risk(
                feed_type=sample_type,
                color_desc=visual_res["cv_details"]["color_analysis"]["color_risk"],
                texture_desc=visual_res["cv_details"]["texture_analysis"]["texture_risk"],
                smell_desc="Normal" if visual_res["mould_risk"] == "Low" else "Fungal",
                storage_condition=storage_condition,
                foreign_particles=visual_res["foreign_particle_risk"],
                crude_protein=crude_protein,
                moisture=moisture,
                fiber=fiber
            )

            # 4. Run Simulated Nutrition Analysis
            nutrition_res = analyze_nutrition(
                sample_type=sample_type,
                crude_protein=crude_protein,
                moisture=moisture,
                fiber=fiber
            )

            # 5. Fetch Past Test Trend History
            past_tests = get_quality_trend(sample_type=sample_type)

            # 6. Execute SmartFeed Risk Intelligence Engine
            risk_summary = evaluate_smartfeed_risks(
                visual_res=visual_res,
                adulteration_res=adulteration_res,
                nutrition_res=nutrition_res,
                storage_condition=storage_condition,
                historical_tests=past_tests
            )

            # 7. Generate Multilingual Farmer Advisory
            advisory_payload = {
                "sample_type": sample_type,
                "health_score": risk_summary["health_score"],
                "overall_risk": risk_summary["overall_risk"],
                "farmer_label": visual_res["farmer_label"],
                "mould_risk": visual_res["mould_risk"],
                "foreign_particle_risk": visual_res["foreign_particle_risk"],
                "adulteration_risk": adulteration_res["adulteration_risk"],
                "crude_protein": crude_protein,
                "moisture": moisture,
                "fiber": fiber,
                "storage_condition": storage_condition,
                "primary_concern": risk_summary["primary_concern"],
                "recommended_action": risk_summary["recommended_action"],
                "protein_status": nutrition_res["parameter_status"]["protein"],
                "flagged_hazards": adulteration_res["flagged_hazards"]
            }
            advisory_res = generate_advisory(advisory_payload, language=lang_code, provider=chosen_provider)

            # 8. Persist Record to SQLite
            new_batch_id = generate_batch_id()
            db_payload = {
                "batch_id": new_batch_id,
                "sample_type": sample_type,
                "image_path": str(saved_img_path),
                "visual_prediction": visual_res["farmer_label"],
                "confidence": visual_res["confidence"],
                "quality_score": risk_summary["health_score"],
                "mould_risk": visual_res["mould_risk"],
                "foreign_particle_risk": visual_res["foreign_particle_risk"],
                "adulteration_risk": adulteration_res["adulteration_risk"],
                "nutrition_status": nutrition_res["nutrition_status"],
                "crude_protein": crude_protein,
                "moisture": moisture,
                "fiber": fiber,
                "storage_condition": storage_condition,
                "overall_risk": risk_summary["overall_risk"],
                "primary_concern": risk_summary["primary_concern"],
                "advisory": advisory_res["full_advisory_text"],
                "language": lang_code
            }
            create_test(db_payload)

            # 9. Generate QR Code Passport
            qr_file_path = generate_feed_passport_qr(new_batch_id)

        # ---------------------------------------------------------
        # RESULTS DISPLAY: STEP 2 (DUAL VISION) & STEP 3 (DIAGNOSTICS)
        # ---------------------------------------------------------
        st.success("✅ Diagnostics successfully computed! See complete risk intelligence report below:")

        st.markdown("<div class='step-banner'>STEP 2 &nbsp;•&nbsp; Dual-Spectrum Computer Vision Inspection</div>", unsafe_allow_html=True)
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.markdown("##### 📸 Original Feed Sample")
            st.image(image_to_process, use_container_width=True, caption=f"Sample: {sample_type} • Captured Resolution: 400x400")

        with col_v2:
            st.markdown("##### 🎨 OpenCV Visual Anomaly Overlay")
            st.image(
                visual_res["cv_details"]["annotated_image_rgb"],
                use_container_width=True,
                caption="🔴 Red Bounding Boxes: Possible Foreign Particles | 🔷 Cyan Contours: Mould Mycelium"
            )

        # STEP 3: SCORE & MULTI-FACTOR RADAR
        st.markdown("<div class='step-banner'>STEP 3 &nbsp;•&nbsp; SmartFeed Health Score & Multi-Factor Intelligence</div>", unsafe_allow_html=True)

        col_score, col_radar = st.columns([2, 3])

        with col_score:
            # Render Circular Radial Score Dial
            score_gauge_html = render_circular_score_gauge(
                score=risk_summary["health_score"],
                risk_level=risk_summary["overall_risk"],
                safety_badge=risk_summary["safety_badge"],
                primary_concern=risk_summary["primary_concern"]
            )
            st.markdown(score_gauge_html, unsafe_allow_html=True)

        with col_radar:
            st.markdown("##### 🧠 Multi-Factor Component Analysis")
            
            # Component Meters
            cv_col = visual_res["cv_details"]["color_analysis"]
            white_area = cv_col.get("white_grey_patch_pct", 0.0)
            particle_count = visual_res["cv_details"]["foreign_particle_risk"]["particle_count"]
            
            st.write(f"**Visual Quality Index:** `{visual_res['visual_quality_score']:.0f}%` ({visual_res['farmer_label']})")
            st.progress(float(visual_res['visual_quality_score']) / 100.0)

            st.write(f"**Fungal / Mould Safety:** `Risk: {visual_res['mould_risk']}` ({white_area:.1f}% pale mycelium coverage)")
            mould_bar = 0.20 if visual_res['mould_risk'] == "High" else (0.60 if visual_res['mould_risk'] == "Medium" else 0.95)
            st.progress(mould_bar)

            st.write(f"**Foreign Particle Safety:** `Risk: {visual_res['foreign_particle_risk']}` ({particle_count} inclusions detected)")
            particle_bar = 0.30 if visual_res['foreign_particle_risk'] == "High" else (0.70 if visual_res['foreign_particle_risk'] == "Medium" else 0.95)
            st.progress(particle_bar)

            st.write(f"**Adulteration Safety:** `Risk: {adulteration_res['adulteration_risk']}`")
            adult_bar = 0.25 if adulteration_res['adulteration_risk'] == "High" else (0.65 if adulteration_res['adulteration_risk'] == "Medium" else 0.95)
            st.progress(adult_bar)

            st.write(f"**Nutritional Adequacy:** `{nutrition_res['nutrition_status']}` ({nutrition_res['nutrition_score']:.0f}/100)")
            st.progress(float(nutrition_res['nutrition_score']) / 100.0)

        # SPECIAL FEATURE 2: EXPLAINABLE AI
        st.markdown("#### ❓ WHY THIS RESULT? (Explainable AI)")
        col_why1, col_why2 = st.columns([3, 2])
        why_data = risk_summary["why_this_result"]

        with col_why1:
            st.markdown("##### ⚠️ Specific Risk Drivers:")
            for c in why_data["concerns_list"]:
                st.markdown(f"<div style='background: #FFF1F2; border-left: 3px solid #E11D48; padding: 8px 12px; border-radius: 6px; margin-bottom: 6px; font-size: 0.92rem; color: #9F1239;'>{c}</div>", unsafe_allow_html=True)
            
            if why_data["positives_list"]:
                st.markdown("##### 🟢 Favorable Attributes:")
                for p in why_data["positives_list"]:
                    st.markdown(f"<div style='background: #F0FDF4; border-left: 3px solid #16A34A; padding: 8px 12px; border-radius: 6px; margin-bottom: 6px; font-size: 0.92rem; color: #166534;'>✓ {p}</div>", unsafe_allow_html=True)

        with col_why2:
            st.markdown("##### ⚖️ Exact Point Deductions:")
            if why_data["deductions_list"]:
                for d in why_data["deductions_list"]:
                    st.markdown(f"""
                    <div style='display: flex; justify-content: space-between; align-items: center; background: #F8FAFC; border: 1px solid #E2E8F0; padding: 8px 12px; border-radius: 8px; margin-bottom: 6px;'>
                        <span style='font-weight: 600; font-size: 0.85rem;'>{d['factor']}</span>
                        <span style='background: #FEE2E2; color: #991B1B; font-weight: 800; font-size: 0.85rem; padding: 2px 8px; border-radius: 4px;'>{d['points']:.0f} pts</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("• No deductions applied! Perfect baseline score.")

        # STEP 4: ADVISORY & PASSPORT
        st.markdown("<div class='step-banner'>STEP 4 &nbsp;•&nbsp; Multilingual Farmer Advisory & Digital Feed Passport</div>", unsafe_allow_html=True)

        col_adv, col_pass = st.columns([1, 1])

        with col_adv:
            st.markdown(f"##### 🗣️ Multilingual Farmer Advisory ({selected_lang})")
            st.markdown(f"""
            <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 14px; padding: 18px; color: #1E3A8A; font-size: 0.95rem; line-height: 1.6;">
                <h4 style="margin-top:0; color: #1D4ED8;">{advisory_res['safety_status']}</h4>
                {advisory_res['full_advisory_text'].replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)

            # Modern Soundwave Audio Player Button
            audio_html = render_audio_speaker_button(advisory_res["full_advisory_text"], lang=lang_code)
            st.components.v1.html(audio_html, height=75)

        with col_pass:
            st.markdown("##### 📦 Generated Digital Feed Passport")
            passport_record = get_digital_feed_passport(new_batch_id)
            if passport_record:
                cert_html = render_passport_certificate(passport_record, str(qr_file_path))
                st.markdown(cert_html, unsafe_allow_html=True)

                with open(qr_file_path, "rb") as qrf:
                    st.download_button(
                        "⬇️ Download Certified QR Passport Image",
                        qrf,
                        file_name=f"QR_{new_batch_id}.png",
                        mime="image/png",
                        use_container_width=True
                    )

    elif analyze_clicked and image_to_process is None:
        st.error("Please upload an image, capture one with your camera, or select a demo sample first!")


# ---------------------------------------------------------
# PAGE 3: ⚠️ ADULTERATION CHECK
# ---------------------------------------------------------
elif menu_option == "⚠️ Adulteration Check":
    st.markdown(render_page_header("⚠️ Adulteration Risk Screening", "Screen cattle feed for non-protein nitrogen (urea), low-grade fillers, and moisture spoilage"), unsafe_allow_html=True)

    st.markdown("""
    <div class='clean-warning'>
        <strong>⚠️ Scientific Disclaimer:</strong> This engine screens for <em>Possible Adulteration Risks</em> using sensory observations and nutrient inputs. 
        It does NOT claim chemical certainty from images. Laboratory verification is required to confirm chemical contaminants.
    </div>
    """, unsafe_allow_html=True)

    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown("##### 1. Sensory Physical Markers")
        ad_feed_type = st.selectbox("Feed Category", ["Compound Cattle Feed", "Feed Ingredient", "Silage"], index=0)
        ad_color = st.selectbox("Observed Coloration", ["Normal", "Dark / Burnt", "Greenish", "White Patches", "Unusual / Discolored"])
        ad_texture = st.selectbox("Observed Texture", ["Fine", "Rough / Gritty", "Sticky / Clumped", "Powdery / Chalky"])
        ad_smell = st.selectbox("Aroma Condition", ["Normal Fresh", "Sour / Fermentative", "Fungal / Musty", "Unusual / Pungent / Chemical"])

    with col_a2:
        st.markdown("##### 2. Environmental & Nutrient Profile")
        ad_storage = st.selectbox("Storage Environment", ["Dry & Ventilated", "Damp / Humid", "Poorly Ventilated / Warm", "Outdoors"])
        ad_particles = st.radio("Visible Foreign Particles / Debris", ["None (Low)", "A Few Inclusions (Medium)", "Many Foreign Particles (High)"], horizontal=True)
        ad_protein = st.slider("Crude Protein % (Simulated)", 0.0, 35.0, 21.0, 0.5)
        ad_moisture = st.slider("Moisture % (Simulated)", 0.0, 30.0, 10.5, 0.5)
        ad_fiber = st.slider("Crude Fiber % (Simulated)", 0.0, 40.0, 12.0, 0.5)

    if st.button("🔍 Run Adulteration Risk Screening", type="primary", use_container_width=True):
        particle_val = "High" if "High" in ad_particles else ("Medium" if "Medium" in ad_particles else "Low")
        res = check_adulteration_risk(
            feed_type=ad_feed_type,
            color_desc=ad_color,
            texture_desc=ad_texture,
            smell_desc=ad_smell,
            storage_condition=ad_storage,
            foreign_particles=particle_val,
            crude_protein=ad_protein,
            moisture=ad_moisture,
            fiber=ad_fiber
        )

        st.divider()
        risk_level = res["adulteration_risk"]
        if risk_level == "High":
            st.markdown("<div style='background:#FEE2E2; border-left:5px solid #DC2626; padding:16px; border-radius:8px;'><h3 style='color:#991B1B; margin:0;'>🔴 Adulteration Risk Level: HIGH HAZARD</h3></div>", unsafe_allow_html=True)
        elif risk_level == "Medium":
            st.markdown("<div style='background:#FEF3C7; border-left:5px solid #F59E0B; padding:16px; border-radius:8px;'><h3 style='color:#92400E; margin:0;'>🟡 Adulteration Risk Level: MEDIUM CAUTION</h3></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='background:#DCFCE7; border-left:5px solid #16A34A; padding:16px; border-radius:8px;'><h3 style='color:#166534; margin:0;'>🟢 Adulteration Risk Level: LOW (SAFE / NORMAL)</h3></div>", unsafe_allow_html=True)

        if res["flagged_hazards"]:
            st.markdown("##### 🚨 Flagged Hazard Patterns:")
            for h in res["flagged_hazards"]:
                st.write(f"• **{h}**")

        st.markdown("##### 🔍 Explanatory Reasons:")
        for r in res["reasons"]:
            st.write(f"• {r}")

        st.markdown(f"**💡 Recommended Action:** {res['recommended_action']}")
        st.caption(f"Machine Learning Cross-Validation: {res.get('ml_validation_indicator', 'Validated')}")


# ---------------------------------------------------------
# PAGE 4: 🤖 AI ADVISORY
# ---------------------------------------------------------
elif menu_option == "🤖 AI Advisory":
    st.markdown(render_page_header("🤖 Multilingual Farmer Advisory", "Instant, culturally tailored feed guidance in English, Telugu, and Hindi with speech playback"), unsafe_allow_html=True)

    adv_tab1, adv_tab2 = st.tabs(["📋 Farm Hazard Scenarios", "💬 Custom Farmer Consultation"])

    with adv_tab1:
        st.markdown("#### Select a Feed Hazard Scenario:")
        scenario = st.selectbox(
            "Common Dairy Farm Situations",
            [
                "Mouldy Feed with White/Grey Patches",
                "Suspected Urea Chemical Adulteration",
                "High Moisture Feed Deterioration",
                "Low Protein Concentrate (Milk Drop)",
                "Safe Healthy Feed Management"
            ]
        )

        sc_data = {
            "sample_type": "Compound Cattle Feed",
            "storage_condition": "Standard Shed",
            "crude_protein": 19.5,
            "moisture": 11.0,
            "fiber": 11.5,
            "protein_status": "Optimal",
            "flagged_hazards": []
        }

        if "Mouldy" in scenario:
            sc_data.update({"health_score": 42.0, "overall_risk": "High", "farmer_label": "High Mould Risk", "mould_risk": "High", "moisture": 16.0, "primary_concern": "Fungal & Mould Proliferation", "recommended_action": "Withhold feed immediately."})
        elif "Urea" in scenario:
            sc_data.update({"health_score": 38.0, "overall_risk": "High", "farmer_label": "Normal Color", "mould_risk": "Low", "adulteration_risk": "High", "crude_protein": 31.0, "protein_status": "Abnormally High", "flagged_hazards": ["Possible Urea / NPN Spiking"], "primary_concern": "Possible Urea Spiking Risk", "recommended_action": "Quarantine feed for lab test."})
        elif "Moisture" in scenario:
            sc_data.update({"health_score": 58.0, "overall_risk": "Medium", "farmer_label": "Damp Feed", "mould_risk": "Medium", "moisture": 15.5, "primary_concern": "High Moisture Spoilage", "recommended_action": "Sun-dry feed on clean sheet."})
        elif "Low Protein" in scenario:
            sc_data.update({"health_score": 64.0, "overall_risk": "Medium", "farmer_label": "Low Protein", "mould_risk": "Low", "crude_protein": 12.0, "protein_status": "Deficient", "primary_concern": "Crude Protein Deficiency", "recommended_action": "Supplement with oil cakes."})
        else:
            sc_data.update({"health_score": 90.0, "overall_risk": "Low", "farmer_label": "Good Quality", "mould_risk": "Low", "primary_concern": "Feed in Good Condition", "recommended_action": "Feed according to animal body weight."})

        adv_out = generate_advisory(sc_data, language=lang_code, provider=chosen_provider)
        
        st.divider()
        st.markdown(f"""
        <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 14px; padding: 20px; color: #1E3A8A; font-size: 1rem; line-height: 1.6;">
            <h3 style="margin-top:0; color: #1D4ED8;">{adv_out['safety_status']}</h3>
            {adv_out['full_advisory_text'].replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
        
        audio_html = render_audio_speaker_button(adv_out["full_advisory_text"], lang=lang_code)
        st.components.v1.html(audio_html, height=75)

    with adv_tab2:
        st.markdown("#### Ask a Question to SmartFeed AI:")
        farmer_q = st.text_area("Question (English, Telugu, or Hindi):", "What is the safest way to store silage after opening the pit?")
        if st.button("Get AI Guidance", type="primary"):
            custom_payload = {
                "sample_type": "Silage",
                "health_score": 75.0,
                "overall_risk": "Medium",
                "farmer_label": "Silage Management",
                "mould_risk": "Low",
                "foreign_particle_risk": "Low",
                "adulteration_risk": "Low",
                "crude_protein": 8.5,
                "moisture": 65.0,
                "fiber": 24.0,
                "storage_condition": "Opened Silo",
                "primary_concern": farmer_q,
                "recommended_action": "Keep face vertical, remove only daily ration, cover with plastic."
            }
            res_custom = generate_advisory(custom_payload, language=lang_code, provider=chosen_provider)
            st.markdown(f"""
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; margin-top: 14px;">
                {res_custom['full_advisory_text'].replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
            audio_custom = render_audio_speaker_button(res_custom["full_advisory_text"], lang=lang_code)
            st.components.v1.html(audio_custom, height=75)


# ---------------------------------------------------------
# PAGE 5: 📊 DASHBOARD (Quality Trend & Spoilage Alert)
# ---------------------------------------------------------
elif menu_option == "📊 Dashboard":
    st.markdown(render_page_header("📊 Quality Trend & Spoilage Dashboard", "Historical test monitoring, early spoilage warning indicators, and batch statistics"), unsafe_allow_html=True)

    all_tests = get_all_tests(limit=200)
    metrics = compute_dashboard_metrics(all_tests)

    # Top KPI Metric Cards
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total Tests", metrics["total_tests"])
    k2.metric("Average Score", f"{metrics['avg_quality_score']:.1f} / 100")
    k3.metric("🟢 Safe Batches", metrics["safe_tests"], f"{metrics['safe_pct']}%")
    k4.metric("🟡 Caution Batches", metrics["caution_tests"])
    k5.metric("🔴 High Risk Batches", metrics["high_risk_tests"], f"{metrics['high_risk_pct']}%")

    st.divider()

    # SPECIAL FEATURE 5: EARLY SPOILAGE WARNING
    trend_history = get_quality_trend()
    spoilage_alert = detect_early_spoilage_warning(trend_history)

    if spoilage_alert["has_warning"]:
        st.markdown(f"""
        <div style="background: #FEF2F2; border: 2px solid #DC2626; border-radius: 14px; padding: 20px; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(220, 38, 38, 0.1);">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <span style="font-size: 1.6rem;">🚨</span>
                <h3 style="color: #991B1B; margin: 0; font-size: 1.25rem;">{spoilage_alert["title"]}</h3>
            </div>
            <p style="color: #450A0A; font-weight: 600; margin-bottom: 6px;">Recent quality tests indicate a decreasing quality trend:</p>
            <ul style="color: #991B1B; margin-bottom: 12px;">
        """, unsafe_allow_html=True)
        for r in spoilage_alert["reasons"]:
            st.markdown(f"<li><b>{r}</b></li>", unsafe_allow_html=True)
        st.markdown(f"""
            </ul>
            <div style="background: #FFFFFF; border-radius: 8px; padding: 10px 14px; border: 1px solid #FECACA; color: #166534; font-weight: 700; font-size: 0.95rem;">
                💡 Recommended Action: {spoilage_alert["recommendation"]}
            </div>
            <div style="font-size: 0.78rem; color: #666; margin-top: 8px;">
                <em>{spoilage_alert["disclaimer"]}</em>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="clean-disclaimer">
            <b>✅ Feed Quality Trend is Stable.</b> Sequential evaluations indicate safe, non-deteriorating feed preservation.
        </div>
        """, unsafe_allow_html=True)

    # Time-Series Quality Score Chart
    st.plotly_chart(create_quality_trend_chart(trend_history), use_container_width=True)

    col_ch1, col_ch2 = st.columns(2)
    with col_ch1:
        st.plotly_chart(create_risk_distribution_chart(all_tests), use_container_width=True)
    with col_ch2:
        st.plotly_chart(create_sample_type_pie(all_tests), use_container_width=True)

    # Recent Test History Table
    st.markdown("#### 📋 Recent Evaluation Logs")
    if all_tests:
        table_data = []
        for t in all_tests[:10]:
            table_data.append({
                "Batch ID": t["batch_id"],
                "Date": t["timestamp"][:16].replace("T", " "),
                "Type": t["sample_type"],
                "Score": f"{t['quality_score']:.0f}/100",
                "Visual Finding": t["visual_prediction"],
                "Mould": t["mould_risk"],
                "Risk": t["overall_risk"]
            })
        st.dataframe(table_data, use_container_width=True)
    else:
        st.write("No test records in database yet. Run a test using the Quality Scanner to populate logs.")


# ---------------------------------------------------------
# PAGE 6: 📦 FEED PASSPORT
# ---------------------------------------------------------
elif menu_option == "📦 Feed Passport":
    st.markdown(render_page_header("📦 Digital Feed Passport Gallery", "Certified batch passports ensuring tamper-evident quality traceability from farm to dairy cooperative"), unsafe_allow_html=True)

    recent_tests = get_all_tests(limit=20)
    if not recent_tests:
        st.info("No Digital Feed Passports have been generated yet. Use the Quality Scanner to evaluate a batch.")
    else:
        st.markdown(f"Displaying **{len(recent_tests)}** registered Feed Passports:")
        for t in recent_tests:
            passport = get_digital_feed_passport(t["batch_id"])
            if passport:
                qr_path = PROJECT_ROOT / "generated_qr" / f"{passport['batch_id'].replace('-', '_')}.png"
                if not qr_path.exists():
                    generate_feed_passport_qr(passport["batch_id"])

                cert_html = render_passport_certificate(passport, str(qr_path))
                st.markdown(cert_html, unsafe_allow_html=True)


# ---------------------------------------------------------
# PAGE 7: 🔎 BATCH LOOKUP
# ---------------------------------------------------------
elif menu_option == "🔎 Batch Lookup":
    st.markdown(render_page_header("🔎 Digital Passport & QR Lookup", "Scan a Feed Passport QR code or enter Batch ID to verify quality history and authenticity"), unsafe_allow_html=True)

    lookup_method = st.radio("Verification Method:", ["Enter Batch ID Manually", "Upload & Decode QR Image"], horizontal=True)
    batch_to_find = None

    if lookup_method == "Enter Batch ID Manually":
        input_id = st.text_input("Enter Batch ID (e.g., SFA-2026-000001):", "")
        if st.button("🔎 Fetch Digital Passport", type="primary"):
            batch_to_find = input_id.strip()

    else:
        qr_upload = st.file_uploader("Upload QR Code Image:", type=["png", "jpg", "jpeg"])
        if qr_upload:
            qr_img = Image.open(qr_upload)
            st.image(qr_img, width=160, caption="Uploaded QR Code")
            with st.spinner("Decoding QR Code..."):
                decoded = decode_qr_image(qr_img)
                if decoded:
                    st.success(f"Decoded Batch ID: `{decoded}`")
                    batch_to_find = decoded
                else:
                    st.error("Could not decode a valid Batch ID from this image. Ensure the QR is clear and well-lit.")

    if batch_to_find:
        passport = get_digital_feed_passport(batch_to_find)
        if passport:
            qr_path = PROJECT_ROOT / "generated_qr" / f"{passport['batch_id'].replace('-', '_')}.png"
            if not qr_path.exists():
                generate_feed_passport_qr(passport["batch_id"])

            cert_html = render_passport_certificate(passport, str(qr_path))
            st.markdown(cert_html, unsafe_allow_html=True)
        else:
            st.error(f"No test record found in database for Batch ID: `{batch_to_find}`. Please verify the ID.")
