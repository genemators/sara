"""
APP: SARA - VOICE ASSISTANT
AUTHOR: Genemator Sakhib
VERSION: 0.0.1 alpha
STATUS: Rolling
"""

#
# Starting import process here
#

# Global scopic functions
from __future__ import print_function

# Loading installed modules
try:
    print('Importing "os" Module')
    import os
    print('"os" Module import completed successfully')

    print('Importing "time" Module')
    import time
    print('"time" Module import completed successfully')

    print('Importing "playsound" Module')
    import playsound
    print('"playsound" Module import completed successfully')

    print('Importing "SpeechRecognition" Module')
    import speech_recognition as sr
    print('"SpeechRecognition" Module import completed successfully')

    print('Importing "gtts" Module')
    from gtts import gTTS
    print('"gtts" Module import completed successfully')

    print('Importing "subprocess" Module')
    import subprocess
    print('"subprocess" Module import completed successfully')

    print('Importing "webbrowser" Module')
    import webbrowser
    print('"webbrowser" Module import completed successfully')

    print('Importing "datetime" Module')
    import datetime
    print('"datetime" Module import completed successfully')

    print('Importing "pickle" Module')
    import pickle
    print('"pickle" Module import completed successfully')

    print('Importing "os.path" Module')
    import os.path
    print('"os.path" Module import completed successfully')

    print('Importing "googleapiclient.discovery" Module')
    from googleapiclient.discovery import build
    print('"googleapiclient.discovery" Module import completed successfully')

    print('Importing "google_auth_oauthlib.flow" Module')
    from google_auth_oauthlib.flow import InstalledAppFlow
    print('"google_auth_oauthlib.flow" Module import completed successfully')

    print('Importing "google.auth.transport.requests" Module')
    from google.auth.transport.requests import Request
    print('"google.auth.transport.requests" Module import completed successfully')

    print('Importing "pyttsx3" Module')
    import pyttsx3
    print('"pyttsx3" Module import completed successfully')

    print('Importing "pytz" Module')
    import pytz
    print('"pytz" Module import completed successfully')

#
# Ending import section and if errors occur
# It will be consoled with explanation
#

except ImportError as e:
    print("Import of modules has failed with error of: " + str(e.name))


#
# Global Scopic Variables
# Used for public functions
#

#
# Google Calendar API Scope
#

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

#
# Name of months
#

MONTHS = ["january",
          "february",
          "march",
          "april",
          "may",
          "june",
          "july",
          "august",
          "september",
          "october",
          "november",
          "december"]

#
# Name of days
#

DAYS = ["monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday"]

#
# Name of number extensions
#

DAYS_EXTENSIONS = ["st",
                   "nd",
                   "rd",
                   "th"]


#
# The Speak Function
# Used to make assistant speak something
#

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 130)
    engine.setProperty('volume', 1)
    Sarah = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    engine.setProperty('voice', Sarah)
    engine.say(text)
    engine.runAndWait()
    pass


#
# The Listen Function
# Used to make assistant listen user and get audio
#

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception " + str(e))

    return said.lower()


#
# The Google Authentication Function
# Used to make assistant authenticate user to google
#

def authenticate_google():
    creds = None

    #
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    #

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    #
    # If there are no (valid) credentials available, let the user log in.
    #

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        #
        # Save the credentials for the next run
        #

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


#
# The Google Event Handler
# Used to make assistant authenticate user to google
#

def get_events(day, service):

    #
    # Setting up local timezone
    #

    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    #
    # Call the Calendar API
    #

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    #
    # If there are no events, reply it
    #

    if not events:
        speak('No upcoming events found.')

    #
    # Or display the results
    #

    else:
        speak(f"You have {len(events)} events on this day.")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])

            #
            # Let assistant learn how to pronounce 24 o'clock system in 12 one
            #

            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0]) - 12) + start_time.split(":")[1]
                start_time = start_time + "pm"

            #
            # Speak the achieved result
            #

            speak(event["summary"] + " at " + start_time)

#
# The Date Function
# Used to make assistant calculate current time
#

def get_date(text):

    #
    # Text receive time
    #

    text = text.lower()
    today = datetime.date.today()

    #
    # Nulling current date
    #

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    #
    # There begins fun
    #

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAYS_EXTENSIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year = year + 1

    if day < today.day and month == -1 and day != -1:
        month = month + 1

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if month == -1 or day == -1:
        return None

    return datetime.date(month=month, day=day, year=year)


#
# The Note Function
# Used to make assistant save notes
#

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    #
    # Open the note with Notepad
    #

    subprocess.Popen(["notepad.exe", file_name])


#
# Creating main function that handles all logic
#

def main():

    #
    # Letting the bot to introduce himself
    #

    speak("Hello, my name is Sarah and I am your voice assistant!")
    speak("What would you like to do with me?")

    #
    # Make the assistant wait for waking word to be pronounced by user
    # Converting input to string variable and saving as variable
    #
    WAKE = "hey sarah"
    service = authenticate_google()
    print("Start")

    while True:
        print("Listening")
        text = get_audio()

        if text.count(WAKE) > 0:
            speak("I am ready oni chan!")
            text = get_audio()

            CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]
            for phrase in CALENDAR_STRS:
                if phrase in text:
                    date = get_date(text)
                    if date:
                        get_events(get_date(text), service)
                    else:
                        speak("I don't understand")

            NOTE_STRS = ["make a note", "write this down", "remember this"]
            for phrase in NOTE_STRS:
                if phrase in text:
                    speak("What would you like me to write down?")
                    note_text = get_audio()
                    note(note_text)
                    speak("I've created the note file.")

            #
            # There begins our logic
            #

            # Just ordinary speech to speech responses
            if "hello" in text:
                speak("Hello, how are you?")

            if "what is your name" in text:
                speak("My name is Sara")

            if "anime" in text:
                anime_website_url = "https://mover.uz/video/anime/"
                speak("Opening animes in browser")
                webbrowser.open(anime_website_url)

            if "news" in text:
                news_website_url = "https://review.uz"
                speak("Opening fresh news page")
                webbrowser.open(news_website_url)


if __name__ == '__main__':
    main()
