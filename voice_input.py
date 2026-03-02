import speech_recognition as sr

def get_voice_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except:
        return "Voice not recognized"