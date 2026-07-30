import cv2
import pandas as pd
import streamlit as st

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
    "Capture an image, detect facial emotion, combine with speech every 30 seconds."
)

# ----------------------------------------------------
# Session
# ----------------------------------------------------
if "session" not in st.session_state:
    st.session_state.session = SessionManager()
    st.session_state.session.start()

session = st.session_state.session

# ----------------------------------------------------
# CAMERA INPUT
# ----------------------------------------------------
left, right = st.columns([2, 1])

with left:

    st.subheader("📷 Camera")

    image = st.camera_input("Capture Image")

    if image is not None:

        processed = EmotionProcessor.process(image)

        processed = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)

        st.image(processed, use_container_width=True)

# ----------------------------------------------------
# Face prediction
# ----------------------------------------------------
emotion, confidence = session.collect_face_prediction()

latest_summary = session.update()

# ----------------------------------------------------
# Live status
# ----------------------------------------------------
with right:

    st.subheader("Live Status")

    st.metric("Current Face Emotion", emotion)

    if confidence > 0:

        st.metric(
            "Confidence",
            f"{confidence*100:.2f}%"
        )

    st.metric(
        "Time Remaining",
        f"{session.remaining_time()} sec"
    )

    st.metric(
        "Frames",
        session.frame_count()
    )

    st.divider()

    speech = session.speech_summary()

    st.metric(
        "Speech Emotion",
        speech["emotion"]
    )

    st.metric(
        "Speech Samples",
        speech["count"]
    )

    if speech["count"]:

        st.write("Recent Speech")

        for txt in speech["texts"][-3:]:

            st.write("•", txt)

# ----------------------------------------------------
# Latest Fusion
# ----------------------------------------------------
if latest_summary:

    st.divider()

    st.success("Latest 30 Second Summary")

    st.write(
        f"Face : {latest_summary['face_emotion']}"
    )

    st.write(
        f"Speech : {latest_summary['speech_emotion']}"
    )

    st.success(
        latest_summary["final_emotion"]
    )

# ----------------------------------------------------
# Analytics
# ----------------------------------------------------
st.divider()

analytics = session.analytics()

history = session.history()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Windows",
    analytics["total_windows"]
)

col2.metric(
    "Dominant",
    analytics["dominant_emotion"]
)

col3.metric(
    "CSV",
    "outputs/emotion_history.csv"
)

if analytics["total_windows"]:

    final_df = pd.DataFrame(

        analytics["emotion_counts"].items(),

        columns=["Emotion", "Count"]

    )

    st.bar_chart(
        final_df.set_index("Emotion")
    )

# ----------------------------------------------------
# History
# ----------------------------------------------------
st.divider()

st.subheader("History")

if history:

    df = pd.DataFrame(history)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No history available.")

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------
with st.sidebar:

    st.subheader("Controls")

    if st.button("Reset"):

        session.reset()

        st.rerun()

    if st.button("Stop Speech"):

        session.stop()

    if st.button("Start Speech"):

        session.start()
