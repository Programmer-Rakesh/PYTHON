import pyttsx3

engine = pyttsx3.init("sapi5")
engine.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
engine.setProperty('rate', 185)

def speak(audio):
    print(f"Jarvis: {audio}")
    engine.say(audio)
    engine.runAndWait()

speak("Hello Rakesh, I am Zira. This is your assistant speaking in a female voice.")
