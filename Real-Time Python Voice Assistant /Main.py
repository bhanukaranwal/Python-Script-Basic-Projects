import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime

def speak(text):
    print(f"Assistant: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        query = recognizer.recognize_google(audio, language='en-US')
        print(f"You said: {query}")
        return query.lower()
    except Exception:
        speak("Sorry, I did not understand.")
        return ""

def voice_assistant():
    speak("Hello! How can I help you today?")
    while True:
        query = listen()
        if "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        elif "open google" in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
        elif "time" in query:
            now = datetime.datetime.now().strftime("%H:%M")
            speak(f"The current time is {now}")
        elif "exit" in query or "quit" in query:
            speak("Goodbye!")
            break
        elif query != "":
            speak("Sorry, I didn't understand that. Please try again.")

if __name__ == '__main__':
    voice_assistant()
