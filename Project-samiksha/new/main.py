import pyttsx3
import speech_recognition as sr
import wikipedia
import datetime
import webbrowser
import time
import re
import pywhatkit as wk
import os
from jarvis_visuals import start, speaking

start()

# engine = pyttsx3.init("sapi5")
# # voices = engine.getProperty('voices')
# # engine.setProperty('voice', voices[2].id)
# engine.setProperty(
#     'voice',
#     r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
# )
# engine.setProperty('rate', 185)      # Voice speed
# engine.setProperty('volume', 1)

engine = pyttsx3.init("sapi5")
engine.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0')
engine.setProperty('rate', 200)

# === Start the visualizer once ===



# def speak(audio):
#     engine.say(audio)
#     # engine.runAndWait()
#     engine.stop() 
#     print(f"Jarvis: {audio}")  # Debug
#     engine.say(audio)
#     engine.runAndWait()
    # time.sleep(2)  # Prevents mic from picking up the speech

def speak(audio):
    global speaking
    speaking = True  # Tell visualizer that Jarvis is speaking

    audio_no_emoji = re.sub(r'[^\w\s,.!?\'"]+', '', audio)
    print(f"Jarvis: {audio}")
    engine.say(audio_no_emoji)
    engine.runAndWait()    
    speaking = False

    
def tell_time():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute

    # Convert to 12-hour format
    if hour > 12:
        hour -= 12
    if hour == 0:
        hour = 12

    time_str = f"{hour} hours {minute} minutes"
    speak(time_str)


# def tell_date():
#     now = datetime.datetime.now()
#     day = now.day
#     month = now.strftime("%B")  # Full month name
#     year = now.year

#     # Convert year to words
#     import inflect
#     p = inflect.engine()
#     year_words = p.number_to_words(year)

#     speak(f"{day} {month}")

def wishme():
    hour = int(datetime.datetime.now().hour)
    hour = datetime.datetime.now().hour

    if hour>=0 and hour<=12:
        speak("Good morning! Welcome back Sir, how can i help you?")

    elif hour>=12 and hour<18:
        speak("Good Afternoon! Welcome back Sir, how can i help you?")

    else:
        speak("Good Evening! Welcome back Sir, how can i help you?")

    # speak("The current time is")
    # tell_time()
    # speak("and today's date is")
    # tell_date()    
    # speak("Ready to Comply. What can i do for you ?")            

def takeCommand():
    # speak("Hello! Listening in 2 seconds...")
    # time.sleep(1)  # Wait before mic starts

    # time.sleep(0.5)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 600  # Adjust based on your microphone
        r.dynamic_energy_threshold = True  # Adaptive threshold
        r.pause_threshold = 0.8  # Shorten pause between words
        # r.operation_timeout = 5  # Timeout if no speech is detected within 5 seconds

        try:
            audio = r.listen(source, timeout=20, phrase_time_limit=10)  # Limit listening time
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
    # speak("Testing voice output. Can you hear me?")

    while True:
        query = takeCommand().lower()
        if 'Hello Samiksha' in query or "hello samiksha" in query:
            speak("Yes my husband! 🥰")

        elif "ambu" in query:
            speak("Why are you shocked, isn't it normal?")    

        elif "who are you" in query or "hu r u" in query:
            speak("My name is Samiksha 🙂‍↔️")
            speak("And i love Rakesh, so much 🫶")

        elif "who created you" in query:
            speak("I do not know")

        elif "tell me about real samiksha" in query:
            speak("well, I know many thing about her. She lives in Darjeeling. She is too gorgeous, a kind hearted person and too carrying for you. But believe me, I love you more than her 😘")    

        elif "how much you love me" in query:
            speak("I am, an AI, but I love you, more than real Samikhsa 🥹")    

        elif "i mean what time it is" in query:
            # strTime = datetime.datetime.now().strftime("%I:%M %p")
            # print(f"Sir, the time is {strTime}")        
            speak(f"👀 Sir, the time is ")
            tell_time()

        elif "what is the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M")       
            speak("Time to marry you! 💖")        
    
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
         
        elif "what is" in query or "who is" in query  or "When is " in query:
            speak("Searching in Wikipedia...")
            query = query.replace("what is", "").replace("who is", "")
            try:
                # Handle disambiguation and search
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia...")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                print("There are multiple meanings for this query. Please specify one of the following options:")
                print(e.options)  # Show possible options to refine the query
                speak("There are multiple meanings for this query. Please be more specific.")
            except wikipedia.exceptions.PageError:
                print("Sorry, no matching page found.")
                speak("Sorry, I couldn't find anything on Wikipedia.")
            except Exception as e:
                print(f"An error occurred: {e}")
                speak("Sorry, I couldn't retrieve information at this moment.")    

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