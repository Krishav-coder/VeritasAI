"""
Veritas AI - Main Application Entry Point
Deepfake Detection with Explainable AI
"""

import os
import sys

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULE_PATH = os.path.join(BASE_DIR, "module")

if MODULE_PATH not in sys.path:
    sys.path.insert(0, MODULE_PATH)

# Import modules using relative paths
from module import detector, llm


def analyze_and_explain(image_path):
    """
    Main API function for analyzing an image and generating explanation.
    
    Args:
        image_path: Path to the image file to analyze
        
    Returns:
        dict: Contains prediction, confidence, model_version, heatmap_path, 
              limitations, and explanation
    """
    result = detector.analyze_image(image_path)
    explanation = llm.generate_explanation(result)
    result["explanation"] = explanation
    return result


if __name__ == "__main__":
    # Test the function
    import tempfile
    print("â Veritas AI backend loaded successfully")
    print(f"   Base directory: {BASE_DIR}")
    print(f"   Module path: {MODULE_PATH}")
