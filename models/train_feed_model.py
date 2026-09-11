"""
SmartFeed AI - MobileNetV2 Feed Ingredient Model Training
Trains a transfer learning model to classify visual defects in feed ingredients:
[good, moldy, burnt, pecky, scorched, greenish].
"""

import os
import sys
import json
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "grain_defects"
MODEL_SAVE_PATH = PROJECT_ROOT / "models" / "feed_quality_model.keras"
LABELS_PATH = PROJECT_ROOT / "models" / "labels.json"

CLASSES = ["good", "moldy", "burnt", "pecky", "scorched", "greenish"]
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
INITIAL_EPOCHS = 15
FINE_TUNE_EPOCHS = 10


def verify_dataset() -> bool:
    """Checks whether the grain defect dataset exists and contains image files."""
    if not DATA_DIR.exists():
        print(f"\n[ERROR] Dataset directory not found: {DATA_DIR}")
        print("Please check data/README_DATASET.md for download instructions.")
        return False

    total_images = 0
    class_counts = {}
    valid_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    for cls in CLASSES:
        cls_dir = DATA_DIR / cls
        if cls_dir.exists():
            count = len([f for f in cls_dir.iterdir() if f.suffix.lower() in valid_exts])
        else:
            count = 0
        class_counts[cls] = count
        total_images += count

    print("\n--- Feed Ingredient Dataset Summary ---")
    for cls, count in class_counts.items():
        print(f"  • {cls:10s}: {count} images")
    print(f"Total Images: {total_images}\n")

    if total_images < 10:
        print("[WARNING] Dataset contains fewer than 10 total images.")
        print("Model training requires images placed in data/grain_defects/<class>/.")
        print("Refer to data/README_DATASET.md to download and unpack the dataset.\n")
        return False

    return True


def train():
    """Builds, trains, fine-tunes, and evaluates the MobileNetV2 transfer learning model."""
    if not verify_dataset():
        print("[INFO] Dataset check completed. Exiting training without error.")
        return

    try:
        import tensorflow as tf
        from tensorflow.keras import layers, models
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
    except ImportError:
        print("\n[NOTICE] TensorFlow is not installed in the current Python environment.")
        print("To train deep learning models, install TensorFlow (or run in Python <= 3.12).")
        print("SmartFeed AI will continue using its OpenCV & heuristic visual analyzer fallback.\n")
        return

    print(f"[INFO] Initializing TensorFlow version: {tf.__version__}")

    # 1. Dataset Loading & Train-Val Split
    print("[INFO] Loading and splitting dataset (80% train, 20% validation)...")
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR,
        validation_split=0.2,
        subset="training",
        seed=42,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_names=CLASSES
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR,
        validation_split=0.2,
        subset="validation",
        seed=42,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_names=CLASSES
    )

    # Dataset optimization with caching & prefetching
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # 2. Data Augmentation Pipeline
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.2),
        layers.RandomContrast(0.1),
    ], name="data_augmentation")

    # 3. Base MobileNetV2 Pre-trained on ImageNet
    print("[INFO] Loading MobileNetV2 base weights (ImageNet)...")
    base_model = MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False  # Freeze base during feature extraction

    # Preprocessing layer for MobileNetV2
    preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input

    # 4. Architecture Assembly
    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = data_augmentation(inputs)
    x = preprocess_input(x)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D(name="avg_pool")(x)
    x = layers.Dropout(0.3, name="top_dropout")(x)
    x = layers.Dense(128, activation="relu", name="dense_features")(x)
    x = layers.Dropout(0.2, name="feature_dropout")(x)
    outputs = layers.Dense(len(CLASSES), activation="softmax", name="predictions")(x)

    model = tf.keras.Model(inputs, outputs, name="smartfeed_mobilenetv2")

    # 5. Model Compilation
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    model.summary()

    # Callbacks
    callbacks = [
        EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True, verbose=1),
        ModelCheckpoint(str(MODEL_SAVE_PATH), monitor="val_accuracy", save_best_only=True, verbose=1),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, verbose=1)
    ]

    # 6. Phase 1: Train Classifier Head
    print(f"\n[INFO] Starting Phase 1: Training classifier head ({INITIAL_EPOCHS} epochs)...")
    history_phase1 = model.fit(
        train_ds,
        epochs=INITIAL_EPOCHS,
        validation_data=val_ds,
        callbacks=callbacks
    )

    # 7. Phase 2: Fine-Tuning Top Layers
    print("\n[INFO] Unfreezing top layers of MobileNetV2 for fine-tuning...")
    base_model.trainable = True
    # Freeze all layers before layer 100
    for layer in base_model.layers[:100]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),  # Lower learning rate
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    total_epochs = INITIAL_EPOCHS + FINE_TUNE_EPOCHS
    print(f"[INFO] Starting Phase 2: Fine-tuning ({FINE_TUNE_EPOCHS} epochs)...")
    history_fine = model.fit(
        train_ds,
        epochs=total_epochs,
        initial_epoch=history_phase1.epoch[-1] + 1,
        validation_data=val_ds,
        callbacks=callbacks
    )

    # 8. Evaluation
    print("\n[INFO] Evaluating final model on validation data...")
    val_loss, val_acc = model.evaluate(val_ds, verbose=0)
    print("=" * 50)
    print(f"Validation Loss:     {val_loss:.4f}")
    print(f"Validation Accuracy: {val_acc * 100:.2f}%")
    print("=" * 50)

    # Save final model
    MODEL_SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(MODEL_SAVE_PATH))
    print(f"[SUCCESS] Trained model saved to: {MODEL_SAVE_PATH}")


if __name__ == "__main__":
    train()
