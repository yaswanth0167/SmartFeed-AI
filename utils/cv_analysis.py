"""
SmartFeed AI - OpenCV Computer Vision Analysis Module
Performs deep visual quality inspection of cattle feed and silage:
- Color Analysis (Dark, Greenish, White/Grey fungal patches)
- Texture Analysis (Roughness, Edge Density, Surface Irregularity)
- Possible Foreign Particle Detection (Visual Outliers, Sharp Inclusions)
"""

import cv2
import numpy as np
from pathlib import Path
from PIL import Image
from typing import Union, Dict, Any, Tuple, List


def load_image_to_cv(image_input: Union[str, np.ndarray, Image.Image]) -> np.ndarray:
    """
    Normalizes various image input formats into a standard BGR numpy array.
    
    Args:
        image_input: File path (str), numpy array (BGR or RGB), or PIL Image.
        
    Returns:
        np.ndarray: BGR image array.
    """
    if isinstance(image_input, (str, Path)):
        img = cv2.imread(str(image_input))
        if img is None:
            raise ValueError(f"Could not load image from path: {image_input}")
        return img
    elif isinstance(image_input, Image.Image):
        rgb_arr = np.array(image_input.convert("RGB"))
        return cv2.cvtColor(rgb_arr, cv2.COLOR_RGB2BGR)
    elif isinstance(image_input, np.ndarray):
        if len(image_input.shape) == 2:
            return cv2.cvtColor(image_input, cv2.COLOR_GRAY2BGR)
        elif image_input.shape[2] == 4:
            return cv2.cvtColor(image_input, cv2.COLOR_RGBA2BGR)
        return image_input
    else:
        raise TypeError(f"Unsupported image input type: {type(image_input)}")


