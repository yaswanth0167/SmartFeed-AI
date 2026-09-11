"""
SmartFeed AI - Quality Trend Analytics & Early Spoilage Warning Module
Computes dashboard metrics, analyzes historical trajectories, triggers early spoilage
alerts (without false certainty), and creates interactive Plotly visualizations.
"""

from typing import List, Dict, Any, Optional
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def compute_dashboard_metrics(tests: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes summary KPIs across all recorded feed evaluations.
    
    Args:
        tests: List of test dictionaries from database.
        
    Returns:
        dict: Total tests, average score, counts by risk category, and breakdowns.
    """
    total = len(tests)
    if total == 0:
        return {
            "total_tests": 0,
            "avg_quality_score": 0.0,
            "safe_tests": 0,
            "caution_tests": 0,
            "high_risk_tests": 0,
            "safe_pct": 0.0,
            "high_risk_pct": 0.0,
            "sample_type_counts": {},
            "recent_activity": []
        }

    scores = [float(t.get("quality_score", 0.0)) for t in tests]
    avg_score = sum(scores) / total

    safe_count = 0
    caution_count = 0
    high_risk_count = 0
    type_counts: Dict[str, int] = {}

    for t in tests:
        score = float(t.get("quality_score", 0.0))
        risk = str(t.get("overall_risk", "")).lower()

        if score >= 80.0 and risk != "high":
            safe_count += 1
        elif score >= 50.0 and risk != "high":
            caution_count += 1
        else:
            high_risk_count += 1

        st = t.get("sample_type", "Feed Ingredient")
        type_counts[st] = type_counts.get(st, 0) + 1

    return {
        "total_tests": total,
        "avg_quality_score": round(avg_score, 1),
        "safe_tests": safe_count,
        "caution_tests": caution_count,
        "high_risk_tests": high_risk_count,
        "safe_pct": round((safe_count / total) * 100, 1),
        "high_risk_pct": round((high_risk_count / total) * 100, 1),
        "sample_type_counts": type_counts,
        "recent_activity": tests[:5]
    }


def detect_early_spoilage_warning(trend_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evaluates chronological records to detect progressive feed deterioration.
    
    CRITICAL SCIENTIFIC STANDARD:
    Does NOT predict exact future dates. Uses 'Potential Spoilage Risk'.
    
    Args:
        trend_records: Chronologically sorted list of test records (oldest first).
        
    Returns:
        dict: Warning status, severity, identified drivers, and actionable recommendations.
    """
    if len(trend_records) < 2:
        return {
            "has_warning": False,
            "severity": "None",
            "title": "Insufficient Trend Data",
            "message": "At least 2 sequential tests are required to detect spoilage trajectories.",
            "reasons": [],
            "recommendation": "Continue periodic quality monitoring every 2–3 days."
        }

    # Analyze last 4 records
    recent = trend_records[-4:]
    scores = [float(r.get("quality_score", 0.0)) for r in recent]
    moistures = [float(r.get("moisture", 0.0)) for r in recent]
    mould_risks = [str(r.get("mould_risk", "Low")).lower() for r in recent]

    reasons = []
    has_warning = False
    severity = "None"

    # 1. Total Decline Delta Check
    total_drop = scores[0] - scores[-1]
    if total_drop >= 20.0:
        has_warning = True
        severity = "Severe"
        reasons.append(f"Feed Quality Score dropped significantly by {total_drop:.1f} points across recent tests ({scores[0]:.0f} → {scores[-1]:.0f}).")
    elif total_drop >= 12.0:
        has_warning = True
        severity = "Moderate"
        reasons.append(f"Feed Quality Score decreased by {total_drop:.1f} points ({scores[0]:.0f} → {scores[-1]:.0f}).")

    # 2. Consistent Downward Trajectory Check
    is_strictly_decreasing = all(scores[i] > scores[i + 1] for i in range(len(scores) - 1))
    if len(scores) >= 3 and is_strictly_decreasing:
        has_warning = True
        if severity == "None":
            severity = "Moderate"
        reasons.append("Quality score has declined consistently across consecutive tests.")

    # 3. Moisture Increase Check
    if len(moistures) >= 2 and moistures[-1] > moistures[0] + 2.5:
        has_warning = True
        reasons.append(f"Moisture has risen from {moistures[0]:.1f}% to {moistures[-1]:.1f}%, accelerating potential microbial growth.")

    # 4. Emerging Mould Trend
    if "high" in mould_risks[-1] and "high" not in mould_risks[0]:
        has_warning = True
        severity = "Severe"
        reasons.append("Fungal/mould risk has escalated from safe baseline to High in recent tests.")

    if has_warning:
        title = "⚠️ EARLY SPOILAGE WARNING: Potential Spoilage Risk Detected"
        recommendation = (
            "Inspect the feed batch immediately. Avoid long-term storage. "
            "Aerate or sun-dry damp feed, relocate bags to a well-ventilated dry area, "
            "and prioritize feeding older, verified-safe stock first."
        )
    else:
        title = "✅ Stable Quality Trajectory"
        recommendation = "Feed quality trend is steady. Maintain current dry storage practices."

    return {
        "has_warning": has_warning,
        "severity": severity,
        "title": title,
        "total_drop": round(total_drop, 1) if len(scores) >= 2 else 0.0,
        "reasons": reasons,
        "recommendation": recommendation,
        "disclaimer": "Potential Spoilage Risk indicates historical deterioration trends. Exact future expiration dates require biological shelf-life modeling."
    }


def create_quality_trend_chart(trend_records: List[Dict[str, Any]]) -> go.Figure:
    """
    Builds an interactive Plotly time-series chart showing Quality Score over time
    with threshold bands for Safe (80-100), Caution (50-79), and High Risk (0-49).
    """
    fig = go.Figure()

    if not trend_records:
        fig.add_annotation(
            text="No test history available yet. Evaluate feed samples to visualize quality trends.",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="#666666")
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=360
        )
        return fig

    # Extract series data
    timestamps = [r.get("timestamp", "").replace("T", " ")[:16] for r in trend_records]
    scores = [float(r.get("quality_score", 0.0)) for r in trend_records]
    batch_ids = [r.get("batch_id", "") for r in trend_records]
    sample_types = [r.get("sample_type", "Feed") for r in trend_records]
    overall_risks = [r.get("overall_risk", "Unknown") for r in trend_records]

    # Background threshold bands
    fig.add_hrect(y0=80, y1=100, fillcolor="#28a745", opacity=0.10, line_width=0, annotation_text="🟢 Safe Range (80-100)", annotation_position="top left")
    fig.add_hrect(y0=50, y1=80, fillcolor="#ffc107", opacity=0.10, line_width=0, annotation_text="🟡 Caution (50-79)", annotation_position="top left")
    fig.add_hrect(y0=0, y1=50, fillcolor="#dc3545", opacity=0.10, line_width=0, annotation_text="🔴 High Risk (0-49)", annotation_position="bottom left")

    # Main Trend Line
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=scores,
        mode="lines+markers+text",
        name="Quality Score",
        line=dict(color="#1f77b4", width=3, shape="spline"),
        marker=dict(
            size=10,
            color=["#28a745" if s >= 80 else "#ffc107" if s >= 50 else "#dc3545" for s in scores],
            line=dict(width=2, color="#ffffff")
        ),
        text=[f"{s:.0f}" for s in scores],
        textposition="top center",
        hovertext=[
            f"<b>Batch:</b> {b}<br><b>Type:</b> {st}<br><b>Score:</b> {s:.1f}/100<br><b>Risk:</b> {r}"
            for b, st, s, r in zip(batch_ids, sample_types, scores, overall_risks)
        ],
        hoverinfo="text"
    ))

    fig.update_layout(
        title="📈 Feed Quality Score Over Time (0–100)",
        xaxis_title="Test Date & Time",
        yaxis_title="SmartFeed Health Score",
        yaxis=dict(range=[0, 105], dtick=20),
        template="plotly_white",
        height=400,
        margin=dict(l=40, r=40, t=50, b=40),
        hovermode="closest"
    )

    return fig


