import csv
import io
import os

from utils.constants import OUTPUTS_DIR


class CSVLogger:
    """Session CSV log with optional local file append and export support."""

    HEADERS = [
        "Time",
        "Face Emotion",
        "Face Confidence",
        "Frames",
        "Speech Emotion",
        "Speech Samples",
        "Final Emotion",
    ]

    def __init__(self, filename=None):
        if filename is None:
            os.makedirs(OUTPUTS_DIR, exist_ok=True)
            filename = os.path.join(OUTPUTS_DIR, "emotion_history.csv")

        self.filename = filename
        self._ensure_file()

    def _ensure_file(self):
        directory = os.path.dirname(self.filename)
        if directory:
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="", encoding="utf-8") as handle:
                csv.writer(handle).writerow(self.HEADERS)

    def log(self, record):
        row = [
            record["time"],
            record["face_emotion"],
            record["face_confidence"],
            record["frames"],
            record["speech_emotion"],
            record["speech_count"],
            record["final_emotion"],
        ]

        try:
            with open(self.filename, "a", newline="", encoding="utf-8") as handle:
                csv.writer(handle).writerow(row)
        except OSError:
            # Streamlit Cloud filesystem is ephemeral; in-memory history still works.
            pass

    @staticmethod
    def export_csv(history):
        """Build CSV text from in-memory history for download."""
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(CSVLogger.HEADERS)

        for record in history:
            writer.writerow([
                record["time"],
                record["face_emotion"],
                record["face_confidence"],
                record["frames"],
                record["speech_emotion"],
                record["speech_count"],
                record["final_emotion"],
            ])

        return buffer.getvalue()
