# voice_input.py

from streamlit_mic_recorder import mic_recorder

def get_voice_input():
    audio = mic_recorder(
        start_prompt="🎤 Speak",
        stop_prompt="⏹ Stop",
        key="voice_recorder_unique"
    )

    if audio:
        return audio["bytes"]

    return None