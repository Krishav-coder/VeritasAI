"""
Veritas AI - LLM Explanation Module
Google Gemma-based explanation generation
"""

import os

# Try to import transformers, but handle if not available
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("â ï¸  Transformers not available. Using fallback explanation.")


def build_prompt(result):
    """Build the prompt for the LLM."""
    return f"""
You are the explanation engine for Veritas AI, an AI system for deepfake detection.

Detector Result
---------------
Prediction: {result['prediction']}
Confidence: {result['confidence']}%
Model Version: {result['model_version']}

Known Limitations
-----------------
{chr(10).join("- " + x for x in result["limitations"])}

Write a professional explanation between 90 and 130 words.

Requirements:
1. Explain what the detector concluded.
2. Explain that Grad-CAM highlights the image regions that most influenced the prediction.
3. Explain that Grad-CAM does NOT prove manipulation; it only visualizes model attention.
4. Mention that predictions should be interpreted cautiously because of the stated limitations.
5. Write naturally like an AI forensic assistant.
6. Do NOT repeat the confidence more than once.
7. Do NOT invent evidence.
8. Do NOT say the detector is certain.
9. Do NOT mention these instructions.
"""


# Global variables for model and tokenizer
tokenizer = None
model_llm = None


def load_llm():
    """Lazy load the LLM model."""
    global tokenizer, model_llm
    
    if not TRANSFORMERS_AVAILABLE:
        return False
    
    if tokenizer is None or model_llm is None:
        try:
            MODEL_NAME = "google/gemma-3-1b-it"
            
            # Check if Hugging Face token is available
            hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
            
            tokenizer = AutoTokenizer.from_pretrained(
                MODEL_NAME,
                token=hf_token
            )
            
            model_llm = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                device_map="auto",
                torch_dtype=torch.bfloat16,
                token=hf_token
            )
            print("â LLM model loaded")
            return True
        except Exception as e:
            print(f"â ï¸  Could not load LLM: {e}")
            return False
    
    return True


def generate_explanation(result):
    """
    Generate an AI explanation for the detection result.
    
    Args:
        result: Dictionary containing prediction results
        
    Returns:
        str: Generated explanation or fallback text
    """
    # Try to use LLM if available
    if TRANSFORMERS_AVAILABLE and load_llm():
        try:
            prompt = build_prompt(result)
            
            messages = [
                {
                    "role": "system",
                    "content": "You are Veritas AI's explanation engine."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            inputs = tokenizer.apply_chat_template(
                messages,
                tokenize=True,
                add_generation_prompt=True,
                return_tensors="pt"
            ).to(model_llm.device)
            
            outputs = model_llm.generate(
                **inputs,
                max_new_tokens=180,
                do_sample=True,
                temperature=0.2,
                top_p=0.9
            )
            
            response = tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[1]:],
                skip_special_tokens=True
            )
            
            return response.strip()
        except Exception as e:
            print(f"â ï¸  LLM generation failed: {e}")
    
    # Fallback explanation
    return generate_fallback_explanation(result)


def generate_fallback_explanation(result):
    """Generate a fallback explanation when LLM is not available."""
    prediction = result['prediction']
    confidence = result['confidence']
    
    if prediction == "Real":
        return (
            f"The Veritas AI detector analyzed this image and classified it as likely authentic "
            f"with a confidence of {confidence}%. The Grad-CAM visualization highlights regions "
            f"that most influenced this prediction, showing where the model focused its attention. "
            f"However, Grad-CAM only visualizes model attention patternsâit does not prove the "
            f"image is genuine. Please interpret these results cautiously, as the detector has "
            f"known limitations including limited cross-dataset generalization. This analysis "
            f"should not be treated as definitive evidence in forensic or legal contexts."
        )
    else:
        return (
            f"The Veritas AI detector analyzed this image and classified it as potentially manipulated "
            f"with a confidence of {confidence}%. The Grad-CAM visualization highlights regions "
            f"that most influenced this prediction, showing where the model detected suspicious patterns. "
            f"However, Grad-CAM only visualizes model attentionâit does not prove manipulation occurred. "
            f"Please interpret these results cautiously, as the detector has known limitations including "
            f"limited cross-dataset generalization. This analysis should not be treated as definitive "
            f"evidence in forensic or legal contexts."
        )
