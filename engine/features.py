import os
import shlex
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pyaudio
import pyautogui
import requests
# from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import pvporcupine
from engine.helper import extract_yt_term, remove_words
from huggingface_hub import InferenceClient
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from engine.speakk import speak
import pypdf
from transformers import pipeline

# Database connection
con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# Load environment variables
load_dotenv()
api_token = os.getenv("HF_TOKEN")
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")

# Check if required environment variables are set
if not api_token:
    raise ValueError("Hugging Face token not found. Make sure it's in the .env file as HF_TOKEN.")
if not sender_email or not sender_password:
    raise ValueError("Sender email or password not found in the .env file.")


model_name = "mistralai/Mistral-7B-Instruct-v0.3"
llm_client = InferenceClient(model=model_name, token=api_token)

@eel.expose
def playAssistantSound():
    # Adjust the path to the correct location
    music_dir = "C:/Users/LENOVO/Desktop/jarvis/www/assets/audio/start_sound.mp3"
    

    if os.path.exists(music_dir):
        playsound(music_dir)
    else:
        print(f"Error: {music_dir} not found!")

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()
    app_name = query.strip()

    if app_name != "":
        try:
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + query)
                os.startfile(results[0][0])
            elif len(results) == 0:
                cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                if len(results) != 0:
                    speak("Opening " + query)
                    webbrowser.open(results[0][0])
                else:
                    speak("Opening " + query)
                    try:
                        os.system('start ' + query)
                    except:
                        speak("not found")
        except:
            speak("something went wrong")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)

# Updated chatbot function
def chatBot(query):
    """Generates a chatbot response for the given query using Hugging Face."""
    try:
        response = llm_client.text_generation(prompt=query, max_new_tokens=150)
        print(response)  # Log the response
        speak(response)  # Speak the response
        return response
    except Exception as e:
        return f"Error: {str(e)}"

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)
            if keyword_index >= 0:
                print("hotword detected")
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)
    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str
        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0

def whatsApp(mobile_no, message, flag, name):
    if flag == 'message':
        target_tab = 17
        jarvis_message = "message sent successfully to " + name
    elif flag == 'call':
        target_tab = 12
        message = ''
        jarvis_message = "calling to " + name
    else:
        target_tab = 11
        message = ''
        jarvis_message = "starting video call with " + name

    encoded_message = shlex.quote(message)
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
    full_command = f'start "" "{whatsapp_url}"'
    subprocess.run(full_command, shell=True)
    time.sleep(2)
    subprocess.run(full_command, shell=True)
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(2)
    for i in range(1, target_tab):
        pyautogui.hotkey('tab')
    pyautogui.hotkey('enter')
    speak(jarvis_message)

def makeCall(name, mobileNo):
    mobileNo = mobileNo.replace(" ", "")
    speak("Calling " + name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:' + mobileNo
    os.system(command)

def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    tapEvents(370, 2176)
    tapEvents(840, 2252)
    adbInput(mobileNo)
    tapEvents(500, 513)
    tapEvents(500, 2301)
    adbInput(message)
    tapEvents(974, 1480)
    speak("message sent successfully to " + name)

def get_weather_report(location, api_key):
    
    try:
        # OpenWeatherMap API endpoint
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

        # Send GET request to fetch the weather data
        response = requests.get(url)
        data = response.json()

        # Check if the API returned an error
        if data["cod"] != 200:
            return f"Error fetching weather data: {data['message']}"

        # Extract weather information
        city = data["name"]
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]

        # Format the weather report
        report = f"The current temperature in {city} is {temperature}°C with {weather_description}."
        return report

    except Exception as e:
        return f"An error occurred: {str(e)}"
    



def generate_email_content(prompt):
    """
    Generate email content using the Hugging Face model.
    """
    try:
        # Ensure the prompt is not empty
        if not prompt:
            return "Error: Email prompt is empty."

        # Generate the email content using the LLM client
        response = llm_client.text_generation(
            prompt=prompt,
            max_new_tokens=150,
            temperature=0.7
        )
        return response
    except Exception as e:
        return f"Error generating email content: {str(e)}"


def send_email(subject, body, recipient_email):
    """
    Send an email with the given subject and body to the specified recipient.
    """
    try:
        # Ensure all required fields are present
        if not subject or not body or not recipient_email:
            return "Error: Missing email subject, body, or recipient email."

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure connection
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {str(e)}"


        
def extract_email_from_query(query):
    """
    Extracts email addresses or recipient names from the query using regex.
    """
    import re

    # Check if the query contains an email address
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_matches = re.findall(email_regex, query)

    if email_matches:
        return email_matches[0]  # Return the first match

    # If no email found, check for common names (you can add more names here)
    if "vivek" in query.lower():
        return "vp983351@gmail.com"
    elif "omkar" in query.lower():
        return "omkarchandra206@gmail.com"

    # Return None if no email is found
    return None






