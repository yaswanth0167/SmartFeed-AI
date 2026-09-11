"""
SmartFeed AI - Demo Sample Image Generator
Generates high-contrast sample images for hackathon demonstrations:
1. Healthy Golden Cattle Feed
2. Mouldy Feed with Fungal Mycelium Patches
3. Heat-Damaged / Burnt Feed
"""

import cv2
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_DIR = PROJECT_ROOT / "data" / "sample_images"


def generate_sample_images():
    """Creates synthetic feed demo images for instant UI testing."""
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Clean Golden Feed
    h, w = 400, 400
    clean = np.full((h, w, 3), (40, 175, 220), dtype=np.uint8)  # Golden Yellow in BGR
    # Add subtle grain texture
    noise = np.random.normal(0, 10, (h, w, 3)).astype(np.int16)
    clean = np.clip(clean.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    cv2.imwrite(str(SAMPLE_DIR / "sample_healthy_feed.jpg"), clean)

    # 2. Mouldy Feed
    mouldy = clean.copy()
    # Add white/pale grey fungal mycelium colonies
    cv2.circle(mouldy, (140, 160), 55, (235, 240, 245), -1)
    cv2.circle(mouldy, (270, 250), 45, (230, 235, 240), -1)
    cv2.circle(mouldy, (220, 130), 35, (225, 230, 235), -1)
    # Blur colonies to look organic
    mouldy = cv2.GaussianBlur(mouldy, (15, 15), 0)
    cv2.imwrite(str(SAMPLE_DIR / "sample_mouldy_feed.jpg"), mouldy)

    # 3. Burnt / Heat-Damaged Feed
    burnt = clean.copy()
    # Add dark scorch patches
    cv2.ellipse(burnt, (200, 200), (90, 60), 30, 0, 360, (20, 25, 25), -1)
    cv2.circle(burnt, (100, 100), 40, (15, 20, 20), -1)
    cv2.circle(burnt, (300, 300), 35, (25, 30, 30), -1)
    burnt = cv2.GaussianBlur(burnt, (11, 11), 0)
    cv2.imwrite(str(SAMPLE_DIR / "sample_burnt_feed.jpg"), burnt)

    # 4. Fresh Silage (Olive Green)
    silage_fresh = np.full((h, w, 3), (35, 130, 85), dtype=np.uint8)
    silage_noise = np.random.normal(0, 12, (h, w, 3)).astype(np.int16)
    silage_fresh = np.clip(silage_fresh.astype(np.int16) + silage_noise, 0, 255).astype(np.uint8)
    cv2.imwrite(str(SAMPLE_DIR / "sample_fresh_silage.jpg"), silage_fresh)

    print(f"[SUCCESS] Sample images generated in: {SAMPLE_DIR}")


if __name__ == "__main__":
    generate_sample_images()
