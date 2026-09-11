# 🌾 SmartFeed AI - Dataset Setup & Guidelines

This document provides instructions for setting up and managing training datasets for cattle feed ingredients, compound cattle feed, and silage.

---

## 📌 Scientific & Prototype Disclaimer

> **Important Scientific Notice**:
> The grain defect dataset is used as a prototype dataset for visual assessment of feed ingredients. The architecture can later be fine-tuned using cattle-feed-specific and regional fodder datasets.
>
> SmartFeed AI provides **AI-based visual assessment and risk intelligence**. It is a software-only decision support tool and **does NOT replace chemical or microbiological laboratory testing**. Chemical contaminants such as urea, aflatoxins, mycotoxins, heavy metals, and silica require laboratory confirmation.

---

## 1. Primary Dataset: Grain Defects Dataset (Mendeley)

Used for **Visual Feed Ingredient & Cattle Feed Assessment**.

- **Dataset Source**: [Mendeley Data - Grain Defects Dataset](https://data.mendeley.com/datasets/xnx9bfbh6b/1)
- **Target Location**: `data/grain_defects/`

### Expected Folder Structure
Place images in the following subdirectories:

```
data/grain_defects/
├── good/         # Normal, healthy, clean grain & feed ingredients
├── moldy/        # Visible fungal/mould mycelium growth, spore patches
├── burnt/        # Severely heat-damaged or blackened grains
├── pecky/        # Insect-damaged, punctured, or contaminated grains
├── scorched/     # Moderately heat-damaged or discolored grains
└── greenish/     # Immature, abnormally pigmented, or chlorophyll-stained grains
```

### Model Label Mapping
The model maps technical computer vision classes to actionable farmer-friendly terminology:

| Raw Class | Farmer-Friendly Assessment | Risk Level |
|---|---|---|
| `good` | 🟢 Good Quality | Low Risk |
| `moldy` | 🔴 High Mould/Fungal Risk | High Risk |
| `burnt` | 🟡 Heat-Damaged / Quality Warning | Medium Risk |
| `pecky` | 🟡 Defective / Contamination Warning | Medium Risk |
| `scorched` | 🔴 Heat Damage / Spoilage Warning | High Risk |
| `greenish` | 🟡 Abnormal Color / Quality Warning | Medium Risk |

---

## 2. Silage Dataset: Fresh vs. Spoiled

Used for **Silage Fermentation & Preservation Quality Assessment**.

- **Target Location**: `data/silage/`

### Expected Folder Structure
```
data/silage/
├── fresh/       # Well-preserved silage: olive-green/yellowish-brown, firm structure, sweet/lactic aroma
└── spoiled/     # Deteriorated silage: dark brown/black, slimy, visible white/grey mould, butyric discoloration
```

- **Prototype Minimum**: 10–20 images per class with transfer learning and data augmentation.
- If images are not yet collected, the system will provide an informative message and use rule-based visual heuristics rather than crashing.

---

## 3. Training the Models

Once images have been placed in the respective folders:

### Train Feed Ingredient Model:
```powershell
python models/train_feed_model.py
```
This script trains a MobileNetV2 transfer learning model with data augmentation, early stopping, and checkpointing, saving weights to `models/feed_quality_model.keras` and configuration to `models/labels.json`.

### Train Silage Quality Model:
```powershell
python models/train_silage_model.py
```
This script trains a binary classifier (Fresh vs. Spoiled) and saves weights to `models/silage_quality_model.keras`.

---

## 4. Optional Secondary Datasets for Future Refinement
- **Soybean Quality**: [Roboflow Universe - Soybean Quality](https://universe.roboflow.com/newideas/soybean-quality)
- **Grain Label**: [Roboflow Universe - Grain Label](https://universe.roboflow.com/paddy-labelling/grain-label)
- **Wheat Quality**: [Roboflow Universe - Wheat Quality](https://universe.roboflow.com/aspire/wheat_1-o2abp)
