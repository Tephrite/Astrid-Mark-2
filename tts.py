import pyttsx3 as tts

def speakText(text):
    
    engine = tts.init()
    engine.say(text)
    engine.runAndWait()
