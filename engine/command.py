import webbrowser
import pyautogui
import pyttsx3
import requests
import speech_recognition as sr
import eel
import time
from engine.features import  extract_email_from_query, send_email, generate_email_content 
from engine.speakk import speak

# def speak(text):
#     text = str(text)
#     engine = pyttsx3.init('sapi5')
#     voices = engine.getProperty('voices') 
#     engine.setProperty('voice', voices[0].id)
#     engine.setProperty('rate', 170)
#     eel.DisplayMessage(text)
#     engine.say(text)
#     eel.receiverText(text)
#     engine.runAndWait()






def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
       
    except Exception as e:
        return ""
    
    return query.lower()

# def takecommand():
#     """Try to capture voice input. If it fails, fall back to frontend chatbox input."""
#     r = sr.Recognizer()

#     try:
#         with sr.Microphone() as source:
#             print('Listening....')
#             eel.DisplayMessage('Listening....')  # Update frontend UI
#             r.pause_threshold = 1
#             r.adjust_for_ambient_noise(source)
#             audio = r.listen(source, timeout=5, phrase_time_limit=5)  # Listen for 5 seconds

#         try:
#             print('Recognizing....')
#             eel.DisplayMessage('Recognizing....')  # Update frontend UI
#             query = r.recognize_google(audio, language='en-in')  # Recognize speech using Google API
#             print(f"User said: {query}")
#             eel.DisplayMessage(query)  # Display recognized text on frontend
#             return query.lower()  # Return the recognized text

#         except sr.UnknownValueError:
#             print("Sorry, I could not understand the audio.")
#             eel.DisplayMessage("Sorry, I could not understand the audio.")  # Update frontend UI

#         except sr.RequestError as e:
#             print(f"Could not request results from Google Speech Recognition service; {e}")
#             eel.DisplayMessage("Speech recognition service error.")  # Update frontend UI

#     except sr.WaitTimeoutError:
#         print("No audio received. Falling back to frontend input.")
#         eel.DisplayMessage("No audio received. Falling back to frontend input.")  # Update frontend UI

#     # Fallback to frontend input
#     print("Waiting for text input from frontend...")
#     eel.DisplayMessage("Please type your command.")  # Update frontend to inform the user
#     query = eel.getFrontendInput()()  # Wait for the frontend to provide input
#     print(f"Frontend input received: {query}")
#     return query.lower()

# # Example usage
# query = takecommand()
# if query is None:
#     # Fallback to frontend input
#     query = eel.getFrontendInput()()  # Call frontend function to get text input
#     print(f"Frontend input: {query}")


@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query or "play" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query: 
                        speak("what message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("what message to send")
                        query = takecommand()
                                        
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name)

        elif "where i am" in query or "where we are" in query:
            speak("wait sir, let me check")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()
                city= geo_data['city']
                region = geo_data['region']
                country=geo_data['country']
                speak(f"sir we are in {city} city of {region} in {country}")
            except Exception as e:
                speak("sorry sir,due to network issue i am unable to find")
                pass

        
        elif "my instagram profile" in query or "instagram profile"in query:
            speak("opening your instagram .")
            webbrowser.open("www.instagram.com/vivk.here")
            speak("sir here is your instagram profile")
        

        elif "weather in this area" in query or "current weather" in query:
            from engine.features import get_weather_report 
            weather_report = get_weather_report("Maharashtra", "9b2cc80669e58967131002941db919f8")

            print(weather_report)
            speak(weather_report)

        elif "write email" in query.lower():
            """Generate email content based on the query and send it to the specified recipient."""
            recipient_email = extract_email_from_query(query)
            if recipient_email:
                email_content = generate_email_content(query)
                subject = "Generated Email from Chatbot"
                status =  send_email(subject, email_content, recipient_email)
                eel.DisplayMessage(status)
                return status
            else:
                error_message = "Recipient email is missing or invalid."
                eel.DisplayMessage(error_message)
                return error_message



        elif "take screenshot"in query or "take a screenshot"in query:
            speak("what should be the file name for screenshot")
            name = takecommand().lower()
            speak("please hold the screen")
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("done sir, i am ready for next command ")


        else:
            # Non-command queries are handled by the chatbot
            from engine.features import chatBot
            response = chatBot(query)
            eel.DisplayMessage(response)  # Display chatbot response on the UI

    except Exception as e:
        print("Error:", e)

    eel.ShowHood()

