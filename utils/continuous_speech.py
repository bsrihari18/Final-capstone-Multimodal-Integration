from utils.speech_buffer import SpeechBuffer
from utils.speech_recognition import recognize_speech_from_audio
from utils.text_prediction import predict_text_emotion


class ContinuousSpeech:
    """Browser-audio speech collector — no background threads or PyAudio."""

    def __init__(self, interval=5):
        self.interval = interval
        self.buffer = SpeechBuffer()
        self.enabled = False
        self.last_error = None

    def start(self):
        self.enabled = True
        self.last_error = None

    def stop(self):
        self.enabled = False

    def process_audio(self, audio_bytes):
        """Process one browser audio sample and append to the buffer."""
        if not self.enabled or not audio_bytes:
            return False

        text = recognize_speech_from_audio(audio_bytes)

        if not text or not text.strip():
            self.last_error = "Could not recognize speech in this recording."
            return False

        text = text.strip()

        try:
            result = predict_text_emotion(text)
            emotion = result[-1] if isinstance(result, tuple) else result
        except Exception as exc:
            self.last_error = f"Emotion prediction failed: {exc}"
            return False

        self.buffer.add_prediction(emotion=emotion, text=text)
        self.last_error = None
        return True

    def get_summary(self):
        return self.buffer.get_summary()

    def clear(self):
        self.buffer.clear()
        self.last_error = None
