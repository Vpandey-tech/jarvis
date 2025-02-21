import os
import re
import time


def extract_yt_term(command):
    """
    Extracts a search term (e.g., song name, artist) from a command string for YouTube.
    Handles various formats like:
    - "play [song name] on youtube"
    - "play [song name] by [artist]"
    - "play [song name] from [album]"
    - "search for [song name] on youtube"
    - "youtube [song name]"
    """
    # Define a flexible regular expression pattern to capture the search term
    pattern = r'(?:play|search|find)\s+(.*?)\s+(?:on\s+youtube|by\s+.*|from\s+.*|on\s+yt|$)'
    
    # Use re.search to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)
    
    if match:
        # Extract the search term and clean it up
        search_term = match.group(1).strip()
        
        # Remove unnecessary words like "the", "a", "on", "by", "from", etc.
        stop_words = {"the", "a", "an", "on", "by", "from", "for", "with", "to"}
        search_term = " ".join([word for word in search_term.split() if word.lower() not in stop_words])
        
        return search_term
    else:
        # If no match is found, return None
        return None



def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string



# key events like receive call, stop call, go back
def keyEvent(key_code):
    command =  f'adb shell input keyevent {key_code}'
    os.system(command)
    time.sleep(1)

# Tap event used to tap anywhere on screen
def tapEvents(x, y):
    command =  f'adb shell input tap {x} {y}'
    os.system(command)
    time.sleep(1)

# Input Event is used to insert text in mobile
def adbInput(message):
    command =  f'adb shell input text "{message}"'
    os.system(command)
    time.sleep(1)

# to go complete back
def goback(key_code):
    for i in range(6):
        keyEvent(key_code)

# To replace space in string with %s for complete message send
def replace_spaces_with_percent_s(input_string):
    return input_string.replace(' ', '%s')