def create_risk_distribution_chart(tests: List[Dict[str, Any]]) -> go.Figure:
    """Creates a Plotly bar chart showing distribution of Low, Medium, and High risk tests."""
    metrics = compute_dashboard_metrics(tests)
    categories = ["🟢 Safe / Low Risk", "🟡 Caution / Medium Risk", "🔴 High Risk"]
    counts = [metrics["safe_tests"], metrics["caution_tests"], metrics["high_risk_tests"]]
    colors = ["#28a745", "#ffc107", "#dc3545"]

    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=counts,
            marker_color=colors,
            text=counts,
            textposition="auto"
        )
    ])

    fig.update_layout(
        title="📊 Risk Level Breakdown",
        xaxis_title="Risk Category",
        yaxis_title="Batch Count",
        template="plotly_white",
        height=300,
        margin=dict(l=30, r=30, t=40, b=30)
    )
    return fig


def create_sample_type_pie(tests: List[Dict[str, Any]]) -> go.Figure:
    """Creates a Plotly donut chart of evaluated feed types."""
    metrics = compute_dashboard_metrics(tests)
    type_counts = metrics.get("sample_type_counts", {})

    if not type_counts:
        return go.Figure()

    labels = list(type_counts.keys())
    values = list(type_counts.values())

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.45,
        marker=dict(colors=["#2ca02c", "#1f77b4", "#ff7f0e", "#9467bd"])
    )])

    fig.update_layout(
        title="🌾 Feed Types Evaluated",
        template="plotly_white",
        height=300,
        margin=dict(l=30, r=30, t=40, b=30)
    )
    return fig
