# voice_input.py

import streamlit as st
from streamlit_mic_recorder import mic_recorder


def get_voice_input():
    """
    Records voice input from the user using streamlit-mic-recorder.
    Returns recorded audio bytes if available.
    """

    audio = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop Recording",
        key="voice_input_recorder"
    )

    if audio:
        return audio["bytes"]

    return None