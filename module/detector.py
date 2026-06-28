import os
import cv2
import numpy as np
import tensorflow as tf
import sys

MODULE_PATH = "/content/drive/MyDrive/VeritasAI/module"

if MODULE_PATH not in sys.path:
    sys.path.insert(0, MODULE_PATH)

    
from gradcam import (
    preprocess_image,
    compute_gradcam,
    overlay_heatmap
)

IMG_SIZE = (299, 299)

MODEL_PATH = "/content/drive/MyDrive/VeritasAI/models/veritas_xception_v2_finetuned.keras"

OUTPUT_DIR = "/content/veritas_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load model once
model = tf.keras.models.load_model(MODEL_PATH)

print("✅ Veritas model loaded")


def predict_image(img_path):

    img = cv2.imread(img_path)

    if img is None:
        raise ValueError(f"Could not load image: {img_path}")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = cv2.resize(img, IMG_SIZE)

    img = tf.keras.applications.xception.preprocess_input(
        img.astype(np.float32)
    )

    img = np.expand_dims(img, axis=0)

    prob = float(model.predict(img, verbose=0)[0][0])

    return prob


def analyze_image(image_path):

    prob = predict_image(image_path)

    prediction = "Real" if prob >= 0.5 else "Fake"

    img_tensor, img_orig = preprocess_image(image_path)

    heatmap, _ = compute_gradcam(
        model,
        img_tensor,
        "block12_sepconv2_act"
    )

    overlay = overlay_heatmap(
        heatmap,
        img_orig
    )

    filename = os.path.splitext(
        os.path.basename(image_path)
    )[0]

    heatmap_path = os.path.join(
        OUTPUT_DIR,
        f"{filename}_gradcam.jpg"
    )

    cv2.imwrite(
        heatmap_path,
        cv2.cvtColor(
            overlay,
            cv2.COLOR_RGB2BGR
        )
    )

    return {
        "prediction": prediction,
        "confidence": round(prob * 100, 2),
        "model_version": "Veritas AI v2",
        "heatmap_path": heatmap_path,
        "limitations": [
            "External evaluation revealed limited cross-dataset generalization.",
            "Predictions should not be treated as definitive evidence."
        ]
    }