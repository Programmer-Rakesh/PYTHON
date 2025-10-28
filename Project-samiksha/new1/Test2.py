import pyttsx3
import speech_recognition as sr
import wikipedia
import datetime
import webbrowser
import pywhatkit as wk
import os
import pygame
import threading
import math
import time
import re


# GLOBALS
speaking = False        # Visual reacts when Jarvis speaks
subtitle_lock = threading.Lock()  # Thread-safe subtitle update
current_subtitle = ""   # Text shown in visual


# VISUALIZER
def visualizer():
    """Siri/Alexa style ripple visualizer with wrapped subtitles"""
    global speaking, current_subtitle
    pygame.init()
    WIDTH, HEIGHT = 800, 600   # Bigger window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jarvis Visualizer")
    clock = pygame.time.Clock()
    t = 0

    font = pygame.font.SysFont('arial', 20, bold=True)  # Slightly smaller font

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        t += 0.05
        base_radius = 120
        extra_radius = 60 if speaking else 20

        # Ripple circles
        for i in range(4):
            radius = base_radius + math.sin(t + i) * extra_radius
            alpha = max(30, 150 - i*30)
            color = pygame.Color(0, 180, 255)
            color.a = alpha
            surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(surface, color, (WIDTH//2, HEIGHT//2), int(radius), 6)
            screen.blit(surface, (0, 0))

        # Subtitles (wrapped)
        subtitle_lock.acquire()
        text = current_subtitle
        subtitle_lock.release()
        words = text.split()
        line = ""
        lines = []
        max_width = WIDTH - 100
        for word in words:
            test_line = line + word + " "
            render = font.render(test_line, True, (255, 255, 255))
            if render.get_width() > max_width:
                lines.append(line)
                line = word + " "
            else:
                line = test_line
        lines.append(line)

        for i, l in enumerate(lines):
            render = font.render(l, True, (255, 255, 255))
            screen.blit(render, (50, HEIGHT - 50 - 25*(len(lines)-i-1)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# Start visualizer thread
threading.Thread(target=visualizer, daemon=True).start()


# SPEECH ENGINE
engine = pyttsx3.init("sapi5")
engine.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0')
engine.setProperty('rate', 200)

def update_subtitle(text):
    global current_subtitle
    subtitle_lock.acquire()
    current_subtitle = text
    subtitle_lock.release()

def speak(audio):
    global speaking
    speaking = True
    update_subtitle(f"Jarvis: {audio}")
    audio_no_emoji = re.sub(r'[^\w\s,.!?\'"]+', '', audio)
    engine.say(audio_no_emoji)
    engine.runAndWait()
    speaking = False


# TIME & WISH FUNCTIONS
def tell_time():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    if hour > 12:
        hour -= 12
    if hour == 0:
        hour = 12
    speak(f"{hour} hours {minute} minutes")

def wishme():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good morning! Welcome back Sir, how can I help you?")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon! Welcome back Sir, how can I help you?")
    else:
        speak("Good Evening! Welcome back Sir, how can I help you?")


# COMMAND LISTENER
def takeCommand():
    update_subtitle("Listening...")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 600
        r.dynamic_energy_threshold = True
        r.pause_threshold = 0.8
        try:
            audio = r.listen(source, timeout=20, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return "None"
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except:
        query = "None"
    update_subtitle(f"You: {query}\nJarvis: ...")
    return query.lower()

# MAIN
if __name__ == "__main__":
    wishme()

    while True:
        query = takeCommand()

        if 'hello samiksha' in query:
            speak("Yes my husband! 🥰")

        elif "ambu" in query:
            speak("Why are you shocked, isn't it normal?")

        elif "who are you" in query or "hu r u" in query:
            speak("My name is Samiksha 🙂‍↔️")
            speak("And I love Rakesh, so much 🫶")

        elif "who created you" in query:
            speak("I do not know")

        elif "tell me about real samiksha" in query:
            speak("Well, I know many things about her. She lives in Darjeeling. She is gorgeous, kind-hearted and caring. But believe me, I love you more than her 😘")

        elif "how much you love me" in query:
            speak("I am an AI, but I love you more than real Samiksha 🥹")

        elif "i mean what time it is" in query:        
            speak(f"👀 Sir, the time is ")
            tell_time()

        elif "what is the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M")       
            speak("Time to marry you! 💖")     

        elif "what is" in query:
            speak("Searching in Wikipedia...")
            query_clean = query.replace("what is", "")
            try:
                results = wikipedia.summary(query_clean, sentences=2)
                speak("According to Wikipedia...")
                speak(results)
            except:
                speak("Sorry, I couldn't find anything.")

        elif "who is" in query:
            speak("Searching in Wikipedia...")
            query_clean = query.replace("who is", "")
            try:
                results = wikipedia.summary(query_clean, sentences=2)
                speak("According to Wikipedia...")
                speak(results)
            except:
                speak("Sorry, I couldn't find anything.")

        elif "open google" in query:
            speak("What should I search?")
            qry = takeCommand().lower()
            webbrowser.open(f"{qry}")

        elif "open youtube" in query:
            speak("What would you like to watch?")
            qrry = takeCommand().lower()
            wk.playonyt(f'{qrry}')

        elif "close browser" in query:
            os.system("taskkill /f /im msedge.exe")
