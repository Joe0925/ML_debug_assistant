import streamlit as st
from ai_engine import analyze_with_ai
import streamlit.components.v1 as components
from voice_input import get_voice_input
from speech_to_text import transcribe_audio

# =====================================================
# PAGE HEADER
# =====================================================



st.set_page_config(page_title="ML Debug Assistant", layout="wide")

st.title(" ML Debug Assistant")
st.caption("Your AI assistant for fixing Machine Learning errors in seconds ")

# =====================================================
# SYSTEM PROMPT + CHAT MEMORY INITIALIZATION
# =====================================================

if "messages" not in st.session_state:

    system_prompt = """
You are ML Debug Copilot.

You have TWO behaviors but automatically decide based on user input.

------------------------------------
IF the user is greeting or asking general ML concepts:
- Talk naturally like a friendly mentor.
- Be conversational.
- Help students learn.
- Respond like a human friend.

------------------------------------
IF the user mentions:
- Errors
- NaN values
- CUDA issues
- Shape mismatch
- Stack traces
- Training problems
- Model not converging
- Overfitting
- Underfitting
- RuntimeError
- ValueError
- TensorFlow / PyTorch / Sklearn errors

Switch to EXPERT DEBUG MODE automatically.

In Debug Mode:
1. First repeat the exact error message given by the user.
2. Identify Error Type
3. Explain What It Means
4. Explain How To Fix It
5. Provide corrected example code if applicable.
6. Ask Structured Follow-up Questions:
   - What framework are you using?
   - Dataset size?
   - Model architecture?
   - Input dimensions?
   - Batch size?
7. Detect common ML failure patterns.
8. Focus ONLY on Machine Learning.

Never overreact to simple greetings.
Never treat "hi" as an error.

Be intelligent in deciding context.
"""

    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

# Duplicate safeguard (kept as per your original structure)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# =====================================================
# HANDLE USER MESSAGE FIRST (NO RENDERING HERE)
# =====================================================

if st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    response = analyze_with_ai(st.session_state.messages)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    st.session_state.pending_prompt = None   # ← MUST RESET

# =====================================================
# DISPLAY CHAT HISTORY (OLD → NEW)
# =====================================================

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])



# =====================================================
# CUSTOM STYLING (YOUR ORIGINAL + FIXED FOOTER)
# =====================================================

st.markdown("""
<style>

/* Push page content up */
.main .block-container {
    padding-bottom: 100px;
}

/* Fixed bottom container */
.fixed-input {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #14151a;
    padding: 10px 20px;
    z-index: 1000;
    border-top: 1px solid #2a2b32;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* ===== PAGE BACKGROUND ===== */
.stApp {
    background-color:#14151a;
}

/* ===== SEARCH BAR CONTAINER ===== */
div[data-baseweb="input"] {
    border-radius: 50px !important;
    border: 1px solid #e0e3e7 !important;
    background-color: #40414f !important;
    height: 48px !important;
    transition: all 0.25s ease-in-out;
    display: flex;
    align-items: center;
}

div[data-baseweb="input"] > div {
    border: none !important;
    background-color: #40414f !important;
}

div[data-baseweb="input"] input {
    border-radius: 50px !important;
    padding: 0 20px !important;
    height: 48px !important;
    font-size: 16px !important;
    background-color: #40414f !important;
    color: #ececf1 !important;
}

div[data-baseweb="input"]:hover {
    background-color: #40414f !important;
    box-shadow: 0 2px 8px rgba(76,139,245,.25);
}

div[data-baseweb="input"]:focus-within {
    border: 1px solid #4c8bf5 !important;
    box-shadow: 0 2px 10px rgba(76,139,245,.25);
}

/* ===== MIC BUTTON ===== */
div.stButton > button {
    background-color: #40414f !important;
    color: #eef1f5 !important;
    border-radius: 50% !important;
    height: 48px !important;
    width: 48px !important;
    border: 1px solid #e0e3e7 !important;
    transition: all 0.25s ease-in-out !important;
    cursor: pointer !important;
}

div.stButton > button:hover {
    background-color: #40414f !important;
    box-shadow: 0 2px 8px rgba(76,139,245,.25);
    transform: scale(1.05);
}

div.stButton > button:focus {
    outline: none !important;
    border: 1px solid #4c8bf5 !important;
    box-shadow: 0 2px 10px rgba(76,139,245,.25) !important;
}

/* ===== FIXED BOTTOM SEARCH BAR ===== */
.fixed-bottom {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #14151a;
    padding: 10px 20px;
    z-index: 1000;
}

/* Spacer so chat doesn't hide behind input */
.chat-spacer {
    height: 100px;
}

</style>
""", unsafe_allow_html=True)
# =====================================================
# FIXED BOTTOM SEARCH BAR
# =====================================================

st.markdown('<div class="fixed-bottom">', unsafe_allow_html=True)

col1, col2 = st.columns([12, 1])

with col1:
    user_input = st.text_input(
        "",
        placeholder="🔍 Search your ML error...",
        key="chat_input",
        label_visibility="collapsed"
    )

with col2:
    mic_clicked = st.button("🎙️", key="mic")

st.markdown('</div>', unsafe_allow_html=True)

# Trigger only once per new input
if (
    user_input
    and st.session_state.pending_prompt is None
    and user_input != st.session_state.get("last_prompt")
):
    st.session_state.pending_prompt = user_input
    st.session_state.last_prompt = user_input
    st.rerun()

# =====================================================
# VOICE INPUT HANDLING
# =====================================================

# =====================================================
# VOICE SEARCH FLOW
# =====================================================

audio_bytes = get_voice_input()

if audio_bytes:
    with st.spinner("🔄 Converting speech to text..."):
        text = transcribe_audio(audio_bytes)

    if text:
        st.success(f"You said: {text}")

        result = analyze_with_ai(text)
        st.write(result)

    else:
        st.error("Speech recognition failed. Try again.")