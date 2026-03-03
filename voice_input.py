from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import tempfile

def get_voice_input():
    audio = mic_recorder(
        start_prompt=" Start Recording",
        stop_prompt=" Stop Recording",
        key="recorder"
    )

    if audio:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            tmpfile.write(audio["bytes"])
            tmp_path = tmpfile.name

        recognizer = sr.Recognizer()

        with sr.AudioFile(tmp_path) as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except:
            return "Could not understand audio"

    return None