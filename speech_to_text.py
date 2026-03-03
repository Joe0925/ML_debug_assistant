import requests
import streamlit as st

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"

headers = {
    "Authorization": f"Bearer {st.secrets['HF_TOKEN']}"
}

def transcribe_audio(audio_bytes):
    response = requests.post(API_URL, headers=headers, data=audio_bytes)

    if response.status_code == 200:
        return response.json().get("text", "")
    else:
        return ""