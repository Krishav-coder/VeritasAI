"""
Veritas AI - Deepfake Detection Platform
Production-grade Streamlit application
"""

from __future__ import annotations

from datetime import datetime
import hashlib
import sys
import time
from pathlib import Path
from typing import Any

import streamlit as st


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Veritas AI | Deepfake Detection",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def inject_custom_css() -> None:
    """Apply Veritas AI's dark glass interface without altering app behavior."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

        :root {
            --veritas-bg: #080a0f;
            --veritas-surface: rgba(18, 22, 34, 0.60);
            --veritas-surface-strong: rgba(20, 25, 39, 0.78);
            --veritas-border: rgba(255, 255, 255, 0.08);
            --veritas-text: #f3f4f6;
            --veritas-muted: #9ca3af;
            --veritas-cyan: #06b6d4;
            --veritas-purple: #8b5cf6;
        }

        .stApp,
        [data-testid="stAppViewContainer"] {
            color: var(--veritas-text);
            background:
                radial-gradient(circle at 8% 4%, rgba(139, 92, 246, 0.08), transparent 28rem),
                radial-gradient(circle at 92% 12%, rgba(6, 182, 212, 0.08), transparent 25rem),
                var(--veritas-bg);
            font-family: 'Inter', sans-serif;
        }

        [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer {
            visibility: hidden;
        }

        .block-container {
            max-width: 1180px;
            padding: 2.5rem 1.5rem 3rem;
        }

        h1, h2, h3, h4, h5, h6,
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3 {
            color: var(--veritas-text) !important;
            font-family: 'Space Grotesk', 'Inter', sans-serif;
            letter-spacing: -0.035em;
        }

        h1, [data-testid="stMarkdownContainer"] h1 {
            font-size: clamp(2.5rem, 6vw, 4.5rem) !important;
            line-height: 1.02;
            font-weight: 700;
            background: linear-gradient(115deg, #ffffff 20%, #c4b5fd 57%, #67e8f9 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        p, li, label, [data-testid="stCaptionContainer"],
        [data-testid="stMarkdownContainer"] p {
            color: var(--veritas-muted) !important;
        }

        [data-testid="stCaptionContainer"] {
            font-size: 0.83rem;
            letter-spacing: 0.01em;
        }

        code, pre, .pipeline-spec, [data-testid="stMetricLabel"] {
            font-family: 'JetBrains Mono', monospace;
        }

        hr, [data-testid="stDivider"] {
            border-color: rgba(255, 255, 255, 0.07) !important;
            margin: 1.75rem 0 !important;
        }

        /* Shared glass cards: only Streamlit's explicit bordered containers become cards. */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--veritas-surface);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid var(--veritas-border);
            border-radius: 12px;
            box-shadow: 0 12px 34px rgba(0, 0, 0, 0.16);
            overflow: hidden;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: 0.15rem 0.15rem !important;
        }

        /* Keep nested content clean instead of turning every block into another box. */
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlockBorderWrapper"] {
            background: transparent;
            backdrop-filter: none;
            border: 0;
            border-radius: 0;
            box-shadow: none;
        }

        section[data-testid="stFileUploader"] {
            border: 0 !important;
            background: transparent !important;
        }

        section[data-testid="stFileUploader"] > div,
        section[data-testid="stFileUploaderDropzone"] {
            min-height: 172px;
            background: rgba(18, 22, 34, 0.50) !important;
            border: 1px dashed rgba(6, 182, 212, 0.30) !important;
            border-radius: 12px !important;
            transition: border-color 180ms ease, background 180ms ease, box-shadow 180ms ease;
        }

        section[data-testid="stFileUploader"] > div:hover,
        section[data-testid="stFileUploaderDropzone"]:hover {
            background: rgba(6, 182, 212, 0.06) !important;
            border-color: rgba(6, 182, 212, 0.82) !important;
            box-shadow: 0 0 0 4px rgba(6, 182, 212, 0.07), 0 0 28px rgba(6, 182, 212, 0.10);
        }

        section[data-testid="stFileUploader"] small,
        section[data-testid="stFileUploader"] span,
        section[data-testid="stFileUploader"] p {
            color: var(--veritas-muted) !important;
        }

        section[data-testid="stFileUploader"] button,
        .stDownloadButton > button {
            color: #cffafe !important;
            background: rgba(6, 182, 212, 0.10) !important;
            border: 1px solid rgba(6, 182, 212, 0.32) !important;
            border-radius: 8px !important;
            font-weight: 600;
        }

        .stButton > button {
            min-height: 2.85rem;
            color: #fff !important;
            background: linear-gradient(135deg, #7c3aed 0%, var(--veritas-purple) 50%, #a855f7 100%) !important;
            border: 1px solid rgba(196, 181, 253, 0.36) !important;
            border-radius: 9px !important;
            box-shadow: 0 12px 28px rgba(139, 92, 246, 0.22);
            font-weight: 700;
            transition: transform 160ms ease, box-shadow 160ms ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 16px 34px rgba(139, 92, 246, 0.30);
        }

        div[data-testid="stAlert"] {
            gap: 0.5rem;
            padding: 0.65rem 0.8rem !important;
            background: rgba(18, 22, 34, 0.58) !important;
            border: 1px solid rgba(6, 182, 212, 0.20) !important;
            border-radius: 9px !important;
            color: var(--veritas-muted) !important;
            font-size: 0.875rem !important;
            box-shadow: none !important;
        }

        div[data-testid="stAlert"] p,
        div[data-testid="stAlert"] div {
            color: var(--veritas-muted) !important;
            font-size: 0.875rem !important;
        }

        div[data-testid="stAlert"] svg { color: var(--veritas-cyan) !important; }
        div[data-testid="stAlert"][data-baseweb="notification"] { border-color: rgba(245, 158, 11, 0.25) !important; }

        div[data-testid="stMetric"] {
            padding: 0.8rem 0 !important;
            background: transparent !important;
            border: 0 !important;
        }

        [data-testid="stMetricLabel"] {
            color: var(--veritas-muted) !important;
            font-size: 0.68rem !important;
            font-weight: 500;
            letter-spacing: 0.11em;
            text-transform: uppercase;
        }

        [data-testid="stMetricValue"] {
            color: var(--veritas-text) !important;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.55rem !important;
        }

        [data-testid="stExpander"] {
            background: rgba(8, 10, 15, 0.32) !important;
            border: 1px solid var(--veritas-border) !important;
            border-radius: 9px !important;
        }

        [data-testid="stImage"] img { border-radius: 10px; }

        .veritas-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            margin-bottom: 0.75rem;
            color: #a5f3fc;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.70rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .veritas-eyebrow::before {
            width: 0.45rem;
            height: 0.45rem;
            border-radius: 50%;
            background: var(--veritas-cyan);
            box-shadow: 0 0 11px var(--veritas-cyan);
            content: '';
        }

        .pipeline-panel, .capability-card {
            background: var(--veritas-surface);
            border: 1px solid var(--veritas-border);
            border-radius: 12px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }

        .pipeline-panel { padding: 1.1rem 1.2rem; }
        .pipeline-title {
            margin-bottom: 0.8rem;
            color: var(--veritas-muted);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }

        .pipeline-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.75rem;
            padding: 0.55rem 0;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
        }

        .pipeline-item:first-of-type { border-top: 0; }
        .pipeline-label { color: #9ca3af; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; }
        .pipeline-pill {
            padding: 0.23rem 0.55rem;
            border: 1px solid rgba(6, 182, 212, 0.24);
            border-radius: 999px;
            color: #a5f3fc;
            background: rgba(6, 182, 212, 0.08);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.70rem;
        }

        .capability-card { min-height: 168px; padding: 1.25rem; }
        .capability-icon {
            display: grid;
            width: 2.25rem;
            height: 2.25rem;
            margin-bottom: 0.85rem;
            place-items: center;
            border: 1px solid rgba(139, 92, 246, 0.30);
            border-radius: 8px;
            color: #c4b5fd;
            background: rgba(139, 92, 246, 0.10);
        }
        .capability-card h3 { margin: 0 0 0.4rem; font-size: 1.05rem; }
        .capability-card p { margin: 0; font-size: 0.88rem; line-height: 1.65; }

        @media (max-width: 768px) {
            .block-container { padding: 1.5rem 1rem 2rem; }
            h1, [data-testid="stMarkdownContainer"] h1 { font-size: 2.7rem !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# Style setup must run directly after Streamlit page configuration.
inject_custom_css()


# =============================================================================
# PATH SETUP
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent
MODULE_PATH = BASE_DIR / "module"
TEMP_DIR = BASE_DIR / "temp"

if str(MODULE_PATH) not in sys.path:
    sys.path.insert(0, str(MODULE_PATH))


# Backend entry point must remain intact.
from app import analyze_and_explain


# =============================================================================
# CONSTANTS
# =============================================================================

ALLOWED_SUFFIXES = {".png", ".jpg", ".jpeg"}

UPLOAD_SIGNATURE_KEY = "veritas_upload_signature"
UPLOAD_PATH_KEY = "veritas_upload_path"
UPLOAD_NAME_KEY = "veritas_upload_name"
UPLOAD_SIZE_KEY = "veritas_upload_size"
ANALYSIS_RESULT_KEY = "veritas_analysis_result"
ANALYSIS_ERROR_KEY = "veritas_analysis_error"
RESULT_ANIMATE_KEY = "veritas_result_animate"
ANALYSIS_TIMESTAMP_KEY = "veritas_analysis_timestamp"


# =============================================================================
# SESSION STATE
# =============================================================================

def initialize_state() -> None:
    """Initialize Streamlit session state keys used by the app."""
    defaults: dict[str, Any] = {
        UPLOAD_SIGNATURE_KEY: None,
        UPLOAD_PATH_KEY: None,
        UPLOAD_NAME_KEY: None,
        UPLOAD_SIZE_KEY: 0,
        ANALYSIS_RESULT_KEY: None,
        ANALYSIS_ERROR_KEY: None,
        RESULT_ANIMATE_KEY: False,
        ANALYSIS_TIMESTAMP_KEY: None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_analysis_state() -> None:
    """Clear any prior analysis result and related messages."""
    st.session_state[ANALYSIS_RESULT_KEY] = None
    st.session_state[ANALYSIS_ERROR_KEY] = None
    st.session_state[RESULT_ANIMATE_KEY] = False
    st.session_state[ANALYSIS_TIMESTAMP_KEY] = None


# =============================================================================
# HELPERS
# =============================================================================

def human_readable_size(size_bytes: int) -> str:
    """Format a file size into a friendly display string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.1f} MB"


