import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Adjusting...")
    r.adjust_for_ambient_noise(source, duration=2)
    print(f"Energy threshold: {r.energy_threshold}")
