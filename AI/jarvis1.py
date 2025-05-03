import pyttsx3
import speech_recognition as sr
import wikipedia
import datetime
import webbrowser
import pywhatkit as wk
import os

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 185)      # Voice speed

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
            speak("My name is Jarvis")
            print("I can do Everything that my creator programmed me to do ")
            speak("I can do Everything that my creator programmed me to do ")

        elif "who created you" in query:
            print("I do not know")
            speak("I do not know")

        elif "what is the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            print(f"Sir, the time is {strTime}")        
            speak(f"Sir, the time is {strTime}")    
    
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

        # elif "what is" in query or "who is" in query:
        #     speak("Searching in Wikipedia...")
        #     query = query.replace("what is", "").replace("who is", "")
        #     try:
        #         # Handle disambiguation and search
        #         results = wikipedia.summary(query, sentences=2)
        #         speak("According to Wikipedia...")
        #         print(results)
        #         speak(results)
        #     except wikipedia.exceptions.DisambiguationError as e:
        #         print("There are multiple meanings for this query. Please specify one of the following options:")
        #         print(e.options)  # Show possible options to refine the query
        #         speak("There are multiple meanings for this query. Please be more specific.")
        #     except wikipedia.exceptions.PageError:
        #         print("Sorry, no matching page found.")
        #         speak("Sorry, I couldn't find anything on Wikipedia.")
        #     except Exception as e:
        #         print(f"An error occurred: {e}")
        #         speak("Sorry, I couldn't retrieve information at this moment.")    

        elif "just open Google" in query:
            webbrowser.open("google.com")

        elif "open google" in query:
            speak("what should I search ?")
            qry = takeCommand().lower()
            webbrowser.open(f"{qry}")
            results = wikipedia.summary(qry, sentences=1)
            speak(results)

        elif "just open youtube" in query:
            webbrowser.open("youtube.com")

        elif "open youtube" in query:
            speak("what you will like to watch ?")
            qrry = takeCommand().lower()
            wk.playonyt(f'{qrry}')

        elif "search on youtube" in query:
            query = query.replace("search on youtube", "")
            webbrowser.open(f"www.youtube.com/results?search_query={query}")

        elif "close browser" in query:
            os.system("taskkill /f /im msedge.exe")

        elif "shut down the system" in query:
            os.system("shutdown /s /t 5")

        elif "restart the system" in query:
            os.system("shutdown /r /t 5")