def clamp_confidence(value: Any) -> float:
    """Coerce confidence into a valid percentage range."""
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        confidence = 0.0
    return max(0.0, min(100.0, confidence))


def save_uploaded_file(uploaded_file: Any) -> tuple[str, str, int, str]:
    """Persist an uploaded file to disk and return metadata."""
    file_bytes = uploaded_file.getvalue()
    signature = hashlib.sha256(file_bytes).hexdigest()

    original_name = Path(uploaded_file.name).name
    suffix = Path(original_name).suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        suffix = ".png"

    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    saved_path = TEMP_DIR / f"upload_{signature[:16]}{suffix}"

    if (not saved_path.exists()) or saved_path.stat().st_size != len(file_bytes):
        saved_path.write_bytes(file_bytes)

    return str(saved_path), original_name, len(file_bytes), signature


def animate_progress(progress_bar: Any, target: int) -> None:
    """Animate a progress bar from 0 to the target value."""
    target = max(0, min(100, target))
    if target == 0:
        progress_bar.progress(0, text="Confidence score: 0%")
        return

    step = max(1, target // 10)
    current = 0
    while current < target:
        progress_bar.progress(current, text=f"Confidence score: {current}%")
        current = min(target, current + step)
        time.sleep(0.01)

    progress_bar.progress(target, text=f"Confidence score: {target}%")


def get_heatmap_bytes(heatmap_path: str | None) -> tuple[bytes | None, str | None]:
    """Read a Grad-CAM image from disk if it exists."""
    if not heatmap_path:
        return None, None

    path = Path(heatmap_path)
    if not path.exists():
        return None, None

    try:
        return path.read_bytes(), path.name
    except OSError:
        return None, None


def get_verdict_theme(prediction: str) -> dict[str, Any]:
    """Return UI labels for a prediction value."""
    is_real = prediction.strip().lower() == "real"
    return {
        "is_real": is_real,
        "headline": "REAL IMAGE" if is_real else "DEEPFAKE DETECTED",
        "lead_icon": "🟢" if is_real else "🔴",
        "badge_label": "Real" if is_real else "Fake",
        "badge_color": "green" if is_real else "red",
    }


def get_confidence_theme(confidence: float) -> tuple[str, str]:
    """Map a confidence value to a summary label and badge color."""
    if confidence >= 85.0:
        return "High Confidence", "green"
    if confidence >= 65.0:
        return "Moderate Confidence", "yellow"
    return "Low Confidence", "red"


def format_timestamp(value: str | None = None) -> str:
    """Format a timestamp for display."""
    if value:
        return value
    return datetime.now().strftime("%b %d, %Y • %I:%M %p")


# =============================================================================
# RENDERING
# =============================================================================

def render_hero() -> None:
    """Render the brand hero section."""
    left_col, right_col = st.columns([1.55, 0.95], gap="large")

    with left_col:
        st.markdown('<div class="veritas-eyebrow">AI-Powered Detection</div>', unsafe_allow_html=True)
        st.title("Veritas AI")
        st.subheader("Forensic deepfake detection, made legible.")
        st.write(
            "Veritas AI combines a finetuned Xception detector, Grad-CAM visual evidence, "
            "and Gemma-assisted explanations into one forensic workflow."
        )
        st.caption("Built for responsible review, not automated judgment.")

    with right_col:
        st.markdown(
            """
            <section class="pipeline-panel" aria-label="Pipeline overview">
                <div class="pipeline-title">Pipeline overview</div>
                <div class="pipeline-item"><span class="pipeline-label">Detector</span><span class="pipeline-pill">Xception</span></div>
                <div class="pipeline-item"><span class="pipeline-label">Explainability</span><span class="pipeline-pill">Grad-CAM</span></div>
                <div class="pipeline-item"><span class="pipeline-label">LLM</span><span class="pipeline-pill">Gemma</span></div>
            </section>
            """,
            unsafe_allow_html=True,
        )


def render_features() -> None:
    """Render the platform feature cards."""
    st.subheader("Core Capabilities")

    col1, col2, col3 = st.columns(3, gap="medium")

    cards = [
        ("Deep Learning", "Xception-based architecture trained for deepfake classification with production-oriented inference.", "◈"),
        ("Explainable AI", "Grad-CAM visualizations reveal where the model focuses when deciding whether an image is real or fake.", "⌁"),
        ("AI Explanations", "Natural-language analysis generated by Gemma to translate detector output into readable insight.", "✦"),
    ]

    for column, card in zip((col1, col2, col3), cards):
        with column:
            title, description, icon = card
            st.markdown(
                f'''<article class="capability-card">
                    <span class="capability-icon" aria-hidden="true">{icon}</span>
                    <h3>{title}</h3><p>{description}</p>
                </article>''',
                unsafe_allow_html=True,
            )


def render_upload() -> Any | None:
    """Render the upload card and return the uploaded file, if any."""
    with st.container(border=True):
        st.subheader("Upload Image")
        st.caption("Choose a PNG, JPG, or JPEG to inspect for potential manipulation.")
        uploaded_file = st.file_uploader(
            "Upload an image",
            type=["png", "jpg", "jpeg"],
            label_visibility="collapsed",
        )
        st.info("Your file stays in this workspace while it is being analyzed.")

    return uploaded_file


def render_preview(image_path: str, file_name: str, file_size_bytes: int) -> None:
    """Render the uploaded image preview."""
    with st.container(border=True):
        st.subheader("Preview")
        st.caption(f"{file_name} • {human_readable_size(file_size_bytes)}")
        _, center_col, _ = st.columns([1.15, 1.0, 1.15], gap="small")
        with center_col:
            if Path(image_path).exists():
                st.image(image_path, use_container_width=True)
            else:
                st.warning("The uploaded image could not be previewed.")



def render_analysis_button() -> bool:
    """Render the analyze button."""
    with st.container(border=True):
        st.caption("Generate the detector verdict, Grad-CAM map, and explanation.")
        _, col_center, _ = st.columns([1, 1.4, 1])
        with col_center:
            return st.button(
                "Analyze Image",
                icon="🔍",
                type="primary",
                use_container_width=True,
            )


def render_loading() -> Any:
    """Render and return the loading placeholder."""
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        with st.container(border=True):
            st.status("Analyzing image...", state="running", expanded=False)
            st.caption(
                "Running detector inference, Grad-CAM generation, and explanation synthesis."
            )
    return loading_placeholder


def render_results(result: dict[str, Any], original_image_path: str) -> None:
    """Render the complete analysis dashboard."""
    prediction = str(result.get("prediction", "Unknown"))
    confidence = clamp_confidence(result.get("confidence", 0.0))
    model_version = str(result.get("model_version", "Veritas AI"))
    explanation = str(result.get("explanation", "") or "").strip()
    limitations = [
        str(item).strip()
        for item in (result.get("limitations") or [])
        if str(item).strip()
    ]
    heatmap_path = result.get("heatmap_path")
    heatmap_path_obj = Path(str(heatmap_path)) if heatmap_path else None
    heatmap_bytes, heatmap_name = get_heatmap_bytes(
        str(heatmap_path) if heatmap_path else None
    )
    verdict_theme = get_verdict_theme(prediction)
    confidence_label, confidence_color = get_confidence_theme(confidence)
    processed_at = format_timestamp(
        str(st.session_state.get(ANALYSIS_TIMESTAMP_KEY) or "")
    )
    is_real = bool(verdict_theme["is_real"])

    st.subheader("Analysis Dashboard")
    st.caption("Prediction first, then confidence, followed by the visual evidence and explanation.")

    with st.container(border=True):
        summary_col_1, summary_col_2 = st.columns([1.7, 1], gap="medium")

        with summary_col_1:
            st.markdown("#### Prediction")
            st.markdown(f"### {verdict_theme['lead_icon']} {verdict_theme['headline']}")
            if is_real:
                st.success("The detector favors a real image.")
            else:
                st.error("The detector favors a fake or manipulated image.")
            st.caption("Classifier verdict from the backend model.")

            status_badge_col, verdict_badge_col = st.columns(2, gap="small")
            with status_badge_col:
                st.badge("Analysis Complete", icon="✅", color="green")
            with verdict_badge_col:
                st.badge(
                    verdict_theme["badge_label"],
                    icon=verdict_theme["lead_icon"],
                    color=verdict_theme["badge_color"],
                )
            st.caption(f"Processed {processed_at}")

        with summary_col_2:
            st.markdown("#### Confidence")
            st.metric("Confidence", f"{confidence:.1f}%")

            progress_bar = st.progress(0, text="Confidence score: 0%")
            if st.session_state.get(RESULT_ANIMATE_KEY, False):
                animate_progress(progress_bar, int(round(confidence)))
                st.session_state[RESULT_ANIMATE_KEY] = False
            else:
                progress_bar.progress(
                    int(round(confidence)),
                    text=f"Confidence score: {confidence:.1f}%",
                )
            st.badge(confidence_label, icon="📈", color=confidence_color)
            st.caption("The confidence score is a model estimate, not proof.")

        meta_col_1, meta_col_2 = st.columns(2, gap="small")
        with meta_col_1:
            st.metric("Model Version", model_version)
        with meta_col_2:
            st.metric("Processing Status", "Analysis Complete")

    st.subheader("Visual Analysis")

    with st.container(border=True):
        st.caption("Original image and Grad-CAM are presented together for direct comparison.")
        image_col_1, image_col_2 = st.columns(2, gap="medium")

        with image_col_1:
            st.markdown("##### Original Image")
            if Path(original_image_path).exists():
                st.image(original_image_path, caption="Uploaded input", use_container_width=True)
            else:
                st.warning("The original image is no longer available.")

        with image_col_2:
            st.markdown("##### Grad-CAM Heatmap")
            if heatmap_path_obj and heatmap_path_obj.exists():
                st.image(str(heatmap_path_obj), caption="Model attention map", use_container_width=True)
            else:
                st.warning("Grad-CAM visualization is not available for this result.")

        if heatmap_bytes and heatmap_name:
            st.download_button(
                "Download Grad-CAM",
                data=heatmap_bytes,
                file_name=heatmap_name,
                mime="image/jpeg",
                icon="⬇️",
                type="secondary",
            )

    with st.container(border=True):
        st.markdown("#### 🤖 AI Explanation")
        st.caption("Readable summary generated from the detector output and visual context.")
        with st.expander("Open explanation", expanded=True):
            if explanation:
                st.write(explanation)
            else:
                st.info("No explanation text was returned by the backend.")

    with st.container(border=True):
        st.warning("Known Limitations")
        st.caption("These caveats should accompany every result.")
        if limitations:
            for item in limitations:
                st.write(f"• {item}")
        else:
            st.info("No limitations were returned by the backend.")


def render_footer() -> None:
    """Render the page footer."""
    st.divider()
    st.caption(
        "Veritas AI v2 • Xception detector • Grad-CAM explainability • Gemma-assisted explanations"
    )
    st.caption("Built for responsible review and human oversight.")


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main() -> None:
    """Main application entry point."""
    initialize_state()

    render_hero()
    st.divider()
    render_features()
    st.divider()

    uploaded_file = render_upload()

    image_path = None
    image_name = None
    image_size = 0

    if uploaded_file is not None:
        try:
            saved_path, original_name, size_bytes, signature = save_uploaded_file(
                uploaded_file
            )
        except Exception:
            reset_analysis_state()
            st.error(
                "We couldn't prepare the uploaded image. Please try a different PNG, JPG, or JPEG file."
            )
        else:
            if st.session_state.get(UPLOAD_SIGNATURE_KEY) != signature:
                st.session_state[UPLOAD_SIGNATURE_KEY] = signature
                st.session_state[UPLOAD_PATH_KEY] = saved_path
                st.session_state[UPLOAD_NAME_KEY] = original_name
                st.session_state[UPLOAD_SIZE_KEY] = size_bytes
                reset_analysis_state()
            else:
                st.session_state[UPLOAD_PATH_KEY] = saved_path
                st.session_state[UPLOAD_NAME_KEY] = original_name
                st.session_state[UPLOAD_SIZE_KEY] = size_bytes

            image_path = saved_path
            image_name = original_name
            image_size = size_bytes

    elif st.session_state.get(UPLOAD_PATH_KEY):
        candidate_path = Path(str(st.session_state[UPLOAD_PATH_KEY]))
        if candidate_path.exists():
            image_path = str(candidate_path)
            image_name = str(st.session_state.get(UPLOAD_NAME_KEY) or candidate_path.name)
            image_size = int(st.session_state.get(UPLOAD_SIZE_KEY) or 0)

    if image_path:
        render_preview(image_path, image_name or Path(image_path).name, image_size)
        analyze_clicked = render_analysis_button()

        if analyze_clicked:
            loading_placeholder = render_loading()
            try:
                st.session_state[ANALYSIS_ERROR_KEY] = None
                analysis_result = analyze_and_explain(image_path)
                st.session_state[ANALYSIS_RESULT_KEY] = analysis_result
                st.session_state[RESULT_ANIMATE_KEY] = True
                st.session_state[ANALYSIS_TIMESTAMP_KEY] = datetime.now().strftime(
                    "%b %d, %Y • %I:%M %p"
                )
            except FileNotFoundError:
                st.session_state[ANALYSIS_RESULT_KEY] = None
                st.session_state[RESULT_ANIMATE_KEY] = False
                st.session_state[ANALYSIS_TIMESTAMP_KEY] = None
                st.session_state[ANALYSIS_ERROR_KEY] = (
                    "The model file could not be found. Please confirm that the trained weights are available in the `models/` directory."
                )
            except ValueError:
                st.session_state[ANALYSIS_RESULT_KEY] = None
                st.session_state[RESULT_ANIMATE_KEY] = False
                st.session_state[ANALYSIS_TIMESTAMP_KEY] = None
                st.session_state[ANALYSIS_ERROR_KEY] = (
                    "The uploaded file could not be processed as an image. Please upload a valid PNG, JPG, or JPEG."
                )
            except Exception as exc:
                print(f"Analysis error: {exc}")
                st.session_state[ANALYSIS_RESULT_KEY] = None
                st.session_state[RESULT_ANIMATE_KEY] = False
                st.session_state[ANALYSIS_TIMESTAMP_KEY] = None
                st.session_state[ANALYSIS_ERROR_KEY] = (
                    "The analysis could not be completed. Please try again in a moment."
                )
            finally:
                loading_placeholder.empty()

        if st.session_state.get(ANALYSIS_ERROR_KEY):
            st.error(str(st.session_state[ANALYSIS_ERROR_KEY]))
            st.info(
                "If this keeps happening, confirm that the backend model and output directories are available."
            )

        if st.session_state.get(ANALYSIS_RESULT_KEY):
            render_results(st.session_state[ANALYSIS_RESULT_KEY], image_path)
    else:
        with st.container(border=True):
            st.info("Upload an image above to unlock the preview and analysis dashboard.")

    st.markdown("<div style='height:64px;'></div>", unsafe_allow_html=True)
    render_footer()


if __name__ == "__main__":
    main()
