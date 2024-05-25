import speech_recognition as sr
import datetime
import os
import webbrowser
import random
import wikipedia
from requests import get
import pywhatkit as kit
import sys
import openai

# Replacing 'YOUR_OPENAI_API_KEY' with your actual API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Function to print instead of speaking
def speak(text):
    print(text)

# Convert voice into text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as audio:
        speak('Listening...')
        r.pause_threshold = 1
        try:
            voice = r.listen(audio, timeout=10, phrase_time_limit=5)
            speak("Thinking...")
            query = r.recognize_google(voice, language='en-in')
            speak("Transcription: " + query)
            return query
        except sr.UnknownValueError:
            speak("I couldn't understand what you said.")
            return "none"
        except sr.RequestError:
            speak("There was an issue with the speech recognition service.")
            return "none"

def chat_with_gpt3(query):
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=query,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        speak("Error in GPT-3 API: " + str(e))
        return "I'm sorry, there was an issue with my response."

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good Morning")
    elif hour > 12 and hour < 18:
        speak("Good Evening")
    else:
        speak("Good Evening")
    speak("I'm Geralt AI, Is there anything I can help you with?")

if __name__ == "__main__":
    speak("Hello Sir!")
    wish()
    while True:
        query = takecommand().lower()

        # Logic building for tasks
        if "open notepad" in query:
            speak("Notepad is not available on this platform.")
        elif "launch chrome" in query:
            webbrowser.open('https://www.google.com/')
        elif "open command prompt" in query:
            speak("Command prompt is not available on this platform.")
        elif "open discord" in query:
            webbrowser.open('https://discord.com/')
        elif "open camera" in query:
            speak("Camera access is not available on this platform.")
        elif "play music" in query:
            speak("Music playback is not supported on this platform.")
        elif "ip address" in query:
            ip = get('http://api.ipify.org').text
            speak(f"Your IP Address is {ip}")
        elif "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
            print(results)
        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")
        elif "open facebook" in query:
            webbrowser.open("www.facebook.com")
        elif "open google" in query:
            speak("Sir, what should I search on Google?")
            cm = takecommand().lower()
            webbrowser.open(f"https://www.google.com/search?q={cm}")
        elif "send message" in query:
            kit.sendwhatmsg("+917439897125", "This is a testing message from Geralt AI.", 2, 25)
        elif "play song on youtube" in query:
            kit.playonyt("A Thousand Years")
        elif "no" in query or "no thanks" in query:
            speak("Thanks for using me Sir, have a good day.")
            sys.exit()
        else:
            chat_response = chat_with_gpt3(query)
            speak(chat_response)
            speak("Sir, do you have any other work?")
