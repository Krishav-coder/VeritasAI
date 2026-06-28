import sys

MODULE_PATH = "/content/drive/MyDrive/VeritasAI/module"

if MODULE_PATH not in sys.path:
    sys.path.insert(0, MODULE_PATH)



import importlib.util

# -----------------------------
# Load Detector Module
# -----------------------------
detector_spec = importlib.util.spec_from_file_location(
    "detector",
    "/content/drive/MyDrive/VeritasAI/module/detector.py"
)

detector = importlib.util.module_from_spec(detector_spec)
detector_spec.loader.exec_module(detector)


# -----------------------------
# Load LLM Module
# -----------------------------
llm_spec = importlib.util.spec_from_file_location(
    "llm",
    "/content/drive/MyDrive/VeritasAI/module/llm.py"
)

llm = importlib.util.module_from_spec(llm_spec)
llm_spec.loader.exec_module(llm)


# -----------------------------
# Main API
# -----------------------------
def analyze_and_explain(image_path):

    result = detector.analyze_image(image_path)

    explanation = llm.generate_explanation(result)

    result["explanation"] = explanation

    return result