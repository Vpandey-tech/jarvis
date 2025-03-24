

import eel
import pyttsx3
from pynput import keyboard
import threading

# Global engine reference and stop flag
engine = None
stop_speech_flag = False

def on_press(key):
    global stop_speech_flag, engine
    if key == keyboard.Key.esc:
        stop_speech_flag = True
        if engine is not None:
            engine.stop()  # Stop speech immediately
        eel.ShowHood()  # Show hood right away
        return False  # Stop listener

def speak(text):
    global stop_speech_flag, engine
    stop_speech_flag = False

    text = str(text)
    engine = pyttsx3.init('sapi5')  # Initialize engine here
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 170)

    # Start keyboard listener in a separate thread
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    print(f"Sending to chat: {text}")
    eel.receiverText(text)

    # Speak the full text at once (no sentence splitting)
    engine.say(text)
    engine.runAndWait()

    # Clean up
    if listener.is_alive():
        listener.stop()
    if stop_speech_flag:
        eel.ShowHood()
    stop_speech_flag = False
    engine = None  # Reset engine reference