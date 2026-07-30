import time

import pandas as pd
import streamlit as st
from streamlit_webrtc import webrtc_streamer

from utils.session_manager import SessionManager
from utils.webcam import EmotionProcessor

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(
    page_title="Continuous Emotion Monitoring",
    page_icon="😊",
    layout="wide",
)

st.title("😊 Continuous Multimodal Emotion Monitoring")
st.caption(
    "Monitors face and speech continuously, fuses every 30 seconds, "
    "and logs results to history and CSV."
)

# ----------------------------------------------------
# Session (single instance)
# ----------------------------------------------------
if "session" not in st.session_state:
    st.session_state.session = SessionManager()
    st.session_state.session.start()

session = st.session_state.session

# ----------------------------------------------------
# Collect face + check 30-second window
# ----------------------------------------------------
emotion, confidence = session.collect_face_prediction()
latest_summary = session.update()

# ----------------------------------------------------
# Main layout: Webcam | Live status
# ----------------------------------------------------
left, right = st.columns([2, 1])

with left:
    st.subheader("📷 Live Webcam")

    webrtc_streamer(
        key="camera",
        video_processor_factory=EmotionProcessor,
        media_stream_constraints={
            "video": True,
            "audio": False,
        },
    )

with right:
    st.subheader("📊 Live Status")

    st.metric("Current Face Emotion", emotion)

    if confidence > 0:
        st.metric("Face Confidence", f"{confidence * 100:.1f}%")

    st.metric("Time Until Fusion", f"{session.remaining_time()} sec")
    st.metric("Frames Collected", session.frame_count())

    st.divider()
    st.subheader("🎤 Live Speech")

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

        st.write(f"**Face:** {latest_summary['face_emotion']} "
                 f"({latest_summary['face_confidence']:.1f}%)")
        st.write(f"**Speech:** {latest_summary['speech_emotion']} "
                 f"({latest_summary['speech_count']} samples)")
        st.success(f"**Final Emotion:** {latest_summary['final_emotion']}")

# ----------------------------------------------------
# Dashboard: analytics + history
# ----------------------------------------------------
st.divider()
st.subheader("📈 Analytics Dashboard")

analytics = session.analytics()
history = session.history()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Windows", analytics["total_windows"])

with col2:
    st.metric("Dominant Emotion", analytics["dominant_emotion"])

with col3:
    st.metric("CSV Log", "outputs/emotion_history.csv")

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
    st.info("Analytics will appear after the first 30-second fusion window completes.")

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
else:
    st.info("No history yet. Keep the webcam running — summaries are saved every 30 seconds.")

# ----------------------------------------------------
# Sidebar controls
# ----------------------------------------------------
with st.sidebar:
    st.subheader("Session Controls")

    if st.button("Reset Session", use_container_width=True):
        session.reset()
        st.rerun()

    if st.button("Stop Speech Listener", use_container_width=True):
        session.stop()

    if st.button("Start Speech Listener", use_container_width=True):
        session.start()

    st.divider()
    st.markdown("### How it works")
    st.markdown(
        """
        1. **Webcam** detects face emotion continuously
        2. **Microphone** records speech every 5 seconds
        3. Every **30 seconds**, face + speech are fused
        4. Results are saved to **history** and **CSV**
        """
    )

# ----------------------------------------------------
# Auto-refresh for live timer and buffer updates
# ----------------------------------------------------
time.sleep(1)
st.rerun()
