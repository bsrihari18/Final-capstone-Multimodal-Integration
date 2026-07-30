import streamlit as st

from utils.model_loader import missing_models


def render_model_status():
    """Show model readiness banner; returns True when all models are present."""
    missing = missing_models()

    if missing:
        st.error(
            "Required model files are missing. Ensure Git LFS assets are pulled "
            "and the `models/` directory is deployed with the app."
        )
        with st.expander("Missing files"):
            for item in missing:
                st.write(f"- {item}")
        return False

    st.success("All model files found. Select a mode from the sidebar to begin.")
    return True


st.set_page_config(
    page_title="Multimodal Emotion Recognition",
    page_icon="😊",
    layout="wide",
)

st.title("😊 Multimodal Emotion Recognition System")
st.markdown(
    """
    Production-ready Streamlit app for **facial** and **speech-based** emotion recognition
    with multimodal fusion. Optimized for [Streamlit Cloud](https://streamlit.io/cloud)
    using browser webcam and microphone capture.
    """
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Snapshot Prediction")
    st.markdown(
        """
        - Live webcam face emotion detection
        - Record speech from your browser microphone
        - Instant multimodal fusion result
        """
    )
    st.page_link("pages/1_Snapshot_Prediction.py", label="Open Snapshot Mode →")

with col2:
    st.subheader("📈 Continuous Monitoring")
    st.markdown(
        """
        - Continuous face sampling with 30-second fusion windows
        - Submit speech samples during each window
        - Session history, analytics, and CSV export
        """
    )
    st.page_link("pages/2_Continuous_Monitoring.py", label="Open Monitoring Mode →")

st.divider()
st.subheader("System Status")
render_model_status()

with st.sidebar:
    st.markdown("### Models")
    st.markdown("- CNN (FER) — facial emotions")
    st.markdown("- SVC, Random Forest, XGBoost — text emotions")
    st.markdown("---")
    st.caption(
        "Grant camera and microphone permissions when prompted. "
        "Use Chrome or Edge for best WebRTC support."
    )
