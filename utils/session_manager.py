import time

from utils.face_buffer import FaceBuffer
from utils.timer import WindowTimer
from utils.continuous_speech import ContinuousSpeech
from utils.fusion_manager import FusionManager
from utils.history_manager import HistoryManager
from utils.csv_logger import CSVLogger
from utils.analytics_manager import AnalyticsManager
from utils.face_detection import get_current_face_prediction


class SessionManager:

    def __init__(self):

        # -----------------------------
        # Core Components
        # -----------------------------
        self.face_buffer = FaceBuffer(window_size=30)

        self.timer = WindowTimer(seconds=30)

        self.speech_service = ContinuousSpeech(interval=5)

        self.fusion_manager = FusionManager(
            self.face_buffer,
            self.speech_service,
            self.timer
        )

        self.history_manager = HistoryManager()

        self.csv_logger = CSVLogger()

        self.analytics_manager = AnalyticsManager()

        self.started = False

        self.last_saved_second = -1

    # ------------------------------------------------
    # Start Monitoring
    # ------------------------------------------------
    def start(self):

        if self.started:
            return

        self.speech_service.start()

        self.started = True

    # ------------------------------------------------
    # Stop Monitoring
    # ------------------------------------------------
    def stop(self):

        if not self.started:
            return

        self.speech_service.stop()

        self.started = False

    # ------------------------------------------------
    # Collect Face Prediction (1 prediction / second)
    # ------------------------------------------------
    def collect_face_prediction(self):

        emotion, confidence = get_current_face_prediction()

        current_second = int(time.time())

        if current_second != self.last_saved_second:

            self.last_saved_second = current_second

            if emotion != "No Face":

                self.face_buffer.add(
                    emotion,
                    confidence
                )

        return emotion, confidence

    # ------------------------------------------------
    # Update Session
    # ------------------------------------------------
    def update(self):

        summary = self.fusion_manager.update()

        if summary is None:
            return None

        self.history_manager.add(summary)

        latest = self.history_manager.latest()

        self.csv_logger.log(latest)

        return latest

    # ------------------------------------------------
    # Live Status
    # ------------------------------------------------
    def remaining_time(self):

        return self.timer.remaining()

    def frame_count(self):

        return len(self.face_buffer.emotions)

    def speech_summary(self):

        return self.speech_service.get_summary()

    # ------------------------------------------------
    # Latest Summary
    # ------------------------------------------------
    def latest(self):

        return self.history_manager.latest()

    # ------------------------------------------------
    # History
    # ------------------------------------------------
    def history(self):

        return self.history_manager.get_history()

    # ------------------------------------------------
    # Analytics
    # ------------------------------------------------
    def analytics(self):

        history = self.history()

        return {

            "total_windows":
                self.analytics_manager.total_windows(history),

            "dominant_emotion":
                self.analytics_manager.dominant_emotion(history),

            "emotion_counts":
                self.analytics_manager.emotion_counts(history),

            "face_counts":
                self.analytics_manager.face_counts(history),

            "speech_counts":
                self.analytics_manager.speech_counts(history)

        }

    # ------------------------------------------------
    # Reset
    # ------------------------------------------------
    def reset(self):

        self.face_buffer.reset()

        self.speech_service.clear()

        self.timer.reset()

        self.history_manager.clear()