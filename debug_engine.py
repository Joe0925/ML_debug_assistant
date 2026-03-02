from ai_engine import analyze_with_ai

def analyze_error(user_input):

    if not user_input or not user_input.strip():
        return "Please enter an ML error to analyze."

    if user_input.lower().strip() in [
        "voice not recognized",
        "could not understand",
        "none"
    ]:
        return "🎙️ Voice not recognized. Please try again."

    try:
        return analyze_with_ai(user_input)

    except Exception as e:
        return f"AI Service Error: {str(e)}"