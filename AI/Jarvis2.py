import pyttsx3
import datetime
import speech_recognition as sr

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 195)      # Voice speed

def speak(audio):
    engine.say(audio)
    engine.runAndWait()    

#speak("This is Jarvis AI assistant")
#speak("The current time is")

def time():
    Time = datetime.datetime.now().strftime("%I:%M")     
    speak(Time)

#time()
#speak("The current date is")

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)      #convert int to variable
    date = int(datetime.datetime.now().day)
    speak(date)
    speak(month)
    speak(year)
#date()    

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <12:
        speak("Good Morning sir")

    elif hour >= 12 and hour <18:
        speak("Good Afternoon sir")    

    else:
        speak("Good Evening sir")
    #speak('Welcome back')    
    speak("the current time is")
    time()
    speak("and today's date is")
    date()
    speak("Jarvis at your service. please tell me how may I help you ?")
  
wishme()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recongnizing...")
        query = r.recognize_google(audio, language= 'en-in')
        print(query)
    except Exception as e:
        print(e)
        speak("Say that again please...")
        return "none"
    return query

takeCommand()

if __name__=="__main__":
    with True:
        query = takeCommand().lower()
        if 'Jarvis' in query:
            print("Yes sir")
            speak("Yes sir")