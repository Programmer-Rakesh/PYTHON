import pyttsx3
import speech_recognition as sr
import wikipedia
import datetime
import webbrowser
import os

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 195)      # Voice speed

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("Ready to Comply. What can i do for you ?")            

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 300  # Adjust based on your microphone
        r.dynamic_energy_threshold = True  # Adaptive threshold
        r.pause_threshold = 0.8  # Shorten pause between words
        r.operation_timeout = 5  # Timeout if no speech is detected within 5 seconds

        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=5)  # Limit listening time
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase.")
            return "None"
        
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return "None"
    except sr.RequestError:
        print("Request failed; check your network connection.")
        return "None"

    return query.lower()

if __name__=="__main__":
    wishme()
    while True:
        query = takeCommand().lower()
        if 'hello jarvis' in query:
            print("Yes sir")
            speak("Yes sir")

        elif "who are you" in query:
            print("My name is Jarvis")
            speak("My name isd Jarvis")
            print("I can do Everything that my creator programmed me to do ")
            speak("I can do Everything that my creator programmed me to do ")

        elif "who created you" in query:
            print("I do not know")
            speak("I do not know")

        elif "what is" in query:
            speak("Searching in wikipedia...")
            query = query.replace("what is", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia...")
            print(results)
            speak(results)

        elif "who is" in query:
            speak("Searching in wikipedia...")
            query = query.replace("who is", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia...")
            print(results)
            speak(results)    

        elif "just open Google" in query:
            webbrowser.open("google.com")

        elif "open google" in query:
            speak("what should I search ?")
            qry = takeCommand().lower()
            webbrowser.open(f"{qry}")
            results = wikipedia.summary(qry, sentences=1)
            speak(results)

