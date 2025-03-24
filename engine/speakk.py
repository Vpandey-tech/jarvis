import eel
import pyttsx3
from pynput import keyboard
import threading

stop_speech_flag = False

def on_press(key):
    global stop_speech_flag
    if key == keyboard.Key.esc:
        stop_speech_flag = True
        return False

def speak(text):
    global stop_speech_flag
    stop_speech_flag = False

    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 170)
    
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Debug: Log to console to confirm this runs
    print(f"Sending to chat: {text}")
    eel.receiverText(text)  # Send to chat section

    sentences = text.split('. ')
    for sentence in sentences:
        if stop_speech_flag:
            engine.stop()
            eel.ShowHood()
            break
        engine.say(sentence)
        engine.runAndWait()

    if listener.is_alive():
        listener.stop()

    if stop_speech_flag:
        eel.ShowHood()
    stop_speech_flag = False