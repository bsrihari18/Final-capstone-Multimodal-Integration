from datetime import timedelta

import pandas as pd
import streamlit as st
from streamlit_webrtc import webrtc_streamer

from utils.csv_logger import CSVLogger
from utils.model_loader import missing_models
from utils.session_manager import SessionManager
from utils.webcam import EmotionProcessor

st.set_page_config(
    page_title="Continuous Monitoring",
    page_icon="📈",
    layout="wide",
)

if missing_models():
    st.error("Model files are missing. Return to the home page for details.")
    st.stop()

st.title("📈 Continuous Multimodal Emotion Monitoring")
st.caption(
    "Face emotion is sampled continuously. Submit speech samples during each "
    "30-second window; results are fused automatically."
)

if "session" not in st.session_state:
    st.session_state.session = SessionManager()
    st.session_state.session.start()

if "last_processed_audio" not in st.session_state:
    st.session_state.last_processed_audio = None

session = st.session_state.session

left, right = st.columns([2, 1])

with left:
    st.subheader("📷 Live Webcam")
    webrtc_streamer(
        key="monitoring-camera",
        video_processor_factory=EmotionProcessor,
        media_stream_constraints={"video": True, "audio": False},
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    )

with right:
    st.subheader("🎤 Speech Samples")
    st.caption(
        f"Submit short recordings during each window (target: every "
        f"{session.speech_service.interval}s while listening is on)."
    )

    if session.speech_service.enabled:
        st.success("Speech listener active")
    else:
        st.warning("Speech listener paused")

    audio = st.audio_input("Record speech sample", key="monitoring-audio")

    if audio is not None:
        audio_id = hash(audio.getvalue())
        if st.session_state.last_processed_audio != audio_id:
            with st.spinner("Processing speech…"):
                ok = session.speech_service.process_audio(audio.getvalue())
            st.session_state.last_processed_audio = audio_id

            if ok:
                st.success("Speech sample added to the current window.")
            elif session.speech_service.last_error:
                st.warning(session.speech_service.last_error)


@st.fragment(run_every=timedelta(seconds=1))
def live_status_panel():
    emotion, confidence = session.collect_face_prediction()
    latest_summary = session.update()

    st.subheader("📊 Live Status")
    st.metric("Current Face Emotion", emotion)

    if confidence > 0:
        st.metric("Face Confidence", f"{confidence * 100:.1f}%")

    st.metric("Time Until Fusion", f"{session.remaining_time()} sec")
    st.metric("Frames Collected", session.frame_count())

    speech_summary = session.speech_summary()
    st.metric("Speech Emotion", speech_summary["emotion"])
    st.metric("Speech Samples", speech_summary["count"])

    if speech_summary["count"] > 0:
        st.write("**Recent Speech**")
        for text in speech_summary["texts"][-3:]:
            st.write(f"• {text}")

    if latest_summary:
        st.divider()
        st.success("✅ 30-Second Multimodal Summary")
        st.write(
            f"**Face:** {latest_summary['face_emotion']} "
            f"({latest_summary['face_confidence']:.1f}%)"
        )
        st.write(
            f"**Speech:** {latest_summary['speech_emotion']} "
            f"({latest_summary['speech_count']} samples)"
        )
        st.success(f"**Final Emotion:** {latest_summary['final_emotion']}")


with right:
    live_status_panel()

st.divider()
st.subheader("📈 Analytics Dashboard")

analytics = session.analytics()
history = session.history()

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Total Windows", analytics["total_windows"])
with c2:
    st.metric("Dominant Emotion", analytics["dominant_emotion"])
with c3:
    st.metric("History Rows", len(history))

if analytics["total_windows"] > 0:
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("**Final Emotion Frequency**")
        final_df = pd.DataFrame(
            list(analytics["emotion_counts"].items()),
            columns=["Emotion", "Count"],
        )
        st.bar_chart(final_df.set_index("Emotion"))

    with chart_col2:
        st.write("**Face vs Speech Emotions**")
        face_df = pd.DataFrame(
            list(analytics["face_counts"].items()),
            columns=["Face Emotion", "Count"],
        )
        speech_df = pd.DataFrame(
            list(analytics["speech_counts"].items()),
            columns=["Speech Emotion", "Count"],
        )
        st.write("Face")
        st.bar_chart(face_df.set_index("Face Emotion"))
        st.write("Speech")
        st.bar_chart(speech_df.set_index("Speech Emotion"))
else:
    st.info("Analytics appear after the first 30-second fusion window completes.")

st.divider()
st.subheader("🕒 Emotion History")

if history:
    history_df = pd.DataFrame([
        {
            "Time": row["time"],
            "Face": row["face_emotion"],
            "Face Conf.": row["face_confidence"],
            "Frames": row["frames"],
            "Speech": row["speech_emotion"],
            "Samples": row["speech_count"],
            "Final": row["final_emotion"],
        }
        for row in history
    ])
    st.dataframe(history_df, use_container_width=True, hide_index=True)

    st.download_button(
        label="Download session CSV",
        data=CSVLogger.export_csv(history),
        file_name="emotion_history.csv",
        mime="text/csv",
        use_container_width=True,
    )
else:
    st.info("No history yet. Keep the webcam running and submit speech samples.")

with st.sidebar:
    st.subheader("Session Controls")

    if st.button("Reset Session", use_container_width=True):
        session.reset()
        st.session_state.last_processed_audio = None
        st.rerun()

    if st.button("Pause Speech Listener", use_container_width=True):
        session.stop()

    if st.button("Resume Speech Listener", use_container_width=True):
        session.start()

    st.divider()
    st.markdown("### How it works")
    st.markdown(
        """
        1. **Webcam** detects face emotion continuously
        2. **You record speech** via browser mic during each window
        3. Every **30 seconds**, face + speech are fused
        4. Export results as **CSV** at any time
        """
    )
