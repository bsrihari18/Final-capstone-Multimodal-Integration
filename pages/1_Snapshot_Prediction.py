import streamlit as st
from streamlit_webrtc import webrtc_streamer

from utils.face_detection import get_current_face_prediction
from utils.fusion import fuse_emotions
from utils.model_loader import missing_models
from utils.speech_recognition import recognize_speech_from_audio
from utils.text_prediction import predict_text_emotion
from utils.webcam import EmotionProcessor

st.set_page_config(
    page_title="Snapshot Prediction",
    page_icon="📸",
    layout="wide",
)

if missing_models():
    st.error("Model files are missing. Return to the home page for details.")
    st.stop()

st.title("📸 Snapshot Emotion Prediction")
st.caption("Capture face emotion live and record one speech sample for instant fusion.")

left, right = st.columns([2, 1])

with left:
    st.subheader("📷 Facial Emotion Recognition")
    webrtc_streamer(
        key="snapshot-emotion",
        video_processor_factory=EmotionProcessor,
        media_stream_constraints={"video": True, "audio": False},
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    )

with right:
    st.subheader("🎤 Speech Emotion Recognition")
    st.caption("Use your browser microphone — works on Streamlit Cloud.")

    audio = st.audio_input("Record speech", key="snapshot-audio")

    text_input = st.text_area(
        "Or type what was said (fallback if mic fails)",
        height=80,
        placeholder="Optional text fallback…",
    )

    if st.button("Analyze Speech", use_container_width=True, type="primary"):
        text = None

        if audio is not None:
            with st.spinner("Transcribing audio…"):
                text = recognize_speech_from_audio(audio.getvalue())

        if not text and text_input.strip():
            text = text_input.strip()

        if not text:
            st.error("No speech detected. Record audio or enter text manually.")
        else:
            st.success("Speech captured")
            st.text_area("Recognized Speech", value=text, height=100, disabled=True)

            svc, rf, xgb, final_text = predict_text_emotion(text)
            face_emotion, _ = get_current_face_prediction()
            final_emotion = fuse_emotions(face_emotion, final_text)

            st.divider()
            st.subheader("Prediction Results")

            c1, c2 = st.columns(2)
            with c1:
                st.write("**SVC**")
                st.success(svc)
                st.write("**Random Forest**")
                st.success(rf)
            with c2:
                st.write("**XGBoost**")
                st.success(xgb)
                st.write("**Final Text Emotion**")
                st.success(final_text)

            st.divider()
            st.subheader("🧠 Multimodal Emotion")
            st.write(f"😀 **Face Emotion:** {face_emotion}")
            st.write(f"💬 **Text Emotion:** {final_text}")
            st.success(f"🎯 **Final Emotion:** {final_emotion}")

with st.sidebar:
    st.markdown("### Tips")
    st.markdown(
        """
        1. Allow camera access when prompted
        2. Position your face in the webcam frame
        3. Record a short, clear speech sample
        4. Review fused emotion results
        """
    )
