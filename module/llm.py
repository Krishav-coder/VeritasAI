from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def build_prompt(result):

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

def generate_explanation(result):

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

MODEL_NAME = "google/gemma-3-1b-it"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model_llm = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    torch_dtype=torch.bfloat16,
)

