import io

import speech_recognition as sr


def recognize_speech_from_audio(audio_bytes):
    """
    Transcribe browser-captured audio (WAV bytes from st.audio_input).

    Works on Streamlit Cloud — no server-side microphone or PyAudio required.
    """
    if not audio_bytes:
        return None

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio = recognizer.record(source)

        return recognizer.recognize_google(audio)

    except sr.UnknownValueError:
        return None

    except sr.RequestError:
        return None

    except Exception:
        return None


def recognize_speech():
    """
    Legacy helper kept for local scripts/tests.

    On Streamlit Cloud there is no server microphone — use
    recognize_speech_from_audio() with st.audio_input instead.
    """
    try:
        import pyaudio  # noqa: F401
    except ImportError:
        return None

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

        return recognizer.recognize_google(audio)

    except (sr.UnknownValueError, sr.RequestError, OSError):
        return None
