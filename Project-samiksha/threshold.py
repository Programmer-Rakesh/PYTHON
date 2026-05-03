import speech_recognition as sr

r = sr.Recognizer()

# Try index 25 first — your physical mic
with sr.Microphone(device_index=3) as source:
    print("Calibrating...")
    r.adjust_for_ambient_noise(source, duration=1)
    print("Say something now...")
    try:
        audio = r.listen(source, timeout=10)
        print("Heard:", r.recognize_google(audio))
    except sr.WaitTimeoutError:
        print("Still timed out — try index 3 or 27")
    except sr.UnknownValueError:
        print("Heard something but couldn't understand")