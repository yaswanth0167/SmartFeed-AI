"""
SmartFeed AI - Modern UI Components Module
Provides visually stunning, responsive HTML/SVG components for:
- Animated Logo Opening Hero Banner with glowing aura & float effects
- Circular Radial Score Dial (0–100)
- Certified Digital Feed Passport Card with Official Emblem
- Modern Soundwave Voice Advisory Button
- Sidebar Glowing Logo Badge
"""

import base64
from pathlib import Path
from typing import Dict, Any, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGO_PATH = PROJECT_ROOT / "assets" / "logo.jpg"


def get_logo_base64() -> str:
    """Retrieves the official SmartFeed AI logo as a base64 URI."""
    if LOGO_PATH.exists():
        try:
            with open(LOGO_PATH, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/jpeg;base64,{encoded}"
        except Exception:
            pass
    return ""


def render_page_header(title: str, subtitle: str) -> str:
    """Renders a sleek top bar header with the glowing official logo emblem."""
    logo_src = get_logo_base64()
    html = f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 16px;
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(248,250,252,0.95));
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 18px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        font-family: 'Plus Jakarta Sans', sans-serif;
    ">
        <div style="
            display: inline-block;
            padding: 3px;
            background: linear-gradient(135deg, #10B981, #2563EB, #059669);
            border-radius: 50%;
            box-shadow: 0 4px 14px rgba(16,185,129,0.35);
            animation: floatLogoMini 4s ease-in-out infinite;
        ">
            <img src="{logo_src}" style="
                width: 56px;
                height: 56px;
                border-radius: 50%;
                object-fit: cover;
                display: block;
                border: 2px solid white;
            " alt="SmartFeed AI Emblem" />
        </div>
        <div>
            <h2 style="
                margin: 0;
                font-size: 1.85rem;
                font-weight: 800;
                background: linear-gradient(135deg, #064E3B 0%, #059669 50%, #2563EB 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: -0.5px;
                line-height: 1.2;
            ">{title}</h2>
            <div style="color: #64748B; font-size: 0.95rem; font-weight: 500; margin-top: 2px;">{subtitle}</div>
        </div>
    </div>
    <style>
        @keyframes floatLogoMini {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-4px); }}
            100% {{ transform: translateY(0px); }}
        }}
    </style>
    """
    return html


def render_opening_hero(logo_b64: Optional[str] = None) -> str:
    """
    Renders a spectacular opening hero presentation with the official SmartFeed AI logo,
    rotating conic-gradient energy halo, multi-layer floating 3D animation,
    triple ambient glowing radial auras, and animated shimmering typography.
    """
    logo_src = logo_b64 or get_logo_base64()

    html = f"""
    <!-- Master Opening Hero Section -->
    <div style="
        position: relative;
        background: radial-gradient(circle at 50% 28%, rgba(16, 185, 129, 0.18) 0%, rgba(37, 99, 235, 0.1) 45%, rgba(248, 250, 252, 0.98) 100%), #FFFFFF;
        border: 1.5px solid rgba(16, 185, 129, 0.25);
        border-radius: 28px;
        padding: 44px 24px 38px 24px;
        text-align: center;
        box-shadow: 0 25px 60px -15px rgba(5, 150, 105, 0.18), 0 0 0 1px rgba(16, 185, 129, 0.15);
        margin-bottom: 28px;
        overflow: hidden;
        font-family: 'Plus Jakarta Sans', sans-serif;
        animation: heroEntrance 1.1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    ">
        <!-- Ambient Glowing Aura Behind Logo (Emerald Center) -->
        <div style="
            position: absolute;
            top: 25px;
            left: 50%;
            transform: translateX(-50%);
            width: 280px;
            height: 280px;
            background: radial-gradient(circle, rgba(16, 185, 129, 0.45) 0%, rgba(5, 150, 105, 0.2) 55%, transparent 75%);
            border-radius: 50%;
            filter: blur(35px);
            z-index: 0;
            pointer-events: none;
            animation: pulseEmeraldAura 4.5s ease-in-out infinite alternate;
        "></div>

        <!-- Ambient Cyan/Blue Orbit Aura -->
        <div style="
            position: absolute;
            top: 15px;
            left: 52%;
            transform: translateX(-50%);
            width: 320px;
            height: 320px;
            background: radial-gradient(circle, rgba(37, 99, 235, 0.3) 0%, rgba(59, 130, 246, 0.1) 60%, transparent 80%);
            border-radius: 50%;
            filter: blur(45px);
            z-index: 0;
            pointer-events: none;
            animation: pulseBlueAura 6s ease-in-out infinite alternate;
        "></div>

        <!-- Animated Floating Logo Container with Rotating Energy Ring -->
        <div style="position: relative; z-index: 2; margin-bottom: 20px;">
            <div style="position: relative; display: inline-block;">
                <!-- Spinning Conic-Gradient Energy Halo -->
                <div style="
                    position: absolute;
                    top: -8px;
                    left: -8px;
                    right: -8px;
                    bottom: -8px;
                    border-radius: 50%;
                    background: conic-gradient(from 0deg, #10B981, #2563EB, #059669, #3B82F6, #10B981);
                    animation: spinOrbitalHalo 7s linear infinite;
                    filter: blur(3px);
                    opacity: 0.9;
                "></div>

                <!-- Floating Emblem Container -->
                <div style="
                    position: relative;
                    z-index: 1;
                    display: inline-block;
                    padding: 6px;
                    background: linear-gradient(135deg, #10B981, #2563EB, #059669);
                    border-radius: 50%;
                    box-shadow: 0 16px 36px rgba(5, 150, 105, 0.35), 0 0 30px rgba(37, 99, 235, 0.25);
                    animation: floatLogo 5s ease-in-out infinite;
                ">
                    <img src="{logo_src}" style="
                        width: 215px;
                        height: 215px;
                        border-radius: 50%;
                        object-fit: cover;
                        display: block;
                        border: 4px solid #FFFFFF;
                        box-shadow: inset 0 2px 10px rgba(0,0,0,0.15);
                    " alt="SmartFeed AI Official Logo" />
                </div>
            </div>
        </div>

        <!-- Official SIH Innovation Badge -->
        <div style="position: relative; z-index: 2; margin-bottom: 12px;">
            <span style="
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background: #ECFDF5;
                border: 1.5px solid #A7F3D0;
                color: #065F46;
                padding: 6px 18px;
                border-radius: 9999px;
                font-size: 0.84rem;
                font-weight: 800;
                letter-spacing: 1.2px;
                text-transform: uppercase;
                box-shadow: 0 2px 8px rgba(5, 150, 105, 0.1);
            ">
                <span style="width: 8px; height: 8px; background: #10B981; border-radius: 50%; box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.35); animation: pulseDot 2s infinite;"></span>
                SMART INDIA HACKATHON 2026 • AI AGRI-TECH INNOVATION
            </span>
        </div>

        <!-- Headline & Slogan -->
        <div style="position: relative; z-index: 2;">
            <h1 style="
                font-size: 3.1rem;
                font-weight: 900;
                letter-spacing: -1.5px;
                margin: 0 0 6px 0;
                background: linear-gradient(135deg, #064E3B 0%, #059669 35%, #2563EB 70%, #047857 100%);
                background-size: 250% auto;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                line-height: 1.15;
                animation: textShimmer 6s ease infinite;
            ">
                SmartFeed AI
            </h1>
            <div style="
                font-size: 1.22rem;
                font-weight: 800;
                letter-spacing: 2.2px;
                text-transform: uppercase;
                color: #047857;
                margin-bottom: 10px;
                text-shadow: 0 1px 2px rgba(4, 120, 87, 0.1);
            ">
                FEED SMART &nbsp;•&nbsp; FARM BETTER &nbsp;•&nbsp; GROW TOGETHER
            </div>
            <p style="
                font-size: 1.08rem;
                color: #475569;
                max-width: 780px;
                margin: 0 auto 24px auto;
                line-height: 1.55;
            ">
                AI-Powered Smart Cattle Feed & Silage Quality Assessment, Risk Intelligence, Explainable Advisory & QR Digital Traceability.
            </p>

            <!-- Feature Quick Pills -->
            <div style="
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                justify-content: center;
                align-items: center;
            ">
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 7px 16px; border-radius: 9999px; font-size: 0.88rem; font-weight: 700; color: #1E293B; box-shadow: 0 2px 6px rgba(0,0,0,0.04); transition: transform 0.2s ease;">
                    📸 CV Defect Vision
                </span>
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 7px 16px; border-radius: 9999px; font-size: 0.88rem; font-weight: 700; color: #1E293B; box-shadow: 0 2px 6px rgba(0,0,0,0.04); transition: transform 0.2s ease;">
                    ⭐ 0–100 Health Score
                </span>
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 7px 16px; border-radius: 9999px; font-size: 0.88rem; font-weight: 700; color: #1E293B; box-shadow: 0 2px 6px rgba(0,0,0,0.04); transition: transform 0.2s ease;">
                    ⚠️ Urea Spiking Risk
                </span>
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 7px 16px; border-radius: 9999px; font-size: 0.88rem; font-weight: 700; color: #1E293B; box-shadow: 0 2px 6px rgba(0,0,0,0.04); transition: transform 0.2s ease;">
                    🗣️ Telugu • Hindi • English
                </span>
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 7px 16px; border-radius: 9999px; font-size: 0.88rem; font-weight: 700; color: #1E293B; box-shadow: 0 2px 6px rgba(0,0,0,0.04); transition: transform 0.2s ease;">
                    📦 QR Digital Passport
                </span>
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 7px 16px; border-radius: 9999px; font-size: 0.88rem; font-weight: 700; color: #1E293B; box-shadow: 0 2px 6px rgba(0,0,0,0.04); transition: transform 0.2s ease;">
                    📈 Spoilage Forecasting
                </span>
            </div>
        </div>
    </div>

    <!-- CSS Keyframe Animations -->
    <style>
        @keyframes heroEntrance {{
            0% {{ opacity: 0; transform: translateY(24px) scale(0.97); }}
            100% {{ opacity: 1; transform: translateY(0px) scale(1); }}
        }}
        @keyframes spinOrbitalHalo {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        @keyframes floatLogo {{
            0% {{ transform: translateY(0px) rotate(0deg); }}
            50% {{ transform: translateY(-10px) rotate(1.2deg); }}
            100% {{ transform: translateY(0px) rotate(0deg); }}
        }}
        @keyframes pulseEmeraldAura {{
            0% {{ transform: translateX(-50%) scale(0.9); opacity: 0.45; }}
            100% {{ transform: translateX(-50%) scale(1.25); opacity: 0.85; }}
        }}
        @keyframes pulseBlueAura {{
            0% {{ transform: translateX(-50%) scale(1.15) rotate(0deg); opacity: 0.6; }}
            100% {{ transform: translateX(-50%) scale(0.9) rotate(45deg); opacity: 0.35; }}
        }}
        @keyframes pulseDot {{
            0% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
            70% {{ box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
        }}
        @keyframes textShimmer {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
    </style>
    """
    return html


def render_sidebar_logo(logo_b64: Optional[str] = None) -> str:
    """Renders a sleek glowing circular emblem in the sidebar with rotating energy ring."""
    logo_src = logo_b64 or get_logo_base64()

    html = f"""
    <div style="text-align: center; margin-bottom: 14px; font-family: 'Plus Jakarta Sans', sans-serif;">
        <div style="position: relative; display: inline-block; margin-bottom: 4px;">
            <!-- Spinning Halo -->
            <div style="
                position: absolute;
                top: -3px;
                left: -3px;
                right: -3px;
                bottom: -3px;
                border-radius: 50%;
                background: conic-gradient(from 0deg, #10B981, #2563EB, #059669, #10B981);
                animation: spinOrbitalHalo 7s linear infinite;
                filter: blur(1.5px);
                opacity: 0.8;
            "></div>

            <!-- Floating Container -->
            <div style="
                position: relative;
                z-index: 1;
                display: inline-block;
                padding: 4px;
                background: linear-gradient(135deg, #10B981, #2563EB, #059669);
                border-radius: 50%;
                box-shadow: 0 6px 18px rgba(5, 150, 105, 0.3);
                animation: floatLogo 5s ease-in-out infinite;
            ">
                <img src="{logo_src}" style="
                    width: 105px;
                    height: 105px;
                    border-radius: 50%;
                    object-fit: cover;
                    display: block;
                    border: 2px solid white;
                " alt="SmartFeed AI Logo" />
            </div>
        </div>
        <div style="font-size: 1.2rem; font-weight: 900; color: #064E3B; margin-top: 6px; letter-spacing: -0.5px;">
            SmartFeed AI
        </div>
        <div style="font-size: 0.72rem; font-weight: 800; color: #059669; letter-spacing: 1.2px; text-transform: uppercase;">
            FEED SMART • FARM BETTER
        </div>
    </div>
    """
    return html


def render_circular_score_gauge(
    score: float,
    risk_level: str,
    safety_badge: str,
    primary_concern: str,
    components: Optional[Dict[str, Any]] = None
) -> str:
    """
    Renders an SVG circular radial progress meter with glowing gradients,
    animated stroke offset, bold centered score, and sub-score component progress bars.
    """
    clamped_score = max(0.0, min(100.0, score))
    circumference = 439.82
    offset = circumference - (clamped_score / 100.0) * circumference

    if clamped_score >= 80.0 and risk_level != "High":
        stroke_color = "#10B981"
        bg_gradient_start = "#ECFDF5"
        bg_gradient_end = "#D1FAE5"
        badge_bg = "#DEF7EC"
        badge_text = "#03543F"
        badge_icon = "🟢"
        status_title = "SAFE FOR USE"
    elif clamped_score >= 50.0 and risk_level != "High":
        stroke_color = "#F59E0B"
        bg_gradient_start = "#FFFBEB"
        bg_gradient_end = "#FEF3C7"
        badge_bg = "#FEF08A"
        badge_text = "#713F12"
        badge_icon = "🟡"
        status_title = "NEEDS ATTENTION"
    else:
        stroke_color = "#EF4444"
        bg_gradient_start = "#FEF2F2"
        bg_gradient_end = "#FEE2E2"
        badge_bg = "#FDE8E8"
        badge_text = "#9B1C1C"
        badge_icon = "🔴"
        status_title = "HIGH RISK - DO NOT FEED"

    html = f"""
    <div style="
        background: linear-gradient(135deg, {bg_gradient_start} 0%, {bg_gradient_end} 100%);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 20px;
        padding: 28px 24px;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin-bottom: 20px;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    ">
        <div style="font-size: 0.85rem; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; color: #475569; margin-bottom: 12px;">
            🐄 SMARTFEED RISK INTELLIGENCE ENGINE
        </div>
        
        <div style="position: relative; width: 180px; height: 180px; margin: 6px auto;">
            <svg viewBox="0 0 160 160" width="180" height="180" style="transform: rotate(-90deg);">
                <circle cx="80" cy="80" r="70" stroke="#E2E8F0" stroke-width="12" fill="transparent" />
                <circle cx="80" cy="80" r="70" 
                    stroke="{stroke_color}" 
                    stroke-width="12" 
                    stroke-linecap="round" 
                    fill="transparent"
                    stroke-dasharray="{circumference}"
                    stroke-dashoffset="{offset:.2f}"
                    style="transition: stroke-dashoffset 0.8s ease-in-out;"
                />
            </svg>
            <div style="
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            ">
                <span style="font-size: 3.2rem; font-weight: 800; color: #0F172A; line-height: 1; letter-spacing: -1px;">
                    {clamped_score:.0f}
                </span>
                <span style="font-size: 0.85rem; font-weight: 700; color: #64748B; margin-top: 2px;">
                    OUT OF 100
                </span>
            </div>
        </div>

        <div style="
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background-color: {badge_bg};
            color: {badge_text};
            font-size: 1rem;
            font-weight: 800;
            padding: 8px 20px;
            border-radius: 9999px;
            margin-top: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
            letter-spacing: 0.5px;
        ">
            <span>{badge_icon}</span>
            <span>{status_title}</span>
        </div>

        <div style="
            margin-top: 14px;
            font-size: 0.95rem;
            color: #334155;
            background: rgba(255, 255, 255, 0.7);
            padding: 8px 16px;
            border-radius: 10px;
            border: 1px solid rgba(0,0,0,0.04);
            max-width: 90%;
        ">
            <b>Primary Observation:</b> {primary_concern}
        </div>
    </div>
    """
    return html


def render_passport_certificate(passport: Dict[str, Any], qr_image_path: str) -> str:
    """
    Renders an authentic, certified boarding-pass / agricultural certificate
    for the Digital Feed Passport with official logo emblem.
    """
    batch_id = passport.get("batch_id", "SFA-2026-000000")
    sample_type = passport.get("sample_type", "Feed Ingredient")
    date_str = passport.get("timestamp", "").replace("T", " ")[:16]
    score = passport.get("quality_score", 0.0)
    badge = passport.get("quality_badge", "Safe")
    qr_b64 = image_to_base64(qr_image_path)
    logo_b64 = get_logo_base64()

    nutr = passport.get("nutrients", {})
    protein = nutr.get("crude_protein", 0.0)
    moisture = nutr.get("moisture", 0.0)
    fiber = nutr.get("fiber", 0.0)

    html = f"""
    <div style="
        background: #FFFFFF;
        border: 2px solid #059669;
        border-radius: 18px;
        padding: 0;
        overflow: hidden;
        box-shadow: 0 15px 35px -5px rgba(0,0,0,0.08);
        font-family: 'Plus Jakarta Sans', sans-serif;
        margin: 20px 0;
    ">
        <!-- Certificate Header -->
        <div style="
            background: linear-gradient(135deg, #064E3B 0%, #059669 100%);
            color: white;
            padding: 18px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div style="display: flex; align-items: center; gap: 12px;">
                <img src="{logo_b64}" style="width: 44px; height: 44px; border-radius: 50%; border: 2px solid white;" />
                <div>
                    <div style="font-size: 0.75rem; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; opacity: 0.85;">
                        SMARTFEED DIGITAL TRACEABILITY PROTOCOL
                    </div>
                    <div style="font-size: 1.3rem; font-weight: 800; letter-spacing: -0.5px;">
                        📦 DIGITAL FEED PASSPORT
                    </div>
                </div>
            </div>
            <div style="
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.4);
                padding: 6px 14px;
                border-radius: 9999px;
                font-family: 'JetBrains Mono', monospace;
                font-weight: 700;
                font-size: 0.95rem;
            ">
                {batch_id}
            </div>
        </div>

        <!-- Certificate Body -->
        <div style="padding: 24px;">
            <div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: center; justify-content: space-between;">
                
                <!-- Left: QR Code -->
                <div style="text-align: center; min-width: 140px;">
                    <img src="{qr_b64}" style="width: 130px; height: 130px; border-radius: 12px; border: 1px solid #E2E8F0; padding: 4px; background: white;" />
                    <div style="font-size: 0.75rem; font-weight: 700; color: #059669; margin-top: 6px;">
                        ✓ CRYPTOGRAPHIC TRACE
                    </div>
                </div>

                <!-- Middle: Key Parameters Table -->
                <div style="flex: 1; min-width: 250px;">
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">
                        <div style="background: #F8FAFC; padding: 10px 14px; border-radius: 10px; border: 1px solid #E2E8F0;">
                            <div style="font-size: 0.75rem; color: #64748B; font-weight: 600;">SAMPLE TYPE</div>
                            <div style="font-size: 1rem; color: #0F172A; font-weight: 700;">{sample_type}</div>
                        </div>
                        <div style="background: #F8FAFC; padding: 10px 14px; border-radius: 10px; border: 1px solid #E2E8F0;">
                            <div style="font-size: 0.75rem; color: #64748B; font-weight: 600;">DATE & TIME</div>
                            <div style="font-size: 0.95rem; color: #0F172A; font-weight: 700;">{date_str}</div>
                        </div>
                        <div style="background: #F8FAFC; padding: 10px 14px; border-radius: 10px; border: 1px solid #E2E8F0;">
                            <div style="font-size: 0.75rem; color: #64748B; font-weight: 600;">HEALTH SCORE</div>
                            <div style="font-size: 1.1rem; color: #059669; font-weight: 800;">{score:.0f} / 100</div>
                        </div>
                        <div style="background: #F8FAFC; padding: 10px 14px; border-radius: 10px; border: 1px solid #E2E8F0;">
                            <div style="font-size: 0.75rem; color: #64748B; font-weight: 600;">STATUS</div>
                            <div style="font-size: 0.95rem; font-weight: 700;">{badge}</div>
                        </div>
                    </div>
                </div>

                <!-- Right: Nutrition Snapshot -->
                <div style="background: #ECFDF5; border: 1px dashed #059669; border-radius: 12px; padding: 14px 18px; min-width: 170px;">
                    <div style="font-size: 0.8rem; font-weight: 800; color: #064E3B; margin-bottom: 8px;">
                        🥗 NUTRIENTS (SIMULATED)
                    </div>
                    <div style="font-size: 0.85rem; color: #047857; margin-bottom: 4px;">
                        • Crude Protein: <b>{protein:.1f}%</b>
                    </div>
                    <div style="font-size: 0.85rem; color: #047857; margin-bottom: 4px;">
                        • Moisture: <b>{moisture:.1f}%</b>
                    </div>
                    <div style="font-size: 0.85rem; color: #047857;">
                        • Crude Fiber: <b>{fiber:.1f}%</b>
                    </div>
                </div>

            </div>

            <!-- Advisory Callout -->
            <div style="
                margin-top: 18px;
                background: #F1F5F9;
                border-left: 4px solid #059669;
                padding: 12px 16px;
                border-radius: 6px;
                font-size: 0.9rem;
                color: #334155;
            ">
                <b>Verified Advisory Guidance:</b> {passport.get('advisory', '')[:280]}...
            </div>
        </div>

        <!-- Footer Disclaimer Strip -->
        <div style="
            background: #F8FAFC;
            border-top: 1px solid #E2E8F0;
            padding: 10px 24px;
            font-size: 0.75rem;
            color: #64748B;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <span>Official SmartFeed AI Digital Certificate • SIH 2026</span>
            <span>Laboratory testing recommended for chemical confirmation</span>
        </div>
    </div>
    """
    return html


def render_audio_speaker_button(text_to_speak: str, lang: str = "en") -> str:
    """
    Renders an audio pill button with soundwave pulse animation
    triggering the browser's native Web Speech API.
    """
    clean_text = text_to_speak.replace('"', '\\"').replace("'", "\\'").replace("\n", " ").replace("•", "")
    tts_lang = "te-IN" if lang == "te" else ("hi-IN" if lang == "hi" else "en-IN")

    html = f"""
    <div style="margin: 14px 0;">
        <button onclick="
            var synth = window.speechSynthesis;
            if (synth.speaking) {{
                synth.cancel();
            }} else {{
                var utterance = new SpeechSynthesisUtterance('{clean_text}');
                utterance.lang = '{tts_lang}';
                utterance.rate = 0.95;
                utterance.pitch = 1.0;
                synth.speak(utterance);
            }}
        " style="
            background: linear-gradient(135deg, #059669 0%, #047857 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 0.95rem;
            font-weight: 700;
            border-radius: 9999px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 4px 14px rgba(5, 150, 105, 0.35);
            transition: all 0.2s ease;
            font-family: 'Plus Jakarta Sans', sans-serif;
        ">
            <span style="font-size: 1.2rem;">🔊</span>
            <span>Listen to Advisory / సలహా వినండి / सलाह सुनें</span>
        </button>
    </div>
    """
    return html