def analyze_colors(bgr_img: np.ndarray) -> Dict[str, Any]:
    """
    Analyzes color distribution using HSV color space:
    - Automatically segments background / packaging / container (e.g. white feed sacks, bags, trays)
      so they do NOT get erroneously counted as fungal mould mycelium.
    - Dark/charred patches (low brightness)
    - Greenish patches (chlorophyll / immature grain / green mould)
    - White/grey patches (fungal mycelium / surface mould on feed)
    """
    hsv = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
    h, w = bgr_img.shape[:2]
    total_pixels = h * w

    # 1. Dark Patches: V < 55 (charred, burnt, rotting dark areas)
    raw_dark_mask = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 55]))

    # 2. Greenish Patches: Hue ~ 35 to 85, Saturation > 35, Value > 40
    raw_green_mask = cv2.inRange(hsv, np.array([35, 35, 40]), np.array([85, 255, 255]))

    # 3. White / Pale Grey Patches: High Value (V > 180), Low Saturation (S < 45)
    # Frequently associated with fungal mycelium / powdery mould growth
    raw_white_mask = cv2.inRange(hsv, np.array([0, 0, 180]), np.array([180, 45, 255]))

    # Intelligent Container / Packaging / Backdrop Detection:
    # In agricultural photos, feed is often photographed inside a white plastic / woven sack,
    # on white paper/tray, or on a dark floor.
    # A region is considered packaging/container if:
    # - It is a large white contour (> 3.5% of total image area) that touches the outer image boundary
    # - Or a large dark border contour (> 8% of total image) representing an outer background/bucket.
    container_mask = np.zeros((h, w), dtype=np.uint8)

    white_contours, _ = cv2.findContours(raw_white_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in white_contours:
        area = cv2.contourArea(c)
        x, y, cw, ch = cv2.boundingRect(c)
        touches_border = (x <= 5 or y <= 5 or (x + cw) >= (w - 5) or (y + ch) >= (h - 5))
        if touches_border and area > (total_pixels * 0.035):
            cv2.drawContours(container_mask, [c], -1, 255, -1)

    dark_contours, _ = cv2.findContours(raw_dark_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in dark_contours:
        area = cv2.contourArea(c)
        x, y, cw, ch = cv2.boundingRect(c)
        touches_border = (x <= 5 or y <= 5 or (x + cw) >= (w - 5) or (y + ch) >= (h - 5))
        if touches_border and area > (total_pixels * 0.08):
            cv2.drawContours(container_mask, [c], -1, 255, -1)

    container_pixels = cv2.countNonZero(container_mask)
    feed_pixels = max(int(total_pixels * 0.25), total_pixels - container_pixels)

    # Actual defect pixels isolated strictly to the feed sample region:
    white_grey_mask = cv2.bitwise_and(raw_white_mask, cv2.bitwise_not(container_mask))
    dark_mask = cv2.bitwise_and(raw_dark_mask, cv2.bitwise_not(container_mask))
    green_mask = cv2.bitwise_and(raw_green_mask, cv2.bitwise_not(container_mask))

    white_grey_pixels = cv2.countNonZero(white_grey_mask)
    dark_pixels = cv2.countNonZero(dark_mask)
    green_pixels = cv2.countNonZero(green_mask)

    white_grey_pct = (white_grey_pixels / feed_pixels) * 100.0
    dark_pct = (dark_pixels / feed_pixels) * 100.0
    green_pct = (green_pixels / feed_pixels) * 100.0
    container_pct = (container_pixels / total_pixels) * 100.0

    # Determine Color Risk
    findings = []
    if container_pct > 5.0:
        findings.append(f"Packaging / Container background detected ({container_pct:.1f}% area) and automatically segmented from feed analysis.")

    if white_grey_pct > 8.0:
        findings.append(f"Significant pale white/grey patches detected on feed ({white_grey_pct:.1f}% feed area), suggesting potential fungal or mould mycelium.")
    elif white_grey_pct > 2.5:
        findings.append(f"Mild pale patches detected on feed ({white_grey_pct:.1f}% feed area).")

    if dark_pct > 12.0:
        findings.append(f"Substantial dark/burnt patches detected on feed ({dark_pct:.1f}% feed area), indicating heat scorch or rot.")
    elif dark_pct > 4.0:
        findings.append(f"Minor dark regions detected ({dark_pct:.1f}% feed area).")

    if green_pct > 15.0:
        findings.append(f"Noticeable greenish discoloration ({green_pct:.1f}% feed area), indicating immature grains or chlorophyll residue.")

    if not [f for f in findings if "detected on feed" in f]:
        findings.append("Feed color distribution appears relatively uniform with no extreme discoloration.")

    # Risk level determination
    if white_grey_pct > 8.0 or dark_pct > 15.0:
        color_risk = "High"
    elif white_grey_pct > 2.5 or dark_pct > 5.0 or green_pct > 10.0:
        color_risk = "Medium"
    else:
        color_risk = "Low"

    return {
        "dark_patch_pct": round(dark_pct, 2),
        "greenish_patch_pct": round(green_pct, 2),
        "white_grey_patch_pct": round(white_grey_pct, 2),
        "container_pct": round(container_pct, 2),
        "color_risk": color_risk,
        "findings": findings,
        "masks": {
            "dark": dark_mask,
            "green": green_mask,
            "white_grey": white_grey_mask,
            "container": container_mask
        }
    }


def analyze_texture(bgr_img: np.ndarray) -> Dict[str, Any]:
    """
    Analyzes surface texture, roughness, and edge uniformity:
    - Grayscale conversion
    - Laplacian variance (micro-roughness / focus)
    - Canny edge density (granularity / fragmentation)
    - Contour regularity analysis
    """
    gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
    total_pixels = gray.shape[0] * gray.shape[1]

    # 1. Laplacian Variance (Roughness / Sharp Texture Variation)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    # 2. Canny Edge Density
    edges = cv2.Canny(gray, 60, 160)
    edge_pixels = cv2.countNonZero(edges)
    edge_density = (edge_pixels / total_pixels) * 100.0

    # 3. Contour Regularity & Fragmentation
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_count = len(contours)

    findings = []
    # Classify texture metrics
    if edge_density > 18.0 or laplacian_var > 600.0:
        texture_risk = "High"
        findings.append("High surface irregularity and excessive fragmentation detected.")
    elif edge_density > 8.0 or laplacian_var > 200.0:
        texture_risk = "Medium"
        findings.append("Moderate surface roughness and noticeable particulate variations.")
    else:
        texture_risk = "Low"
        findings.append("Relatively smooth and uniform surface texture.")

    return {
        "roughness_score": round(float(laplacian_var), 2),
        "edge_density_pct": round(float(edge_density), 2),
        "contour_count": contour_count,
        "texture_risk": texture_risk,
        "findings": findings,
        "edge_map": edges
    }


def analyze_foreign_particles(bgr_img: np.ndarray, color_res: Dict[str, Any]) -> Dict[str, Any]:
    """
    Identifies visible anomalous particles, stark color contrasts, or foreign objects.
    Note: Scientifically labeled as 'Possible Foreign Particle Risk' (visual only).
    """
    gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    min_particle_area = int((h * w) * 0.0003)   # ~0.03% of image
    max_particle_area = int((h * w) * 0.05)     # ~5% of image

    # Morphological Top-Hat and Black-Hat to detect bright and dark isolated inclusions
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    inclusions = cv2.add(tophat, blackhat)

    # Exclude packaging / container region so bag folds or seams aren't counted as foreign particles
    container_mask = color_res.get("masks", {}).get("container", None)
    if container_mask is not None:
        inclusions = cv2.bitwise_and(inclusions, cv2.bitwise_not(container_mask))

    # Threshold inclusions
    _, thresh = cv2.threshold(inclusions, 35, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_particles = []
    for c in contours:
        area = cv2.contourArea(c)
        if min_particle_area < area < max_particle_area:
            x, y, cw, ch = cv2.boundingRect(c)
            aspect_ratio = float(cw) / max(ch, 1)
            detected_particles.append({
                "x": int(x), "y": int(y), "w": int(cw), "h": int(ch),
                "area": float(area),
                "aspect_ratio": round(aspect_ratio, 2)
            })

    particle_count = len(detected_particles)
    findings = []

    if particle_count > 15:
        risk_level = "High"
        findings.append(f"Multiple high-contrast visual inclusions ({particle_count} detected) indicating possible foreign particles, stones, or clumps.")
    elif particle_count > 5:
        risk_level = "Medium"
        findings.append(f"A few distinct visual inclusions ({particle_count} detected) that differ from the surrounding feed texture.")
    else:
        risk_level = "Low"
        findings.append("No significant high-contrast foreign particles visually detected.")

    return {
        "risk_level": risk_level,
        "particle_count": particle_count,
        "detected_particles": detected_particles,
        "findings": findings,
        "caveat": "Possible Foreign Particle Risk - AI visual observation only; manual inspection advised."
    }


def generate_annotated_image(bgr_img: np.ndarray, color_res: Dict[str, Any], particle_res: Dict[str, Any]) -> np.ndarray:
    """
    Draws visual detection overlays on a copy of the input image:
    - Red boxes for possible foreign particles
    - Cyan highlights for white/grey mould regions
    - Orange highlights for dark scorched patches
    """
    annotated = bgr_img.copy()

    # Draw foreign particle bounding boxes
    for p in particle_res.get("detected_particles", [])[:20]:
        x, y, w, h = p["x"], p["y"], p["w"], p["h"]
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(annotated, "Particle?", (x, max(15, y - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

    # Highlight mould patches (White/Grey mask contours)
    white_mask = color_res["masks"]["white_grey"]
    mould_contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for mc in mould_contours:
        if cv2.contourArea(mc) > 100:
            cv2.drawContours(annotated, [mc], -1, (255, 255, 0), 1)

    return annotated


def analyze_feed_image(image_input: Union[str, np.ndarray, Image.Image]) -> Dict[str, Any]:
    """
    Full OpenCV computer vision pipeline execution for feed and silage samples.
    
    Args:
        image_input: Image file path, numpy array, or PIL Image.
        
    Returns:
        dict: Complete visual analysis metrics, risks, and findings.
    """
    bgr_img = load_image_to_cv(image_input)
    color_res = analyze_colors(bgr_img)
    texture_res = analyze_texture(bgr_img)
    particle_res = analyze_foreign_particles(bgr_img, color_res)
    annotated_bgr = generate_annotated_image(bgr_img, color_res, particle_res)
    annotated_rgb = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)

    # Calculate overall visual mould risk indicator from CV
    white_grey_pct = color_res["white_grey_patch_pct"]
    if white_grey_pct > 8.0:
        mould_risk = "High"
    elif white_grey_pct > 2.5:
        mould_risk = "Medium"
    else:
        mould_risk = "Low"

    # Base visual quality score estimate (0 to 100)
    # Deductions based purely on CV metrics
    base_score = 100.0
    base_score -= color_res["white_grey_patch_pct"] * 2.5
    base_score -= color_res["dark_patch_pct"] * 1.5
    base_score -= min(30.0, particle_res["particle_count"] * 1.8)
    if texture_res["texture_risk"] == "High":
        base_score -= 10.0
    elif texture_res["texture_risk"] == "Medium":
        base_score -= 5.0
    visual_quality_score = max(5.0, min(100.0, base_score))

    # Compile concise summary
    all_findings = color_res["findings"] + texture_res["findings"] + particle_res["findings"]

    return {
        "color_analysis": {
            "dark_patch_pct": color_res["dark_patch_pct"],
            "greenish_patch_pct": color_res["greenish_patch_pct"],
            "white_grey_patch_pct": color_res["white_grey_patch_pct"],
            "color_risk": color_res["color_risk"],
            "findings": color_res["findings"]
        },
        "texture_analysis": {
            "roughness_score": texture_res["roughness_score"],
            "edge_density_pct": texture_res["edge_density_pct"],
            "contour_count": texture_res["contour_count"],
            "texture_risk": texture_res["texture_risk"],
            "findings": texture_res["findings"]
        },
        "foreign_particle_risk": {
            "risk_level": particle_res["risk_level"],
            "particle_count": particle_res["particle_count"],
            "caveat": particle_res["caveat"],
            "findings": particle_res["findings"]
        },
        "cv_mould_indicator": mould_risk,
        "visual_quality_score": round(visual_quality_score, 1),
        "annotated_image_rgb": annotated_rgb,
        "all_findings": all_findings,
        "summary": " ".join(all_findings[:3])
    }
