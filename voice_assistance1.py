import os
import subprocess
import webbrowser
import pyautogui
import speech_recognition as sr
import pyttsx3
import requests
from datetime import datetime

recognizer = sr.Recognizer()
mic = sr.Microphone()

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Error with pyttsx3:", e)

def process_command(command):
    command = command.lower().strip()
    responses = []
    
    if "what is the time" in command:
        current_time = datetime.now().strftime("%H:%M:%S")
        responses.append(f"The time is {current_time}.")

    
    if "what is the date" in command:
        current_date = datetime.now().strftime("%Y-%m-%d")
        responses.append(f"Today's date is {current_date}.")
    
    if "open telegram" in command:
        telegram_path = r"C:\\Users\\Nedal\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe" 
        if os.path.exists(telegram_path):
            subprocess.Popen([telegram_path])
            responses.append("Opening Telegram.")
        else:
            responses.append("Telegram executable not found.")

    if "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        responses.append("Opening WhatsApp.")

    if "open instagram" in command:
        webbrowser.open("https://www.instagram.com")
        responses.append("Opening Instagram.")

    if "open chrome" in command or "open browser" in command:
        webbrowser.open("https://www.google.com")
        responses.append("Opening Chrome.")

    if "open settings" in command:
        if os.name == 'nt':  # Windows
            subprocess.run(["start", "ms-settings:"], shell=True)
            responses.append("Opening Settings.")
        else:
            responses.append("Settings command is not supported on this OS.")

    if "take a screenshot" in command:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        responses.append("Screenshot taken and saved as 'screenshot.png'.")

    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        responses.append("Opening YouTube.")

    if "search for" in command:
        query = command.split("search for")[-1].strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            responses.append(f"Searching for {query} on Google.")

    if "exit" in command:
        responses.append("Exiting. Goodbye!")
        return "exit"

    if responses:
        return " ".join(responses)
    else:
        return "I don't understand!"

def main():
    print("Listening...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)
                print(f"Command: {command}")

                
                speak(f"You said: {command}")

                
                response = process_command(command)
                if response == "exit":
                    speak("Goodbye!")
                    print("Exiting...")
                    break

                print(f"Assistant: {response}")
                speak(response)

            except sr.UnknownValueError:
                print("Sorry, I didn't catch that.")
                speak("Sorry, I didn't catch that.")
            except sr.RequestError as e:
                print(f"Error: {e}")
                speak(f"There was an error: {e}")

if __name__ == "__main__":
    main()
