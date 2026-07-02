"""
Veritas AI - Deepfake Detection Module
Xception-based detector with Grad-CAM explainability
"""

import os
import cv2
import numpy as np
import tensorflow as tf

# Get base directory (parent of module folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from module.gradcam import (
    preprocess_image,
    compute_gradcam,
    overlay_heatmap
)

IMG_SIZE = (299, 299)

# Use relative path for model
MODEL_PATH = os.path.join(BASE_DIR, "models", "veritas_xception_v2_finetuned.keras")

# Output directory for Grad-CAM visualizations
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Global model variable
model = None


def load_model():
    """Lazy load the model when needed."""
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}. "
                "Please ensure the model file is in the models/ directory."
            )
        model = tf.keras.models.load_model(MODEL_PATH)
        print("â Veritas model loaded")
    return model


def predict_image(img_path):
    """
    Predict the probability of an image being real.
    
    Args:
        img_path: Path to the image file
        
    Returns:
        float: Probability (0-1) of the image being real
    """
    m = load_model()
    
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Could not load image: {img_path}")
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, IMG_SIZE)
    img = tf.keras.applications.xception.preprocess_input(
        img.astype(np.float32)
    )
    img = np.expand_dims(img, axis=0)
    
    prob = float(m.predict(img, verbose=0)[0][0])
    return prob


def analyze_image(image_path):
    """
    Analyze an image for deepfake detection with Grad-CAM visualization.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        dict: Analysis results including prediction, confidence, heatmap path
    """
    prob = predict_image(image_path)
    prediction = "Real" if prob >= 0.5 else "Fake"
    
    # Generate Grad-CAM visualization
    img_tensor, img_orig = preprocess_image(image_path)
    m = load_model()
    
    heatmap, _ = compute_gradcam(
        m,
        img_tensor,
        "block12_sepconv2_act"
    )
    
    overlay = overlay_heatmap(heatmap, img_orig)
    
    # Save heatmap
    filename = os.path.splitext(os.path.basename(image_path))[0]
    heatmap_path = os.path.join(OUTPUT_DIR, f"{filename}_gradcam.jpg")
    
    cv2.imwrite(
        heatmap_path,
        cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR)
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
