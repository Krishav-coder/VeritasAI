# Veritas AI - Deepfake Detection Platform

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13+-orange.svg)](https://tensorflow.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)

This project evaluates a deepfake detector trained and evaluated on DFDC and tested cross-dataset on Celeb-DF v2. It also packages the model in a Streamlit app with Grad-CAM visualizations and optional LLM-based explanations.

## Research Findings

### What Was Tested

The model was trained and evaluated on DFDC, then tested cross-dataset on Celeb-DF v2.

### Performance Delta

The main comparison is between in-distribution performance on DFDC and cross-dataset performance on Celeb-DF v2.

| Evaluation setting | Result |
| --- | --- |
| DFDC (in-distribution) | [ACCURACY/AUC ON DFDC] |
| Celeb-DF v2 (cross-dataset) | [ACCURACY/AUC ON CELEB-DF V2] |

The gap between these results shows how much performance can drop when the same detector is moved outside its training distribution.

### Failure Modes

#### Domain Shift

The model sees a different data distribution in Celeb-DF v2, including changes in source material, face appearance, and capture conditions. Features that work well on DFDC can stop transferring cleanly once the input statistics change.

#### Compression Artifacts

Video and image compression can blur or reshape the manipulation cues the detector relies on. In some cases, the model may also learn shortcuts from compression patterns instead of the deepfake signal itself.

#### Dataset Bias

If the training data overrepresents certain identities, manipulation methods, or visual conditions, the detector can learn dataset-specific correlations. That can make it look strong on DFDC while still failing on a different dataset.

### Takeaway

Deepfake detectors can look strong on the data they were trained on and still fail when tested on a different dataset. That matters because real-world use rarely matches a single benchmark distribution, so cross-dataset evaluation is essential.

## Features

- **Deep Learning Detection**: Xception-based neural network trained for deepfake classification
- **Explainable AI**: Grad-CAM visualizations showing model attention regions
- **AI Explanations**: Natural language explanations powered by Google's Gemma LLM
- **Modern UI**: Professional dark-themed Streamlit interface
- **Production Ready**: Optimized for deployment on Streamlit Community Cloud

## Architecture

```
Veritas AI/
├── app.py                 # Main backend entry point
├── streamlit_app.py       # Streamlit frontend application
├── requirements.txt       # Python dependencies
├── module/
│   ├── detector.py        # Xception-based detection model
│   ├── gradcam.py         # Grad-CAM explainability
│   └── llm.py             # Gemma-based explanation generation
├── models/                # Model weights directory
└── outputs/               # Grad-CAM output directory
```

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd VeritasAI
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download model weights**

   Place the trained model file at:
   ```
   models/veritas_xception_v2_finetuned.keras
   ```

5. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

6. **Open in browser**

   Navigate to `http://localhost:8501`

### Streamlit Cloud Deployment

1. **Fork/Upload to GitHub**
   - Push the code to a GitHub repository

2. **Connect to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select the repository

3. **Configure Secrets (Optional)**

   For LLM explanations, add Hugging Face token:
   ```toml
   # .streamlit/secrets.toml
   HF_TOKEN = "your_huggingface_token"
   ```

4. **Deploy**
   - Click "Deploy" and wait for the build

## Backend Integration

The frontend communicates with the backend through the `app.analyze_and_explain()` function:

```python
from app import analyze_and_explain

result = analyze_and_explain(image_path)
# Returns: {
#     "prediction": "Real" | "Fake",
#     "confidence": 87.5,
#     "model_version": "Veritas AI v2",
#     "heatmap_path": "outputs/image_gradcam.jpg",
#     "limitations": [...],
#     "explanation": "AI-generated explanation..."
# }
```

## Model Requirements

### Required Files

- **Model**: `models/veritas_xception_v2_finetuned.keras`
  - Xception-based deepfake detection model
  - Input size: 299x299 pixels
  - Output: Binary classification (Real/Fake)

### Optional (for LLM explanations)

- **Hugging Face Token**: Required to download Google Gemma model
- **GPU**: Recommended for faster inference

## API Reference

### `app.analyze_and_explain(image_path)`

Main entry point for image analysis.

**Parameters:**
- `image_path` (str): Path to the image file

**Returns:**
- `dict`: Analysis results containing:
  - `prediction`: "Real" or "Fake"
  - `confidence`: Confidence score (0-100)
  - `model_version`: Model version string
  - `heatmap_path`: Path to Grad-CAM visualization
  - `limitations`: List of known limitations
  - `explanation`: AI-generated explanation (if LLM available)

## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Deep Learning | TensorFlow / Keras |
| Model Architecture | Xception |
| Explainability | Grad-CAM |
| LLM | Google Gemma-3-1B |
| Computer Vision | OpenCV |

## Known Limitations

- Limited cross-dataset generalization
- Predictions should not be treated as definitive evidence
- Requires 299x299 pixel input images
- LLM explanations require Hugging Face authentication

## Development

### Project Structure

```
├── app.py              # Backend API
├── streamlit_app.py    # Frontend application
├── module/
│   ├── detector.py     # Detection logic
│   ├── gradcam.py      # Grad-CAM implementation
│   └── llm.py          # Explanation generation
├── requirements.txt    # Dependencies
└── README.md          # Documentation
```

### Adding Features

1. **Backend modifications**: Edit files in `module/`
2. **Frontend modifications**: Edit `streamlit_app.py`
3. **Styling**: Update CSS in `streamlit_app.py`

## Troubleshooting

### Model Not Found

```
FileNotFoundError: Model not found at models/veritas_xception_v2_finetuned.keras
```

**Solution**: Ensure the model file is placed in the `models/` directory.

### LLM Not Loading

```
⚠️  Could not load LLM: ...
```

**Solution**: The app will use fallback explanations. To enable LLM:
1. Set `HF_TOKEN` environment variable
2. Ensure `transformers` and `torch` are installed

### Memory Issues

**Solution**: Reduce batch size or use CPU-only inference by setting:
```bash
export CUDA_VISIBLE_DEVICES=""
```

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Xception architecture by Francois Chollet
- Grad-CAM implementation based on original paper
- Google Gemma model by Google DeepMind

---

**Veritas AI** - Illuminating Truth in the Age of Synthetic Media
