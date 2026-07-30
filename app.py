import streamlit as st
from streamlit_webrtc import webrtc_streamer

from utils.webcam import EmotionProcessor
from utils.speech_recognition import recognize_speech
from utils.text_prediction import predict_text_emotion
from utils.face_detection import get_current_face_prediction
from utils.fusion import fuse_emotions

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Multimodal Emotion Recognition",
    page_icon="😊",
    layout="wide"
)

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("😊 Multimodal Emotion Recognition System")
st.markdown("---")

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.title("Project Information")

st.sidebar.markdown("### Models Used")

st.sidebar.success("✅ CNN (FER)")
st.sidebar.success("✅ SVC")
st.sidebar.success("✅ Random Forest")
st.sidebar.success("✅ XGBoost")

st.sidebar.markdown("---")
st.sidebar.info("System Ready")

# --------------------------------------------------
# Layout
# --------------------------------------------------
left, right = st.columns([2, 1])

# ==================================================
# Webcam Section
# ==================================================
with left:

    st.subheader("📷 Facial Emotion Recognition")

    webrtc_streamer(
        key="emotion",
        video_processor_factory=EmotionProcessor,
        media_stream_constraints={
            "video": True,
            "audio": False
        }
    )

# ==================================================
# Speech Section
# ==================================================
with right:

    st.subheader("🎤 Speech Emotion Recognition")

    if st.button("🎙 Start Recording", use_container_width=True):

        with st.spinner("Listening..."):

            text = recognize_speech()

        if text:

            st.success("✅ Speech Recognized")

            st.text_area(
                "Recognized Speech",
                value=text,
                height=120
            )

            svc, rf, xgb, final_text = predict_text_emotion(text)

            # Get latest face prediction
            face_emotion, face_confidence = get_current_face_prediction()

            # Fuse emotions
            final_emotion = fuse_emotions(
                face_emotion,
                final_text
            )

            st.markdown("---")

            st.subheader("Prediction Results")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**SVC**")
                st.success(svc)

                st.write("**Random Forest**")
                st.success(rf)

            with col2:
                st.write("**XGBoost**")
                st.success(xgb)

                st.write("**Final Text Emotion**")
                st.success(final_text)

            st.markdown("---")

            st.subheader("🧠 Multimodal Emotion")

            st.write(f"😀 **Face Emotion:** {face_emotion}")
            st.write(f"💬 **Text Emotion:** {final_text}")

            st.success(f"🎯 Final Emotion: {final_emotion}")

        else:
            st.error("❌ Could not recognize speech.")