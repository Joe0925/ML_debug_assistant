import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import numpy as np
import tempfile
import speech_recognition as sr

def get_voice_input():
    st.write(" Click start and speak")

    ctx = webrtc_streamer(
        key="speech",
        mode=WebRtcMode.SENDRECV,
        audio_receiver_size=1024,
        media_stream_constraints={"audio": True, "video": False},
    )

    if ctx.audio_receiver:
        try:
            audio_frames = ctx.audio_receiver.get_frames(timeout=1)
            audio_data = b"".join([frame.to_ndarray().tobytes() for frame in audio_frames])

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                tmpfile.write(audio_data)
                tmp_path = tmpfile.name

            recognizer = sr.Recognizer()
            with sr.AudioFile(tmp_path) as source:
                audio = recognizer.record(source)

            text = recognizer.recognize_google(audio)
            return text

        except:
            return None