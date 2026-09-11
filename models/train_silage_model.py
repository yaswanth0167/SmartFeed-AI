"""
SmartFeed AI - MobileNetV2 Silage Quality Model Training
Trains a transfer learning model to classify silage preservation:
[fresh, spoiled].
"""

import os
import sys
import json
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SILAGE_DIR = PROJECT_ROOT / "data" / "silage"
MODEL_SAVE_PATH = PROJECT_ROOT / "models" / "silage_quality_model.keras"
LABELS_PATH = PROJECT_ROOT / "models" / "silage_labels.json"

CLASSES = ["fresh", "spoiled"]
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 20


def verify_silage_dataset() -> bool:
    """Checks whether the silage dataset exists and contains image files."""
    if not SILAGE_DIR.exists():
        print(f"\n[ERROR] Silage dataset directory not found: {SILAGE_DIR}")
        return False

    fresh_dir = SILAGE_DIR / "fresh"
    spoiled_dir = SILAGE_DIR / "spoiled"

    valid_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    fresh_count = len([f for f in fresh_dir.iterdir() if f.suffix.lower() in valid_exts]) if fresh_dir.exists() else 0
    spoiled_count = len([f for f in spoiled_dir.iterdir() if f.suffix.lower() in valid_exts]) if spoiled_dir.exists() else 0

    print("\n--- Silage Dataset Summary ---")
    print(f"  • Fresh silage images:   {fresh_count}")
    print(f"  • Spoiled silage images: {spoiled_count}")
    print(f"Total Images: {fresh_count + spoiled_count}\n")

    if fresh_count < 5 or spoiled_count < 5:
        print("[WARNING] Silage model dataset not yet available or contains fewer than 5 images per class.")
        print("Please add labelled images to:")
        print("  - data/silage/fresh")
        print("  - data/silage/spoiled")
        print("SmartFeed AI will operate using OpenCV visual analysis heuristics.\n")
        return False

    return True


def train_silage():
    """Trains a transfer learning binary classifier on silage images."""
    if not verify_silage_dataset():
        print("[INFO] Silage dataset verification completed. Exiting training without error.")
        return

    try:
        import tensorflow as tf
        from tensorflow.keras import layers, models
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
    except ImportError:
        print("\n[NOTICE] TensorFlow is not installed in the current Python environment.")
        print("To train deep learning models, install TensorFlow (or run in Python <= 3.12).")
        print("SmartFeed AI will continue using OpenCV heuristic analysis.\n")
        return

    print(f"[INFO] Initializing TensorFlow version: {tf.__version__}")

    # Dataset loading
    train_ds = tf.keras.utils.image_dataset_from_directory(
        SILAGE_DIR,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_names=CLASSES
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        SILAGE_DIR,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_names=CLASSES
    )

    # Data Augmentation
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.2),
    ])

    # Base MobileNetV2
    base_model = MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False

    preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input

    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = data_augmentation(inputs)
    x = preprocess_input(x)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(len(CLASSES), activation="softmax")(x)

    model = tf.keras.Model(inputs, outputs, name="silage_mobilenetv2")

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    callbacks = [
        EarlyStopping(monitor="val_loss", patience=4, restore_best_weights=True),
        ModelCheckpoint(str(MODEL_SAVE_PATH), monitor="val_accuracy", save_best_only=True)
    ]

    print(f"[INFO] Training Silage Model ({EPOCHS} epochs)...")
    model.fit(
        train_ds,
        epochs=EPOCHS,
        validation_data=val_ds,
        callbacks=callbacks
    )

    val_loss, val_acc = model.evaluate(val_ds, verbose=0)
    print(f"Validation Accuracy: {val_acc * 100:.2f}%")

    MODEL_SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(MODEL_SAVE_PATH))
    print(f"[SUCCESS] Silage model saved to: {MODEL_SAVE_PATH}")


if __name__ == "__main__":
    train_silage()
